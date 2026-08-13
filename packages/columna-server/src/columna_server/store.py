"""
columna_server.store — the Manifold store (WP-2.1 stub: a directory of Manifolds).

Layout (per WP-2.2 spec):

    <manifolds_dir>/
      <manifold_id>/
        manifold.cml     # the Frame-QL Manifold definition (parsed by columna-core)
        data.toml        # connector type + data path

    data.toml:
        [manifold]                 # optional metadata
        name = "Benchmark"
        description = "..."
        [connector]
        type = "duckdb"            # only "duckdb" in Core
        warehouse = "warehouse"   # dir of parquet, relative to this manifold dir (or absolute)

Every Manifold is parsed and its backend loaded ONCE at startup. `list_manifolds` / `describe_*`
read from the parsed object and never touch data; `query` / `explain` go through the per-Manifold
`ExecutionProvider` (a `CoreExecutionProvider` over `ManifoldServer` today). `explain` uses `plan()`
and must not increment the connector's fetch count.
"""
from __future__ import annotations

import glob
import os
import os.path as _osp
from dataclasses import dataclass
from typing import Optional

try:                       # py3.11+
    import tomllib
except ModuleNotFoundError:  # py3.10
    import tomli as tomllib

from columna_core import DuckDBConnector, ManifoldServer
from columna_core.parser import parse_file

from .provider import CoreExecutionProvider, ExecutionProvider
from .registry import (
    FolderManifoldRegistry,
    GovernedPublication,
    ManifoldRef,
    ManifoldRegistry,
    ManifoldSelector,
    NotRealizableHere,
    PublicationArtifactError,
    PublicationNotFound,
    ResolvedManifold,
    governed_publication_from_artifact,
    load_publication_artifact,
    source_ref_of,
)

#: The publication-authority artifact retained beside a governed .cml realization (S2.2a-2/-3). The
#: runtime deployment contract for artifact-backed Core serving is:
#:     <runtime-manifold>/{governed-publication.json, manifold.cml, data.toml}
PUBLICATION_ARTIFACT = "governed-publication.json"

# ── the three runtime-entry kinds (S2.2a-3) ────────────────────────────────────────────────────────
#: no SOURCE_MANIFOLD — an id-only legacy runtime, compatibility-served, never governed.
ENTRY_LEGACY = "legacy"
#: a concrete SOURCE_MANIFOLD but no (or unusable) governed-publication.json — a *source-referenced
#: runtime with incomplete publication authority*. Compatibility-served for now; NEVER a
#: GovernedPublication, NEVER in the governed registry. Missing authority never manufactures a
#: publication (the P0(c) migration discipline).
ENTRY_SOURCE_REFERENCED_INCOMPLETE = "source_referenced_incomplete"
#: governed-publication.json present AND its ref matches the .cml SOURCE_MANIFOLD — a real governed
#: publication with a Core realization bound by concrete ManifoldRef.
ENTRY_GOVERNED = "governed"


@dataclass(frozen=True)
class LoadCondition:
    """An observable per-runtime ingest condition — the deployment gap made visible, never silently
    swallowed. ``kind`` is the class name of the underlying registry condition
    (PublicationArtifactMissing / PublicationArtifactInvalid / UnsupportedPublicationFormat /
    RealizationIdentityMismatch)."""

    manifold_id: str
    kind: str
    detail: str


@dataclass
class LoadedManifold:
    manifold_id: str
    name: str
    description: str
    manifold: object              # columna_core.model.Manifold — the logical/read model
    provider: ExecutionProvider   # execution capability (the seam); the concrete Core
    #                               runtime lives on CoreExecutionProvider.runtime, not here
    # Governed identity (S2.2a-3). ``publication``/``ref`` are set ONLY for a governed entry —
    # an artifact present AND matching the .cml SOURCE_MANIFOLD. Its ref/logical/authority come
    # from governed-publication.json, never from the .cml. A source-referenced-but-incomplete or
    # legacy entry carries no publication (never fabricated).
    publication: Optional[GovernedPublication] = None
    ref: Optional[ManifoldRef] = None
    entry_kind: str = ENTRY_LEGACY
    condition: Optional[LoadCondition] = None
    # The concrete ManifoldRef the .cml CLAIMS to realize (its SOURCE_MANIFOLD), or None for a
    # legacy runtime. A runtime's claim about publication origin — NOT established authority; for a
    # governed entry it equals ``ref``, for an authority-incomplete entry it is the row's source_ref.
    source_ref: Optional[ManifoldRef] = None


def _load_duckdb(warehouse_dir: str):
    import duckdb

    con = duckdb.connect()
    files = sorted(glob.glob(os.path.join(warehouse_dir, "*.parquet")))
    if not files:
        raise FileNotFoundError(f"no parquet files under connector warehouse {warehouse_dir!r}")
    for f in files:
        table = os.path.basename(f)[:-8]
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_parquet('{f}')")
    return con


def _load_one(manifold_id: str, mdir: str) -> LoadedManifold:
    cml = os.path.join(mdir, "manifold.cml")
    toml_path = os.path.join(mdir, "data.toml")
    if not os.path.isfile(cml):
        raise FileNotFoundError(f"manifold '{manifold_id}': missing manifold.cml")
    if not os.path.isfile(toml_path):
        raise FileNotFoundError(f"manifold '{manifold_id}': missing data.toml")

    with open(toml_path, "rb") as f:
        cfg = tomllib.load(f)
    meta = cfg.get("manifold", {})
    conn = cfg.get("connector", {})
    ctype = conn.get("type", "duckdb")
    if ctype != "duckdb":
        raise ValueError(f"manifold '{manifold_id}': connector type {ctype!r} is not supported "
                         f"(Core supports 'duckdb')")

    manifold = parse_file(cml)
    errs = manifold.check()
    if errs:
        raise ValueError(f"manifold '{manifold_id}' is not well-formed: {errs}")

    warehouse = conn.get("warehouse")
    if not warehouse:
        raise ValueError(f"manifold '{manifold_id}': [connector].warehouse is required")
    if not os.path.isabs(warehouse):
        warehouse = os.path.join(mdir, warehouse)
    con = _load_duckdb(os.path.abspath(warehouse))
    server = ManifoldServer(manifold, DuckDBConnector(con))

    # WP-B: adjudicate declared derived-column fertility at load — the publish-time integrity gate.
    # A CONTRADICTED declaration fails closed here (the manifold does not load), and the constructed
    # licenses populate the members so describe can expose them. A no-fertility manifold is a no-op.
    from columna_core import adjudicate, Contradiction
    try:
        adjudicate(server)
    except Contradiction as e:
        raise ValueError(f"manifold '{manifold_id}' fails adjudication (fertility refuted by the "
                         f"attested data): {e}")

    # Governed identity (S2.2a-3): three-way classification. A GovernedPublication is built ONLY from
    # a co-located governed-publication.json whose ref matches the .cml's SOURCE_MANIFOLD claim — its
    # ref/logical/authority come from the artifact, never from the .cml. A .cml with a SOURCE_MANIFOLD
    # but no (or unusable) artifact is source-referenced-but-authority-incomplete: still
    # compatibility-served, never promoted to governance. A .cml without SOURCE_MANIFOLD is legacy.
    src_ref = source_ref_of(manifold)
    artifact_path = _osp.join(mdir, PUBLICATION_ARTIFACT)
    publication: Optional[GovernedPublication] = None
    ref: Optional[ManifoldRef] = None
    entry_kind = ENTRY_LEGACY
    condition: Optional[LoadCondition] = None

    if _osp.isfile(artifact_path):
        try:
            artifact = load_publication_artifact(artifact_path)
        except PublicationArtifactError as e:
            # Present but unusable (malformed/unsupported): observable, not fatal to the install.
            entry_kind = ENTRY_SOURCE_REFERENCED_INCOMPLETE if src_ref else ENTRY_LEGACY
            condition = LoadCondition(manifold_id, type(e).__name__, str(e))
        else:
            if src_ref is None or src_ref != artifact.ref:
                # The .cml does not (or wrongly) claim to realize this publication: do not bind.
                claimed = "no SOURCE_MANIFOLD" if src_ref is None else f"{src_ref.manifold_id}@{src_ref.version}"
                entry_kind = ENTRY_SOURCE_REFERENCED_INCOMPLETE if src_ref else ENTRY_LEGACY
                condition = LoadCondition(
                    manifold_id, "RealizationIdentityMismatch",
                    f"artifact ref {artifact.ref.manifold_id}@{artifact.ref.version} != .cml {claimed}",
                )
            else:
                publication = governed_publication_from_artifact(artifact)
                ref = artifact.ref
                entry_kind = ENTRY_GOVERNED
    elif src_ref is not None:
        # Source-referenced runtime with incomplete publication authority (no artifact present).
        entry_kind = ENTRY_SOURCE_REFERENCED_INCOMPLETE
        condition = LoadCondition(
            manifold_id, "PublicationArtifactMissing",
            f"{src_ref.manifold_id}@{src_ref.version} has no {PUBLICATION_ARTIFACT}",
        )

    return LoadedManifold(
        manifold_id=manifold_id,
        name=meta.get("name", manifold_id),
        description=meta.get("description", ""),
        manifold=manifold,
        provider=CoreExecutionProvider(server),
        publication=publication,
        ref=ref,
        entry_kind=entry_kind,
        condition=condition,
        source_ref=src_ref,
    )


class ManifoldStore:
    """All Manifolds under a directory, parsed and connected once at construction."""

    def __init__(self, manifolds_dir: str):
        self.dir = os.path.abspath(manifolds_dir)
        if not os.path.isdir(self.dir):
            raise FileNotFoundError(f"manifolds dir not found: {self.dir}")
        self._loaded: dict[str, LoadedManifold] = {}
        for entry in sorted(os.listdir(self.dir)):
            mdir = os.path.join(self.dir, entry)
            if os.path.isdir(mdir) and os.path.isfile(os.path.join(mdir, "manifold.cml")):
                self._loaded[entry] = _load_one(entry, mdir)
        if not self._loaded:
            raise FileNotFoundError(f"no manifolds (<id>/manifold.cml) found under {self.dir}")

        # The governed-publication registry (WHICH), plus this installation's provider realizations
        # (HOW), derived from the loaded entries. ONLY governed entries (artifact present AND matching
        # the .cml SOURCE_MANIFOLD) enter the registry and bind a provider — the exact-ref-match gate
        # was already applied in _load_one, so a mismatch never reaches this point with a publication.
        # Legacy and source-referenced-but-incomplete entries carry no publication and are absent from
        # the registry; they remain reachable through the compatibility get()/ids()/all() below.
        pubs: dict[ManifoldRef, GovernedPublication] = {}
        self._providers_by_ref: dict[ManifoldRef, ExecutionProvider] = {}
        self._loaded_by_ref: dict[ManifoldRef, LoadedManifold] = {}
        self._conditions: list[LoadCondition] = []
        for lm in self._loaded.values():
            if lm.condition is not None:
                self._conditions.append(lm.condition)
            if lm.publication is not None and lm.ref is not None:
                pubs[lm.ref] = lm.publication
                self._providers_by_ref[lm.ref] = lm.provider
                self._loaded_by_ref[lm.ref] = lm
        self._registry: ManifoldRegistry = FolderManifoldRegistry(pubs)

    # ── compatibility surface (unchanged; folder-keyed) ──────────────────────────────────────────
    def ids(self) -> list[str]:
        return list(self._loaded)

    def get(self, manifold_id: str) -> LoadedManifold:
        lm = self._loaded.get(manifold_id)
        if lm is None:
            raise KeyError(manifold_id)
        return lm

    def all(self) -> list[LoadedManifold]:
        return list(self._loaded.values())

    # ── governed identity surface (S2.1/S2.2a-3; additive — no wire/API change) ───────────────────
    def registry(self) -> ManifoldRegistry:
        """The governed-publication registry (WHICH). Governed publications only; legacy and
        source-referenced-but-authority-incomplete entries are not published governance and are absent
        from it."""
        return self._registry

    def conditions(self) -> list[LoadCondition]:
        """The observable per-runtime ingest conditions (S2.2a-3) — missing/invalid/unsupported
        artifacts and realization-identity mismatches. Preserved so the deployment gap (an artifact
        not yet co-located with its realization) is visible, never silently swallowed."""
        return list(self._conditions)

    def resolve(self, selector: ManifoldSelector) -> ResolvedManifold:
        """Serving resolution: join WHICH (the governed publication, from the registry) with HOW (this
        installation's provider for its ref). ``provider is None`` on the result means *not realizable
        here* — the publication exists but this installation cannot serve it. Raises
        ``PublicationNotFound`` when no such governed publication exists."""
        publication = self._registry.resolve(selector)
        provider = self._providers_by_ref.get(publication.ref)
        return ResolvedManifold(publication=publication, provider=provider)

    def governed_ids(self) -> list[str]:
        """The stable ids of the known governed publication lineages (each has ≥1 published version)."""
        return sorted({r.manifold_id for r in self._registry.list()})

    def realizable_refs(self) -> set[ManifoldRef]:
        """The concrete governed refs this installation can realize (has a bound provider for) — an
        INSTALLATION fact, distinct from publication existence in the registry."""
        return set(self._providers_by_ref)

    def resolve_public(
        self, manifold_id: str, version: Optional[str] = None
    ) -> "tuple[LoadedManifold, Optional[ManifoldRef]]":
        """Governed-first PUBLIC resolution (S2.2b-1). Returns ``(loaded, resolved_ref)`` where
        ``resolved_ref`` is the concrete governed ``ManifoldRef`` (disclose its version) or ``None`` for
        a compatibility runtime (unversioned — nothing to disclose).

        The deterministic rule — governed publication identity OUTRANKS compatibility-folder identity
        for the same logical id; no filesystem/load-order choice is ever made:

            manifold_id names a governed lineage
                → resolve through the registry (exact version, or highest published semver)
                → raises PublicationNotFound (unknown version) / NotRealizableHere (no provider here)
            else, version supplied      → PublicationNotFound (compatibility runtimes are unversioned)
            else, version omitted       → compatibility store.get(manifold_id) (raises KeyError if none)
        """
        if self._registry.latest(manifold_id) is not None:
            resolved = self.resolve(ManifoldSelector(manifold_id, version))  # raises PublicationNotFound
            if resolved.provider is None:
                ref = resolved.publication.ref
                raise NotRealizableHere(f"{ref.manifold_id}@{ref.version}")
            return self._loaded_by_ref[resolved.publication.ref], resolved.publication.ref
        if version is not None:
            raise PublicationNotFound(f"{manifold_id}@{version}")
        return self.get(manifold_id), None  # compatibility fallback (raises KeyError if unknown)

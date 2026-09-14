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
from .lowering_receipt import (
    LOWERING_RECEIPT,
    LoweringReceiptError,
    LoweringReceiptMissing,
    load_lowering_receipt,
    verify_binding,
)
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
#:     <runtime-manifold>/{governed-publication.json, manifold.cml, lowering-receipt.json, data.toml}
#: `lowering-receipt.json` joined the contract with the publication→image binding (2026-08-22): a
#: SOURCE_MANIFOLD claim plus an artifact is an ORIGIN CLAIM, not evidence that a compiler ever
#: established the realization. See lowering_receipt.py.
PUBLICATION_ARTIFACT = "governed-publication.json"

# ── the three runtime-entry kinds (S2.2a-3) ────────────────────────────────────────────────────────
#: no SOURCE_MANIFOLD — an id-only legacy runtime, compatibility-served, never governed.
ENTRY_LEGACY = "legacy"
#: a concrete SOURCE_MANIFOLD but no (or unusable) governed-publication.json — a *source-referenced
#: runtime with incomplete publication authority*. Compatibility-served for now; NEVER a
#: GovernedPublication, NEVER in the governed registry. Missing authority never manufactures a
#: publication (the P0(c) migration discipline).
ENTRY_SOURCE_REFERENCED_INCOMPLETE = "source_referenced_incomplete"
# ── runtime selection: an OPERATIONAL fact, kept apart from every governed one ────────────────────
#: Which execution runtime a deployment has chosen for one manifold. THIS IS NOT A GOVERNED FACT and
#: not an artifact kind (ruled Huayin, 2026-09-12 §3/§8). Three things stay separate here, and the
#: separation is the ruling:
#:
#:     the governed publication major        a fact about the ARTIFACT
#:     the presence/absence of `manifold.cml`  a fact about the DEPLOYED UNIT
#:     the selected execution provider       a fact about THIS INSTALLATION
#:
#: A v2 artifact therefore never activates the successor runtime by existing. Selection is explicit,
#: or it is Core.
RUNTIME_CORE = "core"
RUNTIME_PLATFORM = "platform"

#: PROVISIONAL, and deliberately the smallest thing that works (ruled §8: "do not freeze a larger
#: deployment-manifest design from one slice"). `COLUMNA_RUNTIME="lighthouse=platform,demo=core"`.
#: The permanent home for deployment configuration is not decided by this proof, and this name is
#: expected to move when it is.
RUNTIME_ENV_VAR = "COLUMNA_RUNTIME"


class RuntimeSelectionError(ValueError):
    """A deployment selected a runtime that this unit cannot satisfy — raised AT CONSTRUCTION.

    FAIL CLOSED, LOUDLY, AND EARLY. The alternatives were both worse: serving the unit through the
    other runtime would be the silent provider switch §8 forbids, and dropping it from the catalog
    would let a misconfigured deployment look like a correctly-configured smaller one. An operator
    who names a runtime is making a claim about what this installation is; if the claim cannot be
    honoured, the installation should not come up pretending otherwise."""


def parse_runtime_selection(spec: Optional[str]) -> dict:
    """`"lighthouse=platform,demo=core"` → `{"lighthouse": "platform", "demo": "core"}`.

    A malformed entry RAISES rather than being skipped: a deployment that typed the configuration
    wrong and got the default runtime anyway would be the quietest possible way to serve the wrong
    thing. Empty or unset means no selections, which means everything is Core, which is today."""
    out: dict = {}
    for chunk in (spec or "").split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        mid, sep, chosen = chunk.partition("=")
        if not sep or not mid.strip() or not chosen.strip():
            raise RuntimeSelectionError(
                f"{RUNTIME_ENV_VAR} entry {chunk!r} is not `<manifold_id>=<runtime>`")
        out[mid.strip()] = chosen.strip()
    return out



#: governed-publication.json present AND its ref matches the .cml SOURCE_MANIFOLD AND a valid
#: lowering-receipt.json binds this exact publication to this exact execution image — a real governed
#: publication with a Core realization bound by concrete ManifoldRef and by established provenance.
#: The receipt requirement is publication STANDING only: it says a compiler produced this image from
#: this publication, and says nothing about certification, attestation or PublishedScope admission.
ENTRY_GOVERNED = "governed"


@dataclass(frozen=True)
class LoadCondition:
    """An observable per-runtime ingest condition — the deployment gap made visible, never silently
    swallowed. ``kind`` is the class name of the underlying registry or receipt condition
    (PublicationArtifactMissing / PublicationArtifactInvalid / UnsupportedPublicationFormat /
    RealizationIdentityMismatch / LoweringReceiptMissing / LoweringReceiptInvalid /
    LoweringReceiptMismatch). Every kind the store can emit MUST have a stable public code in
    tools._CONDITION_CODE — an unmapped kind would vanish from the catalog instead of being
    reported, which is the one failure this dataclass exists to prevent."""

    manifold_id: str
    kind: str
    detail: str


@dataclass
class LoadedManifold:
    manifold_id: str
    name: str
    description: str
    #: columna_core.model.Manifold — the legacy logical/read model, or **None** for a
    #: SUCCESSOR-NATIVE governed unit that ships no `manifold.cml` (ruled §2). `.cml` is a legacy
    #: Core execution artifact and a private ontology; it is not baggage a governed unit must carry,
    #: so its absence is represented as absence and never as an empty stand-in. Only the legacy Core
    #: provider requires it.
    manifold: Optional[object]
    #: Execution capability (the seam), or **None** when this installation has no realization for
    #: the unit. Not a new state: `resolve_public` already raises `NotRealizableHere` for exactly
    #: this, and the wire already says `not_realizable_here`.
    provider: Optional[ExecutionProvider]
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
    #: THE THREE SEPARATE FACTS (§3). Which runtime this deployment selected; whether a legacy `.cml`
    #: is present; which publication major the artifact was read as. None of the three implies
    #: another, and no combination of the first two is allowed to select the third or be selected by
    #: it — provider choice is operational, artifact major is governed, `.cml` presence is packaging.
    runtime: str = RUNTIME_CORE
    has_cml: bool = True
    publication_major: Optional[int] = None
    #: Where this unit's governed artifact lives, when it has one. Carried so a governed-native
    #: read-only surface can resolve a reference THROUGH THE v2 CONTRACT'S OWN READER rather than
    #: reimplementing the lookup over the plain-data projection — the server holds a path, never a
    #: second name→family map.
    publication_path: Optional[str] = None


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


def _is_governed_only_unit(mdir: str) -> bool:
    """Does this `.cml`-less directory carry a v2 governed publication?

    ONLY v2, and only when it READS. A v1 artifact without its execution image is an incomplete
    LEGACY deployment, not a successor unit, and an unreadable artifact is not a unit either — both
    are left exactly as invisible as they are today, because making them newly fatal would change
    legacy behaviour to say something this unit was not asked to say. A deployment that MEANT either
    of them to be a successor unit finds out the moment it selects one: the selection path refuses,
    loudly and by name."""
    path = _osp.join(mdir, PUBLICATION_ARTIFACT)
    if not _osp.isfile(path):
        return False
    try:
        return load_publication_artifact(path).major == _PLATFORM_PUBLICATION_MAJOR
    except PublicationArtifactError:
        return False


def _load_governed_only(manifold_id: str, mdir: str, *, bind_provider: bool) -> LoadedManifold:
    """A SUCCESSOR-NATIVE governed runtime unit: a governed publication and NO `manifold.cml`.

    THE DEPLOYMENT UNIT IS THE PUBLICATION, not a lowered image (ruled Huayin, 2026-09-12 §2). A
    `.cml` is the legacy Core execution artifact and a private ontology; requiring one here would
    make every successor unit carry a file it must not read for meaning, purely to satisfy a loader.
    So this path builds no `Manifold`, opens no connector, and runs no adjudication — not because
    those are deferred, but because there is no legacy image for them to be about.

    NO LOWERING RECEIPT IS REQUIRED, AND THIS IS NOT A WEAKENING. The receipt discharges one specific
    obligation: that a compiler produced THIS EXECUTION IMAGE from THIS PUBLICATION. Where there is no
    image there is no such binding to attest, and demanding a receipt would be demanding evidence
    about a file the unit deliberately does not have. The receipt requirement is a property of the
    lowered path, and it stays exactly as strict there — see `_load_one`, unchanged.

    THE PROVIDER IS BOUND BY SELECTION, NEVER BY THE ARTIFACT (`bind_provider`). A v2 publication
    sitting in a directory makes the unit VISIBLE — a governed lineage this installation knows about
    — and nothing more. Only an explicit deployment selection binds the successor runtime to it.
    Unselected, it loads with no provider, which is not a new state: `NotRealizableHere` and the
    public `not_realizable_here` have always meant "the publication exists and this installation
    cannot serve it". No new catalog kind, no new condition code, no new public state.""" 
    artifact_path = _osp.join(mdir, PUBLICATION_ARTIFACT)
    if not _osp.isfile(artifact_path):
        raise RuntimeSelectionError(
            f"manifold '{manifold_id}': the deployment selects the {RUNTIME_PLATFORM!r} runtime, "
            f"which serves a governed publication, and this unit has no {PUBLICATION_ARTIFACT}")
    try:
        artifact = load_publication_artifact(artifact_path)
    except PublicationArtifactError as e:
        raise RuntimeSelectionError(
            f"manifold '{manifold_id}': the deployment selects the {RUNTIME_PLATFORM!r} runtime and "
            f"its {PUBLICATION_ARTIFACT} is unusable: {e}") from e
    if artifact.major != _PLATFORM_PUBLICATION_MAJOR:
        raise RuntimeSelectionError(
            f"manifold '{manifold_id}': a governed unit with no manifold.cml is served by the "
            f"{RUNTIME_PLATFORM!r} runtime, which requires "
            f"a publication of major {_PLATFORM_PUBLICATION_MAJOR}, and this artifact "
            f"is major {artifact.major}. A v{artifact.major} artifact is NOT read as v"
            f"{_PLATFORM_PUBLICATION_MAJOR}: its family law is not there to be found, and inferring "
            f"it is the defect v{_PLATFORM_PUBLICATION_MAJOR} exists to remove")

    return LoadedManifold(
        manifold_id=manifold_id,
        name=manifold_id,           # no data.toml to name it, and a fabricated name is a claim
        description="",
        manifold=None,              # no legacy image, honestly absent
        provider=_platform_provider(manifold_id, artifact_path) if bind_provider else None,
        publication=governed_publication_from_artifact(artifact),
        ref=artifact.ref,
        entry_kind=ENTRY_GOVERNED,
        condition=None,
        source_ref=artifact.ref,    # the unit IS the publication; origin and identity coincide
        runtime=RUNTIME_PLATFORM if bind_provider else RUNTIME_CORE,
        has_cml=False,
        publication_path=artifact_path,
        publication_major=artifact.major,
    )


def _platform_provider(manifold_id: str, artifact_path: str):
    """The successor runtime's provider, or a fail-closed refusal — NEVER a fallback to Core.

    THE IMPORT IS LAZY, AND THAT IS A PACKAGING FACT WORTH STATING. `columna-platform` is a
    workspace member that is deliberately NOT published and NOT in the release-set lockstep, so
    `columna-server` cannot declare a dependency on it without dragging it into the published
    triad. The consequence is honest and must not be hidden: THE SUCCESSOR RUNTIME IS SELECTABLE
    ONLY WHERE `columna-platform` IS INSTALLED — a source/workspace install today, not the shipped
    wheel. A deployment that selects it without the package gets a refusal that says so, at
    construction, rather than a unit that loads and then cannot answer.

    THE DEPENDENCY RUNS SERVER → PLATFORM, one way. Platform implements `ExecutionProvider`
    structurally (it is a `@runtime_checkable` Protocol) and imports nothing from this package,
    because `columna_server.store` imports `columna_core.parser` at module scope and importing the
    server from the successor path would drag the legacy execution stack into it."""
    try:
        from columna_platform.provider import PlatformExecutionProvider
    except ImportError as exc:                                   # pragma: no cover - env-dependent
        raise RuntimeSelectionError(
            f"manifold '{manifold_id}': the deployment selects the {RUNTIME_PLATFORM!r} runtime and "
            f"`columna-platform` is not installed in this environment ({exc}). That package is not "
            f"published, so the successor runtime is available only to a workspace install. There "
            f"is no fallback to the {RUNTIME_CORE!r} runtime") from exc
    return PlatformExecutionProvider.from_artifact(artifact_path, manifold_id=manifold_id)


#: The publication major a successor-native unit must carry. Not a general policy about which majors
#: the server READS (that is `SUPPORTED_PUBLICATION_FORMAT_MAJORS`, and it includes v1 for the legacy
#: path) — a requirement of THIS runtime, kept here so the two cannot be confused.
_PLATFORM_PUBLICATION_MAJOR = 2


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
    publication_major: Optional[int] = None

    if _osp.isfile(artifact_path):
        try:
            artifact = load_publication_artifact(artifact_path)
        except PublicationArtifactError as e:
            # Present but unusable (malformed/unsupported): observable, not fatal to the install.
            entry_kind = ENTRY_SOURCE_REFERENCED_INCOMPLETE if src_ref else ENTRY_LEGACY
            condition = LoadCondition(manifold_id, type(e).__name__, str(e))
        else:
            publication_major = artifact.major     # what it WAS, not what it selects
            if src_ref is None or src_ref != artifact.ref:
                # The .cml does not (or wrongly) claim to realize this publication: do not bind.
                claimed = "no SOURCE_MANIFOLD" if src_ref is None else f"{src_ref.manifold_id}@{src_ref.version}"
                entry_kind = ENTRY_SOURCE_REFERENCED_INCOMPLETE if src_ref else ENTRY_LEGACY
                condition = LoadCondition(
                    manifold_id, "RealizationIdentityMismatch",
                    f"artifact ref {artifact.ref.manifold_id}@{artifact.ref.version} != .cml {claimed}",
                )
            else:
                # The origin claim and the authority agree. That is IDENTITY, and identity is not
                # conformance: nothing so far shows a compiler ever produced this image from this
                # publication. The receipt is what carries that discharged obligation across the
                # lowering→provisioning boundary, so admission can trust it without re-running
                # lowering, loading the mapping, or reading meaning out of the .cml.
                receipt_path = _osp.join(mdir, LOWERING_RECEIPT)
                if not _osp.isfile(receipt_path):
                    e = LoweringReceiptMissing(
                        f"{artifact.ref.manifold_id}@{artifact.ref.version} has no "
                        f"{LOWERING_RECEIPT}: a SOURCE_MANIFOLD claim is an origin claim, not "
                        f"evidence that lowering established this image"
                    )
                    entry_kind = ENTRY_SOURCE_REFERENCED_INCOMPLETE
                    condition = LoadCondition(manifold_id, type(e).__name__, str(e))
                else:
                    try:
                        receipt = load_lowering_receipt(receipt_path)
                        verify_binding(receipt, artifact.ref, artifact_path, cml)
                    except LoweringReceiptError as e:
                        # Present but unusable, or usable but binding different files: observable,
                        # never auto-repaired, and never promoted.
                        entry_kind = ENTRY_SOURCE_REFERENCED_INCOMPLETE
                        condition = LoadCondition(manifold_id, type(e).__name__, str(e))
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
        runtime=RUNTIME_CORE,
        has_cml=True,
        publication_major=publication_major,
        publication_path=artifact_path if publication is not None else None,
    )


class ManifoldStore:
    """All Manifolds under a directory, parsed and connected once at construction."""

    def __init__(self, manifolds_dir: str, runtime_selection: Optional[dict] = None):
        """`runtime_selection` maps manifold_id → `RUNTIME_CORE` / `RUNTIME_PLATFORM`; when omitted it
        is read from `COLUMNA_RUNTIME`. UNSELECTED MEANS CORE, so every existing deployment loads
        exactly as it did — the successor runtime is reachable only by naming it."""
        self.dir = os.path.abspath(manifolds_dir)
        if not os.path.isdir(self.dir):
            raise FileNotFoundError(f"manifolds dir not found: {self.dir}")
        self.runtime_selection = (parse_runtime_selection(os.environ.get(RUNTIME_ENV_VAR))
                                  if runtime_selection is None else dict(runtime_selection))
        for mid, chosen in sorted(self.runtime_selection.items()):
            if chosen not in (RUNTIME_CORE, RUNTIME_PLATFORM):
                raise RuntimeSelectionError(
                    f"manifold '{mid}': unknown runtime {chosen!r} "
                    f"(known: {RUNTIME_CORE!r}, {RUNTIME_PLATFORM!r})")

        self._loaded: dict[str, LoadedManifold] = {}
        for entry in sorted(os.listdir(self.dir)):
            mdir = os.path.join(self.dir, entry)
            if not os.path.isdir(mdir):
                continue
            has_cml = os.path.isfile(os.path.join(mdir, "manifold.cml"))
            chosen = self.runtime_selection.get(entry)

            has_v2_only = (not has_cml) and _is_governed_only_unit(mdir)

            if chosen == RUNTIME_PLATFORM:
                # Successor-native, and NEVER a fallback: if this unit still carries a `.cml`, that
                # is a deployment saying two contradictory things about what it is, and guessing
                # which it meant is the silent provider switch this seam exists to prevent.
                if has_cml:
                    raise RuntimeSelectionError(
                        f"manifold '{entry}': the deployment selects the {RUNTIME_PLATFORM!r} "
                        f"runtime and the unit also ships manifold.cml. A successor-native unit is "
                        f"the publication; a lowered image beside it is a different unit, not a "
                        f"variant of this one")
                self._loaded[entry] = _load_governed_only(entry, mdir, bind_provider=True)
                continue

            if chosen == RUNTIME_CORE and not has_cml:
                # Explicitly selected Core with nothing for Core to execute. FAIL CLOSED — and in
                # particular do NOT quietly serve it through the successor runtime because an
                # artifact happens to be present.
                raise RuntimeSelectionError(
                    f"manifold '{entry}': the deployment selects the {RUNTIME_CORE!r} runtime and "
                    f"the unit has no manifold.cml, which that runtime executes. There is no "
                    f"fallback to another runtime")

            if has_cml:                                  # unchanged legacy discovery
                self._loaded[entry] = _load_one(entry, mdir)
            elif has_v2_only:
                # VISIBLE, UNSERVED. The publication is a governed fact this installation can see;
                # binding a runtime to it is a separate, explicit act. Loading it here is what lets
                # `not_realizable_here` be the honest answer instead of "no such manifold" — the
                # deployment gap made visible, which is the same discipline the load conditions
                # already follow.
                self._loaded[entry] = _load_governed_only(entry, mdir, bind_provider=False)

        missing = sorted(set(self.runtime_selection) - set(self._loaded))
        if missing:
            raise RuntimeSelectionError(
                f"the deployment selects a runtime for {missing}, which are not units under "
                f"{self.dir} — a selection naming nothing is a configuration error, not a no-op")
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
                self._loaded_by_ref[lm.ref] = lm
                if lm.provider is not None:
                    # A None provider must not enter this map: `realizable_refs()` is its key set, so
                    # registering one would advertise `realizable: true` for a unit nothing can serve.
                    self._providers_by_ref[lm.ref] = lm.provider
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

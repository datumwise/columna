"""
columna_server.registry — shared Manifold identity + a governed-publication registry (S2.1).

The registry answers **WHICH governed publication**; the serving layer (``store``) answers **HOW it
is served**. A Manifold is identified by a governed publication (stable id + concrete semantic
version), never by a folder layout or a ``.cml`` runtime artifact.

Identity discipline
-------------------
- ``ManifoldSelector`` is a *convenience input*: an id and an OPTIONAL version. It may be ambiguous
  (``version is None`` ⇒ "latest").
- ``ManifoldRef`` is a *resolved governed identity*: id + a CONCRETE semantic version. It is never
  ambiguous. **No implicit ``None`` version survives resolution.** "latest" is resolution policy,
  never identity.

Publication vs. runtime standing
--------------------------------
``GovernedPublication`` is IMMUTABLE meaning: its ``ref``, its physical-clean logical projection, and
its publication authority/provenance. It deliberately excludes runtime/provider standing — Core's
``PublishedScope``, current adjudication, data attestation, and provider availability are *not*
constitutive of a publication and can change without changing the publication.

Governance is never manufactured
--------------------------------
A ``.cml`` that carries a complete ``SOURCE_MANIFOLD <id> VERSION <semver>`` has a real governed
identity and becomes a ``GovernedPublication``. A source-identity-less ``.cml`` is a
``LegacyRuntimeEntry`` — compatibility-served, id-only, **not** promoted to a governed publication and
never given an invented id/version. Migration/compatibility may recover access; it never manufactures
governance (the P0(c) migration principle).

Ratification note (recorded, deferred): the ratification record established at publish (P0(c)) lives in
the Studio **publication bundle**, not in the ``.cml`` runtime artifact (the ``.cml`` grammar has no
ratification construct). A registry built over bare ``.cml`` folders therefore carries source identity
but not the ratification record; ``PublicationAuthority.ratification`` is left ``None`` rather than
fabricated. Ingesting publication bundles (so serving carries the ratification record) is a later step.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional, Protocol, runtime_checkable

#: The publication-artifact format major this server understands (matches
#: manifold_agent.publication.PUBLICATION_FORMAT_VERSION's major). Its own dimension — unrelated to
#: the wire CONTRACT_VERSION, columna-core's engine VERSION, or the Manifold's semantic version.
SUPPORTED_PUBLICATION_FORMAT_MAJOR = 1


# ── identity ─────────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class ManifoldSelector:
    """A convenience selector. ``version is None`` means "latest published" — resolution policy, not
    identity. It must resolve to a concrete ``ManifoldRef`` before anything governed happens."""

    manifold_id: str
    version: Optional[str] = None


@dataclass(frozen=True)
class ManifoldRef:
    """A resolved governed identity: stable id + CONCRETE semantic version. Never ambiguous."""

    manifold_id: str
    version: str


# ── publication authority (immutable provenance — NOT runtime standing) ──────────────────────────
@dataclass(frozen=True)
class PublicationAuthority:
    """Immutable publication authority/provenance. Excludes runtime standing (PublishedScope, current
    adjudication, data attestation, provider availability) by construction.

    ``ratification`` is the P0(c) ratification record when the source artifact carries it; it is
    ``None`` when the artifact (e.g. a bare ``.cml``) does not — never fabricated.
    """

    source_manifold_id: str
    source_manifold_version: str
    ratification: Optional[Any] = None
    actor: Optional[str] = None
    at: Optional[str] = None


@dataclass(frozen=True)
class GovernedPublication:
    """One immutable governed publication: a concrete ``ref``, a physical-clean logical projection
    (from the governed-publication artifact — no table/column/reject/realization), and immutable
    authority/provenance. All three come from ``governed-publication.json``, never from the ``.cml``."""

    ref: ManifoldRef
    logical: dict
    authority: PublicationAuthority


@dataclass(frozen=True)
class LegacyRuntimeEntry:
    """An id-only Core runtime served for compatibility. NOT a governed publication: it has no real
    source id/version and no publication authority, and is never promoted to one."""

    manifold_id: str


# ── errors / serving-resolution outcome ──────────────────────────────────────────────────────────
class PublicationNotFound(KeyError):
    """No such governed publication (unknown id, or unknown version for a known id)."""


class NotRealizableHere(Exception):
    """The publication exists but this installation has no provider/realization for it. This is
    availability/capability state — NOT an analytical refusal mood; do not route it through the wire's
    four moods."""


class RealizationIdentityMismatch(Exception):
    """A governed-publication artifact and a co-located ``.cml`` realization claim DISAGREE on the
    concrete ``ManifoldRef`` (``artifact.ref`` != ``.cml SOURCE_MANIFOLD``). The provider must not
    attach as the realization of that publication — an invalid realization binding, never an
    authority-selection rule, never auto-repaired."""


class PublicationArtifactError(Exception):
    """Base for problems reading a ``governed-publication.json`` — a pre-adjudication serving/ingest
    condition, never an analytical mood."""


class PublicationArtifactMissing(PublicationArtifactError):
    """A runtime carries a concrete ``SOURCE_MANIFOLD`` ref but no ``governed-publication.json`` — a
    source-referenced runtime with INCOMPLETE publication authority. It may stay compatibility-served,
    but it must never become a ``GovernedPublication`` (missing authority never manufactures one)."""


class PublicationArtifactInvalid(PublicationArtifactError):
    """The artifact claims a supported format but is malformed or structurally inconsistent (bad JSON,
    missing/!concrete ref, wrong declaration/authority shape, ratification keys that do not correspond
    to universes). A deployment/artifact defect — distinct from an unsupported format."""


class UnsupportedPublicationFormat(PublicationArtifactError):
    """The artifact may be perfectly valid but its ``publication_format_version`` major is one this
    server does not understand — a server/artifact version-compatibility problem, distinct from a
    malformed artifact."""


@dataclass
class ResolvedManifold:
    """The serving layer's join of WHICH (publication) and HOW (provider). ``provider is None`` means
    *not realizable here* — the publication exists but this installation cannot serve it."""

    publication: GovernedPublication
    provider: Optional[Any] = None  # an ExecutionProvider; Optional to model not-realizable-here


# ── the registry (WHICH) ─────────────────────────────────────────────────────────────────────────
def _semver_key(version: str) -> Optional[tuple[int, int, int]]:
    """(major, minor, patch) for ordering; None if not a plain semantic version. Pre-release/build
    metadata is out of scope for "latest" selection in S1.1-era artifacts."""
    core = version.split("-", 1)[0].split("+", 1)[0]
    parts = core.split(".")
    if len(parts) != 3:
        return None
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return None


@runtime_checkable
class ManifoldRegistry(Protocol):
    """WHICH governed publication? Pure identity/lookup — it never returns a runtime handle or a path,
    and it knows nothing about how (or whether) a publication is served here."""

    def list(self) -> list[ManifoldRef]:
        """Every governed publication ref this registry knows (id + concrete version)."""
        ...

    def resolve(self, selector: ManifoldSelector) -> GovernedPublication:
        """Resolve a (possibly version-less) selector to one immutable governed publication.
        ``version is None`` resolves to ``latest``. Raises ``PublicationNotFound`` if none matches."""
        ...

    def latest(self, manifold_id: str) -> Optional[str]:
        """The highest valid published semantic version for an id, or ``None`` if the id is unknown.
        Deterministic: highest ``(major, minor, patch)`` — never folder name or filesystem recency."""
        ...


class FolderManifoldRegistry:
    """The first local ``ManifoldRegistry``: governed publications discovered from parsed ``.cml``
    folders (a folder becomes governed iff its ``.cml`` carries ``SOURCE_MANIFOLD id VERSION semver``).

    Constructed from already-parsed publications so it stays free of filesystem/parse concerns; the
    ``store`` builds it. Multiple versions of the same id coexist without collision.
    """

    def __init__(self, publications: dict[ManifoldRef, GovernedPublication]):
        self._pubs = dict(publications)
        self._by_id: dict[str, list[str]] = {}
        for ref in self._pubs:
            self._by_id.setdefault(ref.manifold_id, []).append(ref.version)

    def list(self) -> list[ManifoldRef]:
        return sorted(self._pubs, key=lambda r: (r.manifold_id, _semver_key(r.version) or (0, 0, 0)))

    def latest(self, manifold_id: str) -> Optional[str]:
        versions = [v for v in self._by_id.get(manifold_id, []) if _semver_key(v) is not None]
        if not versions:
            return None
        return max(versions, key=lambda v: _semver_key(v))  # type: ignore[arg-type]

    def resolve(self, selector: ManifoldSelector) -> GovernedPublication:
        version = selector.version
        if version is None:
            version = self.latest(selector.manifold_id)
            if version is None:
                raise PublicationNotFound(selector.manifold_id)
        ref = ManifoldRef(selector.manifold_id, version)
        pub = self._pubs.get(ref)
        if pub is None:
            raise PublicationNotFound(f"{selector.manifold_id}@{version}")
        return pub


# ── the governed-publication artifact (S2.2a-3: authoring authority, consumed as plain data) ───────
@dataclass(frozen=True)
class PublicationArtifactData:
    """The server's minimal, plain-data reading of a ``governed-publication.json`` — the durable
    output of the governed-publish path (manifold_agent v0.12.0). Read with the stdlib only; the
    server never imports ``manifold_agent`` and never re-runs authored-Manifold governance."""

    format_version: str
    ref: ManifoldRef
    logical: dict          # the artifact's physical-clean logical projection, AUTHORING vocabulary
    authority: dict        # {published_by, published_at, ratifications{universe -> record}}


def _artifact_major(version: str) -> int:
    try:
        return int(str(version).split(".", 1)[0])
    except (ValueError, AttributeError) as exc:
        raise PublicationArtifactInvalid(
            f"unreadable publication_format_version {version!r}: expected 'MAJOR.MINOR'"
        ) from exc


def parse_publication_artifact(data: Any) -> PublicationArtifactData:
    """Structurally validate a governed-publication artifact and return its plain-data reading.

    This checks ARTIFACT STRUCTURE only — supported format major, a concrete ref, the
    declaration-native ``logical`` shape (``kind``/``name``/``body``), the ``authority`` shape, and
    the format-contract correspondence ``{universe names} == {ratification keys}``. It NEVER re-runs
    authored-declaration semantics, universe-law resolution, ``elf-1`` fingerprinting, or
    RATIFIED/STALE currency — authoring already adjudicated those; serving consumes them.

    Raises ``UnsupportedPublicationFormat`` for an unknown format major, ``PublicationArtifactInvalid``
    for any structural defect.
    """
    if not isinstance(data, dict):
        raise PublicationArtifactInvalid("artifact is not a JSON object")
    fmt = data.get("publication_format_version")
    if not isinstance(fmt, str) or not fmt:
        raise PublicationArtifactInvalid("missing publication_format_version")
    if _artifact_major(fmt) != SUPPORTED_PUBLICATION_FORMAT_MAJOR:
        raise UnsupportedPublicationFormat(
            f"publication_format_version {fmt!r} has an unsupported major (this server supports "
            f"major {SUPPORTED_PUBLICATION_FORMAT_MAJOR})"
        )
    ref = data.get("ref")
    if not isinstance(ref, dict):
        raise PublicationArtifactInvalid("missing ref object")
    mid, ver = ref.get("manifold_id"), ref.get("version")
    if not isinstance(mid, str) or not mid or not isinstance(ver, str) or not ver:
        raise PublicationArtifactInvalid("ref must carry a concrete manifold_id and version")

    logical = data.get("logical")
    if not isinstance(logical, dict) or not isinstance(logical.get("declarations"), list):
        raise PublicationArtifactInvalid("logical.declarations must be a list")
    universe_names: list[str] = []
    for decl in logical["declarations"]:
        if (not isinstance(decl, dict) or not isinstance(decl.get("kind"), str)
                or not isinstance(decl.get("name"), str) or not isinstance(decl.get("body"), dict)):
            raise PublicationArtifactInvalid("each logical declaration needs kind/name/body")
        if decl["kind"] == "universe":
            universe_names.append(decl["name"])

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise PublicationArtifactInvalid("missing authority object")
    rats = authority.get("ratifications")
    if not isinstance(rats, dict):
        raise PublicationArtifactInvalid("authority.ratifications must be an object")
    if set(rats) != set(universe_names):
        raise PublicationArtifactInvalid(
            "ratification keys must correspond exactly to the logical universe names "
            f"({sorted(set(rats) ^ set(universe_names))!r} differ)"
        )
    return PublicationArtifactData(format_version=fmt, ref=ManifoldRef(mid, ver),
                                   logical=logical, authority=authority)


def load_publication_artifact(path: str) -> PublicationArtifactData:
    """Read + structurally validate a ``governed-publication.json`` from disk (stdlib JSON only).
    Malformed JSON is a ``PublicationArtifactInvalid`` like any other structural defect."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as exc:
        raise PublicationArtifactInvalid(f"artifact is not valid JSON: {exc}") from exc
    return parse_publication_artifact(raw)


def governed_publication_from_artifact(artifact: PublicationArtifactData) -> GovernedPublication:
    """Build the immutable ``GovernedPublication`` from the artifact — its ``ref``, ``logical``, and
    ``authority`` come EXCLUSIVELY from ``governed-publication.json``, never from ``logical_spec(.cml)``,
    the folder name, ``data.toml``, or Core model metadata. The ``.cml``'s ``SOURCE_MANIFOLD`` is a
    realization claim checked separately, not publication authority."""
    return GovernedPublication(
        ref=artifact.ref,
        logical=artifact.logical,
        authority=PublicationAuthority(
            source_manifold_id=artifact.ref.manifold_id,
            source_manifold_version=artifact.ref.version,
            ratification=artifact.authority.get("ratifications"),
            actor=artifact.authority.get("published_by"),
            at=artifact.authority.get("published_at"),
        ),
    )


def source_ref_of(manifold: Any) -> Optional[ManifoldRef]:
    """The concrete ``ManifoldRef`` a ``.cml`` CLAIMS to realize (its ``SOURCE_MANIFOLD id VERSION``),
    or ``None`` when it carries no source identity (a legacy runtime). A reference/claim of origin —
    NOT established publication authority (that lives in the artifact)."""
    sid = getattr(manifold, "source_manifold_id", None)
    sver = getattr(manifold, "source_manifold_version", None)
    if not sid or not sver:
        return None
    return ManifoldRef(sid, sver)

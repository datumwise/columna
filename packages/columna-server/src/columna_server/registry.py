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

#: The publication-artifact format majors this server understands. Its own dimension — unrelated to
#: the wire CONTRACT_VERSION, columna-core's engine VERSION, or the Manifold's semantic version.
#:
#: A SET, NOT A SCALAR (ruled Huayin, 2026-09-12). The scalar said "the major this server supports",
#: which stopped being true the moment two majors were supportable, and a scalar cannot express the
#: thing that is actually true now: v1 remains a supported input FOR THE LEGACY CORE SERVING PATH and
#: v2 is a supported input FOR THE SUCCESSOR PLATFORM PATH, each read according to its own contract.
#: Keeping the scalar and quietly widening its meaning would have been the misleading compatibility
#: the ruling forbids.
#:
#: NEITHER IS A SHIM FOR THE OTHER. A v1 artifact is never read as v2 and a v2 artifact is never read
#: as v1: no family law is inferred from a v1 artifact, and no v2 artifact is degraded to the v1
#: shape. `_READERS` below is the whole of the per-major dispatch, so adding a major is adding a
#: reader, never a branch inside one.
#:
#: **MAJOR 3 — the native ToD-v7.1 contract (C2, 2026-09-22).** Added as a reader, exactly as the
#: comment above promises. The failure it corrects was measured and is worth stating precisely: a
#: v3 artifact did not REFUSE here, it was *invisible* — `_is_governed_only_unit` swallowed the
#: unsupported-format error and the unit vanished from the catalog, so a deployment holding a
#: lawful native publication was told it had nothing. **The refusal was never the problem; the
#: silence was.** And the refusal itself was load-bearing: relabel that artifact `"2.0"` and the
#: v2 reader ACCEPTS it, discarding every constitution, attestation and denotation it carries. So
#: v3 is admitted by being READ AS v3 — never by relabelling, never by wrapping it in v2's
#: `logical` envelope, and never by widening v2's contract to tolerate it.
SUPPORTED_PUBLICATION_FORMAT_MAJORS = (1, 2, 3)


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
    """One immutable governed publication: a concrete ``ref``, immutable authority/provenance, and
    the major's own reading of what was published. Everything here comes from
    ``governed-publication.json``, never from the ``.cml``.

    **``logical`` AND ``native`` ARE PER-MAJOR, AND EXACTLY ONE IS PRESENT** (C2, 2026-09-22).

    ``logical`` is the v1/v2 physical-clean projection — a declaration list under a ``logical``
    wrapper, named that way because it stood opposite a physical ``.cml``. ``native`` is the v3
    resolved model (``columna_core.governed.native.NativePublication``): a constitution per
    universe, a derived geometry, a denotation table, and per-declaration authority records.

    **The v3 reading is NOT projected into ``logical``.** It could be made to fit — a native
    declaration list would deserialize into that slot without complaint — and that is exactly why
    it is refused: the v2 shape has no place for a constitution, an attestation or a denotation
    table, so filling it would carry the artifact while silently dropping everything that makes it
    native. That is the measured v2 failure, reproduced deliberately instead of accidentally. A
    consumer asks which one it has; it never finds a fabricated one of the other kind."""

    ref: ManifoldRef
    logical: Optional[dict]
    authority: PublicationAuthority
    native: Optional[Any] = None

    @property
    def is_native(self) -> bool:
        """True when this publication is the v3 native model. A consumer that branches on this is
        branching on WHAT IT HOLDS, not on a version string it has to interpret."""
        return self.native is not None


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
    #: The format major this artifact was READ AS. A separate fact from which runtime serves it and
    #: from whether a legacy `.cml` sits beside it — keeping the three apart is what stops a v2
    #: artifact from silently meaning "successor runtime" (ruled 2026-09-12 §3).
    major: int
    ref: ManifoldRef
    #: v1/v2 ONLY. The artifact's physical-clean logical projection, AUTHORING vocabulary.
    logical: Optional[dict] = None
    #: v1/v2 ONLY. {published_by, published_at, ratifications{universe -> record}}. A native
    #: artifact has no such section: its standing lives on the declarations that carry it.
    authority: Optional[dict] = None
    #: v3 ONLY. The native resolved model, read by `columna_core.governed.native` — never a
    #: projection of it into either of the two slots above.
    native: Optional[Any] = None


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
    major = _artifact_major(fmt)
    reader = _READERS.get(major)
    if reader is None:
        raise UnsupportedPublicationFormat(
            f"publication_format_version {fmt!r} has an unsupported major (this server supports "
            f"majors {list(SUPPORTED_PUBLICATION_FORMAT_MAJORS)})"
        )
    ref = data.get("ref")
    if not isinstance(ref, dict):
        raise PublicationArtifactInvalid("missing ref object")
    mid, ver = ref.get("manifold_id"), ref.get("version")
    if not isinstance(mid, str) or not mid or not isinstance(ver, str) or not ver:
        raise PublicationArtifactInvalid("ref must carry a concrete manifold_id and version")

    logical, authority, native = reader(data)   # …then THIS major's own contract, and all of it
    return PublicationArtifactData(format_version=fmt, major=major, ref=ManifoldRef(mid, ver),
                                   logical=logical, authority=authority, native=native)


# ── per-major contracts ──────────────────────────────────────────────────────────────────────────
# **THE SPINE SPLIT** (C2, ruled Huayin 2026-09-22).
#
# Above this line is now the whole of what EVERY major shares, and it is two facts: a supported
# format major, and a concrete `ref`. That is not a reduction for tidiness — it is the correction
# of a category error. The old spine additionally required a `logical` wrapper, an `authority`
# object, and ratification keys corresponding to universe names, and called those "the spine both
# majors share". **They were never a spine; they were v1 and v2's contract, hoisted.** Measured:
# a native v3 artifact has no `logical` wrapper at all, no top-level `authority` section, and no
# publication-global ratification map — its universes carry their own constitutions and their own
# `elf-2` attestations, and its families carry their own constitution authority and U-authority
# binding. Every one of those three "shared" requirements is a v1/v2 fact about where standing was
# FILED, not a requirement of being a governed publication.
#
# So they move down, into `_v1v2_envelope`, and each major's reader owns the whole of its own
# contract. **A shared spine is not a shim only while what it shares is genuinely common**; keeping
# those three above the line would have forced v3 to grow a `logical` wrapper and an `authority`
# map it does not have — translating the new house back into the old one at the very first seam.
#
# Adding a major remains adding a reader, never a branch inside one. Each returns
# `(logical, authority, native)`, and exactly one side of that is populated.

def _v1v2_envelope(data: Any) -> tuple[dict, dict]:
    """The v1/v2 ENVELOPE — `logical.declarations` in the authoring vocabulary, an `authority`
    section, and ratification keys corresponding one-to-one with the logical universe names.

    **This is where publication-global standing lives, and that is a v1/v2 property.** v2 hoists
    declaration-level standing into a top-level map keyed by universe NAME (ratifications) and
    another keyed by `family_id` (family constitutions) — two identity spaces for one job, which
    exists only because `{kind, name, body}` had no room for standing. Nothing is wrong with it as
    v2's own contract, and nothing about it is changed here; it simply stops pretending to be a
    fact about publication artifacts in general."""
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
    return logical, authority


def _read_v1(data: Any) -> tuple[Optional[dict], Optional[dict], Optional[Any]]:
    """v1 — the legacy Core serving path's input, UNCHANGED and deliberately not deepened.

    v1 carries `measure`/`member` declarations and its family law lives in a private realization
    mapping, so there is no family law here for this server to check and none may be inferred. The
    ENVELOPE is the whole of the v1 contract as this server reads it; that is exactly what it was
    before v2 support existed, and nothing about v1 ingest changed when v2 arrived.

    The envelope moved out of the shared spine and into this function at C2, UNCHANGED: the same
    checks run in the same order over the same bytes, so v1 reads exactly as it read before. What
    changed is only that it is now stated as v1 and v2's contract rather than as every major's."""
    return (*_v1v2_envelope(data), None)


def _read_v2(data: Any) -> tuple[Optional[dict], Optional[dict], Optional[Any]]:
    """v2 — read through V2'S OWN READER, not through a second implementation of it.

    `columna_core.governed.publication.parse_publication` IS the v2 contract: family identity,
    canonical-reference uniqueness (§2.2 — two families under one reference refuse), law citations,
    constitution authority. Re-implementing any of that here would be a second enumeration of a
    contract this server does not own, free to drift from the reader every other consumer uses.

    Imported inside the function, not at module scope: artifact READING is stdlib-JSON work and the
    registry's independence from any heavier surface is worth keeping visible. The disjointness that
    matters — the server never imports `manifold_agent` — is unaffected and still test-enforced.

    Structural failures are re-raised as `PublicationArtifactInvalid` so every ingest defect reaches
    the store through the one exception family it already classifies."""
    from columna_core.governed.publication import PublicationFormatRefusal
    from columna_core.governed.publication import parse_publication as _v2

    logical, authority = _v1v2_envelope(data)
    try:
        _v2(data)
    except PublicationFormatRefusal as exc:
        raise PublicationArtifactInvalid(f"v2 contract: {exc}") from exc
    return logical, authority, None


def _read_v3(data: Any) -> tuple[Optional[dict], Optional[dict], Optional[Any]]:
    """v3 — the NATIVE ToD-v7.1 contract, read through ITS OWN reader.

    `columna_core.governed.native.parse_native_publication` IS the v3 contract, the way
    `parse_publication` is v2's: the version gate's two mechanisms, consume-or-refuse at the
    declaration envelope, the constitution as governed facts, and the four currency claims
    recomputed from the carried bytes. Re-implementing any of it here would be a second
    enumeration of a contract this server does not own.

    **THIS FUNCTION IS THE WHOLE OF WHAT C2 ADDS TO INGEST, AND IT TRANSLATES NOTHING.** It calls
    no v1/v2 helper, builds no `logical` wrapper, synthesizes no `authority` section and no
    ratification map, and produces no declaration in the authoring vocabulary. What it returns is
    the native model itself. Every legacy object that a v2 reading would have required — an anchor
    declaration, a publication-global anchor map, `universe.body.anchor`, a basis, a global
    coordinate namespace — is not "not yet supported" here; there is no expression in this path
    that could produce one.

    Imported inside the function, for the reason `_read_v2`'s import is: artifact READING is
    stdlib-JSON work at this layer, and the registry's independence from heavier surfaces is worth
    keeping visible. The disjointness that matters — the server never imports `manifold_agent` —
    is unaffected and still test-enforced."""
    from columna_core.governed.native import NativePublicationRefusal
    from columna_core.governed.native import parse_native_publication as _v3

    try:
        return None, None, _v3(data)
    except NativePublicationRefusal as exc:
        raise PublicationArtifactInvalid(f"v3 contract: {exc}") from exc


#: major → the reader for that major's own contract. The whole of the per-major dispatch.
_READERS = {1: _read_v1, 2: _read_v2, 3: _read_v3}


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
    """Build the immutable ``GovernedPublication`` from the artifact — everything it carries comes
    EXCLUSIVELY from ``governed-publication.json``, never from ``logical_spec(.cml)``, the folder
    name, ``data.toml``, or Core model metadata. The ``.cml``'s ``SOURCE_MANIFOLD`` is a realization
    claim checked separately, not publication authority.

    **PER-MAJOR, AND NOTHING IS CROSS-FILLED** (C2). A v3 publication carries ``native`` and leaves
    ``logical`` ``None``; a v1/v2 publication is exactly as it was.

    ``PublicationAuthority.ratification`` IS ``None`` FOR v3, AND IT DOES NOT MEAN "NOT RATIFIED".
    That field holds v2's publication-global ratification MAP, keyed by universe name. Natively
    there is no such map: each universe carries its own ``elf-2`` attestation on its own
    declaration, **and that attestation was recomputed from the carried constitution and verified
    before this function was reached** — so the native standing is strictly stronger than the slot
    it is absent from. The slot stays empty because the v2 OBJECT does not exist, never because
    nothing was ratified, and it is not back-filled with a fabricated map: the records are reachable
    where they actually live, on ``native``. ``actor``/``at`` come from ``published``, which is
    provenance of the publication ACT — not a claim that this publication is the authoritative one,
    which the surrounding governance process settles outside the bytes."""
    if artifact.native is not None:
        return GovernedPublication(
            ref=artifact.ref,
            logical=None,
            authority=PublicationAuthority(
                source_manifold_id=artifact.ref.manifold_id,
                source_manifold_version=artifact.ref.version,
                ratification=None,
                actor=artifact.native.published_by,
                at=artifact.native.published_at,
            ),
            native=artifact.native,
        )
    authority = artifact.authority or {}
    return GovernedPublication(
        ref=artifact.ref,
        logical=artifact.logical,
        authority=PublicationAuthority(
            source_manifold_id=artifact.ref.manifold_id,
            source_manifold_version=artifact.ref.version,
            ratification=authority.get("ratifications"),
            actor=authority.get("published_by"),
            at=authority.get("published_at"),
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

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

from dataclasses import dataclass
from typing import Any, Optional, Protocol, runtime_checkable

from columna_core import logical_spec


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
    (``logical_spec`` — no table/column/reject/realization), and immutable authority/provenance."""

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


def governed_publication_from_manifold(manifold: Any) -> Optional[GovernedPublication]:
    """Build a ``GovernedPublication`` from a parsed ``columna_core`` Manifold IFF it carries a
    complete source identity (P0(b)). Returns ``None`` for a source-identity-less (legacy) manifold —
    never fabricating an id/version. The logical projection is ``logical_spec`` (physical-clean)."""
    sid = getattr(manifold, "source_manifold_id", None)
    sver = getattr(manifold, "source_manifold_version", None)
    if not sid or not sver:
        return None
    ref = ManifoldRef(sid, sver)
    return GovernedPublication(
        ref=ref,
        logical=logical_spec(manifold),
        authority=PublicationAuthority(source_manifold_id=sid, source_manifold_version=sver),
    )

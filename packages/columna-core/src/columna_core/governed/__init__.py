"""
columna_core.governed — the governed layer: publication format v2, the foundation-law vocabulary,
and the resolver that turns a family's declarations into a TOTAL canonical `Law(F)` view.

Three objects and one rule.

  `foundation`   shared, versioned, backend-independent semantic vocabulary. Cited by families,
                 never a family identity. Re-derived from the theory rather than promoted from the
                 operator registry, because holding the content is not standing to be its authority.
  `publication`  the v2 artifact: ONE family kind covering primitive and constructed formation, and
                 named and query-constructed alike. `measure`, `member` and `boundary` are retired.
  `native`       **format v3, the NATIVE ToD-v7.1 artifact.** Not an evolution of `publication`:
                 it has no `logical` wrapper, no universe `body`, no `anchor` kind and no
                 publication-global anchor map, because none of those objects exists natively. A
                 universe carries its CONSTITUTION and the geometry is COMPUTED from it. Neither
                 major is a shim for the other.
  `resolve`      the total view: every ToD v7.1 §4 responsibility carries `established` /
                 `explicit-none` / `unestablished`, with the provenance that settled it.

  THE RULE      declaration is for analytical choices; derivation is for consequences.
"""
from __future__ import annotations

from .foundation import (
    LawCitation,
    FoundationLaw,
    UnknownFoundationLaw,
    VOCABULARY as FOUNDATION_VOCABULARY,
    VERSION as FOUNDATION_VERSION,
    cite,
    resolve as resolve_law,
)
from .publication import (
    PUBLICATION_FORMAT_VERSION,
    ExplicitNone,
    Family,
    Formation,
    GovernedPublicationV2,
    PublicationFormatRefusal,
    load_publication,
    parse_family_declaration,
    parse_publication,
)
from .native import (
    NATIVE_PUBLICATION_FORMAT_VERSION,
    SUPPORTED_NATIVE_VERSIONS,
    Anchor,
    Constitution,
    Family as NativeFamily,
    NativePublication,
    NativePublicationRefusal,
    Resolution,
    Universe,
    load_native_publication,
    parse_native_publication,
)
from .resolve import (
    ESTABLISHED,
    EXPLICIT_NONE,
    IDENTITY_BEARING,
    RESPONSIBILITIES,
    UNESTABLISHED,
    LawResolutionRefusal,
    LawView,
    render,
    resolve_all,
    resolve_family,
)

__all__ = [
    "FOUNDATION_VOCABULARY", "FOUNDATION_VERSION", "FoundationLaw", "LawCitation",
    "UnknownFoundationLaw", "cite", "resolve_law",
    "PUBLICATION_FORMAT_VERSION", "GovernedPublicationV2", "Family", "Formation", "ExplicitNone",
    "PublicationFormatRefusal", "parse_publication", "load_publication",
    "parse_family_declaration",
    "NATIVE_PUBLICATION_FORMAT_VERSION", "SUPPORTED_NATIVE_VERSIONS", "NativePublication",
    "NativePublicationRefusal", "NativeFamily", "Universe", "Constitution", "Anchor",
    "Resolution", "parse_native_publication", "load_native_publication",
    "RESPONSIBILITIES", "IDENTITY_BEARING", "ESTABLISHED", "EXPLICIT_NONE", "UNESTABLISHED",
    "LawView", "LawResolutionRefusal", "resolve_family", "resolve_all", "render",
]

"""ASSERTION RESPONSIBILITY AND ASSERTION REVISION — what a realization claims, and which revision.

THE TWO LEVELS (ruled Huayin, 2026-09-14, repairing OF-57).

    RESPONSIBILITY   which realization responsibility OWNS the claim
                     family:            publication_ref + kind + family_id
                     anchor component:  publication_ref + kind + anchor_ref + component_name
                     Changing the endpoint, grain, operators or exactness does NOT change it.

    REVISION         the COMPLETE content that responsibility asserts, at a particular revision.
                     Any change to a content-bearing fact produces a different revision.

WHY THIS MODULE EXISTS. `Standing.realization` is a compatibility axis: a change to it blocks
combination. It was built by hand-concatenating five strings out of the claim's SIX content-bearing
facts, dropping `formation_operator` and `continuation_operator` — so two realizations that disagree
about what the fold MEANS (sum versus min) produced a byte-identical standing and combined. OF-57
has the measurement. The repair is not "append the two missing fields": that is correct today and
reproduces the defect the next time a field is added, which is how this one arrived. **Completeness
is derived here, from the parsed claim's own dataclass fields, so it cannot drift by omission.**

WHAT THIS IS NOT, STATED BEFORE THE CODE BECAUSE IT IS THE PART MOST EASILY OVER-READ.

  · NOT AUTHORSHIP. An assertion revision says WHAT was claimed. It says nothing about WHO claimed
    it or on what authority. Realization attestation is a separate open jurisdiction and must not be
    acquired here by accident. Nothing author-bearing may enter this computation, ever.
  · NOT CURRENCY. Two observations agreeing on the assertion revision have established that THE
    CLAIM DID NOT CHANGE. They have established nothing about whether the claim is still TRUE of the
    source. Realization currency is a separate open jurisdiction.
  · NOT CRYPTOGRAPHIC AUTHENTICITY. The digest is a deterministic identity over content the process
    already holds. It resists ACCIDENT — a field silently dropped, two revisions compared as one. It
    does not resist a forger: anyone who can write the mapping can write a mapping that fingerprints
    however they like. That is the same threat model the lowering receipt records for itself, and it
    is stated here so the guarantee is not over-read.
  · NOT THE MAPPING REVISION. A mapping is a document carrying many realizations; naming ITS
    revision is a different object at a different granularity and is rowed separately (P2-10).
    Folding it in here would make one mapping-wide fact gate every family's compatibility.
  · NOT A PUBLIC TYPE. Like `Standing`, this is Platform's working representation. No class or type
    name here is frozen, and nothing downstream may treat the shape as a contract.

SCHEME NAMESPACING, AND WHY. The digest is prefixed `ar-1`. Two fingerprints under different schemes
are INCOMPARABLE, and incomparable must read as CHANGED, never as equal — the polarity
`constitution_status`, `Connector.data_identity` and the projection-scoped change detector already
share. If the composition below ever changes, the scheme moves with it, and every prior fingerprint
becomes incomparable rather than quietly wrong.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from typing import Any, Optional

#: The assertion-revision scheme. BUMP THIS whenever the canonical composition below changes — a
#: fingerprint computed under another scheme is incomparable, not unequal-by-accident.
ASSERTION_SCHEME = "ar-1"

#: Realization fields that are ENCODING METADATA rather than asserted content. `mapping_format_version`
#: lives on the document, not on a realization, and is listed here for the completeness check's sake.
_NOT_CONTENT = frozenset({"mapping_format_version"})

#: The subject fields per realization kind — the part that identifies the RESPONSIBILITY rather than
#: the revision. Everything else on the claim is revision content.
_SUBJECT = {
    "family": ("family_id",),
    "anchor_component": ("anchor_ref", "component_name"),
}


def _kind(realization: Any) -> str:
    """The realization kind, from the parsed type rather than from a re-read of the document."""
    name = type(realization).__name__
    if name == "FamilyRealization":
        return "family"
    if name == "AnchorComponentRealization":
        return "anchor_component"
    raise TypeError(f"unknown realization type {name!r}; this profile fingerprints two kinds")


def _canonical(value: Any) -> Any:
    """A JSON-encodable canonical form.

    NULL IS PRESERVED AS NULL, and that is load-bearing rather than incidental: a null `schema` is a
    POSITIVE ruled claim — *"no schema qualification applies"* — and not an absent field. JSON
    distinguishes `null` from the string `"null"`, so a schema literally named `null` and an absent
    schema qualification do not collide."""
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if dataclasses.is_dataclass(value):
        return {f.name: _canonical(getattr(value, f.name))
                for f in sorted(dataclasses.fields(value), key=lambda f: f.name)}
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    if isinstance(value, dict):
        return {k: _canonical(value[k]) for k in sorted(value)}
    raise TypeError(f"{type(value).__name__} has no canonical form here; add one deliberately "
                    f"rather than letting str() decide what a claim means")


def _digest(payload: dict) -> str:
    """Canonical JSON -> blake2b-16. `sort_keys` and fixed separators make the encoding canonical,
    so a producer's key order or whitespace cannot change the identity of what was asserted."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.blake2b(encoded, digest_size=16).hexdigest()


def responsibility(publication_ref: Any, realization: Any) -> str:
    """WHICH realization responsibility owns this claim. Stable across every content change.

    Readable on purpose — it is an address, not a digest, and an operator reading a refusal should
    be able to see whose claim is at issue without a lookup table."""
    kind = _kind(realization)
    subject = ".".join(str(getattr(realization, f)) for f in _SUBJECT[kind])
    return f"{publication_ref.manifold_id}@{publication_ref.version}/{kind}/{subject}"


def revision(publication_ref: Any, realization: Any, *, extra: Optional[dict] = None) -> str:
    """The assertion REVISION identity — complete over every content-bearing fact of the claim.

    COMPLETENESS IS DERIVED, NOT LISTED. Every dataclass field of the parsed realization enters the
    payload except those named as encoding metadata. A field added to the claim therefore enters
    this identity automatically, and the alternative — a hand-maintained list — is the mechanism
    that produced OF-57.

    `extra` carries facts that are part of what was asserted but do not live on the realization
    object itself. The constructed path uses it for the continuation law and operand actually
    applied, which the previous string also carried; it is a named parameter rather than an
    implicit append so that what is included is visible at the call site.

    The responsibility is folded into the payload: a revision identity that did not say WHOSE
    revision it is would compare two different responsibilities' content as one."""
    kind = _kind(realization)
    content = {f.name: _canonical(getattr(realization, f.name))
               for f in dataclasses.fields(realization)
               if f.name not in _NOT_CONTENT}
    payload = {
        "scheme": ASSERTION_SCHEME,
        "responsibility": responsibility(publication_ref, realization),
        "kind": kind,
        "content": content,
    }
    if extra:
        payload["applied"] = _canonical(extra)
    return f"{ASSERTION_SCHEME}:{_digest(payload)}"


def content_fields(realization: Any) -> tuple:
    """The content-bearing field names this profile fingerprints, for controls and disclosure."""
    return tuple(sorted(f.name for f in dataclasses.fields(realization)
                        if f.name not in _NOT_CONTENT))

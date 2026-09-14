"""One positive movement licence, as a RUNTIME PROJECTION — not a governed serialization.

WHAT THIS IS, AND WHAT IT IS DELIBERATELY NOT (ruled Huayin, 2026-09-12). The governed v2 artifact
carries `movement` as an opaque slot with no shape, and Proof B does NOT give it one. The permanent
serialization question stays open. What crosses into execution here is a PROJECTION derived by the
layer that owns the law and handed to the SSE as EXECUTION INPUT — the same standing the C7
sufficient-state basis has in Proof A: derived, not constitutive, and not realization.

THE PUBLIC NAME AND SHAPE OF THIS OBJECT ARE NOT FROZEN. `MovementLicence` is Proof B's working
representation. Nothing downstream may treat its field list as a contract, for the same reason the
SSE contract declines to name the retained-state standing object: naming it would also fix its arity,
and the arity is what is still being learned.

THE ONLY ADMITTED MOVEMENT NOTION IN THIS PROOF:

    projection from a declared anchor onto a SUBSET of its declared components.

No hierarchy, no lineage, no calendar, no functional edge, no provider table, no blocked-lineage
scope, no legacy planner movement. `sale_at = store x day` -> `store` is the whole of it.

WHAT THE COMPONENT-SUBSET RELATION IS, AND WHAT IT IS NOT (ruled Huayin, 2026-09-12). Recorded here
because the check below is the kind that quietly grows into a doctrine if nobody writes down its
edge:

    The component-subset relation is a STRUCTURAL ADMISSIBILITY CHECK for this proof. It does not
    create or imply a movement licence. Positive movement authority comes ONLY from the explicit
    licence.

    Proof B does not establish that every subset of a compound anchor is automatically a governed
    target. Its claim is narrower: GIVEN an explicitly licensed source->target continuation,
    component-subset projection is sufficient MECHANICAL STRUCTURE to realize this exact coarsening
    without hierarchy or lineage machinery.

So the subset check answers "could this coarsening be realized at all?" and the licence answers "may
this family be moved?" — and the first never answers the second. `sale_at(store x day) -> store` is
structurally projectable whether or not anyone licensed it; that is exactly why the unlicensed case
still refuses. NO FORMAT OR GENERAL MOVEMENT DOCTRINE FOLLOWS FROM THIS PROOF.

THE SUBSET IS CHECKED, NOT TRUSTED. A licence naming a target anchor is a string; a licence whose
target components are verified against the publication's DECLARED anchor components is a fact. The
string is never the evidence — `_declared_components` reads the anchor declaration and the projection
is refused unless the target is a proper subset of what that declaration actually says.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .anchors import declared_coordinate_names
from .refusals import WantOfLaw

#: THE SCOPE OF THIS PROOF, verbatim (ruled Huayin, 2026-09-12). A constant for the reason
#: `EMPTY_FIBER_RULING` and `RESPONSIBILITY_STANDING_RULE` are constants: it is the sentence that
#: stops a reader inferring a general movement doctrine from a passing structural check.
PROOF_B_SCOPE = (
    "The component-subset relation is a structural admissibility check for this proof. It does not "
    "create or imply a movement licence. Positive movement authority comes only from the explicit "
    "licence. Given an explicitly licensed source->target continuation, component-subset projection "
    "is sufficient mechanical structure to realize this exact coarsening without hierarchy or "
    "lineage machinery."
)

#: The only standing this proof accepts. Stated as a token rather than a bool so that "licensed" is
#: never the absence of a negative — a licence must POSITIVELY say so.
POSITIVE = "positive"


@dataclass(frozen=True)
class MovementLicence:
    """Enough to establish source, target, law, and positive standing — and nothing more."""

    source_anchor: str
    #: the source anchor's DECLARED components, as read from the publication (never from the caller)
    source_components: tuple
    target_anchor: str
    #: a proper subset of `source_components`, verified at construction
    target_components: tuple
    #: the continuation law this movement is licensed under
    law: str
    #: POSITIVE, or this is not a licence
    standing: str
    #: who licensed it. Carried so a served result can say what it stood on.
    authority: str = "hand-authored (Proof B)"

    @property
    def is_positive(self) -> bool:
        return self.standing == POSITIVE

    def describe(self) -> str:
        return (f"{self.source_anchor}({'*'.join(self.source_components)})"
                f" -> {self.target_anchor}({'*'.join(self.target_components)})"
                f" under {self.law} [{self.standing}]")


#: THE MOVEMENT VIEW: ordered governed coordinate NAMES. A movement asks whether a target names real
#: coordinates and is a proper part of the anchor; it never asks what a coordinate IS. Order is
#: load-bearing here and nowhere else — it reaches `MovementLicence.source_components` and is
#: rendered in the licence's description, which is evidence a human reads.
#:
#: DERIVED, NOT RE-PARSED (2026-09-14). This used to be its own parser of the anchor declaration's
#: with its own malformation policy — the strictest of the three that existed, and reachable only
#: through this door. The canonical reader in `anchors` now carries that policy for every consumer.
_declared_components = declared_coordinate_names


def project(publication, *, source_anchor: str, target_anchor: str, target_components,
            law: str, authority: str = "hand-authored (Proof B)") -> MovementLicence:
    """Derive one positive licence, validating the projection against the DECLARED components.

    Refuses — rather than returning an unusable licence — because a licence that does not licence
    anything is not a value any caller should have to check for."""
    declared = _declared_components(publication, source_anchor)
    target = tuple(target_components)

    unknown = [c for c in target if c not in declared]
    if unknown:
        raise WantOfLaw(
            f"target components {unknown} are not declared components of {source_anchor!r} "
            f"(declared: {list(declared)}); a movement may not invent a coordinate",
            subject=source_anchor)
    if not target:
        raise WantOfLaw(
            "a target with NO components is a projection onto the grand total, which is outside "
            "this proof's admitted movement notion", subject=source_anchor)
    if set(target) == set(declared):
        raise WantOfLaw(
            f"target components {list(target)} are the whole of {source_anchor!r}; that is not a "
            f"movement, and licensing it would make every family trivially 'movable'",
            subject=source_anchor)

    return MovementLicence(
        source_anchor=source_anchor, source_components=declared,
        target_anchor=target_anchor, target_components=target,
        law=law, standing=POSITIVE, authority=authority)


def licence_for(licence: Optional[MovementLicence], *, source: str, target: str,
                continuation_law: str) -> Optional[str]:
    """`None` if this licence authorizes THIS movement; otherwise why it does not.

    Returning the REASON rather than a bool is the point: all three refusals below are `want_of_law`,
    and an operator who is told only "unlicensed" cannot tell a missing licence from a licence for
    somewhere else from a licence under the wrong law. Those have three different remedies."""
    if licence is None:
        return ("no positive movement licence was carried into execution. Mechanical combinability "
                "is NOT analytical permission: the operator's monoid property says these values CAN "
                "be folded, never that this family MAY be moved")
    if not licence.is_positive:
        return f"the carried licence has standing {licence.standing!r}, which is not {POSITIVE!r}"
    if licence.source_anchor != source:
        return (f"the carried licence moves from {licence.source_anchor!r}, not from {source!r}; "
                f"a movement licence is specific and is not implicitly transitive")
    if licence.target_anchor != target:
        return (f"the carried licence targets {licence.target_anchor!r}, not {target!r}; "
                f"a movement licence is specific, not general")
    if licence.law != continuation_law:
        return (f"the carried licence is under {licence.law!r} while the family's established "
                f"continuation is {continuation_law!r}; a licence under one law does not license "
                f"continuation under another")
    return None

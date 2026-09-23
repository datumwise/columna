"""columna_platform.native_law — **is this resolved identity lawfully answerable?**

C4 of the native-consumer sequence. C3 ended with `F @ A` resolved from a native publication with
no family-law resolution at all. This is the next question, and it is a different one:

    C3 · WHICH analytical point is being asked for      -> answered by U's constitution + geometry
    C4 · MAY that point be answered, and from what      -> answered by Law(F)

**AND THE ANSWER IS THAT LAW(F) IS FINALLY REQUIRED.** Not as an implementation dependency inherited
from the legacy engine — the rule below never mentions an anchor, a declaration, a level or a basis
— but because the question itself is a question about the family's own governed law.

THE RULE, IN TWO CLAUSES AND IN THIS ORDER
------------------------------------------
  1. **C7 · sufficient-state bases** must be ESTABLISHED. Without a governed basis there is nothing
     from which a value of `F` can be determined, at any anchor.
  2. **C3 · domain and movement** must POSITIVELY license the ask, and only when the ask is off the
     family's constitutive anchor. At the constitutive anchor the question does not arise:
     *constitutive* is what it means for the family to be established there.

**WHY C7 IS ASKED FIRST.** Both refusals can be true at once, and the ruled diagnosis order is to
surface the one whose remedy is upstream. A family with no governed basis is unanswerable at EVERY
anchor, so reporting the movement gap first would send a steward to license a movement that still
could not be answered. (The v2 serving path asks them in the same order. That agreement is reported
as a measurement, not adopted as a template.)

**WHY `C3.standing == ESTABLISHED` WAS NOT THE TEST, AND WHY IT NOW IS.** C3 *was* "domain AND
movement", resolved into one standing that became ESTABLISHED when EITHER was declared — so a family
declaring a domain and no movement resolved ESTABLISHED carrying no licence, and testing the standing
would have served a coarser anchor for it. This module inspected the content instead.

**The conflation is retired (ruled Huayin, 2026-09-22): C3 is now two responsibilities.** This rule
reads `C3_EDGE_VALIDITY`, whose standing means exactly what this module needs it to mean, and the
content inspection is gone with the defect that forced it. The family-domain half is not read here at
all — it is a relation to a resolved location and is adjudicated in `native_domain`, one layer up.

WHAT THIS MODULE IS CAREFUL NOT TO DO (ruled Huayin, 2026-09-22)
----------------------------------------------------------------
**It does not create a native movement contract.** C3 made the absence reachable; that is not a
licence to invent a representation for it. Where a movement is asked for and C3 establishes nothing,
this module REFUSES and says exactly what is missing and whose it is to decide. No `MovementLicence`
is constructed, no `movement` content shape is assumed, no default is supplied, and nothing is
inferred from the geometry that showed the target is reachable.

**It does not port the v2 licence mechanism.** `MovementLicence` identifies a movement by a pair of
anchor NAMES and verifies its structural half against an anchor DECLARATION — two objects with no
native referent. Its own module says what it is: *"a RUNTIME PROJECTION — not a governed
serialization… the governed v2 artifact carries `movement` as an opaque slot with no shape, and
Proof B does NOT give it one."* So it is not a candidate native representation, and C4 does not
treat it as one.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from columna_core.governed.native import Family, NativePublication
from columna_core.governed.publication import parse_family_declaration
from columna_core.governed.resolve import (
    C3_EDGE_VALIDITY,
    C7_SUFFICIENT_STATE,
    ESTABLISHED,
    EXPLICIT_NONE,
    LawView,
    resolve_family,
)

from .refusals import WantOfLaw


class _ParentLookup:
    """**The only thing `resolve_family` asks of a publication: a parent family by `family_id`.**

    Worth a class rather than a lambda because the narrowness is the finding. Law resolution needs
    no publication-shaped object, no declaration list, no anchor map and no universe — it needs to
    follow `formation.operands` to the families they name, which is `§3.7`'s lineage edge and
    nothing else. A constructed family cites its parents by identity, so the lookup is by identity.
    """

    def __init__(self, families: dict):
        self._families = families

    def family(self, family_id: str) -> Optional[Any]:
        return self._families.get(family_id)


def law_of(pub: NativePublication, family: Family) -> LawView:
    """`Law(F)` for a native family — **the total nine-responsibility view, from its own clauses.**

    ⟨measured, C4⟩ this resolves TOTALLY over the shipped native fixture, with every responsibility
    settled and `VALID: yes`, and it consults **no anchor declaration, no `universe.body`, no basis,
    no level, no denotation table and no geometry.** That is not a result about this module; it is a
    result about `Law(F)`: **the nine responsibilities are a family's statement about itself**, and
    the family's declared clauses are carried identically by both majors.

    So no anchor model is translated here, in either direction. What is reused is the rule; what is
    supplied to it is the native family's own body, parsed by the one reader of the family-clause
    contract (`parse_family_declaration`).

    **One discrepancy, recorded rather than smoothed.** `C2 · identity_and_ancestry` carries
    `universe` and `constitutive_anchor` in its VALUE — two nominal references that native identity
    has deliberately left behind (`fcf-2` removed both from the payload: the world is governed
    through the U-authority binding, and the anchor is resolved to its constituent set). Nothing
    consumes them, so nothing is wrong today; but a consumer that began to read `C2.value` for
    meaning would be reading a spelling on the native path.
    """
    declared = {f.family_id: parse_family_declaration(f.name, dict(f.body)) for f in pub.families}
    return resolve_family(declared[family.family_id], _ParentLookup(declared))


def laws_of(pub: NativePublication) -> dict:
    """Every native family's total view, keyed by `family_id`."""
    declared = {f.family_id: parse_family_declaration(f.name, dict(f.body)) for f in pub.families}
    lookup = _ParentLookup(declared)
    return {fid: resolve_family(fam, lookup) for fid, fam in declared.items()}


@dataclass(frozen=True)
class MissingGovernedFact:
    """A fact the artifact does not carry, CHARACTERIZED rather than represented.

    Instantiated where C4 stops. It names what is missing, whose decision it is and where it would
    belong — and deliberately carries no candidate encoding, because *"if C4 discovers that a
    governed fact is genuinely missing, stop with the missing fact characterized rather than
    inventing its representation"* (Huayin, 2026-09-22)."""

    fact: str
    whose: str
    where: str


#: The one fact C4 reached and could not obtain. The `movement` SLOT exists in the family body's
#: total key set in both majors; what has never been decided is what goes in it. v2's reader accepts
#: arbitrary content for it (`_slot(..., lambda r: r)`), and the only thing in this tree that builds
#: a movement is a runtime projection its own module declines to call a serialization.
#: **NARROWED, 2026-09-22.** C4 recorded one undecided fact covering both halves of C3. The
#: family-domain half is now decided for primitive Case-S families and implemented in
#: `native_domain`; what remains undecided is the EDGE half, and this constant is narrowed to it
#: rather than retired, because `Γ_F`'s conditions are still held.
MOVEMENT_STANDING_UNDECIDED = MissingGovernedFact(
    fact=("what a native EDGE CONTRACT Γ_F(B→A) states — the conditions under which a particular "
          "movement between ADMITTED locations is lawful. Family-domain membership is now decided "
          "for a primitive family and does not answer this: being admitted to stand at A does not "
          "make every proposed derivation to A lawful. Coverage permission γ, participation and "
          "support, evidence, and commutation are independent premises with no home yet"),
    whose=("the steward who constitutes F. §1.5 files coverage at edge-or-evidence validity, not "
           "at family identity, so this is not the family-domain declaration under another name"),
    where=("the family declaration's movement slot, which both majors carry as a total key and "
           "neither has given a content contract"),
)


def assert_answerable(view: LawView, *, moving: bool) -> None:
    """**The decision, and the whole of it.** Raises `WantOfLaw`, or returns.

    **NOTE THE SIGNATURE: THERE IS NO ANCHOR IN IT.** `moving` is a boolean — *is the ask off the
    family's constitutive anchor* — and the caller answers it from its own anchor model. So this
    rule runs unchanged over a native `LawView` and a legacy one, translating neither, which is the
    C4 question about convergence asked in the only form that can be answered: by writing the rule
    so that an anchor model cannot enter it, and then seeing whether it still says everything it
    needs to. It does.
    """
    c7 = view[C7_SUFFICIENT_STATE]
    if c7.standing != ESTABLISHED:
        raise WantOfLaw(
            f"{view.canonical_reference!r} has no established sufficient-state basis "
            f"({c7.standing}): {c7.note or 'no governing law establishes one'}. There is nothing "
            f"from which a value of this family can be determined — at this location or at any "
            f"other — so this is a defect of the family's own law and not of the ask",
            subject=view.canonical_reference)
    if not moving:
        return

    c3 = view[C3_EDGE_VALIDITY]
    licensed = None if c3.standing == EXPLICIT_NONE else c3.value
    if licensed is None:
        raise WantOfLaw(
            f"{view.canonical_reference!r} establishes no positive movement: C3 is {c3.standing}"
            + (" — the family has DECLARED that nothing moves" if c3.standing == EXPLICIT_NONE
               else (f" ({c3.note})" if c3.note else ""))
            + f". {MOVEMENT_STANDING_UNDECIDED.fact.split('.')[0]}. This path will not infer a "
              f"licence from the geometry that showed the location is reachable, and it will not "
              f"supply one: what belongs in that slot is not yet decided, and inventing it here "
              f"would make an execution profile the author of a governed contract",
            subject=view.canonical_reference)

    # A POSITIVE movement fact exists and this path cannot yet read it.
    #
    # STOP, AND SAY SO — do not guess at its shape. The v2 slot is opaque by construction and the
    # only movement object in this tree is a runtime projection identified by two anchor NAMES,
    # which have no native referent. A native reading of this content is exactly the undecided
    # contract above; reaching it is where C4 ends.
    raise WantOfLaw(
        f"{view.canonical_reference!r} carries positive C3 movement content, and this path has no "
        f"governed reading of it. The content is preserved, not rejected: what a native movement "
        f"declaration MEANS — how it identifies a target location without an anchor name, and what "
        f"authority it carries — is undecided, and a profile that guessed would be authoring the "
        f"contract rather than consuming it",
        subject=view.canonical_reference)

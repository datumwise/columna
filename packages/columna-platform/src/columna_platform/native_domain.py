"""columna_platform.native_domain — **may this family stand at this resolved location?**

C5 of the native-consumer sequence, and the narrowest question yet asked. C3 resolved WHICH
analytical point is being asked for; C4 asked whether the family's law makes it answerable AT ALL,
without ever naming an anchor. This asks the one question that lies between them and that neither
could answer:

    C3 · WHICH analytical point                  -> U's constitution + geometry
    C5 · MAY `F` STAND AT IT                     -> Law(F)'s family-domain condition + that geometry
    C4 · may the resolved identity be answered   -> Law(F), anchor-model-free

**WHY THIS IS NOT IN `native_law.assert_answerable`** (ruled Huayin, 2026-09-22). C4 proved
something real and this module preserves it: resolving `Law(F)` consults no anchor model, and the
law-level sufficiency rule runs unchanged over a native and a legacy view. What C4 *also* claimed —
that the COMPLETE answerability decision could stay anchor-free — is now known to be false, and the
distinction is not a technicality:

* **resolving the family law is anchor-free** — it is the family's statement about itself;
* **applying its family-domain condition to a requested `A` necessarily consumes resolved geometry**,
  because domain membership is a RELATION between `F` and a location.

So the predicate lives here, at the narrowest layer where both the law and the resolved geometry are
legitimately in hand, and `assert_answerable` keeps its anchor-free signature rather than being bent
to carry a constituent set it has no business seeing.

WHAT THIS MODULE DOES NOT DO
----------------------------
**It does not decide lawful query admission.** Passing the family-domain condition establishes that
`F` is admitted to stand at `A`. It establishes nothing else. Edge validity `Γ_F(B→A)`, coverage
`γ`, participation and support, evidence, commutation, and Case-G conditions are independently
governed premises and remain separate — *"this unit establishes the primitive Case-S family-domain
predicate, not a universal biconditional for complete query validity."*

**It does not serve constructed families.** The scope gate is `formation.kind == PRIMITIVE`. Where a
construction reaches this question, the module STOPS with the missing governed fact characterized
and supplies no derivation, no propagation, no union, and no default.

**It does not mint a wire reason code.** All refusals here are `WantOfLaw`. The closed reason
registry has no member whose governed subject is the requested OUTPUT location's admission, and
minting one is a separate ruling — so the distinction is carried in the refusal's subject and
detail, and the boundary is reported rather than crossed.
"""
from __future__ import annotations

from typing import Optional

from columna_core.governed.native import Anchor, Family
from columna_core.governed.resolve import (
    C3_FAMILY_DOMAIN,
    ESTABLISHED,
    EXPLICIT_NONE,
    LawView,
    UNESTABLISHED,
)

from .native_law import MissingGovernedFact
from .refusals import WantOfLaw

#: The fact this unit reaches and does not fill. R8: *"For a constructed family, if answering the
#: domain question would require establishing how its own `P_F` follows from its formation or
#: operands, stop with the missing governed fact characterized. Do not fill it."*
CONSTRUCTED_DOMAIN_UNDECIDED = MissingGovernedFact(
    fact=("what establishes a CONSTRUCTED family's prohibited Case-S constituents. Its own "
          "declaration may state them; whether — and how — they instead follow from its formation "
          "law and its operands is undecided. The Measure Algebra's capability-indexed union is "
          "NOT the answer: it governs a different object, indexed by capability rather than by "
          "family, and importing it while discarding the capability index would under-prohibit"),
    whose=("the steward, as a governed question about constructed-family law — not an "
           "implementation detail, and not inferable from the fact that `formation.operands` makes "
           "a recursion technically possible"),
    where=("the constructed family's own declaration, or a governed propagation rule that does not "
           "yet exist"),
)


def forgotten(root: Anchor, target: Anchor) -> frozenset:
    """`Forgotten(A_0 → A)` — the Case-S constituents present in `A_0` and absent from `A`.

    Set difference, computed by the geometry, never declared and never stored. Named `Forgotten`
    rather than `Spent` deliberately (R7): `Spent(q)` is a primitive of the inherited contract
    calculus, is undefined even there, and is not adopted as a native term — which also leaves the
    door open for Case G, where forgotten constituents will not be a sufficient representation."""
    return root.projection_forgets(target)


def assert_within_domain(view: LawView, family: Family, *, root: Anchor, target: Anchor) -> None:
    """**The family-domain condition, and the whole of it.** Raises `WantOfLaw`, or returns.

    Adjudication order is R13's, and the order is load-bearing: geometry is settled before any law
    is consulted, so a location this family could never stand at is refused as a fact of GEOMETRY
    and never as a missing licence. `Forgotten` is derived only once the projection is known to
    exist."""
    # ── the scope gate ───────────────────────────────────────────────────────────────────────
    if not family_is_primitive(family):
        m = CONSTRUCTED_DOMAIN_UNDECIDED
        raise WantOfLaw(
            f"{view.canonical_reference!r} is a CONSTRUCTED family, and this path has no governed "
            f"reading of its family domain. {m.fact}. That is {m.whose}. It would belong in "
            f"{m.where}. This path will not derive it from the operands, will not union their "
            f"prohibitions, and will not supply a default: filling it here would make an execution "
            f"profile the author of a governed contract",
            subject=view.canonical_reference)

    # ── 1-2 · geometry first, and it is not a law question ───────────────────────────────────
    if not root.refines(target):
        raise WantOfLaw(
            f"{target} is not a Case-S projection of {view.canonical_reference!r}'s family root "
            f"{root}. A coarser location is reached by FORGETTING constituents, never by acquiring "
            f"them — so there is no such location for this family to stand at. This is a fact of "
            f"the universe's governed geometry and NOT a missing licence: no family-domain law "
            f"could admit it, and none was consulted",
            subject=view.canonical_reference)

    # ── 3 · the spend, derived ───────────────────────────────────────────────────────────────
    lost = forgotten(root, target)

    # ── 4 · the family-domain condition ──────────────────────────────────────────────────────
    slot = view[C3_FAMILY_DOMAIN]

    if slot.standing == UNESTABLISHED:
        if not lost:
            return                      # the root itself — admitted by constitution, not by a rule
        raise WantOfLaw(
            f"{view.canonical_reference!r} establishes no family-domain law, so no analytical "
            f"location other than its own family root is admitted. Standing at {target} would "
            f"require forgetting {sorted(lost)}, and §4.1 is explicit that 'a geometrically "
            f"available projection and a computable state operation do not by themselves put A in "
            f"the admitted anchors' — absence of a prohibition is not permission. The remedy is a "
            f"governed declaration by the steward who constitutes this family, not a movement",
            subject=view.canonical_reference)

    if slot.standing == EXPLICIT_NONE:
        if not lost:
            return                      # the root itself — explicitly the whole of the domain
        raise WantOfLaw(
            f"{view.canonical_reference!r} has DECLARED that no off-root analytical domain is "
            f"admitted under its family-domain condition. Standing at {target} would require "
            f"forgetting {sorted(lost)}. This is a positive declaration, not a gap: nothing is "
            f"missing and nothing is to be supplied",
            subject=view.canonical_reference)

    # ESTABLISHED — and the root needs no exception here: Forgotten(A_0 → A_0) is empty, so it
    # passes the ordinary rule rather than an early return justified by what "constitutive" means.
    prohibited = slot.value or frozenset()
    offending = lost & prohibited
    if offending:
        raise WantOfLaw(
            f"{view.canonical_reference!r} may not stand at {target}: its governed family-domain "
            f"law prohibits losing {sorted(offending)}, and the projection from its family root "
            f"{root} forgets {sorted(lost)}. The family is defined at its root and at the "
            f"locations its own law admits; this is not one of them. No movement, licence, "
            f"re-realization or coarser plan can supply what the family's law withholds",
            subject=view.canonical_reference)


def assert_request_within_domain(view: LawView, req) -> None:
    """The same condition, taken from a resolved native request — **the ordinary call site.**

    `req.identity.anchor` IS `A_0`: resolution establishes identity at the constitutive anchor and
    lets the target ride alongside as a request fact, so the root is read from the identity rather
    than recomputed. A non-moving request has no target and adjudicates root-against-root, which is
    not a special case — `Forgotten(A_0 → A_0)` is empty and the ordinary rule decides it."""
    root = req.identity.anchor
    assert_within_domain(view, req.family, root=root, target=req.target or root)


def family_is_primitive(family: Family) -> bool:
    """**The scope gate, read from a field the reader already validated.**

    `formation.kind` is parsed strictly: a primitive formation cannot carry operands and a
    construction must name at least one, so this is a read of a governed fact rather than a
    classification this module invents."""
    formation = family.body.get("formation")
    return isinstance(formation, dict) and formation.get("kind") == "primitive"


def prohibited_constituents(view: LawView) -> Optional[frozenset]:
    """`P_F` where a governed family-domain law establishes one, else `None`.

    Legibility only. No decision may be taken on this without also taking the standing into
    account, because `frozenset()` (an established law prohibiting nothing) and `None` (no law) are
    different governed states."""
    slot = view[C3_FAMILY_DOMAIN]
    return slot.value if slot.standing == ESTABLISHED else None

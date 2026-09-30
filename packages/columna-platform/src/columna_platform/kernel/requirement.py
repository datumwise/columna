"""
columna_platform.kernel.requirement — **what governed family state is NEEDED. The MME's half of the seam.**

    **MME says what governed family state is needed. Realization says what governed family state the
    physical estate can supply. The later Fulfillment Coordinator will decide how to combine those two
    answers.**  — Huayin, 2026-09-29 (R-1)

M-2 left `NEED` as a disposition nobody could act on: the engine can say *"lawful, and I do not hold it"*
and there was no second actor whose job was to obtain it. R-1 introduces that actor, and this module is
the **first half** of the interface between them — deliberately a separate file from
`realization_manager.py`, because the dependency arrow is load-bearing:

    mme.py  ──imports──▶  requirement.py  ◀──imports──  realization_manager.py

**The MME imports this and NOT the manager.** It states what it needs and has no vocabulary at all for who
might supply it, which is the structural form of *"Realization does not bypass MME"* and of *"MME emits
analytical requirements, not fetch plans."* You can delete every provider in the estate and the MME still
compiles, serves, and states its requirements.

WHAT A REQUIREMENT IS, AND THE ONE THING IT MUST NOT BECOME
------------------------------------------------------------
Ruled §2. A `NEED` must remain

    Need lawful Revenue family state sufficient to establish Revenue@Month

and must never become

    query table sales / group by month / sum amount

So there is no table here, no column, no predicate, no projection, no pushdown and no plan. A
`FamilyRequirement` names an **analytical identity, a location, an analytical instance, and the standing
the state must carry** — and physical route planning belongs strictly below the Realization boundary. The
test that guards this is a vocabulary ban: no field of this module may name a physical object.

`acceptable` IS DESCRIPTION, NEVER PERMISSION
---------------------------------------------
A requirement carries the anchors from which the target is lawfully establishable, derived from the family
law rather than supplied by a caller. That list exists so a future Fulfillment Coordinator can see that

    Revenue@Month directly   ·   Revenue@Day then continue   ·   Revenue@Order then continue

are three lawful shapes of the same need (§G). **It confers nothing.** An offer at an anchor in the list
is still adjudicated by `MME.admit` on its own merits, and an offer at an anchor *outside* the list is
adjudicated by exactly the same rule rather than refused for being unlisted — which matters, because the
list is capped for very wide universes and a cap that could cause a false refusal would have turned a
reporting limit into an authority limit.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Optional

from .geometry import Anchor
from .materialization import cumulative_forgotten, entitlement_holds
from .sorts import MeasureFamily
from .standing import AnalyticalInstance

#: How many anchors between the target and `R_F` will be enumerated before the list is truncated. The
#: bound is on the POWER SET of the constituents the target forgets, which is what makes this necessary at
#: all: a 20-constituent universe has a million anchors between a scalar target and its root.
#:
#: **TRUNCATION IS A REPORTING LIMIT AND NEVER AN AUTHORITY LIMIT** — see the module docstring. Nothing
#: consults `acceptable` to decide whether material may be admitted.
ACCEPTABLE_ANCHOR_CAP = 256


def acceptable_anchors(family: MeasureFamily, law: Any, target: Anchor) -> tuple[tuple[Anchor, ...], bool]:
    """**Every anchor from which `target` is lawfully establishable**, coarsest first, and whether the
    enumeration was truncated.

    Two conditions, and both are the family law's rather than a provider's:

      · **reachability** — `target ⊆ A ⊆ R_F`, so `target` is a coarsening of `A`;
      · **entitlement**  — the family may hold a lawful value AT `A`, which is `region.admits(R_F − A)`.

    The second is asked of the intermediate anchor for its own sake. A provider supplying `Revenue@Store`
    when the law admits no value there is offering material the family may not hold, and that it happens to
    lie on a route to an admitted target does not launder it."""
    free = sorted(family.root.constituents - target.constituents)
    if not target.constituents <= family.root.constituents:
        return (), False
    found: list[Anchor] = []
    truncated = False
    for size in range(len(free) + 1):
        for extra in combinations(free, size):
            if len(found) >= ACCEPTABLE_ANCHOR_CAP:
                truncated = True
                break
            candidate = Anchor(universe=target.universe,
                               constituents=frozenset(target.constituents | set(extra)))
            if entitlement_holds(family, law, candidate):
                found.append(candidate)
        if truncated:
            break
    # coarsest first: fewest constituents is least material to fetch, which is the ORDER a reader expects
    # and explicitly NOT a preference — see `ProposalSet`, which refuses to rank at all.
    return tuple(sorted(found, key=lambda a: (len(a.constituents), a.order))), truncated


@dataclass(frozen=True)
class FamilyRequirement:
    """**One analytical requirement for governed family state.** No fetch plan, by construction.

    Ruled §3's conceptual shape, derived rather than copied: `manifold_build`, `family`,
    requested/acceptable anchors, analytical-instance constraints, standing requirements."""

    # ── which semantic world ─────────────────────────────────────────────────────────────────
    manifold: str
    build: str
    # ── which analytical identity, and where ─────────────────────────────────────────────────
    family_id: str
    target: Anchor
    root: Anchor
    #: Anchors from which `target` is lawfully establishable, coarsest first. **Description, not
    #: permission** — see the module docstring.
    acceptable: tuple[Anchor, ...] = ()
    #: Whether `acceptable` was capped. A truncated list is still sound: it never causes a refusal.
    acceptable_truncated: bool = False
    # ── analytical-instance constraints ──────────────────────────────────────────────────────
    instance: Optional[AnalyticalInstance] = None
    #: The evidence state the material must belong to, where the request named one. `None` means the
    #: requirement is indifferent — NOT that any mixture will do.
    data_state: Optional[str] = None
    # ── standing requirements ────────────────────────────────────────────────────────────────
    #: The family's law. Realization must supply state this law can compose, which is a stronger
    #: requirement than "a number of the right dtype".
    law: str = ""
    #: `scalar` / `structured`. A SUM family wants addends; an HLL family wants **sketches**, and supplying
    #: a finalized estimate would be supplying something the law cannot merge.
    value_form: str = ""
    #: **WHAT THE ROOT VALUE THE ESTATE MUST SUPPLY IS CONSTITUTED FROM** (B-4a). One of
    #: `sorts.FORMATION_LAWS`, read off the FAMILY — which declares it — and never off the law.
    #:
    #: Ruled (Huayin, 2026-09-30): *"The provider does not infer formation. It receives the already-governed
    #: formation requirement and executes it."* B-3 established that shape for `fold_shape`; this is the
    #: same arrow for a different fact, and the two facts are deliberately both here and deliberately not
    #: derived from one another:
    #:
    #:     formation    → what `F@R_F` IS            (this field, from the family)
    #:     fold_shape   → what domain contributes    (below, from the law)
    #:     law          → how an established value continues
    #:
    #: A provider reading this supplies a value of the declared formation. **THAT IS NOT INFERENCE EVEN
    #: THOUGH THE PROVIDER COMPUTES SOMETHING** (§7): it performs the physical construction the governed
    #: formation names; it does not decide what the construction means.
    formation: str = ""
    #: **`value-bearing` or `population` — WHAT THE REDUCTION CONTRIBUTES OVER** (B-3).
    #:
    #: Ruled (Huayin, 2026-09-30): *"The provider does not state or infer fold shape. Analytical authority
    #: determines fold shape; `FamilyRequirement` carries that governed requirement to the provider."*
    #:
    #: **THIS IS THE SAME REPAIR B-0b MADE ONE LAYER UP, AND THE SAME DEFECT IT PREVENTS.** B-0b deleted
    #: `_POPULATION_LAWS = frozenset({"COUNT"})` from the columnar cache engine because a law-name
    #: enumeration is constitutional knowledge in a place ruled to hold none. A provider that mapped
    #: `COUNT → population` would have rebuilt that enumeration below the realization boundary instead of
    #: above it, which is the same defect wearing a different address. The fact is a property OF THE LAW —
    #: `AnalyticalLaw.fold_shape` declares it and it is identity-bearing, so it enters the family's
    #: `ConstitutionWitness` — and this field carries it, unexamined, to whoever must satisfy it.
    #:
    #: `AuthorizedFamilyContinuation` carries the same fact through `FoldRequirement.fold_shape`, and that
    #: is **duplication in messages, not duplication of authority**: one says what HELD state needs for
    #: authorized execution, the other what MISSING state the estate must supply. Both read it off the one
    #: law, neither decides it, and a test pins that they agree.
    fold_shape: str = ""
    #: The law's own words for what its composition needs. Carried verbatim so a provider author reads the
    #: requirement rather than inferring it.
    sufficient_state: str = ""
    approximation: str = "exact"
    #: **THE PER-OBJECT CONSTITUTION WITNESS THIS REQUIREMENT IS MADE UNDER** (added by B-1′, and it is the
    #: one governed fact that unit found missing).
    #:
    #: B-1′ requires a physical offer to state which governed environment its claim was made against, so
    #: that a value realized under a declaration that has since moved cannot be admitted as though it were
    #: current. The test-double exercise then exposed that **a provider could not state it, because nothing
    #: ever told it**: this record already carries `manifold`, `build`, `instance`, `law`, `value_form`,
    #: `sufficient_state` and `approximation` — everything else a provider is told about what to supply —
    #: and not the digest of the declaration it is supplying it for.
    #:
    #: It is placed here rather than invented inside the fidelity boundary because this is the object whose
    #: whole purpose is telling a provider what governed state would satisfy a lawful request, and a
    #: constitution digest is that kind of fact. It remains a fact the provider RESTATES and never judges;
    #: `MME.put` compares it.
    witness: str = ""
    #: The `NEED` this requirement came from, in words. Diagnostics; nothing branches on it.
    note: str = ""

    @property
    def forgotten(self) -> frozenset:
        """What reaching `target` from `R_F` forgets. The quantity the family law is asked about."""
        return frozenset(self.root.constituents - self.target.constituents)

    def names_anchor(self, anchor: Anchor) -> bool:
        """Is `anchor` among the ones this requirement listed? **A report, and never a permission test** —
        no admission path calls this, and a `False` is not a refusal."""
        return anchor in self.acceptable

    def render(self) -> str:
        """The requirement in the words §2 asks for, and in no other words."""
        at = f" from {self.data_state}" if self.data_state else ""
        form = f" carrying {self.value_form} state" if self.value_form else ""
        # The fold shape is named because a provider must ESTABLISH A STANDING that satisfies it, and a
        # requirement a provider author has to look up the law to read is a requirement that will be guessed.
        over = f" contributing over its {self.fold_shape} domain" if self.fold_shape else ""
        return (f"Need lawful {self.family_id} family state{form}{over} sufficient to establish "
                f"{self.family_id}@{self.target}{at}")

    def __str__(self) -> str:
        return self.render()


@dataclass(frozen=True)
class RequirementOutcome:
    """**A requirement, or the governed reason there is none.**

    `Optional[FamilyRequirement]` alone would have been a silent `None` at the most important call site in
    the seam: *"this `UNSUPPORTED` request produced no requirement"* and *"this `READY` request produced no
    requirement"* are opposite facts and must not arrive as the same absence."""

    requirement: Optional[FamilyRequirement]
    reason: str = ""

    def __bool__(self) -> bool:
        return self.requirement is not None

    def __str__(self) -> str:
        return str(self.requirement) if self.requirement is not None else f"no requirement — {self.reason}"


__all__ = ["ACCEPTABLE_ANCHOR_CAP", "FamilyRequirement", "RequirementOutcome", "acceptable_anchors",
           "cumulative_forgotten"]

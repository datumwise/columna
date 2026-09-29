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
    #: The law's own words for what its composition needs. Carried verbatim so a provider author reads the
    #: requirement rather than inferring it.
    sufficient_state: str = ""
    approximation: str = "exact"
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
        return (f"Need lawful {self.family_id} family state{form} sufficient to establish "
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

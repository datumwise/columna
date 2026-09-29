"""
columna_platform.kernel.fulfillment — **the Fulfillment Coordinator. F-1: orchestration, nothing else.**

    **Resolver establishes the lawful question. MME governs reusable family materialization. Realization
    describes what missing family state the estate can supply. ExpressionEvaluator owns governed
    expression semantics and delegates heavy columnar compute behind its own provider boundary.
    Fulfillment Coordinator combines these components without inventing analytical authority, execution
    semantics, or economic policy.**  — Huayin, 2026-09-29

Until F-1 the serving loop was a **convention**: a caller wired `measure` → `requirement_from` →
`propose` → `realize` → `establish` → `measure` by hand, and every caller wired it slightly differently
or not at all. This module is that loop as a component, and it is deliberately the smallest component
that could be one.

WHAT IT OWNS, AND THE FOUR THINGS IT DOES NOT
----------------------------------------------
It owns **how** a lawful analytical request is fulfilled using the three actors that already exist. It
does not decide analytical meaning (the Resolver and the family law do), does not perform physical
realization (providers do), does not perform heavy expression compute (the evaluator and its own provider
boundary do), and does not manage cache internals (the MME does). Every one of those is enforced by what
this module cannot reach: it holds no store, no law registry, no provider profile and no Arrow.

THE DISPOSITION IS NOT READ OFF THE OBSERVATION LOG
-----------------------------------------------------
The coordinator must tell `NEED` from `UNSUPPORTED` from `WANT_OF_STATE` (§3: *"Do not collapse these
into generic failure"*), and M-2 computes exactly that classification — **into the observation record**.
The obvious implementation is to read it back from there. **That would be a defect**, and a subtle one:
M-2 §6 rules that *"observations never create analytical rights"*, and a coordinator that routed on an
observation would have made the workload log authoritative over serving. The sink is write-only for this
reason and the coordinator never touches it.

So the mood is derived from facts the serving path already returns:

    `answer.served`                            → SERVED
    `answer.refusal.code == "want-of-state"`   → UNRESOLVED_STATE   (a direct, unwrapped refusal)
    otherwise, ask the MME for a REQUIREMENT:
        a requirement exists                   → NEED     (lawful, and we do not hold it)
        no requirement, with a reason          → NOT_SUPPORTED

That second question is `MME.requirement_for`, which is R-1's seam doing precisely its job — *"MME emits
analytical requirements"* — rather than a classification being read off a log line. It is also the
stronger test: `requirement_for` refuses for an unlawful target, for a target outside `R_F`, **and** for a
law this build cannot realize, which are three different ways to be unsupported and all three are things
no amount of realization would fix.

NOTHING HERE CHOOSES A ROUTE
-----------------------------
Ruled §2 and §8. The policy is replaceable behind `RoutePolicy.choose`, and F-1's policy is the least
opinionated one that can exist:

    0 proposals  → lawful but unavailable
    1 proposal   → take it
    >1 proposals → **route-policy-needed, and nothing is executed**

Explicitly NOT *"take the coarsest"*: coarsest is fewest cells, which is a fact about size and says
nothing about network cost, backend latency, pushdown, locality or descendant reuse — all of which belong
to the fulfillment-cost quantity that has not been ruled. A placeholder that looked like a preference
would be a preference, and the next unit would inherit it as a decision nobody made.

TERMINATION IS A BOUND, NOT A HOPE
-----------------------------------
Ruled §4. One realization round by default: attempt, realize once, retry once, stop. There is no
recursive chase of realization chains and no condition under which the loop runs longer than `rounds + 1`
measurements. A coordinator whose termination depended on the estate eventually cooperating would be a
coordinator that hangs when it does not.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Optional, Protocol, runtime_checkable

from .geometry import Anchor
from .observation import NEED as NEED_DISPOSITION
from .realization_manager import ProposalSet, RealizationProposal, RealizationManager
from .requirement import FamilyRequirement
from .value import Answer

# ── the fulfillment moods ────────────────────────────────────────────────────────────────────────
#
# **THESE ARE NOT M-2's DISPOSITIONS AND MUST NOT BE CONFUSED WITH THEM** (§3). An MME disposition
# answers *"what did the cache say?"*; a fulfillment mood answers *"what happened to the request, after
# everyone who could help was asked?"* One `NEED` becomes three different moods depending on what the
# estate offers, which is exactly the information a caller needs and exactly what a collapsed
# `FulfillmentError` would have destroyed.
SERVED = "served"
#: Lawful, not held, and the estate offers nothing. **Not a refusal about the question** — the question is
#: fine and the answer is obtainable in principle. Nobody can obtain it right now.
UNAVAILABLE = "lawful-but-unavailable"
#: Lawful, not held, and the estate offers MORE THAN ONE admissible way to get it. Nothing was executed.
#: This is a request for a decision that F-1 deliberately cannot make (§2, §8).
ROUTE_POLICY_NEEDED = "route-policy-needed"
#: The material is held and the VALUE it requires is not established at some participating points. A
#: realizable need of a DIFFERENT shape (R-1 §F), and not a cache miss.
UNRESOLVED_STATE = "unresolved-required-state"
#: No lawful route to this target exists in this build — outside the continuation region, outside `R_F`,
#: or a law this provider profile cannot execute. **An implementation/profile limitation**, and retaining
#: or fetching anything would not change it.
NOT_SUPPORTED = "implementation-limitation"
#: Realization ran, admission happened or was refused, and the target is STILL not servable within the
#: round bound. Distinct from `UNAVAILABLE`: work was done and it was not enough.
INCOMPLETE = "incomplete-fulfillment"

MOODS = (SERVED, UNAVAILABLE, ROUTE_POLICY_NEEDED, UNRESOLVED_STATE, NOT_SUPPORTED, INCOMPLETE)


# ── the route-policy seam ────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RouteContext:
    """**What a route policy is allowed to see today**, which is deliberately almost nothing.

    It exists so that the signature `choose(requirement, proposals, context)` is stable while the third
    argument grows. A future cost model will reach through here for demand, latency, backend price,
    cached-continuation cost and descendant reuse value — **none of which is here, and none of which is
    stubbed**, because a field carrying a zero is a cost model asserting that everything is free."""

    target: str
    round: int
    manifold: str = ""
    build: str = ""
    #: Proposals already attempted in earlier rounds, so a policy cannot loop on one that failed.
    attempted: tuple[str, ...] = ()


@dataclass(frozen=True)
class RouteDecision:
    """A policy's answer: one proposal, or the mood that explains why not one."""

    chosen: Optional[RealizationProposal] = None
    mood: str = ""
    reason: str = ""

    def __bool__(self) -> bool:
        return self.chosen is not None


@runtime_checkable
class RoutePolicy(Protocol):
    """**Replaceable by construction** (§8). One method, and the coordinator calls nothing else."""

    name: str

    def choose(self, requirement: FamilyRequirement, proposals: ProposalSet,
               context: RouteContext) -> RouteDecision: ...


class UnambiguousRoute:
    """**F-1's policy: choose only when there is nothing to choose.**

        0 proposals  → `lawful-but-unavailable`
        1 proposal   → take it
        >1 proposals → `route-policy-needed`, and **nothing is executed**

    Ruled §2/§8: no ranking, no scoring, no cost estimation. The >1 case is the interesting one and it is
    deliberately not a tie-break — it is a refusal to invent the policy that has not been ruled. A caller
    that receives `route-policy-needed` is holding every alternative, unexecuted, and can decide."""

    name = "unambiguous-route-only"

    def choose(self, requirement: FamilyRequirement, proposals: ProposalSet,
               context: RouteContext) -> RouteDecision:
        available = tuple(p for p in proposals.proposals
                          if f"{p.provider}:{p.anchor}" not in context.attempted)
        if not available:
            asked = f"{len(proposals.consulted)} provider(s) consulted"
            declined = "; ".join(f"{name}: {why}" for name, why in proposals.declined)
            return RouteDecision(
                mood=UNAVAILABLE,
                reason=f"{requirement.render()} — and the estate offers no way to obtain it. {asked}"
                       + (f" — {declined}" if declined else "")
                       + ". **THE QUESTION IS LAWFUL AND THE ANSWER IS OBTAINABLE IN PRINCIPLE**; what is "
                         "absent is a provider that can supply it now. This is not a refusal about the "
                         "request.")
        if len(available) == 1:
            return RouteDecision(chosen=available[0],
                                 reason=f"exactly one admissible way to obtain "
                                        f"{requirement.family_id}@{requirement.target}: "
                                        f"{available[0]}. Chosen because there was nothing to choose.")
        return RouteDecision(
            mood=ROUTE_POLICY_NEEDED,
            reason=f"{len(available)} admissible ways to obtain {requirement.family_id}@"
                   f"{requirement.target} — {[str(p) for p in available]} — and **NOTHING HAS BEEN "
                   f"EXECUTED**. Choosing among them is a route-policy decision, and F-1 does not have "
                   f"one: the relevant quantity is end-to-end lawful fulfillment cost (network, backend "
                   f"price, latency, pushdown, cached-continuation cost, descendant reuse), none of "
                   f"which is observable from here. Taking the coarsest would have been a preference "
                   f"wearing the clothes of a placeholder.")


# ── what came back ───────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RealizedRoute:
    """One realization the coordinator actually performed. **The coordinator's own report** — distinct
    from the workload observation, which records the REQUEST and is written by the MME."""

    provider: str
    family_id: str
    anchor: Anchor
    admitted: bool
    detail: str = ""

    def __str__(self) -> str:
        return (f"{self.family_id}@{self.anchor} from {self.provider} "
                f"{'ADMITTED' if self.admitted else 'REFUSED'}")


@dataclass(frozen=True)
class FulfillmentOutcome:
    """**What happened to one request, and by which route.**

    Named `FulfillmentOutcome` and not `Fulfillment` on purpose: `observation.Fulfillment` already exists
    and is a different thing — the work-performed part of a workload record. One is the coordinator's
    answer to a caller; the other is the MME's note to a future cache economist."""

    mood: str
    target: str
    answer: Optional[Answer] = None
    #: The MME disposition that produced this mood, where there was one. Reported, never routed on by
    #: anyone downstream — see the module docstring.
    disposition: str = ""
    detail: str = ""
    #: Realizations actually performed, in order. Empty on every path that executed nothing.
    realized: tuple[RealizedRoute, ...] = ()
    #: The unexecuted alternatives, present only on `route-policy-needed` — the caller is handed the
    #: whole choice rather than a summary of it.
    proposals: Optional[ProposalSet] = None
    #: Per-operand outcomes, on an expression request.
    operands: tuple["FulfillmentOutcome", ...] = ()
    rounds: int = 0
    elapsed_ns: int = 0

    def __bool__(self) -> bool:
        return self.mood == SERVED

    @property
    def served(self) -> bool:
        return self.mood == SERVED

    @property
    def value(self) -> Any:
        if self.answer is None or not self.answer.served:
            raise self._cannot()
        return self.answer.value

    def cell(self, key: tuple = ()):
        if self.answer is None or not self.answer.served:
            raise self._cannot()
        return self.answer.cell(key)

    def _cannot(self):
        from .geometry import KernelRefusal

        return KernelRefusal(self.mood, self.target, self.detail)

    def __str__(self) -> str:
        via = f" via {len(self.realized)} realization(s)" if self.realized else ""
        return f"{self.mood.upper()}  {self.target}{via}"


# ── the coordinator ──────────────────────────────────────────────────────────────────────────────
class FulfillmentCoordinator:
    """**The serving loop, as a component.**

    Holds the three actors and composes them. Note what it does NOT hold: no `MaterializationStore`, no
    `LawRegistry`, no `ProviderProfile`, no `CoordinateIndex`, nothing from `pyarrow` and nothing from
    `datafusion`. It cannot construct a materialization, cannot evaluate an expression and cannot execute
    a query; every one of those belongs to a component it merely calls."""

    def __init__(self, mme: Any, *, realization: Optional[RealizationManager] = None,
                 evaluator: Any = None, policy: Optional[RoutePolicy] = None,
                 rounds: int = 1) -> None:
        self.mme = mme
        #: An empty manager is a valid estate: it consults nobody and offers nothing, which is the honest
        #: state of a deployment with no providers configured and produces `lawful-but-unavailable`.
        self.realization = realization if realization is not None else RealizationManager()
        #: Constructed here if not supplied, because expression support is not optional — but injected
        #: readily, because **the coordinator must not know how the evaluator computes** (§1). It calls
        #: `evaluate` and reads `admitted_bases`; it never learns whether Arrow, DataFusion, DuckDB or a
        #: native kernel did the work.
        self.evaluator = evaluator if evaluator is not None else self._default_evaluator(mme)
        self.policy: RoutePolicy = policy if policy is not None else UnambiguousRoute()
        #: **The bound** (§4). `rounds=1` means: attempt, realize once, retry once, stop.
        self.rounds = max(0, int(rounds))

    @staticmethod
    def _default_evaluator(mme: Any) -> Any:
        from .expression import ExpressionEvaluator

        return ExpressionEvaluator(mme)

    # ── the family loop ──────────────────────────────────────────────────────────────────────
    def fulfill(self, family: Any, anchor: Anchor, *, data_state: Optional[str] = None,
                on_behalf_of: str = "") -> FulfillmentOutcome:
        """**Fulfil one family target.** Deterministic, bounded, and it executes at most `rounds`
        realizations.

        `family` may be a `MeasureFamily` or a `family_id`; the engine normalises it. That widening is
        F-1's only change to an existing interface, and it exists because the two engines' `measure`
        signatures had diverged far enough that no component above both could call either."""
        started = time.perf_counter_ns()
        # **EITHER SPELLING, AND THE ENGINE NORMALISES IT** (F-1's one seam correction). The coordinator
        # does not itself know how to turn a token into a family — that is the analytical authority's
        # registry — so it asks, and thereby works over the in-memory and columnar engines unchanged.
        family = self.mme.subject(family)
        target = f"{family.family_id}@{anchor}"
        realized: list[RealizedRoute] = []
        attempted: list[str] = []

        for round_index in range(self.rounds + 1):
            answer = self.mme.measure(family, anchor, data_state=data_state,
                                      on_behalf_of=on_behalf_of)
            if answer.served:
                return self._outcome(SERVED, target, started, answer=answer, disposition="ready",
                                     realized=tuple(realized), rounds=round_index)

            mood, detail, requirement = self._diagnose(family, anchor, answer, data_state)
            if mood is not None:
                return self._outcome(mood, target, started, answer=answer,
                                     disposition=self._disposition_of(mood), detail=detail,
                                     realized=tuple(realized), rounds=round_index)

            # ── NEED ─────────────────────────────────────────────────────────────────────────
            if round_index >= self.rounds:
                return self._outcome(
                    INCOMPLETE, target, started, answer=answer, disposition=NEED_DISPOSITION,
                    detail=f"{requirement.render()} — still NEED after {round_index} realization "
                           f"round(s), which is this coordinator's explicit bound. **NO FURTHER "
                           f"ATTEMPT IS MADE**, deliberately: chasing realization chains until they "
                           f"resolve would make termination depend on the estate cooperating. "
                           + (f"Realized so far: {[str(r) for r in realized]}." if realized else ""),
                    realized=tuple(realized), rounds=round_index)

            proposals = self.realization.propose(requirement)
            decision = self.policy.choose(
                requirement, proposals,
                RouteContext(target=target, round=round_index, manifold=requirement.manifold,
                             build=requirement.build, attempted=tuple(attempted)))
            if not decision:
                return self._outcome(decision.mood, target, started, answer=answer,
                                     disposition=NEED_DISPOSITION, detail=decision.reason,
                                     realized=tuple(realized),
                                     proposals=proposals if decision.mood == ROUTE_POLICY_NEEDED
                                     else None,
                                     rounds=round_index)

            # ── one realization, through the ordinary door ───────────────────────────────────
            chosen = decision.chosen
            attempted.append(f"{chosen.provider}:{chosen.anchor}")
            offer = self.realization.realize(chosen)
            admission = self.realization.establish(self.mme, offer)
            realized.append(RealizedRoute(
                provider=offer.provider, family_id=offer.family_id, anchor=offer.anchor,
                admitted=bool(admission),
                detail=str(admission.id) if admission else f"{admission.code}: {admission.detail}"))
            # **AND THE LOOP RETRIES THROUGH `measure`.** Not through the offer, and not by returning the
            # offer's value directly: a realized value that `admit` refused must not be served, and the
            # only thing that knows whether it was admitted — and whether it is the best current
            # materialization — is the MME. There is no serving shortcut here (§5).

        # unreachable while `rounds >= 0`; kept total rather than trusting the arithmetic
        return self._outcome(INCOMPLETE, target, started, realized=tuple(realized),  # pragma: no cover
                             rounds=self.rounds, detail="the round bound was exhausted")

    # ── the expression loop ──────────────────────────────────────────────────────────────────
    def fulfill_expression(self, expression: Any, anchor: Anchor, *, basis_id: Optional[str] = None,
                           data_state: Optional[str] = None) -> FulfillmentOutcome:
        """**Fulfil one expression target**: make its family operands available, then hand over.

        Ruled §6. The coordinator's entire contribution is the first clause — it fulfils the family
        operands a declared basis needs, through the ordinary family loop, so realization can happen for
        them. Then it calls `evaluator.evaluate` **once** and returns what the evaluator says.

        **IT DOES NOT SELECT A BASIS AND DOES NOT EVALUATE ANYTHING.** Basis selection is governed
        semantics and belongs to the evaluator, which tries admitted bases in declaration order. What the
        coordinator walks is the same declared order, for the sole purpose of deciding which operands to
        make available — and it stops walking as soon as one basis's operands are all fulfillable, because
        that is the basis the evaluator will use. When the evaluator then calls `measure` for those
        operands, they are warm and it gets `READY`.

        **NO EXPRESSION OUTPUT ENTERS THE MME** and none is cached here: there is no store on this class
        either, and the evaluator has none (M-2 §1)."""
        started = time.perf_counter_ns()
        target = f"{expression.expression_id}@{anchor}"
        bases = ([b for b in expression.admitted_bases if b.basis_id == basis_id]
                 if basis_id else list(expression.admitted_bases))

        operands: list[FulfillmentOutcome] = []
        realized: list[RealizedRoute] = []
        for basis in bases:
            attempts = [
                self.fulfill(self.mme.family(basis.components[role]), anchor,
                             data_state=data_state,
                             on_behalf_of=f"{expression.expression_id}@{anchor} via {basis.basis_id}")
                for role in basis.component_laws]
            operands = attempts
            realized.extend(r for a in attempts for r in a.realized)
            # **A ROUTE-POLICY DECISION STOPS EVERYTHING**, rather than quietly falling through to the
            # next basis. Falling through would let the coordinator avoid a decision it was asked to
            # surface, and the caller would never learn that a choice was waiting.
            blocked = next((a for a in attempts if a.mood == ROUTE_POLICY_NEEDED), None)
            if blocked is not None:
                return self._outcome(ROUTE_POLICY_NEEDED, target, started, detail=blocked.detail,
                                     proposals=blocked.proposals, operands=tuple(attempts),
                                     realized=tuple(realized))
            if all(a.served for a in attempts):
                break

        # ── AND NOW THE EVALUATOR, WHICH OWNS EVERYTHING FROM HERE ───────────────────────────
        # Compatibility, basis selection, the constructor, finalization, the refusals — all of it is
        # governed semantics and none of it is the coordinator's. Whether the evaluator computes with
        # Python dicts, Arrow kernels, DataFusion or something not written yet is invisible from here,
        # which is the property F-1 exists to preserve.
        answer = self.evaluator.evaluate(expression, anchor, basis_id=basis_id,
                                         data_state=data_state)
        if answer.served:
            return self._outcome(SERVED, target, started, answer=answer, disposition="ready",
                                 realized=tuple(realized), operands=tuple(operands))
        # The evaluator refused. The coordinator reports the operand story ALONGSIDE the governed
        # refusal and does not replace it: "role unfilled" and "incompatible basis" are different facts
        # and only the evaluator can tell them apart.
        unfulfilled = [o for o in operands if not o.served]
        mood = (unfulfilled[0].mood if unfulfilled else NOT_SUPPORTED)
        return self._outcome(mood, target, started, answer=answer,
                             detail=answer.refusal.detail if answer.refusal else "",
                             realized=tuple(realized), operands=tuple(operands))

    # ── diagnosis: NEED vs WANT_OF_STATE vs UNSUPPORTED ──────────────────────────────────────
    def _diagnose(self, family: Any, anchor: Anchor, answer: Answer,
                  data_state: Optional[str]) -> tuple[Optional[str], str, Any]:
        """**Which kind of not-served is this?** Returns `(mood, detail, requirement)`; `mood is None`
        means NEED and the requirement is populated.

        Reads only what serving returned and what the MME will state as a requirement — never the
        observation log (see the module docstring)."""
        code = answer.refusal.code if answer.refusal else ""
        if code in ("want-of-state", "basis-operand-wants-state"):
            return (UNRESOLVED_STATE,
                    f"{answer.refusal.detail} **THIS IS NOT A CACHE MISS AND NOT A FETCH**: the "
                    f"material is held and the value it requires is not established. Realization of a "
                    f"coarser anchor would not supply it.", None)
        outcome = self.mme.requirement_for(family, anchor, data_state=data_state,
                                           note="fulfillment coordinator")
        if not outcome:
            return (NOT_SUPPORTED, outcome.reason, None)
        return (None, "", outcome.requirement)

    @staticmethod
    def _disposition_of(mood: str) -> str:
        from .observation import UNSUPPORTED, WANT_OF_STATE

        return {UNRESOLVED_STATE: WANT_OF_STATE, NOT_SUPPORTED: UNSUPPORTED}.get(mood, "")

    @staticmethod
    def _outcome(mood: str, target: str, started: int, **kwargs) -> FulfillmentOutcome:
        return FulfillmentOutcome(mood=mood, target=target,
                                  elapsed_ns=max(0, time.perf_counter_ns() - started), **kwargs)


__all__ = ["INCOMPLETE", "MOODS", "NOT_SUPPORTED", "ROUTE_POLICY_NEEDED", "SERVED", "UNAVAILABLE",
           "UNRESOLVED_STATE", "FulfillmentCoordinator", "FulfillmentOutcome", "RealizedRoute",
           "RouteContext", "RouteDecision", "RoutePolicy", "UnambiguousRoute"]

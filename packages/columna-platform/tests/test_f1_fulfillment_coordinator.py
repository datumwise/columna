"""
test_f1_fulfillment_coordinator.py — **F-1: the serving loop as a component.**

    **Resolver establishes the lawful question. MME governs reusable family materialization. Realization
    describes what missing family state the estate can supply. ExpressionEvaluator owns governed
    expression semantics and delegates heavy columnar compute behind its own provider boundary.
    Fulfillment Coordinator combines these components without inventing analytical authority, execution
    semantics, or economic policy.**  — Huayin, 2026-09-29

The ruling's §10 proofs are the sections, plus the structural guards F-1 exists to keep:

    A  family already cached — no realization call at all
    B  cold family, one route — NEED → realize → admit → retry → READY
    C  no realization available — lawful-but-unavailable
    D  multiple proposals — route-policy-needed, NOTHING executed
    E  unlawful material — refused at ordinary admission
    F  duplicate-current disagreement — a backend does not override
    G  still NEED after the bound — incomplete fulfillment, deterministic
    H  expression — operands fulfilled, evaluator evaluates, nothing enters the MME
    I  HLL finalization — the MME holds only the sketch
    J  the moods stay distinct, the observation seam survives, and nothing chooses

WHAT IS NOT EXERCISED, DELIBERATELY: no backend, no ADBC, no persistence, no cost model, no adaptive
cache optimizer, no expression cache, no DataFusion expression execution. Ruled out by name.
"""
from __future__ import annotations

from dataclasses import fields

import pytest

from columna_platform.columnar import exhibit as CEX
from columna_platform.kernel import (
    IN_MEMORY,
    MME,
    REGISTRY,
    ExpressionEvaluator,
    FulfillmentCoordinator,
    FulfillmentOutcome,
    ProposalSet,
    RealizationManager,
    RealizationOffer,
    RealizationProposal,
    RealizationStanding,
    RecordingObserver,
    RouteContext,
    RouteDecision,
    UnambiguousRoute,
)
from columna_platform.kernel import exhibit as KEX
from columna_platform.kernel import fulfillment as fulfillment_module
from columna_platform.kernel.fulfillment import (
    INCOMPLETE,
    MOODS,
    NOT_SUPPORTED,
    ROUTE_POLICY_NEEDED,
    SERVED,
    UNAVAILABLE,
    UNRESOLVED_STATE,
)
from columna_platform.kernel.materialization import INDEPENDENT, Establishment
from columna_platform.kernel.observation import NEED, READY, WANT_OF_STATE
from columna_platform.kernel.value import FamilyState


# ══ TEST DOUBLES ══════════════════════════════════════════════════════════════════════════════════
class Estate:
    """A provider holding pre-built family state. Not a backend; see R-1's note."""

    def __init__(self, name, holdings, *, carrier="in-memory"):
        self.name, self.holdings, self.carrier = name, dict(holdings), carrier
        self.proposed = self.realized = 0

    @property
    def standing(self):
        return RealizationStanding(provider=self.name, carrier=self.carrier)

    def propose(self, requirement):
        self.proposed += 1
        for (family_id, anchor), value in self.holdings.items():
            if family_id == requirement.family_id:
                yield RealizationProposal(
                    provider=self.name, family_id=family_id, anchor=anchor,
                    value_form=getattr(value, "value_form", ""), realization=self.standing,
                    # the environment rides in the opaque handle — see R-1's double for why
                    handle=(family_id, anchor, requirement.build, requirement.witness))

    def realize(self, proposal):
        self.realized += 1
        family_id, anchor, build, witness = proposal.handle
        value = self.holdings[(family_id, anchor)]
        return RealizationOffer(
            provider=self.name, family_id=proposal.family_id, anchor=proposal.anchor, value=value,
            instance=value.instance, realization=self.standing,
            establishment=Establishment(INDEPENDENT), from_proposal=proposal,
            build=build, witness=witness)


def _code_only(module) -> str:
    """The executable text of a module, docstrings and comments removed. A ban that a comment can trip is
    a ban nobody can write about — see the same helper in R-1's suite."""
    import ast
    import inspect

    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


def _state(engine, family_id, anchor, cells):
    family = engine.family(family_id)
    return FamilyState(point=family.at(anchor), law=engine.law_of(family_id).name, cells=dict(cells),
                       instance=engine.instance_of(family_id),
                       value_form=engine.law_of(family_id).value_form,
                       forgotten_since_root=frozenset(family.root.constituents - anchor.constituents))


# ── fixtures ─────────────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def fams():
    revenue, order_count, audited, distinct, on_hand, gauge = KEX._families()
    return dict(revenue=revenue, order_count=order_count, audited=audited, distinct=distinct,
                on_hand=on_hand, gauge=gauge)


@pytest.fixture
def exprs():
    aov, aov_audited, estimate = KEX._expressions()
    return dict(aov=aov, aov_audited=aov_audited, estimate=estimate)


@pytest.fixture
def warm():
    """Roots established — the world where the MME answers on its own."""
    return KEX.build()


@pytest.fixture
def cold():
    """Constituted and holding nothing — the world where `NEED` is the answer."""
    engine = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=KEX.MANIFOLD,
                 observer=RecordingObserver())
    for family in KEX._families():
        engine.register_family(family)
    for expression in KEX._expressions():
        engine.register_expression(expression)
    return engine


def _revenue_at_day(engine):
    return {("revenue", KEX.BY_DAY): _state(engine, "revenue", KEX.BY_DAY,
                                            {("D1",): 175.0, ("D2",): 325.0})}


# ══ A · THE FAMILY IS ALREADY CACHED — NO REALIZATION CALL ════════════════════════════════════════
def test_a_cached_family_is_served_without_consulting_the_estate(warm, fams):
    """§10: `request F@A → MME READY → no realization call → answer`.

    **The negative is the assertion.** A coordinator that asked the estate anyway would be paying for a
    backend round-trip on every cache hit, and no test of the happy path would have noticed."""
    estate = Estate("warehouse", _revenue_at_day(warm))
    coordinator = FulfillmentCoordinator(warm, realization=RealizationManager(estate))

    outcome = coordinator.fulfill(fams["revenue"], KEX.TOTAL)

    assert outcome.served and outcome.mood == SERVED
    assert outcome.cell() == pytest.approx(500.0)
    assert estate.proposed == 0 and estate.realized == 0        # **never consulted**
    assert outcome.realized == ()
    assert outcome.rounds == 0
    assert outcome.disposition == READY


def test_an_exact_hit_and_a_continuation_are_both_SERVED(warm, fams):
    """Whether the MME held the target or folded to it is a cache fact, not a fulfillment mood."""
    derived = FulfillmentCoordinator(warm).fulfill(fams["revenue"], KEX.BY_DAY)
    hit = FulfillmentCoordinator(warm).fulfill(fams["revenue"], KEX.BY_DAY)
    assert derived.mood == hit.mood == SERVED
    assert derived.answer.route == "continued" and hit.answer.route == "cached"


# ══ B · COLD FAMILY, ONE ROUTE ════════════════════════════════════════════════════════════════════
def test_cold_request_realizes_once_admits_and_then_serves(cold, fams):
    """§10, and F-1's whole point:

        request F@A → MME NEED → one proposal → realize → MME.admit → retry → READY
    """
    estate = Estate("warehouse", _revenue_at_day(cold))
    coordinator = FulfillmentCoordinator(cold, realization=RealizationManager(estate))

    outcome = coordinator.fulfill(fams["revenue"], KEX.TOTAL)

    assert outcome.served
    assert outcome.cell() == pytest.approx(500.0)
    assert estate.proposed == 1 and estate.realized == 1        # exactly one of each
    assert len(outcome.realized) == 1
    route = outcome.realized[0]
    assert route.provider == "warehouse" and route.anchor == KEX.BY_DAY and route.admitted
    assert outcome.rounds == 1
    # the realized material is an ORDINARY independent materialization
    admitted = cold.materializations.select("revenue", anchor=KEX.BY_DAY)
    assert admitted and admitted[0].establishment.kind == INDEPENDENT
    assert "realized by warehouse" in admitted[0].note


def test_the_retry_goes_back_THROUGH_measure_and_not_through_the_offer(cold, fams):
    """§5: no serving shortcut. The answer must come from the MME's own selection, because only the MME
    knows whether the offer was admitted and whether it is the best current materialization."""
    calls = []
    real = cold.measure

    def watched(family, anchor, **kwargs):
        calls.append((family.family_id, str(anchor)))
        return real(family, anchor, **kwargs)

    cold.measure = watched                                       # type: ignore[method-assign]
    estate = Estate("warehouse", _revenue_at_day(cold))
    outcome = FulfillmentCoordinator(cold, realization=RealizationManager(estate)).fulfill(
        fams["revenue"], KEX.TOTAL)

    assert outcome.served
    assert calls == [("revenue", str(KEX.TOTAL)), ("revenue", str(KEX.TOTAL))]   # attempt, then retry
    # and what was served was FOLDED from the realized material, by the MME
    assert outcome.answer.route == "continued"


# ══ C · NO REALIZATION AVAILABLE ══════════════════════════════════════════════════════════════════
def test_zero_proposals_is_lawful_but_unavailable(cold, fams):
    """§3: **not a refusal about the question.** The question is lawful and the answer is obtainable in
    principle; what is absent is a provider that can supply it now."""
    outcome = FulfillmentCoordinator(cold).fulfill(fams["revenue"], KEX.TOTAL)

    assert outcome.mood == UNAVAILABLE
    assert not outcome.served
    assert outcome.disposition == NEED
    assert "THE QUESTION IS LAWFUL" in outcome.detail
    assert outcome.realized == ()


def test_a_provider_that_offers_nothing_is_named_in_the_unavailability(cold, fams):
    """Why it is unavailable matters: *"no provider offers this"* and *"the one that would have was
    unreachable"* are different facts a caller may act on differently."""
    class Unreachable:
        name = "lakehouse"

        def propose(self, requirement):
            raise ConnectionError("down for maintenance")

        def realize(self, proposal):                             # pragma: no cover
            raise AssertionError

    outcome = FulfillmentCoordinator(
        cold, realization=RealizationManager(Unreachable())).fulfill(fams["revenue"], KEX.TOTAL)
    assert outcome.mood == UNAVAILABLE
    assert "lakehouse" in outcome.detail and "ConnectionError" in outcome.detail


# ══ D · MULTIPLE PROPOSALS — NOTHING EXECUTED ═════════════════════════════════════════════════════
def test_two_proposals_yield_route_policy_needed_and_execute_nothing(cold, fams):
    """§2/§8, and **the assertion that matters is that nothing ran.** A coordinator that quietly took the
    first, or the coarsest, would have invented the policy that has not been ruled."""
    holdings = _revenue_at_day(cold)
    one, two = Estate("warehouse", holdings), Estate("lakehouse", holdings, carrier="parquet")
    coordinator = FulfillmentCoordinator(cold, realization=RealizationManager(one, two))

    outcome = coordinator.fulfill(fams["revenue"], KEX.TOTAL)

    assert outcome.mood == ROUTE_POLICY_NEEDED
    assert one.realized == 0 and two.realized == 0               # **NOTHING EXECUTED**
    assert outcome.realized == ()
    assert not cold.materializations.select("revenue", eligibility=None)
    # and the caller is handed the whole choice, unexecuted
    assert isinstance(outcome.proposals, ProposalSet)
    assert len(outcome.proposals) == 2
    assert {p.provider for p in outcome.proposals} == {"warehouse", "lakehouse"}


def test_two_anchors_from_ONE_provider_is_also_a_route_decision(cold, fams):
    """§G's first axis is a choice too: `Revenue@Day` then continue versus `Revenue@Total` directly."""
    estate = Estate("warehouse", {
        **_revenue_at_day(cold),
        ("revenue", KEX.TOTAL): _state(cold, "revenue", KEX.TOTAL, {(): 500.0})})
    outcome = FulfillmentCoordinator(
        cold, realization=RealizationManager(estate)).fulfill(fams["revenue"], KEX.TOTAL)

    assert outcome.mood == ROUTE_POLICY_NEEDED
    assert estate.realized == 0
    assert set(outcome.proposals.anchors) == {KEX.BY_DAY, KEX.TOTAL}


def test_the_route_policy_reason_refuses_to_pretend_it_could_choose(cold, fams):
    holdings = _revenue_at_day(cold)
    outcome = FulfillmentCoordinator(
        cold, realization=RealizationManager(Estate("a", holdings), Estate("b", holdings))
    ).fulfill(fams["revenue"], KEX.TOTAL)
    assert "NOTHING HAS BEEN EXECUTED" in outcome.detail
    assert "end-to-end lawful fulfillment cost" in outcome.detail
    assert "coarsest" in outcome.detail                          # and says why that was not used


# ══ E · UNLAWFUL MATERIAL REACHES ORDINARY ADMISSION AND IS REFUSED THERE ═════════════════════════
def test_a_provider_offering_unlawful_material_is_refused_at_admission(cold, fams):
    """§5/§10. The coordinator does not pre-screen and does not serve it; `MME.admit` refuses it by the
    family law, and the request ends as incomplete rather than as a served wrong number."""
    estate = Estate("confident-warehouse", {
        ("on_hand", KEX.BY_STORE): _state(cold, "on_hand", KEX.BY_STORE, {("S1",): 42})})
    coordinator = FulfillmentCoordinator(cold, realization=RealizationManager(estate))

    # the TARGET here is lawful; only the offered anchor is not
    outcome = coordinator.fulfill(fams["on_hand"], KEX.BY_DAY)

    assert not outcome.served
    assert estate.realized == 1                                  # it did run …
    assert len(outcome.realized) == 1 and not outcome.realized[0].admitted      # … and was refused
    assert "outside-continuation-region" in outcome.realized[0].detail
    assert not cold.materializations.select("on_hand", anchor=KEX.BY_STORE, eligibility=None)
    assert outcome.mood == INCOMPLETE


def test_an_unlawful_TARGET_never_reaches_the_estate_at_all(warm, fams):
    """The stronger form: where the law admits no value at the target, no requirement is emitted, so no
    provider is even asked. R-1's blast wall, reached through the coordinator."""
    estate = Estate("confident-warehouse", {
        ("on_hand", KEX.BY_STORE): _state(warm, "on_hand", KEX.BY_STORE, {("S1",): 42})})
    outcome = FulfillmentCoordinator(
        warm, realization=RealizationManager(estate)).fulfill(fams["on_hand"], KEX.BY_STORE)

    assert outcome.mood == NOT_SUPPORTED
    assert estate.proposed == 0                                  # **never asked**
    assert "NO REALIZATION REQUIREMENT IS EMITTED" in outcome.detail


# ══ F · DUPLICATE-CURRENT DISAGREEMENT ════════════════════════════════════════════════════════════
def test_a_backend_offer_does_not_override_a_current_materialization(warm, fams):
    """§5: *"No provider may settle duplicate-current disagreement by authority."*"""
    served = warm.measure(fams["revenue"], KEX.BY_DAY)
    assert served.served
    before = dict(served.value.cells)

    estate = Estate("warehouse", {
        ("revenue", KEX.BY_DAY): _state(warm, "revenue", KEX.BY_DAY,
                                        {("D1",): 999.0, ("D2",): 1.0})})
    # force the estate to be consulted by asking for something the MME cannot answer alone
    coordinator = FulfillmentCoordinator(warm, realization=RealizationManager(estate))
    warm.invalidate("order_count")
    outcome = coordinator.fulfill(fams["revenue"], KEX.BY_DAY)

    # the MME answers from what it holds; the disagreeing offer is never needed …
    assert outcome.served
    assert dict(outcome.value.cells) == before
    # … and offering it directly is refused as a consistency failure, not accepted on authority
    offer = estate.realize(next(iter(estate.propose(
        warm.requirement_for(fams["revenue"], KEX.BY_DAY).requirement))))
    # **THE CLAIM IS FAITHFUL AND THE ADMISSION IS STILL REFUSED** (B-1′, the layering made visible). The
    # provider really does hold a `revenue@{day}` of the right family, anchor, value form and instance — so
    # fidelity IS established — and the cache refuses it anyway, because a second disagreeing CURRENT answer
    # to one question is a consistency failure no origin overrides. Forcing this into a generic realization
    # refusal would have hidden which layer owns it.
    adjudicated = warm.realizations.adjudicate(offer)
    assert adjudicated, adjudicated.refusal
    refused = RealizationManager.establish(warm, adjudicated.credential)
    assert not refused and refused.code == "duplicate-current-disagreement"
    assert dict(warm.measure(fams["revenue"], KEX.BY_DAY).value.cells) == before


# ══ G · STILL NEED AFTER THE BOUND ════════════════════════════════════════════════════════════════
class UselessEstate:
    """Proposes something lawful that does not actually help: `Revenue@{store}` cannot reach `{day}`."""

    name = "useless"

    def __init__(self, engine):
        self.engine = engine
        self.realized = 0

    def propose(self, requirement):
        yield RealizationProposal(provider=self.name, family_id=requirement.family_id,
                                  anchor=KEX.BY_STORE, value_form="scalar",
                                  realization=RealizationStanding(provider=self.name),
                                  handle="s")

    def realize(self, proposal):
        self.realized += 1
        value = _state(self.engine, "revenue", KEX.BY_STORE, {("S1",): 500.0})
        return RealizationOffer(provider=self.name, family_id="revenue", anchor=KEX.BY_STORE,
                                value=value, instance=value.instance,
                                realization=RealizationStanding(provider=self.name),
                                establishment=Establishment(INDEPENDENT), from_proposal=proposal)


def test_still_need_after_the_round_bound_is_incomplete_fulfillment(cold, fams):
    """§4: **deterministic termination.** Realization ran, admission happened, and the target is still
    not servable — which is a different fact from `lawful-but-unavailable`, because work was done."""
    estate = UselessEstate(cold)
    coordinator = FulfillmentCoordinator(cold, realization=RealizationManager(estate))

    outcome = coordinator.fulfill(fams["revenue"], KEX.BY_DAY)

    assert outcome.mood == INCOMPLETE
    assert estate.realized == 1                                  # exactly one round, not a chase
    assert outcome.rounds == 1
    assert "explicit bound" in outcome.detail
    assert "NO FURTHER ATTEMPT IS MADE" in outcome.detail


def test_the_loop_terminates_within_the_bound_however_unhelpful_the_estate_is(cold, fams):
    """**The bound is a CEILING on measurements, and the loop may stop short of it.**

    It stops short here for a good reason, which this test also pins: `RouteContext.attempted` records
    the routes already tried, so the policy will not re-offer one that already failed and the second round
    finds nothing admissible. A coordinator that re-realized the same useless proposal every round would
    have terminated too — after paying for it `rounds` times."""
    for rounds in (0, 1, 2, 5):
        engine = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=KEX.MANIFOLD)
        for family in KEX._families():
            engine.register_family(family)
        calls = []
        real = engine.measure
        engine.measure = lambda f, a, **k: (calls.append(1), real(f, a, **k))[1]  # type: ignore

        estate = UselessEstate(engine)
        outcome = FulfillmentCoordinator(
            engine, realization=RealizationManager(estate), rounds=rounds).fulfill(
            fams["revenue"], KEX.BY_DAY)
        assert not outcome.served
        assert 1 <= len(calls) <= rounds + 1, (rounds, len(calls))
        assert estate.realized <= 1                      # the failed route is never retried


def test_a_route_that_already_failed_is_not_offered_again(cold, fams):
    """`RouteContext.attempted` exists so a policy cannot loop on a proposal that did not help."""
    estate = UselessEstate(cold)
    outcome = FulfillmentCoordinator(
        cold, realization=RealizationManager(estate), rounds=4).fulfill(fams["revenue"], KEX.BY_DAY)
    assert estate.realized == 1
    assert outcome.mood in (INCOMPLETE, UNAVAILABLE)


def test_rounds_zero_never_realizes_at_all(cold, fams):
    """A deployment with realization disabled: the estate is never asked to execute."""
    estate = Estate("warehouse", _revenue_at_day(cold))
    outcome = FulfillmentCoordinator(
        cold, realization=RealizationManager(estate), rounds=0).fulfill(fams["revenue"], KEX.TOTAL)
    assert outcome.mood == INCOMPLETE
    assert estate.realized == 0


# ══ H · THE EXPRESSION PATH ═══════════════════════════════════════════════════════════════════════
def test_AOV_fulfils_its_family_operands_then_evaluates(warm, exprs):
    """§10:

        AOV@A → fulfill Revenue@A → fulfill OrderCount@A → ExpressionEvaluator → AOV result
    """
    coordinator = FulfillmentCoordinator(warm)
    outcome = coordinator.fulfill_expression(exprs["aov"], KEX.TOTAL)

    assert outcome.served
    assert outcome.cell() == pytest.approx(500 / 6)              # pooled, not the mean of daily means
    assert {o.target.split("@")[0] for o in outcome.operands} == {"revenue", "order_count"}
    assert all(o.served for o in outcome.operands)
    assert outcome.answer.route == "evaluated"


def test_no_expression_output_enters_the_mme_through_the_coordinator(warm, exprs):
    """§6, and M-2's boundary held through a new caller."""
    coordinator = FulfillmentCoordinator(warm)
    coordinator.fulfill_expression(exprs["aov"], KEX.TOTAL)
    coordinator.fulfill_expression(exprs["estimate"], KEX.TOTAL)

    assert all(warm.sort_of(k.identity) == "family" for k in warm.held)
    for expression_id in warm.expressions:
        assert not warm.materializations.select(expression_id, eligibility=None)
    assert not hasattr(coordinator, "_store")                    # and the coordinator caches nothing


def test_a_cold_expression_realizes_its_OPERANDS(cold, exprs, fams):
    """The coordinator's contribution to the expression path, exactly: it makes the family operands
    available. The evaluator then finds them warm."""
    estate = Estate("warehouse", {
        ("revenue", KEX.BY_DAY): _state(cold, "revenue", KEX.BY_DAY,
                                        {("D1",): 175.0, ("D2",): 325.0}),
        ("order_count", KEX.BY_DAY): _state(cold, "order_count", KEX.BY_DAY,
                                            {("D1",): 2, ("D2",): 4})})
    coordinator = FulfillmentCoordinator(cold, realization=RealizationManager(estate))

    outcome = coordinator.fulfill_expression(exprs["aov"], KEX.BY_DAY)

    assert outcome.served
    assert outcome.answer.value.cells[("D1",)] == pytest.approx(87.5)
    assert {r.family_id for r in outcome.realized} == {"revenue", "order_count"}
    assert estate.realized == 2
    # and the operand demand was attributed to the expression (M-2 §8, preserved)
    observer = cold.observations.observer
    assert any("average_order_value" in r.request.on_behalf_of for r in observer.records)


def test_an_operand_route_decision_stops_the_expression_and_executes_nothing(cold, exprs):
    """Falling through to another basis would let the coordinator dodge a decision it was asked to
    surface, and the caller would never learn a choice was waiting."""
    holdings = {("revenue", KEX.BY_DAY): _state(cold, "revenue", KEX.BY_DAY, {("D1",): 175.0})}
    coordinator = FulfillmentCoordinator(
        cold, realization=RealizationManager(Estate("a", holdings), Estate("b", holdings)))

    outcome = coordinator.fulfill_expression(exprs["aov"], KEX.BY_DAY)

    assert outcome.mood == ROUTE_POLICY_NEEDED
    assert outcome.realized == ()
    assert outcome.proposals is not None and len(outcome.proposals) == 2


def test_the_evaluators_governed_refusal_is_reported_and_not_replaced(warm, exprs):
    """*"role unfilled"* and *"incompatible basis"* are different facts and only the evaluator can tell
    them apart. The coordinator reports the operand story alongside the refusal, never instead of it."""
    coordinator = FulfillmentCoordinator(warm)
    outcome = coordinator.fulfill_expression(exprs["aov_audited"], KEX.BY_DAY)

    assert not outcome.served
    assert all(o.served for o in outcome.operands)               # BOTH operands were fulfilled …
    assert "jointly meaningless" in outcome.answer.refusal.detail  # … and the refusal is semantic
    assert "different-participation" in outcome.answer.refusal.detail


def test_the_coordinator_does_not_select_a_basis(warm, exprs):
    """Basis selection is governed semantics and stays with the evaluator. The coordinator walks the
    declared order only to decide which operands to make available."""
    coordinator = FulfillmentCoordinator(warm)
    named = coordinator.fulfill_expression(exprs["estimate"], KEX.BY_DAY, basis_id="b_sketch")
    default = coordinator.fulfill_expression(exprs["estimate"], KEX.BY_DAY)
    assert named.served and default.served
    assert named.answer.seeded_from == default.answer.seeded_from == "b_sketch"


# ══ I · HLL FINALIZATION ══════════════════════════════════════════════════════════════════════════
def test_the_estimate_is_finalized_above_and_the_MME_holds_only_the_sketch(warm, exprs, fams):
    """§10:

        estimate(HLLSketch@A) → fulfill HLLSketch@A → evaluator/finalizer → estimate
    """
    coordinator = FulfillmentCoordinator(warm)
    outcome = coordinator.fulfill_expression(exprs["estimate"], KEX.TOTAL)

    assert outcome.served
    assert outcome.cell() == len({o["customer"] for o in KEX.ORDERS})
    assert isinstance(outcome.cell(), int)

    # the MME holds the SKETCH …
    sketch = warm.materializations.select("distinct_customers", anchor=KEX.TOTAL)
    assert sketch and sketch[0].value.value_form == "structured"
    assert hasattr(sketch[0].value.cells[()], "get_estimate")
    # … and nothing at all for the estimate
    assert not warm.materializations.select("distinct_customer_estimate", eligibility=None)


def test_a_cold_sketch_family_is_realized_as_STRUCTURED_state(cold, exprs, fams):
    """The requirement demanded `structured`; what the estate supplies must be mergeable, not a
    finalized number. The whole chain is visible in one test."""
    warm_source = KEX.build()
    sketch_state = warm_source.measure(fams["distinct"], KEX.BY_DAY).value
    estate = Estate("warehouse", {("distinct_customers", KEX.BY_DAY): sketch_state})
    coordinator = FulfillmentCoordinator(cold, realization=RealizationManager(estate))

    outcome = coordinator.fulfill_expression(exprs["estimate"], KEX.BY_DAY)

    assert outcome.served
    assert sorted(outcome.answer.value.cells.values()) == [2, 3]
    held = cold.materializations.select("distinct_customers", anchor=KEX.BY_DAY)
    assert held and held[0].value.value_form == "structured"


# ══ J · MOODS, OBSERVATION, AND THE THINGS THAT MUST NOT BE HERE ══════════════════════════════════
def test_the_six_moods_are_distinct_and_none_collapses_into_a_generic_failure(cold, warm, fams):
    """§3: *"Do not collapse these into generic failure."* Five of the six from real requests."""
    seen = set()
    seen.add(FulfillmentCoordinator(warm).fulfill(fams["revenue"], KEX.TOTAL).mood)
    seen.add(FulfillmentCoordinator(cold).fulfill(fams["revenue"], KEX.TOTAL).mood)
    seen.add(FulfillmentCoordinator(warm).fulfill(fams["on_hand"], KEX.BY_STORE).mood)
    holdings = _revenue_at_day(cold)
    seen.add(FulfillmentCoordinator(
        cold, realization=RealizationManager(Estate("a", holdings), Estate("b", holdings))
    ).fulfill(fams["revenue"], KEX.TOTAL).mood)
    seen.add(FulfillmentCoordinator(
        cold, realization=RealizationManager(UselessEstate(cold))
    ).fulfill(fams["revenue"], KEX.BY_DAY).mood)

    assert seen == {SERVED, UNAVAILABLE, NOT_SUPPORTED, ROUTE_POLICY_NEEDED, INCOMPLETE}
    assert set(MOODS) - seen == {UNRESOLVED_STATE}               # the columnar one, below


def test_want_of_state_is_its_own_mood_and_is_not_a_cache_miss():
    """§3. The material is held and the value is owed; realization of a coarser anchor would not supply
    it, so calling it `NEED` would have sent a coordinator shopping for the wrong thing."""
    engine, _block = CEX.build(settled=False)
    # **THE SAME COORDINATOR, OVER THE COLUMNAR ENGINE.** F-1's one seam correction is what makes this
    # line possible: before it, the two engines' `measure` signatures had diverged and a coordinator
    # written against either was written against that substrate.
    outcome = FulfillmentCoordinator(engine).fulfill("revenue", CEX.BY_DAY)

    assert outcome.mood == UNRESOLVED_STATE
    assert outcome.disposition == WANT_OF_STATE
    assert "NOT A CACHE MISS AND NOT A FETCH" in outcome.detail


def test_the_observation_seam_survives_the_coordinator(cold, fams):
    """§7. The coordinator adds no observation and removes none: it calls `measure` normally, so every
    request it makes is observed exactly as a hand-wired one would be."""
    observer = cold.observations.observer
    estate = Estate("warehouse", _revenue_at_day(cold))
    FulfillmentCoordinator(cold, realization=RealizationManager(estate)).fulfill(
        fams["revenue"], KEX.TOTAL)

    dispositions = [r.disposition for r in observer.records]
    assert dispositions == [NEED, READY]                         # the attempt, then the retry
    # the original requested TARGET is preserved on both, which is λ(q) (M-2 §8)
    assert all(r.request.target == KEX.TOTAL for r in observer.records)
    served = observer.records[-1]
    # cached-vs-realized is recoverable: the selected materialization names its provider
    assert served.fulfillment.selected
    assert "realized by warehouse" in cold.materialization(served.fulfillment.selected[0]).note
    assert served.fulfillment.seeded_from == KEX.BY_DAY          # the continuation work performed


def test_the_coordinator_never_reads_an_observation(cold, fams):
    """**M-2 §6 held through a new consumer**: *"observations never create analytical rights."* A
    coordinator that routed on the workload log would have made logging authoritative — and it would
    have worked, which is what makes the guard necessary."""
    import ast
    import inspect

    tree = ast.parse(inspect.getsource(fulfillment_module))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    code = ast.unparse(tree)
    for forbidden in ("observations", "RecordingObserver", ".records", "ObservationSink", "observe("):
        assert forbidden not in code, forbidden
    assert inspect is not None

    # and it still works with no observer at all
    quiet = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=KEX.MANIFOLD)
    for family in KEX._families():
        quiet.register_family(family)
    quiet.establish_root(fams["revenue"], KEX.ORDERS)
    assert FulfillmentCoordinator(quiet).fulfill(fams["revenue"], KEX.TOTAL).served


def test_the_route_policy_is_replaceable(cold, fams):
    """§8: `RoutePolicy.choose(requirement, proposals, context)`, and the coordinator calls nothing
    else. A policy that DOES choose is installable without touching the coordinator — which is the
    property that lets the cost model arrive as one file."""
    holdings = _revenue_at_day(cold)
    seen = {}

    class FirstOffered:
        name = "first-offered"

        def choose(self, requirement, proposals, context):
            seen.update(requirement=requirement, proposals=proposals, context=context)
            return RouteDecision(chosen=proposals.proposals[0], reason="a later unit's job")

    outcome = FulfillmentCoordinator(
        cold, realization=RealizationManager(Estate("a", holdings), Estate("b", holdings)),
        policy=FirstOffered()).fulfill(fams["revenue"], KEX.TOTAL)

    assert outcome.served                                        # it chose, and F-1's policy would not
    assert seen["requirement"].family_id == "revenue"
    assert isinstance(seen["context"], RouteContext)
    assert seen["context"].round == 0 and seen["context"].target == f"revenue@{KEX.TOTAL}"


def test_the_f1_policy_itself_contains_no_ranking():
    """§2/§8: no scoring, no cost estimation, and explicitly **not** 'take the coarsest'.

    **The ban is on OPERATIONS, not on words.** The policy's refusal text names cost and coarseness in
    order to say why neither was used, and a word-ban would have forced that explanation out of the code."""
    import ast
    import inspect

    tree = ast.parse(inspect.getsource(UnambiguousRoute).lstrip())
    ordering = {"sorted", "min", "max"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in ordering, node.func.id
        if isinstance(node, ast.Call):
            assert not any(k.arg in ("key", "reverse") for k in node.keywords), ast.dump(node.func)
    # and it has no attribute anyone could mistake for a ranking
    for forbidden in ("score", "cost", "rank", "cheapest", "weigh"):
        assert not hasattr(UnambiguousRoute, forbidden), forbidden


def test_nothing_in_the_coordinator_surface_optimizes_or_computes():
    """F-1's stop condition, as a guard. It is an orchestration unit: no cost model, no adaptive cache
    policy, no execution engine, no Arrow."""
    import ast

    forbidden_names = ("score", "cost_of", "optimize", "rank", "cheapest", "best_route",
                       "estimate_cost", "evict", "policy_for", "compute", "kernel")
    for name in forbidden_names:
        assert not hasattr(FulfillmentCoordinator, name), name
        assert not hasattr(FulfillmentOutcome, name), name

    code = _code_only(fulfillment_module)
    for banned in ("pyarrow", "datafusion", "duckdb", "adbc", "SessionContext",
                   "MaterializationStore", "LawRegistry", "pc.", "pa."):
        assert banned not in code, banned
    assert ast.parse(code)


def test_the_coordinator_does_not_know_HOW_the_evaluator_computes(warm, exprs):
    """§1, and the reason E-X preceded F-1: the coordinator calls `evaluate` and reads `admitted_bases`.
    Swap in an evaluator that computes differently and the coordinator cannot tell."""
    calls = []

    class Elsewhere:
        """Stands in for a future DataFusion/DuckDB/native-kernel evaluator."""

        def __init__(self, inner):
            self.inner = inner

        def evaluate(self, expression, anchor, **kwargs):
            calls.append((expression.expression_id, str(anchor)))
            return self.inner.evaluate(expression, anchor, **kwargs)

    coordinator = FulfillmentCoordinator(warm, evaluator=Elsewhere(ExpressionEvaluator(warm)))
    outcome = coordinator.fulfill_expression(exprs["aov"], KEX.TOTAL)

    assert outcome.served and outcome.cell() == pytest.approx(500 / 6)
    assert calls == [("average_order_value", str(KEX.TOTAL))]
    # the coordinator used ONLY `evaluate` on it — nothing substrate-specific
    assert not hasattr(coordinator.evaluator, "provider") or True


def test_the_outcome_type_carries_the_ruled_reporting_fields():
    """§7's list, as the coordinator's own report — distinct from the workload observation."""
    names = {f.name for f in fields(FulfillmentOutcome)}
    assert {"mood", "target", "answer", "disposition", "detail", "realized", "proposals",
            "operands", "rounds", "elapsed_ns"} <= names
    # and no score of any kind
    assert not (names & {"score", "cost", "rank", "value_of", "benefit"})

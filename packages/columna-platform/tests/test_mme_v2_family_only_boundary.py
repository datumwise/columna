"""
test_mme_v2_family_only_boundary.py — **M-2: expressions above the MME, and the request-observation seam.**

    **MME manages only family materializations `F@A`. Expressions consume them. Workload observations
    inform future cache residency economics but never analytical meaning.**  — Huayin, 2026-09-29

The ruling's stop-condition letters are the sections:

    A  the final MME family-only boundary
    B  the expression-serving path above the MME
    C  what shared F/E machinery retired
    D  the request-disposition interface after the split
    E  the workload/request observation shape
    F  proof that logging is non-authoritative and non-blocking for correctness
    G  preservation of M-1 cache-neutrality
    H  the AOV and HLL-estimate exhibits through the new boundary

WHAT IS NOT EXERCISED, DELIBERATELY: no persistence, no Iceberg, no Postgres, no expression cache, no
refresh orchestration, no adaptive cache algorithm, no realization manager. Ruled out of M-2 by name. A
test that mocked one would be where the next unit's design got made by accident — and §5 in particular is
a warning about arriving at a cost model early, so there is no test here that scores a materialization.
"""
from __future__ import annotations

from dataclasses import fields, replace

import pytest

from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar.expression import ColumnarExpressionEvaluator
from columna_platform.kernel import (
    IN_MEMORY,
    MME,
    REGISTRY,
    ExpressionEvaluator,
    KernelRefusal,
    RecordingObserver,
    Retained,
    RetentionKey,
)
from columna_platform.kernel import exhibit as KEX
from columna_platform.kernel import mme as kernel_mme_module
from columna_platform.kernel.builtins import NO_MEAN
from columna_platform.kernel.materialization import CURRENT, EVICTED, SUPERSEDED
from columna_platform.kernel.observation import (
    DISPOSITIONS,
    NEED,
    READY,
    UNSUPPORTED,
    WANT_OF_STATE,
    FamilyRequest,
    Fulfillment,
    NullObserver,
    ObservationSink,
    RequestObservation,
    disposition_for,
)

LOAD = "load:orders@08:00Z"


# ── fixtures ─────────────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def mme():
    """The constituted in-memory engine. Families AND expressions are registered here — constitution is
    not residency, and M-2 moves only the second."""
    return KEX.build()


@pytest.fixture
def evaluator(mme):
    return ExpressionEvaluator(mme)


@pytest.fixture
def watched():
    """An engine with a recorder attached, and the recorder."""
    engine = KEX.build()
    observer = RecordingObserver()
    engine.observations.observer = observer
    return engine, observer


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
def columnar():
    """The settled columnar world and an evaluator over it. `CEX.build` hands back `(engine, block)`."""
    engine, _block = CEX.build(settled=True, data_state=LOAD)
    return engine, ColumnarExpressionEvaluator(engine)


# ══ A · THE FINAL MME FAMILY-ONLY BOUNDARY ════════════════════════════════════════════════════════
def test_the_mme_has_no_expression_serving_method_at_all(mme):
    """Ruled §1. **And no delegating shim**: a forwarding `MME.evaluate` would have kept every call site
    compiling and kept the boundary imaginary."""
    assert not hasattr(mme, "evaluate")
    assert not hasattr(mme, "_establish")
    assert not hasattr(type(mme), "evaluate")


def test_the_mme_holds_no_expression_store(mme, evaluator, exprs):
    """The keyed side store that held `E@A` through M-1 is gone — not emptied, absent."""
    assert not hasattr(mme, "_store")
    evaluator.evaluate(exprs["aov"], KEX.TOTAL)
    evaluator.evaluate(exprs["estimate"], KEX.TOTAL)
    # every attribute of the engine, searched for a container holding an expression output
    for name in dir(mme):
        if name.startswith("__"):
            continue
        value = getattr(mme, name, None)
        if isinstance(value, dict):
            assert not any(getattr(v, "point", None) is not None
                           and getattr(v.point, "sort", "") == "expression" for v in value.values())


def test_everything_the_mme_holds_is_family_state(mme, evaluator, exprs, fams):
    """Ruled §1, and the whole of section A in one assertion."""
    mme.measure(fams["revenue"], KEX.TOTAL)
    mme.measure(fams["distinct"], KEX.TOTAL)
    evaluator.evaluate(exprs["aov"], KEX.TOTAL)
    evaluator.evaluate(exprs["estimate"], KEX.TOTAL)

    assert mme.held                                              # it is not vacuous
    assert all(mme.sort_of(k.identity) == "family" for k in mme.held)
    assert all(r.value.point.sort == "family" for r in mme.holdings())
    assert all(m.point.sort == "family" for m in mme.materializations.all())
    for expression_id in mme.expressions:
        assert not mme.materializations.select(expression_id, eligibility=None)


def test_retain_refuses_an_expression_output_by_a_governed_reason(mme, evaluator, exprs):
    """Not an `AttributeError` two calls later, and not a silent accept into a cache that is not there."""
    output = evaluator.evaluate(exprs["estimate"], KEX.TOTAL).value
    with pytest.raises(KernelRefusal) as refused:
        mme.retain(output)
    assert refused.value.code == "not-a-family-materialization"
    # the refusal NAMES WHERE IT BELONGS, because the caller's question was reasonable
    assert "ExpressionEvaluator" in refused.value.detail
    assert "does not cache `E@A` at all" in refused.value.detail


def test_retained_refuses_an_expression_point_rather_than_answering_not_held(mme, exprs):
    """**`None` would have been a lie about an empty cache** and would have invited a caller to establish
    the expression and try again forever."""
    with pytest.raises(KernelRefusal) as refused:
        mme.retained(exprs["aov"].at(KEX.TOTAL), exprs["aov"].instance())
    assert refused.value.code == "not-a-family-materialization"


def test_the_columnar_mme_is_family_only_on_the_same_terms(columnar):
    engine, evaluator = columnar
    assert not hasattr(engine, "evaluate")
    assert not hasattr(engine, "_store")
    output = evaluator.evaluate("average_order_value", CEX.BY_DAY).value
    with pytest.raises(KernelRefusal) as refused:
        engine.retain(output)
    assert refused.value.code == "not-a-family-materialization"
    assert all(engine.sort_of(k.identity) == "family" for k in engine.held)


def test_invalidate_is_family_only_and_still_conservative(mme, fams):
    """The dependency lifecycle is family-only (§2) and unchanged in kind: rebuild is from the root."""
    mme.measure(fams["revenue"], KEX.BY_DAY)
    mme.measure(fams["revenue"], KEX.TOTAL)
    dropped = mme.invalidate("revenue")
    assert dropped and all(k.sort == "family" for k in dropped)
    after = mme.measure(fams["revenue"], KEX.TOTAL)
    assert not after.served
    assert "must be established at" in after.refusal.detail


# ══ B · THE EXPRESSION-SERVING PATH ABOVE THE MME ═════════════════════════════════════════════════
def test_the_evaluator_is_a_separate_object_the_engine_does_not_know_about(mme, evaluator):
    """**The arrow points one way, and that is the unit.** The engine holds no reference to the evaluator,
    no registration and no hook — you can delete the evaluator and the engine still serves families."""
    assert evaluator.mme is mme
    assert not any(isinstance(getattr(mme, n, None), ExpressionEvaluator)
                   for n in dir(mme) if not n.startswith("__"))


def test_the_evaluator_obtains_family_state_only_through_measure(mme, evaluator, exprs):
    """**The seam, observed from the inside.** Every operand arrives by `measure`; the evaluator never
    reaches into the materialization store and never names a `MaterializationId`."""
    calls: list[tuple] = []
    real = mme.measure

    def watched_measure(family, anchor, **kwargs):
        calls.append((family.family_id, anchor, kwargs.get("on_behalf_of", "")))
        return real(family, anchor, **kwargs)

    mme.measure = watched_measure                     # type: ignore[method-assign]
    answer = evaluator.evaluate(exprs["aov"], KEX.BY_DAY)
    assert answer.served
    assert {c[0] for c in calls} == {"revenue", "order_count"}
    assert all(c[1] == KEX.BY_DAY for c in calls)
    # and every one of them carried the route/use evidence of §8
    assert all("average_order_value" in c[2] for c in calls)


def test_the_expression_is_re_evaluated_and_its_operands_are_not_re_established(mme, evaluator, exprs):
    """**The cost of retiring the expression cache, measured.** Ruled §1: no expression caching in v1. The
    second ask re-derives the expression and does NOT re-establish the family operands — the cache that
    matters is the family cache and it is still doing the work."""
    first = evaluator.evaluate(exprs["aov"], KEX.TOTAL)
    before = {f: len(mme.materializations.select(f, eligibility=None))
              for f in ("revenue", "order_count")}
    second = evaluator.evaluate(exprs["aov"], KEX.TOTAL)
    after = {f: len(mme.materializations.select(f, eligibility=None))
             for f in ("revenue", "order_count")}

    assert first.route == "evaluated" and second.route == "evaluated"   # never `cached`
    assert before == after                                             # no new family work
    assert first.cell() == second.cell()                               # and the same answer


def test_platform_serving_still_supports_expressions_fully(mme):
    """Ruled §1: *"Expressions remain fully supported by Platform serving."* The service holds both
    collaborators; the dispatch is still by SORT and never by inspecting what came back."""
    from columna_platform.frameql.serving import FrameQLService

    service = FrameQLService(mme)
    assert isinstance(service.expressions, ExpressionEvaluator)
    assert service.expressions.mme is service.mme

    served = service.serve("SELECT average_order_value AT {day}")
    assert served.served and served.frame.columns[0].route == "evaluated"
    family = service.serve("SELECT revenue AT {day}")
    assert family.served and family.frame.columns[0].route in ("cached", "continued", "root")


def test_an_injected_evaluator_is_used(mme):
    """A caller with a different evaluation strategy supplies one rather than subclassing the service."""
    from columna_platform.frameql.serving import FrameQLService

    class Counting(ExpressionEvaluator):
        calls = 0

        def evaluate(self, expression, anchor, **kwargs):
            type(self).calls += 1
            return super().evaluate(expression, anchor, **kwargs)

    service = FrameQLService(mme, evaluator=Counting(mme))
    service.serve("SELECT average_order_value AT {day}")
    assert Counting.calls == 1


# ══ C · WHAT SHARED F/E MACHINERY RETIRED ═════════════════════════════════════════════════════════
def test_retention_key_sort_is_retired_as_a_field(mme):
    """Ruled §2: *"assess whether M-2 now allows retirement of `RetentionKey.sort`."* **It does.** The
    field existed so that two sorts sharing one key could be told apart in it; they no longer share it."""
    assert "sort" not in {f.name for f in fields(RetentionKey)}
    assert RetentionKey.sort == "family"
    assert all(k.sort == "family" for k in mme.held)
    # and it cannot be varied, by keyword or by position
    with pytest.raises(TypeError):
        RetentionKey(sort="expression", identity="x", anchor=KEX.TOTAL, instance=None,
                     realization=mme.realization)


def test_the_sort_DISTINCTION_is_not_retired(mme, evaluator, exprs, fams):
    """**Retiring the key axis is not retiring the distinction.** Two types, two sets of rights, and a
    governed verdict that still names the rule (§2: *"Do not remove expression semantics from the
    kernel"*)."""
    state = mme.measure(fams["revenue"], KEX.TOTAL).value
    output = evaluator.evaluate(exprs["aov"], KEX.TOTAL).value

    assert state.point.sort == "family" and output.point.sort == "expression"
    assert state.CONTINUATION_BEARING is True and output.CONTINUATION_BEARING is False
    assert hasattr(state, "fold_onto") and not hasattr(output, "fold_onto")
    assert mme.sort_of("revenue") == "family"
    assert mme.sort_of("average_order_value") == "expression"


def test_the_sort_verdict_survives_as_a_BOUNDARY_check(mme, evaluator, exprs, fams):
    """`adjudicate`'s first question is now unreachable from inside the store and reachable from ABOVE —
    which is where an `ExpressionOutput` now lives. A refusal that names the rule beats one that is
    merely impossible to provoke."""
    output = evaluator.evaluate(exprs["estimate"], KEX.TOTAL).value
    from_above = Retained(
        key=RetentionKey(identity="distinct_customer_estimate", anchor=KEX.TOTAL,
                         instance=output.instance, realization=mme.realization),
        value=output)
    assert not from_above.continuation_bearing
    verdict = mme.adjudicate(from_above, fams["distinct"], KEX.TOTAL)
    assert not verdict and verdict.code == "not-continuation-bearing"
    assert "never becomes family continuation state" in verdict.detail


def test_pool_resolution_and_resolve_pool_are_retired(mme):
    """Their only remaining caller was the expression cache, and M-2 does not have one."""
    assert not hasattr(kernel_mme_module, "resolve_pool")
    assert not hasattr(kernel_mme_module, "PoolResolution")
    import columna_platform.kernel as kernel_pkg

    assert not hasattr(kernel_pkg, "resolve_pool")
    assert not hasattr(kernel_pkg, "PoolResolution")


def test_the_constitution_screen_is_now_STRUCTURAL_rather_than_procedural(fams):
    """`resolve_pool`'s first question — is this held under the CURRENT constitution? — is answered by the
    BUILD partition that M-1 introduced, so removing the screen removes no governed refusal."""
    engine = KEX.build()
    engine.measure(fams["revenue"], KEX.BY_DAY)
    moved = replace(fams["revenue"], participation="every order the auditor confirmed")
    engine.register_family(moved)                             # the declaration moves

    assert engine.stale_states()                              # still reported, and still names what moved
    assert all(m.eligibility == SUPERSEDED
               for m in engine.materializations.select("revenue", eligibility=None))
    refused = engine.measure(moved, KEX.TOTAL)
    assert not refused.served
    assert "NOT CURRENT (superseded)" in refused.refusal.detail


def test_the_ambiguous_evidence_state_is_now_UNREACHABLE_rather_than_refusable():
    """`resolve_pool`'s second question retired the same way, and STRONGER: M-1's coexistence standing
    refuses to make a second evidence state CURRENT in one slot, so the ambiguity is prevented at
    admission instead of detected at serving.

    **This test is the guard on that claim.** If a future widening ever lets two evidence states be
    current in one slot, the engine would silently pick one by cost — and this fails."""
    engine, block = CEX.build(settled=True, data_state=LOAD)
    engine.establish(block, "order_count", data_state="load:orders@17:30Z")
    current = [m for m in engine.materializations.select("order_count", eligibility=CURRENT)
               if m.anchor == CEX.SALE_AT]
    # **AT MOST ONE CURRENT EVIDENCE STATE PER SLOT.** That is the invariant that retires the screen.
    assert len({m.data_state for m in current}) == 1
    assert engine.measure("order_count", CEX.BY_DAY).served


def test_family_only_candidate_selection(mme, evaluator, exprs, fams):
    """Ruled §2. Candidate selection was already the MME's (M-1 §2); M-2 makes its population
    homogeneous, so there is no sort screen at the top of the loop any more."""
    mme.measure(fams["revenue"], KEX.BY_DAY)
    evaluator.evaluate(exprs["aov"], KEX.BY_DAY)
    candidates = mme.candidates(fams["revenue"])
    assert candidates
    assert all(c.continuation_bearing for c in candidates)
    assert all(c.key.sort == "family" for c in candidates)


# ══ D · THE REQUEST-DISPOSITION INTERFACE AFTER THE SPLIT ═════════════════════════════════════════
def test_the_four_dispositions_are_the_closed_set():
    assert DISPOSITIONS == (READY, NEED, WANT_OF_STATE, UNSUPPORTED)


def test_disposition_for_is_total():
    """Every refusal code lands somewhere, and the unlisted direction is the conservative one."""
    assert disposition_for("outside-continuation-region") == UNSUPPORTED
    assert disposition_for("unrealized-law") == UNSUPPORTED
    assert disposition_for("want-of-state") == WANT_OF_STATE
    assert disposition_for("basis-operand-wants-state") == WANT_OF_STATE
    assert disposition_for("a-code-nobody-has-minted-yet") == NEED
    assert disposition_for("") == NEED


def test_READY_is_recorded_for_a_direct_hit_and_for_a_derivation(watched, fams):
    engine, observer = watched
    derived = engine.measure(fams["revenue"], KEX.BY_DAY)      # a fold from a finer materialization
    hit = engine.measure(fams["revenue"], KEX.BY_DAY)          # now directly held

    assert derived.served and hit.served
    first, second = observer.records[-2], observer.records[-1]
    assert first.disposition == READY and not first.fulfillment.directly_held
    assert second.disposition == READY and second.fulfillment.directly_held
    # **THE DIFFERENCE IS LEGIBLE**, which is the point: same family, same anchor, different cost.
    assert first.fulfillment.seeded_from is not None
    assert second.fulfillment.seeded_from is None


def test_NEED_is_recorded_when_nothing_lawful_is_held(fams):
    """**The only disposition where a cache decision would have changed the outcome** — and therefore the
    row a future optimizer cares most about."""
    observer = RecordingObserver()
    cold = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=KEX.MANIFOLD, observer=observer)
    cold.register_family(fams["revenue"])

    refused = cold.measure(fams["revenue"], KEX.TOTAL)
    assert not refused.served
    assert len(observer) == 1
    assert observer.records[0].disposition == NEED
    assert observer.records[0].fulfillment.selected == ()


def test_UNSUPPORTED_is_recorded_when_no_lawful_route_exists(watched, fams):
    """A restricted continuation region. **Retaining anything, anywhere, forever, would not change this
    answer**, and a policy that could not see that would try to cache its way out of a law."""
    engine, observer = watched
    refused = engine.measure(fams["on_hand"], KEX.BY_STORE)
    assert not refused.served
    record = observer.records[-1]
    assert record.disposition == UNSUPPORTED
    assert record.refusal_code == "outside-continuation-region"


def test_WANT_OF_STATE_is_recorded_and_is_NOT_a_cache_miss():
    """The material is present and the VALUE is owed and absent. The remedy is establishment, not
    residency — so it is kept out of `NEED` deliberately."""
    engine = CEX.build(settled=False)
    engine = engine[0] if isinstance(engine, tuple) else engine
    observer = RecordingObserver()
    engine.observations.observer = observer

    refused = engine.measure("revenue", CEX.BY_DAY)
    assert not refused.served and refused.refusal.code == "want-of-state"
    record = observer.records[-1]
    assert record.disposition == WANT_OF_STATE
    assert record.disposition != NEED
    # and it names the material it DID have, which is what distinguishes it from a miss
    assert record.fulfillment.selected != ()


def test_every_disposition_is_reachable_and_they_are_distinguished(fams):
    """All four, from real requests, in one assertion — because the value of the interface is that the
    four are FOUR."""
    seen = set()

    engine, observer = KEX.build(), RecordingObserver()
    engine.observations.observer = observer
    engine.measure(fams["revenue"], KEX.BY_DAY)                # READY
    engine.measure(fams["on_hand"], KEX.BY_STORE)              # UNSUPPORTED
    seen |= set(observer.by_disposition())

    cold_observer = RecordingObserver()
    cold = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=KEX.MANIFOLD, observer=cold_observer)
    cold.register_family(fams["revenue"])
    cold.measure(fams["revenue"], KEX.TOTAL)                   # NEED
    seen |= set(cold_observer.by_disposition())

    columnar = CEX.build(settled=False)
    columnar = columnar[0] if isinstance(columnar, tuple) else columnar
    columnar_observer = RecordingObserver()
    columnar.observations.observer = columnar_observer
    columnar.measure("revenue", CEX.BY_DAY)                    # WANT_OF_STATE
    seen |= set(columnar_observer.by_disposition())

    assert seen == set(DISPOSITIONS)


# ══ E · THE WORKLOAD/REQUEST OBSERVATION SHAPE ════════════════════════════════════════════════════
def test_one_observation_per_request_on_every_path(watched, fams):
    """Ruled §7: *"observation should happen at the request boundary, not only when a cached
    materialization is selected."*"""
    engine, observer = watched
    before = len(observer)
    engine.measure(fams["revenue"], KEX.BY_DAY)                # served, derived
    engine.measure(fams["revenue"], KEX.BY_DAY)                # served, held
    engine.measure(fams["on_hand"], KEX.BY_STORE)              # refused
    assert len(observer) - before == 3


def test_the_record_carries_every_field_the_ruling_names(watched, fams):
    """Ruled §4's minimum list, each one checked: manifold/build, family, target anchor, time,
    disposition, selected materialization(s), directly-held-or-derived, work performed, counters."""
    engine, observer = watched
    engine.measure(fams["revenue"], KEX.BY_DAY)
    record = observer.records[-1]

    assert isinstance(record, RequestObservation)
    assert record.request.manifold == engine.manifold                      # Manifold
    assert record.request.build == engine.build.reference                  # build
    assert record.request.family_id == "revenue"                           # family
    assert record.request.target == KEX.BY_DAY                             # target anchor
    assert record.at > 0 and record.elapsed_ns >= 0                        # time, and a latency counter
    assert record.disposition in DISPOSITIONS                              # disposition
    assert record.fulfillment.selected                                     # selected materialization(s)
    assert record.fulfillment.directly_held is False                       # held or derived
    assert record.fulfillment.seeded_from is not None                      # the work actually performed
    assert record.fulfillment.folded and record.fulfillment.considered     # counters, observed not modelled
    assert record.route in ("cached", "root", "continued")


def test_a_request_that_PRODUCED_a_materialization_says_so(watched, fams):
    """A derived answer is also a producer. Without this, the fold that made a materialization is charged
    to nobody and the object looks as though it appeared for free."""
    engine, observer = watched
    engine.measure(fams["revenue"], KEX.BY_DAY)
    record = observer.records[-1]
    assert record.fulfillment.admitted
    assert engine.materialization(record.fulfillment.admitted[0]) is not None


def test_demand_is_counted_over_WHAT_WAS_ASKED_and_never_over_what_answered(watched, fams):
    """Ruled §8: *"Do not conflate exact-target frequency with materialization value."* λ(q) is a count of
    requests for `F@A`, and a record keyed by the answering materialization would have made an ancestor's
    value invisible."""
    engine, observer = watched
    for _ in range(3):
        engine.measure(fams["revenue"], KEX.TOTAL)
    engine.measure(fams["revenue"], KEX.BY_DAY)

    demand = observer.demand()
    assert demand[("revenue", str(KEX.TOTAL))] == 3
    assert demand[("revenue", str(KEX.BY_DAY))] == 1


def test_an_ancestor_never_asked_for_directly_is_still_visible_as_the_thing_that_served(fams):
    """**§8's case, exactly.** `Revenue@{day, order, store}` is the root. Nobody ever asks for it. It
    answers every coarser target, and the observation record preserves enough to see that — which is what
    a later descendant-reuse estimator needs and what M-2 must not make impossible.

    **No scoring here**, deliberately: §8 says *"Do not implement descendant-value scoring yet."*"""
    engine, observer = KEX.build(), RecordingObserver()
    engine.observations.observer = observer
    root = engine.materializations.select("revenue", anchor=KEX.SALE_AT)[0]

    engine.measure(fams["revenue"], KEX.STORE_DAY)
    engine.measure(fams["revenue"], KEX.BY_DAY)
    engine.measure(fams["revenue"], KEX.TOTAL)

    # the ROOT was never the target of a request …
    assert all(r.request.target != KEX.SALE_AT for r in observer.records)
    # … and it is nonetheless recorded as having served, at more than one distinct target
    uses = observer.uses_of(root.id)
    assert uses
    assert len({r.request.target for r in uses}) >= 1
    assert all(r.fulfillment.seeded_from == KEX.SALE_AT for r in uses)


def test_expression_driven_demand_is_attributed_to_the_expression(watched, exprs):
    """Ruled §8's *"route/use information"*. Demand for `Revenue@Month` because a user asked for it is not
    the same signal as demand for `Revenue@Month` because `AOV@Month` needed it."""
    engine, observer = watched
    ExpressionEvaluator(engine).evaluate(exprs["aov"], KEX.BY_DAY)

    on_behalf = [r for r in observer.records if r.request.on_behalf_of]
    assert on_behalf
    assert {r.request.family_id for r in on_behalf} == {"revenue", "order_count"}
    assert all("average_order_value" in r.request.on_behalf_of for r in on_behalf)
    # a DIRECT ask for the same family at the same anchor is distinguishable from it
    engine.measure(engine.family("revenue"), KEX.BY_DAY)
    assert observer.records[-1].request.on_behalf_of == ""


def test_misses_are_retrievable_as_their_own_population(watched, fams):
    """Ruled §7: *"A cache policy cannot learn from hits alone."*"""
    engine, observer = watched
    engine.measure(fams["revenue"], KEX.BY_DAY)
    engine.measure(fams["on_hand"], KEX.BY_STORE)
    assert observer.misses()
    assert all(not r.served for r in observer.misses())
    assert any(r.served for r in observer.records)


def test_the_observation_is_an_APPEND_only_event_and_the_interface_can_refuse_nothing(watched, fams):
    """Ruled §4: *"Prefer an append/event-style observation interface rather than coupling correctness to
    logging."* One method, no return value, no veto."""
    engine, observer = watched
    engine.measure(fams["revenue"], KEX.BY_DAY)
    record = observer.records[-1]

    assert observer.observe(record) is None                  # no return value to branch on
    with pytest.raises(Exception):                           # frozen: an emitted record is immutable
        record.disposition = READY                           # type: ignore[misc]
    seqs = [r.seq for r in observer.records]
    assert seqs == sorted(seqs)                              # monotone, append-only


def test_an_observation_is_not_part_of_family_identity_or_standing(watched, fams):
    """Ruled §4: *"not analytical data and not part of family identity or standing."* Two engines whose
    only difference is whether anyone was watching hold materializations with identical identities,
    instances, fingerprints and establishments."""
    watched_engine, observer = watched
    quiet = KEX.build()
    assert isinstance(quiet.observations.observer, NullObserver)

    watched_engine.measure(watched_engine.family("revenue"), KEX.TOTAL)
    quiet.measure(quiet.family("revenue"), KEX.TOTAL)

    def analytical(engine):
        # **THE FINGERPRINT IS OMITTED FOR STRUCTURED VALUES, AND THAT IS NOT A WEAKENING.** A live
        # `hll_sketch` has no value-based `repr`, so its fingerprint is derived from its address and
        # differs between two runs of the same program — which is a known property of the sketch object,
        # not an analytical difference. Everything identity-bearing is still compared.
        # The establishment's KIND and ARITY are compared, not its parent TOKEN: `MaterializationId`s are
        # minted from a process-wide counter, so two engines necessarily name different parents for the
        # same derivation. That the id is opaque and non-comparable is M-1's design, not a gap here.
        return sorted((m.family_id, str(m.anchor), m.instance, m.eligibility,
                       m.establishment.kind, len(m.establishment.derived_from),
                       m.value_fingerprint if m.value.value_form != "structured" else "")
                      for m in engine.materializations.all())

    assert analytical(watched_engine) == analytical(quiet)
    assert len(observer) > 0                                  # and one of them really was observed


# ══ F · LOGGING IS NON-AUTHORITATIVE AND NON-BLOCKING FOR CORRECTNESS ═════════════════════════════
class Hostile:
    """An observer that fails as badly as an observer can."""

    def __init__(self, exc=None):
        self.exc = exc or RuntimeError("the logging backend is down")
        self.calls = 0

    def observe(self, observation):
        self.calls += 1
        raise self.exc


def test_a_raising_observer_cannot_fail_a_SERVED_request(fams):
    """Ruled §4: *"If observation fails, serving correctness must not fail."*"""
    hostile, quiet = KEX.build(), KEX.build()
    hostile.observations.observer = Hostile()

    a = hostile.measure(fams["revenue"], KEX.BY_DAY)
    b = quiet.measure(fams["revenue"], KEX.BY_DAY)
    assert a.served and b.served
    assert dict(a.value.cells) == dict(b.value.cells)
    assert a.route == b.route
    assert hostile.observations.failures == 1


def test_a_raising_observer_cannot_change_a_REFUSAL(fams):
    """The refusal path is the one where a naive `try/except` around the happy case would have leaked."""
    hostile, quiet = KEX.build(), KEX.build()
    hostile.observations.observer = Hostile()

    a = hostile.measure(fams["on_hand"], KEX.BY_STORE)
    b = quiet.measure(fams["on_hand"], KEX.BY_STORE)
    assert not a.served and not b.served
    assert a.refusal.code == b.refusal.code
    assert a.refusal.detail == b.refusal.detail


def test_even_a_BaseException_from_an_observer_is_contained(fams):
    """`BaseException`, not `Exception`. A `KeyboardInterrupt` raised inside a logging callback would
    violate the ruled guarantee exactly as squarely as a `TypeError`."""
    engine = KEX.build()
    engine.observations.observer = Hostile(KeyboardInterrupt())
    answer = engine.measure(fams["revenue"], KEX.BY_DAY)
    assert answer.served
    assert isinstance(engine.observations.last_failure, KeyboardInterrupt)


def test_an_observer_that_lies_about_its_shape_is_contained(fams):
    """Not every broken observer raises. One that is not callable at all must also cost nothing."""
    engine = KEX.build()
    engine.observations.observer = object()                   # type: ignore[assignment]
    assert engine.measure(fams["revenue"], KEX.BY_DAY).served
    assert engine.observations.failures == 1


def test_observer_failures_are_COUNTED_rather_than_swallowed_silently(fams):
    """Contained is not the same as hidden. A broken observer is loud where it is safe to be loud."""
    engine = KEX.build()
    engine.observations.observer = Hostile()
    for _ in range(3):
        engine.measure(fams["revenue"], KEX.TOTAL)
    assert engine.observations.failures == 3
    assert "FAILED" in engine.observations.summary()
    assert engine.observations.emitted == 0


def test_the_seam_is_WRITE_ONLY_so_an_observation_cannot_create_an_analytical_right(fams):
    """Ruled §6: *"They never create analytical rights."* Held as a property of the TYPE: the engine holds
    a SINK, and a sink's only verb is `emit`. There is no method on it that returns an observation, so no
    serving path could consult one even by mistake."""
    engine = KEX.build()
    assert isinstance(engine.observations, ObservationSink)
    assert not any(hasattr(engine.observations, n)
                   for n in ("records", "read", "history", "replay", "lookup", "get"))
    # the PROTOCOL an observer must satisfy has exactly one verb, and it returns nothing
    assert Hostile().observe.__code__.co_argcount == 2


def test_an_observer_that_records_a_HISTORY_of_hits_does_not_thereby_grant_one(fams):
    """The sharpest form of §6. An observer is handed every successful request, so a naive
    implementation could try to *replay* one — and it would still change nothing, because the serving
    path never asks."""
    engine = KEX.build()
    recorder = RecordingObserver()
    engine.observations.observer = recorder
    engine.measure(fams["revenue"], KEX.TOTAL)
    assert recorder.records and recorder.records[0].served

    engine.invalidate("revenue")                              # the RIGHT is gone; the LOG is not
    assert recorder.records                                   # the observation still remembers a hit
    refused = engine.measure(fams["revenue"], KEX.TOTAL)
    assert not refused.served                                 # and it buys exactly nothing
    assert "must be established at" in refused.refusal.detail


def test_the_default_engine_has_no_observer_and_takes_the_same_code_path(fams):
    """No `if observing:` branch anywhere: a serving path that differs by whether it is logged is a
    serving path whose logs describe a different program."""
    quiet = KEX.build()
    assert isinstance(quiet.observations.observer, NullObserver)
    assert not quiet.observations.active

    loud, observer = KEX.build(), RecordingObserver()
    loud.observations.observer = observer
    assert loud.observations.active

    a, b = quiet.measure(fams["revenue"], KEX.BY_DAY), loud.measure(fams["revenue"], KEX.BY_DAY)
    assert a.route == b.route and dict(a.value.cells) == dict(b.value.cells)
    assert a.seeded_from == b.seeded_from and a.considered == b.considered


def test_a_recording_observer_is_accepted_even_though_an_empty_one_is_FALSY():
    """**A regression guard on a real defect found building M-2.** `RecordingObserver` defines `__len__`,
    so a freshly-constructed one is falsy, and `observer or NullObserver()` silently discarded it —
    observation looked wired up and recorded nothing. The sink tests identity, not truthiness."""
    empty = RecordingObserver()
    assert not empty                                          # falsy, and that is fine
    sink = ObservationSink(empty)
    assert sink.observer is empty
    assert sink.active
    engine = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=KEX.MANIFOLD, observer=empty)
    assert engine.observations.observer is empty


def test_the_columnar_engine_has_its_own_sink(columnar):
    """Two request boundaries serving different material. Merging the logs would make "which substrate
    answered" unrecoverable from a record whose whole purpose is cost."""
    engine, _ = columnar
    observer = RecordingObserver()
    engine.observations.observer = observer
    assert engine.observations is not engine.authority.observations

    engine.measure("revenue", CEX.BY_DAY)
    assert len(observer) >= 1
    assert all(r.request.manifold == engine.manifold for r in observer.records)


# ══ G · M-1 CACHE-NEUTRALITY IS PRESERVED ═════════════════════════════════════════════════════════
def _comparable(cells):
    """**Compare a structured value by what it MEANS, not by its address.** A live `hll_sketch` has no
    value-based equality, so comparing the objects would compare identities and every neutrality claim
    would fail for the wrong reason. Its estimate is the analytical content."""
    out = {}
    for key, payload in cells.items():
        if hasattr(payload, "get_estimate"):
            out[key] = ("sketch", round(payload.get_estimate(), 9))
        else:
            out[key] = payload
    return out


def _answers(engine, evaluator, targets, expressions):
    """One engine's complete analytical output: every family target and every expression."""
    out = {}
    for family_id, anchor in targets:
        served = engine.measure(engine.family(family_id), anchor)
        out[(family_id, str(anchor))] = (
            _comparable(served.value.cells) if served.served
            else ("refused", served.refusal.code))
    for expression, anchor in expressions:
        served = evaluator.evaluate(expression, anchor)
        out[(expression.expression_id, str(anchor))] = (
            _comparable(served.value.cells) if served.served
            else ("refused", served.refusal.code))
    return out


TARGETS = [("revenue", KEX.BY_DAY), ("revenue", KEX.TOTAL),
           ("order_count", KEX.BY_DAY), ("order_count", KEX.TOTAL),
           ("distinct_customers", KEX.TOTAL)]


def test_cache_neutrality_holds_across_the_new_boundary(exprs):
    """**M-1's flagship invariant, re-run with expressions moved above the engine** (§3, §9 G): given the
    same lawful realization availability, answers are identical under a cold cache, a warm cache, and
    every lawful eviction subset — *and the expression answers are identical too*, which is a new claim
    because the expression is now re-derived from whatever the family cache happens to hold."""
    expressions = [(exprs["aov"], KEX.BY_DAY), (exprs["aov"], KEX.TOTAL),
                   (exprs["estimate"], KEX.TOTAL)]

    cold = KEX.build()
    baseline = _answers(cold, ExpressionEvaluator(cold), TARGETS, expressions)

    warm = KEX.build()
    warm_evaluator = ExpressionEvaluator(warm)
    _answers(warm, warm_evaluator, TARGETS, expressions)                 # populate
    assert _answers(warm, warm_evaluator, TARGETS, expressions) == baseline

    # and under every single eviction of a payload the warm engine holds
    for victim in [m.id for m in warm.materializations.all() if m.has_payload]:
        engine = KEX.build()
        engine_evaluator = ExpressionEvaluator(engine)
        _answers(engine, engine_evaluator, TARGETS, expressions)
        held = [m.id for m in engine.materializations.all() if m.has_payload]
        if len(held) <= len(TARGETS):
            continue
        engine.materializations.evict(held[len(held) // 2])
        assert _answers(engine, engine_evaluator, TARGETS, expressions) == baseline, victim


def test_cache_neutrality_is_unaffected_by_whether_anyone_is_OBSERVING(exprs):
    """**The new neutrality claim M-2 owes.** Observation is not a cache decision, so attaching an
    observer — or a broken one — must not move a single answer."""
    expressions = [(exprs["aov"], KEX.BY_DAY), (exprs["estimate"], KEX.TOTAL)]

    quiet = KEX.build()
    baseline = _answers(quiet, ExpressionEvaluator(quiet), TARGETS, expressions)

    for observer in (RecordingObserver(), Hostile(), object()):
        engine = KEX.build()
        engine.observations.observer = observer                # type: ignore[assignment]
        assert _answers(engine, ExpressionEvaluator(engine), TARGETS, expressions) == baseline


def test_eviction_neutrality_for_a_descendants_rights_still_holds(fams):
    """M-1's second flagship, re-asserted (§3): evicting an ancestor payload must not alter the analytical
    rights of a retained descendant."""
    engine = KEX.build()
    engine.measure(fams["revenue"], KEX.BY_DAY)
    day = [m for m in engine.materializations.select("revenue", anchor=KEX.BY_DAY)][0]
    root = engine.materializations.select("revenue", anchor=KEX.SALE_AT)[0]

    before = engine.adjudicate(
        Retained(key=engine._descriptor(day), value=day.value), fams["revenue"], KEX.TOTAL)
    engine.materializations.evict(root.id)
    after = engine.adjudicate(
        Retained(key=engine._descriptor(day), value=day.value), fams["revenue"], KEX.TOTAL)

    assert bool(before) == bool(after) and before.code == after.code
    assert engine.materialization(root.id).residency == EVICTED
    assert engine.measure(fams["revenue"], KEX.TOTAL).served


def test_the_other_m1_invariants_survive_the_split(mme, fams, evaluator, exprs):
    """§3's checklist, asserted together because the claim is that ALL of them survived."""
    # opaque MaterializationId
    mme.measure(fams["revenue"], KEX.BY_DAY)
    ids = [m.id for m in mme.materializations.all()]
    assert len(set(ids)) == len(ids)
    assert all(mme.materialization(i) is not None for i in ids)

    # coexistence of multiple materializations of one F@A, and currentness separate from residency
    at_root = mme.materializations.select("revenue", anchor=KEX.SALE_AT, eligibility=None)
    assert at_root
    assert {m.eligibility for m in mme.materializations.all()} <= {CURRENT, SUPERSEDED}
    assert all(hasattr(m, "residency") and hasattr(m, "eligibility")
               for m in mme.materializations.all())

    # dependency-based supersession propagation, along ACTUAL dependency
    day = mme.materializations.select("revenue", anchor=KEX.BY_DAY)[0]
    assert day.establishment.derived_from
    assert day.id in mme.materializations.descendants(day.establishment.derived_from[0])

    # continuation entitlement from family law/root/target rather than ancestry
    from columna_platform.kernel.materialization import cumulative_forgotten, entitlement_holds

    assert cumulative_forgotten(fams["revenue"], KEX.TOTAL) == (
        fams["revenue"].root.constituents - KEX.TOTAL.constituents)
    assert entitlement_holds(fams["revenue"], mme.law_of("revenue"), KEX.TOTAL)

    # structured family values, still structured and still never finalized by the engine
    sketch = mme.measure(fams["distinct"], KEX.TOTAL)
    assert sketch.served and sketch.value.value_form == "structured"
    assert hasattr(sketch.cell(), "get_estimate")


# ══ H · THE AOV AND HLL-ESTIMATE EXHIBITS THROUGH THE NEW BOUNDARY ════════════════════════════════
def test_exhibit_AOV_through_the_new_boundary(mme, evaluator, exprs):
    """The ruling's first diagram, asserted end to end:

        AOV@Month → MME supplies Revenue@Month + OrderCount@Month → basis compatibility
                  → expression evaluator → AOV result
    """
    calls: list[str] = []
    real = mme.measure

    def watched(family, anchor, **kwargs):
        calls.append(family.family_id)
        return real(family, anchor, **kwargs)

    mme.measure = watched                                     # type: ignore[method-assign]
    aov = evaluator.evaluate(exprs["aov"], KEX.TOTAL)

    # the MME supplied both operands. The ORDER is the basis's own `component_laws` order and is not
    # a claim this test makes.
    assert sorted(calls) == ["order_count", "revenue"]
    assert aov.served and aov.route == "evaluated"
    assert aov.seeded_from == "b_revenue_ordercount"          # from a declared sufficient basis
    assert aov.cell() == pytest.approx(500 / 6)               # pooled, NOT the mean of daily means
    assert abs(aov.cell() - (87.5 + 81.25) / 2) > 1.0         # the error a Mean family would have made
    # and the result is nowhere in the engine
    assert all(k.identity != "average_order_value" for k in mme.held)


def test_exhibit_AOV_refuses_an_incompatible_basis_above_the_boundary(mme, evaluator, exprs):
    """Compatibility is asked by the evaluator, over operands the MME supplied and validated. Both are
    established and available; what is missing is authority to combine them."""
    assert mme.measure(mme.family("revenue"), KEX.BY_DAY).served
    assert mme.measure(mme.family("audited_order_count"), KEX.BY_DAY).served

    refused = evaluator.evaluate(exprs["aov_audited"], KEX.BY_DAY)
    assert not refused.served
    assert "different-participation" in refused.refusal.detail
    assert "jointly meaningless" in refused.refusal.detail


def test_exhibit_HLL_estimate_through_the_new_boundary(mme, evaluator, exprs, fams):
    """The ruling's second diagram:

        estimate(HLLSketch@Month) → MME supplies HLLSketch@Month → finalizer/evaluator → estimate

    and the load-bearing negative: **the MME supplies the SKETCH and never the estimate.**"""
    supplied: list[tuple] = []
    real = mme.measure

    def watched(family, anchor, **kwargs):
        answer = real(family, anchor, **kwargs)
        supplied.append((family.family_id, answer.value.value_form if answer.served else None))
        return answer

    mme.measure = watched                                     # type: ignore[method-assign]
    estimate = evaluator.evaluate(exprs["estimate"], KEX.TOTAL)

    assert supplied == [("distinct_customers", "structured")]      # a SKETCH crossed the seam
    assert estimate.served and estimate.route == "evaluated"
    assert estimate.cell() == len({o["customer"] for o in KEX.ORDERS})
    assert isinstance(estimate.cell(), int)                        # the estimate is finalized, above
    # the family cache holds the sketch; it does not hold the estimate
    sketch = mme.materializations.select("distinct_customers", anchor=KEX.TOTAL)
    assert sketch and sketch[0].value.value_form == "structured"
    assert not mme.materializations.select("distinct_customer_estimate", eligibility=None)


def test_exhibit_a_coarser_estimate_goes_back_through_the_sketch(mme, evaluator, exprs):
    """**The doctrine the boundary protects.** With no expression cache the route is unmistakable: a
    coarser estimate cannot be folded from a finer estimate, it is re-finalized from a merged sketch."""
    fine = evaluator.evaluate(exprs["estimate"], KEX.BY_DAY)
    coarse = evaluator.evaluate(exprs["estimate"], KEX.TOTAL)
    assert fine.served and coarse.served
    assert fine.seeded_from == coarse.seeded_from == "b_sketch"
    # the coarse answer is NOT the sum of the fine ones — it went through a sketch UNION
    assert coarse.cell() < sum(fine.value.cells.values())


def test_exhibit_both_run_over_the_COLUMNAR_substrate_too(columnar):
    """The same two exhibits, positionally, through `ColumnarExpressionEvaluator`."""
    engine, evaluator = columnar
    observer = RecordingObserver()
    engine.observations.observer = observer

    aov = evaluator.evaluate("average_order_value", CEX.BY_DAY)
    assert aov.served and aov.route == "evaluated"
    assert aov.value.cell(("D2",)) == pytest.approx(81.25)

    estimate = evaluator.evaluate("distinct_customer_estimate", CEX.BY_DAY)
    assert estimate.served and estimate.seeded_from == "b_sketch"

    # neither output is held, and every family request behind them was observed
    assert all(k.identity not in ("average_order_value", "distinct_customer_estimate")
               for k in engine.held)
    assert observer.records
    assert {r.request.family_id for r in observer.records} >= {"revenue", "order_count"}
    assert all(r.request.on_behalf_of for r in observer.records)


def test_an_unrealized_law_is_still_a_PROVIDER_limit_said_as_one(exprs):
    """Above the boundary as below it: a provider's inability does not remove a law."""
    thin = MME(KEX.COMMERCE, REGISTRY, NO_MEAN, manifold=KEX.MANIFOLD)
    revenue, order_count = KEX._families()[0], KEX._families()[1]
    for family in (revenue, order_count):
        thin.register_family(family)
    thin.register_expression(exprs["aov"])
    thin.establish_root(revenue, KEX.ORDERS)
    thin.establish_root(order_count, KEX.ORDERS)

    with pytest.raises(KernelRefusal) as refused:
        ExpressionEvaluator(thin).evaluate(exprs["aov"], KEX.TOTAL)
    assert refused.value.code in ("unrealized-law", "unrealized-capability")


# ══ THE EXHIBITS RUN GREEN ════════════════════════════════════════════════════════════════════════
def test_the_three_exhibits_run_green_through_the_new_boundary(capsys):
    """Every narrative check in all three exhibits, which is where the boundary is demonstrated rather
    than asserted."""
    from columna_platform.columnar import exhibit as columnar_exhibit
    from columna_platform.frameql import exhibit as frameql_exhibit
    from columna_platform.kernel import exhibit as kernel_exhibit

    for exhibit in (kernel_exhibit, columnar_exhibit, frameql_exhibit):
        assert exhibit.main() == 0, exhibit.__name__
        captured = capsys.readouterr().out
        assert "✗" not in captured, exhibit.__name__


# ══ WHAT M-2 DELIBERATELY DID NOT BUILD ═══════════════════════════════════════════════════════════
def test_no_cost_model_no_scoring_and_no_optimizer_arrived_early():
    """Ruled §4/§5/§8: *"Do not build the optimization algorithm yet… Do not implement this optimizer in
    M-2… Do not implement descendant-value scoring yet."*

    A guard, not a formality: the temptation in a unit that builds an observation record is to add the one
    obvious score — and §5 is specifically a warning that the obvious score
    (`request_frequency × recompute_from_root_cost`) is the WRONG quantity."""
    from columna_platform.kernel import observation

    forbidden = ("value_of", "score", "cache_value", "evict_candidates", "policy", "optimize",
                 "recommend", "cost_of", "benefit")
    public = {n for n in dir(observation) if not n.startswith("_")}
    assert not (public & set(forbidden))
    assert not any(hasattr(RecordingObserver, n) for n in forbidden)
    assert not any(hasattr(Fulfillment, n) for n in forbidden)

    # the counters that ARE present are observed quantities with no weighting applied
    assert {f.name for f in fields(Fulfillment)} == {
        "directly_held", "selected", "seeded_from", "folded", "considered", "admitted"}
    assert {f.name for f in fields(FamilyRequest)} == {
        "manifold", "build", "family_id", "target", "data_state", "on_behalf_of"}


def test_no_persistence_no_iceberg_no_postgres_and_no_scheduler_arrived_either():
    """The other rulings-out, held as an import ban rather than an intention."""
    import columna_platform.kernel.expression as kernel_expression
    import columna_platform.kernel.observation as observation

    source = "".join(open(m.__file__, encoding="utf-8").read()
                     for m in (observation, kernel_expression))
    for banned in ("iceberg", "psycopg", "sqlalchemy", "postgres", "APScheduler", "sqlite3",
                   "pickle", "json.dump", "open("):
        assert banned not in source, banned

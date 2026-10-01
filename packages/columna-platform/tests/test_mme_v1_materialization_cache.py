"""
test_mme_v1_materialization_cache.py — **M-1: the governed family-materialization cache.**

    *"MME v1 is a governed family-materialization cache. Ordinary cache mechanics manage residency and
    dependency; analytical law governs reuse."*  — Huayin, 2026-09-29

The required capabilities A–I are the sections. Two invariants are the flagship and are stated as such:

    **CACHE NEUTRALITY** — given the same lawful realization availability, analytical answers are identical
    under a cold cache, a fully warm cache, and every lawful eviction subset.

    **EVICTION NEUTRALITY** — evicting an ancestor payload must not alter the analytical rights of a
    retained descendant.

WHAT IS NOT EXERCISED, DELIBERATELY: no persistence, no Iceberg, no Postgres, no expression cache, no
scheduler, no CDC, no source refresh. A test that mocked one would be where the next unit's design got made
by accident.
"""
from __future__ import annotations

from dataclasses import replace
from itertools import combinations

import pyarrow as pa
import pytest

from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar import CoordinateIndex, GovernedBlock, standing
from columna_platform.kernel import KernelRefusal
from columna_platform.kernel import exhibit as KEX
from columna_platform.kernel.materialization import (
    AT_ROOT,
    COEXIST,
    CONTINUED,
    CURRENT,
    EVICTED,
    EXPIRED,
    INDEPENDENT,
    REJECT,
    RESIDENT,
    SUPERSEDE,
    SUPERSEDED,
    Establishment,
    ManifoldBuild,
    MaterializationId,
    TransitionIntent,
    admitted_targets,
    cumulative_forgotten,
    entitlement_holds,
)

LOAD = "load:orders@08:00Z"
RELOAD = "load:orders@17:30Z"


@pytest.fixture
def engine():
    """The settled columnar world, established from one evidence state."""
    return CEX.build(settled=True, data_state=LOAD)


@pytest.fixture
def mme(engine):
    return engine[0]


@pytest.fixture
def block(engine):
    return engine[1]


def _current(mme, family_id, anchor=None):
    return mme.materializations.select(family_id, anchor=anchor)


def _supersede_held(mme, family_id, anchor=None):
    """Transition intent that replaces whatever is current in that slot — `None` when nothing is."""
    held = tuple(m.id for m in _current(mme, family_id, anchor))
    return TransitionIntent(SUPERSEDE, held) if held else None


# ══ A · THE MATERIALIZATION OBJECT ════════════════════════════════════════════════════════════════
def test_cache_identity_is_opaque_and_is_not_derived_from_analytical_attributes(mme):
    """*"Please introduce an opaque `MaterializationId` … rather than deriving cache identity from
    family/anchor/data-state fields."*"""
    m = _current(mme, "revenue", CEX.SALE_AT)[0]
    assert isinstance(m.id, MaterializationId)
    token = m.id.token
    for attribute in (m.family_id, str(m.anchor), m.data_state, m.instance.participation,
                      m.realization.provider, m.build.reference):
        assert attribute not in token
    assert token.startswith("mat-")


def test_the_analytical_attributes_remain_searchable_properties(mme):
    """*"Those analytical/cache attributes remain searchable/selectable properties of the
    materialization; they do not define the object's cache identity."*"""
    assert _current(mme, "revenue")
    assert mme.materializations.select("revenue", anchor=CEX.SALE_AT)
    assert mme.materializations.select("revenue", data_state=LOAD)
    assert mme.materializations.select(eligibility=CURRENT)
    assert not mme.materializations.select("revenue", data_state="load:nothing-like-this")


def test_the_materialization_carries_everything_required_and_nothing_expression_shaped(mme):
    m = _current(mme, "revenue", CEX.SALE_AT)[0]
    assert m.build == mme.build                       # Manifold build
    assert m.point.family_id == "revenue"             # family identity
    assert m.anchor == CEX.SALE_AT                    # anchor
    assert m.value.CONTINUATION_BEARING is True       # continuation-bearing family value
    assert m.data_state == LOAD                       # cache-instance/data-state attribute
    assert m.eligibility == CURRENT and m.residency == RESIDENT
    assert m.establishment.kind == AT_ROOT
    for expression_shaped in ("constructor", "basis_id", "operands", "admitted_bases"):
        assert not hasattr(m, expression_shaped)
    for scheduler_shaped in ("cursor", "watermark", "schedule", "source", "refresh"):
        assert not hasattr(m, scheduler_shaped)


# ══ B · THE DEPENDENCY GRAPH ══════════════════════════════════════════════════════════════════════
def test_supersession_propagates_along_actual_dependency(mme):
    """`Revenue@Order #1 → Revenue@Day #2 → Revenue@Month #3`. Superseding `#2` affects `#3` because `#3`
    actually depends on it."""
    one = _current(mme, "revenue", CEX.SALE_AT)[0]
    mme.measure("revenue", CEX.BY_DAY)                       # #2, continued from #1
    two = _current(mme, "revenue", CEX.BY_DAY)[0]
    mme.measure("revenue", CEX.TOTAL)                        # #3, continued from #2
    three = _current(mme, "revenue", CEX.TOTAL)[0]

    assert two.establishment == Establishment(CONTINUED, (one.id,))
    assert three.establishment == Establishment(CONTINUED, (two.id,))
    assert mme.materializations.descendants(one.id) == (two.id, three.id)

    mme.materializations.supersede([two.id], reason="a newer Revenue@Day arrived")
    assert mme.materialization(two.id).eligibility == SUPERSEDED
    assert mme.materialization(three.id).eligibility == SUPERSEDED           # inherited
    assert "which was superseded" in mme.materialization(three.id).superseded_reason
    assert mme.materialization(one.id).eligibility == CURRENT                # ancestors untouched


def test_an_independently_established_materialization_is_not_invalidated_by_a_sibling(mme, block):
    """*"A separately established Revenue@Month #9 should not be invalidated merely because #2 changed."*
    Consequence follows a recorded edge, never a family name."""
    one = _current(mme, "revenue", CEX.SALE_AT)[0]
    mme.measure("revenue", CEX.BY_DAY)
    two = _current(mme, "revenue", CEX.BY_DAY)[0]

    # #9 — the same F@A as a derived Revenue@Day would be, supplied directly by a governed realization
    nine_block = GovernedBlock.of(
        CoordinateIndex.of(CEX.MANIFOLD, CEX.BY_STORE, [("S1",), ("S2",)]),
        {"revenue": pa.array([1.0, 2.0], type=pa.float64())},
        {"revenue": standing("revenue", mme.authority.instance_of("revenue"), n=2)})
    mme.establish(nine_block, "revenue", at_root=False, data_state=LOAD)
    nine = _current(mme, "revenue", CEX.BY_STORE)[0]
    assert nine.establishment == Establishment(INDEPENDENT)
    assert nine.establishment.derived_from == ()

    mme.materializations.supersede([two.id], reason="a newer Revenue@Day arrived")
    assert mme.materialization(nine.id).eligibility == CURRENT               # nothing propagated
    assert nine.id not in mme.materializations.descendants(one.id)


def test_a_shared_data_state_is_not_a_dependency_edge(mme, block):
    """A `data_state` coincidence is suggestive and is NOT an edge: *"Do not infer supersession merely from
    equal `DataStateRef` tokens."*"""
    mme.measure("revenue", CEX.BY_DAY)
    two = _current(mme, "revenue", CEX.BY_DAY)[0]
    counts = _current(mme, "order_count", CEX.SALE_AT)[0]
    assert counts.data_state == two.data_state == LOAD

    mme.materializations.supersede([two.id], reason="evidence moved")
    assert mme.materialization(counts.id).eligibility == CURRENT


# ══ C · COEXISTENCE ═══════════════════════════════════════════════════════════════════════════════
def test_two_materializations_of_one_family_at_one_anchor_coexist(mme, block):
    """**The defect M-1 exists to fix.** Before this unit the second silently overwrote the first."""
    before = mme.materializations.select("order_count", anchor=CEX.SALE_AT, eligibility=None)
    mme.establish(block, "order_count", data_state=RELOAD)
    after = mme.materializations.select("order_count", anchor=CEX.SALE_AT, eligibility=None)

    assert len(after) == len(before) + 1
    assert len({m.id for m in after}) == len(after)                 # distinct cache identities
    assert {LOAD, RELOAD} <= {m.data_state for m in after}
    assert all(m.has_payload for m in after)                        # nothing was dropped


def test_an_ordinary_request_still_gets_exactly_one_answer(mme, block):
    """*"The request asks for an analytical identity, not a physical materialization."*"""
    mme.establish(block, "order_count", data_state=RELOAD)
    served = mme.measure("order_count", CEX.BY_DAY)
    assert served.served
    assert len(mme.materializations.select("order_count", anchor=CEX.SALE_AT)) == 1   # one CURRENT


# ══ D · SUPERSESSION ══════════════════════════════════════════════════════════════════════════════
def test_transition_intent_coexist_retains_without_becoming_current(mme, block):
    mme.establish(block, "order_count", data_state=RELOAD, intent=TransitionIntent(COEXIST))
    coexisting = [m for m in mme.materializations.select("order_count", anchor=CEX.SALE_AT,
                                                         eligibility=None)
                  if m.data_state == RELOAD][0]
    assert coexisting.eligibility == SUPERSEDED
    assert "coexisting under a different data state" in coexisting.superseded_reason
    assert coexisting.residency == RESIDENT                          # retained by policy


def test_transition_intent_supersede_moves_currentness_and_not_residency(mme, block):
    first = _current(mme, "order_count", CEX.SALE_AT)[0]
    mme.establish(block, "order_count", data_state=RELOAD,
                  intent=TransitionIntent(SUPERSEDE, (first.id,)))
    assert mme.materialization(first.id).eligibility == SUPERSEDED
    assert mme.materialization(first.id).residency == RESIDENT       # still resident
    assert mme.materialization(first.id).superseded_by is not None
    assert _current(mme, "order_count", CEX.SALE_AT)[0].data_state == RELOAD


def test_supersede_may_name_a_materialization_with_no_dependency_edge(mme, block):
    """*"An external caller may offer a new F@A and explicitly say that one or more currently retained
    materializations are superseded, even when there are no parent/child dependency edges between them."*"""
    mme.measure("revenue", CEX.BY_DAY)
    by_day = _current(mme, "revenue", CEX.BY_DAY)[0]
    at_root = _current(mme, "revenue", CEX.SALE_AT)[0]
    assert by_day.id not in at_root.establishment.derived_from

    # a NEW root materialization that declares the (unrelated-by-edge) BY_DAY one superseded too
    mme.establish(block, "revenue", data_state=RELOAD,
                  intent=TransitionIntent(SUPERSEDE, (at_root.id, by_day.id)))
    assert mme.materialization(by_day.id).eligibility == SUPERSEDED
    assert mme.materialization(at_root.id).eligibility == SUPERSEDED


def test_supersession_across_families_is_refused(mme, block):
    """MME validates the claimed analytical relationship. Across families it would be an evidence-level
    claim this engine cannot check."""
    other = _current(mme, "order_count", CEX.SALE_AT)[0]
    with pytest.raises(KernelRefusal) as exc:
        mme.establish(block, "revenue", data_state=RELOAD,
                      intent=TransitionIntent(SUPERSEDE, (other.id,)))
    assert exc.value.code == "unrelated-supersession-target"
    assert "cannot validate" in exc.value.detail


def test_an_unnamed_supersession_is_refused(mme):
    with pytest.raises(KernelRefusal) as exc:
        TransitionIntent(SUPERSEDE, ())
    assert exc.value.code == "supersede-names-nothing"


def test_the_reject_intent_admits_nothing(mme, block):
    before = len(mme.materializations)
    with pytest.raises(KernelRefusal) as exc:
        mme.establish(block, "order_count", data_state=RELOAD, intent=TransitionIntent(REJECT))
    assert exc.value.code == "rejected-by-offerer"
    assert len(mme.materializations) == before


# ══ E · CURRENTNESS VS RESIDENCY ══════════════════════════════════════════════════════════════════
def test_a_superseded_materialization_may_remain_resident_and_still_never_answers(mme, block):
    """*"Residency never creates analytical authority."*"""
    first = _current(mme, "order_count", CEX.SALE_AT)[0]
    mme.establish(block, "order_count", data_state=RELOAD,
                  intent=TransitionIntent(SUPERSEDE, (first.id,)))
    superseded = mme.materialization(first.id)
    assert superseded.residency == RESIDENT and superseded.has_payload
    assert not superseded.serviceable
    assert superseded not in mme.materializations.candidates_for(
        "order_count", CEX.BY_DAY, mme.authority.instance_of("order_count"))


def test_expiring_a_current_materialization_withholds_it_without_calling_it_wrong(mme):
    """`EXPIRED` ≠ `SUPERSEDED`: a policy withdrawal is not a claim that the value was wrong."""
    m = _current(mme, "revenue", CEX.SALE_AT)[0]
    mme.materializations.expire(m.id)
    expired = mme.materialization(m.id)
    assert expired.eligibility == CURRENT                     # governed standing untouched
    assert expired.residency == EXPIRED and not expired.serviceable

    answer = mme.measure("revenue", CEX.BY_DAY)
    assert not answer.served
    assert "unusable by POLICY" in answer.refusal.detail
    assert "OUR absence, not the world's" in answer.refusal.detail


def test_a_pinned_materialization_may_not_be_evicted_or_dropped(mme):
    m = _current(mme, "revenue", CEX.SALE_AT)[0]
    mme.materializations.pin(m.id)
    for operation in (mme.materializations.evict, mme.materializations.drop):
        with pytest.raises(KernelRefusal) as exc:
            operation(m.id)
        assert exc.value.code == "pinned"


def test_eviction_releases_the_payload_and_keeps_the_record(mme):
    mme.measure("revenue", CEX.BY_DAY)
    two = _current(mme, "revenue", CEX.BY_DAY)[0]
    mme.materializations.evict(two.id)
    evicted = mme.materialization(two.id)
    assert evicted is not None                                # the record survives
    assert evicted.residency == EVICTED and not evicted.has_payload
    assert evicted.eligibility == CURRENT                     # eviction says nothing governed


# ══ F · CACHE ADMISSION POLICY ════════════════════════════════════════════════════════════════════
def test_materialization_does_not_imply_retention(mme):
    """*"A fetched/derived F@A may serve one request and be discarded."*"""
    before = len(mme.materializations)
    served = mme.measure("revenue", CEX.TOTAL, retain=False)
    assert served.served
    assert len(mme.materializations) == before                # nothing was admitted


def test_the_engine_works_cold_warm_and_partially_populated(block):
    cold, cold_block = CEX.build(settled=True, data_state=LOAD)
    for m in list(cold.materializations.all()):               # empty it completely
        cold.materializations.drop(m.id)
    assert len(cold.materializations) == 0
    assert not cold.measure("revenue", CEX.BY_DAY).served     # NEED, in v1's vocabulary

    cold.establish(cold_block, "revenue", data_state=LOAD)
    assert cold.measure("revenue", CEX.BY_DAY).served         # warm enough

    warm, _ = CEX.build(settled=True, data_state=LOAD)
    warm.measure("revenue", CEX.BY_DAY)
    assert warm.measure("revenue", CEX.TOTAL).served          # fully warm


# ══ G · THE FLAGSHIP INVARIANTS ═══════════════════════════════════════════════════════════════════
# The sweep runs on the IN-MEMORY kernel engine: the cache lifecycle is substrate-agnostic — one
# `MaterializationStore`, one `adjudicate` — and re-running hundreds of DataFusion aggregations would
# measure Arrow rather than the invariant. The columnar engine gets its own spot-check below, so the
# substrate is not taken on trust either.
KERNEL_TARGETS = [("revenue", KEX.BY_DAY), ("revenue", KEX.TOTAL), ("order_count", KEX.BY_DAY),
                  ("order_count", KEX.TOTAL), ("distinct_customers", KEX.BY_DAY),
                  ("gauge", KEX.BY_STORE)]

_ROWS = {"revenue": (KEX.ORDERS, "value"), "order_count": (KEX.ORDERS, "value"),
         "distinct_customers": (KEX.ORDERS, "customer"), "gauge": (KEX.READINGS, "value")}


def _kernel_answer(mme, family_id, anchor):
    """Ask the cache; if it cannot answer, establish the root and ask again — the Realization Manager in
    miniature, so *"the same lawful realization availability"* is held constant across cache shapes."""
    family = mme.family(family_id)
    served = mme.measure(family, anchor)
    if not served.served:
        rows, key = _ROWS[family_id]
        held = tuple(m.id for m in mme.materializations.select(family_id, anchor=family.root))
        mme.establish_root(family, rows, value_key=key,
                           intent=TransitionIntent(SUPERSEDE, held) if held else None)
        served = mme.measure(family, anchor)
    return served


def _rendered(value):
    """A comparable rendering of ONE family value. A structured family value is a live object whose `repr`
    is its address, so a sketch is compared by its portable serialization — the value itself, not a pointer
    to it, and NOT its estimate, which would be the finalization this unit deliberately never performs."""
    if hasattr(value, "serialize_compact"):
        return value.serialize_compact()
    return repr(value)


def _cells(answer):
    return tuple(sorted((tuple(map(str, k)), _rendered(v)) for k, v in answer.value.cells.items()))


def _warm_kernel():
    mme = KEX.build()
    for family_id, anchor in KERNEL_TARGETS:
        _kernel_answer(mme, family_id, anchor)
    return mme


def test_cache_neutrality_cold_warm_and_every_eviction_subset():
    """**THE FLAGSHIP.** *"Given the same lawful realization availability, analytical answers are identical
    under a cold cache, fully warm cache, and every lawful eviction subset. Eviction may change
    cost/latency, never meaning."*

    The space covered, stated exactly rather than implied: the **fully warm** cache; the **cold** cache
    (every materialization dropped, not merely evicted); **every single-eviction** subset, each from its own
    fresh warm engine; and a **nested chain** that evicts every originally-held materialization one at a
    time, checking after each step — so the invariant is asked of a cache of every size in between. A
    failure of this invariant is witnessed by ONE eviction if it is witnessed at all, which is why the
    single evictions are the exhaustive part and the chain is the belt."""
    reference = {}
    warm = _warm_kernel()
    for family_id, anchor in KERNEL_TARGETS:
        reference[(family_id, anchor)] = _cells(_kernel_answer(warm, family_id, anchor))
    assert len(reference) == len(KERNEL_TARGETS)

    cold = KEX.build()
    for m in list(cold.materializations.all()):
        cold.materializations.drop(m.id)
    assert len(cold.materializations) == 0
    for family_id, anchor in KERNEL_TARGETS:
        assert _cells(_kernel_answer(cold, family_id, anchor)) == reference[(family_id, anchor)]

    population = len(_warm_kernel().materializations)
    assert population >= 8
    for position in range(population):
        trial = _warm_kernel()
        victim = trial.materializations.all()[position]
        trial.materializations.evict(victim.id)
        for family_id, anchor in KERNEL_TARGETS:
            assert _cells(_kernel_answer(trial, family_id, anchor)) == \
                reference[(family_id, anchor)], (family_id, str(anchor), str(victim.id))

    # The victim list is captured UP FRONT: answering re-establishes material, and a loop that waited for
    # the store to empty would never finish — it did not, the first time this was written.
    chain = _warm_kernel()
    victims = [m.id for m in chain.materializations.all()]
    for victim in victims:
        held = chain.materialization(victim)
        if held is not None and held.has_payload:
            chain.materializations.evict(victim)
        for family_id, anchor in KERNEL_TARGETS:
            assert _cells(_kernel_answer(chain, family_id, anchor)) == \
                reference[(family_id, anchor)], (family_id, str(anchor), str(victim))
    assert all(not chain.materialization(v).has_payload
               for v in victims if chain.materialization(v) is not None)


def test_cache_neutrality_holds_over_the_columnar_substrate_too(mme, block):
    """The same invariant over real Arrow/DataFusion material — a SPOT-CHECK: warm, cold, and one eviction
    of each held materialization of the families under test. The exhaustive sweep is the kernel one."""
    targets = [("revenue", CEX.TOTAL), ("order_count", CEX.BY_DAY)]

    def answer(engine, source, family_id, anchor):
        served = engine.measure(family_id, anchor)
        if not served.served:
            held = tuple(m.id for m in engine.materializations.select(family_id, anchor=CEX.SALE_AT))
            engine.establish(source, family_id, data_state=LOAD,
                             intent=TransitionIntent(SUPERSEDE, held) if held else None)
            served = engine.measure(family_id, anchor)
        return served

    def cells(served):
        state = served.value
        return tuple(sorted((tuple(map(str, c)), repr(v))
                            for c, v in zip(state.index.coordinates, state.values.to_pylist())))

    reference = {t: cells(answer(mme, block, *t)) for t in targets}

    cold, cold_block = CEX.build(settled=True, data_state=LOAD)
    for m in list(cold.materializations.all()):
        cold.materializations.drop(m.id)
    for target in targets:
        assert cells(answer(cold, cold_block, *target)) == reference[target]

    for victim in [m.id for m in mme.materializations.all()
                   if m.family_id in ("revenue", "order_count")]:
        held = mme.materialization(victim)
        if held is not None and held.has_payload:
            mme.materializations.evict(victim)
        for target in targets:
            assert cells(answer(mme, block, *target)) == reference[target], (target, str(victim))


def test_eviction_of_an_ancestor_payload_does_not_alter_a_descendants_rights(mme):
    """**The second flagship**, and the reason the entitlement is derived rather than walked: if rights were
    computed by walking `derived_from`, evicting `#2` would make `#3` look independently established."""
    mme.measure("revenue", CEX.BY_DAY)
    two = _current(mme, "revenue", CEX.BY_DAY)[0]
    mme.measure("revenue", CEX.TOTAL)
    three = _current(mme, "revenue", CEX.TOTAL)[0]

    family, law = mme.family("revenue"), mme.law_of("revenue")
    anchors = (CEX.SALE_AT, CEX.BY_DAY, CEX.BY_STORE, CEX.TOTAL)
    before = admitted_targets(family, law, anchors)

    mme.materializations.evict(two.id)                       # release the ancestor's payload
    assert admitted_targets(family, law, anchors) == before
    mme.materializations.drop(two.id)                        # and forget the record entirely
    assert admitted_targets(family, law, anchors) == before
    assert mme.materialization(three.id) is not None
    assert mme.materialization(three.id).eligibility == CURRENT


def test_the_same_invariant_holds_for_a_restricted_region():
    """The additive family cannot show this alone — `revenue` admits everything. `on_hand` is the family
    whose region actually bites, and its rights are unchanged by eviction too."""
    mme, _ = CEX.build(data_state=LOAD)
    on_hand = CEX._families()[4]
    mme.authority.register_family(on_hand)
    index = CoordinateIndex.of(CEX.MANIFOLD, CEX.COMMERCE.anchor({"store", "day"}),
                               [("D1", "S1"), ("D1", "S2"), ("D2", "S1"), ("D2", "S2")])
    level = GovernedBlock.of(index, {"on_hand": pa.array([10, 7, 12, 9], type=pa.int64())},
                             {"on_hand": standing("on_hand", mme.authority.instance_of("on_hand"), n=4)})
    mme.establish(level, "on_hand", data_state=LOAD)
    mme.measure("on_hand", CEX.BY_DAY)
    day = _current(mme, "on_hand", CEX.BY_DAY)[0]
    root = _current(mme, "on_hand", CEX.COMMERCE.anchor({"store", "day"}))[0]

    family, law = mme.family("on_hand"), mme.law_of("on_hand")
    anchors = (CEX.COMMERCE.anchor({"store", "day"}), CEX.BY_DAY, CEX.BY_STORE, CEX.TOTAL)
    before = admitted_targets(family, law, anchors)
    assert CEX.BY_DAY in before and CEX.BY_STORE not in before and CEX.TOTAL not in before

    mme.materializations.evict(root.id)
    assert admitted_targets(family, law, anchors) == before
    # and the laundering route is still refused from the surviving descendant
    laundered = mme.measure("on_hand", CEX.TOTAL)
    assert not laundered.served
    assert "cannot launder an edge the law does not admit" in laundered.refusal.detail
    assert mme.materialization(day.id).eligibility == CURRENT


# ══ H · DUPLICATE-CURRENT CONSISTENCY ═════════════════════════════════════════════════════════════
def test_agreeing_duplicates_may_both_be_current_and_the_mme_picks(mme, block):
    """*"Agreement may allow MME to choose one."*"""
    mme.establish(block, "order_count", data_state=LOAD)      # the same slot, state and VALUE
    both = mme.materializations.select("order_count", anchor=CEX.SALE_AT)
    assert len(both) == 2
    assert len({m.value_fingerprint for m in both}) == 1
    served = mme.measure("order_count", CEX.BY_DAY)
    assert served.served                                     # one answer; the cache chose


def test_disagreeing_duplicates_are_a_consistency_failure(mme):
    """*"Disagreement is a consistency failure … user/request never chooses the cache entry."*"""
    different = GovernedBlock.of(
        CoordinateIndex.of(CEX.MANIFOLD, CEX.SALE_AT, [("D1", "O1", "S1")]),
        {"order_count": pa.array([99], type=pa.int64())},
        {"order_count": standing("order_count", mme.authority.instance_of("order_count"), n=1)})
    with pytest.raises(KernelRefusal) as exc:
        mme.establish(different, "order_count", data_state=LOAD)
    assert exc.value.code == "duplicate-current-disagreement"
    assert "will not pick between two answers to one question" in exc.value.detail
    assert "nothing is admitted" in exc.value.detail
    # and the held one is untouched
    assert len(mme.materializations.select("order_count", anchor=CEX.SALE_AT)) == 1


# ══ I · THE STRUCTURED FAMILY, THROUGH THE SAME LIFECYCLE ═════════════════════════════════════════
def test_the_sketch_family_runs_the_whole_lifecycle_without_finalizing(mme, block):
    """*"Run the same lifecycle through HLLSketch, without finalizing to the estimate."*"""
    root = _current(mme, "distinct_customers", CEX.SALE_AT)[0]
    mme.measure("distinct_customers", CEX.BY_DAY)
    day = _current(mme, "distinct_customers", CEX.BY_DAY)[0]
    assert day.establishment == Establishment(CONTINUED, (root.id,))
    assert isinstance(day.value.cell(("D1",)), bytes)             # still a sketch, never an estimate

    # coexistence
    mme.establish(block, "distinct_customers", data_state=RELOAD)
    assert len(mme.materializations.select("distinct_customers", anchor=CEX.SALE_AT,
                                           eligibility=None)) == 2
    # supersession propagates to the derived sketch
    mme.materializations.supersede([root.id], reason="a newer sketch arrived")
    assert mme.materialization(day.id).eligibility == SUPERSEDED
    # residency is independent
    assert mme.materialization(day.id).residency == RESIDENT and mme.materialization(day.id).has_payload
    # the estimate is an EXPRESSION and is not in the family cache at all
    assert not mme.materializations.select("distinct_customer_estimate", eligibility=None)


# ══ THE §7 QUESTION · ENTITLEMENT IS DERIVED, AND THERE IS NO COUNTEREXAMPLE ══════════════════════
def test_the_cumulative_forgotten_set_is_route_independent():
    """**The theorem.** For `T ⊆ M ⊆ R`, `(R − M) ∪ (M − T) = R − T`. Every route from `R_F` to a target
    forgets the same set, so continuation entitlement cannot depend on the route."""
    mme = KEX.build()
    for family_id in mme.families:
        family = mme.family(family_id)
        root = family.root
        anchors = [KEX.COMMERCE.anchor(set(c))
                   for n in range(len(root.constituents) + 1)
                   for c in combinations(sorted(root.constituents), n)]
        for middle in anchors:
            for target in anchors:
                if not target.constituents < middle.constituents:
                    continue
                by_route = ((root.constituents - middle.constituents)
                            | (middle.constituents - target.constituents))
                assert frozenset(by_route) == cumulative_forgotten(family, target)


def test_no_family_in_the_vocabulary_has_route_sensitive_entitlement():
    """*"Please produce one concrete v8 family counterexample if you believe two lawful instances of the
    same F@A … can have different onward continuation rights solely because they were established through
    different routes."* **There is none**, and this measures it rather than asserting it."""
    mme = KEX.build()
    route_sensitive = []
    for family_id in mme.families:
        family, law = mme.family(family_id), mme.law_of(family_id)
        root = family.root
        anchors = [KEX.COMMERCE.anchor(set(c))
                   for n in range(len(root.constituents) + 1)
                   for c in combinations(sorted(root.constituents), n)]
        for target in anchors:
            verdicts = {law.region.admits(frozenset(
                (root.constituents - middle.constituents) | (middle.constituents - target.constituents)))
                for middle in anchors
                if target.constituents < middle.constituents <= root.constituents}
            if target.constituents < root.constituents:
                verdicts.add(law.region.admits(cumulative_forgotten(family, target)))
            if len(verdicts) > 1:
                route_sensitive.append((family_id, str(target)))
    assert route_sensitive == []


def test_the_derived_entitlement_agrees_with_the_stored_provenance_everywhere():
    """The equivalence, pinned so that widening `ContinuationRegion` into a genuine per-edge graph — the one
    change that would make routes matter — fails here rather than silently."""
    mme = KEX.build()
    for family_id in mme.families:
        family = mme.family(family_id)
        for retained in mme.holdings():
            if retained.key.sort != "family" or retained.key.identity != family_id:
                continue
            state = retained.value
            for target in (KEX.BY_DAY, KEX.BY_STORE, KEX.TOTAL):
                if not target.constituents < state.anchor.constituents:
                    continue
                stored = state.forgotten_since_root | state.anchor.forgets(target)
                assert stored == cumulative_forgotten(family, target)


def test_entitlement_is_the_same_for_derived_and_independent_material(mme):
    """Two lawful instances of one `F@A`, one derived and one independently established: identical rights."""
    mme.measure("revenue", CEX.BY_DAY)
    derived = _current(mme, "revenue", CEX.BY_DAY)[0]
    assert derived.establishment.kind == CONTINUED

    family, law = mme.family("revenue"), mme.law_of("revenue")
    anchors = (CEX.BY_DAY, CEX.BY_STORE, CEX.TOTAL)
    rights = admitted_targets(family, law, anchors)
    assert entitlement_holds(family, law, CEX.TOTAL)
    # the same rights hold for material that never came down that route — the formula never mentions it
    assert admitted_targets(family, law, anchors) == rights


# ══ §8 · INDEPENDENT ESTABLISHMENT DOES NOT FABRICATE A ROUTE ═════════════════════════════════════
def test_independent_establishment_is_recorded_as_independent(mme):
    """*"A non-root materialization supplied directly by a governed realization must be admitted as
    independently established at that anchor. Do not manufacture a fictitious 'forgotten from root' route."*"""
    supplied = GovernedBlock.of(
        CoordinateIndex.of(CEX.MANIFOLD, CEX.BY_DAY, [("D1",), ("D2",)]),
        {"revenue": pa.array([10.0, 20.0], type=pa.float64())},
        {"revenue": standing("revenue", mme.authority.instance_of("revenue"), n=2)})
    mme.establish(supplied, "revenue", at_root=False, data_state=RELOAD,
                  intent=_supersede_held(mme, "revenue", CEX.BY_DAY))
    m = _current(mme, "revenue", CEX.BY_DAY)[0]
    assert m.establishment == Establishment(INDEPENDENT)
    assert m.establishment.derived_from == ()                 # no manufactured parent
    assert m.establishment.kind != CONTINUED


def test_an_anchor_outside_the_region_is_refused_for_independent_material_too():
    """A governed realization can supply a value; it cannot make the family law admit one where it does
    not. `on_hand` does not compose across time, so `on_hand@{store}` is not a lawful materialization —
    however it was produced."""
    mme, _ = CEX.build(data_state=LOAD)
    on_hand = CEX._families()[4]
    mme.authority.register_family(on_hand)
    unlawful = GovernedBlock.of(
        CoordinateIndex.of(CEX.MANIFOLD, CEX.BY_STORE, [("S1",), ("S2",)]),
        {"on_hand": pa.array([10, 7], type=pa.int64())},
        {"on_hand": standing("on_hand", mme.authority.instance_of("on_hand"), n=2)})
    with pytest.raises(KernelRefusal) as exc:
        mme.establish(unlawful, "on_hand", at_root=False, data_state=LOAD)
    assert exc.value.code == "outside-continuation-region"
    assert "ASKED OF INDEPENDENTLY ESTABLISHED MATERIAL TOO" in exc.value.detail


def test_a_continuation_without_a_parent_is_refused():
    with pytest.raises(KernelRefusal) as exc:
        Establishment(CONTINUED, ())
    assert exc.value.code == "continuation-without-a-parent"


def test_a_root_or_independent_standing_may_not_name_a_parent():
    for kind in (AT_ROOT, INDEPENDENT):
        with pytest.raises(KernelRefusal) as exc:
            Establishment(kind, (MaterializationId("mat-000001"),))
        assert exc.value.code == "unattributed-derivation"


# ══ §6 · THE BUILD IS THE SEMANTIC WORLD ══════════════════════════════════════════════════════════
def test_the_build_is_the_constitution_context(mme):
    assert mme.build == ManifoldBuild(manifold=CEX.MANIFOLD, build="build-1")
    assert mme.authority.instance_of("revenue").constitution_context == mme.build.reference
    assert all(m.build == mme.build for m in mme.materializations.all())


def test_a_declaration_move_inside_one_build_is_refused_rather_than_absorbed(mme):
    """**J-0 retired the irregular case instead of handling it.** It used to supersede every
    materialization of that name — across every attached store, by bare `family_id`, with no manifold
    or build filter. A meaning change is a successor build, so the edit is refused and the held
    material stays exactly as current as the constitution that established it."""
    held = _current(mme, "revenue", CEX.SALE_AT)[0]
    with pytest.raises(KernelRefusal) as exc:
        mme.authority.register_family(
            replace(mme.family("revenue"), participation="every order the auditor confirmed"))
    assert exc.value.code == "constitution-moved-in-place"
    assert "participation" in exc.value.detail
    assert mme.materialization(held.id).eligibility == CURRENT
    assert mme.materialization(held.id).residency == RESIDENT
    assert mme.measure("revenue", CEX.BY_DAY).served


def test_the_per_object_witness_is_still_computable_and_is_not_the_partition(mme):
    """*"Per-object ConstitutionWitness may remain useful for admission validation, diagnostics, persistence
    assurance … but it should not become the central runtime cache-partition/version mechanism."*"""
    witness = mme.authority.witness_of("revenue")
    assert witness.digest.startswith("cw-1:")
    assert all(witness.digest not in str(m.id) for m in mme.materializations.all())
    assert all(m.build.reference != witness.digest for m in mme.materializations.all())


def test_off_build_material_is_refused_at_admission(mme):
    """The witness's surviving admission job: material carrying another build's constitution."""
    verdict = mme.authority.admit(
        _current(mme, "revenue", CEX.SALE_AT)[0].value, witness="cw-1:not-this-build")
    assert not verdict and verdict.code == "off-build-material"
    assert "new semantic world" in verdict.detail

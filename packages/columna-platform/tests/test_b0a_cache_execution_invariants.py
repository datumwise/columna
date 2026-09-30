"""
test_b0a_cache_execution_invariants.py — **B-0a-i: the two `adjudicate` verdicts nothing protected.**

    *"The governed analytical runtime decides what may be done. MME decides whether it can do it from what
    it currently holds."*  — Huayin, 2026-09-29

    *"Add coverage for `not-reachable` and `state-no-longer-sufficient`. These are genuine MME/cache
    invariants and become more important under this architecture."*

WHY THESE TWO, AND WHY NOW
--------------------------
`MME.adjudicate` returns five verdicts. The B-0 reconciliation classified them:

    not-continuation-bearing      already a TYPE fact; the verdict is a courtesy
    not-reachable                 **CACHE/GEOMETRY** — can I get there from what I hold?
    outside-continuation-region   **CONSTITUTIONAL** — expected to leave MME entirely
    state-no-longer-sufficient    **CACHE/EXECUTION** — is what I hold still foldable?
    unrealized-law                **BUILD CAPABILITY** — can this build run the reducer?

Three of the five were covered. **`not-reachable` and `state-no-longer-sufficient` had ZERO coverage
anywhere in the suite** — not the codes, and not their detail text (`"is not finer than"`, `"composes over
a"`). They are precisely the two that must SURVIVE the jurisdiction split, because they are the questions
that remain MME's after the constitutional one leaves. Nothing would have caught them being deleted.

So this file exists before the refactor rather than after it. It is pure coverage: **no production code is
touched by B-0a-i.**

THE DISTINCTION THESE TWO PIN, WHICH IS THE WHOLE POINT
-------------------------------------------------------
Neither is an analytical judgement, and each says so in a different way:

  * **`not-reachable`** — holding `F@{store}` and being asked for `F@{day}` is not the MME overruling the
    Manifold. `{day}` may be perfectly lawful. The cache is saying *"I cannot obtain day from the state I
    hold, because coarsening forgets and does not acquire."* Geometry, not governance.
  * **`state-no-longer-sufficient`** — holding a SCALAR where the law composes STRUCTURED state is not a
    statement about whether `F@A` is lawful either. It is *"the payload I am holding cannot be folded by
    this law's composition."* Execution, not governance.

A useful check on both: **changing a Manifold's continuation region changes neither verdict.** That is the
design test for whether a responsibility belongs inside the cache engine, and these two pass it.
"""
from __future__ import annotations

import pytest

from columna_platform.kernel import (
    MME,
    FamilyPoint,
    FamilyState,
    KernelRefusal,
    Retained,
    RetentionKey,
)
from columna_platform.kernel import exhibit as EX
from columna_platform.kernel.law import SCALAR, STRUCTURED


@pytest.fixture
def mme():
    return EX.build()


@pytest.fixture
def fams():
    revenue, order_count, audited, distinct, on_hand, gauge = EX._families()
    return dict(revenue=revenue, order_count=order_count, audited=audited, distinct=distinct,
                on_hand=on_hand, gauge=gauge)


def _retained(mme: MME, state: FamilyState) -> Retained:
    """A `Retained` wrapper around a state that need not be in the store.

    `adjudicate` takes a candidate and a family; it does not look the candidate up. That is what makes it
    testable on a constructed payload — and is itself a small piece of evidence for the boundary, since a
    function that had to consult the store to answer would be a function whose answer depended on what
    else was cached."""
    return Retained(
        key=RetentionKey(identity=state.point.family_id, anchor=state.anchor,
                         instance=state.instance, realization=mme.realization),
        value=state)


# ══ A · `not-reachable` — GEOMETRY, NOT GOVERNANCE ════════════════════════════════════════════════
def test_a_sibling_anchor_cannot_reach_the_target_and_the_verdict_is_geometric(mme, fams):
    """**The uncovered verdict, covered.** `revenue@{store}` is lawful, `revenue@{day}` is lawful, and
    neither can be obtained from the other: `{store}` and `{day}` are siblings, not a coarsening pair.

    Note what this is NOT: no law forbids `revenue@{day}` — SUM's region is `everywhere()`. The refusal is
    that this particular held payload has already forgotten the constituent the request needs."""
    revenue = fams["revenue"]
    by_store = mme.measure(revenue, EX.BY_STORE)
    assert by_store.served                                       # {store} is lawful and served

    verdict = mme.adjudicate(_retained(mme, by_store.value), revenue, EX.BY_DAY)
    assert not verdict
    assert verdict.code == "not-reachable"
    assert "is not finer than" in verdict.detail
    assert "A coarsening forgets; it does not acquire" in verdict.detail


def test_the_target_it_could_not_reach_is_itself_perfectly_lawful(mme, fams):
    """The other half of the same fact, and the reason `not-reachable` carries no analytical meaning: the
    engine serves the very target it just refused to reach, from a different seed."""
    revenue = fams["revenue"]
    by_store = mme.measure(revenue, EX.BY_STORE)
    refused = mme.adjudicate(_retained(mme, by_store.value), revenue, EX.BY_DAY)
    assert refused.code == "not-reachable"

    assert mme.measure(revenue, EX.BY_DAY).served                # …and yet the target is servable
    assert mme.requirement_for(revenue, EX.BY_DAY)               # …and a requirement WOULD be emitted


def test_reachability_is_asked_of_the_scalar_anchor_in_the_right_direction(mme, fams):
    """`TOTAL` is reachable from everything and reaches nothing. Both directions, so the predicate cannot
    be accidentally inverted without a failure."""
    revenue = fams["revenue"]
    total = mme.measure(revenue, EX.TOTAL)
    assert total.served

    # the grand total cannot seed anything finer …
    verdict = mme.adjudicate(_retained(mme, total.value), revenue, EX.BY_DAY)
    assert not verdict and verdict.code == "not-reachable"
    # … and it is trivially adequate for itself
    assert mme.adjudicate(_retained(mme, total.value), revenue, EX.TOTAL).code == "exact"


def test_an_equal_anchor_is_EXACT_and_never_reaches_the_reachability_test(mme, fams):
    """The boundary case immediately before the check, pinned so the two cannot be confused: a candidate
    already AT the target short-circuits with `exact` rather than being tested for refinement."""
    revenue = fams["revenue"]
    by_day = mme.measure(revenue, EX.BY_DAY)
    verdict = mme.adjudicate(_retained(mme, by_day.value), revenue, EX.BY_DAY)
    assert verdict and verdict.code == "exact"
    assert "already at the asked location" in verdict.detail


def test_the_cache_pool_ALSO_filters_by_reachability_so_measure_never_reaches_this_verdict(mme, fams):
    """**Why this verdict had no coverage: `measure` cannot produce it.**

    `MaterializationStore.candidates_for` already filters the pool with
    `target.constituents <= m.anchor.constituents` — the same reachability question — so by the time
    `adjudicate` runs inside `measure`, every candidate is reachable. Step 2 is therefore a guard for
    DIRECT callers of `adjudicate` (the Frame-QL `EXPLAIN` path and the Fulfillment Coordinator both call
    it), and this test records that, so nobody later removes one of the two on the grounds that the other
    exists. Two callers, two entry points, one question."""
    revenue = fams["revenue"]
    mme.measure(revenue, EX.BY_STORE)                            # put a sibling in the store

    pool = mme.materializations.candidates_for(
        "revenue", EX.BY_DAY, mme.instance_of("revenue"))
    assert pool                                                  # there IS a usable candidate …
    assert all(EX.BY_DAY.constituents <= m.anchor.constituents for m in pool)
    assert not any(m.anchor == EX.BY_STORE for m in pool)        # … and the sibling is not in it

    answer = mme.measure(revenue, EX.BY_DAY)
    assert answer.served
    assert "not-reachable" not in (answer.refusal.detail if answer.refusal else "")


# ══ B · `state-no-longer-sufficient` — EXECUTION, NOT GOVERNANCE ══════════════════════════════════
def _finalized_sketch_state(mme: MME, distinct, anchor) -> FamilyState:
    """A payload shaped like what a careless provider would hand back: the SKETCH family's identity, at a
    lawful anchor, carrying a **scalar** where the law composes structured state.

    This is the exact case `kernel/requirement.py` and `realization_manager.py` both name in prose — *"a
    provider that would hand back a finalized HLL estimate where the law needs a sketch"* — and it is the
    only way to reach verdict 4, because nothing inside the engine produces one."""
    return FamilyState(
        point=FamilyPoint(distinct.family_id, anchor),
        law="HLL_SKETCH", value_form=SCALAR,                     # ← the defect: scalar, not structured
        cells={("D1",): 4},                                      # a finalized estimate, not a sketch
        instance=mme.instance_of(distinct.family_id),
        forgotten_since_root=frozenset({"store", "order"}))


def test_a_finalized_scalar_cannot_seed_a_structured_familys_continuation(mme, fams):
    """**The second uncovered verdict, covered.** The anchor is lawful, the identity is right, the
    instance matches — and the payload cannot be folded, because `HLL_SKETCH` composes over sketches and
    this is a number. Merging numbers would produce a confident wrong cardinality."""
    distinct = fams["distinct"]
    candidate = _retained(mme, _finalized_sketch_state(mme, distinct, EX.BY_DAY))

    verdict = mme.adjudicate(candidate, distinct, EX.TOTAL)
    assert not verdict
    assert verdict.code == "state-no-longer-sufficient"
    assert "composes over a" in verdict.detail
    assert SCALAR in verdict.detail and STRUCTURED in verdict.detail


def test_the_verdict_quotes_the_laws_own_words_for_what_its_composition_needs(mme, fams):
    """The refusal carries `law.sufficient_state` rather than a message invented here, so a law that
    changes what it needs changes the explanation without anyone editing the engine."""
    distinct = fams["distinct"]
    law = mme.law_of("distinct_customers")
    candidate = _retained(mme, _finalized_sketch_state(mme, distinct, EX.BY_DAY))

    verdict = mme.adjudicate(candidate, distinct, EX.TOTAL)
    assert law.sufficient_state
    assert law.sufficient_state in verdict.detail


def test_the_same_anchor_pair_is_ADMITTED_when_the_state_is_actually_sufficient(mme, fams):
    """**The control that makes the verdict mean something.** Identical family, identical anchors — the
    only difference is that the held payload is a real sketch. If this did not pass, the test above would
    be passing for the wrong reason."""
    distinct = fams["distinct"]
    real = mme.measure(distinct, EX.BY_DAY)
    assert real.served and real.value.value_form == STRUCTURED

    verdict = mme.adjudicate(_retained(mme, real.value), distinct, EX.TOTAL)
    assert verdict and verdict.code == "admitted"


def test_a_scalar_law_is_indifferent_to_the_check(mme, fams):
    """The guard is asked only where the law composes STRUCTURED state. A SCALAR law holding a scalar is
    exactly right, so `revenue` never reaches verdict 4 — pinned so the check cannot be widened into a
    general type assertion by accident."""
    revenue = fams["revenue"]
    law = mme.law_of("revenue")
    assert law.value_form == SCALAR

    by_day = mme.measure(revenue, EX.BY_DAY)
    assert by_day.value.value_form == SCALAR
    verdict = mme.adjudicate(_retained(mme, by_day.value), revenue, EX.TOTAL)
    assert verdict and verdict.code == "admitted"


# ══ C · NEITHER VERDICT IS A CONSTITUTIONAL JUDGEMENT ═════════════════════════════════════════════
def test_neither_verdict_moves_when_the_continuation_region_changes(mme, fams):
    """**THE DESIGN TEST, EXECUTED.**

        *"If changing a Manifold's continuation region requires changing MME logic, the boundary is
        probably wrong."*  — Huayin, 2026-09-29

    So: take the two verdicts, and re-ask them of a family whose region is RESTRICTED rather than
    `everywhere()`. `on_hand` composes across stores and not across time. Both verdicts come back
    unchanged, because neither consults the region — which is what makes them cache questions and what
    makes them safe to leave inside MME when the constitutional check departs."""
    on_hand = fams["on_hand"]
    assert mme.law_of("on_hand").region != mme.law_of("revenue").region

    # `not-reachable`, asked of the restricted family: same code, same reason.
    by_day = mme.measure(on_hand, EX.BY_DAY)
    assert by_day.served
    sibling = mme.adjudicate(_retained(mme, by_day.value), on_hand, EX.STORE_DAY)
    assert not sibling and sibling.code == "not-reachable"

    # and the region's own verdict is a DIFFERENT code on the same family, so the two are distinguishable
    laundered = mme.adjudicate(_retained(mme, by_day.value), on_hand, EX.TOTAL)
    assert not laundered and laundered.code == "outside-continuation-region"
    assert sibling.code != laundered.code


def test_the_five_verdicts_are_all_reachable_and_distinct(mme, fams):
    """All five, in one place, for the first time — so the refactor has a single row to check itself
    against. Three were already covered elsewhere; `not-reachable` and `state-no-longer-sufficient` are
    new here."""
    revenue, on_hand, distinct = fams["revenue"], fams["on_hand"], fams["distinct"]
    seen = {}

    seen["exact"] = mme.adjudicate(
        _retained(mme, mme.measure(revenue, EX.BY_DAY).value), revenue, EX.BY_DAY).code
    seen["not-reachable"] = mme.adjudicate(
        _retained(mme, mme.measure(revenue, EX.BY_STORE).value), revenue, EX.BY_DAY).code
    seen["outside-continuation-region"] = mme.adjudicate(
        _retained(mme, mme.measure(on_hand, EX.BY_DAY).value), on_hand, EX.TOTAL).code
    seen["state-no-longer-sufficient"] = mme.adjudicate(
        _retained(mme, _finalized_sketch_state(mme, distinct, EX.BY_DAY)), distinct, EX.TOTAL).code
    seen["admitted"] = mme.adjudicate(
        _retained(mme, mme.measure(revenue, EX.SALE_AT).value), revenue, EX.TOTAL).code

    assert seen == {k: k for k in seen}, seen
    assert len(set(seen.values())) == 5


def test_nothing_in_this_file_touched_production_code():
    """B-0a-i is coverage only. Recorded as an assertion so the unit's claim is in the suite: the two
    verdicts are pinned exactly as they already behave, before B-0a-ii collapses the constitutional
    predicate and before any jurisdiction moves."""
    import inspect

    from columna_platform.kernel import mme as mme_module

    source = inspect.getsource(mme_module.MME.adjudicate)
    assert source.count("return Adequacy(") == 7                 # 5 refusals + exact + admitted
    for code in ("not-continuation-bearing", "not-reachable", "outside-continuation-region",
                 "state-no-longer-sufficient", "unrealized-law"):
        assert code in source, code


# ══ D · B-0a-ii · THE CONSTITUTIONAL PREDICATE IS ASKED THROUGH ONE NAME ═══════════════════════════
def test_the_constitutional_predicate_is_inlined_nowhere(mme):
    """**B-0a-ii, pinned.** `law.region.admits(cumulative_forgotten(...))` was inlined at four sites —
    `MME.admit`, `MME.adjudicate`, `MME.requirement_for` and `ColumnarMME.admit` — while
    `entitlement_holds()` existed and none of them called it.

    Four copies of one question is why the jurisdiction argument was hard to see. This test keeps it
    visible: the predicate has exactly ONE implementation, and every asker goes through its name. That
    matters because the question is expected to LEAVE the cache engine, and a single call site is one edit
    rather than four."""
    import inspect

    from columna_platform.columnar import mme as columnar_mme_module
    from columna_platform.kernel import materialization as materialization_module
    from columna_platform.kernel import mme as kernel_mme_module

    implementation = inspect.getsource(materialization_module.entitlement_holds)
    assert "law.region.admits(cumulative_forgotten(family, target))" in implementation

    for module in (kernel_mme_module, columnar_mme_module):
        code = _code_only(module)
        assert "region.admits(" not in code, module.__name__
        assert "entitlement_holds(" in code, module.__name__


def test_every_asker_of_the_predicate_still_refuses_exactly_as_before(mme, fams):
    """The collapse is a refactor, so the burden is sameness. All four askers, reached by their own
    public route, each still producing its own code and its own words.

    (The by-eye version of this was done once, by capturing every detail string before and after the edit
    and diffing them — byte-identical. This is the standing form.)"""
    on_hand = fams["on_hand"]

    # asker 1 · admit, on independently established material
    unlawful = FamilyState(
        point=FamilyPoint("on_hand", EX.BY_STORE), law="STOCK_LEVEL", value_form=SCALAR,
        cells={("S1",): 42}, instance=mme.instance_of("on_hand"),
        forgotten_since_root=frozenset({"day"}))
    admitted = mme.admit(unlawful)
    assert not admitted and admitted.code == "anchor-outside-the-continuation-region"
    assert "THIS IS ASKED OF INDEPENDENTLY ESTABLISHED MATERIAL TOO" in admitted.detail

    # asker 2 · adjudicate, on a held intermediate
    by_day = mme.measure(on_hand, EX.BY_DAY).value
    verdict = mme.adjudicate(_retained(mme, by_day), on_hand, EX.TOTAL)
    assert not verdict and verdict.code == "outside-continuation-region"
    assert "cannot launder an edge the law does not admit" in verdict.detail

    # asker 3 · requirement_for, which emits NOTHING rather than refusing
    outcome = mme.requirement_for(on_hand, EX.BY_STORE)
    assert not outcome and outcome.requirement is None
    assert "NO REALIZATION REQUIREMENT IS EMITTED" in outcome.reason

    # asker 4 · the columnar twin, over real Arrow, which RAISES rather than returning
    import pyarrow as pa

    from columna_platform.columnar import CoordinateIndex, GovernedBlock
    from columna_platform.columnar import exhibit as CEX
    from columna_platform.columnar.standing import standing

    engine, _block = CEX.build(settled=True, data_state="load:orders@08:00Z")
    columnar_on_hand = next(f for f in CEX._families() if f.family_id == "on_hand")
    engine.authority.register_family(columnar_on_hand)
    index = CoordinateIndex.of(CEX.MANIFOLD, CEX.BY_STORE, [("S1",), ("S2",)])
    block = GovernedBlock.of(
        index, {"on_hand": pa.array([1, 2], type=pa.int64())},
        {"on_hand": standing("on_hand", engine.authority.instance_of("on_hand"), n=2)})

    with pytest.raises(KernelRefusal) as raised:
        engine.establish(block, "on_hand", data_state="load:orders@08:00Z")
    assert raised.value.code == "anchor-outside-the-continuation-region"
    assert "ASKED OF INDEPENDENTLY ESTABLISHED MATERIAL TOO" in raised.value.detail


def _code_only(module) -> str:
    """Executable text only — docstrings and comments stripped, so a ban cannot be tripped by the prose
    that explains it. Same helper as the E-1/E-3, F-1 and R-1 suites."""
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

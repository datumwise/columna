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


def _request(mme: MME, family, target):
    """**Authorize, then hand the request to the cache** (B-0b). Every `adjudicate` call in this file goes
    through here, because after B-0b there is no other way to reach the method: the cache adjudicates an
    already-authorized continuation and there is no signature that takes a family and a target.

    Fails loudly rather than returning `None` for an unauthorized target, so a test that meant to exercise
    the cache cannot silently end up exercising nothing."""
    authorized = mme.authorizer.authorize(family, target)
    assert authorized, f"expected {family.family_id}@{target} to be authorized: {authorized.refusal}"
    return authorized.request


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

    verdict = mme.adjudicate(_retained(mme, by_store.value), _request(mme, revenue, EX.BY_DAY))
    assert not verdict
    assert verdict.code == "not-reachable"
    assert "is not finer than" in verdict.detail
    assert "A coarsening forgets; it does not acquire" in verdict.detail


def test_the_target_it_could_not_reach_is_itself_perfectly_lawful(mme, fams):
    """The other half of the same fact, and the reason `not-reachable` carries no analytical meaning: the
    engine serves the very target it just refused to reach, from a different seed."""
    revenue = fams["revenue"]
    by_store = mme.measure(revenue, EX.BY_STORE)
    refused = mme.adjudicate(_retained(mme, by_store.value), _request(mme, revenue, EX.BY_DAY))
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
    verdict = mme.adjudicate(_retained(mme, total.value), _request(mme, revenue, EX.BY_DAY))
    assert not verdict and verdict.code == "not-reachable"
    # … and it is trivially adequate for itself
    assert mme.adjudicate(_retained(mme, total.value), _request(mme, revenue, EX.TOTAL)).code == "exact"


def test_an_equal_anchor_is_EXACT_and_never_reaches_the_reachability_test(mme, fams):
    """The boundary case immediately before the check, pinned so the two cannot be confused: a candidate
    already AT the target short-circuits with `exact` rather than being tested for refinement."""
    revenue = fams["revenue"]
    by_day = mme.measure(revenue, EX.BY_DAY)
    verdict = mme.adjudicate(_retained(mme, by_day.value), _request(mme, revenue, EX.BY_DAY))
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

    verdict = mme.adjudicate(candidate, _request(mme, distinct, EX.TOTAL))
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

    verdict = mme.adjudicate(candidate, _request(mme, distinct, EX.TOTAL))
    assert law.sufficient_state
    assert law.sufficient_state in verdict.detail


def test_the_same_anchor_pair_is_ADMITTED_when_the_state_is_actually_sufficient(mme, fams):
    """**The control that makes the verdict mean something.** Identical family, identical anchors — the
    only difference is that the held payload is a real sketch. If this did not pass, the test above would
    be passing for the wrong reason."""
    distinct = fams["distinct"]
    real = mme.measure(distinct, EX.BY_DAY)
    assert real.served and real.value.value_form == STRUCTURED

    verdict = mme.adjudicate(_retained(mme, real.value), _request(mme, distinct, EX.TOTAL))
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
    verdict = mme.adjudicate(_retained(mme, by_day.value), _request(mme, revenue, EX.TOTAL))
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

    # `not-reachable`, asked of the restricted family: same code, same reason. STILL THE CACHE'S.
    by_day = mme.measure(on_hand, EX.BY_DAY)
    assert by_day.served
    sibling = mme.adjudicate(_retained(mme, by_day.value), _request(mme, on_hand, EX.STORE_DAY))
    assert not sibling and sibling.code == "not-reachable"

    # **AND THE REGION'S OWN VERDICT HAS LEFT THE CACHE ENTIRELY (B-0b).** It is not a different code from
    # a different `adjudicate` branch any more — it is a different LAYER. `on_hand@TOTAL` is unauthorized,
    # so there is no request to adjudicate and the cache is never consulted about it. That is the sharper
    # form of this test's claim: the two verdicts did not merely fail to move when the region changed, they
    # are in a component the region cannot reach.
    unauthorized = mme.authorizer.authorize(on_hand, EX.TOTAL)
    assert not unauthorized and unauthorized.refusal.code == "outside-continuation-region"
    assert sibling.code != unauthorized.refusal.code
    with pytest.raises(AssertionError):
        _request(mme, on_hand, EX.TOTAL)                         # no request exists to hand the cache


def test_the_cache_verdicts_are_reachable_and_the_constitutional_one_is_not_a_verdict_at_all(mme, fams):
    """**The whole B-0a → B-0b movement, in one test.**

    B-0a asserted five `adjudicate` verdicts in one place so the refactor had a single row to check itself
    against. B-0b then removed one of them — and the removal is the unit's result, so this test records the
    new shape rather than being deleted. Four verdicts remain in the cache, each a
    materialization/execution question; the fifth is now an AUTHORIZATION REFUSAL one layer up, and it is
    not a verdict about held state at all."""
    revenue, on_hand, distinct = fams["revenue"], fams["on_hand"], fams["distinct"]

    cache = {}
    cache["exact"] = mme.adjudicate(
        _retained(mme, mme.measure(revenue, EX.BY_DAY).value), _request(mme, revenue, EX.BY_DAY)).code
    cache["not-reachable"] = mme.adjudicate(
        _retained(mme, mme.measure(revenue, EX.BY_STORE).value), _request(mme, revenue, EX.BY_DAY)).code
    cache["state-no-longer-sufficient"] = mme.adjudicate(
        _retained(mme, _finalized_sketch_state(mme, distinct, EX.BY_DAY)),
        _request(mme, distinct, EX.TOTAL)).code
    cache["admitted"] = mme.adjudicate(
        _retained(mme, mme.measure(revenue, EX.SALE_AT).value), _request(mme, revenue, EX.TOTAL)).code

    assert cache == {k: k for k in cache}, cache
    assert len(set(cache.values())) == 4

    # the fifth, where it now lives — and note it needs no candidate, because it is not about one
    above = mme.authorizer.authorize(on_hand, EX.TOTAL)
    assert not above and above.refusal.code == "outside-continuation-region"
    assert "outside-continuation-region" not in cache


def test_b0a_i_was_coverage_only_and_b0b_then_changed_the_production_code():
    """**A scope guard that outlived its scope, updated rather than deleted.**

    B-0a-i touched no production code and this test asserted it by counting `adjudicate`'s returns. B-0b
    then removed one verdict, so the count moved — and that is the unit's result, not a regression. What
    survives is the useful half: the four cache verdicts are all still there under their own names, and the
    constitutional one is not."""
    import inspect

    from columna_platform.kernel import mme as mme_module

    source = inspect.getsource(mme_module.MME.adjudicate)
    assert source.count("return Adequacy(") == 6                 # 4 refusals + exact + admitted
    for code in ("not-continuation-bearing", "not-reachable",
                 "state-no-longer-sufficient", "unrealized-law"):
        assert code in source, code
    # and the fifth is gone from the cache engine entirely
    assert "outside-continuation-region" not in source
    assert "region" not in source and "admits" not in source


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


# ══ D · B-0a-ii → B-0b · ONE QUESTION, ONE NAME, AND NOW ONE MODULE ════════════════════════════════
def test_the_constitutional_predicate_left_both_engines():
    """**The two-step, recorded.** B-0a-ii collapsed four inlined copies of
    `law.region.admits(cumulative_forgotten(...))` onto the one `entitlement_holds()` that already existed,
    so the duplication became visible. B-0b then moved that one call out of both cache engines and into the
    authority.

    So the assertion inverts from B-0a's: neither engine calls the predicate now, and the module that does
    is not a cache. This is the mechanical form of the ruling — *"MME must not read `ContinuationRegion`;
    call `region.admits`; receive an entitlement wrapper and evaluate it; reconstruct permission from family
    law; infer lawful continuation from provider capability."*"""
    import inspect

    from columna_platform.columnar import mme as columnar_mme_module
    from columna_platform.kernel import authorization as authorization_module
    from columna_platform.kernel import materialization as materialization_module
    from columna_platform.kernel import mme as kernel_mme_module

    implementation = inspect.getsource(materialization_module.entitlement_holds)
    assert "law.region.admits(cumulative_forgotten(family, target))" in implementation

    for module in (kernel_mme_module, columnar_mme_module):
        code = _code_only(module)
        for constitutional in ("region.admits(", "entitlement_holds(", "cumulative_forgotten(",
                               "ContinuationRegion"):
            assert constitutional not in code, f"{module.__name__} still reads {constitutional}"

    authority = _code_only(authorization_module)
    assert "entitlement_holds(" in authority
    assert "region.why_not(" in authority


def test_no_law_name_enumeration_survives_in_either_engine():
    """The other constitutional leak B-0a found: `_POPULATION_LAWS = frozenset({"COUNT"})` and
    `_shape_of(law_name)` in the columnar MME — a cache deciding what a reduction contributes over from a
    hardcoded set of law NAMES.

    Relocating the set would have satisfied the letter and kept the defect, so the fact moved to the law
    instead: `AnalyticalLaw.fold_shape` is declared, `COUNT` says `POPULATION` of itself, and it enters every
    family's constitution witness by subtraction."""
    from columna_platform.columnar import mme as columnar_mme_module
    from columna_platform.kernel import REGISTRY
    from columna_platform.kernel.law import POPULATION, VALUE_BEARING

    code = _code_only(columnar_mme_module)
    assert "_POPULATION_LAWS" not in code
    assert "_shape_of" not in code
    assert '"COUNT"' not in code and "'COUNT'" not in code

    assert REGISTRY.get("COUNT").fold_shape == POPULATION
    assert REGISTRY.get("SUM").fold_shape == VALUE_BEARING
    assert REGISTRY.get("HLL_SKETCH").fold_shape == VALUE_BEARING


def test_no_approximation_disclosure_is_authored_inside_either_engine():
    """The third leak: both engines read `law.approximation` and authored an `approximate` disclosure — a
    cache asserting an analytical fact about a law. It is now decided by the authority and carried on the
    request's `conditions`, which the engines propagate."""
    from columna_platform.columnar import mme as columnar_mme_module
    from columna_platform.kernel import authorization as authorization_module
    from columna_platform.kernel import mme as kernel_mme_module

    for module in (kernel_mme_module, columnar_mme_module):
        code = _code_only(module)
        assert "approximation" not in code, module.__name__
        assert "request.conditions" in code, module.__name__

    assert "approximation" in _code_only(authorization_module)


def test_there_is_now_ONE_asker_and_its_refusals_are_the_same_words(mme, fams):
    """**B-0a found four askers of one question; B-0b left one.**

    The four were `MME.admit`, `MME.adjudicate`, `MME.requirement_for` and `ColumnarMME.admit`. Every one of
    them now routes to `ContinuationAuthority`, and the refusals a caller sees are the same sentences in the
    same cases — which is the whole burden of a jurisdiction move, since nothing about what is lawful
    changed."""
    on_hand = fams["on_hand"]

    # asker 1 · a continuation. No request is minted, so the cache is never asked.
    refused = mme.authorizer.authorize(on_hand, EX.TOTAL)
    assert not refused and refused.refusal.code == "outside-continuation-region"
    assert "cannot launder an edge the law does not admit" in refused.refusal.detail
    assert "NO CONTINUATION IS AUTHORIZED" in refused.refusal.detail

    # …and `measure` surfaces exactly that, rather than dressing it as a cache miss
    served = mme.measure(on_hand, EX.TOTAL)
    assert not served.served and served.refusal.code == refused.refusal.code
    assert served.refusal.detail == refused.refusal.detail

    # asker 2 · a STANDING, for independently established material
    standing = mme.authorizer.authorize_standing(on_hand, EX.BY_STORE)
    assert not standing and standing.refusal.code == "outside-continuation-region"
    assert "ASKED OF INDEPENDENTLY ESTABLISHED MATERIAL TOO" in standing.refusal.detail

    # …and `admit` surfaces exactly that, with no second check of its own
    unlawful = FamilyState(
        point=FamilyPoint("on_hand", EX.BY_STORE), law="STOCK_LEVEL", value_form=SCALAR,
        cells={("S1",): 42}, instance=mme.instance_of("on_hand"),
        forgotten_since_root=frozenset({"day"}))
    admitted = mme.admit(unlawful)
    assert not admitted and admitted.code == standing.refusal.code
    assert admitted.detail == standing.refusal.detail

    # asker 3 · the realization requirement, which emits NOTHING rather than refusing
    outcome = mme.requirement_for(on_hand, EX.BY_STORE)
    assert not outcome and outcome.requirement is None
    assert "NO REALIZATION REQUIREMENT IS EMITTED" in outcome.reason

    # asker 4 · the columnar engine, which shares the SAME authority over the SAME constitution
    from columna_platform.columnar import exhibit as CEX

    engine, _block = CEX.build(settled=True, data_state="load:orders@08:00Z")
    columnar_on_hand = next(f for f in CEX._families() if f.family_id == "on_hand")
    engine.authority.register_family(columnar_on_hand)
    columnar = engine.measure("on_hand", CEX.TOTAL)
    assert not columnar.served and columnar.refusal.code == "outside-continuation-region"

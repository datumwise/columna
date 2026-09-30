"""
test_kernel_mme.py — the v8-native Platform kernel's own suite.

    *"This parallel path should have its own Platform tests. Do NOT run the entire Core suite as the
    inner-loop gate for every Platform change."*
        — Huayin, 2026-09-28

So this file is the inner loop. It imports `columna_platform.kernel` and `datasketches` and nothing
else, and the first test in it measures that.

The five stop-condition proofs have their own sections. `exhibit.py` is the narrative version and is run
here too, because an exhibit that is not executed is a document.
"""
from __future__ import annotations

import pytest

from columna_platform.kernel import (
    CACHED,
    CONTINUED,
    EVALUATED,
    AnalyticalInstance,
    AnalyticalLaw,
    Composition,
    ContinuationRegion,
    ExpressionOutput,
    ExpressionPoint,
    FamilyPoint,
    FamilyState,
    GovernedExpression,
    KernelRefusal,
    MAP,
    MME,
    MeasureFamily,
    ORDERED,
    Operand,
    ProviderProfile,
    REDUCER,
    REGISTRY,
    ExpressionEvaluator,
    Realization,
    Retained,
    RetentionKey,
    RequiredBasis,
    STRUCTURED,
    SufficientBasis,
)
from columna_platform.kernel import builtins as B
from columna_platform.kernel import exhibit as EX


def _holding(mme, key):
    """One held object, by its descriptor — a descriptor REPORTS what is held; materializations are located
    by their opaque `MaterializationId`, so this is a search over attributes rather than a lookup."""
    return next(r for r in mme.holdings() if r.key == key)


@pytest.fixture
def mme():
    return EX.build()


@pytest.fixture
def evaluator(mme):
    """**The M-2 seam, as a fixture.** Expressions are served by an evaluator constructed OVER the engine;
    the engine has no `evaluate`. Every expression proof below goes through this object, and that it is a
    separate object is the unit's result rather than an inconvenience."""
    return ExpressionEvaluator(mme)


@pytest.fixture
def fams():
    revenue, order_count, audited, distinct, on_hand, gauge = EX._families()
    return dict(revenue=revenue, order_count=order_count, audited=audited, distinct=distinct,
                on_hand=on_hand, gauge=gauge)


@pytest.fixture
def exprs():
    aov, aov_audited, estimate = EX._expressions()
    return dict(aov=aov, aov_audited=aov_audited, estimate=estimate)


# ══ 0 · the boundary. A boundary nobody measures is a boundary that leaks. ════════════════════════
def test_the_kernel_imports_nothing_from_columna_core():
    """**THE ARCHITECTURAL CONSTRAINT, ENFORCED RATHER THAN INTENDED.**

    Ruled: the v8-native path must not depend semantically on `columna_core.governed.Family`, Core
    `LawView`/C1–C9, Core native publication v3.0/v3.1, Core generated-family doctrine, or Core
    `operators.py` classifications. A semantic dependency starts as an import, so the import is what is
    measured.

    **Checked over the AST, not over the text.** The first version of this test grepped for the string
    `columna_core` near the word `import` and failed on its own module docstrings — which say, in prose,
    that `columna_core.sketch` was read and not imported. A textual scan cannot tell an import from a
    sentence about one; `ast` can, and it is also the thing that cannot be fooled by a lazy import inside
    a function."""
    import ast
    import pathlib

    import columna_platform.kernel as pkg

    root = pathlib.Path(pkg.__file__).parent
    offenders = []
    for path in sorted(root.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                if name.split(".")[0] == "columna_core":
                    offenders.append(f"{path.name}:{node.lineno} imports {name}")
    assert not offenders, "the kernel must not import Core:\n" + "\n".join(offenders)


def test_the_kernel_does_not_reach_core_at_runtime_either():
    """The same constraint, measured DYNAMICALLY — a transitive or lazy import would satisfy the AST
    scan and fail here.

    **Run in a SUBPROCESS, and that is not incidental.** The first version called `importlib.reload` in
    this interpreter, which rebuilds every class in the reloaded modules — so `KernelRefusal` became a
    different object from the one this file imported, and seventeen unrelated `pytest.raises` assertions
    in this suite began failing for a reason that had nothing to do with what they test. A fresh
    interpreter is the only honest way to ask what an import pulls in."""
    import subprocess
    import sys

    probe = (
        "import sys;"
        "import columna_platform.kernel as k;"
        "from columna_platform.kernel import exhibit;"
        "exhibit.build();"
        "leaked = sorted(m for m in sys.modules if m.split('.')[0] == 'columna_core');"
        "print('LEAKED:' + ','.join(leaked));"
    )
    result = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "LEAKED:" in result.stdout, result.stdout
    leaked = result.stdout.split("LEAKED:")[1].strip()
    assert leaked == "", f"building a whole MME pulled in Core modules: {leaked}"


def test_the_kernel_reaches_exactly_one_third_party_algorithm_and_names_it():
    """`datasketches` — the Apache DataSketches HLL implementation. A third-party ALGORITHM, not an
    ontology, and the one piece of reuse in this package. Pinned so that a second dependency has to be
    a deliberate act."""
    import ast
    import pathlib

    import columna_platform.kernel as pkg

    external = set()
    # stdlib is not "external" in the sense this test guards: what it forbids is a THIRD-PARTY or Core
    # import. `hashlib` joined the list when the constitution witness became computed (P-1) — a digest
    # over identity-bearing governed facts, in-process and written nowhere.
    # `time` joined the list in M-2, when the family-request observation seam began stamping a wall
    # clock on each record. The kernel still holds no clock of its own for any ANALYTICAL purpose —
    # `time.time()` and `time.perf_counter_ns()` are read only for workload observation, which is
    # non-authoritative by construction (M-2 §4, §6).
    stdlib = {"__future__", "dataclasses", "typing", "math", "abc", "enum", "functools", "itertools",
              "hashlib", "time"}
    root = pathlib.Path(pkg.__file__).parent
    for path in sorted(root.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                top = node.module.split(".")[0]
                if top not in stdlib:
                    external.add(top)
            elif isinstance(node, ast.Import):
                for a in node.names:
                    top = a.name.split(".")[0]
                    if top not in stdlib:
                        external.add(top)
    assert external == {"datasketches"}, external


# ══ 1 · the law schema's three distinctions ═══════════════════════════════════════════════════════
def test_structural_kind_is_orthogonal_to_analytical_sort():
    """A REDUCER that founds a family, a REDUCER that cannot, a MAP that cannot, an ORDERED that does.
    Every combination that matters is present, so the orthogonality is a property of the vocabulary."""
    assert REGISTRY.get("HLL_SKETCH").kind == REDUCER
    assert REGISTRY.get("HLL_SKETCH").may_found_a_family
    assert REGISTRY.get("MEAN").kind == REDUCER
    assert not REGISTRY.get("MEAN").may_found_a_family
    assert REGISTRY.get("HLL_ESTIMATE").kind == MAP
    assert not REGISTRY.get("HLL_ESTIMATE").may_found_a_family
    assert REGISTRY.get("LAST").kind == ORDERED
    assert REGISTRY.get("LAST").may_found_a_family


def test_a_law_may_not_carry_both_establishment_routes():
    with pytest.raises(KernelRefusal) as exc:
        AnalyticalLaw(
            name="BOTH", kind=REDUCER, target_form="x", operand_domains=frozenset({"integer"}),
            result_domain="integer", value_form="scalar", sufficient_state="x",
            continuation=Composition("addition", True, True, True, "n"),
            required_basis=RequiredBasis(("SUM",), True, "n"))
    assert exc.value.code == "both-sorts"


def test_a_continuation_region_without_a_continuation_is_refused():
    with pytest.raises(KernelRefusal) as exc:
        AnalyticalLaw(name="R", kind=MAP, target_form="x", operand_domains=frozenset({"integer"}),
                      result_domain="integer", value_form="scalar", sufficient_state="x",
                      continuation=None,
                      region=ContinuationRegion.forgetting_only({"store"}, "n"))
    assert exc.value.code == "region-without-continuation"


def test_a_structured_family_law_must_name_its_finalization():
    with pytest.raises(KernelRefusal) as exc:
        AnalyticalLaw(name="S", kind=REDUCER, target_form="x",
                      operand_domains=frozenset({"text"}), result_domain="sketch",
                      value_form=STRUCTURED, sufficient_state="x",
                      continuation=Composition("sketch_union", True, True, True, "n"))
    assert exc.value.code == "structured-without-finalization"
    assert REGISTRY.get("HLL_SKETCH").finalized_by == "HLL_ESTIMATE"
    assert not REGISTRY.get("HLL_ESTIMATE").continuation_bearing


def test_sum_and_stock_level_share_a_composition_and_differ_only_in_region():
    """The fact a global `re_entrant` Boolean cannot carry, which is why `ContinuationRegion` exists."""
    a, b = REGISTRY.get("SUM"), REGISTRY.get("STOCK_LEVEL")
    assert a.continuation.token == b.continuation.token == "addition"
    assert a.region.forgettable is None
    assert b.region.forgettable == frozenset({"store"})
    assert B.IN_MEMORY.of("SUM").merge(2, 3) == B.IN_MEMORY.of("STOCK_LEVEL").merge(2, 3) == 5


# ══ 2 · constitution-time containment (ToD v8 §9.2) ═══════════════════════════════════════════════
def test_a_mean_family_is_not_a_constructible_object(mme):
    """**§9.2 as an impossibility, not a gate.** In Core this had to fire after resolution, over an
    object already constituted as a family. Here `MeasureFamily(law="MEAN")` has no reachable state."""
    with pytest.raises(KernelRefusal) as exc:
        mme.register_family(MeasureFamily(
            family_id="mean_order_value", manifold=EX.MANIFOLD, universe="commerce", root=EX.SALE_AT, law="MEAN",
            value_domain="decimal", participation=EX.PARTICIPATION, target="the mean"))
    assert exc.value.code == "not-a-family-law"
    assert "GOVERNED EXPRESSION" in exc.value.detail
    assert "does not make this value continuation-bearing" in exc.value.detail


def test_an_expression_over_a_continuation_bearing_law_is_refused(mme):
    with pytest.raises(KernelRefusal) as exc:
        mme.register_expression(GovernedExpression(
            expression_id="bad", manifold=EX.MANIFOLD, universe="commerce", constructor="SUM",
            operands=(Operand("operand", "revenue"),), participation=EX.PARTICIPATION))
    assert exc.value.code == "not-a-constructor"


def test_an_ordered_law_without_a_governed_order_is_refused(mme):
    with pytest.raises(KernelRefusal) as exc:
        mme.register_family(MeasureFamily(
            family_id="ungoverned", manifold=EX.MANIFOLD, universe="commerce", root=EX.STORE_DAY, law="LAST",
            value_domain="integer", participation="p", target="t"))
    assert exc.value.code == "order-not-governed"
    assert "picks one, which is a different and ungoverned act" in exc.value.detail


def test_a_familys_value_domain_is_its_own_value_not_its_operands(mme):
    with pytest.raises(KernelRefusal) as exc:
        mme.register_family(MeasureFamily(
            family_id="sketchy", manifold=EX.MANIFOLD, universe="commerce", root=EX.SALE_AT, law="HLL_SKETCH",
            value_domain="text", participation="p", target="t"))
    assert exc.value.code == "value-domain-mismatch"


def test_a_basis_may_not_relax_the_laws_participation_requirement(mme):
    with pytest.raises(KernelRefusal) as exc:
        mme.register_expression(GovernedExpression(
            expression_id="lax", manifold=EX.MANIFOLD, universe="commerce", constructor="MEAN",
            operands=(Operand("operand", "revenue"),), participation=EX.PARTICIPATION,
            admitted_bases=(SufficientBasis("b", {"SUM": "revenue", "COUNT": "order_count"}, False),)))
    assert exc.value.code == "basis-participation-requirement"
    assert "not a default a declaration may relax" in exc.value.detail


def test_one_route_declared_twice_is_not_two_alternatives(mme):
    with pytest.raises(KernelRefusal) as exc:
        mme.register_expression(GovernedExpression(
            expression_id="dupe", manifold=EX.MANIFOLD, universe="commerce", constructor="MEAN",
            operands=(Operand("operand", "revenue"),), participation=EX.PARTICIPATION,
            admitted_bases=(
                SufficientBasis("b1", {"SUM": "revenue", "COUNT": "order_count"}, True),
                SufficientBasis("b2", {"SUM": "revenue", "COUNT": "order_count"}, True))))
    assert exc.value.code == "duplicate-route"


# ══ PROOF 1 · additive family: root → lawful continuation → coarser family measure ════════════════
def test_proof_1_root_state_continues_to_a_coarser_family_measure(mme, fams):
    revenue = fams["revenue"]
    assert mme.measure(revenue, EX.SALE_AT).route == CACHED
    store_day = mme.measure(revenue, EX.STORE_DAY)
    assert store_day.route == CONTINUED
    assert store_day.value.cells[("D1", "S1")] == 100.0
    by_day = mme.measure(revenue, EX.BY_DAY)
    assert by_day.value.cells[("D1",)] == 175.0 and by_day.value.cells[("D2",)] == 325.0
    assert mme.measure(revenue, EX.TOTAL).cell() == 500.0


def test_a_NON_ROOT_materialization_may_seed_a_later_continuation(mme, fams):
    """The ruled distinction, and it is only observable because the engine prefers the LEAST-WORK seed.
    A root-first engine would be correct and would never exercise this right."""
    revenue = fams["revenue"]
    mme.measure(revenue, EX.STORE_DAY)
    by_day = mme.measure(revenue, EX.BY_DAY)
    assert by_day.seeded_from.anchor == EX.STORE_DAY
    assert not by_day.seeded_from.anchor == revenue.root
    total = mme.measure(revenue, EX.TOTAL)
    assert total.seeded_from.anchor == EX.BY_DAY          # a CHAIN of non-root continuations


def test_the_root_remains_the_canonical_origin_and_is_never_evicted_by_a_continuation(mme, fams):
    revenue = fams["revenue"]
    mme.measure(revenue, EX.TOTAL)
    assert any(k.identity == "revenue" and k.anchor == revenue.root for k in mme.held)
    assert mme.measure(revenue, revenue.root).route == CACHED


def test_a_family_with_no_established_root_is_unanswerable_and_nothing_is_invented(fams):
    m = MME(EX.COMMERCE, REGISTRY, B.IN_MEMORY, manifold=EX.MANIFOLD)
    m.register_family(fams["revenue"])
    answer = m.measure(fams["revenue"], EX.TOTAL)
    assert not answer.served
    assert "must be established at" in answer.refusal.detail


# ══ PROOF 1b · edge-relative closure, and the laundering guard ════════════════════════════════════
def test_a_stock_composes_across_stores_and_not_across_time(mme, fams):
    on_hand = fams["on_hand"]
    lawful = mme.measure(on_hand, EX.BY_DAY)
    assert lawful.served and lawful.value.cells[("D1",)] == 17 and lawful.value.cells[("D2",)] == 21
    unlawful = mme.measure(on_hand, EX.BY_STORE)
    assert not unlawful.served
    # **B-0b: the refusal is the AUTHORITY'S and carries the code as a code.** It used to arrive wrapped in
    # a cache miss whose detail recited the blocking code as text; an unlawful target is no longer a miss.
    assert unlawful.refusal.code == "outside-continuation-region"
    assert "its value closure does not extend to" in unlawful.refusal.detail


def test_an_intermediate_materialization_cannot_launder_an_inadmissible_edge(mme, fams):
    """**The subtle one.** Forgetting `{store}` then `{day}` forgets `{store, day}`. The one-step route
    is refused; the two-step route must be refused identically, or an intermediate becomes a way to
    obtain an answer the law forbids — and physical availability would have become analytical authority
    in the place it is hardest to see."""
    on_hand = fams["on_hand"]
    assert mme.measure(on_hand, EX.BY_DAY).served                # the intermediate IS lawful
    laundered = mme.measure(on_hand, EX.TOTAL)
    assert not laundered.served
    assert "cannot launder an edge the law does not admit" in laundered.refusal.detail
    # and the state it would have used is sitting in the store
    assert any(k.identity == "on_hand" and k.anchor == EX.BY_DAY for k in mme.held)


def test_the_guard_is_cumulative_and_not_per_hop(mme, fams):
    on_hand = fams["on_hand"]
    by_day = mme.measure(on_hand, EX.BY_DAY).value
    assert by_day.forgotten_since_root == frozenset({"store"})
    # **B-0b: THE REGION'S VERDICT MOVED OUT OF THE CACHE.** `on_hand@TOTAL` is not a lawful location,
    # so no continuation is AUTHORIZED and `adjudicate` is never reached — the guard is no longer a
    # check the cache applies but a request that cannot exist. The cumulative-not-per-hop property is
    # unchanged and is now asserted where it is computed.
    authorized = mme.authorizer.authorize(on_hand, EX.TOTAL)
    assert not authorized and authorized.refusal.code == "outside-continuation-region"
    assert "cannot launder an edge the law does not admit" in authorized.refusal.detail


# ══ PROOF 2 · structured family → merge → finalize as an EXPRESSION ═══════════════════════════════
def test_proof_2_a_sketch_family_merges_and_its_estimate_is_an_expression(mme, fams, exprs, evaluator):
    sketch_total = mme.measure(fams["distinct"], EX.TOTAL)
    assert sketch_total.route == CONTINUED
    assert sketch_total.value.value_form == STRUCTURED
    assert hasattr(sketch_total.cell(), "get_estimate")          # it is a sketch, not a number

    estimate = evaluator.evaluate(exprs["estimate"], EX.TOTAL)
    assert estimate.route == EVALUATED
    assert estimate.cell() == len({o["customer"] for o in EX.ORDERS}) == 4
    assert isinstance(estimate.value, ExpressionOutput)


def test_the_estimate_is_served_is_not_held_and_may_never_seed(mme, exprs, fams, evaluator):
    """**M-2 restates PROOF 5's other half on the flagship object, and STRENGTHENS it.**

    M-1 asserted two facts at once: the estimate is in the store, and it is refused as continuation state.
    M-2 removes the first: `E@A` is not cached at all (§1), so the claim becomes *served, not held, and
    still refused* — which is a strictly stronger statement about continuation, because there is now no
    object in the engine for anyone to mistake for family state."""
    expr = exprs["estimate"]
    served = evaluator.evaluate(expr, EX.TOTAL)
    assert served.served and served.route == EVALUATED

    # NOT HELD. Not by the store, and not by the engine's own reckoning of what it holds.
    assert all(k.identity != expr.expression_id for k in mme.held)
    assert not mme.materializations.select(expr.expression_id, eligibility=None)

    # ASKED AGAIN, IT IS EVALUATED AGAIN. There is no cache to hit.
    assert evaluator.evaluate(expr, EX.TOTAL).route == EVALUATED

    # OFFERED TO THE STORE, it is refused by a governed reason that names where it belongs.
    with pytest.raises(KernelRefusal) as offered:
        mme.retain(served.value)
    assert offered.value.code == "not-a-family-materialization"
    assert "ExpressionEvaluator" in offered.value.detail

    # OFFERED FROM ABOVE as a continuation candidate — the only route left by which an
    # `ExpressionOutput` can reach `adjudicate` — the sort verdict still refuses it by name.
    held = Retained(key=RetentionKey(identity=expr.expression_id, anchor=EX.TOTAL,
                                     instance=served.value.instance, realization=mme.realization),
                    value=served.value)
    assert not held.continuation_bearing
    verdict = mme.adjudicate(held, mme.authorizer.authorize(fams["distinct"], EX.TOTAL).request)
    assert not verdict and verdict.code == "not-continuation-bearing"
    assert "never becomes family continuation state" in verdict.detail


def test_the_type_is_the_primary_enforcement_and_the_verdict_is_the_explanation(mme, exprs):
    """`ExpressionOutput` has NO merge path — not one that refuses, none. The governed verdict exists so
    a caller learns which rule stopped them instead of what Python noticed."""
    assert hasattr(FamilyState, "fold_onto")
    assert not hasattr(ExpressionOutput, "fold_onto")
    assert FamilyState.CONTINUATION_BEARING is True
    assert ExpressionOutput.CONTINUATION_BEARING is False


def test_a_coarser_estimate_goes_back_through_the_sketch_never_through_estimates(mme, exprs, evaluator):
    evaluator.evaluate(exprs["estimate"], EX.BY_DAY)
    coarse = evaluator.evaluate(exprs["estimate"], EX.TOTAL)
    assert coarse.seeded_from == "b_sketch"                       # re-established from the basis


def test_the_approximation_rides_on_every_answer(mme, fams, exprs, evaluator):
    assert any(d.code == "approximate" for d in mme.measure(fams["distinct"], EX.TOTAL).disclosures)
    assert any(d.code == "approximate" for d in evaluator.evaluate(exprs["estimate"], EX.TOTAL).disclosures)
    assert B.hll_rse(12) < 0.02


# ══ PROOF 3 · cross-family expression from compatible operands ════════════════════════════════════
def test_proof_3_aov_is_established_from_revenue_and_order_count(mme, exprs, evaluator):
    aov = exprs["aov"]
    by_day = evaluator.evaluate(aov, EX.BY_DAY)
    assert by_day.route == EVALUATED
    assert by_day.value.cells[("D1",)] == pytest.approx(87.5)
    assert by_day.value.cells[("D2",)] == pytest.approx(81.25)
    total = evaluator.evaluate(aov, EX.TOTAL)
    assert total.cell() == pytest.approx(500 / 6)


def test_the_expression_is_not_a_mean_family_in_disguise(mme, exprs, evaluator):
    """The error a Mean family would have made, measured. The fixture is UNBALANCED (2 orders on D1, 4
    on D2) precisely so that this difference is not zero by coincidence."""
    by_day = evaluator.evaluate(exprs["aov"], EX.BY_DAY).value.cells
    mean_of_means = (by_day[("D1",)] + by_day[("D2",)]) / 2
    true_mean = evaluator.evaluate(exprs["aov"], EX.TOTAL).cell()
    assert true_mean == pytest.approx(500 / 6)
    assert mean_of_means == pytest.approx(84.375)
    assert abs(true_mean - mean_of_means) > 1.0


def test_the_two_operands_are_established_independently(mme, fams):
    rev = mme.measure(fams["revenue"], EX.BY_DAY)
    cnt = mme.measure(fams["order_count"], EX.BY_DAY)
    assert rev.served and cnt.served
    assert rev.value.instance.compatible_with(cnt.value.instance)


def test_an_expression_is_evaluated_never_continued(mme, exprs, evaluator):
    aov = exprs["aov"]
    evaluator.evaluate(aov, EX.SALE_AT)
    coarse = evaluator.evaluate(aov, EX.TOTAL)
    assert coarse.route == EVALUATED and coarse.seeded_from == "b_revenue_ordercount"


def test_an_expression_undefined_on_its_basis_says_so_rather_than_returning_zero():
    """ToD v8 §4.3: at `n = 0` the SUM/COUNT basis IS established — as `(0, 0)` — and the expression is
    UNDEFINED on it. Not an error, and not zero."""
    m = MME(EX.COMMERCE, REGISTRY, B.IN_MEMORY, manifold=EX.MANIFOLD)
    revenue, order_count, *_ = EX._families()
    m.register_family(revenue)
    m.register_family(order_count)
    aov, *_ = EX._expressions()
    m.register_expression(aov)
    rows = ({"store": "S1", "day": "D1", "order": "O1", "value": None},)
    m.establish_root(revenue, rows)
    m.establish_root(order_count, rows)
    answer = ExpressionEvaluator(m).evaluate(aov, EX.TOTAL)
    assert answer.served
    assert answer.value.cells == {}
    assert any(d.code == "undefined-on-basis" for d in answer.disclosures)


# ══ PROOF 4 · the same expression refusing an INCOMPATIBLE basis ══════════════════════════════════
def test_proof_4_an_incompatible_basis_is_refused_while_both_operands_exist(mme, fams, exprs, evaluator):
    """**The whole point: both operands are established, available, and individually valid.**"""
    rev = mme.measure(fams["revenue"], EX.BY_DAY)
    audited = mme.measure(fams["audited"], EX.BY_DAY)
    assert rev.served and audited.served                          # physically available

    refused = evaluator.evaluate(exprs["aov_audited"], EX.BY_DAY)
    assert not refused.served
    assert "different-participation" in refused.refusal.detail
    assert "jointly meaningless" in refused.refusal.detail
    assert "ESTABLISHED AND AVAILABLE" in refused.refusal.detail


def test_the_refusal_is_not_a_claim_that_the_operands_are_absent(mme, exprs, evaluator):
    refused = evaluator.evaluate(exprs["aov_audited"], EX.BY_DAY)
    assert "physical availability is not analytical authority" in refused.refusal.detail
    assert refused.refusal.code == "no-sufficient-basis-establishes"


def test_an_expression_admitting_no_basis_is_well_formed_and_not_evaluable(mme, evaluator):
    expr = mme.register_expression(GovernedExpression(
        expression_id="unrouted", manifold=EX.MANIFOLD, universe="commerce", constructor="MEAN",
        operands=(Operand("operand", "revenue"),), participation=EX.PARTICIPATION))
    answer = evaluator.evaluate(expr, EX.TOTAL)
    assert not answer.served and answer.refusal.code == "no-admitted-basis"
    assert "capability limit rather than a defect" in answer.refusal.detail


def test_a_named_basis_that_is_not_admitted_is_refused(mme, exprs, evaluator):
    answer = evaluator.evaluate(exprs["aov"], EX.TOTAL, basis_id="nope")
    assert not answer.served and answer.refusal.code == "no-admitted-basis"


# ══ PROOF 5, AS M-2 LEAVES IT · there is ONE store and it holds families ══════════════════════════
def test_proof_5_there_is_one_store_and_it_holds_family_materializations_only(mme, fams, exprs,
                                                                              evaluator):
    """M-1 proved two stores with different rights. **M-2 proves there is no second store** (§1), which is
    the stronger claim: an expression output is not held under weaker rights, it is not held."""
    mme.measure(fams["revenue"], EX.TOTAL)
    served = evaluator.evaluate(exprs["aov"], EX.TOTAL)
    assert served.served                                        # fully supported, just not from here

    held = list(mme.held)
    assert held                                                 # families ARE held
    assert all(mme.sort_of(k.identity) == "family" for k in held)
    assert not any(mme.sort_of(k.identity) == "expression" for k in held)

    # the expression is CONSTITUTED by this engine and MATERIALIZED nowhere in it
    assert "average_order_value" in mme.expressions
    assert mme.sort_of("average_order_value") == "expression"
    assert not mme.materializations.select("average_order_value", eligibility=None)

    # every held state may be asked to seed; at least one may and at least one may not
    verdicts = []
    for key in held:
        if key.anchor.is_scalar:
            continue
        target = EX.COMMERCE.anchor(sorted(key.anchor.constituents)[1:])
        _auth = mme.authorizer.authorize(mme.family(key.identity), target)
        verdicts.append(bool(_auth) and bool(mme.adjudicate(_holding(mme, key), _auth.request)))
    assert any(verdicts) and not all(verdicts)


def test_retention_key_sort_is_retired_and_the_sort_distinction_is_not(mme, fams, exprs, evaluator):
    """Ruled §2: *"assess whether M-2 now allows retirement of `RetentionKey.sort`."* It does — and the
    thing the field existed to protect is protected by the type and by `adjudicate` instead."""
    from dataclasses import fields

    # RETIRED as a field: nothing can construct a key claiming another sort.
    assert "sort" not in {f.name for f in fields(RetentionKey)}
    assert RetentionKey.sort == "family"
    assert all(k.sort == "family" for k in mme.held)

    # NOT RETIRED as a distinction: the two sorts are still two types with two sets of rights.
    revenue_state = mme.measure(fams["revenue"], EX.TOTAL).value
    estimate = evaluator.evaluate(exprs["estimate"], EX.TOTAL).value
    assert revenue_state.point.sort == "family" and estimate.point.sort == "expression"
    assert hasattr(revenue_state, "fold_onto") and not hasattr(estimate, "fold_onto")
    assert mme.sort_of("revenue") == "family" and mme.sort_of("average_order_value") == "expression"


def test_the_retention_key_distinguishes_sort_identity_anchor_instance_and_provider(mme, fams):
    revenue = fams["revenue"]
    state = mme.measure(revenue, EX.BY_DAY).value
    held = mme.retained(state.point, state.instance)
    assert held.key.sort == "family" and held.key.identity == "revenue"
    assert held.key.anchor == EX.BY_DAY and held.key.provider == "in-memory"
    # a DIFFERENT analytical instance is a different retained object, never a silent overwrite
    other = AnalyticalInstance(manifold=EX.MANIFOLD, universe="commerce",
                               participation="something else")
    assert mme.retained(state.point, other) is None


def test_a_family_point_and_an_expression_point_are_peers_not_one_widened_type():
    f, e = FamilyPoint("x", EX.TOTAL), ExpressionPoint("x", EX.TOTAL)
    assert f.sort == "family" and e.sort == "expression"
    assert type(f) is not type(e)
    assert not hasattr(f, "expression_id") and not hasattr(e, "family_id")


def test_sort_of_answers_the_dispatch_question_before_the_call(mme):
    assert mme.sort_of("revenue") == "family"
    assert mme.sort_of("average_order_value") == "expression"
    assert mme.sort_of("nothing") is None


# ══ PROOF 6 · ordered family ══════════════════════════════════════════════════════════════════════
def test_proof_6_last_continues_by_governed_order(mme, fams):
    gauge = fams["gauge"]
    root = mme.measure(gauge, EX.STORE_DAY)
    assert root.value.cells[("D1", "S1")] == ("17:00", 5)         # the key rides with the witness
    by_store = mme.measure(gauge, EX.BY_STORE)
    assert B.witness_value(by_store.value.cells[("S1",)]) == 5    # D1 17:00 beats D2 09:00 by ORDER
    assert B.witness_value(by_store.value.cells[("S2",)]) == 1


def test_a_known_empty_witness_is_a_standing_and_not_an_absence():
    empty = B.IN_MEMORY.of("LAST").contribute([], {"order_by": "recorded_at", "rows": ()})
    assert empty == B.KNOWN_EMPTY
    assert B.witness_value(empty) is None
    assert not REGISTRY.get("LAST").continuation.has_identity
    merge = B.IN_MEMORY.of("LAST").merge
    assert merge(B.KNOWN_EMPTY, ("08:00", 3)) == ("08:00", 3)
    assert merge(("08:00", 3), B.KNOWN_EMPTY) == ("08:00", 3)
    assert merge(B.KNOWN_EMPTY, B.KNOWN_EMPTY) == B.KNOWN_EMPTY


# ══ realization, invalidation, and the geometry's own rules ═══════════════════════════════════════
def test_a_backends_inability_does_not_remove_a_law(mme, exprs):
    thin = MME(EX.COMMERCE, REGISTRY, B.NO_MEAN, manifold=EX.MANIFOLD)
    revenue, order_count, *_ = EX._families()
    thin.register_family(revenue)
    thin.register_family(order_count)
    thin.register_expression(exprs["aov"])
    thin.establish_root(revenue, EX.ORDERS)
    thin.establish_root(order_count, EX.ORDERS)
    with pytest.raises(KernelRefusal) as exc:
        ExpressionEvaluator(thin).evaluate(exprs["aov"], EX.TOTAL)
    assert exc.value.code in ("unrealized-law", "unrealized-capability")
    assert "does not remove a law" in exc.value.detail or "is unchanged" in exc.value.detail
    assert "MEAN" in REGISTRY.vocabulary or REGISTRY.get("MEAN") is not None   # the law is intact


def test_invalidation_is_conservative_and_rebuild_is_from_the_root(mme, fams):
    revenue = fams["revenue"]
    mme.measure(revenue, EX.TOTAL)
    dropped = mme.invalidate("revenue")
    assert dropped
    assert not mme.measure(revenue, EX.TOTAL).served
    mme.establish_root(revenue, EX.ORDERS)
    assert mme.measure(revenue, EX.TOTAL).cell() == 500.0


def test_no_delta_retraction_exists_to_be_called(mme):
    for forbidden in ("retract", "subtract", "delete_contribution", "unmerge"):
        assert not hasattr(mme, forbidden)


def test_an_anchor_is_a_constituent_set_so_synonyms_cannot_exist():
    a = EX.COMMERCE.anchor({"store", "day"})
    b = EX.COMMERCE.anchor(["day", "store"])
    assert a == b and hash(a) == hash(b)


def test_a_coarsening_forgets_and_does_not_acquire():
    with pytest.raises(KernelRefusal) as exc:
        EX.BY_DAY.forgets(EX.STORE_DAY)
    assert exc.value.code == "not-a-coarsening"


def test_an_unknown_constituent_refuses_rather_than_being_created():
    with pytest.raises(KernelRefusal) as exc:
        EX.COMMERCE.anchor({"store", "region"})
    assert exc.value.code == "unknown-constituent"


def test_a_contribution_with_no_governed_location_refuses():
    with pytest.raises(KernelRefusal) as exc:
        EX.COMMERCE.cell_of(EX.SALE_AT, {"store": "S1", "day": "D1"})
    assert exc.value.code == "unlocated-contribution"
    assert "There is no default coordinate" in exc.value.detail


def test_an_unknown_law_is_never_substituted():
    with pytest.raises(KernelRefusal) as exc:
        REGISTRY.get("MEDIAN")
    assert exc.value.code == "unknown-law"
    assert "will not substitute one of its own" in exc.value.detail


def test_a_provider_may_not_realize_one_law_twice():
    with pytest.raises(KernelRefusal) as exc:
        ProviderProfile("x", (Realization(law="SUM"), Realization(law="SUM")))
    assert exc.value.code == "duplicate-realization"


# ══ the exhibit runs, and every one of its checks holds ═══════════════════════════════════════════
def test_the_exhibit_runs_green(capsys):
    """An exhibit that is not executed is a document. This is the stop condition, asserted."""
    assert EX.main() == 0
    out = capsys.readouterr().out
    assert "ALL CHECKS PASSED" in out
    assert "✗" not in out
    for proof in ("PROOF 1 ·", "PROOF 1b ·", "PROOF 2 ·", "PROOF 3 ·", "PROOF 4 ·", "PROOF 5 ·",
                  "PROOF 6 ·"):
        assert proof in out

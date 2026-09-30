"""
test_columnar_substrate.py — the v8-native MME executing over Arrow/DataFusion columnar state.

    *"Stop at executing columnar state through the MME."* — Huayin, 2026-09-28

The ten stop conditions are the ten sections. `exhibit.py` is the narrative version and is run here too.
"""
from __future__ import annotations

import ast
import pathlib

import pyarrow as pa
import pytest

from columna_platform.columnar import exhibit as EX
from columna_platform.columnar import (
    ColumnarExpressionOutput,
    ColumnarFamilyState,
    ColumnarMME,
    ColumnStanding,
    CoordinateIndex,
    GovernedBlock,
    POPULATION,
    VALUE_BEARING,
    standing,
)
from columna_platform.columnar.provider import HLL_PRECISION, estimate_of, sketch_of
from columna_platform.kernel import MME, REGISTRY, KernelRefusal
from columna_platform.kernel.materialization import SUPERSEDE, TransitionIntent
from columna_platform.kernel.builtins import IN_MEMORY
from columna_platform.kernel.mme import MME as KernelMME
from columna_platform.kernel.mme import Retained, RetentionKey
from columna_platform.columnar.expression import ColumnarExpressionEvaluator


@pytest.fixture
def built():
    return EX.build()


@pytest.fixture
def mme(built):
    return built[0]


@pytest.fixture
def evaluator(mme):
    return ColumnarExpressionEvaluator(mme)


@pytest.fixture
def settled_evaluator(settled):
    return ColumnarExpressionEvaluator(settled)


@pytest.fixture
def block(built):
    return built[1]


@pytest.fixture
def settled_built():
    """**The control world.** The same seven orders, with O7's amount supplied — one support bit apart
    from `built`. Every value-bearing proof runs here, because in the as-recorded world a value-bearing
    reduction over O7's participating domain is REFUSED rather than folded (ruled 2026-09-29)."""
    return EX.build(settled=True)


@pytest.fixture
def settled(settled_built):
    return settled_built[0]


@pytest.fixture
def settled_block(settled_built):
    return settled_built[1]


def _sources():
    import columna_platform.columnar as pkg

    return sorted(pathlib.Path(pkg.__file__).parent.glob("*.py"))


# ══ 0 · BOUNDARIES ════════════════════════════════════════════════════════════════════════════════
def test_the_columnar_layer_imports_no_core_semantic_module():
    """*"Add boundary tests ensuring the new columnar execution layer does not import Core semantics."*"""
    offenders = []
    for path in _sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = ([a.name for a in node.names] if isinstance(node, ast.Import)
                     else [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            offenders += [f"{path.name}:{node.lineno} {n}" for n in names
                          if n.split(".")[0] == "columna_core"]
    assert not offenders, "\n".join(offenders)


def test_the_columnar_layer_reaches_core_at_runtime_nowhere():
    import subprocess
    import sys

    probe = ("import sys;"
             "from columna_platform.columnar import exhibit;"
             "exhibit.build();"
             "print('LEAKED:' + ','.join(sorted(m for m in sys.modules "
             "if m.split('.')[0] == 'columna_core')))")
    result = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.split("LEAKED:")[1].strip() == "", result.stdout


def test_the_kernel_itself_is_still_core_free():
    import columna_platform.kernel as pkg

    for path in sorted(pathlib.Path(pkg.__file__).parent.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = ([a.name for a in node.names] if isinstance(node, ast.Import)
                     else [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            assert not [n for n in names if n.split(".")[0] == "columna_core"], path.name


# ══ 9 · NO RELATIONAL DISCOVERY OF ALIGNMENT ══════════════════════════════════════════════════════
def test_no_join_and_no_generated_sql_in_the_columnar_path():
    """**THE GOVERNING PHYSICAL RULE**, enforced over the AST rather than by review: *"MME does not
    discover analytical alignment by joining analytical tables."*

    Checked as method CALLS, so a docstring saying the word `join` cannot fail it and a real
    `df.join(...)` cannot hide in one."""
    offenders = []
    for path in _sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            attr = node.func.attr
            if attr in ("sql", "join_on", "register_table", "from_pandas"):
                offenders.append(f"{path.name}:{node.lineno} .{attr}()")
            elif attr == "join":
                # `", ".join(...)` is a STRING join and is not a relational one. The receiver being a
                # string literal is what tells them apart, and it is the only form this package uses.
                receiver = node.func.value
                is_string_join = (isinstance(receiver, ast.Constant)
                                  and isinstance(receiver.value, str))
                if not is_string_join:
                    offenders.append(f"{path.name}:{node.lineno} .join() on a non-string receiver")
    assert not offenders, "\n".join(offenders)


def test_alignment_is_a_reindex_that_refuses_an_invented_point(mme):
    """The refusal that makes it a reindex and not a join: a join would have accepted the extra row as a
    correspondence it discovered."""
    index = CoordinateIndex.of(EX.MANIFOLD, EX.BY_DAY, [("D1",)])
    with pytest.raises(KernelRefusal) as exc:
        mme.provider.align_onto({("D1",): 1.0, ("D9",): 2.0}, index)
    assert exc.value.code == "provider-invented-a-point"
    assert "a join would have accepted these rows" in exc.value.detail


def test_alignment_refuses_a_target_point_the_reduction_did_not_produce(mme):
    index = CoordinateIndex.of(EX.MANIFOLD, EX.BY_DAY, [("D1",), ("D2",)])
    with pytest.raises(KernelRefusal) as exc:
        mme.provider.align_onto({("D1",): 1.0}, index)
    assert exc.value.code == "target-point-unproduced"
    assert "Nothing is zero-filled" in exc.value.detail


def test_the_alignment_is_reported_in_the_route(settled):
    route = settled.measure("revenue", EX.BY_DAY).value.route
    assert any("align:" in s and "not a join on keys" in s for s in route)


# ══ 1 · REAL ARROW STATE AT A GOVERNED ANCHOR INSTANCE ════════════════════════════════════════════
def test_the_block_is_real_arrow_over_a_sparse_governed_index(block):
    assert isinstance(block.batch, pa.RecordBatch)
    assert block.batch.num_rows == len(block.index) == 7
    assert set(block.index.anchor.order) <= set(block.batch.schema.names)
    assert block.column("revenue").type == pa.float64()
    assert block.column("distinct_customers").type == pa.binary()


def test_sparse_geometry_stays_sparse(block):
    """`{store, day, order}` is not a Cartesian product and this representation cannot make it one."""
    assert len(block.index) == 7 < 2 * 2 * 7
    with pytest.raises(KernelRefusal) as exc:
        block.index.position(("D1", "O99", "S1"))
    assert exc.value.code == "coordinate-not-in-index"
    assert "sparse geometry stays sparse" in exc.value.detail


def test_a_duplicate_coordinate_is_refused_because_it_would_double_count():
    with pytest.raises(KernelRefusal) as exc:
        CoordinateIndex(manifold="m", anchor=EX.BY_DAY, coordinates=(("D1",), ("D1",)))
    assert exc.value.code == "duplicate-coordinate"


def test_the_index_identity_is_local_and_not_a_universal_point_id():
    a = CoordinateIndex.of("m1", EX.BY_DAY, [("D1",)])
    b = CoordinateIndex.of("m2", EX.BY_DAY, [("D1",)])
    assert a.identity != b.identity            # the Manifold is in the digest
    assert a.identity == CoordinateIndex.of("m1", EX.BY_DAY, [("D1",)]).identity


def test_co_location_confers_nothing(block):
    """*"Two columns in the same Arrow RecordBatch are not analytically compatible merely because they
    are co-located."* Proved on ONE batch, at identical positions."""
    verdict = block.compatibility_of("revenue", "audited_order_count")
    assert not verdict and verdict.code == "different-participation"
    assert block.standing("revenue").instance != block.standing("audited_order_count").instance
    assert len(block.standing("revenue")) == len(block.standing("audited_order_count"))


def test_a_value_column_without_a_governed_standing_is_unusable(block):
    with pytest.raises(KernelRefusal) as exc:
        block.standing("nope")
    assert exc.value.code == "no-standing-for-column"
    assert "Arrow nullability carries no ToD standing" in exc.value.detail


# ══ 8 · STANDING INDEPENDENT OF ARROW NULL ════════════════════════════════════════════════════════
def test_participation_is_known_independently_of_value_presence(block):
    position = block.index.position(("D1", "O7", "S1"))
    assert block.column("revenue")[position].as_py() is None          # Arrow null
    assert block.standing("revenue").participation[position].as_py() is True
    assert block.standing("revenue").support[position].as_py() is False
    assert block.standing("order_count").participation[position].as_py() is True


def test_count_is_not_count_of_non_null_revenue(block, mme):
    revenue = block.column("revenue")
    assert revenue.null_count == 1
    assert sum(block.contributing_domain("order_count", POPULATION).to_pylist()) == 7
    counts = mme.measure("order_count", EX.BY_DAY).value
    assert counts.cell(("D1",)) == 3                       # O1, O4 AND O7
    assert counts.cell(("D2",)) == 4


# ══ THE 2026-09-29 CORRECTION ═════════════════════════════════════════════════════════════════════
# *"Participation determines the contributing domain. Support determines whether the values required
# over that participating domain are established."*
def test_support_does_not_shrink_the_contributing_domain(block):
    """**The error this section exists to prevent.** The value-bearing domain is participation — all
    seven — and the unsupported point is IN it, reported as want of state rather than removed."""
    position = block.index.position(EX.UNSUPPORTED_POINT)
    st = block.standing("revenue")
    assert sum(block.contributing_domain("revenue", VALUE_BEARING).to_pylist()) == 7
    assert block.contributing_domain("revenue", VALUE_BEARING)[position].as_py() is True
    assert st.participation[position].as_py() is True and st.support[position].as_py() is False
    assert block.want_of_state("revenue", VALUE_BEARING)[position].as_py() is True
    assert st.positions_wanting_state(VALUE_BEARING) == (position,)
    # and `participation ∧ support` — the retired filter — would have given SIX
    assert sum(1 for a, b in zip(st.participation.to_pylist(), st.support.to_pylist())
               if a and b) == 6


def test_a_population_reduction_requires_no_value_and_never_wants_state(block):
    """Count remains independent: three participating Orders are three Orders."""
    assert not block.wants_state("order_count", POPULATION)
    assert not any(block.want_of_state("revenue", POPULATION).to_pylist())
    assert sum(block.contributing_domain("order_count", POPULATION).to_pylist()) == 7


def test_the_retired_contribution_filter_refuses_rather_than_returning_the_old_mask(block):
    with pytest.raises(KernelRefusal) as exc:
        block.standing("revenue").contributing_for(VALUE_BEARING)
    assert exc.value.code == "retired-contribution-filter"
    assert "validates it" in exc.value.detail


def test_the_canonical_case_count_serves_revenue_wants_state_aov_refuses(mme, evaluator):
    """**THE CANONICAL TEST** (Huayin, 2026-09-29). Three Orders participate at D1; one participating
    Revenue is unsupported. `OrderCount` = 3. `Revenue` refuses. `AOV` refuses because one required
    basis operand is not established."""
    assert len([o for o in EX.ORDERS if o["day"] == "D1"]) == 3

    counts = mme.measure("order_count", EX.BY_DAY)
    assert counts.served and counts.value.cell(("D1",)) == 3

    revenue = mme.measure("revenue", EX.BY_DAY)
    assert not revenue.served
    assert revenue.refusal.code == "want-of-state"
    assert "O7" in revenue.refusal.detail
    assert "THE REDUCTION HAS NOT RUN" in revenue.refusal.detail
    assert "does not shrink it" in revenue.refusal.detail

    aov = evaluator.evaluate("average_order_value", EX.BY_DAY)
    assert not aov.served and aov.value is None
    assert "role 'SUM'" in aov.refusal.detail and "want of state" in aov.refusal.detail


def test_nothing_is_inferred_from_support_not_na_not_empty_not_nonparticipation(mme):
    """*"Do not infer `NA`, known-empty, or nonparticipation from support."*"""
    detail = mme.measure("revenue", EX.BY_DAY).refusal.detail
    for disclaimed in ("not `NA`", "not a known-empty fibre", "not nonparticipation",
                       "not a nonexistent point"):
        assert disclaimed in detail
    # the point is still counted by the population reduction, which is the operative proof that it was
    # not read as nonparticipation
    assert mme.measure("order_count", EX.BY_DAY).value.cell(("D1",)) == 3


def test_the_expression_refuses_at_the_root_anchor_on_its_own_basis_check(mme, evaluator):
    """At the root both operands are held, so no continuation intervenes: the refusal is the expression
    path's own, and it names the unestablished operand rather than dividing around it."""
    aov = evaluator.evaluate("average_order_value", EX.SALE_AT)
    assert not aov.served
    assert "basis-operand-wants-state" in aov.refusal.detail
    assert "THE ARITHMETIC HAS NOT RUN" in aov.refusal.detail
    assert "NOT evaluated over the subset" in aov.refusal.detail
    # and NOT as §4.3 undefined-on-basis, which is a different fact about an established basis
    assert "UNDEFINED" not in aov.refusal.detail


def test_a_held_state_may_want_state_and_discloses_it_rather_than_hiding_it(mme):
    """Recording a column is not serving a value."""
    held = mme.retained("revenue", EX.SALE_AT,
                        mme.authority.instance_of("revenue")).value
    assert held.wants_state
    assert held.points_wanting_state() == (EX.UNSUPPORTED_POINT,)
    assert any(d.code == "want-of-state" for d in held.disclosures)


def test_reading_a_cell_at_a_point_with_want_of_state_refuses(mme):
    held = mme.retained("revenue", EX.SALE_AT,
                        mme.authority.instance_of("revenue")).value
    assert held.cell(("D1", "O1", "S1")) == 100.0
    with pytest.raises(KernelRefusal) as exc:
        held.cell(EX.UNSUPPORTED_POINT)
    assert exc.value.code == "want-of-state-at-a-point"
    assert "The carrier's null at this position means nothing" in exc.value.detail


def test_one_support_bit_is_the_whole_difference(mme, settled):
    """The control. The same seven orders, the same law, the same layout — one support bit apart."""
    assert not mme.measure("revenue", EX.BY_DAY).served
    served = settled.measure("revenue", EX.BY_DAY)
    assert served.served and served.value.cell(("D1",)) == 235.0
    # and the population reduction is IDENTICAL in both worlds, which is the point of the two masks
    assert (mme.measure("order_count", EX.BY_DAY).value.cell(("D1",))
            == settled.measure("order_count", EX.BY_DAY).value.cell(("D1",)) == 3)


def test_arrow_validity_and_the_support_mask_may_disagree_and_the_mask_wins(mme):
    """**A support mask matters even when the Arrow value array contains NO NULLS.** Three non-null
    values, one participating position unsupported. The effect is REFUSAL — want of state for a required
    contribution — and not silent exclusion: the old behaviour folded the two it believed and served
    30.0 as though the third point had never participated."""
    index = CoordinateIndex.of(EX.MANIFOLD, EX.SALE_AT,
                               [("D1", "O1", "S1"), ("D1", "O2", "S1"), ("D1", "O3", "S1")])
    block = GovernedBlock.of(
        index, {"revenue": pa.array([10.0, 20.0, 30.0], type=pa.float64())},
        {"revenue": standing("revenue", mme.authority.instance_of("revenue"), n=3,
                             support=[True, True, False])})
    assert block.column("revenue").null_count == 0          # NO nulls at all
    assert sum(block.contributing_domain("revenue", VALUE_BEARING).to_pylist()) == 3
    # REPLACING a family's root state is a SUPERSESSION and must say so (MME v1): offering a different
    # value for one analytical slot without transition intent is a consistency failure, not an overwrite.
    held = mme.materializations.select("revenue", anchor=EX.SALE_AT)
    mme.establish(block, "revenue",
                  intent=TransitionIntent(SUPERSEDE, tuple(m.id for m in held)))

    answer = mme.measure("revenue", EX.BY_DAY)
    assert not answer.served and answer.refusal.code == "want-of-state"
    assert "THE REDUCTION HAS NOT RUN" in answer.refusal.detail
    assert answer.value is None                             # not 30.0, and not 60.0


def test_a_provider_handed_an_unestablished_domain_refuses_rather_than_folding_around_it(mme, block):
    """A backstop, not a judgment: if the kernel's want-of-state check were ever bypassed, the provider
    still will not fold the remainder and report a total."""
    with pytest.raises(KernelRefusal) as exc:
        mme.provider.continue_grouped(block, "revenue", composition="addition",
                                      target_index=CoordinateIndex.of(
                                          EX.MANIFOLD, EX.BY_DAY, [("D1",), ("D2",)]),
                                      shape=VALUE_BEARING)
    assert exc.value.code == "want-of-state-reached-the-provider"
    assert "will not fold the remainder" in exc.value.detail


def test_a_carrier_that_contradicts_its_declared_support_is_refused(mme):
    """Declaring a value established while the carrier holds none is a broken representation contract,
    and the engine will not choose which side to believe."""
    index = CoordinateIndex.of(EX.MANIFOLD, EX.SALE_AT,
                               [("D1", "O1", "S1"), ("D1", "O2", "S1")])
    bad = GovernedBlock.of(
        index, {"revenue": pa.array([10.0, None], type=pa.float64())},
        {"revenue": standing("revenue", mme.authority.instance_of("revenue"), n=2,
                             support=[True, True])})
    with pytest.raises(KernelRefusal) as exc:
        mme.establish(bad, "revenue")
    assert exc.value.code == "support-without-a-value"
    assert "the honest standing is want of state" in exc.value.detail


def test_a_null_in_a_standing_mask_is_refused_outright(mme):
    with pytest.raises(KernelRefusal) as exc:
        ColumnStanding(family_id="x", instance=mme.authority.instance_of("revenue"),
                       participation=pa.array([True, None], type=pa.bool_()),
                       support=pa.array([True, True], type=pa.bool_()))
    assert exc.value.code == "null-in-a-standing-mask"
    assert "a third standing this model does not represent" in exc.value.detail


def test_the_standing_default_is_all_true_and_never_derived_from_the_values(mme):
    st = standing("revenue", mme.authority.instance_of("revenue"), n=3)
    assert st.participation.to_pylist() == [True] * 3
    assert st.support.to_pylist() == [True] * 3


# ══ 4 · GROUPED CONTINUATION BY DATAFUSION ════════════════════════════════════════════════════════
def test_revenue_is_continued_by_grouped_datafusion_reduction(settled):
    answer = settled.measure("revenue", EX.BY_DAY)
    assert answer.served and answer.route == "continued"
    assert answer.value.cell(("D1",)) == 235.0 and answer.value.cell(("D2",)) == 325.0
    assert any("datafusion: aggregate(group_by=['day'], agg=addition)" in s
               for s in answer.value.route)


def test_the_governed_filter_runs_before_the_engine_sees_anything(settled):
    """The filter restricts to the CONTRIBUTING DOMAIN — participation, all seven — and never to
    `participation ∧ support`."""
    route = settled.measure("revenue", EX.BY_DAY).value.route
    step = next(s for s in route if s.startswith("governed-filter"))
    assert "7/7 positions in the CONTRIBUTING DOMAIN" in step
    assert "NOT from Arrow validity" in step
    assert "never subtracted from it" in step
    assert route.index(step) < next(i for i, s in enumerate(route) if "datafusion" in s)


def test_the_output_is_aligned_on_the_target_anchors_coordinate_index(settled, settled_block):
    state = settled.measure("revenue", EX.BY_DAY).value
    assert state.index.anchor == EX.BY_DAY
    assert state.index.identity != settled_block.index.identity
    assert len(state.index) == 2


def test_the_coarser_index_is_derived_from_existing_points_only(settled):
    state = settled.measure("revenue", EX.TOTAL).value
    assert len(state.index) == 1 and state.index.coordinates == ((),)


def test_an_unrealized_composition_is_a_provider_limit(mme):
    """**Asked of the capability table now, not of a private if-chain** (E-1). The refusal is the same
    governed answer it always was: a provider's inability does not remove a law (ToD v8 §4.1)."""
    from columna_platform.columnar import GROUPED

    with pytest.raises(KernelRefusal) as exc:
        mme.provider.capability(GROUPED, "latest_by_order")
    assert exc.value.code == "unrealized-composition"
    assert "The law is unchanged" in exc.value.detail
    # and it can be ASKED without raising, which the if-chain could not do
    assert not mme.provider.realizes(GROUPED, "latest_by_order")
    assert mme.provider.realizes(GROUPED, "addition")


# ══ 2 · POSITIONAL EXPRESSION EVALUATION ══════════════════════════════════════════════════════════
def test_revenue_over_ordercount_is_a_positional_column_operation(settled, settled_evaluator):
    revenue = settled.measure("revenue", EX.BY_DAY).value
    counts = settled.measure("order_count", EX.BY_DAY).value
    assert revenue.index.identity == counts.index.identity        # ONE layout, no discovery needed
    aov = settled_evaluator.evaluate("average_order_value", EX.BY_DAY)
    assert aov.route == "evaluated" and aov.seeded_from == "b_revenue_ordercount"
    assert aov.value.cell(("D2",)) == pytest.approx(81.25)


def test_differing_layouts_refuse_rather_than_being_joined(settled, settled_evaluator):
    """If two operands ever arrive on different layouts, this path REFUSES and names the lawful remedy.
    It does not reach for the columns' coordinate values."""
    mme = settled
    state = mme.measure("revenue", EX.BY_DAY).value
    other = ColumnarFamilyState(
        family_id="order_count",
        anchor_instance=type(state.anchor_instance)(
            index=CoordinateIndex.of(EX.MANIFOLD, EX.BY_DAY, [("D1",)]),
            instance=mme.authority.instance_of("order_count")),
        values=pa.array([1], type=pa.int64()),
        standing=standing("order_count", mme.authority.instance_of("order_count"), n=1),
        law="COUNT", value_form="scalar", forgotten_since_root=frozenset({"order", "store"}))
    mme.retain(other)
    answer = settled_evaluator.evaluate("average_order_value", EX.BY_DAY)
    assert not answer.served
    assert "layouts-differ" in answer.refusal.detail
    assert "would be relational discovery of analytical alignment" in answer.refusal.detail


def test_an_expression_output_is_not_family_state_and_has_no_continuation_path(settled,
                                                                               settled_evaluator):
    """**And after M-2 it is not held either** (§1). The type still forbids continuation, the verdict
    still names the rule, and there is no longer a store the output could be sitting in when asked."""
    mme = settled
    output = settled_evaluator.evaluate("average_order_value", EX.BY_DAY).value
    assert isinstance(output, ColumnarExpressionOutput)
    assert output.CONTINUATION_BEARING is False
    assert ColumnarFamilyState.CONTINUATION_BEARING is True
    assert not hasattr(ColumnarExpressionOutput, "fold_onto_grouped")

    # NOT HELD: the columnar MME manages family materializations only.
    assert all(k.identity != "average_order_value" for k in mme.held)
    assert not mme.materializations.select("average_order_value", eligibility=None)
    with pytest.raises(KernelRefusal) as offered:
        mme.retain(output)
    assert offered.value.code == "not-a-family-materialization"

    # OFFERED FROM ABOVE — the only remaining route to `adjudicate` — and still refused by name.
    from_above = Retained(
        key=RetentionKey(identity="average_order_value", anchor=EX.BY_DAY,
                         instance=output.instance, realization=mme.realization),
        value=output)
    verdict = mme.adjudicate(
        from_above, mme.authority.authorizer.authorize(mme.family("revenue"), EX.BY_DAY).request)
    assert not verdict and verdict.code == "not-continuation-bearing"


# ══ 3 · COMPATIBILITY BEFORE ARITHMETIC ═══════════════════════════════════════════════════════════
def test_an_incompatible_basis_is_refused_before_arithmetic_on_one_aligned_layout(settled, settled_evaluator):
    revenue = settled.measure("revenue", EX.BY_DAY).value
    audited = settled.measure("audited_order_count", EX.BY_DAY).value
    assert revenue.index.identity == audited.index.identity        # perfectly aligned
    assert len(revenue.values) == len(audited.values)              # same shape

    answer = settled_evaluator.evaluate("average_order_value_audited", EX.BY_DAY)
    assert not answer.served
    assert "THE ARITHMETIC HAS NOT RUN" in answer.refusal.detail
    assert "different-participation" in answer.refusal.detail
    # AUTHORITY BEFORE EVIDENCE: a jointly-unusable basis refuses on participation, and this is not
    # dressed up as a want-of-state refusal even in a world where one could also be owed.
    assert "basis-operand-wants-state" not in answer.refusal.detail


# ══ 5 · NON-ROOT SEEDING, AND THE LAUNDERING GUARD ════════════════════════════════════════════════
def test_a_non_root_columnar_state_seeds_a_later_continuation(settled):
    mme = settled
    mme.measure("revenue", EX.BY_DAY)
    total = mme.measure("revenue", EX.TOTAL)
    assert total.seeded_from.anchor == EX.BY_DAY
    assert total.value.cell(()) == 560.0
    assert total.value.forgotten_since_root == frozenset({"order", "store", "day"})


def test_the_authority_is_the_kernels_own_adjudicate_reused_verbatim(mme):
    """**The architectural claim of this unit, and it is not fakeable.** `ColumnarMME.adjudicate` calls
    `kernel.MME.adjudicate` — the same function object, over columnar state — so the five questions are
    asked by the analytical authority and the substrate does not get a vote."""
    import inspect

    source = inspect.getsource(ColumnarMME.adjudicate)
    assert "self.authority.adjudicate(candidate, request)" in source
    assert mme.authority.adjudicate.__func__ is KernelMME.adjudicate


def test_the_laundering_guard_survives_the_substrate(mme):
    """It holds here FOR FREE, because it was not reimplemented."""
    on_hand = EX._families()[4]
    mme.authority.register_family(on_hand)
    index = CoordinateIndex.of(EX.MANIFOLD, EX.COMMERCE.anchor({"store", "day"}),
                               [("D1", "S1"), ("D1", "S2"), ("D2", "S1"), ("D2", "S2")])
    block = GovernedBlock.of(index, {"on_hand": pa.array([10, 7, 12, 9], type=pa.int64())},
                             {"on_hand": standing("on_hand",
                                                  mme.authority.instance_of("on_hand"), n=4)})
    mme.establish(block, "on_hand")

    assert mme.measure("on_hand", EX.BY_DAY).value.cell(("D1",)) == 17      # forgets store: lawful
    assert not mme.measure("on_hand", EX.BY_STORE).served                   # forgets day: refused
    laundered = mme.measure("on_hand", EX.TOTAL)                            # two-step: refused
    assert not laundered.served
    assert "cannot launder an edge the law does not admit" in laundered.refusal.detail
    assert any(k.identity == "on_hand" and k.anchor == EX.BY_DAY for k in mme.held)


# ══ 6 + 7 · THE STRUCTURED FAMILY ═════════════════════════════════════════════════════════════════
def test_the_sketch_family_continues_through_the_datafusion_udaf(mme):
    answer = mme.measure("distinct_customers", EX.BY_DAY)
    assert answer.served and answer.route == "continued"
    assert answer.value.values.type == pa.binary()
    assert any("agg=sketch_union" in s for s in answer.value.route)
    assert estimate_of(answer.value.cell(("D1",))) == 3


def test_the_persisted_family_value_is_the_sketch_and_not_the_estimate(mme):
    state = mme.measure("distinct_customers", EX.TOTAL).value
    payload = state.cell(())
    assert isinstance(payload, bytes)
    from datasketches import hll_sketch

    assert hll_sketch.deserialize(payload).lg_config_k == HLL_PRECISION


def test_sketch_parameters_are_compatibility_bearing_and_read_from_the_value(mme, evaluator):
    from columna_platform.columnar.provider import sketch_parameters

    state = mme.measure("distinct_customers", EX.BY_DAY).value
    assert sketch_parameters(state.cell(("D1",)))["lg_k"] == HLL_PRECISION
    output = evaluator.evaluate("distinct_customer_estimate", EX.BY_DAY).value
    assert any(d.code == "sketch-parameters" for d in output.disclosures)


def test_the_estimate_is_served_only_through_expression_finalization(mme, evaluator):
    answer = evaluator.evaluate("distinct_customer_estimate", EX.BY_DAY)
    assert answer.route == "evaluated" and answer.seeded_from == "b_sketch"
    assert answer.value.cell(("D1",)) == 3 and answer.value.cell(("D2",)) == 3
    # NOT HELD (M-2 §1) — and refused as continuation state when offered from above.
    assert all(k.identity != "distinct_customer_estimate" for k in mme.held)
    from_above = Retained(
        key=RetentionKey(identity="distinct_customer_estimate", anchor=EX.BY_DAY,
                         instance=answer.value.instance, realization=mme.realization),
        value=answer.value)
    verdict = mme.adjudicate(
        from_above,
        mme.authority.authorizer.authorize(mme.family("distinct_customers"), EX.BY_DAY).request)
    assert not verdict and verdict.code == "not-continuation-bearing"


def test_a_sketch_column_never_displays_an_estimate_through_formatting(mme):
    state = mme.measure("distinct_customers", EX.BY_DAY).value
    block = GovernedBlock.of(state.index, {"distinct_customers": state.values},
                             {"distinct_customers": state.standing})
    rendered = block.render()
    assert "⟨sketch:" in rendered
    assert "Estimate" not in rendered


def test_the_udaf_state_and_evaluate_return_the_same_portable_sketch():
    """*"Only the governed family value may be persisted as family state."* There is no engine-native
    intermediate that could become the persisted representation by being convenient."""
    from columna_platform.columnar.provider import HllUnionAccumulator

    acc = HllUnionAccumulator()
    acc.update(pa.array([sketch_of(["C1"]), sketch_of(["C2"])], type=pa.binary()))
    assert acc.state()[0].as_py() == acc.evaluate().as_py()
    assert estimate_of(acc.evaluate().as_py()) == 2


# ══ 10 · MANIFOLD ISOLATION ═══════════════════════════════════════════════════════════════════════
def test_two_manifolds_may_use_the_same_family_name(mme):
    other, _ = EX.build(EX.OTHER_MANIFOLD)
    assert "revenue" in mme.authority.families and "revenue" in other.authority.families
    assert mme.manifold != other.manifold


def test_state_from_one_manifold_may_not_satisfy_or_seed_a_request_in_the_other(mme):
    """**The negative isolation test.** One shared provider, two jurisdictions, no shared state."""
    other, other_block = EX.build(EX.OTHER_MANIFOLD)
    other.provider = mme.provider                       # deliberately the SAME provider object
    assert other.provider is mme.provider

    with pytest.raises(KernelRefusal) as exc:
        mme.establish(other_block, "revenue")
    assert exc.value.code == "foreign-manifold-block"

    verdict = (mme.authority.instance_of("revenue")
               .compatible_with(other.authority.instance_of("revenue")))
    assert not verdict and verdict.code == "different-manifold"

    # in the SETTLED world both jurisdictions can serve, and each serves only from its own state
    mine, _ = EX.build(EX.MANIFOLD, settled=True)
    theirs, _ = EX.build(EX.OTHER_MANIFOLD, settled=True)
    theirs.provider = mine.provider
    mine.measure("revenue", EX.BY_DAY)
    other_answer = theirs.measure("revenue", EX.BY_DAY)
    assert other_answer.served
    assert other_answer.seeded_from.instance.manifold == EX.OTHER_MANIFOLD


def test_a_foreign_manifolds_object_cannot_be_registered():
    authority = MME(EX.COMMERCE, REGISTRY, IN_MEMORY, manifold=EX.MANIFOLD)
    with pytest.raises(KernelRefusal) as exc:
        authority.register_family(EX._families(EX.OTHER_MANIFOLD)[0])
    assert exc.value.code == "foreign-manifold"
    assert "one identity under two authorities" in exc.value.detail


def test_two_manifolds_coordinate_indexes_are_different_identities():
    a = CoordinateIndex.of(EX.MANIFOLD, EX.BY_DAY, [("D1",)])
    b = CoordinateIndex.of(EX.OTHER_MANIFOLD, EX.BY_DAY, [("D1",)])
    assert a.identity != b.identity


def test_an_anchor_instance_may_not_straddle_two_jurisdictions(mme):
    from columna_platform.columnar.index import AnchorInstance

    with pytest.raises(KernelRefusal) as exc:
        AnchorInstance(index=CoordinateIndex.of(EX.OTHER_MANIFOLD, EX.BY_DAY, [("D1",)]),
                       instance=mme.authority.instance_of("revenue"))
    assert exc.value.code == "manifold-disagreement"


def test_a_block_may_not_declare_a_familys_analytical_instance(mme, block):
    from columna_platform.kernel import AnalyticalInstance

    forged = AnalyticalInstance(manifold=EX.MANIFOLD, universe="commerce",
                               participation="something else")
    bad = GovernedBlock.of(block.index, {"revenue": block.column("revenue")},
                           {"revenue": standing("revenue", forged, n=len(block.index))})
    with pytest.raises(KernelRefusal) as exc:
        mme.establish(bad, "revenue")
    assert exc.value.code == "block-instance-mismatch"


# ══ the exhibit runs ══════════════════════════════════════════════════════════════════════════════
def test_the_columnar_exhibit_runs_green(capsys):
    assert EX.main() == 0
    out = capsys.readouterr().out
    assert "ALL CHECKS PASSED" in out and "✗" not in out
    for proof in ("PROOF 1 ·", "PROOF 2 ·", "PROOF 3 ·", "PROOF 4 ·", "PROOF 5 ·", "PROOF 5b ·",
                  "PROOF 6 ·", "PROOF 8 ·", "PROOF 9 ·", "PROOF 10 ·"):
        assert proof in out, proof

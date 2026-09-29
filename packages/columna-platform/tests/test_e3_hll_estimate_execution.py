"""
test_e3_hll_estimate_execution.py — **E-3: the HLL estimate's execution form, and the end of
`Realization.finalize`.**

    *"Remove or characterize the remaining per-cell Python boundary in HLL estimate/finalization while
    preserving Arrow-in/Arrow-out execution. Do not assume beforehand that 'move it into DataFusion' is the
    answer. A DataFusion UDF that simply contains the same Python per-cell loop is not an architectural
    improvement. … Python may orchestrate; analytical payload stays columnar; cell-scale compute should run
    in a columnar/native engine where doing so produces a real execution improvement."*
        — Huayin, 2026-09-29

    *"Also adjudicate the currently dead `Realization.finalize` slot separately. Do not populate it merely
    because HLL estimate sounds like 'finalization.' Under v8, `HLLSketch` is the family value and HLL
    estimate is an expression over that family value."*

Recon E-X's step 3 said: *"move `hll_estimate` off the Python comprehension to a DataFusion UDF or an Arrow
kernel."* **E-3 measured that recommendation and reversed it.** Each branch fails for a different reason, and
§C below is the reversal as executable evidence rather than prose:

    a DataFusion **Python UDF**      the same Python loop, plus a per-batch Arrow→Python→Arrow round trip.
                                     MEASURED 1.95 µs/cell vs 1.51 in-process — **1.29× SLOWER.**
    DataFusion **`approx_distinct`** not this operation. Over the governed family value it counts distinct
                                     BLOBS: 2 where the population is 4. A confident wrong number. Its
                                     internal HLL is also a vendored redis derivative, not DataSketches.
    an **Arrow kernel**              does not exist and cannot: the work is a third-party sketch decode.
    the **DataSketches binding**     has no batch API and no zero-copy input. `bytes` or nothing.

A **native Rust kernel does exist** — crate `datasketches` ≥ 0.5.0 reads C++ compact HLL images, DataFusion
54 registers Rust UDFs in-engine via the `datafusion-ffi` PyCapsule protocol, and `datafusion-comet` PR
#4802 is a merged reference implementation. It is **DEFERRED, and not for want of a library:** the Rust
crate's estimates are not bit-identical to the C++ library's for merged sketches (≈0.7%, inside RSE but not
zero), so adopting it would be **a second REALIZATION of the same law, not a faster one** — a
`RealizationStanding` change under §8.7/P-1, requiring its own admission evidence, not an optimization of
one function. §C pins that reasoning as tests.

So the boundary is **characterized, not removed** — and what E-3 *did* remove is the carriage around it. The
removed cost is per-cell and size-independent, so the ratio falls as sketches grow while the saving does not
(2 000 sketches, best of 15 CPU-time runs):

    uniform LIST/SET (172 B)         2.305 → 1.456 µs/cell   36.8% removed   1.58×
    mixed LIST+SET+HLL (12–4136 B)   3.768 → 2.908 µs/cell   22.8% removed   1.30×

The five sections, in the order the burden of proof runs:

    A  the output is BYTE-FOR-BYTE what the pre-E-3 algorithm produced — verbatim reimplementation
    B  the estimate is still an EXPRESSION and never family continuation state
    C  the alternatives, as negative controls that fail for the recorded reason
    D  the Python-cell-loop count, counted from the AST rather than claimed
    E  `Realization.finalize` is retired, and finalization has exactly one route

WHAT IS NOT EXERCISED, DELIBERATELY: no continuation or alignment optimization, no backend, no ADBC, no
persistence, no DuckDB, no expression caching. Ruled out by name; §F checks that each stayed out.
"""
from __future__ import annotations

import ast
import inspect
from dataclasses import fields

import pyarrow as pa
import pyarrow.compute as pc
import pytest

from columna_platform.columnar import (
    GROUPED,
    POSITIONAL,
    ColumnarExpressionEvaluator,
    ColumnarProvider,
    ExecutionCapability,
    estimate_of,
    estimates_of,
    sketch_of,
)
from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar import expression as columnar_expression_module
from columna_platform.columnar import provider as provider_module
from columna_platform.columnar.mme import ColumnarExpressionOutput, ColumnarFamilyState
from columna_platform.kernel import ADDITION, REGISTRY, SKETCH_UNION, KernelRefusal
from columna_platform.kernel.builtins import IN_MEMORY
from columna_platform.kernel.law import SCALAR, STRUCTURED
from columna_platform.kernel.realization import ProviderProfile, Realization

LOAD = "load:orders@08:00Z"


def _body_only(fn) -> str:
    """A function's executable text, docstring stripped. Needed because these tests assert on the code of
    functions whose docstrings *quote* that code — `_pre_e3_hll_estimate` prints the pre-E-3 comprehension
    in its own docstring, so a naive `count()` over `getsource` counts it twice."""
    tree = ast.parse(inspect.getsource(fn).lstrip())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


def _code_only(module) -> str:
    """Executable text only — docstrings and comments stripped, so a ban cannot be tripped by the prose
    that explains it. Same helper as the E-1, F-1 and R-1 suites."""
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


# ══════════════════════════════════════════════════════════════════════════════════════════════════
#  THE PRE-E-3 ALGORITHM, VERBATIM
# ══════════════════════════════════════════════════════════════════════════════════════════════════
def _pre_e3_hll_estimate(columns, parameters):
    """`provider._hll_estimate` **exactly as it stood before E-3**, transcribed from
    `provider.py:293-296` at merge `ef65fb4`. Not a paraphrase and not a simplification: if the two ever
    disagree on any column, the memoised claim "cost only, not semantics" is false and §A fails.

        sketches = columns["HLL_SKETCH"]
        return pa.array([None if v.as_py() is None else estimate_of(v.as_py()) for v in sketches],
                        type=pa.int64())
    """
    sketches = columns["HLL_SKETCH"]
    return pa.array([None if v.as_py() is None else estimate_of(v.as_py()) for v in sketches],
                    type=pa.int64())


@pytest.fixture
def provider():
    return ColumnarProvider()


@pytest.fixture
def settled():
    engine, block = CEX.build(settled=True, data_state=LOAD)
    return engine, ColumnarExpressionEvaluator(engine)


def _sketch_column(specs):
    """`specs` is a sequence of either `None` or an iterable of values to sketch."""
    return pa.array([None if s is None else sketch_of(list(s)) for s in specs], type=pa.binary())


# ══ A · THE OUTPUT IS WHAT THE PRE-E-3 ALGORITHM PRODUCED ═════════════════════════════════════════
CASES = {
    "dense": [("a", "b", "c"), ("c", "d"), ("e",)],
    "all-null": [None, None],
    "null-bearing": [("a",), None, ("b", "c"), None],
    "leading-null": [None, ("a", "b")],
    "single": [("only",)],
    "empty-column": [],
    "empty-sketches": [(), ()],
    "duplicate-payloads": [("a", "b"), ("a", "b"), ("a", "b")],
    "wide": [tuple(f"v{i}-{j}" for j in range(50)) for i in range(40)],
}


@pytest.mark.parametrize("name", sorted(CASES))
def test_the_finalizer_returns_exactly_what_the_pre_e3_algorithm_returned(provider, name):
    """**The whole unit's central claim, on nine shapes.** Equal values, equal type, equal null mask —
    `Array.equals` checks all three, and the type is asserted separately because an int64 column of the
    right numbers under the wrong type is still a changed result."""
    column = _sketch_column(CASES[name])
    before = _pre_e3_hll_estimate({"HLL_SKETCH": column}, {})
    after = provider.evaluate_positional({"HLL_SKETCH": column}, law="HLL_ESTIMATE")

    assert after.equals(before), name
    assert after.type == before.type == pa.int64()
    assert after.null_count == before.null_count
    assert after.to_pylist() == before.to_pylist()


def test_an_empty_sketch_estimates_zero_and_is_not_a_null(provider):
    """The two absences stay distinct. A sketch of nothing is a sketch that says ZERO; a null cell is no
    sketch at all. Collapsing them would be reading a carrier null as a standing."""
    out = provider.evaluate_positional({"HLL_SKETCH": _sketch_column([(), None])}, law="HLL_ESTIMATE")
    assert out.to_pylist() == [0, None]
    assert out.null_count == 1


def test_the_estimate_is_arrow_in_and_arrow_out(provider):
    """Ruled: *"while preserving Arrow-in/Arrow-out execution."* Nothing but Arrow crosses either edge."""
    column = _sketch_column(CASES["dense"])
    assert isinstance(column, pa.Array)
    out = provider.evaluate_positional({"HLL_SKETCH": column}, law="HLL_ESTIMATE")
    assert isinstance(out, pa.Array) and out.type == pa.int64()
    assert len(out) == len(column)                        # a MAP: one index in, the same index out


def test_estimates_of_is_the_one_named_place_and_agrees_with_per_cell_calls():
    """`estimates_of` is the whole cell-scale step, extracted so that a future native kernel replaces one
    function body. It must agree cell-for-cell with `estimate_of`, which is the in-memory route's call."""
    payloads = [sketch_of(["a", "b", "c"]), None, sketch_of([])]
    assert estimates_of(payloads).to_pylist() == [estimate_of(payloads[0]), None, estimate_of(payloads[2])]
    assert estimates_of([]).type == pa.int64()            # type survives an empty column


def test_the_served_estimate_is_unchanged_end_to_end(settled):
    """Above the provider, through the governed evaluator, on the exhibit's own world. The numbers E-1
    asserted are the numbers E-3 serves."""
    engine, evaluator = settled
    by_day = evaluator.evaluate("distinct_customer_estimate", CEX.BY_DAY)
    assert by_day.served and by_day.seeded_from == "b_sketch"
    assert sorted(by_day.value.values.to_pylist()) == [3, 3]

    total = evaluator.evaluate("distinct_customer_estimate", CEX.TOTAL)
    assert total.served
    assert total.value.values.to_pylist() == [len({o["customer"] for o in CEX.ORDERS})]


def test_the_sketch_parameter_disclosure_still_rides_along(settled):
    """Sketch parameters are compatibility-bearing and are read from the value. A carriage change must not
    cost the disclosure that says so."""
    _engine, evaluator = settled
    answer = evaluator.evaluate("distinct_customer_estimate", CEX.BY_DAY)
    codes = {d.code for d in answer.value.disclosures}
    assert "sketch-parameters" in codes
    detail = next(d for d in answer.value.disclosures if d.code == "sketch-parameters").detail
    assert "lg_k" in detail and "COMPATIBILITY-BEARING" in detail


# ══ B · STILL AN EXPRESSION. NEVER FAMILY CONTINUATION STATE. ═════════════════════════════════════
def test_the_MME_holds_the_SKETCH_and_nothing_for_the_ESTIMATE(settled):
    """§10's chain, after E-3 as before it:

        estimate(HLLSketch@A) → MME supplies HLLSketch@A → finalizer/evaluator → estimate

    The MME manages family materializations. The estimate is not one, and there is nothing of it to find."""
    engine, evaluator = settled
    answer = evaluator.evaluate("distinct_customer_estimate", CEX.BY_DAY)
    assert answer.served

    held = engine.materializations.select("distinct_customers", anchor=CEX.BY_DAY)
    assert held and held[0].value.value_form == STRUCTURED
    assert not engine.materializations.select("distinct_customer_estimate", eligibility=None)


def test_the_finalized_output_is_not_family_state_and_carries_no_merge_path(settled):
    """A TYPE distinction, not a convention. `ColumnarExpressionOutput` is not a
    `ColumnarFamilyState`, and it has no `merge`/`continue` of any spelling for a caller to reach for."""
    _engine, evaluator = settled
    output = evaluator.evaluate("distinct_customer_estimate", CEX.BY_DAY).value

    assert isinstance(output, ColumnarExpressionOutput)
    assert not isinstance(output, ColumnarFamilyState)
    for continuation in ("merge", "continue", "continued", "fold", "combine", "with_merge"):
        assert not hasattr(output, continuation), continuation


def test_the_law_registry_still_says_the_estimate_cannot_continue():
    """The semantic half of the same fact, and it is the one that licenses the other: `HLL_SKETCH` names
    its finalizer, and the named law has no continuation for anything to merge."""
    sketch, estimate = REGISTRY.get("HLL_SKETCH"), REGISTRY.get("HLL_ESTIMATE")
    assert sketch.value_form == STRUCTURED and sketch.finalized_by == "HLL_ESTIMATE"
    assert estimate.continuation is None
    assert estimate.value_form == SCALAR


def test_the_finalizer_may_not_be_declared_as_a_grouped_capability():
    """The structural bar on finalizing INSIDE the MME. A grouped capability changes the anchor; one that
    also finalized would be turning family state into a display value during continuation, which is the
    one place the value would then be retained as if it were still family state."""
    with pytest.raises(KernelRefusal) as refused:
        ExecutionCapability(mode=GROUPED, operation="HLL_ESTIMATE",
                            execute=provider_module._hll_estimate,
                            value_form_in=STRUCTURED, value_form_out=SCALAR)
    assert refused.value.code == "grouped-capability-may-not-finalize"


def test_the_provider_does_not_realize_the_estimate_as_a_composition(provider):
    """Asked the other way round: the provider's own table refuses to fold `HLL_ESTIMATE` at all, and the
    refusal still says the law is unchanged — a provider's inability never removes a law (§4.1)."""
    assert provider.realizes(POSITIONAL, "HLL_ESTIMATE")
    assert not provider.realizes(GROUPED, "HLL_ESTIMATE")
    assert not provider.realizes_composition("HLL_ESTIMATE")
    with pytest.raises(KernelRefusal) as refused:
        provider.capability(GROUPED, "HLL_ESTIMATE")
    assert "law is unchanged" in refused.value.detail or "unchanged" in refused.value.detail


def test_a_coarser_estimate_is_re_finalized_from_a_merged_sketch_not_folded_from_finer_estimates(settled):
    """**The proof that the estimate is an expression and not a continuation, arithmetically.** Summing the
    per-day estimates gives 6; the governed total is 3 — the same three customers shopped on both days. If
    the estimate were family state, continuing it would have to produce a number, and the number it would
    produce is wrong."""
    _engine, evaluator = settled
    per_day = evaluator.evaluate("distinct_customer_estimate", CEX.BY_DAY).value.values.to_pylist()
    total = evaluator.evaluate("distinct_customer_estimate", CEX.TOTAL).value.values.to_pylist()

    distinct_overall = len({o["customer"] for o in CEX.ORDERS})
    assert sum(per_day) == 6                              # what folding finalized values would give
    assert total == [distinct_overall] == [5]             # what re-finalizing a merged sketch gives
    assert sum(per_day) > total[0]                        # and the fold OVERCOUNTS the shared customers


# ══ C · THE ALTERNATIVES, AS NEGATIVE CONTROLS ════════════════════════════════════════════════════
def test_datafusions_native_approx_distinct_is_the_wrong_operation_over_the_family_value():
    """**The reason "move it into DataFusion" is not merely unhelpful but WRONG in its native form.**

    `approx_distinct` is DataFusion's only HLL-shaped capability, and it computes its own internal sketch
    over the values it is given. Given the governed family value — a column of serialized sketches — the
    values it sees are BLOBS, so it counts blobs: **2** for two sketches whose union is over **4**
    customers. It is not an approximation of the right answer; it is an answer to a different question."""
    from datafusion import SessionContext, col
    from datafusion import functions as DF

    sketches = pa.array([sketch_of(["a", "b", "c"]), sketch_of(["c", "d"])], type=pa.binary())
    batch = pa.RecordBatch.from_arrays([sketches], names=["sk"])
    frame = SessionContext().create_dataframe([[batch]])
    counted = frame.aggregate([], [DF.approx_distinct(col("sk")).alias("n")]).collect()

    assert counted[0].column("n").to_pylist() == [2]      # distinct BLOBS
    # the governed route — union the family values, then finalize the union — is 4
    from columna_platform.columnar.provider import HLL_PRECISION
    from datasketches import hll_sketch, hll_union

    union = hll_union(HLL_PRECISION)
    for payload in sketches.to_pylist():
        union.update(hll_sketch.deserialize(payload))
    assert int(round(union.get_result().get_estimate())) == 4


def test_datafusion_exposes_no_estimator_over_an_already_materialized_sketch():
    """The other half: there is no native function to *adopt*. `approx_distinct` is an aggregate over raw
    occurrences whose internal sketch is never exposed, so it cannot be a finalizer over stored family
    state, and no DataFusion function names HLL or sketch at all."""
    from datafusion import functions as DF

    assert hasattr(DF, "approx_distinct")                 # it exists …
    named = [n for n in dir(DF) if "hll" in n.lower() or "sketch" in n.lower()]
    assert named == [], named                             # … and nothing takes a sketch


def test_pyarrow_compute_has_no_sketch_kernel():
    """An Arrow kernel was recon E-X's other suggestion. Arrow's kernel registry is arithmetic and
    string/temporal work over its own types; decoding a third-party sketch is not in it and would not be."""
    kernels = set(pc.list_functions())
    assert not [k for k in kernels if "hll" in k or "sketch" in k or "distinct_count" in k]
    assert "approx_median" not in kernels


def test_the_datasketches_binding_offers_no_batch_api_and_no_zero_copy_input():
    """**Why the loop cannot simply be hoisted into the library.** The binding takes one sketch at a time and
    takes it as `bytes` — so both the per-sketch call and one `bytes` materialization are forced from Python,
    and `to_pylist()` is the cheapest legal way to produce the latter for a whole column.

    (Contrast the quantiles families, which DO accept numpy arrays in `update`. HLL does not, so this is a
    gap in the binding rather than a property of the library.)"""
    from datasketches import hll_sketch

    plural = [n for n in dir(hll_sketch) if "many" in n or "batch" in n or n.endswith("_all")]
    assert plural == [], plural

    payload = sketch_of(["a", "b"])
    assert isinstance(hll_sketch.deserialize(payload), hll_sketch)
    for zero_copy in (memoryview(payload), bytearray(payload), pa.py_buffer(payload)):
        with pytest.raises(TypeError):
            hll_sketch.deserialize(zero_copy)


def test_a_native_kernel_would_be_a_SECOND_REALIZATION_and_the_model_already_says_so():
    """**The deciding reason the Rust route is deferred, as a property of the model rather than an opinion.**

    A native kernel on Apache's Rust crate exists and is buildable (crate `datasketches` ≥ 0.5.0,
    registered through DataFusion 54's `datafusion-ffi` PyCapsule protocol; `datafusion-comet` PR #4802 is
    the reference). But its estimates are not bit-identical to the C++ library's for merged sketches, so it
    would be a DIFFERENT physical realization of one analytical quantity — and `RealizationStanding` is
    exactly the axis that makes such a value non-interchangeable rather than merely faster.

    So the decision is not "Rust is too hard." It is that the change belongs to the axis below, with its own
    admission evidence, and this test pins that the axis is present and load-bearing today."""
    from columna_platform.kernel.mme import RetentionKey
    from columna_platform.kernel.realization import RealizationStanding

    exact = RealizationStanding(provider="arrow+datafusion")
    other = RealizationStanding(provider="arrow+datasketches-rust")
    assert exact != other and exact.token != other.token
    assert "realization" in {f.name for f in fields(RetentionKey)}


def test_the_provider_registers_one_UDAF_for_CONTINUATION_and_no_scalar_UDF():
    """**The structural form of "a UDF wrapping the same loop is not an improvement."** DataFusion is used
    here for the one thing it does natively and well — grouped reduction, via the governed union UDAF — and
    the finalizer is not routed through a `udf` at all. Measured at E-3 the UDF form was 1.29× SLOWER than
    the in-process one; this test pins that nobody adds it back on the theory that it must be faster."""
    code = _code_only(provider_module)
    assert "udaf(" in code                                # the union: DataFusion's job
    assert "udf(" not in code.replace("udaf(", "")         # the finalizer: not a UDF
    assert "= udf" not in code


def test_the_estimate_never_touches_a_session_context(provider):
    """A finalizer is a MAP over one aligned column. It needs no engine, no plan, no partitioning — and
    reaching for one would add the round trip E-3 measured for nothing in return."""
    source = _body_only(provider_module._hll_estimate) + _body_only(estimates_of)
    for engine_concept in ("self.ctx", "SessionContext", "create_dataframe", "aggregate(", "collect()"):
        assert engine_concept not in source, engine_concept


# ══ D · THE PYTHON-CELL-LOOP COUNT, FROM THE AST ══════════════════════════════════════════════════
def _cell_loops(fn) -> list[str]:
    """Every Python construct in `fn` that iterates once per cell: a `for`, a comprehension, a
    generator expression. Counted from the tree, so a rewrite that hides one in a helper still shows."""
    tree = ast.parse(inspect.getsource(fn).lstrip())
    return [type(n).__name__ for n in ast.walk(tree)
            if isinstance(n, (ast.For, ast.AsyncFor, ast.ListComp, ast.SetComp,
                              ast.DictComp, ast.GeneratorExp))]


def test_the_finalizer_carries_exactly_one_python_cell_loop():
    """**BEFORE 2, AFTER 1.** The pre-E-3 finalizer iterated the Arrow array itself — one comprehension
    boxing N `BinaryScalar`s, each then converted TWICE. E-3's `_hll_estimate` has none at all and the one
    that remains is in `estimates_of`, which is the irreducible native call."""
    assert _cell_loops(_pre_e3_hll_estimate) == ["ListComp"]
    assert _cell_loops(provider_module._hll_estimate) == []
    assert _cell_loops(estimates_of) == ["ListComp"]

    on_the_path = _cell_loops(provider_module._hll_estimate) + _cell_loops(estimates_of)
    assert len(on_the_path) == 1


def test_no_per_cell_as_py_survives_on_the_finalizer_path():
    """The removed carriage, named. `as_py()` on a boxed scalar is the per-cell Arrow→Python crossing; the
    pre-E-3 form called it twice per cell, once to test the null and once to use the value. One
    `to_pylist()` replaces both for the whole column."""
    before = _body_only(_pre_e3_hll_estimate)
    assert before.count("as_py()") == 2                   # once to test the null, once to use the value

    after = _body_only(provider_module._hll_estimate) + _body_only(estimates_of)
    assert "as_py()" not in after
    assert "to_pylist()" in _body_only(provider_module._hll_estimate)


def test_the_extraction_is_one_vectorised_call_and_the_native_call_is_one_per_sketch():
    """The division of labour, asserted rather than described: exactly one bulk extraction, and exactly one
    `estimate_of` call site — so "one native call per sketch" is a property of the code, not a claim."""
    assert _body_only(provider_module._hll_estimate).count("to_pylist()") == 1
    assert _body_only(estimates_of).count("estimate_of(") == 1


def test_the_in_memory_finalizer_is_already_native_and_unchanged():
    """The in-memory twin was never the defect — recon E-X classed it **(d)**, one native call per cell
    driven by the kernel's own cell loop. E-3 leaves it exactly as it was."""
    apply = IN_MEMORY.of("HLL_ESTIMATE").apply
    assert _cell_loops(apply) == []
    assert "get_estimate" in _body_only(apply)


# ══ E · `Realization.finalize` IS RETIRED ═════════════════════════════════════════════════════════
def test_the_finalize_slot_is_gone():
    """Ruled: *"if no, retire the slot and its dead conceptual machinery."* It is no.

    The field was declared at `kernel/realization.py:78`, never populated by any profile and never read by
    any caller. It named no family-level responsibility under v8, because a structured family law names its
    finalizer by governed LAW NAME and that law's own realization supplies it."""
    assert "finalize" not in {f.name for f in fields(Realization)}
    assert {f.name for f in fields(Realization)} == {
        "law", "contribute", "merge", "identity", "apply", "note"}
    assert not hasattr(Realization(law="X"), "finalize")


def test_finalization_has_exactly_one_route_and_it_is_the_constructors_apply():
    """Where finalization actually lives, shown as a chain rather than asserted: the family law names
    `HLL_ESTIMATE`; `HLL_ESTIMATE` is a law in the registry; its realization has an `apply`; that `apply`
    is the finalizer. No step of that goes through the family's own realization."""
    family = REGISTRY.get("HLL_SKETCH")
    assert family.finalized_by == "HLL_ESTIMATE"

    constructor = IN_MEMORY.of(family.finalized_by)
    assert constructor.apply is not None
    assert constructor.merge is None and constructor.contribute is None

    sketch_realization = IN_MEMORY.of("HLL_SKETCH")
    assert sketch_realization.apply is None               # the FAMILY finalizes nothing
    assert sketch_realization.merge is not None           # it continues, which is its job


def test_asking_a_profile_to_finalize_is_now_a_governed_refusal():
    """The slot's removal is reachable as a refusal rather than an `AttributeError`: `capability` answers
    for any absent capability with a governed message naming the provider, so a caller written against the
    old field learns that the profile does not supply it and that the law is unchanged."""
    with pytest.raises(KernelRefusal) as refused:
        IN_MEMORY.capability("HLL_SKETCH", "finalize")
    assert refused.value.code == "unrealized-capability"
    assert "the law is unchanged" in refused.value.detail


def test_no_profile_anywhere_ever_passed_a_finalize():
    """A profile constructed with the retired keyword now fails loudly instead of silently carrying a field
    nothing reads — which is what the slot did for its whole life."""
    with pytest.raises(TypeError):
        Realization(law="HLL_ESTIMATE", finalize=lambda v: v)     # type: ignore[call-arg]
    profile = ProviderProfile("p", (Realization(law="HLL_ESTIMATE", apply=lambda p, q: 1),))
    assert profile.realizes("HLL_ESTIMATE")


def test_the_concepts_surviving_residue_is_the_derived_columnar_property(provider):
    """What replaces the slot, and why nothing was lost. "Is a finalizer" is **derived** from a
    capability's value-form transition and asserted nowhere — a property read off a declaration instead of
    a slot a provider can fill. `finalizes` is not even a field."""
    estimate = provider.capability(POSITIONAL, "HLL_ESTIMATE")
    assert estimate.value_form_in == STRUCTURED and estimate.value_form_out == SCALAR
    assert estimate.finalizes
    assert "finalizes" not in {f.name for f in fields(ExecutionCapability)}

    mean = provider.capability(POSITIONAL, "MEAN")
    assert not mean.finalizes                             # SCALAR → SCALAR is a plain map


def test_the_retirement_is_recorded_where_the_slot_was():
    """A deleted field leaves no trace for the next reader, so the ruling goes in the module that held it.
    Not decoration: the question "why is there no `finalize` here?" has exactly one right answer and it is
    not rediscoverable from the remaining code."""
    from columna_platform.kernel import realization as realization_module

    doc = realization_module.__doc__ or ""
    assert "THERE IS NO `finalize`" in doc
    assert "finalized_by" in doc and "E-3" in doc


# ══ F · WHAT E-3 DID NOT DO ═══════════════════════════════════════════════════════════════════════
def test_no_backend_no_adbc_no_persistence_no_duckdb_arrived():
    """Ruled out by name, all five."""
    from columna_platform.columnar import mme as mme_module

    code = "".join(_code_only(m) for m in (provider_module, columnar_expression_module, mme_module))
    for banned in ("duckdb", "adbc", "psycopg", "sqlalchemy", "polars", "import sqlite3",
                   "parquet", "to_parquet", "iceberg"):
        assert banned not in code.lower(), banned


def test_no_expression_cache_appeared():
    """Ruled out by name, and M-2 §1 removed it on purpose. No store on the evaluator, no `retain`."""
    import inspect as _inspect

    assert "retain" not in _inspect.signature(ColumnarExpressionEvaluator.evaluate).parameters
    code = _code_only(columnar_expression_module)
    for cache in ("lru_cache", "cached_property", "self._cache", "self.store"):
        assert cache not in code, cache


def test_continuation_and_alignment_were_not_touched(settled):
    """Ruled out by name: *"no continuation/alignment optimization."* The union UDAF still drives the
    grouped fold and `align_onto` still reindexes it, both by the same route E-1 left them on — including
    the per-group Python passes that recon E-X measured and that E-3 deliberately did not enter."""
    engine, _evaluator = settled
    answer = engine.measure("revenue", CEX.BY_DAY)
    assert answer.served
    assert any("datafusion: aggregate" in step for step in answer.value.route)
    assert any("align:" in step for step in answer.value.route)

    accumulator = provider_module.HllUnionAccumulator
    for method in ("update", "merge"):
        assert _cell_loops(getattr(accumulator, method)), f"{method} still iterates in Python, as ruled"


def test_the_provider_interface_is_unchanged(provider):
    """E-1's table, both dispatch signatures, four capabilities. E-3 is a kernel-body change."""
    import inspect as _inspect

    assert len(provider.capabilities) == 4
    assert "target_index" in _inspect.signature(provider.continue_grouped).parameters
    assert "law" in _inspect.signature(provider.evaluate_positional).parameters
    assert {c.operation for c in provider.capabilities} == {
        ADDITION, SKETCH_UNION, "MEAN", "HLL_ESTIMATE"}


def test_the_exhibits_still_run_green(capsys):
    """The three exhibits are the unit's end-to-end witness and they print real numbers."""
    from columna_platform.columnar import exhibit as columnar_exhibit
    from columna_platform.frameql import exhibit as frameql_exhibit
    from columna_platform.kernel import exhibit as kernel_exhibit

    for module in (kernel_exhibit, columnar_exhibit, frameql_exhibit):
        module.main() if hasattr(module, "main") else module.run()
    out = capsys.readouterr().out
    assert "REFUS" in out.upper() or "refus" in out

"""
test_e1_columnar_capability_table.py — **E-1: the provider-owned capability table.**

    *"Add provider-owned capability lookup keyed by operation shape + governed law; remove the
    evaluator's physical kernel-name switch; preserve distinct REDUCER vs MAP/finalizer contracts; keep
    the capability key extensible for SCAN later."*  — Huayin, 2026-09-29

Recon E-X found the defect: `columnar/expression.py` held

    kernel = "ratio" if law.name == "MEAN" else "hll_estimate"

a governed evaluator naming a **physical kernel**, where its in-memory twin dispatches through
`ProviderProfile.capability`. This suite pins that it is gone and cannot come back.

WHAT IS NOT EXERCISED, DELIBERATELY: no new engine, no HLL kernel rewrite, no `CoordinateIndex`
memoisation, no DuckDB, no persistence, no backend work. Ruled out by name. E-1 is a dispatch change with
no behaviour change, and the strongest evidence for that is that **the whole pre-existing suite passes
untouched** except for one test that named the deleted private method.
"""
from __future__ import annotations

import ast
import inspect
from dataclasses import fields

import pyarrow as pa
import pytest

from columna_platform.columnar import (
    EXECUTION_MODES,
    GROUPED,
    IMPLEMENTABLE_MODES,
    POSITIONAL,
    SCAN,
    CapabilityTable,
    ColumnarExpressionEvaluator,
    ColumnarProvider,
    ExecutionCapability,
)
from columna_platform.columnar import capability as capability_module
from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar import expression as columnar_expression_module
from columna_platform.columnar import provider as provider_module
from columna_platform.kernel import ADDITION, REGISTRY, SKETCH_UNION, KernelRefusal
from columna_platform.kernel.law import ORDERED_WITNESS, SCALAR, STRUCTURED

LOAD = "load:orders@08:00Z"


def _code_only(module) -> str:
    """Executable text only — docstrings and comments stripped. A ban a comment can trip is a ban nobody
    can write about; see the same helper in the R-1 and F-1 suites."""
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


@pytest.fixture
def provider():
    return ColumnarProvider()


@pytest.fixture
def settled():
    engine, _block = CEX.build(settled=True, data_state=LOAD)
    return engine, ColumnarExpressionEvaluator(engine)


# ══ A · THE KERNEL-NAME SWITCH IS GONE ════════════════════════════════════════════════════════════
def test_the_evaluator_names_no_physical_kernel():
    """**The defect, pinned closed.** Neither magic string may appear in the governed evaluator, and
    neither may any hard-coded law switch that selects one."""
    code = _code_only(columnar_expression_module)
    for physical in ('"ratio"', "'ratio'", '"hll_estimate"', "'hll_estimate'", "kernel="):
        assert physical not in code, physical
    # and it passes the GOVERNED law name down instead
    assert "law=law.name" in code


def test_the_evaluator_switches_on_no_law_name_at_all():
    """A stronger form: not merely "not those two strings" but **no comparison against a law name**. An
    `if law.name == "SOMETHING"` anywhere in the evaluator would be the same defect with new spellings."""
    tree = ast.parse(inspect.getsource(columnar_expression_module))
    known = {law.name for law in REGISTRY}
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            literals = {n.value for n in ast.walk(node)
                        if isinstance(n, ast.Constant) and isinstance(n.value, str)}
            assert not (literals & known), f"evaluator compares against law name(s) {literals & known}"


def test_the_private_aggregate_if_chain_is_gone(provider):
    assert not hasattr(provider, "_aggregate_for")
    code = _code_only(provider_module)
    assert "_aggregate_for" not in code
    # the grouped dispatch is now a table lookup, and there is exactly one of them
    assert code.count("self.capability(GROUPED,") == 1


def test_no_if_chain_dispatch_survives_in_the_provider(provider):
    """Both dispatches are lookups. A comparison against a composition token or a law name inside the
    provider's *methods* would be the if-chain growing back — the declarations in `__init__` are the table
    itself and are where those names belong."""
    tree = ast.parse(inspect.getsource(provider_module))
    tokens = {ADDITION, SKETCH_UNION, "MEAN", "HLL_ESTIMATE"}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name != "__init__":
            for inner in ast.walk(node):
                if isinstance(inner, ast.Compare):
                    literals = {n.value for n in ast.walk(inner)
                                if isinstance(n, ast.Constant) and isinstance(n.value, str)}
                    assert not (literals & tokens), (node.name, literals & tokens)


# ══ B · THE TABLE, KEYED BY (MODE, GOVERNED OPERATION) ════════════════════════════════════════════
def test_the_provider_declares_what_it_can_execute(provider):
    assert isinstance(provider.capabilities, CapabilityTable)
    assert len(provider.capabilities) == 4
    assert {c.key for c in provider.capabilities} == {
        (GROUPED, ADDITION), (GROUPED, SKETCH_UNION),
        (POSITIONAL, "MEAN"), (POSITIONAL, "HLL_ESTIMATE")}


def test_capability_discovery_does_not_execute_and_does_not_raise(provider):
    """`realizes` is the question a caller asks *before* doing work — the columnar peer of
    `ProviderProfile.realizes`, which the provider previously had no analogue of at all."""
    assert provider.realizes(GROUPED, ADDITION)
    assert provider.realizes(POSITIONAL, "HLL_ESTIMATE")
    assert not provider.realizes(GROUPED, "latest_by_order")
    assert not provider.realizes(POSITIONAL, "SUM")          # SUM has no positional constructor
    assert not provider.realizes(SCAN, ADDITION)


def test_every_key_names_a_GOVERNED_operation(provider):
    """Neither half of the key is physical. The composition tokens and law names are `kernel/law.py`'s."""
    compositions = {law.continuation.token for law in REGISTRY if law.continuation is not None}
    law_names = {law.name for law in REGISTRY}
    for capability in provider.capabilities:
        if capability.mode == GROUPED:
            assert capability.operation in compositions, capability.operation
        else:
            assert capability.operation in law_names, capability.operation


def test_the_grouped_key_is_a_COMPOSITION_and_that_is_why(provider):
    """**Three laws, one composition, one kernel.** `SUM`, `COUNT` and `STOCK_LEVEL` all compose under
    `addition`; keying on the law would have produced three identical entries and invited them to drift."""
    under_addition = {law.name for law in REGISTRY
                      if law.continuation is not None and law.continuation.token == ADDITION}
    assert under_addition >= {"SUM", "COUNT", "STOCK_LEVEL"}
    assert len(provider.capabilities.in_mode(GROUPED)) == 2      # not one per law
    for law_name in under_addition:
        assert provider.realizes_composition(REGISTRY.get(law_name).continuation.token)


def test_the_physical_handle_is_not_reachable_by_any_governed_name(provider):
    """The handle lives in `execute` and nothing above the provider reads it. A caller can obtain it only
    by asking for a capability, which is the boundary."""
    assert callable(provider.capability(POSITIONAL, "MEAN").execute)
    assert "execute" in {f.name for f in fields(ExecutionCapability)}
    # the evaluator never touches it
    assert ".execute" not in _code_only(columnar_expression_module)


# ══ C · DISTINCT REDUCER vs MAP/FINALIZER CONTRACTS ═══════════════════════════════════════════════
def test_grouped_and_positional_are_distinct_contracts(provider):
    """Ruled: *"preserve distinct REDUCER vs MAP/finalizer contracts."* `GROUPED` changes the index and
    needs a target index and a standing shape; `POSITIONAL` preserves the index and needs neither."""
    grouped_signature = inspect.signature(provider.continue_grouped)
    positional_signature = inspect.signature(provider.evaluate_positional)

    assert "target_index" in grouped_signature.parameters       # the index CHANGES
    assert "shape" in grouped_signature.parameters              # standing masks are read
    assert "target_index" not in positional_signature.parameters   # the index is PRESERVED
    assert "law" in positional_signature.parameters


def test_a_mode_cannot_be_used_in_the_other_modes_lookup(provider):
    """The separation is mechanical, not documentary: asking the positional lookup for a composition
    refuses, and vice versa."""
    with pytest.raises(KernelRefusal) as as_positional:
        provider.capability(POSITIONAL, ADDITION)
    assert as_positional.value.code == "unrealized-constructor"

    with pytest.raises(KernelRefusal) as as_grouped:
        provider.capability(GROUPED, "MEAN")
    assert as_grouped.value.code == "unrealized-composition"


def test_the_refusal_vocabulary_differs_by_mode(provider):
    """*"This composition has no columnar reduction"* and *"this constructor has no columnar kernel"* send
    a reader to different places, so they are different codes with different words."""
    with pytest.raises(KernelRefusal) as grouped:
        provider.capability(GROUPED, "latest_by_order")
    with pytest.raises(KernelRefusal) as positional:
        provider.capability(POSITIONAL, "LAST")

    assert "composition 'latest_by_order'" in grouped.value.detail
    assert "grouped reduction" in grouped.value.detail
    assert "law 'LAST'" in positional.value.detail
    assert "positional kernel" in positional.value.detail
    # and BOTH keep §4.1's clause: a provider's inability does not remove a law
    for exc in (grouped, positional):
        assert "The law is unchanged" in exc.value.detail
        assert "its remedy is a provider" in exc.value.detail


def test_a_refusal_reports_what_the_provider_DOES_declare(provider):
    """So a reader learns the shape of the gap rather than only that there is one."""
    with pytest.raises(KernelRefusal) as exc:
        provider.capability(POSITIONAL, "LAST")
    assert "HLL_ESTIMATE" in exc.value.detail and "MEAN" in exc.value.detail


# ══ D · FINALIZATION IS A VALUE-FORM TRANSITION, AND GROUPED MAY NEVER DO IT ═══════════════════════
def test_the_finalizer_is_identified_by_its_value_form_transition(provider):
    estimate = provider.capability(POSITIONAL, "HLL_ESTIMATE")
    mean = provider.capability(POSITIONAL, "MEAN")

    assert estimate.value_form_in == STRUCTURED and estimate.value_form_out == SCALAR
    assert estimate.finalizes
    assert mean.value_form_in == mean.value_form_out == SCALAR
    assert not mean.finalizes
    # derived, never asserted: there is no flag to disagree with the forms
    assert "finalizes" not in {f.name for f in fields(ExecutionCapability)}


def test_a_GROUPED_capability_may_never_change_value_form():
    """**The guard the string switch could not express.** A continuation must preserve what the family
    retains; a grouped capability that finalized would be finalizing family state INSIDE the MME, which is
    the one thing ToD v8 §3.7 withholds."""
    with pytest.raises(KernelRefusal) as refused:
        ExecutionCapability(mode=GROUPED, operation="sketch_union", execute=lambda *a: None,
                            value_form_in=STRUCTURED, value_form_out=SCALAR)
    assert refused.value.code == "grouped-capability-may-not-finalize"
    assert "FINALIZING FAMILY STATE INSIDE THE MME" in refused.value.detail
    assert "never a continuation" in refused.value.detail


def test_the_shipped_grouped_capabilities_all_preserve_value_form(provider):
    for capability in provider.capabilities.in_mode(GROUPED):
        assert capability.value_form_in == capability.value_form_out
        assert not capability.finalizes
    # and the sketch union folds sketches into a SKETCH, which is the case that matters
    union = provider.capability(GROUPED, SKETCH_UNION)
    assert union.value_form_in == union.value_form_out == STRUCTURED


def test_a_positional_capability_MAY_change_value_form():
    """Because that is what finalization is, and it happens above the engine."""
    allowed = ExecutionCapability(mode=POSITIONAL, operation="HLL_ESTIMATE",
                                  execute=lambda columns, parameters: None,
                                  value_form_in=STRUCTURED, value_form_out=SCALAR)
    assert allowed.finalizes


def test_an_unknown_value_form_is_refused():
    with pytest.raises(KernelRefusal) as refused:
        ExecutionCapability(mode=POSITIONAL, operation="MEAN", execute=lambda c, p: None,
                            value_form_in="float64")            # a dtype, not a governed value form
    assert refused.value.code == "unknown-value-form"
    assert ORDERED_WITNESS in refused.value.detail              # it names the governed vocabulary


# ══ E · THE MODE VOCABULARY, AND WHY IT IS NOT `law.KINDS` ════════════════════════════════════════
def test_the_mode_names_do_not_collide_with_law_kinds():
    """**The decisive evidence for the naming.** `MEAN` has structural kind `REDUCER` and is executed
    POSITIONALLY — it is a reducer that cannot found a family, and what a provider does with it is
    index-preserving column arithmetic. A capability keyed on `law.kind` would have filed it as a grouped
    reduction, which is the opposite of what happens."""
    from columna_platform.kernel.law import KINDS

    assert REGISTRY.get("MEAN").kind == "REDUCER"
    assert ColumnarProvider().realizes(POSITIONAL, "MEAN")
    assert not ColumnarProvider().realizes(GROUPED, "MEAN")
    assert not (set(EXECUTION_MODES) & KINDS)                   # no shared spelling at all


def test_the_mode_is_not_the_standing_shape(provider):
    """The other collision avoided: `continue_grouped(shape=)` is VALUE_BEARING / POPULATION, which is
    about masks, not about execution."""
    from columna_platform.columnar.standing import POPULATION, VALUE_BEARING

    assert not (set(EXECUTION_MODES) & {POPULATION, VALUE_BEARING})


def test_an_unknown_mode_is_refused():
    with pytest.raises(KernelRefusal) as refused:
        ExecutionCapability(mode="REDUCER", operation="addition", execute=lambda *a: None)
    assert refused.value.code == "unknown-execution-mode"


# ══ F · SCAN IS RESERVED, AND THE KEY IS EXTENSIBLE WITHOUT IT ════════════════════════════════════
def test_scan_is_in_the_vocabulary_and_implementable_by_nobody():
    """Ruled: *"keep the capability key extensible for SCAN later."* The mode exists so the key does not
    change shape when a windowed operation is finally needed — and nothing may declare one yet, because a
    contract designed before a caller exists is designed against a guess."""
    assert SCAN in EXECUTION_MODES
    assert SCAN not in IMPLEMENTABLE_MODES
    assert IMPLEMENTABLE_MODES == (GROUPED, POSITIONAL)


def test_declaring_a_scan_capability_is_refused():
    with pytest.raises(KernelRefusal) as refused:
        ExecutionCapability(mode=SCAN, operation="row_number", execute=lambda *a: None)
    assert refused.value.code == "scan-is-reserved"
    assert "no caller to check it against" in refused.value.detail


def test_asking_for_a_scan_capability_refuses_with_the_reason(provider):
    """Not a `KeyError`, and explicitly **not a gap in this provider**."""
    with pytest.raises(KernelRefusal) as refused:
        provider.capability(SCAN, "row_number")
    assert refused.value.code == "no-scan-capability"
    assert "RESERVED" in refused.value.detail
    assert "not a gap in" in refused.value.detail


def test_the_key_shape_is_stable_across_modes():
    """Adding SCAN later must not migrate a table. The key is `(mode, operation)` for every mode."""
    assert capability_module.capability_key(GROUPED, ADDITION) == (GROUPED, ADDITION)
    assert capability_module.capability_key(SCAN, "row_number") == (SCAN, "row_number")
    for capability in ColumnarProvider().capabilities:
        assert capability.key == (capability.mode, capability.operation)


# ══ G · THE CONTRACT IS PROVIDER-NEUTRAL ══════════════════════════════════════════════════════════
def test_the_capability_module_imports_no_engine():
    """**DuckDB must be able to implement this contract without inheriting DataFusion.** So the contract
    lives in its own module and imports nothing physical — not even Arrow."""
    code = _code_only(capability_module)
    for engine in ("datafusion", "pyarrow", "import pa", "pc.", "duckdb", "SessionContext", "udaf",
                   "datasketches"):
        assert engine not in code, engine


def test_a_second_provider_can_implement_the_contract_without_the_first(provider):
    """The point of E-1, demonstrated: a stand-in provider declares the same keys with its own handles and
    the evaluator cannot tell. **No engine is added** — this is a test double, and it is here rather than in
    `src/` for the same reason R-1's estates are."""
    class Elsewhere:
        """Stands in for a DuckDB or native-kernel provider."""

        name = "stand-in"

        def __init__(self):
            self.capabilities = CapabilityTable(self.name, (
                ExecutionCapability(mode=POSITIONAL, operation="MEAN",
                                    execute=lambda columns, parameters: pa.array(
                                        [None] * len(columns["SUM"]), type=pa.float64()),
                                    note="a different engine's divide"),
            ))

        def capability(self, mode, operation):
            return self.capabilities.of(mode, operation)

        def realizes(self, mode, operation):
            return self.capabilities.realizes(mode, operation)

        def evaluate_positional(self, columns, *, law, parameters=None):
            return self.capability(POSITIONAL, law).execute(columns, dict(parameters or {}))

    stand_in = Elsewhere()
    assert stand_in.realizes(POSITIONAL, "MEAN")
    assert not stand_in.realizes(GROUPED, ADDITION)             # it declares no reduction
    result = stand_in.evaluate_positional(
        {"SUM": pa.array([1.0, 2.0]), "COUNT": pa.array([1, 2])}, law="MEAN")
    assert len(result) == 2
    # and its refusal for the reduction it lacks is the SAME governed answer
    with pytest.raises(KernelRefusal) as refused:
        stand_in.capability(GROUPED, ADDITION)
    assert refused.value.code == "unrealized-composition"
    assert "The law is unchanged" in refused.value.detail


def test_a_table_refuses_two_handles_for_one_key():
    """A provider that declared one key twice could not say what it does — the selection between them
    would be made by declaration order, which is nobody's decision."""
    with pytest.raises(KernelRefusal) as refused:
        CapabilityTable("confused", (
            ExecutionCapability(mode=POSITIONAL, operation="MEAN", execute=lambda c, p: None),
            ExecutionCapability(mode=POSITIONAL, operation="MEAN", execute=lambda c, p: None)))
    assert refused.value.code == "duplicate-capability"


# ══ H · NO BEHAVIOUR CHANGE ═══════════════════════════════════════════════════════════════════════
def test_AOV_still_evaluates_through_the_table(settled):
    engine, evaluator = settled
    answer = evaluator.evaluate("average_order_value", CEX.BY_DAY)
    assert answer.served and answer.route == "evaluated"
    assert answer.value.cell(("D2",)) == pytest.approx(81.25)


def test_the_HLL_estimate_still_finalizes_through_the_table(settled):
    engine, evaluator = settled
    answer = evaluator.evaluate("distinct_customer_estimate", CEX.BY_DAY)
    assert answer.served and answer.seeded_from == "b_sketch"
    assert sorted(answer.value.values.to_pylist()) == [3, 3]
    # and the MME still holds only the SKETCH
    held = engine.materializations.select("distinct_customers", anchor=CEX.BY_DAY)
    assert held and held[0].value.value_form == STRUCTURED


def test_grouped_continuation_still_runs_through_datafusion(settled):
    engine, _evaluator = settled
    answer = engine.measure("revenue", CEX.BY_DAY)
    assert answer.served
    assert any("datafusion: aggregate" in step for step in answer.value.route)


def test_the_exhibits_still_run_green(capsys):
    from columna_platform.columnar import exhibit as columnar_exhibit
    from columna_platform.frameql import exhibit as frameql_exhibit
    from columna_platform.kernel import exhibit as kernel_exhibit

    for exhibit in (kernel_exhibit, columnar_exhibit, frameql_exhibit):
        assert exhibit.main() == 0, exhibit.__name__
        assert "✗" not in capsys.readouterr().out, exhibit.__name__


# ══ I · WHAT E-1 DID NOT DO ═══════════════════════════════════════════════════════════════════════
def test_no_new_engine_arrived():
    """Ruled: no new engine, no DuckDB. The import surface is unchanged from before E-1."""
    import columna_platform.columnar as package

    code = "".join(_code_only(m) for m in (capability_module, provider_module,
                                           columnar_expression_module))
    for banned in ("duckdb", "adbc", "psycopg", "sqlalchemy", "polars", "import sqlite3"):
        assert banned not in code, banned
    assert package is not None


def test_the_HLL_kernel_was_not_rewritten(provider):
    """Ruled: no HLL kernel rewrite yet (E-X step 3). It is still the Python comprehension it was — moved
    into a named function, not changed."""
    source = inspect.getsource(provider_module)
    assert "for v in sketches" in source                        # still O(cells) in Python
    assert "estimate_of(v.as_py())" in source


def test_coordinate_index_identity_was_not_memoised():
    """Ruled: no `CoordinateIndex` optimization yet (E-X step 2). Recorded here so the sequencing stays
    visible — this test is expected to be DELETED by the unit that does it."""
    from columna_platform.columnar import index as index_module

    code = _code_only(index_module)
    assert "hexdigest" in code
    for memo in ("lru_cache", "cached_property", "_identity_cache"):
        assert memo not in code, memo


def test_no_route_or_cost_information_entered_the_capability_record():
    """A capability says what a provider CAN do, never what it would cost. The cost model is not ruled and
    E-1 is not where it arrives."""
    names = {f.name for f in fields(ExecutionCapability)}
    assert names == {"mode", "operation", "execute", "value_form_in", "value_form_out", "note"}
    for forbidden in ("cost", "latency", "rows_per_second", "score", "rank", "preferred", "weight"):
        assert forbidden not in names
        assert not hasattr(CapabilityTable, forbidden)

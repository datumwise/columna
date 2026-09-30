"""
B-2's two seam corrections, proved in the package that owns them.

    **Choose the Arrow-native Platform path and repair the substrate abstraction above it. Do not weaken
    the columnar state model or convert Arrow into Python cache objects merely to preserve an in-memory
    serving assumption.**  — Huayin, 2026-09-30 (B-2, the ruling)

SEAM 2  `FrameQLService` went through `mme.measure` and therefore could never reach a provider: a cold
        family came back unserved and was classified as a refusal. It now goes through
        `FulfillmentCoordinator`, and **there is no fallback path** (ruled §1).
SEAM 3  `FrameQLService` read `answer.value.cells`, a `Mapping` only the in-memory substrate has, so it
        could not serve one query over the columnar engine. The shared surface is `coordinates` +
        `cell(coordinate)`, and **the kernel state was widened UP to it** rather than the columnar state
        narrowed DOWN to a dict (ruled §2).
"""
from __future__ import annotations

import ast
import inspect
import textwrap

import pyarrow as pa
import pytest

from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar.mme import ColumnarExpressionOutput, ColumnarFamilyState
from columna_platform.frameql import FrameQLService
from columna_platform.frameql import serving as serving_module
from columna_platform.kernel import exhibit as KEX
from columna_platform.kernel.fulfillment import (
    INCOMPLETE,
    NOT_SUPPORTED,
    ROUTE_POLICY_NEEDED,
    UNAVAILABLE,
    FulfillmentCoordinator,
)
from columna_platform.kernel.geometry import KernelRefusal
from columna_platform.kernel.value import ExpressionOutput, FamilyState

MANIFOLD = "andfam.commerce"


def _code_only(obj) -> str:
    """Source with every docstring removed. **A structural test must read CODE, not prose.**

    The first draft of this file asserted `"mme.measure" not in inspect.getsource(FrameQLService)` and
    failed — on the very comment that explains why the direct path was removed. A guard that a correct
    explanation can break is a guard against writing explanations. Same shape as the B-1' suite's.

    Comments are stripped too, because `ast.unparse` does not reproduce them."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(obj)))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


# ══ SEAM 2 · THE SERVING PATH GOES THROUGH THE COORDINATOR, AND ONLY THROUGH IT ═══════════════════

def test_the_service_holds_a_coordinator_and_has_no_direct_measure_path():
    """**Ruled §1: do not preserve the direct `FrameQLService → mme.measure` family path as a fallback.**

    A structural pin, because the defect was one line and a future edit could put it back without any
    behavioural test noticing on a warm world — which is the only kind of world the suite had."""
    code = _code_only(FrameQLService)
    assert "self.coordinator" in code
    assert "mme.measure" not in code, "the direct cache path is back"
    assert "self.coordinator.fulfill(" in code
    # A service built with no coordinator gets a real one over an EMPTY estate, not a bypass.
    default = FrameQLService(KEX.build())
    assert isinstance(default.coordinator, FulfillmentCoordinator)
    assert default.coordinator.realization.providers == ()


def test_a_warm_world_serves_identically_through_the_coordinator():
    """The correction is behaviour-preserving where a provider is irrelevant."""
    service = FrameQLService(KEX.build())
    outcome = service.serve("SELECT revenue AT {day}")
    assert outcome.classification == "serve"
    assert len(outcome.frame.rows) == 2


def test_a_cold_family_is_lawful_but_unavailable_and_NOT_an_analytical_refusal():
    """**Ruled §7: do not turn `lawful but unavailable` into an analytical refusal.**

    Before B-2 this ask was classified `REFUSE` — the engine's *"I do not hold it"* read as a verdict about
    the question. The question is fine and nobody can answer it, which are different sentences."""
    authority_world = _cold_kernel_world()
    service = FrameQLService(authority_world)
    outcome = service.serve("SELECT revenue AT {day}")
    assert outcome.classification != "refuse"
    assert outcome.classification == "unsupported"
    assert outcome.refusal.code == UNAVAILABLE
    assert "NOT A CLAIM THAT THE BUILD CANNOT DO IT" in outcome.refusal.detail
    assert "vocabulary gap" in outcome.refusal.detail


def test_the_three_estate_moods_keep_their_own_codes_rather_than_being_collapsed():
    """The recorded vocabulary gap is findable **by code**, which is the whole reason it is stamped."""
    code = _code_only(FrameQLService._not_served)
    for mood_name in ("UNAVAILABLE", "ROUTE_POLICY_NEEDED", "INCOMPLETE"):
        assert mood_name in code, mood_name
    # And the mapping that IS truthful is written as a mapping, not left to a fallthrough.
    assert "mood == NOT_SUPPORTED" in code
    # **THE ESTATE MOODS ARE TESTED BEFORE ANY CARRIED REFUSAL**, which is what keeps a cache miss from
    # being classified as an analytical refusal on the in-memory engine.
    assert code.index("ROUTE_POLICY_NEEDED") < code.index("answer.refusal.code")
    # The four mood constants are IMPORTED rather than spelled as literals, so a rename in
    # `fulfillment.py` cannot leave this mapping silently matching nothing.
    for mood in (UNAVAILABLE, ROUTE_POLICY_NEEDED, INCOMPLETE, NOT_SUPPORTED):
        assert getattr(serving_module, _const_name(mood)) == mood


def test_a_governed_verdict_still_classifies_itself_and_carries_the_mood_alongside():
    """A refusal about the ASK stays `REFUSE` with its own code; the mood is appended, never substituted."""
    service = FrameQLService(KEX.build())
    # `on_hand` is a STOCK: lawful across stores, unlawful across time. The frameql exhibit's PROOF 5.
    outcome = service.serve("SELECT on_hand AT {store}")
    assert outcome.classification == "refuse", outcome.render()
    assert outcome.refusal.code not in (UNAVAILABLE, NOT_SUPPORTED, INCOMPLETE, ROUTE_POLICY_NEEDED)
    assert "fulfilment mood" in outcome.refusal.detail, "the mood is carried alongside, not dropped"


def test_the_expression_path_was_deliberately_left_alone():
    """**Recorded, not fixed** (ruled §8). `fulfill_expression` hands the evaluator a `GovernedExpression`
    object; the columnar evaluator takes an `expression_id` string. B-2 is one family request, so the
    service still evaluates expressions directly and does not route them through the coordinator."""
    code = _code_only(FrameQLService)
    assert "self.expressions.evaluate(" in code
    assert "fulfill_expression" not in code
    service = FrameQLService(KEX.build())
    assert service.serve("SELECT average_order_value AT {}").classification in ("serve", "disclose")


# ══ SEAM 3 · ONE READ SURFACE, AND IT IS THE STRONGER ONE ═════════════════════════════════════════

def test_both_substrates_implement_the_same_family_state_read_surface():
    for state_type in (FamilyState, ColumnarFamilyState):
        assert hasattr(state_type, "coordinates"), state_type
        assert hasattr(state_type, "cell"), state_type
    for output_type in (ExpressionOutput, ColumnarExpressionOutput):
        assert hasattr(output_type, "coordinates"), output_type
        assert hasattr(output_type, "cell"), output_type


def test_the_columnar_states_values_stay_in_arrow_behind_the_neutral_surface():
    """The surface is neutral; **the payload is not converted to make it so.** `cell` reads one position
    out of an Arrow array on demand, which is a different thing from materializing a dict of every cell."""
    mme, _ = CEX.build(MANIFOLD, settled=True)
    state = mme.measure("revenue", CEX.SALE_AT).value
    assert isinstance(state.values, (pa.Array, pa.ChunkedArray))
    assert len(state.coordinates) == len(state.values)


def test_no_cells_mapping_was_added_to_the_columnar_state():
    """**Ruled §2: do not add a `.cells` dictionary to `ColumnarFamilyState`.** Its absence is the whole
    load-bearing fact — a dict cannot refuse."""
    assert not hasattr(ColumnarFamilyState, "cells")
    assert "cells" not in ColumnarFamilyState.__dataclass_fields__
    assert not hasattr(ColumnarExpressionOutput, "cells")


def test_the_frame_builder_reads_only_the_neutral_surface():
    code = _code_only(serving_module.FrameQLService._frame)
    assert ".cells" not in code, "the frame builder reaches for the in-memory representation again"
    assert ".coordinates" in code
    assert ".cell(" in code


def test_frameql_serves_over_the_columnar_engine():
    """**THE REGRESSION.** Before B-2 this raised `AttributeError: 'ColumnarFamilyState' object has no
    attribute 'cells'` — the service could not answer one query over Arrow-backed state."""
    mme, _ = CEX.build(MANIFOLD, settled=True)
    service = FrameQLService(mme)
    outcome = service.serve("SELECT revenue AT {day}")
    assert outcome.classification == "serve", outcome.render()
    assert [row[0] for row in outcome.frame.rows] == ["D1", "D2"]


def test_frameql_serves_over_the_in_memory_engine_unchanged():
    """The same query, the other substrate, and the service is told which it holds by nobody."""
    service = FrameQLService(KEX.build())
    outcome = service.serve("SELECT revenue AT {day}")
    assert outcome.classification == "serve", outcome.render()
    assert [row[0] for row in outcome.frame.rows] == ["D1", "D2"]


def test_a_want_of_state_point_is_REFUSED_in_the_frame_and_never_printed_as_an_absence():
    """**THIS IS WHAT THE RULING BOUGHT, AND IT IS OBSERVABLE.**

    The root state IS held here, so the engine serves it and the frame builder is the first thing to ask
    for O7's value. `ColumnarFamilyState.cell` refuses — the point PARTICIPATES and its required value is
    not established — and the outcome is a governed `REFUSE` carrying that code.

    **Had a `.cells` mapping been added instead, this query would have SERVED**, printing a dash or a null
    where a participating point's missing value belongs, and a caller would have had an absence to
    interpret. The stronger semantics survived the abstraction, which is what §2 required."""
    mme, _ = CEX.build(MANIFOLD, settled=False)             # AS RECORDED: O7's amount not established
    outcome = FrameQLService(mme).serve("SELECT revenue AT {store, day, order}")
    assert outcome.classification == "refuse", outcome.render()
    assert outcome.refusal.code == "want-of-state-at-a-point"
    assert outcome.frame is None, "no frame was built, so no cell was improvised"
    assert "not established" in outcome.refusal.detail


def test_the_same_world_settled_serves_that_very_point():
    """The control: one support bit and one amount apart."""
    mme, _ = CEX.build(MANIFOLD, settled=True)
    outcome = FrameQLService(mme).serve("SELECT revenue AT {store, day, order}")
    assert outcome.classification == "serve", outcome.render()
    assert len(outcome.frame.rows) == 7


def test_a_want_of_state_point_is_still_LISTED_as_covered():
    """`coordinates` includes it and `cell` refuses it. **Two facts, two answers** — omitting the point
    would make the list a silent claim of nonparticipation."""
    mme, _ = CEX.build(MANIFOLD, settled=False)
    state = mme.measure("revenue", CEX.SALE_AT).value
    wanting = state.points_wanting_state()
    assert len(wanting) == 1
    assert wanting[0] in state.coordinates
    with pytest.raises(KernelRefusal) as raised:
        state.cell(wanting[0])
    assert raised.value.code == "want-of-state-at-a-point"


def test_the_kernel_states_refusal_is_absence_and_it_is_a_governed_refusal_too():
    """The widened kernel surface does not return `None` for a point it does not hold."""
    state = FamilyState(point=KEX._families()[0].root and _point(), law="SUM", value_form="scalar",
                        cells={("a",): 1.0}, instance=_instance())
    assert state.coordinates == (("a",),)
    assert state.cell(("a",)) == 1.0
    with pytest.raises(KernelRefusal) as raised:
        state.cell(("b",))
    assert raised.value.code == "no-value-at-this-point"


def test_an_absent_series_cell_is_still_reported_as_absent_and_not_as_zero():
    """§4.3's undefined-on-basis case is unchanged: a dash, and never a `0`. The correction replaced a
    `dict.get` DEFAULT with a membership test, which is what kept these two conditions apart."""
    service = FrameQLService(KEX.build())
    outcome = service.serve("SELECT revenue, audited_order_count AT {store, day, order}")
    assert outcome.classification in ("serve", "disclose"), outcome.render()
    rendered = outcome.frame.render()
    assert "—" in rendered, rendered


# ── helpers ───────────────────────────────────────────────────────────────────────────────────────

def _const_name(mood: str) -> str:
    return {UNAVAILABLE: "UNAVAILABLE", ROUTE_POLICY_NEEDED: "ROUTE_POLICY_NEEDED",
            INCOMPLETE: "INCOMPLETE", NOT_SUPPORTED: "NOT_SUPPORTED"}[mood]

def _cold_kernel_world():
    """A constituted in-memory MME with **no root established** and no estate behind it."""
    from columna_platform.kernel import IN_MEMORY, MME, REGISTRY

    mme = MME(KEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=MANIFOLD)
    for family in KEX._families():
        mme.register_family(family)
    return mme


def _point():
    from columna_platform.kernel.geometry import Anchor
    from columna_platform.kernel.sorts import FamilyPoint

    return FamilyPoint("revenue", Anchor(universe="commerce", constituents=frozenset({"day"})))


def _instance():
    from columna_platform.kernel.standing import AnalyticalInstance

    return AnalyticalInstance(manifold=MANIFOLD, universe="commerce", participation="p",
                              constitution_context=f"{MANIFOLD}@build-1", data_state="data:unstated")

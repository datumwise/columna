"""The three findings — now as GUARDED FACTS about their repairs.

Findings 1 and 2 were accidental seams and are CLOSED. These tests no longer assert that the gaps
exist; they assert that the repairs hold, so a later change cannot quietly reopen them. Finding 3 was
never a seam — it is a real distinction in the law, and it stays asserted as one.
"""
import ast
import inspect
import subprocess
import sys
from pathlib import Path

import pytest

CORE = Path(__file__).resolve().parents[2] / "columna-core" / "src" / "columna_core"
PLATFORM = Path(__file__).resolve().parents[1] / "src" / "columna_platform"

EXECUTION_STACK = {"planner", "engine", "model", "projection", "frameql", "expr", "adjudication",
                   "connector", "parser"}


def _relative_imports(path: Path) -> set:
    """Module names this file imports from its own package (`from .x import ...`)."""
    out = set()
    for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(n, ast.ImportFrom) and n.level and n.module:
            out.add(n.module.split(".")[0])
    return out


def _closure(start: str) -> set:
    """Transitive intra-package import closure, statically — independent of package `__init__`."""
    seen, todo = set(), [start]
    while todo:
        mod = todo.pop()
        if mod in seen:
            continue
        seen.add(mod)
        f = CORE / f"{mod}.py"
        if f.exists():
            todo.extend(_relative_imports(f) - seen)
    return seen - {start}


# ── FINDING 1 · CLOSED — the wire's types no longer belong to the planner ────────────────────────
def test_the_serving_contract_owns_the_wire_result_types():
    src = (CORE / "serving_contract.py").read_text(encoding="utf-8")
    assert "class FrameResult:" in src and "class ColumnResult:" in src


def test_there_is_exactly_one_definition_not_a_second_enumeration():
    """`planner` RE-EXPORTS. A copy would be strictly worse than the seam it replaced."""
    from columna_core import planner, serving_contract
    assert planner.FrameResult is serving_contract.FrameResult
    assert planner.ColumnResult is serving_contract.ColumnResult
    assert (CORE / "planner.py").read_text(encoding="utf-8").count("class FrameResult") == 0


def test_existing_imports_still_work():
    import columna_core
    from columna_core.planner import ColumnResult, FrameResult          # noqa: F401
    assert columna_core.FrameResult is FrameResult


def test_the_serving_contract_does_not_reach_the_execution_stack():
    assert not (_closure("serving_contract") & EXECUTION_STACK)


def test_the_wire_does_not_reach_the_execution_stack():
    """THE ARCHITECTURAL PROPERTY. Asserted over the STATIC closure, which is the real claim —
    `columna_core/__init__` still imports the planner eagerly at runtime, a separate and larger
    surface change that this proof was not authorized to make. Recorded, not silently relied upon."""
    assert not (_closure("disclosure_wire") & EXECUTION_STACK)


def test_wire_frame_consumes_the_neutral_type():
    from columna_core.disclosure_wire import wire_frame
    assert wire_frame.__annotations__["fr"] in ("FrameResult", __import__(
        "columna_core.serving_contract", fromlist=["FrameResult"]).FrameResult)


# ══ the integration factoring (ruled Huayin 2026-09-12 §4) ═══════════════════════════════════════

def test_the_successor_path_answers_in_the_neutral_type():
    """`decide_result` returns the architecture-neutral `FrameResult`, NOT a wire dict.

    This is the seam a serving surface consumes. If it ever returns a dict again, the server would
    be handed something already serialized and would either double-wire it or bypass its own
    stamping — which is how a second contract starts."""
    from columna_core.serving_contract import FrameResult
    from columna_platform import serving
    assert serving.decide_result.__annotations__["return"] in ("FrameResult", FrameResult)


def test_the_platform_serializes_the_wire_in_exactly_one_place():
    """ONE SERIALIZER. `wire_frame` may be called from `decide` — the standalone-proof wrapper — and
    from nowhere else in the package, because the server is the single place the wire is applied for
    the integrated path. Asserted over the AST rather than by grep, so a call inside a nested
    function or a comprehension cannot hide from it."""
    calls = []
    for f in sorted(PLATFORM.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for n in ast.walk(fn):
                if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "wire_frame":
                    calls.append(f"{f.name}::{fn.name}")
    assert calls == ["serving.py::decide"], f"wire_frame is called from {calls}"


def test_the_wrapper_still_wires_the_real_contract():
    """The factoring cost the proofs nothing: `decide` remains the wired entry point at version 5."""
    src = inspect.getsource(_serving().decide)
    assert "wire_frame(" in src and "executed=True" in src


def _serving():
    from columna_platform import serving
    return serving


def test_proof_a_does_not_import_the_excluded_stack():
    """Platform still climbs nothing. The repair was at the seam, not here."""
    forbidden = {"columna_core.planner", "columna_core.engine", "columna_core.model",
                 "columna_core.adjudication", "columna_core.connector", "columna_core.parser",
                 "columna_core.compiler.compile_v2", "duckdb", "adbc_driver_manager"}
    reached = set()
    for f in sorted(PLATFORM.glob("*.py")):
        for n in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):
            if isinstance(n, ast.Import):
                reached.update(a.name for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                reached.add(n.module)
    assert not (reached & forbidden), f"Proof A reaches for {sorted(reached & forbidden)}"


def test_the_successor_path_loads_no_execution_module_at_runtime():
    """THE RUNTIME COMPLEMENT to the static closure, in a CLEAN INTERPRETER.

    The static test says Proof A's modules do not NAME the execution stack. This one says the
    interpreter does not END UP with it loaded — which is the property that was actually asked for,
    and the one that was false until `columna_core.__init__` became lazy. Neither test replaces the
    other: a module could name nothing forbidden and still pull the stack in transitively (that was
    the bug), or name it in a docstring and pull in nothing."""
    prog = (
        "import sys\n"
        "import columna_platform.serving, columna_platform.admission, columna_platform.state\n"
        "banned = {'planner','engine','model','adjudication','parser','projection','frameql',"
        "'expr','connector'}\n"
        "loaded = {m.split('.')[1] for m in sys.modules "
        "if m.startswith('columna_core.') and m.count('.') == 1}\n"
        "print('BANNED', ' '.join(sorted(loaded & banned)))\n"
        "print('DUCKDB', 'duckdb' in sys.modules)\n"
    )
    out = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True, check=True)
    lines = {ln.split(" ", 1)[0]: (ln.split(" ", 1)[1] if " " in ln else "")
             for ln in out.stdout.splitlines()}
    assert lines["BANNED"] == "", f"Proof A loaded {lines['BANNED']} at runtime"
    assert lines["DUCKDB"] == "False"


# ── FINDING 2 · CLOSED — the registry can express a want-of-state refusal ────────────────────────
def test_the_realization_jurisdiction_now_has_a_refuse():
    from columna_core.disclosure import REASON_OUTCOME, REFUSE
    rz = [r for r, v in REASON_OUTCOME.items() if len(v) > 2 and v[2] == "realization" and v[0] == REFUSE]
    assert rz == ["want_of_state"]


def test_the_three_way_split_is_expressible():
    """want-of-law / want-of-state / error — three conditions, three verdicts, not one."""
    from columna_core.disclosure import jurisdiction_for, outcome_for
    assert outcome_for("want_of_law") == ("refuse", "unsupported")
    assert outcome_for("want_of_state") == ("refuse", "unsupported")
    assert outcome_for("unsupported") == ("error", None)
    # both refuse; JURISDICTION is what separates them
    assert jurisdiction_for("want_of_law") == "analytical"
    assert jurisdiction_for("want_of_state") == "realization"


def test_the_registry_is_still_closed_and_fail_closed():
    from columna_core.disclosure import UnregisteredReason, outcome_for
    with pytest.raises(UnregisteredReason):
        outcome_for("some_reason_nobody_registered")


def test_no_analytical_reason_was_borrowed_for_a_state_failure():
    from columna_core.disclosure import jurisdiction_for
    assert jurisdiction_for("want_of_state") != "analytical"
    # and the two reasons the registry warns about keep their own intents
    assert jurisdiction_for("blocked_reduction") == "analytical"
    assert jurisdiction_for("input_anchor_unavailable") == "analytical"


# ── FINDING 3 · STANDING — empty-fiber law is not absence law ────────────────────────────────────
def test_the_empty_fiber_distinction_is_recorded_verbatim():
    """The statement lives in the code it governs, not in a docstring beside it."""
    from columna_platform.admission import EMPTY_FIBER_RULING

    assert EMPTY_FIBER_RULING == (
        "Empty-fiber law governs evaluation of a constituted fiber with no contributions. It does "
        "not establish analytical existence, eligibility, observed support, carrier nullability, or "
        "the meaning of an absent observation."
    )


def test_c9_is_established_and_still_does_not_govern_absence(revenue):
    """The naive check would PASS here. That is the whole finding."""
    _family, view, _real = revenue
    c9 = view["exceptional_cases"]

    assert c9.standing == "established"
    assert set(c9.value) == {"empty_fiber"}

    from columna_platform.admission import _ENTAILED_NOT_ABSENCE
    assert set(c9.value) <= _ENTAILED_NOT_ABSENCE


def test_admission_inspects_c9_content_and_never_reads_standing_alone():
    from columna_platform import admission
    src = inspect.getsource(admission.admit)
    assert "_ENTAILED_NOT_ABSENCE" in src
    assert "c9.standing != ESTABLISHED" not in src


def test_no_absence_standing_axis_was_added_to_the_sse_contract():
    """Ruled 2026-09-12: do NOT invent a seventh axis from one proof. The Phase-7 question stays open."""
    sse = (Path(__file__).resolve().parents[3] / "docs" / "architecture"
           / "sse_contract_v0_1.md").read_text(encoding="utf-8")
    assert "absence standing" not in sse.lower()
    assert "six axes" in sse

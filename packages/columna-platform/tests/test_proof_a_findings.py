"""The three findings, pinned as GUARDED FACTS rather than prose.

A finding recorded only in a docstring decays into an opinion. Each test below asserts the state of
the repository that MAKES the finding true, so that if someone closes one of these gaps the test
fails and the finding is revisited deliberately instead of quietly outliving its cause.

NONE of these is a workaround. They are the shape of the wall.
"""
import ast
import inspect
from pathlib import Path

import pytest

CORE_SRC = Path(__file__).resolve().parents[2] / "columna-core" / "src" / "columna_core"


# ── FINDING 1 · the wire is unreachable inside the approved boundary ─────────────────────────────
def test_the_wire_result_types_are_owned_by_the_excluded_planner():
    """`wire_frame` needs a `FrameResult`, and `FrameResult` lives behind the legacy import wall."""
    planner = (CORE_SRC / "planner.py").read_text(encoding="utf-8")
    assert "class FrameResult:" in planner
    assert "class ColumnResult:" in planner

    tree = ast.parse(planner)
    imported = {n.module for n in ast.walk(tree)
                if isinstance(n, ast.ImportFrom) and n.level == 1 and n.module}
    # importing the wire's data types executes the whole excluded stack
    assert {"engine", "model", "projection", "frameql"} <= imported


def test_the_disclosure_wire_frame_path_consumes_that_type():
    wire = (CORE_SRC / "disclosure_wire.py").read_text(encoding="utf-8")
    assert "def wire_frame(fr" in wire
    assert "fr.columns" in wire and "fr.disclosure" in wire and "fr.anchor" in wire


def test_proof_a_does_not_import_the_excluded_stack():
    """The proof stops at the wall rather than climbing it, and this is what says so.

    Asserted over the IMPORT GRAPH, not over the file text: these modules discuss the excluded names
    in prose on purpose, and a text scan would either fail on the documentation or be defeated by
    it."""
    src = Path(__file__).resolve().parents[1] / "src" / "columna_platform"
    forbidden = {"columna_core.planner", "columna_core.engine", "columna_core.model",
                 "columna_core.adjudication", "columna_core.connector", "columna_core.parser",
                 "columna_core.compiler.compile_v2", "duckdb", "adbc_driver_manager"}

    reached = set()
    for f in sorted(src.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                reached.update(a.name for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                reached.add(n.module)

    assert not (reached & forbidden), f"Proof A reaches for {sorted(reached & forbidden)}"


# ── FINDING 2 · the closed reason registry cannot express a want-of-state refusal ────────────────
def test_no_registered_reason_can_carry_a_want_of_state_refusal():
    from columna_core.disclosure import REASON_OUTCOME, REFUSE

    realization_refusals = [r for r, v in REASON_OUTCOME.items()
                            if len(v) > 2 and v[2] == "realization" and v[0] == REFUSE]
    assert realization_refusals == [], (
        "a REFUSE reason now exists in the realization jurisdiction — FINDING 2 may be closed, and "
        f"Proof A's refusal mapping should be revisited: {realization_refusals}")


def test_the_registry_is_closed_so_borrowing_is_the_only_alternative_to_a_ruling():
    from columna_core.disclosure import UnregisteredReason, outcome_for

    with pytest.raises(UnregisteredReason):
        outcome_for("want_of_state")


def test_proof_a_did_not_mint_a_reason():
    from columna_core.disclosure import REASON_OUTCOME
    assert "want_of_state" not in REASON_OUTCOME
    assert "want_of_law" not in REASON_OUTCOME


# ── FINDING 3 · C9 established does not mean absence is governed ─────────────────────────────────
def test_c9_is_established_and_still_does_not_govern_absence(revenue):
    """The substitution this blocks is the withdrawn `empty_fiber -> FILL`, re-made at admission."""
    _family, view, _real = revenue
    c9 = view["exceptional_cases"]

    assert c9.standing == "established"          # the naive check would pass here
    assert set(c9.value) == {"empty_fiber"}      # and it answers a different object entirely

    from columna_platform.admission import _ENTAILED_NOT_ABSENCE
    assert set(c9.value) <= _ENTAILED_NOT_ABSENCE


def test_admission_keys_on_c9_content_not_on_c9_standing():
    from columna_platform import admission
    src = inspect.getsource(admission.admit)
    assert "_ENTAILED_NOT_ABSENCE" in src
    # the naive form must not be what decides absence
    assert "c9.standing != ESTABLISHED" not in src

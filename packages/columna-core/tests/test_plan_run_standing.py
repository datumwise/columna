"""The shared plan/run repair — one standing, settled before the branch.

Ruled Huayin, 2026-09-01:

    A positive preflight disposition must not be returned when the same build already knows that the
    admitted request cannot be realized.

`check_frame_query` is the advertised zero-fetch pre-flight, and it answered `serve` for asks that
`execute_frame_query` then refused. The cause is architectural rather than local: `plan()`
re-implements a SUBSET of `run()`'s checks instead of sharing them, so every capability question the
engine asks on the way to the data was invisible to it.

The repair is to call the SAME data-free predicate from both sides, in `run_statement`'s pre-branch
region — where `_where_reachability` (P1-14's gate) already sat as its only occupant. Nothing is
copied into planning; `face_crossing_standing` and `plan_order_axis` each have exactly one
implementation and two callers.

Stage order is preserved, not flattened. What the pass collects is a MIX of analytical readings (a
face-driver ambiguity is |L| > 1) and realization standing (a crossing this build cannot express),
and each keeps its own jurisdiction. Only the TIMING is shared.
"""
import dataclasses
import os
import sys

import pytest

from columna_core.disclosure import ANALYTICAL, REALIZATION, jurisdiction_for
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement


@pytest.fixture(scope="module")
def srv():
    sys.path.insert(0, os.path.join(os.getcwd(), "docs", "tools"))
    from manual_fixtures import harness
    return harness.servers()["finance_manifold"]


def _d(w):
    nr = next((c.get("no_result") for c in w.get("columns", []) if c.get("no_result")), None)
    return w["outcome"], (nr or {}).get("reason")


def _both(srv, q):
    plan = _d(wire_frame(srv.planner.plan_statement(parse_statement(q)), executed=False))
    run = _d(wire_frame(srv.planner.run_statement(parse_statement(q)), executed=True))
    return plan, run


# ── the invariant, over every case the repair covers ─────────────────────────────────────────────
COVERED = [
    ("P1-21 one face + an ordinary level", "SELECT revenue AT {category.touch*month}"),
    ("P1-24 several lawful orders",        "SELECT cumsum(revenue.sum) AS c AT {month, year}"),
    ("P1-24 no lawful order",              "SELECT cumsum(revenue.sum) AS c AT {customer}"),
    ("P1-24 an invalid named order",       "SELECT cumsum(revenue.sum, by='zzz') AS c AT {customer, day}"),
    ("P1-14 a joined WHERE dimension",     "SELECT revenue AT {customer} WHERE region == 'east'"),
]


@pytest.mark.parametrize("label,q", COVERED, ids=[c[0] for c in COVERED])
def test_plan_and_run_agree(srv, label, q):
    plan, run = _both(srv, q)
    assert plan == run, f"{label}: preflight said {plan}, execution said {run}"


@pytest.mark.parametrize("label,q", COVERED, ids=[c[0] for c in COVERED])
def test_no_positive_preflight_for_something_the_build_will_not_realize(srv, label, q):
    """The invariant as ruled, stated on its own so a future change that keeps the two sides equal by
    making BOTH of them wrong still fails here."""
    plan, _run = _both(srv, q)
    assert plan[0] not in ("serve", "disclose"), f"{label}: preflight promised {plan[0]}"


def test_a_lawful_ask_still_serves_from_both_sides(srv):
    """The half a capability gate breaks if written one notch too wide."""
    plan, run = _both(srv, "SELECT revenue AT {customer} WHERE day == '2024-01-05'")
    assert plan[0] == "serve" and run[0] == "serve"


# ── jurisdictions are NOT flattened by sharing the timing ─────────────────────────────────────────
def test_the_shared_pass_preserves_distinct_jurisdictions(srv):
    _p, run = _both(srv, "SELECT revenue AT {category.touch*month}")
    assert jurisdiction_for(run[1]) == REALIZATION          # a crossing this build cannot express
    _p2, run2 = _both(srv, "SELECT cumsum(revenue.sum) AS c AT {month, year}")
    assert jurisdiction_for(run2[1]) == ANALYTICAL          # several lawful readings


def test_the_face_diagnostic_no_longer_claims_two_faces(srv):
    """P1-21(b). The ask names ONE face; `chained_crossing` told the reader it "would cross two
    declared faces in sequence", which sends them to remove a face they did not write."""
    w = wire_frame(srv.planner.run_statement(
        parse_statement("SELECT revenue AT {category.touch*month}")), executed=True)
    nr = next(c["no_result"] for c in w["columns"] if c.get("no_result"))
    assert nr["reason"] == "mixed_faced_anchor"
    assert "two declared faces" not in nr["detail"]
    assert "single faced coordinate" in nr["detail"]


# ── P1-20: the driver member is decided before realization ───────────────────────────────────────
def test_a_multi_member_face_driver_clarifies_before_realization(srv):
    """v0.2 §12: "A realization layer may not use insertion order, dictionary order, delivery-frame
    availability, or another physical fact to select one silently." The engine chose with
    `next(iter(dmeas.family))`, so the served answer moved when two members were declared in the
    other order.

    NOTE FOR A FUTURE READER: the planner and the engine hold SEPARATE manifold projections
    (`srv.planner.m is not srv.engine.m`), so a fixture edited on one side only is silently ignored
    by the other. That cost a debugging pass; both are patched here deliberately."""
    ranks = srv.planner.m.measures["category_rank"]
    assert len(ranks.family) == 1, "fixture drifted: this test needs a single-member driver to widen"
    originals = {}
    for mm in (srv.planner.m, srv.engine.m):
        originals[id(mm)] = mm.measures["category_rank"]
        mm.measures["category_rank"] = dataclasses.replace(
            mm.measures["category_rank"], family=("min", "max"))
    try:
        plan, run = _both(srv, "SELECT revenue AT {category.assign}")
        assert plan == run == ("clarify", "face_driver_ambiguous")
        assert jurisdiction_for("face_driver_ambiguous") == ANALYTICAL
    finally:
        for mm in (srv.planner.m, srv.engine.m):
            mm.measures["category_rank"] = originals[id(mm)]


def test_a_single_member_driver_is_not_disturbed(srv):
    """The ambiguity is the defect, not the face. One lawful member is not a choice to put to anyone."""
    _plan, run = _both(srv, "SELECT revenue AT {category.assign}")
    assert run[0] in ("serve", "disclose")


# ── what the repair deliberately does NOT cover ──────────────────────────────────────────────────
@pytest.mark.parametrize("row,q", [
    ("P1-28", "SELECT revenue AT {customer} WHERE customer == 'C1'"),
    ("P1-15", "SELECT revenue AT {month, year}"),
])
def test_the_uncovered_divergences_are_recorded_not_hidden(srv, row, q):
    """A shared symptom is not a shared cause (ruled Huayin). These two still diverge, ON PURPOSE:

      * P1-28 is a level-name-to-physical-column MAPPING defect. Teaching the standing model about it
        would ratify a bug as a capability of the build.
      * P1-15 fails in frame assembly, which is not knowable without attempting it.

    Asserted as still-diverging so the exclusion stays a decision rather than an oversight — when
    either row is repaired, this test fails and points at itself."""
    plan, run = _both(srv, q)
    assert plan != run, f"{row} now agrees; fold it into COVERED and delete this case"

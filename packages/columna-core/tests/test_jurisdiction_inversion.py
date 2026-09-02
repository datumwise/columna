"""P1-23 — analytical law that was riding the build-gap reason.

Three refusals were `Refusal("unsupported", ...)` — (ERROR, REALIZATION) — while the string each one
carried cited the LANGUAGE or the measure's DECLARED MEANING, not a build limit:

    map operand ... a map's operands must be co-anchored (§2.4)
    resolution-anchor metric '<m>' is served at a single level — its meaning is a reduction of ...
    crossing a<->b is events-only in v1: universe 'u' is 'spine' basis, where replication corrupts
        completeness — declare an events population or use a functional designation

Ruled Huayin, 2026-09-01: "analytical law failures belong to the analytical jurisdiction even when
the current implementation historically routed them through a realization-capability reason."

This is the MIRROR of P1-21, which reports a realization gap as an analytical Refuse. Both are the
same error — a claim made in the wrong jurisdiction — and both mislead in the same practical way: a
reader told "not supported in this build" waits for a release, and no release will fix a law.

THE DISCRIMINATOR, stated once because it is what makes this reviewable rather than a matter of
taste: **would a maximally capable build refuse this identically?** If yes it is analytical law; if no
it is a build limit. The neighbour of the third site — "ordered/holistic/sketch crossings are
post-launch" — answers no, and deliberately stays `unsupported`.
"""
import os
import sys

import pytest

from columna_core.disclosure import (ANALYTICAL, REALIZATION, REASON_OUTCOME, REFUSE,
                                     jurisdiction_for)
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement


@pytest.fixture(scope="module")
def srv():
    sys.path.insert(0, os.path.join(os.getcwd(), "docs", "tools"))
    from manual_fixtures import harness
    return harness.servers()["finance_manifold"]


def _w(srv, q):
    w = wire_frame(srv.planner.run_statement(parse_statement(q)), executed=True)
    nr = next((c.get("no_result") for c in w.get("columns", []) if c.get("no_result")), None)
    return w["outcome"], (nr or {}).get("reason"), nr


def test_the_co_anchor_law_is_an_analytical_refusal(srv):
    outcome, reason, nr = _w(srv, "SELECT (revenue @ {transaction}) / orders AS r AT {customer}")
    assert (outcome, reason) == (REFUSE, "co_anchor_required")
    assert jurisdiction_for(reason) == ANALYTICAL
    assert "co-anchored" in nr["detail"]


def test_a_crossing_that_would_corrupt_completeness_is_an_analytical_refusal(srv):
    outcome, reason, nr = _w(srv, "SELECT category_weight AT {category.touch}")
    assert (outcome, reason) == (REFUSE, "crossing_basis_not_events")
    assert jurisdiction_for(reason) == ANALYTICAL
    assert "replication corrupts completeness" in nr["detail"]


def test_its_remedy_is_a_declaration_not_a_release(srv):
    """The tell that it is analytical: what the refusal asks for is a change to the DECLARED world,
    which no amount of engine capability supplies."""
    _o, _r, nr = _w(srv, "SELECT category_weight AT {category.touch}")
    assert "declare an events population" in nr["detail"]


@pytest.mark.parametrize("reason", ["co_anchor_required", "resolution_anchor_arity",
                                    "crossing_basis_not_events"])
def test_the_re_reasoned_laws_are_registered_analytical_and_refuse(reason):
    kind, _disc, stage = REASON_OUTCOME[reason]
    assert (kind, stage) == (REFUSE, ANALYTICAL)


def test_a_genuine_build_limit_is_left_alone(srv):
    """The other half of the discriminator, and the reason this commit is narrow: `unsupported` stays
    REALIZATION and keeps every site that really is one. Re-reasoning by sweep instead of by claim
    would have moved these too, and they belong where they are."""
    assert jurisdiction_for("unsupported") == REALIZATION
    assert jurisdiction_for("filter_unsupported") == REALIZATION


def test_no_analytical_reason_hides_in_the_error_umbrella():
    """The seam's own invariant, re-asserted after the re-reasoning: an analytical verdict riding
    `error` is an adjudication the caller cannot see."""
    from columna_core.disclosure import ERROR
    assert not [r for r, (k, _d, stage) in REASON_OUTCOME.items()
                if stage == ANALYTICAL and k == ERROR]

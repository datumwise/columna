"""P1-22 — one WHERE reason was spanning three jurisdictions.

Everything a predicate could fail on arrived as `filter_unreachable`, a CLARIFY:

    WHERE amount >= 100        `amount` is a source column of `txns`, not a declared level
    WHERE zzz_not_a_name >= 1  not a name anywhere; the remedy offered was to "change series
                               'revenue' to an input anchor that reaches 'zzz_not_a_name'"
    WHERE store == 'S1'        a declared level, base of another universe

The first two never became valid Frame-QL filter references. The third is real governed structure
with no lawful reading here. Neither is an under-determined request, and a Clarify asks the reader to
CHOOSE — so the Clarify was a polite failure, offering rewrites of the ask as though they were
readings of it. Of the eight dimensions its menu listed, five answered `filter_unsupported` when
actually named.

Ruled Huayin, 2026-09-01:

    a name/category that does not form a valid filter reference  -> language validity
    a valid governed dimension that cannot participate here      -> analytical Refuse
    Clarify is reserved for genuine multiple lawful readings
    every Clarify alternative must itself be lawful when submitted
    rewrites that change the request are remedies, not alternatives
"""
import os
import sys

import pytest

from columna_core.disclosure import ANALYTICAL, LANGUAGE, REALIZATION, jurisdiction_for
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


# ── the three jurisdictions, on the three asks that used to be one ────────────────────────────────
@pytest.mark.parametrize("name", ["amount", "zzz_not_a_name"])
def test_a_predicate_naming_non_structure_is_a_language_failure(srv, name):
    assert name not in srv.planner.m.levels
    _o, reason, _nr = _w(srv, f"SELECT revenue AT {{customer}} WHERE {name} >= 100")
    assert reason == "unknown" and jurisdiction_for(reason) == LANGUAGE


def test_a_declared_dimension_the_universe_cannot_reach_is_an_analytical_refusal(srv):
    assert "store" in srv.planner.m.levels          # real governed structure ...
    outcome, reason, _nr = _w(srv, "SELECT revenue AT {customer} WHERE store == 'S1'")
    assert (outcome, reason) == ("refuse", "filter_unreachable")   # ... with no lawful reading here
    assert jurisdiction_for(reason) == ANALYTICAL


def test_a_reachable_dimension_the_build_cannot_push_is_a_realization_gap(srv):
    """Unchanged by P1-22, and asserted here so the three sit side by side: this one IS lawful, and
    only this build cannot execute it."""
    _o, reason, _nr = _w(srv, "SELECT revenue AT {customer} WHERE region == 'east'")
    assert reason == "filter_unsupported" and jurisdiction_for(reason) == REALIZATION


def test_the_three_asks_no_longer_share_a_reason(srv):
    """The row in one assertion."""
    reasons = {_w(srv, f"SELECT revenue AT {{customer}} WHERE {p}")[1]
               for p in ["amount >= 100", "store == 'S1'", "region == 'east'"]}
    assert len(reasons) == 3, reasons


# ── no Clarify survives on this path, and no rewrite is offered as a reading ──────────────────────
def test_the_where_path_no_longer_clarifies(srv):
    """Clarify is reserved for genuine multiple lawful readings. Nothing on the WHERE path is one."""
    for p in ["amount >= 100", "zzz_not_a_name >= 1", "store == 'S1'", "region == 'east'"]:
        outcome, _r, _nr = _w(srv, f"SELECT revenue AT {{customer}} WHERE {p}")
        assert outcome != "clarify", p


def test_no_remedy_offers_to_reach_a_name_that_does_not_exist(srv):
    """The old menu's second entry was "change series 'revenue' to an input anchor that reaches
    'zzz_not_a_name'" — an instruction to reach something that is not there."""
    _o, _r, nr = _w(srv, "SELECT revenue AT {customer} WHERE zzz_not_a_name >= 1")
    for a in (nr or {}).get("alternatives", ()):
        assert "zzz_not_a_name" not in a["token"], a


# ── the invariant the ruling asks for, stated over the whole menu ─────────────────────────────────
def test_every_named_remedy_dimension_is_at_least_analytically_lawful(srv):
    """THE INVARIANT, at the strength this seam can actually assert.

    The old menu listed eight dimensions and five answered `filter_unsupported` when named — a remedy
    that trades one refusal for another. Only dimensions the filter can BIND to are named now.

    The assertion is that none of them comes back with an ANALYTICAL or LANGUAGE failure — never that
    they serve, because they may still meet a realization gap, and writing this test the strong way
    is how that was discovered: on this fixture `WHERE customer == 'C1'` answers `unsupported` on a
    BinderException, the logical level not reaching its physical column in the push-down. Asserting
    "serves" here would either be false or would quietly bind this row to a defect that is not its
    own."""
    _o, _r, nr = _w(srv, "SELECT revenue AT {customer} WHERE store == 'S1'")
    offered = nr["alternatives"][0]["token"]
    dims = offered[offered.index("(") + 1:offered.rindex(")")].split(", ")
    assert dims, offered
    for d in dims:
        _outcome, reason, _ = _w(srv, f"SELECT revenue AT {{customer}} WHERE {d} == 'probe'")
        assert reason not in ("filter_unreachable", "unknown"), (d, reason)


def test_the_unexecutable_dimensions_are_described_not_offered(srv):
    """They are lawful, so hiding them would be a lie of omission; they do not work, so offering them
    as a remedy would be a lie of commission. They are named with what is true of them."""
    _o, _r, nr = _w(srv, "SELECT revenue AT {customer} WHERE store == 'S1'")
    described = [a["token"] for a in nr["alternatives"] if "filter_unsupported" in a["token"]]
    assert described, [a["token"] for a in nr["alternatives"]]
    assert "region" in described[0]

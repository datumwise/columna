"""P1-14 — the planner must not promise what the build cannot execute.

THE RULE (ruled Huayin, 2026-08-31):

    A planner must not return a positive Serve/Disclose disposition for a form the current build
    cannot execute.

Two WHERE conditions planned `serve` and then died inside the engine with a bare `unsupported`,
*after* the plan had told the caller the ask was fine. An EXPLAIN that says `serve` about a query
that cannot run is a wrong answer to the one question EXPLAIN exists to answer.

The gate is scoped tight on purpose. A capability gate written one notch too wide classifies a
WORKING capability as unsupported, which is a worse failure than the one it fixes — so the tests
below assert the working forms are untouched as carefully as they assert the broken ones refuse.
"""
import duckdb
import pytest

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.parser import parse_manifold

_CML = """
MANIFOLD w VERSION 1
UNIVERSE sales = customer * day BASIS events
LEVEL customer = customer_id BASE
LEVEL day      = day         BASE
LEVEL region   = region
HIERARCHY geo { customer -> region VIA customers(customer_id, region) }
MEASURE revenue ON sales FROM txns AS sum(amount)
"""


@pytest.fixture(scope="module")
def srv():
    con = duckdb.connect()
    con.execute("CREATE TABLE customers (customer_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO customers VALUES (?, ?)", [("C1", "east"), ("C2", "west")])
    con.execute("CREATE TABLE txns (customer_id VARCHAR, day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO txns VALUES (?, ?, ?)",
                    [("C1", "2024-01-05", 120.0), ("C1", "2024-02-02", 80.0), ("C2", "2024-02-02", 200.0)])
    s = ManifoldServer(parse_manifold(_CML), connector=DuckDBConnector(con))
    s.publish()
    return s


def _plan(srv, q):
    return wire_frame(srv.planner.plan_statement(parse_statement(q)), executed=False)


def _run(srv, q):
    return wire_frame(srv.planner.run_statement(parse_statement(q)))


def _reason(w):
    return next((c["no_result"]["reason"] for c in w["columns"] if c.get("no_result")), None)


# ── the forms that ship must be completely unaffected ───────────────────────────────────────────
def test_a_base_dimension_predicate_still_serves(srv):
    q = "SELECT revenue AT {customer} WHERE day >= '2024-02-01'"
    assert _plan(srv, q)["outcome"] == "serve"
    fr = srv.planner.run_statement(parse_statement(q))
    assert sorted(r["revenue"] for r in fr.data.to_dicts()) == [80.0, 200.0]


def test_an_IN_predicate_on_a_base_dimension_still_serves(srv):
    """The Mission B A5 repair, executing. Guards the gate against swallowing it."""
    q = "SELECT revenue AT {customer} WHERE day IN ('2024-02-02')"
    assert _plan(srv, q)["outcome"] == "serve"
    fr = srv.planner.run_statement(parse_statement(q))
    assert sorted(r["revenue"] for r in fr.data.to_dicts()) == [80.0, 200.0]


def test_an_unreachable_dimension_still_clarifies_not_refuses(srv):
    """`filter_unreachable` is a fact about the MANIFOLD and stays a CLARIFY: the asker can fix it by
    choosing another dimension. The new reason must not have absorbed it."""
    w = _plan(srv, "SELECT revenue AT {customer} WHERE amount >= 100")
    assert w["outcome"] == "clarify" and _reason(w) == "filter_unreachable"


# ── the forms the build cannot execute are now classified BEFORE the engine ─────────────────────
def test_a_double_quoted_literal_is_refused_at_plan_time(srv):
    """Pre-gate: plans `serve`, then dies in the engine. SQL reads `"…"` as an identifier, so the
    backend goes looking for a column by that name. One character from working — and the remedy is
    named in the alternatives rather than left to be guessed."""
    w = _plan(srv, 'SELECT revenue AT {customer} WHERE day >= "2024-02-01"')
    assert w["outcome"] == "error" and _reason(w) == "filter_unsupported"
    assert "single quotes" in str(w["columns"][0]["no_result"]["alternatives"])


def test_a_joined_dimension_is_refused_at_plan_time(srv):
    """`region` IS reachable — it is not `filter_unreachable`. The filter is pushed to the measure's
    own source, which carries the base coordinates and not the joined ones."""
    w = _plan(srv, "SELECT revenue AT {customer} WHERE region == 'east'")
    assert w["outcome"] == "error" and _reason(w) == "filter_unsupported"


def test_plan_and_execution_agree_on_every_where_form(srv):
    """THE POINT OF THE MISSION. Before the gate, three of these planned `serve` and executed to an
    error — the plan was a promise the engine did not keep."""
    for q in ["SELECT revenue AT {customer} WHERE day >= '2024-02-01'",
              'SELECT revenue AT {customer} WHERE day >= "2024-02-01"',
              "SELECT revenue AT {customer} WHERE region == 'east'",
              "SELECT revenue AT {customer} WHERE amount >= 100"]:
        assert _plan(srv, q)["outcome"] == _run(srv, q)["outcome"], q


def test_the_reason_is_specific_and_registered(srv):
    """Not generic `unknown`, and not the engine's bare `unsupported`: a reason a reader can look up
    and a checker can key on. `outcome_for` is closed and fail-closed, so registration is the test."""
    from columna_core.disclosure import outcome_for
    assert outcome_for("filter_unsupported") == ("error", None)

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

P1-14a (repaired 2026-08-31, authorized): one of the two conditions — the DOUBLE-QUOTED string
literal — is no longer gated, because it is fixed. `_to_backend_predicate` normalizes the Frame-QL
literal into the substrate's spelling before the predicate becomes SQL, so the push-down path now
agrees with `_literal`, which accepted either quote all along. The tests that asserted the refusal
are replaced by tests that assert CONVERGENCE (same disposition AND same rows as the single-quoted
spelling) plus a scope guard: the repair grants no dimension that was not already filterable.
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


def test_a_name_that_is_not_a_dimension_is_a_LANGUAGE_failure(srv):
    """WAS `test_an_unreachable_dimension_still_clarifies_not_refuses`, and its example was never an
    unreachable dimension: `amount` is a source column of `txns`, not a declared level at all. It
    reached `filter_unreachable`/CLARIFY because one reason spanned three jurisdictions — which is
    P1-22, found through this very test's example.

    The distinction this test was written to defend — MANIFOLD fact vs BUILD fact — is intact and is
    asserted below; what was wrong was the disposition and the example. A predicate naming something
    that is not governed structure never became a valid Frame-QL filter reference, so no L(Q) is
    formed for it (v0.2 §5). The genuinely-unreachable-DIMENSION case needs a second universe and is
    covered in `test_filter_jurisdiction.py` on the Manual fixture."""
    w = _plan(srv, "SELECT revenue AT {customer} WHERE amount >= 100")
    assert w["outcome"] == "error" and _reason(w) == "unknown"


def test_the_manifold_fact_and_the_build_fact_remain_distinct(srv):
    """The scope guard this file exists for, restated over the reasons rather than the moods:
    `filter_unsupported` (a BUILD limit on a reachable dimension) must not absorb, or be absorbed by,
    the analytical refusal for a dimension the universe cannot reach."""
    from columna_core.disclosure import jurisdiction_for
    assert jurisdiction_for("filter_unsupported") == "realization"
    assert jurisdiction_for("filter_unreachable") == "analytical"
    assert _reason(_plan(srv, "SELECT revenue AT {customer} WHERE region == 'east'")) == "filter_unsupported"


# ── the forms the build cannot execute are now classified BEFORE the engine ─────────────────────
# ── P1-14a: the quote path CONVERGES (repaired 2026-08-31, authorized) ─────────────────────────
@pytest.mark.parametrize("op", [">=", "=="])
def test_the_two_quote_spellings_of_one_literal_are_one_ask(srv, op):
    """THE LAW BEING RESTORED: Frame-QL accepts `'x'` and `"x"` as the SAME language-level kind, and
    `_literal` (the polars/HAVING path) already honoured both. Only the push-down path diverged — it
    handed the predicate to the backend verbatim, where SQL re-read the double-quoted literal as a
    COLUMN NAME. This asserts convergence directly: same disposition, same rows, not merely `serve`.

    Written as one parametrized comparison rather than two hand-copied expectations, because the
    defect WAS the same fact written twice with one copy wrong."""
    sq = f"SELECT revenue AT {{customer}} WHERE day {op} '2024-02-02'"
    dq = f'SELECT revenue AT {{customer}} WHERE day {op} "2024-02-02"'
    assert _plan(srv, dq)["outcome"] == _plan(srv, sq)["outcome"] == "serve"
    rows = lambda q: sorted(r["revenue"] for r in srv.planner.run_statement(parse_statement(q)).data.to_dicts())
    assert rows(dq) == rows(sq) == [80.0, 200.0]


def test_the_IN_repair_converges_on_quotes_too(srv):
    """A5's `IN` list goes through the same normalization — one literal law, not one per operator."""
    dq = 'SELECT revenue AT {customer} WHERE day IN ("2024-02-02")'
    assert _plan(srv, dq)["outcome"] == "serve"
    assert sorted(r["revenue"] for r in srv.planner.run_statement(parse_statement(dq)).data.to_dicts()) == [80.0, 200.0]


def test_normalization_is_a_quote_swap_and_not_a_filtering_feature(srv):
    """SCOPE GUARD. The repair converges two spellings of one literal; it grants no dimension. A
    double-quoted predicate on a JOINED dimension is still `filter_unsupported` and on an UNREACHABLE
    one still `filter_unreachable` — exactly as the single-quoted spelling is."""
    joined = _plan(srv, 'SELECT revenue AT {customer} WHERE region == "east"')
    assert joined["outcome"] == "error" and _reason(joined) == "filter_unsupported"
    # `amount` is not a declared level, so this is a LANGUAGE failure (P1-22); it was
    # `clarify`/`filter_unreachable` when one reason spanned three jurisdictions. The point of the
    # assertion is unchanged and is the point of this test: normalizing the quote admits NO dimension
    # that was not already filterable, whatever the disposition happens to be called.
    unreach = _plan(srv, 'SELECT revenue AT {customer} WHERE amount >= "100"')
    assert unreach["outcome"] == "error" and _reason(unreach) == "unknown"


def test_an_embedded_single_quote_cannot_escape_the_literal(srv):
    """The normalization rewrites into SQL's quoting, so it owes SQL's escape. A literal carrying a
    single quote must come out as one doubled-quote literal, never as a literal that closes early and
    leaves the rest as predicate syntax."""
    from columna_core.planner import Planner
    assert Planner._to_backend_predicate('x == "O\'Brien"') == "x == 'O''Brien'"
    assert Planner._to_backend_predicate("amount >= 100") == "amount >= 100"        # numerics untouched
    assert Planner._to_backend_predicate("day >= '2024-01-01'") == "day >= '2024-01-01'"  # already SQL
    assert Planner._to_backend_predicate(None) is None


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
              'SELECT revenue AT {customer} WHERE region == "east"',
              "SELECT revenue AT {customer} WHERE amount >= 100"]:
        assert _plan(srv, q)["outcome"] == _run(srv, q)["outcome"], q


def test_the_reason_is_specific_and_registered(srv):
    """Not generic `unknown`, and not the engine's bare `unsupported`: a reason a reader can look up
    and a checker can key on. `outcome_for` is closed and fail-closed, so registration is the test."""
    from columna_core.disclosure import outcome_for
    assert outcome_for("filter_unsupported") == ("error", None)

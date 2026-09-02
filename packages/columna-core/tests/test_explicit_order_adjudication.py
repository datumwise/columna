"""P1-24 — explicit `by=` may SELECT governed order standing; it may not CREATE it.

Ruled Huayin, 2026-09-01, after the sweep found that `plan_order_axis` began

    if by is not None:
        return by

so a named order axis was never validated against anything at all.

    by='customer'         a real level, present in the anchor, carrying NO governed order
                          -> SERVED, silently walking an axis the unnamed path refuses to derive
    by='zzz_not_a_level'  -> bare ColumnNotFoundError, reported as a BUILD CAPABILITY GAP

The escape hatch both refusals recommended was unchecked in every direction. `by='customer'` working
today is not authority to preserve it: v0.2 §11 and Ruling 0.1 §7 ("a query cannot manufacture an
undeclared order law merely by naming a physical sort key") both say naming selects, never creates.

WHAT THIS COMMIT DELIBERATELY DOES NOT DECIDE. The governed-order set is `orderable_levels()` —
levels on ADMITTED temporal lineages. The ruling says a temporal level is "one common source of
governed order, not the definition of order", so the set may later widen. Widening it declares a NEW
SOURCE of order standing, which is declaration law, not this repair's to invent. These tests assert
the ADJUDICATION over whatever the set contains, never that the set is temporal-only — so they
survive the set growing.
"""
import duckdb
import pytest

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.disclosure import (ANALYTICAL, CLARIFY, LANGUAGE, REFUSE, jurisdiction_for)
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.parser import parse_manifold

# `calendar` is a TEMPORAL lineage, so day/month/year carry governed order once certified.
# `customer` is a declared level on no temporal lineage — a real name with no order standing, which
# is precisely the shape that used to serve.
_CML = """
MANIFOLD w VERSION 1
UNIVERSE sales = customer * day BASIS events
LEVEL customer = customer_id BASE
LEVEL day      = day         BASE
LEVEL month    = month
LEVEL year     = year
LEVEL region   = region
HIERARCHY calendar {
    day   -> month VIA cal(day, month) ;
    month -> year  VIA cal(month, year)
}
HIERARCHY geography { customer -> region VIA customers(customer_id, region) }
MEASURE revenue ON sales FROM txns AS sum(amount)
"""


@pytest.fixture(scope="module")
def srv():
    con = duckdb.connect()
    con.execute("CREATE TABLE customers (customer_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO customers VALUES (?, ?)", [("C1", "east"), ("C2", "west")])
    con.execute("CREATE TABLE cal (day VARCHAR, month VARCHAR, year VARCHAR)")
    con.executemany("INSERT INTO cal VALUES (?, ?, ?)",
                    [("2024-01-05", "2024-01", "2024"), ("2024-02-02", "2024-02", "2024")])
    con.execute("CREATE TABLE txns (customer_id VARCHAR, day VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO txns VALUES (?, ?, ?)",
                    [("C1", "2024-01-05", 120.0), ("C1", "2024-02-02", 80.0),
                     ("C2", "2024-02-02", 200.0)])
    s = ManifoldServer(parse_manifold(_CML), connector=DuckDBConnector(con))
    s.publish()
    return s


def _wire(srv, q):
    w = wire_frame(srv.planner.run_statement(parse_statement(q)), executed=True)
    nr = next((c.get("no_result") for c in w.get("columns", []) if c.get("no_result")), None)
    return w["outcome"], (nr or {}).get("reason"), nr


def _governed(srv, anchor):
    return srv.planner.m.orderable_levels() & set(anchor)


# ── the withdrawal ────────────────────────────────────────────────────────────────────────────────
def test_by_naming_a_level_with_no_governed_order_is_an_analytical_refusal(srv):
    """THE WITHDRAWN BEHAVIOUR. `customer` is a declared level and a coordinate of the anchor, so the
    engine could and did sort by it — it just carries no order the governed world confers."""
    assert "customer" in srv.planner.m.levels                      # a real level ...
    assert "customer" not in srv.planner.m.orderable_levels()      # ... with no order standing
    outcome, reason, nr = _wire(srv, "SELECT cumsum(revenue.sum, by='customer') AS c AT {customer, day}")
    assert (outcome, reason) == (REFUSE, "order_not_governed")
    assert jurisdiction_for(reason) == ANALYTICAL
    assert "does not create it" in nr["detail"]


def test_the_withdrawn_form_used_to_serve_and_the_replacement_names_the_lawful_axis(srv):
    """A withdrawal must leave the caller somewhere to go, or it is just a wall. The refusal offers
    the axes that DO carry governed order over this anchor."""
    _o, _r, nr = _wire(srv, "SELECT cumsum(revenue.sum, by='customer') AS c AT {customer, day}")
    tokens = [a["token"] for a in nr["alternatives"]]
    assert any("'day'" in t for t in tokens), tokens


# ── the four other §11 cases ──────────────────────────────────────────────────────────────────────
def test_by_naming_something_that_is_not_a_level_is_a_language_failure(srv):
    """Not a realization gap, which is what a bare ColumnNotFoundError from the engine used to make
    it look like. The request never became valid; no L(Q) was formed (v0.2 §5)."""
    outcome, reason, _nr = _wire(srv, "SELECT cumsum(revenue.sum, by='zzz') AS c AT {customer, day}")
    assert reason == "unknown" and jurisdiction_for(reason) == LANGUAGE


def test_by_naming_a_governed_order_outside_the_anchor_has_no_standing_for_this_operation(srv):
    """`month` carries governed order, but this frame has no `month` coordinate, so it confers no
    order HERE. Ruled analytical: a valid request with no lawful reading."""
    assert "month" in srv.planner.m.orderable_levels()
    outcome, reason, nr = _wire(srv, "SELECT cumsum(revenue.sum, by='month') AS c AT {customer}")
    assert (outcome, reason) == (REFUSE, "order_not_governed")
    assert "not a coordinate" in nr["detail"]


def test_several_lawful_governed_orders_and_no_selection_clarifies(srv):
    """|L(Q)| > 1. Was `unknown`/ERROR, which told the caller the request was malformed when it was
    merely under-determined."""
    anchor = ("month", "year")
    assert len(_governed(srv, anchor)) > 1
    outcome, reason, nr = _wire(srv, "SELECT cumsum(revenue.sum) AS c AT {month, year}")
    assert (outcome, reason) == (CLARIFY, "order_axis_ambiguous")
    assert jurisdiction_for(reason) == ANALYTICAL
    assert {a["token"] for a in nr["alternatives"]} == {"by='month'", "by='year'"}


def test_no_lawful_governed_order_refuses(srv):
    """|L(Q)| = 0. Also was `unknown`/ERROR."""
    assert not _governed(srv, ("customer",))
    outcome, reason, _nr = _wire(srv, "SELECT cumsum(revenue.sum) AS c AT {customer}")
    assert (outcome, reason) == (REFUSE, "order_not_governed")


# ── genuinely lawful explicit order STILL WORKS (the half a withdrawal can break) ─────────────────
def test_explicitly_selecting_a_governed_order_in_the_anchor_still_serves(srv):
    assert "day" in _governed(srv, ("customer", "day"))
    outcome, reason, _nr = _wire(srv, "SELECT cumsum(revenue.sum, by='day') AS c AT {customer, day}")
    assert outcome == "serve" and reason is None


def test_a_single_derivable_governed_order_still_serves_without_by(srv):
    outcome, _reason, _nr = _wire(srv, "SELECT cumsum(revenue.sum) AS c AT {month}")
    assert outcome == "serve"


def test_selecting_the_axis_the_unnamed_path_would_have_derived_is_the_same_answer(srv):
    """Selection must be a no-op when it names what the derivation would have chosen — otherwise
    `by=` is not selecting, it is steering."""
    named = srv.planner.run_statement(parse_statement("SELECT cumsum(revenue.sum, by='month') AS c AT {month}"))
    derived = srv.planner.run_statement(parse_statement("SELECT cumsum(revenue.sum) AS c AT {month}"))
    assert named.outcome == derived.outcome == "serve"
    assert named.data.equals(derived.data)


# ── the adjudication follows the set, not the calendar ────────────────────────────────────────────
def test_the_rule_is_stated_over_the_governed_set_not_over_temporality(srv):
    """The ruling says a temporal level is one SOURCE of governed order, not the definition. So the
    property under test is `by=` ∈ governed-orders-of-this-anchor — which stays true if the set
    later grows a non-temporal source. Nothing here asserts the set is temporal-only."""
    anchor = ("customer", "day")
    governed = _governed(srv, anchor)
    for lv in sorted(set(anchor) - governed):
        out, reason, _ = _wire(srv, f"SELECT cumsum(revenue.sum, by='{lv}') AS c AT {{customer, day}}")
        assert (out, reason) == (REFUSE, "order_not_governed"), lv
    for lv in sorted(governed):
        out, _r, _ = _wire(srv, f"SELECT cumsum(revenue.sum, by='{lv}') AS c AT {{customer, day}}")
        assert out == "serve", lv

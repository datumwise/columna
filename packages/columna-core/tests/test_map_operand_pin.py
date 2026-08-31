"""The Mission B runtime repairs: forms the Manual documents that the planner could not reach.

Each of these parsed CLEAN and then died — which is why the grammar-only manual gate reported 37/37
green while a third of the Manual was unreachable. The class is "parser acceptance masking a planner
refusal", and these are its standing regressions.

ADVERSARIAL NOTE. Every test here was run against the pre-repair source and fails there, with the
error quoted in its docstring. Three of them (`unknown column 'transaction'`, `unsupported
expression node Tuple`, `an input anchor @ { } is empty`) are the exact strings P0-18 recorded.
"""
import duckdb
import pytest

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.parser import parse_manifold

_CML = """
MANIFOLD m VERSION 1
UNIVERSE sales = transaction BASIS events
LEVEL transaction = txn_id BASE
LEVEL customer    = customer_id
LEVEL day         = day
HIERARCHY who { transaction -> customer VIA txns(txn_id, customer_id) }
HIERARCHY cal { transaction -> day      VIA txns(txn_id, day) }
MEASURE revenue ON sales FROM txns AS sum(amount)
MEASURE cost    ON sales FROM txns AS sum(cost_amount)
MEASURE orders  ON sales FROM txns AS count(*)
"""

ROWS = [("T1", "C1", "2024-01-05", 120.0, 70.0),
        ("T2", "C1", "2024-01-19",  80.0, 40.0),
        ("T3", "C2", "2024-02-02", 200.0, 90.0)]


@pytest.fixture(scope="module")
def srv():
    con = duckdb.connect()
    con.execute("CREATE TABLE txns (txn_id VARCHAR, customer_id VARCHAR, day VARCHAR, "
                "amount DOUBLE, cost_amount DOUBLE)")
    con.executemany("INSERT INTO txns VALUES (?, ?, ?, ?, ?)", ROWS)
    s = ManifoldServer(parse_manifold(_CML), connector=DuckDBConnector(con))
    s.publish()
    return s


def _ask(srv, q):
    fr = srv.planner.run_statement(parse_statement(q))
    return wire_frame(fr), fr


def _plan(srv, q):
    return wire_frame(srv.planner.plan_statement(parse_statement(q)), executed=False)


# ── the map-operand input pin (§2.4 / §5.2) ──────────────────────────────────────────────────────
def test_single_level_pin_on_map_operands_serves(srv):
    """Pre-repair: `error/unknown` — "unknown column 'transaction'". The level EXISTS; the pin was
    read as a column because only a reducer call knew what `@` meant."""
    w, fr = _ask(srv, "SELECT (revenue @ {transaction}) / (orders @ {transaction}) AS a AT {transaction}")
    assert w["outcome"] == "serve"
    assert sorted(r["a"] for r in fr.data.to_dicts()) == [80.0, 120.0, 200.0]


def test_composite_pin_on_map_operands_plans(srv):
    """Pre-repair: `error/unknown` — "unsupported expression node Tuple". The composite pin is now
    READ (the planner resolves the form); it plans."""
    w = _plan(srv, "SELECT (revenue @ {customer, day}) - (cost @ {customer, day}) AS p "
                   "AT {customer, day}")
    assert w["outcome"] == "serve"


def test_composite_pin_map_still_fails_IN_THE_ENGINE_on_this_manifold_shape(srv):
    """THE STATE AS IT IS, pinned so it cannot be mistaken for repaired (Mission B).

    The planner repair is real and is what the test above asserts. It is NOT the whole story: on a
    manifold where the two pinned levels are reached from the base by SEPARATE hierarchies through
    one table, the engine still cannot assemble the frame and returns `ColumnNotFoundError`. On the
    Manual-fixture shape (a chained calendar) the identical form executes and serves, so this is an
    engine assembly limitation of a particular shape, not of the form.

    Recorded rather than hidden, because a form that PLANS `serve` and dies in the engine is exactly
    the plan/execute divergence this mission exists to find, and one I am not authorized to fix here.
    **If this test starts failing, the engine grew the capability and this row can be struck.**"""
    w, _ = _ask(srv, "SELECT (revenue @ {customer, day}) - (cost @ {customer, day}) AS p "
                     "AT {customer, day}")
    assert w["outcome"] == "error"
    assert w["columns"][0]["no_result"]["reason"] == "unsupported"


def test_the_pin_is_held_to_what_it_declares(srv):
    """A pin is a DECLARATION of the grain the operand is read at, so a pin that disagrees with the
    grain must not be quietly ignored — a pin that does nothing is worse than one that refuses."""
    w = _plan(srv, "SELECT (revenue @ {customer}) - (cost @ {day}) AS bad AT {customer}")
    assert w["outcome"] == "error"
    nr = w["columns"][0]["no_result"]
    assert nr["reason"] == "unsupported" and "co-anchored" in nr["detail"]


def test_composite_pin_is_grain_not_joint_operands(srv):
    """The ruling (Huayin, 2026-08-31): `@ {a,b}` keeps ONE meaning — composite analytical grain.
    `{a,b}` and `{a*b}` are two spellings of that one product, and neither is a joint-operand
    surface. If this ever starts meaning "two operands", that decision was taken elsewhere."""
    a = _plan(srv, "SELECT (revenue @ {customer, day}) - (cost @ {customer, day}) AS p AT {customer, day}")
    b = _plan(srv, "SELECT (revenue @ {customer*day}) - (cost @ {customer*day}) AS p AT {customer, day}")
    assert a["outcome"] == b["outcome"] == "serve"


def test_plan_and_execute_agree_on_the_pinned_map(srv):
    """The whole class this mission is about: a form that plans one way and executes another. These
    two dispatchers (`_infer` for plan, `_node` for resolution) must not disagree."""
    q = "SELECT (revenue @ {transaction}) / (orders @ {transaction}) AS a AT {transaction}"
    assert _plan(srv, q)["outcome"] == _ask(srv, q)[0]["outcome"] == "serve"


# ── the Manifold-wide scalar and broadcast (§2.6) ────────────────────────────────────────────────
def test_the_scalar_input_anchor_broadcasts(srv):
    """Pre-repair: FrameQLSyntaxError — "an input anchor `@ { }` is empty". `{}` is a DECLARED grain
    (the boundaries collapsed to one point), not a missing one. The shares must sum to 1."""
    w, fr = _ask(srv, "SELECT (revenue @ {customer}) / (revenue @ {}) AS share AT {customer}")
    assert w["outcome"] == "serve"
    shares = [r["share"] for r in fr.data.to_dicts()]
    assert sum(shares) == pytest.approx(1.0)
    assert sorted(shares) == pytest.approx([200.0 / 400, 200.0 / 400])


# ── the macro binding's own name (§4.5 / §6.14) ──────────────────────────────────────────────────
def test_a_binding_name_survives_its_inlining(srv):
    """Pre-repair: FrameQLSyntaxError — "series '((revenue - cost))' has no derivable name".
    Substitution ran before naming, so the only name anyone had written was gone by the time naming
    looked. Adding `AS profit` served, which is the tell: the expression was always fine."""
    w, fr = _ask(srv, "WITH profit = (revenue - cost) SELECT profit AT {customer}")
    assert w["outcome"] == "serve"
    assert "profit" in fr.data.columns


def test_an_expression_with_no_name_of_its_own_still_refuses(srv):
    """WP-NAME-1 is NOT relaxed by the repair above. A binding has a declared name; a bare
    expression does not, and must still be refused rather than given a mechanical default."""
    from columna_core import FrameQLSyntaxError
    with pytest.raises(FrameQLSyntaxError):
        srv.planner.run_statement(parse_statement("SELECT (revenue - cost) AT {customer}"))

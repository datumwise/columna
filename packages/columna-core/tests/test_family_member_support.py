"""P1-10 — every member of a family over one declared VALUE shares one support.

WHAT WAS WRONG. `count` was registered `deliver_sql=lambda p: "count(*)"`, which DISCARDS its
operand. So as a family member over a declared VALUE it counted ROWS while its siblings — `sum`,
`min`, `max`, and SQL generally — counted OBSERVATIONS. Two members of one declared family therefore
carried different supports, and `revenue.sum / revenue.count` served a mean over mismatched
denominators, silently: 20.0 where the mean per revenue observation was 25.0.

Neither figure was wrong on its face. Which one it WAS depended on a law nobody declared, and the
wire said nothing either way. That is the defect.

THE DISTINCTION WAS ALREADY DECLARED; only the delivery threw it away. The parser normalizes the
AS-form `count(...)` to `pre_expr = "1"` (`parser.py:453`) — in that form `count` MEANS rows — while
the VALUE+FAMILY form carries the declared value expression. Passing the operand through honours both
readings with one lambda: `count(1)` is exactly `count(*)` (a literal is never null), and
`count(<value>)` is the observation count the siblings already use.

WHY THIS IS A REPAIR AND NOT A DISCLOSURE. The invariant is that a shared output coordinate does not
establish shared analytical support. It can be satisfied two ways: retain the divergence and disclose
it, or remove the divergence at its source. Here the divergence had no reason to exist — a family
member over a value is a reducer OVER THAT VALUE — so removing it is both smaller and stronger than
disclosing it. Nothing is hidden: row-counting stays fully available and separately addressable as
`AS count(*)`, and the two readings can be asked side by side.

NOT ADDRESSED, deliberately — see `test_the_residual_is_not_representable` at the bottom.
"""
import duckdb

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.parser import parse_manifold

CML = """
MANIFOLD p VERSION 1
UNIVERSE ops = store BASIS spine
LEVEL store = store_id BASE
MEASURE revenue ON ops FROM t TYPE Float64 VALUE v
    FAMILY {
        sum
        count
        min
        max
    }
MEASURE lines ON ops FROM t AS count(*)
DERIVED avg_obs  = revenue.sum / revenue.count
DERIVED avg_line = revenue.sum / lines
"""


def _server(values):
    con = duckdb.connect()
    con.execute("CREATE TABLE t AS SELECT * FROM (VALUES "
                + ",".join(f"('s1',{'NULL' if v is None else repr(v)})" for v in values)
                + ") AS x(store_id,v)")
    srv = ManifoldServer(parse_manifold(CML), DuckDBConnector(con))
    srv.publish()
    return srv


def _one(srv, expr):
    w = wire_frame(srv.planner.run_statement(parse_statement(f"SELECT {expr} AS x AT {{store}}")))
    col = w["columns"][0]
    val = (col.get("values") or [{}])[0].get("value") if col.get("values") else None
    codes = {(d.get("code"), d.get("materiality")) for d in (col.get("disclosures") or [])}
    return w["outcome"], val, codes


FULL = [10.0, 20.0, 30.0, 40.0]              # 4 rows, 4 observations
GAP = [10.0, 20.0, None, 30.0, 40.0]         # 5 rows, 4 observations


def test_equal_underlying_support_is_unchanged():
    """No nulls: rows == observations, so nothing about this case may move."""
    srv = _server(FULL)
    assert _one(srv, "revenue.sum")[1] == 100.0
    assert _one(srv, "revenue.count")[1] == 4
    assert _one(srv, "lines")[1] == 4
    assert float(_one(srv, "avg_obs")[1]) == 25.0
    assert float(_one(srv, "avg_line")[1]) == 25.0


def test_divergent_support_at_an_identical_coordinate():
    """THE DEFECT. One coordinate, both members present, different underlying support. The family
    members must now agree on which observations they are about."""
    srv = _server(GAP)
    assert _one(srv, "revenue.sum")[1] == 100.0
    assert _one(srv, "revenue.count")[1] == 4, "a family member over VALUE counts OBSERVATIONS"
    assert float(_one(srv, "avg_obs")[1]) == 25.0, "was 20.0 — a mean over mismatched denominators"


def test_null_skipping_and_row_counting_are_both_available():
    """The repair removes an ambiguity, it does not remove a capability. Row-counting stays
    addressable and unchanged; the two readings can be asked side by side and differ visibly."""
    srv = _server(GAP)
    assert _one(srv, "revenue.count")[1] == 4      # observations of the declared value
    assert _one(srv, "lines")[1] == 5              # rows, via AS count(*)
    assert float(_one(srv, "avg_line")[1]) == 20.0  # a different, legitimate question


def test_as_count_star_is_byte_for_byte_unchanged():
    """`count(1)` is `count(*)`: a literal is never null. The AS-form must not move at all."""
    for values in (FULL, GAP):
        srv = _server(values)
        assert _one(srv, "lines")[1] == len(values)


def test_all_value_family_members_share_one_support():
    """sum/count/min/max over one declared VALUE are about the same observations."""
    srv = _server(GAP)
    assert _one(srv, "revenue.sum")[1] == 100.0
    assert _one(srv, "revenue.min")[1] == 10.0
    assert _one(srv, "revenue.max")[1] == 40.0
    assert _one(srv, "revenue.count")[1] == 4


def test_ineligible_observations_never_enter_the_count():
    """A universe carve removes observations from the population BEFORE aggregation, so an ineligible
    row is not merely unsupported — it is not part of the question. Both members must honour the
    carve identically, or the ratio is again a mean over two populations."""
    cml = """
MANIFOLD p VERSION 1
UNIVERSE sales = store * day WHERE day >= store.opened BASIS spine
LEVEL store = store_id BASE ATTR opened = stores.opened_date
LEVEL day = day BASE
LEVEL region = region
HIERARCHY geo { store -> region VIA stores(store_id, region) }
MEASURE revenue ON sales FROM t TYPE Float64 VALUE v
    FAMILY {
        sum
        count
    }
DERIVED avg_obs = revenue.sum / revenue.count
"""
    con = duckdb.connect()
    con.execute("CREATE TABLE stores AS SELECT * FROM (VALUES "
                "('s1', DATE '2024-01-02','r1')) AS x(store_id, opened_date, region)")
    # four in-carve rows, one of them with no observation; one PRE-OPENING row = ineligible
    con.execute("""CREATE TABLE t AS SELECT * FROM (VALUES
        ('s1', DATE '2024-01-02', 10.0),
        ('s1', DATE '2024-01-03', 20.0),
        ('s1', DATE '2024-01-04', NULL),
        ('s1', DATE '2024-01-05', 30.0),
        ('s1', DATE '2024-01-01', 999.0)) AS x(store_id, day, v)""")
    srv = ManifoldServer(parse_manifold(cml), DuckDBConnector(con))
    srv.publish()
    assert _one(srv, "revenue.sum")[1] == 60.0, "the pre-opening 999.0 is outside the carve"
    assert _one(srv, "revenue.count")[1] == 3, "ineligible AND unsupported rows are both excluded"
    assert float(_one(srv, "avg_obs")[1]) == 20.0


def test_warm_and_cold_agree():
    srv = _server(GAP)
    cold, warm = _one(srv, "avg_obs"), _one(srv, "avg_obs")
    assert cold == warm


def test_semantic_disclosure_parity_between_members():
    """Equal supports means nothing to disclose — the repair must not leave a residual caveat."""
    srv = _server(GAP)
    w = wire_frame(srv.planner.run_statement(
        parse_statement("SELECT revenue.sum AS a, revenue.count AS b AT {store}")))
    for col in w["columns"]:
        assert not (col.get("disclosures") or []), f"{col['name']} should have nothing to disclose"
    assert w["outcome"] == "serve"


def test_the_residual_is_not_representable():
    """THE ARCHITECTURAL BLOCKER, pinned as a fact rather than a wish.

    `revenue.sum / lines` combines two DIFFERENT measures that both have a row at the coordinate but
    rest on different underlying support (4 observations vs 5 rows). P1-11's alignment domain cannot
    see it — the coordinate exists for both. P1-10's repair cannot see it either — they are not
    members of one family.

    Here it is a *declared* question and 20.0 is the right answer. But the runtime cannot distinguish
    a declared divergence from an accidental one, because the engine delivers ONE aggregate per
    measure per coordinate and the observation count is consumed inside the SQL aggregate and never
    returned. Detecting it would need a companion support carrier on every delivery — new machinery,
    not a small change, and not supported by current doctrine.

    This test asserts the CURRENT state so the gap stays visible and dated. If it ever starts
    failing, the runtime grew a support representation and this blocker can be struck."""
    srv = _server(GAP)
    outcome, val, codes = _one(srv, "avg_line")
    assert outcome == "serve"
    assert float(val) == 20.0
    assert not codes, "no support divergence is detectable across measures at a shared coordinate"

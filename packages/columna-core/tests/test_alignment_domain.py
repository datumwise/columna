"""P1-11 — the alignment domain of a binary map is declared, and support divergence is disclosed.

WHAT WAS WRONG. `Planner._apply` joined its two operands `how="inner"`. That one word was an
undeclared complete-case participation policy chosen by the substrate: it discarded every coordinate
the operands did not share, BEFORE Φ could see it. The absence had therefore ceased to exist by the
time the absence pass ran, so nothing was disclosed — and the column went on asserting
`population: <universe>` while serving the intersection. Two measures served side by side returned
three rows and a MATERIAL caveat; the same two combined by `/` returned two rows and silence.

The law was already written, 1,280 lines earlier, for juxtaposition: *"Absence is only definable
relative to a DOMAIN; the full-outer align supplies one LOCALLY."* An expression needs a domain for
the same reason a frame does. The repair is that same law one level down — one alignment law, not
two.

WHAT THESE TESTS PIN, and why each one exists:
  · equal supports invent nothing (the repair must not manufacture gaps);
  · a divergence keeps the coordinate AND discloses it MATERIAL, from either side;
  · the one distinction current law CAN make survives — Φ `undefined` on the absent operand means the
    point is INELIGIBLE (immaterial, still `serve`), while `unknown` means eligible-but-unsupported
    (material, `disclose`). Collapsing those two would be a new defect, not a fix;
  · a `zero` rule NEVER fills a divergence gap. `zero` declares what an absence of THAT MEASURE
    denotes; it says nothing about a coordinate where one operand was present and the other absent.
    Filling there would assert the expression was nil when what is true is that it is undefined;
  · provenance caveats still ride alongside (the bug was specific to support, never to disclosure);
  · warm and cold agree — Unit B's rule that the semantic channel is call-invariant.

NOT FIXED BY THIS, deliberately: P1-10. There the two operands are members of one family and both
produce a row at the anchor; the divergence is in the underlying observation counts, not in the
anchor coordinates, so there was no coordinate for an alignment domain to preserve. It took its own
repair — `count`'s delivery, see `test_family_member_support.py`. Pinned below so the two cannot be
confused for one.
"""
import duckdb
import pytest

from columna_core import ManifoldServer
from columna_core.connector import DuckDBConnector
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.parser import parse_manifold


def _server(lphi="unknown", rphi="unknown", left=(1, 2, 3), right=(1, 2, 3), rhs="headcount"):
    if rhs == "buyers":
        rmeas, formula = f"MEASURE buyers ON ops FROM staffing AS distinct(who) FILL {rphi}", "revenue / buyers"
    else:
        rmeas, formula = f"MEASURE headcount ON ops FROM staffing AS sum(heads) FILL {rphi}", "revenue / headcount"
    cml = f"""
MANIFOLD p VERSION 1
UNIVERSE ops = store BASIS spine
LEVEL store = store_id BASE
MEASURE revenue ON ops FROM sales AS sum(amount) FILL {lphi}
{rmeas}
DERIVED d = {formula}
"""
    con = duckdb.connect()
    con.execute("CREATE TABLE sales AS SELECT * FROM (VALUES "
                + ",".join(f"('s{i}',{i * 100}.0)" for i in left) + ") AS t(store_id,amount)")
    con.execute("CREATE TABLE staffing AS SELECT * FROM (VALUES "
                + ",".join(f"('s{i}',{i * 10}.0,'w{i}')" for i in right) + ") AS t(store_id,heads,who)")
    srv = ManifoldServer(parse_manifold(cml), DuckDBConnector(con))
    srv.publish()
    return srv


def _ask(srv, q="SELECT d AS d AT {store}"):
    return wire_frame(srv.planner.run_statement(parse_statement(q)))


def _codes(wire):
    col = wire["columns"][0]
    return {(d.get("code"), d.get("materiality")) for d in (col.get("disclosures") or [])}


def _rows(wire):
    return wire["columns"][0].get("values") or []


# ── the alignment domain ─────────────────────────────────────────────────────────────────────────

def test_equal_supports_invent_no_gap():
    """The repair must not manufacture a disclosure where nothing diverged."""
    w = _ask(_server(left=(1, 2, 3), right=(1, 2, 3)))
    assert w["outcome"] == "serve"
    assert len(_rows(w)) == 3
    assert not any(code == "incomplete_data" for code, _ in _codes(w))


@pytest.mark.parametrize("left,right", [((1, 2, 3), (1, 2)), ((1, 2), (1, 2, 3))])
def test_divergence_keeps_the_coordinate_and_discloses_it(left, right):
    """Either side may be the short one. The union is the domain; the shortfall is MATERIAL."""
    w = _ask(_server(left=left, right=right))
    assert len(_rows(w)) == 3, "the coordinate must survive into the frame, not be joined away"
    assert ("incomplete_data", "material") in _codes(w)
    assert w["outcome"] == "disclose", "a material condition must move the mood off `serve`"


def test_the_column_no_longer_asserts_a_population_it_did_not_serve():
    """THE ORIGINAL DEFECT, stated as the thing that must stay true: the population claim and the
    coordinates delivered agree. Before the repair this served 2 of 3 while claiming `ops`."""
    w = _ask(_server(left=(1, 2, 3), right=(1, 2)))
    col = w["columns"][0]
    assert col.get("population") == "ops"
    assert {r["store"] for r in _rows(w)} == {"s1", "s2", "s3"}


# ── the distinction current law can make ─────────────────────────────────────────────────────────

def test_ineligible_is_not_reported_as_a_support_gap():
    """Φ `undefined` on the absent operand means the point is OUTSIDE that operand's population.
    That is a population boundary, not a shortfall, so it is immaterial and the frame still serves."""
    w = _ask(_server("undefined", "undefined", (1, 2, 3), (1, 2)))
    assert ("out_of_population", "immaterial") in _codes(w)
    assert not any(code == "incomplete_data" for code, _ in _codes(w))
    assert w["outcome"] == "serve"


def test_eligible_but_unsupported_is_material():
    """Φ `unknown` means a value existed and was not recorded — a real shortfall."""
    w = _ask(_server("unknown", "unknown", (1, 2, 3), (1, 2)))
    assert ("incomplete_data", "material") in _codes(w)
    assert w["outcome"] == "disclose"


def test_zero_never_fills_a_divergence_gap():
    """`zero` declares what an absence of THAT MEASURE denotes. It does not declare what an absence
    of the EXPRESSION denotes, and filling would assert the ratio was nil when it is undefined."""
    w = _ask(_server("zero", "zero", (1, 2, 3), (1, 2)))
    gap = [r for r in _rows(w) if r["store"] == "s3"]
    assert gap and gap[0]["value"] is None, "a divergence gap must never be filled with 0"
    assert ("incomplete_data", "material") in _codes(w)


# ── the repair is specific to support ────────────────────────────────────────────────────────────

def test_provenance_caveats_still_ride_alongside_a_support_gap():
    """The original bug was never a disclosure-plumbing bug: an HLL approximation always propagated
    through a map. It must keep propagating, now beside the support gap."""
    w = _ask(_server(left=(1, 2, 3), right=(1, 2), rhs="buyers"))
    codes = {code for code, _ in _codes(w)}
    assert "approximation" in codes
    assert "incomplete_data" in codes


def test_warm_and_cold_agree():
    """Unit B's rule: the semantic channel is call-invariant. Asserted as equality in both
    directions, so a change that ADDS a caveat only on the warm path fails too."""
    srv = _server(left=(1, 2, 3), right=(1, 2))
    cold, warm = _ask(srv), _ask(srv)
    assert _codes(cold) == _codes(warm)
    assert cold["outcome"] == warm["outcome"]
    assert _rows(cold) == _rows(warm)


# ── the scope boundary, pinned ───────────────────────────────────────────────────────────────────

def test_p1_10_is_a_separate_repair_not_this_one():
    """SCOPE PIN. P1-10 divides two members of ONE family; both produce a row at the anchor, so the
    alignment domain is identical and there was no coordinate for it to preserve. Repairing the join
    did NOT repair P1-10 — that took a separate change to `count`'s delivery (see
    `test_family_member_support.py`), because its divergence lives in the underlying OBSERVATION
    counts rather than in the anchor coordinates.

    This test exists so the two repairs cannot be confused for one. It asserts the post-P1-10 value;
    if it ever reads 20.0 again, the count delivery regressed, not the alignment domain."""
    cml = """
MANIFOLD p2 VERSION 1
UNIVERSE ops = store BASIS spine
LEVEL store = store_id BASE
MEASURE revenue ON ops FROM t TYPE Float64 VALUE v
    FAMILY {
        sum
        count
    }
DERIVED avg_line = revenue.sum / revenue.count
"""
    con = duckdb.connect()
    con.execute("CREATE TABLE t AS SELECT * FROM (VALUES "
                "('s1',10.0),('s1',20.0),('s1',NULL),('s1',30.0),('s1',40.0)) AS x(store_id,v)")
    srv = ManifoldServer(parse_manifold(cml), DuckDBConnector(con))
    srv.publish()
    w = _ask(srv, "SELECT avg_line AS d AT {store}")
    assert w["outcome"] == "serve"
    assert not _codes(w), "supports are equal by construction now — nothing to disclose"
    assert float(_rows(w)[0]["value"]) == 25.0, "mean per OBSERVATION; 20.0 would mean count regressed to rows"

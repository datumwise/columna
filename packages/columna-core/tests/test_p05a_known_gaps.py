"""
test_p05a_known_gaps.py — the THREE holes P0.5a does not yet close, encoded as strict xfails.

Provenance: an explicit adversarial audit of the P0.5a change asked the question the design review
demanded — *is positive admission STRUCTURAL, or is there still a path where absence of a verdict is
read as permission?* The answer was no, not yet: three paths survive. Each is pinned here as
`xfail(strict=True)`, so the branch carries the defect as a RED test rather than as prose, and each
pin flips to a passing test the moment the hole is closed (strict = it fails loudly if it starts
passing silently).

The common root: **the gate and the executor traverse different graphs.**
`PlannerView.find_path` (the gate) walks the CERTIFIED shape DAG; `Manifold.find_path` (what
`engine.py` re-derives for itself at ~8 call sites) walks the FULL DECLARED graph and has no notion
of certification. Where those two graphs disagree, the planner admits one route and the engine
executes another.

  GAP 1  the AT-metric path never calls `_check_addressable` at the anchor the user ASKED at.
  GAP 2  REGRESSION: with two routes to a target, the gate certifies route A while the engine
         executes the BLOCKED route B — serving a wrong number across a CONTRADICTED edge.
  GAP 3  the admission key is `(frm, to)` but the verdict is per-LINEAGE, so one lineage's
         CORROBORATED certifies another lineage's uncertified edge over the same level pair.
"""
import duckdb
import os
import pytest

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.parser import parse_manifold

_CML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "benchmark.cml")
_AT_DEFS = ("DERIVED aov = revenue / orders\n"
            "DERIVED daily_aov = revenue / orders AT day\n"
            "    FAMILY {\n        mean FERTILE { }\n    }\n")


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


def _server_con(text, tables):
    con = duckdb.connect()
    for name, (cols, rows) in tables.items():
        values = ", ".join("(" + ", ".join(_lit(v) for v in row) + ")" for row in rows)
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM (VALUES {values}) AS t({', '.join(cols)})")
    return ManifoldServer(parse_manifold(text), DuckDBConnector(con)), con


# ── GAP 1 ─────────────────────────────────────────────────────────────────────────────────────────
@pytest.mark.xfail(strict=True, reason="P0.5a GAP 1: the AT-metric path bypasses _check_addressable "
                                       "at the asked anchor; engine.reduce_series re-BFSes the "
                                       "UNCERTIFIED Manifold graph and transports anyway.")
def test_at_metric_must_not_bypass_the_certification_gate(fixture_connector):
    """Same manifold, same anchor, same `day -> cal.month` edge, same (absent) certification: the
    PLAIN derived ratio correctly refuses `uncertified_edge` while the AT-anchored one SERVES. The
    law cannot depend on which spelling of the same transport the author chose."""
    srv = ManifoldServer(parse_manifold(open(_CML).read() + "\n" + _AT_DEFS), fixture_connector)
    plain = srv.frame("cal.month").column("aov").run()
    assert plain.data is None                                  # the gate works on this path
    at = srv.frame("cal.month").column("daily_aov").run()
    assert at.data is None, ("the AT-metric transported day -> cal.month without a certified edge "
                             f"(served {at.outcome})")


# ── GAP 2 — the regression ────────────────────────────────────────────────────────────────────────
_TWO_ROUTE = """
MANIFOLD h2 VERSION 1
UNIVERSE sales = day
LEVEL day = day BASE
LEVEL month = month
LEVEL quarter = quarter
HIERARCHY good { day -> month VIA cal(day, month) -> quarter VIA cal2(month, quarter) }
HIERARCHY direct { day -> quarter VIA calq(day, quarter) }
MEASURE revenue ON sales FROM tx AS sum(amount)
"""


@pytest.mark.xfail(strict=True, reason="P0.5a GAP 2 (REGRESSION vs e3460e8): the certified-graph "
                                       "find_path routes AROUND the blocked edge, so "
                                       "_blocked_transport never fires, while the engine's own BFS "
                                       "over the declared graph takes the BLOCKED one-hop route.")
def test_transport_must_refuse_when_the_engine_route_crosses_a_contradicted_edge():
    """The sharpest of the three. Two routes day->quarter: `good` (2 hops, CORROBORATED) and `direct`
    (1 hop, CONTRADICTED on re-attestation). The planner checks `good` and admits; the engine BFSes
    the full declared graph, picks the shorter `direct`, and serves — a wrong total (40 vs 30) plus a
    phantom bucket 'q9', with outcome=serve and no refusal and no disclosure.

    At the base commit this query REFUSED `contradicted_edge`. Closing the gate on a graph the
    executor does not use turned a correct refusal into a wrong number."""
    srv, con = _server_con(_TWO_ROUTE, {
        "cal":  (["day", "month"], [("d1", "m1"), ("d2", "m1")]),
        "cal2": (["month", "quarter"], [("m1", "q1")]),
        "calq": (["day", "quarter"], [("d1", "q1"), ("d2", "q1")]),
        "tx":   (["day", "amount"], [("d1", 10.0), ("d2", 20.0)])})
    srv.publish()
    con.execute("INSERT INTO calq VALUES ('d1', 'q9')")        # refute ONLY the `direct` lineage
    diff = srv.reattest()
    assert ("day", "quarter") in diff["blocked_edges"]         # the adjudicator DID refute it

    fr = srv.frame("quarter").column("revenue", "revenue").run()
    assert fr.outcome == "refuse", (
        f"served across a CONTRADICTED edge: {None if fr.data is None else fr.data.to_dicts()}")
    assert fr.columns[0].refusal.classified().reason == "contradicted_edge"


# ── GAP 3 ─────────────────────────────────────────────────────────────────────────────────────────
_SHARED_HOP = """
MANIFOLD h3 VERSION 1
UNIVERSE sales = day
LEVEL day = day BASE
LEVEL month = month
HIERARCHY good { day -> month VIA cal(day, month) }
HIERARCHY shadow { day -> month VIA missing_tbl(day, month) }
MEASURE revenue ON sales FROM tx AS sum(amount)
"""


@pytest.mark.xfail(strict=True, reason="P0.5a GAP 3: certified_edges/_gated_edges are keyed on "
                                       "(frm, to) but a verdict is per-LINEAGE, so a CORROBORATED "
                                       "lineage certifies a co-located UNTESTABLE one.")
def test_admission_must_be_keyed_on_the_lineage_not_just_the_level_pair():
    """`good` corroborates day->month; `shadow` declares the same hop VIA a table that does not
    exist, so it is UNTESTABLE — never positively admitted. Because both collapse to the key
    ('day','month'), `_admitted` returns True for the shadow edge: one lineage's evidence silently
    licenses another's claim."""
    from columna_core.model import UNTESTABLE
    srv, _con = _server_con(_SHARED_HOP, {
        "cal": (["day", "month"], [("d1", "m1"), ("d2", "m1")]),
        "tx":  (["day", "amount"], [("d1", 10.0), ("d2", 20.0)])})
    srv.publish()
    verdicts = {h.lineage: h.license.verdict for h in srv.m.hierarchies}
    assert verdicts["shadow"] == UNTESTABLE                    # never earned admission

    shadow_edge = next(e for e in srv.m.edges if e.lineage == "shadow")
    assert not srv.planner.m._admitted(shadow_edge), (
        "an UNTESTABLE lineage's edge was admitted on a DIFFERENT lineage's verdict")

"""
test_p05a_execution_contract.py — the planner→engine execution contract (P0.5a, ruling 2026-08-11).

Provenance: an adversarial audit of the first P0.5a implementation asked whether positive admission was
STRUCTURAL, or whether absence of a verdict was still read as permission. It was not structural: the
gate walked the CERTIFIED graph while `engine.py` re-derived transport over the FULL DECLARED graph, so
where the two disagreed the planner admitted one route and the engine executed another. Three holes
followed, and were pinned here as strict xfails. The ruling rejected keeping two routing authorities in
sync and required ONE:

    declared graph + PublishedScope positive admissions
            -> PlannerView
            -> one concrete admitted transport path
            -> engine executes THAT path

These are the same three scenarios, now as ordinary passing regressions.

    GAP 1  an AT-metric may not serve where the equivalent ordinary metric refuses.
    GAP 2  the engine executes the planner's certified route and never a contradicted shortcut.
    GAP 3  certification identity is per-LINEAGE and cannot bleed between co-located edges.

The invariant is NOT "refuse if any contradicted edge exists". It is: **never execute an edge that is
not positively admitted.** A certified alternate route therefore serves a correct answer rather than
reproducing the base branch's refusal.
"""
import duckdb
import os
import pytest

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.model import EdgeKey
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


# ══ GAP 2 — the engine executes the planner's route ═══════════════════════════════════════════════
# Two routes day->quarter: `good` (2 hops, stays CORROBORATED) and `direct` (1 hop, CONTRADICTED on
# re-attestation). The engine used to BFS the declared graph, prefer the shorter `direct`, and serve a
# wrong total (40) plus a phantom bucket 'q9'.
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
_TWO_ROUTE_TABLES = {
    "cal":  (["day", "month"], [("d1", "m1"), ("d2", "m1")]),
    "cal2": (["month", "quarter"], [("m1", "q1")]),
    "calq": (["day", "quarter"], [("d1", "q1"), ("d2", "q1")]),
    "tx":   (["day", "amount"], [("d1", 10.0), ("d2", 20.0)]),
}
_ONE_ROUTE = _TWO_ROUTE.replace(
    "HIERARCHY good { day -> month VIA cal(day, month) -> quarter VIA cal2(month, quarter) }\n", "")


def _two_route_server_with_direct_refuted():
    srv, con = _server_con(_TWO_ROUTE, _TWO_ROUTE_TABLES)
    srv.publish()
    con.execute("INSERT INTO calq VALUES ('d1', 'q9')")        # refute ONLY the `direct` lineage
    diff = srv.reattest()
    assert EdgeKey("direct", "day", "quarter") in diff["blocked_edges"]
    assert EdgeKey("good", "day", "month") in srv.published_scope.certified_edges
    return srv, con


def test_engine_executes_the_certified_route_never_the_contradicted_shortcut():
    """The GAP-2 repro, now the law. A certified alternate route exists, so the query SERVES — and
    serves the CORRECT number, because the route that executes is the route that was certified.

    Before the fix this served total 40 (30 + a phantom 'q9' bucket of 10) across the refuted `direct`
    edge, with outcome=serve and no refusal and no disclosure."""
    srv, _con = _two_route_server_with_direct_refuted()
    fr = srv.frame("quarter").column("revenue", "revenue").run()
    assert fr.outcome in ("serve", "disclose"), "a certified route exists — it must answer"
    rows = {r["quarter"]: float(r["revenue"]) for r in fr.data.iter_rows(named=True)}
    assert rows == {"q1": 30.0}, f"executed the refuted shortcut: {rows}"
    assert "q9" not in rows, "the phantom bucket only exists on the CONTRADICTED edge"


def test_the_executed_transport_is_the_planned_transport():
    """Observability alignment: the route EXPLAIN advertises is the route that runs.

    The engine's trace names each hop it actually transports along, with its lineage. On the GAP-2
    topology that must be the two `good` hops and never the one `direct` hop — and it must agree with
    the dependency cone EXPLAIN publishes for the same query."""
    srv, _con = _two_route_server_with_direct_refuted()
    trace = srv.frame("quarter").column("revenue", "revenue").explain().splitlines()
    hops = [ln for ln in trace if "transport" in ln]
    executed = " ".join(hops)
    assert "along good" in executed, f"expected the certified lineage in {hops}"
    assert "along direct" not in executed, f"executed the refuted lineage: {hops}"
    assert len(hops) == 2, f"expected the 2-hop certified route, got {hops}"

    # ...and the dependency cone EXPLAIN publishes describes that same route, not a third one.
    _atoms, _derived, cone_edges = srv.planner.cone_atoms_and_edges("revenue", ("quarter",))
    lineages = {e["lineage"] for e in cone_edges}
    assert lineages == {"good"}, f"explain advertises a route the engine does not run: {cone_edges}"
    assert not any(e["blocked"] for e in cone_edges)


def test_no_certified_route_but_a_contradicted_declared_one_refuses_contradicted_edge():
    """The ladder's middle rung. Remove the alternate route entirely: with `direct` refuted and nothing
    else reaching quarter, the refusal names the REFUTATION — the stronger factual claim."""
    srv, con = _server_con(_ONE_ROUTE, _TWO_ROUTE_TABLES)
    srv.publish()
    con.execute("INSERT INTO calq VALUES ('d1', 'q9')")
    srv.reattest()
    fr = srv.frame("quarter").column("revenue", "revenue").run()
    assert fr.outcome == "refuse"
    assert fr.columns[0].refusal.classified().reason == "contradicted_edge"


def test_no_certified_route_and_merely_uncertified_refuses_uncertified_edge():
    """The ladder's lower rung: nothing was refuted, the edge simply never earned admission."""
    srv, _con = _server_con(_ONE_ROUTE, _TWO_ROUTE_TABLES)      # never published
    fr = srv.frame("quarter").column("revenue", "revenue").run()
    assert fr.outcome == "refuse"
    assert fr.columns[0].refusal.classified().reason == "uncertified_edge"


# ══ GAP 1 — the AT-metric obeys the REQUESTED anchor ══════════════════════════════════════════════
def test_at_metric_cannot_bypass_uncertified_transport(fixture_connector):
    """The resolution anchor says where the metric is FORMED; the requested anchor says where it must
    lawfully TRAVEL. Same manifold, same `day -> cal.month` edge, nothing certified: the plain derived
    ratio refuses, so the AT-anchored one must refuse too. The law cannot depend on which spelling of
    the same transport the author chose."""
    srv = ManifoldServer(parse_manifold(open(_CML).read() + "\n" + _AT_DEFS), fixture_connector)
    plain = srv.frame("cal.month").column("aov").run()
    assert plain.data is None
    at = srv.frame("cal.month").column("daily_aov").run()
    assert at.data is None, f"the AT-metric travelled an uncertified edge (served {at.outcome})"
    assert at.columns[0].refusal.classified().reason == "uncertified_edge"


def test_at_metric_still_serves_once_the_route_is_certified(fixture_connector):
    """The other half — the gate is the SCOPE, not a ban on AT metrics. Publishing the identical
    manifold admits day -> cal.month and the AT-metric travels it."""
    srv = ManifoldServer(parse_manifold(open(_CML).read() + "\n" + _AT_DEFS), fixture_connector)
    srv.publish()
    at = srv.frame("cal.month").column("daily_aov").run()
    assert at.data is not None and at.outcome in ("serve", "disclose")


# ══ GAP 3 — certification identity is per-lineage ═════════════════════════════════════════════════
_SHARED_HOP = """
MANIFOLD h3 VERSION 1
UNIVERSE sales = day
LEVEL day = day BASE
LEVEL month = month
HIERARCHY good { day -> month VIA cal(day, month) }
HIERARCHY shadow { day -> month VIA missing_tbl(day, month) }
MEASURE revenue ON sales FROM tx AS sum(amount)
"""
_SHARED_TABLES = {
    "cal": (["day", "month"], [("d1", "m1"), ("d2", "m1")]),
    "tx":  (["day", "amount"], [("d1", 10.0), ("d2", 20.0)]),
}


def test_certification_is_lineage_specific_and_does_not_bleed():
    """`good` corroborates day->month; `shadow` declares the same hop VIA a table that does not exist,
    so it is UNTESTABLE and never earns admission. Keyed on the level pair alone, one lineage's evidence
    silently licensed the other's edge; keyed on EdgeKey(lineage, frm, to) it cannot."""
    from columna_core.model import UNTESTABLE, CORROBORATED
    srv, _con = _server_con(_SHARED_HOP, _SHARED_TABLES)
    srv.publish()
    verdicts = {h.lineage: h.license.verdict for h in srv.m.hierarchies}
    assert verdicts["shadow"] == UNTESTABLE and verdicts["good"] == CORROBORATED

    shadow_edge = next(e for e in srv.m.edges if e.lineage == "shadow")
    good_edge = next(e for e in srv.m.edges if e.lineage == "good")
    assert not srv.planner.m._admitted(shadow_edge), "an UNTESTABLE lineage rode another's verdict"
    assert srv.planner.m._admitted(good_edge)
    assert srv.published_scope.certified_edges == frozenset({EdgeKey("good", "day", "month")})

    # and the query travels the certified lineage — never the untestable co-located one.
    # (explain(execute=True) IS the first execution here; a second identical query would cache-hit
    # and emit no transport line at all.)
    trace = srv.frame("month").column("revenue", "revenue").explain().splitlines()
    assert any("along good" in ln for ln in trace), trace
    assert not any("along shadow" in ln for ln in trace), trace


# ══ the engine may not choose a route, even if asked directly ═════════════════════════════════════
def test_engine_refuses_to_transport_without_a_planned_route():
    """The structural backstop for the whole ruling: there is no `if no planned path: find_path(...)`
    fallback anywhere on a governed path. Called with no route plan, the engine refuses rather than
    selecting one — absence of an admitted route is CLOSED, not an invitation."""
    from columna_core.disclosure import Refusal
    srv, _con = _server_con(_SHARED_HOP, _SHARED_TABLES)
    srv.publish()
    with pytest.raises(Refusal) as ei:
        srv.engine.resolve("revenue", "sum", ("month",))        # no routes= handed down
    assert ei.value.reason == "uncertified_edge"


# ══ ORDER AXIS — declared structure may not create an executable capability ═══════════════════════
# Ruling 2026-08-11: an order axis is execution-relevant (it fixes the sort a scan walks, so it moves
# shipped numbers). A declared-but-uncertified temporal hierarchy therefore confers no axis: it may
# inform conservative diagnosis, but it may not turn "no lawful axis -> refuse" into "one -> serve".
_SCAN_MANIFOLD = """
MANIFOLD sc VERSION 1
UNIVERSE sales = day
LEVEL day = day BASE
LEVEL cal.month = month
HIERARCHY calendar { day -> cal.month VIA cal(day, month) }
MEASURE revenue ON sales FROM tx AS sum(amount)
"""
_SCAN_TABLES_OK = {
    "cal": (["day", "month"], [("d1", "m1"), ("d2", "m2"), ("d3", "m3")]),
    "tx":  (["day", "amount"], [("d1", 10.0), ("d2", 20.0), ("d3", 30.0)]),
}
# same topology, but the VIA table does not exist -> the hierarchy is UNTESTABLE, never admitted
_SCAN_TABLES_UNCERTIFIED = {"tx": _SCAN_TABLES_OK["tx"]}


def test_uncertified_temporal_hierarchy_confers_no_order_axis():
    """Anchored on the BASE level `day`, so NO transport is involved and the order axis is the only
    thing under test. The one thing that could make `day` an order axis is the `calendar` hierarchy it
    sits on. Leave that UNCERTIFIED (undeliverable VIA table -> UNTESTABLE, publish still succeeds) and
    the scan must refuse for want of a lawful axis — never quietly pick one off the declared graph."""
    from columna_core.model import UNTESTABLE
    srv, _con = _server_con(_SCAN_MANIFOLD, _SCAN_TABLES_UNCERTIFIED)
    srv.publish()                                              # untestable, not refuted
    assert srv.m.hierarchies[0].license.verdict == UNTESTABLE
    assert srv.planner.m.orderable_levels() == frozenset(), "an uncertified lineage conferred an axis"

    fr = srv.frame("day").column("c", "cumsum(revenue.sum)").run()
    assert fr.outcome in ("refuse", "error"), f"scanned on an uncertified order axis ({fr.outcome})"
    assert fr.data is None
    # ...and specifically for want of a CERTIFIED axis — not because anything failed to transport
    detail = str(fr.columns[0].refusal)
    assert "order axis" in detail and "CERTIFIED" in detail, detail
    assert "uncertified_edge" not in detail, f"refused for transport, not the axis: {detail}"

    # ...and NAMING IT DOES NOT RESCUE IT. This assertion is inverted from what it said before
    # P1-24 (ruled Huayin, 2026-09-01): "`by=` is the author naming the axis explicitly ... so it
    # serves." That was the loophole. The test asserts three lines above that the uncertified lineage
    # confers NO orderable level; honouring `by='day'` anyway let an explicit name manufacture the
    # standing the certification withheld, which is exactly what
    #     "explicit `by=` may SELECT governed order standing; it may not CREATE it"
    # forbids. The gate is on the STANDING, not on how the axis was arrived at.
    named = srv.frame("day").column("c", "cumsum(revenue.sum, by='day')").run()
    assert named.outcome == "refuse", named.outcome
    assert named.columns[0].refusal.reason == "order_not_governed"
    assert named.data is None, "a refused scan must not also return the walk it refused to justify"
    # The cumulative walk itself is NOT lost from the suite — it is asserted, on a CERTIFIED
    # hierarchy where it is lawful, by the very next test. That test is also the standing evidence
    # that scan execution works, which P0-20 needs; nothing here may weaken it.


def test_certified_temporal_hierarchy_yields_a_planned_axis_the_engine_uses():
    """Same manifold, same topology, same query, same anchor — the edge now CORROBORATED. The planner
    selects the axis and the engine walks exactly it. Certification is the ONLY difference between this
    and the test above, which is the whole point."""
    srv, _con = _server_con(_SCAN_MANIFOLD, _SCAN_TABLES_OK)
    srv.publish()
    assert "day" in srv.planner.m.orderable_levels()
    assert srv.planner.plan_order_axis("cumsum", "revenue", ("day",)) == "day"

    fr = srv.frame("day").column("c", "cumsum(revenue.sum)").run()
    assert fr.outcome in ("serve", "disclose"), fr.outcome
    rows = {r["day"]: float(r["c"]) for r in fr.data.iter_rows(named=True)}
    assert rows == {"d1": 10.0, "d2": 30.0, "d3": 60.0}, rows      # the cumulative walk, in order

    trace = srv.frame("day").column("c", "cumsum(revenue.sum)").explain().splitlines()
    assert any("ordered by 'day'" in ln for ln in trace), trace


def test_engine_refuses_to_scan_without_a_planned_order_axis():
    """The backstop, symmetric with the transport one: handed no axis, the engine refuses rather than
    inferring one from the declared graph. There is no fallback."""
    from columna_core.disclosure import Refusal
    srv, _con = _server_con(_SCAN_MANIFOLD, _SCAN_TABLES_OK)
    srv.publish()
    routes, split = srv.planner.plan_routes("revenue", ("day",))
    with pytest.raises(Refusal):
        srv.engine.scan("revenue", "sum", ("day",), "cumsum",
                        routes=routes, split=split)               # no order_axis= handed down

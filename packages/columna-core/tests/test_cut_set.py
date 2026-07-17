"""
test_cut_set.py — the published-scope / cut-set (WP on-ramp/Explorer tier-2, CP-1 increment 4, B1).

The scope-edit law made concrete: `publish()` is strict (a violated invariant fails closed);
`reattest()` is the constitutionally different verb — a violation EDITS the published scope (cuts the
declaration cone), returns the authoring-event diff, and is SYMMETRIC (fixing the data restores the
region — no ratchet). A query into a cut region refuses as the `conflicting_data` MOOD; everything
else serves untouched. The PublishedScope is a pure function of the current attestation's verdicts.
"""
import duckdb

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.parser import parse_manifold


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


def _server_con(manifold_text, tables):
    con = duckdb.connect()
    for name, (cols, rows) in tables.items():
        values = ", ".join("(" + ", ".join(_lit(v) for v in row) + ")" for row in rows)
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM (VALUES {values}) AS t({', '.join(cols)})")
    return ManifoldServer(parse_manifold(manifold_text), DuckDBConnector(con)), con


_CUT = """
MANIFOLD c VERSION 1
UNIVERSE sales = store
LEVEL store = store_id BASE
MEASURE revenue   ON sales FROM tx AS sum(amount)
MEASURE gross     ON sales FROM tx AS sum(gross)
MEASURE discounts ON sales FROM tx AS sum(disc)
MEASURE orders    ON sales FROM tx AS count(*)
DERIVED aov = revenue / orders
ASSERT recon ON sales AT store HOLDS revenue == gross - discounts
"""


def _outcome(srv, col):
    return srv.frame("store").column(col, col).run().outcome


def test_cut_set_full_lifecycle():
    srv, con = _server_con(_CUT, {"tx": (["store_id", "amount", "gross", "disc"], [
        ("s1", 100.0, 120.0, 20.0), ("s2", 50.0, 50.0, 0.0)])})

    # 1) first publish — the assert holds, strict, clean scope
    srv.publish()
    assert srv.published_scope.cut == frozenset()
    assert _outcome(srv, "revenue") == "serve"

    # 2) data drifts to violate the invariant, then RE-ATTEST — scope is EDITED, not failed
    con.execute("UPDATE tx SET disc = 10 WHERE store_id = 's1'")   # revenue=100 but gross-disc=110
    diff = srv.reattest()
    assert {"revenue", "gross", "discounts", "aov"} <= set(diff["cuts"])   # cone: seeds + derived
    assert "orders" not in srv.published_scope.cut                        # outside the cone
    assert diff["cut_by"]["revenue"][0]["counterexample"]                 # summoning coordinates present

    # 3) a query INTO the cut refuses as the conflicting_data MOOD; the derived cone too; the rest serves
    fr = srv.frame("store").column("revenue", "revenue").run()
    assert fr.outcome == "refuse"
    assert fr.columns[0].refusal.classified().reason == "conflicting_data"
    assert _outcome(srv, "aov") == "refuse"        # derived cone is cut
    assert _outcome(srv, "orders") == "serve"      # untouched declaration serves

    # 4) fix the data and RE-ATTEST — symmetric: the region is RESTORED, no ratchet
    con.execute("UPDATE tx SET disc = 20 WHERE store_id = 's1'")
    diff2 = srv.reattest()
    assert "revenue" in diff2["restores"] and not diff2["cuts"]
    assert srv.published_scope.cut == frozenset()
    assert _outcome(srv, "revenue") == "serve"


def test_reattest_with_no_violation_is_an_empty_authoring_event():
    srv, con = _server_con(_CUT, {"tx": (["store_id", "amount", "gross", "disc"], [
        ("s1", 100.0, 120.0, 20.0)])})
    srv.publish()
    diff = srv.reattest()
    assert diff == {"cuts": [], "restores": [], "revocations": [], "relicenses": [],
                    "blocked_edges": [], "unblocked_edges": [], "cut_by": {}, "blocked_by": {}}
    assert srv.published_scope.cut == frozenset()


# ── edges degrade to BLOCKED TRANSPORT (the third degrade target; Huayin 2026-07-16) ───────────────
_HDEG = """
MANIFOLD hd VERSION 1
UNIVERSE sales = day
LEVEL day   = day   BASE
LEVEL month = month
HIERARCHY day -> month ALONG calendar VIA cal(day, month)
MEASURE revenue ON sales FROM tx AS sum(amount)
"""


def test_hierarchy_degrades_to_blocked_transport_not_manifold_failure():
    srv, con = _server_con(_HDEG, {
        "cal": (["day", "month"], [("d1", "m1"), ("d2", "m1")]),          # functional at birth
        "tx":  (["day", "amount"], [("d1", 10.0), ("d2", 20.0)])})
    srv.publish()
    assert srv.published_scope.blocked_edges == frozenset()
    assert srv.frame("month").column("revenue", "revenue").run().outcome in ("serve", "disclose")

    # the FD breaks on new data: d1 now maps to two months. RE-ATTEST — the edge blocks, nothing else fails.
    con.execute("INSERT INTO cal VALUES ('d1', 'm2')")
    diff = srv.reattest()
    assert ("day", "month") in diff["blocked_edges"]
    assert diff["blocked_by"][("day", "month")][0]["key"] == "d1"
    assert diff["cuts"] == []                                              # NOT manifold-level severity

    # transport ACROSS the blocked edge refuses contradicted_edge; the base grain still serves
    fr = srv.frame("month").column("revenue", "revenue").run()
    assert fr.outcome == "refuse"
    assert fr.columns[0].refusal.classified().reason == "contradicted_edge"
    assert srv.frame("day").column("revenue", "revenue").run().outcome in ("serve", "disclose")

    # fix the data -> symmetric restore (the edge unblocks, transport returns)
    con.execute("DELETE FROM cal WHERE day = 'd1' AND month = 'm2'")
    diff2 = srv.reattest()
    assert ("day", "month") in diff2["unblocked_edges"]
    assert srv.frame("month").column("revenue", "revenue").run().outcome in ("serve", "disclose")


def test_publish_still_fails_closed_on_first_violation():
    # publish is the strict verb — a violated invariant at first birth fails closed (never cuts).
    from columna_core import AssertContradiction
    import pytest
    srv, _ = _server_con(_CUT, {"tx": (["store_id", "amount", "gross", "disc"], [
        ("s1", 100.0, 120.0, 10.0)])})     # violates from birth
    with pytest.raises(AssertContradiction):
        srv.publish()

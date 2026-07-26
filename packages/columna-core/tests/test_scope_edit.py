"""
test_scope_edit.py — the published scope and its degradation (WP on-ramp/Explorer tier-2, CP-1).

The scope-edit law made concrete: `publish()` is strict; `reattest()` is the constitutionally
different verb — a refutation EDITS the published scope, returns the authoring-event diff, and is
SYMMETRIC (fixing the data restores what was withdrawn — no ratchet). The PublishedScope is a pure
function of the current attestation's verdicts.

Provenance: this file is the surviving half of `test_cut_set.py`. The CUT degrade target was the
ASSERT channel's, and it retired with ASSERT in 0.13.0 (ruling 2026-07-26) — one construct, one
degrade target, both gone. The two targets that survive have their own provers and are exercised
here: edges degrade to BLOCKED TRANSPORT (a refuted HIERARCHY), licenses degrade to RECOMPUTE (a
refuted fertility claim — covered in test_adjudication.py).
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


# ── edges degrade to BLOCKED TRANSPORT (Huayin 2026-07-16) ─────────────────────────────────────────
_HDEG = """
MANIFOLD hd VERSION 1
UNIVERSE sales = day
LEVEL day   = day   BASE
LEVEL month = month
HIERARCHY calendar { day -> month VIA cal(day, month) }
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


def test_reattest_with_no_refutation_is_an_empty_authoring_event():
    srv, con = _server_con(_HDEG, {
        "cal": (["day", "month"], [("d1", "m1")]),
        "tx":  (["day", "amount"], [("d1", 10.0)])})
    srv.publish()
    diff = srv.reattest()
    assert diff["blocked_edges"] == [] and diff["unblocked_edges"] == []
    assert diff["revocations"] == [] and diff["relicenses"] == []
    assert srv.published_scope.blocked_edges == frozenset()

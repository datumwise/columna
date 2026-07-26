"""
test_track1_adjudication.py — HIERARCHY adjudication (WP on-ramp/Explorer tier-2, CP-1).

The kernel-reuse demonstration (the ADR-034 generality test): the SAME adjudicator that licenses
derived-column fertility also licenses B2 hierarchies — minting the UNCHANGED `License`, failing
publish CLOSED on refutation via a `Contradiction` sibling. No `License` field changed; this is a new
customer of the kernel, not a change to it.

The B1 ASSERT half retired with the construct in 0.13.0 (ruling 2026-07-26): its provers licensed no
serving behavior, so it failed the admission test. HIERARCHY is the counter-example the doctrine
names — its prover licenses climbs, so it stays.
"""
import duckdb
import pytest

from columna_core import (License, CORROBORATED, ManifoldServer, DuckDBConnector,
                          adjudicate, Contradiction, HierarchyContradiction)
from columna_core.parser import parse_manifold


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


def _server(manifold_text: str, tables: dict) -> ManifoldServer:
    con = duckdb.connect()
    for name, (cols, rows) in tables.items():
        values = ", ".join("(" + ", ".join(_lit(v) for v in row) + ")" for row in rows)
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM (VALUES {values}) AS t({', '.join(cols)})")
    return ManifoldServer(parse_manifold(manifold_text), DuckDBConnector(con))


# ── B2 HIERARCHY — functional-dependence test ─────────────────────────────────────────────────────
_HIER = """
MANIFOLD h VERSION 1
UNIVERSE u = day
LEVEL day = day BASE
LEVEL week = week
LEVEL month = month
HIERARCHY calendar { day -> week VIA caltbl(day, week) -> month VIA caltbl(week, month) }
MEASURE n ON u FROM ev AS count(*)
"""


def test_hierarchy_fd_holds_is_corroborated():
    srv = _server(_HIER, {"caltbl": (["day", "week", "month"], [
        ("d1", "w1", "m1"), ("d2", "w1", "m1"), ("d3", "w2", "m1")])})
    report = adjudicate(srv)
    assert report["_hierarchies"]["calendar"] == CORROBORATED
    lic = srv.m.hierarchies[0].license
    assert isinstance(lic, License) and lic.verdict == CORROBORATED   # the UNCHANGED License type


def test_hierarchy_fd_violation_fails_closed():
    # d1 maps to two weeks — not a function; publish must fail closed.
    srv = _server(_HIER, {"caltbl": (["day", "week", "month"], [
        ("d1", "w1", "m1"), ("d1", "w2", "m1")])})
    with pytest.raises(HierarchyContradiction) as ei:
        adjudicate(srv)
    assert isinstance(ei.value, Contradiction)             # sibling of the fertility contradiction
    assert "not functional" in str(ei.value) and "d1" in str(ei.value)


def test_demo_adjudication_still_clean(fixture_server):
    # the shipped demo declares no hierarchies; the fertility path is unchanged and publishes.
    report = adjudicate(fixture_server)
    assert "_hierarchies" not in report

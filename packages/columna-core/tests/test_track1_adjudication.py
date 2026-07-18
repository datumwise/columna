"""
test_track1_adjudication.py — ASSERT + HIERARCHY adjudication (WP on-ramp/Explorer tier-2, CP-1).

The kernel-reuse demonstration (the ADR-034 generality test): the SAME adjudicator that licenses
derived-column fertility now also licenses B1 invariants and B2 hierarchies — minting the UNCHANGED
`License`, failing publish CLOSED on refutation via `Contradiction` siblings. No `License` field
changed; these are new customers of the kernel, not changes to it.
"""
import duckdb
import pytest

from columna_core import (License, CORROBORATED, UNTESTABLE, ManifoldServer, DuckDBConnector,
                          adjudicate, Contradiction, AssertContradiction, HierarchyContradiction,
                          AssertNotWellFormed)
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


# ── B1 ASSERT — invariant at an anchor ────────────────────────────────────────────────────────────
_ASSERT = """
MANIFOLD a VERSION 1
UNIVERSE sales = store
LEVEL store = store_id BASE
MEASURE revenue   ON sales FROM tx AS sum(amount)
MEASURE gross     ON sales FROM tx AS sum(gross)
MEASURE discounts ON sales FROM tx AS sum(disc)
ASSERT recon ON sales AT store HOLDS revenue == gross - discounts
"""


def test_assert_invariant_holds_is_corroborated():
    # per store: sum(amount) == sum(gross) - sum(disc)
    srv = _server(_ASSERT, {"tx": (["store_id", "amount", "gross", "disc"], [
        ("s1", 100.0, 120.0, 20.0), ("s1", 50.0, 60.0, 10.0), ("s2", 30.0, 30.0, 0.0)])})
    report = adjudicate(srv)
    assert report["_asserts"]["sales.recon"] == CORROBORATED
    lic = srv.m.asserts[0].license
    assert isinstance(lic, License) and lic.verdict == CORROBORATED and lic.attestation


def test_assert_invariant_violation_fails_closed():
    # s2: revenue=30 but gross-disc = 30-10 = 20 -> violated
    srv = _server(_ASSERT, {"tx": (["store_id", "amount", "gross", "disc"], [
        ("s1", 100.0, 120.0, 20.0), ("s2", 30.0, 30.0, 10.0)])})
    with pytest.raises(AssertContradiction) as ei:
        adjudicate(srv)
    assert isinstance(ei.value, Contradiction)
    assert "recon" in str(ei.value)


_ROW = """
MANIFOLD r VERSION 1
UNIVERSE sales = store
LEVEL store = store_id BASE
LEVEL region = region
HIERARCHY geo { store -> region VIA stores(store_id, region) }
MEASURE revenue ON sales FROM tx AS sum(amount)
ASSERT nonneg ON sales WHERE region >= 0
"""


def test_row_assert_is_untestable_in_this_build():
    srv = _server(_ROW, {"tx": (["store_id", "amount"], [("s1", 10.0)]),
                         "stores": (["store_id", "region"], [("s1", "r1")])})
    report = adjudicate(srv)
    assert report["_asserts"]["sales.nonneg"] == UNTESTABLE
    assert srv.m.asserts[0].license.verdict == UNTESTABLE


def test_demo_adjudication_still_clean(fixture_server):
    # the shipped demo has no asserts/hierarchies; the fertility path is unchanged and publishes.
    report = adjudicate(fixture_server)
    assert "_asserts" not in report and "_hierarchies" not in report


# ── rider 1: "you may not assert what may not be asked" — ill-posed invariants FAIL CLOSED at ──────
#            declaration, naming the reason; NEVER UNTESTABLE (that stays for askable-but-unattested).
_BLOCKED = """
MANIFOLD b VERSION 1
UNIVERSE sd = store * day
LEVEL store = store_id BASE
LEVEL day   = day      BASE
LEVEL region = region
LEVEL month = month
HIERARCHY geo { store -> region VIA stores(store_id, region) }
HIERARCHY calendar { day -> month VIA cal(day, month) }
MEASURE level ON sd FROM inv VALUE lvl
    M_ANCHOR { }
    FAMILY {
        sum  BLOCKED { calendar }
        last ORDER day
    }
ASSERT r ON sd AT region HOLDS level.sum >= level.last
"""


def test_blocked_reduction_invariant_fails_closed_at_declaration():
    # level.sum @ region collapses `day` along the BLOCKED calendar lineage — disclose-critical, not a
    # clean quantity. Must fail publish closed (well-formedness), never UNTESTABLE.
    srv = _server(_BLOCKED, {"stores": (["store_id", "region"], [("s1", "r1")]),
                             "cal": (["day", "month"], [("d1", "m1")]),
                             "inv": (["store_id", "day", "lvl"], [("s1", "d1", 5.0)])})
    with pytest.raises(AssertNotWellFormed) as ei:
        adjudicate(srv)
    assert "blocked_reduction" in str(ei.value) and "LHS" in str(ei.value)


_UNPINNED = """
MANIFOLD u VERSION 1
UNIVERSE sales = store * day
LEVEL store = store_id BASE
LEVEL day   = day      BASE
LEVEL region = region
HIERARCHY geo { store -> region VIA stores(store_id, region) }
MEASURE revenue ON sales FROM tx AS sum(amount)
ASSERT r ON sales AT region HOLDS mean(revenue) >= revenue
"""


def test_unpinned_inline_reduction_invariant_fails_closed():
    # mean(revenue) @ region does not pin its input anchor -> input_anchor_ambiguous (clarify).
    srv = _server(_UNPINNED, {"stores": (["store_id", "region"], [("s1", "r1")]),
                              "tx": (["store_id", "day", "amount"], [("s1", "d1", 10.0)])})
    with pytest.raises(AssertNotWellFormed) as ei:
        adjudicate(srv)
    assert "input_anchor_ambiguous" in str(ei.value)


def test_unknown_name_invariant_fails_closed_at_declaration():
    # the third ill-posed shape: an unknown name. Parses clean (invariants may use inline reductions,
    # so expression content is the planner's authority), then fails publish closed at adjudication.
    m = _ASSERT.replace("revenue == gross - discounts", "revenue == nonesuch")
    srv = _server(m, {"tx": (["store_id", "amount", "gross", "disc"], [("s1", 1.0, 1.0, 0.0)])})
    with pytest.raises(AssertNotWellFormed) as ei:
        adjudicate(srv)
    assert "nonesuch" in str(ei.value) or "unknown" in str(ei.value)

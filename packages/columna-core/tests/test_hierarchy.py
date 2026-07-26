"""
test_hierarchy.py — HIERARCHY parsing (WP on-ramp/Explorer tier-2, CP-1, B2).

Parser + model + well-formedness only. HIERARCHY desugars to edges INDISTINGUISHABLE from
hand-declared EDGEs (the single truth), plus a provenance record carrying the branching paths.

Provenance: this file is the surviving half of `test_assert_hierarchy.py`. Its B1 ASSERT half retired
with the construct in 0.13.0 (ruling 2026-07-26); B2 HIERARCHY did not retire, so its coverage moved
here rather than dying with the filename it happened to share.
"""
import pytest

from columna_core.parser import parse_manifold, ParseError


_M = """
MANIFOLD t VERSION 1
UNIVERSE sales = store * day
UNIVERSE ops   = store * day BASIS events
LEVEL store = store_id BASE
LEVEL day   = day      BASE
LEVEL region = region
LEVEL week  = week
LEVEL month = month
HIERARCHY geo { store -> region VIA stores(store_id, region) }
MEASURE revenue   ON sales FROM sales AS sum(amount)
MEASURE gross     ON sales FROM sales AS sum(gross_amt)
MEASURE discounts ON sales FROM sales AS sum(disc)
"""


def _m(*extra):
    return parse_manifold(_M + "\n".join(extra) + "\n")


# ── HIERARCHY ────────────────────────────────────────────────────────────────────────────────────
def test_hierarchy_desugars_to_edges_indistinguishable_from_hand_edges():
    m = _m("HIERARCHY calendar { day -> week VIA caltbl(day, week) -> month VIA caltbl(week, month) }")
    # two plain FunctionalEdges, connecting consecutive pairs, ALONG the lineage
    cal = [e for e in m.edges if e.lineage == "calendar"]
    assert {(e.frm, e.to) for e in cal} == {("day", "week"), ("week", "month")}
    assert all(e.provider_table == "caltbl" for e in cal)
    # the single truth: find_path traverses them exactly like hand-declared edges
    assert m.find_path(["day"], "month") is not None
    # provenance recorded, communicative only — the branching-path record (§2a EDGE purge)
    h = next(h for h in m.hierarchies if h.lineage == "calendar")
    assert h.paths == (("day", "week", "month"),)
    assert h.chain == ("day", "week", "month")   # back-compat: the primary path


def test_hierarchy_hop_needs_per_hop_via():
    # §2a: every hop carries its own VIA(<col>, <col>). Bare arrows with no VIA don't parse as hops.
    with pytest.raises(ParseError) as ei:
        _m("HIERARCHY calendar { day -> week -> month }")
    assert "HIERARCHY" in str(ei.value)


def test_hierarchy_path_needs_at_least_two_levels():
    with pytest.raises(ParseError) as ei:
        _m("HIERARCHY calendar { day }")
    assert ">= 2 levels" in str(ei.value)


def test_shipped_demo_still_parses_clean(parsed_manifold):
    # post §2a EDGE-purge: the demo declares its functional paths as HIERARCHYs
    assert {h.lineage for h in parsed_manifold.hierarchies} == {"store_geo", "calendar"}

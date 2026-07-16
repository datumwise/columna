"""
test_assert_hierarchy.py — ASSERT + HIERARCHY parsing (WP on-ramp/Explorer tier-2, CP-1, B1/B2).

Parser + model + well-formedness only (CP-1 syntax increment). Adjudication (the data-channel
verdicts that mint a License) is the next increment. Syntax approved by Huayin (2026-07-15) with four
riders, all exercised here: row-WHERE reuses the universe-carving predicate grammar; the aggregate
anchor is the ruled `*` grammar; the comparison set is {==,<=,>=,<,>}; assert names are universe-scoped.
HIERARCHY desugars to edges INDISTINGUISHABLE from hand-declared EDGEs (the single truth), plus a
provenance record.
"""
import pytest

from columna_core.parser import parse_manifold, ParseError, ASSERT_OPS


_M = """
MANIFOLD t VERSION 1
UNIVERSE sales = store * day
UNIVERSE ops   = store * day BASIS events
LEVEL store = store_id BASE
LEVEL day   = day      BASE
LEVEL region = region
LEVEL week  = week
LEVEL month = month
EDGE store -> region ALONG geo VIA stores(store_id, region)
MEASURE revenue   ON sales FROM sales AS sum(amount)
MEASURE gross     ON sales FROM sales AS sum(gross_amt)
MEASURE discounts ON sales FROM sales AS sum(disc)
"""


def _m(*extra):
    return parse_manifold(_M + "\n".join(extra) + "\n")


# ── ASSERT row-form ─────────────────────────────────────────────────────────────────────────────
def test_row_assert_parses_and_reuses_predicate_grammar():
    m = _m("ASSERT nonneg ON sales WHERE region >= 0")
    a = m.asserts[0]
    assert (a.name, a.universe, a.kind) == ("nonneg", "sales", "row")
    assert a.predicate is not None


def test_row_assert_referencing_a_measure_is_impure():
    with pytest.raises(ParseError) as ei:
        _m("ASSERT bad ON sales WHERE revenue >= 0")
    assert "measure 'revenue'" in str(ei.value)


# ── ASSERT invariant-form ───────────────────────────────────────────────────────────────────────
def test_invariant_assert_parses_left_op_right():
    m = _m("ASSERT recon ON sales AT store HOLDS revenue == gross - discounts")
    a = m.asserts[0]
    assert a.kind == "invariant" and a.anchor == ("store",)
    assert (a.left, a.op, a.right) == ("revenue", "==", "gross - discounts")


@pytest.mark.parametrize("op", list(ASSERT_OPS))
def test_each_comparison_op_parses(op):
    m = _m(f"ASSERT c ON sales AT store HOLDS revenue {op} gross")
    assert m.asserts[0].op == op


def test_invariant_anchor_uses_the_ruled_star_grammar():
    m = _m("ASSERT r2 ON sales AT store*day HOLDS revenue <= gross")
    assert m.asserts[0].anchor == ("store", "day")


def test_invariant_anchor_comma_still_accepted():
    m = _m("ASSERT r3 ON sales AT store, day HOLDS revenue <= gross")
    assert m.asserts[0].anchor == ("store", "day")


def test_invariant_unknown_column_fails_closed():
    with pytest.raises(ParseError) as ei:
        _m("ASSERT r ON sales AT store HOLDS revenue == nonesuch")
    assert "unknown column 'nonesuch'" in str(ei.value)


def test_invariant_bad_anchor_level_fails_closed():
    with pytest.raises(ParseError) as ei:
        _m("ASSERT r ON sales AT nowhere HOLDS revenue <= gross")
    assert "unknown level 'nowhere'" in str(ei.value)


def test_not_equal_is_not_in_v1_set():
    with pytest.raises(ParseError):                 # `!=` is excluded; no comparison is found
        _m("ASSERT r ON sales AT store HOLDS revenue != gross")


def test_assert_unknown_universe_fails_closed():
    with pytest.raises(ParseError) as ei:
        _m("ASSERT r ON nosuch WHERE region >= 0")
    assert "unknown universe 'nosuch'" in str(ei.value)


# ── universe-scoped names (rider 4) ──────────────────────────────────────────────────────────────
def test_duplicate_assert_name_same_universe_fails():
    with pytest.raises(ParseError) as ei:
        _m("ASSERT ok ON sales WHERE region >= 0",
           "ASSERT ok ON sales WHERE region <= 100")
    assert "duplicate ASSERT 'ok'" in str(ei.value)


def test_same_assert_name_across_universes_is_allowed():
    m = _m("ASSERT ok ON sales WHERE region >= 0",
           "ASSERT ok ON ops   WHERE region >= 0")
    assert len(m.asserts) == 2


# ── HIERARCHY ────────────────────────────────────────────────────────────────────────────────────
def test_hierarchy_desugars_to_edges_indistinguishable_from_hand_edges():
    m = _m("HIERARCHY day -> week -> month ALONG calendar VIA caltbl(day, week, month)")
    # two plain FunctionalEdges, connecting consecutive pairs, ALONG the lineage
    cal = [e for e in m.edges if e.lineage == "calendar"]
    assert {(e.frm, e.to) for e in cal} == {("day", "week"), ("week", "month")}
    assert all(e.provider_table == "caltbl" for e in cal)
    # the single truth: find_path traverses them exactly like hand-declared edges
    assert m.find_path(["day"], "month") is not None
    # provenance recorded, communicative only
    h = m.hierarchies[0]
    assert (h.lineage, h.chain, h.via_table) == ("calendar", ("day", "week", "month"), "caltbl")


def test_hierarchy_column_count_must_match_levels():
    with pytest.raises(ParseError) as ei:
        _m("HIERARCHY day -> week -> month ALONG calendar VIA caltbl(day, week)")
    assert "one column per level" in str(ei.value)


def test_hierarchy_needs_at_least_two_levels():
    with pytest.raises(ParseError) as ei:
        _m("HIERARCHY day ALONG calendar VIA caltbl(day)")
    assert ">= 2 levels" in str(ei.value)


def test_shipped_demo_still_parses_clean(parsed_manifold):
    assert not parsed_manifold.asserts and not parsed_manifold.hierarchies

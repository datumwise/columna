"""
test_anchor_grammar.py — the ruled anchor naming and product laws (WP anchor-grammar v0.1).

Covers the manifold-AWARE half of the WP (the manifold-blind string parser `*` lives in
test_frameql_parse.py):
  · item 2  — level leaf-name uniqueness, scoped PER UNIVERSE (well-formedness, fail closed)
  · item 3a — anchor-side `family.level` resolution + edge-derived membership (planner resolution)
  · item 3b — the "one bad state": a single token reaching two levels (well-formedness, fail closed)
  · item 4  — universe names rejected in anchor position (planner resolution)

Resolution errors ride the EXISTING query-error channel: FrameQLSyntaxError — the same class the
server catches to emit the `frameql_syntax` wire error. No new wire reason code; the four-mood wire
is byte-identical.
"""
import pytest

from columna_core import FrameQLSyntaxError, ManifoldServer
from columna_core.parser import parse_manifold, ParseError, check_wellformed
from columna_core.projection import PlannerView
from columna_core.planner import Planner


def _resolver(text: str) -> Planner:
    """A Planner over a parsed manifold, engine-free (resolve_anchor never touches the engine)."""
    return Planner(PlannerView(parse_manifold(text)), engine=None)


# a clean, dotless family.level manifold — `region` ∈ family `geo`, `month` ∈ family `cal`.
_CLEAN = """
MANIFOLD t VERSION 1
UNIVERSE sales = store * day
LEVEL store  = store_id BASE
LEVEL day    = day      BASE
LEVEL region = region
LEVEL month  = month
HIERARCHY geo { store -> region VIA stores(store_id, region) }
HIERARCHY cal { day -> month VIA calx(day, month) }
MEASURE revenue ON sales FROM sales AS sum(amount)
"""


# ── item 4 · universe names never appear in anchor position ─────────────────────────────────────
def test_universe_name_in_anchor_is_rejected():
    p = _resolver(_CLEAN)
    with pytest.raises(FrameQLSyntaxError) as ei:
        p.resolve_anchor(("sales",))
    msg = str(ei.value)
    assert "universe" in msg and "ON UNIVERSE" in msg


def test_universe_rejection_rides_the_frame_build_channel():
    # Integration: a universe-name anchor raises out of ManifoldServer.frame — the existing catch site
    # (the server wraps _build_frame in `except FrameQLSyntaxError`) turns this into a frameql_syntax
    # error. Behavior delta on record: today this is an accidental out_of_universe REFUSAL.
    srv = ManifoldServer(parse_manifold(_CLEAN), connector=object())
    with pytest.raises(FrameQLSyntaxError):
        srv.frame("sales")


# ── item 3a · qualified family.level resolution + edge-derived membership ────────────────────────
def test_literal_level_name_wins_standing_law():
    # STANDING resolution order (not transitional): a literal level-name match wins. `region` and
    # `month` resolve to themselves; nothing is marked for deletion — only the comma retires later.
    p = _resolver(_CLEAN)
    assert p.resolve_anchor(("region", "month")) == ("region", "month")


def test_valid_qualification_resolves_to_the_level():
    p = _resolver(_CLEAN)
    assert p.resolve_anchor(("geo.region",)) == ("region",)
    assert p.resolve_anchor(("cal.month",)) == ("month",)


def test_qualification_wrong_family_names_the_actual_families():
    p = _resolver(_CLEAN)
    with pytest.raises(FrameQLSyntaxError) as ei:
        p.resolve_anchor(("cal.region",))          # region ∈ geo, not cal
    msg = str(ei.value)
    assert "region" in msg and "cal" in msg and "geo" in msg


def test_qualification_unknown_level_is_rejected():
    p = _resolver(_CLEAN)
    with pytest.raises(FrameQLSyntaxError) as ei:
        p.resolve_anchor(("geo.nowhere",))
    assert "no level named 'nowhere'" in str(ei.value)


def test_bare_unknown_token_passes_through_unchanged():
    # A bare (dotless), non-universe, non-level token is NOT a resolution error — it flows to the
    # engine and reaches the SAME out_of_universe addressability mood as before (unchanged behavior).
    p = _resolver(_CLEAN)
    assert p.resolve_anchor(("mystery",)) == ("mystery",)


# ── item 2 · leaf-name uniqueness, scoped PER UNIVERSE ───────────────────────────────────────────
_LEAF_COLLIDE = """
MANIFOLD t VERSION 1
UNIVERSE sales = store * day
LEVEL store       = store_id BASE
LEVEL day         = day      BASE
LEVEL cal.week    = week
LEVEL fiscal.week = fweek
HIERARCHY calendar { day -> cal.week VIA cal(day, week) }
HIERARCHY fiscal { day -> fiscal.week VIA fis(day, fweek) }
MEASURE revenue ON sales FROM sales AS sum(amount)
"""


def test_leaf_collision_within_a_universe_fails_closed_both_sites():
    with pytest.raises(ParseError) as ei:
        parse_manifold(_LEAF_COLLIDE)
    msg = str(ei.value)
    assert "cal.week" in msg and "fiscal.week" in msg     # both declaration sites named
    assert "week" in msg and "sales" in msg


# same leaf ('week') recurs across DIFFERENT universes as distinct levels — allowed.
_LEAF_CROSS_UNIVERSE = """
MANIFOLD t VERSION 1
UNIVERSE u1 = a * day1
UNIVERSE u2 = b * day2
LEVEL a        = a     BASE
LEVEL b        = b     BASE
LEVEL day1     = day1  BASE
LEVEL day2     = day2  BASE
LEVEL cal.week = week
LEVEL fis.week = fweek
HIERARCHY calendar { day1 -> cal.week VIA t1(day1, week) }
HIERARCHY fiscal { day2 -> fis.week VIA t2(day2, fweek) }
MEASURE r1 ON u1 FROM u1 AS sum(p)
MEASURE r2 ON u2 FROM u2 AS sum(q)
"""


def test_same_leaf_across_universes_is_well_formed():
    m = parse_manifold(_LEAF_CROSS_UNIVERSE)          # must NOT raise
    assert not check_wellformed(m)


def test_duplicate_level_declaration_is_rejected():
    dup = _CLEAN.replace("LEVEL month  = month", "LEVEL month  = month\nLEVEL month  = month2")
    with pytest.raises(ParseError) as ei:
        parse_manifold(dup)
    assert "duplicate LEVEL declaration 'month'" in str(ei.value)


# ── item 3b · the one bad state — a single token reaching two levels ─────────────────────────────
# `month` (∈ family `cal`) reachable in u1; the literal dotted level `cal.month` reachable in u2. The
# token `cal.month` would reach BOTH (literal, and the family.level split → `month`). Distinct
# universes, so the per-universe leaf law does NOT fire — the collision law (global) does.
_ONE_BAD_STATE = """
MANIFOLD t VERSION 1
UNIVERSE u1 = a * day1
UNIVERSE u2 = b * day2
LEVEL a         = a       BASE
LEVEL b         = b       BASE
LEVEL day1      = day1    BASE
LEVEL day2      = day2    BASE
LEVEL month     = monthc
LEVEL cal.month = cm
HIERARCHY cal { day1 -> month VIA t1(day1, monthc) }
HIERARCHY other { day2 -> cal.month VIA t2(day2, cm) }
MEASURE r1 ON u1 FROM u1 AS sum(p)
MEASURE r2 ON u2 FROM u2 AS sum(q)
"""


def test_one_bad_state_token_reaching_two_levels_fails_closed():
    with pytest.raises(ParseError) as ei:
        parse_manifold(_ONE_BAD_STATE)
    msg = str(ei.value)
    assert "cal.month" in msg and "month" in msg and "cal" in msg

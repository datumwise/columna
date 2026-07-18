"""
test_expression_law.py — the §2c expression law + frame law (WP on-ramp/Explorer tier-2, CP-1).

A column expression evaluates in ONE universe and never crosses the boundary: a cross-universe
expression is a `cross_universe` ERROR (category error, not a clarify), named with the two legal
paths. Columns from different universes juxtapose (alignment view; the old multi-universe `coverage`
caveat is retired). `co_anchor_ambiguous` is RETIRED (tombstone) — the retirement pin asserts it is
never emitted. Includes the DG-2 everything-classifies pin.
"""
import pytest

from columna_core.disclosure import REASON_OUTCOME
from columna_core.parser import parse_manifold, ParseError


def _col(fr, name="c"):
    return next(c for c in fr.columns if c.name == name)


def test_cross_universe_expression_is_a_category_error(fixture_server):
    fr = fixture_server.frame("store", "day").column("c", "revenue / level.last").run()
    r = _col(fr).refusal
    assert fr.outcome == "error" and r.is_error and r.reason == "cross_universe"
    assert "transactions" in r.detail and "store_days" in r.detail           # names both universes
    assert any("juxtapose" in a for a in r.alternatives) and any("declare" in a for a in r.alternatives)


def test_cross_universe_is_caught_statically(fixture_server):
    fr = fixture_server.frame("store", "day").column("c", "revenue / level.last").plan()
    assert _col(fr).refusal is not None and _col(fr).refusal.reason == "cross_universe"


def test_juxtaposition_serves_without_a_coverage_caveat(fixture_server):
    fr = fixture_server.frame("store", "day").column("rev", "revenue").column("inv", "level.last").run()
    assert _col(fr, "rev").refusal is None and _col(fr, "inv").refusal is None
    assert fr.outcome in ("serve", "disclose")
    assert not fr.disclosure.has("coverage")             # the multi-universe caveat is retired (§2c)


def test_co_anchor_ambiguous_is_retired_and_never_emitted(fixture_server):
    # retirement pin (Huayin 2026-07-16): the reason left the ACTIVE vocabulary (kept only as a dated
    # tombstone comment), and the case that emitted it now emits `cross_universe`.
    assert "co_anchor_ambiguous" not in REASON_OUTCOME
    fr = fixture_server.frame("store", "day").column("c", "revenue / level.last").run()
    assert _col(fr).refusal.reason != "co_anchor_ambiguous"


def test_collapse_with_blocked_transport_classifies_never_raw(fixture_server):
    # DG-2: `level.sum @ cal.month` (collapse `store` while transporting `day` across the BLOCKED
    # calendar lineage) must be CLASSIFIED, never a raw exception. Today the backstop classifies it as
    # error; when DG-2's structural fix lands it becomes disclose-critical (blocked_reduction).
    fr = fixture_server.frame("cal.month").column("c", "level.sum").run()
    assert fr.outcome in ("serve", "disclose", "clarify", "refuse", "error")     # classified, no raw throw
    assert _col(fr).refusal is None or _col(fr).refusal.is_error


# ── §2c single-universe sugar: ON optional with one universe; required with more ──────────────────
_ONE_UNI = """
MANIFOLD s VERSION 1
UNIVERSE sales = store
LEVEL store = store_id BASE
MEASURE revenue FROM tx AS sum(amount)
ASSERT nonneg WHERE store >= 0
"""


def test_single_universe_sugar_fills_the_sole_universe():
    m = parse_manifold(_ONE_UNI)
    assert m.measures["revenue"].universe == "sales"
    assert m.asserts[0].universe == "sales"


def test_on_universe_required_with_more_than_one():
    two = _ONE_UNI.replace("UNIVERSE sales = store\n", "UNIVERSE sales = store\nUNIVERSE ops = store\n")
    with pytest.raises(ParseError) as ei:
        parse_manifold(two)
    assert "'ON <universe>' is required" in str(ei.value)

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


def test_collapse_with_blocked_transport_refuses_blocked_reduction(fixture_server):
    # DG-2, CLOSED 2026-08-20 (generated-family law, Huayin). `level.sum @ cal.month` collapses `store`
    # while transporting `day` across the BLOCKED calendar lineage. It always had to be CLASSIFIED,
    # never a raw exception (the everything-classifies guarantee) — that half is unchanged. What moved
    # is WHICH classification: the row's original target (serve with a critical `blocked_reduction`
    # CAVEAT, via the everything-classifies backstop's `error`/`unsupported` interim) is superseded by
    # a structural REFUSE carrying `blocked_reduction` as its REASON. Disclose may qualify a lawful
    # result; it may not legalize a reduction the governed law does not possess.
    fr = fixture_server.frame("cal.month").column("c", "level.sum").run()
    assert fr.outcome == "refuse"                                  # classified, no raw throw
    r = _col(fr).refusal
    assert (r.kind, r.reason, r.discriminator) == ("refuse", "blocked_reduction", "unsupported")
    assert not r.is_error                                          # an analytical verdict, not the backstop
    assert "calendar" in r.detail                                  # names the lineage it may not cross


# ── §2c single-universe sugar: ON optional with one universe; required with more ──────────────────
_ONE_UNI = """
MANIFOLD s VERSION 1
UNIVERSE sales = store
LEVEL store = store_id BASE
MEASURE revenue FROM tx AS sum(amount)
"""


def test_single_universe_sugar_fills_the_sole_universe():
    # ASSERT was the sugar's second customer until 0.13.0 (ruling 2026-07-26); MEASURE is now its only one.
    m = parse_manifold(_ONE_UNI)
    assert m.measures["revenue"].universe == "sales"


def test_on_universe_required_with_more_than_one():
    two = _ONE_UNI.replace("UNIVERSE sales = store\n", "UNIVERSE sales = store\nUNIVERSE ops = store\n")
    with pytest.raises(ParseError) as ei:
        parse_manifold(two)
    assert "'ON <universe>' is required" in str(ei.value) and "MEASURE revenue" in str(ei.value)

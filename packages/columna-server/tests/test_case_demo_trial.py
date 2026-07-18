"""
test_case_demo_trial.py — Cascadia case-demo increment 2: the full Manifold, live.

The Cascadia Manifold (demo/cascadia) is authored to chapter 2's spec and adjudicated against the
bundled warehouse. This pins THE TRIAL — the chapter-3 verdict table — against reality, and confirms
the four moods reproduce chapter 3's question section (serve · disclose · clarify).

Flags where reality bends chapter 3 (brought to the desk, not silently absorbed):
  • product ↔ category (M:N) — chapter 3 lists it 'corroborated', but a RELATE is RECORDED, not
    adjudicated: it carries no standalone verdict today (the fan-out refusal still fires — the
    relationship is load-bearing, just unverified).
  • inventory carve `day >= store.opened` — chapter 3 lists it 'corroborated', but a universe
    CONFINEMENT predicate is not an adjudicated claim: no standalone verdict (the raw data does
    respect it — 0 snapshots predate their store — so the carve removes nothing here).
  • chapter 3's seeded query numbers (e.g. '16 rows, 4×4') assume ONE year; the warehouse carries
    TWO (2024-2025), so the real shapes differ (32 rows, 4×8). The seeded exemplars are the desk's
    to ratify (increment 3), so this test asserts SHAPE/MOOD, never a seeded number.
"""
import os

import pytest

import columna_server
from columna_server.store import _load_one
from columna_server import tools as T

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


@pytest.fixture(scope="module")
def live():
    lm = _load_one("cascadia", _CASCADIA)   # parse + well-formed + connect + adjudicate
    lm.server.publish()                     # run the trials + build witnesses
    return lm


class _Store:
    """A one-manifold store, so the four-mood WIRE (tools.query) can be exercised."""
    def __init__(self, lm):
        self._lm = lm
    def get(self, mid):
        if mid != self._lm.manifold_id:
            raise KeyError(mid)
        return self._lm


# ── THE TRIAL (chapter-3 verdict table) — the adjudicated claims ─────────────────────────────────────
def test_location_hierarchy_is_corroborated(live):
    h = next(h for h in live.manifold.hierarchies if h.lineage == "location")
    assert h.license.verdict == "corroborated"          # ch3: 24/24 stores, one region each


def test_calendar_hierarchy_is_corroborated_over_every_hop_and_the_week_branch(live):
    h = next(h for h in live.manifold.hierarchies if h.lineage == "calendar")
    assert h.license.verdict == "corroborated"          # ch3: 731/731 days, the chain AND the day->week branch
    # the branching structure is on the record: the chain plus the week branch
    assert ("day", "cal.month", "cal.quarter", "cal.year") in h.paths
    assert ("day", "cal.week") in h.paths


def test_returns_bounded_row_assert_is_corroborated(live):
    a = next(a for a in live.manifold.asserts if a.name == "returns_bounded")
    assert a.license.verdict == "corroborated"          # ch3: holds on every tracked row (nulls = no return)


def test_both_bases_are_untestable_on_the_record(live):
    us = {u.name: u for u in live.manifold.universes.values()}
    assert us["transaction"].basis_license.verdict == "untestable"   # ch3: the author's call, recorded
    assert us["inventory"].basis_license.verdict == "untestable"


def test_inventory_carve_is_a_definition_not_a_tried_claim(live):
    # ch3 v0.4: the opened-date carve LEFT the trial table — a definition confines, a claim gets tried;
    # nothing outside the population exists to test. For the record the raw feed respects it anyway —
    # proven by serving stock.last and getting a clean, non-empty position.
    r = live.server.frame("store").column("stock", "stock.last").run()
    assert r.data.height > 0 and r.columns[0].refusal is None


# ── THE FOUR MOODS (chapter-3 question section) — shape/mood, never a seeded number ──────────────────
def test_serve_revenue_and_orders_by_region_and_quarter(live):
    r = live.server.frame("region", "cal.quarter").column("rev", "revenue.sum").column("ord", "orders").run()
    assert r.data.height > 0 and not r.disclosure.caveats and r.columns[0].refusal is None


def test_stock_sum_over_time_serves_with_a_critical_blocked_caveat(live):
    # the first burn, retried: stock.sum across the blocked calendar SERVES but wears a critical caveat.
    r = live.server.frame("store", "cal.month").column("stock", "stock.sum").run()
    crossing = [c for c in r.disclosure.caveats if c.category == "b_anchor_crossing"]
    assert crossing and crossing[0].severity == "critical"
    assert "calendar" in crossing[0].detail


def test_revenue_by_category_clarifies_naming_the_many_to_many(live):
    # ch3 v0.4: the question that comes back with its reason attached is a CLARIFY (not a refuse) —
    # the M:N fan-out is underdetermined; the WIRE mood is clarify, and the edge is named.
    res = T.query(_Store(live), "cascadia", "SELECT revenue AT {category}")
    assert res["outcome"] == "clarify"
    # the engine object underneath is the non_functional_transport refusal the planner classifies to clarify
    ref = live.server.frame("category").column("rev", "revenue.sum").run().columns[0].refusal
    assert ref is not None and ref.reason == "non_functional_transport" and "category" in ref.detail

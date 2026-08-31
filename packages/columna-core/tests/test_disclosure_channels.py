"""
test_disclosure_channels.py — STANDING RULES for the semantic/mechanical split (OF-24 ruling (a)).

These state obligations, not implementations:

  1. Warm execution is never quieter than fresh — the SEMANTIC channel is call-invariant.
  2. Mechanical facts ("served from cache") live on their own channel and never reach the mood.
  3. A support shortfall that changes the denominator is MATERIAL, on every face that can have one.

WHY. OF-24 found the defect by its consequence: on a fresh store the FIRST asker received LESS
disclosure than the second, for the same question on the same data. The content was true and the
values identical; a mechanical fact was wearing a semantic name on the semantic channel. Separately
(P1-04) the TOUCH path returned from its cache BEFORE coverage and the fill dispositions were
computed, so a warm answer dropped real semantic facts including a MATERIAL one — and (P1-05) the
coverage shortfall itself was graded IMMATERIAL, on a wire code whose MATERIAL slot existed, was
wired, and had no producer.

P1-04 and P1-05 had to land together: re-grading coverage to MATERIAL while warm still dropped it
would have made the divergence OUTCOME-visible (`disclose` cold, `serve` warm), which is strictly
worse than the quiet version.
"""
import duckdb

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.disclosure import Caveat, Disclosure, FRESHNESS, COVERAGE
from columna_core.disclosure_wire import CATEGORY_TABLE, MATERIAL, wire_frame
from columna_core.parser import parse_manifold

# A touch face with a REAL coverage shortfall: p9 carries revenue and is in no category.
MANIFOLD = """
MANIFOLD shortfall VERSION 1
UNIVERSE sales = product BASIS events
LEVEL product = product_id BASE
LEVEL category = category_id
RELATE product <-> category VIA memberships(product_id, category_id)
    FACES { touch = TOUCH -- "revenue reaches every category a product sits in" }
MEASURE revenue ON sales FROM sales_lines AS sum(amount) FILL unknown
"""


def _server():
    con = duckdb.connect()
    con.execute("""CREATE TABLE sales_lines AS SELECT * FROM (VALUES
        ('p1', 10.0), ('p2', 20.0), ('p3', 30.0), ('p9', 999.0))
        AS t(product_id, amount)""")
    con.execute("""CREATE TABLE memberships AS SELECT * FROM (VALUES
        ('p1','c1'), ('p2','c1'), ('p3','c2'))
        AS t(product_id, category_id)""")
    srv = ManifoldServer(parse_manifold(MANIFOLD), DuckDBConnector(con))
    srv.publish()
    return srv


def _ask(srv):
    return srv.planner.run(("category.touch",), [("revenue", "revenue")], None)


def _semantic(fr):
    """(category, detail) for every semantic caveat, frame and column."""
    out = {(c.category, c.detail) for c in fr.disclosure.caveats}
    for col in fr.columns:
        if col.refusal is None:
            out |= {(c.category, c.detail) for c in col.disclosure.caveats}
    return out


# ── 1. the semantic channel is call-invariant ─────────────────────────────────────────────────

def test_warm_is_never_quieter_than_fresh():
    """THE RULE. Identical request, identical data — the semantic disclosure set must be equal, not
    merely a superset or 'close enough'. Asserted as set equality in BOTH directions so a future
    change that ADDS a caveat only on the warm path fails too."""
    srv = _server()
    cold = _semantic(_ask(srv))
    warm = _semantic(_ask(srv))
    assert srv.engine.stats.cache_hits >= 1, "the second ask did not hit the cache; test is vacuous"
    assert cold == warm


def test_warm_and_fresh_agree_on_the_served_mood():
    srv = _server()
    a = wire_frame(_ask(srv))
    b = wire_frame(_ask(srv))
    assert a["outcome"] == b["outcome"]
    assert a["frame"]["rollup_severity"] == b["frame"]["rollup_severity"]


def test_the_cache_is_actually_exercised():
    """Fixture guard. If the cache stopped being hit, every parity test above would pass vacuously."""
    srv = _server()
    _ask(srv)
    before = srv.engine.stats.cache_hits
    _ask(srv)
    assert srv.engine.stats.cache_hits == before + 1


# ── 2. mechanical facts are on their own channel ──────────────────────────────────────────────

def test_served_from_cache_is_mechanical_not_semantic():
    """OF-24 (a). The annotation is truthful; it is not a claim about what the number means."""
    srv = _server()
    _ask(srv)
    warm = _ask(srv)
    assert not any(c.category == FRESHNESS for c in warm.disclosure.caveats), \
        "a mechanical fact is on the semantic channel"
    mech = {c.category for c in warm.disclosure.mechanical}
    for col in warm.columns:
        mech |= {c.category for c in col.disclosure.mechanical}
    assert FRESHNESS in mech


def test_the_mechanical_channel_cannot_change_the_mood():
    """Structural, not incidental: severity and materiality read `caveats` only."""
    d = Disclosure.clean()
    assert d.severity == "none" and d.is_clean
    loud = d.with_mechanical(Caveat(FRESHNESS, "served from cache", severity="critical"))
    assert loud.severity == "none", "a mechanical caveat moved the severity rollup"
    assert loud.is_clean, "a mechanical caveat made a clean disclosure unclean"
    assert loud.mechanical and not loud.caveats


def test_the_wire_carries_both_channels_always():
    """Emitted even when empty, so a consumer never distinguishes 'nothing to say' from 'old wire'."""
    srv = _server()
    w = wire_frame(_ask(srv))
    assert "mechanical" in w["frame"]
    for col in w["columns"]:
        assert "mechanical" in col


# ── 3. a shortfall is material, on every face that can have one ────────────────────────────────

def test_coverage_is_wired_material():
    assert CATEGORY_TABLE[COVERAGE] == ("denominator_population", MATERIAL)


def test_a_touch_shortfall_is_material():
    """It was TRANSPORT -> `provenance` -> IMMATERIAL, which could not trip `disclose` on its own,
    while the correct MATERIAL slot sat wired with no producer."""
    srv = _server()
    w = wire_frame(_ask(srv))
    cov = [d for col in w["columns"] for d in col["disclosures"]
           if d["code"] == "denominator_population"]
    assert cov, "the coverage shortfall did not reach the wire as denominator_population"
    assert all(d["materiality"] == MATERIAL for d in cov)


def test_a_shortfall_alone_is_enough_to_disclose():
    """The consequence that makes the grading matter: on its own, without any co-caveat, a shortfall
    must move the frame off `serve`. Previously it could not."""
    from columna_core.disclosure_wire import derive_outcome
    srv = _server()
    fr = _ask(srv)
    only_cov = tuple(c for c in fr.columns[0].disclosure.caveats if c.category == COVERAGE)
    assert only_cov, "fixture has no coverage caveat; test would be vacuous"
    stripped = Disclosure(only_cov, fr.columns[0].disclosure.population)
    material = any(CATEGORY_TABLE[c.category][1] == MATERIAL for c in stripped.caveats)
    assert material
    assert derive_outcome(fr, material) != "serve"

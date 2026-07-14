"""
test_derivation.py — must-exist-first derivation pins (audit v0.2 §D item 1; B4).

These lock in what the v0.2 review established empirically, BEFORE anything touches
`model.DerivedColumn` or the planner's derivation-expansion path (reserved for WP-B):

  (a) A NAMED derived expression inherits the full static hazard pipeline of the equivalent
      inline expression — D5 co-anchoring AND B-anchor crossings — because the planner recursively
      expands the derived name into its formula before the checks run (planner.py:339-340; `_atoms`
      expands for the crossing scan). v0.1's "named ratios bypass hazard detection" claim was
      DISPROVEN empirically; these pins exist so that property survives the coming WP-B changes.
  (b) A characterization test, red-flagged DOCTRINE-DIVERGENT: a same-universe derived ratio at a
      coarse anchor currently SERVES the pooled (output-anchor) reading with zero resolution-time
      disclosure. Pinned deliberately (NOT xfail) so it FAILS LOUDLY the moment S1a / WP-B changes
      behavior, forcing a deliberate update.
  (c) The new B4 parser finding: a `DERIVED` formula referencing a dotted family member is rejected
      at parse, though the identical `DerivedColumn` built in Python plans fine. xfail(strict) until
      T2 scopes the token check to dotted-head names.

Fixtures (`hand_manifold`, `fixture_connector`, `fixture_server`) come from tests/conftest.py.
"""
import os

import pytest

from columna_core import DerivedColumn, ManifoldServer
from columna_core.disclosure_wire import wire_frame
from columna_core.parser import parse_manifold

_HERE = os.path.dirname(os.path.abspath(__file__))
_BENCHMARK_CML = os.path.join(_HERE, "fixtures", "benchmark.cml")


def _classification(fr) -> dict:
    """Outcome + the first column's no-result classification — the byte-for-byte hazard verdict,
    independent of the column's display name or cache order."""
    w = wire_frame(fr)
    cols = w.get("columns", [])
    nr = (cols[0].get("no_result") or {}) if cols else {}
    alts = sorted((a.get("apply") or {}).get("universe")
                  for c in cols for a in (c.get("no_result") or {}).get("alternatives", [])
                  if (a.get("apply") or {}).get("universe"))
    return {"outcome": w["outcome"], "reason": nr.get("reason"),
            "discriminator": nr.get("discriminator"), "alternatives": alts}


def _codes(fr) -> list:
    w = wire_frame(fr)
    return sorted(d.get("code") for c in w.get("columns", []) for d in (c.get("disclosures") or []))


@pytest.fixture
def derived_server(hand_manifold, fixture_connector):
    """The benchmark server with two NAMED derived columns added in Python (the definition parser
    cannot yet express the dotted one — see T1c): a cross-universe ratio and a blocked-lineage
    rollup, the two hazard shapes."""
    m = hand_manifold
    m.derived = dict(m.derived)
    m.derived["sell_through"] = DerivedColumn("sell_through", "revenue / level.last")
    m.derived["lvlsum"] = DerivedColumn("lvlsum", "level.sum")
    return ManifoldServer(m, fixture_connector)


# --- (a) hazard inheritance: named == inline ------------------------------------------------
def test_named_ratio_inherits_coanchor_clarify(derived_server):
    """D5 co-anchoring: a named cross-universe derived ratio clarifies byte-for-byte identically to
    the inline expression (recursive expansion before the BinOp/D5 check)."""
    named = derived_server.frame("store").column("r", "sell_through").run()
    inline = derived_server.frame("store").column("r", "revenue / level.last").run()
    assert _classification(named) == _classification(inline)
    assert _classification(named) == {
        "outcome": "clarify", "reason": "co_anchor_ambiguous",
        "discriminator": "ambiguous", "alternatives": ["store_days", "transactions"],
    }


def test_named_derived_inherits_b_anchor_crossing(derived_server):
    """B-anchor crossing scan (`_atoms` expands the formula): a named derived over a blocked-lineage
    rollup carries the same critical `blocked_reduction` disclosure as the inline expression. (The
    served value may also pick up an immaterial `freshness` caveat depending on cache order —
    orthogonal to the crossing; we pin the crossing itself, not the full disclosure set.)"""
    named = _codes(derived_server.frame("store").column("x", "lvlsum").run())
    inline = _codes(derived_server.frame("store").column("x", "level.sum").run())
    assert "blocked_reduction" in inline
    assert "blocked_reduction" in named


# --- (b) characterization of the unimplemented trichotomy -----------------------------------
def test_aov_at_month_serves_pooled_undisclosed(fixture_server):
    # DOCTRINE-DIVERGENT (audit Fork 3): a same-universe derived ratio at a COARSE anchor currently
    # SERVES the pooled (output-anchor) reading with ZERO resolution-time disclosure. The "mean of
    # daily rates" reading is inexpressible, and the pooled reading is taken silently rather than
    # disclosed or asked back. This pins the CURRENT (divergent) behavior ON PURPOSE — it is NOT
    # xfail — so it FAILS LOUDLY the moment S1a (interim disclose caveat) or WP-B (the trichotomy)
    # lands, forcing a deliberate update instead of a silent drift. See audit B4 (§ "what genuinely
    # is missing") and Fork 3(a).
    fr = fixture_server.frame("cal.month").column("aov", "aov").run()
    w = wire_frame(fr)
    assert w["outcome"] == "serve", "aov @ cal.month no longer serves — the trichotomy may have landed; update this pin deliberately (audit Fork 3)."
    ndisc = (sum(len(c.get("disclosures") or []) for c in w.get("columns", []))
             + len(w.get("frame", {}).get("disclosures") or []))
    assert ndisc == 0, "aov @ cal.month gained a disclosure — S1a/WP-B may have landed; update this pin deliberately (audit Fork 3)."


# --- (c) the B4 parser finding — un-xfailed by T2 (dotted-head token check) ------------------
def test_derived_dotted_member_reference_parses():
    """After T2 scoped the well-formedness check to dotted-head names, an authored `DERIVED` over a
    multi-member family reference parses (was rejected: "references unknown column 'last'")."""
    with open(_BENCHMARK_CML) as f:
        cml = f.read() + "\nDERIVED sell_through = revenue / level.last\n"
    m = parse_manifold(cml)
    assert "sell_through" in m.derived
    assert m.derived["sell_through"].formula == "revenue / level.last"


def test_parsed_derived_over_family_plans_like_python_built(fixture_connector):
    """T2 positive test: the object model already supported a dotted family-member reference in a
    derived formula; now the DEFINITION LANGUAGE can too — and the parsed manifold's derived ratio
    resolves identically to the Python-built one (same clarify classification), closing the gap the
    B4 finding named."""
    with open(_BENCHMARK_CML) as f:
        cml = f.read() + "\nDERIVED sell_through = revenue / level.last\n"
    m = parse_manifold(cml)
    srv = ManifoldServer(m, fixture_connector)
    got = _classification(srv.frame("store").column("r", "sell_through").run())
    assert got == {"outcome": "clarify", "reason": "co_anchor_ambiguous",
                   "discriminator": "ambiguous", "alternatives": ["store_days", "transactions"]}

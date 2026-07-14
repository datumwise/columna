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
from columna_core.parser import parse_manifold, ParseError

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
    # DOCTRINE-CORRECT (Fork 3 RE-RULED 2026-07-14; S1a withdrawn): a same-universe derived ratio at
    # a COARSE anchor SERVES the pooled (output-anchor) reading CLEAN — no resolution-time disclosure
    # — and that is the intended behavior. Governing law: the mood follows where the resolution
    # decision lives. For `aov` (= revenue/orders, a formula), "averaged over what" is settled at
    # DECLARATION (the formula is inspectable in the Explorer), and the pooled-vs-mean-of-daily choice
    # lives in TRANSLATION (between the sentence and any expression), not at the gate — so the engine
    # receives a definite computation and serves it. The interim weighting_grain caveat (S1a) is
    # WITHDRAWN. A disclosure appearing HERE would be the regression this pins against; the end-state
    # clarify (WP-B, once the alternative reading is expressible) is a separate, named change.
    fr = fixture_server.frame("cal.month").column("aov", "aov").run()
    w = wire_frame(fr)
    assert w["outcome"] == "serve", "aov @ cal.month no longer serves clean — Fork 3 re-ruled serve-clean as correct; investigate."
    ndisc = (sum(len(c.get("disclosures") or []) for c in w.get("columns", []))
             + len(w.get("frame", {}).get("disclosures") or []))
    assert ndisc == 0, "aov @ cal.month gained a disclosure — Fork 3 re-ruled serve-clean as correct, so a caveat here is a regression, not S1a."


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


def test_parsed_derived_unknown_family_member_errors_classified(fixture_connector):
    """T2 carries its own guarantee (rider): T2 widens what the DEFINITION PARSER admits, so an
    UNKNOWN family member (`level.lasst`) now reaches the PLANNER instead of being caught at parse.
    The planner classifies it — `error` / `unknown`, detail naming the bad operator and the registry
    — never a silent number and never a crash. So the widening does not open a hole."""
    with open(_BENCHMARK_CML) as f:
        cml = f.read() + "\nDERIVED bad = revenue / level.lasst\n"
    m = parse_manifold(cml)   # parses now: head 'level' is known; member validity is the planner's job
    srv = ManifoldServer(m, fixture_connector)
    w = wire_frame(srv.frame("store").column("b", "bad").run())
    assert w["outcome"] == "error"
    nr = (w["columns"][0].get("no_result") or {})
    assert nr.get("reason") == "unknown"
    detail = nr.get("detail") or ""
    assert "lasst" in detail and "registry" in detail


# =====================================================================================
# B-2 — the fertility grammar (FERTILE {..} + AT <level>). The parser RECORDS declarations
# (declared_lineages, resolution_anchor) and constructs NO License; the adjudicator (B-3) is
# the sole authority that mints a verdict. Fail-closed: a FERTILE/BLOCKED lineage or an AT
# level that no declaration carries is a well-formedness error.
# =====================================================================================
def _parse(extra: str):
    with open(_BENCHMARK_CML) as f:
        return parse_manifold(f.read() + "\n" + extra + "\n")


def test_fertility_grammar_composes_with_dotted_head_and_at():
    """The T2 dotted-head fix and the new grammar must compose: a formula with a dotted family ref,
    an `AT <level>` resolution anchor, and a FAMILY block, all on one declaration."""
    m = _parse("DERIVED x = revenue / level.last AT day FAMILY { mean FERTILE { } }")
    d = m.derived["x"]
    assert d.formula == "revenue / level.last"           # everything up to the top-level AT
    assert d.resolution_anchor == "day"                  # AT rides the formula line, stripped off
    assert set(d.family) == {"mean"}                     # the member is declared...
    assert d.family["mean"].declared_lineages == frozenset()   # ...with no travel (empty FERTILE)
    assert d.family["mean"].license is None              # parser never mints a License


def test_fertile_records_declared_lineages_no_license():
    """A non-empty FERTILE {..} records exactly those lineages as declared; still no License."""
    m = _parse("DERIVED net = revenue - orders FAMILY { sum FERTILE { calendar store_geo } }")
    fm = m.derived["net"].family["sum"]
    assert fm.declared_lineages == frozenset({"calendar", "store_geo"})
    assert fm.license is None


def test_no_family_block_is_denotation_only():
    """No FAMILY block ⇒ denotation-only: an empty family, no implied member, no travel."""
    m = _parse("DERIVED plain = revenue - orders")
    assert m.derived["plain"].family == {}
    assert m.derived["plain"].resolution_anchor is None


def test_freshly_parsed_manifold_has_no_license_anywhere():
    """The authority chain, negative pin (B-2 adjustment #1): parsing constructs NO License objects
    anywhere — on derived members OR measure members. Only the adjudicator mints verdicts."""
    m = _parse("DERIVED net = revenue - orders AT day\n"
               "    FAMILY {\n        sum FERTILE { calendar }\n        mean FERTILE { }\n    }")
    licenses = [fm.license
                for holder in (list(m.derived.values()) + list(m.measures.values()))
                for fm in holder.family.values()]
    assert licenses and all(lic is None for lic in licenses)


def test_fertile_lineage_fail_closed():
    """A FERTILE lineage no declared edge carries is a well-formedness error (opening a door that
    doesn't exist)."""
    with pytest.raises(ParseError) as ei:
        _parse("DERIVED bad = revenue - orders FAMILY { sum FERTILE { nonesuch } }")
    assert "nonesuch" in str(ei.value) and "FERTILE" in str(ei.value)


def test_at_level_fail_closed():
    """An `AT <level>` naming an undeclared level is a well-formedness error (reachability from the
    components' universes is the adjudicator's job; existence is the parser's)."""
    with pytest.raises(ParseError) as ei:
        _parse("DERIVED bad = revenue / orders AT no_such_level FAMILY { mean FERTILE { } }")
    assert "no_such_level" in str(ei.value)


def test_blocked_lineage_fail_closed_aligned():
    """B-2 adjustment #3, alignment: the measure BLOCKED validation was previously absent; it now
    fails closed on the same rule as FERTILE (a BLOCKED lineage no edge carries is an error)."""
    with pytest.raises(ParseError) as ei:
        _parse("MEASURE bogus ON transactions FROM transactions AS sum(amount)\n"
               "    FAMILY {\n        sum BLOCKED { nonesuch }\n    }")
    assert "nonesuch" in str(ei.value) and "BLOCKED" in str(ei.value)

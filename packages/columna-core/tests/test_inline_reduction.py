"""
test_inline_reduction.py — WP-B.1: inline reduction of a derivation (capture v0.8; ruling (A)).

Closes doctrine-gap DG-1. Two forms of `R(inner)` in a column expression:

  * PINNED   `avg(aov@day) @ month` — the input anchor is pinned; a definite quantity, served with an
              IMMATERIAL communicative disclosure naming the reading. Identical to the DECLARED
              AT-metric (`daily_aov`) — same reading, two spellings; never the pooled value.
  * UNPINNED `avg(aov) @ month`     — the input anchor is structurally underdetermined ⇒ an engine
              clarify enumerating candidate input anchors, choosing none.

input_anchor-fit finding (owed to CP-B2, pinned here): an EXPLICITLY user-pinned input anchor is a
deliberate, visible choice, so it owes a communicative note (immaterial `provenance`), NOT the
material `input_anchor` caveat. Fork surfaced to Huayin (reason-code reuse; caveat materiality).

Fixtures (`fixture_connector`) come from tests/conftest.py.
"""
import os

import pytest

from columna_core import ManifoldServer
from columna_core.adjudication import adjudicate
from columna_core.disclosure_wire import wire_frame
from columna_core.parser import parse_manifold

_HERE = os.path.dirname(os.path.abspath(__file__))
_BENCHMARK_CML = os.path.join(_HERE, "fixtures", "benchmark.cml")

_DEFS = ("DERIVED aov = revenue / orders\n"
         "DERIVED daily_aov = revenue / orders AT day\n"
         "    FAMILY {\n        mean FERTILE { }\n    }\n")


def _srv(fixture_connector, certify=True):
    """P0.5a closed-by-default: travel over an FD-claimed edge (day -> cal.month) serves only once the
    governing hierarchy is CORROBORATED on the attested data. These tests are about inline-reduction
    semantics, so the helper certifies first (`adjudicate` = the publish gate)."""
    with open(_BENCHMARK_CML) as f:
        srv = ManifoldServer(parse_manifold(f.read() + "\n" + _DEFS), fixture_connector)
    if certify:
        adjudicate(srv)
    return srv


def _vals(srv, anchor, expr):
    return srv.frame(anchor).column("c", expr).run().data.sort(anchor)["c"].to_list()


# ── PINNED: legal, definite, communicative-disclosed ────────────────────────────────────────
def test_pinned_inline_reduction_serves_with_immaterial_note(fixture_connector):
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("cal.month").column("x", "avg(aov@day)").run())
    assert w["outcome"] == "serve"
    discs = w["columns"][0].get("disclosures") or []
    assert [(d["code"], d["materiality"]) for d in discs] == [("provenance", "immaterial")], \
        "a user-pinned input anchor owes a communicative note (immaterial provenance), not a material caveat"


def test_pinned_inline_equals_declared_at_metric(fixture_connector):
    """The inline pinned reduction is the SAME reading as the declared AT-metric — two spellings of
    'mean of the day-resolved series'."""
    s = _srv(fixture_connector)
    inline = _vals(s, "cal.month", "avg(aov@day)")
    declared = _vals(s, "cal.month", "daily_aov")
    assert inline == pytest.approx(declared)


def test_pinned_inline_is_never_the_pooled_value(fixture_connector):
    """never-substitute: the pinned reading ≠ the pooled `aov@month`."""
    s = _srv(fixture_connector)
    assert _vals(s, "cal.month", "avg(aov@day)") != pytest.approx(_vals(s, "cal.month", "aov"))


def test_pinned_at_its_own_anchor_is_the_denotation(fixture_connector):
    """`avg(aov@day) @ day` — asked AT the pinned anchor, no travel: the day denotation itself."""
    s = _srv(fixture_connector)
    assert _vals(s, "day", "avg(aov@day)") == pytest.approx(_vals(s, "day", "aov"))


def test_avg_is_mean_alias(fixture_connector):
    s = _srv(fixture_connector)
    assert _vals(s, "cal.month", "avg(aov@day)") == pytest.approx(_vals(s, "cal.month", "mean(aov@day)"))


@pytest.mark.parametrize("reducer", ["sum", "min", "max", "mean"])
def test_pinned_reducers_serve(fixture_connector, reducer):
    """Each inline reducer resolves the pinned series and collapses it to the frame anchor."""
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("cal.month").column("c", f"{reducer}(aov@day)").run())
    assert w["outcome"] == "serve"


# ── UNPINNED: engine clarify enumerating candidate input anchors ────────────────────────────
def test_unpinned_inline_reduction_clarifies(fixture_connector):
    s = _srv(fixture_connector)
    fr = s.frame("cal.month").column("y", "avg(aov)").run()
    w = wire_frame(fr)
    assert w["outcome"] == "clarify"
    nr = w["columns"][0].get("no_result") or {}
    # OF-1 ruling: its own reason `input_anchor_ambiguous` (one reason per contested dimension),
    # NOT a reuse of `ambiguous_grain`.
    assert nr.get("reason") == "input_anchor_ambiguous" and nr.get("discriminator") == "ambiguous"
    # candidate input anchors are enumerated (only `day` rolls up to cal.month in this fixture),
    # and the clarify chooses none.
    alts = nr.get("alternatives") or []
    assert alts, "unpinned reduction must enumerate candidate input anchors"
    assert any("day" in (a.get("description") or "") for a in alts)


def test_unpinned_names_a_pinnable_fix(fixture_connector):
    """The clarify's detail points the user at the pin that resolves it."""
    s = _srv(fixture_connector)
    fr = s.frame("cal.month").column("y", "mean(aov)").run()
    detail = (wire_frame(fr)["columns"][0].get("no_result") or {}).get("detail") or ""
    assert "@day" in detail and "does not pin" in detail


# ── OF-1: the minted reason lives in the closed vocabulary, distinct from ambiguous_grain ───
def test_input_anchor_ambiguous_is_a_distinct_clarify_reason():
    """OF-1 ruling: `input_anchor_ambiguous` is its OWN reason (CLARIFY/AMBIGUOUS), sibling to
    `co_anchor_ambiguous` — not a reuse of `ambiguous_grain`, whose gloss stays single-meaning."""
    from columna_core.disclosure import REASON_OUTCOME, CLARIFY, AMBIGUOUS
    assert REASON_OUTCOME["input_anchor_ambiguous"] == (CLARIFY, AMBIGUOUS)
    assert "input_anchor_ambiguous" != "ambiguous_grain"          # one reason per contested dimension


# ── boundary: multi-arg / bad pin refuse cleanly, never a silent number ─────────────────────
def test_bad_input_anchor_pin_refuses(fixture_connector):
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("cal.month").column("z", "avg(aov@nonesuch)").run())
    assert w["outcome"] in ("refuse", "error")


# ════════════════════════════════════════════════════════════════════════════════════════════
# WP-GRAIN-1 — the COMPOSITE input anchor (doctrine ratified Huayin 2026-07-29; 0.13.4).
#
# `R(inner @ {a*b*c})` pins a PRODUCT grain, not a single level. The engine's
# `reduce_series_to_anchor` is already composite-grain-native; the planner lifts the single-level
# restriction and adds the pin × output-anchor lattice's laws. Reason codes minted: Law 1 REFUSE
# `pin_coarser_than_output` (its own dimension per OF-1), Law 2 CLARIFY `redundant_pin`.
# ════════════════════════════════════════════════════════════════════════════════════════════
from columna_core.envelope import parse_statement                       # noqa: E402


def _stmt(s, q):
    """The real ask surface: parse → desugar/plan → wire (composite pins carry `{a*b}` braces, which
    only the statement path converts; the low-level `.column()` API expects pre-converted syntax)."""
    return wire_frame(s.planner.run_statement(parse_statement(q)))


def _note(wire, col=0):
    discs = wire["columns"][col].get("disclosures") or []
    return [(d.get("code"), d.get("materiality"), d.get("detail")) for d in discs]


def _no_result(wire, col=0):
    c = wire["columns"][col]
    return c.get("no_result") or wire.get("error") or {}


# ── Law 1 (REFUSE `pin_coarser_than_output`): a pin coarser than the output cannot resolve ──
def test_law1_pin_coarser_than_output_refuses(fixture_connector):
    """`avg(revenue @ {cal.month}) AT {store*day}` — the output asks at `day`, but the pin fixes
    `cal.month`, which `day` reaches (day -> cal.month): a coarser pin cannot serve a finer output."""
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(revenue @ {cal.month}) AT {store*day}")
    assert w["outcome"] == "refuse"
    nr = _no_result(w)
    assert nr.get("reason") == "pin_coarser_than_output"
    assert "COARSER" in nr.get("detail", "") and "cal.month" in nr["detail"] and "day" in nr["detail"]
    alts = [a.get("description") for a in (nr.get("alternatives") or [])]
    assert len(alts) == 2                                   # replace the pin, or drop it


def test_law1_is_its_own_dimension_per_of1():
    """OF-1 (one reason per contested dimension): Law 1 mints its OWN reason, REFUSE family, distinct
    from `out_of_universe` (which owns the run-time-unreachability dimension)."""
    from columna_core.disclosure import REASON_OUTCOME, REFUSE, UNSUPPORTED
    assert REASON_OUTCOME["pin_coarser_than_output"] == (REFUSE, UNSUPPORTED)
    assert "pin_coarser_than_output" != "out_of_universe"


# ── Law 2 (CLARIFY `redundant_pin`): two cross-comparable pin levels fix one axis, not two ──
def test_law2_redundant_pin_clarifies(fixture_connector):
    """`avg(revenue @ {day*cal.month}) AT {cal.month}` — `day` determines `cal.month`, so the pair
    fixes one axis; a CLARIFY offering the two admissible pins, never a refuse."""
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(revenue @ {day*cal.month}) AT {cal.month}")
    assert w["outcome"] == "clarify"
    nr = _no_result(w)
    assert nr.get("reason") == "redundant_pin"
    alts = [a.get("description") for a in (nr.get("alternatives") or [])]
    assert any("{day}" in a for a in alts) and any("{cal.month}" in a for a in alts)


def test_law2_is_a_clarify_sibling_of_ambiguous_grain():
    from columna_core.disclosure import REASON_OUTCOME, CLARIFY, AMBIGUOUS
    assert REASON_OUTCOME["redundant_pin"] == (CLARIFY, AMBIGUOUS)


# ── Law 4 rendering: the two-stage-statistic disclosure, generalized to the composite pin ──
def test_composite_pin_serves_with_rider_when_pin_axis_is_in_output(fixture_connector):
    """`avg(revenue @ {store*product*cal.month}) AT {cal.month}` — a pin axis (`cal.month`) is the
    output's own; the immaterial note names it as the fixed axis and the rest as reduced-over."""
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}")
    assert w["outcome"] == "serve"                          # immaterial note ⇒ serve (Law 4: "serve with TRANSPORT, always")
    (code, mat, detail), = _note(w)
    assert (code, mat) == ("provenance", "immaterial")
    assert detail == ("'mean of revenue@{store*product*cal.month}' reduced to cal.month — "
                      "pin fixes cal.month, reduces over store, product")


def test_composite_pin_serves_with_standard_note_when_no_pin_axis_in_output(fixture_connector):
    """A composite pin whose levels are all orthogonal to / finer than the output renders the
    generalized STANDARD note (the pin as a braced product), not the rider."""
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(revenue @ {store*product}) AT {cal.month}")
    assert w["outcome"] == "serve"
    (code, mat, detail), = _note(w)
    assert (code, mat) == ("provenance", "immaterial")
    assert detail == ("'mean of revenue@{store*product}' reduced to cal.month — the mean of "
                      "revenue@{store*product} reading (input anchor pinned to '{store*product}'), "
                      "not the pooled value at cal.month")


# ── byte-regression: the single-level path is the composite grammar at n=1, unchanged ──
def test_single_level_note_is_byte_identical(fixture_connector):
    """Criterion 6: no regression on the single-level path. The rendered note for `avg(aov@day)` is
    byte-for-byte what it was before WP-GRAIN-1 (bare `@day`, `pinned to 'day'`, no rider)."""
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(aov @ {day}) AT {cal.month}")
    (code, mat, detail), = _note(w)
    assert (code, mat) == ("provenance", "immaterial")
    assert detail == ("'mean of aov@day' reduced to cal.month — the mean of aov@day reading "
                      "(input anchor pinned to 'day'), not the pooled value at cal.month")


def test_single_level_pin_equal_output_is_still_standard_form(fixture_connector):
    """`avg(aov@day) AT {day}` — a single-level pin equal to the output keeps the STANDARD note (the
    rider is composite-only), so this case is byte-identical to the pre-WP-GRAIN-1 form."""
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(aov @ {day}) AT {day}")
    (code, mat, detail), = _note(w)
    assert detail == ("'mean of aov@day' reduced to day — the mean of aov@day reading "
                      "(input anchor pinned to 'day'), not the pooled value at day")


# ── wire contract: WP-GRAIN-1 added reason codes WITHOUT a bump; WP-NAME-1 (0.14.0) bumped to "2" ──
def test_wire_contract_version_is_current(fixture_connector):
    # WP-GRAIN-1 added `pin_coarser_than_output`/`redundant_pin` inside the existing vocabulary — no bump
    # (readers on the contract route by outcome). WP-NAME-1 changed the default column KEY for the same
    # utterance (canonical expression identity) -> contract "2". S2.2b-2 changed list_manifolds catalog
    # semantics (per-lineage, not per-folder) -> contract "3"; the bump is global, so this frame wire
    # reports "3" too though no analytical behavior changed here.
    from columna_core.disclosure_wire import CONTRACT_VERSION
    assert CONTRACT_VERSION == "3"
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}")
    assert w["contract_version"] == "3"
    # the composite pin's reduction column is keyed by its canonical expression (WP-NAME-1)
    assert w["columns"][0]["name"] == "avg(revenue @ {store*product*cal.month})"


# ── the composite pin denotes a DIFFERENT statistic than the atom-grain reading (F1's point) ──
def test_composite_pin_is_not_the_faithful_atom_reading(fixture_connector):
    """The whole F1 exhibit: `mean of revenue@{store*product*cal.month}` (mean of sums) is a
    different number than the atom-grain mean — two well-formed asks that disagree."""
    s = _srv(fixture_connector)
    coarse = _stmt(s, "SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}")
    fine = _stmt(s, "SELECT avg(revenue @ {store*product*day}) AT {cal.month}")
    cv = [v["value"] for v in coarse["columns"][0]["values"]]
    fv = [v["value"] for v in fine["columns"][0]["values"]]
    assert cv != fv                                         # the composition denotes a different statistic


# ── Law 3 boundary (composite input × FACED output): the rowed future finding, refused honestly ──
def test_law3_composite_faced_pin_refuses_at_the_chain_guard():
    """WP-GRAIN-1 scope note (spec §"scope, precisely", last row): the composite-input × faced-output
    combinatoric is BEYOND the natural extension of `serve_touch_crossing`. Pinning both a base level
    and a faced coordinate (`{product*category.touch}`) resolves the inner at a faced-composite grain,
    which the existing G4 chain guard refuses with `chained_crossing` — an honest, named refusal, never
    a silent wrong number. The face-crossing SERVE path for a pinned reduction is the rowed future
    finding (see PR discussion / Huayin ruling at the 0.13.4 gate)."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import test_relate_touch as TR
    srv = TR._server(TR.MANIFOLD, TR.TABLES)
    w = _stmt(srv, "SELECT sum(revenue @ {product*category.touch}) AT {category.touch}")
    assert w["outcome"] in ("refuse", "error")
    assert _no_result(w).get("reason") == "chained_crossing"
    # and the PLAIN faced output (no inline-reduction pin) still SERVES — no regression to the face path
    plain = wire_frame(srv.frame("category.touch").column("revenue", "revenue").run())
    assert plain["outcome"] in ("serve", "disclose")

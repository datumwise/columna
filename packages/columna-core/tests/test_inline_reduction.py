"""
test_inline_reduction.py — WP-B.1: inline reduction of a derivation (capture v0.8; ruling (A)).

Closes doctrine-gap DG-1. Two forms of `R(inner)` in a column expression:

  * PINNED   `avg(aov@day) @ month` — the input anchor is pinned; a definite quantity, served with an
              IMMATERIAL communicative disclosure naming the reading. Identical to the DECLARED
              AT-metric (`daily_aov`) — same reading, two spellings; never the pooled value.
  * UNPINNED `avg(aov) @ ...`       — the input anchor is not given, so the planner filters the
              candidate grains for LAWFULNESS FIRST and disposes on how many survive (ruling §9,
              Huayin 2026-08-20, superseding the flat "unpinned ⇒ clarify" of capture v0.8):
                |L| = 0  REFUSE  `blocked_reduction` — no reading is lawful, so there is no question
                |L| = 1  DISCLOSE — default to it, with a MATERIAL `input_anchor` caveat naming the
                                    grain the planner chose on the reader's behalf
                |L| > 1  CLARIFY `input_anchor_ambiguous` — over the LAWFUL candidates ONLY
              A clarify is a menu of readings the asker may choose between; an unlawful reading is
              not a choice, and offering it would make Clarify reachable before lawfulness.

input_anchor-fit finding (owed to CP-B2, pinned here): an EXPLICITLY user-pinned input anchor is a
deliberate, visible choice, so it owes a communicative note (immaterial `provenance`), NOT the
material `input_anchor` caveat. Fork surfaced to Huayin (reason-code reuse; caveat materiality).

Fixtures (`fixture_connector`) come from tests/conftest.py.
"""
import os
import re

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


def _srv(fixture_connector, certify=True, extra=""):
    """P0.5a closed-by-default: travel over an FD-claimed edge (day -> cal.month) serves only once the
    governing hierarchy is CORROBORATED on the attested data. These tests are about inline-reduction
    semantics, so the helper certifies first (`adjudicate` = the publish gate)."""
    with open(_BENCHMARK_CML) as f:
        srv = ManifoldServer(parse_manifold(f.read() + "\n" + _DEFS + "\n" + extra), fixture_connector)
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


# ── UNPINNED: lawfulness FIRST, then the |L| trichotomy (ruling §9, 2026-08-20) ──────────────
def _menu(w):
    """The candidate LEVELS an `input_anchor_ambiguous` clarify offers, read out of its alternatives."""
    nr = w["columns"][0].get("no_result") or {}
    return sorted(m.group(1) for a in (nr.get("alternatives") or [])
                  if (m := re.search(r"to \'([\w.]+)\'", a.get("description") or "")))


def test_unpinned_inline_reduction_clarifies_over_lawful_candidates(fixture_connector):
    """|L| > 1 ⇒ CLARIFY, and the menu contains ONLY lawful readings.

    ANCHOR SWAPPED 2026-08-20 (ruling §9). MENU CORRECTED 2026-08-31 (P1-13): this asserted exactly
    `{day, store}`, which was the set the enumeration produced while it still required a candidate to
    REACH the output anchor — the pre-WP-GRAIN-1 rule the execution path had already left behind. A
    pin need not reach the anchor; the anchor's orthogonal levels join the input grain. So the ask is
    underdetermined between MORE readings than two, and the old two-item expectation was pinning the
    defect. The assertion below is deliberately no longer a COUNT: it is the invariant itself —
    everything offered is admissible under the same law an explicit pin is held to."""
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("region", "cal.month").column("y", "avg(aov)").run())
    assert w["outcome"] == "clarify"
    nr = w["columns"][0].get("no_result") or {}
    # OF-1 ruling: its own reason `input_anchor_ambiguous` (one reason per contested dimension),
    # NOT a reuse of `ambiguous_grain`.
    assert nr.get("reason") == "input_anchor_ambiguous" and nr.get("discriminator") == "ambiguous"
    assert _menu(w) == ["cal.quarter", "cal.week", "cal.year", "customer", "day", "product", "store"]
    # THE INVARIANT, checked rather than trusted: every level on the menu is a reading the planner
    # ADMITS when the asker writes it out. Asserted at PLAN, which is where admissibility lives —
    # three of these then die in the ENGINE assembling a two-branch composite grain, which is P1-15
    # and is exactly as true when the reader pins it by hand.
    for L in _menu(w):
        planned = wire_frame(s.planner.plan(("region", "cal.month"), [("y", f"avg(aov@{L})")]),
                             executed=False)
        assert planned["outcome"] in ("serve", "disclose"), f"offered an inadmissible pin: {L}"


def test_unpinned_single_lawful_candidate_defaults_and_discloses(fixture_connector):
    """|L| = 1 ⇒ PROCEED, not clarify (ruling §9, MINTED 2026-08-20).

    ANCHOR SWAPPED 2026-08-31 (P1-13), was `cal.month` on the claim that "only `day` reaches the
    anchor" — true under the superseded reachability rule and false under WP-GRAIN-1, where seven
    other levels are lawful readings there. Defaulting silently to one of eight was the defect, not
    the fix. `customer*day*store` is a genuine one-reading anchor: `product` is the only level left
    that is neither an output target nor excluded, so nothing is contested.

    The DISPOSITION LAW is unchanged and is what this test exists for: one lawful reading is not a
    question. The planner defaults to it and serves, and because the defaulting is a decision the
    READER did not make it rides as a MATERIAL `input_anchor` caveat (OF-2's defaulted half) — wire
    outcome `disclose`, never a silent serve and never a clarify with one answer."""
    s = _srv(fixture_connector)
    anchor = ("customer", "day", "store")
    w = wire_frame(s.frame(*anchor).column("y", "avg(aov)").run())
    assert w["outcome"] == "disclose"
    assert w["columns"][0].get("no_result") is None
    discs = {d["code"]: d for d in (w["columns"][0].get("disclosures") or [])}
    assert discs["input_anchor"]["materiality"] == "material"
    assert "DEFAULTED to \'product\'" in discs["input_anchor"]["detail"]
    # the defaulted reading IS the pinned reading — same number, one of them merely disclosed harder
    d1 = s.frame(*anchor).column("c", "avg(aov)").run().data.sort(list(anchor))["c"].to_list()
    d2 = s.frame(*anchor).column("c", "avg(aov@product)").run().data.sort(list(anchor))["c"].to_list()
    assert d1 == pytest.approx(d2)


def test_unpinned_with_no_lawful_candidate_refuses(fixture_connector):
    """|L| = 0 ⇒ REFUSE `blocked_reduction` (MINTED 2026-08-20, ruling §9 + the generated-family law).

    ANCHOR SWAPPED 2026-08-31 (P1-13). This used `sum(level.last)` at `cal.month` and reasoned that
    "the one candidate grain (`day`) would have to cross exactly that lineage". There was never only
    one: pinning `@store` or `@region` reduces the stock across the STORE axis at a month, crosses no
    calendar edge, and SERVES. The old expectation was the superseded enumeration, and the ask it
    named is one of the six-explicit-pins-serve cases P1-13 is about.

    `sum(level)` at `cal.month*category` keeps the test's actual subject — a generated `sum` over a
    stock whose `sum` is BLOCKED along `calendar` — at an anchor where the exclusion really is total.
    Nothing is asked of the reader: generating the family does not create the permission, so the ask
    is refused rather than offered as a menu item that would launder the answer one keystroke later."""
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("cal.month", "category").column("z", "sum(level)").run())
    assert w["outcome"] == "refuse"
    nr = w["columns"][0]["no_result"]
    assert (nr["kind"], nr["reason"], nr["discriminator"]) == ("refuse", "blocked_reduction", "unsupported")
    assert "no lawful input anchor" in nr["detail"]
    # The detail REPORTS the verdicts rather than asserting one cause (P1-13): each candidate is
    # named with the refusal the pin would earn if it were written out.
    assert "blocked_reduction" in nr["detail"] and "day" in nr["detail"]
    assert nr.get("alternatives"), "a refusal owes the reader a lawful neighbour (DG-2 invariant 5)"


def test_unpinned_names_a_pinnable_fix(fixture_connector):
    """The clarify's detail points the user at a pin that resolves it — and the pin it names is one
    of the readings it offered, not a level picked from somewhere else."""
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("region", "cal.month").column("y", "mean(aov)").run())
    detail = (w["columns"][0].get("no_result") or {}).get("detail") or ""
    assert "does not pin" in detail
    hint = re.search(r"mean\(aov@([\w.]+)\)\'", detail)
    assert hint and hint.group(1) in _menu(w)


# ── the generated-family law: a family is generated, a PERMISSION is not (2026-08-20) ────────
@pytest.mark.parametrize("expr", [
    "level.sum",                       # WRITTEN as a declared family member
    "sum(level.last@day)",             # GENERATED by an inline reducer above a lawful sibling
    "-sum(level.last@day)",            # unary carrier
    "sum(level.last@day) + level.last",  # binary carrier
    "2 * sum(level.last@day)",         # scalar carrier
    "cumsum(level.sum)",               # scan carrier
])
def test_blocked_reduction_refuses_through_every_carrier(fixture_connector, expr):
    """MINTED 2026-08-20 (Huayin, generated-family law, §2). The verdict follows the OPERATION and its
    governed ancestry, not the spelling: whether `sum` over the stock is written as the declared member
    `level.sum` or generated inline above the lawful sibling `level.last`, and whether it is then
    wrapped in unary / binary / scalar / scan carriers, the answer is the same REFUSAL. A carrier
    transports an operation; it does not grant it an authority the declaration withholds."""
    s = _srv(fixture_connector)
    w = wire_frame(s.frame("store").column("c", expr).run())
    assert w["outcome"] == "refuse"
    nr = w["columns"][0]["no_result"]
    assert (nr["kind"], nr["reason"], nr["discriminator"]) == ("refuse", "blocked_reduction", "unsupported")
    assert "calendar" in nr["detail"]
    assert not (w["columns"][0].get("disclosures") or [])       # nothing served ⇒ nothing to caveat


def test_derived_carrier_refuses_the_same_way(fixture_connector):
    """The DERIVED carrier, same law (2026-08-20). Naming the blocked reduction in a `DERIVED` formula
    is the most authoritative-looking carrier there is, and it changes nothing: the planner expands the
    name before the law chokepoint, so the declaration inherits the refusal."""
    s = _srv(fixture_connector, extra="DERIVED lvlsum = level.sum")
    named = wire_frame(s.frame("store").column("c", "lvlsum").run())
    inline = wire_frame(s.frame("store").column("c", "level.sum").run())
    assert named["outcome"] == inline["outcome"] == "refuse"
    assert named["columns"][0]["no_result"]["reason"] == "blocked_reduction"


# ── OF-1: the minted reason lives in the closed vocabulary, distinct from ambiguous_grain ───
def test_input_anchor_ambiguous_is_a_distinct_clarify_reason():
    """OF-1 ruling: `input_anchor_ambiguous` is its OWN reason (CLARIFY/AMBIGUOUS), sibling to
    `co_anchor_ambiguous` — not a reuse of `ambiguous_grain`, whose gloss stays single-meaning."""
    from columna_core.disclosure import ANALYTICAL, REASON_OUTCOME, CLARIFY, AMBIGUOUS
    assert REASON_OUTCOME["input_anchor_ambiguous"] == (CLARIFY, AMBIGUOUS, ANALYTICAL)
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
    from columna_core.disclosure import ANALYTICAL, REASON_OUTCOME, REFUSE, UNSUPPORTED
    assert REASON_OUTCOME["pin_coarser_than_output"] == (REFUSE, UNSUPPORTED, ANALYTICAL)
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
    from columna_core.disclosure import ANALYTICAL, REASON_OUTCOME, CLARIFY, AMBIGUOUS
    assert REASON_OUTCOME["redundant_pin"] == (CLARIFY, AMBIGUOUS, ANALYTICAL)


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
    assert CONTRACT_VERSION == "4"
    s = _srv(fixture_connector)
    w = _stmt(s, "SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}")
    assert w["contract_version"] == "4"
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

"""
test_envelope_sugars.py — the FrameQL sugar set (WP-FrameQL sugars increment).

The ratified minimal set (grammar §3), each MECHANICAL-or-refused (rider 2). Three properties enforced:
 - rider 1: desugaring is ONE real transform to canonical AST before planning; the canonical form is a
   faithful artifact (round-trips), so EXPLAIN can emit it directly.
 - rider 2: every sugar ships its refusal test; the refusal fires a RATIFIED code.
 - rider 3: the omitted-input-anchor sugar's refusal IS the shipped input_anchor_ambiguous clarify —
   same code, same channel, identical wire shape (no re-mint).
"""
import pytest

from columna_core.envelope import parse_statement, Series
from columna_core.disclosure_wire import wire_frame
from columna_core.frameql import FrameQLSyntaxError


def _desugar(server, q):
    return server.planner.desugar(parse_statement(q))


def _wire(server, q):
    return wire_frame(server.planner.run_statement(parse_statement(q)))


# --- rider 1: the transform produces a faithful canonical artifact -------------------------------
def test_desugar_fills_alias_and_braces(fixture_server):
    d = _desugar(fixture_server, "SELECT avg(aov @ day) AT {cal.month}")
    # WP-NAME-1 (0.14.0): bare @ -> canonical braces; the identity IS the canonical expression (no mechanical `avg_aov`)
    assert d.series == [Series(expr="avg(aov @ {day})", alias="avg(aov @ {day})")]
    assert d.anchor == ("cal.month",) and d.bindings == []


def test_desugar_inlines_with(fixture_server):
    d = _desugar(fixture_server, "WITH t = revenue @ {transaction} SELECT sum(t) AS g AT {store}")
    assert d.bindings == []                                    # WITH is gone from the canonical form
    assert "revenue @ {transaction}" in d.series[0].expr and d.series[0].alias == "g"


def test_desugar_comma_anchor_to_star(fixture_server):
    d = _desugar(fixture_server, "SELECT revenue AT {product, region}")
    assert d.anchor == ("product", "region")
    assert "AT {product*region}" in d.render_canonical()      # `*` is canonical in the emitted form


def test_canonical_round_trips_and_is_idempotent(fixture_server):
    d1 = _desugar(fixture_server, "SELECT avg(aov @ day) AS a, revenue AT {store}")
    d2 = fixture_server.planner.desugar(parse_statement(d1.render_canonical()))
    assert d1.render_canonical() == d2.render_canonical()     # canonical is a fixed point


# --- the bare `@ level` sugar: same anchor, same wire as the braced form -------------------------
def test_bare_and_braced_input_anchor_identical(fixture_server):
    bare = _wire(fixture_server, "SELECT avg(aov @ day) AT {cal.month}")
    braced = _wire(fixture_server, "SELECT avg(aov @ {day}) AT {cal.month}")
    assert bare["outcome"] == braced["outcome"] == "serve"

    def keyed(w):
        return sorted((r["cal.month"], round(r["value"], 9)) for r in w["columns"][0]["values"])
    assert keyed(bare) == keyed(braced)          # same anchor -> same data (order-independent)


# --- rider 3: the omitted-input-anchor sugar's refusal IS the shipped clarify --------------------
# ANCHOR SWAPPED 2026-08-20 (Huayin, ruling §9). Rider 3 is about the sugar path and the shipped terse
# path landing on the SAME channel — it is not about `{cal.month}` in particular. Since §9 filters
# candidate input anchors for lawfulness FIRST, `{cal.month}` leaves exactly ONE lawful reading
# (`day`), which is no longer a contested choice: it defaults and DISCLOSES (pinned separately below).
# The clarify carrier moves to `{region*cal.month}`, where `store` and `day` both reach the anchor
# lawfully — two readings, a real menu, and the ratified code is unchanged.
def test_omitted_input_anchor_clarifies_ratified_code(fixture_server):
    w = _wire(fixture_server, "SELECT avg(aov) AT {region*cal.month}")
    assert w["outcome"] == "clarify"
    assert w["columns"][0]["no_result"]["reason"] == "input_anchor_ambiguous"    # ratified code, no re-mint


def test_sugar_and_shipped_paths_identical_wire_shape(fixture_server):
    # the envelope sugar path and the shipped terse path must produce the IDENTICAL no-result (rider 3)
    sugar = _wire(fixture_server, "SELECT avg(aov) AT {region*cal.month}")
    shipped = wire_frame(fixture_server.frame("region", "cal.month").column("rate", "avg(aov)").run())
    s_nr = sugar["columns"][0]["no_result"]
    h_nr = shipped["columns"][0]["no_result"]
    assert sugar["outcome"] == shipped["outcome"] == "clarify"
    assert (s_nr["reason"], s_nr["discriminator"], s_nr["alternatives"]) == \
           (h_nr["reason"], h_nr["discriminator"], h_nr["alternatives"])


def test_omitted_input_anchor_defaults_and_discloses_when_one_lawful_reading(fixture_server):
    # MINTED 2026-08-20 (Huayin, ruling §9), the other half of what the sugar can now do. Omitting the
    # input anchor is not automatically a question: the candidates are filtered for lawfulness first,
    # and when exactly one survives the planner defaults to it and PROCEEDS. The choice it made for the
    # reader rides on the wire as a MATERIAL `input_anchor` caveat — disclose, never a silent serve —
    # and the sugar path and the shipped terse path agree on that too.
    # ANCHOR SWAPPED 2026-08-31 (P1-13). This used `{cal.month}` on the claim that `day` is the ONLY
    # lawful input anchor there — true under the SUPERSEDED enumeration, which required a candidate to
    # REACH the output anchor, and false under WP-GRAIN-1, where eight levels are lawful readings at
    # `cal.month`. Defaulting silently to one of eight was the defect. `{customer, day, store}` is a
    # genuine one-reading anchor: `product` is the only level that survives the same law an explicit
    # pin is held to. The DISPOSITION LAW under test is unchanged.
    sugar = _wire(fixture_server, "SELECT avg(aov) AT {customer, day, store}")
    shipped = wire_frame(fixture_server.frame("customer", "day", "store").column("rate", "avg(aov)").run())
    assert sugar["outcome"] == shipped["outcome"] == "disclose"
    assert sugar["columns"][0].get("no_result") is None

    def material(w):
        return {(d["code"], d["materiality"]) for d in w["columns"][0]["disclosures"]
                if d["materiality"] == "material"}
    assert material(sugar) == material(shipped) == {("input_anchor", "material")}


# --- rider 2: every sugar ships its refusal (mechanical-or-refused, no heuristic middle) ---------
def test_unaliased_complex_expr_refused(fixture_server):
    # the bare-measure-at-AT sugar names itself only where unambiguous; a composite has no default
    with pytest.raises(FrameQLSyntaxError) as ei:
        _desugar(fixture_server, "SELECT revenue / orders AT {region}")
    assert "AS" in str(ei.value)


def test_composite_input_anchor_desugars_mechanically(fixture_server):
    # WP-GRAIN-1 (ratified 2026-07-29): a product input anchor is no longer refused at the sugar layer —
    # it is a first-class COMPOSITE pin. `*` and `,` are two spellings of the one product grain, folded
    # to `*` in canonical form (mirroring the anchor parser). The refusals moved to the SEMANTIC laws
    # (pin_coarser_than_output / redundant_pin), tested in test_inline_reduction.
    # WP-NAME-1 (0.14.0): the key IS the canonical expression — the composite pin is visible in it.
    star = _desugar(fixture_server, "SELECT avg(aov @ {day*store}) AT {region}")
    comma = _desugar(fixture_server, "SELECT avg(aov @ {day, store}) AT {region}")
    assert star.series == [Series(expr="avg(aov @ {day*store})", alias="avg(aov @ {day*store})")]
    assert comma.series == star.series                          # comma folds to the product spelling
    assert "avg(aov @ {day*store})" in star.render_canonical()  # canonical carries the braced product


def test_single_universe_sugar_refusal_is_cross_universe(fixture_server):
    # the single-universe sugar resolves silently when one universe; spanning two is the ratified refusal
    # (aliased so it clears the §4 naming law and reaches the §2c expression-law check)
    w = _wire(fixture_server, "SELECT revenue / level.last AS ratio AT {store}")
    assert w["outcome"] == "error"
    assert w["columns"][0]["no_result"]["reason"] == "cross_universe"


def test_bad_anchor_level_refused(fixture_server):
    # the comma-anchor sugar desugars mechanically; an unknown qualified level is refused at resolution
    with pytest.raises(FrameQLSyntaxError):
        _desugar(fixture_server, "SELECT revenue AT {geo.nowhere}")

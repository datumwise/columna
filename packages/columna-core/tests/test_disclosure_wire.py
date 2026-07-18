"""
test_disclosure_wire.py — pure unit tests for the wire adapter (no server, no warehouse).

Covers the NORMATIVE category->(code, materiality) table, caveat/outcome mapping, faithful
alternative re-encoding (with the derived `apply.universe`), and full-frame assembly built from
synthetic Caveat/Outcome/ColumnResult/FrameResult values.
"""
import polars as pl
import pytest

from columna_core.disclosure import Caveat, Disclosure, Outcome
from columna_core.planner import ColumnResult, FrameResult
from columna_core import disclosure_wire as dw


# --- the normative table --------------------------------------------------------------------
def test_category_table_is_the_normative_mapping():
    assert dw.code_for("b_anchor_crossing") == "blocked_reduction"
    assert dw.code_for("coverage") == "denominator_population"
    assert dw.code_for("unconfirmed_assumption") == "input_anchor"
    assert dw.code_for("approximation") == "approximation"
    assert dw.code_for("freshness") == "freshness"
    assert dw.code_for("transport") == "provenance"


@pytest.mark.parametrize("category,expected", [
    ("b_anchor_crossing", "material"),
    ("coverage", "material"),
    ("unconfirmed_assumption", "material"),
    ("freshness", "immaterial"),
    ("transport", "immaterial"),
])
def test_default_materiality(category, expected):
    assert dw.materiality_for(category) == expected


def test_approximation_materiality_is_rel_error_gated():
    assert dw.materiality_for("approximation", 0.005) == "immaterial"
    assert dw.materiality_for("approximation", 0.01) == "material"    # threshold is inclusive
    assert dw.materiality_for("approximation", 0.02) == "material"
    assert dw.materiality_for("approximation", None) == "immaterial"


def test_reserved_codes_present():
    for code in ("stock_reading", "distinct_grain", "weighting_grain", "extremum_grain",
                 "incomplete_data", "conflicting_data", "other"):
        assert code in dw.RESERVED_CODES


def test_unknown_category_falls_back_to_other_immaterial():
    c = Caveat("some_future_category", "detail")
    w = dw.wire_caveat(c)
    assert w["code"] == "other" and w["materiality"] == "immaterial"
    assert w["category"] == "some_future_category"   # engine category preserved


# --- caveat mapping -------------------------------------------------------------------------
def test_wire_caveat_full_fields_b_anchor():
    c = Caveat("b_anchor_crossing", "collapses 'day' along blocked lineage 'calendar'",
               severity="critical", source="day", remedy="use .last")
    w = dw.wire_caveat(c)
    assert w == {
        "code": "blocked_reduction", "materiality": "material", "severity": "critical",
        "category": "b_anchor_crossing",
        "detail": "collapses 'day' along blocked lineage 'calendar'",
        "remedy": "use .last", "source": "day", "rel_error": None,
    }


def test_wire_caveat_approximation_material_by_rel_error():
    assert dw.wire_caveat(Caveat("approximation", "hll", rel_error=0.05))["materiality"] == "material"
    assert dw.wire_caveat(Caveat("approximation", "hll", rel_error=0.001))["materiality"] == "immaterial"


# --- outcome / alternatives (faithful, with derived apply) ----------------------------------
@pytest.mark.skip(reason="co_anchor_ambiguous RETIRED (§2c, 2026-07-16, tombstone); the on_universe "
                         "wire-apply mechanism it exercised is dormant, pending OF-4 (server universe-arg removal)")
def test_wire_outcome_coanchor_derives_universe_apply():
    o = Outcome("co_anchor_ambiguous", "which population is the rate over?",
                alternatives=("express both numerator and denominator within universe 'store_days'",
                              "express both numerator and denominator within universe 'transactions'"),
                discriminator="ambiguous")
    w = dw.wire_outcome(o)
    assert w["kind"] == "clarify" and w["discriminator"] == "ambiguous"
    assert w["reason"] == "co_anchor_ambiguous"
    assert [a["token"] for a in w["alternatives"]] == ["on_universe('store_days')", "on_universe('transactions')"]
    assert [a["apply"] for a in w["alternatives"]] == [{"universe": "store_days"}, {"universe": "transactions"}]
    # description is the engine prose verbatim (faithful)
    assert w["alternatives"][0]["description"].endswith("universe 'store_days'")


def test_wire_outcome_non_universe_alternative_echoes_verbatim_no_apply():
    o = Outcome("non_functional_transport", "fan-out",
                alternatives=("membership filter — accept the overlap deliberately",
                              "WITH allocation — supply a partition-of-unity split [Pro]"))
    w = dw.wire_outcome(o)
    assert w["kind"] == "clarify"
    for a in w["alternatives"]:
        assert a["token"] == a["description"]   # echoed verbatim
        assert "apply" not in a                 # no machine action invented


def test_wire_outcome_refuse_and_error_kinds():
    assert dw.wire_outcome(Outcome("out_of_universe", "x", discriminator="unsupported"))["kind"] == "refuse"
    assert dw.wire_outcome(Outcome("unknown", "no such op"))["kind"] == "error"


# --- full frame assembly --------------------------------------------------------------------
def _served_col(name, frame, caveats=(), population=None):
    return ColumnResult(name, name, frame, Disclosure(tuple(caveats), population))


def test_wire_frame_served_scalar_and_vector():
    scal = _served_col("revenue", pl.DataFrame({"revenue": [42.0]}))
    vec = _served_col("revenue", pl.DataFrame({"region": ["east", "west"], "revenue": [10.0, 20.0]}))
    fs = FrameResult(scal.frame, Disclosure.clean(), [scal], ())
    fv = FrameResult(vec.frame, Disclosure.clean(), [vec], ("region",))
    ws = dw.wire_frame(fs)
    wv = dw.wire_frame(fv)
    assert ws["columns"][0]["value"] == 42.0
    assert wv["columns"][0]["values"] == [{"region": "east", "value": 10.0}, {"region": "west", "value": 20.0}]
    assert ws["contract_version"] == "1"
    assert ws["outcome"] == "serve" and wv["outcome"] == "serve"   # nothing material -> serve


def test_outcome_serve_vs_disclose_is_materiality_driven():
    # an IMMATERIAL disclosure (freshness) on a served frame stays `serve`
    fresh = _served_col("x", pl.DataFrame({"g": [1], "x": [1.0]}),
                        [Caveat("freshness", "served from cache")])
    w_imm = dw.wire_frame(FrameResult(fresh.frame, Disclosure((), None), [fresh], ("g",)))
    assert w_imm["columns"][0]["disclosures"][0]["materiality"] == "immaterial"
    assert w_imm["outcome"] == "serve"

    # a MATERIAL disclosure (b_anchor) flips it to `disclose`
    mat = _served_col("x", pl.DataFrame({"g": [1], "x": [1.0]}),
                     [Caveat("b_anchor_crossing", "collapses day", severity="critical")])
    w_mat = dw.wire_frame(FrameResult(mat.frame, Disclosure((), None), [mat], ("g",)))
    assert w_mat["outcome"] == "disclose"


def test_derive_outcome_no_result_moods_dominate():
    class _FR:  # minimal stand-in exposing .outcome
        def __init__(self, o): self.outcome = o
    assert dw.derive_outcome(_FR("refuse"), True) == "refuse"
    assert dw.derive_outcome(_FR("clarify"), True) == "clarify"
    assert dw.derive_outcome(_FR("error"), False) == "error"
    assert dw.derive_outcome(_FR("serve"), True) == "disclose"
    assert dw.derive_outcome(_FR("serve"), False) == "serve"


def test_wire_frame_banchor_served_with_material_critical_caveat():
    cav = Caveat("b_anchor_crossing", "collapses 'day'", severity="critical", source="day")
    col = _served_col("inv", pl.DataFrame({"store": [1], "inv": [7.0]}), [cav], population="store_days")
    fr = FrameResult(col.frame, Disclosure((cav,), "store_days"), [col], ("store",))
    w = dw.wire_frame(fr)
    assert w["outcome"] == "disclose"
    d = w["columns"][0]["disclosures"][0]
    assert (d["code"], d["materiality"], d["severity"]) == ("blocked_reduction", "material", "critical")


def test_wire_frame_clarify_column_carries_no_result():
    # a clarify column carries a no_result on the wire (generic encoding; uses an ACTIVE clarify reason
    # after co_anchor_ambiguous's §2c retirement).
    o = Outcome("input_anchor_ambiguous", "the input anchor is underdetermined",
                alternatives=("pin the input anchor to 'day'",), discriminator="ambiguous")
    col = ColumnResult("rate", "avg(aov)", None, Disclosure.clean(), refusal=o.classified())
    fr = FrameResult(None, Disclosure.clean(), [col], ("store", "day"))
    w = dw.wire_frame(fr)
    assert w["outcome"] == "clarify"
    assert w["columns"][0]["status"] == "clarify"
    assert w["columns"][0]["no_result"]["reason"] == "input_anchor_ambiguous"
    assert w["columns"][0]["no_result"]["alternatives"][0]["token"] == "pin the input anchor to 'day'"


def test_wire_frame_surfaces_frame_only_coverage_caveat():
    # two served columns; a frame-level coverage caveat that is on NO single column
    a = _served_col("revenue", pl.DataFrame({"store": [1], "revenue": [5.0]}), population="transactions")
    b = _served_col("inv", pl.DataFrame({"store": [1], "inv": [9.0]}), population="store_days")
    cover = Caveat("coverage", "frame spans multiple universes ['store_days','transactions']")
    fr = FrameResult(a.frame, Disclosure((cover,)), [a, b], ("store",))
    w = dw.wire_frame(fr, universe=None)
    codes = [d["code"] for d in w["frame"]["disclosures"]]
    assert "denominator_population" in codes
    assert all(d["materiality"] == "material" for d in w["frame"]["disclosures"])
    # a frame-scoped MATERIAL disclosure makes the served frame read `disclose` (not `serve`)
    assert w["outcome"] == "disclose"

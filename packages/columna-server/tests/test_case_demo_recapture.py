"""
test_case_demo_recapture.py — Cascadia inc3 (THE RECAPTURE): the seeded corpus is the drift gate.

Built expectation-first against recapture_exemplar_spec v0.1 (+ the desk's E6/E10 amendment, 2026-07-19
— RELATE faces made visible: E6 clarifies with the face MENU, E10 executes the touch crossing). The ten
exemplars' MOODS and REASON CODES are ratified expectations, asserted here; the NUMBERS are recorded
(asserted as shapes the spec fixes: 32 / 24 / 24), never as free values. Any deviation surfaces as a
`flags` entry with wire evidence — the corpus never harmonizes silently.

Recorded-and-flagged findings (brought to the desk in the recapture diff):
  • E8's reason code (left open by the desk) records as `out_of_universe`.
  • the manager transcript's `WHERE region = west` construction does NOT resolve in this build
    (`unsupported` / BinderException — a query-level WHERE cannot filter a dimension value; even a
    base dim refuses); the working construction anchors at {region, cal.quarter} and reads the row.
"""
import os

import pytest

import columna_server
from columna_server.store import _load_one
from columna_server import recapture

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


@pytest.fixture(scope="module")
def corpus():
    lm = _load_one("cascadia", _CASCADIA)
    lm.server.publish()

    class _Store:
        def get(self, mid):
            if mid != "cascadia":
                raise KeyError(mid)
            return lm
    return recapture.generate(_Store(), lm.server)


def test_every_exemplar_lands_on_its_ratified_mood(corpus):
    by_id = {e["id"]: e for e in corpus["exemplars"]}
    expected = {eid: mood for eid, _c, _q, mood, _r in recapture.EXEMPLARS}
    for eid, mood in expected.items():
        assert by_id[eid]["mood"] == mood, f"{eid}: mood {by_id[eid]['mood']} != ratified {mood}"


def test_ratified_reason_codes_are_present(corpus):
    by_id = {e["id"]: e for e in corpus["exemplars"]}
    for eid, _c, _q, _mood, reason in recapture.EXEMPLARS:
        if reason:
            assert reason in by_id[eid]["reason_tokens"], \
                f"{eid}: expected reason {reason!r} not in {by_id[eid]['reason_tokens']}"


def test_seeded_counts_are_the_shapes_the_spec_fixes(corpus):
    rc = {e["id"]: e["row_count"] for e in corpus["exemplars"]}
    assert rc["E1"] == 32     # 4 regions × 8 quarters (two years)
    assert rc["E5"] == 24     # 24 months
    assert rc["E7"] == 24     # 24 months


def test_e2_disclose_caveat_is_critical_and_names_calendar(corpus):
    e2 = next(e for e in corpus["exemplars"] if e["id"] == "E2")
    crossing = [d for d in e2["disclosures"] if d["token"] == "b_anchor_crossing"]
    assert crossing and crossing[0]["severity"] == "critical"
    assert "calendar" in (crossing[0]["detail"] or "")


def test_e9_explain_would_be_disclose_touches_no_data(corpus):
    e9 = next(e for e in corpus["exemplars"] if e["id"] == "E9")
    assert e9["kind"] == "explain" and e9["mood"] == "disclose"
    assert "b_anchor_crossing" in e9["reason_tokens"]


def test_e8_records_out_of_universe_the_open_code(corpus):
    e8 = next(e for e in corpus["exemplars"] if e["id"] == "E8")
    assert e8["mood"] == "refuse"
    assert "out_of_universe" in e8["reason_tokens"]   # the code the desk left open, recorded


def test_corpus_has_no_undeclared_drift(corpus):
    # the corpus flags deviations rather than harmonizing; the two KNOWN, desk-bound flags are the
    # manager WHERE (a transcript concern, not an exemplar) and E8's now-recorded code — neither is an
    # exemplar mood/reason deviation, so the exemplar corpus itself must carry ZERO flags.
    assert corpus["flags"] == [], f"unexpected exemplar drift: {corpus['flags']}"


def test_wheel_is_the_four_mood_story_order(corpus):
    assert corpus["wheel"] == ["E4", "E8", "E2", "E5"]   # clarify -> refuse -> disclose -> serve


def test_corpus_carries_all_twelve_with_the_wheel_subset_marked(corpus):
    # the recorded corpus is the FULL twelve E1-E12 (E10/E11/E12 = the RELATE-faces triad:
    # touch executes, assign single-counts with the shadow, alloc splits with the badge); the --play
    # wheel is a marked SUBSET of it.
    assert [e["id"] for e in corpus["exemplars"]] == [f"E{i}" for i in range(1, 13)]
    marked = {e["id"] for e in corpus["exemplars"] if e["in_wheel"]}
    assert marked == set(corpus["wheel"]) == {"E2", "E4", "E5", "E8"}


def test_e6_clarify_carries_the_face_menu(corpus):
    # ship-dark revoked: the bare-coordinate clarify now LISTS the declared face + its ratified folklore.
    e6 = next(e for e in corpus["exemplars"] if e["id"] == "E6")
    assert e6["mood"] == "clarify" and "non_functional_transport" in e6["reason_tokens"]
    menu = e6.get("menu") or []
    assert any(m.startswith("category.touch") for m in menu), f"the face menu is missing: {menu}"
    assert any("deliberately multi-counted" in m for m in menu)     # the ratified description rides the menu


def test_e10_touch_executes_and_discloses_the_overcount(corpus):
    e10 = next(e for e in corpus["exemplars"] if e["id"] == "E10")
    assert e10["mood"] == "disclose"                                # the crossing serves, honestly skewed
    assert "over_count" in e10["reason_tokens"]                     # the deliberate multi-count drives disclose
    oc = [d for d in e10["disclosures"] if d["token"] == "over_count"]
    assert oc and oc[0]["severity"] == "caution"
    cov = [d for d in e10["disclosures"] if d["token"] == "transport" and "coverage" in (d["detail"] or "")]
    assert cov, "the coverage info caveat is missing"
    assert e10["row_count"] == 12                                   # 12 categories (recorded)

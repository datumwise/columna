"""
test_case_demo_recapture.py — Cascadia inc3 (THE RECAPTURE): the seeded corpus is the drift gate.

Built expectation-first against recapture_exemplar_spec v0.1 (+ the desk's E6/E10 amendment, 2026-07-19
— RELATE faces made visible: E6 clarifies with the face MENU, E10 executes the touch crossing). The
exemplars' MOODS and REASON CODES are ratified expectations, asserted here; the NUMBERS are recorded
(asserted as shapes the spec fixes: 32 / 24 / 24), never as free values. Any deviation surfaces as a
`flags` entry with wire evidence — the corpus never harmonizes silently.

RE-RATIFICATION 2026-08-20 (Huayin, generated-family law) — superseding ADR-020's inform-and-serve for
structurally prohibited reductions: a reduction traversing a lineage its operator is declared BLOCKED
along now REFUSES (`blocked_reduction`) instead of serving under a critical `b_anchor_crossing` caveat.
E2 and E9 moved from (disclose, b_anchor_crossing) to (refuse, blocked_reduction); a NEW exemplar E13
(`SELECT buyers AT {cal.month}` -> disclose/approximation) was minted to carry the wheel's disclose leg,
so the wheel is E4 -> E8 -> E13 -> E5 and the corpus is THIRTEEN.

Recorded-and-flagged findings (brought to the desk in the recapture diff):
  • E8's reason code (left open by the desk) records as `out_of_universe`.
  • the manager transcript's `WHERE region = west` construction does NOT resolve in this build
    (`unsupported` / BinderException — a query-level WHERE cannot filter a dimension value; even a
    base dim refuses); the working construction anchors at {region, cal.quarter} and reads the row.
  • E9's ratified reason now rides `would_be["no_result"]["reason"]`, not the disclosure channel —
    a would-be REFUSE has no caveats to carry it. `recapture.generate`'s EXPLAIN branch reads both
    channels (2026-08-20), matching the query branch's `_disclosure_tokens`; asserted below.
"""
import os

import pytest

import columna_server
from columna_server.store import _load_one
from columna_server import recapture

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


@pytest.fixture(scope="module")
def live():
    """The live one-manifold store + its loaded manifold. Exposed (2026-08-20) so a test can go back
    to the WIRE itself — needed now that an exemplar's ratified reason can live in `no_result`."""
    lm = _load_one("cascadia", _CASCADIA)
    lm.provider.runtime.publish()

    class _Store:
        def get(self, mid):
            if mid != "cascadia":
                raise KeyError(mid)
            return lm

        def ids(self):
            return ["cascadia"]

        def governed_ids(self):
            return []

        def resolve_public(self, mid, version=None):
            if version is not None:
                from columna_server.registry import PublicationNotFound
                raise PublicationNotFound(f"{mid}@{version}")
            return self.get(mid), None
    return _Store(), lm


@pytest.fixture(scope="module")
def corpus(live):
    store, lm = live
    return recapture.generate(store, lm.provider)


def test_every_exemplar_lands_on_its_ratified_mood(corpus):
    by_id = {e["id"]: e for e in corpus["exemplars"]}
    expected = {eid: mood for eid, _c, _q, mood, _r in recapture.EXEMPLARS}
    for eid, mood in expected.items():
        assert by_id[eid]["mood"] == mood, f"{eid}: mood {by_id[eid]['mood']} != ratified {mood}"


def test_ratified_reason_codes_are_present(corpus):
    by_id = {e["id"]: e for e in corpus["exemplars"]}
    for eid, _c, _q, _mood, reason in recapture.EXEMPLARS:
        if reason:
            # covers E9 too (2026-08-20): a would-be REFUSE carries its reason on `no_result`, and the
            # EXPLAIN branch of the recorder now harvests that channel as well as the disclosure one.
            assert reason in by_id[eid]["reason_tokens"], \
                f"{eid}: expected reason {reason!r} not in {by_id[eid]['reason_tokens']}"


def test_seeded_counts_are_the_shapes_the_spec_fixes(corpus):
    rc = {e["id"]: e["row_count"] for e in corpus["exemplars"]}
    assert rc["E1"] == 32     # 4 regions × 8 quarters (two years)
    assert rc["E5"] == 24     # 24 months
    assert rc["E7"] == 24     # 24 months


def test_e2_blocked_reduction_refuses_and_names_the_calendar_lineage(corpus):
    # FLIPPED 2026-08-20 (Huayin, generated-family law). Was: E2 DISCLOSES, carrying a CRITICAL
    # `b_anchor_crossing` caveat that named the calendar lineage. Now: E2 REFUSES with
    # `blocked_reduction`, because Disclose lives inside the lawful region and cannot legalize an
    # operation the governed law does not possess. What survives the flip is the load-bearing part —
    # the refusal still NAMES the lineage it is blocked along, so the reader learns why, not just no.
    e2 = next(e for e in corpus["exemplars"] if e["id"] == "E2")
    assert e2["mood"] == "refuse"
    blocked = [d for d in e2["disclosures"] if d["token"] == "blocked_reduction"]
    assert blocked, f"E2 must record `blocked_reduction`, got {e2['disclosures']}"
    assert "calendar" in (blocked[0]["detail"] or "")
    # NO values, and no caveat riding in place of the refusal: a refuse carries no disclosures at all.
    assert e2["row_count"] is None
    assert [d["token"] for d in e2["disclosures"]] == ["blocked_reduction"]
    assert not [d for d in e2["disclosures"] if d["token"] == "b_anchor_crossing"]


def test_e9_explain_would_be_refuse_touches_no_data(corpus, live):
    # FLIPPED 2026-08-20 (Huayin, generated-family law): the would-be mood of `EXPLAIN SELECT
    # stock.sum AT {store*cal.month}` moved from `disclose` to `refuse` — same reason as E2, and
    # `check before you run` now genuinely warns you OFF rather than pre-announcing a caveat. The
    # test's PURPOSE is unchanged: EXPLAIN answers this without touching a single row.
    from columna_server import tools as T

    e9 = next(e for e in corpus["exemplars"] if e["id"] == "E9")
    assert e9["kind"] == "explain" and e9["mood"] == "refuse"
    assert e9["row_count"] is None                       # no frame was materialized
    # touches no data — asserted against the wire, not inferred from the corpus entry
    store, _lm = live
    ex = T.explain_statement(store, "cascadia", e9["query"][len("EXPLAIN"):].strip())
    assert ex["executed"] is False and ex["fetches_delta"] == 0
    # and the would-be refusal names the ratified reason on `no_result` (not as a caveat)
    assert ex["series"][0]["would_be"]["no_result"]["reason"] == "blocked_reduction"
    # and the corpus RECORDS that reason: a would-be refusal carries it on `no_result`, not as a
    # caveat, so the recorder's EXPLAIN branch has to read both channels (2026-08-20).
    assert "blocked_reduction" in e9["reason_tokens"]
    assert "b_anchor_crossing" not in e9["reason_tokens"]


def test_e8_records_out_of_universe_the_open_code(corpus):
    e8 = next(e for e in corpus["exemplars"] if e["id"] == "E8")
    assert e8["mood"] == "refuse"
    assert "out_of_universe" in e8["reason_tokens"]   # the code the desk left open, recorded


def test_corpus_has_no_undeclared_drift(corpus):
    # the corpus flags deviations rather than harmonizing; the two KNOWN, desk-bound flags are the
    # manager WHERE (a transcript concern, not an exemplar) and E8's now-recorded code — neither is an
    # exemplar mood/reason deviation, so the exemplar corpus itself must carry ZERO flags.
    # STILL ZERO after the 2026-08-20 re-ratification: E2/E9 land on `refuse`/`blocked_reduction` and
    # the new E13 lands on `disclose`/`approximation`, exactly as the desk ratified them. (This gate
    # also surfaced the recorder's EXPLAIN blind spot: a would-be REFUSE carries its reason on
    # `no_result`, not as a caveat, so `recapture.generate` now harvests both channels there — the
    # gate flagged it rather than harmonizing it, which is exactly its job.)
    assert corpus["flags"] == [], f"unexpected exemplar drift: {corpus['flags']}"


def test_wheel_is_the_four_mood_story_order(corpus):
    # RE-CUT 2026-08-20 (Huayin, generated-family law): was ["E4", "E8", "E2", "E5"]. E2's mood moved
    # to `refuse`, so it can no longer carry the disclose leg; the new E13 (a lawful ask with an
    # approximate realization) takes it. The story order — clarify -> refuse -> disclose -> serve —
    # is unchanged; only the witness for `disclose` moved.
    assert corpus["wheel"] == ["E4", "E8", "E13", "E5"]   # clarify -> refuse -> disclose -> serve


def test_corpus_carries_all_thirteen_with_the_wheel_subset_marked(corpus):
    # the recorded corpus is the FULL thirteen E1-E13 (E10/E11/E12 = the RELATE-faces triad:
    # touch executes, assign single-counts with the shadow, alloc splits with the badge); the --play
    # wheel is a marked SUBSET of it.
    # WIDENED 2026-08-20 (Huayin, generated-family law): twelve -> THIRTEEN. E13 (`SELECT buyers AT
    # {cal.month}` -> disclose/approximation) was minted to carry the wheel's disclose leg after E2
    # became a refuse; E2 stays in the corpus as the structural-refusal witness, just out of the wheel.
    assert [e["id"] for e in corpus["exemplars"]] == [f"E{i}" for i in range(1, 14)]
    marked = {e["id"] for e in corpus["exemplars"] if e["in_wheel"]}
    assert marked == set(corpus["wheel"]) == {"E4", "E5", "E8", "E13"}
    assert "E2" in {e["id"] for e in corpus["exemplars"]} and not next(
        e for e in corpus["exemplars"] if e["id"] == "E2")["in_wheel"]


def test_e13_is_the_disclose_witness_a_lawful_ask_approximately_realized(corpus):
    # NEW 2026-08-20 (Huayin, generated-family law): the wheel's disclose leg. The ask is SOUND — it
    # is the realization that is approximate (an HLL distinct estimate), so the numbers come back and
    # the one condition on them travels with them. This is the shape Disclose is FOR, and the reason
    # E2 could never have been it: a disclosure conditions an answer, it does not authorize one.
    e13 = next(e for e in corpus["exemplars"] if e["id"] == "E13")
    assert e13["mood"] == "disclose"
    assert "approximation" in e13["reason_tokens"]
    approx = [d for d in e13["disclosures"] if d["token"] == "approximation"]
    assert approx and "HLL distinct estimate" in (approx[0]["detail"] or "")
    assert e13["row_count"] == 24                                   # 24 months (recorded)


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

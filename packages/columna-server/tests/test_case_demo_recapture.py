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
so the wheel is E4 -> E2 -> E13 -> E5 and the corpus is THIRTEEN. The REFUSE leg then moved from E8
(out-of-universe) to E2 as well: the four cases are meant to be distinguished by LAWFULNESS, and only
E2 teaches that a perfectly computable number can still be one the governed law does not grant. E8
stays in the corpus and keeps its own tests.

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
from columna_server import recapture, tools as T

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
    # RE-CUT 2026-08-20 (Huayin, generated-family law): was ["E4", "E8", "E2", "E5"]. Twice over.
    # E2's mood moved to `refuse`, so it could no longer carry the DISCLOSE leg — the new E13 (a
    # lawful ask with an approximate realization) takes it. E2 then took the REFUSE leg from E8,
    # because the four cases should be distinguished by lawfulness: E8 is a true refusal but teaches
    # only that the ask was addressed outside the contracted space. The story order — clarify ->
    # refuse -> disclose -> serve — is unchanged; two of its four witnesses moved.
    assert corpus["wheel"] == ["E4", "E2", "E13", "E5"]   # clarify -> refuse -> disclose -> serve


def test_corpus_carries_all_thirteen_with_the_wheel_subset_marked(corpus):
    # the recorded corpus is the FULL thirteen E1-E13 (E10/E11/E12 = the RELATE-faces triad:
    # touch executes, assign single-counts with the shadow, alloc splits with the badge); the --play
    # wheel is a marked SUBSET of it.
    # WIDENED 2026-08-20 (Huayin, generated-family law): twelve -> THIRTEEN. E13 (`SELECT buyers AT
    # {cal.month}` -> disclose/approximation) was minted to carry the wheel's disclose leg after E2
    # became a refuse; E2 then took the refuse leg, and E8 left the wheel while staying in the corpus.
    assert [e["id"] for e in corpus["exemplars"]] == [f"E{i}" for i in range(1, 14)]
    marked = {e["id"] for e in corpus["exemplars"] if e["in_wheel"]}
    assert marked == set(corpus["wheel"]) == {"E2", "E4", "E5", "E13"}
    # E8 stays in the corpus, out of the wheel — a true refusal the wheel no longer needs to spend a
    # leg on, kept because it is still the clearest out-of-universe witness the tests have.
    assert "E8" in {e["id"] for e in corpus["exemplars"]} and not next(
        e for e in corpus["exemplars"] if e["id"] == "E8")["in_wheel"]


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


# ── ORPHANED REASONS, CERTIFIED FROM THEIR CALL SITES (2026-08-20) ───────────────────────────────
# `chained_crossing` and `anchor_spent` were EMITTED by the engine but absent from
# `disclosure.REASON_OUTCOME`, so `outcome_for`'s silent `.get(..., ERROR)` default gave them a
# verdict nobody chose: both shipped as ERROR for months. Registering them closed that, and
# `outcome_for` now fails closed — but a registration is a claim about what the code MEANS, and a
# claim belongs in a test rather than in the commit message that made it. These two exercise the real
# refusal paths (Cascadia is the only fixture carrying declared RELATE faces) and check that the
# verdict and the reason the reader receives match the intent the call site states in words.

def test_a_mixed_faced_anchor_is_a_REALIZATION_gap_not_an_analytical_refusal(live):
    """P1-21, ruled Huayin 2026-09-01. THE DOCSTRING THIS TEST USED TO CARRY WAS THE DEFECT, so it is
    replaced rather than edited around. It read:

        "A well-formed ask with no lawful path is a REFUSE ... never an ERROR, which would say the
         request was malformed. It was not."

    Both halves are right about what they deny and wrong about this ask. There IS a lawful path —
    G4's own account is that the shape is "not yet licensed (disclosure-stacking undesigned)", and
    OF-26 records "a single faced coordinate is the maximal expressible CROSS seam at v1". Those are
    statements about THIS BUILD, so the standing is a realization gap: a more capable realization
    serves this ask unchanged, which is exactly what an analytical Refuse must never be said of.

    The second correction is the diagnostic. This ask names ONE face plus `cal.month`, and the old
    refusal told the reader it "would cross two declared faces in sequence" — false, and it sends
    them to remove a face they did not write. The two shapes are now told apart.

    The `error` mood is transitional, not the destination: `unsupported`/`filter_unsupported` ride it
    too, pending the wire ruling (v0.2 §13, Step 6). What is settled here is the JURISDICTION."""
    from columna_core.disclosure import REALIZATION, jurisdiction_for
    store, _lm = live
    w = T.query(store, "cascadia", "SELECT revenue AT {category.touch, cal.month}")
    nr = w["columns"][0]["no_result"]
    assert nr["reason"] == "mixed_faced_anchor"
    assert jurisdiction_for(nr["reason"]) == REALIZATION
    assert "single faced coordinate" in nr["detail"]
    assert "two declared faces" not in nr["detail"], "the old diagnostic was false of this ask"


def test_anchor_spent_refuses_because_the_counts_cannot_travel(live):
    """engine.py's G5 anchor law: a distinct-class measure's anchor is SPENT at the frontier grain —
    per-member counts "cannot be summed, weighted, or routed". A structural prohibition with named
    alternatives, which is a REFUSE."""
    store, _lm = live
    w = T.query(store, "cascadia", "SELECT buyers AT {category.touch}")
    nr = w["columns"][0]["no_result"]
    assert w["outcome"] == "refuse"
    assert (nr["kind"], nr["reason"], nr["discriminator"]) == ("refuse", "anchor_spent", "unsupported")
    assert "cannot be summed, weighted, or routed" in nr["detail"]


def test_no_engine_refusal_reason_is_unregistered():
    """The census that found the two orphans, kept as a standing guard. Every `Refusal("<reason>"` in
    the shipped source must have a REASON_OUTCOME entry — otherwise `outcome_for` now raises where it
    used to silently classify, which is the right failure but a late one. Catch it here instead."""
    import pathlib
    import re

    from columna_core.disclosure import REASON_OUTCOME

    roots = [pathlib.Path(m.__file__).parent for m in (__import__("columna_core"),
                                                       __import__("columna_server"))]
    emitted = {m for root in roots for f in root.rglob("*.py")
               for m in re.findall(r'Refusal\(\s*"([a-z_]+)"', f.read_text(encoding="utf-8"))}
    assert emitted, "the scan found no Refusal sites — the pattern drifted, not the vocabulary"
    unregistered = sorted(emitted - set(REASON_OUTCOME))
    assert not unregistered, (
        f"refusal reason(s) {unregistered} are emitted but unregistered. Register each with a dated "
        f"note on its intent — a vocabulary that grows by rule cannot also grow by accident.")

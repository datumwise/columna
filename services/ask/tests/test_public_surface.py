"""F4 — the public surface of a REVIEWED, PUBLISHED Q&A.

APPROVED 2026-08-26 16:35, item 8. Hermetic: no key, no network, no model. These are the checks that
can be made deterministic; the inspection of the real published servability answer is reported beside
them in the F report, because a specimen is evidence and a test is a rule.

WHAT THIS FILE EXISTS TO CATCH. Until 2026-08-26 a fresh answer entered the public collection the
moment it was generated. The architecture that replaced that has four states in one table —
provisional, rejected, reviewed-and-published, and reviewed-with-a-different-published-text — and the
failure mode of any such table is LEAKAGE: one unpublished row rendering as though a human had put
datumwise's name on it. So the tests are written from the reader's side, asserting what a reader can
and cannot see, rather than from the writer's side asserting that the right column was set.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ask import standing, store  # noqa: E402


def _mk(question: str, answer: str = "A provisional answer.") -> str:
    return store.save_qa(
        question=question, answer=answer, provider="test", model="test:model", external=[],
        sources=[{"cite": "S1", "label": "Analytical Governance: From User Intent to Governed Analytical Execution",
                  "labelAtAnswer": "Analytical Governance: From User Intent to Governed Analytical Execution",
                  "heading": "4. The servability gap", "layer": "core",
                  "sourceId": "s-analytical-governance",
                  "readableRecordId": "w-analytical-governance.r03",
                  "currentRecordIdAtAnswer": "w-analytical-governance.r03",
                  "standingTemplate": "{CURRENT}; deposited text",
                  "standing": "current record v2.0 (2026-08-26); deposited text",
                  "standingAtAnswer": "current record v2.0 (2026-08-26); deposited text"}],
        evidence=[{"cite": "S1", "heading": "4. The servability gap", "layer": "core",
                   "standing": "current", "text": "Servable = Support Sufficient AND Analytically Established"}],
    )


def _review(qid: str, disposition: str = "APPROVE") -> str:
    return store.save_review(qid, {"disposition": disposition, "summary": "sound", "changes": [],
                                   "findings": {"core_support": {"ok": True, "note": "traces to S1"}},
                                   "proposedAnswer": None, "model": "test:model", "costUsd": 0.0,
                                   "quoteFacts": [], "quoteFactsAsSent": "  (no direct quotations)"})


# ── leakage, in both directions ───────────────────────────────────────────────────────────────────

def test_only_reviewed_and_published_objects_reach_the_public_collection():
    """The one that matters. A provisional answer, a rejected answer and a reviewed-but-unpublished
    answer are all invisible to a reader; only the published one is in the collection."""
    provisional = _mk("Does a provisional answer reach the public collection?")
    reviewed_unpublished = _mk("Does a reviewed answer publish itself?")
    _review(reviewed_unpublished)
    rejected = _mk("Does a rejected answer stay public?")
    _review(rejected, "DO_NOT_PUBLISH")
    store.reject(rejected, "reviewer", "not worth publishing")
    published = _mk("Does a published answer reach the public collection?")
    _review(published)
    store.publish(published, "reviewer")

    ids = {i["id"] for i in store.listing(limit=200)}
    assert published in ids
    assert provisional not in ids, "a provisional answer leaked into the public collection"
    assert reviewed_unpublished not in ids, "a review published an answer without a human"
    assert rejected not in ids, "a rejected answer stayed public"


def test_a_provisional_object_never_wears_a_reviewed_notice():
    qid = _mk("What does a reader see on an unreviewed answer?")
    row = store.get(qid)
    assert row["standing"] == standing.PROVISIONAL
    assert row["published"] is False
    assert row["notice"]["label"].startswith("Provisional answer")
    assert "not been reviewed" in row["notice"]["detail"]
    assert row["notice"]["reviewedAt"] is None


def test_publishing_writes_the_reviewed_standing_a_date_and_the_published_text():
    qid = _mk("What changes when a human publishes?")
    _review(qid)
    out = store.publish(qid, "huayin", "The text a human approved.")
    assert out is not None
    row = store.get(qid)
    assert row["standing"] == standing.REVIEWED and row["published"] is True
    assert row["notice"]["label"].startswith("Reviewed by datumwise · ")
    assert row["notice"]["reviewedAt"] is not None
    # BOTH texts survive: what a reader sees, and what the agent actually said.
    assert row["answer"] == "The text a human approved."
    assert row["provisionalAnswer"] == "A provisional answer."


def test_publishing_the_provisional_text_unchanged_is_still_two_fields():
    """The common case — APPROVE, publish as-is. `answer` and `provisionalAnswer` are then equal in
    value and still separate in kind; a later edit must not be able to rewrite the record of what
    was said."""
    qid = _mk("What if the provisional text is published unchanged?")
    _review(qid)
    store.publish(qid, "huayin")
    row = store.get(qid)
    assert row["answer"] == row["provisionalAnswer"] == "A provisional answer."


# ── reputation ────────────────────────────────────────────────────────────────────────────────────

def test_reputation_exists_only_on_reviewed_objects():
    """Votes are useful signal for a reviewer, so they are collected on a provisional answer — and
    stars, ratings and views stay NULL until a human has published it, because a reputation on an
    unreviewed answer reads as an endorsement."""
    qid = _mk("Can an unreviewed answer have stars?")
    store.vote(qid, "voter-1", True)
    store.vote(qid, "voter-2", True)
    store.get(qid, bump_view=True)
    row = store.get(qid)
    assert row["stars"] is None and row["ratings"] is None and row["views"] is None
    assert row["up"] == 2                     # the signal is kept, just not published

    _review(qid)
    store.publish(qid, "huayin")
    row = store.get(qid)
    assert row["ratings"] == 2 and row["stars"] == 5.0
    assert isinstance(row["views"], int)


def test_a_rejected_object_keeps_its_evidence_and_loses_its_audience():
    qid = _mk("Is a rejected answer erased?")
    _review(qid, "DO_NOT_PUBLISH")
    store.reject(qid, "reviewer", "thin")
    row = store.get(qid)
    assert row["provisionalAnswer"] == "A provisional answer."   # the record survives
    assert row["published"] is False
    assert qid not in {i["id"] for i in store.listing(limit=200)}


# ── what a published citation shows a reader ──────────────────────────────────────────────────────

def test_a_published_citation_shows_current_presentation_and_preserves_the_historical_one():
    """The durable-citation contract, seen from the public surface: the reader gets the label and
    standing that are true now, and the record of what was shown when the answer was written is still
    there beneath it."""
    qid = _mk("What does a reader see on a citation after the label was renamed?")
    _review(qid)
    store.publish(qid, "huayin")
    s = store.get(qid)["sources"][0]
    assert s["label"] == "Analytical Governance"                       # resolved now
    assert s["labelAtAnswer"].endswith("Governed Analytical Execution")  # shown then
    assert s["labelChangedSinceAnswer"] is True
    assert s["supersededSinceAnswer"] is False                         # a rename is not a supersession
    assert s["readableRecordId"] == "w-analytical-governance.r03"
    assert "v2.0" in s["standing"] and "22115819" in s["standing"]
    assert s["standingAtAnswer"] == "current record v2.0 (2026-08-26); deposited text"


def test_review_provenance_is_reachable_from_a_published_object():
    """A reader can be shown the verdict behind a published answer, and the reviewer's
    quote-verification facts are part of that record rather than a runtime artefact."""
    qid = _mk("Can the review behind a published answer be read?")
    rid = _review(qid)
    store.publish(qid, "huayin")
    r = store.latest_review(qid)
    assert r["id"] == rid and r["disposition"] == "APPROVE"
    assert r["quoteFactsRecorded"] is True and r["quoteFacts"] == []
    assert r["quoteFactsReconstructed"] is False
    assert "no direct quotations" in r["quoteFactsAsSent"]

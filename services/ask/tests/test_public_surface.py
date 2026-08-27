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
    # DERIVED, not typed: the assertion reads the current record out of the registry, so it stays
    # true across the next deposit instead of pinning a recid fragment the echo audit cannot see.
    from ask import citations
    _, current_by_work = citations._records()  # noqa: SLF001
    assert current_by_work["w-analytical-governance"]["doi"] in s["standing"]
    assert f"v{current_by_work['w-analytical-governance']['version']}" in s["standing"]
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


# ── view counting: public readership vs pre-publication reads ─────────────────────────────────────
#
# Huayin, 2026-08-26: "Public `views` should count public reads after publication.
# Pre-publication/provisional/reviewer reads should not appear as public readership on the reviewed
# object. If internal/review read counts are useful, preserve them separately."
#
# The defect these pin was found by inspection, not by a test: the published servability answer showed
# `views: 2` and BOTH reads were a reviewer's own before/after inspection of a still-provisional
# object. The counter was right about how many times the row had been fetched and wrong about what it
# was called. So these tests are written from the counter's side — which one moved, and by how much —
# because "did a reader read this?" is exactly the question `views` was answering incorrectly.

def _counts(qid: str) -> tuple[int, int]:
    """The two raw counters, straight from the row. Not through any rendering."""
    with store.connect() as c:
        r = c.execute("SELECT views, provisional_views FROM qa WHERE id=?", (qid,)).fetchone()
    return r["views"], r["provisional_views"]


def test_a_pre_publication_read_is_not_counted_as_public_readership():
    """The servability case, as a rule. Two reads of a provisional object leave `views` at zero."""
    qid = _mk("Does a reviewer's own read make an unpublished answer look read?")
    store.get(qid, bump_view=True)
    store.get(qid, bump_view=True)
    views, provisional = _counts(qid)
    assert views == 0, "a pre-publication read was counted as public readership"
    assert provisional == 2, "a pre-publication read was thrown away instead of kept separately"


def test_a_read_after_publication_is_counted_as_public_readership():
    """And the pre-publication count does not move again, so the two are never confused."""
    qid = _mk("Does a read after publication count?")
    store.get(qid, bump_view=True)                      # one provisional read
    _review(qid)
    store.publish(qid, "huayin")
    store.get(qid, bump_view=True)                      # one public read
    views, provisional = _counts(qid)
    assert views == 1, "a read of a published object was not counted as public readership"
    assert provisional == 1, "publication rewrote the pre-publication count"


def test_every_read_increments_exactly_one_counter():
    """The invariant that makes the split lossless: `views + provisional_views` is every read the
    service served, whichever side of publication it fell on. Neither double-counted nor dropped."""
    qid = _mk("Is any read lost or counted twice?")
    for _ in range(3):
        store.get(qid, bump_view=True)
    _review(qid)
    store.publish(qid, "huayin")
    for _ in range(4):
        store.get(qid, bump_view=True)
    views, provisional = _counts(qid)
    assert (views, provisional) == (4, 3)
    assert views + provisional == 7


def test_a_read_that_is_not_asked_to_count_counts_nothing():
    """`bump_view=False` is still the default, and the review surface never bumps either counter —
    opening the review screen is not readership of any kind."""
    qid = _mk("Does looking at the review screen count as a read?")
    store.get(qid)
    store.get_for_review(qid)
    assert _counts(qid) == (0, 0)


def test_the_public_payload_never_carries_a_pre_publication_read_count():
    """The leakage check, in the shape this file uses for every other private field: not "is the
    number right" but "can a reader see it at all". Checked on all three public renderings."""
    qid = _mk("Can a reader see how often a reviewer looked at this?")
    store.get(qid, bump_view=True)
    store.cache_put("Can a reader see how often a reviewer looked at this?", qid, "test:model")
    _review(qid)
    store.publish(qid, "huayin")
    store.get(qid, bump_view=True)

    for surface, payload in (
        ("GET /qa/<id>", store.get(qid)),
        ("the cache serve", store.find_cached("Can a reader see how often a reviewer looked at this?")),
        ("the public collection", next(i for i in store.listing(limit=500) if i["id"] == qid)),
    ):
        assert payload is not None
        assert "provisionalViews" not in payload, f"{surface} leaked the pre-publication read count"
        assert "provisional_views" not in payload, f"{surface} leaked the pre-publication read count"
        assert payload["views"] == 1, f"{surface} reported a view count that includes a reviewer's read"


def test_the_review_surface_does_see_the_pre_publication_read_count():
    """Preserved separately means preserved somewhere a human can read it. The review payload —
    /review/item/<id>, behind the review token — is that somewhere."""
    qid = _mk("Can a reviewer see how often this was read before publication?")
    store.get(qid, bump_view=True)
    store.get(qid, bump_view=True)
    item = store.get_for_review(qid)
    assert item is not None and item["provisionalViews"] == 2
    assert item["views"] is None                       # still no public reputation on a provisional row
    assert qid in {i["id"] for i in store.review_queue(limit=500)}
    queued = next(i for i in store.review_queue(limit=500) if i["id"] == qid)
    assert queued["provisionalViews"] == 2


def test_migrating_an_existing_database_does_not_rewrite_its_view_counts(tmp_path):
    """"Do not silently rewrite historical metrics." A database written before this column existed
    gains it at 0 and keeps every `views` it already had — the pre-existing counts are left exactly
    where they are, to be corrected (or not) by a human ruling rather than by a migration.

    Runs against its own file, so it asserts the migration and not the ambient database.
    """
    import sqlite3 as _sqlite3
    old = tmp_path / "pre-column.db"
    con = _sqlite3.connect(old)
    con.executescript(store.SCHEMA)                     # the schema WITHOUT provisional_views
    con.execute(
        "INSERT INTO qa (id, question, question_key, answer, created_at, provider, model, sources, "
        "views, standing, published, reviewed_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        ("legacy1", "An answer from before the split", "an answer from before the split",
         "text", 1787771751.0, "test", "test:model", "[]", 7, standing.REVIEWED, 1, 1787771751.0),
    )
    con.commit()
    assert "provisional_views" not in {r[1] for r in con.execute("PRAGMA table_info(qa)")}
    con.close()

    original = store.DB_PATH
    store.DB_PATH = old
    try:
        row = store.get("legacy1")                      # connect() migrates on the way in
        assert row["views"] == 7, "the migration rewrote a historical view count"
        with store.connect() as c:
            r = c.execute("SELECT views, provisional_views FROM qa WHERE id='legacy1'").fetchone()
        assert (r["views"], r["provisional_views"]) == (7, 0)
    finally:
        store.DB_PATH = original

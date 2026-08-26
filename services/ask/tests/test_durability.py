"""F3 — THE DURABILITY INVARIANT, tested across an explicit registry move.

Approved 2026-08-26 16:35, item 6. No model call, no network: this is a `pytest`, not an evaluation,
because the thing under test is a split rather than a judgement.

    Identity is durable. Current presentation is resolved. Historical presentation is preserved.

WHY A MOVE HAS TO BE SIMULATED. Every piece of this machinery was built AFTER a registry move and
verified by reading its output once. That is not a test of the move — it is a reading of one moment.
So these tests apply a synthetic move to a real stored answer and assert what changed, what did not,
and above all which of those two lists each field belongs to. The two failure modes named in the
ruling are the two the assertions are written against:

    · a CURRENT PRESENTATION string carried as though it were identity
    · HISTORICAL PRESENTATION silently rewritten

THE MOVE IS SYNTHETIC AND THE REGISTRY IS UNTOUCHED. `citations._records` and `citations._naming`
are the only two readers of the registry inside the resolution path, so the move is applied by
substituting what those two functions return. Editing registry/ to run a test would make the test a
migration, and a test that mutates the source of truth is not one.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from ask import citations, quotes, store  # noqa: E402

# ── the world before and after ────────────────────────────────────────────────────────────────────
#
# One work, two records. BEFORE: r01 is current and is the record the answer cites. AFTER: r02 exists
# and is current, and the work's editorial label has been renamed. Both moves at once, deliberately:
# a supersession and a rename are different facts and the test's whole job is that they stay
# different.

WORK = "w-fixture-work"
R01 = {"recordId": f"{WORK}.r01", "workId": WORK, "title": "A Fixture Paper: The First Subtitle",
       "version": "1.0", "date": "2026-08-01", "doi": "10.5281/zenodo.90000001",
       "recid": "90000001", "status": "current"}
R02 = {"recordId": f"{WORK}.r02", "workId": WORK, "title": "A Fixture Paper: A Different Subtitle",
       "version": "2.0", "date": "2026-08-20", "doi": "10.5281/zenodo.90000002",
       "recid": "90000002", "status": "current", "supersedes": f"{WORK}.r01"}

SOURCE = {"sourceId": "s-fixture", "workId": WORK, "role": "foundation"}

LABEL_BEFORE = "A Fixture Paper: The First Subtitle"
LABEL_AFTER = "A Fixture Paper"


def _install(monkeypatch, records: list[dict], label: str) -> None:
    by_id = {r["recordId"]: r for r in records}
    current = {r["workId"]: r for r in records if r["status"] == "current"}
    monkeypatch.setattr(citations, "_records", lambda: (by_id, current))
    monkeypatch.setattr(citations, "_naming",
                        lambda: ({SOURCE["sourceId"]: SOURCE}, {WORK: label}))


def _before(monkeypatch):
    _install(monkeypatch, [dict(R01)], LABEL_BEFORE)


def _after(monkeypatch):
    superseded = {**R01, "status": "superseded"}
    _install(monkeypatch, [superseded, dict(R02)], LABEL_AFTER)


def _answer_with_a_citation() -> str:
    """A stored answer whose citation is, at write time, both current and correctly labelled."""
    return store.save_qa(
        question="What does the fixture paper establish?",
        answer=('The fixture paper establishes that "a fixture is not a fact" and nothing more [S1].'),
        provider="test", model="test:model", external=[],
        sources=[{
            "cite": "S1",
            "label": LABEL_BEFORE,
            "labelAtAnswer": LABEL_BEFORE,
            "heading": "1. What a fixture is",
            "layer": "core",
            "sourceId": SOURCE["sourceId"],
            "readableRecordId": R01["recordId"],
            "currentRecordIdAtAnswer": R01["recordId"],
            "standingTemplate": "{CURRENT}; deposited text",
            "standing": "current record v1.0 (2026-08-01, doi:10.5281/zenodo.90000001); deposited text",
            "standingAtAnswer": "current record v1.0 (2026-08-01, doi:10.5281/zenodo.90000001); deposited text",
        }],
        evidence=[{"cite": "S1", "label": LABEL_BEFORE, "heading": "1. What a fixture is",
                   "layer": "core", "standing": "current",
                   "text": "A fixture is not a fact. It stands in for one."}],
    )


# ── the invariant ─────────────────────────────────────────────────────────────────────────────────

MUST_CHANGE = ("standing", "label", "supersededSinceAnswer", "labelChangedSinceAnswer")
MUST_NOT_CHANGE = ("readableRecordId", "currentRecordIdAtAnswer", "standingAtAnswer",
                   "labelAtAnswer", "sourceId", "cite", "heading", "layer")


def test_a_registry_move_changes_presentation_and_only_presentation(monkeypatch):
    """The whole invariant, in one test, across one move that supersedes AND renames."""
    qid = _answer_with_a_citation()
    facts = quotes.verify(store.get(qid)["answer"], store.get(qid)["evidence"])
    rid = store.save_review(qid, {
        "disposition": "APPROVE", "summary": "sound", "changes": [],
        "findings": {"core_support": {"ok": True, "note": "traces to S1"},
                     "currency": {"ok": True, "note": "current at the time"}},
        "proposedAnswer": None, "model": "test:model", "costUsd": 0.0,
        "quoteFacts": facts, "quoteFactsAsSent": quotes.format_facts(facts),
    })

    _before(monkeypatch)
    before = store.get(qid)
    before_review = store.latest_review(qid)
    b = before["sources"][0]
    assert b["label"] == LABEL_BEFORE
    assert b["supersededSinceAnswer"] is False and b["labelChangedSinceAnswer"] is False

    _after(monkeypatch)
    after = store.get(qid)
    after_review = store.latest_review(qid)
    a = after["sources"][0]

    # MUST CHANGE — current standing, current presentation, and the two derived flags.
    assert a["standing"] != b["standing"]
    assert "v2.0" in a["standing"] and "90000002" in a["standing"]
    assert a["label"] == LABEL_AFTER != b["label"]
    assert a["supersededSinceAnswer"] is True
    assert a["labelChangedSinceAnswer"] is True
    assert a["currentRecordId"] == R02["recordId"]
    for field in MUST_CHANGE:
        assert a[field] != b[field], f"{field} is in MUST CHANGE and did not move"

    # MUST NOT CHANGE — every identity, and every presentation string captured at answer time.
    for field in MUST_NOT_CHANGE:
        assert a[field] == b[field], f"{field} is in MUST NOT CHANGE and moved"
    assert a["standingAtAnswer"] == b["standingAtAnswer"] == \
        "current record v1.0 (2026-08-01, doi:10.5281/zenodo.90000001); deposited text"
    assert a["labelAtAnswer"] == LABEL_BEFORE

    # The answer, the provisional answer, and the whole review record are historical facts.
    assert after["answer"] == before["answer"]
    assert after["provisionalAnswer"] == before["provisionalAnswer"]
    assert after_review == before_review, "a registry move rewrote part of the review record"
    assert after_review["quoteFacts"] == facts
    assert after_review["quoteFactsAsSent"] == before_review["quoteFactsAsSent"]
    assert after_review["disposition"] == "APPROVE"
    assert after_review["findings"] == before_review["findings"]
    assert after_review["id"] == rid


def test_the_stored_row_is_never_rewritten_by_a_move(monkeypatch):
    """Re-resolution happens on the way OUT. If a move can edit the stored bytes, then 'preserved'
    is a description of a moment rather than a property, and the next move erases this one."""
    qid = _answer_with_a_citation()
    with store.connect() as c:
        raw_before = c.execute("SELECT sources, answer FROM qa WHERE id=?", (qid,)).fetchone()
        snapshot = (raw_before["sources"], raw_before["answer"])

    _before(monkeypatch)
    store.get(qid)
    _after(monkeypatch)
    store.get(qid)          # the read that does the re-resolving

    with store.connect() as c:
        raw_after = c.execute("SELECT sources, answer FROM qa WHERE id=?", (qid,)).fetchone()
    assert (raw_after["sources"], raw_after["answer"]) == snapshot
    # and the stored row still carries the ORIGINAL presentation, not the resolved one
    stored = json.loads(raw_after["sources"])[0]
    assert stored["label"] == LABEL_BEFORE
    assert stored["standing"].startswith("current record v1.0")


_VERSION_ISH = re.compile(r"\bv?\d+\.\d+\b|10\.5281/zenodo\.\d+|\b20\d\d-\d\d-\d\d\b")


def test_no_identity_field_carries_a_presentation_string(monkeypatch):
    """The failure mode the ruling names first: a current presentation string carried as though it
    were identity. An identity field is a locally minted id and nothing else — no version, no date,
    no DOI. If a version string ever appears in one, a rename or a redeposit silently invalidates
    every stored reference, which is the defect this whole architecture removes."""
    qid = _answer_with_a_citation()
    _after(monkeypatch)
    s = store.get(qid)["sources"][0]
    for field in ("sourceId", "readableRecordId", "currentRecordIdAtAnswer", "currentRecordId"):
        value = s[field]
        assert isinstance(value, str) and value
        assert not _VERSION_ISH.search(value), f"{field} carries a presentation string: {value!r}"
        assert re.fullmatch(r"[a-z0-9-]+(\.r\d+)?", value), f"{field} is not a minted id: {value!r}"


def test_a_rename_alone_is_not_a_supersession(monkeypatch):
    """The two flags must not collapse. Rename the label and move nothing else: the label changes,
    the supersession flag does not, and the cited record is untouched."""
    qid = _answer_with_a_citation()
    _before(monkeypatch)
    _install(monkeypatch, [dict(R01)], LABEL_AFTER)     # rename only; r01 is still current
    s = store.get(qid)["sources"][0]
    assert s["labelChangedSinceAnswer"] is True
    assert s["supersededSinceAnswer"] is False
    assert s["readableRecordId"] == s["currentRecordId"] == R01["recordId"]
    assert s["standing"].startswith("current record v1.0")


def test_a_supersession_alone_is_not_a_rename(monkeypatch):
    """The mirror case, and the one a careless implementation gets wrong: move the current record and
    keep the label. Standing moves, the label does not, and both flags say so independently."""
    qid = _answer_with_a_citation()
    _install(monkeypatch, [{**R01, "status": "superseded"}, dict(R02)], LABEL_BEFORE)
    s = store.get(qid)["sources"][0]
    assert s["supersededSinceAnswer"] is True
    assert s["labelChangedSinceAnswer"] is False
    assert s["label"] == s["labelAtAnswer"] == LABEL_BEFORE
    assert "v2.0" in s["standing"] and s["standingAtAnswer"].startswith("current record v1.0")


def test_historical_evidence_survives_a_move_that_changes_everything_else(monkeypatch):
    """`evidence` is the passage text the answer was actually built on — the thing a reviewer
    verifies quotations against. A move must not touch it, or a later reader would be checking the
    answer against evidence it never saw."""
    qid = _answer_with_a_citation()
    _before(monkeypatch)
    ev_before = store.get(qid)["evidence"]
    _after(monkeypatch)
    ev_after = store.get(qid)["evidence"]
    assert ev_after == ev_before
    assert ev_after[0]["text"].startswith("A fixture is not a fact")
    # and the quote facts computed from it are stable, which is what makes reconstruction sound
    assert quotes.verify(store.get(qid)["answer"], ev_after) == \
           quotes.verify(store.get(qid)["answer"], ev_before)

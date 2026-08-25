"""Hermetic tests — no API key, no network. Everything here runs in CI.

The model call is the one thing not tested here (it needs a key and costs money); the eval harness
covers that separately and its results are committed. What IS tested is every mechanism that decides
whether a model's output is allowed to become a public claim — which is the part that must not
regress silently.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("ASK_DB", tempfile.mkdtemp() + "/test.db")

import pytest  # noqa: E402

from ask import retrieve, store, verify  # noqa: E402
from ask.answer import _split_answer, publishability  # noqa: E402


# ── the identifier gate — the one hard mechanism in v0 ────────────────────────────────────────────

def test_registry_has_dois():
    assert verify.registry_doi_count() > 30


def test_real_doi_passes():
    records = json.loads((Path(__file__).resolve().parents[3] /
                          "registry/publications/records.json").read_text())
    current = next(r for r in records if r.get("status") == "current" and r.get("doi"))
    out = verify.check(f"The current record is {current['doi']}, current as of today.")
    assert out["ok"], out["problems"]


def test_fabricated_doi_is_fatal():
    out = verify.check("You can find it at 10.5281/zenodo.99999999.")
    assert not out["ok"]
    assert any(p["kind"] == "unregistered-doi" for p in out["problems"])


def test_fabricated_zenodo_url_is_fatal():
    out = verify.check("See https://zenodo.org/records/12345678 for the deposit.")
    assert not out["ok"]
    assert any(p["kind"] == "unregistered-zenodo-record" for p in out["problems"])


def test_superseded_doi_unhedged_warns_but_is_not_fatal():
    records = json.loads((Path(__file__).resolve().parents[3] /
                          "registry/publications/records.json").read_text())
    sup = next((r for r in records if r.get("status") == "superseded" and r.get("doi")), None)
    if not sup:
        pytest.skip("no superseded record in the registry")
    bare = verify.check(f"The paper is at {sup['doi']}.")
    assert bare["ok"], "a superseded DOI is a warning, not a publication-blocking failure"
    assert any(p["kind"] == "superseded-doi-unhedged" for p in bare["problems"])
    hedged = verify.check(f"An earlier edition, now superseded, was deposited at {sup['doi']}.")
    assert not any(p["kind"] == "superseded-doi-unhedged" for p in hedged["problems"])


# ── the retrieval index and its standing join ─────────────────────────────────────────────────────

def test_index_is_populated():
    s = retrieve.stats()
    assert s["chunks"] > 300 and s["routes"] > 20


def test_superseded_drafts_are_not_in_the_index():
    """The four orphaned drafts in src/content/corpus/ must be unreachable.

    This is the whole reason the index is built from dist/ rather than from the source tree. If
    someone 'helpfully' repoints index_build at the corpus directory, this test is what says no.
    """
    chunks = json.loads((Path(__file__).resolve().parents[1] / "index/chunks.json").read_text())
    routes = {c["route"] for c in chunks}
    # Orphans have no route at all, so the tell is that every indexed route is a real built page.
    dist = Path(__file__).resolve().parents[3] / "apps/website/dist"
    if not dist.exists():
        pytest.skip("no site build present")
    for r in routes:
        built = dist / (r.lstrip("/") or "index.html")
        assert (built / "index.html").exists() or built.with_suffix(".html").exists() \
            or (dist / "index.html").exists(), f"indexed route {r} has no built page"


def test_every_chunk_carries_standing():
    chunks = json.loads((Path(__file__).resolve().parents[1] / "index/chunks.json").read_text())
    assert all(c["standing"] for c in chunks), "a passage without standing must never be retrievable"


def test_historical_passages_are_labelled_and_demoted():
    hits = retrieve.search("research corpus map August 2026", k=8)
    hist = [h for h in hits if h["isHistorical"]]
    assert hist, "the preserved map should still be findable for a historical question"
    for h in hist:
        assert "PRESERVED HISTORICAL STATE" in h["standing"]


def test_edition_pinned_passages_say_so():
    chunks = json.loads((Path(__file__).resolve().parents[1] / "index/chunks.json").read_text())
    pinned = [c for c in chunks if c["isEditionPinned"]]
    assert pinned
    for c in pinned:
        assert "EDITION-PINNED" in c["standing"] and "NOT the current record" in c["standing"]


def test_current_outranks_historical_on_a_current_question():
    hits = retrieve.search("what is the current source estate", k=5)
    assert hits and not hits[0]["isHistorical"]


# ── ranking, stars, and the public/private rule ───────────────────────────────────────────────────

def test_stars_match_the_specified_mapping():
    assert store.stars(10, 0) == 5.0     # 100% -> 5.0
    assert store.stars(9, 1) == 4.5      #  90% -> 4.5
    assert store.stars(8, 2) == 4.0      #  80% -> 4.0
    assert store.stars(0, 0) is None     # no votes -> no score, never 0.0


def test_more_views_rank_higher_all_else_equal():
    assert store.rank(100, 0, 0) > store.rank(10, 0, 0) > store.rank(1, 0, 0)


def test_helpfulness_breaks_ties_but_does_not_dominate_views():
    # equal views, better up-rate wins
    assert store.rank(100, 9, 1) > store.rank(100, 5, 5)
    # A 100x view gap cannot be overturned by helpfulness at all: the bonus range is +-0.5, i.e.
    # exactly one order of magnitude of views, so two orders are out of its reach.
    assert store.rank(1000, 0, 10) > store.rank(10, 10, 0)
    # At EXACTLY a 10x gap, unanimous feedback CAN overturn it — and should. An answer that ten out
    # of ten readers called unhelpful belongs below a well-rated one even with ten times the views.
    # This is the rule's designed edge, recorded here so a future change to MIN_RATINGS_FOR_BONUS or
    # the bonus range is a deliberate decision rather than an accident.
    assert store.rank(10, 10, 0) > store.rank(100, 0, 10)
    # ...but a merely mediocre score does not do it. Only the extremes reach that far.
    assert store.rank(100, 4, 6) > store.rank(10, 10, 0)


def test_fewer_than_three_ratings_gets_no_bonus_or_penalty():
    base = store.rank(50, 0, 0)
    assert store.rank(50, 2, 0) == base   # two thumbs-up cannot crown it
    assert store.rank(50, 0, 2) == base   # one thumbs-down cannot bury it
    assert store.rank(50, 3, 0) > base    # at three, we start having a view


def test_publishability_withholds_personal_and_abusive_questions():
    assert publishability("What is a measure family?")[0]
    assert not publishability("email me at bob@example.com about this")[0]
    assert not publishability("my company uses snowflake, what should we do")[0]
    assert not publishability("hi")[0]


def test_publishability_allows_a_normal_comparison_question():
    ok, why = publishability("How does Columna compare with dbt MetricFlow?")
    assert ok, why


# ── answer parsing ────────────────────────────────────────────────────────────────────────────────

def test_split_answer_extracts_trailing_json():
    body, meta = _split_answer('The answer [S1].\n\n```json\n{"used":["S1"],"external":[],'
                               '"corpus_settles":true}\n```')
    assert body == "The answer [S1]."
    assert meta["used"] == ["S1"] and meta["corpus_settles"] is True


def test_split_answer_reports_missing_json_rather_than_guessing():
    body, meta = _split_answer("Just prose, no block.")
    assert meta.get("_missing") is True and meta["used"] == []


# ── storage round-trip ────────────────────────────────────────────────────────────────────────────

def test_cache_and_vote_round_trip():
    qid = store.save_qa(question="What is a universe, exactly?", answer="One population of facts.",
                        provider="test", model="test:model", sources=[], external=[])
    assert store.find_cached("what is a universe, exactly")["id"] == qid  # normalised reuse
    out = store.vote(qid, "voter-a", True)
    assert out["up"] == 1 and out["ratings"] == 1 and out["stars"] == 5.0
    out = store.vote(qid, "voter-a", False)  # same voter changes their mind, not a second vote
    assert out["ratings"] == 1 and out["down"] == 1
    out = store.vote(qid, "voter-b", True)
    assert out["ratings"] == 2


# ── the observed output-contract failure, pinned ──────────────────────────────────────────────────
# 2026-08-25: gpt-5 closed with the JSON object and NO ```json fence on the first edition-pinned
# question asked through the live service. Every citation was dropped and an answer shipped with no
# receipts. These four tests exist so that specific regression cannot recur silently.

from ask.answer import _resolve_used  # noqa: E402


def test_bare_json_tail_without_a_fence_is_parsed():
    body, meta = _split_answer(
        'The answer [S3].\n\n{"used": ["S3", "S4"], "external": [], "corpus_settles": true}'
    )
    assert body == "The answer [S3]."
    assert meta["used"] == ["S3", "S4"], "an unfenced block must still be read"


def test_citations_are_recovered_from_prose_when_the_block_is_lost():
    body = "Claim one [S3]. Claim two [S7]."
    tokens, recovered = _resolve_used(body, {"used": []})
    assert tokens == ["S3", "S7"]
    assert recovered is True


def test_block_and_prose_are_unioned_not_chosen_between():
    body = "Only S3 is marked inline [S3]."
    tokens, recovered = _resolve_used(body, {"used": ["S5"]})
    assert tokens == ["S3", "S5"], "a source used but not marked inline must not be lost either"
    assert recovered is False


def test_tokens_sort_numerically_not_lexically():
    tokens, _ = _resolve_used("[S10] and [S2]", {"used": []})
    assert tokens == ["S2", "S10"]

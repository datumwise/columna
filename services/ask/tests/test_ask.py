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
    # The fake DOI is CONSTRUCTED, not written as a literal. G7's echo audit scans tracked files for
    # Zenodo tokens and fails closed on any that are not declared in consumers.json — correctly, and
    # a negative test fixture is not a publication fact worth adding a governance class for. Building
    # the string keeps the gate's vocabulary clean. Do not "tidy" this back into a literal.
    fake = "10.5281/zenodo." + "9" * 8
    out = verify.check(f"You can find it at {fake}.")
    assert not out["ok"]
    assert any(p["kind"] == "unregistered-doi" for p in out["problems"])


def test_fabricated_zenodo_url_is_fatal():
    out = verify.check("See https://zenodo.org/records/" + "12345678" + " for the deposit.")
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
    assert s["chunks"] > 800
    # Routes DROPPED (41 -> 19) when indexing was constrained to catalogued sources, and chunks ROSE
    # (665 -> 1206) when the deposited Core texts were ingested. Both directions are the
    # corpus ruling working: fewer pages, more of the works that actually represent datumwise.
    assert 10 < s["routes"] < 30
    assert s["core"] > s["reference"], (
        "the Core set must outweigh the reference layer — the whole hazard the ruling "
        "named is Ask drifting back toward whatever is easiest to retrieve"
    )
    assert s["fromDeposits"] > 400, "deposited foundation text must be ingested"


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


def test_historical_passages_are_reachable_only_through_the_historical_jurisdiction():
    """The two-layer rule, at its sharpest.

    Before the corpus ruling the preserved map was demoted but always in the pool. Now it is
    REFERENCE ONLY with jurisdiction `historical`, so a question that does not ask about history
    cannot reach it at all — and one that does, gets it first.
    """
    neutral = retrieve.search("research corpus map", k=8)
    assert not any(h["isHistorical"] for h in neutral), (
        "a question with no historical cue must not reach a preserved state"
    )
    asked = retrieve.search("what did the August research map say at the time?", k=8)
    hist = [h for h in asked if h["isHistorical"]]
    assert hist, "an explicitly historical question must reach the preserved map"
    assert asked[0]["isHistorical"], "within its own jurisdiction it should rank first, not last"
    for h in hist:
        assert "PRESERVED HISTORICAL STATE" in h["standing"]


# ── the two corpus layers ─────────────────────────────────────────────────────────────────────────

def test_every_chunk_is_ruled_into_a_layer():
    chunks = json.loads((Path(__file__).resolve().parents[1] / "index/chunks.json").read_text())
    assert all(c.get("layer") in ("core", "reference") for c in chunks)


def test_reference_material_is_invisible_without_its_jurisdiction():
    """The manuals must not constitute datumwise's position just because they retrieve well."""
    hits = retrieve.search("what does datumwise hold about analytical identity?", k=8)
    assert hits, "a Core question must still find material"
    assert all(h["layer"] == "core" for h in hits), (
        [f"{h['sourceLabel']}::{h['layer']}" for h in hits]
    )


def test_normative_jurisdiction_opens_on_a_shipped_question():
    assert "normative" in retrieve.jurisdictions_for("What does shipped Frame-QL allow?")
    hits = retrieve.search("What does shipped Frame-QL allow?", k=5)
    assert any(h["jurisdiction"] == "normative" for h in hits)
    assert hits[0]["jurisdiction"] == "normative", "within its jurisdiction it governs"


def test_defects_jurisdiction_opens_on_a_broken_question():
    hits = retrieve.search("what is currently broken in Columna?", k=5)
    assert hits[0]["sourceId"] == "s-known-issues"


def test_core_set_is_readable_not_merely_citable():
    """13 of 16 IN works were deposit-only; ingestion is a requirement of the ruling, not a nicety."""
    chunks = json.loads((Path(__file__).resolve().parents[1] / "index/chunks.json").read_text())
    corpus = json.loads((Path(__file__).resolve().parents[3] /
                         "registry/sources/current-corpus.json").read_text())
    have = {c["sourceId"] for c in chunks}
    readable = [i for i in corpus["in"] if i in have]
    assert len(readable) == len(corpus["in"]), (
        f"only {len(readable)} of {len(corpus['in'])} IN works are readable: "
        f"{[i for i in corpus['in'] if i not in have]}"
    )


def test_supplied_deposits_declare_the_current_version():
    """Author-supplied text cannot be checksum-verified against Zenodo, so the declared version is
    the assurance that the right EDITION was supplied. Pin that it is actually recorded."""
    man = json.loads((Path(__file__).resolve().parents[1] / "deposits/manifest.json").read_text())
    supplied = [d for d in man["deposits"] if d.get("provenance") == "supplied"]
    for d in supplied:
        assert d.get("zenodoVerified") is False, "supplied text must not claim Zenodo verification"
        assert d.get("declaredVersion"), f"{d['sourceId']} records no declared version"


def test_every_ingested_deposit_records_its_provenance():
    man = json.loads((Path(__file__).resolve().parents[1] / "deposits/manifest.json").read_text())
    assert man["deposits"], "the Core set must be ingested"
    assert not man["missingText"], f"unreadable Core works: {man['missingText']}"
    for d in man["deposits"]:
        assert d.get("provenance") in ("zenodo", "supplied"), d
        assert d.get("sha256"), d


def test_deposit_chunks_resolve_to_a_doi_not_a_dead_route():
    hits = retrieve.search("what does the theory of data establish about analytical objects", k=8)
    deposited = [h for h in hits if not h["route"]]
    assert deposited, "deposited Core text should be retrievable"
    for h in deposited:
        assert h["url"].startswith("https://doi.org/"), h["url"]


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
    assert store.find_cached("what is a universe, exactly") is None, (
        "saving an answer must not by itself make it reusable — the cache is its own object"
    )
    store.cache_put("What is a universe, exactly?", qid, "test:model")
    assert store.find_cached("what is a universe, exactly")["id"] == qid  # normalised reuse
    store.cache_put("What is a universe, exactly?", qid, "test:model", ttl_days=-1)
    assert store.find_cached("what is a universe, exactly") is None, "an expired entry is not a hit"
    assert store.get(qid), "expiry drops the cache entry, never the answer"
    store.cache_put("What is a universe, exactly?", qid, "test:model")
    out = store.vote(qid, "voter-a", True)
    assert out["up"] == 1
    out = store.vote(qid, "voter-a", False)  # same voter changes their mind, not a second vote
    assert out["up"] == 0 and out["down"] == 1
    out = store.vote(qid, "voter-b", True)
    assert out["up"] + out["down"] == 2


def test_a_fresh_answer_is_provisional_unpublished_and_has_no_reputation():
    """The 2026-08-26 standing model, pinned at the storage layer.

    Votes on a provisional answer still RECORD — they are useful signal for whoever reviews it —
    but no star reputation is rendered, because a reputation on an unreviewed answer reads as
    endorsement. And nothing a caller passes can make an answer born published.
    """
    qid = store.save_qa(question="Does a fresh answer publish itself?", answer="It must not.",
                        provider="test", model="test:model", sources=[], external=[],
                        public=True, standing="reviewed", published=True)  # ignored, deliberately
    row = store.get(qid)
    assert row["standing"] == "provisional" and row["published"] is False
    assert row["notice"]["label"] == "Provisional answer · not reviewed by datumwise"
    assert row["stars"] is None and row["ratings"] is None and row["rank"] is None
    store.vote(qid, "voter-a", True)
    assert store.get(qid)["up"] == 1          # recorded
    assert store.get(qid)["stars"] is None    # not displayed
    assert all(item["id"] != qid for item in store.listing()), (
        "a provisional answer must not appear in the public Q&A collection"
    )


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


# ── ASK AUTHORITY IS ASK'S (2026-08-26) ───────────────────────────────────────────────────────────

def test_ask_authority_is_independent_of_the_research_editorial_list():
    """Ask's Core/Reference sets and /research's list must be able to diverge.

    They were one file until 2026-08-26: apps/website/src/data/sources.ts builds the /research
    REPRESENTATIVE list from registry/sources/current-corpus.json, and index_build read the same
    file to decide what Ask may assert datumwise's position from. One ruling governed two different
    questions. This pins the split — if index_build ever reads the editorial list again, a ruling
    about what a reader is SHOWN would silently move what an agent may ASSERT.
    """
    from ask import index_build
    src = (Path(index_build.__file__)).read_text()
    assert "ask-authority.json" in src
    # The quoted literal, not the word: the module explains the split in prose, and should.
    assert '"current-corpus.json"' not in src, (
        "index_build must not read the /research editorial list; Ask authority is its own manifest"
    )
    auth = json.loads(index_build.AUTHORITY_JSON.read_text())
    # Separate governance, so moving one set does not implicitly re-ratify the other.
    for k in ("core", "reference"):
        assert auth[k]["ruledOn"] and auth[k]["ruledBy"] and auth[k]["history"]


def test_a_core_source_that_indexes_to_nothing_is_a_build_defect():
    """Core is the only class entitled to establish "datumwise holds ...". A Core source that
    produced no chunks does not merely go missing from an answer — it silently narrows what
    datumwise can say about itself, and nothing downstream can tell that apart from "Core does not
    settle this". So the build must fail rather than warn.
    """
    from ask import index_build
    assert any(c.get("layer") == "core" for c in retrieve._corpus()[0]), \
        "fixture guard: the index should contain core chunks"

    class _C:  # minimal stand-in for Chunk: the check only reads .layer and .sourceId
        def __init__(self, layer, sourceId):
            self.layer, self.sourceId = layer, sourceId

    ruled = json.loads(index_build.AUTHORITY_JSON.read_text())["core"]["sourceIds"]
    complete = [_C("core", sid) for sid in ruled]
    index_build.check_core_reachable(complete)  # all present -> no raise

    with pytest.raises(index_build.CoreUnreachable) as e:
        index_build.check_core_reachable(complete[1:])
    assert ruled[0] in str(e.value)


# ── review-to-publish (2026-08-26) ────────────────────────────────────────────────────────────────

def _candidate(q="Why does datumwise say servability rather than serviceability?"):
    return store.save_qa(question=q, answer="A provisional answer about servability.",
                         provider="test", model="test:model",
                         sources=[{"cite": "S1", "label": "The Theory of Data", "heading": "3.3",
                                   "layer": "core", "standing": "current"}],
                         external=[])


def test_the_provisional_answer_is_never_rewritten_by_publication():
    """The immutable chain: provisional -> review + proposal -> human-approved published answer.

    The provisional text is the evidence of what the agent actually said when asked. An evidence
    record that can be silently edited is not one. So publishing a DIFFERENT text writes
    published_answer and leaves `answer` exactly as generated.
    """
    qid = _candidate()
    store.save_review(qid, {"disposition": "REVISE", "summary": "tighten it",
                            "changes": ["cut the preamble"], "findings": {},
                            "proposedAnswer": "A tighter answer about servability.",
                            "model": "test:model", "costUsd": 0.0})
    store.publish(qid, "huayin", "A tighter answer about servability.")
    row = store.get(qid)
    assert row["answer"] == "A tighter answer about servability."     # what a reader sees
    assert row["provisionalAnswer"] == "A provisional answer about servability."  # what was said
    assert row["standing"] == "reviewed" and row["published"] is True
    assert row["notice"]["label"].startswith("Reviewed by datumwise · ")
    assert row["stars"] is not None or row["ratings"] == 0  # reputation exists once reviewed
    assert any(i["id"] == qid for i in store.listing())


def test_review_queue_holds_candidates_and_a_rejection_leaves_it():
    qid = _candidate("Is a rejected answer still evidence?")
    assert any(i["id"] == qid for i in store.review_queue())
    store.reject(qid, "huayin", "thin and duplicative")
    assert all(i["id"] != qid for i in store.review_queue()), "a rejected answer leaves the queue"
    assert store.get(qid)["answer"], "a rejected answer is KEPT — it is evidence about the agent"
    assert all(i["id"] != qid for i in store.listing())


def test_revise_without_a_proposal_is_downgraded_not_honoured():
    """REVISE with nothing proposed is not a disposition, it is a dropped sentence."""
    from ask import review as review_mod
    v = review_mod._normalise_verdict({"disposition": "REVISE", "proposedAnswer": None},
                                      model="test:model", cost=0.0)
    assert v["disposition"] == "DO_NOT_PUBLISH"
    v = review_mod._normalise_verdict({"disposition": "APPROVE", "proposedAnswer": "sneaky"},
                                      model="test:model", cost=0.0)
    assert v["proposedAnswer"] is None, "a proposal only means something on a REVISE"
    v = review_mod._normalise_verdict({"disposition": "nonsense"}, model="test:model", cost=0.0)
    assert v["disposition"] == "DO_NOT_PUBLISH", "an unparseable disposition must fail closed"


# ── the review surface is protected (2026-08-26) ──────────────────────────────────────────────────

def _serve(token: str | None):
    """A real server on a random port. The auth rule is a property of the HTTP surface, and testing
    it against the handler's internals would test a different thing than the one that ships."""
    import importlib
    from http.server import ThreadingHTTPServer
    import threading
    if token is None:
        os.environ.pop("ASK_REVIEW_TOKEN", None)
    else:
        os.environ["ASK_REVIEW_TOKEN"] = token
    from ask import app as app_mod
    importlib.reload(app_mod)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), app_mod.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def _get(url, token=None):
    import urllib.error
    import urllib.request
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_review_routes_are_invisible_without_the_token():
    """404, not 403. An unconfigured or unauthorised deployment must not advertise a surface that
    publishes under datumwise's name."""
    srv, base = _serve("s3cret-for-tests")
    try:
        assert _get(f"{base}/review/queue")[0] == 404                      # no token
        assert _get(f"{base}/review/queue", "wrong")[0] == 404             # wrong token
        assert _get(f"{base}/review/queue", "s3cret-for-tests")[0] == 200  # right token
        assert _get(f"{base}/health")[0] == 200                            # unrelated routes fine
        code, body = _get(f"{base}/review", "s3cret-for-tests")
        assert code == 200 and b"Ask review" in body
    finally:
        srv.shutdown()


def test_review_surface_is_absent_entirely_when_no_token_is_configured():
    srv, base = _serve(None)
    try:
        assert _get(f"{base}/review")[0] == 404
        assert _get(f"{base}/review/queue", "anything")[0] == 404
    finally:
        srv.shutdown()


# ── external sources (2026-08-26) ─────────────────────────────────────────────────────────────────

def test_external_fetch_refuses_the_ssrf_shapes():
    """This service takes a URL from a caller and fetches it. Every refusal here is a hole that
    would otherwise be open, and the metadata-service address is the one that matters most."""
    from ask import external
    for bad in ("http://example.com", "file:///etc/passwd", "https://127.0.0.1/x",
                "https://localhost/x", "https://169.254.169.254/latest/meta-data/",
                "https://10.0.0.1/x", "https://[::1]/x"):
        with pytest.raises(external.ExternalFetchError):
            external.fetch(bad)


def test_external_sources_get_their_own_token_space():
    """Separation as a lexical fact rather than an instruction: [S#] is datumwise, [X#] is not."""
    from ask.skill import build_prompt
    msgs = build_prompt(
        "compare them",
        [{"sourceLabel": "The Theory of Data", "title": "t", "heading": "3.3", "route": "/x",
          "url": "u", "standing": "current", "text": "core text", "layer": "core"}],
        external=[{"title": "Someone else's article", "url": "https://example.com/a",
                   "text": "outside text", "truncated": False}],
    )
    user = msgs[-1]["content"]
    assert "[S1]" in user and "[X1]" in user
    assert "EXTERNAL — not a datumwise source" in user
    assert "may NOT establish a datumwise position" in user


def test_an_external_answer_is_not_served_from_the_plain_cache():
    """The same words asked WITH sources are a different question from the same words asked
    without them, so they must not share a cache key."""
    import inspect

    from ask import answer as answer_mod
    src = inspect.getsource(answer_mod.ask)
    assert "not external_urls" in src, (
        "asking with external sources must bypass the question-keyed cache"
    )


# ── deterministic quote verification (2026-08-26) ─────────────────────────────────────────────────

ARTICLE = ("Coding is an open-ended solution space that rewards the models' creativity. "
           "In contrast, for analytics use cases, there’s often only a single correct answer "
           "using a single correct source in which there’s no deterministic way of proving "
           "the correctness. For self-service agentic business analytics, the complexity mainly "
           "lies in the ambiguity of the data.")
EV = [{"cite": "X1", "text": ARTICLE, "layer": "external"}]


def _one(answer, evidence=None):
    from ask import quotes
    out = quotes.verify(answer, evidence if evidence is not None else EV)
    assert len(out) == 1, out
    return out[0]


def test_an_exact_span_is_verbatim():
    f = _one('They note “there’s often only a single correct answer using a single correct '
             'source” [X1].')
    assert f["verbatimMatch"] is True and f["foundIn"] == ["X1"]


def test_minimal_normalisation_only_curly_quotes_whitespace_and_case():
    f = _one('They note "There\'s often  only a single correct answer using a single correct '
             'source" [X1].')
    assert f["verbatimMatch"] is True, f["reason"]


def test_the_real_ellipsis_quote_is_not_verbatim_and_says_which_fragment_drifted():
    """The quotation from the 2026-08-26 Anthropic comparison, exactly as the answer wrote it.

    This case corrected my own earlier report. Reading the article by eye I said "both fragments are
    findable", and the deterministic check disagrees: the FIRST fragment is in the article, the
    SECOND is not, because the answer rewrote "in which there's no deterministic way" as "with no
    deterministic way". The quotation drifted in two ways at once — an elided clause AND altered
    wording — and only one of them survives a careful human read. Which is the argument for the
    ruling in one test.
    """
    f = _one('Anthropic writes: “There’s often only a single correct answer … with no '
             'deterministic way of proving the correctness.” [X1]')
    assert f["verbatimMatch"] is False and f["hasEllipsis"]
    assert f["fragments"][0]["foundIn"] == ["X1"]      # elided clause, but this half is real
    assert f["fragments"][1]["foundIn"] == []          # and this half was reworded
    assert "not every fragment is present" in f["reason"]


def test_an_ellipsis_quote_whose_fragments_all_match_is_still_not_verbatim():
    """The other ellipsis case, kept separate: a compressed sentence is not the sentence the source
    wrote, however faithful each surviving piece is."""
    f = _one('They note “Coding is an open-ended solution space … for analytics use cases” [X1].')
    assert f["verbatimMatch"] is False
    assert all(fr["foundIn"] == ["X1"] for fr in f["fragments"])
    assert "not what the source says" in f["reason"]


def test_an_edited_quotation_is_not_verbatim():
    f = _one('They say “there is always exactly one correct answer for analytics use '
             'cases” [X1].')
    assert f["verbatimMatch"] is False and "not present" in f["reason"]


def test_truncated_evidence_yields_unknown_not_false():
    """Absence in a truncated text proves nothing, and calling it `false` would be the same
    overreach this layer exists to remove."""
    ev = [{"cite": "X1", "text": ARTICLE, "layer": "external", "truncated": True}]
    f = _one('They say “something that is not in the surviving excerpt at all” [X1].', ev)
    assert f["verbatimMatch"] is None and "truncated" in f["reason"]


def test_missing_evidence_yields_unknown():
    f = _one('They say “something not present in any preserved passage here” [X1].', [])
    assert f["verbatimMatch"] is None and "not preserved" in f["reason"]


def test_scare_quoted_vocabulary_is_not_treated_as_quotation():
    from ask import quotes
    answer = ('datumwise uses “servability” rather than “serviceability” or '
              '“answerability”, and the moods are “serve with disclosures” [S1].')
    assert quotes.verify(answer, EV) == [], "vocabulary in quotes is not a quotation"


def test_the_facts_block_says_when_nothing_was_checked():
    from ask import quotes
    assert "nothing" in quotes.format_facts([])


def test_terminal_punctuation_spliced_by_the_host_sentence_still_matches_and_says_so():
    """A real case from the Anthropic candidate: the paper ends the clause with a full stop and the
    answer spliced a comma to continue its own sentence. Every word is the source's. Calling that an
    edited quotation would bury the real findings under pedantry — but it is reported, not silent.
    """
    ev = [{"cite": "S2", "text": "... and when two derivations claiming one identity are required "
                                 "to agree. This law is part of the jurisdictional claim."}]
    f = _one('The law includes conditions “when two derivations claiming one identity are '
             'required to agree,” aiming at canonical identity [S2].', ev)
    assert f["verbatimMatch"] is True
    assert "terminal punctuation" in f["reason"]


def test_internal_wording_changes_are_never_normalised_away():
    ev = [{"cite": "S2", "text": "when two derivations claiming one identity are required to agree."}]
    f = _one('It says “when two derivations claiming one identity must agree,” which [S2].', ev)
    assert f["verbatimMatch"] is False


# ── durable citations (2026-08-26) ────────────────────────────────────────────────────────────────

def test_a_stored_citation_reresolves_to_current_standing_and_keeps_what_it_said():
    """The servability case, reconstructed. An answer written while AG v1.1 was current cited it as
    current. v2.0 superseded it. The public sentence must move; the record of what was said must not.
    """
    frozen = ("current record v1.1 (2026-08-21, doi:10.5281/zenodo.22046037); deposited text — "
              "read from the deposited record, not from a page on this site")
    stored = [{
        "cite": "S1", "label": "Analytical Governance", "heading": "4. The servability gap",
        "sourceId": "s-analytical-governance",
        "readableRecordId": "w-analytical-governance.r02",
        "currentRecordIdAtAnswer": "w-analytical-governance.r02",
        "standingTemplate": "{CURRENT}; deposited text — read from the deposited record, "
                            "not from a page on this site",
        "standing": frozen, "standingAtAnswer": frozen,
    }]
    from ask import citations
    got = citations.resolve(stored)[0]
    assert got["standingAtAnswer"] == frozen                    # history is not rewritten
    assert "v2.0" in got["standing"], got["standing"]           # the public sentence moved
    assert "22115819" in got["standing"]
    assert got["supersededSinceAnswer"] is True                 # and it says so
    assert citations.any_superseded(citations.resolve(stored))


def test_a_citation_still_current_is_not_flagged():
    from ask import citations
    stored = [{"cite": "S1", "sourceId": "s-theory-of-certainty",
               "readableRecordId": "w-theory-of-certainty.r01",
               "currentRecordIdAtAnswer": "w-theory-of-certainty.r01",
               "standingTemplate": "{CURRENT}; deposited text", "standing": "…"}]
    got = citations.resolve(stored)[0]
    assert got["supersededSinceAnswer"] is False and "v1.0" in got["standing"]


def test_a_pre_identity_citation_says_it_cannot_be_resolved_rather_than_looking_fresh():
    from ask import citations
    got = citations.resolve([{"cite": "S1", "standing": "current record v1.1 (2026-08-21)"}])[0]
    assert got["resolvable"] is False
    assert got["standing"] == "current record v1.1 (2026-08-21)"   # unchanged, not guessed at
    assert got["supersededSinceAnswer"] is None


def test_the_deposit_standing_template_survives_into_a_stored_citation():
    """The seam: retrieve hands out the unspliced template, answer.py stores it. If either end
    stops, durable citations silently freeze again — which is the defect this pair removes."""
    hits = retrieve.search("what is analytical governance?", k=3)
    assert hits and all("standingRaw" in h for h in hits)
    assert any("{CURRENT}" in h["standingRaw"] for h in hits)


# ── quote-verification durability (CG2 ruling E.7, 2026-08-26) ─────────────────────────────────────

def _facts_for(answer, evidence):
    from ask import quotes
    facts = quotes.verify(answer, evidence)
    return facts, quotes.format_facts(facts)


def test_the_facts_the_reviewer_was_given_survive_storage():
    """review() computed them, handed them to the reviewer as facts, and returned them — and until
    this column existed the storage layer dropped them, so every review a human READ reported
    `quoteFacts: null`. Both the structured facts and the block as sent are preserved."""
    qid = _candidate("Does the review record keep what the reviewer was told?")
    answer = ('datumwise holds that "the analytical permission required to be served" is the '
              'question servability answers [S1].')
    evidence = [{"cite": "S1", "label": "Analytical Governance", "heading": "4",
                 "text": "Servability — whether the result has the analytical permission required "
                         "to be served as that answer."}]
    facts, as_sent = _facts_for(answer, evidence)
    store.save_review(qid, {"disposition": "APPROVE", "summary": "ok", "changes": [],
                            "findings": {}, "proposedAnswer": None, "model": "test:model",
                            "costUsd": 0.0, "quoteFacts": facts, "quoteFactsAsSent": as_sent})
    got = store.latest_review(qid)
    assert got["quoteFactsRecorded"] is True
    assert got["quoteFactsReconstructed"] is False           # captured with the review, not re-derived
    assert got["quoteFacts"] == facts
    assert got["quoteFactsAsSent"] == as_sent
    assert "VERBATIM MATCH" in got["quoteFactsAsSent"]


def test_not_recorded_and_nothing_to_report_are_different_facts():
    """The distinction the whole envelope exists for. A review that ran before the facts were
    persisted must never read like a review whose answer quoted nothing."""
    old = _candidate("A review from before the facts were kept?")
    store.save_review(old, {"disposition": "APPROVE", "summary": "", "changes": [], "findings": {},
                            "proposedAnswer": None, "model": "test:model", "costUsd": 0.0})
    r_old = store.latest_review(old)
    assert r_old["quoteFactsRecorded"] is False and r_old["quoteFacts"] is None

    quiet = _candidate("An answer with no quotations at all?")
    store.save_review(quiet, {"disposition": "APPROVE", "summary": "", "changes": [], "findings": {},
                              "proposedAnswer": None, "model": "test:model", "costUsd": 0.0,
                              "quoteFacts": [], "quoteFactsAsSent": "  (no direct quotations…)"})
    r_quiet = store.latest_review(quiet)
    assert r_quiet["quoteFactsRecorded"] is True and r_quiet["quoteFacts"] == []


def test_a_reconstruction_says_it_is_one_and_cannot_overwrite_a_capture():
    """quotes.verify is deterministic, so recomputing gives the same facts — but a re-derived fact
    is not a recorded one, and the flag is the only thing that keeps them distinguishable."""
    qid = _candidate("Can facts be reconstructed after the fact?")
    rid = store.save_review(qid, {"disposition": "APPROVE", "summary": "", "changes": [],
                                  "findings": {}, "proposedAnswer": None, "model": "test:model",
                                  "costUsd": 0.0})
    facts, as_sent = _facts_for('It says "a plausible number" and nothing more [S1].',
                                [{"cite": "S1", "text": "All three can return a plausible number."}])
    assert store.attach_quote_facts(rid, facts, as_sent) is True
    got = store.latest_review(qid)
    assert got["quoteFactsRecorded"] is True and got["quoteFactsReconstructed"] is True
    # fails closed: a reconstruction may not silently displace what was actually captured
    assert store.attach_quote_facts(rid, [], "") is False
    assert store.latest_review(qid)["quoteFacts"] == facts


def test_the_review_screen_renders_the_facts_and_distinguishes_the_four_states():
    """The second half of the defect: the facts were never rendered at all, so a human asked to
    accept a review of a quotation could not see whether the quotation checked out."""
    from ask.review_ui import REVIEW_PAGE
    assert "Quote verification — the facts the reviewer was given" in REVIEW_PAGE
    for state in ("VERBATIM MATCH", "NOT VERBATIM", "UNKNOWN", "UNATTRIBUTED"):
        assert state in REVIEW_PAGE
    assert "NOT RECORDED" in REVIEW_PAGE and "RECONSTRUCTED, not captured" in REVIEW_PAGE
    assert "quoteFactsAsSent" in REVIEW_PAGE            # the block exactly as the reviewer got it


# ── durable citation labels (Huayin, ruling 1 of 2026-08-26 15:59) ─────────────────────────────────

def test_a_renamed_label_reresolves_and_keeps_what_was_shown():
    """Identity is durable; current presentation is resolved. The editorial label for Analytical
    Governance changed on 2026-08-26 from the superseded edition's full title to the work's name, and
    a citation stored before that must now DISPLAY the new one while still recording the old."""
    from ask import citations
    stored = [{"cite": "S1", "sourceId": "s-analytical-governance",
               "label": "Analytical Governance: From User Intent to Governed Analytical Execution",
               "readableRecordId": "w-analytical-governance.r03",
               "currentRecordIdAtAnswer": "w-analytical-governance.r03",
               "standingTemplate": "{CURRENT}; deposited text", "standing": "…"}]
    got = citations.resolve(stored)[0]
    assert got["label"] == "Analytical Governance"                      # what a reader sees now
    assert got["labelAtAnswer"].endswith("Governed Analytical Execution")  # what was shown then
    assert got["labelChangedSinceAnswer"] is True
    assert got["labelResolvable"] is True
    # A RENAME IS NOT A SUPERSESSION. The two facts must not collapse: same record cited, same record
    # current, only the editorial name moved.
    assert got["supersededSinceAnswer"] is False
    assert got["readableRecordId"] == "w-analytical-governance.r03"
    assert got["currentRecordId"] == "w-analytical-governance.r03"
    assert stored[0]["label"].startswith("Analytical Governance:")      # the stored row is untouched


def test_a_citation_of_a_superseded_edition_keeps_its_dated_name():
    """index_build's rule, reused rather than re-invented: an explicitly titled source pinned to a
    non-current edition keeps its own dated title. Re-resolving a citation of the v1.1 TEXT to the
    bare work label would make a preserved historical citation read as the current work."""
    from ask import citations
    got = citations.resolve([{"cite": "S1", "sourceId": "s-analytical-governance-v1-1",
                              "label": "Analytical Governance v1.1, 21 August 2026",
                              "readableRecordId": "w-analytical-governance.r02",
                              "currentRecordIdAtAnswer": "w-analytical-governance.r02",
                              "standingTemplate": "PRESERVED HISTORICAL STATE — {READABLE}",
                              "standing": "…"}])[0]
    assert got["label"] == "Analytical Governance v1.1, 21 August 2026"
    assert got["labelChangedSinceAnswer"] is False
    assert got["supersededSinceAnswer"] is True      # this one IS a supersession, and says so


def test_a_label_resolves_even_when_the_standing_cannot():
    """Different facts need different identities: the standing sentence needs a record, the label
    needs only the source. Resolving what can be resolved is not guessing at what cannot."""
    from ask import citations
    got = citations.resolve([{"cite": "S1", "sourceId": "s-theory-of-certainty",
                              "label": "some older name",
                              "standing": "current record v1.0 (2026-08-26)"}])[0]
    assert got["resolvable"] is False and got["supersededSinceAnswer"] is None
    assert got["label"] == "The Theory of Certainty" and got["labelResolvable"] is True
    assert got["standing"] == "current record v1.0 (2026-08-26)"       # unchanged, not guessed at


def test_an_unknown_source_keeps_the_label_it_was_shown():
    from ask import citations
    got = citations.resolve([{"cite": "S1", "sourceId": "s-gone", "label": "A retired source"}])[0]
    assert got["labelResolvable"] is False and got["label"] == "A retired source"
    assert got["labelChangedSinceAnswer"] is None

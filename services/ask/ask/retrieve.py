"""Retrieval over the shipped-build index. Lexical BM25 first; embeddings only if they earn it.

The brief said: "If simple lexical + semantic retrieval works, use it. Use embeddings/vector search
only if they materially improve the prototype." So this module ships BM25 as the default and keeps a
measured, switchable embedding path behind `ASK_EMBEDDINGS=1`. The eval harness reports retrieval
hit-rate for both, so the decision is made on numbers rather than on taste. Whatever the numbers say
is in the report.

WHY BM25 IS A SERIOUS CANDIDATE HERE AND NOT A STRAW MAN. This corpus is small (663 sections) and
unusually keyword-dense: it is a body of work that *defines its own vocabulary* and then uses those
exact words consistently — universe, manifold, anchor, basis, verdict, measure family, edition. The
retrieval failure that embeddings normally fix (the reader's words differ from the corpus's words) is
partly pre-solved by the corpus being a glossary of itself. That is a real property of this material,
not an excuse to skip the work.

ONE NON-OBVIOUS RULE, AND IT IS THE IMPORTANT ONE: historical and edition-pinned passages are NOT
excluded from retrieval. They are demoted, and they arrive labelled. Excluding them would make the
agent unable to answer "what did the August map say?" — a legitimate historical question the brief
explicitly wants supported. Silently ranking them equal with current material would reproduce the
defect Gateway 1 removed. So: demote, label, and let the skill decide. The tool takes a position on
relevance; the skill takes the position on standing.
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

INDEX = Path(__file__).resolve().parent.parent / "index" / "chunks.json"

# Demotion factors applied AFTER lexical scoring. Deliberately mild: strong enough that a current
# source outranks a superseded one on equal lexical evidence, weak enough that a historical passage
# still surfaces when it is overwhelmingly the best match (which is exactly what a historical
# question looks like).
HISTORICAL_FACTOR = 0.55
EDITION_PINNED_FACTOR = 0.80
# Applied to a reference passage whose jurisdiction the question explicitly opened. Within its own
# jurisdiction a reference source is the authority, not a fallback — see the note in search().
JURISDICTION_BOOST = 1.6

_WORD = re.compile(r"[a-z0-9][a-z0-9'_-]*")

# Deliberately short. Corpus vocabulary like "data", "value", "table" is *load-bearing* here, so the
# usual aggressive stoplist would delete the signal.
STOP = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "is", "are", "was", "were", "be",
    "been", "it", "its", "this", "that", "these", "those", "as", "at", "by", "for", "from", "on",
    "with", "you", "your", "we", "our", "i", "not", "no", "so", "do", "does", "did", "can", "could",
    "would", "should", "what", "which", "who", "how", "when", "where", "why", "there", "here",
}


def _tok(s: str) -> list[str]:
    return [w for w in _WORD.findall(s.lower()) if w not in STOP and len(w) > 1]


# ── request-time identifier resolution ────────────────────────────────────────────────────────────
# The index stores foreign keys (`currentRecordId`, `readableRecordId`), never publication facts —
# see the long comment in index_build.py about why G7 was right to reject the first design. The
# version, date and DOI are spliced into the standing sentence HERE, from records.json inside the
# running service. Consequence: the agent physically cannot be handed a stale identifier, because
# every identifier it ever sees was read from the registry during the request that used it.

RECORDS_JSON = Path(__file__).resolve().parents[3] / "registry" / "publications" / "records.json"


@lru_cache(maxsize=1)
def _records() -> dict[str, dict]:
    return {r["recordId"]: r for r in json.loads(RECORDS_JSON.read_text())}


def _describe(record_id: str | None) -> str:
    r = _records().get(record_id or "")
    if not r:
        return "an edition"
    v = f"v{r['version']}" if r.get("version") else "the first edition"
    doi = f", doi:{r['doi']}" if r.get("doi") else ""
    return f"{v} ({r.get('date', '')}{doi})"


def _resolve_url(chunk: dict) -> str:
    """A deposited work has no page to link; send the reader to the record itself."""
    if chunk.get("url"):
        return chunk["url"]
    r = _records().get(chunk.get("currentRecordId") or "")
    return f"https://doi.org/{r['doi']}" if r and r.get("doi") else ""


def _fill_standing(chunk: dict) -> str:
    """Splice live registry facts into the standing sentence's placeholders."""
    s = chunk["standing"]
    if "{CURRENT}" in s:
        s = s.replace("{CURRENT}", f"current record {_describe(chunk.get('currentRecordId'))}")
    if "{READABLE}" in s:
        s = s.replace("{READABLE}", _describe(chunk.get("readableRecordId")))
    return s


@lru_cache(maxsize=1)
def _corpus() -> tuple[list[dict], list[list[str]], dict[str, float], float]:
    chunks = json.loads(INDEX.read_text())
    # Heading and source label are part of the searchable text: a section titled "What is a measure
    # family?" should be found by that question even if the body never repeats the phrase.
    docs = [
        _tok(f"{c.get('sourceLabel') or ''} {c['title']} {c['heading']} {c['text']}")
        for c in chunks
    ]
    n = len(docs)
    df = Counter()
    for d in docs:
        df.update(set(d))
    idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
    avgdl = sum(len(d) for d in docs) / max(1, n)
    return chunks, docs, idf, avgdl


def _bm25(query: str, k1: float = 1.5, b: float = 0.75) -> list[tuple[int, float]]:
    chunks, docs, idf, avgdl = _corpus()
    q = _tok(query)
    if not q:
        return []
    scores: list[tuple[int, float]] = []
    for i, d in enumerate(docs):
        if not d:
            continue
        tf = Counter(d)
        dl = len(d)
        s = 0.0
        for t in q:
            f = tf.get(t)
            if not f:
                continue
            s += idf.get(t, 0.0) * (f * (k1 + 1)) / (f + k1 * (1 - b + b * dl / avgdl))
        if s > 0:
            scores.append((i, s))
    return scores


@lru_cache(maxsize=1)
def _embeddings():
    """Lazy, optional. Returns (matrix, dim) or None. Costs one embedding call per chunk, once."""
    if os.environ.get("ASK_EMBEDDINGS") != "1":
        return None
    cache = INDEX.parent / "embeddings.json"
    chunks, _, _, _ = _corpus()
    if cache.exists():
        data = json.loads(cache.read_text())
        if data.get("n") == len(chunks):
            return data["vectors"]
    from .providers import embed  # local import: embeddings are optional

    texts = [f"{c['title']} — {c['heading']}\n{c['text']}" for c in chunks]
    vectors = embed(texts)
    cache.write_text(json.dumps({"n": len(chunks), "vectors": vectors}))
    return vectors


def _cosine_scores(query: str) -> list[tuple[int, float]] | None:
    vecs = _embeddings()
    if not vecs:
        return None
    from .providers import embed

    qv = embed([query])[0]
    out = []
    for i, v in enumerate(vecs):
        dot = sum(a * b for a, b in zip(qv, v))
        out.append((i, dot))  # provider returns unit-normalised vectors
    return out


# ── THE TWO LAYERS (Huayin, 2026-08-25) ───────────────────────────────────────────────────────────
# Ask has two source layers, not one flat corpus.
#
#   REPRESENTATIVE — the works through which datumwise currently STATES its intellectual position.
#     Used by default, for "what does datumwise hold about X?"
#   REFERENCE — entered when the question calls for a particular jurisdiction or object. NOT weak,
#     obsolete or untrusted: several reference sources are the HIGHEST authority for the thing they
#     actually establish. Jurisdiction, not rank.
#
# The router below is deliberately the dumbest thing that implements that: literal cues per
# jurisdiction. Not a classifier, no model call, fully inspectable — you can read it and predict
# exactly which layer a question opens. The ruling said to add harder adjudication machinery only
# after observed failures, so this is what ships until a failure argues otherwise.
#
# When no cue matches, retrieval is representative-only. That is the default the ruling asks for,
# and it is what stops "useful to Ask" from quietly becoming a reason for membership.
JURISDICTION_CUES: dict[str, tuple[str, ...]] = {
    "normative": ("shipped", "syntax", "grammar", "parser", "keyword", "signature", "accepts",
                  "manual", "implemented in columna", "is it implemented", "does columna support",
                  "api", "cli", "command"),
    "defects": ("broken", "defect", "bug", "known issue", "known issues", "currently wrong",
                "regression", "not working", "unreliable"),
    "evidence": ("demonstrate", "demonstrated", "the case", "cascadia", "exhibit", "transcript",
                 "worked example", "actually did", "actually does", "explorer", "walkthrough"),
    "study": ("study", "benchmark", "nine-model", "text-to-sql", "cross-comparison", "experiment"),
    "historical": ("august map", "research map", "used to say", "at the time", "back then",
                   "previously said", "historical", "preserved", "earlier version of the site"),
    "teaching": ("explain simply", "in plain language", "for a beginner", "walk me through",
                 "one afternoon", "park", "start here", "cold start"),
    "position": ("position", "stance", "do you think", "argue", "atlas", "silent failure"),
}


# ── the definitional fallback (2026-08-26) ────────────────────────────────────────────────────────
# The cue router above answers "does this question CALL FOR a jurisdiction?". It cannot answer the
# other question a definitional query raises: "does the representative layer even ESTABLISH this
# term?" — and when the answer is no, representative-only retrieval does not abstain. It returns
# the best lexical near-miss it can find and the agent answers confidently from it.
#
# That is exactly how "What is a basis?" failed on BOTH models on 2026-08-26. In Columna, BASIS is
# a declaration construct — `UNIVERSE active_stores BASIS registry(store_directory)` — and the four
# bases (registry, spine, product, events) are what fix whether an absent row is a real zero, a gap
# or a membership fact. That is established in the Columna reference manual, ch. 9, and NOWHERE in
# the representative layer. The representative layer carries only "certificate basis" and "basis
# token": different terms that happen to share a word. Both models therefore explained the free
# commutative monoid F(S) and its generators e_a — a correct reading of a passage that was not
# about the asked term.
#
# The rule is narrow on purpose: it fires ONLY when the question is definitional in shape AND no
# representative section is HEADED for the asked term. "What is an anchor?", "What is a measure
# family?" and "What is a universe?" all have representative sections titled exactly that, so the
# fallback never sees them and the representative layer keeps its own vocabulary. When it does
# fire, it does not pick a winner — it opens the reference layer and lets the existing ranking and
# the skill's standing rules adjudicate.
_DEFN_Q = re.compile(
    r"^\s*(?:what\s+(?:is|are)\s+(?:an?|the)\s+(?P<a>[^?]+?)"
    r"|what\s+does\s+(?:an?|the)?\s*(?P<b>[^?]+?)\s+mean"
    r"|define\s+(?P<c>[^?]+?))\s*\??\s*$",
    re.I,
)
_HEAD_NUM = re.compile(
    r"^\s*(?:chapter\s+\d+|appendix\s+[a-z]|part\s+[ivx]+|\d+(?:\.\d+)*)[.:\u2014-]*\s*", re.I
)


def definitional_subject(query: str) -> str | None:
    """The term a "what is X?" question is asking about, or None if it is not that shape."""
    m = _DEFN_Q.match(query.strip())
    if not m:
        return None
    term = (m.group("a") or m.group("b") or m.group("c") or "").strip().lower()
    # A TERM, not a sentence-long descriptor. "What is the current Theory of Data publication?" is
    # a question about a record's standing, not a request for a definition, and widening the layers
    # for it would be the fallback overreaching into questions the cue router already handles.
    return term if term and len(term.split()) <= 3 else None


def _headed_for(term: str) -> bool:
    """Does any REPRESENTATIVE section carry this term as its heading's head, not as a modifier?

    "2.3 Anchor" and "3.2 Measure family" count. "6.6 Certificate basis is open-typed" does not:
    the term there is `certificate basis`, and treating it as a locus for `basis` is the exact
    confusion this function exists to prevent.
    """
    for c in _corpus()[0]:
        if c.get("layer") != "representative":
            continue
        h = _HEAD_NUM.sub("", c["heading"]).strip().lower().lstrip("\u2014- ")
        h = h[4:].lstrip() if h.startswith("the ") else h
        if h == term or h.startswith(f"{term} ") or h.startswith(f"{term},"):
            return True
    return False


# ── structural exclusions: a section that is not prose (2026-08-26) ───────────────────────────────
# A bibliography is a LIST OF OTHER PEOPLE'S WORKS. It is in the index because it is in the paper,
# and BM25 loves it: it is dense with exactly the proper nouns and title words a question uses,
# while containing no claim at all. After the dedup repair let deposit passages through, reference
# lists surfaced in the top 8 on 6 of the 26 trap cases — and the worst of them was a1, the primary
# DOI hallucination trap, which received FOUR bibliography passages out of eight. A question asking
# for the DOI of a work that does not exist was being handed four pages of real DOIs belonging to
# other works. It passed on both models. It should never have been asked to.
#
# This is a hard gate rather than a demotion, for the same reason `layer == "out"` is a hard gate:
# the problem is not that these passages rank too high, it is that they cannot support a claim. A
# demotion still admits them when nothing else scores, which is precisely the case where citing one
# does the most damage.
#
# They stay reachable, because "what does this paper cite?" is a real question. Matching is on the
# WHOLE normalised heading, not a substring: "8. The reference map, and the outer boundary" and
# "Appendix A: Operator Reference" are prose and stay in.
# Enumerated rather than pattern-matched, and that is a deliberate choice: this corpus is small
# enough that every heading containing "reference"/"reading" was read by hand before this set was
# written. The last two are here because they ARE reference lists — "References and reading path"
# and "Project references" are lists of works with DOIs, whatever their headings say.
# "Implementation and further reading" is deliberately NOT here: it is prose that names which
# source is authoritative for shipped meaning, which is a claim, and s3 is a case about exactly
# that. A pattern would have swept it up with the rest.
BIBLIOGRAPHY_HEADINGS = {
    "references", "reference list", "bibliography", "works cited", "further reading",
    "references and reading path", "project references",
}
CITATION_CUES = (
    "cite", "cites", "cited", "citation", "citations", "bibliograph", "references list",
    "reference list", "related literature", "prior literature", "further reading",
    "reading list", "what does it reference", "which works",
)


def _bare_heading(heading: str) -> str:
    return _HEAD_NUM.sub("", heading).strip().lower().strip(":\u2014- ")


def is_bibliography(chunk: dict) -> bool:
    return _bare_heading(chunk["heading"]) in BIBLIOGRAPHY_HEADINGS


def asks_about_citations(query: str) -> bool:
    q = query.lower()
    return any(c in q for c in CITATION_CUES)


def jurisdictions_for(query: str) -> list[str]:
    q = query.lower()
    return sorted({j for j, cues in JURISDICTION_CUES.items() if any(c in q for c in cues)})


def search(query: str, k: int = 8, layers: list[str] | None = None) -> list[dict]:
    """Return the k best passages, each carrying its standing AND its corpus layer.

    Representative always. Reference only for jurisdictions the question actually calls for.
    """
    chunks, _, _, _ = _corpus()
    lex = dict(_bm25(query))
    if not lex:
        return []
    lex_max = max(lex.values()) or 1.0
    combined: dict[int, float] = {i: s / lex_max for i, s in lex.items()}

    sem = _cosine_scores(query)
    if sem:
        sem_d = dict(sem)
        sem_max = max(sem_d.values()) or 1.0
        # Simple, documented blend. Not tuned — if it needs tuning, that is a finding to report,
        # not a knob to quietly turn.
        for i in set(combined) | set(sem_d):
            combined[i] = 0.6 * combined.get(i, 0.0) + 0.4 * (sem_d.get(i, 0.0) / sem_max)

    opened = jurisdictions_for(query)
    wants_citations = asks_about_citations(query)
    if not opened:
        term = definitional_subject(query)
        if term and not _headed_for(term):
            # No cue fired and the representative layer has no section headed for the asked term.
            # Widen rather than answer from a near-miss; ranking decides which jurisdiction wins.
            #
            # "historical" is deliberately NOT opened. Opening a jurisdiction does two things —
            # it admits that reference layer AND it cancels the demotion of preserved state — and
            # only the first is wanted here. A question that does not know a term is not thereby a
            # question about what the site said in August. Caught by
            # test_current_outranks_historical_on_a_current_question, which the first version of
            # this fallback broke: "what is the current source estate" widened, the preserved
            # research map stopped being demoted, and a question with "current" in it was answered
            # from a historical snapshot.
            opened = sorted(set(JURISDICTION_CUES) - {"historical"})
    ranked = []
    for i, s in combined.items():
        c = chunks[i]
        lay = c.get("layer", "unruled")
        if lay == "out":
            continue
        if is_bibliography(c) and not wants_citations:
            continue
        if lay == "reference":
            # Reference material is reachable only through its own jurisdiction. A question that
            # does not call for it never sees it — which is what stops the manuals from quietly
            # constituting datumwise's intellectual position because they happen to be easy to
            # retrieve.
            if c.get("jurisdiction") not in opened:
                continue
            # ...and once the question HAS opened that jurisdiction, the source is PROMOTED, not
            # demoted.
            #
            # The first version demoted it, and that was wrong twice over: "What does shipped
            # Frame-QL allow?" returned three representative passages and no Manual, and "What did
            # the August research map say?" returned no map at all. The gate and the demotion were
            # doing the same job twice — a source was first excluded unless invited, then penalised
            # for having been invited.
            #
            # The correct rule: within its own jurisdiction a reference source is the AUTHORITY.
            # The Frame-QL Manual governs shipped semantics; Known Issues governs defects; the
            # preserved map governs what was said in August. Being asked for is exactly the
            # condition under which it should win.
            s *= JURISDICTION_BOOST
        if c["isHistorical"] and "historical" not in opened:
            # Demote a preserved state only when the question did NOT ask about history. When it
            # did, the preserved state is the thing being asked for.
            s *= HISTORICAL_FACTOR
        elif c["isEditionPinned"]:
            # Edition-pinning is orthogonal to layer — it is about WHICH edition a route renders —
            # so it still applies. The passage arrives labelled either way.
            s *= EDITION_PINNED_FACTOR
        ranked.append((s, i))
    ranked.sort(reverse=True)

    # One passage per SECTION — a section should not occupy three of eight slots because it was
    # long enough to be split.
    #
    # The key was (route, anchor), and that was a serious bug rather than a cosmetic one: a
    # DEPOSITED work has no route and no anchor (it has no page on the site — see index_build.py),
    # so all 765 deposit-derived chunks — 60% of the index, and the whole of the representative
    # corpus of papers — collapsed into the single key ("", ""). The loop therefore admitted
    # EXACTLY ONE deposit passage per query no matter how many scored well, and discarded the rest
    # silently. "What is a basis?" reached the model with one passage in its hands.
    #
    # Section identity is what the dedup actually meant, and the index already carries it: the
    # heading, plus whichever of route/sourceId the passage came from. Split sections still
    # collapse (the longest is 8 parts under one key); distinct sections no longer do.
    out, seen = [], set()
    for s, i in ranked:
        c = chunks[i]
        key = (c["route"] or c["sourceId"], c["anchor"], c["heading"])
        if key in seen:
            continue
        seen.add(key)
        out.append({**c, "standing": _fill_standing(c), "url": _resolve_url(c),
                    "score": round(s, 4)})
        if len(out) >= k:
            break
    return out


def stats() -> dict:
    chunks, _, _, _ = _corpus()
    return {
        "chunks": len(chunks),
        "routes": len({c["route"] for c in chunks}),
        "catalogued": sum(1 for c in chunks if c["sourceId"]),
        "historical": sum(1 for c in chunks if c["isHistorical"]),
        "editionPinned": sum(1 for c in chunks if c["isEditionPinned"]),
        "representative": sum(1 for c in chunks if c.get("layer") == "representative"),
        "reference": sum(1 for c in chunks if c.get("layer") == "reference"),
        "fromDeposits": sum(1 for c in chunks if not c.get("route")),
        "embeddings": bool(os.environ.get("ASK_EMBEDDINGS") == "1"),
    }

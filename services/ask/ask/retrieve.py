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


def search(query: str, k: int = 8) -> list[dict]:
    """Return the k best passages, each carrying its standing. Never returns a bare quotation."""
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

    ranked = []
    for i, s in combined.items():
        c = chunks[i]
        if c["isHistorical"]:
            s *= HISTORICAL_FACTOR
        elif c["isEditionPinned"]:
            s *= EDITION_PINNED_FACTOR
        ranked.append((s, i))
    ranked.sort(reverse=True)

    # One passage per (route, anchor) — a section should not occupy three of eight slots because it
    # was long enough to be split.
    out, seen = [], set()
    for s, i in ranked:
        c = chunks[i]
        key = (c["route"], c["anchor"])
        if key in seen:
            continue
        seen.add(key)
        out.append({**c, "standing": _fill_standing(c), "score": round(s, 4)})
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
        "embeddings": bool(os.environ.get("ASK_EMBEDDINGS") == "1"),
    }

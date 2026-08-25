"""SQLite storage: cached Q&A, votes, views, conversations.

RANKING RULE (the one the brief asked me to choose and report):

    rank = log10(views + 1) + helpfulness_bonus
    helpfulness_bonus = 0.0                if ratings < 3
                      = up_rate - 0.5      otherwise        # in [-0.5, +0.5]

That is the whole rule. Three properties I chose it for:

  1. VIEWS LEAD, LOG-DAMPED. The brief says more-viewed questions move up. log10 means a 10x view
     advantage is worth 1.0 — real, but not enough for one runaway question to bury everything
     beneath it forever.
  2. HELPFULNESS REORDERS WITHIN ROUGHLY ONE ORDER OF MAGNITUDE OF VIEWS. The bonus spans exactly
     [-0.5, +0.5], and log10 makes a 10x view gap worth 1.0 — so the full width of the feedback
     signal is exactly one order of magnitude of views. The consequences, both intended:
       · a merely mediocre score never overturns a 10x view advantage;
       · a UNANIMOUS one does, at exactly 10x. An answer ten of ten readers called unhelpful should
         sit below a well-rated one even with ten times the traffic.
       · nothing about feedback can overturn a 100x view gap.
     This edge is pinned by test_helpfulness_breaks_ties_but_does_not_dominate_views, so changing
     the bonus range or the rating threshold is a deliberate act with a failing test attached.
  3. UNDER 3 RATINGS, NO OPINION. Not a Bayesian prior, not a confidence interval, not smoothing —
     the brief explicitly ruled those out. Just: with fewer than three votes we decline to have a
     view, so a single thumbs-down cannot bury a new answer and two thumbs-up cannot crown one.
     The threshold is one constant, on the next line, and changing it is a one-line diff.

Deliberately absent: recency decay, personalisation, engagement weighting, hidden quality scores.
When real usage shows this rule is wrong, it is four lines to replace and the stored counters are
raw, so no history is lost to a scoring change.

STARS are display only. Users vote 👍/👎; stars are the up-rate on a five-point scale, rounded to
the nearest half — 100% -> 5.0, 90% -> 4.5, 80% -> 4.0, exactly as specified. The rating count is
always returned beside them so two votes cannot masquerade as a reputation.
"""

from __future__ import annotations

import json
import math
import os
import sqlite3
import time
import uuid
from pathlib import Path

MIN_RATINGS_FOR_BONUS = 3

DB_PATH = Path(os.environ.get("ASK_DB", "/data/ask.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS qa (
  id            TEXT PRIMARY KEY,
  question      TEXT NOT NULL,
  question_key  TEXT NOT NULL,              -- normalised, for exact/obvious reuse only
  answer        TEXT NOT NULL,
  created_at    REAL NOT NULL,
  provider      TEXT NOT NULL,
  model         TEXT NOT NULL,
  sources       TEXT NOT NULL,              -- JSON: datumwise sources cited
  external      TEXT NOT NULL DEFAULT '[]', -- JSON: external sources cited
  corpus_settles INTEGER NOT NULL DEFAULT 1,
  views         INTEGER NOT NULL DEFAULT 0,
  up            INTEGER NOT NULL DEFAULT 0,
  down          INTEGER NOT NULL DEFAULT 0,
  public        INTEGER NOT NULL DEFAULT 1,
  withheld_reason TEXT,
  verify        TEXT NOT NULL DEFAULT '{}', -- JSON: the identifier gate's verdict
  prompt_tokens INTEGER NOT NULL DEFAULT 0,
  completion_tokens INTEGER NOT NULL DEFAULT 0,
  cost_usd      REAL NOT NULL DEFAULT 0.0,
  parent_id     TEXT                        -- set when this was asked as a follow-up
);
CREATE INDEX IF NOT EXISTS qa_key    ON qa(question_key);
CREATE INDEX IF NOT EXISTS qa_public ON qa(public);

-- One row per model call, whether or not it became a public Q&A. This is the conversation log the
-- brief asks for: what was asked, what came back, which sources, which model, when.
-- NO chain-of-thought is stored, by instruction: the answer and its evidence record, nothing else.
CREATE TABLE IF NOT EXISTS turns (
  id            TEXT PRIMARY KEY,
  conversation  TEXT NOT NULL,
  qa_id         TEXT,
  question      TEXT NOT NULL,
  answer        TEXT NOT NULL,
  sources       TEXT NOT NULL,
  external      TEXT NOT NULL DEFAULT '[]',
  provider      TEXT NOT NULL,
  model         TEXT NOT NULL,
  created_at    REAL NOT NULL,
  cached        INTEGER NOT NULL DEFAULT 0,
  corpus_settles INTEGER NOT NULL DEFAULT 1,
  verify        TEXT NOT NULL DEFAULT '{}',
  prompt_tokens INTEGER NOT NULL DEFAULT 0,
  completion_tokens INTEGER NOT NULL DEFAULT 0,
  cost_usd      REAL NOT NULL DEFAULT 0.0
);
CREATE INDEX IF NOT EXISTS turns_conv ON turns(conversation);

-- Feedback is binary and one vote per (qa, voter). voter is a random client-side id in a cookie,
-- not an account: enough to stop double-voting by accident, not an identity.
CREATE TABLE IF NOT EXISTS votes (
  qa_id   TEXT NOT NULL,
  voter   TEXT NOT NULL,
  helpful INTEGER NOT NULL,
  at      REAL NOT NULL,
  PRIMARY KEY (qa_id, voter)
);
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=15)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.executescript(SCHEMA)
    return c


def normalise(q: str) -> str:
    """Exact / obviously-identical reuse only. No semantic canonicalisation in v0, by instruction.

    Lowercase, collapse whitespace, drop terminal punctuation. That reuses "What is an anchor?" for
    "what is an anchor" and nothing cleverer. If duplicate phrasings turn out to be a real problem we
    will have the log to prove it, which is the point.
    """
    import re
    return re.sub(r"\s+", " ", q.strip().lower()).rstrip("?.! ")


def stars(up: int, down: int) -> float | None:
    n = up + down
    if n == 0:
        return None
    return round(up / n * 5 * 2) / 2


def rank(views: int, up: int, down: int) -> float:
    n = up + down
    bonus = 0.0 if n < MIN_RATINGS_FOR_BONUS else (up / n) - 0.5
    return math.log10(views + 1) + bonus


def _row_to_public(r: sqlite3.Row) -> dict:
    up, down = r["up"], r["down"]
    return {
        "id": r["id"],
        "question": r["question"],
        "answer": r["answer"],
        "createdAt": r["created_at"],
        "sources": json.loads(r["sources"]),
        "external": json.loads(r["external"]),
        "corpusSettles": bool(r["corpus_settles"]),
        "views": r["views"],
        "ratings": up + down,
        "up": up,
        "down": down,
        "stars": stars(up, down),
        "model": r["model"],
        "provider": r["provider"],
        "rank": round(rank(r["views"], up, down), 4),
    }


def find_cached(question: str) -> dict | None:
    with connect() as c:
        r = c.execute(
            "SELECT * FROM qa WHERE question_key=? AND public=1 ORDER BY created_at DESC LIMIT 1",
            (normalise(question),),
        ).fetchone()
        return _row_to_public(r) if r else None


def save_qa(**kw) -> str:
    qid = kw.get("id") or uuid.uuid4().hex[:12]
    with connect() as c:
        c.execute(
            """INSERT INTO qa (id, question, question_key, answer, created_at, provider, model,
                               sources, external, corpus_settles, public, withheld_reason, verify,
                               prompt_tokens, completion_tokens, cost_usd, parent_id)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                qid, kw["question"], normalise(kw["question"]), kw["answer"], time.time(),
                kw["provider"], kw["model"], json.dumps(kw.get("sources", [])),
                json.dumps(kw.get("external", [])), int(kw.get("corpus_settles", True)),
                int(kw.get("public", True)), kw.get("withheld_reason"),
                json.dumps(kw.get("verify", {})), kw.get("prompt_tokens", 0),
                kw.get("completion_tokens", 0), kw.get("cost_usd", 0.0), kw.get("parent_id"),
            ),
        )
    return qid


def log_turn(**kw) -> str:
    tid = uuid.uuid4().hex[:12]
    with connect() as c:
        c.execute(
            """INSERT INTO turns (id, conversation, qa_id, question, answer, sources, external,
                                  provider, model, created_at, cached, corpus_settles, verify,
                                  prompt_tokens, completion_tokens, cost_usd)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                tid, kw["conversation"], kw.get("qa_id"), kw["question"], kw["answer"],
                json.dumps(kw.get("sources", [])), json.dumps(kw.get("external", [])),
                kw["provider"], kw["model"], time.time(), int(kw.get("cached", False)),
                int(kw.get("corpus_settles", True)), json.dumps(kw.get("verify", {})),
                kw.get("prompt_tokens", 0), kw.get("completion_tokens", 0), kw.get("cost_usd", 0.0),
            ),
        )
    return tid


def get(qa_id: str, bump_view: bool = False) -> dict | None:
    with connect() as c:
        if bump_view:
            c.execute("UPDATE qa SET views = views + 1 WHERE id=?", (qa_id,))
        r = c.execute("SELECT * FROM qa WHERE id=?", (qa_id,)).fetchone()
        return _row_to_public(r) if r else None


def vote(qa_id: str, voter: str, helpful: bool) -> dict | None:
    with connect() as c:
        c.execute(
            "INSERT INTO votes (qa_id, voter, helpful, at) VALUES (?,?,?,?) "
            "ON CONFLICT(qa_id, voter) DO UPDATE SET helpful=excluded.helpful, at=excluded.at",
            (qa_id, voter, int(helpful), time.time()),
        )
        agg = c.execute(
            "SELECT SUM(helpful) AS up, COUNT(*) - SUM(helpful) AS down FROM votes WHERE qa_id=?",
            (qa_id,),
        ).fetchone()
        c.execute("UPDATE qa SET up=?, down=? WHERE id=?",
                  (agg["up"] or 0, agg["down"] or 0, qa_id))
        r = c.execute("SELECT * FROM qa WHERE id=?", (qa_id,)).fetchone()
        return _row_to_public(r) if r else None


def listing(limit: int = 50) -> list[dict]:
    """Public Q&A, ranked. Ranking is computed in Python, not SQL, so the rule stays readable."""
    with connect() as c:
        rows = c.execute("SELECT * FROM qa WHERE public=1").fetchall()
    items = [_row_to_public(r) for r in rows]
    items.sort(key=lambda x: (-x["rank"], -x["createdAt"]))
    return items[:limit]


def usage_totals() -> dict:
    with connect() as c:
        r = c.execute(
            "SELECT COUNT(*) n, SUM(prompt_tokens) pt, SUM(completion_tokens) ct, SUM(cost_usd) c "
            "FROM turns WHERE cached=0"
        ).fetchone()
        cached = c.execute("SELECT COUNT(*) n FROM turns WHERE cached=1").fetchone()["n"]
    return {
        "modelCalls": r["n"] or 0,
        "cachedServes": cached or 0,
        "promptTokens": r["pt"] or 0,
        "completionTokens": r["ct"] or 0,
        "costUsd": round(r["c"] or 0.0, 4),
    }

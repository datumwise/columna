"""SQLite storage: answers, review state, votes, views, conversations.

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

from . import citations, standing

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
  -- `public` STOPPED MEANING "published" on 2026-08-26. It is now REVIEW ELIGIBILITY: whether this
  -- answer may be put in front of a reviewer at all. The privacy/abuse filter that used to decide
  -- publication now decides candidacy, and publication is decided by a human. See standing.py.
  public        INTEGER NOT NULL DEFAULT 1,
  withheld_reason TEXT,
  standing      TEXT NOT NULL DEFAULT 'provisional',   -- provisional | reviewed
  published     INTEGER NOT NULL DEFAULT 0,            -- only a human approval sets this
  reviewed_at   REAL,
  reviewed_by   TEXT,
  verify        TEXT NOT NULL DEFAULT '{}', -- JSON: the identifier gate's verdict
  prompt_tokens INTEGER NOT NULL DEFAULT 0,
  completion_tokens INTEGER NOT NULL DEFAULT 0,
  cost_usd      REAL NOT NULL DEFAULT 0.0,
  parent_id     TEXT                        -- set when this was asked as a follow-up
);
CREATE INDEX IF NOT EXISTS qa_key    ON qa(question_key);
CREATE INDEX IF NOT EXISTS qa_public ON qa(public);
CREATE INDEX IF NOT EXISTS qa_stand ON qa(standing, published);

-- ── THE TECHNICAL CACHE (2026-08-26) ────────────────────────────────────────────────────────────
-- A cache entry and a published Q&A are different objects with different lifetimes, different
-- owners and different meanings, and they were the same row until today. `find_cached` selected
-- `WHERE public=1`, so "have we answered this before, cheaply?" and "is this a datumwise
-- publication?" were the same question. They are not: reuse is a COST decision made by the service,
-- publication is an EDITORIAL decision made by a person.
--
-- Consequences of the split, all wanted: a cache entry expires and a publication does not; a cache
-- entry carries no reputation; unpublishing an answer does not make the service re-pay for it; and
-- the cache can be dropped wholesale without touching the public collection.
CREATE TABLE IF NOT EXISTS answer_cache (
  question_key TEXT PRIMARY KEY,
  qa_id        TEXT NOT NULL,
  created_at   REAL NOT NULL,
  expires_at   REAL NOT NULL,
  model        TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS cache_exp ON answer_cache(expires_at);

-- ── REVIEW (2026-08-26) ─────────────────────────────────────────────────────────────────────────
-- One row per review pass. Reviews ACCUMULATE: a second pass does not overwrite the first, because
-- the interesting thing about a re-review is usually that it disagreed with the last one.
--
-- `proposed_answer` is the reviewer's proposal for publication. It is stored HERE and never written
-- back into qa.answer. The provisional answer is the evidence of what the agent said when asked,
-- and an evidence record that can be silently edited is not one.
CREATE TABLE IF NOT EXISTS reviews (
  id              TEXT PRIMARY KEY,
  qa_id           TEXT NOT NULL,
  created_at      REAL NOT NULL,
  disposition     TEXT NOT NULL,           -- APPROVE | REVISE | DO_NOT_PUBLISH
  findings        TEXT NOT NULL DEFAULT '{}',
  summary         TEXT NOT NULL DEFAULT '',
  changes         TEXT NOT NULL DEFAULT '[]',
  proposed_answer TEXT,
  model           TEXT NOT NULL,
  cost_usd        REAL NOT NULL DEFAULT 0.0
);
CREATE INDEX IF NOT EXISTS reviews_qa ON reviews(qa_id, created_at);

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


_ADDED_COLUMNS = (
    ("standing", "TEXT NOT NULL DEFAULT 'provisional'"),
    ("published", "INTEGER NOT NULL DEFAULT 0"),
    ("reviewed_at", "REAL"),
    ("reviewed_by", "TEXT"),
    # The text that was actually published. May be the provisional answer, the reviewer's proposal,
    # or the human's edit of either. Kept SEPARATE from `answer`, which is never rewritten.
    ("published_answer", "TEXT"),
    ("rejected_at", "REAL"),
    ("rejected_by", "TEXT"),
    ("reject_reason", "TEXT"),
    # The passage text the answer was actually built on. Without it the reviewer cannot verify a
    # direct quotation, and verifying against a fresh retrieval would check the answer against
    # evidence it never saw.
    ("evidence", "TEXT NOT NULL DEFAULT '[]'"),
)


def _migrate(c: sqlite3.Connection) -> None:
    """Additive only. Existing rows become provisional and unpublished, which is the truthful
    reading of them: nothing in the table was ever approved by a human, because until 2026-08-26
    nothing had to be."""
    have = {r["name"] for r in c.execute("PRAGMA table_info(qa)")}
    for name, decl in _ADDED_COLUMNS:
        if name not in have:
            c.execute(f"ALTER TABLE qa ADD COLUMN {name} {decl}")


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=15)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.executescript(SCHEMA)
    _migrate(c)
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
    """One row, rendered for a reader — WITH its standing, and with reputation only if it earned it.

    A provisional answer may collect votes internally (they are useful signal for whoever reviews
    it) but it does not get a public star reputation, because a reputation on an unreviewed answer
    reads as endorsement. So stars/rank/ratings are present on reviewed rows and null on
    provisional ones, rather than being computed and quietly ignored by an interface.
    """
    up, down = r["up"], r["down"]
    st = (r["standing"] if "standing" in r.keys() else standing.PROVISIONAL) or standing.PROVISIONAL
    reviewed_at = r["reviewed_at"] if "reviewed_at" in r.keys() else None
    is_reviewed = st == standing.REVIEWED
    return {
        "id": r["id"],
        "question": r["question"],
        # A reader of a REVIEWED item sees the published text; the provisional answer stays
        # available as `provisionalAnswer` so the record of what the agent said is never lost.
        "answer": (r["published_answer"] if ("published_answer" in r.keys()
                                             and r["published_answer"]) else r["answer"]),
        "provisionalAnswer": r["answer"],
        "evidence": json.loads(r["evidence"]) if "evidence" in r.keys() else [],
        "createdAt": r["created_at"],
        # CURRENT standing, re-derived from the registry on every read — not the sentence that was
        # true on the day the answer was written. Each entry keeps `standingAtAnswer` for audit and
        # gains `supersededSinceAnswer`. See citations.py.
        "sources": citations.resolve(json.loads(r["sources"])),
        "external": json.loads(r["external"]),
        "corpusSettles": bool(r["corpus_settles"]),
        "standing": st,
        # A published answer whose citations have been superseded since it was written. The reviewer
        # sees it before publishing; a reader deserves it on an old answer.
        "citationsSuperseded": citations.any_superseded(
            citations.resolve(json.loads(r["sources"]))),
        "notice": standing.notice(st, reviewed_at),
        "published": bool(r["published"]) if "published" in r.keys() else False,
        "views": r["views"] if is_reviewed else None,
        "ratings": (up + down) if is_reviewed else None,
        "up": up,
        "down": down,
        "stars": stars(up, down) if is_reviewed else None,
        "model": r["model"],
        "provider": r["provider"],
        "rank": round(rank(r["views"], up, down), 4) if is_reviewed else None,
    }


CACHE_TTL_DAYS = float(os.environ.get("ASK_CACHE_TTL_DAYS", "14"))


def find_cached(question: str) -> dict | None:
    """Technical reuse. Expires; carries no reputation; says nothing about publication."""
    with connect() as c:
        r = c.execute(
            "SELECT qa.* FROM answer_cache JOIN qa ON qa.id = answer_cache.qa_id "
            "WHERE answer_cache.question_key=? AND answer_cache.expires_at > ?",
            (normalise(question), time.time()),
        ).fetchone()
        return _row_to_public(r) if r else None


def cache_put(question: str, qa_id: str, model: str, ttl_days: float | None = None) -> None:
    """Remember that this question has an answer, for a while. Idempotent per question."""
    now = time.time()
    ttl = (CACHE_TTL_DAYS if ttl_days is None else ttl_days) * 86_400
    with connect() as c:
        c.execute(
            "INSERT INTO answer_cache (question_key, qa_id, created_at, expires_at, model) "
            "VALUES (?,?,?,?,?) ON CONFLICT(question_key) DO UPDATE SET "
            "qa_id=excluded.qa_id, created_at=excluded.created_at, expires_at=excluded.expires_at, "
            "model=excluded.model",
            (normalise(question), qa_id, now, now + ttl, model),
        )


def cache_purge(before: float | None = None) -> int:
    """Drop expired entries. Never touches qa: the answers themselves are evidence and are kept."""
    with connect() as c:
        cur = c.execute("DELETE FROM answer_cache WHERE expires_at <= ?", (before or time.time(),))
        return cur.rowcount


def cache_drop_all() -> int:
    """Drop EVERY cache entry. The thing you run when the corpus moves underneath it.

    A cached answer is a promise that asking again would produce the same thing. Supersede a work,
    re-rule a source, or rebuild the index, and that promise is void: the entry would go on serving
    a pre-supersession answer, with pre-supersession citations, for up to its full TTL — and a
    reader would have no way to tell. Expiry is the wrong instrument here because expiry measures
    time and this is not about time.

    Only cache rows are dropped. The answers stay: they are evidence of what Ask said on a day when
    the corpus said something else, which is exactly the record that must not be erased.
    """
    with connect() as c:
        return c.execute("DELETE FROM answer_cache").rowcount


def save_qa(**kw) -> str:
    qid = kw.get("id") or uuid.uuid4().hex[:12]
    with connect() as c:
        c.execute(
            """INSERT INTO qa (id, question, question_key, answer, created_at, provider, model,
                               sources, external, corpus_settles, public, withheld_reason, verify,
                               prompt_tokens, completion_tokens, cost_usd, parent_id,
                               standing, published, evidence)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                qid, kw["question"], normalise(kw["question"]), kw["answer"], time.time(),
                kw["provider"], kw["model"], json.dumps(kw.get("sources", [])),
                json.dumps(kw.get("external", [])), int(kw.get("corpus_settles", True)),
                int(kw.get("public", True)), kw.get("withheld_reason"),
                json.dumps(kw.get("verify", {})), kw.get("prompt_tokens", 0),
                kw.get("completion_tokens", 0), kw.get("cost_usd", 0.0), kw.get("parent_id"),
                # Every answer is born provisional and unpublished. There is no argument the
                # caller can pass to change that; publication is an act a human performs later.
                standing.PROVISIONAL, 0, json.dumps(kw.get("evidence", [])),
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
    """The public Q&A collection: REVIEWED AND PUBLISHED only.

    This used to be `WHERE public=1`, which meant every fresh answer that passed a privacy filter
    entered the public collection the moment it was generated. Ranking is computed in Python, not
    SQL, so the rule stays readable.
    """
    with connect() as c:
        rows = c.execute(
            "SELECT * FROM qa WHERE standing=? AND published=1", (standing.REVIEWED,)
        ).fetchall()
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


# ── REVIEW AND PUBLICATION ────────────────────────────────────────────────────────────────────────
# The one rule these functions exist to enforce: qa.answer is never written after creation. Publish
# writes qa.published_answer. Nothing here can silently change what the agent said.

def save_review(qa_id: str, verdict: dict) -> str:
    rid = uuid.uuid4().hex[:12]
    with connect() as c:
        c.execute(
            """INSERT INTO reviews (id, qa_id, created_at, disposition, findings, summary, changes,
                                    proposed_answer, model, cost_usd)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (rid, qa_id, time.time(), verdict["disposition"],
             json.dumps(verdict.get("findings", {})), verdict.get("summary", ""),
             json.dumps(verdict.get("changes", [])), verdict.get("proposedAnswer"),
             verdict.get("model", ""), float(verdict.get("costUsd") or 0.0)),
        )
    return rid


def _review_row(r: sqlite3.Row) -> dict:
    return {
        "id": r["id"], "qaId": r["qa_id"], "createdAt": r["created_at"],
        "disposition": r["disposition"], "findings": json.loads(r["findings"]),
        "summary": r["summary"], "changes": json.loads(r["changes"]),
        "proposedAnswer": r["proposed_answer"], "model": r["model"], "costUsd": r["cost_usd"],
    }


def reviews_for(qa_id: str) -> list[dict]:
    with connect() as c:
        rows = c.execute(
            "SELECT * FROM reviews WHERE qa_id=? ORDER BY created_at DESC", (qa_id,)
        ).fetchall()
    return [_review_row(r) for r in rows]


def latest_review(qa_id: str) -> dict | None:
    rs = reviews_for(qa_id)
    return rs[0] if rs else None


def review_queue(limit: int = 50) -> list[dict]:
    """Candidates awaiting a human: eligible, provisional, not already rejected.

    `public=1` is the eligibility flag — it stopped meaning "published" on 2026-08-26 and now means
    "may be put in front of a reviewer". A rejected answer stays in the table as evidence but leaves
    the queue; re-queueing it is a deliberate act, not a refresh.
    """
    with connect() as c:
        rows = c.execute(
            "SELECT * FROM qa WHERE standing=? AND published=0 AND public=1 AND rejected_at IS NULL "
            "AND parent_id IS NULL ORDER BY created_at DESC LIMIT ?",
            (standing.PROVISIONAL, limit),
        ).fetchall()
    out = []
    for r in rows:
        item = _row_to_public(r)
        item["review"] = latest_review(r["id"])
        out.append(item)
    return out


def publish(qa_id: str, reviewer: str, answer_text: str | None = None) -> dict | None:
    """A HUMAN approves. The published text may differ from the provisional one; both are kept."""
    with connect() as c:
        r = c.execute("SELECT * FROM qa WHERE id=?", (qa_id,)).fetchone()
        if not r:
            return None
        c.execute(
            "UPDATE qa SET standing=?, published=1, reviewed_at=?, reviewed_by=?, "
            "published_answer=?, rejected_at=NULL, rejected_by=NULL, reject_reason=NULL WHERE id=?",
            (standing.REVIEWED, time.time(), reviewer, answer_text or r["answer"], qa_id),
        )
    return get(qa_id)


def reject(qa_id: str, reviewer: str, reason: str) -> dict | None:
    """Not published. The answer is KEPT — a rejected answer is evidence about the agent."""
    with connect() as c:
        if not c.execute("SELECT 1 FROM qa WHERE id=?", (qa_id,)).fetchone():
            return None
        c.execute(
            "UPDATE qa SET published=0, standing=?, rejected_at=?, rejected_by=?, reject_reason=? "
            "WHERE id=?",
            (standing.PROVISIONAL, time.time(), reviewer, reason, qa_id),
        )
    return get(qa_id)

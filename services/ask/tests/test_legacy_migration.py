"""OPENING A DATABASE WRITTEN BY THE PRE-2026-08-26 SCHEMA.

Found in production on 2026-08-26, in the first minute of release v7, and it could not have been
found anywhere else.

`CREATE INDEX IF NOT EXISTS qa_stand ON qa(standing, published)` lived in SCHEMA, and SCHEMA runs
BEFORE _migrate. On a table created by the older schema those columns do not exist yet, so
`IF NOT EXISTS` does not save the statement — the index genuinely is absent, sqlite proceeds, and
fails on the COLUMN:

    sqlite3.OperationalError: no such column: standing

out of connect(), which every read and every write passes through. The machine came up, `/health`
returned 200 because it never touches the database, and every other route returned 500.

WHY NO TEST CAUGHT IT. Every local and test database is created fresh from SCHEMA, whose CREATE TABLE
already declares `standing` and `published`. The migration branch was therefore never taken by any
test in the suite: `_migrate` ran, found every column present, and did nothing. The only file in
existence with rows written by the older schema is on the Fly volume.

So the fixture here is the old schema, retyped. It is a LITERAL on purpose, for the same reason the
acceptance rows in check_publications.py are: a fixture that generated the old schema from the new
one would be asserting that the two are the same, which is the opposite of the thing under test. It
does not track SCHEMA and it must not — it is a historical artifact, and it is frozen at what the
deployed database actually contains.

The rule this file enforces: SCHEMA may only reference columns CREATE TABLE itself declares.
Anything depending on a migrated column belongs in POST_MIGRATION_SCHEMA.
"""

from __future__ import annotations

import sqlite3

import pytest

from ask import store

# The qa/reviews tables EXACTLY as they stood before 2026-08-26. Frozen; do not regenerate.
LEGACY_SCHEMA = """
CREATE TABLE qa (
  id            TEXT PRIMARY KEY,
  question      TEXT NOT NULL,
  question_key  TEXT NOT NULL,
  answer        TEXT NOT NULL,
  created_at    REAL NOT NULL,
  provider      TEXT NOT NULL,
  model         TEXT NOT NULL,
  sources       TEXT NOT NULL,
  external      TEXT NOT NULL DEFAULT '[]',
  corpus_settles INTEGER NOT NULL DEFAULT 1,
  views         INTEGER NOT NULL DEFAULT 0,
  up            INTEGER NOT NULL DEFAULT 0,
  down          INTEGER NOT NULL DEFAULT 0,
  public        INTEGER NOT NULL DEFAULT 1,
  withheld_reason TEXT,
  verify        TEXT NOT NULL DEFAULT '{}',
  prompt_tokens INTEGER NOT NULL DEFAULT 0,
  completion_tokens INTEGER NOT NULL DEFAULT 0,
  cost_usd      REAL NOT NULL DEFAULT 0.0,
  parent_id     TEXT
);
CREATE INDEX qa_key    ON qa(question_key);
CREATE INDEX qa_public ON qa(public);
CREATE TABLE reviews (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  qa_id      TEXT NOT NULL,
  created_at REAL NOT NULL
);
"""


@pytest.fixture()
def legacy_db(tmp_path, monkeypatch):
    """A database with one row written under the old meaning of `public`."""
    p = tmp_path / "legacy.db"
    c = sqlite3.connect(p)
    c.executescript(LEGACY_SCHEMA)
    c.execute(
        "INSERT INTO qa (id,question,question_key,answer,created_at,provider,model,sources,views)"
        " VALUES (?,?,?,?,?,?,?,?,?)",
        ("legacy01", "What are the four moods?", "what are the four moods",
         "The four moods are serve, disclose, clarify and refuse.", 0.0,
         "openai", "gpt-5", "[]", 4),
    )
    c.commit()
    c.close()
    monkeypatch.setattr(store, "DB_PATH", p)
    return p


def test_a_legacy_database_can_be_opened_at_all(legacy_db):
    """The production failure, as one line. Without the fix this raises OperationalError."""
    with store.connect() as c:
        assert c.execute("SELECT count(*) FROM qa").fetchone()[0] == 1


def test_the_index_over_migrated_columns_is_created_after_the_migration(legacy_db):
    with store.connect() as c:
        names = {r["name"] for r in c.execute("PRAGMA index_list(qa)")}
    assert "qa_stand" in names, "the index must exist once its columns do"


def test_schema_never_references_a_column_create_table_does_not_declare():
    """The rule, asserted directly, so the next person cannot reintroduce the shape.

    Checked textually against SCHEMA rather than by running it, because running it against a fresh
    database is exactly the thing that hides this defect.
    """
    migrated = {name for name, _ in store._ADDED_COLUMNS}
    body = store.SCHEMA
    offenders = [col for col in migrated
                 if f"ON qa({col}" in body or f", {col})" in body or f"({col})" in body]
    assert not offenders, (
        f"SCHEMA references migrated column(s) {offenders}; they belong in POST_MIGRATION_SCHEMA")


def test_a_legacy_row_becomes_provisional_and_leaves_the_public_collection(legacy_db):
    """Not a defect — the ruled reading, asserted so it is a decision and not a surprise.

    Before 2026-08-26 `public=1` meant "auto-published", and nothing in the table had ever been
    approved by a person. Under the standing model those rows are provisional and unpublished, so
    they leave the public collection and enter the review queue. The ANSWER is not touched: it can
    be reviewed and published at any time, by a human, through the real path.
    """
    assert store.listing() == []
    queue = store.review_queue()
    assert len(queue) == 1 and queue[0]["id"] == "legacy01"
    with store.connect() as c:
        r = c.execute("SELECT answer, standing, published FROM qa WHERE id='legacy01'").fetchone()
    assert r["standing"] == "provisional" and r["published"] == 0
    assert r["answer"] == "The four moods are serve, disclose, clarify and refuse."


def test_a_legacy_rows_views_are_hidden_rather_than_reassigned(legacy_db):
    """Its 4 views were counted under a regime where nothing was reviewed. They are not moved into
    `provisional_views` — reassigning history is the specific thing the view ruling forbids — they
    simply stop being shown, because views are only shown on a reviewed object."""
    with store.connect() as c:
        r = c.execute("SELECT views, provisional_views FROM qa WHERE id='legacy01'").fetchone()
    assert (r["views"], r["provisional_views"]) == (4, 0)
    assert store.get("legacy01")["views"] is None

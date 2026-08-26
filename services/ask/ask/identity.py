"""PUBLICATION IDENTITY AND CURRENCY — the one class of question the corpus cannot answer about itself.

WHY THIS MODULE EXISTS (Huayin, ruling C of 2026-08-26, after F1).

Three cases failed on BOTH models for one structural reason, and the reason is not similarity
ranking. `h2` told a reader that a superseded edition was datumwise's current position. `r6` gave
the SUPERSEDED title as the current title while giving the current version and DOI correctly, in
one sentence. In both, the evidence the model leaned on was a passage inside ANOTHER paper that
names this work — a reference list, a reading path, a "where to go next" pointer.

    Other papers' pointers carry stale titles and versions of the work being asked about, and for
    identity and currency questions they out-rank the work's own current deposit.

THE PASSAGE IS NOT WRONG, AND THAT IS THE WHOLE DIFFICULTY. The Frame-QL Primer's reading path says
"Analytical Governance, Version 1.1" because that is what it was called when the Primer was
deposited. It is authoritative — as part of the Primer. It is not thereby authority for what
Analytical Governance is called TODAY. Demoting it in the ranking would be treating a question of
ENTITLEMENT as a question of score, and would leave it entitled to answer the moment nothing else
scored, which is exactly the case where citing it does the most damage.

AND THE DEEPER CAUSE IS OURS. index_build.py deliberately keeps publication facts OUT of the index
— it stores foreign keys, never a title, version or DOI — because a fact copied into a build
artifact is a second source of truth for it, and G7 was right to reject that. The consequence went
unnoticed until F1: having removed the fact from every passage, we then asked the agent questions
that ONLY that fact can answer, and handed it nothing entitled to carry it. The agent did what
anyone would do and read the title off the nearest piece of prose that had one.

So the repair is not a filter. It is a SOURCE — the registry itself, presented as its own class,
with its own token namespace and its own entitlement:

    [S#]  datumwise passages     — what the corpus says.
    [X#]  external sources       — the outside world.
    [R#]  the publication registry — what a work is CALLED, which version is CURRENT, and which DOI
                                     resolves to it. Carries no argument and settles no doctrine.

[R#] rather than a fourth `layer` on [S#] for the same reason [X#] is not a layer (see skill.py):
the cheapest way to make a model keep two classes apart is to never let them share a namespace.
A registry card is also not a catalogued source — it has no deposit, no route and no text of its
own — so filing it as one would have made the source catalog claim a member it does not have.

WHAT IT IS NOT. It is not a fifth retrieval signal, and it does not touch scoring. It fires only
when the question is ABOUT publication identity or currency, and it never suppresses the corpus.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RECORDS_JSON = REPO / "registry" / "publications" / "records.json"
WORKS_JSON = REPO / "registry" / "publications" / "works.json"
SOURCES_JSON = REPO / "registry" / "sources" / "sources.json"


# ── the question class ────────────────────────────────────────────────────────────────────────────
# Two families, deliberately kept in one list because the ruling keeps them in one list: what a work
# is CALLED / which version is CURRENT (identity), and whether what I am looking at is still the
# position (currency). Cues, not a classifier: this is the same shape as ROADMAP_CUES and
# CITATION_CUES in retrieve.py, and it is auditable by reading it.
IDENTITY_CUES = (
    # identity
    "what is it called", "what's it called", "what is it named", "called now",
    "what is the title", "what's the title", "current title", "retitled", "renamed",
    "paper called", "work called", "publication called",
    # version / edition / record
    "what version", "which version", "what edition", "which edition", "current version",
    "current edition", "latest version", "newest version", "most recent version",
    "current record", "version is current", "edition is current", "still the latest",
    # currency of a thing in front of the reader
    "current position", "still current", "still the current", "is that current", "is this current",
    "is that the current", "is this the current", "still datumwise's", "up to date",
    "out of date", "superseded", "supersede", "still the position", "current doctrine",
    # the identifier itself
    "doi", "zenodo record",
)

_VERSION_RE = re.compile(r"\b(?:v|ver\.?|version)\s*([0-9]+\.[0-9]+)\b", re.I)


def asks_identity(query: str) -> bool:
    """Is this a question about what a work is called, which version is current, or whether the
    thing in front of the reader is still the position?"""
    q = query.lower()
    return any(c in q for c in IDENTITY_CUES)


# ── resolving WHICH work the question is about ───────────────────────────────────────────────────
def _norm(s: str) -> str:
    s = re.sub(r"[—–]", "-", s.lower())
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return re.sub(r"^the ", "", s)


@lru_cache(maxsize=1)
def _registry() -> tuple[list[dict], dict[str, dict], dict[str, list[dict]]]:
    records = json.loads(RECORDS_JSON.read_text())
    works = {w["workId"]: w for w in json.loads(WORKS_JSON.read_text())}
    by_work: dict[str, list[dict]] = {}
    for r in records:
        by_work.setdefault(r["workId"], []).append(r)
    for rs in by_work.values():
        rs.sort(key=lambda r: (r.get("date") or "", r.get("version") or ""))
    return records, works, by_work


@lru_cache(maxsize=1)
def _names() -> list[tuple[str, str]]:
    """(normalised name, workId), longest first.

    EVERY name the work has EVER been published under is a key, not only the current one. A reader
    asking "is the Theory of Certainty still current?" is asking about a work whose current title no
    longer contains those words, and a name index built only from current titles would fail to
    recognise precisely the question this module exists to answer. Subtitles are indexed as their
    own keys too, because a bibliography prints the whole thing and a person prints the short part.
    """
    _, works, by_work = _registry()
    seen: dict[str, str] = {}

    def add(name: str | None, work_id: str) -> None:
        if not name:
            return
        for part in [name, name.split(":")[0]]:
            n = _norm(part)
            if len(n) >= 8:
                seen.setdefault(n, work_id)

    for wid, w in works.items():
        add(w.get("canonicalLabel"), wid)
    for wid, rs in by_work.items():
        for r in rs:
            add(r.get("title"), wid)
    for s in json.loads(SOURCES_JSON.read_text())["sources"]:
        if s.get("workId"):
            add(s.get("title"), s["workId"])
    return sorted(seen.items(), key=lambda kv: -len(kv[0]))


def works_named(query: str) -> list[str]:
    """Which works this question names, by any title they have ever carried. Longest match wins."""
    q = f" {_norm(query)} "
    out: list[str] = []
    claimed: list[str] = []
    for name, wid in _names():
        if f" {name} " in q and not any(name in c for c in claimed):
            claimed.append(name)
            if wid not in out:
                out.append(wid)
    return out


def edition_named(query: str, work_id: str) -> dict | None:
    """The record of `work_id` this question names by version, if it names one."""
    _, _, by_work = _registry()
    wanted = {m.group(1) for m in _VERSION_RE.finditer(query)}
    if not wanted:
        return None
    for r in by_work.get(work_id, []):
        if r.get("version") in wanted:
            return r
    return None


def names_superseded_edition(query: str) -> bool:
    """Does this question name, by version, an edition that is no longer current?

    THIS IS THE HISTORICAL-QUESTION DETECTOR THE CUE LIST COULD NOT BE (ruling D). `h4` asks "What
    did version 1.1 of Analytical Governance argue?" — as explicit a historical question as one can
    write — and opened NOTHING, because `historical` was cued on phrases like "used to say" and
    "back then". Naming a superseded edition by its number is the plainest way a person asks a
    historical question about a publication, and it was the one way that did not work.

    Registry-derived, not a cue: it is true exactly when the version named is a version the registry
    rules superseded, so it becomes true for a new work the day that work is superseded and needs no
    edit here.
    """
    for wid in works_named(query):
        r = edition_named(query, wid)
        if r and r.get("status") == "superseded":
            return True
    return False


# ── the card ──────────────────────────────────────────────────────────────────────────────────────
STANDING = (
    "REGISTRY RECORD — datumwise's publication registry, read from registry/publications at the "
    "moment this question was asked. It is the authority for what this work is CURRENTLY CALLED, "
    "which version is current, which DOI resolves to it, and which editions it has superseded. It "
    "carries no argument: it establishes nothing about what the work SAYS, and it may not be used "
    "to settle a question of doctrine."
)


def record_card(work_id: str) -> dict | None:
    """The registry's own account of one work's identity and currency, as a readable block."""
    _, works, by_work = _registry()
    w, rs = works.get(work_id), by_work.get(work_id) or []
    if not w or not rs:
        return None
    current = next((r for r in rs if r.get("status") == "current"), None)
    if not current:
        return None
    older = [r for r in rs if r is not current]

    def line(r: dict) -> str:
        return (f"v{r.get('version')} ({r.get('date')}, doi:{r.get('doi')}) — deposited under the "
                f"title \"{r.get('title')}\"")

    body = [
        f"datumwise work: {w['canonicalLabel']} (editorial label; internal id {work_id}).",
        f"CURRENT RECORD: {line(current)}.",
    ]
    if older:
        body.append(
            "SUPERSEDED RECORDS, preserved and still resolvable — a citation made to one of these "
            "while it was current still resolves to the words that were actually cited:")
        body += [f"  · {line(r)}" for r in reversed(older)]
    else:
        body.append("This work has one record; nothing has been superseded.")
    body.append(
        "An editorial label and a deposited title are different facts. The label is what datumwise "
        "calls the work; the title is what was published under that DOI. Neither is derived from "
        "the other, and a superseded record keeps its own title forever.")
    return {
        "workId": work_id,
        "label": w["canonicalLabel"],
        "currentRecordId": current["recordId"],
        "url": f"https://doi.org/{current['doi']}" if current.get("doi") else "",
        "standing": STANDING,
        "text": "\n".join(body),
    }


def cards_for(query: str) -> list[dict]:
    """The registry cards this question is entitled to, or none.

    Both conditions, and the conjunction is the point: a question that merely MENTIONS a work is not
    a question about that work's identity, and a currency question that names no work has nothing to
    look up. Either alone would put the registry in front of the model on questions it has no
    business answering.
    """
    if not asks_identity(query):
        return []
    return [c for c in (record_card(w) for w in works_named(query)[:3]) if c]

"""Durable citations: keep the identity, re-resolve the standing.

THE ERROR THIS REMOVES (Huayin, 2026-08-26). Ask treats publication facts as foreign keys while it
is answering — the index stores record ids and retrieve.py splices version, date and DOI in from the
registry on every request, so a reader physically cannot be handed a stale identifier. Then an
answer becomes a durable object and all of that is thrown away: `qa.sources` stored the RESOLVED
standing sentence as text. Currency survived retrieval and died at publication.

The servability candidate found it. Its four citations read, as literal stored text, that
Analytical Governance v1.1 was the current record. Publish that and the sentence is on a public page
permanently; on 2026-08-26, when v2.0 superseded v1.1, it became false with nothing anywhere to
notice. The identifier is deliberately not repeated here — a publication fact echoed into a
docstring is the same defect one echoed into a page, and registry/publications/consumers.json exists
to keep that surface small.

    Carrying a resolved presentation, rather than the identity from which current truth can be
    resolved, is the same class of error corrected repeatedly elsewhere in this repo.

WHAT IS PRESERVED, AND IT IS BOTH:

  standingAtAnswer   the sentence exactly as it read when the answer was written. History is not
                     rewritten: the answer really did cite v1.1 as current, because on that day it
                     was, and an audit must be able to see that.
  standing           re-resolved from the registry now, at render/review time. A public page never
                     goes on calling a superseded record current.

plus `supersededSinceAnswer`, which is the interesting fact neither sentence states on its own: this
citation was current when written and is not current now. That is the flag a reviewer needs before
publishing, and the one a reader deserves on an old answer.

Identity is what gets stored — sourceId, the record whose text was quoted, and the record that was
current at the time. Everything else is derived on the way out.

THE LABEL IS THE SAME DEFECT, ONE FIELD OVER (Huayin, ruling 1 of 2026-08-26, 15:59).

  Identity is durable; current presentation is resolved.

`label` was stored as text, so when the editorial label for Analytical Governance changed from the
superseded edition's full title to "Analytical Governance", every durable citation went on displaying
the old one — exactly as citations used to go on displaying a superseded standing sentence. So:

  labelAtAnswer   the presentation label as it was shown when the answer was created. Preserved for
                  audit; never recomputed.
  label           resolved now, from sourceId -> the source's workId -> canonicalLabel.

plus `labelChangedSinceAnswer`, the fact neither string states on its own.

SIX FACTS, AND THEY ARE SIX (the ruling is explicit that these must not collapse):

  1  the record whose words were cited          readableRecordId   — identity, stored
  2  the record current at answer time          currentRecordIdAtAnswer — identity, stored
  3  the record currently authoritative         currentRecordId    — identity, resolved
  4  the standing sentence as it read then      standingAtAnswer   — presentation, stored
  5  the standing sentence now                  standing           — presentation, resolved
  6  the label then / the label now             labelAtAnswer / label — presentation, both

A label is presentation and nothing else. `canonicalLabel` is EDITORIAL NAMING at the Work level, so
re-resolving it cannot and does not move which record was cited: (1) and (2) are untouched by a
rename, and a label that changed is not a supersession. The two flags stay separate for that reason.

WHY THE EXPLICIT SOURCE TITLE STILL WINS FOR A NON-CURRENT EDITION. `index_build` already rules that
an explicitly titled source whose readable record is not the current record keeps its own title —
which is how "Analytical Governance v1.1, 21 August 2026" gets its dated name instead of the work's
label. That rule is REUSED here rather than a second one invented: re-resolving a citation of the
v1.1 text to the bare work label would make a preserved historical citation read as the current work.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_REG = Path(__file__).resolve().parents[3] / "registry"
RECORDS_JSON = _REG / "publications" / "records.json"
WORKS_JSON = _REG / "publications" / "works.json"
SOURCES_JSON = _REG / "sources" / "sources.json"


@lru_cache(maxsize=1)
def _records() -> tuple[dict[str, dict], dict[str, dict]]:
    recs = json.loads(RECORDS_JSON.read_text())
    by_id = {r["recordId"]: r for r in recs}
    current_by_work = {r["workId"]: r for r in recs if r.get("status") == "current"}
    return by_id, current_by_work


@lru_cache(maxsize=1)
def _naming() -> tuple[dict[str, dict], dict[str, str]]:
    """(source catalog by sourceId, canonicalLabel by workId) — the editorial naming layer.

    Read from the registry, never from the index: the index is a build artifact, and a label that
    could only be corrected by rebuilding it would be the stale fact this module exists to end.
    """
    srcs = json.loads(SOURCES_JSON.read_text())
    by_source = {s["sourceId"]: s for s in srcs["sources"]}
    labels = {w["workId"]: w["canonicalLabel"] for w in json.loads(WORKS_JSON.read_text())}
    return by_source, labels


def _label_now(source_id: str | None, readable_id: str | None, current_id: str | None) -> str | None:
    """The label this citation would be shown with today, or None if it cannot be derived."""
    if not source_id:
        return None
    by_source, labels = _naming()
    src = by_source.get(source_id)
    if src is None:
        return None
    work_id = src.get("workId")
    # An explicitly titled source pinned to a non-current edition keeps its own dated name.
    if src.get("title") and readable_id and current_id and readable_id != current_id:
        return src["title"]
    if work_id:
        return labels.get(work_id) or src.get("title")
    return src.get("title")


def _describe(record_id: str | None) -> str:
    by_id, _ = _records()
    r = by_id.get(record_id or "")
    if not r:
        return "an edition"
    v = f"v{r['version']}" if r.get("version") else "the first edition"
    doi = f", doi:{r['doi']}" if r.get("doi") else ""
    return f"{v} ({r.get('date', '')}{doi})"


def _splice(template: str, readable_id: str | None, current_id: str | None) -> str:
    s = template
    if "{CURRENT}" in s:
        s = s.replace("{CURRENT}", f"current record {_describe(current_id)}")
    if "{CURRENT_BARE}" in s:
        s = s.replace("{CURRENT_BARE}", _describe(current_id))
    if "{READABLE}" in s:
        s = s.replace("{READABLE}", _describe(readable_id))
    return s


def resolve(sources: list[dict]) -> list[dict]:
    """Stored citations in, citations with CURRENT standing out. Never mutates the stored row.

    A citation written before this shipped has no template and no record identity, only the frozen
    sentence. Those are passed through with `standing` unchanged and `resolvable: False` rather than
    guessed at — an unresolvable citation should say so, not quietly look fresh.
    """
    by_id, current_by_work = _records()
    out = []
    for s in sources:
        c = dict(s)
        frozen = c.get("standingAtAnswer") or c.get("standing")
        c["standingAtAnswer"] = frozen
        readable_id = c.get("readableRecordId")
        template = c.get("standingTemplate")
        if not template or not readable_id:
            c["resolvable"] = False
            c["supersededSinceAnswer"] = None
            # A citation can carry a resolvable NAME and an unresolvable STANDING: the standing
            # sentence needs record identity, the label needs only the source. Resolving what can be
            # resolved is not the same as guessing at what cannot.
            _resolve_label(c, readable_id, None)
            out.append(c)
            continue

        readable = by_id.get(readable_id)
        work_id = (readable or {}).get("workId")
        current_now = current_by_work.get(work_id) if work_id else None
        current_now_id = current_now["recordId"] if current_now else None

        c["resolvable"] = True
        c["currentRecordId"] = current_now_id
        c["standing"] = _splice(template, readable_id, current_now_id)
        _resolve_label(c, readable_id, current_now_id)
        # Was current when written, is not current now. Neither sentence says this on its own.
        c["supersededSinceAnswer"] = bool(
            current_now_id
            and c.get("currentRecordIdAtAnswer") == readable_id
            and current_now_id != readable_id
        )
        out.append(c)
    return out


def _resolve_label(c: dict, readable_id: str | None, current_id: str | None) -> None:
    """In place, on the COPY. Preserves what was shown and states what is shown now."""
    stored = c.get("labelAtAnswer") or c.get("label")
    c["labelAtAnswer"] = stored
    now = _label_now(c.get("sourceId"), readable_id, current_id)
    c["labelResolvable"] = now is not None
    c["label"] = now if now is not None else stored
    # NOT a supersession, and deliberately a different field: an editorial rename says nothing about
    # which record was cited. None when there is nothing to compare.
    c["labelChangedSinceAnswer"] = (bool(now and stored and now != stored)
                                    if (now and stored) else None)


def any_superseded(sources: list[dict]) -> bool:
    return any(s.get("supersededSinceAnswer") for s in sources)

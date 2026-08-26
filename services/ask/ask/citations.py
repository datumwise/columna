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
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

RECORDS_JSON = Path(__file__).resolve().parents[3] / "registry" / "publications" / "records.json"


@lru_cache(maxsize=1)
def _records() -> tuple[dict[str, dict], dict[str, dict]]:
    recs = json.loads(RECORDS_JSON.read_text())
    by_id = {r["recordId"]: r for r in recs}
    current_by_work = {r["workId"]: r for r in recs if r.get("status") == "current"}
    return by_id, current_by_work


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
            out.append(c)
            continue

        readable = by_id.get(readable_id)
        work_id = (readable or {}).get("workId")
        current_now = current_by_work.get(work_id) if work_id else None
        current_now_id = current_now["recordId"] if current_now else None

        c["resolvable"] = True
        c["currentRecordId"] = current_now_id
        c["standing"] = _splice(template, readable_id, current_now_id)
        # Was current when written, is not current now. Neither sentence says this on its own.
        c["supersededSinceAnswer"] = bool(
            current_now_id
            and c.get("currentRecordIdAtAnswer") == readable_id
            and current_now_id != readable_id
        )
        out.append(c)
    return out


def any_superseded(sources: list[dict]) -> bool:
    return any(s.get("supersededSinceAnswer") for s in sources)

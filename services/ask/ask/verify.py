"""The one hard gate in v0: identifiers must exist in the registry.

WHY THIS IS THE ONE MECHANISM AND NOT THE FIRST OF FORTY. Huayin's rule was to prefer instruction
and earn hard checks from observed failures. I agree for every failure class but one.

A confabulated DOI is different in kind from the other failures:
  · it is SILENT — the answer reads perfectly, with a plausible 10.5281/zenodo.######## shape;
  · it is PUBLIC — Ask is a public web service;
  · it is FALSIFIABLE BY A STRANGER — anyone can paste it into a browser and get a 404;
  · and it attacks precisely the asset datumwise is selling, which is that we do not misstate our
    own record.

The cost of waiting to observe that failure in production is paid in the only currency the project
cannot easily earn back. So this gate ships on day one. It is also nearly free — the registry is
right here, and this is the same shape as scripts/check_publications.py G1-G10, pointed at model
output instead of at the site.

WHAT IT DOES, AND WHAT IT DELIBERATELY DOES NOT DO. It does not rewrite the answer, silently repair
it, or retry behind the reader's back. It reports. `answer.py` decides what to do with the report,
and an answer that fails is never cached as public. Hiding a failure by patching the text would
destroy the evidence the whole prototype exists to gather.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RECORDS_JSON = REPO / "registry" / "publications" / "records.json"

DOI_RE = re.compile(r"10\.5281/zenodo\.\d+", re.I)
ZENODO_URL_RE = re.compile(r"zenodo\.org/records?/(\d+)", re.I)


@lru_cache(maxsize=1)
def _registry() -> tuple[set[str], set[str], dict[str, dict]]:
    records = json.loads(RECORDS_JSON.read_text())
    dois = {r["doi"].lower() for r in records if r.get("doi")}
    recids = {str(r["recid"]) for r in records if r.get("recid")}
    by_doi = {r["doi"].lower(): r for r in records if r.get("doi")}
    return dois, recids, by_doi


def check(answer: str, cited_urls: set[str] | None = None) -> dict:
    """Return a verdict. `ok` False means: do not publish this answer, and record why."""
    dois, recids, by_doi = _registry()
    problems: list[dict] = []

    for m in DOI_RE.finditer(answer):
        d = m.group(0).lower()
        if d not in dois:
            problems.append({
                "kind": "unregistered-doi",
                "value": m.group(0),
                "detail": "this DOI does not appear in registry/publications/records.json",
            })

    for m in ZENODO_URL_RE.finditer(answer):
        if m.group(1) not in recids:
            problems.append({
                "kind": "unregistered-zenodo-record",
                "value": m.group(0),
                "detail": "this Zenodo record id is not in the publication registry",
            })

    # A DOI that exists but is SUPERSEDED, offered without any hedge, is the currency failure in its
    # most checkable form. Flagged rather than fatal: quoting a superseded record is legitimate when
    # the answer says that is what it is doing.
    lowered = answer.lower()
    hedged = any(w in lowered for w in ("supersede", "superseded", "earlier edition", "at the time",
                                        "historical", "preserved", "edition-pinned", "pinned",
                                        "current record", "no longer current", "previous version"))
    for m in DOI_RE.finditer(answer):
        rec = by_doi.get(m.group(0).lower())
        if rec and rec.get("status") == "superseded" and not hedged:
            problems.append({
                "kind": "superseded-doi-unhedged",
                "value": m.group(0),
                "detail": f"{rec.get('title')} v{rec.get('version')} is superseded, and the answer "
                          f"does not say so",
            })

    fatal = [p for p in problems if p["kind"] != "superseded-doi-unhedged"]
    return {
        "ok": not fatal,
        "problems": problems,
        "fatal": len(fatal),
        "warnings": len(problems) - len(fatal),
    }


def registry_doi_count() -> int:
    dois, _, _ = _registry()
    return len(dois)

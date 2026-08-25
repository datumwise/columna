"""Redact publication identifiers from stored eval transcripts, preserving the VERDICT.

WHY, AND WHY NOT A consumers.json ROW.

G7's echo audit scans every tracked file for Zenodo tokens and fails closed on undeclared ones. It
caught the committed eval transcripts, because the model quotes real DOIs in its answers. The
obvious move is a consumers.json row per results file — but that is the wrong shape twice over:

  · it makes every eval re-run a governance edit, which is friction on exactly the artifact we want
    to regenerate freely as the registry moves;
  · and it declares a model transcript to be a datumwise publication surface, which it is not. It is
    evidence about a model, not a claim by us.

What we actually need to inspect is not the digits — it is WHETHER THE IDENTIFIER WAS REAL. So the
transcript stores that instead:

    10.5281/zenodo.22013410  ->  (DOI:registered-current)
    10.5281/zenodo.21774490  ->  (DOI:registered-superseded)
    10.5281/zenodo.99999999  ->  (DOI:UNREGISTERED)

The DOI-trap cases stay fully inspectable — a fabricated identifier is louder in this form than in
its raw one — and the gate's vocabulary stays clean. Same principle as index_build.py: the registry
owns identity; everything else carries a reference to it.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RECORDS = REPO / "registry" / "publications" / "records.json"

_DOI = re.compile(r"\b10\.5281/zenodo\.\d+\b", re.I)
_ZURL = re.compile(r"https?://(?:www\.)?zenodo\.org/records?/(\d+)", re.I)


@lru_cache(maxsize=1)
def _status_by_doi() -> dict[str, str]:
    return {r["doi"].lower(): r.get("status", "unknown")
            for r in json.loads(RECORDS.read_text()) if r.get("doi")}


@lru_cache(maxsize=1)
def _recids() -> set[str]:
    return {str(r["recid"]) for r in json.loads(RECORDS.read_text()) if r.get("recid")}


def redact(text: str) -> str:
    def doi_sub(m: re.Match) -> str:
        st = _status_by_doi().get(m.group(0).lower())
        return f"(DOI:registered-{st})" if st else "(DOI:UNREGISTERED)"

    def url_sub(m: re.Match) -> str:
        return ("(zenodo-record:registered)" if m.group(1) in _recids()
                else "(zenodo-record:UNREGISTERED)")

    return _DOI.sub(doi_sub, _ZURL.sub(url_sub, text))


def redact_tree(obj):
    if isinstance(obj, str):
        return redact(obj)
    if isinstance(obj, list):
        return [redact_tree(x) for x in obj]
    if isinstance(obj, dict):
        return {k: redact_tree(v) for k, v in obj.items()}
    return obj


if __name__ == "__main__":
    import sys
    for p in map(Path, sys.argv[1:]):
        p.write_text(json.dumps(redact_tree(json.loads(p.read_text())), indent=1))
        print(f"redacted {p}")

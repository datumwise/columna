#!/usr/bin/env python3
"""Fail-closed adjudication gate for the current representative corpus.

WHAT THIS DEFENDS. `registry/sources/current-corpus.json` records which catalogued sources currently
represent datumwise. The failure mode it exists to prevent is DRIFT BY ADDITION: someone adds a
source to the catalog, nobody rules on it, and it silently either appears in the representative
corpus or vanishes from consideration. Both are wrong, and both are invisible without a gate.

So membership is EXHAUSTIVE by construction: every catalogued sourceId must appear in exactly one
of `in` / `referenceOnly` / `out`. A new source fails the build until someone rules on it. That is
the same discipline as G7's echo audit — a new fact may not simply appear.

C1  exhaustive     — every catalogued source is ruled exactly once
C2  no ghosts      — no ruling names a source the catalog does not have
C3  ids only       — no publication fact (title, version, date, DOI) is typed into the file
C4  jurisdiction   — every referenceOnly entry names a jurisdiction the file defines
C5  in-set shape   — no IN source carries `preservedState` (a preserved state cannot be current)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "registry" / "sources" / "current-corpus.json"
SOURCES = REPO / "registry" / "sources" / "sources.json"

findings: list[str] = []


def fail(code: str, msg: str) -> None:
    findings.append(f"  [{code}] {msg}")


def main() -> int:
    corpus = json.loads(CORPUS.read_text())
    cat = json.loads(SOURCES.read_text())
    sources = cat["sources"] if isinstance(cat, dict) else cat
    by_id = {s["sourceId"]: s for s in sources}

    def ids(key: str) -> list[str]:
        return [x if isinstance(x, str) else x["sourceId"] for x in corpus.get(key, [])]

    in_, ref, out = ids("in"), ids("referenceOnly"), ids("out")
    ruled = in_ + ref + out

    # ── C1 · exhaustive, exactly once ─────────────────────────────────────────────────────────────
    seen: dict[str, int] = {}
    for s in ruled:
        seen[s] = seen.get(s, 0) + 1
    for s, n in sorted(seen.items()):
        if n > 1:
            fail("C1", f"{s} is ruled {n} times. A source has exactly one standing.")
    for s in sorted(set(by_id) - set(ruled)):
        fail("C1", f"{s} is in the source catalog but is not ruled IN, REFERENCE ONLY or OUT. "
                   f"FAILING CLOSED: a new source may not enter the estate unadjudicated — rule on "
                   f"it in registry/sources/current-corpus.json.")

    # ── C2 · no ghosts ────────────────────────────────────────────────────────────────────────────
    for s in sorted(set(ruled) - set(by_id)):
        fail("C2", f"current-corpus.json rules on {s}, which is not in the source catalog. A ruling "
                   f"that outlives its subject reads as coverage.")

    # ── C3 · ids only, no publication facts ───────────────────────────────────────────────────────
    # Scan only the ruled entries — the $comment blocks legitimately discuss the rule — and within
    # them, only the NON-ID fields. A sourceId is an identifier, not a publication fact, even when it
    # happens to contain a date: `s-research-map-2026-08-03` names a preserved state whose date is
    # part of its name. The first version of this check failed on exactly that, which is the right
    # kind of over-eagerness to catch here rather than in review.
    def non_id_fields(key: str) -> list:
        out_ = []
        for x in corpus.get(key, []):
            if isinstance(x, dict):
                out_.append({k: v for k, v in x.items() if k != "sourceId"})
        return out_

    payload = json.dumps([non_id_fields(k) for k in ("in", "referenceOnly", "out")])
    for pat, what in (
        (r"10\.5281/zenodo\.\d+", "a DOI"),
        (r"\bv\d+\.\d+\b", "a version string"),
        (r"\b20\d\d-\d\d-\d\d\b", "a date"),
    ):
        for m in re.finditer(pat, payload):
            fail("C3", f"the membership lists carry {what} ({m.group(0)!r}). Membership is ids only; "
                       f"publication facts are resolved from the registry.")

    # ── C4 · declared jurisdictions ───────────────────────────────────────────────────────────────
    declared = set(corpus.get("jurisdictions", {})) - {"$comment"}
    for entry in corpus.get("referenceOnly", []):
        if isinstance(entry, str):
            fail("C4", f"{entry} is REFERENCE ONLY but names no jurisdiction. Reference standing is "
                       f"jurisdictional, not a demotion — say what it governs.")
        elif entry.get("jurisdiction") not in declared:
            fail("C4", f"{entry['sourceId']} names jurisdiction {entry.get('jurisdiction')!r}, which "
                       f"the file does not define. Known: {sorted(declared)}")

    # ── C5 · a preserved state cannot be current ──────────────────────────────────────────────────
    for s in in_:
        src = by_id.get(s)
        if src and src.get("preservedState"):
            fail("C5", f"{s} is ruled IN but carries preservedState={src['preservedState']!r}. A "
                       f"preserved historical state cannot be part of the CURRENT representative "
                       f"corpus — that is the distinction Gateway 1 established.")

    if findings:
        print("\nCORPUS MEMBERSHIP GATE FAILED — %d finding(s):\n" % len(findings))
        print("\n".join(findings))
        return 1

    print(f"corpus membership OK — {len(by_id)} catalogued sources: "
          f"{len(in_)} IN, {len(ref)} REFERENCE ONLY, {len(out)} OUT, 0 unadjudicated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

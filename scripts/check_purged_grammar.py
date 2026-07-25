#!/usr/bin/env python3
"""
check_purged_grammar.py — THE CLASS GUARD (Huayin, 2026-07-25, item 7).

Fossils accumulated silently once; this makes accumulation loud.

WHAT HAPPENED. `EDGE <a> -> <b> ALONG <lineage> VIA t(x, y)` was PURGED (case-demo §2a) — a functional
path is declared only inside `HIERARCHY <lineage> { <a> -> <b> VIA t(a, b) }`. A micro-PR was ruled to
migrate the survivors and never landed. It went unnoticed because the only check that would have
caught it (docs.yml's regen-check) fires on a `docs/**` path filter and simply did not run — `main`
sat red from 2026-07-19 to 2026-07-25 with nobody seeing it. By the time it surfaced, the purged form
was still in a doc fixture, the PyPI-facing core README, a shipped benchmark fixture, and a test.

Guarding the INSTANCES would have fixed a day. This guards the CLASS: any reappearance of the purged
surface form anywhere in the repo fails CI.

INTENTIONAL USES WHITELIST THEMSELVES. A line carrying the marker `INTENTIONALLY-PURGED` is skipped.
That is not a loophole — it is the point: `test_init_plumbing.py` feeds deliberately-WRONG proposal
bodies (`wrong->place`) to prove the harness strikes them, and a proposal body there is an opaque
string that is never parsed. Retired syntax is, if anything, more faithful for that job. The marker
makes the intent legible to the next sweep so nobody "fixes" it back into a broken test.

NOT FLAGGED: the word "edge" as internal taxonomy. Edges remain the single internal truth — the parser
desugars HIERARCHY into FunctionalEdges, and `kind="edge"` closures are what the init eval SCORES on.
Only the purged *surface syntax* is a fossil, so the pattern below is deliberately narrow: it requires
the full `EDGE ... -> ... ALONG ... VIA` shape and will not match `kind="edge"` or prose about edges.

Usage:  python scripts/check_purged_grammar.py        # exits 1 on any unmarked occurrence
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# The purged SURFACE form only. `<from>`-style placeholders are matched too, so README syntax summaries
# and templates cannot reintroduce it either.
PURGED = re.compile(r"\bEDGE\s+[<\w.]+>?\s*->\s*[<\w.]+>?\s+ALONG\s+[<\w.]+>?\s+VIA\b")

MARKER = "INTENTIONALLY-PURGED"

# ROWED FOSSILS — known, tracked, NOT silently forgiven.
#
# A fossil too large to fix in the PR that found it does not get a quiet whitelist; it gets a row in
# specs/open_forks.md and an entry here. The guard then does two things a whitelist never would: it
# PRINTS the fossil loudly on every run, and it FAILS if the named fork is missing or already struck
# in the ledger. So the exemption cannot outlive its row — closing the fork without fixing the file
# turns the build red. "Rulings that aren't tracked didn't happen" (Huayin, 2026-07-25), enforced.
ROWED = {
    # The reference manual's §26.6 status annotation has SHIPPED/SCHEDULED exactly inverted (it calls
    # EDGE the shipped form and HIERARCHY merely scheduled), and §26.6's body documents a HIERARCHY
    # signature without braces or per-hop VIA. That is a manual CONTENT pass, not a fixture rewrite.
    "docs/columna_reference_manual_5e.md": "OF-16",
}
LEDGER = ROOT / "specs" / "open_forks.md"

# The ledgers DESCRIBE fossils — an OF/DG row has to quote the retired form to be legible about what it
# is rowing. Quoting is not using, so these files are exempt wholesale. (Same reason this script is
# exempt from itself: its docstring and regex both contain the pattern.)
DESCRIBES_FOSSILS = {"specs/open_forks.md", "specs/doctrine_gaps.md"}

SUFFIXES = {".py", ".md", ".cml", ".txt", ".ts", ".astro", ".yml", ".yaml", ".json", ".toml"}
SKIP_DIRS = {
    ".git", "node_modules", "dist", ".astro", ".vercel", "__pycache__", ".venv", "venv",
    "build", ".pytest_cache", ".mypy_cache", "eval_runs", "reserve",
}
# This file necessarily contains the pattern (in its own docstring and regex).
SELF = pathlib.Path(__file__).resolve()


def iter_files():
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix not in SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.resolve() == SELF:
            continue
        yield p


def ledger_has_open(fork_id: str) -> bool:
    """A rowed exemption is valid only while its fork is present AND still OPEN in the ledger."""
    if not LEDGER.exists():
        return False
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if re.search(rf"\b{re.escape(fork_id)}\b", line) and "**OPEN**" in line:
            return True
    return False


def main() -> int:
    hits, allowed, rowed_hits = [], 0, []
    for p in iter_files():
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "EDGE" not in text:                     # cheap prefilter
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if not PURGED.search(line):
                continue
            if MARKER in line:
                allowed += 1
                continue
            rel = p.relative_to(ROOT).as_posix()
            if rel in DESCRIBES_FOSSILS:
                continue
            if rel in ROWED:
                rowed_hits.append((rel, n, line.strip(), ROWED[rel]))
                continue
            hits.append((p.relative_to(ROOT), n, line.strip()))

    # A rowed exemption whose fork has vanished or been struck is itself a failure.
    stale_rows = sorted({fid for _, _, _, fid in rowed_hits if not ledger_has_open(fid)})
    if stale_rows:
        print("ROWED EXEMPTION WITHOUT AN OPEN FORK — the row cannot outlive its ledger entry.")
        for fid in stale_rows:
            print(f"  {fid}: not found as an OPEN row in specs/open_forks.md")
        print("\nEither the fossil was fixed (drop it from ROWED in this script) or the fork was closed")
        print("prematurely (reopen it). A tracked exemption stops being tracked the moment its row goes.")
        return 1

    if rowed_hits:
        print("ROWED FOSSILS (tracked, not forgiven) — still present, each against an OPEN fork:")
        for rel, n, line, fid in rowed_hits:
            print(f"  [{fid}] {rel}:{n}: {line[:100]}")
        print()

    if hits:
        print("PURGED GRAMMAR FOUND — `EDGE <a> -> <b> ALONG <lineage> VIA t(x, y)` was retired.")
        print("The sole surface for a functional path is:")
        print("    HIERARCHY <lineage> { <a> -> <b> VIA <table>(<col>, <col>) [-> ...] [; <path>] }\n")
        for path, n, line in hits:
            print(f"  {path}:{n}: {line[:118]}")
        print(f"\n{len(hits)} occurrence(s). If a use is deliberate (an opaque, never-parsed string —")
        print(f"e.g. a struck proposal body), mark that line `{MARKER}` and it is whitelisted.")
        return 1

    print(f"purged-grammar guard OK: no unmarked `EDGE ... ALONG ... VIA` "
          f"({allowed} intentional occurrence(s) whitelisted).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

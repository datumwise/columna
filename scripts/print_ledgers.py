#!/usr/bin/env python3
"""
print_ledgers.py — THE LEDGER HEARTBEAT (Huayin, 2026-07-25).

A ledger that must be *consulted* is a ledger that gets forgotten. The fossil ruling evaporated even
though `doctrine_gaps.md` already existed and already said "never a silent drop" — the failure was a
ledger not USED, not a ledger not PRESENT. So the weekly `docs.yml` run prints every open row of both
ledgers into its job summary: the ledger ARRIVES instead of waiting to be looked at.

Emits GitHub-flavoured Markdown on stdout. In CI:

    python scripts/print_ledgers.py >> "$GITHUB_STEP_SUMMARY"

Locally it is just a readable digest of what `main` currently owes.

A row counts as OPEN when its id is not struck (`~~OF-3~~`) and its status cell says `**OPEN**`.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

LEDGERS = [
    ("Doctrine ↔ code gaps", ROOT / "specs" / "doctrine_gaps.md",
     "Ratified doctrine `main` does not yet match, plus authorized work tracked to completion."),
    ("Open forks", ROOT / "specs" / "open_forks.md",
     "Code ahead of doctrine — a provisional choice awaiting a ruling."),
]

ROW = re.compile(r"^\|\s*(~~)?\s*((?:DG|AW|OF)-\d+)\s*(~~)?\s*\|(.*)$")


def open_rows(path: pathlib.Path):
    """Yield (id, cells) for every non-struck row whose status cell is **OPEN**."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        if m.group(1) or m.group(3):          # struck id -> closed
            continue
        if "**OPEN**" not in line:
            continue
        cells = [c.strip() for c in m.group(4).split("|")]
        yield m.group(2), cells


def summarize(cells: list[str], limit: int = 180) -> str:
    """The row's DESCRIPTION cell, flattened and clipped.

    All three tables put the description second after the id — DG: `opened | doctrine | …`,
    AW: `ruled | authorized work | …`, OF: `opened | fork | …` — so index 1 is the description in
    every case. (Taking the longest cell instead surfaces the evidence column, which reads as a
    footnote rather than as what the row owes.) Falls back to the longest cell if the shape changes.
    """
    text = cells[1] if len(cells) > 1 and cells[1] else max((c for c in cells if c), key=len, default="")
    text = re.sub(r"\s+", " ", text).strip()
    return (text[: limit - 1] + "…") if len(text) > limit else text


def main() -> int:
    out: list[str] = ["## 📒 Open ledger rows", ""]
    total = 0

    for title, path, blurb in LEDGERS:
        rows = list(open_rows(path))
        total += len(rows)
        rel = path.relative_to(ROOT).as_posix()
        out.append(f"### {title} — {len(rows)} open")
        out.append(f"_{blurb}_  \n`{rel}`")
        out.append("")
        if rows:
            out.append("| # | what it owes |")
            out.append("|---|---|")
            for rid, cells in rows:
                out.append(f"| **{rid}** | {summarize(cells)} |")
        else:
            out.append("_Nothing open._")
        out.append("")

    out.insert(2, f"**{total} open row(s) across both ledgers.**  ")
    out.insert(3, "")
    out.append("---")
    out.append("_This heartbeat exists because a ruling once evaporated while a ledger that would have "
               "caught it sat unread. A row you have to go looking for is a row that gets forgotten._")

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

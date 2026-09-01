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

**Extended 2026-09-01 (consolidated P0/P1 coverage).** The heartbeat read only the two table-shaped
`specs/` ledgers, so every P0/P1 row in `docs/architecture/consolidated_ledger_v0_1.md` — including
the bounded blocker P1-12 and the open capability gaps P1-14/P1-15/P1-17 — was structurally
invisible to the one mechanism built to keep open rows visible. That is the bug this file's own
docstring exists to prevent, reproduced one ledger over.

The consolidated ledger is heading-shaped, not table-shaped, so it gets its own parser. Its
disposition lives in the `### ` heading's **bold** segments, and it has three states, not two:
a row is CLOSED only when it positively says so. **A row carrying no disposition at all is reported
as UNMARKED, never silently dropped** — reading silence as closure is the same failure in miniature,
and this ledger has twelve such rows, two of them CRITICAL.
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

CONSOLIDATED = (
    "Consolidated architecture ledger — P0/P1",
    ROOT / "docs" / "architecture" / "consolidated_ledger_v0_1.md",
    "The governing inventory. Heading-shaped; a row is closed only when it positively says so.",
)

#   ### P1-14 · <title> · **HIGH** · **CAPABILITY GATE SHIPPED; the gap remains OPEN** · VX
HEADING = re.compile(r"^###\s+((?:P0|P1)-\d+)\s+·\s+(.*)$")
BOLD = re.compile(r"\*\*(.+?)\*\*")
SEVERITY = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "MEDIUM/LOW"}


def disposition(bold_segments: list[str]) -> str:
    """OPEN | CLOSED | UNMARKED, from the heading's non-severity bold segments.

    Order is load-bearing. P1-14 reads `**CAPABILITY GATE SHIPPED; the underlying gap remains
    OPEN**` — shipped *and* open — so OPEN is tested first and wins. `PARTLY FIXED` (P0-11, P0-13:
    "the packaged half is RELEASE-GATED") is still owed, so it is open too, and is tested before the
    bare FIXED match that would otherwise swallow it.

    Only the BOLD segments are inspected, never the title: P1-02 is `data_identity() -> None` is
    **fail-OPEN** on the witness store` — a title that contains the word OPEN while carrying no
    disposition whatsoever.
    """
    status = " ".join(b for b in bold_segments if b.strip() not in SEVERITY).upper()
    if "OPEN" in status or "BLOCKER" in status:
        return "OPEN"
    if "PARTLY" in status:
        return "OPEN"
    if "FIXED" in status or "CLOSED" in status:
        return "CLOSED"
    return "UNMARKED"


def consolidated_rows(path: pathlib.Path):
    """Yield (id, disposition, title) for every P0/P1 heading, in file order."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEADING.match(line)
        if not m:
            continue
        rid, rest = m.group(1), m.group(2)
        title = re.sub(r"\s+", " ", rest.split(" · ")[0]).strip()
        yield rid, disposition(BOLD.findall(rest)), title


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


def clip(text: str, limit: int = 180) -> str:
    """The same clip `summarize` applies to table cells, for heading titles."""
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

    # ---- the consolidated P0/P1 ledger (heading-shaped) --------------------
    title, path, blurb = CONSOLIDATED
    rows = list(consolidated_rows(path))
    opened = [r for r in rows if r[1] == "OPEN"]
    unmarked = [r for r in rows if r[1] == "UNMARKED"]
    total += len(opened)
    rel = path.relative_to(ROOT).as_posix()

    out.append(f"### {title} — {len(opened)} open")
    out.append(f"_{blurb}_  \n`{rel}`")
    out.append("")
    if opened:
        out.append("| # | what it owes |")
        out.append("|---|---|")
        for rid, _, name in opened:
            out.append(f"| **{rid}** | {clip(name)} |")
    else:
        out.append("_Nothing open._")
    out.append("")

    if unmarked:
        out.append(f"### ⚠ Carrying no disposition — {len(unmarked)}")
        out.append("_Neither closed nor marked open. Silence is not closure: each needs a status, "
                   "or a strike._  \n`" + rel + "`")
        out.append("")
        out.append("| # | what it says |")
        out.append("|---|---|")
        for rid, _, name in unmarked:
            out.append(f"| **{rid}** | {clip(name)} |")
        out.append("")

    out.insert(2, f"**{total} open row(s) across {len(LEDGERS) + 1} ledgers"
                  + (f", and {len(unmarked)} carrying no disposition" if unmarked else "")
                  + ".**  ")
    out.insert(3, "")
    out.append("---")
    out.append("_This heartbeat exists because a ruling once evaporated while a ledger that would have "
               "caught it sat unread. A row you have to go looking for is a row that gets forgotten._")

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

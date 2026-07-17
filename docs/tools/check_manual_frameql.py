#!/usr/bin/env python3
"""
check_manual_frameql.py — the manual verifies itself against the shipped parser (standing test).

The prose-coherence tripwire's principle applied to the manual, PRE-MERGE: every FrameQL example in
`docs/frame_ql_manual_v1.md` either parses clean against `columna_core.envelope.parse_statement` OR is
deliberately marked ill-formed-for-teaching. The manual can never again document syntax its own parser
rejects; Huayin's sitting is spent on prose and doctrine, never on a syntax typo the parser catches free.

MARKING CONVENTION (stated once, here and in the manual's harness note):
  • A FrameQL query block — a ```frameql fence, OR a bare ``` fence whose first statement begins with
    SELECT/EXPLAIN/FROM/WITH — MUST parse clean (it may still refuse/clarify at PLAN time; that is
    semantics, not grammar — this check is grammar only).
  • A ```frameql-illformed fence is a DELIBERATELY ill-formed example (a syntax the manual shows in order
    to name what the parser rejects). This check asserts it does NOT parse — a marked example that starts
    parsing is itself a failure (the teaching went stale). This is the ONLY way to exempt a query block.
  • Any other fence (```text, ```frameql-output, ```cml, …) is prose/output and is not checked.

Run: `python docs/tools/check_manual_frameql.py`  → exit 0 iff every example is clean-or-marked.
"""
import re
import sys
import pathlib

try:
    from columna_core.envelope import parse_statement, EnvelopeSyntaxError
except ModuleNotFoundError:                                    # pragma: no cover
    sys.stderr.write("columna_core.envelope not importable — install columna-core (0.9.0+) first.\n")
    sys.exit(2)

MANUAL = pathlib.Path(__file__).resolve().parents[1] / "frame_ql_manual_v1.md"
_FENCE = re.compile(r"^(\s*)```([A-Za-z0-9_-]*)\s*$")
_STMT_START = re.compile(r"^\s*(EXPLAIN|FROM|WITH|SELECT)\b", re.IGNORECASE)


def _fenced_blocks(text: str):
    """Yield (lineno, info_string, body) for every fenced block."""
    out, i, lines = [], 0, text.splitlines()
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if m:
            info, start, body = m.group(2), i + 1, []
            i += 1
            while i < len(lines) and not _FENCE.match(lines[i]):
                body.append(lines[i]); i += 1
            out.append((start, info.lower(), "\n".join(body)))
        i += 1
    return out


_SELECT = re.compile(r"^\s*SELECT\b", re.IGNORECASE)


def _statements(body: str):
    """Split a frameql block into individual statements WITHOUT a crude blank-line heuristic. A statement
    is `[EXPLAIN] [FROM] [WITH…] SELECT … AT …` — the preamble keywords belong to the SAME statement as
    their SELECT. So a NEW statement boundary is a top-level EXPLAIN/FROM/WITH/SELECT line reached only
    AFTER the current statement already has its SELECT (i.e. the prior one is complete)."""
    stmts, cur, has_select, depth = [], [], False, 0
    for ln in body.splitlines():
        at_start = depth == 0 and bool(_STMT_START.match(ln))
        if at_start and has_select and cur:                    # the prior statement ended; start a new one
            stmts.append("\n".join(cur).strip()); cur, has_select = [], False
        cur.append(ln)
        if depth == 0 and _SELECT.match(ln):
            has_select = True
        depth += ln.count("(") + ln.count("{") + ln.count("[")
        depth -= ln.count(")") + ln.count("}") + ln.count("]")
    if "\n".join(cur).strip():
        stmts.append("\n".join(cur).strip())
    return [s for s in stmts if s]


def main() -> int:
    text = MANUAL.read_text()
    clean, marked, failures = 0, 0, []
    for lineno, info, body in _fenced_blocks(text):
        stmts = _statements(body)
        is_frameql = info == "frameql" or (info == "" and stmts and _STMT_START.match(stmts[0]))
        if is_frameql:
            for stmt in stmts:
                try:
                    parse_statement(stmt); clean += 1
                except EnvelopeSyntaxError as e:
                    failures.append((lineno, "should-parse", stmt.splitlines()[0][:64], str(e)[:80]))
        elif info == "frameql-illformed":
            for stmt in _statements(body):
                try:
                    parse_statement(stmt)
                    failures.append((lineno, "marked-but-parses", stmt.splitlines()[0][:64], "no longer ill-formed"))
                except EnvelopeSyntaxError:
                    marked += 1
    total = clean + marked + len(failures)
    for lineno, kind, head, err in failures:
        print(f"FAIL @L{lineno} [{kind}]: {head!r} -> {err}", file=sys.stderr)
    print(f"manual FrameQL examples: {total} total — {clean} parse-clean, {marked} marked ill-formed, "
          f"{len(failures)} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

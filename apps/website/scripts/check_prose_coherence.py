#!/usr/bin/env python3
"""
check_prose_coherence.py — the PROSE-COHERENCE TRIPWIRE (from the #45 incident, 2026-07-17).

The integrity gate guards seeded WIRE behaviour; it does not read the WORDS. So the CP-3b corpus
(envelope-syntax prose) once merged and deployed against a shipped package whose parser could not run
it — prose incoherence nothing caught. This tripwire closes that structurally: it extracts every
FrameQL code block from the corpus pieces + the llms files and PARSE-CHECKS each against the INSTALLED
SHIPPED package. Documented syntax the shipped parser rejects FAILS the deploy. Runs in the
shipped-coherent CI job (which installs columna from PyPI), so it speaks for the exact wheel that ships.
"""
import re
import sys
import pathlib

from columna_core.envelope import parse_statement, EnvelopeSyntaxError

ROOT = pathlib.Path(__file__).resolve().parents[1]                      # apps/website
# The llms index moved out of public/ and became a composed route (Phase 1A, 2026-08-21): its
# publication block is derived from the publication registry, so the prose now lives in
# src/content/llms_index.txt. The FrameQL blocks this gate parses are all in the ratified prose,
# which is byte-unchanged — only the path moved. Fails closed below if the file is not there.
LLMS_INDEX = ROOT / "src" / "content" / "llms_index.txt"
if not LLMS_INDEX.exists():
    raise SystemExit(
        f"prose coherence: {LLMS_INDEX} is missing. The machine-facing index is the one document\n"
        "strangers' agents read first; this gate refuses to pass by silently checking one fewer file."
    )
SOURCES = sorted((ROOT / "src" / "content" / "corpus").glob("*.md")) + [LLMS_INDEX]
_FQL_START = re.compile(r"^\s*(SELECT|EXPLAIN|FROM|WITH)\b", re.IGNORECASE)


def _code_blocks(text: str):
    out, cur, in_fence = [], [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            if in_fence:
                out.append("\n".join(cur)); cur = []
            in_fence = not in_fence
            continue
        if in_fence:
            cur.append(line)
    return out


def _frameql_statements(text: str):
    return [b.strip() for b in _code_blocks(text) if _FQL_START.match(b.strip())]


def main() -> int:
    checked, failed = 0, 0
    for src in SOURCES:
        if not src.exists():
            continue
        for stmt in _frameql_statements(src.read_text()):
            checked += 1
            try:
                parse_statement(stmt)
            except EnvelopeSyntaxError as e:
                failed += 1
                print(f"PROSE-COHERENCE FAIL — {src.name}: the shipped parser rejects a documented query:\n"
                      f"    {stmt!r}\n    -> {e}", file=sys.stderr)
    if failed:
        print(f"\n{failed}/{checked} documented FrameQL block(s) do not parse against the shipped "
              f"package — the site would deploy prose it cannot run. Deploy blocked.", file=sys.stderr)
        return 1
    print(f"prose-coherence OK: {checked} documented FrameQL block(s) parse against the shipped package.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

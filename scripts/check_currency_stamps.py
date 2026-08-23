#!/usr/bin/env python3
"""Fail closed when a documented CURRENT-STATE version or contract stamp stops matching what ships.

THE FAILURE THIS EXISTS FOR. The Frame-QL Manual's body was reconciled through 2026-08-20 while its
header still said it documented columna-core 0.14.0 at wire contract "2" — four releases behind — and
`contract_version "1"` was live on /llms.txt through TWO contract bumps. Nothing caught either,
because no gate in this repository compared a documented version string against the shipped package.
The parse gates check grammar; `check_prose_coherence.py` checks grammar; `/docs/grammar` cannot go
stale only because it is generated rather than asserted. A claim about what ships had no guard at all.

THE DESIGN, IN ONE LINE: history is the default, currency is declared.

A guard that scanned prose for version tokens would eventually flag — and invite someone to "fix" —
a sentence like `wire contract "1" -> "2"` (0.14.0), which is a true historical record. Rewriting the
record is a worse outcome than the drift. So this guard reads NO prose. It renders only the templates
a human enrolled in `scripts/currency_stamps.toml` and asserts each rendered literal is present. Every
unenrolled version mention in every covered file is structurally out of reach: the guard never looks
at it, so it cannot rewrite it, flag it, or have an opinion about it.

AUTHORITATIVE VALUES, NEITHER OF THEM TYPED HERE:
  · the package triad  — `scripts/release_pins.py`, already the one policy source that reads all
    three pyprojects (`read_release_set`). This guard does not become a fourth reader of them.
  · the wire contract  — `columna_core.disclosure_wire.CONTRACT_VERSION`, IMPORTED from the package.
    The contract is the package's to declare; a literal here would be the very defect being guarded.

Because both come from the working tree / the installed package, this checks the stamps against what
THIS COMMIT would ship — before it ships, which is the only useful moment.

Usage:  python scripts/check_currency_stamps.py [--manifest PATH]
Exit:   0 all enrolled claims present · 1 a claim failed · 2 the guard could not run
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "scripts" / "currency_stamps.toml"


def authoritative_values() -> dict:
    """The shipped state, from the two sources that own it. Never typed into this file."""
    try:
        from release_pins import read_release_set          # the one pyproject policy source
    except Exception as exc:                                # pragma: no cover - guard-cannot-run path
        print(f"currency guard CANNOT RUN: scripts/release_pins.py is not importable ({exc}).",
              file=sys.stderr)
        raise SystemExit(2)
    versions, _floors = read_release_set()

    try:
        from columna_core.disclosure_wire import CONTRACT_VERSION
    except Exception as exc:                                # pragma: no cover - guard-cannot-run path
        print("currency guard CANNOT RUN: columna_core is not importable, so the wire contract "
              f"cannot be read from the package ({exc}). Install columna-core first — this guard "
              "reads the contract from the shipped module and never from a literal.", file=sys.stderr)
        raise SystemExit(2)

    missing = [k for k in ("columna", "columna-core", "columna-server") if k not in versions]
    if missing:
        print(f"currency guard CANNOT RUN: release_pins did not report {missing}.", file=sys.stderr)
        raise SystemExit(2)

    return {
        "umbrella": versions["columna"],
        "core": versions["columna-core"],
        "server": versions["columna-server"],
        "contract": CONTRACT_VERSION,
    }


def load_manifest(path: Path) -> list:
    if not path.is_file():
        print(f"currency guard CANNOT RUN: no manifest at {path.relative_to(ROOT)}.", file=sys.stderr)
        raise SystemExit(2)
    stamps = tomllib.loads(path.read_text(encoding="utf-8")).get("stamp", [])
    if not stamps:
        print(f"currency guard CANNOT RUN: {path.relative_to(ROOT)} enrols no claims. An empty "
              "manifest would pass silently, which is the one thing a fail-closed guard may not do.",
              file=sys.stderr)
        raise SystemExit(2)
    for i, st in enumerate(stamps, 1):
        for key in ("file", "claim", "template"):
            if not st.get(key):
                print(f"currency guard CANNOT RUN: stamp #{i} is missing `{key}`.", file=sys.stderr)
                raise SystemExit(2)
    return stamps


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", default=str(MANIFEST))
    args = ap.parse_args(argv)

    values = authoritative_values()
    stamps = load_manifest(Path(args.manifest))

    print("currency guard — the shipped state this commit would ship:")
    print(f"  columna {values['umbrella']} · columna-core {values['core']} · "
          f"columna-server {values['server']} · wire contract_version \"{values['contract']}\"")

    failures, checked, cache = [], 0, {}
    for st in stamps:
        rel = st["file"]
        if rel not in cache:
            path = ROOT / rel
            cache[rel] = path.read_text(encoding="utf-8") if path.is_file() else None
        text = cache[rel]

        # FAILURE 1 — the enrolled FILE is gone.
        if text is None:
            failures.append(
                f"ENROLLED FILE MISSING: {rel}\n"
                f"    claim: {st['claim']}\n"
                f"    The manifest enrols a current-state claim in a file that does not exist. Either "
                f"the file moved — in which case update its rows in scripts/currency_stamps.toml — or "
                f"it was deleted, in which case retire its rows deliberately rather than by absence.")
            continue

        try:
            expected = st["template"].format(**values)
        except KeyError as exc:                             # pragma: no cover - manifest typo path
            failures.append(
                f"UNKNOWN PLACEHOLDER {exc} in the template for {rel}\n"
                f"    claim: {st['claim']}\n"
                f"    Known placeholders: {{umbrella}} {{core}} {{server}} {{contract}}.")
            continue

        checked += 1
        # FAILURE 2 — the enrolled CLAIM is absent: either the version moved and the stamp did not,
        # or the sentence was reworded out from under its enrolment. Both must fail, and neither is
        # a false positive: a currency claim that stops existing is as broken as one gone stale.
        if expected not in text:
            failures.append(
                f"CURRENT-STATE CLAIM NOT PRESENT: {rel}\n"
                f"    claim:    {st['claim']}\n"
                f"    expected: {expected!r}\n"
                f"    {_diagnose(text, st['template'], values)}\n"
                f"    Fix the stamp in the file if the version moved; re-enrol the template in "
                f"scripts/currency_stamps.toml if the sentence was legitimately reworded. Do not "
                f"edit any dated historical statement to make this pass — the guard does not read "
                f"them and they are not what failed.")

    if failures:
        print(f"\ncurrency guard FAILED — {len(failures)} of {len(stamps)} enrolled claim(s):\n",
              file=sys.stderr)
        for f in failures:
            print(f"  · {f}\n", file=sys.stderr)
        return 1

    print(f"currency guard OK — {checked} enrolled current-state claim(s) across "
          f"{len(cache)} file(s) match the shipped state. Unenrolled version mentions are "
          f"history and were not read.")
    return 0


def _diagnose(text: str, template: str, values: dict) -> str:
    """Say WHICH of the two failures it is, when the file makes that decidable.

    A template whose non-version skeleton still appears in the file is a STALE STAMP; one whose
    skeleton is gone was REWORDED. Guessing is not required — the skeleton is derivable by rendering
    the template with each placeholder blanked and keeping the longest literal run.
    """
    blanked = template
    for key in values:
        blanked = blanked.replace("{" + key + "}", "\x00")
    runs = [r for r in blanked.split("\x00") if len(r.strip()) >= 12]
    for run in sorted(runs, key=len, reverse=True):
        if run in text:
            return ("the surrounding wording IS present, so the stamp itself is stale — the version "
                    "moved and this sentence did not move with it.")
    return ("the surrounding wording is NOT present either, so the sentence was reworded or removed; "
            "its enrolment no longer describes the file.")


if __name__ == "__main__":
    sys.exit(main())

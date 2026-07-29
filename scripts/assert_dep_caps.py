#!/usr/bin/env python3
"""THE CAP GUARD — every declared dependency, in every package, must carry an UPPER BOUND.

Runs in CI on every push and PR. Exits non-zero, naming the offender, if any dependency is declared
with a floor and no ceiling.

WHY THIS EXISTS — twice is a class, not a coincidence:

  2026-07-27 (0.13.2)  `datasketches>=5.0` had a cap already, but `requires-python` did not. A
                       Windows fresh-venv pass found `pip install columna` on 3.14 falling through
                       to a C++ source build instead of refusing. Fixed by declaring the ceiling.

  2026-07-28 (0.8.1)   `mcp>=1.0` — unbounded. `mcp 2.0.0` was published 13:45 UTC, four minutes
                       after the last 1.x, and hours after our public launch. It moved
                       `mcp.server.fastmcp`. Every fresh `pip install columna` from that minute on
                       resolved to 2.0.0 and died at import with ModuleNotFoundError, before a
                       single mood printed. Nothing in our repo changed; the break arrived by
                       resolver.

An uncapped dependency is not permissiveness. It is an UNTESTED CLAIM — an assertion that every
future major version of somebody else's package will keep our contract, made before those versions
exist. The house rule (0.13.2's doctrine, restated in dependency metadata): *fail closed with a
named reason beats rare success.* A cap turns "mysterious ImportError on a stranger's machine after
a clean install" into pip's one-line "no matching distribution found" — a sentence a person can act
on, produced at install time, on our terms.

WHAT COUNTS AS A CAP: `<`, `<=`, `==`, or `~=`. A `!=` exclusion does NOT — it names one bad version,
not a boundary, and the next major is still admitted.

MARKERS ARE NOT SPECIFIERS: `tomli>=2.0,<3.0; python_version < '3.11'` carries a `<` inside its
environment marker. Everything after the first `;` is stripped before the check, so a marker can
never be mistaken for a ceiling.

SCOPE: `[project].dependencies`, every list in `[project.optional-dependencies]`, and
`[build-system].requires` for every pyproject.toml under packages/ — plus the website's
package.json, whose npm ranges must be bounded too (`^`/`~`/pins are; a bare `>=` is not). A build
dependency that breaks is as user-visible as a runtime one: it stops the release that carries the fix.

TO LIFT A CAP: raise it to the next known-good major and say why in the CHANGELOG. Do not delete it.
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAP_OPS = ("<", "<=", "==", "~=")


def has_cap(requirement: str) -> bool:
    """True if `requirement` declares an upper bound.

    The environment marker (everything after the first ';') is removed FIRST — a marker's own
    comparison operators say nothing about which versions of the package are admitted.
    """
    spec = requirement.split(";", 1)[0]
    # Drop extras — `uvicorn[standard]>=0.23` — so a bracket can never be read as a specifier.
    spec = re.sub(r"\[[^\]]*\]", "", spec)
    # A URL/direct reference (`pkg @ https://...`) is pinned by construction.
    if "@" in spec:
        return True
    for clause in spec.split(","):
        clause = clause.strip()
        if clause.startswith("<") or clause.startswith("==") or clause.startswith("~="):
            return True
    return False


def python_offenders() -> list[str]:
    out: list[str] = []
    for path in sorted(ROOT.glob("packages/*/pyproject.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)
        project = data.get("project", {})
        groups: list[tuple[str, list]] = [("dependencies", project.get("dependencies", []) or [])]
        for extra, reqs in (project.get("optional-dependencies", {}) or {}).items():
            groups.append((f"optional-dependencies.{extra}", reqs or []))
        groups.append(("build-system.requires", data.get("build-system", {}).get("requires", []) or []))
        for group, reqs in groups:
            for req in reqs:
                if not has_cap(req):
                    out.append(f"{rel} [{group}] {req!r} — no upper bound")
    return out


def npm_offenders() -> list[str]:
    out: list[str] = []
    for path in sorted(ROOT.glob("apps/*/package.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)
        for group in ("dependencies", "devDependencies"):
            for name, rng in (data.get(group) or {}).items():
                r = str(rng).strip()
                bounded = (
                    r.startswith("^")
                    or r.startswith("~")
                    or r.startswith("<")
                    or "<" in r
                    or re.match(r"^\d", r) is not None      # an exact pin
                )
                if not bounded:
                    out.append(f"{rel} [{group}] {name}@{r} — no upper bound")
    return out


def main() -> int:
    offenders = python_offenders() + npm_offenders()
    if offenders:
        print("FAIL — dependency without an upper bound:\n", file=sys.stderr)
        for o in offenders:
            print(f"  {o}", file=sys.stderr)
        print(
            "\nEvery dependency must declare a ceiling. An uncapped dependency is an untested claim "
            "about versions that do not exist yet, and it breaks strangers' fresh installs by "
            "resolver, with nothing in this repo changing (mcp 2.0.0, 2026-07-28; see this file's "
            "docstring). Add the next-major cap and record it in the CHANGELOG.",
            file=sys.stderr,
        )
        return 1
    print("OK — every declared dependency carries an upper bound.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

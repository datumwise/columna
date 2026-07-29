#!/usr/bin/env python3
"""Print the exact PyPI pins for THIS commit's release triad, read from the pyprojects.

    $ python scripts/release_pins.py
    columna==0.13.3 columna-core==0.13.3 columna-server==0.8.2

WHY THIS EXISTS — the third instance of one class, all found on 2026-07-29:

  1. `ci.yml` installed the server's deps from a hand-copied `pip install "mcp>=1.0"` instead of from
     the package metadata, so the SHIPPED constraint was never the thing under test.
  2. `website.yml` hand-typed the deploy wedge's pins — `columna==0.13.2 ...` — a second copy of the
     release version, kept in sync by memory.
  3. (the one that bit) v0.13.3 published, `main` merged, the deploy ran, and the wedge installed
     **0.13.2 / 0.8.1** — the previous, broken triple — and reported "resolved on attempt 1". Green.
     The site then published "0.13.2 · the declared Python floor and ceiling" as the current release
     while PyPI served 0.13.3. The fail-closed release rail could not catch it either: the version it
     saw WAS 0.13.2, which has a curated entry. Every guard behaved correctly, and the site still
     shipped a false claim, because the input was quietly the wrong release.

The class: **the same fact, written down twice.** Not a typo problem — a topology problem. The second
copy is always green until the moment it is silently wrong, and it drifts in the direction nobody
checks, because a stale pin RESOLVES. An absent package fails loudly; a superseded one does not.

So the pin is now DERIVED. The wedge pins the exact versions this commit claims to have shipped, and
its retry budget goes back to meaning what its name says: waiting out index propagation for a release
that exists. If those versions are not on PyPI, the deploy fails closed — which is the correct
outcome and the standing release order (docs/RELEASE_ORDER.md: publish before deploy, every time).
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ["packages/columna", "packages/columna-core", "packages/columna-server"]


def pin(pkg_dir: str) -> str:
    data = tomllib.loads((ROOT / pkg_dir / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]
    return f"{project['name']}=={project['version']}"


def main() -> int:
    pins = [pin(p) for p in PACKAGES]
    if len({p for p in pins if p.startswith(("columna==", "columna-core=="))}) != 2:
        print("unexpected package set", file=sys.stderr)
        return 1
    print(" ".join(pins))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

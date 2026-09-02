#!/usr/bin/env python3
"""Fail closed when a package's `__version__` disagrees with the distribution actually installed.

THE FAILURE THIS EXISTS FOR (P0-19, ruled Huayin 2026-08-31). All three packages carried a
hand-maintained `__version__` literal, and all three had stopped moving:

    columna         "0.14.0"        distribution 0.18.1   — four releases, under a docstring
                                                            promising lockstep with columna-core
    columna-core    "0.16.0-core"   distribution 0.18.1   — three code-changing releases
    columna-server  "0.11.0"        distribution 0.11.1   — one release, no declared semantics

Nothing caught it. The one test that mentioned the core value ASSERTED it — so it could catch an
UNINTENDED bump and was structurally incapable of catching an OMITTED one, the same asymmetry as
`assert_pypi_versions.py` (which catches a forgotten bump only when the forgotten version is
ABSENT). The test did not merely miss the drift; it pinned it in place.

WHY A GUARD AT ALL, WHEN THE ATTRIBUTE IS NOW DERIVED. Deriving it removes today's drift — but it
does not stop someone reintroducing a literal, and a literal is right on the day it is typed. This
guard makes that regression fail on the first release that moves, which is the direction a version
guard has to fail in. It reads the installed distribution rather than the pyprojects on purpose:
`release_pins.py` already owns "what this commit intends to ship", and a second reader of the
pyprojects would be the very duplication this whole class is about.

THE UMBRELLA IS WHY THIS IS A SCRIPT AND NOT THREE UNIT TESTS. `columna` ships a package directory
and has no test suite of its own, so its attribute had no coverage anywhere — which is exactly how
it drifted furthest.

Usage:  python scripts/check_version_attributes.py
Exit:   0 all three agree · 1 a package disagrees · 2 the guard could not run
"""
from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError, version

#: module name -> distribution name. Both halves are named explicitly: the mapping is not derivable
#: (``columna_core`` vs ``columna-core``) and guessing it is how a guard silently checks nothing.
PACKAGES = [
    ("columna", "columna"),
    ("columna_core", "columna-core"),
    ("columna_server", "columna-server"),
]


def main() -> int:
    bad, checked = [], []
    for module_name, dist_name in PACKAGES:
        try:
            module = __import__(module_name)
        except Exception as exc:
            print(f"version-attribute guard CANNOT RUN: `{module_name}` is not importable ({exc}). "
                  f"Install all three distributions first — this guard compares the attribute a "
                  f"consumer reads against the distribution pip actually resolved.", file=sys.stderr)
            return 2
        try:
            installed = version(dist_name)
        except PackageNotFoundError:
            print(f"version-attribute guard CANNOT RUN: `{dist_name}` has no distribution metadata, "
                  f"so there is nothing to compare against. Install it rather than skipping it — a "
                  f"guard that quietly checks two of three packages is worse than none.",
                  file=sys.stderr)
            return 2

        attr = getattr(module, "__version__", None)
        checked.append((dist_name, attr, installed))
        if attr != installed:
            bad.append((module_name, dist_name, attr, installed))

    if bad:
        print("version-attribute guard FAILED — an attribute disagrees with what is installed:\n")
        for module_name, dist_name, attr, installed in bad:
            print(f"  · {module_name}.__version__ is {attr!r}, but the installed {dist_name} "
                  f"distribution is {installed!r}.")
        print("\nThis attribute must be DERIVED from `importlib.metadata`, never typed. A literal is "
              "correct on the day it is written and silently wrong at the next release — that is "
              "P0-19, and it went four releases undetected. See the consolidated ledger.")
        return 1

    print("version-attribute guard OK — " + " · ".join(
        f"{d} {a}" for d, a, _ in checked) + "; every attribute is the installed distribution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

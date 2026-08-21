#!/usr/bin/env python3
"""The release set for THIS commit — derived from the pyprojects, and checked before it is trusted.

    $ python scripts/release_pins.py
    columna==0.15.0 columna-core==0.15.0 columna-server==0.8.2

    $ python scripts/release_pins.py --check                    # the guard alone, prints nothing
    $ python scripts/release_pins.py --check --release v0.15.0  # ...and bind it to a release tag
    $ python scripts/release_pins.py --selftest                 # the guard's own regression fixtures

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

So the pin is DERIVED. The wedge pins the exact versions this commit claims to have shipped, and its
retry budget goes back to meaning what its name says: waiting out index propagation for a release
that exists. If those versions are not on PyPI, the deploy fails closed — which is the correct
outcome and the standing release order (docs/RELEASE_ORDER.md: publish before deploy, every time).

═══ THE FOURTH INSTANCE, AND THE INVARIANT THIS FILE NOW ENFORCES ═══════════════════════════════════

2026-08-20, found in the v0.15.0 preflight, BEFORE the tag: `columna-core` was bumped to 0.15.0 for
the generated-family law and the umbrella `columna` was left at 0.14.0. Every prior release had moved
them together (0.13.0/0.13.0, 0.13.4/0.13.4, 0.14.0/0.14.0). Nothing would have caught it:

  · `assert_pypi_versions.py` asserts every INTENDED version is live. `columna 0.14.0` was already
    live, so it passes. It catches a forgotten bump only when the forgotten version is ABSENT.
  · The homepage's fail-closed Latest rail throws when `RELEASE_NOTES` has no entry for the shipped
    version. It reads the UMBRELLA version, which was 0.14.0 — and 0.14.0 has a curated entry, so it
    does not throw. Production would have announced "currently at 0.14.0 · column identity is the
    canonical expression (Jul 30)" while PyPI served the generated-family law in core 0.15.0.
  · The dependency graph stays satisfiable throughout — `columna 0.14.0` requires
    `columna-core>=0.14.0,<1.0`, which 0.15.0 satisfies. The wedge resolves and goes green.

Same class again, one layer up: the stale fact was not the pin but the UMBRELLA VERSION, and a stale
version that still exists on PyPI resolves. So the guard belongs where the release set is derived —
here, in the one place that already reads all three pyprojects — rather than in a fourth checker with
its own copy of the truth.

THE INVARIANT (ratified Huayin, 2026-08-20):

    umbrella version == core version == release version
    umbrella's minimum core version >= that release version

`columna-server` is INDEPENDENTLY VERSIONED and excluded from lockstep — it may sit unchanged across
several core releases (0.8.2 spanned 0.13.4, 0.14.0 and 0.15.0), and requiring it to move would mint
empty releases whose only content is a version number.

The release-version half is checkable only where a release version exists — `publish.yml` passes the
tag with `--release`. The lockstep and floor halves need no tag and run on every push and PR.
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

UMBRELLA = "packages/columna"
CORE = "packages/columna-core"
SERVER = "packages/columna-server"
PACKAGES = [UMBRELLA, CORE, SERVER]

# The two packages that share a release version. `columna-server` is deliberately absent.
LOCKSTEP = (UMBRELLA, CORE)


def _project(pkg_dir: str) -> dict:
    return tomllib.loads((ROOT / pkg_dir / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def pin(pkg_dir: str) -> str:
    p = _project(pkg_dir)
    return f"{p['name']}=={p['version']}"


# ── version arithmetic, dependency-free ──────────────────────────────────────────────────────────
# These are our own version strings (simple `X.Y.Z` releases), and this guard has to run in the
# publish job and the deploy wedge alike. Importing `packaging` would make a release gate depend on
# whatever a runner happens to have installed; a release gate should not have that failure mode.
def release_tuple(v: str) -> tuple:
    """`'0.15.0'` -> `(0, 15, 0)`. Non-numeric suffixes are dropped, so `0.15.0rc1` sorts as 0.15.0."""
    parts = []
    for seg in str(v).strip().split("."):
        m = re.match(r"\d+", seg)
        parts.append(int(m.group()) if m else 0)
    return tuple(parts)


def core_floor(umbrella: dict) -> str | None:
    """The minimum `columna-core` the umbrella permits — the `>=` bound in its own dependencies."""
    for dep in umbrella.get("dependencies", []):
        name = re.split(r"[<>=!~;\[]", dep, maxsplit=1)[0].strip()
        if name == "columna-core":
            m = re.search(r">=\s*([0-9][^,;\s]*)", dep)
            return m.group(1) if m else None
    return None


def normalize_release(release: str) -> str:
    """`'v0.15.0'` / `'0.15.0'` -> `'0.15.0'`. The tag form carries a `v`; the pyprojects do not."""
    return release[1:] if release.startswith("v") else release


# ── the guard ────────────────────────────────────────────────────────────────────────────────────
def check_release_set(versions: dict, floor: str | None, release: str | None = None) -> list:
    """Return a list of named complaints; empty means the release set is coherent.

    PURE — takes already-read values, touches no filesystem, so the regression fixtures in
    `--selftest` exercise exactly the code the release runs and not a re-implementation of it.

    `versions` maps package NAME -> version, e.g. `{"columna": "0.15.0", "columna-core": "0.15.0"}`.
    `floor` is the umbrella's minimum `columna-core`. `release` is the tag, when one exists.
    """
    bad = []
    umbrella_v, core_v = versions.get("columna"), versions.get("columna-core")

    if umbrella_v is None or core_v is None:
        return [f"release set is missing a lockstep package: got {sorted(versions)}"]

    # 1. lockstep — the umbrella and core share the release version.
    if umbrella_v != core_v:
        bad.append(
            f"LOCKSTEP BROKEN: columna=={umbrella_v} but columna-core=={core_v}. The umbrella and "
            f"core share the release version (ratified 2026-08-20). This is the state that ships a "
            f"correction while the site and `pip install columna` still report the previous release "
            f"— and it resolves cleanly, so nothing downstream will fail for you."
        )

    # 2. the floor — the umbrella must not permit a core older than the release it names.
    if floor is None:
        bad.append("columna declares no `columna-core>=` floor — the umbrella must pin a minimum core")
    elif release_tuple(floor) < release_tuple(core_v):
        bad.append(
            f"CORE FLOOR TOO LOW: columna=={umbrella_v} permits columna-core>={floor}, which admits "
            f"a core older than {core_v}. `pip install columna=={umbrella_v}` could resolve to a core "
            f"without the correction this release is named after."
        )

    # 3. the release version, when there is one to bind to.
    if release is not None:
        want = normalize_release(release)
        for name, got in (("columna", umbrella_v), ("columna-core", core_v)):
            if got != want:
                bad.append(
                    f"RELEASE MISMATCH: tag names {want} but {name}=={got}. The tag must name the "
                    f"exact version the artifacts carry."
                )
    return bad


def read_release_set() -> tuple:
    """This commit's release set, read from the pyprojects: (versions, umbrella core floor)."""
    projects = {p: _project(p) for p in PACKAGES}
    versions = {projects[p]["name"]: projects[p]["version"] for p in PACKAGES}
    return versions, core_floor(projects[UMBRELLA])


# ── the regression fixtures ──────────────────────────────────────────────────────────────────────
# Every row is a state the release machinery has actually reached or could reach. The first is the
# one found in the v0.15.0 preflight: stale umbrella, both versions live on PyPI, dependencies
# satisfiable, every other guard green.
SELFTEST = [
    ("the 2026-08-20 stale-resolvable umbrella (core moved, umbrella did not)",
     {"columna": "0.14.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.14.0", None,
     ["LOCKSTEP BROKEN", "CORE FLOOR TOO LOW"]),
    ("...and the same state offered under a v0.15.0 tag",
     {"columna": "0.14.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.14.0", "v0.15.0",
     ["LOCKSTEP BROKEN", "CORE FLOOR TOO LOW", "RELEASE MISMATCH"]),
    ("lockstep held but the floor left a release behind",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.14.0", "v0.15.0",
     ["CORE FLOOR TOO LOW"]),
    # Both lockstep packages are named, deliberately: a mismatched tag is wrong about each of them,
    # and a reader fixing it needs to see every version the tag disagrees with, not the first.
    ("a tag that names a version nobody built",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.15.0", "v0.16.0",
     ["RELEASE MISMATCH: tag names 0.16.0 but columna==0.15.0",
      "RELEASE MISMATCH: tag names 0.16.0 but columna-core==0.15.0"]),
    ("umbrella ahead of core — the mirror of the found bug",
     {"columna": "0.16.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.15.0", None,
     ["LOCKSTEP BROKEN"]),
    ("no floor declared at all",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, None, None,
     ["declares no `columna-core>=` floor"]),
    # ── the states that must PASS ────────────────────────────────────────────────────────────────
    ("the intended v0.15.0 release set",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.15.0", "v0.15.0",
     []),
    ("server unchanged across releases is lawful — it is not in lockstep",
     {"columna": "0.16.0", "columna-core": "0.16.0", "columna-server": "0.8.2"}, "0.16.0", "v0.16.0",
     []),
    ("a floor AHEAD of the release is lawful — it forbids less, never more",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.15.1", None,
     []),
    ("v-prefixed and bare tags name the same release",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.15.0", "0.15.0",
     []),
    ("the historical v0.14.0 set still passes — the guard is not new policy applied backwards",
     {"columna": "0.14.0", "columna-core": "0.14.0", "columna-server": "0.8.2"}, "0.14.0", "v0.14.0",
     []),
]


def selftest() -> int:
    failures = 0
    for name, versions, floor, release, expect in SELFTEST:
        got = check_release_set(versions, floor, release)
        ok = len(got) == len(expect) and all(any(e in g for g in got) for e in expect)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            failures += 1
            print(f"        expected {expect}")
            print(f"        got      {got}")
    if failures:
        print(f"\nFAIL — {failures} of {len(SELFTEST)} release-coherence fixtures regressed.",
              file=sys.stderr)
        return 1
    print(f"\nOK — {len(SELFTEST)} release-coherence fixtures hold.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="validate the release set and print nothing (exit non-zero on a complaint)")
    ap.add_argument("--release", metavar="TAG",
                    help="also require the release set to match this tag, e.g. v0.15.0")
    ap.add_argument("--selftest", action="store_true", help="run the guard's regression fixtures")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    versions, floor = read_release_set()
    complaints = check_release_set(versions, floor, args.release)
    if complaints:
        print("release set is INCOHERENT — refusing to hand out pins:", file=sys.stderr)
        for c in complaints:
            print(f"  ✗ {c}", file=sys.stderr)
        print("\n  derived set: " + ", ".join(f"{n}=={v}" for n, v in versions.items()),
              file=sys.stderr)
        print(f"  columna's core floor: {floor}", file=sys.stderr)
        return 1

    if args.check:
        return 0
    print(" ".join(pin(p) for p in PACKAGES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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


def dep_floor(umbrella: dict, want: str) -> str | None:
    """The minimum version of `want` the umbrella permits — the `>=` bound in its dependencies."""
    for dep in umbrella.get("dependencies", []):
        name = re.split(r"[<>=!~;\[]", dep, maxsplit=1)[0].strip()
        if name == want:
            m = re.search(r">=\s*([0-9][^,;\s]*)", dep)
            return m.group(1) if m else None
    return None


def normalize_release(release: str) -> str:
    """`'v0.15.0'` / `'0.15.0'` -> `'0.15.0'`. The tag form carries a `v`; the pyprojects do not."""
    return release[1:] if release.startswith("v") else release


# ── the guard ────────────────────────────────────────────────────────────────────────────────────
def check_release_set(versions: dict, floors, release: str | None = None) -> list:
    """Return a list of named complaints; empty means the release set is coherent.

    PURE — takes already-read values, touches no filesystem, so the regression fixtures in
    `--selftest` exercise exactly the code the release runs and not a re-implementation of it.

    `versions` maps package NAME -> version. `floors` maps the umbrella's dependency NAME -> its
    minimum version (a bare string is accepted as the columna-core floor, for readability in the
    fixtures). `release` is the tag, when one exists.
    """
    if isinstance(floors, str) or floors is None:
        floors = {"columna-core": floors}
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

    # 2. the floors — the umbrella must not permit a COMPANION older than the one this release ships.
    #    Core is the lockstep companion; the server is the independently-versioned one. Both matter:
    #    v0.15.0 shipped a correct core floor and a stale SERVER floor, and the stale half is what
    #    made the published set incoherent (the demo's seeds came from the older server).
    for dep, shipped in (("columna-core", core_v), ("columna-server", versions.get("columna-server"))):
        floor = floors.get(dep)
        if shipped is None:
            continue
        if floor is None:
            bad.append(f"columna declares no `{dep}>=` floor — the umbrella must pin a minimum {dep}")
        elif release_tuple(floor) < release_tuple(shipped):
            label = "CORE" if dep == "columna-core" else "SERVER"
            bad.append(
                f"{label} FLOOR TOO LOW: columna=={umbrella_v} permits {dep}>={floor}, which admits "
                f"a {dep} older than the {shipped} this release ships. "
                f"`pip install columna=={umbrella_v}` could resolve to the stale companion."
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
    """This commit's release set, read from the pyprojects: (versions, umbrella dependency floors)."""
    projects = {p: _project(p) for p in PACKAGES}
    versions = {projects[p]["name"]: projects[p]["version"] for p in PACKAGES}
    floors = {d: dep_floor(projects[UMBRELLA], d) for d in ("columna-core", "columna-server")}
    return versions, floors


# ── THE PAYLOAD/VERSION INVARIANT (the third stale-artifact class) ───────────────────────────────
#
# 2026-08-20, found AFTER v0.15.0 published: `columna-server`'s SOURCE changed in the release (the
# four-mood demo seeds were re-cut by the generated-family law) while its VERSION stayed 0.8.2. PyPI
# therefore kept serving the pre-correction payload, `skip-existing` uploaded nothing, and
# `assert_pypi_versions.py` passed — 0.8.2 *is* live. The published set installed cleanly and the
# flagship `demo --play` printed a leg labelled `disclose` that returned `refuse`, exiting 0.
#
# The class, three variants deep now:
#     1. a stale PIN resolves                 (0.13.2/0.13.3)
#     2. a stale VERSION resolves             (v0.15.0 preflight — the lockstep guard above)
#     3. stale CONTENT behind an unchanged version resolves   (this one)
#
# THE INVARIANT (ratified Huayin, 2026-08-20):
#
#     If the distributable payload of a package differs from the payload represented by its
#     currently published version, that package's version must advance before the release proceeds.
#
# WHY IT COMPARES BUILT ARTIFACTS, NOT THE WORKING TREE. "Did files under packages/<x>/ change" is
# the wrong question and would have been a weak heuristic: it answers with commit history rather than
# with shipped bytes, it cannot see include/exclude rules, and it goes red for edits that never reach
# a wheel (tests, README-only churn under a package). The only trustworthy representation of what a
# package would ship is the wheel it actually builds. So this compares BUILT wheel against PUBLISHED
# wheel, normalized.
#
# WHAT "NORMALIZED" MEANS. Archive bytes are not comparable — zip entry order, timestamps and the
# `WHEEL` generator line all vary with the toolchain and would produce noisy false positives that
# train people to ignore the guard. The logical payload is: every entry's path and content hash, with
#   · the version-stamped `<name>-<ver>.dist-info/` prefix normalized (so the comparison is about
#     content, not about the directory name repeating the version);
#   · `RECORD` dropped (it is a manifest OF the hashes — including it double-counts and adds its own
#     ordering noise);
#   · `WHEEL` dropped (carries `Generator: hatchling 1.x` / `setuptools x.y` — a toolchain fact, not
#     a payload fact).
# `METADATA` is KEPT, deliberately: dependency floors live there, so loosening a floor without a
# version bump is exactly as much a payload change as editing code.
DIST_INFO_RE = re.compile(r"^[^/]+\.dist-info/")
_IGNORED_DIST_INFO = ("RECORD", "WHEEL")


def payload_entries(wheel_bytes: bytes) -> dict:
    """The normalized logical payload of a wheel: {normalized path: sha256 of content}."""
    import hashlib
    import io
    import zipfile

    out = {}
    with zipfile.ZipFile(io.BytesIO(wheel_bytes)) as z:
        for name in z.namelist():
            if name.endswith("/"):
                continue
            norm = DIST_INFO_RE.sub("*.dist-info/", name)
            if norm.startswith("*.dist-info/") and norm.rsplit("/", 1)[-1] in _IGNORED_DIST_INFO:
                continue
            out[norm] = hashlib.sha256(z.read(name)).hexdigest()
    return out


def payload_digest(wheel_bytes: bytes) -> str:
    """One stable digest over the normalized payload — the thing two builds must agree on."""
    import hashlib

    entries = payload_entries(wheel_bytes)
    h = hashlib.sha256()
    for path in sorted(entries):
        h.update(path.encode("utf-8"))
        h.update(b"\0")
        h.update(entries[path].encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def diff_payloads(built: dict, published: dict) -> dict:
    """What actually differs, so a failure names files rather than two opaque hashes."""
    b, p = set(built), set(published)
    return {
        "added": sorted(b - p),
        "removed": sorted(p - b),
        "changed": sorted(k for k in (b & p) if built[k] != published[k]),
    }


def published_wheel_url(name: str, version: str):
    """The PyPI URL of the wheel for an ALREADY-PUBLISHED version, or None if that version is absent.

    An absent version is not a failure — it is the normal case for the package being released.
    """
    import json
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=20) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    for u in data.get("urls", []):
        if u.get("packagetype") == "bdist_wheel":
            return u["url"]
    return None


def check_payload_coherence(built_wheels: dict, fetch=None) -> list:
    """Return named complaints; empty means no package ships changed content under a reused version.

    `built_wheels` maps `(name, version) -> wheel bytes`. `fetch` is injectable so the regression
    fixtures can exercise this without a network — the released path passes the real PyPI fetcher.
    """
    fetch = fetch or _default_fetch
    bad = []
    for (name, version), blob in sorted(built_wheels.items()):
        published = fetch(name, version)
        if published is None:
            continue                      # this version is not on PyPI yet — a genuinely new release
        if payload_digest(blob) == payload_digest(published):
            continue                      # identical payload under the same version — lawful skip-existing
        d = diff_payloads(payload_entries(blob), payload_entries(published))
        detail = ", ".join(
            f"{k}: {', '.join(v[:4])}{' …' if len(v) > 4 else ''}" for k, v in d.items() if v
        )
        bad.append(
            f"STALE PAYLOAD: {name}=={version} is already on PyPI, and this tree would build a "
            f"DIFFERENT package under that same version. `skip-existing` would upload nothing, so "
            f"the release would ship the OLD payload while claiming this tree. Bump {name} before "
            f"releasing. Differences — {detail}"
        )
    return bad


def _default_fetch(name: str, version: str):
    import urllib.request

    url = published_wheel_url(name, version)
    if url is None:
        return None
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def built_wheels_from(dist_dir: str) -> dict:
    """Read `(name, version) -> bytes` for every wheel in a dist directory (as publish.yml builds)."""
    import pathlib as _p

    out = {}
    for whl in sorted(_p.Path(dist_dir).glob("*.whl")):
        stem = whl.name.split("-")
        name, version = stem[0].replace("_", "-"), stem[1]
        out[(name, version)] = whl.read_bytes()
    return out


# ── the regression fixtures ──────────────────────────────────────────────────────────────────────
# Every row is a state the release machinery has actually reached or could reach. The first is the
# one found in the v0.15.0 preflight: stale umbrella, both versions live on PyPI, dependencies
# satisfiable, every other guard green.
SELFTEST = [
    ("the 2026-08-20 stale-resolvable umbrella (core moved, umbrella did not)",
     {"columna": "0.14.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.14.0", "columna-server": "0.8.2"}, None,
     ["LOCKSTEP BROKEN", "CORE FLOOR TOO LOW"]),
    ("...and the same state offered under a v0.15.0 tag",
     {"columna": "0.14.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.14.0", "columna-server": "0.8.2"}, "v0.15.0",
     ["LOCKSTEP BROKEN", "CORE FLOOR TOO LOW", "RELEASE MISMATCH"]),
    ("lockstep held but the floor left a release behind",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.14.0", "columna-server": "0.8.2"}, "v0.15.0",
     ["CORE FLOOR TOO LOW"]),
    # Both lockstep packages are named, deliberately: a mismatched tag is wrong about each of them,
    # and a reader fixing it needs to see every version the tag disagrees with, not the first.
    ("a tag that names a version nobody built",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.15.0", "columna-server": "0.8.2"}, "v0.16.0",
     ["RELEASE MISMATCH: tag names 0.16.0 but columna==0.15.0",
      "RELEASE MISMATCH: tag names 0.16.0 but columna-core==0.15.0"]),
    ("umbrella ahead of core — the mirror of the found bug",
     {"columna": "0.16.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.15.0", "columna-server": "0.8.2"}, None,
     ["LOCKSTEP BROKEN"]),
    ("no floor declared at all",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": None, "columna-server": "0.8.2"}, None,
     ["declares no `columna-core>=` floor"]),
    # ── the SERVER floor (v0.15.0 incident): the umbrella must not admit a stale companion ───────
    ("the v0.15.0 declaration itself — correct core floor, STALE server floor",
     {"columna": "0.15.1", "columna-core": "0.15.1", "columna-server": "0.8.3"},
     {"columna-core": "0.15.1", "columna-server": "0.8.2"}, "v0.15.1",
     ["SERVER FLOOR TOO LOW"]),
    ("core floor lags too, in the same declaration",
     {"columna": "0.15.1", "columna-core": "0.15.1", "columna-server": "0.8.3"},
     {"columna-core": "0.15.0", "columna-server": "0.8.2"}, "v0.15.1",
     ["CORE FLOOR TOO LOW", "SERVER FLOOR TOO LOW"]),
    ("no server floor declared at all",
     {"columna": "0.15.1", "columna-core": "0.15.1", "columna-server": "0.8.3"},
     {"columna-core": "0.15.1"}, None,
     ["declares no `columna-server>=` floor"]),
    # ── the states that must PASS ────────────────────────────────────────────────────────────────
    ("the intended v0.15.1 release set",
     {"columna": "0.15.1", "columna-core": "0.15.1", "columna-server": "0.8.3"},
     {"columna-core": "0.15.1", "columna-server": "0.8.3"}, "v0.15.1",
     []),
    ("the intended v0.15.0 release set (as it was declared — core-floor half only)",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.15.0", "columna-server": "0.8.2"}, "v0.15.0",
     []),
    ("server unchanged across releases is lawful — it is not in lockstep",
     {"columna": "0.16.0", "columna-core": "0.16.0", "columna-server": "0.8.2"},
     {"columna-core": "0.16.0", "columna-server": "0.8.2"}, "v0.16.0",
     []),
    ("a floor AHEAD of the release is lawful — it forbids less, never more",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.15.1", "columna-server": "0.8.3"}, None,
     []),
    ("v-prefixed and bare tags name the same release",
     {"columna": "0.15.0", "columna-core": "0.15.0", "columna-server": "0.8.2"},
     {"columna-core": "0.15.0", "columna-server": "0.8.2"}, "0.15.0",
     []),
    ("the historical v0.14.0 set still passes — the guard is not new policy applied backwards",
     {"columna": "0.14.0", "columna-core": "0.14.0", "columna-server": "0.8.2"},
     {"columna-core": "0.14.0", "columna-server": "0.8.2"}, "v0.14.0",
     []),
]


def _fake_wheel(files: dict) -> bytes:
    """A minimal in-memory wheel, for the payload fixtures — no network, no toolchain."""
    import io
    import zipfile

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, content in files.items():
            z.writestr(name, content)
    return buf.getvalue()


# The payload fixtures. The first is the v0.15.0 incident itself, reduced to its essence: the same
# version, on PyPI, with a different four-mood seed inside.
_PUB = {"columna_server/demo.py": 'DISCLOSE_Q = "SELECT stock.sum AT {store*cal.month}"',
        "columna_server-0.8.2.dist-info/METADATA": "Name: columna-server\nVersion: 0.8.2\n"}
_NEW = {"columna_server/demo.py": 'DISCLOSE_Q = "SELECT buyers AT {cal.month}"',
        "columna_server-0.8.2.dist-info/METADATA": "Name: columna-server\nVersion: 0.8.2\n"}
_NEW_BUMPED = {"columna_server/demo.py": 'DISCLOSE_Q = "SELECT buyers AT {cal.month}"',
               "columna_server-0.8.3.dist-info/METADATA": "Name: columna-server\nVersion: 0.8.3\n"}
# Same payload, different toolchain noise — must NOT trip the guard.
_PUB_NOISY = dict(_PUB, **{"columna_server-0.8.2.dist-info/WHEEL": "Generator: hatchling 1.27.0\n",
                           "columna_server-0.8.2.dist-info/RECORD": "columna_server/demo.py,sha256=x,42\n"})
# A loosened dependency floor with no version bump is a payload change too (METADATA is kept).
_PUB_FLOOR = {"columna/__init__.py": "", "columna-0.15.1.dist-info/METADATA":
              "Name: columna\nVersion: 0.15.1\nRequires-Dist: columna-core<1.0,>=0.15.1\n"}
_NEW_FLOOR = {"columna/__init__.py": "", "columna-0.15.1.dist-info/METADATA":
              "Name: columna\nVersion: 0.15.1\nRequires-Dist: columna-core<1.0,>=0.15.0\n"}

PAYLOAD_SELFTEST = [
    ("the 2026-08-20 incident: server content changed, version did not",
     {("columna-server", "0.8.2"): _fake_wheel(_NEW)},
     {("columna-server", "0.8.2"): _fake_wheel(_PUB)}, ["STALE PAYLOAD: columna-server==0.8.2"]),
    ("unchanged payload under a reused version — lawful skip-existing",
     {("columna-server", "0.8.2"): _fake_wheel(_PUB)},
     {("columna-server", "0.8.2"): _fake_wheel(_PUB)}, []),
    ("changed payload WITH a version bump — lawful",
     {("columna-server", "0.8.3"): _fake_wheel(_NEW_BUMPED)}, {}, []),
    ("toolchain noise only (WHEEL/RECORD differ) — must NOT trip",
     {("columna-server", "0.8.2"): _fake_wheel(_PUB)},
     {("columna-server", "0.8.2"): _fake_wheel(_PUB_NOISY)}, []),
    ("a loosened dependency floor with no bump IS a payload change",
     {("columna", "0.15.1"): _fake_wheel(_NEW_FLOOR)},
     {("columna", "0.15.1"): _fake_wheel(_PUB_FLOOR)}, ["STALE PAYLOAD: columna==0.15.1"]),
    ("the intended v0.15.1 set: all three new or unchanged — lawful",
     {("columna", "0.15.1"): _fake_wheel({"columna/__init__.py": ""}),
      ("columna-core", "0.15.1"): _fake_wheel({"columna_core/__init__.py": ""}),
      ("columna-server", "0.8.3"): _fake_wheel(_NEW_BUMPED)}, {}, []),
]


def payload_selftest() -> int:
    failures = 0
    for name, built, published, expect in PAYLOAD_SELFTEST:
        got = check_payload_coherence(built, fetch=lambda n, v: published.get((n, v)))
        ok = len(got) == len(expect) and all(any(e in g for g in got) for e in expect)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            failures += 1
            print(f"        expected {expect}")
            print(f"        got      {got}")
    return failures


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
    print()
    failures += payload_selftest()
    total = len(SELFTEST) + len(PAYLOAD_SELFTEST)
    if failures:
        print(f"\nFAIL — {failures} of {total} release-coherence fixtures regressed.", file=sys.stderr)
        return 1
    print(f"\nOK — {total} release-coherence fixtures hold "
          f"({len(SELFTEST)} release-set, {len(PAYLOAD_SELFTEST)} payload/version).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="validate the release set and print nothing (exit non-zero on a complaint)")
    ap.add_argument("--release", metavar="TAG",
                    help="also require the release set to match this tag, e.g. v0.15.0")
    ap.add_argument("--selftest", action="store_true", help="run the guard's regression fixtures")
    ap.add_argument("--check-payload", metavar="DIST_DIR",
                    help="refuse the release if any built wheel in DIST_DIR would ship content "
                         "different from what its already-published version serves (needs network)")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.check_payload:
        wheels = built_wheels_from(args.check_payload)
        if not wheels:
            print(f"no wheels found in {args.check_payload!r} — nothing to check, which is not the "
                  f"same as coherent. Build the dists first.", file=sys.stderr)
            return 1
        print("payload/version coherence — built wheels vs what PyPI already serves:")
        complaints = check_payload_coherence(wheels)
        for (name, version) in sorted(wheels):
            state = next((c for c in complaints if c.startswith(f"STALE PAYLOAD: {name}=={version}")), None)
            print(f"  {'STALE' if state else 'ok   '}  {name}=={version}")
        if complaints:
            print("\nrelease REFUSED — a package would ship changed content under a reused version:",
                  file=sys.stderr)
            for c in complaints:
                print(f"  ✗ {c}", file=sys.stderr)
            return 1
        print("OK — every reused version ships the payload it already published.")
        return 0

    versions, floors = read_release_set()
    complaints = check_release_set(versions, floors, args.release)
    if complaints:
        print("release set is INCOHERENT — refusing to hand out pins:", file=sys.stderr)
        for c in complaints:
            print(f"  ✗ {c}", file=sys.stderr)
        print("\n  derived set: " + ", ".join(f"{n}=={v}" for n, v in versions.items()),
              file=sys.stderr)
        print("  columna's floors: " + ", ".join(f"{d}>={f}" for d, f in floors.items()),
              file=sys.stderr)
        return 1

    if args.check:
        return 0
    print(" ".join(pin(p) for p in PACKAGES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

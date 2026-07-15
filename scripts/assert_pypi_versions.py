#!/usr/bin/env python3
"""Post-publish integrity check (publish.yml): assert every package's INTENDED version — the version
declared in its `pyproject.toml` — is actually live on PyPI after the release upload.

Fails loudly if any intended version is missing. This is the guard `skip-existing` needs: skip-existing
lets a release re-run without choking on already-published dists, but it must never *silently* skip a
version that was supposed to go out (a forgotten bump, a Trusted-Publisher misconfig, a swallowed
upload error). If the version we built is not on PyPI when the release job finishes, the release is a
lie — and this fails it.
"""
from __future__ import annotations

import json
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

PACKAGES = ["packages/columna-core", "packages/columna-server", "packages/columna"]
RETRIES, DELAY = 8, 10  # PyPI's JSON index lags the upload slightly; poll up to ~80s


def intended(pkg_dir: str) -> tuple[str, str]:
    data = tomllib.loads((Path(pkg_dir) / "pyproject.toml").read_text())
    return data["project"]["name"], data["project"]["version"]


def live_versions(name: str) -> set[str]:
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return set(json.load(r).get("releases", {}))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return set()          # project not on PyPI at all
        raise


def main() -> int:
    want = [intended(p) for p in PACKAGES]
    print("intended (from pyproject):", ", ".join(f"{n}=={v}" for n, v in want))
    missing: list = []
    for attempt in range(1, RETRIES + 1):
        missing = [(n, v) for n, v in want if v not in live_versions(n)]
        if not missing:
            print("OK — every intended version is live on PyPI.")
            return 0
        print(f"attempt {attempt}/{RETRIES}: not live yet: {missing}")
        if attempt < RETRIES:
            time.sleep(DELAY)
    print(f"FAIL — intended version(s) NOT live on PyPI: {missing}", file=sys.stderr)
    print("A version that should have published is missing — skip-existing or a swallowed upload "
          "error may have masked a forgotten bump. The release did not publish what it claimed.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

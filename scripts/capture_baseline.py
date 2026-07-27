#!/usr/bin/env python3
"""capture_baseline.py — the dated pre/post-launch record (§5 baseline captures).

    python scripts/capture_baseline.py specs/baselines/<YYYY-MM-DD>/

WHY THIS IS A SCRIPT AND NOT A ONE-OFF PASTE. The point of a baseline is that post-launch drift
becomes MEASURABLE against a dated record. A number you cannot re-derive is not a baseline, it is an
anecdote — you can look at it later but you cannot diff it, because you no longer know what question
produced it. So the capture is executable: run it again next week against a new dated directory and
the two are comparable by construction, field for field.

WHAT IT RECORDS, and the standing rule for each: **every field either carries a value or carries the
reason it does not.** A capture that silently omits an unavailable source reads, six weeks later, as
"this was zero" or "nobody thought to look" — both of which are confident wrong answers about our own
history. Unavailable is a finding. It gets written down, with its cause, in the file.

  site_state      the live version string, the seven primary surfaces, per-surface HTTP status and a
                  content hash (so a silent copy change is visible as a hash diff, not a vibe)
  github_traffic  views/clones/referrers/paths from the repo Traffic API snapshot on meta/analytics
  pypi            per-package live versions, requires-python as PyPI reports it, and download counts
  vercel_web      Vercel Web Analytics — PLAN-GATED on this account; see the note it writes
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

SITE = "https://datumwise.ai"

# The seven primary surfaces, read from BaseLayout.astro's `nav` — not a hand-kept list that can
# drift from the site. GitHub is the eighth nav entry and is external, so it is not a site surface.
PRIMARY_SURFACES = ["/learn", "/case", "/positions", "/thesis", "/why", "/ladder", "/atlas"]

# Not in the primary nav, but load-bearing for launch: the install door and the machine-readable
# corpus an external AI reads. Captured separately so the seven stay the seven.
ALSO_CAPTURED = ["/", "/install", "/llms.txt"]

PACKAGES = ["columna", "columna-core", "columna-server"]

UA = {"User-Agent": "datumwise-baseline-capture/1.0 (+https://datumwise.ai)"}


def _get(url: str, timeout: int = 30, headers: dict | None = None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def capture_site() -> dict:
    out: dict = {"origin": SITE, "surfaces": {}, "primary_surface_count": len(PRIMARY_SURFACES)}

    for path in PRIMARY_SURFACES + ALSO_CAPTURED:
        rec: dict = {"primary": path in PRIMARY_SURFACES}
        try:
            status, body = _get(SITE + path)
            text = body.decode("utf-8", "replace")
            rec["status"] = status
            rec["bytes"] = len(body)
            # A hash makes a silent copy edit VISIBLE in a diff of two captures. Without it the only
            # evidence of a changed page is a byte count, which collides trivially.
            rec["sha256"] = hashlib.sha256(body).hexdigest()
            start = text.find("<title>")
            if start != -1:
                rec["title"] = text[start + 7:text.find("</title>", start)].strip()
        except Exception as exc:                      # noqa: BLE001 — the reason IS the record
            rec["status"] = None
            rec["unavailable_reason"] = f"{type(exc).__name__}: {exc}"
        out["surfaces"][path] = rec

    # The live version string, from the homepage. This is the number the site CLAIMS to be running;
    # it is generated from the PyPI-pinned package at deploy, so a mismatch against `pypi` below
    # means the deploy and the publish have come apart.
    try:
        _, body = _get(SITE + "/")
        text = body.decode("utf-8", "replace")
        marker = "currently at "
        i = text.find(marker)
        out["live_version_string"] = (
            text[i + len(marker):i + len(marker) + 12].split("<")[0].strip().rstrip(".")
            if i != -1 else None)
    except Exception as exc:                          # noqa: BLE001
        out["live_version_string"] = None
        out["live_version_unavailable_reason"] = f"{type(exc).__name__}: {exc}"

    return out


def capture_pypi() -> dict:
    out: dict = {"packages": {}}
    for pkg in PACKAGES:
        rec: dict = {}
        try:
            # /simple/ is what pip RESOLVES FROM. The JSON metadata endpoint is a different vantage
            # point and has been observed stale in BOTH directions (0.13.1 and 0.13.2). Record the
            # resolver's answer as authoritative and the JSON's separately, so a future disagreement
            # is legible rather than confusing.
            _, body = _get(
                f"https://pypi.org/simple/{pkg}/",
                headers={"Accept": "application/vnd.pypi.simple.v1+json"})
            rec["simple_index_versions_tail"] = json.loads(body).get("versions", [])[-5:]
        except Exception as exc:                      # noqa: BLE001
            rec["simple_index_unavailable_reason"] = f"{type(exc).__name__}: {exc}"

        try:
            _, body = _get(f"https://pypi.org/pypi/{pkg}/json")
            info = json.loads(body)["info"]
            rec["json_api_latest_version"] = info.get("version")
            rec["requires_python"] = info.get("requires_python")
        except Exception as exc:                      # noqa: BLE001
            rec["json_api_unavailable_reason"] = f"{type(exc).__name__}: {exc}"

        try:
            _, body = _get(f"https://pypistats.org/api/packages/{pkg}/recent")
            rec["downloads_recent"] = json.loads(body).get("data")
        except Exception as exc:                      # noqa: BLE001
            # pypistats rate-limits aggressively and anonymously. "if trivially available" was the
            # instruction; when it is not, the reason is the record.
            rec["downloads_unavailable_reason"] = f"{type(exc).__name__}: {exc}"

        out["packages"][pkg] = rec
    return out


def capture_github_traffic(repo_root: pathlib.Path) -> dict:
    """Read the newest snapshot from the isolated meta/analytics branch."""
    def git(*args) -> str:
        return subprocess.run(["git", "-C", str(repo_root), *args],
                              capture_output=True, text=True, check=True).stdout

    try:
        git("fetch", "-q", "origin", "meta/analytics")
        names = [n for n in git("ls-tree", "-r", "--name-only", "FETCH_HEAD").splitlines()
                 if n.startswith("snapshots/")]
        if not names:
            return {"unavailable_reason": "no snapshots/ files on meta/analytics"}
        newest = sorted(names)[-1]
        payload = json.loads(git("show", f"FETCH_HEAD:{newest}"))
        return {"source_file": newest, "snapshot": payload}
    except Exception as exc:                          # noqa: BLE001
        return {"unavailable_reason": f"{type(exc).__name__}: {exc}"}


def capture_vercel_web() -> dict:
    """Vercel Web Analytics — recorded as BLOCKED, with the exact cause and the human workaround.

    The public Web Analytics API (`/v1/query/web-analytics/events/aggregate`) exists and authenticates
    fine with the project token, but EVERY grouping dimension returns
    `payment_required: Accessing Analytics custom events requires an Enterprise or Pro plan` on this
    account's plan — including plain `by=day`. So the website's own page counts, referrers and the
    utm_source rows are NOT machine-exportable from here. They are visible in the dashboard, which
    offers a CSV export; a human pasting that CSV beside this file completes the capture.
    """
    return {
        "status": "BLOCKED — plan-gated, not missing",
        "api": "https://api.vercel.com/v1/query/web-analytics/events/aggregate",
        "observed_error": ("payment_required: Accessing Analytics custom events requires an "
                           "Enterprise or Pro plan (returned for every `by` dimension, incl. `day`)"),
        "consequence": ("site page-counts-by-path, referrers, and the utm_source=chatgpt.com row "
                        "cannot be captured programmatically on the current plan"),
        "workaround": ("Vercel dashboard → project `website` → Analytics → CSV export, saved beside "
                       "this file as vercel_web_analytics.csv"),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2

    outdir = pathlib.Path(argv[1])
    outdir.mkdir(parents=True, exist_ok=True)
    repo_root = pathlib.Path(__file__).resolve().parent.parent

    for name, payload in [
        ("site_state.json", capture_site()),
        ("pypi.json", capture_pypi()),
        ("github_traffic.json", capture_github_traffic(repo_root)),
        ("vercel_web_analytics.json", capture_vercel_web()),
    ]:
        (outdir / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {outdir / name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

#!/usr/bin/env python3
"""
harvest_zenodo_snapshot.py — THE EVIDENCE CAPTURE for the publication registry.

The registry's bibliographic facts (title, version, date, DOI, authors, licence) are NEVER hand-typed.
They are read from Zenodo, frozen into a dated snapshot beside the registry, and the checker asserts
the registry equals the snapshot. This file is how the snapshot is made and re-made.

WHY A FROZEN SNAPSHOT AND NOT A LIVE CALL. A gate that reaches the network is a gate that fails on
someone else's outage and passes on someone else's cache. The snapshot makes the gate hermetic and
makes the evidence reviewable in the diff: when a publication fact changes, the change is visible as
bytes in a PR, with a date on it, rather than as a silent difference between two CI runs.

SEEDS, THEN EXPANSION. Zenodo's public search does not index this project's creator string (a query
for "Huayin Wang" returns zero hits — verified 2026-08-21), so a creator sweep is not available.
Instead: seed from every Zenodo record id cited anywhere in this repo, resolve each to its CONCEPT
record, and expand the concept to ALL of its versions. That makes the snapshot closed under
versioning — the property the registry actually needs — without depending on a search index.

Usage:
    python scripts/harvest_zenodo_snapshot.py                  # rescan repo for seeds, write snapshot
    python scripts/harvest_zenodo_snapshot.py --out FILE
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = "https://zenodo.org/api/records"
TOKEN_RE = re.compile(r"zenodo\.(\d{6,9})")


def _get(url: str) -> dict:
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return json.load(resp)
        except Exception as exc:  # noqa: BLE001 - reported, then retried
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"zenodo unreachable for {url}: {last}")


EXTRA_SEEDS = ROOT / "registry" / "publications" / "extra_seeds.txt"


def repo_seeds() -> list[str]:
    """Every Zenodo record id cited in a TRACKED file. dist/ is build output, so it is excluded."""
    # `registry` IS EXCLUDED, and it has to be (2026-08-21). Once the registry landed, its own files
    # became the largest source of Zenodo ids in the repo — including CONCEPT recids, which are not
    # version records. Seeding from them asks Zenodo for /records/<concept>/versions, which 404s, and
    # the harvester correctly refused to write a snapshot it could not complete. Seeds come from what
    # the repo CITES plus extra_seeds.txt; the registry is the OUTPUT of this script, never its input.
    out = subprocess.run(
        ["git", "grep", "-h", "-oE", r"zenodo\.[0-9]{6,9}", "--", ".",
         ":(exclude)apps/website/dist", ":(exclude)registry"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    ).stdout
    return sorted({m.group(1) for m in TOKEN_RE.finditer(out)})


def extra_seeds() -> list[str]:
    """Ruled-but-uncited ids. See registry/publications/extra_seeds.txt for why this exists."""
    if not EXTRA_SEEDS.exists():
        return []
    ids = []
    for line in EXTRA_SEEDS.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            ids.append(line)
    return ids


def flatten(rec: dict) -> dict:
    meta = rec["metadata"]
    return {
        "recid": str(rec["id"]),
        "doi": rec.get("doi"),
        "conceptRecid": str(rec.get("conceptrecid")),
        "conceptDoi": rec.get("conceptdoi"),
        "title": meta.get("title"),
        "version": meta.get("version"),
        "publicationDate": meta.get("publication_date"),
        "resourceType": (meta.get("resource_type") or {}).get("title"),
        "license": (meta.get("license") or {}).get("id"),
        "authors": [c.get("name") for c in meta.get("creators", [])],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--seed", action="append", default=[])
    args = ap.parse_args()

    seeds = sorted(set(repo_seeds()) | set(extra_seeds()) | set(args.seed))
    print(f"seeds from repo: {len(seeds)}", file=sys.stderr)

    records: dict[str, dict] = {}
    concepts: dict[str, dict] = {}
    missing: list[str] = []

    for seed in seeds:
        if seed in records:
            continue
        try:
            rec = _get(f"{API}/{seed}")
        except Exception as exc:  # noqa: BLE001
            missing.append(seed)
            print(f"  MISS {seed}: {exc}", file=sys.stderr)
            continue
        records[str(rec["id"])] = flatten(rec)
        concept = str(rec.get("conceptrecid"))
        if concept in concepts:
            continue
        vs = _get(f"{API}/{seed}/versions?size=25&sort=version")
        hits = vs["hits"]["hits"]
        if vs["hits"]["total"] > len(hits):
            raise SystemExit(
                f"REFUSING TO WRITE A PARTIAL SNAPSHOT: concept {concept} has "
                f"{vs['hits']['total']} versions but the page returned {len(hits)}. "
                "Paginate before trusting this file."
            )
        for hit in hits:
            records[str(hit["id"])] = flatten(hit)
        concepts[concept] = {
            "conceptRecid": concept,
            "conceptDoi": rec.get("conceptdoi"),
            "versionCount": vs["hits"]["total"],
            "versions": sorted((str(h["id"]) for h in hits), key=lambda r: int(r)),
        }

    payload = {
        "source": "https://zenodo.org/api/records",
        "note": (
            "Frozen evidence for registry/publications. Regenerate with "
            "scripts/harvest_zenodo_snapshot.py. Seeds are every Zenodo id cited in a tracked file, "
            "expanded to every version of each seed's concept record."
        ),
        "seedCount": len(seeds),
        "unresolvedSeeds": missing,
        "concepts": dict(sorted(concepts.items())),
        "records": dict(sorted(records.items())),
    }
    text = json.dumps(payload, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}: {len(records)} records, {len(concepts)} concepts", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

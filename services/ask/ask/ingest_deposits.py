"""Fetch the EXACT current deposited text for representative-corpus works that live only on Zenodo.

WHY THIS EXISTS, AND WHY IT IS NOT OPTIONAL (Huayin, 2026-08-25).

The representative corpus is 16 works. THIRTEEN of them are deposit-only: they have no onsite route,
so before this module Ask could cite them but never quote them. The whole default corpus — the works
through which datumwise states its intellectual position — was unreadable by the agent, while the
reference layer (manuals, teaching surfaces, positions) was fully readable.

That asymmetry is dangerous in a specific way, and the ruling named it: it would quietly push Ask
back toward whatever is easiest to retrieve. An agent that can quote the Frame-QL Manual but not The
Theory of Data will constitute datumwise's position out of the manual. So ingestion is a requirement
of the corpus ruling, not a convenience.

DETERMINISTIC, AND PINNED TO A RECORD.
  · The record fetched is the one the registry rules `current` — never "newest on Zenodo". If the
    registry moves, this must be re-run, and the diff shows exactly which edition changed.
  · Zenodo's own checksum is verified on download and stored in the manifest. A silent re-upload
    under the same record id is therefore detectable.
  · The manifest records recordId, version, date, checksum and byte length. `--check` re-verifies
    the stored files against it without any network access, so CI can assert the corpus has not
    drifted without depending on Zenodo being up.

WHAT IS DELIBERATELY NOT DONE. No PDF extraction. Two IN works are deposited as PDF only
(see MISSING_TEXT in the run report), and text pulled out of a PDF is a lossy derivation, not the
exact deposited text the ruling asks for. Adding a PDF parser would also spend the dependency budget
to paper over what is really a deposit-practice gap: the other eleven works already ship a `.md`
beside the PDF. The remedy is to deposit one for those two as well, and it is reported rather than
worked around.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CORPUS = REPO / "registry" / "sources" / "current-corpus.json"
SOURCES = REPO / "registry" / "sources" / "sources.json"
RECORDS = REPO / "registry" / "publications" / "records.json"
WORKS = REPO / "registry" / "publications" / "works.json"
OUT = Path(__file__).resolve().parent.parent / "deposits"
MANIFEST = OUT / "manifest.json"

TEXT_EXT = (".md", ".markdown", ".txt")
UA = {"User-Agent": "datumwise-ask-ingest/0 (+https://datumwise.ai)"}


def _get(url: str, timeout: int = 60) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def _registry():
    corpus = json.loads(CORPUS.read_text())
    cat = json.loads(SOURCES.read_text())
    sources = {s["sourceId"]: s for s in (cat["sources"] if isinstance(cat, dict) else cat)}
    records = json.loads(RECORDS.read_text())
    works = {w["workId"]: w for w in json.loads(WORKS.read_text())}
    return corpus, sources, records, works


def current_record(records: list[dict], work_id: str) -> dict:
    found = [r for r in records if r.get("workId") == work_id and r.get("status") == "current"]
    if len(found) != 1:
        raise SystemExit(f"registry: work {work_id!r} has {len(found)} current records, expected 1")
    return found[0]


def targets() -> list[dict]:
    """IN sources with no onsite route — the ones Ask cannot otherwise read."""
    corpus, sources, records, works = _registry()
    out = []
    for sid in corpus["in"]:
        s = sources[sid]
        if s.get("route"):
            continue  # already readable from the shipped site build
        wid = s.get("workId")
        if not wid:
            continue  # an IN source with neither route nor deposit would be a catalog defect
        rec = current_record(records, wid)
        out.append({"sourceId": sid, "workId": wid, "label": works[wid]["canonicalLabel"],
                    "recordId": rec["recordId"], "recid": str(rec["recid"]),
                    "version": rec.get("version"), "date": rec.get("date"), "doi": rec.get("doi")})
    return out


def fetch() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest, missing = [], []
    for t in targets():
        meta = json.loads(_get(f"https://zenodo.org/api/records/{t['recid']}"))
        files = meta.get("files", [])
        text = next((f for f in files if f["key"].lower().endswith(TEXT_EXT)), None)
        if not text:
            missing.append({**t, "deposited": sorted({f["key"].rsplit(".", 1)[-1] for f in files})})
            print(f"  MISSING TEXT  {t['sourceId']:<32} {t['label'][:44]}", flush=True)
            continue

        blob = _get(text["links"]["self"])
        got = hashlib.md5(blob).hexdigest()
        want = (text.get("checksum") or "").replace("md5:", "")
        if want and got != want:
            raise SystemExit(f"checksum mismatch for {t['sourceId']}: zenodo says {want}, got {got}")

        path = OUT / f"{t['recordId']}.md"
        path.write_bytes(blob)
        manifest.append({**t, "file": path.name, "zenodoKey": text["key"],
                         "md5": got, "bytes": len(blob),
                         "sha256": hashlib.sha256(blob).hexdigest()})
        print(f"  ok            {t['sourceId']:<32} {len(blob):>7} bytes  {text['key']}", flush=True)
        time.sleep(0.4)  # be a polite client

    payload = {
        "$comment": "Generated by ask/ingest_deposits.py. Do not hand-edit. Every entry is pinned "
                    "to the record the publication registry rules CURRENT; re-run after a "
                    "registry change and the diff shows which edition moved.",
        "deposits": manifest,
        "missingText": missing,
    }
    MANIFEST.write_text(json.dumps(payload, indent=1))
    return payload


def check() -> int:
    """Offline: verify stored files still match the manifest, and that it matches the registry."""
    if not MANIFEST.exists():
        print("no deposit manifest — run `python3 -m ask.ingest_deposits` first")
        return 1
    m = json.loads(MANIFEST.read_text())
    want = {t["sourceId"]: t for t in targets()}
    bad = 0
    for d in m["deposits"]:
        p = OUT / d["file"]
        if not p.exists():
            print(f"  MISSING FILE  {d['file']}")
            bad += 1
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != d["sha256"]:
            print(f"  ALTERED       {d['file']} no longer matches its recorded sha256")
            bad += 1
        w = want.get(d["sourceId"])
        if w and w["recordId"] != d["recordId"]:
            print(f"  STALE         {d['sourceId']} is ingested at {d['recordId']} but the registry "
                  f"now rules {w['recordId']} current — re-run the ingest")
            bad += 1
    covered = {d["sourceId"] for d in m["deposits"]} | {x["sourceId"] for x in m["missingText"]}
    for sid in want:
        if sid not in covered:
            print(f"  UNINGESTED    {sid} is IN and deposit-only but absent from the manifest")
            bad += 1
    if bad:
        print(f"\ndeposit check FAILED — {bad} problem(s)")
        return 1
    print(f"deposits OK — {len(m['deposits'])} ingested, {len(m['missingText'])} awaiting a text "
          f"deposit, all checksums match the manifest")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    out = fetch()
    print(f"\ningested {len(out['deposits'])}; {len(out['missingText'])} have no text deposit")
    for x in out["missingText"]:
        print(f"  · {x['label']} — deposited as {x['deposited']} only (record {x['recordId']})")

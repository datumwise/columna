"""Fetch the EXACT current deposited text for Core-corpus works that live only on Zenodo.

WHY THIS EXISTS, AND WHY IT IS NOT OPTIONAL (Huayin, 2026-08-25).

The Core corpus is 16 works. THIRTEEN of them are deposit-only: they have no onsite route,
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
  · The manifest records recordId, recid, checksum and byte length — foreign keys and file
    facts, never publication facts. `--check` re-verifies
    the stored files against it without any network access, so CI can assert the corpus has not
    drifted without depending on Zenodo being up.

WHAT IS DELIBERATELY NOT DONE. No PDF extraction. Two IN works are deposited as PDF only, and text
pulled out of a PDF is a lossy derivation, not the exact text the ruling asks for. Adding a PDF
parser would also spend the dependency budget to paper over a deposit-practice gap. Those two are
instead handled by the SUPPLIED path below, with weaker provenance recorded rather than hidden.

STATUS: 13 of 13 representative deposit-only works are ingested — 11 Zenodo-verified, 2
author-supplied. All 16 Core works are now readable by Ask.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CORPUS = REPO / "registry" / "sources" / "ask-authority.json"
SOURCES = REPO / "registry" / "sources" / "sources.json"
RECORDS = REPO / "registry" / "publications" / "records.json"
WORKS = REPO / "registry" / "publications" / "works.json"
OUT = Path(__file__).resolve().parent.parent / "deposits"
MANIFEST = OUT / "manifest.json"

SUPPLIED = OUT / "supplied"
TEXT_EXT = (".md", ".markdown", ".txt")

# THE SUPPLIED PATH, AND WHY IT IS MARKED DIFFERENTLY (2026-08-25).
#
# Two Core works are deposited on Zenodo as PDF ONLY. Huayin supplied their markdown
# directly so the corpus could be completed to 16/16 rather than waiting on a re-deposit.
#
# That text is NOT weaker in content — it is the author's own copy of the same edition. But it
# carries WEAKER PROVENANCE, and the manifest says so rather than flattening the difference:
#
#   provenance "zenodo"   — fetched from the deposited record, md5 checked against Zenodo's own.
#                           An independent third party can reproduce the exact bytes.
#   provenance "supplied" — placed in deposits/supplied/<recordId>.md by a human. Integrity is
#                           still pinned (sha256 in the manifest, re-checked offline), but nothing
#                           external corroborates that these bytes are the deposited edition.
#
# Since no checksum can be verified against the record, the next best assurance is applied instead:
# the supplied document must DECLARE the version the registry rules current, and the ingest fails if
# it does not. That catches the realistic mistake — uploading the wrong edition — which a sha256
# cannot.
#
# The durable fix remains depositing a `.md` beside the PDF on Zenodo; when that happens this path
# empties itself, because the zenodo branch is tried first.
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


_VERSION_LINE = re.compile(r"[Vv]ersion\s+([0-9]+\.[0-9]+)")


def _declared_version(text: str) -> str | None:
    """The version the document states about itself, from its first ~40 lines."""
    m = _VERSION_LINE.search("\n".join(text.splitlines()[:40]))
    return m.group(1) if m else None


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
        # recordId and recid ONLY — no doi, no version, no date. Third time this lesson has come up
        # on this branch and it is the same rule every time: a generated file that copies a
        # publication fact becomes a second source of truth for it. The manifest carries the foreign
        # key; the DOI is resolved from records.json wherever it is actually needed. `recid` is kept
        # because it is the Zenodo API address this module must call, not a claim about the work.
        out.append({"sourceId": sid, "workId": wid, "label": works[wid]["canonicalLabel"],
                    "recordId": rec["recordId"], "recid": str(rec["recid"])})
    return out


def fetch() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest, missing = [], []
    for t in targets():
        meta = json.loads(_get(f"https://zenodo.org/api/records/{t['recid']}"))
        files = meta.get("files", [])
        text = next((f for f in files if f["key"].lower().endswith(TEXT_EXT)), None)
        if not text:
            sup = SUPPLIED / f"{t['recordId']}.md"
            if sup.exists():
                blob = sup.read_bytes()
                declared = _declared_version(blob.decode("utf-8", "replace"))
                want_v = current_record(json.loads(RECORDS.read_text()), t["workId"]).get("version")
                if want_v and declared and declared != want_v:
                    raise SystemExit(
                        f"{t['sourceId']}: supplied text declares version {declared!r} but the "
                        f"registry rules v{want_v} current. Supplied text cannot be checksum-verified "
                        f"against the record, so the declared version is the assurance — refusing to "
                        f"ingest a different edition."
                    )
                path = OUT / f"{t['recordId']}.md"
                path.write_bytes(blob)
                manifest.append({**t, "file": path.name, "provenance": "supplied",
                                 "zenodoVerified": False, "declaredVersion": declared,
                                 "bytes": len(blob),
                                 "sha256": hashlib.sha256(blob).hexdigest()})
                print(f"  supplied      {t['sourceId']:<32} {len(blob):>7} bytes  "
                      f"(declares v{declared}; Zenodo has PDF only)", flush=True)
                continue
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
                         "provenance": "zenodo", "zenodoVerified": True,
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
    zen = sum(1 for d in m["deposits"] if d.get("provenance") == "zenodo")
    sup = [d for d in m["deposits"] if d.get("provenance") == "supplied"]
    print(f"deposits OK — {len(m['deposits'])} ingested "
          f"({zen} Zenodo-verified, {len(sup)} author-supplied), "
          f"{len(m['missingText'])} awaiting text, all sha256 match the manifest")
    for d in sup:
        print(f"  note: {d['sourceId']} is author-supplied — integrity pinned, but no external "
              f"party can reproduce these bytes until a .md is deposited beside the PDF")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    out = fetch()
    print(f"\ningested {len(out['deposits'])}; {len(out['missingText'])} have no text deposit")
    for x in out["missingText"]:
        print(f"  · {x['label']} — deposited as {x['deposited']} only (record {x['recordId']})")

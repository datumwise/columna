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

WHICH FILE IN THE RECORD IS THE WORK is a separate question from which record is current, and since
2026-09-07 it has a separate answer: see ARTIFACT SELECTION below. A record may deposit more than one
document, and this module refuses to guess which of them is the work.

STATUS is not re-typed here. `--check` prints the live counts, because a status line that must be
edited to stay true is the defect this whole registry exists to remove. What is worth stating is the
DIRECTION: the supplied path empties itself. It held two works; A Primer on the Theory of Data left it
on 2026-09-08 when v2.3 deposited a .md beside the PDF and the text became publisher-verifiable, and
one work remains on it. All Core works are readable by Ask.

Usage:
    python services/ask/ask/ingest_deposits.py              # fetch and rewrite the deposit corpus
    python services/ask/ask/ingest_deposits.py --check      # offline: bytes AND binding
    python services/ask/ask/ingest_deposits.py --selftest   # hermetic selection fixtures, no network
"""

from __future__ import annotations

import contextlib
import hashlib
import io
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


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# ARTIFACT SELECTION — WHICH FILE IN THE RECORD IS THE WORK (Huayin, ruling of 2026-09-07).
#
# THE DEFECT THIS CLOSES. Until today this module chose the work's text like this:
#
#     text = next((f for f in files if f["key"].lower().endswith(TEXT_EXT)), None)
#
# — the FIRST markdown file in whatever order Zenodo's API happened to return. Every deposit in the
# corpus carried exactly one text file, so the rule was never wrong and never tested. Record 22289091
# was the last one where that was true. The Theory of Data v7.1 (22649945) deposits TWO markdown
# documents under ONE record: the 140 KB foundation, and a 10 KB statistical extension reference that
# legitimately shares the DOI. On the day it was read, the API returned the foundation first — by
# ordering, not by rule.
#
# Zenodo's file order is not a contract. Had it flipped, this module would have written a 10 KB
# supplement into `w-theory-of-data.rNN.md`, and Ask and /read/theory-of-data would have served a
# supplement as *The Theory of Data*, under the right DOI, byte-verified against the right record.
# `--check` would have passed: it compares stored bytes to the manifest, and the manifest would have
# recorded the wrong file as the right one. A self-consistent manifest is not a correct one — which
# is why `check()` now validates the BINDING and not only the bytes.
#
# THE RULE, AND WHY IT IS SHAPED THIS WAY.
#
#   · A DECLARED key selects exactly that artifact. The declaration lives in the source catalog as
#     `artifacts: {<recordId>: <fileKey>}` — a foreign key and a file name, and nothing else. No
#     title, version, date or currentness is duplicated there; those have an authority already and a
#     second copy of a publication fact is the defect this whole registry exists to remove.
#   · IT IS KEYED BY recordId, NOT BY SOURCE. A selection made for one edition must not silently
#     carry into its successor: the successor is a different deposit with different files, and a
#     stale selector that still resolves is worse than one that fails. A new record simply has no
#     declaration, and falls to the rule below.
#   · WITHOUT A DECLARATION, EXACTLY ONE eligible text is acceptable. That is the whole of the old
#     behaviour, restated as a rule instead of an accident, and it keeps every existing single-text
#     deposit working unchanged.
#   · MULTIPLE ELIGIBLE TEXTS AND NO DECLARATION FAILS CLOSED. It does not guess, and it does not
#     fall through to the supplied-copy path — an ambiguity answered from a local file would be the
#     same wrong answer with weaker provenance.
#   · A DECLARED KEY THAT IS NOT IN THE RECORD FAILS CLOSED, even when another text is available.
#     Falling back would make the declaration advisory, and an advisory guard is not one.
#
# NOTHING HERE READS API ORDER, SORTS BY FILENAME, COMPARES FILE SIZES, OR INTERPRETS A TITLE. Each
# of those would be a heuristic that is right until it is not, and the failure mode is silent.
#
# THE COMPANION IS NOT DISCARDED. The non-selected texts of the record are recorded in the manifest
# with their publisher checksums, so the supplement's identity and its link to this record are
# preserved as evidence — without giving it a second publication identity, a second source id, or a
# second file on disk that the recordId-based storage convention would then overwrite.


class ChecksumError(RuntimeError):
    """The bytes are not the bytes the publisher deposited."""


def verify_publisher_checksum(blob: bytes, file_meta: dict, *, what: str) -> str:
    """Match the download against ZENODO'S OWN md5 and return it. A locally computed digest is not
    verification — it agrees with itself no matter what arrived — so a record that publishes no
    checksum cannot earn `zenodoVerified` here either."""
    got = hashlib.md5(blob).hexdigest()
    want = (file_meta.get("checksum") or "").replace("md5:", "")
    if not want:
        raise ChecksumError(f"{what}: the record publishes no checksum for {file_meta.get('key')!r}. "
                            f"REFUSING to call a self-computed digest publisher verification.")
    if got != want:
        raise ChecksumError(f"checksum mismatch for {what}: zenodo says {want}, got {got}")
    return got


class SelectionError(RuntimeError):
    """The record does not determine one artifact. Raised instead of guessing."""


def eligible_texts(files: list[dict]) -> list[dict]:
    """Every text artifact in a record. Sorted by key for STABLE REPORTING ONLY — no rule reads
    position, and `select_text` never indexes this list except when it holds exactly one member."""
    return sorted((f for f in files if f["key"].lower().endswith(TEXT_EXT)),
                  key=lambda f: f["key"])


def declared_artifact(source: dict, record_id: str) -> str | None:
    """The file key this source declares for THIS record, or None. Never inherited from another."""
    return (source.get("artifacts") or {}).get(record_id)


def select_text(files: list[dict], declared: str | None, *, source_id: str,
                record_id: str) -> tuple[dict | None, str]:
    """Choose the work's text. Returns (file, how) — (None, 'no-text') means the supplied path may
    be tried. Raises SelectionError on every ambiguity; ambiguity NEVER reaches the supplied path."""
    eligible = eligible_texts(files)
    keys = [f["key"] for f in eligible]

    if declared is not None:
        match = [f for f in eligible if f["key"] == declared]
        if not match:
            raise SelectionError(
                f"{source_id}: the source catalog declares artifact {declared!r} for record "
                f"{record_id}, and that record does not contain it. Deposited texts: {keys or 'none'}. "
                f"REFUSING — a declared key that silently fell back to another file would make the "
                f"declaration advisory, and the whole point of declaring is that it is not."
            )
        return match[0], "declared"

    if len(eligible) == 1:
        return eligible[0], "sole-text"
    if not eligible:
        return None, "no-text"

    raise SelectionError(
        f"{source_id}: record {record_id} deposits {len(eligible)} text artifacts and the source "
        f"catalog declares none of them: {keys}. REFUSING — this module will not choose the work "
        f"out of a record by API order, filename, size or title. Add "
        f"`\"artifacts\": {{\"{record_id}\": \"<key>\"}}` to {source_id} in "
        f"registry/sources/sources.json, naming the artifact that IS the work."
    )


def current_record(records: list[dict], work_id: str) -> dict:
    found = [r for r in records if r.get("workId") == work_id and r.get("status") == "current"]
    if len(found) != 1:
        raise SystemExit(f"registry: work {work_id!r} has {len(found)} current records, expected 1")
    return found[0]


def record_by_id(records: list[dict], record_id: str) -> dict:
    found = [r for r in records if r.get("recordId") == record_id]
    if len(found) != 1:
        raise SystemExit(f"registry: recordId {record_id!r} matched {len(found)} records, expected 1")
    return found[0]


def targets() -> list[dict]:
    """The deposits Ask must hold: current Core, plus every PRESERVED EDITION.

    TWO CLASSES, AND THEY ARE PINNED DIFFERENTLY. That is the whole point of this function.

      CORE          — a source that currently states datumwise's position. It floats: it is pinned
                      to whatever record the registry rules CURRENT, so when a work is superseded
                      this function starts asking for a different file and `--check` reports the
                      old one as STALE. Skipped if the source has an onsite route, because the site
                      build already makes that text readable.
      HISTORICAL    — a preserved edition, carrying its own sourceId because one sourceId cannot be
                      both current authority and preserved history (Huayin, 2026-08-26). It does NOT
                      float: it is pinned to the `recordId` written in the source catalog, forever.
                      A route does NOT exclude it — the preserved DOORWAY PAGE and the preserved
                      PAPER are different texts, and AG v1.1 has both.

    REPAIRED 2026-08-26. This read `corpus["in"]`, a key that left this file when Ask's authority
    manifest was split out of current-corpus.json (commit 06b6ee1). It had raised KeyError on every
    invocation since — so `--check`, the offline gate that reports a deposit gone STALE against the
    registry, has been crashing rather than checking, and the historical class was never modelled
    here at all: AG v1.1's manifest row was written by hand. A gate that cannot run is not a gate,
    and a manifest header that says "do not hand-edit" beside a generator that cannot generate is
    the more expensive half of the defect.
    """
    corpus, sources, records, works = _registry()
    out = []
    historical = [e["sourceId"] for e in corpus["reference"]["entries"]
                  if sources[e["sourceId"]].get("role") == "historical-record"]
    for sid in list(corpus["core"]["sourceIds"]) + historical:
        s = sources[sid]
        preserved = s.get("role") == "historical-record"
        if s.get("route") and not preserved:
            continue  # already readable from the shipped site build
        wid = s.get("workId")
        if not wid:
            continue  # a Core source with neither route nor deposit would be a catalog defect
        rec = record_by_id(records, s["recordId"]) if preserved else current_record(records, wid)
        # recordId and recid ONLY — no doi, no version, no date. Third time this lesson has come up
        # on this branch and it is the same rule every time: a generated file that copies a
        # publication fact becomes a second source of truth for it. The manifest carries the foreign
        # key; the DOI is resolved from records.json wherever it is actually needed. `recid` is kept
        # because it is the Zenodo API address this module must call, not a claim about the work.
        # The LABEL, and why it is not always the work's canonical label. `canonicalLabel` names
        # the work as it is called NOW. A preserved edition is precisely the thing that must not be
        # called what the work is called now — labelling AG v1.1's deposit "Analytical Governance"
        # would make the preserved paper answer to the current name. So a historical-record source
        # is labelled by its own catalog `title`, which is written to say WHICH edition it is.
        label = s["title"] if preserved else works[wid]["canonicalLabel"]
        # `declaredKey` is CARRIED, NOT STORED. fetch() pops it before the manifest is written, so
        # the manifest never restates the catalog's declaration — which is what lets `check()` compare
        # the two and catch a manifest that is perfectly self-consistent and bound to the wrong file.
        out.append({"sourceId": sid, "workId": wid, "label": label,
                    "recordId": rec["recordId"], "recid": str(rec["recid"]),
                    "declaredKey": declared_artifact(s, rec["recordId"])})
    return out


def fetch() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest, missing = [], []
    for t in targets():
        t = dict(t)
        declared = t.pop("declaredKey", None)
        meta = json.loads(_get(f"https://zenodo.org/api/records/{t['recid']}"))
        files = meta.get("files", [])
        # Raises rather than guessing. A SelectionError is not caught here and must not be: an
        # ambiguous record is a thing for a person to declare, not for this run to resolve.
        text, how = select_text(files, declared, source_id=t["sourceId"], record_id=t["recordId"])
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
        got = verify_publisher_checksum(blob, text, what=t["sourceId"])

        # THE COMPANION TEXTS, RECORDED AND NOT STORED. A record may deposit more than one document
        # — ToD v7.1 deposits the foundation and a statistical extension reference under one DOI.
        # Only the selected artifact becomes the work's text on disk, because the storage convention
        # is one file per recordId and a second document would overwrite the first. Their publisher
        # checksums are captured here so the supplement's identity and its link to THIS record are
        # preserved as evidence, without giving it a publication identity it does not have.
        companions = []
        for f in eligible_texts(files):
            if f["key"] == text["key"]:
                continue
            cblob = _get(f["links"]["self"])
            cgot = verify_publisher_checksum(cblob, f, what=f"{t['sourceId']} / {f['key']}")
            companions.append({"key": f["key"], "md5": cgot, "bytes": len(cblob),
                               "sha256": hashlib.sha256(cblob).hexdigest()})
            time.sleep(0.4)

        path = OUT / f"{t['recordId']}.md"
        path.write_bytes(blob)
        row = {**t, "file": path.name, "zenodoKey": text["key"], "selection": how,
               "provenance": "zenodo", "zenodoVerified": True,
               "md5": got, "bytes": len(blob),
               "sha256": hashlib.sha256(blob).hexdigest()}
        if companions:
            row["companions"] = companions
        manifest.append(row)
        print(f"  ok            {t['sourceId']:<32} {len(blob):>7} bytes  {text['key']}  "
              f"[{how}{', +%d companion' % len(companions) if companions else ''}]", flush=True)
        time.sleep(0.4)  # be a polite client

    payload = {
        "$comment": "Generated by ask/ingest_deposits.py. Do not hand-edit. Every entry is pinned "
                    "to the record the publication registry rules CURRENT; re-run after a "
                    "registry change and the diff shows which edition moved.",
        "deposits": manifest,
        "missingText": missing,
    }
    MANIFEST.write_text(json.dumps(payload, indent=1) + "\n")
    return payload


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# VALIDATING THE BINDING, NOT ONLY THE BYTES (Huayin, ruling of 2026-09-07).
#
# The manifest records WHICH artifact was stored and proves the bytes have not moved since. It cannot
# say why that artifact was the right one — the reasons live in the source catalog and in the record
# — so a manifest that names the statistical supplement as the work is internally perfect and
# externally wrong. Byte integrity and binding correctness are different claims and are checked apart.
#
# HERMETIC, LIKE EVERY OTHER GATE HERE. This reads the COMMITTED declaration (sources.json) and the
# FROZEN evidence captured at ingest (`selection`, `companions`) — never the network. A gate that
# asked Zenodo what the record contains would fail on someone else's outage and pass on their cache.
def _check_binding(d: dict, sources: dict) -> int:
    """Does the manifest row agree with the catalog declaration and the evidence of the record?"""
    if d.get("provenance") != "zenodo":
        # PROVENANCE IS NOT A COURTESY LABEL. `supplied` bytes are checksum-pinned locally and are
        # NOT verified against the publisher; saying otherwise would launder the difference the
        # supplied path exists to keep visible.
        if d.get("zenodoVerified"):
            print(f"  MISLABELLED   {d['sourceId']} is provenance {d.get('provenance')!r} but claims "
                  f"zenodoVerified — only a publisher-checksum match earns that")
            return 1
        return 0
    if not d.get("zenodoVerified") or not d.get("md5"):
        print(f"  UNVERIFIED    {d['sourceId']} is provenance 'zenodo' without a matched publisher "
              f"checksum. A locally computed sha256 is not publisher verification")
        return 1

    src = sources.get(d["sourceId"], {})
    declared = declared_artifact(src, d["recordId"])
    key = d.get("zenodoKey")
    companion_keys = [c["key"] for c in d.get("companions") or []]

    if key in companion_keys:
        print(f"  INCOHERENT    {d['sourceId']} names {key} as both the selected artifact and a "
              f"companion")
        return 1

    if declared is not None:
        if key != declared:
            print(f"  MISBOUND      {d['sourceId']} stored {key!r} for record {d['recordId']}, but "
                  f"the source catalog declares {declared!r}. The bytes may be intact and still be "
                  f"the wrong document")
            return 1
        if d.get("selection") != "declared":
            print(f"  UNDECLARED    {d['sourceId']} matches its declaration but records selection "
                  f"{d.get('selection')!r} — the manifest must say the choice was declared")
            return 1
        return 0

    if companion_keys:
        print(f"  AMBIGUOUS     {d['sourceId']} record {d['recordId']} deposits more than one text "
              f"({[key] + companion_keys}) and the source catalog declares none. Re-running the "
              f"ingest will refuse; declare the artifact that is the work")
        return 1
    if d.get("selection") not in (None, "sole-text"):
        print(f"  UNDECLARED    {d['sourceId']} records selection {d.get('selection')!r} with no "
              f"declaration in the source catalog")
        return 1
    return 0


def _check_declarations(sources: dict, records: list[dict]) -> int:
    """A declaration must name a record the registry actually has. A selector that outlives its
    record reads as coverage and selects nothing."""
    known = {r["recordId"] for r in records}
    bad = 0
    for sid, s in sorted(sources.items()):
        for rid in sorted((s.get("artifacts") or {})):
            if rid not in known:
                print(f"  ORPHAN DECL   {sid} declares an artifact for {rid}, which is not a record "
                      f"in registry/publications/records.json")
                bad += 1
    return bad


def check() -> int:
    """Offline: verify stored files still match the manifest, and that it matches the registry."""
    if not MANIFEST.exists():
        print("no deposit manifest — run `python3 -m ask.ingest_deposits` first")
        return 1
    m = json.loads(MANIFEST.read_text())
    _, sources, records, _ = _registry()
    want = {t["sourceId"]: t for t in targets()}
    bad_decl = _check_declarations(sources, records)
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
        if w and w["recordId"] != d["recordId"]:  # pinned targets can never trip this: same source
            print(f"  STALE         {d['sourceId']} is ingested at {d['recordId']} but the registry "
                  f"now rules {w['recordId']} current — re-run the ingest")
            bad += 1
        bad += _check_binding(d, sources)
    covered = {d["sourceId"] for d in m["deposits"]} | {x["sourceId"] for x in m["missingText"]}
    for sid in want:
        if sid not in covered:
            print(f"  UNINGESTED    {sid} is a ruled deposit target but absent from the manifest")
            bad += 1
    bad += bad_decl
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


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# THE REGRESSIONS — HERMETIC, AND RIDING THE GATE THAT ALREADY EXISTS.
#
# No network and no registry: every fixture is a literal below. They ride `deposit-corpus` rather
# than getting a job of their own, for the reason the publication gate's `--selftest` rides its own
# job — a fixture nobody runs is not a fixture.
#
# The case that matters most is the FIRST one. Reversing the two-file response is the exact
# perturbation the old `next(...)` rule could not survive, and it is the reason this code exists.
FOUNDATION = {"key": "the_theory_of_data_v7_1_zenodo_22649945.md",
              "checksum": "md5:2679d8d7dfb943a39e37abc2788c12a9", "size": 140001}
SUPPLEMENT = {"key": "the_theory_of_data_v7_1_statistical_extension_reference_22649945.md",
              "checksum": "md5:0450fd63830dd117b2dede239c176cb3", "size": 10511}
PDF = {"key": "the_theory_of_data_v7_1_zenodo_22649945.pdf", "checksum": "md5:8fe7d251", "size": 237448}
LONE = {"key": "theory_of_data_v6_1.md", "checksum": "md5:8cc8cefd8fa2d83786012bc19d8e518c", "size": 96625}


def selftest() -> int:
    results: list[tuple[bool, str]] = []

    def ok(cond: bool, label: str) -> None:
        results.append((bool(cond), label))

    def quietly(fn):
        """Run a check that is SUPPOSED to report, capturing what it says. The diagnostics of a
        deliberate negative are evidence, not output — printing them into a gate log makes a passing
        selftest read like a failing one. The captured text is asserted on, so the fixture pins the
        REASON and not merely the exit count."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = fn()
        return rc, buf.getvalue()

    def refuses(fn, label: str) -> None:
        try:
            fn()
        except SelectionError:
            ok(True, label)
        except Exception as exc:  # noqa: BLE001 — a WRONG refusal is still a failure
            ok(False, f"{label}  [raised {type(exc).__name__}, expected SelectionError]")
        else:
            ok(False, f"{label}  [did not refuse]")

    R7 = "w-theory-of-data.r07"
    R8 = "w-theory-of-data.r08"
    src = {"sourceId": "s-theory-of-data", "artifacts": {R8: FOUNDATION["key"]}}

    # 1 · REVERSING THE TWO-FILE RESPONSE STILL SELECTS THE FOUNDATION. The defect, pinned.
    forward = [PDF, FOUNDATION, SUPPLEMENT]
    reversed_ = list(reversed(forward))
    a, how_a = select_text(forward, FOUNDATION["key"], source_id="s", record_id=R8)
    b, how_b = select_text(reversed_, FOUNDATION["key"], source_id="s", record_id=R8)
    ok(a["key"] == b["key"] == FOUNDATION["key"] and how_a == how_b == "declared",
       "reversing the two-file response still selects the foundation")
    ok(select_text([SUPPLEMENT, FOUNDATION], SUPPLEMENT["key"], source_id="s",
                   record_id=R8)[0]["key"] == SUPPLEMENT["key"],
       "...and a declaration selects the supplement when the supplement is what is declared")

    # 2 · AN UNCONFIGURED MULTI-TEXT RECORD REFUSES — and does NOT reach the supplied path.
    refuses(lambda: select_text([PDF, FOUNDATION, SUPPLEMENT], None, source_id="s", record_id=R8),
            "an unconfigured multi-text record refuses")

    # 3 · A MISSING DECLARED KEY REFUSES EVEN WHEN ANOTHER TEXT IS AVAILABLE.
    refuses(lambda: select_text([PDF, SUPPLEMENT], FOUNDATION["key"], source_id="s", record_id=R8),
            "a missing declared key refuses even when another text is available")
    refuses(lambda: select_text([PDF], FOUNDATION["key"], source_id="s", record_id=R8),
            "...and refuses rather than falling through to the supplied path when no text exists")

    # 4 · A SELF-CONSISTENT MANIFEST FOR THE WRONG SUPPLEMENT IS REJECTED.
    wrong = {"sourceId": "s-theory-of-data", "recordId": R8, "provenance": "zenodo",
             "zenodoVerified": True, "md5": "0450fd63830dd117b2dede239c176cb3",
             "zenodoKey": SUPPLEMENT["key"], "selection": "declared",
             "companions": [{"key": FOUNDATION["key"], "md5": "2679d8d7dfb943a39e37abc2788c12a9"}]}
    rc, said = quietly(lambda: _check_binding(wrong, {"s-theory-of-data": src}))
    ok(rc == 1 and "MISBOUND" in said,
       "a self-consistent manifest bound to the wrong supplement is rejected")
    right = dict(wrong, zenodoKey=FOUNDATION["key"],
                 companions=[{"key": SUPPLEMENT["key"], "md5": "0450fd63830dd117b2dede239c176cb3"}])
    ok(_check_binding(right, {"s-theory-of-data": src}) == 0,
       "...and the correctly bound manifest passes")

    rc, said = quietly(lambda: _check_binding(dict(right, selection="sole-text"),
                                              {"s-theory-of-data": {}}))
    ok(rc == 1 and "AMBIGUOUS" in said,
       "...and a manifest whose record has companions but no declaration is rejected")

    # 5 · A CHANGED SUCCESSOR RECORD DOES NOT SILENTLY INHERIT AN OLD SELECTOR.
    stale = {"sourceId": "s-theory-of-data", "artifacts": {R7: FOUNDATION["key"]}}
    ok(declared_artifact(stale, R8) is None,
       "a selector declared for one edition is not inherited by its successor")
    refuses(lambda: select_text([FOUNDATION, SUPPLEMENT], declared_artifact(stale, R8),
                                source_id="s", record_id=R8),
            "...so the successor's ambiguity refuses instead of resolving by inheritance")
    rc, said = quietly(lambda: _check_declarations({"s": {"artifacts": {R8: FOUNDATION["key"]}}},
                                                   [{"recordId": R7}]))
    ok(rc == 1 and "ORPHAN DECL" in said,
       "a declaration naming no registry record is reported")

    # 6 · EXISTING UNAMBIGUOUS SINGLE-TEXT AND HISTORICAL-EDITION CASES SURVIVE.
    sole, how = select_text([PDF, LONE], None, source_id="s", record_id="w-x.r01")
    ok(sole["key"] == LONE["key"] and how == "sole-text",
       "an unambiguous single-text record still selects it, undeclared")
    ok(select_text([PDF], None, source_id="s", record_id="w-x.r01") == (None, "no-text"),
       "a PDF-only record still yields to the supplied path")
    ok(_check_binding({"sourceId": "s", "recordId": "w-x.r01", "provenance": "zenodo",
                       "zenodoVerified": True, "md5": "x", "zenodoKey": LONE["key"],
                       "selection": "sole-text"}, {"s": {}}) == 0,
       "a historical/pinned single-text row validates with no declaration")
    ok(_check_binding({"sourceId": "s", "recordId": "w-x.r01", "provenance": "supplied",
                       "zenodoVerified": False}, {"s": {}}) == 0,
       "an author-supplied row is exempt from artifact binding and stays unverified")
    rc, said = quietly(lambda: _check_binding({"sourceId": "s", "recordId": "w-x.r01",
                                               "provenance": "supplied", "zenodoVerified": True},
                                              {"s": {}}))
    ok(rc == 1 and "MISLABELLED" in said,
       "...and a supplied row claiming zenodoVerified is rejected")

    # 7 · CHECKSUM CORRUPTION FAILS.
    good = b"the deposited bytes"
    meta = {"key": "x.md", "checksum": "md5:" + hashlib.md5(good).hexdigest()}
    ok(verify_publisher_checksum(good, meta, what="x") == hashlib.md5(good).hexdigest(),
       "an intact download matches the publisher checksum")
    try:
        verify_publisher_checksum(good + b"!", meta, what="x")
        ok(False, "checksum corruption fails  [did not raise]")
    except ChecksumError:
        ok(True, "checksum corruption fails")
    try:
        verify_publisher_checksum(good, {"key": "x.md"}, what="x")
        ok(False, "a record with no published checksum refuses  [did not raise]")
    except ChecksumError:
        ok(True, "a record with no published checksum refuses")

    for good_, label in results:
        print(f"  {'PASS' if good_ else 'FAIL'}  {label}")
    failed = [l for g, l in results if not g]
    if failed:
        print(f"\nSELFTEST FAILED — {len(failed)} of {len(results)}")
        return 1
    print(f"\nOK — {len(results)} artifact-selection fixtures hold (declared beats order; ambiguity "
          f"refuses; a wrong binding is caught even when the bytes are perfect).")
    return 0


if __name__ == "__main__":
    # THE WRITE PATH IS THE BARE INVOCATION, AND ONLY THAT. `--selftest` must never fall through to
    # fetch(): the fixtures are hermetic and a flag that reads as "run the tests" silently reaching
    # the network and rewriting the corpus is exactly the kind of surprise this module exists to
    # refuse. Found the first time --selftest was run alone, which is the cheapest possible way to
    # find it.
    if "--selftest" in sys.argv:
        rc = selftest()
        if rc or "--check" not in sys.argv:
            sys.exit(rc)
    if "--check" in sys.argv:
        sys.exit(check())
    out = fetch()
    print(f"\ningested {len(out['deposits'])}; {len(out['missingText'])} have no text deposit")
    for x in out["missingText"]:
        print(f"  · {x['label']} — deposited as {x['deposited']} only (record {x['recordId']})")

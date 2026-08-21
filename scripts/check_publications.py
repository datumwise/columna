#!/usr/bin/env python3
"""
check_publications.py — THE PUBLICATION REGISTRY GATE.

The registry only helps if it is the ONLY place a publication fact can come from. This is the guard
that makes that true, and it fails closed, naming its reason.

WHAT IT IS FOR. Before the registry, the site simultaneously claimed The Theory of Data was at v3.1
(/about), at v1.0 (llms.txt), and at v4.0 (the current framework manual), while Zenodo had served v6.1
since 2026-08-19; every page footer cited The Two Anchors of a Measure v1.0 ten days after v2.0 was
deposited. None of those were typos. Each was a fact that had to be re-typed to stay true, in a place
whose surrounding comments read as maintained. This gate removes the possibility of that class rather
than the instances of it.

THE TEN GATES

  G1  works        — ids unique; required fields; every work carries an `attachedConcepts` list; no
                     concept is attached by two works
  G2  records      — ids unique; every record's work exists; EXACTLY ONE current record per work
  G3  supersession — edges stay inside a work, are acyclic, and the chain from the current record
                     covers every record of that work (no orphaned deposits). Edges MAY cross attached
                     concepts — see the attachment note below
  G4  concept      — record.conceptRecid ∈ work.attachedConceptRecids; each attachment exists in the
                     snapshot, carries Zenodo's own conceptDoi, and is witnessed by at least one record
  G5  snapshot     — every bibliographic field equals the frozen Zenodo evidence, and every version
                     Zenodo knows about is modeled (no silently dropped versions)
  G6  identity     — no internal id embeds a DOI or a recid. Internal reference integrity may never
                     depend on parsing a DOI string
  G7  echo audit   — every Zenodo token in every tracked file is accounted for by consumers.json:
                     derived surfaces carry NONE, everything else carries only what it is allowed
  G8  reconciliation — known discrepancies are live, scoped, and not silently outlived
  G9  acceptance   — the four rulings of 2026-08-21, asserted as facts about the encoded registry
  G10 counts       — no count-of-publications claim may appear on a derived surface while the corpus
                     classification is ungoverned

ONE WORK MAY ATTACH MANY ZENODO CONCEPTS (Huayin, ruling of 2026-08-21, Phase 3B.1).

    A datumwise Work is the governed intellectual identity. A Zenodo concept is an ATTACHED EXTERNAL
    PUBLICATION IDENTITY — one of possibly several a work acquires over its publication history.

Two deposits in this corpus proved the single-concept model wrong, and neither is an error anyone
made in this repo. The Silent Failure Atlas was deposited as v1.2 under concept 20710592 and, three
days later, as v1.3 under a NEW concept 20762838 rather than as a new version of the first. And The
Two Great Sources of Silent Analytical Failure acquired a retitled successor — Three Structural
Sources, v2.0 — deposited under its own concept while declaring, in its own Zenodo metadata,
`isNewVersionOf` the earlier record. Both are ordinary things to do at a deposit provider. Under the
old model the first was unrepresentable and the second would have left a superseded record rendering
as current on /about and llms.txt.

So attachment is 1..n, and the consequences are deliberate and narrow:

  • CURRENTNESS STILL COMES FROM GOVERNED STATUS, and from nothing else. Not from concept, not from
    attachment order, not from version string, date, or DOI magnitude. A work has exactly one record
    with status `current` (G2) and that is the whole of the rule.
  • SUPERSESSION MAY CROSS ATTACHED CONCEPTS inside one work. `w-two-great-sources`'s current record
    supersedes a record in a different concept, and that is now a sentence the registry can say.
  • ATTACHMENT IS MANY-TO-ONE. A concept attaches to at most one work (G1). Relax that and "which
    work does this deposit belong to?" stops having an answer.
  • ATTACHMENT IS A SET (Phase 3B.2). The list is persisted in first-deposit order because a human
    reads the file, but no gate may consult position: the same identities in either order are the
    same governed meaning. `--selftest` pins that, and pins that membership, absence and duplication
    still bite.
  • THE WORK'S LOCAL IDENTITY DOES NOT MOVE. `w-two-great-sources` keeps its workId although its
    current deposit is titled *Three Structural Sources*. The slug is a mnemonic; no code reads it,
    and renaming it to match a title would make internal identity track external naming — the exact
    coupling this registry exists to break.

WHY G9 IS HERE AND NOT IN A TEST FILE. The rulings are what the registry is FOR. "current record =
v6.1; v6.1 supersedes v6.0; v6.0 remains historical; no current view may accidentally select v6.0" is
not an implementation detail that a unit test happens to cover — it is the acceptance condition, and
it belongs beside the thing it accepts.

WHAT IT DELIBERATELY DOES NOT DO. It does not decide whether a citation is semantically appropriate.
An edition-pinned page citing its own deposited edition and a stale page citing a superseded record
look identical to a scanner. The decidable layer is enforced here; the rest is a human review gate,
and pretending otherwise would manufacture false confidence (Slice 2 ledger §0).

Usage:
    python scripts/check_publications.py            # hermetic: registry vs frozen snapshot
    python scripts/check_publications.py --live     # additionally re-verify against Zenodo
    python scripts/check_publications.py --report    # print the inventory, then check
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "registry" / "publications"
SNAPSHOT = REG / "zenodo_snapshot_2026-08-21.json"

# TWO SPELLINGS OF ONE ECHO (widened 2026-08-21, on a blind spot the AG v1.1 supersession found).
#
# The audit originally read only the DOI form, `zenodo.<id>`. A ratified architecture checkpoint had
# been citing three records as "Zenodo 21958062" — bare prose, no DOI — for two days, entirely
# invisible to the gate. It happened to be correct (an edition-pinned Sources line), which is the
# unsettling part: the gate would have been equally silent had it been wrong. A scanner that reads one
# spelling of an identifier does not audit identifiers, it audits a spelling.
#
# Both forms normalize to `10.5281/zenodo.<id>` before anything compares them.
DOI_TOKEN_RE = re.compile(r"zenodo\.(\d{6,10})")
PROSE_TOKEN_RE = re.compile(r"[Zz]enodo[ :]+(\d{6,9})")
# A count claim on a derived surface: a number word or digit immediately governing "papers" /
# "publications". Deliberately narrow — this gate refuses magic numbers, it does not police prose.
COUNT_RE = re.compile(
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\s+"
    r"(?:published\s+)?(?:papers|publications)\b",
    re.IGNORECASE,
)

FAILURES: list[str] = []
NOTES: list[str] = []


def fail(gate: str, msg: str) -> None:
    FAILURES.append(f"[{gate}] {msg}")


def note(msg: str) -> None:
    NOTES.append(msg)


def load(name: str):
    path = REG / name
    if not path.exists():
        raise SystemExit(f"publication registry: {path} is missing. Nothing to check, so nothing passes.")
    return json.loads(path.read_text(encoding="utf-8"))


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--", ".", ":(exclude)apps/website/dist", ":(exclude)registry"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [line for line in out.splitlines() if line]


def scan_tokens() -> dict[str, set[str]]:
    """Every Zenodo record reference in every tracked file, in either spelling, as `10.5281/zenodo.<id>`."""
    per: dict[str, set[str]] = {}
    patterns = [
        (r"zenodo\.[0-9]{6,10}", DOI_TOKEN_RE),        # the DOI form
        (r"[Zz]enodo[ :]+[0-9]{6,9}", PROSE_TOKEN_RE),  # the prose form: "Zenodo 21958062"
    ]
    for grep_pattern, extract in patterns:
        listing = subprocess.run(
            ["git", "grep", "-n", "-o", "-E", grep_pattern, "--",
             ".", ":(exclude)apps/website/dist", ":(exclude)registry"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout
        for line in listing.splitlines():
            path, _lineno, raw = line.split(":", 2)
            m = extract.search(raw)
            if m:
                per.setdefault(path, set()).add("10.5281/zenodo." + m.group(1))
    return per


# ──────────────────────────────────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# ATTACHMENT IS A SET. SERIALIZATION ORDER CARRIES NO LAW. (Huayin, ruling of 2026-08-21, Phase 3B.2.)
#
# `attachedConcepts` is persisted as a JSON array in first-deposit order, because a file a human reads
# wants a stable order and that one is meaningful to read. It is not meaningful to a GATE. Nothing in
# the model consults position: currentness is governed `status`, supersession is by recordId, and
# membership is membership.
#
# THE DEFECT THIS CLOSES. Three G9 acceptance assertions compared the array as an ORDERED LIST, so a
# byte-different-but-semantically-identical serialization — the same concepts, written the other way
# round — failed a gate for a reason the model says does not exist. A test that rejects a legal state
# is not a strict test, it is a wrong one, and it teaches the next person that order is load-bearing.
#
# Both helpers are pure and take plain data, which is what lets --selftest exercise them on fixtures
# instead of on the live registry. See selftest() at the bottom of this file.


def attached_recids(work: dict | None) -> set[str]:
    """The concept identities a work attaches, as a SET. Order-blind by construction."""
    return {c["recid"] for c in (work or {}).get("attachedConcepts", []) if c.get("recid")}


def duplicate_attachments(work: dict | None) -> list[str]:
    """Concept ids listed more than once on one work. A set comparison cannot see these — G1 must."""
    seen: set[str] = set()
    dupes: list[str] = []
    for att in (work or {}).get("attachedConcepts", []):
        recid = att.get("recid")
        if not recid:
            continue
        if recid in seen and recid not in dupes:
            dupes.append(recid)
        seen.add(recid)
    return dupes


def _shippable(path: pathlib.Path) -> str:
    """
    A derived surface's source, minus the parts that never reach a reader.

    G10 forbids a publication COUNT on a derived surface. It reads source, not built output, so it
    would otherwise fire on the comments that explain why the count was removed — and a guard that
    punishes documenting its own reason teaches people to stop documenting. Line and block comments
    are stripped from .ts/.astro/.js sources before the scan.

    KNOWN LIMIT, STATED RATHER THAN HIDDEN: this is a lexer's job done with a regex, so a `//` inside
    a string literal will over-strip. The consequence is a MISSED count, never a false one — the gate
    can under-report here, and the only real defence against a hand-typed count on a derived surface
    is that a derived surface has no business hand-typing anything. G7 is the load-bearing half.
    """
    text = path.read_text(encoding="utf-8")
    if path.suffix not in (".ts", ".tsx", ".js", ".mjs", ".astro"):
        return text
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    text = re.sub(r"(?m)^\s*//.*$", "", text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="also re-verify the snapshot against Zenodo")
    ap.add_argument("--report", action="store_true", help="print the inventory before checking")
    ap.add_argument("--selftest", action="store_true",
                    help="run the attachment set-semantics fixtures (hermetic; no registry, no network)")
    args = ap.parse_args()

    if args.selftest and selftest() != 0:
        return 1

    works = load("works.json")
    records = load("records.json")
    consumers = load("consumers.json")
    reconciliation = load("reconciliation.json")
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    snap_records = snapshot["records"]
    snap_concepts = snapshot["concepts"]

    by_work = {w["workId"]: w for w in works}
    by_record = {r["recordId"]: r for r in records}
    records_of: dict[str, list[dict]] = {}
    for r in records:
        records_of.setdefault(r["workId"], []).append(r)

    # ── G1 · works ────────────────────────────────────────────────────────────────────────────────
    if len(by_work) != len(works):
        fail("G1", "duplicate workId in works.json")
    concept_owner: dict[str, str] = {}
    for w in works:
        for field in ("workId", "canonicalLabel", "kind"):
            if not w.get(field):
                fail("G1", f"work {w.get('workId')!r} is missing required field {field!r}")
        if "attachedConcepts" not in w:
            fail("G1", f"work {w.get('workId')!r} has no `attachedConcepts` list. A work with no deposits "
                       "carries an EMPTY list, not a missing field: 'never deposited' is a fact this "
                       "registry states, not one it leaves to inference.")
            continue
        for concept in duplicate_attachments(w):
            fail("G1", f"work {w['workId']} attaches concept {concept} twice. Attachment is a set; "
                       "a repeated entry is either a paste or a claim nobody meant to make. G9 compares "
                       "attachment as a set and CANNOT see this — catching it is G1's job, and stays G1's job.")
        for att in w["attachedConcepts"]:
            concept = att.get("recid")
            if not concept or not att.get("doi"):
                fail("G1", f"work {w['workId']}: an attached concept is missing recid or doi ({att!r})")
                continue
            # ATTACHMENT IS MANY-TO-ONE, NEVER MANY-TO-MANY (Huayin, Phase 3B.1). A work may attach
            # several concepts; a concept may be attached by ONE work. Relax this and "which work does
            # this deposit belong to?" stops having an answer, which is the question the registry exists
            # to answer. If a genuine shared-concept case ever appears, it stops here and is reported.
            if concept in concept_owner:
                fail("G1", f"concept {concept} is attached by two works: {concept_owner[concept]} and "
                           f"{w['workId']}. One Zenodo concept attaches to at most ONE datumwise work. A work "
                           "may hold several concepts; a concept may not be split across works.")
            concept_owner[concept] = w["workId"]
        if not records_of.get(w["workId"]):
            note(f"work {w['workId']} has no deposited record — legal (a work need never be deposited), reported for visibility")

    # ── G2 · records ──────────────────────────────────────────────────────────────────────────────
    if len(by_record) != len(records):
        fail("G2", "duplicate recordId in records.json")
    for r in records:
        if r["workId"] not in by_work:
            fail("G2", f"record {r['recordId']} names work {r['workId']!r}, which does not exist")
        if r["status"] not in ("current", "superseded"):
            fail("G2", f"record {r['recordId']} has status {r['status']!r}; expected current|superseded")
    for wid, rs in records_of.items():
        current = [r for r in rs if r["status"] == "current"]
        if len(current) != 1:
            fail("G2", f"work {wid} has {len(current)} current records, expected exactly 1 "
                       f"({', '.join(r['recordId'] for r in current) or 'none'}). A current view cannot be "
                       "resolved deterministically until this is exactly one.")

    # ── G3 · supersession ─────────────────────────────────────────────────────────────────────────
    for wid, rs in records_of.items():
        ids = {r["recordId"] for r in rs}
        for r in rs:
            sup = r.get("supersedes")
            if sup is None:
                continue
            if sup not in by_record:
                fail("G3", f"record {r['recordId']} supersedes {sup!r}, which does not exist")
            elif sup not in ids:
                fail("G3", f"record {r['recordId']} supersedes {sup}, which belongs to work "
                           f"{by_record[sup]['workId']}, not {wid}. Supersession is within a work; across "
                           "works it would be a relationship, not version identity.")
        current = [r for r in rs if r["status"] == "current"]
        if len(current) != 1:
            continue
        seen, cursor, guard = [], current[0], 0
        while cursor is not None:
            guard += 1
            if guard > len(rs) + 1:
                fail("G3", f"work {wid} has a cycle in its supersession chain")
                break
            seen.append(cursor["recordId"])
            nxt = cursor.get("supersedes")
            cursor = by_record.get(nxt) if nxt else None
        missing = ids - set(seen)
        if missing:
            fail("G3", f"work {wid}: records {sorted(missing)} are not reachable from the current record "
                       "by following `supersedes`. An unreachable deposit is one no view will ever show and "
                       "no history will ever mention.")

    # ── G4/G5 · concept identity and snapshot conformance ─────────────────────────────────────────
    modeled_recids = set()
    for r in records:
        recid = r["recid"]
        modeled_recids.add(recid)
        snap = snap_records.get(recid)
        if snap is None:
            fail("G5", f"record {r['recordId']} (recid {recid}) is absent from the Zenodo snapshot. "
                       "Every bibliographic fact in this registry must be evidenced; re-run "
                       "scripts/harvest_zenodo_snapshot.py.")
            continue
        w = by_work.get(r["workId"], {})
        attached = {c["recid"] for c in w.get("attachedConcepts", []) if c.get("recid")}
        if attached and snap["conceptRecid"] not in attached:
            fail("G4", f"record {r['recordId']} belongs to Zenodo concept {snap['conceptRecid']}, which its work "
                       f"{r['workId']} does not attach (attached: {sorted(attached)}). THE INVARIANT: "
                       "record.conceptRecid ∈ work.attachedConceptRecids. A record whose concept the work never "
                       "attached is a deposit filed under a work on somebody's say-so.")
        for ours, theirs in (("title", "title"), ("version", "version"), ("date", "publicationDate"),
                             ("doi", "doi"), ("license", "license"), ("resourceType", "resourceType")):
            if r.get(ours) != snap.get(theirs):
                fail("G5", f"record {r['recordId']}.{ours} = {r.get(ours)!r} but Zenodo says "
                           f"{snap.get(theirs)!r}. The registry does not get to disagree with the record.")
        if r.get("authors") != snap.get("authors"):
            fail("G5", f"record {r['recordId']}.authors = {r.get('authors')!r} but Zenodo says {snap.get('authors')!r}")

    recids_of_work: dict[str, set[str]] = {}
    for r in records:
        recids_of_work.setdefault(r["workId"], set()).add(r["recid"])
    for w in works:
        for att in w.get("attachedConcepts", []):
            concept = att.get("recid")
            if not concept:
                continue
            known = snap_concepts.get(concept)
            if known is None:
                fail("G4", f"work {w['workId']} attaches concept {concept}, absent from the snapshot")
                continue
            if att.get("doi") != known.get("conceptDoi"):
                fail("G4", f"work {w['workId']} attaches concept {concept} with conceptDoi {att.get('doi')!r}, "
                           f"but Zenodo says {known.get('conceptDoi')!r}. An attached identity is EXTERNAL "
                           "evidence and does not get to be approximately right.")
            # AN ATTACHMENT MUST BE WITNESSED. Attaching a concept is a claim that this work was
            # deposited there; if no record of the work carries it, the claim has no evidence and the
            # attachment is decoration. It would also silently widen G4 for every future record.
            if not (set(known["versions"]) & recids_of_work.get(w["workId"], set())):
                fail("G4", f"work {w['workId']} attaches concept {concept}, but not one of its records belongs "
                           "to that concept. An attachment nothing witnesses is a claim without evidence.")
            missing = set(known["versions"]) - modeled_recids
            if missing:
                fail("G5", f"work {w['workId']}: Zenodo knows versions {sorted(missing)} of concept {concept} "
                           "that the registry does not model. A version the registry cannot see is a version no "
                           "view can ever cite and no supersession chain can ever reach.")

    # ── G6 · internal identity never encodes external identity ────────────────────────────────────
    for w in works:
        if re.search(r"\d{6,}", w["workId"]) or "10.5281" in w["workId"]:
            fail("G6", f"workId {w['workId']!r} embeds what looks like a Zenodo id or DOI. Internal identity "
                       "is minted locally and permanently; a later deposit ATTACHES a concept identity to an "
                       "existing work, it does not name it.")
    for r in records:
        rid = r["recordId"]
        if "10.5281" in rid or re.search(r"\d{6,}", rid):
            fail("G6", f"recordId {rid!r} embeds a DOI or recid. Internal reference integrity must not depend "
                       "on parsing DOI strings.")
        if r.get("supersedes") and "10.5281" in str(r["supersedes"]):
            fail("G6", f"record {rid}.supersedes points at a DOI, not a recordId")

    # ── G7 · the echo audit ───────────────────────────────────────────────────────────────────────
    occurrences = scan_tokens()
    by_path = {c["path"]: c for c in consumers}
    if len(by_path) != len(consumers):
        fail("G7", "duplicate path in consumers.json")

    known_dois = {r["doi"] for r in records}
    rc_tokens_for: dict[str, set[str]] = {}
    for item in reconciliation:
        for pattern in item.get("allowedContexts", []):
            rc_tokens_for.setdefault(pattern, set()).update(item.get("tokens", []))

    def reconciliation_allows(path: str, token: str) -> bool:
        for pattern, tokens in rc_tokens_for.items():
            if pattern == "*" or fnmatch.fnmatch(path, pattern) or path == pattern:
                if "*" in tokens or token in tokens:
                    return True
        return False

    all_tracked = set(tracked_files())
    for c in consumers:
        if c["path"] not in all_tracked:
            fail("G7", f"consumers.json lists {c['path']}, which is not a tracked file. A ledger row that "
                       "outlives its subject is worse than no row: it reads as coverage.")

    for path, tokens in sorted(occurrences.items()):
        entry = by_path.get(path)
        if entry is None:
            fail("G7", f"{path} carries Zenodo publication tokens {sorted(tokens)} but is not classified in "
                       "registry/publications/consumers.json. FAILING CLOSED: a new hand-authored publication "
                       "fact must be declared as derived, frozen, edition-pinned, historical or owed — it may "
                       "not simply appear.")
            continue
        if entry["class"] == "derived":
            fail("G7", f"{path} is classified `derived` but carries literal Zenodo tokens {sorted(tokens)}. "
                       "A derived surface reads the registry; the moment it also types a DOI, it is a "
                       "second source of truth wearing the clothes of the first.")
            continue
        allowed = set(entry.get("allowedDois", []))
        for token in sorted(tokens):
            if token in allowed or reconciliation_allows(path, token):
                continue
            fail("G7", f"{path} carries {token}, which its consumers.json row does not allow. Either the fact "
                       "changed (update the row, deliberately) or a publication fact was hand-typed into a "
                       "surface that had stopped doing that.")
        for token in sorted(allowed):
            if token not in tokens:
                fail("G7", f"consumers.json allows {token} in {path}, but it no longer appears there. Stale "
                           "permission: it grants cover to a fact nobody is asserting.")
            if token not in known_dois and not reconciliation_allows(path, token):
                fail("G7", f"consumers.json allows {token} in {path}, but no record in the registry has that "
                           "DOI and no reconciliation item covers it. An unregistered DOI is either a typo or "
                           "a publication this registry has never heard of.")

    for c in consumers:
        if c["class"] == "derived" and c.get("allowedDois"):
            fail("G7", f"{c['path']} is `derived` and yet declares allowedDois. Derived means none.")
        if c["path"] not in occurrences and c["class"] != "derived":
            fail("G7", f"{c['path']} is classified `{c['class']}` but carries no Zenodo token at all. Remove "
                       "the row or explain it; a classification of nothing classifies nothing.")

    # ── G8 · reconciliation items must be live and scoped ─────────────────────────────────────────
    for item in reconciliation:
        for field in ("id", "tokens", "disposition", "allowedContexts", "reason", "provenance"):
            if field not in item:
                fail("G8", f"reconciliation item {item.get('id')!r} is missing required field {field!r}")
        matched = False
        for pattern in item.get("allowedContexts", []):
            if pattern == "*":
                matched = True
                break
            if any(fnmatch.fnmatch(p, pattern) or p == pattern for p in all_tracked):
                matched = True
        if not matched:
            fail("G8", f"reconciliation item {item['id']}: none of its allowedContexts match a tracked file. "
                       "The discrepancy it tolerates no longer exists, or the paths moved. Either way this row "
                       "is now fiction.")
        for pattern in item.get("forbiddenContexts", []):
            if pattern == "derived":
                continue
            for path, tokens in occurrences.items():
                if (fnmatch.fnmatch(path, pattern) or path == pattern) and tokens & set(item["tokens"]):
                    fail("G8", f"reconciliation item {item['id']} forbids its tokens in {pattern}, but {path} "
                               f"carries {sorted(tokens & set(item['tokens']))}.")

    # ── G9 · the rulings of 2026-08-21, asserted ──────────────────────────────────────────────────
    def current_of(wid: str):
        rs = [r for r in records_of.get(wid, []) if r["status"] == "current"]
        return rs[0] if len(rs) == 1 else None

    tod = current_of("w-theory-of-data")
    if not tod or tod["doi"] != "10.5281/zenodo.22013410" or tod["version"] != "6.1":
        fail("G9", f"ruling 5: the current record of The Theory of Data must be v6.1 / 22013410; got "
                   f"{tod and (tod['version'], tod['doi'])}")
    else:
        prev = by_record.get(tod.get("supersedes") or "")
        if not prev or prev["doi"] != "10.5281/zenodo.21958062" or prev["version"] != "6.0":
            fail("G9", "ruling 5: v6.1 must supersede v6.0 (21958062) by recordId")
        elif prev["status"] != "superseded":
            fail("G9", "ruling 5: v6.0 must remain historically addressable with status `superseded`")

    primer = current_of("w-tod-primer")
    if not primer or primer["doi"] != "10.5281/zenodo.22018549" or primer["version"] != "2.2":
        fail("G9", f"ruling 4: the current Primer record must be v2.2 / 22018549; got "
                   f"{primer and (primer['version'], primer['doi'])}")
    v20 = [r for r in records_of.get("w-tod-primer", []) if r["doi"] == "10.5281/zenodo.21959668"]
    if len(v20) != 1 or v20[0]["status"] != "superseded" or v20[0]["version"] != "2.0":
        fail("G9", "ruling 4: Primer v2.0 (21959668) must be a superseded record of the SAME work as v2.2")

    triangle = {
        "w-tod-primer": "21842993",
        "w-tod-primer-applied": "21960379",
        "w-tod-applied": "21959940",
    }
    for wid, concept in triangle.items():
        w = by_work.get(wid)
        if not w:
            fail("G9", f"ruling 4: work {wid} is missing from the registry")
        elif attached_recids(w) != {concept}:
            fail("G9", f"ruling 4: {wid} must attach exactly the one concept {concept}; got "
                       f"{sorted(attached_recids(w))}")
    tri_records = {r["recordId"] for wid in triangle for r in records_of.get(wid, [])}
    for wid in triangle:
        for r in records_of.get(wid, []):
            sup = r.get("supersedes")
            if sup and by_record.get(sup, {}).get("workId") != wid:
                fail("G9", f"ruling 4: {r['recordId']} supersedes a record outside its own work. There is NO "
                           "supersession edge among the three Primer/Applied works; their cross-references are "
                           "relationships, not version identity.")

    op = current_of("w-open-planner")
    if not op or op["doi"] != "10.5281/zenodo.21695710" or op["version"] != "1.3":
        fail("G9", f"ruling 1: the current Open Planner record must be v1.3 / 21695710; got "
                   f"{op and (op['version'], op['doi'])}")
    v10 = [r for r in records_of.get("w-open-planner", []) if r["doi"] == "10.5281/zenodo.21632723"]
    if len(v10) != 1 or v10[0]["version"] != "1.0":
        fail("G9", "ruling 1: 21632723 must be modeled as Open Planner v1.0 — the frozen deposit's claim that "
                   "it is v1.3 is tolerated in that file and must never become the registry's belief")

    # The registry's FIRST POST-PHASE-1 SUPERSESSION EVENT (Huayin, 2026-08-21). Pinned here rather
    # than trusted to the mint rule, because "latest deposit wins" is what PRODUCES this answer and an
    # acceptance test that re-derives its expectation from the rule under test asserts nothing.
    ag = current_of("w-analytical-governance")
    if not ag or ag["doi"] != "10.5281/zenodo.22046037" or ag["version"] != "1.1":
        fail("G9", f"AG v1.1: the current Analytical Governance record must be v1.1 / 22046037; got "
                   f"{ag and (ag['version'], ag['doi'])}")
    else:
        prev = by_record.get(ag.get("supersedes") or "")
        if not prev or prev["doi"] != "10.5281/zenodo.21959749" or prev["version"] != "1.0":
            fail("G9", "AG v1.1: v1.1 must supersede v1.0 (21959749) by recordId, not by DOI or by date")
        elif prev["status"] != "superseded":
            fail("G9", "AG v1.1: v1.0 must remain a first-class historical record with status `superseded` — "
                       "superseded is a status, not a deletion")

    # ── THE PHASE 3B.1 RULINGS, ASSERTED (Huayin, 2026-08-21) ────────────────────────────────
    # Pinned here, not left to the mint rule, for the reason G9 exists at all: an acceptance test that
    # re-derives its expectation from the rule under test asserts nothing.

    # Case 1 — one work, two attached concepts, one chain across them.
    atlas = by_work.get("w-silent-failure-atlas")
    if attached_recids(atlas) != {"20710592", "20762838"}:
        fail("G9", f"3B.1 case 1: the Atlas must attach exactly the concepts 20710592 and 20762838, in any "
                   f"serialization order; got {sorted(attached_recids(atlas))}")
    atlas_cur = current_of("w-silent-failure-atlas")
    if not atlas_cur or atlas_cur["doi"] != "10.5281/zenodo.20762839" or atlas_cur["version"] != "1.3":
        fail("G9", f"3B.1 case 1: the current Atlas record must be v1.3 / 20762839; got "
                   f"{atlas_cur and (atlas_cur['version'], atlas_cur['doi'])}")
    else:
        prev = by_record.get(atlas_cur.get("supersedes") or "")
        if not prev or prev["recid"] != "20710593" or prev["version"] != "1.2":
            fail("G9", "3B.1 case 1: v1.3 must supersede v1.2 (20710593) — the deposit in the OTHER attached "
                       "concept. A concept break is not a work break.")
        elif prev["status"] != "superseded":
            fail("G9", "3B.1 case 1: Atlas v1.2 must remain a first-class historical record, status `superseded`")
        elif snap_records.get(prev["recid"], {}).get("conceptRecid") == \
                snap_records.get(atlas_cur["recid"], {}).get("conceptRecid"):
            fail("G9", "3B.1 case 1: this edge is supposed to CROSS concepts. If both records now sit in one "
                       "concept, either the snapshot changed or the case this ruling was made for is gone.")

    # Case 2 — a retitled successor across a concept boundary; the local workId does NOT follow the title.
    tgs = by_work.get("w-two-great-sources")
    if not tgs:
        fail("G9", "3B.1 case 2: workId w-two-great-sources must be PRESERVED. The public title changed; "
                   "local identity does not track external naming, and renaming it would be the coupling "
                   "this registry exists to break.")
    else:
        if attached_recids(tgs) != {"21553378", "21893928"}:
            fail("G9", f"3B.1 case 2: w-two-great-sources must attach exactly 21553378 and 21893928, in any "
                       f"serialization order; got {sorted(attached_recids(tgs))}")
        cur = current_of("w-two-great-sources")
        if not cur or cur["doi"] != "10.5281/zenodo.21893929" or cur["version"] != "2.0":
            fail("G9", f"3B.1 case 2: the current record must be v2.0 / 21893929; got "
                       f"{cur and (cur['version'], cur['doi'])}")
        elif cur["title"] != "Three Structural Sources of Silent Analytical Failure":
            fail("G9", f"3B.1 case 2: the current record's title is the EXACT deposited one, "
                       f"'Three Structural Sources of Silent Analytical Failure'; got {cur['title']!r}. "
                       "The Phase 3B.1 brief quoted a subtitle ('Anchor, Universe, and Regime') that the "
                       "deposit does not carry. Zenodo is the bibliographic authority, not the brief.")
        else:
            prev = by_record.get(cur.get("supersedes") or "")
            if not prev or prev["doi"] != "10.5281/zenodo.21553379":
                fail("G9", "3B.1 case 2: v2.0 must supersede the Two Great Sources deposit (21553379) by "
                           "recordId, across the concept boundary")
            elif prev["status"] != "superseded":
                fail("G9", "3B.1 case 2: 21553379 must remain first-class and historical, status `superseded` — "
                           "it is retired as CURRENT AUTHORITY, not retired")

    # Case 3 — the two clean identities claimed by the same unit.
    for wid, doi, ver in (("w-frameql-primer", "10.5281/zenodo.21960873", "2.0"),
                          ("w-data-has-its-own-ontology", "10.5281/zenodo.22026962", "1.1")):
        cur = current_of(wid)
        if not cur or cur["doi"] != doi or cur["version"] != ver:
            fail("G9", f"3B.1 case 3: the current record of {wid} must be v{ver} / {doi.rsplit('.', 1)[1]}; "
                       f"got {cur and (cur['version'], cur['doi'])}")

    anchors = current_of("w-two-anchors")
    if not anchors or anchors["version"] != "2.0":
        fail("G9", f"ruling 7: the current Two Anchors record must be v2.0; got {anchors and anchors['version']}")

    # ── G10 · no count while the classification is ungoverned ─────────────────────────────────────
    unclassified = [w["workId"] for w in works if w["kind"] == "unclassified"]
    if unclassified:
        for c in consumers:
            if c["class"] != "derived":
                continue
            path = ROOT / c["path"]
            if not path.exists():
                continue
            hit = COUNT_RE.search(_shippable(path))
            if hit:
                fail("G10", f"{c['path']} states a publication count ({hit.group(0)!r}) while "
                            f"{len(unclassified)} works are `kind: unclassified`. Records, works, papers, "
                            "primers, positions and program notes are not the same counting unit; no governed "
                            "definition says which the word ranges over. Drop the claim or govern the "
                            "classification — do not replace a stale magic number with a fresh one.")
        note(f"counts are NOT derivable: {len(unclassified)} of {len(works)} works are `kind: unclassified`. "
             "This is deliberate at Phase 1A and is what keeps a recomputed count off the site.")

    # ── optional live re-verification ─────────────────────────────────────────────────────────────
    if args.live:
        import urllib.request
        for r in records:
            url = f"https://zenodo.org/api/records/{r['recid']}"
            try:
                with urllib.request.urlopen(url, timeout=30) as resp:
                    live = json.load(resp)
            except Exception as exc:  # noqa: BLE001
                fail("LIVE", f"{r['recordId']}: {url} unreachable ({exc})")
                continue
            m = live["metadata"]
            if m.get("title") != r["title"] or m.get("version") != r["version"] or live.get("doi") != r["doi"]:
                fail("LIVE", f"{r['recordId']} has drifted from Zenodo: registry "
                             f"{(r['version'], r['title'][:40], r['doi'])} vs live "
                             f"{(m.get('version'), (m.get('title') or '')[:40], live.get('doi'))}")
        note(f"live re-verification: {len(records)} records fetched from Zenodo")

    # ── report ────────────────────────────────────────────────────────────────────────────────────
    if args.report:
        print(f"{len(works)} works · {len(records)} records · {len(consumers)} classified consumers · "
              f"{len(reconciliation)} reconciliation items\n")
        for w in sorted(works, key=lambda w: w["workId"]):
            cur = current_of(w["workId"])
            n = len(records_of.get(w["workId"], []))
            ver = f"v{cur['version']}" if cur and cur["version"] else "(unversioned)"
            print(f"  {w['workId']:<38} {ver:<8} {cur['doi'] if cur else '—':<28} "
                  f"{n} record{'s' if n != 1 else ''}  "
                  f"concept{'s' if len(w.get('attachedConcepts', [])) != 1 else ''} "
                  f"{'+'.join(c['recid'] for c in w.get('attachedConcepts', [])) or '—'}")
        print()
        buckets: dict[str, int] = {}
        for c in consumers:
            buckets[c["class"]] = buckets.get(c["class"], 0) + 1
        print("  consumers by class: " + ", ".join(f"{k}={v}" for k, v in sorted(buckets.items())))
        print()

    for n in NOTES:
        print(f"note: {n}")
    if FAILURES:
        print(f"\nPUBLICATION REGISTRY GATE FAILED — {len(FAILURES)} finding(s):\n", file=sys.stderr)
        for f in FAILURES:
            print(f"  {f}\n", file=sys.stderr)
        return 1
    print(f"\npublication registry OK — {len(works)} works, {len(records)} records, "
          f"{len(consumers)} classified consumers, {len(reconciliation)} reconciliation items.")
    return 0


# ──────────────────────────────────────────────────────────────────────────────────────────────────


def selftest() -> int:
    """
    THE FIXTURE FOR SET SEMANTICS (Phase 3B.2).

    It runs on two-letter fake concept ids, NOT on the live registry, and that is the point: an
    assertion about `["A", "B"]` versus `["B", "A"]` is about the comparison, and checking it against
    real data would make it pass or fail for reasons that have nothing to do with ordering.

    What it pins, in one sentence each:
      • the same identities in either order are the same governed meaning;
      • a missing one, or an extra one, still fails — set semantics is not laxity;
      • a duplicate is INVISIBLE here and belongs to G1, which is asserted rather than assumed.
    """
    def work(*recids):
        return {"workId": "w-fixture", "attachedConcepts": [{"recid": r, "doi": f"10.5281/zenodo.{r}"}
                                                            for r in recids]}

    cases: list[tuple[str, bool]] = []

    def expect(label: str, actual, wanted) -> None:
        cases.append((label, actual == wanted))

    expected = {"A", "B"}

    # THE RULING, ASSERTED BOTH WAYS ROUND.
    expect("['A','B'] attaches {A,B}", attached_recids(work("A", "B")) == expected, True)
    expect("['B','A'] attaches {A,B}", attached_recids(work("B", "A")) == expected, True)
    expect("['A','B'] and ['B','A'] are the same attachment",
           attached_recids(work("A", "B")) == attached_recids(work("B", "A")), True)

    # ORDER-INSENSITIVE IS NOT LENIENT.
    expect("missing concept still fails", attached_recids(work("A")) == expected, False)
    expect("extra concept still fails", attached_recids(work("A", "B", "C")) == expected, False)
    expect("empty attachment still fails", attached_recids(work()) == expected, False)
    expect("a work with no attachment list at all is empty, not an error here",
           attached_recids({"workId": "w-never-deposited"}), set())

    # DUPLICATES: G9 CANNOT SEE THEM, G1 MUST. Both halves are asserted, because the first half is
    # exactly the property that would make someone think set semantics had lost a check.
    expect("a duplicate is invisible to the set comparison",
           attached_recids(work("A", "A", "B")) == expected, True)
    expect("...and is caught by the duplicate helper G1 uses",
           duplicate_attachments(work("A", "A", "B")), ["A"])
    expect("no false duplicate on a clean work", duplicate_attachments(work("A", "B")), [])

    failed = [label for label, ok in cases if not ok]
    for label, ok in cases:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if failed:
        print(f"\nSELFTEST FAILED — {len(failed)} of {len(cases)}", file=sys.stderr)
        return 1
    print(f"\nOK — {len(cases)} attachment-semantics fixtures hold "
          "(serialization order carries no law; membership, absence and duplication all still do).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
mint_publication_records.py — how a new deposit ENTERS the registry.

THE INVARIANT THIS FILE PROTECTS (Huayin, ruling 2 of 2026-08-21):

    A later deposit ATTACHES an external concept identity to an existing datumwise work.
    It does not change the work's internal identity.

So this script mints, it does not renumber. A recordId, once minted, is permanent — records are
matched to the snapshot by Zenodo recid, never by position, version string or date, so a new version
appearing in the middle of a family (Zenodo permits it) appends a new id and disturbs nothing. There
is no pre-deposit → post-deposit identity migration, because there is no identity to migrate: the
work already had one.

WHAT IT WRITES, AND WHAT A HUMAN STILL OWES. It refreshes every bibliographic field from the frozen
snapshot (title, version, date, DOI, authors, licence, resource type — all record-level, because all
of them can differ between versions of one work, and in this corpus they demonstrably do), mints ids
for versions not yet modeled, and recomputes `status` and `supersedes` in publication order.

IT PROPOSES CURRENCY; IT DOES NOT RATIFY IT. "Latest deposit is the current record" is a rule, not a
law: an erratum, a withdrawn version, or a deposit made in the wrong order would each make it wrong.
So every status change is PRINTED LOUDLY and lands as bytes in a diff, where a person approves it. So
is every bibliographic field that moves — a deposited title, date or DOI changing under a recid is
either a correction made at the deposit or a harvest against the wrong record, and both deserve a
line rather than a silent rewrite.
The registry is machine-maintained and human-ratified, in that order.

New works are NOT invented here. A concept the snapshot knows and works.json does not is reported and
refused: naming a work — deciding that these deposits are one intellectual object, and what to call it
— is the one genuinely editorial act in this system. That refusal now covers ATTACHMENT too: deciding
that a second Zenodo concept belongs to an existing work is the same editorial act wearing a different
hat, and a script that guessed it from a title string would be inventing publication history.

Usage:
    python scripts/mint_publication_records.py --dry-run
    python scripts/mint_publication_records.py
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "registry" / "publications"
SNAPSHOT = REG / "zenodo_snapshot_2026-08-28.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    works = json.loads((REG / "works.json").read_text(encoding="utf-8"))
    records = json.loads((REG / "records.json").read_text(encoding="utf-8"))

    snap_records = snapshot["records"]
    snap_concepts = snapshot["concepts"]
    by_concept = {c["recid"]: w for w in works for c in w.get("attachedConcepts", [])}
    existing = {r["recid"]: r for r in records}

    unknown = sorted(set(snap_concepts) - set(by_concept))
    if unknown:
        for concept in unknown:
            titles = {snap_records[v]["title"] for v in snap_concepts[concept]["versions"]}
            print(f"REFUSING: Zenodo concept {concept} is not claimed by any work — {sorted(titles)[0]!r}",
                  file=sys.stderr)
        print("\nA new WORK is not minted automatically. Deciding that a set of deposits is one\n"
              "intellectual object, and what the corpus calls it, is editorial. Add it to works.json\n"
              "with a locally minted workId, then re-run.", file=sys.stderr)
        return 1

    out: list[dict] = []
    minted: list[str] = []
    changed: list[str] = []
    # BIBLIOGRAPHIC DRIFT IS ALSO A REPORT, not only a diff (2026-08-26).
    #
    # This script refreshes title, version, date, doi, authors, licence and resourceType from the
    # snapshot on every run, and until today it printed NOTHING when one of them moved — a run that
    # rewrote a deposited title said "nothing to mint; registry already matches the snapshot". That
    # sentence was false in the one register that matters: the registry did NOT match the snapshot,
    # which is exactly what G5 asserts. Found while correcting the Analytical Governance v2.0 title
    # after the deposit itself was corrected at Zenodo. Currency was printed loudly; a title
    # correction, which changes what every derived surface renders, was silent.
    fields: list[str] = []

    for w in sorted(works, key=lambda w: w["workId"]):
        concepts = [c["recid"] for c in w.get("attachedConcepts", [])]
        if not concepts:
            continue
        # ONE CHAIN ACROSS EVERY ATTACHED CONCEPT (Huayin, ruling of 2026-08-21, Phase 3B.1).
        #
        # A work's deposits are pooled from all of its attached concepts and ordered ONCE, by
        # publication date. Attachment order does not order the chain and neither does concept
        # membership: The Silent Failure Atlas was deposited as v1.2 under one concept and v1.3 under
        # another, three days apart, and the chain that results is v1.2 -> v1.3 like any other. That
        # is the whole content of "a concept is an attached external identity, not the work".
        #
        # A single-concept work is the same computation with one concept in the pool, so no existing
        # work's chain, ids or currency move on this change — verified against the pre-migration
        # records.json byte for byte, except where a second concept was deliberately attached.
        versions = sorted((v for c in concepts for v in snap_concepts[c]["versions"]),
                          key=lambda r: (snap_records[r]["publicationDate"], int(r)))
        used = {r["recordId"] for r in records if r["workId"] == w["workId"]}
        seq = max((int(rid.rsplit(".r", 1)[1]) for rid in used), default=0)

        prev_id = None
        for recid in versions:
            snap = snap_records[recid]
            prior = existing.get(recid)
            if prior is None:
                seq += 1
                record_id = f"{w['workId']}.r{seq:02d}"
                minted.append(f"{record_id}  ({snap['title'][:52]}  v{snap['version']}  {snap['doi']})")
            else:
                record_id = prior["recordId"]

            record = {
                "recordId": record_id,
                "workId": w["workId"],
                "title": snap["title"],
                "version": snap["version"],
                "date": snap["publicationDate"],
                "doi": snap["doi"],
                "recid": recid,
                "status": "current" if recid == versions[-1] else "superseded",
                "authors": snap["authors"],
                "license": snap["license"],
                "resourceType": snap["resourceType"],
            }
            if prev_id:
                record["supersedes"] = prev_id
            for f in ("title", "version", "date", "doi", "authors", "license", "resourceType"):
                if prior and prior.get(f) != record[f]:
                    fields.append(f"{record_id}.{f}: {prior.get(f)!r} -> {record[f]!r}")
            if prior and prior.get("status") != record["status"]:
                changed.append(f"{record_id}: status {prior.get('status')} -> {record['status']}  "
                               f"(v{record['version']}, {record['doi']})")
            out.append(record)
            prev_id = record_id

    orphans = sorted(set(existing) - {r["recid"] for r in out})
    for recid in orphans:
        print(f"WARNING: record {existing[recid]['recordId']} (recid {recid}) is in the registry but not "
              f"in the snapshot. It is DROPPED by this run — re-harvest before trusting that.", file=sys.stderr)

    for line in minted:
        print(f"MINTED   {line}")
    for line in fields:
        print(f"FIELD    {line}")
    for line in changed:
        print(f"CURRENCY {line}")
    if fields:
        print("\n^ A BIBLIOGRAPHIC FIELD MOVED. The snapshot is the evidence and the registry is being\n"
              "  brought to it — but a deposited title, date or DOI changing is either a correction at\n"
              "  the deposit or a harvest against the wrong record. Read the snapshot diff before\n"
              "  merging, the same way currency changes are read.")
    if changed:
        print("\n^ CURRENCY CHANGES ARE PROPOSALS. 'Latest deposit is current' is a rule, not a law —\n"
              "  an erratum or an out-of-order deposit breaks it. Read the diff before merging.")
    if not minted and not changed and not fields:
        print("nothing to mint; registry already matches the snapshot")

    if not args.dry_run:
        (REG / "records.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nwrote registry/publications/records.json — {len(out)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

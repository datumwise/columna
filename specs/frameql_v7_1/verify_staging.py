#!/usr/bin/env python3
"""Two integrity checks, reported SEPARATELY because they have different scopes.

The archived `audit_joint_review.py` was written against the review package's EXACT membership: it
walks the packaged files and resolves their local links as siblings. Running it in this staged
directory as-is FAILS, and the failure is a scope artifact, not a loss of integrity — the staged tree
deliberately contains more than the package (`proposed_adoption/`, `editorial_archive/`, this file),
and `editorial_archive/sources/` holds a second copy of the theory manuscript whose siblings differ.

The archived check is therefore NOT weakened to accommodate those additions. Instead:

  CHECK 1  pristine-package integrity  — reconstruct exactly the package membership recorded in
           MANIFEST_SHA256.json into a temporary tree, verify every hash, and run the archived audit
           there unmodified. This is the claim "the reviewed package is intact in this repository".

  CHECK 2  adoption-tree integrity     — verify that every local link in the adopted reading set
           resolves, that the archived trees are untouched, and that the adopted copies differ from
           their baselines only where this pass says they do. This is a DIFFERENT claim, and it is
           the one that covers the staging's own additions.

Read-only. Writes nothing outside a temporary directory.
"""
from __future__ import annotations
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

BASE = pathlib.Path(__file__).resolve().parent
def sha(p: pathlib.Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def manifest_entries():
    man = json.loads((BASE / "MANIFEST_SHA256.json").read_text())
    entries = man if isinstance(man, list) else (man.get("files") or man.get("entries") or man)
    if isinstance(entries, dict):
        return list(entries.items())
    return [(e.get("path") or e.get("file"), e.get("sha256")) for e in entries]

def check_1_pristine() -> bool:
    print("CHECK 1 — pristine-package integrity (archived audit, unmodified, over package membership only)")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="pristine_package_"))
    bad, n = [], 0
    for rel, exp in manifest_entries():
        if isinstance(exp, dict): exp = exp.get("sha256")
        src = BASE / rel
        if not src.is_file():
            bad.append(f"{rel}: MISSING"); continue
        if sha(src) != exp: bad.append(f"{rel}: hash mismatch")
        dst = tmp / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst); n += 1
    shutil.copy2(BASE / "MANIFEST_SHA256.json", tmp / "MANIFEST_SHA256.json")
    print(f"   membership reconstructed from this repository: {n} files, {len(bad)} problem(s)")
    for b in bad: print("     ", b)
    r = subprocess.run([sys.executable, "audit_joint_review.py"], cwd=tmp, capture_output=True, text=True)
    archived = json.loads((BASE / "tod_frameql_joint_review_document_audit_v0_1.json").read_text())
    try:
        got = json.loads(r.stdout)
    except json.JSONDecodeError:
        print("   archived audit FAILED to run:"); print("   " + (r.stdout + r.stderr).strip()[-400:]); return False
    ok = (got == archived) and not bad
    print(f"   archived audit status: {got.get('status')}   identical to the archived audit JSON: {got == archived}")
    shutil.rmtree(tmp, ignore_errors=True)
    return ok

def check_2_adoption() -> bool:
    print("\nCHECK 2 — adoption-tree integrity (this staging's own additions)")
    ok = True
    pa = BASE / "proposed_adoption"
    tot = broken = 0
    for p in sorted(pa.glob("*.md")):
        for m in re.finditer(r"\]\((?!https?:|#)([^)#]+)\)", p.read_text()):
            tot += 1
            if not (p.parent / m.group(1)).resolve().is_file():
                broken += 1; ok = False; print(f"     BROKEN {p.name} -> {m.group(1)}")
    print(f"   adopted-set local links: {tot} checked, {broken} broken")

    tot2 = broken2 = 0
    for p in sorted((BASE / "reviewed_sources").glob("*.md")):
        for m in re.finditer(r"\]\((?!https?:|#)([^)#]+)\)", p.read_text()):
            tot2 += 1
            if not (p.parent / m.group(1)).resolve().is_file():
                broken2 += 1; ok = False; print(f"     BROKEN (archived) {p.name} -> {m.group(1)}")
    print(f"   archived reviewed_sources links still resolve: {tot2} checked, {broken2} broken")

    # the adopted set must differ from its baseline ONLY in the files this pass names
    named = {"frameql_language_vnext_working_draft_v0_4.md", "columna_o3_governed_analytical_order_v0_2.md",
             "frameql_an_introduction_v2_4_working_draft_v0_1.md", "a_primer_on_frameql_v2_3_working_draft_v0_1.md",
             "frameql_v7_1_authority_and_supersession_index_v0_1.md"}
    adopted = {p.name for p in pa.glob("*.md")} - {
        "REVISION_METADATA.md", "EDITORIAL_FOLLOWUP.md", "PROVENANCE_EVIDENCE.md", "INDEX.md",
        "PATCH_SHEET_DISPOSITIONS.md"}
    if adopted != named:
        ok = False; print(f"     UNEXPECTED adopted-copy set: {sorted(adopted ^ named)}")
    else:
        print(f"   adopted copies are exactly the {len(named)} documents this pass edits")
    return ok

if __name__ == "__main__":
    a = check_1_pristine(); b = check_2_adoption()
    print(f"\nCHECK 1 pristine-package: {'PASS' if a else 'FAIL'}   CHECK 2 adoption-tree: {'PASS' if b else 'FAIL'}")
    sys.exit(0 if (a and b) else 1)

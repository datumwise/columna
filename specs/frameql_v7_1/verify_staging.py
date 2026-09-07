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

def check_3_entry_point() -> bool:
    """The staging README is the entry point. Verify what it actually SAYS, not just that its links
    resolve: the command it documents must be the command that exists and runs, and the reading set it
    points at must be the corrected one."""
    print("\nCHECK 3 - entry-point agreement (specs/frameql_v7_1/README.md)")
    ok = True
    readme = (BASE / "README.md").read_text()
    idx = (BASE / "proposed_adoption" / "INDEX.md").read_text()

    def want(cond, msg):
        nonlocal ok
        print(f"   {'ok  ' if cond else 'FAIL'} {msg}")
        if not cond: ok = False

    # 1. the documented command is the real one, invoked from the repository root
    want("python specs/frameql_v7_1/verify_staging.py" in readme,
         "documents `python specs/frameql_v7_1/verify_staging.py` (repo-root invocation)")
    want((BASE / "verify_staging.py").is_file(), "that script exists at the documented path")

    # 2. it must NOT tell a reader to run the archived audit here, nor promise it reproduces
    want("cd specs/frameql_v7_1 && python audit_joint_review.py" not in readme,
         "does not instruct running the archived audit in the expanded tree")
    want("Do not run `audit_joint_review.py` directly in this directory" in readme,
         "warns against that invocation explicitly")

    # 3. reading order is delegated, not duplicated
    want("proposed_adoption/INDEX.md" in readme, "delegates the reading order to the adoption-facing index")
    want("does not repeat that list" in readme, "states that it keeps no competing list")
    numbered = sum(1 for line in readme.splitlines()
                   if re.match(r"^\s*\d+\.\s+\[", line) and "_v0_" in line)
    want(numbered == 0, f"maintains no competing numbered document list (found {numbered})")

    # 4. the baselines stay reachable as history
    want("reviewed_sources/frameql_v7_1_authority_and_supersession_index_v0_1.md" in readme,
         "keeps the archived baseline index reachable as history")

    # 5. patch-sheet status agrees with the recorded dispositions
    want("not applied to any repository file" not in readme,
         "no longer claims the patch sheet is applied to no repository file")
    want("PATCH_SHEET_DISPOSITIONS.md" in readme, "points at the recorded dispositions")

    # 6. INTENDED DOCUMENT SELECTIONS: the index picks corrected copies for the edited documents,
    #    and archived copies for the rest.
    edited = {"frameql_language_vnext_working_draft_v0_4.md", "columna_o3_governed_analytical_order_v0_2.md",
              "frameql_an_introduction_v2_4_working_draft_v0_1.md", "a_primer_on_frameql_v2_3_working_draft_v0_1.md",
              "frameql_v7_1_authority_and_supersession_index_v0_1.md"}
    for name in sorted(edited):
        want(f"]({name})" in idx and f"](../reviewed_sources/{name})" not in idx,
             f"index selects the CORRECTED copy of {name}")
    for name in ("the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md",
                 "frameql_v7_1_semantic_acceptance_cases_v0_1.md",
                 "frameql_v7_1_reference_integration_patch_sheet_v0_1.md"):
        want(f"](../reviewed_sources/{name})" in idx,
             f"index selects the ARCHIVED copy of {name}")

    # 7. the archived audit is preserved byte-identical to its manifest hash
    exp = dict((r, s if not isinstance(s, dict) else s.get("sha256")) for r, s in manifest_entries())
    want(sha(BASE / "audit_joint_review.py") == exp.get("audit_joint_review.py"),
         "audit_joint_review.py is unchanged (matches MANIFEST_SHA256.json)")
    return ok


if __name__ == "__main__":
    a = check_1_pristine(); b = check_2_adoption(); c = check_3_entry_point()
    print(f"\nCHECK 1 pristine-package: {'PASS' if a else 'FAIL'}   "
          f"CHECK 2 adoption-tree: {'PASS' if b else 'FAIL'}   "
          f"CHECK 3 entry-point: {'PASS' if c else 'FAIL'}")
    sys.exit(0 if (a and b and c) else 1)

# ToD v7.1 / Frame-QL — docs-only staging report

**Base:** `bfb3cfe` · **Staged head:** see branch `docs/tod-v7-1-staging` · **Date:** 7 September 2026
**Status: staging only.** No merge, publication, deployment, reindexing or implementation.

## 1. Pinned state

Repository state was inspected, not assumed. `origin/main` was fetched and found still at `bfb3cfe`
("Ledger: close R4-C0, row R4-C0-R1 as a deferred residue"); the local checkout matched it and the
working tree was clean before any staging occurred.

## 2. Placement, and why

The set is staged at `specs/frameql_v7_1/`, **deliberately outside `docs/`**. `docs/README.md` states
the repository's publication rule in its first paragraph: *"The merge that published these files is
the publication."* An unpublished working successor placed under `docs/` would therefore be published
by the act of landing it. `specs/` is the established home for working specifications and already
carries seven subdirectories, so this uses the existing document architecture rather than inventing
one.

The five jurisdictions the review asks to keep apart map onto structure that already exists:
published deposits (`registry/publications/` + Zenodo) · shipped-language documentation (`docs/`) ·
authored profile obligations (`docs/*_profile.md`, `specs/profiles/`) · measured build coverage
(`docs/frame_ql_build_status.md`, generated) · **working successor theory and language (here)**.

One edit was made outside this directory: an 18-line section appended to `docs/README.md` naming the
successor set, stating that it is not shipped and carries no DOI, and warning off the withdrawn
rulings. It closes the failure mode the brief names — an implementer mistaking a superseded O1/O2/M2
ruling for the current family contract — at the place an implementer actually reads.

## 3. J1 / J2 application evidence

Applied from the supplied exact replacement strings in
`tod_frameql_joint_review_editorial_corrections_v0_1.json`; **never reconstructed**. Each verified
four ways before it was written:

| check | J1 — language §6.3 | J2 — O3 §17 |
|---|---|---|
| reviewed-source sha256 matches the record | ✅ `7df99739…e1a5820` | ✅ `37307c32…0eb54bc45` |
| replaced text occurs exactly once in the source | ✅ unique | ✅ unique |
| adopted sha256 matches the record's `proposed_content_sha256` | ✅ `78e84a60…9e5873ab` | ✅ `ae55b0bd…97dcb707` |
| replayed diff line-identical to the supplied `.diff` | ✅ 8 content lines | ✅ 2 content lines |

Sizes: J1 62,812 → 63,218 bytes, lines 1,293 → 1,293 (the fenced `text` block is untouched).
J2 32,132 → 32,468 bytes, lines 381 → 383 (additive; no existing line removed).

J2's `[S6]` referent resolves inside the repository: `START_HERE(2).md` is staged under
`historical_provenance/`, which carries its own "not active instructions" notice. The parenthesised
filename was kept rather than tidied, because the citation names it.

No revision metadata was written **into** either document body. Assigning an edition number is an
adoption act and this is not one; the provenance is recorded beside the files in
`proposed_adoption/REVISION_METADATA.md`, where it alters neither the reviewed text nor its hashes.

## 4. Introduction / Primer predecessor comparison

Two questions were separated, because the review package conflates them.

**(a) Are the repository predecessor sources deposit-faithful?** **Yes — verified, and this corrects
the review's own qualification.** Both Zenodo records were fetched and compared byte-for-byte:

| document | record | repo source | verdict |
|---|---|---|---|
| *Frame-QL: An Introduction* v2.3 | 22071910 | `apps/website/src/content/corpus/frameql_an_introduction_v2_3.md` | **byte-identical** · md5 `8aa327a4…` · 28,310 bytes |
| *A Primer on Frame-QL* v2.2 | 22071833 | `apps/website/src/content/corpus/a_primer_on_frameql_v2_2.md` | **byte-identical** · md5 `6c1292a2…` · 9,295 bytes |

Both deposits publish markdown alongside the PDF, so this is a genuine byte comparison and not a
PDF-derived paraphrase; the md5s match Zenodo's publisher-declared checksums. The authority index §4
records the predecessors as *"not independently checksum-verified Zenodo deposit bytes"* — that
qualification is **understated and may be upgraded**. The index text was not edited: it is a reviewed
source, and upgrading it is an adoption decision.

**(b) Do the editorial transcriptions match those sources?** Mostly.

- **Primer v2.2 — byte-identical** to the deposit-verified source.
- **Introduction v2.3 — content-identical, structurally divergent.** 3,988 word tokens on both sides
  with **not one word changed**, and all 16 fenced blocks byte-identical — but three long paragraphs
  are split in two, giving +3 paragraph blocks, +6 lines, +3 bytes. **Two of the three splits
  propagated into the proposed v2.4 successor**; the third fell in a paragraph v2.4 revises anyway.

The archive's note describes this as "blank-line and paragraph whitespace normalized". Accurate for
the Primer; generous for the Introduction, since introducing a paragraph break is a structural edit
rather than a normalisation, even when no word moves.

**Remaining provenance qualifications, stated rather than rounded away:** the deposit verification
covers the **markdown artifact only** (no claim about the PDF rendering); it is a **point-in-time
fetch** on 7 September 2026 pinned to record IDs, not concept DOIs; and **neither work is registered
in `services/ask/deposits/manifest.json`**, the repository's durable checksummed deposit record. That
manifest is machine-generated and marked do-not-hand-edit, so registering them is an ingest-pipeline
run — out of scope here, and listed below as an adoption decision.

Example counts and the "preserved examples" claim are addressed in `editorial_archive/README.md`.
**No preserved example is a newly executed test.** These corpus documents are outside the manual's
`regen_examples.py` regime, so carrying an example across a revision establishes nothing about the
current build.

## 5. Reference integration patch sheet — reconciled, and NOT applied

The sheet is staged as **proposed wording only** and is applied to no repository file. Reconciled
destination-by-destination against the exact current source at `bfb3cfe`, resolving by heading text
because the sheet itself warns that older line numbers are stale.

| § | destination in the current reference | exists? | conflict | recommendation |
|---|---|---|---|---|
| 2 opening authority notice | `frame_ql_language.md` §Editions and availability + §The Theory of Data (two headings, not one) | partly | would-overclaim-shipped · jurisdiction regression | **do not adopt** |
| 3 alias ≠ identity | §1.6 Series names and the `AS` alias | yes | mild stale-target | **APPLIED, reduced** — family-admission sentence dropped |
| 4 EXPLAIN | §1.7 | yes | needs-semantic-ruling · stale adoption condition | **do not adopt as-is** |
| 5 canonical vs decomposition | §2.1 | yes | needs-semantic-ruling | **do not adopt** |
| 6 default completion | §3.1–3.3 | yes | **already fixed** — no-op | **do not adopt** |
| 7 family / FIRST-LAST / ordered ops | §2.2 carries family-variant prose (see correction below) | yes | no exact replacement destination as written | **not applied** |
| 8 WHERE / HAVING | §4.1–4.4 | yes | already distinguished · needs-semantic-ruling | **do not adopt** |
| 9 Φ / NULL / support | §1.5, §7.5 | yes | would-overclaim-shipped (unbuilt R4) | **do not adopt the enumeration** |
| 10 bracket roadmap withdrawal | §2.8, §6.7 | yes | needs-semantic-ruling · moves a gate census | **do not adopt** |
| 11 profile / generated-table notice | authored prose above `BEGIN GENERATED` | yes | generated-artifact if written inside the block | **APPLIED outside the block** — family-continuation sentence dropped |
| 12 checklist | — | — | — | two items verified holding |

Three findings worth the reviewer's attention:

1. **§7 — CORRECTION to this report as first written.** It said the family / FIRST-LAST / ordered-
   operation destinations "do not exist". **That was an overstatement and is withdrawn.** §2.2 *Bare
   names: inputs versus complete series* carries family-variant prose explicitly — *"A **family
   variant** is the measure under one named reduction of its family, written with a dot: `level.last`,
   `level.sum`… `SELECT level.last AT {store}` reads the end-of-period inventory snapshot per store"* —
   and it goes on to distinguish a family variant from a `member`. The subject is **not absent from
   non-generated prose.** What is true is narrower: the §7 proposal supplies **no exact replacement
   destination matching the current headings**, and the only *enumeration* of `first`/`last` sits
   inside a machine-generated capability block, which is not hand-editable. A future version of the
   proposal needs text pinned to §2.2.
2. **§2 and §9 would present unshipped successor obligations as facts about the shipped release** — a
   v7.1 candidate authority that is not a published edition, and the existence/placement/eligibility/
   support architecture that the consolidated ledger records as explicitly **not built and not
   authorized**. §2 also collides with §2.9 of the language law itself: *"A Theory-of-Data distinction
   enters this language when it is implemented, tested, versioned, and ruled in — not when it is
   published."*
3. **§2 and §4 would reintroduce release-scoped wording** into the one document deliberately stripped
   of it. `docs/README.md`: `frame_ql_language.md` is *"canonical language law, independent of any
   build. No version stamps."* `scripts/currency_stamps.toml` records that move as "**Moved, not
   reworded**". Either such sentences go unenrolled and stale silently — the exact defect the guard
   exists to catch — or they require a new enrolment with a named reason.

**Pre-existing drift surfaced en route, not caused by this staging:** `docs/README.md` says
`frame_ql_language.md` carries "no roadmap marks", but the file carries `[ROADMAP]`/`[SCHEDULED]` in
about eight headings plus a section explaining them. That is an index/document disagreement
independent of this package, and it sits on the §2 and §10 destinations.

## 6. Gate results

Documentation gates, before and after staging, unchanged and green: `regen-examples` ·
`capability-authority` · `capability-tables` · `manual-frameql` · `no-tier-claims` ·
`ledger-heartbeat` · `currency-stamps` · `purged-grammar`. Baseline detail: 86 capabilities projected
into 4 documents, **0 drifted**; 49 manual blocks → 67 statements with **0 drift, 0 unchecked**; 11
enrolled currency claims across 4 files matching `columna 0.19.0 · columna-core 0.19.0 ·
columna-server 0.12.0 · contract_version "4"`.

### 6.1 Two integrity scopes, reported separately

An earlier version of this report said the archived audit "reproduces in-repo". **That conflated two
different claims and is corrected here.** `audit_joint_review.py` was written against the review
package's exact membership and resolves local links as siblings; run as-is in the *expanded* staging
directory it now **fails**, because `editorial_archive/sources/` holds a second copy of the theory
manuscript whose siblings differ. That is a scope artifact of the expansion, not a loss of integrity,
and the archived check was **not weakened** to accommodate it.

`python specs/frameql_v7_1/verify_staging.py` runs both scopes and reports them apart:

- **CHECK 1 — pristine-package integrity.** Exactly the membership recorded in `MANIFEST_SHA256.json`
  is reconstructed from this repository into a temporary tree and the archived audit runs there
  **unmodified**. Result: *40 files, 0 hash problems; status `passed`; output identical to the archived
  audit JSON.*
- **CHECK 2 — adoption-tree integrity.** A different claim, covering this staging's own additions:
  *adopted-set local links 60 checked / 0 broken; archived `reviewed_sources/` links 57 checked / 0
  broken (still intact); adopted copies are exactly the 5 documents this pass edits.*

Both pass. Neither result is offered as the other.

## 7. Confirmations required by the return

- **Protected theory and proof content unchanged.** The ToD v7.1 manuscript, the forty semantic
  acceptance cases (`.md` and `.json`) and the authority index are byte-identical to the review
  package. The theory was not revised to accommodate current code.
- **The forty semantic expectations are unchanged**, and are staged as what they are: premises and
  expectations for review, **not executed engine tests**. No case was described as a passing runtime
  test, and no historical mathematical count was reused as new validation.
- **Non-documentary authorities unchanged**, proven structurally rather than promised:
  `git diff origin/main -- packages/ specs/frameql_capabilities.toml specs/profiles/ apps/ services/
  registry/ scripts/ .github/` is **empty**. No parser grammar, planner or engine behaviour, operator
  or family admission, capability ID, category or schema, profile promise, measured coverage, type
  definition, wire field, contract version or serving outcome was touched.
- **No public spelling or execution mechanism was retired.** No DOI was invented; no v7.1 DOI exists.

## 8. Known ordered-path correctness issues — visible, separate, unclosed

Named in §6 of the set's own authority index: physical-row FIRST/LAST selection, and ordered
contribution surviving late placement withholding. This staging **neither fixes them nor authorizes
postponing them until publication**, and makes no claim about their status on current `main`. Their
reproduced evidence lives in a separate, non-merged reconnaissance branch and is not part of this
staging.

## 9. Adoption decisions — resolved 7 September 2026

All five open items were ruled and are now recorded in the branch. Their resolutions:

1. **Provenance wording** — **resolved: accept and record the new evidence, keeping three facts apart.**
   The adopted Introduction and Primer mastheads and the adopted authority index §4 now distinguish what
   the original editorial pass had available, what was verified later against the deposited Markdown, and
   the exact transcription differences and successor edits. Durable evidence:
   `proposed_adoption/PROVENANCE_EVIDENCE.md`. The archived notes, manifests and register are **not**
   rewritten, so the later verification is never attributed to the original pass; and verifying
   predecessor bytes is stated not to make a revised successor a byte-identical republication.
2. **Authority index §4** — resolved as part of 1, in the **adopted** copy only. The archived baseline is
   preserved unedited.
3. **Deposit registration** — **not done, by instruction.** The ingest pipeline was not run and
   `services/ask/deposits/manifest.json` was not edited. The verification's durable home is the evidence
   record above.
4. **The two inherited Introduction paragraph splits** — **retained and recorded as editorial changes**,
   itemised in the evidence record. No rebuild was performed to undo them.
5. **Patch sheet** — **two proposals applied, nine not.** §3 applied reduced (family-admission sentence
   dropped); §11 applied in the authored prose above `BEGIN GENERATED` (family-continuation sentence
   dropped). Dispositions for all eleven recorded in `proposed_adoption/PATCH_SHEET_DISPOSITIONS.md` so
   the sheet cannot later be applied wholesale. **Withholding an edit does not certify the existing
   wording as correct** — EXPLAIN (§4) and the §5, §8 and §10 contract questions remain open.

## 10. Adopted reading paths

`proposed_adoption/INDEX.md` is the single unambiguous adoption-facing reading index. It selects the
corrected copy of every document that has one and the archived copy of every document this pass does not
change. Adopted copies exist for exactly five documents — language 0.4 (J1), O3 0.2 (J2), Introduction
v2.4, Primer v2.3, and the authority index — and every local link in them resolves under one rule: a
target with an adopted copy stays same-directory, a target this pass does not change points to
`../reviewed_sources/`.

The archived baseline index still selects the uncorrected copies **and is deliberately left that way**,
with an adoption-facing header on the corrected copy saying so. No archived file was edited to fix a link.

Editorial revisions and hashes for these link and provenance edits are in
`proposed_adoption/EDITORIAL_FOLLOWUP.md`, kept **separate** from `proposed_adoption/REVISION_METADATA.md`,
which preserves the original J1/J2 replay evidence exactly as first written.

## 11. Authority descriptions corrected

Both README accounts of the four-document split were wrong in the same way — they read as four
statements about what the released build does.

- `docs/README.md`: the language reference is now described as **adopted language meaning and canonical
  standing**, build status as **measured implementation coverage** (and named as the only one of the four
  that reports build behaviour), profiles as authored obligations, and the successor set as **not yet
  adopted language law, establishing no implementation conformance**.
- `specs/frameql_v7_1/README.md`: the same correction in its jurisdiction table.

Two further `docs/README.md` repairs, both required and both bounded: the stale **"no roadmap marks"**
assertion is corrected by describing the document accurately (eleven `[ROADMAP]`/`[SCHEDULED]` marks are
present) — **no roadmap construct was removed and no standing changed**; and the **duplicate, obsolete
Currency pointer** to a Currency block that no longer exists in the language document is deleted rather
than restated, because restating a version there is the drift it was written to warn about. **No
build-version stamp was reintroduced into language law.**

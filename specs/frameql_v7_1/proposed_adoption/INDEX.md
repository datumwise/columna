# Adoption-facing reading index — the one unambiguous path

**This is the reading index to use.** It selects the corrected copy of every document that has one,
and the archived copy of every document this pass does not change. Status is unchanged by it: the set
is a **working successor** — not adopted language law, not a publication, and not evidence of
implementation conformance.

There are two other indexes in this directory tree and neither is this one:

- `../reviewed_sources/frameql_v7_1_authority_and_supersession_index_v0_1.md` — the **archived
  baseline**, preserved unedited. It selects the *uncorrected* copies and its links are same-directory
  by construction. Read it to see what was reviewed, not to read the adopted set.
- `../START_HERE.md` — the review package's own entry point, also archived unedited.

## Read in this order

| # | Document | Copy used | Why |
|---|---|---|---|
| 1 | ToD v7.1 Full Manuscript Draft 0.4 | [archived](../reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md) | unchanged by this pass; the theory, its four propositions and their proofs are not edited |
| 2 | Frame-QL Language-Law Candidate 0.4 | [**corrected**](frameql_language_vnext_working_draft_v0_4.md) | J1 applied; links repointed |
| 3 | Supporting Contract Notes 0.1 | [archived](../reviewed_sources/frameql_v7_1_supporting_contract_notes_v0_1.md) | unchanged |
| 4 | O3 Order Interface 0.2 | [**corrected**](columna_o3_governed_analytical_order_v0_2.md) | J2 applied; links repointed |
| 5 | Semantic Acceptance Cases 0.1 | [archived](../reviewed_sources/frameql_v7_1_semantic_acceptance_cases_v0_1.md) · [json](../reviewed_sources/frameql_v7_1_semantic_acceptance_cases_v0_1.json) | unchanged — **premises and expectations for review, not executed engine tests** |
| 6 | Capability / Profile Plan 0.2 | [archived](../reviewed_sources/frameql_vnext_capability_profile_reconciliation_plan_v0_2.md) | unchanged; no registry, promise or measurement altered |
| 7 | Release-reference integration patch sheet | [archived](../reviewed_sources/frameql_v7_1_reference_integration_patch_sheet_v0_1.md) | unchanged — **proposed wording. Two items are authorized; nine are not. See [DISPOSITIONS](PATCH_SHEET_DISPOSITIONS.md) before applying anything from it.** |
| 8 | **Frame-QL: An Introduction v2.4 — PUBLISHED** | [**published edition**](https://doi.org/10.5281/zenodo.22661455) · onsite: [/learn/frameql-an-introduction](https://datumwise.ai/learn/frameql-an-introduction) | deposited 8 September 2026. It **supersedes** the working draft this row used to select. The reviewed draft is retained unedited as evidence: [draft 0.1](frameql_an_introduction_v2_4_working_draft_v0_1.md) |
| 9 | **A Primer on Frame-QL v2.3 — PUBLISHED** | [**published edition**](https://doi.org/10.5281/zenodo.22661076) · onsite: [/learn/frameql-primer](https://datumwise.ai/learn/frameql-primer) | deposited 8 September 2026. It **supersedes** the working draft this row used to select. The reviewed draft is retained unedited as evidence: [draft 0.1](a_primer_on_frameql_v2_3_working_draft_v0_1.md) |
| — | Authority and supersession index 0.1 | [**corrected**](frameql_v7_1_authority_and_supersession_index_v0_1.md) | §4 provenance corrected; selects corrected copies; archived baseline preserved |
| — | ToD v7.1 statistical extension supplement 0.1 | [archived](../reviewed_sources/tod_v7_1_statistical_extension_supplement_v0_1.md) | unchanged |
| — | Reconciliation register 0.1 | [archived](../reviewed_sources/frameql_v7_1_reconciliation_register_v0_1.md) | unchanged; its historical statements are left as written |

A conceptual reader may begin at 8 and 9. Neither replaces the technical authority above.

## Rows 8 and 9 were repointed to published editions (Huayin's ruling of 2026-09-09)

On 8 September 2026 the two reader-facing companions were **published**: *Frame-QL: An Introduction*
v2.4 (`10.5281/zenodo.22661455`) and *A Primer on Frame-QL* v2.3 (`10.5281/zenodo.22661076`). They
are not the drafts this index used to select — the published editions carry real publication metadata
in place of the drafts' *"Status: working successor for review; not published, no DOI assigned"*,
take their analytical foundation from the **published** *Theory of Data* v7.1
(`10.5281/zenodo.22649945`) instead of a working manuscript, and revise the prose substantively (153
and 59 changed lines respectively).

So these two rows now select the publication of record, and the site serves those bytes at the two
`/learn` routes. **The reviewed drafts are retained, unedited, exactly where they were**, and both
rows still name them: the J1/J2 diffs are written against these paths, `REVISION_METADATA.md` and
`EDITORIAL_FOLLOWUP.md` describe them, and `verify_staging.py` checks they have not moved. A
publication supersedes a draft; it does not delete the record of what was reviewed.

**THIS REPOINTING IS EXACTLY TWO ROWS WIDE.** Publishing two reader-facing companions adopts nothing
else. Rows 1–7 and the unnumbered rows are unchanged, and the Frame-QL language-law candidate, the O3
order interface, the capability/profile plan, the semantic acceptance cases and the patch sheet all
remain **unpublished working successors** with exactly the status they had before. Nothing here is
adopted language law, and nothing here is evidence of implementation conformance.

## Evidence beside the documents

- [PROVENANCE_EVIDENCE.md](PROVENANCE_EVIDENCE.md) — deposit verification, record ids, artifact names,
  checksums, pinned repository paths, verification date, the Markdown-only limitation, the itemised
  transcription differences, and the examples-preserved-not-executed statement.
- [REVISION_METADATA.md](REVISION_METADATA.md) — the **original J1/J2 replay evidence**, preserved as
  first written and deliberately not mixed with anything later.
- [EDITORIAL_FOLLOWUP.md](EDITORIAL_FOLLOWUP.md) — every subsequent link and provenance edit, with
  before/after hashes.
- [PATCH_SHEET_DISPOSITIONS.md](PATCH_SHEET_DISPOSITIONS.md) — the recorded disposition of all eleven
  patch-sheet proposals, so the sheet cannot later be applied wholesale.

## What is still true of the whole set

Superseded working guidance in `../editorial_archive/sources/` is historical evidence at its own
snapshot and carries no active instruction. The withdrawn categorical FIRST/LAST-family exclusion, the
universal formation-locality veto, and the older compulsory-migration recommendations must not be
reactivated by citation.

Known ordered-path correctness issues — physical-row FIRST/LAST selection, and ordered contribution
surviving late placement withholding — remain **visible and separate**. This pass neither fixes them
nor authorizes postponing them, and makes no claim about their status on current `main`.

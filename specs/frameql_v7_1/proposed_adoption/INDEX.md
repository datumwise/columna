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
| 8 | Introduction proposed v2.4, draft 0.1 | [**corrected**](frameql_an_introduction_v2_4_working_draft_v0_1.md) | provenance masthead corrected; links repointed |
| 9 | Primer proposed v2.3, draft 0.1 | [**corrected**](a_primer_on_frameql_v2_3_working_draft_v0_1.md) | provenance masthead corrected; links repointed |
| — | Authority and supersession index 0.1 | [**corrected**](frameql_v7_1_authority_and_supersession_index_v0_1.md) | §4 provenance corrected; selects corrected copies; archived baseline preserved |
| — | ToD v7.1 statistical extension supplement 0.1 | [archived](../reviewed_sources/tod_v7_1_statistical_extension_supplement_v0_1.md) | unchanged |
| — | Reconciliation register 0.1 | [archived](../reviewed_sources/frameql_v7_1_reconciliation_register_v0_1.md) | unchanged; its historical statements are left as written |

A conceptual reader may begin at 8 and 9. Neither replaces the technical authority above.

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

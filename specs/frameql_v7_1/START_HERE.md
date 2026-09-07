# ToD v7.1 / Frame-QL — Joint Consistency Review Package

**7 September 2026 · Review 0.1**

## Decision

The joint source review found no new contradiction requiring a theory revision. The next unit is **docs-only staging**, with two exact editorial corrections, followed by review before any merge or publication.

This package is not a new ToD edition or an implementation authorization. The reviewed source files are unchanged. J1 and J2 are prepared adoption edits, not already installed revisions.

## Read in this order

1. [Joint consistency and release-readiness report](tod_frameql_joint_consistency_release_readiness_report_v0_1.md).
2. [The forty-case review ledger](tod_frameql_joint_consistency_case_ledger_v0_1.md), with [machine-readable mapping](tod_frameql_joint_consistency_case_ledger_v0_1.json).
3. [Two exact editorial corrections](tod_frameql_joint_review_editorial_corrections_v0_1.md). J1 states the supported-observation participation premise in a count example. J2 identifies O3's historical S6 source.
4. [Prepared CC docs-only staging brief](FRAMEQL_TOD_V7_1_DOCS_ONLY_STAGING_BRIEF_v0_1.md). It has **not** been sent. Dispatch by the user would authorize staging only; it does not authorize merge, publication, deployment, or implementation.

## Source snapshot

The [source manifest](tod_frameql_joint_review_source_manifest_v0_1.json) identifies twelve complete active Markdown inputs, the supplied acceptance-case JSON, unchanged browser reading copies, and two historical files used only to resolve S6.

The theory remains [Full Manuscript Working Draft 0.4](reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md). The language remains [Language-Law Candidate 0.4](reviewed_sources/frameql_language_vnext_working_draft_v0_4.md). Their [active index](reviewed_sources/frameql_v7_1_authority_and_supersession_index_v0_1.md) identifies the other companions and historical supersessions. `historical_provenance/` does not contain active instructions.

## Validation limits

The case ledger is a reviewer-authored comparison of claims and premises, not a newly executed analytical test suite. The document audit checks hashes, source locations, exact patch replay, unchanged examples and equations, and local links. It does not independently prove semantics. No historical mathematical suite, Columna tests, or CDT API inspection was run here.

To reproduce the file-integrity audit after extracting this package:

```sh
python audit_joint_review.py
```

The result should match [the included audit JSON](tod_frameql_joint_review_document_audit_v0_1.json). `MANIFEST_SHA256.json` covers every packaged file except itself; the audit checks it when present.

## Next boundary

The local semantic review can close at this scope. Publication files/metadata, exact predecessor-source provenance where claimed, live adoption, and implementation assurance remain separate gates. Known correctness-containment needs are not closed or postponed by this review.

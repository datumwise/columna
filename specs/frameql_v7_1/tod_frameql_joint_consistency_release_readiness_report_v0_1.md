# ToD v7.1 / Frame-QL — Joint Consistency and Release-Readiness Review

**Review 0.1 — 7 September 2026**  
**Theory target:** ToD v7.1 Full Manuscript Working Draft 0.4.  
**Language target:** Frame-QL Language-Law Candidate 0.4 and the aligned companion set.  
**Disposition:** Ready for a bounded, docs-only staging pass, with two exact editorial corrections. No new theory revision is required by this review. Publication and live adoption remain separate gates.

This is a joint source review by the same assistant involved in drafting the documents. It is not an independently verified external review, a proof-assistant result, or an implementation audit. The supplied reviews already recorded in the manuscript retain their stated provenance and scope.

## 1. Executive conclusion

The active local documents now give a consistent account of analytical identity, family admission, formation, sufficient state, ordered selection, evidence, and reuse. I found no cross-document contradiction that requires reopening the ToD ontology or changing a proposition. The forty supplied acceptance cases retain their expected semantic judgments under their stated premises.

There are two bounded edits to carry into adoption:

- **J1 — State the participation premise in one count example.** The language candidate's §6.3 presents a count of 97 after noting 97 supported Revenue observations. Its surrounding contract, §8.5, the theory, and acceptance case E02 correctly leave participation to the particular law. The local example should explicitly assume that law counts supported observations, rather than rely on a qualification elsewhere.
- **J2 — Resolve an orphaned historical source marker.** O3 §10 uses `[S6]`, but its current source section does not identify S6. The earlier O3 source section identifies the 14 August 2026 architectural handoff and its limited authority-boundary use. Restoring that identification closes the provenance gap without making its operational status current.

These edits neither change the forty expected judgments nor add a semantic mechanism. They are supplied as exact, source-hash-pinned replacements and diffs. They were replay-checked in memory; **the authoritative input files have not been overwritten or installed as new editions**.

**Recommended decision:** close the joint semantic review at this scope; keep the analytical candidate stable; stage documentation adoption using this exact snapshot plus J1 and J2. Do not publish or declare the live corpus aligned from this report alone.

## 2. Sources and method

Twelve complete local Markdown documents form the reviewed set. Their exact hashes and line counts are in the [source manifest](tod_frameql_joint_review_source_manifest_v0_1.json). Each matches the same-named file in the previously delivered aligned review packet. This checks continuity of the review inputs, not their identity to published deposit bytes.

| Key | Reviewed file and role |
|---|---|
| T | [ToD v7.1 Full Manuscript 0.4](reviewed_sources/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md): analytical authority for this working comparison |
| LQ | [Language-Law Candidate 0.4](reviewed_sources/frameql_language_vnext_working_draft_v0_4.md): request/expression semantic target |
| SN | [Supporting Contract Notes 0.1](reviewed_sources/frameql_v7_1_supporting_contract_notes_v0_1.md): completion, contextual domains, and standing |
| O3 | [Governed Analytical Order 0.2](reviewed_sources/columna_o3_governed_analytical_order_v0_2.md): order declaration/comparison/realization interface |
| I | [Introduction, proposed 2.4, draft 0.1](reviewed_sources/frameql_an_introduction_v2_4_working_draft_v0_1.md): fuller conceptual entry point |
| P | [Primer, proposed 2.3, draft 0.1](reviewed_sources/a_primer_on_frameql_v2_3_working_draft_v0_1.md): shorter conceptual entry point |
| CP | [Capability/Profile Plan 0.2](reviewed_sources/frameql_vnext_capability_profile_reconciliation_plan_v0_2.md): future adoption constraints |
| PI | [Reference Integration Patch Sheet 0.1](reviewed_sources/frameql_v7_1_reference_integration_patch_sheet_v0_1.md): proposed released-reference wording |
| AC | [Forty Semantic Acceptance Cases 0.1](reviewed_sources/frameql_v7_1_semantic_acceptance_cases_v0_1.md): review premises, expectations, and prohibited shortcuts |
| AI | [Authority/Supersession Index 0.1](reviewed_sources/frameql_v7_1_authority_and_supersession_index_v0_1.md): active versus historical guidance |
| CR | [Reconciliation Register 0.1](reviewed_sources/frameql_v7_1_reconciliation_register_v0_1.md): change provenance and remaining limits |
| SS | [Statistical Extension Supplement 0.1](reviewed_sources/tod_v7_1_statistical_extension_supplement_v0_1.md): inherited catalog scope; formulas were not re-proved |

The review compared each acceptance case with T and LQ, then checked the relevant supporting note and introductory summary. It also read the interfaces, migration constraints, status statements, and source index for instructions that could reinstate a superseded rule.

The [case ledger](tod_frameql_joint_consistency_case_ledger_v0_1.md) records each premise, expected judgment, prohibited shortcut, review reasoning, and source sections. Its JSON companion adds section line ranges for the exact T/LQ snapshots. These are reviewer-authored source comparisons, not engine test outcomes.

The original O3 §17 and historical architecture handoff were consulted only to identify S6 for J2. They are segregated in `historical_provenance/` and are not active semantic or operational authority. No live repository, website, package, DOI registration, or CDT API was inspected in this pass.

## 3. Family identity and target resolution agree

**Cases F01–F08: consistent, with no admission-rule change required.**

The explicit target specification is present in T §4 and enforced through T §5.3. LQ §6.5 references that single contract rather than defining a weaker alternative. The distinction is carried into I §6.2: a canonical expression can denote an admitted construction, but arithmetic or an alias cannot supply a missing target or family law.

The positive AOV case survives. T §3.7 permits an explicitly governed multi-parent family; LQ §§2.3 and 11 explain why an output label does not create it automatically. The warning against automatic admission is not a prohibition on ratio families.

Constitutive lineage remains identity-bearing. Alternative lawful staging or proof of an already specified target does not split identity. LQ §10.1 and I §8.2 preserve this direction, which is necessary for T §6.4's consistency obligation to remain meaningful.

The resolution/availability boundary is especially clear across the set:

> Two adequate bases for one target are two possible constructions, not two user meanings. Two identity-distinct targets do not become one meaning because only one presently has an executable plan.

That rule appears in LQ §10.1, SN §1.2, I §3, P's output-dimensions discussion, and PI §6. A short conceptual reader does not need the full basis proof to avoid the wrong inference.

The materialization and COUNT examples also preserve intake versus continuation: retained counts 37 and 12 combine to 49 under their law; counting the two summaries as new observations answers another question. No new count syntax or execution result is claimed here.

## 4. Governed order and the witness construction agree

**Cases O01–O11: consistent.**

T §7, LQ §9.2, and O3 §§1–4 use the same construction: constituent anchors jointly identify existing points; each constituent has its complete governed point order; selected precedence induces the lexicographic order. This does not imply a full Cartesian population, a universal factorization algorithm, or an order inferred from column position.

A complete Day order alone is not a global Customer-Day order. A narrower fixed-customer construction does not gain cross-customer continuation from the physical presence of multiple customers. Neither a lineage label nor lexical identifier ordering supplies a missing constituent law.

The local documents correctly distinguish:

- establishing the operand at its constitutive analytical anchor from selecting a physical row;
- an admitted ordered family from a legacy spelling or runtime category;
- the self-sufficient witness family W from the scalar target L;
- optional retained family R from a mandatory runtime pipeline;
- continuing original S-point witnesses from forming a new ordered family at an intermediate anchor.

The non-contiguous intermediate-group example has the same interpretation in T §8.4, LQ §9.5, and O3 §7. The retained winner is compared using the original order, not the intermediate group label. Admission, compatible contributions, and evidence remain explicit premises.

The language, order note, and capability plan also agree that family standing neither requires nor proves scalar re-entry. This removes both of the previously tempting but invalid category migrations.

Finally, output ORDER BY/LIMIT PER remains legitimate frame selection. It is not prohibited because its output can numerically coincide with LAST, and it does not thereby establish an inner ordered family or reusable witness. The intro is brief on this distinction; its wording does not contradict the technical account.

## 5. Contextual formation and restriction agree

**Cases C01–C04: consistent.**

T §§3.3–3.4 supplies the governing distinction. The daily-change construction is formed under its original predecessor context; addition of those established contributions yields 5. Restarting the predecessor rule inside separate pairs gives 20 because it changes formation.

LQ §§2.4 and 6.10, SN §2.3, I §6.4, and PI §8 all preserve the relevant restriction: a query or optimization must not silently re-form an existing contextual quantity under different conditions while claiming the same construction.

Faithful recomputation remains permitted. The texts do not impose a caching requirement or prohibit an implementation from reconstructing the same constitutive values from adequate evidence.

The prior universal formation-locality veto is explicitly withdrawn. The replacement is the complete family contract, not automatic promotion of every focal expression. LAG, ranking, and rolling forms still require the domain, participation, locus, neighborhood, and boundary semantics that their particular targets need. T's lexicographic point order does not supply a window's distance unit or endpoint convention.

## 6. Evidence and reuse agree; one local count example needs its premise

**Cases E01–E07: consistent at the contract level; E02 identifies correction J1 in a separate LQ example.**

The source/target distinction is now maintained. A contributing point's placement can be unestablished while the output point exists and its eligible measure is unsupported. R4's earlier linear wording no longer makes all source placements a precondition for describing target missingness. See T §2.3, LQ §§8.1–8.4, and SN §3.1.

The unavailable-staged-witness case keeps its exact premises. Participation and the intermediate blocks are known. The missing fact is the operand needed for one intermediate witness. The coarser winner can be established through maximality evidence without replacing that missing witness with the known-empty identity. See T §§6.1 and 9.5, LQ §8.7, and O3 §9.

The scalar-without-winner example also remains guarded in every place that summarizes its particular argument: fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner. It establishes L, not W. The broader statement that other adequate scalar arguments may exist is not itself a general constant-fill rule. See T §9.6, LQ §8.8, SN §3.3, O3 §9, and I §8.4.

This is compatible with the operand-formation rule: a construction consumes established analytical points and values where its argument requires them; it does not demand every nonwinning value solely because the complete-input proof uses one sufficient construction.

Known-empty contribution, missing selected value, unresolved eligibility, and unestablished existence remain distinct. The semigroup qualification for MIN/MAX survives; no synthetic identity or semantic Null is added.

The late-withholding warning is consistent as well. Removing an unplaced row after it contributed to a scan does not repair surviving results. A disclosure can state the limits of a correctly described partial result, but cannot supply missing analytical meaning. The review changes no recorded R4-C0 outcome or current serving policy.

### J1: 97 is conditional on the participation rule

LQ §6.3 presently says that 100 known orders and 97 supported Revenue values give counts 100 and 97, “unless a separate totality/support rule establishes another result.” Its surrounding discussion refers to governed participation, but the numerical example leaves the supported-observation rule implicit.

T §11.5.1 makes the same example conditional on the latter count's participation law counting those supported observations. AC E02 and LQ §8.5 likewise state that counting measure participation does not mean automatically counting surviving values.

The smallest correction is to give the local example that explicit premise. The numerical values and fenced forms remain unchanged. This is an implementation-facing clarification of an existing contract, not a new COUNT rule. The exact text is in the [correction sheet](tod_frameql_joint_review_editorial_corrections_v0_1.md).

## 7. Materialization and approximation do not change authority on the way through the corpus

**Cases R01–R05: consistent.**

T §10.7's three materialization claims are preserved in LQ §10.6 and O3 §12. I §8.4 summarizes the distinction without turning it into another ontology. W can supply L through its admitted nonempty value projection; the reverse is not generally available. Two scalar establishment histories do not create two family identities. A history of having computed a witness is not proof of current retention or recoverability.

The lossy-conflict example stays scoped to its actual result: a local equal-point check on compressed winners is not a global coherence validator. Compatible context must be established outside the lossy shortcut. Matching context labels alone are insufficient; this does not mandate storing all input records. T §10.6, LQ §10.7, and O3 §12 agree.

Equal displayed means do not supply equal continuation state. A retained winner need not answer later deletion, restriction, or a change of order. Additive summaries cannot silently double-count overlap. Each later use retains its own sufficiency and compatibility obligations.

The approximation boundary is also consistent: an explicitly contracted approximation may target the same exact quantity without becoming exact sufficient state. An error grade alone does not create a new semantic target. The companion set does not add a sketch catalog or claim the implementation of HLL. See T §10.9, LQ §§6.9 and 10.8, and CP §4.

## 8. Authority, explanations, and historical guidance agree

**Cases G01–G05: consistent.**

The applicable grammar, versioned language semantics, profile promises, measured coverage, and analytical law are no longer collapsed. The shorter introductions retain their released-syntax boundary and do not advertise T's mathematical notation as new parser acceptance.

EXPLAIN's proposed wording separates normalized surface, resolved meaning, a plan, and applicable evidence. It cannot guarantee all later data-dependent disclosures without the evidence needed for that guarantee. Execution must consume the same resolved meaning; this is not a claim that the current payload or engine already does so. See LQ §§10.2–10.3, O3 §11, I §7, and PI §4.

The actual CDT interface remains unverified. Requiring a faithful point/value representation and comparator does not prove an existing API is present or absent and does not require a nominal type called Witness.

The authority index explicitly dispositions thirteen earlier files. Their observations remain versioned historical evidence. Their withdrawn family exclusions, locality rules, migration proposals, and old mission scopes do not become current authorization. The separate public-reference patch sheet states that it must be adopted against a pinned repository revision rather than applied blindly to moving-main prose.

### J2: identify the historical S6 source locally

O3 §10 retains a bare `[S6]`. Current O3 §17 sends readers to the archived earlier source list but does not identify S6 itself. O3 v0.1 §17 identifies it as the 14 August 2026 architecture handoff, `START_HERE(2).md`, used for persistent authority boundaries only.

The prepared edit restores that identification in current O3's source section and explicitly denies any current operational-status inference. It does not update the lifecycle, reopen the architecture, or convert the August handoff into active instructions.

## 9. What the review does not ask us to change

No new family-admission condition, sufficiency ontology, tie rule, order constructor, type catalog, standing enum, query syntax, capability class, or serving policy is required by these findings.

The theory's four propositions, proof text, evidence cases, and materialization section need no revision for companion consistency. The statistical supplement remains inherited reference material at its declared conditional completion. Its formulas were read for consistency of participation, convention, exactness, and scope claims, not independently re-proved.

The Introduction and Primer need not repeat every theorem. They need to avoid false shortcuts, and they do. Neither needs another witness chapter or a larger operator catalog in this pass.

The source manuscript's Appendix C.4 warning that earlier O2/Frame-QL guidance requires reconciliation remains valid as a warning about those historical texts. At final publication preparation, a current companion-status pointer can describe the local alignment and any actual live adoption then established. That is a metadata/readership update, not a reason to reopen the core now.

## 10. Release-readiness disposition

| Gate | Result of this pass |
|---|---|
| Joint analytical meaning across the active local set | No semantic contradiction established in the reviewed scope |
| Forty acceptance expectations | 39 require no local edit; E02 is consistent with explicit J1 clarification in LQ §6.3 |
| New theory revision or change of proof | Not required by this review |
| Local citation hygiene | J2 prepared; apply during staged adoption |
| Stable source handoff | Ready: exact inputs, two patches, source sections, and hashes are supplied |
| Full publication freeze | Not declared: final files/metadata/source provenance and the chosen review acceptance remain to close |
| Repository/site/retrieval alignment | Not performed or freshly verified |
| Exact Intro/Primer predecessor deposit-byte match | Not established by the supplied transcription-based provenance |
| Actual CDT/type/ordered-state implementation contract | Not inspected |
| Runtime correctness and reported containment work | Not tested or closed by this document review |
| Independent verification | Not claimed; this pass is a self-review of supplied sources |

The publication-source qualification should be interpreted precisely. A new authored revision need not pretend to be byte-identical to its predecessor. But any claimed deposit-faithful source comparison must be supported by exact source evidence. Before adoption, CC should obtain the exact current repository sources, record the pins, and describe any differences from the transcriptions; unexplained source substitutions are not authorized.

A reserved DOI can be incorporated when supplied. No DOI, publication approval, or current deployment status has been inferred in this report.

## 11. Next bounded action

Proceed to **docs-only staging**, not runtime implementation or another theoretical design pass. The [prepared adoption brief](FRAMEQL_TOD_V7_1_DOCS_ONLY_STAGING_BRIEF_v0_1.md) specifies the task for later dispatch to CC. It has not been sent by this review.

The stage should preserve this snapshot, apply J1 and J2 with an explicit source/version record, install the intended working-authority index, and prepare the released-reference wording without claiming new shipped semantics. The applicable grammar, profiles, generated measurements, runtime, and wire remain unchanged. Obtain a reviewable diff and stop before merge, publication, or deployment.

Known correctness containment remains separate. This report neither authorizes it nor postpones it behind publication or type-specification completion.

## 12. Validation scope

The new mechanical audit checks source hashes, case identity and source mapping, exact patch replay, preservation of fenced examples and equations under the two edits, local links within the packaged snapshot, and package integrity. It does not compute the forty analytical examples or turn source agreement into implementation conformance.

The historical 384,728 baseline assertions, 181,530 adversarial checks, and the earlier companion document-audit counts are not new results of this review. They were not rerun or added together as evidence of this report's quality.

The reviewed inputs are unchanged. No independent mathematical or empirical claim is added by writing the case ledger. The report's bounded conclusion is a documented judgment about the consistency of this exact reading set and its readiness for the next controlled documentation step.

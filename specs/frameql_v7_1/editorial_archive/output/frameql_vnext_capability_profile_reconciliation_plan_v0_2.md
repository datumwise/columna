# Frame-QL vNext — Capability and Profile Reconciliation Plan

**Working Draft 0.2 — 7 September 2026**  
**Status:** Rebased documentation/adoption proposal. No implementation authorization.  
**Basis:** [ToD v7.1 Full Manuscript Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md) (**T**) and [Language-Law Candidate 0.4](frameql_language_vnext_working_draft_v0_4.md) (**LQ**).

## 1. What this revision replaces

The v0.1 plan was written when all analytical-point-order-dependent operations were treated as non-family expressions. It proposed moving FIRST/LAST to that exclusive category and making family re-entry inapplicable. Those recommendations are superseded.

The current theory admits complete ordered family constructions while distinguishing the witness-valued family W from scalar target L. W can provide sufficient state for L; a scalar L does not generally retain W's continuation information. A runtime operation name does not determine either claim.

This revision retains the separation of canonical language meaning/standing, authored profile promises, and measured build realization. It does not choose a replacement registry schema or retrospectively validate a legacy operation.

## 2. The questions the authorities must answer

| Responsibility | Governing question | Must not be inferred from |
|---|---|---|
| Analytical family law | Is the target independently specified and the complete family contract admitted? | Function name or execution kind |
| Language meaning and standing | What does this accepted construct denote, and in which language version is it admitted? | Mere parser acceptance or a theory example |
| Profile obligation | What realization does the implementation undertake? | A generated measurement or proposed extension |
| Materialized capability | What information is retained, what is established and why, and what reuse is justified? | A label such as “LAST available” or equal scalar displays |
| Build measurement | What does this measured release actually support? | An authored capability promise |

These are semantic distinctions, not five mandatory fields or services. A later schema design should express them without duplicating authority. The earlier `semantic_class` field name is a proposal, not a frozen implementation contract.

## 3. FIRST/LAST and re-entry

Keep these judgments separate:

- A complete admitted FIRST/LAST construction can denote a family under T §4 and §8.
- The witness family can be self-sufficient under its admitted compatible composition.
- The scalar target can be constructed from W on the admitted nonempty domain but does not generally retain W's point witness.
- A legacy runtime `re_entrant=False` may correctly describe finalized-value insufficiency. It is not proof that FIRST/LAST cannot be a family.

Do not change a boolean to true merely because ordered family admission is possible. Do not remove the question as irrelevant merely because runtime kind differs. A later interface must state what analytical value or representation the capability describes and which next operation is being authorized.

The old registry/runtime categories may continue to serve version-specific routing or reporting until deliberately reconciled. Exact category names are not the theoretical source of family authority.

## 4. Other capabilities

### Contextual operations

LAG, rank, cumulative, and rolling constructs retain their particular language/version standing unless separately changed. No category migration in this plan ratifies an operator. A proposed family based on contextual formation must satisfy T §4; no blanket locality veto survives.

### Value and standing operations

Keep the distinction between semantic-value operations and conceptual standing predicates. `is_missing` has a target-standing meaning only if its complete language contract is admitted. Carrier-null inspection is not analytical missingness. Generic `coalesce` is not a governed completion law.

The v0.1 suggestion to remove proposed `is_null` or `coalesce` rows is not an automatic mutation instruction. Their exact namespace and status need to be reconciled against their actual declared purpose. They must not be used to manufacture support or null-based analytical authority in the meantime.

### Brackets and rich values

The working target reserves brackets for value subscription and withdraws the analytical-filter roadmap. That is a future-language ownership rule. No grammar scaffold is removed here, and no type is declared subscriptable by this note. The CDT capability catalog remains a separate authority.

### Approximation

An exact finite set or multiset may grow with the evidence. A bounded-memory limitation or absent bounded-size witness must not be described as impossibility of finite exact retained state. Cost and implementation support remain separate from mathematical adequacy.

An estimate may target the same exact family while carrying an explicit approximate-realization contract. It is not an exact sufficient-state basis. A coverage row must not erase exactness, retained state, or reuse limitations when reporting that a callable operator exists.

## 5. Preserve actual profile obligations during reconciliation

This document changes no Core promise, Platform addition, capability ID, operator standing, accepted spelling, error code, or wire field. The prior reports and repository documents are evidence at their own dates; no current package has been installed or tested for this task.

A later adoption should compare the actual versioned registry, profiles, generator, runtime routing, and public surfaces. Where identity and semantics stay the same, a label change does not require changing the capability ID. Where the analytical contract genuinely changes, the change cannot be disguised as editorial renaming.

Do not invent a Platform-only dialect because Platform has another runtime mission. Shared analytical meaning remains the invariant; any additional capability requires an explicit requirement and contract.

## 6. Release-reference adoption

The public Manual's successor wording should separate:

1. the resolved analytical target;
2. accepted versioned surface syntax;
3. profile obligations;
4. measured coverage and known realization gaps.

Its EXPLAIN promise should describe resolved meaning and applicable assurance without guaranteeing all future data-dependent disclosures. Its alias terminology should say output key rather than analytical identity. The [reference integration patch sheet](frameql_v7_1_reference_integration_patch_sheet_v0_1.md) supplies focused replacements without hand-editing generated tables.

The published Introduction and Primer sources remain historical artifacts until separately released successors replace their routes or citations. Installing the new working texts in a repository is a separate documentation action, not implied by their creation here.

## 7. Public references and old mechanisms

The corpus inventory established public exposure of `.last` in examples and documentation; it did not prove the absence or presence of every external customer dependency. Preserve useful public analytical reference where complete meaning can be resolved, and report ambiguity or unsupported realization truthfully.

An old `FAMILY { last ORDER day }` encoding is neither permanent semantic authority nor automatically a category-B feature that can be deleted without impact. Its eventual normalization or retirement is a separate evidence-based decision. No such decision is executed in this plan.

Reported nondeterministic physical-row selection and ordered contribution before late placement withholding remain correctness concerns. They are not repaired by changing operator classes or documenting an approximation. A separately authorized fail-closed containment can proceed without waiting for the full successor implementation.

## 8. Minimum checks before a later adoption

Review the actual coupled authorities, rather than copying old line numbers. The resulting changes should demonstrate that canonical target identity is independent of physical plans; ordered family admission is separate from retained re-entry capability; no new operator standing was silently introduced; profile promises changed only by explicit decision; generated measurements remain generated; and any known divergence is explained rather than erased.

A spec/runtime check cannot simply assert equality between semantic class and engine kind. It must test the applicable contract and distinguish intentional versioned compatibility from accidental disagreement. A generator must not silently omit an unfamiliar class and declare success.

The first implementation slice should be selected from current evidence after this document set is reviewed. This plan does not authorize registry edits, tests, parser changes, family-founding gates, new types, or wire migration.

## 9. Sources and status

T and LQ are the working semantic sources. The v0.1 plan, earlier M2/O2 reports, migration matrices, and CC instructions remain historical inputs with the dispositions in the [authority index](frameql_v7_1_authority_and_supersession_index_v0_1.md). Public repository reads during this task were document observations at moving `main` URLs, not a pinned implementation audit.

The present accomplishment is a corrected migration target. Implementation conformance, publication status, and repository/site installation remain unclaimed.

# Frame-QL — Release-Reference Integration Patch Sheet

**Working editorial replacements 0.1 — 7 September 2026**  
**Scope:** Proposed wording and version notices for the release-reference layer. Not applied to a repository.  
**Working target:** [Language-Law Candidate 0.4](frameql_language_vnext_working_draft_v0_4.md) and [ToD v7.1 Full Manuscript Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md).

## 1. Use and source boundary

The public `docs/frame_ql_language.md` was read at a moving `main` URL. Its headings identify the destinations below; line numbers from older reconnaissance are not reused as current patch coordinates. This sheet is not a byte-level diff or a claim that these replacements apply cleanly to a particular commit.

The replacement paragraphs below are actual proposed text, not instructions to edit generated measurements. An authorized documentation adoption should compare them with the exact current source, keep release-specific facts truthful, and make version scope explicit. If a paragraph describes a successor obligation not yet met by the released implementation, retain that limitation beside it.

**Source read:** `https://raw.githubusercontent.com/datumwise/columna/main/docs/frame_ql_language.md`, 7 September 2026. The earlier companion assessment records the broader profile/capability/revision-history observations; none was rerun as implementation evidence in this task.

## 2. Opening compatibility / authority notice

**Destination:** the edition/availability and ToD reconciliation opening.

**Proposed successor notice:**

> This reference describes the accepted grammar and behavior of its identified Frame-QL release. The accompanying v7.1 language-law candidate supplies the successor analytical interpretation; it is not evidence that this release implements every admitted family construction. The Theory of Data governs analytical identity and family law. The versioned grammar determines formal syntax, this reference describes its released meaning, profiles state authored implementation obligations, and build-status records report measured coverage. Retained implementation vocabulary does not redefine the theory, and theoretical admission does not enlarge the released language.

**Adoption condition:** identify the reference's actual release scope. Do not relabel the existing document as fully v7.1-conforming while it still documents known legacy gaps. The current working theory is not a published v7.1 edition.

## 3. Query aliases and output keys

**Destination:** §1.6 and other passages calling an alias the output column's “identity.”

**Proposed replacement:**

> An alias supplies an output column key and follows the reference's existing visibility and collision rules. It does not establish analytical family identity. A canonical analytical construction can denote a family when its complete law is admitted; assigning `AS name` neither supplies a missing law nor publishes or ratifies a definition. Changing the output key does not change the already-resolved analytical quantity.

Keep the actual syntax, alias scope, error behavior, and compatibility code unchanged. This is a terminology correction, not an alias feature change.

## 4. EXPLAIN

**Destination:** §1.7, especially the promise to return “every disclosure the executed query would carry” while not touching data.

**Proposed replacement:**

> EXPLAIN presents the resolved request, the proposed realization, and findings justified by information available to that explanation. It must distinguish applicable assurance from checks not yet performed. A data-free explanation does not itself establish every data-dependent support condition or guarantee every later disclosure. Execution must use the same resolved analytical meaning; it may establish additional evidence or decline the proposed realization when its premises fail. The exact fields emitted by this release remain defined by its documented interface.

**Adoption condition:** compare this contract against the actual payload and document any missing distinction. Do not add fields or claim data validation through an editorial change. Retain the parser/render round-trip guarantee separately where it is an actual release contract.

## 5. Canonical target versus execution decomposition

**Destination:** §2.1 and EXPLAIN descriptions that equate canonical form with reducer-atom decomposition.

**Proposed replacement:**

> A normalized surface spelling, the resolved analytical target, and a physical decomposition are different records. Equivalent admitted plans may establish the same target. A particular engine's reducer atoms, scans, or materialization choices do not become constitutive lineage merely by appearing in its trace. The implementation must preserve the resolved target and its meaning-bearing anchors, law, order, and participation throughout execution.

Retain genuine release-specific trace mechanics as mechanics. Do not let a statement that a particular plan has been produced stand in for evidence that its inputs are available.

## 6. Default completion and input-anchor clarification

**Destination:** bare-name/default-family sugars and omitted input-anchor rules.

**Proposed replacement:**

> Default completion resolves an already-governed construction when the selected definitions establish one analytical meaning. The zero/one/many reading discipline counts distinct targets after governed equivalence, not candidate bases or physical plans. Several adequate bases for one target do not require an intent clarification. If two identity-distinct readings remain and only one can currently execute, availability does not silently select the user's meaning. A resolved target can remain unavailable from the present evidence without becoming a different target.

Keep actual supported sugar and reason codes version-specific. This text does not create new default-completion authority.

## 7. Family and ordered-operation explanation

**Destination:** family/member explanations, FIRST/LAST descriptions, and the ordered-operation section.

**Proposed successor paragraph:**

> Analytical-point-order dependence does not categorically exclude family standing under the v7.1 working theory. A complete admitted FIRST/LAST construction uses governed order on the constitutive analytical points and adequate state. Its witness-valued family can supply scalar LAST without making the scalar sufficient for witness continuation. The released `first`/`last` category and legacy declaration encoding are implementation facts; neither the spelling nor the runtime kind proves the full successor family contract. Missing constituent order or precedence, unestablished analytical formation, and physical row selection must remain visible as gaps rather than being completed by backend convention.

**Do not:** delete public `.last`, set re-entry true, change family-founding gates, or declare all legacy paths conforming through this wording. The eventual mechanism is a separately authorized engineering decision.

## 8. WHERE, HAVING, and frame selection

**Destination:** frame clauses and any summary saying all clauses simply shape output.

**Proposed replacement:**

> `WHERE` restricts inputs within the request's declared formation scope. It can change the quantities formed from those contributions. It must not silently re-form an already-constituted contextual quantity under a different context while claiming the same construction. `HAVING` selects already-formed output, and output `ORDER BY` and `LIMIT ... PER` order or select the returned frame. Their use does not supply the order of an inner analytical operation. Predicate pushdown is a realization choice only when it preserves the declared analytical formation and participation.

Keep current per-series reachability, valid clause forms, and documented realization limitations. A currently unsupported lawful filter remains a realization issue; this wording does not reclassify it automatically.

## 9. Phi, NULL, support, and partial results

**Destination:** basis/fill explanation and absence-disclosure summaries.

**Proposed addition:**

> The release's fill and carrier representation is not the ontology of analytical standing. Point existence, placement, eligibility, target support, known-empty contribution, and supported zero are distinct judgments. Evidence requirements depend on the target law; not every unavailable earlier value blocks LAST, and a sufficient witness is not necessary for every adequate scalar argument. A downstream caveat or row filter cannot repair a computation that has already consumed an unestablished ordered contribution. Where the release cannot represent a distinction, record that limitation rather than mapping it silently to NULL or zero.

**Adoption condition:** preserve the exact released Phi behavior as a compatibility description unless a separate implementation change alters it. Do not promise new predicates, standing enums, or a complete R4 implementation.

## 10. Bracket roadmap and typed value access

**Destination:** roadmap analytical filtering and reserved syntax.

**Proposed replacement:**

> The older analytical bracket-filter roadmap is withdrawn from the successor language target. The working semantic role of `E[key]` is value subscription where the semantic type and language contract admit it. This reservation does not assert current parser acceptance or type support. A future expression-local analytical restriction requires its own unambiguous language rule.

This withdraws a roadmap recommendation. Any code retirement, parser grammar change, or new subscription implementation requires separate authorization.

## 11. Profile and generated-table notices

**Destination:** capability-reference introduction and profile/build-status cross-links; not generated rows.

**Proposed addition:**

> These entries record the distinct authorities identified by their columns or source files. Callable availability is not full analytical-law conformance. A family-capable construction may have a scalar output insufficient for continuation; retained capability must be qualified by what the representation contains and what next use is admitted. No theoretical revision silently changes operator standing, profile promises, or measured release coverage.

Do not hand-edit generated tables to produce superficial agreement. The rebased capability/profile plan defers schema decisions until actual coupling is inspected.

## 12. Adoption and supersession checklist

After a separate authorized documentation adoption, reviewers should verify that the selected current reference points to the current candidate or publication; historical editions remain identifiable; active O1/O2/R4/O3 instructions use the same theory; the latest Intro/Primer links do not point to older successor drafts; generated tables remain generated; and no public page claims a DOI, publication, implementation, or verification state that has not been established.

No part of that installation has been performed in this local task. This sheet closes the wording-design portion and supplies the proposed changes; it does not report repository or site alignment as completed.

# Frame-QL — Supporting Contract Notes for ToD v7.1

**Working Notes 0.1 — 7 September 2026**  
**Status:** Supporting explanation, not a second language or family specification.  
**Sources of current meaning:** [ToD v7.1 Full Manuscript Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md) (**T**) and [Language-Law Candidate 0.4](frameql_language_vnext_working_draft_v0_4.md) (**LQ**).  
**Not published. No syntax, schema, runtime, or implementation authorization.**

These notes consolidate the retained work of O1, O2, and R4. O3 has a separately revised [order-interface note](columna_o3_governed_analytical_order_v0_2.md). Their prior documents remain historical inputs; the [supersession index](frameql_v7_1_authority_and_supersession_index_v0_1.md) identifies the recommendations that must not be reused.

## 1. O1 — Governed shorthand and complete meaning

### 1.1 What omission is allowed to do

A shorter spelling may resolve to a complete governed construction. Omitting an input anchor, order selection, or other identity-bearing parameter is legitimate only when the selected environment establishes a unique analytical reading, including any admitted equivalences. The source of completion is the governing definition, not a physical row order or the plan that happens to run.

This preserves O1's useful distinction: surface explicitness is not the same as every field being typed by the user. Completed meaning must be inspectable. It need not be forced into a query string whose grammar cannot express it.

The complete order in the foundational FIRST/LAST law is T §7's order of analytical points, constituted by complete constituent orders and dimension precedence. Neither a time-like label nor a backend comparator selects that law implicitly.

### 1.2 What resolution counts

Resolve analytical meanings before choosing evidence and physical realization. Several sufficient-state bases for one target are not an ambiguity of intent. Conversely, only one executable alternative does not remove an unresolved distinction between MEAN over orders and MEAN over customers.

A canonical name can resolve an admitted family construction without creating it. Its constitutive input, target law, and lineage determine identity. Proof methods and internal staging paths to the same target do not become identity fields merely to avoid consistency obligations.

### 1.3 Compatibility without silent certification

Public `.last` references are not presumed disposable merely because their old engine representation is awkward. A compatible successor may resolve them to complete admitted meaning. But an old `ORDER day` field does not prove a complete multidimensional order, establish the analytical operand at the required input anchor, or show that the engine consumes the correct witness state.

The earlier instruction to make FIRST/LAST categorically non-family is withdrawn. The opposite shortcut—declare every legacy FIRST/LAST family conforming—is also invalid. Syntax, analytical family admission, retained re-entry capability, and runtime conformance must be examined separately.

No deprecation deadline, normalization grammar, or internal mechanism migration is decided here. The exact accepted versioned surface remains unchanged by this document task.

## 2. O2 — Contextual ordered expressions

### 2.1 Preserve the domain insight, not the family exclusion

O2 correctly distinguished the complete analytical point from its order coordinate. An Account-Day balance is about an Account-Day point, not a physical transaction row or the string naming a Day. Contextual operations can need a focal anchor, a comparison/sequence domain, a contextual grouping, and an operator-specific neighborhood or selection law.

These are useful explanatory roles. They are not a new ordered ontology, a mandatory class hierarchy, or a common object that every family must instantiate.

For an admitted FIRST/LAST family, the constitutive support anchor and its order are fixed by the law. Each admitted current anchor supplies the relevant projection fibers, and the original support-point witnesses remain comparable under that fixed order. A separate generic peer parameter is not added merely to emulate a SQL window.

For focal expressions, contextual grouping can be distinct from the output anchor. A cumulative series by account, for example, must not silently acquire an annual reset merely because a Year coordinate is added to its displayed frame. That context must be specified in the analytical expression or its governing definition.

### 2.2 Relative position, comparison class, and range are different

Positional LAG uses a predecessor relation. Rank can intentionally classify equal compared values together. A seven-point window and a preceding-seven-day range use different neighborhood laws. An order alone supplies neither a time-distance unit nor an endpoint convention.

A contextual law therefore states the domain, participation, required comparison or position, missing-operand behavior, focal locus, and boundary or undefined cases that affect its target. There is no universal “ignore missing” policy. A predecessor whose value is unavailable is not silently replaced by the preceding supported point.

These distinctions are retained from O2. They do not automatically admit every proposed rank/window form into Frame-QL or require that all such operations be excluded from families.

### 2.3 Formation and continuation

Use T §3.4 and the full T §4 contract. A contextual formation must be specified, an independently establishable adequate basis must construct the specified target, and admitted continuation must preserve that formation, participation, and defined-result conditions.

The contextual formation can be faithfully recomputed from adequate evidence. The restriction is against changing its meaning, not against recomputation itself. The difference-then-SUM example yields 5; restarting differences in each subgroup yields 20 because it removes a boundary contribution.

The early rule “any cross-point formation fails projection-fiber locality and therefore cannot be a family” is withdrawn. Fiber-local continuation does not prohibit a contextual history of already-established contributions. The earlier TOP-k promotion is also withdrawn from this pass; no complete TOP-k contract is supplied here.

### 2.4 Frame operations remain frame operations

`WHERE` restricts inputs within the declared formation scope. `HAVING` selects already-formed output. Output `ORDER BY` and `LIMIT ... PER` may select a terminal-looking row without thereby constructing an inner LAST family or its sufficient state.

Returning the same number does not make two operations the same analytical object. This preserves legitimate frame-selection functionality while forbidding ambient inheritance of outer order into an inner expression.

## 3. R4 — Standing, evidence dependencies, and partial results

### 3.1 Distinguish the claim that is unestablished

The retained distinctions are point existence, projection placement, eligibility, target support, and semantic value. They are not one carrier-null classification and not an obligatory linear pipeline for every request.

A candidate root point may be known nonexistent, known existent, or of unresolved existence. A known point can have unsupported placement under a particular anchor. An established target point can remain present while its measure is unsupported because required contributing placements are unresolved. Each statement identifies a different subject.

In particular, an existing eligible output point with unsupported value can carry the conceptual `missing(E)` judgment even when the cause is an upstream placement failure. This does not erase that cause. A nonexistent output point, known ineligibility, and unresolved eligibility are not that same judgment.

### 3.2 Known loss does not imply universe shrinkage

When governed evidence establishes that a particular transaction occurred but its record was lost, occurrence is not inferred from the surviving table. Its coordinates, eligibility evidence, and values may be recoverable to different degrees from other sources.

If governance establishes exactly 100 participating events, point count remains 100 even if 99 Revenue values are supported. A different measure count may deliberately count supported Revenue participation under its own law. Neither lets a mean over all 100 silently discard the lost value from its target population.

### 3.3 Evidence adequacy follows the target law

A LAST result can be established without every earlier operand value when the complete intended domain, order, maximality, and selected value are established. The example does not authorize dropping unknown points or assuming the latest surviving row is the actual maximal participant.

The known `s1 < s2 < s3` example can establish `(s3,30)` at a coarser anchor while a staged plan lacks the exact intermediate witness at s1. This is not unknown block membership: participation is known, but the required intermediate value is unavailable. Never replace it with the identity for known-empty contribution.

For a scalar without an identified winner, the specific T §9.6 argument requires a fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner. It establishes scalar L, not W. Equal values among observed survivors are not sufficient evidence. This example does not create a generic constant-fill execution rule.

### 3.4 Partial output is a claim, not a repair mechanism

A partial-result contract must identify what the returned result establishes and which intended coverage it does not supply. A disclosure cannot retroactively define a computation that had no lawful ordered domain. Removing an unplaced row after it contributed to a cumulative result is not containment of that contribution.

Recorded R4-C0 behavior and open ordered-path defects remain historical engineering facts at their reported revisions. This note neither reruns those probes nor changes their dispositions. It does not introduce a standing enum or reopen the accepted narrow empty-frame-with-disclosure behavior through documentation alone.

### 3.5 Standing predicates are not finalized grammar

`exists`, `eligible`, `supported`, and `missing` are conceptual in these notes. A complete public predicate contract would need to define its subject, unknown cases, result behavior, and supported language/profile surface. No SQL NULL test, generic `is_null`, or `coalesce` operation is silently promoted into that role.

## 4. O3 — Declaration and realization interface

Use [O3 v0.2](columna_o3_governed_analytical_order_v0_2.md) for the retained logical proposal. It describes constituent point orders, precedence at the support anchor, and the family's binding. Its comparator requirements are obligations for the actual CDT/interface review, not inspected API features.

The resolved meaning must be the one execution consumes, not an EXPLAIN-only annotation. The authored Manifold remains logical-only; private mappings realize it. Current evidence and certification establish applicability without re-inventing the law from physical conventions.

T owns W/L/R, the four finite propositions, and evidence/materialization distinctions. O3 does not duplicate their proofs. One physical artifact may retain several analytical values or only one; the claim must identify actual retained content and permitted reuse.

## 5. Common constraints for every companion

A sufficient basis need not be necessary for every adequate argument. A supported scalar need not retain a basis. An alternative basis is checked against a specified target, not admitted through pairwise agreement alone. Lossy compression does not certify coherent input. Approximation may target the same family while carrying a different realization guarantee; it does not become an exact basis or excuse an unestablished computation.

These are the common obligations referenced by the [semantic acceptance set](frameql_v7_1_semantic_acceptance_cases_v0_1.md). They must survive future editorial shortening, code generation, and handoff. No new theorem, proof execution, release conformance, or deployment result is claimed by the notes.

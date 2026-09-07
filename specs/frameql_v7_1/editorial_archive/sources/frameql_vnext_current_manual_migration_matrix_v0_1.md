# Frame-QL vNext — Current Manual Migration Matrix

**Working Draft 0.1 — 6 September 2026**  
**Basis:** current public `docs/frame_ql_language.md` on 6 September 2026, reconciled against the consolidated vNext language-law candidate.  
**Purpose:** classify existing Manual content before any repository edit.  
**Not an implementation authorization.**

---

# 0. Classification key

Each current section is assigned one primary action.

| Action | Meaning |
|---|---|
| **KEEP** | Semantic content remains valid; migrate with only editorial/terminology cleanup. |
| **REWRITE** | The problem and much of the content remain, but the conceptual model must change under vNext. |
| **COMPAT** | Preserve as historical/shipped compatibility behavior, not as the canonical conceptual grammar. |
| **RETIRE** | Remove from the canonical target; normally an unshipped roadmap form or superseded concept. |
| **MOVE** | Content belongs primarily to profile/build/wire/surface authority rather than canonical language law. |
| **AUDIT** | Orthogonal subsystem remains valuable but should be reconciled separately; do not casually rewrite it as part of expression vNext. |

The rule is conservative:

> **Keep useful clause-level law. Rewrite only where the new semantic architecture actually changes jurisdiction or meaning.**

---

# 1. Executive result

The current Manual does **not** need to be discarded.

Its envelope, frame model, explicit output anchoring, clarification discipline, macro/alias distinction, one-expression-one-universe rule, most frame clauses, and much of its outcome machinery remain useful.

The heavy rewrite is concentrated in five regions:

```text
1. implementation vocabulary / authority preface
2. reducer / family-member expression ontology
3. fill-rule Φ as the model of absence
4. ordered reducer / scan semantics
5. generated reducer | map | scan capability taxonomy
```

One unshipped branch should be removed entirely:

```text
analytical bracket filtering E[predicate]
```

The rest is migration, not reinvention.

---

# 2. Preface and authority

| Current section | Lines | Action | vNext treatment |
|---|---:|---|---|
| Manual identity / build-status pointer | 0–9 | **KEEP** | Preserve the fact that language meaning and measured build are separate. Strengthen the four-authority model rather than reintroducing availability into prose. |
| Preface — “The Frame is the query” | 10–26 | **KEEP** | This remains the origin law. Replace “series/reducer” assumptions only where they appear later. |
| Editions and availability | 27–42 | **MOVE** | Canonical language should state standing; profile/build documents state realization. Remove prose that makes the Manual itself the place to infer what “ships today.” |
| Statistical Bridge scope | 43–45 | **KEEP / EDIT** | Preserve stage boundary. Update old inherited-v5 explanation only as needed; do not let it dominate language law. |
| ToD v6.1 reconciliation / retained v5 vocabulary | 46–57 | **REWRITE** | Point to ToD v7. Replace “measure/member/family set” as conceptual bridge with vNext family/measure/expression jurisdictions. Retained implementation terms move to compatibility notes rather than forming the Manual’s conceptual spine. |

### Ruling

The new opening should say once:

```text
ToD                 analytical objects and laws
CDT                 semantic value types/capabilities
Frame-QL            expression/request semantics
capability registry canonical language standing
Core/Platform       realization promises
build status        measured release reality
```

---

# 3. Chapter 1 — Basic Structure

| Current section | Lines | Action | vNext treatment |
|---|---:|---|---|
| 1.1 What a query is | 60–66 | **KEEP** | One output frame, one final anchor, selected value expressions. |
| 1.2 Skeleton / fixed envelope | 67–92 | **KEEP** | Preserve shipped grammar exactly until a syntax ruling changes it. |
| 1.3 `FROM` / bound Manifold | 93–111 | **KEEP / MOVE DETAILS** | Keep language semantics. Move UI/session injection and current entitlement mechanics to surface/profile docs where overly operational. |
| 1.4 `SELECT` + output `AT` | 112–126 | **KEEP** | Strongly aligned with vNext. |
| 1.5 `AT` and `@` — anchor ascription | 127–151 | **REWRITE** | Preserve `@` expression anchoring and `AT` final-frame anchoring. Remove the claim that ascription itself chooses aggregation/broadcast mechanics as the conceptual definition. Explain family/expression anchoring first; realization follows later. |
| Universe resolution inside 1.5 | 133–138 | **KEEP / EDIT** | Preserve one-expression-one-universe and structural resolution. Explain universe law using current ToD vocabulary. |
| Basis + Φ fill rule | 136–141 | **REWRITE HEAVILY** | Replace `event/spine + Φ` as the standing model with existence → placement → eligibility → support → value. Keep current Φ only as compatibility realization/completion policy until authoring migration is understood. |
| “Two anchors” compatibility note | 149–151 | **REWRITE** | Replace old reduction language with constitutive inner anchor vs current analytical anchor. |
| 1.6 aliases / output keys | 152–190 | **KEEP / EDIT** | Preserve alias visibility, collisions, output-key rules. Remove bracket-filter references; move dotted family references to compatibility. State explicitly that `AS` never promotes an expression. |
| 1.7 `EXPLAIN` | 191–207 | **KEEP / SPLIT** | Keep canonical-resolution/explanation semantics. Move exact current atom decomposition and certificate payload details to profile/build/wire authority where implementation-specific. |

---

# 4. Chapter 2 — Current Series Expression Model

This chapter is the largest conceptual rewrite.

The current framing says:

```text
series = reduction | map | composite
```

vNext instead requires an expression-sort model.

## 4.1 Chapter-level migration

| Current section | Lines | Action | vNext treatment |
|---|---:|---|---|
| Ch.2 introduction / “Series Expressions: canonical form” | 210–223 | **REWRITE** | Replace with **Expression Sorts**. `series` can remain the output-column/SELECT-item term, but it is not the ontology of every subexpression. |
| 2.1 canonical `op(col @ a...) @ A` | 224–254 | **REWRITE** | Preserve self-contained canonical meaning. Replace “every expression decomposes into reducer atoms + maps” with family-law, pointwise, tuple, ordered, standing, and frame expression forms. Planner atom decomposition becomes profile realization, not semantic definition. |
| Multi-input shape | 236–241 | **REWRITE / PROMOTE CONCEPT** | The prior missing “participation/joint-support law” is now the governed **co-participation contract**. Tuple and multi-input family laws are semantically ruled. Exact grammar/implementation remains profile-specific. |
| 2.2 bare names | 255–269 | **REWRITE** | Bare governed name resolves to a family reference; anchoring establishes a measure. Short forms may use governed default completion where single-valued. Avoid “column under default reducer from root” as foundational semantics. |
| 2.2 dotted family variants | 270–276 | **COMPAT** | `revenue.sum`, `level.last` cease to define family-member grammar. `sum` normalizes to family-law formation; `last` to ordered expression. |
| 2.3 reducer + input pin | 277–364 | **REWRITE, KEEP CORE LAW** | Preserve the excellent ambiguity/equivalence discipline: zero readings refuse, one proceeds, several clarify; equivalence must be governed. Rewrite “reducer/mule/fertile” exposition around family-forming laws and constitutive inner anchors. |
| Product/composite input pin laws | 352–364 | **KEEP / EDIT** | Preserve pin-coarser and redundant-pin adjudication where still valid under governed anchor geometry. |
| 2.4 map expressions | 365–383 | **REWRITE** | Rename to pointwise/general anchorable expressions. Preserve anchor/co-universe obligations. Add explicit co-participation; arithmetic syntax does not establish joint support by itself. |
| 2.5 one expression, one universe | 384–406 | **KEEP / AUDIT** | Preserve current cross-universe rule unless separately changed by composition architecture. Replace `level.last` example with canonical or explicitly compatibility-marked form. |
| 2.6 broadcast | 407–427 | **KEEP / REWRITE TERMINOLOGY** | Keep replicate-only analytical distinction. Replace old B-anchor explanation where it relies on implementation ontology; connect prohibition to governed law/conservation. |
| 2.7 composite reductions | 428–444 | **REWRITE** | Recast as nested family-forming laws / anchorable expressions. `max(sum(...))` remains a useful example; “two reducer atoms” is realization detail. |
| 2.8 bracket filtering | 445–455 | **RETIRE** | Remove canonical roadmap entirely. `[]` is reserved for value subscription. |
| 2.8 scans | 456–465 | **REWRITE** | Move to ordered-expression chapter. Replace “orderable/natural axis” with governed order contract + unique default completion. |
| 2.9 grows by ruling | 466–474 | **KEEP / EDIT** | Preserve grow-by-ruling. Change “enters when implemented/tested/versioned” to the new authority order: semantic ruling establishes language standing; profile/build realization is separate. |

---

# 5. Chapter 3 — Sugars

| Current section | Lines | Action | vNext treatment |
|---|---:|---|---|
| Ch.3 purpose | 475–477 | **KEEP** | Mechanical sugar remains a good design principle. |
| 3.1 default-family reduction implicit | 478–501 | **REWRITE** | Recast using ToD v7 **single-valued governed default completion**. A short surface can resolve to an already governed family construction; it does not invent a reducer/root. |
| “mules/fertile reducers” in 3.1 | 496–501 | **COMPAT / REWRITE** | Keep current implementation compatibility vocabulary where needed, but canonical semantics should talk about identity-bearing inner anchors and continuation standing. |
| 3.2 omitted input anchor equivalence | 502–537 | **KEEP / REWRITE TERMS** | Strongly aligned with vNext. Governed equivalence, not accidental data equality. Connect directly to constitutive-inner-anchor law. |
| 3.3 no implicit output anchor | 538–544 | **KEEP** | Exact invariant survives. |
| 3.3 no implicit non-default family choice | 543–544 | **KEEP / EDIT** | Preserve “do not guess another family law”; use family-law/default-completion terminology. |

---

# 6. Chapter 4 — Frame Clauses

The envelope clauses largely survive.

| Current section | Lines | Action | vNext treatment |
|---|---:|---|---|
| 4.1 `WHERE` | 547–580 | **KEEP / EDIT** | Keep pre-formation/input restriction semantics. Replace row-centric language with analytical participation where useful. |
| 4.1.1 relationship-derived filter | 581–597 | **KEEP SEMANTICS / MOVE AVAILABILITY** | Canonical law says whether form is lawful; current build support belongs in profile/build status. |
| 4.2 `HAVING` | 598–635 | **KEEP** | Output-frame predicate semantics survive. |
| `count(*)` discussion | 616–624 | **KEEP AS RETIRED/UNRULED NOTE, UPDATE** | ToD v7 now cleanly distinguishes `count(I)` from `count(x@I)`. Do not assign `count(*)` silently. Future canonical teaching should use explicit anchor-derived count rather than `*`. |
| 4.3 `ORDER BY` | 636–650 | **KEEP + ADD BOUNDARY** | Preserve output-frame ordering; explicitly state it never supplies an inner ordered-expression contract. |
| 4.4 `LIMIT` / `PER` | 651–692 | **KEEP** | This is frame selection, not family formation. Tie behavior remains frame-selection semantics. |
| 4.5 allocation bindings | 693–701 | **AUDIT** | Relationship-crossing law, not vNext expression core. Keep separate until shared crossing-authority reconciliation says otherwise. |
| 4.5 macros | 702–732 | **KEEP** | Strongly compatible. Add explicit note: macros do not promote durable identity. |

---

# 7. Chapter 5 — Type Rules / Validity

This chapter should become **Validity, Adjudication, and Realization** rather than a mixture of old type rules and risk policy.

| Current section | Lines | Action | vNext treatment |
|---|---:|---|---|
| Ch.5 opening: well-formedness vs soundness | 733–747 | **REWRITE** | Separate language validity, analytical adjudication, support standing, profile realization, and disclosures. Do not let one “soundness” bucket absorb standing/permission/certification. |
| 5.1 output anchor required | 748–751 | **KEEP** | Grammar invariant. |
| 5.2 anchor compatibility | 752–768 | **REWRITE** | Pointwise co-participation, family-law anchor conditions, broadcast/structural movement should be stated by expression sort. |
| 5.3 B-anchor checking | 769–800 | **COMPAT / REWRITE** | Preserve shipped prohibition behavior as compatibility/profile mechanics. Canonical law should refer to family-law permission, constitutive anchors, conservation, and governed movement—not make B-anchor the foundational public semantic object. |
| 5.4 family selection | 801–809 | **COMPAT** | Dotted reducer/member lookup is compatibility syntax. Canonical form uses family law or ordered expression. |
| 5.5 order specification | 810–823 | **REWRITE COMPLETELY UNDER O1** | Retire “natural order” authority. Canonical meaning carries peer domain, order, direction, ties, window/offset as relevant. Short form only via unique governed completion. |
| 5.6 many-to-many / faces | 824 onward | **AUDIT / KEEP CORE LAW** | The analytical distinction is valuable and orthogonal to expression vNext. Preserve until relationship-crossing authority is separately reconciled. Do not let current Core serialization define shared meaning. |
| coverage / restrictions material | later Ch.5 | **AUDIT** | Keep outside expression rewrite. Reconcile with revised standing where terminology overlaps. |

---

# 8. Chapter 6 — Examples

Examples should be regenerated **after** language-law migration, not manually patched one at a time.

| Current example class | Action | Target |
|---|---|---|
| Simple family aggregation | **REWRITE** | Teach governed named family + explicit family law equivalence. |
| Multiple measures at shared anchor | **KEEP / UPDATE** | Replace unruled `count(*)` with explicit `count(I)`-style surface once grammar is ruled. |
| Composite `max(sum(...))` | **KEEP / REFRAME** | Family-forming nested laws and constitutive anchors. |
| Ratio/share across grains | **KEEP / REFRAME** | General anchorable expression + anchoring/broadcast. |
| Bracket filter | **RETIRE** | Remove. |
| `WHERE`, `HAVING`, top-N | **KEEP** | Frame semantics. |
| first/last / scans | **REWRITE** | Ordered-expression contract and compatibility shorthand. |
| YTD/YoY | **REWRITE** | Ordered-expression/window/reset semantics; no “natural order” inference. |
| macros | **KEEP** | Query-local textual reuse only. |
| composite input anchors | **KEEP / REFRAME** | Constitutive inner-anchor identity. |
| availability labels inside examples | **MOVE** | Profiles/build status should provide measured availability. |

---

# 9. Chapter 7 — Outcomes, Disclosures, Clarifications

The structure is valuable, but it must be separated from standing semantics and wire implementation.

| Current section | Action | vNext treatment |
|---|---|---|
| 7.1 `(result, annotation)` concept | **KEEP / SPLIT** | Keep language-level explainability contract if desired; move exact field schema/versioned wire mechanics to wire/profile authority. |
| 7.2 serve/disclose/clarify/refuse taxonomy | **KEEP / AUDIT** | Preserve as language dispositions. Ensure revised standing/placement failures land in the right jurisdiction rather than being called generic “missing anchor.” |
| 7.3 language-invalid vs analytical refusal vs realization failure | **KEEP STRONGLY** | This distinction aligns directly with vNext staged jurisdiction. |
| 7.4 zero/one/many lawful readings | **KEEP STRONGLY** | This is one of the best existing pieces and should become central to canonicalization. |
| `input_anchor_ambiguous` | **KEEP / RENAME EXPLANATION** | Request determinacy failure, not missing data. |
| `order_axis_ambiguous` / `order_not_governed` | **KEEP / REFRAME** | Directly supports O1: many completions clarify; zero refuse. |
| exact shipped reason codes | **MOVE / COMPAT** | Keep compatibility appendix/profile unless canonical language intentionally promises codes. |
| Φ absence disclosures | **REWRITE HEAVILY** | Replace old four-way carrier/fill interpretation as semantic ontology with existence/placement/eligibility/support/value. Current Φ mappings become compatibility/realization migration material. |
| four-party control model | **AUDIT** | Valuable governance architecture, but outside the core expression rewrite. Check against current positive-admission serving and wire contracts separately. |

### Important standing additions

The new outcome examples must distinguish:

```text
input anchor omitted
    → request under-specification / Clarify

anchor not governed
    → language/geometry invalidity or analytical refusal, depending surface

point existence unsupported
    → upstream support-standing failure

point exists, placement under A unsupported
    → anchored-result support defect

measure eligible but unsupported
    → missing(E)
```

Never collapse these under one “missing anchor” phrase.

---

# 10. Chapter 8 — Sugar and Extensions

| Current section | Action | vNext treatment |
|---|---|---|
| 8.1 surface sugar principle | **KEEP** | Surfaces may generate canonical Frame-QL; no new semantics. |
| 8.2 operator aliases | **AUDIT / REWRITE** | A governed alias may resolve to existing canonical family law/capability; aliasing must not mint new analytical identity. |
| 8.3 implicit surface `AT`, `FROM`, NL translation | **KEEP AS SURFACE GUIDANCE** | Keep clearly outside formal language. |
| pipeline rendering | **KEEP AS PRESENTATION** | Do not make it semantic syntax unless separately ruled. |

---

# 11. Appendix A — Capability Reference

This section is generated and should **not** be hand-edited.

## Current problem

The current canonical registry groups capabilities as:

```text
reducers
maps
predicate position
scans
```

That classification mixes semantic standing with implementation routing.

## vNext target

A registry schema should separate:

```text
capability identity
semantic class
surface position
canonical standing
profile realization
build realization
```

Semantic classes should be able to represent:

```text
family-forming law
pointwise/value operation
standing predicate
ordered expression
frame operation
```

### Specific migrations

| Capability | Current | Target |
|---|---|---|
| `first`, `last` | ratified reducer | ratified ordered expression |
| `lag`, `lead`, cumulative, rolling, rank | proposed scan | proposed ordered expression unless separately ratified |
| `is_missing` | proposed map | proposed standing predicate |
| `is_null` | proposed map | remove from canonical analytical registry unless carrier inspection is separately ruled |
| `coalesce` | proposed map | suspend/remove generic meaning until governed completion semantics are ruled |
| `sum`, `count`, `min`, `max`, `mean` | reducers | family-forming analytical laws where ToD v7 contract applies |
| arithmetic `+ - * /` | maps | pointwise/general anchorable operations |

Do not change capability IDs solely because semantic category changes.

---

# 12. Appendix B — Reserved Keywords

| Current item | Action |
|---|---|
| envelope keywords | **KEEP** |
| `@`, `AT`, anchor products | **KEEP / EDIT EXPLANATION** |
| bracket-filter `[...]` roadmap reservation | **RETIRE** |
| ordered-expression parameter words | **AUDIT AFTER GRAMMAR RULING** |
| definition-language `ON` boundary | **KEEP** |
| future allocation/composition keywords | **AUDIT SEPARATELY** |

`[]` should now be reserved for semantic-value subscription even if no current profile realizes a subscriptable type.

---

# 13. Appendix C — SQL-speaker contrasts

Preserve the appendix, but update two items.

1. “No GROUP BY; output anchor declares location” survives.
2. `WHERE` versus output frame survives.
3. “No joins” should be phrased as **no requester-authored physical joins**; governed crossings/relationships remain separate law.
4. Any current claim that `SUM` may silently rescale based on old missingness defaults must be audited against the new standing/completion model before publication.
5. Alias vs macro distinction survives.

---

# 14. Appendix D — Retired terse `@` fragment

**KEEP.**

The historical reason for separating inner `@` from final `AT` remains useful.

Update only the statement that dotted member addressing is something the envelope “absorbed” as a canonical conceptual mechanism:

```text
level.last
```

should now be explicitly labeled a compatibility spelling whose vNext semantic home is ordered expressions.

---

# 15. New material with no adequate current home

The vNext Manual needs several sections the present Manual does not contain cleanly.

## A. Expression sorts

```text
family reference
measure expression
general anchorable expression
tuple expression
family-forming analytical expression
ordered analytical expression
standing expression
frame expression
```

## B. Semantic value layer

```text
qualified governed names
typed value attributes
typed value methods
value subscription
```

## C. Standing architecture

```text
point existence
anchor placement
measure eligibility
measure support
semantic value
```

including unsupported eligibility and the lost-record acceptance cases.

## D. Manifold promotion boundary

```text
AS alias ≠ family
WITH macro ≠ family
query expression ≠ durable governed object
```

## E. Family-forming law contract

Explicit tie to ToD v7:

```text
constitutive inner anchors
co-participation
sufficient-state basis
type capabilities
family identity
```

---

# 16. Proposed edit order

Do not edit the current Manual from top to bottom.

Use dependency order:

```text
1. Preface / authority seam
2. Expression sorts
3. Families, measures, anchoring
4. Pointwise + tuple + co-participation
5. Family-forming laws
6. Semantic values
7. Standing architecture
8. Ordered expressions
9. Canonicalization / compatibility
10. Frame clauses
11. Outcomes / validity / realization
12. Capability registry / generated appendix
13. Examples
14. SQL-speaker appendix
15. history / compatibility appendix
```

This avoids rewriting examples and outcome tables twice.

---

# 17. Repository-edit stop-gates

Before any repository changes, require two things.

## Gate M1 — semantic review

Review the consolidated vNext language-law candidate and this migration matrix together.

Question:

> **Does the target language preserve every useful shipped distinction while correcting the old ontology?**

## Gate M2 — implementation reconnaissance

Only after M1, ask CC to inspect:

```text
frameql_capabilities.toml
profile TOMLs
capability-table generator
parser/operator registry
canonicalizer
planner reason taxonomy
fill/absence representation
docs conformance tests
```

and return:

```text
schema coupling
minimal migration options
compatibility hazards
tests that encode old semantics
recommended sequence
```

No edits during reconnaissance.

---

# 18. Current conclusion

The Manual rewrite is now bounded.

There is no need to invent a new query language.

There is no need to throw away the envelope.

There is no need to break current capability IDs.

The central migration is:

```text
old:
column/member + reducer/map/scan + Φ

new:
family/measure/expression sorts
+ family-forming law
+ semantic-value layer
+ ordered-expression contract
+ explicit standing layers
```

with the existing frame, clarification, governance, and execution boundaries preserved wherever they remain valid.

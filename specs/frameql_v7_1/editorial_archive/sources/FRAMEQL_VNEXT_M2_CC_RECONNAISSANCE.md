# M2 Instruction to andFam / CC — Frame-QL vNext Reconciliation Reconnaissance

**Mission:** Frame-QL vNext M2 reconciliation reconnaissance  
**Authority posture:** reconnaissance only  
**Do not edit code, specs, docs, profiles, generated tables, or tests. Do not open a PR.**

We have completed the semantic design and the first Manual-reconciliation pass for Frame-QL vNext. Your job in this mission is **not** to implement the design. It is to inspect the current repositories and tell us the smallest safe migration from the current shipped/canonical structures to the attached target.

Our collaboration rule remains:

> **We decide what must remain true. You decide the cleanest way to make it true.**

For this mission, stop before “make it true.” Bring back the implementation evidence and your recommended migration.

---

# 1. Read order

Read the attached documents in this order:

1. `frameql_language_vnext_working_draft_v0_3.md`
   - consolidated semantic target;
   - not yet the shipped Manual.

2. `frameql_vnext_current_manual_migration_matrix_v0_1.md`
   - clause-by-clause classification of the current public Manual;
   - distinguishes keep / rewrite / compatibility / retire / move / audit.

3. `frameql_vnext_m1_semantic_review_v0_1.md`
   - records the semantic review and the two recovered existing capabilities:
     broadcast as structural alignment, and `WHERE` as analytical restriction.

4. `frameql_vnext_r4_standing_amendment_v0_2.md`
   - authoritative working refinement for point existence, anchor placement, eligibility, support, and missingness.

5. `frameql_vnext_o1_ordered_expression_compatibility_ruling_v0_1.md`
   - ordered-expression semantic/compatibility ruling.

6. `frameql_vnext_capability_profile_reconciliation_plan_v0_1.md`
   - intended authority split and registry/profile migration constraints.

7. `frameql_vnext_authority_reconciliation_v0_1.md`
   - context for preserving the repository's current four-authority documentation architecture.

Then inspect current `main` directly. Treat the repository as current-state evidence; do not assume the attached documents describe implementation reality.

---

# 2. What is settled

Do not reopen these unless current implementation evidence reveals an actual contradiction that makes the target impossible.

## 2.1 Authority separation

Preserve:

```text
canonical Frame-QL language law
        ↓
canonical capability authority
        ↓
Core / Platform profile promises
        ↓
measured build status
```

A build does not define language law.

A profile does not define language law.

Generated build status must remain measured rather than hand-authored.

## 2.2 Expression architecture

Canonical Frame-QL distinguishes at least:

```text
family reference
measure expression
general anchorable expression
tuple expression
family-forming analytical expression
ordered analytical expression
predicate / standing expression
semantic-value access expression
```

Envelope clauses are request operations, not expression sorts.

## 2.3 `@` and `AT`

```text
E @ A
    expression-level analytical anchoring

AT A
    the unique final output anchoring of the frame
```

Do not restore the old claim that one measure has two current anchors.

Constitutive inner anchors may remain part of constructed family identity.

## 2.4 Broadcast

Broadcast survives.

It is **structural expression alignment**, not family establishment.

A coarse value may be replicated to participate in a finer outer expression without asserting that the coarse family now has a finer measure.

Replicate is not allocation.

## 2.5 Pointwise / multi-input semantics

Joint use requires governed co-participation.

Physical co-location or a join does not establish the analytical pair.

## 2.6 Family-forming laws

Forms such as:

```text
sum(x @ I)
mean(x @ I)
variance(x @ I)
covariance(x @ I, y @ I)
count(I)
count(x @ I)
```

have family standing only under the admitted ToD analytical-law contract.

General arithmetic does not mint family identity.

`count(I)` and `count(x @ I)` are analytically distinct.

## 2.7 Dot

Canonical dot roles:

```text
governed qualified/faced name
typed semantic-value member/method access
```

Historical:

```text
revenue.sum
level.last
```

may remain compatibility syntax where they uniquely normalize, but they do not define the conceptual grammar.

## 2.8 Brackets

Retire roadmap analytical bracket filtering.

```text
E[key]
```

is reserved semantically for value subscription.

Do not preserve `E[predicate]` analytical filtering merely because parser scaffolding exists.

## 2.9 `WHERE`

`WHERE` is request-local **analytical restriction** applied before affected expressions are formed.

It is not merely output frame shaping.

It does not automatically carve a new universe.

`HAVING` is output selection.

`ORDER BY` / `LIMIT` are output-frame ordering/selection.

## 2.10 Ordered expressions

`first`, `last`, `lag`, `lead`, cumulative, rolling, rank, etc. belong to the ordered-expression layer.

`first` / `last` are no longer canonically measure-family reducers merely because the current registry calls them reducers.

O1-A is settled:

> Canonical meaning has a determinate order contract. Legacy shorthand may omit fields only when governance supplies exactly one mechanical completion, and canonicalization exposes the completed contract.

No physical row-order inference.

No `ORDER BY` inheritance.

No “time exists, therefore chronology” inference.

Direction and ties are meaning-bearing where they affect the result.

## 2.11 Standing

The semantic dependency is:

```text
universe existence law
    ↓
point-existence standing
    ↓
placement under the required anchor
    ↓
measure eligibility
    ↓
measure support
    ↓
semantic value
```

Distinguish:

```text
point nonexistent
point existence unsupported
point exists but placement under A unsupported
eligibility unsupported
ineligible
eligible but unsupported = missing
supported value, including zero
```

Do not flatten these into SQL NULL / carrier missingness.

The working term `anchor-placement standing` is not required as final public vocabulary. The distinction is required.

## 2.12 Promotion

```text
AS alias
WITH macro
saved query
```

do not mint durable analytical identity.

Promotion belongs to governed Manifold authoring.

A named reusable ordered expression need not become a measure family.

## 2.13 Platform

Do not invent Platform-only Frame-QL merely because Platform has a different runtime mission.

Current `Platform extends Core; adds = []` is acceptable unless a genuine language requirement proves otherwise.

---

# 3. Reconnaissance questions

Please answer these from the current repos, with file/symbol/test references.

## A. Current repository state

Report:

```text
repo(s) inspected
main HEAD(s)
relevant package versions
whether the four Frame-QL authorities are still current
uncommitted/local state if relevant
```

If current main has materially changed since the public state represented in the attached matrix, say so first.

## B. Capability authority coupling

Inspect at least:

```text
specs/frameql_capabilities.toml
specs/profiles/core_profile.toml
specs/profiles/platform_profile.toml
docs/tools/regen_capability_tables.py
all validators/tests that enforce the schema
all runtime code that reads or mirrors these categories
```

Determine:

1. What depends on `category = reducer | scan | map`?
2. Is `category` used only for generated documentation, or for parser/planner/runtime routing too?
3. What depends on `position = series | predicate`?
4. What depends on `re_entry_certified`?
5. Can semantic classification be separated from realization/routing without duplicating authority?
6. What is the smallest schema evolution you recommend?
7. Can capability IDs remain stable for `first`, `last`, scans, and current maps?
8. What generator/test changes would necessarily follow?

Do not change the schema.

Bring back options and your recommendation.

## C. Parser / expression grammar coupling

Trace current treatment of:

```text
revenue.sum
level.last
E.member
E.method(...)
E[key]
E[predicate]
sum(E @ A)
multi-input functions
tuples
first / last
scan parameters
explicit `by =`
@ / AT
```

Report:

- what the parser accepts;
- what is grammar-recognized but planner-refused;
- what normalizes before planning;
- what semantics are encoded directly in parser shape;
- where dotted family/member assumptions are baked in;
- whether `[]` can be reassigned to value subscription without syntax ambiguity;
- whether a tuple form currently conflicts with another grammar production.

No grammar edits.

## D. Canonicalizer coupling

Find every place canonical form currently assumes:

```text
reducer atom
map expression
scan
default reducer
family member
input pin
fill rule
natural/derived order
```

For each, state whether vNext requires:

```text
rename/reclassification only
semantic data model change
new canonical field
compatibility normalization
no change
```

Especially inspect whether canonical form can expose a completed ordered-expression contract without requiring new surface syntax immediately.

## E. Planner / adjudication coupling

Trace current code for:

```text
input_anchor_ambiguous
input_anchor_unavailable
redundant_pin
pin_coarser_than_output
order_axis_ambiguous
order_not_governed
broadcast
cross_universe
filter reachability
family/member selection
blocked reduction
standing / fill / support
```

Answer:

1. Is the current zero/one/many-reading logic centralized enough to become the general canonical-resolution rule?
2. Where does current order-axis derivation obtain its authority?
3. Can the planner distinguish “one governed order completion” from “natural time order” without new Manifold data?
4. What current structure represents broadcast, and does it already preserve the coarse operand's analytical identity?
5. Where does `WHERE` restriction enter the plan, and does anything currently treat it as universe carve?
6. Which current reasons would be semantically wrong under the new standing model?

Do not alter reason codes.

## F. Standing / fill representation

This is a high-value part of the reconnaissance.

Trace current representations for:

```text
universe point existence
event/spine basis
fill rule Phi
zero
unknown
undefined
eligibility
support
missing cells
no-data
coverage
coordinate/anchor realization
```

Then map current facts to the target layers:

| Target layer | Current representation(s) | Faithful? | Gap? |
|---|---|---:|---:|
| point existence | | | |
| point-existence support | | | |
| anchor placement | | | |
| placement support | | | |
| eligibility | | | |
| eligibility support | | | |
| measure support | | | |
| semantic value | | | |
| carrier null | | | |

Use the lost-record acceptance cases from R4 as tests of representational sufficiency.

Do **not** invent new enums to make the table complete.

If current architecture cannot represent a distinction, say so.

## G. Restriction / carve / `WHERE`

Inspect whether current `WHERE`:

- preserves the source universe/reference population;
- changes coverage/support metadata;
- silently shrinks denominators;
- creates any named population object;
- is implemented per-series as documented;
- interacts with missing/fill policy in ways the vNext standing model must account for.

If current behavior conflates restriction and carve, flag it as an architectural issue rather than fixing it.

## H. Family laws and multi-input formation

Trace what would be required for canonical forms such as:

```text
mean(revenue @ order)
variance(price @ transaction)
covariance(price @ order, quantity @ order)
(revenue, cost) @ order
```

Separate:

```text
language grammar
canonical identity
Manifold law/admission
co-participation
planner capability
engine realization
```

We are **not** asking you to implement multi-input statistics now.

We want to know which seams already exist and which do not.

## I. Ordered expressions

Trace:

```text
first
last
lag
lead
cumsum
rolling_*
rank
```

Report whether one shared ordered-expression semantic descriptor could cover them without forcing one implementation mechanism.

Specifically identify current representations for:

```text
peer domain
order axis/key
direction
tie rule
window
offset
reset/within/step
```

Call out missing fields.

Do not invent the final syntax.

## J. Manifold authoring implications

Inspect shared/publication authoring and, where necessary, Studio/manifold-agent private repos.

We need to know whether current authored/publication structures can represent:

```text
canonical family identity formed by analytical law
constitutive inner anchor
governed default completion
semantic type capabilities
standing distinctions
governed default order / ordered-expression completion
named non-family expression
```

Do not add fields.

If one of these belongs in a different authority than the Manifold, recommend that instead.

## K. Wire and outcome coupling

Inspect current wire/output contracts for assumptions about:

```text
fill rule
NULL
missing
input anchor
order
canonical form
reason codes
annotation fields
```

Identify which changes would be semantic additions versus wire-version changes.

No wire changes.

## L. Test coupling

Find tests that would fail if we merely changed canonical semantic categories while leaving current runtime behavior intact.

Classify them:

```text
semantic-law pin
profile-contract pin
build-measurement pin
implementation-detail pin
historical compatibility pin
```

This is important: do not "fix" a semantic-law test by changing runtime behavior until we know which authority it was intended to protect.

---

# 4. Required deliverable

Bring back one report, no code.

Use this structure.

## 1. Executive conclusion

Tell us whether the vNext target can be reconciled with the current implementation incrementally, or whether any part requires a deeper architectural replacement.

## 2. Verified current state

Main heads, relevant packages, authorities, changed facts since the attached matrix.

## 3. Coupling map

A compact diagram of:

```text
language authority
    ↓
capability schema
    ↓
profile generation
    ↓
parser/canonicalizer/planner
    ↓
engine
    ↓
wire/build status
```

show where the current categories are actually consumed.

## 4. Semantic mismatch matrix

For each material mismatch:

| Area | Current behavior/model | vNext target | Jurisdiction | Migration size | Compatibility risk |
|---|---|---|---|---|---|

At minimum cover:

```text
dot
brackets
family laws
first/last
scans
broadcast
WHERE restriction
standing/fill
promotion
capability taxonomy
```

## 5. Recommended migration sequence

Give us the smallest coherent sequence.

Prefer independently reviewable slices.

State dependencies and stop-gates.

## 6. Schema options

Where a schema must change, give 2–3 viable options only if the trade-off is real.

Recommend one.

Do not manufacture alternatives for their own sake.

## 7. Compatibility strategy

Tell us what can remain accepted unchanged, what needs canonical re-normalization, and what is unshipped and can simply be retired.

## 8. Questions requiring our ruling

Only include questions that implementation evidence genuinely cannot settle.

For each:

```text
evidence
why code cannot decide it
available choices
your recommendation
```

## 9. Suggested first implementation slice

Recommend the first implementation/reconciliation slice we should authorize **after** reviewing your report.

Do not start it.

---

# 5. Constitutional invariants

Carry these throughout the reconnaissance:

> **Meaning first, realization second.**

> **A build may realize language; it does not define language.**

> **A profile may promise capability; it may not redefine capability.**

> **Mapping realizes meaning; it does not create it.**

> **Declaration is not certification.**

> **Positive admission authorizes execution.**

> **The planner chooses the lawful operation. The engine performs it.**

> **Internal value structure is not analytical location.**

> **Computability does not create family identity.**

> **A missing carrier value does not determine analytical standing.**

> **Broadcast makes a coarse value available; it does not manufacture a finer measure.**

> **Restriction does not silently become population carve.**

> **Canonical ordered meaning may be completed by governance; it may not be guessed from physical order or familiarity.**

> **Two physical runtimes are acceptable. Two meanings of a measure are not.**

---

# 6. Stop condition

Stop after the reconnaissance report.

Do not:

```text
edit the canonical capability schema
change categories
change standing
change Core/Profile promises
change parser grammar
change canonicalization
change planner reasons
change fill semantics
add standing enums
change wire version
rewrite docs
open a PR
```

If you discover that an apparently simple reconciliation would force one of those changes, that is exactly the evidence we need you to bring back.

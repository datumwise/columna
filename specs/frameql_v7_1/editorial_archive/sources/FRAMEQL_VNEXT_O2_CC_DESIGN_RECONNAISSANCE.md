# O2 Instruction to andFam / CC — Ordered-Expression Successor Design Reconnaissance

**Mission:** Frame-QL vNext O2 ordered-expression design reconnaissance  
**Authority posture:** reconnaissance only  
**Do not implement. Do not edit parser, planner, runtime registry, capability specs, profiles, Manifold schema, wire, docs, or tests. Do not open a PR.**

We have completed the semantic design pass for the successor ordered-expression layer.

Your task is to inspect current `main` and tell us the smallest clean implementation architecture that can realize the attached semantic target **without routing the design through legacy family-founding FIRST/LAST**.

Our collaboration rule remains:

> **We decide what must remain true. You decide the cleanest way to make it true.**

For this mission, stop before implementation.

---

# 1. Read order

Read:

1. `frameql_vnext_o2_ordered_expression_semantic_architecture_v0_2.md`
   - authoritative working O2 semantic target.

2. `frameql_vnext_r4_standing_amendment_v0_2.md`
   - point existence / placement / eligibility / support distinctions that ordered-domain standing must respect.

3. `frameql_vnext_o1_ordered_expression_compatibility_ruling_v0_1.md`
   - O1 canonical-order and shorthand ruling.

4. `frameql_language_vnext_working_draft_v0_3.md`
   - broader vNext language context.

5. `frameql_vnext_m1_semantic_review_v0_1.md`
   - preserves broadcast, WHERE restriction, and zero/one/many resolution discipline.

Then inspect current `main` directly.

Treat current code as implementation evidence, not semantic authority.

---

# 2. Successor semantics that are settled

Do not reopen these unless current evidence reveals a genuine impossibility.

## 2.1 Ordered expressions are a separate language layer

Examples:

```text
FIRST
LAST
LAG
LEAD
RANK
DENSE_RANK
ROW_NUMBER
cumulative operations
rolling operations
```

They do not become ToD measure families merely because they return values.

## 2.2 Minimal common structure

The semantic target is:

```text
Ordered Expression
    = operand
    + governed ordered domain
    + operator law
```

with the ordered domain containing:

```text
sequence anchor I
peer anchor P
projection I -> P
governed order specification
domain-formation rule
```

and the operator law determining:

```text
required order strength
selection / neighborhood semantics
result locus
operand-standing behavior
boundary / exceptional cases
meaning-bearing parameters
```

## 2.3 Sequence anchor and peer anchor are different roles

Example:

```text
balance @ {account, day}

sequence anchor = {account, day}
peer anchor     = {account}
order           = day chronology within account
```

Do not reduce this to “order by day.”

The ordered objects are complete analytical points at the sequence anchor.

## 2.4 Peer domains come from governed anchor geometry

Foundational vNext uses:

```text
I >= P
```

so each sequence point belongs to exactly one peer fiber.

Do not introduce arbitrary SQL-style partition sets as semantic authority.

If a desired grouping is not a partition, it first needs lawful analytical structure.

## 2.5 Order is a governed relation, not fundamentally key + direction fields

Surface syntax may later use:

```text
by=day ASC
```

but canonical semantics require the governed order relation (or an equivalent resolved specification).

Direction is part of that meaning where reversal changes the result.

## 2.6 Order strength is operator-relative

Examples:

```text
RANK
    may admit tied order classes

ROW_NUMBER
    requires unique positions

LAST
    requires a unique terminal point or governed selector

LAG
    requires determinate relative positions
```

Do not invent one universal tie-policy enum merely to unify implementation.

## 2.7 Result locus is operator-specific

Peer-collapsing:

```text
FIRST / LAST
    result at peer anchor P
```

Focal-preserving:

```text
LAG / LEAD / RANK / cumulative / rolling
    result at sequence anchor I
```

FIRST/LAST landing at a coarser peer anchor does **not** make them ToD reducers.

## 2.8 Participation / support cannot be silently collapsed

Distinguish:

```text
candidate point participation
peer placement standing
order-key standing
operand support
```

An eligible point with unsupported order key or peer placement may not silently disappear from the sequence.

An unsupported operand at a selected/predecessor point is not automatically skipped.

“Last value” and “last supported value” are different operators.

## 2.9 Windows are neighborhood laws

Distinguish:

```text
previous 7 points
previous 7 days
```

Positional windows and order-value range windows are different semantic objects.

## 2.10 WHERE and ORDER BY

```text
WHERE
    restricts the ordered input domain before expression formation

ORDER BY
    orders the returned frame only
```

Output `ORDER BY` never completes an inner ordered-expression contract.

## 2.11 No automatic continuation rights

An ordered expression can be materialized or reused without acquiring ToD family continuation law.

Availability is not continuation permission.

## 2.12 Legacy bonus boundary

Ignore as successor-design constraints:

```text
FAMILY { last ORDER ... }
legacy first/last family founding
old reducer classification
```

These are provisionally retirement-candidate bonus features.

Do not build a migration bridge unless you find evidence of a genuine public compatibility obligation.

The existence of code/tests/fixtures alone does not prove such an obligation.

---

# 3. Questions for reconnaissance

Please answer from current code with file/symbol/test references.

## A. Existing internal representation

Trace how current Core represents or plans:

```text
first
last
lag
lead
cumsum
cummax
cummin
pct_change
rolling_sum
rolling_mean
rank / row-number-like behavior if present
```

For each, identify where current code carries:

```text
operand
input/sequence anchor
peer/partition domain
order axis/key
direction
tie behavior
window kind
window extent
offset
reset/within semantics
result anchor/locus
missing/unsupported operand behavior
```

Use “not represented” where appropriate.

Do not invent missing fields.

## B. Common descriptor feasibility

Can one successor semantic descriptor represent all of these operations while allowing distinct execution paths?

We are looking for something conceptually equivalent to:

```text
OrderedDomainSpec
OrderedOperatorSpec
ResolvedOrderedExpression
```

Names are not prescribed.

Tell us:

- what fields are truly common;
- what belongs in operator-specific descriptors;
- what should remain planner/runtime derived;
- whether one descriptor would simplify or distort current implementation.

Prefer composition over one giant parameter bag.

## C. Sequence anchor and peer anchor

Can current anchor/planner structures already represent:

```text
sequence anchor I
peer anchor P
I >= P projection
```

without adding a new geometry concept?

Inspect whether current “order axis,” output anchor, partition keys, or scan-within structures can be cleanly reused.

Flag any place where current implementation confuses:

```text
order coordinate
sequence anchor
peer anchor
output anchor
```

## D. Peer-domain surface

Without choosing final syntax, assess whether current grammar could eventually express the peer anchor through an existing structural form or whether a dedicated `within`-like surface is likely necessary.

Do not propose syntax merely because SQL has `PARTITION BY`.

Give 1–2 genuinely viable approaches only if there is a real trade-off.

## E. Canonical resolved artifact

O1 says governed shorthand may be short, but resolved canonical meaning must expose the completed order contract.

M2 suggested the resolved/EXPLAIN path may be a better home than `render_canonical()`.

Inspect current structures and tell us the smallest clean place for a `ResolvedOrderedExpression`-like artifact carrying:

```text
sequence anchor
peer anchor
order relation/spec
operator law identity
operator parameters
result locus
```

We do not want to destroy parse/render round-trip merely to serialize semantic completion into surface text.

## F. Order relation representation

Inspect current order-axis / type / hierarchy structures.

Can current governed data distinguish:

```text
chronological day ascending
chronological day descending
revenue descending
(event_time, transaction_id) lexicographic
```

If not, identify exactly what is missing.

Do not preserve “natural order” as canonical authority.

Tell us whether the missing authority belongs in:

```text
Manifold logical declaration
Frame-QL request/resolved expression
CDT comparison capability
another existing authority
```

or a combination.

## G. Ties / order strength

Trace current behavior for tied order keys in DuckDB, Polars, planner tests, and any canonicalizer logic.

Map current behavior against operator needs:

| Operation | Needed order strength | Current representation | Current deterministic? | Governed? |
|---|---|---|---:|---:|
| LAST | unique terminal or selector | | | |
| LAG | unique relative positions | | | |
| RANK | tie classes allowed | | | |
| ROW_NUMBER | unique positions | | | |
| rolling positional | positional sequence | | | |
| rolling range | value-order boundary | | | |

If an operation is not implemented, say so.

## H. Participation / standing

Use R4 semantics.

Trace what current Core does if an otherwise participating point has:

```text
unsupported peer coordinate
unsupported order key
unsupported operand value
NULL carrier key
NULL carrier operand
```

We need to know where successor ordered semantics can be implemented before full R4, and where exact semantics are blocked by missing standing representation.

Do not broaden R4-C0.

## I. FIRST/LAST result locus

Inspect whether current planner/runtime can produce one value at peer anchor P from values at sequence anchor I without routing through family-founding machinery.

We are explicitly asking whether a **general ordered-expression result** can land at a coarser peer anchor independently of reducer/family standing.

If no such seam exists, identify the smallest missing abstraction.

Do not solve it using legacy family founding.

## J. Focal-preserving result locus

Inspect whether scans already provide a reusable seam for:

```text
result at sequence/focal anchor I
peer context P
```

Tell us which parts can be reused semantically and which are merely execution mechanics.

## K. Neighborhood laws

Trace current rolling/cumulative representations.

Can they distinguish:

```text
positional window
order-value range window
boundary inclusion
current-point inclusion
offset
```

If current support only implements a subset, state exactly which subset.

Do not generalize current implementation into canonical language law.

## L. Named reusable ordered expressions

Inspect current authored/publication/Manifold structures for the cleanest future home of a durable governed non-family expression.

We are **not** authorizing a new object class.

Tell us whether:

```text
existing derived expression machinery
logical declarations
publication artifact
another current layer
```

could host this cleanly, or whether a genuinely new authoring object would be required.

Legacy `FAMILY { last ... }` is not a candidate answer.

## M. Retirement evidence

Inspect legacy family-founding FIRST/LAST and related paths only to answer:

```text
Is this actually a public compatibility obligation,
or merely code/tests/fixtures/demo behavior?
```

Bring concrete evidence:

```text
public docs
published examples
Studio-generated artifacts
external API contract
persistent authored files
backward-compat promises
```

Do not count internal tests alone as compatibility evidence.

Do not retire anything in this mission.

---

# 4. Required deliverable

Bring back one report, no code.

Use this structure.

## 1. Executive conclusion

Can the O2 semantic model be implemented cleanly on current architecture, or does it require a new core expression abstraction?

## 2. Current ordered implementation map

A diagram showing parser → canonicalization → planner → resolved operation → engine for current FIRST/LAST and scans.

## 3. Semantic-field matrix

| O2 semantic field | Current carrier | Reusable? | Gap? | Recommended authority |
|---|---|---:|---:|---|

Cover at least:

```text
sequence anchor
peer anchor
peer projection
order relation
order keys
direction/order comparison
order strength/ties
domain-formation rule
operand-standing rule
selection/neighborhood law
result locus
offset/window/boundary
```

## 4. Recommended successor object model

Give the smallest clean internal semantic model.

Do not mirror the attached document mechanically if current architecture suggests a simpler faithful representation.

Explain why every field exists.

## 5. Operator mapping

Show how the model represents:

```text
FIRST
LAST
LAG
LEAD
RANK
DENSE_RANK
ROW_NUMBER
CUMSUM
rolling positional
rolling range
```

Mark unsupported future operations rather than pretending they already work.

## 6. Required authority additions

List any genuinely missing governed facts and where you recommend they live.

Separate:

```text
language semantic artifact
Manifold declaration
CDT capability
profile/runtime realization
```

## 7. Standing blockers

Tell us what can be implemented truthfully before full R4 and what cannot.

## 8. Legacy retirement evidence

Classify old FIRST/LAST family-founding as:

```text
bonus / retirement candidate
real compatibility obligation
uncertain
```

with evidence.

## 9. Suggested first ordered-expression implementation slice

Recommend one smallest slice to authorize after review.

Prefer a slice that proves the new expression abstraction without requiring legacy migration or full R4.

Do not start it.

## 10. Questions requiring our ruling

Only include questions that code evidence genuinely cannot settle.

For each:

```text
evidence
choices
recommendation
```

---

# 5. Invariants

Carry these throughout:

> **Order is over governed analytical points, not rows.**

> **The sequence anchor is the complete analytical point anchor; an order coordinate is not a substitute for it.**

> **Peer domains come from governed analytical geometry.**

> **The governed order must be strong enough for the result the operator claims.**

> **Missing order/peer standing may not silently shrink the sequence.**

> **A missing operand does not mean “skip this point” unless the operator law explicitly says so.**

> **FIRST/LAST can land at a coarser peer anchor without becoming measure-family reducers.**

> **Using SUM inside a cumulative/rolling neighborhood does not turn the whole ordered expression into a SUM family.**

> **Output ORDER BY never supplies inner order meaning.**

> **Availability is not continuation permission.**

> **Legacy bonus features do not constrain successor architecture.**

> **Do not invent syntax before semantic structure requires it.**

---

# 6. Stop condition

Stop after the design-reconnaissance report.

Do not:

```text
implement an OrderedExpression class
change FIRST/LAST
change scans
change parser grammar
change canonical form
change runtime Operator.kind
change capability taxonomy
change Manifold schema
add order/tie fields
change wire
change standing
retire legacy behavior
open a PR
```

If current architecture makes the semantic target impossible without one of those changes, report that fact and the smallest required abstraction.

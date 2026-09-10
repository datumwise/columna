# Frame-QL vNext — M1 Semantic Review

**Review 0.1 — 6 September 2026**  
**Reviewed:** `frameql_language_vnext_working_draft_v0_2.md` against Theory of Data v7, the inherited Contract Calculus restriction/carve distinction, and current shipped Frame-QL language behavior.  
**Purpose:** Determine whether the vNext target accidentally drops useful existing semantics before any repository reconciliation.  
**Result:** **PASS WITH TWO REQUIRED AMENDMENTS AND THREE NON-BLOCKING CLEANUPS.**

---

# 0. Review conclusion

The vNext semantic direction holds.

No foundational ruling needs to be reopened.

Two useful existing semantics were compressed too far in Working Draft 0.2:

1. **broadcast / coarse-to-fine expression alignment**;
2. **`WHERE` as analytical restriction rather than generic frame shaping**.

Both can be restored without adding a new ToD primitive.

Three smaller cleanups are also required:

3. distinguish expression sorts from envelope/request operations;
4. keep output alias identity separate from analytical identity everywhere, including compatibility prose;
5. preserve the current zero/one/many lawful-reading discipline as canonical adjudication rather than leaving it only in the outcome chapter.

After these amendments, M1 can close.

---

# 1. Required amendment M1-A — broadcast is alignment, not family establishment

## Problem in Working Draft 0.2

The draft says, correctly, that:

```text
F @ A
```

denotes family `F` at current anchor `A` where that measure is lawfully established.

It also says ordinary pointwise anchoring distributes over operands when they can be co-established at the requested anchor.

What it does not yet explain is the existing lawful pattern:

```frameql
SELECT
    (revenue @ {customer}) / (revenue @ {}) AS share
AT {customer}
```

The denominator is a scalar measure at `{}`.

The outer expression needs that scalar value available at each customer point.

Current Frame-QL calls this **broadcast** and correctly gives it replicate-only semantics.

If the vNext account simply rewrites the denominator as:

```text
revenue @ {customer}
```

it would claim a different analytical object.

That is wrong.

## Ruling

Preserve broadcast as a **structural expression-alignment operation**.

If expression `E` is established at coarser anchor `B` and an outer expression is evaluated at finer anchor `A`, a governed broadcast may make the value of `E@B` available at the `A` points required by that outer expression.

This does **not** establish:

```text
F @ A
```

for family `F` merely by replication.

It establishes only the availability of the coarser expression's value for the enclosing computation.

Thus:

```text
Revenue @ {}
```

remains a scalar Revenue measure.

Broadcasting its value into a customer-level ratio does not turn it into:

```text
Revenue @ customer
```

## Consequences

Broadcast:

- is replicate-only;
- does not distribute a total;
- does not create a new family measure at the finer anchor;
- is governed by the structural relation required to align the expression;
- can carry downstream conservation/reaggregation restrictions;
- belongs to expression alignment / structural semantics, not family formation.

## Canonical pointwise rule

The simple distributive form:

```text
(E1 ★ E2) @ A
    =
(E1 @ A) ★ (E2 @ A)
```

should be stated only for operands directly lawfully establishable at `A`.

The more general pointwise rule is:

> **Every operand must be lawfully available for participation at the evaluation anchor, either because it is established there or because a governed structural alignment such as broadcast makes its already-established value available there without changing its analytical identity.**

---

# 2. Required amendment M1-B — `WHERE` is analytical restriction

## Problem in Working Draft 0.2

The draft groups:

```text
WHERE
HAVING
ORDER BY
LIMIT
LIMIT ... PER
```

as frame operations.

That is too coarse.

Current Frame-QL correctly distinguishes:

```text
WHERE
    restricts input before selected expressions are formed

HAVING
    selects output after expressions are formed

ORDER BY / LIMIT
    order and select the returned frame
```

The distinction is analytically meaningful because `WHERE` can change which points contribute to a family-forming law.

## Existing theoretical support

The inherited Contract Calculus distinguishes:

```text
restriction
    select a subdomain while retaining the source universe/reference population

carve
    establish a new governed population/subuniverse
```

A physical predicate does not decide which one occurred.

Current Frame-QL `WHERE` is already described as request-local restriction:

```text
WHERE restricts the query's input;
the Manifold's declared coverage is unchanged.
```

That is compatible with **restriction**, not automatic carve.

## Ruling

The vNext language should distinguish three request-level operations:

### Analytical restriction

```text
WHERE
```

applies a governed predicate to the input participation/domain of the request before the affected analytical expressions are formed.

It can change values.

It does not, merely by appearing in a query:

- rewrite the Manifold universe;
- mint a new named subuniverse;
- promote a durable family;
- become part of the physical scan plan as user authority.

### Output selection

```text
HAVING
```

selects already-formed output points according to output expressions/coordinates.

### Frame ordering and limiting

```text
ORDER BY
LIMIT
LIMIT ... PER
```

order or select rows/points of the output frame.

They do not retroactively supply inner analytical order.

## Consequence for expression taxonomy

`WHERE` itself is an envelope/request operation.

Its predicate is a predicate expression.

Do not make `WHERE` an expression sort.

Likewise `HAVING`, `ORDER BY`, and `LIMIT` are clauses/request operations, not expression objects.

This keeps:

```text
expression grammar
```

separate from:

```text
request/frame grammar.
```

---

# 3. Cleanup M1-C — expression sorts versus request operations

Working Draft 0.2 currently lists a `frame expression` sort and then gives clause names as examples.

That blurs grammar levels.

## Revised expression sorts

Use:

```text
family reference
measure expression
general anchorable expression
tuple expression
family-forming analytical expression
ordered analytical expression
predicate / standing expression
semantic-value member/subscription expression
```

## Request/envelope operations

Separately:

```text
FROM
WITH
SELECT / AS
AT
WHERE
HAVING
ORDER BY
LIMIT / PER
EXPLAIN
```

Some clauses consume expressions.

The clauses are not thereby expression sorts.

---

# 4. Cleanup M1-D — output key is not analytical identity

The current shipped Manual sometimes says an output column's “identity” is its alias or canonical expression.

Under vNext this must be lexicalized more carefully.

Use:

```text
output key / frame column key
```

for:

```text
AS aov
canonical unaliased expression spelling
```

Reserve:

```text
analytical identity
```

for governed analytical identity.

Thus:

```text
AS aov
```

can change the output key without changing the analytical object denoted by the expression.

This is already reflected in the vNext promotion ruling; the clause-level migration must apply it consistently.

---

# 5. Cleanup M1-E — zero / one / many readings becomes canonical resolution law

The current Manual has an excellent rule:

```text
zero distinct lawful readings
    → Refuse

one distinct lawful reading
    → proceed

several distinct lawful readings
    → Clarify
```

with equivalence determined by governed law rather than current-data coincidence.

This should be promoted into the canonicalization/adjudication chapter rather than treated mainly as a list of current outcomes.

It applies naturally to:

```text
omitted constitutive input anchors
legacy dotted-family completion
ordered-expression default completion
ambiguous governed paths
```

The rule is one of Frame-QL's central semantic safety mechanisms.

---

# 6. Standing review — PASS

The revised R4 architecture survives review.

The important distinctions remain:

```text
point nonexistent
point existence unsupported
point exists but placement under A unsupported
measure eligibility unsupported
measure ineligible
measure eligible but unsupported = missing
supported value, including zero
```

The `count(I)` versus `count(x@I)` distinction in ToD v7 confirms that known point existence can retain analytical consequences even when a measure is unsupported.

No new ToD primitive is required for placement standing.

It is support for establishing the governed partition projection:

\[
\pi_A(\omega)=a.
\]

The final public term remains intentionally open.

---

# 7. Ordered-expression review — PASS

O1-A survives review.

Canonical meaning must determine:

```text
peer domain
order key(s)
direction/order relation
tie behavior
window/frame where relevant
offset/reset where relevant
```

Surface shorthand may omit fields only under one governed mechanical completion.

The current distinction:

```text
zero governed orders → refuse
several governed orders → clarify
```

is directly reusable.

The phrase **natural order** should be retired as canonical justification.

---

# 8. Family-forming-law review — PASS

The family/expression boundary remains sound:

```text
mean(revenue @ order)
    can denote a constructed family under admitted law

revenue / orders
    ordinary anchorable expression
    no durable family identity merely from syntax
```

The constitutive inner anchor remains identity-bearing.

Multi-input family laws use governed co-participation.

Rich values remain value domains, not anchors.

No change required.

---

# 9. Restriction caveat kept open

M1-B identifies `WHERE` as analytical restriction, but does not attempt to solve every restriction/carve question.

In particular, future expression-local restriction, named subpopulation construction, sampling restriction, and value-dependent carve may have different analytical contracts.

The current Frame-QL `WHERE` rule can remain narrow:

> **request-local restriction over the existing governed universe; it does not by itself create a new universe.**

That is sufficient for the language rewrite.

---

# 10. M1 verdict

After amendments M1-A through M1-E:

\[
\boxed{\text{M1 semantic review = PASS}}
\]

The vNext language-law candidate can then be treated as the semantic target for clause-by-clause Manual reconciliation.

The next gate becomes M2:

> **Ask CC to inspect current registry/parser/canonicalizer/planner/profile/test coupling and report the smallest implementation migration that can realize the target without changing semantics.**

M2 is reconnaissance only.

No code changes should be authorized in that first pass.

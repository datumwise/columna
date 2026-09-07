# Frame-QL vNext — Capability and Profile Reconciliation Plan

**Working Draft 0.1 — 6 September 2026**  
**Status:** Reconciliation plan; no implementation authorization  
**Inputs:** vNext language-law drafts, R4 Standing Amendment 0.2, O1 Ordered-Expression Ruling 0.1, current public repository authorities on 6 September 2026.

---

# 0. Position

The current repository already separates three questions correctly:

```text
canonical language standing
    specs/frameql_capabilities.toml

profile realization standing
    specs/profiles/core_profile.toml
    specs/profiles/platform_profile.toml

current build realization
    measured from installed package
```

That separation should be preserved.

vNext does not require capability IDs to be renamed merely because their semantic class changes.

The clean migration is:

> **Keep capability identity stable where the analytical operation is the same; correct the canonical semantic classification; preserve profile promises; let build status continue to measure reality.**

---

# 1. What changes and what does not

## Changes

The canonical authority should stop treating:

```text
reducer
scan
map
```

as if those three implementation-shaped classes were the whole semantic expression taxonomy.

vNext needs to distinguish at least:

```text
family-forming analytical law
pointwise / value expression
standing predicate
ordered analytical expression
frame operation
```

Predicate syntax position remains a separate concern.

## Does not change automatically

This reconciliation does not itself change:

```text
capability IDs
surface spellings
Core execute/plan promises
Platform additions
backend implementation
parser acceptance
wire contract
current measured build
```

Each of those has its own authority.

---

# 2. Current authority problem

The current canonical registry says:

```text
category = reducer | scan | map
```

and places:

```text
first
last
```

under `reducer`.

That was internally coherent under the older Frame-QL model.

It is no longer semantically adequate under ToD v7 and vNext.

The problem is not that Core executes `first` and `last`.

The problem is that the canonical category implies the wrong analytical standing.

Similarly:

```text
is_missing
is_null
coalesce
```

currently appear as proposed `map` capabilities even though vNext gives them three different semantic statuses.

---

# 3. Proposed registry schema direction

Do not force a final TOML schema until CC inspects generator/test coupling.

Architecturally, the registry needs a field equivalent to:

```text
semantic_class
```

whose values can represent:

```text
family_law
pointwise
value_member
value_subscription
value_predicate
standing_predicate
ordered_expression
frame_operation
```

Not every class must be populated immediately.

The existing:

```text
position = series | predicate
```

may remain useful as a separate surface-placement axis.

This separation is preferable to overloading one `category` field with both semantics and parser routing.

Conceptually:

```text
capability identity
    what operation this is

semantic class
    what kind of analytical expression it is

surface position
    where grammar permits it

canonical standing
    ratified / proposed / retired

profile realization
    execute / plan / none

build realization
    measured
```

These are different facts.

---

# 4. Family-forming laws

Capabilities whose canonical Frame-QL meaning refers to an admitted ToD family-forming law should be classified as such.

Clear examples under ToD v7 include:

```text
sum
count
min
max
mean / avg
```

and, as admitted law/catalog coverage expands:

```text
variance
stddev
weighted_mean
quantile / median
count_distinct / exact distinct constructions
...
```

However:

> **Do not mechanically reclassify every current "reducer" as a family law solely because it is currently in the reducer table.**

For example, current language standing for `mode`, approximate families, and other historical entries must be reconciled against their actual governed law before the registry asserts family-law standing.

This is a semantic review, not a bulk rename.

---

# 5. `first` and `last`

## Canonical change

Keep capability IDs:

```text
first
last
```

Keep their current canonical standing:

```text
ratified
```

unless a separate review finds a reason to change standing.

Change their semantic class to:

```text
ordered_expression
```

They are no longer described canonically as reducers.

## Re-entry field

The current registry carries:

```text
re_entry_certified = false
```

for `first` and `last`.

Under vNext, re-entry certification is a family-continuation question and should not be made to characterize a non-family ordered expression.

Therefore the registry reconciliation should determine whether:

```text
re_entry_certified
```

becomes valid only for family-law capabilities.

Do not replace `false` with another made-up value.

If the field is inapplicable, the schema should represent inapplicability honestly.

---

# 6. Scans

Capabilities such as:

```text
cumsum
cummax
cummin
lag
lead
pct_change
rolling_sum
rolling_mean
rank
...
```

belong semantically to:

```text
ordered_expression
```

where their meaning depends on an order contract.

Their **standing does not automatically change**.

The current registry can legitimately continue to say:

```text
proposed
```

for scans that the language has not individually ratified.

Thus vNext can produce:

```text
semantic class     ordered_expression
standing           proposed
Core undertakes    execute
build              execute
```

for `cumsum`.

That is not a contradiction.

It is exactly what the current three-layer architecture was designed to reveal.

---

# 7. `is_missing`

The capability identity:

```text
is_missing
```

has a clear vNext semantic target:

```text
standing predicate
```

It should not remain a generic map.

Its standing can remain:

```text
proposed
```

until exact surface syntax/position is ruled.

Its semantics must refer to:

```text
eligible(E) AND NOT supported(E)
```

only after required point/placement standing is established.

It must not be defined as carrier-null inspection.

---

# 8. `is_null`

The current proposed canonical row should not be promoted.

vNext explicitly declines `is_null` as a canonical analytical missingness predicate.

Possible future uses are carrier/profile inspection.

That creates a jurisdiction issue:

> a carrier-inspection feature is not automatically a Frame-QL analytical capability.

Recommended canonical treatment:

```text
remove the proposed canonical capability row
```

unless a separate language ruling establishes a genuine Frame-QL carrier-inspection construct.

Because it has never been ratified, removal is cleaner than preserving a misleading proposed analytical identity.

This follows the same discipline already used for unresolved `count(*)`: do not give canonical capability standing to a surface whose proper analytical identity is not established.

---

# 9. `coalesce`

The current proposed row:

```text
coalesce
category = map
```

is too broad for vNext.

Generic SQL-style null replacement is not canonical analytical semantics.

A future governed completion construct may exist, but it must carry:

```text
completion authority
scope
result type
standing/disclosure consequences
```

Recommended canonical treatment:

```text
remove or suspend the generic proposed capability identity
```

until the completion operation itself is ruled.

Do not silently reinterpret today's proposed `coalesce` row as governed completion merely because the spelling is familiar.

---

# 10. Value members and subscription

The canonical registry will eventually need to represent semantic-value capabilities such as:

```text
attribute
method
subscription
```

without treating each concrete datatype member as a global Frame-QL operator.

The likely authority split is:

```text
Frame-QL
    establishes that value member/subscription forms exist

Columna Data Types
    declares which semantic types supply which members/capabilities

profile
    undertakes realization of those language forms/types

build
    measures actual realization
```

Do not pre-populate a large global member catalog in Frame-QL.

---

# 11. Order requirements become canonical semantics

The current registry comments explicitly defer:

```text
needs_order
needs_window
```

as possibly canonical but not yet ruled.

O1 now settles the semantic point:

> ordered expressions require an order contract.

Therefore the registry needs a canonical way to say:

```text
this capability is an ordered expression
```

and, eventually where useful:

```text
window required / optional
offset required / optional
tie behavior class
```

Do not copy Core's current signatures wholesale into canonical law.

The semantic class should be settled first.

Detailed operator contract schema can follow from actual grammar design.

---

# 12. Core Profile

The Core Profile should preserve its current realization promises unless implementation/product evidence gives a separate reason to change them.

In particular:

```text
first       executes
last        executes

cumsum      executes
cummax      executes
cummin      executes
lag         executes
lead        executes
pct_change  executes

rolling_sum   plans
rolling_mean  plans
```

can remain.

Generated documentation will simply group these under the correct semantic class once the registry/generator is reconciled.

Thus:

```text
first/last move category
```

does not mean:

```text
Core loses first/last.
```

---

# 13. Platform Profile

Keep:

```text
extends = "core"
adds = []
```

unless a future language capability genuinely requires Platform-specific realization.

Platform's runtime mission does not justify a separate Frame-QL dialect.

Cross-domain identity, custody, certificate transport, and distributed composition are runtime/architecture concerns until a distinct query-language capability is actually needed.

Permanent rule:

> **Two physical runtimes are acceptable. Two meanings of a measure are not.**

---

# 14. Build Status

Build Status remains generated and measured.

Do not hand-edit it during semantic reconciliation.

If capability IDs stay stable, the existing build can continue to report realization against the same IDs while presentation groups change.

Possible temporary states are legitimate:

```text
canonical class changed
profile promise unchanged
build execution unchanged
```

The generator should display that honestly.

---

# 15. Migration sequence for CC later

When implementation reconciliation is authorized, give CC invariants rather than a patch recipe.

The required sequence is conceptually:

```text
1. inspect registry schema/generator/test coupling

2. propose the smallest schema evolution that separates:
       capability identity
       semantic class
       syntax position
       canonical standing
       profile realization
       build realization

3. migrate canonical entries
       first / last
       scans
       is_missing
       is_null
       coalesce
   without changing unrelated capability IDs

4. regenerate Core/Profile/Build tables

5. prove profile promises did not silently change

6. prove measured build did not become authored

7. update Manual cross-references

8. stop and report semantic mismatches rather than inventing new categories
```

---

# 16. Migration acceptance checks

A successful reconciliation should make all of these true:

```text
first and last are not canonically called reducers

first and last remain Core-executable capabilities

scan standing remains proposed unless separately ratified

Core may exceed canonical standing without promoting it

is_missing is not a generic value map

is_null is not presented as analytical missingness

generic coalesce does not manufacture support

Platform still extends Core with zero additions

build-status rows remain measured

capability IDs remain stable unless identity itself changed
```

---

# 17. Stop-gate

This document does not authorize edits to:

```text
specs/frameql_capabilities.toml
specs/profiles/*.toml
generator code
planner
engine
parser
wire
```

The canonical language-law draft should be reviewed as one semantic body first.

After that, CC can perform a bounded **reconciliation reconnaissance** and bring back:

```text
current schema coupling
minimal migration options
compatibility hazards
recommended implementation sequence
```

before any code change is authorized.

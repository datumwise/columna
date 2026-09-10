# Frame-QL vNext — O1 Ordered-Expression Compatibility Ruling

**Working Ruling 0.1 — 6 September 2026**  
**Status:** Semantic/compatibility ruling  
**Purpose:** Settle how vNext ordered-expression semantics coexist with shipped `first` / `last` / scan syntax.  
**Not an implementation authorization.**

---

# 0. Decision

Adopt **O1-A**.

> **Canonical ordered expressions have a fully determinate order contract. Legacy shorthand may omit parts of that contract only where the governed environment mechanically completes exactly one lawful reading, and canonicalization must expose the completed contract.**

This is a semantic ruling, not a requirement that every user type every contract field in surface syntax.

The distinction is:

```text
surface shorthand
    may omit governably single-valued detail

canonical meaning
    may not omit meaning-bearing detail
```

---

# 1. Why this ruling is required

Theory of Data v7 draws a firm family boundary:

```text
max(x @ I)
    order-independent over analytical points
    value order may be a type capability
    can be a measure-family law

last(x @ I; ...)
    depends on an ask-selected order over analytical points
    ordered analytical expression
    not a measure family merely because it returns a value
```

The current shipped Frame-QL language predates this distinction.

It currently:

- classifies `first` and `last` as ratified reducers;
- permits `level.last` as a family-variant spelling;
- treats scans separately but also as order-dependent;
- allows an order axis to be derived from an input anchor when the planner finds a suitable governed order;
- distinguishes zero governed orders from several governed orders.

Those behaviors are valuable compatibility evidence.

They do not determine the vNext semantic category.

---

# 2. Canonical semantic category

The canonical language distinguishes:

```text
family-forming analytical laws
    sum
    count
    min
    max
    mean
    variance
    ...

ordered analytical expressions
    first
    last
    lag
    lead
    cumulative
    rolling
    rank
    dense_rank
    row_number
    ...
```

`first` and `last` therefore cease to be conceptualized as reducers in the vNext language model.

This does not mean:

```text
the current build must stop executing them
```

or:

```text
their public spellings must disappear immediately
```

It means their analytical standing is corrected.

---

# 3. The order contract

An ordered expression must have enough governed information to determine its result.

Depending on the operation, the contract includes:

```text
operand
peer / partition domain
order key or keys
direction / order relation
tie semantics
window / frame
offset / step
reset boundary
```

Not every operator uses every field.

The semantic requirement is determinacy, not bureaucratic completeness.

---

# 4. Explicit does not mean "typed by the user"

The vNext principle that order must be explicit means:

> **Order must be explicit in canonical analytical meaning.**

It does not require the user to repeat a governed single-valued convention in every query.

A short form may be accepted where the Manifold / governed environment determines exactly one completion.

For example, conceptually:

```text
last(level @ {store, day})
```

may be compatibility shorthand if governance establishes exactly one sequence:

```text
peer domain     within store
order key       day
order relation  chronological ascending
tie semantics   unique day within peer
```

The canonical form must expose that completion.

If the environment does not determine all meaning-bearing fields uniquely, the shorthand is not complete.

---

# 5. "Natural order" is retired as canonical justification

The current language says that order may be derived when an anchor contains an axis with a "natural order," typically temporal.

That wording should not survive as canonical semantic authority.

A time dimension may make a likely order obvious to a human.

Likelihood is not governance.

The vNext replacement is:

> **A shorthand ordered expression may use a governed default completion only when the selected environment establishes one unique order contract for that use.**

Thus:

```text
time exists
```

does not imply:

```text
use chronological ascending order
```

unless that order is itself governed.

This avoids turning a semantic-value property or familiar convention into query authority.

---

# 6. Direction

Direction must be part of the completed order semantics wherever reversing it changes the result.

The language does not need to freeze the final surface spelling yet.

Possible future surfaces might express:

```text
by = event_time ASC
```

or another equivalent form.

Compatibility syntax may omit direction only if the governed completion supplies one unique direction.

`last` does not authorize the system to infer arbitrary direction from storage order or column naming.

---

# 7. Tie semantics

An ordered expression that selects one point must define what happens when its order keys do not uniquely distinguish participating points.

Acceptable cases include:

```text
a governed secondary key
a governed deterministic tie rule
ties are part of the result semantics
Clarify
Refuse
```

For `first` / `last`, arbitrary backend tie-breaking is not canonical.

Compatibility shorthand is permitted only where:

```text
the order is unique
```

or:

```text
the tie behavior is itself governed.
```

---

# 8. Peer / partition domain

The sequence over which the ordered operation runs is part of meaning.

It is not automatically:

```text
the whole output frame
```

or:

```text
whatever SQL PARTITION BY would be convenient.
```

A compatibility completion may derive a peer domain from established analytical structure only when there is exactly one governed reading.

Canonicalization must expose it.

---

# 9. Output `ORDER BY` is separate

Query-level:

```text
ORDER BY
```

orders the returned frame.

It does not supply any field of an inner ordered-expression contract.

Therefore:

```text
SELECT last(level ...)
AT {store}
ORDER BY store
```

does not mean that `store` is the order used by `last`.

No ambient inheritance is allowed.

This is true even where the same expression happens to appear in both places.

---

# 10. Compatibility rule for `level.last`

Historical:

```text
level.last
```

may remain accepted as compatibility syntax.

It is not a vNext family-member identity.

It denotes an ordered analytical expression only where canonicalization can establish, without guessing:

```text
operand identity
required input anchor
peer domain
order key(s)
order relation / direction
tie behavior
```

If any identity-bearing input anchor is ambiguous:

```text
Clarify
```

under the existing input-anchor discipline.

If no governed order exists:

```text
Refuse
```

If several governed orders remain:

```text
Clarify
```

If a unique completion exists:

```text
proceed
```

and the canonical explanation shows the completed ordered expression.

---

# 11. Compatibility rule for `first(...)` and `last(...)`

Function syntax may likewise remain.

The function name identifies the ordered operation.

It does not by itself provide the order contract.

A short function call is accepted only when its missing contract fields receive one unique governed completion.

Otherwise it must require an explicit order surface once such surface is canonically chosen.

---

# 12. Scans

The same semantic discipline applies to:

```text
lag
lead
cumsum
cummax
rolling_mean
rank
...
```

Existing scan syntax and implementation may continue as compatibility/profile reality.

Canonical meaning must distinguish:

```text
operand
peer domain
order
direction
ties where relevant
window / offset / reset semantics
```

The fact that a scan preserves its output anchor does not make its order incidental.

---

# 13. Capability-registry consequence

The canonical capability registry currently groups `first` and `last` under:

```text
category = "reducer"
```

while scans occupy a separate category.

The vNext target taxonomy should distinguish at least:

```text
family_law
pointwise
standing_predicate
ordered_expression
frame_operation
```

or equivalent names.

Under that target:

```text
first
last
lag
lead
cumsum
rolling_*
rank
...
```

share **ordered-expression** standing even if their realization mechanics differ.

The registry should describe semantic category.

The profile should describe implementation obligation.

The measured build should describe actual availability.

Do not use one field to answer all three questions.

---

# 14. Core-profile consequence

A Core implementation may continue to undertake:

```text
first
last
lag
lead
cumsum
...
```

after their semantic reclassification.

Reclassification does not reduce Core capability.

It makes the contract more accurate:

```text
Core supports these ordered expressions
```

rather than:

```text
these operations are ToD-style reducers.
```

---

# 15. Manifold consequence

A Manifold may govern a reusable ordered expression.

Naming it does not make it a ToD measure family.

For example, a governed end-of-period balance expression could have durable reusable request-level standing while remaining order-sensitive.

If such named non-family expressions become product requirements, they should receive their own explicit Manifold standing rather than being smuggled back into measure-family vocabulary.

---

# 16. Acceptance suite

| Case | Expected judgment |
|---|---|
| `last` with one governed unique order contract | short form may mechanically complete; canonical form exposes contract |
| `last` with two governed candidate order axes | Clarify |
| `last` with no governed order | Refuse |
| `last` relying only on physical row order | invalid/unlawful completion |
| `last` relying only on presence of a time dimension | insufficient unless a governed order completion exists |
| `last` with non-unique order keys and no tie rule | Clarify or Refuse according to operator contract |
| `last` with governed deterministic secondary key | determinate |
| output `ORDER BY` supplies only inner order | prohibited; inner contract remains unresolved |
| `max(x@I)` | family-forming value-order law where ToD contract holds |
| `last(x@I; order=...)` | ordered expression; not a measure family |
| `level.last` | compatibility syntax only; never evidence of family standing |
| named reusable `last(balance...)` in Manifold | may be governed reusable expression; not family merely by naming |

---

# 17. What remains open

O1 settles semantics and compatibility policy.

It deliberately does **not** settle:

1. final surface grammar for explicit order contracts;
2. exact serialization of the canonical order contract;
3. whether existing `by =` syntax is generalized or replaced;
4. registry schema migration mechanics;
5. whether `first` / `last` compatibility syntax receives a deprecation horizon;
6. the authoring surface for named governed non-family expressions.

Those can now be decided from implementation/product evidence without reopening the semantic boundary.

---

# 18. Stop-gate

No parser or engine change is authorized by this ruling.

The next task is the canonical language-law rewrite:

```text
family-forming laws
semantic value access
standing
ordered expressions
```

using R4 Amendment 0.2 and O1 as settled semantic inputs.

Only after that language text stabilizes should the capability registry and Core profile be reconciled.

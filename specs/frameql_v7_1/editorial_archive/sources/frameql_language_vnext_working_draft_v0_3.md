# The Frame-QL Manual — vNext Language-Law Candidate

**Working Draft 0.3 — 6 September 2026**  
**Status:** Consolidated canonical-language candidate  
**Scope:** Semantic language law and compatibility boundaries; not yet clause-by-clause replacement of the shipped Manual  
**Not a syntax release. Not an implementation authorization.**

> This draft rewrites the canonical language account. It does not claim that every form described semantically is accepted by the current parser or executed by the current build. Availability belongs to the Core/Platform profiles and measured build status.

---

# Preface

Frame-QL is a language for stating a governed analytical result.

A query says which analytical expressions should appear in the result, where the result frame should live, and which conditions shape that frame. It does not prescribe a relational procedure, choose physical joins, or tell an execution engine how to manufacture the result.

The central boundary is:

> **The query should contain the information required to identify the analytical result, not the information required to physically manufacture it.**

That boundary is why Frame-QL has an output anchor but no `GROUP BY`, can express meaning-bearing input anchors without exposing arbitrary query-time joins, and can refuse or clarify a request before physical execution.

The language sits between three neighboring authorities:

```text
Theory of Data
    analytical identity and analytical law

Frame-QL
    expression and request semantics

Columna Data Types
    semantic value types and capabilities
```

An implementation then realizes a profile of the language.

```text
Frame-QL language law
        ↓
Core / Platform profile
        ↓
specific build
```

These layers must not be collapsed.

A value-returning expression is not automatically a measure family.

A syntax accepted by a parser is not automatically canonical language law.

A capability executed by one build is not automatically part of the language.

A new Theory distinction does not automatically become Frame-QL syntax.

This Manual states what Frame-QL means.

The Core Profile states what a conforming Core implementation undertakes to realize.

The Platform Profile states what Platform adds beyond Core.

Build Status reports what a particular shipped build actually runs.

---

# 1. Authority and jurisdictions

## 1.1 The language's job

Frame-QL has one job:

> **Represent a governed analytical request precisely enough that its meaning can be adjudicated independently of its physical realization.**

The request may contain:

- governed family references;
- anchored measures and other anchorable expressions;
- pointwise expressions;
- family-forming analytical laws;
- order-sensitive analytical expressions;
- predicates over values or analytical standing;
- clauses that shape or select the returned frame.

Those forms do not all have the same analytical standing.

Frame-QL must preserve that difference.

## 1.2 What Theory of Data owns

Theory of Data owns analytical facts such as:

- universe and point existence;
- anchor geometry;
- measure-family identity;
- the measure identity `F@A`;
- family formation under admitted analytical law;
- sufficient-state relationships;
- lawful analytical derivability;
- analytical lineage;
- identity-relative consistency.

Frame-QL consumes those objects and laws.

It does not redefine them.

## 1.3 What Columna Data Types owns

Columna Data Types owns the semantic value domains and capabilities required by expressions and analytical laws.

Examples of capability requirements include:

- addition;
- multiplication;
- division;
- equality;
- value ordering;
- set union;
- structured values;
- attribute access;
- methods;
- value subscription.

A set, tuple, vector, sketch, struct, or other rich value can be the value of one measure.

Its internal structure is not an analytical anchor.

> **Internal value structure is not analytical location.**

## 1.4 What Frame-QL owns

Frame-QL owns the language-level distinctions needed to make analytical requests explicit.

It determines:

- expression sorts;
- expression composition;
- where analytical anchoring may appear;
- how pointwise co-participation is expressed;
- how admitted family-forming laws are referenced;
- how order-sensitive expressions state their order contracts;
- how semantic value capabilities are accessed;
- how analytical standing may be inspected;
- how a frame is assembled, filtered, ordered, and limited;
- what constitutes a valid request before realization.

## 1.5 What profiles own

A profile says which canonical language capabilities an implementation undertakes to realize.

A profile may implement less or more than another profile.

It may not change what the language means.

## 1.6 What a build owns

A build owns no semantics merely by existing.

It is evidence of implementation.

Build Status may say that a build:

```text
conforms
lags
exceeds
```

a profile.

That is a useful fact.

It is not a license to redefine the language to make every build appear conforming.

---

# 2. The query and the frame

## 2.1 A query returns one frame

A Frame-QL query requests one result frame.

Conceptually:

```text
[governed environment]
SELECT <expressions>
AT {<output anchor>}
[frame-shaping clauses]
```

The frame has one final output anchor.

The output anchor's coordinates identify its analytical rows.

The selected expressions provide its value columns.

## 2.2 The output frame is not a new analytical ontology

A frame is a requested assembly of analytical results.

It does not become a new measure family merely because several expressions appear beside one another.

Two selected expressions may:

- belong to different measure families;
- be ordinary pointwise expressions;
- be ordered expressions;
- even belong to different governed universes where the language permits juxtaposition.

Co-location in one frame does not collapse those identities.

## 2.3 Query aliases name output columns

A query may assign an output key:

```frameql
SELECT revenue / orders AS aov
AT {region}
```

`aov` is an output-column alias.

It does not establish a durable `AOV` measure family.

Saving the query text does not establish one either.

Durable analytical identity is established by governed analytical law and Manifold declaration, not by an output label.

## 2.4 Request clauses have different analytical jurisdictions

The envelope contains several request-level operations. They do not all act at the same stage.

### `WHERE` — analytical restriction

`WHERE` restricts the input participation/domain of the request before the affected analytical expressions are formed.

It can therefore change the values those expressions establish.

A Frame-QL `WHERE` is request-local restriction over the existing governed universe. It does not, merely by appearing in a query:

- redefine the Manifold universe;
- mint a named subuniverse;
- promote a durable family;
- grant the requester authority over physical scan mechanics.

A separate governed carve or population declaration is required where the population claim itself changes.

### `HAVING` — output selection

`HAVING` selects among already-formed output points using output coordinates or expressions.

It does not change which input contributions formed those expressions.

### `ORDER BY`, `LIMIT`, and `LIMIT ... PER` — frame ordering and selection

These operate on the returned frame.

`ORDER BY` in particular orders output points.

It does not silently provide any field of the order contract of an inner ordered analytical expression.

None of these clauses mints measure-family identity merely by shaping a request.

---

# 3. Expression sorts

Frame-QL has several expression sorts.

These are language distinctions.

They are not additional ontological kinds in Theory of Data.

## 3.1 Family reference

Example:

```text
revenue
```

A family reference resolves to one governed measure-family identity.

It can be anchored.

Its family identity and analytical lineage exist independently of the query.

A query alias cannot create or change that identity.

## 3.2 Measure expression

Example:

```text
revenue @ {region}
```

Conceptually this denotes:

```text
Revenue@Region
```

where the governed environment establishes the family and anchor.

The final anchor is the current analytical location of the measure.

## 3.3 General anchorable expression

Examples:

```text
revenue / orders
price * quantity
margin / revenue
```

A general anchorable expression is:

- typed;
- governed by the co-participation rules of its operands;
- anchorable where its operands can be lawfully co-established;
- not given durable measure-family identity merely by its syntax;
- not given an independent continuation law merely by its syntax.

For ordinary pointwise forms:

```text
(E1 ★ E2) @ A
```

has the pointwise reading:

```text
(E1 @ A) ★ (E2 @ A)
```

only where the governed co-participation contract and semantic type capabilities admit the operation.

A computable expression is therefore not automatically a new measure family.

## 3.4 Tuple expression

Example:

```text
(revenue, cost)
```

At anchor `A`:

```text
(revenue, cost) @ A
```

means the co-participating pair:

```text
(revenue @ A, cost @ A)
```

where the governed pairing contract is satisfied.

The tuple is a structured expression value.

It is not an anchor.

It does not become a measure family merely because its value is structured.

## 3.5 Family-forming analytical expression

Examples:

```text
sum(revenue @ {order})
mean(revenue @ {order})
variance(price @ {transaction})
count(order)
```

Where an admitted Theory-of-Data analytical law applies, such an expression establishes or denotes a governed measure family.

The constitutive inner anchor and other identity-bearing law parameters belong to the constructed family identity.

For example:

```text
mean(revenue @ {order})
```

and:

```text
mean(revenue @ {customer})
```

need not denote the same family even if both are later displayed at the same outer anchor.

Family formation is governed by the analytical law.

The mere fact that a function returns a scalar is insufficient.

## 3.6 Ordered analytical expression

Conceptual examples include:

```text
first(...)
last(...)
lag(...)
lead(...)
cumsum(...)
rolling(...)
rank(...)
```

An ordered analytical expression depends on an explicit governed order contract over analytical points.

Its meaning may depend on:

- the peer or partition domain;
- one or more order keys;
- direction;
- tie semantics;
- a window or frame;
- an offset or step.

Ordered expressions are valid analytical expressions.

They do not become ToD measure families merely because they return values.

This distinction is structural.

For example:

```text
max(x @ I)
```

selects the greatest participating **value** under a value order and can remain permutation-invariant over the participating analytical points.

By contrast:

```text
last(x @ I; order = ...)
```

selects a terminal **point** under an ask-selected order over those points.

The first can be a family-forming law.

The second is an ordered expression.

## 3.7 Predicate and standing expression

Predicates may inspect different jurisdictions.

### Value predicates

These operate on semantic values where the type supplies the required capability.

Examples include equality and ordered comparisons.

### Standing predicates

These inspect analytical standing such as:

```text
point existence
measure eligibility
measure support
```

Standing predicates are not ordinary functions over a nullable value type.

An unsupported expression has no established semantic value merely because a carrier happens to use `NULL`.

## 3.8 Semantic-value access expression

Typed semantic values may support value-layer access forms such as:

```text
E.member
E.method(...)
E[key]
```

where the resolved semantic value type supplies the requested capability.

These expressions operate on the value carried by `E`.

They do not turn internal value structure into analytical location, and they do not create measure-family identity merely by exposing part or a property of a value.

The exact member, method, and subscription capabilities belong to Columna Data Types and the canonical Frame-QL capability authority.

---

# 4. Analytical anchoring

## 4.1 The semantic operation

Analytical anchoring is written conceptually as:

```text
E @ A
```

and asks for expression `E` at analytical anchor `A`.

Where `E` is a family reference `F`, the result is the measure:

```text
F@A
```

where the family law and governed environment establish it.

Where `E` is a general anchorable expression, its operands must be lawfully available for participation at the evaluation anchor under the applicable co-participation, structural-alignment, and type rules.

Anchoring does not mean "group these physical rows."

It states analytical location.

It also does not grant arbitrary movement authority. In particular, making the value of a coarser anchored expression available inside a finer outer expression by broadcast does not thereby establish a finer measure of the same family.

## 4.2 `@` and `AT`

The shipped Frame-QL surface uses two spellings because two structural positions must remain visible.

```text
E @ {A}
    expression-level / input-position anchoring

AT {A}
    the one final output anchor of the frame
```

The underlying semantic distinction is not two unrelated meanings of anchor.

`@` anchors an expression that can be consumed by another expression.

`AT` declares the unique anchoring of the completed frame.

## 4.3 One current anchor, constitutive inner anchors

A measure has one current analytical anchor.

For a constructed family expression:

```text
mean(revenue @ {order}) @ {region}
```

the two anchors have different jobs.

```text
order
    constitutive inner anchor of the mean-family identity

region
    current analytical location of the resulting measure
```

The inner anchor does not become a second current anchor.

It belongs to family identity because changing it can change what quantity the family denotes.

## 4.4 Pointwise anchoring

For a pointwise expression:

```text
revenue / orders
```

anchoring at `region` has the intended reading:

```text
(revenue @ {region}) / (orders @ {region})
```

only when both operands are themselves lawfully establishable at `region` and:

- the operands may co-participate;
- their universes are compatible for one expression;
- division is supported by their semantic value types;
- denominator exceptional cases are governed.

The more general pointwise rule is slightly broader: every operand must be lawfully **available for participation** at the evaluation anchor. An operand may be directly established there, or an already-established coarser expression may be made available there through a governed structural alignment such as broadcast.

Structural availability does not change analytical identity.

Anchor equality alone does not establish all of these premises.

## 4.5 Tuple anchoring

For:

```text
(revenue, cost) @ {order}
```

the pair exists only where both components have governed co-participating standing at `order`.

This matters for multi-input laws such as covariance and correlation.

A physical join that happens to place two values on one row does not by itself establish the analytical pair.

## 4.6 Broadcast and structural expression alignment

A coarser anchored expression may sometimes participate in a finer outer expression.

For example:

```frameql
SELECT
    (revenue @ {customer}) / (revenue @ {}) AS share
AT {customer}
```

The denominator remains the scalar measure:

```text
Revenue @ {}
```

Its value is replicated so that the outer ratio can be evaluated at customer points.

That broadcast does **not** establish:

```text
Revenue @ customer
```

merely by replication.

Broadcast therefore has a narrow semantic role:

- make an already-established coarse value available to a finer enclosing expression;
- replicate, never allocate;
- preserve the analytical identity of the broadcast operand;
- carry any downstream conservation or reaggregation restrictions required by governed law.

Broadcast is structural expression alignment, not family formation.

## 4.7 Anchoring does not create durable identity

This expression:

```text
(revenue / orders) @ {region}
```

can be a lawful result without creating a durable `AOV` measure family.

A governed Manifold declaration may separately promote a suitable expression into a family.

The query does not perform that promotion.

---

# 5. The three postfix axes

The language should keep three semantic axes distinct:

```text
E @ A
    analytical anchoring / location

E.member
E.method(...)
    governed semantic-value capability or qualified-name resolution

E[key]
    semantic-value subscription
```

They answer different questions:

```text
@
    where does this analytical object live?

.
    what governed name qualification or semantic value capability is being used?

[]
    what internal part of the semantic value is being subscribed?
```

No axis may silently act as another.

In particular:

- an internal key is not an analytical dimension;
- a value attribute does not change anchor merely because it exposes structure;
- analytical filtering is not value subscription;
- backend object-property lookup is not language authority.

---

---

# 6. Family-forming analytical laws

## 6.1 A family law does more than compute a value

Some Frame-QL expressions can denote measure families because Theory of Data admits a governed analytical law for them.

Conceptual examples include:

```text
sum(revenue @ {order})
count(order)
count(revenue @ {order})
mean(revenue @ {order})
variance(price @ {transaction})
covariance(price @ {order}, quantity @ {order})
```

These expressions are different from ordinary arithmetic such as:

```text
revenue / orders
price * quantity
```

A pointwise arithmetic expression may produce a lawful analytical value without acquiring:

- a family ID;
- independent analytical lineage;
- a continuation law;
- sufficient-state standing;
- durable materializability.

A family-forming law does establish a governed analytical family when its law contract is satisfied.

> **Computability does not create family identity. Analytical law does.**

## 6.2 The constitutive inner anchor

A family-forming law consumes its analytical input at an inner anchor.

For example:

```text
mean(revenue @ {order})
```

denotes a different family from:

```text
mean(revenue @ {customer})
```

unless governance establishes an explicit equivalence.

The inner anchor is therefore part of family identity when changing it changes what quantity is being formed.

Later anchoring does a different job:

```text
mean(revenue @ {order}) @ {region}
```

has:

```text
order
    constitutive inner anchor

region
    current analytical location
```

The resulting measure still has one current anchor.

The inner anchor survives inside the family identity.

## 6.3 Anchor-derived families

A family law need not begin with a measure-valued operand.

The clearest example is:

```text
count(I)
```

where `I` is an anchor.

`count(I)` counts points of the anchor.

This must remain distinct from:

```text
count(x @ I)
```

which counts participating `x @ I` measures under the governed participation law.

Suppose 100 orders are known to exist but Revenue is supported on only 97.

Then, conceptually:

```text
count(order)              = 100
count(revenue @ {order})   = 97
```

unless a separate totality/support rule establishes another result.

This distinction becomes especially important under data loss.

Point existence is not measure participation.

## 6.4 Pointwise formation before reduction

Some family laws need relationships among several values at the same inner point.

For a weighted mean, the numerator needs the pointwise product of value and weight while both are jointly available.

Conceptually:

```text
(x * w) @ I
```

must be formed before a reduction that would destroy their pointwise pairing.

Likewise covariance and correlation require governed paired participation at their constitutive inner anchor.

A physical join does not by itself establish that pair.

The governing co-participation contract must do so.

> **A later law cannot use a relationship that was neither retained nor reconstructed from governed evidence.**

## 6.5 The family-law contract

A canonical family-forming law must be determinate enough to fix the family it forms.

Depending on the law, that includes:

```text
canonical family form
identity-bearing parameters
operands
constitutive inner anchor requirements
eligibility and participation
co-participation where needed
semantic type requirements
sufficient-state basis
anchor-local construction
continuation law where self-sufficient
empty / undefined / exceptional cases
exactness or approximation conventions
```

Frame-QL does not invent these obligations.

It exposes and consumes the governed law.

## 6.6 Sufficient state belongs to analytical law

A displayed result is not automatically sufficient state for later continuation.

For mean:

```text
mean(x @ I)
```

one admitted basis is:

```text
sum(x @ I)
count(x @ I)
```

The displayed mean scalar does not by itself license a later mean-of-means continuation.

Likewise exact distinct count may depend on a set-valued family rather than the displayed scalar count.

This is why a materialized value can be available while exact continuation is unavailable.

## 6.7 Rich-value state remains ordinary analytical data

A family can carry a structured semantic value.

Examples may include:

```text
Set<T>
Multiset<T>
sketch values
tuples
structured state
```

The value's internal fields or elements do not become analytical anchor levels.

A set-valued family remains a measure family.

Its concrete value representation belongs to Columna Data Types.

Its analytical law belongs to Theory of Data.

## 6.8 Family aliases and governed named families

A Manifold may already declare a governed family whose law corresponds to an explicit family-forming expression.

For example, a governed `revenue` family may already be the family established by the relevant sum law.

Where identity, participation, and law agree, canonicalization may resolve the explicit construction to the governed family identity.

This is governed identity resolution.

It is not string aliasing.

## 6.9 Availability is profile-specific

This chapter defines semantic standing.

It does not claim that every analytical law shown here is accepted by the current parser or realized by the current engine.

The capability registry and Core / Platform profiles state which forms have language standing and implementation obligation.

Build Status reports what a particular build actually runs.

---

# 7. Semantic values, attributes, methods, and subscription

## 7.1 Analytical location and value structure are different axes

A Frame-QL expression can have both:

- an analytical location;
- an internal semantic value.

These must remain separate.

```text
E @ A
```

asks where the analytical expression lives.

```text
E.member
E.method(...)
E[key]
```

operates on the semantic value carried there.

> **Internal value structure is not analytical location.**

## 7.2 Dot at the name layer

A dotted token can be a governed qualified name when the whole token resolves as one governed analytical or structural name.

Example:

```text
category.touch
```

where `touch` is a governed relationship face.

In that case the dot belongs to name resolution.

It is not value-member access.

The parser/resolver should first ask whether the complete dotted form is a governed qualified name.

## 7.3 Dot at the value layer

If the complete dotted token does not resolve as a governed name, dot may denote a semantic-value attribute or method where the value type supplies that capability.

Conceptually:

```text
E.cardinality
E.norm
E.method(...)
```

The exact catalog belongs to Columna Data Types and the canonical language capability registry.

Value-member access:

- acts on the semantic value;
- does not create a dimension;
- does not create a new anchor;
- does not create family identity merely by being applied;
- does not turn internal fields into analytical coordinates.

## 7.4 Historical dotted family forms

Historical forms such as:

```text
revenue.sum
level.last
```

may remain compatibility syntax where their normalized meaning is uniquely governed.

They are not the vNext conceptual grammar.

`revenue.sum` belongs conceptually to family-forming analytical law.

`level.last` belongs conceptually to ordered analytics.

A generic "family member" model must not erase that difference.

## 7.5 Value subscription

Brackets are reserved for semantic-value subscription:

```text
E[key]
E[i]
```

where the semantic value type supports subscription.

Subscription means access to an internal part of a value.

It does not mean:

```text
filter analytical points
restrict a population
select an anchor coordinate
create a dimension
```

The former roadmap form:

```text
revenue[region = "east"]
```

is therefore not canonical analytical filtering.

Analytical restriction remains in explicit predicate/request semantics unless a separate local-restriction surface is ruled in later.

## 7.6 Subscription does not imply current implementation support

Reserving `[]` for value subscription settles semantic ownership of the syntax.

It does not require current Core to ship a subscriptable semantic type immediately.

A semantic role can be settled before a profile undertakes it.

---

# 8. Analytical standing: existence, placement, eligibility, and support

## 8.1 Why "missing" needs a narrow meaning

Physical systems often use one representation for many different conditions:

```text
no row
NULL
NaN
missing dataframe cell
absent JSON field
```

Frame-QL cannot use those carrier states as the definition of analytical missingness.

The language must first know what analytical claim failed.

The standing dependency is:

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

These are different questions.

## 8.2 Point existence

The universe existence law determines which root points belong to the analytical universe.

For a candidate event/root point:

```text
existent
nonexistent
existence unsupported
```

are different states.

In an event universe:

```text
event known not to have occurred
    → nonexistent

event known to have occurred
    → existent

no record and no governed evidence either way
    → existence unsupported
```

Unsupported existence must not be coerced to nonexistence merely because an ordinary record is absent.

## 8.3 Placement under an anchor

Assume a root point is known to exist.

A governed anchor partitions the universe, so the point has exactly one true placement under that anchor.

But governance may not have enough evidence to establish which anchor point it belongs to.

Example:

```text
transaction T123 occurred
transaction date was carried only by a lost record
```

Then:

```text
transaction existence
    established

placement under day
    unsupported
```

This is not a missing Revenue value.

It is not an invalid `day` anchor.

The governed placement cannot currently be established.

This chapter uses **placement support** as an explanatory phrase. The exact public predicate name remains open.

## 8.4 Placement is anchor-relative

A point can have different standing under different anchors.

Example:

```text
customer placement     established
store placement        established
day placement          unsupported
campaign placement     unsupported
```

Therefore there is no useful universal state called "the point has a missing anchor."

The analytical question is always relative to an anchor.

## 8.5 Four different anchor-related failures

The language should not collapse these:

### Required input anchor omitted

Example:

```text
mean(revenue)
```

where order versus customer changes identity.

This is request under-specification.

It can Clarify.

### Referenced anchor is not governed

The request names something that does not resolve to a lawful anchor.

This is geometry/anchor standing failure.

### Point existence unsupported

The system cannot establish whether the underlying point exists.

### Placement unsupported

The point exists and the anchor is valid, but the system cannot establish the point's membership under that anchor.

These require different diagnoses and different repairs.

## 8.6 Anchor-point existence is derived

A coordinate tuple does not create an analytical point merely by being writable.

In an occurrence-based universe:

```text
store = S, day = D
```

denotes an anchor point only where governed root points actually occupy the corresponding block.

If no root point belongs there, there is no nonempty anchor point.

If relevant existence or placement is unsupported, the system may also be unable to establish whether that candidate block is populated.

Coordinates are not proof of existence.

## 8.7 Eligibility

After the relevant analytical point is established, a measure/expression can be:

```text
eligible
ineligible
eligibility unsupported
```

Example:

```text
metric applies only to active subscriptions
customer-month exists
active-status evidence is unavailable
```

The system cannot truthfully classify the case as either:

```text
ineligible
```

or:

```text
eligible but missing
```

until eligibility itself is established.

## 8.8 Support

At an established analytical point where eligibility is known:

```text
supported(E)
```

means the governed evidence required to establish the semantic value is available.

The canonical meaning of:

```text
missing(E)
```

is:

```text
eligible(E) AND NOT supported(E)
```

after the required point and placement are established.

`missing(E)` does not mean:

```text
point nonexistent
point existence unsupported
required placement unsupported
eligibility unsupported
ineligible
carrier NULL
parse failure
```

## 8.9 A lost record

The phrase "lost record" itself may be evidence of existence.

If governance accepts:

```text
the transaction record was lost
```

then the transaction is known to have occurred.

What remains unsupported depends on which facts were carried only by that record.

### Value lost, coordinates preserved

```text
point exists
day placement established
Revenue eligible
Revenue unsupported
```

This is ordinary missing Revenue.

### Coordinates and values lost

```text
point exists
day placement unsupported
customer placement unsupported
Revenue may separately be unsupported
```

These are several standing failures, not one undifferentiated missing record.

### Value survives elsewhere, placement lost

```text
point exists
Revenue supported
day placement unsupported
```

Total Revenue may remain exact while Revenue by day is not fully establishable.

This proves that placement support and measure support are different.

## 8.10 Point counts and measure counts

Theory of Data distinguishes:

```text
count(I)
```

from:

```text
count(x @ I)
```

The first counts analytical points.

The second counts participating measures.

This lets a system preserve a known population even when some measure values are unsupported.

Suppose:

```text
100 transactions known to exist
99 Revenue values supported
1 Revenue value lost
```

Then the transaction population remains 100.

A mean over the governed 100-transaction eligible population must not silently shrink its denominator to 99 because only 99 ordinary records remain.

## 8.11 Placement failure propagates only where needed

Suppose one known transaction has:

```text
Revenue supported
day placement unsupported
```

A total that does not depend on day placement may remain establishable.

A daily breakdown does depend on it and therefore cannot claim complete support.

The rule is:

> **Unsupported placement blocks claims that require that placement; it does not make every claim about the point unavailable.**

This is narrower than unsupported point existence.

## 8.12 Supported zero

A supported zero is an ordinary value:

```text
supported(E)
value(E) = 0
```

It is not missing.

A declared/spine universe can establish a point independently of an observation.

A separate governing law may then establish zero from absence.

Neither existence nor zero is inferred from the physical absence alone.

## 8.13 Carrier nullability

Carrier `NULL`, `NaN`, absent fields, and parse failures may be evidence used by a realization layer.

They do not define the analytical state.

A conversion failure:

```text
Text -> Decimal
```

is a conversion/realization failure unless governing rules establish another interpretation.

It does not automatically mean the measure is missing.

## 8.14 Conceptual standing predicates

The semantic model may eventually expose predicates conceptually like:

```text
exists(point)
existence_supported(point)

placement_supported(point, A)

eligible(E)
eligibility_supported(E)
supported(E)
missing(E)
```

These names are explanatory, not final grammar.

The important distinction is jurisdiction.

Point/placement standing belongs upstream of measure standing.

Measure standing belongs upstream of semantic value.

## 8.15 Frame-level consequences

A support defect need not correspond to a returned row containing a missing cell.

Suppose one known transaction has unknown day placement.

If the query requests daily Revenue, the system must not silently omit the transaction and call the daily frame complete.

Depending on the governed policy and profile, the request may:

```text
Refuse
Clarify
or return an explicitly governed partial result with disclosure
```

What it may not do is convert upstream placement uncertainty into invisible population shrinkage.

---

# 9. Ordered analytical expressions

## 9.1 Ordered analytics is a language layer

Some analytical expressions depend on an order over analytical points.

Examples include:

```text
first
last
lag
lead
cumsum
rolling_mean
rank
dense_rank
row_number
```

These are legitimate analytical expressions.

They are not measure families merely because they return values.

The family ontology remains order-independent.

## 9.2 Value order versus point order

This distinction is central.

```text
max(x @ I)
```

uses an order over the **values** of `x`.

The participating analytical points can be enumerated in any order.

The result is permutation-invariant over the points.

By contrast:

```text
last(x @ I; ...)
```

selects a terminal **analytical point** under an order chosen for the ask.

Changing that point order can change the answer.

Therefore:

```text
max
```

can be a family-forming law where its ToD contract holds.

```text
last
```

is an ordered expression.

## 9.3 The order contract

An ordered expression must have enough governed information to determine one result.

Depending on the operator, that includes:

```text
operand
peer / partition domain
order key or keys
direction / order relation
tie semantics
window or frame
offset / step
reset boundary
```

Not every operator uses every field.

The rule is determinacy.

## 9.4 Peer domain

The expression must know which analytical points form one sequence or compete with one another.

Examples conceptually include:

```text
within customer
within account
within all admitted points
```

The peer domain is not automatically the output frame.

Nor is it automatically whatever physical partitioning is convenient for an engine.

## 9.5 Order key and direction

Order keys are analytical/value expressions that establish the sequence.

Example:

```text
event_time
```

Direction is part of meaning where reversing the order changes the result.

The final surface syntax is not frozen here.

The canonical meaning may be thought of as carrying something like:

```text
event_time ASC
```

where the governing environment establishes that order.

Physical row order, storage clustering, and backend defaults are never canonical order.

## 9.6 Tie semantics

If the declared order does not distinguish participating points, the operator must have a governed result.

Depending on the operation, that may require:

```text
secondary key
governed tie rule
tied-rank semantics
Clarify
Refuse
```

`first` and `last` must not use arbitrary backend tie-breaking.

## 9.7 Window and offset

Some operations need additional sequence structure.

Examples:

```text
lag 1
lead 2
rolling 7 points
rolling 7 days
include current point
exclude current point
reset at year
```

Those choices belong to the ordered-expression contract.

They are not merely execution parameters when changing them changes the answer.

## 9.8 Canonical explicitness and shorthand

Canonical ordered meaning is explicit.

Surface syntax may be shorter.

A shorthand is accepted only when the governed environment mechanically supplies exactly one completion.

Example conceptually:

```text
level.last
```

may remain compatibility syntax where governance uniquely establishes:

```text
operand
input anchor
peer domain
order axis
direction
tie behavior
```

Canonicalization must expose that completed meaning.

If several completions remain:

```text
Clarify
```

If no governed completion exists:

```text
Refuse
```

No guessing is permitted.

## 9.9 "Natural order" is not authority

A time dimension often has an obvious human chronology.

That does not make chronology implicit language law.

The vNext rule is not:

```text
time dimension present
    → infer chronological order
```

It is:

```text
one governed order completion exists
    → shorthand may mechanically resolve to it
```

A familiar convention may motivate a Manifold declaration.

It does not replace one.

## 9.10 Output `ORDER BY`

Query-level:

```text
ORDER BY
```

orders the returned frame.

It does not provide an order contract to an inner ordered expression.

For example:

```text
SELECT last(level ...)
AT {store}
ORDER BY store
```

does not make `store` the order used by `last`.

Ambient order inheritance is prohibited.

## 9.11 Historical `first` / `last` reducer classification

The current shipped language classifies `first` and `last` as reducers and supports dotted forms such as:

```text
level.last
```

vNext keeps those spellings only as compatibility surfaces where appropriate.

Their canonical semantic category is:

```text
ordered analytical expression
```

not:

```text
measure-family reducer
```

A profile may continue to undertake and execute them.

Semantic category and implementation availability are different questions.

## 9.12 Scans use the same order discipline

Scans such as:

```text
lag
lead
cumsum
rolling_mean
rank
```

are already visibly order-dependent.

vNext gives `first` and `last` the same semantic home.

Implementation mechanics can still differ.

The language category is shared because the analytical dependency is shared: the answer depends on a governed sequence of analytical points.

## 9.13 Named reusable ordered expressions

A Manifold may eventually govern and name an ordered expression for reuse.

That does not make the object a ToD measure family.

If product requirements need durable named non-family expressions, the Manifold should represent that standing explicitly rather than overloading derived-measure identity.

---

---

# 10. Canonicalization and compatibility syntax

## 10.1 Canonical resolution counts lawful meanings, not spellings

Whenever surface syntax omits meaning-bearing information, Frame-QL resolves the governed candidate readings and groups candidates that are analytically equivalent under governed law.

The governing rule is:

```text
zero distinct lawful readings
    → Refuse

one distinct lawful reading
    → proceed with that canonical meaning

several distinct lawful readings
    → Clarify
```

Different spellings or intermediate anchors do not create several readings where governance proves them analytically equivalent.

Current-data coincidence never proves equivalence.

This rule applies to, among other cases:

- omitted constitutive input anchors;
- governed default family completion;
- legacy dotted-family compatibility syntax;
- ordered-expression shorthand;
- ambiguous governed paths.

## 10.2 Compatibility does not define semantics

Frame-QL has shipped forms whose historical explanation predates the vNext semantic model.

Compatibility syntax may remain where its canonical meaning is unique.

It does not remain authoritative merely because existing queries use it.

The canonicalizer's job is:

```text
accepted surface
    ↓
governed resolution
    ↓
canonical semantic form
```

not:

```text
accepted surface
    ↓
preserve the old conceptual model forever
```

## 10.3 Dotted historical family forms

Historical forms such as:

```text
revenue.sum
level.last
```

may remain accepted where the governed environment can normalize them uniquely.

Their canonical semantic destinations differ:

```text
revenue.sum
    → family-forming analytical law

level.last
    → ordered analytical expression
```

A generic "family member" abstraction must not erase that difference.

## 10.4 Brackets

The former roadmap analytical-filter form:

```text
revenue[region = "east"]
```

is not canonical vNext syntax.

`[]` is reserved for value subscription.

Expression-local analytical restriction, if ever added, requires a different syntax ruling.

## 10.5 Ordered shorthand

Historical or short ordered forms may omit parts of the order contract only where governance supplies exactly one completion.

Canonicalization must expose the completed order meaning.

No completion may come from:

```text
physical row order
storage clustering
outer ORDER BY
the mere presence of a time dimension
```

## 10.6 Input-anchor omission

A required identity-bearing input anchor may be omitted only where one governed reading is mechanically determined.

If several identity-distinct inner anchors remain, the request Clarifies.

This is request under-specification, not analytical missingness.

## 10.7 Alias and promotion

```text
AS name
```

names an output column.

```text
WITH name = expression
```

is query-local reuse where that form is supported.

Neither creates durable analytical family or dimension identity.

Promotion belongs to governed Manifold authoring.

---

# 11. Manifold promotion boundary

## 11.1 Query expressions are request-level terms

A lawful Frame-QL expression can exist only for the request being made.

That does not give it durable governed identity.

For example:

```text
revenue / orders
```

can be a valid expression without being the governed `Average Order Value` family.

## 11.2 Derived measure family

A Manifold may establish a durable derived measure family where the defining analytical law satisfies Theory-of-Data family standing.

That declaration must establish the identity-bearing law, operands, constitutive anchors, lineage, participation/support contract, value type requirements, sufficient-state basis, and other law obligations.

The query does not mint that family.

## 11.3 Derived dimension or structural object

A categorical-looking expression does not automatically form an anchor.

A governed declaration must establish lawful analytical geometry, including the source universe, partition or derived-universe construction, lineage, and overlap/multiplicity handling.

## 11.4 Named governed non-family expression

An ordered expression may need a durable reusable governed name without becoming a measure family.

If product requirements call for that object class, the Manifold should represent it explicitly rather than overloading "derived measure."

The exact authoring syntax remains open.

---

# 12. Validity, adjudication, and realization

A Frame-QL expression is not lawful merely because it parses.

Depending on the form, validity may require:

```text
governed name resolution
anchor standing
point / placement standing
universe compatibility
co-participation
request restriction / population contract where relevant
structural alignment such as broadcast
family-law admission
semantic type capability
eligibility and support
order contract
relationship construction
conversion standing
profile realization standing
```

These belong to different jurisdictions.

The language should preserve that staging.

Conceptually:

```text
parse
  ↓
name / type / structural resolution
  ↓
analytical adjudication
  ↓
profile realization check
  ↓
physical planning / execution
```

A lower layer may report an inability to realize a lawful request.

It may not redefine the request into something it can execute.

---

# 13. Capability and profile boundary

The canonical language states what a capability means and what standing it has.

The Core Profile states what a conforming Core implementation undertakes to realize.

The Platform Profile adds any Frame-QL capabilities beyond Core.

Build Status measures what a specific release actually runs.

These remain separate authorities.

The vNext semantic taxonomy needs to distinguish at least:

```text
family-forming analytical law
pointwise / value expression
standing predicate
ordered analytical expression
frame operation
```

without using implementation mechanics as analytical ontology.

Current capability IDs can remain stable where identity has not changed.

For example:

```text
first
last
```

can remain the same capabilities while moving from the old `reducer` category to the vNext ordered-expression category.

Core may continue to undertake them.

The build may continue to execute them.

Platform currently needs no Frame-QL additions merely because its runtime architecture differs.

---

# 14. Semantic acceptance suite

The following cases are intended to survive future syntax and implementation changes.

| Case | Expected semantic judgment |
|---|---|
| `mean(revenue @ order)` vs `mean(revenue @ customer)` | distinct families absent explicit equivalence |
| `count(order)` with 100 known orders and 97 supported Revenue values | point count 100; Revenue participation may be 97 |
| `revenue / orders` | anchorable expression where contracts hold; no family identity merely from syntax |
| rich set-valued state | value structure remains inside one measure, not an anchor |
| `E[key]` | value subscription only |
| event known not to occur | point nonexistent |
| event occurrence unresolved | point existence unsupported |
| event known, value lost, placement known | measure may be missing |
| event known, day placement lost, value known | placement unsupported; total may remain establishable |
| point exists but measure ineligible | not missing |
| eligibility unresolved | not yet missing |
| supported zero | supported value |
| carrier `NULL` | no analytical judgment by itself |
| `max(x @ I)` | family-forming value-order law where admitted |
| `last(x @ I; order=...)` | ordered expression, not family |
| `level.last` with one governed completion | compatibility shorthand; canonicalization exposes contract |
| `level.last` with several order readings | Clarify |
| `last` with no governed order | Refuse |
| output `ORDER BY` with unresolved inner order | inner order remains unresolved |
| `mean(revenue)` with several identity-bearing input anchors | Clarify; not missing data |
| unknown/non-governed anchor | geometry/anchor-standing failure, not missing value |

---

# 15. Remaining work before implementation reconciliation

The main semantic architecture is now substantially settled.

The remaining language work is narrower:

1. exact clause-level migration from the current Manual into this semantic spine;
2. final grammar decisions for ordered-expression contracts;
3. exact public spellings for standing predicates, if exposed;
4. Columna Data Types member/method/subscription catalog;
5. exact Manifold declaration syntax for promoted objects;
6. capability-registry schema reconciliation;
7. Core profile table regeneration under the corrected semantic categories;
8. Introduction and Primer reconciliation.

None requires reopening the ToD/Frame-QL boundary established here.

---

# 16. Status

This draft is a **canonical-language candidate**, not the currently shipped Manual.

It is intended to become the semantic target against which the current Manual, capability registry, profiles, parser, planner, and build are reconciled.

No implementation work is authorized by this document.

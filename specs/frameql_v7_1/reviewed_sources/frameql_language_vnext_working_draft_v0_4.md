# The Frame-QL Manual — vNext Language-Law Candidate

**Working Draft 0.4 — 7 September 2026**  
**Status:** Reconciled working semantic target; not the shipped Manual.  
**Theory reference:** [ToD v7.1 Full Manuscript Working Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md), abbreviated **T** below.  
**Scope:** Expression and request meaning, evidence and reuse obligations, and compatibility boundaries. This is not a complete grammar reference or a release-conformance claim.  
**No DOI assigned. Not a syntax release. Not an implementation authorization.**

This candidate succeeds Language-Law Candidate 0.3 for the local working program. The [authority and supersession index](frameql_v7_1_authority_and_supersession_index_v0_1.md) identifies its supporting notes and the older rules withdrawn for current design. It does not replace a published edition, change repository files, or establish that current code conforms to the successor theory.

**Reading notation.** Fenced `frameql` examples retain familiar envelope forms; they were not executed in this documentation pass. Fenced `text` expressions and mathematical formulas describe semantics and do not claim parser acceptance. The applicable versioned grammar determines formal syntax, the language reference its versioned meaning, the profiles their obligations, and measured build records implementation coverage. T determines analytical family law. These responsibilities are distinct.

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

This candidate states the proposed reconciled language meaning. It is not a replacement for the applicable shipped reference until separately adopted.

The Core Profile states what a conforming Core implementation undertakes to realize.

The Platform Profile states what Platform adds beyond Core.

Build Status records implementation coverage measured for a particular build. A coverage result is not, by itself, a proof of the complete analytical contract.

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

It does not redefine them. The authored Manifold supplies the selected logical definitions; separate private mappings and runtime evidence realize them. Physical bindings do not become authored analytical law.

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

Profiles may undertake different subsets of canonical language capabilities. Their declarations do not execute those capabilities or change their meaning.

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

An admitted canonical analytical construction can denote a family without a separate business name. An output label does not establish that law, publish a declaration, or ratify a new analytical identity (§11).

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

Restriction must preserve the declared formation scope. A request-local law may deliberately form its inputs within the stated restriction. A previously constituted contextual quantity must not silently be re-formed under a new context while retaining the same claim. Selecting already-established daily changes differs from restarting the predecessor relation inside each selected group. Physical predicate pushdown is permitted only where that equivalence is established; this is a semantic obligation, not a new clause or prescribed plan. See T §§3.1–3.4 and §10.2.

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

These are language distinctions, not a proposal for mutually exclusive runtime enum values. Some descriptions overlap: an ordered family-forming expression is both ordered and family-forming. They are not additional ontological kinds in Theory of Data.

## 3.1 Family reference

Example:

```text
revenue
```

A family reference resolves to one governed measure-family identity.

It can be anchored.

Its family identity and constitutive analytical lineage are resolved from governed declarations. The chosen realization path and proof method for an already specified target do not create another family identity.

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

Conceptual examples include:

```text
sum(revenue @ {order})
mean(revenue @ {order})
variance(price @ {transaction})
count(order)
```

Where the complete admitted analytical law applies, a canonical family expression can denote the resulting family. It need not first receive a noun-like business name. Operator spelling alone does not supply the law: the target, formation, constitutive anchors, participation, basis adequacy, and admitted continuation must be established under T §4.

The inner anchor remains identity-bearing when changing it changes the quantity. `mean(revenue @ {order})` and `mean(revenue @ {customer})` need not denote the same family even when reported at the same outer anchor. Syntax, catalog membership, a query alias, or code execution does not replace this admission judgment.

Family-forming and ordered are not mutually exclusive classifications. An admitted ordered law is one case of this same family contract.

## 3.6 Ordered analytical expression

An ordered expression uses a governed order of analytical points. Whether it denotes a family is a separate question about its complete analytical law.

T §§7–8 admits finite FIRST/LAST constructions through an independently constituted witness-valued family and a value-returning target family. General contextual expressions such as LAG, ranking, cumulative, and rolling operations need their own domain and operator contracts. Their focal syntax does not itself establish continuation, but a contextual formation history does not categorically prohibit a subsequently governed family (§6.10).

The earlier distinction between value order and analytical-point order remains useful: MAX compares operand values; LAST selects a point under the constitutive analytical order and returns its associated value. Both can belong to admitted family constructions. Neither is admitted merely by its name.

All such constructions must be invariant to incidental evidence enumeration to the extent claimed by their analytical laws. Backend row order, storage layout, and output `ORDER BY` supply no hidden inner-order authority. Chapter 9 describes the ordered-family and contextual-expression cases without merging their distinct requirements.

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

## 4.7 Anchoring and family identity

This expression:

```text
(revenue / orders) @ {region}
```

can be a lawful result without creating a durable `AOV` measure family.

A complete governed analytical law can establish a family from a suitable expression. Its canonical family expression can then denote that identity without a separate business name. The act of anchoring an arbitrary arithmetic expression does not perform that admission, and `AS` or `WITH` does not publish or ratify it (§11).

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

**T §4 is the governing family-law contract.** This language candidate references that contract rather than maintaining a competing shortened admission rule.

In particular, a family must specify its asserted target, either through a nominated non-circular defining construction or an independent semantic specification over the governed inputs and contributions. Candidate bases are checked against that target; agreement among bases cannot supply a missing target specification. The same law fixes formation, constitutive ancestry and parameters, admitted anchors and movements, participation and coverage, semantic value requirements, sufficient-state constructors and adequacy, and empty or undefined cases.

Frame-QL must resolve which admitted target and which meaning-bearing parameters the request selects. It must distinguish an absent or ambiguous definition from inadequate present evidence or unsupported implementation. A catalog entry stated at incomplete contract depth does not become realizable merely by appearing in an example here.

Canonical names resolve the identity; they do not mint it. Constitutive formation is identity-bearing where the law makes it so. A choice between compatible realizations or proof methods for the same specified target is not.

## 6.6 Sufficient state belongs to analytical law

For a target family F, an admitted basis is a collection of ordinary families whose established measures at A construct F@A under its law. T §§5–6 defines adequacy, well-foundedness, and coherence. Frame-QL consumes those obligations; it does not infer sufficiency from a type name or matching display.

For exact MEAN, SUM and COUNT supply one admitted basis. A finalized mean alone does not generally supply continuation state. An exact multiset can supply an alternative basis under the same participation law, while a set that discards multiplicity cannot replace it: the mean of `0, 0, 6` is 2; the mean after deduplication is 3.

Three questions remain distinct: whether a basis is valid for the target, whether its required measures are available in the present evidence, and whether a proposed substitution retains what a later operation requires. The two exact states `(sum=10,count=1)` and `(sum=1000,count=100)` both display 10, but adding `(20,1)` produces 15 and `1020/101`. Current display agreement is not continuation equivalence.

This also separates intake from continuation. Adding two retained counts 37 and 12 yields 49; treating them as two raw observations and counting them yields 2. The requested law determines which operation is intended.

An unavailable basis does not prove that the target is unavailable through every admitted argument. Conversely, an available scalar target does not prove that a particular basis is retained. Chapters 8–10 carry these distinctions into evidence, explanation, and reuse.

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

An exact finite set or multiset can retain a growing amount of evidence. Failure to provide a bounded-size sketch is not proof that no finite exact sufficient basis exists. Analytical adequacy and the cost of a particular representation remain different questions.

## 6.8 Family aliases and governed named families

A Manifold may already declare a governed family whose law corresponds to an explicit family-forming expression.

For example, a governed `revenue` family may already be the family established by the relevant sum law.

Where identity, participation, and law agree, canonicalization may resolve the explicit construction to the governed family identity.

This is governed identity resolution.

It is not string aliasing.

## 6.9 Availability is profile-specific

A theoretically admitted law is not automatically a ratified language construct, a profile obligation, or an implemented operation. Those claims require their own versioned authorities. This chapter makes no new availability or implementation-conformance claim.

Exact semantic requirements also remain distinct from an approximate realization of the same target. Under T §10.9, an HLL estimate may target exact count distinct under an explicit approximation contract; it is not an exact sufficient-state basis for that target. Approximation does not automatically create another family identity, and it cannot excuse an undefined computation.

## 6.10 Contextual formation and later continuation

A contextual expression can be the input to an admitted family construction only when the target, constitutive formation and participation, empty or undefined cases, an independently establishable adequate basis, and coherent admitted continuation are specified. The continuation must not change the formation. These are the same T §4 obligations, not a new admission test.

For example, governed predecessor formation over `100, 110, 95, 105` yields changes `10, -15, 10`. Summing those established changes yields 5 under regrouping. Recomputing changes separately inside `(100,110)` and `(95,105)` yields 20 because it omits the boundary change. That is changed formation, not an alternative continuation of the original construction.

Faithful recomputation using the same governing formation and adequate evidence remains possible; caching is not a theoretical requirement. Ordinary LAG, rank, cumulative, or rolling syntax neither supplies a family contract by itself nor makes such a contract impossible merely because formation uses context.

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

`level.last` requires resolution to its complete governed analytical meaning; an admitted FIRST/LAST family law is possible, while the legacy spelling alone supplies no proof of that contract.

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

## 8.1 Standing questions precede carrier interpretation

A missing row, SQL NULL, NaN, absent JSON field, or failed conversion is a realization observation. It does not determine an analytical judgment by itself. T §§2.3 and 9 distinguish point existence, eligibility, evidence support, and supported values; the earlier R4 work additionally identifies support for placing an existing point under a governed anchor.

These are dependencies of particular claims, not a mandatory all-input pipeline. A request needs evidence sufficient for its actual law. The point whose existence or placement is unresolved must be identified: it may be a contributing point, not the already-established output point.

## 8.2 Point existence and placement

An existence law specifies what makes a root point belong to the universe. Evidence may establish existence, establish nonexistence, or leave a candidate's existence unresolved. Absence from a surviving physical table alone does not prove nonexistence.

When a point is known to exist and A is a governed anchor, partition law determines its unique A-block. Evidence may still be insufficient to identify that block. This is an unavailable placement judgment, not an invalid partition and not necessarily an unavailable operand value.

A known transaction can retain its value and Store placement while losing Day placement. A Store total may remain establishable; a complete Day breakdown may not. Conversely, an independently established Day output point can exist while source contributions cannot be placed into it. Do not relabel that output point nonexistent merely because its measure cannot be established.

## 8.3 Four different anchor-related failures

| Case | Meaning |
|---|---|
| A necessary input anchor is omitted | The request may have several identity-distinct readings. This is request determinacy, not missing data. |
| The referenced anchor is not governed | The requested analytical location is not established by the selected model. |
| A candidate point's existence is unresolved | The system lacks adequate evidence whether the point belongs to the governed domain. |
| An existing point's required projection is unresolved | The point is known; its membership under this particular anchor cannot be established. |

The exact refusal/clarification codes remain a versioned language and serving contract. No new code or standing enum is defined here.

## 8.4 Eligibility, support, and missing

At an established output point, a measure may be eligible, ineligible, or of unresolved eligibility. Its value is supported only where adequate evidence establishes it under the governing law.

The conceptual predicate `missing(E)` retains its narrow reading:

```text
established point + established eligibility + unsupported target value
```

It does not mean a nonexistent point, established ineligibility, unresolved eligibility, or carrier NULL. If the target point exists and eligibility is established, an upstream placement gap can be the reason the value is unsupported there. Calling that measure missing does not erase the distinct upstream cause.

This corrects the earlier overbroad precondition that every relevant contributing placement must already be established before target missingness can be described. Required evidence depends on the law; failure causes and target standing should both remain legible.

## 8.5 Lost records and point counts

Accepting a governed account that a particular transaction occurred but its record was lost can establish the point's existence independently of its values. A count of known transaction points can remain 100 while only 99 Revenue values are supported. That does not authorize a mean over the 100-point eligible population to shrink its denominator to 99.

`count(I)` and `count(x@I)` refer to different targets: point count and law-defined measure participation. A complete-case participation rule, where actually declared, defines its own contribution semantics; missing observations cannot silently establish that rule.

Loss of the whole record can affect existence evidence, coordinates, eligibility evidence, or values differently. Do not classify every known loss as universal value missingness, or every absent record as unsupported existence.

## 8.6 Target-relative evidence requirements

FIRST/LAST illustrates why a universal all-values-present rule would be wrong. With a fixed complete participating domain `s1 < s2 < s3`, known placement and order, and supported value 30 at the maximal point s3, the LAST witness can be established even when an earlier operand value is unavailable. SUM generally requires different evidence.

The converse limitation matters: a supported value at s3 is insufficient when a later eligible point may exist and affect the target. The law requires evidence about the possible winner, not simply a convenient supported value.

Under the ordinary last-participating-point law, an unsupported selected operand is not replaced by an earlier supported value. “Last participating point's value” and “last supported value” are different targets unless an admitted equivalence establishes otherwise.

## 8.7 An unavailable staged plan need not make the target unavailable

In T §9.5, participation and order of `s1 < s2 < s3` are known. The value at s1 is unavailable; s2 and s3 have supported values 20 and 30. An intermediate anchor separates `{s1}` from `{s2,s3}`. The first exact intermediate witness is unavailable, yet the coarser witness `(s3,30)` is established by the maximality evidence.

A plan consuming every intermediate witness cannot simply run with those missing inputs. Another adequate derivation can establish the target. In particular, **the unavailable intermediate witness must not be replaced by the known-empty identity**. Admitted movements do not by themselves establish a staged plan's evidence premises.

## 8.8 A scalar can be established without an identified winner

T §9.6 supplies a bounded value-only argument. Under a fixed LAST law, suppose `p < q`, p definitely participates, participation of q is unresolved, p and q exhaust all possible participants, and their operand values are supported as 7. The target is known nonempty; every possible winner has supported value 7. Thus scalar LAST is established as 7 while the winning point identity is not.

This argument requires **the fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner**. Equal observed values among surviving records are not enough. It establishes the scalar only, never a fabricated witness. These are premises of this particular argument, not a universal necessity test for all value-only establishment.

## 8.9 Empty contribution, unsupported value, and zero

The identity of a state-combination law represents known-empty contribution under that law. It is not semantic NULL and is not a replacement for unknown evidence. MIN/MAX may instead use a semigroup over nonempty supported fibers; no artificial empty value is required.

A supported zero is an ordinary established value. An absent observation can establish zero only under the applicable existence, participation, coverage, and completion law. `coalesce(E,0)` cannot manufacture that authority merely through a familiar spelling.

## 8.10 Frame-level consequence

A returned frame must not claim completeness after silently losing eligible evidence. Nor can a later disclosure validate a computation whose required participation was never established. In particular, removing an unplaced output row after an ordered walk does not undo that row's contribution to cumulative or predecessor results.

A partial-result contract must say which result is actually established and what is withheld. This document neither overturns the recorded R4-C0 empty-frame-with-disclosure decision nor certifies the current implementation as complete R4 support. Reported remaining ordered-path defects are not closed by this text.

## 8.11 Introspection remains a separate language decision

`exists`, `eligible`, `supported`, and `missing` above are conceptual names. Their public grammar, availability, unknown-case behavior, and wire representation are not finalized here. They inspect different analytical judgments; they are not generic functions over a nullable scalar domain.

---

# 9. Ordered families and contextual ordered expressions

## 9.1 Order is a semantic dependency, not a family veto

Analytical-point order and evidence enumeration are different. An admitted family can depend on a governed order of analytical points while its continuation is invariant to the order in which compatible contributions are processed. T §§7–8 provides the finite FIRST/LAST construction. Nothing in this chapter certifies every operation called `first` or `last`.

The MAX/LAST contrast concerns what is compared: operand values versus constitutive analytical points. It does not decide family standing. The complete target and family-law contract decides that question.

## 9.2 Constitutive ordered support

For the admitted construction, S is an ordinary constitutive input anchor. Its governed constituent anchors A1 through An jointly identify its existing points:

```text
q: S ↪ product(A1, ..., An)
```

The image need not fill the Cartesian product. Governance supplies a complete analytical-point order within each constituent anchor and a complete precedence among those constituents. Their lexicographic composition determines the order on existing S-points. This is the initial construction admitted by T, not a claim that every possible product order must be lexicographic.

A complete Day chronology does not automatically supply global Customer-Day order. When the claimed support is the whole compound space, its constituent orders and precedence must be established. A narrower fixed-customer context does not acquire cross-customer continuation because several customers happen to appear in the carrier.

Order structure is part of the identity where it constitutes the family law. Output-coordinate listing order, lexical identifier order, a lineage named `calendar`, and physical insertion order cannot silently supply it.

## 9.3 Form analytical points before selecting them

FIRST/LAST consumes established analytical support points under the declared law, not arbitrary finer carrier rows. Several Product records beneath one Account-Day point must first establish the operand at that Account-Day anchor. This does not authorize choosing SUM by convenience: the operand's governing formation determines the value.

If distinct support points are still indistinguishable under the supplied order representation, the claimed complete order is unestablished. The foundational FIRST/LAST construction has no generic physical tie-breaker. The valid response is to identify the missing law or failed realization premise, not append a row ID.

## 9.4 Witness family and value-returning family

T §8 defines a witness-valued family W independently from the operand, support order, and participation. It then defines a value-returning target L. Under an admitted nonempty construction:

```text
W@A = selected original support point with its value
L@A = value(W@A)
```

The witness family supplies sufficient state for the scalar target and may itself continue by the admitted extremum-witness law. The scalar does not generally retain the point needed for later witness comparison. Family standing and scalar re-entry sufficiency are separate facts.

A rich retained point–value family R supplies an alternative basis and an exact compatible-union-to-witness compression. R, W, and L are mathematical family names, not mandatory API names, types, storage stages, or separate public declarations. The language refers to T's proofs; it does not define another witness algebra here.

## 9.5 Continuation preserves original-point witnesses

For admitted `S ⪰ B ⪰ A`, intermediate states retain their original S-point witnesses and compare them under the same constitutive order. No new order on intermediate B labels is needed for that continuation.

This is not permission to cross every geometrically possible projection. The family must admit the movement and its evidence premises must hold. Selecting global LAST and summing separate customer LAST values are different constructions. A claim that LAST and another family operation commute needs its own law.

A typed tuple, governed point reference, or other faithful representation may carry the witness. The concrete CDT comparison and representation contract is a separate verification task; no nominal type named `Witness` is required by this text.

## 9.6 Contextual order and neighborhoods

LAG, LEAD, ranking, cumulative operations, and rolling operations require governed focal context. Their request semantics must determine, as relevant, the complete analytical points being considered, the comparison or positional relation, the contextual grouping, selection or neighborhood, boundary behavior, and operand participation.

For an account's daily balances the complete points may be Account-Day, not just Day labels. A contextual grouping cannot be inferred merely as “the output anchor minus the order key.” Changing presentation must not silently change that context.

A positional seven-point window differs from a preceding-seven-day range. A complete order does not alone supply a distance convention, endpoint inclusion, reset rule, or support-skipping policy. Rank may intentionally assign equal ordinal standing to equal compared values; that equality-class law is not a substitute for the complete support-point order of the foundational FIRST/LAST family.

These requirements describe contextual expression meaning. They neither automatically give the expression family continuation nor rule out a separately admitted family constructed from that expression. Section 6.10 and T §3.4 govern that admission.

## 9.7 Shorthand, output selection, and compatibility

A short ordered spelling is usable only when its governing environment determines the intended meaning under the selected language version. Completed meaning must be inspectable even when not every field is written in the query. T §7's family order is not a free query-time sort convention.

Query-level `ORDER BY` and `LIMIT ... PER` order or select the returned frame. They may happen to return the same number as an inner LAST expression, but that does not establish the same target, sufficient state, or continuation. Their legitimate use as frame selection is not prohibited merely because the results can coincide.

The published `.last` spelling and the old `FAMILY { last ORDER ... }` execution encoding are different compatibility questions. Preserve useful public reference where complete meaning can be resolved, but do not mechanically upgrade an incomplete declaration into v7.1 conformance. This document neither removes the spelling nor mandates retirement or preservation of a particular internal mechanism.

---

# 10. Resolution, canonicalization, and materialized reuse

## 10.1 Resolve the target before selecting a realization

Canonical resolution counts distinct analytical meanings, not spellings, execution paths, or available bases. Under the selected governed environment:

```text
no lawful analytical reading      → cannot serve this request as stated
one distinct analytical reading   → target resolved; evidence and realization remain to check
several user-distinguishable readings → clarify the intended target
```

The zero/one/many discipline does not turn every unavailable plan into an absent meaning. A fully specified target can remain well defined when its required evidence is unavailable. Exact disposition codes belong to the applicable serving contract.

MEAN over orders and MEAN over customers may be two meanings. SUM/COUNT and an adequate multiset construction for one fixed MEAN are two bases for one meaning. Current numerical equality does not collapse different family identities, and different valid proof methods do not split one identity.

If two meanings remain but only one is presently executable, executable availability does not choose the user's intent. Once the meaning is fixed, choosing among compatible admitted realizations need not become another intent question.

## 10.2 Four different records

Distinguish the normalized surface statement, the resolved analytical meaning, a proposed physical plan, and the evidence establishing the particular result or its premises. These are responsibilities, not a prescribed new wire schema.

A canonical surface renderer may retain a parse/render round-trip contract. The complete resolved meaning can be exposed separately; it need not be forced into unsupported surface syntax. The selected family, constitutive anchors and order, participation, and target anchor must not diverge between explanation and execution.

## 10.3 EXPLAIN states what is known and what remains to be established

EXPLAIN can show resolved meaning, proposed realization, and applicable existing assurance without executing the result computation. It must distinguish those facts from checks not yet performed and from evidence that is not applicable or current.

A data-free explanation cannot promise every disclosure a later execution will produce unless adequate applicable evidence already establishes all those conditions. A clean static explanation does not certify unobserved placement completeness, coherent inputs, or a numerical result. This is corrected successor-reference wording; it does not claim that the present EXPLAIN payload already exposes all these distinctions.

## 10.4 Input anchors and governed completion

An omitted identity-bearing anchor or law parameter may be completed only when the governed definitions determine one meaning, including any established equivalences. Default completion selects an already defined construction; it does not invent identity.

An unavailable preferred basis, cache, or engine path may be disclosed as a constraint, not used to silently select another target. Governance-controlled alternatives must remain visibly alternatives when they change the requested quantity.

## 10.5 Dots, brackets, and retained surfaces

Historical `revenue.sum` may resolve to a governed sum-family reference or construction. Historical `level.last` may resolve to an admitted ordered family where the full contract exists. Neither dotted spelling decides family standing or proves the current execution encoding faithful. Normalization must respect constitutive anchors, input formation, and retained information; it is not a string substitution.

In this working target, `[]` remains reserved for semantic-value subscription, not the earlier analytical bracket-filter roadmap. That supersedes the roadmap recommendation, not an actual parser release. Exact accepted syntax remains versioned separately.

`AS` names an output key; supported `WITH` forms provide query-local reuse. Neither ratifies an analytical law or grants institutional publication authority. Section 11 distinguishes these acts from canonical family denotation.

## 10.6 Retained content, established claim, and permitted reuse

A catalog entry saying only “LAST at A is available” is insufficient for deciding reuse. T §10.7 distinguishes:

| Retained content | Established claim | Reuse boundary |
|---|---|---|
| Nonempty witness W@A | Selected point and associated value under the applicable evidence | Scalar projection and admitted witness continuation under compatible premises |
| Scalar L@A after valid witness finalization, witness no longer retained or recoverable | The scalar target | No inferred witness reconstruction or continuation |
| Scalar L@A established without identifying the winner | The scalar target under its adequate argument | No selected-point claim or inferred witness capability |

The last two rows can have the same family identity and value. Their establishment records and retained capabilities differ. The third row includes the specific argument of §8.8 only under its fixed law, known nonemptiness, exhaustive possible-participant coverage, and supported equal values at every possible winner.

An established witness can supply the scalar through its admitted constructor. The scalar does not generally supply the witness. A history recording that a witness was once used is not proof that the witness remains recoverable now.

## 10.7 Compatibility before lossy combination

A compressed winner is not a global consistency validator. If `p < q`, one source's `(p,10),(q,20)` compresses to `(q,20)` and can hide a conflicting `(p,11)` supplied later. A local equal-point conflict exception does not establish coherent inputs after the conflicting point has been discarded.

The evidence and context required for combination must be established outside that lossy shortcut. Matching context labels alone do not prove the premise. Nor does this require a full source-record set in every witness: a sufficient assurance or recoverability account can establish the needed compatibility. The concrete mechanism is outside this language revision.

## 10.8 Reuse is specific to the next operation

Witness coarsening does not automatically answer a later restriction that excludes the winner, a deletion of that winner, or changed formation. Additive summaries with overlapping contributions cannot simply be combined without compatible contribution accounting. Approximate and exact realizations of the same target are not interchangeable merely because their family IDs match.

The governing rule is the same throughout: retained information and established premises must justify the particular target and reuse being claimed. Material availability creates no additional analytical permission.

---

# 11. Family denotation, naming, and publication

## 11.1 Canonical denotation does not require a business-name ceremony

A complete admitted canonical construction can denote a family directly. Under an established MEAN law and constitutive operand, `mean(revenue@order)` can be an identity-bearing reference even before a separate human-readable name is assigned.

This does not turn arbitrary query syntax into governance authority. The target specification and family contract must already be supplied by the selected governed definitions and applicable law. Neither successful computation nor an alias proves that contract.

## 11.2 Output naming and institutional authoring are separate

An `AS` alias changes a frame column key. A supported `WITH` macro binds query-local text or expression reuse according to its language contract. Saving a query persists the request. None of these acts publishes or ratifies a new Manifold declaration.

A governed authoring process may establish a durable named definition or binding when authorized to do so. Names resolve existing identity; changes to an identity-bearing formation or law establish succession rather than redefining the old family retroactively. Proof method and physical plan remain outside constitutive identity.

## 11.3 Contextual and structural declarations

A named contextual expression does not automatically gain family continuation. A separately admitted family constructed from it must satisfy T §4 and preserve its stated formation. This applies to ordered and unordered contextual formation alike.

A categorical-looking value also does not automatically create an anchor. A structural declaration must establish the partition or explicit universe construction it claims, including contribution semantics when relationships overlap.

## 11.4 No new authoring format is specified here

This language revision does not add a Manifold kind, a `DERIVED` syntax, a publication field, or a witness type. Those are separate specification tasks. The distinction established here is semantic: denoting a family, naming an output, retaining a result, and publishing an authoritative definition are different acts.

---

# 12. Validity, adjudication, and realization

A parseable request is not necessarily determinate, supported, realizable, or authorized. The language must preserve those distinctions instead of mapping every problem to a nullable cell or an engine exception.

The selected governed model supplies the analytical laws. Resolution identifies the target and required context. Evidence establishes the applicable premises. A profile and implementation determine whether an admitted realization is supported here. Trusted execution must remain faithful to the resolved meaning. Institutional authorization and result policy remain surrounding responsibilities.

These dependencies do not require all evidence checks to run before every planning step: planning can identify missing premises, and an execution can obtain evidence. What it cannot do is silently rewrite the target, reinterpret assured declarations from physical conventions, or replace an unknown premise with a convenient default.

The planner selects the admitted route and semantic operation; execution performs that operation. Declaration is not certification, and absence of contradiction is not permission. Existing positive-admission boundaries are retained. A later disclosure cannot make an unestablished computation a lawful answer.

Refusal, clarification, partial-result contracts, and errors retain their versioned meanings. No new reason code, outcome, standing enum, wire field, or approval workflow is created by this document. Known engineering defects reported in earlier reconnaissance remain a separate correctness mission; this revision neither reproduces nor closes them.

---

# 13. Capability and profile boundary

The canonical language defines expression meaning and language standing. Profiles undertake subsets of those capabilities; build records report measured realization. T independently decides whether a construction satisfies analytical family law. A callable spelling or runtime kind does not answer all these questions.

In particular, distinguish analytical-point-order dependence, family-law admission, retained value/state capability, and the operation a representation is licensed to perform next. These distinctions do not require four new registry columns. The [rebased reconciliation plan](frameql_vnext_capability_profile_reconciliation_plan_v0_2.md) gives the constraints for a later schema review.

An implementation may route FIRST/LAST through legacy machinery while the successor theory has a different account of their admitted laws. That is a declared implementation gap or compatibility boundary, not evidence that the machinery already conforms. A displayed-value re-entry flag cannot be changed merely because ordered family admission is now possible.

No Core promise is reduced or enlarged in this document. No Platform-only dialect is introduced. Existing versioned grammar, profile files, generated capability tables, and measured build status remain unchanged. A future adoption must explicitly map language coverage, known limitations, and implementation evidence; it cannot manufacture agreement by editing generated status by hand.

---

# 14. Semantic acceptance suite

The [companion acceptance set](frameql_v7_1_semantic_acceptance_cases_v0_1.md) records the reconciled expectations with premises, expected judgments, prohibited shortcuts, and source sections. These are semantic review cases, **not executed Columna tests or a new formal proof suite**.

The principal questions are whether FIRST/LAST can be admitted without certifying legacy paths, whether a target is distinguished from its bases, whether partial evidence is handled under the actual law, whether retained content limits reuse, and whether versioned syntax/coverage stays separate from theory.

The older §14 rows that categorically placed LAST outside families are superseded. So are intermediate acceptance claims using universal formation locality or admitting TOP-k without a complete contract. The active index identifies the historical files rather than silently deleting the research record.

---

# 15. Remaining work before implementation reconciliation

The local companion set now uses one theory reference and one language-law target. Its supporting notes and supersession index must travel together when used for review. Older handoffs are not current instructions merely because a filename says “settled” or “PASS.”

This documentation pass does not decide public grammar for order declarations, typed subscriptions, standing predicates, or new authoring kinds. It does not establish actual CDT capability, choose a runtime representation, or fix reported ordered-path defects. Those require bounded interface and engineering work after their own authorization.

The draft successors of the Introduction and Primer preserve their entry-point purpose. Repository/site/deposit adoption, release-specific reference patches, and final publication metadata remain separate tasks. This local candidate must not be advertised as already shipped.

---

# 16. Status and sources

This is a local working language-law candidate aligned to T Draft 0.4, not a published language edition or implementation authorization. T remains unchanged. Its proofs and their recorded validation status are referenced, not reproduced or rerun here.

The [active-source index](frameql_v7_1_authority_and_supersession_index_v0_1.md) is the reading entry point. The [supporting notes](frameql_v7_1_supporting_contract_notes_v0_1.md) own the order-completion, contextual-domain, standing, and order-realization explanations subordinate to this candidate. The [acceptance set](frameql_v7_1_semantic_acceptance_cases_v0_1.md) records semantic checks. The [capability/profile plan](frameql_vnext_capability_profile_reconciliation_plan_v0_2.md) records future reconciliation constraints without changing those authorities.

The source and change register supplies exact local input hashes, full-text Intro/Primer retrieval provenance, and the diff against candidate 0.3. Historical publications retain their own versioned statements. Only the active working guidance identified in this package is superseded for current design.

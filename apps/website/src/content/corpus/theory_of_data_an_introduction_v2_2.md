---
title: "The Theory of Data: An Introduction"
subtitle: "Analytical Meaning, Lawful Transformation, and Governed Results"
author: "Huayin Wang"
date: "Version 2.2 - 19 August 2026"
lang: en-US
geometry: margin=0.82in
fontsize: 11pt
papersize: letter
subject: "Accessible introduction to The Theory of Data, Version 6.1"
keywords:
  - Theory of Data
  - analytical data
  - governed analytical data
  - analytical identity
  - datum
  - universe
  - existence law
  - anchor
  - measure family
  - family identity
  - measure
  - sufficient state
  - mapper
  - reducer
  - analytical lineage
  - lawful transformation
  - analytical governance
---

**datumwise, an independent open-source research project**

**Version 2.2 — DOI pending publication assignment**

**Aligned with:** Huayin Wang, *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*, Version 6.1, Zenodo DOI 10.5281/zenodo.22013410.

---

## Abstract

The Theory of Data begins from a distinction that analytical systems often leave implicit: producing values is different from establishing what analytical object those values represent.

The Theory describes analytical data independently of current physical storage. A **datum** is one typed value at one analytical point. A **universe** establishes which root points exist under an explicit existence law. An **anchor** partitions those points into analytical locations. A **measure family** supplies a governed analytical identity, and a **measure** is that family at one anchor:

\[
\boxed{Measure = MeasureFamily @ Anchor}
\]

or simply:

\[
F@A.
\]

Version 6.1 makes one additional point operationally explicit: **identity is established before outputs are compared**. A measure family has one governed analytical identity. An immutable family ID represents that identity in a system; a canonical name such as `revenue` is its human-readable governed handle. Two derivations that claim the same family identity are required to agree under the family law and satisfied contracts. Agreement itself never creates identity.

The revision also distinguishes where governed information belongs. Some declarations define **family identity**; some govern **edge validity**; some belong to the **certificate or materialization** layer; others are ordinary **metadata**. That separation keeps approximation, evidence grade, implementation fidelity, and display choices from being confused with the semantic identity of a quantity.

Within one universe, the primary value operators remain deliberately simple. A **mapper** preserves the anchor. A **reducer** moves from a strictly finer anchor to a coarser one. Whether a reduction preserves the same family is governed by the family law. **Sufficient state** distinguishes what can be displayed from what must be retained for lawful continuation. **Analytical lineage** records when new measure families are established from existing ones.

This paper is the systematic introduction. The shortest conceptual entry point is *A Primer on the Theory of Data*. The canonical reference is *The Theory of Data*, Version 6.1.

---

## About this introduction

The Theory of Data is a proposal about the foundation of analytical systems.

Its question is:

> **What must analytical data be so that identity, transformation, and reuse can be governed systematically?**

The paper uses familiar expressions as teaching bridges:

| Familiar expression | Theory expression | Important qualification |
|---|---|---|
| value at a key | datum | the key must identify a complete analytical point |
| population | universe | the universe has an explicit point-existence law |
| grain or analytical location | anchor | an anchor is a governed partition, not merely a column list |
| metric identity | measure family | the family is the governed quantity across lawful anchors |
| metric at a grain | measure \(F@A\) | one family at one current anchor |
| metric name | canonical family name | a human-readable governed handle resolving to one family identity |
| transformation at the same grain | mapper | the anchor is preserved |
| aggregation / rollup | reducer | the source anchor must strictly refine the target |
| retained aggregation state | sufficient state | the displayed value may be insufficient for exact continuation |
| derived metric identity | new measure family | a family-changing operation establishes a new identity |
| dependency lineage | analytical lineage | records constitutive analytical ancestry |
| requested result table | frame / result container | co-location does not by itself establish shared analytical identity |

These bridges are deliberately approximate. A SQL `GROUP BY` does not automatically establish an anchor. A named metric does not automatically establish a measure family. A column copied onto finer rows does not automatically create the corresponding finer-anchored measure.

The formal vocabulary exists to make those differences explicit.

# 1. An analytical request asks for data, not a production procedure

Suppose a person asks for revenue by customer and month.

The request appears simple. Yet an ordinary workflow may require someone to know which revenue definition is authoritative, which records belong to the relevant population, which date determines month, how customers are identified, whether returns are included, which relationship path is valid, whether a join duplicates contribution, and whether an existing materialization can be reused.

The person asked for a result.

The analyst is often required to supply both the result and the procedure that produces it.

This coupling feels natural because analytical systems expose storage and processing structures directly. Analysts see rows, tables, schemas, joins, filters, grouping expressions, and execution plans, so analytical questions are routinely translated into operations over those objects.

The requested object, however, is a governed quantity at an analytical location.

If \(Revenue\) is a governed measure family and \(CustomerMonth\) is an anchor, the requested measure is:

\[
Revenue@CustomerMonth.
\]

That notation identifies the analytical object before any table or SQL plan is chosen.

This gives the Theory its first practical separation:

> **Represent what the data is independently of how the data is currently stored and produced.**

Tables, files, APIs, dataframes, caches, indexes, and SQL remain implementation mechanisms. A customer-month Revenue measure may be served from transactions, a monthly aggregate, a service response, or a cache. Physical realization can change while the governed analytical identity remains stable.

# 2. A datum is a value at an analytical point

Begin with one value:

```text
420
```

By itself, it is insufficient to identify an analytical datum. It could be an amount, a count, a temperature, an identifier, or an error code.

Now bind it to a typed analytical point:

```text
(customer = C17, month = 2026-07) -> USD 420
```

A **datum** is one typed value at one analytical point.

The datum is more than the scalar `420`. Its meaning depends on what the value is a value of and where it lives analytically.

A database key may physically encode that point. A row may carry the value. The analytical definition comes from the governed point and value type.

This is the smallest version of a broader principle:

> **Storage tells us where a representation is kept. Analytical structure tells us what the represented value is about.**

# 3. A universe tells us which points exist

Suppose an analysis uses `{store, day}` coordinates.

Which store-days exist?

- every possible store-day?
- only days on which a sale occurred?
- every day a store was open?
- every contractual reporting day?

Those choices describe different analytical worlds.

A **universe** establishes a governed root-point domain under an explicit **existence law**.

The existence law answers:

> **What makes a root point exist here?**

Occurrence-based existence is familiar. A transaction point may exist because a transaction occurred under the governed recording rule.

Declared or generated existence is equally important. A store-day may exist because a store calendar declares that the store was open, even if no sale occurred. A scheduled visit may exist before an outcome is observed. A future reporting date may exist because a planning calendar generated it.

These forms are often described as event-like and spine-like universes. Version 6 keeps the more general existence law as the foundational object.

This immediately explains why a missing row is not self-interpreting.

A point may be absent because it never existed in the universe. A point may exist while the measure is ineligible. A point may exist and be eligible while support is unavailable. A point may exist, be eligible, and have value zero.

The database can encode several of these with an absent row or `NULL`. The analytical model keeps them distinct.

# 4. An anchor is a partition of a universe

Once a universe establishes which root points exist, an **anchor** partitions those points into analytical locations.

A partition divides the universe into non-overlapping blocks. Every root point belongs to exactly one block of the anchor.

If the root domain contains store-day points, anchors might partition them by:

- day;
- store;
- month;
- `{store, month}`.

These are different analytical locations over one universe.

## 4.1 Refinement

Suppose every store-day belongs to exactly one store-month. Then `{store, day}` is finer than `{store, month}`.

Write:

\[
B \succ A
\]

when \(B\) is strictly finer than \(A\).

This is the geometry required by ordinary reduction.

Not every familiar pair of grains is nested. Calendar Week and Calendar Month can cross, so a lawful Weekly Revenue materialization may still be insufficient to reconstruct exact calendar-month Revenue.

## 4.2 Relationships, overlap, and anchor construction

Suppose a customer can have several tags.

The groups "VIP customer" and "Newsletter customer" overlap. They therefore do not form a partition of the customer universe.

A governed system has several choices.

It can declare a single-valued assignment, such as one primary category per customer.

It can declare an allocation rule that splits contribution among several memberships.

Or it can establish a separate membership universe whose root points are pairs such as:

```text
(customer, tag)
```

Tag then partitions that membership universe even though it did not partition the original customer universe.

The principle is:

> **An anchor remains a partition. Overlap becomes analytical geometry only through a governed construction.**

# 5. Measure family, measure, and identity

A **measure family** is a governed analytical family.

`Revenue` can name such a family.

A **measure** is that family at one anchor:

\[
\boxed{Measure = MeasureFamily @ Anchor}
\]

so:

\[
Revenue@CustomerMonth
\]

means the Revenue family at the CustomerMonth anchor.

This replaces the Version 5 distinction between a measure and its anchored *members*. Version 6 retires **member** from the core public vocabulary.

## 5.1 One family, several measures

A single family may exist lawfully at several anchors:

\[
Revenue@Transaction,
\qquad
Revenue@Day,
\qquad
Revenue@CustomerMonth.
\]

These are different measures because they live at different anchors. They belong to one family where the family law establishes coherent continuation among them.

Family membership still respects anchor geometry. Week and month may both support Revenue measures while remaining incomparable anchors.

## 5.2 Identity comes before comparison

Version 6.1 makes family identity explicit before consistency is tested.

A governed family declaration determines what analytical quantity the family denotes, where the family begins, which parent families establish it, which continuation law it carries, and which contracts are identity-bearing.

An immutable family ID can represent that governed identity in a system. The canonical family name is its human-readable governed handle.

The two therefore remain distinct:

\[
\boxed{
family\_id
\neq
canonical\_name.
}
\]

Within one active namespace version, the canonical name resolves unambiguously to one family identity.

Why does the direction matter?

Suppose two calculations both return `100`.

That agreement can occur accidentally. One calculation may include tax and another exclude it. One may allocate duplicated membership differently. One may have begun a `MAX` operation at a different anchor.

The Theory therefore uses the family declaration to establish identity first.

Then consistency can ask whether two derivations that claim the same identity agree.

> **Identity is an input to the consistency test. Agreement never creates identity.**

If an identity-bearing family law later changes, the result is a successor family identity. A later namespace version can keep a familiar canonical name while preserving both family IDs underneath it.

# 6. Transformation is movement over governed analytical objects

Measures are transformed, reduced, aligned, restricted, and used to establish new families.

Version 6 keeps the primary value-operator geometry small.

## 6.1 Mapper

A **mapper** preserves the anchor:

\[
F@A \longrightarrow G@A.
\]

The output remains at the same analytical location.

## 6.2 Reducer

A **reducer** moves from a strictly finer anchor to a coarser one:

\[
F@B
\xrightarrow{\rho}
G@A,
\qquad
B\succ A.
\]

A reduction-shaped computation has two possible analytical roles.

If the family is preserved:

\[
F@B \rightarrow F@A,
\]

the edge is a **family-preserving reduction**.

If the computation establishes a new family:

\[
F@B \rightarrow G@A,
\qquad
F\neq G,
\]

the reduction participates in a **family-establishing graft**.

The geometry concerns the anchor contraction. The family law determines whether identity is preserved.

# 7. Sufficient state is different from the displayed value

A measure may display one value while requiring richer state for exact continuation.

Suppose a daily mean is displayed as:

```text
42
```

For an ordinary exact mean, useful sufficient state is:

\[
(sum,count).
\]

The state combines lawfully:

\[
(s_1,n_1)\oplus(s_2,n_2)
=
(s_1+s_2,n_1+n_2),
\]

and the displayed mean is finalized as:

\[
s/n.
\]

A materialization that stores only the finalized mean retains the daily display while losing the state required for exact arbitrary continuation.

Exact distinct count makes the same point. The displayed cardinality `3` does not identify which three entities were counted.

Thus:

\[
\boxed{
\text{displayed value}
\neq
\text{sufficient state}
\neq
\text{analytical identity}.
}
\]

## 7.1 State laws have different staging properties

The commutative-monoid case is central because grouping and staging can be rearranged safely when the same governed contributions are combined.

Other state laws require stronger conditions.

An associative but noncommutative law may permit regrouping while preserving logical order.

FIRST, LAST, cumulative calculations, windows, and other ordered operations can require an explicit order key or richer ordered state.

Some procedures have no declared compositional summary and therefore require retained roots or richer state.

Approximation is a separate question: an approximate materialization can still target the same analytical identity while carrying a different certificate and error contract.

# 8. Family law gives local coherence

Suppose Revenue can be reduced from Transaction to Day and then from Day to Month. If the same family law and required contracts govern both stages, a direct Transaction-to-Month path should agree with the lawful staged path.

Conceptually:

\[
Revenue@Transaction
\rightarrow
Revenue@Day
\rightarrow
Revenue@Month
\]

and:

\[
Revenue@Transaction
\rightarrow
Revenue@Month.
\]

The central theorem is standard algebra in a governed setting: under a commutative-monoid state law and satisfied contracts, lawful regrouping of the same contributions produces the same target state.

The architectural contribution is where the law lives:

> **The state law belongs to the family identity, and edge contracts determine when a derivation is entitled to use it.**

This lets systems distinguish incidental execution staging from meaning-bearing analytical difference.

# 9. New analytical identities require lineage

Not every lawful operation stays inside one measure family.

A maximum begun at Order may establish `MaxOrderRevenue`.

A maximum begun at Day may establish `MaxDailyRevenue`.

Revenue divided by OrderCount may establish `AverageOrderValue`.

These are new analytical families.

Version 6 records identity-bearing construction through governed **analytical lineage**.

A single-parent example is:

```text
Revenue@Day
    |
    | MAX begun at Day
    v
MaxDailyRevenue
```

A multi-parent example is:

```text
Revenue -------\
                >---- AverageOrderValue
OrderCount ----/
```

The lineage graph records constitutive analytical ancestry.

A family governs local analytical coherence.

Lineage records where family identities came from.

# 10. Identity, edge validity, certificate, and metadata

Version 6.1 gives governed information four different locations.

| Location | What it answers |
|---|---|
| **Family identity** | What analytical quantity is this? |
| **Edge validity** | Did this derivation faithfully realize that identity? |
| **Certificate / materialization** | How exact, supported, and capable is this realization? |
| **Metadata** | What descriptive or operational information accompanies it? |

A participation rule, currency semantics, tax treatment, multiplicity rule, or identity-bearing regime can belong to family identity.

A relationship cardinality check, support condition, order contract, or allocation proof can belong to edge validity.

Exact versus approximate realization, retained sufficient state, error bounds, and evidence grade can belong to the certificate/materialization layer when the semantic target stays fixed.

Descriptions, owners, UI labels, and commentary are metadata.

This separation prevents one common governance mistake: treating every important field as part of the measure's identity.

# 11. Materialization is different from analytical identity

A measure may have several physical realizations.

`Revenue@CustomerMonth` might be:

- derived from transactions;
- stored in a monthly table;
- returned by a service;
- cached from a previous computation.

These physical routes can realize one governed analytical identity.

Conversely, two columns with the same physical type and label can represent different analytical objects.

This gives another important separation:

> **Physical lineage tells us where a representation came from. Analytical lineage tells us how the analytical family itself was constituted.**

A materialization is a realization of an analytical object. Its exactness, retained state, provenance, and evidence status can be carried in the certificate/materialization layer.

# 12. Governed knowledge has to live somewhere

The analytical facts described so far are often already known in organizations.

Someone knows:

- what Revenue means;
- what makes an OpenStoreDay exist;
- which anchors refine which others;
- whether a relationship is functional or many-to-many;
- what contribution semantics apply to overlap;
- what state exact continuation requires;
- which construction established a derived family;
- which source or materialization currently supports the measure.

The problem is that this knowledge is often scattered across SQL, semantic models, tests, documentation, dashboards, naming conventions, and experienced people's memory.

ToD's architectural consequence is that analytical knowledge can be represented as **governed data about analytical data**.

Version 6.1 also supplies a minimal conformance idea. A conforming system can carry declarations for universes, anchors, family identities, lineage edges, contracts, and certificates in a machine-readable publication.

That does not determine organizational authority. The surrounding governance system decides which conforming publication is authoritative.

The foundation only requires the analytical declarations to be explicit enough to resolve identity and lawful transformation.

# 13. Query languages can declare the result

Once analytical identity is represented independently of physical storage, a query language can ask for a governed analytical result without giving the requester authority to invent its physical construction.

Frame-QL is one language designed around this consequence.

Conceptually:

```frameql
FROM retail_manifold
SELECT revenue, orders
AT {customer, cal.month}
```

asks for governed Revenue and Orders measures at the requested output anchor.

The theoretical requirement is broader than any one language:

> **The request should be able to identify the analytical object independently of the procedure that manufactures it.**

A trusted planner can then choose joins, sources, materializations, and backend execution.

# 14. AI can interpret without becoming analytical authority

The same separation creates a natural role for AI.

A model can:

- interpret ordinary language;
- search semantic and local knowledge;
- propose candidate governed meanings;
- map user vocabulary to known measure families;
- ask clarifying questions;
- explain ambiguity or unsupported requests.

Those are interpretive functions.

Analytical authority remains with the governed declarations and adjudication rules.

If "maximum revenue" could mean either `MaxOrderRevenue` or `MaxDailyRevenue`, an AI model can surface both possibilities. Where several governed meanings remain possible, the correct state is unresolved intent until the distinction is clarified.

# 15. Neighboring questions: regime, evidence, and statistics

Version 6 keeps the foundational analytical ontology small.

A **regime** is a neighboring value-generation distinction used where observational, interventional, forecast, simulated, or restated arrangements affect meaning.

**Evidence status** records how strongly a premise is supported.

**Statistical inference** asks whether governed analytical evidence supports a formal target and licensed claim.

These are important neighboring structures. They remain distinct from the smaller ToD foundation.

The Statistical Bridge develops the passage from governed evidence to inference certificates and licensed claims.

# 16. The change in perspective

The ordinary starting point of analytical systems is often the container.

The Theory of Data begins elsewhere.

A universe establishes which root points exist.

An anchor partitions those points into analytical locations.

A datum is a typed value at one analytical point.

A measure family supplies analytical identity.

A measure is that family at one anchor:

\[
F@A.
\]

Mappers preserve anchor.

Reducers contract finer anchors to coarser ones under governed law.

Sufficient state determines whether exact continuation remains possible.

Family coherence governs local path agreement.

Analytical lineage records when new families are established and where their identities came from.

Version 6.1 adds an operational identity rule:

> **Family identity is established ex ante from governed declaration. Consistency tests the consequences of that identity.**

And it separates the layers around that identity:

\[
\boxed{
\text{Identity}
\rightarrow
\text{Edge validity}
\rightarrow
\text{Certificate / materialization}
\rightarrow
\text{Metadata}.
}
\]

The dependency of concepts remains:

\[
\boxed{
Universe
\rightarrow
Anchor\ Geometry
\rightarrow
Measure\ Families
\rightarrow
Measures
\rightarrow
State\ and\ Law
\rightarrow
Analytical\ Lineage
}
\]

with **governed identity and conformance** supplying the operational layer that makes the structure machine-checkable.

The practical ambition is compact:

> **Know which analytical points exist, where a measure lives, which governed family identity it carries, what state its continuation requires, how its family was established, and which transformations preserve that identity.**

---

## Introductory glossary

| Term | Meaning in Version 6.1 |
|---|---|
| **Datum** | One typed value at one analytical point |
| **Universe** | Governed root-point domain under an explicit existence law |
| **Existence law** | Rule determining what makes a root point exist in a universe |
| **Anchor** | Governed partition of a universe |
| **Anchor point** | One block of an anchor partition |
| **Refinement** | Partial order in which a finer anchor partitions the universe more finely than a coarser anchor |
| **Measure family** | Governed analytical family carrying one semantic identity and declared family law |
| **Family ID** | Immutable system identifier for one governed family identity |
| **Canonical family name** | Human-readable governed handle resolving to one family identity within a namespace version |
| **Measure \(F@A\)** | Measure family \(F\) at current anchor \(A\) |
| **Mapper** | Anchor-preserving value operator |
| **Reducer** | Value operator moving from a strictly finer anchor to a coarser anchor |
| **Sufficient state** | State required for lawful exact continuation under a family law |
| **Edge contract \(\Gamma(e)\)** | Conditions licensing a governed analytical movement |
| **Family coherence** | Agreement of lawful staged and direct paths within one measure family where contracts hold |
| **Graft / family establishment** | Identity-bearing operation that establishes a new measure family from governed analytical input |
| **Family succession** | Establishment of a successor family after an identity-bearing family declaration changes |
| **Analytical lineage** | Directed, well-founded ancestry among measure families |
| **Support** | Availability of the evidence or value required for a measure at eligible points |
| **Certificate / materialization** | Governed realization information such as exactness, approximation, retained capability, and evidence status |
| **Materialization** | Physical realization of an analytical object |
| **Frame / result container** | Presentation or request assembly at an output anchor |
| **Regime** | Neighboring value-generation distinction used where observational/interventional structure matters |

---

## References and reading path

Wang, Huayin. 2026a. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 6.1. Zenodo. DOI: 10.5281/zenodo.22013410.

Wang, Huayin. 2026b. *A Primer on the Theory of Data*. Version 2.2. DOI pending publication assignment.

Wang, Huayin. 2026c. *The Theory of Data Applied: Classical Analytical Failures as Problems of Identity, Geometry, State, and Law*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21959941.

Wang, Huayin. 2026d. *A Primer on the Theory of Data Applied: Why Familiar Analytics Rules Are Stranger Than They Look*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21960380.

Wang, Huayin. 2026e. *Analytical Governance: From User Intent to Governed Analytical Execution*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21959749.

Wang, Huayin. 2026f. *Frame-QL: An Introduction — Query by Declaring the Result*. Version 2.1. Zenodo. DOI: 10.5281/zenodo.21966453.

Wang, Huayin. 2026g. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: 10.5281/zenodo.21979821.

Wang, Huayin. 2026h. *A Contract Calculus for Governed Analytical Transformation: Totality, Partiality, Population, Expansion, and Fan-Out*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21752373.

---

## Revision note

**Version 2.2.** This targeted revision aligns the Introduction with *The Theory of Data*, Version 6.1 while preserving the Version 2.1 teaching architecture. It makes ex-ante family identity explicit; separates family ID from canonical family name; distinguishes family identity, edge validity, certificate/materialization, and metadata; explains governed paths from overlapping relationships to partition anchors; introduces family succession; and marks the broader state-law boundary. The teaching sequence remains unchanged.

**DOI:** pending publication assignment.

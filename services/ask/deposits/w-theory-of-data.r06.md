---
title: "The Theory of Data"
subtitle: "A Foundation for Analytical Identity, Derivability, and Consistency"
author: "Huayin Wang"
doi: "10.5281/zenodo.22013410"
version: "6.1"
license: "CC BY 4.0"
date: "Version 6.1 - 19 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.85in
fontsize: 11pt
subject: "A foundational framework for governed analytical identity, derivability, consistency, and lineage"
keywords:
  - Theory of Data
  - analytical identity
  - analytical governance
  - measure family
  - measure
  - anchor
  - universe
  - lineage
  - sufficient state
  - semantic layer
  - governed analytics
header-includes:
  - |
    \usepackage{microtype}
  - |
    \usepackage{booktabs}
  - |
    \usepackage{longtable}
  - |
    \usepackage{array}
  - |
    \usepackage{enumitem}
  - |
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{mathtools}
  - |
    \usepackage{fancyhdr}
  - |
    \usepackage{url}
  - |
    \linespread{0.97}
  - |
    \setlist{nosep}
  - |
    \setlength{\emergencystretch}{3em}
  - |
    \clubpenalty=10000
    \widowpenalty=10000
    \displaywidowpenalty=10000
  - |
    \pagestyle{fancy}
    \fancyhf{}
    \fancyhead[L]{\small The Theory of Data}
    \fancyhead[R]{\small Huayin Wang}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \setlength{\headheight}{14pt}
  - |
    \urlstyle{same}
---

**datumwise, an independent open-source research project**  
**Version 6.1 - 19 August 2026**  
**DOI:** 10.5281/zenodo.22013410  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Supersedes:** *The Theory of Data*, Version 6.0, DOI [10.5281/zenodo.21958062](https://doi.org/10.5281/zenodo.21958062)


## Abstract

A value becomes data only when it is bound to something it is about. This observation leads to a foundational problem for analytical systems: values, rows, tables, and operators can be physically well formed while the analytical objects they claim to represent remain under-specified.

The Theory of Data (ToD) develops a compact ontology for those analytical objects. A **universe** establishes a governed root-point domain under an explicit existence law. An **anchor** is a governed partition of that universe. A **measure family** supplies analytical identity and family law. A **measure** is one family at one anchor:

$$
F@A.
$$

Version 6.1 makes the identity criterion operationally explicit. Family identity is determined **ex ante** from a governed semantic signature, independently of agreement or disagreement among computed outputs. An implementation may assign an opaque immutable `family_id` to that signature; canonical names remain governed resolvable handles. Identity is therefore an input to a consistency test, never an inference from its result.

The revision also separates four locations for governance information: **family identity**, **edge validity**, **certificate/materialization**, and **metadata**. Population and participation semantics, multiplicity, units, regimes, and other meaning-bearing rules belong to family identity when they change the quantity or its declared family law. Edge predicates determine whether a particular derivation faithfully realizes that identity. Exactness, approximation, retained capability, and evidence grade belong to the certificate/materialization layer when the semantic target is unchanged. Metadata remains outside all three.

Inside a measure family, the central coherence theorem uses commutative-monoid sufficient state. The underlying algebra is standard; ToD's contribution is architectural: the state law is attached to family identity and edge contracts so that staging equivalence becomes a governed property. The revision makes the boundary explicit through a state-law taxonomy covering commutative, order-sensitive, ordered/stateful, and non-decomposable cases.

Partition anchors remain foundational. Many-to-many membership, overlapping cohorts, and fractional allocations are handled through governed assignment, allocation, expansion, or derived membership universes while partition geometry remains intact. Multi-parent lineage is illustrated with Average Order Value. A minimal conformance appendix shows how universes, anchors, families, edges, certificates, immutable IDs, and semantic signatures can be declared without making organizational authority part of the ontology.

The resulting claim remains narrow. ToD governs analytical identity, derivability, consistency, and materialized capability under declared premises. Empirical truth and statistical warrant require their own evidential grounds.

# 1. Introduction

Suppose you find the number:

```text
42
```

Is it data?

Not yet. It is a value. It could be an age, a temperature, a quantity, a price, an identifier, or an error code.

Now write:

```text
age = 42
```

The value has acquired a type of meaning. Write:

```text
John's age = 42
```

and the statement has become an assertion about an analytical point.

This gives the Theory of Data its intellectual starting point:

> **Data is always something about something else.**

The smallest meaningful analytical assertion is a value bound to a governed analytical point. The Theory calls this a **datum**.

That observation immediately raises deeper questions. What makes the analytical point exist? How is it related to other points? When several datums describe the same kind of quantity, what structure makes them one analytical object? When may that object move from one analytical location to another? When do two derivations produce the same quantity, and when do they produce different quantities that merely look similar?

Those questions are surprisingly difficult to answer from ordinary data-system primitives.

A table can store values without telling us which analytical transformations preserve their meaning. A valid join can duplicate contribution. A valid `SUM` can aggregate a quantity along a direction where addition does not preserve its identity. A monthly average can be calculated from daily averages even after the sufficient state needed for the true monthly average has been lost. Weekly and monthly Revenue can both be lawful analytical objects even though neither is derivable from the other. Two operations named `MAX` can create different quantities when they begin at different analytical locations.

These failures arise from ungoverned analytical identity and derivation even when the arithmetic is valid.

The Theory of Data asks:

- What analytical points exist?
- How are those points organized into analytical locations?
- What does it mean for a quantity to exist at one of those locations?
- Which analytical transformations preserve a quantity's identity?
- Which transformations establish a new quantity?
- How is a derived quantity rooted in the universe?
- When are different lawful derivations guaranteed to agree?
- What information must survive for a lawful derivation to remain executable?

The aim of v6 is to answer these questions with a small foundation.

## 1.1 Intellectual order and formal dependency

The Theory begins intellectually with datum because datum exposes the problem: a value must be about something.

Formal treatment then moves one step backward. Before a datum can exist at an analytical point, the Theory must say what makes that point exist and how such points are organized. That leads to universe and partition geometry.

The expository movement is therefore:

```text
value
  -> datum
  -> analytical point
  -> universe
  -> anchor
  -> measure family and measure
  -> operator
  -> lineage
```

while the formal dependency is closer to:

```text
universe
  -> anchor
  -> anchor point
  -> datum
  -> measure
  -> operator
  -> measure family coherence
  -> lineage
```

There is no contradiction between the two. One explains why the Theory is needed; the other supplies the structure that makes the objects well-defined.

## 1.2 Terminology and succession from Version 5

Version 6 deliberately changes two central terms from Version 5 (Wang 2026a). The change is small in vocabulary but important in structure.

| Version 5 | Version 6 |
|---|---|
| datum | datum |
| member of a measure | **measure** |
| measure | **measure family** |
| anchored member identity | **measure-family @ anchor** |

The term **member** is retired from the core v6 ontology. What Version 5 called a member of a measure is now simply a **measure**: one uniquely governed measure family at one anchor. What Version 5 called a measure is now called a **measure family**.

The reason is the identity form developed in this paper:

$$
\boxed{
\text{measure}=\text{measure family}@\text{anchor}.
}
$$

The revision preserves the governed objects of Version 5 while clarifying their roles. A v5 object described as a Revenue member at month corresponds, under the v6 terminology, to the measure:

$$
revenue@month.
$$

This succession note is normative for reading the two versions together. Downstream specifications and implementations may retain v5 vocabulary during migration, but the v6 terms in this paper define the current theoretical usage.

## 1.3 What ToD governs

ToD is a theory of **governed analytical data**. Storage, query syntax, physical execution, business vocabulary, and statistical inference belong to neighboring jurisdictions.

Given a declared universe, partition geometry, measure-family identities, operator laws, sufficient state, lineage, and the contracts required by a derivation, ToD aims to establish:

1. **analytical standing** - whether a family and its measures have governed ancestry in the universe;
2. **analytical identity** - what measure family is being named and at what anchor the measure exists;
3. **derivability** - whether a requested measure can be lawfully derived from governed analytical objects already available;
4. **consistency** - whether derivations that claim the same governed identity are required to agree;
5. **materialized capability** - whether an available representation retains the state required to perform the lawful derivation.

ToD establishes the analytical structure of a claim. Factual correctness, business judgment, and statistical or causal warrant require their own evidence and governance.

The full **evidence-status calculus** by which governance premises are established, challenged, or updated belongs to the surrounding governance system. A surrounding governance system may distinguish states such as verified, corroborated, assumed, proposed, contradicted, or untestable. ToD v6 requires those statuses to remain available where they affect a claim. The foundation here specifies the analytical structure and contracts whose premises such evidence statuses qualify.


Version 6.1 also distinguishes **structural conformance** from **institutional authority**.

ToD can specify what a conforming analytical declaration must contain and which consequences follow from that declaration. It can require immutable identifiers, explicit semantic signatures, designated roots, family laws, edge contracts, lineage, and certificate references. Institutional authority to publish one declaration or another belongs to the surrounding governance process.

The boundary is:

$$
\boxed{
\text{ToD checks the structure of a selected governed publication;}
\quad
\text{institutional governance selects the authoritative publication.}
}
$$

Appendix A gives a minimal implementation-neutral conformance surface.

## 1.4 A foundation, not a manual

Analytical systems must eventually deal with missingness, ordered state, fan-out, allocation, cross-universe movement, approximation, regimes, provenance, materializations, and many other issues.

The foundation becomes stronger by keeping the primitive set small and routing secondary concerns to explicit contracts and adjacent layers.

The editorial and conceptual rule of v6 is:

> **Keep a distinction in the foundation when it changes analytical identity, derivability, consistency, or the validity of those claims. Otherwise treat it as a contract, consequence, or application of the core.**

This paper therefore develops the central structure and marks its important boundaries. Detailed application belongs elsewhere.

## 1.5 The central architecture

The compact architecture is:

```text
Universe Existence Law
  -> Root-Point Domain
  -> Partition Geometry
  -> Datum and Measure
  -> Operators and Sufficient State
  -> Measure Family Coherence
  -> Lineage DAG
  -> Analytical Governance
```

The most important change in v6 is the relationship between **measure family** and **lineage**.

A measure family is the basic algebraic unit in which ToD proves staging invariance:

$$
\boxed{
\text{coherent family path}
\Rightarrow
\text{derivability + path consistency}
}
$$

Analytical governance extends beyond the family into identity-bearing lineage, contracts, and materialized capability.

The universe-wide lineage graph is itself governed. Measure families are its nodes. Family-establishing derivations connect those nodes directionally. The graph determines analytical ancestry and therefore identity.

The central distinction is instead:

$$
\boxed{
\text{Measure Family}
\rightarrow
\text{local algebraic coherence and path compression}
}
$$

and:

$$
\boxed{
\text{Lineage Graph}
\rightarrow
\text{governed analytical ancestry, identity, and derivation}
}
$$

## 1.6 Relation to prior work

ToD connects established work on provenance, multidimensional aggregation, summarizability, and governed metrics around a specific object: **governed analytical identity**.

Database provenance asks where data came from and how query results depend on source data. Buneman, Khanna, and Tan (2001) distinguished forms of why- and where-provenance, while Green, Karvounarakis, and Tannen (2007) developed an algebraic provenance framework based on commutative semirings. These lines of work are concerned with dependency and explanation of query results. ToD uses the word *lineage* more narrowly for analytical ancestry: a physical or query dependency becomes analytically sufficient only when it determines the families, anchors, family-changing derivations, and contracts that establish the resulting quantity. Provenance and analytical lineage can therefore be connected while remaining distinct.

OLAP and multidimensional database research developed data cubes, roll-up, dimension hierarchies, and conditions for correct summarization. Gray et al. (1997) formalized the data cube and distinguished important classes of aggregation functions; Lenz and Shoshani (1997) studied summarizability conditions; Pedersen, Jensen, and Dyreson (2001) developed multidimensional models that address complex hierarchies and many-to-many structures. ToD shares the concern that aggregation validity depends on dimensional structure. Its emphasis begins from partition geometry and makes the resulting anchored analytical quantity the object whose identity is governed.

The use of sufficient state also has clear predecessors in work on decomposable and algebraic aggregates. Associativity and sufficient statistics for AVG are established results. Their role here is to prove when a governed region of one analytical family may erase internal staging while preserving identity.

Contemporary semantic-layer architecture likewise defines reusable governed metrics, relationships, business terminology, and access rules independently of individual queries. Thoughtworks describes the semantic layer as a shared business-logic layer between data stores and consumers, including BI tools, APIs, and AI agents (Thoughtworks 2026). ToD is complementary to that architecture. It asks what conditions make a metric a unique analytical family, what an anchored realization such as `revenue @ {customer, month}` denotes, which derivations preserve that identity, and which derivations must establish another family.

The W3C PROV data model supplies a domain-agnostic provenance language for entities, activities, derivations, revisions, agents, bundles, and collections, with explicit extensibility for domain-specific information (W3C 2013). A ToD implementation can use such a provenance carrier. The analytical types introduced here remain domain-specific semantics carried by that record: family identity, anchors, family-preserving versus family-establishing edges, sufficient state, and the contracts that make those edges analytically valid.

Machine-readable data-contract standards provide another adjacent implementation surface. The Open Data Contract Standard defines a structured YAML contract covering fundamentals, schema, references, data quality, support, roles, and related producer-consumer obligations (Bitol 2026). ToD's conformance surface is narrower in jurisdiction: it specifies the declarations needed to resolve analytical identity and lawful transformation, while a broader data contract may carry operational, organizational, and service obligations alongside them.

The formalism in this paper is deliberately modest. Several propositions simply expose consequences of partition or monoid laws. Their purpose is architectural: to make explicit which analytical distinctions those laws license a governed system to preserve, compress, or refuse. The stronger claim of ToD is architectural: analytical identity can be made explicit enough that derivability and consistency become directly governable from declared semantics instead of inferred from physical data structures or familiar operator names.

# 2. Universe and Partition Geometry

A datum is meaningful only if the point it describes exists. The first formal task is therefore to establish analytical point existence and the geometry built from those points.

## 2.1 Universe and existence law

A **universe** is a governed domain of analytical point existence.

Let the universe be:

$$
U
$$

with governed root-point domain:

$$
\Omega_U.
$$

Domain membership is governed by an **existence law**:

$$
\lambda_U.
$$

The existence law answers:

> **What makes a root point exist in this universe?**

Different universes can answer that question differently. Under an **occurrence-based** existence law, a point exists because the governed occurrence happened or was admitted as an occurrence. Transaction and event universes are common examples. Under a **declared or generated** existence law, the point domain is established independently of whether a particular value is observed there. Registered entities, expected store-days, scheduled appointments, sensor-hours, and forecast horizons are common examples. Such universes are often implemented as spines.

The distinction is important. In v6, `event` and `spine` are important forms of the more general existence law and remain below the top-level primitive layer. The foundational requirement is that point existence be explicit enough to distinguish an absent point from an existing point whose value is absent.

The primitive core of the universe is:

$$
\boxed{
\{\text{root points},\ \text{primitive dimensions},\ \text{primitive measures}\}.
}
$$

Here **primitive** is relative to the declared universe. The term makes no claim of metaphysical, physical, or event-level atomicity.

A daily account state may be primitive in one universe even if another universe models the events from which that state could be reconstructed. A modeled scientific output may be primitive in a universe whose governed starting points are model runs. A transaction may be a root point in one system and a derived object in another.

ToD governs the declared universe at the finest structure selected for that analytical domain.

The dependency is therefore:

$$
\boxed{
\lambda_U
\rightarrow
\Omega_U
\rightarrow
\text{partition geometry}.
}
$$

The existence law determines which root points exist. Anchors organize those already-established points.

## 2.2 Root point and root anchor

A **root point** is a governed analytical point that cannot be broken into a finer analytical point within the universe.

The root points induce the finest anchor of the universe:

$$
R_U
=
\big\{\{\omega\}:\omega\in\Omega_U\big\}.
$$

This is the **root anchor**.

Its special status is internal to the universe:

1. no finer governed anchor exists in that universe;
2. primitive dimensions are supplied on its root points rather than derived from another dimension inside the universe;
3. primitive analytical objects are supplied under the universe declaration rather than produced by analytical operators inside the universe.

The phrase **governed root point** is important. The root is the finest point structure selected for governance in this universe.

## 2.3 Anchor

An **anchor** is a governed partition of the universe's root points.

Let:

$$
A=\{a_i\}
$$

be an anchor over universe $U$. Then:

$$
a_i\subseteq\Omega_U,
$$

$$
a_i\cap a_j=\varnothing
\qquad (i\neq j),
$$

and:

$$
\bigcup_i a_i=\Omega_U.
$$

Each block $a_i$ is an **anchor point**.

An anchor is a complete governed partition of the universe, with stronger semantics than an arbitrary grouping label.

If the anchor is `store`, each store anchor point contains the root points assigned to that store. If the anchor is `{store, day}`, each anchor point contains the root points belonging to one governed store-day block.

## 2.4 Refinement

Let $B$ and $A$ be anchors in the same universe.

Write:

$$
B\succeq A
$$

when every point of $B$ lies inside exactly one point of $A$.

If $B\neq A$, write:

$$
B\succ A.
$$

Then $B$ is strictly finer than $A$, and $A$ is strictly coarser than $B$.

### Proposition 1 - Partition projection

If:

$$
B\succeq A,
$$

then every $B$-point belongs to exactly one $A$-point.

This follows from the partition law and supplies the geometry needed by reduction.

## 2.5 Incomparable anchors

Not every pair of anchors is ordered by refinement.

Suppose `day` refines both `week` and `month`:

$$
day\succ week
$$

and:

$$
day\succ month.
$$

Ordinary calendar weeks and months overlap. A week can cross a month boundary and a month contains pieces of several weeks. Therefore, in general:

$$
week\not\succeq month
$$

and:

$$
month\not\succeq week.
$$

They are incomparable.

Incomparability is routine. Calendar year and fiscal year can be incomparable. Product and category can be incomparable even when both are valid dimensions. State and ZIP may fail to nest under the governed definitions in use.

Partition geometry therefore forms a partial order with potentially incomparable branches.

## 2.6 Dimension

A **dimension** is a conventionally named governed partition of the universe.

Dimensions give stable names to analytically important partitions such as:

```text
store
customer
product
calendar day
calendar month
fiscal year
```

The distinction between dimension and anchor is useful:

> **Dimensions name conventional partitions. Anchors are the governed partitions themselves.**

A dimension is a governed partition; hierarchy appears when two such partitions stand in a refinement relation.

Two dimensions may both be valid while being incomparable.

### Many-to-many relations do not automatically create dimensions

Suppose `product` is a dimension, and a later Product-to-Category relation permits one product to belong to several categories.

That relation does not assign every root point to exactly one category block. It therefore does not, by itself, induce a category partition of the universe.

Category is not thereby a dimension of that universe.

If both `product` and `product_category` are primitive dimensions, however, every root point has exactly one value for each. Both induce valid partitions even if the value-level relation between products and categories is many-to-many. The partitions may simply be incomparable.

This illustrates why ToD treats partition geometry as prior to familiar schema language.

## 2.7 From relationships to anchors

Partition geometry remains foundational even when business relationships overlap.

Let $C$ be a set of category labels and let:

$$
R\subseteq\Omega_U\times C
$$

be a governed relationship.

If $R$ is total and functional on $\Omega_U$, it induces an ordinary anchor directly. Each root point belongs to exactly one category block.

If $R$ is genuinely many-to-many, it does not induce a partition of $\Omega_U$. A conforming system has several governed choices.

### Assignment

A governed function:

$$
a:\Omega_U\rightarrow C
$$

can select exactly one category for each root point. The resulting blocks form an anchor.

### Membership universe

The relationship can instead establish a derived universe:

$$
\Omega_R
=
\{(\omega,c):(\omega,c)\in R\}.
$$

Category now induces a genuine partition of $\Omega_R$: every membership point has exactly one category coordinate.

Moving a measure from $U$ into this membership universe requires declared contribution semantics.

### Allocation

For conserved allocation, a weight function may be declared:

$$
w:\Omega_R\rightarrow\mathbb{R},
$$

with, where conservation is required,

$$
\sum_{c:(\omega,c)\in R}w(\omega,c)=1
\qquad
\text{for each source point }\omega.
$$

The allocation rule is analytically significant because it determines contribution in the derived universe.

### Full-touch expansion

A system may deliberately assign full contribution to every membership. That is another governed semantic choice. It generally establishes a different analytical family from conserved allocation.

This bridge covers common cases such as overlapping cohorts, multi-category membership, geographic catchments, and fractional allocation while preserving the foundational statement:

> **An anchor is a partition. Overlap is represented through governed construction, not by weakening the anchor law.**

Data-dependent grouping follows the same discipline. A governed single-valued grouping rule can induce a partition. Overlapping windows or memberships require an expanded or otherwise explicitly constructed universe.

## 2.8 Anchor expressions and common refinement

A combination of dimensions commonly denotes their common refinement.

For example:

```text
{store, day}
```

denotes the partition obtained by intersecting the store and day blocks over the governed root-point domain $\Omega_U$ established by $\lambda_U$. Empty intersections are omitted because partition blocks are, by definition, nonempty.

That last statement is geometrical. The universe existence law separately determines whether a particular store-day contributes governed root points.

In an occurrence-based transaction universe, a store-day with no qualifying transaction may contribute no root point and therefore no store-day anchor point. In a declared store-day universe, the same store-day can exist independently of whether any observed value is available there.

This distinction prevents partition geometry from silently deciding missingness or population.

It is useful to distinguish the **anchor expression** from the actual governed partition it denotes.

Two different expressions can happen to produce the same observed grouping in one dataset. Analytical equivalence comes from governed partition law; current data coincidence supplies no such proof.

Partition geometry now gives us the analytical locations required by datum and measure.

# 3. Datum, Measure Family, and Measure

The geometry tells us where analytical assertions can live. We can now define the analytical objects that live there.

## 3.1 Datum

A **datum** is one governed typed value at one anchor point.

If $a$ is an anchor point and $v$ a value, we may write informally:

$$
d=v@a.
$$

The point and value type are part of the meaning. `42` and `age = 42 at John` are different analytical assertions.

A datum is the smallest governed analytical assertion.

## 3.2 Measure family

A **measure family** is a governed analytical family with one analytical identity and one declared family law. Section 5 defines the coherence conditions for family-preserving reduction.

Version 6.1 separates analytical identity from its human-readable handle.

Every governed family has:

1. an ex-ante **semantic identity signature** $\Sigma(F)$;
2. an immutable governed **family ID**, written $id(F)$;
3. one canonical governed name within a namespace version;
4. a designated governed family root;
5. a declared family law and identity-bearing contracts;
6. governed constitutive ancestry.

The semantic signature is defined in Section 6.7. A conforming implementation may derive an opaque digest from the signature:

$$
id(F)=H(\Sigma(F)),
$$

or may assign another immutable identifier while storing the signed declaration that establishes $\Sigma(F)$.

The hash is an implementation choice. The semantic signature is the theoretical object.

A canonical name is a resolvable handle:

$$
name_U(F)\longrightarrow id(F).
$$

Within one namespace version, the mapping must be unambiguous:

$$
name_U(F_1)=name_U(F_2)
\Rightarrow
id(F_1)=id(F_2).
$$

Names support ordinary analytical reference. IDs and signatures carry identity across implementations, publications, and versioned namespaces.

Examples of canonical family names might be:

```text
revenue
inventory_level
max_product_day_revenue
cumulative_revenue
average_order_value
```

Section 6 develops the identity signature, family establishment, and multi-parent lineage.

## 3.3 Measure

A **measure** is a measure family at one anchor.

If family $F$ exists lawfully at anchor $A$, the measure is:

$$
\boxed{F@A}
$$

If the canonical governed family name is `revenue`, examples are:

```text
revenue @ transaction
revenue @ day
revenue @ {store, month}
```

This is the central identity form of v6.

> **A measure family answers what analytical quantity this is. The anchor answers where that quantity lives.**

## 3.4 One current anchor per measure

A measure has one **current analytical anchor**:

$$
F@A.
$$

The derivation that established its family can contain other identity-bearing anchors. In particular, a source or graft anchor may be preserved recursively inside the family identity $F$ when changing that anchor would establish a different analytical family.

Those ancestral anchors do not become additional current anchors of $F@A$. They explain what family $F$ is. The final $A$ still says where the present measure lives.

Thus the compact rule remains:

> **A measure has one current anchor. Reduction is two-anchor. Family identity may preserve earlier anchors when they were constitutive of the family.**

This preserves the analytical importance of input location without confusing derivation history with the current analytical location of the resulting measure.

## 3.5 Existence, eligibility, support, and value

A measure need not have an available value at every point of its anchor.

The distinctions begin one level earlier than measure support. The universe first establishes point existence through $\lambda_U$; an anchor then partitions those existing points. For measure $F@A$, let:

$$
E_{F,A}\subseteq A
$$

be the eligible anchor points and:

$$
S_{F,A}\subseteq E_{F,A}
$$

be the points at which a governed value is supported or available.

Then the realized value map may be written:

$$
m_{F,A}:S_{F,A}\rightarrow V_F.
$$

The layering is:

$$
\boxed{
\lambda_U
\rightarrow
\text{point existence}
\rightarrow
A
\rightarrow
E_{F,A}
\rightarrow
S_{F,A}
\rightarrow
\text{value}.
}
$$

This lets ToD distinguish:

1. a point that does not exist under the universe existence law;
2. an existing anchor point where the measure is ineligible;
3. an eligible point where the value is unavailable;
4. a supported point whose value is zero.

These cases can have different analytical consequences even when a physical table represents some of them by row absence or null.

The existence law is especially important when interpreting absence. In an occurrence-based universe, no qualifying occurrence can mean that no corresponding root point exists. In a declared or generated universe, an expected point can exist even when no observation is available. The same physical absence therefore need not have the same analytical meaning across universes.

Support does not silently redefine the anchor, and missingness does not define point existence.

## 3.6 Names, IDs, and analytical identity

A family name is a governed handle for an identity already established by declaration and lineage.

Thus an expression such as:

$$
revenue@\{store,month\}
$$

is meaningful analytical notation when the active namespace resolves `revenue` to exactly one immutable family ID.

The relationship is:

$$
\boxed{
family\_id
\neq
canonical\_name.
}
$$

A practical governed reference can therefore be understood as something like:

```text
universe / namespace_version / family_id @ anchor_id
```

while the reader-facing notation remains:

```text
revenue @ {store, month}
```

The full signature and lineage remain governed underneath the handle and can be exposed when explanation, conformance checking, or certification requires them.

A version label by itself leaves family identity unchanged. If a new publication version changes only documentation, implementation, or other identity-neutral material, the family ID may remain stable. If it changes an identity-bearing semantic field, the semantic signature changes and the new publication must resolve to a distinct family identity.

This gives a direct analytical reading to governed query notation such as Frame-QL anchor ascription (Wang 2026f). The syntax is an implementation surface whose meaning is grounded by resolution through a governed namespace to one family ID.

# 4. Operators and Sufficient State

Analytical work transforms measures.

ToD keeps the primary value-operator calculus small: **mapper** and **reducer**.

Other operations may establish structural context while remaining structural operations outside the primary value-operator vocabulary.

## 4.1 Mapper

A **mapper** is an anchor-preserving value transformation.

For one input:

$$
F@A\xrightarrow{f}G@A.
$$

Anchor preservation is definitional.

A mapper may be point-local:

$$
g(a)=f(m(a)),
$$

or contextual:

$$
g(a)=f\big(m|_{C(a)}\big),
$$

where $C(a)$ is a governed context associated with focal point $a$.

This is broad enough to cover ordinary arithmetic and, when governed context is supplied, analytical patterns such as share, rank, cumulative calculations, and rolling calculations.

Ordered and neighborhood semantics belong to operator contracts, preserving the small top-level value-operator vocabulary.

### Proposition 2 - Mapper geometry

If $f$ is a mapper with input measure at anchor $A$, its output measure is also at $A$.

## 4.2 Reducer

A **reducer** contracts a measure from a strictly finer anchor to a coarser anchor.

Let:

$$
B\succ A.
$$

Then a reduction-shaped computation may be written:

$$
F@B\xrightarrow{\rho}G@A.
$$

When $F=G$, the edge is a **family-preserving reduction**. When the reduction-shaped construction establishes $G
eq F$, the reduction participates in a **family-establishing graft**. The reducer geometry concerns the anchor contraction; family identity determines which of these two analytical roles the edge has.

The computation is reducer-shaped when $
ho$ evaluates the governed $B$-points contained in each $A$-point.

For $a\in A$, define its finer fiber:

$$
B(a)=\{b\in B:b\subseteq a\}.
$$

A reducer consumes governed state from $B(a)$ to establish the target value at $a$.

### Proposition 3 - Reducer geometry

A reducer requires:

$$
B\succ A
$$

within the same universe.

Anchor-changing operations include reduction, broadcast, expansion, allocation, relationship traversal, and universe transfer, each with distinct structural meaning.

## 4.3 Source and target anchors

Reduction is intrinsically two-anchor:

$$
F@B\xrightarrow{\rho}G@A.
$$

The source $B$-anchor says what finer analytical units the reducer consumes. The target $A$-anchor says where the resulting measure exists.

The source anchor can change the identity of the quantity being formed.

For example, an average over orders and an average over customers can both be reported at `{region, quarter}` while denoting different quantities because the units being averaged differ.

The important point is level of attachment:

> **The source anchor belongs to the derivation. When it establishes a new measure-family identity, the distinction survives in that family identity. Each resulting measure still has one current anchor.**

This formulation refines the earlier two-anchor account by retaining the source-anchor insight at the derivation and family-identity levels while each resulting measure keeps one current anchor (Wang 2026b).

## 4.4 Displayed value is not sufficient state

A reducer may require more information than the displayed value of an intermediate measure.

This is why mechanically valid arithmetic on stored outputs can still violate analytical identity.

A daily average of `10` leaves the count unknown. An exact distinct count of `100` leaves the identity set unknown. A closing value leaves the selecting order law unknown.

ToD therefore separates displayed value from the state required for lawful continuation.

## 4.5 Sufficient state

A compositional reducer can be described by:

$$
(S,\eta,\oplus,e,\phi),
$$

where:

- $S$ is sufficient state;
- $\eta$ initializes or embeds source contribution into state;
- $\oplus$ combines state;
- $e$ is the identity state;
- $\phi$ finalizes state into the displayed value.

### SUM

For ordinary additive Revenue:

$$
S=\mathbb{R},
\qquad
\eta(x)=x,
\qquad
\oplus=+,
\qquad
e=0,
\qquad
\phi(s)=s.
$$

The displayed value is itself sufficient state.

### Average

For an exact arithmetic mean:

$$
S=\mathbb{R}\times\mathbb{N},
$$

with state:

$$
(s,n),
$$

combination:

$$
(s_1,n_1)\oplus(s_2,n_2)
=
(s_1+s_2,n_1+n_2),
$$

and finalization:

$$
\phi(s,n)=\frac{s}{n}.
$$

A finalized average alone generally lacks the sufficient state required for exact further averaging.

### Exact distinct count

For exact distinct count, one sufficient state is the set of governed identities:

$$
S=\mathcal P(I),
$$

with:

$$
S_1\oplus S_2=S_1\cup S_2
$$

and:

$$
\phi(S)=|S|.
$$

The scalar cardinality alone lacks the state required for exact arbitrary continuation.

## 4.6 Three things that must remain distinct

The foundation therefore requires:

$$
\boxed{
\text{displayed value}
\neq
\text{sufficient state}
\neq
\text{analytical identity}
}
$$

A displayed value answers what is shown.

Sufficient state answers what information must survive for lawful continuation.

Analytical identity answers what governed quantity the state and value represent.

Conflating these three is a recurring source of silent analytical error.

## 4.7 State-law taxonomy

The commutative-monoid case is central because it supports arbitrary regrouping and ordering independence. It is one region of a broader state-law taxonomy.

| Declared state law | Governed staging property |
|---|---|
| **Commutative monoid** | regrouping and ordering of the same governed contributions preserve state |
| **Associative, noncommutative** | regrouping is safe while logical order must be preserved |
| **Ordered/stateful composition** | continuation requires an explicit sequence, order key, context, or composition contract |
| **No declared compositional state** | arbitrary staged reduction is unavailable from summarized state; retained roots or richer state are required |

The row is determined by the **declared state law**; operator names alone are insufficient.

`FIRST` or `LAST`, for example, can be compositional when state retains an order key, value, and deterministic tie-breaking rule. A sketch can have a commutative merge law while remaining approximate. Approximation is therefore orthogonal to this table: it belongs to the certificate and materialization contract unless the semantic target itself changes.

The governing question is:

> **What staging transformations does the declared state law certify?**

# 5. Measure Families and Analytical Coherence

A single measure $F@A$ tells us one quantity at one analytical location. Its family law separately governs behavior across anchors.

The measure family supplies that coherent trans-anchor structure.

## 5.1 The family as a coherent region

A measure family $F$ consists of the governed measures:

$$
F@A_1,
F@A_2,
\ldots
$$

that share one family identity and are connected by one coherent family-preserving reducer law.

The family may be visualized as a cloud over partition geometry. Different points inside the cloud are the family's measures at different anchors.

If two analytical directions require genuinely different coherent reducer laws, ToD assigns them distinct family identities even when everyday language reuses one label. The distinct coherent regions are connected through lineage. Ordinary language may call both quantities “inventory,” for example; governed canonical names distinguish them when their analytical identities differ.

For Revenue, for example:

```text
               revenue @ day
                  /       \
                 v         v
       revenue @ week   revenue @ month
```

The cloud can branch because anchors can be incomparable.

Every family has:

1. one ex-ante semantic identity signature and immutable family ID;
2. one unique governed canonical name within each active namespace version;
3. a **designated governed family root**;
4. one declared family law governing its admitted family-preserving continuation;
5. identity-bearing contracts and constitutive ancestry.

The phrase **full reducer law** is important. Two operations both called `SUM` do not necessarily belong to the same family law if their participation, multiplicity, support, regime, approximation, or other contribution semantics differ.

## 5.2 Designated family root

Every family declaration designates one governed family root:

$$
F@R_F.
$$

The designation is constitutive. Its uniqueness comes from the family declaration and identity signature, independently of whether the partition partial order supplies a unique greatest refinement.

The designated root must stand at an anchor from which the family law establishes the family-preserving measures admitted by that declaration, or at which the family's declared synthesis law begins when its continuation is intentionally more restricted.

For a primitive additive Revenue family, the designated family root may coincide with the universe root anchor.

For a derived family such as MaxRevenue, the designated root may begin at the anchor where that new quantity is established.

The universe root and family root therefore answer different questions:

- universe root: where does governed point geometry begin?
- family root: where does this governed family declaration begin?

## 5.3 Coherent state law

For the central coherence result, the family law lies in the commutative-monoid fragment of the state-law taxonomy:

$$
(S,\oplus,e).
$$

Thus:

### Associativity

$$
(x\oplus y)\oplus z
=
x\oplus(y\oplus z).
$$

### Identity

$$
x\oplus e=e\oplus x=x.
$$

### Commutativity

$$
x\oplus y=y\oplus x.
$$

These laws mean that lawful grouping and staging preserve the result when they combine the same governed contribution states.

## 5.4 Family coherence theorem

Suppose:

$$
B\succ C\succ A
$$

and all reductions remain in one family $F$. For target point $a\in A$, direct reduction gives:

$$
S_A(a)
=
\bigoplus_{b\subseteq a}S_B(b).
$$

The staged path gives:

$$
S_A'(a)
=
\bigoplus_{c\subseteq a}
\left(
\bigoplus_{b\subseteq c}S_B(b)
\right).
$$

When the family-preserving edge contracts are satisfied, both paths range over the same governed contributions. Because the $C$-points partition the relevant $B$-points inside $a$, associativity and commutativity give:

$$
S_A'(a)
=
S_A(a).
$$

### Theorem 1 - Family path independence

If $d_1$ and $d_2$ are licensed family-preserving paths from $F@B$ to $F@A$, then for every $a\in A$:

$$
\boxed{
S_A^{(d_1)}(a)
=
S_A^{(d_2)}(a).
}
$$

Finalization therefore yields the same displayed value.

The algebra is the standard monoidal fold result. ToD attaches that algebra to a declared family identity and to edge contracts that determine when staging equivalence is analytically licensed. This turns a familiar algebraic fact into a governance rule for analytical identity.

## 5.5 Why the family matters

The measure family is the unit of **analytical coherence**. When Revenue reduced transaction->day->month and Revenue reduced transaction->month satisfy the same family law and edge contracts, the family coherence theorem establishes one target measure and permits internal staging to disappear from canonical identity.

The family therefore supplies local algebraic coherence. The lineage graph in Section 6 supplies the larger structure of analytical ancestry and family identity.

## 5.6 Same family does not imply mutual derivability

Family membership permits directed reachability only where partition geometry and family law provide a path.

If:

$$
day\succ week
$$

and:

$$
day\succ month
$$

while week and month are incomparable, then both:

$$
revenue@week
$$

and:

$$
revenue@month
$$

belong to family `revenue`.

Neither follows from the other by family reduction:

$$
revenue@week\not\rightsquigarrow_F revenue@month
$$

and:

$$
revenue@month\not\rightsquigarrow_F revenue@week.
$$

### Proposition 4 - Family membership does not imply mutual reachability

Measures may share one family identity while occupying incomparable anchors.

The family provides coherent identity and path equivalence along lawful directed paths, while partition geometry continues to govern reachability.

## 5.7 Materialized family state

Theoretical family derivability assumes that the state required by the family law is available.

A stored daily mean may carry only the displayed scalar and omit `(sum,count)`. The mean family may still have a lawful daily->monthly reduction in the analytical model, while that materialization lacks the state required to perform it exactly.

This distinction becomes important later:

$$
\text{analytically derivable}
\not\Rightarrow
\text{derivable from every materialization}.
$$

# 6. Lineage: The Universe-Level Family DAG

Measure families are coherent regions. A universe normally contains many such regions, and analytical work can establish new families from existing ones.

The **lineage graph** governs those relationships.

A useful visual picture is a sky containing **measure-family clouds**. A *family cloud* is only a visual metaphor for the set and geometry of anchored measures belonging to one measure family; it introduces no additional formal object. Each cloud has its own shape because it spans the anchors at which its measures lawfully exist. Directed connections between clouds record how new analytical identities are established from earlier ones.

For a well-formed governed universe, the constitutive lineage of measure families is a directed acyclic graph.

## 6.1 Family-level lineage graph

Let:

$$
G_U=(\mathcal F_U,E_U)
$$

be the governed lineage graph of universe $U$.

The nodes $\mathcal F_U$ are the uniquely identified, uniquely named measure families governed in $U$.

The lineage graph may carry an implementation or publication name; user-facing canonical naming is required only where the surrounding governance system needs it. In the common case, the universe already determines the relevant lineage graph.

A directed edge:

$$
F_i\rightarrow F_j
$$

means that the root of family $F_j$ is established through a governed family-changing derivation whose analytical ancestry includes family $F_i$.

Inside each node lies the family's own anchor geometry and family-preserving reduction structure. The family-level lineage graph can omit those internal paths because family identity already contains them.

Conceptually:

```text
        .-----------------.
       /      revenue      \
      |  txn -> day        |
      |       /   \        |
      |    week   month     |
       \                 /
        '-------+---------'
                |
                v
        .-----------------.
       / max_monthly_rev   \
      | month -> customer  |
       \                   /
        '-----------------'
```

The cloud is the family. The arrow is family-establishing lineage.

## 6.2 Well-formedness of constitutive lineage

The lineage graph records **constitutive analytical ancestry**; executable conversions outside that ancestry remain operational relationships.

If:

$$
F_i\rightarrow F_j,
$$

then $F_j$'s identity depends on already governed parent family $F_i$.

A cycle such as:

$$
F_1\rightarrow F_2\rightarrow F_3\rightarrow F_1
$$

would make the family identities circular. ToD makes **well-founded constitutive ancestry** a condition of a well-formed governed lineage graph.

### Well-formedness condition - Lineage well-foundedness

The constitutive family-lineage relation must be acyclic and well-founded. Every family's ancestry terminates in the primitive core of the universe.

Executable transformations can be reversible operationally. Constitutive family ancestry remains well-founded and acyclic.

## 6.3 Rooted analytical standing

Some family identities begin directly in the primitive core of the universe. These are the roots of the family-level lineage DAG.

For a governed family $F$, write:

$$
U\rightsquigarrow_L F
$$

when $F$ has governed ancestry rooted in the universe.

Then a measure $F@A$ has analytical standing when its family has standing and the family law establishes that the family exists at anchor $A$.

### Well-formedness condition - Rooted standing

Every governed family in universe $U$ must have well-founded constitutive lineage rooted in the primitive core of $U$:

$$
F\text{ governed in }U
\Rightarrow
U\rightsquigarrow_L F.
$$

This is a well-formedness condition for governed families. It ensures that every governed measure has analytical ancestry instead of appearing as an unexplained named number.

## 6.4 Graft: establishing a new family

A **graft** marks the establishment of a new measure-family root from an existing governed measure.

Suppose Revenue exists at anchor $B$:

$$
revenue@B.
$$

A MAX-based construction can establish a new family at that same anchor:

$$
revenue@B
\xRightarrow{\gamma_{MAX}}
max\_revenue_B@B.
$$

The precise canonical family name is a governance choice and must uniquely denote the new family identity within the namespace version.

At the graft point the displayed values may be equal, since MAX over a singleton returns the singleton value. Yet the families are different because their future lawful reductions use different state laws.

A graft is an **identity event** in lineage: the point where a governed derivation leaves family-preserving continuation and establishes a new family.

The present foundation develops the single-source case and one explicit multi-parent example. A general algebra of multi-input family synthesis remains outside the current scope.


### Multi-parent synthesis: Average Order Value

Version 6.1 makes one multi-parent case explicit.

Suppose an order universe contains two governed parent families:

$$
revenue@A
$$

and:

$$
orderCount@A.
$$

Define Average Order Value at any admitted anchor $A$ by:

$$
aov@A
=
\frac{revenue@A}{orderCount@A}.
$$

The family-level ancestry is multi-parent:

```text
revenue -------\
                >---- average_order_value
orderCount ----/
```

A conforming `average_order_value` family declaration records both parent family IDs and the synthesis law in its semantic signature.

The scalar AOV display is generally insufficient for arbitrary exact continuation. Suppose two child points have:

$$
(revenue,orderCount)=(100,1)
$$

and:

$$
(revenue,orderCount)=(300,2).
$$

Their displayed AOV values are $100$ and $150$. Averaging those displays gives $125$, while exact recombination gives:

$$
\frac{100+300}{1+2}
=
\frac{400}{3}.
$$

A family can therefore declare one of two continuation structures:

1. **re-derive at each anchor** from the two parent measures, admitting no scalar AOV coarsening edge; or
2. retain a governed composite sufficient state such as `(revenue_state, order_count_state)` and admit a family-preserving reducer for that composite state.

These are different declared family laws even when some current displays happen to agree. Materializations can also differ in which continuation capability they retain.

The example establishes the general lineage point required here: a family may have several parent identities, and the parent IDs plus synthesis law are constitutive of the child identity.

## 6.5 The graft anchor is identity-bearing

The anchor at which a new family begins can change the quantity.

Suppose one store has product-level daily Revenue:

| Day | Product revenues |
|---|---:|
| d1 | 6, 4 |
| d2 | 7, 0 |

If the MAX family is established at:

$$
\{store,day,product\},
$$

then the store-level maximum is:

$$
\max(6,4,7,0)=7.
$$

If Revenue is first reduced by SUM to:

$$
\{store,day\},
$$

we obtain:

$$
10,7.
$$

Establishing MAX only there produces:

$$
\max(10,7)=10.
$$

The two constructions therefore establish different family identities.

They require distinct canonical governed family names within the same namespace version.

The graft anchor is identity-bearing and remains part of family ancestry, while each resulting measure still has one current anchor. Each resulting measure still has one current anchor. The source/graft anchor survives recursively inside the identity of the family that was established there.

### Proposition 5 - Graft identity

The governed rule and anchor at which a new family root is established are part of that family's analytical identity.

## 6.6 Detailed lineage and family compression

A system may retain detailed direct derivation paths for explanation, execution, provenance, contract checking, or materialization planning.

For example:

$$
revenue@transaction
\rightarrow
revenue@day
\rightarrow
revenue@month
\xRightarrow{\gamma}
max\_monthly\_revenue@month
\rightarrow
max\_monthly\_revenue@year.
$$

The first three measures lie inside the same `revenue` family cloud. By the family coherence theorem, the intermediate day staging preserves the Revenue identity.

The last two measures lie inside the new MAX-family cloud.

At family level, the detailed path compresses to:

$$
revenue
\rightarrow
max\_monthly\_revenue.
$$

### Proposition 6 - Family compression

A maximal coherent family-preserving subpath may be replaced in canonical lineage by the identity of that measure family.

The compression is justified by proof. Internal edges disappear from canonical identity only where family coherence establishes that their staging is analytically irrelevant.

## 6.7 Semantic identity signature, family ID, and canonical name

Family identity is established **before** values are compared.

Let:

$$
\Sigma(F)
=
\operatorname{canon}\!\left(
U_F,\,
R_F,\,
Parents(F),\,
Establish(F),\,
Law(F),\,
Contracts_{id}(F)
\right).
$$

Here $U_F$ is the governed universe, $R_F$ the designated family root, $Parents(F)$ the immutable parent family IDs, $Establish(F)$ the family-establishing construction, and $Law(F)$ the declared continuation law.

By definition:

$$
Contracts_{id}(F)
=
\{\text{fields classified as **Family identity** below}\}.
$$

A field belongs there exactly when changing it changes the denoted quantity, its participation/contribution semantics, or its declared family law.

A conforming implementation may derive an immutable ID:

$$
id(F)=H(\Sigma(F)),
$$

or assign another immutable identifier tied to the signed declaration. The signature is the theoretical object; the hash mechanism is implementation-specific.

Output agreement carries no power to create identity, and disagreement carries no power to split it retroactively.

### Classifying governed information

| Location | Criterion | Typical examples |
|---|---|---|
| **Family identity** | changes the denoted analytical quantity, participation/contribution semantics, or declared family law | population/participation, unit/currency, tax inclusion, deduplication/multiplicity, identity-bearing fill/null rule, meaning-bearing regime, constitutive parents, graft anchor |
| **Edge validity** | determines whether one derivation faithfully realizes an already-declared identity | cardinality proof, overlap check, support predicates, order contract, allocation weights |
| **Certificate / materialization** | changes exactness, approximation grade, retained capability, evidential status, or realization quality while the semantic target stays fixed | error bounds, retained state, evidence grade, materialization fidelity |
| **Metadata** | changes none of identity, edge validity, or certified realization | descriptions, owners, UI labels, commentary |

The classification uses the declared semantic target. A semantic-model version reference is lineage/publication metadata unless a meaning-bearing field inside that version changes and is classified accordingly.

### Canonical name and family succession

Governance assigns one canonical name within an active namespace version:

$$
name_U(F)\longrightarrow id(F).
$$

### Proposition 7 - Unique family naming

Within one namespace version:

$$
name_U(F_1)=name_U(F_2)
\Rightarrow
id(F_1)=id(F_2).
$$

The semantic signature constitutes identity; the name resolves it.

Because $Law(F)$ and $Contracts_{id}(F)$ lie inside $\Sigma(F)$, changing an identity-bearing continuation law establishes a **family succession**.

For example, an `average_order_value` family that re-derives from its parents at every anchor and a successor family that admits composite-state coarsening have distinct signatures and IDs:

$$
\Sigma(F_{old})\neq\Sigma(F_{new})
\quad\Rightarrow\quad
id(F_{old})\neq id(F_{new}).
$$

A later namespace version may resolve the same canonical human-readable name to the successor ID while prior namespace versions continue to resolve the earlier ID. Semantic capability can therefore evolve through explicit succession while prior analytical identities remain historically stable.

## 6.8 Measure identity

A measure identity is compact:

$$
\boxed{F@A}
$$

or, using the canonical family name:

$$
\boxed{name(F)@A.}
$$

Thus:

$$
\boxed{revenue@\{store,month\}}
$$

is a complete ordinary reference to the Revenue family at the store-month anchor.

Expanded ancestry remains available when explanation requires it. A single-parent chain may be shown as:

$$
[F_0,F_1,\ldots,F_n]@A
\quad\leadsto\quad
F_n@A.
$$

Multi-parent ancestry is a rooted DAG. Once the target family identity has been established, ordinary analytical reference remains:

$$
F@A.
$$

## 6.9 The critical consistency rule

Consistency is evaluated **after** identity has been established.

This direction is essential:

$$
\boxed{
\text{identity is an input to the consistency test;}
\quad
\text{consistency never creates identity from output comparison.}
}
$$

Let $C(d)$ denote the canonical measure identity claimed by derivation $d$, resolved from the ex-ante family ID and target anchor.

Let:

$$
K(d)
$$

denote the governed sufficient state produced by the derivation.

For family $F$, write:

$$
K_1\equiv_F K_2
$$

when the two states are equivalent under the equality relation declared by the family law.

A conforming family-state equivalence must satisfy two well-formedness conditions.

First, it is a **congruence** for the family's combine law. Whenever the relevant combinations are admitted,

$$
K_1\equiv_F K_1'
\quad\text{and}\quad
K_2\equiv_F K_2'
$$

imply:

$$
K_1\oplus_F K_2
\equiv_F
K_1'\oplus_F K_2'.
$$

Second, it must refine display equality:

$$
\boxed{
K_1\equiv_F K_2
\Rightarrow
\phi_F(K_1)=\phi_F(K_2).
}
$$

In the ordinary exact monoid case, $\equiv_F$ may be literal state equality. Alternative representations may declare another canonical semantic equivalence only when these well-formedness conditions hold.

Suppose:

$$
C(d_1)=C(d_2)=F@A.
$$

Then both derivations have independently committed themselves to one analytical identity. When the contracts licensing both derivations are satisfied, consistency requires:

$$
\boxed{
K(d_1)\equiv_F K(d_2).
}
$$

Finalization then requires equal displayed values:

$$
\phi_F(K(d_1))
=
\phi_F(K(d_2)).
$$

A disagreement therefore indicates a failed premise, implementation, edge contract, evidence/materialization condition, or conformance claim. Family identity remains fixed by the ex-ante signature.

If:

$$
C(d_1)\neq C(d_2),
$$

the derivations claim different analytical measures. Equality is outside the consistency obligation even when current displayed values happen to coincide.

### Proposition 8 - Identity-relative consistency

Under satisfied contracts:

$$
\boxed{
C(d_1)=C(d_2)=F@A
\Rightarrow
K(d_1)\equiv_F K(d_2).
}
$$

Conversely, different canonical identities establish different analytical objects, so ToD imposes no equality obligation across them.

This is the falsifiable direction of the theory: **same declared identity implies governed agreement**. The theory never infers identity merely because two outputs agree.

## 6.10 Lineage is fully inside analytical governance

The family-level DAG is the universe-wide structure of analytical ancestry. Measure families provide local algebraic coherence; lineage records which family identities exist, where they were established, and how identity-bearing derivations connect them.

Physical dependency alone is insufficient. Analytical lineage must carry enough information to resolve families, anchors, family transitions, state laws, and contracts.

$$
\boxed{
\text{family}
\rightarrow
\text{local coherence}
\qquad
\text{lineage}
\rightarrow
\text{governed ancestry and identity}
}
$$

## 6.11 One governed construction, end to end

A compact example shows how the pieces fit together.

Consider a transaction universe whose governed root points are sale lines. Let `transaction`, `day`, `month`, and `store` induce governed partitions, with transaction finer than day and month in the relevant time geometry. Suppose `revenue` is a primitive measure family whose root measure is available at the transaction anchor and whose family law is additive:

$$
(\mathbb{R},+,0).
$$

The ordinary measures:

$$
revenue@transaction,\qquad revenue@day,\qquad revenue@month
$$

all belong to the uniquely named `revenue` family. A direct reduction from transaction to month and a staged reduction through day combine the same contribution states. By Theorem 1 they are equivalent:

$$
revenue@transaction\to revenue@day\to revenue@month
\equiv
revenue@transaction\to revenue@month.
$$

The intermediate day staging can therefore disappear from canonical analytical identity. Both derivations resolve to the same measure:

$$
\boxed{revenue@month}.
$$

Now suppose the analytical question changes to the maximum daily Revenue in each month. First form the daily Revenue measure, then establish a new family by MAX at the day anchor:

$$
revenue@day
\rightsquigarrow
maxDailyRevenue@day.
$$

The family name `maxDailyRevenue` denotes a different governed family identity whose graft ancestry records that MAX began over daily Revenue. It can then reduce coherently by MAX to month:

$$
maxDailyRevenue@day
\xrightarrow{MAX}
maxDailyRevenue@month.
$$

At family level the lineage is simply:

```text
revenue  ---->  maxDailyRevenue
```

while each family contains its own cloud of anchored measures. The first cloud is additive; the second is MAX-coherent. Their different laws establish different uniquely named analytical identities.

Finally suppose someone expands sale-line Revenue through a many-to-many product-tag relation and then attempts to SUM the replicated values as though they were still `revenue`. If one line of Revenue 100 appears under three tags, the expansion may present three physical values of 100. The proposed continuation violates the multiplicity contract of the Revenue lineage edge, leaving the resulting 300 uncertified as `revenue@tag`. A governed assignment, allocation, membership semantics, or another explicitly established family would be required.

This one construction illustrates the full pattern:

```text
universe and partitions
        |
        v
revenue family -- coherent internal reduction
        |
        +---- family-establishing graft ----> maxDailyRevenue family
        |
        +---- invalid fan-out continuation -> not certified as revenue
```

The theory can make these judgments from governed geometry, family laws, lineage, and contracts; a physical table plan is secondary.

# 7. Analytical Governance and Its Boundaries

Analytical governance covers the full lineage DAG. Inside a coherent family, algebra establishes path equivalence. Across family boundaries, lineage records identity-changing derivations. When two derivations claim one identity, consistency becomes a governance obligation.

## 7.1 Five core governance questions

### 1. Does the family have analytical standing?

$$
U\rightsquigarrow_L F\ ?
$$

Is the family rooted through governed ancestry in the universe?

### 2. What measure is being requested?

$$
F@A
$$

Which uniquely named family and which anchor identify the analytical object?

### 3. Can it be derived from what is available?

Does governed lineage and partition geometry provide a lawful path from the available analytical objects to the requested measure?

### 4. Do alternative derivations claim the same identity?

Canonicalize the derivations.

If their resulting family identities differ, they are different measures.

If they claim the same $F@A$, the system must verify the laws and contracts that make the results consistent.

### 5. Is the required state materially available?

A lawful analytical path may exist even when a stored representation has discarded sufficient state needed to execute it.

These five questions separate identity, derivability, consistency, and execution capability while keeping the full lineage graph inside governance.

## 7.2 Contracts make lineage edges governable

Support, multiplicity, and order remain explicit edge-validity conditions within the theory.

For a direct governed derivation edge:

$$
e:M_B\longrightarrow N_A,
$$

let:

$$
\Gamma(e)
$$

denote its **governance contract**: the predicates and declarations that must hold for the edge to be admitted as the claimed analytical derivation. Depending on the edge, $\Gamma(e)$ may include:

- eligibility and support;
- participation;
- contribution multiplicity;
- logical order;
- regime;
- approximation status;
- structural relationship properties;
- universe membership or transfer conditions.

Thus a lineage edge should be read conceptually as:

$$
M_B
\xrightarrow[\Gamma(e)]{op}
N_A.
$$

The edge belongs to governed lineage only to the extent that its contract is established. A missing or contradicted required contract leaves the derivation unlicensed under the claimed identity.

For a family-preserving reduction, $\Gamma(e)$ must also preserve the contribution semantics assumed by the family's sufficient-state law. The shared operator label `SUM` alone is insufficient. An uncontrolled fan-out can violate multiplicity even while the arithmetic operator remains addition.

Family coherence is therefore conditional in the appropriate way:

$$
\text{same coherent family law}
+
\text{satisfied edge contracts}
\Rightarrow
\text{path equivalence}.
$$


Version 6.1 locates these declarations explicitly: identity-bearing contracts belong in $\Sigma(F)$; edge-validity predicates in $\Gamma(e)$; approximation, retained capability, and realization quality in the certificate/materialization layer when the semantic target is unchanged; descriptive metadata remains separate.

This keeps edge contracts focused and preserves universe, anchor, measure family, and lineage as the primary structural objects. The view is consistent with the project's earlier contract-calculus work on governed analytical transformation (Wang 2026c).

## 7.3 Support, absence, and zero

For measure $F@A$:

$$
S_{F,A}\subseteq E_{F,A}\subseteq A.
$$

This distinguishes:

```text
point absent from the universe
point exists; measure ineligible
point eligible; unsupported / unobserved
point supported with value zero
```

A fill rule such as `missing -> 0` can therefore be analytically significant. If later operations consume the filled values, the fill is part of derivation rather than mere presentation.

## 7.4 Multiplicity and fan-out

A structurally valid relationship can alter analytical contribution multiplicity.

If one order with Revenue 100 is expanded across three tags, the physical rows may become:

```text
100
100
100
```

The relation may be valid while the original Revenue family law still leaves a SUM of 300 uncertified as Revenue.

The function name `SUM` alone is insufficient to establish family coherence. Contribution semantics must remain governed.

This is one reason ordinary schema lineage is insufficient as analytical lineage.

## 7.5 Order and sequence contracts

Some state laws require a governed logical order.

Examples include:

- FIRST and LAST;
- cumulative calculations;
- rolling calculations;
- lag and lead;
- noncommutative state composition.

Order is an analytical declaration, never physical row order.

The state-law taxonomy of Section 4.7 determines what staging is safe. An associative noncommutative law permits regrouping while preserving sequence. Ordered/stateful composition may require an explicit order key, context, or sequence contract. Some FIRST/LAST constructions can become compositional when sufficient state retains the relevant order key, value, and deterministic tie-breaking rule.

The governing principle is:

> **When result semantics depend on sequence, the sequence law belongs in the declared family or edge semantics that make the result meaningful.**

## 7.6 Regime and approximation

Regime and approximation occupy different governance locations.

A **regime** can be identity-bearing when changing the value-generation arrangement changes the analytical quantity that may be substituted under one family identity. Actual, forecast, simulated, restated, and intervention-qualified quantities therefore require an explicit classification by the family declaration. Regime is developed more fully as a neighboring structural contract in Wang (2026d).

**Approximation** is normally a certificate/materialization property when the approximate procedure targets the same governed analytical quantity.

An exact distinct count and an approximate sketch can therefore claim the same analytical target while carrying different realization certificates, error contracts, and materialized capabilities. *Certifiable State Under Information Loss* develops this separation between claim content, retained state, and certificate grade (Wang 2026g).

Approximation enters family identity only when the declaration changes the semantic target or family law itself.

The rule is:

> **Semantic target determines identity; realization quality determines the certificate unless the target itself changes.**

## 7.7 Structural operations are not reducers

Structural changes include value reduction as one case among several.

Examples include:

- restriction;
- assignment;
- relationship traversal;
- expansion;
- allocation;
- alignment;
- universe transfer;
- neighborhood construction.

These operations can establish the context in which mapper or reducer laws act.

The foundation preserves a small value-operator core by keeping such structural work conceptually separate.

## 7.8 Analytical derivation versus output selection

A useful boundary arises between operations that change an analytical object and operations that merely choose which already-formed results are shown.

A restriction that changes which contributions participate in forming Revenue may belong in analytical lineage.

After `revenue@store` has already been formed, selecting stores with Revenue above a threshold can remain a frame-selection operation over the existing family.

Likewise, sorting or taking the top ten returned store measures can remain a presentation or frame-selection operation over already-formed measures.

The theoretical boundary is:

> **If an operation changes what the measure is, it belongs in analytical lineage. Selection and presentation over already-formed measures preserve their analytical identity.**

Query languages may expose this boundary through different clauses. The distinction is prior to any particular syntax.

## 7.9 Universe boundaries

Refinement is defined among partitions of one root-point domain.

If universes $U$ and $V$ have root domains:

$$
\Omega_U
$$

and:

$$
\Omega_V,
$$

then identically spelled anchor expressions can still refer to different analytical points.

`{store, month}` in a transaction universe and `{store, month}` in an inventory-state universe partition different governed root-point populations.

Cross-universe analysis therefore requires an explicit governed relation, reconciliation, or transfer law. At minimum, such a law must identify the source and target universes, state how analytical points correspond or are constructed across the boundary, and specify which measure identity and contribution contracts survive the transfer. For example, moving customer-attributed Revenue from a transaction universe into a customer-registry universe must declare the matching relation, treatment of unmatched points, and contribution multiplicity. The foundation requires cross-universe movement to be explicit and leaves the specific transfer calculus to the governed application.

## 7.10 Materialization

A **measure** is analytical. A **materialization** is a stored representation of analytical state.

A materialization may retain:

- displayed value;
- sufficient state;
- family identity;
- anchor;
- support;
- regime;
- approximation state;
- lineage references.

These capabilities are governed independently and may diverge.

For example, the average family may lawfully reduce daily state to monthly state when `(sum,count)` is available. A daily materialization that stores only the finalized mean lacks the state required for that exact continuation.

### Proposition 9 - Materialized derivability

Analytical derivability can exceed the capability of a particular materialization.

A requested derivation is materially executable only if the available representation retains the required state and contracts.

## 7.11 Observation and provenance

Observation answers how evidence for a measure became available.

Provenance records where a representation or value came from.

Both remain distinct from analytical identity.

Two materializations from different physical sources can represent the same governed measure. Two columns from one table can represent different measures.

Thus:

$$
\boxed{
\text{Observation}
\neq
\text{Provenance}
\neq
\text{Analytical Identity}
}
$$

Constructive analytical identity requires a governed account of the quantity and its standing in the universe; physical reconstruction from finer data is optional. It requires a governed account of what quantity the observation is evidence for and how that quantity stands in the universe.

## 7.12 The Statistical Bridge

Analytical validity and statistical validity are different questions.

ToD asks:

- what analytical object exists?
- at what anchor?
- under what family identity?
- through what lineage?
- is the derivation lawful?
- where is consistency established?

Statistical reasoning asks what evidence permits us to infer about a population, process, parameter, intervention, or future outcome.

That may require assumptions about:

- sampling;
- measurement;
- uncertainty;
- causal identification;
- model specification;
- external validity.

Therefore:

$$
\boxed{
\text{Analytical Validity}
\neq
\text{Statistical Validity}
}
$$

A perfectly governed analytical measure can support an unjustified inference. A sophisticated statistical model can begin from an analytically malformed quantity.

The Statistical Bridge connects these layers while preserving their distinct jurisdictions (Wang 2026e).

## 7.13 What ToD can certify

Given adequate declarations and evidence for its premises, ToD can certify structural conclusions such as:

- a family has governed standing in universe $U$;
- a canonical family name resolves to one immutable family identity;
- a requested $F@A$ is lawfully derivable under satisfied family and edge contracts;
- alternative derivations claiming the same identity are required to agree under the family-state equivalence relation;
- a materialization has, or lacks, the state required to execute an analytically lawful continuation.

The surrounding governance system owns the lifecycle by which premises become verified, provisional, contradicted, or revised. A conforming implementation can surface supplied evidence statuses and their provenance as annotations or certificate fields alongside ToD's structural conclusions; ToD preserves and exposes those statuses while the surrounding governance system interprets, challenges, or promotes them.

Formal coherence certifies analytical structure. Empirical truth requires evidential warrant.

> **Given governed premises, ToD can determine what analytical object is being claimed, whether it has standing, how it may be derived, and when alternative derivations are required to agree.**

A conforming system can also test whether the declarations needed for those claims are structurally present. Appendix A defines the minimum surface for that check. Institutional governance separately selects which conforming publication is authoritative.

## 7.14 Refusal is part of governance

A theory of analytical governance must permit the answer:

> **not established**

or:

> **under-specified**.

If a category relation does not induce a partition, `revenue@category` may be undefined until assignment or allocation law is supplied.

An average with unspecified averaging units is under-specified.

If a requested exact continuation lacks sufficient state, the computation is unavailable from that materialization.

If two constructions have different canonical family identities, governance assigns distinct canonical names within one namespace version.

Refusal and clarification are valid outcomes of taking analytical identity seriously.

# 8. Conclusion

The Theory of Data begins with a simple observation:

> **Data is always something about something else.**

A datum is a governed typed value at an analytical point. To understand that point, the Theory introduces a universe and partition geometry. The universe establishes governed root-point existence under an explicit existence law. Anchors partition those points. Dimensions name conventional partitions. Refinement gives direction to analytical reduction, while incomparability prevents false movement between unrelated groupings.

From this geometry, v6 builds a compact analytical ontology.

A **measure family** is a uniquely identified and uniquely named coherent analytical family.

A **measure** is that family at an anchor:

$$
\boxed{F@A.}
$$

A mapper preserves anchor. A reducer contracts a strictly finer anchor to a coarser anchor. Reducer coherence depends on sufficient state; displayed values alone may be insufficient.

Inside one family, a commutative-monoid state law makes lawful staged reductions path-independent. This is the algebraic basis for family coherence and for removing analytically irrelevant staging from identity.

Analytical governance extends beyond family coherence into lineage, contracts, and materialized capability.

At the universe level, well-formed constitutive ancestry organizes uniquely named measure families as a directed acyclic lineage graph. The graph records constitutive analytical ancestry. Family-establishing derivations create new identities. Within the family-cloud metaphor, each cloud contains the family's internally coherent anchored measures; directed links between clouds govern where new analytical identities come from.

This changes how apparent inconsistency should be understood.

If two derivations canonicalize to different family identities, they are different measures and require distinct canonical governed family names within one namespace version.

If two derivations claim the same family at the same anchor, then they claim the same analytical object, and consistency becomes a governance obligation.

Thus:

$$
\boxed{
C(d_1)=C(d_2)
\Rightarrow
\text{same measure identity; consistency required}
}
$$

while:

$$
\boxed{
C(d_1)\neq C(d_2)
\Rightarrow
\text{different measures; equality not required}
}
$$

The resulting architecture is small:

```text
Universe Existence Law
  -> Root-Point Domain
  -> Partition Geometry
  -> Measure Families and Measures
  -> Operators and Sufficient State
  -> Family Coherence
  -> Family-Level Lineage DAG
  -> Analytical Governance
```

It is also practical. A governed family name can serve as the stable handle for a complete analytical identity. The ordinary measure expression:

```text
measure_family @ anchor
```

is therefore meaningful on its face. The full lineage remains underneath it for governance, explanation, certification, and implementation, while ordinary references can use the compact governed handle.

This provides a clear foundation for analytical systems and analytical agents. Governed identity can be resolved directly instead of inferred from physical tables or free-floating metric names. A governed system can instead ask whether the requested family exists, whether its name resolves uniquely, whether the requested anchor is lawful, how the family stands in the universe-wide lineage DAG, and whether the necessary state and contracts support the requested derivation.

The Theory preserves analytical differences while making their governing structure explicit:

> **make the structural differences explicit enough that distinct analytical objects remain distinguishable in governance and execution.**

---

# Appendix A. Minimal Conformance Surface

This appendix gives an implementation-neutral sketch of the declarations needed for structural conformance. It is intentionally smaller than a complete governed-publication format, catalog protocol, or publication system.

A conforming publication needs enough information to identify universes, anchors, families, lineage edges, and realization certificates.

## A.1 Universe declaration

```yaml
universe:
  universe_id: "..."
  existence_law:
    kind: "occurrence | declared | generated | other"
    declaration_ref: "..."
  primitive_core:
    root_anchor_id: "..."
    primitive_dimensions: [...]
    primitive_family_ids: [...]
```

The declaration establishes the governed point domain and the root geometry on which later identities depend.

## A.2 Anchor declaration

```yaml
anchor:
  anchor_id: "..."
  universe_id: "..."
  partition_signature: "..."
  dimension_refs: [...]
  refinement_edges: [...]
```

`partition_signature` identifies the governed partition semantics independently of the physical grouping expression that happened to produce one observed table.

## A.3 Family declaration

```yaml
family:
  family_id: "immutable-id-or-digest"
  canonical_name: "revenue"
  namespace_version: "..."
  universe_id: "..."
  designated_root:
    anchor_id: "..."
    establishment_ref: "..."
  parent_family_ids: [...]
  family_law:
    state_schema: "..."
    combine_law: "..."
    finalizer: "..."
    ordering_semantics: "..."
    admitted_reductions: [...]
  identity_contracts:
    participation: "..."
    multiplicity: "..."
    unit_or_currency: "..."
    regime: "..."
    other: [...]
  semantic_signature: "canonicalized declaration or digest"
```

The `family_id` is primary. `canonical_name` is the governed human-readable handle.

The semantic signature excludes identity-neutral publication metadata. A new namespace version can preserve the same family ID when identity-bearing semantics remain unchanged.

## A.4 Derivation-edge declaration

```yaml
edge:
  edge_id: "..."
  source_refs:
    - family_id: "..."
      anchor_id: "..."
  target_ref:
    family_id: "..."
    anchor_id: "..."
  edge_role: "family_preserving | family_establishing"
  operation_semantics: "..."
  edge_contract:
    support: "..."
    relationship_or_allocation: "..."
    order: "..."
    other: [...]
  certificate_ref: "..."
```

A multi-parent synthesis lists several `source_refs`.

For a family-preserving edge, the target family ID equals the source family ID. A family-establishing edge targets a distinct family ID whose semantic signature records the constitutive ancestry.

## A.5 Certificate / materialization declaration

```yaml
certificate:
  certificate_id: "..."
  target_measure:
    family_id: "..."
    anchor_id: "..."
  exactness: "exact | approximate"
  approximation_contract: "..."
  retained_state: "..."
  evidence_status: "..."
  materialization_refs: [...]
```

This layer can change while family identity remains stable.

## A.6 Conformance and authority

A publication is **structurally conforming** when the declarations required by its analytical claims are present, internally resolvable, and satisfy the well-formedness conditions of the theory.

A separate institutional question remains:

> Which conforming publication has authority for this organization or use?

That decision belongs to the surrounding governance system.

The separation is deliberate:

$$
\boxed{
\text{structural conformance}
\neq
\text{institutional authority}.
}
$$

# References

Buneman, Peter, Sanjeev Khanna, and Wang-Chiew Tan. 2001. “Why and Where: A Characterization of Data Provenance.” In *Database Theory - ICDT 2001*, 316-330. DOI: [10.1007/3-540-44503-X_20](https://doi.org/10.1007/3-540-44503-X_20).

Bitol. 2026. *Open Data Contract Standard*, Version 3.1.0. Accessed 19 August 2026. https://bitol-io.github.io/open-data-contract-standard/v3.1.0/


Gray, Jim, Surajit Chaudhuri, Adam Bosworth, Andrew Layman, Don Reichart, Murali Venkatrao, Frank Pellow, and Hamid Pirahesh. 1997. “Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals.” *Data Mining and Knowledge Discovery* 1: 29-53. DOI: [10.1023/A:1009726021843](https://doi.org/10.1023/A:1009726021843).

Green, Todd J., Grigoris Karvounarakis, and Val Tannen. 2007. “Provenance Semirings.” In *Proceedings of the Twenty-Sixth ACM SIGACT-SIGMOD-SIGART Symposium on Principles of Database Systems*, 31-40. DOI: [10.1145/1265530.1265535](https://doi.org/10.1145/1265530.1265535).

Lenz, Hans-Joachim, and Arie Shoshani. 1997. “Summarizability in OLAP and Statistical Data Bases.” In *Proceedings of the Ninth International Conference on Scientific and Statistical Database Management*, 132-143. DOI: [10.1109/SSDM.1997.621175](https://doi.org/10.1109/SSDM.1997.621175).

Pedersen, Torben Bach, Christian S. Jensen, and Curtis E. Dyreson. 2001. “A Foundation for Capturing and Querying Complex Multidimensional Data.” *Information Systems* 26(5): 383-423. DOI: [10.1016/S0306-4379(01)00023-0](https://doi.org/10.1016/S0306-4379(01)00023-0).

Thoughtworks. 2026. “Semantic Layer.” *Technology Radar*, April 2026. Accessed 19 August 2026. https://www.thoughtworks.com/radar/techniques/semantic-layer

W3C. 2013. *PROV-DM: The PROV Data Model*. W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-dm/

Wang, Huayin. 2026a. *The Theory of Data: A Foundational Framework for Governed Analytical Data, Lawful Transformation, and Certification*. Version 5.0. Zenodo. DOI: [10.5281/zenodo.21842194](https://doi.org/10.5281/zenodo.21842194).

Wang, Huayin. 2026b. *The Two Anchors of a Measure: Why Input and Output Anchors Are Part of Analytical Meaning*. Version 2.0. Zenodo. DOI: [10.5281/zenodo.21888464](https://doi.org/10.5281/zenodo.21888464).

Wang, Huayin. 2026c. *A Contract Calculus for Governed Analytical Transformation: Totality, Partiality, Population, Expansion, and Fan-Out*. Version 1.0. Zenodo. DOI: [10.5281/zenodo.21752373](https://doi.org/10.5281/zenodo.21752373).

Wang, Huayin. 2026d. *Regime Has a Contract: Intervention, Observation, and the Data Foundation of Causal Identification*. Version 1.0. Zenodo. DOI: [10.5281/zenodo.21840854](https://doi.org/10.5281/zenodo.21840854).

Wang, Huayin. 2026e. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: [10.5281/zenodo.21979821](https://doi.org/10.5281/zenodo.21979821).

Wang, Huayin. 2026f. *Frame-QL: An Introduction — Query by Declaring the Result*. Version 2.1. Zenodo. DOI: [10.5281/zenodo.21966453](https://doi.org/10.5281/zenodo.21966453).

Wang, Huayin. 2026g. *Certifiable State Under Information Loss: Governed Derivability, Claim Transport, and Approximate Closure*. Version 1.0. Zenodo. DOI: [10.5281/zenodo.21972541](https://doi.org/10.5281/zenodo.21972541).

# Compact Formal Summary

This summary collects the foundation without turning the paper into a reference manual.

## Definitions

**Universe.** A governed root-point domain $\Omega_U$ established under an explicit existence law $\lambda_U$, together with its primitive analytical core.

**Root point.** A point that cannot be refined further within the governed universe.

**Anchor.** A governed partition $A$ of $\Omega_U$.

**Refinement.** $B\succeq A$ when every $B$-point belongs to exactly one $A$-point; $B\succ A$ when additionally $B\neq A$.

**Dimension.** A conventionally named governed partition.

**Datum.** One governed typed value at one anchor point.

**Measure family.** A governed analytical family carrying one ex-ante semantic identity signature, immutable family ID, designated family root, declared family law, identity-bearing contracts, and constitutive ancestry.

**Semantic identity signature.** $\Sigma(F)$ is the canonicalized identity-bearing declaration of family $F$, including universe, designated root, parents, family-establishing construction, family law, and identity-bearing contracts.

**Family ID.** An immutable identifier for one semantic family identity. An implementation may derive $id(F)=H(\Sigma(F))$ or assign another immutable identifier tied to the declaration.

**Measure.** A measure family at an anchor: $F@A$.

**Mapper.** An anchor-preserving value transformation.

**Reducer.** A value transformation from a strictly finer anchor to a coarser anchor within one universe.

**Sufficient state.** State $S$ sufficient for lawful continuation of a reducer, together with initialization, combination, identity, and finalization laws.

**Family root.** The designated governed measure $F@R_F$ at which the family declaration begins. Its uniqueness comes from declaration, not from an assumed unique greatest refinement in the anchor partial order.

**Graft.** A governed family-boundary event that establishes the root of a new measure family from an existing governed analytical object.

**Lineage graph.** The universe-level graph whose nodes are uniquely named measure families and whose directed edges record constitutive family-establishing analytical ancestry; a well-formed governed lineage graph is required to be well-founded and acyclic.

**Canonical family name.** A governed human-readable handle resolving to exactly one immutable family ID within an active namespace version.

**Family succession.** A change to an identity-bearing field of $\Sigma(F)$, including $Law(F)$ or $Contracts_{id}(F)$, establishes a successor family identity. A later namespace version may resolve the same canonical name to that successor while prior IDs remain historically resolvable.

**Family state equivalence.** $K_1\equiv_F K_2$ means that two sufficient states are equivalent under the equality relation declared by family law $F$. A conforming relation is a congruence for admitted combination and implies equal final displays.

**Governance contract.** For a direct derivation edge $e$, $\Gamma(e)$ is the set of edge-validity predicates and declarations whose satisfaction licenses that edge under its claimed analytical identity.

**Certificate/materialization contract.** Declaration of exactness, approximation, retained capability, evidential status, and realization properties for a materialized analytical claim.

**Structural conformance.** Satisfaction of the declaration and well-formedness requirements needed for ToD to evaluate analytical identity, derivability, and consistency. Institutional authority is external to this condition.

## Well-formedness conditions

### W1 - Universe existence

The governed root-point domain $\Omega_U$ is established under a declared existence law $\lambda_U$. Anchor geometry partitions points whose existence has already been governed.

### W2 - Lineage well-foundedness

Constitutive family ancestry is acyclic and well-founded.

### W3 - Rooted standing

Every governed family in universe $U$ has constitutive ancestry rooted in the primitive core of $U$:

$$
F\text{ governed in }U
\Rightarrow
U\rightsquigarrow_L F.
$$

### W4 - Contracted edge validity

A direct lineage edge $e$ is licensed under its claimed analytical identity only when its governance contract $\Gamma(e)$ is satisfied. Family path-equivalence claims presuppose satisfaction of the contracts on the family-preserving edges involved.


### W5 - Ex-ante family identity

A governed family identity is established from its semantic signature before result comparison:

$$
\Sigma(F)
=
\operatorname{canon}
(U_F,R_F,Parents(F),Establish(F),Law(F),Contracts_{id}(F)).
$$

Consistency outcomes may test consequences of that identity; they do not create or revise it retroactively.

### W6 - Family-state equivalence well-formedness

If family $F$ declares a state equivalence relation $\equiv_F$, that relation must be a congruence for the family's admitted combine law and must refine display equality:

$$
K_1\equiv_F K_2
\Rightarrow
\phi_F(K_1)=\phi_F(K_2).
$$

A declaration that collapses analytically distinguishable states while violating either condition is nonconforming.

## Core theorem

### Theorem 1 - Family path independence

For one coherent family law with commutative-monoid sufficient state, and with the required edge contracts satisfied, lawful family-preserving paths between the same source and target anchors are path-independent. The algebraic fold result is standard; its ToD role is to govern when staging can be erased from analytical identity.

## Core propositions

### P1 - Partition projection

$$
B\succeq A
\Rightarrow
\text{every B-point belongs to exactly one A-point.}
$$

### P2 - Mapper geometry

$$
F@A\xrightarrow{mapper}G@A.
$$

### P3 - Reducer geometry

$$
F@B\xrightarrow{reducer}G@A
\Rightarrow
B\succ A.
$$

### P4 - Family membership does not imply mutual reachability

Measures of one family may occupy incomparable anchors.

### P5 - Graft identity

The rule and anchor that establish a new family root contribute to that family's analytical identity.

### P6 - Family compression

A coherent family-internal derivation subpath may be replaced in canonical lineage by its family identity.

### P7 - Unique family naming

Within one governed namespace version:

$$
name_U(F_1)=name_U(F_2)
\Rightarrow
id(F_1)=id(F_2).
$$

The name resolves identity; it does not constitute identity.

### P7a - Family succession

If an identity-bearing field in $\Sigma(F)$ changes, the successor declaration has a distinct family identity. A later namespace version may resolve the same canonical name to that successor while preserving prior family IDs.

### P8 - Identity-relative consistency

For canonicalization function $C$, under satisfied contracts:

$$
C(d_1)=C(d_2)=F@A
\Rightarrow
K(d_1)\equiv_F K(d_2).
$$

Finalized display equality follows under the family finalizer. If canonical identities differ, ToD imposes no equality requirement.

Identity is established ex ante from the family signature; comparison never determines identity retroactively.

### P9 - Materialized derivability

Analytical derivability does not imply that every stored representation retains sufficient state to execute the derivation.

---

## Publication note

**Version 6.1.** Publication version.

**DOI:** **10.5281/zenodo.22013410**

**Supersedes:** Version 6.0, DOI **10.5281/zenodo.21958062**

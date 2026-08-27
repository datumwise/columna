---
title: "A Contract Calculus for Governed Analytical Transformation"
subtitle: "Totality, Partiality, Population, Expansion, and Fan-Out"
author: "Huayin Wang"
date: "2026-08-01"
lang: en-US
documentclass: article
papersize: letter
fontsize: 10pt
geometry: margin=0.9in
colorlinks: true
linkcolor: blue
urlcolor: blue
---

**datumwise, an independent open-source research project**  
**Version 1.0**  
**Companion to:** *The Theory of Data*  
**Technical supplement collection:** released separately as a versioned research artifact

**Keywords:** analytical data; semantic layers; data contracts; sufficient state; population; partiality; aggregation; fan-out; allocation; certification

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

---

## Abstract

Analytical engines can compute values without establishing that those values are entitled to the analytical identities, population claims, or downstream operations assigned to them. A stock can be summed across time, a join can replicate a measure, an empty fold can be displayed as zero, and a finalized statistic can be re-aggregated after its sufficient state has been discarded. Such plans may be typed, executable, deterministic, and numerically stable.

This paper defines a finite, syntax-directed contract calculus that separates physical evaluation from governed analytical closure. The calculus is organized as three conservative fragments:

$$
G_0\subset G_1\subset G_2.
$$

The total-atom core \(G_0\) combines nominal value types, anchors, aggregate sufficient-state algebras, and capability-indexed movement boundaries. It proves determinacy under disciplined staging, compositional boundary checking, decidable certification, and the existence of evaluable but non-closing plans. An ordered extension proves that scalar `first` and `last` require declared fiber order rather than physical enumeration.

The partiality-and-population fragment \(G_1\) adds finite image-generated universes, complete grain \((U,A)\), eligibility \(E\), observed support \(S\), structural restriction, explicit population carving, and two coverage modes. Its reducers carry aggregate state together with eligible and observed counts, so value, support, and coverage decisions survive distributed staging.

The expansion fragment \(G_2\) adds finite relation-edge universes and explicit dispositions for replication, source-functional assignment, and exact unit-sum allocation. It proves the replication multiplicity law, refuses silent loss of unmatched eligible sources, synthesizes downstream boundaries for duplication-sensitive capabilities, and proves conservation for assignment and exact allocation under stated premises.

Two worked certificates apply the fragments to inventory across time and orders expanded to order items. They distinguish certified plans, deterministic non-closing plans, explicit population changes, contract synthesis, and operations that remain outside the proved grammar.

The result is a small trusted-kernel basis for semantic-layer certification: the planner may propose a computation, but only the calculus determines which governed object, if any, that computation is entitled to produce.

## Publication and proof status

This paper is independently readable and contains the principal definitions, rules, theorem statements, and proofs or proof sketches. The accompanying technical supplement collection preserves the complete fragment reports, extended derivations, and machine-readable certificates used to construct this unified presentation. Editorial review records are retained separately as development history.

The formal guarantees are **relative** to finite declarations, registered operator laws, admitted physical disciplines, and source contracts. The calculus proves internal derivability; it does not prove that source declarations are externally true.

![The formal development is a conservative fragment chain.](figures/figure_1_fragment_chain.png){width=95%}

### Claim-status summary

| Fragment | Adds | Proved scope |
|---|---|---|
| \(G_0\) | Total atoms, anchors, sufficient-state reducers, movement boundaries, ordered fibers | Finite registries, total atoms, declared pure functions, registered exact capabilities |
| \(G_1\) | Population, eligibility, support, restriction, carve, `Any` and `Complete` coverage | Finite image-generated universes and structural subsets |
| \(G_2\) | Relation-edge universes, replication, assignment, exact allocation, fan-out refusal | Finite declared relations, exact dispositions and weights |
| Later fragments | Partial ordered selection, temporal integration, approximation, observation, evidence, frames | Not proved here |

---

# Part I - Problem, contribution, and position

# 1. The governed-result problem

The central problem is not whether an analytical engine can compute a value. It is whether the computed value has a complete and defensible analytical identity.

SQL engines, data frames, OLAP systems, and semantic layers are designed to evaluate expressions over stored values. They can group, join, sort, aggregate, window, and project. These capabilities are necessary for analytics, but physical executability does not by itself determine:

- what analytical type a result has;
- what population it describes;
- where the result is located;
- whether multiplicity has been preserved;
- whether displayed state is sufficient for re-aggregation;
- whether physical enumeration realizes a logical order;
- whether the result may inherit the source measure's identity;
- whether it may participate in later governed calculations.

The distinction appears in several recurring failure classes.

## 1.1 Fan-out double counting

Suppose an order-level amount is joined to several order-item rows. The join is physically valid. The amount is copied to every related item row. A subsequent sum over the joined rows is also physically valid.

Let:

$$
q:J\to O
$$

map joined rows \(J\) back to source orders \(O\), and let:

$$
w:O\to M
$$

be an order-level measure in an additive commutative monoid \((M,+,0)\).

Then:

$$
\sum_{j\in J}w(q(j))
=
\sum_{o\in O}
\left|q^{-1}(o)\right|w(o).
$$

The joined sum is the multiplicity-weighted source sum. It agrees with the original order-level sum only under an appropriate multiplicity law, such as singleton fibers, deduplication by order identity, or explicit allocation weights.

The problem is not that the sum operator malfunctioned. It is that a valid value operation was applied after a structural expansion that changed the multiplicity of the measure.

## 1.2 Stock summed across time

An inventory quantity may use an ordinary integer carrier and support ordinary addition. A database can therefore sum daily inventory snapshots across a quarter.

That computation is numerically defined. It does not follow that the result is another inventory level.

A stock quantity records a state at an instant or reference time. Summing repeated observations of that state across time generally produces a different quantity, such as inventory-unit-days, not an inherited stock identity. The arithmetic can remain useful under a new contract. It cannot inherit the source contract automatically.

## 1.3 Mean of means

A displayed mean:

$$
\bar x
$$

does not generally contain enough state for exact re-aggregation. Exact composition requires at least:

$$
(\operatorname{sum},\operatorname{count}).
$$

For subgroup states \((s_i,n_i)\), the combined mean is:

$$
\frac{\sum_i s_i}{\sum_i n_i}.
$$

An unweighted mean of the displayed subgroup means is a different statistic unless the subgroup weights happen to agree.

Again, every arithmetic step may be executable. The error is a loss of sufficient state followed by an unjustified inheritance of the original statistical identity.

## 1.4 Physical first without logical order

Every execution traverses rows or particles in some sequence. A host system can therefore return a physically encountered first value.

A certifiable analytical `first`, however, requires a declared order over the relevant source points. Sorting may realize that order; it does not create the analytical order.

A physical result can therefore be deterministic within one plan while remaining execution-relative or semantically unspecified across plans.

## 1.5 The governing distinction

These examples motivate two different questions.

**Value question.**

> Can the host compute a typed value?

**Governed-result question.**

> Does the computation derive a result with an inherited or explicitly created analytical contract?

The paper's principal claim is:

> **Producing a value is not the same as producing a governed analytical object.**

This paper makes this claim formal in a deliberately restricted calculus. The core result is not merely that some uncertified plans are nondeterministic. It is that a plan may be typed, executable, and invariant under all admitted execution schedules while still having no certification derivation under its inherited contract.

---

# 2. Contributions, claims, and limits

The paper separates proved results from framework definitions and research targets.

## 2.1 Claim-status table

| Claim | Status in this paper | Basis |
|---|---|---|
| Nominally typed pointwise functions can be checked before structural movement | Defined in \(G_0\) | Finite function registry |
| Order-insensitive aggregate state is invariant to fiber enumeration | Proved | Commutative-monoid laws |
| Staged state aggregation equals direct state aggregation | Proved | Fiber partition and monoid laws |
| Inherited boundary checks compose across anchor factorizations | Proved | Spent-axis composition |
| Certified plans are deterministic under state-disciplined schedules | Proved | Structural induction |
| A plan can be evaluable and deterministic but non-closing | Proved by witness | Raw typing plus failed boundary side condition |
| Certification in \(G_0\) is decidable with a stated complexity bound | Proved | Syntax-directed traversal |
| Scalar `first` and `last` cannot be certified from bag structure alone | Proved | No natural section from bags to lists |
| Partiality, eligibility, support, observation, and evidence form a complete calculus | Not claimed | Framework extension |
| The full analytical language has a complete map/reduce normal form | Conjecture | Open research |
| Natural-language intent can be decided automatically | Not claimed | External interpretation problem |
| Source contracts are true because they are internally well formed | Not claimed | External adequacy remains a premise |

## 2.2 Main formal contribution

The contract-inclusive core introduces two judgments.

Raw value typing:

$$
\Gamma\vdash_{\mathrm{raw}}P:X@A
$$

states that plan \(P\) has a typed physical denotation of type \(X\) at anchor \(A\).

Certification:

$$
\Gamma\vdash P\Downarrow(v,C)
$$

derives both the canonical value function \(v\) and the output contract \(C\).

The distinction allows the central separation theorem:

$$
\exists\,\Gamma,P,X,A,v:
$$

$$
\Gamma\vdash_{\mathrm{raw}}P:X@A,
$$

$$
\forall\sigma,\quad\llbracket P\rrbracket_\sigma=v,
$$

but:

$$
\nexists C,\quad
\Gamma\vdash P\Downarrow(v,C).
$$

The refusal is therefore not a safeguard against an unstable execution. It is a refusal to inherit an analytical identity across a boundary that the contract blocks.

## 2.3 Main design contribution

The core makes three design choices that address defects in the earlier framework.

First, contract boundaries attach to stable aggregate **capability identities**, not operator spellings. If `sum` and `total` are aliases for the same capability, they receive the same boundary rule.

Second, general ordered reduction uses a dependent family of fiber orders. The core does not assume that every anchor map has one uniform reduced-anchor product.

Third, the core does not define semantic coherence through a recursive predicate over arbitrary transformer outputs. It separates:

- local contract well-formedness;
- environment consistency;
- preservation by certification rules;
- external adequacy of the source declarations.

## 2.4 Deliberate restrictions

The proved fragment assumes:

- a finite set of axes;
- finite rooted-tree hierarchies;
- finite anchor spaces;
- total atoms;
- exact operators;
- finite registries;
- deterministic pointwise functions;
- commutative-monoid sufficient state for order-insensitive aggregates;
- conservative inheritance of boundary declarations.

The restrictions are not descriptions of all enterprise data. They define the smallest fragment in which the governed-result distinction can be proved rather than stipulated.

---

# 3. Relation to prior work

The paper combines obligations that existing fields usually treat separately.

## 3.1 Relational and multidimensional data

The relational model established a formal account of relations and relational operations (Codd, 1970). Multidimensional database theory formalized dimensions, levels, and aggregation structure (Gray et al., 1997; Gyssens and Lakshmanan, 1997). Summarizability research examined when roll-up preserves meaningful aggregate results, including constraints on hierarchies and measure behavior (Lenz and Shoshani, 1997; Hurtado, Gutierrez, and Mendelzon, 2005).

The present core does not replace that work. It isolates a smaller contract question:

> When may the result of a typed reduction inherit the analytical identity of its source?

The boundary map \(\beta\) is intentionally operator-indexed. It can express that a capability is available over the value carrier while blocked from spending particular axes under the inherited contract.

## 3.2 Aggregate classifications and sufficient state

Gray et al.'s distributive, algebraic, and holistic classification concerns the structure needed to combine partial aggregate results.

The core represents an aggregate capability \(\kappa\) through:

$$
(S_\kappa,\oplus_\kappa,0_\kappa,\eta_\kappa,\rho_\kappa),
$$

where:

- \(S_\kappa\) is the sufficient-state carrier;
- \((S_\kappa,\oplus_\kappa,0_\kappa)\) is a commutative monoid;
- \(\eta_\kappa\) embeds one input value into state;
- \(\rho_\kappa\) finalizes state into the displayed result.

This formulation makes staged aggregation a theorem about state. It also explains why displayed output may or may not be suitable for re-aggregation.

## 3.3 Provenance and multiplicity

Provenance semirings and aggregate-provenance work provide formal accounts of how source contributions and multiplicities propagate through relational queries (Green, Karvounarakis, and Tannen, 2007; Amsterdamer, Deutch, and Tannen, 2011).

The fan-out law in this paper is compatible with that tradition. Provenance can explain that a source fact was replicated and with what multiplicity. The governed contract adds a different question: whether the replicated or recombined value may retain the source analytical identity.

Multiplicity is therefore necessary evidence for certification, but not a complete output contract.

## 3.4 Units and nominal value typing

Units-of-measure type systems show that physically similar carriers can support different legal operations because their dimensions or nominal identities differ (Kennedy, 1996).

The core adopts the same principle for analytical value types. Equality of carriers does not identify types, and a pointwise function must be declared on its nominal input types.

The contribution is not a new theory of units. It places nominal value typing before aggregate-state construction and contract inheritance.

## 3.5 Indexed families and data migration

Anchor maps, fibers, reindexing, and fiberwise combination are closely related to indexed-set and functorial data-migration semantics (Spivak, 2012; Spivak and Wisnesky, 2015).

The core uses only the restricted consequences it proves directly:

- fibers are preimages of admitted anchor maps;
- bag pushforward forgets enumeration but preserves multiplicity;
- state aggregation composes over fiber partitions;
- no canonical bag ordering exists.

It does not claim that the complete governed framework has already been reduced to a categorical model.

## 3.6 Semantic and metrics layers

Systems such as LookML, Malloy, dbt Semantic Layer, and Cube address shared metrics, joins, aggregate planning, and reuse. Looker's symmetric aggregates and Malloy's join-cardinality handling directly target fan-out duplication.

The present contribution is positioned above any one implementation language. It asks whether a proposed result can be certified as a governed analytical object under explicit type, structure, boundary, and execution premises.

The core is therefore a candidate certification substrate, not a replacement for semantic-layer execution or modeling systems.

---

# Part II - Analytical objects used by the core

# 4. Values, coordinates, anchors, particles, and atoms

## 4.1 Nominal value types

Let:

$$
X\in\mathsf{Type}
$$

be a nominal value type with carrier set \(|X|\).

Two types may share a carrier without being identical:

$$
|\mathrm{RevenueUSD}|
=
|\mathrm{CostUSD}|
=
\mathbb R,
$$

while:

$$
\mathrm{RevenueUSD}
\neq
\mathrm{CostUSD}.
$$

A typed pointwise function is a declared operation:

$$
f:X_1\times\cdots\times X_n\to Y.
$$

Physical compatibility of carriers does not create such a declaration.

Aggregate availability is also typed. An aggregate capability specifies its accepted input type, output type, sufficient-state algebra, embedding, and finalizer.

## 4.2 Axes and levels

Let:

$$
\mathsf{Axis}
$$

be a finite set of axes.

Each axis \(\alpha\) has a finite rooted tree of levels:

$$
\mathsf{Level}_\alpha.
$$

The root is a terminal singleton level:

$$
\top_\alpha.
$$

If level \(D\) is finer than level \(E\), write:

$$
D\preceq_\alpha E.
$$

The declaration supplies a functional coarsening:

$$
c^\alpha_{D,E}:|D|\to|E|.
$$

The component maps satisfy:

$$
c^\alpha_{D,D}=\operatorname{id}_{|D|}
$$

and:

$$
c^\alpha_{E,H}\circ c^\alpha_{D,E}
=
c^\alpha_{D,H}.
$$

The tree restriction ensures that every admitted coarsening path on one axis is unique. Ragged, non-strict, contextual, and time-varying hierarchies remain outside the proved fragment.

## 4.3 Anchors and anchor points

An anchor selects one level from each axis:

$$
A:\mathsf{Axis}\to\bigcup_\alpha\mathsf{Level}_\alpha.
$$

Its anchor space is:

$$
\operatorname{Pts}(A)
=
\prod_{\alpha\in\mathsf{Axis}}|A(\alpha)|.
$$

An anchor point is:

$$
a\in\operatorname{Pts}(A).
$$

An admitted anchor map:

$$
q:A\to A'
$$

exists when:

$$
A(\alpha)\preceq_\alpha A'(\alpha)
$$

for every axis \(\alpha\). It applies the unique per-axis coarsening componentwise.

Because every axis hierarchy is a tree, the resulting anchor category is thin: between two anchors there is at most one admitted coarsening.

## 4.4 Particles and total atoms

A particle is one typed value at one anchor point:

$$
p=(a,x),
\qquad
a\in\operatorname{Pts}(A),
\quad
x\in|X|.
$$

An \(X\)-typed total atom over anchor \(A\) is:

$$
v:\operatorname{Pts}(A)\to|X|.
$$

> **Intuition.** A particle resembles a typed analytical key-value pair. An atom resembles a homogeneous semantic column indexed by complete analytical keys. These are teaching aliases, not formal equivalences.

The full framework permits partial atoms over governed universes. The proved core suppresses those distinctions so that value and contract composition can be isolated.

## 4.5 Spent axes

For:

$$
q:A\to A',
$$

define:

$$
\operatorname{Spent}(q)
=
\{
\alpha\in\mathsf{Axis}
\mid
A(\alpha)\neq A'(\alpha)
\}.
$$

An axis is spent when the map removes distinctions along that axis.

**Lemma G0.L1 (spent-axis composition).** For:

$$
A\xrightarrow{q}A'\xrightarrow{r}A'',
$$

$$
\operatorname{Spent}(r\circ q)
=
\operatorname{Spent}(q)
\cup
\operatorname{Spent}(r).
$$

**Proof.** On a rooted-tree axis, a coarsening cannot return to a finer level. The composite acts as the identity on an axis exactly when both component maps act as identities on that axis. **QED.**

This elementary lemma supplies the contract-side composition law used later.

---

# 5. Fibers, aggregation, and logical order

## 5.1 Fibers

For an anchor map:

$$
q:A\to A'
$$

and target point:

$$
a'\in\operatorname{Pts}(A'),
$$

the source fiber is:

$$
\operatorname{Fib}_q(a')
=
\{
a\in\operatorname{Pts}(A)
\mid
q(a)=a'
\}.
$$

A fiber is a set of source points related to one target point.

A SQL group is a common physical representation of such a fiber. The formal object is the preimage of the grouping map, not the row container used to implement it.

## 5.2 Order-insensitive aggregates

An order-insensitive aggregate depends on input values and their multiplicities but not on their enumeration.

Its denotation factors through a bag:

$$
g:\operatorname{Bag}(X)\to Y.
$$

In the proved fragment, an aggregate capability \(\kappa\) is represented by:

$$
(S_\kappa,\oplus_\kappa,0_\kappa,\eta_\kappa,\rho_\kappa).
$$

For bag \(M\):

$$
g_\kappa(M)
=
\rho_\kappa
\left(
\bigoplus_{x\in M}
\eta_\kappa(x)
\right).
$$

The aggregate function is not itself a monoid. Its sufficient-state combination may form a commutative monoid.

## 5.3 Display value versus sufficient state

For sum:

$$
S_{\mathrm{sum}}=X,
\qquad
\eta_{\mathrm{sum}}=\operatorname{id},
\qquad
\rho_{\mathrm{sum}}=\operatorname{id}.
$$

For mean:

$$
S_{\mathrm{mean}}
=
\mathbb R\times\mathbb N,
$$

with:

$$
(s_1,n_1)\oplus(s_2,n_2)
=
(s_1+s_2,n_1+n_2),
$$

and:

$$
\rho_{\mathrm{mean}}(s,n)
=
\frac{s}{n}.
$$

A displayed mean is not the sufficient state. Exact re-aggregation requires the state pair.

## 5.4 Anchor-ordered evaluators

`first`, `last`, `nth`, and ordered folds do not factor through bags. They require order over source points.

The core does not infer that order from:

- physical row order;
- the written order of dimensions;
- sortable storage carriers;
- hierarchy alone.

A declared order over each relevant fiber is additional analytical structure.

## 5.5 Anchor-aware evaluators

Duration-weighted means, distance-weighted statistics, interpolation, and geometric operations require more than an enumeration. They require coordinates, intervals, distances, or other structure attached to the source points.

These evaluators belong to the broader framework. They are not included in \(G_0\).

---


![Reducer architecture separates fiber construction, evaluator semantics, and output-contract synthesis.](figures/figure_2_reducer_architecture.png){width=92%}

# 6. Raw evaluation, certification, and closure

## 6.1 Raw value typing

The raw judgment:

$$
\Gamma\vdash_{\mathrm{raw}}P:X@A
$$

states that plan \(P\) has a typed denotation of type \(X\) at anchor \(A\), ignoring contract-inheritance boundaries.

Raw typing establishes:

- source existence;
- declared pointwise-function signatures;
- declared aggregate capability typing;
- admitted anchor maps.

It does not establish that the output may inherit the source analytical identity.

## 6.2 Certification

The certification judgment is:

$$
\Gamma\vdash P\Downarrow(v,C).
$$

It derives:

- a canonical value function \(v\);
- an output contract \(C\).

Within the core, certification is the closure judgment. A certified plan produces a governed result relative to the source bindings and the minimal contract calculus.

## 6.3 Minimal contract

A core contract is:

$$
C=(X,A,\beta),
$$

where:

- \(X\) is the nominal value type;
- \(A\) is the anchor;
- \(\beta\) is a capability-indexed boundary map:
  $$
  \beta:\mathsf{AggCap}\to\mathcal P(\mathsf{Axis}).
  $$

For capability \(\kappa\), the set:

$$
\beta(\kappa)
$$

contains axes that \(\kappa\) may not spend while the output automatically inherits the current contract.

The boundary does not say that the physical operation is unavailable. It says that inherited analytical identity is unavailable across the stated movement.

## 6.4 Contract equivalence

Within \(G_0\):

$$
(X,A,\beta)
\equiv_C
(X',A',\beta')
$$

iff:

$$
X=X',
\qquad
A=A',
$$

and:

$$
\forall\kappa\in\mathsf{AggCap},
\quad
\beta(\kappa)=\beta'(\kappa).
$$

This is nominal equivalence for the proved fragment. The full framework will require richer equivalence and refinement relations.

## 6.5 Closure is relative

Certification is relative to:

- the declarations in \(\Gamma\);
- the admitted plan grammar;
- the aggregate capability registry;
- the boundary map;
- the execution discipline used by the physical soundness theorem.

A certified result can still rest on a false source declaration. Internal derivability is not external truth.

---


![Physical evaluation, particle typing, frame evaluation, and governed closure are distinct judgments.](figures/figure_3_evaluation_closure_judgments.png){width=92%}

# Part III - The contract-inclusive proved calculus

# 7. Core fragment \(G_0\)

## 7.1 Registries

The declaration environment contains finite registries for:

- axes and levels;
- nominal value types;
- pointwise functions;
- aggregate capabilities;
- aggregate-name aliases;
- governed source bindings.

A source binding is:

$$
\Gamma(x)=(v,C),
$$

where:

$$
v:\operatorname{Pts}(A)\to|X|
$$

and:

$$
C=(X,A,\beta).
$$

Source origination and evidential adequacy are premises of the environment.

## 7.2 Aggregate capability identity

Let:

$$
\mathsf{AggCap}
$$

be a finite registry of stable aggregate capability identities.

A capability:

$$
\kappa\in\mathsf{AggCap}
$$

contains:

- input type \(X_\kappa\);
- output type \(Y_\kappa\);
- state carrier \(S_\kappa\);
- commutative operation:
  $$
  \oplus_\kappa:S_\kappa\times S_\kappa\to S_\kappa;
  $$
- identity:
  $$
  0_\kappa\in S_\kappa;
  $$
- input embedding:
  $$
  \eta_\kappa:X_\kappa\to S_\kappa;
  $$
- finalizer:
  $$
  \rho_\kappa:S_\kappa\to Y_\kappa.
  $$

A surface operator name resolves to a capability:

$$
\operatorname{resolveAggName}:
\mathsf{Name}
\rightharpoonup
\mathsf{AggCap}.
$$

Several names may resolve to one capability. An alias therefore cannot bypass a boundary by changing spelling.

The kernel does not decide extensional equality of arbitrary implementations. Declaring a new capability identity is a new semantic premise that remains visible in the certificate.

## 7.3 Plan syntax

The plan grammar is:

$$
P::=
x
\mid
\operatorname{map}_f(P_1,\ldots,P_n)
\mid
\operatorname{red}_{\kappa,q}(P).
$$

The constructors mean:

- \(x\): governed source binding;
- \(\operatorname{map}_f\): pointwise function at one common anchor;
- \(\operatorname{red}_{\kappa,q}\): order-insensitive aggregate capability over fibers of \(q\).

The ordered extension later adds:

$$
\operatorname{last}_{q,\mathcal O}(P)
$$

and related evaluators.

## 7.4 Conservative map-boundary propagation

Suppose the inputs to a pointwise map have boundary maps:

$$
\beta_1,\ldots,\beta_n.
$$

Define:

$$
\operatorname{JoinBoundary}
(\beta_1,\ldots,\beta_n)(\kappa)
=
\bigcup_{i=1}^{n}\beta_i(\kappa).
$$

The output inherits every blocked axis present on any input.

This rule is conservative. It may reject a domain-specific pointwise operation that legitimately creates a new identity or discharges a boundary. Such operations require an explicit contract transformer outside \(G_0\).

## 7.5 Raw typing rules

The raw judgment has one rule per plan constructor.

**Source.**

If:

$$
\Gamma(x)=(v,(X,A,\beta)),
$$

then:

$$
\Gamma\vdash_{\mathrm{raw}}x:X@A.
$$

**Map.**

If:

$$
\Gamma\vdash_{\mathrm{raw}}P_i:X_i@A
$$

for every \(i\), and:

$$
f:X_1\times\cdots\times X_n\to Y
$$

is declared, then:

$$
\Gamma\vdash_{\mathrm{raw}}
\operatorname{map}_f(P_1,\ldots,P_n):Y@A.
$$

**Reduction.**

If:

$$
\Gamma\vdash_{\mathrm{raw}}P:X_\kappa@A
$$

and:

$$
q:A\to A',
$$

then:

$$
\Gamma\vdash_{\mathrm{raw}}
\operatorname{red}_{\kappa,q}(P):Y_\kappa@A'.
$$

No boundary side condition appears in raw typing.

---

# 8. Certification rules and physical semantics

## 8.1 Source rule

$$
\frac{
\Gamma(x)=(v,C)
}{
\Gamma\vdash x\Downarrow(v,C)
}
\quad\textsc{SRC}
$$

## 8.2 Pointwise-map rule

Suppose:

$$
\Gamma\vdash P_i\Downarrow(v_i,(X_i,A,\beta_i))
$$

for every \(i\), all at the same anchor \(A\), and:

$$
f:X_1\times\cdots\times X_n\to Y
$$

is declared.

Define:

$$
v'(a)
=
f(v_1(a),\ldots,v_n(a))
$$

and:

$$
\beta'
=
\operatorname{JoinBoundary}(\beta_1,\ldots,\beta_n).
$$

Then:

$$
\frac{
\Gamma\vdash P_i\Downarrow(v_i,(X_i,A,\beta_i))
\ \forall i
\qquad
f:X_1\times\cdots\times X_n\to Y
}{
\Gamma\vdash
\operatorname{map}_f(P_1,\ldots,P_n)
\Downarrow
(v',(Y,A,\beta'))
}
\quad\textsc{MAP}
$$

The common-anchor requirement is part of the proved core. Alignment and frame synthesis are later extensions.

## 8.3 Reduction rule

Suppose:

$$
\Gamma\vdash P\Downarrow(v,(X,A,\beta)),
$$

capability \(\kappa\) is typed at \(X\), and:

$$
q:A\to A'.
$$

The inherited boundary side condition is:

$$
\operatorname{Spent}(q)
\cap
\beta(\kappa)
=
\varnothing.
$$

Define:

$$
v'(a')
=
\rho_\kappa
\left(
\bigoplus_{a\in\operatorname{Fib}_q(a')}
\eta_\kappa(v(a))
\right).
$$

Then:

$$
\frac{
\Gamma\vdash P\Downarrow(v,(X,A,\beta))
\qquad
X=X_\kappa
\qquad
q:A\to A'
\qquad
\operatorname{Spent}(q)\cap\beta(\kappa)=\varnothing
}{
\Gamma\vdash
\operatorname{red}_{\kappa,q}(P)
\Downarrow
(v',(Y_\kappa,A',\beta))
}
\quad\textsc{RED}
$$

The output inherits \(\beta\) unchanged. Boundary discharge, allocation, unit conversion, and creation of a distinct analytical identity require a different transformer rule outside \(G_0\).

## 8.4 Why reduction can be raw-valid and uncertified

Aggregate capability typing establishes that:

$$
g_\kappa:\operatorname{Bag}(X_\kappa)\to Y_\kappa
$$

is available.

The \textsc{RED} side condition asks a separate question: whether the current contract may be inherited after the map spends the stated axes.

Therefore:

$$
\Gamma\vdash_{\mathrm{raw}}
\operatorname{red}_{\kappa,q}(P):Y_\kappa@A'
$$

does not imply the existence of:

$$
\Gamma\vdash
\operatorname{red}_{\kappa,q}(P)
\Downarrow(v',C').
$$

## 8.5 Physical schedules

A physical schedule \(\sigma\) assigns to every reducer node:

1. a factorization:
   $$
   q=q_m\circ\cdots\circ q_1;
   $$
2. an enumeration of every fiber at every stage;
3. a representation choice for intermediate values.

A schedule is **state disciplined** when:

- every nonfinal stage carries \(S_\kappa\)-state;
- states combine using \(\oplus_\kappa\);
- \(\rho_\kappa\) is applied only after the final stage of that reducer.

The physical denotation is:

$$
\llbracket P\rrbracket_\sigma.
$$

The core does not claim invariance for arbitrary floating-point reassociation, approximate sketches without error contracts, nondeterministic functions, or engines that violate the declared operator laws.

---

# 9. Theorem package

## 9.1 Certified determinacy

**Theorem G0.1.** If:

$$
\Gamma\vdash P\Downarrow(v,C),
$$

then for every state-disciplined schedule \(\sigma\):

$$
\llbracket P\rrbracket_\sigma=v.
$$

**Proof.** By structural induction on \(P\).

For a source node, the physical value is the environment binding.

For a map node, the induction hypotheses identify every input value function under every admitted schedule. Applying the same declared pointwise function at each common anchor point yields the same output function.

For a reducer node, every admitted staging factorization partitions each final fiber into intermediate fibers. Associativity permits regrouping of state, commutativity removes dependence on fiber enumeration and intermediate-group order, and the identity handles empty intermediate groups. State discipline ensures that finalization occurs only after the complete state has been combined. The physical result therefore equals the canonical reducer value derived by \textsc{RED}. **QED.**

## 9.2 Staged sufficient-state equality

Let:

$$
A\xrightarrow{q}A'
\xrightarrow{r}A''.
$$

**Theorem G0.2.** For every:

$$
a''\in\operatorname{Pts}(A''),
$$

$$
\bigoplus_{a:(r\circ q)(a)=a''}
\eta_\kappa(v(a))
=
\bigoplus_{a':r(a')=a''}
\left(
\bigoplus_{a:q(a)=a'}
\eta_\kappa(v(a))
\right).
$$

**Proof.** The sets:

$$
\operatorname{Fib}_q(a')
$$

for:

$$
a'\in\operatorname{Fib}_r(a'')
$$

form a disjoint partition of:

$$
\operatorname{Fib}_{r\circ q}(a'').
$$

The equality follows from associativity, commutativity, and identity of the state monoid. **QED.**

**Corollary G0.3.** Direct and staged aggregate values agree when intermediate stages retain sufficient state and apply the finalizer only after the last combination.

This corollary distinguishes state composition from displayed-value re-aggregation. It explains why mean composes through `(sum, count)` rather than through displayed means.

## 9.3 Boundary-check composition

**Theorem G0.4.** For capability \(\kappa\):

$$
\operatorname{Spent}(r\circ q)\cap\beta(\kappa)=\varnothing
$$

iff:

$$
\operatorname{Spent}(q)\cap\beta(\kappa)=\varnothing
$$

and:

$$
\operatorname{Spent}(r)\cap\beta(\kappa)=\varnothing.
$$

**Proof.** By Lemma G0.L1:

$$
\operatorname{Spent}(r\circ q)
=
\operatorname{Spent}(q)
\cup
\operatorname{Spent}(r).
$$

Intersecting with \(\beta(\kappa)\) yields the empty set exactly when both component intersections are empty. **QED.**

## 9.4 Agreement of value staging and contract staging

**Theorem G0.5.** For a reducer using one capability \(\kappa\), direct and state-disciplined staged execution agree on sufficient state by Theorem G0.2, and direct and staged inherited-boundary checks agree by Theorem G0.4.

Therefore the value projection and the minimal contract projection compose over the same anchor factorization.

This is a proved instance of the paper's broader dual-projection idea. It is not a proof that every analytical transformation has one complete normal form.

## 9.5 Boundary soundness

Call a raw-well-typed reducer node **boundary violating** when:

$$
\operatorname{Spent}(q)
\cap
\beta(\kappa)
\neq
\varnothing.
$$

**Theorem G0.6.** If a raw-well-typed plan contains a boundary-violating reducer node under its propagated input contract, no certification derivation exists for the complete plan in \(G_0\).

**Proof.** Certification is syntax directed. The only rule that concludes a reducer judgment is \textsc{RED}. Its boundary side condition is false at the violating node. Therefore no certification derivation can cross that node. **QED.**

The theorem does not state that the physical value is undefined or unstable.

## 9.6 Central separation theorem

**Theorem G0.7 (evaluable, deterministic, non-closing).** There exist \(\Gamma\) and \(P\) such that:

$$
\Gamma\vdash_{\mathrm{raw}}P:X@A',
$$

$$
\forall\sigma,\quad
\llbracket P\rrbracket_\sigma=v,
$$

but:

$$
\nexists C,\quad
\Gamma\vdash P\Downarrow(v,C).
$$

**Proof by witness.**

Let the axes include `time`. Let:

$$
\kappa_+
$$

be exact integer sum, with sufficient-state monoid:

$$
(\mathbb Z,+,0).
$$

Let source \(x\) have contract:

$$
C_x
=
(
\mathrm{InventoryQuantity},
A,
\beta
),
$$

where:

$$
\mathrm{time}
\in
\beta(\kappa_+).
$$

Choose:

$$
q:A\to A'
$$

that spends the time axis, and define:

$$
P=
\operatorname{red}_{\kappa_+,q}(x).
$$

The raw reduction is typed because \(\kappa_+\) accepts `InventoryQuantity` and \(q\) is admitted.

Every state-disciplined schedule computes the same integer sum by commutativity and associativity.

However:

$$
\operatorname{Spent}(q)
\cap
\beta(\kappa_+)
\neq
\varnothing.
$$

The \textsc{RED} side condition fails, so no certification derivation exists under the inherited contract. **QED.**

The plan can be rebound outside \(G_0\) under a different contract, such as an integrated stock-exposure quantity. That would create a different analytical object rather than prove inherited closure.

## 9.7 Certification decidability and complexity

**Theorem G0.8.** Certification in \(G_0\) is decidable by one bottom-up traversal of the plan.

Let:

- \(|P|\) be the number of plan nodes;
- \(m=|\mathsf{Axis}|\);
- registry lookup be constant time;
- boundary sets be represented as machine-word bitsets.

Then certification takes:

$$
O
\left(
|P|
\cdot
\left\lceil\frac{m}{w}\right\rceil
\right)
$$

machine-word operations, excluding physical evaluation of user functions and aggregate state.

**Proof.** Every syntax node has one applicable certification rule. Source, function, capability, and anchor-map checks are finite-registry lookups. The only nonconstant contract operations are union and intersection over finite axis bitsets. **QED.**

The full framework may contain temporal entailment, evidence combination, universe reconciliation, or probabilistic checks with different complexity.

## 9.8 Well-formedness preservation

Define local contract well-formedness:

$$
\Gamma\vdash_{\mathrm{wf}}(X,A,\beta)
$$

to require:

- \(X\) is a registered type;
- \(A\) is a registered anchor;
- \(\beta\) is total over registered aggregate capabilities;
- every boundary set mentions registered axes;
- source values inhabit \(|X|\).

**Theorem G0.9.** If:

$$
\operatorname{Consistent}(\Gamma)
$$

and:

$$
\Gamma\vdash P\Downarrow(v,C),
$$

then:

$$
\Gamma\vdash_{\mathrm{wf}}C.
$$

**Proof.** By induction on the certification derivation.

\textsc{SRC} returns a well-formed environment binding.

\textsc{MAP} returns a registered output type, the common registered anchor, and the pointwise union of total boundary maps.

\textsc{RED} returns the registered capability output type, an admitted target anchor, and the unchanged total boundary map. **QED.**

This preservation theorem replaces a recursive definition in which a contract was considered coherent only when every possible transformer output was itself coherent.

---

# 10. Ordered evaluators and dependent fiber structure

## 10.1 Why one global reduced anchor is insufficient

For a split product projection:

$$
A\cong A'\times R,
$$

one shared reduced-anchor schema \(R\) describes every fiber.

General maps need not have that uniform form. Hierarchy coarsenings can produce fibers with different cardinalities. Irregular or constrained structures can produce fibers with different internal shapes.

The ordered extension therefore uses the fibers themselves as primary objects.

## 10.2 Dependent fiber-order specification

For:

$$
q:A\to A',
$$

a fiber-order specification is:

$$
\mathcal O_q
=
\{
\le_{q,a'}
\}_{a'\in\operatorname{Pts}(A')},
$$

where each:

$$
\le_{q,a'}
$$

is a declared total order on:

$$
\operatorname{Fib}_q(a').
$$

For regular product projections, the family may be derived from one ordered reduced-anchor schema. For irregular fibers, the dependent family is authoritative.

## 10.3 Physical realization

A physical enumeration:

$$
\pi_{a'}:
\{1,\ldots,n_{a'}\}
\to
\operatorname{Fib}_q(a')
$$

realizes \(\mathcal O_q\) when it enumerates the fiber according to the declared total order and tie policy.

A physical sort, ordered index, source sequence, or engine order guarantee may provide realization evidence. The implementation artifact is distinct from the logical order declaration.

## 10.4 Certified last

For nonempty fibers:

$$
\operatorname{last}_{q,\mathcal O}(v)(a')
=
v
\left(
\max_{\le_{q,a'}}
\operatorname{Fib}_q(a')
\right).
$$

The complete rule also requires an explicit policy for empty fibers.

Certification requires:

- a certified input;
- a declared fiber-order family;
- a typed ordered capability;
- a boundary side condition;
- a nonempty-fiber or empty-fiber policy;
- evidence that physical execution realizes the order.

## 10.5 Ordered soundness

**Theorem G0.10.** Every physical schedule that realizes \(\mathcal O_q\) returns the same certified `last` value.

**Proof.** Every realizing enumeration has the same declared maximal source point in each fiber. The evaluator returns the value at that point. **QED.**

## 10.6 No canonical scalar first or last from a bag

Let:

$$
\pi_X:
\operatorname{List}(X)
\to
\operatorname{Bag}(X)
$$

forget list order.

**Theorem G0.11.** There is no natural family:

$$
s_X:
\operatorname{Bag}(X)
\to
\operatorname{List}(X)
$$

such that:

$$
\pi_X\circ s_X
=
\operatorname{id}
$$

for every set \(X\).

**Proof.** Take:

$$
X=\{0,1\}
$$

and bag:

$$
M=\{\!\{0,1\}\!\}.
$$

A section must choose either `[0,1]` or `[1,0]`. Let:

$$
\tau:X\to X
$$

swap 0 and 1. The bag \(M\) is fixed by \(\tau\). Naturality would therefore require:

$$
\operatorname{List}(\tau)(s_X(M))
=
s_X(M).
$$

But the list action swaps `[0,1]` and `[1,0]`; neither list is fixed. Contradiction. **QED.**

**Consequence.** A generic, symmetry-respecting semantics cannot recover a canonical scalar order from bag structure. Certifiable `first` and `last` require additional ordered structure.

A physical enumeration supplies a sequence for one execution. It becomes analytically authoritative only when it realizes the declared fiber order.

---

# Part IV - Population and partiality

# 11. Fragment extension discipline

The formal development is cumulative but not monolithic:

$$
G_0\subset G_1\subset G_2.
$$

Each fragment fixes a grammar, contract shape, physical discipline, and theorem boundary. A later fragment may add obligations, constructors, or synthesized contracts; it does not retroactively strengthen the claims of an earlier theorem.

This separation keeps assumptions visible, prevents implementation choices from being mistaken for semantic laws, and lets refusal remain informative. A plan outside the current grammar is not thereby analytically wrong. It is **not derivable in the current fragment**.

# 12. \(G_1\) objective, scope, and restrictions

An anchor identifies coordinate structure. It does not identify the population described by a value. Likewise, a partial function alone does not distinguish a point outside the population, an ineligible point, an eligible but unobserved point, or an observed point.

\(G_1\) is the smallest population-and-partiality extension used here. It adds image-generated universes, eligibility, support, structural restriction, population carving, and coverage-aware order-insensitive reducers.

The fragment deliberately excludes scaffold-completed universes, imputation, event-to-zero inference, weighted coverage, joins, partial ordered reducers, observation-process contracts, and evidence. Those exclusions preserve the theorem boundary; they are not claims that the excluded operations are impossible.

# 13. Image-coherent universes and lawful grain

## 13.1. Simple universe class

\(G_1\) uses a deliberately restricted universe class. It formalizes **image-generated populations**: every admitted coarse population point must be reached from at least one represented finer point. This class is chosen because image formation composes directly over the same anchor maps used by the core proofs. It is not proposed as a definition of every enterprise universe.

**Definition G1.D1 (image-coherent universe).** A \(G_1\) universe is:

$$
U=
(\operatorname{id}_U,
\mathcal A_U,
\mathcal P_U),
$$

where:

- \(\operatorname{id}_U\) is stable nominal universe identity;
- \(\mathcal A_U\) is a finite set of admitted anchors;
- \(\mathcal P_U\) assigns each admitted anchor \(A\) a population:
  $$
  P_{U,A}\subseteq\operatorname{Pts}(A).
  $$

The anchor set is upward closed under admitted coarsening. For every:

$$
q:A\to A'
$$

with \(A,A'\in\mathcal A_U\), the populations satisfy:

$$
P_{U,A'}
=
q[P_{U,A}],
$$

where:

$$
q[R]
=
\{q(a)\mid a\in R\}.
$$

This is the **image-coherence law**.

The law makes population representation compose:

$$
P_{U,A''}
=
(r\circ q)[P_{U,A}]
=
r[q[P_{U,A}]].
$$

## 13.2. Lawful grain

**Definition G1.D2.** The judgment:

$$
\Gamma\vdash U@A\Downarrow P_{U,A}
$$

holds when \(U\) is registered, \(A\in\mathcal A_U\), and \(P_{U,A}\) is the registered population at that anchor.

A complete grain is:

$$
(U,A).
$$

An anchor without a lawful universe representation is not a complete analytical grain.

## 13.3. What image coherence does and does not mean

Image coherence says that the population at a coarser anchor consists of coarse points reached by at least one finer population point.

It does not provide:

- completion of missing spine points;
- event-to-zero interpretation;
- nonfunctional hierarchy movement;
- contextual or time-varying membership;
- universe reconciliation;
- transfer between populations.

Those are intentionally excluded from \(G_1\).

A common excluded case is **independent parent existence**. A sales region may remain part of the governed population even when no store represented in the current finer population maps to it. Such a universe is not image generated.

A later scaffold-completion extension may declare:

$$
P_{U,A'}
=
q[P_{U,A}]
\cup
K_{U,A'},
$$

where:

$$
K_{U,A'}
\subseteq
\operatorname{Pts}(A')
$$

is a separately governed coarse-level register or scaffold. The set \(K_{U,A'}\) is not an artificial row-filling trick. It is an additional population premise with its own identity, lineage, and evidence.

**Design boundary.** No theorem in this paper relies on such completion. The current proofs apply only to the image-coherent class of Definition G1.D1. A possible intermediate fragment \(G_{1s}\) may add scaffold-completed universes and prove the corresponding staging and support laws.

## 13.4. Canonical population carve

Let:

$$
R\subseteq P_{U,A}.
$$

**Definition G1.D3 (carved universe).** The carved universe:

$$
U\!\upharpoonright_{A,R}
$$

has:

- a new stable universe identity derived from \((\operatorname{id}_U,A,R)\);
- admitted anchors reachable by coarsening from \(A\);
- population at \(A\):
  $$
  P_{U\upharpoonright R,A}=R;
  $$
- population at any admitted \(A'\) reached by \(q:A\to A'\):
  $$
  P_{U\upharpoonright R,A'}=q[R].
  $$

**Lemma G1.L1.** The carved universe is image coherent.

**Proof.** For:

$$
A\xrightarrow{q}A'\xrightarrow{r}A'',
$$

$$
P_{U\upharpoonright R,A''}
=(r\circ q)[R]
=r[q[R]]
=r[P_{U\upharpoonright R,A'}].
$$

**QED.**

---

# 14. Partial atoms and \(G_1\) contracts

## 14.1. Population, eligibility, and observed support

For a lawful grain \((U,A)\), let:

$$
P=P_{U,A}.
$$

**Definition G1.D4.** A partial atom has:

$$
S\subseteq E\subseteq P,
$$

where:

- \(P\) is the represented population;
- \(E\) is the eligibility set;
- \(S\) is the observed support.

The value function is total on observed support:

$$
v:S\to|X|.
$$

No value is assigned outside \(S\).

## 14.2. Absence states represented in \(G_1\)

For \(a\in\operatorname{Pts}(A)\), \(G_1\) distinguishes:

1. **outside population:**
   $$
   a\notin P;
   $$
2. **ineligible:**
   $$
   a\in P\setminus E;
   $$
3. **eligible but unobserved:**
   $$
   a\in E\setminus S;
   $$
4. **observed:**
   $$
   a\in S.
   $$

Operator exclusion and transformation undefinedness are represented by the output eligibility and support derived by plan rules.

Observed null-like members are excluded. A point in \(S\) has an ordinary value in \(|X|\).

## 14.3. Coverage permissions

Partial aggregation requires more than an axis boundary. It requires a declared rule for whether incomplete observation may still yield an inherited result.

Let:

$$
\mathsf{Cov}
=
\{\mathsf{Any},\mathsf{Complete}\}.
$$

The modes mean:

- \(\mathsf{Any}\): at least one eligible source point is observed; aggregate the observed participating values;
- \(\mathsf{Complete}\): every eligible source point in the fiber is observed.

A coverage-permission map is:

$$
\gamma:
\mathsf{AggCap}
\to
\mathcal P(\mathsf{Cov}).
$$

For capability \(\kappa\), \(\gamma(\kappa)\) lists the coverage modes under which the current analytical identity may be inherited.

This permission is contract specific. A sales-event measure may admit \(\mathsf{Any}\) under an external completeness premise in a later fragment; an inventory snapshot may permit only \(\mathsf{Complete}\). \(G_1\) records the permission but does not infer it.

### 14.3.1. Why only two modes are proved

The two admitted modes are intended to expose the contract mechanism with the smallest finite policy family. They are not asserted to be complete for enterprise analytics.

A natural unweighted extension is:

$$
\mathsf{Threshold}_{\tau},
\qquad
0\le\tau\le 1,
$$

with:

$$
\operatorname{Covered}_{\mathsf{Threshold}_{\tau}}(e,o)
\iff
e>0
\land
\frac{o}{e}\ge\tau.
$$

The existing domain state \((e,o)\) already contains sufficient information to decide this predicate after direct or staged execution. The threshold \(\tau\) would have to be part of the declared coverage permission and therefore part of contract identity.

Weighted coverage requires additional additive state. For declared nonnegative weights \(w(a)\), one possible domain state is:

$$
(e,o,e_w,o_w),
$$

where:

$$
e_w=\sum_{a\in E}w(a),
\qquad
o_w=\sum_{a\in S}w(a).
$$

A weighted threshold can then require:

$$
e_w>0
\land
\frac{o_w}{e_w}\ge\tau.
$$

This extension is sound under staging only when weight identity, eligibility, and additivity are declared before reduction.

### 14.3.2. Contract-directed domain state

The proved \(G_1\) state:

$$
\widehat S_\kappa
=
S_\kappa\times\mathbb N\times\mathbb N
$$

is the specialization needed by the admitted `Any` and `Complete` coverage modes. It is not a requirement that every implementation reserve every possible future coverage field.

For a coverage capability \(h\), let:

$$
D_h
$$

be a declared commutative **domain-state monoid** sufficient to decide the coverage predicate for \(h\). The general contract-directed reducer state has form:

$$
\widehat S_{\kappa,h}
=
S_\kappa\times D_h.
$$

For the two proved modes:

$$
D_{\mathsf{Any}}
=
D_{\mathsf{Complete}}
=
(\mathbb N\times\mathbb N,+,(0,0)).
$$

A weighted-threshold capability may instead require an enlarged domain state containing \(e_w\) and \(o_w\). Another policy may require different finite sufficient state.

**Design constraint.** An implementation may specialize its physical state layout to the selected coverage contract. It need not pre-allocate components for policies that are absent from the contract. What it must preserve is the full declared sufficient state for every policy it certifies.

**Open proof obligation.** A future generic coverage theorem should quantify over registered domain-state monoids and prove that each policy's coverage decision is invariant under state-disciplined staging.

**Design boundary.** Coverage qualification is not numerical approximation. A statistic may be exact over the observed values while having incomplete coverage; an approximate sketch may have complete coverage. Coverage, approximation, and statistical estimation require separate contract components.

## 14.4. \(G_1\) contract

**Definition G1.D5.** A \(G_1\) contract is:

$$
C_1
=
(X,U,A,E,S,\beta,\gamma).
$$

A certified atom is a pair:

$$
(v,C_1),
$$

where:

$$
v:S\to|X|.
$$

## 14.5. Local well-formedness

The judgment:

$$
\Gamma\vdash_{\mathrm{wf1}}(v,C_1)
$$

requires:

1. \(X\) is a registered value type;
2. \(\Gamma\vdash U@A\Downarrow P_{U,A}\);
3. \(S\subseteq E\subseteq P_{U,A}\);
4. \(v:S\to|X|\);
5. \(\beta\) is total over registered aggregate capabilities and mentions only registered axes;
6. \(\gamma\) is total over registered aggregate capabilities and contains only admitted coverage modes.

## 14.6. Contract equivalence in \(G_1\)

Within this fragment:

$$
(X,U,A,E,S,\beta,\gamma)
\equiv_{C_1}
(X',U',A',E',S',\beta',\gamma')
$$

iff all seven components are nominally or extensionally equal as appropriate.

This is current-contract equivalence. It does not identify certificates that used different derivations, predicates, or physical evidence. Certificate equivalence remains separate.

---

# 15. Coverage modes and domain sufficient state

## 15.1. Fiber domain counts

For a contract at \((U,A)\), an anchor map:

$$
q:A\to A',
$$

and target point:

$$
a'\in P_{U,A'},
$$

define:

$$
e_q(a')
=
\left|
\operatorname{Fib}_q(a')\cap E
\right|,
$$

and:

$$
o_q(a')
=
\left|
\operatorname{Fib}_q(a')\cap S
\right|.
$$

Because \(S\subseteq E\):

$$
0\le o_q(a')\le e_q(a').
$$

The output is eligible exactly when:

$$
e_q(a')>0.
$$

## 15.2. Coverage predicates

Define:

$$
\operatorname{Covered}_{\mathsf{Any}}(e,o)
\iff
o>0,
$$

and:

$$
\operatorname{Covered}_{\mathsf{Complete}}(e,o)
\iff
e>0\land o=e.
$$

For mode \(h\in\mathsf{Cov}\), the output support is:

$$
S'_{q,h}
=
\left\{
a'\in P_{U,A'}
\mid
\operatorname{Covered}_h
(e_q(a'),o_q(a'))
\right\}.
$$

The output eligibility is:

$$
E'_q
=
\{a'\in P_{U,A'}\mid e_q(a')>0\}
=
q[E].
$$

## 15.3. Proved extended sufficient state for `Any` and `Complete`

For an aggregate capability \(\kappa\), define the domain-and-value state carrier used by the two proved coverage modes:

$$
\widehat S_\kappa
=
S_\kappa
\times
\mathbb N
\times
\mathbb N.
$$

This is the instance:

$$
\widehat S_{\kappa,h}
=
S_\kappa\times D_h
$$

with:

$$
D_h=\mathbb N\times\mathbb N
$$

for \(h\in\{\mathsf{Any},\mathsf{Complete}\}\).

Define combination:

$$
(s,e,o)
\widehat\oplus_\kappa
(s',e',o')
=
(s\oplus_\kappa s',e+e',o+o').
$$

The identity is:

$$
\widehat 0_\kappa
=
(0_\kappa,0,0).
$$

**Lemma G1.L2.**

$$
(\widehat S_\kappa,
\widehat\oplus_\kappa,
\widehat 0_\kappa)
$$

is a commutative monoid.

**Proof.** The product of commutative monoids is a commutative monoid. \((\mathbb N,+,0)\) supplies both count components. **QED.**

## 15.4. Per-point embedding

For a population point \(a\in P_{U,A}\), define:

$$
\widehat\eta_{\kappa,E,S,v}(a)
=
\begin{cases}
(\eta_\kappa(v(a)),1,1), & a\in S,\\
(0_\kappa,1,0), & a\in E\setminus S,\\
(0_\kappa,0,0), & a\in P_{U,A}\setminus E.
\end{cases}
$$

Folding this state over a target fiber yields:

$$
(s_q(a'),e_q(a'),o_q(a')).
$$

The first component contains sufficient state for observed values only. The second and third components carry the analytical domain facts needed to decide eligibility and support.

## 15.5. Partial reducer denotation

For:

$$
a'\in S'_{q,h},
$$

define:

$$
v'_{q,\kappa,h}(a')
=
\rho_\kappa(s_q(a')).
$$

No value is defined outside \(S'_{q,h}\), even when the aggregate monoid has an identity and:

$$
\rho_\kappa(0_\kappa)
$$

is numerically meaningful.

This is the formal separation between an algebraic empty fold and an observed analytical value.

---

# 16. Plan language

## 16.1. Registered structural subsets

For each lawful grain \((U,A)\), the environment may register a finite structural subset:

$$
R\subseteq P_{U,A}.
$$

Its identity is stable and auditable.

\(G_1\) does not allow an arbitrary data-dependent predicate over another atom. Such predicates require frame semantics.

## 16.2. Syntax

The plan grammar is:

$$
P::=
 x
\mid
\operatorname{map}^{\cap}_f(P_1,\ldots,P_n)
\mid
\operatorname{restrict}_R(P)
\mid
\operatorname{carve}_R(P)
\mid
\operatorname{red}_{\kappa,q,h}(P),
$$

where:

- \(x\) is a source atom;
- \(\operatorname{map}^{\cap}_f\) is a strict intersection-domain pointwise map;
- \(\operatorname{restrict}_R\) narrows eligibility and support while retaining the universe;
- \(\operatorname{carve}_R\) creates a new carved universe;
- \(\operatorname{red}_{\kappa,q,h}\) is an order-insensitive reduction with coverage mode \(h\in\mathsf{Cov}\).

## 16.3. Restriction versus carve

Both operations may expose the same current values on \(R\). Their population claims differ.

Restriction retains:

$$
U
$$

and:

$$
P_{U,A}.
$$

It changes:

$$
E' = E\cap R,
\qquad
S' = S\cap R.
$$

Carve creates:

$$
U\!\upharpoonright_{A,R}
$$

with population:

$$
P_{U\upharpoonright R,A}=R.
$$

The distinction prevents a scoped result from silently becoming a global measure and prevents a new subpopulation from being treated as mere row filtering.

---

# 17. Raw elaboration and certification rules

## 17.1. Raw grain typing

The raw judgment is:

$$
\Gamma\vdash_{\mathrm{raw1}}P:X@(U,A).
$$

It checks type, universe, anchor, structural subset, capability, coverage-mode syntax, and admitted anchor maps. It does not check inherited boundaries or coverage permissions.

### Source

If:

$$
\Gamma(x)=(v,(X,U,A,E,S,\beta,\gamma)),
$$

then:

$$
\Gamma\vdash_{\mathrm{raw1}}x:X@(U,A).
$$

### Strict map

If every input has:

$$
\Gamma\vdash_{\mathrm{raw1}}P_i:X_i@(U,A)
$$

and:

$$
f:X_1\times\cdots\times X_n\to Y,
$$

then:

$$
\Gamma\vdash_{\mathrm{raw1}}
\operatorname{map}^{\cap}_f(P_1,\ldots,P_n)
:Y@(U,A).
$$

### Restrict

If:

$$
\Gamma\vdash_{\mathrm{raw1}}P:X@(U,A)
$$

and \(R\subseteq P_{U,A}\) is registered, then:

$$
\Gamma\vdash_{\mathrm{raw1}}
\operatorname{restrict}_R(P)
:X@(U,A).
$$

### Carve

Under the same premises:

$$
\Gamma\vdash_{\mathrm{raw1}}
\operatorname{carve}_R(P)
:X@(U\upharpoonright_{A,R},A).
$$

### Reduction

If:

$$
\Gamma\vdash_{\mathrm{raw1}}P:X_\kappa@(U,A),
$$

$$
q:A\to A',
$$

$$
\Gamma\vdash U@A'\Downarrow P_{U,A'},
$$

and \(h\in\mathsf{Cov}\), then:

$$
\Gamma\vdash_{\mathrm{raw1}}
\operatorname{red}_{\kappa,q,h}(P)
:Y_\kappa@(U,A').
$$

## 17.2. Certification judgment

The \(G_1\) certification judgment is:

$$
\Gamma\vdash_1 P\Downarrow(v,C_1).
$$

### Source rule

$$
\frac{
\Gamma(x)=(v,C_1)
\qquad
\Gamma\vdash_{\mathrm{wf1}}(v,C_1)
}{
\Gamma\vdash_1 x\Downarrow(v,C_1)
}
\quad\textsc{SRC1}
$$

### Strict intersection-map rule

Suppose:

$$
\Gamma\vdash_1 P_i
\Downarrow
(v_i,(X_i,U,A,E_i,S_i,\beta_i,\gamma_i))
$$

for every \(i\), and:

$$
f:X_1\times\cdots\times X_n\to Y.
$$

Define:

$$
E'=\bigcap_i E_i,
\qquad
S'=\bigcap_i S_i,
$$

$$
v'(a)=f(v_1(a),\ldots,v_n(a))
\quad
(a\in S'),
$$

$$
\beta'(\kappa)
=
\bigcup_i\beta_i(\kappa),
$$

and:

$$
\gamma'(\kappa)
=
\bigcap_i\gamma_i(\kappa).
$$

Then:

$$
\frac{
\Gamma\vdash_1 P_i\Downarrow
(v_i,(X_i,U,A,E_i,S_i,\beta_i,\gamma_i))\ \forall i
\qquad
f:X_1\times\cdots\times X_n\to Y
}{
\Gamma\vdash_1
\operatorname{map}^{\cap}_f(P_1,\ldots,P_n)
\Downarrow
(v',(Y,U,A,E',S',\beta',\gamma'))
}
\quad\textsc{MAP1}
$$

The union of blocked axes and intersection of coverage permissions are conservative automatic-inheritance rules.

### Restriction rule

Let:

$$
\Gamma\vdash_1 P
\Downarrow
(v,(X,U,A,E,S,\beta,\gamma)),
$$

and let \(R\subseteq P_{U,A}\) be registered.

Define:

$$
E'=E\cap R,
\qquad
S'=S\cap R,
\qquad
v'=v|_{S'}.
$$

Then:

$$
\frac{
\Gamma\vdash_1 P\Downarrow(v,(X,U,A,E,S,\beta,\gamma))
\qquad
R\subseteq P_{U,A}
}{
\Gamma\vdash_1
\operatorname{restrict}_R(P)
\Downarrow
(v',(X,U,A,E',S',\beta,\gamma))
}
\quad\textsc{RESTRICT1}
$$

### Carve rule

Under the same input premises, let:

$$
U_R=U\upharpoonright_{A,R}.
$$

Then:

$$
\frac{
\Gamma\vdash_1 P\Downarrow(v,(X,U,A,E,S,\beta,\gamma))
\qquad
R\subseteq P_{U,A}
}{
\Gamma\vdash_1
\operatorname{carve}_R(P)
\Downarrow
(v|_{S\cap R},
(X,U_R,A,E\cap R,S\cap R,\beta,\gamma))
}
\quad\textsc{CARVE1}
$$

### Partial reduction rule

Suppose:

$$
\Gamma\vdash_1 P
\Downarrow
(v,(X,U,A,E,S,\beta,\gamma)),
$$

capability \(\kappa\) accepts \(X\), and:

$$
q:A\to A'.
$$

The side conditions are:

$$
\operatorname{Spent}(q)
\cap
\beta(\kappa)
=
\varnothing,
$$

and:

$$
h\in\gamma(\kappa).
$$

Let:

$$
P'=P_{U,A'},
$$

$$
E'=q[E],
$$

$$
S'
=
S'_{q,h},
$$

and let \(v'\) be the partial reducer denotation from Section 15.5.

Then:

$$
\frac{
\begin{gathered}
\Gamma\vdash_1 P\Downarrow
(v,(X,U,A,E,S,\beta,\gamma))
\\
X=X_\kappa,
\quad q:A\to A',
\quad h\in\gamma(\kappa)
\\
\operatorname{Spent}(q)\cap\beta(\kappa)=\varnothing
\end{gathered}
}{
\Gamma\vdash_1
\operatorname{red}_{\kappa,q,h}(P)
\Downarrow
(v',(Y_\kappa,U,A',E',S',\beta,\gamma))
}
\quad\textsc{RED1}
$$

The rule derives both the value function and its output domain.

## 17.3. Two independent refusal classes

A raw-well-typed reduction may fail certification because:

1. it spends an axis blocked by \(\beta(\kappa)\); or
2. it requests a coverage mode not admitted by \(\gamma(\kappa)\).

The first is a movement-and-identity failure. The second is a partial-observation-and-identity failure.

Both may leave a stable physical calculation available.

---

# 18. Physical semantics

## 18.1. Population-aware reducer execution

A physical reducer must process enough domain information to distinguish eligible-unobserved points from points that do not belong to the eligible fiber.

For each target fiber, it folds the extended state:

$$
(s,e,o)
\in
\widehat S_\kappa.
$$

A system may obtain the domain counts from:

- an explicit spine or population relation;
- source eligibility metadata;
- a generated scaffold;
- another physical representation certified to realize \(P\), \(E\), and \(S\).

The theorem assumes that the physical representation realizes those declared sets. It does not infer them from observed rows.

## 18.2. Domain-and-state-disciplined schedules

A physical schedule for a reducer may:

- factor \(q\) into admitted anchor maps;
- enumerate fibers in any order;
- partition work arbitrarily;
- combine intermediate states in any tree shape.

It is **domain-and-state disciplined** when every intermediate stage carries the full state:

$$
(s,e,o)
$$

and applies both:

- aggregate finalization \(\rho_\kappa\);
- coverage finalization \(\operatorname{Covered}_h\);

only at the final stage of that reducer.

Finalizing displayed values or dropping eligibility/observation counts at an intermediate stage is not an admitted schedule.

## 18.3. Canonical partial denotation

The canonical denotation of a plan contains:

- output universe \(U\);
- output anchor \(A\);
- population \(P_{U,A}\);
- eligibility \(E\);
- support \(S\);
- value function \(v:S\to|X|\).

For schedule \(\sigma\), write:

$$
\llbracket P\rrbracket^1_\sigma
=
(U,A,P,E,S,v).
$$

The contract fields \(\beta\) and \(\gamma\) are derived by certification, not by physical execution.

---

# 19. Theorem package

## 19.1. Domain-state staging

Let:

$$
A\xrightarrow{q}A'\xrightarrow{r}A''.
$$

For final target \(a''\in P_{U,A''}\), the final source fiber is partitioned by intermediate target points:

$$
\operatorname{Fib}_{r\circ q}(a'')\cap P_{U,A}
=
\biguplus_{a'\in\operatorname{Fib}_r(a'')\cap P_{U,A'}}
\left(
\operatorname{Fib}_q(a')\cap P_{U,A}
\right).
$$

**Theorem G1.1 (extended-state staging).** Folding \(\widehat\eta\) directly over the final fiber equals folding intermediate extended states and then combining them:

$$
\widehat\bigoplus_{a:(r\circ q)(a)=a''}
\widehat\eta(a)
=
\widehat\bigoplus_{a':r(a')=a''}
\left(
\widehat\bigoplus_{a:q(a)=a'}
\widehat\eta(a)
\right).
$$

**Proof.** The intermediate fibers form a disjoint partition of the final fiber. The result follows from associativity, commutativity, and identity of the extended state monoid from Lemma G1.L2. **QED.**

## 19.2. Coverage invariance

**Corollary G1.2.** For \(h\in\{\mathsf{Any},\mathsf{Complete}\}\), direct and staged execution derive the same:

- eligible count \(e\);
- observed count \(o\);
- output eligibility;
- output support decision.

**Proof.** Theorem G1.1 gives the same final \((e,o)\). Both coverage predicates are functions only of that pair. **QED.**

## 19.3. Partial certified determinacy

**Theorem G1.3 (partial certified determinacy).** If:

$$
\Gamma\vdash_1 P\Downarrow(v,C_1),
$$

then every domain-and-state-disciplined schedule \(\sigma\) yields the canonical denotation derived by the certification rules.

In particular, every admitted schedule agrees on:

$$
(U,A,P,E,S,v).
$$

**Proof.** By structural induction on \(P\).

- **Source.** The schedule returns the registered source denotation.
- **Strict map.** By the induction hypotheses, every input has the same universe, anchor, eligibility, support, and value function. Intersection and pointwise application therefore produce the same output.
- **Restriction.** Intersection with a fixed registered set \(R\) is schedule independent.
- **Carve.** The carved universe and its population family are canonical by Definition G1.D3 and Lemma G1.L1; value restriction is fixed.
- **Reduction.** Theorem G1.1 gives the same extended state under every admitted staging and enumeration. Corollary G1.2 gives the same output eligibility and support. Aggregate finalization gives the same value on that support.

**QED.**

## 19.4. Well-formedness preservation

**Theorem G1.4.** If the environment is consistent, source bindings are locally well formed, and:

$$
\Gamma\vdash_1 P\Downarrow(v,C_1),
$$

then:

$$
\Gamma\vdash_{\mathrm{wf1}}(v,C_1).
$$

**Proof.** By induction on the derivation.

- **Source:** premise.
- **Map:** intersections preserve \(S'\subseteq E'\subseteq P\); the pointwise function is typed; boundary unions and permission intersections remain total maps over finite registries.
- **Restriction:** intersections preserve containment.
- **Carve:** \(S\cap R\subseteq E\cap R\subseteq R=P_{U_R,A}\); Lemma G1.L1 supplies lawful coarser representations.
- **Reduction:** \(S'\subseteq E'\subseteq P_{U,A'}\) by construction; \(v'\) is defined exactly on \(S'\); inherited maps remain well formed.

**QED.**

## 19.5. Algebraic identity does not create observed support

**Theorem G1.5 (no automatic observed zero).** For either admitted coverage mode, if:

$$
o_q(a')=0,
$$

then:

$$
a'\notin S'_{q,h}.
$$

Therefore \(v'(a')\) is undefined, even if:

$$
\rho_\kappa(0_\kappa)
$$

is a numeric zero or another displayable identity.

**Proof.**

For \(\mathsf{Any}\), coverage requires \(o>0\).

For \(\mathsf{Complete}\), coverage requires \(e>0\) and \(o=e\). If \(o=0\), this would require \(e=0\), contradicting \(e>0\).

**QED.**

This theorem prevents the algebraic identity of an empty fold from being mistaken for an observed analytical value.

## 19.6. Restriction and carve are not equivalent

Let:

$$
R\subsetneq P_{U,A}
$$

be a proper nonempty subset.

Apply both operations to the same certified source.

**Theorem G1.6.** The restriction result and carve result may have identical current value functions on \(S\cap R\), but their contracts are not equivalent:

$$
C_{\mathrm{restrict}}
\not\equiv_{C_1}
C_{\mathrm{carve}}.
$$

**Proof.** Restriction retains universe identity \(U\), whose population at \(A\) is \(P_{U,A}\). Carve uses the distinct universe identity \(U\upharpoonright_{A,R}\), whose population at \(A\) is \(R\). Since \(R\subsetneq P_{U,A}\), the universe components differ. Strict contract equivalence therefore fails. **QED.**

The theorem formalizes the practical distinction between scoping a calculation and defining a new governed population.

## 19.7. Coverage refusal can coexist with deterministic value computation

Suppose a raw reduction requests mode:

$$
h\notin\gamma(\kappa).
$$

The host may still fold observed values and produce a deterministic number wherever the chosen physical policy allows it.

**Theorem G1.7.** No \(G_1\) certification derivation exists for that reducer under the inherited contract.

**Proof.** The only certification rule for partial reduction is \textsc{RED1}. Its coverage-permission side condition is false. **QED.**

This is a second inhabitant of the general separation between computation and governed identity, independent of axis-boundary failure.

## 19.8. Lifted central separation

**Theorem G1.8.** There exist a \(G_1\) environment and plan such that:

$$
\Gamma\vdash_{\mathrm{raw1}}P:X@(U,A'),
$$

all domain-and-state-disciplined schedules agree on the same partial denotation, but there is no certified output pair:

$$
\nexists\,(v,C_1)
\;\text{such that}\;
\Gamma\vdash_1P\Downarrow(v,C_1).
$$

**Proof by witness.** Use the inventory-over-time witness from \(G_0\). Place the source in an image-coherent universe whose source population, eligibility, and support are finite and equal on all represented source points. Permit \(\mathsf{Complete}\) coverage for sum. Choose an anchor map that spends the time axis while:

$$
\mathrm{time}\in\beta(\kappa_+).
$$

The raw plan and extended-state fold are deterministic. The boundary side condition of \textsc{RED1} fails. **QED.**

## 19.9. Agreement with \(G_0\) on populated fibers

A \(G_0\) reducer defines an aggregate value even on an empty fiber through the monoid identity. \(G_1\) deliberately does not treat that value as observed support.

**Proposition G1.P1.** On every target point whose source fiber contains at least one eligible observed point, a total \(G_1\) source using either coverage mode agrees in value with the corresponding \(G_0\) reducer under the same capability and anchor map.

On empty target fibers, \(G_0\) may return the algebraic identity while \(G_1\) returns no observed analytical value.

This is not a contradiction. It is the semantic refinement introduced by population and support.

## 19.10. Decidability and complexity

Assume:

- finite plan syntax;
- finite universe populations;
- registered subsets represented as bitsets over each finite population;
- finite capability and axis registries;
- constant-time registry lookup.

**Theorem G1.9.** \(G_1\) certification is decidable.

Let \(|\mathsf{Plan}|\) denote plan nodes, \(m\) the number of axes, and \(D\) the total number of population-point bit positions processed across domain-transforming nodes. With machine word size \(w\), certification requires:

$$
O\left(
|\mathsf{Plan}|\left\lceil\frac{m}{w}\right\rceil
+
\left\lceil\frac{D}{w}\right\rceil
\right)
$$

word operations, excluding evaluation of user functions and aggregate arithmetic.

**Proof.** The rules are syntax directed. Boundary and permission propagation use finite bitsets. Eligibility and support derivations use finite set intersection, image, and count operations. Every node is visited once. **QED.**

---

# Part V - Expansion, allocation, and fan-out

# 20. \(G_2\) objective, scope, and restrictions

A physical join establishes reachability. It does not determine whether a source value is replicated, assigned, allocated, reconciled, or left undefined. Nor does it determine whether unmatched source points may disappear or whether later aggregation preserves analytical identity.

\(G_2\) adds one structural constructor:

$$
\operatorname{expand}_{R,\delta}(P),
$$

where \(R\) is a finite declared source-target relation and \(\delta\) is a registered disposition. Expansion synthesizes a new contract on a relation-edge universe; it never inherits the source contract mechanically.

The fragment assumes finite relations, image-generated edge universes, exact registered weights, no target-spine completion, no data-dependent relation discovery, and no contextual or temporal relation qualification.

# 21. Capability extensions used by \(G_2\)

## 21.1 Duplication invariance

**Definition.** An aggregate capability \(\kappa\) is **duplication invariant** when its bag denotation satisfies:

$$
g_\kappa(M\uplus n\cdot\{\!\{x\}\!\})
=
g_\kappa(M\uplus\{\!\{x\}\!\})
$$

for every finite bag \(M\), value \(x\), and integer \(n\ge 1\).

Examples normally include set-like existence, minimum, and maximum under their domain policies. Sum, count, and ordinary mean are not duplication invariant.

The registry records a proved or adjudicated predicate:

$$
\operatorname{DupInv}(\kappa).
$$

**Design constraint.** Absence of a duplication-invariance declaration is treated conservatively as duplication sensitivity. Surface operator names cannot override the capability property.

### 21.1.1 Duplication invariance is not scalar re-aggregability

Duplication invariance concerns the aggregate capability's bag semantics and sufficient state. It does not imply that the finalized scalar output is additive or safely re-aggregable.

For exact distinct count, one possible sufficient-state carrier is:

$$
S_{\mathrm{dc}}
=
\mathcal P_{\mathrm{fin}}(X),
$$

with:

$$
S_1\oplus_{\mathrm{dc}}S_2
=
S_1\cup S_2,
\qquad
\rho_{\mathrm{dc}}(S)=|S|.
$$

Set union is duplication invariant. Repeating the same identity does not change the state. But finalized counts do not generally satisfy:

$$
|S_1\cup S_2|
=
|S_1|+|S_2|.
$$

Therefore replicated inputs may feed a duplication-invariant distinct-count capability only while the sufficient set-like state is retained. Summing finalized distinct-count scalars is a different, generally invalid operation.

The same distinction applies to mergeable sketches: sketch state may be composable and duplication tolerant under declared laws, while the finalized estimate is neither exact nor sufficient for later scalar rollup.

## 21.2 Additive scalable types

Allocation requires more than ordinary pointwise arithmetic.

**Definition.** A value type \(X\) is **nonnegative-rational scalable** when it carries:

- a commutative additive monoid:
  $$
  (|X|,+_X,0_X);
  $$
- scalar action:
  $$
  \odot:\mathbb Q_{\ge0}\times |X|\to |X|;
  $$
- laws:
  $$
  (r+s)\odot x
  =
  (r\odot x)+_X(s\odot x),
  $$
  $$
  r\odot(x+_X y)
  =
  (r\odot x)+_X(r\odot y),
  $$
  $$
  1\odot x=x,
  \qquad
  0\odot x=0_X.
  $$

The additive aggregate capability for \(X\) is written:

$$
\kappa_X^+.
$$

The exact laws are premises of the registered value and capability declaration.

---

# 22. Relation universes and edge anchors

## 22.1. Source-target relations

Let:

$$
\Gamma\vdash U@A\Downarrow P_{U,A}
$$

and:

$$
\Gamma\vdash V@B\Downarrow P_{V,B}.
$$

A registered relation is:

$$
R\subseteq P_{U,A}\times P_{V,B}.
$$

Write:

$$
\operatorname{dom}(R)
=
\{a\mid\exists b,\ (a,b)\in R\},
$$

$$
\operatorname{im}(R)
=
\{b\mid\exists a,\ (a,b)\in R\}.
$$

The source degree is:

$$
d_R(a)
=
\left|
\{b\mid(a,b)\in R\}
\right|.
$$

The target degree is:

$$
d_R^{\leftarrow}(b)
=
\left|
\{a\mid(a,b)\in R\}
\right|.
$$

## 22.2. Tagged edge anchor

Source and target axes are placed in disjoint namespaces.

Let:

$$
A\boxtimes B
$$

be the anchor over the tagged union:

$$
\mathsf{Axis}_S\uplus\mathsf{Axis}_T.
$$

A point of the full product anchor has form:

$$
(a,b).
$$

The relation population is not generally the full product. It is exactly:

$$
R.
$$

## 22.3. Relation-edge universe

**Definition.** The relation \(R\) generates an edge universe:

$$
J_R
=
\operatorname{Edge}(U,V,R).
$$

Its native population is:

$$
P_{J_R,A\boxtimes B}=R.
$$

It has canonical image representations at:

- the tagged source anchor:
  $$
  A\boxtimes\top_B;
  $$
- the tagged target anchor:
  $$
  \top_A\boxtimes B.
  $$

The populations are:

$$
P_{J_R,A\boxtimes\top_B}
=
\operatorname{dom}(R),
$$

and:

$$
P_{J_R,\top_A\boxtimes B}
=
\operatorname{im}(R).
$$

The canonical coarsenings are the edge projections:

$$
\pi_S(a,b)=a,
\qquad
\pi_T(a,b)=b.
$$

The target result of a transfer therefore describes the relation-induced population \(\operatorname{im}(R)\), not automatically the entire target universe \(V\).

## 22.4. Totality over eligible source points

A certified expansion must not silently discard an eligible source point.

**Definition.** Relation \(R\) is **eligible-total** for source eligibility \(E\) when:

$$
E\subseteq\operatorname{dom}(R).
$$

If this condition fails, the physical edge relation still exists, but a governed transfer requires one of:

- an explicit prior restriction;
- an explicit population carve;
- a later unmatched-source policy outside \(G_2\);
- refusal.

\(G_2\) chooses refusal unless the source contract has already been changed before expansion.

### 22.4.1. Governed matched-population pattern

An ordinary inner join often behaves as though it had silently replaced source eligibility \(E\) with the matched subset:

$$
M_R
=
E\cap\operatorname{dom}(R).
$$

\(G_2\) does not treat that replacement as automatic inheritance. A modeler may express the intended matched population explicitly:

$$
P_{\mathrm{match}}
=
\operatorname{carve}_{M_R}(P),
$$

and restrict the relation to:

$$
R_{M}
=
R\cap
\left(
M_R\times P_{V,B}
\right).
$$

The resulting plan is:

$$
\operatorname{expand}_{R_M,\delta}
\left(
\operatorname{carve}_{M_R}(P)
\right).
$$

Because every eligible point of the carved source lies in \(\operatorname{dom}(R_M)\), eligible-totality can now hold.

This is not a repair of the original population claim. It is a different certified result whose universe identifies the matched-source population. The unmatched-source refusal and the matched-population carve may expose the same physical inner-join rows, but they make different analytical claims.

## 22.5. Source-functionality

**Definition.** Relation \(R\) is **source-functional on \(E\)** when:

$$
\forall a\in E,
\qquad
d_R(a)=1.
$$

Many source points may still share one target. The requirement prohibits one source point from being sent to several targets under assignment.

---

# 23. Disposition capabilities

## 23.1. Replication

Replication copies the observed source value to every related edge.

For:

$$
(a,b)\in R,
$$

define:

$$
v_R^{\mathrm{rep}}(a,b)
=
v(a)
$$

whenever \(a\in S\).

The edge eligibility and support are:

$$
E_R
=
\{(a,b)\in R\mid a\in E\},
$$

$$
S_R
=
\{(a,b)\in R\mid a\in S\}.
$$

Replication makes no conservation claim.

## 23.2. Assignment

Assignment uses the same edge value rule:

$$
v_R^{\mathrm{asg}}(a,b)
=
v(a),
$$

but certification requires source-functionality on \(E\).

Each eligible source point therefore contributes to exactly one target edge.

Assignment may change population and grain, but it does not duplicate source contribution.

## 23.3. Weighted allocation

A registered allocation supplies:

$$
w:R\to\mathbb Q_{\ge0}.
$$

For every eligible source point:

$$
\sum_{b:(a,b)\in R}w(a,b)=1.
$$

The edge value is:

$$
v_R^{\mathrm{alloc}}(a,b)
=
w(a,b)\odot v(a)
$$

for \(a\in S\).

Allocation requires:

- eligible-total relation;
- nonnegative-rational scalable value type;
- exact registered weights;
- unit row sums over eligible source points.

The eligibility and support sets remain \(E_R\) and \(S_R\). Weight zero does not erase the existence of a governed relation edge unless the relation declaration itself omits that edge.

### 23.3.1. Exactness classes for physical allocation

The conservation theorem is stated over exact declared weights. This does not require an implementation to use symbolic fractions internally, but it does require the certified allocation to belong to an exact semantic class.

**Exact declared allocation.** The weights use a representation with decidable exact row sums, such as:

- rational numbers;
- exact decimal arithmetic;
- fixed-point integers with a shared denominator;
- another registered exact field.

Then:

$$
\sum_b w(a,b)=1
$$

is checked exactly.

**Residual-corrected exact allocation.** An engine may first calculate approximate candidate weights and then apply a declared residual rule to one or more designated edges. For a designated edge \(b^\ast\):

$$
w'(a,b^\ast)
=
1-
\sum_{b\neq b^\ast}w'(a,b).
$$

If the corrected weights are stored and checked in an exact representation, the ordinary \(G_2\) theorem applies. The residual policy is part of the allocation certificate because it changes individual target values.

**Approximate allocation.** If an implementation establishes only:

$$
\left|
1-\sum_b\widetilde w(a,b)
\right|
\le\epsilon_a,
$$

then the transformation is not an exact \(G_2\) allocation. It requires a later approximation contract recording the arithmetic representation, row-sum error, propagation rule, and downstream rights.

**Design constraint.** A binary floating-point result that happens to compare near `1.0` is not itself a conservation proof. Tolerance checks may diagnose physical implementation behavior, but they may not silently replace the exact semantic premise of Theorem G2.5.

## 23.4. Disposition registry

A disposition descriptor is one of:

$$
\delta
::=
\operatorname{rep}
\mid
\operatorname{asg}
\mid
\operatorname{alloc}(w,\kappa_X^+).
$$

A registered transfer descriptor is:

$$
\chi=(\operatorname{id}_R,U,A,V,B,R,\delta).
$$

For allocation, \(\chi\) also identifies the weight declaration and scalar-law declaration.

The declaration is a formal premise. \(G_2\) does not prove that a business relationship or allocation weight is externally appropriate.

---

# 24. Contract synthesis

## 24.1. Why expansion cannot use ordinary inheritance

Expansion changes:

- universe identity;
- anchor;
- population;
- multiplicity;
- eligibility and support;
- downstream aggregate rights.

The output contract is therefore synthesized.

Write:

$$
\operatorname{Synth}_\delta(C_1,R)
=
C_R^\delta.
$$

A failed inheritance check may not be repaired by copying the old contract label onto the expanded field.

## 24.2. Lifted source boundaries

Let:

$$
\iota_S:
\mathsf{Axis}_S\to
\mathsf{Axis}_S\uplus\mathsf{Axis}_T
$$

tag source axes.

For source boundary \(\beta\), define:

$$
\beta^{S}(\kappa)
=
\iota_S[\beta(\kappa)].
$$

These boundaries continue to govern movement across source-side distinctions after expansion.

Let:

$$
\mathsf{TgtAxes}(B)
$$

be the set of nonterminal tagged target axes represented by \(B\).

## 24.3. Replicate synthesis

For replication, define:

$$
D_{\mathrm{rep}}(\kappa)
=
\begin{cases}
\varnothing,
&
\operatorname{DupInv}(\kappa),
\\[4pt]
\mathsf{TgtAxes}(B),
&
\text{otherwise}.
\end{cases}
$$

Then:

$$
\beta_R^{\mathrm{rep}}(\kappa)
=
\beta^S(\kappa)
\cup
D_{\mathrm{rep}}(\kappa).
$$

The synthesized contract is:

$$
C_R^{\mathrm{rep}}
=
(
X,
J_R,
A\boxtimes B,
E_R,
S_R,
\beta_R^{\mathrm{rep}},
\gamma
).
$$

The target-axis boundary does not prohibit displaying replicated values or aggregating toward a specific target. It prohibits automatic inherited use of duplication-sensitive capabilities across target distinctions.

## 24.4. Assignment synthesis

For assignment:

$$
D_{\mathrm{asg}}(\kappa)=\varnothing,
$$

and:

$$
\beta_R^{\mathrm{asg}}(\kappa)
=
\beta^S(\kappa).
$$

The synthesized contract is:

$$
C_R^{\mathrm{asg}}
=
(
X,
J_R,
A\boxtimes B,
E_R,
S_R,
\beta_R^{\mathrm{asg}},
\gamma
).
$$

No target duplication boundary is added because every eligible source contributes to exactly one target.

## 24.5. Allocation synthesis

Allocation establishes conservation only for the registered additive capability \(\kappa_X^+\).

Define:

$$
D_{\mathrm{alloc}}(\kappa)
=
\begin{cases}
\varnothing,
&
\kappa=\kappa_X^+,
\\[4pt]
\mathsf{TgtAxes}(B),
&
\text{otherwise, unless another preservation theorem is registered}.
\end{cases}
$$

Then:

$$
\beta_R^{\mathrm{alloc}}(\kappa)
=
\beta^S(\kappa)
\cup
D_{\mathrm{alloc}}(\kappa).
$$

The synthesized contract is:

$$
C_R^{\mathrm{alloc}}
=
(
X,
J_R,
A\boxtimes B,
E_R,
S_R,
\beta_R^{\mathrm{alloc}},
\gamma
).
$$

Allocation does not grant unrestricted semantics for mean, maximum, count, or another capability merely because additive total is conserved.

## 24.6. Coverage permissions

Canonical \(G_2\) synthesis preserves only the `Any` and `Complete` coverage permissions already admitted by the source contract:

$$
\gamma_R=\gamma.
$$

It does not create a threshold, imputation, approximation, or event-to-zero policy.

Because `Any` and `Complete` depend only on whether observed edge counts are zero or equal to eligible edge counts, their truth is well defined on the relation universe. Weighted and threshold coverage require additional source-normalized state and remain outside this fragment.

---

# 25. Plan language and judgments

## 25.1. Syntax

The \(G_2\) grammar extends \(G_1\):

$$
P::=
P_{G_1}
\mid
\operatorname{expand}_{\chi}(P).
$$

Target transfer is derived syntax:

$$
\operatorname{xfer}_{\chi,\kappa}(P)
=
\operatorname{red}_{\kappa,\pi_T}
\bigl(
\operatorname{expand}_{\chi}(P)
\bigr).
$$

## 25.2. Raw expansion typing

Raw typing asks whether the physical edge values are defined for observed related source points.

If:

$$
\Gamma\vdash_{\mathrm{raw}}P:X@(U,A),
$$

and \(\chi\) is a registered relation descriptor typed for \(X\), then:

$$
\Gamma\vdash_{\mathrm{raw}}
\operatorname{expand}_{\chi}(P)
:
X@(J_R,A\boxtimes B).
$$

For allocation, raw typing also requires the declared scalar action.

Raw typing does not require:

- eligible-total relation;
- source-functionality;
- unit row sums;
- synthesized-boundary acceptance.

A raw edge result may therefore be computable even when governed certification fails.

## 25.3. Certification judgment

The imported certification judgment is:

$$
\Gamma\vdash P\Downarrow(v,C_1).
$$

Expansion rules derive both the edge value and synthesized contract.

## 25.4. Replication rule

$$
\frac{
\Gamma\vdash P\Downarrow(v,C_1)
\qquad
\chi=(R,\operatorname{rep})
\qquad
E\subseteq\operatorname{dom}(R)
}{
\Gamma\vdash
\operatorname{expand}_{\chi}(P)
\Downarrow
(v_R^{\mathrm{rep}},C_R^{\mathrm{rep}})
}
\quad\textsc{EXP-REP}
$$

## 25.5. Assignment rule

$$
\frac{
\Gamma\vdash P\Downarrow(v,C_1)
\qquad
\chi=(R,\operatorname{asg})
\qquad
E\subseteq\operatorname{dom}(R)
\qquad
\forall a\in E,\ d_R(a)=1
}{
\Gamma\vdash
\operatorname{expand}_{\chi}(P)
\Downarrow
(v_R^{\mathrm{asg}},C_R^{\mathrm{asg}})
}
\quad\textsc{EXP-ASG}
$$

## 25.6. Allocation rule

$$
\frac{
\begin{gathered}
\Gamma\vdash P\Downarrow(v,C_1),
\quad
\chi=(R,\operatorname{alloc}(w,\kappa_X^+))
\\
E\subseteq\operatorname{dom}(R),
\quad
\forall a\in E:\
\sum_{b:(a,b)\in R}w(a,b)=1
\end{gathered}
}{
\Gamma\vdash
\operatorname{expand}_{\chi}(P)
\Downarrow
(v_R^{\mathrm{alloc}},C_R^{\mathrm{alloc}})
}
\quad\textsc{EXP-ALLOC}
$$

The rule also requires the registered nonnegative-rational scalar laws for \(X\).

## 25.7. Reduction after expansion

Once expansion is certified, ordinary \(G_1\) reduction rules apply over the relation universe.

For target aggregation:

$$
\pi_T:
A\boxtimes B
\to
\top_A\boxtimes B.
$$

This spends source-side axes while retaining target distinctions.

A later rollup across target axes is checked against the synthesized target-axis boundaries. This is where fan-out refusal becomes an ordinary boundary refusal rather than a special-case join heuristic.

## 25.8. Explicit refusal classes

Certification can fail because:

1. an eligible source point has no related target;
2. assignment is not source-functional;
3. allocation weights are negative, missing, or do not sum to one;
4. the value type lacks the required scalar action;
5. source-side movement violates an inherited boundary;
6. replicated target-axis movement uses a duplication-sensitive capability;
7. allocation attempts an unproved nonadditive capability;
8. a required coverage mode is unavailable.

The physical relation or value may still exist in several of these cases.

---

# 26. Physical semantics

## 26.1. Edge enumeration

A physical expansion schedule may:

- partition \(R\);
- enumerate edges in any order;
- broadcast or shuffle source values;
- materialize or stream edge values;
- combine target groups in stages.

The relation and disposition declaration are fixed.

For replication and assignment, each edge value is a deterministic lookup of its source value.

For allocation, each edge value is a deterministic scalar action using the registered weight.

## 26.2. Domain-and-value state

For a target fiber over \(b\), the engine carries:

$$
(s,e,o)
\in
S_\kappa\times\mathbb N\times\mathbb N.
$$

Per eligible edge \((a,b)\):

- \(e\) receives one;
- \(o\) receives one exactly when \(a\in S\);
- \(s\) receives:
  - \(\eta_\kappa(v(a))\) for replication or assignment;
  - \(\eta_\kappa(w(a,b)\odot v(a))\) for allocation.

The product state combines componentwise.

## 26.3. Direct transfer semantics

For target point \(b\), define replicated target state:

$$
T_{\mathrm{rep}}(b)
=
\bigoplus_{a:(a,b)\in R,\ a\in S}
\eta_{\kappa_X^+}(v(a)).
$$

Assignment uses the same formula under source-functionality.

Allocation uses:

$$
T_{\mathrm{alloc}}(b)
=
\bigoplus_{a:(a,b)\in R,\ a\in S}
\eta_{\kappa_X^+}
\bigl(
w(a,b)\odot v(a)
\bigr).
$$

Coverage status is derived from eligible and observed edge counts under the imported \(G_1\) rule.

## 26.4. State-disciplined schedules

A schedule is \(G_2\)-disciplined when:

- every declared relation edge is processed exactly once;
- the declared disposition is applied exactly once per edge;
- allocation weights are not renormalized physically;
- aggregate sufficient state and domain state are retained until finalization;
- no target-spine rows are invented;
- no unmatched eligible source point is silently discarded in a certified plan.

---

# 27. Theorem package

## 27.1. Expansion determinacy

**Theorem G2.1.** If:

$$
\Gamma\vdash
\operatorname{expand}_{\chi}(P)
\Downarrow
(v_R,C_R),
$$

then every \(G_2\)-disciplined expansion schedule produces the same edge value function, eligibility set, and observed support.

**Proof.** The relation \(R\), source value function, disposition, and allocation weights are fixed finite declarations. Every edge is processed once. Replication and assignment use direct source lookup. Allocation uses a fixed scalar action and weight. Edge eligibility and support are set comprehensions over fixed \(E,S,R\). Enumeration and partitioning do not alter any result. **QED.**

## 27.2. Replication multiplicity law

Let \(\kappa\) be an additive-state capability and let:

$$
n\cdot s
$$

denote \(n\)-fold monoid addition of state \(s\).

**Theorem G2.2.** The total replicated state over observed edges is:

$$
\bigoplus_{(a,b)\in R,\ a\in S}
\eta_\kappa(v(a))
=
\bigoplus_{a\in S}
d_R(a)\cdot\eta_\kappa(v(a)).
$$

**Proof.** Regroup the finite edge sum by source point \(a\). The value contributed by \(a\) appears once for each related target, exactly \(d_R(a)\) times. Associativity and commutativity permit the regrouping. **QED.**

## 27.3. Structural conservation criterion

Let:

$$
F(S)=\mathbb N^{(S)}
$$

be the free commutative monoid over observed source identities, and assign source point \(a\) the basis token \(e_a\).

**Theorem G2.3.** In \(F(S)\):

$$
\sum_{(a,b)\in R,\ a\in S}e_a
=
\sum_{a\in S}e_a
$$

iff:

$$
d_R(a)=1
$$

for every \(a\in S\).

**Proof.** The coefficient of basis token \(e_a\) on the left is \(d_R(a)\); on the right it is one. Equality in the free commutative monoid is coefficientwise. **QED.**

**Interpretation.** Degree one is the exact structural condition for replication to conserve one copy of every observed source contribution. Numeric equality can occur under higher degree through zeros, cancellation in richer groups, or coincidental values. Such equality is data-dependent and does not establish a general conservation law.

## 27.4. Assignment conservation

**Theorem G2.4.** If \(R\) is source-functional on \(E\), then for the additive capability:

$$
\sum_{(a,b)\in R,\ a\in S}v(a)
=
\sum_{a\in S}v(a).
$$

Equivalently, summing assigned target contributions yields the observed source total.

**Proof.** Every observed source point belongs to \(E\) and has exactly one related target. The edge set partitions observed sources into singleton outgoing fibers. Regrouping by source contributes each value once. **QED.**

## 27.5. Allocation conservation

**Theorem G2.5.** Suppose \(X\) is nonnegative-rational scalable and:

$$
\forall a\in E,
\qquad
\sum_{b:(a,b)\in R}w(a,b)=1.
$$

Then:

$$
\sum_{(a,b)\in R,\ a\in S}
w(a,b)\odot v(a)
=
\sum_{a\in S}v(a).
$$

**Proof.** Regroup by source:

$$
\sum_{a\in S}
\left(
\sum_{b:(a,b)\in R}
w(a,b)\odot v(a)
\right).
$$

By scalar additivity this equals:

$$
\sum_{a\in S}
\left(
\left(
\sum_b w(a,b)
\right)
\odot v(a)
\right).
$$

Each row sum is one, and \(1\odot v(a)=v(a)\). **QED.**

## 27.6. Expansion and target reduction agreement

**Theorem G2.6.** For each disposition mode, direct target-state construction in Section 26.3 equals:

$$
\operatorname{red}_{\kappa,\pi_T}
\bigl(
\operatorname{expand}_{\chi}(P)
\bigr)
$$

under every state-disciplined schedule.

**Proof.** The target fiber of \(\pi_T\) over \(b\) is exactly:

$$
\{(a,b)\in R\}.
$$

Expansion supplies the declared edge value. The imported \(G_1\) staging theorem then makes fiber folding invariant to enumeration and intermediate partitioning. **QED.**

## 27.7. Support transport

**Theorem G2.7.** For target point \(b\), the eligible and observed edge counts are:

$$
e_b
=
\left|
\{a\in E\mid(a,b)\in R\}
\right|,
$$

$$
o_b
=
\left|
\{a\in S\mid(a,b)\in R\}
\right|.
$$

Therefore:

- `Any` holds exactly when \(o_b>0\);
- `Complete` holds exactly when \(e_b>0\) and \(o_b=e_b\).

These results are invariant under \(G_2\)-disciplined staging.

**Proof.** By the definitions of \(E_R,S_R\), followed by the \(G_1\) domain-state staging theorem. **QED.**

## 27.8. Fan-out boundary soundness

**Theorem G2.8.** Let \(\chi\) use replication, and let \(\kappa\) lack a duplication-invariance declaration. If a downstream reducer spends any tagged target axis, then no inherited certification derivation crosses that reducer.

**Proof.** Replicate synthesis places every tagged target axis in:

$$
\beta_R^{\mathrm{rep}}(\kappa).
$$

The ordinary reduction rule requires:

$$
\operatorname{Spent}(q)
\cap
\beta_R^{\mathrm{rep}}(\kappa)
=
\varnothing.
$$

Spending a tagged target axis makes the intersection nonempty. The only applicable reduction rule therefore fails. **QED.**

The theorem does not say that the physical aggregate is undefined. It says that duplication-sensitive target rollup cannot inherit the synthesized replicated contract.

## 27.9. Assignment and allocation remedies

**Theorem G2.9.** Suppose source-side boundaries permit the required additive reduction.

1. Under certified assignment, no target duplication boundary is added, so additive target rollup may certify.
2. Under certified unit-sum allocation, no target boundary is added for \(\kappa_X^+\), so additive target rollup may certify.
3. For another capability \(\kappa\), allocation remains blocked unless a separate preservation theorem is registered.

**Proof.** Immediate from the synthesis definitions and the ordinary boundary side condition. Conservation of additive state follows from Theorems G2.4 and G2.5. **QED.**

## 27.10. Deterministic but non-closing join witness

**Theorem G2.10.** There exist a certified source, relation \(R\), replication expansion, and downstream sum such that:

- raw execution is typed;
- every disciplined schedule returns the same number;
- the complete plan has no certification derivation.

**Proof by witness.**

Let two observed orders have amounts:

$$
v(o_1)=100,
\qquad
v(o_2)=50.
$$

Let relation \(R\) connect:

- \(o_1\) to two items;
- \(o_2\) to one item.

Replicated edge values are:

$$
100,\ 100,\ 50.
$$

Every disciplined sum returns:

$$
250.
$$

The source total is:

$$
150.
$$

Sum is duplication sensitive. Replicate synthesis therefore blocks target-axis additive rollup. The downstream global sum spends the target item axis, so the certification side condition fails. **QED.**

## 27.11. Unmatched-source separation

**Theorem G2.11.** A raw expansion may be deterministic while expansion certification fails because an eligible source point has degree zero.

**Proof.** Raw expansion computes values on existing relation edges. If:

$$
a\in E
\setminus
\operatorname{dom}(R),
$$

the edge function is still well defined on \(R\), but every certification rule requires eligible-totality. No expansion certification derivation exists. **QED.**

This refusal prevents a join from silently changing the claimed source population by dropping eligible points.

## 27.12. Well-formedness preservation

**Theorem G2.12.** If the input \(G_1\) contract is locally well formed and one of \textsc{EXP-REP}, \textsc{EXP-ASG}, or \textsc{EXP-ALLOC} succeeds, the synthesized output contract is locally well formed.

**Proof sketch.**

- \(J_R\) is a registered finite universe with population \(R\).
- \(E_R,S_R\) satisfy:
  $$
  S_R\subseteq E_R\subseteq R.
  $$
- the output value inhabits \(|X|\);
- every boundary mentions registered tagged axes;
- \(\gamma\) remains a valid finite permission map;
- allocation additionally uses a registered scalar action.

Therefore every local well-formedness clause holds. **QED.**

## 27.13. Decidability and complexity

**Theorem G2.13.** \(G_2\) certification is decidable.

Let:

- \(|P|\) be plan size;
- \(m\) be the number of tagged axes;
- \(|R|\) be the total size of relation declarations encountered;
- \(|W|\) be the total number of registered allocation weights encountered.

With hash-indexed relation endpoints and bitset boundaries, certification takes:

$$
O
\left(
|P|
\left\lceil\frac{m}{w}\right\rceil
+
|R|
+
|W|
\right)
$$

machine-word and registry operations, excluding physical evaluation of user functions and aggregate state.

**Proof.** Source, map, restriction, carve, and reduction remain syntax directed. Each expansion scans its finite relation to compute degrees and eligible-totality. Assignment checks degree one. Allocation scans weights and exact row sums. Boundary synthesis uses finite bitsets. **QED.**

---

# 28. Contract and certificate equivalence

## 28.1. Output-contract equivalence

Two synthesized \(G_2\) output contracts are equivalent under the imported \(G_1\) relation when they agree on:

- nominal type;
- universe identity;
- anchor;
- eligibility;
- support;
- boundary map;
- coverage permissions.

Write:

$$
C\equiv_{C_1}C'.
$$

Replication and assignment usually produce different boundary maps and are therefore not equivalent when a duplication-sensitive capability is relevant.

## 28.2. Certificate identity

A certification record retains:

- source certificate identity;
- relation identity and version;
- source and target universe identities;
- disposition mode;
- allocation-weight identity, when present;
- proofs or checks for eligible-totality;
- degree or row-sum obligations;
- synthesized contract;
- downstream reduction obligations.

Two derivations may synthesize equivalent output contracts while having different certificate identities.

For example, two distinct unit-sum allocations can produce the same kind of target quantity while using different weights.

## 28.3. Contract construction versus relabeling

A synthesized contract is produced by a registered rule whose premises are visible.

Binding an arbitrary replicated numeric field as though it were conserved allocation is not a derivation. It is an external adjudication and must carry a separate binding record.

---

# Part VI - Worked certificates

# 29. Inventory across time

## 29.1. Source setting

Consider two stores over three required observation days. The values are:

| Store | \(d_1\) | \(d_2\) | \(d_3\) |
|---|---:|---:|---:|
| A | 100 | 110 | 90 |
| B | 50 | 55 | unobserved |

For both stores, all three days are eligible. Store A has complete support; Store B has two observed points.

For additive state, the extended fiber states are:

| Store | Sum state \(s\) | Eligible \(e\) | Observed \(o\) |
|---|---:|---:|---:|
| A | 300 | 3 | 3 |
| B | 105 | 3 | 2 |

The source contract declares `InventoryQuantity` and blocks additive spending of the time axis.

## 29.2. Sum with `Any` coverage

The plan is raw typed. `Any` coverage gives support for both stores because each has at least one observation. Every disciplined execution returns:

- Store A: 300;
- Store B: 105.

The time axis is spent by sum and is in the inventory boundary:

$$
\operatorname{Spent}(q)\cap\beta(\kappa_+)\neq\varnothing.
$$

The result is deterministic and non-closing as `InventoryQuantity`.

## 29.3. Sum with `Complete` coverage

Complete coverage retains Store A and removes Store B from output support. It does not repair the value-identity boundary. Store A's value 300 remains a deterministic non-closing stock sum.

Coverage answers whether enough source observations exist for a stated mode. It does not decide whether the aggregate operation preserves the quantity's identity.

## 29.4. Last observed value

With a declared time order, a physical candidate returns:

- Store A: 90;
- Store B: 55.

The current integrated fragments do not certify this plan. \(G_0\) contains ordered total evaluators; \(G_1\) contains partial support and coverage but explicitly excludes ordered partial reducers.

The missing rule must specify:

- which partial points participate;
- whether the requirement is “last observed” or “observed at the exact boundary”;
- empty-fiber behavior;
- output support;
- execution evidence realizing the declared fiber order.

This is a rule gap, not a proof that the candidate value is wrong.

## 29.5. Exact quarter-end-day restriction

Let \(R\) select exactly the quarter-end day. Then:

$$
\operatorname{restrict}_R(P)
$$

certifies at the day anchor. Store A has observed value 90. Store B remains eligible but unobserved.

The carved variant:

$$
\operatorname{carve}_R(P)
$$

may expose the same values while claiming a new exact-day population. The two outputs are not contract-equivalent.

Collapsing the exact-day result to a coarser quarter anchor still needs either a singleton selector rule or the partial ordered-reducer extension.

## 29.6. Inventory exposure

An inventory-exposure quantity requires temporal structure. A candidate transformation may use intervals or duration weights to produce `InventoryUnitDays` or another integrated quantity.

Ordinary pointwise mapping is insufficient because the operation changes:

- quantity type;
- unit;
- temporal interpretation;
- boundary behavior;
- output identity.

The required rule is an explicit temporal contract synthesizer. A valid exposure result could be lawful while remaining unfaithful to an ask for end-of-period inventory.

## 29.7. Inventory certificate matrix

| Case | Raw value | Deterministic | Current certification | Principal reason |
|---|---:|---:|---:|---|
| Sum / `Any` | A 300; B 105 | Yes | No | Time boundary for inherited inventory identity |
| Sum / `Complete` | A 300; B absent | Yes | No | Coverage does not discharge the boundary |
| Last observed | A 90; B 55 | With declared order | Rule gap | Partial ordered reducer absent |
| Exact-day restriction | A 90; B unobserved | Yes | Yes at day anchor | No prohibited reduction |
| Inventory exposure | Transformer dependent | Potentially | Rule gap | Temporal synthesis absent |

# 30. Orders and order-items fan-out

## 30.1. Source setting

Let three observed orders have amounts:

$$
v(o_1)=100,
\qquad
v(o_2)=50,
\qquad
v(o_3)=80.
$$

The incomplete order-item relation contains:

$$
(o_1,i_{11}),
\quad
(o_1,i_{12}),
\quad
(o_2,i_{21}),
$$

and no edge for \(o_3\).

## 30.2. Ordinary inner-join replication

Physical replication produces edge values:

$$
100,\ 100,\ 50.
$$

The plan is deterministic. It does not certify against the original eligible order population because:

$$
o_3\in E
\setminus
\operatorname{dom}(R).
$$

The join has silently dropped an eligible source point.

## 30.3. Explicit matched-population replication

Define:

$$
M_R=\{o_1,o_2\},
$$

carve the source to that population, restrict the relation accordingly, and replicate.

Expansion now certifies on the relation-edge universe. The field may be displayed beside items. A global additive rollup remains blocked because replication synthesized an item-axis boundary for sum.

The physical sum is:

$$
100+100+50=250,
$$

while the matched-order source total is:

$$
100+50=150.
$$

The difference is structural fan-out, not execution instability.

## 30.4. Exact weighted allocation

Choose exact weights:

$$
w(o_1,i_{11})=\frac35,
\qquad
w(o_1,i_{12})=\frac25,
\qquad
w(o_2,i_{21})=1.
$$

The edge values are:

$$
60,\ 40,\ 50.
$$

Each matched source row has unit weight sum. The allocated total is:

$$
60+40+50=150.
$$

The additive target rollup certifies. No automatic right is granted for unrelated capabilities.

## 30.5. Source-functional assignment

Add one declared target for every order, including \(o_3\), with one outgoing edge per source. Assignment produces:

$$
100,\ 50,\ 80,
$$

and conserves the full source total:

$$
230.
$$

The theorem proves that each source contributes once. It does not prove that the selected “primary item” is externally meaningful.

## 30.6. Approximate allocation

Weights represented only approximately do not satisfy the exact \(G_2\) premise merely because their floating sum is near one.

Two lawful paths remain:

1. use a declared residual correction and store the corrected weights in an exact representation;
2. introduce an approximation contract carrying row-sum error, arithmetic representation, propagation rule, and downstream rights.

## 30.7. Distinct-count state

Exact distinct-count sufficient state may be a finite set with union. Repeated order identities do not change that state, so the capability can be duplication invariant.

Its finalized scalar is not additive. Two groups with counts two and two may have a union count anywhere from two to four. Certification must retain mergeable sufficient state rather than summing finalized counts.

## 30.8. Fan-out certificate matrix

| Case | Expansion | Additive target rollup | Population claim | Status |
|---|---:|---:|---|---|
| Ordinary inner replicate | Fails | Not reached | Original claim silently loses \(o_3\) | Non-closing |
| Matched-population replicate | Certifies | Blocked | Explicit matched orders | Mixed rights |
| Exact allocation | Certifies | Allowed for registered additive capability | Explicit matched orders | Certified |
| Source-functional assignment | Certifies | Allowed | Full source population | Certified |
| Approximate weights | Not exact \(G_2\) | Requires approximation rule | Explicit matched orders | Rule gap |
| Distinct-count state | Capability specific | Finalized scalars not additive | Explicit matched orders | State-dependent |

# Part VII - Limits, implementation, and release boundary

# 31. Limits exposed by the worked certificates

The certificate stress test found no contradiction in the \(G_0\)-\(G_2\) theorem chain. It exposed four operations that require later rules.

## 31.1 Partial ordered reducers

The ordered \(G_0\) extension assumes total atoms. \(G_1\) proves partial order-insensitive reduction. A combined rule must derive eligibility and support after ordered selection, specify empty-fiber behavior, and preserve the observation required by the resolved ask.

## 31.2 Singleton selection at a coarser anchor

Restricting to one declared date can produce a certified date-indexed stock atom. Removing the now-singleton time coordinate requires an explicit selector or an ordered rule. Cardinality one in current data is not, by itself, a general contract transformer.

## 31.3 Temporal integration

Stock-to-exposure transformation needs interval semantics, duration state, interpolation or carry rules, unit transformation, support and coverage rules, and a synthesized output identity. It must not be encoded as ordinary map inheritance.

## 31.4 Approximation

Approximate weights, sketches, sampling, and floating-point reassociation require explicit error semantics. The exact fragments are not weakened into tolerance-based contracts.

# 32. Trusted-kernel implementation consequence

A practical system can separate proposal from certification.

1. A human, compiler, semantic model, or language model proposes a plan.
2. The host engine supplies physical capabilities and a compiled realization.
3. A small kernel checks types, anchors, universes, domains, capabilities, boundaries, relations, dispositions, coverage, and exactness premises.
4. The kernel returns an output contract or a structured refusal.
5. Only certified rights propagate to later governed operations.

The planner may be heuristic or generative. The kernel remains syntax directed over finite declarations in the proved fragments.

Representative diagnostics include:

- `BOUNDARY.TIME.SUM.INVENTORY`;
- `G2.UNMATCHED_ELIGIBLE_SOURCE`;
- `G2.FANOUT.TARGET_AXIS.SUM`;
- `STATE_LOSS.DISTINCT_COUNT.FINALIZED_SCALAR`;
- `PARTIAL_ORDERED_REDUCER.NOT_MODELED`;
- `TEMPORAL_INTEGRATION.TRANSFORMER_REQUIRED`;
- `APPROXIMATION.CONTRACT_REQUIRED`.

# 33. Conclusion

The fragment chain establishes three progressively stronger conclusions.

\(G_0\): a typed and deterministic value need not close under an inherited analytical contract.

\(G_1\): a certified partial plan must determine the population, eligibility, and observed support on which its result exists.

\(G_2\): a governed join must determine not only reachability, but how source contributions move through the relation and which downstream operations remain licensed.

The common principle is:

> **A computation does not become a governed analytical object merely because a host engine can execute it.**

A reliable semantic layer therefore needs a certificate for both the value path and the contract path.


# References

Amsterdamer, Yael, Daniel Deutch, and Val Tannen. 2011. “Provenance for Aggregate Queries.” In *Proceedings of the 30th ACM SIGMOD-SIGACT-SIGART Symposium on Principles of Database Systems*, 153-164. <https://doi.org/10.1145/1989284.1989302>

Codd, E. F. 1970. “A Relational Model of Data for Large Shared Data Banks.” *Communications of the ACM* 13 (6): 377-387. <https://doi.org/10.1145/362384.362685>

Gray, Jim, Surajit Chaudhuri, Adam Bosworth, Andrew Layman, Don Reichart, Murali Venkatrao, Frank Pellow, and Hamid Pirahesh. 1997. “Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals.” *Data Mining and Knowledge Discovery* 1: 29-53. <https://doi.org/10.1023/A:1009726021843>

Green, Todd J., Grigoris Karvounarakis, and Val Tannen. 2007. “Provenance Semirings.” In *Proceedings of the 26th ACM SIGMOD-SIGACT-SIGART Symposium on Principles of Database Systems*, 31-40. <https://doi.org/10.1145/1265530.1265535>

Gyssens, Marc, and Laks V. S. Lakshmanan. 1997. “A Foundation for Multi-Dimensional Databases.” In *Proceedings of the 23rd International Conference on Very Large Data Bases*, 106-115.

Hurtado, Carlos A., Claudio Gutierrez, and Alberto O. Mendelzon. 2005. “Capturing Summarizability with Integrity Constraints in OLAP.” *ACM Transactions on Database Systems* 30 (3): 854-886. <https://doi.org/10.1145/1093382.1093388>

Kennedy, Andrew J. 1996. *Programming Languages and Dimensions*. University of Cambridge Computer Laboratory Technical Report UCAM-CL-TR-391. <https://doi.org/10.48456/tr-391>

Lenz, Hans-Joachim, and Arie Shoshani. 1997. “Summarizability in OLAP and Statistical Data Bases.” In *Proceedings of the Ninth International Conference on Scientific and Statistical Database Management*, 132-143. IEEE Computer Society. <https://doi.org/10.1109/SSDM.1997.621175>

Spivak, David I. 2012. “Functorial Data Migration.” *Information and Computation* 217: 31-51. <https://doi.org/10.1016/j.ic.2012.05.001>

Spivak, David I., and Ryan Wisnesky. 2015. “Relational Foundations for Functorial Data Migration.” In *Proceedings of the 15th Symposium on Database Programming Languages*, 21-28. ACM. <https://doi.org/10.1145/2815072.2815075>

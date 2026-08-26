---
title: "Certifiable State Under Information Loss"
subtitle: "Governed Derivability, Claim Transport, and Approximate Closure"
author: "Huayin Wang"
date: "Version 1.0 - 16 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "A formal account of certifiable analytical state under reduction, merge, compression, and approximation"
keywords:
  - certifiable state
  - Theory of Data
  - analytical governance
  - sufficient state
  - evidence
  - claim transport
  - weakest precondition
  - proof relevance
  - Theta sketch
  - approximation
  - provenance
  - informativeness
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
    \usepackage{fancyhdr}
  - |
    \usepackage{url}
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
    \fancyhead[L]{\small Certifiable State Under Information Loss}
    \fancyhead[R]{\small Huayin Wang}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \setlength{\headheight}{14pt}
  - |
    \urlstyle{same}
---

**datumwise, an independent open-source research project**

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

**DOI:** **10.5281/zenodo.21972541**

**Foundation.** This paper develops consequences of *The Theory of Data*, Version 6.0, DOI **10.5281/zenodo.21958062**, and *The Statistical Bridge*, Version 2.0, DOI **10.5281/zenodo.21966764**. It uses the current Theory-of-Data vocabulary in which a measure family is a governed analytical family and a measure is that family at one anchor, written $F@A$.

---

## Abstract

Data systems routinely transform state without preserving everything that made the state analytically trustworthy. A scalar may preserve a numerical answer while discarding the state needed to continue lawful aggregation. A sketch may preserve enough information to estimate a set cardinality while weakening the precision of later set-expression estimates. A recomputation may reproduce exactly the same values as a governed pipeline while lacking the evidence needed to certify what those values mean.

This paper develops a formal account of these differences. A **governed state** is represented as

$$
\mathbb K=(K,\Gamma,E),
$$

where $K$ is operational state, $\Gamma$ its governing contracts, and $E$ its evidence ledger. The central judgment is proof-relevant and graded:

$$
\mathbb K\Vdash_g c,
$$

meaning that an admissible certificate derivation establishes claim $c$ from $\mathbb K$ at evidence status at least $g$. This immediately separates extensional information from certifiability: two states can have identical $K$ and different certifiable futures.

For a deterministic partial governed transformation $T$, target claims pull back contravariantly:

$$
T^*c'
=
Def_T\wedge(c'\circ\Phi_T),
$$

and compose functorially. Certificate witnesses transport through a second map $T^\dagger$. Evidence-neutral forward transformations are deflationary in warrant: they may preserve or weaken evidence status but cannot manufacture stronger warrant. State composition and certificate composition therefore become distinct judgments; a physical operation can be executable while the corresponding analytical certificate must refuse.

Approximate state exposes a second distinction. Theta-style sketches support exact mechanical claims about sketch state together with statistical claims about the cardinalities represented by that state. Under the Theta-Sketch Framework's stated conditions, union, subpopulation, and intersection estimators remain within a common certificate-producing family with unbiasedness and comparative variance guarantees. Yet useful precision need not be uniformly preserved. A statistically warranted claim can remain valid while becoming weak. Thus:

$$
\boxed{
\text{information loss}
\neq
\text{evidential loss}
\neq
\text{loss of informativeness}.
}
$$

The result is a theory of **certifiable state under transformation**: what a state still entitles an analytical system to claim after reduction, merge, compression, or approximation.

---

## 1. Introduction

Consider two stored pairs:

$$
K_1=(s,n),
\qquad
K_2=(s,n).
$$

The first was recomputed by an untrusted process. The second was produced by a governed reduction that preserved the measure-family contract, the legal reduction path, and an evidence record of how the state was obtained.

Numerically, there is no difference. Both yield the same displayed mean:

$$
\bar x=\frac{s}{n}.
$$

Operationally, the pairs may also be interchangeable: any program that sees only the two numbers can perform the same arithmetic on each.

Analytically, however, they need not be interchangeable. The governed pair may certify that $s/n$ is the lawful reduction of a specified measure over a specified governed population. The untrusted pair may only reproduce the same number. The difference is not in the extension $K$. It is in what the state is entitled to support.

This motivates a question that is distinct from several familiar ones.

Information theory asks what information survives a transformation. Program semantics asks what computations or properties are preserved. Provenance asks how results depend on their inputs and derivations. Statistical sufficiency asks whether a statistic preserves information relevant to a parameter. Sketch theory asks what approximate queries a compact state can answer and with what error. Proof-carrying systems ask whether prescribed properties can travel with computed data.

The present question is narrower:

> **After state has been transformed, what analytical claims remain certifiable, at what evidence status, and with what remaining informativeness?**

The question matters because analytical systems increasingly work with derived state rather than raw records: sufficient-state vectors, materialized aggregates, model state, sketches, caches, distributed summaries, and approximate intermediates. These objects are useful precisely because they discard information. But information loss is not one-dimensional. A transformation may preserve an answer while destroying its warrant; preserve warrant while weakening the proposition being warranted; or preserve both.

This paper develops a small formalism for keeping those cases separate.

The starting object is a governed state:

$$
\boxed{
\mathbb K=(K,\Gamma,E)
}
$$

where:

- $K$ is the operational state extension;
- $\Gamma$ is the contract environment governing the state's identity, production, legal transformations, and approximation laws;
- $E$ is the evidence ledger recording what premises and checks support those contracts and transformations.

The primitive judgment is:

$$
\boxed{
\mathbb K\Vdash_g c,
}
$$

read: claim $c$ is certifiable from $\mathbb K$ at evidence status $g$.

The paper makes seven claims.

**R1 — Extensional separation.** Certifiability is not a function of state extension alone.

**R2 — Compositional claim transport.** A governed transformation induces a contravariant pullback on claims.

**R3 — Certificate conservation.** Evidence-neutral transformation may preserve or weaken warrant but cannot manufacture stronger warrant.

**R4 — Composition refusal.** State algebra can compose where certificate derivation must refuse because an external semantic premise is missing.

**R5 — Approximate two-layer state.** Approximate state may support exact mechanical claims and statistical approximation claims simultaneously.

**R6 — Theta certificate closure.** Theta-style union, subpopulation, and intersection operations remain within a common certifiable sketch family under the published framework's stated conditions.

**R7 — Informativeness non-closure.** Certificate closure does not imply uniform preservation of useful precision.

The contribution is not a claim to have invented proof relevance, predicate transformers, provenance, graded evidence, or sketch algebra. Those have mature prior literatures. The contribution is the conjunction: governed analytical state whose certifiable claims depend jointly on state, contract, and evidence history, and whose claim content and certificate witnesses are transported through transformations that may lose information.

The central finding can be stated compactly:

$$
\boxed{
\textbf{A transformation can preserve computation, warrant, and informativeness independently.}
}
$$

Here **independently** means that preservation of any one of the three does not, by itself, entail preservation of either of the others. It is a logical non-implication claim, not a probabilistic-independence claim.

---

## 2. Governed State and Certifiable Claims

### 2.1 Governed state

Let a governed state be:

$$
\mathbb K=(K,\Gamma,E).
$$

The three coordinates have different roles.

### Operational state $K$

$K$ is the state manipulated by execution: a scalar, a tuple such as `(sum, count)`, a vector of native sufficient state, a sketch, a materialized relation, or another finite operational object.

### Contract environment $\Gamma$

$\Gamma$ identifies what the state is and under what laws it was produced or may be transformed. Depending on the domain, it may contain:

- governed universe and anchor identity;
- measure-family identity;
- legal reducer/mapper contracts;
- participation and support rules;
- multiplicity or fan-out disposition;
- order law;
- state-combination law;
- approximation law;
- transformation preconditions.

$\Gamma$ is not commentary on $K$. It can change what operations are lawful even when $K$ is numerically unchanged.

### Evidence ledger $E$

$E$ records support for the premises used by $\Gamma$ and by certificate derivations. The governing corpus records epistemic statuses including verified, corroborated, assumed, unidentifiable, and contradicted. The paper does not assume these form a universal total order. Let:

$$
(\mathcal G,\preceq)
$$

be a typed preorder or partial order appropriate to the evidence calculus, where:

$$
g_1\preceq g_2
$$

means that $g_2$ is at least as strong as $g_1$ in the relevant fragment.

### 2.2 Why a claim is not graded by “the” support set

A tempting definition is to assign each claim one minimal evidence support and take the weakest grade among its items. This fails for two reasons.

First, a claim can have several incomparable minimal supports.

Second, and more decisively, inclusion-minimality and evidential strength can point in opposite directions. Suppose $e_1$ alone supports claim $c$, while $e_1$ and an independent $e_2$ jointly corroborate $c$ more strongly. Then $\{e_1\}$ is already inclusion-minimal, but restricting attention to minimal support would discard the stronger certificate.

The primitive must therefore be the derivation, not the support set.

Let:

$$
Der_{\mathbb K}(c)
$$

be the admissible certificate derivations of $c$ from $(\Gamma,E)$. A derivation $\delta$ records at least:

- the conclusion $c$;
- the evidence items it uses;
- the contract/rules invoked;
- its derivation structure;
- its attained grade $gr(\delta)$.

Define:

$$
\boxed{
\mathbb K\Vdash_g c
\iff
\exists\delta\in Der_{\mathbb K}(c):
gr(\delta)\succeq g.
}
$$

The certifiable family at grade $g$ is then:

$$
C_g(\mathbb K)
=
\{c:\mathbb K\Vdash_g c\}.
$$

If $\mathcal G$ is a chain, these sets form a filtration. In the general case they form an order-indexed decreasing family.

The evidence footprint of a derivation,

$$
Foot(\delta)\subseteq E,
$$

is useful metadata but not the semantic foundation. Minimal footprints can instead be asked relative to a particular claim and requested grade.

### 2.3 Proposition versus certificate witness

The judgment

$$
\mathbb K\Vdash_g c
$$

is existential. A concrete emitted certificate is proof-relevant:

$$
Cert=(c,\delta,gr(\delta)).
$$

A weaker emitted certificate is not silently upgraded merely because a stronger derivation exists somewhere in $Der_{\mathbb K}(c)$. The witness matters for audit, transport, and composition.

This makes the logic proof-relevant in a direct operational sense: certificates are not merely truth values attached to propositions; they are inspectable derivation objects.

---

## 3. Extensional Separation

### Proposition 1 — State extension underdetermines certifiability

There exist governed states

$$
\mathbb K_1=(K,\Gamma_1,E_1),
\qquad
\mathbb K_2=(K,\Gamma_2,E_2)
$$

with identical operational extension $K$ such that, for some claim $c$ and grade $g$,

$$
\mathbb K_2\Vdash_g c
$$

while:

$$
\mathbb K_1\not\Vdash_g c.
$$

Therefore $C_g(\mathbb K)$ is not determined by $K$ alone.

### Proof by exhibit

Take:

$$
K=(s,n).
$$

Let $\mathbb K_2$ be produced through a governed reduction whose contract identifies:

- the source analytical object;
- the governed population/universe;
- the reduction law;
- the retained sufficient state;
- the legal staging path.

Let $E_2$ contain admissible evidence supporting those premises.

Let $\mathbb K_1$ contain the same pair $(s,n)$, but produced by an untrusted recomputation with no admissible evidence that it is the lawful reduction of the intended analytical object.

The proposition

$$
c:
\text{“}s/n\text{ is the governed mean over the declared target.”}
$$

is derivable from $\mathbb K_2$ at whatever grade the premises support. It is not derivable from $\mathbb K_1$ merely because the numbers coincide.

Hence identical extension does not imply identical certifiable future. $\square$

### 3.1 What the proposition does and does not establish

The proposition is a necessity result. It says that extensional state content is insufficient for this governance problem.

It does **not** say that abstract interpretation, provenance, or another formalism is incapable of representing provenance or evidence. Any sufficiently enriched domain may carry such metadata. The point is narrower: if certifiability depends on production contracts and evidential history, then those coordinates are logically load-bearing.

The same separation can occur at the transformation level. Two transformations can expose identical values while differing in universe semantics or contract effects. In that case the physical value map is the same while the induced claim transport differs.

---

## 4. Claim Transport

A transformed state generally supports a different claim language from its source. Therefore certificate conservation cannot be expressed by literal set inclusion:

$$
C_g(\mathbb K')
\subseteq
C_g(\mathbb K).
$$

Claims must be transported.

### 4.1 Partial governed transformations

Let:

$$
T:\mathbb K\rightsquigarrow\mathbb K'
$$

be a deterministic governed transformation. The arrow is partial because physical execution and governed admission are distinct. A database may be able to compute bytes for a transformation while the governance layer refuses to certify the result.

Let:

$$
Def_T(\mathbb K)
$$

be the proposition that $T$ is admitted as a governed transformation on $\mathbb K$.

Let:

$$
\Phi_T(\mathbb K)
$$

be the governed target state when $Def_T$ holds.

For a target claim $c'$, define the claim pullback:

$$
\boxed{
T^*c'
=
Def_T\wedge(c'\circ\Phi_T).
}
$$

The pullback says two things:

1. the governed target is lawfully established;
2. the target proposition holds of that governed result.

This is weakest-precondition-shaped. The definedness conjunct is essential. Without it, one obtains a liberal form that says what would hold if the target existed; with it, the source must establish that the transformation is actually admitted.

### Proposition 2 — Contravariant composition

For deterministic governed transformations

$$
T_1:\mathbb K_0\rightsquigarrow\mathbb K_1,
\qquad
T_2:\mathbb K_1\rightsquigarrow\mathbb K_2,
$$

with composite definedness

$$
Def_{T_2\circ T_1}
=
Def_{T_1}
\wedge
(Def_{T_2}\circ\Phi_{T_1}),
$$

claim transport satisfies:

$$
\boxed{
(T_2\circ T_1)^*
=
T_1^*\circ T_2^*
}
$$

and:

$$
\boxed{
id^*=id.
}
$$

### Proof

For target claim $c$:

$$
\begin{aligned}
T_1^*(T_2^*c)
&=
Def_{T_1}
\wedge
\left[
Def_{T_2}\circ\Phi_{T_1}
\wedge
c\circ\Phi_{T_2}\circ\Phi_{T_1}
\right]\\
&=
Def_{T_2\circ T_1}
\wedge
c\circ\Phi_{T_2\circ T_1}\\
&=
(T_2\circ T_1)^*c.
\end{aligned}
$$

The identity law is immediate. $\square$

### 4.2 Finite symbolic transport

The semantic definition is not by itself a practical certificate calculus. A trusted checker needs finite syntax.

A registered primitive transformation should therefore expose a finite signature:

$$
\boxed{
Sig(T)
=
(\Phi_T,Prem_T,Trans_T,F_T).
}
$$

Here:

- $\Phi_T$ is the state/contract transformer;
- $Prem_T$ is the finite set of admissibility premises;
- $Trans_T$ rewrites supported target claims into source obligations;
- $F_T$ is the forward effect on evidence status.

The symbolic pullback has the form:

$$
\widehat T^*c'
=
Prem_T\wedge Trans_T(c').
$$

The important requirement is not that all primitive operators share one literal formula. Predicate-transformer calculi also require primitive rules. The requirement is that plan-level transport be **derived compositionally from registered primitive signatures**, rather than invented separately for each downstream query or optimization plan.

### 4.3 Existing exact instances

Several exact analytical transformations already have this form.

A staged reduction transports a coarse-grain closure claim to source premises about legal reducer composition, boundary preservation, and sufficient-state retention.

A reindexing transports target claims by coordinate substitution while preserving the declared governed contract.

A restriction and a carve may expose the same current values but differ in universe semantics, hence differ in $T^*$.

Support transport provides an especially literal example. If $A_{elig}$ is the eligible source carrier and $S\subseteq A_{elig}$ is the supported source set, define:

$$
e_b
=
|\{a\in A_{elig}:(a,b)\in R\}|,
\qquad
o_b
=
|\{a\in S:(a,b)\in R\}|.
$$

Then target support claims can pull back as:

$$
Any(b)\mapsto o_b>0,
$$

and:

$$
Complete(b)
\mapsto
e_b>0\wedge o_b=e_b.
$$

The target proposition is rewritten into a finite predicate over source eligibility, source support, and the mapping relation.

This is claim transport in operational form.

---

## 5. Certificate Witness Transport and Conservation

Claim transport acts on propositions. Proof relevance requires a second transport acting on certificate witnesses.

Let:

$$
T^\dagger
$$

denote backward decomposition/recovery of the source witness underlying an inherited target certificate.

Let:

$$
T_\#
$$

denote forward application of a source certificate through the transformation.

### 5.1 Forward grade effect

Let:

$$
F_T:\mathcal G\rightarrow\mathcal G
$$

be the registered forward grade transformer.

For an evidence-neutral transformation, the conservation law is:

$$
\boxed{
F_T(g)\preceq g.
}
$$

Transformation may preserve warrant or impose a ceiling. It may not, merely by processing existing state, create stronger evidential warrant.

If:

$$
\delta:
\mathbb K\Vdash_h T^*c',
$$

then forward certificate application produces:

$$
T_\#\delta
$$

with:

$$
gr(T_\#\delta)
=
F_T(h).
$$

### 5.2 Backward witness recovery

Suppose an inherited target certificate is witnessed by:

$$
\delta'
$$

at grade:

$$
gr(\delta')=g'.
$$

Then backward witness recovery must recover source support at least as strong:

$$
\boxed{
gr(T^\dagger\delta')
\succeq
gr(\delta').
}
$$

The two inequalities are the same conservation fact viewed from opposite directions.

Forward application is deflationary:

$$
gr(T_\#\delta)\preceq gr(\delta).
$$

Backward recovery identifies the stronger or equal source warrant required to have produced the attained target grade.

### 5.3 Registration admissibility

The backward-recovery inequality is not a theorem about arbitrary executable transformations. It is an **admissibility condition on evidence-neutral registration**.

A transformation is admitted to the conservation-valid fragment only if its registered witness transport $T^\dagger$ is checkable and satisfies the required recovery condition for the certificate classes it claims to preserve:

$$
gr(T^\dagger\delta')
\succeq
gr(\delta').
$$

Equivalently, the registration checker refuses a purported evidence-neutral transport whose witness map cannot recover source support at least as strong as the inherited target certificate. The normative force therefore lives in the registration rule, not in an assumption silently introduced inside Proposition 3.

With that classification, the next proposition is a **soundness theorem relative to valid registration**.

### Proposition 3 — Certificate conservation

For an evidence-neutral registered transformation $T$, if:

$$
\mathbb K'\Vdash_g c'
$$

through certificate structure inherited from $T$—that is, through a target witness in the image of the registered forward witness map $T_\#$—then:

$$
\boxed{
\mathbb K\Vdash_g T^*c'.
}
$$

### Proof sketch

Let $\delta'$ witness the target judgment at grade at least $g$. Apply $T^\dagger$. By backward witness recovery:

$$
gr(T^\dagger\delta')
\succeq
gr(\delta')
\succeq g.
$$

The recovered derivation establishes $T^*c'$ from the source. Therefore:

$$
\mathbb K\Vdash_g T^*c'.
$$

$\square$

### 5.4 Promotion requires evidence

The conservation proposition applies to evidence inherited through an evidence-neutral transformation.

A checking event is different. If a check adds a new evidence item:

$$
E'
=
E\cup\{e_{check}\},
$$

the target theory has new premises. A claim may legitimately acquire stronger support.

Thus the law has two parts:

$$
\boxed{
\begin{array}{ll}
\textbf{Conservation:}&
\text{evidence-neutral transformation does not manufacture warrant;}\\[2mm]
\textbf{Promotion:}&
\text{stronger warrant requires an evidence-producing event or rule.}
\end{array}}
$$

This is why a later check can promote a premise while mere recomputation cannot.


Premises relevant to transport come in at least two kinds.

A **schema-level premise** can be discharged from governed structure alone: for example, a declared disjointness or boundary condition may be decidable from universe and contract metadata.

A **data-dependent premise** requires inspecting or measuring the realized data. In the approximate case, an informativeness condition may depend on the realized size of a target subpopulation relative to the population from which the sketch's sampling scale was established. Establishing such a premise is therefore itself an evidence event. This connects informativeness transport back to the promotion law: a stronger precision claim can become available because a check supplies a new premise, not because the transformation manufactured warrant.

---

## 6. State Composition Is Not Certificate Composition

State algebra answers whether operational state can be combined. Certificate algebra asks whether the resulting analytical claim is warranted.

The two judgments are different.

### Example: overlapping sufficient states

Let:

$$
K_A=(s_A,n_A),
\qquad
K_B=(s_B,n_B).
$$

The state algebra can always form:

$$
K_A\oplus K_B
=
(s_A+s_B,n_A+n_B).
$$

Mechanically, the operation is exact.

Suppose, however, the intended target claim is:

$$
c_{A\cup B}:
\text{“the result is the mean over }U_A\cup U_B\text{.”}
$$

That claim generally requires a premise about how the source universes relate. Under a naïve additive merge, one sufficient premise is:

$$
U_A\cap U_B=\varnothing.
$$

If the universes overlap, another explicit overlap-disposition law is required.

A certificate rule therefore has a form such as:

$$
\frac{
Cert(A)
\qquad
Cert(B)
\qquad
Cert(Disjoint(U_A,U_B))
\qquad
Law_\oplus
}{
Cert(A\cup B)
}.
$$

If the disjointness or overlap premise is absent, the numeric merge still executes. The certificate derivation does not.

Hence:

$$
\boxed{
\text{state composability}
\not\Rightarrow
\text{certificate composability}.
}
$$

### Proposition 4 — Composition refusal

There exist governed states for which the operational merge is defined and exact while no certificate derivation exists for the intended merged analytical claim.

The preceding overlap construction is such an exhibit.

### 6.1 Refusal as underivability

Refusal is not an execution error.

It is:

$$
\boxed{
\mathbb K\not\Vdash_g c.
}
$$

The machine may have produced a state. The governance layer refuses to promote that state into the requested analytical claim because the total precondition is not derivable.

This gives precise content to closed-by-default serving: the absence of a certificate is not repaired by the presence of a value.

---

## 7. Approximate State Has Two Certificate Layers

Approximation does not make every property of a state approximate.

A sketch can have:

1. exact mechanical laws governing its internal state;
2. statistical claims connecting that state to an external cardinality.

Those are different propositions with different evidential bases.

### 7.1 HyperLogLog as the small example

A HyperLogLog sketch has an exact register-update and merge mechanism defined by the algorithm, together with an approximate cardinality finalizer (Flajolet et al. 2007).

Thus one may separately certify:

$$
c_{merge}:
\text{“the register state was combined according to the registered merge law,”}
$$

and:

$$
c_{card}:
\text{“the finalizer satisfies its declared approximation contract under the stated assumptions.”}
$$

The first is a mechanical/state-law claim.

The second is a statistical approximation claim.

The evidence status of one need not equal the evidence status of the other.

This yields:

$$
\boxed{
\text{approximate target}
\not\Rightarrow
\text{uniformly approximate certificate}.
}
$$

### 7.2 Approximation contracts are themselves claims

Suppose an algorithm's native approximation statement is an RSE claim. A downstream bounded-probability statement is not merely a cosmetic reformulation. It is another claim, derived through an additional probabilistic argument and its premises.

In the present formalism:

$$
c_{RSE}
\overset{\text{rule, premises}}{\Longrightarrow}
c_{\varepsilon,\delta}.
$$

The approximation contract therefore lives inside the same derivability calculus as other analytical claims.

---

## 8. Theta Sketches as the Nontrivial Test

HyperLogLog shows the two-layer distinction but offers a relatively narrow algebra. Theta sketches provide the harder test because they support set expressions.

The Theta-Sketch Framework of Dasgupta, Lang, Rhodes, and Thaler (2016) treats a sketch as a pair of a threshold and a retained sample, commonly represented schematically as:

$$
(\theta,S).
$$

The framework analyzes distributed stream-expression cardinalities and identifies conditions under which estimators are unbiased and have strong variance bounds.

The purpose here is not to rederive the Theta framework. It is to ask what its results mean inside certifiable state.

### 8.1 Mechanical layer

For a registered Theta-style transformation, finite state semantics determine:

- how thresholds are chosen or combined;
- which retained hashes belong to the resulting state;
- whether source configurations are compatible;
- which set-expression operation is being computed.

These are mechanically checkable state claims.

They belong to $Trans_T$ as exact propositions about the resulting sketch state.

### 8.2 Statistical layer

The statistical proposition is different. It concerns the cardinality represented by the sketch.

For a property $P$, the Theta framework studies estimators of the form:

$$
\widehat n_{P,A}
=
\frac{|P(S)|}{\theta}.
$$

The published ICDT 2016 paper makes the hypotheses precise. **Condition 6** defines 1-Goodness for threshold choosing functions. **Theorem 11** proves that `EstimateOnSubPopulation` is unbiased for a theta sketch produced by a threshold choosing function satisfying Condition 6. In the multi-stream setting, the union-preservation result immediately preceding Theorem 11 together with Theorem 11 yields unbiasedness for the corresponding union estimator when the constituent sampling schemes use 1-Good threshold choosing functions.

For variance, **Condition 12** defines monotonicity: when a stream is enlarged by concatenation, the threshold chosen by the threshold choosing function may not increase. **Theorem 13** assumes both Condition 6 (1-Goodness) and Condition 12 (monotonicity), and proves that the variance of the multi-stream union/subpopulation estimator is bounded above by the variance of the corresponding estimator obtained by running the same base sampler on the concatenated input stream.

These are statistical claims. Their validity depends on the estimator theory and its stated hypotheses, not merely on the correctness of the state-update code.

### Proposition 5 — Two-layer certification

A Theta-style governed sketch state may simultaneously certify:

- exact state-algebra propositions about $(\theta,S)$;
- statistical propositions about the estimator induced by that state.

The two proposition classes can have distinct evidence derivations and statuses.

---

## 9. Certificate Closure in the Theta Framework

The primary Theta framework provides the strongest formal basis for the closure claim.

### 9.1 Union and subpopulation estimates

For a collection of input streams, the framework constructs a union sketch and proves unbiasedness for property-defined subpopulation estimates under 1-Goodness.

This supplies a finite transformation signature:

$$
Sig(T_\cup)
=
(\Phi_\cup,Prem_\cup,Trans_\cup,F_\cup),
$$

where:

- $\Phi_\cup$ builds the union sketch state;
- $Prem_\cup$ contains the algorithmic and compatibility conditions;
- $Trans_\cup$ transports exact state claims and statistical estimator claims;
- $F_\cup$ records any effect on evidence status.

For a lawful operation, statistical precision may change as part of the proposition being transported even when evidence status does not.

### 9.2 Intersection as a property-restricted query

Section 3.7 of the published Theta framework handles intersection by defining the intersection sample under the union threshold and observing that the intersection estimator is exactly a property-restricted estimator on the union. The paper then states that, because that property-restricted union estimator was already shown to be unbiased with variance bounded as in Theorem 13, the intersection estimator satisfies the same properties.

Thus the inheritance is conditional in exactly the same way as the source results: unbiasedness rests on the framework's 1-Goodness requirements, while the comparative variance statement rests additionally on monotonicity.

That establishes an important form of closure:

$$
\boxed{
\text{the transformed state remains inside a family with certifiable estimator semantics.}
}
$$

This is stronger than state closure alone. The resulting state does not merely have the same datatype; it remains inside a theorem-bearing family.

### Proposition 6 — Theta certificate closure

Within the Theta framework's proved conditions, union/subpopulation/intersection transformations preserve membership in a certifiable sketch family: the resulting state has finite mechanical semantics; unbiasedness is inherited under the published 1-Goodness conditions; and the comparative variance guarantee is inherited when the additional published monotonicity condition holds.

### 9.3 What is not claimed

The claims discipline is simple: **implementation capability is not promoted into a statistical theorem.** An API may support an operation without the present paper claiming a quantitative guarantee for that operation until a primary theorem or an explicit derivation supplies it. For the present Theta claims, the primary anchors are Condition 6, Theorem 11, Condition 12, Theorem 13, and the intersection argument in §3.7 of Dasgupta et al. (2016).

This proposition does not claim:

- that every set-expression API operation has the same quantitative guarantee;
- that relative error is uniformly preserved;
- that implementation documentation is itself a theorem;
- that every confidence interval is equally useful.

**Set difference is deliberately outside the theorem family of this Version 1.0.** Implementations may support it, and the Theta paper discusses other set operations, but this paper does not assign difference the unbiasedness/variance result unless a primary theorem or an explicit derivation establishes the required conditions.

More general set expressions can be treated where the chosen primary theorem or a separate derivation supports them. The paper does not promote implementation capability into a statistical theorem without that step.

---

## 10. Certificate Closure Does Not Imply Informativeness Closure

The Theta result exposes a second axis.

A transformed sketch may remain inside a statistically valid estimator family while the resulting claim becomes weak for the intended purpose.

For example, estimating a small subpopulation from a sketch whose sampling scale is governed by a much larger union can yield a valid but high-variance estimate. The estimator may still be unbiased and its variance theorem may still apply. Yet the relative informativeness of the resulting claim can be poor.

This is not low evidence status.

It is weak claim content.

### 10.1 Warrant and informativeness are orthogonal

Let:

$$
g\in\mathcal G
$$

represent evidence status.

Let the proposition $c$ itself carry its quantitative content, for example:

$$
c:
n\in[L,U].
$$

Two claims can have the same evidence status while differing dramatically in usefulness:

$$
n\in[99,101]
$$

versus:

$$
n\in[0,10^9].
$$

Both may be correctly derived from the same estimator theory and equally well supported by the same evidence class.

Thus:

$$
\boxed{
\text{warrant strength}
\neq
\text{claim informativeness}.
}
$$

### 10.2 Approximation degradation belongs in claim transport

This clarifies the transformation signature:

$$
Sig(T)
=
(\Phi_T,Prem_T,Trans_T,F_T).
$$

$F_T$ acts on evidence status.

$Trans_T$ acts on proposition content.

For a lawful approximate transformation it is entirely possible that:

$$
F_T(g)=g
$$

while:

$$
Trans_T(c)
$$

is substantially weaker than $c$ in an entailment or precision order.

Approximation degradation therefore belongs primarily in the transported proposition, not automatically in the evidence grade.

### 10.3 Refusal versus vacuity

The distinction is now formal.

**Refusal:**

$$
\mathbb K\not\Vdash_g c.
$$

There is no admissible derivation of the requested claim.

**Vacuity or low informativeness:**

$$
\mathbb K\Vdash_g c,
$$

but $c$ is too weak for the intended decision.

A valid wide interval is the canonical example.

Hence:

$$
\boxed{
\text{uncertifiable}
\neq
\text{certifiable but uninformative}.
}
$$

A Theta corner state makes the distinction concrete. The sketch representation permits:

$$
\theta<1,
\qquad
retained=0,
\qquad
empty=false.
$$

Mechanically, `retained = 0` says that no qualifying hash values are currently retained. It does **not** certify that the represented set is empty; `empty = false` records exactly that distinction. The resulting state can therefore remain a valid estimator state with statistically defined bounds even though the available claim may be broad.

This is the estimator-state analogue of the analytical distinction between eligibility and observed support: **zero retained evidence is typed absence, not evidence of emptiness.**

### Proposition 7 — Informativeness non-closure

Certificate-producing approximate transformations need not preserve a uniform lower bound on claim informativeness, even when they preserve valid estimator semantics and evidence status.

The Theta intersection/subpopulation setting supplies the canonical example: theorem-bearing estimator semantics survive while relative usefulness may deteriorate for small target subpopulations.

---

## 11. Three Independent Losses

The preceding results separate three phenomena often collapsed under the single word “loss.”


The word *independently* in the paper's central claim can now be earned by direct exhibits. The table states pairwise non-implication rather than a claim that every Boolean combination is equally meaningful.

| Exhibit | Relevant computation preserved? | Warrant preserved? | Informativeness preserved? |
|---|---:|---:|---:|
| lawful exact reindexing | yes | yes | yes |
| untrusted recomputation of the same `(sum, count)` | yes | no | yes |
| governed finalization to an exact scalar | no for lawful continuation | yes | yes |
| small-subpopulation Theta estimate | yes | yes | potentially no |
| value-only transformation that strips contract/evidence | yes | no | yes — claim content unchanged |

These examples establish the non-implications needed by the central claim: computation does not entail warrant; warrant does not entail informativeness; and loss of future computational capacity does not by itself entail loss of warrant for the claim already established.

### 11.1 Information loss

A transformation may discard operational information.

Examples include:

- finalizing `(sum, count)` to a scalar mean;
- reducing a set to a sketch;
- materializing only an aggregate.

Information loss concerns what can still be reconstructed or computed from $K$.

### 11.2 Evidential loss

A transformation may preserve the same numerical state while losing the production contract or evidence needed to certify an analytical claim.

This is the separation result:

$$
K_1=K_2
$$

while:

$$
C_g(\mathbb K_1)\neq C_g(\mathbb K_2).
$$

Evidential loss concerns what remains warranted.

### 11.3 Informativeness loss

A transformation may preserve warrant while weakening the proposition.

A statistically valid sketch can still produce a broad interval or high-variance estimate.

Informativeness loss concerns what the warranted claim still says.

Therefore:

$$
\boxed{
\text{information loss}
\neq
\text{evidential loss}
\neq
\text{loss of informativeness}.
}
$$

This is the central conceptual result of the paper.

---

## 12. Relation to Existing Formalisms

The present construction is intentionally conservative about novelty. Its pieces have close predecessors.

### 12.1 Provenance semirings

Green, Karvounarakis, and Tannen's provenance-semiring framework (2007) annotates relational data with semiring values that track derivational dependence through query algebra. It is explicitly algebraic and compositional.

The present framework does not compete with provenance as a derivation-tracking formalism. Instead, provenance-like information can form part of $E$ or of a certificate witness.

The distinction is that derivational dependence alone does not determine whether an analytical proposition is warranted under a governed universe, measure-family contract, approximation law, or evidence status. Those additional premises belong to $\Gamma$ and $E$.

### 12.2 Proof-carrying code and proof-carrying data

Necula's proof-carrying code (1997) makes safety properties mechanically checkable before code is trusted. Chiesa and Tromer's proof-carrying data (2010) goes further: proofs attached to messages can certify that outputs and their computation history satisfy a system-designer-specified compliance predicate.

This is a close formal neighbor, especially for $T^\dagger$.

The distinction is not that proof-carrying data lacks domain-specific properties. It need not. The narrower distinction is that the present framework allows analytical premises whose warrant may be non-proof-grade—corroborated, assumed, or otherwise epistemically qualified—and separately tracks degradation in the content of approximate claims.

### 12.3 Justification logic

Justification logics make reasons explicit in formulas such as (Artemov 2008):

$$
t:F.
$$

That is structurally close to proof-relevant certificate derivations.

The present construction can therefore be read as a justification-logic-shaped layer over governed operational state. Its additional subject is what happens when the state carrying those justifications is reduced, compressed, merged, or made terminal.

### 12.4 Abstract interpretation

Abstract interpretation provides a mature theory of sound approximation and abstract semantic transformers (Cousot and Cousot 1977). The present paper does not claim abstract domains cannot be enriched with provenance or evidence.

The separation result says only that the extensional state $K$ is insufficient for certifiability. At the transport layer, abstract-interpretation-style soundness reappears structurally: target claims are justified by source obligations under a sound transformer.

### 12.5 Predicate transformers

Dijkstra's predicate-transformer work is a direct structural predecessor of (Dijkstra 1975; Dijkstra and Scholten 1982):

$$
T^*c'
=
Def_T\wedge(c'\circ\Phi_T).
$$

The contribution here lies not in contravariance itself but in what the precondition means: governed analytical lawfulness, not merely execution correctness, and in the proof-relevant/evidence-graded witness that must travel with it.

### 12.6 Statistical sufficiency

Classical sufficiency, from Fisher's early formulation (1922) through the measure-theoretic treatment of Halmos and Savage (1949), asks whether a statistic retains information relevant to a parameter. That concept is foundational and broader than the exact sufficient-state examples used here.

The present question differs: even if a state is statistically or algebraically sufficient for a computation, does it retain the contracts and evidence needed to certify the intended analytical claim?

The pair `(sum, count)` is sufficient to continue exact mean aggregation, but a bare pair without governed identity and production evidence may still fail the certification problem.

### 12.7 Sketch theory

The sketch literature supplies the approximate state algebra and estimator theory used here. The Theta-Sketch Framework (Dasgupta et al. 2016) already proves the key statistical properties of its estimator family.

The present contribution is not a new sketch. It is the surrounding certificate semantics: mechanical versus statistical claims, evidence status, claim transport, refusal, and the distinction between warrant preservation and informativeness preservation.

---

## 13. Operational Consequences

The formalism is useful only if it can constrain systems.

A practical observation motivates the object rather than merely following from it: systems that persist native sufficient state together with contract headers and evidence/lineage already store, in substance,

$$
\mathbb K=(K,\Gamma,E).
$$

The theory therefore does not require an exotic new storage object. It explains what an already natural governed-storage layout entitles the system to certify.


### 13.1 A complete operator signature

A governed operator should expose:

$$
Sig(T)
=
(\Phi_T,Prem_T,Trans_T,F_T).
$$

A value-only operator exposes only:

$$
\Phi_T.
$$

Such an operator may compute a result, but the system lacks enough registered semantics to derive downstream analytical certificates generically.

Governed family closure is therefore earned by the completeness of the operator signature, not by the existence of an executable function.

### 13.2 The certification/execution seam

Execution engines routinely rewrite plans.

A rewrite is analytically safe only if the claims and certificate witnesses can be transported across it.

Thus an engine-side rewrite should be accompanied, conceptually, by:

$$
T^*
$$

for claim transport and:

$$
T^\dagger
$$

for witness transport.

The execution layer may change physical realization. It may not silently change analytical identity or evidential entitlement.

### 13.3 Terminal values

A terminal scalar is not merely a value from which more arithmetic happens to be inconvenient.

It is a state whose contract/evidence structure no longer supports the derivations required for lawful continuation.

Once `(sum, count)` has been finalized to a scalar mean and the native state is discarded, later processing cannot recreate the original sufficient state or its certificate history by arithmetic alone.

Terminality is therefore certificate-theoretic as well as information-theoretic.

### 13.4 Approximate planning

Approximate state introduces a new planning objective.

Two algebraically equivalent set-expression plans can have different intermediate sample sizes, error trajectories, and final claim strength. Thus mathematically equivalent plans may preserve different amounts of **certifiable informativeness**.

This suggests a future planning criterion:

$$
\boxed{
\text{choose an equivalent plan that preserves the strongest certifiable future.}
}
$$

That criterion is deliberately left as an open systems problem. It may require an explicit informativeness floor in the ask contract or a richer identity rule for approximate results.

---

## 14. Scope and Non-Claims

This paper does not claim:

1. that every state object is a governed state;
2. that every provenance system is a certificate system;
3. that proof-carrying data cannot encode analytical predicates;
4. that abstract interpretation cannot carry provenance or evidence;
5. that all evidence statuses form one total lattice;
6. that statistical approximation automatically lowers evidence grade;
7. that every sketch operation preserves useful precision;
8. that certifiability is equivalent to mathematical proof.

The term **certificate** is used broadly for a warranted claim with an evidence status. A mechanically verified claim and a statistical approximation claim supported at whatever status its premises warrant may both be certificates while having different epistemic kinds.

The paper also does not attempt a universal epistemology of evidence. It assumes an external evidence calculus supplies admissible statuses and rule-specific ceilings. The contribution is to make those statuses travel with analytical state rather than disappear at transformation boundaries.

---

## 15. Open Problems

### 15.1 Evidence calculus

The present paper treats:

$$
(\mathcal G,\preceq)
$$

abstractly. A future account should formalize when evidence grades combine, when independent corroboration strengthens warrant, and how adverse statuses such as contradiction interact with derivability.

### 15.2 Approximate claim order

The paper distinguishes claim informativeness from evidence status but leaves the informativeness order mostly implicit.

For interval claims, one natural order is reverse set inclusion: narrower valid intervals are more informative. Other claim classes require other orders.

A general typed informativeness order would permit optimization over certificate quality.

### 15.3 Plan-dependence and identity

Exact governed analytics seeks plan-independent canonical identity. Approximate plans may yield the same estimand with different certified bounds.

Should approximate analytical identity include the transport trajectory? Or should the ask declare a minimum informativeness contract that every admissible plan must satisfy?

This is a systems-and-semantics problem rather than a sketch-estimation problem alone.

### 15.4 Mechanization

The finite signature suggests a small trusted checker.

For a registered transformation, the checker would verify:

- the premises in $Prem_T$;
- the syntax-directed claim transport;
- the witness transport;
- the grade effect;
- any approximation contract referenced by the resulting claim.

The exact boundary between a decidable mechanical kernel and external statistical evidence deserves separate treatment.

### 15.5 Beyond sketches

The same question arises for:

- approximate sufficient states used by iterative statistical algorithms;
- posterior sample states;
- model summaries;
- lossy materializations;
- streaming estimators.

The present paper restricts itself to exact sufficient-state examples and Theta-style sketches because they make the separation between state algebra, evidence, and claim strength unusually visible.

---

## 16. Conclusion

A data transformation does more than move values.

It changes what the system can still compute, what it can still certify, and how much the certified proposition still says.

Those three consequences should not be conflated.

The formal object developed here is:

$$
\mathbb K=(K,\Gamma,E),
$$

with graded proof-relevant derivability:

$$
\mathbb K\Vdash_g c.
$$

Its transformation semantics are governed by:

$$
T^*c'
=
Def_T\wedge(c'\circ\Phi_T)
$$

for claims and by $T^\dagger$ for certificate witnesses. Evidence-neutral forward transformation is deflationary in warrant. Missing semantic premises can therefore force refusal even when physical state composition succeeds.

Approximate state then reveals the final distinction. Theta-style sketches remain within a theorem-bearing estimator family under lawful set-expression transformations, but the informativeness of the resulting statistical claim need not be uniformly preserved. A certificate can survive compression while what it certifies becomes weak.

The resulting principle is:

$$
\boxed{
\textbf{A transformation can preserve computation, warrant, and informativeness independently.}
}
$$

That is the sense in which certifiable state survives information loss.

---

## References

1. Artemov, Sergei N. 2008. “The Logic of Justification.” *The Review of Symbolic Logic* 1(4): 477-513. DOI: 10.1017/S1755020308090060.

2. Cousot, Patrick, and Radhia Cousot. 1977. “Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints.” In *Conference Record of the Fourth ACM Symposium on Principles of Programming Languages (POPL)*, 238-252. DOI: 10.1145/512950.512973.

3. Dasgupta, Anirban, Kevin J. Lang, Lee Rhodes, and Justin Thaler. 2016. “A Framework for Estimating Stream Expression Cardinalities.” In *19th International Conference on Database Theory (ICDT 2016)*, LIPIcs 48, Article 6, 6:1-6:17. DOI: 10.4230/LIPIcs.ICDT.2016.6.

4. Dijkstra, Edsger W. 1975. “Guarded Commands, Nondeterminacy and Formal Derivation of Programs.” *Communications of the ACM* 18(8): 453-457. DOI: 10.1145/360933.360975.

5. Dijkstra, Edsger W., and C. S. Scholten. 1982. “Weakest Preconditions, Liberal and Not.” EWD816, April 1982, circulated privately. E. W. Dijkstra Archive, University of Texas at Austin. https://www.cs.utexas.edu/~EWD/ewd08xx/EWD816.PDF

6. Green, Todd J., Grigoris Karvounarakis, and Val Tannen. 2007. “Provenance Semirings.” In *Proceedings of the 26th ACM SIGMOD-SIGACT-SIGART Symposium on Principles of Database Systems (PODS)*, 31-40. DOI: 10.1145/1265530.1265535.

7. Necula, George C. 1997. “Proof-Carrying Code.” In *Proceedings of the 24th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL)*, 106-119. DOI: 10.1145/263699.263712.

8. Chiesa, Alessandro, and Eran Tromer. 2010. “Proof-Carrying Data and Hearsay Arguments from Signature Cards.” In *Innovations in Computer Science (ICS 2010)*, 310-331. Tsinghua University Press.

9. Flajolet, Philippe, Éric Fusy, Olivier Gandouet, and Frédéric Meunier. 2007. “HyperLogLog: The Analysis of a Near-Optimal Cardinality Estimation Algorithm.” In *AOFA 2007 - Analysis of Algorithms*, *Discrete Mathematics & Theoretical Computer Science Proceedings* AH, 127-146.

10. Fisher, Ronald A. 1922. “On the Mathematical Foundations of Theoretical Statistics.” *Philosophical Transactions of the Royal Society of London. Series A* 222(594-604): 309-368. DOI: 10.1098/rsta.1922.0009.

11. Halmos, Paul R., and Leonard J. Savage. 1949. “Application of the Radon-Nikodym Theorem to the Theory of Sufficient Statistics.” *The Annals of Mathematical Statistics* 20(2): 225-241. DOI: 10.1214/aoms/1177730032.

12. Wang, Huayin. 2026. *The Theory of Data*. Version 6.0. Zenodo. DOI: 10.5281/zenodo.21958062.

13. Wang, Huayin. 2026. *A Primer on the Theory of Data*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21959668.

14. Wang, Huayin. 2026. *The Theory of Data: An Introduction - Analytical Meaning, Lawful Transformation, and Governed Results*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21960639.

15. Wang, Huayin. 2026. *The Theory of Data Applied: Classical Analytical Failures as Problems of Identity, Geometry, State, and Law*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21959941.

16. Wang, Huayin. 2026. *Analytical Governance*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21959749.

17. Wang, Huayin. 2026. *The Statistical Bridge: From Events to Spines, Data Work, and the Interpretation of Results*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21966764.

---

## Publication note

**Version 1.0.** The argument, theorem scope, evidence-status language, Theory-of-Data v6 terminology, and primary Theta hypotheses have been reconciled for publication. Set difference is intentionally outside the theorem family in this version.

**DOI:** **10.5281/zenodo.21972541**

This DOI identifies the Version 1.0 publication of record.

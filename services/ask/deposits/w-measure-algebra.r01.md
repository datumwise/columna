---
title: "The Measure Algebra of the Theory of Data"
subtitle: "Formation, Sufficient State, and Lawful Transformation"
author: "Huayin Wang"
date: "Version 1.0 - 31 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "The operation layer over governed measures of the Theory of Data"
doi: "10.5281/zenodo.22219691"
version: "1.0"
license: "CC BY 4.0"
keywords:
  - Theory of Data
  - measure algebra
  - measure family
  - analytical identity
  - sufficient state
  - support
  - eligibility
  - population
  - governed transformation
---

**datumwise, an independent open-source research project**

**Version 1.0 - 31 August 2026**  
**DOI:** 10.5281/zenodo.22219691  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

> **Central claim.** The Theory of Data already contains the objects and laws needed for an operation layer over governed measures. A governed measure has a type, an analytical location, a population, eligibility and support, and a family law. Operations over measures are valid only when those objects and laws support the transformation. The formal fragments previously developed in the Contract Calculus make much of this algebra explicit; Theory of Data Version 6.1 supplies the current measure-family ontology in which to read them.

# Abstract

The Theory of Data treats a measure as a governed analytical object, not as a numeric column plus an aggregation function. In Version 6.1, a measure is a measure family at an anchor, written \(F@A\). Its values are typed datums; its universe, eligibility, and support determine where those values can exist; its state law determines what can survive reduction; and its family law determines when analytical identity is preserved or a new family must be established.

This paper reconstructs the finite Contract Calculus fragments \(G_0\), \(G_1\), and \(G_2\) as the operation layer over governed measures of the Version 6 ontology. The fragments already provide typed pointwise formation, state-disciplined reduction, restriction, population carve, and relation-based expansion with explicit disposition. Read together under Version 6, they form the proved finite core of the **Measure Algebra of the Theory of Data**.

Three consequences become especially clear in this reading. First, multi-measure operations must form the relationships they need at a common analytical location before reduction destroys those relationships. Second, value state and domain state have their own sufficiency boundaries: a materialization may preserve enough information for one future derivation and not another. Third, analytical identity is not determined by a displayed value, shared state carrier, or executable backend operation.

A recurring conservation rule follows:

> **An operation cannot use a relationship that was neither retained nor reconstructed from governed evidence.**

The paper does not claim a complete normal form for every Theory-of-Data transformation. It identifies a proved finite algebraic core, states where Version 6 broadens that core, and marks the extension boundaries that remain open.

# 1. Position: a layer of the Theory of Data

This is a layer paper, not a new foundation paper.

Theory of Data Version 6.1 supplies the governing ontology (Wang 2026a). A **measure family** \(F\) is a rooted analytical family with a governed identity and law. A **measure** is that family at an anchor:

\[
M = F@A.
\]

A universe \(U\) establishes which root points exist under its existence law. An **anchor** \(A\) is a governed partition of those already-established points; it organizes analytical location but does not by itself determine population or missingness. For a measure \(F@A\), eligibility and support then state where that measure applies and where a governed value is available. A **datum** is one governed typed value at one anchor point (Wang 2026a, §§2–3).

A measure therefore carries more structure than the familiar software picture:

```text
column
+ data type
+ aggregation function
```

The analytical object may also depend on:

- measure-family identity;
- universe and anchor;
- eligibility and observed support;
- sufficient state;
- movement and transformation law;
- lineage and, where required, construction evidence.

Several distinctions follow immediately:

\[
\text{displayed value}
\neq
\text{sufficient state}
\neq
\text{analytical identity}
\neq
\text{material realization}.
\]

The Measure Algebra asks a narrower question than the Theory of Data as a whole:

> Given governed measures and their laws, what operations can be formed, what information must survive those operations, and when may the result preserve or establish analytical identity?

The answer is partly formal already. The Contract Calculus developed finite fragments for total values, partiality and population, and relation-based expansion (Wang 2026b). Those fragments used an earlier Theory-of-Data vocabulary and deliberately did not claim to be the canonical ontology. The present paper retains their proved operations and results while reading them under the Version 6 family/measure distinction.

The paper therefore makes two claims and no larger one.

First, the proved fragments form a genuine algebraic core: they have typed carriers, operation constructors, side conditions, composition laws, and preservation theorems.

Second, Version 6 shows what those operations are operations **of**: governed measures \(F@A\), not physical columns and not the retired Version 5 notion of a measure with members.

The contribution of this paper is not the invention of the \(G_0\)–\(G_2\) operators. It is their reconstruction as the operation layer over governed measures of the Version 6 ontology. That reading makes three consequences explicit. Multi-measure work begins with lawful formation at a common analytical location. Information needed by a later operation must be formed before reduction or retained in sufficient state. And analytical identity remains separate from both shared state and physical realization. The paper uses those consequences to connect the earlier finite calculi to current typed and multi-measure analytical work.

Relative to the cited finite fragments, this paper derives three consequences from reading them under the Version 6 ontology. First, the Version 6 state-law taxonomy bounds where the commutative staging result may be used: \(G_0.2\) applies in the commutative-monoid region and does not travel merely because an operator has a familiar name (Wang 2026a, §4.7; Wang 2026b, Theorem G0.2). Second, marginal support state does not determine cross-measure overlap, which creates a concrete sufficiency boundary for materialized analytical state. Third, several analytical families may reuse one sufficient-state carrier without sharing family identity; this is the family-level reading of the broader result that identical retained state need not support identical certifiable claims (Wang 2026e, Proposition 1). These are consequences of the existing formal core under the current ontology, not claims of a separate theory.

# 2. The formal core already present

## 2.0 What the operations act on and return

The Contract Calculus already supplies the carrier of the operation grammar through its certification judgments. In the \(G_1\) fragment:

\[
\Gamma \vdash_1 P \Downarrow (v,C_1),
\]

where \(v\) is the resulting value function and:

\[
C_1=(X,U,A,E,S,\beta,\gamma),
\qquad
v:S\to |X|.
\]

The earlier \(G_0\) fragment uses the smaller contract \(C=(X,A,\beta)\); \(G_1\) is the fragment used here when universe, eligibility, support, and coverage matter (Wang 2026b, Definition G1.D5 and §17.2).

So the recursive grammar is closed over **certified analytical results**: a value function together with the contract that states its type, universe, anchor, eligibility, support, boundary information, and coverage permission.

Version 6 adds a separate identity question that the local contract does not answer by itself: which measure family, if any, does the certified result belong to?

- If an admitted operation preserves family \(F\), the certified result at anchor \(B\) is the measure \(F@B\).
- If a governed synthesis or graft establishes a new family \(G\), the certified result is \(G@B\).
- If neither preservation nor synthesis has been established, the calculus may still produce a certified local value-and-contract result, but it does not acquire a durable measure-family identity by arithmetic alone.

This is the carrier used throughout the paper. The operation grammar acts on certified analytical results; Version 6 determines how those results relate to measure identity.


The finite Contract Calculus fragments can be read as an operation grammar over already-governed measure inputs.

The smallest useful combined grammar is:

\[
P ::= x
\mid map_f(P_1,\ldots,P_n)
\mid restrict_R(P)
\mid carve_R(P)
\mid red_{\kappa,q,h}(P)
\mid expand_\chi(P).
\]

Here:

- \(x\) is an already-governed input;
- \(map_f\) applies a declared typed function pointwise to inputs at one common analytical location;
- \(restrict_R\) narrows applicability within the current population;
- \(carve_R\) creates a distinct governed population;
- \(red_{\kappa,q,h}\) reduces along an admitted anchor map using a declared state capability and coverage mode;
- \(expand_\chi\) moves a value through a declared relation under an explicit disposition: replication, assignment, or weighted allocation.

In \(red_{\kappa,q,h}\), \(\kappa\) names the aggregate capability, \(q\) the anchor map, and \(h\) the coverage mode used to decide whether a reduced target point is supported. The proved \(G_1\) fragment uses `Any` and `Complete`. The aggregate capability \(\kappa\) contains the aggregate finalizer \(\rho_\kappa\); the reduction parameter \(h\) is separate from that capability and induces the coverage finalizer \(Covered_h\). In a disciplined schedule, both aggregate and coverage finalization are delayed until the final stage of that reducer (Wang 2026b, §§15 and 17).

This is not claimed to be a complete normal form for every lawful analytical transformation. The original formal work explicitly left that theorem open. Ordered partial reducers, temporal integration, richer coverage, approximation, and other operations require additional fragments.

But the grammar is enough to answer the main criticism of treating “algebra” as a metaphor. These are actual constructors with typing rules and proved consequences.

Two existing certification rules make that claim concrete (Wang 2026b, §17.2).

For strict multi-input formation in \(G_1\), let:

\[
\Gamma \vdash_1
P_i
\Downarrow
\bigl(v_i,(X_i,U,A,E_i,S_i,\beta_i,\gamma_i)\bigr)
\quad\text{for every }i,
\]

and let:

\[
f:X_1\times\cdots\times X_n\rightarrow Y
\]

be declared. Define:

\[
E'=\bigcap_i E_i,
\qquad
S'=\bigcap_i S_i,
\]

\[
v'(a)=f(v_1(a),\ldots,v_n(a))
\quad(a\in S'),
\]

\[
\beta'(\kappa)=\bigcup_i\beta_i(\kappa),
\qquad
\gamma'(\kappa)=\bigcap_i\gamma_i(\kappa).
\]

Then the certified map rule is:

\[
\frac{
\Gamma \vdash_1 P_i \Downarrow
\bigl(v_i,(X_i,U,A,E_i,S_i,\beta_i,\gamma_i)\bigr)\;\forall i
\qquad
f:X_1\times\cdots\times X_n\rightarrow Y
}{
\Gamma \vdash_1
map_f^{\cap}(P_1,\ldots,P_n)
\Downarrow
\bigl(v',(Y,U,A,E',S',\beta',\gamma')\bigr)
}
\;\textsc{MAP1}
\]

For partial reduction, suppose:

\[
\Gamma \vdash_1
P
\Downarrow
(v,(X,U,A,E,S,\beta,\gamma)),
\]

capability \(\kappa\) accepts \(X\), and \(q:A\to A'\). Let:

\[
Spent(q)\cap\beta(\kappa)=\varnothing
\]

and:

\[
h\in\gamma(\kappa).
\]

With output eligibility \(E'=q[E]\), output support \(S'=S'_{q,h}\), and \(v'\) given by the partial reducer denotation, the rule is:

\[
\frac{
\Gamma \vdash_1 P \Downarrow (v,(X,U,A,E,S,\beta,\gamma))
\qquad
X=X_\kappa
\qquad
q:A\rightarrow A'
\qquad
Spent(q)\cap\beta(\kappa)=\varnothing
\qquad
h\in\gamma(\kappa)
}{
\Gamma \vdash_1
red_{\kappa,q,h}(P)
\Downarrow
(v',(Y_\kappa,U,A',E',S',\beta,\gamma))
}
\;\textsc{RED1}
\]

These rules show two different kinds of closure. `MAP1` forms a new certified value-and-contract result by combining co-located inputs under a declared function and conservative domain rules. `RED1` permits reduction only when both movement and coverage obligations are satisfied.


## 2.1 Typed pointwise formation

The strict map rule above is already \(n\)-ary. It does not create a product measure. The inputs remain distinct certified analytical results at the same universe and anchor; the declared function consumes their values pointwise.

The important result is the domain rule:

\[
E'=\bigcap_i E_i,
\qquad
S'=\bigcap_i S_i.
\]

This is one conservative, proved formation law. It is not a claim that every future multi-measure operation must use strict intersection participation. Other participation laws may be added explicitly. What is already fixed is that multi-input formation has an analytical domain rule; backend row alignment is not that rule.

## 2.2 Restriction and carve

Let \(R\) be a governed subset of the current population at anchor \(A\).

Restriction retains the universe and narrows eligibility and support:

\[
E' = E\cap R,
\qquad
S' = S\cap R.
\]

Carve instead creates a distinct universe whose population at \(A\) is \(R\).

The formal fragment defines a canonical carved universe:

\[
U\!\restriction_{A,R},
\]

with a new stable universe identity derived from the original universe, anchor, and carve set.

Theorem \(G_1.6\) proves that restriction and carve are not equivalent when \(R\) is a proper subset, even if they currently expose the same values.

This is an algebraic distinction, not a reporting preference. A restriction says:

> evaluate within this part of the original population.

A carve says:

> this subset is now the governed population of the result.

That distinction becomes critical whenever a later calculation uses population identity, denominators, coverage, or transport.

## 2.3 Reduction through sufficient state

For the order-insensitive \(G_0\) fragment, an aggregate capability \(\kappa\) has:

\[
(S_\kappa,\oplus_\kappa,0_\kappa,\eta_\kappa,\rho_\kappa),
\]

where:

- \(S_\kappa\) is the sufficient-state carrier;
- \(\eta_\kappa\) embeds one input value into state;
- \(\oplus_\kappa\) combines state;
- \(0_\kappa\) is the identity;
- \(\rho_\kappa\) finalizes state into the displayed output.

For an anchor map:

\[
q:A\rightarrow B,
\]

a reducer acts over the fibers of \(q\).

The state at target point \(b\) is:

\[
K_\kappa(b)
=
\bigoplus_{a\in Fib_q(b)} \eta_\kappa(v(a)).
\]

The displayed result is then:

\[
v'(b)=\rho_\kappa(K_\kappa(b)).
\]

Theorem \(G_0.2\) proves staged sufficient-state equality for commutative-monoid state. For:

\[
A\xrightarrow{q}A'\xrightarrow{r}A'',
\]

folding sufficient state first to \(A'\) and then to \(A''\) gives the same final state as folding directly along \(r\circ q\). Corollary \(G_0.3\) then states the displayed-value consequence: direct and staged aggregate values agree when intermediate stages retain sufficient state and apply \(\rho_\kappa\) only after the last combination (Wang 2026b, Theorem G0.2 and Corollary G0.3).

This is why a mean can compose through:

\[
(sum,count)
\]

while displayed subgroup means generally cannot be averaged again.

The central distinction is:

> **The state law governs continuation; the displayed value does not necessarily carry that law.**

## 2.4 Partial reduction carries domain state too

Once eligibility and support are explicit, value state alone is insufficient.

For the proved \(G_1\) coverage modes `Any` and `Complete`, the reducer carries:

\[
\widehat S_\kappa
=
S_\kappa\times\mathbb N\times\mathbb N.
\]

The added counts are:

- \(e\): eligible source points in the fiber;
- \(o\): observed supported source points in the fiber.

The combined state is:

\[
(s,e,o)\widehat\oplus
(s',e',o')
=
(s\oplus_\kappa s',e+e',o+o').
\]

Lemma \(G_1.L2\) establishes the commutative-monoid structure of the extended state, and Theorem \(G_1.1\) proves its staged-fold equality. Corollary \(G_1.2\) then shows, for `Any` and `Complete`, that direct and staged execution produce the same eligible count \(e\), observed count \(o\), output eligibility, and output-support decision (Wang 2026b, Lemma G1.L2, Theorem G1.1, Corollary G1.2).

So the algebraic object carried through a reduction can include both:

\[
\text{value state}
\quad\text{and}\quad
\text{domain state}.
\]

This matters because an exact numeric result can still have incomplete coverage. Approximation, coverage, and statistical inference are separate questions.

## 2.5 Expansion: structure before value reduction

The \(G_2\) fragment adds relation-based expansion:

\[
expand_\chi(P),
\]

where \(\chi\) identifies a declared source-target relation and a disposition.

The proved dispositions are:

- **replicate** — copy a source contribution to every related target;
- **assign** — send each eligible source contribution to exactly one target;
- **allocate** — distribute a source contribution across targets under declared unit-sum weights.

A target transfer is then derived as:

\[
xfer_{\chi,\kappa}(P)
=
red_{\kappa,\pi_T}(expand_\chi(P)).
\]

This equation captures an important separation:

\[
\boxed{\text{structural transformation} \;\text{then}\; \text{value reduction}}
\]

A physical join may execute both stages in one backend operation. The analytical laws remain different.

Replication is admitted on the relation edge by its own expansion rule, with multiplicity governed separately. Theorem \(G_2.8\) states the later refusal boundary: if \(\chi\) uses replication, \(\kappa\) lacks a duplication-invariance declaration, and a downstream reducer spends a tagged target axis, no inherited certification derivation crosses that reducer (Wang 2026b, EXP-REP; Theorems G2.2 and G2.8). Assignment and weighted allocation have different premises and conservation results.

Reachability therefore does not determine disposition.

# 3. Worked derivation: weighted mean

The first useful multi-measure operation is already ordinary map. A fully worked example shows what the algebra does without introducing a special statistical primitive.

Suppose two governed measures are established at line-item anchor \(L\):

\[
Price@L,
\qquad
Quantity@L.
\]

For two lines:

| line | price | quantity |
|---|---:|---:|
| A | 10 | 2 |
| B | 5 | 10 |

The requested quantity is the quantity-weighted mean price.

## 3.1 Formation at the input anchor

The numerator requires the declared pointwise function:

\[
f(p,q)=p\,q.
\]

The map is formed at \(L\):

\[
WeightedContribution@L
=
map_\times(Price@L,Quantity@L).
\]

The values are:

\[
20,\;50.
\]

The denominator uses Quantity itself at the same input anchor.

## 3.2 Reduction

Let:

\[
q:L\rightarrow B
\]

be the admitted movement to the requested output anchor \(B\).

The additive numerator state reduces to:

\[
20+50=70.
\]

The additive denominator state reduces to:

\[
2+10=12.
\]

At \(B\), a second declared map forms the ratio:

\[
g(n,d)=\frac{n}{d}.
\]

The strict map rule applies again at this stage: numerator and denominator must be jointly available under the declared domain rule at \(B\), and the map must be defined on the admitted denominator values. Under those conditions:

\[
WeightedMeanPrice@B
=
g(70,12)
=
5.83\ldots
\]

The ratio map establishes a certified value; it does not by itself mint a family identity. Whether `WeightedMeanPrice` receives durable family identity is a separate establishment question. Version 6.1 provides one explicit multi-parent precedent in Average Order Value, whose declaration records both Revenue and OrderCount parent family IDs and the ratio synthesis law; this paper does not generalize that case into a synthesis rule (Wang 2026a, §6.4).

## 3.3 The illegal reordering

Now reduce Price and Quantity separately before the pointwise product.

The plain average price is:

\[
\frac{10+5}{2}=7.50,
\]

and total quantity is:

\[
12.
\]

Those two reduced values do not determine the weighted numerator \(70\).

The information required by the map has been lost.

The failure is structural:

\[
\text{reduce first}
\not\Rightarrow
\text{form later}.
\]

This is the two-anchor result in algebraic form. The input anchor can be a typing and co-location requirement of the operation that constructs sufficient state (Wang 2026c).

The general conservation rule is:

> **An operation cannot use a relationship that was neither retained nor reconstructed from governed evidence.**

# 4. What Version 6 adds to the reading

The Contract Calculus fragments were developed under an earlier vocabulary. The mathematics is still useful, but the ontology should be read through Theory of Data Version 6.1.

Version 6 retires `member` from the core ontology (Wang 2026a, §1.2). What Version 5 called a measure is now a **measure family**; what Version 5 called a **member of a measure** is now a **measure**:

\[
\text{measure}=\text{measure family}@\text{anchor}=F@A.
\]

This changes how the calculus should be interpreted.

A source term in the finite algebra is not a physical column and need not be promoted into a new product object merely because an operator takes several inputs. The inputs are governed measures that are established at the locations required by the operation.

Likewise, a successful transformation does not automatically mean “same measure with a different value.” Version 6 distinguishes:

- transformations that preserve one measure-family identity;
- transformations that establish a new measure family through a governed establishing construction.

The old contract rules formalize part of this preservation problem. The v6 family model gives it a stable analytical identity.

## 4.1 The current state-law taxonomy is broader than \(G_0\)

The proved \(G_0\) reducer theorem uses commutative-monoid state because that is the smallest fragment in which arbitrary regrouping and enumeration independence can be proved cleanly.

Theory of Data Version 6.1 states a broader state-law taxonomy (Wang 2026a, §4.7):

| State-law class | What composition permits |
|---|---|
| commutative monoid | regrouping and ordering of the same governed contributions preserve state |
| associative, noncommutative | regrouping is safe while logical order must be preserved |
| ordered/stateful composition | continuation requires an explicit sequence, order key, context, or composition contract |
| no declared compositional state | arbitrary staged reduction is unavailable from summarized state; retained roots or richer state are required |

The algebraic consequence is direct.

Theorems such as \(G_0.2\) apply to the commutative-monoid region. They should not be generalized by operator name to the other regions.

For an associative but noncommutative law, factorization may remain valid while permutation does not.

For ordered/stateful composition, the order itself is an input to the law.

Where no compositional state has been declared, a summarized result cannot be used as though one existed.

Thus:

> **The declared state law determines the admissible composition. Current implementation behavior does not define the state law.**

# 5. Population and support are part of formation

The same rule applies to analytical domain, not only to values.

For a measure \(F@A\) in universe \(U\), let:

\[
S_F\subseteq E_F\subseteq P_{U,A},
\]

where:

- \(P_{U,A}\) is the represented population;
- \(E_F\) is the eligible set;
- \(S_F\) is observed support.

Suppose Revenue and Headcount are both eligible for 50 stores. Revenue is observed at 47; Headcount is observed at all 50.

Then:

\[
|E_R|=|E_H|=50,
\qquad
|S_R|=47,
\qquad
|S_H|=50.
\]

Under the proved strict map rule:

\[
E' = E_R\cap E_H,
\qquad
|E'|=50,
\]

while:

\[
S' = S_R\cap S_H,
\qquad
|S'|=47.
\]

The certified result remains over the 50-point governed population, with 47 supported values; whether it preserves or establishes a durable measure-family identity is a separate question. The other three points are not silently removed from the analytical domain.

A lawful joint frame is built from eligibility rather than by intersecting observed rows (Wang 2026d, §§8.1 and 11.4). A physical inner join that returns only the 47 observed pairs can realize those supported values. It cannot, by itself, decide that the population has become 47.

If an analysis instead intends the 47 supported stores to be the population of a new result, the restriction/carve distinction applies: for a proper nonempty subset, Theorem \(G_1.6\) shows that restriction and carve are contractually different even though their current value functions **may** agree on the exposed subset (Wang 2026b, §19.6). A carve therefore needs a distinct population identity.

## 5.1 Same coordinate does not mean same support

Two measures can both have a value at the same output coordinate while depending on different source support sets. Coordinate agreement therefore does not establish common observational support, and equal marginal support counts do not establish support identity.

The stronger materialization result follows next.

## 5.2 Support state has its own sufficiency boundary

The domain state retained by a reduction can be sufficient for one later operation and insufficient for another.

Marginal support cardinalities do not determine cross-measure overlap. For example,

\[
S_F=\{1,2,3\},
\]

and either

\[
S_G=\{1,2,3\}
\]

or

\[
S_G'=\{1,2,4\}
\]

give the same marginal support counts:

\[
|S_F|=|S_G|=|S_G'|=3,
\]

while the intersections differ:

\[
|S_F\cap S_G|=3,
\qquad
|S_F\cap S_G'|=2.
\]

Therefore the marginal \((e,o)\) state that is sufficient for some coverage claims is not sufficient to reconstruct every later joint-participation claim.

The material consequence is direct:

> **What domain state must survive a materialization is determined by the later operations that materialization claims to support.**

No universal bitmap requirement follows. If participation is decided before reduction, the resulting certified object may no longer need the original support identities for that purpose. If participation is deferred, more support evidence may have to survive. A materialization can therefore retain enough state for lawful continuation along one path while being insufficient for another.


Local compositionality does not require a materialization to anticipate every future query. A materialization can support a later derivation only if the information required by that derivation remains in retained state or can be re-established from another governed source. Retained-state composability is necessary but not sufficient: identity, contracts, certification, and current evidence may still block the derivation (Wang 2026e; Wang 2026b, Theorem G1.7).

If a later request needs a relationship that the materialization no longer carries, a planner may use another admitted representation or retained root from which that relationship can be re-established. If no such route exists, the requested result is **not derivable from the available state**.

The algebra therefore requires neither a universal raw-data fallback nor a special null value for lost derivability. Choosing another realization path is an execution decision. The algebraic fact is simply whether the required relationship survives in state or can be established again under governed evidence.

> **A materialization is not required to preserve every future possibility. It must make clear what information it retains and therefore which derivations remain possible subject to the governing contracts, identity, and evidence.**

# 6. Participation is not a join default

The finite \(G_1\) fragment gives one explicit multi-input formation rule: strict intersection of eligibility and support (Wang 2026b, MAP1). It also gives two coverage modes for reduction, `Any` and `Complete`.

That is enough to make one point precise without pretending to have a complete participation calculus:

> **Participation is part of the analytical operation and must be declared or derived under law. It is not selected by backend join behavior.**

A future correlation operator may require complete joint support. Another operation may admit a different rule. Pairwise covariance, for example, would form different support per matrix entry and therefore does not automatically have the same analytical type as covariance over one common participating population.

Until such a formation and participation law is declared, `corr` is **not** an operator of the proved Measure Algebra. It is a candidate extension whose numerical implementation would not be enough to admit it.

Those extensions should be stated when their laws are known. The existing algebra does not need invented participation constructors merely to acknowledge that the choice is identity-bearing.

Where a result is formed by carving observed support into a new population, the carve must remain explicit. Where the original population remains and some points are unsupported, the result must remain partial rather than silently becoming a smaller population.

# 7. Family preservation and family establishment

The algebra distinguishes an operation that preserves a measure family from one that establishes a new family. That distinction is determined **ex ante** by governed family identity; agreement among computed outputs cannot create identity after the fact (Wang 2026a, §§4.2 and 6.7).

The simplest preservation example is additive Revenue under a family law that licenses reduction from a finer anchor \(A\) to a coarser anchor \(B\):

\[
Revenue@A
\xrightarrow{\;red\;}
Revenue@B.
\]

The displayed values change location. The family identity does not.

The Contract Calculus expresses the same constraint through inherited-contract side conditions: a capability may spend only those analytical distinctions the contract permits. Theorem \(G_0.7\) gives the canonical witness. Summing Inventory across a blocked time axis can be typed, executable, and deterministic while still failing to inherit Inventory identity (Wang 2026b, Theorem G0.7). Deterministic computation therefore does not by itself preserve analytical identity.

Version 6.1 uses **graft** for the family-boundary event that establishes the root of a new family from an existing governed analytical object. It develops the single-source case and one explicit multi-parent example; it explicitly leaves a general algebra of multi-input family synthesis outside scope (Wang 2026a, §6.4).

That explicit multi-parent example is Average Order Value:

\[
AverageOrderValue@A
=
\frac{Revenue@A}{OrderCount@A}.
\]

A conforming `average_order_value` declaration records both parent family IDs and the ratio synthesis law in its semantic signature. More generally, Version 6 writes family identity as:

\[
\Sigma(F)
=
\operatorname{canon}
\bigl(
U_F,\,
R_F,\,
Parents(F),\,
Establish(F),\,
Law(F),\,
Contracts_{id}(F)
\bigr).
\]

The AOV case therefore demonstrates the point needed here: a multi-input value computation does not mint durable family identity by arithmetic alone. A governed declaration must establish the new family, and its semantic signature includes the constitutive parents, establishing construction, continuation law, and identity-bearing contracts. The present paper does not generalize that one explicit multi-parent case into a synthesis calculus.

# 8. Architectural boundaries and realization

The formal core is intentionally about analytical law. Several nearby distinctions matter because a software system must realize that law without becoming its source.

## 8.1 Rich values and shared state

Internal value structure is not analytical location. A measure may carry a matrix, vector, set, sketch, or another composite value. Internal axes or coordinates belong to the value type; they do not become anchor levels of the containing measure.

Shared sufficient state also does not merge identity. A retained moment state such as

\[
N,\qquad \sum x,\qquad \sum xx^\top
\]

may support several later finalizations under declared laws. Reuse of one state carrier does not make the resulting analytical families identical.

Rich values can require more than shape checks. Calling a numeric matrix `CovarianceMatrix<Variables,Population>` makes a construction claim about its inputs and population. Two numerically equal matrices may therefore have different analytical status. The exact certificate format belongs to the neighboring Certifiable State problem (Wang 2026e).

## 8.2 Analytical law and implementation capability

The algebra states what a transformation means and under what law it composes. A software build separately states what it can execute today.

\[
\boxed{
\text{analytical impossibility}
\neq
\text{implementation absence}
}
\]

and:

\[
\boxed{
\text{implemented}
\not\Rightarrow
\text{lawful for every analytical use}
}.
\]

A build may lack a decomposition that the analytical state law permits. Conversely, a backend may execute a terminal calculation for which no reusable compositional state has been declared. Runtime dispatch categories therefore cannot define the Theory's state-law classes.

## 8.3 Declaration, certification, and use

A governed implementation has at least three distinct stages:

1. **Declaration** states analytical law and candidate capabilities.
2. **Certification and current admission** establish which declared capabilities hold for a particular realization and current data state.
3. **Ask time** resolves a request against the declared and currently admitted law.

The planner applies declared law. It does not infer missing law from coincidental values or backend behavior.

Frame-QL is one request surface over the Measure Algebra, not part of its formal core.

## 8.4 Boundary with statistical inference

Objects familiar from statistics enter the Measure Algebra only after their formation and state laws have been declared. Until then, a numerical implementation is only a candidate computation.

Once admitted, a covariance, correlation, regression coefficient, or similar governed result does not become an inferential claim merely because its mathematical form is familiar.

A result can be a deterministic fact about the governed target established by the data. Statistical inference begins when the result is asked to stand for something beyond that target: a larger population, future periods, a latent process, another regime, a causal effect, or another transported setting.

Those questions require the additional structure of the Statistical Bridge (Wang 2026f).

> **The Measure Algebra determines which analytical results can be validly derived from governed data. Statistical inference requires additional assumptions and evidence.**

# 9. Formal status and open boundary

The Measure Algebra should not be read as a claim that the full Theory of Data already has one complete algebraic normal form.

The existing formal status is more precise.

The finite fragments of the Contract Calculus prove (Wang 2026b):

- typed multi-input pointwise maps at a common anchor;
- sufficient-state staging for commutative-monoid state;
- propagation of eligibility and observed support;
- restriction and population carve;
- coverage-qualified partial reduction for proved modes;
- relation-based expansion under replication, assignment, and weighted-allocation dispositions;
- structural conservation and fan-out refusal results;
- decidability and well-formedness preservation within those fragments.

Theory of Data Version 6.1 broadens the state-law space beyond the commutative fragment and supplies the current measure-family ontology.

This paper additionally derives the cross-measure support consequence in §5.2: marginal support counts do not determine support overlap. That result uses the deposited support model but is not attributed here as a theorem of the \(G_0\)–\(G_2\) fragments.

Several important extensions remain open or only partly formalized, including richer participation rules, partial ordered reducers, temporal integration, broader approximation contracts, richer universe forms, and a general multi-input family-synthesis calculus beyond the explicit cases already given in Version 6.1.

Those are extension boundaries, not reasons to deny the algebra already present.

The right claim is therefore:

> **The Measure Algebra is visible through proved finite fragments of governed measure transformation. It is not yet a completeness theorem for every lawful analytical operation.**

# 10. Conclusion

The Theory of Data starts from a simple change in viewpoint: an analytical quantity has identity and law before it has a physical realization.

Once measures are treated that way, their operations cannot be reduced to functions over columns.

A pointwise map requires typed inputs at a common analytical location.

A reduction requires sufficient state and a lawful movement.

A partial reduction must preserve enough domain state to determine eligibility and support.

A restriction and a carve can show the same values while making different population claims.

A relation establishes reachability, while a disposition determines what happens to the value and what can be done with it afterward.

A multi-measure operation cannot use a value or support relationship after that relationship has been destroyed. A materialization may therefore support some later derivations and not others.

These are algebraic facts about governed measures.

The practical conservation rule is:

> **An operation cannot use a relationship that was neither retained nor reconstructed from governed evidence.**

The architectural rule beneath it is:

> **Law determines what may be done. Realization determines how it is done.**

That is the Measure Algebra of the Theory of Data: not an algebra of physical columns, and not merely a larger query language, but the typed operation layer under which governed measures can be formed, transformed, reduced, and combined without silently changing what they mean.

# References

Wang, Huayin. 2026a. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 6.1. Zenodo. DOI: 10.5281/zenodo.22013410.

Wang, Huayin. 2026b. *A Contract Calculus for Governed Analytical Transformation: Totality, Partiality, Population, Expansion, and Fan-Out*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21752373.

Wang, Huayin. 2026c. *The Two Anchors of a Measure: Why Input and Output Anchors Are Part of Analytical Meaning*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21888464.

Wang, Huayin. 2026d. *Missingness Has a Universe: A Typed and Compositional Foundation for Missing-Data Research*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21783563.

Wang, Huayin. 2026e. *Certifiable State Under Information Loss: Governed Derivability, Claim Transport, and Approximate Closure*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21972541.

Wang, Huayin. 2026f. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: 10.5281/zenodo.21979821.

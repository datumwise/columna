---
title: "The Two Jobs of the Conditioning Bar"
subtitle: "Conditionalization, Model Constitution, and the Missing Inference Record"
author: "Huayin Wang"
doi: "10.5281/zenodo.22010143"
version: "1.0"
license: "CC BY 4.0"
date: "Version 1.0 - 19 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "A typed-record account of conditionalization, model constitution, Bayesian workflow, and theorem applicability"
keywords:
  - Bayesian inference
  - conditionalization
  - model revision
  - Bayesian workflow
  - Statistical Bridge
  - inference record
  - provenance
  - probabilistic programming
  - sufficient state
  - sequential inference
  - model checking
  - AI agents
---

**datumwise, an independent open-source research project**

**Version 1.0 - 19 August 2026**  
**DOI:** 10.5281/zenodo.22010143  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

**Foundation:** Huayin Wang, *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*, Version 3.0, DOI **10.5281/zenodo.21979821**.

# Abstract

Bayesian notation commonly writes a posterior as $p(\theta\mid X)$. The expression is always relative to a declared model. Writing that declaration explicitly gives $p(\theta\mid X,M)$, or, more carefully when $M$ serves as an index of the probability construction, $p_M(\theta\mid X)$.

That restoration is familiar. The consequence examined here appears only when the two inputs are also typed by how they entered the analysis. $X$ enters through an evidence event. $M$ enters through a declaration. Formal epistemology already distinguishes evidence update from expansion or revision of the hypothesis space. The additional problem arises in statistical practice: ordinary posterior notation places the realized evidence and the declared model inside one conditional presentation while the analysis record usually omits the transition type by which either changed.

This paper develops a record-level consequence. Bayes' theorem supplies lawful conditionalization inside a fixed declared model. A workflow can also criticize and replace that model. If the transcript records posterior states while suppressing model identity and transition type, two different histories can have the same transcript: one in which every transition is conditionalization under a fixed model and another containing a model-constitution event. The applicability of Bayes' theorem to a displayed transition is then **record-undecidable**: no decision rule using that transcript alone can recover the transition's type in every compatible history. The term names observational underdetermination of the record. Turing decidability lies outside the claim.

The constructive repair is a typed inference lineage. A **conditioning edge** adds evidence within one declared model version. A **constitution edge** establishes a new declared model version and starts a new inferential episode. Retained evidence may then be recomputed under the new declaration; any compressed transfer from the old episode requires its own explicit transport contract. This typing clarifies sequential Bayes, model checking, probabilistic programming, provenance, distributed inference, and approximate streaming updates. It also explains why modern Bayesian workflow necessarily contains tools outside posterior conditionalization itself: model criticism supplies evidence about declarations, computational diagnostics examine implementation fidelity, and software provenance records changes across model versions.

The mathematical content of Bayes' theorem remains unchanged. The object added here is its missing paperwork: a record rich enough to show where the theorem applies.

# 1. Introduction: the formula and its missing paperwork

A Bayesian analysis is often summarized by a line such as
$$
p(\theta\mid X)
\propto
p(X\mid\theta)\,p(\theta).
$$
The line is compact because much of the analysis has already been declared. The parameter has a meaning. The sample space has a structure. The likelihood belongs to a family. The prior belongs to the same construction. The observations have been admitted as evidence. Conditional-independence relations, measurement assumptions, and other premises determine what counts as the same model from one update to the next.

Collect those premises under a declared model $M$. Then the familiar expression has an additional coordinate:
$$
p_M(\theta\mid X)
\propto
p_M(X\mid\theta)\,p_M(\theta).
$$
The subscript notation is mathematically cleaner when $M$ indexes a probability construction. The alternative notation
$$
p(\theta\mid X,M)
$$
is epistemically useful because it puts the hidden operand on the page. The standing notation rule is therefore simple: $p_M(\theta\mid X)$ carries the mathematical development; $p(\theta\mid X,M)$ appears where the conditioning bar itself is under inspection. In both forms, $M$ means a **declared model**: the inferential construction that fixes the probability model, the meaning of its parameters, the evidence-generating account relevant to the certificate, and the material typed premises supplied to the analysis.

Nothing controversial has happened yet. Bayesian authors have made background information explicit for decades. Jaynes routinely wrote probabilities relative to background information, and modern probabilistic programs make model declaration far more explicit than compact textbook notation does (Jaynes 2003; Carpenter et al. 2017).

The first rung of the argument is deliberately obvious:
$$
\boxed{
\textbf{Bayesian inference is relative to a declared model }M.
}
$$
The next question creates the paper.

How did the two operands enter?

The observed $X$ was learned or admitted as evidence. The declared $M$ was supplied as a premise of the current inferential episode. Those are different epistemic acts. They also have different continuation rules. New evidence can be incorporated by further conditionalization under the same declaration. Criticism of the declaration can lead to a new model $M'$, after which the evidence is analyzed under a new inferential construction.

Formal epistemology already knows this distinction in several forms. Work on new theories and growing awareness studies what happens when the agent's hypothesis language or state space changes, where ordinary conditionalization over a fixed language no longer supplies the whole update rule (Wenmackers and Romeijn 2016; Steele and Stefánsson 2021; Karni and Vierø 2013). The present paper inherits that result.

Its question is about the **record of statistical practice**.

When a model changes during a workflow, does the transcript show that the transition crossed a declaration boundary? Can a later reviewer distinguish an ordinary Bayes update from a recomputation under a revised model? Can an autonomous statistical agent make the same distinction mechanically?

The central claim is:

> **A statistical record that suppresses model identity and transition type can erase the information required to determine whether a displayed posterior transition was an application of Bayes' theorem under one fixed declared model.**

The repair is constructive. The record carries two edge types:
$$
\text{conditioning within }M_v
\qquad\text{and}\qquad
\text{constitution of }M_{v+1}.
$$
Once those edges are explicit, theorem applicability becomes a checkable lineage property.

This paper therefore adds no new mathematics of probability. It proposes a type discipline for the history around the mathematics. Its stance is internal to modern Bayesian practice: iterative model building, model checking, simulation, computational diagnostics, and software development already behave as though the distinction matters. The purpose is to make the distinction explicit enough to audit.

# 2. The suppressed argument

## 2.1 What $M$ contains

The declared model $M$ is wider than a likelihood formula.

For the present paper, $M$ identifies enough structure to determine the current inferential episode. Depending on the problem, this can include:

- the sample and parameter spaces;
- the meaning and identity of $\theta$;
- the likelihood or forward probability construction;
- the prior or other target-side probability source;
- conditional-independence structure;
- measurement and missingness components carried inside the probabilistic construction;
- the mapping from governed evidence to the model's observed variables;
- computational parameterization where it changes the formal object being approximated.

The Statistical Bridge separates these components by role and evidential standing. A likelihood can supply evidence-side probability. A prior can supply target-side probability. A causal or measurement premise can participate in the construction while retaining a different evidential status. The joint mathematical representation therefore provides an inferential construction; its premises retain their own warrant (Wang 2026a).

That distinction matters here because a model can remain mathematically well formed while one of its premises becomes the object of criticism.

## 2.2 “Understood” and “recorded” are different states

A human analyst may know which model produced every posterior in a notebook. A collaborator reading one plot may infer the same context from nearby code. A probabilistic programming environment may reconstruct much of it from the source file.

Those are forms of recoverability from surrounding artifacts.

The compact posterior symbol itself carries less:
$$
p(\theta\mid X).
$$
It names the target quantity and evidence argument. It carries no explicit model version and no transition type.

This is often harmless. A theorem can suppress fixed context while everyone agrees that the context remains fixed.

The issue appears when workflow makes revision routine.

Suppose an analyst fits $M_0$, checks it, changes the likelihood family, adds a varying effect, revises the measurement model, or alters a missingness assumption, and then fits again. The analyst has crossed from one declared construction to another. The scientific workflow may be excellent. The posterior notation can remain unchanged:
$$
p(\theta\mid X).
$$
The symbol $\theta$ can also remain lexically unchanged while its interpretation changes because the surrounding model changed. Gelman, Simpson, and Betancourt's discussion of priors in the context of likelihoods is a useful reminder that parameter meaning and prior implications arise relationally from the entire model (Gelman, Simpson, and Betancourt 2017).

The missing coordinate is therefore more than a cosmetic subscript.

It is part of the identity of the inferential episode.

## 2.3 A useful objection: model uncertainty can live inside a larger model

Bayesian model comparison supplies an immediate objection.

Let a declared supermodel $M^\star$ contain a model index $J$:
$$
p(\theta,J,X\mid M^\star).
$$
Conditioning on evidence can then change posterior probability over $J$. Reversible-jump methods, mixture models, Bayesian model averaging, and other trans-dimensional constructions can likewise move among submodels while remaining inside one larger probability construction.

This is a lawful conditioning trajectory.

The present distinction therefore applies at the **highest declaration boundary relevant to the episode**.

If $M^\star$ and its alternatives were declared in advance, posterior movement among those alternatives is conditionalization within $M^\star$. If later criticism introduces a likelihood family, variable, measurement process, hypothesis, or state-space distinction absent from $M^\star$, a new declaration has occurred.

The distinction is:
$$
\boxed{
\text{uncertainty represented inside a declared model}
\quad\text{versus}\quad
\text{revision of the declared model itself}.
}
$$
That boundary is exactly where the awareness-growth literature becomes relevant.

# 3. The two jobs of the conditioning bar

With $M$ restored, the posterior can be displayed as
$$
p(\theta\mid X,M).
$$
The notation places $X$ and $M$ to the right of the same bar. Their epistemic provenance differs.
$$
\begin{array}{c|c|c}
\text{operand} & \text{entry event} & \text{role in current episode}\\
\hline
X & \text{evidence event} & \text{learned / observed / admitted}\\
M & \text{declaration event} & \text{supplied inferential construction}
\end{array}
$$
The bar is performing two jobs in the human reading of the expression.

This underlying two-kinds-of-change fact belongs to prior literature. Wenmackers and Romeijn develop open-minded Bayesianism with conditionalization for evidence and an additional rule for the arrival of new hypotheses, allowing successive probability functions to have different domains. Steele and Stefánsson study belief revision under growing awareness. Karni and Vierø develop reverse Bayesianism for expanding awareness in decision theory. These programs differ in purpose, yet all make one point available to the present paper: change inside a fixed state space and change of the state space require different treatment (Wenmackers and Romeijn 2016; Steele and Stefánsson 2021; Karni and Vierø 2013).

The statistical problem begins after that distinction is granted.

The two jobs diverge under four independent laws: **composition, continuation, repair, and warrant**. Each subsection isolates one.

## 3.1 Composition

Conditionalization has a staging law.

For evidence blocks $X_1,X_2$, under one fixed declared model and the relevant factorization,
$$
p_M(\theta\mid X_1,X_2)
\propto
p_M(X_2\mid \theta,X_1)\,
p_M(\theta\mid X_1).
$$
When $X_2$ is conditionally independent of $X_1$ given $\theta$,
$$
p_M(\theta\mid X_1,X_2)
\propto
p_M(X_2\mid\theta)\,
p_M(\theta\mid X_1).
$$
The first posterior can serve as the prior state for the next evidence event because the parameter and probability construction retain identity.

Replacing $M_0$ with $M_1$ changes the construction relative to which the posterior is defined. A general identity of the following form is unavailable:
$$
p_{M_1}(\theta\mid X)
=
\text{BayesUpdate}\bigl(p_{M_0}(\theta\mid X),M_1\bigr).
$$
Any relationship carrying state from $M_0$ to $M_1$ is additional structure.

## 3.2 Continuation

An exact posterior under fixed $M$, together with the new-data likelihood, can lawfully continue sequential inference.

A new declaration changes the carrier question. The previous posterior may still serve as evidence about past analysis, initialization, a proposal distribution, or an input to an explicitly justified transfer construction. Its authority under $M_0$ stays attached to $M_0$.

The canonical crossing is: declare $M_1$, retain or reconstruct the governed evidence relevant under $M_1$, and derive the new certificate there. A compressed carrier can cross when an explicit map states what information and warrant survive; that map belongs to the constitution contract.

## 3.3 Repair

Evidence correction and model criticism also differ.

If one observation was miscoded while the declared model remains fixed, the analysis can repair the evidence record and recompute under the same $M$.

If a predictive check reveals that the likelihood family misses a material feature, the repair targets $M$. A revised declaration begins a new episode.

The same software action—edit code and rerun—can therefore instantiate different epistemic edges.

## 3.4 Warrant

An evidence event can add support relevant to a claim. A model declaration introduces premises whose evidential standing is inherited from their sources: design, domain knowledge, measurement studies, prior elicitation, scientific theory, convenience, or other grounds.

Representation inside a probability model changes mathematical role while evidential standing remains source-governed. This is the conservation discipline used in the Statistical Bridge and in *Certifiable State Under Information Loss*: evidence-neutral transformation can preserve or weaken warrant, while promotion requires a relevant evidence-producing event or rule (Wang 2026a, 2026b).

## 3.5 Jaynes as a controlled experiment

Jaynes is especially important because he restored background information explicitly.

His notation consistently emphasizes that probability is conditional on information. That is a major ancestor of the present argument. It shows that explicitness alone can coexist with epistemic flattening.

A symbol such as $I$ can contain logical facts, model assumptions, prior information, measurement conventions, and learned evidence. Once all of them enter as one undifferentiated information bundle, the record still lacks the type of event by which each component entered.

The point is therefore:
$$
\boxed{
\text{explicit background}
+
\text{typed provenance}
}
$$
is stronger than explicit background alone.

Jaynes reached the first half on principle. The present paper asks what statistical workflow requires from the second.

# 4. A record-undecidability result

The strongest claim can be stated with very little machinery.

## 4.1 Histories and transcripts

Let $H$ be a set of full analysis histories.

A history records, at minimum:

- the declared model version active at each step;
- the admitted evidence;
- the inferential state;
- the transition type between steps.

Let
$$
\rho:H\rightarrow T
$$
be a projection into a standard transcript language $T$ that suppresses model version and transition type. The transcript may retain parameter labels, observed data labels, posterior summaries, plots, or even complete posterior distributions.

For a particular **displayed transition** $j$, let the full history contain the edge segment that connects the two displayed states. Define
$$
V_j(h)=1
$$
when that segment is pure conditionalization under one fixed declared model, and
$$
V_j(h)=0
$$
when the segment contains a declaration boundary while the transcript presents it as continuation of the same inferential episode.

The question is whether a function of the transcript alone can recover $V_j$.

## 4.2 Proposition: transcript insufficiency

**Proposition 1 — Record-undecidability of transition validity.**

If there exist histories $h_0,h_1\in H$ such that
$$
\rho(h_0)=\rho(h_1)
$$
while
$$
V_j(h_0)\neq V_j(h_1),
$$
then no decision function
$$
d:T\rightarrow\{0,1\}
$$
can satisfy
$$
d(\rho(h))=V_j(h)
$$
for every history $h\in H$.

**Proof.** Let $\rho(h_0)=\rho(h_1)=t$. Any function $d$ assigns one value to $t$. Since $V_j(h_0)\neq V_j(h_1)$, that value disagrees with at least one history. $\square$

**Converse for the transition predicate.** Let an enriched record language retain the ordered edge segment behind each displayed transition, with source and target model versions and
$$
\tau_k\in\{\mathsf{cond},\mathsf{const}\}
$$
for every constituent edge $k$. Then $V_j$ is decidable by inspection: $V_j=1$ exactly when the segment consists only of conditioning edges under one unchanged model version; any constitution edge makes $V_j=0$. Proposition 1 establishes the necessity of the erased coordinate whenever histories that differ on $V_j$ collide under $\rho$; retaining the typed segment is sufficient to decide $V_j$.

This converse concerns the transition predicate defined here. The remaining premises of an inference retain their own certificate obligations: evidence admissibility, likelihood and prior specification, approximation fidelity, implementation correctness, and claim license remain separately governed.

The result is elementary. Its burden lies in the premise: can two inferentially different histories project to the same standard transcript?

They can whenever the record language omits the distinguishing coordinate.

One history can remain within $M_0$:
$$
M_0
\xrightarrow{\operatorname{cond}(X_1)}
M_0
\xrightarrow{\operatorname{cond}(X_2)}
M_0.
$$
Another can revise the declaration after $X_1$:
$$
M_0
\xrightarrow{\operatorname{cond}(X_1)}
M_0
\xrightarrow{\operatorname{const}}
M_1
\xrightarrow{\operatorname{cond}(X_1\cup X_2)}
M_1.
$$
The constitution edge establishes the new declaration. The retained governed evidence then re-enters the new episode through conditioning.

**Worked collision: a stopping-rule pair.** Let
$$
\theta\sim\operatorname{Beta}(1,1)
$$
and let $X_1$ contain 10 Bernoulli trials with four successes and six failures. Under the initial declaration $M_0$, the design is fixed-$n$ sampling. The first displayed posterior is
$$
\theta\mid X_1,M_0\sim\operatorname{Beta}(5,7).
$$
Now observe another 10 trials containing four successes and six failures, with trial 20 being the eighth success overall. History $h_A$ keeps $M_0$ fixed and conditions on $X_2$, giving
$$
\theta\mid X_1,X_2,M_0\sim\operatorname{Beta}(9,13).
$$
History $h_B$ discovers after $X_1$ that the experiment was actually governed by a stopping rule: sampling continued until the eighth success. It therefore crosses a constitution edge to $M_1$ and reconditions from the retained evidence roots on all 20 trials. The two realized likelihoods are
$$
L_0(\theta)
\propto
\binom{20}{8}\theta^8(1-\theta)^{12}
$$
under fixed-$n$ sampling and
$$
L_1(\theta)
\propto
\binom{19}{7}\theta^8(1-\theta)^{12}
$$
under stopping at the eighth success on trial 20. Their combinatorial factors differ while their $\theta$-dependence is proportional, so the second displayed posterior under $M_1$ is again
$$
\theta\mid X_1,X_2,M_1\sim\operatorname{Beta}(9,13).
$$
A transcript retaining only the two posterior displays therefore records the same sequence,
$$
\operatorname{Beta}(5,7)
\longrightarrow
\operatorname{Beta}(9,13),
$$
for both histories. In $h_A$, the displayed transition is ordinary conditioning under $M_0$. In $h_B$, the displayed transition spans constitution into $M_1$ followed by reconditioning from roots. The sample spaces, stopping-rule declaration, predictive questions, and replication semantics differ even though the realized posterior for $\theta$ coincides exactly.

This is an explicit witness to the premise of Proposition 1:
$$
\rho(h_A)=\rho(h_B),
\qquad
V_j(h_A)\neq V_j(h_B).
$$
A transcript that records only “posterior after $X_1$” and “posterior after $X_2$” can therefore hide the distinction even when it retains exact numerical posterior output. Extensional equality of the displayed state leaves inferential lineage underdetermined.

This echoes a central result of *Certifiable State Under Information Loss*: identical operational extension can support different certifiable futures when contract and evidence history differ (Wang 2026b).

## 4.3 What “undecidable” means here

The proposition is a statement about **record semantics**.

It says that validity is underdetermined by a projection that erases a load-bearing coordinate.

It makes no claim about Turing undecidability, halting problems, or computational complexity.

The more formal phrase is:

> **transition validity is non-identifiable from the projected transcript.**

“Record-undecidable” is retained because it states the practical review problem directly: the record lacks enough information for a reviewer or checker to decide the property.

## 4.4 The closest antecedent

Wenmackers and Romeijn provide the closest formal-epistemology antecedent. Their open-minded Bayesian framework distinguishes ordinary evidence conditionalization from enlargement of the hypothesis domain, and their discussion of silent open-mindedness observes that implicit conditioning on theoretical context can make an episode appear like ordinary Bayesianism (Wenmackers and Romeijn 2016).

That is an antecedent of the premise above.

The additional move here is to treat the suppressed distinction as a property of the **analysis record** and to ask what information is necessary for theorem applicability to become mechanically reviewable.

The same division separates this result from diachronic Dutch-book and Reflection arguments. Lewis, Teller, and van Fraassen study rational constraints across credence trajectories (Teller 1973; van Fraassen 1984; Lewis 1999). The present question begins after a trajectory is observed: what type of transition produced each movement, and can the record establish that type?

## 4.5 The frequentist mirror

The record problem has a frequentist mirror.

A sampling or testing guarantee is relative to a declared procedure and reference structure. Data-dependent changes to the analysis can alter the relevant ensemble even when the final formula looks familiar. Gelman and Loken's garden of forking paths gives a prominent example: analysis choices can depend on realized data even when the analyst follows one apparently natural path (Gelman and Loken 2013).

The orthography differs across traditions. The structural issue is shared:
$$
\boxed{
\text{a theorem relative to a fixed procedure needs a record of what stayed fixed}.
}
$$
Preregistration, analysis plans, source control, and workflow provenance can all record pieces of that history. The next section gives the inference-specific typing they currently lack as a common statistical vocabulary.

# 5. The constructive repair: two edge types

The repair is a typed lineage.

Let an inferential state at step $t$ be represented schematically as
$$
R_t=(M_v,E_t,K_t,\Gamma_t),
$$
where:

- $M_v$ is the active declared model version;
- $E_t$ is the governed evidence ledger;
- $K_t$ is the carried inferential state;
- $\Gamma_t$ is the contract environment identifying what $K_t$ means and which continuations it supports.

Two transition types are primitive.

## 5.1 Conditioning edge

A conditioning edge has the form
$$
R_t
\xrightarrow{\;\mathsf{cond}(x)\;}
R_{t+1}
$$
with
$$
M_{v(t+1)}=M_{v(t)}.
$$
Its checker can require:

1. the declared model identity is unchanged;
2. the new evidence is admissible under the active evidence contract;
3. the carried state is sufficient for the declared update or the root evidence is available for recomputation;
4. the prior contribution is applied exactly once;
5. any conditional-independence or dependence assumptions used by staged updating are declared.

Bayes applies on this edge.

## 5.2 Constitution edge

A constitution edge has the form
$$
R_t
\xrightarrow{\;\mathsf{const}(\Delta M)\;}
R_{t+1}
$$
with a new declared model version
$$
M_{v+1}.
$$
This edge records:

- what changed in the declaration;
- why the change occurred;
- which evidence or criticism motivated it;
- which prior inferential objects are retained as evidence-about, initialization, proposals, or transfer inputs;
- which root evidence is re-admitted under the new construction;
- any explicit transport map used in place of full recomputation.

Bayes is silent about the constitution edge itself. Bayesian inference resumes inside the newly declared model once the new episode is established.

## 5.3 A two-edge lineage

The core picture is:
$$
\begin{aligned}
R^{(0)}_0
&\xrightarrow{\mathsf{cond}(X_1)}
R^{(0)}_1
\xrightarrow{\mathsf{cond}(X_2)}
R^{(0)}_2,\\[5pt]
R^{(0)}_1
&\xrightarrow{\mathsf{const}\,[M_0\to M_1;\,E_{\le 1}]}
R^{(1)}_0
\xrightarrow{\mathsf{cond}(X_1)}
R^{(1)}_1
\xrightarrow{\mathsf{cond}(X_2)}
R^{(1)}_2.
\end{aligned}
$$
The constitution edge leaves the concrete analysis state $R^{(0)}_1$. Its label records the model-version crossing $M_0\to M_1$ and retains the governed evidence ledger $E_{\le 1}$. The target $R^{(1)}_0$ is the newly constituted pre-conditioning state under $M_1$; governed evidence then re-enters through conditioning edges.

The constitution edge is epistemically different from the conditioning edges.

A workflow can cross it freely when criticism warrants revision. The type keeps the crossing explicit in the inferential lineage.

## 5.4 Refit from roots and explicit transport

Refitting from retained root evidence is the canonical crossing. A compressed crossing is also lawful when an explicit transformation
$$
\Phi_{0\to1}
$$
states what information and warrant survive from $M_0$ into $M_1$. Analytically justified moment transfer, modular prior construction, and deliberate empirical-prior reuse are examples when their contracts are explicit.

The governing rule is:
$$
\boxed{
\text{cross-model state travels only through an explicit transport contract}.
}
$$
**Worked transfer: a prior revision.** Suppose $M_0$ uses the Bernoulli likelihood from Section 6 and
$$
\theta\sim\operatorname{Beta}(\alpha_0,\beta_0).
$$
Evidence $X$ contributes $s$ successes and $f$ failures, so
$$
\theta\mid X,M_0
\sim
\operatorname{Beta}(\alpha_0+s,\beta_0+f).
$$
Now a new elicitation changes only the prior:
$$
M_1:\qquad
\theta\sim\operatorname{Beta}(\alpha_1,\beta_1),
$$
while the parameter meaning, Bernoulli likelihood, and evidence semantics stay fixed. The count contribution $(s,f)$ has the same likelihood meaning under both declarations. A transport contract can therefore carry $(s,f)$ across the constitution edge, yielding
$$
\theta\mid X,M_1
\sim
\operatorname{Beta}(\alpha_1+s,\beta_1+f).
$$
The failure mode is equally concrete. If the old posterior
$$
\operatorname{Beta}(\alpha_0+s,\beta_0+f)
$$
is substituted for the newly declared $M_1$ prior and the same evidence $X$ is then entered again, the result is
$$
\operatorname{Beta}(\alpha_0+2s,\beta_0+2f).
$$
The old evidence has been counted twice, and the declared prior $\operatorname{Beta}(\alpha_1,\beta_1)$ has disappeared from the construction.

For this crossing, the portable evidence state is the likelihood contribution represented by $(s,f)$. Posterior authority remains attached to the declaration under which the posterior was formed; a posterior can take on a new cross-model role only through an explicit transfer contract.

This distinction matters in distributed and privacy-constrained systems, where certified compressed carriers may be required even when retained-root recomputation would otherwise be preferable.

## 5.5 PROV as carrier, typed lineage as vocabulary

W3C PROV already supplies a general provenance model with entities, activities, derivations, revisions, bundles, and extensibility for domain-specific types. A typed Bayesian lineage can therefore be implemented using PROV or another provenance system (W3C 2013).

The contribution here is the inference-specific vocabulary:
$$
\mathsf{conditioning\_under}(M_v)
$$
and
$$
\mathsf{constitution\_of}(M_{v+1}),
$$
together with the rules that attach Bayes applicability to the first type.

This is a useful architectural separation:

> **The provenance carrier stores the history. The inference type system states what the history means.**

A repository diff records that an artifact changed. The edge type records what kind of inferential event the change was.

# 6. The worked thread: from exact staging to lossy carriers

The argument becomes concrete in the simplest conjugate example.

Let
$$
\theta\sim\operatorname{Beta}(\alpha,\beta)
$$
and, under fixed $M$,
$$
Y_i\mid\theta\sim\operatorname{Bernoulli}(\theta)
$$
conditionally independently.

For a batch with $s$ successes and $f$ failures,
$$
\theta\mid Y
\sim
\operatorname{Beta}(\alpha+s,\beta+f).
$$
The sufficient carried state is the pair of accumulated counts.

## 6.1 Beat one: sequential equals batch

Split one dataset into two batches:
$$
(s_1,f_1),
\qquad
(s_2,f_2).
$$
Updating in sequence gives
$$
\operatorname{Beta}(\alpha,\beta)
\rightarrow
\operatorname{Beta}(\alpha+s_1,\beta+f_1)
\rightarrow
\operatorname{Beta}(\alpha+s_1+s_2,\beta+f_1+f_2).
$$
Batch updating gives the same final distribution immediately:
$$
\operatorname{Beta}(\alpha+s_1+s_2,\beta+f_1+f_2).
$$
The order of the two batches also disappears from the final exact state.

This is one of Bayesian inference's strongest practical properties. Evidence can be staged.

The result has premises:
$$
\boxed{
\begin{array}{l}
\text{same declared model};\\
\text{same parameter identity};\\
\text{prior contribution used once};\\
\text{declared dependence structure respected};\\
\text{exact carrier or exact recomputation}.
\end{array}
}
$$
The ordinary posterior symbol suppresses most of that list.

## 6.2 Beat two: the extreme early batch

Take the prior
$$
\theta\sim\operatorname{Beta}(1,1).
$$
Suppose the first ten observations are all successes. The exact posterior is
$$
\operatorname{Beta}(11,1).
$$
It is strongly concentrated near one. Yet it retains positive density throughout the open interval $(0,1)$, and its two parameters retain exactly the count information required for the declared continuation.

If the next 990 observations contain 495 successes and 495 failures, exact updating yields
$$
\operatorname{Beta}(506,496).
$$
Processing the 990 observations first and the ten successes later yields the same final result.

The early extreme batch therefore creates no exact-Bayes trapping in this model.

The original instinct becomes useful once an approximation step is inserted.

Suppose the $\operatorname{Beta}(11,1)$ posterior is projected into a lossy approximation family and only that approximation is carried forward. A Gaussian approximation on an inconvenient scale can distort support and tail mass. A moment projection in assumed-density filtering can make the next approximation depend on the order of likelihood factors. Minka's expectation propagation work begins from precisely this setting: assumed-density filtering is a one-pass sequential approximation, while EP revisits factors iteratively to improve the global approximation (Minka 2001).

Now the schedule can matter.

Under regular Bernstein-von Mises conditions, a larger initial batch can move the posterior into a region where a Gaussian approximation is more accurate. “Large batch first” can therefore become a useful **approximation-contract heuristic**. Its authority is conditional on those regularity and approximation conditions.

The lesson is:

> **Exact Bayes removes the order effect under the staging premises. Approximation can reintroduce process dependence.**

## 6.3 Beat three: the impossible finite exact carrier

Conjugacy makes the exact carrier unusually small.

For general models, a finite-dimensional posterior family may fail closure under arbitrary future updates. Three carrier classes then become useful.

**Exact finite carrier.** A finite state such as conjugate counts supports exact continuation under its declared model.

**Exact-in-principle carrier.** The system retains governed root evidence plus the declared model. Future analysis can be recomputed exactly in mathematical principle even when no compact exact posterior state exists.

**Lossy carrier with contract.** Posterior draws, variational parameters, assumed-density approximations, sketches, or other compressed states support declared continuations with approximation error, Monte Carlo error, or restricted query classes.

A fourth case belongs on another axis:

**Model crossing.** The declared model changes. Continuation requires a constitution edge plus retained roots or an explicit transport map.

This taxonomy keeps two questions separate:

1. how much inferential state survived;
2. whether the inferential identity itself stayed fixed.

## 6.4 Chunked-versus-batch agreement as a diagnostic

The staging theorem suggests a runnable check.

Under one fixed model and an exact implementation, compare:
$$
\text{fit}(X_1\cup X_2)
$$
with
$$
\text{update}(\text{fit}(X_1),X_2).
$$
Material disagreement can reveal:

- accidental prior reuse;
- approximation loss;
- dropped dependence;
- model changes between episodes;
- software defects;
- stochastic Monte Carlo error beyond tolerance.

The check is diagnostic; certification requires additional checks and record evidence.

Agreement is compatible with several hidden failures. Two wrong implementations can agree. A lossy approximation can happen to be order-stable. A changed model can coincide numerically on the realized data.

The asymmetry is useful:

> **Order sensitivity under a theorem that predicts order invariance identifies a violated premise or approximation effect worth investigating. Order agreement supplies one check among several.**

# 7. The posterior display and the missing carrier contract

The phrase “the posterior” can name several different objects:

- an exact mathematical distribution;
- a normalized density expression;
- a finite set of draws;
- variational parameters;
- a plot;
- a table of quantiles;
- a serialized object in software.

Their continuation capabilities differ.

An exact posterior under fixed $M$, with the new-evidence likelihood available, is a lawful prior state for sequential Bayes.

A posterior **display** can be much poorer.

## 7.1 Why posterior displays require provenance for composition

Let $D_1$ and $D_2$ be conditionally independent given $\theta$, with shared prior $p(\theta)$.

Then
$$
p(\theta\mid D_1,D_2)
\propto
p(\theta)L_1(\theta)L_2(\theta).
$$
The product of two independently computed posteriors is
$$
p(\theta\mid D_1)\,
p(\theta\mid D_2)
\propto
p(\theta)^2L_1(\theta)L_2(\theta).
$$
The prior has been counted twice.

The correction is straightforward when provenance is known:
$$
p(\theta\mid D_1,D_2)
\propto
\frac{
p(\theta\mid D_1)\,
p(\theta\mid D_2)
}{
p(\theta)
}.
$$
Other distributed constructions allocate fractional priors or use approximation schemes designed for subset posteriors. Consensus Monte Carlo and embarrassingly parallel MCMC literatures make the engineering problem explicit: distributed subposterior states require carefully specified combination rules (Scott et al. 2016; Neiswanger, Wang, and Xing 2014).

The structural point is:
$$
\boxed{
\text{generic posterior composition requires provenance beyond posterior values}.
}
$$
The missing information includes prior allocation, model identity, evidence overlap, approximation method, and dependence assumptions.

## 7.2 A posterior sample bag is an approximate state

Posterior draws are enormously useful. They can approximate expectations, quantiles, decisions, predictive distributions, and derived quantities.

They are still a materialized approximation to a mathematical posterior unless the problem itself is discrete and exactly enumerated.

Their continuation contract depends on what future operation is requested.

Importance reweighting may support one class of changes.

Sequential Monte Carlo may support another.

A fresh model fit from retained data may be required for another.

The right question is therefore:

> **What continuation does this carried state certify?**

That is the statistical analogue of a general state principle in *Certifiable State Under Information Loss*: a displayed value can preserve a present answer while discarding state, contracts, or evidence needed for future lawful operations (Wang 2026b).

# 8. The calculus and its boundaries

A modern Bayesian workflow contains much more than repeated applications of Bayes' theorem.

Gelman and Shalizi place model checking and model revision at the center of applied Bayesian practice and explicitly locate those activities outside a closed Bayesian confirmation story (Gelman and Shalizi 2013). The 2026 *Bayesian Workflow* book expands this into a many-object, many-pass practice of model building, simulation, fitting, checking, troubleshooting, comparison, scientific interpretation, and software development (Gelman et al. 2026).

The typed record explains why this surrounding machinery is structurally necessary.

## 8.1 Model warrant

Bayes' theorem derives consequences relative to a declared probability construction.

Evidence that the construction is scientifically adequate comes from other passages:

- experimental or design knowledge;
- measurement studies;
- prior predictive implications;
- simulated-data experiments;
- posterior predictive criticism;
- external validation;
- sensitivity analysis;
- domain evidence.

These activities can affect the evidential status of model premises.

They are evidence-producing or premise-testing events that add information about premises beyond the algebraic consequences of the original posterior.

The earlier *Reading Bayesian Workflow Through the Statistical Bridge* summarized this with a simple question: **what checking checks?** Different checks interrogate different premises, and warrant is promoted only where the new evidence bears (Wang 2026c).

## 8.2 Implementation fidelity

Even a well-warranted model can be implemented badly.

MCMC diagnostics, convergence analysis, simulation-based calibration, unit tests, synthetic-data recovery, and other computational checks ask whether the software and algorithm realize the declared inferential object accurately enough for the intended certificate.

This creates another boundary:
$$
\text{declared model validity}
\qquad\text{and}\qquad
\text{implementation fidelity}
$$
are different review questions.

A converged sampler can faithfully approximate the wrong empirical model.

A scientifically sensible model can also be paired with a broken sampler.

The Statistical Bridge keeps these authorities separate: an inference certificate derives from declared sources and premises, while executable checks strengthen reviewability of particular parts of the construction (Wang 2026a).

## 8.3 Workflow as typed revision

The workflow school can therefore be read constructively.

A loop permits:
$$
M_0
\to
\text{fit}
\to
\text{check}
\to
M_1
\to
\text{fit}
\to
\text{check}
\to\cdots
$$
The typed lineage expands that into alternating edge classes:
$$
M_0
\xrightarrow{\mathsf{cond}}
\text{posterior}_0
\xrightarrow{\mathsf{check}}
\text{evidence-about-}M_0
\xrightarrow{\mathsf{const}}
M_1
\xrightarrow{\mathsf{cond}}
\text{posterior}_1.
$$
The loop is legitimate because the edge types differ.

This is the paper's inversion:

> **Model criticism, computational diagnostics, simulation, and refitting are structural boundary equipment around conditional inference. Their plurality follows from the fact that the conditional calculus derives consequences inside a declaration while the workflow must also evaluate and revise the declaration itself.**

That gives Bayesian workflow a structural justification.

## 8.4 Refusal lives at the boundary

Inside a fully specified probability model, conditional questions usually receive mathematical answers wherever the relevant conditional distribution is defined.

A governed statistical system faces an earlier question:

> Is the requested inferential passage established strongly enough to emit the requested claim?

The answer can be refusal.

A required model declaration may be missing. Evidence provenance may be unresolved. The requested claim may outrun the license. A model crossing may lack a transport contract.

Refusal is therefore a property of the governed boundary around inference. It corresponds to underivability in the wider certificate system and appears as a boundary outcome.

# 9. The typed Bayesian record

The constructive artifact can now be stated directly.

For a reported inferential result, retain:
$$
\boxed{
\mathcal R
=
(
C,\,
M_v,\,
E,\,
P,\,
K,\,
\Lambda
)
}
$$
where:

- $C$ is the claim or inferential target;
- $M_v$ is the versioned declared model with typed premises and evidential statuses;
- $E$ is the governed evidence object and provenance;
- $P$ is the probability-source and conditioning/reference declaration;
- $K$ is the carried inferential state together with its continuation or approximation contract;
- $\Lambda$ is the typed lineage of conditioning, checking, transport, and constitution events.

$M_v$ records the versioned inferential construction itself. $P$ records the role assignment of that construction for this claim: where probability enters, which components serve evidence-side or target-side roles, and any non-Bayesian reference declaration carried by the certificate.

The object is intentionally schematic: a record contract independent of any one file format.

## 9.1 Relation to the Statistical Bridge

The Statistical Bridge already asks a mature analysis to expose:

- bridge constitution;
- probability source;
- inference certificate;
- evidential standing of material premises;
- claim license.

The typed Bayesian record adds the **diachronic coordinate** needed when the declared model changes through workflow.

A posterior can serve as an inference certificate for one episode.

The lineage records which declaration licensed that certificate and how later episodes relate to it.

This avoids a common flattening:
$$
\text{posterior}_0,\text{posterior}_1,\text{posterior}_2
$$
is a sequence of displayed objects.

A typed lineage says whether the sequence is:
$$
\text{one model + accumulating evidence},
$$
$$
\text{one model + approximate state updates},
$$
or
$$
\text{several models + constitution events}.
$$
Those are different inferential histories even when every element is called “posterior.”

## 9.2 Probabilistic programming gets halfway there

Probabilistic programming provides strong evidence that the distinction is implementable.

Stan separates declared data and parameters from statements contributing to the model log density, and probabilistic-programming semantics can make conditioning an explicit language construct. Stein and Staton's work gives first-class exact conditioning a compositional semantics in a probabilistic language (Stein and Staton 2021).

This types the **single episode**.

The remaining object is the relationship between program versions.

Stan's current Reference Manual makes exact reproducibility depend on a fixed computational environment and configuration, including Stan and interface versions, initialization, data, and other execution details. Its diagnostic guidance separately tells users to save model and initialization files, keep interface commands in scripts, and use Git so changes have a history (Stan Development Team 2026a, 2026b).

Those recommendations are revealing.

Part of the cross-model trajectory currently lives in software-development provenance. The typed Bayesian record gives that trajectory inferential semantics.

## 9.3 Five partial remedies

The surrounding literature now presents a useful pattern.

**Jaynes:** background information is explicit; its epistemic kinds remain bundled.

**McElreath-style model blocks:** the declaration is visible and teachable; the block still represents several premises inside one construction (McElreath 2020; Wang 2026e).

**Probabilistic programming:** declaration and conditioning become executable and, in some languages, semantically typed inside an episode.

**Version control:** program changes become historically recoverable across episodes; the repository records edits, while the typed lineage supplies their inferential type.

**Update-trail epistemology:** Stilwell's 2026 manuscript treats a posterior credence as answerable to its evidential history and develops update trails, path integrity, and audit-trail adequacy; the companion *Category Confidence* adds explicit attention to frame changes (Stilwell 2026a, 2026b).

These are independent partial remedies around one general pressure: final-state notation loses history that later evaluation may need.

The specific claim of the present paper is narrower:

> **A typed inference record should distinguish conditioning under a fixed declared model from constitution of a new declared model because that distinction is the information required to audit Bayes-theorem applicability across a workflow.**

## 9.4 The Stilwell boundary

Stilwell is the closest contemporary neighbor on record sensitivity.

His object is an agent's credence trajectory: how assigned confidence answers to evidence over time. The update trail records prior confidence, evidence events, live alternatives, update conditions, revisions, and reasons for movement; path integrity evaluates evidence gathering, alternative representation, symmetry of standards, preservation of uncertainty, responsiveness to update conditions, and record quality (Stilwell 2026a).

The present object is an analysis transcript.

Its key predicate is transition validity: whether a displayed inferential step belongs to one fixed declared model and therefore qualifies as a conditioning edge, or crosses a model-constitution boundary.

The two programs can complement each other.

A doxastic audit asks whether confidence moved as evidence warranted.

An inference-lineage audit asks what formal operation occurred and whether the theorem invoked at that edge had the required declaration identity.

## 9.5 Autonomous statistics

Human analysts often carry model versions tacitly.

An autonomous agent can edit model code, choose variables, revise priors, alter likelihoods, rerun inference, inspect diagnostics, and continue the loop at machine speed. That capability makes the edge type operationally important.

A governed agent should be able to answer:

- Which declared model version produced this certificate?
- Which evidence events entered by conditioning?
- Which checks generated evidence about the model or implementation?
- Which model changes created constitution edges?
- Which carried states remain valid for the requested continuation?
- Which claim is licensed by the current lineage?

The typed record becomes the wire object between statistical episodes.

It lets the agent continue when continuation is derivable, reconstitute when the model changes, disclose approximation limits when material, and refuse a transition whose required contract is absent.

# 10. Adjacencies and the novelty boundary

The literature search for this paper changed its novelty claim.

That is a feature of the result.

## 10.1 New theories and growing awareness

Wenmackers and Romeijn are the principal antecedent. Their framework for open-minded Bayesianism distinguishes ordinary evidence conditionalization from a second kind of update associated with new hypotheses and changing domains. Their silent-context observation also anticipates part of the indistinguishability premise used in Section 4 (Wenmackers and Romeijn 2016).

Steele and Stefánsson and Karni and Vierø independently reinforce the broader point: fixed-language conditionalization and growing-awareness revision are different normative problems (Steele and Stefánsson 2021; Karni and Vierø 2013).

The present paper therefore claims no discovery of the two-kinds-of-change fact.

Its contribution begins at statistical record semantics.

## 10.2 Diachronic coherence

Teller, van Fraassen, and Lewis study constraints on rational credence across time: conditionalization, Reflection, and diachronic coherence (Teller 1973; van Fraassen 1984; Lewis 1999).

Those results ask how beliefs should relate across a trajectory.

The present record problem asks which operation generated a particular inferential transition and whether the transcript contains enough information to classify it.

## 10.3 Old evidence

Glymour's old-evidence problem exposed a durable difficulty for simple Bayesian confirmation accounts when known evidence becomes newly relevant to a theory (Glymour 1980). Later open-minded Bayesian work connects that problem to new theories explicitly.

This is close to the evidence/background boundary.

The present paper uses a different target property: recoverability of model identity and transition type from the statistical record.

## 10.4 Probabilistic-programming semantics

Probabilistic programming is a stronger neighbor than ordinary notation because model declaration is code and conditioning can be a typed operation.

That resolves much of the single-episode problem.

The workflow crosses another boundary when the program itself changes.

The cross-version lineage is the remaining object.

## 10.5 Provenance systems

W3C PROV can represent revisions and can be specialized with application-specific types. The present proposal can therefore ride on a mature provenance carrier.

Its additional content is a statistical type vocabulary and applicability rule.

## 10.6 Evidential histories of posterior credence

Stilwell's update trails establish clear prior art for record-sensitive evaluation of posterior credence, and *Category Confidence* explicitly adds frame-change logs to those trails (Stilwell 2026a, 2026b).

The current claim is more specific: conditioning/constitution typing supplies the coordinate needed to determine whether a Bayes step remained inside one declared model.

The resulting novelty statement is intentionally narrow:

> **The contribution is a typed inference lineage in which conditioning and model constitution are distinct transition classes, making Bayes-theorem applicability a checkable property of a recorded workflow.**

# 11. Scope and boundaries

The paper's scope can be stated positively.

It treats Bayes' theorem as a sound identity inside its declared probability construction.

It inherits the distinction between evidence update and hypothesis-space change from formal epistemology.

It treats probabilistic programming and provenance standards as implementation allies.

It treats Bayesian workflow as the practical setting in which typed model transitions become most useful.

It uses sufficient-state language only relative to declared statistical continuation. Classical statistical sufficiency, conjugate finite state, Monte Carlo state, and Theory-of-Data sufficient state remain distinct concepts with partially analogous roles.

It leaves several neighboring problems to other work.

The frequentist-Bayesian school divide remains in *Where Does Probability Live?* (Wang 2026d).

The wider warrant structure of statistical inference remains in *The Statistical Bridge* (Wang 2026a).

Proof-relevant state and evidence conservation remain in *Certifiable State Under Information Loss* (Wang 2026b).

Parameter identity across changing model spaces, trans-dimensional inference, and the question “where does the parameter live?” deserve a separate treatment.

The present paper has one job:

> **Make the model coordinate and transition type explicit enough that a workflow can show where conditionalization ends and constitution begins.**

# 12. Open problems

## 12.1 A trusted lineage checker

The record semantics suggest a small checker.

For every edge, verify:
$$
\begin{array}{ll}
\mathsf{cond}: &
\text{model version stable; evidence admissible; carrier adequate; prior use lawful};\\[3pt]
\mathsf{const}: &
\text{new model version declared; change recorded; retained evidence or transfer contract identified}.
\end{array}
$$
A practical system could then reject a purported conditioning edge whose model hash changed, or require a constitution record before accepting the next inference certificate.

The proof obligations can remain small even when the scientific evidence supporting the declarations is rich and partly external.

## 12.2 Transfer across model versions

Full refitting from governed root evidence gives a clean baseline.

Many systems need more economical transfer.

A future theory should classify when a posterior, sufficient statistic, sample bag, variational state, or learned representation from $M_0$ can be transported into $M_1$, what proposition the transport preserves, and how evidence status changes.

This is a natural meeting point with *Certifiable State Under Information Loss*.

## 12.3 Approximate commutation

Chunked-versus-batch diagnostics can be made quantitative.

Given an approximation operator $A$, compare
$$
A\bigl(\operatorname{Bayes}(X_1\cup X_2)\bigr)
$$
with
$$
A\bigl(
\operatorname{Bayes}(X_2;
A(\operatorname{Bayes}(X_1)))
\bigr).
$$
A divergence between the two measures process dependence introduced by the approximation schedule under a fixed test model. General bounds would depend on the approximation family and regularity conditions.

## 12.4 PPL semantics across program versions

Probabilistic-programming semantics are mature inside programs.

A semantics of **program-version transition** could distinguish:

- semantics-preserving refactor;
- numerical implementation change;
- reparameterization preserving the probability model;
- evidence change;
- model constitution.

Those categories matter because a source-code diff is finer in some places and coarser in others than an inferential diff.

## 12.5 Model-space totalization

A sufficiently broad declared supermodel can turn some apparent model changes into ordinary conditioning on a model index.

That raises a natural boundary question:

> How much model uncertainty can be declared inside one episode before the declaration itself becomes scientifically unreviewable or computationally unhelpful?

The answer belongs partly to model design and partly to the wider Statistical Bridge.

# 13. Conclusion

Bayesian inference is often displayed as a relation between $\theta$ and $X$:
$$
p(\theta\mid X).
$$
A fuller record adds the declared model:
$$
p_M(\theta\mid X).
$$
A governed workflow adds one more thing: the history of how $X$ and $M$ changed.

Evidence enters through conditionalization.

Model revision enters through constitution.

Those transitions already appear in mature statistical practice. Formal epistemology distinguishes the underlying kinds of change. Bayesian workflow performs both routinely. Probabilistic programming can make the first explicit inside an episode. Version control can record changes between programs. Provenance systems can carry the resulting history. Update-trail epistemology shows why posterior histories can matter for accountability.

The missing statistical object is the transition type that connects these pieces to theorem applicability.

A projected transcript that erases model identity and transition type can map a valid fixed-model history and a model-revision history to the same display. Validity is then record-undecidable in the precise sense developed here: the transcript lacks enough information to recover whether the step was conditionalization under one declaration.

A typed lineage repairs the problem with two edges:
$$
\boxed{
\mathsf{conditioning}
\qquad
\mathsf{constitution}.
}
$$
The first is the lawful interior move of Bayes under a fixed declared model.

The second establishes a new inferential episode.

Once the distinction is recorded, model revision becomes auditable while remaining fully available to the workflow. Sequential Bayes keeps its staging theorem. Approximate carriers acquire explicit schedules and continuation contracts. Distributed posteriors retain the provenance required for composition. Model checking gains a place in the lineage as evidence about a declaration. Software version history gains inferential meaning. Autonomous agents gain a record that tells them when to continue, when to reconstitute, and when the requested step lacks a derivation.

The paper therefore ends where it began: with familiar mathematics and missing paperwork.
$$
\boxed{
\textbf{Bayes' theorem needs no repair. Its workflow record needs types.}
}
$$
# References

Carpenter, Bob, Andrew Gelman, Matthew D. Hoffman, Daniel Lee, Ben Goodrich, Michael Betancourt, Marcus Brubaker, Jiqiang Guo, Peter Li, and Allen Riddell. 2017. “Stan: A Probabilistic Programming Language.” *Journal of Statistical Software* 76(1): 1–32. DOI: 10.18637/jss.v076.i01.

Gelman, Andrew, and Eric Loken. 2013. “The Garden of Forking Paths: Why Multiple Comparisons Can Be a Problem, Even When There Is No ‘Fishing Expedition’ or ‘P-Hacking’ and the Research Hypothesis Was Posited Ahead of Time.” Unpublished manuscript, Columbia University.

Gelman, Andrew, Daniel Simpson, and Michael Betancourt. 2017. “The Prior Can Often Only Be Understood in the Context of the Likelihood.” *Entropy* 19(10): 555. DOI: 10.3390/e19100555.

Gelman, Andrew, and Cosma Rohilla Shalizi. 2013. “Philosophy and the Practice of Bayesian Statistics.” *British Journal of Mathematical and Statistical Psychology* 66(1): 8–38. DOI: 10.1111/j.2044-8317.2011.02037.x.

Gelman, Andrew, Aki Vehtari, Richard McElreath, Daniel Simpson, Charles C. Margossian, Yuling Yao, Lauren Kennedy, Jonah Gabry, Paul-Christian Bürkner, Martin Modrák, and Vianey Leos Barajas. 2026. *Bayesian Workflow*. Chapman & Hall.

Glymour, Clark. 1980. *Theory and Evidence*. Princeton, NJ: Princeton University Press.

Jaynes, E. T. 2003. *Probability Theory: The Logic of Science*. Edited by G. Larry Bretthorst. Cambridge: Cambridge University Press.

Karni, Edi, and Marie-Louise Vierø. 2013. “‘Reverse Bayesianism’: A Choice-Based Theory of Growing Awareness.” *American Economic Review* 103(7): 2790–2810. DOI: 10.1257/aer.103.7.2790.

Lewis, David. 1999. “Why Conditionalize?” In *Papers in Metaphysics and Epistemology*. Cambridge: Cambridge University Press. DOI: 10.1017/CBO9780511625343.024.

McElreath, Richard. 2020. *Statistical Rethinking: A Bayesian Course with Examples in R and Stan*. 2nd ed. Boca Raton, FL: Chapman & Hall/CRC.

Minka, Thomas P. 2001. “Expectation Propagation for Approximate Bayesian Inference.” In *Proceedings of the Seventeenth Conference on Uncertainty in Artificial Intelligence*, 362–369.

Neiswanger, Willie, Chong Wang, and Eric Xing. 2014. “Asymptotically Exact, Embarrassingly Parallel MCMC.” In *Proceedings of the Thirtieth Conference on Uncertainty in Artificial Intelligence*, 623–632.

Scott, Steven L., Alexander W. Blocker, Fernando V. Bonassi, Hugh A. Chipman, Edward I. George, and Robert E. McCulloch. 2016. “Bayes and Big Data: The Consensus Monte Carlo Algorithm.” *International Journal of Management Science and Engineering Management* 11(2): 78–88. DOI: 10.1080/17509653.2016.1142191.

Stan Development Team. 2026a. “Reproducibility.” *Stan Reference Manual*, Version 2.39. Accessed 18 August 2026. https://mc-stan.org/docs/reference-manual/reproducibility.html

Stan Development Team. 2026b. “How to Diagnose and Resolve Convergence Problems.” *Stan Learning Resources*. See “Getting help” for model-file, script, and Git history guidance. Accessed 18 August 2026. https://mc-stan.org/learn-stan/diagnostics-warnings.html

Steele, Katie, and H. Orri Stefánsson. 2021. “Belief Revision for Growing Awareness.” *Mind* 130(520): 1207–1232. DOI: 10.1093/mind/fzaa056.

Stein, Dario, and Sam Staton. 2021. “Compositional Semantics for Probabilistic Programs with Exact Conditioning.” In *2021 36th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS)*, 1–13. DOI: 10.1109/LICS52264.2021.9470552.

Stilwell, Phil. 2026a. “The Evidential History of a Posterior: Update Trails, Path Integrity, and Doxastic Accountability.” Manuscript. PhilArchive record STITEF. Uploaded 9 June 2026. https://philarchive.org/rec/STITEF

Stilwell, Phil. 2026b. “Category Confidence: Framing, Ontology, and the Credence We Assign to the Question Itself.” Manuscript. PhilArchive record STICCS. https://philarchive.org/rec/STICCS

Teller, Paul. 1973. “Conditionalization and Observation.” *Synthese* 26(2): 218–258. DOI: 10.1007/BF00873264.

van Fraassen, Bas C. 1984. “Belief and the Will.” *The Journal of Philosophy* 81(5): 235–256.

W3C. 2013. *PROV-DM: The PROV Data Model*. W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-dm/

Wang, Huayin. 2026a. *The Statistical Bridge: From Governed Evidence to Inference Certificates and Licensed Claims*. Version 3.0. Zenodo. DOI: 10.5281/zenodo.21979821.

Wang, Huayin. 2026b. *Certifiable State Under Information Loss: Governed Derivability, Claim Transport, and Approximate Closure*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21972541.

Wang, Huayin. 2026c. *Reading Bayesian Workflow Through the Statistical Bridge: Loop, Tangle, and Warrant in Statistical Practice*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21983508.

Wang, Huayin. 2026d. *Where Does Probability Live? The Statistical Bridge and the Frequentist-Bayesian Divide*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21977942.

Wang, Huayin. 2026e. *Reading Statistical Rethinking Through the Statistical Bridge: Assumption, Inference, and the Typed Architecture of Statistical Practice*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21998564.

Wenmackers, Sylvia, and Jan-Willem Romeijn. 2016. “New Theory About Old Evidence.” *Synthese* 193(4): 1225–1250. DOI: 10.1007/s11229-014-0632-x.

---

## Publication note

**Version 1.0.** Publication version.

**DOI:** **10.5281/zenodo.22010143**

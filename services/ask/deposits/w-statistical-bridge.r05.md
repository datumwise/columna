---
title: "The Statistical Bridge"
subtitle: "From Governed Evidence to Inference Certificates and Licensed Claims"
author: "Huayin Wang"
date: "Version 3.0 - 17 August 2026"
lang: en-US
papersize: letter
geometry: margin=1in
fontsize: 11pt
subject: "A governed architecture for statistical practice"
doi: "10.5281/zenodo.21979821"
version: "3.0"
license: "CC BY 4.0"
keywords:
  - statistical bridge
  - Theory of Data
  - evidence
  - target
  - event
  - spine
  - probability source
  - inference certificate
  - claim license
  - regime
  - evidence status
  - executable generative model
  - statistical practice
---

**datumwise, an independent open-source research project**

**Version 3.0 — 17 August 2026**  
**DOI:** 10.5281/zenodo.21979821  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

This version supersedes *The Statistical Bridge*, Version 2.0, DOI **10.5281/zenodo.21966764**. It preserves the Version 2 event–spine foundation and Theory-of-Data Version 6 alignment while incorporating later results on probability source, inference certificates, claim licensing, evidential status, and executable forward accounts.

# Abstract

A business asks for average revenue per active customer this quarter, with a standard error. The analyst has login events, transaction events, customer identifiers, and a familiar formula. Every arithmetic step can be correct while the analysis has not established what one customer-quarter point is, which points belong to the target, whether no recorded transaction means zero or incomplete coverage, what supplies probability, what formal statement carries inferential authority, or what the reported result is entitled to mean beyond the completed quarter.

The difficulty is not inside the formula. It lies in the governed passage by which operational material becomes statistical evidence, evidence bears on a formal target, formal machinery derives an inferential result, and that result returns as a bounded claim about the world. This passage is the **Statistical Bridge**.

The framework has two scopes. Broadly, the Statistical Bridge is the governed interface among application, empirical evidence, formal target, inference, and interpretation. Narrowly, one recurring structural center is the regime-qualified relation

\[
E^{(r)}
\rightleftarrows
S^{(r)},
\]

between realized event-side evidence and independently established spine-side targets. Event and spine are recurring existence forms under Theory of Data Version 6: event points are occurrence-established, while spine points exist independently under a declared or generated existence law. They provide the geometry of a possible crossing, not its evidential warrant.

Version 3 makes the bridge's middle and return layers more explicit. A statistical analysis must distinguish **bridge constitution**, **probability source**, **inference certificate**, and **claim license**. Probability sources may be evidence-side, governing how possible evidence could arise, or target-side, placing probability over target-side unknowns. An inference certificate is the formal statement or guarantee carrying inferential authority under the declared sources. A claim license bounds what that certificate may mean over population, time, regime, transport, and sensitivity. These are logical obligations rather than chronological stages; one declaration may discharge several, and later diagnostics may reopen earlier ones.

The framework also separates mathematical role from evidential standing: components can coexist inside one statistical construction while having very different warrant. Where possible, the forward evidence-production account should be executable, strengthening internal reviewability without proving large-world truth.

The resulting thesis is compact:

> **Statistical analysis is the governed work of making evidence bear on a target, making the warrant inspectable, and bounding what the resulting claim may mean.**

# Scope and contribution

This paper proposes a conceptual architecture of statistical practice. It introduces no estimator, theorem, or identification result, and does not claim that established statistical fields lack bridges. Survey sampling, experimental design, missing-data theory, stochastic-process theory, regression, prediction, Bayesian analysis, causal inference, and domain expertise already supply rigorous local structures.

The contribution is organizational and data-foundational. Real analyses enter those fields only after substantial work has fixed units, populations, eligibility, values, support, observation, recording, and transformations. Theory of Data Version 6 supplies the substrate for making that layer explicit through universes, anchors, measure families, eligibility, observation, support, sufficient state, provenance, and governed transformation.

The Statistical Bridge adds a neighboring qualification, **regime**, for the arrangement under which values arise, and distinguishes two scopes. Broadly, it is the governed interface among application, evidence, formal target, inference, and interpretation. Narrowly, the event–spine relation

\[
E^{(r)}
\rightleftarrows
S^{(r)}
\]

is one recurring geometry of evidence and target.

Version 3 is an architectural completion of Version 2. It preserves the event–spine foundation, Theory-of-Data alignment, cross-universe distinction, five failures, and nonchronological review logic while making explicit where probability enters, what carries inferential authority, how premise warrant differs, and how final claim scope is bounded.

# Architecture at a glance

The Statistical Bridge can be reviewed through a compact set of typed questions.

| Review question | Statistical Bridge object |
|---|---|
| What empirical points exist, and why? | universe / existence law |
| At what analytical location are they organized? | anchor |
| What realized material counts as evidence? | governed evidence object |
| How could possible evidence arise? | forward evidence-production account |
| Where does probability enter, if anywhere? | evidence-side and/or target-side probability source |
| Why does the evidence bear on this target? | target relation / identification argument |
| What formal statement carries inferential authority? | inference certificate |
| What is the evidential standing of material premises? | evidence status |
| What may the certificate legitimately mean in the world? | claim license |

The corresponding broad geography is:

\[
\text{operational world}
\overset{\mathcal K}{\longrightarrow}
E^{(r)}
\underset{\mathcal I}{\overset{\mathcal G}{\rightleftarrows}}
S^{(r)}
\overset{\mathcal J}{\longrightarrow}
\text{world claim}.
\]

The four central obligations are:

\[
\boxed{
\text{Bridge Constitution}
\rightarrow
\text{Probability Source}
\rightarrow
\text{Inference Certificate}
\rightarrow
\text{Claim License}.
}
\]

The diagram is **geography**; the four-part sequence is an **obligation list**. They are complementary, not rival decompositions. Obligations may be discharged together, revisited, or reopened as inquiry proceeds.

# 1. A familiar analysis before statistics begins

Consider again a routine request:

> What is average revenue per active customer this quarter, with a standard error?

Suppose the analyst has a login-event table, a transaction-event table, a customer-account table, imperfectly shared identifiers, timestamps, amounts, and status fields.

A familiar implementation is immediate:

1. define *active* as at least one recorded login during the quarter;
2. aggregate transaction amounts by customer;
3. join the tables;
4. compute the mean;
5. report

\[
\bar r
\pm
1.96\frac{s}{\sqrt n}.
\]

The SQL can be correct. The join can be deterministic. The mean can be exactly the mean of the surviving rows. The standard-error formula can be algebraically correct.

The statistical analysis can still be wrong.

## 1.1 What is one point?

“Active customer this quarter” does not state the analytical point.

The point might be:

- Customer;
- Account;
- CustomerQuarter;
- AccountQuarter;
- a person-quarter formed from several account identities;
- or an event-defined unit that exists only because an activity record occurred.

These are not interchangeable descriptions of the same table. They are different analytical objects.

## 1.2 Which points exist?

Suppose a customer had no transaction.

Did the customer-quarter point exist with Revenue \(=0\)?

Did it exist but Revenue was unobserved?

Was the customer ineligible?

Did the transaction pipeline miss qualifying records?

Did a join remove the row?

The absence of a row cannot decide among these states.

## 1.3 What supplies probability?

Suppose the 10,000 observed revenues vary substantially.

Variation is not itself a probability source.

If those 10,000 points are the complete finite target for the completed quarter and revenue is completely captured, the mean is determined. No repeated-sampling uncertainty is created merely because individual revenues differ.

The same table could instead represent:

- a probability sample from a larger finite population;
- one realization from a stochastic customer process;
- a noisy observation of latent revenue;
- a period used to predict future periods;
- or a partially captured event stream.

Those are different bridges.

## 1.4 What does the interval certify?

Even after a probability source is declared, an interval must be typed. Confidence, credible, predictive, and bootstrap intervals carry different guarantee semantics. A numerical interval is not its own inferential meaning.

## 1.5 What may the result claim?

A result about registered account-quarter points in a completed quarter does not become a statement about:

- customers rather than accounts;
- future quarters;
- latent customer engagement;
- a stable revenue-generating mechanism;
- causal effects of an intervention;
- or another geography or population

merely because the displayed statistic has a familiar name.

The statistical problem begins before the estimator and continues after it.

# 2. The bridge practitioners already use

Statistical practice is precedent-based.

Analysts learn recurring structures: one row per unit, samples from populations, repeated measurements, treatment and control arms, time-at-risk with failures, likelihoods and parameters, posteriors and predictions.

A new problem is recognized as resembling a familiar case:

\[
\text{new problem}
\overset{\text{resembles}}{\longrightarrow}
\text{familiar statistical structure}
\longrightarrow
\text{standard method}.
\]

This is indispensable. Statistical practice cannot be rebuilt from first principles for every analysis.

But the visible method travels more easily than the conditions that made it valid.

A precedent silently carries:

\[
\begin{aligned}
&\text{question}
+\text{target}
+\text{anchor}
+\text{universe}
+\text{evidence object}
+\text{observation structure}\\
&+\text{forward account}
+\text{probability source}
+\text{target relation}
+\text{method conditions}
+\text{claim scope}.
\end{aligned}
\]

A warehouse table can resemble a textbook sample while lacking almost every supporting condition.

The rows may be recorded events rather than target units.

Population membership may depend on having been observed.

Inclusion may be opportunistic rather than randomized.

Values may be aggregates over incomplete streams.

A formal method can remain familiar while the bridge has changed.

This gives a portability principle:

> **A statistical precedent is portable only to the extent that its bridge structure is portable.**

The Statistical Bridge does not replace precedent. It makes enough of its hidden structure explicit that precedent can be reused more safely.

# 3. The broad bridge and the narrow event–spine center

The broad architecture can be written:

\[
\text{operational world}
\overset{\mathcal K}{\longrightarrow}
E^{(r)}
\underset{\mathcal I}{\overset{\mathcal G}{\rightleftarrows}}
S^{(r)}
\overset{\mathcal J}{\longrightarrow}
\text{world claim}.
\]

Here \(\mathcal K\) constitutes governed empirical objects; \(\mathcal G\) supplies the forward evidence-production account; \(S^{(r)}\) may also carry a target-side law such as \(\pi(S)\); \(\mathcal I\) carries reverse inferential reasoning; and \(\mathcal J\) bounds interpretation. As summarized above, the diagram is geography and the four-part architecture is the obligation list.

These are not mathematical inverses or a mandatory workflow. Inquiry may begin from model, evidence, or target, and failed checks can reopen earlier obligations. The diagram is a map of obligations, not a conveyor belt.

## 3.1 The narrow center

For many practical analyses, a recurring structural center is:

\[
E^{(r)}
\rightleftarrows
S^{(r)}.
\]

An **event universe** is occurrence-established. Its governed points exist because recorded occurrences exist.

Examples include:

- recorded purchases;
- recorded failures;
- completed calls;
- detected visits;
- produced measurements.

A **spine universe** has points established independently of a particular observed event value.

Examples include:

- registered account-quarters;
- scheduled patient visits;
- finite-population frame units;
- person-time exposure locations;
- trading days;
- future forecast dates.

The mnemonic remains useful:

> **Events generate points. Spines establish points and await values.**

But event and spine are existence forms, not the whole Theory-of-Data universe ontology.

## 3.2 Geometry is not warrant

Shared anchor coordinates do not create an evidential relation.

Two datasets may both be indexed by PersonDay and have no statistical connection.

The event–spine geometry supplies a place for a crossing.

A warranted bridge additionally requires:

- lawful attribution;
- a forward evidence-production account;
- a target relation or identification argument;
- probability where required;
- assumptions adequate for the claim;
- and appropriate observation/evidence conditions.

# 4. Constituting evidence and targets

Formal statistics often begins with objects such as

\[
X_1,\ldots,X_n,
\qquad
P_\theta,
\qquad
\tau,
\qquad
\widehat\tau.
\]

Operational work begins earlier.

It begins with:

- event logs;
- registries;
- schedules;
- identity systems;
- instruments;
- validity intervals;
- timestamps;
- joins;
- exclusions;
- deduplication;
- transformations;
- partial recording.

The point of Theory of Data is not to rename rows and columns.

It is to preserve the analytical identity of the objects that those operational artifacts are being asked to establish.

## 4.1 Existence

A target population must exist under some law.

A registered account-quarter can exist because an account was valid and eligible during a calendar quarter.

A scheduled visit can exist because a protocol and schedule establish it.

A purchase event can exist because a qualifying purchase was recorded.

Those are different existence laws.

## 4.2 Eligibility

Existence does not imply measure eligibility: a patient-visit can exist while an assay is not required, or a customer-quarter while a product-specific measure is inapplicable.

## 4.3 Observation and support

Eligibility does not imply observation. An eligible assay may be missing, a recorded transaction may lack an attribute, or a respondent may omit an item. Support therefore needs its own contract.

## 4.4 Within-universe transformation versus cross-universe construction

Theory-of-Data reducers move a measure family lawfully from a finer to a coarser anchor within a governed family when sufficient state and reducer law exist.

A statistical bridge may require something else.

Event-side state can be lawfully summarized first, but establishing a measure on an independently existing spine is a cross-universe attribution or construction.

That crossing must state its own contract.

For revenue:

\[
\text{TransactionAmount@Transaction}
\]

and

\[
\text{Revenue@AccountQuarter}
\]

are not the same measure at different groupings merely because one can be calculated from the other.

The latter requires a law saying which transactions belong to which account-quarter points, which statuses count, how refunds enter, what complete capture means, and what an empty qualifying event fiber means.

# 5. Forward evidence-production accounts

The bridge also needs an account of how evidence like the realized evidence could arise relative to target-side structure.

Schematically:

\[
S^{(r)}
\overset{\mathcal G}{\longrightarrow}
E_{\mathrm{possible}}^{(r)}.
\]

The umbrella term **forward evidence-production account** may include:

- physical occurrence;
- randomized sampling;
- randomized assignment;
- stochastic value generation;
- measurement;
- detection;
- recording;
- response;
- missingness;
- selection;
- censoring;
- prediction.

These components should not be collapsed when the analysis depends on their difference.

## 5.1 Occurrence, recording, and value observation

A useful decomposition is:

\[
\text{occurrence or selection}
\neq
\text{recording}
\neq
\text{value observation}.
\]

A transaction can occur but fail to reach the ledger; a recorded transaction can lack an amount; a sampled unit can respond but omit an item. A null value or absent row cannot decide which layer failed.

## 5.2 Declarative and executable forward accounts

A forward account can be merely declarative:

> under this design/model/mechanism, evidence would arise according to these rules.

Where possible, it can also be executable.

A simulator or generative program can produce synthetic evidence under the declared account. McElreath's current workflow is a concrete pedagogical example of treating synthetic simulation and predictive checking as first-class review artifacts rather than afterthoughts (McElreath 2024).

The simulator is itself a typed bridge component. It carries an **implementation-fidelity premise**: the code must actually implement the declared forward account. That premise can often be checked mechanically or by synthetic recovery, but executability should not collapse the semantic account and its implementation into one object.

That makes additional checks possible.

### Prior-predictive review

If a target-side prior and evidence-side likelihood are declared, simulate their joint implications before fitting.

This can expose unintended implications of the declared construction.

### Synthetic-data recovery

Generate data under known settings, run the intended analysis, and ask whether the procedure recovers what was planted. Simulation-based calibration is one formal example of this general validation idea for Bayesian algorithms (Talts et al. 2018), while McElreath's developing workflow emphasizes synthetic-data simulation and validation as routine analytical quality assurance (McElreath 2024).

This can detect implementation errors, weak identification, estimator/estimand mismatch, numerical pathology, or unintended parameterization.

### Posterior-predictive or fitted-model checks

Generate replicated evidence under a fitted model and compare selected discrepancies with realized evidence (Gelman, Meng, and Stern 1996).

This may reveal model failure.

Passing does not prove the model true.

### Sensitivity experiments

Vary uncertain assumptions and examine which claims remain stable.

The key principle is:

\[
\boxed{
\text{executable forward account}
\Rightarrow
\text{stronger internal reviewability}.
}
\]

But:

\[
\boxed{
\text{internal reviewability}
\not\Rightarrow
\text{large-world truth}.
}
\]

Simulation can test machinery under the declared small world.

It cannot manufacture evidence that the small world is scientifically adequate.

# 6. Probability source, inference certificate, and claim license

The most important addition in Version 3 is to separate three objects that statistical language often compresses.

\[
\boxed{
\text{probability source}
\neq
\text{inference certificate}
\neq
\text{claim license}.
}
\]

## 6.1 Ask first whether probability is needed

Before choosing any inferential method, ask:

> Is the requested target already exhausted by deterministic constitution of complete realized evidence?

If yes, probability may be unnecessary.

For a completed finite population with complete capture, the finite mean

\[
\bar y
=
\frac{1}{N}
\sum_{i=1}^N y_i
\]

can be known exactly.

Variation among the \(y_i\) does not create repeated-sampling uncertainty about that finite mean.

Therefore:

\[
\boxed{
\text{variation}
\neq
\text{probability source}.
}
\]

and:

\[
\boxed{
\text{variation}
\neq
\text{need for inference}.
}
\]

## 6.2 Evidence-side probability sources

An evidence-side source governs how possible evidence arises.

Examples:

- simple random sampling;
- cluster or stratified sampling;
- treatment randomization;
- measurement error;
- stochastic process evolution;
- missingness or response;
- a predictive model over future observations.

Write schematically:

\[
P_E(\cdot\mid S,\Gamma,r).
\]

This is not necessarily a likelihood in a Bayesian model. It is the broader role of a probability law on possible evidence.

## 6.3 Target-side probability sources

A target-side probability source places probability directly over target-side unknowns.

The canonical Bayesian example is:

\[
\pi(\theta).
\]

Hierarchical laws over latent or unit-level quantities can also play this role.

A target-side source is optional. Its presence is a structural choice, not something forced by empirical variation.

## 6.4 Inference certificate

An inference certificate is the formal statement or guarantee carrying inferential authority under the declared bridge and probability source.

Examples include:

### Frequentist coverage

\[
P_\theta\{\theta\in C(X)\}
\ge
1-\alpha.
\]

### Bayesian posterior probability

\[
P(\theta\in B\mid Y=y).
\]

### Likelihoodist comparative support

A likelihood ratio comparing specified hypotheses, as in the likelihood paradigm (Royall 1997).

### Confidence-distribution, inferential-model, fiducial, or betting certificates

These use different formal objects and guarantee semantics (Hannig 2009; Martin and Liu 2013; Xie and Singh 2013; Ramdas et al. 2023).

The point is not to classify all inference.

It is to prevent one mistake:

> **the certificate does not create the probability source that makes it meaningful.**

## 6.5 Same evidence, different sources, different certificates

The distinction between realized evidence, probability source, and certificate is easiest to see when the evidence object is held fixed.

Suppose the same realized vector is:

\[
y=(y_1,\ldots,y_n).
\]

Under a random-sampling design, the probability source may be:

\[
P_D(S=s),
\]

and a frequentist confidence procedure can certify:

\[
P_D\{\tau\in C(Y_S)\}\ge 1-\alpha.
\]

Under a Bayesian joint construction using the same realized values,

\[
p(y\mid\theta)\pi(\theta),
\]

the target-side source \(\pi(\theta)\) and evidence-side source \(p(y\mid\theta)\) support a posterior certificate such as:

\[
P(\theta\in B\mid y).
\]

The realized values can be identical while the inferential authority differs because the probability sources and certificate semantics differ.

\[
\boxed{
\text{same realized evidence}
\not\Rightarrow
\text{same probability source}
\not\Rightarrow
\text{same inference certificate}.
}
\]

## 6.6 Certificate basis is open-typed

Frequentist operating behavior and Bayesian conditional target-side probability are historically dominant certificate forms, not the definition of inference. The architecture must also accommodate likelihoodist evidence, confidence distributions, generalized fiducial constructions, inferential models, e-values/e-processes, predictive guarantees, and multi-certificate analyses.

## 6.7 Claim license

A formal certificate does not carry unlimited empirical meaning.

A practical claim-license review asks at least:

1. **Population** — which governed population or target domain is supported?
2. **Time** — what period or forecasting horizon is licensed?
3. **Regime** — under which value-generation arrangement does the claim hold?
4. **Transport** — what argument permits movement to another population, setting, policy, or future condition?
5. **Sensitivity** — which uncertain bridge premises materially control the conclusion?

This is a review surface, not yet a complete logic of scientific claims.

It makes explicit a central non-implication:

\[
\boxed{
\text{formal uncertainty statement}
\not\Rightarrow
\text{world-facing claim}.
}
\]

# 7. Regime, identification, and causal passage

Regime answers a different question from universe or anchor.

Universe says which root points exist.

Anchor says how those points are partitioned.

Regime says under what arrangement values arise.

A regime-local bridge is:

\[
E^{(r)}
\rightleftarrows
S^{(r)}.
\]

A causal or policy question may require another passage:

\[
S^{(r)}
\longrightarrow
S^{(r')}.
\]

This is not itself the event–spine crossing.

It is a cross-regime relation.

## 7.1 Identification assumptions remain obligations

Consider two causal workflows.

### Identify then estimate

\[
\text{graph / structural assumptions}
\rightarrow
\text{identified estimand}
\rightarrow
\text{estimation}.
\]

The identification assumptions remain visibly outside the estimator; graphical identification and intervention calculus make this separation explicit in structural causal models (Pearl 2009).

### Joint probabilistic modeling

A large causal system may instead be encoded into one joint probability model, from which intervention or counterfactual quantities are simulated.

This may be elegant and computationally unified.

But representing a premise inside probability syntax does not supply evidence for it.

A causal graph can be wrong while the posterior is numerically excellent.

An invariance assumption can be false while MCMC converges perfectly.

Therefore:

\[
\boxed{
\text{probabilistic representation of a bridge premise}
\not\Rightarrow
\text{evidential discharge of that premise}.
}
\]

The paradigm question and the identification question are orthogonal.

## 7.2 Regime, identification, certificate, and license

For causal claims, four obligations should remain separate:

\[
\text{regime contrast}
\rightarrow
\text{identification premises}
\rightarrow
\text{inference certificate}
\rightarrow
\text{claim license}.
\]

Suppose evidence is observed under regime \(r\), while the intended claim concerns an intervention regime \(r'\). A model can estimate associations under \(r\) very precisely. To license a claim about \(r'\), the analysis needs an identification argument connecting the observed regime to the intervention target. Even after identification succeeds, transport to another hospital, population, year, or policy environment is an additional claim-license question.

Therefore:

\[
\boxed{
\text{estimation}
\neq
\text{identification}
\neq
\text{transport}.
}
\]

Precision at one stage cannot substitute for a missing obligation at another.

# 8. Evidence status and inspectable warrant

A single statistical model can contain components with very different evidential standing.

For example:

| Component | Bridge role | Possible evidential basis |
|---|---|---|
| randomized assignment | evidence-side source | instituted / verified |
| sampling frame | target premise | externally governed / verified |
| measurement model | evidence-side source | corroborated / assumed |
| prior | target-side source | elicited / assumed / empirically informed |
| causal graph | identification premise | argued / corroborated |
| invariance assumption | transport premise | assumed / corroborated |
| posterior or confidence statement | inference certificate | derived conditionally on premises |

The categories are illustrative; mathematical co-location does not imply equal evidential standing.

\[
\boxed{
\text{same joint model}
\not\Rightarrow
\text{same warrant}.
}
\]

Evidential status is also **dynamic**, but not freely so. Re-expression, transformation, or probabilistic encoding does not by itself upgrade a premise. A status may strengthen only when an explicit evidence-producing event supplies new warrant—for example, a validation study, design verification, calibration check, external measurement, or other governed evidence event. This is the dynamic form of the same rule used in causal modeling: putting an assumption into a joint distribution changes representation, not evidential standing.

The three formulations in this paper—mathematical co-location does not equalize warrant, probabilistic representation does not discharge a premise, and re-representation does not upgrade status—are instances of one principle that may be called **representation-invariance of warrant**: how a premise is written down does not by itself change the evidence for it.

The corpus uses evidence statuses including:

- verified;
- corroborated;
- assumed;
- unidentifiable;
- contradicted.

They should not be forced into one universal total ladder; ordering and combination depend on the evidence calculus and claim.

## 8.1 Inference certificate versus certificate witness

The Statistical Bridge uses **inference certificate** for the proposition or guarantee carrying inferential authority.

The companion paper *Certifiable State Under Information Loss* uses **certificate** for a proof-relevant witness establishing a claim from governed state, contracts, and evidence:

\[
Cert
=
(c,\delta,gr(\delta)).
\]

The two levels are compatible.

SB asks:

> What formal claim carries inferential force?

Certifiable State asks:

> What derivation and evidence entitle the system to emit that claim?

This gives a useful layering:

\[
\text{bridge premises}
\rightarrow
\text{inference-certificate proposition}
\rightarrow
\text{certificate witness and evidence status}
\rightarrow
\text{claim license}.
\]

## 8.2 Warrant is not informativeness

A statistically valid certificate can be weak.

A very wide interval can be perfectly warranted.

A posterior may be coherent but diffuse.

A sensitivity analysis may show that only a weak conclusion survives.

Therefore:

\[
\boxed{
\text{evidential warrant}
\neq
\text{claim informativeness}.
}
\]

Version 2 used *carrying capacity* as a useful qualitative metaphor for how much a bridge could bear.

Version 3 types that idea more carefully.

A bridge does not have one scalar capacity.

It supports a family of claims under particular premises, evidence statuses, and informativeness levels.

# 9. Five recurrent bridge failures

The five Version 2 failures remain useful.

Version 3 keeps them and locates them more precisely.

## 9.1 Wrong target

The analysis answers a different target from the one the practical question requires.

Examples include event mean instead of customer mean, account effect instead of person effect, or current-period target instead of future target. This is primarily a target-constitution and claim-license failure.

## 9.2 Collapsed population

Observed rows silently become the target population.

Examples include transacting customers becoming all eligible customers, complete cases becoming the population, or recorded failures becoming all units at risk. This is primarily an existence/eligibility/universe failure.

## 9.3 Unlicensed attribution

Evidence is moved to another analytical object without a lawful relation.

Examples include accounts mapped to customers without identity rules, events assigned to exposure periods without attribution law, or shared coordinates treated as evidential connection. This is primarily a cross-universe bridge failure.

## 9.4 Missing evidence-production account

A target and evidence are co-located, but no account explains how the evidence could arise relative to the target or why it bears on the claim.

This is primarily a forward-account and probability-source failure.

A standard error calculated from row variation in a census is a common example.

### Certificate/source confusion

A related sub-failure occurs when a familiar formal object—posterior, interval, p-value, bootstrap distribution—is treated as if its presence supplied the probability source that would make it meaningful.

It does not.

## 9.5 Claim overreach

A valid result is transported beyond its home without additional warrant.

Examples:

- one completed quarter becomes future expectation;
- association becomes intervention effect;
- one population becomes another;
- account-level evidence becomes customer-level law;
- a fitted relationship becomes mechanistic explanation.

This is primarily a claim-license and transport failure.

### Evidence-status flattening

A cross-cutting sub-failure occurs when assumed, instituted, corroborated, and verified premises are represented as though they had equal status.

It is discussed here because it often manifests as overclaimed warrant, but it can contribute to any of the five top-level failures—for example by hiding a weak population premise, attribution rule, observation model, or transport assumption.

That can make a mathematically unified model look epistemically more unified than it is.

# 10. Reconstructing the customer-revenue analysis

The running example can now be rebuilt with the expanded typing.

## 10.1 State the target

Choose:

> Mean net Revenue over all registered account-quarter points that were eligible during the completed quarter.

Let the target spine be:

\[
P_S
=
\{
(a,q):
a
\text{ is registered and eligible during }
q
\}.
\]

The bridge anchor is:

\[
A_B
=
\{\text{Account},\text{Quarter}\}.
\]

## 10.2 Identify evidence

Login events occupy a recorded event universe.

Transaction events occupy another.

Their occurrence is distinct from:

- recording completeness;
- value observation;
- status eligibility;
- downstream transformation.

Neither event universe is yet the target population.

## 10.3 Construct revenue lawfully

Transaction events can be summarized within the event universe to account-quarter fibers, retaining whatever sufficient state the Revenue family requires:

\[
\eta_T(E_{a,q})
=
(
gross,
refunds,
chargebacks,
count,
coverage\ evidence
).
\]

A cross-universe contract then determines whether that event-side evidence establishes:

\[
Revenue@AccountQuarter
\]

on the independent spine.

For a complete descriptive calculation, the contract may require:

- complete capture of qualifying transactions;
- lawful attribution to eligible account-quarter points;
- a declared Revenue law for refunds and corrections;
- an empty event fiber under complete capture to mean zero;
- retained evidence sufficient to certify those conditions.

If those conditions hold, Revenue can be established deterministically for the complete spine.

## 10.4 Evidence status in the running example

The same reconstructed analysis can contain premises with different evidential standing.

| Premise or component | Illustrative evidential status |
|---|---|
| account registry and eligibility rules | verified against governed source |
| quarter boundaries | verified |
| transaction-to-account attribution code | mechanically verified |
| transaction capture completeness | corroborated, but not necessarily verified |
| zero from an empty qualifying event fiber | valid only conditional on capture completeness |
| future-quarter stability | assumed |
| causal effect of customer engagement | unidentifiable from this descriptive bridge |

This table is not a universal hierarchy.

Its purpose is to prevent one verified component from silently upgrading another. Verified attribution code does not verify transaction completeness. A valid zero rule does not become warranted unless the condition that licenses it has adequate evidence. Re-encoding any of these premises inside a model changes representation, not warrant.

## 10.5 No probability required

The finite target mean is:

\[
\tau_{\mathrm{all}}
=
\frac{1}{|P_S|}
\sum_{(a,q)\in P_S}
r(a,q).
\]

If the spine and values are complete, this quantity is determined.

No standard error is required to describe uncertainty about the finite total or mean.

The appropriate answer to:

> Which inferential school should we use?

is:

> **Neither yet. What is uncertain?**

## 10.6 When probability enters

Suppose instead the question is:

> What does this quarter tell us about revenue in future quarters under a stable continuation process?

Now a probability source is needed.

An evidence-side source might be a stochastic time-series or hierarchical model for future account-quarter revenue.

A target-side source may or may not also be declared.

The resulting certificate might be:

- a frequentist prediction guarantee;
- a Bayesian posterior predictive distribution;
- another predictive certificate.

The certificate then needs a claim license over:

- future time;
- population continuity;
- regime stability;
- structural assumptions;
- sensitivity to model choice.

The same observed table has become a different statistical problem.

## 10.7 From certificate to licensed and over-reaching claims

Assume the completed-quarter constitution is valid and yields the exact finite-population mean \(\tau_{\mathrm{all}}\).

A directly licensed statement is:

> Mean net revenue over all eligible registered account-quarter points in the completed quarter was \(\tau_{\mathrm{all}}\).

A partially licensed extension is:

> This quarter is informative about expected revenue next quarter.

That statement requires a new bridge: a future-time probability source plus assumptions about population continuity, regime stability, and transport over time.

An over-reaching statement would be:

> Customer engagement causes approximately \(\tau_{\mathrm{all}}\) in quarterly revenue.

Nothing in the descriptive certificate establishes a causal target, customer-level identity rather than account-level identity, an intervention regime, or the identification premises needed for such a claim.

The certificate has not changed.

The claim has.

That is exactly why claim license is a separate obligation.

# 11. A revised review discipline

The following is a **review order**, not a mandated discovery workflow.

## 11.1 State the target and intended claim

What formal object is requested?

What practical or scientific claim is ultimately intended?

Is the request descriptive, inferential, predictive, causal, decision-oriented, or mixed?

## 11.2 Establish target universe and anchor

What points exist?

Why do they exist?

How are they partitioned into analytical locations?

Do not let observed rows silently become the target unless occurrence itself defines the target.

## 11.3 Identify evidence in its native role

What records, measurements, events, assignments, registrations, or responses actually entered? Distinguish occurrence, recording, eligibility, observation, and support.

## 11.4 Expose data movement to the bridge

Show within-universe transformations.

Show cross-universe attribution separately.

State reducer laws and sufficient state where ToD reduction is involved.

## 11.5 State the forward evidence-production account

How could evidence like this arise relative to target-side structure? Separate occurrence, selection, assignment, measurement, recording, response, and missingness where the distinction matters.

## 11.6 Type the probability source

Is probability needed?

If yes, where does it enter?

Evidence-side?

Target-side?

Both?

Do not infer a probability source from empirical variation.

## 11.7 State the target relation or identification argument

Why does the evidence bear on this target?

For causal or transport claims, what additional identification or invariance relation is required?

## 11.8 State the inference certificate

What exact formal statement carries inferential authority?

Coverage?

Posterior probability?

Likelihood support?

Predictive guarantee?

E-value?

Other?

## 11.9 Record material evidential status

Which bridge premises are instituted, verified, corroborated, assumed, unidentifiable, or contradicted? Do not flatten them into one category called “the model.”

## 11.10 Import formal results with conditions

Theorem assumptions are part of the bridge.

A familiar formula does not carry its empirical applicability automatically.

## 11.11 Bound the claim license

Ask:

- population?
- time?
- regime?
- transport?
- sensitivity?

## 11.12 Execute and criticize the forward account where possible

This activity is listed last for readability, but it should be treated as **cross-cutting from Step 5 onward**, not postponed until a certificate has already been trusted.

Simulate.

Run recovery checks.

Inspect prior implications.

Perform fitted-model criticism.

Vary uncertain assumptions.

If these checks expose a broken forward account, simulator, source declaration, or estimator, return to the earlier obligation immediately.

Treat success as stronger internal reviewability, not as proof of large-world truth.

# 12. Consequences for statistical practice and software

## 12.1 Data engineering and statistics are adjacent, not identical

Data engineering can lawfully establish analytical objects without statistical inference. The boundary is not SQL versus mathematics; it is whether the claim requires warrant beyond deterministic constitution of realized records.

## 12.2 A finished table is not a primitive statistical object

A matrix can hide unit decisions, exclusions, joins, event-to-spine mappings, missingness, coverage, support, and transformed identities. Software that receives only the matrix cannot recover those contracts by inspection.

## 12.3 Computational correctness is not bridge validity

An algorithm can correctly realize its intended certificate while the bridge is wrong:

\[
\boxed{
\text{computational convergence}
\neq
\text{inferential validity}
\neq
\text{bridge validity}.
}
\]

A bootstrap can converge to the wrong resampling target, an optimizer can fit the wrong likelihood perfectly, and a standard-error routine can compute a quantity with no declared sampling interpretation.

## 12.4 Statistical systems should store more than methods

A serious analytical system should make recoverable the target, universe, anchor, evidence, data lineage, cross-universe attribution, forward account, probability source(s), target relation, inference certificate, material evidence statuses, claim license, and sensitivity conditions. Its purpose is reviewability.

## 12.5 AI agents need the bridge more than human precedent does

Agents are especially vulnerable to choosing methods from superficial table shape. Explicit bridge structure can prevent confidence intervals over complete censuses, causal language from association-only designs, silent population collapse, zeros inferred from absent event rows, posterior interpretation with an unexamined observation model, and generalization beyond the declared claim license.

# 13. Relationship to established statistical fields

The Statistical Bridge does not replace statistical theory; it exposes the governed interfaces through which local theories become empirically applicable.

## 13.1 Survey sampling

Sampling theory already supplies target populations, inclusion laws, probability sources, and estimators (Neyman 1934). The bridge asks whether the operational frame and values actually instantiate those objects.

## 13.2 Experimental design

Randomization is an unusually strong evidence-side source because part of the probability structure is physically instituted (Fisher 1935). The bridge must still preserve assignment, eligibility, outcome observation, deviations, and claim scope.

## 13.3 Missing data

Missing-data theory supplies models and identification conditions for unobserved values (Rubin 1976). The bridge distinguishes an unobserved value at an established eligible point from absence of the point itself.

## 13.4 Point processes

Point-process theory models stochastic occurrence and random measures (Daley and Vere-Jones 2003). The bridge distinguishes modeled possible occurrence from governed event existence, detection, recording, and downstream value observation.

## 13.5 Regression and prediction

Regression supplies formal variable relations and prediction supplies target-specific performance or probability statements. Neither determines population constitution or wider claim license.

## 13.6 Bayesian analysis

Bayesian analysis combines target-side and evidence-side probability in a joint construction and derives conditional target-side certificates. Its computational uniformity is powerful; the bridge remains responsible for empirical correspondence.

## 13.7 Causal inference

Causal inference supplies identification results under causal assumptions and regime contrasts (Pearl 2009). The bridge makes source/target regimes, evidence for identification premises, and the difference between encoding and warranting those premises explicit.

# 14. Version 2 to Version 3: terminology migration

Version 3 preserves Version 2's architecture while refining terms that later work showed were carrying too much.

| Version 2 expression | Version 3 treatment |
|---|---|
| carrying capacity | licensed claim family, typed by warrant/derivability, evidence status, informativeness, and claim license |
| generation / inference | forward account plus probability source(s) / inference certificate |
| event-spine as dominant visual center | broad bridge geography presented first; event-spine retained as the narrow characteristic crossing |
| heterogeneous assumptions inside “the model” | bridge premises typed separately by role and evidential standing |
| claim overreach | retained as a top-level failure; evidence-status flattening identified as a cross-cutting sub-diagnosis |
| familiar inferential output | explicitly typed by probability source and certificate basis |
| forward evidence-production account | may be declarative or executable; executable form carries an implementation-fidelity premise |

These are refinements, not repudiations. Version 2 supplied the structure that made the Version 3 distinctions possible.

# 15. Evaluation program and open formal questions

Because the framework remains primarily conceptual, evaluation is essential.

## 15.1 Inter-analyst agreement

Give analysts the same operational problem and ask them independently to specify target universe, anchor, evidence, forward account, probability source, inference certificate, and claim license. Agreement and disagreement reveal where precedent had carried hidden assumptions.

## 15.2 Recoverability

Given a reported result, ask whether an independent reviewer can recover its population, probability source, material assumptions, certificate, and claim scope.

## 15.3 Before-and-after formulation

Compare analyses before and after explicit bridge declaration, measuring changes in target definition, missingness handling, standard-error use, causal language, population scope, and robustness checks.

## 15.4 Production failure review

Examine incidents in which data processing and formal mathematics were correct but the empirical claim was wrong, and classify the bridge failure.

## 15.5 Certificate recoverability

Ask whether a reviewer can identify the exact proposition carrying inferential authority and the probability source relative to which it is valid. “95% interval” is not enough.

## 15.6 Evidence-status agreement

Ask whether reviewers agree on which premises are instituted, verified, corroborated, assumed, or unresolved, testing whether evidential typing improves auditability.

## 15.7 Claim-license agreement

Give reviewers the same formal result and ask them to state population, time, regime, transport conditions, and sensitivity limits. Disagreement exposes interpretive ambiguity.

## 15.8 Executability of forward accounts

Ask which bridge components can be represented as runnable simulations or testable generative procedures, and what internal errors become detectable that were invisible in prose-only declarations.

## 15.9 Open formal problem

A mature future system should be able to distinguish at least:

\[
\text{claim derivability},
\qquad
\text{evidence status},
\qquad
\text{informativeness},
\qquad
\text{claim license}.
\]

The Certifiable State work formalizes part of this problem for governed transformed state.

A complete Statistical Bridge calculus remains open.

# 16. Conclusion

Statistics is often compressed into mathematics applied to data or data processing followed by a familiar formula. Both omit the governed passage that makes the formula empirically meaningful: operational material must become evidence; a target must be established; a forward account must explain possible evidence; probability, if needed, must enter from a specific source; a certificate must state inferential authority; premise warrant must remain inspectable; and the final claim must stay within its licensed population, time, regime, transport, and sensitivity scope.

The narrow event–spine relation remains a useful geometry:

\[
E^{(r)}
\rightleftarrows
S^{(r)}.
\]

But geometry is not warrant.

The broad Statistical Bridge is the governed architecture surrounding that crossing:

\[
\text{constitution}
\rightarrow
\text{evidence}
\rightleftarrows
\text{target}
\rightarrow
\text{licensed claim}.
\]

Its obligations may be discharged in different orders and revisited as inquiry proceeds.

The final principle is therefore:

\[
\boxed{
\textbf{Statistical analysis is the governed work of making evidence bear on a target,}
}
\]

\[
\boxed{
\textbf{making the warrant inspectable, and bounding what the resulting claim may mean.}
}
\]

# References

Daley, D. J., and David Vere-Jones. 2003. *An Introduction to the Theory of Point Processes, Volume I: Elementary Theory and Methods*. 2nd ed. New York: Springer. DOI: 10.1007/b97277.

Fisher, R. A. 1935. *The Design of Experiments*. Edinburgh: Oliver and Boyd.

Gelman, Andrew, Xiao-Li Meng, and Hal Stern. 1996. “Posterior Predictive Assessment of Model Fitness via Realized Discrepancies.” *Statistica Sinica* 6: 733-760.

Hannig, Jan. 2009. “On Generalized Fiducial Inference.” *Statistica Sinica* 19 (2): 491-544.

Martin, Ryan, and Chuanhai Liu. 2013. “Inferential Models: A Framework for Prior-Free Posterior Probabilistic Inference.” *Journal of the American Statistical Association* 108 (501): 301-313. DOI: 10.1080/01621459.2012.747960.

McElreath, Richard. 2024. “The Third Edition, the Dotted Half Note of Editions.” *Elements of Evolutionary Anthropology*, January 2, 2024.

Neyman, Jerzy. 1934. “On the Two Different Aspects of the Representative Method: The Method of Stratified Sampling and the Method of Purposive Selection.” *Journal of the Royal Statistical Society* 97 (4): 558-606. DOI: 10.1111/j.2397-2335.1934.tb04184.x.

Neyman, Jerzy. 1937. “Outline of a Theory of Statistical Estimation Based on the Classical Theory of Probability.” *Philosophical Transactions of the Royal Society of London. Series A* 236 (767): 333-380. DOI: 10.1098/rsta.1937.0005.

Pearl, Judea. 2009. *Causality: Models, Reasoning, and Inference*. 2nd ed. Cambridge: Cambridge University Press.

Ramdas, Aaditya, Peter Grünwald, Vladimir Vovk, and Glenn Shafer. 2023. “Game-Theoretic Statistics and Safe Anytime-Valid Inference.” *Statistical Science* 38 (4): 576-601. DOI: 10.1214/23-STS894.

Royall, Richard M. 1997. *Statistical Evidence: A Likelihood Paradigm*. New York: Chapman & Hall.

Rubin, Donald B. 1976. “Inference and Missing Data.” *Biometrika* 63 (3): 581-592. DOI: 10.1093/biomet/63.3.581.

Talts, Sean, Michael Betancourt, Daniel Simpson, Aki Vehtari, and Andrew Gelman. 2018. “Validating Bayesian Inference Algorithms with Simulation-Based Calibration.” arXiv:1804.06788.

Xie, Min-ge, and Kesar Singh. 2013. “Confidence Distribution, the Frequentist Distribution Estimator of a Parameter: A Review.” *International Statistical Review* 81 (1): 3-39. DOI: 10.1111/insr.12000.

Wang, Huayin. 2026. *The Theory of Data*. Version 6.0. Zenodo. DOI: 10.5281/zenodo.21958062.

Wang, Huayin. 2026. *The Statistical Bridge: From Events to Spines, Data Work, and the Interpretation of Results*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21966764.

Wang, Huayin. 2026. *Where Does Probability Live? The Statistical Bridge and the Frequentist-Bayesian Divide*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21977942.

Wang, Huayin. 2026. *Certifiable State Under Information Loss: Governed Derivability, Claim Transport, and Approximate Closure*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21972541.

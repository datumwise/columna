---
title: "Where Does Probability Live?"
subtitle: "The Statistical Bridge and the Frequentist-Bayesian Divide"
author: "Huayin Wang"
date: "Version 1.0 - 17 August 2026"
lang: en-US
papersize: letter
geometry: margin=1in
fontsize: 11pt
subject: "Typing the frequentist-Bayesian divide through bridge constitution, probability source, inference certificates, and claim licensing"
keywords:
  - Statistical Bridge
  - frequentist inference
  - Bayesian inference
  - probability
  - evidence
  - likelihood principle
  - de Finetti
  - Birnbaum
  - calibrated Bayes
  - fiducial inference
  - Theory of Data
  - inference certificate
  - claim license
  - MCMC
  - probabilistic programming
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
    \fancyhead[L]{\small Where Does Probability Live?}
    \fancyhead[R]{\small Huayin Wang}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \setlength{\headheight}{14pt}
  - |
    \urlstyle{same}
---

**datumwise, an independent open-source research project**

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

**DOI:** **10.5281/zenodo.21977942**

**Foundation.** This paper develops a consequence of *The Statistical Bridge: From Events to Spines, Data Work, and the Interpretation of Results*, Version 2.0, DOI **10.5281/zenodo.21966764**, and *The Theory of Data*, Version 6.0, DOI **10.5281/zenodo.21958062**. A companion formal account of certificates and governed state appears in *Certifiable State Under Information Loss*, Version 1.0, DOI **10.5281/zenodo.21972541**.

# Abstract

The frequentist-Bayesian divide is usually introduced as a dispute about the meaning of probability, the status of parameters, priors, repeated sampling, or the interpretation of intervals. Those disagreements are real. But they begin after an earlier statistical problem has already been solved or silently assumed: what empirical evidence exists, what formal target it bears on, how the evidence could arise, what connects it to the target, and what world-facing claim the result is meant to support.

The Statistical Bridge relocates that shared work. A statistical analysis first **constitutes a bridge** between realized evidence and a formal target. If inferential probability is needed, it then declares a **probability source** and supplies an **inference certificate**: a formal account of what the evidence licenses about the target. Finally, it requires a **claim license** governing what the result may mean beyond the mathematics.

This yields four analytical obligations:

$$
\boxed{
\text{Bridge Constitution}
\rightarrow
\text{Probability Source}
\rightarrow
\text{Inference Certificate}
\rightarrow
\text{Claim License}
}
$$

The arrows indicate dependence, not a mandatory chronology. A randomized design can constitute part of the bridge and establish an evidence-side probability source in the same declaration; model criticism can later reopen earlier obligations. Paradigm sensitivity can also enter before the certificate layer: a Bayesian joint construction may add a **target-side probability source** through a prior, whereas many frequentist analyses do not. The certificate layer then states what inferential authority those declared sources support. Frequentist inference characteristically certifies procedures through their behavior over possible evidence under a declared reference system. Bayesian inference characteristically certifies target-side uncertainty conditional on realized evidence under a declared joint probability construction. This paper calls the governing distinction the **certificate basis**, while treating certificate basis as an open type rather than a new binary. "Quantifier home" is a useful mnemonic, but too crude as a definition because both traditions contain several probability statements and several quantifiers.

The distinction matters because the familiar presentation of the debate begins largely at the inference layer: fixed versus random parameters, long-run frequency versus posterior probability, p-values versus priors, and competing interval interpretations. Those distinctions are important, but they leave the bridge that makes either analysis empirically meaningful mostly implicit. Some apparent school disputes are therefore premature: a complete finite description may require no inferential probability at all. The architecture also prevents a different mistake: treating problem types as owned by schools. Randomized designs, hierarchical models, missingness, prediction, and causal targets can all support more than one inferential architecture. Evidence status attaches to particular bridge contracts, not to paradigms. Large-sample agreement between procedures is likewise not identity of certificate basis, and pragmatic coexistence between schools does not eliminate bridge obligations.

The architecture also offers an explanation for the modern fertility of Bayesian computation. Once a joint probability model and realized evidence are declared, Bayesian inference presents a remarkably stable computational target: a conditional distribution over unknown quantities. That regularity helped turn general-purpose sampling and optimization ideas into reusable inference engines for hierarchical and latent-variable models, and later into probabilistic programming systems. This is an advantage in computational realization of an inference certificate, not an automatic advantage in bridge constitution or claim licensing.

The paper then uses de Finetti, Birnbaum, calibrated Bayes, fiducial inference, and empirical Bayes as **stress tests** of the architecture rather than as premises for it. De Finetti becomes a representation bridge from exchangeability to mixture structure; Birnbaum becomes a dispute over which features of possible-evidence structure remain relevant after observation; calibrated Bayes becomes multi-certificate inference; and fiducial inference makes explicit the question of when forward probability may license reverse probability without a Bayesian prior.

The purpose is not to settle the frequentist-Bayesian debate. It is to type it. Before asking how probability should be interpreted, ask **where probability entered the analysis**. After probability enters, ask **what it is being allowed to certify**. Only then ask what claim the result is entitled to carry. Probability is not a property of "the analysis" in the abstract: it enters through a particular bridge relation, and its inferential authority extends only as far as that relation and its certificate license.

# 1. The debate usually starts too late

A familiar diagram of statistical inference is:

$$
\text{data}
\longrightarrow
\begin{cases}
\text{frequentist inference}\\
\text{Bayesian inference}
\end{cases}
\longrightarrow
\text{conclusion}.
$$

This picture is useful pedagogically and dangerous architecturally.

It begins with "data" as though the data object were already settled. It introduces the statistical schools as though they were the first important fork. It ends with "conclusion" as though a formal result carried its own empirical interpretation.

The familiar comparison is not wrong. Frequentist and Bayesian systems really do make different probability statements, treat unknown quantities differently, and attach different meanings to intervals, evidence, and conditioning.

The problem is that the comparison begins after much of the empirical statistical problem has already been built.

Suppose a company asks for average revenue among all eligible customers this quarter.

Before a confidence interval or posterior is meaningful, someone must decide:

- what counts as one customer-quarter point;
- which customer-quarter points exist even when no purchase occurred;
- how transactions attach to customers and quarters;
- whether transaction capture is complete;
- what Revenue means and how refunds or chargebacks enter;
- whether an empty qualifying event fiber means zero;
- what target the requested average refers to;
- and whether the final claim is only about the completed quarter or about something beyond it.

Those decisions do not become frequentist or Bayesian merely because a later calculation does.

They determine what evidence exists and what target that evidence is supposed to bear on.

The Statistical Bridge begins here.

Its characteristic structural center is:

$$
E^{(r)}\rightleftarrows S^{(r)},
$$

where $E^{(r)}$ is realized event-side evidence, $S^{(r)}$ is a spine-side target, and $r$ qualifies the relevant value-generation regime.

That notation does not say that all statistics literally consists of event logs and physical spines. It says something more general: statistical reasoning needs an evidence side, a target side, and a governed account of why the evidence can bear on that target.

The frequentist-Bayesian question enters only after much of this structure exists.

That gives the first claim of this paper:

> **Frequentist and Bayesian inference do not create the empirical bridge they cross.**

A confidence interval cannot repair an undefined population.

A posterior cannot make an event-defined row set into an independently established target population.

Neither school can infer its way out of a wrong analytical object.

This is not yet a theory of the frequentist-Bayesian divide. It is the ground on which such a theory has to stand.

# 2. The familiar map - and what it leaves implicit

A conventional account of the divide usually emphasizes distinctions such as:

- long-run or sampling behavior versus posterior probability;
- fixed unknown parameters versus probabilistically represented unknowns;
- confidence intervals versus credible intervals;
- tests and p-values versus priors, posteriors, and Bayes factors;
- sensitivity to stopping rules versus conditioning on realized evidence;
- philosophical purity versus modern pragmatic coexistence.

These distinctions matter.

But notice what the map usually takes for granted.

Before a parameter can be called fixed or probabilistically represented, **what target does it parameterize?**

Before data can be called random, **what evidence object has been constituted?**

Before a likelihood can connect the two, **what forward evidence-production account makes that likelihood empirically relevant?**

Before an interval can be interpreted, **what population, time, regime, or predictive domain is it supposed to speak about?**

And before debating the meaning of probability, a more primitive question appears:

> **Why is probability entitled to be here at all?**

The Statistical Bridge therefore does not reject the familiar map.

It places the map inside a larger argument.

The difference can be stated compactly:

The familiar debate asks **how probability should be used**.

SB first asks **what empirical bridge exists, and where probability entered it**.

Only then does the familiar school comparison become well-posed.

This also explains why the paper does not start by declaring one philosophy of probability correct. The prior question is architectural rather than philosophical.

# 3. From bridge to certificate

Once the evidence-target bridge is constituted, the familiar debate becomes interesting again.

The architecture proposed here is:

$$
\boxed{
\text{Bridge Constitution}
\rightarrow
\text{Probability Source}
\rightarrow
\text{Inference Certificate}
\rightarrow
\text{Claim License}
}
$$

The four terms are **logical obligations, not a temporal waterfall**. One declaration may discharge more than one obligation. A randomized assignment can simultaneously help constitute the bridge and establish an evidence-side probability source. A later model check, design failure, or transport challenge can reopen an earlier obligation rather than merely move the analysis "forward." The arrows therefore indicate dependency: a later claim cannot borrow authority from an undeclared earlier relation.

The four terms should not be collapsed.

## 3.1 Bridge constitution

Bridge constitution answers:

> What empirical objects are being connected, and why is there a statistical connection between them at all?

Schematically:

$$
\mathcal B
=
(E,S,A,r,\mathcal G,\mathcal T,\mathcal O),
$$

where:

- $E$ identifies the governed evidence object;
- $S$ identifies the target;
- $A$ represents the relevant anchor geometry;
- $r$ states the value-generation regime where needed;
- $\mathcal G$ is a forward evidence-production account;
- $\mathcal T$ is the target relation connecting evidence to the quantity of interest;
- $\mathcal O$ records observation, recording, and support conditions.

This notation is schematic, not a proposed universal statistical language.

Its purpose is to make one point clear:

$$
\boxed{\text{an inference method cannot repair an undefined bridge endpoint.}}
$$

## 3.2 Probability source

If the target is not exhausted by deterministic constitution of the realized evidence, inferential probability may be required.

The next question is:

> **Where did probability enter this analysis, and on which side of the bridge?**

Two broad locations matter.

**Evidence-side probability sources** govern how evidence could arise: randomized sampling, treatment assignment, stochastic process models, measurement-error models, response mechanisms, missingness models, and predictive models for future observations.

**Target-side probability sources** place probabilistic structure directly over target-side unknowns. A Bayesian prior is the canonical case; hierarchical laws over latent or unit-level quantities are another.

The distinction matters because stage 2 is not wholly paradigm-neutral. A frequentist and a Bayesian analysis can share the same randomized design and likelihood while differing over whether a target-side probability source is declared at all. The certificate difference at stage 3 is then partly downstream of that stage-2 choice.

Those structures are not interchangeable, and merely observing variation among values does not create one.

## 3.3 Inference certificate

Only after a probability source is declared do we ask:

> **What probability statement is supposed to carry the inferential return from evidence toward the target?**

This is where the familiar schools become central.

Frequentist inference characteristically certifies procedures through behavior over possible evidence under a declared reference system.

Bayesian inference characteristically produces target-side probability statements conditional on realized evidence under a declared joint probability construction.

The paper calls this distinction the **certificate basis**.[^certificate-reconciliation]

[^certificate-reconciliation]: The word *certificate* is used at two compatible levels across the corpus. In this paper, an **inference certificate** is the probability statement or guarantee carrying inferential authority. In *Certifiable State Under Information Loss*, a certificate is a proof-relevant witness establishing a claim from declared contracts and evidence. Read together, an SB inference certificate is a certified claim whose derivation rests on the declared probability-source premises; its evidence status is the grade of that derivation, the minimal inference declaration supplies part of the contract environment, and claim license bounds the entailment scope of the certified claim.

The detailed comparison comes later. For now, the important point is only that:

Probability source and inference certificate are therefore distinct objects.

## 3.4 Claim license

A final question remains after the formal inference is correct:

> What is the result entitled to mean about the world?

A 95% confidence interval with valid repeated-sampling coverage does not by itself establish that the reference experiment corresponds to the empirical data-production process.

A coherent posterior does not by itself establish that the likelihood describes the evidence mechanism, that the prior is appropriate for the intended target, or that the target corresponds to the practical claim.

The result has a home:

- an evidence object;
- a target;
- a model or design;
- a conditioning or reference structure;
- a regime;
- a population and time domain;
- a set of bridge assumptions.

Moving beyond that home requires another argument.

A practical claim-license review can therefore ask at least five questions:

1. **Population:** which governed population or target domain is covered?
2. **Time:** what time window or forecasting horizon is licensed?
3. **Regime:** under which assignment, observation, or value-generation regime does the claim hold?
4. **Transport:** what argument permits movement to another population, setting, policy, or future condition?
5. **Sensitivity:** which bridge premises materially control the conclusion, and what happens when they are varied?

The list is intentionally provisional. It is an operational review surface, not a complete logic of scientific claims.

Thus, **a formal uncertainty statement does not by itself license a world-facing claim**.

The layered picture is better written as:

$$
\begin{array}{c}
\textbf{Shared bridge obligations}\\
\text{bridge constitution + evidence-side probability sources}\\
\hline
\textbf{Potentially paradigm-marking source choice}\\
\text{target-side probability source, when declared}\\
\hline
\textbf{Open certificate layer}\\
\text{inference certificate(s)}\\
\hline
\textbf{Shared obligation again}\\
\text{claim license}
\end{array}
$$

The claim is not that frequentism and Bayesianism are the same.

It is that the schools occupy only part of the statistical architecture, and that some of their difference begins at target-side source declaration before it appears in the certificate.

## 3.5 Scope: this is not a new theory of probability

The architecture does not try to choose among frequency, propensity, subjective, logical, or other interpretations of probability as a general philosophical matter.

Its claim is more local.

A statistical analysis contains identifiable places where probabilistic structure is introduced and identifiable probability statements that are asked to do inferential work. The paper therefore studies **the address and authority of probability inside an empirical bridge**:

- where the probabilistic structure enters;
- what object it governs;
- what inferential certificate it supports;
- and what claim that certificate is licensed to carry.

Different philosophies can disagree about what probability ultimately means while still agreeing that these roles should not be silently conflated.

That boundary is deliberate:

$$
\boxed{
\text{this paper types probabilistic commitments; it does not legislate one philosophy of probability.}
}
$$

# 4. "Neither yet": sometimes the school question is premature

The cleanest way to see the architecture is to consider a case in which no inferential school is needed.

Suppose a completed quarter contains every eligible customer-quarter point and every qualifying transaction is completely captured. Revenue has been deterministically established for every point on the target spine.

The target is:

$$
\tau=
\frac{1}{|P_S|}
\sum_{s\in P_S}Revenue(s).
$$

Customers have different revenues. The empirical standard deviation may be large.

But heterogeneity is not itself an inferential probability source.

If the claim is only the finite descriptive mean for that completed, fully enumerated population, then the mean is determined.

So when asked:

> Should we report a frequentist confidence interval or a Bayesian credible interval?

the correct response may be:

> **Neither yet. What is uncertain?**

Probability may enter if the target changes:

- future quarters rather than the completed quarter;
- a superpopulation rather than the enumerated population;
- latent values under measurement error;
- incomplete capture under an observation model;
- a probability sample rather than a census;
- an intervention response rather than an observational description.

Only then does a probability-bearing bridge become necessary.

This produces one of the paper's core distinctions:

$$
\boxed{
\text{variation}
\neq
\text{probability source}
\neq
\text{inference certificate}.
}
$$

A dataset can vary without generating inferential uncertainty.

A probability source can exist without uniquely determining an inferential philosophy.

An inferential certificate can be mathematically valid while being attached to the wrong empirical bridge.

The point is more general than the example. A school-first vocabulary encourages the analyst to choose among inference engines before asking whether the target actually requires inference.

The Statistical Bridge reverses that order.

# 5. Probability source is not the same thing as inference certificate

The phrase "where probability enters" needs one refinement.

There are at least two different questions:

1. What probabilistic structure is part of the forward or joint account?
2. What probability statement is being used to certify the return from evidence to target?

These often travel together, but they are not identical.

## 5.1 Probability source

A probability source may be evidence-side or target-side.

Evidence-side sources include:

- a physically randomized sampling design;
- randomized treatment assignment;
- a stochastic process model;
- a measurement-error model;
- a response or missingness model;
- a model for future observations.

Target-side sources include:

- a prior over target-side unknowns;
- hierarchical laws over latent or unit-level quantities;
- other declared probabilistic constructions on the target side.

In randomized designs, part of the probability structure is physically instituted. In other cases it is modeled, elicited, or learned.

The phrase **probability source** should therefore not be confused with "posterior" or "confidence interval." Those are inferential products or certificates, not the source by themselves. The split also clarifies where the school divide begins: frequentist and Bayesian analyses may share evidence-side sources while differing over target-side probabilistic structure.

## 5.2 Inference certificate

The inference certificate states what probability-based guarantee or distribution licenses the inferential return.

For a frequentist confidence set in the Neyman tradition (Neyman 1937):

$$
P_\theta\{\theta\in C(X)\}\ge 1-\alpha.
$$

For a Bayesian posterior:

$$
\pi(\theta\mid x).
$$

For prediction, the certificate may concern a predictive distribution.

For a test, it may concern controlled error probabilities.

For a calibrated Bayesian procedure, more than one certificate can be present.

The important question is not merely:

> What method was used?

It is:

> **What exact probability statement is supposed to carry the inferential weight?**

Two elementary constructions make the source/certificate split explicit.

**Design-based example.** Let a finite population carry fixed values $y_1,\ldots,y_N$, and let a sampling design $P_D(S=s)$ randomize the selected sample $S$. The **probability source** is $P_D$, physically instituted by the design. If an estimator and interval procedure $C(S,Y_S)$ satisfy

$$
P_D\{\tau\in C(S,Y_S)\}\ge 1-\alpha,
$$

then the coverage statement is the **inference certificate**. The source is the design law; the certificate is a theorem about the behavior of the procedure under that law. They are related but not identical.

**Bayesian hierarchical example.** Let

$$
\theta_i\mid\eta\sim p(\theta_i\mid\eta),
\qquad
Y_i\mid\theta_i\sim p(y_i\mid\theta_i),
\qquad
\eta\sim\pi(\eta).
$$

The joint construction

$$
\pi(\eta)\prod_i p(\theta_i\mid\eta)p(y_i\mid\theta_i)
$$

contains both evidence-side and target-side probability sources. After observing $y$, a posterior statement such as

$$
P(\theta_j\in B\mid Y=y)
$$

is an **inference certificate** licensed by that joint construction and the conditioning rule. Again the certificate is derived from the source; it is not the source itself.

## 5.3 Certificate basis: two canonical tendencies

The conventional contrast can now be stated without pretending that one line exhausts either tradition.

| Question | Frequentist tendency | Bayesian tendency |
|---|---|---|
| Primary certificate basis | operating behavior over possible evidence | conditional distribution over target-side unknowns |
| Realized evidence | one outcome of a reference experiment/model | object conditioned upon |
| Target parameter | fixed/indexing state in the probability statement | represented probabilistically under prior/posterior |
| Sampling/data model | generates reference behavior | likelihood component of joint model |
| Prior | not required as target probability | part of the joint construction |
| Typical guarantee | coverage, error, risk, calibration | posterior probability, posterior expectation, predictive probability |

This is a structural summary of two canonical tendencies, not an exhaustive classification.

The mnemonic **quantifier home** can help:

- one architecture characteristically asks about behavior across possible evidence;
- the other characteristically makes target-side probability statements conditional on the evidence actually observed.

But "quantifier home" should not be promoted into a total definition. Frequentist statements quantify over parameter values and nuisance structures as well as possible data. Bayesian systems also define probability over possible observations, predictive quantities, model indices, and hierarchical levels.

The safer claim is:

> **The paradigms characteristically differ in the probability object used as the primary certificate for the inferential return passage.**

And beneath that difference:

Both still owe the evidence-target bridge.

## 5.4 Certificate basis is an open type

The certificate layer should not recreate the binary that the paper is trying to demote.

At least four neighboring constructions show why.

- **Likelihoodist evidence.** In the likelihood paradigm associated with Royall (1997), a likelihood ratio can be read as comparative evidence for one simple hypothesis against another. Its certificate semantics are not naturally reduced either to long-run operating behavior or to a posterior probability over the target.
- **Confidence distributions.** Modern confidence-distribution work represents frequentist inferential information through a sample-dependent distribution function on parameter space while retaining frequentist calibration requirements (Xie and Singh 2013).
- **Inferential models.** Martin and Liu (2013) construct prior-free, data-dependent probabilistic measures for assertions about parameters together with frequency-validity guarantees. This is explicitly multi-structured rather than a clean instance of either canonical column.
- **Betting/e-value certificates.** E-values and e-processes use nonnegative betting or supermartingale constructions to provide anytime-valid evidence and testing guarantees (Howard et al. 2021; Ramdas et al. 2023). These remain reference-law based but their guarantee semantics are usefully different from a fixed-sample confidence-set description.

Generalized fiducial inference supplies another target-side probability-like construction without a Bayesian prior and is treated separately in the stress tests.

The architectural claim is therefore:

> **Certificate basis is an open type. Frequentist and Bayesian forms are historically dominant instances, not the definition of the type.**

# 6. Do not assign problem types to schools

Once the bridge-first point is accepted, another temptation appears: classify empirical problems by the school that "naturally" owns them.

That is also too coarse.

A randomized experiment may support frequentist randomization inference, Bayesian analysis using the same assignment structure, or both.

A hierarchical problem may be analyzed through Bayesian multilevel models, empirical Bayes, frequentist mixed models, shrinkage estimators, or other procedures.

Missing-data problems can be approached through frequentist, Bayesian, semiparametric, design-based, or sensitivity-analysis frameworks.

Prediction, causal inference, measurement error, and latent-variable models likewise do not belong to one school.

The Statistical Bridge should therefore avoid claims of the form:

> frequentism is for designs; Bayesianism is for hierarchy.

The more precise questions are:

- What target has been constituted?
- What forward evidence-production structure is available?
- Where does probability enter?
- What inference certificate is desired?
- What assumptions and evidence statuses support that certificate?
- What claim will be made afterward?

A problem can support more than one valid certificate basis.

The school label is therefore less informative than the declared bridge architecture.

# 7. Evidence status belongs to contracts, not paradigms

A randomized sampling design can be physically instituted and audited. A prior distribution usually cannot be verified in that same mechanical sense. It is tempting to turn that difference into a ranking of paradigms.

That would be a mistake.

A Bayesian analysis can use the same verified randomized assignment or sampling design in its likelihood.

A frequentist analysis can use an iid or parametric model whose relevance is assumed rather than physically instituted.

The evidential status attaches to components of the bridge, not to the school chosen for inference.

For example:

| Bridge component | Possible evidential basis |
|---|---|
| Randomized assignment | instituted and auditable |
| Probability-sampling inclusion mechanism | instituted and auditable |
| Sensor recording mechanism | calibrated, monitored, partly verified |
| iid assumption | assumed and diagnostically examined |
| Exchangeability | argued from symmetry/domain knowledge |
| Parametric likelihood | scientifically motivated, fitted, checked |
| Prior | elicited, historically informed, reference/conventional, hierarchical |
| Missingness model | assumed, partly identified, sensitivity-tested |
| Transport assumption | scientifically argued, externally supported |
| Claim to another regime | requires a causal or transport contract |

This yields a neutral principle:

$$
\boxed{
\text{evidence status attaches to bridge contracts, not paradigms.}
}
$$

This point is easy to miss because school-level polemics often target the other side's weakest contract:

- an arbitrary prior;
- an imaginary repeated experiment;
- an unexamined iid assumption;
- optional stopping;
- misspecified likelihood;
- an implausible exchangeability claim.

Typing the bridge localizes the criticism.

# 8. Agreement is not identity, and pragmatism is not architecture

Modern accounts often conclude that the old school war matters less than it once did. Large samples can make Bayesian and frequentist procedures numerically similar. Hybrid methods deliberately combine posterior reasoning with frequentist calibration. Practitioners often choose methods pragmatically rather than defending one philosophy as universally correct.

All of that can be true without weakening the Statistical Bridge argument.

It clarifies it.

## 8.1 Certificate convergence is not bridge convergence

Under suitable regularity conditions, Bayesian posterior distributions can become approximately normal around efficient estimators, as in the Bernstein–von Mises theorem (van der Vaart 1998, ch. 10) around estimators with frequentist sampling properties. Confidence and credible intervals may then become numerically very close.

That is an important mathematical convergence.

But it is convergence at the certificate layer.

Two intervals can have nearly identical endpoints while entering the analysis through different inferential constructions and carrying different formal interpretations.

More importantly, agreement between the intervals says nothing by itself about whether:

- the target population was correctly constituted;
- the evidence object matches the intended unit of analysis;
- recording and observation were complete enough for the target;
- the likelihood or sampling model describes the relevant evidence-production process;
- the analysis has crossed to another population, time, or regime without a transport argument.

Thus:

$$
\boxed{
\text{certificate convergence}
\not\Rightarrow
\text{bridge convergence}.
}
$$

Large data can reduce sensitivity to some priors or make several inferential procedures agree. It cannot make an undefined denominator, wrong anchor, collapsed target universe, or unsupported causal passage disappear.

The distinction is useful even when the two schools give the same number. Numerical agreement can be reassuring about one layer while leaving another layer untouched.

## 8.2 Optional stopping is a certificate question, not a school slogan

A common practical contrast says that frequentist methods forbid continuous "peeking" while Bayesian methods allow it.

That contrast is too school-level.

A classical fixed-horizon frequentist test carries one reference structure. A sequential or anytime-valid frequentist procedure carries another. They are different inference certificates.

Likewise, a Bayesian posterior, Bayes factor, or sequential decision rule has its own probability construction and conditions under which stopping behavior is or is not ignorable for the claimed interpretation.

The bridge question is therefore:

> **What guarantee does this certificate make under this stopping process?**

not:

> Which school permits peeking?

This is a recurring pattern. Once the certificate is declared precisely, many culture-war slogans decompose into questions about the actual reference structure.

## 8.3 Pragmatic coexistence does not remove bridge obligations

Suppose the statistical community reaches complete peace and agrees:

> use Bayesian methods when useful, frequentist methods when useful, and hybrids when useful.

That resolves a social dispute about method choice.

It does not answer:

- what evidence object exists;
- what target the analysis concerns;
- why the evidence bears on that target;
- where probability enters;
- what probability statement is being asserted;
- what assumptions support that statement;
- what population, time, or regime the final claim may cover.

So:

$$
\boxed{
\text{pragmatic détente}
\not\Rightarrow
\text{bridge completion}.
}
$$

"Use whatever works" still owes a meaning for **works**.

Works for prediction under what future distribution?

Works for coverage under what repeated experiment?

Works for posterior concentration under what model?

Works for a business decision under what loss and target population?

Works for a causal claim under what interventional identification conditions?

The Statistical Bridge is not opposed to pragmatism. It asks pragmatism to declare its success criterion and the bridge relative to which that criterion is meaningful.

This is why the decline of the frequentist-Bayesian culture war does not make the present architecture obsolete.

The schools may reach détente.

The bridge obligations do not disappear.

# 9. Why Bayesianism became algorithmically fertile

The rise of Bayesian computation is often narrated as a philosophical victory enabled by faster computers. That explanation is incomplete.

Once a joint probability construction is declared,

$$
p(y,\theta)=p(y\mid\theta)\pi(\theta),
$$

and realized evidence $y=y_{\mathrm{obs}}$ is fixed, an enormous range of scientific problems share a recognizable computational target:

$$
\boxed{
\pi(\theta\mid y_{\mathrm{obs}})
}
$$

or, up to normalization,

$$
\pi(\theta\mid y)
\propto
p(y\mid\theta)\pi(\theta).
$$

The substantive model changes; the computational request remains remarkably stable:

> **Approximate this conditional target distribution.**

That interface regularity created unusually fertile ground for reusable algorithms.

## 9.1 MCMC was not born Bayesian

The Metropolis algorithm arose in statistical mechanics, Hastings generalized Markov-chain sampling, and Hybrid Monte Carlo arose in computational physics. Robert and Casella (2011) review this history. These were not algorithms invented because Bayesian philosophy had prevailed.

Bayesian statistics instead supplied a vast recurring class of target distributions for which such algorithms were useful. Gelfand and Smith (1990) helped demonstrate how Gibbs and related sampling methods could turn difficult posterior integration into a general computational program.

The practical problem shifted from deriving a posterior analytically to constructing an algorithm whose output represents that posterior well enough for downstream quantities.

## 9.2 Bayes standardized the return object

The Statistical Bridge makes the computational advantage easier to locate.

Inference is a return movement from realized evidence toward a target. Bayesianism gives that return a standardized mathematical form:

$$
E=x
\quad\Longrightarrow\quad
P(S\mid E=x),
$$

once the joint probability construction has been supplied.

Frequentist inference is no less rigorous, but its computational return object is more heterogeneous: estimators, confidence sets, randomization distributions, estimating equations, tests, bootstrap distributions, conformal sets, prediction intervals, and other procedure-specific objects.

The point is not superiority. It is **interface regularity**:

$$
\text{model}
+
\text{observations}
\longrightarrow
\text{conditional target distribution}.
$$

That regularity makes generic inference machinery exceptionally reusable.

## 9.3 The integration bottleneck became an algorithm factory

Rich Bayesian models were historically easy to state and often hard to calculate because normalization and marginalization could be analytically intractable.

That weakness concentrated effort on one reusable question:

> How can expectations, marginals, predictions, and decisions under a complicated target distribution be approximated without evaluating the defining integrals directly?

MCMC, HMC (Duane et al. 1987), NUTS (Hoffman and Gelman 2014), sequential Monte Carlo, importance sampling, variational inference, Laplace approximations, and related methods answer versions of that question.

A posterior approximation is also reusable. Draws

$$
\theta^{(1)},\ldots,\theta^{(M)}
\approx
\pi(\theta\mid y)
$$

can support posterior means, credible intervals, comparisons, predictive distributions, derived quantities, and expected losses. The posterior is therefore a rich **conditional inferential object**. This is only a computational analogy to sufficient state, not ToD sufficient state itself.

Hierarchy and latent structure amplify the payoff. Models may add hyperparameters, latent states, missing values, mixtures, spatial structure, or measurement error while preserving the recognizable request for a conditional distribution over unknowns. Systems such as Stan and Turing exploit exactly this separation between model declaration and reusable inference machinery (Carpenter et al. 2017; Ge, Xu, and Ghahramani 2018).

## 9.4 Computational success is not bridge validity

The resulting computational advantage need not be read as evidence that one philosophy of probability defeated another. A substantial part of the Bayesian revival can instead be explained by the falling cost of realizing a powerful and standardized inference certificate.

But excellent realization of a certificate is not evidence that the empirical bridge is correct.

A sampler can faithfully approximate the declared posterior while the likelihood describes the wrong observation process, the target population is wrong, exchangeability is unjustified, missingness is mishandled, or the final claim outruns the design.

Therefore:

$$
\boxed{
\text{computational convergence}
\neq
\text{inferential validity}
\neq
\text{bridge validity}.
}
$$

A sampler can be excellent at crossing the bridge it was given.

It cannot certify that the bridge should have been built there.

The companion paper *Certifiable State Under Information Loss* reaches the same boundary from the state side: computational state, evidential warrant, and claim informativeness can be preserved or lost separately. The only consequence needed here is that **a computationally faithful realization of an inference certificate does not create the empirical warrant for that certificate**.

Bayesianism's computational interface is a genuine success. It belongs primarily to certificate realization, not to bridge constitution or claim licensing.

# 10. Stress tests: what the architecture reveals in classic boundary cases

The sections that follow are **not premises for the paper's main thesis**.

The thesis does not depend on a new reading of de Finetti, Birnbaum, fiducial inference, or empirical Bayes.

These cases are useful because they put pressure on the distinction among:

- bridge constitution;
- probability source;
- inference certificate;
- and claim license.

If the architecture clarifies those difficult cases without pretending to settle them, that is evidence that the distinction is doing useful work.

Each case is read through the same five questions:

1. **Bridge:** what evidence-target relation has already been constituted?
2. **Probability source:** where does probabilistic structure enter?
3. **Certificate:** what probability statement carries inferential authority?
4. **Residual obligation:** what premise remains outside that certificate?
5. **Claim license:** what may the result actually be said to establish?

Using one diagnostic matters. It prevents the stress tests from becoming five unrelated historical commentaries and makes clear that they are applications of one architecture.

## 10.1 De Finetti: a representation bridge, not a Bayesian trophy

De Finetti's representation theorem is an especially revealing test case.

In the classic infinite exchangeable Bernoulli setting, exchangeability implies that the joint distribution can be represented as a mixture of iid Bernoulli processes:

$$
P(X_1=x_1,\ldots,X_n=x_n)
=
\int
\prod_{i=1}^n
p^{x_i}(1-p)^{1-x_i}
\,d\mu(p).
$$

The theorem is useful here because it connects two different descriptions:

- a symmetry property of the observable sequence;
- a mixture representation involving a latent law parameter.

That makes it tempting to call de Finetti a theorem translating frequentism into Bayesianism.

The Statistical Bridge suggests a more precise interpretation.

> **De Finetti is a representation bridge from an exchangeability declaration to a mixture-of-laws representation.**

The input is not "frequentism." It is a symmetry condition.

The output is not a physically verified sampling design. It is a mathematical representation.

Nor does the theorem, by itself, establish that the real empirical sequence is exchangeable, that an infinite extension is appropriate, that the latent mixture variable is the substantive target of interest, or that a particular prior distribution has empirical authority.

Finite exchangeability also requires care; finite sequences do not automatically receive the same exact infinite-mixture representation (Diaconis and Freedman 1980).

So the typed contribution is not:

$$
\text{frequentist world}\Rightarrow\text{Bayesian world}.
$$

It is:

$$
\boxed{
\text{symmetry on possible evidence}
\Rightarrow
\text{law-space representation}.
}
$$

That is still highly relevant to the frequentist-Bayesian divide because it shows how a constraint stated on the evidence side can imply a representation on the law side.

In the limited sense used here, it is a representation bridge between two formal descriptions.

But it does not abolish the empirical obligations around the theorem.

## 10.2 Birnbaum: which bridge information survives observation?

Birnbaum's 1962 argument is a more direct pressure point.

The strong likelihood principle says, roughly, that if two experimental outcomes generate proportional likelihood functions for the parameter, they carry the same evidential meaning about that parameter. This differs sharply from procedures whose significance levels or confidence properties depend on the full experimental structure, including outcomes that did not occur.

Birnbaum argued that versions of the sufficiency and conditionality principles jointly imply the likelihood principle.

Whatever one's position on that argument, the Statistical Bridge gives the controversy a useful address.

### 10.2.1 Sufficiency as retained inferential state

Sufficiency says that, relative to a probability model and parameter, certain data distinctions may be discarded without losing information about the parameter.

That resembles a state discipline:

$$
x
\longrightarrow
T(x),
$$

where $T$ retains what the declared inferential target requires under the model.

This should not be conflated with ToD sufficient state, which concerns exact lawful analytical continuation of a measure family. But the structural analogy is real: both ask what information may be discarded relative to a declared continuation.

### 10.2.2 Conditionality as experiment selection

Conditionality principles concern what should happen inferentially when the realized experiment is selected from a mixture or when ancillary structure is observed.

In bridge language, conditionality asks which parts of the possible-evidence architecture remain relevant once the realized branch is known.

### 10.2.3 The typed restatement

The Birnbaum controversy can therefore be read as a dispute over a question like:

> **After observation, which features of the bridge's possible-evidence structure remain evidentially relevant: only the realized likelihood, or also the larger experiment that could have produced other outcomes?**

That is much more precise than saying one school "cares about the sampling plan" and the other does not.

It also connects directly to optional stopping. Two datasets may yield the same likelihood while arising under different stopping rules. A strict likelihood-principle reading treats them as evidentially equivalent for the parameter. Many frequentist procedures do not, because the reference distribution over possible evidence changes with the stopping rule.

The disagreement therefore concerns the status of **unrealized passages** after the realized evidence is fixed.

This is close to the "quantifier home" intuition, but sharper:

$$
\boxed{
\text{Which counterfactual evidence paths remain part of the inference certificate?}
}
$$

### 10.2.4 Why SB should not claim to settle Birnbaum

The exact logical status of Birnbaum's theorem, especially the formulation and use of conditionality, has been disputed extensively.

That is not a weakness of the Statistical Bridge reading.

It is the point.

Typing the objects does not magically make the disagreement disappear. It tells us where the disagreement lives. In particular, the bridge reading inherits rather than resolves disputes over the exact formulation of conditionality and the logical route from sufficiency plus conditionality to the strong likelihood principle (Birnbaum 1962; Mayo 2014).

One camp may treat the larger experiment identity as inferentially relevant. Another may treat the realized likelihood as exhausting the relevant evidence about the parameter. Others may distinguish evidence from decision, or accept some conditionality principles but not the form needed for the strong likelihood principle.

The Statistical Bridge can host those positions without collapsing them.

## 10.3 Calibrated Bayes: two certificates, not philosophical compromise

The calibrated-Bayes tradition is often described as pragmatic reconciliation: conduct Bayesian inference while seeking good frequentist properties. Rubin's account of Bayesianly justifiable frequency calculations is an early canonical statement of this posture (Rubin 1984), and Little (2011) develops the calibrated-Bayes framing explicitly.

In the bridge architecture, the structure is cleaner.

A Bayesian analysis can produce a realized-evidence certificate:

$$
\pi(\theta\mid x).
$$

The procedure generating that posterior, interval, decision, or prediction can also be evaluated across possible evidence under a declared reference system:

$$
P_\theta\{\theta\in C(X)\},
$$

or through another calibration criterion.

These are not rival statements.

They are two certificates addressing different questions.

One concerns target-side uncertainty conditional on realized evidence.

The other concerns the behavior of the procedure across possible passages.

Thus:

$$
\boxed{
\text{calibrated Bayes}
=
\text{conditional-target certificate}
+
\text{passage-level calibration certificate}.
}
$$

This reframing has two advantages.

First, it avoids treating calibrated Bayes as a philosophical truce. The two statements simply have different homes.

Second, it makes disagreement testable. One can ask separately whether the posterior model is substantively adequate and whether the induced procedure has desirable reference behavior.

Matching priors, frequentist evaluation of Bayesian intervals, posterior predictive calibration, and related practices become examples of **multi-certificate inference**.

The architecture does not require every analysis to carry both certificates. It merely makes clear what additional assurance is being requested when both are demanded.

## 10.4 Fiducial inference: can forward probability travel backward without a prior?

Fiducial inference is perhaps the most revealing stress test because it attacks the exact boundary that the Statistical Bridge exposes. Fisher introduced the fiducial argument in his discussion of inverse probability (Fisher 1930), and modern generalized fiducial work supplies explicit data-generating equations and inversion recipes (Hannig 2009; Hannig et al. 2016).

A forward data-generating equation may be written schematically as:

$$
X=G(\theta,U),
\qquad
U\sim P_U.
$$

The probability law for $U$ supplies randomness on the evidence-generating side.

Fiducial reasoning attempts, under suitable conditions, to invert that construction after observing $X=x$ and obtain a probability-like distribution for $\theta$ without introducing a Bayesian prior.

Modern generalized fiducial inference describes this as transferring randomness from the data-generating equation to parameter space through inversion. The modern literature also makes clear that the construction is not automatically unique or valid in arbitrary problems: the generating equation, inversion rule, and regularity conditions are substantive parts of the method.

As a stress test of the Statistical Bridge distinction, the question becomes:

> **When does a probability law on a forward evidence-generating construction license a probability law on the target side after the evidence is observed?**

That is not merely a historical curiosity.

It isolates a general problem hidden inside many inferential systems:

$$
\boxed{
\text{forward probability}
\not\Rightarrow
\text{reverse probability}
}
$$

without an additional rule.

Bayes supplies one such rule through a joint prior-likelihood construction and conditioning.

Frequentist inference often avoids assigning reverse probability to a fixed parameter and instead certifies a procedure over repeated possible evidence.

Fiducial inference attempts another route.

Seen this way, the historical controversy around fiducial reasoning is almost a laboratory experiment for the Statistical Bridge. It asks whether the return passage can inherit probability from the forward passage, and under what structural conditions that inheritance is well-defined.

The right SB conclusion is not that fiducial inference "forgot where the quantifier lives." Modern fiducial approaches are explicit about their generating equations and inversion rules.

The deeper conclusion is:

> **Any reverse probabilistic passage owes a contract explaining why probability may move from the forward construction to the target-side statement.**

## 10.5 Empirical Bayes and hierarchical problems: the target may itself have a spine

Empirical Bayes, originating in Robbins's ensemble-based program (Robbins 1956), is often described as living awkwardly between frequentism and Bayesianism.

The bridge view suggests why.

Suppose there are many related units or problems:

$$
\theta_1,\ldots,\theta_m,
$$

with observations:

$$
X_i\mid\theta_i\sim p(\cdot\mid\theta_i),
$$

and a higher-level distribution:

$$
\theta_i\sim G.
$$

The law $G$ is itself learned from the ensemble.

The architecture now exposes at least two related inferential levels:

1. within-unit evidence about $\theta_i$;
2. across-unit evidence about the law $G$.

The "law space" is no longer merely a philosophical location. It is associated with an empirical population of related problems or units.

This explains why empirical Bayes can feel neither purely frequentist nor fully Bayesian in the classical sense. It learns part of the target-side probability structure from repeated related cases and then uses that learned structure to regularize or infer unit-level targets.

A Statistical Bridge account would ask:

- What establishes the population of exchangeable or related units?
- Why may information travel across units?
- What symmetry, hierarchical, or domain contract supports that passage?
- Which parts of the law are estimated from the ensemble?
- Which uncertainty statements condition on the estimated law and which propagate uncertainty about it?
- What claim is made about a new unit versus the existing ensemble?

The important point is again architectural:

The "school" label is therefore less informative than the declared bridge structure.

## 10.6 The five stress tests in one view

The cases can now be compressed without erasing their differences.

| Case | Where probability enters | Primary certificate issue | Residual bridge obligation |
|---|---|---|---|
| de Finetti | exchangeable law on possible evidence | mixture/law-space representation | why exchangeability is empirically warranted |
| Birnbaum | experiment/model structure over possible evidence | which features remain evidentially relevant after observation | which conditioning/experiment identity the bridge preserves |
| calibrated Bayes | joint model plus repeated/reference evaluation | conditional target certificate plus calibration certificate | whether either certificate's model/reference structure fits the empirical bridge |
| fiducial | forward generating equation and auxiliary randomness | whether forward probability may be transported to target-side probability | the inversion/transport rule licensing that reverse passage |
| empirical Bayes | ensemble of related units/problems | learned higher-level law used for unit-level inference | why units are exchangeable/related and how uncertainty about the learned law propagates |

The table is not a taxonomy of schools.

It shows that several foundational disputes are better described as disagreements about **where probability is introduced, what it certifies, and which bridge obligations remain active afterward**.

## 10.7 Relation to prior foundational work

The four-obligation architecture overlaps several established programs without being identical to any one of them.

The **likelihood-principle** literature asks which features of an experiment remain evidentially relevant once the realized likelihood is fixed. SB places that dispute primarily at the certificate and conditioning/reference layers: it asks which unrealized evidence paths remain part of the inferential warrant.

**Calibrated Bayes** explicitly combines conditional Bayesian output with frequency-based evaluation (Rubin 1984; Little 2011). SB's contribution is to type those as distinct certificates rather than treating calibration as philosophical compromise.

**Confidence distributions**, **inferential models**, and **generalized fiducial inference** all demonstrate that target-side distribution-like inferential objects need not be ordinary Bayesian posteriors (Xie and Singh 2013; Martin and Liu 2013; Hannig 2009). Their existence is one reason certificate basis must remain an open type.

Modern **pragmatic Bayesianism** also emphasizes posterior predictive checking, model criticism, and revision rather than treating Bayesian updating as a closed inductive logic (Gelman and Shalizi 2013). SB agrees with that practical diagnosis while adding an explicit distinction between bridge constitution, probability source, certificate, and claim license.

The proposed contribution is therefore organizational rather than imperial. It does not replace these foundations. It supplies a typed architecture in which their disagreements can be located without asking any single school to carry the whole empirical problem.

# 11. The divide does not disappear

A typed architecture can make philosophical arguments clearer. It cannot honestly erase them.

Several genuine disagreements remain.

## 11.1 What is probability allowed to mean?

Bayesian traditions permit probability statements about unknown quantities under a probability model. Frequentist traditions generally reserve inferential probability for repeatable random mechanisms or model-generated evidence and avoid treating fixed unknown parameters as random merely because they are unknown.

That is a substantive difference.

## 11.2 Which unrealized outcomes matter?

Likelihood-based and Bayesian arguments often emphasize the realized likelihood.

Frequentist operating guarantees may depend on outcomes that could have occurred but did not.

That is a substantive difference.

## 11.3 What role should prior information play?

Priors may represent substantive information, hierarchical regularization, reference structure, or conventions needed to complete a model.

How such information should be represented and justified remains a substantive issue.

## 11.4 Is evidence the same thing as decision performance?

A procedure can have excellent long-run error properties while an evidential interpretation of a particular result remains controversial.

A posterior can be coherent under its model while its repeated performance under misspecification is poor.

Evidence, uncertainty, prediction, and decision are related but not identical objects.

## 11.5 What survives model misspecification?

Both paradigms face the problem that formal guarantees are relative to declared models, designs, or asymptotic structures.

Robustness, sensitivity analysis, model checking, and external evidence remain bridge obligations.

Typing the bridge does not settle these questions.

It does something more useful:

> **It prevents one disagreement from masquerading as five.**

# 12. A minimal declaration for inferential probability

If the argument is right, a statistical result should be able to answer a small set of questions before it advertises itself as "frequentist" or "Bayesian."

A minimal inference declaration would state:

1. **Evidence object** - what realized empirical object entered the analysis?
2. **Target object** - what quantity, population, parameter, prediction, or state is being reasoned about?
3. **Forward account** - how could evidence like this arise relative to the target?
4. **Probability source** - where does probability enter?
5. **Certificate basis** - what probability statement certifies the inferential return?
6. **Conditioning/reference structure** - what is conditioned upon and what possible evidence remains relevant?
7. **Evidence status** - which bridge components are instituted, measured, modeled, assumed, elicited, or externally supported?
8. **Claim license** - what population, time, regime, transport domain, and sensitivity envelope does the result actually support?

This is not intended as bureaucratic metadata.

It is a way to reveal when two analyses that use the same formula are not the same statistical argument.

For example:

### Probability survey

- evidence: sampled eligible units;
- target: finite population total;
- forward account: randomized inclusion design;
- probability source: sampling design;
- certificate basis: repeated design behavior;
- status: design instituted and inclusion probabilities auditable;
- claim: finite population under declared frame and response conditions.

### Bayesian clinical model

- evidence: observed outcomes under treatment assignment;
- target: model parameters and/or future outcomes;
- forward account: outcome likelihood plus randomized assignment where relevant;
- probability source: joint prior-model construction;
- certificate basis: posterior conditional on realized evidence;
- additional certificate: repeated operating characteristics may be evaluated;
- claim: bounded by model, trial population, treatment regime, and transport conditions.

### Completed census description

- evidence: complete values for every eligible target point;
- target: finite descriptive mean;
- forward account: deterministic construction under complete capture;
- probability source: none required for the descriptive target;
- certificate basis: none required;
- claim: completed finite population only.

The third case is important.

The declaration can say:

$$
\boxed{\text{no inferential probability is needed}.}
$$

That is something a school-first vocabulary tends to hide.

# 13. What this says about the century-old debate

The Statistical Bridge does not replace the frequentist-Bayesian divide. It reduces the amount of statistical architecture that the divide is asked to carry.

The four obligations can be stated once:

1. **Constitute the bridge:** identify evidence, target, forward account, and target relation.
2. **Type the probability:** identify evidence-side and any target-side probability sources.
3. **State the certificate:** declare the probability statement or guarantee carrying inferential authority.
4. **License the claim:** bound the population, time, regime, transport, and sensitivity scope of the world-facing statement.

These obligations need not occur chronologically, and one declaration may discharge several of them. The school divide can enter at stage 2 through target-side probability and at stage 3 through certificate basis. It does not own stages 1 or 4.

That is enough to preserve the genuine disagreements—posterior probability versus operating behavior, prior structure, counterfactual evidence paths, stopping rules, and the meaning of statistical evidence—without treating "frequentist" or "Bayesian" as a substitute for declaring the empirical argument.

# 14. Consequences for statistical theory and practice

## 14.1 Textbook pedagogy

Introductory statistics often teaches the interpretation of probability before teaching students to ask where the probability came from.

The order should be reversed.

Before explaining confidence versus credibility, ask:

> What is random in this problem, under what declared structure?

That question prevents finite descriptions, randomized designs, superpopulation models, measurement uncertainty, and predictive uncertainty from being treated as interchangeable.

## 14.2 Statistical software

Software routinely exposes a choice of estimator or inferential engine while hiding the bridge that makes the result meaningful.

A more governed system would represent the target, evidence domain, probability source, and certificate basis independently of the numerical procedure.

"Bayesian" and "frequentist" would become properties of a declared inferential contract, not substitutes for declaring the empirical problem.

## 14.3 Model criticism

Model criticism becomes a bridge question. This is compatible with the practice-oriented Bayesian account of Gelman and Shalizi (2013), where model checking and revision are not reducible to posterior updating inside a fixed model.

A failed posterior predictive check, poor frequentist calibration, design violation, missingness sensitivity, or transport failure attacks different components.

The architecture helps localize the failure rather than collapsing every problem into "the model is wrong."

## 14.4 AI-assisted statistical analysis

An AI system can easily select a familiar method from a familiar table shape.

That is exactly the precedent problem the Statistical Bridge was designed to expose.

A governed statistical agent should not begin with:

> frequentist or Bayesian?

It should begin with:

> What is the evidence object? What is the target? Where does probability enter?

Only then should it propose an inference certificate.

# 15. Open questions

The framework raises several questions that deserve more careful formal treatment.

## 15.1 Can certificate bases be composed?

Calibrated Bayes suggests yes, but a general theory would need to distinguish logically independent certificates from redundant or contradictory ones.

## 15.2 Can evidence status be typed compositionally?

If a randomized design is verified but the measurement model is assumed, what status should attach to the final inference?

A simple weakest-link rule is probably too crude. The companion paper *Certifiable State Under Information Loss* develops a proof-relevant graded derivability framework for this broader problem, but a fully statistical evidence calculus remains open here: design evidence, model evidence, calibration evidence, and scientific support need not live on one total ladder.

## 15.3 What exactly survives conditioning?

Birnbaum, ancillarity, conditional inference, selective inference, and optional stopping all ask versions of this question.

A bridge calculus might help state which pieces of the possible-evidence structure remain active after conditioning.

## 15.4 When can probability be transported backward?

Bayes, fiducial inference, confidence distributions, inferential models, and related systems give different answers.

The forward-to-reverse passage is a natural object for a Statistical Bridge research program.

## 15.5 How should exchangeability be grounded?

De Finetti gives a representation theorem once exchangeability is declared.

Applied statistics still needs an account of why that symmetry is appropriate for the empirical units and target.

That is a bridge-construction question, not a theorem-proving question.

# 16. Conclusion

The frequentist-Bayesian divide is real, but it is smaller than the statistical problem.

Before a confidence procedure or posterior can carry empirical meaning, an analysis must establish what evidence exists, what target that evidence bears on, how evidence could arise, and why the connection is relevant. If probability is needed, its source must be identified. Only then can an inference certificate state what probabilistic authority is being claimed, and only after that can a world-facing claim be licensed.

The resulting architecture is:

$$
\text{Bridge Constitution}
\rightarrow
\text{Probability Source}
\rightarrow
\text{Inference Certificate}
\rightarrow
\text{Claim License}.
$$

This relocation preserves the genuine disagreements. Frequentist procedures characteristically appeal to behavior over possible evidence. Bayesian procedures characteristically derive conditional target-side distributions from joint probability constructions. Likelihoodist, confidence-distribution, inferential-model, fiducial, betting/e-value, and multi-certificate constructions show that the certificate layer is broader than either canonical tendency.

The architecture also explains several otherwise confusing facts:

- a complete finite description may need no inferential probability;
- calibrated Bayes can carry more than one certificate without becoming a philosophical compromise;
- computational convergence does not establish bridge validity;
- asymptotic agreement does not make bridge constructions identical;
- and evidence status belongs to particular contracts, not to schools.

The final principle is therefore:

$$
\boxed{
\textbf{Probability has an address.}
}
$$

It enters at a particular relation in the bridge, under particular assumptions or instituted mechanisms. Its inferential authority is carried by a particular certificate. That authority extends only as far as the source, certificate, and claim license support.

The frequentist-Bayesian divide becomes clearer when probability is asked not only **what it means**, but **where it lives and what it is licensed to do**.

# Publication note

**Version 1.0.** The architecture is frozen and the manuscript has completed two external review passes, source verification, structural reconciliation, and copy editing. The four stages are stated as logical obligations rather than a chronology; probability sources are separated into evidence-side and target-side forms; certificate basis is explicitly open; the source/certificate distinction receives formal examples; claim license has an operational review surface; and primary or canonical sources anchor the foundational stress tests and neighboring literature.

**DOI:** **10.5281/zenodo.21977942**

# References

Birnbaum, Allan. 1962. "On the Foundations of Statistical Inference." *Journal of the American Statistical Association* 57 (298): 269-306. DOI: 10.1080/01621459.1962.10480660.

Carpenter, Bob, Andrew Gelman, Matthew D. Hoffman, Daniel Lee, Ben Goodrich, Michael Betancourt, Marcus Brubaker, Jiqiang Guo, Peter Li, and Allen Riddell. 2017. "Stan: A Probabilistic Programming Language." *Journal of Statistical Software* 76 (1): 1-32. DOI: 10.18637/jss.v076.i01.

de Finetti, Bruno. 1937. "La prévision: ses lois logiques, ses sources subjectives." *Annales de l'Institut Henri Poincaré* 7 (1): 1-68.

Diaconis, Persi, and David Freedman. 1980. "Finite Exchangeable Sequences." *The Annals of Probability* 8 (4): 745-764.

Duane, Simon, A. D. Kennedy, Brian J. Pendleton, and Duncan Roweth. 1987. "Hybrid Monte Carlo." *Physics Letters B* 195 (2): 216-222. DOI: 10.1016/0370-2693(87)91197-X.

Fisher, R. A. 1930. "Inverse Probability." *Proceedings of the Cambridge Philosophical Society* 26 (4): 528-535. DOI: 10.1017/S0305004100016297.

Ge, Hong, Kai Xu, and Zoubin Ghahramani. 2018. "Turing: A Language for Flexible Probabilistic Inference." *Proceedings of the 21st International Conference on Artificial Intelligence and Statistics (AISTATS)* 84: 1682-1690.

Gelfand, Alan E., and Adrian F. M. Smith. 1990. "Sampling-Based Approaches to Calculating Marginal Densities." *Journal of the American Statistical Association* 85 (410): 398-409. DOI: 10.1080/01621459.1990.10476213.

Gelman, Andrew, and Cosma Rohilla Shalizi. 2013. "Philosophy and the Practice of Bayesian Statistics." *British Journal of Mathematical and Statistical Psychology* 66 (1): 8-38. DOI: 10.1111/j.2044-8317.2011.02037.x.

Hannig, Jan. 2009. "On Generalized Fiducial Inference." *Statistica Sinica* 19: 491-544.

Hannig, Jan, Hari Iyer, Randy C. S. Lai, and Thomas C. M. Lee. 2016. "Generalized Fiducial Inference: A Review and New Results." *Journal of the American Statistical Association* 111 (515): 1346-1361. DOI: 10.1080/01621459.2016.1165102.

Hastings, W. K. 1970. "Monte Carlo Sampling Methods Using Markov Chains and Their Applications." *Biometrika* 57 (1): 97-109. DOI: 10.1093/biomet/57.1.97.

Hoffman, Matthew D., and Andrew Gelman. 2014. "The No-U-Turn Sampler: Adaptively Setting Path Lengths in Hamiltonian Monte Carlo." *Journal of Machine Learning Research* 15: 1593-1623.

Howard, Steven R., Aaditya Ramdas, Jon McAuliffe, and Jasjeet Sekhon. 2021. "Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences." *The Annals of Statistics* 49 (2): 1055-1080. DOI: 10.1214/20-AOS1991.

Little, Roderick J. A. 2011. "Calibrated Bayes, for Statistics in General, and Missing Data in Particular." *Statistical Science* 26 (2): 162-174. DOI: 10.1214/10-STS318.

Martin, Ryan, and Chuanhai Liu. 2013. "Inferential Models: A Framework for Prior-Free Posterior Probabilistic Inference." *Journal of the American Statistical Association* 108 (501): 301-313. DOI: 10.1080/01621459.2012.747960.

Mayo, Deborah G. 2014. "On the Birnbaum Argument for the Strong Likelihood Principle." *Statistical Science* 29 (2): 227-239. DOI: 10.1214/13-STS457.

Metropolis, Nicholas, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller, and Edward Teller. 1953. "Equation of State Calculations by Fast Computing Machines." *The Journal of Chemical Physics* 21 (6): 1087-1092. DOI: 10.1063/1.1699114.

Neyman, Jerzy. 1937. "Outline of a Theory of Statistical Estimation Based on the Classical Theory of Probability." *Philosophical Transactions of the Royal Society of London. Series A* 236 (767): 333-380. DOI: 10.1098/rsta.1937.0005.

Ramdas, Aaditya, Peter Grünwald, Vladimir Vovk, and Glenn Shafer. 2023. "Game-Theoretic Statistics and Safe Anytime-Valid Inference." *Statistical Science* 38 (4): 576-601. DOI: 10.1214/23-STS894.

Robbins, Herbert. 1956. "An Empirical Bayes Approach to Statistics." In *Proceedings of the Third Berkeley Symposium on Mathematical Statistics and Probability*, Vol. 1, 157-163. Berkeley: University of California Press.

Robert, Christian P., and George Casella. 2011. "A Short History of Markov Chain Monte Carlo: Subjective Recollections from Incomplete Data." *Statistical Science* 26 (1): 102-115. DOI: 10.1214/10-STS351.

Royall, Richard M. 1997. *Statistical Evidence: A Likelihood Paradigm*. London: Chapman & Hall.

Rubin, Donald B. 1984. "Bayesianly Justifiable and Relevant Frequency Calculations for the Applied Statistician." *The Annals of Statistics* 12 (4): 1151-1172. DOI: 10.1214/aos/1176346785.

van der Vaart, A. W. 1998. *Asymptotic Statistics*. Cambridge: Cambridge University Press.

Wang, Huayin. 2026. *The Theory of Data*. Version 6.0. Zenodo. DOI: 10.5281/zenodo.21958062.

Wang, Huayin. 2026. *The Theory of Data: An Introduction - Analytical Meaning, Lawful Transformation, and Governed Results*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21960639.

Wang, Huayin. 2026. *The Statistical Bridge: From Events to Spines, Data Work, and the Interpretation of Results*. Version 2.0. Zenodo. DOI: 10.5281/zenodo.21966764.

Wang, Huayin. 2026. *A Primer on the Statistical Bridge: Why Statistical Analysis Is Neither Pure Mathematics nor Data Processing*. Version 1.1. Zenodo. DOI: 10.5281/zenodo.21966876.

Wang, Huayin. 2026. *Certifiable State Under Information Loss: Governed Derivability, Claim Transport, and Approximate Closure*. Version 1.0. Zenodo. DOI: 10.5281/zenodo.21972541.

Xie, Min-ge, and Kesar Singh. 2013. "Confidence Distribution, the Frequentist Distribution Estimator of a Parameter: A Review." *International Statistical Review* 81 (1): 3-39. DOI: 10.1111/insr.12000.

---

**Publication:** Version 1.0, 17 August 2026  
**DOI:** 10.5281/zenodo.21977942  
**License:** CC BY 4.0

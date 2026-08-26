---
title: "Regime Has a Contract"
subtitle: "Intervention, Observation, and the Data Foundation of Causal Identification"
author: "Huayin Wang, datumwise · independent open-source research project V"
date: "Version 1.0 - 7 August 2026"
lang: en-US
papersize: letter
geometry: margin=1in
fontsize: 11pt
subject: "A Theory-of-Data reading of intervention and Judea Pearl's causal framework"
toc: true
toc-depth: 2
keywords:
  - Theory of Data
  - causal inference
  - intervention
  - regime
  - do-calculus
  - structural causal model
  - experimental design
  - statistical bridge
  - observational data
  - causal identification
  - evidence provenance
  - data provenance
  - observation status
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
    \fancyhead[L]{\small Regime Has a Contract}
    \fancyhead[R]{\small Huayin Wang}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \setlength{\headheight}{14pt}
  - |
    \urlstyle{same}
---

*Keywords:* regime; intervention; observational data; experimental design; causal identification; structural causal model; do-calculus; Theory of Data; statistical bridge; evidence provenance; data provenance; observation status

# Abstract

The Theory of Data distinguishes event and spine universes by their point-existence laws. Event points exist through recorded occurrence; spine points exist through declaration, registry, design, or mathematical construction independently of realization. Neither distinction says how values are created at those points. This paper introduces **regime** as a separate governed object: the value-generation arrangement under which a member is produced. Observational and interventional are therefore not additional universe types. They are regime classes that qualify member-generating laws over event and spine universes. The term *regime* has established precedent in decision-theoretic causality and dynamic treatment strategy research; the Theory-of-Data contribution is to place it alongside, but not inside, the universe contract. The paper also separates regime from observation status and provenance: observed versus unobserved concerns support at eligible points, while empirical recording, derivation, and simulation concern how a value came to be available. These are independent contract dimensions rather than one four-valued status.

The distinction clarifies experimental design. A randomized trial begins from a common eligible spine, uses a random assignment mechanism to determine assignment or protocol regime, and produces realized arm-specific evidence under controlled interventional regimes. The control arm is not a normal observational regime merely because the assigned protocol may prescribe no active treatment. Both arms are observed under interventional assignment regimes. Assignment, treatment receipt, treatment-delivery evidence, outcome, and outcome observation remain different governed objects. Under perfect compliance and a sufficiently well-defined treatment protocol, an assigned arm may coincide with a treatment intervention such as $do(X=x)$; under noncompliance it need not. Each arm supplies an event-side record that crosses to a regime-qualified spine-side distribution through its own statistical bridge.

The paper then gives a bounded reading of Judea Pearl's causal framework. Pearl's structural causal models, do-operator, identification theory, and do-calculus correctly distinguish seeing from doing and provide a formal language for deriving interventional and counterfactual queries from data plus causal assumptions. Pearl does not claim that an observational distribution alone determines an intervention distribution. His causal inference engine explicitly includes knowledge, assumptions, a causal model, a query, and data. The important qualification is that the cross-regime structural contract is not derived from the observational-regime distribution that it is later used to transform. Do-calculus can establish that an intervention target is uniquely determined within a class of causal models satisfying the declared assumptions; it does not supply the empirical warrant for those assumptions.

A Theory-of-Data critique follows. The phrase "identified from observational data" compresses two evidentially different inputs: an observational distribution and a cross-regime causal contract. An observational distribution is not a regime-transition law. If an interventional claim is to be empirically warranted rather than merely model-conditional, the regime contract must ultimately be supported by evidence that bears on regime change: randomized or quasi-experimental intervention, natural or engineered policy variation, validated mechanism knowledge, or imported scientific laws whose own provenance extends beyond the same normal observational distribution. The derived interventional target must inherit the evidence status of both the source data and the regime contract.

The contribution is not a new causal calculus and does not reject Pearl's formal results. It adds a data foundation beneath them. The proposed extension introduces a regime determination mechanism, regime-qualified member laws, regime-local statistical bridges, cross-regime contracts, and evidence-status rules. Under this restatement, do-calculus becomes a calculus of derivability through a declared regime bridge, while experimental design remains the direct way to create observed data under intervention regimes.

# Status and contribution

**Version 1.0.** This is the first publication version of the paper. It is written against the published *Theory of Data*, Version 4.0; the regime extension proposed here is intended for later incorporation into the canonical Theory.

This paper proposes an extension to the Theory of Data and a reading of Pearl's causal framework through that extension. It introduces no new estimator, graphical identification theorem, completeness result, or experimental design result. Its definitions and principles are framework proposals about data identity, regime provenance, and evidential status; when the paper describes established causal results, those results retain the scope given by the cited causal-inference literature.

The argument has three parts.

First, it adds **regime** to the Theory of Data. Universe type and regime answer different questions:

- a universe law determines which points exist and why;
- a regime determines how member values are generated at those points.

Second, it locates classical randomized experimental design within the extended framework. Randomization is a regime determination mechanism for assignment or protocol. Treatment and control arms are interventional assignment regimes, not merely values stored in a treatment column. A treatment-receipt intervention such as $do(X=x)$ coincides with an assigned arm only under additional implementation and compliance conditions.

Third, it reclassifies Pearl's contribution. Pearl provides a formal language and calculus for intervention, counterfactuals, identification, mediation, and transportability. The Theory-of-Data critique is not that those derivations are algebraically invalid. It is that the data, structural assumptions, and evidence for cross-regime invariance must remain separate governed objects. Identification under a regime contract is not empirical derivation of that contract from observational data.

The public excerpts of *The Book of Why* available from the authors include the introduction and first two chapters. The technical reading in this paper therefore relies primarily on Pearl's *Causality*, his 2009 overview of causal inference, his work on do-calculus, and his work with Elias Bareinboim on transportability. *The Book of Why* is used as Pearl's own popular exposition of the central claims and of the causal inference engine.

The central thesis is:

> **Event and spine classify how data points exist. Regime classifies how values are created at those points. Observational evidence directly supports statistical inference about distributions within its own regime. Passage to an intervention regime requires a separately declared cross-regime contract. Pearl's calculus can determine what follows under that contract; it cannot derive the contract's empirical warrant from the same observational-regime distribution.**

# 1. The distinction that causal analysis needs

## 1.1 Point existence and value creation are different laws

The Statistical Bridge distinguishes two foundational data-universe types.

An **event universe** contains realized recorded occurrences. A transaction point, detected failure, completed visit, delivered dose, or measured assay point exists in the event universe because the occurrence entered the record.

A **spine universe** contains points established independently of a particular occurrence or observed value. Registered persons, eligible trial participants, scheduled visits, person-time opportunities, calendar months, and future forecast dates are spine points when their existence is determined by a registry, protocol, calendar, eligibility rule, or mathematical construction.

The recent note on extent and absence sharpens the distinction. An anchor defines what one point is. A universe identifies which points exist and supplies their existence law. Support identifies where a member actually has observed values. These are separate objects even when a table presents them as one.

None of these objects determines the value-generation arrangement. The same participant spine can support:

- naturally chosen treatment;
- physician-assigned treatment;
- randomized treatment;
- forced treatment under a protocol;
- no-treatment control;
- a policy intervention;
- a simulated treatment policy.

The points may remain exactly the same while the value-generating process changes.

This motivates a third axis of description, but not a third universe type.

> **A regime is the governed arrangement under which member values are generated, assigned, or induced over an existing universe.**

Universe type concerns point existence. Regime concerns value creation.

## 1.2 Regime is orthogonal to universe type

Let a universe be represented schematically as

$$
U=(\kappa,A,P,\lambda),
$$

where:

- $\kappa\in\{E,S\}$ is the event or spine type;
- $A$ is the anchor;
- $P$ is the point extent;
- $\lambda$ is the point-existence law.

Let $r\in\mathcal R$ identify a regime. For a member $m$, let

$$
K_m^{(r)}
$$

denote the regime-qualified value-generation law.

Then two objects may have the same universe and different regimes:

$$
(U,r_0),
\qquad
(U,r_1).
$$

They may also have different universes under the same regime:

$$
(U_1,r),
\qquad
(U_2,r).
$$

Thus:

$$
\text{universe identity}
\neq
\text{regime identity}.
$$

The distinction is not merely terminological. It prevents three substitutions:

1. treating a treatment value as evidence of intervention;
2. treating a different value distribution as evidence of a different population;
3. treating a shared population as evidence that the value-generating law was unchanged.

## 1.3 Observed is not observational

The words *observed* and *observational* must be separated.

**Observed** is an observation-status statement. A member has a value in the record at an eligible point; equivalently, the point belongs to the member's observed support.

**Observational regime** is a value-generation statement. The system operated under the ordinary or idle mechanism relevant to the causal question, without the intervention being studied. Causal-inference literature also uses *idle regime* and, less consistently, *natural regime* for this case. This paper uses **observational regime** as the primary term because it is the established contrast to **interventional regime**, while using *idle* when the word *observational* could be mistaken for evidence status.

A randomized trial therefore produces observed data under interventional assignment or protocol regimes. Its treatment and control-arm outcomes are observed. They are not thereby generated under the observational regime, and their assignment regime should not be collapsed with treatment receipt when compliance is imperfect.

The phrase "observational universe" should be avoided because it can mean two incompatible things:

- a realized universe of observed records;
- a universe whose values were generated under the noninterventional regime.

This paper uses **observed arm universe** for the realized data from a trial arm and reserves **observational regime** for the ordinary or idle mechanism.

## 1.4 Relation to established terminology

The word **regime** is not introduced here as a new causal term. Several prior traditions already use it.

Dawid's decision-theoretic framework introduces a nonstochastic regime indicator whose values distinguish an observational or *idle* regime from intervention regimes (Dawid 2000, 2021). Causal inference is then reasoning across distributions indexed by that regime indicator. Dawid and Didelez likewise formulate dynamic treatment evaluation through observational and interventional regimes and call the assumptions connecting their probabilistic behavior **stability** (Dawid and Didelez 2010). In the Robins and dynamic-treatment-regime tradition, a **treatment regime** commonly means a static, dynamic, or stochastic decision rule assigning treatment from history (Murphy 2003). Pearl more often writes observational and interventional distributions and represents intervention through the $do$-operator rather than through a named regime indicator.

The Theory of Data should align with this prior art while preserving two distinctions.

First, **regime class** and **specific regime identity** are not the same. The broad classes used here are:

$$
\mathsf{RegimeClass}=\{\text{observational},\text{interventional}\}.
$$

A specific regime may be $do(X=0)$, $do(X=1)$, a stochastic intervention, a dynamic treatment policy $g$, a threshold rule, or a named protocol. Thus the theory does not reduce the causal literature's many treatment regimes to one binary treatment variable.

Second, **regime** is not a synonym for data-generating process. A data-generating process can include point existence, sampling, value generation, recording, and transformation. Regime is narrower: it qualifies the mechanisms by which specified member values are generated or assigned while leaving universe existence as a separate contract.

The term **natural regime** is retained only as an informal alias. It is not adopted as the canonical term because *natural value*, *natural direct effect*, and *natural treatment value* already have technical meanings in causal-inference subliteratures, and because "natural" can misleadingly suggest that the ordinary mechanism is unengineered or normatively privileged.

## 1.5 Observation status, provenance, and evidential status

A second terminological correction is needed. The labels *observed*, *unobserved*, *derived*, and *simulated* do not form one mutually exclusive four-valued classification.

They answer different questions.

### Observation status

Observation status asks whether a member has a value in the record at an eligible point:

$$
\mathsf{ObsStatus}\in\{\text{observed},\text{unobserved}\}.
$$

The more specific reading of an absent value - missing, unknown, structural zero, ineligible, or undefined - depends on universe, eligibility, measure kind, recording completeness, and fill rule. Observation status is therefore part of support and observation contracts.

### Value provenance

Value provenance asks how the available value was produced. Relevant provenance relations include:

- **empirically recorded or measured** - obtained through an interaction with an operational, experimental, or measurement process;
- **derived** - produced by a governed transformation from prior values;
- **simulated or model-generated** - produced by executing a model rather than by interaction with the represented target system.

These categories are not mutually exclusive as a flat enumeration. A derived value may be materialized and therefore observed in a downstream table. A simulated value may also be stored and observed as a digital record. A derived result may combine empirical and simulated inputs. The correct representation is therefore a provenance or lineage graph, not one status flag. This usage is compatible with the W3C PROV distinction among entities, generating activities, and derivation relations such as `wasGeneratedBy` and `wasDerivedFrom` (World Wide Web Consortium 2013).

### Evidential or claim status

A causal target or analytical claim has a further **evidential status**: for example, directly intervention-observed, experimentally estimated, identified under an assumed regime contract, model-implied, simulated, or contradicted by intervention evidence. This is a status of the claim and its warrant, not merely of a value cell.

The resulting architecture has at least four independent questions:

| Contract dimension | Question | Core vocabulary |
|---|---|---|
| Universe type | Why does the point exist? | event / spine |
| Regime | Under which value-generation arrangement does the member arise? | observational (idle) / interventional; then a specific regime identity |
| Observation status | Is a value available at this eligible point? | observed / unobserved, with a governed reading of absence |
| Provenance and warrant | How was the value or claim produced and supported? | empirical recording, derivation, simulation; evidential status and lineage |

A compact descriptor may therefore be written schematically as

$$
(A,U,r,S_m,\Pi_m,\mathcal E_m),
$$

where $A$ and $U$ locate the member, $r$ identifies the regime, $S_m$ is observed support, $\Pi_m$ is provenance, and $\mathcal E_m$ is the evidential status of the resulting claim. No one component substitutes for another.

# 2. A regime extension to the Theory of Data

## 2.1 Regime determination mechanism

A regime must be determined somehow. Let

$$
\rho:P\to\mathcal R
$$

be a **regime determination mechanism** assigning a regime to each eligible point or experimental unit.

Several cases are possible.

### Observational or idle regime determination

The system operates under its ordinary institutional, behavioral, biological, or physical mechanisms relative to the intervention being studied. There may be no explicit regime-assignment variable. Following established causal terminology, this is the observational or idle regime and is declared at the frame level:

$$
\rho(u)=r_{\mathrm{obs}}
\quad\text{for all }u\in P.
$$

Treatment $X$ is then generated by its ordinary mechanism:

$$
X(u)=K_X^{(r_{\mathrm{obs}})}(C(u),U_X(u)),
$$

where $C$ represents measured context and $U_X$ unmeasured background state.

### Randomized regime determination

An experimental design creates an assignment member

$$
Z:P\to\{0,1\}
$$

under a randomization contract. A protocol map determines regime:

$$
\rho(u)=
\begin{cases}
r_0,&Z(u)=0,\\
r_1,&Z(u)=1.
\end{cases}
$$

Here $r_0$ and $r_1$ are interventional **assignment or protocol regimes** determined by the randomization mechanism. They should not automatically be identified with $do(X=0)$ and $do(X=1)$ for treatment actually received. Under perfect compliance and a sufficiently well-defined treatment protocol the two descriptions may coincide; under noncompliance they do not. The assignment mechanism is part of the evidence-production account, not a descriptive label added after the values are observed.

### Policy or natural-experiment regime determination

Regime may be assigned by a threshold, jurisdiction, date, lottery, resource constraint, administrative rule, or exogenous shock. The design is not necessarily randomized by the analyst, but the regime determination law can still be declared and evaluated.

### Model-imposed regime

A simulation or structural model may define a hypothetical intervention regime without realizing it. Such a regime has model status rather than observed intervention status.

## 2.2 Regime-qualified member contract

A governed member already carries an anchor, universe, eligibility, support, observation contract, evidence, and lineage. The regime extension makes the following components explicit and keeps observation status, provenance, and evidential status separate:

- regime identity;
- regime determination mechanism;
- regime-qualified value-generation law;
- intervention target, if any;
- mechanisms declared invariant;
- mechanisms declared replaced;
- provenance of values and transformations;
- evidential status of regime and invariance declarations.

A schematic regime-qualified member is

$$
m^{(r)}=
(A,U,E_m,S_m,K_m^{(r)},O_m^{(r)},\Pi_m,\mathcal E_m),
$$

where:

- $E_m$ is eligibility;
- $S_m$ is observed support;
- $K_m^{(r)}$ is the regime-qualified value-generation law;
- $O_m^{(r)}$ is the observation or recording contract;
- $\Pi_m$ is provenance and lineage;
- $\mathcal E_m$ is the evidential status of regime-qualified claims and declarations.

The value distribution is therefore not written as an unqualified $P(m)$. It is located:

$$
P_U^{(r)}(m).
$$

## 2.3 Regime and member identity

Regime qualification has an identity consequence. Two governed members may share a measure name, anchor, universe, eligibility, and observation definition while representing different analytical objects because their values are generated under materially different regimes.

For a regime-affected outcome, the default is therefore:

$$
Y^{(r_0)}\not\equiv Y^{(r_1)}.
$$

The regime is **identity-bearing** when the member's value-generation law or intended claim materially depends on the regime. A measure may project regime difference away only under a declared **regime-invariance law** establishing that the member or relevant mechanism is unchanged over the stated regime set. Thus a baseline characteristic may retain one member identity across randomized arms under an appropriate invariance declaration, while a treatment-affected outcome normally does not.

This principle is distinct from grain. The member may remain at the same anchor and universe:

$$
\operatorname{Grain}(m)=(U,A),
$$

while its regime-qualified identity differs. Regime answers how values are generated, not where the member lives or why its points exist.

## 2.4 Intervention target and regime-affected members

An intervention usually replaces the mechanism of one member while changing the distributions of downstream members.

Suppose

$$
X=K_X^{(r_{\mathrm{obs}})}(C,U_X),
$$

and

$$
Y=K_Y(X,C,U_Y).
$$

Under the intervention $r_x=do(X=x)$, the mechanism for $X$ is replaced:

$$
K_X^{(r_{\mathrm{obs}})}
\longmapsto
K_X^{(r_x)}(\cdot)=x.
$$

The structural function for $Y$ may remain unchanged, but its distribution changes because its input has changed:

$$
Y^{(r_x)}=K_Y(x,C,U_Y).
$$

Thus the contract should distinguish:

- **intervened member:** the member whose generating mechanism is replaced;
- **regime-affected member:** a member whose distribution changes under the intervention;
- **invariant mechanism:** a member-generation law declared unchanged across regimes.

Calling both $X$ and $Y$ simply "interventional variables" loses this structure.

## 2.5 Universe, regime, observation, and provenance compose

A value does not "live" in an evidence-status category. It lives at an anchor point in a universe; its generating mechanism is regime-qualified; its availability is expressed through support; and its origin is represented through provenance.

The universe-regime combinations are all coherent:

| Universe type | Observational regime | Interventional regime |
|---|---|---|
| **Event** | recorded transaction, diagnosis, failure, or visit arising under ordinary mechanisms | recorded dose, adverse event, compliance event, or response event arising under a protocol |
| **Spine** | recorded or unobserved balance, state, or outcome at a registered or scheduled point under ordinary mechanisms | recorded or unobserved trial outcome at an eligible participant point under an intervention protocol |

For each cell, values may be observed or unobserved. Available values may be empirical, derived, simulated, or connected by a longer provenance chain. Examples include:

- a transaction amount: event universe, observational regime, observed support, empirical recording;
- customer-month revenue: spine universe, observational regime, derived from transaction events;
- a trial participant's measured outcome: spine universe, interventional regime, observed support, empirical measurement;
- an identified $P^{do(x)}(Y)$: spine-side interventional target, derived from observational members through a regime contract, with evidential status inherited from that contract;
- simulated adverse-event realizations under a policy: model-generated provenance under an interventional regime, represented over a declared simulation domain rather than treated as empirically recorded event-universe points;
- simulated demand over future months under business as usual: spine universe under an observational regime, with model-generated provenance.

This composition corrects a common categorical error. **Observed** does not mean observational-regime; **derived** does not mean unobserved; **simulated** does not define a universe type; and **interventional** does not establish empirical observation.

## 2.6 Regime-local bridge

The Statistical Bridge relates realized event-side evidence to spine-side mathematical objects. Regime makes that bridge qualified.

Under regime $r$:

$$
E^{(r)}
\underset{\text{inference}}{\overset{\text{generation}}{\rightleftarrows}}
S^{(r)}.
$$

The forward side states how a regime-qualified spine model could generate possible evidence. The reverse side reasons from realized evidence toward a target in that same regime.

For example, a randomized control arm supplies evidence under $r_0$:

$$
E^{(r_0)}
\longrightarrow
P_S^{(r_0)}(Y).
$$

A treatment arm supplies evidence under $r_1$:

$$
E^{(r_1)}
\longrightarrow
P_S^{(r_1)}(Y).
$$

These are regime-local statistical crossings.

## 2.7 Cross-regime bridge

A causal identification problem introduces another passage:

$$
(S,r)
\longrightarrow
(S,r').
$$

This is not an event-spine crossing. It is a **regime passage** between different value-generation laws over a spine-side domain.

A cross-regime contract must state:

- source regime;
- target regime;
- affected members;
- replaced mechanisms;
- invariant mechanisms;
- source and target populations;
- any anchor or extent changes;
- identification map;
- evidential basis for the invariance and exclusion claims;
- scope of the derived result.

The distinction yields a two-dimensional architecture:

| | Observational (idle) regime | Interventional regime |
|---|---|---|
| **Event side** | realized naturally generated records | realized experimental or policy-regime records |
| **Spine side** | observational-regime value law | intervention-regime value law |

Event and spine remain the foundational universe types. Observational and interventional are regime classes that qualify member-generating laws.

# 3. Experimental design before Pearl

Pearl's do-operator gives a formal semantics to intervention. Randomized experimental design predates that notation and directly creates data under controlled regimes.

## 3.1 Common trial spine

Let

$$
A_T=\{\text{Participant},\text{Trial}\}
$$

be the trial anchor. Let

$$
U_T=(S,A_T,P_T,\lambda_T)
$$

be the eligible enrolled spine. Its extent is established by participant identity, eligibility criteria, enrollment, baseline time, and protocol rules.

The trial spine exists before treatment assignment and before outcome observation.

A broader source or target population may also exist. Sampling or recruitment into the trial is a separate passage:

$$
P_T\subseteq P_{\mathrm{source}}.
$$

Random sampling into the trial and random treatment assignment inside the trial are different mechanisms and support different claims.

## 3.2 Random assignment and realized arms

Let

$$
Z:P_T\to\{0,1\}
$$

be the assignment member generated by a randomization contract $\alpha$.

The assignment event creates two realized arm extents:

$$
P_0=\{u\in P_T:Z(u)=0\},
$$

$$
P_1=\{u\in P_T:Z(u)=1\}.
$$

These arm extents are not two independent baseline spines. They are assignment-derived restrictions of a common trial spine. Their relationship is part of the design:

$$
P_T=P_0\sqcup P_1.
$$

The randomization contract supplies a distribution over possible assignments before the realized partition is observed.

## 3.3 Both arms are interventional

Let the randomization and protocol map assignment to arm-specific regimes:

$$
Z=0\mapsto r_0^{\mathrm{assign}},
$$

$$
Z=1\mapsto r_1^{\mathrm{assign}}.
$$

Both are interventional with respect to the assignment or protocol mechanism. The control arm is not the normal observational regime merely because its protocol prescribes no active treatment: the ordinary treatment-assignment mechanism has been replaced by the trial design in both arms.

This does **not** imply in general that

$$
r_0^{\mathrm{assign}}=do(X=0),
\qquad
r_1^{\mathrm{assign}}=do(X=1),
$$

where $X$ denotes treatment actually received. Under perfect compliance and a sufficiently well-defined treatment protocol, the assigned regime may coincide with the corresponding treatment-receipt intervention. Under noncompliance, assignment and receipt diverge. The arm contrast then identifies an effect of assignment or protocol - the intention-to-treat contrast - while a causal effect of treatment receipt requires additional assumptions (Imbens and Rubin 2015).

The familiar difference between

$$
P(Y\mid X=0)
$$

and

$$
P(Y\mid do(X=0))
$$

therefore remains a difference between naturally untreated points and points whose treatment-receipt mechanism is intervened upon. It should not be used to collapse randomized assignment into treatment receipt when compliance is imperfect.

## 3.4 Assignment, treatment, and delivery

A single `status` column is generally inadequate.

Let:

- $Z$ be randomized assignment;
- $R=\rho(Z)$ be the assigned arm or protocol regime;
- $X$ be treatment actually received;
- $D_X$ be treatment-delivery events or evidence;
- $Y$ be outcome;
- $O_Y$ be the outcome-observation contract.

If $Z$ and $X$ use the same binary coding, perfect compliance may be written:

$$
X=Z.
$$

Under noncompliance:

$$
X\neq Z
$$

for some points. In that case the randomized regime remains the assignment or protocol regime determined by $Z$; the realized treatment-receipt process is a distinct governed object.

Treatment delivery may itself occupy an event universe: prescriptions, administrations, sessions, device activations, or policy applications. These events must be assigned back to the participant spine. Assignment is not delivery; delivery is not recording; recording is not necessarily complete treatment receipt.

## 3.5 Outcome constitution

The outcome may live at another anchor:

$$
A_Y=\{\text{Participant},\text{Follow-up time}\}.
$$

It may be a state-valued member, an event-derived count, a survival outcome, or a reduction of repeated measurements. The experiment must still establish:

- outcome eligibility;
- follow-up origin;
- measurement time;
- competing events;
- loss to follow-up;
- detection and recording;
- reduction to the analysis anchor.

Randomization does not automatically repair a wrongly constituted outcome member.

## 3.6 Experimental bridges

For compact notation, write $r_0$ and $r_1$ in this subsection for the two randomized assignment or protocol regimes defined above. They are not assumed to equal treatment-receipt interventions when compliance is imperfect.

The realized control-arm evidence crosses to the control-regime spine distribution:

$$
E_0^{(r_0)}
\longrightarrow
P_{U_T}^{(r_0)}(Y).
$$

The realized treatment-arm evidence crosses to the treatment-regime spine distribution:

$$
E_1^{(r_1)}
\longrightarrow
P_{U_T}^{(r_1)}(Y).
$$

The experimental contrast is then

$$
\tau_T
=
E_{U_T}^{(r_1)}[Y]
-
E_{U_T}^{(r_0)}[Y].
$$

Under a randomized design and appropriate outcome observation, this arm contrast is directly grounded in evidence produced under the two randomized intervention regimes. Its default causal interpretation is the effect of assignment or protocol. Interpreting the same contrast as the effect of treatment actually received requires the additional conditions under which assignment and receipt coincide or an explicit noncompliance identification argument.

## 3.7 What the experiment validates

An experiment can corroborate or refute an interventional implication. It does not generally prove an entire causal graph or every structural equation.

Suppose a causal model predicts an arm-assignment or protocol contrast

$$
\tau_M^{Z}
=
E_M[Y\mid do(Z=1)]
-
E_M[Y\mid do(Z=0)].
$$

The randomized trial directly estimates the corresponding $\tau_T$ under its design and observation conditions. Under perfect compliance and a sufficiently well-defined treatment, the model may additionally imply the treatment-receipt contrast

$$
\tau_M^{X}
=
E_M[Y\mid do(X=1)]
-
E_M[Y\mid do(X=0)],
$$

and the two contrasts may coincide. Under noncompliance they need not. Agreement therefore supports the particular interventional implication actually matched by the design, population, protocol, compliance, observation, and uncertainty. Several different causal models may imply the same average contrast. Disagreement can arise from a false causal model, failed treatment delivery, noncompliance, outcome misconstitution, recording failure, population difference, or sampling variation.

The evidence remains located.

# 4. Pearl's causal framework correctly read

## 4.1 The ladder of causation

Pearl distinguishes three levels of queries.

**Association** asks about patterns under a regime, such as

$$
P(Y\mid X=x).
$$

**Intervention** asks what distribution would result if a mechanism were changed:

$$
P(Y\mid do(X=x)).
$$

**Counterfactual** asks about a particular unit or evidence state under an alternative intervention:

$$
P(Y_x=y\mid e).
$$

The distinction is substantive. Conditioning selects points within an existing distribution. Intervention modifies the mechanism that creates a value.

## 4.2 Structural causal models

A structural causal model represents endogenous variables through assignments such as

$$
V_i=f_i(\operatorname{pa}_i,U_i),
$$

where $\operatorname{pa}_i$ are causal parents and $U_i$ are exogenous background variables.

The equations are interpreted asymmetrically. They are not merely algebraic equalities. Each assignment represents a mechanism by which the value of one variable is determined from its parents and background conditions.

An intervention $do(X=x)$ replaces the structural assignment for $X$ by a constant:

$$
f_X(\operatorname{pa}_X,U_X)
\longmapsto
X:=x.
$$

The remaining structural assignments are declared unchanged. This is the modularity or autonomy claim on which the intervention semantics depends.

## 4.3 Pearl does not claim data alone are sufficient

Pearl's 2009 overview repeatedly characterizes causal answers as derived from a combination of data and assumptions. *The Book of Why* makes the same point through its causal inference engine. The inputs include:

- knowledge;
- explicit assumptions;
- a causal model;
- a causal query;
- data.

The outputs include:

- a decision about identifiability;
- an estimand;
- a statistical estimate.

This matters for a fair critique. Pearl does not formally claim that an observational joint distribution, by itself, contains the intervention distribution. He explicitly argues that data alone cannot distinguish seeing from doing.

## 4.4 Identification

A causal target is **identified** under a class of causal models when all models in that class that agree on the available observable distribution also agree on the target causal quantity.

Identification is therefore conditional uniqueness:

$$
P^{(r_{\mathrm{obs}})}(V)
+
\mathcal A
\Longrightarrow
Q^{(r_x)},
$$

where $\mathcal A$ is the causal assumption set.

An identification result does not show that $\mathcal A$ is true. It shows what follows if it is true.

Once the target has been expressed as an estimand in observable distributions, conventional statistical methods estimate that estimand from finite data.

## 4.5 Do-calculus

Do-calculus provides transformation rules for expressions containing intervention operators. Its central identification role is to determine whether an interventional query can be rewritten in terms of available observational distributions under the graphical assumptions encoded by the causal model.

Schematically:

$$
P^{(r_x)}(Y)
=
\Phi_{\mathcal A}
\left(P^{(r_{\mathrm{obs}})}(V)\right).
$$

The subscript is essential. The mapping $\Phi_{\mathcal A}$ exists because the causal assumptions connect the regimes. It is not supplied by the observational distribution alone.

Do-calculus is a formal contribution of great importance. It turns assumptions about causal structure into a disciplined derivation rather than an informal adjustment story. The Theory-of-Data critique concerns the provenance and status of $\mathcal A$, not the validity of the derivation conditional on $\mathcal A$.

## 4.6 Transportability

Pearl and Bareinboim's transportability theory makes the role of experimental evidence even clearer. It asks when causal effects learned in experiments in one population can be transported to another population where only passive observations are available. Selection diagrams represent which mechanisms may differ, and do-calculus derives the required combination of experimental and observational distributions.

This work is not an attempt to eliminate intervention evidence. It explicitly organizes how experimental findings and target-population observations can be combined. It is therefore a mature example of a cross-universe and cross-regime contract, even though it does not use Theory-of-Data terminology.

## 4.7 The popular formulation

*The Book of Why* describes predicting intervention effects without actually enacting the intervention as a crowning achievement of the causal revolution. Read casually, this can sound as though observational-regime data themselves contain the intervention distribution.

The book's own inference-engine diagram prevents that reading. Data are only one input. Knowledge, assumptions, and a causal model are separate inputs. The correct technical statement is:

> An intervention target may be computable from observational distributions when a declared causal model makes the target identifiable.

That is different from:

> The intervention target was empirically learned from observational-regime data alone.

# 5. Why the observational distribution cannot determine the intervention distribution

## 5.1 A simple non-derivability example

Let $U\sim\operatorname{Bernoulli}(1/2)$.

Consider two causal models.

### Model A: $X$ causes $Y$

$$
X:=U,
$$

$$
Y:=X.
$$

### Model B: $Y$ causes $X$

$$
Y:=U,
$$

$$
X:=Y.
$$

Both models produce exactly the same observational distribution:

$$
P(X=0,Y=0)=1/2,
$$

$$
P(X=1,Y=1)=1/2.
$$

Thus:

$$
P_A^{(r_{\mathrm{obs}})}(X,Y)
=
P_B^{(r_{\mathrm{obs}})}(X,Y).
$$

But under $do(X=0)$ they disagree.

In Model A:

$$
P_A(Y=1\mid do(X=0))=0.
$$

In Model B, intervening on $X$ does not change $Y$:

$$
P_B(Y=1\mid do(X=0))=1/2.
$$

Therefore:

$$
P^{(r_{\mathrm{obs}})}(X,Y)
\not\Rightarrow
P^{(r_0)}(Y).
$$

The observational distribution alone cannot decide which intervention distribution is correct.

## 5.2 What the graph contributes

A graph $X\to Y$ selects Model A's causal direction. A graph $Y\to X$ selects Model B's.

The graph is therefore not a visualization of the observational distribution. It is a claim about the mechanisms that remain meaningful under intervention. In Theory-of-Data language, it is part of a cross-regime contract.

The graph may be supported by temporal order, physical knowledge, experimental history, institutional design, exclusion restrictions, or causal-discovery assumptions. It is not generally derived from the same two-variable observational distribution.

## 5.3 Observational causal discovery does not remove the issue

Observational data can constrain causal structure. Conditional independences may identify v-structures and orient some edges under Markov, faithfulness, acyclicity, causal sufficiency, and related assumptions (Spirtes, Glymour, and Scheines 2000; Pearl 2009a). Larger variable sets can therefore provide more information than the two-variable example.

But two qualifications remain.

First, the conclusions are conditional on causal-discovery assumptions that are not merely summaries of the observed distribution.

Second, observational data commonly identify a Markov-equivalence class rather than one fully oriented causal graph. Different members of that class may imply different intervention distributions.

Intervention data are one direct way to break those equivalences and test cross-regime predictions.

# 6. The Theory-of-Data critique

## 6.1 Observational data establish regime-local distributions

Evidence produced under the normal regime can support claims about that regime through an appropriate statistical bridge:

$$
E^{(r_{\mathrm{obs}})}
\longrightarrow
P^{(r_{\mathrm{obs}})}.
$$

It may support prediction at future spine points under a stability assumption within the same regime. A regression model can forecast without causal interpretation when the task is to predict under continuation of the value-generation arrangement.

What observational evidence does not establish by itself is the distribution under a changed mechanism:

$$
P^{(r_{\mathrm{obs}})}
\not\Rightarrow
P^{(r_x)}.
$$

## 6.2 The cross-regime contract is a separate input

Pearl's causal assumptions supply a mapping:

$$
\mathcal C_{r_{\mathrm{obs}}\to r_x}.
$$

Then:

$$
P^{(r_x)}(Y)
=
\Phi
\left(
P^{(r_{\mathrm{obs}})}(V),
\mathcal C_{r_{\mathrm{obs}}\to r_x}
\right).
$$

The observational distribution and the regime contract are not interchangeable evidence.

A Theory-of-Data account should preserve:

- where the observational distribution came from;
- where the causal structure came from;
- which mechanisms are assumed invariant;
- which interventions have been observed previously;
- whether the contract is verified, corroborated, transported, mechanistically justified, assumed, or speculative.

## 6.3 Identification does not upgrade assumption status

Suppose do-calculus establishes that a target is identifiable under graph $G$. The resulting estimand may be statistically estimable with high precision. Neither fact upgrades $G$ from an assumption into an observation.

The result inherits two evidence streams:

$$
\mathcal E_{\mathrm{result}}
=
\operatorname{combine}
\left(
\mathcal E_{\mathrm{data}},
\mathcal E_{\mathrm{regime\ contract}}
\right).
$$

A precise estimate under a weakly warranted regime contract remains a precise conditional answer.

## 6.4 Empirical warrant must come from beyond the same observational-regime distribution

The following is a **Theory-of-Data epistemic principle**, not an identification theorem of Pearl's framework: if a causal conclusion is intended as an empirical claim about what an intervention will do, the cross-regime contract needs evidential support.

That support may come from:

- randomized experiments;
- prior controlled interventions;
- natural experiments or policy discontinuities;
- engineered assignment systems;
- intervention data in another population combined through transportability;
- validated physical, biological, or institutional mechanisms;
- repeated regime changes whose consequences are observed.

The present analysis need not itself contain intervention data. The causal contract may be imported from established science. But then the empirical warrant is inherited from prior evidence rather than created by the current observational distribution.

This is the qualified sense in which interventional claims ultimately require regime-bearing evidence. The evidence need not be a randomized trial in the current study, but it must bear on the transition between regimes rather than merely reproduce associations inside one normal regime.

## 6.5 Pearl's theory is conditional, not impossible

Under the extended Theory of Data, the following passage is unavailable:

$$
P^{(r_{\mathrm{obs}})}
\overset{\text{data alone}}{\longrightarrow}
P^{(r_x)}.
$$

The following passage is coherent:

$$
P^{(r_{\mathrm{obs}})}
+
\mathcal C_{r_{\mathrm{obs}}\to r_x}
\overset{\text{identification}}{\longrightarrow}
P^{(r_x)}.
$$

Pearl's theory supplies the formal semantics and identification calculus for the second expression. It does not make the first expression valid.

The critique is therefore not that Pearl's causal theory is mathematically impossible. It is that the common phrase "learn the causal effect from observational data" can obscure the separately supplied regime contract and its evidential provenance.

## 6.6 A bounded reformulation

A more accurate statement is:

> **An interventional target is derivable from observational distributions only through a declared cross-regime causal contract. That contract is not derived from the same observational-regime distribution. If the target is to be empirically warranted rather than merely model-conditional, the contract must carry evidence whose provenance bears on regime change.**

# 7. Misunderstandings that the regime framework corrects

## 7.1 Mistaking treatment value for intervention

False:

$$
X=1
\Rightarrow
do(X=1).
$$

Correct:

$$
do(X=1)
$$

is a claim about how the value was generated: the ordinary mechanism was replaced by an intervention mechanism.

## 7.2 Treating the control arm as observational

A randomized control arm is generated under a controlled assignment or protocol regime. It is observed data under an intervention regime, not passive evidence under the normal treatment-assignment mechanism. Only under perfect compliance and an adequately specified treatment does that assigned regime coincide with a treatment-receipt intervention such as $do(X=0)$.

## 7.3 Collapsing assignment and receipt

Random assignment $Z$, treatment receipt $X$, and treatment-delivery events $D_X$ may differ. Intention-to-treat, per-protocol, and treatment-received effects target different regime relations and require different assumptions.

## 7.4 Treating the causal graph as a fitted summary

A causal graph is not a graphical rendering of correlations. It encodes asymmetry, exclusion, and intervention stability. It is part of a regime-transition contract.

## 7.5 Treating identification as empirical verification

Identification proves that the target is uniquely determined under a model class. It does not establish that the model class describes the world.

## 7.6 Treating estimation precision as causal confidence

A narrow standard error quantifies finite-data uncertainty for the identified estimand. It does not quantify uncertainty about omitted confounding, wrong edge direction, failed modularity, or invalid transport unless those are explicitly modeled.

## 7.7 Treating prediction as intervention

A predictive model may forecast future outcomes under continuation of the same regime:

$$
P^{(r)}(Y_{t+1}\mid H_t).
$$

A policy forecast asks about a changed regime:

$$
P^{(r')}(Y_{t+1}).
$$

Only the second requires a regime-transition law. Forecasting is not inherently causal.

## 7.8 Treating counterfactual non-realization as ordinary missingness

An unobserved factual value is missing at an eligible point under the realized regime. A counterfactual value belongs to an unrealized regime. Its absence is not a recording failure. It is a consequence of mutually exclusive regime realization and requires a causal coupling, not a fill rule.

## 7.9 Treating one successful experiment as validation of the whole SCM

An experiment tests selected intervention implications under a declared population and protocol. It need not identify every causal direction, mediator relation, individual counterfactual, or transport claim in the structural model.

# 8. Proposed Theory-of-Data objects and principles

The definitions and principles in this section are proposed Theory-of-Data framework statements. They organize the identity, provenance, and evidential status of causal data objects; they are not presented as new identification theorems or replacements for established causal calculi.

## 8.1 Regime

> **Definition.** A regime is a governed value-generation arrangement over one or more members on declared universes. It identifies the mechanisms under which values are assigned, produced, or induced.

A regime is not a universe type. It does not, by itself, determine which points exist.

## 8.2 Regime determination mechanism

> **Definition.** A regime determination mechanism is a governed rule $\rho$ assigning a regime to eligible points or declaring one regime for a frame.

It may be natural, randomized, threshold-based, policy-based, or model-imposed.

## 8.3 Regime-qualified member

> **Definition.** A regime-qualified member is a governed member whose contract includes its regime identity, generation law, observation law, and evidence provenance.

Write:

$$
m^{(r)}:P\rightharpoonup X.
$$

The partiality refers to eligibility and observation, not uncertainty about regime identity.

## 8.4 Regime-sensitive member identity

> **Principle.** Regime is identity-bearing for a member when the member's value-generation law or intended claim materially differs across regimes. A declared regime-invariance law may project multiple regimes to one member identity only over the scope for which that invariance is warranted.

Consequently, a regime-affected outcome $Y^{(r_0)}$ and $Y^{(r_1)}$ are different member identities by default even when they share anchor and universe. This does not change analytical grain: $\operatorname{Grain}(m)=(U,A)$ remains the location-and-population descriptor.

## 8.5 Regime-locality principle

> **Principle.** Data generated under regime $r$ directly support statistical inference about distributions and members under regime $r$. They do not, by themselves, determine distributions under another regime $r'$.

## 8.6 Cross-regime non-derivability principle

> **Principle.** In general, $P^{(r)}$ does not determine $P^{(r')}$. A passage between regimes requires an additional contract stating which mechanisms change and which remain invariant.

The two-model example in Section 5 is a constructive witness.

## 8.7 Regime-evidence principle

> **Theory-of-Data epistemic principle.** A result derived through a cross-regime contract inherits the evidence status of that contract. Identification does not convert an assumption into an observed fact.

## 8.8 Experimental grounding principle

> **Principle.** A randomized experiment produces observed evidence under multiple interventional assignment or protocol regimes by a governed randomization mechanism. Its arm contrast is licensed by the design as a contrast of assignment regimes, subject to outcome observation. A treatment-receipt interpretation additionally depends on implementation, compliance, and any assumptions required to relate assignment to receipt.

## 8.9 Regime bridge contract

A regime bridge contract may be represented schematically as

$$
\mathcal C_{r\to r'}
=
(U,A,r,r',I,J,\Phi,\mathcal E,\mathcal L),
$$

where:

- $U$ is the relevant universe or universe relation;
- $A$ is the anchor or anchor relation;
- $I$ is the set of mechanisms replaced or intervened upon;
- $J$ is the set of mechanisms declared invariant;
- $\Phi$ is the identification or transport mapping;
- $\mathcal E$ is evidence status;
- $\mathcal L$ is lineage.

This is a conceptual signature, not yet a formal calculus.

## 8.10 Evidential statuses for causal claims and results

A causal member, target, or returned claim should carry an evidential status distinct from its observation status and value provenance. Useful statuses include:

- directly intervention-observed;
- experimentally estimated;
- observationally identified under an intervention-verified contract;
- observationally identified under an experimentally corroborated contract;
- observationally identified under a mechanistically supported contract;
- observationally identified under an assumed contract;
- model-implied but unidentified;
- simulated;
- contradicted by intervention evidence.

The displayed numerical value may be identical across several statuses. The claim is not. These are claim-level warrant classes; they do not replace member support or provenance lineage.

# 9. Relationship to the Statistical Bridge

The Statistical Bridge distinguishes the inward and outward passages of statistical work.

Under the regime extension, every statistical bridge is regime-qualified:

$$
E^{(r)}
\rightleftarrows
S^{(r)}.
$$

Causal analysis adds a second passage:

$$
S^{(r)}
\longrightarrow
S^{(r')}.
$$

The complete route from observational-regime records to an intervention claim is therefore:

$$
E^{(r_{\mathrm{obs}})}
\longrightarrow
S^{(r_{\mathrm{obs}})}
\longrightarrow
S^{(r_x)}.
$$

The first arrow is a statistical bridge. The second is a regime bridge.

An experimental route differs:

$$
E^{(r_x)}
\longrightarrow
S^{(r_x)}.
$$

Here the evidence was produced under the target intervention regime, so no observational-to-interventional passage is required for that target-regime distribution. A randomized assignment arm is such a direct route for the assignment-regime distribution; treatment-receipt effects under noncompliance remain a separate identification problem.

This distinction localizes disagreements that are often compressed into one term, "causal inference."

# 10. Relationship to Regression Has an Anchor

*Regression Has an Anchor* argues that a fitted regression is a member with a home anchor and universe, not a law that automatically applies elsewhere. Movement to another time, population, grain, or predictor domain requires a separate law.

The regime extension adds another coordinate to that home:

$$
H_m=(A,U,r,K_m^{(r)},S_m,O_m,\Pi_m,\mathcal E_m).
$$

A regression forecast under continuation of $r$ may be valid without causal assumptions. The needed premise is predictive stability:

$$
P_{t+1}^{(r)}(Y\mid X)
\approx
P_t^{(r)}(Y\mid X).
$$

A policy forecast under $r'$ requires more:

$$
P_{t+1}^{(r')}(Y).
$$

The fitted association under $r$ does not determine that distribution.

Thus the regression and causal papers share a form:

> **A fitted member is not a law. An observational distribution is not a regime-transition law.**

The first guards against unsupported movement across anchors and universes. The second guards against unsupported movement across value-generation regimes.

# 11. Pearl's contribution after the critique

The Theory-of-Data restatement leaves Pearl with a major and precise contribution.

## 11.1 A language for regime-changing queries

Pearl supplied notation that separates conditioning from intervention and intervention from counterfactuals. This ended the practice of trying to express causal questions using probability syntax that lacked an intervention operator.

## 11.2 A structural semantics

Structural causal models represent causal direction through autonomous assignments rather than symmetric equations. Interventions are defined as mechanism replacements.

## 11.3 Identification as a formal problem

Pearl made it possible to ask whether a causal query follows from a declared assumption set before choosing an estimator or collecting more of the wrong kind of data.

## 11.4 Do-calculus and completeness

Do-calculus provides a general symbolic method for eliminating intervention operators when the causal graph licenses it. For causal effects in recursive semi-Markovian models, Shpitser and Pearl (2006a) gave a necessary-and-sufficient identification characterization and used it to prove completeness of do-calculus for that identification problem; Huang and Valtorta (2006) independently proved completeness through a sound-and-complete identifiability algorithm. Related work established complete identification conditions for conditional interventional distributions (Shpitser and Pearl 2006b). The claim here is limited to the scopes established in those results, not to every causal query or model class.

## 11.5 Mediation, counterfactuals, and probabilities of causation

The framework provides a common semantics for direct and indirect effects, individual counterfactual queries, and attribution questions that ordinary associational statistics cannot express.

## 11.6 Transportability and meta-synthesis

Pearl and collaborators formalized the combination of experimental and observational evidence across populations. This is close to the regime-and-universe architecture proposed here.

The critique therefore narrows the interpretation rather than diminishing the mathematics:

> **Pearl supplies a calculus of causal consequence under a declared regime contract. The Theory of Data supplies a governance layer for the data objects, regime provenance, and evidence status of that contract.**

# 12. A practice declaration for causal analyses

A causal analysis should record at least the following.

## 12.1 Target

- target anchor;
- target universe and extent law;
- source and target populations;
- target regime;
- causal functional or counterfactual query.

## 12.2 Source data

- native anchors and universes;
- observed supports;
- event and spine roles;
- member construction;
- missingness, detection, and fill rules;
- source regime or regimes under which the records arose, whether observational or interventional.

## 12.3 Regime contract

- intervention target member;
- ordinary generation mechanism;
- replacement mechanism;
- mechanisms declared invariant;
- regime determination mechanism;
- evidence supporting those declarations.

## 12.4 Identification

- causal graph or SCM;
- adjustment, front-door, instrumental, mediation, transport, or other identification argument;
- estimand derived from the assumptions;
- positivity and support requirements.

## 12.5 Estimation

- estimator;
- probability source;
- conditioning;
- finite-data uncertainty;
- sensitivity analysis.

## 12.6 Return claim

- whether the result is intervention-observed or observationally identified;
- evidence status of the regime contract;
- population and regime scope;
- untested invariance assumptions;
- transport limits.

# 13. Research program

## 13.1 Formal regime contracts

Extend the Theory-of-Data contract calculus with regime identity, determination, intervention replacement, mechanism invariance, and evidence inheritance.

## 13.2 Composition with event and spine bridges

Define when regime passage commutes with anchor movement, event reduction, sampling, missingness, and observation. A treatment may be assigned at one anchor, delivered through events at another, and evaluated at a third.

## 13.3 Experimental certification

Represent randomization algorithms, allocation probabilities, concealment, compliance, delivery evidence, and outcome observation as machine-checkable or evidence-ranked declarations.

## 13.4 Causal-graph typing

Attach anchors, universes, regimes, and member contracts to graph nodes. Require edges crossing anchors to carry transport or reduction rules. Distinguish causal roles from data-construction types.

## 13.5 Regime-evidence audit

Study published observational causal analyses and classify the evidence status of their cross-regime contracts. Record how often the graph is supported by prior intervention evidence, mechanistic law, temporal design, convention, or unsupported assumption.

## 13.6 Interventional validation

Compare observationally identified effects with later intervention-regime evidence. Separate failures of the structural contract from failures of data constitution, compliance, observation, and transport.

## 13.7 Counterfactual coupling

Develop the relation between regime-qualified spines and unit-level counterfactual identity. A cross-world coupling is additional structure beyond ordinary missingness and beyond regime-local distributions.

# 14. Boundaries

This paper does not claim:

- that randomized experiments are the only source of causal knowledge;
- that observational studies cannot make useful causal arguments;
- that mechanistic knowledge is reducible to trial data;
- that Pearl concealed the role of assumptions in his technical work;
- that do-calculus is invalid;
- that every causal assumption can be empirically tested;
- that intervention evidence validates an entire SCM;
- that regime replaces event or spine as a universe type.

The narrower claim is that causal conclusions combine different kinds of objects and evidence. The observational distribution, the cross-regime contract, the identification derivation, and the intervention target should not be collapsed into one phrase.

# 15. Conclusion

The Theory of Data begins by asking what the data objects are. Event and spine universes answer why analytical points exist. They do not answer how values were generated at those points. Causal prior art already provides a useful name for that second question: regime. Dawid's regime indicators, observational or idle regime, and interventional regimes; the treatment-regime literature's static and dynamic decision rules; and Pearl's observational and interventional distributions all address related structures. The contribution here is to type regime as a contract dimension orthogonal to universe, support, and provenance.

Causal analysis requires that additional question. A regime is the governed value-generation arrangement under which members arise. Observational and interventional are therefore regimes, not foundational universe types. A randomized experiment begins from a common trial spine, assigns interventional arm or protocol regimes through a governed randomization mechanism, and produces observed evidence under both control and treatment assignment regimes. The control arm is no more observational in Pearl's passive sense than the treatment arm. Assignment, treatment receipt, delivery, outcome, and observation remain distinct; an assigned arm coincides with a treatment-receipt intervention only under the conditions that make that equivalence valid.

Pearl's causal framework correctly identifies the conceptual gap between seeing and doing. Structural causal models encode asymmetric mechanisms. The do-operator represents mechanism replacement. Identification asks whether an interventional target is uniquely determined by available distributions under declared causal assumptions. Do-calculus supplies a disciplined method for performing that derivation.

The Theory-of-Data critique begins where that derivation obtains its premises. An observational distribution does not determine a regime-transition law. Two causal models can generate the same observational distribution and disagree under intervention. A graph or SCM supplies the missing cross-regime contract, but the contract is a separate input whose empirical warrant is not produced by the same observational-regime distribution.

The correct statement is therefore not that Pearl extracts intervention effects from observational data alone. It is that an intervention target may be derivable from observational distributions under a declared causal regime contract. If the resulting claim is to be empirically warranted rather than merely model-conditional, that contract must carry evidence whose provenance bears on regime change, whether through direct experiments, natural interventions, transported experimental findings, or validated mechanism knowledge.

This restatement preserves Pearl's contribution and clarifies its boundary. Do-calculus is a calculus of derivability through a regime bridge. It is not the empirical source of the bridge.

The proposed Theory-of-Data extension makes the distinction governable:

> **A regime has a contract. An observational distribution is not a regime-transition law. A causal result inherits the evidential status of the bridge that carries it from observation to intervention.**

# References

Bareinboim, E., and Pearl, J. (2013). "A General Algorithm for Deciding Transportability of Experimental Results." *Journal of Causal Inference* 1(1): 107-134. https://doi.org/10.1515/jci-2012-0004.

Dawid, A. P. (2000). "Causal Inference without Counterfactuals." *Journal of the American Statistical Association* 95(450): 407-424. https://doi.org/10.1080/01621459.2000.10474210.

Dawid, A. P. (2021). "Decision-Theoretic Foundations for Statistical Causality." *Journal of Causal Inference* 9(1): 39-77. https://doi.org/10.1515/jci-2020-0008.

Dawid, A. P., and Didelez, V. (2010). "Identifying the Consequences of Dynamic Treatment Strategies: A Decision-Theoretic Overview." *Statistics Surveys* 4: 184-231. https://doi.org/10.1214/10-SS081.

Fisher, R. A. (1935). *The Design of Experiments*. Edinburgh: Oliver and Boyd.

Imbens, G. W., and Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction*. Cambridge: Cambridge University Press.

Huang, Y., and Valtorta, M. (2006). "Pearl's Calculus of Intervention Is Complete." In *Proceedings of the Twenty-Second Conference on Uncertainty in Artificial Intelligence*, 217-224. AUAI Press.

Murphy, S. A. (2003). "Optimal Dynamic Treatment Regimes." *Journal of the Royal Statistical Society, Series B* 65(2): 331-355. https://doi.org/10.1111/1467-9868.00389.

Neyman, J. (1990 [1923]). "On the Application of Probability Theory to Agricultural Experiments: Essay on Principles, Section 9." Translated and edited by D. M. Dabrowska and T. P. Speed. *Statistical Science* 5(4): 465-472. https://doi.org/10.1214/ss/1177012031.

Pearl, J. (2009a). *Causality: Models, Reasoning, and Inference*. 2nd ed. Cambridge: Cambridge University Press.

Pearl, J. (2009b). "Causal Inference in Statistics: An Overview." *Statistics Surveys* 3: 96-146. https://doi.org/10.1214/09-SS057.

Pearl, J. (2012). "The Do-Calculus Revisited." In *Proceedings of the Twenty-Eighth Conference on Uncertainty in Artificial Intelligence*, 3-11. arXiv:1210.4852.

Pearl, J. (2019). "The Seven Tools of Causal Inference, with Reflections on Machine Learning." *Communications of the ACM* 62(3): 54-60. https://doi.org/10.1145/3241036.

Pearl, J., and Bareinboim, E. (2011). "Transportability of Causal and Statistical Relations: A Formal Approach." *Proceedings of the Twenty-Fifth AAAI Conference on Artificial Intelligence* 25(1): 247-254. https://doi.org/10.1609/aaai.v25i1.7861.

Pearl, J., and Bareinboim, E. (2014). "External Validity: From Do-Calculus to Transportability Across Populations." *Statistical Science* 29(4): 579-595. https://doi.org/10.1214/14-STS486.

Pearl, J., Glymour, M., and Jewell, N. P. (2016). *Causal Inference in Statistics: A Primer*. Chichester: Wiley.

Pearl, J., and Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. New York: Basic Books.

Rubin, D. B. (1974). "Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies." *Journal of Educational Psychology* 66(5): 688-701. https://doi.org/10.1037/h0037350.

Shpitser, I., and Pearl, J. (2006a). "Identification of Joint Interventional Distributions in Recursive Semi-Markovian Causal Models." In *Proceedings of the Twenty-First National Conference on Artificial Intelligence*, 1219-1226. AAAI Press.

Shpitser, I., and Pearl, J. (2006b). "Identification of Conditional Interventional Distributions." In *Proceedings of the Twenty-Second Conference on Uncertainty in Artificial Intelligence*, 437-444. AUAI Press.

Spirtes, P., Glymour, C., and Scheines, R. (2000). *Causation, Prediction, and Search*. 2nd ed. Cambridge, MA: MIT Press.

World Wide Web Consortium. (2013). *PROV-DM: The PROV Data Model*. W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-dm/.

Wang, H. (2026a). *The Theory of Data: Governed Analytical Objects, Lawful Transformation, and Certification*. Version 4.0. datumwise. https://doi.org/10.5281/zenodo.21774032.

Wang, H. (2026b). *The Statistical Bridge: From Events to Spines, Data Work, and the Interpretation of Results*. Version 1.0. datumwise.

Wang, H. (2026c). *Regression Has an Anchor: Members, State, and Lawful Movement in the Most Performed Analysis in Statistics*. Version 1.0. datumwise. https://doi.org/10.5281/zenodo.21783729.

Wang, H. (2026d). *Missingness Has a Universe: A Typed and Compositional Foundation for Missing-Data Research*. Version 2.0. datumwise. https://doi.org/10.5281/zenodo.21783563.

Wang, H. (2026e). *Extent, Missing Points, and the Readings of Absence*. Internal working note, version 0.2. datumwise.

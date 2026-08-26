---
title: "The Theory of Certainty"
subtitle: "Grounds for Analytical and Operational Reliance"
author: "Huayin Wang"
date: "Version 1.0 - 26 August 2026"
lang: en-US
papersize: letter
geometry: margin=0.9in
fontsize: 11pt
subject: "A concise theory of the grounds sufficient for analytical and operational reliance"
keywords:
  - Theory of Certainty
  - analytical governance
  - operational reliance
  - grounds of certainty
  - theory of object
  - theory of other
  - behavioral evidence
  - AI agents
  - trust
  - statistical inference
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
    \fancyhead[L]{\small The Theory of Certainty}
    \fancyhead[R]{\small Huayin Wang}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \setlength{\headheight}{14pt}
  - |
    \urlstyle{same}
---

**datumwise, an independent open-source research project**  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**DOI:** 10.5281/zenodo.22114802

## Abstract

The Theory of Certainty develops a concise framework for analytical and operational reliance. Its central claim is that the same expectation can rest on different grounds of certainty, and those grounds are not interchangeable. The paper distinguishes three important families of ground: theory of object, which relies on knowledge of laws, rules, mechanisms, machinery, or code; theory of other, which uses a generative model of how an intelligent actor arrives at action; and behavioral evidence, which relies on observed regularity within a warranted regime. It then develops three practical consequences: each ground has a limited reach, grounds may compose without losing their identity, and the certainty sufficient for reliance depends on the exposure created by that reliance. A substitution error occurs when certainty earned on one ground is spent as though another ground had been established. The framework is applied to analytical population errors and to current general-purpose AI agents, where object-level constraints, models of the actor, and behavioral evaluation often provide substantial but differently bounded grounds. The resulting discipline is operational: identify what is carrying the certainty, determine what it establishes, find where its warrant stops, and ask whether it can bear the contemplated reliance.

This is a theory of certainty for analytical and operational reliance. Certainty matters when something is going to depend on it.

An analyst serves a result. A statistical model supports a claim. An operator authorizes an action. A person relies on another person. A system lets an agent cross a consequential boundary. In each case, the practical question is not whether uncertainty has disappeared. It is whether there are grounds strong enough for the reliance being placed on them.

This paper uses **certainty** in that narrow operational sense: being sufficiently sure, on warranted grounds, for the reliance at issue. It is not a philosophical theory of certainty, and it does not attempt a comprehensive treatment of probability, knowledge, decision theory, reliability, or trust. Its concern is smaller: the grounds on which analytical and operational reliance can be warranted, the limits of those grounds, and what happens when one kind of certainty is mistaken for another.

The central claim is simple:

> **The same expectation can rest on different grounds of certainty. Those grounds are not interchangeable.**

Here certainty means warranted confidence sufficient for the reliance at issue. A ground is what warrants that confidence. The reach of a ground is the conditions over which its warrant holds. Reliance is the use or decision that depends on the expectation; exposure is what that reliance places at stake. To spend a ground is to use it as warrant for a conclusion, decision, or action.

Three families of ground are especially important here: a theory of the object, a theory of the other, and behavioral evidence. They are not claimed to be exhaustive or mutually exclusive. They often work together, but they establish different things and fail differently.

# 1. Same expectation, different grounds

Suppose I am certain that you will not enter a room tomorrow.

There are several ways I might have reached that conclusion.

The door may be locked and you may not have a key. My certainty rests on the structure of the situation: what the door permits, what you can do, and what constraints hold.

You may have the key but have committed not to enter. My certainty now depends on my understanding of you as an actor: your capability, constraints, motives, principles, commitments, and the circumstances in which you will choose.

Or I may simply have observed that you have walked past the room every day for a year. My certainty rests on behavioral evidence and on whatever warrants carrying that pattern into tomorrow.

The expected behavior is the same. The grounds are not.

Give you a key and the first ground changes. Give you a powerful reason to enter and the second may need to be reconsidered. Change the conditions under which the behavioral record was accumulated and the third may no longer generalize.

This is the first distinction of the theory: **certainty about a behavior does not identify what is carrying that certainty.**

For analytical and operational work, that distinction matters because different grounds support different conclusions, over different conditions, with different failure modes.

# 2. Three grounds of certainty

## Theory of object

Theory of object grounds certainty in knowledge of the target thing or system itself: the physical laws, formal rules or specifications, mechanisms and machinery, or software code that govern its behavior.

A physical object may be understood through physical law and material constitution. A machine may be understood through its mechanism, engineered design, and constraints. A software system may be understood through its specification and code. In each case, the ground of certainty comes from understanding what governs the object's behavior, rather than primarily from observing a pattern of past behavior.

This knowledge may establish that an outcome must occur, cannot occur, or is constrained to a particular range. Its strength depends on how completely the relevant object, governing rules, state, and operating conditions are known. Having access to a mechanism or source code does not by itself make behavior easy to determine; it identifies the kind of ground on which the certainty is being sought.

The distinction is therefore not between kinds of objects. The same machine or software system may also be understood behaviorally. “I know what this system will do because I know how it works” and “I expect what this system will do because I have observed how it behaves” are different grounds of certainty about the same target.

## Theory of other

A theory of the other becomes relevant when the target of reliance is an actor with meaningful discretion. As used here, it is an operational model of action, not a general psychological theory of another mind. It grounds certainty by modeling how that other generates action, rather than by extrapolating behavior alone.

The generative model includes at least four familiar constituents: goals or motives; intellect and knowledge; principles or self-regulation; and environment. Intellect is especially important because action is chosen against the situation as represented by the other, not simply the situation as known by us. Information, knowledge, perception, bias, memory, and limitation can make those two environments materially different.

A door may in fact be unlocked while the other believes it is locked. Theory of object tells us that entry is structurally possible. A theory of the other may still predict that the person will not attempt entry because the represented environment differs from the actual one. The same distinction applies to capability: what an actor can do and what the actor believes it can do need not coincide.

This is familiar in human reliance and appears, less completely, with trained animals and other adaptive actors. The model need not be verbal or philosophical. It needs only to provide a warranted basis for expecting choice beyond memorized behavior.

Trust belongs especially here. It is not the whole theory of certainty; it is one form of reliance in which a generative model of another actor materially carries the expectation.

## Behavioral evidence

**Behavioral evidence** grounds certainty in what has been observed.

A component has failed at a measured rate. A model has passed an evaluation set. A person has honored a commitment repeatedly. An agent has refused a class of requests in testing.

This evidence can be extremely strong. Its limitation is not that it is “only behavior.” Its limitation is that its warrant depends on the conditions under which the behavior was observed and on the conditions over which the pattern is expected to generalize.

A change of population, environment, incentives, measurement process, deployment conditions, or actor can change that warrant. Responsive subjects can make the problem sharper because measurement or deployment may itself alter behavior. None of this makes behavioral evidence invalid. It means that behavioral certainty has a regime.

The Statistical Bridge develops one important case: the passage from governed evidence through formal inference to licensed claims. Here the relevant point is simply that evidence does not carry its own interpretation, and a formal result does not carry its own empirical applicability. The warranted passage must be established.

| **Ground**          | **What carries certainty**                                                                             | **Characteristic failure**                                           | **Common substitution**                                                                                     |
|---------------------|--------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Theory of object    | Law, rule, mechanism, machinery, code, structural constraint                                           | Relevant state, condition, rule, or mechanism is incomplete or wrong | Treating constraint as competence                                                                           |
| Theory of other     | Generative model of goals or motives, represented situation, reasoning, principles and self-regulation | The model of how the other arrives at choice is wrong or incomplete  | Treating our situation as the other's, assigned objective as motive, or represented principle as commitment |
| Behavioral evidence | Observed behavior under relevant conditions                                                            | The evidence is carried beyond the regime it warrants                | Treating history as structural impossibility                                                                |

# 3. Grounds are not interchangeable

The most important error is not uncertainty itself. It is using certainty earned on one ground as though another ground had been established.

Repeated safe behavior does not establish that unsafe behavior is structurally impossible.

A declared principle does not establish fidelity to that principle.

A high evaluation score does not by itself establish authority for a particular claim.

A formal derivation does not establish that its premises describe the world to which the conclusion is being applied.

These are not objections to behavior, declarations, constraints, evaluations, or derivations. Each can be a legitimate ground. The error is substitution.

Consider a simple analytical case. Revenue rows arrive for 47 stores, and the arithmetic can compute total revenue divided by 47. The request, however, is average revenue per open store. The observed rows establish which stores reported revenue; they do not by themselves establish that those 47 stores were the open-store population.

A roster may establish that 50 stores exist. An operating-status source may establish that 48 were open. Historical feed completeness may provide behavioral evidence that reported stores usually match open stores. These grounds answer different questions. More precise arithmetic on the 47 rows cannot establish the missing population ground.

The substitution error is therefore analytical, not merely statistical: a computable denominator is spent as though the ground required by the requested denominator had already been established.

The honest remedies follow from the missing ground. Establish the open-store population from an appropriate source; narrow the claim to the stores actually observed; disclose the limitation if the narrower result is still useful; or decline to serve the requested interpretation. More arithmetic on the 47 rows cannot substitute for any of these.

Applied to this case, the discipline is compact:

- **What is carrying the certainty?** The reported rows and the arithmetic performed on them.

- **What does that establish?** Mean revenue among the stores that reported revenue.

- **Where does the warrant stop?** It does not establish the open-store population or the process that produced the missing rows.

- **What is the exposure?** If the figure sets a published KPI, compensation, or an operational decision, the missing population ground can matter materially.

- **What substitution occurred?** The observed denominator was used as though it were the requested denominator.

> **A ground of certainty may be spent only for what that ground warrants.**

This principle explains why additional evidence does not always repair a weak reliance. If the missing ground is structural, more examples of good behavior may improve confidence without establishing the needed constraint. If the missing ground concerns the applicability of an inference, a more precise calculation does not establish the missing passage. If the missing ground concerns an actor's commitment, eloquent declarations do not establish fidelity.

The first task in a certainty problem is therefore not to ask only \*how confident are we?\* It is to ask:

> **What is carrying the confidence?**

# 4. Every ground has a reach

No useful ground is unlimited.

A proof has premises. A structural constraint has a boundary. A commitment has conditions under which it is expected to hold. Behavioral evidence has a warranted regime. A statistical claim has the evidence, assumptions, target, and inferential passage that license it.

Reach includes both the conditions of application and the period over which those conditions are presumed to hold. A mechanism may be modified, a permission boundary reconfigured, an actor's goals or knowledge may change, and behavioral evidence may cease to represent the current regime. Certainty should therefore be re-evaluated when the ground or the conditions under which it carries materially change.

This gives a second general rule:

> **Certainty travels only as far as its grounds warrant.**

The rule is easy to violate because conclusions travel more easily than their grounds. A number moves from analysis to slide. A model score becomes a reputation. A successful evaluation becomes “reliable.” A principle stated in a system prompt becomes “aligned.” A claim licensed under one population becomes a claim about another.

The visible conclusion remains while the conditions that carried it disappear.

Good governance therefore preserves more than the conclusion. It preserves enough of the ground to know where the conclusion is entitled to travel.

This is why assumptions, evidence, certificates, claim scope, and behavioral regime cannot be treated as incidental documentation: they are part of what tells us how far a conclusion may travel.

# 5. Reliance adds exposure

Certainty becomes operational when someone relies on it.

The same grounds may be sufficient for one reliance and insufficient for another. A model's demonstrated accuracy may be entirely adequate for suggesting a chart title and inadequate for changing prices across a region. A weakly supported forecast may be useful for exploration and unacceptable as the sole basis for an irreversible decision.

Nothing about the evidence necessarily changed. The exposure did.

This gives the third rule:

> **The certainty required is relative to the reliance and its exposure.**

This does not mean that risk can legalize a bad analytical object or repair an unsupported claim. Some questions must be settled before risk is relevant. Analytical Governance makes the separation explicit: whether a result is supported and analytically established is a different question from whether later risk and authority conditions permit it to be served or executed.

Exposure instead answers a later question: given what has been established, is it enough for what we are about to place at stake?

The practical consequence is straightforward. When available grounds cannot bear the contemplated reliance, there are only a few honest directions: strengthen the grounds, reduce the exposure, narrow the claim or action, or change the boundary at which consequential reliance occurs.

# 6. Grounds can compose

Operational certainty rarely rests on one ground alone.

A system may combine structural constraints with behavioral evaluation. A human relationship may combine enforceable constraints, observed history, and trust. An analytical claim may combine governed data, a statistical model, declared assumptions, and a certificate of inference.

Composition can strengthen certainty. It does not erase the identity of the grounds.

Structural constraint and theory of other compose without becoming the same ground. A permission boundary can establish the actual action space by making one class of actions unavailable. A theory of other addresses how the actor is likely to choose within the action space as the actor represents it. A contract or enforcement regime may alter both: it can objectively constrain consequences and also change the actor's perceived incentives or available choices.

Institutional artifacts are not treated here as a fourth family of ground. A contract, authorization, certificate, role, or governed crossing matters according to what it establishes: it may constrain the actual action space, alter the situation represented by an actor, certify a proposition through a governed process, or combine these functions.

> Structural constraint establishes what actions are actually available; theory of other models choice among the actions the other believes are available.

For example, an analytical agent may be structurally prevented from executing against a database while behavioral evaluation supports confidence that it formulates requests well. A theory of other may separately support expectations about how it handles ambiguity. These grounds compose without collapsing: the execution boundary establishes what the agent cannot do directly, evaluation supports observed task performance, and the model of the agent supports expectations about discretionary choice.

The useful question is therefore not whether the system has “multiple safeguards.” It is:

> **Which ground carries which part of the reliance?**

This prevents a common form of double counting in which several pieces of evidence all support the same narrow proposition but are treated as though together they established a different proposition.

It also makes residual uncertainty visible. If every ground stops before the proposition on which the consequential action depends, adding more of the same kind does not close the gap.

# 7. The intelligent-agent problem

Current general-purpose AI agents under open-ended tasking make the distinction among grounds unusually consequential.

They are engineered systems, so theories of the object matter. Architecture, permissions, tools, model lineage, system instructions, and execution boundaries can establish real constraints and useful priors. But present object-level understanding does not let us derive an open-ended agent's choices across arbitrary novel situations with the completeness available for simpler engineered systems.

Agents also behave like intelligent others in important respects. They construct representations of tasks and environments, generate alternatives, reason about consequences, respond to instructions, and can act through tools. That makes a theory of other relevant, but the uncertainty across its constituents is uneven.

The operating environment and structural constraints can often be specified externally, even though the agent's representation of that environment remains partly uncertain. Intellectual capability can be characterized substantially through evaluation, while generalization, internal representation, and reasoning under novel conditions remain incompletely understood.

The harder questions concern goal, motive, and self-regulation. An assigned objective, task instruction, reward structure, or system prompt can influence behavior without by itself establishing a durable motive. An agent may represent a principle, explain it, and reason about its implications without that fact alone establishing commitment to the principle.

This helps explain why behavioral evaluation carries so much weight for current agents. Where the generative theory of the other is weakest, observed behavior becomes an especially valuable independent ground. It can inform the missing theory; it cannot silently substitute for it.

Evaluations, red-team exercises, deployment history, and monitoring can establish important regularities. But those regularities remain evidence obtained under conditions. Their authority does not automatically extend to materially different regimes.

The problem is therefore not that AI agents give us no grounds of certainty. They give us several, often substantial ones.

The problem is that none of the familiar grounds, by itself, presently closes reliance under open-ended tasking. A structurally closed action path may require little prediction of the actor. A bounded task can sometimes be supported by inventoried grounds within a specified regime. The harder case is reliance that must survive novel situations, expanding action spaces, or claim authority traveling beyond the grounds already established.

This is why a system that merely becomes more capable, more fluent, or better evaluated can still create a governance problem. Capability expands what the actor can do. It does not automatically strengthen the ground on which we are certain what the actor will choose or what authority its output should carry.

# 8. What follows

The practical discipline is:

When relying on a result, claim, system, or actor, ask:

1.  **What is carrying the certainty?**

2.  **What exactly does that ground establish?**

3.  **Where does its warrant stop?**

4.  **Can it bear the exposure of the contemplated reliance?**

5.  **Are we spending one ground as though another had been established?**

For intelligent agents, the response may be architectural rather than a stronger claim about the agent.

If certainty about the actor cannot safely carry the exposure, strengthen the grounds where possible, reduce the exposure where appropriate, or move consequential authority to a boundary whose behavior can be grounded more strongly.

That is the logic behind a blast wall: a structural boundary that prevents reasoning output from becoming consequential execution directly. It is also the logic behind governed serving: a model may help formulate a request or produce a candidate result, while an independently governed crossing determines whether the result is established, supported, authorized, and entitled to proceed.

Trust and Statistical Bridge develop particular regions of this larger problem: Trust where reliance materially depends on expectations about an intelligent other's choices, and Statistical Bridge where governed evidence supports inference and licensed claims.

# 9. Scope

This theory is intentionally incomplete.

It does not claim that theory of object, theory of other, and behavioral evidence exhaust every possible ground of certainty. It does not supply a universal scale of certainty. Reliability engineering, assurance cases, statistics, decision theory, trust-in-automation, and formal verification provide mature methods for important parts of the problem; this theory does not attempt to subsume them. Its narrower concern is the operational distinction among grounds of certainty, the substitution errors created when one ground is spent as another, and whether the available grounds are sufficient for the reliance at issue. It also does not claim that future AI systems cannot acquire stronger forms of durable motive, principle, or commitment.

Its claim is narrower.

For analytical and operational reliance, it is useful to distinguish **what is carrying certainty**, because different grounds establish different things, under different conditions, and fail in different ways. Those grounds cannot be silently substituted. Their warrant has limits. The sufficiency of the resulting certainty depends on what will rely on it and what that reliance exposes.

AI agents make these distinctions harder to ignore, but they did not create them.

The practical test is simple:

> **Before relying, identify the ground. Before extending the reliance, check how far that ground reaches.**

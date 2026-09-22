---
title: "The Theory of Data — Development Addendum toward Version 7.2"
subtitle: "Working companion to Version 7.1. Not a publication."
author: "Huayin Wang"
date: "Development draft v0.1 — 22 September 2026"
version: "development addendum v0.1"
status: "development — not deposited, no DOI"
lang: en-US
---

# Standing of this document

This addendum records theoretical clarifications discovered **after** the freeze of Version 7.1, for
adjudication in the next edition of the theory.

It is **not a publication**, **not an amendment to Version 7.1**, and carries **no DOI**. The
deposited Version 7.1 text is unchanged and remains the governing edition. Nothing here has current
analytical authority; an entry acquires standing only if and when a successor edition adopts it.

Entries are numbered `A.n` in order of adjudication. Each states its subject, what Version 7.1 says,
what is added or corrected, and — explicitly — what it does **not** decide. Implementation names
belong to the crosswalk, not to this document, and do not appear here.

---

# A.1 · The family root and the generated Case-S analytical domain

## A.1.1 Subject

Version 7.1 §4.1 introduces two symbols in one sentence:

> "Write \(\mathcal A_F\) for the family law's admitted anchors. This is notation for its defined
> analytical domain, not a proposed registry or new object. An edge contract \(\Gamma_F(B\to A)\)
> states the applicable conditions for a proposed movement between admitted locations."

It states what \(\mathcal A_F\) is *not* — not a registry, not a new object — and that a family's
definition must license the quantity claimed at \(A\). It does not state **from what** an admitted
domain is generated, nor whether the family's own constitutive location belongs to it. This entry
supplies both, for one bounded geometric case.

## A.1.2 Restoration of a Version 6.1 term, with a changed role

**Family root.** The governed analytical location \(A_0\) from which a family's Case-S analytical
domain is generated.

This term is **restored, not coined**. Version 6.1 §5.2 is titled "Designated family root" and
defines \(F@R_F\) as "the designated governed measure at which the family declaration begins", whose
"uniqueness comes from declaration, not from an assumed unique greatest refinement in the anchor
partial order". Version 7.1 Appendix C.1 records "designated family origins" among the Version 6.1
inheritance, and Appendix C.2's continuity table — which disposes of the graft, the semantic identity
signature, multi-parent lineage, the structural constructions, semigroup and monoid continuation,
basis adequacy, state equivalence, the four governance locations, and the information quotient —
**does not dispose of it.** The term is therefore an undisposed inheritance, and this entry restores
it rather than introducing a new object.

**The role has changed, and the change is the substance of this entry.** In Version 6.1 the family
root was *declared* per family and was identity-bearing: \(R_F\) is a component of the Version 6.1
identity signature \(\Sigma(F)=(U_F,R_F,Parents(F),Establish(F),Law(F),Contracts_{id}(F))\). Here
\(A_0\) is the location from which a domain is *generated*. Whether the generating root should remain
identity-bearing is **not decided by this entry** (§A.1.8).

## A.1.3 Three distinct roots, not to be conflated

The theory now carries three locations that a reader may mistake for one another.

**Universe root.** The root anchor \(R_U\) determined by the universe's root points (§2.1.1). It
answers: *where does governed point geometry begin?* It is a property of \(U\), not of any family.

**Constitutive input anchors inside a family's expression.** The anchors, operands, order
definitions and participation conventions that §2.2 keeps **inside** \(F\): "Constitutive anchors,
operands, order definitions, participation conventions, and other meaning-bearing parameters remain
inside \(F\). They do not become additional current anchors of \(F@A\)." These are meaning-bearing
parameters of the family's identity. They are **not** locations the family stands at, and this entry
does not make them so.

**Family root \(A_0\).** The location from which the family's admitted domain is generated. It
answers: *where does this governed family declaration begin?* — Version 6.1's own formulation.

A family root may coincide with the universe root; Version 6.1 noted the case for a primitive
additive family. Coincidence is not identity, and the three questions remain distinct.

## A.1.4 The family root is in the domain, under an established domain law

Let a family's domain law be **established** in the sense of §A.1.5. Then

\[
A_0 \in \mathcal A_F
\]

**follows from the domain rule and is not a separate premise.** Refinement is reflexive, so
\(A_0 \succeq A_0\); the identity projection forgets nothing, so the prohibition test is satisfied
vacuously. Version 7.1 §2.1.2 already licenses the geometric half — "Equality permits identity
movement; it is not a strictly contracting reducer."

**The theorem is conditional and may not be detached from its condition.** Where no domain law is
established, \(\mathcal A_F\) is not generated at all, and the family's standing at its own
constitutive location is governed separately — by its constitution, not by this rule. **Absence of a
domain law never becomes general permission.** This preserves §4.1's requirement that the family's
definition license the quantity claimed, and §3.6's separation of geometric shape from family
admission.

## A.1.5 Generation of the Case-S domain

Within the Case-S geometry — where a universe's constituent placements and their fiber partitions are
consequences of the universe's constitution rather than separately authored claims — an anchor is a
set of governed constituents, refinement is containment, and the projection from one anchor to a
coarser one forgets exactly the constituents that do not survive it. Write

\[
\operatorname{Forgotten}(A_0 \to A) = A_0 \setminus A .
\]

Let \(P_F\) be the family's **prohibited Case-S constituents**: the governed fact, stated by the
family's own law, naming the constituent distinctions the family may not lose while remaining within
its analytical domain. Then for an established domain law

\[
A \in \mathcal A_F
\iff
A_0 \succeq A
\;\land\;
\operatorname{Forgotten}(A_0 \to A) \cap P_F = \varnothing .
\]

**The polarity is two-level, and both levels are required.** Establishing the domain law is the
**positive** governed act §4.1 demands. \(P_F\) is **negative** content *within* an established law,
restricting a domain the geometry generates. An established law with \(P_F=\varnothing\) admits every
Case-S projection from the family root; an **absent** law admits nothing beyond what constitution
separately supplies. These are different states and must not be collapsed.

So \(\mathcal A_F\) remains exactly what §4.1 says it is — notation for a defined analytical domain,
derived and never enumerated. The family states the compact governing fact; the universe's governed
geometry supplies the available projections; the domain is a consequence. An enumeration of admitted
locations would record consequences rather than the governing fact, and §4.1 rules it out in terms.

**Relation to inherited notation.** \(\operatorname{Forgotten}\) is defined here only for the Case-S
geometry, and is **not** declared identical to the \(Spent(q)\) of the inherited contract calculus,
which is a primitive of a different inference system and is undefined there. The resemblance is
explanatory. Likewise \(P_F\) is a fact about a **family's analytical domain**; the inherited
capability-indexed boundary map answers a different question — which distinctions a given capability
may not spend in a derivation contract — and the two are **not the same governed object**, though
they coincide in simple cases.

## A.1.6 Family domain and edge validity are different facts

§4.1's two symbols sit at two of the four governance locations of §1.5. \(\mathcal A_F\) is a fact of
**family identity**: may this family stand at this location at all? \(\Gamma_F(B\to A)\) is a fact of
**edge validity**: is this particular proposed movement lawful under its own further premises? §4's
preamble permits the separation — the facts "are not separate ontological kinds or necessarily
separate records" — and the theory's own summaries already list admitted anchors and movements as two
coordinate items (§14; Appendix B.2).

**Domain membership does not establish a lawful movement.** The complete question is layered:

1. does the location exist in the universe's governed geometry?
2. is it in \(\mathcal A_F\)?
3. do the edge and evidence premises hold for this proposed movement?
4. can a realization execute it?

Coverage permission, participation and support, evidence adequacy, and commutation or order
requirements belong to layers 3 and 4. Version 7.1 already separates them: coverage is "an edge- or
evidence-validity question" (§1.5), "self-sufficiency is a composition claim, not a coverage claim"
(§5.2), participation is selected by the law and the resolved request (§4.2), and basis admission and
evidence availability "have different scopes" (§5.5). Nothing in layer 3 may be folded into \(P_F\)
to let one formula decide everything.

§6.3 is consistent with this and is not a counterexample to §A.1.5. Two anchors of one family may be
mutually incomparable — Week and Month are the familiar case, and Day refines each — so both may lie
in a domain generated from a finer family root. What §6.3 denies is a *path between* them: "The family
guarantees agreement along admitted paths; it does not manufacture a path between incomparable
locations." That is a statement about edge validity, not about domain membership, and it supports the
separation made here.

## A.1.7 Scope boundary

**This entry governs Case S only.** It applies where the constituent placements of a universe and
their fiber partitions are consequences of the universe's constitution. It is **not** a general
definition of family domain, and it must not be generalized through the residual case where a
placement is itself the governed primitive, through the structural constructions of §2.1 and
Appendix D, or through any other held geometry.

Outside Case S, "the constituents forgotten by a projection" is not a sufficient general
representation of what a movement costs, and the rule above should be expected to fail rather than
extended. Appendix C.4's withdrawal of "universal projection-fiber locality of formation as a
family-admission test" is the standing warning: a geometric criterion that admits without a family
law has been proposed before and retracted. The rule stated here admits nothing without an
established family law.

## A.1.8 Explicitly not decided

This entry decides nothing about:

* **Constructed-family propagation.** What establishes \(P_F\) for a family constructed over
  operands — its own declaration, or something derived from its parents — is open. Conservative
  accumulation rules from the inherited capability calculus are **not** imported, because that
  calculus's boundary map is a different object (§A.1.5).
* **A general notion of what a movement spends.** \(\operatorname{Forgotten}\) is defined for Case S
  and not beyond it.
* **Case G and the structural constructions.** Held.
* **Coverage permission.** A real, positive, independent premise. It is not part of \(P_F\), and its
  governing location is not assigned here.
* **Non-commutative and ordered continuation.** Two movements may forget the same constituents while
  only one regroups lawfully. A test on forgotten constituents alone cannot distinguish them. Vacuous
  where every admitted law is commutative; not a theorem.
* **The general edge calculus \(\Gamma_F(B\to A)\).** Its conditions are not stated here.
* **Whether the family root is identity-bearing**, as Version 6.1's \(R_F\) was (§A.1.2).
* **Whether a domain law change is a succession trigger** under §3.9, whose list does not currently
  mention domain or movement.

---

# Source continuity

Version 7.1 (deposited) governs. Version 6.1 is cited only for the restored term of §A.1.2 and for
the disposition gap in Appendix C.2. The Case-S geometry of §A.1.5 rests on the separately ruled
constitution of universes and the derivation of Case-S coordinates and anchors from it, not on
Version 7.1, which admits any governed partition as an anchor and does not require a uniquely
discoverable constituent factorization. Inherited contract-calculus notation is referenced for
contrast only and is not adopted.

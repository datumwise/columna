# What must an author say to constitute a governed analytical world?

**A theory-first design reconnaissance of the Manifold family declaration.**
Recorded by Claude at Huayin's direction, 2026-09-22/23. Working upstream of C3/C5, which is suspended.

**Standing of this document.** Reconnaissance and design proposal. **No rule is enacted here and no source
change is authorized.** Where the authorities leave a question undecided I name the missing governed
decision and stop, per instruction. Seven such decisions are named in §9; two of them are stop conditions
that were hit during the work and are reported rather than resolved.

**Method.** Current Manifold schema and Columna implementation were excluded as design constraints
throughout §§1-7. Implementation is consulted only in §8, and only as evidence for later reconciliation.
No existing carrier — `Family`, `Formation`, `C1`-`C9`, `prohibited_constituents`, `domain`, `movement`,
the publication JSON — was preserved merely because it exists.

---

## 0. Standing of the authorities, which is not uniform

This must be stated first, because the instruction placed "the settled v7.2 development rulings/addendum"
second in the authority order, and the addendum's own words decline that standing.

| authority | standing, in its own words |
|---|---|
| **ToD v7.1** (deposited, Zenodo 22649945) | publication of record; **governs** |
| **ToD v7.2 development addendum v0.1** | *"It is **not a publication**, **not an amendment to Version 7.1**, and carries **no DOI**… **Nothing here has current analytical authority; an entry acquires standing only if and when a successor edition adopts it.**"* |
| **Ruling 2026-09-15, universe constitution** | *"**DRAFT FOR REVIEW.**"* — but *"**Rulings 7 through 11 (§§7-11), and the two amendments at §7b and §7c** … are recorded as ruled"*. **§§1-6 — which contain Case S, Case G and compound anchors — remain draft.** |
| **Ruling 2026-09-14, anchor identity** | **RATIFIED** |
| **Frame-QL 1.0** | adopted 2026-09-10; used here **only** to test the boundary, per instruction |
| **Measure Algebra v2.0 rev1** | used **only** where it establishes a consequence of family law |

Two consequences bind this whole note.

**(i) The entire family-domain apparatus is unadopted.** The family root \(A_0\), the prohibited
constituents \(P_F\), and the generation rule for \(\mathcal A_F\) exist only in the v7.2 addendum, which
carries no authority. ToD v7.1 itself supplies \(\mathcal A_F\) and \(\Gamma_F\) as **notation** (§4.1) and
states *"from what"* an admitted domain is generated **nowhere**.

**(ii) The apparatus rests on geometry that is itself draft.** The addendum says so: *"The Case-S geometry
of §A.1.5 rests on the separately ruled constitution of universes and the derivation of Case-S coordinates
and anchors from it"* — and that derivation is universe-constitution **§§2-4, which are draft, not ruled**.

So the honest description of the present position is: **a family's analytical domain has no adopted
governing law at all.** That is a larger gap than "constructed-family propagation is open", and it should
be visible before anything is built on top of it.

---

## 1. The semantic object a Manifold publication means

Before representation.

A Manifold publication is **a set of governed premises sufficient to determine an analytical world and
the quantities claimable within it** — and nothing else. ToD v7.1 §12.3:

> A Manifold supplies a governed instance of analytical definitions: universes, anchor structures, family
> laws, particular orders, and their relevant authority and evidence. It does not establish mathematical
> coherence by naming a declaration or establish current empirical premises merely by having once ratified
> a definition.

Three properties follow, and they are the shape of the whole design.

**1.1 It determines; it does not enumerate.** The universe-constitution ruling states the standard:
*"`Ω_U` is fixed by determination, not by extension… a constitution must *determine* its world; it need
not *enumerate* it, and a publication that enumerated it would be recording evidence, not law."* The same
standard governs families: ToD §4.1 rules an enumeration of admitted anchors out **in terms** — \(\mathcal
A_F\) is *"not a proposed registry or new object"*.

> **A publication that lists its consequences has recorded evidence in the place where law belongs.**

**1.2 It is closed under derivation, and the derived part must be absent, not merely consistent.** The
universe ruling's reasoning generalizes exactly: an authoring surface that accepts a declaration of a
theorem *"is accepting a statement that cannot be false and cannot be authoritative"* — and *"creates a
surface on which they can state it **falsely**, producing a publication that is internally inconsistent in
a way no gate can adjudicate."* This is the strongest available argument for the derivation rule, and it is
an argument from **adjudicability**, not from economy.

**1.3 It is premises only — not evidence, not realization.** ToD §9.1 separates definition, evidence and
realization; §12.3 places declaration assurance upstream of derivation and forbids the planner to
*"reconstruct or reinterpret missing law from physical bindings"*. The Manifold assurance boundary states
the same division for this estate.

**The object, in one sentence.**

> **A Manifold publication is the minimal set of governed choices from which an analytical world, its
> quantities, and the locations at which those quantities may be claimed are all determined — stated so
> that every consequence is absent from it and every premise is present exactly once.**

The four standings that discipline this are the ones the universe work established, now applied to
families:

| standing | test | may it be authored? |
|---|---|---|
| **Constitution** | a governed choice; it could have been made otherwise | **yes — and only here** |
| **Derivation** | follows from constituted facts; asserting it independently creates a falsifiable restatement | **never** |
| **Naming / reference** | a convention resolving to something constituted or derived | yes, separately; never constitutive |
| **Evidence / certification / realization** | establishes that a declared object can presently be evidenced or executed | yes, elsewhere; never meaning-creating |

### 1.4 The four layers, and where authority passes

*Added at Huayin's request, 2026-09-23. My conceptual model, not a survey. It sits here because §1 says
what a Manifold **is**, and this says what it is **relative to its neighbours** — which turns out to
constrain the declaration model in §7.*

#### 1.4.1 Two kinds of authority, which never convert into each other

ToD §4 names three authorities in one passage and, tellingly, defines each by **what it cannot do**:

> A declaration states a proposed definition. **Human ratification establishes the declaration's authority in
> its domain; it does not prove its mathematical laws.** A proof establishes a conditional analytical
> statement; **it does not certify that a particular source currently satisfies its premises.** A backend
> computation establishes neither merely by returning a value.

Underneath that sit **two kinds of authority**, and the whole architecture is the refusal to convert one into
the other.

**Constitutive authority** is held by a person, concerns a contingent world, and could have been exercised
otherwise. It is ratifiable, versionable, and *wrong-able*: a Manifold can be mistaken.

**Nomological authority** is held by nobody, concerns every world, and could not have been otherwise. It is
not ratifiable — a human ratifying a theorem adds nothing to it, and a human ratifying a falsehood does not
make it true.

> **Every architectural defect this estate has found is an attempted conversion between these two.**

A reducer token in a private realization mapping is constitutive content held at a site with no constitutive
authority. A publication that enumerates \(\mathcal A_F\) is nomological content held at a constitutive site —
and §1.2 gives the precise cost: it creates *"a surface on which they can state it **falsely**"*. The claim
examined in §1.4.3 is a third instance: that **notation can do constitutive work**.

#### 1.4.2 Four jobs, four verbs

| layer | job | verb | its characteristic failure |
|---|---|---|---|
| **Manifold** | constitutes one analytical world and the quantities claimed in it | **constitutes** | *wrong* — it can be mistaken about its world |
| **Measure Algebra** | states what follows in **any** world, given such a constitution | **entails** | *unsound* — or, honestly, *open* |
| **MEL** | canonical notation in which an analytical identity is written and compared | **denotes** | *ambiguous* — two identities under one expression |
| **Frame-QL** | states which identified result is presently wanted, and how it is presented | **requests** | *unresolved* — several identities fit the request |

**Only the first verb creates anything.** That is the model in one line, and I would put it in front of the
MA formulation:

> **Manifold constitutes · Measure Algebra entails · MEL denotes · Frame-QL requests.**

**Where authority passes.** Downhill only, and each edge carries a different cargo:

```text
   Manifold  ──premises──▶  Measure Algebra  ──identities──▶  MEL  ──◀──resolution──  Frame-QL
      ▲                                                                                   │
      └──────────────────────  NOTHING PASSES UPWARD  ───────────────────────────────────┘
```

- **Manifold → MA: premises.** MA does not check them, by its own statement: *"Measure Algebra does not decide
  whether a Manifold is correctly authored or currently certified. It begins after the required analytical
  standing exists."*
- **MA → MEL: consequences, as notation.** MA proves; MEL writes the subject of the proof down canonically and
  supplies the equivalence relation under which two writings are one identity.
- **Frame-QL → MEL: a resolution.** A resolved request *contains* an analytical identity; it does not produce
  one.
- **Upward: nothing.** Not from Frame-QL (*"Computability does not create family identity. Analytical law
  does."*), not from MEL, not from execution. MA states the same guard from its own side: *"Downstream
  expression evaluation should not become a second Manifold validator."*

Each layer may **consume** the one above it and may **refuse**. None may **write** upward. Refusal travelling
up is not a counterexample — a refusal reports that a premise is missing; it does not supply one.

#### 1.4.3 "The Manifold declares the generators…" — right in two clauses, overstated in the third

**First, a fact about the text: Measure Algebra gives this formulation twice, and the third clause differs.**

| | third clause |
|---|---|
| **rev1 §2.1** | *"The Manifold supplies the governed operands and local facts. Measure Algebra supplies the laws. **MEL supplies the canonical analytical expression.**"* |
| **rev1 §9.1** | *"The Manifold declares the generators. Measure Algebra supplies the laws. **MEL generates the governed family space.**"* |

*Supplies the canonical expression* is a **denotation** claim. *Generates the family space* is a
**constitution** claim. They are not the same job, and §9.1 is the one carrying the load. Note also that §9
opens with its own status line — *"new construction/generalization in Version 2.0; **intended as a candidate
simplification for a future ToD foundation**"* — so the stronger clause is explicitly candidate, not
established.

**What "generators" means, literally.** §9 is concrete about it. A generator is a **governed analytical
source** plus a **declared default closure law**:

```text
SOURCE revenue
    TYPE Decimal
    DEFAULT sum
```

…from which \(D(revenue)=sum\) and \(revenue@customer \equiv sum(revenue)@customer\) — *"**default
completion**, not global textual substitution."* So "generators" means: **named governed quantities at their
constitutive locations, together with the Manifold-declared completion that turns a source into a measure.**
It is an algebraic metaphor — a generating set, closed under the algebra's operations.

**My verdict: the first two clauses are exactly right, and the third is right only under the §2.1 reading.**

The metaphor fails in one specific and diagnosable way. **The closure of a generating set under a set of
operations is *determined*. The family space is not** — because each application of a law needs **fresh
contingent input that the generators do not contain**. It is not a free algebra over generators; it is closer
to a presentation in which every new element requires a new governed decision.

**The arithmetic, against ToD §4's nine responsibilities.** Take a catalogued foundation law applied to a
governed source at a governed anchor — the best case for the strong reading. MEL + MA determine:

| determined by law + expression | **not** determined |
|---|---|
| formation (the expression *is* it) | **participation intent** |
| target, where the law nominates a defining construction | **family root \(A_0\)** |
| continuation law | **the domain law (the positive act) and \(P_F\)** |
| sufficient-state bases (ToD Appendix A) | |
| result value domains | |
| empty / undefined cases | |

**Six entailed, three residual.** And the residual three are not an awkward remainder — they are precisely the
facts that are **contingent choices about this world**, which is where constitutive authority lives by
definition.

**The falsification is ToD's own published example.** `mean(revenue@order)` does not say whether the
participating points are the 100 governed Order points or the 97 supported Revenue observations. §11.5.1
refuses to let the expression decide: *"That does not authorize replacing an intended 100-order MEAN with a
97-observation MEAN."* And §4.2 forecloses the general repair: participation *"is **not** automatically the set
of surviving physical records or supported operand values."*

The intent has to come from somewhere, and the expression is not it. It **may** be defaulted — MA §22:
*"Automatic MEL completion is permitted only when the governed profile determines one lawful interpretation"* —
but a governed profile is **itself a Manifold act**. So the fact is not eliminated; it is factored out and
paid for once instead of per family. That is a good design, and it is not generation.

**MA already knows this in the fine print.** §9.1 hedges twice in three lines: the space is *"may make
available, **where lawful**"*, and its members are *"lawfully generated family **expressions**"* — expressions,
not families. And §8 says outright: *"This makes 'mean revenue by region' analytically **incomplete** unless
the input anchor is uniquely determined by governed law."* Frame-QL states the same qualification in its own
voice, and more sharply — §11.1: a canonical construction *"can be an identity-bearing reference even before a
separate human-readable name is assigned. **This does not turn arbitrary query syntax into governance
authority. The target specification and family contract must already be supplied by the selected governed
definitions and applicable law.**"*

> **The slogan overstates what its own body text claims.** I would restate it as:
>
> **The Manifold declares the generators. Measure Algebra supplies the laws. MEL generates the *candidate*
> family space — the expressions that *could* denote a governed family. Which of them *do* is settled per
> family, by the Manifold, and costs three facts.**

**And this is the same finding as §5.5, arriving from the other direction.** A generator is a **source**; the
thing generated is a **family**; and the constructed family is a **different quantity** from the source. The
prior reconnaissance's diagnosis governs both cases:

> **A prohibition is a fact about a QUANTITY. A formation law CHANGES the quantity.**

Replace "prohibition" with "participation intent" or "family root" and the sentence still holds. That is why
\(P_F\) does not propagate along lineage *and* why MEL cannot finish constituting a family: **both are attempts
to carry a fact about one quantity across a law that made a different one.**

#### 1.4.4 The example, transition by transition

The shape is worth naming first: **ascription → constitution → ascription.** Steps 1 and 3 are the *same kind*
of step. Only the middle one needs a human.

---

**(1) `balance` ⟶ `balance @ {account, day}` — ascription. No new family.**

| | |
|---|---|
| **meaning** | **Manifold** — which quantity `balance` is (A1). **ToD §2.2** — what \(F@A\) means: *"A **measure** is that family at one current anchor."* |
| **law** | whether the location is admitted: \(\mathcal A_{balance}\), generated from A4+A6. Here it is \(A_0\), so §A.1.4's vacuous theorem admits it. |
| **new declaration?** | **No.** Nothing is constituted. |

One trap worth flagging, because the next step walks into it: **inside** `mean(balance @ day)` this same
phrase is **not a measure at all** — it is a constitutive input consumed by a law, and §2.2 keeps it inside
\(F\). Same syntax, two roles, and Frame-QL §4.3 keeps them apart in terms.

---

**(2) `balance @ day` ⟶ `mean(balance @ day)` — constitution. The only transition that needs a person.**

| | |
|---|---|
| **meaning** | **split.** The *law* MEAN is universal — ToD Appendix A / MA §14. The *quantity asserted* is fixed by law + operand **for the six entailed facts**, and by **the Manifold** for the three residual ones. |
| **law** | **Measure Algebra**, entirely: §14.3's information law (contribution + participation), §14.4's \((\Sigma,N)\) sufficient state, §14.6's finalization-loses-information. Nobody declares these and no Manifold may contradict them. |
| **new declaration?** | **Yes — and exactly three facts.** |

The three:

1. **participation intent** — the 100-vs-97 choice (or a governed profile default, which is the same act paid
   once);
2. **the family root \(A_0\)** — or a ruling that it is derived, which is **D-2**;
3. **the domain law: the positive act, and \(P_F\)** — and §A.1.5 is explicit that its absence is not a gap
   to be filled downstream: *"an **absent** law admits nothing beyond what constitution separately supplies."*

This reframes a question the estate has been asking as yes/no. *"Must every constructed family be declared?"* —
**the useful answer is neither yes nor no: three facts must be, and six must not.** A declaration that restates
the six has restated theorems; one that omits the three has not constituted a family.

It also re-reads `CONSTRUCTED_DOMAIN_UNDECIDED` the same way §5.7 does, from the layering side: the refusal is
**correct**, and what it is correctly detecting is *a missing constitutive act*, not *a missing propagation
rule*. No amount of algebra was ever going to supply it, because algebra has no constitutive authority.

---

**(3) `mean(balance @ day)` ⟶ `mean(balance @ day) @ {account, week}` — ascription again. No new family.**

| | |
|---|---|
| **meaning** | **ToD §2.2** — one current anchor; `day` stays constitutive, `week` is where this measure lives. No new quantity. |
| **law** | **Measure Algebra / ToD** supply the construction: §5.1 anchor-locality, the \((\Sigma,N)\) basis established at the target, Proposition 6.2 for path-independence. |
| **new declaration?** | **No** — *provided step (2) did its job.* Admission is \(\mathcal A_F\), which step (2)'s A6 already fixed. |

**This is why the estate kept trying to derive step (3): step (3) genuinely is derivable.** The error was
seeking its derivation from step (2)'s **operands** rather than from step (2)'s **declaration**.

*(And under the settled Case-S geometry `week` is not reachable at all — §5.8, **D-1**. That is a fourth,
lower-level problem and it is not a layering question.)*

#### 1.4.5 MEL is not Frame-QL

> **MEL is a language of identity. Frame-QL is a language of request.**

MEL answers *what is this quantity?* Its equality relation is **analytical identity**: two MEL expressions are
the same expression iff they denote the same family. Frame-QL answers *what do I want to see?* Its output is a
**frame**, which is a presentation artifact — *"The frame assembles them without becoming a new measure family,
universe, or analytical ontology."*

| | MEL | Frame-QL |
|---|---|---|
| **output** | an identity | a frame |
| **equality** | analytical identity | — (two queries are two queries) |
| **closed under** | the algebra's operations | presentation |
| **has** | operands, laws, anchors, parameters | all of that **plus** selection, output naming, ordering, limiting, juxtaposition, and a resolution procedure against a **selected Manifold version** |
| **failure mode** | **unrealizable** | **unresolved** |

The failure modes are the sharpest test I know for telling them apart.

**MEL is entitled to express what nothing can compute.** MA §27: *"A valid Measure Algebra law may exist before
any engine implements it. A valid MEL expression may therefore be unrealizable by a particular system… A
missing implementation is a realization gap. It does not make the analytical expression meaningless."*

**Frame-QL is not entitled to express what nothing identifies.** Its own §1: *"The query should contain the
information required to identify the analytical result, **not** the information required to physically
manufacture it"* — and where several identities fit, the request is **unresolved**, with *"A cache, table
grain, implementation capability, or executable plan cannot break the tie."*

So the relation is **containment, not rivalry**: a resolved Frame-QL request **contains** a MEL identity, plus
request apparatus that sits below the analytical line. Frame-QL ≈ MEL + selection/framing/presentation + a
resolution procedure. Neither mints; Frame-QL says so repeatedly, and MEL's body text agrees with Frame-QL even
where its slogan does not.

One asymmetry worth keeping: **Frame-QL must resolve against a *version*.** *"The resolved canonical record
always includes the selected Manifold identity and version."* MEL needs no version — an identity is an identity.
Versioning is a property of *which world you are asking about*, not of *what a quantity is*.

#### 1.4.6 A note on what Measure Algebra says the Manifold supplies

MA §2.1 lists \(\Gamma\)'s contributions: *"governed analytical sources; universes and anchor structure;
eligibility, support, and population; governed order; declared relationships; local prohibitions and
certifications; default closure profiles; semantic type declarations."*

Read against §1's four standings, that list is **jurisdictional, not ontological** — it is "everything below the
algebra", and it mixes the standings freely. **Support is evidence** (ToD §2.3), not constitution.
*"Prohibitions and certifications"* pairs a constitutive fact with an evidential one. That is fine for MA's
purpose, which is to say where its own reasoning starts; it is **not** a specification of what a Manifold
declares, and it should not be read as one.

Two absences from that list are more interesting, and they are the same diagnosis again:

> \(\Gamma\) contains **no target specification** and **no family root** — the two most constitutive facts a
> family has.

That is exactly what one would expect from a framework whose slogan has the algebra generating families: if
laws generate targets, the Manifold need not supply them. **They do — but only for catalogued constructions
over already-governed operands, and never for the observational leaves.** Revenue's and Balance's targets
(§§3-4) are not entailed by any law. They are the premises everything else runs on.


---

## 2. The minimum authorial acts

### 2.0 The hinge: what licenses a quantity at a location

ToD §4.1 states the demand and refuses to meet it geometrically:

> A geometrically available projection and a computable state operation do not by themselves put \(A\) in
> \(\mathcal A_F\). **The family's definition must license the quantity being claimed there.**

ToD supplies **exactly two** licensing mechanisms, and no third.

**(i) Continuation.** §5.2 — *"A family is **self-sufficient** when its own supported measure values compose
across admitted refinement by an associative and commutative continuation law."* Proposition 6.1 then gives
direct/staged agreement. The family stands at \(A\) because **its own state folds over the \(A\)-fiber.**

**(ii) Construction.** §5.1 — *"The constructor is **anchor-local**: its required inputs are the already-established
measures \(G_i@A\) at the target anchor."* The family stands at \(A\) because **an admitted basis is
established at \(A\)** and the constructor is defined there.

That exhausts it. §5.1 adds the closure: *"If a chosen basis role is available only at finer \(B\), that
particular plan must first establish \(G_i@A\) under the law of \(G_i\), recursively through its own basis
where needed"* — so (ii) terminates in (i) or in an observational leaf, under §5.4 well-foundedness.

> **A family stands where its own state folds, or where its basis is established. Nowhere else.**

This is the single most useful sentence in the note, and everything in §§3-5 is an application of it. It is
an assembly of existing v7.1 text, not a new rule.

### 2.1 The acts

Each act below states: what the author establishes · why it is independent · governing text · what follows ·
what must therefore **not** be declared.

---

**A1 · The quantity.** *(ToD §4 "Target specification"; §5.3)*

The author establishes **what is being asserted**, as either an independent semantic specification over
governed analytical inputs and participating contributions, or a nominated defining construction — with its
**applicability and defined-result conditions**.

*Independent because* §5.3 forbids deriving it from any candidate basis: *"The specification must not rely on
the assertion that a candidate basis is sufficient."* A target that is defined by its bases cannot be used to
adjudicate them, and §5.3's whole adequacy obligation collapses.

*What follows:* basis adequacy is checkable; the empty and undefined cases follow wherever the nominated law
settles them; **and the fiber-uniformity of the target is fixed** — see A6.

*Must not be declared:* anything that restates the chosen construction's own theorems.

> **This is the primary act. Every other family act is either a parameter of A1 or a consequence of it.**

---

**A2 · The formation.** *(§3.1, §4 "Formation"; Appendix B.3)*

The author establishes how the analytical input is constituted: the **operands** (by family identity, or as a
governed analytical input of the universe), their **constitutive input anchors** \(I\), the **law** \(L\), and
its **identity-bearing parameters** \(\theta\). Appendix B.3's form:

\[ F=L(E_1@I,\ldots,E_m@I;\theta) \]

*Independent because* §3.1 — *"Formation can change family identity."* §2.2 keeps \(I\) inside \(F\):
*"Constitutive anchors, operands, order definitions, participation conventions… remain inside \(F\). They do
not become additional current anchors of \(F@A\)."* And §11.5.2 makes it bite: \(mean(x@order)\neq
mean(x@customer)\).

*What follows:* **analytical lineage is fully determined.** §3.7 defines a lineage edge as exactly *"the
governed constitution of \(G\) depends on \(F\)"* — which is the operand relation A2 already names.

*Must not be declared:* **the lineage graph.** It is a projection of A2. Declaring it separately creates a
second, falsifiable copy of the same fact and makes §5.4's well-foundedness an assertion rather than a check.

*Must not be declared:* **a `primitive | construction` discriminator.** Whether a family is observational is
`operands ∩ families = ∅` — read off A2. (Already settled for this estate, Huayin 2026-09-11: *"primitive/constructed
and named/query-constructed are not separate kinds"*.)

---

**A3 · Participation and eligibility.** *(§4.2, §11.5.1)*

Which existing points the quantity applies to, which contributions the law consumes, and any governed
restriction or completion.

*Independent because* §4.2 — *"Participation is selected by the law and the resolved request; it is **not
automatically the set of surviving physical records or supported operand values**."* §11.5.1's published case
is the proof that it cannot be inferred: 100 governed Order points and 97 supported Revenue observations give
`count(order) = 100` and `count(revenue@order) = 97`, and *"That does not authorize replacing an intended
100-order MEAN with a 97-observation MEAN."*

*What follows:* the denominator of every ratio-shaped law; §5.3's "matching participation" premise across
basis roles.

*Must not be declared:* per-basis participation. §11.5.2 requires *"the same participating contributions in
both components"* — one participation fact, cited by every role.

---

**A4 · The family root \(A_0\).** *(v7.2 addendum §A.1.2; ToD v6.1 §5.2, undisposed)*

The governed analytical location from which the family's analytical domain is generated.

*Independent because* — for an **observational** family, nothing derives it. That a balance is observed per
(account, day) rather than per (account, day, transaction) is a governed starting fact of the world, exactly as
the universe's individuation is. A.2.2 makes it identity-bearing: *"a change of **structural anchor** does change
\(A_0\)"*.

*For a **constructed** family this is a live fork — see **Decision D-2 (§9)**.* Nothing in the corpus decides
whether \(A_0 = I\) is derived or separately declared, and the two models are **not** expressively equivalent:
because A.1.4 makes \(A_0\in\mathcal A_F\) a vacuous theorem, a derived root **cannot exclude its own degenerate
case**, and a declared root can.

*Must not be declared:* \(A_0 \in \mathcal A_F\). It is a theorem (A.1.4) and may not be restated as an
admission.

---

**A5 · The continuation law, or its explicit absence.** *(§4 "Continuation and agreement"; §5.2, §3.9)*

Whether the family's own values compose across admitted refinement, and under which commutative semigroup or
monoid.

*Independent because* §3.9 lists *"declared continuation law"* among the **succession triggers** — changing it
mints a successor family. And §5.2 is explicit that possession of a law is not free: *"A self-sufficient family
must separately establish its continuation law"* (§5.1); *"The identity map does not turn every family into its
own sufficient state."*

*Explicit absence is a real state.* MEAN has no continuation law over its own values — §5.2: *"For MEAN, a
displayed scalar generally loses the weight required for exact continuation."* That is a **positive governed
negative**, not silence, and it must be distinguishable from an unestablished one. (The estate already carries
this three-state discipline; the realization-null ruling of 2026-09-14 states the general principle: *"`EXPLICIT_NONE`
is a positive governed negative, and can therefore be CONTRADICTED"* while *"`UNESTABLISHED` supplies no governed
fact… the defect is different in kind."*)

*Must not be declared:* an additivity boolean. Whether values compose is A5; **where** they may compose is A6;
collapsing them is the error §A.1.6 warns against.

---

**A6 · The domain law — established, and its prohibited constituents \(P_F\).** *(v7.2 addendum §A.1.5)*

Two levels, both required.

- **The positive act:** that a domain law is established at all. *"An **absent** law admits nothing beyond what
  constitution separately supplies."*
- **The negative content:** \(P_F\), *"the constituent distinctions the family may not lose while remaining
  within its analytical domain."*

*Independent because* — this is the act that carries the **anisotropy of a quantity across its own geometry**,
and §2.0's licence test shows nothing else can. Balance and Revenue differ in exactly one respect: Revenue's
state folds over every fiber, Balance's folds over the account fiber and not the day fiber. Both are additive
monoids. Both are observed at a root. The difference **is** \(P_F\) and lives nowhere else in the contract.

*What follows:* \(\mathcal A_F\) entirely — *"derived and never enumerated"*.

*Must not be declared:* \(\mathcal A_F\); any allow-list of anchors; any edge list. §4.1 rules out the registry
in terms.

*Not identity-bearing* (A.2.3) — and this is load-bearing for §5 below.

---

### 2.2 Three conditional acts, which are consequences wherever a law is cited

**A7 · Semantic value requirements.** *(§4 "Semantic values"; §5.7)*
Authored **only at the observational leaves** — the value domain of what is observed. Every downstream result
domain is derived from the cited law plus the operand domain. §5.7 fixes the jurisdiction: *"ToD states those
semantic requirements. A concrete type specification determines which value domains supply them."* The Manifold
states the **requirement** (addition, division, equality, set union, a point reference); the type specification
satisfies it; **satisfaction is realization and does not belong here.**

**A8 · Exceptional cases.** *(§4 last row; §6.1.1)*
Authored **only where the law leaves a choice.** MEAN's empty case is undefined by its own nonempty constructor
domain; MIN/MAX receive no fold value from a semigroup with no identity (§6.1.1) — *"MIN and MAX need not acquire
an artificial identity or semantic Null in order to qualify"* (§5.2). A family restating these has restated a
theorem. What remains authorable is a **declared completion**, which is a choice, and §5.3's warning that
*"Returning zero for a known-empty input also fails the nonempty scalar-MEAN contract"* is the reason it must be
explicit when taken.

**A9 · Sufficient-state bases.** *(§5.1, §5.3; Appendix A)*
Derived wherever a catalogued foundation law is cited: Appendix A supplies the basis for each
(`mean(x@I)` → *"Matching SUM and COUNT"*; `count_distinct` → *"Distinct-set family"*; scalar `LAST` → *"Nonempty
value projection from \(W\)"*). Authored **only** for a bespoke target with no catalogued law — and then the §5.3
adequacy obligation is discharged by proof, not by declaration: *"Admission first requires **each basis to
construct the target law on its own declared domain**. Pairwise agreement alone is not enough."*

### 2.3 What the nine §4 responsibilities become

§4's own preamble licenses the regrouping: *"They are not separate ontological kinds or necessarily separate
records."*

| §4 responsibility | disposition |
|---|---|
| Target specification | **A1** — authored |
| Identity and ancestry | **A2** + **A4**; the *ancestry* half is **derived from A2** |
| Domain and movement | **splits**: domain → **A6**; movement → edge validity, not a family-identity act (§A.1.6) |
| Formation | **A2** — authored |
| Eligibility and participation | **A3** — authored |
| Semantic values | **A7** — authored at observational leaves only, else derived |
| Sufficient-state bases | **A9** — derived where a law is cited |
| Continuation and agreement | **A5** authored; *agreement* is **Propositions 6.1/6.2**, never declared |
| Exceptional cases and realization | **A8** authored only where a choice; *realization* is **outside the Manifold** |

**Six irreducible authorial acts (A1-A6), three conditional (A7-A9), and two items that leave the family
contract entirely** — movement, to edge validity; realization, to the other side of the assurance boundary.

---

## 3. Worked: Sales / Revenue

### 3.1 Constituting the world

Per the universe-constitution ruling §12, exactly three governed facts.

```
universe sales
  identity      : sales                        # the subject, not a term in the law
  individuates  : { store, day, ticket }       # CLOSED. "these and no others".
                    store  : governed ref + value domain
                    day    : governed ref + value domain
                    ticket : governed ref + value domain
  exists_when   : λ_sales -- a root point exists iff a ticket was rung
                  at that store on that day      # occurrence-established
```

**Derived, and absent from the publication:** \(\Omega_{sales}\) · \(R_{sales}\) · the scalar anchor `{}` ·
each of `{store}`, `{day}`, `{ticket}` and their fiber partitions · every compound anchor · **the equality
\(\{store*day*ticket\}=R_{sales}\)** · the refinement order over all eight anchors.

Note what is *not* authored and would have been under the current model: the totality, single-valuedness,
covering and disjointness of `store` — all four are theorems (Ruling 2), and *"an authoring surface that asks
the author to assert "store is total over sales" is asking them to re-state a theorem."*

### 3.2 Constituting Revenue

```
family revenue
  in            : sales
  A1 quantity   : the consideration accruing from the participating ticket
                  points of the target fiber
                  applicable : every root point of sales
                  defined    : always (empty fiber -> identity, see A8)
  A2 formation  : observed( at the root )        # no family operands
  A3 participation : every eligible root point contributes exactly once
  A4 root A_0   : { store, day, ticket }         # = R_sales, coincidentally
  A5 continuation : commutative monoid ( +, 0 )
  A6 domain law : ESTABLISHED,  P_F = { }
  A7 values     : amount in a governed currency; requires + , = , 0
```

**Derived:** lineage = ∅ (A2 names no family operand) · kind = observational (same reason) ·
\(\mathcal A_{revenue}\) = **all eight anchors** \(A\preceq A_0\), since \(P_F=\varnothing\) admits every
projection · path agreement across `{store,day,ticket} → {store,day} → {store}` = Proposition 6.1 ·
empty-fiber value = the monoid identity, from A5 and §6.1.

### 3.3 What makes Revenue *the same family* at other anchors

This was the question the example was chosen to force, and the answer is short.

**Revenue at Region is one measure of one family.** Family identity is
\((U,\,\text{A1},\,\text{A2},\,\text{A3},\,A_0,\,\text{A5})\); **not one of those varies with the current
anchor.** §2.2: *"A **measure** is that family at one current anchor: \(F@A\)."* The licence at each \(A\) is
mechanism **(i)**: A5's fold over the \(A\)-fiber, admitted by A6.

Frame-QL states the consequence for the request layer and is worth quoting because it forecloses the tempting
misreading — §3.1:

> `SELECT revenue AT {region}` resolves analytically to the measure: `revenue @ {region}`.
> It does **not** need to become: `sum(revenue @ {transaction}) @ {region}` merely because Revenue happens to
> have an additive family law. **The query names the family identity.**

So the sum-construction is Revenue's **continuation law**, not Revenue's identity. `sum(revenue@ticket)` is a
*different* family that happens to agree; §3.9's default completion may let the short name resolve to one of
them *"only where identity and participation agree under the governed declaration"* — and that resolution is a
**naming act**, not a constitution.

> **Revenue is the same family at every admitted anchor because none of its constitutive facts mention an
> anchor other than \(A_0\).** Standing elsewhere is licensed, not re-constituted.

### 3.4 One thing the example exposes that is not in the theory's gift

The publication asserts nothing about how many *contributions* sit at one root point. If a carrier holds three
rows for one `(store, day, ticket)`, the rule combining them is an **analytical** rule (A3 participation +
A5's fold at the root), and Ruling 9 holds that realization cardinality is a separate claim that *"does not by
itself contradict the universe."* This is the intake end of the same discipline the estate already found at the
continuation end, and it is **A3's job, not the realization mapping's.** Recorded; not a new act.

---

## 4. Worked: Balance

The instruction was explicit: *do not silently make Balance additive merely because Revenue is.* The design
keeps two questions apart that a single "additive" flag would fuse.

### 4.1 Constituting the world

```
universe ledger
  identity      : ledger
  individuates  : { account, day }
  exists_when   : λ_ledger -- a root point exists for every (account, day)
                  on which the account is open, whether or not it transacted
```

\(\lambda_{ledger}\) is **generative**, not occurrence-established. Ruling 7b requires the constitution reach
this case: *"The first corrected universe constitution must be semantically capable of constituting BOTH
occurrence-established and declared/generated worlds."* It is the case a restriction over an occurrence
population cannot express, and Balance is unstatable without it — a balance exists on a day with no
transactions.

### 4.2 Constituting Balance

```
family balance
  in            : ledger
  A1 quantity   : the amount standing to the account at the close of the day
                  applicable : every root point of ledger
                  defined    : always
  A2 formation  : observed( at the root )
  A3 participation : every eligible root point contributes exactly once
  A4 root A_0   : { account, day }
  A5 continuation : commutative monoid ( +, 0 )      # SEE 4.3 -- an authored claim
  A6 domain law : ESTABLISHED,  P_F = { day }
  A7 values     : amount in a governed currency; requires + , = , 0
```

**Derived:** \(\mathcal A_{balance}=\{\,\{account,day\},\ \{day\}\,\}\). Reading the rule:
forgetting `account` gives \(\operatorname{Forgotten}=\{account\}\), disjoint from \(P_F\) → **admitted**;
forgetting `day` gives \(\{day\}\cap P_F\neq\varnothing\) → **refused**; forgetting both → refused.

So Balance stands at `{account, day}` and at `{day}` — the total balance across all open accounts on a day —
and **stands nowhere else**.

### 4.3 The two questions a single "additive" flag would fuse

**(a) Do balance values compose at all, and under what law?** — **A5.** This is *not* free, and it is *not*
inherited from Revenue's shape. That the balances of two accounts add to the balance of the pair is a
**semantic claim about the quantity** that fails in ordinary cases: mixed currencies, asset/liability sign
conventions, intercompany positions requiring elimination. An author who declines it declares **A5 = explicit
none**, and then \(\mathcal A_{balance}=\{A_0\}\) — Balance stands only where it is observed. **Both are
lawful. This design does not choose, and the choice is the author's, per instance.**

**(b) Where may that composition be applied?** — **A6.** \(P_F=\{day\}\).

These are different facts with **different identity standing**, which is the decisive argument that they must
be two acts and not one: §3.9 makes *"declared continuation law"* a **succession trigger**, while §A.2.3 rules
that \(P_F\) *"is not identity-bearing… Changing an established family-domain law does not by itself mint a
successor family."* A representation that fused them would have to give one answer to a question the
authorities answer twice, differently.

### 4.4 What is *not* known about Balance across time, stated precisely

The interesting fact is that **two independent guards refuse `balance @ {account, week}`, at different layers,
and it matters which does the work.**

**A1 does not denote there.** *"the amount standing to the account at the close of the day"* has no reading at
a location with no single day. The target specification is simply silent — not prohibited, **undefined**.

**A6 refuses membership.** \(\{account,week\}\) would require forgetting `day`, which \(P_F\) prohibits. This is
a domain fact, adjudicable without evaluating anything.

**And §5.3 would independently catch the repair.** A basis of "sum of the daily balances" *is* establishable
and *does* produce a number; §5.3's adequacy obligation refuses it because it **does not construct A1's
target** — *"Determinism and path independence of each constructor do not prove target correctness. SUM and MAX
can each be deterministic and coherent while denoting different quantities."*

This triple is worth recording because it **defends §A.2.3**, which reads uncomfortably on first contact. If
\(P_F\) is not identity-bearing, could governance quietly delete \(P_{balance}=\{day\}\) and thereby make
"balance" mean "sum of daily balances"? **No** — A1 still denotes the same quantity, and no admitted argument
constructs it at `{account}`. The semantics are carried by A1; \(P_F\) is a **domain guard, not the meaning**.
A.2.3 is therefore correct *because* A1 is the primary act.

### 4.5 The cross-time quantities exist — they are simply not Balance

Nothing here says the business question is unanswerable. It says the answers are **other families**:

| the question | the family | its \(A_0\) | licence at `{account, week}` |
|---|---|---|---|
| closing balance for the week | `last(balance @ {account,day})` under a governed day order | `{account, day}` | mechanism (i), witness monoid (§8.2) |
| average daily balance | `mean(balance @ {account,day})` | `{account, day}` | mechanism (ii), SUM/COUNT basis |
| the balance itself | `balance` | `{account, day}` | **none — refused** |

> **Balance's inability to cross time is a fact about Balance. It is not a fact about every quantity formed
> from balance.** §5 shows why that distinction is the whole of the C3/C5 problem.

---

## 5. Worked: `mean(balance @ day)`

### 5.1 Which governed act creates the new family

**A2, and only A2.** The family-creating act is the formation

\[ F = \mathrm{MEAN}\bigl(balance\,@\,\{account,day\}\,;\ \rho\bigr) \]

naming an operand identity, a constitutive input anchor \(I\), a law, and a participation rule. Everything
commonly said to "create" it does not:

- **Computing it does not.** Frame-QL §6.1: *"**Computability does not create family identity. Analytical law
  does.**"*
- **Naming it does not.** §2.2: *"Canonical names resolve this identity; they do not mint it."*
- **Requesting it does not.** Frame-QL §2.9: *"None of these clauses mints measure-family identity merely by
  shaping a request."* §4.9: *"`AS` names an output column. `WITH` may name an expression for reuse. Neither
  publishes or ratifies a family."*
- **The expression's mere well-formedness does not.** Frame-QL §3.5: *"A family-forming expression denotes a
  governed family **only when an admitted analytical law establishes that family**."*

*Why `Day` is constitutive:* §2.2 keeps \(I\) inside \(F\), and §11.5.2 states the consequence in terms —
\(mean(x@order)\neq mean(x@customer)\) absent an explicit equivalence. MA rev1 §14.2 repeats it: *"The input
anchor is generally constitutive: \(mean(m@A)\neq mean(m@B)\)."* Averaging **daily** balances and averaging
**monthly** balances are different quantities, and the difference is carried by \(I\) alone.

### 5.2 The declaration

```
family mean_daily_balance
  in            : ledger
  A1 quantity   : the arithmetic mean of the participating daily balances
                  over the day-points of the target fiber
                  applicable : every anchor at which the fiber is nonempty
                  defined    : nonempty fiber only            # from the MEAN law
  A2 formation  : MEAN( balance @ {account, day} )            # operand + I + law
  A3 participation : every {account,day} point at which balance is eligible
  A4 root A_0   : { account, day }        # = I -- SEE DECISION D-2
  A5 continuation : EXPLICIT NONE         # a mean does not continue from a mean
  A6 domain law : ESTABLISHED,  P_F = { }
  A7 values     : requires + , / , and a nonempty-fiber contract
```

**Derived:** lineage = `{ balance }`, from A2 · kind = constructed, from A2 · bases =
`{ sum(balance@I), count(balance@I) }` with \(mean=sum/count\), from the cited foundation law (Appendix A:
*"Mean: `mean(x@I)` — Matching SUM and COUNT"*) · the empty case = undefined, from the law's nonempty
constructor domain · \(\mathcal A_F\) — **§5.4**.

**A5 is `EXPLICIT NONE`, and that is a positive fact.** §5.2: *"For MEAN, a displayed scalar generally loses
the weight required for exact continuation. Its SUM and COUNT basis retains that information."* MA rev1 §14.6
concurs: *"Finalization is therefore information-losing even though it correctly derives the current measure
value."* A mean does **not** stand at coarser anchors by folding means.

### 5.3 The three expressions, separated

| | `balance @ {account,day}` | `mean(balance @ {account,day})` | `… @ {account,week}` |
|---|---|---|---|
| **what it is** | a **measure** | a **family** | a **measure** |
| **family identity** | `balance` | `mean_daily_balance` — \((U,\text{A1},\text{A2},\text{A3},A_0,\text{A5})\) | `mean_daily_balance` |
| **family root** | `{account,day}` (balance's) | `{account,day}` (its own \(A_0\)) | unchanged — a root is not a location you move |
| **constitutive input anchor** | — | `{account,day}` — **inside \(F\)**, never a current anchor | unchanged |
| **family domain** | \(\{\{account,day\},\{day\}\}\) | not a property of the expression | membership of `{account,week}` is the question |
| **continuation** | monoid \((+,0)\), restricted by \(P=\{day\}\) | **none** | not used — licence is by construction |
| **current measure location** | `{account,day}` | **none — a family has no current anchor** | `{account,week}` |

Two readings of the *same* form must not be conflated. In `mean(balance @ {account,day})` the inner phrase is a
**constitutive input**, consumed by a law; as a request it is a **measure**, ascribed to a location. Frame-QL
§3.2 gives `@` one meaning — *"an analytical **ascription** operator"* — and §4.3 keeps the roles apart:
*"`region` is the current anchor of the measure. `order` remains inside the family expression because it is a
constitutive input anchor of the mean-family identity."*

### 5.4 Looking only at the declaration, do we already know where it may stand?

**Yes — up to the positive act, and the derivation is short.**

Apply §2.0. \(F\) has **no** continuation law (A5 = explicit none), so mechanism (i) is unavailable and the
licence must come from mechanism (ii): an admitted basis established at the target anchor. §5.1: *"its required
inputs are the already-established measures \(G_i@A\) at the target anchor."*

The basis roles are two **ordinary families**, and their own declarations settle the question:

```
family sum_of_daily_balances        family count_of_daily_balances
  A2 : SUM( balance @ I )             A2 : COUNT( balance @ I )
  A4 : A_0 = I                        A4 : A_0 = I
  A5 : monoid (+, 0)                  A5 : monoid (+, 0)
  A6 : ESTABLISHED, P = { }           A6 : ESTABLISHED, P = { }
```

Their targets — *the additive total of the participating daily balance values in the fiber*, and *the count of
participating day-points* — are quantities whose state folds over **any** fiber. Neither is a balance; neither
inherits a balance's restrictions. So

\[
\bigcap_{\text{roles}}\mathcal A_{G_i}=\{A:\ I\succeq A\},
\]

and the basis is established at `{account}`, `{day}` and `{}`. With A6 established and \(P_F=\varnothing\),

\[
\mathcal A_{F}=\{A:\ A_0\succeq A\}\quad\text{— every anchor coarser than }\{account,day\}.
\]

**`mean(balance@day)` stands at `{account}` — the average daily balance per account — which Balance itself
cannot reach.**

**Which law entails it.** The bound is ToD's, in two places. §5.1's anchor-locality makes the basis roles the
things that must be admitted at \(A\). §8.1 states the coupling explicitly, for the one case v7.1 works:

> Every target covered by that basis claim must admit the corresponding \(W@A\); **a more restricted
> witness-family domain would yield a correspondingly restricted basis claim.**

That is the general rule in its single published instance. Its quantifier structure is
\(\bigcup_{\text{bases}}\bigcap_{\text{roles}}\) — union over admitted bases (§5.5 permits several with
different domains), intersection over the roles of each.

**One thing it does not supply.** The bound is a **ceiling, not a licence.** The estate's own prior finding is
exactly right and survives this analysis unchanged: *"C7 constrains C3's content. It never supplies its
authority."* A6's positive act is still required, and \(\mathcal A_F\) with an **absent** domain law remains
\(\{A_0\}\) — *"an **absent** law admits nothing beyond what constitution separately supplies."*

### 5.5 Do the operands constrain that fact? — a reductio

The operands constrain it at **exactly one point, and it is not a domain fact**:

> \(I\in\mathcal A_{balance}\) — the operand must be establishable at the constitutive input anchor.

Here \(I=\{account,day\}=A_0^{balance}\), so it holds. This is a **constitution-time obligation**, discharged
once, at one location. It contributes nothing to the *shape* of \(\mathcal A_F\).

**And any rule that propagates prohibitions along the lineage edge is falsified by this example.** Suppose
\(P_F\supseteq P_{balance}=\{day\}\). Then forgetting `day` is refused, and

\[
\mathcal A_{mean}=\{\{account,day\},\{day\}\}
\]

— the family **cannot stand at `{account}`**. But `mean(balance@day)@{account}` *is* average daily balance per
account: **the only thing the family was constructed to produce.** A propagation rule that accumulates operand
prohibitions makes it impossible, in general, to ever form a family that averages over the very distinction its
operand may not lose — which is the single most common constructed family in ledger analytics.

The estate's earlier reconnaissance reached the same wall from the other side and stated the cause in one line;
it is confirmed here and should be treated as the governing diagnosis:

> **A prohibition is a fact about a QUANTITY. A formation law CHANGES the quantity.**

**Why the two relations differ is in ToD's own text.** §3.8 — a section *titled* *"Lineage and sufficient-state
dependency answer different questions"* — draws the picture:

```text
Constitutive lineage:
    revenue at Order -- MEAN law --> mean(revenue@order)

One target construction at A:
    sum(revenue@order)@A   ─┐
                           ├─ governed constructor ─> mean(revenue@order)@A
    count(revenue@order)@A ─┘
```

The operand appears on the **top** line only. The things that must be established **at \(A\)** are on the
bottom line, and the operand is not among them. Domain bounding runs along the bottom. **A prohibition on the
top line has no path to the target anchor.**

### 5.6 MAP1 is not merely the wrong relation — its premises exclude the case

MAP1's premise shape, verbatim from MA rev1 §3.1, has every input certified in the same universe \(U\) **and at
the same anchor \(A\)**, with the conclusion at that same \(A\). rev1 states it as a premise, not an incidental:

> **The shared \(U\) and \(A\) are part of the premise shape.** The rule therefore proves one conservative
> multi-measure formation law **at a common analytical location**.

So MAP1 governs ToD §3.5's co-located pointwise formation, \((E_1\star E_2)@A\). `mean(balance@I)@A` with
\(I\succ A\) is a **reduction**, not a co-located map, and MAP1's premises are unsatisfiable for it as stated.
Importing \(\beta'=\bigcup_i\beta_i\) into \(P_F\) would be three category errors at once:

1. **wrong relation** — lineage, where §3.8 and §8.1 put the bound on the basis;
2. **wrong operator class** — a co-located map rule applied to a reduction;
3. **wrong object** — \(\beta\) is the contract calculus's capability-indexed boundary map, and §A.1.5 says in
   terms that it and \(P_F\) *"are **not the same governed object**, though they coincide in simple cases."*

rev1 also declines the generalization itself: *"It does not prove that all future multi-input laws must use
strict intersection participation."* And §30.4 still lists *"a general multi-parent family-formation calculus"*
among open obligations. **The union is not imported, and the theory does not independently demand it.**

### 5.7 What, then, is still an authorial fact?

A.1.8 posed the constructed case as a dichotomy — \(P_F\) from *"its own declaration, or something derived from
its parents."* The analysis answers it:

> **Its own declaration.** Parents contribute one constitution-time point condition (\(I\in\mathcal
> A_{operand}\)) and, through the **bases**, a ceiling. Neither is propagation, and the second is a bound on
> content, never a source of authority.

That also **dissolves** the prior reconnaissance's open Q-2 (*"for a construction that does not declare, is
\(P_F\) unestablished, or something the formation law entails?"*) without any propagation theory: A6's
two-level polarity already answers it, **uniformly for observational and constructed families**. An absent
domain law admits nothing beyond \(A_0\). No special constructed-family rule is needed, and the present
`CONSTRUCTED_DOMAIN_UNDECIDED` refusal turns out to be **right for the wrong reason** — right because the
positive act is absent, not because propagation is undecided.

What genuinely remains open is narrower than the question that was being asked, and is **Decision D-3 (§9)**:
may a constructed family declare a \(P_F\) *more restrictive* than the derived basis ceiling? I see no reason
why not — it is the same governed semantic act available to an observational family — but nothing in the
authorities decides it, and I am not deciding it here.

### 5.8 …and then asking for it at **Week** — where the example actually breaks

The second half of forcing example 3 does **not** break on constructed-family propagation. It breaks one level
below that, on geometry, and the break is general: it is not about `mean`, not about `balance`, and not about
constructions.

**The generation rule is stated over sets of constituents.** §A.1.5: *"an anchor is **a set of governed
constituents**, refinement is **containment**, and the projection from one anchor to a coarser one forgets
exactly the constituents that do not survive it"*, with
\(\operatorname{Forgotten}(A_0\to A)=A_0\setminus A\).

If `ledger` is individuated by `{account, day}`, then **`{account, week}` is not a subset of `{account, day}`**.
It is not reachable by forgetting. The rule does not refuse it — **the rule cannot express it**, for *any*
family. Calendar coarsening is not constituent-forgetting.

This is not an edge case. Frame-QL's own canonical example is `sum(revenue @ {transaction}) @ {customer *
cal.month}`, which is outside the rule's reach on the same grounds. **The most common analytical movement there
is — day to week to month — is the one the settled geometry does not model.**

There are two admissible repairs, and they are genuinely different worlds.

---

**M1 · `week` is a Case-G placement.** `day → week` is total and single-valued over \(\Omega_{ledger}\), so
Ruling 4 applies: *"the additional governed primitive is the placement / construction ITSELF… its fibers
determine a Case-G partition."* Note this is structurally **identical to the ruling's own Case-G example** —
`region` is a function of `store` exactly as `week` is a function of `day`.

**M1 is blocked, twice over, and both blocks are explicit:**

- §A.1.7: *"**This entry governs Case S only.** … it must not be generalized through the residual case where a
  placement is itself the governed primitive… **the rule above should be expected to fail rather than
  extended.**"*
- Universe ruling §15, Still open: *"**Whether a Case-G partition may participate in a compound anchor** with
  Case-S constituents. Left open."*

So under M1, `mean(balance@day) @ {account, week}` has **no governing law at all** — and neither does
`balance @ {account, week}`, nor `revenue @ {region}`.

---

**M2 · `week` and `month` are constituents of the individuation.** Lawful: ToD §2.1.3 explicitly declines to
require independence or minimality — *"The constituent description need not be a uniquely discoverable
factorization, and its dimensions need not be statistically independent."*

```
universe ledger
  individuates : { account, day, week, month }
  exists_when  : account open on day
                 ∧ week  = weekOf(day)          # λ_U carries the dependency
                 ∧ month = monthOf(day)
```

Then \(A_0=\{account,day,week,month\}\) and everything falls out **in pure Case S**:

| request | Forgotten | test | result |
|---|---|---|---|
| `balance @ {account,week}` | `{day, month}` | meets \(P_{balance}=\{day\}\) | **refused** ✓ |
| `balance @ {account,day}` | `{week, month}` | disjoint | admitted ✓ |
| `mean(balance@day) @ {account,week}` | `{day, month}` | \(P_F=\varnothing\) | **admitted** ✓ |
| `mean(balance@day) @ {account}` | `{day,week,month}` | \(P_F=\varnothing\) | admitted ✓ |

**Every answer is the intuitively correct one, and the machinery of §§2-5 produces all four with no new rule.**
Under M2 the forcing example is fully answerable, and \(P_F\) does precisely the work it was introduced to do.

M2's costs are real and should not be hidden: the individuation carries derived calendar structure; \(\lambda_U\)
acquires functional dependencies among constituents; the constituent set grows with every governed calendar
level; and it reopens the *"lawful residual role of `hierarchy` evidence"* that the universe ruling left open.

---

> **⚠ STOP CONDITION.** Choosing between M1 and M2 decides Case G and the residual role of hierarchy — both
> explicitly held — and it decides the shape of every calendar in the estate. It is not a decision this
> reconnaissance may make. **Decision D-1 (§9).**

**The finding to carry forward is the decomposition, not the blockage.** The C3/C5 question splits into two
parts that were being asked as one:

| part | status |
|---|---|
| may a constructed family forget a constituent its operand may not lose? | **answerable now** — §5.4-5.7, yes, and lineage propagation is falsified |
| may any family stand at a *coarsening of a constituent* rather than a subset of them? | **blocked** — held geometry, D-1 |

The second was invisible because it was being read as an instance of the first.

---

## 6. Authored vs derived

`AUTHORED` · `DERIVED` (with source) · `NAMING` · `EVIDENCE/CERT` · `REALIZATION`.

### 6.1 Universe

| fact | class | source / note |
|---|---|---|
| identity of the analytical world | **AUTHORED** | Ruling §12(1) |
| primitive root-point individuation (closed set; each constituent's governed ref + value domain) | **AUTHORED** | Ruling §12(2) — *"these and no others"* |
| \(\lambda_U\) | **AUTHORED** | Ruling §7 — determinate, internally resolvable; generative forms required (§7b) |
| \(\Omega_U\) | **DERIVED** | the constitution — *"determined… not separately enumerated"* |
| \(R_U\), scalar anchor `{}` | **DERIVED** | §1a — *"a **theorem** of the constitution"* |
| every Case-S placement and its fiber partition | **DERIVED** | Ruling §2 — *"proved, not claimed"* |
| totality / single-valuedness / covering / disjointness of a coordinate | **DERIVED** | Ruling §2 — never authorable |
| every compound anchor, incl. \(\{store*day\}=R_{sales}\) | **DERIVED** | Ruling §3 |
| the refinement order | **DERIVED** | Ruling §12 |
| sparsity of a compound anchor | **DERIVED** | *"a consequence of the law, never a defect of the anchor"* |
| a Case-G **placement / construction** | **AUTHORED**, separately | Ruling §4 — the placement, never the anchor |
| a governed name resolving to a derived partition | **NAMING** | Ruling §11 — established, never inferred; never stales the law |
| `unique_at(full individuation)` | **EVIDENCE/CERT** | Ruling §6, §9 — admissible, never required |
| realization cardinality | **REALIZATION** | Ruling §9 — *"Keep realization cardinality separate from analytical point identity"* |

### 6.2 Family

| fact | class | source / note |
|---|---|---|
| **A1** target specification + applicability + defined-result conditions | **AUTHORED** | §4; §5.3 forbids deriving it from a basis |
| **A2** operands, constitutive input anchors \(I\), law, identity-bearing parameters \(\theta\) | **AUTHORED** | §3.1, App. B.3 |
| **A3** eligibility and participation | **AUTHORED** | §4.2 — not the surviving physical records |
| **A4** family root \(A_0\) — observational | **AUTHORED** | addendum §A.1.2; identity-bearing per §A.2.2 |
| **A4** family root \(A_0\) — constructed | **UNDECIDED** | **D-2** — authored, or derived \(=I\) |
| **A5** continuation law, or explicit none | **AUTHORED** | §5.2; a succession trigger per §3.9 |
| **A6** *that* a domain law is established | **AUTHORED** | §A.1.5 — the positive act |
| **A6** \(P_F\) | **AUTHORED** | §A.1.5 — negative content; **not** identity-bearing (§A.2.3) |
| **A7** operand value domain (observational leaves only) | **AUTHORED** | §5.7 — the *requirement*, not the type |
| **A8** a declared completion where the law leaves a choice | **AUTHORED** | §5.3's empty-MEAN warning |
| **A9** bases, for a bespoke target with no catalogued law | **AUTHORED** + proof obligation | §5.3 adequacy |
| analytical lineage graph | **DERIVED** | **A2** — §3.7's edge *is* the operand relation |
| `primitive \| constructed` kind | **DERIVED** | **A2** — `operands ∩ families = ∅` |
| \(\mathcal A_F\) | **DERIVED** | **A4 + A6 + universe geometry** — §4.1, *"never enumerated"* |
| \(A_0\in\mathcal A_F\) | **DERIVED** | §A.1.4 — vacuous theorem; never an admission |
| bases, where a foundation law is cited | **DERIVED** | **A2** + ToD Appendix A |
| basis applicability domain | **DERIVED** | **A9 roles' domains** + §5.1 anchor-locality + §8.1 |
| result value domains | **DERIVED** | **A7 leaf domains + cited law** |
| empty / undefined case where the law settles it | **DERIVED** | §6.1.1, §5.2 — *"no family restates it"* |
| path agreement, direct vs staged | **DERIVED** | Propositions 6.1, 6.2 — a theorem, never declared |
| cross-basis agreement | **DERIVED** | §5.3 — *"an obligation of the existing sufficiency relation"* |
| \(\Sigma(F)\) / `family_id` | **DERIVED** | §2.2 — from the identity-bearing acts; *"A digest is one possible implementation"* |
| canonical name, aliases, default completion | **NAMING** | §2.2 `family_id ≠ canonical_name`; §3.9 |
| ratification / assurance of the declaration | **EVIDENCE/CERT** | §4 — *"Human ratification establishes the declaration's authority… it does not prove its mathematical laws"* |
| support \(S_{F,A}\), eligibility evidence | **EVIDENCE/CERT** | §2.3 |
| coverage | **EVIDENCE/CERT** | §1.5 — *"an edge- or evidence-validity question"*; **not** \(P_F\) (§A.1.8) |
| availability of a basis | **EVIDENCE/CERT** | §5.5 — *"A valid basis need not be available"* |
| approximation / error certificates | **EVIDENCE/CERT** | §1.5, §10.9 |
| physical bindings, tables, columns | **REALIZATION** | §12.3; Frame-QL §1.3 |
| execution plans, caches, materializations | **REALIZATION** | §10.8 — *"Materialization creates availability, not permission"* |
| numerical carriage (precision, scale, carrier type) | **REALIZATION** | §12.1; the 2026-09-12 decimal ruling |
| a reducer/evaluator token in a mapping | **REALIZATION** — and **inadmissible** | the mapping *"may **not** say 'resolve the contributions by sum'"* |

---

## 7. The recommended semantic declaration model

Syntax below is **illustrative**. It is shaped to make the semantic acts visible and to make every derived fact
**unstatable**; it is not a schema proposal and does not optimize for today's JSON.

```
universe <identity>
  individuates : { <constituent> : <governed ref, value domain> , ... }   # A closed set
  exists_when  : <λ_U>                                                     # determinate
# --- and nothing else. R_U, {}, placements, compound anchors, refinement: DERIVED, absent.

placement <identity>            # Case G only, where a placement is not derivable
  on           : <universe>
  construction : <governed construction>      # the placement is authored; the anchor is derived
  kind         : assignment | membership-universe | allocation | full-touch
                 # allocation and full-touch are CONTRIBUTION LAWS and never partitions

name <token> -> <derived partition>          # optional, established, non-constitutive

family <identity>
  in              : <universe>
  quantity        : <target specification>                    # A1
    applicable    : <conditions>
    defined       : <defined-result conditions>
  formation       : observed( at root )                       # A2, observational
                  | <LAW>( <operand> @ <I> ; <θ> )            # A2, constructed
  participation   : <rule>                                    # A3
  root            : <A_0>                                     # A4   (constructed: see D-2)
  continuation    : <commutative monoid | semigroup> | none   # A5   ('none' is positive)
  domain          : established { may_not_forget : { ... } }  # A6   (P_F; '{ }' ≠ absent)
                  | unestablished
  values          : <requirements>                            # A7, observational leaves only
  empty_case      : <declared completion>                     # A8, only where a choice
  bases           : <role-indexed> + adequacy proof           # A9, only if no catalogued law
```

Four properties of this surface are the whole of the design.

1. **There is no `kind` discriminator.** `formation: observed(...)` versus `formation: LAW(...)` *is* the
   distinction, and it is read, never declared. (Already settled for this estate; the surface now enforces it.)
2. **There is no lineage block, no `admitted_anchors`, no `derived_value_domain`, no agreement clause.** Each
   would be a restatable theorem. Per §1.2, the cost of admitting one is not verbosity — it is *"a surface on
   which they can state it falsely."*
3. **`continuation` and `domain` are adjacent but separate,** because §3.9 makes one a succession trigger and
   §A.2.3 makes the other not.
4. **Three states are expressible everywhere they are needed** — `established { }`, `established {day}`, and
   `unestablished` — and `established { }` must never be confusable with absence.

### 7.1 The synthesis, applied: what a *constructed* family's declaration actually costs

§1.4.3 settled the arithmetic — for a catalogued law over a governed operand, **six of the nine §4
responsibilities are entailed and three are not.** The declaration surface should therefore make the six
*unstatable* and the three *mandatory*. Written out, `mean(balance@day)` reduces to this:

```
family mean_daily_balance
  in            : ledger
  formation     : MEAN( balance @ {account, day} )    # the generator + the law. Not a residual --
                                                     # this IS the expression, and it is what MEL writes.
  # ---- the three residual facts; nothing else is constitutive ----
  participation : every {account,day} point at which balance is ELIGIBLE      # (1) the 100-vs-97 choice
  root          : { account, day }                                           # (2) A_0   -- or derived, D-2
  domain        : established { may_not_forget : { } }                       # (3) the positive act + P_F
```

Everything else about this family — its target, its continuation standing, its bases, its result value domain,
its empty case, its lineage, its kind — **is entailed, and must be absent.** Spelling any of them out would be
restating a theorem on a surface that permits stating it falsely (§1.2).

Three consequences for the model in §7, which I would not have reached without §1.4.

**(a) `quantity` is conditional, not universal.** §7's surface lists `quantity` on every family. That is right
for an **observational** family, whose target is a premise entailed by nothing (Revenue's and Balance's targets
are not consequences of any law — §1.4.6). It is **wrong** for a construction citing a catalogued law, where
the law *nominates* the defining construction and a restated target is a fourth opportunity to disagree with
the algebra. So:

> `quantity` is **AUTHORED** at observational leaves and **DERIVED** wherever the formation cites a catalogued
> foundation law — and **AUTHORED again** for a bespoke target with no catalogued law, where it carries the
> §5.3 adequacy obligation alongside A9.

This is the same shape as A7 and A9 already have in §2.2, and it means **A1 joins the conditional acts for
constructions.** The irreducible core for a *constructed* family is therefore **A2 + A3 + A4 + A6** — four acts,
of which A2 is the expression itself. The six-act core of §2.1 is the *observational* case, which is correct:
that is where premises actually live.

**(b) The surface must distinguish a source from a family.** MA's generators are `SOURCE`s (§1.4.3), and a
source is **not** a family — it has no participation intent, no root, no domain law. If the authoring model
admits sources at all (as MA's `SOURCE revenue / DEFAULT sum` proposes), then a **governed default completion**
is a Manifold act with its own standing, and it is what pays the participation cost once instead of per family.
Recorded as a real option, not adopted: §9 **D-7**.

**(c) The refusal is a missing act, and should say so.** `CONSTRUCTED_DOMAIN_UNDECIDED` is correct, but its
name records the wrong diagnosis. What is missing is not a propagation rule; it is one or more of the three
residual constitutive facts. A refusal that named *which of the three* is absent would be actionable by an
author; the present one is not.

---

## 8. Consequences for the existing architecture

Comparison only. **No change is proposed and none is authorized.**

### 8.1 Represented correctly already

- **The three-state polarity of the domain law.** `ESTABLISHED { }` ≠ `EXPLICIT_NONE` ≠ `UNESTABLISHED`, with
  *"absence of prohibition means unestablished, never permission"*. This note reaches the same result from A6's
  two-level polarity and finds it **uniform across observational and constructed families** — which is a
  simplification, not a correction.
- **The C3 split** into family-domain and edge-validity. §A.1.6 and ToD §6.3 both support it; the disjunction
  it replaced was a defect.
- **Lineage derived from formation**, and **C6 derived from operand domain + cited law**. Both independently
  re-derived here (§6.2).
- **One family kind.** Settled 2026-09-11; this note supplies the further argument that the discriminator is
  *readable* from A2 and therefore must not be stored.
- **Record totality** over the responsibilities, with `established` reachable by *"lawful entailment from other
  established parts"*. That is precisely the derivation rule this note applies.
- **`CONSTRUCTED_DOMAIN_UNDECIDED` refuses rather than propagates.** Correct — but §5.7 finds it is **right for
  a different reason** than the one recorded: the positive act is absent, not the propagation rule.

### 8.2 Represented in the wrong place

- **The family reducer lives in the private realization mapping** (`root_evaluator`), which the ledger records
  as carrying **five of nine** §4 responsibilities. Under §2.0 the continuation law is **A5**, an authored,
  identity-bearing, succession-triggering family fact. A mapping *"may not say 'resolve the contributions by
  sum'."* This is the single largest misplacement in the estate and both of its ends — intake (§3.4) and
  continuation — are the same defect.
- **`universe.body.anchor`** as a presumed constitutive anchor. Already ruled against twice; §3.1 here shows it
  has nothing to be: the root anchor is a **theorem**, and families in one universe may root differently.
- **Anchor declarations as constitutive objects.** Case-S anchors are derived (Ruling 2, 3). What may survive
  is a **naming act** (Ruling 11) — *established, never inferred*.
- **Calendar levels, wherever they sit today.** §5.8 shows the estate has no governing law for `day → week`
  under either reading. Whatever currently answers it is answering ungoverned.

### 8.3 Redundant declarations that should become derived

Lineage records · any `formation.kind` · any enumerated or cached \(\mathcal A_F\) · restatements of a
foundation law's empty-case theorem · result value domains · per-basis participation · coordinate totality and
single-valuedness · `R_U` and `{}`.

### 8.4 Missing authorial facts

- **\(\lambda_U\).** The recorded witness is decisive: nothing in the present universe body *is* the existence
  law — `anchor` names a derived object, `basis` is a classification, `restriction` presupposes a population it
  narrows, `law_description` has *"NO executable authority"*. And a spine universe's whole law payload is *"a
  name, a label, and two empty containers."*
- **The root-point individuation itself**, as a closed governed set. The same witness shows deleting a
  constituent leaves the ratified fingerprint **bit-identical**.
- **A5 as a first-class family fact**, distinct from A6 — see 8.2.
- **\(A_0\) at all.** ⟨measured 2026-09-23⟩ the producer's family body carries `constitutive_anchor` and
  **no family root**: the 13 keys are `aliases · canonical_reference · constitutive_anchor · continuation ·
  domain · exceptional · family_id · formation · movement · participation · target · universe · value_domain`.
  §A.1.3 keeps \(A_0\) and \(I\) explicitly distinct, so the estate currently has one of the three roots and
  is generating a domain from the other. This is upstream of **D-2**, which asks only whether the two coincide
  for constructions.

### 8.5 Producer / consumer mismatches

- **\(P_F\) is currently unproducible.** `manifold-agent`'s `BODY_KEYS` has 13 keys; Core's has 14; the missing
  one is `prohibited_constituents`, and the conformance test compares Core against Core, so it never reaches
  the producer. A consumer reads a key no producer can emit. ⟨re-measured 2026-09-23: still 13,
  `prohibited_constituents in BODY_KEYS` → `False`⟩

  Worth noting alongside it: `NON_IDENTITY_KEYS` already excludes `domain` and `movement` *"capability, not
  identity: establishing a movement later must not mint a successor family"* — which is §A.2.3 reached
  independently, and correctly, before the addendum ruled it.
- **R8's declared-\(P_F\) branch is unreachable.** The gate tests `formation.kind` **before** the geometry and
  before the \(P_F\) read, so the constructed case is closed by **gate ordering**, not by ruling. Under this
  design that gate should not exist at all — there is no `kind` to test (§7, property 1).
- **`domain` is write-only.** Nothing branches on its content; its only behavioural effect is to raise a
  responsibility's standing falsely.

### 8.6 Migration implications

The format break already identified stands and is reinforced: a v1 artifact *"under-determines its own
meaning"* because its family law lives in a private mapping. **Under §2.0 the under-determination is now
nameable** — a publication that omits A5 cannot say where its families stand, because mechanism (i) is
unstated; and one that omits A6 cannot either, because the positive act is absent. **No dual read, no shim, no
optional keys**, and — per Ruling 10 — legacy fields are *disposed of*, never compared.

### 8.7 What happens to C1-C9

| | disposition |
|---|---|
| **C1** target | **survives, promoted to primary** → A1 |
| **C2** identity and ancestry | **splits** — parameters → A2/A4; **ancestry becomes DERIVED** |
| **C3** domain and movement | **splits** — domain → A6; **movement leaves the family contract** (edge validity) |
| **C4** formation | **survives, merges** with C2's parameter half → A2 |
| **C5** eligibility and participation | **survives** → A3 |
| **C6** semantic values | **mostly DERIVED**; survives only at observational leaves → A7 |
| **C7** sufficient-state bases | **mostly DERIVED** from A2 + cited law; survives for bespoke targets → A9. Its **bounding** role on C3 is confirmed and should be made explicit — a ceiling, never an authority |
| **C8** continuation and agreement | **splits** — continuation → A5 (authored, identity-bearing); **agreement is Prop 6.1/6.2 and DERIVED** |
| **C9** exceptional cases and realization | **splits** — exceptional-where-a-choice → A8; **realization leaves the Manifold entirely** |

Nine responsibilities → **six irreducible authorial acts, three conditional, two departures.** No act is lost;
three become consequences and two change jurisdiction.

---

## 9. Missing governed decisions, and the stop conditions reached

Exposed, not filled. Two are stop conditions under the brief and were the reason to stop rather than continue.
D-7 was added after the layering analysis of §1.4.

---

**D-1 · ⚠ STOP · The calendar geometry: M1 or M2.** *(§5.8)*

Is a coarsening of a constituent (`day → week → month`) a **Case-G placement**, or are the coarser levels
**constituents of the individuation** with \(\lambda_U\) carrying the dependency?

Under **M1** the question is blocked: §A.1.7 fences Case S and warns the rule *"should be expected to fail
rather than extended"*, and the universe ruling holds open *"whether a Case-G partition may participate in a
compound anchor with Case-S constituents."* Under **M2** the whole forcing example resolves in pure Case S and
every answer comes out right.

**Why this is a stop condition:** it decides Case G and the residual role of hierarchy evidence — both
explicitly held — and it decides the shape of every calendar in the estate. It is also **the actual blocker on
forcing example 3**, which had been read as a constructed-family-propagation problem.

*Not recommended here.* M2 is expressively adequate and needs no held boundary; its costs (derived structure
inside the individuation, dependencies inside \(\lambda_U\), constituent-set growth) are real and are a
governance question, not a technical one.

---

**D-2 · ⚠ STOP · Is \(A_0\) authored or derived for a constructed family?** *(§2.1 A4)*

Two models, and they are **not expressively equivalent**. Because §A.1.4 makes \(A_0\in\mathcal A_F\) a
vacuous theorem, a **derived** root (\(A_0=I\)) cannot exclude its own degenerate case — `mean(balance@day)`
would necessarily stand at `{account,day}`, where it equals `balance`. A **declared** root can exclude it.

*For deriving:* \(I\) is already identity-bearing, so deriving \(A_0=I\) loses no identity content and removes
a falsifiable restatement; and the degenerate case is lawful, not wrong.
*Against:* ToD v6.1 §5.2, the source of the restored term, says in terms that its *"uniqueness comes from
**declaration**, not from an assumed unique greatest refinement in the anchor partial order."*

**Why this is a stop condition:** ToD permits two genuinely different declaration models, the counter-evidence
is textual and direct, and the difference is observable. I lean to deriving, and record that the lean is not an
argument.

---

**D-3 · May a constructed family declare a \(P_F\) more restrictive than its derived basis ceiling?**
*(§5.7)*

This is what remains of §A.1.8's open question after §5.4-5.6 dispose of propagation. **Recommendation: yes** —
it is the same governed semantic act available to an observational family, and §A.1.5 already makes \(P_F\)
*"the governed fact, stated by the family's own law."* Ruling it closes the constructed case for every family
that declares, exactly as the prior reconnaissance anticipated, **and needs no propagation theory.**

Note that the *complementary* half is **not** open: a constructed family may not declare a \(P_F\) **less**
restrictive than the ceiling, because the ceiling is not a prohibition but the absence of any admitted
argument (§2.0).

---

**D-4 · What actually governs a family's analytical domain today?** *(§0)*

The apparatus is unadopted (addendum: *"Nothing here has current analytical authority"*) and rests on
universe-constitution §§2-4, which are **draft**. ToD v7.1 supplies \(\mathcal A_F\) as notation and never says
from what it is generated. **Either the addendum's A.1/A.2 need adopting into a successor edition, or the
estate is building on an acknowledged non-authority.** This is prior to D-1, D-2 and D-3 and was not visible
from inside the C3/C5 framing.

---

**D-5 · Per-constituent or per-edge?** *(inherited, unresolved)*

\(P_F\)-as-a-constituent-set makes \(\mathcal A_F\) **downward closed** over the unblocked constituents, so
*"may drop `store`, but not all the way to `{}`"* is **unstatable**. ToD's own notation \(\Gamma_F(B\to A)\) is
indexed by **edge**. The design in §7 inherits the constituent-set form and therefore inherits this limit. Is a
non-monotone domain a case the theory means to permit? Recorded, not answered.

---

**D-6 · Where does contribution intake at a root point belong?** *(§3.4)*

When a carrier holds several contributions for one root point, the rule combining them is analytical. This note
places it in **A3 + A5-at-the-root**, and Ruling 9 keeps realization cardinality separate. But the estate
currently answers it in `root_evaluator`, at the realization layer — *"the same defect a second time, at the
intake end rather than the continuation end."* Confirming A3's ownership is a small ruling that closes a real
hole.

---

**D-7 · Does the authoring model admit `SOURCE` + governed default completion?** *(§7.1(b))*

MA §9 proposes generators as **sources** with a declared default closure (`SOURCE revenue / DEFAULT sum`),
giving \(revenue@customer\equiv sum(revenue)@customer\) — ToD §3.9's governed single-valued completion, at
the source rather than the family. Its attraction is real: it is the mechanism that pays the **participation
intent** cost once per source instead of once per constructed family (§1.4.3). Its risk is equally real: a
default completion is a **naming/resolution act that resolves to a constitution**, and §3.9 permits it *"only
where identity and participation agree under the governed declaration"*. Recorded as an option with a stated
benefit, not adopted, and not a prerequisite for D-1 through D-3.

---

### What was deliberately not done

No propagation rule was invented. MAP1's union was **not** imported — §5.6 shows its premises exclude the case.
Legacy `BLOCKED` accumulation was not imported. Case G was not decided. The primitive-family rule was not
reopened to make the constructed case symmetrical. No ToD concept was coined: `A1`-`A9` are labels for acts the
§4 contract already names, and \(A_0\)/\(P_F\) are the addendum's.

---

## 10. Whether we can now say the sentence

The brief set the test: *can we look at a declaration for Revenue, Balance and `mean(balance@day)` and say —
yes, this is enough to know what these families are, where their authority comes from, and which further facts
follow?*

**For Revenue: yes.** §3.2 is complete, and §3.3 answers what makes it the same family elsewhere without
appeal to anything outside the declaration.

**For Balance: yes** — and the declaration now carries the thing that was missing, which is that Balance's
additivity and the *scope* of that additivity are two authored facts with different identity standing. The
model also declines to choose whether balances add across accounts at all, correctly: that is the author's.

**For `mean(balance@day)`: yes for where it may stand under the coarsenings the settled geometry models, and
the answer is derivable from the declaration alone** (§5.4). Lineage propagation is not merely unproven — it is
**falsified by this example**, because inheriting \(P_{balance}=\{day\}\) would forbid the family from doing the
one thing it exists to do.

**For `mean(balance@day) @ week`: no — and the reason is not the one we were chasing.** It is blocked on
calendar geometry (D-1), which is held, and which blocks `balance @ week` and `revenue @ region` in the same
breath. The C3/C5 question had two problems folded into one, and the second was invisible because it was being
read as an instance of the first.

**And on "where their authority comes from" — which §1.4 was added to answer.** From the Manifold, and from
nowhere else, because it is the only layer with a generative verb. Measure Algebra entails, MEL denotes,
Frame-QL requests; none of the three can constitute, and every attempt to let one of them do so has shown up
in this estate as a defect. For a constructed family the constitutive cost is small and exactly enumerable —
**three facts** (§1.4.3) — but it is never zero, and that is why no amount of reading the algebra was ever
going to close C3/C5.

> **The suspended constructed-family-domain work turns out to be answerable. The thing underneath it is not,
> and was not what anyone was looking at.**


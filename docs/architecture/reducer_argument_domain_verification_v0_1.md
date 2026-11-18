# What, exactly, are the arguments of a reducer?

**An upstream corpus check, before the LAST/SUM decision and the freeze of the abstract declaration contract.**
Claude, at Huayin's direction, 2026-09-25. **No implementation, serialization, schema work or migration.**

## Headline

> **Huayin's reading of MA v1.0 is correct: §2.3 as written does not compose with `v : S → |X|`.**
>
> **But the corrected formulation already exists, in the other paper.** **ToD v7.1 §6.1 defines the reduction over
> `D_A(a) = D ∩ π⁻¹(a)`** — a *governed participating domain* intersected with the fiber. **Huayin's temporary
> notation `D_{F,q}(b)` is, almost symbol for symbol, published theory.**

> ## ⚠ CORRECTION, same day, before any of this is acted on
>
> **Two things above and below are wrong, and the second is the more interesting.**
>
> **(1) Contract Calculus *is* deposited in this repository** — `services/ask/deposits/w-contract-calculus.r01.md`,
> **published v1.0**, Zenodo recid 21752373. §3 originally said it was not. It is, and **it answers the question
> directly.**
>
> **(2) The answer is three-way, not two-way, and *nobody* says "participating fiber".** Published **CC §15.4**
> gives the \(G_1\) partial-reducer denotation that MA v1.0 defers to, and it does **not** restrict the index
> set. It folds over the **fiber ∩ population** with a **three-way case-split embedding**:
>
> \[
> \widehat\eta(a)=\begin{cases}(\eta_\kappa(v(a)),1,1)&a\in S\\(0_\kappa,1,0)&a\in E\setminus S\\(0_\kappa,0,0)&a\in P\setminus E\end{cases}
> \]
>
> **So eligibility and support enter through the *embedding and the counts*, not through the index.** ToD §6.1
> instead restricts the *index* to \(D\cap\pi^{-1}(a)\). **These are two different constructions of the same
> intent, and the corpus contains both.**
>
> **(3) Therefore a zero-extension *is* published — in the state monoid — and my §4 was too strong.** See the
> corrected §4. **Huayin's classification survives and is in fact strengthened, because Contract Calculus itself
> draws the line he predicted.**
>
> The headline claim — *MA v1.0 is loose where ToD v7.1 is exact* — **survives**, but the repair is narrower than
> stated: MA v1.0 shows the \(G_0\) formula and **does not carry forward the \(G_1\) refinement it already
> cites.**

So the seam is **between the papers, not inside the theory**. MA v1.0 is loose at a point where ToD v7.1 is
exact, and MA v1.0 **says so itself** (§9: *"richer participation rules"* remain open).

| question | answer |
|---|---|
| What are a reducer's arguments? | **governed contributions over `D`**, not points of the geometric fiber |
| Is *"reducers operate over participating fibers"* established? | **Yes — by ToD v7.1 §6.1, not by MA v1.0.** MA v1.0 neither establishes nor denies it |
| Is `contribution` more fundamental than `participating fiber`? | **Yes**, and MA v1.0's own expansion fragment proves it |
| Is *structural zero* established anywhere? | **No. The corpus is silent**, and in two places says the opposite |
| Does `clause = source × scope` still suffice? | **Yes. No new field.** The four inputs to `D` all have homes, three of them outside the family |
| Does the LAST/SUM conclusion change? | **No.** It was already stated over the participating domain. One refinement — §6.4 |

---

## 1. What MA v1.0 actually establishes

### 1.1 The seam is real, and it is a gap rather than a contradiction

§2.0 gives \(C_1=(X,U,A,E,S,\beta,\gamma)\) with \(v:S\to|X|\). §2.3 then writes

\[
K_\kappa(b)=\bigoplus_{a\in Fib_q(b)}\eta_\kappa(v(a)).
\]

**Taken literally these do not compose.** But notice the sentence §2.3 opens with:

> *"**For the order-insensitive \(G_0\) fragment**, an aggregate capability \(\kappa\) has…"*

and what §2.0 says about \(G_0\):

> *"The earlier \(G_0\) fragment uses the smaller contract \(C=(X,A,\beta)\); \(G_1\) is the fragment used here
> **when universe, eligibility, support, and coverage matter**."*

**\(G_0\) has no \(E\) and no \(S\).** In \(G_0\), \(v\) is total on \(A\), so \(Fib_q(b)\subseteq\operatorname{dom}v\)
holds trivially and the formula is well-typed. **§2.3 is not wrong; it is stated in the fragment where the
question cannot arise.**

The gap is that **v1.0 never restates the reduction denotation for \(G_1\).** `RED1` defers it —
*"\(v'\) given by **the partial reducer denotation**"* — to Wang 2026b §§15, 17. So the one place where eligibility
and support exist, MA v1.0 **cites rather than states** the reducer's argument domain.

> **Diagnosis: MA v1.0 is formally underspecified on this point, by its own architecture.** §9 lists among what
> *"remain open or only partly formalized"*: **"richer participation rules."** And §6 says outright that it gives
> *"one point precise **without pretending to have a complete participation calculus**."*
>
> **Huayin is right not to let *"reducers operate over participating fibers"* be attributed to Measure Algebra.**

### 1.2 §2.4 confirms the three sets are distinct, and supplies the only well-typed reading

§2.4 carries \(\widehat S_\kappa=S_\kappa\times\mathbb N\times\mathbb N\) with

> *"\(e\): **eligible** source points in the fiber; \(o\): **observed supported** source points in the fiber."*

Counting both **presupposes that the fiber contains points that are neither.** The only well-typed reading of
§§2.3–2.4 together is therefore

\[
K(b)=\Bigl(\ \bigoplus_{a\in Fib_q(b)\cap S}\eta(v(a)),\ \ |Fib_q(b)\cap E|,\ \ |Fib_q(b)\cap S|\ \Bigr),
\]

**value fold over the supported part, counts over the eligible and supported parts.** That is coherent — but note
what it means: **in MA v1.0 as written, the value fold ranges over support.** What protects meaning is not the
fold but the **second finalizer**: \(\rho_\kappa\) finalizes the value, \(Covered_h\) decides servability.

> ⚠ **And that locates the one genuine risk precisely.** Under `Complete`, \(o=e\) is required, so
> \(Fib\cap S=Fib\cap E\) and the distinction collapses harmlessly. **Under `Any`, a fold over whatever happens
> to be supported is served as a value** — which is exactly where support would leak into meaning. §5 supplies
> the guard: *"Where the original population remains and some points are unsupported, **the result must remain
> partial rather than silently becoming a smaller population**."* **`Any` is a partial/disclosed result, not a
> redefinition of the quantity.**

### 1.3 What v1.0 *does* establish, and it is a lot

- **Population comes from eligibility, never from observed rows.** §5: *"A lawful joint frame is built from
  **eligibility** rather than by intersecting observed rows… A physical inner join that returns only the 47
  observed pairs can realize those supported values. **It cannot, by itself, decide that the population has
  become 47.**"*
- **Participation is an analytical choice.** §6: *"**Participation is part of the analytical operation and must
  be declared or derived under law. It is not selected by backend join behavior.**"*
- **Carve versus restriction.** Making the supported subset into the population is a **carve**, needing *"a
  distinct population identity"* (Theorem \(G_1.6\)).
- **The monoid theorems are invariance results over a *given* contribution multiset.** §4.1's state-law table:
  *"commutative monoid | regrouping and ordering of **the same governed contributions** preserve state."*

> ⚠ **On the phrase Huayin flagged.** *"Same governed contributions"* is **MA v1.0's wording**, in §4.1's table,
> which MA attributes to **ToD v6.1 §4.7**. It has **zero occurrences in ToD v7.1 or Frame-QL v7.1**, whose
> wording is *"the same **compatible** contributions"* (ToD §6.1, Prop 6.1) and *"the same **correctly accounted**
> contributions"* (§10.4). **The three phrasings are doing the same job and none of them is a definition** —
> `contribution` is never given a standalone definition anywhere in v7.1.

> ⚡ **That last line answers the question Huayin flagged.** \(G_0.2\), \(G_1.1\) and ToD's Proposition 6.1 are all
> theorems about **re-associating the same contributions**. **They presuppose the contribution multiset; they do
> not determine it.** `Fib_q(b)` appears in §2.3 as the *index set of a fold in a fragment where it coincides with
> everything else* — it is doing bookkeeping, not ontology. **Nothing in MA v1.0 asserts that the geometric fiber
> is the reducer's semantic argument.**

### 1.4 And "contribution" is the more fundamental notion — provable from v1.0 itself

§2.5's expansion dispositions are stated over **contributions**, not points:

> *"**replicate** — copy a source **contribution** to every related target; **assign** — send each eligible source
> **contribution** to exactly one target; **allocate** — distribute a source **contribution** across targets under
> declared unit-sum weights."*

After `replicate`, **one source point yields several contributions**; after `allocate`, **fractional** ones.
Theorem \(G_2.8\)'s duplication-invariance condition exists precisely because contribution multiplicity is
visible to the downstream reducer.

> **So a reducer's arguments are contributions, and a point is not a contribution.** MA's own boxed separation —
> *structural transformation then value reduction* — then supplies the discipline that makes "points" usable
> again: **once expansion is explicit, contributions are the points of the expanded anchor.** Where the expansion
> is implicit (a physical join doing both at once), the identification fails, which is what \(G_2.8\) refuses.

---

## 2. What ToD v7.1 establishes — the corrected formulation, already published

**§6.1 states it exactly, and Huayin's `D_{F,q}(b)` is already there under the name \(D_A(a)\):**

> *"Suppose a self-sufficient family \(G\) has established contribution states \(g_I(i)\) at constitutive anchor
> \(I\), **with governed participating domain \(D\subseteq I\)**. … suppose the **contributing fiber**
> \(D_A(a)=D\cap\pi_{I\to A}^{-1}(a)\) is finite. Define \(g_A(a)=\bigoplus_{i\in D_A(a)}g_I(i)\)."*

**The fold is over \(D\cap\text{fiber}\). Not over the fiber.** And the proof is explicit about why:

> *"**This proof index is defined from the fixed governed contribution domain, not by dropping groups whose
> support is unknown.**"*

### 2.1 What determines \(D\)

**§4.2** — *"let \(D\) be its governed participating domain at a constitutive anchor \(I\). **Participation is
selected by the law and the resolved request**; it is not automatically the set of surviving physical records or
supported operand values."*

So, assembling §§2.1.3, 2.3, 4.2, 6.1:

\[
D \;=\; \underbrace{\text{existing points}}_{\text{universe}}\;\cap\;\underbrace{E_F}_{\text{family eligibility}}\;\cap\;\underbrace{\text{the law's participation rule}}_{\text{the cited law}}\;\cap\;\underbrace{\text{restriction in the resolved target}}_{\text{the request}}
\]

**Support appears nowhere in that intersection.**

### 2.2 What role support plays once \(D\) is determined

**Three roles, all downstream of meaning:**

1. **It decides what can be computed.** Only \(D\cap S\) has values to fold.
2. **It is carried as domain state and finalized separately** — MA §2.4's \((e,o)\) and \(Covered_h\).
3. **It may never be substituted for.** ToD §6.1: *"The identity \(e_G\) applies to a **known empty contribution
   fiber**. **It is not a substitute for an unknown domain, unsupported placement, or unavailable value.**"* and
   *"**That unavailable witness must not be replaced by the identity.**"* §6.1.1: *"**blocks with unknown support
   cannot be treated as known empty.**"*

> **Support determines what can be computed and whether the result may be served. It never determines what is
> meant.** ToD and MA v1.0 agree on this; MA states it as a population rule, ToD as a substitution prohibition.

### 2.3 The five states Huayin asked to keep apart — ToD keeps all five apart already

**§2.3** — *"A point can be **absent from the universe**, **present but ineligible** for a quantity, **eligible but
unsupported**, or **supported with value zero**. These are different analytical claims even when a carrier
represents several of them with row absence or a null."* Plus **§6.1**'s fifth: a **known-empty contribution
fiber**, where the identity applies.

| | state | where it sits |
|---|---|---|
| non-participating point | in the fiber, **not in \(D\)** | excluded by the participation rule |
| participating contribution valued zero | **in \(D\), in \(S\)**, value \(0\) | an ordinary contribution |
| eligible but unsupported | **in \(D\)** (if the law participates it), **not in \(S\)** | counted in \(e\), not in \(o\); **may not be replaced by the identity** |
| ineligible point | in the fiber, **not in \(E\)**, so not in \(D\) | excluded before participation |
| known-empty fiber | \(D_A(a)=\varnothing\) **and that is established** | the identity applies — monoid only |

**No two of these are interchangeable, and the corpus says so for each.**

### 2.4 What LAST ranges over — answered, not inferred from the word

**§8.2** — *"Fix one governed order, **one participating domain \(D\subseteq S\)**, and one coherent operand
instance \(f:D\to V_x\)."*

> **LAST ranges over \(D\), the participating domain — exactly like every other reducer.** No special case.

**And §9.3 settles the follow-up before it can be asked** — *"If the selected eligible point's value is
unsupported, **ordinary LAST over eligible points cannot retreat to the previous supported value. LAST over
supported observations has a different participation rule.**"*

> ⚡ **So there are two LASTs, and the participation rule is what distinguishes them.** *Ordinary* LAST
> participates over eligible points and **fails** when the winner's value is unsupported — it may **not** silently
> fall back. A LAST that walks back to the last supported value is **a different family with a different
> participation rule**, which must be declared as such. This is the same shape as case 23's AOV, and it is the
> strongest single confirmation that **participation is identity-bearing and is not an evidence accommodation.**
>
> ⚠ **One trap worth naming.** The \(S\) in *"\(D\subseteq S\)"* is **the constitutive input anchor**, not the
> support set. ToD §2.3 warns about precisely this: *"the standalone symbol \(S\) used later denotes a
> **constitutive input anchor**… **the two uses of support must not be conflated.**"* Read carelessly, §8.2 looks
> like it says LAST ranges over support. **It says the opposite.**

---

## 3. What Contract Calculus establishes — **published, deposited, and decisive**

`services/ask/deposits/w-contract-calculus.r01.md` — *A Contract Calculus for Governed Analytical Transformation*,
**published v1.0**, Zenodo recid 21752373, verified deposit.

### 3.1 Where `Fib_q(b)` comes from, and why it is unqualified

**§5.1 "Fibers"** — *"the source fiber is \(\operatorname{Fib}_q(a')=\{a\in\operatorname{Pts}(A)\mid q(a)=a'\}\)… A SQL group is a common
physical representation of such a fiber. **The formal object is the preimage of the grouping map**, not the row
container used to implement it."*

**It is the set-theoretic preimage over \(\operatorname{Pts}(A)\) — no eligibility, support or participation qualifier**, and
it is unqualified for a stated reason. **§4.4** — *"An \(X\)-typed **total** atom over anchor \(A\) is
\(v:\operatorname{Pts}(A)\to|X|\)… **The proved core suppresses those distinctions** so that value and contract composition can be
isolated."* \(G_0\)'s contract is \(C=(X,A,\beta)\): **no \(E\), no \(S\), no \(U\).**

**§12** states the limitation outright — *"a partial function alone does not distinguish a point outside the
population, an ineligible point, an eligible but unobserved point, or an observed point. \(G_1\) is the smallest
population-and-partiality extension used here."* And the claims table marks *"Partiality, eligibility, support,
observation, and evidence form a complete calculus"* as **"Not claimed."**

### 3.2 What \(G_1\) actually does — and it is not what I inferred

**\(G_1\) does not re-index the fold.** **§15.4** defines a **per-point embedding** over the population:

\[
\widehat\eta_{\kappa,E,S,v}(a)=
\begin{cases}
(\eta_\kappa(v(a)),\,1,\,1), & a\in S,\\
(0_\kappa,\,1,\,0), & a\in E\setminus S,\\
(0_\kappa,\,0,\,0), & a\in P_{U,A}\setminus E,
\end{cases}
\qquad\text{folded to }(s_q(a'),e_q(a'),o_q(a')).
\]

*"The first component contains sufficient state **for observed values only**. The second and third carry the
analytical domain facts needed to decide eligibility and support."*

**§15.1** keeps the fiber as the ambient index and intersects for the counts — \(e_q(a')=|\operatorname{Fib}_q(a')\cap E|\),
\(o_q(a')=|\operatorname{Fib}_q(a')\cap S|\), output eligible exactly when \(e_q(a')>0\). **§15.2**:
\(S'_{q,h}=\{a'\mid \operatorname{Covered}_h(e_q(a'),o_q(a'))\}\), \(E'_q=q[E]\).

> ⚡ **So the published answer to *"what are the arguments of a reducer?"* is: the points of the fiber intersected
> with the population, under a three-way case-split embedding in which non-supported points contribute the state
> identity and are counted rather than dropped.** **Eligibility and support enter through the embedding and the
> counts — not through the index set.**

### 3.3 And the line is drawn where Huayin predicted

**§15.5, the partial reducer denotation** — the sentence MA v1.0 defers to and does not reproduce:

> *"For \(a'\in S'_{q,h}\), define \(v'(a')=\rho_\kappa(s_q(a'))\). **No value is defined outside \(S'_{q,h}\), even
> when the aggregate monoid has an identity and \(\rho_\kappa(0_\kappa)\) is numerically meaningful. This is the formal
> separation between an algebraic empty fold and an observed analytical value.**"*

**§19.9, Proposition G1.P1** — *"A \(G_0\) reducer defines an aggregate value even on an empty fiber through the
monoid identity. **\(G_1\) deliberately does not treat that value as observed support.**… On empty target fibers,
\(G_0\) may return the algebraic identity while \(G_1\) returns **no observed analytical value**. This is not a
contradiction. It is the semantic refinement introduced by population and support."*

And the realization obligation, **§18.1** — *"A physical reducer must process enough domain information to
distinguish eligible-unobserved points from points that do not belong to the eligible fiber."*

### 3.4 CC versus ToD — two constructions, and they are not the same

| | index set | how \(E\) and \(S\) enter | empty-fiber behaviour |
|---|---|---|---|
| **CC \(G_0\)** | \(\operatorname{Fib}_q(a')\) | not at all — atoms are total | returns \(\rho_\kappa(0_\kappa)\) |
| **CC \(G_1\)** | \(\operatorname{Fib}_q(a')\cap P\) | **case-split embedding + counts \((e,o)\)** | **no value**, by §15.5 |
| **ToD §6.1** | \(D\cap\pi^{-1}(a)\) — **index-restricted** | \(D\) is a governed participating domain | identity, only for a **known**-empty contribution fiber |

**Both are published. Neither uses the phrase "participating fiber" in the sense we had been using**, and they
are different constructions: CC is **index-total, embedding-partial**; ToD is **index-partial**. They agree on
values wherever \(D=E\), because \(E\setminus S\) and \(P\setminus E\) contribute the state identity — **but they
differ in what they carry** (CC carries \((e,o)\) through the fold; ToD's index simply omits non-participants) and
**in where the empty case is decided.**

> ⚠ **And ToD has its own looseness here, symmetric to MA's.** §4.2 says \(D\) is *"not automatically… supported
> operand values"*, but §8.2's proof assumes *"**operand values are established on \(D\)**"*, and §6.1 speaks of
> *"**established** contribution states \(g_I(i)\)"*. **So \(D\)-as-declared and \(D\)-as-used-in-the-proofs are not
> obviously the same set**, and where they differ is exactly the eligible-but-unsupported case that CC handles
> explicitly with \((0_\kappa,1,0)\). **Neither paper is wrong; the two have simply not been reconciled.**

---

## 4. Structural zero — **corrected**: published in the *state*, and explicitly barred from becoming a *value*

> ⚠ **This section originally read *"not established, the corpus is silent."* That was too strong.** The term is
> absent, but **the construction is published**, in Contract Calculus §15.4 — and CC then draws exactly the line
> Huayin predicted. **The corrected finding is more useful than the original one.**

### 4.0 What is actually established

> **A zero-extension exists in published Contract Calculus \(G_1\), in the *state monoid only*.** A point in
> \(E\setminus S\) embeds as \((0_\kappa,1,0)\) and a point in \(P\setminus E\) as \((0_\kappa,0,0)\). **It is never
> permitted to become a value:** §15.5 — *"**No value is defined outside \(S'_{q,h}\), even when the aggregate monoid
> has an identity and \(\rho_\kappa(0_\kappa)\) is numerically meaningful.**"*
>
> **The counts are what stop it collapsing.** Strip \((e,o)\) and the identity-embedding is indistinguishable from
> a real zero. Carry them, and the embedding is bookkeeping while \(\operatorname{Covered}_h\) decides whether anything may be
> served. **That is the whole mechanism.**

**So Huayin's hypothesis is confirmed and sharpened.** *"An invariance result for SUM under lawful zero-extension;
it does not prove that the geometric fiber is fundamentally the reducer's semantic argument."* — **Contract
Calculus says precisely this itself**, in §19.9: \(G_0\)-over-the-fiber and \(G_1\)-over-the-population **disagree
on empty fibers**, *"not a contradiction… the semantic refinement introduced by population and support."*
**If the fiber were the semantic argument, there would be nothing to refine.**

### 4.1 What remains genuinely absent



**Searched: `structural zero`, `structural-zero`, `zero-extension`, `extend by zero`, across the specs, docs,
editorial and research trees and the MA v1.0 deposit.**

- **MA v1.0: zero occurrences.** \(0_\kappa\) is the **state-carrier identity** used for the empty fold. There is
  no zero-extension of a value function anywhere.
- **ToD v7.1: zero occurrences** of the term. Its nearest neighbours are both **restrictions**, not licences:
  *"Any additionally enumerated, **established empty contribution fiber** supplies the identity and does not
  change the result"* (§6.1 — about **empty blocks in a staged fold**, not about non-participating points), and
  *"**That unavailable witness must not be replaced by the identity**"* (§6.1), and *"**blocks with unknown support
  cannot be treated as known empty**"* (§6.1.1).
- **The one literal occurrence in the whole repository** is in a deposited Q&A corpus, and it names the notion as
  **an open question, not a law**: *"The more specific reading of an absent value — missing, unknown, **structural
  zero**, ineligible, or undefined — **depends on universe, eligibility, measure kind, recording completeness, and
  fill rule.**"*

**And the published Frame-QL chapter addresses the notion directly, in order to withhold the authority** —
LQ §8.9, *"Empty contribution, unsupported value, and zero"*:

> *"The identity of a state-combination law represents known-empty contribution under that law. It is not semantic
> NULL and is not a replacement for unknown evidence… **A supported zero is an ordinary established value. An
> absent observation can establish zero only under the applicable existence, participation, coverage, and
> completion law.** `coalesce(E,0)` cannot manufacture that authority merely through a familiar spelling."*

Two further published refusals: ToD §5.3 — *"**Returning zero for a known-empty input also fails** the nonempty
scalar-MEAN contract, even if nonempty cases agree"* — and §11.1's table — *"SUM … **Known empty additive
identity is not a missing input.**"*

> ⚠ **AND A DRIFT FINDING, which is the reason the check was worth running.** The phrase **"structural zero" *is*
> live in this estate — but only **outside the governing theory**: in `manifold-eval/prompts/agent.md`,
> `columna-studio/docs/skill.md`, `manifold-agent/…/instructions/audit@0.5.md`, and an alignment attachment which
> attributes structural-zero reasoning to **its own "§8.9" and to a Manual "B3 law" — not to ToD v7.1**. Within
> `specs/frameql_v7_1/` the phrase has **zero occurrences**.
>
> **So the concept is operating in the implementation and prompt corpus while being absent from — and in two
> places contradicted by — the governing theory.** That is a real divergence, independent of anything in PR #343,
> and it is worth someone's attention on its own account.

> **Verdict, corrected.** **The term "structural zero" is not a law anywhere.** The *identity-embedding* is
> published (CC §15.4) and is confined to the state. **What is not established is the thing the phrase is usually
> reached for** — that an absent observation may be read as a zero **value**. On that, Frame-QL §8.9 is explicit:
> *"An absent observation can establish zero **only under the applicable existence, participation, coverage, and
> completion law**."* **Huayin was right to check. What would have become theory by recollection is not the
> embedding — it is the licence to finalize it.**

**And Huayin's classification of the SUM result is exactly right.** \(\Sigma_D r=\Sigma_G\tilde r\) is:

- **an invariance property of one monoid** — it holds because \(0\) is SUM's identity, and for no deeper reason;
- **conditional on a semantic warrant** — writing \(\tilde r(a)=0\) on \(G\setminus D\) **asserts something about
  the world**: that a non-participating point contributes nothing. Plausible for Revenue. **For Balance it is
  false**: a closed account-day does not have balance \(0\); it has no balance. **That assertion is an
  observation, not an algebraic step**;
- **not evidence about the reducer's argument domain.** It shows one fold is insensitive to a particular padding,
  not that the padding is what the fold was always over.

---

## 5. Reducer by reducer

For each: what it ranges over, and whether extending \(D\) to the whole geometric fiber preserves the result.

| reducer | argument domain | does \(D\to G\) extension preserve? | why |
|---|---|---|---|
| **SUM** | contributions over \(D\) | **yes, conditionally** | \(0\) is the monoid identity — **and only if the zero-assertion is semantically warranted** (§4) |
| **COUNT** | contributions over \(D\) | **no** | \(\eta\) maps a *contribution* to \(1\). There is no "contribution of count \(0\)"; a non-contributor is **absent**, not a zero. Extension counts non-contributors |
| **MIN / MAX** | contributions over \(D\) | **no, and it fails instantly** | \(0\) is **not** MIN's identity \((+\infty)\) nor MAX's \((-\infty)\). \(\min\{5,7\}=5\); zero-extended, \(0\). **ToD §6.1.1 names MIN and MAX as the standard no-identity examples** |
| **MEAN** | contributions over \(D\) | **no** | the basis is \((\Sigma,N)\); the extension leaves \(\Sigma\) alone and **corrupts \(N\)**. \(\{5,7\}\to 6\); \(\{5,7,0,0\}\to 3\). **The falsifier Huayin predicted** |
| **LAST / FIRST** | contributions over \(D\) — **ToD §8.2 explicitly** | **no, and worse than MEAN** | the witness monoid selects **by position**. A fabricated later point **becomes the answer**. ToD §11.2 forbids the move by name: *"**No \((C_2,d_3)\) point is fabricated.**"* |

**Two of these are settled by published worked examples, not by my arithmetic.**

- **MEAN.** ToD §11.5.1: *"100 governed Order points and 97 supported Revenue observations give
  `count(order) = 100` and `count(revenue@order) = 97`… **That does not authorize replacing an intended 100-order
  MEAN with a 97-observation MEAN.**"* And §11.5.2: *"**The law cannot silently replace an intended eligible
  domain with the supported observations simply to obtain a denominator.**"*
- **MIN/MAX.** §11.5.1: *"self-sufficient commutative **semigroup** families… **An identity is not required**, and
  an empty eligible fiber receives no MIN/MAX value from the semigroup alone."* A law with **no identity** cannot
  have an identity-extension.

> **One reducer out of five tolerates the extension, conditionally.** Therefore the geometric fiber is **not** the
> reducer's semantic argument; it is the *ambient index* within which \(D\) is located. **Huayin's hypothesis is
> confirmed on every count.**

---

## 6. The smallest corrected formulation

### 6.1 The correction

> **Replace `Fib_q(b)` in MA v1.0 §2.3 with ToD v7.1 §6.1's contributing fiber.** No new concept is required,
> because the concept is already published in the companion paper.

For \(q:A\to B\), target \(b\), family \(F\), with \(D_{F,q}(b)=D_F\cap Fib_q(b)\):

\[
\text{value state } s(b)=\!\!\bigoplus_{d\,\in\, D_{F,q}(b)\,\cap\, S}\!\!\eta_\kappa(v(d)),
\qquad
e(b)=\bigl|D_{F,q}(b)\bigr|,
\qquad
o(b)=\bigl|D_{F,q}(b)\cap S\bigr|
\]

\[
\text{value}=\rho_\kappa(s(b)),
\qquad
\text{servability}=Covered_h(e,o)
\]

**Two substantive changes to §2.4, both flagged as recommendations against published text:**

1. **\(e=|D|\), not \(|Fib\cap E|\).** §2.4 says *"eligible source points **in the fiber**"*, which is right only
   when \(D=Fib\cap E\). Where the law or the resolved request narrows participation, **coverage must be measured
   against \(D\)** — otherwise every restricted request reports itself under-covered.
2. **The fold is over contributions, not points** — with multiplicity and weights where an explicit `expand_χ`
   has produced them (MA §2.5).

### 6.2 The layering — Huayin's diagram, falsified in two places and otherwise confirmed

```
geometric fiber  Fib_q(b)                       ambient index; NOT the argument
   ↓   ∩ universe existence ∩ E_F ∩ law's participation rule ∩ resolved-request restriction
governed contribution domain  D_{F,q}(b)        the argument domain
   ↓   explicit expansion only (replicate / assign / allocate)
governed contributions                          multiplicity and weights live HERE
   ↓
┌─ value state s over D ∩ S ──────┬─ domain state (e,o) over D ─┐   ONE monoid, folded together
└─ finalizer ρ_κ → the value ─────┴─ finalizer Covered_h → servability ┘   TWO finalizers
```

**Confirmed:** the fiber is ambient, not the argument; \(D\) sits between fiber and state; support is a separate
state; a finalizer is last.

**Falsified in two places:**

- **support/evidence state is *not* downstream of value state.** MA §2.4 folds \((s,e,o)\) as **one combined
  commutative monoid** — they are **parallel**, and Lemma \(G_1.L2\) is exactly the proof that the combination is
  a monoid. A pipeline ordering would misdescribe the theorem.
- **there is not one finalizer but two**, and keeping them apart is what stops support from becoming meaning:
  \(\rho_\kappa\) for the value, \(Covered_h\) for servability.

**And one insertion:** **contributions** between \(D\) and the state, because `replicate` makes points and
contributions genuinely different (§1.4).

---

## 7. Does it change the frozen declaration model?

### 7.1 `clause = source × scope` — **survives, with no new field**

Applying Huayin's discipline — *do not add a field merely because the algebra needs a fact; first determine where
the fact comes from* — to each conjunct of \(D\):

| input to \(D\) | comes from | already in the model? |
|---|---|---|
| existing points, sparsity | **the universe** | yes — outside the family, as designed |
| \(E_F\), eligibility | **the observational grounding** | **yes** — the `observes` clause's optional `for` |
| the law's participation rule | **the cited law**, plus `co-participating` where multi-operand | **yes** |
| restriction in the resolved target | **the request**, under the pin-versus-population criterion | yes — request layer, not declaration |

> **All four have homes; three are outside the family declaration; the fourth was already there.**
> **No new field. `source × scope` stands.**

### 7.2 Two independent corroborations of things already decided

- **Amendment 1 (retiring contribution multiplicity) is confirmed by a source not consulted when it was made.**
  MA §2.5 puts multiplicity in an **explicit governed expansion** with a declared disposition — *"Replication is
  admitted on the relation edge by its own expansion rule, **with multiplicity governed separately**"* — and
  Theorem \(G_2.8\) refuses inherited certification across a reducer when replication is unaccounted for.
  **Multiplicity belongs to a construction, not to a family clause.** That is exactly the amendment.
- **A.12 (pin versus population) is corroborated.** MA §5's **restriction/carve** distinction and Theorem
  \(G_1.6\) are the same boundary in the algebra's vocabulary: *"restriction and carve are contractually different
  even though their current value functions **may** agree on the exposed subset. **A carve therefore needs a
  distinct population identity.**"*

### 7.3 The LAST/SUM conclusion — **unchanged**, with one refinement

The rectangularity argument was already stated over the **participating** domain, and ToD §6.1's \(D_A(a)\) is
precisely that object. ToD §11.2's ruling — *"an interchange law would need its own premises"* — is untouched.

> ⚠ **One refinement, and it matters for the third pending decision.** Since **\(D\) is selected by the law *and
> the resolved request*** (§4.2), **rectangularity of \(D\) can be request-dependent.** So *"is rectangularity a
> fact a universe may declare?"* has a sharper answer than I gave: a universe can declare rectangularity of the
> **eligible** region, but a request that narrows participation can make a rectangular region ragged. **Any
> interchange licence must therefore be checked against the resolved \(D\), not only against the universe.**

Decisions 1 and 2 from the interchange note (composition closure; clause-incoherence versus path-disagreement)
are **unaffected** and still pending.

---

## 8. A second, symmetric gap — this one in ToD

Fairness requires recording that ToD is not complete here either.

> **ToD v7.1 never states any relation between \(D\) and \(E\).** \(E_{F,A}\subseteq A\) is defined at the
> **target** anchor (§2.3); \(D\subseteq I\) is defined at the **constitutive input** anchor (§4.2, §6.1). They
> are introduced in different sections, at different anchors, with **no bridging axiom** — no \(D=E\cap I\), no
> \(D\subseteq E\), nothing.

§3.1 and the §4 contract table list eligibility and participation as **separate** items, which is the best
evidence they are not the same. §9.3 supplies the operative bridge in prose rather than in symbols — *"ordinary
LAST over **eligible points**"* versus *"LAST over **supported observations** [which] has a different
participation rule"* — from which the working reading is: **eligibility supplies the ordinary participation rule,
and other rules are declarable departures from it.** That reading is sound and is what §6 assumes, **but it is
inferred, not stated.**

Two smaller silences, both flagged rather than filled: §11.5's *"empty-count law"* is **named and never stated**;
and §11.5.1's MIN/MAX sentence mixes registers, giving the semigroup over *"nonempty **supported** fibers"* while
stating the empty case over an *"empty **eligible** fiber"* — the one place in §11.5 where \(D\) is absent and
both \(E\) and \(S\) appear as fiber qualifiers.

---

## 9. Later Measure Algebra drafts — **proposals, not results**

**Kept strictly separate, per instruction. None of the following is published v1.0, and none of it should be
cited as establishing anything.**

| document | status, in its own words |
|---|---|
| `measure_algebra_design_record_v0_3.md` | *"design record. **No implementation is authorized by this document.**"* |
| `measure_algebra_finding_1_support_participation_v0_1.md` | *"design finding + **proposed amendment**… design only"* |
| `measure_algebra_finding_2_typed_values_and_state_v0_2.md` | *"design finding + **proposed amendment**… read-only reconciliation"* |

**What they propose that bears on this question:**

- **Design Record v0.3** carries the same state-law table, including the *"same governed contributions"* row —
  confirming the phrase is MA's own lineage from ToD v6.1 §4.7, and **not a v7.1 term**.
- **Finding 1** proposes a *Support Sufficiency Principle*: *"**Support identity need never be retained past a
  reduction whose participation law was declared BEFORE that reduction. Retention is the price of DEFERRING the
  participation decision.**"* — i.e. **declare participation early and the support bookkeeping collapses.**
  This is a *proposed* result, and it is the sharpest statement in the estate of why participation must be an
  analytical declaration rather than an execution outcome. **It is also consistent with everything in §§1–2
  above**, which is a point in its favour and not an argument for adopting it here.
- **Finding 2** records that **participation is `Absent`** from the current implementation's type-and-state
  representation, and that *"support / participation standing [is] **ABSENT from both keys and both payloads**."*

> **None of these is needed for the correction in §6.** The correction comes from **published ToD v7.1 §6.1**,
> which is the point: **the repair does not require adopting any draft.**

---

## 10. Report summary

1. **MA v1.0** — establishes that population comes from eligibility not support, that participation is an
   analytical choice not a join default, that carve ≠ restriction, and that the monoid theorems govern
   *regrouping of the same governed contributions*. **It does not establish the reducer's argument domain under
   \(G_1\); it defers it and lists richer participation rules as open. §2.3 is formally loose, and I say so
   plainly.**
2. **ToD v7.1** — **already gives the corrected formulation**: §6.1's contributing fiber \(D\cap\pi^{-1}(a)\),
   §4.2's *"selected by the law and the resolved request"*, §8.2's participating domain for LAST, §2.3's
   four-way distinction among absence kinds, and explicit prohibitions on substituting the identity for an
   unavailable value.
3. **Contract Calculus** — **not deposited in this repository.** \(G_0\) has no \(E\)/\(S\), which is why
   `Fib_q(b)` is unproblematic there; the \(G_1\) partial-reducer denotation is cited and not reproduced. **Check
   the deposit before treating §6 as settled.**
4. **Later MA drafts** — §9. All three are **design records / proposed amendments**, none published. Finding 1's
   *Support Sufficiency Principle* is the sharpest statement of why participation must be declared, **and the §6
   correction does not depend on it.**
5. **Smallest correction** — §6.1: adopt ToD §6.1's contributing fiber in MA §2.3, set \(e=|D|\), and read the
   fold as over contributions.
6. **Effect on the frozen model** — **none.** `source × scope` survives; the LAST/SUM conclusion survives with a
   request-dependence refinement; two earlier decisions gain independent corroboration.

---

**Stopped at the report.**

# Measure Algebra — Design Finding 1
## Support Representability and Participation

**Version:** 0.1 · **Date:** 31 August 2026
**Type:** design finding + **proposed amendment** to *The Measure Algebra of the Theory of Data — Design Record v0.3*
**Mandate:** design only. **No code, grammar, Manual, ledger or Unit D work is authorized by this document.**
**Written in:** canonical ToD v6 terms. No Core vocabulary migration; no Unit D dependency.

Starting point, as given:

> Two governed measures may both have a value at the same analytical coordinate while resting on
> different underlying observational support. Coordinate presence therefore does not establish
> common support. **(P1-12)**

---

## 0. Verdict

**The smaller interpretation is correct, and it is adopted — more strongly than expected.**

> **This is principally a MATERIAL WITNESS problem for a support theory the corpus has largely
> already built. The two shipped defects do not merely lack a law; they contradict a PROVED THEOREM.**

Three findings, in descending order of consequence:

1. **Support is already a contract component, not a proposal.** The Contract Calculus defines
   $C_1=(X,U,A,E,S,\beta,\gamma)$ with $v:S\to|X|$ — support is a **set**, and it sits *inside the
   contract* alongside the type, universe and anchor.
2. **The joint multi-measure rule already exists, and is already conservative.** MAP1 — the strict
   intersection-map — gives $E'=\bigcap E_i$, $S'=\bigcap S_i$, $\beta'=\bigcup\beta_i$,
   $\gamma'=\bigcap\gamma_i$. It is safe. **It is also silent about divergence**, which is the gap.
3. **Complete-case alignment is a CARVE, and carve ≠ restriction is a theorem.** *Missingness* §8.1:
   *"if $E$ is formed as an intersection of observed supports it is a **carve, not a restriction**,
   and the joint object then denotes a selected subpopulation with a mechanism of its own… A lawful
   joint frame is built from **eligibility** sets."* And §11.4: the complete-case intersection
   *"should not silently inherit the universe name of the original members."* The Contract Calculus
   **proves** the two are inequivalent (Theorem G1.6) even when their value functions agree.

**P1-11 is that theorem being violated.** `how="inner"` intersected *observed supports*, which is a
carve, and the column went on asserting `population: ops` — silently inheriting the universe name the
corpus says it must not. **P1-12 is the evidence that would have revealed the carve, not retained.**

**What is genuinely open is narrower than "new Measure Algebra law", and the corpus says so itself.**
The Contract Calculus's own claim table marks *"Partiality, eligibility, support, observation, and
evidence form a complete calculus"* as **"Not claimed — framework extension"**; §8.2 defers
*"alignment and frame synthesis"* to later extensions; *Missingness* §17.4 records that it *"does not
yet provide a complete algebra for propagating M-contracts."*

> **So the cross-measure support-divergence case sits in a gap the corpus has already scoped as
> future work, adjacent to proved fragments on both sides. It is a fragment extension, not a
> foundation.** That is the smaller interpretation, and the evidence supports it.

**Confidence.** High on the verdict and on §§1–3. Moderate on §4's minimal-representation result,
which is derived here rather than cited — though its central quantity turns out to be already proved
sufficient state (§4.1), which raises confidence considerably.

---

## 1. What the corpus already supplies

### 1.1 Support is a SET, and it is part of the contract

ToD v6.1 §3.5 / §7.3: $S_{F,A}\subseteq E_{F,A}\subseteq A$, with $m_{F,A}:S_{F,A}\rightarrow V_F$,
under the layering $\lambda_U \rightarrow$ point existence $\rightarrow A \rightarrow E_{F,A}
\rightarrow S_{F,A} \rightarrow$ value, distinguishing: point absent from the universe · point exists,
measure ineligible · point eligible, unsupported · **point supported with value zero**.

The Contract Calculus makes it structural (G1.D4/G1.D5):

$$S\subseteq E\subseteq P,\qquad v:S\to|X|,\qquad C_1=(X,U,A,E,S,\beta,\gamma)$$

*Missingness* §4.5 gives the same chain per member —
$\operatorname{Pts}(A_V)\supseteq P_{U,A_V}\supseteq E_v\supseteq S_v$ — and the governing rule:
*"Missingness is defined on $E_v$, not on every conceivable coordinate and not merely on the rows that
happened to be stored."*

**Support is indexed by the MEASURE, never by the coordinate.** Two measures at one coordinate have
two different $S$ sets by construction, and all three papers already have vocabulary for that.

### 1.2 The $(e,o)$ counts are already PROVED sufficient state

This is the find that most changes the shape of the answer. Contract Calculus §15.1, §15.3–15.4:

$$e_q(a')=\left|\operatorname{Fib}_q(a')\cap E\right|,\qquad o_q(a')=\left|\operatorname{Fib}_q(a')\cap S\right|$$

$$\widehat S_\kappa=S_\kappa\times\mathbb N\times\mathbb N,\qquad
(s,e,o)\ \widehat\oplus_\kappa\ (s',e',o')=(s\oplus_\kappa s',\,e+e',\,o+o')$$

embedded per point as $(\eta(v(a)),1,1)$ · $(0,1,0)$ · $(0,0,0)$, with the gloss: *"The first
component contains sufficient state for observed values only. The second and third components carry
the analytical domain facts needed to decide eligibility and support."*

**An eligibility/observation counter is not a design proposal. It is proved reducer sufficient state
with a proved componentwise combiner.** *Certifiable State* §4.3 gives the same pair as claim
transport, with $Any(b)\mapsto o_b>0$ and $Complete(b)\mapsto e_b>0\wedge o_b=e_b$.

### 1.3 Coverage is a declared permission, and the system may not infer it

Contract Calculus §14.3: $\mathsf{Cov}=\{\mathsf{Any},\mathsf{Complete}\}$, carried by a
coverage-permission map $\gamma:\mathsf{AggCap}\to\mathcal P(\mathsf{Cov})$ — and decisively:

> *"This permission is contract specific… **$G_1$ records the permission but does not infer it.**"*

*Certifiable State* §2.1 lists **"participation and support rules"** among the contract coordinates of
$\Gamma$, with: *"$\Gamma$ is not commentary on $K$. **It can change what operations are lawful even
when $K$ is numerically unchanged.**"*

### 1.4 The joint rule exists — MAP1 — and it is lossy in exactly the respect asked about

Contract Calculus §17.2, the strict intersection-map:

$$E'=\bigcap_i E_i,\qquad S'=\bigcap_i S_i,\qquad
\beta'(\kappa)=\bigcup_i\beta_i(\kappa),\qquad \gamma'(\kappa)=\bigcap_i\gamma_i(\kappa)$$

Union of blocked axes, intersection of coverage permissions: conservative and safe. **But the output
records $S'$ and nothing about how $S_1$ and $S_2$ differed.** Downstream, $S'$ is indistinguishable
from a single measure that happened to be observed exactly on $S'$.

> **That single sentence is P1-12 in the corpus's own machinery.**

### 1.5 Complete-case is a CARVE — and carve ≠ restriction is proved

*Missingness* §8.1, on building a joint eligible frame:

> *"if $E$ is formed as an intersection of **observed supports** it is a **carve, not a restriction**,
> and the joint object then denotes a selected subpopulation with a mechanism of its own. **A lawful
> joint frame is built from eligibility sets.**"*

§11.4: $S_{\mathrm{cc}}=\bigcap_j S_{v_j}$ *"may define a selected subpopulation with its own
missingness mechanism. **It should not silently inherit the universe name of the original members.**"*

Contract Calculus §16.3 and **Theorem G1.6**: restriction and carve *"may have identical current value
functions on $S\cap R$, but their contracts are not equivalent."*

### 1.6 The value-path analogue of the non-derivability result is already published

*Two Anchors* §6:

> *"the necessary pointwise products may be unrecoverable. **An average price of \$7.50 and a total
> quantity of 12 do not determine the weighted numerator 70.**"*
> *"The input anchor can be a typing and co-location requirement of the operation that constructs
> sufficient state."*

§4.2's principle: *"Analytical storage must preserve three things separately: the value, the sufficient
state required for lawful continuation, and the identity-bearing contract fields required to know what
the value means."*

### 1.7 Joint ignorability does not decompose

*Missingness* §8: *"Ignorability is a property of the **joint** law of the whole response pattern, and
it does not decompose member by member. Per-member contracts that are each MAR can aggregate to a
non-ignorable joint mechanism."* The coupling premise (SF) is *"a located premise that the per-member
contracts leave implicit… **It should be a declared clause of the joint contract with its own evidence
status.**"*

And the structural escape, **(C1) Complete parents**: $S_{v_l}=E$ — supports equal to eligibility by
construction. **The corpus already names the contract that removes the need for a witness.**

### 1.8 State composability does not imply certificate composability

*Certifiable State* §6, Proposition 4, and Contract Calculus §19.7 (Theorem G1.7) agree:

$$\boxed{\text{state composability}\not\Rightarrow\text{certificate composability}}$$

> *"If the disjointness or overlap premise is absent, the numeric merge still executes. The certificate
> derivation does not."*
> *"A computation does not become a governed analytical object merely because a host engine can
> execute it."*

---

## 2. What Columna materially lacks

1. **Support is a scalar cardinality.** `Engine.validate_universe_support`'s docstring states the
   set-valued law — *"cover the SAME support (the same set of base points)"* — and implements a
   **count** comparison, describing itself as *"the COUNT-reducer instance of a more general
   path-independence check."* Zero callers.
2. **$o_b$ is computed and discarded in the same statement.** The engine delivers one aggregate per
   measure per coordinate; the observation count is consumed inside the SQL aggregate and never
   returned. The corpus's proved domain state $(e,o)$ is produced and thrown away.
3. **No joint quantity exists at any grain**, so a participation law can only be *defaulted to*.
4. **No carve is ever declared.** The intersection happens; the universe name persists.

**A structural observation.** P1-10, P1-11 and P1-12 are the **three objects of §5 failing, one each**:

| row | object that failed | corpus rule violated |
|---|---|---|
| **P1-10** | the **support contract** — `count` claimed row-support, siblings claimed value-support, inside one family | coverage permission *"recorded, not inferred"* |
| **P1-11** | the **participation result** — `how="inner"` chose complete-case | **carve ≠ restriction (Theorem G1.6)**; *"should not silently inherit the universe name"* |
| **P1-12** | the **realized support evidence** — nothing retained | MAP1 records $S'$, not the divergence |

That they failed separately is itself evidence that they are separate objects.

---

## 3. What is actually missing

### 3.1 Not a new joint predicate — a divergence witness at MAP1's output

My first draft proposed a cross-measure `Complete` predicate as "the one new law." **That was too
large a claim**: MAP1 already gives the multi-measure intersection, and $Any$/$Complete$ already exist.

The precise gap is narrower:

> **MAP1's output contract records the intersection $S'$ but not the fact that a carve occurred, nor
> how far $S_1$ and $S_2$ diverged. A joint result therefore cannot state its own population claim.**

What must be added is not a predicate but a **retained divergence fact** — and, because
$S'=\bigcap S_i$ is a carve, a **declared output universe** for the carved population.

### 3.2 The non-derivability that makes it unavoidable

Define, at output coordinate $b$ over input anchor $A'$:

$$o_b^{F\wedge G}=|\{a\in S_{F,A'}\cap S_{G,A'}:(a,b)\in R\}|$$

> ### $o_b^{F\wedge G}$ is not a function of $o_b^{F}$ and $o_b^{G}$.

Two configurations with identical marginal counts and identical marginal values can have different
intersections, hence different joint quantities.

**This is the support-path analogue of *Two Anchors* §6's value-path result** — *"an average price of
\$7.50 and a total quantity of 12 do not determine the weighted numerator 70"* — and it has the same
remedy: **form the joint object where the operands are co-located, before reduction.** The corpus
already draws that conclusion for values; this finding observes that support obeys it too.

---

## 4. The minimal representation, derived

The instruction was explicit: *do not assume the answer is "attach a bitmap to every value."* It is not.

### 4.1 A support-witness ladder — retained state, NOT evidence grade

These are grades of **retained state $K$**, not evidence statuses $(\mathcal G,\preceq)$. The corpus's
own $\mathbb K=(K,\Gamma,E)$ is what keeps the two from being confused. **W1 is not proposed here** —
it is the Contract Calculus's $\widehat S_\kappa = S_\kappa\times\mathbb N\times\mathbb N$, with its
combiner already proved. W2 and W3 are the additions this finding identifies, and they exist only
because the cross-measure case escapes W1 (§3.2).

| grade | what is retained, per output coordinate | sufficient for | **insufficient for** |
|---|---|---|---|
| **W0** | nothing | available-case value only | telling a declared divergence from an accidental one |
| **W1** | the pair $(e_b, o_b)$ — **already proved sufficient state**, Contract Calculus §15.3 | `Any` / `Complete` for **one** measure over its own fiber (proved); available-case denominators; a **one-sided** cross-measure divergence test | any cross-measure claim: $o^F_b=o^G_b \not\Rightarrow S_F=S_G$ |
| **W2** | an order-insensitive, mergeable **support digest** of $S_{F,A'}\cap R^{-1}(b)$ | equality testing w.h.p.; approximate $\lvert S_F\cap S_G\rvert$ (MinHash-class) | computing the joint **value** over the intersection |
| **W3** | support **identity** — the point set itself | exact post-hoc complete-case and pairwise formation | — |

And the grade that dominates all of them:

| **C** | a **declared support contract** making the supports equal *by construction* | everything | — |

### 4.2 The two results

**Result 1 — the honesty floor is W1, and the explanation floor is W2.**

W1 is enough to stop serving a false claim: if $o^F_b \neq o^G_b$ the supports differ, full stop. It
is **not** enough to conclude they agree. W2 is the first grade at which *"declared divergence vs
accidental divergence"* — P1-12's own words — becomes decidable. So:

> **The cost of honesty is far below the cost of computation.** W2 buys a true disclosure; only W3 or
> co-reduction buys a joint answer.

This maps onto the four moods exactly: at W0 a joint ask cannot be adjudicated at all; at W1 it can be
refused or served-available-case with a divergence caveat; at W2 the caveat can be *accurate*; at W3
the joint reading can be *served*.

**And there is a disposition W-grades alone do not supply.** Because a complete-case intersection is a
**carve** (§1.5), serving it requires more than evidence — it requires a **declared output universe**
for the carved population, since it *"should not silently inherit the universe name of the original
members."* **Evidence tells you a carve happened; only a declaration tells you what the carved thing
is.** A system at W3 with no carve declaration can compute the joint number and still not name its
population — which is Theorem G1.6 arriving at the wire.

**Result 2 — the Support Sufficiency Principle** *(proposed)*

> **A materialization must retain support evidence of the grade sufficient for the participation laws
> it claims to support — and no more.**
>
> **Support identity need never be retained past a reduction whose participation law was declared
> BEFORE that reduction. Retention is the price of DEFERRING the participation decision.**

This is v0.3 §5.1's ordering rule one level down, and it is the compression answer. If the
participation law is declared first, the reduction is taken **over the joint support** and the joint
quantity is consumed where it exists — after which W0 suffices downstream, because there is nothing
left to disagree about. A bitmap is what you need only when you have already reduced separately.

**Grounding, not invention.** This is *Certifiable State* §5.4's own distinction: a support-equality
premise discharged from a **declared contract** is a *schema-level premise*; the same premise
discharged by comparing realized sets is a *data-dependent premise*, and *"establishing such a premise
is itself an evidence event."* **Declaring earlier lowers the required grade because it moves the
premise from data-dependent to schema-level.** Mission A′ (P1-10) is a worked instance: it did not
build a witness, it made the supports equal by construction and thereby removed the need for one.

### 4.3 What can lawfully be discarded

- Everything above the grade the declared participation claim requires.
- **W3 → W2** whenever only *detection and disclosure* are claimed, never joint serving.
- **W2 → W1** whenever the participation law is available-case per measure.
- **W1 → W0** whenever a support contract makes supports equal by construction — the only lawful route
  to W0, and the cheapest available answer.
- Support identity may be discarded at any reduction that has already consumed it under a declared
  participation law.

**What may never be discarded:** the *contract* and the *participation law*. They are $\Gamma$, they
are cheap, and by §1.3 they change what is lawful even when the numbers do not move.

---

## 5. The three objects, and why they must stay separate (Q5)

They are not three fields of one record. They are the corpus's governed-state triple:

| object | corpus location | time (v0.3 §9) | what it is |
|---|---|---|---|
| **support contract** | $\Gamma$ — *"participation and support rules"* | **declaration** | what this family *claims* about where it is supported |
| **realized support evidence** | $K$ (grade W) + $E$ (attestation) | **adjudication / materialization** | what was *found*, for this data as attested |
| **participation result** | a claim $c$, with $\mathbb K\Vdash_g c$ | **ask** | the outcome of applying a participation law to two measures' evidence |

Collapsing any pair reproduces a shipped defect: contract into evidence gives **P1-10**; result into
evidence gives **P1-11**; evidence absent altogether gives **P1-12**.

---

## 6. How support evidence composes (Q6)

**Support evidence composes under the same state law as the value it witnesses, because it *is* a
measure** — the count of $F$'s own supported contributions.

- **W1** composes as a commutative monoid under **disjoint** contribution: $o$ adds.
- **W2** composes iff the digest is mergeable by construction (XOR/sum of point-ID hashes; a MinHash or
  Theta sketch).
- **W3** composes by union.

**And it inherits the multiplicity hazard exactly.** Under fan-out (ToD §7.4), one root point
contributes to several output points, and $o$ over-counts precisely as SUM over-counts. This is not a
new caveat: it is *Certifiable State* §6's missing disjointness premise, and the same
$Cert(Disjoint(\cdot))$ is what licenses the composition.

> **A support witness is a measure, so it is governed by its family's contribution semantics — not by
> arithmetic on the carrier.** A support count composed without the disjointness premise is the same
> error as the uncertified SUM of 300 in ToD §7.4.

**A material observation that follows.** After Mission A′, `F.count` over a declared VALUE *is*
$o_b^F$ — the observation count of $F$'s own support at the asked anchor. **W1 is therefore already a
shipped, now-correct family member**, not new machinery. That does not close P1-12 (which needs the
*joint* quantity of §3.2), but it means the honesty floor is materially much nearer than the ledger
implies, and it should be stated in any implementation mission that follows.

---

## 7. When value state survives but support evidence is lost (Q7)

The corpus answers this directly and the answer is not "disclose harder."

By $\boxed{\text{state composability}\not\Rightarrow\text{certificate composability}}$ and
Proposition 4, the numeric merge remains defined and exact while **no certificate derivation exists**
for the joint claim. The correct disposition is refusal in the corpus's precise sense:

$$\boxed{\mathbb K\not\Vdash_g c}\qquad\text{— }\textit{"the absence of a certificate is not repaired by the presence of a value."}$$

Three consequences:

1. **It cannot be repaired by recomputation.** Conservation (§1.6): evidence-neutral transformation
   does not manufacture warrant. Re-running the query re-loses the same evidence.
2. **At W0 the planner cannot even caveat honestly**, because it cannot distinguish a declared
   divergence from an accidental one — so a disclosure would assert a distinction it has not made.
   **W0 + a joint ask is a capability-honesty failure of the P1-14 family**, one level up from the
   surface: the system serves a number whose analytical identity it does not know.
3. **The value's own continuation is unaffected.** Value sufficient state and support-sufficient state
   are independent, which is *Certifiable State*'s central principle applied to this case:
   $\boxed{\text{information loss}\neq\text{evidential loss}\neq\text{loss of informativeness}}$.

---

## 8. Reusable joint state — identity vs attestation (Q8)

> **The support contract and the participation law belong to SEMANTIC IDENTITY. The realized support
> set belongs to MATERIAL ATTESTATION.**

A joint moment state $(N,\Sigma x,\Sigma xx^{\mathsf T})$ computed complete-case and one computed
pairwise are **different analytical objects** and are not substitutable, even at numerically identical
values — precisely §1.3's *"$\Gamma$ can change what operations are lawful even when $K$ is numerically
unchanged."* This mirrors ToD §7.6's regime (identity-bearing) versus approximation
(certificate/materialization).

**Operational consequence, stated because it is a soundness property and not a preference:**

> A reusable-state cache keyed on *(family, anchor, filter)* alone is **unsound** as soon as two
> participation laws are admissible. The key must carry the participation law and the support
> contract. It must **not** carry the realized support set — that is attestation, it belongs in $E$,
> and putting it in the key would defeat reuse across refreshes for no analytical gain.

---

## 9. Complete-case versus pairwise (Q9)

| | complete-case (listwise) | pairwise |
|---|---|---|
| the support used | one set: $\bigcap_i S_i$ | one set **per pair**: $S_i\cap S_j$ |
| evidence required | a single joint reduction over the intersection, **or** W3 | $\binom{k}{2}$ joint reductions, **or** W3 once |
| retained-state cost | $O(1)$ if co-reduced | $O(k^2)$ if co-reduced |
| **what it does to the population** | **ONE carve** — a new declared subpopulation | **$\binom{k}{2}$ DIFFERENT carves**, one per entry |
| what the numbers hide | the carved population may be small and unrepresentative | **the entries do not share a population at all** |

**The asymmetry, in the corpus's terms.** Complete-case performs *one* carve, so the result has *a*
population — it simply is not the one the operands named, and per §1.5 it must be declared rather than
inherited. Pairwise performs a **different carve per entry**, so the assembled object has **no single
population to declare.**

> **That is the real difference, and it is not a matter of cost.** Complete-case needs a declared
> universe; pairwise needs a declared universe *per entry*, which is another way of saying the
> assembled matrix is not a single governed analytical object at all unless something certifies how
> its entries relate.

This is also why a pairwise covariance matrix need not be positive semi-definite while a complete-case
one is: PSD-ness is a property of a Gram matrix over **one** population, and pairwise construction does
not produce one. **The numerical pathology is the population incoherence, showing through.**

## 10. `CovarianceMatrix<Variables, Population>` — the construction witness (Q10)

The type is the question. `Population` is **not** the universe; it is *"the population this matrix's
entries were actually computed over,"* which under pairwise construction **is not single-valued.**

**`Population` is not single-valued under pairwise construction** (§9): the type parameter names a
population the object may not have. That is the sharpest statement of why this type needs a witness
rather than a parameter.

**Why numeric values cannot determine standing.** Two matrices of identical shape and plausible
magnitudes:

- **complete-case** — every entry over $\bigcap_i S_i$; PSD; possibly a tiny, unrepresentative population;
- **pairwise** — entry $(i,j)$ over $S_i\cap S_j$; **need not be PSD**; a downstream Cholesky,
  inversion, or regression may fail or, worse, succeed and be meaningless.

Nothing in the numbers separates them. So the type requires a **construction witness**, and the corpus
already says what shape that has: $Cert=(c,\delta,gr(\delta))$ — a claim, an **inspectable derivation
object**, and a grade — with *"a weaker emitted certificate is not silently upgraded merely because a
stronger derivation exists."*

**Minimum contents of the witness:**

1. the **participation law** under which the matrix was formed;
2. the **support contract** of each variable;
3. the **carve(s) performed** — one declared subpopulation for complete-case, $\binom{k}{2}$ for
   pairwise — since a carve *"should not silently inherit the universe name of the original members"*;
4. the **support cardinalities** actually used — $(e,o)$ per entry;
5. a **derived, recorded** structural verdict (e.g. PSD) rather than a property a consumer is expected
   to know to re-check;
6. the **evidence grade** of (4), since a support cardinality established by measurement is itself an
   evidence event.

**Why this cannot be a value-only type.** *Certifiable State* §13.1: a value-only operator exposes only
$\Phi_T$; *"governed family closure is earned by the completeness of the operator signature, not by the
existence of an executable function."* A covariance matrix produced by a value-only operator is exactly
the object that cannot state its own standing — **which is v0.3's O3, reached from the other side.**

---

## 11. The five worked cases

**(a) Same coordinate, same support.**
Sharper than it looks: *sameness is not observable at W1.* $o^F_b=o^G_b$ is consistent with disjoint
supports of equal size. W2 certifies it; a **contract** makes it true without measuring. Available-case,
complete-case and pairwise all coincide, and this is the only case where they do — which is why it is
worth making true by declaration rather than discovering by comparison.

**(b) Same coordinate, different support — P1-12.**
W1 **detects** it (one-sided). W2 **explains** it — declared vs accidental. W3 or co-reduction
**resolves** it. Today, at W0: the ratio serves and *"20.0 is not flatly wrong… and that is precisely
the defect: which one it is depends on a law nobody declared."*

**(c) Complete-case two-measure reduction.**
Needs $o_b^{F\wedge G}$, which by §3.2 is not recoverable from the marginals. Either **co-reduce at
$A'$** under the declared law — after which W0 suffices downstream — or retain W3. **This is the case
that proves declaration-before-reduction is a compression technique, not merely good hygiene.**
And evidence is not sufficient on its own: the result is a **carve**, so it also owes a declared output
universe. *"A lawful joint frame is built from eligibility sets"* — building it from observed supports
is admissible only when the new population is named.

**(d) Pairwise covariance.**
$\binom{k}{2}$ distinct supports — and therefore $\binom{k}{2}$ distinct **carves**, which is why the
assembled matrix has no single population to name (§9). W3 pays for itself here; the result needs the
§10 construction witness; and PSD-ness must be **recorded**, not assumed, because its failure is the
population incoherence showing through rather than a numerical accident. The one case where retaining
support identity is the economical choice.

**(e) Reusable joint moment state.**
$(N,\Sigma x,\Sigma xx^{\mathsf T})$ is *value*-sufficient for mean, covariance, correlation and OLS —
and **support-terminal** the moment the participation law is not carried with it, because $N$ alone
cannot say which population it counted. Cache key: family, anchor, filter, **participation law,
support contract**. Attestation: the realized supports and their evidence grade. And per §1.6, a
cached state may not be *promoted* to a stronger participation claim later without a new evidence
event — Conservation: *"evidence-neutral transformation does not manufacture warrant."*

---

## 12. Proposed amendment to Design Record v0.3

Offered as text, not applied. Five edits.

**A · §5.3 — replace the closing paragraph.** It currently says support "must be a first-class fact
carried with the datum." That is too strong and names a mechanism. Replace with:

> **The corpus already carries the law; Columna lacks the witness.** ToD §3.5/§7.3 define support as a
> set and *Certifiable State* §4.3 already transports it as $(e_b, o_b)$ with `Any` and `Complete`
> defined over them. What a materialization owes is a **support witness of the grade sufficient for
> the participation laws it claims to support** — which may be nothing at all when a declared contract
> makes supports equal by construction. See Design Finding 1.

**B · §6 — add, as the participation section's governing economy:**

> **Support Sufficiency Principle.** A materialization must retain support evidence of the grade
> sufficient for the participation laws it claims to support, and no more. Support identity need never
> be retained past a reduction whose participation law was declared *before* that reduction; retention
> is the price of deferring the participation decision.

**C · §8 (derivability) — add to the open half:**

> A result's standing may be undeterminable from its values. `CovarianceMatrix` under pairwise versus
> complete-case construction is the canonical case: same shape, plausible numbers, different analytical
> object, and only one of them reliably PSD. The construction witness has the shape *Certifiable State*
> §2.3 gives — $Cert=(c,\delta,gr(\delta))$ — and a value-only operator cannot produce one.

**D · §11 — amend O1, and add O8.**

> **O1 (amended).** Support is not materially represented. **The law is not missing** — ToD §3.5/§7.3
> and *Certifiable State* §4.3 supply it. *Closes when* a support witness exists at a declared grade,
> and when the joint quantity $o_b^{F\wedge G}$ is either materialized under a declared participation
> law or witnessed.
>
> **O8 (new).** MAP1 already gives the multi-measure intersection $S'=\bigcap S_i$, conservatively.
> What it does **not** record is that a **carve** occurred, or how far the operand supports diverged —
> and $o_b^{F\wedge G}$ is not a function of the marginals. *Closes when* (a) a divergence witness is
> retained at joint formation and (b) a carved joint population is **declared** rather than inheriting
> the operands' universe name. **This sits in a gap the corpus itself scopes as future work** —
> Contract Calculus §2.1 marks the support/observation/evidence calculus *"Not claimed"* and §8.2
> defers alignment; *Missingness* §17.4 defers the M-contract propagation algebra. It is a fragment
> extension, not a new foundation.

**E · §2 — add to the do-not-promote list:**

> **A support count is not a support set.** Columna's `validate_universe_support` states the set-valued
> law in its docstring and implements a count comparison. The count is a projection: the Contract
> Calculus proves $(e,o)$ sufficient **within one measure's own fiber**, and the cross-measure case
> escapes it because counts do not determine intersections. Promoting the count to the definition
> would make a present material limitation into law, which is what §2.2 exists to prevent.
>
> **And an intersection of observed supports is not a filter.** It is a **carve** — a new population —
> and treating it as a restriction is inequivalent by proof (Contract Calculus Theorem G1.6), not by
> convention. P1-11 is that theorem being violated on a shipped wire.

---

## 13. What this finding does NOT close

- **Which participation laws Columna should admit.** Available-case, complete-case and pairwise are
  described here; declaring the admissible set is a ruling.
- **Whether a support contract is per-family, per-measure, or per-declaration.** P1-10 shows two
  contracts *inside* one family, so "per-family" is not obviously right.
- **The witness's material form.** W2 in particular has real choices (mergeable hash-sum vs MinHash vs
  Theta) with different composition properties. Deliberately not selected.
- **Whether the carved population needs a NAME or only a marker.** *Missingness* §15.3 says
  complete-case selection *"should be represented as a carve with an explicit resulting universe"*.
  Whether Columna would need a full declared universe per joint expression, or a lighter derived-scope
  marker, is a real design fork and is not resolved here.
- **The relationship between $\gamma'=\bigcap\gamma_i$ and a participation law.** MAP1 already
  intersects coverage permissions. Whether a participation law is a *third* thing or is expressible as
  a coverage permission over a joint capability is an open question — and the smaller answer would be
  better if it holds.
- **Anything about implementation.** No mission is proposed and none is authorized here.

---

## 14. Corpus index

| source | supplies |
|---|---|
| **ToD v6.1** §3.5, §7.3 | $S_{F,A}\subseteq E_{F,A}\subseteq A$; the four absence cases; *"support does not silently redefine the anchor"* |
| **ToD v6.1** §4.6, §4.7, §7.4 | value ≠ sufficient state ≠ analytical identity; the state-law classes; multiplicity/fan-out |
| **Contract Calculus** G1.D4–D5, §14.2–14.3 | $C_1=(X,U,A,E,S,\beta,\gamma)$; the four absence states; $\mathsf{Cov}=\{\mathsf{Any},\mathsf{Complete}\}$ *"recorded, not inferred"* |
| **Contract Calculus** §15.1, §15.3–15.4 | $(e_q,o_q)$; $\widehat S_\kappa=S_\kappa\times\mathbb N\times\mathbb N$ with a proved componentwise combiner — **W1** |
| **Contract Calculus** §16.3, §17.2, Thm G1.5–G1.7 | MAP1; restriction vs **carve**; no automatic observed zero; coverage refusal ⟂ determinism |
| **Missingness Has a Universe** §4.5, §8.1, §11.4, §15.3 | $S_v$; joint frames built from **eligibility**; complete-case is a **carve** that must not inherit the universe name |
| **Missingness** §8, §8.5 | joint ignorability does not decompose; **(C1) complete parents** $S_{v_l}=E$ — the contract that removes the need for a witness |
| **Two Anchors** §4.2, §6 | co-location before reduction; *"an average price of \$7.50 and a total quantity of 12 do not determine the weighted numerator 70"* |
| **Certifiable State** §2.1, §4.3, §5.4, §6, §13.1, §13.3 | *"participation and support rules"* in $\Gamma$; support transport; schema-level vs data-dependent premise; state ⇏ certificate composability; terminality; value-only operators cannot yield standing |

---

*End of Design Finding 1. Design only; no implementation is authorized by this document.*

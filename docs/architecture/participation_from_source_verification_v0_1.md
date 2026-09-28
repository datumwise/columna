# Is participation entailed by `source`?

**A final upstream test before the abstract family-declaration contract is settled.** Claude, at Huayin's
direction, 2026-09-25. **No implementation, serialization, schema work or migration.**

## Verdict

> **`source × scope` survives. Participation is entailed by `source`, and no third factor is needed.**
>
> **No pair of lawful clauses was found with the same resolved source and scope but different governed
> participation.** Every apparent pair differed in the source — in eligibility, in an operand binding, in a law
> parameter, or in a co-participation rule.

**Participation is authored in exactly two places, and both are inside `source`:**

| | where | what it fixes |
|---|---|---|
| **1** | the **world** source's `eligibility` | which points the quantity applies to |
| **2** | a **law** source's **co-participation rule**, where there is more than one operand | whose population governs the result |

**A composition clause authors neither.** Its participation is **inherited** from the operand's grounding. That is
the tightening this exercise produced: **most clauses do not author participation at all.**

One case came close to breaking it — §4, `LAST` over supported observations — and its resolution is the most
useful thing in this report.

---

## 1. The vocabulary, checked against authority rather than accepted

Huayin's four-way reading is **faithful, with one correction**.

| term | authority | verdict |
|---|---|---|
| **geometric fiber** \(\pi^{-1}(a)\) | CC v1.0 §5.1 — *"the source fiber is \(\operatorname{Fib}_q(a')=\{a\in\operatorname{Pts}(A)\mid q(a)=a'\}\)… **the formal object is the preimage of the grouping map**"* | ✅ exactly as stated. No eligibility, support or participation qualifier |
| **participating domain** \(D\subseteq I\) | ToD §4.2 — *"**Participation is selected by the law and the resolved request**; it is not automatically the set of surviving physical records or supported operand values"*; §6.1, §8.2, §11.5 preamble | ✅ semantic, and explicitly not evidential |
| **contributing fiber** \(D_A(a)=D\cap\pi^{-1}(a)\) | ToD §6.1, verbatim | ✅ **derived, and never independently declared** — ToD introduces it inside a supposition, not as an authored object |
| **support** | ToD §2.3 \(S_{F,A}\subseteq E_{F,A}\); §11.5.2 *"**The law cannot silently replace an intended eligible domain with the supported observations simply to obtain a denominator**"* | ⚠️ **correction below** |

> ⚠ **The one correction: "support is then separate evidence/realization state" is faithful to ToD and only
> *half* faithful to Contract Calculus.** In CC, \(S\) is **inside the contract** \(C_1=(X,U,A,E,S,\beta,\gamma)\)
> and **inside the fold's embedding** — §15.4's three-way case-split sends \(E\setminus S\) to \((0_\kappa,1,0)\) and
> carries the counts *through* the reduction. **Support is separate from *participation*, but it is not
> downstream of the reduction; it is carried by it.** What is downstream is the *decision* — §15.5's
> \(\operatorname{Covered}_h\), and its refusal to define a value outside \(S'_{q,h}\).
>
> **The distinction that actually matters survives intact:** support never selects the population. It is carried,
> counted, and finalized separately.

**And the two unreconciled formalisations recorded previously still stand:** CC is **index-total,
embedding-partial** (fold over \(\operatorname{Fib}\cap P\), case-split embedding); ToD §6.1 is **index-partial**
(fold over \(D\cap\pi^{-1}(a)\)). Both published. Neither uses "participating fiber" in the sense we had adopted.

---

## 2. Revenue — four readings, four different sources

| reading | what it is | differs in |
|---|---|---|
| **(a)** revenue over every eligible sale | the base family. Participation **= eligibility**, which for a grounding clause is *"which points the quantity applies to"* | — |
| **(b)** revenue over only revenue-bearing sales | a **value predicate**. By the frozen A.12 criterion it is **not a coordinate pin**, so it does not denote a point of (a); it must be **constituted** — which makes it (d) — or refused with `Clarify` | — |
| **(c)** revenue over sales satisfying a value predicate | **the same as (b).** There is no third thing here | — |
| **(d)** revenue over a governed classification (channel, customer class) | **two lawful spellings, and they are different acts**: a **coordinate pin** `revenue @ {channel=web, …}` — *the same family at a location*; or a **restricted grounding** `observes … for "web-channel sales"` — **a different family** | (pin) nothing; (restricted) **eligibility, inside the world source** |

> **Participation for a world source is eligibility**, and eligibility is a component of that source. For a
> grounding clause there is no fiber to reduce, so *"which contributions the law consumes"* and *"which points the
> quantity applies to"* coincide. **No separate participation fact exists to author.**

---

## 3. MEAN — the denominator problem, and COUNT which settles it

**Can the same resolved MEAN source and scope lawfully mean three different things?**

| candidate denominator | verdict |
|---|---|
| all **eligible** \(I\) points | **lawful** — `mean` whose basis binds `count(I)` |
| **participating** \(I\) points | **the same thing**, for a single-operand MEAN: participation is the operand's own, inherited from its grounding. These coincide unless a law parameter separates them (§3.1) |
| **supported observations only** | **lawful only as a different construction**, never as a re-reading of the same source |

**COUNT is what settles it, and ToD states it as a source difference in so many words.** §11.5.1:

> *"`count(I)` counts **participating analytical points of anchor \(I\)**, each contributing one. `count(x@I)`
> counts **participation under the operand construction's governed rule**. **These are distinct targets.**… 100
> governed Order points and 97 supported Revenue observations give `count(order) = 100` and `count(revenue@order)
> = 97`… **That does not authorize replacing an intended 100-order MEAN with a 97-observation MEAN.**"*

> ⚡ **So Huayin's question 3 answers itself in the affirmative.** *"Participation **under the operand
> construction's governed rule**"* says the participation fact **belongs to the operand**, not to the counting
> clause and not to a free-floating governed fact. The 100-versus-97 distinction is a **different operand
> binding** — `count(I)` versus `count(x@I)` — and an operand binding is **part of the resolved source**.
>
> **It does not presuppose an independently governed participation fact. It locates the fact in the operand.**

In the declaration model this is already literal: `count(I)` is `CARDINALITY of ( <a family grounded "one per
point of I"> )`, exactly the `order_count` family written for AOV; `count(x@I)` binds `x` instead. **Two bindings,
two sources, two quantities.**

### 3.1 The one way MEAN's participation can differ from its operand's

A **trimmed** mean drops a governed fraction of the extremes. That is either a distinct catalogued law or
`MEAN[trim = 0.05]` — **an identity-bearing law parameter**, and `trim = 0` and `trim = 0.05` are different
quantities, not different estimates of one. **Either way it is inside the source.** A mean *"excluding outliers"*
where "outlier" is a value predicate is **§2(b)** again: constitute the classification, or `Clarify`.

---

## 4. Multi-input / AOV — the strongest challenge, decided semantically

Two AOV clauses: same law `RATIO`, same operands `revenue` and `order_count`, same anchors, same scope, same
universe, same value type — **differing only in `co-participating: intersection` versus `denominator`**. Both
lawful; the in-transit-delivery case shows they are **different quantities**.

**So co-participation is not determined by the law, and not by the operands.** Is it (i) a law parameter inside
`source`, (ii) a separate authored family fact, or (iii) proof that `source × scope` is insufficient?

### 4.1 The semantic argument, not a field-placement preference

Semantically, co-participation is a function

\[
D_{\text{result}} \;=\; \Phi\bigl(D_1,\dots,D_n\bigr),
\]

**a rule for combining the operands' participating domains.** The question is whether \(\Phi\) belongs on the
`source` axis or is a third axis. **The deciding test is whether \(\Phi\) can depend on the target.**

> **It cannot — and the frozen contract already forbids it.** Suppose \(\Phi\) varied with \(A\): intersection at
> day, denominator-governed at week. Then at any anchor where both readings apply the family would take two
> values, **violating the coherence condition** — a family must be a function. So **\(\Phi\) is necessarily
> target-independent.**
>
> **And `scope` is exactly the target-dependent factor.** So \(\Phi\) and `scope` are **orthogonal by
> construction**, and \(\Phi\) cannot be a refinement of scope or a third factor alongside it. It belongs with the
> thing that fixes *which contributions are consumed*, which is `source`.

That is the non-circular form of the claim: **`source` fixes the contributions; `scope` fixes the locations;
\(\Phi\) demonstrably fixes contributions and demonstrably cannot fix locations.**

### 4.2 And the corpus places it the same way

Contract Calculus's `MAP1` puts \(E'=\bigcap_i E_i\) and \(S'=\bigcap_i S_i\) **in the rule's conclusion** —
\(\Phi\) is part of the *formation rule*, not a side condition on it. MA v1.0 §6: *"**Participation is part of the
analytical operation** and must be declared or derived under law. It is not selected by backend join behavior"*,
and *"This is one conservative, proved formation law… Other participation laws may be added explicitly."*

> **Verdict: (i).** A co-participation rule is a **law-application parameter**, identity-bearing, part of the
> resolved source — **and it is the second and last place participation is authored.**

---

## 5. The case that nearly broke it — `LAST` over supported observations

**ToD §9.3, which reads at first like an explicit counterexample:**

> *"If the selected eligible point's value is unsupported, **ordinary LAST over eligible points cannot retreat to
> the previous supported value. LAST over supported observations has a different participation rule.**"*

Same law, same order parameter, same operand, same scope, same universe, same type — **and ToD itself says the
participation rule differs.** If both were lawful families, `source × scope` would be **incomplete**.

**They are not both lawful families.** Apply the frozen evidence test:

> *If the value can change while the world, the declaration and the request all stay fixed, the population is
> support-based and the thing is not a quantity.*

Load the missing Sunday value and *"LAST over supported observations"* moves from Wednesday's answer to Sunday's,
with nothing in the world, the declaration or the request having changed. **It is not a quantity.** And the
representational proof from the same review applies: a clause's scope must be decidable from governed geometry
alone, so **there is no scope that denotes it** — it cannot be written.

**So §9.3 is a prohibition on conflation, not an admission of a second family.** Read in context it says: *do not
let ordinary LAST silently retreat*, because that silently swaps the participation rule.

### 5.1 But the business need is real, and the corpus already says where it goes

Stale-price carry-forward is a genuine governed practice. ToD §8.3 names the route:

> *"A known-empty fiber can have an established empty witness without an eligible scalar LAST value… **A separate
> completion or alternative result type must be declared** if another empty-result behavior is intended."*

> ⚡ **The distinction, and it is the sharpest thing in this report:**
>
> | | what it does | is it a quantity? |
> |---|---|---|
> | **participate over support** | **lets the data choose the population** | **no** — the value moves when data arrives |
> | **a declared completion** | **says deterministically what to do** when the eligible winner is unsupported — *carry the last observed value forward, up to \(N\) days* | **yes** — the rule is authored, the answer is fixed by world + declaration |
>
> A completion **changes what is produced**, so by the frozen premise rule it is a **law application** and must be
> its own family. **Its parameters — which completion, what bound — are identity-bearing and sit in `source`.**
>
> **So the pair is: (i) ordinary LAST, participation inherited from the operand, → `want_of_state` when the
> winner is unsupported; (ii) a completed LAST, a different family with a different source. The third option,
> "participate over whatever happens to be supported," is not admissible at all.**

**No counterexample. And this is the case that would have produced one**, had the evidence test not already been
frozen.

---

## 6. Empty and unsupported — five states, and a sixth the algebra cannot represent

| | state | in \(D\)? | in \(S\)? | CC §15.4 embedding | outcome |
|---|---|---|---|---|---|
| 1 | **no participating contributions** | \(D_A(a)=\varnothing\), **and established so** | — | nothing to fold | monoid → identity; **semigroup → no value** (MIN/MAX). ToD §6.1: *"not a substitute for an unknown domain"* |
| 2 | **participating, value zero** | ✅ | ✅ | \((\eta(0),1,1)\) | an ordinary established value |
| 3 | **participating, unsupported** | ✅ | ❌ | \((0_\kappa,1,0)\) | counted in \(e\) not \(o\); **no value outside \(S'_{q,h}\)** (CC §15.5); *"must not be replaced by the identity"* (ToD §6.1) |
| 4 | **ineligible point** | ❌ | ❌ | \((0_\kappa,0,0)\) | not counted at all |
| 5 | **unresolved existence / eligibility** | **unknown** | unknown | **no case applies** | see below |

> ⚠ **State 5 has no home in Contract Calculus.** ToD §2.3: *"**Eligibility may be unresolved rather than
> established or denied.** These are dependencies to preserve, not instructions to create one universal standing
> enum."* But CC §14.2's taxonomy is **four** states — \(a\notin P\), \(a\in P\setminus E\), \(a\in E\setminus S\),
> \(a\in S\) — and §15.4's embedding is **total on \(P\)**, so it must know which of the three cases holds.
> **An unresolved point cannot be embedded.**
>
> **And it is genuinely different from state 3.** In 3 we know the point participates and lack its value; in 5 we
> do not know whether it participates — so **\(D\) itself is unknown, which is not the same as \(D\) being
> empty**, and neither the value nor the coverage count is established. **ToD has five states; CC has four.**
>
> **This does not affect participation-from-source** — it is evidence *about* eligibility, not an authoring
> question — but it is a real gap between the two papers, and it is the second such gap this exercise has found.

---

## 7. Why no third factor is needed — the closure argument

\(D\) has exactly four inputs, and each is already placed:

| input to \(D\) | comes from | in the clause? |
|---|---|---|
| existing points, sparsity | **the universe** | no — and correctly so |
| eligibility | the **world source** | **yes — inside `source`** |
| the law's participation rule, incl. \(\Phi\) | the **law source**: cited law · parameters · operand bindings · co-participation | **yes — inside `source`** |
| a restriction in the resolved target | the **request** — a coordinate pin (same family) or a constituted classification (new source) | no — and A.12 keeps it out |

**Residual candidates tested and closed:**

- **expansion multiplicity** — after `replicate`, contributions ≠ points. But the disposition is a **law**
  (`expand_χ`), a separate construction with *"multiplicity governed separately"* (MA §2.5). **In source, and a
  third independent corroboration of Amendment 1.**
- **a value-dependent population** — §2(b): constitute a classification, or `Clarify`.
- **support** — §5: not admissible as a population; the need it answers is a **completion**, which is a law.

> **The list is closed. Participation is entailed by `source`.**

---

## 8. What this changes

**Nothing in the frozen model.** No field is added; no factor is added.

**Two things are tightened, and both should be recorded:**

1. **Participation is authored in exactly two places** — a world source's `eligibility`, and a multi-operand law
   source's co-participation rule. **A composition clause authors none**, inheriting from its operand's grounding.
2. **The orthogonality argument for co-participation** (§4.1) replaces what was previously a placement assertion:
   \(\Phi\) must be target-independent on pain of violating coherence, and `scope` is the target-dependent
   factor — so they cannot be the same kind of thing.

**Still pending, unaffected:** the three LAST/SUM decisions (composition closure; clause-incoherence versus
path-disagreement; whether rectangularity is universe-declarable, now with the request-dependence refinement).

**Newly recorded for the reconciliation pile:** ToD's five absence states versus CC's four (§6), joining CC's
index-total/embedding-partial versus ToD's index-partial (§1), and ToD's \(D\)-as-declared versus
\(D\)-as-used-in-the-proofs.

---

**Stopped at the report.**

> **Note.** Huayin's message ended mid-sentence in case 5 (*"Check that"*). The five states are worked above
> against both authorities; **if the sentence continued to a further check, it has not been seen.**

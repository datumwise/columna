# Candidate entry A.6 for the v7.2 development journal — family continuation is not family formation

**Standing.** A **candidate entry**, drafted by Claude at Huayin's direction, 2026-09-24, for adjudication into
`tod_v7_2_development_addendum_v0_1.md`. It is written in that document's form. **It is not adopted, carries no
authority, and is deliberately filed separately rather than edited into an authored document.**

**Why it is recorded.** Huayin supplied a single business example that explains, more compactly than the
archaeology did, what the inherited prohibition model was actually getting wrong. A.3 recovered the *identity*
half of the answer from Version 6.1 (*different analytical directions produce distinct family identities*). This
entry records the *structural* half: the prohibition model conflated two different questions and then indexed the
conflation on the wrong thing. The example is worked in full as case 17 of
`manifold_semantic_starting_point_v0_5.md`.

---

## A.6.1 Subject

A business explicitly defines

> `balance @ week` = *"balance at the last day of the week."*

Version 7.1 has no difficulty with the sentence, but it has no place to put it. The sentence is not a query, not a
construction, and not a permission: it is **a statement about how Balance itself is determined**, alongside the
statement that Balance is determined at a day by observation and summed across accounts. It is a second
determination clause of the Balance family.

The moment it is admitted, three expressions that the estate has always treated as competing turn out to be
simply **different, and simultaneously true**:

| expression | what it is |
|---|---|
| `balance @ week` | **Balance itself**, determined at Week by Balance's own LAST clause |
| `mean(balance @ day) @ week` | a **different family** — the mean daily balance over the week |
| `sum(balance @ day) @ week` | a **different family** — the additive total of daily balances |
| `last(balance @ day) @ week` | a **different family**, which **agrees in value** with the first and may be canonicalized to it |

## A.6.2 The principle

> **A family's determination clauses govern how *that family* is determined. They do not license, and cannot
> prohibit, that family's measures serving as operands of other lawful family-forming constructions.**

Two questions, answered at different places and indexed on different things:

| question | answered by | indexed on |
|---|---|---|
| **continuation** — is \(F\) itself determined at \(A\)? | \(F\)'s own determination clauses | the family |
| **formation** — is \(g(F@I)@A\) a lawful family? | \(g\)'s law, over measures of \(F\) at \(I\) | the construction |

Formation asks exactly one thing of \(F\): **that \(F@I\) be determined.** It does not ask which clause
determined it, and a family declaration contains **no term ranging over constructions**, so it cannot ask what
clauses \(F\) lacks.

## A.6.3 What the prohibition model was conflating

A temporal block on Balance's `day` axis asserts two propositions at once:

1. **Balance itself does not continue through time by SUM.**
2. **SUM may not consume Balance values across time.**

**The first is true. The second is false.** `sum(balance @ day) @ week` denotes a perfectly definite quantity —
and at `inventory` it is a standard financial one with its own name, integrated stock exposure, which Contract
Calculus names itself (case 16). The block cannot tell the two apart because it is attached to the family and
quantified over an axis, and neither of those is the index of the false proposition.

**A.3 established that the old mechanism had the wrong *label*.** This entry adds: **it also had the wrong
*index*, and that is the deeper error**, because a correct label on an axis-indexed set would still have been
unable to express the business's own declaration.

## A.6.4 Why the example is a constructive refutation and not a counterexample

After the business's declaration, Balance says **two different things about the same axis `day`**:

* determined across `day` **under LAST**;
* **silent** across `day` under SUM — not barred, simply unclaimed.

**A set of blocked axes cannot hold two verdicts about one axis.** To express the declaration at all, `BLOCKED`
would have to be re-indexed by **law as well as axis**. At that point:

* it is \(\beta:\mathsf{AggCap}\to\mathcal P(\mathsf{Axis})\), which is **capability-indexed by definition** and
  **must never be imported family-indexed**; and
* it is the positive clause list **with its sign flipped, and strictly worse** — the negative form must be
  **complete over every law** to mean anything, while the positive form is open and states only what the author
  actually knows.

**The mechanism cannot be repaired into something that expresses the case. Retiring it is not a simplification;
it is the only way to say what the business said.**

## A.6.5 Three monotonicity claims the principle owes

| | claim |
|---|---|
| **extension-monotone** | adding a clause to \(F\) can only **add** anchors at which \(F\) is determined; no value already determined changes |
| **downstream-inert** | adding a clause to \(F\) changes **nothing** about the identity, law, extension or meaning of any construction over \(F\)'s existing measures |
| **upstream-consequential** | it **does** change \(\Sigma(F)\) — a clause is identity-bearing (§3.9). The change lands on \(F\) and stops there |

The second is the one Huayin named as important, and it is the reason the first is safe: **a business may answer
one more question about Balance without silently redefining every analysis built on Balance.** The third is the
counterintuitive one: **Balance's own definition changed while nothing built on Balance did.**

## A.6.6 Canonical equivalence, in three claims that must not be merged

1. **Value agreement is ENTAILED and conditional** — on the cited law, its identity-bearing parameters (**the
   order**), the operand anchor, eligibility and the known-empty outcome, and the value type. Under a different
   order there is no equivalence at all.
2. **Canonicalization is AUTHORED, at the naming layer** — §11.5.1, the same mechanism as
   `sum(revenue @ line) ≡ revenue`, and no other is needed. Generalized: **a construction that restates one of
   \(F\)'s own clauses, at an anchor inside that clause's scope, with matching parameters, is canonically
   \(F\).**
3. **Identity is not minted.** \(W = last(balance@day)\) remains its own family; downstream lineage naming \(W\)
   is untouched. And the equivalence may **never** be inferred from extensional coincidence: agreement on every
   servable value is evidence, not a governed equivalence. A system that mints equivalences from agreeing data is
   constituting from evidence.

## A.6.7 The auditable form

The principle is worth stating negatively, because that is the form in which it can be checked against any
downstream proposal:

> **A check that consults \(\mathcal A_F\), an edge-validity fact about \(F\), or \(F\)'s clause list, while
> deciding a construction over \(F\)'s measures, is the defect — under whatever name it travels.**

Three live places where it would appear:

* **a per-family admitted-anchor list** checked against the **request** anchor. For `g(F@I)@A`, family standing is
  checked on **\(F@I\)**; \(A\) is checked against **\(g\)'s** clause. Never \(A\) against \(\mathcal A_F\).
* **\(\beta'\)-style propagation** from operand to result — `sum(balance@day)` inheriting Balance's blocked `day`
  axis and refusing at week. The leak in Measure Algebra's own vocabulary.
* **an operand rule phrased over the operand's clause kind.** The working record itself contained one: *"MEAN
  consumes Balance at singleton fibers of its grounding clause — never its composition clause"* — a true
  observation about a Balance that has no reaching composition clause, mis-stated as a rule. It is repaired at
  case 6. **The example found a real defect in the model that was written to accommodate it**, which is the best
  argument for keeping it as a standing acceptance case.

## A.6.8 Open, and not decided here

* **Is a purely extension-widening clause addition a §3.9 succession, or a refinement?** \(\Sigma(F)\) changes
  and no determined value does. This is the strongest case in the corpus for a definitional change that does not
  succeed. **Orthogonal to downstream inertness, which holds either way.**
* **A fiber varying in the scopes of two different clauses.** SUM over account-varying fibers and LAST over
  day-varying ones do not compose to `balance @ {week}`, and do not commute in general, since the last observed
  day can differ across accounts. The conservative reading is *undetermined until a clause covers it*. Whether a
  **commutation obligation** could entail it instead is open. **It must not be resolved by widening a scope.**

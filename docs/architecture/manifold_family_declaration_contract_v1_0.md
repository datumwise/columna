# The abstract Manifold family-declaration contract

**Claude, at Huayin's direction, 2026-09-24.** Derived from the **frozen** semantic declaration model.

**Standing.** Design record, **semantic only**. **No serialization, no YAML or JSON, no publication fields, no
schema versions, no migration, no compatibility machinery, no implementation.** Nothing below chooses a concrete
syntax; the notation is mathematical, and where a symbol is used it is used to make a claim, not to propose a
field name.

**The frozen model this makes precise:**

> **A family is a name bound to determination clauses.**
> **A determination clause is `source × scope`.**

**Carried into the freeze:**

- **R1′ — single authority.** A derived fact gets its authority from entailment; restating it does not create
  another authority.
- **R1″ — identity over resolved semantics.** Declarations resolving to the same semantic constitution identify
  the same family regardless of redundant spelling.
- **Amendment 1.** Contribution multiplicity is **retired as a primitive family fact**. If multiplicity is
  governed, the index over which it exists must itself be governed — which is individuation, or another governed
  construction.
- **Amendment 2.** A **coordinate pin** selects governed analytical points without introducing a new population.
  A **value predicate** may instead define a different participating population, and **cannot acquire
  constitutive authority merely because request syntax can express it.** Qualified, not universal — §8.4.

## Verdict, first

> **`source × scope` survives.** No source kind was added, no third factor was needed, and no field was added to
> the clause.

**No contradiction was found.** One genuinely missing piece of **derived vocabulary** was found — §5 — and it
closes a latent gap between two claims the contract makes side by side. One **new required condition** was found
— §4.4 — and it is the positive successor to the only legitimate work the B-anchor was ever doing.

---

## 1. The signature

```
Family        F   ::=  Name  ↦  Clauses(F)              a finite set of clauses; unordered
Clause        c   ::=  ⟨ source(c) , scope(c) ⟩
```

Everything else in this document is either a definition over that signature, a condition on it, or a consequence
of it.

---

## 2. Source

### 2.1 Two kinds, and why there is no third

```
source  ::=  world⟨ universe , anchor , grounding , type , eligibility ⟩
          |  law⟨ law-ref , parameters , operands ⟩
```

**The closure argument, rather than an assertion.** A determination either **appeals to something outside the
formal system** — the world — or **derives from something inside it** — a law applied to measures. There is no
third place a value can come from. Every apparent third kind is one of four other acts:

| apparent third source | what it actually is |
|---|---|
| a governed constant (a published tax rate, a policy threshold) | **world**, grounded at a coarse anchor. It *is* an observation — of a governed artifact |
| a hand-maintained override or adjustment table | **world.** Uncomfortable, and correct: someone is asserting what is the case |
| an alias for another family | **naming** — no clause, no source |
| a cross-universe reference | **world or law**, plus a **governed passage**, which is a universe fact. Anchor identity is universe-relative |
| an imputation or default-filling rule | **law** — and one that changes what is produced, so it constitutes **its own family** |
| a materialized cache or pre-aggregate | **realization** — not a source at all |

**No source kind was added to accommodate an implementation object**, and the list above is how each candidate was
turned away.

### 2.2 The world source

```
world⟨ universe , anchor , grounding , type , eligibility ⟩
```

| component | what it is |
|---|---|
| `universe` | a governed world reference, **by identity** |
| `anchor` | a governed anchor **of that universe** |
| `grounding` | the **identity-bearing handle** on what quantity exists at a point. Opaque; §5.2 notes it is the one non-normalizable identity input |
| `type` | a governed value-type reference, with any authored type parameters |
| `eligibility` | a restriction of the universe's existence predicate, **ranging over eligible points, never observed ones**. Absent ⇒ the universe's own predicate |

**No multiplicity component** (Amendment 1). A world clause determines **one value at one eligible point**, and
if the world puts more than one there, the index distinguishing them is either governed — in which case
individuate it — or not governed, in which case it is not countable and the coincidence is a realization fact.

### 2.3 The law source

```
law⟨ law-ref , parameters , operands ⟩
operands  ::=  { role ↦ ⟨ family , locus ⟩ }
locus     ::=  at(I)          -- a governed anchor: the fine end of the fiber
            |  colocated      -- the clause's own target location
```

| component | what it is |
|---|---|
| `law-ref` | a reference to the universal law catalogue. **The catalogue supplies the law's argument shape and its operand roles**; neither is authored |
| `parameters` | the law's **identity-bearing** parameters. Two sub-kinds, both identity-bearing: **convention** parameters (`ddof`, a quantile convention) and **governed-reference** parameters (the order LAST uses, a conversion's rate source) |
| `operands` | role-indexed bindings. `colocated` exactly when the law is a mapper; `at(I)` exactly when it is a reducer |
| co-participation | which operand's population governs, where there is more than one: `intersection ǀ ⟨role⟩`. **A property of how the operands are bound, therefore part of `source` — not a third factor** |

**A composition** is the case where the bound family is the clause's own family. It is not a separate source
kind; it is self-reference, and §4.2 gives the condition that keeps it well-founded.

---

## 3. Scope

### 3.1 What it is

> **`scope(c)` is a predicate on a governed projection.**
>
> For a reducer clause with operand locus `at(I)`: `scope(c)(I ⪰ A)` — *does this clause determine the family at
> `A` by reducing the `I`-fiber below it?*
> For a mapper clause: the projection is the identity, and scope is the constant predicate at every location
> where the operands are co-established.

Its content is a condition on **the forgotten set** — the constituents `I` has and `A` does not — plus, where a
case requires it, a geometric qualifier such as order-contiguity.

```
over { account }   ≡   forgotten(I ⪰ A) ⊆ { account }
over *             ≡   no condition on the forgotten set
```

### 3.2 A predicate, not a stored set — and the six tests it must pass

**It is a predicate**, and the argument is not aesthetic:

1. **The governed lattice is open.** New placements and projections may be added to a universe. A predicate
   remains correct across that; **a stored set silently goes stale** — the same non-monotonicity that sank R1's
   strong form.
2. **A stored set can disagree with the geometry**, so by the converse test it is storing a consequence.
3. **A predicate is what the necessity test actually vindicated.** Revenue and Balance differ in `over *` versus
   `over { account }` — a difference of *condition*, which no enumeration of anchors states as compactly or as
   stably.

**And it must not quietly become something else.** Six invariance tests, each decidable:

| scope must not be | the test |
|---|---|
| an enumerated \(\mathcal A_F\) | scope is **per clause**; the extension is **per family** and is a union over clauses. §3.3 |
| a B-anchor | scope is **positive and per-clause**. Two clauses may carry different conditions over the same constituent with no conflict — Balance's `over { account }` and `over { day }`. A B-anchor cannot hold two verdicts about one axis |
| \(P_F\) | **the add-a-clause test:** under scope, adding a clause **grows** the family's extension. Under \(P_F\), adding a clause grows nothing — you would have to *shrink a prohibition set*, a different edit at a different index |
| an execution capability | **scope's truth value must be invariant under changing the execution engine** |
| an evidence predicate | **scope's truth value must be invariant under changing which data is loaded.** This is the same test that excludes support-based populations |
| a serving policy | scope may not mention governance; its vocabulary is geometric |

### 3.3 The firewall: scope is per-clause, the extension is per-family

This is where \(\mathcal A_F\) would creep back in, so it is stated as a definition and a warning.

```
determines(F, A)   ⟺   ∃ c ∈ Clauses(F) . applies(c, A)
𝒜_F                =   { A : determines(F, A) }          -- NOTATION. Derived. Never authored, never stored
```

**Scope is authored; the extension is computed.** They have different arities (a clause versus a family),
different types (a predicate on projections versus a set of locations) and different modality (a claim versus a
consequence). **Conflating them is exactly the \(\mathcal A_F\) error**, and the giveaway that it has happened is
that something starts *consulting* the extension where it should be evaluating a scope.

---

## 4. Determination and clause resolution

### 4.1 The resolution function

```
applies(c, A)  ⟺  scope(c)(I_c ⪰ A)                                  -- geometry
                ∧  ∀ (role ↦ ⟨H, ℓ⟩) ∈ operands(c) . determines(H, locus(ℓ, A))
                                                                      -- operand determinacy

determines(F, A)  ⟺  ∃ c ∈ Clauses(F) . applies(c, A)
```

> ⚡ **Read the recursive call.** It is `determines(H, J)` — **a boolean at one location.** Nothing in this
> definition can reach `Clauses(H)` except through that boolean. **The continuation/formation separation is a
> property of the resolution function's signature, not a rule anyone applies.**

### 4.2 Well-foundedness

A composition clause binds its own family, so `determines` is recursive at the same family. It terminates
because **every clause's operand locus strictly refines its target** (a reducer) **or equals it with a different
family** (a mapper), and the refinement order is well-founded.

> **Condition (groundedness).** Every location at which `F` is determined must have a derivation bottoming out at
> a clause whose source is `world`, or whose operands are families other than `F`. A family whose clauses are all
> self-compositions determines nothing anywhere — **it has an empty extension, which is a consequence, not an
> error.** A surface may choose to warn; the semantics does not need to.

### 4.3 The four cases

Let `App(F, A) = { c ∈ Clauses(F) : applies(c, A) }`.

| | case | what it is | disposition |
|---|---|---|---|
| **0** | `App = ∅` | **not determined.** Distinguish the prior failure: if no governed projection reaches `A` at all, the failure is **geometry**; if the geometry exists and no clause claims it, **`want_of_law`** | §8 |
| **1** | `‖App‖ = 1` | determined | serve |
| **2** | `‖App‖ > 1`, all **co-determining by construction** | **redundancy, not error** — §4.3.1 | normalize; serve |
| **3** | `‖App‖ > 1`, determinations **genuinely differ** | **splits three ways** — §4.3.2 | see below |

#### 4.3.1 Case 2 — co-determining by construction

Two clauses **co-determine by construction** when their resolved derivations at `A` are **identical** — same law,
same identity-bearing parameters, same operand derivations, same scope instance.

This is R1″ at the clause level: **redundant spelling does not make two determinations.** It arises from
subsumption (`SUM over *` alongside `SUM over { account }`) and from restatement. **Normalize and proceed.**

> ⚠ **Value agreement is not co-determination.** `MAX` and `LAST` over a series that happens to be monotone agree
> on every current value and are **different determinations**. Case 2 is a statement about derivations, not about
> data — otherwise evidence would be deciding identity.

#### 4.3.2 Case 3 — genuinely different determinations

**Not automatically malformed**, and the existing theory already distinguishes three things here. The
discriminator is **whether the disagreement is decidable before data**.

| | condition | what it is | where it belongs |
|---|---|---|---|
| **3a** | the derivations differ but **provably agree in every admissible world** | a **redundant derivation**; the second is a free consistency check | fine. Normalize to either; keep both as a check |
| **3b** | they **may** disagree, and which is right is an **evidence** question — two independent observations of one quantity; a reported total alongside a line-level sum | **legitimate alternative derivation carrying an agreement obligation** — the contract's §2.4 case | **fine at constitution.** Disagreement is an *evidence* disposition: reconcile, Disclose, or `want_of_state` — **never a constitution defect** |
| **3c** | they **provably disagree** in some admissible world — `LAST over { day }` alongside `SUM over { day }` | **the declaration does not determine a quantity.** A family is functional; this is not | **a declaration-time refusal** — §8.1 |

> **3c is not `Clarify`.** `Clarify` is a **request** disposition: the asker's question admitted several lawful
> readings. In 3c the request `balance @ week` is perfectly unambiguous and it is **the declaration** that has no
> answer. **Ambiguity lives in the request; incoherence lives in the declaration**, and they are addressed to
> different people.

### 4.4 The coherence condition — and what it quietly replaces

> **Coherence.** For every `A` and every pair `c, c′ ∈ App(F, A)`, the two must not provably disagree.
> Equivalently: **`F` must be a function.**

This is a **new required condition**, and it is required by nothing more exotic than *a quantity has one value
where it has a value*.

> ⚡ **It is also the positive successor to the only legitimate work the B-anchor ever did.** The B-anchor's real
> worry was *"do not let SUM produce a thing called Balance at week."* Coherence delivers it, without a
> prohibition:
>
> - declare `LAST over { day }` **and** `SUM over { day }` → they provably disagree → **refused, at declaration
>   time**, because Balance would not be a function;
> - declare **only** `SUM over { day }` → coherent. Balance is then additive over time, which is an unusual
>   business but a perfectly well-formed one, **and it is not our place to forbid it**;
> - declare **neither** → `balance @ week` is `want_of_law`, which is the contract's case 6.
>
> **The prohibition was never needed. Functionality was.**

---

## 5. Identity

### 5.1 Two notions, because one was doing two jobs

> **`identity(F)` — the family.** The normalized resolved clause set. This is what changes when a business says
> one more thing about what Balance *is*.

> **`identity_at(F, A)` — the determination.** The normalized derivation term for `F @ A`:
>
> ```
> identity_at(F, A)  =  for the clause c determining F@A —
>     world : ⟨ world , universe-id , anchor-id , grounding-handle , type-ref , eligibility ⟩
>     law   : ⟨ law-id , parameters , scope-instance(I ⪰ A) ,
>               { role ↦ identity_at(H, J) } , co-participation ⟩
> ```
>
> Well-founded by §4.2.

**Read what is absent from `identity_at`: the family's name, and the family's other clauses.**

> **An operand binding contributes `identity_at` of the operand, never `identity` of the operand family.**

### 5.2 The accounting

| | is it an identity input? |
|---|---|
| **authored spelling** — whitespace, clause order, redundant-but-agreeing statements, an alias used to reach a governed object | **no** (R1″) |
| **resolved source kind, law and identity-bearing parameters** | **yes** |
| **constitutive operand anchors** — `mean(balance@day)` ≠ `mean(balance@week)` | **yes** |
| **operand roles**, where the law is asymmetric | **yes** |
| **governed world references** — universe, anchor, order, placement, conversion — **by identity, not by name** | **yes** |
| **scope**, in normalized form | **yes** — Revenue and Balance differ here and in the grounding |
| **the grounding handle** | **yes** — and it is the **one non-normalizable identity input**, so a textual edit is conservatively a re-ratification. The known, located cost |
| **eligibility**, resolved | **yes** |
| **the family's name and aliases** | **no** — naming. **You cannot mint a quantity by renaming one** |
| **extension \(\mathcal A_F\)** | **no** — a consequence |
| **empty-fiber outcome · sufficient-state basis · result value domain · lineage · observational-vs-constructed · argument shape** | **no** — consequences. *Identity-bearing* and *identity input* are different: a consequence can be identity-determining without being an input |
| **coverage · carriers · plans · precision · ratification · governance** | **no** — assurance, evidence, realization |

### 5.3 The latent gap this closes

The frozen contract asserts two things side by side:

> **upstream-consequential** — adding a clause changes \(\Sigma(F)\).
> **downstream-inert** — adding a clause changes nothing about the identity of any construction over `F`'s
> measures.

**With one notion of identity these are inconsistent**, because a construction's identity references its operand
family. The contract never said which way that reference goes, and the question had not been asked.

**With the split, both are theorems.**

> **Theorem (inertness).** Let `F′ = F` with one clause added. For any family `G` whose clauses bind `F` only at
> loci `I` where `identity_at(F, I) = identity_at(F′, I)`: **`identity_at(G, A)` is unchanged at every `A`,** and
> so is `determines(G, ·)`.
>
> *Proof.* `identity_at(G, A)` mentions `F` only through `identity_at(F, I)`, by the definition in §5.1. ∎
>
> **Corollary.** `identity(F) ≠ identity(F′)` while `identity(G)` is unchanged. **Balance's own definition
> changed and nothing built on Balance did** — and the criterion is exact: inertness holds **iff the added clause
> does not change how `F` is determined at the bound loci.** Add a *second grounding clause at the same anchor*
> and `identity_at(F, I)` does change, and `G`'s identity changes with it — **correctly**, because `G`'s operand
> really is a different thing.

**Classification: a derived notion the theory needed and lacked.** Not an authored fact, not a new source kind,
not a new field — **new vocabulary**, and the model does not grow.

### 5.4 Canonicalization becomes computable

Case 10's equivalence, restated exactly:

> `closing_balance ≡ balance` over a region `R` **⟺** `∀ A ∈ R . identity_at(closing_balance, A) = identity_at(balance, A)`,
> while `identity(closing_balance) ≠ identity(balance)`.

**The equality is entailed and checkable**, not asserted — so the `justified by` in the surface model is a check
the system can perform itself. **What remains authored is only which name is canonical.** That is the contract's
*value agreement entailed · canonicalization authored · identity not minted*, now with each of the three attached
to a distinct formal object.

---

## 6. Several clauses in one family — Balance, worked

> ⚠ **NOT YET FROZEN — see [`last_sum_interchange_verification_v0_1.md`](./last_sum_interchange_verification_v0_1.md).** The conclusion
> below (Balance is **one** family) is correct and unchanged. Two things are not: **(1)** this section is silent
> on the fact that `determines` in §4.1 is **existential over single clauses**, so it has **no composition
> rule** — which is the real reason `balance @ {week}` is undetermined here, prior to any question about
> commutation; **(2)** the reason given elsewhere for non-commutation (the last *observed* day) was wrong —
> governed LAST is `argmax` over the **participating** fiber, and the obstruction is **governed sparsity** of
> that domain (ToD §11.2). Three decisions pend: whether to close `determines` under clause composition, whether
> to add the **clause-incoherence versus path-disagreement** distinction it requires, and whether rectangularity
> of a participating domain is universe-declarable.

```
Clauses(balance) = {
  c₁  world⟨ ledger , {account,day} , "the amount standing at the close of the day" , Decimal , ⊥ ⟩
  c₂  law⟨ SUM  , {} , { ↦ ⟨balance, at({account,day})⟩ } ⟩   over { account }
  c₃  law⟨ LAST , {order: ledger.day.chronological} , { ↦ ⟨balance, at({account,day})⟩ } ⟩   over { day }
}
```

**Why this is one family, proved rather than asserted.** Apply §4.4. The clauses can collide only where their
scopes overlap:

| pair | overlap | verdict |
|---|---|---|
| `c₂ , c₃` | `forgotten ⊆ {account} ∧ forgotten ⊆ {day}` ⟹ `forgotten = ∅` — **the identity projection** | at a singleton fiber, `SUM` and `LAST` both return the one value. **Co-determining (case 2)** |
| `c₁ , c₂` and `c₁ , c₃` | only at `{account,day}` itself | same argument. **Co-determining** |

**Coherence holds, so Balance is a function, so it is one quantity with three ways of being determined.** A
fourth clause over a third dimension — `SUM over { branch }`, in a ledger that individuates branches — joins by
the same argument: every pairwise overlap collapses to the identity projection.

> **And the exact condition under which a new clause instead defines a different quantity:**
>
> > **A new clause `c` belongs to `F` iff, at every location where `c` and an existing clause both apply, they do
> > not provably disagree. Otherwise it is a different quantity and must be a different family.**
>
> `FIRST over { day }` added to the set above: it overlaps `c₃` wherever `forgotten ⊆ {day}`, and provably
> disagrees on any non-constant balance. **So it is not a clause of Balance — it is `opening_balance`.** The
> theory produces the split rather than the author asserting it.

---

## 7. Construction, structurally

Each is `identity_at` unfolded once. `G` is the constructed family; `B = identity_at(balance, {account,day})`,
the grounding derivation.

| expression | `identity_at(G, {account,week})` |
|---|---|
| `mean(balance@day)@week` | `⟨MEAN, {}, scope({account,day} ⪰ {account,week}), {↦ B}⟩` |
| `sum(balance@day)@week` | `⟨SUM, {}, …same scope…, {↦ B}⟩` |
| `last(balance@day)@week` | `⟨LAST, {order:O}, …same scope…, {↦ B}⟩` |
| nested — `mean(mean(balance@day)@week)@quarter` | `⟨MEAN, {}, scope({account,week} ⪰ {account,quarter}), {↦ identity_at(M₁, {account,week})}⟩`, and **the outer scope instance requires a governed `week ⪰ quarter`**: present under a 4-4-5 calendar, absent under ISO weeks. **Geometry, in the identity term itself** |
| AOV | `⟨RATIO, {}, identity-scope at A, {num ↦ identity_at(revenue, A), den ↦ identity_at(order_count, A)}, intersection⟩` |

**Now add `c₃` to Balance and recompute.** `identity_at(balance, {account,day})` is `c₁`'s derivation, and `c₃`
does not determine Balance at `{account,day}` — so `B` is unchanged, so **every row above is unchanged**, in
identity and in value. **By the definition in §5.1, not by a rule.**

Two further readings worth recording:

- **`last(balance@day)@week` and Balance's own `c₃` now have equal `identity_at` at every `{account,week}`.**
  That is §5.4's equivalence, **discovered rather than declared.**
- **AOV's identity at `{store,day,order}` references Revenue's *composition* derivation, not its grounding one** —
  because `identity_at(revenue, {store,day,order})` unfolds Revenue's `SUM` clause. That is correct and
  desirable: if Revenue's composition changed, AOV at that anchor really would be a different quantity. **A
  construction is sensitive to how its operand is determined *at the bound locus*, and to nothing else about the
  operand family.** That is the precise content of the separation, and it is neither weaker nor stronger than it
  should be.

---

## 8. Failure classification

### 8.1 Two tiers, which the contract half-saw

**Declaration-tier** — decidable when the declaration is made, **anchor-invariant**, addressed to the author:

| | failure |
|---|---|
| D1 | **incoherence** — §4.3.2(3c). The clause set is not a function |
| D2 | **law-to-type inadequacy** — the cited law's required capability does not exist on the type. *This is why it felt anchor-invariant: it is not a request failure at all* |
| D3 | **incomplete law** — a non-catalogued law cited without being supplied. **The declaration fails to constitute; it does not mint a family with an undecided domain** |
| D4 | **ungoverned reference** — a universe, anchor, order, placement or type reference that does not resolve |

**Request-tier** — decidable against a request, addressed to the asker or the operator:

| | failure | the earlier test that keeps it distinct |
|---|---|---|
| R1 | **no governed geometry** | no projection or placement reaches `A`; or the relationship yields a **cover, not a partition** |
| R2 | **`want_of_law`** | geometry exists; `App(F,A) = ∅` |
| R3 | **undefined result** | determined at the anchor, **undefined at a point**. Not disclosable |
| R4 | **`Clarify`** | several **identity-distinct** readings of the request. *Never* used for D1 |
| R5 | **`want_of_state`** | the meaning stands; the required argument or basis was not retained |
| R6 | **want of evidence / coverage** | a **lawful result with a required disclosure** — served, annotated |
| R7 | **realization unsupported** | no carrier or plan honours the clause's semantics |
| R8 | **withhold** | governance. Meaning and servability both fine |

### 8.2 The resolution order is part of the contract

> **D1–D4 · R1 · R2 · operand determinacy (recursively) · R3 · R5 · R6 · R7 · R8 — and the first failure wins.**

**The order is what prevents collapse into a generic admission concept.** Without it, a missing projection and an
absent clause both surface as *"cannot answer"*, and the remedies — a universe declaration versus a family
clause — are entirely different. Every disposition must name its tier and its kind.

### 8.3 Two collapses explicitly forbidden

- **R2 and R5.** *The meaning does not exist* and *the meaning exists and the evidence does not* are different
  facts about different objects. Returning R2 for a retention gap invites the author to "fix" the theory.
- **D1 and R4.** §4.3.2.

### 8.4 The qualification on Amendment 2

The coordinate-pin criterion is stated **for the cases tested and not as a universal Frame-QL theorem.** It holds
where the predicate ranges over a **governed constituent of a governed anchor**. It is **not yet established**
for: predicates over a *derived* constituent whose governance is itself in question; predicates that are
formation-sensitive, where the same surface predicate pins a coordinate for one clause and subsets a population
for another within one request; and contextual restrictions that interact with co-participation. **Those are
open, and the criterion should not be generalized ahead of them.**

---

## 9. Audit of the old constructs

| construct | status |
|---|---|
| **\(\mathcal A_F\)** | **reduced to derived notation.** `{ A : determines(F, A) }`. Never authored, never stored, **and not the same object as scope** (§3.3) |
| **\(P_F\)** | **eliminated.** Its work is split between **silence** (R2 of the declaration model) and the **coherence condition** (§4.4) |
| **family root / \(A_0\)** | **eliminated.** Every clause carries its own anchor reference; a family with two grounding clauses has no single root, and needs none |
| **C3 family-domain standing** | **eliminated.** The question it held is answered by `determines(F, A)`, which is computed, not stood upon |
| **\(\Gamma_F\) / movement** | **relocated** to the evidence jurisdiction, and narrowed: consulted for **ascriptions of `F` only**, never while deciding a construction over `F`'s measures |
| **B-anchor / `BLOCKED`** | **eliminated.** Its one legitimate concern is now the **coherence condition**, which is positive, per-location, and decidable before data (§4.4) |
| **`formation.kind`** | **reduced to derived notation** — the presence of a `world` clause |
| **`domain`** | **eliminated** as a field; it was \(\mathcal A_F\) |
| **`movement`** | **relocated** — edge validity, evidence jurisdiction |
| **`CONSTRUCTED_DOMAIN_UNDECIDED`** | **eliminated.** A declaration is complete — and its extension derived — or incomplete, and refused at **declaration tier** (D3) |
| **contribution multiplicity** | **relocated** — to **universe individuation** where the index is governed, and to **realization conformance** where it is not (Amendment 1) |
| *(also settled earlier)* stock / flow / semi-additive kinds | **eliminated** — a scope is not a kind |
| *(also settled earlier)* reducer semantics from realization mappings | **relocated** — realization is **checked against** the clause, never the source of it |

> **Still genuinely required: none of them.** The audit is not vacuous, though — **one thing is newly required**,
> and it is not on the list: the **coherence condition** of §4.4, which is the positive successor to the
> B-anchor's legitimate worry and costs one well-formedness check.

---

## 10. Report

### 10.1 Does `source × scope` survive?

> **Yes, explicitly, and without growing.**

- **No source kind was added.** Two, with a closure argument (§2.1) rather than an enumeration.
- **No third factor was added.** Co-participation was the only candidate, and it is a property of how a law's
  operands are bound — therefore part of `source` (§2.3).
- **No field was added to the clause**, and one — contribution multiplicity — left.

### 10.2 Contradictions

**None found.**

### 10.3 Genuinely missing semantic concepts

**One, and it is derived rather than authored:** **`identity_at(F, A)`**, the determination identity at a
location, distinct from family identity. Without it, *upstream-consequential* and *downstream-inert* cannot both
be true (§5.3). With it, both are theorems, canonicalization becomes computable, and the separation stops being
a rule and becomes a property of a function's signature.

**One new required condition:** **coherence** (§4.4) — a family must be a function. This is a *condition*, not a
concept, and it costs one check.

**Three qualifications carried forward, not resolved:** the non-normalizable grounding handle (§5.2); the law of
a non-catalogued construction (D3 names it, and the contract does not solve it); and the boundary qualifications
on Amendment 2 (§8.4).

---

**Stopped at the abstract semantic declaration contract.** No serialization, no implementation.

# The Columna semantic contract

**A positive statement of the model, and the acceptance suite it survived.** Consolidated by Claude at Huayin's
direction, 2026-09-24.

> ❄ **FROZEN**, 2026-09-24, by Huayin, as the semantic contract for the declaration-design unit — subject to
> the standing rule that **a genuine contradiction discovered downstream can reopen it**. The representation
> derived from it is [`manifold_declaration_model_v1_0.md`](./manifold_declaration_model_v1_0.md), which found no
> contradiction.
>
> **Freeze amendments, 2026-09-24 (Huayin).** Carried as part of the freeze, from
> [`manifold_declaration_model_review_v1_1.md`](./manifold_declaration_model_review_v1_1.md):
> **(1) contribution multiplicity is retired as a primitive family fact** — if multiplicity is governed, the index
> over which it exists must itself be governed, which is individuation or another governed construction. §1.4 and
> §5.1 are amended: an observational family's irreducible facts go from **five to four**.
> **(2) governed point selection versus population-changing restriction** — a coordinate pin selects governed
> analytical points without introducing a new population; a value predicate may instead define a different
> participating population and **cannot acquire constitutive authority merely because request syntax can express
> it**. Qualified, not universal — see the contract §8.4.
> **(3) R1 is replaced** by **R1′ single authority** and **R1″ identity over resolved semantics**.

**Standing.** Design record. **No implementation, no publication schema, no migration, no deletion of code, no
repair of the producer/consumer mismatch.** This document states what we believe and reports what happened when
we tried to break it. It stops there.

**How to read it.** The main body is written **forward, from the current understanding**. It does not require the
archaeological sequence that produced it. Appendix S records which earlier hypotheses were withdrawn and why, for
anyone who needs to know that a question was asked and closed; nothing in the body depends on it.

> ⚠ **WORKING PREMISE, NOT RATIFIED.** The worked cases use the Case-S universe constitution of the 2026-09-15
> record as a **working premise**. Its §§1–6 remain **draft**; only §§7–11 are ruled. **Nothing here ratifies
> it.** Where a fact turns out to belong to universe constitution, §1.6 places it there rather than duplicating
> it into a family.

---

## 0. The four layers

> **Manifold constitutes → Measure Algebra entails → MEL denotes → Frame-QL requests.**

| layer | what it does | what it may **not** do |
|---|---|---|
| **Manifold** | constitutes quantities: says what is observed, where, for which points, in what type, and how it is determined | derive anything; store anything a law already entails |
| **Measure Algebra** | entails consequences of universal law from what was constituted | constitute; admit a law it was not given |
| **MEL** | denotes — supplies the canonical analytical expression, parametrically | constitute; decide standing |
| **Frame-QL** | requests, resolves, and disposes | redefine meaning; refuse for a reason belonging to a different quantity |

Strictly **below** the analytical line, and never mixed into it: **governance may withhold; evidence and
realization determine servability.**

---

## 1. The model

### 1.1 The one sentence

> **A family is constituted by determination clauses.**

A **determination clause** says how a value of that family is determined. There is nothing else in a family
except the small set of per-family facts a clause presupposes (§1.4). A family is not a domain, not a lattice,
not a root with a reach, not a kind. **It is a set of claims about how it is determined, and the union of what
those claims cover is everything it means.**

### 1.2 The clause

```
determination clause
  ├── argument shape   observation | fiber-reducing | co-located
  ├── source           THE WORLD          -- observation shape only; this is where law runs out
  │                  | a cited universal law, with its identity-bearing parameters
  ├── operands         for law sources: the measures consumed, WITH THEIR ROLES
  ├── scope            the structural conditions — decidable from governed geometry alone
  └── premises         the value/data conditions — decidable only from values
```

**Argument shape.**

| shape | what it consumes | what it produces |
|---|---|---|
| **observation** | the world at a point | the value at that point |
| **fiber-reducing** | the family's values over the fiber below a coarser point | the value at that point |
| **co-located** | measures at the **same** point | the value at that point |

The shape is **identity-bearing**: `mean(X@I)@A` and `X/Y@A` are different kinds of object, not two spellings.
MEL carries it, and MEL must carry **operand roles** too, because some laws are noncommutative (case 22).

**Source.** Either the world, or a cited universal law. A source that cites a law **terminates**: the operands
are measures of other families, and that recursion bottoms out at observation. **A family with an observation
clause is observational; one with none is constructed.** Nothing declares which — it is read off.

**Scope versus premise — separated by *when the condition can be decided*, and by nothing else.**

| | decidable from | example |
|---|---|---|
| **scope** | governed geometry alone, before any data | *over fibers varying only in `{account}`* |
| **premise** | the values | *given the fiber is currency-homogeneous* |

> **A premise may *gate* a clause; it may not *change* what the clause produces.** If a proposed condition changes
> the result's value domain or its target, it is a **law application** and must be a construction with its own
> identity (case 16). Without this rule "premise" is an unbounded escape hatch and the clause model degenerates
> into arbitrary code.

**Law parameters are identity-bearing.** `ddof`, the governed order LAST uses, a quantile convention, a sketch
precision: change one and the quantity is different, not better-approximated. §1.9 gives the test for telling an
identity-bearing parameter from a realization choice.

### 1.3 Scope is a quantifier, not a prohibition

This is the distinction the whole model turns on, so it is stated before anything is built on it.

A clause's scope is a **positive quantifier on a claim**: *this law, over these fibers, means this.* It asserts
nothing about fibers it does not mention. **The absence of a clause is the absence of a meaning, never the
presence of a bar.** A negative declaration would have to be *complete over every law* to mean anything at all;
a positive one need not be, and says only what the author actually knows.

### 1.4 The per-family facts a clause presupposes

Three, and they survive because a clause cannot be read without them.

| fact | what it says | who has it |
|---|---|---|
| **eligibility** | which points the quantity applies to — **ranging over *eligible* points, never observed ones** | observational families only |
| **contribution multiplicity** | how many governed contributions sit at one point | observational families only |
| **governed value-type reference** | a CDT reference, **possibly with an authored parameter** (an exact-equality profile; a collation) | both, but constructed families author it only where the law does not determine it |

Eligibility must range over eligible points, or known-empty and unknown become indistinguishable and the
empty-fiber outcome stops being entailed. **A constructed family authors no eligibility of its own**: it is
entailed from its operands and its co-participation contract.

### 1.5 Family continuation is not family formation

> **A family's determination clauses govern how *that family* is determined. They do not license, and cannot
> prohibit, that family's measures serving as operands of other lawful family-forming constructions.**

| question | answered by | indexed on |
|---|---|---|
| **continuation** — is \(F\) itself determined at \(A\)? | \(F\)'s own clauses | the family |
| **formation** — is \(g(F@I)@A\) a lawful family? | \(g\)'s law, over measures of \(F\) at \(I\) | the construction |

**Formation asks exactly one thing of \(F\): that \(F@I\) be determined.** It does not ask *which* clause
determined it, and a family declaration contains **no term ranging over constructions**, so it cannot ask what
clauses \(F\) lacks.

**The operand rule.** A construction names an operand \(F@A\) and requires only that \(F@A\) be determined.
**Any clause of \(F\) may supply it** — grounding or composition, original or added later.

**Three consequences the model owes:**

1. **extension-monotone** — adding a clause to \(F\) only adds anchors at which \(F\) is determined; **no value
   already determined changes**.
2. **downstream-inert** — adding a clause to \(F\) changes **nothing** about the identity, law, extension or
   meaning of any construction over \(F\)'s measures.
3. **upstream-consequential** — it *does* change \(\Sigma(F)\); a clause is identity-bearing. **The change lands
   on \(F\) and stops there.**

So declaring `balance @ week := LAST(balance @ day)` under the governed day order changes **what Balance
determines**. It does not touch `mean(balance @ day) @ week`, `sum(balance @ day) @ week`, or any other
construction whose operand remains `balance @ day`.

> ⚠ **Formation is not a bypass.** What a construction escapes is \(F\)'s *clauses* — not the world's structure,
> not CDT's capabilities, and not its own law's requirements. A construction over an impossible geometry fails on
> the geometry, exactly as an ascription would (case 5). The separation is a statement about *where restrictions
> live*, not a loophole.

**The auditable form, for anything derived from this contract:**

> **A check that consults \(\mathcal A_F\), an edge-validity fact about \(F\), or \(F\)'s clause list, while
> deciding a construction over \(F\)'s measures, is the defect — under whatever name it travels.**

### 1.6 What the universe supplies

The family declaration is small because most of what used to be crowded into it is a fact about the world.

| universe fact | needed by |
|---|---|
| individuation of a world, and its `exists_when` | every case |
| governed **projections** between anchors, including calendar relationships | cases 6–13 |
| governed **placements** (`store → region`), **with their multiplicity** | cases 4, 5 |
| governed **orders** on a constituent | cases 7, 10, 21, 22 |
| whether a governed projection is **order-compatible** with a governed order | case 21 — **new in this pass** |
| a constituent's identity and value domain | cases 15, 16 |
| governed **conversions** to a numéraire | case 16 |

**Anchor identity is universe-relative.** A world individuated by `{account, week}` has weeks as *root points*;
its `week` is **not the same anchor** as a `week` reached by projection from days. Comparing them is universe
passage, not a family question.

### 1.7 What CDT supplies

The value-type reference is a **governed reference**, and what it refers to carries consequences the family never
restates: the capability matrix (which laws a type admits at all), equality and collation profiles, result
domains, and the partiality of operations. `Set<Text>` is *not admitted from the bare spelling `Text`* — it needs
a declared exact-text-equality profile, and **that profile is an authored parameter inside the type reference,
not in the family law.**

> **Open obligation on CDT, raised by case 3 and unresolved here:** the capability matrix must carry
> **measurement scale** (ratio / interval / ordinal / nominal), or the model admits constructions with no
> meaning — `sum` over an interval-scaled type is the standing example. This is the single strongest remaining
> argument anyone could make for a prohibition mechanism, and §4 shows it lands in CDT rather than in the
> family.

### 1.8 What Measure Algebra entails

Never authored, always derived:

- the **extension** \(\{A : F@A \text{ is determined}\}\) — **notation for a derived predicate, never an object**;
- whether a family is observational or constructed;
- analytical lineage — the operands the clauses name;
- result value domains, from law × operand domain;
- **sufficient-state bases**, where a law is cited — *establishment only, never standing*;
- the **empty-fiber outcome**, from the cited law's identity and eligibility, and only where the fiber is
  **known**-empty;
- the witness family and witness monoid for FIRST/LAST — establishment machinery, which **does not split
  identity**;
- **direct/staged agreement**, and here the model carries a refinement:

> **Staged agreement requires associativity. For a *noncommutative* law it additionally requires the intermediate
> projection to be order-compatible with the law's governed order.** Where that fact is absent, only **direct**
> composition stands, and the engine must decline to stage rather than produce a number. **Absence of a theorem,
> like absence of a clause, is absence of meaning — not a bar** (case 21).

### 1.9 Meaning versus approximation — the operational test

A parameter is **identity-bearing** (meaning) if the author must supply it, and **realization** if the planner
may choose it.

> **If the planner may choose it, the meaning is the exact quantity and the choice is reported as realization
> quality. If the author supplies it, the parameter is part of the quantity.**

An exact distinct count served through a sketch is one family, approximately served. An estimator with an
authored precision is a **different** family, exactly served. Confusing them is confusing meaning with
servability (case 18).

### 1.10 The failure kinds

Nine, and they must not be merged. Frame-QL's disposition vocabulary needs all of them.

| # | kind | what it means | decidable |
|---|---|---|---|
| 1 | **geometry** (want of relationship) | no governed projection or placement; or the relationship yields a **cover, not a partition**, so there is no fiber to reduce | before data |
| 2 | **law-to-type inadequacy** | the type lacks the law's required capability. **Anchor-invariant** — it fails at the constitutive anchor too | before data |
| 3 | **want of law** (want of meaning) | the geometry and the types are fine; **no clause claims this means anything** | before data |
| 4 | **ambiguity** | several lawful readings; → **Clarify** | before data |
| 5 | **undefined result** | determined at the anchor, **undefined at a point**. Not disclosable | after data |
| 6 | **want of state** | the meaning stands; the basis was not retained | after data |
| 7 | **want of evidence / coverage** | partial support → **Disclose** | after data |
| 8 | **realization inadequacy** | no carrier or plan honours the clause's semantics | after data |
| 9 | **withhold** | governance. Meaning and servability are both fine | policy |

**The serving principle.** A meaningful, resolved request is **not** refused because some intermediate operation
would have been rejected under a different identity. **Refusal requires a real failure belonging to the quantity
actually requested**, and the disposition must name which of the nine it is.

### 1.11 Distinctions held hard

| do not collapse | kept apart by | what the collapse would cost |
|---|---|---|
| meaning / servability | §1.9; cases 18, 24 | an estimator's precision becomes a quantity, or a quantity becomes a planner's choice |
| lawful expression / available evidence | kinds 3 vs 6–7 | *want of law* returned for a retention gap; the author "fixes" the theory |
| **family continuation / construction over a family measure** | §1.5; cases 7–13, 22 | the case-17 defect: one family's silence bars unrelated quantities |
| current value / sufficient state | §1.8; case 12 | \((\Sigma,N)\) mistaken for identity; case-12's three objects fuse |
| geometry / analytical law | kinds 1 vs 3; cases 5, 11, 12 | a missing projection "repaired" by widening a scope — a wrong number |
| semantic type compatibility / analytical meaning | kind 2; cases 3, 19 | `Timestamp + Timestamp` because the carrier is numeric |
| ambiguity / invalidity | kind 4; cases 8, 12, 15, 20 | Clarify replaced by Refuse — the old instinct, and the most common one |
| governance restriction / analytical meaning | kind 9 | `WITHHOLD` becomes ontology and the theory absorbs policy |
| observation / entailment | §1.1–1.2, §1.8 | either the author restates theorems, or the engine invents observations |

---

## 2. The acceptance suite

Twenty-four cases. Each answers exactly five questions: what is **constituted**, what is **entailed** by
universal law, what MEL merely **denotes**, what Frame-QL **requests/resolves**, and — if it fails — **which of
the nine failure kinds** it is. Cases that were built specifically to break the model are marked **⚡**.

The suite was chosen to spread across the three stress dimensions: **semantic value type** (cases 3, 14–20),
**anchor/coordinate structure — point-in-time versus interval, and governed order** (cases 6–13, 20–22), and
**every historical form of prohibition behaviour** (cases 3, 5, 6, 8, 13, 19, 21).

### I. Observation

#### Case 1 — observational `revenue`

```
family revenue
  grounds    : at sales.{store,day,order,line}, the consideration accruing from the line
  eligible   : every root point of the universe
  contributes: one contribution per eligible point
  valued in  : CDT Decimal
  composes   : fiber-reducing, SUM, over ANY fiber
```

- **Constituted** — five facts. The grounding prose is the only irreducibly extra-formal one. *That additive
  composition means anything* is the author's contingent claim, and it is the whole of what distinguishes this
  family from case 2.
- **Entailed** — extension = every anchor reached by a governed projection; direct/staged agreement; known-empty
  fiber takes the monoid identity; `sum(revenue @ line)` **is this family**, by canonicalization, not a
  construction.
- **Denoted** — `revenue`. MEL knows nothing of consideration; it knows a governed operand at a governed anchor
  with a cited SUM clause.
- **Resolved** — by name, at any anchor. Serve; Disclose on partial coverage.
- **Failure** — none.

#### Case 2 — observational `balance`

Identical in shape. **Three of the five facts are word-for-word case 1's.**

```
  grounds    : at ledger.{account,day}, the amount standing to the account at the close of the day
  composes   : fiber-reducing, SUM, over fibers varying only in { account }
```

- **Constituted** — five facts, differing from case 1 in **the grounding prose and one quantifier**.
- **Entailed** — extension = `{ {account,day}, {day} }`. **Nothing else is entailed and nothing is prohibited.**
- **Denoted / Resolved** — as case 1, within its extension.
- **Failure** — none.

> That one quantifier is the entirety of semi-additivity, the stock/flow taxonomy, the B-anchor and \(P_F\).

#### Case 3 ⚡ — observational `temperature`, and the construction a prohibition model would have had to catch

```
family temperature
  grounds    : at weather.{station,day}, the mean air temperature at the station that day
  valued in  : CDT Decimal, °C                    -- an INTERVAL scale, not a ratio scale
  composes   : fiber-reducing, MEAN, over fibers varying only in { day }
```

**Built to break the model**, because `sum(temperature @ day) @ {month}` is the one construction where the two
refusals that catch everything else both miss: the geometry is fine, and the carrier is `Decimal`, which admits
`+`. A prohibition model would have needed a bar here. What actually happens:

- **Constituted** — the grounding clause, and a MEAN clause. **No SUM clause**, because summing temperatures is
  not a quantity this author has.
- **Entailed** — `temperature @ {month}` is a mean, from the MEAN clause. `sum(temperature @ day) @ {month}` is
  **a different family** whose law is complete and whose arithmetic is perfectly well-defined.
- **Denoted** — MEL writes both.
- **Resolved** — the ascription Serves. The construction is where the case bites.
- **Failure** — **kind 2, law-to-type inadequacy — *if and only if* CDT carries measurement scale.** Summing an
  interval-scaled quantity has no meaning: the sum of Celsius readings depends on the zero of the scale, so it is
  not a quantity at all. Summing the **difference** `degree_excess = temperature − base` — a ratio-scaled
  difference — is meaningful, and is exactly heating/cooling **degree-days** (case 13).

> ⚡ **This is the closest the suite came to a counterexample, and it is worth being exact about where it lands.**
> The model as stated does not catch `sum(temperature@day)`; it admits it as a lawful construction with a
> meaningless unit. **But the missing fact is a property of the *type*, not of the quantity's anchor** — it fails
> at the constitutive anchor too, which is the signature of kind 2 and the reason it cannot be a family fact. The
> obligation therefore falls on **CDT**, as §1.7 records. **A family-indexed prohibition would have been the
> wrong repair**: it would have blocked `sum` on Temperature while leaving `sum` on every other interval-scaled
> family — Fahrenheit, pH, calendar dates as numbers, credit scores — untouched, because it is indexed on the
> family and the defect is in the type.

### II. Ascription and geometry

#### Case 4 — `revenue @ {region}`

- **Constituted** — **nothing at the family layer.** `region` needs a **governed placement `store → region`**,
  which is a **universe** fact, and it must carry its multiplicity.
- **Entailed** — Revenue's clause is claimed over **any** fiber, so given a *functional* placement the law
  determines a value. **Geometry does not license it; the clause's universal quantification does.** Geometry only
  supplies the fiber.
- **Denoted** — `revenue @ {region}` — an **ascription, not a construction**. The query names the family identity;
  it does not need to become `sum(revenue @ {line}) @ {region}`.
- **Resolved** — Serve; Disclose on partial coverage; two governed placements → **Clarify**.
- **Failure** — none, once the placement is governed. Today: **kind 1**, and nameably so — a held universe
  question, not a family one.

#### Case 5 ⚡ — `revenue @ {tag}`, where the relationship is many-to-many

The canonical fan-out: a line carries several tags, and the naive answer is a well-typed, deterministic, wrong
number. **Built to test whether the model stops rather than inventing an answer.**

- **Constituted** — nothing, and **nothing at the family layer could help.**
- **Entailed** — **nothing, and this is the point.** A fiber-reducing clause consumes *the fiber below a point*,
  and *fiber* presupposes that the points below **partition**. A many-to-many relationship gives each tag an
  overlapping preimage: **a cover, not a partition. There is no fiber to reduce.** The clause's argument does not
  exist.
- **Denoted** — MEL writes it.
- **Resolved** — refuse, and **name the missing fact**: either a governed **functional** placement, or an
  **allocation construction**.
- **Failure** — **kind 1, geometry.**

> **Where the model stops, and why that is the right behaviour.** Allocating revenue across a line's tags changes
> what is produced — it is a law application, so by §1.2 it must be a **construction**, with its own authored
> allocation law, its own parameters and its own identity. **The model declines to choose one.** It does not
> silently sum, silently de-duplicate, or silently allocate, and it does not invent a default. That is the
> natural stopping point for relationship expansion, and it needs no new concept to reach it.
>
> ⚠ **And note the consistency check:** writing it explicitly as `sum(revenue @ {line}) @ {tag}` does **not**
> rescue it. The construction's own clause needs a fiber too, and the geometry is the same. **§1.5's separation
> is not a loophole** — formation escapes \(F\)'s clauses, never the world's structure.

#### Case 6 — `balance @ {week}`, before any weekly clause exists

- **Constituted** — nothing, *given Balance as declared in case 2*.
- **Entailed** — no clause covers fibers varying in `day`. **The law determines no value.** Not prohibited —
  *undetermined*.
- **Denoted** — the expression denotes perfectly well. **What fails is family standing, not denotation.**
- **Resolved** — **kind 3, want of law.** The remedy is not to widen a permission; it is either to ask cases 8–10,
  which are different quantities, or to *say one more thing about Balance* — case 7.
- **Failure** — kind 3.

#### Case 7 — the business declares `balance @ week := LAST(balance @ day)`

```
family balance
  ...
  composes   : fiber-reducing, SUM,  over fibers varying only in { account }
  composes   : fiber-reducing, LAST, over fibers varying only in { day },  order = O    -- NEW
```

- **Constituted** — **one new fact: a second composition clause on Balance itself.** The order `O` is a universe
  fact; *which* order is a family fact only where the world admits more than one.
- **Entailed** —
  - the extension **widens monotonically**: `{account,week}`, `{account,month}`, and every anchor reachable by
    day-fibering. **It loses nothing.**
  - the LAST machinery — witness family, basis, witness monoid, known-empty \(\bot\) — is **establishment, not
    identity**. A witness family inside Balance's establishment does **not** split Balance.
  - **not entailed:** a fiber varying in **both** `account` and `day`. SUM's scope is account-only, LAST's is
    day-only, and they do not commute in general. ⚠ **Corrected 2026-09-25** — the reason is **not** that the last
    *observed* day differs across accounts, which would wrongly let support choose the winner. Governed LAST is
    `argmax` over the **participating** fiber (ToD §8.2), and the obstruction is **governed sparsity** of that
    domain. ToD §11.2 works the counterexample with numbers and rules that *"an interchange law would need its
    own premises."* See [`last_sum_interchange_verification_v0_1.md`](./last_sum_interchange_verification_v0_1.md).
    `balance @ {week}` with no account stays **undetermined** until a clause covers it. **The right failure mode.**
- **Denoted** — `balance @ {account,week}` — an **ascription**, exactly as case 4.
- **Resolved** — Serve. *"Weekly balance"* is now unambiguous **for this business**; *"total balance"* is still
  **Clarify**.
- **Failure** — none.

> **This is the first family in the suite with two composition clauses citing different laws over different
> scopes**, and it is the case that fixes the model's shape. Case 6 is not overturned: the verdict changed because
> **the declaration changed** — the business said one more thing about what Balance *is* — not because a bar was
> lifted.

### III. Construction over `F @ I`

Cases 8–13 all consume `balance @ {account,day}` or an analogue. **None of them is affected in any way by case
7's new clause**, and that is the acceptance criterion.

#### Case 8 — `sum(balance @ {day}) @ {week}`

- **Constituted** — **nothing.** The law is catalogued; the operand is established by Balance's grounding clause.
- **Entailed** — Balance's own clause does not cover day-varying fibers, so this is **a different family**, with a
  complete law: Σ over any fiber of Balance point-values. Extension: every anchor coarser than `{account,day}`.
  Its target — **the additive total of daily balances** — is a perfectly definite quantity.
- **Denoted** — `sum(balance @ {account,day})`, parametric in the operand.
- **Resolved** — **Serve, under its own identity.** *"Total balance"* → **Clarify**: this, a closing balance, or a
  current balance.
- **Failure** — none. **The number was never the problem; the label was.**

#### Case 9 — `mean(balance @ {day}) @ {week}`

- **Constituted** — nothing.
- **Entailed** — MEAN consumes Balance **at the operand anchor the expression names**. Balance does not travel to
  Week; **MEAN establishes a different family** whose fibers happen to be week-fibers of days. Result type
  **Rational** — exact division is not closed in Decimal. Empty fiber **undefined**, from the law's nonempty
  constructor domain. \((\Sigma,N)\) is **how it is established, not what makes it stand**.
- **Denoted** — `mean(balance @ {account,day})`.
- **Resolved** — Serve; partial day coverage → Disclose; only weekly scalars retained → **kind 6**, never kind 3.
- **Failure** — none.

> ⚠ **The rule this case must be stated with care to avoid.** It is tempting to write *"MEAN consumes Balance at
> singleton fibers of its grounding clause — never its composition clause."* That is a true observation about
> case 2's Balance **mis-stated as a rule**, and it is precisely the leak §1.5 forbids. Under case 7's Balance,
> `mean(balance @ {account,week}) @ {quarter}` is lawful and **its operand comes from a composition clause.**

#### Case 10 — `last(balance @ {day}) @ {week}`, and canonical equivalence

- **Constituted** — a governed complete order on `day` (universe); at the family layer, **which** order, and only
  if the world admits more than one. Appending a storage identifier or relying on sort stability is not a repair
  of analytical law.
- **Entailed** — witness family \(W\), basis, witness monoid, known-empty \(\bot\) — all theorem. Extension: every
  anchor coarser than `{account,day}`, **wider than case-2 Balance's own**, because the witness monoid composes
  where Balance's clause does not. **Nothing propagated; nothing was blocked.**
- **Denoted** — `last(balance @ {account,day}; order = O)`.
- **Resolved** — Serve. Two governed day-orders → Clarify.
- **Failure** — none.

**Canonical equivalence with case 7 — three claims that must not be merged:**

1. **Value agreement is ENTAILED and conditional** — on the cited law, its identity-bearing parameters (**the
   order**), the operand anchor, eligibility and the known-empty outcome, and the value type. Under \(O'\neq O\)
   there is **no** equivalence; that is \(W(O')\), standing alone.
2. **Canonicalization is AUTHORED, at the naming layer.** The business declares the governed equivalence and the
   construction resolves to the family name — the same mechanism as `sum(revenue@line) ≡ revenue`, and the model
   needs no other. Generalized: **a construction restating one of \(F\)'s own clauses, at an anchor inside that
   clause's scope, with matching parameters, is canonically \(F\).** *It is not string aliasing.*
3. **Identity is not minted.** \(W\) remains its own family; any downstream lineage naming \(W\) is untouched.

> ⚠ **Equivalence may never be inferred from extensional coincidence.** Agreement on every currently servable
> value is **evidence**, not a governed equivalence. A system that mints equivalences from agreeing data is
> constituting from evidence.

#### Case 11 ⚡ — `mean(mean(balance @ day) @ week) @ {quarter}`, where the outer grouping does **not** preserve the inner

- **Constituted** — nothing at the family layer.
- **Entailed** — the outer MEAN consumes \(M_1\) established at `{account,week}`. Its extension is every anchor
  **coarser than `{account,week}`** — which requires a governed projection `{account,week} ⪰ {account,quarter}`.
  Under ISO weeks and calendar quarters **that projection does not exist**: a week crosses the quarter boundary.
  **Decidable before any data.**
- **Denoted** — `mean(mean(balance@{account,day})@{account,week})`. MEL writes it happily.
- **Resolved** — refuse, **naming the missing universe fact**: no governed `week → quarter`.
- **Failure** — **kind 1, geometry** — *not* kind 3. The remedy is a **universe** declaration, never a family
  clause. **Widening \(M_1\)'s scope to "fix" it would produce a wrong number**, and this is the sharpest instance
  of the geometry/law distinction in the suite.

#### Case 12 — the same expression (the control for case 11) where the outer grouping **does** preserve the inner

Change one universe fact and nothing else: a **4-4-5 retail calendar**, whose fiscal quarters are *defined as*
thirteen whole weeks. Now `{account,week} ⪰ {account,fiscal_quarter}` **holds**.

- **Constituted** — still nothing at the family layer. **The same two families, unchanged.**
- **Entailed** — \(M_2\) is determined at `{account,fiscal_quarter}`. **Three objects must stay apart:**

| | what it is |
|---|---|
| `mean(mean(balance@day)@week)@fq` | **a new family** — the unweighted mean of weekly means |
| `mean(balance@day)@fq` | **the same family as \(M_1\)**, at a coarser anchor — meaning fixed at constitution, establishment via its \((\Sigma,N)\) basis |
| the *"mean of means"* criticism | **confusing the two, or leaving the intended one ambiguous** |

- **Resolved** — explicit MEL → Serve. *"Average balance for the quarter"* → **Clarify** among the three. Weekly
  \((\Sigma,N)\) retained but weekly scalars discarded → the second Serves and the first is **kind 6**.
- **Failure** — none.

> **Cases 11 and 12 are the same expression, the same families and the same laws in two different worlds, with
> opposite verdicts, and the deciding fact is a *universe* fact.** *Mean-of-mean is not intrinsically unlawful* —
> and *composite sufficient state does not imply composite measure identity*, which is what keeps the three
> objects apart.

#### Case 13 — `sum(degree_excess @ {day}) @ {season}` — degree-days

```
family degree_excess
  constructs : co-located, DIFFERENCE[ base = 18°C ], of ( temperature )   -- ratio-scaled: a °C DIFFERENCE
  composes   : fiber-reducing, SUM, over ANY fiber                          -- unit: degree-days
```

- **Constituted** — the base, an identity-bearing law parameter (18 °C and 65 °F are **different quantities**),
  and a SUM clause on the derived family.
- **Entailed** — the result unit `degree-days`; `temperature @ {month}` remains a mean and is untouched.
- **Denoted / Resolved** — Serve, under its own identity and unit. *"Temperature for the season"* → Clarify.
- **Failure** — none.

> **The third independent witness that what prohibition rejected is a real, named, standard quantity** — after
> the additive total of daily balances (case 8) and integrated stock exposure, *inventory-unit-days*, the
> quantity behind DIO and inventory turns. **Three different domains, three real quantities, one mislabelling
> each time.** The only error was ever the label — and, as case 3 shows, the index.

### IV. Semantic value types

#### Case 14 — currency in the **semantic value type**

```
  valued in : Money = ( amount, currency )        -- `+` is PARTIAL: within a currency only
  composes  : fiber-reducing, SUM, over ANY fiber, GIVEN the fiber is currency-homogeneous
                                                   ^^^^^ a PREMISE
```

- **Constituted** — the type reference and the premise.
- **Entailed** — the family **stands** at `{region}` — the clause is claimed over any fiber — and is **undefined
  at region-points whose fiber spans currencies. Determined at the anchor; undefined at a point.**
- **Denoted** — `revenue`, unchanged. The partiality lives in the type and the premise, not the expression.
- **Resolved** — Serve at homogeneous points; **kind 5** at heterogeneous ones, and **not disclosable**: a
  disclosure may state a limitation on an otherwise established result; it cannot make arbitrary point selection
  determinate.
- **Failure** — kind 5, pointwise.

> **This is why no per-anchor domain object could ever have been right, even for observational families:
> definedness here is *below anchor granularity*.** No object indexed by anchor can carry it.

#### Case 15 — currency as an **analytical constituent**

The universe individuates `{store, day, order, line, currency}` — **a universe change, not a family change.** The
value is then a bare Decimal:

```
  composes  : fiber-reducing, SUM, over fibers varying only in { store, day, order, line }
                                                                ^^^^^ a SCOPE
```

- **Constituted** — a scope instead of a premise. **Nothing else moved.**
- **Entailed** — `revenue @ {region}` now **forgets `currency`**, which the scope excludes → **kind 3**, decided
  from geometry before any data. `revenue @ {region, currency}` is determined.
- **Denoted** — `revenue`, at a richer anchor lattice.
- **Resolved** — `@ {region,currency}` Serves; `@ {region}` is kind 3; *"revenue by region"* in a multi-currency
  world → **Clarify**, because the caller has probably not said which they mean.
- **Failure** — kind 3, for the `{region}` reading only.

> **Cases 14 and 15 jointly fix the scope/premise rule: the two are separated by *when the condition can be
> decided* — geometry alone versus the values — and by nothing else.** The same analytical concern lands in a
> different slot depending on representation, **and both are lawful**; the model must not force either.
>
> And note the shape: **under case 15's representation, Revenue's clause looks exactly like Balance's** — a scope
> excluding one constituent. **The flow/stock difference is not even a difference of kind.**

#### Case 16 — a conversion, which produces a new value domain

```
family revenue_usd
  constructs : co-located, CONVERT[ to = USD, rate = <governed> ], of ( revenue )
  composes   : fiber-reducing, SUM, over ANY fiber        -- ENTAILED: USD is homogeneous
```

- **Constituted** — a governed conversion is a **universe** structure; the family authors the citation and its
  parameters.
- **Entailed** — the tempting alternative, a premise *"SUM over currency-varying fibers **given** a conversion"*,
  is **rejected**: a conversion **changes the result's value domain** — the output is in USD, the point values
  are not. That makes it a **law application**, so it constitutes **a different family**. A changed target gets a
  successor identity instead of hiding inside a condition.
- **Denoted** — `convert[USD](revenue)`.
- **Resolved** — Serve where the governed rate covers the points; rate missing for some points → **kind 6**; two
  governed rate sources → **Clarify**; rate ungoverned → **kind 3**.
- **Failure** — none, as declared.

#### Case 17 — a set-valued family, and a scalar that never composes

```
family distinct_customers
  grounds    : at sales.{store,day,order,line}, the customer identity on the line
  valued in  : Set<CustomerId>            -- requires a governed exact equality on CustomerId
  composes   : fiber-reducing, UNION, over ANY fiber

family count_distinct_customers
  constructs : co-located, CARDINALITY, of ( distinct_customers )
```

- **Constituted** — the type reference **with its equality-profile parameter**. `Set<Text>` is *not admitted from
  the bare spelling `Text`*; without a declared exact-text-equality profile, equality-dependent set operations
  are refused. **That parameter is authored, and it sits in the type reference, not in the family law.**
- **Entailed** — UNION is associative, commutative and **idempotent** — a materially different continuation from
  SUM, and CDT supplies it. The scalar **stands exactly where the set family stands and never composes**, because
  a cardinality does not retain enough information to determine overlap during a later union. **A co-located
  clause and no fiber-reducing clause of its own.**
- **Denoted** — `distinct_set(customer@line)`, `count_distinct(...)`.
- **Resolved** — Serve; **kind 3** if no equality profile is declared for the element type.
- **Failure** — none, given the profile.

#### Case 18 ⚡ — a sketch, and the line between meaning and approximation

**Built to test the meaning/servability distinction**, because a sketch can legitimately be either side of it.

| | declaration | what the parameters are |
|---|---|---|
| **(a)** | `distinct_customers` valued in `Set<CustomerId>` (case 17), **served through an HLL sketch** | the precision is a **planner choice**; the meaning is the **exact** count; the error is **realization quality**, reported on the certificate → **Disclose** |
| **(b)** | `estimated_distinct_customers` valued in `HLLSketch[p=14, hash=H]`, composing by **MERGE**, with a co-located `CARDINALITY-ESTIMATE` clause | `p` and the hash are **identity-bearing**. Change `p` and it is **a different quantity**, not a better approximation of the same one |

- **Constituted** — (a) nothing beyond case 17. (b) the sketch type reference **and its parameters**.
- **Entailed** — MERGE is associative, commutative and idempotent-ish in the sketch algebra, so (b) composes; the
  cardinality estimate is co-located and does not compose, for case 17's reason.
- **Denoted** — MEL cannot tell (a) from (b); **it is not supposed to**.
- **Resolved** — (a) Serve with a disclosure. (b) Serve exactly, under its own identity.
- **Failure** — none. **Collapsing (a) and (b) would be the failure**: either an estimator's tuning becomes a
  quantity, or a quantity becomes a planner's choice.

> **The operational test, §1.9: if the planner may choose the parameter, the meaning is the exact quantity and
> the choice is realization quality. If the author supplies it, the parameter is part of the quantity.** One
> question, and it separates them every time.

#### Case 19 — a `Timestamp`-valued family

- **Constituted** — the grounding clause and the type reference.
- **Entailed** — `Timestamp + Timestamp → undefined`. These are **capability restrictions, not syntactic
  conventions**: a timestamp cannot enter an additive analytical family merely because its carrier is numerically
  encoded.
- **Denoted** — MEL writes `sum(event_time@...)`.
- **Resolved** — **kind 2, law-to-type inadequacy**, which is **neither want of law nor want of state**.
- **Failure** — kind 2, and **anchor-invariant**: it fails at the constitutive anchor too.

> **`sum(event_time@…)` and `balance @ week` fail for completely different reasons and a model with one refusal
> here would be wrong.** The first: the values **cannot be added at all**, decidable before any anchor is
> considered. The second: the values **could** be added — no clause claims it means anything.

#### Case 20 — point-in-time versus interval

**Four objects that calendar vocabulary fuses, and the model keeps apart:**

| | what it is | where it lives |
|---|---|---|
| **a point-in-time quantity** | grounded at a point, no time-crossing composition | Balance, case 2 |
| **"over the members of" a period** | a fiber-reducing clause | cases 8, 9 |
| **"at the end of" a period** | a fiber-reducing clause citing LAST with a governed point order | cases 7, 10 |
| **an interval-*valued* quantity** | the **value** is an `Interval` | **a type fact, not an anchor fact** |

- **Entailed** — `Interval` has *no intrinsic total order*, *no general analytical additive claim*, and is
  distinct from `Duration`; an internal numeric representation *does not make `Interval` an additive scalar*.
  **Internal value structure is not analytical location. A family whose value is an interval is not a family at
  an interval anchor.**
- **Resolved** — the fourth is the trap, and the disposition for confusing it with the third is **Clarify**, not
  Refuse.
- **Failure** — none; a misreading is kind 4.

> **And "at a period" as an anchor is a *universe* question.** A world individuated by `{account, week}` has
> weeks as root points; that `week` is **not the same anchor** as a `week` reached by projection from days.
> Comparing them is universe passage.
>
> **Constraint honoured explicitly:** the order LAST requires is the **analytical point order**. It is unrelated
> to the proposed `{a*b}` coordinate/presentation precedence, which is not adopted and which — even if adopted —
> is not LAST/LAG/SCAN analytical order. Nothing here uses that syntax to solve a governed-order problem.

### V. Order, and more than one operand

#### Case 21 ⚡ — a noncommutative reducer, and the universe fact it turns out to need

```
family status_trace
  grounds    : at ledger.{account,day}, the account's status that day
  valued in  : List<StatusCode>                          -- point value: a singleton list
  composes   : fiber-reducing, CONCAT[ order = O ], over fibers varying only in { day }
```

CONCAT is **associative and noncommutative**. Built to test whether the clause model carries enough to stop a
wrong staging without a prohibition.

- **Constituted** — the citation, and the **order** as an identity-bearing law parameter.
- **Entailed** — **direct** composition `day → month` is fine. **Staged** composition `day → week → month`
  requires more, and this is new:

> **Staged agreement requires associativity. For a noncommutative law it additionally requires that the
> intermediate projection be *order-compatible* with the law's governed order** — each intermediate block
> order-convex, and the blocks themselves ordered. **Order-compatibility is a property of a governed projection
> against a governed order, so it is a *universe* fact** (§1.6), and it is new in this pass.

  Where it holds — contiguous calendar blocks — staging agrees with the direct answer. Where it does not — group
  the days by `day_type ∈ {weekday, weekend}`, a perfectly good partition that is wildly non-convex in
  chronological order — **staging silently produces a different list.** The engine must **decline to stage**.
- **Denoted** — `concat(status@{account,day}; order = O)`.
- **Resolved** — Serve by direct composition. Where only the staged basis is retained → **kind 6**, nameably: the
  intermediate is not order-compatible.
- **Failure** — none, and **no prohibition was needed.** The engine simply **lacks the theorem**. **Absence of a
  theorem, like absence of a clause, is absence of meaning.** SUM never notices, because commutativity makes
  every partition order-compatible vacuously.

#### Case 22 ⚡ — `net_change`: a noncommutative binary, with more than one operand — and the axis its parent cannot cross

```
family closing_balance   constructs : fiber-reducing, LAST[order=O],  of ( balance@{account,day} ), over {day}-varying
family opening_balance   constructs : fiber-reducing, FIRST[order=O], of ( balance@{account,day} ), over {day}-varying

family net_change
  constructs : co-located, DIFFERENCE, of ( minuend  = closing_balance ,
                                            subtrahend = opening_balance )
               co-participation : both established at the same point
  composes   : fiber-reducing, SUM, over ORDER-CONVEX, ORDER-ADJACENT fibers varying only in { day }
```

- **Constituted** — four facts, all genuinely contingent: the governed order; **which operand is the minuend**;
  the co-participation contract; and the SUM clause's **order-convexity scope**.
- **Entailed** —
  - **Operand role is identity-bearing.** DIFFERENCE is noncommutative, so `Σ(F)` carries roles, not a set of
    operands. **MEL must carry roles too.**
  - the co-located clause has **no** fiber-reducing behaviour of its own across accounts; the empty-fiber outcome
    comes from the witness monoids' \(\bot\), and the co-participation contract decides what a half-established
    pair does.
  - **and the finding:** net change over adjacent intervals **is additive** — `Δ(Jan) + Δ(Feb) = Δ(Jan∪Feb)` —
    so `net_change` may declare a fiber-reducing SUM clause over `{day}`-varying fibers, **scoped to order-convex
    order-adjacent fibers** (case 21's universe fact again).
- **Denoted** — `closing_balance − opening_balance`, with roles.
- **Resolved** — Serve. *"Change in balance"* over a non-contiguous selection → **Clarify**, not Refuse.
- **Failure** — none.

> ⚡ **This is the strongest single refutation of propagated prohibition in the suite.** Balance **cannot** cross
> `day` by SUM. `net_change` is built entirely out of Balance's measures, and it **composes across `day` by
> SUM** — because it is a different quantity with a different law. **The derived family composes across exactly
> the axis its parent does not.** Any mechanism that propagated a blocked axis from operand to result would
> refuse a correct, standard, everyday financial quantity; §1.5's separation is what makes it expressible.

#### Case 23 — AOV, `revenue / order_count`

- **Constituted** — **one fact: the co-participation contract.** Does the denominator count **every eligible
  order**, or **only orders carrying revenue**? Two lawful worlds, two different quantities. Operands must be
  *lawfully co-established under the applicable universe, type and co-participation contract*, and inference is
  foreclosed: *individually supported inputs drawn from incompatible populations do not form an admitted basis
  merely because their types match.*
- **Entailed** — **argument shape matters here.** AOV does **not** reduce a fiber; it consumes **co-located
  measures at the target anchor**. **AOV has no fiber-reducing clause at all**, which is why the child-state
  discipline is a theorem rather than a warning: a ratio of ratios is not the ratio of the totals, and the model
  cannot even write the wrong one. Result type Rational; **undefined where `order_count = 0`** — a value premise.
- **Denoted** — `revenue / order_count`, or the governed name resolving to it.
- **Resolved** — Serve. Without the contract → **kind 3**, and the refusal can **name** the missing fact.
- **Failure** — none, given the contract.

#### Case 24 — covariance, where a law parameter is a convention

```
family revenue_margin_covariance
  constructs : co-located, COVARIANCE[ ddof = 1 ], of ( revenue , margin ) formed at sales.{...,line}
               co-participation : the pair is established at the line, both eligible
```

- **Constituted** — two facts, both genuinely contingent: the **co-participation contract**, and **`ddof`** — a
  law parameter whose two values are two different quantities, which is why it belongs in the family's name.
- **Entailed** — the conservation rule bites here in a way it does not for AOV: a weighted statistic requires
  **pointwise** co-establishment, so the pair must exist at the same point, not merely in the same fiber. The
  sufficient-state basis follows from the law.
- **Denoted** — `covariance[ddof=1](revenue, margin)`.
- **Resolved** — Serve. *"Covariance"* with no convention stated → **Clarify**, never a default.
- **Failure** — none.

### Suite result

**Twenty-four cases, six built specifically to break the model. No case required a prohibition concept, and no
case required a family fact the model does not have.** Three cases produced genuinely new obligations, none of
them at the family layer:

| finding | where it lands |
|---|---|
| **measurement scale** (ratio / interval / ordinal / nominal) must be in the capability matrix, or meaningless sums are admitted (case 3) | **CDT** |
| **order-compatibility** of a governed projection with a governed order, required for staged agreement under a noncommutative law (cases 21, 22) | **universe** |
| **operand roles** must be carried, because some laws are noncommutative (case 22) | **MEL**, and \(\Sigma(F)\) |

**One case changed the model rather than confirming it** — case 7, which forced §1.5 — and it did so by finding a
real defect in an earlier draft's statement of case 9.

---

## 3. The disposition test

Each construct below was **tested, not assumed**. The test is the one Huayin set: *show the smallest example that
cannot be expressed correctly without it.* For each we state what it was for, the hardest case we could find for
its absence, and what actually happens there.

### 3.1 \(P_F\) / `prohibited_constituents` — **dies**

*For:* recording that \(F\) may not exist at anchors varying in some axis.
*Hardest case for its absence:* case 7 — a business that wants `balance @ week` to mean LAST and definitely not
a sum of daily balances.
*What happens:* nothing wrongly serves. **There is no bar to fail to cross**, because there is no SUM-over-`day`
clause and therefore no meaning to produce. A family declaring only a `last` clause cannot "serve `sum` because
nothing forbids it" — absence of a clause is absence of meaning, **necessarily**.
*And it could not have expressed the requirement anyway:* case 7's Balance holds **two verdicts about the one
axis `day`**, which an axis-indexed set cannot represent.

### 3.2 A stored or enumerated \(\mathcal A_F\) — **dies as a constituted fact**

*For:* answering *at which anchors does \(F\) stand?*
*Hardest case:* case 14 — currency in the value type. `{region}` **is** in the extension and **particular
region-points are undefined**.
*What happens:* **definedness is below anchor granularity, so no per-anchor object can carry it** — not for
constructed families and not for observational ones either.
*What survives:* \(\mathcal A_F\) as **notation for a derived predicate**. A materialized index of that predicate
is a legitimate *cache*, and a cache is not a constituted object: never authored, never a source of truth, and —
per §1.5's auditable form — **never consulted while deciding a construction**.

### 3.3 C3 family-domain standing — **dies**

*For:* giving the family domain the standing of a first-class declared contract.
*Hardest case:* any case where standing at \(A\) is a fact *about* \(F\) rather than a consequence of \(F\)'s
clauses. **The suite contains none.**
*What happens:* case 7 is decisive in the cleanest possible way — **standing changed because a clause was added,
not because a domain was edited.** Standing is always downstream. A declared domain would be a second place to
say the same thing, and the two could disagree.

### 3.4 `CONSTRUCTED_DOMAIN_UNDECIDED` — **dies**

*For:* a status for a constructed family whose domain cannot be computed.
*Hardest case:* a construction citing a **non-catalogued law** — the one genuinely open question in the model
(§6.4).
*What happens:* **an incomplete declaration must not mint a family with an undecided domain; it must fail to
constitute.** For a law not in the catalogue the author must supply its argument shape, scope, premises and
target — *the law itself*. Missing → the **declaration** is rejected, nameably, and **no family exists**. A
status that admits an under-specified family is a way of storing an unanswered question as data, where it will
later be read as an answer.

### 3.5 B-anchor / `BLOCKED` as family ontology — **dies, and cannot be repaired**

*For:* prohibiting a family from crossing an axis.
*Hardest cases:* three, and each kills it differently.

| case | what it shows |
|---|---|
| 8, 13, and *inventory-unit-days* | **what it rejected is a real, named, standard quantity** in three different domains. The only error was the label |
| 7 | one family, **two verdicts about one axis** — an axis-indexed set cannot hold them |
| 22 | a derived family **composes across exactly the axis its parent cannot** |

*Why repair fails:* to express case 7 it would have to be re-indexed by **law as well as axis** — at which point
it is \(\beta\), **capability-indexed by definition and never to be imported family-indexed** — and it is then
the clause list **with its sign flipped, and strictly worse**, because the negative form must be **complete over
every law** to mean anything at all. **Retiring it is not a simplification; it is the only way to say what the
business said.**

### 3.6 Family root as a separate object — **dies**

*For:* the anchor a family lives at, from which its reach is computed.
*Hardest case:* a family with **two grounding clauses at different granularities** — line-level revenue plus an
independently reported regional total. Even there, **each clause has its own anchor and there is no single
root**; what the two share is an agreement obligation, not a root.
*What happens:* **one anchor per clause suffices everywhere.** For observational families the "root" is just the
grounding clause's anchor; for constructed families there is nothing for it to be.

### 3.7 `formation.kind` — **dies**

*For:* declaring whether a family is observational or constructed.
*Hardest case:* none found.
*What happens:* it is **read off** — the presence of an observation clause. A declared kind is a second place to
say it, and the two could disagree.

### 3.8 Separate `domain` / `movement` declarations — **die as declaration fields**

*For:* two fields on a family declaration.
*What happens:* **`domain` is §3.2's notation** — a derived predicate, not a field. **`movement` is edge
validity**, \(\Gamma_F(B\to A)\): whether a *path* exists between two locations the family **already stands at**.
That is an **evidence-layer** fact, and per §1.5 it is consulted **only for ascriptions of \(F\), never for
constructions over \(F\)'s measures.** Neither is a constitutive field.

### 3.9 Stock / flow / semi-additive family kinds — **die**

*For:* a taxonomy predicting how a family composes.
*Hardest case:* case 15. Under currency-as-constituent, **Revenue's clause is Balance's shape** — a scope
excluding one constituent. The taxonomy is not even a difference of kind; **it is a quantifier.**
*And case 22 makes it self-contradictory:* `net_change` is a "flow" derived from a "stock" that **composes across
the stock's forbidden axis**. Any kind assigned to it would have to be contradicted immediately.
*Two authorities already refuse it on independent grounds* — *"No stock/flow/rating type"*, and *"It does not
need a separate folklore taxonomy such as 'additive metric,' 'semi-additive metric,' or 'non-additive metric.'"*

### 3.10 Reducer semantics originating in realization mappings — **die**

*For:* letting the backend operator map decide what a reducer means.
*Smallest example that kills it:* **one backend where `SUM` over an empty group yields `NULL`, and one where it
yields `0`.** If reducer semantics come from the mapping, **the same family means two different things depending
on where it is served** — which is the meaning/servability collapse, in its purest form.
*What happens instead:* the empty-fiber outcome is **entailed from the cited law's identity and eligibility**,
fixed at constitution, and **only for a *known*-empty fiber**. Realization is then **checked against the clause**.
A backend that cannot honour it is **kind 8, realization inadequacy** — never a redefinition. The same argument
covers null propagation, ordering, precision and overflow.

### 3.11 Two things that look like survivors and are not

**(a) *"A clause's scope is \(P_F\) in disguise."*** It is not, and there is a one-line test: **add a new law to
the catalogue.** A scope's meaning does not change — it was a positive quantifier on one claim, and it still
claims exactly what it claimed. **A prohibition set's meaning does change** — it silently becomes incomplete,
because it had been asserting something about every law including ones that did not exist yet. And case 7
separates them outright: one family, two scopes, one axis.

**(b) \(\Gamma\) / `blocked_edges`.** These survive, and they are **not on the list**. They are not ontology and
not a prohibition on meaning: they are **want of evidence about a refuted edge of \(F\)'s own path**, at the
evidence layer, consulted only for ascriptions of \(F\). **A refuted Balance edge must never reach
`sum(balance @ day) @ week`,** whose basis is Balance's *day* measures and which stands on its own.

### 3.12 Verdict

> **None of the ten survives. No smallest example was found for any of them.**

No object on that list is preserved because implementation currently has one.

---

## 4. Surviving counterexamples

**None.**

The closest the suite came is **case 3** — `sum(temperature @ day)`, which the model admits and which has no
meaning. We report it as a **bounded, located gap rather than a counterexample**, for a reason that matters: the
missing fact is **anchor-invariant**, failing at the constitutive anchor too, which is the signature of a
**type** fact and not a family fact. It therefore lands on **CDT's capability matrix as an open obligation**
(§1.7), and a family-indexed prohibition would have been the **wrong** repair — it would have blocked `sum` on
Temperature while leaving every other interval-scaled family untouched, because it is indexed on the family and
the defect is in the type.

Two further findings were produced and both were absorbed without new machinery: **order-compatibility** of a
projection with an order (a universe fact, cases 21–22) and **operand roles** (MEL and \(\Sigma(F)\), case 22).

---

## 5. The irreducible authored facts

### 5.1 An observational family — **five, plus a name**

| # | fact | why it cannot be derived |
|---|---|---|
| 1 | **the observation clause** — what quantity exists, at which points of which universe | the only irreducibly extra-formal fact in the system. Nothing entails what the world contains |
| 2 | **eligibility** — which points it applies to, **over eligible points** | otherwise known-empty and unknown are indistinguishable |
| 3 | **contribution multiplicity** — how many governed contributions sit at one point | analytical where contributions genuinely coincide; realization otherwise |
| 4 | **the governed value-type reference**, with any authored type parameter | an equality or collation profile is a real choice about the world, not about the carrier |
| 5 | **zero or more composition clauses** — law, identity-bearing parameters, scope, premises | *that this composition means anything* is the author's claim. **Zero is a perfectly good answer** |
| — | *canonical name and aliases* | naming, not constitution |

**Revenue and Balance are each exactly these five, three of them word-for-word identical, differing in one
sentence and one quantifier.**

### 5.2 A constructed family — **three to five, plus a name**

| # | fact | notes |
|---|---|---|
| 1 | **one or more construction clauses** — argument shape, cited law + identity-bearing parameters, **operands with their roles**, scope, premises | roles because some laws are noncommutative |
| 2 | **a co-participation contract**, where the clause has more than one operand | cases 22, 23, 24. Genuinely contingent every time |
| 3 | **a value-type reference**, *only* where the law does not determine the result domain | usually entailed |
| 4 | **zero or more further composition clauses of its own** | case 22 — and these may cover axes its operands' families do not |
| — | *canonical name; any governed equivalence to an existing family* | naming and resolution |

**What a constructed family does *not* author: no grounding clause, no eligibility (entailed from its operands
and its co-participation contract), no domain, no root, no kind.**

### 5.3 The whole of it, in one sentence

> **What a person must say is: what they observe, where, for which points, in what type, and how it composes.
> What they must not say is anything that follows from that.**

---

## 6. Consequences for the Manifold declaration model

**Stated as consequences, not as a proposal. No format is designed here.**

### 6.1 What a family declaration becomes

| today | under this contract |
|---|---|
| one `constitutive_anchor` per **family** | **one anchor per *clause*** — the family has no single anchor, and does not need one |
| `formation` with a `kind` | **no kind** — read off the presence of an observation clause |
| `continuation` declared for primitives, **entailed** for constructions | **a continuation *is* a fiber-reducing clause**, and **a constructed family may declare its own** (case 22). The asymmetry is wrong in exactly one direction |
| `prohibited_constituents`, `domain`, `movement` as body keys | **gone as constitutive fields**; `movement`'s content is evidence-layer edge validity |
| `participation` as one free-form slot | **two facts** — eligibility over *eligible* points, and contribution multiplicity |
| `contribution_structure` carried on `formation` | a **per-family** fact, not a property of how the family was formed |
| `value_domain { designation, equality }` | **already right** — this is §1.7's governed reference with an authored parameter |

### 6.2 The C1–C9 grid

| responsibility | disposition |
|---|---|
| **C1 target**, **C2 identity** | survive; identity now includes clause-level law parameters **and operand roles** |
| **C3 family domain** | **dissolves.** Its value was \(P_F\); the question it answered is entailed from clauses |
| **C3 edge validity** (\(\Gamma_F\)) | survives, **at the evidence layer**, for ascriptions of \(F\) only |
| **C4 formation** | **splits**: the clause absorbs the law citation, parameters, operands and shape; `kind` is entailed; `contribution_structure` moves to the family |
| **C5 participation** | survives, **as two facts** |
| **C6 semantic values** | survives, essentially unchanged |
| **C7 sufficient state** | survives, **establishment only, never standing** |
| **C8 continuation** | **is** a fiber-reducing clause — and is available to constructed families too |
| **C9 exceptional** | survives; its rule (*refuse a family that re-declares what the law entails*) generalizes to every entailed fact |

### 6.3 What moves out of the family entirely

**To the universe:** governed orders; projections and calendar relationships; placements **with their
multiplicity**; constituent identity and value domains; governed conversions; and — new in this pass —
**order-compatibility of a projection with an order**.
**To CDT:** equality and collation profiles; the capability matrix; and — new in this pass, as an open obligation
— **measurement scale**.
**To MEL:** argument shape and **operand roles**.
**To Frame-QL:** the nine failure kinds.

### 6.4 The one thing still genuinely open

**The law of a non-catalogued construction.** Case 23 shows the gap's exact shape: AOV has a co-located clause
and no fiber-reducing clause, and **nothing derives that from the ratio**. The missing constitutive act is the
law itself — its argument shape, scope, premises and target. **The model cannot entail a law it was not given and
must not be extended by guessing** (and see §3.4: the answer is to refuse the declaration, not to mint a family
with an undecided domain).

### 6.5 Two notes about the producer/consumer mismatch — **observations only, no repair**

1. The consolidated model **changes what a producer would be producing.** Repairing the current publication
   format to the current schema would be work done against a shape this contract retires.
2. Independently: **the concept pair is not symmetric today.** That is a fact about the current code, recorded and
   **not acted on**, per the stop gate.

---

## 7. Implementation concepts that would eventually need removal or reinterpretation

**A list, not a plan. Nothing here is scheduled, and nothing is being changed.** References are to
`packages/columna-core` and `packages/columna-platform`.

### 7.1 Would need removal

| concept | where it lives | why |
|---|---|---|
| **\(P_F\) / `prohibited_constituents`** | `governed/publication.py` (parser, `Family.prohibited_constituents`, `_FAMILY_KEYS`); `governed/native.py` (`FAMILY_BODY_KEYS`, `NON_IDENTITY_KEYS`); `governed/resolve.py` (→ the C3 standing); `platform/native_domain.py` (`prohibited`, `prohibited_constituents`) | §3.1 |
| **The C3 family-domain responsibility slot** | `governed/resolve.py` `C3_FAMILY_DOMAIN`; `platform/native_domain.py` `assert_within_domain`, `assert_request_within_domain` | §3.3. Note the *predicate* form is right; it is the **slot valued by \(P_F\)** that goes |
| **`CONSTRUCTED_DOMAIN_UNDECIDED`** | `platform/native_domain.py` — raised as `WantOfLaw` whenever `formation.kind != "primitive"` | §3.4, and see §7.4 — **this is the single most consequential item on the list** |
| **`MOVEMENT_STANDING_UNDECIDED`** | `platform/native_law.py` | the same pattern for \(\Gamma_F\): a held question stored as a family status |
| **`BAnchor` / `BLOCKED` / `blocked_lineages`** | `model.py` `BAnchor`; `parser.py` (the `BLOCKED { … }` grammar); `planner.py` (five enforcement sites); `disclosure.py` reason token `blocked_reduction`; the `.cml` demo corpora | §3.5 |
| **`outside_family_domain`** as a disposition | `disclosure.py`; `platform/serving.py` | §1.5's auditable form, in production: it is the *"check the request anchor against \(\mathcal A_F\)"* refusal |
| **`domain` / `movement` as declaration body keys** | `governed/publication.py` (`Family.domain`, `Family.movement`); `governed/resolve.py` `C3_DOMAIN_MOVEMENT`; `platform/serving.py` | §3.8. `movement`'s **content** survives as edge validity; the **field** does not |
| **`formation.kind`** | `governed/publication.py` `Formation.kind`, `PRIMITIVE`/`CONSTRUCTION`; `platform/native_domain.py` `family_is_primitive` | §3.7 — entailed |
| **`NO_CONTINUATION = "none"`** as a declarable value | `governed/foundation.py` | a declared *absence* is a negative declaration. Analytically, *explicitly no continuation clause* and *no continuation clause* are **the same fact**; the difference is whether the author has **ratified the silence**, which is assurance, not meaning |

### 7.2 Would need reinterpretation, not removal

| concept | current shape | under the contract |
|---|---|---|
| **`constitutive_anchor`** | one required field **per family** | **per clause.** The family has no single anchor |
| **`Formation`** | one object carrying `kind`, `law`, `operands`, `parameters`, `contribution_structure` | **splits**: law/operands/parameters/**roles**/shape → the clause; `kind` → entailed; `contribution_structure` → a per-family fact |
| **`participation`** (free-form slot) | one string | **two facts**, and eligibility must range over **eligible** points |
| **C8 `continuation`** | declared for primitives, **entailed** for constructions | a **fiber-reducing clause**, declarable by **either** — case 22 |
| **`Planner.blocked_edges`** | refuted-hierarchy edges → `contradicted_edge` | **survives unchanged** — but it must never be consulted while deciding a construction over \(F\)'s measures, and it needs a name that does not collide with `BAnchor` |

> ⚠ **A real vocabulary collision, worth fixing regardless of anything in this contract.** `BAnchor.blocked_lineages`
> (a declared operator prohibition, `.cml`-level, → `blocked_reduction`) and `Planner.blocked_edges` (refuted
> hierarchy edges, publish-time, → `contradicted_edge`) are **unrelated mechanisms sharing a word.** One dies and
> one survives, so the collision is actively misleading.

### 7.3 Already correct — keep, and generalize

Recorded because a removal list that does not say what is right is misleading.

- **The family domain is never stored.** `platform/native_domain.py` computes it as a set difference — *"never
  declared and never stored"* — and `governed/publication.py` states outright that \(P_F\) is *"a governed
  negative condition, not an enumeration of the family's domain."* **The code already refused to build the object
  §3.2 retires.**
- **Additivity is already operator-level, not family-level.** `operators.py` carries `is_monoid`, `linear`,
  `witness`, `re_entrant`, and a benchmark comment states it explicitly: *"Tier … is NOT declared here: it is
  operator-level, from the registry."* **There is no stock/flow taxonomy in the code at all** (§3.9) — it was
  only ever in prose.
- **`empty_fiber` is entailed from the law, and C9 refuses a family that re-declares it.** `foundation.py` and
  `governed/resolve.py`. **This is §1.8's rule, already implemented**, and it should be the template for every
  other entailed fact.
- **The realization's operator is a *claim checked against* the governed fact, not the source of it.**
  `platform/formation.py`. **This is §3.10's rule, already implemented** — and it is exactly what should be
  generalized to the places that still decide semantics downstream.
- **`value_domain { designation, equality }`** is §1.7's governed type reference with an authored parameter,
  already in the right place.

### 7.4 The two findings that matter most

1. **Every construction in the acceptance suite is refused by the current implementation.**
   `platform/native_domain.py` raises `CONSTRUCTED_DOMAIN_UNDECIDED` as `WantOfLaw` for **any** family whose
   `formation.kind != "primitive"` — with no default, no union and no propagation. Cases 8, 9, 10, 13, 16, 17,
   18, 22, 23 and 24 are all constructed. **The gap between the contract and the implementation is not a detail
   at the edges; it is the whole of family formation.** And the refusal is reported as **kind 3** when the true
   state is *the declaration is incomplete* — the wrong kind, too.

2. **Reducer semantics is decided in four places, and one of them is a SQL lambda.** The law layer
   (`foundation.py`) is right. But null handling is settled by the `deliver_sql` lambdas in `operators.py` —
   whose own comments record a real prior bug where passing the operand through made `count` skip nulls
   (observation count) rather than count rows. **That is §3.10's smallest example, already having happened in
   this codebase.** Under the contract the law fixes the meaning and the emitter is checked against it.

---

## 8. For the ToD successor-development journal

**Notes and candidates. Nothing here is adopted, and no authored theory document is edited.**

| entry | action | content |
|---|---|---|
| **A.1**, **A.2** — the family root and the generated Case-S domain; identity standing of the root and the domain | **WITHDRAW** | both objects disappear (§3.3, §3.6). A.1.8's *constructed-family propagation* question **dissolves rather than resolves** — there is no propagation relation to decide |
| **A.3** — family splitting, recovered from v6.1 | **ADOPT** | *"different analytical directions produce distinct family identities even when everyday language reuses one label"* is the published form of what cases 8, 13 and *inventory-unit-days* demonstrate |
| **A.4** — the determination-clause model | **DRAFT** | §1.2–§1.4, including scope/premise separated by decidability, *a premise may gate but not change*, and **operand roles** |
| **A.5** — the failure kinds | **DRAFT** | §1.10, now **nine**. Newly required beyond the earlier list: **geometry** as its own kind (cases 5, 11) and **ambiguity** as its own kind |
| **A.6** — family continuation is not family formation | **DRAFT** | §1.5, with the three monotonicity claims and the auditable negative form |
| **A.7 (new)** — staged agreement under a noncommutative law | **DRAFT** | §1.8: associativity is not sufficient; the intermediate projection must be **order-compatible** with the governed order, which is a **universe** fact. Where absent, only direct composition stands, and **the engine declines to stage** |
| **A.8 (new)** — meaning versus approximation | **DRAFT** | §1.9: *if the planner may choose the parameter, the meaning is the exact quantity; if the author supplies it, the parameter is part of the quantity* |
| **§4.1** — *"\(\mathcal A_F\) is not a proposed registry or new object"* | **CONFIRM, do not change** | vindicated, and the implementation already agreed (§7.3) |
| **§5.2** — *"compose across **admitted refinement**"* | **SUPPLY THE FILLER** | admitted **by a clause's scope**. The smallest theory change the model needs |
| **§7.2** — *"the family must resolve which order it uses"* | **CONFIRM** | entailed where the world admits one, authored where several |
| **§11.5.1** — canonicalization | **CONFIRM and lean on** | cases 1 and 10 are its two instances, and no other mechanism is needed |
| **§3.9** — succession on a changed identity-bearing definition | **OPEN A QUESTION** | is a **purely extension-widening clause addition** a succession or a refinement? \(\Sigma(F)\) changes and no determined value does (case 7). **Orthogonal to downstream inertness, which holds either way** |

**Referred outward, not to the journal:** **CDT** — measurement scale in the capability matrix (§1.7, case 3).
**Universe/Case-S** — order-compatibility of a governed projection with a governed order (§1.6, case 21).

**Not proposed, for the avoidance of doubt:** any restoration of \(\beta\) or \(\mathcal C_L\); any new
ontological kind; any resolution of the non-catalogued-construction question.

---

## Appendix S — supersession

What was believed along the way, and why it is no longer believed. **Nothing in the body depends on this
appendix.**

| hypothesis | status | retired by |
|---|---|---|
| a family has a **root anchor** \(A_0\) and a **reach** computed from it | **withdrawn** | one anchor per clause suffices; two grounding clauses have no single root (§3.6) |
| a family has a **domain** \(\mathcal A_F\) that is constituted, serialized or governed | **withdrawn** | definedness is **below anchor granularity** (case 14). Survives as notation for a derived predicate (§3.2) |
| \(P_F\) records which constituents a family may not forget | **withdrawn** | a negative encoding of a missing clause, at the wrong index (§3.1, §3.5) |
| a **B-anchor** records which axes a family may not cross | **withdrawn, and unrepairable** | one family, two verdicts about one axis (case 7); a derived family crossing its parent's axis (case 22); three real quantities mislabelled (cases 8, 13, inventory-unit-days) |
| constructed families have an **undecided domain** pending a propagation rule | **withdrawn — the question dissolves** | there is no propagation relation to decide. An incomplete declaration should fail to constitute (§3.4) |
| families have **kinds** — stock, flow, semi-additive | **withdrawn** | under one representation Revenue's clause **is** Balance's shape (case 15); `net_change` would contradict any kind assigned to it (case 22) |
| `formation.kind` is declared | **withdrawn** | entailed from the presence of an observation clause (§3.7) |
| `domain` and `movement` are declaration fields | **withdrawn** | notation, and evidence-layer edge validity (§3.8) |
| *"composition over fibers"* is the only non-observational shape | **superseded** | **three** argument shapes; cases 17 and 23 have co-located clauses and **no** fiber-reducing clause at all |
| participation is one fact | **superseded** | **two** — which points, and how many contributions at a point |
| the value-type reference is atomic | **superseded** | it carries **authored parameters** (equality profile; sketch precision) — cases 17, 18 |
| eligibility may range over observed points | **superseded** | it must range over **eligible** points, or known-empty and unknown fuse |
| a premise may carry a conversion | **superseded** | a premise may **gate** a clause, never **change** what it produces (case 16) |
| *"MEAN consumes its operand from the grounding clause, never a composition clause"* | **withdrawn** | the case-17/§1.5 defect — a true observation about one family mis-stated as a rule (case 9) |
| staged agreement follows from associativity alone | **superseded** | noncommutative laws additionally require an **order-compatible** projection (case 21) |

---

## 9. The deliverables, in one page

| asked for | answer | where |
|---|---|---|
| **the minimal semantic model** | **A family is constituted by determination clauses.** A clause is argument shape × source × operands-with-roles × scope × premises; plus three per-family facts — eligibility, contribution multiplicity, a governed value-type reference. **Family continuation is not family formation** | §1 |
| **acceptance-suite results** | **24 cases, 6 built to break it. All pass.** Three new obligations produced, **none at the family layer**: measurement scale → CDT; order-compatibility → universe; operand roles → MEL | §2 |
| **any surviving counterexample** | **None.** The closest, `sum(temperature@day)`, is a **type** fact — anchor-invariant — and lands in CDT. A family-indexed prohibition would have been the wrong repair | §4 |
| **irreducible authored facts** | **observational: five** (observation clause, eligibility, contribution multiplicity, value-type reference, zero-or-more composition clauses). **constructed: three to five**, and **no eligibility, no domain, no root, no kind** | §5 |
| **consequences for the Manifold declaration** | the anchor moves **per-clause**; C3 dissolves; C4 splits; C8 becomes a clause available to constructed families too; C5 becomes two facts; C6/C7/C9 survive | §6 |
| **implementation concepts needing removal or reinterpretation** | **nine to remove, five to reinterpret, five already correct.** The two that matter: `CONSTRUCTED_DOMAIN_UNDECIDED` refuses **every construction in the suite**, and reducer semantics is settled in a SQL lambda | §7 |
| **for the ToD journal** | withdraw A.1/A.2; adopt A.3; draft A.4–A.8 (**A.7 and A.8 are new**); confirm §4.1, §7.2, §11.5.1; supply §5.2's filler; open the §3.9 succession-versus-refinement question | §8 |

**The model survives.** The next decision is Huayin's: freeze the semantic contract and derive the Manifold
declaration from it, or not.

---

**Stopped here.** No implementation. No publication schema. No migration. No deletion of existing code. No repair
of the producer/consumer mismatch.

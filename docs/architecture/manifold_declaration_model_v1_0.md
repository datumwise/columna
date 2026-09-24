# The Manifold declaration model

**Derived from the frozen semantic contract.** Designed by Claude at Huayin's direction, 2026-09-24.

**Standing.** Design record. **No implementation, no code, no migration, no compatibility work.**

**The freeze.** [`columna_semantic_contract_v1_0.md`](./columna_semantic_contract_v1_0.md) is the semantic
contract for this unit, subject to the standing rule that a **genuine contradiction discovered downstream can
reopen it**. This document derives a representation from it and **does not reopen it**. Where the representation
exposed something the contract does not settle, it is reported in §7 and §8 rather than decided here.

**What this is not.** Not a semantic-design exercise. The question is narrow:

> **If this semantic contract were all we knew, what would a human need to declare in a Manifold, and what must
> instead be derived?**

Nothing below proceeds from the current publication schema, Core objects, the C1–C9 carriers, \(P_F\), B-anchors,
`formation.kind`, or compatibility. §9 looks at the current model **only after** the clean one is complete, and
only as migration evidence.

---

## 1. Method

Every candidate field was put through both of Huayin's tests, and **both had to pass**.

> **Necessity.** Remove this field. Is there now a pair of analytically different governed worlds the declaration
> can no longer distinguish?

> **Converse.** Can this field contradict something already entailed by the remaining declaration plus universal
> law? If yes, it is storing a consequence.

Every surviving field is classified as exactly one of:

| | class | meaning |
|---|---|---|
| **1** | **authored constitutive fact** | a contingent fact a human or governed source must establish |
| **2** | **nomological citation / parameter** | a reference to a universal law, plus its identity-bearing parameters |
| **3** | **derived consequence** | must not be independently authored |
| **4** | **naming / reference** | resolves something without constituting it |
| **5** | **assurance / evidence / realization** | therefore **not in the semantic Manifold declaration at all** |

---

## 2. The declaration model

### 2.1 What a Manifold contains

```
manifold
  ├── universe declarations        -- upstream; the contract places these outside the family (§1.6)
  ├── family declarations          -- THE SUBJECT OF THIS DOCUMENT
  └── equivalence declarations     -- class 4: naming and resolution, never constitution
```

> **The universe layer is shown only far enough to make the examples readable, and is not designed here.** It
> supplies individuation and `exists_when`, governed orders, governed projections, governed placements **with
> their multiplicity**, governed conversions, and order-compatibility. Held questions — Case G among them — stay
> held: see §4.13.

### 2.2 The family

> **A family declaration is a name and a list of clauses. There is nothing else in it.**

```
family <name>
  <clause>
  <clause>
  ...
```

Every fact the contract calls a per-family fact turned out to belong to **a clause**, not to the family — because
each of them is a fact about *how a value is determined*, and a family may determine values in more than one way
(§3.3). **The family itself carries no fields.**

### 2.3 The observation clause

```
observes  <universe>.<anchor>
          "<the grounding prose>"
          valued in   <type>[ <type parameters> ]
        [ for         <eligibility restriction> ]
        [ contributing many combined by <LAW> ]
```

| element | class | necessity | converse |
|---|---|---|---|
| `observes <universe>.<anchor>` | **1** | Revenue at `line` and Revenue at `order` are different quantities | cannot contradict — nothing else entails it |
| the grounding prose | **1** | two families identical in every formal respect — same anchor, same `Decimal`, same `SUM over *` — and one is Revenue and one is Cost | cannot contradict; **also cannot be canonicalized**, §7.2 |
| `valued in` | **1**, with **1** parameters | `Decimal` vs `Money` vs `Set<CustomerId>` are different worlds | cannot contradict on an observation clause |
| `for` | **1**, optional | a world where only interest-bearing accounts carry the quantity is analytically different | **must be absent when it equals the universe's `exists_when`** — §2.8 |
| `contributing` | **1**, optional, default `one` | holding the universe fixed: a line carrying two governed revenue recognitions is a different world | cannot contradict. **The most universe-sensitive field in the model** — §7.1 |

**`for` ranges over *eligible* points, never observed ones.** That is what makes a known-empty fiber
distinguishable from an unknown one, and it is the only reason the field exists.

### 2.4 The composition and construction clause

```
composes    <LAW>[ <law parameters> ]  over <scope>              -- operand is this family, implicitly
constructs  <LAW>[ <law parameters> ]  of ( <operand bindings> ) [ over <scope> ]
                                       [ co-participating <selector> ]
```

`composes` is sugar: *"`constructs LAW of (this family @ this family's constitutive anchor) over …`"*. The two
keywords exist only so a reader can see at a glance whether a clause continues the family or forms from
elsewhere; **they produce the same object**, which is what makes §2.5's guarantee possible.

| element | class | necessity | converse |
|---|---|---|---|
| `<LAW>` | **2** | SUM and MEAN over the same fiber are different quantities | cannot contradict |
| `[ <law parameters> ]` — `ddof`, `base`, `to`, `p` | **2** | `ddof=0` and `ddof=1` are different quantities, not different estimates | cannot contradict |
| `by <order>` — an order parameter | **2** | two governed day-orders give two different LASTs | **must be absent where the world admits exactly one order** — §2.8 |
| `of ( … )` operand bindings | **1** (the binding) over **2** (the roles) | AOV's operands are contingent; `numerator`/`denominator` are the law's | binding cannot contradict; **roles may not be invented**, they come from the law |
| `over <scope>` | **1** | **Revenue and Balance differ in this token and in nothing else** | cannot contradict |
| `co-participating` | **1** | case 23's two lawful worlds | cannot contradict |
| *a result type on a construction* | — | **fails both tests** — entailed from law × operand domains, and able to contradict them. **Not a field** | |

### 2.5 Operands, and why there are no anonymous intermediates

> **An operand is always a `<family> @ <anchor>` pair. It is never an inline expression.**

Forced by the contract: an operand is *a measure*, and a measure belongs to a family. An inline expression would
mint an anonymous family with no identity, no name and no lineage. Every intermediate therefore gets a name in
the Manifold. MEL may still *write* `mean(mean(balance@day)@week)@quarter`; resolution matches it against the
named families (§2.7).

> ⚡ **And this is where the contract's central separation becomes a property of the grammar rather than a rule
> anyone has to follow.** An operand reference names **a family and an anchor**. **There is no syntax for naming
> a clause.** A construction therefore *cannot* depend on which clause of \(F\) determined \(F@A\) — not by
> discipline, but because the declaration language has no term for it.
>
> Adding `composes LAST over { day }` to `family balance` adds **one line to one family** and cannot, as a matter
> of grammar, reach any declaration that names `balance @ …`.

### 2.6 Scope

> `over { c₁, …, cₙ }` — *over fibers that vary only in these constituents.*
> `over *` — *over any fiber.*
> `over { c₁, … } <qualifier>` — where a geometric qualifier is required (case 22).

**Scope is mandatory on every clause citing a reducer law. There is no default**, and that is deliberate: a
default of `over *` would mean an incomplete clause **silently claims the maximum**, which inverts the contract's
*absence of a clause is absence of meaning*. The maximum claim must always be typed out. (§8.1.)

Qualifiers are a **closed** vocabulary, decidable from geometry alone. The suite needs exactly one:
**`order-contiguous by <order>`** — the fiber's points are convex and adjacent in the governed order (case 22).
Its closure is unproven (§7.4).

### 2.7 Equivalence declarations

```
equivalence  <expression>  ≡  <family>
             justified by  <the clause that makes them agree>
```

Class **4**. Case 10's three claims stay separated **by the syntax**:

- **value agreement** is checked, not asserted — `justified by` names the clause, and the check is the contract's
  conditional entailment (same law, same identity-bearing parameters, same operand anchor, same eligibility and
  known-empty outcome, same value type);
- **canonicalization** is the authored part, and it is here;
- **identity is not minted** — this is a **separate top-level declaration**. It adds nothing to either family, so
  the constructed family keeps its own identity and its downstream lineage is untouched.

An equivalence with no `justified by`, or one whose cited clause does not agree, **is ill-formed**. Extensional
coincidence is not admissible as a justification, and there is no syntax to offer it.

### 2.8 The three standing rules

**R1 — Speak only where the world is silent.** *A declaration may not state a fact that the remaining declaration
plus universal law already entails.* Not "may omit" — **may not state**. A redundant field can only agree or
contradict, and agreeing teaches nothing while contradicting is a defect the system then has to adjudicate. This
generalizes the rule the codebase already applies to `empty_fiber`, and it is what keeps the declaration minimal
**by construction** rather than by discipline. It is the converse test, promoted to a well-formedness rule.

**R2 — Every clause is a positive claim.** There is no syntax for a negative one: no prohibition, no blocked
axis, no "does not compose", no explicit-none. **Silence is the only way to not claim something**, and it means
exactly one thing: this is not determined that way.

**R3 — Nothing in a family may refer to another family's clauses.** Operand references name a family and an
anchor. This is §2.5, stated as a rule so it can be checked.

### 2.9 The whole grammar

```
manifold        := universe* family* equivalence*

family          := "family" NAME clause+

clause          := observation | composition | construction

observation     := "observes" ANCHOR_REF STRING
                     "valued in" TYPE_REF
                     [ "for" ELIGIBILITY ]
                     [ "contributing many combined by" LAW_REF ]

composition     := "composes"   LAW_REF [ scope ]                       -- operand implicit: this family
construction    := "constructs" LAW_REF "of" "(" binding ("," binding)* ")"
                     [ scope ] [ "co-participating" SELECTOR ]

binding         := [ ROLE "=" ] NAME [ "@" ANCHOR_REF ]      -- anchor REQUIRED for a reducer law,
                                                             --        FORBIDDEN for a mapper (co-located)
scope           := "over" ( "*" | "{" CONSTITUENT,* "}" ) [ QUALIFIER ]
LAW_REF         := NAME [ "[" PARAM "=" VALUE,* "]" ] [ "by" ORDER_REF ]
TYPE_REF        := NAME [ "(" PARAM ":" VALUE,* ")" ]

equivalence     := "equivalence" EXPR "≡" NAME "justified by" CLAUSE_REF
```

**Ten productions. Nine authored positions.** The parser can enforce most of the contract structurally: `scope`
and the operand's `@ anchor` are *required* exactly when the cited law is a reducer and *forbidden* when it is a
mapper; `ROLE` is required exactly when the law declares asymmetric roles; `by` is forbidden where the world
admits one order (R1). **Four structural checks, all falling out of the law's own shape.**

---

## 3. Testing the clause quadruple

Huayin asked whether **argument shape × source × scope × premises** is actually sufficient as the family-law
surface. It is more than sufficient. **Two of the four are derived, and the declaration carries neither.**

### 3.1 Argument shape — **derived (class 3)**

The shape is not a fact about the family. **It is a fact about the cited law**: SUM, MEAN, UNION, LAST and CONCAT
are reducers; RATIO, CARDINALITY, CONVERT and DIFFERENCE-of-two-measures are mappers; the world is neither. ToD
names the distinction already — *mapper versus reducer*.

- **Necessity fails:** there is no law in the suite that can be cited in two shapes. Reducer-SUM and pointwise-ADD
  are **different laws**, not one law in two postures.
- **Converse succeeds:** an authored shape could disagree with the law's own, and then something must adjudicate.

**Removed.** It remains identity-bearing and MEL still carries it — *identity-bearing* and *authored* are
different things, and the extension is the standing example of the first without the second.

> **This places one requirement upstream: the law catalogue must be shape-typed.** It already is, in substance —
> and the payoff is that the grammar becomes self-checking (§2.9).

### 3.2 Premises — **derived (class 3)**

Every premise in the contract's twenty-four cases comes from one of exactly two places:

| premise in the contract | where it actually comes from |
|---|---|
| *"undefined where `order_count = 0`"* (case 23) | **the law's constructor domain** — RATIO's own partiality |
| *"empty fiber undefined"* (case 9) | **the law's constructor domain** — MEAN's nonempty constructor |
| *"given the fiber is currency-homogeneous"* (case 14) | **the value type's partiality** — `Money.+` is defined within a currency only |

- **Necessity fails:** removing the field loses nothing, because the type and the law already carry all three.
- **Converse succeeds, decisively:** an authored premise on case 14 would restate `Money`'s partiality — and could
  be written on a `Decimal` family where it is vacuous, or omitted on a `Money` family where it holds regardless.
  It can only be noise or contradiction.

**Removed. There is no authored premise anywhere in the acceptance suite.**

> **What would bring it back:** a premise that is neither the cited law's constructor domain nor the value type's
> partiality. We could not construct one. Recorded in §7.3 with what it would look like.
>
> **And the contract's *"a premise may gate but not change"* rule survives intact — it simply changes
> jurisdiction.** It is now a well-formedness rule on **CDT and the law catalogue**: an operation whose partiality
> changes the result's value domain may not be declared as partiality; it must be a separate law. That is a
> better place for it, because it is now checked once per law rather than once per author.

### 3.3 Source and scope — **both survive, and they are the whole surface**

**Source** is class 1 (the world, with its anchor and prose) or class 2 (a cited law with its parameters) plus
class 1 operand bindings. **Scope** is class 1 and is the single most load-bearing authored token in the model:
**Revenue and Balance differ in it and in nothing else.**

### 3.4 And the three per-family facts moved into clauses

Eligibility, contribution multiplicity and the value-type reference are all facts about **how a value is
determined at a point** — so they belong to the **observation clause**, not the family. The test that settles it:
a family with **two** grounding clauses at different granularities has **two** eligible point sets and possibly
two types. A per-family field could not hold them. **The family is left with no fields at all.**

### 3.5 The clause, as the representation actually needs it

> **clause = source (world | law + parameters + operand bindings) × scope**

with **shape** and **premises** entailed, and eligibility, multiplicity and type carried by the observation form
of *source*.

---

## 4. Worked Manifolds

The universe layer, shown only so the families read. **Not designed here.**

```
universe sales
  individuates { store, day, order, line }
  exists_when  "a line was transacted"
  order        day   chronological
  projects     { .., day } ⪰ { .., week } ⪰ { .., month }

universe ledger
  individuates { account, day }
  exists_when  "the account is open that day"
  order        day   chronological
  projects     { account, day } ⪰ { account, week } ⪰ { account, month }
```

### 4.1 Observational Revenue

```
family revenue
  observes  sales.{ store, day, order, line }
            "the consideration accruing from the line"
            valued in  Decimal
  composes  SUM  over *
```

`for` is absent, so eligibility **is** the universe's `exists_when` (R1). `contributing` is absent, so one
contribution per point. **Four authored facts and one law citation.**

### 4.2 Observational Balance

```
family balance
  observes  ledger.{ account, day }
            "the amount standing to the account at the close of the day"
            valued in  Decimal
  composes  SUM  over { account }
```

> **Revenue and Balance differ in the grounding prose and in one token: `*` versus `{ account }`.** That token is
> the entirety of semi-additivity, the stock/flow taxonomy, the B-anchor and \(P_F\).

### 4.3 Balance extended with the business definition

```
family balance
  observes  ledger.{ account, day }
            "the amount standing to the account at the close of the day"
            valued in  Decimal
  composes  SUM   over { account }
  composes  LAST  over { day }              -- NEW: "balance at the last day of the week"
```

**The whole change is one line.** `by ledger.day.chronological` is **absent and must be** — the world admits
exactly one governed order on `day`, so stating it would restate an entailment (R1).

> ⚡ **Continuation without formation, visible.** That line adds anchors at which Balance is determined. It cannot
> reach §4.4–§4.8, because those name `balance @ <anchor>` and **the grammar has no term for a clause**.

### 4.4 `mean(revenue @ sale)` — and the operand rule, in one line

```
family mean_order_revenue
  constructs  MEAN  of ( revenue @ sales.{ store, day, order } )  over *
```

> ⚡ **`revenue @ {store,day,order}` is *not* Revenue's grounding anchor** — Revenue is grounded at `line`. This
> operand is supplied by Revenue's **composition** clause. **This is the case-9 repair, in the representation:**
> a construction names `F @ A` and requires only that `F @ A` be determined. Had the model kept *"consumes the
> grounding clause, never a composition clause"*, this everyday family would be unwritable.

### 4.5 `mean(balance @ day)` · 4.6 `sum(balance @ day)` · 4.7 `last(balance @ day)`

```
family mean_daily_balance
  constructs  MEAN  of ( balance @ ledger.{ account, day } )  over *

family daily_balance_total
  constructs  SUM   of ( balance @ ledger.{ account, day } )  over *

family closing_balance
  constructs  LAST  of ( balance @ ledger.{ account, day } )  over { day }

equivalence  closing_balance  ≡  balance
             justified by  balance.composes[ LAST over { day } ]
```

**One line each.** The equivalence is a **separate declaration**: it adds nothing to either family, so
`closing_balance` keeps its identity and its downstream lineage, and it is checkable — same law, same (absent,
therefore identical) order, same operand anchor, same scope, same type. **Delete the equivalence and nothing
about either family changes.** Delete Balance's LAST clause and the equivalence becomes **ill-formed**, which is
the correct failure.

### 4.8 Nested mean-of-mean

```
family mean_weekly_mean_balance
  constructs  MEAN  of ( mean_daily_balance @ ledger.{ account, week } )  over *
```

> **Cases 11 and 12 are the same two declarations in two different worlds.** Whether this family is determined at
> `{account, quarter}` turns entirely on whether the universe supplies `{account,week} ⪰ {account,quarter}` — ISO
> weeks do not; a 4-4-5 retail calendar's quarters do. **Nothing in either family declaration differs between the
> two worlds, and there is no field in which it could.**

### 4.9 AOV — a genuine co-located multi-input construction

```
family order_count
  observes    sales.{ store, day, order }
              "one, for each order the business accepted"
              valued in  Decimal
  composes    SUM  over *

family average_order_value
  constructs  RATIO  of ( numerator = revenue , denominator = order_count )
              co-participating  eligible-intersection
```

Three structural facts, all enforced by the grammar rather than by discipline:

- **no `over`** — RATIO is a mapper, and scope is *forbidden* on a mapper. **So AOV has no fiber-reducing clause,
  and could not have one written by accident.** The child-state discipline becomes a parse-level fact.
- **no `@ anchor` on the operands** — for a mapper, the absent anchor *is* the meaning: co-located at the target.
- **roles are named**, because RATIO declares asymmetric roles. `COVARIANCE` declares symmetric ones and takes
  positional operands.

`co-participating` is **mandatory**, with no default. `eligible-intersection` and `defined-intersection` are
case 23's two lawful worlds; omitting it is want of law, and **the refusal can name the missing field**.

### 4.10 Currency: value semantics versus structural

```
-- (a) value semantics
family revenue
  observes  sales.{ store, day, order, line } "…"
            valued in  Money( amount: Decimal, currency: Currency )
  composes  SUM  over *
```

```
-- (b) structural
universe sales individuates { store, day, order, line, currency }        -- a UNIVERSE change

family revenue
  observes  sales.{ store, day, order, line, currency } "…"
            valued in  Decimal
  composes  SUM  over { store, day, order, line }
```

> **One token in `valued in`, one token in `over`, and one line in the universe.** Both are lawful and answer
> different questions; the declaration forces neither.
>
> **And there is no currency-homogeneity premise in (a).** `Money.+` is partial within a currency, so the family
> is determined at `{region}` and undefined at heterogeneous region-points **by entailment from the type** (§3.2).
> Writing the premise would restate CDT.

### 4.11 Ordered and non-ordered

```
-- non-ordered: SUM, UNION, MEAN, RATIO, COVARIANCE      -- no order term exists to write
-- ordered, one governed order:
family closing_balance
  constructs  LAST  of ( balance @ ledger.{ account, day } )  over { day }
                                                             -- `by` FORBIDDEN (R1)
-- ordered, two governed orders in the world:
family closing_balance
  constructs  LAST by ledger.day.value_date  of ( balance @ ledger.{ account, day } )  over { day }
                                                             -- `by` REQUIRED
```

> **The same field is forbidden in one world and required in another**, and R1 is what decides. This is the
> contract's *"entailed where the world admits one order, authored where several"* made structural: the author is
> never invited to restate the world, and never allowed to leave it ambiguous.

**And the noncommutative case**, which needs both a mapper clause and a reducer clause in one family:

```
family opening_balance
  constructs  FIRST of ( balance @ ledger.{ account, day } )  over { day }

family net_change
  constructs  DIFFERENCE  of ( minuend = closing_balance , subtrahend = opening_balance )
              co-participating  eligible-intersection
  composes    SUM  over { day }  order-contiguous
```

> ⚡ **Six lines, and the strongest claim in the contract is legible in them.** Balance **cannot** cross `day` by
> SUM (§4.2). `net_change` is built entirely from Balance's measures and **crosses `day` by SUM** — because it is
> a different quantity with a different law. Any mechanism that propagated a restriction from operand to result
> would make this declaration unwritable.

### 4.12 Known-empty versus unsupported evidence

```
family interest_accrual
  observes  ledger.{ account, day }
            "the interest accruing to the account that day"
            valued in  Decimal
            for        "accounts bearing interest"          -- an ELIGIBILITY restriction
  composes  SUM  over *
```

| situation | what the declaration says | outcome |
|---|---|---|
| a week whose account is **not interest-bearing** | **not eligible** — the `for` clause | **known-empty** → the monoid identity |
| a week whose account **is** interest-bearing and has no rows | eligible, unobserved | **unknown** → want of evidence |
| a week whose rows were **never loaded** | **nothing at all** | class 5 — no declaration surface exists |

> **One optional field carries the entire distinction, and the second half of it has no declaration surface by
> design.** That is why `for` must range over *eligible* points: made to range over observed ones, the first two
> rows collapse and known-empty becomes indistinguishable from unknown.

### 4.13 Case G — where the declaration stops

```
family revenue
  ...
  composes  SUM  over *
```

`revenue @ { region }` is determined **iff** the universe supplies a governed placement `store → region` **that
is functional**. The family declaration above is **unchanged, and unchangeable**:

- there is **no field** in which a placement could be declared;
- there is **no field** in which *"region is admitted"* could be asserted;
- there is **no field** in which it could be refused.

> **The held Case-G question cannot be answered opportunistically, because the declaration language cannot
> express an answer to it.** And case 5 adds the sharper half: the placement's **multiplicity** decides whether
> there is a fiber at all — a many-to-many placement yields a **cover, not a partition** — and that too is a
> universe fact with no family surface.

---

## 5. The authored-versus-derived accounting

### 5.1 Every position in the declaration

| # | position | class | necessity test | converse test |
|---|---|---|---|---|
| 1 | `family <name>` | **4** | fails — two families with identical clauses are one quantity | n/a |
| 2 | `observes <universe>.<anchor>` | **1** | **passes** — Revenue at `line` ≠ Revenue at `order` | passes |
| 3 | the grounding prose | **1** | **passes** — Revenue and Cost can be formally identical | passes; **but is opaque**, §7.2 |
| 4 | `valued in <type>` | **1** | **passes** — `Decimal` / `Money` / `Set<…>` | passes |
| 5 | type parameters — `equality`, `p`, `hash` | **1** | **passes** — `Set<Text>` is not admitted from the bare spelling | passes |
| 6 | `for <eligibility>` | **1**, optional | **passes** — §4.12 | **forbidden when it equals `exists_when`** (R1) |
| 7 | `contributing many combined by <LAW>` | **1**, optional | **passes, holding the universe fixed** | passes. §7.1 |
| 8 | `<LAW>` citation | **2** | **passes** — SUM ≠ MEAN | passes |
| 9 | law parameters — `ddof`, `base`, `to` | **2** | **passes** — `ddof=0` ≠ `ddof=1` | passes |
| 10 | `by <order>` | **2** | **passes where the world admits several** | **forbidden where it admits one** (R1) |
| 11 | operand **bindings** | **1** | **passes** | passes |
| 12 | operand **roles** | **2** | **passes** — DIFFERENCE is noncommutative | **may not be invented** — they come from the law |
| 13 | `over <scope>` | **1** | **passes, maximally** — Revenue and Balance differ here and nowhere else | passes |
| 14 | scope qualifier — `order-contiguous` | **1** | **passes** — case 22 | passes. Closure unproven, §7.4 |
| 15 | `co-participating <selector>` | **1** | **passes** — case 23's two lawful worlds | passes |
| 16 | `equivalence … justified by …` | **4** | fails as constitution — **and that is the point** | **ill-formed if the cited clause does not agree** |

**Nine authored constitutive positions (class 1), four nomological (class 2), two naming (class 4).**

### 5.2 Everything that was tested and is **not** a field

| candidate | class | why it is not in the declaration |
|---|---|---|
| **argument shape** | **3** | a property of the cited law, not of the family (§3.1) |
| **premises** | **3** | the law's constructor domain × the type's partiality. **No authored instance in the suite** (§3.2) |
| **a result type on a construction** | **3** | entailed from law × operand domains, and able to contradict them |
| **the extension \(\mathcal A_F\)** | **3** | a derived predicate. **There is no syntax for it** |
| **observational-versus-constructed** | **3** | read off the presence of an `observes` clause |
| **the empty-fiber outcome** | **3** | the cited law's identity × eligibility |
| **sufficient-state basis** | **3** | the cited law. Establishment, never standing |
| **lineage** | **3** | the operand bindings already name it |
| **a family root / constitutive anchor** | **3** | each clause has an anchor; the family needs none |
| **any prohibition, blocked axis, or explicit-none** | — | **R2: the grammar has no negative form** |
| **coverage, support, carriers, plans, precision, ratification** | **5** | not in the semantic Manifold at all |
| **`WITHHOLD` and governance restriction** | **5** | governance. Meaning is untouched by it |

### 5.3 The size claim, concretely

| family | authored positions |
|---|---|
| **Revenue** (§4.1) | anchor · prose · type · law · scope = **5** |
| **Balance** (§4.2) | the same **5**, differing in the prose and in one token |
| **Balance extended** (§4.3) | **7** — one law, one scope more |
| **`mean(balance @ day)`** (§4.5) | law · operand binding · scope = **3** |
| **AOV** (§4.9) | law · two bindings · co-participation = **4** |

---

## 6. The twenty-four cases against the representation

| case | what the Manifold declares | result |
|---|---|---|
| 1 Revenue | §4.1 — five positions | ✅ |
| 2 Balance | §4.2 — the same five, one token different | ✅ |
| 3 temperature | `observes … valued in Decimal°C` · `composes MEAN over { day }`. `sum(temperature@day)` is a separate family, and **the declaration has no field that could stop it** | ✅ **correctly** — the gap is CDT's measurement-scale obligation, and giving the family a field for it would be the wrong repair |
| 4 `revenue @ region` | **nothing** (§4.13) | ✅ |
| 5 `revenue @ tag` | **nothing, and nothing writable** — a cover is not a partition, and there is no family surface for a placement's multiplicity | ✅ |
| 6 `balance @ week` before | **nothing** — Balance has no `{ day }` clause. **R2: silence is the only way to not claim it** | ✅ |
| 7 `balance @ week` declared | **one line** (§4.3) | ✅ |
| 8 `sum(balance@day)` | §4.6 — three positions | ✅ |
| 9 `mean(balance@day)` | §4.5 — three positions | ✅ |
| 10 `last(balance@day)` + equivalence | §4.7 — three positions plus a separate class-4 declaration | ✅ |
| 11 mean-of-mean, projection absent | §4.8 — **unchanged** | ✅ |
| 12 mean-of-mean, projection present | §4.8 — **the identical declaration** | ✅ **the same two families, two worlds, two verdicts** |
| 13 degree-days | `constructs DIFFERENCE[ base = 18°C ] of ( temperature )` · `composes SUM over *` | ✅ the base is a law parameter, so 18 °C and 65 °F are different families by construction |
| 14 currency as value | §4.10(a) — **and no premise** | ✅ |
| 15 currency as constituent | §4.10(b) — one token, one universe line | ✅ |
| 16 conversion | `constructs CONVERT[ to = USD ] of ( revenue )` · `composes SUM over *` | ✅ — see §8.7 on the second clause |
| 17 set + cardinality | `valued in Set<CustomerId>( equality: … )` · `composes UNION over *`; then `constructs CARDINALITY of ( distinct_customers )` **with no scope** | ✅ **the scalar cannot compose, structurally** — scope is forbidden on a mapper |
| 18 sketch | (a) nothing new; (b) `valued in HLLSketch( p: 14, hash: H )` · `composes MERGE over *` | ✅ **§1.9's test becomes structural: a planner cannot choose a value that appears in the declaration** |
| 19 Timestamp | `valued in Timestamp`. A family citing SUM over it **fails to typecheck against CDT at declaration time** | ✅ anchor-invariant, as required |
| 20 interval-valued | `valued in Interval`. **There is no anchor syntax for "at an interval"** | ✅ the fourth object cannot be mistyped as the third |
| 21 CONCAT | `valued in List<StatusCode>` · `composes CONCAT over { day }`. **No field mentions staging**, so no author can authorize a wrong one | ✅ |
| 22 net_change | §4.11 — six lines, two clause shapes in one family | ✅ **crosses the axis its operand's family cannot** |
| 23 AOV | §4.9 — no scope, no operand anchors, named roles, mandatory co-participation | ✅ |
| 24 covariance | `constructs COVARIANCE[ ddof = 1 ] of ( revenue, margin ) co-participating eligible-intersection` — positional, because COVARIANCE's roles are symmetric | ✅ |

**Twenty-four of twenty-four are representable.** Nine of them require the Manifold to say **nothing at all**, or
nothing beyond what an earlier family already said.

---

## 7. Facts in the contract that do not represent cleanly

**Reported, not repaired.**

### 7.1 Contribution multiplicity

`contributing many combined by <LAW>` is the **only** place where the observation clause — the one clause form
that should face the world and nothing else — carries a **law citation**. It also blurs §3.1: an observation
clause with a combining law has two sources.

Its necessity test passes **only while the universe is held fixed**. If a line genuinely carries two governed
revenue recognitions, one may either (a) declare `contributing many combined by SUM`, or (b) **individuate the
recognition in the universe**, after which multiplicity is `one` and an ordinary fiber-reducing clause carries
the rest. **(b) removes the field entirely.**

**Both readings are available and this document does not choose.** The field is retained, conservatively,
because the contract retains it and the contract is frozen. **It is the field we would most like to challenge.**

### 7.2 The grounding prose

Identity-bearing, opaque, and **not canonicalizable** — the contract's own open item. The representation can only
carry it as an authored string, which means any textual edit is conservatively a re-ratification. **An accepted
cost, not a defect**, but it is the one authored position the model cannot check.

### 7.3 A value-restricted population

Case 23's second world is colloquially *"only orders carrying revenue."* The representation offers
`defined-intersection`, which covers *orders where revenue is **defined***. It has **no way to express** *orders
where revenue is **nonzero*** — a value condition on a population.

That would have been a **premise**, and §3.2 removed premises after finding no authored instance. **This is the
one place where a premise would have had work to do**, and it is also the contract's own open item — *eligibility
is a bound, jointly determined with the resolved request; where request-local restriction becomes target change
is unsettled.* **The two questions are the same question**, which is worth recording: resolving the request-local
restriction question would also decide whether the premise slot comes back.

### 7.4 Scope qualifier closure

The suite requires exactly one qualifier, `order-contiguous`. **We have no argument that the vocabulary is
closed**, and an open-ended qualifier language would reintroduce the escape hatch the contract's premise rule was
written to prevent.

### 7.5 A family with two observation clauses at different anchors

The contract permits it and no case forces it. If it existed, a composition clause would have to say **which
anchor it reduces from**, and the grammar has no term for that. **Not exercised, and therefore not designed.**

### 7.6 The law of a non-catalogued construction

The grammar has `LAW_REF` and **no production for defining a law.** That is the contract's open question showing
up as a missing production, and it is the correct place for it to stop: **the declaration language cannot invent
a law, which is exactly the contract's instruction.**

---

## 8. Where representation forced a choice the contract did not make

**Each is a decision this document made. None is offered as a semantic finding.**

1. **`over` is mandatory, with no default.** A default of `over *` would let an incomplete clause silently claim
   the maximum, inverting *absence of a clause is absence of meaning*. The contract rules on silence *between*
   clauses and is silent on silence *inside* one.
2. **`co-participating` is mandatory, with no default.** The contract calls MAP1 *a conservative default*. **The
   representation declines to have one**, because case 23's two readings are different quantities and a default
   would pick one silently. This makes some declarations that the contract would admit **ill-formed**.
3. **No anonymous operands.** Every intermediate is a named family. Forced by *an operand is a measure and a
   measure belongs to a family*, but the contract never says it.
4. **No support-based co-participation selector.** Forbidden so that evidence cannot enter a population. Forced
   by the meaning/servability distinction — but the contract never says the selector vocabulary is closed.
5. **Two requirements pushed upstream.** The **law catalogue must be shape-typed** (§3.1), and **CDT must carry
   the partiality that used to be written as premises** (§3.2). Neither is a new semantic claim; both are now
   load-bearing in a way the contract did not spell out.
6. **R1 makes a redundant-but-agreeing declaration *ill-formed*, not merely pointless.** The contract does not
   rule on redundancy. This is the strongest of the six choices and the one most worth challenging: it is what
   makes minimality structural rather than stylistic.
7. **Case 16's `ENTAILED: USD is homogeneous` is read as applying to the *premise*, not to the clause.** Read the
   other way it would mean a clause can be entailed, which contradicts case 1's *that additive composition means
   anything is the author's contingent claim*. **The representation takes the first reading and does not repair
   the annotation.** Under §3.2 the two readings coincide in effect, because the premise is derived either way —
   which is why this is a note rather than a contradiction.

> **No contradiction in the frozen contract was found.** §8.7 is the only place where a contract annotation
> admits two readings, and the readings agree in outcome.

---

## 9. Comparison with the current model

**Only now, and only as migration evidence.** Nothing here is a plan.

| current concept | disposition |
|---|---|
| `prohibited_constituents` (\(P_F\)) | **disappears** — R2 gives the grammar no negative form |
| `BAnchor` / `BLOCKED { … }` in the `.cml` grammar | **disappears** — same |
| `CONSTRUCTED_DOMAIN_UNDECIDED`, `MOVEMENT_STANDING_UNDECIDED` | **disappear** — a held question has no declaration surface; an incomplete declaration fails to parse |
| `formation.kind` (`primitive` / `construction`) | **disappears** — read off the presence of `observes` |
| `domain`, `movement` body keys | **disappear as fields**; `movement`'s content **moves** to the evidence layer |
| `Family.constitutive_anchor` (one per family) | **moves** — onto the `observes` clause, one per clause |
| `Formation` (one object: kind, law, operands, parameters, contribution_structure) | **splits** — law/parameters/operands/roles → the clause; `kind` → derived; `contribution_structure` → the `observes` clause |
| `participation` (one free-form slot) | **splits** — `for` (eligibility) and `contributing` (multiplicity), on the `observes` clause |
| C8 `continuation` — declared for primitives, entailed for constructions | **survives, symmetric** — `composes` is available to **any** family (§4.11's `net_change`) |
| C6 `value_domain { designation, equality }` | **survives**, as `valued in TYPE( params )` |
| C7 sufficient state | **survives as derived** — no declaration surface |
| C9 *"refuse a family that re-declares what the law entails"* | **survives and generalizes** — it becomes **R1**, applied to every field rather than to `empty_fiber` alone |
| `Planner.blocked_edges` | **survives, untouched** — evidence layer, and it was never a declaration field |
| `operators.py` `is_monoid` / `linear` / `witness` / `needs_order` | **survives, and becomes load-bearing** — this is the shape-typed catalogue §3.1 requires |
| `deliver_sql` lambdas deciding null handling | **moves** — to *checked against the clause*, per the pattern `formation.py` already uses |
| the `.cml` `FAMILY { sum BLOCKED { calendar } }` surface | **requires migration** — and it is a **narrowing**: several current declarations say things the new grammar cannot express, which is the intended direction |

**What would require genuine migration judgement, as opposed to deletion:** (i) every existing `participation`
string must be split into an eligibility and a multiplicity; (ii) every `BLOCKED` set must be re-expressed as the
**absence** of a clause, which means deciding, per family, which clauses it actually has; (iii) every constructed
family currently refused by `CONSTRUCTED_DOMAIN_UNDECIDED` must be **written for the first time** — there is no
existing declaration to convert.

---

**Stopped at the design gate.** No implementation, no code, no schema, no migration.

# The smallest semantic Manifold declaration

**Revenue and Balance from first principles, then six constructions.** Recorded by Claude at Huayin's
direction, 2026-09-24.

**Standing.** Semantic model only. **No YAML/JSON, no publication classes, no C5 or producer repair.** Stops
after the model and the examples, and reports where minimality fails.

**The ruthless test, applied to every field:**

> **Remove it.** If the analytical meaning is still uniquely determined from the remaining governed premises
> plus universal law, **the field should not be authored.**
> **Converse:** if two analytically different worlds can satisfy everything that remains, the missing fact is
> **genuinely constitutive** and needs a governed home.

**Result up front.** The irreducible declaration is **five facts**. Revenue and Balance differ in **two of
them**, and one of those two is a single quantifier. Of the six constructions, **four cost nothing**, one costs
a world fact, and one costs a single family fact.

---

## 1. What a declaration is, after the archaeology

A family law is a **partial function from a fiber of participating contributions to a value**. Governed geometry
supplies the fibers; the law says what it makes of them. A declaration therefore states **clauses**, and there
are only two kinds:

| clause | what it does | irreducibly |
|---|---|---|
| **grounding** | says what the quantity *is* at a point of its constitutive anchor | **extra-formal** — this is where meaning enters the system from the world |
| **composition** | says what the quantity is over a fiber, by citing a law and naming the fibers it is claimed over | formal — a cited law plus a scope |

**Absence of a composition clause is not a prohibition.** It means the quantity is stated at its anchor and
nowhere else. Two states, positive, no polarity apparatus:

\[ \mathcal A_F=\{A: F@A \text{ is defined by the law of } F\} \]

— **descriptive notation for the extension of a partial law, never an authored object.**

---

## 2. The two declarations

```
universe sales
  individuates : { store, day, order, line }
  exists_when  : a line was transacted

universe ledger
  individuates : { account, day }
  exists_when  : the account is open on that day          -- generative
```

```
family revenue
  at            : sales.{ store, day, order, line }
  observes      : the consideration accruing from the line
  participates  : every eligible point of that anchor, once
  valued in     : CDT Decimal, in a governed currency
  composes      : SUM over ANY fiber
```

```
family balance
  at            : ledger.{ account, day }
  observes      : the amount standing to the account at the close of the day
  participates  : every eligible point of that anchor, once
  valued in     : CDT Decimal, in a governed currency
  composes      : SUM over fibers varying only in { account }
```

> **Five facts each. Identical shape. Three fields are word-for-word identical. They differ in the `observes`
> prose and in one quantifier of `composes`.**

That single quantifier is the whole of what used to be called semi-additivity, the stock/flow taxonomy, the
B-anchor, and \(P_F\).

---

## 3. Field-by-field classification, with the ruthless test

| field | class | remove it → | verdict |
|---|---|---|---|
| **`at`** | **governed reference** to independently constituted structure — the anchor is *proved* from the universe constitution, never claimed — **but which anchor is contingent** | the law has no argument; and revenue-per-line vs revenue-per-order are different quantities | **KEEP** |
| **`observes`** | **contingent fact Manifold must constitute** | two worlds satisfy everything else: one where the number is consideration, one where it is units | **KEEP** |
| **`participates`** | **contingent** (factorable to a governed default — MA §22, *"permitted only when the governed profile determines one lawful interpretation"*) | ToD §11.5.1's published 100-vs-97 | **KEEP** |
| **`valued in`** | **governed reference** to a CDT type; **which** type is contingent | Decimal and Float are different worlds — *"Operation availability is not algebraic adequacy"* | **KEEP** |
| **`composes`** (law + scope) | **contingent** | **Revenue and Balance become the same declaration** | **KEEP** |
| ~~universe~~ | **governed reference, carried by `at`** | nothing — Ruling 2026-09-14: *"F already determines its governed universe… The universe is a precondition of resolution, not a component of the identity that resolution produces."* | **ELIMINATED** |
| ~~value capabilities~~ (`+`, `=`, `0`) | **consequence** — CDT's §10 matrix supplies them from the cited type | nothing | **ELIMINATED** |
| ~~result value domain~~ | **consequence** — cited law × operand domain | nothing | **ELIMINATED** |
| ~~additivity flag~~ | **consequence** — it *is* `composes` | nothing | **ELIMINATED** |
| ~~stock / flow / semi-additive kind~~ | **consequence** — refused independently by ADR-036 D6 and CDT v0.5 (*"a separate folklore taxonomy"*) | nothing | **ELIMINATED** |
| ~~\(\mathcal A_F\) / admitted anchors~~ | **consequence** — the extension of the partial law | nothing | **ELIMINATED** |
| ~~\(P_F\) / prohibited constituents~~ | **consequence** — *absence of a clause*, stated negatively at the wrong index | nothing | **ELIMINATED** |
| ~~continuation law as a separate field~~ | **merged** — it is `composes` | nothing | **ELIMINATED** |
| ~~lineage~~ | **consequence** — an observational family has none; a construction's is its expression | nothing | **ELIMINATED** |
| ~~empty-fiber value~~ | **consequence of `composes` + `participates`** — see §5.1 | nothing, **provided `participates` is stated over *eligible* points** | **ELIMINATED, conditionally** |
| ~~path agreement, basis, adequacy~~ | **consequence** — Props 6.1/6.2, ToD Appendix A | nothing | **ELIMINATED** |
| canonical name, aliases | **naming only** | the family survives unnamed — §11.1 of Frame-QL: a canonical construction *"can be an identity-bearing reference even before a separate human-readable name is assigned"* | **not constitutive** |
| `WITHHOLD` | **governance/policy, not analytical meaning** | the meaning is unchanged; only serving is | **excluded from the law** |
| support, coverage, availability, bindings, plans, carriers, precision | **realization/evidence** | — | **excluded from Manifold** |

### 3.1 The converse test, applied to the two differing fields

**`observes`.** Two worlds, identical in the other four fields, differing only here: one where `balance` is the
closing amount, one where it is the *average* amount over the day. Same anchor, same participation, same type,
same composition scope. **Different quantities.** Genuinely constitutive. ✓

**`composes` scope.** Two worlds, identical in the other four: one where a set of accounts has a balance equal
to the sum of theirs, one where it does not (mixed currencies, asset/liability signs, intercompany positions
requiring elimination). **Both are lawful worlds and the model must not choose.** Genuinely constitutive. ✓

---

## 4. The six constructions

Each asks only: **what does this cost the Manifold, beyond what is already declared?**

### 4.1 `sum(revenue @ sale)` — **cost: zero, and it is not a new family**

The SUM law's clause is *Σ over any fiber of the participating operand point-values*. Revenue's `composes` is
*SUM over ANY fiber*. **These are the same law over the same operand with the same participation.**

ToD §11.5.1 anticipates exactly this: *"A named family such as Revenue may already denote the same construction;
canonicalization can identify them only where identity and participation agree."* Here they agree.

> **So this is a canonicalization question, not a construction** — and Frame-QL §3.1's insistence that
> `revenue @ {region}` *"does not need to become `sum(revenue @ {transaction}) @ {region}`"* is the same fact
> from the request side.

**And the general rule falls out with no taxonomy:**

> **`sum(X@I)` is a *new* family exactly when `X`'s own law lacks a Σ-over-those-fibers clause.**

For Revenue it is Revenue. For Balance over a *day*-varying fiber it is **a different family** — which is
precisely ToD v6.1's *"different analytical directions… produce distinct family identities even when everyday
language reuses one label."* The stock/flow phenomenon, with no stock/flow concept anywhere.

### 4.2 `mean(revenue @ sale)` — **cost: zero**

Law cited. Operand established by `observes`. Participation entailed — §11.5.1: *"`count(x@I)` counts
participation under the operand construction's governed rule."* Value requirements `+` and `÷`: Decimal supplies
`+`; **exact division is not closed in Decimal** (*"`1 / 3` is not a finite decimal"*), and CDT's matrix says the
exact quotient *"embeds to `Rational`"*.

> **The result value domain is `Rational`, and it is entailed, not authored.** A concrete demonstration that a
> "consequence" really is derivable — and CDT adds that presenting it as Decimal is *"a separate governed
> conversion"*, i.e. Frame-QL's, not the Manifold's.

Empty fiber: MEAN's clause is over *nonempty* fibers, so **undefined** there — a consequence of the cited law.

### 4.3 `mean(balance @ day)` — **cost: zero**

Law cited. Operand established at `{account, day}` by Balance's **grounding** clause — MEAN consumes point
values, **not** Balance's composition. Participation entailed. Values ✓.

> **MEAN's clause is over *any nonempty fiber*, so it stands at `{account}`, `{day}` and `{}` — entirely
> independently of Balance's composition scope, because it never uses it.** The result the whole thread was
> chasing, now with no domain object, no propagation, and nothing authored.

### 4.4 `last(balance @ day)` — **cost: one world fact, and conditionally one family fact**

LAST's clause is *over any nonempty fiber carrying a governed complete order on points, the value at the
order-greatest participating point.* The order is **not** in the world yet.

| | |
|---|---|
| **world fact, contingent** | a **governed complete order on the `day` constituent**. §7.3 refuses substitutes: *"Appending a storage identifier or relying on sort stability is not a repair of analytical law."* |
| **family fact** | **which** order — §7.2, *"the family must resolve which one it uses"*, identity-bearing. **Entailed where the world admits exactly one; authored where it admits several.** |
| **consequence** | the witness family \(W\), the basis \(\{W\}\to L\), the witness monoid, the known-empty state \(\bot\) — all §8.1-8.3, none authored |

Note the payoff: `last(balance@day)` stands at `{account}`, `{day}`, `{}` — **a wider extension than Balance
itself** — because the witness monoid composes where Balance's `composes` does not. Nothing propagated; nothing
was blocked.

### 4.5 `mean(mean(balance @ day) @ week)` — **cost: zero family facts; one world fact, shared**

Inner \(M_1\) is 4.3. \(M_1@\{account,week\}\) requires a **governed projection**
\(\{account,day\}\succeq\{account,week\}\) — a world fact, and the same one anything asking \(M_1\) at week
needs. Outer MEAN: operand established, participation entailed from \(M_1\)'s, values `Rational` which supplies
`+` and `÷`.

> **No new ontological mechanism at the second level** — the same two clause kinds, one level up. The recursion
> is the strongest evidence the shape is right.

And the `@ month` question is unchanged and geometric: if the governed Week refines the governed Month the
geometric obstacle is absent and other premises may still decide; if it does not, ordinary Week→Month projection
cannot establish it.

### 4.6 AOV — **cost: exactly one family fact**

```
family average_order_value
  law : revenue / order_count            -- a nominated defining construction, §3.7
  co-participates : <contract>           -- *** the one additional fact ***
```

where `order_count` is `count(sales.{store, day, order})` — itself zero-cost.

**The contingent fact.** §3.5 requires operands *"lawfully co-established under the applicable universe, type,
and **co-participation contract**"*, and gives the reason it cannot be inferred: *"Equal coordinate spelling
alone does not establish all these premises."* Concretely: **does the denominator count every eligible order, or
only orders carrying revenue?** An order with no revenue line and a revenue line on a cancelled order are both
real, and the readings give different quantities. §5.3 forecloses the repair: *"Individually supported inputs
drawn from incompatible populations do not form an admitted basis merely because their types match."*

**Converse test:** remove it and two analytically different worlds satisfy everything else. **Genuinely
constitutive.** ✓

**Consequences, not authored:** result type `Rational`; undefined where `order_count = 0` (CDT's premise field
`P`); and the child-state discipline — states \((100,1)\) and \((300,2)\) combine to \(400/3\), *"not the
unweighted mean \(125\) of the displayed child ratios"* — which follows from §5.1 anchor-locality.

### 4.7 The scoreboard

| construction | additional Manifold facts |
|---|---|
| `sum(revenue @ sale)` | **0** — and it is Revenue, by canonicalization |
| `mean(revenue @ sale)` | **0** |
| `mean(balance @ day)` | **0** |
| `last(balance @ day)` | **1 world** (a governed order) + **0 or 1 family** (which order) |
| `mean(mean(balance@day)@week)` | **0 family**; 1 world fact (a projection), shared |
| AOV | **1 family** (co-participation) |

> **Cost is incurred by observing a quantity, by ordering a constituent, by relating two constituents, and by
> combining two operands. It is *not* incurred by constructing.** Constructions acquire their meaning from
> their cited laws, exactly as predicted.

---

## 5. Where the minimality test fails, and where two meanings remain

Reported rather than resolved, as instructed. Five findings; two are genuine gaps.

### 5.1 The elimination of the empty-fiber field is **conditional**, and the condition is load-bearing

I removed `empty-fiber value` as a consequence of `composes` + `participates`. **That holds only if
`participates` ranges over *eligible* points, not *supported* ones.** ToD §6.1:

> The identity \(e_G\) applies to a **known empty contribution fiber**. It is **not** a substitute for an
> unknown domain, unsupported placement, or unavailable value.

If participation were stated as *"the points at which a value is present"*, known-empty and unknown become
indistinguishable and the empty case needs its own field again. So the minimality result depends on a
constraint the exercise discovered rather than assumed:

> **`participates` must be a rule over eligible points — a law fact — and must not be stated over supported
> points, which is an evidence fact.** ToD §2.3's four standings are what make the elimination possible.

This is a design constraint, not a failure. But it is the kind of constraint that is silently violated by any
authoring surface that lets an author point at data.

### 5.2 `composes` needs a **premise**, not only a scope — a required generality

Balance composes over fibers varying in `{account}`. Now take a world individuated by
`{account, day, currency}`. Balance cannot add across currencies **unless a governed conversion is supplied** —
so the honest clause is *"composes over `{account}`; and over `{currency}` **given** a governed conversion."*

**A bare scope-set cannot express a conditional scope.** CDT already has the right shape — its capability tuple
carries a premise contract \(P\) as a first-class field, *"not a Boolean flag saying that an operation exists"* —
and the same field would carry §1.3's per-point definedness (`Timestamp + Timestamp`, zero denominators,
irrational roots) uniformly.

> **Required generality: a composition clause is (cited law × fiber scope × premise), not (law × scope).**
> This is an extension of the model, discovered by pushing on a third constituent, and it is not optional.

### 5.3 The grounding clause is irreducibly extra-formal — a verification limit, not a minimality failure

`observes` is prose. It is where meaning enters the system from the world, and nothing can derive it. So *"the
meaning is uniquely determined"* is always relative to a human reading of one sentence.

This does **not** make `composes` derivable-in-principle-but-stored-in-practice — §3.1's converse test shows the
composition scope is a **separate semantic claim** (a set of accounts having a balance is not implied by an
account having one). Both fields survive on semantic grounds.

What it does mean is that **a gate can check consistency between `observes` and `composes` only with a human in
the loop**, and that an inconsistency between them is a well-formedness defect no machine will catch.

### 5.4 **Genuine gap:** identity determination has no stable handle on the grounding clause

Two families may share `at`, `participates`, `valued in` and `composes`, and differ only in `observes`. That is
the *normal* case — `revenue` and `units` at the same anchor. So **`observes` is necessarily identity-bearing.**

But `observes` is prose. Re-wording it without changing its meaning must **not** mint a successor; changing its
meaning while keeping the wording **must**. §3.9 governs the requirement — *"a change of constitutive order,
participation, or formation cannot be concealed by retaining the old label"* — and the model supplies no
mechanism.

> **This is the `family_id` generation question, already recorded as open, arriving from a new direction: the
> identity determinant now contains exactly one component that cannot be canonicalized.** Conservative
> re-ratification on any textual change is the obvious answer, and it is the same trade Ruling 8 accepted for
> constituent renames — *"That costs one human confirmation. The opposite error… is a publication that claims a
> human ratified a world he never saw."*

### 5.5 **Genuine gap:** `participates` is a bound, not the whole fact

ToD §4.2 makes participation **jointly** determined:

> Participation is selected by **the law and the resolved request**; it is not automatically the set of
> surviving physical records or supported operand values.
>
> A request-local restriction need not create a new named family or universe. **But any restriction that changes
> the analytical target must remain explicit** in the resolved definition, request, or lineage as its law
> requires.

So the declaration's `participates` states a rule the request may restrict *within*, and some restrictions
change the target. **Where the boundary lies — which request-local restrictions stay inside the family and which
mint a different target — is not settled by anything in this model**, and it is adjacent to the
family-construction question of §6.

### 5.6 Two genuinely different meanings remain — and this one is *not* a gap

*"Average revenue per order"* denotes at least three lawful, identity-distinct things:

```
mean(revenue @ {store,day,order,line})     the mean line value
sum(revenue @ line) / count(order)          revenue per order, all eligible orders
average_order_value                          the governed family, under its co-participation contract
```

All three are declarable, all three are denotable in MEL, and they give different numbers. **This is a Frame-QL
`Clarify`, not a missing Manifold fact** — and it is worth naming because it is the case that most *looks* like a
declaration gap and is not. The old instinct was to resolve it by prohibiting two of the three.

---

## 6. What this leaves

**The model does become small.** Five facts per observational family; three of Revenue's and Balance's five are
identical; the difference between a flow and a stock is **one quantifier in one clause**. Four of six
constructions cost nothing, and the two that cost something cost exactly the contingent premise their cited law
cannot entail — a governed order, and a co-participation contract. **Constructions acquire their meaning from
their laws, as predicted.**

**Two required repairs to the model as stated:** composition clauses need premises (§5.2), and `participates`
must range over eligible points (§5.1).

**Two genuine gaps, both pre-existing and both now better located:** identity determination over a prose
grounding clause (§5.4 — the open `family_id` question), and the boundary between request-local restriction and
target change (§5.5).

**And the two hard questions, in the broadened form:**

1. **Given a lawful construction over existing measures, what law does the resulting family have?** §4 answers
   it for six cases by citing catalogued laws. It does not answer it for a construction whose law is *not*
   catalogued — an arbitrary ratio, difference, or composed expression. This is the genuine family-construction
   /law-synthesis question, and §4.1's rule — *`sum(X@I)` is a new family exactly when `X`'s law lacks that
   clause* — is a fragment of the answer, not the answer.
2. **Once analytical meaning is established, what may prevent serving it?** `WITHHOLD`, coverage permission and
   authorization, sorted without being allowed to redefine meaning.

**Stopped here, as instructed:** no serialization, no publication classes, no C5 or producer repair.

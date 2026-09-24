# Stress-testing the semantic model: value types, anchor semantics, and what BLOCKED was

Recorded by Claude at Huayin's direction, 2026-09-24.

**Standing.** Semantic report. **No Manifold redesign, no C3/`P_F` repair, no fields, no implementation work.**

**The hypothesis under test:**

> A family law determines what quantity exists and what arguments it can meaningfully consume. An analytical
> expression may construct a different family from an existing family without moving or propagating the operand
> family. Evidence/realization determines whether the lawful argument is available. Governance prohibition is a
> separate question again.

**Headline: the hypothesis survives all three dimensions, it is under-specified in two places, one of my own
earlier answers was wrong — and the estate had the decisive fact right years ago and then lost it.**

> **The legacy B-anchor was indexed by `(operator × lineage)`. `prohibited_constituents` is indexed by
> `(family × constituent)`. The capability index was dropped, and that single deletion is the whole of the
> constructed-family-domain problem.** §3.5.

- Dimension 1 forces distinctions the hypothesis does not make. Its clause *"what arguments it can meaningfully
  consume"* is **four** gates, not one — law-to-type adequacy, governed type coverage, law determination over
  the fiber, and per-point definedness (§1.3). The first two are decided **before any anchor is examined**;
  `mean(text @ day)` fails at every anchor including its own, while `balance @ week` fails at one.
- One of those gates is **neither a law fact nor an evidence fact but a function of both** — per-point
  definedness under a partial operation. **No declaration can carry it**, which is an independent argument
  against any per-anchor domain object: it would be at the wrong granularity even for observational families.
- **Seven dispositions survive, none collapsing**: the four above, plus want of state, realization, and
  governance. The hypothesis as stated names four.
- Dimension 2 **corrects my previous answer.** I said `balance @ {account}` is undetermined. That was true only
  of one candidate Balance law. Under a different, equally lawful Balance law it is determined and means *the
  current balance*. **Which law is the case is the author's contingent choice, and nothing else decides it.**

---

## Part 1 · Different semantic value types

### 1.1 The distinction dimension 1 forces

Two failures that the previous exercises would both have called *want_of_law* are **structurally different**:

| | `mean(text @ day)` | `balance @ week` |
|---|---|---|
| what fails | the MEAN law requires `+` and `÷`; the operand's value domain supplies neither | Balance's law has no clause over fibers varying in `day` |
| **anchor-relative?** | **no** — fails at every anchor, including the constitutive one | **yes** — succeeds at `{account,day}`, fails at `{account,week}` |
| when it is detected | at **formation**, before any current anchor is considered | at **ascription**, against a particular anchor |
| what it is a fact about | the **operand's value domain** versus the **law's requirements** | the **law's clauses** |

ToD puts the first in its own jurisdiction — §5.7:

> A law may require addition, division, equality, value comparison, set or multiset union, a point reference,
> or a structured value. **ToD states those semantic requirements. A concrete type specification determines
> which value domains supply them.**

And §4 requires *"the operations **and equality laws** they require"* — so a domain that supplies a `+` symbol
without the commutative-monoid laws a construction needs has **not** satisfied the requirement. Notation is not
capability.

> **So there are gates *before* any anchor is examined at all: is this law applicable to this operand at all,
> and only then does this law determine a value over this fiber?** `mean(text@day)` never reaches the second
> question. **This is achieved with no admitted-anchor registry and no family prohibition** — which was the
> thing to demonstrate. §1.3 shows the pre-anchor side is itself two gates, not one.

### 1.2 The cases

Each row: value domain · family law · is `F@A` determined · is a proposed operation defined on the value ·
sufficient state/evidence · realization.

---

**(a) `revenue` — ordinary exact numeric.**
Value: an amount in a governed currency; supplies `+`, `=`, `0` with monoid laws. Law: *over any fiber, the
additive composition of participating contributions.* Determined at every anchor reached by projection.
Operations: `sum`, `mean`, `count`, `min`/`max`, `multiset` all defined. Evidence: ordinary support. Realization:
the 2026-09-12 ruling governs — *"A governed exact-decimal domain must be carried exactly where the current
substrate can carry it exactly"*; a float carrier is a **realization** defect, not a law defect.

**(b) `balance` — point-in-time stock. The decisive control.**
Value: **identical to Revenue's.** Law: see Part 2 — the contrast is entirely in the law.

> **Revenue and Balance share a value domain and differ only in their law.** Dimension 1's own strongest result
> is a negative one: **value semantics does not determine the family law, and cannot.** Any model that read
> additivity off the type would make these two the same quantity.

**(c) counts — integer.**
Value: integer; `+` with monoid laws. But ToD §11.5.1 makes `count(I)` and `count(x@I)` **distinct targets** —
*"`count(x@I)` counts participation under the operand construction's governed rule"* — and §5.2 shows the same
*value* carries two different **roles**:

> For COUNT, two retained count states \(37\) and \(12\) can combine to \(49\) under count-state continuation.
> Counting the two scalar values as new observations gives \(2\). **The distinction is the analytical role of
> the inputs, not their integer type.**

MA states the consequence as *"`count(37)` counts one new value"*. **Second independence result: the value type
does not determine the role; the law does.**

**(d) set-valued — `distinct_set(x@I)`.**
Value: a set under governed element equality (§11.5.3: *"Concrete set types and equality capabilities belong to
the semantic type specification"*). Law: *over any fiber, the union of participating element identities* —
fiber-form, so determined everywhere. Operations defined on it: `cardinality` (giving `count_distinct`).
**Not** defined on it: `mean`, `sum` — so `mean(distinct_set(x@I))` fails **gate one**. And §11.5.3 notes the
asymmetry that matters: *"The cardinality generally does not retain enough information to determine overlap
during later union"* — the scalar is sufficient-for-nothing-further, which is an **evidence/reuse** fact, not a
domain fact.

**(e) sketch / HLL — and it is *not a CDT type at all*. This exposes a gate I had not separated.**

⟨measured⟩ **`HLL`, `t-digest`, sketch types, `Struct`, `Map`, vectors, `witness`, and units/currency are all
absent from the CDT kernel** — listed among *"The kernel does not yet define"* (CDT v0.5 §12). So the case is
not "a rich value type with a merge law"; it is a law ToD can name and CDT does not supply. CDT says so, and
this is the single most important quote for the jurisdiction question (v0.5:838):

> A ToD law may name or analyze a sufficient-state family whose concrete value type is not yet part of this
> kernel. That does not silently extend Columna Data Types. … **ToD may define analytical standing before this
> type kernel supplies an implementation capability; CDT coverage is explicit, never inferred from ToD catalog
> membership.**

MA says the same from its own side: *"A valid Measure Algebra law may exist before any engine implements it. …
A missing implementation is a realization gap. It does not make the analytical expression meaningless."*

> **So there is a gate distinct from law-to-type adequacy: the law is analytically admitted, the value domain it
> needs is coherent, and *no governed type supplies it yet*.** That is **want of type coverage** — adjacent to
> realization, **not** a want of law. Calling it want_of_law would say a lawful quantity does not exist.

The same shape recurs across the statistical catalogue, where CDT's verdict is *"Not as a total exact kernel
capability"* for **`stddev`, `rms`, `skewness`, Pearson `correlation`** (square root is not closed in
`Rational`) and for **geometric mean** (*"No total exact `Log`/`Exp` capability is supplied by the kernel"*).
These laws are admitted; exact standing exists *"only on a law-declared subdomain whose result is exactly
representable"*. **Admitted, and exactly realizable only in part of its own domain** — see (h).

And the parameter point survives: a sketch law would need a governed precision, and CDT's general rule tells us
where that parameter lives (v0.5:770-774): *"**If changing the parameter can change the governed value or the
result of a governed operation, the parameter belongs to semantic type standing.**"*

**(f) structured sufficient state `(sum, count)` — and it is *not* a value.**
This one refutes a tempting reading. `(sum,count)` is **not a family with a pair-valued domain**. ToD §5.1:
*"The tuple notation records input roles; **it does not require a separate composite-state object**."* MA §14.5
is blunter:

> The state relationship \(S_{mean}=S_{sum}\times S_{count}\) does not imply the MEL identity
> \(mean(m)=\frac{sum(m)}{count(m)}\). … **Composite sufficient state does not imply composite measure
> identity.**

> **The line: a rich VALUE (set, multiset, sketch, witness) is one family. A role-indexed TUPLE is several
> families.** §5.6 confirms the first — *"These are ordinary families with rich semantic values, not a separate
> layer of analytical state"* — and §5.7 the boundary: *"Internal value structure is not analytical location."*
> A set's elements do not become dimensions; a witness's point reference does not become a second anchor.

**Third independence result: value structure is not anchor structure.**

**(g) text / categorical — and CDT is stricter than I assumed.**

⟨measured⟩ **CDT defines no `enum` and no `categorical` type**; the only occurrence of "category" is a *denial*
(v0.5:578): *"A text collation, semantic version ordering, category ranking, or business priority order is **not
inferred** from the existence of a raw value type."*

`Text[p]` is parameterised by a **governed profile**, and without one the refusals are broader than I claimed:

> `Text` therefore does not receive one universal analytical equality merely because an implementation can
> compare byte strings or Unicode code points. … Consequently, **`Set<Text>` and `distinct_set` over text are
> not admitted merely from the bare spelling `Text`. They require a declared exact text-equality profile.
> Without one, equality-dependent set/distinct operations are refused** rather than silently inheriting
> storage-engine collation semantics.

So per law, on text:

| law | on `Text[p]` | why |
|---|---|---|
| `count(x@I)` | defined | participation only; *"participation standing belongs to the analytical law"* |
| `distinct_set`, `multiset` | **only with a declared equality profile**, else **refused** | v0.5:325-333, §10 row 787 |
| `last(text@I)` / `first` | **defined** | needs an order on **points**, not on values |
| `min(text@I)` / `max` | **only with a declared collation** | *"no intrinsic order … explicit order may be added separately"* |
| `mean`, `sum` | **never** | no `+`, no `÷` |

> **Correction to my own claim:** I said equality-only laws are "defined on text". They are defined **only under
> a governed equality profile**, and refused without one. So gate one is not type-versus-law — it is **(the
> law's required capabilities) versus (what the type supplies *under its governed profile*)**, and the profile
> is itself an authored fact.

The central demonstration still holds, and now with a second axis: **`last(text @ day) @ week` is lawful with no
profile at all, while `mean(text @ day)` is never lawful and `distinct_set(text @ day)` is lawful only with a
declared equality profile.** One operand, one geometry, three different answers, decided entirely by what each
law requires. And the two orders stay apart — SER:166: *"The required ordering is over the value domain. These
quantile constructions do not depend on an order of analytical input points."*

**(h) the cases that materially challenge the hypothesis — *partial* operations.**

My earlier draft used currency-scoped addition. ⟨measured⟩ **that example is not in the corpus** — units and
currency are on CDT's deferral list, and mixed-scale decimal is resolved the *opposite* way (*"representation
scale alone does not distinguish values"*). Withdrawn. CDT supplies three better-grounded forms of partiality.

**(h1) A two-sorted domain where `+` is admitted only on *unlike* pairs.** CDT v0.5:381-390:

> The temporal structure is **affine rather than additive**. In particular:
> ```text
> Timestamp - Timestamp -> Duration
> Timestamp + Duration  -> Timestamp
> Timestamp + Timestamp -> undefined
> ```
> These rules are **capability restrictions, not syntactic conventions**. A timestamp cannot enter an additive
> analytical family merely because its carrier is numerically encoded.

**(h2) A premise on the operand *value*.** Division carries *"nonzero divisor"* as a domain premise; CDT makes
the premise contract `P` a first-class field of a capability, *"not a Boolean flag saying that an operation
exists."*

**(h3) Exactness available on only part of the domain.** *"`Rational` is not closed under square root; exact
standing is available only on a law-declared subdomain whose result is exactly representable."*

Now trace `stddev` at a point whose variance is irrational:

1. **Law-to-type adequacy — passes.** The law's capability requirements are coherent.
2. **Law determination over the fiber — passes.** The clause is quantified over any fiber.
3. **And the *exact* result is not available at that point.**

This is neither want of law nor want of state, and §9.4 forbids papering over it: *"A disclosure can state a
limitation on an otherwise established, correctly described result. It cannot make arbitrary point selection
determinate."*

> **This gate is a function of the value domain's partiality AND the actual operand values. It is neither a law
> fact nor an evidence fact, and it is *per point*, not per anchor.**
>
> **No declaration can carry it — which is an independent argument against any per-anchor domain object, since
> the object would be at the wrong granularity even for observational families.**

And the deepest form of the same point, which is CDT's own maxim and the best single sentence for gate one
(v0.5:313-319):

> > **Operation availability is not algebraic adequacy.**
>
> Ordinary floating addition is an operation, but because rounding makes it **non-associative**, it does not by
> itself satisfy the exact associative-addition capability required by an exact additive family under arbitrary
> lawful regrouping.

**Float is the limit case: a type that supplies `+` and is still not admissible for an exactly-additive
family.** Notation is not capability — and ToD §4 already required *"the operations **and equality laws** they
require"*.

### 1.3 What Part 1 establishes

**Four independence results, each with a corpus witness:**

1. **Value semantics ⟂ family law.** Revenue and Balance share a value domain and differ only in their law. Any
   model reading additivity off a type makes them one quantity.
2. **Value type ⟂ analytical role.** Counts: *"The distinction is the analytical role of the inputs, not their
   integer type."*
3. **Value structure ⟂ anchor structure.** ToD §5.7 *"Internal value structure is not analytical location"*;
   CDT v0.5:439 *"Tuple positions are not anchors or analytical dimensions"*; and `(sum,count)` is **roles, not
   a value** — *"Composite sufficient state does not imply composite measure identity."*
4. **Operation ⟂ capability.** *"Operation availability is not algebraic adequacy."*

**And the hypothesis is under-specified: the meaning/capability side needs four gates, not one.**

| gate | question | anchor-relative? | witness |
|---|---|---|---|
| **G1 · law-to-type adequacy** | does the operand's type, under its governed profile, supply the capabilities *and laws* this law requires? | **no** | `mean(text@day)`; exact-additive over `Float`; `distinct_set(text)` with no equality profile |
| **G2 · governed type coverage** | is a governed value domain admitted for what the law needs? | **no** | sketch-valued families; exact `stddev` — CDT v0.5:838 |
| **G3 · law determination over the fiber** | does the law have a clause over *these* fibers? | **yes** | `balance @ week` |
| **G4 · per-point definedness** | is the clause's result defined at *this* point? | per **point** | `Timestamp+Timestamp`; zero denominator; irrational root |

G1 and G2 are decided **before any anchor is examined**; G3 is anchor-relative; G4 is below anchor granularity
altogether. Then **evidence (want of state)**, **realization**, and **governance** follow. **Seven distinct
dispositions, none collapsing into another**, and the hypothesis as stated names four of them.

**A recorded jurisdictional disagreement**, per instruction. CDT v0.5:576 says *"Ordering of **values** is
separate from ordering of **anchor points**. Columna Data Types governs the former. **Frame-QL or another
request language governs the latter.**"* But ToD §7 governs the analytical point order that **constitutes an
ordered family**, and §7.2 makes it identity-bearing. CDT has assigned to the request layer a fact ToD places in
family identity. The *distinction* is right and agreed; **the attribution of the second half is not.** Not
resolved here.

---

## Part 2 · Different anchor and temporal semantics

### 2.1 Could `balance @ week` mean *at the close of the week*? — Yes, and this corrects me

**Yes.** And the consequence is larger than the question suggests. Consider two Balance laws over **identical
geometry**:

```
LAW-P  (point clause)
  at ANY point p of {account, day}:
      balance(p) = the amount standing to p.account at the close of p.day

LAW-C  (closing-instant clause)
  over ANY fiber D with a governed order having a maximum:
      balance(D) = the amount standing at the close of the LATEST instant in D
```

| request | under LAW-P | under LAW-C |
|---|---|---|
| `balance @ {account, day}` | determined | determined (the fiber is a singleton) |
| `balance @ {account, week}` | **undetermined** | **determined** — the closing balance of the week |
| `balance @ {account}` | **undetermined** | **determined** — *the current balance* |

> **My previous answer — that `balance @ {account}` is undetermined — was true only under LAW-P.** Under LAW-C
> it is determined, and it names a real business quantity: the account's current balance. **Nothing but the
> author's choice of law decides between them.**

This *strengthens* the hypothesis rather than weakening it: the same name, the same value domain and the same
geometry yield different determinations, and **the law is the only thing that differs.** It also shows that
"Balance cannot cross time" was never a fact about Balance — it was a fact about LAW-P.

**And LAW-C is extensionally equal to a different family.** `balance@{account,week}` under LAW-C and
`last(balance@day)@{account,week}` return the same value. They are **not the same analytical object**: §2.2 —
*"Equal present values do not establish equal analytical identities"* — and identifying them needs a governed
equivalence (§3.9), not an observation that the numbers match.

**Answering the question directly:** we are dealing with **different family laws over the same geometry**, not
different anchor types. The geometry is one partition lattice. What varies is which clause the law states and
what structure that clause requires of the fiber.

### 2.2 The three clause-forms — this is what "temporal semantics" actually is

Every law in the corpus consumes its fiber in one of three ways:

| clause-form | defined on | needs | examples |
|---|---|---|---|
| **at-a-point** | singleton fibers only | nothing | observational `balance` under LAW-P; a raw observation |
| **over-the-fiber** | any (nonempty) fiber | the value operations the composition needs | `revenue`, `sum`, `mean`, `count`, `distinct_set`, `multiset`, `min`/`max` |
| **at-a-distinguished-member** | fibers with a governed order and an extremum | an order **on points** (§7) | `first`/`last`; Balance under LAW-C |

> **"Period" is not an anchor type.** An anchor is a governed partition, full stop. A *period-like* anchor is one
> whose fibers carry an order with extrema — and that order is **additional governed structure**, not part of
> the anchor. ToD §2.3 says so: *"An anchor by itself does not determine a traversal order. A family requiring
> analytical-point order must bind to additional governed structure."* And §7.2 keeps the choice open: *"Different
> order definitions over the same anchor may coexist; the family must resolve which one it uses."*

So three separable things, which the phrase "temporal semantics" has been fusing:

1. **the anchor** — a partition (geometry);
2. **an order on its points** — additional governed structure, optional, possibly several;
3. **the clause-form** — how the law consumes a fiber, possibly exploiting (2).

### 2.3 Interval semantics: three different claims, as suspected

*"At an interval"*, *"over the members of an interval"*, and *"at the end of an interval"* are **three different
analytical claims**, and they are exactly the three clause-forms applied to an order-interval fiber:

| phrasing | clause-form | example |
|---|---|---|
| *at* the interval | **at-a-point** — treats the interval as one atomic point | a weekly observation in a world individuated by `{account, week}`: a genuinely different universe, not a coarsening |
| *over the members of* the interval | **over-the-fiber** | `mean(balance@day)@week`, `sum(revenue@day)@week` |
| *at the end of* the interval | **at-a-distinguished-member** | `last(balance@day)@week`; `balance@week` under LAW-C |

The first is the one that hides. **A world individuated by `{account, week}` is a different universe from one
individuated by `{account, day}`** — its root points are weeks, and a "week" there is not a fiber of anything.
Anchor identity is universe-relative (Ruling 2026-09-14), so the two `week`s are not one anchor, and comparing
them is universe passage, not refinement. Identical calendar vocabulary, different analytical objects.

### 2.4 The four-way Balance contrast

Assume `{account}` exists and the projection is lawful.

| expression | quantity | law's argument | determined? |
|---|---|---|---|
| `balance @ {account}` | **depends on Balance's law** | — | LAW-P: **no**. LAW-C: **yes** — current balance |
| `sum(balance @ {account,day}) @ {account}` | the additive total of that account's daily balances | any fiber; needs `+` | **yes** |
| `last(balance @ {account,day}) @ {account}` | the latest daily balance | fiber + order | **yes** |
| `mean(balance @ {account,day}) @ {account}` | the average daily balance | any nonempty fiber; needs `+`,`÷` | **yes** |

**Does any law require Balance's inability to stand at `{account}` to propagate into the constructed three?
No — and there is no formalism in which the question can be posed.** Each construction consumes
`balance @ {account,day}`, at **singleton fibers**, where Balance's law is determined under *either* LAW-P or
LAW-C. The operand is never asked for a value at `{account}`. **The premise the constructions need is discharged
at the constitutive anchor and nowhere else.**

**And `sum(balance@day)` is not meaningless.** It must be split four ways, as instructed:

| claim | verdict |
|---|---|
| formally constructible | **yes** — `+` is available, the fiber is finite |
| analytically constituted as a family | **yes**, if an author states it; its law is complete and its target is *the additive total of daily balances*, which is a perfectly definite quantity |
| what a user usually wants | **usually no** — which is a **request** fact |
| ambiguous as a request | *"total balance for the account"* → **Clarify**: this, or LAW-C's current balance? |
| available from evidence | separate; §5.5 |
| prohibited by governance | only if some authority says so — see Part 3 |
| supported by implementation | separate |

> **"Not the business quantity anyone wanted" is a Clarify, not a law defect.** Collapsing it into a prohibition
> is how a policy preference became an ontological object.

---

## Part 3 · What the historical B-anchor / BLOCKED mechanism was representing

### 3.1 The decisive fact: β is indexed by the **capability**, not by the family

This is the finding of the whole exercise, and it is verifiable in one line of MA rev1 §3.2. The RED1 reduction
rule's side conditions are:

\[ Spent(q)\cap\beta(\kappa)=\varnothing, \qquad h\in\gamma(\kappa) \]

with, immediately above, *"capability \(\kappa\) accepts \(X\)"*, and immediately below:

> **Type compatibility is therefore necessary but not sufficient. Movement law and coverage permission are
> separate premises.**

\(\beta\) is **applied to \(\kappa\)**. It is a function from a **capability** — the reducer being applied — to
the set of distinctions that capability may not spend. So the fact β encodes is:

> **"You may not SUM *this quantity* across *the time distinction*."**

It is **not**:

> ~~"This quantity may not stand at a location where the time distinction is gone."~~

### 3.2 `P_F` is β with the capability index erased

That single deletion is the reification error, and it is now precisely locatable.

| | indexed by | encodes |
|---|---|---|
| **β(κ)** | (quantity, **capability**) | this *law* may not cross this distinction for this quantity |
| **`P_F`** | (quantity) | this *quantity* may not cross this distinction |

Erasing \(\kappa\) collapses a per-law fact into a per-quantity fact, and **the collapse is empirically false**:

| capability κ | may it cross `day` for `balance`? |
|---|---|
| SUM | **no** — the additive total of daily balances is not a balance |
| LAST | **yes** — it is the closing balance |
| MEAN | **yes** — it is the average daily balance |

\(\beta(\text{SUM})\ni day\) while \(\beta(\text{LAST})=\beta(\text{MEAN})=\varnothing\) on that axis. **A
single `P_F = {day}` cannot express this**, and whichever value it takes is wrong for two of the three
capabilities. That is exactly the pathology every propagation candidate exhibited.

**And the v7.2 addendum knew β was a different object** — §A.1.5 says so in terms:

> the inherited capability-indexed boundary map answers a different question — **which distinctions a given
> capability may not spend in a derivation contract** — and the two are **not the same governed object**, though
> they coincide in simple cases.

The warning was right and the replacement still dropped the index. *"They coincide in simple cases"* is the
tell: they coincide exactly when only one capability is in play.

### 3.3 β and the law-clause formulation are the same information, opposite polarity

A law clause names **both** a fiber scope **and** the composition it uses. So a clause *is* a
(capability, fiber-scope) pair, stated positively:

| quantity | clause | equivalently |
|---|---|---|
| `revenue` | additive composition over **any** fiber | \(\beta(\text{SUM})=\varnothing\) |
| `balance` LAW-P | at singleton fibers only; no composition | \(\beta(\kappa)\supseteq\) every axis, for every \(\kappa\) |
| `balance` LAW-C | value at the latest instant, over **ordered** fibers | \(\beta(\text{LAST})=\varnothing\) on the ordered axis |

> **β states, negatively and per capability, what a law clause states positively.** `P_F` tried to state it
> negatively and *without* the capability — which is not a weaker version of β, it is a different and
> inconsistent claim.

The positive form is preferable for the reason Part 1 and Part 2 both show independently: a clause must name its
composition anyway (to know which value operations it requires — Part 1 gate one) and its fiber scope anyway (to
know which fibers it consumes — Part 2's clause-forms). **Once a clause names both, β is redundant and `P_F` is
unstatable.**

### 3.4 G0.7 — the canonical Inventory case is an *identity* statement, not a prohibition

MA rev1 §3.6 on the theorem that motivated the whole mechanism:

> **Theorem G0.7 provides the canonical witness that a computation can be typed, executable, and deterministic
> while failing to inherit analytical identity.** A reducer can cross a blocked analytical distinction and
> produce a number without producing a lawful continuation of the measure family.
>
> > **Numerical executability cannot create analytical identity after the fact.**

And MA v1.0 §7 gives it with the worked quantity:

> **Summing Inventory across a blocked time axis can be typed, executable, and deterministic while still failing
> to inherit Inventory identity** (Wang 2026b, Theorem G0.7). Deterministic computation therefore does not by
> itself preserve analytical identity.

Read it carefully: **nothing is forbidden.** The sum is computed. It is a number. What the theorem denies is that
the number **is Inventory**. That is Huayin's category **F** — an identity guard — and it is **not** A, B, C, D
or E.

Under the law formulation the guard needs no mechanism at all: `sum(inventory@day)` **is a different family**,
with its own law and its own target, and it was never a candidate to *be* Inventory. The mechanism existed to
prevent a misattribution that the formulation makes impossible to express.

> **G0.7 is the strongest evidence for the hypothesis, and it is the example the old machinery was built
> around.** The machinery was answering *"may this movement happen?"* when the theorem was answering *"what is
> the result?"*

### 3.5 The estate: four unrelated substrates, one English word — and a **regression**

⟨measured⟩ Four structurally unrelated mechanisms share the word *blocked*, and they attach to four different
objects:

| mechanism | attaches to | really represents |
|---|---|---|
| `BAnchor.blocked_lineages` (legacy) | **(operator × lineage)** on a family member | **B** — the continuation law is wrong for this quantity |
| `blocked_edges` / `blocked_by` | a **hierarchy edge**, tested against data and **refuted** | **D** — want of evidence |
| `prohibited_constituents` / \(P_F\) | a **family** and a requested location | attempts A + C |
| `PublishBlocked` (studio) | a **publish plan**, overridable | **C** — a genuine governance gate, the only one |

**And here is the finding that reverses the story.** The legacy B-anchor **kept the capability index**:

```python
# parser.py:476-484 —  <agg> [BLOCKED { lineages }]
family[agg] = FamilyMember(agg, BAnchor(blocked), order_by, ...)

# projection.py:49 —  member -> frozenset(blocked_lineages)
# planner.py:2211 —   bad = sorted(crossed & t.law)   with t.law from  .blocked.get(reducer, ...)
```

It is indexed **by reducer**. `sum BLOCKED { calendar }` says *"SUM may not cross calendar for this quantity"* —
\(\beta(\kappa)\), exactly. And ADR-036 D6 states the consequence in terms:

> **No stock/flow/rating type.** Summing a stock across **stores** stays lawful, because the bar names
> `calendar`, not the measure. **`avg`, `min`, `max` and `count` over a stock across time stay lawful, because
> the author barred `sum` and barred nothing else** — that is a declaration, not an oversight the engine repairs.

> **That is the Balance/SUM/LAST/MEAN table of §3.2, written in the estate's own grammar, correctly, and years
> earlier.** `prohibited_constituents` is indexed by **(family, constituent)** — the capability index is gone.
> **C5 was a regression from the legacy mechanism on precisely the axis that decides the question.**

So the finding is now triangulated from three independent directions: MA's \(\beta(\kappa)\) (§3.1), the
Balance capability table (§3.2), and the legacy grammar. The v7.2 apparatus dropped an index the implementation
already had.

**A disagreement to record, per instruction.** `native_domain.py:74-85` refuses the MA import and gives a
direction:

> **The Measure Algebra's capability-indexed union is NOT the answer**: it governs a different object, indexed by
> capability rather than by family, and **importing it while discarding the capability index would
> under-prohibit**

The refusal is right and the *direction is only half right*. Discarding \(\kappa\) **over**-prohibits across
capabilities — a family-level \(\{day\}\) derived from \(\beta(\text{SUM})\) wrongly bars LAST and MEAN. It also
**under**-prohibits across derivation paths, which is the G2.8 tagged-axis case where an axis is *created* by the
expansion and no ex-ante family set can contain it. **Both directions are real; the estate named one.**

### 3.6 Two compressions that are *not* acknowledged anywhere

The remarkable feature of the estate is that the compression is **documented at almost every site** —
`native_domain.py:38-53` (*"can tell four situations apart internally; that does not make four reason codes"*),
`movement.py:140-142`, `planner.py:1789-1800`, `serving.py:469-482`, DG-6. Three such conflations were
subsequently split. Two are ruled deliberate. **Two are undocumented, and only these are defects rather than
design:**

**(i) `planner.py:1865` asserts a prohibition where nothing was adjudicated.** It emits `blocked_reduction`
saying every candidate *"would reduce by `<op>` across a lineage the governed law blocks for it"* — when the
branch is reached precisely because **no candidate earned any verdict**. The same method's docstring forbids it
at `:1802-1806`: *"THE DETAIL REPORTS THE VERDICTS; IT DOES NOT ASSERT A CAUSE… **FALSE** once §2c and transport
joined it… **A refusal that names the wrong cause sends the reader to fix the wrong thing.**"*

**(ii) `formation.py:122-132` emits an identity guard as want-of-state, with the wrong remedy attached.** The
docstring is unambiguous that this is **F**:

> A mapping that claims `max` for a family whose cited law is MIN is not describing a different backend — **it is
> describing a different family**, which is the succession-by-mapping the v2 format exists to make impossible.

It raises `WantOfState`, which reaches the wire as `want_of_state` **with `REMATERIALIZE` offered**. Rematerializing
cannot repair a mapping that names the wrong operator. This is **F on D's code path with D's remedy** — and
`refusals.py:95-99` states the invariant it breaks.

### 3.7 The positive formulation closes DG-4 for free

DG-4, open and recorded:

> Measure families are OPEN by default (`BLOCKED` closes), so a measure that simply **OMITS** an operator from
> its family grants generated use of it for free. A stock declared `FAMILY { last }` — no `sum` member at all —
> still serves `sum(x@day)` across time, because **there is no bar to cross**. The declared-bar case refuses;
> the *under-declared* case does not.

**DG-4 exists only because the polarity is negative.** Under law clauses stated positively, a family declaring
only a `last` clause **has no sum clause**, so `sum` over its fibers is not a continuation of it at all — it is
a different family (G0.7), and the identity question is the only question. There is no bar to omit and no door
to leave open.

> **A negative mechanism must enumerate what it forbids and therefore leaks whatever it forgets. A positive one
> states what it means and leaks nothing.** DG-4 is the leak; the polarity is the cause.

### 3.8 Why a prohibition was always spellable-around — ADR-036's own measurement

The measurement that triggered the whole rework:

```
SELECT stock.sum           AT {store*cal.month}   ->  disclose, blocked_reduction   179656.0
SELECT sum(stock.last@day) AT {store*cal.month}   ->  serve, CLEAN                  179656.0
```

> The identical meaningless number, one syntax away from its own prohibition, with the caveat gone. … **nine
> spellings of one defect**

**Trace both under the positive model, and the reason the guard failed becomes visible.**

- `sum(stock.last@day) @ month` is a **lawful family** — the additive total of daily closing stocks. 179656 is
  its **correct value**. It should **Serve**, under its own identity.
- `stock @ month` is **want_of_law** under a point-clause stock law — no clause covers fibers varying in
  calendar. It should **Refuse**, and no spelling reaches it.
- Asking for *"monthly stock"* and getting either is a **Clarify**.

> **The harm was never in the arithmetic. It was in the label.** The legacy mechanism tried to prevent a
> labelling error by prohibiting an operation — which is why it could be spelled around, and why nine spellings
> existed. The positive formulation prevents the labelling error directly (`stock @ month` has no meaning) and
> never needs to prohibit the operation at all.

This is G0.7 a third time: *"a computation can be typed, executable, and deterministic while failing to inherit
analytical identity."* **The mechanism was guarding movements; the defect was in identity.**

---

## Part 4 · Which distinctions survive, and which collapse

### 4.1 Survive — seven, and the corpus keeps them apart

| # | disposition | the fact | remedy | authority |
|---|---|---|---|---|
| 1 | **law-to-type inadequacy** | the operand's type, under its governed profile, does not supply the capabilities *and laws* this law requires | declare a profile, or use a different law | CDT × ToD §5.7 |
| 2 | **want of type coverage** | the law is analytically admitted; no governed value domain supplies it yet | admit a type | CDT v0.5:838 |
| 3 | **want of law** | the family's law has no clause over these fibers; **no value is determined** | the author may state a clause — or accept that it is a different quantity | Manifold |
| 4 | **undefined result** | the clause's result is undefined at *this point* | none; §9.4 forbids disclosing over it | law × data |
| 5 | **want of state** | a value is determined; no admitted argument is presently available | supply evidence, or another basis | evidence |
| 6 | **realization limit** | everything analytical is established; this build cannot execute it | a different profile | realization |
| 7 | **governance prohibition** | meaningful, establishable, executable — and **not permitted** | an authority lifts it | policy |

**Number 7 is real and it has a home already**: `PublishBlocked` is the estate's only genuine instance, and it is
a **publish gate with an override** — not a family fact. That is the right shape and the right location.

### 4.2 Collapse

- **"Family domain"** collapses into 3. It was never a separate fact.
- **"Additivity" as a property of a quantity** collapses into a law clause naming its composition.
- **"Stock vs flow vs semi-additive"** collapses — and ADR-036 D6 already refused the type, and CDT v0.5:944
  independently refuses *"a separate folklore taxonomy such as 'additive metric,' 'semi-additive metric,' or
  'non-additive metric.'"* **Two authorities reached that conclusion separately.**
- **`P_F`** collapses into 3, with the capability index restored — i.e. into the clause itself.
- **"Anchor type" (point vs period vs interval)** collapses into the three clause-forms plus an optional
  governed order (§2.2).
- **DG-4** collapses — it is an artifact of negative polarity (§3.7).

### 4.3 Does *not* collapse, though it looks like it should

**1 and 2 are different.** Both are anchor-invariant and both concern value capability, but 1 says *the law
cannot apply to this quantity* and 2 says *nothing has yet been admitted to carry it*. Calling 2 `want_of_law`
would tell a caller their lawful question was unlawful — which the estate already ruled against in an adjacent
case: *"A `want_of_law` would tell the caller their question was unlawful when the truth is that this build does
not implement it, and it would send them to fix a publication that is not wrong."*

**4 is not 5.** An undefined result is not missing evidence; more data cannot supply it.

**7 is not 3.** *"Collapsing them would send an operator to a steward to establish a law that already exists and
already answered."*

## Part 5 · What is genuinely missing from the model

1. **The hypothesis' clause *"what arguments it can meaningfully consume"* is four gates, not one** (§1.3), and
   one of them — undefined result — is a **function of law and data jointly** and can be carried by no
   declaration.
2. **Governance prohibition has no stated location in the theory.** §A.1.8 leaves coverage permission's
   *"governing location… not assigned"*, and this is its sibling. The estate has a working instance
   (`PublishBlocked`); the theory has no slot.
3. **Law-synthesis for composed families** — DG-6, still open. Nothing positively establishes the law a
   map-composed successor **earns**. This is the real residue of Mechanism 2, and it is a **law** question, not a
   domain question.
4. **Non-commutative / ordered continuation** — unchanged and still a genuine falsifier of any
   forgotten-constituents test. Vacuous while every registered law is commutative.
5. **The G2.8 tagged-axis case** — an axis *created* by relationship expansion cannot be in any ex-ante set.
   Held, and it is the *under*-prohibition direction of §3.5.
6. **A recorded jurisdictional disagreement** on who governs anchor-point order (§1.3).

## Part 6 · Is `P_F`, `𝒜_F`, or any family-domain object still necessary?

**No — and the exercise produced three independent arguments, any one of which is sufficient.**

1. **Wrong index.** \(\beta\) is capability-indexed; a family-indexed set cannot express the Balance
   SUM/LAST/MEAN split. Over-prohibits across capabilities, under-prohibits across paths (§3.5).
2. **Wrong granularity.** Undefined-result is **per point**, below anchor granularity, so a per-anchor object
   cannot carry the facts adjacent to it anyway (§1.3, G4).
3. **Wrong polarity.** A negative mechanism must enumerate what it forbids and leaks what it forgets — DG-4 — and
   is spellable-around — ADR-036's nine spellings (§3.7, §3.8).

\(\mathcal A_F\) survives **only** as derived notation, which is what ToD §4.1 always said it was: *"notation for
its defined analytical domain, not a proposed registry or new object."*

**And the discoveries are preserved.** The falsification of propagation is now a consequence. The
family-domain/edge-validity split survives as the 3/5/6 separation. *"Absence of prohibition is not permission"*
becomes unstatable-as-an-error. `CONSTRUCTED_DOMAIN_UNDECIDED` did the job Huayin credits it with: it refused
long enough for the index to be found.

## Part 7 · What the Manifold author therefore has to do

Stated as semantic acts, **not** fields, and not a design.

**For the world:** constitute it — identity, a closed root-point individuation, an existence law. Separately:
declare a **governed order** on a constituent where one is needed, and a **governed projection** between anchors
where one holds. Both are facts about the world, not about quantities.

**For a quantity:** state its **law** — and a law is a set of **clauses**, each of which names three things
together:

> **(the fibers it is stated over) · (the composition it uses) · (the value capabilities that composition
> requires)**

The three are one act because none can be stated without the others. Naming the composition *is* naming the
capability index that \(\beta\) carried and \(P_F\) lost. Naming the fiber scope *is* the clause-form of §2.2 and
the domain of definition whose pullback is \(\mathcal A_F\). Plus the quantity's **participation rule** and its
**value requirements**.

**For a construction:** nothing, where the cited law is complete — and the **contingent premises the law cannot
entail** where it is not: a governed order for FIRST/LAST, a co-participation contract for multi-input, a
convention parameter such as `ddof` or a quantile interpolation rule, a target where no law is catalogued.

**Not the author's at all:** \(\mathcal A_F\) · any prohibition set · any allow-list · additivity flags · any
stock/flow taxonomy · lineage · agreement · empty-case theorems · governance permissions (a policy act
elsewhere) · type coverage (CDT's) · evidence · realization.

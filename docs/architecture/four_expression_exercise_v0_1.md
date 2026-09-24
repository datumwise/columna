# Four expressions, explained without `A₀`, `P_F`, C3, or the publication schema

**A small semantic exercise.** Recorded by Claude at Huayin's direction, 2026-09-24.

**Standing.** Reconnaissance. No rule is enacted; no source change is authorized.

**The constraint.** The four expressions below are explained using only: the universe's constitution, a
family's **constitutive anchor**, its **target**, its **participation rule**, its **value requirements**, the
**cited law**, and the ordinary separation of evidence and realization. `A₀`, `P_F`, C3, "family-domain
propagation", and the current publication schema are **not used**. §9 records what I would have had to
introduce and did not, and what a *fifth* expression would force.

---

## 0. Two concessions first

Both challenges are correct. I concede them before using the corrected account.

### 0.1 `⋃_bases ⋂_roles 𝒜_G` was C7 wearing C3's clothes

v0.2 claimed a constructed family's analytical domain **is** the union over admitted bases of the intersection
over their roles. That was wrong, and ToD says so twice.

**§5.3 — a narrow basis does not narrow the family:**

> A basis may have a restricted domain of validity; an implementation cannot silently extrapolate it to every
> anchor or every missingness case. … **One basis may have a narrower declared application domain; outside it
> the basis does not silently redefine the target.**

**§9.6 — and the known bases are not even a complete account of establishability:**

> A different admitted proof can sometimes establish a scalar result without establishing the witness family
> itself. … **This is a counterexample to claiming that the witness basis is always necessary**

So the formula was wrong in *both* directions. It is not an upper bound on where the family **stands** (§5.3),
and not a complete account of where it can be **established** (§9.6). What it actually gives is:

\[ \bigcup_{\mathcal B}\bigcap_{G\in\mathcal B}\mathcal A_G\ \subseteq\ \{A:\ F@A\text{ is presently
establishable}\}\ \subseteq\ \{A:\ F@A\text{ is a lawful analytical object}\} \]

— a **lower bound on establishability**, which is two steps removed from standing. Collapsing them would have
let a missing basis role read as *"this quantity does not exist here"*, which is §5.5's error precisely:
*"Basis admission is a claim about analytical law. Availability is a claim about the current evidence. **They
have different scopes.**"*

**The corrected account is in §5.3 below and does not mention bases at all.** Bases reappear only in the
Refuse/Serve analysis, where they belong.

### 0.2 `A₀` is not needed, and this exercise does not use it

Setting `A₀ = I` was preserving a concept by defining it away. Below, **one** anchor does the work for every
family — the anchor its target is stated over. For a construction that is where its operand is consumed; for
an observation it is where the quantity is observed. Calling it a second thing added nothing. §9.2 records the
test I applied.

---

## 1. The vocabulary actually used

| term | meaning |
|---|---|
| **universe** | identity, a closed root-point individuation, an existence law |
| **anchor / point / fiber** | a governed partition of \(\Omega_U\); its blocks; \(\pi_{I\to A}^{-1}(a)\) |
| **governed projection** \(\pi_{I\to A}\) | exists iff \(I\succeq A\); *"A physical join does not supply a missing partition projection"* (§2.1.2) |
| **family** | a governed analytical identity, carrying: a **constitutive anchor**, a **target**, a **participation rule**, **value requirements** |
| **constitutive anchor** | the anchor the family's target is stated over. §2.2 keeps it **inside** \(F\): it *"[does] not become [an] additional current anchor of \(F@A\)"* |
| **measure** | \(F@A\) — the family at one **current** anchor |
| **law** | a governed analytical law, cited; ToD's foundation catalogue supplies MEAN |
| **evidence / realization** | support, coverage, availability; bindings, plans, carriers |

---

## 2. The world

```
universe ledger
  identity     : ledger
  individuates : { account, day }
  exists_when  : the account is open on that day          # generative
```

For the later steps the world must additionally supply **governed calendar structure**, as governed
projections among anchors:

```
  projections  : {account,day} ⪰ {account,week}  ?        # a governed fact, not a join
                 {account,week} ⪰ {account,month} ?       # a governed fact, not a join
```

**The exercise is deliberately neutral on how that structure is constituted** — whether calendar levels are
constituents of the individuation or governed placements. It needs only ToD §2.1.2's \(\pi\) to **exist as a
governed fact**. That neutrality is itself a result: the held Case-G question does not have to be settled to
explain these four expressions.

```
family balance
  constitutive anchor : { account, day }
  target              : the amount standing to the account at the close of the day
  participation       : every eligible root point contributes once
  values              : an amount in a governed currency; supports + , ÷ , =
```

**Four facts. Every one contingent.** Note what is *absent*: no domain, no prohibition set, no root, no
continuation declaration. Whether Balance may also stand at coarser anchors **is not asked by any of the four
expressions** — see §9.1.

---

## 3. Transition 1 — `balance @ day`

**Before:** the family `balance`. **After:** a **measure** of it. **No new family.**

| | |
|---|---|
| **new object** | the measure \(balance@\{account,day\}\) — an ascription, not a constitution |
| **from the Manifold** | nothing new; `balance`'s four facts |
| **from the law / MA** | nothing. No law is applied. §2.2 supplies only what \(F@A\) *means* |
| **inner anchor** | — (none; `balance` takes no operand) |
| **current anchor** | `{account, day}`, which **coincides with** the constitutive anchor. Coincidence, not identity |
| **geometry required** | the identity projection. §2.1.2: *"Equality permits identity movement; it is not a strictly contracting reducer"* |

**Refuse:** if `{account,day}` is not a governed anchor of `ledger`; or if the target does not denote at the
requested anchor (`balance @ {account}` — there is no *"the day"* there).
**Clarify:** if `day` is ambiguous between two governed partitions in this world.
**Serve:** where the points are supported. **Serve-with-disclosure:** where some requested points are
eligible-but-unsupported — §2.3 keeps *"absent from the universe, present but ineligible, eligible but
unsupported, supported with value zero"* as four different claims.

> **`@` is ascription.** Nothing is created, and this is the same *kind* of step as Transition 3.

---

## 4. Transition 2 — `mean(balance @ day)`

**Before:** the family `balance` (and, as notation, its measure at the constitutive anchor). **After:** **a new
family identity.** This is the only transition in the exercise that brings a family into existence.

| | |
|---|---|
| **new object** | a family \(M_1\): *the arithmetic mean of the participating balance values over the day-points of the target fiber*, with constitutive anchor `{account, day}` |
| **from the Manifold** | **nothing new.** Three premises, all already discharged by `balance`'s four facts: (i) `balance` is established at `{account,day}`; (ii) its participation rule is determinate; (iii) its values support `+` and `÷` |
| **from the law / MA** | everything else: the target; that participation is *"participation under the operand construction's governed rule"* (§11.5.1); a \((\Sigma,N)\) sufficient state; that the scalar mean **does not continue** (§5.2, MA §14.6); the nonempty-fiber contract; path-independence (Prop 6.2) |
| **inner anchor** | `{account, day}` — **constitutive**. It says *which analytical points the law consumes*. §11.5.2: \(mean(x@order)\neq mean(x@customer)\) absent an explicit equivalence. It is **inside** \(M_1\) and never a current anchor |
| **current anchor** | **none.** A family has no current anchor. Asking for one is Transition 3 |
| **geometry required** | none beyond `{account,day}` being a governed anchor |

**Why `balance`'s inability to cross time is not in play.** MEAN does not move `balance`. It reads `balance` at
`{account,day}` — where `balance` is stated — and applies a different law to the collection. **There is no
movement of `balance` in this expression to license or refuse.**

**Refuse:** if `balance` is not established at `{account,day}`; if its value domain does not support `+`/`÷`
(a currency-free ordinal would fail); if its participation rule is unestablished.
**Clarify:** if the request said *"average balance"* without fixing the inner anchor — §8.2 of MA:
*"'mean revenue by region' [is] analytically incomplete unless the input anchor is uniquely determined by
governed law."* Several inner anchors give **identity-distinct** families.
**Serve / disclose:** not yet applicable — a family is not a result.

---

## 5. Transition 3 — `mean(balance @ day) @ week`

**Before:** the family \(M_1\). **After:** a **measure** of \(M_1\). **No new family.**

| | |
|---|---|
| **new object** | the measure \(M_1@\{account,week\}\) |
| **from the Manifold** | **the governed projection** \(\{account,day\}\succeq\{account,week\}\). This is the one genuinely new Manifold fact in the whole exercise, and it is a fact about the **world's calendar**, not about any family |
| **from the law / MA** | that the value at each week-point is the mean over that point's day-fiber; that this agrees along admitted paths (Prop 6.1 via the \((\Sigma,N)\) state); that it is undefined on an empty fiber |
| **inner anchor** | unchanged — `{account, day}`, still constitutive |
| **current anchor** | `{account, week}` — where **this measure** lives |
| **geometry required** | \(\pi_{\{account,day\}\to\{account,week\}}\), governed |

### 5.1 Why this is lawful, stated without a domain concept

\(M_1\)'s target is *"the mean of the participating balance values over the day-points of **the target
fiber**"*. That is a statement about **an arbitrary fiber**. Give it a fiber and it denotes. The week-point
`(acct, W12)` has a day-fiber, participation selects a subset, and the mean of those values is the value.

> **The target is stated uniformly over the fiber, so it denotes wherever the constitutive anchor projects.**

### 5.2 This is not geometry licensing a quantity

§4.1 is explicit that it must not be: *"A geometrically available projection and a computable state operation
do not by themselves put \(A\) in \(\mathcal A_F\). The family's definition must license the quantity being
claimed there."*

It is honored here. **The licence comes from the definition**, which is fiber-uniform; geometry supplies only
the *candidate* fibers. The contrast proves the point: `balance`'s target names a location — *"at the close of
the day"* — so at `{account}` the geometry is equally available and **the definition does not denote**. Same
geometry, different licence, because the difference lives in the target.

### 5.3 The rule, for both cases

> **\(F@A\) is a lawful analytical object iff \(F\)'s constitutive anchor projects to \(A\) under governed
> geometry, and \(F\)'s target denotes on the resulting fibers.**

For a fiber-uniform target the second clause is satisfied wherever the first is. For a location-naming target
it is not, and what it reaches is a contingent semantic fact about that target. **Bases do not appear.**

### 5.4 Dispositions

**Refuse — three genuinely different refusals, and they must not be merged:**

| refusal | cause | remedy |
|---|---|---|
| **want of geometry** | no governed \(\pi_{\{account,day\}\to\{account,week\}}\) | the world must constitute it |
| **want of law** | the target does not denote on these fibers | nothing; it is a different quantity |
| **want of state** | lawful, but no admitted argument is presently available — *"A valid basis need not be available"* (§5.5) | supply evidence |

That third row is exactly what v0.2's formula erased, and keeping it is the whole of §0.1.

**Clarify:** if `week` resolves to two governed partitions (ISO vs retail); or if the caller said
*"weekly average balance"* and both \(M_1@week\) and `last(balance@day)@week` are lawful readings.

**Serve:** one lawful identity, one adequate argument available.
**Serve-with-disclosure:** lawful and established, but a week's day-fiber is **partially** supported — 3 of 7
days. The mean is well-defined over the participating points; **coverage is an evidence question** (§1.5:
*"an edge- or evidence-validity question"*; §5.2: *"Self-sufficiency is a composition claim, not a coverage
claim"*), so this Serves **with the coverage qualification attached** — it does not Refuse.

---

## 6. Transition 4 — `mean(mean(balance @ day) @ week) @ month`

**This expression performs two acts, and separating them is the point.**

### 6.1 Act one — a second family comes into existence

**Before:** \(M_1\), and its measure at `{account, week}`. **After:** a new family \(M_2\).

| | |
|---|---|
| **new object** | \(M_2\): *the mean of the participating weekly average daily balances over the week-points of the target fiber*, with constitutive anchor `{account, week}` |
| **from the Manifold** | **nothing new.** \(M_2\)'s three premises are discharged by \(M_1\): \(M_1\) is established at `{account,week}` (Transition 3); its participation rule is determinate (entailed from `balance`'s); its values support `+`/`÷` |
| **from the law / MA** | as in Transition 2, one level up |
| **inner anchor** | `{account, week}` — constitutive for \(M_2\). `{account, day}` is constitutive for \(M_1\) and remains **inside** \(M_1\), which is \(M_2\)'s operand |

**This is not \(M_1\) continuing from week to month.** \(M_1@week\) is **consumed as the constitutive input to a
new law**. \(M_2\) is a different analytical quantity from \(M_1\), and `mean(balance@day)@month` is a third,
distinct from both. §3.7's child-state case — \((100,1)\) and \((300,2)\) combining to \(400/3\), *"not the
unweighted mean \(125\) of the displayed child ratios"* — is **not a prohibition on \(M_2\)**; it is the
statement that \(M_2\) and `mean(balance@day)@month` are **different targets**, which is exactly what makes
both declarable.

> **Mean-of-mean was never the problem.** It is an ordinary second formation.

### 6.2 Act two — ascribing \(M_2\) at month

By §5.3, \(M_2@\{account,month\}\) is lawful iff `{account, week}` projects to `{account, month}`.

**And ordinary calendar Week need not refine calendar Month.** ToD §2.1.2:

> Refinement is a partial order. Two anchors can both be governed without either refining the other.
> **Calendar Week and Calendar Month are familiar examples: Day can refine each, while a week can cross a
> month boundary.** A valid weekly materialization does not thereby establish exact calendar-month values.

Stated with the care requested:

- **If the governed Week partition refines the governed Month partition, the geometric obstacle is absent.**
  Participation, support, coverage, evidence and realization premises may still decide the outcome.
- **If it does not, ordinary Week→Month projection cannot establish this construction.** §6.3: the family
  *"does not manufacture a path between incomparable locations."* Forcing it would silently change \(M_1\)'s
  own quantity from *a weekly mean* to *a mean over the part of each week inside the month* — which §4.2
  forbids in terms: *"A staged proof must combine the same intended contributions, with the same multiplicity
  and formation, as its direct counterpart."*

**Refuse:** want of geometry, where Week does not refine Month — and the refusal is **nameable**: there is no
governed projection. Or want of state, where \(M_1@week\) is unavailable for the participating weeks.
**Clarify:** *"monthly average balance"* — `mean(balance@day)@month`, \(M_2@month\), and a mean of closing
balances are all lawful and **identity-distinct**.
**Serve / disclose:** as Transition 3, one level up; partial week coverage inside a month discloses.

> Note the recursion is uniform: Transition 4 = Transition 2 + Transition 3, at one remove. **Nothing new was
> needed at the second level.** That is the strongest evidence that the account is the right shape.

---

## 7. The single rule that covered all four

```
   balance                      a family        (4 contingent facts)
   balance @ day                a measure       (ascription)
   mean(balance @ day)          a family        (law application; 0 new Manifold facts)
   ... @ week                   a measure       (ascription; needs a governed projection)
   mean(... @ week)             a family        (law application; 0 new Manifold facts)
   ... @ month                  a measure       (ascription; needs a governed projection)
```

Two acts alternate, and only two:

> **CONSTITUTION** — a family comes into existence either by a governed observation (its target asserted at a
> constitutive anchor) or by applying a cited law to an operand established at a constitutive anchor. A law
> application needs exactly three things from its operand: **establishment at that anchor, a determinate
> participation rule, and value support for the law's operations.**
>
> **ASCRIPTION** — \(F@A\) is lawful iff \(F\)'s constitutive anchor projects to \(A\) under governed geometry
> and \(F\)'s target denotes on the resulting fibers. Whether it can be **established** there is a separate,
> downstream question.

---

## 8. Dispositions, collected

| | Refuse | Clarify | Serve / disclose |
|---|---|---|---|
| `balance @ day` | not a governed anchor; target does not denote | `day` ambiguous | supported / partially supported |
| `mean(balance @ day)` | operand not established at the anchor; no `+`/`÷`; participation unestablished | *"average balance"* — inner anchor unfixed | n/a (a family is not a result) |
| `… @ week` | want of **geometry**, **law**, or **state** | `week` ambiguous; weekly-mean vs weekly-closing | partial day coverage discloses |
| `… @ month` | want of geometry (Week ⊁ Month) — **nameable**; want of state | *"monthly average balance"* — three lawful readings | partial week coverage discloses |

**Three refusals, kept distinct**: want of geometry (the world lacks a projection), want of law (the target
does not denote), want of state (lawful but not presently establishable). Merging the third into the first two
is the error §0.1 concedes.

---

## 9. What I did not need, and what would force more

### 9.1 Not needed — and the exercise is the reason

| concept | needed? |
|---|---|
| `A₀` / family root | **no** — one constitutive anchor sufficed for every family (§9.2) |
| `P_F` / prohibited constituents | **no** — never reached |
| a declared analytical domain | **no** — standing follows from projection + target denotation |
| domain propagation between families | **no** — the question never arose; there is no movement of `balance` in any of the four |
| a `primitive` / `constructed` discriminator | **no** — readable from whether a law is applied |
| a continuation-law declaration on `balance` | **no** — *not reached by these four expressions* |

**The honest qualification, because it is the discipline asked for.** None of the four expressions requires
`balance` to stand anywhere other than its constitutive anchor. So **the exercise does not force the
fold-scope/extension concept at all.** What forces it is a *fifth* expression:

```
balance @ { day }          # the total balance across all open accounts on a day
revenue @ { region }       # the same shape, for an observational additive quantity
```

Here an observational family is asked to stand at a coarser anchor, its target names a location, and §5.3's
second clause must be decided: **does the target denote on the coarser fiber, and by what law?** That is a
contingent semantic fact and it must come from the Manifold. **It is the one thing v0.2 got right that this
exercise cannot re-derive** — and it is *positive* content (what the quantity means over a coarser fiber),
attached to the target, not a prohibition attached to a domain.

### 9.2 The test I applied to `A₀`

I tried to state a fact about any of the four expressions that needed a root distinct from the constitutive
anchor, and could not. The candidate was *"exclude the degenerate case"* — \(M_1@\{account,day\}\) equals
`balance`, and one might wish to forbid it. But it is **lawful and correct**, merely uninformative; refusing to
serve it is a presentation choice, not an analytical fact. **A concept introduced to carry a presentation
preference is not an ontological object.** `A₀` is not needed.

---

## 10. What this settles, and what it leaves

**Settled by the exercise.** The four expressions are fully explained by **universe constitution + one
constitutive anchor per family + target + participation + values + cited law**, with evidence and realization
kept separate. No `A₀`, no `P_F`, no domain declaration, no propagation. The account is **recursive without
remainder**: level two needed nothing level one did not.

**Corrected from v0.2.** Standing is **not** \(\bigcup_\mathcal{B}\bigcap\mathcal A_G\). That formula is a lower
bound on *establishability*; standing is projection + target denotation. Keeping them apart restores **want of
state** as a distinct refusal.

**Withdrawn from v0.2.** `A₀` for constructions — not needed at all, rather than "forced to \(I\)".

**Still outstanding, and now precisely one thing at the family level:** what an observational family's target
means over a coarser fiber (§9.1). That is the only contingent fact about families that the exercise could not
eliminate, and it is the right candidate for the semantic-scope / governance-prohibition separation you want to
pursue — the first is part of what the quantity *means*, the second is what governance currently *permits*.

**At the world level:** whether the governed Week refines the governed Month is an ordinary authored fact with
a nameable consequence. The exercise turned out to be **neutral on the held Case-G question** — it needs only
that a governed projection exist, not how it was constituted.

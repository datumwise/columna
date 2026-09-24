# The Manifold declaration as Columna's semantic starting point

**Sixteen cases across four layers, and the model they imply.** Recorded by Claude at Huayin's direction,
2026-09-24.

**Standing.** Design record. **No schema, no serialization, no implementation plan, no code changes.** Stops at
the model, the classification, the disposition of inherited concepts, and reconciliation notes.

> ⚠ **WORKING PREMISE, NOT RATIFIED.** This exercise uses the Case-S universe constitution of the 2026-09-15
> record as a **working premise**. Its §§1–6 remain **draft**; only §§7–11 are ruled. **Nothing below ratifies it,
> and no downstream agreement here should be read as adopting it.** Where a family fact turns out to belong to
> universe constitution, §5 moves it upstream rather than duplicating it.

**The discipline:** **Manifold constitutes → Measure Algebra entails → MEL denotes → Frame-QL requests.** Plus,
strictly below the analytical line: governance may withhold; evidence and realization determine servability.

---

## 0. The worlds

```
universe sales    individuates { store, day, order, line }    exists_when a line was transacted
universe ledger   individuates { account, day }               exists_when the account is open that day
```

Universe-level facts the cases will need — **none of them family facts** (§5):

```
governed order on `day`                    (chronological)         -- needed by case 7
governed projection {..,day} ⪰ {..,week} ⪰ {..,month}             -- needed by cases 4-8
governed placement store → region  (Case G, held)                  -- needed by case 3
governed conversion to a numéraire                                 -- needed by case 12
```

---

## 1. The sixteen cases

Each answers only **A** what the author constitutes · **B** what Measure Algebra entails · **C** what MEL denotes
· **D** what Frame-QL may request, and the disposition.

### Case 1 — observational `revenue`

**A.** One grounding clause and one composition clause, plus the facts a clause presupposes.

```
grounds   : at sales.{store,day,order,line}, the consideration accruing from the line
eligible  : every root point of the universe
contributes: one contribution per eligible point
valued in : CDT Decimal
composes  : fiber-reducing, SUM, over ANY fiber
```

**B.** The extension \(\{A: \text{the law determines } revenue@A\}\) = every anchor reached by a governed
projection. Direct/staged agreement (Prop 6.1). The empty fiber takes the monoid identity **where known-empty** —
which is why `eligible` must be a rule over eligible points, not observed ones. `sum(revenue@line)` **is this
family** (§11.5.1 canonicalization), not a construction. **Contingent premise, not theorem:** that the additive
composition means anything — that is the author's clause, and it is the only thing distinguishing this from
case 2.

**C.** `revenue`. MEL knows nothing about consideration; it knows a governed operand named `revenue` exists at a
governed anchor with a cited SUM clause.

**D.** By name, at any anchor. **Serve** where supported; **Disclose** where coverage is partial; carrier
exactness is realization (2026-09-12).

### Case 2 — observational `balance`

**A.** Identical shape. **Three of the five facts are word-for-word identical to case 1.**

```
grounds   : at ledger.{account,day}, the amount standing to the account at the close of the day
eligible  : every root point of the universe
contributes: one contribution per eligible point
valued in : CDT Decimal
composes  : fiber-reducing, SUM, over fibers varying only in { account }
```

**B.** Extension = `{ {account,day}, {day} }`. **Nothing else is entailed, and nothing is prohibited** — the
absence of a day-crossing clause is the absence of a meaning, not the presence of a bar.

**C.** `balance`.

**D.** As case 1, within its extension.

> **Cases 1 and 2 differ in the grounding prose and in one quantifier.** That quantifier is the whole of
> semi-additivity, the stock/flow taxonomy, the B-anchor, and \(P_F\).

### Case 3 — `revenue @ {region}`

**A.** **Nothing at the family layer.** `region` requires a **governed placement `store → region`** — a
**universe** fact (Case G, held), not a family fact.

**B.** Revenue's clause is claimed over **any** fiber, so given the placement the law determines a value here.
**Geometry does not license it — the clause's universal quantification does**; geometry only supplies the fiber.

**C.** `revenue @ {region}` — an ascription, not a construction. Frame-QL §3.1: it *"does not need to become
`sum(revenue @ {transaction}) @ {region}`… The query names the family identity."*

**D.** **Serve**; **Disclose** on partial coverage. If `region` resolves to two governed placements → **Clarify**.
**Blocked in the estate today only because Case G is held — a universe question, not a family one.**

### Case 4 — `balance @ {week}`

**A.** **Nothing, and nothing incremental would help.**

**B.** No clause covers fibers varying in `day`. **The law determines no value.** Not prohibited — *undetermined*.

**C.** The expression denotes; **what fails is family standing**, not denotation. MEL will happily write it.

**D.** **Want of law.** The remedy is not to widen a permission; it is to ask cases 5, 6 or 7, which are
different quantities. **This is the acceptance test for the whole model.**

### Case 5 — `sum(balance @ {day}) @ {week}`

**A.** **Nothing.** The SUM law is catalogued; the operand is established by Balance's grounding clause.

**B.** Balance's own clause does **not** cover day-varying fibers, therefore this is **a different family** —
ToD v6.1: *"distinct family identities even when everyday language reuses one label."* Its law is complete: Σ over
any fiber of balance point values. Extension: every anchor coarser than `{account,day}`. **Its target is the
additive total of daily balances, which is a perfectly definite quantity.**

**C.** `sum(balance @ {account,day})` — a family expression, parametric in the operand.

**D.** **Serve**, under its own identity. If the request said *"total balance"* → **Clarify** (this, or a closing
balance, or a current balance). **The number was never the problem; the label was.**

### Case 6 — `mean(balance @ {day}) @ {week}`

**A.** **Nothing.**

**B.** MEAN consumes Balance at **singleton fibers of its grounding clause** — never its composition clause.
**Balance does not travel to Week; MEAN establishes a different family whose fibers happen to be week-fibers of
days.** Extension: every anchor coarser than `{account,day}`. Result type **Rational** (exact division is not
closed in Decimal). Empty fiber **undefined**, from the law's nonempty constructor domain. **Sufficient state
\((\Sigma,N)\) is how it is established, not what makes it stand.**

**C.** `mean(balance @ {account,day})` — and MEL's knowledge is exactly this shape, parametric in `X`.

**D.** **Serve.** Partial day coverage → **Disclose**. If only finalized weekly scalars are retained →
**want of state**, never want of law.

### Case 7 — `last(balance @ {day}) @ {week}`

**A.** **A governed complete order on `day` — a universe fact.** Plus, at the family layer, **which order**, and
only if the world admits more than one (§7.2; entailed when exactly one). §7.3 refuses substitutes: *"Appending a
storage identifier or relying on sort stability is not a repair of analytical law."*

**B.** Witness family \(W\), basis \(\{W\}\to L\), the witness monoid and known-empty \(\bot\) — §§8.1–8.3, all
theorem. Extension: every anchor coarser than `{account,day}` — **wider than Balance's own**, because the witness
monoid composes where Balance's clause does not. **Nothing propagated; nothing was blocked.**

**C.** `last(balance @ {account,day}; order = O)`.

**D.** **Serve.** Two governed day-orders → **Clarify**.

### Case 8 — `mean(mean(balance @ {day}) @ {week}) @ {month}`

**A.** **Nothing at the family layer.** A **governed projection** `{account,week} ⪰ {account,month}` — a universe
fact, and one that **may not hold**: ToD §2.1.2, *"a week can cross a month boundary."*

**B.** The outer MEAN consumes \(M_1\) established at week. **Three objects must stay apart:**

| | what it is |
|---|---|
| `mean(mean(X@day)@week)@month` | **a new family** — the unweighted mean of weekly means |
| `mean(X@day)@month` | **the same family as \(M_1\)**, at a coarser anchor; meaning fixed at constitution, establishment via its \((\Sigma,N)\) basis |
| the *"mean of means"* criticism | **confusing the two, or leaving the intended one ambiguous** |

§3.7's child-state case — \((100,1)\) and \((300,2)\) combining to \(400/3\), *"not the unweighted mean 125 of the
displayed child ratios"* — is **precisely the statement that these are different targets**, which is what makes
**both** declarable. **Mean-of-mean is not intrinsically unlawful.**

**C.** `mean(mean(balance@{account,day})@{account,week})`.

**D.** Explicit MEL with the projection holding → **Serve**. *"Monthly average balance"* → **Clarify** among the
three. Projection absent → **want of law**, nameably: no governed `week → month`. Weekly \((\Sigma,N)\) retained
but weekly scalars discarded → the second reading Serves and the first is **want of state**.

### Case 9 — AOV, `revenue / order_count`

**A.** **One fact: the co-participation contract.** Does the denominator count **every eligible order**, or **only
orders carrying revenue**? Two lawful worlds, different quantities. §3.5 requires operands *"lawfully
co-established under the applicable universe, type, and **co-participation contract**"*, and §5.3 forecloses
inference: *"Individually supported inputs drawn from incompatible populations do not form an admitted basis
merely because their types match."*

```
constructs : co-located, RATIO, of ( revenue , order_count )
             co-participation : <contract>
```

**B.** **Argument shape matters here and nowhere earlier.** AOV does **not** reduce a fiber — it consumes
**co-located measures at the target anchor** (§5.1 anchor-locality, §3.5 pointwise reading). So **AOV has no
fiber-reducing clause at all**, and that is why the child-state discipline is a theorem rather than a warning.
Result type Rational; **undefined where `order_count = 0`** — a value premise.

**C.** `revenue / order_count`, or the governed name resolving to it.

**D.** **Serve.** Without the co-participation contract → **want of law**, and the refusal can **name** the
missing fact.

### Case 10 — currency in the **semantic value type**

**A.**

```
grounds   : at sales.{store,day,order,line}, the consideration accruing from the line
valued in : Money = ( amount, currency )        -- `+` is PARTIAL: within a currency only
composes  : fiber-reducing, SUM, over ANY fiber, GIVEN the fiber is currency-homogeneous
                                                 ^^^^^ a PREMISE
```

**B.** The family **stands** at `{region}` — the clause is claimed over any fiber — and the measure is
**undefined at region-points whose fiber spans currencies.** Determined at the anchor; undefined at a point.
§9.4 forbids papering over it: *"A disclosure can state a limitation on an otherwise established, correctly
described result. It cannot make arbitrary point selection determinate."*

> **This is why no per-anchor domain object could ever have been right, even for observational families:
> definedness here is *below* anchor granularity.**

**C.** `revenue` — MEL is unchanged. The partiality lives in the type and the premise, not the expression.

**D.** **Serve** at homogeneous points; **undefined result** at heterogeneous ones — a refusal that is neither
want of law nor want of state, and **not disclosable**.

### Case 11 — currency as an **analytical constituent**

**A.** The universe individuates `{store, day, order, line, currency}` — **a universe change, not a family
change.** Revenue's value is then a bare Decimal:

```
composes  : fiber-reducing, SUM, over fibers varying only in { store, day, order, line }
                                                              ^^^^^ a SCOPE
```

**B.** `revenue @ {region}` now **forgets `currency`**, which the scope excludes → **want of law**, decided from
geometry **before any data**. `revenue @ {region, currency}` is determined.

> **The same analytical concern lands in a different slot depending on representation, and both are lawful.**
> Case 11 makes *"revenue by currency"* a governed analytical location; case 10 does not, but keeps amount and
> currency together as one value. **They answer different analytical questions and the model must not force
> either.**
>
> And note the shape: **under this representation Revenue's clause looks exactly like Balance's** — a scope
> excluding one constituent. **The flow/stock difference is not even a difference of kind.**

**C.** `revenue`, at a richer anchor lattice.

**D.** `@ {region, currency}` → **Serve**. `@ {region}` → **want of law**. *"Revenue by region"* in a
multi-currency world → **Clarify**, because the caller has probably not said which they mean.

> **Cases 10 and 11 jointly establish the rule for the clause model: scope and premise are separated by *when
> the condition can be decided* — geometry alone versus the values — and nothing else.**

### Case 12 — a currency-conversion construction

**A.** A **governed conversion** to a numéraire — a **universe-level governed structure**. At the family layer:

```
family revenue_usd
  constructs : co-located, CONVERT[ to = USD, rate = <governed> ], of ( revenue )
  composes   : fiber-reducing, SUM, over ANY fiber        -- ENTAILED: USD is homogeneous
```

**B.** The tempting alternative — a premise *"SUM over currency-varying fibers **given** a conversion"* — is
**rejected**, and the rule it establishes is general:

> **A premise may *gate* a composition; it may not *change* what the composition produces.**

A conversion changes the **result's value domain**: the output is in USD, the point values are not. That makes it
a **law application**, not a premise. So it constitutes **a different family**, and §3.9 is **satisfied rather
than evaded** — a changed target gets a successor identity instead of hiding inside a premise. Without this
rule, "premise" becomes an unbounded escape hatch and the clause model collapses into arbitrary code.

**C.** `convert[USD](revenue)`.

**D.** **Serve** where the governed rate covers the points. Rate missing for some points → **want of state**. Two
governed rate sources → **Clarify**. Rate ungoverned → **want of law**.

### Case 13 — a non-Decimal type where the law changes **materially**

Two contrasting sub-cases, because they fail at **different layers**.

**13a — a set-valued family.**

```
family distinct_customers
  grounds   : at sales.{store,day,order,line}, the customer identity on the line
  valued in : Set<CustomerId>            -- requires governed exact equality on CustomerId
  composes  : fiber-reducing, UNION, over ANY fiber
```

**B.** Union is associative, commutative and **idempotent** — a materially different continuation from SUM, and
CDT supplies it. The scalar is a **separate family with a co-located clause and no fiber-reducing clause of its
own**:

```
family count_distinct_customers
  constructs : co-located, CARDINALITY, of ( distinct_customers )
```

§11.5.3: *"The cardinality generally does not retain enough information to determine overlap during later
union."* So **the scalar stands exactly where the set family stands, and never composes.** Second independent
witness for the co-located argument shape.

⚠ **And `valued in` is a governed reference with a parameter.** CDT: `Set<T>` requires exact equality on `T`; for
text, *"`Set<Text>` and `distinct_set` over text are **not admitted merely from the bare spelling `Text`**. They
require a declared exact text-equality profile. Without one, equality-dependent set/distinct operations are
**refused**."* **That profile is an authored fact, and it sits in the type reference, not in the family law.**

**13b — a family valued in `Timestamp`, and the contrast that matters.**

CDT: *"`Timestamp + Timestamp -> undefined` … These rules are **capability restrictions, not syntactic
conventions.** A timestamp cannot enter an additive analytical family merely because its carrier is numerically
encoded."*

> **So `sum(event_time @ …)` fails for a completely different reason than `balance @ week`, and the model must
> not merge them:**
>
> | | why it fails | when decidable |
> |---|---|---|
> | `balance @ {week}` | the quantity **could** be summed — the values add — but **no clause claims it means anything** | scope, from geometry |
> | `sum(event_time@…)` | the values **cannot be added at all**; the law's required capability does not exist on the type | **before any anchor is considered** |
>
> The first is a **family-law** fact. The second is a **law-to-type** fact and is **anchor-invariant** — it fails
> at the constitutive anchor too. **A model with only one refusal here would be wrong.**

**C.** `distinct_set(customer@line)`, `count_distinct(...)`, `sum(event_time@...)` — MEL writes all three; only
the Manifold and CDT decide which denote governed families.

**D.** 13a → **Serve**, or **want of law** if no equality profile is declared for the element type. 13b →
**law-to-type inadequacy**, which is neither want of law nor want of state.

### Case 14 — point-in-time versus range/interval

**Four objects that calendar vocabulary fuses, and the model keeps apart:**

| | what it is | where it lives |
|---|---|---|
| **point-in-time quantity** | grounded at a point, no time-crossing composition | Balance, case 2 |
| **"over the members of" a period** | a fiber-reducing clause | cases 5, 6 |
| **"at the end of" a period** | a fiber-reducing clause citing LAST with a **governed point order** | case 7 |
| **an interval-*valued* quantity** | the **value** is an `Interval` | a type fact, **not** an anchor fact |

The fourth is the trap. CDT gives `Interval` *"no intrinsic total order"*, *"no general analytical additive
claim"*, keeps it *"distinct from `Duration`"*, and warns that an internal numeric representation *"does not make
`Interval` an additive scalar."* ToD §5.7 settles the jurisdiction: *"Internal value structure is not analytical
location."* **A family whose value is an interval is not a family at an interval anchor.**

And **"at a period" as an anchor is a *universe* question.** A world individuated by `{account, week}` has weeks
as **root points**; its `week` is not a fiber of anything, and anchor identity is universe-relative — so it is
**not the same anchor** as a `week` reached by projection from days. Comparing them is universe passage.

> **Constraint honoured explicitly.** The order LAST requires is ToD §7's **analytical point order**. It is
> unrelated to the proposed `{a*b}` coordinate/presentation precedence, which is not adopted and which — even if
> adopted — **is not LAST/LAG/SCAN analytical order.** Nothing here uses that syntax to solve a family-law or
> governed-order problem.

### Case 15 — multi-input where participation genuinely matters

```
family revenue_margin_covariance
  constructs : co-located, COVARIANCE[ ddof = 1 ], of ( revenue , margin ) formed at sales.{...,line}
               co-participation : the pair is established at the line, both eligible
```

**A.** Two authored facts, and both are genuinely contingent: the **co-participation contract**, and the
**`ddof` convention** — a law parameter, which SER makes non-optional by carrying it in the family's name.

**B.** The conservation rule bites here in a way it does not for AOV. §3.5: *"A weighted mean… requires pointwise
products at its constitutive anchor **before separate reductions destroy the pairing**."* §3.1: *"multiplying
values and weights after reducing them separately does not generally reconstruct their original paired
products."* And the joint-support obligation, SER: *"**Marginal support of \(x\) and \(y\) does not establish
paired support.**"*

> **Participation is a *formation-time* fact here, not a domain fact.** The pairing must be formed at the
> constitutive anchor; no later evidence can reconstruct it. This is the one case where getting participation
> wrong is not a wrong denominator but an **unrecoverable** loss.

**C.** `covariance(revenue, margin @ {store,day,order,line}; ddof=1)`.

**D.** **Serve**. Marginal support only → **want of state**, and specifically **not** repairable by
re-materializing the marginals. Co-participation undeclared → **want of law**.

### Case 16 — what BLOCKED rejected, and what it actually was

The canonical case, with `inventory` declared exactly like Balance:

```
family stock_exposure
  constructs : fiber-reducing, SUM, of ( inventory @ ledger.{sku,day} ), over ANY fiber
  valued in  : unit-days                                  -- ENTAILED: Decimal × the day count
```

**B.** `sum(inventory@day)@month` is **not a mistake**. It is **inventory-unit-days** — the integrated stock
exposure that days-inventory-outstanding and inventory-turns are computed from. **Contract Calculus names it
itself:** *"The plan can be rebound outside \(G_0\) under a different contract, such as an **integrated
stock-exposure quantity**. That would create a different analytical object rather than prove inherited closure."*

| request | this model | the old mechanism |
|---|---|---|
| `inventory @ {month}` | **want of law** — no clause covers day-varying fibers | refuse — *or* **disclose**, in the ADR-036 measurement |
| `sum(inventory@day) @ {month}` | **Serve** — a lawful, named, standard financial quantity | serve **CLEAN**, same number, caveat gone — *"nine spellings of one defect"* |
| calling the second *"monthly inventory"* | **Clarify** | not addressed |

> **The thing BLOCKED rejected was a real business quantity with a standard name.** The only error was ever the
> label. G0.7's content — *"typed, executable, and deterministic while still failing to inherit Inventory
> identity"* — becomes structural: `sum(inventory@day)` was **never a candidate to be Inventory**, because
> Inventory's law has no such clause.
>
> **And DG-4's leak cannot arise.** A family declaring only a `last` clause does not "serve `sum` because there
> is no bar to cross" — absence of a clause is absence of meaning, necessarily.

**C.** `sum(inventory @ {sku,day})`, optionally named `stock_exposure`.

**D.** **Serve**, under its own identity, with its own unit. *"Inventory for the month"* → **Clarify**: the
closing level (case 7), the average level (case 6), or the exposure (this).

---

## 2. The declaration model the examples imply

**Huayin's expected shape survives, with four refinements the cases forced and one rule they added.**

### 2.1 The shape

> **A family is constituted by *determination clauses*. A clause says how a value is determined, and there is
> nothing else in a family.**

```
family
  ├── determination clause(s)
  │     argument shape :  observation | fiber-reducing | co-located
  │     source         :  THE WORLD   (observation only — this is where law runs out)
  │                    |  a cited universal law, with its identity-bearing parameters
  │     scope          :  the structural conditions, decidable from governed geometry alone
  │     premises       :  the value/data conditions
  ├── eligibility          which points the quantity applies to
  ├── contribution multiplicity   how many governed contributions sit at one point
  └── value-type reference        a governed CDT reference, possibly with an authored parameter
```

**An observational family** has a clause whose source is the world. **A constructed family has none** — its
ground is its operand, and the recursion terminates at observations (§5.4).

### 2.2 The four refinements the cases forced

1. **"Composition over fibers" is too narrow.** Cases 9 and 13a have **co-located** clauses and **no
   fiber-reducing clause at all**. There are **three argument shapes**, and ToD already names them (§§3.5–3.6,
   mapper versus reducer). The shape is part of the clause.
2. **"Participation/eligibility" is two facts**, not one: *which points the quantity applies to*, and *how many
   governed contributions sit at a point*. The second is analytical when contributions genuinely coincide, and
   realization otherwise (Ruling 9).
3. **The value-type reference is not atomic.** Case 13a: `Set<Text>` is *"not admitted merely from the bare
   spelling `Text`"* and needs **a declared exact-equality profile**. The parameter is authored; it sits in the
   type reference, not in the family law.
4. **`eligibility` must range over *eligible* points, never observed ones** — otherwise known-empty and unknown
   are indistinguishable and the empty-fiber case stops being entailed (§6.1: the identity applies to a *known*
   empty fiber, and *"is not a substitute for an unknown domain"*).

### 2.3 The rule the cases added

> **A premise may *gate* a clause; it may not *change* what the clause produces.** If a proposed premise changes
> the result's value domain or its meaning, it is a **law application** and must be a construction (case 12).

Without it, "premise" is an unbounded escape hatch. With it, §3.9 is satisfied rather than evaded: a changed
target gets a successor identity instead of hiding inside a condition.

### 2.4 Permitted but not forced by any case

**More than one observation clause.** A quantity independently observed at two granularities — line-level revenue
and an independently reported regional total — would be two grounding clauses with an **agreement obligation**
where both apply (§5.3, at the clause level). **No case here forces it, so the model permits it and this exercise
does not adopt it.** Flagged rather than claimed.

---

## 3. Classification of every fact

`AUTHORED` · `ENTAILED` · `NAMING` · `EVIDENCE-REALIZATION`. *(Governance is a fifth thing that is **not in the
declaration at all** — see §4.)*

| fact | class |
|---|---|
| the constitutive anchor a clause is stated over | **AUTHORED** (as a governed reference; the structure is entailed from the universe, the *choice* is contingent) |
| the observation clause — what quantity exists at a point | **AUTHORED** — the only irreducibly extra-formal fact in the system |
| eligibility | **AUTHORED** |
| contribution multiplicity | **AUTHORED** where contributions genuinely coincide |
| value-type reference | **AUTHORED** (a governed reference) |
| a type profile parameter — e.g. Text equality | **AUTHORED** |
| a clause's cited law | **AUTHORED** (a reference to a universal law) |
| a clause's identity-bearing law parameters — `ddof`, order choice, quantile convention, precision | **AUTHORED** |
| a clause's **scope** | **AUTHORED** |
| a clause's **premises** | **AUTHORED** |
| co-participation contract, for multi-operand laws | **AUTHORED** |
| target specification, **only** for a non-catalogued law | **AUTHORED** + §5.3 adequacy obligation |
| the family's **extension** \(\{A: F@A\ \text{is determined}\}\) | **ENTAILED** — notation, never an object |
| value capabilities of the cited type | **ENTAILED** (CDT's matrix) |
| result value domains | **ENTAILED** (law × operand domain) |
| sufficient-state bases, where a law is cited | **ENTAILED** (ToD Appendix A) |
| basis adequacy; cross-basis agreement | **ENTAILED** (§5.3) |
| direct/staged agreement | **ENTAILED** (Props 6.1, 6.2) |
| empty-fiber outcome | **ENTAILED** from the cited law + eligibility |
| the witness family for FIRST/LAST | **ENTAILED** (§8.1) |
| whether a family is observational or constructed | **ENTAILED** — presence of an observation clause |
| analytical lineage | **ENTAILED** — the operands the clauses name |
| \(\Sigma(F)\) / `family_id` | **ENTAILED**, with one unresolved handle (§4.3) |
| canonical names, aliases, default completion | **NAMING** |
| governed equivalence between two constructions | **NAMING/resolution** — §11.5.1 canonicalization, not identity minting |
| support, coverage, availability of a basis | **EVIDENCE-REALIZATION** |
| ratification / assurance | **EVIDENCE-REALIZATION** |
| bindings, carriers, plans, backend operators, precision, realization cardinality | **EVIDENCE-REALIZATION** |

---

## 4. Inherited concepts: gone, narrowed, or open

### 4.1 Disappear completely

| concept | the example that retires it |
|---|---|
| **\(P_F\) / `prohibited_constituents`** | cases 2, 4, 16 — a negative encoding of a missing clause, at the wrong index. **Delete; do not repair the 13-vs-14 producer gap** |
| **family domain as a constituted object** | cases 10, 11 — definedness is *below* anchor granularity, so no per-anchor object could carry it |
| **B-anchor / `BLOCKED` as ontology** | case 16 — what it rejected is a standard financial quantity |
| **family root \(A_0\)** | every case — one anchor per clause suffices |
| **`formation.kind`** | entailed by the presence of an observation clause |
| **`domain` / `movement` declaration fields** | one is notation, the other is edge validity |
| **stock / flow / semi-additive / basis kinds** | case 11 — under one representation Revenue's clause *is* Balance's shape |
| **`CONSTRUCTED_DOMAIN_UNDECIDED`** | cases 5–8 — nothing is undecided |
| **a reducer token in a realization mapping** | the clause is governed law |

### 4.2 Survive, narrower

| concept | narrowed to |
|---|---|
| **\(\mathcal A_F\)** | **notation only** — the extension of a partial law |
| **C7 / sufficient-state** | **establishment only, never standing** (case 8's second reading) |
| **C8 / continuation** | **is** a fiber-reducing clause |
| **C6 / semantic values** | a governed reference plus consequences |
| **C5 / participation** | two facts, over **eligible** points |
| **\(\Gamma_F(B\to A)\) / edge validity** | whether a *path* exists between two locations the family already stands at |
| **`WITHHOLD`** | unchanged — governance, *"the author's rule… not the engine's analytical judgment"*, **outside the declaration** |
| **`blocked_edges`** | unchanged — want of evidence about a refuted edge |
| **MAP1** | a conservative **default co-participation** rule, not a domain rule |

### 4.3 Genuinely open

1. **The law of a non-catalogued construction.** Per instruction, identified and **not solved**. Case 9 shows the
   shape of the gap precisely: **AOV has a co-located clause and no fiber-reducing clause, and nothing derives
   that from the ratio.** The missing constitutive act is: *for a law not in the catalogue, the author must
   supply its argument shape, its scope, its premises, and its target — i.e. the law itself.* **The model cannot
   entail a law it was not given, and should not be extended by guessing.**
2. **The identity handle on the observation clause.** It is necessarily identity-bearing and cannot be
   canonicalized. Conservative re-ratification on textual change is the Ruling 8 trade.
3. **`eligibility` is a bound**, jointly determined with the resolved request (§4.2); where request-local
   restriction becomes target change is unsettled.
4. **Universe questions, upstream and untouched:** Case G (case 3 depends on it), whether `day→week` is
   constituent-forgetting or a placement, whether the world's `week` projects onto its `month` (case 8), and the
   ratification of §§1–6 of the 2026-09-15 record.

---

## 5. Facts that turned out to belong **upstream**

This is why the family declaration became small. Each was at some point treated as a family fact:

| fact | belongs to |
|---|---|
| governed order on a constituent | **universe** (case 7) |
| projections between anchors, incl. calendar relationships | **universe** (cases 4–8) |
| Case-G placements such as `store → region` | **universe** (case 3) |
| currency as an analytical constituent | **universe individuation** (case 11) |
| a governed conversion to a numéraire | **universe** (case 12) |
| constituent identity and value domains | **universe** |
| equality/collation profiles for a value type | **CDT**, referenced by the family (case 13a) |

> **Only two of the sixteen cases required *any* new authored fact at the family layer: case 9's co-participation
> contract and case 15's co-participation plus `ddof`.** Everything else was either already declared, entailed,
> or a universe fact.

---

## 6. Changes this implies for the ToD v7.2 development journal

**Notes only. The theory is not edited here, and nothing below is adopted.**

| entry | action | why |
|---|---|---|
| **A.1** — the family root and the generated Case-S domain | **WITHDRAW** | both objects it introduces disappear. \(A_0\) is not needed (one anchor per clause); \(P_F\) is a negative encoding of a missing clause at the wrong index. A.1.8's *"constructed-family propagation"* open question **dissolves rather than resolves** — there is no propagation relation to decide |
| **A.2** — identity standing of the family root and the family domain | **WITHDRAW** | moot once A.1 goes. Its live insight survives elsewhere: a **clause** is identity-bearing (§3.9's continuation trigger), and governance restriction is not — but that is now the `WITHHOLD` boundary, not a property of a domain object |
| **A.3** — family splitting, recovered from v6.1 | **ADOPT** (drafted as `tod_v7_2_journal_candidate_a3_family_splitting.md`) | *"different analytical directions… produce distinct family identities even when everyday language reuses one label"* is the published form of what cases 5 and 16 demonstrate |
| **A.4 (new)** — the determination-clause model | **DRAFT** | the shape in §2: argument shape × source × scope × premises; scope/premise separated by decidability; a premise may gate but not change |
| **A.5 (new)** — the distinct failure kinds | **DRAFT** | law-to-type inadequacy · want of type coverage · want of law · undefined result · want of state · realization · withhold. §9.4 already forbids disclosing over the fourth |
| **§4.1** — *"\(\mathcal A_F\) … not a proposed registry or new object"* | **CONFIRM, do not change** | the exercise vindicates it. What v7.1 never said — *from what* the domain is generated — is now answered by the clauses, not by a new object |
| **§5.2** — *"compose across **admitted refinement**"* | **SUPPLY THE FILLER** | v7.1 leaves *admitted by what?* unstated. The answer is: by a clause's scope. This is the smallest theory change the model needs |
| **§7.2** — *"the family must resolve which one it uses"* | **CONFIRM** | case 7: entailed where the world admits one order, authored where several |
| **§11.5.1** — canonicalization of a named family with a construction | **CONFIRM and lean on** | case 5's `sum(revenue@line)` ≡ `revenue` is exactly this, and the model needs no other mechanism |

**Not proposed for the journal:** any restoration of \(\beta\), \(\mathcal C_L\), or draft4 §10.1's premise 5;
any new ontological kind; and any resolution of the non-catalogued-construction question.

---

## 7. Reconciliation notes — Measure Algebra, MEL, Frame-QL

**Notes, not edits.**

### 7.1 Measure Algebra

- **\(\beta\) is capability-indexed by definition** — \(\beta:\mathsf{AggCap}\to\mathcal P(\mathsf{Axis})\),
  *"intentionally operator-indexed"*. **It must never be imported family-indexed.** What its index carried is
  now carried by **the clause's law citation**: a clause names both its law and the fibers it is claimed over,
  which is the same information stated positively.
- **rev1's deletion of \(\mathcal C_L\)/\(\mathrm{Adm}_\Gamma\) removed the vocabulary separating law-level
  meaning from local prohibition from realization.** Per Huayin's direction, **do not restore it wholesale.**
  The simpler reconstruction the model supports is:
  **law determines meaning → governance may withhold → evidence/profile determines servability.**
- **§9.1's slogan overstates its own body text.** *"MEL generates the governed family space"* is a constitution
  claim; §2.1's *"MEL supplies the canonical analytical expression"* is a denotation claim, and the body hedges
  toward the second (*"where lawful"*, *"lawfully generated family **expressions**"*). **Reconcile toward §2.1.**
- **MAP1 is a conservative default co-participation rule** (\(E'=\bigcap E_i,\ S'=\bigcap S_i\)), which cases 9
  and 15 show is a **real** recurring premise. Its \(\beta'\) union is not a domain rule.
- **§30.4's *"a general multi-parent family-formation calculus"* is precisely §4.3(1)**, and the model confirms
  it is still open rather than closing it.
- **§14.5 survives intact and is load-bearing** — *"Composite sufficient state does not imply composite measure
  identity"* is what keeps case 8's three objects apart.

### 7.2 MEL

- **MEL is parametric and it denotes; it never constitutes.** It knows `mean(X @ A) @ B`; it learns that `X` is
  Balance only when a Manifold supplies the governed operand. Every case above respects this — the Manifold
  supplies operands and clauses, MEL supplies the expression.
- **MEL must carry the argument shape**, because the shape is identity-bearing: `mean(X@I)@A` and `X/Y@A` are
  different kinds of object, not different spellings. It already does.
- **Canonicalization is the mechanism case 5 needs**, and no other: `sum(revenue@line)` ≡ `revenue` under a
  **governed equivalence** where the clause, operand and participation agree — *"It is not string aliasing."*
- **§10's anchor elimination is already conditional in the right way** — *"**If** the SUM law and the applicable
  closure profile establish regrouping invariance"* — and the clause is what establishes that premise.

### 7.3 Frame-QL

- **The disposition vocabulary needs more distinctions than it has.** At minimum, **undefined result** (case 10)
  is neither want of law nor want of state, and §9.4 forbids serving it with a caveat. And **law-to-type
  inadequacy** (case 13b) is anchor-invariant and must not be reported as want of law.
- **`Clarify` is the workhorse of this model and must not be replaced by prohibition.** Cases 5, 8, 11 and 16 all
  resolve to Clarify, and in each the old instinct was to refuse one of the readings. *"Monthly inventory"*,
  *"total balance"*, *"monthly average balance"*, *"revenue by region"* in a multi-currency world.
- **"Not pre-enumerated" must never be Refuse.** The Manifold is finite; the family space is not.
- **§6.5's contract list — *"admitted anchors and movements"* — needs reconciling.** Admitted anchors are
  **derived notation**, not a fact the Manifold supplies. Movements are edge validity. Frame-QL should resolve
  against clauses, not against an anchor list.
- **§3.1 is confirmed by case 3** — `revenue @ {region}` *"does not need to become `sum(...)`… The query names
  the family identity."* This reading is only coherent when standing comes from the family's own clause, which
  is what the model supplies.

---

## 8. The success criterion

Could a person look at this and say *"yes, these are exactly the contingent facts about my analytical world that
I actually had to tell the system"*?

For Revenue and Balance: **five facts each, three of them identical, differing in one sentence and one
quantifier.** For the fourteen derived cases: **two new authored facts in total**, both co-participation
contracts, plus law parameters where a law genuinely has a convention. Everything else was a universe fact, a
CDT reference, or a theorem.

**What a person must say is: what they observe, where, for which points, in what units, and how it composes.**
**What they must not say is anything that follows from that.**

**Stopped here.** No schema, no serialization, no implementation plan, no code changes.

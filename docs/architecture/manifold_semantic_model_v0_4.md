# The smallest coherent Manifold declaration model

> **SUPERSEDED for the model.** The current positive statement is
> [`columna_semantic_contract_v1_0.md`](./columna_semantic_contract_v1_0.md), which a fresh reader should read
> instead. This record is retained for the case-by-case derivation and for Appendix S's supersession trail.

**Design record.** Recorded by Claude at Huayin's direction, 2026-09-24.

**Standing.** Design and reconnaissance. **No implementation, no schema, no migration, no repair.** Stops at the
model, the acceptance cases, and the recommended units.

**Method.** Declaration-first. Current publication structures, `prohibited_constituents`, C3,
`CONSTRUCTED_DOMAIN_UNDECIDED`, legacy `BLOCKED`, producer limits and resolver organization are treated as
implementation evidence to reconcile later, never as constraints on the model.

---

## 1. The recommended semantic model

### 1.1 One recursion, two kinds of clause

> **A family is grounded either in the world or in another family.**

```
family  ::=  GROUNDING  +  COMPOSITION*        -- observational
        |    LAW-APPLICATION over established inputs   -- constructed
```

The recursion terminates at observations, which is ToD §5.4's well-foundedness read from the declaration side.

**Clause kinds, and the difference between them is the constitutive/nomological boundary made structural:**

| clause | cites | how many |
|---|---|---|
| **grounding** | **the world** — what quantity exists at a point of this anchor | **exactly one**, and only in an observational family |
| **composition** | **a universal law** — what the quantity is over a fiber | **zero or more** |

Exactly one clause in the whole system is grounded in something that could have been otherwise and cannot be
proved. Everything else cites law. **That is the entire contingent surface of a family.**

### 1.2 What a composition clause is — and the two stress-test results

The candidate was `law × fiber scope × premises`. It survives, **with the tuple's slots given principled
boundaries rather than assumed ones.**

\[ \textbf{composition} \;=\; \underbrace{\text{cited law (with its identity-bearing parameters)}}_{\text{which
universal law}} \;\times\; \underbrace{\text{scope}}_{\text{structural conditions}} \;\times\;
\underbrace{\text{premises}}_{\text{value/data conditions}} \]

**Result A — scope and premise are not arbitrary slots. They are separated by *when the condition can be
decided*.**

> **Scope** is any condition decidable from **governed geometry alone**, before data.
> **Premise** is any condition requiring the **values**.

This is not a syntactic convenience; it is load-bearing for the refusal taxonomy, and it is the only principled
line available:

| fails | consequence | disposition |
|---|---|---|
| **scope** | the law is not claimed over these fibers; **no value is determined anywhere at this anchor** | **want_of_law** |
| **premise** | the law is claimed here; **the value is undefined at *this point*** | **undefined result** (§9.4 forbids disclosing over it) |

Case 11 versus case 12 (§3) shows the same analytical concern landing in either slot depending on how the world
is represented, which is why the line must be drawn by decidability rather than by subject matter.

**Result B — a premise may *gate* a composition; it may not *change* what the composition produces.**

If a proposed premise changes the result's value domain or its meaning, **it is a law application in disguise
and must be a construction, not a premise.** Case 13 is the witness: a currency conversion "premise" produces a
value in a different numéraire, so it is a law (`convert`), and the family it yields is a different family.
Without this rule, premises become an unbounded escape hatch and the clause model collapses into arbitrary code.

**Parameters are inside the law citation**, not a fourth slot: `LAST[order = O]`, `variance[ddof = 1]`,
`quantile[convention = q]`. A parameter *selects among laws*; a premise *gates* one. Different things.

**Result C — a clause also has an *argument shape*, and my first statement of the model was incomplete.**
Case 16 forced it: AOV does **not** reduce a fiber. `revenue(A) / order_count(A)` consumes **co-located measures
at the target anchor** — §5.1's anchor-local constructor. Writing that as a fiber scope would be false.

There are exactly **three** argument shapes, and **ToD already names them** (§§3.5–3.6, mapper versus reducer):

| shape | the clause consumes | examples |
|---|---|---|
| **observation** | the world, at a point of the constitutive anchor | `revenue`, `balance` — the grounding clause |
| **fiber-reducing** | the operand's values over the fiber (the operand may be the points themselves) | `SUM`, `MEAN`, `COUNT`, `LAST`, `distinct_set` |
| **co-located** | already-established measures **at the target anchor** | `AOV`, ratios, differences, covariance — §3.5's pointwise and tuple readings |

So a clause is **argument shape × cited law (with parameters) × scope × premises**, and the grounding clause is
simply the observation shape, which admits no law because it *is* where law runs out.

**Clauses must agree where they overlap.** If two clauses both determine a value for the same fiber, they must
determine the same one — §5.3's cross-basis agreement obligation, at the clause level. That is an **obligation on
the author**, not a further declared fact.

### 1.3 Absence, and the two states

**Absence of a composition clause is not a prohibition and does not become permission.** It means no such
meaning has been established. Two states, positive, no polarity apparatus and no three-state machinery:

\[ \mathcal A_F=\{A:\ F@A\ \text{is defined by the law of}\ F\} \]

— **descriptive notation for the extension of a partial law. Never an authored, serialized or governed object.**

### 1.4 The four authorities, unchanged

**Manifold constitutes · Measure Algebra entails · MEL denotes · Frame-QL requests.** Plus, strictly separate and
below the analytical line: **governance may withhold**, and **evidence/realization determines servability.**

---

## 2. The minimal authored facts

### 2.1 Observational family — **five**

| fact | class |
|---|---|
| **`at`** — the constitutive anchor | **governed reference** to structure proved from the universe constitution; **which** anchor is contingent. Carries the universe (Ruling 2026-09-14: *"the universe is a precondition of resolution, not a component of the identity"*) |
| **`observes`** — the grounding clause | **contingent**, and the only irreducibly extra-formal fact in the system |
| **`participates`** — a rule over **eligible** points, with multiplicity at a point | **contingent**; factorable to a governed profile default |
| **`valued in`** — a CDT type | **governed reference**; which type is contingent |
| **`composes`** — zero or more clauses | **contingent** |

### 2.2 Constructed family — **the expression, plus only what its law cannot entail**

A construction is **denoted**, not declared. What it may still require:

| when | fact |
|---|---|
| the law takes an order | a **governed order on the constituent** (a *world* fact) + **which order**, if the world admits several (entailed when exactly one) |
| the law takes several operands | a **co-participation contract** |
| the law takes a convention | `ddof`, quantile interpolation, sketch precision — a **law parameter** |
| the law is **not catalogued** | a **target specification** and bases, with §5.3 adequacy |

### 2.3 Derived, and therefore unstatable

\(\mathcal A_F\) · any prohibition set · admitted-anchor lists · edge lists · additivity flags · stock/flow kind ·
`primitive|constructed` discriminator · lineage · result value domains · value capabilities · sufficient-state
bases where a law is cited · basis adequacy · path agreement (Props 6.1/6.2) · cross-basis agreement · empty-fiber
values where the law and participation settle them · \(\Sigma(F)\)/`family_id` · the witness family for FIRST/LAST.

---

## 3. The sixteen acceptance cases

```
universe sales    individuates { store, day, order, line }   exists_when a line was transacted
universe ledger   individuates { account, day }              exists_when the account is open that day
```

```
family revenue                                family balance
  at           : sales.{store,day,order,line}    at           : ledger.{account,day}
  observes     : the consideration accruing      observes     : the amount standing to the account
                 from the line                                  at the close of the day
  participates : every eligible point, once      participates : every eligible point, once
  valued in    : CDT Decimal                     valued in    : CDT Decimal
  composes     : SUM over ANY fiber              composes     : SUM over fibers varying only in
                                                                { account }
```

### 3.1 Cases 1–9, in the five-way separation

| # | case | author constitutes | follows by ToD/MA | MEL denotes | Frame-QL may request | may fail only on evidence/realization |
|---|---|---|---|---|---|---|
| **1** | observational Revenue | the five facts above | \(\mathcal A\) = every anchor reached by projection; empty fiber → the monoid identity where known-empty; `sum(revenue@…)` **is** this family | `revenue` | the family by name | support; carrier exactness (2026-09-12) |
| **2** | observational Balance | the five facts, differing in `observes` and one quantifier | \(\mathcal A=\{\{account,day\},\{day\}\}\) | `balance` | the family by name | as above |
| **3** | `revenue @ region` | **nothing further**; `region` needs a governed placement or constituent | the clause is stated over **any** fiber, so it determines a value here | the measure | `SELECT revenue AT {region}` | support; coverage → **Disclose** |
| **4** | `balance @ week` | **nothing, and nothing would help incrementally** | **no clause covers fibers varying in `day`** → **want_of_law**. Not prohibited — *undetermined* | the expression denotes; the **family standing is what fails** | it may ask | n/a — it never reaches evidence |
| **5** | `sum(revenue @ sale)` | nothing | Revenue's `composes` **is** the SUM clause over the same operand with the same participation → §11.5.1 canonicalization: *"A named family such as Revenue may already denote the same construction"* | the construction | either spelling | as case 1 |
| **6** | `sum(balance @ day)` | nothing | Balance's clause does **not** cover day-varying fibers, so this is **a different family** — v6.1: *"distinct family identities even when everyday language reuses one label"*. Its own law is complete: Σ over any fiber of balance point-values | the construction | yes — and it **Serves**, under its own identity | support |
| **7** | `mean(revenue @ sale)` | nothing | MEAN over any nonempty fiber; participation from the operand's rule; **result type `Rational`** — exact division is not closed in Decimal; empty fiber **undefined** | the family | yes | Σ and N availability → **want_of_state** |
| **8** | `mean(balance @ day) @ week` | **nothing** | MEAN consumes Balance's **grounding** clause at singleton fibers, never its composition. Stands at `{account}`, `{day}`, `{}`, and at `{account,week}` given the projection | the measure | yes | Σ/N at week; partial day coverage → **Disclose** |
| **9** | `last(balance @ day) @ week` | **a governed complete order on `day`** (world) + **which order** if several (family) | witness family \(W\), basis \(\{W\}\to L\), witness monoid, known-empty \(\bot\) — all §8.1–8.3. Stands **wider than Balance itself** | the family and its measure | yes | witness availability |

**Case 4 is the acceptance test for the whole model.** It must refuse, it must refuse for the *right* reason,
and no incremental authored fact may repair it — because the correct repair is to ask a different question
(case 6, 8 or 9), not to widen a permission.

**Case 6 is the acceptance test for the old instinct.** The number is lawful and servable. Only its *label* was
ever the problem.

### 3.2 Case 10 — mean-of-mean, and the two things it is confused with

**Three distinct objects, and only the first is a new family.**

```
(a)  mean( mean(balance@day) @ week ) @ month     a NEW family: the unweighted mean of weekly means
(b)  mean(balance@day) @ month                     THE SAME family as M1, at a coarser anchor
(c)  the error                                     using (a)'s value where (b) was wanted
```

**(a) is a second formation.** Its operand is \(M_1\) established at `{account,week}`; its constitutive anchor is
`{account,week}`. Author cost: **zero**. MEL denotes it; Frame-QL may request it; it Serves.

**(b) is not a new family at all.** \(M_1\)'s own clause — MEAN over any nonempty fiber of `{account,day}` —
**already determines a value at `{account,month}`**. Its *meaning* was fixed the moment \(M_1\) was constituted.
What is at stake is only **establishment**: the anchor-local constructor needs \(\Sigma\) and \(N\) over the
month-fiber.

> **This is the case where C7 must not be allowed to manufacture or destroy standing.** If the weekly *scalar*
> is all that is retained, (b) is **want_of_state**, not want_of_law — §5.2: *"For MEAN, a displayed scalar
> generally loses the weight required for exact continuation. **Its SUM and COUNT basis retains that
> information.**"* The meaning never went anywhere; the state did.

**The weighted reconstruction** of the population mean from weekly state is therefore **(b) established through
its basis** — \(\Sigma\) and \(N\) at week, recombined — and **not** a third family. §3.7's child-state case,
\((100,1)\) and \((300,2)\) combining to \(400/3\) *"not the unweighted mean 125 of the displayed child
ratios"*, is precisely the statement that **(a) ≠ (b)**, which is what makes both declarable.

**Frame-QL's obligation:** *"monthly average balance"* matches (a) and (b) and a mean of closing balances →
**Clarify**. Explicit MEL → **Serve**.

### 3.3 Cases 11–13 — currency, and the sharpest stress-test of the clause model

**Case 11 — currency as semantic value/type.** `revenue valued in Money = (amount, currency)`. `+` on Money is
**partial**: defined within a currency, undefined across. So:

```
composes : SUM over ANY fiber  GIVEN the fiber is currency-homogeneous
                               ^^^^^^ a PREMISE -- needs the values
```

`revenue @ {region}`: the family **stands** at `{region}` — the clause is claimed over any fiber — and the
measure is **undefined at those region-points whose fiber spans currencies**. Determined at the anchor;
undefined at a point.

> **This is why a per-anchor domain object is the wrong granularity even for observational families**, and why
> §9.4 matters: *"A disclosure can state a limitation on an otherwise established, correctly described result.
> It cannot make arbitrary point selection determinate."* Undefined is not disclosable.

**Case 12 — currency as an analytical constituent.** `sales` individuates `{store, day, order, line, currency}`;
revenue's value is a bare Decimal. Now the *same* concern is structural:

```
composes : SUM over fibers varying only in { store, day, order, line }
                                           ^^^^^^ a SCOPE -- decidable from geometry
```

`revenue @ {region}` now **forgets `currency`**, which the scope excludes → **want_of_law**, decided before any
data. And `revenue @ {region, currency}` is determined.

> **The same analytical concern lands in a different slot depending on representation, and both are lawful.**
> Case 12 makes *"revenue by currency"* a governed analytical location; case 11 does not, but keeps amount and
> currency together as one value. **They answer different analytical questions and the model must not force
> either.** Note also the shape it gives Revenue: under representation 12, Revenue's clause looks **exactly like
> Balance's** — a scope excluding one constituent. The flow/stock difference is not even a difference of kind.

**Case 13 — a composition whose legality depends on a governed conversion.** Tempting:

```
composes : ... ; SUM over fibers varying in { currency }  GIVEN a governed conversion to USD
```

**Rejected, by Result B.** The conversion **changes the result's value domain** — the output is in USD, the
point values are not — so it is a **law application, not a premise**:

```
family revenue_usd  =  convert[to = USD, rate = <governed>]( revenue )     -- a CONSTRUCTED family
   composes : SUM over ANY fiber                                            -- entailed: USD is homogeneous
```

The governed conversion is a **world fact**; `convert` is a law; `revenue_usd` is a different family, and
**§3.9 is satisfied rather than evaded** — a changed target gets a successor identity instead of hiding inside a
premise.

> **The rule this case establishes: a premise may gate a composition; it may not change what the composition
> produces.** Without it, "premise" becomes an unbounded escape hatch.

### 3.4 Case 14 — point-in-time versus interval/range

Four objects that calendar vocabulary conflates:

| | what it is | model |
|---|---|---|
| **point-in-time quantity** | grounded at a point; no time-crossing composition | Balance |
| **"over the members of" an interval** | a composition over the fiber | `sum`/`mean` |
| **"at the end of" an interval** | a composition citing LAST with a **governed point order** | case 9 |
| **an interval-*valued* quantity** | the **value** is an Interval | CDT `Interval` |

The fourth is the trap. CDT gives `Interval` *"no intrinsic total order"* and *"no general analytical additive
claim"*, and warns *"`Interval` is therefore kept distinct from `Duration`"* and that a numeric encoding *"does
not make `Interval` an additive scalar"*. A family whose **value** is an interval is **not** a family **at** an
interval anchor — ToD §5.7: *"Internal value structure is not analytical location."*

**And "at an interval" as an anchor is a *universe* question, not a coarsening.** A world individuated by
`{account, week}` has weeks as root points; its `week` is not a fiber of anything, and anchor identity is
universe-relative, so it is **not the same anchor** as a `week` reached by projection from days. Comparing them
is universe passage.

> **Constraint honoured, explicitly.** The governed order LAST requires is ToD §7's **analytical point order**.
> It has nothing to do with the proposed `{a*b}` coordinate/presentation precedence, which is not adopted and
> which — even if adopted — **is not LAST/LAG/SCAN analytical order.** Nothing in this model uses that syntax to
> solve a family-law or governed-order problem.

### 3.5 Case 15 — the old B-anchor intuition, preserved without recreating BLOCKED

The canonical case, with `inventory` declared like Balance:

| request | model's answer | old mechanism's answer |
|---|---|---|
| `inventory @ month` | **want_of_law** — no clause covers day-varying fibers | refuse (`blocked_reduction`) — or **disclose**, in the ADR-036 measurement |
| `sum(inventory@day) @ month` | **Serve** — a different, lawful family, correct value, under its own identity | serve **CLEAN**, same number, caveat gone — *"nine spellings of one defect"* |
| calling the second *"monthly inventory"* | **Clarify** | not addressed |

> **The real analytical distinction is preserved exactly, and the prohibition is gone.** G0.7's content —
> *"typed, executable, and deterministic while still failing to inherit Inventory identity"* — is now structural:
> `sum(inventory@day)` was **never a candidate to be Inventory**, because Inventory's law has no such clause.
> The mechanism guarded *movements*; the defect was always *identity*.
>
> **And the leak closes with it.** DG-4 — a family declaring `FAMILY { last }` still serving `sum` across time
> *"because there is no bar to cross"* — cannot arise: absence of a clause is absence of meaning, necessarily.

### 3.6 Case 16 — multi-input requiring an explicit co-participation law

```
family average_order_value
  law             : revenue / order_count          -- nominated defining construction, §3.7
  co-participates : <contract>                     -- *** the one authored fact ***
```

Covariance is the sharper witness, because there the pairing is destroyed by reduction. §3.5: *"For covariance
and correlation, the pair must be established while the operand relationship is available. **Marginally supported
operands do not by themselves establish joint participation.**"* And the conservation rule: *"An operation cannot
use a relationship that was neither retained nor reconstructed from governed evidence."*

**Co-participation is a formation-time fact, not a domain fact.** For AOV: does the denominator count **every
eligible order**, or **only orders carrying revenue**? Two lawful worlds, different quantities, and §5.3
forecloses inference — *"Individually supported inputs drawn from incompatible populations do not form an
admitted basis merely because their types match."*

**Entailed, not authored:** result type `Rational`; **undefined** where `order_count = 0` (a value premise — the
same slot as case 11); and the child-state discipline, from §5.1 anchor-locality.

---

## 4. What becomes unnecessary, and what needs reinterpretation

**Willing to conclude that a concept should disappear, as instructed.**

### 4.1 Disappears entirely

| concept | why |
|---|---|
| **`prohibited_constituents` / \(P_F\)** | a **negative encoding of a missing law clause**, at the wrong index (family, not capability), the wrong granularity (per-anchor, while definedness is per-point), and the wrong polarity (enumerating leaks — DG-4 — and is spellable-around — ADR-036's nine spellings). **Delete; do not repair the 13-vs-14 producer gap.** |
| **C3 as a family-domain *standing*** | there is nothing to stand. *"Does the law determine a value here"* is answered by reading the clauses |
| **`CONSTRUCTED_DOMAIN_UNDECIDED`** | nothing is undecided. It did the right job — it refused long enough for the capability index to be found — and its job is over |
| **B-anchor / `BLOCKED` as ontology** | its real content is the composition scope, stated positively. ToD v6.1 already retired the mechanism; v7.1 has no trace of it |
| **family root \(A_0\)** | `at` is the one anchor. A second distinguished anchor carried only a presentation preference |
| **`formation.kind = primitive \| construction`** | readable from whether a grounding clause is present |
| **`domain` / `movement` declaration fields** | one is derived notation, the other is edge validity and not a family-identity fact |
| **stock / flow / semi-additive / "basis" kinds** | the scope of a composition clause. Refused independently by ADR-036 D6 **and** CDT v0.5 (*"a separate folklore taxonomy"*) |
| **a reducer/evaluator token in a realization mapping** | the composition clause is governed law; a mapping *"may not say 'resolve the contributions by sum'"* |

### 4.2 Survives, reinterpreted

| concept | reinterpretation |
|---|---|
| **C7 / sufficient-state bases** | **establishment only, never standing.** Case 10(b) is the test: meaning is fixed by the clause; whether Σ and N are retained is `want_of_state` |
| **C8 / continuation** | **is** a composition clause with a fiber-reducing shape |
| **C6 / semantic values** | a **governed reference** to a CDT type at observational leaves; everything downstream derived |
| **C9 / exceptional cases** | mostly consequences; authored only where the law leaves a genuine choice |
| **C1 / target** | the grounding clause, for observations; the cited law's nomination, for catalogued constructions; authored only for a **non-catalogued** law |
| **C2 / identity and ancestry** | `at` + the clauses; ancestry is derived from the expression |
| **C5 / participation** | survives, with the §5.1 constraint: **over *eligible* points, never supported ones** |
| **`WITHHOLD`** | survives exactly as it was — governance, *"the author's rule… not the engine's analytical judgment"*, strictly below the analytical line |
| **\(\mathcal A_F\)** | survives **as notation only** — the extension of a partial law. Never constituted, serialized, enumerated, cached or served |
| **\(\Gamma_F(B\to A)\) / edge validity** | survives, and is **not** a family-identity fact. Whether a *path* exists between two locations the family stands at |
| **`blocked_edges`** | survives unchanged — it was always **want of evidence** about a refuted hierarchy edge, and shares only a word with the rest |

---

## 5. Cases the model cannot explain without another governed fact

Four. Two are pre-existing and better located; one is genuinely open; one is a verification limit.

### 5.1 **Genuinely open** — a construction whose law is *not* catalogued

The model says: author the target, the bases, and §5.3 adequacy. **That relocates the problem, it does not solve
it.** It does not say what law an arbitrary composed family *has* — what its argument shape is, what scope its
composition is claimed over, what premises it carries.

> This is exactly the broadened question: **given a lawful construction over existing measures, what law does the
> resulting family have?** §3.1's rule — *`sum(X@I)` is a new family exactly when `X`'s law lacks that clause* —
> is a fragment of the answer, and `revenue / order_count` shows the general case is harder: AOV has a co-located
> clause and **no** fiber-reducing clause at all, and nothing in the model derives that from the ratio.
>
> **The model is correct and incomplete here. It should not be extended by guessing.**

### 5.2 **Pre-existing, better located** — identity over a prose grounding clause

`observes` is necessarily identity-bearing — it is the only thing separating `revenue` from `units` at one
anchor — **and it cannot be canonicalized.** Re-wording without changing meaning must not mint a successor;
changing meaning while keeping wording must. This is the open `family_id` question from a new direction.
Conservative re-ratification on textual change is the Ruling 8 trade: *"That costs one human confirmation. The
opposite error… is a publication that claims a human ratified a world he never saw."*

### 5.3 **Pre-existing, better located** — `participates` is a bound

§4.2 makes participation jointly determined by *"the law **and the resolved request**"*, and holds that *"any
restriction that changes the analytical target must remain explicit."* **Where request-local restriction becomes
target change is unsettled**, and it is adjacent to §5.1.

### 5.4 **Verification limit, not a gap** — the grounding clause is extra-formal

Consistency between `observes` and `composes` can be checked only with a human in the loop. An inconsistency
between them is a well-formedness defect **no machine will catch**. This is not a minimality failure —
§3.1's converse test shows the composition scope is a separate semantic claim — but it bounds what any gate can
promise.

### 5.5 Explicitly *not* gaps

**Geometry** — whether `day → week` is constituent-forgetting or a Case-G placement, and whether the world's
`week` projects onto its `month`. The model needs only that a **governed projection exist**, not how it was
constituted. **It is neutral on the held Case-G boundary**, which is a result, not an omission.

**Ambiguity** — *"average revenue per order"*, *"monthly average balance"*, *"monthly inventory"* each match
several lawful identity-distinct constructions. **Frame-QL `Clarify`.** The old instinct was to resolve these by
prohibiting all but one.

---

## 6. Recommended development units — **after agreement, not now**

Ordered by dependency. Each is small, independently reviewable, and none repairs C5.

| # | unit | why here |
|---|---|---|
| **U0** | **Ratify the model** — the two clause kinds, three argument shapes, scope-versus-premise by decidability, and Result B (a premise may gate, never change) | everything else is downstream, and the current rulings do not say any of it |
| **U1** | **Ratify universe constitution §§1–6**, which remain draft while §§7–11 are ruled | the model's `at` is a governed reference into a constitution that is not yet ratified. **This is the real blocker** |
| **U2** | **The refusal taxonomy**, as vocabulary only: `want_of_law` (no clause) · **undefined result** (premise fails at a point) · `want_of_state` · realization · withhold | it is the observable contract of the model and it can be specified before anything is built. Two undocumented compressions get fixed here: the prohibition asserted where nothing was adjudicated, and the identity guard emitted as `want_of_state` **with the rematerialize remedy** |
| **U3** | **Read-only clause resolution** for observational families — answer *"does the law determine a value at A"* from clauses, alongside the existing path, adjudicating nothing | proves the model against cases 1–4 and 15 without a format change |
| **U4** | **Delete, do not repair** — `prohibited_constituents`, `CONSTRUCTED_DOMAIN_UNDECIDED`, and the C3 family-domain standing | the 13-vs-14 producer gap is a field to remove. This unit is *subtraction*, and should be reviewable as such |
| **U5** | **Constructions resolve at zero cost** — cases 5–8, 10 | the payoff unit, and it is mostly deletion of gates |
| **U6** | **The two contingent premises** — a governed order on a constituent, and a co-participation contract — as small separate acts | cases 9 and 16; each is one fact with one governed home |
| **U7** | **Publication format break** | last, and only once U0–U6 have settled what is being published. No dual read, no shim |

**Not in any unit, and deliberately:** the law-synthesis question (§5.1), the `family_id` handle (§5.2), the
request-restriction boundary (§5.3), Case G, `{a*b}` precedence, and any restoration of \(\beta\) or
\(\mathcal C_L\).

---

## 7. Stop

Returned for review at the stop-gate: the model (§1–2), the sixteen cases (§3), what disappears (§4), what the
model cannot explain (§5), and the units (§6). **No implementation, schema migration, or repair.**

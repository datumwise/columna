# Does `Balance @ {week}` follow from Balance's two clauses?

**A bounded verification before accepting the abstract declaration contract as frozen.** Claude, at Huayin's
direction, 2026-09-25. Checked against **ToD v7.1** (working manuscript v0.4), **Frame-QL v7.1 §9**, the frozen
semantic contract, and the PR #343 declaration model.

## Verdict

| | |
|---|---|
| **Q1 — what does governed LAST select?** | **Huayin is right.** It selects under the **governed analytical-point order over the participating domain** — *not* the last materially supported or observed point. **My earlier wording was wrong** and conflated exactly what he says it conflated |
| **Does the correction deliver `LAST_day ∘ SUM_account = SUM_account ∘ LAST_day`?** | **No.** The residual obstruction is **governed sparsity of the participating domain**, which is an analytical fact, not a material-support fact. **ToD v7.1 §11.2 is the worked counterexample, with numbers** |
| **Does `Balance @ {week}` follow without a third clause?** | **No — for two independent reasons**, and the second is a gap in my contract rather than a fact about Balance |
| **Should §6 of the abstract contract be frozen as written?** | **No.** Its *conclusion* stands; **its stated reason is wrong**, and it is silent on a rule it needs. Three decisions are put to Huayin in §8 |

---

## 1. What LAST selects — Huayin is right, and the corpus is unambiguous

**ToD §8.2** defines the witness monoid over *"one participating domain \(D\subseteq S\)"*, with

> \(\bot\) means **known empty contribution state**. It does not mean zero, ineligibility, missing evidence,
> unresolved existence, or a semantic Null.

**ToD §2.3** keeps the three apart explicitly — *"A point can be absent from the universe, present but ineligible
for a quantity, eligible but unsupported, or supported with value zero. These are different analytical claims
even when a carrier represents several of them with row absence or a null."*

**ToD §4.2** — *"Participation is selected by the law and the resolved request; **it is not automatically the set
of surviving physical records or supported operand values**."*

**Frame-QL §9.1** — *"Analytical-point order and evidence enumeration are different."*

**And ToD §11.3** is the dedicated demonstration that *displayed LAST values from different participation
instances are not interchangeable* — precisely the error of letting support choose the winner.

> **So LAST is `argmax` over the governed participating fiber under \(\mathcal O_S\). Support has no vote.**
> **My phrasing — *"the last **observed** day can differ across accounts"* — was wrong**, in the frozen semantic
> contract (case 7), in the v0.5 record (case 17), and by inheritance in the abstract contract §6. It is
> corrected in §7 below.

---

## 2. But the correction does not deliver commutation

The obstruction survives the correction because it was never really about support. It is about **sparsity of the
governed participating domain**, which the theory treats as an ordinary analytical fact:

- **ToD §2.1.3** — *dimensions and **sparse compound anchors***;
- **ToD §7.1** — the lexicographic order is over *"the **existing** analytical points of \(S\)"*;
- **Frame-QL §9.2** — *"**The image need not fill the Cartesian product.**"*

**A participating domain may be ragged, and raggedness is governed, not evidential.**

### 2.1 ToD §11.2, which is this exact question, already worked

The manuscript's own example, transposed from Customer–Day to Account–Day:

| point | value |
|---|---:|
| \((C_1, d_3)\) | 80 |
| \((C_2, d_1)\) | 20 |
| \((C_2, d_2)\) | 40 |

*"No \((C_2,d_3)\) point is fabricated."*

| path | computation | result |
|---|---|---|
| **`SUM_customer ∘ LAST_day`** | per-customer LAST: \(C_1 \to d_3 \to 80\); \(C_2 \to d_2 \to 40\) | **120** |
| **`LAST_day ∘ SUM_customer`** | per-day SUM: \(d_1\to 20,\ d_2\to 40,\ d_3\to 80\); then LAST over days | **80** |

**120 ≠ 80**, with no missing data anywhere. ToD states the first explicitly — *"Summing the two per-customer
LAST values gives 120, a different construction from selecting one global LAST value"* — and then rules:

> **"Nor does the witness-coherence theorem prove that SUM and LAST commute across dimensions. An interchange law
> would need its own premises, including the relevant participation and alignment. Intermediate execution
> convenience cannot supply them."** — ToD §11.2

Three further published statements say the same thing from different directions:

- **ToD §4.1** — *"A global LAST of one Customer–Day value, a LAST taken separately for each customer, and a SUM
  of those customer results are **not automatically one family**. Each must retain its actual law and ancestry."*
- **ToD §6.2**, after proving composite coherence — *"It does not prove that **arbitrary changes of analytical
  law commute**."*
- **Frame-QL §9.5** — *"Selecting global LAST and summing separate customer LAST values are different
  constructions. **A claim that LAST and another family operation commute needs its own law.**"*

### 2.2 The same thing in the Balance idiom, because it is not a technicality

Account **B** closes Wednesday; account **A** opens Thursday. `Balance(A, Sun) = 80`, `Balance(B, Wed) = 40`,
`Balance(B, Mon) = 20`. Every eligible point is fully supported.

| reading | value | what it is |
|---|---:|---|
| `SUM_account ∘ LAST_day` | **120** | *the sum of each account's closing balance* — each account's final position, including the closed one |
| `LAST_day ∘ SUM_account` | **80** | *the ledger total as it stood at week-end* — the balance-sheet reading |

**Both are standard, both are meaningful, and an accountant would want different ones for different purposes.**
This is not a degenerate edge case; it is a question the business has to answer.

---

## 3. The actual crux — two candidate laws, not two views of one

Huayin's step *"for week `w` there is one governed last day `d_last(w)`, so both paths determine
\(\Sigma_{account}\,Balance(account, d_{last}(w))\)"* is **valid under one reading of LAST and not the other.**

| | law | what it does | is it ToD's LAST? |
|---|---|---|---|
| **(i)** | **`LAST`-of-fiber** — `argmax` over the participating fiber under \(\mathcal O_S\) | each account gets **its own** last participating day | **yes** — ToD §8.2's witness monoid is exactly this fold |
| **(ii)** | **`AT`-terminal-point** — evaluate at the period's designated final point | one day for the whole week, independent of account | **no** — a different law, and **undefined** where that point is not participating |

> **Under (ii) Huayin's commutation argument is correct.** Under (i) it is not, because there is no single
> `d_last(w)`: the fiber's maximum is a function of the fiber, and the fibers differ. **The disagreement was never
> geometry-versus-support. It is which of two governed laws `LAST` denotes** — and ToD has already chosen (i).

**And (ii) is a perfectly declarable quantity**, if that is what a business means. It is a different family, it
needs the terminal point to be participating, and it must say what it does when that point is not. The model
loses nothing by keeping them apart; it would lose a great deal by fusing them.

---

## 4. When *does* the interchange hold?

> **Two reducers over orthogonal axes interchange when the participating domain is a *rectangle* in those axes** —
> when \(q : S \hookrightarrow A_1 \times A_2\) **fills** the product over the region concerned.

- **Sufficient in general.**
- **Necessary whenever one of the two is a *selector*** (`LAST`, `FIRST`, `argmax`, a quantile). A selector's
  choice is a function of the fiber's *shape*; where the shape varies with the other coordinate, the selection
  varies with it. For two total monoid folds (`SUM` with `SUM`) raggedness is harmless, which is why the problem
  never surfaced before an ordered law entered a family.
- **It is a governed condition, checkable without measure evidence** — ToD §4.2 makes the participating domain
  governed, *"not automatically the set of surviving physical records."* **Huayin's instinct that any real
  obstruction must be a governed fact rather than an evidence fact was right; there simply is such a fact.**

So: in a world whose ledger eligibility is rectangular in `account × day` over the week — every participating
account participating on every day of the week — **the two paths agree**, and the only remaining obstacle is §5.

> ⚠ **And agreement in the instance proves nothing.** ToD §7.2: *"**Agreement of current winners is
> insufficient.**"* In §2.1's table, `LAST_day ∘ SUM` and the Day-then-Customer global LAST both return 80 — by
> coincidence, since \(C_1\) is the only customer at \(d_3\). Rectangularity must be established, never observed.

---

## 5. The second, independent reason — and it is a gap in my contract, not a fact about Balance

**Even where the interchange holds, the abstract contract does not determine `Balance @ {week}`**, because §4.1's
resolution function is **existential over single clauses**:

```
determines(F, A) ⟺ ∃ c ∈ Clauses(F) . scope(c)(I_c ⪰ A) ∧ …
```

**There is no rule that composes two clauses.** `forgotten = {account, day}` is admitted by neither
`over { account }` nor `over { day }`, so no clause applies and the question never reaches commutation.

**Huayin's proposal is therefore a real amendment**: close `determines` under clause composition. It has a
genuine motivation — without it, *"the total as it stood at week-end"* is reachable only by constituting a
separate family over `balance @ {account, week}`, which is writable but arguably the wrong shape for what is
plainly Balance.

**If closure is adopted, it must be guarded, and the theory says exactly how.** ToD §5.3 — *"Alternative bases
must agree"* — and §6.2's limit — *"it does not prove that arbitrary changes of analytical law commute."* So:

> **Entailment may produce a value only where the entailment is unique.** Where two composition paths provably
> agree, the composite is determined. Where they may differ, **the composite is simply not determined.**

⚠ **And this forces a distinction the contract does not yet make**, without which adopting closure would break
Balance outright:

| | what it is | disposition |
|---|---|---|
| **clause-level incoherence** | two *clauses* whose scopes both admit `A` and which provably disagree | **a declaration defect** — §4.4, unchanged |
| **path-level disagreement** | two *derivation paths* through clause composition that may differ | **silence, not contradiction.** No clause claimed the composite, so nothing was asserted about it |

Without the distinction, a ledger with ragged eligibility could not declare `SUM over {account}` **and**
`LAST over {day}` at all — which is absurd, since both are plainly legitimate. **A clause is a claim; a
composition path is a derivation the engine might attempt.** Two conflicting claims are a contradiction; two
conflicting derivations are an absence of meaning — which is §1.3 of the frozen contract, applied one level up.

---

## 6. What survives unchanged

- **The Balance-is-one-family proof (abstract contract §6).** Conclusion intact. Pairwise clause application still
  collides only at the identity projection, where `SUM` and `LAST` over a singleton fiber co-determine.
- **The coherence condition (§4.4) as the B-anchor's successor.** `LAST over {day}` alongside `SUM over {day}`
  still provably disagree **at a single location via single clauses** — still a declaration defect. Untouched.
- **Continuation is not formation.** Nothing here concerns operand consumption; `determines` still reaches
  another family only through a boolean at one location.
- **`source × scope`.** No source kind, no third factor, no field. A **resolution rule** is at issue, not the
  clause.

---

## 7. Corrections required, and one open item that turns out to be closed

| where | what is wrong | correction |
|---|---|---|
| frozen semantic contract, case 7 | *"the last **observed** day can differ across accounts"* | the last **participating** day; the obstruction is governed sparsity. Cite ToD §11.2 |
| `manifold_semantic_starting_point_v0_5.md`, case 17 | same phrase | same |
| abstract contract §6 | correct conclusion, **wrong reason**, and silent on the composition rule | rewrite per §§2–5 |
| v0.5 §4.3(5) — *"whether a **commutation obligation** could entail it instead is open"* | **not open** | **ToD v7.1 already ruled**: *an interchange law would need its own premises* (§11.2), and Frame-QL §9.5 repeats it. An item I recorded as open was settled in published text |

---

## 8. Three decisions for Huayin, and the freeze

**Do not accept §6 of the abstract contract as frozen until these are ruled.**

1. **Adopt composition closure on `determines`?** Recommended **yes**, guarded by unique entailment — otherwise
   an ordinary quantity is reachable only under an awkward shape.
2. **Adopt the clause-incoherence / path-disagreement distinction?** **Required if 1 is adopted**, or Balance's
   own declaration becomes ill-formed in any ragged ledger.
3. **Is rectangularity of the participating domain a fact a universe may declare**, so that `Balance @ {week}`
   is entailed where it holds? This is a **universe** question and is put, not answered.

**Everything else in the abstract contract is unaffected** and can freeze as it stands.

---

**Stopped at the verification.** No implementation, no serialization.

> **Note.** Huayin's message ended mid-sentence after question 1 (*"Keep…"*). Question 1 is answered in full
> above, together with the commutation verdict it was asked in service of. **If there were further numbered
> questions, they have not been seen** — send them and they will be picked up against this same material.

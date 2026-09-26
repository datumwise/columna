# Reconnaissance · what establishes `P_F` for a CONSTRUCTED family?

**Standing.** Read-only reconnaissance. **No rule is proposed and no gap is filled.** Where the
corpus determines an answer the derivation is shown; where it does not, the report stops at the
missing fact.

**Sources swept.** ToD v7.1 (primary), v7.0 freeze candidate and v6.1 (secondary, flagged); Measure
Algebra v1.0, v2.0 draft4, v2.0 rev1; MEL working draft v0.4; Frame-QL 1.0 adopted; Frame-QL Platform
Profile v0.3; our own rulings and records. Estate measured across all repos, all artifact formats,
and both `.bundle` files.

---

## 0 · The headline

> **The corpus determines nothing about how an operand's analytical domain constrains a constructed
> family's analytical domain — and both the theory and the algebra say so in their own words.**
>
> Measure Algebra rev1 **§30.4** lists *"a general multi-parent family-formation calculus"* among its
> **open obligations**. ToD's own §3.8 is titled *"Lineage and sufficient-state dependency answer
> different questions"*, and every domain-bounding statement in v7.1 attaches to the **basis**
> relation, not the **formation** relation.
>
> **This is not a gap we can close by reading harder.** Three candidate propagation rules were
> tested and all three fail **in both directions, from one root cause.**

---

## 1 · Facts established by the governing corpus

### 1.1 The only domain-propagation rule in ToD bounds the BASIS claim, not `𝒜_F`

§8.1 (`d777b3f6…:714`), verified first-hand:

> "Every target covered by **that basis claim** must admit the corresponding \(W@A\); a more
> restricted witness-family domain would yield a correspondingly restricted **basis claim**. (This is
> law-level domain admission…)"

The grammatical object is *the basis claim*, twice. And §5.3 (`:460`) forecloses the lift to the
family:

> "One basis may have a narrower declared application domain; **outside it the basis does not
> silently redefine the target.**"

§5.1 (`:428`) scopes the bound to a single plan and then denies universality in its own next sentence:

> "…**that particular plan** must first establish \(G_i@A\) under the law of \(G_i\)… **This does not
> say that every possible basis or intermediate path must be available whenever the target has
> another adequate derivation** (§9)."

> **F-1.** v7.1 contains an **anti-propagation** rule where one might have expected a propagation
> rule. A constructed family may be admitted where a given basis cannot reach. The intersection
> candidate is dead at family level before any counterexample is run.

### 1.2 The basis relation is not the formation relation — and the corpus titles a section to say it

**§3.8 is titled "Lineage and sufficient-state dependency answer different questions."** A constructed
family's formation **operands** (§3.1, §3.7) need not be its **basis roles** (§5.1). §8.1's bound is
on the basis edge; a constructed family's operands sit on the lineage edge.

> **F-2.** Citing §8.1 as precedent for operand-propagation is a category error. The recon of C3 had
> already recorded the general form: *"C7 constrains C3's content. It never supplies its authority."*

### 1.3 The lineage edge carries identity, and its content is stated exhaustively without domain

§3.7 states what the directed edge records; §2.2 states `Σ(F)`'s content; §4's table assigns operands
to *Identity and ancestry* and *Formation*, with *Domain and movement* a separate co-equal row.
**Admitted anchors appear in none of the operand-bearing lists.**

The decisive silence is **Appendix B.3** (`:1316`) — v7.1's *only* formal schema for a constructed
family, `F = L(E₁@I,…,E_m@I;θ)`:

> "where the **formation, participation, parameter identity, type requirements, bases, admitted
> movements, and exceptional cases** are governed."

Seven governed items. **Admitted movements are in. Admitted anchors are not.** The same omission
repeats in §2.2, §3.9's succession triggers, and §12.3's conformance list.

### 1.4 MAP1's union is a STIPULATION, not a theorem

All three MA versions share one textual structure: *"**Define:** … `β'(κ)=⋃ᵢβᵢ(κ)`, `γ'(κ)=⋂ᵢγᵢ(κ)`.
**Then the certified map rule is:** …"*. `β'` is introduced **before** the inference figure and then
appears **in the conclusion**. rev1 §3.8 classifies MAP1 as an *"inherited rule"* — never *theorem*,
which is the word used for G0.2, G1.6, G0.7 and G2.8.

> **F-3.** No proof obligation transfers. A different `β'` would not violate MAP1's soundness; it
> would be a different rule. **The union was a conservative design choice inside one rule's
> conclusion, not a result about how prohibitions compose.**

And its premise shape is load-bearing — rev1 §3.1: *"The shared \(U\) and \(A\) are part of the
premise shape… one conservative multi-measure formation law **at a common analytical location**."*
MAP1 is **anchor-preserving**. Family formation generally is not.

### 1.5 β is capability-indexed and total; `P_F` is neither — and that is not simply a loss

Platform Profile §7.2: *"`β(κ)` — axes capability `κ` may not spend… **Both are total over the
relevant capability vocabulary.**"* §7.4 says what totality buys: *"a second consumer does not inherit
permission merely because a first consumer could use the same state."*

But `P_F` carries a distinction β **cannot express**: three standings, where `absent ≠ declared []`
(measured, C5 record §1). β is binary — *"an empty prohibition set means unrestricted."* Importing
β's totality would **collapse** the two-level polarity the C3 contract exists to preserve.

> **F-4.** The capability index is dispensable for **stating** a family-level prohibition — D1 ruling
> #2 makes κ constitutive of the family, so a one-place `P_F` per family carries what `β(κ)` carried
> per (family, capability) pair. It is **not** dispensable for **deriving** one, because a derivation
> must quantify over a capability that appears in no operand's record. **The object is well-defined;
> the propagation is not, and both facts have the same root cause.**

### 1.6 The algebra states that it does not have this rule

rev1 **§30.4**, open obligations: *"a general multi-parent family-formation calculus"*; *"richer
participation laws beyond the strict MAP1 fragment."* MA v1.0 §7 records the same boundary from ToD's
side: v6.1 *"explicitly leaves a general algebra of multi-input family synthesis outside scope."*

β and γ occur in **MAP1 and RED1 and nowhere else**, in any version — `restrict_R`, `carve_R`,
`expand_χ`, `merge_{L,q}`, `φ`, `finalize`, and default completion are all silent on the negative
condition. There is no second data point from which to generalize.

### 1.7 Frame-QL cannot construct a family, so nothing constrains this from the request side

§1.2 assigns *"family formation under admitted analytical law"* to ToD. §11.4: *"does not add a
Manifold kind, a `DERIVED` syntax, a publication field, or a witness type."* **Construction is
entirely a publication-side act**, so any propagation rule must live in the publication, not the
request.

---

## 2 · Measured implementation facts

### 2.1 The estate

| | measured |
|---|---|
| well-formed constructions, all repos and formats | **21** |
| **maximum operand count, anywhere** | **1** |
| constructions with >1 operand | **0** |
| declaring any C3 content (`domain`, `movement`, `prohibited_constituents`) | **0 of 21** |
| `family_domain` standing | **unestablished, 21 of 21** |
| native-v3 constructions in a persisted artifact | **0** |
| constructions in the two `.bundle` files | **0** (head predates the `governed/` package) |

Nothing forbids a multi-operand construction: the only arity constraint anywhere is **`≥ 1`**, stated
three times, unbounded above, and **no foundation law carries arity information at all**. The two
places that refuse `n > 1` (`compile_v2.py:440`, `serving.py:315`) are *profile* capability limits,
downstream of resolution, and ToD v7.0 `:183` positively admits multi-operand formation.

### 2.2 ⟨measured⟩ `P_F` is currently **unproducible**

`manifold-agent`'s `BODY_KEYS` has **13** keys; Core's `FAMILY_BODY_KEYS` and `_FAMILY_KEYS` have
**14**. The missing key is `prohibited_constituents`, and `grep -rn "prohibited_constituents"
manifold-agent/src/` returns **nothing**.

It does not ignore the key — it **refuses** it, at `family.py:319-325` (*"carries unrecognised body
key(s) … neither may be published"*) and at `publication_v3.py:704`, which aliases the producer's own
13-key set as `FAMILY_BODY_KEYS` (`:66`).

**Why the suite does not catch it:** the conformance test asserts `FAMILY_BODY_KEYS == _FAMILY_KEYS`,
and both are **Core's**. It never reaches the producer.

> **M-1.** C5 shipped a governed declaration **no producer in the estate can emit.** This does not
> affect C5's law or its evidence — its tests construct artifacts directly — but **no real
> publication can currently carry `P_F`**, and every candidate answer to this mission's question
> requires a producer edit regardless of which way it is ruled. Not repaired; may want rowing.

### 2.3 ⟨measured⟩ R8's first branch is stated but unreachable

`native_domain.assert_within_domain` gates on `formation.kind` at `:106` — **before** the geometry
(`:117`) and **before** the `P_F` read (`:130`). `resolve.py`'s C3 branch, by contrast, reads
`prohibited_constituents` **unconditionally on formation kind**.

So a constructed family that *positively declares its own* `P_F` resolves `family_domain:
ESTABLISHED` carrying the right frozenset — **and is refused anyway.** R8 says *"if its own
declaration establishes `P_F`, use that declaration"*; that branch does not yet exist in code.

> **M-2.** Admitting the **declared-`P_F` construction** requires no propagation theory whatsoever.
> It is a strictly smaller decision than the general one, and it is already ruled.

### 2.4 ⟨measured⟩ C6 silently reads `operands[0]`

`resolve.py:250-251` resolves **all** parents (so cycle and existence checks fire) and then consumes
`parent_views[0]`. A two-operand `SUM` over `(decimal, integer)` resolves **`VALID: yes`**, `C6 =
decimal`, with a note true of one operand and silent about the other.

C6 is **the only responsibility that derives a value from an operand's resolved view**, so it is the
precedent any `P_F` rule would be compared against — **and it is not one that generalizes.** Not
repaired; may want rowing.

### 2.5 The only existing propagation implementation

Legacy `BLOCKED` is **dropped** at the record level (a derived column's `BAnchor` is left empty;
`DerivedShape` has no slot), then **re-derived per request** at plan time as a **union over the
transitive ancestry, keyed per reducer** (`planner.py:2186-2188`, `blocked.get(reducer, …)`).

ADR-036 D10 accepts the union on an explicit asymmetry — it *"may withhold a lawful continuation but
can never manufacture an unlawful one"* — and records it as possibly over-strict. **DG-6 is OPEN** and
says closing it needs a **declaration-surface law-synthesis mechanism, not a planner one**.

> **M-3.** Our own ledger already contains this question in its legacy form, already ruled OPEN, with
> the same diagnosis: the missing thing is a **declaration-surface** mechanism. Note also that the
> legacy union **keeps the capability index** (`blocked.get(reducer)`); it is not the index-free
> object a family-level `P_F` would be.

---

## 3 · Candidate rules and attempted falsifiers

Each candidate was evaluated as a pure function over declared prohibitions; the engine implements
none of them, so the verdicts below are **computed, not imagined**.

**The setting.** Universe `{store, day}`. `on_hand` is a **stock**: summing levels across days
double-counts, so the family `on_hand.sum` prohibits losing `day` — this is declared today, as
`afternoon.cml`'s `sum BLOCKED { calendar }`. Its sibling `on_hand.max` prohibits nothing.

### FALSIFIER A — `COUNT` over a stock. **All operand-derived candidates OVER-prohibit.**

Construction: `count(on_hand@…)`, law `COUNT`, one operand. Ask `AT {store}`, which forgets `day`.
**Counting snapshots across days is lawful** — a count of points is not a sum of levels.

| candidate | `P_F` | verdict | |
|---|---|---|---|
| union (MAP1 re-indexed) | `{day}` | **REFUSE** | over-prohibits a lawful count |
| intersection | `{day}` | **REFUSE** | over-prohibits |
| inherit `operand[0]` | `{day}` | **REFUSE** | over-prohibits |

### FALSIFIER B — the steward's case. **All operand-derived candidates UNDER-prohibit.**

`map(revenue.sum, on_hand.max)` then `SUM` across `day`. `β_{on_hand}(max) = ∅` and
`β_{revenue}(sum) = ∅`, so every family-level combination is `∅` — while the prohibition that the
downstream `sum` must trip lives at `β_{on_hand}(sum) = {day}`, **which no operand's family-level
record reaches.**

| candidate | `P_F` | verdict | |
|---|---|---|---|
| union / intersection / inherit | `{}` | **ADMIT** | admits summing stock levels across days |

### FALSIFIER C — silence becomes standing. **Defeats union specifically.**

⟨measured⟩ **21 of 21** constructions have operands whose domain law is *unestablished*. A union over
zero established laws is `∅` — and a **declared-empty** `P_F` reads `ESTABLISHED, prohibits nothing`.
That **manufactures a positively-established domain law out of silence**, against R4 (*"absence of
prohibition is not permission"*) and against the two-level polarity the C3 contract preserves.

### The root cause, and it is one thing

> **A prohibition is a fact about a QUANTITY. A formation law CHANGES the quantity.**
>
> `count(on_hand)` is not a level; summing it across days is lawful where summing `on_hand` is not.
> `sum(map(revenue, on_hand.max))` *is* level-derived, though neither operand's record says so.
> Over-prohibition and under-prohibition are the same failure seen from two sides: **the operands'
> prohibitions are facts about the operands' quantities, and the construction is a different
> quantity.** No function of the operands' prohibitions alone can be right, because the information
> that decides it lives in the formation law.

### Falsifiers that defeat EVERY candidate, including independent declaration

**G2.8 — the construction-created tagged axis.** MA v1.0 §2.5: *"if `χ` uses replication, `κ` lacks a
duplication-invariance declaration, and a downstream reducer spends a **tagged target axis**, no
inherited certification derivation crosses that reducer… **Reachability therefore does not determine
disposition.**"* The tagged axis is **created by the expansion**, so no prohibition set fixed ex ante
over `U`'s constituents can contain it — including one the constructed family declared for itself.
This is a **scope** falsifier, not a choice-between-rules falsifier, and `tod_v7_2` §A.1.7 already
fences it: outside Case S the rule *"should be expected to fail rather than extended."*

**Ordered / non-commutative formation laws.** *"Two movements may forget the same constituents while
only one regroups lawfully."* A test on forgotten constituents alone cannot distinguish them. Vacuous
while every registered law is commutative — ⟨measured⟩ all five are — and **not a theorem**.

---

## 4 · Contradictions and missing governed facts

**The missing governed fact, characterized and not filled:**

> **How a formation law transforms a prohibition.**
>
> Falsifiers A and B establish that `P_F` for a construction is **not a function of its operands'
> `P_F` alone**. The deciding information is in the formation law — `COUNT` of a stock is not a
> stock — and ⟨measured⟩ **`FoundationLaw` carries no domain-shaped field**: it has
> `operand_domains`, `result_domain`, `entails_continuation`, and nothing from which a prohibition
> could be entailed. The five registered laws' `required_parameters` are all empty.
>
> This is the same shape DG-6 named for the legacy case: *"closing it needs a general law-synthesis
> mechanism — a way for a map composition to POSITIVELY establish a successor law — which is a
> **declaration-surface question**, not a planner one."*

**A recoverable deletion, reported because it bears directly.** MA v2.0 **rev1 deleted** draft4
§10.1's six-premise anchor-elimination judgment, whose **premise 5** — *"no restriction, carve,
**family-changing map**, or other identity-changing operation intervenes"* — is **the only sentence in
the algebra that puts a family-changing map in the way of a forgetting.** rev1 also dropped `𝒞_L` /
`Adm_Γ(L,o)` and the principle that *"local prohibitions and implementation gaps do not redefine that
universal law."* **The version of record is the one that lost the vocabulary for "a local prohibition
on a family."** If any of it is wanted as authority it must be **re-adopted from draft4**, not cited
from rev1.

**No contradiction was found** between the corpus and our shipped rulings. R3, R8 and
`CONSTRUCTED_DOMAIN_UNDECIDED` are all confirmed correct by this sweep: the union proposal that R3
withdrew is falsified twice over, and for the reason R8 gives.

---

## 5 · The smallest questions requiring a ruling

**Q-1 — the smallest, and already half-ruled.** R8 says *"if its own declaration establishes `P_F`,
use that declaration."* ⟨measured⟩ the scope gate refuses such a family anyway (§2.3). **Should a
constructed family that positively declares its own `P_F` be admitted on that declaration?** This
needs **no** propagation theory, and every falsifier above is about *derivation*, not declaration.
Ruling it would close the constructed case for every family that declares, leaving only the
undeclared case open.

**Q-2 — the authority boundary.** For a construction that does **not** declare, is `P_F`
(a) **unestablished**, exactly as a primitive that does not declare — so `𝒜_F = {A_0}` and nothing
moves; or (b) something the formation law is expected to entail, in which case the missing fact of §4
must be supplied first? ⟨measured⟩ (a) is what the code does today, and it is consistent with R4 and
with the two-level polarity. **Naming (a) as the ruled position — rather than a consequence of the
gate — would make the constructed case closed-by-default rather than undecided.**

**Q-3 — whether to re-adopt the deleted premise.** Does draft4 §10.1 premise 5 (family-changing map
as a barrier) carry authority, or does rev1's deletion stand? This is the only corpus sentence that
would constrain forgetting across a construction, and it currently has no force.

**Not asked, deliberately.** What the propagation rule *is*. Falsifiers A, B and C establish that the
three obvious candidates are wrong; they do not establish what is right, and §4's missing fact must be
supplied before any candidate can even be stated. **Inventing it here would be exactly what R8
forbids.**

---

## 6 · Recorded, not acted on

* **M-1** — `P_F` is unproducible: the producer refuses the key C5's consumer reads.
* **M-2** — R8's declared-`P_F` branch is stated but unreachable (gate ordering).
* **M-3** — C6 silently reads `operands[0]`; a two-operand construction resolves `VALID: yes`.
* The `exhibit.py` crash on `main` (stale `materialize()` signature), previously recorded.
* DG-6 remains OPEN and is the legacy form of this same question.
* Held throughout and untouched: `Γ_F(B→A)`, coverage `γ`, participation/support, evidence,
  commutation, Case G, relationship expansion, P1-36 repair, and the primitive-family rule — which
  was **not** reopened to make the constructed case symmetrical.

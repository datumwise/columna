# C3 · `domain_and_movement` — read-only reconnaissance

**2026-09-22. No implementation. No serialization. No native movement licence. No anchor allow-list.
No P1-33 repair. No realization work. No cleanup.** Nothing in any repository was modified; this
document is the whole deliverable.

**Method.** The governing corpus first, the code as evidence second. Sources read in full, with
every claim below traceable to one of them:

* `attachments/d777b3f6_the_theory_of_data_v7_1_zenodo_22649945.md` — **ToD v7.1** (governing)
* `attachments/6e378edd_…_measure_algebra_…_v2_0_draft4.md` and `…_v2_0_draft_rev1.md` — **MA v2.0**
* `attachments/ca786c70_…_measure_algebra_…_v1_0_zenodo_22219691.md` — **MA v1.0**, for the
  inherited Contract Calculus
* `attachments/464ec7b8_frameql_language_specification_v1_0_adopted_2026-09-10_r1.md`,
  `docs/frame_ql_language.md`, `attachments/005b004b_frameql_request_adjudication_ruling_v0_2.md`,
  `attachments/011fbc21_frameql_canonical_disposition_ruling_v0_1.md`
* `specs/unit_d_d1_crosswalk_v0_1.md`, `specs/doctrine_gaps.md`, `specs/open_forks.md`,
  `docs/architecture/ruling_2026_09_14_anchor_identity.md`, `docs/architecture/consolidated_ledger_v0_1.md`
* the shipped tree: `governed/resolve.py`, `governed/foundation.py`, `columna_platform/movement.py`,
  `continuation.py`, `serving.py`, `model.py`, `parser.py`, `projection.py`, `engine.py`,
  `disclosure.py`, and `tests/fixtures/afternoon.cml`

**The legacy `MovementLicence` was treated only as evidence about requirements and failure cases.**
The native fact is derived first (§§1–7); the licence is reconciled against it last (§10).

---

## 0 · The headline

**C3 is two facts, the corpus names both, and only one of them is missing.**

ToD v7.1 §4.1 — the only definitional passage — introduces **two symbols in one table row**:

> "Write \(\mathcal A_F\) for the family law's admitted anchors. **This is notation for its defined
> analytical domain, not a proposed registry or new object.** An edge contract \(\Gamma_F(B\to A)\)
> states the applicable conditions for a proposed movement **between admitted locations**."

`𝒜_F` is a *domain*, and the theory says in terms that it is **not a registry**. `Γ_F(B→A)` is a
*condition on a movement*, and it is defined only **between locations already admitted** — so the
domain is prior and the edge contract is the thing that governs travel within it.

**What is missing is `Γ_F`'s content, and an allow-list of anchors would record its consequences.**

---

## 1 · What does `domain` mean in C3, and is it one responsibility?

### The theory gives two symbols at two different governance locations

ToD §4's C3 row: *"The anchors at which the family is defined **and** the conditions licensing
particular movements."* Two conjoined clauses, two symbols in §4.1.

They are not filed together. ToD §1.5's four governance locations are **Family identity** and **Edge
validity** (plus certificates and metadata), and:

* §4.1's *title* is **"Admitted anchors are part of the law"** — the domain sits on the law/identity side;
* §10.1 lists the facts the four locations determine as *"family identity, **movement validity**,
  certificates/materializations, or metadata"* — **movement validity is at Edge validity.**

The theory never reconciles this. §2.2's `Σ(F)` content list and §3.9's succession triggers (*"target,
formation, participation, or declared continuation law"*) **omit domain and movement entirely**.

### The code has already split them three times, independently, working around a disjunction

`governed/resolve.py:378-395` writes one standing from a **disjunction**:

```python
elif fam.domain is not None or fam.movement is not None:
    e[C3_DOMAIN_MOVEMENT] = Standing(C3_DOMAIN_MOVEMENT, ESTABLISHED, DECLARED,
                                     value={"domain": fam.domain, "movement": fam.movement})
```

So a family declaring a **domain and no movement** resolves **ESTABLISHED**. Every consumer that
matters therefore ignores the standing and reads the content:

| site | what it had to do |
|---|---|
| `serving.movement_licence` (`serving.py:388-425`) | docstring header is literally *"WHY THIS IS NOT `C3.standing == ESTABLISHED`"*; reads `c3.value["movement"]` |
| `serving._no_licence_detail` (`:427-442`) | three-way branch to say which kind of absence it was |
| `native_law.assert_answerable` (`native_law.py:166-179`) | same reading, derived again for the native path |

`serving.py:419-421` names the open question in its own words: *"Whether `resolve` should split domain
from movement is a governed question and is left open."*

### ⟨measured⟩ `domain` is write-only in the entire executing system

Every read of the family-body `domain` slot, exhaustively: parsed by an identity reader
(`publication.py:276`, `_slot(..., lambda r: r)` — no shape imposed); presence-tested in the
disjunction (`resolve.py:381, :386`); packed into a dict (`:384, :389`); stringified into one refusal
message (`serving.py:433`); printed by the demo (`exhibit.py:108`). **Nothing branches on its content,
compares it, validates it or serves it.** Its only behavioural effect is to raise C3's standing
falsely — which is exactly the trap three modules exist to close, pinned by
`test_proof_a_negative_controls.py:148-171` (*"# the trap"*) and `test_native_c4_answerability.py:180-188`.

### Columna's own crosswalk already split them

`specs/unit_d_d1_crosswalk_v0_1.md` maps the legacy carriers to **two halves of C3**:

| legacy | crosswalk verdict |
|---|---|
| `FAMILY { <agg> BLOCKED { <lineage> } }` (`BAnchor`) | *"**C3** — `Γ_F(B→A)`, the conditions licensing a movement. **Already `Law(F)`-shaped, and the only part of `FAMILY` that is. Keep the concept; it is the half worth keeping**"* |
| the v1 `boundary` declaration | *"**C3** — **the negative half of domain-and-movement**. Right concept; wrong scope (measure, not family) and wrong index"* |
| `DerivedColumn` + `License`/`FERTILE` | *"**C3 positive half** + **C2** lineage"* |

> **Finding 1 — brought back as a finding, not a change (Q9).** C3 currently combines two separable
> facts that the theory places at two different governance locations, that the code already reads
> apart in three places, and that Columna's own crosswalk maps to different legacy carriers. One of
> the two (`domain`) is inert everywhere and harmful once (the standing trap). **The model should
> split; nothing is split here.**

---

## 2 · What does the constitutive anchor already establish?

### What follows

`F` fixes `U` (Ruling 1, 2026-09-14), and the constitutive anchor stays **inside identity**, never
becoming a second current location. ToD §2.2:

> "Constitutive anchors, operands, order definitions, participation conventions, and other
> meaning-bearing parameters remain inside \(F\). **They do not become additional current anchors of
> \(F@A\).**"

### What does NOT follow, for any other `A`

* §4.1: *"A geometrically available projection and a computable state operation do not by themselves
  put \(A\) in \(\mathcal A_F\). **The family's definition must license the quantity being claimed
  there.**"*
* §3.6: *"**Geometric shape and family admission are separate judgments.** … An execution plan may
  implement these operations, but it cannot create their analytical permissions by performing them."*
* §6.3: *"Family coherence does not erase partition geometry. … The family guarantees agreement along
  admitted paths; **it does not manufacture a path between incomparable locations**."*
* §10.8: a family *"materializable for a target"* participates in another target's basis — *"**That
  does not confer its own cross-anchor continuation.**"*
* Appendix C.4: *"Earlier Version 7.1 working drafts proposed **universal projection-fiber locality of
  formation as a family-admission test. That claim … is withdrawn.**"* — a geometric derivation of
  admission was considered by the theory and **retracted**.

> **Finding 2 — a silence that matters (Q2).** **ToD never states that `A₀ ∈ 𝒜_F`.** There is no
> sentence of the form "the constitutive anchor is admitted". C4 assumed it — *"constitutive is what
> it means for the family to be established there"* — and the assumption is natural, but it is ours.
> **It needs a ruling** (§12, Q-1), because everything in the native path that answers at all today
> rests on it.

---

## 3 · Is off-constitutive standing derivable anywhere?

**No. Four independent corpora were checked and each refuses at the same point.**

**ToD.** Two passages *use* reach operationally — §10.8 (*"self-sufficient under its **admitted**
continuation law, **so** retained measures at appropriate finer anchors can participate in
constructing that family at a coarser anchor"*) and §5.2 (*"compose **across admitted refinement**"*)
— but both are stated **over already-admitted** locations. §6.1's coherence theorem takes admission as
a **premise**: *"Assume **the relevant movements are admitted**, their projections compose…"*. And
§6.1's closing guard is explicit: *"The same-contributions premise is an evidence obligation … **not a
consequence of admitted movements**."* Appendix B.5: *"**Admitted movements alone establish neither**
the same-contributions evidence premise **nor** the availability of exact intermediate inputs."*

**The Measure Algebra.** Every location-changing rule carries an **undischarged premise**:

* `merge_{L,q}` (§8.2) requires *"\(q\) **admitted by** \(L\)"*;
* `RED1` (App. A.2) requires *"\(Spent(q)\cap\beta(\kappa)=\varnothing\)"* and closes with *"Type
  compatibility is necessary but not sufficient. **Anchor movement and coverage permission are
  independent premises.**"*;
* `DEFAULT` (§9) takes `q : A₀ → A` as given and only selects **which law** applies to a movement of
  class `μ_Γ(q)`.

**⟨measured⟩ the word "admitted" occurs throughout MA v2.0 and is defined nowhere in it.** Every
closed contract (§§12–16) ends *"finalize at an **admitted** anchor"*. That is the hole.

MA also forecloses each cheap substitute by name: *"**Materialization creates availability, not
permission**"* (§6, §31); *"**Numerical executability cannot create analytical identity after the
fact**"* (§3.5, Theorem G0.7); *"**Equal current values do not establish equal analytical information
or identity**"* (§3.4); *"If the profile is undefined or not single-valued for the required movement,
the bare source does not acquire a default measure meaning"* (§9). The one closure-shaped rule in the
corpus — rev1 §9.1's *"generated family space"* — generates **family expressions, not locations**, is
hedged *"where lawful"*, and **was deleted in draft4** (the word "generat\*" does not occur there).

**Frame-QL.** `011fbc21` §9, a ruling: *"**Absence of a prohibition is not universally equivalent to
positive authority.** … **Silence is not authority.**"* `011fbc21` §4: *"**Realization capability
cannot manufacture analytical permission.**"*

**One genuine derivation exists, and it is a necessary condition, not a licence.** ToD §8.1:

> "Every target covered by that basis claim **must admit** the corresponding \(W@A\); a more
> restricted witness-family domain would yield a correspondingly restricted basis claim. (**This is
> law-level domain admission**, not a requirement that \(W@A\) be evidentially available whenever
> \(L@A\) is established.)"

Domains **propagate along the basis relation**: a family cannot be admitted at `A` if the families its
basis is built from are not. That bounds `𝒜_F` from above. It never populates it.

> **Finding 3 (Q3).** No part of `Law(F)`, C7, the measure algebra or the geometry entails a single
> lawful off-constitutive location. The corpus contains exactly one domain-derivation rule (§8.1) and
> it is a **restriction**, not a grant. **"Absence is never permission" holds, and it is the corpus's
> own sentence, not our gloss.**
>
> **Provenance correction, recorded because we have been quoting ourselves.** The sentence *"Absence
> of a prohibition is not permission"* in `resolve.py:394` is **Columna's**, not ToD's — it does not
> occur in v7.1 or v7.0. What ToD actually says is the positive requirement (*"The family's definition
> must license the quantity being claimed there"*); the negative form is a ruling of Frame-QL's
> canonical-disposition document. The reading is right; the attribution was wrong.

---

## 4 · What positive fact is actually missing?

The smallest statement that distinguishes the four states, with what each currently produces:

| state | today | what the state actually needs to say |
|---|---|---|
| no positive movement law established | C3 `UNESTABLISHED` — **correct, and already expressible** | nothing; absence is the state |
| the family positively declares it does not move | C3 `EXPLICIT_NONE` — **correct, and already expressible** | a positive negative |
| some off-constitutive standing is lawful | **inexpressible** | *this* is the missing fact |
| a requested `A` is outside that law | **inexpressible, and there is nowhere to put the answer** | which part of the ask exceeded the law |

The first two already work and are pinned by tests. **The missing fact is the third, and the fourth is
its refusal.**

And the fourth is missing on the wire as well as in the law. ⟨measured⟩ **no reason code anywhere in
the tree has the requested OUTPUT anchor's admission as its subject.** Every shipped code approaches
the question from somewhere else: `input_anchor_unavailable` (pin-relative), `blocked_reduction`
(lineage-relative), `uncertified_edge` / `contradicted_edge` (edge-relative), `out_of_universe`
(universe addressability). `want_of_law` is the nearest — registered against *"a movement to a coarser
anchor where governed movement is UNESTABLISHED"* — and it names the **absence of a law**, never a
**boundary of one**.

---

## 5 · Is the missing thing a set, a transformation law, a closure rule, or something else?

The four candidates, compared rather than chosen between:

| candidate | corpus support | against |
|---|---|---|
| **a set of admitted anchors** (allow-list) | the symbol `𝒜_F` and the phrase *"the anchors at which the family is defined"* | ToD §4.1 rules it out in terms: *"**not a proposed registry or new object**"*. It records consequences — one fact over `k` constituents determines up to `2^k` entries. It must be re-enumerated whenever `U`'s individuation changes. And it yields the worst refusal available: *"not in the list"* |
| **a closure rule** | none | **the word "closure" does not occur in ToD v7.1 at all.** No statement closes `𝒜_F` under `⪰`, under composition, or under anything. §6.1 makes composition a *premise*, not a conclusion |
| **a predicate over anchors** | none | *"predicate"* occurs once in ToD, about the general-expression layer |
| **a per-constituent spendability fact, from which admissibility is COMPUTED** | see below — four independent witnesses | it is not ToD's notation, and it constrains `𝒜_F` to a shape ToD never asserts (§12, Q-2) |

### The fourth candidate, and why it is the recommendation

**Witness 1 — the inherited Contract Calculus, proved.** `RED1` (MA v1.0 §, MA v2.0 App. A.2) is the
**only computed admissibility test in the entire corpus**:

\[ Spent(q)\cap\beta(\kappa)=\varnothing \]

`Spent(q)` is the set of analytical distinctions the movement `q` spends. `β(κ)` is a declared set of
distinctions the contract does **not** permit that capability to spend. MA v1.0 glosses it:

> "The Contract Calculus expresses the same constraint through inherited-contract side conditions: **a
> capability may spend only those analytical distinctions the contract permits.** Theorem \(G_0.7\)
> gives the canonical witness. **Summing Inventory across a blocked time axis** can be typed,
> executable, and deterministic while still failing to inherit Inventory identity."

**`Spent(q)` is exactly what C1 already computes.** `Anchor.projection_forgets` returns the constituents
a projection forgets — the native, universe-scoped instance of `Spent`.

**Witness 2 — it already ships, in the legacy declaration surface.** `parser.py:28`:

```
[FAMILY { <agg> [BLOCKED { <lineage>, ... }] ... }]
```

`model.py:150-151`: `blocked_lineages: frozenset  # lineages this agg may NOT be reduced along`.
`projection.py:49`: *"the B-anchor, as SHAPE (**which axes the reducer does not reconcile along**)"*.

**Witness 3 — a live fixture states the law and the reason.** `tests/fixtures/afternoon.cml`:

```
MEASURE on_hand ON stock_snapshot FROM inventory VALUE level
    FAMILY {
        sum  BLOCKED { calendar }   -- "adding snapshots across days counts the same unit once per day"
    }
```

with the authored note: *"summing `on_hand` across CALENDAR is structurally prohibited — in every
spelling; summing `on_hand` across STORES is lawful, **because the bar names `calendar`, not the
measure**; averaging, min-ing, max-ing and counting `on_hand` over time remain lawful … **That is a
DECLARATION, not an oversight the engine repairs**."* The per-axis scope is a **ruling**
(2026-08-20 §6): *"do not infer a global stock personality; **applicability stays per operator ×
lineage**."*

**Witness 4 — Columna's own crosswalk and platform profile.** The crosswalk: `BAnchor` is *"already
`Law(F)`-shaped, and the only part of `FAMILY` that is"*. The platform profile draft §7.2: *"`BLOCKED
{...}` corresponds to a **capability-indexed negative law resembling `β`**"*, and §7.1 lists the
admission premises as *"the requested anchor movement is lawful; **no blocked axis is spent**; the
requested coverage mode is admitted."*

> **Finding 4 — the recommendation (Q5).** **`Γ_F`'s content is a per-constituent fact about the
> family: for each constituent of `U`, whether this family's quantity survives being composed away
> along it.** Admissibility of a requested movement is then **computed**:
>
> ```
> admits(F, A₀ → A)  ⟺  C3 is established for F   ∧   spent(A₀→A) ∩ not_spendable(F) = ∅
> ```
>
> where `spent(A₀→A)` is `A₀.projection_forgets(A)` — already built, already tested, already derived
> from the constitution. **`𝒜_F` is then exactly what ToD says it is: notation for a domain, derived,
> never stored** — and a refusal can name the offending constituent (*"`berthings` may not be composed
> away along `day`"*) instead of reporting a failed lookup.

### Two things the native model does to this shape, both simplifications

1. **"Per operator" disappears.** The legacy index is *operator × lineage* because a legacy `MEASURE`
   carries a `FAMILY { sum, last, … }` of members. Natively those are **separate families** (recon §6:
   a legacy `member` is classified — *"some denote families, some denote a family's own continuation
   under another name"*), and each cites exactly one continuation law. **Per operator × lineage
   becomes per family × constituent.**
2. **"Lineage" becomes "constituent".** A legacy `calendar` is a declared hierarchy over levels.
   Natively there are no hierarchies and no levels; the axis is a **constituent of `U`'s closed
   individuation** — `day`. The fact gets *smaller and better-founded*, not translated.

### The one thing the legacy shape gets wrong, and it is already rowed

`model.py:155-161`: *"On MEASURE columns `license` is None (measures are **open-by-default; the
B-anchor closes**)."* That is the opposite of ToD §4.1. It is **DG-4**, open since 2026-08-20:

> *"Closed-by-default: absence of positive analytical permission cannot become execution permission.
> **Measure families are OPEN by default (`BLOCKED` closes)** … A stock declared `FAMILY { last }` —
> no `sum` member at all — still serves `sum(x@day)` across time, because there is no bar to cross.
> … **OPEN** — recorded, not fixed. Closing it means either a per-measure closed-family opt-in or a
> ruling that silence is permission; both are **declaration-surface questions**, not planner
> questions."*

> **Finding 5 — DG-4 and the native C3 gap are the same question, approached from two ends.** DG-4 is
> *the legacy declaration surface has the right fact with the wrong polarity*; C3 is *the governed
> declaration surface has no fact at all*. **The polarity is already settled for the native side**:
> C3 `UNESTABLISHED` means nothing moves, so the **positive act is establishing the law at all**, and
> the per-constituent content lives *inside* an established law. Absence stays absence. Whether the
> content inside is then stated positively (spendable) or negatively (blocked) is a representation
> question and is **not** settled here (§12, Q-3).

---

## 6 · The relationship between C7 and C3

**C7 constrains C3's content. It never supplies its authority.** Three findings, in increasing
sharpness:

**(a) Domains propagate along the basis relation — a necessary condition.** ToD §8.1's *"law-level
domain admission"* (quoted §3): a family cannot be admitted at `A` if the families in the basis it is
constructed from are not admitted at `A`. This bounds `𝒜_F` from above and populates nothing.

**(b) What moves is the BASIS, not the displayed value — and MEAN proves the two come apart.**
⟨measured⟩ in the shipped vocabulary (`governed/foundation.py`), MEAN carries
`entails_continuation=NO_CONTINUATION` (*"does not compose; a mean of means is not a mean"*) **and** a
`state_basis` of matching `(SUM, COUNT)`. So C7 is **ESTABLISHED** for a family whose displayed value
**cannot** compose. `resolve.py:310-343` records the correction that established this:

> *"the displayed value does not continue"* ≠ *"no sufficient state exists from which the family can be
> continued or re-established"* … *"**THE STANDING OF A RESPONSIBILITY IS NOT THE ESTABLISHMENT OF
> EVERY FACT THAT MAY APPEAR INSIDE IT.**"*

It follows that C3 is not a fact about the family's *value* composing. **It is a fact about whether the
family's sufficient state may be carried across a given distinction and re-finalized** — which is
precisely what `merge_{L,q}` does and precisely what its `q admitted by L` premise gates.

**(c) The two gates already compose, in the shipped legacy engine, in this order.**
`model.py:153-157`, verbatim:

> *"Names an operator (**reaggregability comes from the operator REGISTRY — operator-level**) plus this
> column's **B-anchor (which lineages reduction is PERMITTED along — column-level)**. **The two gates
> compose: reduce iff monoid (possible) AND B-anchor-clear (permitted).**"*

`planner.py:2136-2142` runs the algebra gate first and only then consults the B-anchor. **That is
C4's C7→C3 order, already implemented, reached independently.**

> **Finding 6 (Q6).** C7 → C3 is confirmed as an **adjudication order** and additionally as a
> **content constraint in one direction**: C7 bounds where C3 could reach (§8.1) and tells C3 what the
> subject of the movement is (the basis, not the value). **Sufficiency is not collapsed into
> authority** — MA states the prohibition four separate ways, and the corpus's own witness is Theorem
> G0.7, where a computation is *"typed, deterministic, and executable while failing to inherit
> analytical identity."*
>
> **One legacy exemption that native law does not grant, recorded.** `planner.py:2135-2138` skips the
> B-anchor entirely for a **holistic** reducer, on the reasoning that it *"recomputes from base at the
> target grain and never combines partial results across the axis, so the B-anchor is moot for it."*
> ToD §3.7 says the opposite about the analytical object so produced: *"A MAX formed from Order
> Revenue and a MAX formed after Revenue is established at Day are **different constructions** unless
> a governing equivalence proves otherwise."* **Re-forming at the target is not movement; it is
> another family.** Do not carry the exemption across.

---

## 7 · What the Measure Algebra already determines

It determines the **mechanism and the shape of the missing premise**, and supplies no authority.

**Already supplied — do not reinvent:**

* the composition itself: `merge_{L,q} : StateExpr[E@A_i]ⁿ → StateExpr[E@B]` (§8.2), with Theorem
  G0.2/G0.3 proving staged-vs-direct equality in the commutative-monoid fragment;
* the **law-selection** half of a movement: `D_Γ : (SourceExpr, MovementClass) ⇀ Law` with `μ_Γ(q)`
  the *"governed movement class"* (§9, §22) — the corpus already has the notion of a movement **class**
  and a mapping from it to a law;
* the anchor-elimination discipline: §10.1's six premises, and its closing sentence — *"anchor
  elimination is **a theorem with premises**, not a global property of SUM, MEAN, LAST, or any
  operator name"* — which is the shape any C3 rule must have;
* the negative test: `Spent(q) ∩ β(κ) = ∅`.

**Deliberately not supplied:** the definition of `admitted`. The premises of `Γ;MA ⊢ E@A :
MeasureExpr` are **never written down** — §28 is headed *"Status: proposed formalization, not yet a
proved complete calculus"* and §30.5 lists completeness as open.

> **Finding 7 (Q7).** A movement calculus must **not** be invented: its *mechanism* is proved, its
> *law-selection* exists, and its *shape* is fixed (a theorem with premises, producing the `admitted`
> token that `merge`, `RED1` and `DEFAULT` all consume). **What is missing is one premise, and the
> corpus tells us its type: a fact about which analytical distinctions this family's law permits to
> be spent.**

---

## 8 · What Frame-QL requires

**Nothing changes in Frame-QL, and it already has the right shape.**

`AT {…}` is a **destination, never a claim of definedness**. Manual §1.5: *"You state *where the value
is wanted* … **The ascription itself never names the mechanism, only the destination.**"* Frame-QL 1.0
§4.2: *"**This is not an inferred analytical choice. The output anchor is explicit and mandatory.**"*

The requested location and the constitutive one are already separated. Frame-QL 1.0 §4.3: *"A measure
has one current anchor … `order` remains inside the family expression because it is a constitutive
input anchor … **The outer frame anchor does not automatically supply a missing inner anchor.**"*
§2.3: *"**An output anchor does not by itself resolve a missing constitutive input anchor.**"*

Frame-QL **defers** the domain question rather than owning it. §6.5: *"**T §4 is the governing
family-law contract.** This language candidate references that contract rather than maintaining a
competing shortened admission rule … admitted anchors and movements …"* §1.2 lists *"the measure
identity `F@A`"* among what ToD owns: *"Frame-QL consumes those objects and laws. **It does not
redefine them.**"*

And `AT {…}` does **not** require a declared anchor — Ruling 2 (2026-09-14): *"**A lawful projected
`{store}` is an anchor, whether or not a separate publication declaration gives it a name.**"* — which
is exactly what C3 (the unit) built.

**Two live defects found, neither repaired:**

* **The Manual states anchor compatibility geometrically.** §2.2: *"a bare measure … is a series only
  if its grain matches the output anchor `AT {A}`, **or reaches it by a verified edge**"*; §5.2: *"the
  input anchor must be finer than or equal to the output anchor in the relevant dimensions."* That is
  the premise ToD §4.1 forbids as sufficient. **The Manual's rule is the pre-§4.1 rule.**
* **`{}` is assumed universally available.** No source asks whether `F` is admitted at the scalar
  anchor; Frame-QL 1.0 makes it universe-relative and the Manual Manifold-relative, unreconciled.

**Adjudication order.** `005b004b` §20 fixes three jurisdictions — *"**Validity precedes adjudication.
Adjudication precedes realization.**"* — and both rulings explicitly **decline** to order the
sub-questions inside analytical adjudication (`005b004b` §19 and `011fbc21` §9 list positive capability
admission as a non-goal). **So C4's C7→C3 order is ours.** It is well-founded (§6(c)) and it is not
the corpus's; recorded as such.

---

## 9 · Are the nine responsibilities right?

See **Finding 1**. Additionally, on identity-bearing standing: ToD §2.2's `Σ(F)` and §3.9's succession
triggers both **omit** domain and movement; §4.1's title says the domain is *"part of the law"*;
§10.1 puts movement validity at Edge validity. Columna ruled it 2026-09-11 (*"a family can exist while
a particular continuation/movement has not been established"*) and both majors implement that —
`resolve.py:66-70` excludes C3 from `IDENTITY_BEARING`, `native.py:104-107` excludes `domain`/`movement`
from the `fcf` payload as *"capability, not identity"*. **The existing reading is consistent with the
theory's silence and is not disturbed by anything found here** — but it is a reading (§12, Q-4).

---

## 10 · Reconciling the legacy licence, after the fact

Field by field, classified only now that the native fact has been derived:

| piece | classification | why |
|---|---|---|
| `source_anchor` | **obsolete legacy representation** | a declaration NAME; natively `A₀` is resolved from `U` and the family's token. Its three reads are all selection/scoping, which the native path does structurally |
| `source_components` | **derived geometry** | read from an anchor DECLARATION (`declared_coordinate_names`). ⟨measured⟩ it is read **only** by `describe()` — it decides nothing at execution time. Natively it is `A₀.constituents`, computed |
| `target_anchor` | **obsolete legacy representation** — and it is P1-33 | the one field doing **both** structure and authority; the caller's free string, validated against nothing, independently deciding `AnalyticalIdentity.anchor`, movement/no-movement, the retained-state key and the public frame location. Natively `A` is an `Anchor`; C3 (the unit) removed the need for the label |
| `target_components` | **derived geometry** | the real subset test and the fold's group-by keys. Natively `A.constituents`, and the subset test is `A₀.refines(A)` |
| `law` | **native governed fact — but it is C8, already carried** | checked against `established_continuation_law(law_view)`. The family already declares its continuation; the licence re-states it. Natively this is a consistency check, not a carried fact |
| `standing` (`POSITIVE`) | **native governed fact** — the polarity, and the only part of the licence that is | *"Stated as a token rather than a bool so that 'licensed' is never the absence of a negative."* This is §4.1's requirement, correctly implemented |
| `authority` | **realization/runtime information** — and ⟨measured⟩ **dead**: read by nothing, not in `describe()`, not in any refusal, not on the wire |
| the object as a whole | **not a candidate native representation** | its own module: *"a RUNTIME PROJECTION — **not a governed serialization** … the governed v2 artifact carries `movement` as an opaque slot with no shape, and Proof B does NOT give it one"* |

**C4's finding is preserved and sharpened.** The licence combines structural projection and authority,
and `movement.py:26-37` says so: *"the subset check answers 'could this coarsening be realized at all?'
and the licence answers 'may this family be moved?' — **and the first never answers the second**."*
Under the native model the first half is **computed** (C1's geometry, `projection_forgets`) and the
second half is **the missing fact**. The licence's contribution to the second half is one token,
`POSITIVE` — it carries the polarity and nothing else, because `target_anchor` is a label and `law`
duplicates C8.

⟨measured, confirming C4⟩ **no production path constructs one.** The only constructor is
`movement.project`, whose callers are tests, `conftest`, and `exhibit.py` (outside the packaged source).
The one production door, `PlatformExecutionProvider(movement=…)`, is never passed an argument —
`store.py:342-343` calls `from_artifact(...)` without it.

---

## 11 · The minimum native answerability rule, once C3 exists

Conceptual; **not implemented, and no signature is proposed.**

```
resolved F @ A                              (C3 · the unit — A is an Anchor of U, A₀ is F's)

1. GEOMETRY      does A exist, and is it reachable by forgetting?
                 A₀ ⪰ A, computed from U's closed individuation
                 else → not a location this family could stand at.  NOT a licence question.

2. C7            is a sufficient-state basis established?
                 else → unanswerable at A₀ and at every other A.  A defect of F's own law.

3. C3            is a movement law established for F at all?          ← absence is never permission
                 and  spent(A₀→A) ∩ not_spendable(F) = ∅              ← the missing fact
                 else → want_of_law, NAMING the constituent that exceeded the law.

4. REALIZATION   can the lawful answer actually be produced here?     (not this unit's subject)
```

Step 1 is already built and shipping. Step 2 is already built and shipping. **Step 3 is one predicate
over one fact, and everything it needs except that fact already exists.** Step 4 is untouched.

Two notes on the sequence, since the instruction was not to force the facts into it:

* **The corpus does not order steps 2 and 3** (§8). The order is ours and is defended on diagnosis
  grounds (C4 §2) and by the legacy engine's independent agreement (§6(c)).
* **Step 1 is not a weaker step 3.** A non-projectable ask fails because there is no such location for
  this family, which is a fact of geometry; calling it a missing licence would name the wrong remedy.
  This is the distinction C4 was asked to preserve, and it survives.

---

## 12 · The smallest law C3 needs, and the questions that need a ruling

### The recommendation, stated as small as the evidence allows

> **C3's missing fact is one statement per family: which of `U`'s constituents this family's law
> permits its sufficient state to be composed away along.**
>
> It is **not** a set of locations — ToD §4.1 rules a registry out in terms, and a list would record
> the consequences of this fact rather than state it.
> It is **not** a closure rule — the corpus has none and the word does not occur.
> It is a **transformation-admissibility fact of the smallest kind**: the `β` of the proved Contract
> Calculus, re-indexed from capabilities-and-lineages onto **families-and-constituents**, which the
> native model makes smaller and better-founded than the legacy form.
>
> `𝒜_F` is then what ToD says it is — **notation for a derived domain, never a stored object**; and
> `Γ_F(B→A)`'s conditions are computed from that fact plus the geometry C1 already supplies.

### Why this is the smallest

Everything else in the rule already exists and is shipping: `spent(A₀→A)` is `projection_forgets`
(C1); the polarity is C3's `UNESTABLISHED`/`EXPLICIT_NONE`/established trichotomy (C4); the
continuation law is C8; the basis is C7; the universe scoping is structural (C3, the unit). **One fact
is added and nothing else is.**

### Questions requiring a ruling

**Q-1 · Is the constitutive anchor admitted?** ToD never states `A₀ ∈ 𝒜_F` (Finding 2). C4 assumed it,
and everything the native path answers today rests on the assumption. *Confirm, or state what
additionally establishes it.*

**Q-2 · Per-constituent, or per-edge?** ToD's notation is `Γ_F(B→A)` — indexed by **edge**. The
recommendation is indexed by **constituent**. They are not equivalent: a per-constituent fact makes
`𝒜_F` closed downward over the unblocked constituents, so *"may drop `store`, but not all the way to
`{}`"* becomes **unstatable**. Is a non-monotone domain a case the theory means to permit? If not, the
per-constituent form is strictly smaller and the monotonicity is a theorem rather than a convention.

**Q-3 · Positive or negative content inside an established law?** The polarity of *absence* is settled
(absence is never permission). Inside an established law, does the family state which constituents are
**spendable** or which are **blocked**? **DG-4 is the same question from the legacy end** and is open;
the two should be ruled together.

**Q-4 · Does C3 split?** Finding 1. Two symbols, two governance locations, three independent
work-arounds in code, one half inert. If it splits, does `𝒜_F` remain a responsibility at all, given
that ToD calls it notation for a derived domain?

**Q-5 · Where does coverage permission (`γ`) belong?** `RED1`'s third premise is `h ∈ γ(κ)`, and the
platform profile records that *"the formal coverage permission represented by `γ` has no complete Core
counterpart."* It is a second missing premise, adjacent to this one and probably **not** C3's — it
looks like participation/support (C5). **Deliberately not claimed for C3 here.**

**Q-6 · The output-anchor refusal has no reason code.** §4. Minting one is a wire-vocabulary act with
its own rules; flagged, not proposed.

### Recorded, not acted on

* **The Manual's geometric anchor-compatibility rule** (§8) predates ToD §4.1 and is inconsistent with
  it. Not repaired.
* **The holistic-reducer exemption** (§6) is a legacy shortcut that ToD §3.7 does not grant. Not
  carried across, not removed.
* **`domain` is write-only** (§1). Not removed.
* **OF-59, F-3, P1-33, P1-34, DG-4, OF-48, OF-58** — all untouched. P1-33's repair remains blocked on
  Q-1/Q-2 above, which is the same conceptual question its ledger row named: *"What governed fact
  makes the projected `{store}` location the `A` in `F @ A`?"* — now answered for `A` by C3 (the unit),
  and still open for *may `F` stand there*.

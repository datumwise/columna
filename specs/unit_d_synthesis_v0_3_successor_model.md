# Unit D — synthesis v0.3: the corrected successor model
## One family kind · the classification test · foundation law re-derived · `firstlight` classified

**Status:** ⚠ **SUPERSEDED — read `specs/unit_d_synthesis_v0_4_model_and_publication_design.md`.**
Kept for its reasoning. v0.4 carries the model forward with seven closures (legacy anchors are not
constitutive anchors; foundation-law positive presence; the `measure` kind retires by name;
migration evidence is not authority; family-law authority is a third standing) and adds the
publication design.

**Supersedes** `unit_d_synthesis_v0_2_successor_model.md` (same day). **Builds on**
`unit_d_d1_crosswalk_v0_1.md`. **Target text:** ToD **v7.1**, DOI `10.5281/zenodo.22649945`.

---

## 0. What v0.3 corrects in v0.2

Eight rulings, 2026-09-11. Two are conceptual corrections and the rest close open items.

| # | correction | what it changes in v0.2 |
|---|---|---|
| 1 | **Do not map every legacy `member` uniformly to a MeasureFamily.** A reducer over an operand may be *the continuation law of the operand family itself*, or *a distinct constructed family*. Classify by target specification + succession | **v0.2 §7.2 is withdrawn.** It mapped all four `firstlight` members to four parallel families. See §3 and §5 |
| 2 | **Do not introduce an extra analytical operand kind.** The shared operand may itself be a governed family at its constitutive anchor. Test whether the primitive/source family can carry the operand responsibility | **v0.2 §1.1 is withdrawn.** The "governed analytical input" object is removed. See §2.1 — the test is run, and it passes |
| 3 | **Do not promote the `Operator` dataclass wholesale.** Separate/re-derive its semantic content from `deliver_sql`, `scan_impl`, `in_core`, and mixed-standing fields such as `witness` | **v0.2 §8's "promote" row is wrong as written.** See §4 |
| 4 | **Empty-fiber behaviour is derived, not re-asked.** The foundation law establishes that MIN/MAX supply no identity and therefore no fold value on an empty fiber. Generally: *human authority chooses analytical meaning; mathematical consequences of an established law are derived* | **v0.2 §3.1 and §7.2 overstated the authoring cost.** `min`/`max` need no human. See §4.3 and §5 |
| 5 | R4 stays closed: absence of prohibition is not permission; admission follows positively from `𝒜_F` and the applicable edge contract; **no Boolean `additive` field is implied** | v0.2 §5 stands unchanged |
| 6 | **Generated families:** *a complete admitted family-forming construction creates/resolves a MeasureFamily under the same ontology as a named family.* Named vs constructed is **not a separate family kind** | **Closes v0.2 §9.7** (D2's fifth separation). See §2.2 |
| 7 | **`family_id`** is required and distinct from canonical name, **foundation-law name**, namespace alias, and realization mapping key. Generation open | v0.2 §2 listed three of the four; foundation-law name is added |
| 8 | **Publication law precedes implementation coverage.** The publication may carry law the current Core profile cannot realize; Core **refuses**, and must not narrow or delete it. Do not wait for K1 — but equally **do not manufacture undeclared hierarchy/edge facts** | **v0.2's "before K1 makes the gap reachable" framing is withdrawn as a motivation.** See §6 |

---

## 1. The objects, corrected

**Seven, and now only ONE family kind.**

| object | status | what it is |
|---|---|---|
| **Universe** `U` | existing, unchanged | population: basis, restriction, anchor, ratified existence law |
| **Anchor** `A` | existing, unchanged | analytical location and its components |
| **MeasureFamily** `F` | **the one new kind** | the analytical identity: `family_id` bound to `Σ(F)`, plus the §4 contract. **Covers primitive/source families and constructed families alike, and named and query-constructed alike** (rulings 2, 6) |
| **Foundation law** | **new as a governed vocabulary object**, *re-derived* — not the `Operator` dataclass | SUM, COUNT, MIN, MAX…: target form, continuation law, required sufficient state, value-domain rule, and the theorems that follow. Shared, versioned, **semantic content only** (ruling 3) |
| **Domain + movement** `𝒜_F`, `Γ_F(B→A)` | existing concepts, re-based on `F` | where the family is defined; what licenses a movement; explicit prohibition |
| **Lineage edge** `F → G` | existing concept, re-based on `F` | constitutive ancestry (§3.7) |
| **Namespace / catalog / default completion** | what `measure` + `root_member` become | names, grouping, and a single-valued default resolution. **Carries no identity.** May be vacuous — see §2.1 |
| *(non-object)* **Measure** `F@A` | never declared | the family at a current anchor. Produced by a request |
| *(private)* **Realization binding** | not governed | §6 of v0.2, unchanged and carried forward |

### 1.1 Formation is a property, not a kind

A family's **formation** (C4) is either:

- **primitive intake** — the quantity is established from the universe's governed source at its
  constitutive anchor (§3.7's *"governed primitive inputs"* in which lineage is rooted); or
- **a family-forming construction** — the quantity is established from parent families by an
  admitted construction.

Both are MeasureFamilies. Ruling 6 extends the same point to naming: *"A complete admitted
family-forming construction creates/resolves a MeasureFamily under the same ontology as a named
family."* So **primitive/constructed and named/constructed are both formation facts, not kinds.**
There is exactly one family kind, which is what makes the object list shorter than v0.2's.

---

## 2. The two tests ruling 2 and ruling 6 asked for

### 2.1 TEST: can the operand responsibility be carried by the primitive/source family?

**Yes. The extra kind is removed, and `measure` keeps no analytical identity.**

The operand of `sum(x@I)` is *x*, a governed analytical input. Ruling 2 asks whether that can be a
family at its constitutive anchor rather than a new kind. It can, and three things confirm it:

1. **§2.2 already types it.** *"A **measure** is that family at one current anchor: `F@A`."* A
   governed quantity at a point is a measure of some family. There is no third thing between a
   universe and a family for it to be.
2. **§3.7 gives it a role without giving it a kind.** *"Well-founded and rooted in the universe's
   governed primitive inputs"* describes the **root of the lineage relation** — a position in a
   graph, not a separate ontological category.
3. **The responsibilities redistribute cleanly.** What v0.2 parked on an "analytical input" object —
   operand value domain, Φ, constitutive anchor, universe — are all ordinary family contract items
   (C6, C9, C4, C5) once the operand is a family.

So today's `measure` retains **namespace, catalog organization and default resolution, and nothing
else.** For `firstlight` that role is close to vacuous: the namespace `revenue` would resolve to the
primitive family, which is also called `revenue`. **`measure` therefore need not survive as a
declaration at all where it groups nothing** — it survives where a name genuinely organizes several
families and is not itself one.

**What this costs, stated plainly.** v0.2 leaned on the operand object to make §11.5.2's requirement
checkable — *"the same participating contributions in both components."* That requirement does not
weaken; it is now discharged by two families **citing the same parent family identity** in their
constitutive lineage, which is §3.7's own mechanism. Strictly better: lineage already exists, and an
identity comparison over `family_id` is exactly what §2.2 asks for.

### 2.2 Generated families: one ontology (ruling 6, closing D2's fifth separation)

An inline `mean(revenue@day)` is **a MeasureFamily**, formed by an admitted family-forming
construction, identical in ontology to a named one. Consequences worth stating:

- **No second family kind, and no "query-family" escape hatch.** A construction that is not complete
  or not admitted does not mint a *lesser* family; it mints **nothing** (§3.6: *"A general expression
  can also produce a result without minting a family"*).
- **Identity is the same question.** `Σ(F)` for a constructed family is its construction plus
  operands plus constitutive anchors plus law parameters — which is what §2.2 means by *"denoted
  through an admitted canonical construction."*
- **What stays open is mechanics, not ontology:** whether a query-constructed family's `family_id` is
  minted, resolved against an existing one, or held transient, and whether it is ever published.
  Ruling 6 leaves exactly that open, and v0.3 does not close it.

---

## 3. The classification test for legacy `member`s

Ruling 1's instruction is to classify by **target specification** and the **succession test** rather
than by the historical container. Stated as a procedure, with its authorities.

> Let `P` be the operand family, with declared continuation law `⊕_P`. For a legacy member naming
> reducer `r` over `P`:

**Step 1 — Target test (§4/C1).** Is the member's asserted quantity *the same quantity as `P`*, read
at a coarser anchor — or a different quantity? A different value domain, a different semantic role
(a **count of things** rather than an **amount of something**), or a different unit is decisive.
→ *different quantity* ⇒ **constructed family**, stop.

**Step 2 — Continuation test (§5.2).** Is `r` `P`'s own continuation law — does folding `P`'s
supported values by `r` across admitted refinement yield `P` at the coarser anchor? §5.2: *"A family
is self-sufficient when its own supported measure values compose across admitted refinement by an
associative and commutative continuation law."*
→ *yes, and Step 1 said same quantity* ⇒ **not a family at all. It is `P@A`**, and the member's name
is a namespace alias / canonical reference.
→ *no* ⇒ **constructed family**.

**Step 3 — Participation test (§11.5.1, §3.9).** Identification is not automatic even when Steps 1–2
pass. §11.5.1: *"A named family such as Revenue may already denote the same construction;
canonicalization can identify them **only where identity and participation agree**."* §3.9 repeats
it for the default completion. → *participation differs* ⇒ **two families that happen to compute
alike on today's data**.

**Step 4 — Succession test (§3.9), as the check on 1–3.** If the member's target, formation,
participation or declared continuation can change without `P`'s changing, they are distinct families.

**The test is not a mapping — it can fail to decide**, and when it does, that is information: the
publication does not determine the family, and a human must. Ruling 2's warning holds: *not every
historical member is automatically a valid family.*

---

## 4. The foundation law, re-derived rather than promoted (ruling 3)

Core's `Operator` dataclass has the right *content* in several fields and the wrong *standing* in all
of them, because it mixes three jurisdictions in one record. The split:

### 4.1 Semantic — candidate foundation-law content

| current field | what the law actually states | §4 responsibility |
|---|---|---|
| `combine` | the **continuation law** on the value domain (addition; extremum; union) — not the engine's dispatch tag | C8 |
| `accepts` / `out_rule` | the **value-domain rule**: which operand domains the law admits, and the result domain it yields | C6 |
| `linear` | an algebraic property of the law (distributes over addition) | C8 / fertility |
| `needs_order` | the law **requires a constitutive order parameter** (FIRST/LAST) — §7, and identity-bearing per §2.2 | C1/C2 |

### 4.2 Realization — must not enter the foundation law

`deliver_sql` · `scan_impl` · `in_core` · sketch precision. Plus `kind` (REDUCER/SCAN/MAP), which is
**planner routing**, and §3.6 is explicit that it confers nothing: *"Geometric shape and family
admission are separate judgments… Neither operation receives or loses family authority solely from an
implementation classification."*

### 4.3 Mixed standing — `witness` splits three ways, and `is_monoid`/`re_entrant` are theorems

**`witness` (VALUE | SKETCH | ORDERED_W | HOLISTIC)** conflates:

1. **what sufficient state the law requires** — a value; a value plus an order key; no finite witness.
   *Semantic*, C7.
2. **in what representation it is held.** *Realization* — and §8.5 says so directly: *"The witness
   need not have one physical format."*
3. **whether the retained state is approximate.** SKETCH is an approximation, and §10.9 requires
   *"Approximation remains explicit"* — an analytical **disclosure**, not a representation detail.

One enum currently answers all three. In the foundation law, (1) and (3) belong; (2) does not.

**`is_monoid` and `re_entrant` are not flags to be set — they are theorems about the stated law**,
and ruling 4 governs them: *mathematical consequences of an established law should be derived rather
than re-asked.* Once the law states its continuation on a value domain, self-sufficiency (semigroup),
the existence of an identity (monoid), and re-entry coherence follow or fail to follow. §5.2 already
writes the MIN/MAX case as a consequence: *"MIN and MAX need not acquire an artificial identity or
semantic Null in order to qualify."*

### 4.4 Empty fibers, derived (ruling 4)

Therefore, and withdrawing v0.2 §3.1's claim that `min`/`max` need a human:

- **SUM** — monoid identity exists ⇒ an empty admitted fiber lawfully folds to the identity.
- **MIN / MAX** — commutative semigroup, **no identity** ⇒ an empty eligible fiber receives **no
  value from the semigroup alone** (§6.1.1, §11.5.1). Established once, in the law. Never re-asked.
- **A family declares an empty-result rule only where its target law establishes something beyond
  what follows from the foundation law** — e.g. a target that defines a value on an empty domain by
  convention rather than by algebra.

**The general principle, which v0.3 adopts as the derivation rule's second clause:**

> **Declaration is for choices. Derivation is for consequences.** A human is asked only where
> analytical meaning is genuinely chosen; anything that follows from an already-established law is
> derived. Asking a human to restate a theorem is not governance — it is a second chance to get it
> wrong.

(The first clause, from v0.2 §4, stands: *derivation is only ever from another declaration — never
from a name, never from a mapping, never from execution.*)

---

## 5. `firstlight`, classified rather than mapped

### 5.1 The material facts

Publication: one `measure revenue {value_type: decimal, root_member: revenue_sum}`; four `member`s
with **byte-identical bodies** `{measure: revenue, anchor: sale_at, universe: sales}`. Private
mapping: all four realize `warehouse.main.sales_lines.amount`, differing **only** in
`root_evaluator ∈ {sum, count, min, max}`. Emitted image: one `MEASURE revenue … TYPE Float64 VALUE
amount FAMILY { count max min sum }`. Universe basis `events`; anchor `sale_at = (store, day)`.

### 5.2 Applying the test

| legacy member | Step 1 · target | Step 2 · continuation | verdict |
|---|---|---|---|
| `revenue_sum` | **same quantity** — an amount of revenue, decimal, read at a coarser anchor | **SUM is Revenue's own continuation**, if Revenue is additive | **NOT a distinct family.** It is `Revenue@A` — the primitive family continued. Its name is a namespace alias, and `root_member: revenue_sum` is exactly the default completion recording it. **Subject to Step 3** — §5.3 |
| `revenue_count` | **different quantity** — a count of participations, integer, not an amount | — (stopped at Step 1) | **Constructed family**, parent Revenue. **Target underdetermined** — §5.4 |
| `revenue_min` | **different quantity** — an extremum of operand values (§11.5.1), not a total | MIN is not Revenue's continuation | **Constructed family**, parent Revenue. Empty fiber **derived** (§4.4) |
| `revenue_max` | as `min` | as `min` | as `min` |

**So `firstlight` is one primitive family and three constructed families — not four parallel
families.** v0.2 §7.2 is withdrawn.

### 5.3 The Step 3 question: does `revenue` ≡ `revenue_sum`?

Steps 1 and 2 pass, so §11.5.1 and §3.9 both apply, and both attach the same condition: *only where
identity **and participation** agree*. `firstlight` declares no participation for either, so the
condition cannot be evaluated from the artifact. **This is an authoring question, and it is the
first one.** If they agree, `firstlight` has one primitive family with two names. If not, it has a
primitive family and a constructed SUM family over it, and `root_member` points at the latter.

### 5.4 The `count` target, unchanged from v0.2 and still the sharpest

§11.5.1: *"`count(I)` counts participating analytical points of anchor `I`, each contributing one.
`count(x@I)` counts participation under the operand construction's governed rule. **These are
distinct targets.**"* The publication does not say which, and no rewrite can make it say. It is the
seam **P1-10** came through, and the number is the denominator of every mean anyone takes over this
measure. **Authoring question, the second.**

### 5.5 A third question the test exposes, and it is new

Identifying "the shared operand" presupposes knowing **the grain the contributions live at**, and
`firstlight` does not declare it. The realized table is `sales_lines` — line grain — while the
declared anchor is `sale_at = (store, day)`. Nothing in the publication asserts that `sale_at` is
unique in `sales_lines`; anchor uniqueness is gate *evidence*, which the publication deliberately
drops. In the synthetic fixture the two coincide (six rows, one per `(store, day)`), **but that is a
data fact, not a law**, and §3.7 rules on exactly this shape:

> *"A MAX formed from Order Revenue and a MAX formed after Revenue is established at Day are
> different constructions unless a governing equivalence proves otherwise."*

So `min(amount)` over *contributions within a point* and `min` over *established `Revenue@sale_at`
values* are different constructions that agree on this data. Two readings, and the publication
chooses neither:

- **(a)** Revenue is primitive at `sale_at`, and its **intake** over multiple contributions per point
  is itself an analytical rule — which today is supplied by `root_evaluator` at the realization
  layer. **That is the same defect a second time, at the intake end rather than the continuation
  end**, and it is new here: D1 found `root_evaluator` deciding *continuation*; this finds the same
  token deciding *intake resolution* wherever the anchor is not unique.
- **(b)** A finer governed anchor — the sale line — is declared, Revenue is primitive there, and all
  four constructions cite it.

**Authoring question, the third — and the only one of the three that is structural rather than
semantic.** Naming it is not manufacturing a fact (ruling 8): the gap is in the publication, and
v0.3 declines to fill it.

### 5.6 What `firstlight` looks like afterwards

```text
universe  sales                  basis events, anchor sale_at          — unchanged, ratified
anchor    sale_at (store, day)                                         — unchanged
family    revenue                PRIMITIVE · decimal · Φ declared
                                 continuation law SUM (declared, not derived)
family    count(revenue@sale_at) CONSTRUCTED · parent revenue · COUNT · target TBD (§5.4)
family    min(revenue@sale_at)   CONSTRUCTED · parent revenue · MIN · empty fiber DERIVED
family    max(revenue@sale_at)   CONSTRUCTED · parent revenue · MAX · empty fiber DERIVED
namespace revenue                → revenue's family_id   (today's root_member)
movement  (nothing declared)     ⇒ UNESTABLISHED — and it stays that way (§6)
mapping   4 bindings keyed by family_id; endpoint sales_lines.amount; root_evaluator GONE
```

**Authoring cost, corrected:** three questions — the `revenue ≡ revenue_sum` identification, the
`count` target, and the contribution grain. **Not** an empty-fiber declaration for `min`/`max`
(derived), and **not** four families to compose. v0.2 said "3 of 4 families need a human"; the
corrected statement is *three questions, one of which dissolves a family rather than creating one.*

---

## 6. Publication law precedes implementation coverage (ruling 8)

Two obligations, opposite in direction, and `firstlight` needs both.

**Law is representable regardless of coverage.** The publication may carry admitted family law the
current Core profile cannot realize; Core **refuses that realization** and must not narrow or delete
the law. §4.1 is the authority: *"a backend's inability to realize an admitted movement does not
remove that movement from analytical law."* `K0_REDUCERS` is the existing correct instance — it
refuses with a named category rather than emitting a narrowed image, and it is the model.

**But nothing undeclared may be manufactured.** `firstlight` declares no movement condition, so its
families' movement law is **unestablished** and the successor model must publish it as unestablished
— not as additive, not as prohibited, and not as an invented hierarchy for K1 to execute later.

**v0.2's "before K1 makes the gap reachable" motivation is withdrawn.** It framed representability as
a race against an implementation milestone. The correct framing is that the two are independent:
governed law is made representable because it is law, and coverage is a separate profile question
that refuses where it falls short. That K1 would otherwise make the gap *reachable* remains a true
statement about risk; it is not the reason.

---

## 7. The smallest publication representation implied

Smaller than v0.2's, because ruling 2 removed a kind and ruling 6 removed a distinction.

| action | kind | note |
|---|---|---|
| **keep unchanged** | `universe`, `anchor`, `attribute`, `relationship`, `hierarchy`, `crosswalk` | untouched |
| **add — the ONE new kind** | **`family`** | identity (`family_id` + canonical name); universe; constitutive anchor(s); **formation** (primitive intake *or* family-forming construction over parents); foundation-law nomination + its governed parameters; participation; declared domain; and only those exceptional cases **not** derivable from the law |
| **retire** | `member` | classified out by §3 — some become families, some become names |
| **demote** | `measure` | namespace / catalog / default resolution. **No identity.** Need not be declared where it groups nothing |
| **re-base** | `boundary` | onto `(family, movement/edge)`. Positive half is the family's declared domain. **No `additive` field** (ruling 5) |
| **cite, do not embed** | **foundation-law vocabulary** | shared, versioned, **semantic content only**, re-derived per §4 — not the `Operator` dataclass, and not its realization or mixed-standing fields |
| **carry** | `family_id` | opaque to consumers, never regenerated by a reader, refuse if absent. Distinct from canonical name, **foundation-law name**, namespace alias, and mapping key (ruling 7). Generation open |
| **version** | publication format **MAJOR** bump | an optional key cannot force a consumer that cannot represent the law to refuse |

**One new kind. One retired. One demoted. One re-based. One cited.** Deliberately absent: no `Σ(F)`
object (§2.2 — *"the signature is not an additional ontological kind"*); no separate law record
beside the family (§4 — *"not necessarily separate records"*); no operand kind (ruling 2); no
generated-family kind (ruling 6); no `admitted_reductions`; no additivity field.

---

## 8. Open, and put up for ruling

1. **Foundation-law nomination vs inheritance** — a family *nominates* a law, or *receives* one
   through an admitted canonical construction (ruling 3's own wording). Whether a family may restate
   what it inherits, and whether restating is recorded as inheritance or as authorship, is open.
2. **`family_id` generation** — deliberately open (ruling 7).
3. **Query-constructed family mechanics** — minted, resolved, or transient; ever published (ruling 6).
4. **Family-law ratification** — `firstlight`'s families would be authored and unratified while its
   universe is ratified. Raised, not proposed.
5. **`firstlight`'s three authoring questions** (§5.3, §5.4, §5.5) — semantic, semantic, structural.
   The third may require declaring an anchor the publication currently lacks.
6. **Whether lineage edges publish now or later** — the three constructed families all cite Revenue,
   so `firstlight` would exercise lineage on day one. Unlike movement, this is *declared* by the
   classification rather than manufactured.
7. **Whether `measure` is declared at all** when it groups nothing (§2.1).

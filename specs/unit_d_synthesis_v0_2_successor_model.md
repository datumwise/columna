# Unit D — synthesis v0.2: the conceptual successor model
## Objects, identities, law allocation, and the smallest publication that carries them

**Status:** desk draft, 2026-09-11, awaiting ruling. **No schema. No code. No field names** — objects,
identities and responsibilities only.

**Supersedes** `unit_d_family_law_carrier_synthesis_v0_1.md` (same day) wherever they differ.
**Builds on** `unit_d_d1_crosswalk_v0_1.md` and the D1 ruling of 2026-09-11.
**Target text:** ToD **v7.1**, DOI `10.5281/zenodo.22649945`. Section numbers are v7.1's.

---

## 0. The eight settled facts this model is built on

Recorded so the model can be checked against them rather than against memory.

1. Current governed `measure` is **not** the ToD Measure. It is a legacy namespace / grouping /
   default-resolution container — *unless D1 finds an additional responsibility requiring
   preservation* — and **must not become a second analytical identity above the families.**
2. Current `member`, where it denotes a distinct analytical target, succeeds to a **MeasureFamily**,
   not to a member of another family. `revenue{sum,count,min,max}` must not be carried forward as one
   family with four reducer members. But **not every historical member is automatically a valid
   family** — the law contract still has to establish the target.
3. `root_member` is **default completion**: namespace → uniquely governed default family. It does not
   create or identify a Measure.
4. `root_evaluator` is **family-law content in the wrong jurisdiction.** Do not relocate it
   unchanged; separate governed family law from physical realization.
5. **Shared foundation laws** (SUM, COUNT, MIN, MAX, …) remain useful vocabulary. The foundation-law
   token is a **constituent** of `Σ(F)`/`Law(F)`, **not sufficient to identify the family** — COUNT's
   several target forms prove it. Leading direction, not yet a schema ruling.
6. **Stable family identity is inside Unit D.** The model must support `family_id ≠ canonical_name`
   and bind governed identity to the semantic signature. Generation (digest/UUID/other) stays open.
   **Names, reducer spellings and private mapping keys cannot continue to serve as identity.**
7. The legacy `FAMILY { … }` grouping is **not carried forward as ontology.** Its genuine law-shaped
   content — lineage restrictions, constitutive order — is preserved.
8. **R4 is settled:** absence of a prohibition is not positive permission. The legacy *"additive
   answer → no declaration"* rule is superseded, and **is not to be replaced by a Boolean additivity
   field** — it is solved through the family-law model.

---

## 1. Which governed objects exist

Nine rows, of which **one kind is genuinely new**, two are existing-and-unchanged, one is a
*non*-object, and one is private.

| object | status | what it is |
|---|---|---|
| **Universe** `U` | existing, unchanged | population: basis, restriction, anchor, existence-law ratification |
| **Anchor** `A` | existing, unchanged | the analytical location and its components |
| **Governed analytical input** | **the one surviving responsibility of today's `measure`** — see §1.1 | a governed typed quantity at a constitutive anchor in a universe (`revenue`, decimal, at `sale_at`, in `sales`). §3.7's *"universe's governed primitive inputs"*, in which lineage is rooted |
| **MeasureFamily** `F` | **NEW — what `member` becomes** | the analytical identity: `family_id` bound to `Σ(F)`, plus the §4 contract |
| **Foundation law** | **NEW as a governed object**; the content already exists as Core's operator registry | SUM, COUNT, MIN, MAX, DISTINCT…: continuation law, sufficient-state witness, value-domain rule, self-sufficiency and re-entry properties. **Shared vocabulary, versioned, cited by families** |
| **Movement condition** `Γ_F(B→A)` + domain `𝒜_F` | existing concepts (`boundary`, `BLOCKED`), **re-based on `F`** | where the family is defined, and what licenses a particular movement |
| **Lineage edge** `F → G` | existing concept (derived/`License`), **re-based on `F`** | constitutive ancestry (§3.7) |
| **Namespace entry / default completion** | what `measure`+`root_member` become **as a name service** | a name resolving to one `family_id` where single-valued. **Carries no identity** |
| **Measure** `F@A` | **NOT a declared object** | the family at a current anchor. Produced by a request; never published |
| *(private)* **Realization binding** | not governed | §6 |

### 1.0 `F@A` is never published — and today's `member` looks like it is

Today's `member` body is `{measure, anchor, universe}` and reads like `F@A`. It is not. `sale_at` is
the **constitutive** anchor, which §2.2 places *inside* `F`:

> *"Constitutive anchors, operands, order definitions, participation conventions, and other
> meaning-bearing parameters remain inside `F`. They do not become additional current anchors of
> `F@A`."*

Publishing `F@A` would mint exactly the second analytical identity ruling 1 forbids, one layer
further down. The successor `family` declaration therefore carries its constitutive anchor as law
content, and **no governed object is ever anchored at a current anchor.**

### 1.1 The `measure` exception clause, invoked — and it is one responsibility, not the container

Ruling 1 left an opening: *"unless D1 finds some additional responsibility that requires
preservation."* D1 finds exactly one, and it is **the governed operand identity**. Four independent
pieces of evidence, three of them from the shipped tree:

1. **§11.5.2 makes it a soundness requirement.** MEAN's exact basis is matching SUM and COUNT *"with
   the same participating contributions in both components."* That is uncheckable unless two families
   can cite **the same operand identity**. Without a governed operand there is nothing for "same" to
   range over.
2. **§3.7 requires a root that is not a reducer-formed family.** Lineage *"is well-founded and rooted
   in the universe's governed primitive inputs."* Something must be the root.
3. **Columna already carries it correctly, and has all along.** `measure.value_type` is the
   **operand's** value domain — not a result type — and each family's result domain is already
   *derived* from it: `planner.py:2713`, `output_dtype(member, meas.logical_type)`. So `count` over a
   decimal operand already serves `Int64`. **C6 is already split exactly right — operand domain
   declared, result domain derived — and it is the one responsibility today's `measure` discharges
   correctly.**
4. **The compiler already treats `measure` as operand-scoped**, not container-scoped: it refuses when
   members realize more than one table or column, because *"a Core measure has exactly one home table
   and one value expression."*

**This sits BELOW the families, not above them.** It is an ancestor they cite in their constitutive
lineage, not a grouping identity that owns them — so it does not violate ruling 1's prohibition. But
because it *is* an identity, it is put up for ruling explicitly in §9.1: either `measure` is
re-scoped to this and sheds everything else, or a new kind takes it and `measure` dissolves to pure
namespace. **What must not happen is that it keeps the container role.**

A fifth confirmation arrives in §3 below: the standing ruling that Φ (`fill_rule`) is **per-measure,
never per-member** — *"Φ answers what kind of quantity this is — revenue is a flow, a level is a
stock — and that never changes with the anchor"* — is a statement about **the operand**, and it
becomes *more* correct, not less, once `measure` is the operand.

---

## 2. What identities each object carries

| object | identity | rule |
|---|---|---|
| Universe | governed name + ratified existence law | unchanged |
| Anchor | governed name + components | unchanged |
| Governed input | governed name + universe + constitutive anchor + operand value domain | an **ancestor** identity; cited, never a family |
| **MeasureFamily** | **`family_id`, immutable, bound to `Σ(F)`** | canonical names and aliases **resolve to** it and never mint it |
| Foundation law | an identity in the **shared** vocabulary, versioned | a *constituent* of `Σ(F)`, never sufficient to identify `F` (ruling 5) |
| Namespace entry | **none** | a name and a resolution. If it acquires an identity, ruling 1 is violated |
| Realization binding | **keyed by `family_id`** | never by name, never by reducer, never by position |

**The identity discipline, in one sentence:** *every governed reference is to a `family_id`; every
human-facing reference is a name that resolves to exactly one, within one namespace version.* That is
the sentence the synonym-operator hole dies to — §2.2: *"Two distinct active identities cannot be
hidden under one ambiguous canonical reference."*

### 2.1 `Σ(F)`'s membership is not a design choice

§2.2 lists the signature's content: governed universe, canonical family form, constitutive parents
and anchors, identity-bearing law parameters and contracts, constitutive lineage. §3.9 gives the
succession test: *"A change to an identity-bearing target, formation, participation, or declared
continuation law"* **is** succession; a change of physical representation, retained basis or execution
route is not.

**Those two lists must agree, and they do.** So `Σ(F)`'s membership is *determined* by the succession
test rather than chosen: anything whose change is a succession is in the signature; anything whose
change is not, is out. This is worth stating because it settles a whole class of future arguments
without a ruling — including the one that matters most here: `root_evaluator`'s content changes the
target, therefore it is in `Σ(F)`, therefore it cannot live in a mapping.

Generation of `family_id` — digest, UUID, or other — stays open per ruling 6. §2.2 agrees in advance:
*"A digest is one possible implementation, not a required mechanism."*

---

## 3. Where each §4 responsibility belongs, and whether it is declared or derived

| § | responsibility | belongs to | declared / derived |
|---|---|---|---|
| **C1** | Target specification | **F** | **declared** — foundation-law reference **+** operand **+** constitutive anchor **+** participation. The token alone is insufficient (ruling 5; §11.5.1) |
| **C2** | Identity and ancestry | **F** | **declared**, canonicalized into `Σ(F)`/`family_id`; lineage edges declared |
| **C3** | Domain and movement | **F** | **declared**, in two parts — family domain `𝒜_F` and per-edge conditions `Γ_F(B→A)`. See §5 |
| **C4** | Formation | **F** | **declared** — constitutive anchor, operand construction, multi-input dependencies |
| **C5** | Eligibility and participation | **F**, grounded on `U` | **declared**; the universe's basis/restriction supplies the ground, the family its own participation |
| **C6** | Semantic values | **split** | operand domain **declared** (on the governed input); result and state domains **derived** from the foundation law's rule; a family may declare a narrowing |
| **C7** | Sufficient-state bases | **foundation law**, then **F** | **derived** by default from the foundation law; **declared** where the family names an alternative basis (MEAN ← SUM, COUNT), and alternatives must be declared to agree (§5.3) |
| **C8** | Continuation and agreement | **foundation law**, then **F** | **derived** from the foundation law; **declared** where the family's continuation differs, or where re-entry/path coherence is claimed beyond the law's own certification |
| **C9** | Exceptional cases and realization | **split** — see §3.1 | **declared** |

### 3.1 C9 is two questions, and today they are one field

The standing ruling puts Φ (`fill_rule`) on the measure, never the member, and its reasoning is
exactly right: *"Φ answers what kind of quantity this is — revenue is a flow, a level is a stock —
and that never changes with the anchor."* That is a property of **the operand**. Under the successor
model Φ lands on the **governed input**, and the ruling survives intact and better-founded.

But there is a second empty-case question the current field cannot express, and it is **per family**:

> what does the family's result denote at an admitted anchor where **no contribution exists**?

SUM has a monoid identity, so an empty fiber can lawfully be `0`. **MIN and MAX do not.** §5.2:
*"MIN and MAX need not acquire an artificial identity or semantic Null in order to qualify."*
§11.5.1: *"an empty eligible fiber receives no MIN/MAX value from the semigroup alone (§6.1.1)."*

So `revenue_min` and `revenue_sum` over the **same operand** must answer the empty case differently,
and today they cannot, because the answer is held once per measure. **This is a concrete instance of
"measure is not the family" that costs a served number**, and it is the second one D1 has turned up
(after P1-10). The successor model separates them: Φ on the operand, empty-fiber denotation on the
family, mostly **derived** from the foundation law and **declarable** where a family overrides.

---

## 4. The derivation rule

One rule governs every "derived" cell above:

> **Derivation is only ever from another declaration.** Never from a name, never from a mapping,
> never from execution.

- **Legitimate, and already shipped:** result domain from foundation law + operand domain
  (`planner.py:2713`); the B-anchor verdict from declared lineage ∩ declared movement conditions —
  Core's one correct derivation, and the mechanism to keep.
- **Illegitimate, and currently happening:** family membership from the mapping's `root_evaluator`;
  law from an operator **name** through a global registry the family never consented to; anything
  from runtime behaviour.
- **MA:832 is satisfied,** not bent: *"the planner applies declared law. It does not infer missing
  law."* Deriving from governed vocabulary is *applying* declared law — the foundation law **is** a
  declaration, which is precisely why it must be promoted from a Core-internal table to shared,
  versioned vocabulary before anything may inherit from it.

**Inheritance must be consented to, not assumed.** Ruling 5 says the foundation-law token is a
constituent, not the whole. So a family that cites SUM takes SUM's continuation, witness and value
rule **by default**, may **declare** them explicitly and be checked against the law, and if it
declares something different it is a different family (§3.9). Silent inheritance from a token is what
we are removing; default-with-consent is not the same act, but the model must be able to tell them
apart, which means the default must be *recorded as inherited* rather than materialized as if
authored.

---

## 5. R4, solved through the model rather than by a field

C3 is **two positive declarations**, and that is the whole answer.

```text
admitted      the anchor is in 𝒜_F   AND   the movement is licensed by Γ_F
prohibited    an explicit exclusion  (with its reason)
unestablished neither — the family's law does not speak to it
```

Permission requires **two positive statements**, so absence can never be read as permission. §4.1 is
the citation, and it is unusually direct:

> *"A geometrically available projection and a computable state operation do not by themselves put
> `A` in `𝒜_F`. The family's definition must license the quantity being claimed there. Conversely, a
> backend's inability to realize an admitted movement does not remove that movement from analytical
> law."*

Both halves matter. The first kills "it computed, therefore it was allowed". The second kills "the
backend can't, therefore the law doesn't say so" — which is why `K0_REDUCERS` must keep refusing
rather than narrowing.

No Boolean additivity field appears anywhere. "Additive across calendar" is *the calendar movement is
licensed*; "non-additive" is *it is not licensed, and here is the explicit prohibition and its
reason*; "nobody has ruled" is *silence*, and silence now has a meaning it can be held to. The legacy
*"additive → declare nothing"* rule is superseded exactly as ruled: under the successor model,
declaring nothing produces **unestablished**, which is the truth.

---

## 6. How physical realization refers to a governed family without defining it

The binding is private, keyed by `family_id`, and says:

> *For family `family_id = …`, on this connection, the operand is realized at `sales.amount`, and I
> discharge its declared law with `sum(…)`, exactly.*

Three properties, in order of importance:

1. **Reference by immutable identity.** Not by name, not by reducer, not by mapping position. A
   binding that cannot name a `family_id` has nothing to bind to and refuses.
2. **Correspondence is asserted by the mapping and CHECKED by the compiler** — *can this delivery
   discharge the declared foundation law over the declared operand at the declared constitutive
   anchor?* Mismatch is a named refusal. This is the same inversion the compiler **already performs
   correctly for anchor components** and performs backwards for members; the fix is to make members
   look like anchors, not to invent a mechanism.
3. **A realization edit cannot be a family succession — structurally.** Because `family_id` is not
   derivable from anything in the mapping, §3.9's test stops being a rule someone must remember and
   becomes a property of the shape. **This is the property P2-02's four-mappings reproduction
   currently disproves**, which is why that reproduction is evidence rather than an artifact.

**The binding legitimately carries:** the endpoint; the delivery expression; an exactness /
executability claim (§4.1 — inability **refuses**, it does not narrow `𝒜_F`); realization evidence —
freshness, data-state version, producer attestation (§9, §10.8).

**It must never carry:** which reducer; which participation; which anchor is constitutive; or
anything else whose change would be a change to `Σ(F)`.

---

## 7. `firstlight` in the successor model

### 7.1 Today

```text
measure revenue        { value_type: decimal, root_member: revenue_sum }
member  revenue_sum    { measure: revenue, anchor: sale_at, universe: sales }
member  revenue_count  { …byte-identical… }
member  revenue_min    { …byte-identical… }
member  revenue_max    { …byte-identical… }
private mapping        member → root_evaluator ∈ {sum, count, min, max}; endpoint sales.amount
```

### 7.2 Successor

| successor object | content | migration |
|---|---|---|
| `universe sales` | basis `events`, anchor `sale_at`, ratified | **unchanged**, ratification intact |
| `anchor sale_at` | `store: text`, `day: date` | **unchanged** |
| **governed input `revenue`** | decimal, at `sale_at`, in `sales`, Φ declared | today's `measure`, minus the container role. `value_type: decimal` was **correct as authored** — it was always the operand's domain |
| **family `sum(revenue@sale_at)`** | SUM; continuation `+`; self-sufficient monoid; re-entrant; result domain derived; empty fiber `0` by the monoid identity | **mechanical** |
| **family `count(…)`** | COUNT — **but of what?** | **NOT mechanical.** See §7.3 |
| **family `min(revenue@sale_at)`** | MIN; commutative semigroup, **no identity**; empty fiber has **no value** | **not mechanical** — needs an empty-fiber declaration the measure-level Φ cannot distinguish from SUM's (§3.1) |
| **family `max(…)`** | MAX; as MIN | as MIN |
| **namespace `revenue`** | resolves the bare name to `sum(revenue@sale_at)`'s `family_id` | this is `root_member` doing precisely its successor job (ruling 3) |
| **movement conditions** | **none declared** | under R4 settled that reads **unestablished** — see §7.4 |
| **private mapping** | four bindings keyed by `family_id`: endpoint `sales.amount`, delivery expression, exactness claim | `root_evaluator` **gone** |

### 7.3 The one migration that needs a human, and it is not a small one

§11.5.1, verbatim:

> *"`count(I)` counts participating analytical points of anchor `I`, each contributing one.
> `count(x@I)` counts participation under the operand construction's governed rule. **These are
> distinct targets.** … In the published example, 100 governed Order points and 97 supported Revenue
> observations give `count(order) = 100` and `count(revenue@order) = 97` … That does not authorize
> replacing an intended 100-order MEAN with a 97-observation MEAN."*

`firstlight`'s publication does not say which `revenue_count` is, and **no rewrite can make it say** —
the information is not in the artifact, in the mapping, or in the name. It must be authored.

This is also exactly the seam **P1-10** came through: `count` delivered `count(*)`, discarding its
operand, so two members of one measure carried different supports and `revenue.sum / revenue.count`
served a mean over mismatched denominators. The repair fixed the delivery. The successor model fixes
the **representation**, so the question has a place to be answered before anyone can get it wrong
again. And the stake is not academic: this number is the denominator of every mean anyone ever takes
over this measure.

### 7.4 What the successor model lets `firstlight` say for the first time

Nothing in the current publication declares any movement condition. Under R4 settled, that is
**unestablished** — not "additive". So the honest statement of `firstlight`'s state is:

> four families over one operand, with **no established movement law**, currently served by a Core
> image that has no edges to travel and therefore cannot expose the gap.

The successor model is the first representation able to *say* that. It is also, incidentally, the
first one able to say it **before** K1 adds hierarchies and the gap becomes reachable.

### 7.5 A ratification question arrives with a concrete instance

`sales`'s existence law is ratified and carried in `authority.ratifications`. The four families' laws
would be **authored and unratified**. Whether family law needs its own authority record — carried in
`authority`, on the universe pattern, never inline in a declaration — stops being hypothetical here.
Raised, not proposed (§9.3).

---

## 8. The smallest publication representation consistent with the model

Kinds, not fields.

| action | kind | note |
|---|---|---|
| **keep unchanged** | `universe`, `anchor`, `attribute`, `relationship`, `hierarchy`, `crosswalk` | untouched by this model |
| **re-scope** | `measure` → **the governed analytical input** | keeps: name, universe, constitutive anchor, operand value domain, Φ. **Sheds:** the member list, `root_member`, and any implied result type |
| **add — the one new kind** | **`family`** | identity (`family_id` + canonical name), universe, constitutive anchor(s), operand/parent references, foundation-law reference + governed parameters, participation, declared domain, exceptional cases. C6/C7/C8 inherited from the foundation law unless declared |
| **retire** | `member` | its content moves into `family`; nothing survives at the old scope |
| **re-base** | `boundary` | onto `(family, movement/edge)` rather than `(measure, across-token)`. The positive half is the family's declared domain. **No additivity field** |
| **promote** | **foundation-law vocabulary** | shared and versioned, cited by both sides. Core's operator registry is already this object with the right content (`combine`, `witness`, `is_monoid`, `re_entrant`, `accepts`/`out_rule`); what it lacks is standing |
| **carry** | `family_id` in the artifact | opaque to the consumer, never regenerated by a reader, refuse if absent. Generation open (ruling 6) |
| **version** | publication format **MAJOR** bump | an optional key cannot force a consumer that cannot represent the law to refuse; a major can |

**One new kind. One re-scoped. One retired. One re-based. One promoted.** That is the smallest set I
can find that carries all nine §4 responsibilities while satisfying every settled fact in §0 — without
inventing `admitted_reductions`, and without letting a name, a token or a mapping be identity.

What is deliberately **not** in it: no `Σ(F)` object (§2.2: *"the signature is not an additional
ontological kind"*), no state-schema/combine-law records (the foundation law holds them), no
per-family ratification record (raised, not proposed), and no separate law record beside the family —
§4's *"not necessarily separate records"* is taken at its word.

---

## 9. Open, and put up for ruling

1. **Does `measure` keep the governed-operand responsibility** (§1.1), or does a new kind take it and
   `measure` dissolve to pure namespace? **I recommend it keeps it** — the evidence is four-fold and
   three parts of it are already in the shipped tree — and it sits *below* the families, not above.
   What must not survive either way is the container role.
2. **Foundation-law inheritance: default-with-consent, or must-declare?** (§4) The model needs to
   distinguish "inherited" from "authored"; whether that is a recording obligation or a declaration
   obligation is open.
3. **Family-law ratification** (§7.5) — now concrete via `firstlight`.
4. **`family_id` generation** — deliberately open per ruling 6; the artifact's only obligation is to
   carry it and refuse if absent.
5. **`firstlight`'s `count` target** (§7.3) — an authoring decision, not an architectural one, but it
   blocks migration and it is the denominator of every future mean.
6. **Whether lineage edges between families publish now or at K1.** Nothing in `firstlight` needs
   them; MEAN does, the moment it exists.
7. **D2's five-way separation** (ruling 7) — namespace/default resolution · family identity · family
   law · generated/family-forming constructions · physical realization — is answered for the first
   four by §§1–3 above. **Generated/family-forming constructions are not**: the inline
   `mean(revenue@day)` case mints a family at request time, and where its identity comes from is not
   settled here.

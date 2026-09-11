# Unit D · D1 — the crosswalk
## Current Columna (v5-era ontology) → *The Theory of Data* v7.1

**Status:** desk draft, 2026-09-11. **No implementation.** Delivers Unit D's **D1**.
**Still current.** The D1 ruling that followed it is carried into
`specs/unit_d_synthesis_v0_2_successor_model.md`, which is the live synthesis; this crosswalk
remains the evidence base for it.

**Target text:** ToD **v7.1**, 7 September 2026, DOI `10.5281/zenodo.22649945`, as deposited at
`services/ask/deposits/w-theory-of-data.r08.md`. The unit was opened against v6; v7.1 supersedes it
and is what this crosswalk maps onto. Section numbers below are v7.1's.

**Source trees:** `columna@061e022`, `manifold-agent@d9ea705`.

---

## 0. The settled architectural fact this crosswalk is built on

**Ruled 2026-09-11 (Huayin), superseding the earlier classification:**

> `root_evaluator` is essentially the **measure-family reducer**, misplaced by the current Columna
> Core implementation at the measure / private-mapping level. **The reducer belongs to the measure
> family.** Treat this as a Columna Core modeling defect.
>
> ```text
> governed family law        establishes the family reducer
> private realization mapping    maps that already-established family to executable machinery
> ```
> The private mapping must not originate or decide the family reducer.

**The theory text settles it independently, and the citation is exact.** ToD v7.1 §3.9:

> *"A change of physical representation, retained basis, or execution route is **not** by itself
> family succession. **A change to an identity-bearing target, formation, participation, or declared
> continuation law is.**"*

Now apply that test to the shipped system. In `firstlight` the four governed member bodies are
**byte-identical**; the only thing that makes `revenue_sum` mean a sum and `revenue_max` mean a
maximum is `MemberRealization.root_evaluator` in the **private mapping**. Edit that one string from
`sum` to `count` and the asserted quantity changes from total revenue to a participation count —
**an identity-bearing change of target and formation, i.e. a family succession by §3.9, performed
below the governance line, with the governed publication unchanged.**

This also **reclassifies P2-02.** Its reproduction — *"four different meanings of one governed
`root_member` under one publication digest, four valid receipts"* — was amended on 2026-08-31 to
*"the publication under-determining its own meaning,"* expected to dissolve under P2-03's repair.
Under the corrected architecture it does not merely dissolve: it is the **demonstration** that a
private realization file can mint a family succession. It is evidence for the defect, not an artifact
of the receipt's scope. The amendment should be re-amended rather than struck.

**Consequently, one line of the Unit D synthesis of the same morning is superseded**, and the
supersession is recorded rather than edited away — see §7.

---

## 1. The v7.1 vocabulary the crosswalk maps onto

Three objects and one contract.

- **Measure family `F`** — *"a governed analytical identity with determinate formation and admitted
  measures under its law"* (§2.2). Constitutive anchors, operands, order definitions and
  participation conventions live **inside `F`** and do not become current anchors of `F@A`.
- **Measure `F@A`** — the family at one **current** anchor. `mean(revenue@order)@region` has a
  constitutive Order anchor and one current Region anchor.
- **`Σ(F)` / `family_id`** — the ex-ante identity-bearing declaration, canonicalized; `family_id ≠
  canonical_name`. *"A digest is one possible implementation, not a required mechanism"*; the
  signature is **not an additional ontological kind** (§2.2).
- **The one family-law contract (§4)** — nine responsibilities, with the governing caveat that
  matters for every row below: *"The contract has one authoritative account of the following facts.
  **They are not separate ontological kinds or necessarily separate records.**"*

| # | v7.1 contract responsibility (§4) |
|---|---|
| C1 | **Target specification** — the asserted quantity, by nominated defining construction or independent semantic specification, with applicability and defined-result conditions |
| C2 | **Identity and ancestry** — operand identities, constitutive anchors, law parameters, well-founded constitutive lineage. *Canonical names resolve identity; they do not mint it* |
| C3 | **Domain and movement** — the anchors at which the family is defined (`𝒜_F`) and the conditions licensing particular movements (`Γ_F(B→A)`) |
| C4 | **Formation** — how the analytical input is established, including contextual/multi-input dependencies |
| C5 | **Eligibility and participation** — which points the quantity applies to, which contributions the law consumes, governed restriction/completion |
| C6 | **Semantic values** — operand, state-family and result value domains; required operations and equality laws |
| C7 | **Sufficient-state bases** — independently establishable families, role-indexed anchor-local constructors, basis adequacy |
| C8 | **Continuation and agreement** — combination laws, conservation of contributions, path coherence, agreement of alternative admitted bases |
| C9 | **Exceptional cases and realization** — empty and undefined cases, evidence dependencies, permitted numerical guarantees, conditions for faithful reuse |

---

## 2. The crosswalk

`GOV` = governed publication (`manifold-agent`) · `CML` = the Core execution image · `MAP` = the
private core mapping · `REG` = Core's in-process operator registry · `RT` = runtime/engine state.

| # | Columna concept (where it lives) | v7.1 counterpart | verdict |
|---|---|---|---|
| **1** | `measure` declaration — `{value_type, root_member}` (+`fill_rule`, `default_reduction`) · **GOV** | **Not** a family. A *namespace entry* pointing at a root family, plus C6 (`value_type`) and C9 (`fill_rule`) fragments | **Partial / miscast.** A v5 "measure with aggregations hanging off it". Under v7.1 there is no object between the universe and the family; `revenue` is either a family or a canonical name resolving to one (§3.9) |
| **2** | `member` declaration — `{measure, anchor, universe}` · **GOV** | **This is the family** (`F`), or should be: it is the thing with a target, a formation and a continuation law | **The central defect.** Carries C2's anchor and universe and **nothing else** — no C1, C4, C7, C8. In `firstlight` all four are byte-identical |
| **3** | `root_member` — names the measure's default member · **GOV** | C2/§3.9's *"governed single-valued default completion"* — a shorter reference resolving to an already specified construction | **Right concept, zero consumers.** `grep` finds it only in fixtures and tests. The compiler never reads it (§2 of the ledger's Unit D section already said so; confirmed) |
| **4** | **`root_evaluator`** — one string · **MAP** | **C1 + C4**, and by selection also C6, C7, C8 | **Misplaced analytical law.** Decomposed in §3 below |
| **5** | `FAMILY { agg … }` in the `.cml` · **CML** | Two different things wearing one word — see rows 6 and 7 | **Split required (D2).** |
| **5a** | …its *membership set* | C1/C2 — **which families exist over this measure** | Legitimate, but it is a **list of families**, not a property of one |
| **5b** | …its per-member `BLOCKED { lineage }` (`BAnchor`) | **C3** — `Γ_F(B→A)`, the conditions licensing a movement | **Already `Law(F)`-shaped, and the only part of `FAMILY` that is.** Keep the concept; it is the half worth keeping |
| **5c** | …its per-member `ORDER <level>` | **C2** — a constitutive order parameter, identity-bearing (§7.2, §2.2) | Right concept, correct placement, wrong *kind* of object: it is inside `F`, not a modifier of a reducer token |
| **6** | `FamilyMember.agg` — an operator name · **CML** | A **name that indexes** C1/C4/C6/C7/C8 out of a global table — see §3 | **Under-determined.** §11.5.1: `count(I)` and `count(x@I)` are *"distinct targets"*; one token cannot name either |
| **7** | `MeasureColumn` — `(universe, home_table, pre_expr, logical_type, family{}, fill_rule, m_anchor, evidence, …)` · **CML** | A v5 container fusing C4, C6, C9, realization, and a set of families | **Fossil container.** Its fields belong to *different families* and to *realization*; it has no single v7.1 counterpart |
| **8** | `pre_expr` — `"amount"`, `"price*qty"` · **CML** | **C4** where it is an analytical contribution expression; **realization** where it is a column reference | **Conflated.** K0 forces it to a bare column, so today it is purely realization — but the construct does not draw the line |
| **9** | `fill_rule` (Φ_v) · **GOV → dropped** | **C9** — *"empty and undefined cases"* | Right concept, ruled to the right kind, **silently dropped at the compiler** (no reader, no refusal) |
| **10** | `m_anchor` / MCAR-MAR-MNAR · **CML** | **C5** — participation and governed completion | Right concept; currently a measure-level property where participation is per-family (§4.2) |
| **11** | `default_reduction` · **GOV → dropped** | **C1** for the root family — *"nominated defining construction"* | **Already governed, already published, already ruled distinct from `root_evaluator`, and read by nobody.** The existing half of the answer |
| **12** | `boundary` — `{measure, forbidden, across}` · **GOV** | **C3** — the negative half of domain-and-movement | Right concept; wrong scope (measure, not family) and wrong index (`across: "time"` where a lineage/edge belongs) |
| **13** | `Operator.deliver_sql` · **REG** | **Realization.** §4: *"A backend computation establishes neither merely by returning a value"* | Correctly realization — but bundled with rows 14–17 under one key |
| **14** | `Operator.combine` (`count`→`"sum"`) · **REG** | **C8** — the combination law | **Analytical law held per-operator-name, globally.** Core already knows formation ≠ continuation; it just does not let a family say so |
| **15** | `Operator.witness` (VALUE/SKETCH/ORDERED/HOLISTIC) · **REG** | **C7** — the sufficient-state construction | Analytical; same misplacement as row 14 |
| **16** | `Operator.is_monoid` / `re_entrant` · **REG** | **C8** — self-sufficiency (§5.2, §6.1) and path coherence | Analytical; same misplacement |
| **17** | `Operator.accepts` / `out_rule` · **REG** | **C6** — semantic value domains | Analytical vocabulary; correctly SHARED, correctly global (it is about the *law*, not about a family) |
| **18** | `Operator.in_core` | **Realization capability.** §4.1: *"a backend's inability to realize an admitted movement does not remove that movement from analytical law"* | Correct as a profile flag, provided it refuses rather than narrowing the law |
| **19** | `K0_REDUCERS` · **compiler** | **No counterpart as law.** A realization profile | Correct *as written* — it refuses with a named category rather than emitting a narrowed image. The model to copy |
| **20** | `DerivedColumn` + `License`/`FERTILE` · **CML** | **C3** positive half + **C2** lineage (§3.7) | Right concepts. Note §3.6: *"Geometric shape and family admission are separate judgments"* — a license is not conferred by the operator being a reducer |
| **21** | `resolution_anchor` (`AT <level>`) · **CML** | **C2** — the constitutive anchor, identity-bearing (§2.2: `mean(x@order) ≠ mean(x@customer)`) | Right concept, right place |
| **22** | witness key `(measure, member, base_level)` · **RT** | **C7 / §10.7** — retained sufficient state | **Wrong key.** `member` is a *finalizer's* name, so state is filed under the name of the number it will become (§10.1: *"reuse is a separate analytical claim"*) |
| **23** | `MeasureShape` / `PlannerView` · **CML** | No counterpart — a planner projection | Realization. No action |
| **24** | `evidence` (`PROVEN`/…) · **CML** | **C9** — *"evidence dependencies"*; §9 *"Evidence adequacy is relative to the law"* | Right concept; currently measure-scoped where §9 makes it law-relative |
| **25** | `universe.basis` (`events`/`spine`/`product`/`registry`) · **GOV** | §2.1/§2.3 — point existence and eligibility | Right concept, right level, already governed |
| **26** | `family_id` | **§2.2, `Σ(F)`** | **No counterpart anywhere in Columna.** Identity is carried by the declaration *name*, which §2.2 forbids: *"`family_id ≠ canonical_name`"* |

---

## 3. `root_evaluator`, decomposed

The correction says: identify the analytical concept it carries, and do not relocate the field
unchanged if its shape conflates law with realization. It does conflate, and the conflation is
**six-way**. One string in a private file currently decides:

| what the token selects | v7.1 responsibility | side |
|---|---|---|
| which quantity is asserted (`sum` vs `count` vs `max`) | **C1** Target specification | **analytical** |
| how the value is constituted at the constitutive anchor | **C4** Formation | **analytical** |
| `REGISTRY[agg].combine` — how partial results merge | **C8** Continuation | **analytical** |
| `REGISTRY[agg].witness` — what sufficient state is retained | **C7** Sufficient-state basis | **analytical** |
| `REGISTRY[agg].is_monoid` / `.re_entrant` | **C8** self-sufficiency, path coherence | **analytical** |
| `REGISTRY[agg].accepts` / `.out_rule` | **C6** Semantic values | **analytical** |
| `REGISTRY[agg].deliver_sql`, `.in_core` | — | **realization** |

So the honest statement of the defect is **not** "a field is in the wrong file." It is:

> **A single operator token, held on the realization side, is the sole carrier of five of the nine
> family-law responsibilities — and it carries them by *indexing a global per-operator table*, so
> every family that names the same operator is compelled to share one continuation law, one witness,
> one re-entry certification and one value signature, whether or not its law says so.**

And the token is **not even sufficient** to name the target it selects. §11.5.1: `count(I)` counts
participating analytical points; `count(x@I)` counts participation under the operand construction's
rule; *"These are distinct targets."* P1-10 is that sentence arriving as a served number — `count`
delivered `count(*)`, discarding its operand, so two members of one measure carried different
supports and `revenue.sum / revenue.count` served a mean over mismatched denominators. The registry
comment records the repair; the crosswalk records **why it was possible**: a reducer token is a
*fragment* of C1, and a fragment was doing C1's whole job.

### 3.1 The synonym hole closes — correcting my own note of this morning

The Unit D synthesis said the synonym-operator bypass (register `total` with algebra identical to
`sum`; `BLOCKED { sum }` is then not crossed) *"is an operator-identity defect and survives every
option here."* **Under the corrected architecture that is wrong, and I withdraw it.** The bypass
exists precisely *because* law is indexed by operator **name** into a global registry. Once the
family law itself establishes the reducer — once C1/C4/C8 are properties of `F` rather than of a
token — a synonym is either the same declared law (and inherits the bar) or a different family (and
must declare its own). §2.2 is the governing sentence: *"A canonical name resolves to one family
identity within a governed namespace and version… Two distinct active identities cannot be hidden
under one ambiguous canonical reference."* The bypass is a `family_id ≠ canonical_name` violation,
not a separate defect.

---

## 4. What a private realization mapping legitimately still needs

The point of the correction is the split, so the residue must be stated as carefully as the removal.
After family law establishes the reducer, a private mapping still owes — and only owes — **how this
already-established family is executed here**:

1. **The endpoint** — table/column (or connection) delivering the operand. Already `Endpoint`.
2. **The delivery expression** — the backend aggregate discharging the established formation
   (`deliver_sql`'s job), *chosen to satisfy a law it does not get to choose*.
3. **An executability claim** — whether this backend can discharge this family here, at all and
   exactly (`in_core`-shaped). §4.1 governs the failure mode: inability **refuses**; it does not
   narrow `𝒜_F`.
4. **Realization evidence** — freshness, data-state version, producer attestation (§9, §10.8).

Note what is *not* on that list: **which reducer.** The mapping's obligation becomes a
**correspondence check** — *can this realization discharge the declared family?* — with failure as a
named refusal. That is the same inversion the compiler already performs correctly for anchors (it
checks the mapping's components against the publication's) and performs backwards for members.

Two guard-rails the correction implies and the text confirms:

- **A mapping change must never be a family succession.** §3.9 gives the test directly. If editing a
  mapping can change the asserted target, the boundary is wrong — which is the current state, and is
  the whole content of P2-02.
- **A mapping change is *permitted* to be invisible to identity.** §3.9 again: *"A change of physical
  representation, retained basis, or execution route is not by itself family succession."* So this is
  not an argument for pushing realization above the line. The line moves in exactly one direction.

---

## 5. Concepts with no v7.1 counterpart — and why that is fine

- **`MeasureColumn`** (row 7) — a v5 container. Dissolves; its fields redistribute.
- **`measure` as an object between universe and family** (row 1) — no v7.1 object sits there. It
  survives as a **namespace/default-completion** device (§3.9), which is what `root_member` already
  wants to be.
- **`MeasureShape` / `PlannerView`** — planner projections. Realization; no action.
- **`K0_REDUCERS`** — a profile. **Correct as built**: §4.1 says a backend's limits do not shrink the
  law, and K0 refuses with a named category instead of emitting a narrowed image. This row is the
  model the others should be measured against.

## 6. The inverse direction — v7.1 responsibilities with no Columna carrier

| responsibility | carrier today |
|---|---|
| **C1** Target specification | operator token in **MAP** (row 4) |
| **C2** Identity — `family_id`, `Σ(F)` | **none**; identity is the declaration name (row 26) |
| **C3** Domain and movement | `BLOCKED`/`FERTILE` in **CML**; `boundary` in **GOV**, which the compiler refuses |
| **C4** Formation | split between the operator token (**MAP**) and `pre_expr` (**CML**) |
| **C5** Eligibility and participation | `m_anchor`, `basis`, universe `restriction` — measure/universe-scoped, not family-scoped |
| **C6** Semantic values | `value_type` (**GOV**) + registry signature (**REG**) — the one responsibility carried well |
| **C7** Sufficient-state bases | `Operator.witness` (**REG**, global) + a witness key that is wrong (row 22) |
| **C8** Continuation and agreement | `Operator.combine`/`is_monoid`/`re_entrant` (**REG**, global) |
| **C9** Exceptional cases | `fill_rule` (**GOV**, dropped), `evidence` (**CML**) |

**Read down the right-hand column: not one responsibility is carried by the governed family.** Six of
nine are carried by objects keyed on something other than the family — an operator name, a measure, a
universe, or a private mapping. That is the v5 ontology in one table, and it is the answer D1 was
opened to produce.

---

## 7. What this supersedes in the Unit D synthesis

`specs/unit_d_family_law_carrier_synthesis_v0_1.md`, same day. Superseded, not edited away:

1. **O9 is withdrawn as written.** It said *"`root_evaluator` stays realization… the name and the
   file are right; the direction of flow is wrong."* The name and the file are **not** right: the
   concept is the family reducer and belongs to `Law(F)`. The *operational* half of O9 survives —
   the mapping's role becomes a correspondence check — but it is now a consequence of relocating the
   concept, not of leaving it in place.
2. **§2 item 5 strengthens.** `default_reduction` being *"already governed, already published, already
   ruled distinct from `root_evaluator`"* is no longer merely convenient; it is the **prior ruling
   that already anticipated this one**, and the gap is that nothing reads it.
3. **§5 Part 1(3) is under-scoped.** *"One field on `member` — the declared operator identity"* would
   relocate a token that conflates six responsibilities, which is exactly what the correction forbids
   (*"do not simply relocate the existing field unchanged"*). What `member` must gain is the family's
   **reduction law**, at whatever granularity §4's *"not necessarily separate records"* permits —
   minimally its target/formation, with continuation, witness and value-domain either stated or
   explicitly inherited from a named law rather than silently inherited from a name.
4. **§1 O1's falsifier note is withdrawn** — see §3.1. The synonym bypass closes under the correction.
5. **§5 Part 2 is unaffected and, if anything, reinforced.** The recommendation against creating a
   positive `admitted_reductions` enumeration stands: v7.1 §4 has no such slot, and its
   *"not separate ontological kinds or necessarily separate records"* clause is the strongest
   statement yet that the corpus declines to fix record granularity.
6. **§7's D4 count changes.** Under Part 1(3) as written it was **1 of 1** (`firstlight`, fixed by
   regeneration). It stays 1 of 1 — but the regeneration is no longer mechanical: `firstlight`'s four
   members must acquire *declared law*, and the only place that law currently exists is a private
   mapping. **Regenerating the publication requires first deciding what those four families' laws
   are.** That is authoring work, not a rebuild, and it is the first place this ruling touches a
   human.

---

## 8. Open after D1

1. **Granularity** — §4's *"not necessarily separate records"* leaves open whether C1/C4/C7/C8 are
   one declared law, a named reusable law (`SUM`, `COUNT`, `MIN`, `MAX` as **§11.5 foundation laws**),
   or per-family fields. **The foundation-law reading looks strongest and is not ruled:** v7.1
   catalogues SUM/COUNT/MIN/MAX as named constructions, so a family could declare *"my law is the
   foundation law SUM, over operand X, with participation P"* — which is exactly how §11.5 talks, and
   which keeps the registry as SHARED vocabulary instead of demoting it.
2. **`family_id`** (row 26) — §2.2 requires identity distinct from name, and Columna has none. Not in
   Unit D's charter as opened; it is now visibly adjacent, because the synonym hole (§3.1) is a
   name-as-identity failure.
3. **R4, unchanged and still first** — *"additivity is the absence of a boundary"* vs *"absence of
   prohibition is not permission."*
4. **Whether `measure` survives as an object at all** (row 1), or becomes purely a namespace with a
   default completion. D2 cannot be finished without this.
5. **The witness key** (row 22) — a C7 defect the correction makes more urgent, since relocating the
   reducer to the family is precisely what would give the key something correct to be keyed on.

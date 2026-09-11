# Unit D — the governed carrier for `Law(F)`
## Synthesis for ruling. No representation is implemented; one is recommended.

**Status:** desk draft, 2026-09-11, awaiting ruling. Prepared under the Unit D framing ruling of the
same date: *do not design an "additivity field" or a replacement for `boundary`; the governing object
is the family law; the direction is to make the already-governing family-law obligations REPRESENTABLE
through the Manifold → governed-publication → Core boundary, rather than reconstructed from operator
names, absent boundaries, private mappings, or runtime behavior.*

All file claims are from the trees at `columna@061e022` (post-#271) and `manifold-agent@d9ea705`.

> ## ⚠ SUPERSEDED — 2026-09-11. Read `specs/unit_d_synthesis_v0_2_successor_model.md` instead.
>
> v0.2 is the current synthesis: the conceptual successor model (objects, identities, §4 law
> allocation, declared-vs-derived, realization reference, and `firstlight`'s mapping), written to
> the D1 ruling of the same day. This document is kept for the reasoning that produced the earlier
> reading. The first correction pass is recorded below and remains accurate as far as it goes.
>
> Huayin corrected the classification of `root_evaluator`: it is **the measure-family reducer,
> misplaced at the measure/private-mapping level — a Columna Core modeling defect — and the reducer
> belongs to the measure family.** The private mapping must not originate or decide it.
>
> Six passages here are affected, and the accounting is in
> **`specs/unit_d_d1_crosswalk_v0_1.md` §7**. In short: **O9 is withdrawn as written** (the field's
> *file* is wrong, not only its direction of flow); **§5 Part 1(3) is under-scoped** (relocating the
> token unchanged is exactly what the correction forbids — it conflates six of v7.1's nine
> family-law responsibilities); **§1 O1's "the synonym hole survives every option" note is withdrawn**
> — under the correction it closes. **§5 Part 2 is unaffected and reinforced.**
>
> This document is left as written. The corrections live in the crosswalk, dated, so the reasoning
> that produced the earlier reading stays legible.

---

## 0. The finding that sets the frame

Unit D was opened as an elegance question — where should family law live? Three verified facts turn it
into a correctness question, and they should be read together before anything else.

**(a) `Law(F)` has no governed carrier at all.** The publication's required bodies are
`measure: (value_type, root_member)` and `member: (measure, anchor, universe)`
(`manifold-agent/src/manifold_agent/validate.py:84-85`). In the only real governed publication —
`columna/packages/columna-server/fixtures/firstlight/governed-publication.json` — the four members
`revenue_sum`, `revenue_count`, `revenue_min`, `revenue_max` have **byte-identical bodies**
(`{anchor: sale_at, measure: revenue, universe: sales}`). The only thing distinguishing one family
member from another, in the governed artifact, is **the declaration's name**.

**(b) Core reconstructs the family from the PRIVATE MAPPING.** `compiler/compile.py:321-329`:

```python
_check_reducer(r.root_evaluator, dtype, subject=f"member {d.name}")
...
aggs.append(r.root_evaluator)
measure_blocks.append(emit.measure_block(md.name, universe, table, column, tuple(sorted(aggs)), dtype))
```

`r` is a `MemberRealization`. Core's `FAMILY {…}` — its positive admission set, the thing a query's
`member in meas.family` check consults — is assembled **entirely out of `root_evaluator`**, a field
whose own docstring says (`compiler/inputs.py:166-169`):

> *"`root_evaluator` is captured, never invented: a compiler that chose a reducer would be
> manufacturing analytical law."*

The compiler is not manufacturing analytical law. It is **importing it from the wrong side of the
boundary** — one level up from where that docstring is looking. The ruling that `root_evaluator` is
realization/root-formation information and not family law is correct and is already recorded; the
wiring contradicts it.

**(c) K0's lawfulness is an accident of scope, not a property of the boundary.**
`compile.py:104-107` refuses `boundary` outright:

> `boundary cannot be represented: "across" has no slot anywhere in the Core execution grammar, and
> product-scoped forbiddance collapses in blocked_lineages`

and `emit.py:14` records that K0 emits *SOURCE_MANIFOLD, UNIVERSE (unrestricted), LEVEL (base),
MEASURE (+ FAMILY)* and nothing else — **no hierarchies, therefore no edges, therefore no travel.**
An empty B-anchor on an image with nowhere to travel is vacuously safe. So today: a publication that
carries a prohibition cannot compile, and a publication that compiles has no movement to prohibit.

The moment K1 admits `hierarchy`, both halves fail at once: a publication carrying a boundary still
refuses (its law is unrepresentable), and a publication carrying **no** boundary compiles into an
image whose family is open along every lineage, sourced from a private realization file. That is the
deadline this synthesis is written against.

> **The frame, then: the boundary currently transports realization where law should be, and refuses
> law where law exists. Both are the same defect seen from two sides — there is no channel for
> `Law(F)`, so law travels in the only channel there is.**

---

## 1. The minimum semantic obligations on a governed `Law(F)` representation

Ten obligations. Each states the obligation, its authority, and the concrete case that falsifies a
carrier which does not meet it. They are deliberately stated as constraints on ANY representation,
because ToD leaves record granularity and concrete encoding open.

**O1 · Law belongs to family identity, and must not be recoverable only from a spelling.**
A carrier must attach `Law(F)` to the declared family, not to a member's name or a reducer token.
*Authority:* ToD:1652-1660 — changing `Law(F)` mints a family **succession**; so law must sit in the
object whose change is a succession. *Falsifier:* the synonym operator — register `total` with algebra
byte-identical to `sum`, and a `BLOCKED { … }` naming `sum` is silently not crossed. (Note: this
particular hole is an **operator-identity** defect and is NOT fixed by any carrier choice below. It
must stay rowed separately; a carrier that pretends to fix it is lying.)

**O2 · Three states, all distinguishable: admitted / prohibited / unestablished.**
Absence of prohibition is not permission, and "nobody has ruled" must be readable as itself.
*Authority:* the standing invariant; DG-4. *Falsifier, already live:* Columna runs two admission
polarities with **opposite defaults** in one system — `FAMILY {…}` is a positive enumeration, closed
by default; `BLOCKED {…}` is negative, open by default. DG-4 verbatim: *"The declared-bar case
refuses; the under-declared case does not."* A stock declared `FAMILY { last }` still serves an
inline `sum(x@day)` because there is no bar to cross.

**O3 · Prohibition is lineage/edge-indexed, not measure-global.**
*Authority:* β(κ) ⊆ Axis is per-capability, per-axis (CC:710-723); Core's `blocked_lineages` is per
member × lineage (`model.py:150-151`). *Falsifier:* a measure additive across `store` and not across
`calendar` — `boundary.across` today carries one coarse token (`"time"`, minted at
`interview.py:411-413`) and cannot say it.

**O4 · Family-level domain and edge-level validity stay distinct.**
Where a measure is DEFINED is not the same question as whether a given rollup edge is VALID. A carrier
that folds them makes an undefined region read as a prohibition and a prohibited move read as
undefined — and the two have opposite remedies.

**O5 · Sufficient state is described, not enumerated by consumer.**
A carrier must not make a consumer's analytical identity part of the state's identity.
*Authority:* MA:788-794 — *"reuse of one state carrier does not make the resulting analytical families
identical"*; Σ(F) (ToD:1587-1599) contains **no state-carrier component**. *Falsifier, already
committed:* Columna's witness key is `(measure, member, base_level)` where `member` is the
**finalizer's** name, and `publish_witnesses` takes `next(iter(meas.family))`, so a second member
never gets a witness and never finds one. The store already keys sufficient state by one consumer's
identity. A carrier must not make that shape a rule.

**O6 · Self-sufficient continuation ≠ usable in another family's sufficient-state basis.**
Two relations that do not substitute for each other (reconciliation §4.1). One carrier slot cannot
mean both; `revenue_count` being needed to finalize a mean is not `revenue_count` continuing itself.

**O7 · Participation law, Φ (empty/undefined), constitutive order, approximation/convention, and
exceptional cases are declared or absent — never inferred from execution.**
*Authority:* MA:832 — *"the planner applies declared law. It does not infer missing law."*
*Falsifier, already live and independent of every fork below:* `fill_rule` (Φ_v) is authored governed
meaning, is a ruled per-MEASURE clause with `MISPLACED_CLAUSE` enforcement
(`validate.py:105-127`), is carried in the publication — and **the compiler never reads it and never
refuses it.** `grep fill_rule columna_core/compiler/*.py` returns nothing. Same for
`default_reduction`. The scope gate refuses by declaration KIND (`compile.py:92-110`); it has no
refusal at body-KEY granularity. So a governed Φ silently does not reach the image.

**O8 · Structural operations are not family movement.**
Broadcast / allocation / assignment / universe passage must be representable as **not** establishing a
finer measure of the same family. *Authority:* ToD §3.6 — *"replication of a coarse value for
participation in a finer expression does not establish a finer measure of the same family"*;
Frame-QL §4.7 on broadcast — *"preserves the identity of the scalar operand… does not establish
`revenue @ {customer}` merely by copying the scalar value."* *Carrier consequence:* it must not be
possible to acquire a finer family member by a structural route the carrier never records.

**O9 · `root_evaluator` stays realization, and must stop being the source of family membership.**
The name and the file are right; the direction of flow is wrong. A carrier fix must leave
`root_evaluator` as the answer to *"which physical reduction realizes this declared member"* and make
the declared member itself governed — turning `compile.py:321-329` from a **source** into a
**correspondence check**.

**O10 · Governed law survives publication, and a consumer that cannot represent it refuses.**
*Authority:* already this compiler's own stated doctrine — *"REFUSAL BEFORE OMISSION… a silently-
dropping compiler would make the receipt bind a publication to an image that does not carry its
meaning"* (`compile.py:18-21`) — and already true at KIND granularity, already false at KEY
granularity (O7). Whatever the carrier's granularity is, the refusal test must be **total over it**.

---

## 2. What already exists and must be preserved rather than reinvented

Nine objects. Several of them are more than half of the answer, which is the main reason this
synthesis recommends a small move.

1. **The publication envelope.** Declaration-native `{kind, name, body}` in authored order; meaning
   separate from authority; `publication_format_version` as its own dimension keyed on the major;
   deterministic JSON readable with the standard library. Any law carrier is a body (or a kind)
   INSIDE this envelope. **Do not invent a second artifact.**
2. **Authority / meaning separation.** `authority.ratifications`, keyed by universe, never inline in a
   declaration: *"the law is meaning; ratification is authority over it."* If family law ever needs
   ratification, it goes in `authority` on the same pattern — not as a field on the law record.
3. **`boundary` as the prohibition declaration** — `(measure, forbidden, across)`, born logical with
   no gate (*"a movement a measure may not cross (a B-law; never verifiable)"*, `interview.py:11`),
   and **already carried in the publication even though Core cannot read it**
   (`publication.py:23-26`). Its defects are INDEXING (O3) and SCOPE (measure-level where
   member/family-level belongs) — not existence. The ruling not to replace it is right.
4. **`fill_rule` and the `KIND_ONLY_CLAUSES` discipline.** Φ is per-measure by ruling, enforced by
   `MISPLACED_CLAUSE`, with the reasoning written where it can be read: *"Φ answers what kind of
   quantity this is — revenue is a flow, a level is a stock — and that never changes with the
   anchor."* That "one clause belongs to exactly one kind's contract, and misplacement is an error"
   shape is the right shape for every further law clause.
5. **`default_reduction`, already governed, already published.** P0(a) put the governed measure's
   default reduction family on the measure, *"distinct from a binding's `root_evaluator`… even where
   the two coincide. Persisted so the lowering never invents it"* — and OPAQUE to the Manifold, which
   validates only its PLACEMENT because the reducer vocabulary is the engine's. **This is the existing
   half of the answer and it is already the right design.** Part of the remedy is therefore not new
   representation at all: it is making the consumer read what the producer already publishes.
6. **Core's B-anchor derivation.** Verdict computed from declared structure — traversed lineages from
   `find_path`/`out_edges`, law set as the union of `blocked[reducer]` over governed ancestry,
   `crossed ∩ law ≠ ∅ → Refuse`. This is the one genuinely DERIVED negative fragment in the system and
   it derives from declared structure, which is exactly right. Preserve the mechanism; the only
   question is what feeds it.
7. **The refusal taxonomy** — `LogicalMeaningMissing` / `ExecutionRepresentationGap` /
   `UnsupportedCoreCapability` / `MappingIncomplete`. These are precisely the four ways a law carrier
   can fail at a boundary (the law is absent / Core cannot represent it / Core cannot do it / the
   realization does not correspond). Reuse them; do not mint a fifth.
8. **The operator registry's split** — SHARED vocabulary, CORE mechanics. Already correct. What it
   cannot express is a STATE requirement (`Req(κ) = {X = X_κ}` demands exactly a type match,
   CC: a capability cannot say *"I require a state satisfying law L"*). That gap is O5's, not the
   registry's.
9. **The lowering receipt's byte digest over the image as shipped.** Determinism is a correctness
   property here. Any law the carrier adds must emit deterministically or the receipt binding breaks.

---

## 3. The genuinely open representation choices

**R1 · Where family law attaches: the `measure` body, the `member` body, or a new declaration kind.**
ToD explicitly leaves record granularity open. One asymmetry worth naming: Core's family is
**keyed by operator** and *"cannot hold both"* two members realizing one reducer
(`compile.py:323-325`) — already rowed as a carrier-of-law defect rather than a naming defect. If the
governed member becomes the law's home, the governed layer will be able to express a family Core
cannot represent. That is legitimate (it refuses) but it should be a decision, not a surprise.

**R2 · Positive admission: enumerated, or derived from premise satisfaction?**
This is the hinge and it is the same hinge as Q5's Form A/Form B fork.
- The proved fragment has **no positive admission enumeration anywhere** — every registered capability
  applies to every contract subject to the five RED1 premises; admission is by premise satisfaction,
  never by list membership. Its one candidate slot, `admitted_reductions` (ToD:2381), **occurs exactly
  once in the entire corpus and is never defined, typed, or used.**
- Core **does** enumerate (`FAMILY {…}`, closed by default), which makes Columna *more* restrictive
  than the corpus on the positive side and *less* complete on the negative side (β over lineages only;
  no γ counterpart at all).
So: does the governed layer become corpus-shaped (negative-only) or Core-shaped (enumerated)? Creating
`admitted_reductions` in Columna would be **Columna inventing theory into an undefined published
slot.**

**R3 · What `across` ranges over.** A hierarchy/lineage name (Core has these), an axis in the β sense
(the corpus has these), an anchor component, or a coordinate. Today it carries the token `"time"`.
Three different granularities; one must be named, and the choice determines whether Core can represent
the prohibition at all.

**R4 · How "unestablished" is marked — and this one is a live contradiction, not merely open.**
The authoring layer has a standing ruling: *"additivity is the **absence** of a boundary, not a
boundary of its own. An additive answer produces **nothing**; only a non-additive answer produces a
`boundary`"* (`logical_body_spec.md:15-17`, implemented at `interview.py:408-413`). The Unit D
invariant says: *absence of prohibition is not permission.* **Under the existing ruling, absence
means "additive" — i.e. permission.** Both cannot hold at the carrier. Either the additivity ruling
moves (an additive answer produces a positive record of the ruling), or the third state is carried
somewhere other than the boundary's presence/absence (e.g. a record that the question was ASKED).
*I recommend this be ruled before anything else in Unit D, because every alternative in §4 inherits
whichever way it goes.*

**R5 · Refusal granularity.** Kind-level (today) or total over body keys (O10). A total refusal
requires the consumer to know the complete governed key vocabulary — which promotes that vocabulary
from a convention into a **versioned contract between two repositories**. That is a real cost and a
real benefit, and it is a choice.

**R6 · Whether family law is ratifiable.** Universes carry existence-law ratification; families carry
nothing. If `Law(F)` is governed meaning under authority, the parallel is at least askable. Not
proposed here — noted so the silence is deliberate.

---

## 4. The strongest plausible alternatives

### A · Enrich `member` with its declared operator + movement; keep `boundary` for prohibition.
The governed member states which family member it IS; `boundary` keeps stating what is forbidden.
- **For:** smallest move; `member` is already the family-participant object; kills the
  law-from-the-name defect at its source; converts `compile.py:321-329` from source to check in one
  place; nothing new to version except a member key.
- **Against:** admitted and prohibited then live in two declarations, so O2's three-way distinction is
  a JOIN rather than a read; Core's operator-keying collision (R1) is untouched.

### B · A `family` (or `law`) declaration kind carrying Σ(F)'s law slots.
One record per family: `state_schema`, `combine_law`, `finalizer`, `ordering_semantics`, plus whatever
R2 rules for admission.
- **For:** matches ToD's `Law(F)` object directly; one place to look; a family succession becomes
  literally a new record, making ToD:1652-1660 mechanical; holds the three-way state naturally.
- **Against:** four of its five slots have **no consumer anywhere in Columna** — Core has no
  `state_schema` object and no `combine_law` object — so this is building empty rooms and inviting
  them to be furnished by guess. Worse, there is a specific trap: *enriching `Law(F)` to license a
  capability MINTS A NEW FAMILY* (ToD:1652-1660), so a carrier that invites licensing decisions into
  the `Law(F)` record is dangerous by construction. The reconciliation warns exactly this
  (*"the relation must not live inside `Law(F)`"*).

### C · Corpus-shaped: no positive enumeration in the governed layer at all.
`member` declares its operator (identity, not permission); prohibition is properly indexed; admission
is computed from (operator's declared law) × (declared boundaries) × (declared structure).
- **For:** matches the proved fragment exactly — β/γ, typed, total, negative, open by default;
  preserves and merely widens Core's existing derived B-anchor; makes "absence of prohibition is not
  permission" a property of the PREMISE SET rather than of a field; does not reify
  `admitted_reductions`.
- **Against:** Core enumerates today and is closed by default, so the compiler would have to
  MANUFACTURE Core's positive set from governed negatives — uncomfortably close to the inference being
  removed. Unless Core's `FAMILY` is re-read as **which members are realized here** rather than as
  law — which is, interestingly, exactly what `root_evaluator` already is.

### D · Ship nothing structural; close the two live defects and let the carrier wait for K1.
Fix (i) the compiler reading law out of the mapping and (ii) the silent body-key omission, and defer
the fork.
- **For:** both defects are real, both are independent of every fork above, and both are pure
  subtraction of inference.
- **Against:** (i) cannot actually be fixed without the governed member stating its operator — so D
  collapses into a subset of A the moment it is attempted. Which is itself a useful finding.

---

## 5. Recommendation

The evidence makes a **two-part** recommendation clearly preferable, and the first part is the one I
would ask to be ruled first — it is representation-neutral and it survives any outcome of R2/R4.

### Part 1 — stop the boundary from carrying law in the realization channel. (Subtractive.)
1. **Family membership is read from governed declarations, not from the mapping.** `compile.py` takes
   the member's declared operator identity (and/or the measure's already-published
   `default_reduction`) as the source of `FAMILY {…}`, and uses `root_evaluator` only to verify that
   the realization can discharge the declared member — `MappingIncomplete` on mismatch. `root_evaluator`
   then genuinely is what its docstring says it is.
2. **Refusal becomes total over body keys, not just kinds.** A governed key the consumer does not
   understand refuses with a named category. This is the compiler's own doctrine applied one level
   deeper, and it immediately closes the live `fill_rule` / `default_reduction` silent-omission
   (O7/O10).
3. **The minimum carrier addition that (1) forces: one field on `member`** — the declared family
   member's operator identity. This is the only thing K0 currently steals, and it is the only addition
   that evidence (rather than the open fork) compels.

This is the whole of what the discovery has actually PROVEN is wrong. It is worth landing as its own
unit.

### Part 2 — on the fork itself: C's principle with A's placement. Against B, for now.
Law lives on objects that already exist (`member`, `measure`, `boundary`); prohibition is indexed to a
lineage/edge rather than a coarse `across` token; **no positive `admitted_reductions` enumeration is
created in the governed layer.** Reasons, in order of weight:
- the corpus has no positive enumeration and its one candidate slot is undefined — creating it here is
  Columna legislating into the theory's silence;
- Form A (enumerated consumers) is independently disfavoured by the coupling test — a state's identity
  would become a function of the consumer population **at production time**, a closed-world assumption
  about the future — *and* it is the exact shape Columna's witness key already got wrong (O5). Ruling
  Form A would promote a known defect to a rule;
- B's empty slots have no consumer, and B's record is the one place ToD warns law-plus-licensing must
  not be combined;
- under C, Core's `FAMILY` reads correctly as **realized** membership rather than as law, which is the
  reading that puts `root_evaluator` exactly where the ledger already ruled it belongs.

### And one thing I recommend be ruled BEFORE either part: **R4.**
The additivity ruling and the "absence of prohibition is not permission" invariant contradict each
other at the carrier. Every alternative above inherits the answer, and the authoring layer's behaviour
changes either way.

---

## 6. Consequences per layer

**Manifold authoring.** A steward can already answer the additivity question; what changes is that the
answer must become **indexed** (non-additive across WHICH lineage) and, if R4 goes the invariant's
way, that an additive answer must produce a positive record instead of silence. That is a follow-up
question in an existing interview, not a new authoring surface. `member` gains a declared operator —
which is what an author already means when they name a member `revenue_sum`, so the authoring
experience gets *more* honest, not heavier.

**Governed publication.** No new artifact, no envelope change. But adding a REQUIRED key to `member`
is breaking for a validating reader — which is precisely why `publication_format_version` is its own
dimension with the loader keying on the major. Bodies stay physical-clean. `boundary` continues to be
carried whether or not any consumer can read it; that rule is already written down and is exactly
right for a governed law.

**Core compilation.** `_OUT_OF_SCOPE["boundary"]` splits: the lineage-indexed subset becomes
representable, the rest keeps refusing with the same named category. Core is permitted a narrower
profile — the #271 ruling generalizes here: *plan, run and EXPLAIN must simply agree about the
limitation.* `emit` gains `BLOCKED { … }` inside `FAMILY`. The `aggs` list stops coming from the
mapping. **This is the change that makes the K1 hierarchy step safe rather than accidentally safe.**

**Core runtime.** Mechanism unchanged — the B-anchor derivation already computes the verdict; it
simply receives non-empty input on a compiled image for the first time. Note what is NOT fixed: the
synonym-operator hole (O1's falsifier) is an operator-identity defect and survives every option here.
It must stay rowed on its own.

**Platform, later.** The carrier must not key law by carrier or by consumer, or Platform inherits the
witness-key defect at cross-domain scale. C-with-A keeps `Law(F)`-side authority and state-side
description separate, which is the precondition for Platform's identity-keyed materialization and for
backend-independent governed state standing. The reductio holds: sufficient state does not move to
Platform merely because it is reusable.

---

## 7. Migration and compatibility

The burden is **effectively nil, and that is an asset with an expiry date.**

- One real governed publication exists (`firstlight`: 1 measure, 4 members, 1 universe, 1 anchor,
  **0 boundaries**), plus its fixture copy under `columna_server/governed/firstlight/` with a
  `PROVENANCE.md` recording where it came from. It is a PRODUCED artifact: regenerate it from the
  Manifold rather than hand-editing it.
- **D4's count, stated plainly: 1 of 1.** Under Part 1(3) — a required declared-operator key on
  `member` — the publications that compile today and would stop compiling are *`firstlight`*, and
  that is the entire set. It stops compiling for exactly the right reason (its members do not say
  which family member they are) and it resumes by being regenerated from the Manifold that already
  knows. Under Part 2 alone, with no required key, the count is **0** — nothing that compiles today
  carries a boundary.
- No external consumers. No published format contract outside these two repositories.
- Therefore: **bump `publication_format_version` MAJOR rather than adding an optional key.** An
  optional key cannot force a consumer that cannot represent the law to refuse (O10); a major bump
  can, because the loader already refuses an unsupported major with a message that says so.
- The lowering receipt's digest changes. That is correct and detected, not a problem — the receipt
  exists to notice exactly this.
- No deprecation window, no dual-read path, no compatibility shim, no sugar retained. Today's
  `parse_frameql` retirement is the pattern and the precedent: retire the surface, quarantine the
  reading, keep the tests as a dated pin.

> **This is the cheapest this change will ever be.** Every further month of Studio authoring produces
> governed publications whose members' law is recoverable only from their names.

---

## 8. Against the unit's own deliverables

This synthesis answers the seven questions put to it on 2026-09-11. Measured against Unit D's
original D1–D4, it covers **D2** (§1 O2/O3 and §4 — `FAMILY`'s two jobs, and which half is
`Law(F)`-shaped), **D3** (§5 Part 1 — `root_evaluator` stays as root formation, and stops being the
source of membership), and **D4** (§7, with the count).

**D1 — the full v5→v6 crosswalk table — is NOT delivered here and is not superseded.** Every row of
it (`measure`, `member`, `family`, `MeasureColumn`, `FamilyMember`, `root_member`, `root_evaluator`,
`FAMILY {…}`, `K0_REDUCERS`) is still owed, and the recommendation in §5 is stated so that it does
not presuppose D1's answers: Part 1 is subtractive and survives any crosswalk, and Part 2 is a
principle with a placement, not a schema. If D1 later shows a row with no v6 counterpart, that is
information Part 2 must absorb — not a contradiction of it.

One thing the ledger's Unit D section already said, now confirmed by reading rather than asserted:
*"it sees governed members, ignores `root_member`, reads the member's `root_evaluator`, drops the
governed member name, and rebuilds the Core family from operator names."* §0(b) is that sentence with
line numbers on it. The new part is §0(c) — that the only reason this has not yet produced a wrong
number is that K0 emits no edges, so nothing can travel.

---

## 9. What this synthesis does NOT propose

No schema. No code. No field names beyond the one in Part 1(3), and that one is named by its role, not
its spelling. No ruling on R2 or R4 — both are put up for ruling. No revision to the Measure Algebra
or to ToD. No new refusal category. No `admitted_reductions`. No claim that the synonym-operator hole
or the witness-key defect is addressed by any option here; both are named so they cannot be quietly
absorbed into a carrier decision they do not belong to.

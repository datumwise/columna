# C3 · family domain and edge validity — bounded implementation plan

**Standing.** A PLAN, checked and not executed. No engine code is changed by this document. It
responds to the steward's rulings of 2026-09-22 (nine numbered items, this session), which answered
Q-1…Q-4 of `c3_domain_and_movement_recon_v0_1.md` §12 and deliberately held Q-5 and Q-6.

**Checked against**, as instructed, before any seam was proposed: ToD v7.1
(`d777b3f6_…_zenodo_22649945.md`), the v7.2 addendum ruling (item 1 below — **no such material exists
yet**, §7.1), native v3 (`fixtures_v3/native-v3-publication.json`, `governed/native.py`), `fcf-2`
(`native.py:110-116`), C1–C4 (`native_c1…`/`native_c2…`/`native_c3…`/`native_c4…_record_v0_1.md`),
and the legacy witnesses (`movement.py`, `model.py` `BAnchor`, `planner.py`, `afternoon.cml`).
Secondary: Measure Algebra v1.0 / v2.0 rev1, Frame-QL Platform Profile v0.3, Frame-QL 1.0,
`ruling_2026_09_15_universe_constitution.md`, ToD v6.1 (`services/ask/deposits/w-theory-of-data.r06.md`).

**Bottom line.** The rulings are implementable, and the implementation is small — one declared fact,
one derived predicate, and a split of one responsibility. **Eight stop-gates stand in front of it**
(§5), of which three are blocking and require a ruling: a shipped test that forbids the rule's own
inputs (SG-1), a biconditional that is false as written (SG-2), and a soundness hole in the
family-indexing that the earlier falsification pass did not find (SG-3).

---

## 1 · The rulings as adopted, with three provenance corrections

The rulings stand. What follows corrects where they are *sourced from*, which matters because the
plan is required to cite an authority for every governed fact it moves.

### P-1 · "Family root" is not a new term. It is an undisposed v6.1 inheritance.

Ruling 1 directs that the term be *"recorded as such [new]; do not attribute it to ToD v7.1."* The
second half is correct and is preserved. **The first half is wrong.** ToD v6.1 §5.2 is titled
**"Designated family root"** (`services/ask/deposits/w-theory-of-data.r06.md:1124`):

> "Every family declaration designates one governed family root: \(F@R_F\). **The designation is
> constitutive.** … universe root: where does governed point geometry begin? family root: where does
> this governed family declaration begin?" (`:1126-1143`)

and the v6.1 glossary (`:2522`):

> "**Family root.** The designated governed measure \(F@R_F\) at which the family declaration
> begins. Its uniqueness comes from declaration, not from an assumed unique greatest refinement in
> the anchor partial order."

It was moreover **identity-bearing**: `:1591-1599` makes `R_F` a component of the v6.1 signature
`Σ(F) = (U_F, R_F, Parents(F), Establish(F), Law(F), Contracts_id(F))`.

**The disposition gap, which is the lawful opening.** v7.1 Appendix C.1 (`:1394`) lists *"designated
family origins"* among what v6.1 established. Appendix C.2's continuity table (`:1400-1418`) then
disposes of Graft, `Σ(F)`, multi-parent lineage, structural constructions, semigroup/monoid, basis
adequacy, state equivalence, the four governance locations and the information quotient — and
**never disposes of the family root.**

> **Adopted form.** `A_0` is recorded as **the disposition Appendix C.2 omitted**, restored in a
> changed sense — v6.1's `R_F` was *declared per family and identity-bearing*; `A_0` is the anchor
> from which a domain is *generated*. The sense-change is stated, not glossed. This is a stronger
> provenance than a coinage and does not misstate the succession record.

### P-2 · The determinacy premise is the steward's own prior ruling, not ToD.

"Every geometrically available Case-S projection from the family root" is a determinate set **only**
under `ruling_2026_09_15_universe_constitution.md` §§2–3 (*"The anchor `{store}` is therefore proved,
not claimed"*; totality, single-valuedness, covering and disjointness are *"CONSEQUENCES of the
universe constitution, not separately authored anchor claims"*). Under v7.1 alone it is **not**
determinate: §2.1.1 admits *any* governed partition as an anchor, and §2.1.3 says *"The constituent
description need not be a uniquely discoverable factorization."*

> **Adopted form.** The rule cites `ruling_2026_09_15` §§2–3 as its geometric premise. It does not
> cite ToD for determinacy.

### P-3 · Four of the rule's five symbols are absent from ToD.

⟨measured⟩ zero occurrences in v7.1 of `A_0`, `Case-S`, `Spent`, `spend`, `β`, `γ`, `family root`,
`accumulate`, `monotonic`. Exactly two of the rule's symbols occur in v7.1 — `\mathcal A_F` and
`\Gamma_F(B\to A)` — **both in the single sentence at §4.1**. `Spent(q)` is undefined *corpus-wide*:
it occurs only as an undischarged side condition inside `RED1` (MA v1.0 §3; rev1 §3.2), never with a
definition, and the corpus is split three ways on its type.

> **Adopted form.** Every such symbol is introduced by this plan as a **native definition with a
> named source**, never as a citation of ToD. `Spent` is defined natively and only natively, as
> `Anchor.projection_forgets` (`native.py:360-375`).

### What the checks affirmed without qualification

* **Ruling 2 (the split)** — supported by v7.1's own summaries. App. B.2 and §14 both list *"admitted
  anchors"* and *"movements"* as **two coordinate items**; §4.1 gives two notations at two governance
  locations (§1.5 Family identity vs. Edge validity). §4's preamble — *"They are not separate
  ontological kinds or **necessarily** separate records"* — permits the split rather than forbidding
  it. The code has already made it three times independently (`serving.py:414-424`,
  `serving.py:427-442`, `native_law.py:166-179`).
* **Ruling 5 (separate jurisdictions)** — the best-supported ruling of the nine, and a *restatement*
  rather than an extension. §1.5: *"Checking that a particular realization has the coverage required
  by that unchanged definition is an **edge- or evidence-validity question**."* §5.2:
  *"**Self-sufficiency is a composition claim, not a coverage claim.**"* Plus §4.2 (participation),
  §5.5 and §9.1 (evidence). It should cite these and drop any implication of novelty.
* **Ruling 6 (no allow-list, no native MovementLicence)** — §4.1 rules out a registry in terms
  (*"not a proposed registry or new object"*), and `movement.py`'s own docstring rules itself out
  (*"a RUNTIME PROJECTION — not a governed serialization"*).
* **β's negative polarity** — Platform Profile v0.3 §7.2 (`:381,:384`): *"`β(κ)` — axes capability
  `κ` may not spend"*, *"**`β` is negative: an empty prohibition set means unrestricted with respect
  to that condition.**"*
* **β_F as a constituent set is exact in Case S** — `⪰` is `⊇` (`Anchor.refines`), `Spent` is set
  difference (`Anchor.projection_forgets`), and `Spent` is **compositional** there
  (`A_0\A_2 = (A_0\A_1) ∪ (A_1\A_2)`), so the ruling's root-relative one-shot test and the algebra's
  step-relative chained test agree by construction — **within Case S**.
* **`fcf-2` is a prerequisite, not an obstacle.** It replaced the anchor *spelling* in the identity
  digest with `_anchor = sorted(anchor.constituents)` (`native.py:110-116`), so synonyms collapse
  (`berthing_at` and `berth_day` are ONE anchor) and `Spent` is computed against a structure. Under
  `fcf-1` two spellings were two identities and `Spent` would have been ambiguous.
* **β_F does not change family identity.** `NON_IDENTITY_KEYS` (`native.py:106-108`) excludes
  `domain`/`movement` from the fingerprint — *"capability, not identity"*. A steward may amend β_F
  without re-minting the family. This is a favourable architectural fact and the plan relies on it.

### Two reported conflicts that do not survive, recorded so they do not re-enter

* **§6.3 "incomparable anchors" is not a counterexample to ruling 3.** It was offered as refuting the
  `⟸` direction: Revenue at Week and Revenue at Month in one family with neither refining the other.
  But §2.1.2 answers it in its own words — *"Calendar Week and Calendar Month are familiar examples:
  **Day can refine each**"*. A principal downset of `A_0` is a partial order, not a chain; it
  contains mutually incomparable elements freely, and both Week and Month sit under a Day-grained
  `A_0`. What §6.3 denies is a **path between** them — *"it does not manufacture a path between
  incomparable locations"* — which is `Γ_F(B→A)`. **§6.3 is independent textual support for
  rulings 2 and 5**, not a conflict with ruling 3.
* **The per-member objection misses the native simplification.** That a family-indexed β cannot say
  *"sum may not cross calendar but last may"* is true of legacy and false natively: `sum` and `last`
  are **separate families**, each citing one continuation law (v3 fixture:
  `continuation: {"law": "SUM", …}`). The distinction is not lost; it moves. **But see SG-3** — the
  split handles the *declaration* side and does not handle MAP1's union.

---

## 2 · The four jurisdictions, and where each is decided today

Ruling 5's separation, mapped onto shipping code. This table is the plan's spine; every seam in §4
belongs to exactly one row.

| jurisdiction | question | decided today at | after |
|---|---|---|---|
| **universe geometry** | does the projection exist? | `native_request.resolve` `:176-201` — `universe.anchor()`, then `constitutive.refines(asked)` | unchanged |
| **family domain `𝒜_F`** | may `F` stand at the resulting location? | **nowhere** — `native_law.py:182-190` stops here | the new derived predicate |
| **edge contract `Γ_F(B→A)`** | is this particular movement lawful under its further premises? | **nowhere**; γ has no home at all | still nowhere — held by ruling 7 |
| **realization** | can this implementation execute it now? | `WantOfState` / `serving.py` | unchanged |

⟨measured⟩ **the first three are one wire reason today.** A geometrically non-existent target
(`native_request.py:196-201`), an unlicensed movement (`native_law.py:169-180`) and unreadable
positive content (`native_law.py:185-190`) are **all `WantOfLaw` → `want_of_law`**, distinguished only
by detail substrings that three tests pin. This is why ruling 9 defers the refusal vocabulary until
the conditions are mechanically distinguishable: **they are not distinguishable yet.**

---

## 3 · The domain rule, stated natively

### 3.1 The two-level polarity — and why ruling 4 does not collide with §4.1

v7.1 §4.1 is closed-by-default in terms: *"A geometrically available projection and a computable
state operation do not by themselves put \(A\) in \(\mathcal A_F\). **The family's definition must
license the quantity being claimed there.**"* Ruling 4 says the default *within Case-S projection
geometry* is admission. Read as "silence admits", these contradict. Read as ruling 4 is written —
*"**The family declaration** records the exceptions"* — they do not, because **the declaration is the
licensing act §4.1 requires**, and its content is then negative.

Recon Finding 5 reached the same two-level shape from the legacy end. The existing trichotomy already
carries it, with **no new standing values**:

| family law state | `𝒜_F` | existing standing |
|---|---|---|
| no C3 law declared | `{A_0}` — the root alone, by ruling 1 | `UNESTABLISHED` |
| declares it does not move | `{A_0}`, positively | `EXPLICIT_NONE` |
| declares `β_F = ∅` | every Case-S projection from `A_0` | `ESTABLISHED` |
| declares `β_F ≠ ∅` | derived, less the projections that spend into `β_F` | `ESTABLISHED` |

> **Rows 2 and 3 must never collapse.** They are exactly the rows `C3 == ESTABLISHED` cannot
> distinguish today (`resolve.py:386`, the disjunction), which is ruling 2 arriving at the same seam
> from the theory side. **A DECLARED-empty `β_F` is not an ABSENT `β_F`** — and this is also what
> keeps the rule clear of v7.1 Appendix C.4, which withdrew *"universal projection-fiber locality of
> formation as a family-admission test"*. With `β_F` absent the rule admits nothing off-root; the
> withdrawn claim admitted on geometry alone.

### 3.2 The predicate

```
𝒜_F  =  {A_0}                                                   when C3 is UNESTABLISHED or EXPLICIT_NONE
𝒜_F  =  { A : A_0.refines(A) ∧ A_0.projection_forgets(A) ∩ β_F = ∅ }    when C3 is ESTABLISHED
```

**Ruling 1 becomes a theorem inside an established law, and an axiom only outside one.** `⊇` is
reflexive, so `A_0.refines(A_0)` holds; `projection_forgets(A_0) = ∅`, and `∅ ∩ β_F = ∅` for every
`β_F`. So `A_0 ∈ 𝒜_F` is *derived* in rows 3 and 4 and *declared* in rows 1 and 2. The currently
shipping assumption — the bare early return `if not moving: return` (`native_law.py:164-165`), pinned
by `test_native_c4_answerability.py:113-117` — is thereby **strengthened from an assumption into a
consequence** wherever a law exists. That is the single cleanest result in this plan and it should be
captured as a test.

---

## 4 · Exact seams — every field and line that changes

### 4.1 The declaration surface — a new family-body key

| file | symbol | line | change |
|---|---|---|---|
| `columna-core/.../governed/publication.py` | `_FAMILY_KEYS` | `:192-196` | add the β_F key (13 → 14) |
| `columna-core/.../governed/native.py` | `FAMILY_BODY_KEYS` | `:97-100` | **must change identically** |
| `columna-core/.../governed/native.py` | `NON_IDENTITY_KEYS` | `:106-108` | add it — β_F is capability, not identity |
| `columna-core/.../governed/publication.py` | `parse_family_declaration` | `:238-284`, slot at `:276-277` | the first **real reader** for a C3 slot; `continuation` (`:275`, `LawCitation.from_dict`) is the model, not `lambda r: r` |
| `columna-core/.../governed/publication.py` | `Family` dataclass | `:220-222` | new field beside `domain` / `movement` |

⚠️ `test_native_c4_answerability.py:68-73` asserts `FAMILY_BODY_KEYS == _FAMILY_KEYS`. Both must move
together or the suite fails. `_strict` (`publication.py:106-119`) is consume-or-refuse at key
granularity, so a stray key refuses rather than being ignored — the failure is loud, which is right.

### 4.2 The split — C3 becomes two standings

| file | symbol | line | change |
|---|---|---|---|
| `columna-core/.../governed/resolve.py` | `C3_DOMAIN_MOVEMENT` | `:51` | retained as the compatibility slot (ruling 2 permits it *temporarily*) |
| | `RESPONSIBILITIES` | `:59-60` | gains the second responsibility |
| | `IDENTITY_BEARING` | `:64-70` | **both halves stay out** — `:66-68` already explains why (§4.1 keeps domain out of identity). Consequence preserved: a C3 change is not a §3.9 succession |
| | the C3 block | `:378-397` | **the disjunction at `:386` is the defect.** Splits into two independent standings |
| | the `EXPLICIT_NONE` branch | `:381-385` | a **second latent conflation**: an `ExplicitNone` *domain* currently yields the note *"no movement is licensed for this family"*. Found during this plan; not previously recorded |

⚠️ **The comment above the block states the opposite of the code below it.** `resolve.py:379-380`:
*"Two POSITIVE declarations are required for admission (§4.1): the anchor must be in the declared
domain **AND** the movement licensed."* The code at `:386` is a **disjunction** — `fam.domain is not
None **or** fam.movement is not None`. The comment states ruling 2's conclusion and the code has
never implemented it. Found while verifying this plan; it is the clearest single piece of evidence
that the split is a repair rather than a redesign.

**Note what does not exist.** There is **no** inheritance/derivation rule propagating C3 from parents
through `formation.operands`. C3 is computed *purely locally*. The only responsibility that recurses
is C6 (`resolve.py:233`). So ruling 4's accumulation is **net-new structure** built on C6's shape —
and it must be satisfiable through `_ParentLookup.family()` alone, which
`test_native_c4_answerability.py:97-103` pins to exactly that one capability.

### 4.3 The decision

| file | symbol | line | change |
|---|---|---|---|
| `columna-platform/.../native_law.py` | `assert_answerable` | `:146-190` | `:182-190` — the "no governed reading of it" branch — **is the branch the rule replaces**. See **SG-1**: its signature and body are pinned by an AST test |
| | `MOVEMENT_STANDING_UNDECIDED` | `:133-144` | narrows from the whole fact to `Γ_F(B→A)` + γ. Does not retire |
| | `MissingGovernedFact` | `:115-127` | survives — it still has γ and the edge contract to carry |
| `columna-platform/.../native_request.py` | `resolve` | `:176-201` | `constitutive.refines(asked)` at `:183` **is already the `A_0 ⪰ A` conjunct**. `:153` `universe.denote(family.anchor_token)` is already `A_0`. No change to geometry |

### 4.4 What the rule needs that already ships

* `Anchor` — `native.py:326-390`, `(universe, constituents: frozenset[str])`
* `Anchor.refines` — `:353-358`, *"Refinement is set containment (⊇), **computed**"* → `A_0 ⪰ A`
* `Anchor.projection_forgets` — `:360-375`, *"Projection is set difference"* → `Spent(A_0→A)`
* `Universe.denote` — `:500-507` → `A_0`, with `fcf-2`'s synonym collapse
* pinned already: `projection_forgets(...) == frozenset({"day"})` at `test_native_c3_identity.py:252`

**Nothing new is computed.** One fact is declared; one intersection is taken.

### 4.5 The legacy witness, for reconciliation only

`planner.py:2210-2211` **already ships this rule** over lineages:

```python
crossed = self._traversed_lineages(t.frm, t.to)     # accumulated over the path, :2046-2071
bad = sorted(crossed & t.law)                        # Spent ∩ β ≠ ∅
```

Not migrated, not translated, not touched. Recorded because it is independent evidence that the shape
is right, and because `_traversed_lineages` is the only accumulated-spend-over-a-path code in the tree.

Per ruling 6, **no native `MovementLicence` is created.** `movement.py:67-91`'s fields are disposed of
as the reconnaissance explained them: `source_anchor`/`target_anchor` (`:71,:74`) are obsolete as
authority; `source_components`/`target_components` (`:73,:76`) come from geometry; `law` (`:78`)
belongs to C8; `authority` (`:82`) is dead (*"hand-authored (Proof B)"*); `standing` (`:80`, `POSITIVE`)
is the part whose native successor is this rule.

### 4.6 Scope fact that bounds the blast radius

⟨measured⟩ **`assert_answerable` and `native_request.resolve` have zero production callers.** Every
call site is a test. The native C1–C4 spine is not imported by `columna_platform/__init__.py`,
`serving.py`, `provider.py` or `columna-server`. **Nothing on the wire moves when this lands.** The
v2 serving path (`serving.py:388-442`) is untouched and keeps its own reading.

---

## 5 · Stop-gates

**Blocking — implementation does not start until ruled.**

> ### SG-1 · A shipped test forbids the rule's own inputs, and the convergence claim cannot survive it
>
> `test_native_c4_answerability.py:221-237` (`test_the_decision_rule_names_no_anchor_at_all`) asserts
> `list(sig.parameters) == ["view", "moving"]`, that no identifier inside `assert_answerable`
> contains `"anchor"`, and that its names are `isdisjoint({"universe","denote","constituents",
> "refines","declared"})`. `:240-251` (`test_the_SAME_rule_decides_a_LEGACY_law_view_unchanged`) then
> proves the rule decides a v2 `LawView` unchanged.
>
> Those two tests *are* C4's result: the rule was written so an anchor model could not enter it, and
> it still said everything it needed to. **The Case-S rule needs a constituent set inside the
> decision.** Passing `spent` in changes the signature (forbidden by the first assertion); computing
> it inside trips the identifier ban; and a v2 `LawView` has no native `Anchor`, so the legacy
> convergence test cannot pass either way.
>
> **The anchor-model-free convergence claim and the Case-S domain rule cannot both hold in one
> function.** Options, not chosen here: (a) the domain predicate lives *outside* `assert_answerable`
> and the caller passes a decided verdict, preserving both tests; (b) `assert_answerable` becomes
> native-only and the convergence claim is retired with a recorded reason; (c) the rule takes an
> abstract spend the caller computes, and the tests are re-pointed. **(a) is the only option that
> costs nothing already proved**, but it relocates the decision, which is a governed choice.

> ### SG-2 · The biconditional is false as written
>
> `RED1` has **two** premises, conjoined in one inference: `Spent(q) ∩ β(κ) = ∅` **and** `h ∈ γ(κ)`.
> Ruling 5 correctly holds γ out of `β_F` — and the checks confirm γ *is* separable (MA v1.0 `:123`:
> the `G_0` fragment uses the smaller contract `C=(X,A,β)`, β without γ; rev1 §3.2: *"Movement law
> and coverage permission are separate premises"*). **But a rule that discharges one premise and
> writes `⟺` over admission is false.** γ also determines the output support (`S' = S'_{q,h}`), so
> if `γ(κ) = ∅` nothing reduces whatever β says.
>
> **The `⟺` is sound for `𝒜_F` and unsound for admission** — which is exactly ruling 5's own
> distinction, and the fix is to say so in the notation: `A ∈ 𝒜_F ⟺ …` is fine; `admits(F, A_0→A)`
> is not `𝒜_F` membership. Separating γ is correct **and leaves it homeless** (it is not C3's, and
> the platform profile records it has *"no complete Core counterpart"*). Ruling 7 says to characterize
> rather than fill — so γ is characterized here and given no home.

> ### SG-3 · Family-indexing loses β's totality, and MAP1 needs it — NEW, not in the falsification record
>
> Platform Profile §7.2 (`:381,:384`): `β(κ)` is *"axes capability `κ` may not spend"* and
> **"Both are total over the relevant capability vocabulary."** That totality is what makes MAP1's
> `β'(κ) = ⋃ᵢ βᵢ(κ)` well-typed: every operand's β answers "may κ spend axis a?" **for every κ,
> including capabilities not yet applied to that operand.** A family-indexed `β_F` is a *set*. It
> answers only for `F`'s own declared law. **The re-index collapses a total function to one fiber.**
>
> Witness, over `U = {store, day}`, both at `A = {store, day}`:
> `revenue.sum` (β = ∅) and `on_hand.max` (β = ∅ — `afternoon.cml:53` bars `sum`, not `max`).
> Form `F' = map(revenue.sum, on_hand.max)`, lawful under MAP1 (shared `U`, shared `A`). Reduce `F'`
> by `sum` to `{store}`, spending `day`:
>
> * **family-indexed:** `β_{F'} = ∅ ∪ ∅ = ∅`; `{day} ∩ ∅ = ∅` → **admitted**
> * **capability-indexed:** `β'(sum) = ∅ ∪ {calendar} = {calendar}`; `{day} ⊆ calendar` → **refused**
>
> They disagree, and **the algebra's answer is the safe one** — the derived value still carries stock
> level data and summing it across time still double-counts. The family-indexed form
> **under-prohibits**. Splitting one legacy measure into several native families handles the
> *declaration* side; it does not handle **MAP1's union across families whose continuation laws
> differ**, because after the split no object is total over the capability vocabulary.
>
> The falsification record's *"natively that difference dissolves"* (§6) is the claim this falsifies.
> **Not recorded anywhere in the corpus.** Ruling 7 applies: *"If implementing that exposes another
> missing governed fact, stop there and characterize it."* **This is that fact.** Options, not chosen:
> scope `β_F` to families that never MAP1-compose across differing laws; or retain a capability fiber.

**Non-blocking — must be answered inside the unit, not before it.**

> **SG-4 · "Accumulate where derivations compose" needs a scope.** ⟨measured⟩ **RED1 passes β through
> byte-identical**: its conclusion is `(v',(Y_κ,U,A',E',S',β,γ))`. β accumulates **only at MAP1
> formation**. If "where derivations compose" means chained *reduction*, there is nothing to
> accumulate and the requirement bites on nothing. Read as *multi-operand formation* it is real and
> it is `β'(κ) = ⋃ᵢ βᵢ(κ)`. **This is why the seam is `formation.operands` / C6's recursion (§4.2)
> and not the reduction path** — two independent checks converged on it. Note also: there is **no
> accumulation theorem** in the algebra. There is a clause inside a rule. It has no lemma number and
> no proof. Do not cite "the algebra proves β accumulates".
>
> **SG-5 · The refusal has no lawful home yet, and ruling 9 already holds it.** No reason code in the
> tree has the requested OUTPUT anchor's admission as its subject; `REASON_OUTCOME`
> (`disclosure.py:227`, 32 entries) is closed and fail-closed (`:575-595`). Frame-QL 1.0 §12: *"No new
> reason code, outcome, standing enum, wire field, or approval workflow is created by this
> document."* Do **not** reuse `anchor_spent` — it is an *aperture*-spending reason (`engine.py:528`),
> not a projection-spending one. Ruling 9's condition is met only after SG-1 and SG-2 are ruled.
>
> **SG-6 · Fingerprint helpers must move with the key.** `_refingerprint_fcf2` /
> `_refingerprint_family` (`test_native_c4_answerability.py:264-278`) will silently produce stale
> fingerprints if a new body key is added without updating `FCF2_IDENTITY_KEYS` handling. Silent, not
> loud — the one seam here that fails quietly.
>
> **SG-7 · There is no v7.2 addendum material to add to.** A sweep of `attachments/`, `columna/docs`,
> `columna/specs`, `columna/editorial`, `columna/research`, all zip manifests and both bundles finds
> none; "v7.2" occurs only in forward-looking prose. **Ruling 1 requires creating the file**, which is
> a larger act than amending one and needs the steward's call on form. v7.1's own home for this class
> of note is **Appendix C.4, "Development clarifications and downstream scope"** — the section that
> already records the withdrawal. House style for a *term* is the v6.1 glossary form (bold term,
> period inside the bold, one paragraph), with v7.1's `\(…\)` math convention, not v6.1's `$…$`.
>
> **SG-8 · Lineage granularity is lost, silently.** `BLOCKED { calendar }` names a *chain*
> (`day→month→quarter`); a constituent set is all-or-nothing on `day`. The rule cannot express *"may
> climb `day→month` but not `month→quarter`"*. ⟨measured⟩ currently harmless — the probe shows
> `AT {store, month}`, `AT {store, quarter}` and `AT {store}` refuse identically — but that is a
> contingent fact about one fixture, not a theorem. This is the Case-G boundary ruling 3 already
> holds; recorded so the loss is deliberate.

---

## 6 · Implementation order, once the gates are cleared

Four steps, each independently revertible, no step beginning before its predecessor's tests are green.

1. **Split the standing.** `resolve.py:378-397` → two standings; re-point the eleven `standing` reads
   catalogued in §4.2/§4.3; fix the `ExplicitNone`-domain conflation at `:381-385`. **No new fact
   yet** — this step is pure disambiguation and should change no verdict anywhere.
2. **Add the declared fact.** The β_F key across `_FAMILY_KEYS` / `FAMILY_BODY_KEYS` /
   `NON_IDENTITY_KEYS`, a real reader on the `continuation` model, and the fingerprint helpers (SG-6).
   Still no decision consumes it.
3. **Derive `𝒜_F`.** The predicate of §3.2, sited per SG-1's ruling. `A_0 ∈ 𝒜_F` becomes a test of a
   *derived* result (§3.3) rather than an early return.
4. **Accumulate at formation.** `β_F ⊇ ⋃ᵢ β_operandᵢ` over `formation.operands`, on C6's recursion
   shape, through `_ParentLookup.family()` only. **Stop here** — and if SG-3 is ruled "retain a
   capability fiber", step 4 is where that lands and step 2's shape changes.

---

## 7 · Questions requiring a ruling before step 1

* **Q-P1 · SG-1.** Which of (a)/(b)/(c)? The anchor-model-free convergence claim is a proved C4
  result and one of the three options retires it.
* **Q-P2 · SG-2.** Confirm the `⟺` is scoped to `𝒜_F` membership and not to admission, and confirm γ
  is characterized-and-homeless rather than assigned.
* **Q-P3 · SG-3.** Scope `β_F` away from cross-law MAP1 composition, or retain a capability fiber?
  This is the one place the rulings may need to change rather than be implemented.
* **Q-P4 · ruling 1 / P-1.** Record `A_0` as the restored v6.1 term (the C.2 disposition gap), or
  as new despite v6.1 §5.2?
* **Q-P5 · SG-7.** Create the v7.2 addendum as a companion supplement, an Appendix C.4-style
  clarification, or a term register? And is `A_0` identity-bearing as v6.1's `R_F` was — the plan
  currently says **no**, following `NON_IDENTITY_KEYS`, and that is a governed choice.

---

## 8 · Deliberately not in this unit

Per rulings 3, 6, 7, 8 and 9: Case G; relationship expansion; coverage permission γ beyond
characterization; non-commutative continuation; the general `Γ_F(B→A)` calculus; any allow-list of
anchors or edges; any native `MovementLicence`; the output-anchor reason code; the ordered-family
`LAST` tie defect (rowed separately, ruling 8); DG-4's legacy polarity defect (the native side is
answered by §3.1's two-level reading; the legacy declaration surface is untouched); the Manual's
geometric anchor-compatibility rule; the holistic-reducer exemption (`planner.py:2135-2142`);
`domain` being write-only in v2; OF-59, F-3, P1-33, P1-34, OF-48, OF-58.

Two further things found while writing this plan and **not acted on**: the `ExplicitNone`-domain
conflation (§4.2), and MA v2.0 **rev1's regression against draft4** — rev1 deleted draft4 §10's
constitutive/staging anchor distinction and its §10.1 six-premise anchor-elimination judgment
(*"anchor elimination is a theorem with premises, not a global property of SUM, MEAN, LAST, or any
operator name"*). The document of record is **weaker on exactly the premises that constrain this
rule** than the draft it superseded. Recorded for the steward; not a C3 question.

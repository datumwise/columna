# C3 · family domain and edge validity — bounded implementation plan

**Revision v0.3**, revised against the steward's rulings R1–R12 of 2026-09-22. The first
revision's three blocking stop-gates are **closed by ruling**; one of them (SG-3) was closed by
correcting the design rather than by defending it. The plan is smaller than v0.1.

**Standing.** A PLAN, checked and not executed. No engine code is changed by this document.

**Checked against**: ToD v7.1, the v7.2 development addendum (created alongside this revision —
`tod_v7_2_development_addendum_v0_1.md`), native v3, `fcf-2`, C1–C4, and the legacy witnesses.
Secondary: Measure Algebra v1.0 / v2.0 rev1, Frame-QL Platform Profile v0.3, Frame-QL 1.0,
`ruling_2026_09_15_universe_constitution.md`, ToD v6.1.

---

## 0 · The headline answer

> **Yes — the primitive-family path can be implemented cleanly with constructed-family domain
> propagation held, and holding it costs nothing measurable today.**

⟨measured⟩ three facts establish this, all mechanical:

1. **The boundary is a parsed, fail-closed, total discriminator.** `Formation.kind` is `PRIMITIVE` or
   `CONSTRUCTION` (`publication.py:126-190`), validated by `_strict` at parse time. A `PRIMITIVE`
   formation **cannot even carry operands** — `_strict(raw, frozenset({"kind",
   "contribution_structure"}))` (`:176` vs `:163`) refuses the key. A `CONSTRUCTION` **must** name at
   least one (`:178-182`). `_formation` refuses any third kind (`:188-190`). This is not a convention
   the plan would introduce; it already ships and already fails closed.
2. **The shipped native fixture is entirely primitive.** Both families of
   `fixtures_v3/native-v3-publication.json` carry
   `{"contribution_structure": "coincident", "kind": "primitive"}`. **The native path has zero
   constructed families**, so the primitive unit is complete and fully testable on the artifact the
   native spine actually reads.
3. **No multi-operand construction exists anywhere in the tree.** ⟨measured⟩ across every JSON
   fixture: 3 construction families (all in the v2 lighthouse artifact — `count`, `min`, `max`, each
   over the single parent `revenue`), **maximum operand count 1**. The only code path that builds a
   `Formation(CONSTRUCTION, …)` is the parser itself (`publication.py:186`).

Consequence for R3/R8: **SG-3's counterexample needs two operands under differing laws, and no such
object exists in any shipped artifact.** The held question is therefore held over an empty set on the
native path. It is not thereby answered — R8's question *"what establishes `P_F` for a constructed
family?"* arises at one operand too, and the three v2 constructions are real — but nothing the native
unit must serve depends on it.

---

## 1 · The rulings as adopted

### R1 · `A_0`, restored and re-roled

`A_0` is the **family root**: the governed analytical location from which the family's Case-S domain
is generated. Recorded with **both** its continuity and its change of role — a v6.1 term
(§5.2 *"Designated family root"*, `F@R_F`, glossary `:2522`, and identity-bearing as a component of
`Σ(F)` at `:1591-1599`) that v7.1 left undisposed, despite App. C.1 recording *"designated family
origins"* among the inheritance and App. C.2's continuity table covering nine other constructs. Not
attributed to v7.1; not claimed to be v6.1's `R_F` unchanged.

**`A_0 ∈ 𝒜_F` is a theorem under an established domain law** — `⊇` is reflexive so `A_0 ⪰ A_0`, and
the identity projection forgets nothing, so `∅ ∩ P_F = ∅` for every `P_F`. **It is not a theorem
without one**, and the no-domain-law case stays separately governed (§2.1, rows 1–2). The theorem may
not be used to turn absence of a domain law into general permission.

### R2 · The rule defines `𝒜_F` and nothing else

```
A ∈ 𝒜_F   ⟺   A_0 ⪰ A   ∧   Forgotten(A_0 → A) ∩ P_F = ∅          [Case S, established law]
```

This is the family's **analytical domain**. It is not a statement that a derivation or realization to
`A` is lawful. The four-layer question stands, and each layer keeps its own jurisdiction:

| layer | question | decided at |
|---|---|---|
| universe geometry | does `A` exist? | `native_request.resolve` `:176-201` |
| **family domain** | is `A ∈ 𝒜_F`? | **the new predicate** |
| edge contract `Γ_F(B→A)` | do the edge/evidence premises hold? | nowhere — held (R5, R8) |
| realization | can this implementation execute it? | `WantOfState` / `serving.py` |

Coverage `γ`, participation/support, commutation/order, evidence, and Case-G conditions are **outside
the domain predicate**. This closes **SG-2** without weakening the rule: the biconditional was false
over *admission* and is sound over *domain membership*, which is all it now claims.

### R3 · `P_F` is not Measure Algebra's `β(κ)` — SG-3 closed by correcting the design

The naming is withdrawn. The native fact is **the family's prohibited Case-S constituents**, written
`P_F` where a symbol is needed, and **no permanent public name is minted** for implementation
convenience.

| | question answered |
|---|---|
| `P_F` | which Case-S constituent distinctions may this family **not lose** while remaining within its own analytical domain? |
| `β(κ)` | which distinctions may **capability `κ`** not spend in this derivation contract? |

They coincide in simple cases and are **not the same governed object**. This dissolves the MAP1
counterexample rather than papering over it: the counterexample was a proof that a capability-total
`β` cannot be re-indexed onto families *and keep its guarantee*, and the correct response is not to
re-index it at all.

> **Withdrawn:** the instruction that `P_F` accumulate by importing `β'(κ) = ⋃ᵢ βᵢ(κ)`. That is a
> Measure Algebra rule about capability contracts. Whether a constructed family's domain prohibition
> follows from its operands is a **separate governed question**, not invented here. See **SG-A**.

### R4 · Two-level polarity

Silence is not permission. Establishing the family-domain law is the **positive** governed act;
within an established law, `P_F` is **negative** content restricting the geometry-generated domain.

| family law state | `𝒜_F` | standing |
|---|---|---|
| no domain law | `{A_0}` — by R1's separate governance, **not** by the theorem | `UNESTABLISHED` |
| declares it does not move | `{A_0}`, positively | `EXPLICIT_NONE` |
| established, `P_F = ∅` | every Case-S projection from `A_0` | `ESTABLISHED` |
| established, `P_F ≠ ∅` | derived, less the projections that forget into `P_F` | `ESTABLISHED` |

Compatible with §4.1: geometry alone does not admit the anchor; the **established family law** is what
licenses the domain, and once it exists its compact content need not enumerate every consequence.
Rows 2 and 3 must never collapse — they are precisely the rows `C3 == ESTABLISHED` cannot distinguish
today (`resolve.py:386`). This also keeps the rule clear of App. C.4, which withdrew *"universal
projection-fiber locality of formation as a family-admission test"*: with the law absent, nothing is
admitted off-root.

### R5 · The split stands, conceptually first

`𝒜_F` and `Γ_F(B→A)` are distinct governed responsibilities. The smallest compatibility-safe
*representation* is chosen later; today's combined storage slot does not dictate the theory. `γ` does
not belong in `P_F` and its eventual home remains open.

### R6 · SG-1 closed — the domain decision moves one layer above the anchor-free rule

Option (a). The valuable C4 proof is **preserved and narrowed**, not defended:

* **Preserved:** `Law(F)` resolution and the law-level sufficiency/standing rule remain
  **anchor-model-free**. `test_law_resolution_asks_a_publication_for_exactly_one_thing`
  (`:97-103`) and `test_resolution_consults_no_anchor_model` (`:85-94`) keep passing unchanged.
* **Withdrawn:** the stronger conclusion that *answerability as a whole* can remain anchor-free.
  Domain membership is inherently a relation between `F` and a **resolved** location `A`.

So `Anchor`, `constituents` and `projection_forgets` are **not** forced into
`assert_answerable(view, *, moving)`. The domain adjudication sits at the layer that already holds the
resolved geometry (`native_request`), which already computes `A_0` (`:153`) and `A_0 ⪰ A` (`:183`). No
native anchor is translated into a `MovementLicence` to regain convergence.

### R7 · `Forgotten`, not `Spent`

```
Forgotten(A_0 → A) = A_0 \ A
```

already computed as `Anchor.projection_forgets` (`native.py:360-375`). No new `Spent` abstraction is
introduced to resemble `RED1`. `Forgotten` may be *related* to the inherited `Spent(q)` in explanatory
material; they are **not declared identical beyond the Case-S scope proved**. This deliberately leaves
room for Case G, where forgotten constituents will not be a sufficient general representation.

### R8 · Constructed-family propagation is an explicit stop-gate

For a **primitive** family with an explicitly established Case-S domain law, the rule is bounded and
complete. For a **constructed** family: if its own declaration establishes `P_F`, use that
declaration. If the design requires **deriving** it from operands — **stop**. No recursion rule is
created merely because `formation.operands` makes one technically possible, and union is not inferred
merely because union is conservative in the capability calculus.

### R9 · The ordered-family defect is **P1-36**, graded **VX**

Rowed separately from C3 and from P1-34, with an executed probe. No repair in this unit. *(Filed
separately; not part of this plan document.)*

### R10 · A v7.2 **development** addendum, created — not a publication

`docs/architecture/tod_v7_2_development_addendum_v0_1.md`. Records theoretical clarifications
discovered after v7.1 for adjudication in the next ToD edition. **No DOI; does not alter v7.1**; the
deposited v7.1 text is not edited. Its first entry covers this subject as a whole, and carries **no
Columna implementation names** — those live in the crosswalk, not the theory statement.

### R11 · The family root is identity-bearing — the resolved location, not the spelling

Changing `A_0` changes family identity **unless** the change is only of reference or representation of
the same universe-relative structural anchor. A token or synonym change does not change `A_0`; a
structural change does.

⟨measured⟩ **`fcf-2` already implements exactly this** — `constitutive_anchor` is in `NOMINAL_KEYS`
and leaves the identity payload, replaced by `_anchor = sorted(anchor.constituents)`
(`native.py:110-116`). No change is required for a bound family. **`fcf-1` does not**, and §10 of the
contract records the measured witness and puts the question to the steward.

### R12 · The family domain is governed law and is not identity-bearing

`P_F` — and therefore `𝒜_F` — is **not** identity-bearing; a domain-law change does not by itself mint
a successor. The existing exclusion of `domain`/`movement` from `IDENTITY_BEARING`
(`resolve.py:64-70`) and from `NON_IDENTITY_KEYS`'s complement (`native.py:101-107`) is therefore
**the intended theory for the domain half**, not an accidental implementation choice.

**But the default runs the other way, and that matters.** `native.py:101-104`: *"Everything else is IN
**by derivation** — a body key added later is inside the fingerprint by default, and taking one out is
a decision someone has to write down."* So `P_F` is inside the fingerprint **unless explicitly
excluded**, and omitting the exclusion would make every domain revision a succession. R12 is that
decision; the contract §5 is where it is written down.

⟨measured⟩ **R12's auditability requirement already has a carrier.** The native publication root
carries `ref: {manifold_id, version}` and `published: {at, by}`, so two publications may establish
different domains for one immutable `family_id` and be distinguished by that. **No new versioning
machinery is needed or in scope.**

**Guard.** R12 rules only the identity standing of the family-domain law presently represented by
`P_F`. The eventual contents of `Γ_F` retain their own standing and none may be inferred from it.

---

## 2 · Exact seams

### 2.1 Declaration surface — one new family-body key

| file | symbol | line | change |
|---|---|---|---|
| `governed/publication.py` | `_FAMILY_KEYS` | `:192-196` | add the `P_F` key (13 → 14) |
| `governed/native.py` | `FAMILY_BODY_KEYS` | `:97-100` | **must change identically** — pinned by `test_native_c4_answerability.py:68-73` |
| `governed/native.py` | `NON_IDENTITY_KEYS` | `:106-108` | add it — capability, not identity, so **amending `P_F` does not re-mint the family** |
| `governed/publication.py` | `parse_family_declaration` | `:238-284`, slot `:276-277` | the first **real reader** for a C3 slot. Model it on `continuation` (`:275`, `LawCitation.from_dict`), not on `lambda r: r` |
| `governed/publication.py` | `Family` | `:220-222` | new field |

⚠️ `_refingerprint_fcf2` / `_refingerprint_family` (`test_native_c4_answerability.py:264-278`) must
move with the key or they silently produce stale fingerprints. **The one seam here that fails
quietly** (SG-B).

### 2.2 The split

| symbol | line | change |
|---|---|---|
| `C3_DOMAIN_MOVEMENT` | `resolve.py:51` | retained as the compatibility slot (R5 permits it temporarily) |
| `IDENTITY_BEARING` | `:64-70` | **both halves stay out** — `:66-68` already explains why. A C3 change remains not a §3.9 succession |
| the C3 block | `:378-397` | the disjunction at `:386` is the defect; splits into two standings |
| the `EXPLICIT_NONE` branch | `:381-385` | **second latent conflation**: an `ExplicitNone` *domain* yields the note *"no movement is licensed for this family"* |

⚠️ **The comment contradicts the code one line below it.** `resolve.py:379-380`: *"Two POSITIVE
declarations are required for admission (§4.1): the anchor must be in the declared domain **AND** the
movement licensed."* `:386` implements `fam.domain is not None **or** fam.movement is not None`. The
comment has stated R5's conclusion all along; the code has never implemented it. **This is the
clearest single piece of evidence that the split is a repair, not a redesign.**

Eleven `standing` reads must be re-pointed to whichever half they mean — catalogued at
`compile_v2.py:360` (dead, gated by `K0_EMITS_MOVEMENT`), `serving.py:417,418,431,433,438`,
`native_law.py:168,171`, `exhibit.py:41,107`, and the pins at `test_governed_v2.py:216-217`,
`test_producer_artifact_v2.py:118`, `test_native_c4_answerability.py:116,186,260`,
`test_proof_a_negative_controls.py:159`.

### 2.3 The decision, sited per R6

| symbol | line | change |
|---|---|---|
| `assert_answerable` | `native_law.py:146-190` | **stays anchor-free.** `:182-190` — the "no governed reading of it" branch — narrows to `Γ_F`/γ; it no longer has to decide domain |
| `MOVEMENT_STANDING_UNDECIDED` | `:133-144` | narrows from the whole fact to `Γ_F(B→A)` + γ. Does not retire |
| `MissingGovernedFact` | `:115-127` | survives — it still carries γ, the edge contract, and now SG-A |
| the domain predicate | *new, at the resolved-geometry layer* | consumes `A_0` (`native_request.py:153`), `A_0 ⪰ A` (`:183`), `Forgotten` (`native.py:360-375`) and the established `P_F` |

**Already shipping, unchanged:** `Anchor` (`native.py:326-390`), `Anchor.refines` (`:353-358`, *"set
containment (⊇), computed"*), `Anchor.projection_forgets` (`:360-375`, *"set difference"*),
`Universe.denote` (`:500-507`, with `fcf-2`'s synonym collapse). **Nothing new is computed. One fact
is declared; one intersection is taken.**

### 2.4 Not touched

Per R3, R5, R6, R8 and the earlier rulings: no `β` import; no MAP1 propagation; no general movement
calculus; no `MovementLicence` migration (`movement.py` — its own docstring disposes of it: *"a
RUNTIME PROJECTION — not a governed serialization"*); no Frame-QL syntax change; no reason-code
decision; native geometry preserved as geometry. `planner.py:2210-2211` — the legacy
`crossed & t.law` that already ships this shape over lineages — is **recorded as independent evidence
and not migrated**.

⟨measured⟩ **`assert_answerable` and `native_request.resolve` have zero production callers.** Nothing
on the wire moves when this lands; the v2 serving path keeps its own reading.

---

## 3 · The next bounded unit — specified, and stopping here

> **The full contract is `c3_primitive_family_domain_contract_v0_1.md`.** It states the scope gate,
> the one declared fact and its three states, what is derived and never stored, where the decision
> lives, identity and succession under R11/R12, what must refuse, ten conformance obligations, the
> shipped invariants that must not change, and what is out of contract. Summary only below.

> ### C5 · The primitive-family Case-S domain
>
> **Scope.** Primitive families only, gated on `fam.formation.kind == PRIMITIVE`.
>
> 1. **Split the standing** (`resolve.py:378-397`) and fix the `ExplicitNone`-domain conflation.
>    Pure disambiguation — **this step must change no verdict anywhere**, and that is its test.
> 2. **Add the declared fact** — the `P_F` key across the three key-sets, a real reader, and the
>    fingerprint helpers (SG-B). Nothing consumes it yet.
> 3. **Derive `𝒜_F`** at the resolved-geometry layer (R6), for primitive families. `A_0 ∈ 𝒜_F`
>    becomes a test of a **derived** result, not an early return.
> 4. **Refuse, loudly and by name, for constructed families** whose `P_F` is not established by their
>    own declaration — carrying SG-A as a `MissingGovernedFact`, in the C4 idiom that already exists.
>
> **Stop before step 4's refusal becomes a derivation.** The unit ends with the constructed case
> characterized, not filled.

---

## 4 · Stop-gates remaining

**SG-A · Constructed-family domain propagation (R8).** What establishes `P_F` for a constructed
family? Its own declaration, or something derived from its operands? ⟨measured⟩ **no multi-operand
construction exists in any shipped artifact** (max operand count 1; 3 constructions, all v2), and the
native fixture has **no constructions at all** — so the primitive unit is unblocked. A governed
question, not an implementation detail; not invented here.

**SG-B · Fingerprint helpers must move with the new key.** Silent failure mode. §2.1.

**SG-C · The refusal has no lawful home yet.** No reason code in the tree has the requested OUTPUT
anchor's admission as its subject; `REASON_OUTCOME` (`disclosure.py:227`) is closed and fail-closed
(`:575-595`). Frame-QL 1.0 §12: *"No new reason code, outcome, standing enum, wire field, or approval
workflow is created by this document."* Do **not** reuse `anchor_spent` — an *aperture*-spending
reason (`engine.py:528`), not a projection-spending one. Held by the earlier ruling 9 until the four
layers of §1/R2 are mechanically distinguishable; after C5 they will be.

**SG-D · Lineage granularity, deliberately lost.** `BLOCKED { calendar }` names a chain
(`day→month→quarter`); a Case-S constituent set is all-or-nothing on `day`. ⟨measured⟩ currently
harmless — `AT {store, month}`, `AT {store, quarter}` and `AT {store}` refuse identically — but that
is contingent on one fixture. This is the Case-G boundary R7 deliberately leaves open.

---

## 5 · Recorded, not acted on

* **The `ExplicitNone`-domain conflation** (§2.2), found while writing v0.1.
* **The `resolve.py:379-380` comment/code contradiction** (§2.2), found while verifying v0.1.
* **§6.3 is not a counterexample to the domain rule**, contrary to a reading raised during the
  checks. §2.1.2 says *"Calendar Week and Calendar Month are familiar examples: **Day can refine
  each**"*; a principal downset is a partial order, not a chain, so incomparable anchors sit in it
  freely. What §6.3 denies is a **path between** them — which is `Γ_F`. §6.3 is **support for R2 and
  R5**, not a conflict.
* **MA v2.0 rev1 regresses against draft4.** Rev1 deleted draft4 §10's constitutive/staging anchor
  distinction and its §10.1 six-premise anchor-elimination judgment (*"anchor elimination is a theorem
  with premises, not a global property of SUM, MEAN, LAST, or any operator name"*), and dropped
  *"Participation belongs inside the information law whenever an admitted continuation can observe
  it."* The document of record is **weaker on exactly the premises that constrain this area** than the
  draft it superseded. Not a C3 question; recorded for the steward.
* **DG-4** — the native side is answered by §1/R4's two-level polarity; the legacy declaration surface
  is untouched and DG-4 stays open on its own terms.
* **P1-36** — rowed separately per R9. **OF-59, F-3, P1-33, P1-34, OF-48, OF-58** — untouched.

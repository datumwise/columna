# Family Law, Capability, and Reusable Sufficient State
## A bounded formal reconciliation, with Core/Platform annotations

**Version:** 0.1 · **Date:** 1 September 2026
**Type:** reconciliation note. **Reconnaissance only.**
**Mandate:** no implementation, no representation choice, no syntax, no registry design, no MME/Cache(r) schema, no `witness` refactor, no Frame-QL extension, no Measure Algebra revision.
**Governing corpus:** ToD v6.1 · **Measure Algebra v1.0 (DOI 10.5281/zenodo.22219691)** · Contract Calculus · Design Record v0.3 · Finding 1 · Finding 2 v0.2 · the Cache(r) design capture · the topology record · current Columna.

Hypothesis under test:

> **Family law determines analytical admissibility. A capability/operator declares what typed state it
> requires and how it uses that state. Reusable sufficient state is the material meeting point between
> them.**

**Annotation key** — every finding carries one or more: **[SHARED]** semantics both Core and Platform
must obey · **[CORE]** realization within one governed execution domain · **[CARRIER]** physical
representation/compute · **[PLATFORM]** backend-independent standing and cross-domain reuse ·
**[MIXED]** conflates layers and must be split before it can be placed.

---

## 0. Verdict

**The hypothesis is correct, and the corpus supports two of its three clauses outright. The third —
`Law(F)` determining admissibility — is the one the corpus does not currently express, and the reason
is structural rather than accidental.**

Four results:

1. **`Law(F) ⊢ admits(κ)` does not exist in the corpus, and cannot presently be written in it.** The
   Contract Calculus has **no measure-family object at all** — the word "family" occurs six times and
   never in the ToD sense. Admissibility in CC is a **stored, capability-indexed permission map carried
   by the contract** (`β`, `γ`), and CC rules on the derivation question explicitly:
   > **"$G_1$ records the permission but does not infer it."** (CC:1862) **[SHARED]**
2. **`Req(κ)` is exactly one obligation: `X = X_κ`.** A capability cannot currently state a requirement
   about *state* at all. That, not the finalizer count, is the gap. **[SHARED]**
3. **Option 3 — factoring state production from finalization — is not a new formal move.** The proved
   fragment already runs **two finalizers over one carried state**, and already declares one of them
   *outside* the capability. What is missing is that the factoring is never lifted to a declarable
   object. **[SHARED]**
4. **A new relation is required, and it is small — because the obligation it must discharge is already
   published.** MA §5.2 already requires a materialization to *"make clear what information it retains
   and therefore which derivations remain possible."* Nothing formalizes that sentence. **The smallest
   relation is the formal statement of an obligation the corpus has already imposed.** **[SHARED]**

And the finding that most changes the framing of the old question:

> **The `FAMILY {…}` operator-name list is not a rival mechanism to `β`. It is `β`'s key set,
> materialized as a declaration.** The real question was never "list on the family or list on the
> operator." It is **whether membership in that key set is enumerated or derived** — and Columna already
> derives the *content* of `β` per operator × lineage while enumerating its *keys*. **[MIXED]**

---

## 1. What the corpus establishes

### 1.1 Admissibility today is stored permission, not derived law **[SHARED]**

Every premise of every certification rule in CC is a fact about (i) a subderivation, (ii) the registry,
(iii) anchor/relation geometry, (iv) a **type identity**, or (v) a **stored capability-indexed
permission map inside the contract**. RED1's five premises:

$$\Gamma\vdash_1 P\Downarrow(v,(X,U,A,E,S,\beta,\gamma))\quad X=X_\kappa\quad q:A\to A'\quad \mathrm{Spent}(q)\cap\beta(\kappa)=\varnothing\quad h\in\gamma(\kappa)$$

- $\beta:\mathsf{AggCap}\to\mathcal P(\mathsf{Axis})$ — axes $\kappa$ may not spend (CC:710-723)
- $\gamma:\mathsf{AggCap}\to\mathcal P(\mathsf{Cov})$ — coverage modes admitted for $\kappa$ (CC:1852-1862)

Both are **fields of the contract**, and well-formedness requires them **total over registered
capabilities** (CC:1992-1993) — permission is stored exhaustively, per contract, per capability. That
totality requirement is the structural fact that forecloses derivation.

> **Consequence for §3's question.** The corpus's admissibility mechanism is *richer* than an
> operator-name allowlist — it carries axis sets and coverage modes rather than yes/no — but it is
> **the same shape**: a map keyed by capability identity, recorded rather than inferred.

**The one counter-instance**, and it is instructive: $D_{\mathrm{rep}}(\kappa)=\varnothing$ if
$\mathrm{DupInv}(\kappa)$, else $\mathrm{TgtAxes}(B)$ (CC:3462-3474) — a contract boundary **computed
from a declared predicate on the capability.** It runs capability → permission, the opposite direction
from `Law(F)` → permission, and $\mathrm{DupInv}(\kappa)$ is itself registry-recorded. **The corpus
therefore has exactly one worked example of deriving permission from declared law, and it is
capability-side.** **[SHARED]**

### 1.2 `Law(F)` contains a state law and one undefined slot **[SHARED]** **[MIXED]**

$\Sigma(F)=\operatorname{canon}(U_F,R_F,Parents(F),Establish(F),Law(F),Contracts_{id}(F))$ (ToD:1587-1599),
with *"$Law(F)$ the declared continuation law."* Its only itemization is the conformance appendix
(ToD:2374-2382):

```yaml
  family_law:
    state_schema: "..."
    combine_law: "..."
    finalizer: "..."
    ordering_semantics: "..."
    admitted_reductions: [...]
```

**Four of five fields are a state law** — precisely ToD §4.5's $(S,\eta,\oplus,e,\phi)$. The fifth,
`admitted_reductions`, **occurs exactly once in the entire corpus, and is never defined, typed, or
used.** It is not stated whether its elements are anchor maps, edges, or operator names.

> **So the allowlist slot exists in the published conformance surface and is empty — exactly like
> `state_schema`.** The corpus leaves open whether admitted continuation is enumerated or derived, and
> never resolves it. **This is the single most consequential ambiguity for the hypothesis.**

The narrative points hard toward derivation without arriving: *"The row is determined by the **declared
state law**; operator names alone are insufficient"* (ToD:1073); *"**What staging transformations does
the declared state law certify?**"* (ToD:1079); *"**The declared state law determines the admissible
composition**"* (MA:610). But what is derived in every case is the **staging permission for the family's
own reducer** — never *which other capability may be applied*.

### 1.3 `Req(κ) = {X = X_κ}` **[SHARED]**

A capability contains $(X_\kappa, Y_\kappa, S_\kappa, \oplus_\kappa, 0_\kappa, \eta_\kappa, \rho_\kappa)$
plus the optional registry predicate $\mathrm{DupInv}(\kappa)$ (CC:806-841, 2943-2958). **It demands
exactly one thing of what it is applied to: a type match.** Everything else the corpus calls permission
is contract-side.

> **A capability cannot currently say "I require a state satisfying law L."** That is the gap, and it is
> upstream of the multi-finalizer question. **[SHARED]**

### 1.4 One state, several finalizers: asserted, and separately performed **[SHARED]**

**Asserted** (MA:788-794): a retained moment state $N,\ \Sigma x,\ \Sigma xx^\top$ *"may support several
later finalizations under declared laws. Reuse of one state carrier does not make the resulting
analytical families identical."* The clause **"under declared laws" is never unpacked**, and
multi-finalizer state sharing does **not appear** among MA §9's open boundaries — so it is not even
booked as an open problem.

**Performed** (MA:158, CC:2650-2668): the aggregate capability contains $\rho_\kappa$; *"**the reduction
parameter $h$ is separate from that capability** and induces the coverage finalizer
$\mathrm{Covered}_h$."* A domain-and-state-disciplined schedule carries $(s,e,o)$ and applies **both**
finalizers only at the final stage.

> **So the proved fragment already factors a finalizer out of the capability and already runs two
> finalizers over one carried state.** Option 3 is not a new formal move.

**With the asymmetry that is the actual remaining gap:** $\rho_\kappa$ and $\mathrm{Covered}_h$ finalize
**different components** of the product $\widehat S_\kappa = S_\kappa\times D_h$. MA §8.1's several
finalizations over a moment state would consume **overlapping components of the same state**. That case
— same component, two consumers — has no instance and no rule.

### 1.5 Constraints any such move must satisfy **[SHARED]**

| constraint | source |
|---|---|
| Sufficiency is **relative to the continuations claimed** — *"sufficient for one later operation and insufficient for another"* | MA:669, 705, 709 |
| **Extension alone never suffices** — identical $K$ with different $\Gamma,E$ yields different certifiable claims | CS Prop 1 (324-378) |
| Permission is **per capability and total**; a second consumer inherits nothing | CC:1992-1993 |
| Identity is **ex ante**; *"agreement among computed outputs cannot create identity after the fact"* | MA:738; ToD:2337 |
| **Changing `Law(F)` establishes a family succession** — enriching it to license a capability mints a new family ID | ToD:1652-1660 |
| The planner *"applies declared law. **It does not infer missing law**"* | MA:832 |
| Capability **equality is explicitly refused as derivable** — *"The kernel does not decide extensional equality of arbitrary implementations. Declaring a new capability identity is a new semantic premise"* | CC:853-855 |

---

## 2. What Columna realizes

### 2.1 Admissibility is list membership, with three vetoes **[CORE]** **[MIXED]**

`FAMILY {sum count}` creates two `FamilyMember` records keyed by operator name. Query admission is
`member in meas.family`. Publish applies three **veto** gates in order: name ∈ REGISTRY → kind ==
REDUCER → `signature_ok(op, dtype)`.

> **Nothing is derived. The set is not closed under anything, implies no state, and entails no other
> member.**

**And the decisive evidence for §3's second question:** `sum` may accept `Float64`, the measure may be
`Float64`, `sum` may be a registered REDUCER — and it is **still refused** if undeclared
(`planner.py:1778-1783`). The planner *first* confirms the operator is in the registry, *then* refuses
on family membership: the refusal path is explicitly reserved for **"registered, typechecks, not
declared."**

> **Value-type compatibility is a necessary veto and never sufficient — in the corpus (one premise of
> five) and in the tree (the last gate of three).** *"Reducer declares allowed_types"* cannot establish
> analytical validity. **[SHARED]**

There are in fact **three** disjoint hardcoded allow-lists: `meas.family` (declared), `K0_REDUCERS =
{sum,count,min,max}` (compiler), `SERIES_REDUCERS = {sum,mean,min,max,count}` (inline). **[MIXED]**

### 2.2 The B-anchor is the one derived relation — and it is `β` **[CORE]** **[SHARED]**

`BLOCKED { lineage }` per family member is `β(κ)` restricted to lineages. Its **verdict is derived**,
deterministically, from declared structure: the traversed-lineage set comes from `find_path` (certified)
and `out_edges` (declared); the law set is the union of `blocked[reducer]` over the expression's
*governed ancestry*; the verdict is `crossed ∩ law ≠ ∅ → Refuse` (`planner.py:1388-1554`). ADR-036 D1:

> *"**Family generation creates a new analytical family. It does not create a new operator permission.**
> A successor family preserves the applicability law of its governed ancestry unless the family-changing
> operation positively establishes a different successor law."*

> **On this one axis Columna is ahead of the corpus**: CC records $\beta$ per contract; Columna *derives*
> the violation from declared structure per operator × lineage. But it is **negative-only** — silence is
> permission (DG-4) — and the positive polarity (`FERTILE`/License) is deliberately not enforced (DG-3).

### 2.3 The HLL factoring is real in vocabulary and absent in composition **[CORE]** **[CARRIER]**

Three registry entries — `hll_count` (deliver), `hll_merge` (combine), `hll_estimate` (project) — over
one parametric state type. **That is Option 3, in the operator registry.** But:

- the composition is **hardcoded** in `_resolve_sketch`, dispatched by *witness kind*, not by any
  declared relation;
- `hll_estimate` is **unreachable** on any other sketch — not declarable as a family member (`kind !=
  REDUCER`), not callable in an expression (no MAP-by-name surface), and `HLLSketch(12)` is unspellable
  in the `TYPE` grammar;
- **no producer-lawfulness check exists.** Provenance is guaranteed *structurally* — one function builds
  it, one function reads it — not by any check;
- the intermediate sketch is **never a first-class value**. `CacheEntry.sketches` is written once and
  **read nowhere**.

### 2.4 No materialized state has two consumers, anywhere **[CORE]**

Exhaustively: `WitnessStore` has one writer and one reader; `CacheEntry.sketches` has zero readers; the
result-cache key **contains `member`**, so two operators can never hit one entry by construction; each
in-memory series is built for and collapsed by one reducer within one call.

> **The shape "state produced once, finalized several ways" does not exist in this tree.** It is not
> under-used; it is unrepresentable.

### 2.5 `root_evaluator` — the mapping *is* the family **[MIXED]**

The private mapping's `root_evaluator` becomes the emitted `FAMILY {…}` verbatim; the governed member's
*name* is discarded (`compile.py:319-329`), and *"a Core family is keyed by operator and cannot hold
both"* — two governed members meaning different things but reducing with the same operator are
**structurally inexpressible**. The ledger's own ruling is the right one and this note adopts it:

> *"`root_evaluator` may be in the RIGHT file … The defect is then not a field in the wrong file. It is
> that **the governed layer has no `Law(F)` carrier at all**."*

---

## 3. Answers

### Q1 · Can MA v1.0 already express shared reusable state across multiple finalizers?

**Partly — it asserts the conclusion and performs the mechanism, but cannot state the relation.**

### Q2 · What exactly can it express, and what is missing?

**CAN express**

- one carrier serving several finalizations **as a negative identity result** — shared state does not
  merge identity (MA:788-794, 103, 40; $\Sigma(F)$ carries no state component)
- **factoring a finalizer out of the capability** — $\mathrm{Covered}_h$ from $h$, "separate from that
  capability" (MA:158)
- **two finalizers over one carried state** at one final stage (CC:2650-2668)
- **product state carriers** with componentwise combine, proved a monoid (Lemma G1.L2)
- **sufficiency relative to claimed continuations** (MA §5.2)

**CANNOT express**

- a capability that declares a **state requirement** — `Req(κ)` is a type match and nothing more
- a relation **"realization $R$ satisfies state requirement of $\kappa$"** — the closest object,
  $\equiv_F$ (ToD:1726-1760), has **reversed polarity**: one family and one finalizer over two states,
  where what is needed is one state against several requirements
- **two finalizers over the same state component**
- **capability equality or isomorphism** — explicitly refused (CC:853-855)
- **any family object in CC at all** — hence `Law(F) ⊢ admits(κ)` is not writable in the fragment where
  admissibility lives

### Q3 · Does the old allowed-reducer list have a principled replacement in the existing algebra?

**A principled *generalization*, yes. A *derivation*, no — and the corpus declines it explicitly.**

$\beta(\kappa)$ and $\gamma(\kappa)$ are the principled form: capability-indexed permission carried by
the contract, typed (axis sets, coverage modes) rather than boolean, and **required to be total**. That
is what `FAMILY {…}` should be understood as a degenerate encoding of.

But CC:1862 rules that $G_1$ *records* permission and *does not infer* it, and ToD's one enumeration slot
(`admitted_reductions`) is undefined. **So the corpus today replaces an operator-name list with a typed
permission map, not with a derivation from `Law(F)`.**

**The opposite legacy idea — `Reducer.allowed_types` — is refuted outright**, in both corpus and tree
(§2.1). Type compatibility constrains *representation*; it establishes **no** analytical validity.

### Q4 · Is a new formal relation actually required?

**Yes — one, and only for the reusable-state case.** Not because MA §8.1 contradicts the capability
tuple, but because:

- $\mathrm{Req}(\kappa)$ cannot mention state, so "this state satisfies that capability" is unsayable;
- Option 1 is **closed by ruling** — capability equality is not derivable, and declaring a second
  identity is a new semantic premise (CC:853-855). Identical $(S,\oplus,0,\eta)$ with different $\rho$
  are simply two unrelated registry entries;
- Option 2's polarity does not exist in the corpus;
- Option 3 is latent and instantiated, but never declarable.

### Q5 · What is the smallest obligation that relation must establish?

**The obligation is already published. What is missing is its formal statement.** MA §5.2 (MA:718):

> *"**A materialization is not required to preserve every future possibility. It must make clear what
> information it retains and therefore which derivations remain possible** subject to the governing
> contracts, identity, and evidence."* (MA:718)

Everything else a satisfaction relation would need is **already required elsewhere and inherited**:

| obligation | already supplied by |
|---|---|
| carrier law identity — the producing $(S,\oplus,0,\eta)$ is the one $\kappa$'s finalizer expects, **by declaration, not by extensional comparison** | CC:853-855 (which forbids the comparison) |
| $\kappa$ has its own contract permission — $\beta(\kappa)$, $\gamma(\kappa)$ | CC:1992-1993 totality |
| participation law and support contract in the key; **realized support not in the key** | Finding 1 §8 |
| the relation confers **no identity** on the result | MA:738; ToD:2337 |
| contracts and evidence, not extension, carry the claim | CS Prop 1 |

> **So the smallest new obligation is: a governed state must carry the set of continuations it claims to
> support, and the relation checks a requirement against that declared set.** One relation, one declared
> field. It is not new law — it is the formalization of MA:718. **[SHARED]**

**Two cautions on the shape it may take.** Enriching `Law(F)` to license a capability would **mint a new
family** (ToD:1652-1660), so the relation should not live inside `Law(F)`. And a *derived* $\gamma$ would
contradict CC:1862 unless the ruling is revisited deliberately.

---

## 4. Reusable state as material meeting point — the statement holds

> **Reusable sufficient state is the material meeting point between family law and capability, but it is
> not the authority that binds them.**

**Confirmed, and the corpus supplies the enforcement.** Because $\beta$ and $\gamma$ are total over
registered capabilities and carried by the **contract**, a second consumer of an existing state
**inherits no permission from the first**. The bytes cannot vote. Restated:

```text
law determines admissibility          [SHARED]
state enables reuse                   [CORE] locally, [PLATFORM] across domains
```

The Cache(r) already says exactly this, and said it first:

> *"a cached column at anchor A serves a request at anchor A′ **iff the algebra certifies the reduction
> A→A′** — same criterion that gates a fresh query. **A cache hit is a theorem application.**"*
> — RULED 2026-07-14

> **The MME/Cache(r) may say "I hold a governed state instance satisfying this capability's state
> requirement." It may never say "I hold compatible-looking bytes, therefore this capability is
> allowed."** The corpus's totality requirement on $\beta,\gamma$ is what makes the second sentence
> unsayable rather than merely discouraged. **[SHARED]** + **[CORE]** + **[PLATFORM]**

---

## 5. Semantic key vs material attestation

The decomposition is **consistent with existing architecture and already half-built.**

**Semantic key — [SHARED].** Joint input identities, input anchor, universe/population identity,
participation policy, state-law identity. Core and Platform must agree on what state *means*, so this
is above the execution-provider seam. Finding 1 §8 already fixes two of its members as a **soundness**
property: *"A reusable-state cache keyed on (family, anchor, filter) alone is **unsound** as soon as two
participation laws are admissible. The key must carry the participation law and the support contract."*

**Material attestation — [CORE] locally, [PLATFORM] across domains.** Data-state version, realized
support, freshness, provenance, producer evidence. Finding 1: *"It must **not** carry the realized
support set — that is attestation."*

**Current state of the split:** Columna's keys are `(measure, member, base_level)` and
`(measure, member, target, uni, where)` — **exactly the (family, anchor, filter) shape Finding 1 calls
unsound** — plus one data-version token doing all attestation work. Semantic key and material
attestation are **fused**, and `member` — a *finalizer's* name — is doing semantic-key duty. `P5-05`
already records the verdict: keys *"cannot be keyed by canonical governed identity."*

> **Is today's Cache(r) a genuine Platform seed? Yes — by its own criterion.** *"a cached column's
> identity is **its semantic identity** (family, input anchor, universe, attestation lineage),
> **checkable by the algebra**, so sharing is a theorem about column identity rather than a trust
> arrangement between teams."* That is the **identity-keyed** criterion the topology record assigns to
> Platform (`:146`). Written 2026-07-14, under a Core-side Metric Engine heading.
>
> **Caveat, recorded:** the capture predates the topology ruling, the record never cites it, and its
> layering is organizational/scale-based — a framing the record explicitly retired. **The seam is real
> and unreconciled.** **[MIXED]**

---

## 6. The concrete cases

| case | value | state | reuse question | jurisdiction |
|---|---|---|---|---|
| **`sum`** | `Float64` | `Float64` — state *is* value | degenerate: reuse is result-caching | **[CORE]** |
| **`mean`** | `Float64` | $(\Sigma x, N)$ | the pair could serve `sum`, `count`, `mean` — **unrepresentable today** | **[SHARED]** law, **[CORE]** realization |
| **exact distinct** | `Int64` | $\mathcal P_{\mathrm{fin}}(X)$ — **unbounded, fully compositional** | needs **no new law**; needs a representation | **[SHARED]** + **[CORE]** |
| **HLL** | `Int64` | `HLLSketch(p)` | *"cache the sketch, never the estimate"* — the Cache(r) admission law **is** the value/state distinction | **all four** (§7) |
| **moments** | matrix | $N,\ \Sigma x,\ \Sigma xx^\top$ | **the discriminating case** | **[SHARED]** |

**The moments case, answered.** Can one governed materialized state instance lawfully satisfy several
capabilities without transferring one consumer's analytical identity to the state?

- **Analytically, yes, and it is ruled**: MA:788-794 asserts it, and $\Sigma(F)$ structurally excludes a
  state component, so no consumer's identity can attach to the carrier.
- **Formally, not expressible**: nothing relates a state realization to several requirements.
- **Materially, foreclosed**: the witness key contains `member`, the *finalizer's* name — the state is
  **filed under the name of the number it will become**, and `publish_witnesses` takes
  `next(iter(meas.family))`, so a second member never gets a witness and never finds one.

> **That last point is the sharpest single realization finding: Columna's state store already commits
> the error MA §8.1 forbids — it keys sufficient state by one finalizer's identity.** Not by intent; by
> the key's shape.

**HLL's two material standings** (recomputable cache vs sole surviving root) remain undistinguished:
`P5-04` verified — the result cache adds `Caveat(FRESHNESS, "served from cache")` and **witness reuse
adds no marker at all**. **State type does not determine materialization standing.** **[MIXED]**

---

## 7. Concern-by-concern

| concept | jurisdiction | finding |
|---|---|---|
| **`FAMILY {…}`** | **[MIXED]** | Not a rival to $\beta$ — it is $\beta$'s **key set** materialized as a declaration. Membership is enumerated; $\beta$'s *content* is already derived per operator × lineage. The open question is whether the key set should also be derived. Splitting it into *declared law* and *derived admission* is the reconciliation. |
| **operator-keyed `family`** | **[MIXED]** | Keyed by operator name, so *"a Core family is keyed by operator and cannot hold both"* — two governed members with one reducer are inexpressible. This is a **carrier-of-law defect**, not a naming defect. |
| **`root_evaluator`** | **[CORE]** private mapping, correctly | The ledger's ruling stands: it may be in the right file as root **formation**. *"The defect is that the governed layer has no `Law(F)` carrier at all."* Confirmed by this reconciliation from the corpus side: `Law(F)` exists in ToD and has **no counterpart object anywhere in Columna.** |
| **`witness`** | **[MIXED]** — the designated test case | It mixes **[CORE]** dispatch (nine execution-routing reads), **[CARRIER]** representability (Finding 2 v0.2: it classifies what fits in a Polars column), and **[SHARED]** law *vocabulary* in two prose sites. **Do not force it into one bucket.** The split v0.3 §2.2 already proposes — `sufficient_state` (law) vs `decomposition_built` (build) — is the same split this reconciliation reaches independently. |
| **operator registry** | **[SHARED]** vocabulary, **[CORE]** mechanics | Already correctly split: `projection.py` withholds mechanics from the planner. What the registry **cannot** express is a state requirement — `accepts`/`out_rule` type the value only. This is where `Req(κ)` would live. |
| **Cache(r) / MME** | **[CORE]** locally + **[PLATFORM]** seed | Core owns *"caches and materializations that remain **subordinate to governed identity and law**"* (`:103`); Platform owns ***identity-keyed*** materialization (`:146`). **The differentiating word is `identity-keyed`** — which is precisely the Cache(r)'s own stated criterion. Genuine seed; unreconciled with the record. |
| **shared semantic kernel** | **[SHARED]** | Must carry: family law; capability requirements including a **state** requirement; the semantic state requirement; admissibility; and the claimed-continuation set of §3-Q5. **None of these has a carrier in Columna today.** |
| **Core execution** | **[CORE]** | Must construct, combine, finalize, materialize and **locally reuse** state within one governed domain. §6's reductio holds and the record independently confirms it (`:103`, `:107-113`): Core's non-obligations are backend-independent identity and cross-domain composition — **not sufficient state.** |
| **Platform identity runtime** | **[PLATFORM]** | Backend-independent standing; cross-domain lawful reuse/composition/custody/reconciliation. **Not** reusable state as such. |

**Does the result preserve the target architecture?** Yes, with one gap and one caution.

```text
SHARED SEMANTICS   family law · capability requirements · semantic state requirement · admissibility
CORE               compile and realize those laws · create/combine/finalize state · local governed reuse
CARRIER            physically represent and compute state
PLATFORM           backend-independent standing · cross-domain lawful reuse/composition/custody
```

**The gap:** the SHARED layer has **no carrier in Columna** — `Law(F)` has no object, `Req(κ)` has no
state component, admissibility is a list. Everything currently sits in CORE or CARRIER.

**The caution — and it needs your ruling.** The mission's premise —

> *Core and Platform cannot have different answers about whether an operation is analytically
> admissible*

— is **not currently in the topology record.** `admissib*` occurs **zero times** in it. The record fixes
*meaning* invariance (*"Execution placement may change; governed identity, law, support, conditions, and
standing may not"*, 3×; *"Two physical runtimes are acceptable. Two meanings of a measure are not"*, 2×)
and the nearest statement is about **surfaces**, not domains: *"They should not need different analytical
meanings merely because Core or Platform realizes the request"* (`:299-301`). Whether admissibility falls
inside "law" at `:137` is **an inference the record does not authorize.**

> **This note treats the premise as governing and flags it as an extension requiring ratification.** If
> ratified it is exactly what places `Law(F) ↔ Req(κ)` above the execution-provider seam — and without
> it, that placement is asserted rather than derived.

---

## 8. Open, and not decided here

1. **The `admitted_reductions` slot** (ToD:2381) — enumerated or derived? Undefined in the corpus, and
   the hinge for the whole hypothesis.
2. **MA §8.1's "under declared laws"** — never unpacked, and not listed among MA §9's open boundaries.
3. **Same-component multi-finalization** — the corpus's two-finalizer instance consumes disjoint
   components; overlapping components have no instance and no rule.
4. **Whether $\gamma$ may ever be derived** — CC:1862 says $G_1$ records and does not infer. Deriving
   admissibility from `Law(F)` touches this ruling directly.
5. **Admissibility invariance across execution domains** — §7's caution.
6. **The Cache(r)/topology seam** — the capture predates the ruling and uses a retired framing.

**No representation, syntax, registry design, MME schema, or implementation is proposed. No Measure
Algebra revision is proposed: the reconciliation finds the current formalism cannot *state* the
reusable-state relation, but the obligation that relation must discharge is already published at
MA:718, so the smaller move is to formalize an existing obligation rather than to revise the algebra.**

# Family Law, Capability, and Reusable Sufficient State
## A bounded formal reconciliation, with Core/Platform and Frame-QL profile annotations

**Version:** 0.2 · **Date:** 1 September 2026 · *(v0.1 superseded — see §0.2)*
**Type:** reconciliation note. **Reconnaissance only.**
**Mandate:** no implementation, representation choice, syntax, registry design, MME/Cache(r) schema, `FAMILY`/`root_evaluator`/`witness` change, reusable-state implementation, type registry, Frame-QL syntax change, separate profile specs, or Measure Algebra revision.
**Governing corpus:** ToD v6.1 · **Measure Algebra v1.0 (DOI 10.5281/zenodo.22219691)** · Contract Calculus · Design Record v0.3 · Finding 1 · Finding 2 v0.2 · the Cache(r) design capture · the topology record · current Columna.

Hypothesis under test:

> **Family law supplies analytical authority. Capability supplies requirements. Reusable sufficient
> state is their material meeting point.**

**Annotation keys.** Jurisdiction: **[SHARED]** · **[CORE]** · **[CARRIER]** · **[PLATFORM]** ·
**[MIXED]**. Frame-QL: **{canonical}** language semantics · **{core-profile}** Core realization
capability · **{platform-profile}** additional Platform realization standing.

---

## 0.1 Ratifications recorded

Two rulings are adopted here as governing. Neither is derived by this note; both are recorded so
later work has a citable referent.

### R1 · Analytical admissibility is provider-invariant **[SHARED]** **{canonical}**

> **Given the same governed declarations and the same analytical request, Core and Platform must agree
> on analytical admissibility. They may differ in realization capability and therefore in whether the
> request can currently be served.**

The admissibility-level application of the standing doctrine *"physical realizations may differ;
governed meaning may not."* The separation it fixes:

```text
analytical admissibility   = shared semantic law          [SHARED] {canonical}
realization / serving      = provider capability + evidence [CORE]/{core-profile}
                                                            [PLATFORM]/{platform-profile}
```

Core may refuse because it cannot **realize**. Core may **not** declare analytically invalid what
Platform declares analytically valid under the same governed declarations.

**Status against the corpus: an extension, and a consistent one.** `admissib*` occurs **zero times**
in the topology record; the record fixes *meaning* invariance (*"Execution placement may change;
governed identity, law, support, conditions, and standing may not"*, 3×) and its nearest statement is
about surfaces, not domains (`:299-301`). R1 supplies what was previously an unauthorized inference.
**It conflicts with nothing in the proved corpus**, and it is what places any `Law(F) ↔ Req(κ)`
relation above the execution-provider seam.

### R2 · One language, two realization profiles **{canonical}**

> **Frame-QL** is the canonical language and semantic specification — governed measures, anchors,
> formation, analytical admissibility, participation, state requirements, result identity,
> clarification and refusal. **There must not be two meanings of Frame-QL.**
>
> **Frame-QL Core Profile** records what Columna Core can currently realize under canonical semantics.
> **Frame-QL Platform Profile** records Platform's additional realization capabilities — backend-
> independent state identity, cross-domain reuse and composition, Platform materialization and custody.
> It **does not define a second language**, and the name `Frame-QL-Platform` is not introduced.
>
> **A profile may extend realization capability. It may not change the meaning of a canonical Frame-QL
> expression.**

```text
                    Frame-QL
             canonical semantics
                     │
          ┌──────────┴──────────┐
Frame-QL Core Profile   Frame-QL Platform Profile
          │                     │
    Columna Core          Columna Platform
```

Three separable questions for any expression: **(1)** valid canonical Frame-QL? **(2)** supported by
the Core Profile? **(3)** supported by the Platform Profile?

**Consistency check.** MA:832 already separates *"Frame-QL is one request surface over the Measure
Algebra, not part of its formal core"*, and the topology record already treats requester surfaces as
consuming one governed serving contract. **R2 conflicts with nothing.** It also gives the existing
`unsupported` reason code a principled home: it is a **profile** statement, not a semantic one.

---

## 0.2 What v0.2 corrects in v0.1

**C1 — the `FAMILY {…}` ↔ β claim was wrong.** v0.1 said *"`FAMILY {…}` is β's key set, materialized as
a declaration."* That cannot be true: $\beta:\mathsf{AggCap}\to\mathcal P(\mathsf{Axis})$ is **total
over registered capabilities** (CC:1992), so its key set is *all* of them. §2.1 restates it correctly,
and the corrected finding is **stronger**, not weaker.

**C2 — "one relation, one field" is withdrawn as a canonization.** v0.1's Q5 read MA:718 as licensing a
declared *continuation set*. Re-read under challenge, the sentence's own structure does not support
that. §3-Q5 now presents both forms and declines to choose.

---

## 0.3 Verdict

**The hypothesis holds. The corpus supports two of its three clauses outright; the third — `Law(F)`
determining admissibility — is the one the corpus does not express, structurally rather than
accidentally.**

1. **`Law(F) ⊢ admits(κ)` cannot presently be written in the corpus.** The Contract Calculus has **no
   measure-family object at all** — "family" occurs six times, never in the ToD sense. Admissibility is
   a stored, capability-indexed permission map carried by the *contract*, and CC rules on derivation:
   > **"$G_1$ records the permission but does not infer it."** (CC:1862) **[SHARED]** **{canonical}**
2. **`Req(κ)` is exactly one obligation: `X = X_κ`.** A capability cannot state a requirement about
   **state**. That, not the finalizer count, is the gap. **[SHARED]** **{canonical}**
3. **Factoring finalization from the capability is not a new formal move** — the proved fragment already
   runs two finalizers over one carried state and declares one of them *outside* the capability. It is
   never lifted to a declarable object. **[SHARED]**
4. **A relation is required, and the obligation it discharges is already published (MA:718). Its form is
   an open fork.** §3-Q5.

---

## 1. What the corpus establishes

### 1.1 Admissibility is stored permission, and it is purely negative **[SHARED]** **{canonical}**

RED1's five premises: the subderivation; $X=X_\kappa$; $q:A\to A'$;
$\mathrm{Spent}(q)\cap\beta(\kappa)=\varnothing$; $h\in\gamma(\kappa)$.

- $\beta:\mathsf{AggCap}\to\mathcal P(\mathsf{Axis})$ (CC:710-723) — *"contains axes that $\kappa$ **may
  not** spend while the output automatically inherits the current contract."* **Negative-valued;
  $\beta(\kappa)=\varnothing$ is unrestricted.**
- $\gamma:\mathsf{AggCap}\to\mathcal P(\mathsf{Cov})$ (CC:1852-1862) — admitted coverage modes.
- Both **total over registered capabilities** (CC:1992-1993).

> **Decisive, and verified by search: there is no positive admission enumeration anywhere in the
> Contract Calculus.** Every registered capability is applicable to every contract *subject to the
> premises*. Admission is by **premise satisfaction**, never by membership in a list.

**The one counter-instance**, instructive because it runs the other way: $D_{\mathrm{rep}}(\kappa)$ is
*computed* from the declared predicate $\mathrm{DupInv}(\kappa)$ (CC:3462-3474) — capability → permission,
not `Law(F)` → permission, and $\mathrm{DupInv}$ is itself registry-recorded.

### 1.2 `Law(F)` holds a state law and one undefined slot **[SHARED]** **[MIXED]**

$\Sigma(F)=\operatorname{canon}(U_F,R_F,Parents(F),Establish(F),Law(F),Contracts_{id}(F))$ (ToD:1587-1599).
Its only itemization (ToD:2374-2382) has **four state-law fields** — `state_schema`, `combine_law`,
`finalizer`, `ordering_semantics` — plus `admitted_reductions: [...]`, which **occurs exactly once in
the entire corpus and is never defined, typed, or used.**

> **The enumeration slot exists in the published conformance surface and is empty — exactly like
> `state_schema`.** Whether admitted continuation is enumerated or derived is left open and never
> resolved. This remains the hinge.

### 1.3 `Req(κ) = {X = X_κ}` **[SHARED]** **{canonical}**

A capability contains $(X_\kappa,Y_\kappa,S_\kappa,\oplus_\kappa,0_\kappa,\eta_\kappa,\rho_\kappa)$ plus
optional $\mathrm{DupInv}(\kappa)$. It demands **exactly one thing**: a type match. A capability cannot
say *"I require a state satisfying law L."*

### 1.4 One state, several finalizers: asserted, and separately performed **[SHARED]**

**Asserted** (MA:788-794) — a moment state *"may support several later finalizations under declared
laws. Reuse of one state carrier does not make the resulting analytical families identical."* The clause
**"under declared laws" is never unpacked**, and multi-finalizer sharing does **not appear** among
MA §9's open boundaries.

**Performed** (MA:158; CC:2650-2668) — *"the reduction parameter $h$ is **separate from that capability**
and induces the coverage finalizer $\mathrm{Covered}_h$"*, with both finalizers applied to
$\widehat S_\kappa=S_\kappa\times D_h$ only at the final stage.

**The remaining asymmetry:** those two finalizers consume **disjoint components** of a product state. A
moment state's consumers would overlap on the same components. **That case has no instance and no rule.**

### 1.5 Constraints on any such move **[SHARED]**

Sufficiency is relative to claimed continuations (MA:669/705/709) · extension alone never suffices
(CS Prop 1) · permission is per-capability and total, so a second consumer inherits nothing
(CC:1992-1993) · identity is ex ante (MA:738; ToD:2337) · **changing `Law(F)` mints a family succession**
(ToD:1652-1660) · *"the planner applies declared law. It does not infer missing law"* (MA:832) ·
**capability equality is explicitly not derivable** (CC:853-855).

---

## 2. What Columna realizes

### 2.1 CORRECTED — two admission polarities, with opposite defaults **[CORE]** **{core-profile}** **[MIXED]**

The precise relationship, settled from the proved fragment and the tree:

> **Current `FAMILY {…}` is the explicit *positive* member/admission set. `BLOCKED {…}` realizes part of
> the capability-indexed *negative* law that $\beta$ represents more generally.**

And the sharper consequence:

| | Columna | Contract Calculus |
|---|---|---|
| **positive enumeration** | `FAMILY {sum count}`; query admission is `member in meas.family`; **closed by default** | **no counterpart — none exists** |
| **negative, capability-indexed** | `BLOCKED { lineage }` per member; **open by default** | $\beta(\kappa)$ — axes, total, open by default |
| **coverage permission** | — | $\gamma(\kappa)$ — **no counterpart in Columna** |

> **So Columna is *more* restrictive than the corpus on the positive side (an enumeration the fragment
> does not have) and *less* complete on the negative side ($\beta$ only over lineages, no $\gamma$ at
> all).**

**And the two polarities carry opposite defaults inside one system — which the tree already records.**
Querying `revenue.min` with `min ∉ family` refuses. But an *inline generated* `sum(x@day)` on a measure
declared `FAMILY { last }` **serves**, because there is no bar to cross. DG-4, verbatim:

> *"Measure families are OPEN by default (`BLOCKED` closes)… A stock declared `FAMILY { last }` — no
> `sum` member at all — still serves `sum(x@day)` across time, because there is no bar to cross. **The
> declared-bar case refuses; the under-declared case does not.**"*

**The useful conclusions, unchanged and now correctly grounded:**

- value-type compatibility is **necessary but not sufficient** — one premise of five in RED1, the last
  of three publish gates in the tree, and the planner's refusal path is explicitly reserved for
  *"registered, typechecks, not declared"*; **[SHARED]** **{canonical}**
- current Core **enumerates positive family membership**; **{core-profile}**
- it **derives part of operator applicability from declared law** — the B-anchor verdict is computed from
  declared structure per operator × lineage; **{core-profile}**
- the corpus **records permission and does not generally infer it**. **[SHARED]** **{canonical}**

> **This is not a claim that admission is now derivable.** One negative, lineage-scoped fragment is
> derived. Positive admission is enumerated, and the corpus neither enumerates nor derives it.

### 2.2 The B-anchor is the derived fragment **[CORE]** **{core-profile}**

Verdict computed from declared structure — traversed lineages from `find_path`/`out_edges`, law set as
the union of `blocked[reducer]` over governed ancestry, `crossed ∩ law ≠ ∅ → Refuse`. ADR-036 D1:
*"Family generation creates a new analytical family. It does not create a new operator permission."*
**Negative-only**; the positive polarity (`FERTILE`/License) is deliberately not enforced (DG-3).

### 2.3 The HLL factoring: real in vocabulary, absent in composition **[CORE]** **[CARRIER]**

Three registry entries over one parametric state type — Option 3, in the registry. But the composition
is hardcoded in `_resolve_sketch` and dispatched by *witness kind*; `hll_estimate` is unreachable on any
other sketch; **no producer-lawfulness check exists** (provenance is structural — one writer, one
reader); and `CacheEntry.sketches` is **written once and read nowhere**.

### 2.4 No materialized state has two consumers **[CORE]**

The result-cache key **contains `member`**, so two operators can never hit one entry by construction.
**The shape "state produced once, finalized several ways" is not under-used; it is unrepresentable.**

---

## 3. Answers

**Q1 · Can MA v1.0 express shared reusable state across multiple finalizers?** Partly — it asserts the
conclusion and performs the mechanism, but cannot state the relation.

**Q2 · What exactly?** *Can:* one carrier serving several finalizations **as a negative identity
result**; factoring a finalizer out of the capability; two finalizers over one carried state; product
carriers; sufficiency relative to claimed continuations. *Cannot:* a capability declaring a **state**
requirement; a "realization satisfies requirement" relation (the closest object, $\equiv_F$, has
**reversed polarity** — one family and one finalizer over two states); two finalizers over the **same**
component; capability equality; **any family object in CC at all.**

**Q3 · Principled replacement for the allowed-reducer list?** A principled *form* for the negative side —
$\beta$/$\gamma$, typed and total — and **no counterpart at all for the positive side**. A derivation
from `Law(F)`: **no**, and CC:1862 declines it. `Reducer.allowed_types` is refuted in both corpus and
tree.

**Q4 · Is a new relation required?** Yes, one, and only for the reusable-state case. Option 1 is **closed
by ruling** (CC:853-855). Option 2's polarity does not exist. Option 3 is latent and instantiated but
never declarable.

### Q5 · The smallest obligation — and the fork inside it

**The obligation is already published.** MA:718:

> *"A materialization is not required to preserve every future possibility. It must **make clear what
> information it retains** and **therefore** which derivations remain possible subject to the governing
> contracts, identity, and evidence."*

**v0.1 read this as licensing a declared continuation set. Re-reading it under challenge, the sentence's
own structure does not support that.** The primary obligation is on *what information it retains*; *which
derivations remain possible* is **consequential** — the word is "therefore". So MA:718 leans toward
describing what the state **embodies**, not enumerating who may consume it.

**The two candidate forms, neither chosen:**

```text
FORM A — enumerated consumers          FORM B — declared state semantics
R declares {mean, covariance}          R carries σ (governed state semantics)
                                       κ declares StateReq(κ)
κ admitted if κ ∈ R's list             κ admitted if σ satisfies StateReq(κ)
```

**The coupling test settles more than expected.** Take $R=(N,\Sigma x,\Sigma xx^\top)$ materialized
today, declared to support `{mean, covariance}`. A capability admitted **later** can use exactly the same
retained state.

- Under **Form A**, the continuation names are part of $R$'s declared identity, so the *state must be
  re-declared* — or re-produced — **merely because a finalizer did not exist when it was produced.**
  Nothing about the retained information changed. The state's identity becomes a function of the
  consumer population at production time, which is a **closed-world assumption about the future.**
- Under **Form B**, nothing about $R$ changes; the new capability's `StateReq` is checked against the
  same $\sigma$.

**Form A additionally sits badly with two standing rulings.** It makes a consumer's identity part of the
state's identity, which is the shape MA §8.1 forbids (*"reuse of one state carrier does not make the
resulting analytical families identical"*); and it is the error Columna's witness key **already commits**
(§4.3). Form B keeps `Law(F)`-side authority and state-side description separate.

> **Reported, not chosen.** Form B is better supported by MA:718's structure and by the coupling test.
> But the corpus does **not** force the choice: it never says what $\sigma$ would contain, and
> `admitted_reductions` (ToD:2381) is a live, undefined slot that would be Form A's home if ruled that
> way. **This is the genuinely open representation fork.** **[SHARED]** **{canonical}**

**Whichever form, the relation inherits every other obligation** and adds none: declared carrier-law
identity, not extensional comparison (CC:853-855) · $\kappa$'s own $\beta,\gamma$ (CC:1992-1993) ·
participation law and support contract in the key, realized support **not** in it (Finding 1 §8) · **no
identity conferred on the result** (MA:738; ToD:2337) · contracts and evidence, not extension (CS Prop 1).

**Two cautions on placement.** Enriching `Law(F)` to license a capability **mints a new family**
(ToD:1652-1660) — so the relation must not live inside `Law(F)`. And a *derived* $\gamma$ contradicts
CC:1862 unless that ruling is revisited deliberately.

---

## 4. The material meeting point

### 4.1 Two relations, and they do not substitute **[SHARED]**

```text
Law(F) + Req(κ)          →  analytical permission     [SHARED] {canonical}
governed state R + StateReq(κ)  →  material availability   [CORE] locally
                                                            [PLATFORM] across domains
```

> **State materialization creates availability, not permission.**

A state may establish that it is **materially sufficient** for an **already-lawful** continuation. It can
never manufacture the authority for that continuation. The two questions —

```text
Is κ analytically admitted?
Does materialized state R retain enough governed information to realize κ?
```

— are separate, and **the second can never make the first true.**

**The corpus supplies the enforcement, not merely the exhortation.** Because $\beta$ and $\gamma$ are
**total** over registered capabilities and carried by the **contract**, a second consumer of an existing
state **inherits no permission from the first**. The bytes cannot vote. The Cache(r) said it first:

> *"a cached column at anchor A serves a request at anchor A′ **iff the algebra certifies the reduction
> A→A′** — same criterion that gates a fresh query. **A cache hit is a theorem application.**"*
> — RULED 2026-07-14

> **The MME/Cache(r) may say "I hold a governed state instance satisfying this capability's state
> requirement." It may never say "I hold compatible-looking bytes, therefore this capability is
> allowed."**

### 4.2 Shared state does not merge identity **[SHARED]** **{canonical}**

```text
R ─ρ1→ F1      R ─ρ2→ F2      R ─ρ3→ F3        with   F1 ≠ F2 ≠ F3
```

Structurally grounded: $\Sigma(F)$ contains **no state-carrier component** (ToD:1587-1599), so no
consumer's identity can attach to the carrier.

### 4.3 The realization finding **[CORE]** **{core-profile}**

Columna's witness key is `(measure, member, base_level)` — `member` is the **finalizer's name**. **The
state is filed under the name of the number it will become**, and `publish_witnesses` takes
`next(iter(meas.family))`, so a second member never gets a witness and never finds one.

> **The store already commits the error MA §8.1 forbids: it keys sufficient state by one consumer's
> analytical identity.** Not by intent — by the key's shape. This is also the concrete reason Form A
> above should be examined carefully: it would make that shape a rule.

---

## 5. Semantic key vs material attestation **[SHARED]** / **[CORE]** / **[PLATFORM]**

**Semantic state key/requirement — [SHARED] {canonical}:** joint input identities · input anchor ·
universe/population identity · participation law · state-law identity. Core and Platform must agree on
what state **means**, so this sits above the execution-provider seam. Finding 1 §8 already fixes two
members as a **soundness** property: *"A reusable-state cache keyed on (family, anchor, filter) alone is
**unsound** as soon as two participation laws are admissible."*

**Material attestation — [CORE] locally, [PLATFORM] across domains:** data-state version · realized
support · freshness · provenance · producer/execution evidence. Finding 1: *"It must **not** carry the
realized support set — that is attestation."*

**Not necessarily two stored objects.** The conceptual distinction is what matters; nothing here proposes
a storage split.

**Current state:** Columna's keys are exactly the *(family, anchor, filter)* shape Finding 1 calls
unsound, plus one data-version token doing all attestation work. **Semantic key and material attestation
are fused**, and `member` — a *finalizer's* name — is doing semantic-key duty. `P5-05` already records
the verdict: keys *"cannot be keyed by canonical governed identity."*

**Core** needs enough semantic identity and local attestation to know whether retained state satisfies
the current request. **Platform** adds establishing that **independently produced** realizations have the
governed standing for lawful cross-domain substitution or composition. **This is consistent with the
existing architecture**, and it is why the Cache(r) is a genuine Platform seed by its own criterion —
*"a cached column's identity is **its semantic identity**… **checkable by the algebra**"* — which is the
**identity-keyed** criterion the record assigns to Platform (`:146`). The capture predates the topology
ruling and uses a scale framing the ruling retired; **the seam is real and unreconciled.** **[MIXED]**

---

## 6. The Core/Platform seam — reductio preserved

> **If reusable sufficient state were a Platform-only concept, then `mean`, HLL, exact distinct,
> moments, and the Cache(r) would become Platform features. That contradicts the settled requirement
> that Core remain a complete governed analytical system.**

Independently confirmed by the record: Core owns *"caches and materializations that remain **subordinate
to governed identity and law**"* (`:103`), and Core's stated non-obligations are backend-independent
identity and cross-domain composition (`:107-113`) — **not sufficient state**.

| layer | owns | Frame-QL |
|---|---|---|
| **Shared semantics** | family identity and `Law(F)` · capability requirements · **analytical admissibility (R1)** · semantic state requirement/meaning · result identity law | **{canonical}** |
| **Core** | construct · combine · finalize · materialize · **locally reuse** state within one governed execution domain | **{core-profile}** |
| **Compute / carrier** | physically represent or compute state **without defining its meaning** | — |
| **Platform** | backend-independent governed state identity · cross-domain substitution/composition · identity-keyed materialization and custody · cross-domain provenance, currency, reconciliation | **{platform-profile}** |

> **Do not move sufficient state into Platform merely because it is reusable. Do not move
> backend-independent state standing into Core merely because Core caches state locally.**

---

## 7. Concern-by-concern

| concept | jurisdiction | profile | finding |
|---|---|---|---|
| **`FAMILY {…}`** | **[CORE]** **[MIXED]** | {core-profile} | The explicit **positive** admission set — **no counterpart in the proved fragment**, which admits by premise satisfaction. Closed by default, while its sibling `BLOCKED` is open by default (DG-4). |
| **operator-keyed `family`** | **[MIXED]** | {core-profile} | *"a Core family is keyed by operator and cannot hold both"* — two governed members with one reducer are inexpressible. A **carrier-of-law defect**, not a naming defect. |
| **`root_evaluator`** | **[CORE]**, correctly | {core-profile} | The ledger's ruling stands: it may be in the right file as root **formation**. Confirmed from the corpus side — `Law(F)` exists in ToD and has **no counterpart object anywhere in Columna**. |
| **`witness`** | **[MIXED]** | — | Mixes **[CORE]** dispatch, **[CARRIER]** representability, and **[SHARED]** law vocabulary in two prose sites. Do not force it into one bucket; v0.3 §2.2's split is the same split reached here independently. |
| **operator registry** | **[SHARED]** vocabulary + **[CORE]** mechanics | {canonical} + {core-profile} | Correctly split already. What it **cannot** express is a state requirement — where `Req(κ)` would live. |
| **Cache(r) / MME** | **[CORE]** locally + **[PLATFORM]** seed | both profiles | Differentiating word is **`identity-keyed`** — precisely the Cache(r)'s own criterion. Genuine seed; unreconciled with the record. |
| **shared semantic kernel** | **[SHARED]** | {canonical} | Must carry family law · capability requirements incl. a **state** requirement · semantic state meaning · **admissibility (R1)** · result identity law. **None has a carrier in Columna today.** |
| **Core execution** | **[CORE]** | {core-profile} | §6's reductio holds and the record confirms it. |
| **Platform identity runtime** | **[PLATFORM]** | {platform-profile} | Backend-independent standing and cross-domain reuse — **not** reusable state as such. |

**The gap:** the SHARED layer has **no carrier in Columna**. `Law(F)` has no object, `Req(κ)` has no
state component, positive admission is a list. Everything currently sits in CORE or CARRIER.

---

## 8. Does anything above conflict with the proved corpus?

**No conflicts found.** Four statements are **extensions** rather than restatements, and are flagged:

| statement | status |
|---|---|
| **R1** — admissibility is provider-invariant | **Extension.** `admissib*` absent from the topology record; consistent with the meaning-invariance doctrine and with MA:832. Nothing contradicts it. |
| **R2** — one language, two realization profiles | **Extension.** Consistent with MA:832 (*"Frame-QL is one request surface… not part of its formal core"*). Gives `unsupported` a principled home as a **profile** statement. |
| *State materialization creates availability, not permission* | **Restatement, and enforced.** $\beta,\gamma$ totality on the contract makes the alternative unsayable. |
| *Shared state does not merge identity* | **Published** (MA:788-794), structurally grounded ($\Sigma(F)$ has no state component). |

**One tension inside the publication, unchanged from Finding 2 v0.2 and still unresolved:** the capability
tuple pairs **one** $\rho_\kappa$ with **one** $S_\kappa$ (MA:317), while §8.1 asserts a carrier *"may
support several later finalizations"* (MA:794). No mechanism is given and the two are not reconciled.
**A question about the publication, not about Columna.**

---

## 9. Open, and not decided here

1. **The Q5 representation fork** — Form A (enumerated consumers) vs Form B (declared state semantics
   σ + `StateReq(κ)`). Evidence favours B; the corpus does not force it; `admitted_reductions` remains
   Form A's undefined home.
2. **`admitted_reductions`** (ToD:2381) — enumerated or derived? The hinge.
3. **MA §8.1's "under declared laws"** — never unpacked, not listed among MA §9's open boundaries.
4. **Same-component multi-finalization** — no instance, no rule.
5. **Whether $\gamma$ may ever be derived** — CC:1862 stands until revisited.
6. **The two admission polarities with opposite defaults** — DG-4's ruled-open surface.
7. **The Cache(r)/topology seam.**

**No implementation, representation choice, syntax, registry, schema, or Measure Algebra revision is
proposed. The reconciliation finds that the current formalism cannot *state* the reusable-state relation,
while the obligation that relation must discharge is already published at MA:718 — so the smaller move
remains formalizing an existing obligation rather than revising the algebra, once the Q5 fork is ruled.**

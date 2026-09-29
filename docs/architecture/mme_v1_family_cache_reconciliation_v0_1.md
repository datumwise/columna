# MME v1 — Family-Cache Reconciliation and Design Report

**Status:** design/reconciliation report v0.1 — **no code changes**
**Date:** 29 September 2026
**Answers:** *CC / andFam — MME v1 Family-Cache Reconciliation* (29 Sep 2026), against
*Columna Platform MME v1 Architecture — Governed Family-Materialization Cache* (v0.1, 29 Sep 2026)
**Inspects:** `packages/columna-platform` at `main` after **#349** (columnar substrate + the support/domain
correction), **#351** (computed `ConstitutionWitness`), **#352** (local Arrow/Parquet persistence, open).

> MME v1 manages family materializations `F@A` only.
> Residency never creates analytical authority.

Everything below is measured against the code as it stands, not against the design notes. Five claims are
load-bearing and were **executed** rather than read; each is marked **[verified]** where it appears.

---

## 0 · The five things the current engine actually does, verified

| # | claim | verdict |
|---|---|---|
| 1 | Two materializations of the **same** `F@A` under one instance **cannot coexist** — the second silently overwrites the first | **[verified]** 1 key before, 1 key after |
| 2 | Family state and **expression outputs share one store**, distinguished only by `RetentionKey.sort` | **[verified]** `['expression', 'family']` |
| 3 | Use-once-and-discard already exists (`measure(..., retain=False)`) | **[verified]** store unchanged |
| 4 | An **independently established** non-root state is *assigned* `forgotten_since_root = root.forgets(anchor)` — a **fabricated provenance** | **[verified]** `@{day}` ⇒ `['order','store']` |
| 5 | Approximation disclosures ride on continued state and must survive any round trip | **[verified]** `['approximate']` |

Claim 1 is the single largest gap between the current engine and MME v1: **the architecture requires
`#17` and `#18` to be resident at once (§6) and the current key cannot represent that.** Coexistence is
reachable today only by varying `data_state`, which conflates *"a different evidence state"* with
*"another materialization of the same state"*.

Claim 4 is the second: independent establishment at a coarse anchor currently **claims to have forgotten**
the intervening constituents. For `revenue` (region = everywhere) it is harmless; for a restricted region it
makes independent establishment indistinguishable from derivation — which is the engine deciding a governed
fact about formation.

---

## 1 · Classification of current concepts

| concept | where | classification | note |
|---|---|---|---|
| `FamilyPoint (family_id, anchor)` | `kernel/sorts.py` | **family-materialization identity** | already exactly right; `manifold`/`universe` reach it via the instance and the index |
| `RetentionKey.sort` | `kernel/mme.py` | **expression-only machinery** (in part) | exists to keep `E@A` out of `F@A`'s way *inside one store*; unnecessary once expressions leave |
| `RetentionKey.identity/anchor` | ” | **family-materialization identity** | keep |
| `RetentionKey.instance` | ” | **cache-instance identity** (accidentally) | it is doing two jobs; see §9 |
| `RetentionKey.realization` | ” | **dependency/provenance** + cache-instance | *which* realization produced this material |
| `RetentionKey.constitution` | ” | **cache-instance identity** (accidentally) | its real job is admission, not identity |
| `AnalyticalInstance` (manifold, universe, participation, scope) | `kernel/standing.py` | **family-materialization identity** | the governed axes of the object; not cache state |
| `AnalyticalInstance.constitution_context` | ” | **lifecycle/cache policy** (placeholder) | nothing computes it; under one built Manifold the build *is* the context |
| `AnalyticalInstance.data_state` / `DataStateRef` | ” | **dependency/provenance** | the evidence state the material is *about* — not an instance id |
| `ConstitutionWitness` (+ law witness) | `kernel/witness.py` | **dependency/provenance** + admission credential | see §9 Q1 |
| `MME._constitutions` / `remember_constitution` | `kernel/mme.py` | **semantic-history database** | the MME keeping a version store of its own past |
| `Staleness` / `stale_states()` | ” | **lifecycle** (diagnostics) | becomes `SUPERSEDED` reporting under v1 |
| `PoolResolution` / `resolve_pool` | ” | **lifecycle/cache policy** | proto-`CandidateSelector`; selects on key equality where it should select on *currentness* |
| `Adequacy` / `adjudicate` (5 questions) | ” | **lawful continuation rights** | keep verbatim; this is the `AnalyticalAdjudicator` |
| `forgotten_since_root` | `kernel/value.py`, `columnar/mme.py` | **lawful continuation rights** | frozen entitlement evidence; see §9 Q4 |
| `ContinuationRegion` | `kernel/law.py` | **lawful continuation rights** | family law, unchanged |
| `ColumnarFamilyState` (+ `ColumnStanding`) | `columnar/mme.py`, `columnar/standing.py` | **family value** | the columnar family value, standing included |
| `ColumnarExpressionOutput` + its retention | ” | **expression-only — leaves MME v1** | §11 of the architecture |
| `evaluate` / `_establish` / basis compatibility | ” | **expression-only — leaves MME v1** | moves above MME; keeps using MME-supplied family columns |
| `CoordinateIndex` / `AnchorInstance` | `columnar/index.py` | **family value** (layout) | `identity` is also **persistence-only mechanics** on read |
| `GovernedBlock` | `columnar/block.py` | **persistence-only mechanics** / carriage | a container, never identity — already stated there |
| `RealizationStanding` / `ProviderProfile` | `kernel/realization.py` | **lifecycle** (interchangeability) | cache entitlement input, never analytical |
| P-2 sidecar: `identity`, `coordinate_index`, `standing`, `values` | `columnar/persistence.py` | **persistence-only mechanics** | required to rebuild the value |
| P-2 sidecar: `constitution`, `constitution_context`, `data_state`, `realization` | ” | **dependency/provenance** | the admission credentials |
| P-2 sidecar: `law`, `value_form`, `points`, `references`, `arrow_type` | ” | **persistence-only, and redundant** | derivable from the declaration given a matching witness |
| P-2 sidecar: `route` | ” | **semantic-history database** | narrative provenance; not cache state |
| P-2 sidecar: `disclosures` | ” | **family value** | a disclosure that can be dropped will be dropped — **correctness** |
| P-2 sidecar: `forgotten_since_root` | ” | **lawful continuation rights** | the one field whose loss is silent |
| P-2 sidecar: `constructor`, `basis_id` | ” | **expression-only — leaves MME v1** | |
| `witness-scheme-superseded` | ” | **lifecycle** (fail-closed admission) | keep as admission, not as staleness |

**Nothing is deleted by this report.**

---

## A · The smallest `FamilyMaterialization`

Four grouped records rather than a flat bag of fields, so that no consumer can read one job's field as
another's. **Ten slots.**

```
FamilyMaterialization
  ── cache-instance identity ────────────────────────────────────────────────
  materialization_id : MaterializationId        # opaque, minted at ADMISSION. Not a tuple.
  ── analytical identity ────────────────────────────────────────────────────
  point              : FamilyPoint              # family_id + anchor
  instance           : AnalyticalInstance       # manifold, universe, participation, scope
  ── the value ──────────────────────────────────────────────────────────────
  value              : FamilyValue              # columnar: values + ColumnStanding (+ index)
  disclosures        : tuple[Disclosure, ...]   # rides with the value, always
  ── continuation entitlement (FROZEN at admission) ─────────────────────────
  entitlement        : ContinuationEntitlement  # { forgotten_since_root, formed_at_root: bool }
  ── provenance ─────────────────────────────────────────────────────────────
  provenance         : Provenance               # { derived_from: tuple[MaterializationId],
                                                #   data_state: DataStateRef,
                                                #   realization: RealizationStanding,
                                                #   constitution: WitnessDigest }
  ── lifecycle, two independent axes ────────────────────────────────────────
  eligibility        : CURRENT | SUPERSEDED | HISTORICAL   (+ superseded_by: MaterializationId?)
  residency          : RESIDENT | EVICTABLE | PINNED | EXPIRED
  admitted_at        : AdmissionRecord          # intent + verdict, for explanation only
```

**Why `materialization_id` is explicit and opaque.** Cache-instance identity is *not* a function of the
analytical facts — `#17` and `#18` may agree on family, anchor, participation, scope, evidence state,
realization and constitution and still be two materializations (§6). A structural key cannot express that
and **the current one does not [verified claim 1]**. Minting an id at admission also makes dependency links
(`derived_from`) point at *entries*, which is what §8 requires: *"invalidation follows actual dependency, not
family name alone."*

**Why entitlement is its own record, frozen.** `forgotten_since_root` plus *"was this formed at `R_F`"* is
the whole input to the laundering guard. Freezing it at admission is what makes entitlement decidable
**without any ancestor being resident** — see §9 Q4, which is the most consequential answer in this report.

**Not in it, deliberately:** no `constructor`, no `basis_id`, no basis compatibility, no expression cells
(expression-only, §11); no cursor, no watermark, no schedule, no source reference, no refresh policy
(§7 — *"MME does not own scheduler, CDC, source cursors, or refresh orchestration"*); no `route` narrative.

---

## B · Dependency graph rules

Edges are **recorded at admission** and point from a materialization to the materialization(s) it was
established from. One rule governs everything:

> **R1 — Consequence follows a recorded edge, never a name.** Two materializations of the same family with
> no edge between them are, to this engine, unrelated.

### B.1 Same-family derivation

```
Revenue@Order #1  ──derived──▶  Revenue@Day #2  ──derived──▶  Revenue@Month #3
```

`#2` is superseded by `#2'`. Then, exactly:

| | |
|---|---|
| `#2` | `eligibility := SUPERSEDED`, `superseded_by := #2'`. Residency **unchanged** — it may stay resident. |
| `#3` | `eligibility := SUPERSEDED` **by inheritance**, `superseded_by := ∅`. Its value is a fold of `#2`'s value; it is not *wrong*, it is *no longer current*. |
| `#3`'s entitlement | **unchanged.** It still carries the forgotten set it was formed with, and would still be lawful-as-history. |
| `#3`'s residency | **unchanged.** Supersession is not eviction. |
| a request for current `Revenue@Month` | `NEED` — no current materialization refines `{month}`. It does **not** silently get `#3`. |
| re-deriving `#3'` from `#2'` | ordinary admission; `#3'` becomes CURRENT with `derived_from = (#2',)`. |

**Inheritance is transitive and is computed at supersession time, not lazily at read time.** Lazily walking
ancestors to decide currentness would re-introduce exactly the failure eviction creates: an evicted `#2`
would make `#3` *look* independently established. Marking descendants eagerly keeps the graph's conclusions
in the entries.

**No cascade beyond descendants.** Superseding `#2` says nothing about `#1`. Ancestors are untouched.

### B.2 Independent establishment

`Revenue@Month #9` is established directly from a governed realization; `derived_from = ()`.

> **Superseding `#2` does not affect `#9`.** Nothing propagates, because there is no edge.

This is the ruling's expected default and I recommend it without qualification — **with one residual risk
named, because it is real and MME cannot close it.** If `#2` was superseded because the underlying evidence
changed, `#9` may in fact be about the same superseded evidence. MME does not observe sources (§7), so it
cannot know. Two consequences:

1. The **offerer** must be able to supersede a *set* — `supersede: [ #2, #9 ]` — at admission. Transition
   intent is therefore not per-entry-plus-one-predecessor; it is *"this becomes current, and these cease to
   be"*. Cheap, and it is the only lawful route to an evidence-level supersession.
2. MME must never infer it. A `DataStateRef` *coincidence* is suggestive and is not an edge: two
   materializations sharing an evidence state are **not** thereby dependent, and MME will not propagate
   along that likeness. (It may, and should, **report** it: *"#9 shares the evidence state of a superseded
   entry"* is a diagnostic worth surfacing to whoever owns refresh.)

### B.3 Structured state (`HLLSketch`, un-finalized)

Identical rules — the sketch **is** the family value, so `#1 sketch@Order → #2 sketch@Day → #3 sketch@Month`
supersedes exactly as the additive case does. Three additions specific to structured state:

- **Sketch parameters are compatibility-bearing** (already read from the value, not trusted from a
  declaration). So `#2'` with a different `lg_k` is *not* a drop-in successor: descendants must be
  re-derived, never merged across parameters. Supersession must therefore carry the parameter facts, and a
  `NEED` for a sketch must name them.
- **Adequacy of the value survives as a separate question.** A finalized scalar cannot seed a structured
  continuation; the adjudicator's question 4 already refuses it and is unchanged.
- **The estimate is not in the graph at all.** `estimate(HLLSketch@A)` is an expression above MME (§11), so
  it has no node, no edge, and cannot be superseded — it is simply re-evaluated. That is the cleanest
  argument for the v1 narrowing: today the estimate *is* a node in the same store **[verified claim 2]**,
  and it can never be a lawful parent or child of anything.

### B.4 What the graph is not

Not a lineage log, not an audit trail, not a query plan. It holds exactly one relation — *established from* —
and one derived fact — *superseded by inheritance*. Everything else about how a value came to be is
provenance for explanation, not cache state.

---

## C · Currentness vs residency

Two **independent** axes, deliberately not one enum. The architecture's own example (`#17`/`#18`, §6) is
unstatable in a single lattice.

### Eligibility (governed)

| value | meaning | may SERVE a current ask | may SEED continuation | why |
|---|---|---|---|---|
| `CURRENT` | the standing answer for this `F@A` | ✅ | ✅ | |
| `SUPERSEDED` | a named successor exists, or an ancestor was superseded | ❌ | ❌ | *"must not answer a request for current Revenue@Day merely because its bytes remain present"* |
| `HISTORICAL` | admitted *as* history; never was current | ❌ | ❌ | an as-of ask is a different target, not a cache hit on this one |

Serving a superseded or historical entry is possible only by **naming the materialization id explicitly** —
an as-of/forensic request, which the Resolver must form as such. It is never a fallback.

### Residency (policy)

| value | meaning | affects serving | affects continuation | affects physical retention |
|---|---|---|---|---|
| `RESIDENT` | present and usable | — | — | held |
| `EVICTABLE` | present, may be dropped | — | — | droppable |
| `PINNED` | may not be dropped | — | — | held, protected |
| `EXPIRED` | policy says stop using it | ✅ *withholds* | ✅ *withholds* | pending drop |

### The three rules that make the split safe

- **P1 — Residency never creates authority.** No residency value can turn a `SUPERSEDED` entry into an
  answer. Policy may *restrict*; it may never *grant*.
- **P2 — `EXPIRED` ≠ `SUPERSEDED`.** Expiry is a policy withdrawal of a still-current value: the disposition
  becomes `NEED` (re-establish), not "the value is wrong". Supersession is a governed fact with a successor.
  Collapsing them would report a policy timer as a change in the world.
- **P3 — Eviction of a CURRENT entry is a `NEED`, not a `WANT_OF_STATE`.** Absence created by *us* must not
  be reported as absence of evidence in the world. (This is the same distinction #349 drew between
  nonparticipation and want of state, one layer up.)

---

## D · Incoming-state protocol

```
offer(point, value, instance, provenance_claim, entitlement_claim, intent) -> Admission
```

`intent ∈ { COEXIST, SUPERSEDE(targets…), AS_HISTORICAL }` — the caller *may* supply it; default `COEXIST`.

**Admission checks, in this order** (each is a refusal that names itself; all but 6 exist today):

| # | check | refusal code today |
|---|---|---|
| 1 | is `F` constituted in this Manifold? | `not-constituted` |
| 2 | does the offered constitution witness match this build's? | `constitution-superseded` / `witness-scheme-superseded` |
| 3 | do the governed axes agree with the declaration? *(material may not declare its own instance)* | `block-instance-mismatch`, `constitution-context-mismatch` |
| 4 | is the standing well-formed? *(no null masks; no support-without-a-value)* | `null-in-a-standing-mask`, `support-without-a-value` |
| 5 | is the layout coherent? *(index identity re-derived from the coordinate columns)* | `coordinate-index-identity-mismatch` |
| 6 | **is the entitlement claim admissible?** *(a non-root claim's forgotten set must be admitted by the region)* | **new** |
| 7 | is the intent coherent? *(`SUPERSEDE` targets exist and are this same `F@A`)* | **new** |

Check 6 is the fix for **[verified claim 4]**: an offered materialization must *state* whether it was formed
at `R_F` or reached its anchor by coarsening, and MME must adjudicate that claim rather than manufacture one.
Today the engine fabricates `forgotten_since_root` for any non-root establishment.

**Verdicts:** `ADMITTED_AS_CURRENT(id, superseded=[…], inherited=[…])` · `ADMITTED_AS_COEXISTING(id)` ·
`ADMITTED_AS_HISTORICAL(id)` · `REFUSED(code, detail)`.

**After admission MME owns everything and the offerer owns nothing:** currentness, descendant inheritance,
candidate eligibility, residency class. The offerer's last act is the intent.

**Admission is optional.** A value may be obtained, used to answer one request and never offered — which
already works **[verified claim 3]**. *Materialization does not imply retention* is therefore not new
machinery, it is a default to preserve.

---

## E · Request dispositions

```
consider(target: FamilyPoint, instance) -> Disposition
```

| disposition | payload | meaning |
|---|---|---|
| `READY` | `candidates: [MaterializationId, …]`, `route` | current held state can establish the target |
| `NEED` | `requirements: [FamilyStateRequirement, …]` | governed family state is missing |
| `WANT_OF_STATE` | `points: […]`, `family` | analytically required *values* are unresolved (#349) |
| `UNSUPPORTED` | `capability`, `provider` | the profile cannot execute a lawful composition |

**`NEED` carries analytical requirements only.** Shape:

```
FamilyStateRequirement { family_id, at_or_finer_than: Anchor, within_region: ContinuationRegion,
                         value_form, parameters?, reason }
```

It names *what governed family state would satisfy the target* — never a table, file, connection, query or
fetch plan. The Realization Manager reads it and decides *how*; if it cannot, that is its `UNSUPPORTED`, not
MME's.

**Mapping from today's outcomes:**

| today | v1 |
|---|---|
| `unanswerable` (nothing held) | `NEED` |
| `want-of-state` | `WANT_OF_STATE` |
| `unrealized-composition` / `unrealized-law` / `unrealized-kernel` | `UNSUPPORTED` |
| `outside-continuation-region` / `not-reachable` as a *blocker on a candidate* | folded into `NEED`'s reason — this candidate cannot reach the target, so state that can is needed |
| `outside-continuation-region` as a property of the **target itself** | **Resolver's refusal, before MME** |
| `ambiguous-data-state` | `READY` with **two candidates** — MME reports both and does not pick |
| `retired-contribution-filter`, `provider-invented-a-point`, … | constitution-time / provider refusals; not dispositions |

**Two decisions I am asking to be settled, not assuming:**

- **D-1 · Asking MME about an unlawful target.** *"Resolver owns analytical illegality"*, but MME still holds
  the region law. **Recommendation:** the four dispositions are for lawful targets only, and an unlawful ask
  **REFUSES** (fails closed) rather than returning a fifth disposition. Silence-by-`NEED` would invite a
  Realization Manager to go fetch state for a target that can never be lawfully served.
- **D-2 · Two coexisting current materializations that can both answer.** **Recommendation:** `READY` with
  both named, and the *request* must name one. This keeps *"the engine does not pick an evidence state"*
  while removing the refusal, since under §7 the caller's transition intent has usually already resolved it.

---

## F · Platform responsibility map

| responsibility | owner | may decide | may never decide |
|---|---|---|---|
| target identity & lawfulness | **Resolver** | is `F@A` a lawful governed target in this Manifold | what is held; how to obtain it |
| reuse of held family state | **MME v1** | which held materializations may establish the target, under family law; currentness; residency | that a target is lawful; how to obtain missing state |
| obtaining missing governed state | **Realization Manager** | how to produce state satisfying a `NEED`; what it cannot do (`UNSUPPORTED`) | that the result is lawful, current, or reusable |
| orchestration | **Manifold Runtime / Fulfillment Coordinator** | order of operations; retries; what to ask whom | any analytical fact |
| expression evaluation | **Serving (above MME)** | basis compatibility; the kernel to apply | anything about family cache state |

```
request ──▶ Resolver: is AOV@A lawful?
              │ yes
              ▼
           Runtime ──ask──▶ MME: Revenue@A?  ──▶ READY(#2)   ──┐
                   ──ask──▶ MME: OrderCount@A? ──▶ NEED(…)  ─┐ │
                                                             │ │
                   ◀── Realization Manager ◀── NEED ─────────┘ │
                   ──offer(OrderCount@A, intent=COEXIST)──▶ MME │
                   ◀── ADMITTED_AS_CURRENT(#7) ─────────────────┘
                   ──▶ Serving: basis compatibility(#2, #7) ──▶ columnar kernel ──▶ AOV@A
                                                                  (NOT cached by MME v1)
```

**The invariant across the whole map:** *backend capability cannot override analytical law.* MME asks family
law for reuse entitlement even when the Realization Manager could produce the value more cheaply another way,
and `UNSUPPORTED` is a statement about a provider, never about a law (`kernel/realization.py` already
enforces this and needs no change).

---

## G · Cold and warm start

**One door.** Warm start is not a second ingestion path: pre-populated materializations enter through the
*same* `offer(...)` protocol, with the same seven checks. A loader that bypassed admission would be the place
warm start silently disagreed with cold.

| | cold | warm |
|---|---|---|
| initial store | empty | admitted materializations |
| first ask | `NEED` → Realization Manager → `offer` → `READY` | `READY` |
| analytical answer | **identical** | **identical** |
| difference | cost, latency, number of `NEED` round trips | — |

> **The cache-neutrality invariant.** For any lawful target, the served value is identical for **any** subset
> of derivable materializations resident — including the empty set. Cache population may change cost,
> disposition sequence and route; it may not change an answer.

This is testable and I recommend it as the **first** conformance test of the implementation unit: take the
running exhibit, answer every target from a cold store, then from a fully warm store, then from every
one-entry-evicted store, and require value equality across all of them. It is also the invariant that makes
selective eviction safe to design later: if an eviction can change an answer, the bug is not in the policy.

**Use-once-and-discard** is the same mechanism, unnamed: obtain, answer, never offer **[verified claim 3]**.
Worth naming in the API (`consider → establish → answer` without `offer`), because a caller that must
*remember not to retain* will eventually forget.

---

## H · Assessment of the witness / persistence machinery

### The six questions, answered

**Q1 · Do we need per-object `ConstitutionWitness` for runtime cache correctness if one built Manifold
defines current semantics?**
**No — not for a single-build, in-process cache.** If every held materialization was admitted under the
current build, then *"the cache belongs to the build"* is a simpler and stronger invariant than any digest
comparison: drop the cache when the build changes and nothing stale can be reached. The witness earns its
keep at exactly one place — **the boundary where material crosses a build**: persistence and warm start
(#352), and any externally offered `F@A` (§7). There, dropping everything is the only alternative, and it is
a bad one.

**Q2 · What useful role remains?**
Three, all real: **(a) admission credential** at that boundary — the check that makes warm start safe rather
than hopeful; **(b) diagnostics** — naming *which* determinant moved, which is the difference between
"re-establish something" and "re-establish because participation changed"; **(c) persistence assurance** —
the fail-closed scheme guard (`witness-scheme-superseded`). What it should **stop** being is an *identity
axis of every cache entry*: that is how it ended up doing supersession's job by key inequality.

**Q3 · Is `DataStateRef` merely materialization-instance identity, or something more?**
**Something else, and it must not be used as instance identity.** It is the *analytical attribution* of
material to an evidence state. Two materializations can share one `DataStateRef` (re-derived after eviction;
produced by two providers) and one materialization cannot have two. So instance identity must be a separate
minted `materialization_id`, and `DataStateRef` stays in `provenance` — where it feeds the diagnostic in
§B.2(2) and nothing else automatic.

**Q4 · Is `forgotten_since_root` genuinely needed, or can dependency + family law determine reuse?**
**Genuinely needed. This is the report's sharpest finding.**
For a *derived* materialization the cumulative forgotten set is in principle derivable by walking
`derived_from` to a root and unioning each hop's edge. But **MME v1 introduces eviction**, and an evicted
ancestor breaks the walk. If entitlement were computed by walking, then evicting `#2` would make `#3` look
independently established — and an unlawful onward continuation would become available *because a cache
policy dropped a parent*. That is physical absence becoming analytical authority: the same defect as the
laundering guard, arriving through the cache instead of through a materialization.

> **Rule: a materialization's continuation entitlement must be decidable with none of its ancestors
> resident.**

So the two mechanisms have two jobs and neither replaces the other: **dependency links are for invalidation;
the frozen entitlement is for reuse.** Keep both. And fix the fabrication in **[verified claim 4]**: for an
independently established materialization the forgotten set is a *claim about formation* that must be
declared and adjudicated at admission (check 6), not manufactured from `root.forgets(anchor)`.

**Q5 · Which P-2 fields are necessary to reload a family cache?**

| necessary | why |
|---|---|
| `identity` (sort, family, anchor) | which object this is |
| `values` + `standing` files | the family value, and the standing that gives its nulls meaning |
| `coordinate_index.identity` | re-derived and checked; positions are what every mask is aligned to |
| `data_state` | analytical attribution; distinguishes evidence states |
| `constitution.{scheme,digest}` | admission at the build boundary |
| `constitution_context` | the shared context reference; refuses material from another context |
| `realization` | interchangeability (an approximate provider's value is not an exact one's) |
| `forgotten_since_root` | entitlement — and its loss is **silent** (Q4) |
| `disclosures` | a disclosure that can be dropped will be dropped **[verified claim 5]** |

| unnecessary | disposition |
|---|---|
| `law`, `value_form` | derivable from the declaration; redundant given a matching witness → diagnostics only |
| `coordinate_index.{points,references}` | derivable from the file |
| `values.{arrow_type,arrow_null_count}`, all `note` fields | diagnostics |
| `route` | narrative provenance |
| `constitution.determinants` | diagnostics (see Q6) |
| `constructor`, `basis_id` | expression-only |

**Q6 · Which fields came from treating MME like a semantic-history database?**
Four, and I should own the first two — they are mine from #351/#352:

1. **`constitution.determinants` persisted.** Written so a fresh engine could *name* what moved. Under one
   built Manifold the current build can compute the current determinants; the block only needs the digest to
   compare. **This is diagnostics, and P-2 overstated it as a requirement.**
2. **`MME._constitutions` + `remember_constitution`.** An engine keeping a history of every constitution it
   has ever seen is a version store wearing an MME's clothes. The Manifold *build* should hold that.
3. **`route` as a stored field.** Provenance narrative. Useful in an exhibit; not cache state.
4. **`Staleness`/`WitnessComparison` as engine API.** The comparison is diagnostics; the *governed* fact v1
   needs is `SUPERSEDED`, which the lifecycle model gives directly.

### KEEP / SIMPLIFY / RETIRE

| item | verdict | action |
|---|---|---|
| `FamilyPoint`, `AnalyticalInstance` (governed axes) | **KEEP** | unchanged |
| `adjudicate` (the five questions), `ContinuationRegion` | **KEEP** | unchanged; this is the `AnalyticalAdjudicator` |
| `forgotten_since_root` | **KEEP** | move into `ContinuationEntitlement`; **declared** at admission for independent establishment, not fabricated |
| `disclosures` on state | **KEEP** | they are part of the value |
| `RealizationStanding` | **KEEP** | provenance + interchangeability; never analytical |
| `DataStateRef` | **KEEP** | in `provenance`; **not** instance identity |
| `ConstitutionWitness` | **SIMPLIFY** | admission credential + diagnostics + persistence assurance; **off** the cache key |
| `RetentionKey` | **SIMPLIFY** | → `MaterializationId` (opaque) + selectable attributes. Fixes **[verified claim 1]** |
| `resolve_pool` / `PoolResolution` | **SIMPLIFY** | → `CandidateSelector` selecting on **eligibility**, not key equality |
| `ambiguous-data-state` | **SIMPLIFY** | → `READY` with multiple candidates (decision **D-2**) |
| `constitution_context` | **SIMPLIFY** | → a reference to the Manifold **build**; stop pretending it is an independent axis |
| `constitution.determinants` (persisted) | **SIMPLIFY** | optional diagnostics, not an admission input |
| `Staleness` / `stale_states()` | **SIMPLIFY** | reporting over `SUPERSEDED`; keep the determinant naming as diagnostics |
| `RetentionKey.sort` | **RETIRE** *(with expressions)* | unnecessary once `E@A` leaves the store |
| expression retention in the MME store | **RETIRE from MME v1** | move above MME (§11). Fixes **[verified claim 2]** |
| `_establish` / basis compatibility inside the columnar MME | **RETIRE from MME v1** | to serving; it consumes MME-supplied columns |
| `MME._constitutions` / `remember_constitution` | **RETIRE** | belongs to the Manifold build record |
| sidecar `law`, `value_form`, `route`, `points`, `references`, `arrow_*` | **RETIRE as authority** | keep as clearly-marked diagnostics |
| sidecar `constructor`, `basis_id` | **RETIRE from MME v1** | expression-only |
| `witness-scheme-superseded` | **KEEP** | fail-closed admission, distinct from supersession |

**Nothing above is a deletion instruction.** Every RETIRE means *"stop reading it as authority and move it
out of the MME's core"*, and each needs its own unit.

---

## I · The smallest implementation unit to make the running MME conform

**Unit M-1 — "the materialization store, and the two lifecycle axes."** Design first, one PR, no persistence
changes.

1. `FamilyMaterialization` + `MaterializationId` (§A), and a `MaterializationStore` that can hold **two
   instances of one `F@A`** — the one thing the current store cannot do.
2. `offer(...)` with the seven admission checks and the four verdicts (§D), including **check 6** (entitlement
   claims adjudicated, not fabricated).
3. The two lifecycle axes (§C) and eager descendant inheritance on supersession (§B).
4. `consider(...) → READY | NEED | WANT_OF_STATE | UNSUPPORTED` (§E), replacing today's `Answer`-with-refusal
   on the *family* path only.
5. `CandidateSelector` = today's `resolve_pool`, selecting on **eligibility** instead of key equality;
   `adjudicate` untouched.
6. **First test: the cache-neutrality invariant** (§G) — cold, warm, and every one-entry-evicted store
   produce identical values.

**Explicitly out of M-1:** expression migration above MME (unit M-2), persistence alignment (unit M-3 —
**after** the lifecycle is settled, per §15: *"persistence should encode an already-understood cache lifecycle
rather than define it"*), eviction *policy* (M-4; M-1 provides the axes, not an algorithm), and everything
already deferred (CDC, scheduling, source storage, cross-Manifold).

**Sequencing recommendation.** M-1 before touching #352 further, because the two P-2 answers this report
revises — persisted determinants and the fabricated forgotten set — are both lifecycle questions wearing
persistence clothes. #352 is green and self-consistent; it should merge or wait as a whole, but it should not
be extended.

---

## Open questions for ruling

| # | question | my recommendation |
|---|---|---|
| **D-1** | What does MME return when asked about an **unlawful** target? | REFUSE (fail closed); dispositions are for lawful targets only |
| **D-2** | Two coexisting **current** materializations that can both answer | `READY` with both named; the request must name one |
| **D-3** | May `SUPERSEDE` name a **set**, including entries with no edge? | Yes — it is the only lawful route to an evidence-level supersession (§B.2) |
| **D-4** | Is `HISTORICAL` a distinct eligibility or `SUPERSEDED` + a flag? | Distinct: it was never current, and an as-of ask is a different target |
| **D-5** | Does the Manifold **build** become the `constitution_context`? | Yes; it removes a placeholder axis and matches "one built Manifold defines current semantics" |
| **D-6** | Does a `DataStateRef` coincidence with a superseded entry get **reported**? | Yes, as a diagnostic. Never propagated. |

---

*No code was changed for this report. Claims marked **[verified]** were executed against
`packages/columna-platform` at `main` + #352.*

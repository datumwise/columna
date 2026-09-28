# The v8-native Platform kernel and the running MME — architecture record

**Claude, at Huayin's direction, 2026-09-28.** Implements the strategy change of 2026-09-28 19:07:
*"The priority is a running Columna Platform MME, not migrating Columna Core to v8 one semantic unit at a
time… Platform is the architectural destination. Core will later be a bounded profile extracted from /
enabled by Platform."* **Governing theory:** ToD v8.0, published 2026-09-28, cited by version and section.

**Standing.** A running engine. `python -m columna_platform.kernel.exhibit` exits 0 with 42/42 checks.

---

## A. The architecture that emerged

Ten modules in `columna_platform/kernel/`. The shape was not chosen up front — three of its load-bearing
decisions were forced by what the proofs would not otherwise demonstrate, and those are marked ⚑.

```
geometry     Universe · Constituent · Anchor · Edge ⚑ · KernelRefusal
law          AnalyticalLaw · Composition · ContinuationRegion ⚑ · RequiredBasis · LawRegistry
realization  Realization · ProviderProfile                       ← the other half of the ruled split
standing     AnalyticalInstance · Compatibility · Refusal · Disclosure · routes
sorts        FamilyPoint (F@A) · ExpressionPoint (E@A) · MeasureFamily · GovernedExpression ·
             Operand · SufficientBasis
value        FamilyState (continuation-bearing) · ExpressionOutput (finalized) · Answer
mme          MME · RetentionKey · Retained · Adequacy
builtins     seven laws + the in-memory provider profile
exhibit      the runnable demonstration
```

### The three forced decisions

**⚑ 1 · `Edge` is a first-class object.** Value closure is relative to an edge (§3.1: it holds *"only for
the continuation region over which this condition holds"*), and a law cannot be relative to something
reconstructed at each call site. So an edge — `source → target`, named by what it **forgets** — is an
object before any law is asked about one.

**⚑ 2 · `ContinuationRegion` replaces `re_entrant` rather than porting it.** The V8-1 reconnaissance
recorded that a global Boolean cannot represent v8's edge- and condition-relative closure, and Core's own
`operators.py` comment forbids flattening a conditional certification into `True`. The proof that this
was necessary is in the vocabulary: **`SUM` and `STOCK_LEVEL` carry the same composition (addition) and
different regions.** A stock composes across stores and does not compose across time. A Boolean has
nowhere to put that difference.

**⚑ 3 · `FamilyState` and `ExpressionOutput` are two TYPES, and the expression one has no merge path at
all** — not a merge that refuses, none. The governed verdict in `mme.adjudicate` is the *explanation*, so
a caller learns which rule stopped them instead of what Python noticed. A Boolean on one class would put
those two facts one mutation apart.

### Where the §9.2 containment lives now

In Core it had to be a gate firing **after** resolution, over an object already constituted as a family
(V8-0's C4 clause 2, plus a `MissingGovernedFact` for the sort that did not exist). Here
`MeasureFamily.bind` refuses a law whose `continuation is None`. **"Do not create a Mean family" is not a
rule anyone has to remember — it is not a reachable state of the engine.** That is the difference between
migrating a semantic and building on one, and it is the single clearest argument for the strategy change.

### The MME's shape, and why

`retain` / `candidates` / `adjudicate` / `measure` / `evaluate` — because **holding an object and being
permitted to use it are two facts.** `retain` asks nothing and refuses nothing. `adjudicate` is the only
place a right is decided, and it asks five questions in order:

| | question | a `no` means |
|---|---|---|
| 1 | **sort** — is this family state at all? | an expression output is refused here, by verdict |
| 2 | **reachability** — is the target a coarsening? | geometry, not law |
| 3 | **closure over the whole route from `R_F`** | the laundering guard — see below |
| 4 | **adequacy of the value** | the state no longer carries the sufficient state |
| 5 | **realization** | a provider limit, and it says so |

**The laundering guard is the subtle one.** Forgetting `{store}` then `{day}` forgets `{store, day}`. If
`day` is outside the region, the two-step route must refuse exactly as the one-step does — otherwise an
intermediate materialization becomes a way to obtain an answer the law forbids, and *physical
availability would have become analytical authority* in the place it is hardest to see. So
`forgotten_since_root` rides on every state and closure is asked **cumulatively**, never per hop.

**Seed selection is least-work-first, and that is a governed choice, not an optimization detail.** The
first draft tried the root first — which does the most possible work on every ask and, the real defect,
makes non-root materialization *pointless*, so the engine could never exercise the right the ruling
specifically asks it to make operational. A rule never reached is not a rule that holds. Coarsest-first is
safe because a finer seed has forgotten less and is therefore never less permissive: **if any candidate is
admitted, the root is**, so trying the cheapest first can only turn an expensive answer into a cheap one.

### The retention key

`(sort, identity, anchor, instance, provider)`. Exactly the axes a retained object must be told apart by,
and nothing else: no physical grain, no storage location, no partition, no file. `instance` carries
participation, scope and a constitution witness, so a state from a superseded constitution is a
**different retained object** rather than a silent overwrite. In-memory only, per the ruling.

---

## B. Exact files

| file | lines | what it is |
|---|---|---|
| `packages/columna-platform/src/columna_platform/kernel/geometry.py` | 193 | universe, anchor, edge |
| `…/kernel/law.py` | 276 | the semantic authority |
| `…/kernel/realization.py` | 99 | the provider profile |
| `…/kernel/standing.py` | 107 | instance, compatibility, refusal |
| `…/kernel/sorts.py` | 311 | the two sorts and their identities |
| `…/kernel/value.py` | 161 | the two value types + `Answer` |
| `…/kernel/mme.py` | 479 | the engine |
| `…/kernel/builtins.py` | 310 | seven laws + in-memory provider |
| `…/kernel/exhibit.py` | 472 | the runnable demonstration |
| `…/kernel/__init__.py` | 78 | the package's own statement of the boundary |
| `packages/columna-platform/tests/test_kernel_mme.py` | 624 | 51 tests |

**3,110 lines added. Nothing outside `columna-platform` was touched. Core was not changed to make
Platform easier to build.**

---

## C. The law vocabulary — the smallest set the proofs need

| law | kind | value form | continuation | region | founds a family? |
|---|---|---|---|---|---|
| `SUM` | REDUCER | scalar | addition | everywhere | ✓ |
| `COUNT` | REDUCER | scalar | addition | everywhere | ✓ |
| `STOCK_LEVEL` | REDUCER | scalar | addition | **forget `store` only** | ✓ |
| `HLL_SKETCH` | REDUCER | **structured** | sketch union | everywhere | ✓ |
| `HLL_ESTIMATE` | **MAP** | scalar | — | — | ✗ constructor |
| `MEAN` | REDUCER | scalar | — | — | ✗ constructor |
| `LAST` | **ORDERED** | ordered witness | latest-by-order | everywhere | ✓ |

**The table is arranged so that structural kind × analytical sort covers every combination that
matters** — a REDUCER that founds a family and one that cannot, a MAP that cannot, an ORDERED that does.
The orthogonality is therefore a property of the vocabulary rather than of a comment.

---

## D. Test results — the Platform path

`ruff --select F,E9` clean over `packages/columna-platform`.

| | before | after |
|---|---|---|
| platform suite | 368 | **412 passed** (+51 kernel tests; +7 already on main from the parked unit) |
| exhibit | — | **exit 0, 42/42 checks** |

**The Core suite was not run as the inner-loop gate**, per the development-loop ruling. It is untouched by
this unit — no file outside `columna-platform` changed — and belongs at an integration boundary.

Three tests hold the architectural boundary rather than trusting it:

1. **AST scan** over every kernel module for an `import columna_core`. (A textual grep was written first
   and failed on the modules' own docstrings, which say in prose that `columna_core.sketch` was read and
   *not* imported. A string scan cannot tell an import from a sentence about one.)
2. **A subprocess** that builds a whole MME and asserts nothing under `columna_core` entered
   `sys.modules` — catching a transitive or lazy import the AST scan would pass. (The first version used
   `importlib.reload` in-process, which rebinds every class in the reloaded modules; `KernelRefusal`
   became a different object from the one the test file imported and seventeen unrelated `pytest.raises`
   assertions began failing for a reason unconnected to what they test.)
3. **An external-dependency pin**: the package reaches exactly one third-party module, `datasketches`, so
   a second dependency has to be a deliberate act.

---

## E. The runnable exhibit, and its output

    python -m columna_platform.kernel.exhibit        # exit 0

One universe `commerce`, ground `customer_order`, constituents `{store, day, order}`. Six accepted
orders, four stock levels, four gauge readings. Everything printed is computed.

**Proof 1 · additive family — root → lawful continuation → coarser family measure**

```
revenue @ commerce{day, order, store}  (R_F)   CACHED      6 cells
revenue @ commerce{day, store}                 CONTINUED   4 cells   seeded from R_F
revenue @ commerce{day}                        CONTINUED   D1 175.0  D2 325.0   seeded from {day,store}
revenue @ commerce{}                           CONTINUED   ALL 500.0            seeded from {day}
```

A **chain of non-root continuations**, which is the ruled right made observable.

**Proof 1b · edge-relative closure — a stock is not a flow, and the cache cannot change that**

```
on_hand @ commerce{day, store}  (R_F)    10 · 7 · 12 · 9
on_hand @ commerce{day}         SERVED   D1 17  D2 21            forgets ['store'] — inside the region
on_hand @ commerce{store}       REFUSED  outside-continuation-region
on_hand @ commerce{}            REFUSED  …"a two-step coarsening forgets the union, so an intermediate
                                          materialization cannot launder an edge the law does not admit"
```

and the `{day}` state it would have used **is in the store**.

**Proof 2 · structured family → merge → finalize as an expression**

```
distinct_customers @ R_F        structured, 6 sketch cells
distinct_customers @ {}         CONTINUED   payload type: hll_sketch  ⚠ approximate
distinct_customer_estimate @ {} EVALUATED   ALL 4        (true distinct = 4; rse@p12 ≈ 0.0163)

held: expression:distinct_customer_estimate@commerce{}   continuation_bearing=False
adjudicate(estimate → seed distinct_customers@commerce{}):
  REFUSED [not-continuation-bearing]
  "…It may be cached and served — it is both, right now — and it never becomes family continuation
   state… being named, cached, repeated or durably governed does not make it continuation-bearing (§3.7)"
```

**Proof 3 · cross-family expression — Revenue + OrderCount → AOV. No Mean family exists.**

```
MeasureFamily(law="MEAN")  →  REFUSED [not-a-family-law] at CONSTITUTION
revenue     @ {day}   {D1: 175.0, D2: 325.0}
order_count @ {day}   {D1: 2,     D2: 4}
compatibility: HOLDS — same world, participation, scope and constitution
average_order_value @ {day}   EVALUATED   D1 87.5000   D2 81.2500
average_order_value @ {}      EVALUATED   ALL 83.3333
asked again                   CACHED
```

**83.3333, not 84.3750** — the mean of the daily means, which is the error a Mean family would have made.
The fixture is deliberately **unbalanced** (2 orders on D1, 4 on D2): at 3/3 the two values coincide and
this check would have passed on an accident of the data. The first draft was 3/3 and the check caught it.

**Proof 4 · an incompatible basis is refused while both operands exist**

```
revenue             @ {day}  served  {D1: 175.0, D2: 325.0}
audited_order_count @ {day}  served  {D1: 2,     D2: 2}
average_order_value_audited @ {day}  REFUSED [no-sufficient-basis-establishes]
  "roles 'COUNT' and 'SUM' are both ESTABLISHED AND AVAILABLE at commerce{day} and are not jointly
   usable [different-participation]… individually valid and jointly meaningless, so their combination
   is a number about no population… NOTE WHAT THIS IS NOT: it is not a claim that the operands are
   absent… physical availability is not analytical authority"
```

**Proof 5 · the two caches, and their different continuation rights** — every family state is asked
whether it may seed one step coarser (some ADMITTED, some REFUSED `[outside-continuation-region]`), and
every expression output is asked the same question (all REFUSED `[not-continuation-bearing]`, while all
remain held and servable).

**Proof 6 · ordered family** — the witness is `('17:00', 5)`, the order key rides with the value,
`LAST@S1` selects D1's 17:00 over D2's 09:00 **by order**, and an empty eligible fibre is `KNOWN_EMPTY`
rather than `None`, because `LAST` has no identity and *there was nothing to select* is a governed answer
distinct from *we do not know*.

**Addenda** — a provider that does not realize `MEAN` refuses as a **realization** limit naming the
provider (§4.1: a backend's inability does not remove a law); `invalidate('revenue')` drops 4 states and
rebuild is from `R_F`, with no retraction method existing to be called.

---

## F. What was reused or lifted from the old estate

| | disposition |
|---|---|
| `datasketches` (Apache DataSketches HLL) | **used directly.** A third-party algorithm, not an ontology |
| `columna_core.sketch`'s `rse` formula and `hll_sketch`/`hll_union`/`get_estimate` call shapes | **lifted as knowledge, not imported.** That module carries `Witness` and `WitnessStore`, which are the old estate's *retention doctrine*; this kernel has its own |
| Core `foundation.py`'s law content (target forms, operand domains, `sufficient_state` prose, the MIN/MAX identity argument) | **read as evidence about required capabilities**, re-derived. `is_monoid` → `Composition.has_identity`; `combine` → `Composition.token` |
| Core `operators.py` | **read as evidence and not ported.** `re_entrant` → `ContinuationRegion` (a Boolean could not carry it); `linear` and the SQL/scan machinery are realization and are absent |
| The parked V8-1 unit (#346) | **conceptual reuse only.** Role-indexed operands and basis components; a sufficient basis as an establishment route rather than identity; zero/one/several admitted bases; inner anchors distinguished from a root; the family/expression sort separation and the refusal to reach one through the other |
| Core `governed/*`, `LawView`, C1–C9, native v3.0/v3.1, generated-family doctrine | **not used.** Enforced by three tests |

---

## G. What in v8 proved insufficient

Four items. None blocked the build; all were worked around **by reporting rather than by inventing.**

1. **`governed equivalence` is still undefined** (§7.3 ×2, §7.6). Carried forward from the V8-1 unit as a
   theory errata candidate. It did not bite here only because this slice mints no successors — the moment
   expression succession enters Platform it will, and v7.1 §6.6's congruence obligation is the candidate
   definition.
2. **No law schema in v8 states operand ARITY.** `operand_domains` is a domain set, not a signature, so
   the number of operands a constructor takes has nothing to be validated against. The kernel reports
   this rather than assuming unary. (Same finding as V8-1; it is a gap in the theory's law schema, not in
   either implementation.)
3. **A family declaration does not name the law its own values are FORMED by** — only its target (prose)
   and its continuation. So "does this family supply the `COUNT` role of a basis?" is not decidable from
   the declaration: `SUM` and `COUNT` both entail `SUM`, and a total and a count are indistinguishable by
   continuation congruence. **The Platform kernel makes this worse-behaved and more visible**, because
   `MeasureFamily.law` *is* the forming law — so the kernel can check what Core cannot. v8 owes the rule
   that a basis component's role is satisfied by a family whose forming law *is* that component law; this
   kernel implements exactly that and the theory does not state it.
4. **`ContinuationRegion` has no basis in v8's text.** §3.1 and §3.5 both require edge- and
   condition-relative closure, and v8 gives **no representation** for the region — no notation for *which*
   edges a family's closure covers, and no rule for how a region composes across a multi-step coarsening.
   The cumulative laundering guard is therefore **the kernel's own rule**, derived from what §3.1 means
   rather than from what it says. This is the largest thing v8 leaves to the implementation, and it is
   load-bearing: without it, caching an intermediate is a soundness hole. **Recommended as the next
   errata/extension candidate.**

---

## H. Recommendation — the shortest path from the running MME to Frame-QL serving

Three units, each with its own stop gate. None of them touches Core.

**P-1 · A request-shaped entry over the kernel, and nothing else.**
The MME's entry points already take `(object, anchor)`. What Frame-QL adds is a *token* and a *requested
constituent set*. So: a `kernel/request.py` that resolves a token through `MME.sort_of` — which exists and
is already the single dispatch question — into either `measure` or `evaluate`, and turns an `Answer` into a
classified outcome (serve / disclose / refuse). **`Answer` is already total and already carries `route`,
`disclosures` and a coded `Refusal`, so this unit is a translation and not a decision.** Stop when a
Frame-QL-shaped ask over a token and an anchor serves through the kernel and every refusal class is
reachable. *Explicitly not: parsing.* Construct the request object programmatically, exactly as this unit
constructs the world.

**P-2 · The statement parser, reused as syntax only.** Frame-QL's existing parser produces `series` and
`anchor` and treats both as syntax — the one Core-adjacent component whose output is a *string and a set*
rather than an ontology. Lift it behind an adapter that yields the P-1 request object; do not let its
model cross the boundary. Stop when `SELECT revenue AT {day}` serves from the kernel.

**P-3 · Constitution from bytes.** Only now does serialization earn its place, and it should be a
**Platform-native** format built from the kernel's own objects, not native v3.1 — which is why parking
#346 was right. The kernel's `RetentionKey` and `AnalyticalInstance` already say what a constitution
witness has to be stable across; that is the format's actual requirement, and it is now known rather than
guessed.

**Do P-1 first and alone.** It is small, it needs no parsing and no format, and it converts a running
engine into a running *service* — which is the shortest distance between where this unit stopped and
something a request can reach.

# Column Algebra / Frame-QL Expansion — Mission 1 reconciliation map

**Version:** 0.1
**Date:** 31 August 2026
**Subject:** *Column Algebra / Frame-QL Expansion, Design Record v0.2* — items **1–6 and 10–13**
**Mandate:** reconnaissance and reconciliation. **No implementation authorized by this document.**
**Held back:** items **7, 8, 9** (reusable state, semantic state key, invalidation) are **Mission 2**,
gated behind Unit D / D1's v5→v6 crosswalk, so the reconciliation cannot accidentally ratify the
current hybrid `family` / `root_evaluator` vocabulary (ruling, Huayin, 2026-08-31).

Evidence grades follow the ledger: **VX** reproduced under the real runtime · **SV** read at
file:line · **INF** inferred.

---

## 1. Executive verdict

**Less new than the record assumes at Levels B and C. More new than it assumes at Level A. Three of
its premises are wrong.**

The record reads the *Manual* as evidence of shipped machinery. On the multi-input question the
Manual is not evidence — it documents a form the planner refuses. Meanwhile the record treats
joint-formation discipline as something to be designed, when Columna already implements it correctly
for juxtaposition and incorrectly for expressions, **1,280 lines apart in one file**.

The single most consequential finding: **§4.2.1 is not a principle to adopt. It is a defect Columna
has today** — recorded as **P1-11**.

---

## 2. Reconciliation table

Statuses per the mission brief, including the eighth added at reconciliation time.

| # | Design-record item | Status | Evidence |
|---|---|---|---|
| 1 | Multi-input Frame-QL grammar | **contradicted by shipped behavior** | Manual `:277` states the canonical multi-input shape and claims *"the framework parses this form directly, type-checks it, and plans it."* Reducers are hard-arity-1 (`planner.py:908`). **VX** |
| 1b | `(a,b) @ A` as syntax | **partially shipped** | Envelope accepts it verbatim (`envelope.py:49-55`; depth-aware `_split_top:135`). `ast.Tuple` already in `_ALLOWED` (`planner.py:27-29`). `@ {a*b}` → `@ (a,b)` desugaring ships (`planner.py:576-595`). Refuses semantically at `planner.py:1520`. **VX** |
| 1c | Multi-input clarify | **contradicted by shipped behavior** | Manual `:315` documents `input_anchor_ambiguous` covering the multi-input case; unreachable — the arity gate fires first with generic `unknown`. **VX** |
| 2 | General datum value types | **new runtime machinery** | 11 scalar dtypes; `ANY = DTYPES` (`types.py:22-42`); nested types excluded by docstring (`types.py:16-17`). No type registry; `is_dtype` has zero callers. **SV** |
| 2b | value ≠ state ≠ carrier | **partially shipped** | Exists exactly once (HLL). But the parametric type and the operator marker **never meet**: `out_rule="HLLSketch"` is unparameterized and no value is ever tagged `HLLSketch(12)`; the precision lives on `MeasureColumn.sketch_precision`. **SV** |
| 3 | Internal axes are type parameters | **theory only** — uncontradicted | Nothing composite exists, so nothing conflicts. Cheap to hold now. **SV** |
| 4 | Joint expression formation | **partially shipped / contradicted** | `planner.py:504-513` §2c FRAME LAW: `how="full"`, *"each column keeping its own population semantics."* `planner.py:1791`: `how="inner"`, undeclared. **VX** — see **P1-11** |
| 4b | Eligible frame ≠ co-supported points | **contradicted by shipped behavior** | Support is a scalar cardinality (`f.height`, `engine.py:1138`), not a set; `validate_universe_support` has **zero callers repo-wide**. **SV** |
| 5 | Participation as first-class law | **genuinely new law** | Zero occurrences of `participation` / `complete_case` / `listwise` / `pairwise` in shipped code. One hard-coded policy: `engine.py:335-338` (ORDERED only). **SV** |
| 5b | Ambiguous participation → Clarify | **new runtime machinery** | Five clarify reasons exist, all `(CLARIFY, AMBIGUOUS)`; `outcome_for` fail-closed. OF-1 (`disclosure.py:202-206`) forces a **new registered reason**, not a widening. **SV** |
| 6 | State-law taxonomy | **partially shipped** — see §4 | `witness` distribution: `value` 18, `sketch` 3, `ordered` 2, `holistic` 3. Three of four ToD v6.1 classes have instances; associative-noncommutative has none. **VX** |
| 10 | Construction-dependent types | **genuinely new law** | `License` attaches to members / hierarchies / bases / faces — **never to a result**. No license, verdict or scope field on any wire column (`disclosure_wire.py:235-256`). **SV** |
| 11 | Declaration vs ask time | **already shipped** | 19 enumerated publish-time checks; the planner resolves, never proves. Already ratified at `core_p05a:177-180`. **SV** |
| 11b | Φ declared, absence computed per-ask | **already shipped** | `FILL` at `model.py:180`; which cells are absent is only knowable post-align (`planner.py:524-547`). **SV** |
| 12 | Operator admission tiers | **partially shipped — wrong abstraction** — see §5 | Five independent ladders that disagree about one operator. **VX** |
| 13 | Statistical Bridge boundary | **already shipped — one exception** | Zero hits for p-value / significance / confidence / bootstrap. HLL `rel_error` is structural (`1.04/√2^p`, zero fetches) and stays in the Data World. **The MNAR string leans over**: *"averages are selection-biased"* is a claim about an unobserved target, and it attaches to `sum` and `count` too (`engine.py:1160-1162`). **SV** |

---

## 3. Conflicts and corrections

**C1 — §3.2's premise is false.** *"The Manual already has a multi-input canonical operator shape…
therefore the proposed work does not introduce the concept of a multiple-input operator from
nothing."* The Manual states it; the system refuses it. The record builds on documentation, not
machinery. → **P0-18**

**C2 — the Manual is contradicted by shipped behavior.** §2.4's pinned-map examples and §5.2's
*"the framework checks that all input column references resolve to the same input anchor"* — the
examples error, the check has no implementation. The docs gate missed it because
`check_manual_frameql.py` is **grammar-only by design**. → **P0-18**

**C3 — §4.2.1 describes a present defect.** → **P1-11**

**C4 — §3.3's "one universe" is weaker than the record leans on.** `_check_single_universe`
(`planner.py:212-229`) compares **universe name strings only** — not support, not Φ, not missingness.
The record says joint formation "must not become a backdoor around" the universe rule; the backdoor
is already open *inside* one universe (**P1-10**, **P1-11**).

**C5 — §3.4's discipline does not transfer for free.** OF-1's *"one reason per contested dimension"*
means participation needs its own registered reason, not a widening of `ambiguous_grain`.

---

## 4. `witness` is capability evidence, not a state-law taxonomy

**Ruled by Huayin, 2026-08-31, and it retracts a recommendation made earlier in this mission.** An
earlier draft proposed "make `witness` the declared tier." That would ratify an implementation gap as
analytical law.

```
mean      witness=holistic  is_monoid=False  combine=None  in_core=False
median    witness=holistic  is_monoid=False  combine=None  in_core=True

amt.sum     -> serve
amt.mean    -> error   "holistic operator 'mean' not implemented"
amt.median  -> serve
```

`median` is HOLISTIC because **no finite sufficient state closes it** — a *law* fact. `mean` is
HOLISTIC because **this build implements no decomposition** — a *build* fact. `(Σx, N)` is a
perfectly good sufficient state for mean. The compiler's own `_WHY_NOT` states both:

> `mean` — *"shipped Core accepts `mean` as a declared member and then refuses it at execution"*
> `median` — *"held out of K0 for scope minimality; shipped Core does execute it"*

**Why it matters beyond hygiene.** The record's §7 flagship is a reusable state `(N, Σx, Σxxᵀ)`
serving *mean*, covariance, correlation and OLS. Mean is the first item on that list, and Columna
currently declares it stateless. A taxonomy read off `witness` would have falsified the record's own
motivating example.

**What a canonical taxonomy needs that `witness` cannot give:** a separation between *does a
sufficient state exist* (law) and *does this build implement it* (capability). Today `in_core` and
`witness` both encode build facts and sit in the same dataclass as the law fields. That adjacency is
the mechanism of the error.

---

## 5. Operator admission: a profile, not tiers

**Columna already tried tiers and ended up with five ladders that disagree about one operator:**

| ladder | verdict on `mean` |
|---|---|
| witness dispatch (`engine.py:236-246`) | HOLISTIC — recompute from base |
| `in_core` (`engine.py:266-272`) | `False` — refuses at execution as a declared member |
| `SERIES_REDUCERS` (`operators.py:166`) | present — `avg(x @ {a})` **works** |
| `K0_REDUCERS` (`compile.py:44-67`) | excluded — *"accepts, then refuses at execution"* |
| crossing law G5 (`engine.py:403-417`) | not a monoid — refuses at every face |

**And capability is anti-correlated with admission**, which no total order can express:

| operator | state richness | crossing admission |
|---|---|---|
| `sum`/`min`/`max` | **lowest** — the value *is* the state | **highest** — the only ones that cross a face |
| `last`/`first` | mid — ordered witness, argmax/argmin | refuses |
| `distinct`/HLL | **highest** — carrier + union + finalizer + publish-time materialization | **lowest** — `anchor_spent` at every face |
| `median`/`mode` | none | refuses |

Under the record's §12, `distinct` is simultaneously Tier 3 and Tier 0.

**Recommended shape:**

```
LAW dimensions (analytical, build-independent)
  sufficient_state      none | value | ordered-witness | separate-carrier<T>
  combine_law           op + algebra (commutative? identity? associative-only?)
  order_requirement     none | total order over <axis>
  finalizer             identity | <projection op>
  anchor_consumption    preserved | SPENT           <- G5, declared not hardcoded
  participation         admissible policy set       <- new
  approximation         exact | bounded(ε) | unbounded
─────────────────────────────── wall ───────────────────────────────
BUILD dimensions (this release)
  executes_here         in_core
  decomposition_built   <- where `mean` actually belongs
```

`anchor_consumption` is the dimension that produces the anti-correlation and is currently **not
declared at all** — hardcoded in `engine.py:403-417`. That alone rules out a ladder. Tiers survive as
a *derived reading* ("commutative combine + finalizer ⇒ reusable"), never as the declaration.

---

## 6. Hidden opportunities

1. **`DATA_GAP` is declared, wired MATERIAL as `incomplete_data`, and has zero producers.** A
   pre-contracted empty slot. No wire change needed to use it.
2. **One MATERIAL caveat flips the frame `serve`→`disclose`** (`disclosure_wire.py:271-280`). The
   cheapest correct mitigation needs no new mood and no contract bump.
3. **The alternatives-as-menu carrier already exists** (`planner.py:352-359`) — the shape for "here
   are the N lawful participation policies."
4. **The architecture is already ruled.** `f0_reconnaissance.md:150` — `LAW → EXECUTION DIRECTIVE →
   SUBSTRATE`. `f0:147` already names *"participation/absence"* among ~19 embedded decisions. Only
   frame-assembly has been lifted; the expression path is the same lift.
5. **`mean` was registered solely to give `(operator × lineage)` law an address**
   (`operators.py:97-99`) — the precedent for registering a law-bearing operator the engine composes
   rather than executes directly.
6. **`ADDITIVE, SKETCH, HOLISTIC` are already exported** (`model.py:17-18`) with zero consumers.

---

## 7. True new work

**Language:** arity > 1; multi-input operand resolution; a co-anchor check that actually runs.
**Runtime:** participation declaration; support as a *set* rather than a cardinality; a multi-input
engine entry point; composite value types + a type registry; **a dtype on the wire**.
**Law:** participation as identity-bearing; construction-witnessed types; result-level standing.

---

## 8. Recommended architecture

1. **Fix participation where it already bites**, before any new surface (**Mission A**). Standalone
   value even if the tuple surface never ships.
2. **Zero new syntax.** Implement the Manual's own documented shape `op(a @ {A}, b @ {A})` rather
   than adding `(a,b) @ A`. It already parses, it is already canonical, and building it *repairs*
   C2 instead of adding a second form. Keep `ast.Tuple` meaning composite **grain**, one meaning only
   — otherwise one constructor carries two meanings at the point the record most wants clarity.
3. **Level A starts with observability.** The wire carries no dtype and two declared types
   (`Decimal`, the temporals) have no serialization path. Ship that before composites, or
   `Matrix<Float64,5,5>` becomes the first type to discover the wire cannot carry it.
4. **Profile, not tiers**; declare `anchor_consumption` explicitly.
5. **Do not promote `witness`.** Split it into `sufficient_state` (law) and `decomposition_built`
   (build).

---

## 9. Candidate missions and dependency order

| | Mission | Depends on |
|---|---|---|
| **A** | Alignment-domain declaration + support-divergence disclosure | — |
| **B** | Manual/code reconciliation for multi-input + pinned maps; extend the docs gate to **plan**, not merely parse | — |
| **E** | Type observability: dtype on the wire; `Decimal`/temporal serialization | — |
| **C** | Participation as declared law + `participation_ambiguous` | A |
| **D** | Multi-input arity + a real co-anchor check (the Manual's shape) | B, C |
| **G** | Capability/law profile; split `witness`; declare `anchor_consumption` | C |
| **F** | Composite value types + type registry | E |
| — | Reusable state, semantic keys, invalidation | **Unit D / D1** |

---

## Appendix — probes run during Mission 1

All read-only; no tree was modified during reconnaissance.

| probe | result |
|---|---|
| two measures, divergent support, side by side | `serve`, 3 rows, `unknown_absence`/caution |
| same two, combined by `/` | `serve`, 2 rows, **zero caveats**, `population: ops` |
| DERIVED over an HLL measure | `approximation` caveat **propagates** — `Disclosure.combine` is sound |
| Manual §2.4 pinned map operands | `error` — `unknown column 'transaction'` |
| Manual §2.4 composite pinned operands | `error` — `unsupported expression node Tuple` |
| Manual §2.1 multi-input canonical | `error` — `'corr' is not a scan operator` |
| record §4.4 joint tuple surface | `error` — same |
| multi-arg shipped reducer | `error` — `'avg' takes exactly one column argument` |
| `amt.mean` as a declared family member | `error` — `holistic operator 'mean' not implemented` |
| `amt.median` as a declared family member | `serve` |
| registry enumeration | 26 operators; witness `value` 18 / `sketch` 3 / `ordered` 2 / `holistic` 3 |

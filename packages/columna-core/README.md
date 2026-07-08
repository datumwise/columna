# Columna Core (0.7.7-core)

> **v0.7.7-core — `ON UNIVERSE` pin wiring (Option A).** The population pin recorded by `Frame.on_universe(u)` is now threaded to the planner (`run`/`plan` → `_infer`), where it asserts the frame's intended population. A measure bound to `u` serves; a measure bound to a *different* universe is out-of-domain for that population and **refuses** (`out_of_universe`); an unknown `u` is an **error**. This resolves the multi-universe and D5 co-anchoring ambiguity to the one chosen population — so a cross-universe ratio that *clarifies* unpinned becomes a serve or an honest refuse once pinned, and a multi-universe frame's coverage caveat is resolved. (Resolving a measure over a universe *other* than its declared one — true cross-universe confinement — is Option B, future.) `coanchor_demo` §D covers it. 124 checks across 11 suites.

> **v0.7.6-core — the no-result is a value, not an exception.** The structured no-result is split into a plain `Outcome` value (kind · discriminator · reason · alternatives) and a private internal `Refusal` *signal* that merely carries it from deep in the recursive walk to the planner's single assembly point. `ColumnResult.refusal` now holds an `Outcome`: a clarify/refuse/error is **data** every surface and agent reads, never an `Exception` a caller could swallow with `except Exception`. (`Refusal` remains the internal control-flow goto; eliminating even that would mean return-threading the recursive type-inferencer — deliberately not done.) `coanchor_demo` asserts the clarify is an `Outcome`, not an exception. 116 checks across 11 suites.

> **v0.7.5-core — ratio/rate co-anchoring (ADR-032 D5).** A ratio `N / D` is determinate only when numerator and denominator resolve over one shared population. The planner now checks this statically: a ratio whose operands span different universes is a **clarify** (`co_anchor_ambiguous`, discriminator `ambiguous`) naming the candidate populations — "which population is the rate over?" — never a silent number. It is *not* eager (a same-universe ratio, or a constant denominator, just serves) and is distinct from avg-of-averages (a B-anchor hazard). Scoped to the ratio: the same two measures as *separate columns* still serve with the multi-universe coverage caveat. New `coanchor_demo`; 115 checks across 11 suites.

> **v0.7.4-core — the two-level correctness contract (ADR-032).** The column engine never judges: it attempts and returns either a result or a *no-result carrying a discriminator* — `ambiguous` (no unique answer under the rules) or `unsupported` (the data can't support a result). The **planner** owns the four outcomes (serve · disclose · clarify · refuse), plus `error` for vocabulary/capability failures, and classifies every no-result at one chokepoint (`Refusal.classified`). The multi-grain attribute case is now a **clarify** (ambiguous), not an `unknown` error lumped with real failures; out-of-universe is a **refuse**; an unimplemented operator is an **error**. `FrameResult.outcome / .clarifies / .refusals / .errors` surface the verdicts; `confine_demo` verifies the classification.

> **v0.7.3-core — attribute-anchor resolution hardened.** When a universe predicate references an attribute `T.col`, the engine must broadcast it at the level `T` is keyed. `_attr_anchor` no longer picks the first edge `T` provides: a single-grain table is unambiguous, a denormalized multi-grain table (one `geo` table providing `store→region` *and* `region→country`) is **pinned by the delivery frame**, and a genuinely ambiguous case is **refused with the candidate levels named** — never a silent wrong grain. `confine_demo` proves the pin and the refusal. 107 checks across 10 suites.

> **v0.7.2-core — universe-predicate evaluation hardened to typed predicates.** The universe predicate is evaluated at the base grain by **broadcast-and-filter, never a join**: each referenced attribute is delivered single-table and broadcast onto the frame along its key (transport), the compared sides are **coerced to a common dtype**, and the frame is filtered. Fixes a real gap — a numeric (`qty >= 10`) or real-`Date` predicate previously raised a dtype error because predicate literals arrive as strings, and only the benchmark's ISO-date *strings* compared correctly by luck. `confine_demo` now proves numeric / Date / AND-ed predicates alongside out-of-domain exclusion. 101 checks across 10 suites.

> **v0.7.1-core — B-anchor crossing locus refinement + EXPLAIN-without-execution.** Crossing *detection* moved from the engine (execute time) to the planner (compile time): `blocked_lineages` and the operator's `is_monoid` are now surfaced on the shape projection, so a crossing is knowable from structure alone. The served contract is unchanged (still served-with-critical, never refused), but `frame(...).plan()` / `explain(execute=False)` returns the would-be annotation — the critical crossing plus spec-only provenance caveats — touching **zero backend data**.

> **v0.7.0-core — a custom type + three custom operators, planner untouched (HLL case study).** The `distinct` family is decomposed into a parametric type `HLLSketch(p)` and three registered operators — `hll_count` (deliver), `hll_merge` (a monoid union, combine), `hll_estimate` (project) — that slot into the umbrella via the **registry and engine only**; `planner.py` and `projection.py` hold zero sketch references. Precision is type identity (a mismatched merge is a type error; a raw sketch is opaque to arithmetic). A publish-time **witness store** makes sketches **stored, not cached**, so `distinct@region` merges stored witnesses with **zero base scans at query time**.

> **v0.6.0-core — inform-and-serve reconciliation (Frame-QL Manual).** A B-anchor crossing (e.g. summing a stock over time) is now **served with a critical `b_anchor_crossing` disclosure** that names the alternative reducer — no longer refused. Refusals are reserved for the planner's static clarify/inform cases (fan-out across an M:N edge — now naming all three remedies; out-of-universe; unknown operator; type error). The engine, once handed an executable atom, never withholds on analytical grounds. Disclosures now carry a severity lattice (none<info<caution<critical) with a frame-level rollup. 57 checks across 7 suites pass.


The column-foundation implementation specified in **ADR-031** and the **Manifold object model** — multi-table, transport-based, validated against the real benchmark warehouse (299,934 transactions).

This is **not** the ADR-030 kernel. The kernel proved correctness *techniques* on a single denormalized table; Core implements the architecture: **the backend delivers single-table column-atoms and functional relationship-columns; the engine *transports* and relates them; the backend never joins.**

## The discipline, in code

- `connector.py` — **single-table delivery only.** `deliver_measure` (one-table group-by), `deliver_edge` (one-table key→key mapping), `deliver_base_rows` (one-table, for sketches). No SQL join is ever generated.
- `model.py` — the Manifold object model. Two layers: **universes** (populations) and the **coordinate DAG** (`FunctionalEdge`s). A rollup (`day→month`) and a relationship (`store→region`) are the *same* object — a functional edge the engine transports along, tagged with a lineage. The **B-anchor** blocks per-lineage.
- `engine.py` — the center. For `(measure, family-member) @ anchor`: find the functional path, **B-anchor-check every transport edge *and* every collapsed dimension**, resolve cheapest-faithful (cache vs delivery), **transport** the measure along functional edges (in-engine; no join pushdown), co-compute disclosure, cache.
- `planner.py` — provenance-blind. Parses logical `family.member @ anchor`, expands derived columns, **typechecks addressability — fan-out and out-of-universe are refused HERE, statically** — then assembles frames and folds disclosures.
- `disclosure.py` — the disclosure shadow-value and its sibling, the structured, dialog-capable `Refusal` (carries named alternatives).

## What `build_benchmark.py` proves (10/10, real data)

1. **Transport replaces the join** — `revenue@region` computed from a single-table `revenue@store` delivery + the `store→region` mapping, related *in the engine*; exact vs. ground truth; **zero joins pushed down**.
2. **Coordinate rollup is the same operation** — `revenue@cal.month` via the `day→month` mapping.
3. **★ Fan-out is inexpressible ★** — `revenue@category` is **refused** at the planner (`transaction↔category` is M:N); for contrast, the naive join *silently inflates revenue 1.44× — a 44% overcount*. The refusal names its alternatives (allocation = Pro; membership = rephrase). The flagship.
4. **B-anchor blocks per-lineage** — `level.sum@(region,day)` *works* (additive over the store axis); `level.sum@store` is *refused* (would sum a stock across days — non-reconciling over the calendar lineage). Same metric, opposite verdicts, by edge.
5. **Pre/post-agg boundary** — `aov = revenue/orders` computed post-aggregation = correct AOV (not the avg-of-avgs the shipped `monthly_avg_order_value` would give).
6. **Sketch reaggregation** — `visitors@cal.quarter` by HLL-merging per-day sketches; ≈ true distinct, vs. a naive sum-of-daily-distincts that overcounts.
7. **Out-of-universe** — `level@product` refused as a *distinct* reason (out of domain — undefined, not missing).

```
engine: 5 single-table deliveries, 5 transports, 1 cache-hit, 10 backend fetches (all single-table)
```

## Run

```bash
pip install --break-system-packages polars duckdb datasketches pyarrow
python3 build_benchmark.py     # 10 checks against the benchmark warehouse
```
(The script reads the warehouse parquets from the benchmark instance path; adjust `WAREHOUSE` if needed.)

## Ingest-first: the definition language

A written `MANIFOLD` definition (the `.cf` successor) parses to the Manifold object and is queryable end-to-end — no hand-construction. See `benchmark.cml` for the whole benchmark Manifold as text, and run:

```bash
python3 parse_benchmark.py     # parse benchmark.cml, then the SAME 10 checks on the PARSED Manifold
```

The parser (`parser.py`) reproduces the hand-built object with full structural parity, the corrected semantics survive the parse (`M_ANCHOR { }` → MCAR; `FAMILY { sum : additive BLOCKED { calendar } }` → per-member B-anchor), and publish-time well-formedness checks reject malformed definitions (impure predicate referencing a measure, unknown level/universe/column, etc.).

Grammar (statement-oriented; `#` comments; `{ }` blocks):
```
MANIFOLD <name> VERSION <n>
UNIVERSE <name> = <dim> * <dim> ... [WHERE <predicate>]
LEVEL <name> = <column> [BASE]
EDGE <from> -> <to> ALONG <lineage> VIA <table>(<from_col>, <to_col>)
RELATE <a> <-> <b> VIA <table> [NOTE "<text>"]
MEASURE <name> ON <universe> FROM <table> AS <agg>(<expr>)
MEASURE <name> ON <universe> FROM <table> VALUE <expr>
    [M_ANCHOR { <col>, ... }] [FAMILY { <agg> [: <tier>] [BLOCKED { <lineage>, ... }] ... }]
DERIVED <name> = <expr>
```

## Scope (Core, per ADR-031)

**Logical types, checked at compile time** (`types.py`, `types_demo.py`): every measure declares a **logical (Polars) dtype** and every operator carries a **type signature** (`sum: Numeric∪Duration→same`, `distinct: any→Int64`, `median: Numeric∪Temporal→same`, `last: T→T`). The *signature* is vocabulary the planner holds; the *mechanics* (witness/combine/deliver_sql) stay engine-side. So "operator not supported" and "wrong type for this operator" are **vocabulary errors caught at the planner, before the engine is ever asked** — proven by zero backend fetches on a refused frame. A static type-inference pass runs as a compile step ahead of resolution (`type_error` is its refusal reason, a sibling of unknown-operator). The **connector owns logical→physical**: a measure declares logical `Float64` over a raw column, and the connector supplies the `TRY_CAST` when the physical type is a dirty `VARCHAR` — so the author writes no casts, and a cast *failure* is a coverage fact at resolution, never a type error.

In scope and working: multi-table Manifolds, universes **with runtime predicate confinement**, the coordinate DAG, transport, measure-families with per-lineage B-anchors, **the operator registry (reaggregation as a monoid property, plus type signatures)**, **logical types with a compile-time planner typecheck**, derived columns, structured refusals, EXPLAIN, the definition-language parser + well-formedness checks, **the universe-support consistency check**, **the two projections as an enforced boundary**. Deliberately out (Pro): multiple backends/federation, cloud, custom operators/types, sophisticated optimization, **allocation** (the M:N split — Core catches the case rather than computing it).

**Two projections, enforced** (`projection.py`, `projection_demo.py`): one authored Manifold has two projections. The **planner** holds a `PlannerView` — vocabulary/shape only: logical names, the DAG *topology* (`frm→to` + lineage, no physical columns), family member *names*, derived formulas, M:N pairs for fan-out. The **engine** holds the full Manifold — sources, realizations, the universe predicate, missingness, costs, the operator registry. This makes "the planner cannot see provenance" *structural*: `home_table`, `pre_expr`, `realized_by`, `provider_table`, and the predicate are simply absent from the planner's object — no source string is reachable from it — yet it still does real work (fan-out and out-of-universe are refused from shape alone). The handoff down is a logical request `(measure, member, anchor)`; the return up is a frame + a `Disclosure` (caveats, not sources). Disclosures cross the boundary; provenance does not.

**Reaggregation is a monoid property of the operator** (`operators.py` — the registry, which is the Core/Pro extension point). An operator is reaggregable iff a possibly-enriched witness makes it a monoid; the engine reduces in *witness-space* and projects to the answer at the boundary: `sum`/`count` carry the value (combine `+`), `min`/`max` the value (combine min/max), `distinct` an HLL sketch (combine union), `last`/`first` the **(value, order_key)** pair (combine argmax/argmin — the order key is carried as the witness), and `median`/`mode` are **holistic** (no finite witness → recompute-from-base, never reduced). Two independent gates compose: **monoid-ness** (operator-level, *possible*) and the **B-anchor** (column-level, *permitted*). The headline (`holistic_demo.py`): `level.last@(store, cal.month)` *works* by carrying the day and reducing by argmax, while `level.sum@(store, cal.month)` *refuses* — same column, same target, the two gates disagree.

**Universe-support consistency** (`universe_check_demo.py`): a universe is one population, so every measure bound to it must reduce to the same base-point support (modulo declared coverage). The check reduces each measure to its universe and compares supports; a mismatch not explained by coverage flags a mis-declared universe. (Benchmark passes; a measure mis-sourced from a half-coverage table is flagged "50% short".) This is the **count-reducer instance** of a more general *path-independence* check — reduce a measure to the universe singleton along every anchoring and assert the reduced values agree — which becomes exercisable once a second coordinatization of an axis (e.g. a fiscal calendar forking from `day`) exists; with a single anchoring there is nothing to reconcile against.

**Universe-predicate confinement** (`confine_demo.py`): a measure bound to a predicated universe is confined to its valid points *at the base grain, at delivery, before aggregation* — logically prior to any query `WHERE` (domain before selection), inherited through cache and transport. A cross-table predicate like `day >= stores.opened_date` is evaluated *in the engine*: `opened_date` is delivered from `stores` (single table) and **broadcast** onto `(store, day)` by transport, then compared and filtered — **never a backend join**. The demo injects out-of-domain rows; the engine excludes them while an unconfined Manifold silently includes them.

Still thin in this build (next): the full cached-vs-stored cost search (resolution is correct but the cost model is minimal); hoisting the **B-anchor permission** refusal (`blocked_reaggregation`) from the engine to the planner (it is structural and belongs there, but it currently sits in the engine to preserve behaviour — moving it means the `PlannerView` carries family-member shape); automated Discovery (the parser consumes a written definition; generating one from a warehouse is the layer above).

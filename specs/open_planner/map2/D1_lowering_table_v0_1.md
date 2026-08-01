# MAP-2 · D1 — The Lowering Table (v0.1)
### Certified lowerings of the eight meaning-nodes onto Substrait container-Rels

*Deliverable D1 of the Beat-2 charter (`map2_mapping_study_charter_v0_1.md`). CC proposes; the desk
adjudicates the verdicts. The left column is **attested by execution** — produced by
`specs/open_planner/map2/trace_nodes.py`, which wraps Polars' own methods and records every operation
the shipped engine issues while serving a covering ask set. An empty cell is a finding; a guessed cell
is a violation. No cell in the *Polars ops (attested)* column was written from memory.*

## Version pins (part of the table, per charter §4)

| thing | pin | why it matters |
|---|---|---|
| **Substrait** | **0.46.0** (`plan.version`, emitted by the producer) | the Rel vocabulary and function URIs are version-scoped; drift across versions is a **finding**, not a surprise (§8) |
| columna-core | **0.14.0** (`0.14.0-core`) | the engine whose execution is traced; node→method map is A1 §1.1 pinned to this source |
| Polars | **1.43.1** | the reference-oracle engine; the ops in the left column are its methods |
| producer (study) | `ibis-substrait` 4.0.1 → `substrait` proto 0.16.0 | builds the Substrait plan for D4 |
| consumer (study) | `pyarrow.substrait` / Acero (pyarrow 25.0.0) | executes the plan — **see the pre-D4 flag on DuckDB below** |

## Attestation summary (from `fixtures/d1_polars_trace.json`)

Nine asks, run **cold** (engine cache cleared before each), covering all eight nodes plus the two named
compositions. **Ninth-node candidates: 0** — every Polars operation the engine issued was accounted for
by one of the eight nodes (the connector's base scan is a duckdb read *below* Polars; `ORDER BY` is an
envelope clause, tracked separately). This is IR closure re-confirmed at the *Polars-operation* level,
one layer below beat-1's node-set closure.

Attested per-node Polars-op profile (counts across the ask set):

```
ANCHOR     (no Polars op — output grain is a declaration, realized as the group keys of the terminal REDUCE)
CARVE      filter ×1            (+ the connector duckdb base scan, below Polars — see note F-b)
COLUMN     join ×1  group_by ×1  agg ×1  select ×13  rename ×13
TRANSPORT  join ×7  group_by ×7  agg ×7  rename ×7
CROSS      join ×5  group_by ×1  agg ×1  unique ×3  with_columns ×5  select ×5  sort ×2  rename ×4
REDUCE     group_by ×1  agg ×1  select ×1
ALIGN      join ×1  rename ×21
DERIVE     join ×1  with_columns ×1  select ×1
ORDER(env) sort ×9             (envelope clause — NOT one of the eight nodes)
```

## The table

Verdicts (proposed): **PR** = CERTIFIABLE-PER-RULE (prove once per backend, reuse) · **PS** =
CERTIFIABLE-PER-SHAPE (per-plan-shape proof) · **NL** = NOT-LOWERABLE (stays home; the pushdown
boundary lands here). Every verdict carries its one-sentence reason in the per-node detail below.

| # | node | Polars ops (attested) | proposed Rel composition (Substrait 0.46.0) | what the Rels **lose** | cargo required | verdict (proposed) |
|---|---|---|---|---|---|---|
| 1 | **ANCHOR**(coords) | (declaration; = terminal group keys) | grouping keys of the terminal `AggregateRel` + `RelRoot.names` | that these fields are *anchor coordinates* (grain) vs value series; the (coords, **universe**) identity; lattice order | `(coords, universe)` grain identity; which output fields are anchor dims | **PR** |
| 2 | **CARVE**(universe, pred?) | `filter` + connector duckdb scan | `ReadRel` (named/virtual table) [ + `FilterRel` for a predicate ] | that the read is a **universe** with a *basis* (events/spine/product/registry) and its absence-law (zero vs gap); that the filter is a lawful population restriction, not an arbitrary mask | universe id + **basis** (B3 absence law); resolved (Manifold, version); predicate provenance | **PR** |
| 3 | **COLUMN**(name, measure_ref, family) | `join` `group_by` `agg` `select` `rename` | `ProjectRel` (measure, alias) over the `ReadRel`; `AggregateRel` for the family's monoid delivery when the root is finer | that the projected column is a **measure of a family** (default reducer, fertile/mule); the binding of `measure_ref` to the ask's measure atom (**Attack A**); the V/M/B anchors | measure_ref bound to the ask atom; family (default op, fertility); V/M/B anchors | **PR** |
| 4 | **TRANSPORT**(frm→to, lineage) | `join` `group_by` `agg` `rename` | `JoinRel` (INNER, on the from-key, against the hierarchy table) + `AggregateRel` to the coarser grain; **or** `ProjectRel` when the coarser level is a 1:1 functional attribute (dependent attach) | **that the JoinRel rides a *corroborated functional edge*** — a bare `JoinRel` on a non-functional key silently **fans out**; the whole faithfulness of TRANSPORT (no fan-out) is the edge's adjudication, which the Rel cannot see; the edge verdict and lineage | edge `(frm, to, lineage)` + certificate **verdict** (VERIFIED/CORROBORATED/CONTRADICTED); the functionality guarantee | **PR** (faithful *only under* the certified-edge precondition — the study's honest center) |
| 5 | **CROSS**(relate, face) | `join` `unique` `with_columns` `select` `sort` `group_by` `agg` `rename` | touch → `JoinRel`(M:N)+`AggregateRel`; assign → `JoinRel`+`FilterRel`(top-per-member)+`AggregateRel`; alloc → `JoinRel`+`ProjectRel`(×normalized weight)+`AggregateRel` | **the face LAW has no Rel vocabulary**: a fanning `JoinRel` *is* the forbidden double-count — the Rel cannot say the over-count is *licensed & disclosed* (touch), or that the pick is the *adjudicated unique top* (assign), or that the weights are a *partition of unity that reconciles* (alloc); the reconciliation certificate and the shadow are arithmetic the Rels perform but do not know they owe | face scheme + adjudication (touch over_count; assign driver+ORDER+shadow `memberships_unrepresented`; alloc driver + reconciliation badge); the disclosure obligations (F5) | **PS** (arithmetic per-shape; **disclosure minting is NOT delegable** — custody law) |
| 6 | **REDUCE**(family_op @ coord) | `group_by` `agg` `select` | `AggregateRel`, grouping keys = anchor coords, measure = the family function | **non-monoidal aggregators**: `AggregateRel` has sum/count/min/max, but **mean must lower as (sum, count) then divide** (the mean-of-means theorem is a *lowering constraint*, not just an attack); it does not know a reducer is a **mule** vs fertile, nor the **B-anchor** it may not cross | family law (fertile/mule); sufficient-statistics decomposition (mean→(sum,count)); B-anchor | **PR** monoids & mean-via-(sum,count); **NL** at v1 for **sketch distinct** (engine-specific HLL state) and **exact median/mode** (holistic, no fertile carrier) |
| 7 | **ALIGN**(shared_anchor) | `join` `rename` | `JoinRel` (**FULL OUTER**, on the anchor coordinates) juxtaposing the per-column frames | a FULL-OUTER null does not carry *why*: an events-absence **zero** and a spine **gap** and an alignment miss are three different nulls the Rel renders identically (A1 §1.1 node 7's locally-scoped null semantics) | per-column `(anchor, universe)` so each null reads against its own basis | **PR** |
| 8 | **DERIVE**(expr over columns) | `join` `with_columns` `select` | `ProjectRel` with a scalar arithmetic expression over the aligned columns | a Substrait `divide`/`subtract` is just arithmetic — it does not carry the **co-anchoring / co-universality** precondition (the `cross_universe` category error is invisible), and its null/zero semantics are **drift-prone** across engines (Q5) | co-anchoring + co-universality attestation; the map function's pinned null/zero/rounding semantics | **PR** if engine-stable; **PS**/drift-flagged for functions whose semantics diverge (Q5) |
| C1 | **COMPOSITION — TRANSPORT-shaped** (`sum(revenue @ {store*product*cal.month}) AT {cal.month}`) | `join` `group_by` `agg` (transport) → `group_by` `agg` (reduce) | `JoinRel`(calendar) + `AggregateRel`(→ store*product*month) + `AggregateRel`(→ month) | the intermediate **pin grain** identity; the edge verdict; the sum's extensivity/B-anchor | intermediate `(grain)`; edge verdict; family | **PR** (monoid sum through a corroborated edge — the **D4 pilot target**) |
| C2 | **COMPOSITION — full spine** CARVE→COLUMN→TRANSPORT→REDUCE (`revenue AT {region}`) | `ReadRel`→`Project`→`Join`→`Aggregate` (all attested) | `ReadRel`(transactions) + `ProjectRel`(revenue) + `JoinRel`(stores, store→region) + `AggregateRel`(sum → region) | the full stack of losses above, in one plan; **plus** that the *seam between nodes preserves the grain* | universe basis + measure_ref + edge verdict + family, threaded | **PR** *iff* each node is PR **and** the inter-node seam preserves grain (the study's core composition claim) |

## Per-node detail — the verdict reasons (one sentence each) and the loss, expanded

**1 · ANCHOR — PR.** The output grain is a declaration, not an operation; it is realized as the terminal
`AggregateRel`'s grouping keys and the `RelRoot` names. *Reason:* a naming/grouping declaration lowers
identically every time; the only thing the Rels drop — that these fields are anchor coordinates on a
declared universe — is recorded once as cargo.

**2 · CARVE — PR.** A `ReadRel` (optionally a `FilterRel`) faithfully realizes population selection.
*Reason:* the read itself is a faithful table scan; the **basis** (events/spine/product/registry) and its
absence-law are not expressible in `ReadRel` and ride as cargo — a per-rule obligation, not a per-plan one.

**3 · COLUMN — PR.** `ProjectRel` + the family's monoid `AggregateRel` deliver the measure. *Reason:* the
projection is faithful, but **Attack A** proved the load-bearing loss: no Rel binds `measure_ref` to the
ask's measure atom (revenue-not-units_sold), so the binding is a mandatory cargo obligation checked in
the TCB.

**4 · TRANSPORT — PR, conditional.** `JoinRel`+`AggregateRel` (or a `ProjectRel` attach). *Reason:* the
composition is a faithful realization **only under the certified-edge precondition** — a bare `JoinRel`
on a non-functional key fans out, which is precisely the double-count the framework forbids; the edge's
functionality verdict is invisible in Substrait and is the cargo the certificate exists to carry. This is
the row the charter calls the study's honest center (Q2).

**5 · CROSS — PS, with a non-delegable core.** touch/assign/alloc each map to a Rel composition, but the
**face law itself has no Rel vocabulary**. *Reason:* the Rels can perform the join-multiply, the
top-per-member restriction, and the weighted split, but they cannot *mint* the over-count disclosure, the
`memberships_unrepresented` shadow, or the reconciliation badge — those are minted at our door (custody
law), so CROSS lowers **per-shape** for the arithmetic and its disclosure obligation stays home. (Expected
hard case, charter Q3. `assign`'s top-per-member may further need a window Substrait 0.46.0 expresses
awkwardly — flagged for D4/D5.)

**6 · REDUCE — split verdict.** *Reason:* monoid reducers (sum/count/min/max) lower to `AggregateRel`
**PR**; `mean` lowers **PR** *only* via its sufficient-statistics decomposition `(sum, count)` then a
`ProjectRel` divide — the mean-of-means theorem promoted from attack to **lowering constraint**;
sketch-based `approx_distinct` (engine-specific HLL/witness state) and exact `median`/`mode` (holistic, no
fertile carrier) are **NL at v1** — they stay home and the pushdown boundary lands at the reducer.

**7 · ALIGN — PR.** A FULL-OUTER `JoinRel` on the anchor coordinates realizes the juxtaposition. *Reason:*
faithful in shape; the single loss is null *meaning* — the Rel cannot distinguish an events-zero from a
spine-gap from an alignment-miss, so each column's `(anchor, universe)` rides as cargo to disambiguate.

**8 · DERIVE — PR / PS.** `ProjectRel` with a scalar expression realizes the arithmetic. *Reason:*
faithful when the map function is engine-stable; the loss is the co-universality precondition (invisible
to a Substrait `divide`) plus **engine drift** (Q5) on null/zero/rounding semantics — drift-prone
functions drop to **PS** and force per-backend proof.

## Findings surfaced by building D1 (feed D5)

- **F-a · Node boundaries are LOGICAL, not physical in the engine.** `_deliver_and_transport_monoid`
  fuses COLUMN delivery + TRANSPORT + REDUCE into one method issuing `join`+`group_by`+`agg` together;
  the trace separates them only where the engine itself calls a distinct method (`_transport_reduce`,
  `reduce_series_to_anchor`). *Consequence for lowering:* one engine method emits what a lowering must
  split into `JoinRel` (TRANSPORT) + `AggregateRel` (REDUCE) with a certified seam between — the node
  seam is a lowering obligation the engine currently discharges implicitly.
- **F-b · CARVE's base scan is below Polars.** The universe/population read is a duckdb query →
  `pl.from_arrow`, not a Polars method, so it appears in the trace only as the downstream `filter`. It
  lowers cleanly to `ReadRel` (a table scan is the one thing Substrait expresses natively) — but the
  attestation of the scan lives in the connector, not the Polars op-log; noted so the left column's
  single `filter` is not misread as CARVE's whole footprint.
- **F-c · `ORDER BY` is an envelope clause, not a node.** Every ask emitted one `sort` at
  `planner.py:run`; ORDER/LIMIT are envelope surface (they lower to `SortRel`/`FetchRel`) and are
  correctly **not** counted among the eight IR nodes — and are **not** ninth-node candidates.
- **F-d · The WHERE→filter (`_confine`) path is under-exercised by the Cascadia serving corpus.** Every
  `WHERE` variant attempted either hit a region binder error or a `filter_unreachable` clarify, so CARVE's
  predicate-filter sub-path was exercised only once (the align ask). The `ReadRel`+`FilterRel` proposal
  stands on the code path (engine.py `_confine`), but its execution attestation is thin → a D5 row asks
  for a fixture with a reachable predicate before CARVE's filter lowering is certified.

*— CC, D1 v0.1, for desk adjudication of the verdict column. The Rel compositions are proposals grounded
in the Substrait 0.46.0 Rel set; the pilot (D4) will attest C1 end-to-end before any verdict is treated
as more than proposed.*

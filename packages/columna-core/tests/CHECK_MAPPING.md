# WP-0 check → test-id mapping

All 124 demo `check()` assertions are mirrored 1:1 as pytest items.

- **Fixture-run (104)** — against `tests/fixtures/mini_warehouse`, run in CI.
- **Warehouse-marked (20)** — `@pytest.mark.warehouse`; always collected, skipped in CI unless `COLUMNA_BENCH_WAREHOUSE` is set (10 checks × 2 manifolds: hand-built + parsed).


## `demos/coanchor_demo.py` → `tests/test_coanchor.py`  (17 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | revenue / orders (both ON transactions) -> SERVE (one population) | `test_check[revenue / orders (both ON transactions) -> SERVE (one population)]` |
| 2 | revenue / level.last (transactions vs store_days) -> CLARIFY (ambiguous population) | `test_check[revenue / level.last (transactions vs store_days) -> CLARIFY (ambiguous population)]` |
| 3 | the clarify names BOTH candidate populations (no silent guess) | `test_check[the clarify names BOTH candidate populations (no silent guess)]` |
| 4 | frame-level outcome rolls up to CLARIFY | `test_check[frame-level outcome rolls up to CLARIFY]` |
| 5 | the clarify is a VALUE (Outcome), not an Exception — a consumer receives data, not a throw | `test_check[the clarify is a VALUE (Outcome), not an Exception — a consumer receives data, not a throw]` |
| 6 | the cross-universe ratio is caught STATICALLY (never reaches the engine) | `test_check[the cross-universe ratio is caught STATICALLY (never reaches the engine)]` |
| 7 | revenue / 1000 -> SERVE (constant denominator, one population) | `test_check[revenue / 1000 -> SERVE (constant denominator, one population)]` |
| 8 | revenue and level.last as SEPARATE columns -> both served (no clarify) | `test_check[revenue and level.last as SEPARATE columns -> both served (no clarify)]` |
| 9 | frame carries the multi-universe population caveat (served, not clarified) | `test_check[frame carries the multi-universe population caveat (served, not clarified)]` |
| 10 | pin consistent with both operands -> SERVE (revenue/orders ON transactions) | `test_check[pin consistent with both operands -> SERVE (revenue/orders ON transactions)]` |
| 11 | cross-universe ratio pinned to numerator's universe -> REFUSE (denominator out-of-universe) | `test_check[cross-universe ratio pinned to numerator's universe -> REFUSE (denominator out-of-universe)]` |
| 12 | cross-universe ratio pinned to denominator's universe -> REFUSE (numerator out-of-universe) | `test_check[cross-universe ratio pinned to denominator's universe -> REFUSE (numerator out-of-universe)]` |
| 13 | the SAME ratio WITHOUT a pin still CLARIFIES (D5 unchanged; the pin is what resolves it) | `test_check[the SAME ratio WITHOUT a pin still CLARIFIES (D5 unchanged; the pin is what resolves it)]` |
| 14 | a measure pinned to its own universe -> SERVE (level.last ON store_days) | `test_check[a measure pinned to its own universe -> SERVE (level.last ON store_days)]` |
| 15 | a measure pinned to a FOREIGN universe -> REFUSE (out-of-universe for that population) | `test_check[a measure pinned to a FOREIGN universe -> REFUSE (out-of-universe for that population)]` |
| 16 | an unknown pinned universe -> ERROR (not a declared universe) | `test_check[an unknown pinned universe -> ERROR (not a declared universe)]` |
| 17 | two-universe frame pinned -> off-universe column refuses, on-universe serves, caveat resolved | `test_check[two-universe frame pinned -> off-universe column refuses, on-universe serves, caveat resolved]` |

## `demos/confine_demo.py` → `tests/test_confine.py`  (12 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | WITH predicate: engine EXCLUDES the out-of-domain stock (matches confined truth) | `test_check[WITH predicate: engine EXCLUDES the out-of-domain stock (matches confined truth)]` |
| 2 | WITHOUT predicate: engine SILENTLY INCLUDES the bogus stock (the failure confinement prevents) | `test_check[WITHOUT predicate: engine SILENTLY INCLUDES the bogus stock (the failure confinement prevents)]` |
| 3 | confinement removed exactly the injected out-of-domain mass | `test_check[confinement removed exactly the injected out-of-domain mass]` |
| 4 | numeric predicate 'qty >= 10' confines (string literal coerced to Int64; was a ComputeError before) | `test_check[numeric predicate 'qty >= 10' confines (string literal coerced to Int64; was a ComputeError before)]` |
| 5 | date predicate 'd >= 2024-06-01' confines (string literal coerced to Date) | `test_check[date predicate 'd >= 2024-06-01' confines (string literal coerced to Date)]` |
| 6 | AND predicate 'qty >= 10 AND qty < 25' confines to the intersection | `test_check[AND predicate 'qty >= 10 AND qty < 25' confines to the intersection]` |
| 7 | single-grain table ('stores') resolves unambiguously to its grain | `test_check[single-grain table ('stores') resolves unambiguously to its grain]` |
| 8 | multi-grain 'geo' pinned by a store-grain frame -> store | `test_check[multi-grain 'geo' pinned by a store-grain frame -> store]` |
| 9 | multi-grain 'geo' pinned by a region-grain frame -> region | `test_check[multi-grain 'geo' pinned by a region-grain frame -> region]` |
| 10 | multi-grain 'geo', BOTH levels present -> CLARIFY (ambiguous; engine reports, planner classifies) | `test_check[multi-grain 'geo', BOTH levels present -> CLARIFY (ambiguous; engine reports, planner classifies)]` |
| 11 | multi-grain 'geo', no frame to pin it -> CLARIFY (ambiguous) | `test_check[multi-grain 'geo', no frame to pin it -> CLARIFY (ambiguous)]` |
| 12 | attribute table with no providing edge -> ERROR (vocabulary, not an analytical verdict) | `test_check[attribute table with no providing edge -> ERROR (vocabulary, not an analytical verdict)]` |

## `demos/hll_case_study_demo.py` → `tests/test_hll_case_study.py`  (20 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | planner.py + projection.py contain ZERO sketch/HLL references | `test_check[planner.py + projection.py contain ZERO sketch/HLL references]` |
| 2 | hll_count is a REDUCER (deliver: any → HLLSketch) | `test_check[hll_count is a REDUCER (deliver: any → HLLSketch)]` |
| 3 | hll_merge is a REDUCER monoid (combine: HLLSketch → HLLSketch) | `test_check[hll_merge is a REDUCER monoid (combine: HLLSketch → HLLSketch)]` |
| 4 | hll_estimate is a MAP (project: HLLSketch → Int64) | `test_check[hll_estimate is a MAP (project: HLLSketch → Int64)]` |
| 5 | HLLSketch(p) is a recognized parametric type | `test_check[HLLSketch(p) is a recognized parametric type]` |
| 6 | publish() materialized witnesses (one scan per base dim) | `test_check[publish() materialized witnesses (one scan per base dim)]` |
| 7 | witness stored at base 'store' AND 'day' (serves either rollup axis) | `test_check[witness stored at base 'store' AND 'day' (serves either rollup axis)]` |
| 8 | distinct@region did ZERO base scans at query time (served from witnesses) | `test_check[distinct@region did ZERO base scans at query time (served from witnesses)]` |
| 9 | witness-merged distinct@region ≈ exact distinct (within 5%) | `test_check[witness-merged distinct@region ≈ exact distinct (within 5%)]` |
| 10 | an UN-published server does a base scan for the same query (the witness made the difference) | `test_check[an UN-published server does a base scan for the same query (the witness made the difference)]` |
| 11 | '+' REJECTS a raw HLLSketch (a sketch is not a number) | `test_check['+' REJECTS a raw HLLSketch (a sketch is not a number)]` |
| 12 | hll_estimate ACCEPTS HLLSketch | `test_check[hll_estimate ACCEPTS HLLSketch]` |
| 13 | hll_merge preserves precision (HLLSketch(12) → HLLSketch(12)) | `test_check[hll_merge preserves precision (HLLSketch(12) → HLLSketch(12))]` |
| 14 | dtype_in: sketch ∈ SKETCH family but ∉ NUMERIC | `test_check[dtype_in: sketch ∈ SKETCH family but ∉ NUMERIC]` |
| 15 | same-precision sketches merge | `test_check[same-precision sketches merge]` |
| 16 | mismatched-precision merge is REFUSED as a type error | `test_check[mismatched-precision merge is REFUSED as a type error]` |
| 17 | distinct@region carries an APPROXIMATION caveat | `test_check[distinct@region carries an APPROXIMATION caveat]` |
| 18 | the disclosed error equals rse(precision=12) | `test_check[the disclosed error equals rse(precision=12)]` |
| 19 | the caveat names the sketch type HLLSketch(12) | `test_check[the caveat names the sketch type HLLSketch(12)]` |
| 20 | at precision 14 the disclosed error is tighter and equals rse(14) | `test_check[at precision 14 the disclosed error is tighter and equals rse(14)]` |

## `demos/holistic_demo.py` → `tests/test_holistic.py`  (5 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | level.last@(store,cal.month) == arg_max(level, day) per (store,month) [period-end snapshot] | `test_check[level.last@(store,cal.month) == arg_max(level, day) per (store,month) [period-end snapshot]]` |
| 2 | level.sum@(store,cal.month) is SERVED with a CRITICAL B-anchor-crossing disclosure (inform-and-serve) — not refused | `test_check[level.sum@(store,cal.month) is SERVED with a CRITICAL B-anchor-crossing disclosure (inform-and-serve) — not refused]` |
| 3 | the served crossing names the alternative reducer ('.last') as its remedy | `test_check[the served crossing names the alternative reducer ('.last') as its remedy]` |
| 4 | median@cal.month == true median(amount) per month (recomputed from base) | `test_check[median@cal.month == true median(amount) per month (recomputed from base)]` |
| 5 | a median-of-daily-medians DISAGREES with the true monthly median (so reduction is invalid) | `test_check[a median-of-daily-medians DISAGREES with the true monthly median (so reduction is invalid)]` |

## `demos/locus_demo.py` → `tests/test_locus.py`  (11 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | level.sum@store is SERVED (not refused) with a critical b_anchor_crossing | `test_check[level.sum@store is SERVED (not refused) with a critical b_anchor_crossing]` |
| 2 | the crossing names the reconciling alternative (.last) | `test_check[the crossing names the reconciling alternative (.last)]` |
| 3 | engine.resolve('level','sum',@store) returns a disclosure with NO crossing (engine doesn't detect) | `test_check[engine.resolve('level','sum',@store) returns a disclosure with NO crossing (engine doesn't detect)]` |
| 4 | the planner's served result DOES carry it (detection is the planner's job now) | `test_check[the planner's served result DOES carry it (detection is the planner's job now)]` |
| 5 | plan() did ZERO backend fetches | `test_check[plan() did ZERO backend fetches]` |
| 6 | plan() surfaces the would-be critical crossing before any execution | `test_check[plan() surfaces the would-be critical crossing before any execution]` |
| 7 | plan PREDICTS what run SERVES (same crossing detail) — contract unchanged either way | `test_check[plan PREDICTS what run SERVES (same crossing detail) — contract unchanged either way]` |
| 8 | visitors.distinct@region plan shows the HLL approximation caveat, zero fetches | `test_check[visitors.distinct@region plan shows the HLL approximation caveat, zero fetches]` |
| 9 | revenue.sum@region plans CLEAN (no crossing) | `test_check[revenue.sum@region plans CLEAN (no crossing)]` |
| 10 | level.sum@product is still REFUSED (out_of_universe) at plan time | `test_check[level.sum@product is still REFUSED (out_of_universe) at plan time]` |
| 11 | all of (5) touched zero backend data | `test_check[all of (5) touched zero backend data]` |

## `demos/operator_umbrella_demo.py` → `tests/test_operator_umbrella.py`  (10 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | registry holds reducers, scans, AND maps under one roof | `test_check[registry holds reducers, scans, AND maps under one roof]` |
| 2 | the planner's shape-view carries each operator's KIND (so it can route) but no mechanics | `test_check[the planner's shape-view carries each operator's KIND (so it can route) but no mechanics]` |
| 3 | the SCAN cumsum(revenue.sum)@cal.month == DuckDB running SUM() OVER(ORDER BY month) | `test_check[the SCAN cumsum(revenue.sum)@cal.month == DuckDB running SUM() OVER(ORDER BY month)]` |
| 4 | the reducer and map columns in the same frame are unaffected (revenue.sum exact) | `test_check[the reducer and map columns in the same frame are unaffected (revenue.sum exact)]` |
| 5 | lag(revenue.sum,n=1) shifts the series by one month (first month has no predecessor) | `test_check[lag(revenue.sum,n=1) shifts the series by one month (first month has no predecessor)]` |
| 6 | pct_change(revenue.sum) is month-over-month growth (first is null) | `test_check[pct_change(revenue.sum) is month-over-month growth (first is null)]` |
| 7 | cumsum(revenue.sum)@region has no temporal axis -> refused (clarify), names by= | `test_check[cumsum(revenue.sum)@region has no temporal axis -> refused (clarify), names by=]` |
| 8 | the scan is SERVED (not refused) and carries the underlying sum's critical crossing | `test_check[the scan is SERVED (not refused) and carries the underlying sum's critical crossing]` |
| 9 | rolling_sum is in the registry (planner knows it) but in_core=False -> Pro clarification | `test_check[rolling_sum is in the registry (planner knows it) but in_core=False -> Pro clarification]` |
| 10 | a measure whose family declares a scan ('cumsum') is rejected at publish | `test_check[a measure whose family declares a scan ('cumsum') is rejected at publish]` |

## `demos/projection_demo.py` → `tests/test_projection.py`  (16 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | planner's measure shape has no 'home_table' | `test_check[planner's measure shape has no 'home_table']` |
| 2 | planner's measure shape has no 'pre_expr' | `test_check[planner's measure shape has no 'pre_expr']` |
| 3 | planner's measure shape has no 'distinct_col'/'missingness' | `test_check[planner's measure shape has no 'distinct_col'/'missingness']` |
| 4 | planner's universe shape has no 'predicate' (confinement is engine-only) | `test_check[planner's universe shape has no 'predicate' (confinement is engine-only)]` |
| 5 | planner's measure shape keeps vocabulary it DOES need (universe + family names) | `test_check[planner's measure shape keeps vocabulary it DOES need (universe + family names)]` |
| 6 | a shape edge has frm/to/lineage | `test_check[a shape edge has frm/to/lineage]` |
| 7 | a shape edge has NO 'frm_col'/'to_col'/'provider_table' | `test_check[a shape edge has NO 'frm_col'/'to_col'/'provider_table']` |
| 8 | source tables / physical columns / pre-exprs are absent from the planner's view | `test_check[source tables / physical columns / pre-exprs are absent from the planner's view]` |
| 9 | (sanity) the LOGICAL vocabulary the planner needs IS present | `test_check[(sanity) the LOGICAL vocabulary the planner needs IS present]` |
| 10 | fan-out (revenue@category) refused by the planner from topology | `test_check[fan-out (revenue@category) refused by the planner from topology]` |
| 11 | out-of-universe (level@product) refused by the planner from shape | `test_check[out-of-universe (level@product) refused by the planner from shape]` |
| 12 | a faithful frame (revenue@region) still resolves | `test_check[a faithful frame (revenue@region) still resolves]` |
| 13 | the engine's Manifold knows level's source table is 'eom_inventory' | `test_check[the engine's Manifold knows level's source table is 'eom_inventory']` |
| 14 | measure shape carries the declared logical_type (vocabulary) | `test_check[measure shape carries the declared logical_type (vocabulary)]` |
| 15 | operator shape carries the signature (accepts / out_rule) | `test_check[operator shape carries the signature (accepts / out_rule)]` |
| 16 | operator shape has NO mechanics (deliver_sql / combine / witness) | `test_check[operator shape has NO mechanics (deliver_sql / combine / witness)]` |

## `demos/types_demo.py` → `tests/test_types.py`  (10 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | amount (physical DOUBLE) realizes as-is for logical Float64 | `test_check[amount (physical DOUBLE) realizes as-is for logical Float64]` |
| 2 | v (physical VARCHAR) realizes via TRY_CAST for logical Float64 | `test_check[v (physical VARCHAR) realizes via TRY_CAST for logical Float64]` |
| 3 | a cast FAILURE is a coverage fact, not a type error (uncastable rows are counted, not fatal) | `test_check[a cast FAILURE is a coverage fact, not a type error (uncastable rows are counted, not fatal)]` |
| 4 | revenue.stddev refused as operator-not-supported (vocabulary, not data) | `test_check[revenue.stddev refused as operator-not-supported (vocabulary, not data)]` |
| 5 | NO backend fetch happened — refused before the engine | `test_check[NO backend fetch happened — refused before the engine]` |
| 6 | revenue / cust_region.mode refused as type_error (mode yields Categorical, '/' needs numeric) | `test_check[revenue / cust_region.mode refused as type_error (mode yields Categorical, '/' needs numeric)]` |
| 7 | NO backend fetch happened — type error caught before the engine | `test_check[NO backend fetch happened — type error caught before the engine]` |
| 8 | the categorical measure itself (cust_region.mode) still resolves fine | `test_check[the categorical measure itself (cust_region.mode) still resolves fine]` |
| 9 | sum on a Categorical measure is rejected at publish | `test_check[sum on a Categorical measure is rejected at publish]` |
| 10 | an unknown operator in a family is rejected at publish | `test_check[an unknown operator in a family is rejected at publish]` |

## `demos/universe_check_demo.py` → `tests/test_universe_check.py`  (3 checks, fixture)

| # | demo check | test id |
|---|---|---|
| 1 | benchmark is universe-consistent (transactions' measures reconcile to one support) | `test_check[benchmark is universe-consistent (transactions' measures reconcile to one support)]` |
| 2 | mis-declared measure is FLAGGED — supports on store_days don't reconcile | `test_check[mis-declared measure is FLAGGED — supports on store_days don't reconcile]` |
| 3 | the flag names a base-point support mismatch (different populations) | `test_check[the flag names a base-point support mismatch (different populations)]` |

## `demos/build_benchmark.py` → `tests/test_benchmark_warehouse.py`  (10 checks, @warehouse)

| # | demo check | test id |
|---|---|---|
| 1 | revenue@region == ground truth (transported store→region, no join pushdown) | `test_proof[revenue@region == ground truth (transported store→region, no join pushdown)]` |
| 2 | revenue@cal.month == ground truth (transported day→month) | `test_proof[revenue@cal.month == ground truth (transported day→month)]` |
| 3 | revenue@category is REFUSED (non-functional M:N transport) | `test_proof[revenue@category is REFUSED (non-functional M:N transport)]` |
| 4 | (for contrast) the naive join silently inflates revenue | `test_proof[(for contrast) the naive join silently inflates revenue]` |
| 5 | level.sum@(region,day) is CLEAN — additive over the store axis (no crossing) | `test_proof[level.sum@(region,day) is CLEAN — additive over the store axis (no crossing)]` |
| 6 | level.sum@store is SERVED with a CRITICAL B-anchor crossing disclosure (summing a stock across days) — inform-and-serve, not refused | `test_proof[level.sum@store is SERVED with a CRITICAL B-anchor crossing disclosure (summing a stock across days) — inform-and-serve, not refused]` |
| 7 | aov@cal.month == sum(amount)/count (correct AOV) | `test_proof[aov@cal.month == sum(amount)/count (correct AOV)]` |
| 8 | HLL-merged visitors@quarter ≈ true distinct (within 5%) | `test_proof[HLL-merged visitors@quarter ≈ true distinct (within 5%)]` |
| 9 | (naive sum-of-daily-distincts would overcount) | `test_proof[(naive sum-of-daily-distincts would overcount)]` |
| 10 | level.sum@product is REFUSED as out_of_universe (undefined, not missing) | `test_proof[level.sum@product is REFUSED as out_of_universe (undefined, not missing)]` |

## `demos/parse_benchmark.py` → `tests/test_parse_benchmark_warehouse.py`  (10 checks, @warehouse)

| # | demo check | test id |
|---|---|---|
| 1 | revenue@region == ground truth (transported store→region, no join pushdown) | `test_proof[revenue@region == ground truth (transported store→region, no join pushdown)]` |
| 2 | revenue@cal.month == ground truth (transported day→month) | `test_proof[revenue@cal.month == ground truth (transported day→month)]` |
| 3 | revenue@category is REFUSED (non-functional M:N transport) | `test_proof[revenue@category is REFUSED (non-functional M:N transport)]` |
| 4 | (for contrast) the naive join silently inflates revenue | `test_proof[(for contrast) the naive join silently inflates revenue]` |
| 5 | level.sum@(region,day) is CLEAN — additive over the store axis (no crossing) | `test_proof[level.sum@(region,day) is CLEAN — additive over the store axis (no crossing)]` |
| 6 | level.sum@store is SERVED with a CRITICAL B-anchor crossing disclosure (summing a stock across days) — inform-and-serve, not refused | `test_proof[level.sum@store is SERVED with a CRITICAL B-anchor crossing disclosure (summing a stock across days) — inform-and-serve, not refused]` |
| 7 | aov@cal.month == sum(amount)/count (correct AOV) | `test_proof[aov@cal.month == sum(amount)/count (correct AOV)]` |
| 8 | HLL-merged visitors@quarter ≈ true distinct (within 5%) | `test_proof[HLL-merged visitors@quarter ≈ true distinct (within 5%)]` |
| 9 | (naive sum-of-daily-distincts would overcount) | `test_proof[(naive sum-of-daily-distincts would overcount)]` |
| 10 | level.sum@product is REFUSED as out_of_universe (undefined, not missing) | `test_proof[level.sum@product is REFUSED as out_of_universe (undefined, not missing)]` |

**Total: 124 checks mapped (104 fixture + 20 warehouse).**

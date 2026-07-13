# The Silent Failure Atlas: A Taxonomy of Silent Analytical Failures in Data Analysis

**Huayin Wang** · Version 1.3 · June 2026 · License: CC BY 4.0 · DOI: 10.5281/zenodo.20762839

## Abstract

When a question is asked of data, the most dangerous outcome is not an error message but a plausible, confidently delivered, wrong or misleading number. We call this a *silent analytical failure*: the query runs, a result returns, and nothing in the mechanics signals that the result should not be trusted. The rise of AI analytics agents makes this failure mode urgent — agents answer at scale, with fluency that masks unreliability, over warehouses whose defects and semantic hazards they were never trained to notice. Yet no unified collection of silent analytical failure modes exists: the knowledge is fragmented across OLAP summarizability theory, missing-data statistics, dimensional-modeling practitioner lore, data-observability engineering, spreadsheet-error research, and the query-diagnostic practice of working analysts, each covering one province of the territory. This paper compiles the Silent Failure Atlas: 67 failure modes organized into 9 families across a six-layer model of where failures live — question interpretation, semantic contract, data, computation grammar, query execution, and analytical inference. Each mode is given with its mechanism, its *silent signature* (what it looks like when it succeeds), and a *detection check* (how it is caught). We show that the layers partition into two verification strata with fundamentally different epistemologies: the processing-grammar stratum, whose failures are checkable as invariants and admit certification, and the analytical-inference stratum, whose failures concern the meaning of correctly computed results, can never be exhaustively checked, and admit only audit and disclosure. The detection-check dimension makes this partition operational: grammar-stratum modes carry decidable checks, while inference-stratum modes carry only disclosure triggers. Missing data is shown to decompose across this boundary rather than belong to either side. The Atlas is compiled from the failure space outward — independent of any tool's detection capabilities — and is published as a living document accepting community contributions. We discuss its application to grading the coverage of evaluation benchmarks for AI analytics agents.

## 1. Introduction

Analytical systems fail loudly and silently. Loud failures — crashes, timeouts, constraint violations — announce themselves and get fixed. Silent failures produce answers: a revenue figure that silently sheds 3% of transactions whose regional assignment is missing; an inventory total 28 times the true holding because daily stock levels were summed across a month; a "most revenue" ranking whose winner changes depending on an undisclosed allocation rule; a satisfaction average computed, correctly, over the only customers unhappy enough or happy enough to respond; a `NOT IN` filter that returns nothing because the subquery contained a single null. Each number is plausible. Each survives every mechanical check that was actually run. Each is wrong, or — more dangerously — *right and misleading*.

Three developments make a systematic map of this territory overdue. First, AI analytics agents now answer natural-language questions against enterprise warehouses end to end; their fluency raises the cost of silence, because a confidently narrated wrong number is more persuasive than a raw one. Second, evaluation of these agents has concentrated on SQL correctness over clean schemas, leaving the dominant real-world failure mode — silent failure over defective or hazardous data — largely unmeasured; recent audits of agent benchmarks classify aggregation, join-type, and NULL-handling errors but frame them as agent bugs rather than mapping the underlying failure space. Third, the literatures that understand pieces of this space have not been joined: summarizability theory formalized aggregation validity decades ago and went largely dormant before agents existed; missing-data statistics owns three modes; practitioner traditions own others as design lore or as query-review checklists rather than as taxonomy.

This paper's contributions: (i) a definition and six-layer model of silent analytical failure (§2); (ii) the Atlas — 67 modes in 9 families, each with mechanism, silent signature, and detection check (§4); (iii) the two-strata thesis: a partition of the space into certifiable processing-grammar failures and audit-only analytical-inference failures, with the detection-check dimension as its operational expression and missing data as the bridge case that decomposes across the boundary (§5); (iv) an application: grading the coverage of an agent-evaluation benchmark against the Atlas, with the method's independence requirement made explicit (§6).

**Terminology note.** "Silent data corruption" is an established term in hardware reliability engineering, denoting bit-level miscomputation at fleet scale. The phenomenon studied here is distinct and lives at the analytical layer; we use *silent analytical failure* throughout.

## 2. Definition and the six-layer model

A **silent analytical failure** is any process by which a question asked of data receives a wrong or misleading answer with no error raised.

In scope: failures arising from data content, schema semantics, query construction and execution, and question interpretation. Out of scope: hardware-level corruption; loud failures; model hallucination without data involvement.

Failures are tagged by the layer at which they live — equivalently, what would have to change for the failure to vanish. The layers form a pipeline in the order a question traverses them:

- **Q — question interpretation.** The question itself is unsafe: ambiguous among materially different readings, or unanswerable from the data at hand.
- **S — semantic contract.** The declared meanings of names, codes, and definitions diverge from what the data actually holds. Every downstream layer depends on this contract.
- **D — data.** The data is defective: values missing, records contradictory, populations partially covered.
- **C — computation grammar.** The computation *plan* is unsafe over correct data: an aggregation, join, or window whose construction is invalid for the question, independent of how it is expressed.
- **X — query execution and expression.** The plan is valid, but the query *as written and executed* does not realize it: language semantics (null logic, operator precedence, type coercion), engine defaults (window framing, non-deterministic ordering, approximate functions), and stray constructs (residual limits, sampling) silently produce something other than intended.
- **I — analytical inference.** The number is computed correctly, and the conclusion it invites is wrong: the failure lives in the relationship between the result and its alternatives (its strata, its denominator's history, its sample mass).

The layer determines the verification epistemology, developed in §5: C-, X-, and the mechanics of D-layer failures are checkable as invariants and admit certification; I-layer failures admit only audit, because the space of relationships among correct results is never exhaustively checkable.

The distinction between C and X is worth stating plainly, because it is the structural contribution of this revision. C asks *is this the right computation for the question?* — should this measure be summed at all, is this join valid at this grain. X asks *does the SQL I wrote actually perform the computation I intended?* — a separate failure surface governed by language and engine semantics rather than by the structure of the data. A computation can be conceptually correct (C-clean) and still betrayed in execution (X-failed), and vice versa. Both are grammar-stratum and certifiable; keeping them distinct lets the detection checks target the right surface.

## 3. Related work: the fragments

**Summarizability theory.** Statistical-database and OLAP research formalized when aggregates may be validly computed from finer-grained data: foundational conditions (disjointness, completeness, type compatibility), a taxonomy of inaccurate summaries and management rules, and later surveys of summarizability issues in multidimensional modeling. This is the rigorous core of our family F1 — and only F1; it is schema-design-oriented, and the literature largely predates AI agents.

**Missing-data statistics.** The MCAR/MAR/MNAR distinction is canonical for three modes of family F3 and supplies the deepest single insight the Atlas inherits: that the *mechanism* of missingness, not the fact of it, determines whether any correction is honest — and that the mechanism is in general unverifiable from the data alone.

**Dimensional-modeling practice.** The Kimball-school pattern language (semi-additive facts, bridge tables with allocation, slowly changing dimensions, late-arriving facts) and the fan-trap/chasm-trap lore of the BusinessObjects universe-design tradition encode deep practitioner knowledge of families F1, F2, and F4 — as design advice for modelers, never as a failure taxonomy for answerers.

**Practitioner query-diagnostic frameworks.** Working analysts maintain query-review checklists — null-aware join and `NOT IN` traps, operator-precedence rules, integer-division and type-coercion guards, window-frame and deterministic-ordering discipline, and reconciliation of macro-totals against a trusted source. This tradition is the source of the execution layer (X) and of the detection-check dimension carried by every mode in this revision; it is rigorous and operational but typically circulates as tacit craft rather than as an organized map.

**Data quality and observability.** Data-quality dimension frameworks (accuracy, completeness, consistency, timeliness) characterize properties of data rather than failure modes of analysis; modern data-observability practice (freshness, volume, schema, distribution, lineage) monitors pipeline health and catches some D-layer modes operationally while remaining blind to the C, X, and I layers by design. A recent taxonomy of machine learning over data-quality defects observes that benchmark datasets with ground-truthed defects do not exist and calls their creation a primary research goal.

**Spreadsheet error research.** Two decades of audit studies established that quantitative artifacts contain errors at rates far higher than practitioners believe, with taxonomies of mechanical, logic, and omission errors — the wrong substrate for our purposes, but the strongest prior that silent quantitative failure is endemic rather than exotic.

**Agent evaluation.** Failure taxonomies for tool-augmented and web agents, and audits of data-engineering agent benchmarks, classify errors by agent behavior (flawed SQL logic, join-type selection, NULL semantics). These attribute; they do not map the data's failure space, and none spans the Q/S/D/C/X/I layers.

No unified, layer-spanning, agent-aware collection exists. The Atlas is, to our knowledge, the first attempt.

## 4. The Atlas

Compilation method: assembled from the failure space outward — the literatures and practitioner traditions above, SQL semantics, and incident lore — explicitly not from any tool's detection capabilities (see Independence statement, §7). Each mode carries three fields: its **mechanism and silent signature** (what the failure looks like when it succeeds) and its **detection check** (how it is caught). The checks are not uniform in kind, and that is the point: grammar-stratum checks are decidable tests a verifier can run; inference-stratum checks (marked *disclose*) are characterization-and-disclosure triggers, because no data-internal test can certify them. The check column is thus the operational face of the two-strata thesis (§5).

### F1 — Aggregation & summarizability (layer C)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F1.1 | Average of averages | unweighted mean of per-group means ≠ pooled mean when group sizes vary | recompute SUM(num)/SUM(den) from base granular rows; compare to the average-of-averages |
| F1.2 | Ratio/rate re-aggregation | averaging margins, conversion rates, percentages instead of re-deriving from summed numerator and denominator | re-derive every rate from summed numerator and denominator; never average pre-computed rates |
| F1.3 | Semi-additive stock summed over time | inventory/balance/headcount levels summed across the time axis; plausible huge number | forbid SUM across the time axis for stock measures; use period-end or period-average |
| F1.4 | Non-additive measure aggregated | distinct counts, percentiles, ratios treated as additive | mark non-additive measures in the semantic layer; block SUM/AVG roll-ups on them |
| F1.5 | Distinct-count re-aggregation | per-period uniques summed across periods; overlap double-counted | recompute COUNT(DISTINCT) over the full window from base rows, not SUM of per-period distincts |
| F1.6 | Empty bucket omission | zero-activity entities absent from grouped results; "lowest" answers wrong; gaps invisible | LEFT JOIN against the full dimension domain; assert grouped rows = dimension cardinality |
| F1.7 | Partial-period dilution/comparison | averages over non-operating days; month-to-date compared against full months | normalize by operating days; exclude or flag incomplete periods in any comparison |
| F1.8 | Hierarchy non-strictness | a child rolling to multiple parents (or none); subtotals ≠ total | assert each child maps to exactly one parent; test that subtotals sum to the total |
| F1.9 | Pre-aggregated table misuse | a summary built under one aggregation rule consumed under another | record each summary's aggregation rule in metadata; verify consumption matches it |
| F1.10 | Weighted average with wrong weights | weighting by row count where value-weighting was meant, or vice versa | state the weight column explicitly; reconcile against SUM(value·weight)/SUM(weight) |
| F1.11 | Extremum/count grain presupposition | MIN, MAX, and COUNT re-aggregate path-independently (min of minimums is the minimum; counts sum), so they pass every additivity check, yet their value presupposes the input grain — the population extremized or counted — which the result does not record; "minimum balance" or "active accounts" takes different values over account-day vs customer-day under one name, and once stored is uninterpretable without that grain | record the input grain (the population extremized/counted) with every stored extremum or count; for queries, confirm the extremized/counted grain matches the intended unit; treat path-independence as necessary but not sufficient for a self-interpreting aggregate |

### F2 — Joins & linkage (layer C, sometimes D)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F2.1 | Fan trap | 1:N join replicates measure rows; totals inflate with the fan-out | compare COUNT(*) before and after the join; assert right-side keys are strictly unique |
| F2.2 | Chasm trap | two fact tables joined through a shared dimension; both measures multiply | aggregate each fact independently before joining; never join two fact grains directly |
| F2.3 | Many-to-many aggregate-across | bridge membership sums exceed the grand total; no single number without an allocation rule | apply an explicit allocation rule; assert allocated parts sum to the grand total |
| F2.4 | Wrong join type / inner-join row loss | unmatched rows silently dropped; totals shrink with no residual bucket | validate whether the right table is subset/superset/exact; preserve baselines with LEFT JOIN + residual bucket |
| F2.5 | Duplicate records | the same entity/event loaded twice; everything double-counts | assert COUNT(*) = COUNT(DISTINCT key); dedup or enforce uniqueness upstream |
| F2.6 | Split identity | one real-world entity under multiple keys; distinct counts inflate, per-entity metrics fragment | entity-resolve before distinct counts; monitor the key-to-entity ratio |
| F2.7 | Orphaned/broken foreign keys | referential decay; joins lose or mis-attribute rows depending on join type | profile referential integrity (orphan rate) before joining |
| F2.8 | Grain-mismatch join | joining at the wrong grain multiplies rows combinatorially yet aggregates plausibly | confirm both sides share the join grain; assert post-join row count matches expectation |
| F2.9 | Contradictory attribute records | one entity carries incompatible attribute values across records; distinct-pair rollups double-count | test the functional dependency key→attribute for single-valuedness; route violations to adjudication |
| F2.10 | Null join-key drop | equality (=) fails on NULL, silently dropping records from the join | profile join keys for null rate before joining; use IS NOT DISTINCT FROM if nulls must match |

### F3 — Missingness & coverage (layer D/C mechanics; mechanism attribution is layer I)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F3.1 | MCAR value gaps | random nulls; skip-aggregation undercounts extensive measures (intensive measures survive) | profile null rate per column; decide skip vs. rescale explicitly for extensive measures |
| F3.2 | MAR missingness | missingness depends on observed variables; naive aggregates bias, correctably | model missingness against observed covariates; reweight rather than skip |
| F3.3 | MNAR missingness | missingness depends on the missing value itself; bias undetectable from the data alone | *disclose* — no data-internal test certifies the mechanism; state the assumption explicitly |
| F3.4 | Coverage gap / sampled population | a table covering a non-random subset, presented as the population | compare the table population to the reference universe; state the coverage ratio |
| F3.5 | Survivorship | only surviving entities present; trends flatter than reality | check for a deletion/churn process upstream; reconstruct the entry cohort before trending |
| F3.6 | Three-valued-logic filter drop | negation filters silently exclude NULL-valued rows | audit negation filters for NULL handling; add explicit IS NULL branches |
| F3.7 | Conservation leak | a rollup dimension partially populated; group totals shed value relative to the grand total | assert SUM over each rollup dimension = grand total; quantify the residual |
| F3.8 | Fill-semantics confusion | NULL vs 0 vs "not applicable" conflated; imputation presented as observation | distinguish NULL / 0 / N-A in the dictionary; never silently coalesce |

### F4 — Temporal (layers D and C)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F4.1 | Stale derived source | summary/cache lags detail; recent windows undercount by exactly the lag | check MAX(timestamp) against the pipeline SLA before trusting recent windows |
| F4.2 | Late-arriving facts & restatement | history changes after first load; yesterday's "final" number was not final | track a load/version timestamp; re-run reproductions and compare to first load |
| F4.3 | Slowly-changing-dimension attribution | attributes change over time; current-mapping vs as-of rollups diverge; both look complete | decide current vs as-of explicitly; verify with effective-dated joins |
| F4.4 | As-of join error | a point-in-time question answered with a current snapshot | join on the point-in-time snapshot, not the current dimension; assert temporal alignment |
| F4.5 | Period-length and calendar effects | unnormalized month comparisons; fiscal vs calendar misalignment; 53-week years | normalize by day count; use interval logic (INTERVAL '1 MONTH'), not hardcoded day spans |
| F4.6 | Timezone boundary cuts | "day" cut at UTC vs local; cross-region daily figures shift | standardize all timestamps to UTC centrally; convert to local only at the presentation layer |
| F4.7 | Event-time vs processing-time | when-it-happened vs when-recorded; backfills distort trend edges | document which timestamp is user action vs ingestion; trend on event time |

### F5 — Semantic & schema (layer S)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F5.1 | Definition drift | a metric redefined mid-history; the column name never changed | maintain a data dictionary; monitor upstream release notes for redefinitions |
| F5.2 | Misleading names | a column whose name implies different semantics than it holds | validate column semantics against sample values, not the name |
| F5.3 | Repurposed enumerations | a status code's meaning changed at some date | version enum dictionaries with effective dates; check code distribution over time |
| F5.4 | Test/internal data pollution | test rows and internal accounts inside production aggregates | map every WHERE clause back to the business population; exclude flagged internal rows |
| F5.5 | Soft-delete ambiguity | logically deleted rows included (or excluded) without anyone deciding | decide and document the include/exclude rule for soft-deleted rows |
| F5.6 | Unit & currency mixing | dimensionally invalid sums that are numerically smooth | carry units/currency as columns; block sums across mixed units; convert first |
| F5.7 | Granularity mislabel | a table documented at one grain, populated at another | assert the table's actual grain (COUNT(*) vs COUNT(DISTINCT key)) matches its documented grain |

### F6 — Population & statistical structure (layer I — the analytical-inference stratum)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F6.1 | Confounded aggregate (Simpson's reversal) | the pooled trend contradicts every within-group trend; the aggregate is correct and misleading | *disclose* — decompose across declared stratifiers (Kitagawa identity); surface reversal/mix-dominance, do not refuse |
| F6.2 | Denominator drift | a rate's denominator changes composition across the window; the rate moves without behavior changing | *disclose* — decompose the rate change into within-group and composition effects; report the composition share |
| F6.3 | Small-denominator ranking instability | best/worst rankings dominated by tiny-sample entities | *disclose* — attach sample size to each rank; suppress or flag tiny-n entries |
| F6.4 | Base-rate surface | counts where rates were needed, or vice versa | *disclose* — report rate alongside count; state the denominator |
| F6.5 | Regression-to-mean reading | extreme-group follow-ups mistaken for effects | *disclose* — flag extreme-group selection; note expected reversion |

### F7 — Numeric & computational (layer C)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F7.1 | Integer division truncation | in many dialects 3/4 returns 0; silent floor; rates of zero | cast at least one operand to FLOAT/DECIMAL (e.g., 3.0/4) before dividing |
| F7.2 | Rounding order | round-then-sum vs sum-then-round; totals that don't reconcile | sum then round for reconciled totals; never round then sum |
| F7.3 | Float vs decimal precision loss | floating-point accumulation breaks strict financial reconciliation; large-scale drift | mandate DECIMAL/NUMERIC for financial and high-precision sums |
| F7.4 | Percent vs percentage-point | a 2pp change reported as 2% (or 200%) | label deltas as pp vs %; check the formula against the metric definition |

### F8 — Question-layer (layer Q)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F8.1 | Grain ambiguity | per-customer vs per-transaction — multiple defensible readings, divergent answers | state the entity grain explicitly with the answer; confirm GROUP BY matches the intended dimension |
| F8.2 | Denominator ambiguity | "average revenue per customer": all customers, or purchasers? | state the denominator population in the answer |
| F8.3 | Stock-reading ambiguity | "total inventory in April": closing, average held, or (invalidly) summed | state the stock-reading convention (closing / average) explicitly |
| F8.4 | Attribution ambiguity | which mapping applies to history when entities move | state which temporal mapping (current vs as-of) was applied |
| F8.5 | Unanswerable-but-adjacent | the data contains something near the question; the adjacent number gets served | confirm the served quantity is the asked quantity, not a near neighbor; otherwise decline |
| F8.6 | Universe confusion | the question's population vs the table's universe — answering over what is observed as if it were what exists | confirm the answer's population equals the question's intended universe, not merely what is observed |

### F9 — Query execution & expression (layer X)

| # | Mode | Mechanism → silent signature | Detection check |
|---|---|---|---|
| F9.1 | Subquery NOT IN + NULL trap | a subquery returning one NULL makes NOT IN evaluate to unknown, filtering out everything | use NOT EXISTS, or add WHERE col IS NOT NULL to the subquery |
| F9.2 | Boolean precedence / missing parentheses | AND binds before OR; a missing parenthesis silently changes the whole filter | wrap all OR groups in explicit parentheses when mixed with AND |
| F9.3 | Count semantics: COUNT(col) vs COUNT(*) | COUNT(col) ignores nulls, COUNT(*) counts rows; confusing them biases averages and totals | state whether counting rows or populated values; choose deliberately |
| F9.4 | Window-frame mismatch (ROWS vs RANGE) | default framing differs silently on duplicate order keys, distorting moving aggregates | specify the frame explicitly (ROWS BETWEEN …); add a tiebreaker to the order key |
| F9.5 | Non-deterministic ordering | LIMIT or ROW_NUMBER without a tiebreaker returns results that change between runs | add a unique tiebreaker to every ORDER BY used with LIMIT or ROW_NUMBER |
| F9.6 | Approximate functions treated as exact | APPROX_COUNT_DISTINCT and kin carry ~error, disastrous for strict accounting | ban approximate functions for financial/exact metrics; label them clearly elsewhere |
| F9.7 | Unintentional sampling / stray LIMIT | a legacy LIMIT, TABLESAMPLE, or hardcoded ID bound yields a biased subset posing as the full set | scan the query for legacy LIMIT, TABLESAMPLE, and hardcoded boundaries before trusting totals |
| F9.8 | Implicit type coercion | silent type conversion alters comparison logic and disables index use | cast both sides to a matching type before comparing or joining |
| F9.9 | Case / whitespace mismatch | 'Apple ' ≠ 'apple'; expected string matches silently fail | normalize strings (LOWER, TRIM) before joining or filtering |

**Total: 9 families, 67 modes.** The Atlas claims usefulness, not completeness; §7 describes the contribution process by which it grows.

## 5. The two strata

The layers partition into two verification strata with different epistemologies, and the detection-check column makes the partition operational: where a mode admits a decidable check, it is grammar-stratum; where it admits only a disclosure trigger, it is inference-stratum. This partition is not a matter of convention or current tooling: it reflects an objective property of each failure — whether the failure is *decidable from the data together with its declared semantics*, or not. The boundary is a theorem in at least one case: a value missing not-at-random (F3.3) is provably undetectable from the data alone, whereas a fan-out inflation (F2.1) is provably detectable by a row-count invariant. The detection-check column records which side of this line each mode falls on, and therefore what kind of assurance is honestly available for it.

The **processing-grammar stratum** (F1, F2, F4, F7, F9, and the mechanics of F3) comprises failures of how numbers are computed and executed. Its hazards are invariants of data plus declared semantics — additivity of a measure against the queried axis, alignment of a query's population with a table's universe, single-valuedness of a mapping, faithful execution of the intended expression. Invariants are decidable and enumerable: a verifier can, in principle, *certify* a computation against this stratum, and every grammar-stratum mode above carries a check that is a runnable test. (One refinement family F1 forces: path-independence under re-aggregation is necessary but not sufficient for a self-interpreting result — an extremum or count is path-independent yet presupposes the input grain it ranged over (F1.11), so its certificate must also record that grain.) The execution layer (X) is the most purely certifiable region of all — null-trap, precedence, coercion, framing, and determinism checks are mechanical and complete. The expected output contract is: a correct number, or a correct account of why no number can be given.

The **analytical-inference stratum** (F6, and the mechanism-attribution half of F3) comprises failures of what correctly computed numbers mean. Its hazards are relationships among correct results: a pooled trend versus its stratified components; a rate versus the composition history of its denominator; a ranking versus the sample mass beneath each rank. This space is never exhaustively checkable — there is always another stratifier, another partition — so verification here is constitutionally *audit and disclosure*, never certification, which is why every inference-stratum check above is marked *disclose* rather than given as a test. The expected output contract changes accordingly: not a number, but an answer with its interpretive stability characterized. The characteristic failure is not wrongness but misleadingness: in evaluation terms, the grammar stratum fails as wrong-and-silent, the inference stratum as right-number-misleadingly-silent.

**The universal backstop.** One check cuts across every grammar-stratum family: *reconcile the macro-totals against a trusted source of truth.* When a query's headline totals fail to tie out to a system dashboard or an independent derivation, a silent grammar-stratum error is present somewhere upstream — fan-out, leak, double-count, coercion, or stray limit. Reconciliation does not localize the fault, but it is the most reliable single signal that one exists, and it belongs at the end of every pipeline. It has no inference-stratum analogue: a correctly computed but misleading number reconciles perfectly.

**Missing data is the bridge case**, and it decomposes across the boundary rather than belonging to either side. The *absence* is grammar-stratum mechanics: nulls are visible, countable, and mechanically handled (skip, rescale, stratify), with checkable properties — and, as F9 shows, nulls also drive a cluster of execution-layer traps. The *mechanism* — whether values are missing at random or because of what they would have said — is inference-stratum: unattestable from the data, the determinant of whether any correction is honest, dischargeable only by disclosure. One phenomenon, two strata; the cleanest pedagogy the space offers.

Two corollaries. For tool builders: claim language must track strata — "certified" is coherent only in the grammar stratum; inference-stratum capabilities can honestly promise only audit. For evaluators: scoring systems should distinguish wrong-silent from right-but-misleadingly-silent outcomes, because they are failures of different strata and respond to different remedies.

## 6. Application: grading benchmark coverage

A taxonomy compiled from the failure space outward enables an honest answer to a question every evaluation benchmark should face: *which part of the territory does this exam cover?* As a case study, a defect-seeded analytics benchmark under development by the author's organization — synthetic warehouses with latent ground truth, machine-verified answer keys, and adversarially seeded defects — grades its coverage openly against the Atlas: 20 of 67 modes seeded in its first version, concentrated in the aggregation-mechanics heartland (F1) and the question layer (F8), with open territories now named explicitly: linkage depth (F2), semantic drift (F5), the inference stratum (F6), numerics (F7), and the newly articulated execution layer (F9). The execution layer is a special case worth flagging: its modes are exercised not by seeding defects in the data but by the agent's own query behavior, so an agent benchmark tests F9 *behaviorally* — through whether the agent falls into the null-trap or the precedence trap — rather than through planted defects. The direction of dependency is the method's integrity condition: the map grades the exam; the exam must never define the map. The same exercise, in reverse, is generative: ranking unseeded modes by real-world frequency and seedability yields a versioned roadmap — with the inference stratum, headlined by Simpson's reversal, as the natural second movement, since it is precisely the stratum where current agent evaluation is weakest and "correct but misleading" lives.

## 7. Independence, limitations, and the living document

**Independence statement.** The author founds a company building verification tooling for the grammar stratum of this space. The Atlas was compiled from the failure space outward, includes families the author's tooling does not address (notably the inference stratum), and exists in part to make such gaps publicly gradeable — for the author's tools and benchmark as much as anyone's. Readers should weigh the conflict and the mitigation together.

**Limitations.** The Atlas claims usefulness, not completeness; mode boundaries involve judgment (several modes shade into neighbors, and the C/X split in particular is a useful idealization rather than a hard line); the F6 family's outer boundary — where data analysis ends and statistical methodology begins — is drawn pragmatically at modes that arise in routine business questioning; the detection checks state the standard discipline for catching each mode and are not claimed to be the only or optimal check; frequency claims about which families dominate practice rest on practitioner lore and incident reports, not measured incidence (itself a research gap the benchmark program aims to narrow).

**Living document.** The Atlas is maintained as a versioned public repository accepting contributions of new modes, refined signatures, sharper detection checks, and incident citations. Versioned releases are archived with DOIs; this document is release 1.3 (adds F1.11, extremum/count grain presupposition).

## References

1. H.-J. Lenz, A. Shoshani. Summarizability in OLAP and Statistical Data Bases. *SSDBM*, 1997.
2. J. Horner, I.-Y. Song. A Taxonomy of Inaccurate Summaries and Their Management in OLAP Systems. *ER*, 2005.
3. J.-N. Mazón, J. Lechtenbörger, J. Trujillo. A survey on summarizability issues in multidimensional modeling. *Data & Knowledge Engineering* 68(12), 2009.
4. M. Hachicha, J. Darmont. Summarizability Issues in Multidimensional Models: A Survey. 2013.
5. D. B. Rubin. Inference and Missing Data. *Biometrika* 63(3), 1976.
6. R. Kimball, M. Ross. *The Data Warehouse Toolkit*, 3rd ed. Wiley, 2013.
7. R. R. Panko. What We Know About Spreadsheet Errors. *Journal of End User Computing* 10(2), 1998.
8. R. Y. Wang, D. M. Strong. Beyond Accuracy: What Data Quality Means to Data Consumers. *Journal of Management Information Systems* 12(4), 1996.
9. C. Batini, M. Scannapieco. *Data and Information Quality: Dimensions, Principles and Techniques*. Springer, 2016.
10. E. H. Simpson. The Interpretation of Interaction in Contingency Tables. *Journal of the Royal Statistical Society B* 13(2), 1951.
11. E. M. Kitagawa. Components of a Difference Between Two Rates. *Journal of the American Statistical Association* 50, 1955.
12. Recent taxonomy of machine learning over data-quality defects, noting the absence of ground-truthed defect benchmarks. *Decision Support Systems*, 2025.
13. ELT-Bench-Verified: Benchmark Quality Issues Underestimate AI Agent Capabilities. arXiv preprint, 2026.

---
*Correspondence: Huayin Wang. Cite as: Huayin Wang (2026). The Silent Failure Atlas: A Taxonomy of Silent Analytical Failures in Data Analysis. Version 1.3. Zenodo. DOI: 10.5281/zenodo.20762839*

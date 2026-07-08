# Changelog

All notable changes to **columna-core** are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses the `-core` version line
carried in `columna_core.__version__`.

The entries below are extracted from the README version-history blocks (the de-facto changelog to
date); future changes are recorded here going forward.

## [0.7.7-core] — ON UNIVERSE pin wiring (Option A)
The population pin recorded by `Frame.on_universe(u)` is threaded to the planner (`run`/`plan` →
`_infer`) where it asserts the frame's intended population: a measure bound to `u` serves; a measure
bound to a *different* universe is out-of-domain and **refuses** (`out_of_universe`); an unknown `u`
is an **error**. Resolves the multi-universe / D5 co-anchoring ambiguity to the one chosen
population. 124 checks across 11 suites.

## [0.7.6-core] — the no-result is a value, not an exception
The structured no-result splits into a plain `Outcome` value (kind · discriminator · reason ·
alternatives) and a private internal `Refusal` *signal*. `ColumnResult.refusal` now holds an
`Outcome`: clarify/refuse/error is **data** every surface reads, never an `Exception`. 116 checks.

## [0.7.5-core] — ratio/rate co-anchoring (ADR-032 D5)
A ratio `N / D` is determinate only when numerator and denominator resolve over one shared
population. The planner checks this statically: a cross-universe ratio is a **clarify**
(`co_anchor_ambiguous`), naming the candidate populations, never a silent number. 115 checks.

## [0.7.4-core] — the two-level correctness contract (ADR-032)
The column engine never judges: it attempts and returns a result or a *no-result carrying a
discriminator* (`ambiguous` / `unsupported`). The **planner** owns the four outcomes
(serve · disclose · clarify · refuse) plus `error`, classifying every no-result at one chokepoint.

## [0.7.3-core] — attribute-anchor resolution hardened
`_attr_anchor` no longer picks the first edge a table provides: single-grain is unambiguous, a
denormalized multi-grain table is pinned by the delivery frame, and a genuinely ambiguous case is
**refused with the candidate levels named**. 107 checks across 10 suites.

## [0.7.2-core] — universe-predicate evaluation hardened to typed predicates
The universe predicate is evaluated at base grain by **broadcast-and-filter, never a join**;
compared sides are coerced to a common dtype. Fixes numeric / real-`Date` predicate handling.
101 checks across 10 suites.

## [0.7.1-core] — B-anchor crossing locus refinement + EXPLAIN-without-execution
Crossing *detection* moves from engine (execute time) to planner (compile time);
`frame(...).plan()` / `explain(execute=False)` returns the would-be annotation touching zero
backend data.

## [0.7.0-core] — a custom type + three custom operators, planner untouched (HLL case study)
The `distinct` family is decomposed into a parametric type `HLLSketch(p)` and three registered
operators (`hll_count`, `hll_merge`, `hll_estimate`) that slot in via the registry + engine only;
`planner.py` and `projection.py` hold zero sketch references. A publish-time witness store makes
sketches **stored, not cached**.

## [0.6.0-core] — inform-and-serve reconciliation (Frame-QL Manual)
A B-anchor crossing is **served with a critical `b_anchor_crossing` disclosure** naming the
alternative reducer, no longer refused. Disclosures carry a severity lattice
(none < info < caution < critical) with a frame-level rollup. 57 checks across 7 suites.

[0.7.7-core]: https://github.com/datumwise/columna

# Changelog

All notable changes to **columna-core** are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses the `-core` version line
carried in `columna_core.__version__`.

The entries below are extracted from the README version-history blocks (the de-facto changelog to
date); future changes are recorded here going forward.

## [0.9.0-core] — the FrameQL envelope becomes the language

Full narrative: `specs/release_notes_v0_9_0.md`.

- **The envelope is the language:** `SELECT <series [AS alias]>, … AT {anchor}` with `WHERE`/`HAVING`/
  `ORDER BY`/`LIMIT n PER {dims}` and `WITH` macros; `@` is the input-anchor marker universally and
  `AT {…}` is the sole output grain. The Name's Law — the Frame is the query (DataFrame minus Data = Frame).
- **The terse form is RETIRED:** the shipped `cols @ anchor` fragment leaves the wire (dated tombstone in
  `columna_core.frameql.parse_frameql`); a top-level `@` no longer spells the output anchor.
- **EXPLAIN, first-class:** the canonical desugared form (the exact artifact the planner consumed) + atom
  decomposition + the dependency cone with current verdicts + the would-be annotation, touching zero data.
- **Dependent-pair transport:** a functionally-determined anchor level (region fixed by store) is attached
  1:1 along the edge, never reduced; the §7 worked example `AT {region*store}` runs whole.
- **`filter_unreachable`** clarify minted (a WHERE dimension that cannot reach a series' input); the
  conjoined `PER` law (anchor-coordinates-only AND `PER ⊆ ORDER BY`). The four-mood wire contract is
  unchanged (`contract_version "1"`) — the break lives in the accepted query grammar, carried by this
  version and the tombstone.

## [0.8.0-core] — the Certificate customers, §2c, BASIS, and the describe extension

Full narrative: `specs/release_notes_v0_8_0.md`.

- **Certificate customers:** ASSERT (invariants) + HIERARCHY (FD chains) adjudicated by the same kernel,
  minting the unchanged `License`; the **scope-edit law** — ASSERT→cut (`conflicting_data`), license→recompute,
  edge→blocked transport (`contradicted_edge`); `reattest` recomputes the serving scope (pure, symmetric).
- **§2c universe resolution:** one expression → one universe; a cross-universe expression is a
  `cross_universe` category error; `ON UNIVERSE` retired from the query grammar; juxtaposition; single-universe sugar.
- **BASIS + absence semantics:** universes declare `events`/`spine`/`product`/`registry`; absence means
  zero (events) vs gap (spine/product, `incomplete_data`) vs membership (registry).
- **describe extension + the §2b insulation closure:** License blocks across fertility/hierarchy/assert,
  basis+absence on universes, operator properties, published-scope/cut; **no structural physical identifier
  crosses describe** (`realized_by` gone, predicates logical) — a standing test enforces it.
- Wire contract unchanged (`contract_version` "1").

## [0.7.8-core] — packaging hardening + the disclosure wire adapter

**Packaging / correctness (crediting the WP-0 acceptance audit):**
- Declare the hard `pyarrow>=15` runtime dependency. `connector.py` calls
  `pl.from_arrow(con.execute(q).arrow())` on every fetch and polars does not pull pyarrow
  transitively, so a clean-venv install imported fine but failed on first fetch. A wheel smoke test
  (fresh venv → real fetch) now guards this in CI.
- Resolve `COLUMNA_BENCH_WAREHOUSE` to an absolute path at read time, so a relative value no longer
  silently mis-resolves against the demo runner's cwd.
- Reconcile `benchmark.cml` with the code-built Manifold by adding the `region_label` measure
  (parser now yields 6 measures == the code set; `parse_benchmark` exits 0 on parity YES). A
  structural parity test guards against re-drift.

**v0.7.8 worklist (items 1–2), cleared:**
- `parser.py`: import `Optional` (fixes F821 — annotation-only, was masked by
  `from __future__ import annotations`; would have broken `typing.get_type_hints(parse_predicate)`).
- Remove unused imports / dead locals / a placeholder-less f-string across `disclosure.py`,
  `engine.py`, `model.py`, `parser.py`; the corresponding per-file-ignores are tightened back out.

**New:**
- `columna_core.disclosure_wire` — the structured `{code, materiality, …}` wire adapter (the
  category → (code, default materiality) table is normative, one dict). This is the ADR-032 D8 "one
  contract" serialization the MCP surface (WP-2.2) and every other surface share; WP-1.3 collapses
  into it.

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

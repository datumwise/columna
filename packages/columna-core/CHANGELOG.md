# Changelog

All notable changes to **columna-core** are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses the `-core` version line
carried in `columna_core.__version__`.

The entries below are extracted from the README version-history blocks (the de-facto changelog to
date); future changes are recorded here going forward.

## [0.12.0-core] — the RELATE face triad completes (assign · alloc), and the anchor law

The M:N crossing gains its full vocabulary beside the shipped `touch`:

- **Grammar.** `FACE <name> = ASSIGN BY <measure-ref> ORDER MIN|MAX` and `ALLOC BY <measure-ref>`.
  ORDER is **mandatory on ASSIGN, no default** — "top" is ambiguous across driver kinds (rank-like →
  MIN, score-like → MAX), and a silent default would be an unrecorded resolution. The driver is a
  DECLARED measure (resolved at publish, never a physical column). The declared-but-deferred parse
  refusals retire.
- **Engine.** `ASSIGN` restricts the bridge to each member's top-ranked pair and single-counts (the
  total reconciles to the grand total; the **shadow** of dropped memberships is disclosed). `ALLOC`
  splits by the per-member-normalized driver (the total reconciles to the cent; the **reconciliation
  badge** is the commutation certificate). `touch` unchanged.
- **Adjudication (fail-closed, per scheme).** assign — a UNIQUE top per member (a tie names the tied
  members + affected products); alloc — non-negative driver, strictly-positive per-member sum (a
  zero-sum member = undefined split); the driver must be a **spine** at the frontier grain (an
  events-derived driver must be frozen first — derived-then-recorded); a face-driver dependency DAG.
- **Anchor law (G5).** A **distinct-class** measure refuses at EVERY face, uniformly — its output
  anchor is spent at the frontier grain (per-member counts cannot be summed, weighted, or routed).
  The message speaks the DECLARATION dialect (`distinct(...)`), never the engine's sketch representation.
- **Chain guard (G4).** A multi-hop face path (crossing a crossed result) refuses — one frontier at a time.
- **Wire (additive; `contract_version` stays `"1"`).** `relates[].faces[]` gains `driver`; assign
  answers carry `memberships_unrepresented`; alloc answers carry `reconciliation {crossed_total,
  base_total, delta, tolerance, status}`.

Design history: `docs/proposals/0.12-triad-PROPOSAL.md`.

## [0.11.0-core] — RELATE faces: the many-to-many crossing executes

Full narrative: `specs/release_notes_v0_11_0.md`.

- **`RELATE` gains crossing FACES.** A non-functional (M:N) relationship may declare named crossing
  dispositions — `RELATE a <-> b VIA t(fcol, tcol) FACES { <name> = <SCHEME> -- "folklore" }`. A face
  names the value's DISPOSITION on the trip (the self-teaching verb triad `touch`/`assign`/`alloc`),
  never the selection criterion. The bare `VIA <table>` form is unchanged (back-compat).
- **`touch` EXECUTES.** `SELECT revenue AT {category.touch}` join-multiplies the measure through the
  relation's bridge to the crossed grain — the value reaches every match, deliberately multi-counted,
  served in **disclose** with the over-count as a material caveat. `assign`/`alloc` are declared-but-
  deferred (fail-closed parse refusal — v1 executes `touch` only).
- **The two absence disclosures of the crossing.** Over-count (totals exceed the grand total) and its
  mirror, coverage/shortfall (a fine entity in no bucket is excluded from every cell). Crossed-grain
  absence is a lawful **zero on events basis only** (a spine refuses the crossing — replication would
  corrupt the grid's completeness claim).
- **Adjudication mints the face license at publish** (polarity law — a face is closed by default; its
  license opens the crossing; `touch` = VERIFIED, membership expansion is exact arithmetic).
- **Model reshape:** `Manifold.non_functional` is now `list[Relate]` (from a bare tuple); the `VIA`
  bridge is MAP-LAYER — engine-visible, never on describe/the wire. `contract_version` stays `"1"`.

## [0.10.0-core] — the definition language, taught by a case

Full narrative: `specs/release_notes_v0_10_0.md`.

- **EDGE is purged; HIERARCHY is the sole functional-path surface (§2a):** a functional path is declared
  only inside a `HIERARCHY <lineage> { <a> -> <b> VIA t(a,b) [-> ...] ; <path> }` block (per-hop VIA,
  branching), desugaring to the same `FunctionalEdge`s — edges remain the single internal truth.
- **DESCRIPTION strings** (`-- "text"`) on any declaration and each family member — folklore that flows
  model → describe → wire.
- **Logical attributes (OF-9):** `LEVEL store … ATTR opened = stores.opened_date` and universe
  row-attributes (`ATTR units, units_returned ON transaction`); a predicate references `store.opened`
  and renders logically, the physical binding never crossing.
- **The two-artifact projection** (`columna_core.documents`): `logical_spec` (purely logical) and
  `physical_map` (many-to-one, with attested REJECT rows); `no_physical_leak` makes the blast wall
  checkable.
- **The base-row ASSERT data channel:** a row-form predicate is probed against the attested data
  (holds → corroborated; counterexample → fails closed; NULL comparands are not violations).

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

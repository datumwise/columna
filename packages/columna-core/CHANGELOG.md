# Changelog

All notable changes to **columna-core** are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses the `-core` version line
carried in `columna_core.__version__`.

The entries below are extracted from the README version-history blocks (the de-facto changelog to
date); future changes are recorded here going forward.

## 0.14.0 — column identity is the canonical expression, not a mechanical default

**WIRE CONTRACT BUMP: `contract_version` `"1"` → `"2"`.** No values, moods, disclosures, or reason
codes change — this bump is for exactly one thing: the default column **key** changed for the same
utterance. The `-core` version line moves to `0.14.0-core`. A `contract_version` bump is what a
pre-1.0 minor exists to signal, so this ships as its own minor.

Realizes **WP-NAME-1** (ratified Huayin 2026-07-30). The §4 mechanical default (`<reducer>_<measure>`)
dropped the input anchor — half a pinned reduction's denotation, per the Two Anchors law — and, after
0.13.4's composite pins, two distinct asks collided on one invented name. Retired. An unaliased series
is now keyed by its **canonical expression**, verbatim; no name is invented and none is mangled.

**What changed here:**

- **Unaliased column keys are the canonical expression.** `avg(revenue @ {day})` keys as
  `avg(revenue @ {day})` (the pin is now visible in the key); a bare measure keys as `revenue`; member
  access keys as `revenue.sum` — **verbatim dotted**, the dot-to-underscore mangle (`revenue_sum`) was
  itself an invention and retires with the default. One rule: identity = canonical expression, or an
  `AS` alias; a composite/nested/map/bracket expression is still refused for a name (author names it).
- **`EXPLAIN` / canonical form** emits no redundant `X AS X` — a series whose key equals its expression
  prints without an `AS` clause; only a distinct, author-owned alias prints.
- **`contract_version` → `"2"`.**

### Migration — for consumers keying on column names

`contract_version` is now `"2"`. Unaliased column keys changed from mechanical defaults to canonical
expressions: `avg_revenue` → `avg(revenue)`, `revenue_sum` → `revenue.sum`. **Consumers who key on
column names should key on `AS` aliases** — an alias is author-owned and will never change under any
future rule. That is the durable advice and the whole naming philosophy in one line: the framework
names a column by *what it is*; if you need a stable handle, you *give* it one.

## 0.13.4 — the composite input anchor: a product grain is a first-class pin

**ENGINE/GRAMMAR ADDITION, no wire change.** `contract_version` stays `"1"`; the JSON envelope shape
is unchanged. The `-core` version line moves to `0.13.4-core`. Two reason codes are minted inside the
existing `REASON_OUTCOME` vocabulary (adding a reason does not bump the contract — readers on `"1"`
route the new reasons by outcome, as they already do).

Realizes **WP-GRAIN-1** (ratified Huayin 2026-07-29). An inline reduction's input anchor may now pin a
PRODUCT of levels — `avg(revenue @ {store*product*cal.month})` — not just a single level. The engine's
`reduce_series_to_anchor` was already composite-grain-native; this lifts the planner's single-level
restriction and adjudicates the pin × output-anchor lattice.

**What changed here:**

- **Composite input anchor.** `@ {a*b*c}` (and the `{a,b}` spelling, folded to `*` in canonical form)
  parses to a product-grain pin; `_reduction_call` returns the pin as a tuple of levels. The
  single-level path is the n=1 case and is byte-identical (bare `@day`, `pinned to 'day'`, no rider).
- **Law 1 — `pin_coarser_than_output` (REFUSE, minted).** A pin level coarser than the output grain
  (an output level reaches it) is refused with a pin-specific teaching message and two lawful edits.
  Its OWN dimension per OF-1 (the pin choosing an ill-fitting grain), distinct from `out_of_universe`
  (run-time unreachability).
- **Law 2 — `redundant_pin` (CLARIFY, minted).** Two cross-comparable pin levels (one determines the
  other) fix one axis, not two — a clarify offering the two admissible pins, never a refuse.
- **Law 4 — the two-stage-statistic disclosure, generalized.** The immaterial `provenance`/`TRANSPORT`
  note names the composite pin as a braced product; when a pin axis is the output's own, a rider names
  it as fixed and the rest as reduced-over. Still an immaterial note ⇒ **serve** (OF-2).
- **F1 flip.** The lawful-but-unfaithful two-stage statistic is now a well-formed ask that serves and
  agrees (to float precision) with the below-surface IR it composes — confirming the minted doctrine
  that an expressible pinned ask is its own faithful denotation.

Out of scope (rowed as a future finding): the composite-input × FACED-output combinatoric, which meets
the existing G4 chain guard and refuses honestly with `chained_crossing` rather than serving.

## 0.13.3 — every dependency gets a ceiling, and a guard that makes it permanent

**PACKAGING CHANGE, no code change.** No engine, wire, or contract behaviour is touched;
`contract_version` stays `"1"`. The `-core` version line moves to `0.13.3-core`.

The release is driven by `columna-server` 0.8.2 — see that CHANGELOG for the outage: upstream
`mcp 2.0.0` (2026-07-28 13:45 UTC) moved `mcp.server.fastmcp`, and an uncapped `mcp>=1.0` meant
every fresh `pip install columna` died at import for ~17 hours. `columna-core` was not the broken
package; it is bumped because **the cap sweep is repo-wide and a metadata fix that is not published
does not exist.**

**What changed here:**

- **`pyarrow>=15` → `pyarrow>=15,<26`.** The one genuinely uncapped runtime dependency in core.
  Flagged honestly: pyarrow ships a major roughly quarterly (15 → 25 in about two years), so this
  ceiling needs a deliberate lift more often than the others. That is the cost of the guarantee and
  it is paid on purpose — a quarterly one-line lift beats a stranger's first install detonating on
  a major nobody here has run.
- `[test]`: `pytest>=8.0` → `pytest>=8.0,<10.0`.
- `build-system`: `hatchling` → `hatchling>=1.27,<2.0`. Build dependencies are capped too: a build
  backend that breaks stops the release that carries the fix, which is as user-visible as a runtime
  break. The floor is the first hatchling with PEP 639 (`license` + `license-files`), which this
  package uses.
- `polars<2.0`, `duckdb<2.0`, `datasketches<6.0` already carried ceilings and are unchanged.

**THE GUARD** — `scripts/assert_dep_caps.py`, in CI on every push and PR: every declared dependency,
in every package, must carry an upper bound (`<`, `<=`, `==`, `~=` — a `!=` names one bad version,
not a boundary). It covers `dependencies`, every `optional-dependencies` group, and
`build-system.requires`, and it strips environment markers before checking, so
`tomli>=2.0,<3.0; python_version < '3.11'` is judged on its specifier and not on the `<` inside its
marker. The website's `package.json` is checked too — npm carets are bounded by construction, and
now that is enforced rather than assumed.

**Twice is a class.** 0.13.2 was an unbounded `requires-python` found by a human on a Windows pass
the night before launch. 0.8.1 was an unbounded `mcp` found by CI going red on a specs-only merge
the day after. Both are the same failure: *a claim about versions that do not exist yet, checked by
nobody.* The doctrine was already written down — **fail closed with a named reason beats rare
success** — and this release finishes applying it to dependency metadata, by construction rather
than by vigilance.

## 0.13.2 — the declared Python floor and ceiling: 3.10–3.13, 64-bit

**PACKAGING CHANGE, no code change.** `requires-python` moves from `">=3.10"` to `">=3.10,<3.14"`
across all three packages. No engine, wire, or contract behaviour is touched; `contract_version`
stays `"1"`. The `-core` version line moves to `0.13.2-core`.

**THE FINDING** (Huayin, 2026-07-27, a Windows fresh-venv pass on launch eve). `pip install columna`
on Python 3.14 did not fail — it *started building*. `datasketches` 5.x publishes **no cp314 wheels
on any platform**, and **no 32-bit Windows wheels at any Python version**; `columna-core` hard-depends
on it (`engine.py` imports `sketch.py` at module top, for HLL). With no upper bound declared, pip
considered us a match, found no wheel, and fell through to a C++ source build — minutes of compiler
output ending in failure for anyone without a toolchain, which is nearly everyone we are asking to
try this in two minutes.

**THE DOCTRINE**: *fail closed with a named reason beats rare success for whoever happens to own a
compiler.* An unbounded `requires-python` is not permissiveness, it is an untested claim — we were
asserting support for every future Python, including ones that did not exist when the claim was
written. The bound converts a C++ explosion into pip's one-line `no matching distribution found`,
which is a sentence a person can act on.

**THE DOOR IS NAMED, NOT CLOSED.** Python 3.14 support arrives when `datasketches` ships cp314
wheels, or via the optional-extras split (`datasketches`/`duckdb` optional, with a polite refusal at
point of use) already scoped as **WP-1.1**. That split is rowed, not rushed into launch eve — an
import-graph restructure for the `PolarsConnector` is not a Monday-morning patch.

- **`requires-python = ">=3.10,<3.14"`** on `columna`, `columna-core`, and `columna-server`. Declared
  on each rather than inherited transitively, so installing any one of them alone also refuses
  cleanly (the WP-0 pyarrow lesson: state the constraint where the install actually happens).
- **Classifiers now name 3.13**, which was supported and shipped but never advertised — the list
  stopped at 3.12. CI's test matrix gains 3.13 in the same change: a claimed version that CI never
  runs is a claim nobody checked.
- **The supported line is now written down** — "Requires Python 3.10–3.13, 64-bit." — on the install
  page and both front-door READMEs, each with one troubleshooting line pointing the
  `no matching distribution` symptom at its cause.
- **THE CLASS GUARD.** The `demo wheel install` CI job gains a **windows-latest / py3.13** leg beside
  the existing ubuntu / py3.10 one. The class is *a dependency with platform or version wheel gaps*,
  and it was invisible to a Linux-only CI — which is precisely how this finding survived three
  releases. Both legs run the same assertion file (`scripts/assert_demo_play.py`) so they cannot
  drift into proving different things.

## 0.13.1 — the reconciliation delta reports at the resolution its tolerance warrants

**WIRE CHANGE, named not silent** (standing rule: removal-and-change is always named). Within-tolerance
reconciliation deltas now canonicalize to `0.0` — both the prose in the alloc badge and the structured
`reconciliation.delta` field. In-tree consumers only; **no `contract_version` bump** (the envelope and
the four moods are untouched).

**THE DOCTRINE**: *a value below the system's declared tolerance is noise, not a finding — reporting it
as a finding is false precision.* Once the engine has ruled `abs(delta) <= tol` — the exact condition
of `status: "reconciles"` — the residual bits sit below its own declared resolution of meaning. Serving
them as data is false precision, which is a species of confident wrong number. The masthead does not
say "no *large* wrong numbers."

- **The defect.** The alloc badge rendered `delta 0.0000` on most runs and `-0.0000` on ~20% — same
  package, same input, same machine. Instrumentation showed the raw subtraction alternating between
  exactly `0.0` and `±4.656612873077393e-10` (2**-31), decided by float SUMMATION ORDER, ~2e-16
  relative to a $2.2M total. It reached a byte-preserved recorded exhibit, so an artifact that may
  change only by re-recording was changing by itself, every deploy, on a coin flip.
- **The fix**, at the point of computation (`canonical_delta`), not at the formatting boundary — the
  structured field must be canonical too, or a consumer reading the number gets the artifact even when
  the prose does not.
- **No laundering.** A delta OUTSIDE tolerance keeps its exact value and its sign. Asserted by test:
  the guard must never quietly absorb a real shortfall.
- **Root cause is float summation order**, and it is fixed at the cause. Pinning threads was tried and
  REJECTED as a fix: it did not remove the flap and in fact inverted its distribution — suppressing a
  symptom while leaving the class alive.
- **Structural guard** (site-side, same release): `check_generator_determinism.py` runs every
  committed-output generator twice and asserts byte-identity, so non-determinism in a recorded
  artifact is a loud build failure instead of a 20%-of-deploys surprise.

**Provenance, in full** — flagged at the #85 preview, ordered for the 0.12.1 cargo, never landed;
resurfaced as a flap during the 0.13.0 confirmation re-record; misdiagnosed twice as a signed zero —
once by the builder, once by the desk, neither having looked at the number — then measured, then fixed
at the true cause.

## 0.13.0 — the ASSERT retirement

**BREAKING.** `ASSERT` (both forms — `ASSERT <n> [ON <u>] WHERE <pred>` and
`ASSERT <n> [ON <u>] AT <anchor> HOLDS <invariant>`) and the standalone row-attribute form
`ATTR <names> ON <universe>` are **removed from the definition language**.

**Migration:** delete those lines from your `.cml`. The parser's refusal names this note.

**Rationale — the admission test:** everything a Manifold's trial proves is a precondition of
something it serves. Seven provers shipped; six prove their own construct's serving preconditions.
The assert provers alone proved a claim no serving behavior depended on — load-bearing in form,
unloaded in fact. Data contracts belong to the attestation layer, not the meaning layer. The
standalone `ATTR … ON` form retires by cascade: its sole consumer was the row-form assert.

The **inline** `LEVEL … ATTR` form is unaffected — universe predicates load on it.

**Wire:** describe no longer emits the `asserts` field, nor universe `attributes`.
`contract_version` stays `"1"` — pre-broadcast, zero consumers.

**`conflicting_data`** refusals can no longer occur; the reason code is tombstoned (dated comment
plus a retirement-pin test asserting it is never emitted). The *reserved, unwired caveat code* of the
same name is untouched — same string, different referent.

Ruling: 2026-07-26. Net effect: a breaking release that removes more code than it adds.

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

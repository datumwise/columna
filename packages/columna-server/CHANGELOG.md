# Changelog

All notable changes to **columna-server** are recorded here
([Keep a Changelog](https://keepachangelog.com/)).

## [0.7.0] — the triad on the wire, and the third Cascadia universe

Requires `columna-core>=0.12.0` (the assign/alloc faces + the anchor law).

- **Third universe.** Cascadia gains `category_attributes` (12 rows: a distinct `priority` 1..12 and a
  raw, varied `alloc_weight`, md5-deterministic / byte-reproducible) and `UNIVERSE category_profile =
  category BASIS spine` with the two driver measures. The RELATE declares two more faces beside `touch`:
  `primary = ASSIGN BY priority ORDER MIN`, `split = ALLOC BY alloc_weight` (descriptions are DRAFT,
  ratified at the merge gate).
- **Wire.** `describe_manifold`'s `relates[].faces[]` gains `driver`; query answers carry the assign
  **shadow** (`memberships_unrepresented`) and the alloc **reconciliation** badge. Additive — the VIA
  bridge stays map-layer; `contract_version` stays `"1"`.
- **Exhibits.** E11 (`revenue AT {category.primary}`) discloses the shadow (270 memberships, total ≡
  the grand total $2,212,391.86); E12 (`revenue AT {category.split}`) serves with the reconciliation
  badge (total ≡ the grand total to the cent). Recorded via the standing seed pipeline; the /case copy
  comes to the desk post-build.

## [0.6.1] — warehouse coherence (data-only)

Patch, DATA-ONLY: no code, no wire, no contract change. Requires `columna-core>=0.11.0` (unchanged).

- **The Cascadia demo warehouse now COHERES with its transaction ground truth.** A stranger-read of the
  generated exhibits (verified at the desk) found the reference/summary tables had drifted incoherent:
  FK coverage was 2,051/19,995 (customers held 2,000 of ~10,157 distinct transaction ids) and the
  summaries ran 10-15× off base truth — which *contradicted the ratified burn story*, where the stale
  summaries are *plausibly* wrong, never wild. `transactions` and `eom_inventory` are untouched (every
  recorded number delivers from them); the reference/summary tables are regenerated DERIVED-THEN-
  DEGRADED, each wearing exactly its one story-sin (`customers` grows to 10,157 = full FK coverage;
  `daily_revenue_summary` = true daily revenue minus its 15 missing days; `monthly_avg_order_value` =
  the transaction-for-order substitution; `monthly_unique_visitors` = a per-store double-count;
  `monthly_store_inventory` = the illegal sum-of-stock-over-time; support/engagement redrawn from the
  real customer distribution, engagement covering ~half).
- **A new permanent suite** (`test_warehouse_coherence.py`) makes the class structural — 100% FK
  coverage, each summary within its declared-sin tolerance of base truth, the engagement ratio.
- **Byte-stability guarded:** the E1-E10 seeds and both transcripts' numbers are byte-stable across the
  regen (the served measures deliver only from the untouched facts).
- Regeneration harness: `scripts/regen_warehouse.py` (deterministic, reproducible).

## [0.6.0] — RELATE faces go visible (the crossing served, and shown)

Requires `columna-core>=0.11.0` (the faces mechanism). `contract_version` stays `"1"` — `relates[].faces[]`
is additive, the DESCRIPTION precedent.

- **`describe_manifold`'s `relates[]` gains `faces[]`:** each declared crossing disposition rides describe
  as data — `[{name, scheme, description}]` — so a consulting agent (and the clarify-as-menu) sees the
  disposition from the source of truth before spending the query. Logical fields only; the `VIA` bridge
  stays MAP-LAYER (engine-visible, never on the wire) — the §2b insulation test asserts it.
- **Cascadia declares `FACE touch`** on product↔category (ship-dark revoked): the demo now *shows* the
  crossing. `SELECT revenue AT {category}` clarifies with the **face menu**; `SELECT revenue AT
  {category.touch}` executes — 12 categories, touch total $3.18M vs grand total $2.21M (the ~$970K
  overlap disclosed), 600/600 coverage.
- **The recapture corpus grows to ten (E1–E10):** E6 records the face menu; E10 mints the executed
  crossing (disclose · over_count · coverage). Zero drift flags.

## [0.5.0] — RELATE rides the wire (declared M:N as describe data)

Purely additive; `contract_version` stays `"1"` (the DESCRIPTION precedent — additive fields ride).
Requires `columna-core>=0.10.0` (unchanged).

- **`describe_manifold` gains `relates[]`:** declared many-to-many relationships now ride describe as
  data — `[{frm, to, note}]`, logical level names plus the NOTE string verbatim. Nothing physical (no
  VIA, no bridge-table name); the standing §2b insulation test covers the new field by construction.
  `describe_measure` is untouched.
- **Why it's load-bearing (not decoration):** a consult-first agent can now name a fan-out *before*
  spending the query — answer "why can't I get revenue by category" from the source of truth — instead
  of the M:N being invisible until tripped, its reason living only in the clarify's after-the-fact
  detail text. The RELATE was always declared "so the refusal can name exactly why"; `relates[]` finally
  puts that on the wire. Multiplicity between logical concepts is substance under §2b″.
- **Born with room for its future:** when RELATE-adjudication puts multiplicity claims on trial, their
  verdicts join these entries additively (the allocation-semantics taxonomy's wire foundation).

## [0.4.0] — the Cascadia case demo, and the agent grows hands

Full narrative: `specs/release_notes_v0_10_0.md`. Requires `columna-core>=0.10.0`.

- **The demo is Cascadia Retail** (replacing the benchmark): a realistic case — one team, one warehouse,
  six questions — modeled to a spec, adjudicated live (`demo --play` runs the E4→E8→E2→E5 four-mood
  wheel over the Cascadia Manifold; `stock`/`buyers` are the Cascadia names).
- **The case rides as an on-demand MCP resource:** `case_chapter` / `case_manifest` serve the three
  chapters verbatim — the WHY behind the Manifold, fetched on a triggering pointer, not stuffed in the
  prompt.
- **The query agent has hands:** native tool-use — within a turn it calls `describe_manifold`,
  `describe_measure`, `case_manifest`, `case_chapter`, `explain`, then the terminal `query` — bounded
  cycles, grounding preserved, the MCP boundary intact.
- **The recapture seeded corpus** (`columna_server.recapture`): E1-E9 adjudicated expectation-first
  against the ratified exemplar spec; the drift-gate the site + tripwire bind to.

## [0.3.0] — the envelope wire + EXPLAIN as a first-class tool

Full narrative: `specs/release_notes_v0_9_0.md`.

- **`query` speaks the envelope** (`SELECT … AT {…}`): the terse `cols @ anchor` form is retired from the
  wire and the `universe` argument is gone (§2c — universe is resolved structurally, never named in a
  query). The four-mood wire contract is unchanged (`contract_version "1"`).
- **`explain` is a first-class tool beside `query`:** the canonical desugared form + atom decomposition +
  the dependency cone with current verdicts + the would-be annotation, touching zero data — the agent's
  cheap inner loop.
- **Every speaking surface migrated to the envelope:** the `demo --play` tour, the MCP acceptance suite,
  and the agent's system prompt (its grammar section rewritten to teach `SELECT`/`AT`, `@`-as-input, and
  the `WHERE`/`HAVING`/`ORDER BY`/`LIMIT PER`/`WITH` clauses).

## [0.2.0] — columna init, the measured KP v0.5, the four-mood tour, and the Explorer describe

Full narrative: `specs/release_notes_v0_8_0.md`.

- **columna init** — the authoring on-ramp: the meaning-in seam between a governed aperture (catalog/
  profile/metered samples; no exfiltrating read) and a draft with a two-layer polarity wall (proposes
  closures freely, cannot express an inferred opening). It proposes; the human declares.
- **The knowledge package ships at v0.5**, reached by a pre-registered eval ratchet (v0.3 salience →
  v0.4 prune, reverted under its do-not-ship clause → v0.5 floored prune): flooding down AND ◆-recall held.
- **The four-mood tour** — `demo --play` walks serve/disclose/clarify/refuse on well-posed §2c asks;
  disclose = a stock summed across a blocked time axis (material caveat, never a silent total).
- **describe** gains the full C-1 extension (basis/absence, asserts, hierarchies, licenses, scope/cut,
  operator properties) under the §2b insulation guarantee; the **Manifold Explorer** renders any describe.
- Wire contract unchanged (`contract_version` "1").

## [0.1.0] — the MCP server, the packaged demo, and the NL agent

First release. The Columna MCP server and its two front doors, over one contract (ADR-032 D8 — the
four moods as data; `contract_version` `"1"`).

- **MCP server** (`columna-server mcp --manifolds <dir>`): five read-only tools —
  `list_manifolds`, `describe_manifold`, `describe_measure`, `query`, `explain` — over a Manifold
  store (`<id>/manifold.cml` + `data.toml`, parsed once at startup). stdio canonical;
  `--http` gated by `COLUMNA_MCP_TOKEN` (constant-time `hmac.compare_digest`). No SQL, no writes.
  The envelope grammar is parsed here; every expression is delegated to columna-core (one dialect).
- **Packaged demo** (`columna-server demo [--play]`): the benchmark Manifold over a small bundled
  warehouse (byte-identical to the core fixtures, drift-guarded), runnable with no path args.
  `--play` prints the real clarify → refuse → disclose → serve wire transcript — all four moods
  (post-§2c: the cross-universe wedge that once drove disclose is now a category error, so disclose is
  driven by a well-posed ask — `level.sum @ store*cal.month`, a stock summed across a blocked time axis).
- **Natural-language agent** (`columna-server agent`, `[agent]` extra): a true MCP client — spawns
  the server over stdio and speaks the protocol, never importing the engine. Natural language
  becomes a *proposed* Frame-QL query; the four moods drive the conversation (clarifies relayed,
  never auto-picked; every numeral verbatim from the wire — grounding is structural). Provider layer
  (`anthropic` default via `COLUMNA_AGENT_MODEL`; `scripted` for tests).

[0.1.0]: https://github.com/datumwise/columna

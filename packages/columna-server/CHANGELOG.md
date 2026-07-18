# Changelog

All notable changes to **columna-server** are recorded here
([Keep a Changelog](https://keepachangelog.com/)).

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

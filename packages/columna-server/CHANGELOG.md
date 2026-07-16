# Changelog

All notable changes to **columna-server** are recorded here
([Keep a Changelog](https://keepachangelog.com/)).

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

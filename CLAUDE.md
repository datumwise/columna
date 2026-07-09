# WP-2.3 — COMPLETE ✅ (merged 2026-07-08 via PR #3, merge 45d4cc4)

The packaged demo + `columna-server demo [--play]` + the repo README quickstart are done and merged:
a fresh clone reaches clarify → refuse → disclose in three commands, no path args and no MCP client;
the demo data ships in the wheel (a drift-guarded, byte-identical copy of the core fixtures) and runs
from a clean-venv wheel install (proven on Python 3.10). Server + repo-README only; zero columna-core
changes.

**WP-2.1 (Manifold store) is absorbed.** The directory store shipped inside WP-2.2/2.3
(`<dir>/<id>/manifold.cml` + `data.toml`, parsed once at startup) satisfies its Phase-2 scope; a
dedicated store WP resurfaces only when multi-manifold management needs a real catalog.

---

# WP-2.2 — COMPLETE ✅ (merged 2026-07-08 via PR #2, merge 7d9fe45)

The Columna MCP server (`columna-server` 0.1.0) and `columna-core` 0.7.8 (the `disclosure_wire`
adapter) are done and merged: five read-only tools, one contract (the four moods as data), the
materiality-driven `serve`/`disclose` rule, `--http` gated by COLUMNA_MCP_TOKEN, verified over real
MCP stdio (8/8 acceptance + wire-schema test + a clean-container install-from-wheels + stdio-replay
audit). This task section is retained for reference and will be replaced at the next WP kickoff.

---

# Current WP: 2.4 — the query agent (NL over MCP) [Phase-2 finale]

_(WP-0: COMPLETE via PR #1. WP-2.2 via PR #2. WP-2.3 via PR #3. WP-2.1 absorbed.)_

Implement `specs/wp2_4_query_agent_spec.md`. ADR-032 D8's last surface: `columna-server agent` — a
chat REPL where natural language becomes a *proposed* Frame-QL query, the planner disposes, and the
four moods drive a real conversation. Model proposes, layer checks, human decides.

## Architecture (non-negotiable shape)
1. **True MCP client.** The agent spawns `columna-server mcp/demo` over stdio and speaks the
   protocol; it NEVER imports the engine to answer. Bypassing the MCP boundary = the WP has failed,
   regardless of output quality (asserted in tests).
2. **Loop:** user NL → LLM proposes ONE envelope query (given `describe_manifold` + grammar) →
   `query` tool → outcome routes the turn: serve/disclose present values *from the wire* (every
   material disclosure surfaced); clarify relays alternatives to the HUMAN and applies their choice
   via `apply` (**never auto-picks silently**); refuse/error explains the reason (may propose a
   reformulation, itself a new proposed query).
3. **Grounding invariant:** every numeral in a reply originates in this session's wire JSON — no
   arithmetic on results, no memory-sourced numbers. Tested hermetically.
4. **Provider layer (ruling 3-B):** tiny `propose(context, user_msg) -> str` interface; `anthropic`
   (default) + `scripted` (deterministic, for tests/demos). Agent deps isolated in an `[agent]`
   extra; BYO key; no key → clear error pointing at `demo --play`.

## Invariants
- **columna-core and the wire contract untouched.** Agent code + `[agent]` extra only.
- Hermetic suite is green in CI with **no API key and no network** (scripted provider).
- System prompt lives as a **versioned file**, not an inline string.

## Checkpoint before building (light; wait for approval)
Post: (a) the system prompt **verbatim**; (b) the provider interface surface; (c) the hermetic
test plan — specifically how grounding and no-silent-auto-pick are asserted.

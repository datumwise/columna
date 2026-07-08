# WP-2.2 — COMPLETE ✅ (merged 2026-07-08 via PR #2, merge 7d9fe45)

The Columna MCP server (`columna-server` 0.1.0) and `columna-core` 0.7.8 (the `disclosure_wire`
adapter) are done and merged: five read-only tools, one contract (the four moods as data), the
materiality-driven `serve`/`disclose` rule, `--http` gated by COLUMNA_MCP_TOKEN, verified over real
MCP stdio (8/8 acceptance + wire-schema test + a clean-container install-from-wheels + stdio-replay
audit). This task section is retained for reference and will be replaced at the next WP kickoff.

---

# Current WP: 2.3 — packaged demo + the ten-minute quickstart

_(WP-0: COMPLETE, merged 2026-07-08 via PR #1 — repo/tests/packaging/CI for columna-core.)_

Implement `specs/wp2_3_demo_quickstart_spec.md`. Small: a fresh visitor goes from `git clone` to
*seeing a clarify* in under ten minutes, no path args, no MCP client. Turns the proven three-mood
transcript (clarify → refuse → disclose) into the product's front door: packaged demo,
`columna-server demo [--play]`, and the repo README quickstart.

## Invariants
1. **No columna-core changes.** Server + repo-README only.
2. **Wire contract untouched** (`contract_version` stays `"1"`); `--play` prints what the wire
   actually returns, never a hand-written facsimile.
3. **Demo data is drift-guarded** — the packaged demo warehouse/`.cml` must be byte-identical to
   the core fixture source (same guard pattern as the `.cml` byte-identical test), ≤ 2 MB.
4. **Wheels build with package-data included**, and a clean-venv **wheel** install must run
   `columna-server demo --play` (proves the data ships).
5. **Honest naming stays** (`sell_through_rate`; AOV is reserved for the input-anchor story).
6. Existing suites stay green (core 138/20, server 26 + new tests); CI gains the `--play` smoke.

## Checkpoint before building (light — this WP is small; wait for approval)
Post: (a) the README quickstart text verbatim; (b) the `demo` CLI help surface; (c) the
package-data mechanics (how the ≤ 2 MB ships in the wheel) + the drift-guard plan.

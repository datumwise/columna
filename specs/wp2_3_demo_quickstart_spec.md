# WP-2.3 spec — packaged demo + the ten-minute quickstart (v1)

**Goal.** A fresh visitor goes from `git clone` to *seeing a clarify* in under ten minutes, with
zero path arguments and no MCP client required. This WP turns the proven three-mood transcript
(clarify → refuse → disclose) into the product's front door.

**Context files.** Repo README (placeholder), `columna-server` (`__main__`, store, wire),
`demos/mcp_claude_desktop.md`, core `tests/fixtures/mini_warehouse` + `benchmark.cml`,
server `tests/fixtures/manifolds/benchmark/`. WP-2.2 audit lessons: contributors need
`pip install -e "packages/columna-server[test]"` spelled out; pre-PyPI, core installs first.

## Deliverables

1. **First-class packaged demo.** `columna_server/demo/` as package-data: `manifold.cml`,
   `data.toml`, and the mini warehouse (≤2 MB — reuse core's fixture data). A **drift-guard
   test** asserts the demo data is byte-identical to the core fixture source (same pattern as
   the `.cml` guard). The full 4.7 MB warehouse path (`--manifolds` + core `demos/warehouse`)
   remains the documented "richer run."
2. **`columna-server demo` subcommand.** No arguments → serves MCP stdio on the packaged demo
   manifold. `--http :PORT` passes through with the existing token gate.
3. **`columna-server demo --play`.** Self-playing transcript: runs the three-mood script
   in-process (frameql + disclosure_wire directly; no MCP loop needed) and pretty-prints the
   real wire JSON for: wedge query (`sell_through_rate: revenue / level.last @ store, day`) →
   `clarify` with alternatives; pin substitution → `refuse` (informative reason); reformulation
   → `disclose` with the frame-scoped material coverage caveat. This is the ten-minute payoff
   and the seed of the website widget script. Honest naming stays (`sell_through_rate`; AOV is
   reserved for the input-anchor story).
4. **Repo README quickstart** (replaces placeholder): what Columna is in three sentences (the
   honest-metrics-engine positioning, one line on the four moods); then the three commands —
   clone; `pip install -e packages/columna-core -e packages/columna-server`;
   `columna-server demo --play` — then "connect an agent" (Claude Desktop snippet, linking
   `demos/mcp_claude_desktop.md`); then a contributor block (the `[test]` extra, core-first
   pre-PyPI note, how to run both suites).
5. **CI smoke test:** run `demo --play`, assert the output contains all three moods in order
   (`clarify`, `refuse`, `disclose`) and `contract_version: "1"` — one cheap regression over
   the entire wedge path.

## Invariants
- **No columna-core changes.** Server + repo-README only.
- Wire contract untouched (`contract_version` stays `"1"`); `--play` prints what the wire
  actually returns, never a hand-written facsimile.
- Demo data duplication is drift-guarded; wheels must build with package-data included, and a
  clean-venv **wheel** install must be able to run `demo --play` (proves the data ships).
- Existing suites stay green (core 138/20, server 26 + new tests).

## Acceptance
1. Fresh clone → three commands → `--play` prints the three-mood transcript with real wire JSON.
2. `columna-server demo` serves stdio with zero path args; an MCP client sees 5 tools.
3. Clean-venv install **from wheels** → `columna-server demo --play` works (package-data proof).
4. Drift-guard test green; both suites green; CI includes the smoke test.
5. README quickstart present, includes the contributor install lines from the audit lessons.

## Out of scope
PyPI publication; a downloader for the full warehouse; the website widget; the query agent
(WP-2.4); OSI/dbt import; any engine or contract change.

## Checkpoint (light — this WP is small)
Before building, post: (a) the README quickstart text verbatim, (b) the `demo` CLI help
surface, (c) the package-data mechanics (how the ≤2 MB ships in the wheel + the drift-guard
plan). Then build on approval.

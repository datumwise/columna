# Current WP: 2.2 — the Columna MCP server

_(WP-0: COMPLETE, merged 2026-07-08 via PR #1 — repo/tests/packaging/CI for columna-core.)_

Implement `specs/wp2_2_mcp_server_spec.md`. This is the wedge product: the MCP surface whose
wire contract IS the product's public face. The spec is the contract; where it is silent, ask.

## Hard invariants
1. **Read-only, Frame-QL only.** No SQL acceptance anywhere; no write surface of any kind.
2. **One contract (ADR-032 D8).** Every tool returns the same outcome/disclosure structure the
   Python API returns. No surface gets a different truth.
3. **The adapter table in the spec is NORMATIVE** — the category-to-(code, materiality) mapping
   lives in code as one dict; deviations require sign-off.
4. **Clarify alternatives must be mechanically substitutable** — acceptance #4 scripts the
   round-trip (clarify, pick token, re-query, serve/disclose). Not aspirational; tested.
5. **`explain` proves zero data touched** — fetch-count delta asserted in tests.
6. Zero behavior changes to existing columna-core modules EXCEPT the pre-approved additions
   below.

## Pre-approved core changes (part A, its own commit, before any server code)
- Fix items 1-2 in `specs/v0_7_8_worklist.md` (parser.py F821 `Optional`; unused-import cruft)
  and remove their per-file-ignores from pyproject.
- Add NEW module `src/columna_core/disclosure_wire.py` — the adapter (spec's wire-contract
  section), with unit tests. Additive only; no existing module edited beyond the worklist fixes.
- Bump columna-core to `0.7.8`; CHANGELOG entry crediting the WP-0 audit finds.

## Part B: the server
- Package `columna-server` gets its first real code. Entry:
  `columna-server mcp --manifolds <dir>`; stdio canonical, `--http :PORT` gated by
  COLUMNA_MCP_TOKEN. Manifold dir stub per spec: `<dir>/<id>/manifold.cml` + `data.toml`.
- Fixture Manifold = the repo's benchmark.cml + fixture warehouse (WP-0 assets). The
  region_label measure must appear in describe_manifold output (it exists because of a WP-0
  parity fix; treat it as a canary).

## Checkpoint before building (post plan, wait for approval)
Propose: (1) the five tool JSON schemas; (2) ONE complete wire-contract example — the AOV
clarify case, verbatim JSON; (3) the disclosure_wire module surface; (4) test plan mapped to
the eight acceptance items; (5) anything the spec under-determines.

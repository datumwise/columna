# columna-server

The **Columna MCP server** (ADR-032 D8): a library of Manifolds exposed to AI agents over MCP, with
**one contract** — every tool returns the same outcome/disclosure structure the Python API returns.
This is the wedge product: the first metrics MCP server that can say *"it depends."*

## Run

```bash
pip install -e packages/columna-core -e packages/columna-server
columna-server demo --play                    # the packaged demo: clarify -> refuse -> disclose
columna-server demo                           # serve the packaged demo over MCP stdio (no path args)
columna-server mcp --manifolds <dir>          # serve your own manifolds dir over stdio
columna-server mcp --manifolds <dir> --http :8000   # streamable-http, gated by COLUMNA_MCP_TOKEN
```

**Richer run.** The packaged demo ships a small (~330 KB) warehouse. To run the same benchmark
Manifold over the full 4.7 MB warehouse (299,934 transactions), point `--manifolds` at a directory
whose `data.toml` warehouse path is the repo's `packages/columna-core/demos/warehouse`.

> Before columna-core is published to PyPI, install it FIRST (the workspace/editable install above),
> since `columna-server`'s `columna-core>=0.7.8` dependency cannot yet be resolved from an index. To
> run the tests, install the test extra: `pip install -e "packages/columna-server[test]"`.

`<dir>` holds `<id>/manifold.cml` + `data.toml` (connector type + data path). Manifolds are parsed
and connected once at startup.

## Tools (five, read-only — no SQL, no writes)

| tool | touches data? | returns |
|---|---|---|
| `list_manifolds()` | no | id, name, description, measure count, universes |
| `describe_manifold(manifold_id)` | no | dimensions/levels, edges (+ lineage), universes (+ predicate), measure index |
| `describe_measure(manifold_id, measure)` | no | family triple, per-member anchors, dtype, v-anchor `{universe, grain}`, m-anchor, provenance |
| `query(manifold_id, frameql, universe?)` | yes | the wire contract (serve/disclose/clarify/refuse/error) |
| `explain(manifold_id, frameql, universe?)` | **no** (`fetches_delta: 0`) | the would-be outcome + disclosures |

`frameql` is `"<columns> @ <anchor>"` (e.g. `"rate: revenue / level.last @ store, day"`); the
envelope is parsed here and every expression is delegated to columna-core — one expression dialect.

## The contract

Outcomes are data (the four moods), and disclosures are structured `{code, materiality, severity,
category, detail, remedy, source, rel_error}` via `columna_core.disclosure_wire` — the same
serialization every surface shares. Clarify alternatives are mechanically substitutable (a universe
pin carries `apply: {"universe": U}`).

See [`demos/mcp_claude_desktop.md`](demos/mcp_claude_desktop.md) for a Claude Desktop config and a
real clarify → answer transcript.

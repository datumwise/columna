# Columna

**Columna is an honest metrics engine.** It sits between your questions and your warehouse and
refuses to return a confident wrong number: where a metric is ambiguous, non-reconciling, or
out-of-domain, it says so instead of guessing. Every answer is one of **four moods** — *serve*,
*disclose*, *clarify*, or *refuse* — returned as structured data on one contract, identical on every
surface (Python and MCP).

## Quickstart (ten minutes, no arguments, no MCP client)

```bash
git clone https://github.com/datumwise/columna && cd columna
pip install -e packages/columna-core -e packages/columna-server
columna-server demo --play
```

`demo --play` runs the real wedge end to end and pretty-prints the actual wire JSON for three of the
four moods in one flow:

- **clarify** — `sell_through_rate: revenue / level.last @ store, day` spans two populations, so the
  rate's population is ambiguous; the server names the candidate populations as substitutable
  alternatives instead of inventing a number.
- **refuse** — pin one of those populations and re-ask: the other operand is out-of-domain, so it
  refuses with the reason (still no guess).
- **disclose** — reformulate into separate columns over the union population: the numbers are served
  **with** a material coverage caveat riding on the frame.

That transcript *is* the product. (No path arguments needed — the demo Manifold and a small warehouse
ship in the package. For a richer run over the full benchmark warehouse, see
[`packages/columna-server/README.md`](packages/columna-server/README.md).)

## Connect an agent

`columna-server demo` (no `--play`) serves the same demo over MCP stdio — five read-only tools, no
path args. To wire it into Claude Desktop, add to `claude_desktop_config.json`:

```jsonc
{
  "mcpServers": {
    "columna": { "command": "columna-server", "args": ["demo"] }
  }
}
```

(Claude Desktop launches the server from an arbitrary working directory, so `demo` — which needs no
path — is the reliable choice; if you use `mcp --manifolds <dir>` instead, give an **absolute** path.)
See [`packages/columna-server/demos/mcp_claude_desktop.md`](packages/columna-server/demos/mcp_claude_desktop.md)
for the full config and a real clarify → refuse → disclose transcript.

## Contributing

```bash
# Before Columna is published to PyPI, install columna-core FIRST (editable), since
# columna-server's `columna-core>=0.7.8` dependency can't yet be resolved from an index:
pip install -e packages/columna-core
pip install -e "packages/columna-server[test]"      # brings pytest + the MCP client harness

pytest packages/columna-core -q       # warehouse proofs skipped unless COLUMNA_BENCH_WAREHOUSE is set
pytest packages/columna-server -q     # MCP stdio acceptance + the packaged demo
```

The repo is a uv workspace: `packages/columna-core` (the engine + wire contract) and
`packages/columna-server` (the MCP server). See [`CLAUDE.md`](CLAUDE.md) for the current work package,
[`specs/`](specs/) for the design record, and [`research/`](research/) for the theory behind the four
moods.

## License

Apache-2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

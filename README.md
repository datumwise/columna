# Columna

Also, read the launch post: why we built this.

**Columna is an honest metrics engine.** It sits between your questions and your warehouse and
refuses to return a confident wrong number: where a metric is ambiguous, non-reconciling, or
out-of-domain, it says so instead of guessing. Every answer is one of **four moods** — *serve*,
*disclose*, *clarify*, or *refuse* — returned as structured data on one contract, identical on every
surface (Python, MCP, and a natural-language agent).

## Quickstart (ten minutes, no source checkout)

```bash
pip install columna
columna-server demo --play
```

`pip install columna` is the canonical install — the metapackage that pulls in `columna-core` (the
engine) and `columna-server` (the MCP server + agent). You can still install the two directly
(`pip install columna-core columna-server`) if you want only one.

`demo --play` runs the real wedge end to end and pretty-prints the actual wire JSON for three of the
four moods in one flow:

- **clarify** — a rate whose two measures span different populations is ambiguous; the server names
  the candidate populations as substitutable alternatives instead of inventing a number.
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
path — is the reliable choice.) See
[`packages/columna-server/demos/mcp_claude_desktop.md`](packages/columna-server/demos/mcp_claude_desktop.md)
for the full config and a real clarify → refuse → disclose transcript.

Or talk to it in natural language — Columna's own agent is a true MCP client over the server:

```bash
pip install "columna-server[agent]"
ANTHROPIC_API_KEY=... columna-server agent          # chat REPL over the packaged demo
```

The agent turns your question into a *proposed* Frame-QL query and lets the four moods drive the
conversation — it never touches the engine in-process, never auto-picks a clarify, and every number
comes verbatim from the wire. See
[`packages/columna-server/demos/agent_transcript.md`](packages/columna-server/demos/agent_transcript.md).

## Contributing

```bash
git clone https://github.com/datumwise/columna && cd columna
pip install -e packages/columna-core -e "packages/columna-server[test]"

pytest packages/columna-core -q       # warehouse proofs skipped unless COLUMNA_BENCH_WAREHOUSE is set
pytest packages/columna-server -q     # MCP stdio acceptance + the packaged demo + the agent
```

The repo is a uv workspace: `packages/columna-core` (the engine + wire contract) and
`packages/columna-server` (the MCP server + NL agent). See [`CLAUDE.md`](CLAUDE.md) for the project
state, [`specs/`](specs/) for the design record, and [`research/`](research/) for the theory behind
the four moods.

## License

Apache-2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

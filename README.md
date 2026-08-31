# Columna

Also, read the launch post: why we built this.

**Columna is an honest data framework.** It sits between your questions and your warehouse and
refuses to return a confident wrong number: where a metric is ambiguous, non-reconciling, or
out-of-domain, it says so instead of guessing. Every answer is one of **four moods** — *serve*,
*disclose*, *clarify*, or *refuse* — returned as structured data on one contract, identical on every
surface (Python, MCP, and a natural-language agent).

## Quickstart (ten minutes, no source checkout)

```bash
pip install columna
columna-server demo --play
```

**Requires Python 3.10–3.13, 64-bit.**

`pip install columna` is the canonical install — the metapackage that pulls in `columna-core` (the
engine) and `columna-server` (the MCP server + agent). You can still install the two directly
(`pip install columna-core columna-server`) if you want only one.

> **If pip says "no matching distribution found for columna"** — you are almost certainly on Python
> 3.14, or on 32-bit Python. `columna-core` depends on `datasketches` for HLL, and datasketches 5.x
> publishes no 3.14 wheels on any platform and no 32-bit Windows wheels at all. We declare
> `requires-python = ">=3.10,<3.14"` so pip refuses cleanly instead of dropping you into a C++
> source build that fails minutes later. Install into a 3.10–3.13 64-bit interpreter.
> Python 3.14 support arrives when datasketches ships cp314 wheels, or via the optional-extras
> split already scoped as WP-1.1.

`demo --play` runs four real asks end to end and pretty-prints the actual wire JSON for all four
moods in one flow:

- **clarify** — `SELECT avg(aov) AT {cal.month}`: the inline reduction leaves the input anchor for `aov`
  underdetermined; the server names the candidate input anchors as substitutable alternatives instead
  of inventing one.
- **refuse** — `SELECT level.last AT {customer}`: inventory is keyed by store and day — it has no customers, so
  the ask addresses outside the contracted space and the server refuses with the reason (never a guess).
- **disclose** — `SELECT buyers AT {cal.month}`: distinct buyers per month is a lawful question and the
  server answers it — but it counts distinct customers from a sketch, not by holding every id in memory,
  so the numbers arrive **with** a material caveat carrying the estimator and its relative error
  (HLL, ≈1.6%). Disclose is not a softer refusal: the ask is sound, and the one condition on the answer
  travels with it instead of being left for the reader to discover.
- **serve** — `SELECT aov AT {cal.month}`: average order value by calendar month, one population and well posed;
  the server returns the numbers.

The four moods sort by *lawfulness*, not by confidence: **serve** — lawful, no material condition;
**disclose** — lawful, a material condition travels with the answer; **clarify** — several lawful
meanings remain; **refuse** — no lawful path exists. A structurally prohibited reduction is a refuse,
not a disclosed serve: `SELECT stock.sum AT {store*cal.month}` — summing a stock along a lineage its
`sum` is declared `BLOCKED` along — returns no numbers at all, in every spelling, including
`sum(stock.last@day)` and any expression wrapping it. Family generation creates a new analytical family;
it does not create a new operator permission. *(Ratified 2026-08-20, ADR-036; this leg of the demo used
to be the disclose leg.)*

That transcript *is* the product. (No path arguments needed — the demo Manifold and a small warehouse
ship in the package. For a richer run over the full benchmark warehouse, see
[`packages/columna-server/README.md`](packages/columna-server/README.md).)

### What the demo is, and what it is not

The demo Manifold (**Cascadia**) is **hand-authored**. It carries no `SOURCE_MANIFOLD`, admission
classifies it `ENTRY_LEGACY`, and it demonstrates *serving* — the four moods, the disclosure
contract, the refusals. **It does not demonstrate the governed path**, and nothing here should be
read as saying it does.

The governed path has its own artifact and it ships in `columna-server`: the **firstlight** runtime
unit (`columna_server/governed/firstlight/`) — a governed publication, a compiled execution image,
and a **lowering receipt** binding them — admitted as `ENTRY_GOVERNED` and exercised end to end by
standing tests. That is the repository's governed machine evidence.

One more piece of honest typing, because a reader can only infer it from silence otherwise: these
packages **consume** governed publications; they do not **produce** them. The author → ratify →
publish third of the lifecycle is not in the published packages, and no public governed authoring
surface is open (topology record §17.2).

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
for the full config and a real clarify → refuse → disclose → serve transcript.

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

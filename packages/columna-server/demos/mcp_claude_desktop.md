# Columna MCP server — Claude Desktop config + the AOV clarify → answer flow

The Columna MCP server exposes a library of Manifolds to any MCP client (Claude Desktop, a local
agent, or Columna's own NL agent) over **one contract**: the four moods — serve · disclose ·
clarify · refuse — arrive as *data*, identical to the Python API. This is the first metrics MCP
server that can say **"it depends."**

## 1. Configure Claude Desktop

Add the server to `claude_desktop_config.json` (macOS:
`~/Library/Application Support/Claude/claude_desktop_config.json`). `stdio` is the canonical
transport — Claude Desktop launches the process and speaks MCP over its stdin/stdout:

```jsonc
{
  "mcpServers": {
    "columna": {
      "command": "columna-server",
      "args": ["mcp", "--manifolds", "/abs/path/to/manifolds"]
    }
  }
}
```

`--manifolds` points at a directory of `<id>/manifold.cml` + `data.toml` (connector type + data
path). All Manifolds are parsed and connected **once** at startup; `list_manifolds` / `describe_*`
never touch data, and `explain` executes nothing (`fetches_delta: 0`).

Five read-only tools appear: `list_manifolds`, `describe_manifold`, `describe_measure`, `query`,
`explain`. There is **no SQL** and **no write surface** of any kind.

> Remote transport: `columna-server mcp --manifolds <dir> --http :8000`. When `COLUMNA_MCP_TOKEN`
> is set, every request must carry `Authorization: Bearer <token>` (constant-time checked); when it
> is unset, HTTP binds loopback-only and warns.

## 2. The AOV clarify → answer flow (a real transcript)

The wedge: ask for a rate whose two measures live over *different populations* — `revenue` (over
`transactions`) per `level.last` (over `store_days`). A SQL/metrics layer would silently emit a
number. Columna **clarifies**, and the clarify is machine-actionable.

### Query — "average order value per unit of inventory, by store and day"

```
query(manifold_id="benchmark", frameql="aov_rate: revenue / level.last @ store, day")
```

The server returns `outcome: clarify` — the rate's population is ambiguous, and it names the
candidate populations as **mechanically substitutable** alternatives (`apply.universe`):

```json
{
  "contract_version": "1",
  "outcome": "clarify",
  "columns": [{
    "name": "aov_rate", "status": "clarify",
    "no_result": {
      "kind": "clarify", "discriminator": "ambiguous", "reason": "co_anchor_ambiguous",
      "detail": "ratio combines measures over different populations ['store_days', 'transactions'] … which population should the rate be taken over?",
      "alternatives": [
        {"token": "on_universe('store_days')",   "description": "express both numerator and denominator within universe 'store_days'",   "apply": {"universe": "store_days"}},
        {"token": "on_universe('transactions')", "description": "express both numerator and denominator within universe 'transactions'", "apply": {"universe": "transactions"}}
      ]
    }
  }]
}
```

### Hop 1 — apply a pin token; the server is honest, not eager

The agent picks the first alternative and re-issues the query with `apply.universe`:

```
query(manifold_id="benchmark", frameql="aov_rate: revenue / level.last @ store, day", universe="store_days")
```

The clarify resolves to a **refuse** with an informative reason — pinning to `store_days` makes the
numerator out-of-domain, so there is no faithful rate over that population (it does **not** invent a
number):

```json
{
  "outcome": "refuse",
  "columns": [{
    "name": "aov_rate", "status": "refuse",
    "no_result": {
      "kind": "refuse", "discriminator": "unsupported", "reason": "out_of_universe",
      "detail": "revenue is bound to universe 'transactions', not the pinned population 'store_days' — it is not defined over that population"
    }
  }]
}
```

### Hop 2 — reformulate per the clarify's detail; serve, disclosed

Following the clarify's guidance, the agent asks for the two measures as **separate columns** over
the union population rather than as one rate. Now the server **serves** the numbers and rides the
population caveat on the frame — surfaced, filterable, `material`:

```
query(manifold_id="benchmark", frameql="revenue: revenue, inv: level.last @ store, day")
```

```json
{
  "outcome": "serve",
  "frame": {
    "rollup_severity": "info",
    "disclosures": [
      {"code": "denominator_population", "materiality": "material", "severity": "info",
       "category": "coverage",
       "detail": "frame spans multiple universes ['store_days', 'transactions'] — population is ambiguous; pin it with ON UNIVERSE"}
    ]
  },
  "columns": [
    {"name": "revenue", "status": "served", "population": "transactions",
     "values": [{"store": "S001", "day": "2024-01-03", "value": 58.26}, "…"]},
    {"name": "inv", "status": "served", "population": "store_days",
     "values": [{"store": "S001", "day": "2024-01-01", "value": 5693.0}, "…"]}
  ]
}
```

**The point:** the ambiguity was never guessed away. The agent got a *structured* clarify, tried a
pin (honest refuse), and reformulated into a served-and-disclosed answer — the same conversation a
careful analyst would have, driven entirely by machine-readable fields. One contract, every surface.

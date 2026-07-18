# Columna, by datumwise — honest metrics engine

**Columna** is an honest metrics engine: a grammar layer for analytics that serves a number *and its
disclosure together* — serve, disclose, clarify, refuse — so an AI agent (or a person) never receives
a plausible-but-wrong answer with no way to tell.

This package (`columna`) is the **metapackage**: the canonical one-line install of the whole system.

```
pip install columna
```

It installs:

- **[`columna-core`](https://pypi.org/project/columna-core/)** — the column-foundation engine
  (multi-table, transport-based, correctness-governed): the Manifold object model, Frame-QL, the four
  moods, and the Certificate kernel.
- **[`columna-server`](https://pypi.org/project/columna-server/)** — the read-only MCP server and the
  natural-language query agent over one wire contract.

The implementation lives in those packages; import from `columna_core` and `columna_server`. The
metapackage carries no code of its own beyond a version that rides in lockstep with `columna-core`.

## Links
- Home: <https://datumwise.ai>
- Source & issues: <https://github.com/datumwise/columna>
- License: Apache-2.0

# Columna, by datumwise — honest data framework

**Columna** is an honest data framework: a grammar layer for analytics that serves a number *and its
disclosure together* — serve, disclose, clarify, refuse — so an AI agent (or a person) never receives
a plausible-but-wrong answer with no way to tell.

This package (`columna`) is the **metapackage**: the canonical one-line install of the whole system.

```
pip install columna
```

**Requires Python 3.10–3.13, 64-bit.**

> **If pip says "no matching distribution found for columna"** — you are almost certainly on Python
> 3.14, or on 32-bit Python. `columna-core` depends on `datasketches` for HLL, and datasketches 5.x
> publishes no 3.14 wheels on any platform and no 32-bit Windows wheels at all. We declare
> `requires-python = ">=3.10,<3.14"` so pip refuses cleanly instead of dropping you into a C++
> source build that fails minutes later. Install into a 3.10–3.13 64-bit interpreter.
> Python 3.14 support arrives when datasketches ships cp314 wheels, or via the optional-extras
> split already scoped as WP-1.1.

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

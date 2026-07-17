"""
columna_server.server — the MCP server wiring.

Registers the five read-only tools on a FastMCP instance over a ManifoldStore. Each tool returns
the wire-contract dict (FastMCP serializes it to a JSON content block); structural input errors
raise, surfaced by MCP as an error result. There is no write tool and no SQL path.
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import tools as T
from .store import ManifoldStore


def build_server(store: ManifoldStore, name: str = "columna") -> FastMCP:
    mcp = FastMCP(name)

    @mcp.tool()
    def list_manifolds() -> dict:
        """List the Manifolds this server hosts (id, name, description, measure count, universes).
        Touches no data."""
        return T.list_manifolds(store)

    @mcp.tool()
    def describe_manifold(manifold_id: str) -> dict:
        """Describe a Manifold: dimensions/levels, functional edges (with lineage), universes
        (name + rendered predicate), and the measure index. Touches no data."""
        return T.describe_manifold(store, manifold_id)

    @mcp.tool()
    def describe_measure(manifold_id: str, measure: str) -> dict:
        """Describe one measure: the family (root, members, reducer kinds), per-member anchors
        (blocked lineages, order-by, monoid), dtype, v-anchor {universe, grain}, m-anchor, and
        provenance. Touches no data."""
        return T.describe_measure(store, manifold_id, measure)

    @mcp.tool()
    def query(manifold_id: str, frameql: str) -> dict:
        """Execute a FrameQL envelope statement (`SELECT <series [AS alias]>,… AT {anchor}` with optional
        WHERE/HAVING/ORDER BY/LIMIT n PER {dims}; never SQL; the terse `cols @ anchor` form is retired).
        Returns the wire contract: outcome (serve/disclose/clarify/refuse/error) with per-column values
        and structured disclosures. Universe is resolved structurally (§2c) — never named in a query."""
        return T.query(store, manifold_id, frameql)

    @mcp.tool()
    def explain(manifold_id: str, frameql: str) -> dict:
        """EXPLAIN a FrameQL envelope statement WITHOUT executing it — the cheap inner loop. Returns the
        canonical DESUGARED form (the exact artifact the planner consumed), per-series atom
        decomposition, the dependency cone with current verdicts, and the would-be outcome + disclosures
        — touching ZERO data (`fetches_delta` is 0). A first-class tool beside `query`."""
        return T.explain_statement(store, manifold_id, frameql)

    return mcp

"""
columna_server.server — the MCP server wiring.

Registers the five read-only tools on a FastMCP instance over a ManifoldStore. Each tool returns
the wire-contract dict (FastMCP serializes it to a JSON content block); structural input errors
raise, surfaced by MCP as an error result. There is no write tool and no SQL path.
"""
from __future__ import annotations

from typing import Optional

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
    def query(manifold_id: str, frameql: str, universe: Optional[str] = None) -> dict:
        """Execute a Frame-QL query (`<columns> @ <anchor>`; never SQL). Returns the wire contract:
        outcome (serve/disclose/clarify/refuse/error) with per-column values and structured
        disclosures. `universe` pins the population (ON UNIVERSE)."""
        return T.query(store, manifold_id, frameql, universe)

    @mcp.tool()
    def explain(manifold_id: str, frameql: str, universe: Optional[str] = None) -> dict:
        """Explain a Frame-QL query WITHOUT executing it: the would-be outcome + disclosures with
        zero backend fetches (`fetches_delta` is asserted 0). Same query grammar as `query`."""
        return T.explain(store, manifold_id, frameql, universe)

    return mcp

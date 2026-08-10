"""
columna_server.server — the MCP server wiring.

Registers the read-only tools on a FastMCP instance over a ManifoldStore. The engine tool
(`execute_frame_query`, with `query` as a deprecated alias) plus the no-engine half — `discovery`,
`check_frame_query`, `frame_ql_grammar`, `explain`, `get_evidence`, `manifold_status` — which
introspect and validate WITHOUT touching data. Each tool
returns the wire-contract dict (FastMCP serializes it to a JSON content block); structural input
errors raise, surfaced by MCP as an error result. There is no write tool and no SQL path.
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
    def execute_frame_query(manifold_id: str, frameql: str) -> dict:
        """Execute a FrameQL envelope statement (`SELECT <series [AS alias]>,… AT {anchor}` with optional
        WHERE/HAVING/ORDER BY/LIMIT n PER {dims}; never SQL; the terse `cols @ anchor` form is retired)
        OVER REAL DATA. Returns the wire contract: outcome (serve/disclose/clarify/refuse/error) with
        per-column values and structured disclosures, annotated `executed: true` + `fetches_delta`. The
        executing counterpart to `check_frame_query`. Universe is resolved structurally (§2c)."""
        return T.execute_frame_query(store, manifold_id, frameql)

    @mcp.tool()
    def query(manifold_id: str, frameql: str) -> dict:
        """DEPRECATED alias for `execute_frame_query` (removed after 0.9.x); the wire is identical.
        Retained one release so existing clients do not break — prefer `execute_frame_query`."""
        return T.query(store, manifold_id, frameql)

    @mcp.tool()
    def explain(manifold_id: str, frameql: str) -> dict:
        """EXPLAIN a FrameQL envelope statement WITHOUT executing it — the cheap inner loop. Returns the
        canonical DESUGARED form (the exact artifact the planner consumed), per-series atom
        decomposition, the dependency cone with current verdicts, and the would-be outcome + disclosures
        — touching ZERO data (`fetches_delta` is 0). A first-class tool beside `query`."""
        return T.explain_statement(store, manifold_id, frameql)

    @mcp.tool()
    def check_frame_query(manifold_id: str, frameql: str) -> dict:
        """Validate a FrameQL statement over a manifold WITHOUT executing it — the cheap pre-flight.
        Parse + plan (typecheck, addressability, single-universe, pin laws) touching ZERO data, and
        return the would-be mood (serve/disclose/clarify/refuse/error) with alternatives for an
        ill-posed ask. A syntax error is an `error` wire. Thinner than `explain` (no cone)."""
        return T.check_frame_query(store, manifold_id, frameql)

    @mcp.tool()
    def frame_ql_grammar() -> dict:
        """The FrameQL (envelope) query grammar VERBATIM, with the columna-core version it came from —
        so a caller writes a valid query rather than guessing its shape. Touches no manifold, no data."""
        return T.frame_ql_grammar()

    @mcp.tool()
    def discovery(manifold_id: str) -> dict:
        """What can be asked of this manifold WITHOUT touching data: the measures (with their reducer
        family and universe/grain) and the anchors (universes with base grain) a `SELECT <measure> AT
        {anchor}` can name. The starting point before any query. Logical names only."""
        return T.discovery(store, manifold_id)

    @mcp.tool()
    def manifold_status(manifold_id: str) -> dict:
        """The manifold's health at a glance WITHOUT touching data: counts (measures, universes, levels,
        hierarchies, relations, edges, derived), the published serving scope (edges blocked by refuted
        hierarchies), and the evidence standing (Licenses verified / corroborated / untestable)."""
        return T.manifold_status(store, manifold_id)

    @mcp.tool()
    def get_evidence(manifold_id: str, measure: str | None = None) -> dict:
        """The evidence behind a manifold's claims WITHOUT touching data: each measure's declared
        evidence grade and each functional edge's, plus the adjudicated Licenses (verdict, lineages,
        basis, attestation). With `measure`, scoped to that measure's family and universe."""
        return T.get_evidence(store, manifold_id, measure)

    @mcp.tool()
    def case_chapter(chapter: str) -> dict:
        """Fetch ONE case-demo chapter VERBATIM — the on-demand document behind the moods. `chapter` is
        ch1 (the purpose and the requirement), ch2 (the design's reasons), or ch3 (the behaviors and the
        moods). Consult it when relaying a clarify/refuse/caveat, or a why/folklore question — not on a
        plain serve. See `case_manifest` for routing."""
        return T.case_chapter(chapter)

    @mcp.tool()
    def case_manifest() -> dict:
        """The 3-descriptor routing manifest for the case document: which chapter answers which 'why'."""
        return T.case_manifest()

    return mcp

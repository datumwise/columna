"""
columna_core.projection — the planner-facing PROJECTION of a Manifold (vocabulary/shape).

A Manifold is ONE authored graph, but it has TWO projections of it:

  • the PLANNER gets VOCABULARY/SHAPE — logical names, the rollup/transport DAG *topology*
    (frm->to plus a lineage tag, with NO physical columns), measure families (member NAMES
    only), derived formulas, and the M:N edges for fan-out diagnostics. It reasons about WHAT
    is addressable and whether a frame is well-formed (fan-out, out-of-universe, unknown
    column), purely from structure.

  • the ENGINE gets RESOLUTION — the full Manifold: realizations, sources (home_table,
    pre_expr, realized_by, provider_table/frm_col/to_col), the universe predicate, missingness,
    costs, the operator registry. It reasons about HOW to faithfully and cheaply deliver a
    column, and co-computes the resolution-dependent disclosures/refusals.

The PlannerView below makes "the planner cannot see provenance" STRUCTURAL rather than
conventional: the planner holds this view, and the provenance fields are simply not present
on it to be read. Two find_paths exist over the same topology — the planner's returns
shape (existence + lineage, no physical columns); the engine's returns FunctionalEdges it
can deliver along. That pair is the two-projection idea in miniature.

(The planner->engine handoff is a logical request (measure, member, anchor); the engine->planner
return is a frame + a Disclosure — caveats, not sources. Disclosures cross the boundary;
provenance does not.)

Locus note: B-anchor CROSSING DETECTION is structural — knowable from the b-anchor's
blocked_lineages and the path/out-edge lineages (both shape, not provenance) — so it lives
HERE, in the planner (compile phase), alongside fan-out and out-of-universe. The `blocked`
lineages are therefore surfaced on the shape projection (a structural declaration of which axes
a reducer does not reconcile along — not the b-anchor mechanics, which stay engine-side). A
crossing is SERVED with a critical b_anchor_crossing disclosure (inform-and-serve, ADR-020) —
never a refusal; the planner detects it and the served contract is unchanged. Because detection
is now static, EXPLAIN can show the would-be crossing WITHOUT executing (plan()).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from collections import deque


@dataclass(frozen=True)
class MeasureShape:
    name: str
    universe: str
    family: tuple          # member NAMES only — no order_by, home_table, pre_expr
    logical_type: str = "Float64"   # the DECLARED logical dtype (vocabulary) — not the physical type
    blocked: dict = field(default_factory=dict)   # member -> frozenset(blocked_lineages): the B-anchor,
                                                  # as SHAPE (which axes the reducer does not reconcile along)

@dataclass(frozen=True)
class OperatorSig:
    """An operator's SIGNATURE — the vocabulary the planner typechecks and ROUTES against:
    name, KIND (reducer/scan/map), accepts, out_rule, and the order/window/core flags it needs
    to route. The mechanics (witness/combine/deliver_sql/scan_impl) are resolution and stay
    engine-side; the planner never sees them. `is_monoid` is structural (does this reducer reduce
    by combine at all) — it gates the B-anchor crossing check, which applies only to monoid reducers."""
    name: str
    kind: str              # reducer | scan | map  (the umbrella discriminant the planner routes on)
    accepts: frozenset     # logical dtypes this operator accepts
    out_rule: str          # output dtype: "same", a concrete dtype tag, or "numeric_widen"
    needs_order: bool = False
    needs_window: bool = False
    in_core: bool = True
    is_monoid: bool = True  # reducer reduces by an associative combine (holistic => False)
    linear: bool = False    # ALGEBRAIC (WP-B): preserves linear combinations — the sum-fertility
                            # symbolic gate (sum,+,-,neg True; *,/ conditional via the scalar rule)

@dataclass(frozen=True)
class UniverseShape:
    name: str
    base_dimensions: frozenset    # NO predicate (confinement is an engine/resolution concern)

@dataclass(frozen=True)
class DerivedShape:
    name: str
    formula: str
    resolution_anchor: Optional[str] = None   # declared `AT <level>` — routes the distinct AT-metric reading
    members: tuple = ()                        # declared family member names (shape: which reducers travel)

@dataclass(frozen=True)
class ShapeEdge:
    frm: str
    to: str
    lineage: str           # topology + lineage tag only; NO frm_col/to_col/provider_table


class PlannerView:
    """A provenance-free projection of a Manifold, for the planner."""

    def __init__(self, m):
        from .operators import REGISTRY
        self.measures = {n: MeasureShape(n, mc.universe, tuple(mc.family), mc.logical_type,
                                         {mem: frozenset(fm.b_anchor.blocked_lineages)
                                          for mem, fm in mc.family.items()})
                         for n, mc in m.measures.items()}
        self.universes = {n: UniverseShape(n, u.base_dimensions)
                          for n, u in m.universes.items()}
        self.derived = {n: DerivedShape(n, d.formula, d.resolution_anchor, tuple(d.family))
                        for n, d in m.derived.items()}
        self.non_functional = tuple(m.non_functional)         # (frm, to, detail) — level names only
        self.levels = frozenset(m.levels)                      # declared level names (incl. edgeless base levels)
        self._edges = tuple(ShapeEdge(e.frm, e.to, e.lineage) for e in m.edges)
        # operator SIGNATURES (vocabulary): name -> (kind, accepts, out_rule, flags). NOT mechanics.
        self.operators = {n: OperatorSig(n, op.kind, op.accepts, op.out_rule,
                                         op.needs_order, op.needs_window, op.in_core, op.is_monoid,
                                         op.linear)
                          for n, op in REGISTRY.items()}

    def output_dtype(self, op_name: str, in_dtype: str) -> str:
        sig = self.operators[op_name]
        return in_dtype if sig.out_rule == "same" else sig.out_rule

    def _out(self, level):
        return [e for e in self._edges if e.frm == level]

    def out_edges(self, level):
        """Public: the shape edges leaving a level (frm, to, lineage). Used by B-anchor crossing
        detection to see which lineages a collapsed base dimension exits along."""
        return self._out(level)

    def find_path(self, from_levels, target):
        """Existence/topology BFS over the SHAPE DAG. Returns a shape path (start, edges)
        with NO physical columns, or None. The planner only ever checks `is not None`."""
        if target in from_levels:
            return (target, ())
        q = deque((b, b, ()) for b in from_levels)
        seen = set(from_levels)
        while q:
            start, cur, path = q.popleft()
            for e in self._out(cur):
                if e.to == target:
                    return (start, path + (e,))
                if e.to not in seen:
                    seen.add(e.to)
                    q.append((start, e.to, path + (e,)))
        return None

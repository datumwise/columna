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
from contextlib import contextmanager


@dataclass(frozen=True)
class MeasureShape:
    name: str
    universe: str
    family: tuple          # member NAMES only — no order_by, home_table, pre_expr
    logical_type: str = "Float64"   # the DECLARED logical dtype (vocabulary) — not the physical type
    blocked: dict = field(default_factory=dict)   # member -> frozenset(blocked_lineages): the B-anchor,
                                                  # as SHAPE (which axes the reducer does not reconcile along)
    fill_rule: Optional[str] = None   # Φ_v, the M-contract fill rule (columna#143) — SHAPE the planner reads
                                      # to drive absence semantics; None = undeclared (disclose, never fill)

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
    basis: Optional[str] = None   # B3 population kind: events|spine|product|registry (absence semantics)

@dataclass(frozen=True)
class DerivedShape:
    """A derived column, as SHAPE — including its SUCCESSOR-FAMILY LAW.

    TWO POLARITIES, DELIBERATELY NOT UNIFIED (ruling 2026-08-20). `MeasureShape.blocked` is a
    NEGATIVE law: a measure family is OPEN by default and `BLOCKED { lineage }` closes an operator
    over those lineages. `DerivedShape.member_lineages` is the mirror POSITIVE law: a derived
    successor family is CLOSED by default and `FERTILE { lineage }` establishes travel. Absence
    means opposite things on the two sides — no permission here, no prohibition there — so a
    consumer must know which one it is reading. They are never merged into one default.

    Before 2026-08-20 this shape carried member NAMES only, so authored positive family law was
    invisible to planning and `FERTILE { calendar }` and `FERTILE { }` were behaviourally identical
    (both travelled and served clean). The law existed, was adjudicated, and was never consulted."""
    name: str
    formula: str
    resolution_anchor: Optional[str] = None   # declared `AT <level>` — routes the distinct AT-metric reading
    members: tuple = ()                        # declared family member names (shape: which reducers travel)
    member_lineages: dict = field(default_factory=dict)   # member -> frozenset(FERTILE lineages): the POSITIVE
                                                          # successor law. Absence of a lineage = NO permission.
    member_license: dict = field(default_factory=dict)    # member -> adjudicated verdict | None. PROJECTED for
                                                          # describe/EXPLAIN legibility ONLY. Planning gates on
                                                          # the DECLARATION (member_lineages), never on the
                                                          # verdict: License is the adjudicator's equality
                                                          # theorem for the reduce-path optimization, and
                                                          # reinterpreting UNTESTABLE as "may not travel" would
                                                          # silently redefine it (ruling 2026-08-20 §3).

@dataclass(frozen=True)
class ShapeEdge:
    frm: str
    to: str
    lineage: str           # topology + lineage tag only; NO frm_col/to_col/provider_table

    @property
    def key(self):
        """This edge's certification identity — the SAME EdgeKey the full FunctionalEdge yields, so the
        planner's shape view and the adjudicator's verdicts name the same subject (P0.5a GAP 3)."""
        from .model import EdgeKey
        return EdgeKey(self.lineage, self.frm, self.to)


@dataclass(frozen=True)
class FaceShape:
    """A declared crossing face, as SHAPE — name + scheme + folklore, for the clarify-as-menu. NO
    license and NO VIA bridge (both are engine/adjudication concerns; the planner cannot see provenance)."""
    name: str
    scheme: str
    description: str = ""
    driver: str = ""       # the driver measure-ref for assign/alloc ('' for touch) — additive to the menu

@dataclass(frozen=True)
class RelateShape:
    """A non-functional (M:N) relationship, as SHAPE — logical endpoints + NOTE + declared faces. The VIA
    bridge (table/columns) is STRUCTURALLY absent here: the planner reasons about addressability and mints
    the clarify menu from names alone; the engine (full Manifold) holds the bridge to actually cross."""
    frm: str
    to: str
    detail: str = ""
    faces: tuple = ()      # (FaceShape, ...)


class PlannerView:
    """A provenance-free projection of a Manifold, for the planner."""

    def __init__(self, m):
        from .operators import REGISTRY, canonical, SERIES_REDUCERS
        self.canonical_op = staticmethod(canonical).__func__   # surface spelling -> canonical operator
        self.series_reducers = SERIES_REDUCERS                 # reducers that may collapse a resolved series
        self.measures = {n: MeasureShape(n, mc.universe, tuple(mc.family), mc.logical_type,
                                         {mem: frozenset(fm.b_anchor.blocked_lineages)
                                          for mem, fm in mc.family.items()},
                                         fill_rule=mc.fill_rule)
                         for n, mc in m.measures.items()}
        self.universes = {n: UniverseShape(n, u.base_dimensions, u.basis)
                          for n, u in m.universes.items()}
        self.derived = {n: DerivedShape(n, d.formula, d.resolution_anchor, tuple(d.family),
                                        {mem: frozenset(fm.declared_lineages)
                                         for mem, fm in d.family.items()},
                                        {mem: (fm.license.verdict if fm.license else None)
                                         for mem, fm in d.family.items()})
                        for n, d in m.derived.items()}
        self.non_functional = tuple(                          # RelateShape — level names + face shapes, NO VIA
            RelateShape(r.frm, r.to, r.detail,
                        tuple(FaceShape(f.name, f.scheme, f.description, f.selection) for f in r.faces))
            for r in m.non_functional)
        self.levels = frozenset(m.levels)                      # declared level names (incl. edgeless base levels)
        self._edges = tuple(ShapeEdge(e.frm, e.to, e.lineage) for e in m.edges)
        # P0.5a CLOSED-BY-DEFAULT TRANSPORT. EVERY FunctionalEdge is certification-dependent: transport
        # serves only across an edge adjudication positively ADMITTED. There is deliberately no
        # "this edge carries no hierarchy, therefore admit it" branch — that was a second, silent
        # authority model (ruling 2026-08-11), and since HIERARCHY is the parser's only FunctionalEdge
        # surface a governed .cml never needed it. A Manifold built directly in Python with no
        # hierarchies now certifies nothing and therefore transports nothing: legacy construction does
        # not inherit governed status by omission.
        self.certified_edges: frozenset = frozenset()          # EdgeKey(lineage, frm, to) — admitted transport
        # P0.5a ADJUDICATION PROBE. The adjudicator ESTABLISHES certification by querying across the very
        # edges/faces it is testing — under the serving gate it could never certify anything (the claim is
        # closed until proven, and the proof needs the transport). So adjudication runs against the DECLARED
        # shape, in this explicitly-scoped window, and its results never reach a caller: they become verdicts.
        # This is the ONLY bypass, it is not reachable from the query path, and it always restores.
        self._probing: int = 0
        # P0.5b-0: set once per REQUEST — the certified edges whose EVIDENCE has gone stale because
        # a table its proof read has moved. Contingent evidence may not outlive the data identity it
        # was established against; a table no proof read closes nothing.
        self._stale_edges: frozenset = frozenset()
        # operator SIGNATURES (vocabulary): name -> (kind, accepts, out_rule, flags). NOT mechanics.
        self.operators = {n: OperatorSig(n, op.kind, op.accepts, op.out_rule,
                                         op.needs_order, op.needs_window, op.in_core, op.is_monoid,
                                         op.linear)
                          for n, op in REGISTRY.items()}

    def output_dtype(self, op_name: str, in_dtype: str) -> str:
        sig = self.operators[op_name]
        return in_dtype if sig.out_rule == "same" else sig.out_rule

    def install_certified_edges(self, certified: frozenset):
        """P0.5a: install the positive edge-admission set (from the PublishedScope). One assignment
        boundary — the planner never mutates this piecemeal around fallible work."""
        self.certified_edges = frozenset(certified)

    @property
    def probing(self) -> bool:
        """True inside an adjudication probe window — the gate is lifted because the query IS the test
        that mints the verdict. Never true on a serving path."""
        return self._probing > 0

    @contextmanager
    def probe(self):
        """Scoped, re-entrant lift of the certification gate for adjudication's own probe queries.
        Always restores (finally), including on Contradiction — a failed publish must not leave the
        shape open."""
        self._probing += 1
        try:
            yield self
        finally:
            self._probing -= 1

    def _out(self, level):                                     # STRUCTURAL — all declared edges
        return [e for e in self._edges if e.frm == level]

    def _admitted(self, e) -> bool:                            # P0.5a — usable for governed transport?
        """Positively admitted for governed transport? Closed unless certified — no structural
        exemption, and the key is the LINEAGE-bearing EdgeKey so one lineage's verdict can never
        license another's edge over the same level pair."""
        if self.probing:
            return True                                        # adjudication tests the DECLARED shape
        if e.key in self._stale_edges:
            return False                                       # P0.5b-0: this edge's evidence is stale
        return e.key in self.certified_edges

    def _out_certified(self, level):                           # P0.5a — ADMITTED edges only
        return [e for e in self._edges if e.frm == level and self._admitted(e)]

    # P0.5a (ruling 2026-08-11): a temporal lineage confers an ORDER AXIS, and the axis is
    # execution-relevant — it decides the sort a scan walks, so it changes shipped numbers. Declared
    # structure may therefore inform caution, but it may not CREATE this capability: an order axis
    # exists only where the hierarchy that would confer it is positively admitted.
    TEMPORAL_LINEAGES = frozenset({"calendar", "fiscal"})

    def orderable_levels(self) -> frozenset:
        """Levels carrying a natural (temporal) order, over ADMITTED edges only.

        The manual's "typically a temporal dimension", read off the certified lineages. An
        uncertified hierarchy contributes nothing: it cannot make an axis derivable and so cannot
        turn "no lawful order axis -> refuse" into "exactly one -> serve"."""
        lv = set()
        for e in self._edges:
            if e.lineage in self.TEMPORAL_LINEAGES and self._admitted(e):
                lv.add(e.frm); lv.add(e.to)
        return frozenset(lv)

    def out_edges(self, level):
        """Public: the shape edges leaving a level (frm, to, lineage). Used by B-anchor crossing
        detection to see which lineages a collapsed base dimension exits along — STRUCTURAL (all declared
        edges), independent of certification."""
        return self._out(level)

    def _bfs(self, from_levels, target, out):
        if target in from_levels:
            return (target, ())
        q = deque((b, b, ()) for b in from_levels)
        seen = set(from_levels)
        while q:
            start, cur, path = q.popleft()
            for e in out(cur):
                if e.to == target:
                    return (start, path + (e,))
                if e.to not in seen:
                    seen.add(e.to)
                    q.append((start, e.to, path + (e,)))
        return None

    def find_path(self, from_levels, target):
        """Existence/topology BFS over the CERTIFIED shape DAG (P0.5a). Returns a shape path (start,
        edges) with NO physical columns, or None. Traverses ONLY positively-admitted edges, so an
        uncertified FunctionalEdge does not establish an addressable transport path. The planner only ever
        checks `is not None`."""
        return self._bfs(from_levels, target, self._out_certified)

    def find_path_any(self, from_levels, target):
        """Existence/topology BFS over the FULL declared shape DAG (ignores certification). Diagnosis
        only: lets the planner distinguish 'declared-but-uncertified transport' (→ uncertified_edge /
        contradicted_edge) from 'out of universe' (no declared path at all)."""
        return self._bfs(from_levels, target, self._out)

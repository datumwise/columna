"""
columna_core.planner — the provenance-blind Frame-QL planner.

Parses a frame's column expressions into canonical (measure.member) @ anchor atoms,
expands derived columns (recursively), TYPECHECKS addressability against the vocabulary
(fan-out and out-of-universe are refused HERE, statically, before the engine is asked),
requests atoms from the engine, evaluates the post-agg expression over the returned
columns, assembles the frame, and folds disclosures. It never sees provenance.
"""
from __future__ import annotations
import ast
import re
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Optional
import polars as pl

from .projection import PlannerView
from .engine import ColumnEngine
from .disclosure import (Disclosure, Refusal, Caveat, TRANSPORT, UNCONFIRMED,
                         DECLARED_FILL, UNKNOWN_ABSENCE, OUT_OF_POPULATION, UNDECLARED_ABSENCE,
                         SERVE, DISCLOSE, CLARIFY, REFUSE, ERROR, AMBIGUOUS, Outcome)
from .model import parse_faced, EdgeKey   # EdgeKey: the certification identity of an edge (P0.5a)

_ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Name, ast.Attribute,
            ast.Load, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub,
            ast.MatMult,  # `@` — the INPUT-ANCHOR pin inside an inline reduction (aov@day)
            ast.Tuple,    # a COMPOSITE input anchor `@ {a*b}` desugars to `@ (a, b)` (WP-GRAIN-1); a
                          # Tuple anywhere else is caught semantically by _infer ("unsupported node")
            ast.Call, ast.keyword)
_OP = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}
_V = "_v"

# ── one adjudicable REDUCTION inside an expression (generated-family law, 2026-08-20) ──────────────
#   op        the canonical operator performing the reduction.
#   frm/to    the grain it reduces FROM and the anchor it reduces ONTO (tuples of level names).
#   subject   how to name this operation back to the reader (surface form, not an internal id).
#   law       the governed BLOCKED lineage set for `op` (the measure B-anchor's NEGATIVE polarity —
#             open by default, so an empty set means no prohibition, never no permission).
#   written   True if the reader spelled the reducer as a declared member; False if it was GENERATED.
_Travel = namedtuple("_Travel", "op frm to subject law written")


def _fmt_anchor(anchor) -> str:
    """Spell an anchor with the canonical product separator `*` (never a comma). Every surface that
    WRITES an anchor — the EXPLAIN header, error/clarify messages, traces — routes through here so no
    output ever emits a comma anchor (capture §2b RULED (a))."""
    if isinstance(anchor, (tuple, list)):
        return "*".join(str(a) for a in anchor)
    return str(anchor)


@dataclass
class ColumnResult:
    name: str
    expr: str
    frame: Optional[pl.DataFrame]
    disclosure: Disclosure
    refusal: Optional[Outcome] = None
    trace: list = field(default_factory=list)
    universe: Optional[str] = None      # the column's sole universe (§2c)
    fill_rule: Optional[str] = None     # Φ_v resolved from the member contract (columna#143) — drives
                                        # absence semantics. None = undeclared (disclose, never fill).


@dataclass
class FrameResult:
    data: Optional[pl.DataFrame]
    disclosure: Disclosure
    columns: list                 # [ColumnResult]
    anchor: tuple

    # ---- the four-outcome contract, surfaced (ADR-032) --------------------
    # Served columns carry a frame (+ disclosure); a no-result column carries a classified
    # refusal. These expose the planner's verdicts so any surface reads them uniformly.
    @property
    def served(self): return [c for c in self.columns if c.refusal is None]

    @property
    def clarifies(self): return [c for c in self.columns if c.refusal and c.refusal.is_clarify]

    @property
    def refusals(self): return [c for c in self.columns if c.refusal and c.refusal.is_refuse]

    @property
    def errors(self): return [c for c in self.columns if c.refusal and c.refusal.is_error]

    @property
    def outcome(self):
        """Frame-level rollup of the strongest signal: refuse > clarify > error > disclose > serve.
        (A mixed frame still reports its served columns in `data`; this names what needs attention.)"""
        if self.refusals: return REFUSE
        if self.clarifies: return CLARIFY
        if self.errors: return ERROR
        if any(c.disclosure.severity == "critical" for c in self.served): return DISCLOSE
        return SERVE

    def explain(self) -> str:
        lines = [f"EXPLAIN  frame @ {_fmt_anchor(self.anchor)}"]
        for c in self.columns:
            head = f"  • {c.name}" + (f" = {c.expr}" if c.expr != c.name else "")
            lines.append(head)
            for t in c.trace:
                lines.append(f"      ├─ {t}")
            if c.refusal:
                lines.append(f"      └─ {c.refusal}")
            else:
                lines.append(f"      └─ {c.disclosure.render_human()}")
        return "\n".join(lines)


class Planner:
    def __init__(self, view: PlannerView, engine: ColumnEngine):
        self.m = view          # provenance-free PROJECTION (vocabulary/shape only)
        self.engine = engine
        # the published SCOPE (set by publish/reattest): the blocked edges of refuted hierarchies. A
        # column whose transport crosses a blocked edge refuses `contradicted_edge`. Serving never
        # outruns the verdicts. (The CUT half — declarations withdrawn by a violated ASSERT, refusing
        # `conflicting_data` — retired with ASSERT in 0.13.0; ruling 2026-07-26.)
        self._scope = None                             # P0.5b-0: the installed PublishedScope
        self._stale_faces: frozenset = frozenset()     # faces whose evidence has gone stale
        self.blocked_edges: frozenset = frozenset()    # {(frm, to)} — transport across these is refused
        self.blocked_by: dict = {}                      # (frm, to) -> [{lineage, key}]
        # P0.5a POSITIVE ADMISSION: crossing faces admitted by adjudication ("frm<->to.name"). Absence =
        # closed. The certified EDGE set lives on the view (drives find_path); faces are checked here at
        # the addressability chokepoint. Both installed together via install_scope (one boundary).
        self.certified_faces: frozenset = frozenset()

    def _refresh_scope_currency(self) -> None:
        """P0.5b-0: settle the realized-data state ONCE PER REQUEST.

        One probe pass serves both consumers, which is what makes them one coherent notion rather
        than two freshness heuristics:

          · the ENGINE CACHE is keyed on the LIVE identity, so a table that moved misses and
            recomputes;
          · EVIDENCE CURRENCY compares live against the identities the scope's evidence was
            established under, PER CAPABILITY — a capability closes only when a table its own proof
            actually read has moved.

        Cost is one single-table aggregate per attested table per request, not per resolve. Every
        column in the request then sees one data state."""
        from .adjudication import stale_capabilities, live_identities
        scope = getattr(self, "_scope", None)
        eng = getattr(self, "engine", None)
        con = getattr(eng, "con", None)
        if scope is None or con is None:
            return
        live = live_identities(con, sorted(getattr(scope, "attested_identities", {}) or {}))
        if eng is not None:
            eng.data_identities = live                 # cache validity follows the LIVE data state
        stale_e, stale_f = stale_capabilities(scope, live)
        self.m._stale_edges = stale_e                  # closed for this request (existing P0.5a ladder)
        self._stale_faces = stale_f

    def install_scope(self, scope) -> None:
        """P0.5a: install a complete PublishedScope as the planner's serving authority — ONE assignment
        boundary (never mutated piecemeal around fallible work). The certified edge set is pushed onto the
        view (it gates find_path); certified faces + the negative explanation sets live here."""
        self._scope = scope
        # P0.5b-0: the engine's cache validity token IS the scope's realized-data identity — one
        # coherent notion, installed at the same single assignment boundary as admission itself.
        eng = getattr(self, "engine", None)
        if eng is not None:
            eng.data_identities = dict(getattr(scope, "attested_identities", {}) or {})
        self.m._stale_edges = frozenset()   # a freshly established scope is current by construction
        self._stale_faces = frozenset()
        self.m.install_certified_edges(getattr(scope, "certified_edges", frozenset()))
        self.certified_faces = getattr(scope, "certified_faces", frozenset())
        self.blocked_edges = getattr(scope, "blocked_edges", frozenset())
        self.blocked_by = getattr(scope, "blocked_by", {})

    def _blocked_transport(self, node, anchor) -> Optional["EdgeKey"]:
        """The BLOCKED edge that explains why a column cannot travel, or None.

        P0.5a (ruling 2026-08-11): the invariant is NOT "refuse if any contradicted edge exists" — it is
        "never execute an edge that is not positively admitted". So a blocked edge is only an
        EXPLANATION, consulted when no CERTIFIED route exists. If a certified route does exist the query
        travels it and answers correctly, even though some other declared route was refuted.

        (A blocked edge can never appear ON a certified route: CONTRADICTED is not CORROBORATED, so it
        is never admitted. Scanning the certified path for blocked edges — as this did before — was
        therefore vacuous, and was how GAP 2 hid.)"""
        if not self.blocked_edges:
            return None
        for measure, _member in self._atoms(node, anchor):
            ms = self.m.measures.get(measure)
            if ms is None:
                continue
            base = self.m.universes[ms.universe].base_dimensions
            for T in anchor:
                if self.m.find_path(base, T) is not None:
                    continue                                    # a certified route exists — travel it
                declared = self.m.find_path_any(base, T)         # else: why not? name the refutation
                if declared is None:
                    continue
                for e in declared[1]:
                    if e.key in self.blocked_edges:
                        return e.key
        return None

    def _blocked_transport_refusal(self, edge) -> "Refusal":
        rec = (self.blocked_by.get(edge) or [{}])[0]
        lineage, key = rec.get("lineage", edge.lineage), rec.get("key")
        return Refusal("contradicted_edge",
            f"transport along edge {edge.frm}->{edge.to} (lineage '{lineage}') is BLOCKED: its declared "
            f"functional dependence is refuted on the attested data (key {key!r} has >1 parent); the "
            f"reduction across it is withheld — serving never outruns the verdicts.",
            edge=f"{edge.frm}->{edge.to}",
            alternatives=("fix the data and re-attest", "amend the hierarchy", "address at a grain that does not cross this edge"))

    def _check_single_universe(self, node, anchor):
        """§2c EXPRESSION LAW: a column expression evaluates in ONE universe and never crosses the
        boundary. Measures from >1 universe in a single expression is a language-law CATEGORY ERROR —
        the ERROR channel (`cross_universe`), not the four moods — named with the two legal paths."""
        unis = sorted({self.m.measures[mm].universe for (mm, _) in self._atoms(node, anchor)
                       if mm in self.m.measures})
        if len(unis) == 1:
            return unis[0]                                   # the column's sole universe (routes B3 absence)
        if not unis:
            return None
        raise Refusal("cross_universe",
                f"this column combines measures from more than one universe {unis} — a column "
                f"expression evaluates in ONE universe and never crosses the boundary (combining them "
                f"would assert a single population that does not exist). Two legal paths: juxtapose "
                f"(ask each measure as its own column — they align on the shared anchor), or declare "
                f"(define a DERIVED that carries its population, then ask that).",
                alternatives=("juxtapose: ask each measure as its own column",
                              "declare: define a DERIVED with its population, then ask it"))

    # ---- the ROUTE PLAN (P0.5a): the planner selects, the engine executes ---------------------
    @staticmethod
    def _route(path):
        """A certified shape path -> the wire the engine consumes: (start, (EdgeKey, ...))."""
        return (path[0], tuple(e.key for e in path[1]))

    def plan_order_axis(self, scan_op: str, measure: str, anchor: tuple, by=None) -> str:
        """The lawful ORDER AXIS for a scan @ anchor — the planner's decision, not the engine's.

        P0.5a: the axis is execution-relevant (it fixes the sort the scan walks, so it moves shipped
        numbers), so it is derived from POSITIVELY ADMITTED hierarchy structure only. An explicit
        `by=` is the author naming the axis and is honoured as before."""
        if by is not None:
            return by
        orderable = self.m.orderable_levels() & set(anchor)
        if len(orderable) == 1:
            return next(iter(orderable))
        if not orderable:
            raise Refusal("unknown",
                f"scan '{scan_op}' @ {anchor} has no derivable order axis (no CERTIFIED temporal "
                f"level in the anchor); name it with by=<level>. A declared-but-uncertified "
                f"hierarchy confers no order axis — declaration makes structure eligible for "
                f"certification, not executable.",
                measure=measure, target=str(anchor),
                alternatives=("name the axis explicitly with by=<level>",
                              "publish/adjudicate so the temporal hierarchy is certified"))
        raise Refusal("unknown",
            f"scan '{scan_op}' @ {anchor} order axis is ambiguous ({sorted(orderable)}); "
            f"name it with by=<level>", measure=measure, target=str(anchor),
            alternatives=("name the axis explicitly with by=<level>",))

    def plan_routes(self, measure: str, anchor: tuple):
        """PUBLIC: the certified route plan for `measure` @ `anchor`, as (routes, split).

        The planner owns route selection, so a caller that drives `ColumnEngine` directly (a demo, a
        spec harness, an embedder) asks the planner for a plan rather than bypassing it. This is the
        supported way to reach the engine below the ask surface — it cannot manufacture admission,
        because it refuses exactly where a served query would."""
        routes = {}
        for T in anchor:
            self._check_addressable(measure, T, routes)
        return routes, self._split_dependent(anchor)

    def _plan_route(self, routes, measure: str, level: str, base):
        """Record the CERTIFIED route measure->level in `routes`, or return False if none exists.

        This is the single place a transport route is chosen. Everything the engine later executes
        comes from here, so "the route that is certified and planned is the route that executes" is
        true by construction rather than by keeping two searches in sync."""
        path = self.m.find_path(base, level)
        if path is None:
            return False
        if routes is not None:
            routes[(measure, level)] = self._route(path)
        return True

    def _refuse_uncertified_travel(self, what: str, frm: str, to: str):
        """No positively-admitted route from `frm` to `to`. Name the refutation when we hold one
        (contradicted_edge, the stronger factual claim), else uncertified_edge."""
        declared = self.m.find_path_any({frm}, to) if frm in self.m.levels else None
        if declared is not None:
            for e in declared[1]:
                if e.key in self.blocked_edges:
                    raise self._blocked_transport_refusal(e.key)
        if declared is None:
            # no DECLARED route either: the target is simply not addressable from here. That is the
            # out-of-universe claim (undefined, not withheld) — never dress it as a certification gap.
            raise Refusal("out_of_universe",
                f"{what} @ {to}: '{to}' is not reachable from '{frm}' "
                f"(out of domain — undefined, not missing)",
                measure=what, target=to,
                alternatives=(f"address {what} at a level reachable from '{frm}'",))
        raise Refusal("uncertified_edge",
            f"{what} @ {to}: travelling from '{frm}' to '{to}' needs a positively-admitted "
            f"functional route; none is certified, so the reduction is withheld. A declaration makes "
            f"an edge eligible for certification, not executable.",
            measure=what, target=to,
            alternatives=("publish/adjudicate so the edge is certified on the attested data",
                          "address at a grain that does not cross this edge"))

    # ---- typecheck: addressability (fan-out / out-of-universe caught here) --
    def _check_addressable(self, measure: str, T: str, routes=None):
        meas = self.m.measures[measure]
        uni = meas.universe
        base = self.m.universes[uni].base_dimensions
        if self._plan_route(routes, measure, T, base):
            return
        # A DECLARED faced coordinate `<coord>.<face>` IS addressable: the face licenses the crossing,
        # provided the measure reaches the OTHER endpoint (so a value exists to carry over the edge).
        faced = parse_faced(T, self.m.non_functional)
        if faced is not None:
            coord, _fname, rel, _face = faced
            # P0.5a: parse_faced names the DECLARATION; it does not license execution. The crossing serves
            # only if adjudication positively ADMITTED this face (VERIFIED touch / CORROBORATED assign|alloc).
            _fkey = f"{rel.frm}<->{rel.to}.{_fname}"
            if not self.m.probing and (_fkey in getattr(self, "_stale_faces", frozenset())
                                       or _fkey not in self.certified_faces):
                raise Refusal("uncertified_face",
                    f"{measure} @ {T}: the crossing face '{_fname}' on {rel.frm}<->{rel.to} is not "
                    f"certified for governed use — a declaration makes a crossing eligible for "
                    f"certification, not executable. Adjudication must positively admit it before it serves.",
                    measure=measure, target=T, edge=f"{rel.frm}<->{rel.to}",
                    alternatives=("publish/adjudicate so the face is certified on the attested data",
                                  "if the face was refuted on the data, fix the data and re-attest"))
            other = rel.to if coord == rel.frm else rel.frm
            if self._plan_route(routes, measure, other, base):
                # The DRIVER measure (ASSIGN/ALLOC) is served by the engine on its own second path,
                # below the planner. Plan its route here, while we hold the admitted face, so that
                # path also executes a certified route instead of choosing one (P0.5a).
                # NB the SHAPE calls it `driver`; the full Face model calls it `selection`.
                drv = getattr(_face, "driver", None) or getattr(_face, "selection", None)
                if drv and drv in self.m.measures:
                    dbase = self.m.universes[self.m.measures[drv].universe].base_dimensions
                    self._plan_route(routes, drv, coord, dbase)
                return   # the engine executes the crossing
        # fan-out: the BARE coordinate T is reachable only across a non-functional (M:N) edge — clarify.
        for rel in self.m.non_functional:
            nf, nt, detail = rel.frm, rel.to, rel.detail
            reach_nf = (nf in base) or (self.m.find_path(base, nf) is not None)
            reach_t = (nt == T) or (self.m.find_path([nt], T) is not None)
            if reach_nf and reach_t:
                # THE CLARIFY-AS-MENU (Huayin 2026-07-19): a relation with declared faces LISTS them with
                # their folklore — the human re-issues as `T.<face>`. Same shape as the input-anchor
                # clarify. Ship-dark: no faces -> the standing three-remedy prose, unchanged.
                if rel.faces:
                    alternatives = tuple(f"{T}.{f.name} — {f.description}" for f in rel.faces)
                else:
                    alternatives = ("membership filter — accept the overlap deliberately ('revenue "
                                    "touching each "+T+"')",
                                    "primary designation — make the "+nf+"\u2192"+nt+" edge functional",
                                    "WITH allocation — supply a partition-of-unity split [Pro]")
                raise Refusal("non_functional_transport",
                    f"{measure} @ {T}: relating crosses a non-functional (M:N) edge "
                    f"{nf}\u2194{nt} ({detail}); this aggregate-across is underdetermined — the "
                    f"measure would be replicated across matches and the total inflated",
                    measure=f"{measure}@transaction", target=T, edge=f"{nf}\u2194{nt}",
                    alternatives=alternatives)
        # P0.5a: T is reachable via a DECLARED functional edge that is NOT certified (UNTESTABLE /
        # unadjudicated / contradicted) — the transport exists in the declaration but is not governed-usable.
        # Distinguish it from out-of-universe (no declared path at all); name a contradiction specifically
        # when we hold the refuting detail (a stronger factual claim than 'uncertified').
        declared = self.m.find_path_any(base, T)
        if declared is not None and declared[1]:
            for e in declared[1]:
                if e.key in self.blocked_edges:                    # tested + refuted → the stronger claim
                    raise self._blocked_transport_refusal(e.key)
            offending = next((e for e in declared[1] if not self.m._admitted(e)), declared[1][0])
            raise Refusal("uncertified_edge",
                f"{measure} @ {T}: transport crosses the declared functional edge "
                f"{offending.frm}->{offending.to} (lineage '{offending.lineage}'), which is NOT certified for "
                f"governed use — a declaration makes an edge eligible for certification, not executable. "
                f"Adjudication must positively admit it (CORROBORATED on the attested data) before transport "
                f"across it can serve.",
                measure=measure, target=T, edge=f"{offending.frm}->{offending.to}",
                alternatives=("publish/adjudicate so the edge is certified on the attested data",
                              "address at a grain that does not cross this edge"))
        # otherwise: out of universe (the dimension is not part of this population)
        raise Refusal("out_of_universe",
            f"{measure} @ {T}: '{T}' is not addressable in universe '{uni}' "
            f"(out of domain — undefined, not missing)",
            measure=measure, target=T,
            alternatives=(f"address {measure} only within universe '{uni}'",))

    # ---- anchor resolution (manifold-aware; capture §2b) -------------------
    def _families_of(self, level: str) -> set:
        """Edge-derived membership: the dimension families a level belongs to — the lineages of the
        edges it touches (as `frm` or `to`). No separate declaration; membership IS the edge set."""
        return {e.lineage for e in self.m._edges if level in (e.frm, e.to)}

    def resolve_anchor(self, anchor: tuple) -> tuple:
        """Resolve each anchor token to a canonical declared level name, rejecting universe names and
        invalid family qualifications. Called at frame-build (frameql.ManifoldServer.frame), so a
        rejection rides the EXISTING query-error channel as FrameQLSyntaxError — never a wire reason
        code, and the four-mood wire stays byte-identical.

        Resolution order (STANDING law, not transitional): a literal level-name match wins (dotted
        stored names like the demo's `cal.month` are a legitimate authoring style); otherwise the token
        splits at the first dot and resolves as `family.level`, validated against edge-derived
        membership. A bare token that is neither a universe nor a level passes through unchanged, so an
        unknown level still reaches the same `out_of_universe` addressability mood as before.
        """
        from .frameql import FrameQLSyntaxError
        out = []
        for tok in anchor:
            # universes and levels are DISJOINT namespaces — a universe name never anchors (item 4)
            if tok in self.m.universes and tok not in self.m.levels:
                raise FrameQLSyntaxError(
                    f"'{tok}' is a universe, not a level: universe names do not appear in anchors; "
                    f"populations ride ON UNIVERSE")
            # literal level-name match wins
            if tok in self.m.levels:
                out.append(tok)
                continue
            # qualified family.level — split at the FIRST dot, validate edge-derived membership (item 3a)
            if "." in tok:
                fam, lev = tok.split(".", 1)
                if lev in self.m.levels:
                    fams = self._families_of(lev)
                    if fam not in fams:
                        raise FrameQLSyntaxError(
                            f"anchor '{tok}': level '{lev}' is not in dimension family '{fam}' — it belongs "
                            f"to {sorted(fams) if fams else 'no dimension family'}")
                    out.append(lev)
                    continue
                # not family.level — a faced coordinate `<coordinate>.<face>`? (the LEFT side resolves, the
                # right names a declared crossing face). Kept VERBATIM: `category.touch` IS the grain — a
                # distinct, honestly-named coordinate, not bare `category` (naming honesty, and a distinct
                # cache key). The engine decodes it to join-multiply; addressability is checked below.
                if parse_faced(tok, self.m.non_functional) is not None:
                    out.append(tok)
                    continue
                raise FrameQLSyntaxError(
                    f"anchor '{tok}': no level named '{lev}' — qualify an existing level as "
                    f"family.level, name a level directly, or address a declared face as coordinate.face")
            # bare, non-universe, non-level token: unchanged — addressability handles the unknown level
            out.append(tok)
        return tuple(out)

    # ---- run a frame -------------------------------------------------------
    def run(self, anchor: tuple, columns: list, where: Optional[str] = None, population: Optional[str] = None,
            where_unreachable: Optional[dict] = None) -> FrameResult:
        self._refresh_scope_currency()     # P0.5b-0: one data-identity probe per request, not per column
        results = []
        for name, expr in columns:
            trace = []
            # envelope WHERE reachability (filter_unreachable): a series the planner already adjudicated as
            # unable to reach a WHERE dimension clarifies here, BEFORE any engine call — per-series, so
            # reachable siblings still serve (the juxtaposition model).
            if where_unreachable and name in where_unreachable:
                results.append(ColumnResult(name, expr, None, Disclosure.of(population=None),
                                            refusal=where_unreachable[name].classified(), trace=trace))
                continue
            try:
                # COMPILE: static typecheck (vocabulary, signatures, addressability, expression
                # typing) — no engine calls. Operator-not-supported and type errors are caught
                # HERE, before any backend work; they are vocabulary errors, not data errors.
                tree = ast.parse(expr, mode="eval")
                for n in ast.walk(tree):
                    if not isinstance(n, _ALLOWED):
                        raise Refusal("unknown", f"illegal expression construct: {type(n).__name__}")
                # GENERATED-FAMILY LAW, before typing (ruling 2026-08-20). A structurally prohibited
                # operation is refused for what it ASKS, not for how its ingredients are spelled — so
                # `sum(on_hand@day)`, whose family member is ambiguous, refuses the prohibited temporal
                # sum rather than erroring about which member to pick. Whichever member the reader
                # named, the generated SUM is the thing without authority. Malformed expressions reach
                # no ancestry here and fall through to `_infer`'s vocabulary errors unchanged.
                self._check_expression_law(tree.body, anchor)
                self._infer(tree.body, anchor, population)
                col_uni = self._check_single_universe(tree.body, anchor)  # §2c expr law + the column's universe
                blk = self._blocked_transport(tree.body, anchor)          # transport across a refuted-hierarchy edge
                if blk is not None:
                    raise self._blocked_transport_refusal(blk)
                # EXECUTE: resolve through the engine
                frame, disc = self._eval(expr, anchor, where, trace)
                results.append(ColumnResult(name, expr, frame.rename({_V: name}), disc,
                                            trace=trace, universe=col_uni,
                                            fill_rule=self._column_fill_rule(tree.body, anchor)))
            except Refusal as r:
                results.append(ColumnResult(name, expr, None,
                                Disclosure.of(population=None), refusal=r.classified(), trace=trace))
            except Exception as e:
                # EVERYTHING-CLASSIFIES backstop: an unexpected engine/eval failure must never leak a raw
                # exception past the planner (the guarantee). Classify as ERROR rather than throw.
                # DOCTRINE-GAP (doctrine_gaps.md · classify-collapse-with-blocked-transport): today
                # `level.sum @ cal.month` — collapse a base coordinate while transporting another across a
                # BLOCKED lineage — lands here (a ColumnNotFoundError on main); it SHOULD serve with a
                # critical blocked_reduction caveat. The structural fix is engine-side; this backstop
                # guarantees it is at least CLASSIFIED, never raw, past the gate.
                results.append(ColumnResult(name, expr, None, Disclosure.of(population=None),
                    refusal=Refusal("unsupported",
                        f"this frame could not be resolved in the engine ({type(e).__name__}); the ask is "
                        f"not supported in this build.").classified(), trace=trace))

        # assemble non-refused columns — §2c FRAME LAW (juxtaposition): columns may come from DIFFERENT
        # universes; the result is an ALIGNMENT view (full-outer join on the shared anchor; missing where
        # a universe has no atom at a cell), each column keeping its own population semantics.
        data = None
        for c in results:
            if c.frame is None:
                continue
            data = c.frame if data is None else data.join(c.frame, on=list(anchor), how="full", coalesce=True)
        if data is not None:
            data = data.sort(list(anchor))

        # ABSENCE SEMANTICS — driven by the DECLARED member fill rule Φ_v (columna#143 step 3), NOT by
        # universe basis (that default is retired: a 0-fill keyed on basis alone was a silent wrong number
        # for a state-valued measure, D4). Absence is only definable relative to a DOMAIN; the juxtaposition
        # (the full-outer align above) supplies one LOCALLY, so a column's null cells take meaning from THAT
        # column's own member rule. A single-column frame (no nulls) is untouched. The four dispositions:
        #   zero      -> fill 0 (declared: existed and was nil) — a correct value, immaterial note
        #   unknown   -> LEAVE NULL, MATERIAL note (a value existed but was not recorded)
        #   undefined -> LEAVE NULL, immaterial note (outside the member's population — a restriction)
        #   None      -> UNDECLARED: LEAVE NULL, MATERIAL note (the engine discloses, never chooses).
        if data is not None:
            for c in results:
                if c.frame is None or c.universe is None:
                    continue
                n_absent = data[c.name].null_count()
                if not n_absent:
                    continue
                phi = c.fill_rule
                if phi == "zero":
                    data = data.with_columns(pl.col(c.name).fill_null(0))
                    c.disclosure = c.disclosure.with_caveat(Caveat(DECLARED_FILL, severity="info", detail=(
                        f"{n_absent} absent cell(s) filled with 0 per the declared fill rule — the quantity "
                        f"existed and was nil")))
                elif phi == "unknown":
                    c.disclosure = c.disclosure.with_caveat(Caveat(UNKNOWN_ABSENCE, severity="caution", detail=(
                        f"{n_absent} absent cell(s) left unknown per the declared fill rule — a value existed "
                        f"but was not recorded; not filled")))
                elif phi == "undefined":
                    c.disclosure = c.disclosure.with_caveat(Caveat(OUT_OF_POPULATION, severity="info", detail=(
                        f"{n_absent} cell(s) are outside this measure's population per the declared fill rule")))
                else:  # UNDECLARED — disclose and do NOT fill (#147's interim, now permanent)
                    c.disclosure = c.disclosure.with_caveat(Caveat(UNDECLARED_ABSENCE, severity="caution", detail=(
                        f"{n_absent} absent cell(s) with no declared fill rule — the engine discloses the "
                        f"absence rather than choose a value; declare FILL on the measure to resolve it")))

        # No frame-level population caveat: the old multi-universe `coverage` caveat is RETIRED (§2c). Per-
        # column honesty replaces it — a juxtaposed frame never asserts a single shared population, and
        # ON UNIVERSE is dead in the query grammar (cross-universe combination is an authoring act).
        frame_disc = Disclosure.merge(*[c.disclosure for c in results if c.frame is not None])
        return FrameResult(data, frame_disc, results, anchor)

    # ==== ENVELOPE assembly (WP-FrameQL increment 2) ==========================================
    # The PLANNER owns the envelope; the engine stays per-column and envelope-blind. This is where the
    # naming laws (§4) and the clause-reference law (§5) stop being spec text and become behavior.
    # Multi-series rides the existing juxtaposition (self.run); WHERE is per-series pre-reduction
    # (the existing `where` plumbing into the engine); HAVING/ORDER BY/LIMIT PER are POST-assembly on
    # the frame. `@` is the input anchor inside a series (verbatim to the expression parser); AT is the
    # sole output grain. Static well-formedness (naming, clause-reference, PER-not-alias) rides the
    # EXISTING `frameql_syntax` query-error channel (FrameQLSyntaxError) — no new wire reason code.
    _INPUT_ANCHOR_BRACE = re.compile(r"@\s*\{([^}]*)\}")
    _CMP = [(">=", "ge"), ("<=", "le"), ("!=", "ne"), ("==", "eq"), (">", "gt"), ("<", "lt"), ("=", "eq")]

    def _synerr(self, msg: str):
        from .frameql import FrameQLSyntaxError
        raise FrameQLSyntaxError(msg)

    def _apply_subs(self, expr: str, subs: dict) -> str:
        """Substitute WITH bindings (word-boundary), each wrapped in parens to preserve precedence."""
        for name, sub in subs.items():
            expr = re.sub(rf"\b{re.escape(name)}\b", f"({sub})", expr)
        return expr

    def _convert_input_anchor(self, expr: str) -> str:
        """`@ {X}` -> a form the expression parser reads as the input-anchor pin (WP-GRAIN-1):
          • single level `@ {day}` -> `@ day`         (bare Name/Attribute — the legacy shape, unchanged)
          • composite `@ {a*b}` / `@ {a,b}` -> `@ (a, b)`  (a Python tuple literal the AST carries as a
            `Tuple` of Name/Attribute nodes; `_reduction_call` recovers the pin levels from it).
        The composite input anchor denotes a PRODUCT grain (a tuple of levels); `*` and `,` are two
        spellings of the same product, so both normalize here. Order is preserved; exact duplicates
        collapse. This lifts the single-level restriction (formerly refused at this chokepoint)."""
        def repl(m):
            inner = m.group(1).strip()
            if not inner:
                self._synerr("an input anchor `@ { }` is empty — name the grain, e.g. avg(aov @ {day})")
            levels = [t.strip() for t in re.split(r"[*,]", inner)]
            if any(not t for t in levels):
                self._synerr(f"malformed input anchor `@ {{{inner}}}` — name each level, "
                             f"e.g. avg(aov @ {{store*day}})")
            if len(levels) == 1:
                return f"@ {levels[0]}"                       # legacy single-level shape (bare)
            return "@ (" + ", ".join(levels) + ")"           # composite -> tuple literal
        return self._INPUT_ANCHOR_BRACE.sub(repl, expr)

    def _default_name(self, expr: str) -> str:
        """§4 column identity (WP-NAME-1, 0.14.0): an unaliased series is keyed by its CANONICAL
        EXPRESSION, verbatim — never a mechanical default. `expr` arrives ALREADY canonical (from
        `_canon_expr`); for the cases the framework can identify by rule it is returned unchanged:

          • bare measure          `revenue`               -> `revenue`
          • measure.member        `revenue.sum`           -> `revenue.sum`  (NOT `revenue_sum` — the
                                                             dot-to-underscore mangle was itself an
                                                             invention; it retires with the default)
          • single inline reduction `avg(revenue @ {day})` -> `avg(revenue @ {day})`

        No name is INVENTED (the `<R>_<measure>` default is gone) and none is MANGLED. §4's own law —
        *derived by rule or refused, never invented* — completes: the canonical expression IS the
        derivation. A composite/nested/map/bracket expression is still REFUSED for a name (the
        author owns it with AS — an author-owned name never changes under any future rule)."""
        try:
            body = ast.parse(self._convert_input_anchor(expr), mode="eval").body
        except SyntaxError:
            self._synerr(f"cannot name series {expr!r} — give it a name with AS")
        rc = self._reduction_call(body) if isinstance(body, ast.Call) else None
        if rc is not None:
            _reducer, inner, _pin = rc
            # A SINGLE reduction of a single measure atom is identifiable by its canonical expression.
            # A composite/nested reduction (inner is itself a call or a map expression) is refused — no
            # canonical single-atom identity, so the author names it with AS (Chapter 1.6, unchanged).
            if isinstance(inner, ast.Name) or (isinstance(inner, ast.Attribute)
                                               and isinstance(inner.value, ast.Name)):
                return expr                            # the canonical expression IS the identity
            self._synerr(f"composite reduction {expr!r} has no derivable name — give it one with AS "
                         f"(e.g. SELECT {expr} AS my_name)")
        if isinstance(body, ast.Name):
            return body.id                             # bare measure: trivially its own expression
        if isinstance(body, ast.Attribute) and isinstance(body.value, ast.Name):
            return f"{body.value.id}.{body.attr}"      # member access: verbatim dotted, no mangle
        self._synerr(f"series {expr!r} has no derivable name — give it one with AS "
                     f"(e.g. SELECT {expr} AS my_name)")

    def _canon_expr(self, expr: str) -> str:
        """Normalize a series expression's input anchors to the CANONICAL brace form (rider:
        `@ {…}` is canonical, bare `@ level` and `@ (a, b)` are accepted sugar — grammar §2). A
        composite pin canonicalizes with `*` (the product spelling; comma is folded to it, mirroring
        the anchor parser). Idempotent."""
        bare = self._convert_input_anchor(expr)                  # `@ {X}` -> bare / tuple first (idempotent)
        # composite tuple `@ (a, b, c)` -> canonical `@ {a*b*c}`
        bare = re.sub(r"@\s*\(([^)]*)\)",
                      lambda m: "@ {" + "*".join(t.strip() for t in m.group(1).split(",") if t.strip()) + "}",
                      bare)
        return re.sub(r"@\s*([A-Za-z_][\w.]*)", r"@ {\1}", bare) # then bare single -> canonical `@ {X}`

    def desugar(self, stmt):
        """THE desugaring transform (WP-FrameQL sugars increment, rider 1): rewrite the parsed Statement
        to CANONICAL form BEFORE planning — one dialect at the planner, and the exact artifact EXPLAIN
        emits (never a reconstruction). Sugars folded here, each MECHANICAL-or-refused (rider 2), no
        heuristic middle:
          • WITH bindings inlined into the series (the canonical form carries no WITH);
          • input anchors to canonical brace form `@ {level}` (bare `@ level` accepted → braced);
          • series names resolved (§4: AS alias, else the canonical expression itself; unnameable → refused);
          • anchor to canonical declared levels (comma → `*` already normalized by the parser).
        The single-universe and comma-anchor sugars are already canonical out of the parser. The
        omitted-input-anchor sugar is left as-is: the planner's existing path clarifies
        `input_anchor_ambiguous` — the SAME shipped code/channel (rider 3), no re-mint here."""
        from . import envelope as E
        subs = {}
        for b in stmt.bindings:
            subs[b.name] = self._canon_expr(self._apply_subs(b.expr, subs))
        series = []
        for s in stmt.series:
            expr = self._canon_expr(self._apply_subs(s.expr, subs))
            name = s.alias or self._default_name(expr)   # canonical expression IS the identity (WP-NAME-1)
            series.append(E.Series(expr=expr, alias=name))
        anchor = self.resolve_anchor(stmt.anchor)
        return E.Statement(series=series, anchor=anchor, explain=stmt.explain,
                           from_manifold=stmt.from_manifold, bindings=[], where=list(stmt.where),
                           having=list(stmt.having), order_by=list(stmt.order_by), limit=stmt.limit)

    def _check_name_collisions(self, columns: list, anchor: tuple):
        """§4: collisions are REFUSED, never suffixed — incl. a column name vs an anchor-dimension name."""
        names = [n for n, _ in columns]
        seen = set()
        for n in names:
            if n in seen:
                self._synerr(f"two columns resolve to the name {n!r} — names must be distinct, never "
                             f"suffixed; give one an AS alias")
            seen.add(n)
        for n in names:
            if n in anchor:
                self._synerr(f"column {n!r} collides with the anchor dimension {n!r} — the frame's columns "
                             f"and its anchor coordinates share one namespace; rename the column with AS")

    def _validate_clause_refs(self, stmt, frame_cols: set, anchor: tuple):
        """§5 clause-reference law: ORDER BY / HAVING / PER reference the output frame's OWN columns only
        (named series + anchor coordinates) — no hidden pulls. The remedy names itself."""
        for pred in stmt.having:
            col = self._predicate_column(pred)
            if col not in frame_cols:
                self._synerr(f"HAVING references {col!r}, which is not a column of the frame — select it "
                             f"as a column, or add it to the anchor")
        for k in stmt.order_by:
            if k.column not in frame_cols:
                self._synerr(f"ORDER BY references {k.column!r}, which is not a column of the frame — "
                             f"select it as a column, or add it to the anchor")
        if stmt.limit is not None:
            series_names = frame_cols - set(anchor)              # frame columns that are NOT anchor coordinates
            order_cols = {k.column for k in stmt.order_by}
            for d in stmt.limit.per:
                if d in series_names:                            # an alias/series name ⇒ §4 refusal
                    self._synerr(f"PER {{{d}}} names {d!r}, an output column — PER takes ANCHOR "
                                 f"coordinates only; put {d!r} in the anchor to partition by it")
                if d not in anchor:
                    self._synerr(f"PER {{{d}}} names {d!r}, which is not an anchor coordinate — PER "
                                 f"partitions along the frame's grain; add {d!r} to the anchor")
                # PER ⊆ ORDER BY (the manual's determinism-and-contiguity law, ruled 2026-07-17): PER keys
                # GROUP, the remaining ORDER BY keys RANK within, and the output presents groups contiguously
                # — so every PER key must be an ORDER BY key.
                if d not in order_cols:
                    self._synerr(f"PER {{{d}}} is not in ORDER BY — PER groups and ORDER BY ranks within "
                                 f"each group, so the partition key must also sort; add {d!r} to ORDER BY "
                                 f"(e.g. ORDER BY {d}, …)")

    def _predicate_column(self, pred: str) -> str:
        for op, _m in self._CMP:
            if op in pred:
                return pred.split(op, 1)[0].strip()
        self._synerr(f"cannot read predicate {pred!r} — expected `column <op> value` (op: > < >= <= == !=)")

    def _apply_predicate(self, data, pred: str):
        for op, method in self._CMP:
            if op in pred:
                col, rhs = pred.split(op, 1)
                col, rhs = col.strip(), rhs.strip()
                val = self._literal(rhs)
                return data.filter(getattr(pl.col(col), method)(val))
        self._synerr(f"cannot read predicate {pred!r} — expected `column <op> value`")

    @staticmethod
    def _literal(s: str):
        if (len(s) >= 2 and s[0] in "'\"" and s[-1] == s[0]):
            return s[1:-1]
        if re.fullmatch(r"-?\d+", s):
            return int(s)
        if re.fullmatch(r"-?\d+\.\d+", s):
            return float(s)
        return s

    # Directive 7 (Huayin, 2026-07-17): Polars is the execution substrate. The envelope's frame-level
    # clauses map onto the assembled Polars DataFrame NATIVELY — HAVING a filter, ORDER BY a sort, LIMIT
    # n a head, LIMIT n PER {dims} a grouped top-n — never a Python row loop. The boundary (extending the
    # B3 precedent): Polars EXECUTES what the planner has already adjudicated; a Polars default is never
    # an accidental law. Every four-mood decision, reachability, refusal, and absence rule is decided
    # UPSTREAM (in `run`, before this frame exists). Where a Polars behavior matches ruled law, the ruling
    # is cited below — not the coincidence.
    def _sort_frame(self, data, order_by):
        # ORDER BY is Columna's ruled output order. `nulls_last` is set EXPLICITLY, not left to Polars'
        # sort convention: a gap (null — B3-adjudicated upstream as incomplete_data) has no value to
        # rank, so it sorts to the bottom. A deliberate default, FLAGGED for Huayin — not a leaked rule.
        return data.sort(by=[k.column for k in order_by],
                         descending=[k.descending for k in order_by], nulls_last=True)

    def _apply_output_clauses(self, fr: FrameResult, stmt, anchor: tuple, columns: list) -> FrameResult:
        frame_cols = {n for n, _ in columns} | set(anchor)
        self._validate_clause_refs(stmt, frame_cols, anchor)     # §5 — static, even when the frame refused
        data = fr.data
        if data is None:
            return fr
        # HAVING — one native Polars filter per predicate. A gap (null) cannot satisfy a value predicate,
        # so it is excluded: Polars' null-drop here MATCHES the ruled "a gap is not a value" (B3, cited
        # deliberately) — flagged for confirmation, not relied on as a Polars accident.
        for pred in stmt.having:
            if self._predicate_column(pred) in data.columns:
                data = self._apply_predicate(data, pred)
        # ORDER BY — native Polars sort (the ruled output order).
        if stmt.order_by:
            data = self._sort_frame(data, stmt.order_by)
        # LIMIT — native head; LIMIT n PER {dims} is a native grouped top-n (group_by().head()), the rows
        # picked in the ruled ORDER BY order (maintain_order preserves THAT order — not a Polars default),
        # then re-sorted for a stable frame. No Python row loop.
        if stmt.limit is not None:
            if stmt.limit.per:
                data = data.group_by(list(stmt.limit.per), maintain_order=True).head(stmt.limit.n)
                if stmt.order_by:                                # re-apply the ruled order after per-group truncation
                    data = self._sort_frame(data, stmt.order_by)
            else:
                data = data.head(stmt.limit.n)
        return FrameResult(data, fr.disclosure, fr.columns, fr.anchor)

    def _where_reachability(self, columns: list, where_predicates: list) -> dict:
        """§WHERE reachability (filter_unreachable, minted 2026-07-17): a WHERE dimension must be
        addressable in each series' OWN universe (the filter binds pre-reduction, at the series' input).
        Returns {series_name: Outcome} for series that cannot reach some WHERE dimension — a per-series
        CLARIFY so reachable siblings still serve. Adjudicated HERE, before Polars/engine (directive 7)."""
        levels = [self._predicate_column(p) for p in where_predicates]
        out = {}
        for name, expr in columns:
            try:
                uni = self._check_single_universe(ast.parse(expr, mode="eval").body, ())
            except Exception:
                continue                                         # a malformed series — let the normal run classify it
            if uni is None:
                continue
            base = self.m.universes[uni].base_dimensions
            reachable = sorted({lv for lv in ({e.frm for e in self.m._edges} | {e.to for e in self.m._edges} | set(base))
                                if lv in base or self.m.find_path(base, lv) is not None})
            for lvl in levels:
                if lvl not in base and self.m.find_path(base, lvl) is None:
                    out[name] = Refusal("filter_unreachable",
                        f"WHERE dimension '{lvl}' cannot lawfully reach series '{name}' — '{lvl}' is not "
                        f"addressable in that series' universe '{uni}', so the pre-reduction filter has no "
                        f"grain to bind to; the answer would be silently partial.",
                        target=lvl, measure=name, discriminator=AMBIGUOUS,
                        alternatives=(f"restrict the predicate to a reachable dimension ({', '.join(reachable)})",
                                      f"change series '{name}' to an input anchor that reaches '{lvl}'"))
                    break
        return out

    def _engine_columns(self, desugared) -> list:
        """The canonical desugared series -> [(name, expr)] the engine consumes. The ONLY transform is
        the AST-substrate adapter (canonical `@ {level}` -> `@ level`, since Python's ast can't hold a
        `{…}` set literal as an anchor) — not a re-sugaring; the desugared Statement remains the artifact."""
        return [(s.alias, self._convert_input_anchor(s.expr)) for s in desugared.series]

    def run_statement(self, stmt, execute: bool = True) -> FrameResult:
        """Assemble and dispose an envelope Statement (the whole clause set). Desugars to canonical AST
        FIRST (one dialect), then plans it. ON is dead (§2c); universe is resolved structurally per
        column. Returns a FrameResult exactly like `run`, so every surface reads it uniformly."""
        d = self.desugar(stmt)                                   # canonical AST (EXPLAIN's artifact) — rider 1
        columns = self._engine_columns(d)
        self._check_name_collisions(columns, d.anchor)           # §4 collisions REFUSED
        where = " AND ".join(d.where) if d.where else None       # per-series pre-reduction (existing plumbing)
        unreachable = self._where_reachability(columns, d.where) if d.where else None
        fr = (self.run if execute else self.plan)(d.anchor, columns, where, where_unreachable=unreachable)
        return self._apply_output_clauses(fr, d, d.anchor, columns)

    def plan_statement(self, stmt) -> FrameResult:
        """The would-be assembly without executing (zero backend fetches) — EXPLAIN's engine."""
        return self.run_statement(stmt, execute=False)

    def cone_atoms_and_edges(self, expr: str, anchor: tuple) -> tuple:
        """SHAPE for EXPLAIN's dependency cone (provenance-free — the planner's remit): the atomic
        (measure, member, universe) atoms, the derived names referenced, and the edges the transport
        traverses (with blocked status). The SERVER enriches with verdicts (licenses live on the
        Manifold, not the projection). Zero data touched. (A fourth element — the cut declaration hit —
        left with the ASSERT retirement in 0.13.0; ruling 2026-07-26.)"""
        engine_expr = self._convert_input_anchor(expr)
        tree = ast.parse(engine_expr, mode="eval").body
        atoms = [{"measure": meas, "member": member,
                  "universe": self.m.measures[meas].universe if meas in self.m.measures else None}
                 for (meas, member) in self._atoms(tree, anchor)]
        derived = sorted({n for n in re.findall(r"[A-Za-z_]\w*", engine_expr) if n in self.m.derived})
        edges, seen = [], set()
        for (meas, _member) in self._atoms(tree, anchor):
            mc = self.m.measures.get(meas)
            if mc is None:
                continue
            base = self.m.universes[mc.universe].base_dimensions
            for T in anchor:
                path = self.m.find_path(base, T)
                if path is None:
                    continue
                for e in path[1]:
                    key = (e.frm, e.to, e.lineage)
                    if key not in seen:
                        seen.add(key)
                        edges.append({"frm": e.frm, "to": e.to, "lineage": e.lineage,
                                      "blocked": (e.frm, e.to) in self.blocked_edges})
        return atoms, derived, edges

    # ---- expression evaluation (post-agg over measure columns) -------------
    def _eval(self, expr: str, anchor, where, trace):
        tree = ast.parse(expr, mode="eval")
        for n in ast.walk(tree):
            if not isinstance(n, _ALLOWED):
                raise Refusal("unknown", f"illegal expression construct: {type(n).__name__}")
        kind, payload, disc, _dtype = self._node(tree.body, anchor, where, trace)
        return payload, disc

    def _measure_ref(self, node):
        """Name('revenue') -> (revenue, default-member). Attribute(level, 'sum') -> (level, sum)."""
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            return node.value.id, node.attr
        if isinstance(node, ast.Name):
            return node.id, None
        return None, None

    # inline reduction OF a derivation (capture v0.8; WP-B.1). `avg`/`mean`/`sum`/`min`/`max`/`count`
    # collapse a finer-resolved series to the frame anchor. Distinct from a SCAN (order-preserving) —
    # and from the DECLARED AT-metric (this is the same reading expressed inline, no declaration).
    _INLINE_REDUCERS = {"avg": "mean", "mean": "mean", "sum": "sum",
                        "min": "min", "max": "max", "count": "count"}

    @staticmethod
    def _level_name(node):
        """A level name from an AST leaf: `day` (Name) or `cal.month` (Attribute). None if neither —
        so the pin's level names round-trip verbatim, dotted or not (WP-GRAIN-1)."""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        return None

    def _reduction_call(self, node):
        """Recognize an inline reduction: `R(inner)` or `R(inner @ pin)`, R a reducing operator.
        Returns (reducer, inner_node, pinned | None), or None if `node` is not such a call. The `@`
        (MatMult) PINS the input anchor; `pinned` is a TUPLE of level names — a single-level pin is a
        1-tuple, a composite (product) pin `@ {a*b}` is an n-tuple (WP-GRAIN-1; the pin is a product
        grain). Unpinned ⇒ None ⇒ the input anchor is structurally underdetermined (an engine
        clarify — capture v0.8)."""
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            return None
        r = self._INLINE_REDUCERS.get(node.func.id)
        if r is None:
            return None
        if len(node.args) != 1 or node.keywords:
            raise Refusal("unknown",
                f"inline reduction '{node.func.id}' takes exactly one column argument "
                f"(e.g. {node.func.id}(aov@day) to pin the input anchor)")
        arg = node.args[0]
        if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.MatMult):
            right = arg.right
            elts = right.elts if isinstance(right, ast.Tuple) else [right]
            levels = [self._level_name(e) for e in elts]
            if any(lv is None for lv in levels):
                raise Refusal("unknown",
                    f"inline reduction input anchor must be level name(s), "
                    f"e.g. {node.func.id}(aov@{{day}}) or {node.func.id}(aov@{{store*day}})")
            return r, arg.left, tuple(dict.fromkeys(levels))     # order-preserving; exact dups collapse
        return r, arg, None

    @staticmethod
    def _fmt_pin(pinned: tuple) -> str:
        """A composite pin's surface form: a single level bare (`day`), a product braced (`{a*b}`) —
        so single-level rendering is byte-identical to the pre-WP-GRAIN-1 form (regression), and a
        composite reads as one product grain."""
        return pinned[0] if len(pinned) == 1 else "{" + "*".join(pinned) + "}"

    def _pin_input_grain(self, pinned: tuple, anchor: tuple) -> tuple:
        """The composite input grain a pinned reduction resolves its inner at (WP-GRAIN-1): the pinned
        levels, plus the output's ORTHOGONAL reduction targets (those no pin level reaches) joined in
        so the series carries them. Generalizes `(pinned,) + orthogonal` from the single-level era; the
        engine's `reduce_series_to_anchor` is already composite-grain-native over this tuple."""
        reduction, _dependent = self._split_dependent(anchor)
        orthogonal = tuple(t for t in reduction
                           if t not in pinned
                           and not any(self.m.find_path({p}, t) is not None for p in pinned))
        return tuple(dict.fromkeys(tuple(pinned) + orthogonal))

    def _check_pin_laws(self, pinned: tuple, anchor: tuple):
        """WP-GRAIN-1 Laws 1 & 2, as STATIC planner checks over the pin × output-anchor lattice
        (ratified 2026-07-29). Both name exactly one contested dimension (OF-1):

          Law 1 (REFUSE `pin_coarser_than_output`): an output level `a` functionally reaches a pin
            level `p` (a -> p) — the pin fixes a grain COARSER than the output, which cannot resolve at
            the output's grain without inventing rows the pin does not distinguish.
          Law 2 (CLARIFY `redundant_pin`): a pin level `p_i` functionally determines another pin level
            `p_j` (p_i -> p_j) — the pair fixes ONE axis, not two; the reader picks which pin they mean.
        """
        # Law 1 — no coarser-than-output level in the pin.
        for p in pinned:
            for a in anchor:
                if a != p and self.m.find_path({a}, p) is not None:
                    keep = "*".join(x for x in pinned if x != p)
                    raise Refusal("pin_coarser_than_output",
                        f"pin '{p}' is COARSER than output level '{a}' — the pin fixes a grain that "
                        f"cannot resolve at the output's grain (a coarser pin cannot serve a finer "
                        f"output, so the reduced value at '{a}' would be inventing rows the pin does "
                        f"not distinguish); either replace '{p}' with a level finer than or equal to "
                        f"'{a}', or drop it if another pin already reaches '{a}'",
                        target=_fmt_anchor(anchor),
                        alternatives=(f"replace @ {{{self._fmt_pin(pinned)}}} — use a level finer than '{a}' in place of '{p}'"
                                      if len(pinned) == 1 else
                                      f"replace '{p}' with a level finer than or equal to '{a}'",
                                      f"drop '{p}' from the pin"
                                      + (f" (pin @ {{{keep}}} — another pin reaches '{a}')" if keep else "")))
        # Law 2 — no two pin levels cross-comparable.
        for pj in pinned:
            for pi in pinned:
                if pi != pj and self.m.find_path({pi}, pj) is not None:
                    fine_only = "*".join(x for x in pinned if x != pj)   # keeps the finer determiner p_i
                    coarse_only = "*".join(x for x in pinned if x != pi) # keeps the coarser determined p_j
                    raise Refusal("redundant_pin",
                        f"pin includes both '{pj}' and '{pi}', but '{pi}' functionally determines "
                        f"'{pj}' (a finer level fixes a coarser one) — the pair fixes one axis, not "
                        f"two; write @ {{{fine_only}}} alone",
                        discriminator=AMBIGUOUS,
                        alternatives=(f"pin @ {{{fine_only}}} (the finer level)",
                                      f"pin @ {{{coarse_only}}} (the coarser level — a different denotation)"))

    def _reducer_out_dtype(self, reducer: str, in_dt: str) -> str:
        """Output dtype of an inline reducer over `in_dt`, read from the operator REGISTRY.

        This used to be a hand-written table because `mean` was in no registry at all — the same
        drift that left the inline average with no governable law address (see operators.ALIASES /
        SERIES_REDUCERS). It now agrees with the registry by construction: mean -> Float64,
        count -> Int64, sum/min/max -> `same`. Deliberately NOT extended into a signature check:
        registering `mean` gives the operator a law address, not new arithmetic or new typing."""
        return self.m.output_dtype(reducer, in_dt)

    def _split_dependent(self, target: tuple) -> tuple:
        """Partition a target anchor into independent REDUCTION targets and functionally-DETERMINED
        attribute targets (a level fixed by another target level, S->..->T). Shape-only, from the
        projection's edges — the planner's remit; the engine mirrors this for the actual transport."""
        dependent = [T for T in target
                     if any(S != T and self.m.find_path({S}, T) is not None for S in target)]
        return tuple(T for T in target if T not in dependent), tuple(dependent)

    def _candidate_input_anchors(self, target: str):
        """C — the GOVERNED candidate interpretations of an unpinned reduction's input anchor: every
        level with a functional path to the frame anchor. Structure only; lawfulness is applied on top
        of this set by `_lawful_pins`, never folded into it (the two are different questions and the
        refusal messages need to tell them apart)."""
        levels = {e.frm for e in self.m._edges} | {e.to for e in self.m._edges}
        return sorted(L for L in levels
                      if L != target and self.m.find_path({L}, target) is not None)

    def _unpinned_disposition(self, reducer, inner, anchor):
        """The verdict for an unpinned generated reduction (ruling 2026-08-20 §9):

            |L| = 0  ->  Refuse   — no lawful candidate survives; there is nothing to choose between
            |L| = 1  ->  proceed  — one lawful reading, so nothing is contested; the DEFAULTED input
                                    anchor is returned and the caller owes the MATERIAL input_anchor
                                    caveat (OF-2: a defaulted anchor is a condition the reader weighs)
            |L| > 1  ->  Clarify  — over the LAWFUL candidates only

        Never offer a candidate that is already structurally illegal. A clarify is a menu of readings
        the asker may choose between; an unlawful reading is not a choice, and offering it makes
        Clarify reachable before lawfulness — which is how a reader gets talked into a laundered
        answer one keystroke later."""
        lawful = self._lawful_pins(reducer, inner, tuple(anchor))
        if len(lawful) == 1:
            return (lawful[0],)
        if lawful:
            raise self._unpinned_reduction_refusal(reducer, inner, anchor, lawful)
        raise self._no_lawful_pin_refusal(reducer, inner, anchor)

    def _no_lawful_pin_refusal(self, reducer, inner, anchor):
        """|L| = 0. Either the structure offers no finer input anchor at all, or every one it offers
        would make this reduction cross a lineage the governed law bars. Both are REFUSE: an operation
        with no lawful reading is not a choice the reader can be asked to make.

        Enumerated over the WHOLE anchor, not just a single-level one: a refusal owes the reader the
        lawful neighbours (DG-2 invariant 5), and `sum(on_hand) AT {store, month}` — the Afternoon's
        third beat — is exactly the multi-level case, so leaving it terse would strip the remedy from
        the very ask the correction exists for."""
        expr = ast.unparse(inner)
        blocked_out = [L for T in anchor for L in self._candidate_input_anchors(T)]
        blocked_out = sorted(dict.fromkeys(blocked_out))
        if blocked_out:
            return Refusal("blocked_reduction",
                f"inline reduction '{reducer}({expr})' has no lawful input anchor at "
                f"{_fmt_anchor(anchor)}: every candidate grain ({', '.join(blocked_out)}) would reduce "
                f"by '{reducer}' across a lineage the governed law blocks for it. Generating the "
                f"family does not create the permission, so there is no pin that rescues this ask.",
                target=_fmt_anchor(anchor),
                alternatives=("use a reducer that IS applicable along the blocked lineage "
                              "(e.g. '.last' for a stock collapsed over time)",
                              "address at an anchor the reduction does not have to cross"))
        return Refusal("blocked_reduction",
            f"inline reduction '{reducer}({expr})' has no lawful input anchor at "
            f"{_fmt_anchor(anchor)} — no declared level both reaches this anchor and admits the "
            f"reduction, so the ask has no reading to serve.",
            target=_fmt_anchor(anchor))

    def _unpinned_reduction_refusal(self, reducer, inner, anchor, lawful=None):
        """The engine clarify for an inline reduction with no pinned input anchor (capture v0.8): the
        input anchor is structurally underdetermined, so enumerate the candidate anchors and choose
        none. Reason `input_anchor_ambiguous` (CLARIFY/AMBIGUOUS), sibling to `co_anchor_ambiguous`
        (OF-1, ruled 2026-07-14: one reason per contested dimension). It names the same dimension the
        pinned case's immaterial input-anchor note (OF-2) records."""
        expr = ast.unparse(inner)
        target = anchor[0] if len(anchor) == 1 else None
        # LAWFUL candidates only (ruling 2026-08-20 §9). `lawful` is supplied by `_unpinned_disposition`;
        # the structural fallback exists for the direct-`_node` path and is filtered here too.
        cands = list(lawful) if lawful is not None else self._lawful_pins(reducer, inner, tuple(anchor))
        alts = tuple(f"pin the input anchor to '{L}' (e.g. {reducer}({expr}@{L}))" for L in cands)
        hint = cands[0] if cands else "<level>"
        return Refusal("input_anchor_ambiguous",
            f"inline reduction '{reducer}({expr})' does not pin its input anchor — the grain to "
            f"resolve '{expr}' at before reducing to {_fmt_anchor(target or anchor)} is underdetermined; pin it, "
            f"e.g. '{reducer}({expr}@{hint})'",
            discriminator=AMBIGUOUS, alternatives=alts)

    def _scan_call(self, node):
        """A SCAN call: scan_op( <measure.member>, n=<int>, by=<level> ). Returns
        (scan_op, arg_node, n, by) when node is a registered scan-kind call, else None.
        The planner recognizes the scan from the registry (kind=scan) — it does not know how
        to execute it; that is the engine's job (manual ch.2.8)."""
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            return None
        name = node.func.id
        sig = self.m.operators.get(name)
        if sig is None or sig.kind != "scan":
            # an unknown call, or a non-scan used in call position — a vocabulary refusal
            raise Refusal("unknown",
                f"'{name}' is not a scan operator (registry scans: "
                f"{sorted(n for n,s in self.m.operators.items() if s.kind=='scan')})")
        if len(node.args) != 1:
            raise Refusal("unknown", f"scan '{name}' takes one input expression and keyword params (n=, by=)")
        n, by = 1, None
        for kw in node.keywords:
            if kw.arg == "n" and isinstance(kw.value, ast.Constant):
                n = int(kw.value.value)
            elif kw.arg == "by" and isinstance(kw.value, ast.Constant):
                by = str(kw.value.value)
            else:
                raise Refusal("unknown", f"scan '{name}': unknown parameter '{kw.arg}' (accepts n=, by=)")
        return name, node.args[0], n, by

    # ---- B-anchor crossing detection (STRUCTURAL — shape-only, hoisted from the engine) ----
    def _atoms(self, node, anchor):
        """Yield (measure, member) for every measure atom in an expression — derived columns
        expanded, scans reduced to their underlying member. Shape-only; assumes _infer already
        validated (so _scan_call/_measure_ref will not raise here)."""
        if isinstance(node, ast.Constant):
            return []
        rc = self._reduction_call(node)
        if rc is not None:
            _r, inner, _pinned = rc                 # inline reduction: its atoms are the inner's
            return self._atoms(inner, anchor)
        sc = self._scan_call(node)
        if sc is not None:
            _op, arg, _n, _by = sc
            return self._atoms(arg, anchor)
        m, mem = self._measure_ref(node)
        if m is not None:
            if m in self.m.derived:
                return self._atoms(ast.parse(self.m.derived[m].formula, mode="eval").body, anchor)
            if m not in self.m.measures:
                return []
            mem = mem or next(iter(self.m.measures[m].family))
            return [(m, mem)]
        if isinstance(node, ast.UnaryOp):
            return self._atoms(node.operand, anchor)
        if isinstance(node, ast.BinOp):
            return self._atoms(node.left, anchor) + self._atoms(node.right, anchor)
        return []

    # ══ GENERATED-FAMILY LAW ═══════════════════════════════════════════════════════════════════
    # RULING 2026-08-20 (Huayin). This supersedes ADR-020's inform-and-serve rule for structurally
    # prohibited reductions. The governing sentence:
    #
    #   Family generation creates a new analytical family. It does NOT create a new operator
    #   permission. A successor family preserves the applicability law of its governed ancestry
    #   unless the family-changing operation POSITIVELY establishes a different successor law.
    #
    # WHAT WAS WRONG. The pre-2026-08-20 walk (`_atoms` -> `_crossings`) modelled an expression's law
    # as the law of its LEAF members, so every reducer GENERATED above a leaf was invisible to it.
    # `on_hand.sum AT {store, month}` was caught; `sum(on_hand.last@day) AT {store, month}` — the same
    # prohibited temporal-stock-sum, one syntax away — served CLEAN with the identical meaningless
    # number (960 on the Afternoon fixture, 179656 on Cascadia). Unary, binary, scalar, scan, DERIVED
    # and default-member spellings were all carriers for the same bypass, because in every one of them
    # the leaf stayed lawful and the *generated* reducer did the prohibited travel. So this walk
    # adjudicates the OPERATION, not the leaf: every point in an expression where a reduction actually
    # travels, whether the reader wrote the reducer or generated it.
    #
    # TWO POLARITIES, NEVER FLATTENED (ruling §2). A `_Travel` records which one governs it and the
    # adjudicator never merges them, because ABSENCE means opposite things on the two sides:
    #   · MEASURE B-anchor  — NEGATIVE. Open by default; `BLOCKED { lineage }` closes an operator.
    #                         No declaration => no prohibition from this mechanism.
    #   · DERIVED FERTILE   — POSITIVE. Closed by default; `FERTILE { lineage }` establishes travel.
    #                         No declaration => no permission.
    #
    # DETERMINISM (ruling §4). Every input here is the expression plus the governed declarations:
    # `_atoms`/`_law_travels` are pure AST walks, `find_path`/`out_edges` read declared structure, and
    # nothing consults a value, a row count, a cache or an execution path. Two equivalent resolved
    # expressions therefore cannot acquire different laws. No public or cache identity depends on it.

    def _ancestry(self, node) -> tuple:
        """The governed MEASURE names an expression's value descends from (derived expanded, scans and
        inline reductions reduced to their inner). This is the `governed ancestry` the ruling names:
        the law subject a generated operation is being attempted FROM. It is deliberately NOT the leaf
        member — `on_hand.last` stays its own resolved family; what we ask is whether the operation
        now being generated is permitted over `on_hand`."""
        return tuple(dict.fromkeys(m for (m, _mem) in self._atoms(node, ())))

    def _traversed_lineages(self, frm, to) -> set:
        """The declared lineages a reduction from grain `frm` onto anchor `to` actually travels.

        Two ways a lineage is crossed — the same two the pre-2026-08-20 crossing detector used, kept
        deliberately identical so the DIRECT case's verdict is unchanged in extension (only its mood
        moves from disclose to refuse):
          (1) TRANSPORT — a source level reaches a target level along a path; the path's edge lineages
              are traversed. Read over CERTIFIED structure (`find_path`), because an uncertified edge
              establishes no transport.
          (2) COLLAPSE  — a source level reaches NO target and is marginalized away; it exits along
              every lineage leaving it. Read over DECLARED structure (`out_edges`), certification-
              independent, because the axis is being summed over whether or not anyone may travel it.
        """
        lineages, covered = set(), set()
        for d in frm:
            for T in to:
                path = self.m.find_path({d}, T)
                if path is None:
                    continue
                covered.add(d)
                for e in path[1]:
                    lineages.add(e.lineage)
        for d in (set(frm) - covered):
            for e in self.m.out_edges(d):
                lineages.add(e.lineage)
        return lineages

    def _law_travels(self, node, anchor, out=None) -> list:
        """Every adjudicable reduction in `node` when it is resolved AT `anchor`, outermost first.

        The recursion carries the grain each sub-expression is resolved at, which is what makes the
        walk correct under nesting: the inner of `sum(x@day)` is resolved at the PIN's input grain, so
        its own travel is adjudicated against that grain, not against the frame anchor.

        LAW-PRESERVING classes (ruling §3-A) recurse WITHOUT adding a travel of their own, because
        they establish nothing: unary minus, binary maps, scalar arithmetic, scans and plain DERIVED
        are all anchor-preserving — they reduce nothing, so they can neither acquire nor shed a
        permission. Their operands' law reaches the result unchanged (for a binary, the union of both
        operands' — see ruling §5: the MAP itself establishes no new reduction permission)."""
        out = [] if out is None else out
        if isinstance(node, ast.Constant):
            return out

        rc = self._reduction_call(node)
        if rc is not None:
            reducer, inner, pinned = rc
            if pinned is None:                      # unpinned: adjudicated by `_lawful_pins` instead,
                return out                          # which needs the candidate set, not a fixed travel
            grain = self._pin_input_grain(pinned, anchor)
            out.append(self._generated_travel(reducer, inner, grain, anchor, pinned))
            return self._law_travels(inner, grain, out)

        sc = self._scan_call(node)
        if sc is not None:                          # SCAN: order-preserving, anchor-preserving
            return self._law_travels(sc[1], anchor, out)

        meas_name, member = self._measure_ref(node)
        if meas_name is not None:
            if meas_name in self.m.derived:
                dshape = self.m.derived[meas_name]
                inner = ast.parse(dshape.formula, mode="eval").body
                if dshape.resolution_anchor is None:
                    return self._law_travels(inner, anchor, out)     # denotation-only: no travel
                res = (dshape.resolution_anchor,)
                # HELD (2026-08-20) — the declared derived successor family is NOT adjudicated here.
                # Ruling §3 asked us to consume `FERTILE { .. }` as the successor family's travel
                # permission. Implementing that and running it proved FERTILE cannot carry that meaning:
                # `FERTILE` is an EQUALITY THEOREM about the reduce-path ("reducing from cached finer
                # values equals recomputing from base"), adjudicated against attested data by
                # `adjudication._prove_data`. An AT-metric's travel is the opposite of that by
                # construction — `daily_aov AT day` reduced to month is the MEAN OF DAILY RATES, which
                # is deliberately NOT the recompute-path value (that is the whole point of the reading,
                # pinned by `test_at_metric_at_coarse_is_mean_of_finer_not_pooled`). So declaring
                # `mean FERTILE { calendar }` on it is a FALSE claim and publish fails closed with a
                # Contradiction — while `FERTILE { }` would forbid the metric's own declared meaning.
                # There is therefore NO declaration an author could write to permit this travel, and
                # enforcing the positive polarity through this field would make AT-metrics unusable.
                # Two different concepts wear one name; separating them needs a ruling, not a patch.
                # Recorded as DG-3, and deferred WHOLE: no widened `DerivedShape` is left behind
                # either (ruling §1 — do not leave inert half-semantics as future scaffolding).
                return self._law_travels(inner, res, out)
            if meas_name not in self.m.measures:
                return out
            meas = self.m.measures[meas_name]
            if member is None:
                if len(meas.family) != 1:
                    return out                      # ambiguous family: `_infer` raises the vocabulary error
                member = next(iter(meas.family))
            sig = self.m.operators.get(member)
            # The DIRECT case keeps its pre-existing monoid gate: a HOLISTIC reducer recomputes from
            # base at the target grain and never combines partial results across the axis, so the
            # B-anchor is moot for it. (A GENERATED reducer is not gated this way — see below.)
            if sig is not None and sig.kind == "reducer" and sig.is_monoid:
                base = tuple(self.m.universes[meas.universe].base_dimensions)
                out.append(_Travel(member, base, tuple(anchor),
                                   f"{meas_name}.{member}",
                                   frozenset(meas.blocked.get(member, frozenset())), True))
            return out

        if isinstance(node, ast.UnaryOp):
            return self._law_travels(node.operand, anchor, out)
        if isinstance(node, ast.BinOp):
            self._law_travels(node.left, anchor, out)
            return self._law_travels(node.right, anchor, out)
        return out

    def _generated_travel(self, reducer, inner, grain, anchor, pinned) -> "_Travel":
        """The `_Travel` for one inline generating reduction `R(inner @ pin)` served at `anchor`.

        The law subject is the GOVERNED ANCESTRY of `inner` and the operator is `R` — NOT the leaf
        member `inner` happens to name (ruling §1: "Do not require `R` to be the leaf member the
        expression names. Do not collapse `on_hand.last` back into the identity of bare `on_hand`.").
        `on_hand.last` remains its own resolved family; the question asked here is whether a SUM over
        `on_hand` is permitted along the lineages this reduction will cross. It never is, because
        `on_hand` declares `sum BLOCKED { calendar }` — and it never was, in any spelling.

        NO MONOID GATE, deliberately, unlike the direct case: a generated reducer genuinely collapses
        the resolved series across the axis (that IS the operation), so the reason the direct case
        exempts holistic reducers — they recompute from base rather than combining across the axis —
        does not apply. This is what gives `mean` a real law address rather than a decorative one."""
        law = set()
        for m in self._ancestry(inner):
            law |= set(self.m.measures[m].blocked.get(reducer, frozenset()))
        return _Travel(reducer, tuple(grain), tuple(anchor),
                       f"{reducer}({ast.unparse(inner)}@{self._fmt_pin(pinned)})",
                       frozenset(law), False)

    def _travel_violation(self, t: "_Travel") -> Optional["Refusal"]:
        """Adjudicate one `_Travel`. Returns the Refusal it earns, or None if it is lawful.

        ONE polarity is enforced here: the measure B-anchor's NEGATIVE law (open by default; `BLOCKED
        { lineage }` closes). The mirror POSITIVE law — a derived successor family's `FERTILE { .. }`
        — is NOT enforced, and no branch for it is left behind (DG-3, ruling §1). Family law,
        certification evidence and runtime admission are three boundaries, and `FERTILE`/`License`
        currently sits on the second; using it as the third would reinterpret it. When the successor-
        travel carrier is settled, the polarity it needs arrives with the change that reads it."""
        # ADDRESSABILITY IS A PRIOR QUESTION. If a target level is reachable from NO source level, the
        # ask fails because it is out of the contracted space — not because of a lineage law — and the
        # existing out_of_universe / uncertified-travel machinery gives the truer diagnosis. Without
        # this guard every unaddressable ask would be charged for the out-edges of the source levels it
        # "collapses", and `level.sum @ product` would refuse for the wrong reason. A target that IS
        # reachable while a sibling source level collapses is still adjudicated (that is DG-2's case).
        if any(all(self.m.find_path({d}, T) is None for d in t.frm) for T in t.to):
            return None
        crossed = self._traversed_lineages(t.frm, t.to)
        bad = sorted(crossed & t.law)               # NEGATIVE: prohibited iff a BLOCKED lineage is crossed
        if not bad:
            return None
        lin = bad[0]
        how = ("declared" if t.written else "generated")
        return Refusal("blocked_reduction",
            f"'{t.subject}' reduces by '{t.op}' across blocked lineage '{lin}' — "
            f"'{t.op}' is declared BLOCKED along '{lin}', so this reduction has no lawful "
            f"reading at {_fmt_anchor(t.to)}; per-bucket totals do not reconcile along this axis. "
            f"Generating a new family does not create the permission: the {how} reducer needs "
            f"the same authority the declaration withholds.",
            target=_fmt_anchor(t.to),
            alternatives=(f"use a reducer that IS applicable along '{lin}' "
                          f"(e.g. '.last' for a stock collapsed over time)",
                          f"address at an anchor that does not cross '{lin}'"))

    def _check_expression_law(self, node, anchor):
        """The single law chokepoint for a column expression. Raises the OUTERMOST violation, so the
        reader is told about the operation they actually wrote rather than one of its ingredients."""
        for t in self._law_travels(node, tuple(anchor)):
            r = self._travel_violation(t)
            if r is not None:
                raise r

    def _lawful_pins(self, reducer, inner, anchor) -> list:
        """The GOVERNED CANDIDATE input anchors for an unpinned generated reduction, filtered to the
        ones for which the requested generated operation is actually LAWFUL (ruling §9).

        Never offer a candidate that is already structurally illegal: a clarify is a menu of readings
        the asker may choose between, and an unlawful reading is not a choice — offering it would make
        Clarify reachable before lawfulness, which is how a reader gets talked into a laundered answer.
        Both the pin lattice laws and the generated-family law are applied here."""
        levels = {e.frm for e in self.m._edges} | {e.to for e in self.m._edges}
        out = []
        for L in sorted(levels):
            if L in anchor:
                continue
            if not any(self.m.find_path({L}, T) is not None for T in anchor):
                continue
            pin = (L,)
            try:
                self._check_pin_laws(pin, tuple(anchor))
            except Refusal:
                continue                                    # pin_coarser_than_output / redundant_pin
            grain = self._pin_input_grain(pin, tuple(anchor))
            if self._travel_violation(self._generated_travel(reducer, inner, grain, anchor, pin)):
                continue                                    # structurally prohibited: not a choice
            out.append(L)
        return out

    def _column_fill_rule(self, node, anchor):
        """Φ_v for a column: the fill rule of its member(s) (columna#143). A column resolves to ONE
        universe (§2c); if all its measure atoms agree on a single declared rule, that is the column's
        rule. A conflict between atoms — or no declared rule — is UNDECLARED, and undeclared means the
        engine discloses the absence rather than choose a value (never keyed on basis)."""
        rules = {getattr(self.m.measures.get(m), "fill_rule", None)
                 for (m, _mem) in self._atoms(node, anchor)}
        return next(iter(rules)) if len(rules) == 1 else None

    # ---- PLAN: the would-be annotation WITHOUT executing (zero backend fetches) -------------
    def plan(self, anchor: tuple, columns: list, where: Optional[str] = None, population: Optional[str] = None,
             where_unreachable: Optional[dict] = None) -> "FrameResult":
        """Compile-only: typecheck + addressability + structural crossings + the spec-only
        provenance disclosure (engine.dry_disclose) — assembled into the would-be annotation,
        touching no data. This is EXPLAIN-without-execution: an agent sees the critical crossing
        (and the approximation/assumption caveats) before spending a single backend scan."""
        results = []
        for name, expr in columns:
            trace = []
            if where_unreachable and name in where_unreachable:  # filter_unreachable clarify, would-be
                results.append(ColumnResult(name, expr, None, Disclosure.of(population=None),
                                            refusal=where_unreachable[name].classified(), trace=trace))
                continue
            try:
                tree = ast.parse(expr, mode="eval")
                for n in ast.walk(tree):
                    if not isinstance(n, _ALLOWED):
                        raise Refusal("unknown", f"illegal expression construct: {type(n).__name__}")
                self._check_expression_law(tree.body, anchor)               # generated-family law (2026-08-20)
                self._infer(tree.body, anchor, population)                 # static typecheck + addressability
                col_uni = self._check_single_universe(tree.body, anchor)    # §2c expr law + column universe
                blk = self._blocked_transport(tree.body, anchor)
                if blk is not None:
                    raise self._blocked_transport_refusal(blk)
                disc = Disclosure.clean()
                for (m, mem) in self._atoms(tree.body, anchor):
                    disc = Disclosure.merge(disc, self.engine.dry_disclose(m, mem, anchor))
                    trace.append(f"plan {m}.{mem} @ {_fmt_anchor(anchor)} (would-be annotation; no execution)")
                for c in self._would_be_defaulted_caveats(tree.body, anchor):
                    disc = disc.with_caveat(c)                 # §9 |L|=1: predict the material default
                results.append(ColumnResult(name, expr, None, disc, trace=trace, universe=col_uni,
                                            fill_rule=self._column_fill_rule(tree.body, anchor)))
            except Refusal as r:
                results.append(ColumnResult(name, expr, None,
                                Disclosure.of(population=None), refusal=r.classified(), trace=trace))
        # §2c frame law: no frame-level multi-universe `coverage` caveat (retired) — per-column honesty.
        frame_disc = Disclosure.merge(*[c.disclosure for c in results if c.refusal is None])
        return FrameResult(None, frame_disc, results, anchor)

    # ---- COMPILE: static type inference + vocabulary checks (no engine) -----
    def _infer(self, node, anchor, population=None):
        """Infer the logical dtype of an expression and raise any STATIC refusal
        (unknown column/operator, type mismatch, fan-out, out-of-universe). Calls no
        engine: every error here is knowable from vocabulary/shape alone."""
        if isinstance(node, ast.Constant):
            return "Float64"
        rc = self._reduction_call(node)
        if rc is not None:
            reducer, inner, pinned = rc
            if pinned is None:
                # UNPINNED: the input anchor is structurally underdetermined. Since 2026-08-20 the
                # candidates are filtered for LAWFULNESS first (§9): no lawful candidate refuses,
                # exactly one is not contested and is defaulted to (the caller owes the material
                # input_anchor caveat), several still clarify — over the lawful ones only.
                pinned = self._unpinned_disposition(reducer, inner, anchor)
            # WP-GRAIN-1: a pinned reduction serves at a MULTI-level anchor with a COMPOSITE input
            # anchor. Laws 1 & 2 are static checks over the pin × output lattice (refuse coarser-than-
            # output pins; clarify cross-comparable pins), classified here at the static chokepoint.
            self._check_pin_laws(pinned, anchor)
            # The pinned levels pin their lineage; orthogonal output dims join the input grain (see
            # _resolve_inline_reduction). Typecheck the inner at that composite grain.
            in_dt = self._infer(inner, self._pin_input_grain(pinned, anchor), population)
            return self._reducer_out_dtype(reducer, in_dt)
        sc = self._scan_call(node)
        if sc is not None:
            scan_op, arg, _n, _by = sc
            in_dt = self._infer(arg, anchor, population)        # the scanned measure is itself typechecked
            sig = self.m.operators[scan_op]
            if in_dt not in sig.accepts:
                raise Refusal("type_error",
                    f"scan '{scan_op}' does not accept logical type '{in_dt}' "
                    f"(accepts {sorted(sig.accepts)})",
                    alternatives=("scan a numeric/ordered measure",))
            return self.m.output_dtype(scan_op, in_dt)
        meas_name, member = self._measure_ref(node)
        if meas_name is not None:
            if meas_name in self.m.derived:
                dshape = self.m.derived[meas_name]
                # an AT-metric typechecks at its RESOLUTION anchor (where the formula is evaluated),
                # then the reduction is a downstream engine step — not at the asked anchor.
                infer_anchor = (dshape.resolution_anchor,) if dshape.resolution_anchor else anchor
                return self._infer(ast.parse(dshape.formula, mode="eval").body, infer_anchor, population)
            if meas_name not in self.m.measures:
                raise Refusal("unknown", f"unknown column '{meas_name}'")
            meas = self.m.measures[meas_name]
            # ON UNIVERSE pin: the frame's intended population is asserted. A measure not bound to
            # the pinned universe lives over a different population, so it is out-of-domain FOR THAT
            # population and refuses; measures bound to it serve — which resolves the multi-universe
            # and co-anchoring ambiguity to the one chosen population. (Resolving a measure over a
            # universe OTHER than its declared one is cross-universe confinement — Option B, future.)
            if population is not None:
                if population not in self.m.universes:
                    raise Refusal("unknown",
                        f"ON UNIVERSE '{population}' is not a declared universe "
                        f"(have {sorted(self.m.universes)})")
                if meas.universe != population:
                    raise Refusal("out_of_universe",
                        f"{meas_name} is bound to universe '{meas.universe}', not the pinned "
                        f"population '{population}' — it is not defined over that population",
                        measure=meas_name, target=population,
                        alternatives=(f"pin ON UNIVERSE '{meas.universe}' (this measure's population)",
                                      f"use a measure bound to '{population}'"))
            if member is None:
                if len(meas.family) != 1:
                    raise Refusal("unknown",
                        f"'{meas_name}' has a family {list(meas.family)} — specify a member")
                member = next(iter(meas.family))
            elif member not in meas.family:
                if member not in self.m.operators:
                    raise Refusal("unknown",
                        f"operator '{member}' is not supported (registry: {sorted(self.m.operators)})",
                        measure=meas_name)
                raise Refusal("unknown", f"'{meas_name}' has no family member '{member}' (have {list(meas.family)})")
            sig = self.m.operators.get(member)
            if sig is None:
                raise Refusal("unknown",
                    f"operator '{member}' is not supported (registry: {sorted(self.m.operators)})",
                    measure=meas_name)
            if meas.logical_type not in sig.accepts:
                raise Refusal("type_error",
                    f"{meas_name}.{member}: '{member}' does not accept logical type "
                    f"'{meas.logical_type}' (accepts {sorted(sig.accepts)})", measure=meas_name,
                    alternatives=("use an operator whose signature accepts this type",))
            for T in anchor:
                self._check_addressable(meas_name, T)
            return self.m.output_dtype(member, meas.logical_type)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return self._infer(node.operand, anchor, population)
        if isinstance(node, ast.BinOp):
            ldt = self._infer(node.left, anchor, population)
            rdt = self._infer(node.right, anchor, population)
            op = _OP[type(node.op)]
            sig = self.m.operators.get(op)          # the MAP operator, from the umbrella registry
            if sig is None or sig.kind != "map":
                raise Refusal("unknown", f"'{op}' is not a registered map operator")
            for side, dt in (("left", ldt), ("right", rdt)):
                if dt not in sig.accepts:
                    raise Refusal("type_error",
                        f"map '{op}' requires {sorted(sig.accepts)} operands; {side} operand is '{dt}'",
                        alternatives=("apply a numeric-valued operator/measure on that side",))
            # NOTE: cross-universe combination (the old D5 co-anchoring clarify) is no longer detected
            # per-operator here — §2c's EXPRESSION LAW checks the whole column expression once, in
            # `_check_single_universe` (below), raising the `cross_universe` ERROR. One universe per
            # expression; the denotation rule leaves nothing ambiguous within it.
            return "Float64" if op == "/" else (ldt if ldt == rdt else "Float64")
        raise Refusal("unknown", f"unsupported expression node {type(node).__name__}")

    def _node(self, node, anchor, where, trace):
        if isinstance(node, ast.Constant):
            return "scalar", float(node.value), Disclosure.clean(), "Float64"

        rc = self._reduction_call(node)
        if rc is not None:
            return self._resolve_inline_reduction(rc, anchor, where, trace)

        sc = self._scan_call(node)
        if sc is not None:
            scan_op, arg, n, by = sc
            m_name, member = self._measure_ref(arg)
            if m_name is None or m_name not in self.m.measures:
                raise Refusal("unknown",
                    f"scan '{scan_op}' input must be a measure column "
                    f"(e.g. {scan_op}(revenue.sum)); got a non-column expression")
            meas = self.m.measures[m_name]
            if member is None:
                member = next(iter(meas.family)) if len(meas.family) == 1 else None
                if member is None:
                    raise Refusal("unknown",
                        f"'{m_name}' has a family {list(meas.family)} — specify a member to scan")
            out_dtype = self.m.output_dtype(scan_op, self.m.output_dtype(member, meas.logical_type))
            routes = {}                                        # P0.5a: plan, then execute the plan
            for T in anchor:
                self._check_addressable(m_name, T, routes)
            order_axis = self.plan_order_axis(scan_op, m_name, anchor, by)
            frame, disc = self.engine.scan(m_name, member, anchor, scan_op,
                                           n=n, by=by, where=where, trace=trace,
                                           routes=routes, split=self._split_dependent(anchor),
                                           order_axis=order_axis)
            return "col", frame.rename({"_value": _V}), disc, out_dtype

        meas_name, member = self._measure_ref(node)
        if meas_name is not None:
            if meas_name in self.m.derived:
                dshape = self.m.derived[meas_name]
                if dshape.resolution_anchor is not None:
                    return self._resolve_anchored_metric(meas_name, dshape, anchor, where, trace)
                return self._node(ast.parse(dshape.formula, mode="eval").body,
                                  anchor, where, trace)
            if meas_name not in self.m.measures:
                raise Refusal("unknown", f"unknown column '{meas_name}'")
            meas = self.m.measures[meas_name]
            if member is None:
                if len(meas.family) != 1:
                    raise Refusal("unknown",
                        f"'{meas_name}' has a family {list(meas.family)} — specify a member, e.g. {meas_name}.{next(iter(meas.family))}")
                member = next(iter(meas.family))
            elif member not in meas.family:
                # operator-not-supported is a VOCABULARY error, caught here, not a data error:
                # distinguish "no such operator in the language" from "this measure lacks it".
                if member not in self.m.operators:
                    raise Refusal("unknown",
                        f"operator '{member}' is not supported (registry: {sorted(self.m.operators)})",
                        measure=meas_name)
                raise Refusal("unknown", f"'{meas_name}' has no family member '{member}' (have {list(meas.family)})")
            # type signature check (vocabulary): does the operator accept this column's dtype?
            sig = self.m.operators.get(member)
            if sig is None:
                raise Refusal("unknown",
                    f"operator '{member}' is not supported (registry: {sorted(self.m.operators)})",
                    measure=meas_name)
            if meas.logical_type not in sig.accepts:
                raise Refusal("type_error",
                    f"{meas_name}.{member}: '{member}' does not accept logical type "
                    f"'{meas.logical_type}' (accepts {sorted(sig.accepts)})",
                    measure=meas_name,
                    alternatives=("use an operator whose signature accepts this type",))
            # addressability (fan-out / out-of-universe) — also static, also pre-engine. P0.5a: the
            # same pass RECORDS the certified route for each target; the engine executes exactly it.
            routes = {}
            for T in anchor:
                self._check_addressable(meas_name, T, routes)
            out_dtype = self.m.output_dtype(member, meas.logical_type)
            frame, disc = self.engine.resolve(meas_name, member, anchor, where, trace,
                                              routes=routes, split=self._split_dependent(anchor))
            return "col", frame.rename({"_value": _V}), disc, out_dtype

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            k, p, d, dt = self._node(node.operand, anchor, where, trace)
            if k == "scalar":
                return "scalar", -p, d, dt
            return "col", p.with_columns((-pl.col(_V)).alias(_V)), d, dt

        if isinstance(node, ast.BinOp):
            lk, lp, ld, ldt = self._node(node.left, anchor, where, trace)
            rk, rp, rd, rdt = self._node(node.right, anchor, where, trace)
            op = _OP[type(node.op)]
            return self._apply(op, lk, lp, ld, ldt, rk, rp, rd, rdt, list(anchor))

        raise Refusal("unknown", f"unsupported expression node {type(node).__name__}")

    # ---- resolution-anchor metric (WP-B B-4): a DISTINCT reading, never the pooled sibling ----
    def _resolve_anchored_metric(self, name, dshape, anchor, where, trace):
        """`DERIVED <name> = <formula> AT <res> FAMILY { <member> ... }` is a distinct metric: the
        <member>-reduction of the formula evaluated at <res> (e.g. the mean of daily rates). Evaluate
        the formula AT the resolution anchor, then reduce by the declared member to the asked level.
        This is the metric's DECLARED meaning — no interaction with the pooled `<formula> @ anchor`
        sibling, and the engine NEVER substitutes one reading for the other (never-substitute)."""
        res = dshape.resolution_anchor
        if len(anchor) != 1:
            raise Refusal("unsupported",
                f"resolution-anchor metric '{name}' is served at a single level — its meaning is a "
                f"reduction of the '{res}'-resolved series; asked at {_fmt_anchor(anchor)}")
        if len(dshape.members) != 1:
            raise Refusal("unknown",
                f"resolution-anchor metric '{name}' needs exactly one reduction member "
                f"(declared: {list(dshape.members)})")
        target, member = anchor[0], dshape.members[0]
        # evaluate the formula AT the resolution anchor — the denotation there (recompute-from-components)
        k, frame, disc, dtype = self._node(ast.parse(dshape.formula, mode="eval").body,
                                           (res,), where, trace)
        if k != "col":
            raise Refusal("unknown", f"resolution-anchor metric '{name}' formula is not a column")
        if trace is not None:
            trace.append(f"resolution-anchor metric '{name}' = {member} of ({dshape.formula})@{res} -> {target}")
        if target == res:
            return "col", frame, disc, dtype                # asked AT the anchor: the denotation itself
        # P0.5a GAP 1 (ruling 2026-08-11): the RESOLUTION anchor says where the metric is FORMED; the
        # REQUESTED anchor says where it must lawfully travel. `_infer` recurses at the resolution
        # anchor, which is right for typing but erases the travel obligation — so establish it here.
        # An AT-metric must never serve where the equivalent ordinary metric refuses.
        path = self.m.find_path({res}, target)
        if path is None:
            self._refuse_uncertified_travel(name, res, target)
        reduced = self.engine.reduce_series(frame, res, target, member, trace,
                                            route=tuple(e.key for e in path[1]))
        return "col", reduced, disc, dtype

    # ---- inline reduction of a derivation (WP-B.1): the same reading, expressed without a name ----
    def _resolve_inline_reduction(self, rc, anchor, where, trace):
        """`R(inner @ level)` at frame anchor T: resolve `inner` at its PINNED input anchor `level`,
        then reduce that series to T by R — a definite quantity (capture v0.8). Served with an
        IMMATERIAL communicative disclosure naming the reading (the `provenance`/transport code).

        OF-2 boundary (ruled 2026-07-14): the material `input_anchor` caveat is for an anchor choice
        IMPORTED from a name or DEFAULTED — one the reader must weigh. An EXPLICIT pin owes only the
        immaterial `provenance` note, because the wire's reader may not be the asker: the note names
        the reading for a downstream reader without asserting a decision-relevant assumption the asker
        already made deliberately. Unpinned is caught statically in `_infer`; this defends the
        direct-`_node` path."""
        reducer, inner, pinned = rc
        defaulted = pinned is None
        if defaulted:
            pinned = self._unpinned_disposition(reducer, inner, anchor)
        self._check_pin_laws(pinned, anchor)                   # defends the direct-_node path (see _infer)
        # WP-GRAIN-1: the pinned levels pin THEIR lineage's resolution; output reduction dimensions
        # ORTHOGONAL to the pin (reachable from no pin level) join the input grain so the series carries
        # them, then everything reduces to the output anchor (dependent levels attached 1:1).
        input_grain = self._pin_input_grain(pinned, anchor)
        k, frame, disc, dtype = self._node(inner, input_grain, where, trace)
        if k != "col":
            raise Refusal("unknown", f"inline reduction input '{ast.unparse(inner)}' is not a column")
        out_dtype = self._reducer_out_dtype(reducer, dtype)
        pin_str = self._fmt_pin(pinned)
        reading = f"{reducer} of {ast.unparse(inner)}@{pin_str}"
        if trace is not None:
            trace.append(f"inline reduction: {reading} -> {_fmt_anchor(anchor)}")
        if anchor == tuple(pinned):
            served = frame                                     # asked AT the pinned anchor: no travel
        else:
            # P0.5a: the planner chooses BOTH the source axis and the route for every reduction and
            # attach target, over the certified graph. The engine executes them and picks nothing.
            split = self._split_dependent(anchor)
            red_routes, att_routes = {}, {}
            for rt in split[0]:
                if rt in input_grain:
                    continue
                src = next((g for g in input_grain
                            if g == rt or self.m.find_path({g}, rt) is not None), None)
                if src is None:
                    self._refuse_uncertified_travel(ast.unparse(inner), str(list(input_grain)), rt)
                red_routes[rt] = self._route(self.m.find_path({src}, rt))
            for T in split[1]:
                S = next((x for x in split[0] if self.m.find_path({x}, T) is not None), None)
                if S is None:
                    self._refuse_uncertified_travel(ast.unparse(inner), str(list(split[0])), T)
                att_routes[T] = self._route(self.m.find_path({S}, T))
            served = self.engine.reduce_series_to_anchor(frame, input_grain, anchor, reducer, trace,
                                                         reduction_routes=red_routes,
                                                         attach_routes=att_routes, split=split)
        target = _fmt_anchor(anchor)
        # Law 4 — the two-stage-statistic disclosure, IMMATERIAL (provenance/transport), never a caveat.
        # Rider: a COMPOSITE pin whose levels include an axis PRESENT in the output names it as the fixed
        # axis and the others as reduced, so the reader sees which coordinate is fixed vs reduced over.
        fixed = [p for p in pinned if p in anchor]
        if len(pinned) > 1 and fixed:
            reduced = [p for p in pinned if p not in anchor]
            clause = f"pin fixes {', '.join(fixed)}"
            if reduced:
                clause += f", reduces over {', '.join(reduced)}"
            text = f"'{reading}' reduced to {target} — {clause}"
        else:
            text = (f"'{reading}' reduced to {target} — the {reading} reading (input anchor pinned "
                    f"to '{pin_str}'), not the pooled value at {target}")
        note = Caveat(TRANSPORT, text, source=f"{pin_str}->{target}")
        out = Disclosure.merge(disc, Disclosure.of(note), population=disc.population)
        if defaulted:
            out = out.with_caveat(self._defaulted_anchor_caveat(reducer, inner, pinned, anchor))
        return "col", served, out, out_dtype

    def _defaulted_anchor_caveat(self, reducer, inner, pinned, anchor) -> "Caveat":
        """OF-2, the DEFAULTED half: the reader did not choose this input anchor — the planner did,
        because exactly one lawful reading survived (§9). That is a decision-relevant assumption, so it
        rides as a MATERIAL `input_anchor` caveat, not the immaterial provenance note an explicit pin
        owes. A defaulted anchor is disclosed, never silent.

        Built HERE, in one place, because `plan()` must predict it byte-for-byte: the whole promise of
        EXPLAIN is that the would-be annotation is the annotation. Deriving it twice is how they drift."""
        pin_str, target = self._fmt_pin(pinned), _fmt_anchor(anchor)
        return Caveat(UNCONFIRMED,
            f"input anchor was not given and was DEFAULTED to '{pin_str}' — the only grain at "
            f"which '{reducer}({ast.unparse(inner)})' has a lawful reading at {target}; pin it "
            f"explicitly to make the choice yours",
            source=f"{pin_str}->{target}")

    def _would_be_defaulted_caveats(self, node, anchor) -> list:
        """The defaulted-input-anchor caveats `run` WILL attach, computed without executing anything.

        `plan()` builds its would-be annotation from `engine.dry_disclose` over the expression's ATOMS,
        which cannot see a decision taken above an atom — so before this existed, `SELECT avg(aov) AT
        {cal.month}` planned as `serve` and ran as `disclose`, and EXPLAIN under-reported a material
        condition. That is the one thing EXPLAIN may never do. The defaulting is a pure shape fact
        (`_unpinned_disposition` reads declarations and structure, never a value), so it is knowable at
        compile time and costs no fetch."""
        out = []
        if isinstance(node, ast.Constant):
            return out
        rc = self._reduction_call(node)
        if rc is not None:
            reducer, inner, pinned = rc
            grain = anchor
            if pinned is None:
                pinned = self._unpinned_disposition(reducer, inner, tuple(anchor))
                out.append(self._defaulted_anchor_caveat(reducer, inner, pinned, tuple(anchor)))
            grain = self._pin_input_grain(pinned, tuple(anchor))
            return out + self._would_be_defaulted_caveats(inner, grain)
        sc = self._scan_call(node)
        if sc is not None:
            return self._would_be_defaulted_caveats(sc[1], anchor)
        meas_name, _member = self._measure_ref(node)
        if meas_name is not None:
            if meas_name in self.m.derived:
                dshape = self.m.derived[meas_name]
                inner = ast.parse(dshape.formula, mode="eval").body
                grain = ((dshape.resolution_anchor,) if dshape.resolution_anchor else tuple(anchor))
                return self._would_be_defaulted_caveats(inner, grain)
            return out
        if isinstance(node, ast.UnaryOp):
            return self._would_be_defaulted_caveats(node.operand, anchor)
        if isinstance(node, ast.BinOp):
            return (self._would_be_defaulted_caveats(node.left, anchor)
                    + self._would_be_defaulted_caveats(node.right, anchor))
        return out

    def _apply(self, op, lk, lp, ld, ldt, rk, rp, rd, rdt, keys):
        # map operands are typechecked against the umbrella registry's MAP signature (vocabulary)
        sig = self.m.operators.get(op)
        for side, dt in (("left", ldt), ("right", rdt)):
            if dt not in sig.accepts:
                raise Refusal("type_error",
                    f"map '{op}' requires {sorted(sig.accepts)} operands; {side} operand is '{dt}'",
                    alternatives=("apply a numeric-valued operator/measure on that side",))
        out_dt = "Float64" if op == "/" else (ldt if ldt == rdt else "Float64")
        disc = Disclosure.combine(op, ld, rd, label=op)
        f = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
             "*": lambda a, b: a * b, "/": lambda a, b: a / b}[op]
        if lk == "col" and rk == "col":
            j = lp.join(rp, on=keys, how="inner", suffix="_r")
            return "col", j.with_columns(f(pl.col(_V), pl.col(f"{_V}_r")).alias(_V)).select(keys + [_V]), disc, out_dt
        if lk == "col":
            return "col", lp.with_columns(f(pl.col(_V), rp).alias(_V)), disc, out_dt
        if rk == "col":
            return "col", rp.with_columns(f(lp, pl.col(_V)).alias(_V)), disc, out_dt
        return "scalar", f(lp, rp), disc, out_dt

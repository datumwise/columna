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
from dataclasses import dataclass, field
from typing import Optional
import polars as pl

from .projection import PlannerView
from .engine import ColumnEngine
from .disclosure import (Disclosure, Refusal, Caveat, B_ANCHOR_CROSSING, TRANSPORT, DATA_GAP,
                         SERVE, DISCLOSE, CLARIFY, REFUSE, ERROR, AMBIGUOUS, Outcome)

_ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Name, ast.Attribute,
            ast.Load, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub,
            ast.MatMult,  # `@` — the INPUT-ANCHOR pin inside an inline reduction (aov@day)
            ast.Call, ast.keyword)
_OP = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}
_V = "_v"


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
    universe: Optional[str] = None      # the column's sole universe (§2c) — routes B3 absence semantics


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
        # the published SCOPE (set by publish/reattest): cut declarations (asserts) and blocked edges
        # (refuted hierarchies). A column touching a cut refuses `conflicting_data`; a column whose
        # transport crosses a blocked edge refuses `contradicted_edge`. Serving never outruns the verdicts.
        self.cut: frozenset = frozenset()
        self.cut_by: dict = {}
        self.blocked_edges: frozenset = frozenset()    # {(frm, to)} — transport across these is refused
        self.blocked_by: dict = {}                      # (frm, to) -> [{lineage, key}]

    def _cut_hit(self, expr: str) -> Optional[str]:
        """The first CUT declaration a column expression references (measure or derived), or None.
        Serving never outruns the verdicts: a query into a cut region is withheld."""
        if not self.cut:
            return None
        for ref in re.findall(r"[A-Za-z_]\w*(?:\.\w+)*", expr):
            head = ref.split(".", 1)[0]
            if head in self.cut:
                return head
        return None

    def _blocked_transport(self, node, anchor) -> Optional[tuple]:
        """The first BLOCKED edge (frm, to) a column's transport crosses, or None. A refuted hierarchy
        blocks its edge; any measure whose resolution to an anchor level travels that edge refuses."""
        if not self.blocked_edges:
            return None
        for measure, _member in self._atoms(node, anchor):
            ms = self.m.measures.get(measure)
            if ms is None:
                continue
            base = self.m.universes[ms.universe].base_dimensions
            for T in anchor:
                path = self.m.find_path(base, T)
                if path is None:
                    continue
                for e in path[1]:
                    if (e.frm, e.to) in self.blocked_edges:
                        return (e.frm, e.to)
        return None

    def _blocked_transport_refusal(self, edge: tuple) -> "Refusal":
        rec = (self.blocked_by.get(edge) or [{}])[0]
        lineage, key = rec.get("lineage"), rec.get("key")
        return Refusal("contradicted_edge",
            f"transport along edge {edge[0]}->{edge[1]} (lineage '{lineage}') is BLOCKED: its declared "
            f"functional dependence is refuted on the attested data (key {key!r} has >1 parent); the "
            f"reduction across it is withheld — serving never outruns the verdicts.",
            edge=f"{edge[0]}->{edge[1]}",
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

    def _cut_refusal(self, decl: str) -> "Refusal":
        rec = (self.cut_by.get(decl) or [{}])[0]
        ce = rec.get("counterexample")
        who = (f"assert '{rec['assert']}' ON '{rec['universe']}'" if rec.get("assert")
               else "a declared invariant")
        coord = f" (counterexample @ {ce.get('anchor')})" if ce else ""
        return Refusal("conflicting_data",
            f"'{decl}' is in a CUT region: {who} is violated on the attested data{coord}; serving is "
            f"withheld here — serving never outruns the verdicts.",
            measure=decl,
            alternatives=("fix the data and re-attest", "amend the assert", "accept the reduced scope"))

    # ---- typecheck: addressability (fan-out / out-of-universe caught here) --
    def _check_addressable(self, measure: str, T: str):
        meas = self.m.measures[measure]
        uni = meas.universe
        base = self.m.universes[uni].base_dimensions
        if self.m.find_path(base, T) is not None:
            return
        # fan-out: T reachable only across a non-functional (M:N) edge from this universe
        for (nf, nt, detail) in self.m.non_functional:
            reach_nf = (nf in base) or (self.m.find_path(base, nf) is not None)
            reach_t = (nt == T) or (self.m.find_path([nt], T) is not None)
            if reach_nf and reach_t:
                raise Refusal("non_functional_transport",
                    f"{measure} @ {T}: relating crosses a non-functional (M:N) edge "
                    f"{nf}\u2194{nt} ({detail}); this aggregate-across is underdetermined — the "
                    f"measure would be replicated across matches and the total inflated",
                    measure=f"{measure}@transaction", target=T, edge=f"{nf}\u2194{nt}",
                    alternatives=("membership filter — accept the overlap deliberately ('revenue "
                                  "touching each "+T+"')",
                                  "primary designation — make the "+nf+"\u2192"+nt+" edge functional",
                                  "WITH allocation — supply a partition-of-unity split [Pro]"))
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
                if lev not in self.m.levels:
                    raise FrameQLSyntaxError(
                        f"anchor '{tok}': no level named '{lev}' — qualify an existing level as "
                        f"family.level, or name a level directly")
                fams = self._families_of(lev)
                if fam not in fams:
                    raise FrameQLSyntaxError(
                        f"anchor '{tok}': level '{lev}' is not in dimension family '{fam}' — it belongs "
                        f"to {sorted(fams) if fams else 'no dimension family'}")
                out.append(lev)
                continue
            # bare, non-universe, non-level token: unchanged — addressability handles the unknown level
            out.append(tok)
        return tuple(out)

    # ---- run a frame -------------------------------------------------------
    def run(self, anchor: tuple, columns: list, where: Optional[str] = None, population: Optional[str] = None) -> FrameResult:
        results = []
        for name, expr in columns:
            trace = []
            try:
                # COMPILE: static typecheck (vocabulary, signatures, addressability, expression
                # typing) — no engine calls. Operator-not-supported and type errors are caught
                # HERE, before any backend work; they are vocabulary errors, not data errors.
                tree = ast.parse(expr, mode="eval")
                for n in ast.walk(tree):
                    if not isinstance(n, _ALLOWED):
                        raise Refusal("unknown", f"illegal expression construct: {type(n).__name__}")
                # cut-state (B1): a column touching a CUT declaration refuses as the conflicting_data
                # mood — checked before typecheck/execution (serving never outruns the verdicts).
                cut_decl = self._cut_hit(expr)
                if cut_decl is not None:
                    raise self._cut_refusal(cut_decl)
                self._infer(tree.body, anchor, population)
                col_uni = self._check_single_universe(tree.body, anchor)  # §2c expr law + the column's universe
                blk = self._blocked_transport(tree.body, anchor)          # transport across a refuted-hierarchy edge
                if blk is not None:
                    raise self._blocked_transport_refusal(blk)
                # B-anchor crossings are STRUCTURAL — detected HERE (compile, shape-only), not in
                # the engine. Inform-and-serve: they ride into the served disclosure unchanged.
                crossings = self._frame_crossings(tree.body, anchor)
                # EXECUTE: resolve through the engine
                frame, disc = self._eval(expr, anchor, where, trace)
                if crossings:
                    disc = Disclosure.merge(disc, Disclosure.of(*crossings), population=disc.population)
                results.append(ColumnResult(name, expr, frame.rename({_V: name}), disc,
                                            trace=trace, universe=col_uni))
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

        # B3 ABSENCE SEMANTICS (basis-driven). Absence is only definable relative to a DOMAIN; the
        # juxtaposition (the full-outer align above) supplies one LOCALLY, so a column's null cells here
        # take meaning from THAT column's own universe basis. Serving follows the DECLARATION — like a
        # B-anchor bar, it executes regardless of any License (BASIS is a semantic declaration, not a
        # shortcut). The declared spine-grid (the future domain source) is the single object behind both
        # single-column fill and the completeness oracle (open_forks OF-5); until it lands, absence is
        # scoped to the align, so a single-column frame (no nulls) is untouched.
        if data is not None:
            for c in results:
                if c.frame is None or c.universe is None:
                    continue
                basis = self.m.universes[c.universe].basis
                if basis is None:
                    continue
                n_absent = data[c.name].null_count()
                if not n_absent:
                    continue
                if basis == "events":                        # absence is the honest ZERO
                    data = data.with_columns(pl.col(c.name).fill_null(0))
                    c.disclosure = c.disclosure.with_caveat(Caveat(TRANSPORT,        # immaterial, agent-legible
                        f"{n_absent} absent cell(s) rendered as 0 per events basis"))
                elif basis in ("spine", "product"):          # absence is a GAP
                    c.disclosure = c.disclosure.with_caveat(Caveat(DATA_GAP,
                        f"{n_absent} absent cell(s) are gaps ({basis} basis) — the data is incomplete here"))

        # No frame-level population caveat: the old multi-universe `coverage` caveat is RETIRED (§2c). Per-
        # column honesty replaces it — a juxtaposed frame never asserts a single shared population, and
        # ON UNIVERSE is dead in the query grammar (cross-universe combination is an authoring act).
        frame_disc = Disclosure.merge(*[c.disclosure for c in results if c.frame is not None])
        return FrameResult(data, frame_disc, results, anchor)

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

    def _reduction_call(self, node):
        """Recognize an inline reduction: `R(inner)` or `R(inner @ level)`, R a reducing operator.
        Returns (reducer, inner_node, pinned_level | None), or None if `node` is not such a call. The
        `@` (MatMult) PINS the input anchor: pinned ⇒ a definite quantity; unpinned ⇒ the input anchor
        is structurally underdetermined (an engine clarify — capture v0.8)."""
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
            if not isinstance(arg.right, ast.Name):
                raise Refusal("unknown",
                    f"inline reduction input anchor must be a level name, e.g. {node.func.id}(aov@day)")
            return r, arg.left, arg.right.id
        return r, arg, None

    @staticmethod
    def _reducer_out_dtype(reducer: str, in_dt: str) -> str:
        """Output dtype of an inline reducer over `in_dt` (mean/count are not registry operators)."""
        if reducer == "mean":
            return "Float64"
        if reducer == "count":
            return "Int64"
        return in_dt                                            # sum/min/max preserve the input dtype

    def _candidate_input_anchors(self, target: str):
        """The finer levels a reduction's input anchor could pin: every level with a functional path
        to the frame anchor. These are the alternatives an unpinned reduction's clarify enumerates."""
        levels = {e.frm for e in self.m._edges} | {e.to for e in self.m._edges}
        return sorted(L for L in levels
                      if L != target and self.m.find_path({L}, target) is not None)

    def _unpinned_reduction_refusal(self, reducer, inner, anchor):
        """The engine clarify for an inline reduction with no pinned input anchor (capture v0.8): the
        input anchor is structurally underdetermined, so enumerate the candidate anchors and choose
        none. Reason `input_anchor_ambiguous` (CLARIFY/AMBIGUOUS), sibling to `co_anchor_ambiguous`
        (OF-1, ruled 2026-07-14: one reason per contested dimension). It names the same dimension the
        pinned case's immaterial input-anchor note (OF-2) records."""
        expr = ast.unparse(inner)
        target = anchor[0] if len(anchor) == 1 else None
        cands = self._candidate_input_anchors(target) if target else []
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

    def _crossings(self, measure, member, anchor):
        """The critical b_anchor_crossing caveats for one atom at an anchor — knowable from the
        b-anchor's blocked lineages and the path/out-edge lineages alone (no provenance). Only a
        MONOID reducer reduces across an axis; a holistic reducer recomputes from base (b-anchor
        moot), and a scan/map preserves the anchor (its underlying reducer is checked as an atom)."""
        meas = self.m.measures[measure]
        blocked = meas.blocked.get(member, frozenset())
        sig = self.m.operators.get(member)
        if not blocked or sig is None or not (sig.kind == "reducer" and sig.is_monoid):
            return []
        cav = []
        base = set(self.m.universes[meas.universe].base_dimensions)
        # (1) the transport PATH itself coarsens across a blocked lineage
        for T in anchor:
            path = self.m.find_path(base, T)
            if path is None:
                continue
            for e in path[1]:
                if e.lineage in blocked:
                    cav.append(Caveat(B_ANCHOR_CROSSING,
                        f"{measure}.{member} ({member}) coarsens across blocked lineage "
                        f"'{e.lineage}' (edge {e.frm}->{e.to}); per-bucket totals do not "
                        f"reconcile along this axis",
                        severity="critical", source=f"{e.frm}->{e.to}",
                        remedy=f"use a reducer applicable along '{e.lineage}' "
                               f"(e.g. '.last' for a stock collapsed over time)"))
        # (2) a base dimension is COLLAPSED (marginalized) along a blocked lineage
        covered = set()
        for d in base:
            for T in anchor:
                if self.m.find_path([d], T) is not None:
                    covered.add(d); break
        for d in (base - covered):
            for e in self.m.out_edges(d):
                if e.lineage in blocked:
                    cav.append(Caveat(B_ANCHOR_CROSSING,
                        f"{measure}.{member} ({member}) collapses dimension '{d}' along "
                        f"blocked lineage '{e.lineage}' (reducing across the {e.lineage} axis "
                        f"is non-reconciling)",
                        severity="critical", source=d,
                        remedy=f"address at a finer anchor that preserves '{d}', or use a "
                               f"reconciling family member (e.g. '.last')"))
        return cav

    def _frame_crossings(self, node, anchor):
        """All crossing caveats for an expression, deduplicated across its atoms."""
        seen, out = set(), []
        for (m, mem) in self._atoms(node, anchor):
            for c in self._crossings(m, mem, anchor):
                k = (c.category, c.detail, c.source)
                if k not in seen:
                    seen.add(k); out.append(c)
        return out

    # ---- PLAN: the would-be annotation WITHOUT executing (zero backend fetches) -------------
    def plan(self, anchor: tuple, columns: list, where: Optional[str] = None, population: Optional[str] = None) -> "FrameResult":
        """Compile-only: typecheck + addressability + structural crossings + the spec-only
        provenance disclosure (engine.dry_disclose) — assembled into the would-be annotation,
        touching no data. This is EXPLAIN-without-execution: an agent sees the critical crossing
        (and the approximation/assumption caveats) before spending a single backend scan."""
        results = []
        for name, expr in columns:
            trace = []
            try:
                tree = ast.parse(expr, mode="eval")
                for n in ast.walk(tree):
                    if not isinstance(n, _ALLOWED):
                        raise Refusal("unknown", f"illegal expression construct: {type(n).__name__}")
                # cut-state (B1): a column touching a CUT declaration refuses as the conflicting_data
                # mood — checked before typecheck/execution (serving never outruns the verdicts).
                cut_decl = self._cut_hit(expr)
                if cut_decl is not None:
                    raise self._cut_refusal(cut_decl)
                self._infer(tree.body, anchor, population)                 # static typecheck + addressability
                col_uni = self._check_single_universe(tree.body, anchor)    # §2c expr law + column universe
                blk = self._blocked_transport(tree.body, anchor)
                if blk is not None:
                    raise self._blocked_transport_refusal(blk)
                disc = Disclosure.clean()
                for (m, mem) in self._atoms(tree.body, anchor):
                    disc = Disclosure.merge(disc, self.engine.dry_disclose(m, mem, anchor))
                    trace.append(f"plan {m}.{mem} @ {_fmt_anchor(anchor)} (would-be annotation; no execution)")
                for c in self._frame_crossings(tree.body, anchor):
                    disc = disc.with_caveat(c)
                results.append(ColumnResult(name, expr, None, disc, trace=trace, universe=col_uni))
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
                # UNPINNED: the input anchor is structurally underdetermined — a STATIC engine clarify
                # (capture v0.8), enumerating the candidate input anchors.
                raise self._unpinned_reduction_refusal(reducer, inner, anchor)
            if len(anchor) != 1:
                raise Refusal("unsupported",
                    f"inline reduction is served at a single frame level; asked at {_fmt_anchor(anchor)}")
            in_dt = self._infer(inner, (pinned,), population)    # typecheck the inner at its input anchor
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
            frame, disc = self.engine.scan(m_name, member, anchor, scan_op,
                                           n=n, by=by, where=where, trace=trace)
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
            # addressability (fan-out / out-of-universe) — also static, also pre-engine
            for T in anchor:
                self._check_addressable(meas_name, T)
            out_dtype = self.m.output_dtype(member, meas.logical_type)
            frame, disc = self.engine.resolve(meas_name, member, anchor, where, trace)
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
        reduced = self.engine.reduce_series(frame, res, target, member, trace)
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
        if pinned is None:
            raise self._unpinned_reduction_refusal(reducer, inner, anchor)
        if len(anchor) != 1:
            raise Refusal("unsupported",
                f"inline reduction is served at a single frame level; asked at {_fmt_anchor(anchor)}")
        target = anchor[0]
        k, frame, disc, dtype = self._node(inner, (pinned,), where, trace)
        if k != "col":
            raise Refusal("unknown", f"inline reduction input '{ast.unparse(inner)}' is not a column")
        out_dtype = self._reducer_out_dtype(reducer, dtype)
        reading = f"{reducer} of {ast.unparse(inner)}@{pinned}"
        if trace is not None:
            trace.append(f"inline reduction: {reading} -> {target}")
        if target == pinned:
            served = frame                                     # asked AT the pinned anchor: no travel
        else:
            served = self.engine.reduce_series(frame, pinned, target, reducer, trace)
        # communicative disclosure naming the reading — IMMATERIAL (provenance/transport), not a caveat
        note = Caveat(TRANSPORT,
                      f"'{reading}' reduced to {target} — the {reading} reading (input anchor pinned "
                      f"to '{pinned}'), not the pooled value at {target}",
                      source=f"{pinned}->{target}")
        return "col", served, Disclosure.merge(disc, Disclosure.of(note), population=disc.population), out_dtype

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

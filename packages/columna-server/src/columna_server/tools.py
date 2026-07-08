"""
columna_server.tools — the five read-only tools, as pure functions over a ManifoldStore.

Each returns a plain dict (the wire contract). query/explain serialize through
columna_core.disclosure_wire, so the MCP surface returns exactly the Python API's truth (ADR-032
D8, one contract). No SQL, no write path. Structural failures (unknown manifold/measure, malformed
query) raise ToolInputError; analytical outcomes (serve/disclose/clarify/refuse/error) are DATA in
the wire dict.
"""
from __future__ import annotations

from typing import Optional

from columna_core import disclosure_wire as dw

from .frameql import FrameQLSyntaxError, parse_frameql
from .store import ManifoldStore

CONTRACT_VERSION = dw.CONTRACT_VERSION

# evidence grade (model.py) -> wire provenance vocabulary (WP-2.2 ruling C)
_PROVENANCE = {"proven": "data_attested", "declared": "declared",
               "inferred_sample": "inferred", "inferred_docs": "inferred"}


class ToolInputError(ValueError):
    """A structural input error (unknown manifold/measure, malformed query) — surfaced by the MCP
    layer as an error result, distinct from an analytical `error` outcome carried in the wire."""


def _get(store: ManifoldStore, manifold_id: str):
    try:
        return store.get(manifold_id)
    except KeyError:
        raise ToolInputError(f"unknown manifold_id '{manifold_id}' (have {store.ids()})")


def _render_ref(ref) -> str:
    if ref.is_literal:
        return str(ref.value)
    return f"{ref.table}.{ref.column}" if ref.table else str(ref.column)


def _render_predicate(pred) -> Optional[str]:
    if pred is None or not pred.comparisons:
        return None
    return " AND ".join(f"{_render_ref(c.left)} {c.op} {_render_ref(c.right)}" for c in pred.comparisons)


# --- tool 1 ---------------------------------------------------------------------------------
def list_manifolds(store: ManifoldStore) -> dict:
    out = []
    for lm in store.all():
        m = lm.manifold
        out.append({"manifold_id": lm.manifold_id, "name": lm.name, "description": lm.description,
                    "n_measures": len(m.measures), "universes": list(m.universes)})
    return {"contract_version": CONTRACT_VERSION, "manifolds": out}


# --- tool 2 ---------------------------------------------------------------------------------
def describe_manifold(store: ManifoldStore, manifold_id: str) -> dict:
    lm = _get(store, manifold_id)
    m = lm.manifold
    dimensions = [{"level": lv.name, "realized_by": lv.realized_by, "is_base": lv.is_base}
                  for lv in m.levels.values()]
    edges = [{"frm": e.frm, "to": e.to, "lineage": e.lineage} for e in m.edges]
    universes = [{"name": u.name, "base_dimensions": sorted(u.base_dimensions),
                  "predicate": _render_predicate(u.predicate)} for u in m.universes.values()]
    measures = [{"name": mc.name, "family": list(mc.family), "universe": mc.universe}
                for mc in m.measures.values()]
    return {"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
            "dimensions": dimensions, "edges": edges, "universes": universes, "measures": measures}


# --- tool 3 ---------------------------------------------------------------------------------
def describe_measure(store: ManifoldStore, manifold_id: str, measure: str) -> dict:
    lm = _get(store, manifold_id)
    m = lm.manifold
    mc = m.measures.get(measure)
    if mc is None:
        raise ToolInputError(f"unknown measure '{measure}' in manifold '{manifold_id}' "
                             f"(have {sorted(m.measures)})")
    ops = lm.server.planner.m.operators   # OperatorSig registry (kind, is_monoid)

    member_anchors, reducer_kind = {}, {}
    for member, fm in mc.family.items():
        sig = ops.get(member)
        member_anchors[member] = {
            "blocked_lineages": sorted(fm.b_anchor.blocked_lineages),
            "order_by": fm.order_by,
            "is_monoid": (sig.is_monoid if sig else None),
        }
        reducer_kind[member] = (sig.kind if sig else None)

    base_grain = sorted(m.universes[mc.universe].base_dimensions)
    return {
        "contract_version": CONTRACT_VERSION, "manifold_id": manifold_id, "measure": measure,
        "universe": mc.universe, "dtype": mc.logical_type,
        "family": {"root": mc.name, "members": list(mc.family), "reducer_kind": reducer_kind},
        "member_anchors": member_anchors,
        "v_anchor": {"universe": mc.universe, "grain": base_grain},   # structured, ruling C
        "m_anchor": {"mechanism": mc.missingness, "columns": sorted(mc.m_anchor)},
        "provenance": {"measure": _PROVENANCE.get(mc.evidence, mc.evidence)},
    }


# --- tools 4 & 5 ----------------------------------------------------------------------------
def _build_frame(lm, frameql: str, universe: Optional[str]):
    anchor, columns = parse_frameql(frameql)
    fb = lm.server.frame(*anchor)
    for name, expr in columns:
        fb = fb.column(name, expr)
    if universe:
        fb = fb.on_universe(universe)
    return fb


def _syntax_error_wire(detail: str, universe: Optional[str]) -> dict:
    return {"contract_version": CONTRACT_VERSION, "outcome": "error",
            "frame": {"anchor": [], "universe": universe, "rollup_severity": "none", "disclosures": []},
            "columns": [], "error": {"reason": "frameql_syntax", "detail": detail}}


def query(store: ManifoldStore, manifold_id: str, frameql: str, universe: Optional[str] = None) -> dict:
    lm = _get(store, manifold_id)
    try:
        fb = _build_frame(lm, frameql, universe)
    except FrameQLSyntaxError as e:
        return _syntax_error_wire(str(e), universe)
    fr = fb.run()
    return dw.wire_frame(fr, universe=universe)


def explain(store: ManifoldStore, manifold_id: str, frameql: str, universe: Optional[str] = None) -> dict:
    lm = _get(store, manifold_id)
    try:
        fb = _build_frame(lm, frameql, universe)
    except FrameQLSyntaxError as e:
        return _syntax_error_wire(str(e), universe)
    before = lm.server.fetches
    fr = fb.plan()                       # would-be annotation, zero backend fetches
    delta = lm.server.fetches - before
    return dw.wire_frame(fr, universe=universe, executed=False, fetches_delta=delta)

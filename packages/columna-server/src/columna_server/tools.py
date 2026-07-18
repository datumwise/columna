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

from .frameql import FrameQLSyntaxError
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


def _render_ref(ref, levels=frozenset()) -> str:
    # C-2 insulation (§2b, CP-3): render predicates LOGICALLY — a PHYSICAL table qualifier NEVER
    # crosses describe (the shipped leak was `stores.opened_date`; the standing test bans any table.column).
    # OF-9 (case-demo c): a `<level>.<attr>` reference is a DECLARED LOGICAL attribute — both parts are
    # logical, so it renders WITH its qualifier (`store.opened`). A dotted ref whose head is NOT a declared
    # level is an un-migrated physical residue → drop the qualifier (the shipped guarantee).
    if ref.is_literal:
        return str(ref.value)
    if ref.table is not None and ref.table in levels:
        return f"{ref.table}.{ref.column}"
    return str(ref.column)


def _render_predicate(pred, levels=frozenset()) -> Optional[str]:
    if pred is None or not pred.comparisons:
        return None
    return " AND ".join(f"{_render_ref(c.left, levels)} {c.op} {_render_ref(c.right, levels)}"
                        for c in pred.comparisons)


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
    from columna_core import (describe_derived, describe_universe, describe_assert, describe_hierarchy)
    # C-2 insulation (§2b, CP-3): dimensions no longer emit `realized_by` (a physical identifier).
    # Attributes emit their LOGICAL names only (case-demo c) — the physical binding stays map-side.
    dimensions = [{"level": lv.name, "is_base": lv.is_base, "description": lv.description,
                   "attributes": [a for a, _ in lv.attributes]} for lv in m.levels.values()]
    edges = [{"frm": e.frm, "to": e.to, "lineage": e.lineage} for e in m.edges]
    # C-1 (D1, CP-3): universes carry basis + absence semantics + the basis License (predicate rendered
    # logically); asserts + hierarchies get their own describe blocks with the kernel-reused License.
    _lv = frozenset(m.levels)
    universes = [describe_universe(u, _render_predicate(u.predicate, _lv)) for u in m.universes.values()]
    asserts = [describe_assert(a, _render_predicate(a.predicate, _lv)) for a in m.asserts]
    hierarchies = [describe_hierarchy(h) for h in m.hierarchies]
    # signature addressing (D1): each measure carries its universe qualifier as a STRUCTURED field (a
    # dotted address string would be indistinguishable from a physical `table.column` under the §2b test;
    # the address is (universe, name), and the consumer renders it). Per-member operator props: describe_measure.
    measures = [{"name": mc.name, "family": list(mc.family), "universe": mc.universe,
                 "description": mc.description} for mc in m.measures.values()]
    derived = [describe_derived(m, name) for name in m.derived]
    # published-scope vs cut display (B1): the current serving scope — cut declarations + blocked edges.
    ps = getattr(lm.server, "published_scope", None)
    scope = {"cut": sorted(ps.cut) if ps else [],
             "blocked_edges": [list(e) for e in sorted(ps.blocked_edges)] if ps else [],
             "cut_by": {k: v for k, v in (ps.cut_by.items() if ps else [])},
             "blocked_by": {f"{k[0]}->{k[1]}": v for k, v in (ps.blocked_by.items() if ps else [])}}
    return {"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
            "dimensions": dimensions, "edges": edges, "universes": universes,
            "asserts": asserts, "hierarchies": hierarchies,
            "measures": measures, "derived": derived, "published_scope": scope}


# --- tool 3 ---------------------------------------------------------------------------------
def describe_measure(store: ManifoldStore, manifold_id: str, measure: str) -> dict:
    lm = _get(store, manifold_id)
    m = lm.manifold
    mc = m.measures.get(measure)
    if mc is None:
        raise ToolInputError(f"unknown measure '{measure}' in manifold '{manifold_id}' "
                             f"(have {sorted(m.measures)})")
    ops = lm.server.planner.m.operators   # OperatorSig registry (kind, is_monoid)

    from columna_core import operator_properties
    member_anchors, reducer_kind, signatures = {}, {}, {}
    for member, fm in mc.family.items():
        sig = ops.get(member)
        member_anchors[member] = {
            "blocked_lineages": sorted(fm.b_anchor.blocked_lineages),
            "order_by": fm.order_by,
            "is_monoid": (sig.is_monoid if sig else None),
            "description": fm.description,      # per-member folklore (case-demo b) — LOGICAL, flows to the wire
        }
        reducer_kind[member] = (sig.kind if sig else None)
        # D1 operator properties (registry describe): the algebraic/routing properties, no engine
        # mechanics. Addressing is the STRUCTURED (universe, measure, member) — universe on this dict,
        # measure is `measure`, member is the key — never a dotted string (§2b test would flag it).
        signatures[member] = {"operator": operator_properties(sig)}

    base_grain = sorted(m.universes[mc.universe].base_dimensions)
    return {
        "contract_version": CONTRACT_VERSION, "manifold_id": manifold_id, "measure": measure,
        "description": mc.description,       # measure folklore (case-demo b) — LOGICAL, flows to the wire
        "universe": mc.universe, "dtype": mc.logical_type,
        "family": {"root": mc.name, "members": list(mc.family), "reducer_kind": reducer_kind},
        "member_anchors": member_anchors, "signatures": signatures,
        "v_anchor": {"universe": mc.universe, "grain": base_grain},   # structured, ruling C
        "m_anchor": {"mechanism": mc.missingness, "columns": sorted(mc.m_anchor)},
        "provenance": {"measure": _PROVENANCE.get(mc.evidence, mc.evidence)},
    }


# --- tools 4 & 5 (the ENVELOPE wire) --------------------------------------------------------
def _syntax_error_wire(detail: str, universe: Optional[str]) -> dict:
    return {"contract_version": CONTRACT_VERSION, "outcome": "error",
            "frame": {"anchor": [], "universe": universe, "rollup_severity": "none", "disclosures": []},
            "columns": [], "error": {"reason": "frameql_syntax", "detail": detail}}


def query(store: ManifoldStore, manifold_id: str, frameql: str) -> dict:
    """Execute a FrameQL ENVELOPE statement (`SELECT <series> AT {anchor} [WHERE][HAVING][ORDER BY]
    [LIMIT]`). The terse `cols @ anchor` form is RETIRED from the wire (0.9.0 tombstone). Returns the
    four-mood wire contract."""
    from columna_core.envelope import parse_statement, EnvelopeSyntaxError
    lm = _get(store, manifold_id)
    try:
        stmt = parse_statement(frameql)
        fr = lm.server.planner.run_statement(stmt)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return _syntax_error_wire(str(e), None)
    return dw.wire_frame(fr)


def explain_statement(store: ManifoldStore, manifold_id: str, statement: str) -> dict:
    """EXPLAIN an envelope statement WITHOUT executing: canonical desugared form + atom decomposition +
    dependency cone with verdicts + would-be annotation, zero backend fetches. The rich EXPLAIN payload
    (WP-FrameQL) — distinct from the query wire; a first-class MCP tool beside `query`."""
    from columna_core.envelope import parse_statement, EnvelopeSyntaxError
    lm = _get(store, manifold_id)
    try:
        stmt = parse_statement(statement)
        return lm.server.explain_statement(stmt)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return {"contract_version": CONTRACT_VERSION, "executed": False, "fetches_delta": 0,
                "outcome": "error", "error": {"reason": "frameql_syntax", "detail": str(e)}}

"""
columna_core.documents — the TWO-ARTIFACT projection of a Manifold (case-demo d).

One authored graph, projected into the two documents a data team actually keeps — the same
"two projections of one graph" idea that `projection.py` runs at query time, here at the
AUTHORING/document layer:

  • LOGICAL SPEC  (`logical_spec`)  — the Manifold spec everyone reads. PURELY LOGICAL: measures,
    derived, universes (concept × predicate × basis), levels + their logical attributes,
    hierarchies (lineage + paths), asserts — each with its DESCRIPTION (folklore). It carries NO
    physical identifier and NO reject. This is the blast wall as a document: what an agent or a
    reader sees.

  • PHYSICAL→LOGICAL MAP  (`physical_map`)  — the data team's document, and its shape is MANY-TO-ONE:
    a warehouse accumulates multiple physical incarnations of each concept (copies, denormalizations,
    stale summaries), and the map resolves each many down to ONE authoritative binding, with the
    REJECTS kept on the map, WITH REASONS. Rejects are the author's ATTESTED record — not adjudicated
    — and they live here and ONLY here. They never cross into the logical spec, describe, or the wire.

The wall between the two is the same wall the running system keeps: meaning on one side, plumbing on
the other. `no_physical_leak` makes it checkable — the logical spec, serialized, must contain none of
the physical identifiers the map is built from.
"""
from __future__ import annotations

import json

from .describe import (describe_universe, describe_assert, describe_hierarchy, describe_derived)


# ---- logical predicate rendering (core, self-contained; mirrors the server's insulation) ----------
def render_predicate_logical(pred, levels=frozenset()):
    """Render a universe/assert predicate LOGICALLY. A `<level>.<attr>` reference (a declared logical
    attribute, case-demo c) renders WITH its qualifier — both parts are logical. A dotted ref whose head
    is not a declared level is an un-migrated physical residue → drop the qualifier (the §2b guarantee)."""
    if pred is None or not pred.comparisons:
        return None

    def _ref(r):
        if r.is_literal:
            return str(r.value)
        if r.table is not None and r.table in levels:
            return f"{r.table}.{r.column}"
        return str(r.column)

    return " AND ".join(f"{_ref(c.left)} {c.op} {_ref(c.right)}" for c in pred.comparisons)


# ---- the logical spec (purely logical — the document everyone reads) ------------------------------
def logical_spec(m) -> dict:
    """Project the Manifold as its PURELY-LOGICAL spec: no table, no column, no reject — only meaning
    and folklore. Reuses the describe serializers (the same insulation the Explorer/wire trust)."""
    lv = frozenset(m.levels)
    return {
        "manifold": m.name,
        "version": m.version,
        "universes": [describe_universe(u, render_predicate_logical(u.predicate, lv))
                      for u in m.universes.values()],
        "levels": [{"level": l.name, "is_base": l.is_base, "description": l.description,
                    "attributes": [a for a, _ in l.attributes]}         # LOGICAL names only
                   for l in m.levels.values()],
        "hierarchies": [describe_hierarchy(h) for h in m.hierarchies],
        "measures": [{"name": mc.name, "universe": mc.universe, "family": list(mc.family),
                      "description": mc.description,
                      "members": {mem: fm.description for mem, fm in mc.family.items()}}
                     for mc in m.measures.values()],
        "derived": [describe_derived(m, name) for name in m.derived],
        "asserts": [describe_assert(a, render_predicate_logical(a.predicate, lv)) for a in m.asserts],
    }


# ---- the physical→logical map (many-to-one — the data team's document) ----------------------------
def _measure_realization(mc) -> str:
    """The compact physical realization of a measure: distinct(col) | count(*) | <agg>(<expr>) | <expr>."""
    if mc.distinct_col:
        return f"distinct({mc.distinct_col})"
    if mc.pre_expr == "1":
        return "count(*)"
    if len(mc.family) == 1 and mc.pre_expr:
        return f"{next(iter(mc.family))}({mc.pre_expr})"
    return mc.pre_expr or "—"


def _row(logical, binds_to, rejects=()):
    return {"logical": logical, "binds_to": binds_to,
            "rejects": [[p, r] for p, r in rejects]}


def physical_map(m) -> list:
    """Project the Manifold's PHYSICAL→LOGICAL map (many-to-one): every logical name → its ONE
    authoritative physical binding, with rejected/aside incarnations kept with reasons. This is the
    ONLY artifact that carries physical identifiers and rejects."""
    rows = []

    # universes -> their home table (the modal home_table of the measures bound to them) + rejects
    for u in m.universes.values():
        tables = [mc.home_table for mc in m.measures.values() if mc.universe == u.name]
        binds = max(set(tables), key=tables.count) if tables else "—"
        rows.append(_row(u.name, binds, u.rejects))

    # measures -> their realization + rejected incarnations (the stale summaries)
    for mc in m.measures.values():
        rows.append(_row(mc.name, _measure_realization(mc), mc.rejects))

    # levels: logical attributes -> their physical table.column binding; level rejects (e.g. region)
    #         resolve to the authoritative incoming-edge binding (provider_table.to_col).
    edge_to = {}
    for e in m.edges:
        edge_to.setdefault(e.to, f"{e.provider_table}.{e.to_col}")
    for l in m.levels.values():
        for name, binding in l.attributes:
            rows.append(_row(f"{l.name}.{name}", binding))
        if l.rejects:
            rows.append(_row(l.name, edge_to.get(l.name, "—"), l.rejects))

    # hierarchies -> the VIA tables the lineage's hops traverse
    for h in m.hierarchies:
        vias = []
        for e in m.edges:
            if e.lineage == h.lineage:
                sig = f"{e.provider_table}({e.frm_col}, {e.to_col})"
                if sig not in vias:
                    vias.append(sig)
        rows.append(_row(f"{h.lineage} paths", "; ".join(vias) or "—"))

    return rows


# ---- the wall (checkable) --------------------------------------------------------------------------
def physical_vocabulary(m) -> set:
    """Every physical identifier the map is built from — home tables, pre-exprs, distinct columns,
    attribute bindings, edge provider tables/columns, and every rejected incarnation. The set the
    logical spec must contain NONE of."""
    vocab = set()
    for mc in m.measures.values():
        vocab.add(mc.home_table)
        for p, _ in mc.rejects:
            vocab.add(p)
    for u in m.universes.values():
        for p, _ in u.rejects:
            vocab.add(p)
    for l in m.levels.values():
        for _, binding in l.attributes:
            vocab.add(binding)
        for p, _ in l.rejects:
            vocab.add(p)
    for e in m.edges:
        vocab.add(e.provider_table)
    return {v for v in vocab if v}


def no_physical_leak(m) -> list:
    """Return the physical identifiers (if any) that leaked into the logical spec — empty iff the wall
    holds. The check is structural: serialize the logical spec, look for any physical vocabulary token
    as a qualified `<token>.<x>` or a standalone reject string. Descriptions are prose and exempt (a
    measure may legitimately be described with a word that happens to be a table name); the leak we ban
    is a physical identifier appearing as an IDENTIFIER — a qualified table.column, or a reject reason."""
    import re
    spec = logical_spec(m)
    # strip descriptions/prose before scanning: they are folklore, not identifiers
    def _strip_prose(node):
        if isinstance(node, dict):
            return {k: _strip_prose(v) for k, v in node.items()
                    if k not in ("description", "members", "basis", "absence")}
        if isinstance(node, list):
            return [_strip_prose(x) for x in node]
        return node
    blob = json.dumps(_strip_prose(spec))
    leaks = []
    for tok in physical_vocabulary(m):
        head = tok.split(".", 1)[0]
        if re.search(rf'"[^"]*\b{re.escape(head)}\.[a-z_]+', blob):   # a qualified physical table.column
            leaks.append(tok)
    # no reject reason or reject-physical may appear anywhere in the logical spec
    for coll in (m.measures.values(), m.universes.values(), m.levels.values()):
        for d in coll:
            for p, reason in getattr(d, "rejects", ()):
                if p in blob or reason in blob:
                    leaks.append(p)
    return sorted(set(leaks))

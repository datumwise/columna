#!/usr/bin/env python3
"""MAP-2 · D1 left column — the ATTESTED Polars trace of the eight meaning-nodes.

    python specs/open_planner/map2/trace_nodes.py specs/open_planner/map2/fixtures/

RESEARCH INSTRUMENTATION ONLY. Imports the shipped packages and OBSERVES their execution by wrapping
Polars' own DataFrame/LazyFrame/GroupBy methods for the duration of a run. It edits no engine code,
patches nothing on disk, and restores every wrapper in a `finally`. If deleted, the shipped system is
byte-identical.

WHY THIS EXISTS (charter §3 Q1, §4 D1). The D1 lowering table's left column is "what operations does
the shipped Polars engine actually perform, per node" — and it must be **attested by execution, never
written from memory** (an empty cell is a finding; a guessed cell is a violation). This shim records
every Polars operation the engine issues while serving a curated ask set that exercises all eight
nodes plus the two named compositions, and buckets each operation under the meaning-node whose engine
method issued it (the method->node map is A1 §1.1, pinned to engine.py line numbers).

THE MAP (engine method -> node), from A1 §1.1 (columna-core 0.14.0 source, file:line pinned):
  resolve / _deliver_and_transport_monoid ....... COLUMN delivery + its TRANSPORT/REDUCE
  _transport_reduce / _transport_attach ......... TRANSPORT (climb; dependent 1:1 attach)
  reduce_series / reduce_series_to_anchor ....... REDUCE (collapse to grain)
  _recompute_holistic / _resolve_sketch ......... REDUCE (holistic mule / sketch distinct)
  _confine ...................................... CARVE (WHERE predicate -> filter)
  _resolve_faced/_assign/_alloc/_touch/_serve_driver  CROSS (a declared face of an M:N crossing)
  connector fetch (connector.py) ................ CARVE (universe/population selection — the base scan)
ANCHOR (the output grain), ALIGN (the >1-column full-outer juxtaposition) and DERIVE (arithmetic over
aligned series) are assembled by the PLANNER above the engine's Polars calls; they are attested from
the planner/projection frame that issued the op.
"""
from __future__ import annotations

import json
import pathlib
import sys

import polars as pl

_DF_METHODS = ["group_by", "join", "filter", "select", "with_columns", "rename", "unique",
               "sort", "cast", "drop_nulls", "pivot", "explode"]
_GB_METHODS = ["agg"]

# engine method -> node (A1 §1.1). Longest-match wins; a method not listed is bucketed by file.
_METHOD_NODE = {
    "_confine": "CARVE",
    "resolve": "COLUMN", "_deliver_and_transport_monoid": "COLUMN", "_combine_exprs": "REDUCE",
    "_transport_reduce": "TRANSPORT", "_transport_attach": "TRANSPORT", "_split_dependent_targets": "TRANSPORT",
    "reduce_series": "REDUCE", "reduce_series_to_anchor": "REDUCE",
    "_recompute_holistic": "REDUCE", "_resolve_sketch": "REDUCE", "_build_base_sketches": "REDUCE",
    "_resolve_faced": "CROSS", "_resolve_assign": "CROSS", "_resolve_alloc": "CROSS",
    "_resolve_touch": "CROSS", "_serve_driver": "CROSS", "_touch_disc": "CROSS",
    "_ref_expr": "COLUMN", "_confine_or_scan": "CARVE",
}
_FILE_NODE = {"connector.py": "CARVE", "projection.py": "TRANSPORT"}

# planner assembly is bucketed by (function, op): run does BOTH the ALIGN join and the ORDER sort;
# _apply is DERIVE (the arithmetic over aligned series). ORDER/LIMIT are ENVELOPE clauses, not one of
# the eight IR nodes — tracked separately so they are neither dropped nor miscounted as a ninth node.
_PLANNER_OP_NODE = {
    ("run", "join"): "ALIGN", ("run", "rename"): "ALIGN", ("run", "sort"): "ORDER",
    ("run", "filter"): "ORDER", ("run", "select"): "ALIGN",
    ("_node", "rename"): "ALIGN", ("_node", "select"): "ALIGN",
    ("_apply", "join"): "DERIVE", ("_apply", "with_columns"): "DERIVE",
    ("_apply", "select"): "DERIVE", ("_apply", "rename"): "DERIVE",
}
_ENVELOPE = {"ORDER"}          # known non-node envelope clauses (not eight-node IR, not ninth-node)

TRACE: list = []
_RECORDING = False
_ORIG: dict = {}


def _bucket_from_stack(op):
    """Walk the live stack; return (node, site) from the nearest engine/planner frame that owns a
    method we can name. site is 'file:function'; node is the A1 map's verdict (or an ENVELOPE tag,
    or None -> a ninth-node candidate if it is an unmapped ENGINE op)."""
    import inspect
    for fr in inspect.stack()[2:]:
        fname = fr.filename.rsplit("/", 1)[-1]
        func = fr.function
        if fname == "engine.py":
            if func in _METHOD_NODE:
                return _METHOD_NODE[func], f"engine.py:{func}"
            return None, f"engine.py:{func}"        # unmapped ENGINE op -> genuine ninth-node candidate
        if fname == "connector.py":
            return "CARVE", f"connector.py:{func}"
        if fname in ("planner.py", "projection.py"):
            node = _PLANNER_OP_NODE.get((func, op)) or _METHOD_NODE.get(func) or _FILE_NODE.get(fname)
            return node, f"{fname}:{func}"
    return None, "<outside-engine>"


def _summarize(args):
    """A compact, side-effect-free summary of the interesting positional args (group keys, join keys)."""
    out = []
    for a in args[:2]:
        if isinstance(a, str):
            out.append(a)
        elif isinstance(a, (list, tuple)) and all(isinstance(x, str) for x in a):
            out.append(list(a))
        elif isinstance(a, pl.DataFrame):
            out.append(f"<DF {a.width}c>")
    return out


def _wrap(owner, name):
    orig = getattr(owner, name)
    _ORIG[(owner, name)] = orig

    def wrapper(self, *args, **kwargs):
        if _RECORDING:
            node, site = _bucket_from_stack(name)
            rec = {"op": name, "node": node, "site": site, "args": _summarize(args)}
            if name == "join" and "on" in kwargs:
                rec["args"].append({"on": kwargs["on"]})
            if name == "join" and "how" in kwargs:
                rec["how"] = kwargs["how"]
            TRACE.append(rec)
        return orig(self, *args, **kwargs)

    setattr(owner, name, wrapper)


def _install():
    from polars.dataframe.group_by import GroupBy
    for m in _DF_METHODS:
        if hasattr(pl.DataFrame, m):
            _wrap(pl.DataFrame, m)
    for m in _GB_METHODS:
        if hasattr(GroupBy, m):
            _wrap(GroupBy, m)


def _restore():
    for (owner, name), orig in _ORIG.items():
        setattr(owner, name, orig)
    _ORIG.clear()


# ---- the covering ask set: every node + the two named compositions ------------------------------
# Each entry: (label, nodes-it-is-meant-to-exercise, frameql). All must SERVE/DISCLOSE (verified).
ASKS = [
    ("simple_aggregation", ["ANCHOR", "CARVE", "COLUMN", "REDUCE"],
     "SELECT revenue AT {store}"),
    ("transport_climb", ["ANCHOR", "CARVE", "COLUMN", "TRANSPORT", "REDUCE"],
     "SELECT revenue AT {region}"),
    ("reduce_to_month", ["ANCHOR", "CARVE", "COLUMN", "TRANSPORT", "REDUCE"],
     "SELECT revenue AT {cal.month}"),
    ("cross_touch", ["ANCHOR", "CARVE", "COLUMN", "CROSS", "REDUCE"],
     "SELECT revenue AT {category.touch}"),
    ("cross_alloc", ["ANCHOR", "CARVE", "COLUMN", "CROSS", "REDUCE"],
     "SELECT revenue AT {category.split}"),
    ("align_cross_universe", ["ANCHOR", "CARVE", "COLUMN", "ALIGN", "REDUCE"],
     "SELECT revenue, stock.last AT {store}"),
    ("derive_ratio", ["ANCHOR", "CARVE", "COLUMN", "DERIVE", "REDUCE"],
     "SELECT aov AT {cal.month}"),
    # the two named COMPOSITIONS (charter §4 D1 rows):
    ("COMPOSITION_transport_shaped", ["TRANSPORT", "REDUCE"],
     "SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}"),
    ("COMPOSITION_full_spine", ["CARVE", "COLUMN", "TRANSPORT", "REDUCE"],
     "SELECT revenue AT {region}"),
]


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    outdir = pathlib.Path(argv[1])
    outdir.mkdir(parents=True, exist_ok=True)

    from columna_core import __version__ as core_ver
    from columna_server import tools as T
    from columna_server.demo import demo_store

    store = demo_store()
    engine = store.get("cascadia").server.engine
    per_ask = []
    node_ops: dict = {n: {} for n in ["ANCHOR", "CARVE", "COLUMN", "TRANSPORT", "CROSS",
                                      "REDUCE", "ALIGN", "DERIVE"]}
    envelope_ops: dict = {}
    unmapped: list = []

    global _RECORDING
    _install()
    try:
        for label, meant, q in ASKS:
            engine.cache.clear()               # force COLD execution — a warm cache under-attests ops
            TRACE.clear()
            _RECORDING = True
            try:
                wire = T.query(store, "cascadia", q)
            finally:
                _RECORDING = False
            outcome = wire.get("outcome")
            ops = list(TRACE)
            seen_nodes = {}
            for r in ops:
                node = r["node"]
                if node in _ENVELOPE:          # ORDER/LIMIT — envelope clause, not an IR node
                    envelope_ops[r["op"]] = envelope_ops.get(r["op"], 0) + 1
                    continue
                if node is None:               # an unmapped ENGINE op is a genuine ninth-node candidate
                    unmapped.append({"ask": q, **r})
                    continue
                seen_nodes.setdefault(node, {})
                seen_nodes[node][r["op"]] = seen_nodes[node].get(r["op"], 0) + 1
                node_ops.setdefault(node, {})
                node_ops[node][r["op"]] = node_ops[node].get(r["op"], 0) + 1
            per_ask.append({"label": label, "frameql": q, "outcome": outcome,
                            "meant_to_exercise": meant, "ops_total": len(ops),
                            "ops_by_node": {k: dict(sorted(v.items())) for k, v in seen_nodes.items()},
                            "raw_ops": ops})
            print(f"{outcome:9} | {label:30} | {len(ops):3d} ops | nodes: {sorted(seen_nodes)}")
    finally:
        _restore()

    # ANCHOR is a declaration, not a Polars op; attest it as structural (every ask fixes a grain).
    node_ops["ANCHOR"] = {"(no Polars op — output grain is a declaration, "
                          "materialized as the group keys of the final REDUCE)": len(ASKS)}

    result = {
        "core_version": core_ver,
        "polars_version": pl.__version__,
        "method_node_map": _METHOD_NODE,
        "attestation": "every op below was recorded live from the engine's execution; none written from memory",
        "per_ask": per_ask,
        "node_op_profile": {k: dict(sorted(v.items())) for k, v in node_ops.items()},
        "envelope_ops": dict(sorted(envelope_ops.items())),   # ORDER/LIMIT — not IR nodes
        "unmapped_engine_ops": unmapped,   # unmapped ENGINE ops == genuine ninth-node candidates
        "ninth_node_finding": bool(unmapped),
    }
    (outdir / "d1_polars_trace.json").write_text(json.dumps(result, indent=2, sort_keys=False) + "\n")
    print("\n=== NODE OP PROFILE (attested) ===")
    for n in ["ANCHOR", "CARVE", "COLUMN", "TRANSPORT", "CROSS", "REDUCE", "ALIGN", "DERIVE"]:
        print(f"  {n:10} {dict(sorted(node_ops[n].items())) if n!='ANCHOR' else 'declaration'}")
    print(f"  {'ORDER(env)':10} {dict(sorted(envelope_ops.items()))}")
    print(f"\n  unmapped engine ops (ninth-node candidates): {len(unmapped)}  "
          f"-> {'FINDING' if unmapped else 'CLOSED (eight nodes account for every engine op)'}")
    print(f"  wrote {outdir / 'd1_polars_trace.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

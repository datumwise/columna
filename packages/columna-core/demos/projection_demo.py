"""
projection_demo.py — the two-projection boundary is STRUCTURAL, not conventional.

A Manifold has two projections: the planner gets vocabulary/shape, the engine gets
resolution. This demo proves the planner literally cannot reach provenance — the source
tables, physical columns, pre-aggregation expressions, and universe predicate are simply
absent from the object the planner holds — while it still does real work (static refusals
for fan-out and out-of-universe come from shape alone). The engine, by contrast, has the
full provenance. Disclosures cross the boundary; sources do not.

Run:  python3 projection_demo.py
"""
import sys
from dataclasses import fields, is_dataclass
from columna_core import ManifoldServer, DuckDBConnector
from columna_core.projection import PlannerView
from build_benchmark import load, build_manifold

_P, _F = 0, 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def all_strings(obj, seen=None):
    """Every string reachable from the planner's view (to prove sources are absent)."""
    if seen is None: seen = set()
    out = set()
    if isinstance(obj, str):
        out.add(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            out |= all_strings(k, seen); out |= all_strings(v, seen)
    elif isinstance(obj, (list, tuple, set, frozenset)):
        for x in obj:
            out |= all_strings(x, seen)
    elif is_dataclass(obj):
        for f in fields(obj):
            out |= all_strings(getattr(obj, f.name), seen)
    return out

def main():
    print("="*80)
    print("COLUMNA CORE — the planner/engine provenance boundary is STRUCTURAL")
    print("="*80)
    m = build_manifold()
    pv = PlannerView(m)

    # (1) provenance fields are ABSENT from the planner's measure/universe shapes
    print("\n(1) the planner's view carries vocabulary/shape, never provenance")
    ms = pv.measures["level"]
    check("planner's measure shape has no 'home_table'", not hasattr(ms, "home_table"))
    check("planner's measure shape has no 'pre_expr'",   not hasattr(ms, "pre_expr"))
    check("planner's measure shape has no 'distinct_col'/'missingness'",
          not hasattr(ms, "distinct_col") and not hasattr(ms, "missingness"))
    us = pv.universes["store_days"]
    check("planner's universe shape has no 'predicate' (confinement is engine-only)",
          not hasattr(us, "predicate"))
    check("planner's measure shape keeps vocabulary it DOES need (universe + family names)",
          ms.universe == "store_days" and set(ms.family) == {"sum", "last"})

    # (2) the DAG the planner traverses is topology-only — no physical columns on its edges
    print("\n(2) the planner's transport paths are topology+lineage, with NO physical columns")
    path = pv.find_path(frozenset({"store", "day"}), "region")
    edge = path[1][0]
    check("a shape edge has frm/to/lineage", edge.frm == "store" and edge.to == "region" and edge.lineage)
    check("a shape edge has NO 'frm_col'/'to_col'/'provider_table'",
          not hasattr(edge, "frm_col") and not hasattr(edge, "to_col") and not hasattr(edge, "provider_table"))

    # (3) the planner cannot NAME any source — no table/physical-column/expr strings reachable
    print("\n(3) no source string is reachable from the planner's view")
    strings = all_strings(pv.measures) | all_strings(pv.universes) | all_strings(pv.derived) \
              | all_strings(pv.non_functional) | all_strings(pv._edges)
    # unambiguous provenance: a home table, physical columns, a pre-aggregation expression.
    # (We exclude 'transactions' deliberately — it is a UNIVERSE name the planner legitimately
    # sees as vocabulary; that it also happens to be a table name is a benchmark naming
    # coincidence, not a leak. The planner has no notion a table by that name exists.)
    hidden = {"eom_inventory", "stores", "store_id", "opened_date",
              "customer_id", "TRY_CAST(level AS DOUBLE)"}
    leaked = hidden & strings
    check("source tables / physical columns / pre-exprs are absent from the planner's view",
          not leaked, f"leaked={leaked or 'none'}")
    check("(sanity) the LOGICAL vocabulary the planner needs IS present",
          {"level", "region", "store_days", "sum"} <= strings)

    # (4) the planner still does real work from shape alone — static refusals + resolution
    print("\n(4) from shape alone the planner still refuses statically and resolves the rest")
    con = load()
    srv = ManifoldServer(m, DuckDBConnector(con))
    r_fan = srv.frame("category").column("rev", "revenue").run().columns[0].refusal
    check("fan-out (revenue@category) refused by the planner from topology",
          r_fan is not None and r_fan.reason == "non_functional_transport")
    r_oou = srv.frame("product").column("inv", "level.sum").run().columns[0].refusal
    check("out-of-universe (level@product) refused by the planner from shape",
          r_oou is not None and r_oou.reason == "out_of_universe")
    ok = srv.frame("region").column("rev", "revenue").run()
    check("a faithful frame (revenue@region) still resolves", ok.data is not None and ok.data.height > 0)

    # (5) the complement: the ENGINE side DOES hold provenance
    print("\n(5) the asymmetry — provenance lives on the engine side only")
    check("the engine's Manifold knows level's source table is 'eom_inventory'",
          srv.engine.m.measures["level"].home_table == "eom_inventory")

    # (6) the view carries type/operator VOCABULARY but not the mechanics
    print("\n(6) the view carries type + operator SIGNATURES (vocabulary), not the mechanics")
    check("measure shape carries the declared logical_type (vocabulary)",
          pv.measures["level"].logical_type == "Float64")
    sig = pv.operators["sum"]
    check("operator shape carries the signature (accepts / out_rule)",
          "Float64" in sig.accepts and hasattr(sig, "out_rule"))
    check("operator shape has NO mechanics (deliver_sql / combine / witness)",
          not hasattr(sig, "deliver_sql") and not hasattr(sig, "combine") and not hasattr(sig, "witness"))

    print("\n" + "="*80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("="*80)
    sys.exit(1 if _F else 0)

if __name__ == "__main__":
    main()

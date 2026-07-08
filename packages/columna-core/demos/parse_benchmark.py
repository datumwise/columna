"""
parse_benchmark.py — parse benchmark.cml into a Manifold and run the SAME validation
suite against it. Proves the ingest-first path: a written definition is queryable
end-to-end, identical to the hand-built object.

Run:  python3 parse_benchmark.py
"""
import sys, os
from columna_core import DuckDBConnector, ManifoldServer
from columna_core.parser import parse_file
from build_benchmark import load, run_validations, build_manifold

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    print("="*80)
    print("COLUMNA CORE — ingest-first: parse benchmark.cml, then query the PARSED Manifold")
    print("="*80)
    con = load()

    parsed = parse_file(os.path.join(HERE, "benchmark.cml"))
    print(f"parsed: {len(parsed.universes)} universes, {len(parsed.levels)} levels, "
          f"{len(parsed.edges)} functional edges, {len(parsed.measures)} measures, "
          f"{len(parsed.derived)} derived, {len(parsed.non_functional)} M:N relations")

    # structural parity vs the hand-built Manifold (the parser must reproduce it)
    hand = build_manifold()
    parity = (set(parsed.universes) == set(hand.universes)
              and set(parsed.levels) == set(hand.levels)
              and len(parsed.edges) == len(hand.edges)
              and set(parsed.measures) == set(hand.measures)
              and set(parsed.derived) == set(hand.derived))
    print(f"structural parity with hand-built object: {'YES' if parity else 'NO'}")
    # spot-check the corrected semantics survived the parse
    lvl = parsed.measures["level"]
    print(f"  level.family = {list(lvl.family)}; level.sum blocked lineages = "
          f"{set(lvl.family['sum'].b_anchor.blocked_lineages)}; level missingness = {lvl.missingness}")

    print()
    srv = ManifoldServer(parsed, DuckDBConnector(con))
    failed = run_validations(con, srv)
    sys.exit(1 if (failed or not parity) else 0)

if __name__ == "__main__":
    main()

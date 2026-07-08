"""
smoke_wheel.py — post-build wheel smoke test.

Install the built wheel into a FRESH venv (nothing else on the path), then run this. It exercises a
real connector fetch — `srv.frame(...).run()` → `pl.from_arrow(con.execute(q).arrow())` in
connector.py — through the INSTALLED `columna_core`, so a missing hard runtime dependency (e.g.
pyarrow) fails here rather than silently passing an import-only check. Not collected by pytest;
CI's build job invokes it directly.

Usage (from the repo root, in the fresh venv):
    python packages/columna-core/tests/smoke_wheel.py
"""
import glob
import os
import sys

import duckdb

import columna_core

# Guard: we must be testing the installed wheel, not a src/ checkout shadowing it.
assert "site-packages" in columna_core.__file__, (
    f"expected the installed package, got {columna_core.__file__} — do not put src/ on the path"
)

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEMOS = os.path.join(os.path.dirname(_HERE), "demos")   # the harness (build_manifold) lives here
sys.path.insert(0, _DEMOS)

from build_benchmark import build_manifold          # imported after the demos path insert, by design
from columna_core import DuckDBConnector, ManifoldServer

_MINI = os.path.join(_HERE, "fixtures", "mini_warehouse")


def main():
    con = duckdb.connect()
    for f in sorted(glob.glob(os.path.join(_MINI, "*.parquet"))):
        con.execute(f"CREATE TABLE {os.path.basename(f)[:-8]} AS SELECT * FROM read_parquet('{f}')")

    srv = ManifoldServer(build_manifold(), DuckDBConnector(con))
    # revenue@region transports store->region and fetches via pl.from_arrow — the pyarrow path.
    res = srv.frame("region").column("revenue", "revenue.sum").run()
    rows = list(res.data.iter_rows(named=True))
    assert rows, "revenue@region returned no rows — fetch path did not work"
    assert all(r.get("revenue") is not None for r in rows), "revenue came back null"
    print(f"wheel smoke OK: revenue@region returned {len(rows)} rows via pl.from_arrow "
          f"(columna_core from {columna_core.__file__})")


if __name__ == "__main__":
    main()

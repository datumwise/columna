"""Errata re-measurement: is the fourth-hop decimal collapse keyed on the TYPE or on the VALUE?

ONE QUESTION, DELIBERATELY. The study's §6 collapse point 3 reads "`decimal128(38,0)` at full width
loses digits crossing into Polars while Arrow held it exactly", and `columna-platform`'s admission
CHECK 1 refuses `decimal128(38,0)` AS A TYPE on the strength of it. The measured row behind that
sentence is DuckDB `HUGEINT` -> `decimal128(38,0)` carrying the int128 maximum, which is THIRTY-NINE
digits -- a value out of range for the type it is declared as. Those are two different
discriminators and the original run cannot separate them, because it measured only one value.

This probe separates them. It adds a measurement; it corrects no raw run and replaces no row.

DRIVER LOADING DIFFERS FROM probe_1/probe_2 ON PURPOSE. Those load the DuckDB ADBC driver by
ABSOLUTE PATH to `_duckdb*.so`, which is an environment fact and cannot be pinned. `duckdb`'s own
wheel vendors an `adbc_driver_duckdb` package that resolves the same shared object through
`importlib.util.find_spec`, so the crossing is reachable without a hard-coded path. Same binary,
same entrypoint (`duckdb_adbc_init`); only the way it is located changes.

Reproduce: pip install duckdb==1.5.5 adbc-driver-manager==1.12.0 pyarrow==25.0.1 polars==1.44.2
"""
from __future__ import annotations
import importlib.metadata as md
import platform
import sys
from decimal import Decimal

import polars as pl
import pyarrow as pa
import adbc_driver_duckdb
import adbc_driver_duckdb.dbapi as duck_adbc


def _ver(dist: str) -> str:
    try:
        return md.version(dist)
    except Exception as e:          # noqa: BLE001 -- reporting, not handling
        return f"<{type(e).__name__}>"


print("=== versions, PRINTED rather than remembered (study §2 records these; run 1 and run 2 do not) ===")
print(f"  python                 {sys.version.split()[0]}   {platform.platform()}")
for dist in ("duckdb", "adbc-driver-manager", "pyarrow", "polars"):
    print(f"  {dist:22} {_ver(dist)}")
print(f"  adbc_driver_duckdb     vendored by the duckdb wheel; no distribution of its own")
print(f"  driver shared object   {adbc_driver_duckdb.driver_path()}")

con = duck_adbc.connect()
cur = con.cursor()

print()
print("=== Q. does a decimal128(38,0) lose digits at the fourth hop because of its TYPE? ===")
CASES = [
    ("HUGEINT, 38 nines        (38 digits)", "HUGEINT", "9" * 38),
    ("HUGEINT, int128 max      (39 digits)", "HUGEINT", "170141183460469231731687303715884105727"),
    ("HUGEINT, int128 max - 1  (39 digits)", "HUGEINT", "170141183460469231731687303715884105726"),
    ("HUGEINT, 10^38           (39 digits)", "HUGEINT", "1" + "0" * 38),
    ("DECIMAL(38,0), 38 nines  (38 digits)", "DECIMAL(38,0)", "9" * 38),
]
for label, sql_type, literal in CASES:
    cur.execute(f"SELECT CAST('{literal}' AS {sql_type}) AS v")
    tbl = cur.fetch_arrow_table()
    arrow_type = tbl.schema.field(0).type
    try:
        arrow_value = str(tbl.column(0)[0].as_py())
    except Exception as e:          # noqa: BLE001
        arrow_value = f"<as_py {type(e).__name__}>"
    polars_value = str(pl.from_arrow(tbl)["v"].to_list()[0])
    exact = arrow_value == polars_value == literal
    print(f"  {label}")
    print(f"      arrow  {arrow_type}  ->  {arrow_value}")
    print(f"      polars {'':17}  ->  {polars_value}")
    print(f"      exact across the fourth hop? {'YES' if exact else 'NO   <-- LOSS'}")

print()
print("=== Q. the same fact from the other side: can pyarrow BUILD a 39-digit decimal128(38,0)? ===")
try:
    arr = pa.array([Decimal("1" + "0" * 38)], type=pa.decimal128(38, 0))
    print(f"  built: {arr.type} = {arr[0].as_py()}")
except Exception as e:              # noqa: BLE001
    print(f"  refused: {type(e).__name__}: {str(e)[:100]}")

con.close()
print()
print("done.")

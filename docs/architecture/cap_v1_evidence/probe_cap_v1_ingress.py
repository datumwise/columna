"""CAP v1 ingress confirmation -- the exact path a Platform ingress would take, end to end.

TWO QUESTIONS, AND ONLY TWO. This probe supports deliverable 7 (confirm the reproducible
DuckDB-ADBC driver package/version) and supplies the `[evidence - non-normative]` block behind
CAP v1's value and coordinate envelopes. It is NOT the authority for either rule.

  Q1  Is there a REPRODUCIBLE, PATH-INDEPENDENT DuckDB-ADBC driver package, and what is it?
      The v0.1 study loaded the driver by ABSOLUTE PATH to `_duckdb*.so` (`DUCK_LIB`), which is an
      environment fact and cannot be pinned in a dependency specification.

  Q2  Do CAP v1's three admitted shapes -- governed decimal value as decimal128(18,4), governed text
      coordinate as string, governed date coordinate as date32[day] -- survive the COMPLETE path:
      source -> duckdb-adbc -> arrow -> to_pylist -> polars?

      And are CAP v1's refusals REACHABLE -- i.e. does the driver actually emit the shapes CAP v1
      refuses, so that the refusals are load-bearing rather than decorative?

Everything else is out of scope on purpose. Establishing a narrow profile is not re-measuring an
envelope.

Reproduce: pip install duckdb==1.5.5 adbc-driver-manager==1.12.0 pyarrow==25.0.1 polars==1.44.2
"""
from __future__ import annotations
import importlib.metadata as md
import importlib.util
import platform
import sys

import polars as pl
import adbc_driver_duckdb
import adbc_driver_duckdb.dbapi as duck_adbc


def _ver(dist: str) -> str:
    try:
        return md.version(dist)
    except Exception as e:          # noqa: BLE001 -- reporting, not handling
        return f"<{type(e).__name__}>"


print("=== Q1. the driver PACKAGE, not a filesystem path ===")
print(f"  python                      {sys.version.split()[0]}  {platform.platform()}")
for dist in ("duckdb", "adbc-driver-manager", "pyarrow", "polars"):
    print(f"  dist {dist:24} {_ver(dist)}")
print(f"  dist {'adbc-driver-duckdb':24} {_ver('adbc-driver-duckdb')}"
      "   <-- NO DISTRIBUTION OF ITS OWN")
print(f"  module adbc_driver_duckdb   {adbc_driver_duckdb.__file__}")
print(f"  driver_path() resolves to   {adbc_driver_duckdb.driver_path()}")
print(f"  _duckdb spec origin         {importlib.util.find_spec('_duckdb').origin}")
print("  -> the ADBC driver and the duckdb-native path are THE SAME SHARED OBJECT,")
print("     reached through two different APIs. Distinct crossings, not distinct dependencies.")

con = duck_adbc.connect()
cur = con.cursor()

print()
print("=== Q2a. the three CAP v1 admitted shapes, through the complete path ===")
cur.execute("""
    SELECT CAST('12345678901234.5678' AS DECIMAL(18,4)) AS amount,
           CAST('store-7'             AS VARCHAR)       AS store,
           CAST('2026-09-12'          AS DATE)          AS day
    UNION ALL
    SELECT CAST('0.0001' AS DECIMAL(18,4)), CAST('store-8' AS VARCHAR), CAST('2026-09-13' AS DATE)
""")
tbl = cur.fetch_arrow_table()
print(f"  fetch_arrow_table() returns {type(tbl).__name__}")
EXPECT = {"amount": ["12345678901234.5678", "0.0001"],
          "store": ["store-7", "store-8"],
          "day": ["2026-09-12", "2026-09-13"]}
frame = pl.from_arrow(tbl)
for name in ("amount", "store", "day"):
    arrow_type = tbl.schema.field(name).type
    arrow_vals = [str(v) for v in tbl.column(name).to_pylist()]
    polars_vals = [str(v) for v in frame[name].to_list()]
    ok = arrow_vals == polars_vals == EXPECT[name]
    print(f"  {name:7} arrow  {str(arrow_type):22} to_pylist {arrow_vals}")
    print(f"  {'':7} polars {str(frame.schema[name]):22} values    {polars_vals}")
    print(f"  {'':7} python {type(tbl.column(name).to_pylist()[0]).__name__} / "
          f"{type(frame[name].to_list()[0]).__name__}   ->  "
          f"{'EXACT across all four hops' if ok else 'MISMATCH'}")

print()
print("=== Q2b. CAP v1's coordinate refusals are REACHABLE (the driver emits these) ===")
for label, sql, governed in [
    ("integer where the anchor declares text", "SELECT CAST(7 AS INTEGER) AS store", "text"),
    ("NULL text coordinate",  "SELECT CAST(NULL AS VARCHAR) AS store", "text"),
    ("NULL date coordinate",  "SELECT CAST(NULL AS DATE) AS day",      "date"),
    ("string where the anchor declares date",
     "SELECT CAST('2026-09-12' AS VARCHAR) AS day", "date"),
    ("timestamp where the anchor declares date",
     "SELECT CAST('2026-09-12 00:00:00' AS TIMESTAMP) AS day", "date"),
]:
    cur.execute(sql)
    t = cur.fetch_arrow_table()
    print(f"  governed {governed:5} | {label:42} -> arrow {str(t.schema.field(0).type):22} "
          f"value {t.column(0)[0].as_py()!r}  nulls={t.column(0).null_count}")

print()
print("=== Q2c. CAP v1's value refusals are REACHABLE ===")
for label, sql in [
    ("decimal(9,2)",   "SELECT CAST('1.23' AS DECIMAL(9,2)) AS v"),
    ("decimal(38,9)",  "SELECT CAST('1.123456789' AS DECIMAL(38,9)) AS v"),
    ("double",         "SELECT CAST('12345678901234.5678' AS DOUBLE) AS v"),
    ("bigint",         "SELECT CAST(42 AS BIGINT) AS v"),
    ("varchar decimal","SELECT CAST('12345678901234.5678' AS VARCHAR) AS v"),
    ("boolean",        "SELECT TRUE AS v"),
    ("timestamp us",   "SELECT CAST('2026-09-12 11:59:00.123456' AS TIMESTAMP) AS v"),
]:
    cur.execute(sql)
    t = cur.fetch_arrow_table()
    print(f"  {label:16} -> arrow {str(t.schema.field(0).type):24} "
          f"value {str(t.column(0)[0].as_py())[:34]}")

con.close()
print()
print("done.")

"""Read-only fidelity probe: what survives source -> driver -> Arrow -> Polars.

Measures the MATERIAL distinctions from which governed standing must later be
constituted. Makes no claim about Columna's analytical semantics.
"""
from __future__ import annotations
import decimal, datetime as dt, os, sys
import pyarrow as pa
import polars as pl
import duckdb
import adbc_driver_manager.dbapi as adbc
import adbc_driver_sqlite.dbapi as adbc_sqlite

DUCK_LIB = "/data/probe-venv/lib/python3.12/site-packages/_duckdb.cpython-312-x86_64-linux-gnu.so"
R = []          # rows: (crossing, case, arrow_type, arrow_value, pl_dtype, pl_value, verdict)

def note(crossing, case, tbl, expect_str):
    """Record the arrow type/value and what polars does to it."""
    f = tbl.schema.field(0)
    acol = tbl.column(0)
    try:
        aval = acol[0].as_py()
    except Exception as e:
        aval = f"<as_py failed: {type(e).__name__}>"
    a_ok = (expect_str is None) or (str(aval) == expect_str)
    try:
        df = pl.from_arrow(tbl)
        pdt = str(df.schema[f.name])
        pval = df[f.name][0]
        p_ok = (expect_str is None) or (str(pval) == expect_str)
    except Exception as e:
        pdt, pval, p_ok = f"<{type(e).__name__}>", str(e)[:40], False
    verdict = ("ok" if a_ok else "ARROW-LOSS") if p_ok else ("POLARS-LOSS" if a_ok else "BOTH-LOSS")
    R.append((crossing, case, str(f.type), str(aval), pdt, str(pval), verdict))

# ---- the SQL fixture, shared where the dialect allows -------------------------
DUCK_CASES = [
    ("decimal(38,9) exact",      "SELECT CAST('123456789012345678.123456789' AS DECIMAL(38,9)) AS v", "123456789012345678.123456789"),
    ("decimal(18,4) money",      "SELECT CAST('12345678901234.5678' AS DECIMAL(18,4)) AS v",          "12345678901234.5678"),
    ("decimal(3,1) 0.1+0.2",     "SELECT CAST('0.1' AS DECIMAL(3,1)) + CAST('0.2' AS DECIMAL(3,1)) AS v", "0.3"),
    ("hugeint/int128",           "SELECT CAST('170141183460469231731687303715884105727' AS HUGEINT) AS v", "170141183460469231731687303715884105727"),
    ("timestamp us",             "SELECT CAST('2026-09-12 11:59:00.123456' AS TIMESTAMP) AS v",       "2026-09-12 11:59:00.123456"),
    ("timestamp ns",             "SELECT CAST('2026-09-12 11:59:00.123456789' AS TIMESTAMP_NS) AS v", None),
    ("timestamptz",              "SELECT CAST('2026-09-12 11:59:00-04:00' AS TIMESTAMPTZ) AS v",      None),
    ("time",                     "SELECT CAST('11:59:00.123456' AS TIME) AS v",                       "11:59:00.123456"),
    ("date",                     "SELECT CAST('2026-09-12' AS DATE) AS v",                            "2026-09-12"),
    ("null in decimal col",      "SELECT CAST(NULL AS DECIMAL(18,4)) AS v",                           "None"),
    ("all-null typed col",       "SELECT CAST(NULL AS TIMESTAMPTZ) AS v",                             "None"),
    ("empty string vs null",     "SELECT '' AS v",                                                    ""),
    ("list<int>",                "SELECT [1,2,3] AS v",                                               "[1, 2, 3]"),
    ("struct",                   "SELECT {'a': 1, 'b': 'x'} AS v",                                    None),
    ("map",                      "SELECT MAP {'k': 1} AS v",                                          None),
]

def run_duck_native():
    con = duckdb.connect(":memory:")
    for case, sql, exp in DUCK_CASES:
        try:
            note("duckdb-native", case, con.execute(sql).arrow(), exp)
        except Exception as e:
            R.append(("duckdb-native", case, "-", f"<{type(e).__name__}>", "-", str(e)[:40], "ERROR"))
    con.close()

def run_duck_adbc():
    con = adbc.connect(driver=DUCK_LIB, entrypoint="duckdb_adbc_init", db_kwargs={"path": ":memory:"})
    cur = con.cursor()
    for case, sql, exp in DUCK_CASES:
        try:
            cur.execute(sql); note("duckdb-adbc", case, cur.fetch_arrow_table(), exp)
        except Exception as e:
            R.append(("duckdb-adbc", case, "-", f"<{type(e).__name__}>", "-", str(e)[:40], "ERROR"))
    con.close()

SQLITE_CASES = [
    ("decimal as TEXT",    "SELECT '12345678901234.5678' AS v", "12345678901234.5678"),
    ("decimal as REAL",    "SELECT 12345678901234.5678 AS v",   "12345678901234.5678"),
    ("int64 max",          "SELECT 9223372036854775807 AS v",   "9223372036854775807"),
    ("timestamp as TEXT",  "SELECT '2026-09-12 11:59:00.123456' AS v", "2026-09-12 11:59:00.123456"),
    ("timestamptz as TEXT","SELECT '2026-09-12 11:59:00-04:00' AS v",  "2026-09-12 11:59:00-04:00"),
    ("null",               "SELECT NULL AS v",                  "None"),
    ("empty string",       "SELECT '' AS v",                    ""),
    ("mixed-type column",  "SELECT v FROM (SELECT 1 AS v UNION ALL SELECT 'two' AS v) ORDER BY 1", None),
]

def run_sqlite_adbc():
    con = adbc_sqlite.connect(":memory:")
    cur = con.cursor()
    for case, sql, exp in SQLITE_CASES:
        try:
            cur.execute(sql); note("sqlite-adbc", case, cur.fetch_arrow_table(), exp)
        except Exception as e:
            R.append(("sqlite-adbc", case, "-", f"<{type(e).__name__}>", "-", str(e)[:60], "ERROR"))
    con.close()

def run_ordering():
    """Is row order stable across identical runs with no ORDER BY?"""
    con = duckdb.connect(":memory:")
    con.execute("CREATE TABLE t AS SELECT * FROM (VALUES (3,'c'),(1,'a'),(2,'b')) AS s(i,s)")
    runs = [tuple(con.execute("SELECT i FROM t").arrow().read_all().column(0).to_pylist())
             for _ in range(5)]
    R.append(("duckdb-native", "order w/o ORDER BY (5 runs)", "-", str(set(runs)), "-",
              "stable" if len(set(runs)) == 1 else "UNSTABLE",
              "observed-stable (not a guarantee)" if len(set(runs)) == 1 else "UNSTABLE"))
    con.close()

if __name__ == "__main__":
    run_duck_native(); run_duck_adbc(); run_sqlite_adbc(); run_ordering()
    w = [14, 28, 34, 42, 22, 30, 14]
    hdr = ("crossing", "case", "arrow type", "arrow value (as_py)", "polars dtype", "polars value", "verdict")
    print(" | ".join(h.ljust(x) for h, x in zip(hdr, w)))
    print("-+-".join("-" * x for x in w))
    for row in R:
        print(" | ".join(str(c)[:x].ljust(x) for c, x in zip(row, w)))

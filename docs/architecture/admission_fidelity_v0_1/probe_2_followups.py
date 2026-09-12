"""Follow-ups: the incumbent Columna doorway, and three ambiguous results."""
import decimal
import pyarrow as pa, polars as pl, duckdb
import adbc_driver_manager.dbapi as adbc
import adbc_driver_sqlite.dbapi as adbc_sqlite
DUCK_LIB = "/data/probe-venv/lib/python3.12/site-packages/_duckdb.cpython-312-x86_64-linux-gnu.so"

print("=== A. the INCUMBENT doorway: connector.py does pl.from_arrow(con.execute(q).arrow()) ===")
con = duckdb.connect(":memory:")
res = con.execute("SELECT CAST('12345678901234.5678' AS DECIMAL(18,4)) AS v")
arrow_obj = res.arrow()
print("type of .arrow() in duckdb", duckdb.__version__, "->", type(arrow_obj).__name__)
try:
    df = pl.from_arrow(arrow_obj)
    print("pl.from_arrow(reader) ->", df.schema, "value:", df['v'][0])
except Exception as e:
    print("pl.from_arrow(reader) FAILED:", type(e).__name__, str(e)[:120])
tbl = con.execute("SELECT CAST('12345678901234.5678' AS DECIMAL(18,4)) AS v").arrow().read_all()
print("via read_all(): arrow", tbl.schema.field(0).type, "->", tbl.column(0)[0].as_py())
print("            polars", pl.from_arrow(tbl).schema, pl.from_arrow(tbl)['v'][0])

print()
print("=== B. HUGEINT: real loss or display artifact? ===")
c2 = adbc.connect(driver=DUCK_LIB, entrypoint="duckdb_adbc_init", db_kwargs={"path": ":memory:"})
cur = c2.cursor()
cur.execute("SELECT CAST('170141183460469231731687303715884105727' AS HUGEINT) AS v")
t = cur.fetch_arrow_table()
av = t.column(0)[0].as_py()
pv = pl.from_arrow(t)['v'][0]
print("arrow :", t.schema.field(0).type, repr(av))
print("polars:", pl.from_arrow(t).schema['v'], repr(pv), type(pv).__name__)
print("equal to arrow value?", av == pv, "| exact digits kept?", str(pv) == str(av))

print()
print("=== C. timestamptz: is the SOURCE zone recoverable? ===")
for sql in ["SELECT CAST('2026-09-12 11:59:00-04:00' AS TIMESTAMPTZ) AS v",
            "SET TimeZone='America/New_York'; SELECT CAST('2026-09-12 11:59:00' AS TIMESTAMPTZ) AS v"]:
    cur.execute(sql.split("; ")[-1]) if "; " not in sql else [cur.execute(s) for s in sql.split("; ")]
    t = cur.fetch_arrow_table()
    print(f"  {sql[:58]:58} -> {t.schema.field(0).type} = {t.column(0)[0].as_py()}")

print()
print("=== D. decimal wider than 38 digits ===")
for p, s in [(38, 10), (38, 37)]:
    try:
        cur.execute(f"SELECT CAST('1.{'1'*s}' AS DECIMAL({p},{s})) AS v")
        t = cur.fetch_arrow_table()
        print(f"  DECIMAL({p},{s}) -> {t.schema.field(0).type} = {t.column(0)[0].as_py()}")
    except Exception as e:
        print(f"  DECIMAL({p},{s}) -> refused at source: {type(e).__name__} {str(e)[:70]}")
c2.close()

print()
print("=== E. SQLite dynamic typing: how deep does type inference look? ===")
sc = adbc_sqlite.connect(":memory:"); scur = sc.cursor()
scur.execute("CREATE TABLE t (v)")
scur.execute("INSERT INTO t VALUES (1),(2),(3),('surprise')")
try:
    scur.execute("SELECT v FROM t")
    t = scur.fetch_arrow_table()
    print("  arrow type:", t.schema.field(0).type, "values:", t.column(0).to_pylist())
except Exception as e:
    print("  REFUSED:", type(e).__name__, str(e)[:160])
scur.execute("CREATE TABLE t2 (v)")
scur.execute("INSERT INTO t2 VALUES ('surprise'),(1),(2),(3)")
try:
    scur.execute("SELECT v FROM t2"); t = scur.fetch_arrow_table()
    print("  reversed order -> arrow type:", t.schema.field(0).type, "values:", t.column(0).to_pylist())
except Exception as e:
    print("  reversed order -> REFUSED:", type(e).__name__, str(e)[:160])
sc.close()

print()
print("=== F. null vs NaN in a float column (are they distinguishable?) ===")
con.execute("CREATE TABLE f AS SELECT * FROM (VALUES (CAST(NULL AS DOUBLE)),(CAST('NaN' AS DOUBLE)),(0.0)) AS s(v)")
t = con.execute("SELECT v FROM f").arrow().read_all()
print("  arrow :", t.column(0).to_pylist(), "| null_count =", t.column(0).null_count)
d = pl.from_arrow(t)
print("  polars:", d['v'].to_list(), "| null_count =", d['v'].null_count())
con.close()

"""
test_case_demo_inc2.py — Cascadia increment 2 language/engine additions.

 • the ENGINE resolution of a LOGICAL attribute in a predicate — `day >= store.opened` actually CONFINES
   the population against the physical binding (`stores.opened_date`), carving pre-open snapshots.

The universe ROW-attribute half (`ATTR <names> ON <universe>`) retired in 0.13.0 by cascade: its sole
consumer was the row-form ASSERT (ruling 2026-07-26). The INLINE `LEVEL … ATTR` form below is the
cascade's boundary and did not retire — universe predicates load on it, so it licenses serving.
"""
import duckdb

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.parser import parse_manifold


# ── the engine carve (logical attribute in a predicate confines the population) ───────────────────────
_CARVE = """MANIFOLD t VERSION 1
LEVEL store = store_id BASE ATTR opened = stores.opened_date
LEVEL region = region_id
LEVEL day = day BASE
UNIVERSE inv = store * day WHERE day >= store.opened BASIS spine
HIERARCHY location { store -> region VIA stores(store_id, region_id) }
MEASURE stock ON inv FROM snap VALUE level
    FAMILY { last ORDER day }"""


def test_logical_attribute_predicate_carves_pre_open_snapshots():
    con = duckdb.connect()
    con.execute("CREATE TABLE stores(store_id VARCHAR, region_id VARCHAR, opened_date VARCHAR)")
    con.executemany("INSERT INTO stores VALUES (?,?,?)",
                    [("S1", "R1", "2024-01-10"), ("S2", "R1", "2024-01-01")])
    con.execute("CREATE TABLE snap(store_id VARCHAR, day VARCHAR, level DOUBLE)")
    con.executemany("INSERT INTO snap VALUES (?,?,?)",
                    [("S1", "2024-01-05", 99.0),      # PRE-open (2024-01-05 < S1.opened 2024-01-10) -> carved
                     ("S1", "2024-01-15", 10.0), ("S2", "2024-01-15", 20.0)])
    s = ManifoldServer(parse_manifold(_CARVE), DuckDBConnector(con))
    r = s.frame("store").column("stock", "stock.last").run()
    got = dict(zip(r.data["store"], r.data["stock"]))
    assert got["S1"] == 10.0 and got["S2"] == 20.0   # the 99.0 pre-open snapshot was carved by day >= store.opened

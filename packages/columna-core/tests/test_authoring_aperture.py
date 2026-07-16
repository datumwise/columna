"""
test_authoring_aperture.py — the connector's authoring aperture (catalog / profile / metered sample).

HARNESS behavior only: the call SHAPES and the metering, not any judgment about the data. The aperture
is the two-ends DATA WALL for `columna init` — no method takes SQL, so an exfiltrating read is
structurally impossible; `sample` is capped per call (APERTURE_SAMPLE_CAP).
"""
import duckdb

from columna_core import DuckDBConnector, CatalogAperture, APERTURE_SAMPLE_CAP


def _con():
    con = duckdb.connect()
    con.execute("CREATE TABLE stores AS SELECT * FROM (VALUES (1,'north'),(2,'south'),(3,'north')) t(store_id, region)")
    con.execute("CREATE TABLE tx AS SELECT * FROM (VALUES (1,10.0),(1,20.0),(2,5.0)) t(store_id, amount)")
    return DuckDBConnector(con)


def test_duckdb_connector_satisfies_the_aperture_protocol():
    assert isinstance(_con(), CatalogAperture)


def test_catalog_lists_tables_and_columns():
    cat = {t["table"]: t for t in _con().catalog()}
    assert set(cat) == {"stores", "tx"}
    assert [c["name"] for c in cat["stores"]["columns"]] == ["store_id", "region"]
    assert all("type" in c for c in cat["tx"]["columns"])
    assert "keys" in cat["stores"]                       # best-effort declared keys (empty here)


def test_profile_returns_the_stat_shape():
    p = _con().profile("stores", "region")
    assert set(p) == {"count", "distinct", "nulls", "min", "max"}
    assert p["count"] == 3 and p["distinct"] == 2 and p["nulls"] == 0


def test_sample_is_metered_per_call():
    con = _con()
    assert con.sample("tx", 2).height == 2               # respects the requested n
    assert con.sample("tx", 10_000).height <= APERTURE_SAMPLE_CAP   # …and the per-call cap
    assert con.sample("tx", 10_000).height == 3          # (only 3 rows exist)


def test_aperture_takes_no_sql_only_identifiers():
    # structural: the surface is (table, column, n) — there is no method that accepts a query string,
    # so combination/exfiltration cannot be expressed. (A guard that the shape stays typed.)
    import inspect
    from columna_core import connector as C
    for name in ("catalog", "profile", "sample"):
        params = list(inspect.signature(getattr(C.DuckDBConnector, name)).parameters)
        assert "sql" not in params and "query" not in params

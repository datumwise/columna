"""The first bounded DuckDB-ADBC ingress — material through a real driver, end to end.

THE PROPOSITION, IN ONE SENTENCE: the governed lighthouse revenue case serves the same four exact
decimals it always did, with the carrier now having come through

    DuckDB source -> DuckDB ADBC -> Arrow -> CAP v1 admission -> Platform execution -> public wire

and with admission still refusing everything it refused before.

WHAT THIS IS NOT. It is not a demonstration that DuckDB works. Every negative below DELIVERS —
transport succeeds, Arrow arrives, nothing raises on the way in — and is refused by CAP v1 on the
schema that actually arrived. That is the study's conclusion made executable: SUCCESSFUL TRANSPORT
DOES NOT ESTABLISH ADMISSIBILITY.
"""
from __future__ import annotations

import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pyarrow as pa
import pytest

from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.source import Material, MaterialSource, MaterialBinding, SourceBindings

from columna_adbc import DriverSurfaceUnavailable, DuckDbAdbcSource, driver_surface, projection_sql

sys.path.insert(0, str(Path(__file__).parent))
import lighthouse_duckdb as LH                                                 # noqa: E402

REPO = Path(__file__).resolve().parents[3]
PUBLICATION = REPO / "packages/columna-core/tests/fixtures_v2/lighthouse-v2-publication.json"
MAPPING = REPO / "packages/columna-platform/fixtures/proof_a/private-core-mapping-v2.json"
ASK = "SELECT revenue AT {store*day}"

EXPECTED = {("east", "2026-01-01", "10.0000"), ("east", "2026-01-02", "20.0000"),
            ("west", "2026-01-01", "1.2345"), ("west", "2026-01-02", "3.7037")}


def _mapping_file(tmp_path, mutate=None) -> str:
    doc = json.loads(MAPPING.read_text(encoding="utf-8"))
    if mutate:
        mutate(doc)
    out = tmp_path / "private-core-mapping-v2.json"
    out.write_text(json.dumps(doc), encoding="utf-8")
    return str(out)


def _source(tmp_path, **kw) -> DuckDbAdbcSource:
    return DuckDbAdbcSource(path=LH.build(tmp_path, **kw), name="lighthouse-warehouse")


def _run(tmp_path, *, source=None, mutate=None, connection=LH.CONNECTION):
    src = source if source is not None else _source(tmp_path)
    provider = PlatformExecutionProvider.from_artifact(
        str(PUBLICATION), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=_mapping_file(tmp_path, mutate),
                                 sources=SourceBindings({connection: src})))
    wire = wire_frame(provider.run(parse_statement(ASK)), universe=None, executed=True)
    return wire, src


def _no_result(wire) -> dict:
    return wire["columns"][0]["no_result"]


def _text(wire) -> str:
    """The wire as text, for "no physical identifier crossed" assertions. `default=str` because the
    payload legitimately carries `date` and `Decimal` — which is itself the point of the path."""
    return json.dumps(wire, default=str)


# ══ 1 · the driver surface, resolved through supported APIs ═════════════════════════════════════

def test_the_vendored_surface_resolves_without_a_hard_coded_path():
    s = driver_surface()
    assert s.driver_path and Path(s.driver_path).exists()
    # RESOLVED, NOT REMEMBERED. The probes behind the admission study hard-coded `DUCK_LIB`, an
    # absolute path to `_duckdb*.so`; that is an environment fact and cannot be pinned. Asserted
    # against the source: no absolute path, no interpreter-layout string, anywhere in the package.
    src = Path(__file__).resolve().parents[1] / "src"
    for f in src.rglob("*.py"):
        text = f.read_text(encoding="utf-8")
        for smell in ("site-packages", ".cpython-", "/usr/", "/data/", "lib/python"):
            assert smell not in text, f"{f.name} names a filesystem layout: {smell}"
        assert s.driver_path not in text, f"{f.name} hard-codes the resolved driver path"


def test_the_governing_versions_are_reported_accurately():
    """duckdb==1.5.5 governs the vendored surface; adbc-driver-manager is separately visible."""
    s = driver_surface()
    assert s.duckdb_version == "1.5.5"
    assert s.adbc_manager_version == "1.12.0"


def test_no_independent_duckdb_adbc_driver_version_is_ever_reported():
    """THE FALSE CLAIM THIS PACKAGE IS FORBIDDEN TO MAKE. There is no such distribution."""
    import importlib.metadata as md

    with pytest.raises(md.PackageNotFoundError):
        md.version("adbc-driver-duckdb")
    assert driver_surface().adbc_driver_duckdb_version is None
    assert driver_surface().describe()["adbc-driver-duckdb"] is None


def test_an_unresolvable_surface_fails_closed_at_construction(tmp_path, monkeypatch):
    """A CAPABILITY / SETUP CONDITION, NOT A GOVERNED VERDICT — and raised when the adapter is BUILT,
    so a dependency bump that drops the vendored package fails at startup with a name."""
    import columna_adbc.duckdb_adbc as mod

    monkeypatch.setattr(mod, "VENDORED_ADBC_MODULE", "adbc_driver_that_does_not_exist")
    with pytest.raises(DriverSurfaceUnavailable, match="not importable"):
        mod.driver_surface()
    with pytest.raises(DriverSurfaceUnavailable):
        mod.DuckDbAdbcSource(path=str(tmp_path / "x.duckdb"))


# ══ 2 · ONE projected fetch, generated from realization facts only ══════════════════════════════

def test_the_projection_sql_is_generated_from_realization_facts_and_nothing_else():
    sql = projection_sql("sales", "fact_sale", ["store_code", "sold_on", "amount"])
    assert sql == 'SELECT "store_code", "sold_on", "amount" FROM "sales"."fact_sale"'
    for forbidden in ("*", "WHERE", "GROUP BY", "ORDER BY", "JOIN", "SUM(", "COUNT("):
        assert forbidden not in sql.upper().replace('"', "")
    assert projection_sql(None, "fact_sale", ["a"]) == 'SELECT "a" FROM "fact_sale"'


def test_exactly_one_projected_fetch_is_performed_and_it_names_the_columns(tmp_path):
    wire, src = _run(tmp_path)
    assert wire["outcome"] == "serve"
    assert len(src.fetches) == 1, src.fetches
    schema, table, columns, sql = src.fetches[0]
    assert (schema, table) == ("sales", "fact_sale")
    assert set(columns) == {"store_code", "sold_on", "amount"}
    assert "*" not in sql and "note" not in sql


def test_an_unrequested_source_column_is_irrelevant(tmp_path):
    """`note` exists in the table and is named by no realization; it is never asked for and never
    arrives. Extra source columns are irrelevant BECAUSE THEY WERE NOT REQUESTED."""
    wire, src = _run(tmp_path)
    assert wire["outcome"] == "serve"
    assert "note" not in src.fetches[0][3]
    assert "note" not in _text(wire)


def test_the_adapter_returns_a_materialized_table_not_a_reader(tmp_path):
    """The reader hazard, discharged inside the adapter. A consumed-once object must not reach the
    admission path (admission study [E1]: `.arrow()` returning a RecordBatchReader, fifteen ERRORs)."""
    src = _source(tmp_path)
    m = src.fetch(schema="sales", table="fact_sale", columns=["store_code", "sold_on", "amount"])
    assert isinstance(m, Material)
    assert isinstance(m.table, pa.Table)
    assert m.table.num_rows == 4 and m.table.num_rows == m.table.num_rows   # re-readable


def test_the_adapter_satisfies_the_platform_protocol(tmp_path):
    """STRUCTURAL SUBTYPING, CHECKED. The adapter implements Platform's seam without inheriting from
    anything in Platform — which is what lets the arrow point one way."""
    src = _source(tmp_path)
    assert isinstance(src, MaterialSource)
    assert not isinstance(object(), MaterialSource)          # the check is not vacuous


# ══ 3 · the positive execution case, on the public wire ════════════════════════════════════════

def test_the_governed_revenue_case_serves_through_adbc(tmp_path):
    """THE WHOLE PROPOSITION, as one wire payload."""
    wire, _ = _run(tmp_path)
    assert wire["contract_version"] == "5"
    assert wire["outcome"] == "serve"
    assert wire["executed"] is True
    assert wire["frame"]["anchor"] == ["sale_at"]
    assert wire["columns"][0]["status"] == "served"
    assert wire["columns"][0]["name"] == "revenue"


def test_the_served_rows_carry_the_governed_coordinates_and_exact_decimals(tmp_path):
    wire, _ = _run(tmp_path)
    rows = wire["columns"][0]["values"]
    assert [sorted(r) for r in rows] == [["day", "store", "value"]] * 4
    assert {(r["store"], str(r["day"]), str(r["value"])) for r in rows} == EXPECTED
    assert all(isinstance(r["value"], Decimal) for r in rows)
    assert sum(r["value"] for r in rows) == Decimal("34.9382")


def test_no_physical_identifier_reaches_the_public_wire(tmp_path):
    """The rename is the anchor-component realization's whole job, and this is where it is proved:
    `store_code`, `sold_on`, `amount` and `note` are the SOURCE's vocabulary and the wire is
    governed. If the two were spelled alike, a path that ignored the realization would pass."""
    wire, _ = _run(tmp_path)
    payload = _text(wire)
    for physical in (LH.STORE_COLUMN, LH.DAY_COLUMN, LH.VALUE_COLUMN, "note",
                     "fact_sale", "warehouse.duckdb"):
        assert physical not in payload, physical


def test_data_state_is_none_and_currency_stays_closed(tmp_path):
    """No opaque token is available from this surface as part of THIS observation, and a second
    query to manufacture one would describe a different moment. `None` closes reuse."""
    src = _source(tmp_path)
    m = src.fetch(schema="sales", table="fact_sale", columns=["amount"])
    assert m.data_state is None


def test_the_adbc_result_is_behaviourally_equivalent_to_the_in_memory_slice(tmp_path):
    """THE EQUIVALENCE CLAIM, ASSERTED RATHER THAN HOPED FOR. Same publication, same mapping, same
    ask, same wire — one carrier built in process, one carried through a driver."""
    sys.path.insert(0, str(REPO / "packages/columna-platform/fixtures"))
    import lighthouse_material as M

    in_memory = PlatformExecutionProvider.from_artifact(
        str(PUBLICATION), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=_mapping_file(tmp_path), sources=M.bindings()))
    a = wire_frame(in_memory.run(parse_statement(ASK)), universe=None, executed=True)
    b, _ = _run(tmp_path)
    key = lambda w: (w["contract_version"], w["outcome"], w["executed"], w["frame"]["anchor"],      # noqa: E731
                     sorted((r["store"], str(r["day"]), str(r["value"]))
                            for r in w["columns"][0]["values"]))
    assert key(a) == key(b)


# ══ 4 · CAP v1 decides, not the adapter ════════════════════════════════════════════════════════

def test_a_lossy_double_at_the_source_is_delivered_and_then_refused(tmp_path):
    """THE SOURCE-LOSS NEGATIVE CONTROL. The source stores the governed exact decimal as `DOUBLE`.
    ADBC transports it perfectly; Arrow receives `double`; NOTHING RAISES on the way in. CAP v1
    refuses at the boundary where the loss is still visible.

    This is the whole reason admission exists: if it defaulted to accept, this would be served as if
    it were the governed value."""
    src = _source(tmp_path, value_sql_type="DOUBLE")
    m = src.fetch(schema="sales", table="fact_sale", columns=["amount"])
    assert pa.types.is_floating(m.table.schema.field("amount").type)          # transport SUCCEEDED
    wire, _ = _run(tmp_path, source=src)
    assert wire["outcome"] != "serve"
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "floating-point" in _no_result(wire)["detail"]


@pytest.mark.parametrize("sql_type,arrow_hint", [("DECIMAL(9,2)", "decimal128(9, 2)"),
                                                 ("DECIMAL(38,9)", "decimal128(38, 9)")])
def test_a_decimal_outside_the_cap_v1_envelope_is_refused(tmp_path, sql_type, arrow_hint):
    """CAP v1 admits `decimal128(18,4)` and nothing else. The shape arrives intact and is refused by
    PROFILE CHOICE, not because anything was lost."""
    src = _source(tmp_path, value_sql_type=sql_type)
    m = src.fetch(schema="sales", table="fact_sale", columns=["amount"])
    assert str(m.table.schema.field("amount").type) == arrow_hint
    wire, _ = _run(tmp_path, source=src)
    assert wire["outcome"] != "serve"


def test_a_coordinate_of_the_wrong_type_is_refused(tmp_path):
    """Governed `store: text`; the source stores an INTEGER. Delivered as `int32`, refused by CAP."""
    src = _source(tmp_path, store_sql_type="INTEGER")
    m = src.fetch(schema="sales", table="fact_sale", columns=["store_code"])
    assert str(m.table.schema.field("store_code").type) == "int32"
    wire, _ = _run(tmp_path, source=src)
    assert wire["outcome"] != "serve"
    assert "governed as 'text'" in _no_result(wire)["detail"]


def test_a_null_coordinate_is_refused(tmp_path):
    src = _source(tmp_path, null_store=True)
    wire, _ = _run(tmp_path, source=src)
    assert wire["outcome"] != "serve"
    assert "cannot be partially specified" in _no_result(wire)["detail"]


def test_admission_inspects_the_schema_that_actually_arrived(tmp_path):
    """Not a remembered driver mapping. The same governed claim over two sources differing only in
    the SQL storage type produces serve and refuse — which can only come from the delivered schema."""
    ok, _ = _run(tmp_path, source=_source(tmp_path, filename="ok.duckdb"))
    bad, _ = _run(tmp_path, source=_source(tmp_path, value_sql_type="DOUBLE", filename="bad.duckdb"))
    assert (ok["outcome"], bad["outcome"]) == ("serve", "refuse")


# ══ 5 · realization / source identity — the whole endpoint participates ════════════════════════

def test_changing_only_the_connection_selects_another_binding_or_refuses(tmp_path):
    """R1, through a driver now. The token means whatever the deployment bound it to, and a
    deployment that bound nothing has no material for it."""
    wire, _ = _run(tmp_path, connection="somewhere-else")
    assert wire["outcome"] != "serve"
    assert "no material source is bound to connection 'warehouse'" in _no_result(wire)["detail"]


@pytest.mark.parametrize("field,value", [("schema", "staging"), ("table", "other_fact"),
                                         ("column", "net_amount")])
def test_changing_schema_table_or_column_selects_another_object_or_refuses(tmp_path, field, value):
    """NO DEFAULT IS EVER GUESSED. The adapter does not fall back to another table or column."""
    def mutate(doc):
        for r in doc["realizations"]:
            if r.get("kind") == "family" and r["endpoint"].get("column") == "amount":
                r["endpoint"][field] = value
    wire, _ = _run(tmp_path, mutate=mutate)
    assert wire["outcome"] != "serve"
    assert "values" not in wire["columns"][0]


def test_a_missing_requested_column_refuses_and_never_shortens_the_projection(tmp_path):
    """AT THE ADAPTER: a plain `LookupError`. An adapter has no business choosing a governed
    jurisdiction — it does not know whether the law licensed the ask."""
    src = _source(tmp_path)
    with pytest.raises(LookupError, match="could not read the projection"):
        src.fetch(schema="sales", table="fact_sale", columns=["store_code", "no_such_column"])
    assert len(src.fetches) == 1                       # it asked once and did not retry narrower


def test_a_missing_object_refuses(tmp_path):
    src = _source(tmp_path)
    with pytest.raises(LookupError):
        src.fetch(schema="sales", table="no_such_table", columns=["store_code"])


def test_an_adapter_lookup_failure_reaches_the_wire_in_the_governed_jurisdiction(tmp_path):
    """AT THE SEAM: Platform says WHICH KIND of no it is. Want of STATE — the law licensed the ask
    and the realization named a column this source does not have, which is exactly what
    re-realization resolves. Not a want of law, and not an exception escaping past the server."""
    def mutate(doc):
        for r in doc["realizations"]:
            if r.get("kind") == "family" and r["endpoint"].get("column") == "amount":
                r["endpoint"]["column"] = "net_amount"
    wire, _ = _run(tmp_path, mutate=mutate)
    assert wire["outcome"] == "refuse"
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "could not read the projection" in _no_result(wire)["detail"]


# ══ 6 · isolation — the direction of the arrow, proved ═════════════════════════════════════════

def test_columna_platform_names_no_adbc_or_duckdb_import():
    """STATIC. Platform's own ban is unchanged and is re-asserted from this side of the arrow."""
    src = REPO / "packages/columna-platform/src/columna_platform"
    offenders = []
    for f in sorted(src.rglob("*.py")):
        for line in f.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")) and (
                    "duckdb" in stripped or "adbc" in stripped or "columna_adbc" in stripped):
                offenders.append(f"{f.name}: {stripped}")
    assert not offenders, offenders


def test_platform_loads_neither_driver_in_a_clean_interpreter():
    """AND TRANSITIVELY. A module can name nothing forbidden and still pull the stack in."""
    code = (
        "import sys\n"
        "import columna_platform.serving, columna_platform.source, columna_platform.admission\n"
        "print('DUCKDB', 'duckdb' in sys.modules)\n"
        "print('ADBC', any(m.startswith('adbc') for m in sys.modules))\n"
        "print('ADAPTER', 'columna_adbc' in sys.modules)\n"
        "print('PLANNER', 'columna_core.planner' in sys.modules)\n"
        "print('ENGINE', 'columna_core.engine' in sys.modules)\n"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                         env=_clean_env())
    assert out.returncode == 0, out.stderr
    assert "DUCKDB False" in out.stdout, out.stdout
    assert "ADBC False" in out.stdout, out.stdout
    assert "ADAPTER False" in out.stdout, out.stdout
    assert "PLANNER False" in out.stdout, out.stdout
    assert "ENGINE False" in out.stdout, out.stdout


def test_the_adapter_package_names_no_governed_or_legacy_module():
    """THE BAN IN THE OTHER DIRECTION. An adapter reaching into the planner/engine/compiler would be
    a second execution path. It may import the Platform SEAM it implements, and nothing else."""
    src = Path(__file__).resolve().parents[1] / "src"
    forbidden = ("columna_core.planner", "columna_core.engine", "columna_core.model",
                 "columna_core.compiler")
    for f in sorted(src.rglob("*.py")):
        text = f.read_text(encoding="utf-8")
        for bad in forbidden:
            assert bad not in text, f"{f.name} reaches for {bad}"


def test_no_cml_is_consulted_on_the_adbc_path(tmp_path):
    wire, _ = _run(tmp_path)
    assert wire["outcome"] == "serve"
    assert ".cml" not in _text(wire)


def _clean_env():
    import os

    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([
        str(REPO / "packages/columna-core/src"),
        str(REPO / "packages/columna-platform/src"),
    ])
    return env

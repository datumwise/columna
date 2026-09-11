"""
test_producer_artifact_v2.py — the producer→consumer loop, closed on committed bytes.

`lighthouse-v2-publication.json` is emitted by `manifold-agent`'s
`tests/produce_lighthouse_v2.py` and committed here. The two packages are IMPORT-DISJOINT: this
package never imports `manifold_agent`, and `manifold_agent` never imports this one. **The artifact
is the only thing that crosses.** So if these bytes parse, resolve, compile and serve, the boundary
carries the meaning — which is the claim the format exists to make.

The same relationship the v1 fixture already had, with the defect removed: under v1 these bytes
would not have determined their own meaning, because which family member each declaration named
lived in a private realization mapping.
"""
from __future__ import annotations

import json
import pathlib

import pytest

from columna_core.compiler.compile_v2 import compile_v2
from columna_core.compiler.realization import parse_mapping
from columna_core.governed import parse_publication, resolve_all
from columna_core.governed.resolve import C3_DOMAIN_MOVEMENT, UNESTABLISHED

ARTIFACT = pathlib.Path(__file__).parent / "fixtures_v2" / "lighthouse-v2-publication.json"
ROWS = [("s1", "2026-08-01", 10.0), ("s1", "2026-08-02", 3.0), ("s1", "2026-08-03", 7.0),
        ("s2", "2026-08-01", 5.0), ("s2", "2026-08-02", 40.0), ("s2", "2026-08-03", 20.0)]


@pytest.fixture(scope="module")
def publication():
    return parse_publication(json.loads(ARTIFACT.read_text(encoding="utf-8")))


def _mapping(pub):
    fid = {f.canonical_reference: f.family_id for f in pub.families}

    def ep(column):
        return {"connection": "warehouse", "schema": "main", "table": "sales_lines",
                "column": column}
    return parse_mapping({
        "mapping_format_version": "2",
        "publication_ref": {"manifold_id": pub.ref.manifold_id, "version": pub.ref.version},
        "realizations": [
            {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "store",
             "endpoint": ep("store_id")},
            {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "day",
             "endpoint": ep("sale_date")},
            {"kind": "family", "family_id": fid["revenue"], "endpoint": ep("amount"),
             "grain": "coincident", "continuation_operator": "sum"},
            {"kind": "family", "family_id": fid["count(revenue@sale_at)"], "endpoint": ep("amount"),
             "grain": "coincident", "formation_operator": "count"},
            {"kind": "family", "family_id": fid["min(revenue@sale_at)"], "endpoint": ep("amount"),
             "grain": "coincident", "formation_operator": "min"},
            {"kind": "family", "family_id": fid["max(revenue@sale_at)"], "endpoint": ep("amount"),
             "grain": "coincident", "formation_operator": "max"},
        ]})


def test_the_consumer_does_not_import_the_producer():
    import sys
    assert "manifold_agent" not in sys.modules, (
        "the artifact is the only thing that may cross this boundary")


def test_the_producer_artifact_is_format_v2_and_carries_its_authority(publication):
    assert publication.format_version == "2"
    assert len(publication.families) == 4
    assert set(publication.constitution_authority) == {f.family_id for f in publication.families}
    for record in publication.constitution_authority.values():
        assert record.fingerprint_scheme == "fcf-1", (
            "family constitution authority must not share a scheme with the universe's elf-1 "
            "existence-law ratification; the two attest different objects")
        assert record.established_by and record.at


def test_family_ids_are_opaque_and_carry_no_meaning(publication):
    for fam in publication.families:
        assert fam.family_id.startswith("fam_")
        for leak in ("revenue", "sum", "count", "min", "max", "sales", "sale_at", "amount"):
            assert leak not in fam.family_id.lower(), (
                f"{fam.family_id} leaks {leak!r}: identity must not be derived from a canonical "
                f"name, a foundation-law spelling, a legacy member name, or a realization")


def test_every_produced_family_resolves_valid(publication):
    for view in resolve_all(publication).values():
        assert view.valid, (view.canonical_reference, view.validity_problems)


def test_the_produced_artifact_says_unestablished_rather_than_implying_permission(publication):
    """Nothing declares a movement, so nothing may travel — and the artifact says so rather than
    leaving a reader to infer additivity from a missing record."""
    for view in resolve_all(publication).values():
        assert view.standing(C3_DOMAIN_MOVEMENT) == UNESTABLISHED


def test_the_produced_artifact_compiles(publication):
    image = compile_v2(publication, _mapping(publication))
    assert "MEASURE revenue ON sales FROM sales_lines TYPE Float64 VALUE amount" in image.text
    for member in ("count", "max", "min", "sum"):
        assert f"        {member}" in image.text


def test_the_produced_artifact_serves_the_numbers_its_law_describes(publication, tmp_path):
    import duckdb

    from columna_core import DuckDBConnector, ManifoldServer
    from columna_core.parser import parse_manifold

    con = duckdb.connect(str(tmp_path / "lighthouse.duckdb"))
    con.execute("CREATE SCHEMA IF NOT EXISTS main")
    con.execute("CREATE TABLE main.sales_lines (store_id VARCHAR, sale_date DATE, amount DOUBLE)")
    con.executemany("INSERT INTO main.sales_lines VALUES (?, ?, ?)", ROWS)

    image = compile_v2(publication, _mapping(publication))
    srv = ManifoldServer(parse_manifold(image.text), DuckDBConnector(con))
    srv.publish()
    fr = (srv.frame("store")
          .column("total", "revenue.sum").column("n", "revenue.count")
          .column("lo", "revenue.min").column("hi", "revenue.max").run())
    got = {r["store"]: r for r in fr.data.sort("store").iter_rows(named=True)}

    expected = {}
    for store, _day, amount in ROWS:
        e = expected.setdefault(store, {"total": 0.0, "n": 0, "lo": amount, "hi": amount})
        e["total"] += amount
        e["n"] += 1
        e["lo"] = min(e["lo"], amount)
        e["hi"] = max(e["hi"], amount)
    for store, e in expected.items():
        assert got[store]["total"] == pytest.approx(e["total"])
        assert got[store]["n"] == e["n"]
        assert got[store]["lo"] == pytest.approx(e["lo"])
        assert got[store]["hi"] == pytest.approx(e["hi"])

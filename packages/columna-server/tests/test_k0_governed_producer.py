"""
test_k0_governed_producer — the end-to-end proof the receipt work could not yet have.

`columna-server` 0.9.0 shipped the receipt ADMISSION contract and said so plainly: its receipts were
test-constructed, and therefore "not an end-to-end governed-producer proof". This module closes that
residual. A real compiler now produces the artifact-image binding, and the real store admits it.

The compiler is imported from `columna_core.compiler`. That direction is the allowed one —
`columna-server` depends on `columna-core` — and it is only a TEST dependency: the server's own
admission path never imports the compiler, never loads the private mapping, and never re-runs
lowering. Nothing here weakens that.
"""
import json
import os

import duckdb
import pytest

from columna_core.compiler import (
    build_receipt,
    compile_k0,
    parse_mapping,
    parse_publication,
    render_receipt,
)
from columna_server.lowering_receipt import LOWERING_RECEIPT
from columna_server.store import ENTRY_GOVERNED, ManifoldStore

# ── the governed inputs ──────────────────────────────────────────────────────────────────────────
PUB = {
    "publication_format_version": "1",
    "ref": {"manifold_id": "retail", "version": "1.3.0"},
    "logical": {"declarations": [
        {"kind": "anchor", "name": "sale_at", "body": {"components": [
            {"name": "store", "type": "text"}, {"name": "day", "type": "date"}]}},
        {"kind": "universe", "name": "sales", "body": {"anchor": "sale_at", "basis": "events"}},
        {"kind": "measure", "name": "revenue",
         "body": {"value_type": "decimal", "root_member": "revenue_sum"}},
        {"kind": "member", "name": "revenue_sum",
         "body": {"measure": "revenue", "anchor": "sale_at", "universe": "sales"}},
        {"kind": "member", "name": "revenue_max",
         "body": {"measure": "revenue", "anchor": "sale_at", "universe": "sales"}},
    ]},
    "authority": {
        "published_by": "Huayin", "published_at": "2026-08-22T00:00:00Z",
        "ratifications": {"sales": {"ratified_by": "Huayin", "at": "2026-08-22T00:00:00Z",
                                    "fingerprint": "fp-sales", "fingerprint_version": "elf-1"}},
    },
}

_EP = {"connection": "wh", "schema": "main", "table": "sales_lines"}
MAP = {
    "mapping_format_version": "1",
    "publication_ref": {"manifold_id": "retail", "version": "1.3.0"},
    "realizations": [
        {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "store",
         "endpoint": dict(_EP, column="store_id")},
        {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "day",
         "endpoint": dict(_EP, column="sale_date")},
        {"kind": "member", "measure_ref": "revenue", "member_ref": "revenue_sum",
         "universe_ref": "sales", "anchor_ref": "sale_at", "root_evaluator": "sum",
         "endpoint": dict(_EP, column="amount")},
        {"kind": "member", "measure_ref": "revenue", "member_ref": "revenue_max",
         "universe_ref": "sales", "anchor_ref": "sale_at", "root_evaluator": "max",
         "endpoint": dict(_EP, column="amount")},
    ],
}

ROWS = [("s1", "d1", 10.0), ("s1", "d2", 3.0), ("s1", "d3", 7.0),
        ("s2", "d1", 5.0), ("s2", "d2", 40.0), ("s2", "d3", 20.0)]


def _warehouse(path) -> str:
    """A parquet warehouse whose column names are the PHYSICAL ones the mapping resolves to."""
    os.makedirs(path, exist_ok=True)
    con = duckdb.connect()
    con.execute("CREATE TABLE sales_lines (store_id VARCHAR, sale_date VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO sales_lines VALUES (?,?,?)", ROWS)
    con.execute(f"COPY sales_lines TO '{os.path.join(path, 'sales_lines.parquet')}' (FORMAT PARQUET)")
    con.close()
    return path


def _unit(tmp_path, folder="retail"):
    """Compile, then provision the four-file runtime unit exactly as the contract specifies.

    Order matters and is the point: the receipt digests the artifact and the image AS SHIPPED, so it
    can only be written after both files exist, and any later edit to either invalidates it."""
    wh = _warehouse(str(tmp_path / "warehouse"))
    d = tmp_path / folder
    d.mkdir()

    image = compile_k0(parse_publication(PUB), parse_mapping(MAP))

    pub_bytes = json.dumps(PUB, sort_keys=True, separators=(",", ":")).encode("utf-8")
    (d / "governed-publication.json").write_bytes(pub_bytes)
    (d / "manifold.cml").write_bytes(image.encode())
    receipt = build_receipt(
        manifold_id=image.manifold_id, version=image.version,
        publication_bytes=pub_bytes, image_bytes=image.encode(),
        compiler_name="columna-core-p1-k0", compiler_version="0.1.0",
        mapping_provenance={"mapping_format_version": MAP["mapping_format_version"]},
        established_at="2026-08-22T00:00:00Z")
    (d / LOWERING_RECEIPT).write_text(render_receipt(receipt), encoding="utf-8")
    (d / "data.toml").write_text(
        f'[manifold]\nname = "{folder}"\n[connector]\ntype = "duckdb"\nwarehouse = "{wh}"\n')
    return d, image


# ── the headline: a compiler-produced unit is admitted as GOVERNED ───────────────────────────────
def test_a_compiled_unit_is_admitted_as_governed_with_no_conditions(tmp_path):
    _unit(tmp_path)
    store = ManifoldStore(str(tmp_path))
    assert [c.kind for c in store.conditions()] == []
    assert store.get("retail").entry_kind == ENTRY_GOVERNED


def test_the_governed_meaning_still_comes_only_from_the_artifact(tmp_path):
    _unit(tmp_path)
    lm = ManifoldStore(str(tmp_path)).get("retail")
    assert lm.publication.ref.manifold_id == "retail"
    assert lm.publication.ref.version == "1.3.0"


# ── it does not merely load: it serves, correctly ────────────────────────────────────────────────
def _ask(store, statement):
    from columna_core.disclosure_wire import wire_frame
    from columna_core.envelope import parse_statement
    lm = store.get("retail")
    return wire_frame(lm.provider.runtime.planner.run_statement(parse_statement(statement)))["columns"][0]


@pytest.mark.parametrize("member,expected", [
    ("sum", {"s1": 20.0, "s2": 65.0}),
    ("max", {"s1": 10.0, "s2": 40.0}),
])
def test_the_compiled_image_serves_correct_numbers(tmp_path, member, expected):
    """Rolled up to `{store}` — a subset of the product anchor — so the monoid combine runs."""
    _unit(tmp_path)
    col = _ask(ManifoldStore(str(tmp_path)), f"SELECT revenue.{member} AT {{store}}")
    assert col["status"] == "served", col.get("no_result")
    assert {r["store"]: r["value"] for r in col["values"]} == expected


def test_a_receipt_implies_no_certification(tmp_path):
    """Governed standing is publication->image, and nothing more. The compiled unit exercises the
    kernel while its certification sets stay empty — a lowering receipt is not certification."""
    _unit(tmp_path)
    lm = ManifoldStore(str(tmp_path)).get("retail")
    scope = lm.provider.runtime.published_scope
    assert not scope.certified_edges
    assert not scope.certified_faces
    assert _ask(ManifoldStore(str(tmp_path)), "SELECT revenue.sum AT {store}")["status"] == "served"


# ── the binding is load-bearing, not decorative ──────────────────────────────────────────────────
def test_editing_the_image_after_provisioning_breaks_the_binding(tmp_path):
    d, _ = _unit(tmp_path)
    cml = d / "manifold.cml"
    cml.write_text(cml.read_text() + "\n# an in-place edit on a running host\n", encoding="utf-8")
    store = ManifoldStore(str(tmp_path))
    assert {c.kind for c in store.conditions()} == {"LoweringReceiptMismatch"}
    assert store.get("retail").entry_kind != ENTRY_GOVERNED


def test_a_hand_written_source_claim_without_a_receipt_is_not_governed(tmp_path):
    d, _ = _unit(tmp_path)
    os.remove(d / LOWERING_RECEIPT)
    store = ManifoldStore(str(tmp_path))
    assert {c.kind for c in store.conditions()} == {"LoweringReceiptMissing"}
    assert store.get("retail").entry_kind != ENTRY_GOVERNED


def test_the_same_image_paired_with_another_publication_is_refused(tmp_path):
    d, _ = _unit(tmp_path)
    other = json.loads((d / "governed-publication.json").read_text())
    other["ref"]["version"] = "1.4.0"
    (d / "governed-publication.json").write_text(
        json.dumps(other, sort_keys=True, separators=(",", ":")))
    store = ManifoldStore(str(tmp_path))
    assert store.get("retail").entry_kind != ENTRY_GOVERNED


# ── the compiler's determinism is what makes provisioning reproducible ───────────────────────────
def test_recompiling_reproduces_the_identical_runtime_image(tmp_path):
    d, image = _unit(tmp_path)
    again = compile_k0(parse_publication(PUB), parse_mapping(MAP))
    assert again.encode() == image.encode()
    assert (d / "manifold.cml").read_bytes() == again.encode()

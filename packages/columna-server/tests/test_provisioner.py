"""
test_provisioner — milestone 6. The provisioner is an ASSEMBLER, and these tests say so twice:
once by proving a real unit provisions and serves, and once by proving every way of pairing the
wrong bytes refuses instead of being made to agree.

The K0 compiler produces the inputs, so this is the real pipeline end to end —
compile -> provision -> admit — not three fixtures that happen to be consistent.
"""
import hashlib
import json
import os
import shutil

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
from columna_server.provision import (
    CATEGORIES,
    DestinationNotEmpty,
    DigestMismatch,
    IdentityDisagreement,
    MalformedInput,
    MissingInput,
    ProvisionRefusal,
    RUNTIME_FILES,
    provision_runtime_unit,
)
from columna_server.store import ENTRY_GOVERNED, ENTRY_LEGACY, ManifoldStore

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEMOS = os.path.join(os.path.dirname(_HERE), "src", "columna_server", "demo")


def _publication(version="1.3.0", measure="revenue"):
    return {
        "publication_format_version": "1",
        "ref": {"manifold_id": "retail", "version": version},
        "logical": {"declarations": [
            {"kind": "anchor", "name": "sale_at", "body": {"components": [
                {"name": "store", "type": "text"}, {"name": "day", "type": "date"}]}},
            {"kind": "universe", "name": "sales", "body": {"anchor": "sale_at", "basis": "events"}},
            {"kind": "measure", "name": measure,
             "body": {"value_type": "decimal", "root_member": f"{measure}_sum"}},
            {"kind": "member", "name": f"{measure}_sum",
             "body": {"measure": measure, "anchor": "sale_at", "universe": "sales"}},
        ]},
        "authority": {
            "published_by": "Huayin", "published_at": "2026-08-22T00:00:00Z",
            "ratifications": {"sales": {"ratified_by": "Huayin", "at": "2026-08-22T00:00:00Z",
                                        "fingerprint": "fp-sales", "fingerprint_version": "elf-1"}},
        },
    }


def _mapping(version="1.3.0", measure="revenue"):
    ep = {"connection": "wh", "schema": "main", "table": "sales_lines"}
    return {
        "mapping_format_version": "1",
        "publication_ref": {"manifold_id": "retail", "version": version},
        "realizations": [
            {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "store",
             "endpoint": dict(ep, column="store_id")},
            {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "day",
             "endpoint": dict(ep, column="sale_date")},
            {"kind": "member", "measure_ref": measure, "member_ref": f"{measure}_sum",
             "universe_ref": "sales", "anchor_ref": "sale_at", "root_evaluator": "sum",
             "endpoint": dict(ep, column="amount")},
        ],
    }


ROWS = [("s1", "d1", 10.0), ("s1", "d2", 3.0), ("s2", "d1", 5.0), ("s2", "d2", 40.0)]


def _warehouse(path):
    os.makedirs(path, exist_ok=True)
    con = duckdb.connect()
    con.execute("CREATE TABLE sales_lines (store_id VARCHAR, sale_date VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO sales_lines VALUES (?,?,?)", ROWS)
    con.execute(f"COPY sales_lines TO '{os.path.join(path, 'sales_lines.parquet')}' (FORMAT PARQUET)")
    con.close()
    return path


def _artifacts(tmp_path, name="build", version="1.3.0", measure="revenue"):
    """Produce the three artifacts with the REAL compiler, in a staging dir separate from any
    runtime unit — the shape a provisioner actually meets."""
    pub, mapping = _publication(version, measure), _mapping(version, measure)
    image = compile_k0(parse_publication(pub), parse_mapping(mapping))

    out = tmp_path / name
    out.mkdir(parents=True, exist_ok=True)
    pub_bytes = json.dumps(pub, sort_keys=True, separators=(",", ":")).encode("utf-8")
    (out / "governed-publication.json").write_bytes(pub_bytes)
    (out / "manifold.cml").write_bytes(image.encode())
    receipt = build_receipt(manifold_id=image.manifold_id, version=image.version,
                            publication_bytes=pub_bytes, image_bytes=image.encode(),
                            compiler_name="columna-core-p1-k0", compiler_version="0.16.0",
                            established_at="2026-08-22T00:00:00Z")
    (out / LOWERING_RECEIPT).write_text(render_receipt(receipt), encoding="utf-8")
    return out


def _toml(warehouse, name="retail"):
    return (f'[manifold]\nname = "{name}"\n[connector]\ntype = "duckdb"\n'
            f'warehouse = "{warehouse}"\n')


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _provision(tmp_path, src=None, dest_name="retail", **over):
    src = src or _artifacts(tmp_path)
    wh = _warehouse(str(tmp_path / "warehouse"))
    kw = dict(publication=str(src / "governed-publication.json"),
              image=str(src / "manifold.cml"),
              receipt=str(src / LOWERING_RECEIPT),
              data_toml=_toml(wh))
    kw.update(over)
    return provision_runtime_unit(str(tmp_path / "runtime" / dest_name), **kw), src


# ── 1. the happy path ────────────────────────────────────────────────────────────────────────────
def test_a_compiled_unit_provisions(tmp_path):
    unit, _ = _provision(tmp_path)
    assert sorted(os.listdir(unit.path)) == sorted(RUNTIME_FILES)
    assert (unit.ref.manifold_id, unit.ref.version) == ("retail", "1.3.0")


# ── 2. and the server admits it ──────────────────────────────────────────────────────────────────
def test_the_provisioned_unit_is_admitted_as_governed(tmp_path):
    _provision(tmp_path)
    store = ManifoldStore(str(tmp_path / "runtime"))
    assert [c.kind for c in store.conditions()] == []
    assert store.get("retail").entry_kind == ENTRY_GOVERNED


def test_the_provisioned_unit_serves(tmp_path):
    """Assembly that produces a folder the server rejects is not assembly."""
    from columna_core.disclosure_wire import wire_frame
    from columna_core.envelope import parse_statement

    _provision(tmp_path)
    lm = ManifoldStore(str(tmp_path / "runtime")).get("retail")
    col = wire_frame(lm.provider.runtime.planner.run_statement(
        parse_statement("SELECT revenue.sum AT {store}")))["columns"][0]
    assert col["status"] == "served", col.get("no_result")
    assert {r["store"]: r["value"] for r in col["values"]} == {"s1": 13.0, "s2": 45.0}


# ── 3, 4, 5. bytes in == bytes out ───────────────────────────────────────────────────────────────
@pytest.mark.parametrize("name", ["governed-publication.json", "manifold.cml", LOWERING_RECEIPT])
def test_bytes_are_copied_not_re_emitted(tmp_path, name):
    """The receipt binds bytes AS SHIPPED with no canonicalization, so an equivalent re-serialization
    is still a different file. This is the invariant the whole module exists to keep."""
    unit, src = _provision(tmp_path)
    assert _sha(os.path.join(unit.path, name)) == _sha(str(src / name))
    assert open(os.path.join(unit.path, name), "rb").read() == open(str(src / name), "rb").read()


def test_the_binding_still_describes_its_own_files_after_provisioning(tmp_path):
    unit, _ = _provision(tmp_path)
    receipt = json.loads(open(os.path.join(unit.path, LOWERING_RECEIPT), "rb").read())
    assert receipt["publication_digest"] == "sha256:" + _sha(
        os.path.join(unit.path, "governed-publication.json"))
    assert receipt["image_digest"] == "sha256:" + _sha(os.path.join(unit.path, "manifold.cml"))


# ── 6, 7. unrelated artifacts are never silently paired ──────────────────────────────────────────
def test_a_different_publication_with_a_valid_image_and_receipt_refuses(tmp_path):
    src = _artifacts(tmp_path, "build")
    other = _artifacts(tmp_path, "other", version="1.4.0")
    with pytest.raises(IdentityDisagreement) as e:
        _provision(tmp_path, src=src, publication=str(other / "governed-publication.json"))
    assert "1.4.0" in str(e.value) and "1.3.0" in str(e.value)


def test_a_different_image_with_a_valid_publication_and_receipt_refuses(tmp_path):
    src = _artifacts(tmp_path, "build")
    other = _artifacts(tmp_path, "other", version="1.4.0")
    with pytest.raises(IdentityDisagreement):
        _provision(tmp_path, src=src, image=str(other / "manifold.cml"))


def test_a_same_ref_image_of_different_content_refuses_on_digest(tmp_path):
    """The subtle one: same publication ref, genuinely different image. Identity agrees, so only the
    digest can catch it — which is why the digest check is not redundant with the ref check."""
    src = _artifacts(tmp_path, "build")
    other = _artifacts(tmp_path, "other", measure="margin")
    with pytest.raises(DigestMismatch) as e:
        _provision(tmp_path, src=src, image=str(other / "manifold.cml"))
    assert "manifold.cml" in str(e.value)


# ── 8, 9. tampering ──────────────────────────────────────────────────────────────────────────────
def test_a_tampered_publication_refuses(tmp_path):
    src = _artifacts(tmp_path)
    p = src / "governed-publication.json"
    p.write_bytes(p.read_bytes().replace(b'"published_by":"Huayin"', b'"published_by":"someone"'))
    with pytest.raises(DigestMismatch) as e:
        _provision(tmp_path, src=src)
    assert "governed-publication.json" in str(e.value)


def test_a_whitespace_only_edit_to_the_publication_still_refuses(tmp_path):
    """Byte digests, not canonical form: a semantically identical reformat IS a change to the file,
    and the refusal is reporting the truth."""
    src = _artifacts(tmp_path)
    p = src / "governed-publication.json"
    p.write_bytes(json.dumps(json.loads(p.read_bytes()), indent=2).encode())
    with pytest.raises(DigestMismatch):
        _provision(tmp_path, src=src)


def test_a_tampered_image_refuses(tmp_path):
    src = _artifacts(tmp_path)
    p = src / "manifold.cml"
    p.write_bytes(p.read_bytes() + b"\n# an extra line\n")
    with pytest.raises(DigestMismatch) as e:
        _provision(tmp_path, src=src)
    assert "manifold.cml" in str(e.value)


# ── 10. missing inputs ───────────────────────────────────────────────────────────────────────────
def test_a_missing_receipt_refuses(tmp_path):
    src = _artifacts(tmp_path)
    os.remove(src / LOWERING_RECEIPT)
    with pytest.raises(MissingInput) as e:
        _provision(tmp_path, src=src)
    assert LOWERING_RECEIPT in str(e.value)


@pytest.mark.parametrize("name", ["governed-publication.json", "manifold.cml"])
def test_any_missing_required_input_refuses(tmp_path, name):
    src = _artifacts(tmp_path)
    os.remove(src / name)
    with pytest.raises(MissingInput):
        _provision(tmp_path, src=src)


def test_deployment_configuration_is_required_and_never_invented(tmp_path):
    """Connector choice and warehouse location are operator decisions, not derivable facts."""
    with pytest.raises(MissingInput) as e:
        _provision(tmp_path, data_toml="   ")
    assert "data.toml" in str(e.value)


def test_an_image_with_no_source_manifold_cannot_be_provisioned_as_governed(tmp_path):
    src = _artifacts(tmp_path)
    p = src / "manifold.cml"
    p.write_bytes(b"\n".join(l for l in p.read_bytes().split(b"\n")
                             if not l.startswith(b"SOURCE_MANIFOLD")))
    with pytest.raises(IdentityDisagreement) as e:
        _provision(tmp_path, src=src)
    assert "claims no publication" in str(e.value)


def test_a_malformed_receipt_refuses(tmp_path):
    src = _artifacts(tmp_path)
    (src / LOWERING_RECEIPT).write_text("{not json", encoding="utf-8")
    with pytest.raises(MalformedInput):
        _provision(tmp_path, src=src)


# ── 11. it never repairs, and never leaves a half-unit ───────────────────────────────────────────
@pytest.mark.parametrize("break_it", ["tamper_pub", "tamper_img", "wrong_pub", "no_receipt"])
def test_a_refusal_writes_nothing_at_all(tmp_path, break_it):
    """No partial unit, no re-derived receipt, no 'made to agree'. The destination must not exist."""
    src = _artifacts(tmp_path, "build")
    over = {}
    if break_it == "tamper_pub":
        p = src / "governed-publication.json"
        p.write_bytes(p.read_bytes() + b" ")
    elif break_it == "tamper_img":
        p = src / "manifold.cml"
        p.write_bytes(p.read_bytes() + b"\n#x\n")
    elif break_it == "wrong_pub":
        other = _artifacts(tmp_path, "other", version="1.4.0")
        over["publication"] = str(other / "governed-publication.json")
    elif break_it == "no_receipt":
        os.remove(src / LOWERING_RECEIPT)

    dest = tmp_path / "runtime" / "retail"
    with pytest.raises(ProvisionRefusal):
        _provision(tmp_path, src=src, **over)
    assert not dest.exists(), "a refused provision left a unit behind"
    assert not (tmp_path / "runtime" / "retail.incoming").exists(), "staging leaked"


def test_a_refusal_does_not_rewrite_the_inputs(tmp_path):
    """The provisioner is not permitted to make the artifacts agree — so the inputs it refused must
    be byte-identical afterwards."""
    src = _artifacts(tmp_path, "build")
    other = _artifacts(tmp_path, "other", version="1.4.0")
    before = {n: _sha(str(src / n)) for n in ("governed-publication.json", "manifold.cml",
                                             LOWERING_RECEIPT)}
    with pytest.raises(ProvisionRefusal):
        _provision(tmp_path, src=src, publication=str(other / "governed-publication.json"))
    assert {n: _sha(str(src / n)) for n in before} == before


def test_identity_is_checked_before_digests(tmp_path):
    """Pairing the wrong artifacts should report WHICH publication disagreed, not an opaque hash
    difference — the same ordering the compiler uses for InputIdentityMismatch."""
    src = _artifacts(tmp_path, "build")
    other = _artifacts(tmp_path, "other", version="1.4.0")
    with pytest.raises(IdentityDisagreement):
        _provision(tmp_path, src=src, publication=str(other / "governed-publication.json"))


def test_provisioning_over_an_existing_unit_refuses(tmp_path):
    _provision(tmp_path)
    with pytest.raises(DestinationNotEmpty):
        _provision(tmp_path)


def test_every_refusal_category_is_enumerated():
    for exc in (MissingInput, MalformedInput, IdentityDisagreement, DigestMismatch,
                DestinationNotEmpty):
        assert exc.category in CATEGORIES
    assert len(CATEGORIES) == 5


# ── 12. the packaged legacy fixtures are untouched, and still legacy ─────────────────────────────
def test_packaged_demos_are_untouched_and_remain_legacy(tmp_path):
    """No fixture is promoted by any of this work. The shipped demos carry no SOURCE_MANIFOLD and
    stay compatibility-served — verified against the real packaged directory, and re-verified after
    a provision runs beside them."""
    before = {}
    for root, _dirs, files in os.walk(_DEMOS):
        for f in files:
            p = os.path.join(root, f)
            before[p] = _sha(p)
    assert before, "the packaged demo directory must exist for this test to mean anything"

    demo_copy = tmp_path / "demos"
    shutil.copytree(_DEMOS, demo_copy)
    store = ManifoldStore(str(demo_copy))
    loaded = store.all()
    assert len(loaded) >= 2, f"expected the packaged demos to load, got {len(loaded)}"
    assert {lm.entry_kind for lm in loaded} == {ENTRY_LEGACY}, (
        f"a packaged demo changed entry kind: "
        f"{ {lm.manifold_id: lm.entry_kind for lm in loaded} }")
    assert [c.kind for c in store.conditions()] == [], "a packaged demo grew a load condition"

    _provision(tmp_path)
    assert {p: _sha(p) for p in before} == before, "provisioning touched the packaged demos"

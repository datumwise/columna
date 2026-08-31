"""
test_governed_catalog.py — S2.2b-2: list_manifolds as a governed publication LINEAGE catalog.

The public catalog is organized by governed Manifold publication identity + version, while legacy and
authority-incomplete runtimes remain explicitly classified compatibility entries. Publication existence
(`versions[]`/`latest_version`) and local realizability (`realizable`) are SEPARATE public facts. The
order is deterministic (never filesystem/load order). Only stable condition codes cross the wire — no
raw details, parser text, paths, or exception reprs. contract_version is "4".
"""
import json
import os
import re

import columna_server
from columna_server.registry import ManifoldRef
from columna_server.store import ManifoldStore
from columna_server.tools import list_manifolds
from conftest import write_lowering_receipt

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")
_STABLE_CODES = {"publication_artifact_missing", "publication_artifact_invalid",
                 "unsupported_publication_format", "realization_identity_mismatch",
                 "lowering_receipt_missing", "lowering_receipt_invalid",
                 "lowering_receipt_mismatch"}


def _artifact(src_id, src_ver):
    return {
        "publication_format_version": "1",
        "ref": {"manifold_id": src_id, "version": src_ver},
        "logical": {"declarations": [
            {"kind": "universe", "name": "u", "body": {"basis": "events", "anchor": "keys"}}]},
        "authority": {"published_by": "Huayin", "published_at": "t",
                      "ratifications": {"u": {"ratified_by": "Huayin", "at": "t",
                                              "fingerprint": "fp", "fingerprint_version": "elf-1"}}},
    }


def _scrambled_store(tmp_path) -> ManifoldStore:
    """Folders are named so that directory order != manifold_id order, and retail's versions are
    discovered out of semantic order — to prove the catalog sorts by identity, not by the filesystem."""
    src_cml = open(os.path.join(_CASCADIA, "manifold.cml")).read().splitlines()
    warehouse = os.path.join(_CASCADIA, "warehouse")

    def _write(folder, source_line, artifact=None, receipt=True):
        d = tmp_path / folder
        d.mkdir()
        body = src_cml[:1] + ([source_line] if source_line else []) + src_cml[1:]
        (d / "manifold.cml").write_text("\n".join(body) + "\n")
        (d / "data.toml").write_text(
            f'[manifold]\nname = "{folder}"\n[connector]\ntype = "duckdb"\nwarehouse = "{warehouse}"\n')
        if artifact is not None:
            (d / "governed-publication.json").write_text(json.dumps(artifact))
            if receipt:
                write_lowering_receipt(d, artifact["ref"]["manifold_id"], artifact["ref"]["version"])

    # governed lineages (folder names deliberately out of manifold_id order; retail versions scrambled)
    _write("m_retail_c", "SOURCE_MANIFOLD retail VERSION 1.3.0", _artifact("retail", "1.3.0"))
    _write("a_retail_a", "SOURCE_MANIFOLD retail VERSION 1.1.0", _artifact("retail", "1.1.0"))
    _write("q_retail_b", "SOURCE_MANIFOLD retail VERSION 1.2.0", _artifact("retail", "1.2.0"))
    _write("z_zebra", "SOURCE_MANIFOLD zebra VERSION 2.0.0", _artifact("zebra", "2.0.0"))
    _write("b_finance", "SOURCE_MANIFOLD finance VERSION 0.9.0", _artifact("finance", "0.9.0"))
    # legacy runtimes (no SOURCE_MANIFOLD), folder names out of runtime_id order
    _write("z_demo", None)
    _write("a_demo", None)
    # authority-incomplete: source ref, no artifact (missing) + a ref mismatch (mismatch condition)
    _write("y_incomplete", "SOURCE_MANIFOLD orders VERSION 3.0.0", None)
    _write("x_mismatch", "SOURCE_MANIFOLD widgets VERSION 5.0.0", _artifact("widgets", "9.9.9"))
    return ManifoldStore(str(tmp_path))


def _rows(store, kind):
    return [r for r in list_manifolds(store)["manifolds"] if r["kind"] == kind]


def test_contract_version_is_4(tmp_path):
    assert list_manifolds(_scrambled_store(tmp_path))["contract_version"] == "4"


def test_deterministic_order_governed_then_legacy_then_incomplete(tmp_path):
    store = _scrambled_store(tmp_path)
    cat = list_manifolds(store)["manifolds"]
    kinds = [r["kind"] for r in cat]
    # all governed rows precede all legacy rows precede all authority-incomplete rows
    first_legacy = kinds.index("legacy")
    first_incomplete = kinds.index("authority_incomplete")
    assert all(k == "governed" for k in kinds[:first_legacy])
    assert first_legacy < first_incomplete
    assert [r["manifold_id"] for r in _rows(store, "governed")] == \
        ["finance", "retail", "zebra"]                      # sorted by manifold_id, not folder
    assert [r["runtime_id"] for r in _rows(store, "legacy")] == \
        ["a_demo", "z_demo"]                                # sorted by runtime_id
    assert [r["runtime_id"] for r in _rows(store, "authority_incomplete")] == \
        ["x_mismatch", "y_incomplete"]                      # sorted by runtime_id


def test_versions_ascending_and_latest_is_highest_semver(tmp_path):
    retail = next(r for r in _rows(_scrambled_store(tmp_path), "governed")
                  if r["manifold_id"] == "retail")
    assert [v["version"] for v in retail["versions"]] == ["1.1.0", "1.2.0", "1.3.0"]  # ascending
    assert retail["latest_version"] == "1.3.0"


def test_latest_version_is_a_publication_fact_independent_of_realizable(tmp_path):
    store = _scrambled_store(tmp_path)
    del store._providers_by_ref[ManifoldRef("retail", "1.3.0")]   # the LATEST becomes unrealizable here
    retail = next(r for r in _rows(store, "governed") if r["manifold_id"] == "retail")
    assert retail["latest_version"] == "1.3.0"                    # still latest — a publication fact
    by_ver = {v["version"]: v["realizable"] for v in retail["versions"]}
    assert by_ver == {"1.1.0": True, "1.2.0": True, "1.3.0": False}   # not silently the newest realizable


def test_governed_rows_carry_no_presentation_fields_and_no_conditions(tmp_path):
    for r in _rows(_scrambled_store(tmp_path), "governed"):
        assert set(r) == {"manifold_id", "kind", "latest_version", "versions"}
        assert "conditions" not in r      # a broken runtime never contaminates publication facts
        assert "runtime_id" not in r and "name" not in r and "n_measures" not in r


def test_legacy_row_is_unversioned_and_minimal(tmp_path):
    for r in _rows(_scrambled_store(tmp_path), "legacy"):
        assert set(r) == {"runtime_id", "kind"}
        assert "manifold_id" not in r and "version" not in r and "source_ref" not in r


def test_authority_incomplete_row_keeps_source_ref_and_condition_code(tmp_path):
    store = _scrambled_store(tmp_path)
    rows = {r["runtime_id"]: r for r in _rows(store, "authority_incomplete")}
    missing = rows["y_incomplete"]
    assert missing["source_ref"] == {"manifold_id": "orders", "version": "3.0.0"}   # a CLAIM, not identity
    assert missing["conditions"] == ["publication_artifact_missing"]
    assert "manifold_id" not in missing                     # never looks governed
    mism = rows["x_mismatch"]
    assert mism["source_ref"] == {"manifold_id": "widgets", "version": "5.0.0"}     # the .cml's claim
    assert mism["conditions"] == ["realization_identity_mismatch"]
    # the mismatched artifact's ref (widgets@9.9.9) is NOT admitted as a governed publication
    assert "widgets" not in [r["manifold_id"] for r in _rows(store, "governed")]


def test_only_stable_codes_cross_the_wire_no_raw_detail(tmp_path):
    cat = list_manifolds(_scrambled_store(tmp_path))
    for r in cat["manifolds"]:
        for code in r.get("conditions", []):
            assert code in _STABLE_CODES
    blob = json.dumps(cat)
    for leak in ("governed-publication.json", "Traceback", "Expecting value",
                 str(tmp_path), os.sep + "tmp", "!="):
        assert leak not in blob, leak       # no filenames, parser text, paths, exception reprs


def test_every_condition_the_store_can_emit_has_a_stable_public_code():
    """THE FALL-THROUGH GUARD. `list_manifolds` skips LoadCondition kinds it cannot map, so a new
    condition class without a code would not surface as an unknown value — it would vanish, leaving a
    deployment gap invisible on exactly the surface built to make it visible. This asserts the
    mapping covers every condition class the store constructs, so adding one without a code fails
    here instead of failing silently in production."""
    import inspect

    from columna_server import store as store_mod
    from columna_server.tools import _CONDITION_CODE

    from columna_server import lowering_receipt as lr
    from columna_server import registry as reg

    # the literal kinds the store names itself, read off its source...
    emitted = set(re.findall(r'LoadCondition\(\s*manifold_id,\s*"([A-Za-z]+)"',
                             inspect.getsource(store_mod)))
    # ...plus every condition class it can catch and re-report via type(e).__name__
    for mod, base in ((reg, reg.PublicationArtifactError), (lr, lr.LoweringReceiptError)):
        for name, obj in vars(mod).items():
            if inspect.isclass(obj) and issubclass(obj, base) and obj is not base:
                emitted.add(name)

    missing = sorted(k for k in emitted if k not in _CONDITION_CODE)
    assert not missing, f"LoadCondition kinds with no stable public code: {missing}"
    assert set(_CONDITION_CODE.values()) == _STABLE_CODES

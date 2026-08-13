"""
test_version_aware_serving.py — S2.2b-1: version-aware public selection + resolved-version disclosure.

The public boundary: a convenient selector may omit the version, but every governed operation
resolves to a concrete publication and DISCLOSES it. Governed-first resolution outranks
compatibility-folder identity for the same logical id — deterministically, never by load order. A
legacy / authority-incomplete compatibility runtime stays reachable but is UNVERSIONED (no invented
``manifold_version``). Request-time serving conditions surface through the structural MCP-error channel
as ``publication_not_found`` / ``not_realizable_here`` — pre-adjudication, never analytical moods.
"""
import json
import os

import pytest

import columna_server
from columna_server import tools
from columna_server.registry import ManifoldRef
from columna_server.store import ManifoldStore
from columna_server.tools import (
    ToolInputError,
    check_frame_query,
    describe_manifold,
    execute_frame_query,
)

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")
_Q = "SELECT revenue, orders AT {region*cal.quarter}"


def _artifact(src_id, src_ver):
    return {
        "publication_format_version": "1",
        "ref": {"manifold_id": src_id, "version": src_ver},
        "logical": {"declarations": [
            {"kind": "universe", "name": "u", "body": {"basis": "events", "anchor": "keys"}}]},
        "authority": {"published_by": "Huayin", "published_at": "2026-08-13T00:00:00Z",
                      "ratifications": {"u": {"ratified_by": "Huayin", "at": "t",
                                              "fingerprint": "fp", "fingerprint_version": "elf-1"}}},
    }


def _store(tmp_path) -> ManifoldStore:
    src_cml = open(os.path.join(_CASCADIA, "manifold.cml")).read().splitlines()
    warehouse = os.path.join(_CASCADIA, "warehouse")

    def _write(folder, source_line, artifact=None):
        d = tmp_path / folder
        d.mkdir()
        body = src_cml[:1] + ([source_line] if source_line else []) + src_cml[1:]
        (d / "manifold.cml").write_text("\n".join(body) + "\n")
        (d / "data.toml").write_text(
            f'[manifold]\nname = "{folder}"\n[connector]\ntype = "duckdb"\nwarehouse = "{warehouse}"\n')
        if artifact is not None:
            (d / "governed-publication.json").write_text(json.dumps(artifact))

    _write("retail_v12", "SOURCE_MANIFOLD retail VERSION 1.2.0", _artifact("retail", "1.2.0"))
    _write("retail_v13", "SOURCE_MANIFOLD retail VERSION 1.3.0", _artifact("retail", "1.3.0"))
    _write("retail", None)          # a legacy folder literally named "retail" — must be shadowed
    _write("incomplete", "SOURCE_MANIFOLD finance VERSION 2.0.0", None)   # authority-incomplete
    return ManifoldStore(str(tmp_path))


# ── selector semantics + disclosure ───────────────────────────────────────────────────────────────
def test_explicit_version_resolves_that_publication_and_discloses_it(tmp_path):
    d = describe_manifold(_store(tmp_path), "retail", version="1.2.0")
    assert d["manifold_id"] == "retail" and d["manifold_version"] == "1.2.0"


def test_omitted_version_resolves_highest_governed_semver_and_discloses_it(tmp_path):
    d = describe_manifold(_store(tmp_path), "retail")   # 1.10-style lexical trap absent; 1.3.0 > 1.2.0
    assert d["manifold_id"] == "retail" and d["manifold_version"] == "1.3.0"


def test_query_wire_discloses_the_resolved_publication(tmp_path):
    wire = execute_frame_query(_store(tmp_path), "retail", _Q)          # omitted → latest
    assert wire["manifold_id"] == "retail" and wire["manifold_version"] == "1.3.0"
    # analytical result is unchanged apart from the additive identity
    assert wire["outcome"] in ("serve", "disclose", "clarify", "refuse", "error")
    assert "columns" in wire and "frame" in wire


def test_syntax_error_wire_still_discloses_the_resolved_publication(tmp_path):
    wire = check_frame_query(_store(tmp_path), "retail", "NOT A QUERY", version="1.2.0")
    assert wire["outcome"] == "error"
    assert wire["manifold_id"] == "retail" and wire["manifold_version"] == "1.2.0"


# ── governed-first determinism ─────────────────────────────────────────────────────────────────────
def test_governed_lineage_outranks_a_same_named_compatibility_folder(tmp_path):
    # a legacy folder is literally named "retail"; the governed lineage must win for the public id
    d = describe_manifold(_store(tmp_path), "retail")
    assert d["manifold_version"] == "1.3.0"   # the governed publication, not the legacy folder


def test_provider_bound_to_the_concrete_ref_serves_the_selected_version(tmp_path):
    store = _store(tmp_path)
    # both versions are realizable; the selected one runs and reports its own version
    w12 = execute_frame_query(store, "retail", _Q, version="1.2.0")
    w13 = execute_frame_query(store, "retail", _Q, version="1.3.0")
    assert w12["manifold_version"] == "1.2.0" and w13["manifold_version"] == "1.3.0"


# ── compatibility runtimes are unversioned ─────────────────────────────────────────────────────────
def test_non_governed_id_without_version_falls_back_to_compatibility_unversioned(tmp_path):
    d = describe_manifold(_store(tmp_path), "incomplete")   # a compat folder id (authority-incomplete)
    assert d["manifold_id"] == "incomplete"
    assert "manifold_version" not in d          # never fabricated for an unversioned runtime


def test_legacy_compatibility_response_has_no_invented_version(tmp_path):
    # 'retail' folder is legacy, but shadowed; use the demo's own legacy path via a bare folder id
    store = _store(tmp_path)
    wire = execute_frame_query(store, "incomplete", _Q)
    assert "manifold_version" not in wire


# ── request-time structural failures (pre-adjudication) ─────────────────────────────────────────────
def test_explicit_version_on_a_non_governed_id_is_publication_not_found(tmp_path):
    with pytest.raises(ToolInputError, match="publication_not_found"):
        describe_manifold(_store(tmp_path), "incomplete", version="2.0.0")


def test_unknown_governed_version_is_publication_not_found(tmp_path):
    with pytest.raises(ToolInputError, match="publication_not_found"):
        describe_manifold(_store(tmp_path), "retail", version="9.9.9")


def test_publication_exists_but_no_provider_here_is_not_realizable_here(tmp_path):
    store = _store(tmp_path)
    del store._providers_by_ref[ManifoldRef("retail", "1.2.0")]   # drop this installation's realization
    with pytest.raises(ToolInputError, match="not_realizable_here"):
        describe_manifold(store, "retail", version="1.2.0")


def test_unknown_id_is_an_unknown_manifold_error(tmp_path):
    with pytest.raises(ToolInputError, match="unknown manifold_id"):
        describe_manifold(_store(tmp_path), "nope")


def test_deprecated_query_alias_threads_version(tmp_path):
    wire = tools.query(_store(tmp_path), "retail", _Q, version="1.2.0")
    assert wire["manifold_version"] == "1.2.0"

"""The deployment/provider matrix — runtime selection is OPERATIONAL, and nothing else selects it.

Ruled Huayin, 2026-09-12 §§2-4. Three facts are kept apart and this file is where the separation is
enforced:

    the governed publication major        a fact about the ARTIFACT
    the presence/absence of manifold.cml  a fact about the DEPLOYED UNIT
    the selected execution provider       a fact about THIS INSTALLATION

The failure this guards against is the quiet one: a v2 artifact appearing in a directory and, by
appearing, changing which runtime serves it. That is why every positive case below names its runtime
explicitly and every negative case fails closed rather than falling back.

NO `PlatformExecutionProvider` IS INTEGRATED HERE (§6). A successor-native unit loads, enters the
governed registry, and binds no provider — which the server has always had a word for.
"""
from __future__ import annotations

import pathlib
import shutil

import pytest
from columna_server.registry import NotRealizableHere
from columna_server.store import (
    ENTRY_GOVERNED,
    ENTRY_LEGACY,
    RUNTIME_CORE,
    RUNTIME_PLATFORM,
    ManifoldStore,
    RuntimeSelectionError,
    parse_runtime_selection,
)

V2_ARTIFACT = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
V1_ARTIFACT = (pathlib.Path(__file__).parents[1] / "src" / "columna_server" / "governed"
               / "firstlight" / "governed-publication.json")
DEMO = pathlib.Path(__file__).parents[1] / "src" / "columna_server" / "demo"


def _legacy_unit(root: pathlib.Path, name: str = "cascadia") -> pathlib.Path:
    """A copy of the shipped legacy demo unit — a real `.cml` + data.toml + warehouse."""
    src = DEMO / "cascadia"
    dst = root / name
    shutil.copytree(src, dst)
    return dst


def _governed_only_unit(root: pathlib.Path, name: str = "lighthouse",
                        artifact: pathlib.Path = V2_ARTIFACT) -> pathlib.Path:
    """A successor-native unit: the publication, and NOTHING else. No `.cml`, no data.toml."""
    dst = root / name
    dst.mkdir(parents=True)
    (dst / "governed-publication.json").write_text(artifact.read_text(encoding="utf-8"),
                                                   encoding="utf-8")
    return dst


# ══ the matrix ═══════════════════════════════════════════════════════════════════════════════════

def test_v1_plus_core_plus_cml_is_the_accepted_LEGACY_path(tmp_path):
    """ROW 1. Unchanged: no selection, a `.cml` unit loads through Core exactly as it always did."""
    _legacy_unit(tmp_path)
    store = ManifoldStore(str(tmp_path), runtime_selection={})
    lm = store.get("cascadia")
    assert lm.runtime == RUNTIME_CORE
    assert lm.has_cml is True
    assert lm.manifold is not None and lm.provider is not None
    assert lm.entry_kind == ENTRY_LEGACY


def test_v2_plus_platform_optin_plus_no_cml_is_an_accepted_SUCCESSOR_NATIVE_unit(tmp_path):
    """ROW 2. The unit IS the publication. It loads, it is governed, and it carries no legacy image."""
    _governed_only_unit(tmp_path)
    store = ManifoldStore(str(tmp_path), runtime_selection={"lighthouse": RUNTIME_PLATFORM})
    lm = store.get("lighthouse")
    assert lm.runtime == RUNTIME_PLATFORM
    assert lm.has_cml is False
    assert lm.manifold is None                 # absence represented as absence, not as an empty stub
    assert lm.publication_major == 2
    assert lm.entry_kind == ENTRY_GOVERNED
    assert lm.publication is not None and lm.ref.manifold_id == "lighthouse"
    # it is a real governed lineage…
    assert store.governed_ids() == ["lighthouse"]
    # …that this installation cannot yet serve, which is an ALREADY-EXISTING state, not a new one.
    assert lm.provider is None
    assert store.realizable_refs() == set()
    with pytest.raises(NotRealizableHere):
        store.resolve_public("lighthouse")


def test_the_same_v2_artifact_without_optin_does_not_switch_providers(tmp_path):
    """ROW 3 — THE ONE THAT MATTERS. The artifact is identical; only the selection differs. Without
    it the unit is not served by the successor runtime, and it does not silently become anything."""
    _governed_only_unit(tmp_path)
    _legacy_unit(tmp_path)                     # so the store has at least one loadable unit
    store = ManifoldStore(str(tmp_path), runtime_selection={})
    assert store.ids() == ["cascadia"]          # the governed-only unit is simply not picked up
    assert store.governed_ids() == []
    assert store.get("cascadia").runtime == RUNTIME_CORE


def test_platform_optin_without_a_v2_publication_fails_closed(tmp_path):
    """ROW 4a. A v1 artifact does not become v2 by being selected — its family law is not there."""
    _governed_only_unit(tmp_path, "firstlight", artifact=V1_ARTIFACT)
    with pytest.raises(RuntimeSelectionError) as e:
        ManifoldStore(str(tmp_path), runtime_selection={"firstlight": RUNTIME_PLATFORM})
    assert "major 1" in str(e.value) and "inferring" in str(e.value)


def test_platform_optin_with_no_publication_at_all_fails_closed(tmp_path):
    """ROW 4b. Nothing to serve, and no fallback to the legacy runtime."""
    (tmp_path / "empty").mkdir()
    with pytest.raises(RuntimeSelectionError) as e:
        ManifoldStore(str(tmp_path), runtime_selection={"empty": RUNTIME_PLATFORM})
    assert "governed-publication.json" in str(e.value)


def test_core_selection_without_a_cml_fails_closed_with_no_platform_fallback(tmp_path):
    """ROW 5. The artifact is present and would satisfy the successor runtime — and it is NOT used.
    An explicit Core selection with nothing for Core to execute is an error, not an invitation."""
    _governed_only_unit(tmp_path)
    with pytest.raises(RuntimeSelectionError) as e:
        ManifoldStore(str(tmp_path), runtime_selection={"lighthouse": RUNTIME_CORE})
    assert "no manifold.cml" in str(e.value) and "no fallback" in str(e.value)


def test_a_platform_unit_that_also_ships_a_cml_is_refused(tmp_path):
    """Not in the ruled matrix, but the ambiguity it would create is exactly what the matrix is for:
    a unit claiming to be both is a deployment saying two things, and choosing for it would be the
    silent switch. It refuses instead."""
    unit = _legacy_unit(tmp_path, "lighthouse")
    (unit / "governed-publication.json").write_text(V2_ARTIFACT.read_text(encoding="utf-8"),
                                                    encoding="utf-8")
    with pytest.raises(RuntimeSelectionError) as e:
        ManifoldStore(str(tmp_path), runtime_selection={"lighthouse": RUNTIME_PLATFORM})
    assert "also ships manifold.cml" in str(e.value)


# ══ the selection seam itself ════════════════════════════════════════════════════════════════════

def test_selection_comes_from_the_environment_when_not_passed(tmp_path, monkeypatch):
    _governed_only_unit(tmp_path)
    monkeypatch.setenv("COLUMNA_RUNTIME", "lighthouse=platform")
    store = ManifoldStore(str(tmp_path))
    assert store.get("lighthouse").runtime == RUNTIME_PLATFORM


def test_an_unset_environment_means_everything_is_core(tmp_path, monkeypatch):
    _legacy_unit(tmp_path)
    monkeypatch.delenv("COLUMNA_RUNTIME", raising=False)
    store = ManifoldStore(str(tmp_path))
    assert store.runtime_selection == {}
    assert store.get("cascadia").runtime == RUNTIME_CORE


def test_a_malformed_selection_raises_rather_than_being_ignored():
    """Skipping a typo would hand the deployment the default runtime while it believed otherwise."""
    with pytest.raises(RuntimeSelectionError):
        parse_runtime_selection("lighthouse")                 # no `=runtime`
    with pytest.raises(RuntimeSelectionError):
        parse_runtime_selection("=platform")
    assert parse_runtime_selection(None) == {}
    assert parse_runtime_selection(" a=core , b=platform ") == {"a": "core", "b": "platform"}


def test_an_unknown_runtime_name_refuses(tmp_path):
    _legacy_unit(tmp_path)
    with pytest.raises(RuntimeSelectionError) as e:
        ManifoldStore(str(tmp_path), runtime_selection={"cascadia": "quantum"})
    assert "unknown runtime" in str(e.value)


def test_selecting_a_runtime_for_a_unit_that_does_not_exist_refuses(tmp_path):
    """A selection that names nothing is a configuration error, not a no-op — most likely a typo in
    the id, which would otherwise leave the intended unit quietly on the other runtime."""
    _legacy_unit(tmp_path)
    with pytest.raises(RuntimeSelectionError) as e:
        ManifoldStore(str(tmp_path), runtime_selection={"lightouse": RUNTIME_PLATFORM})
    assert "not units under" in str(e.value)


# ══ the successor-native unit needs no legacy baggage ════════════════════════════════════════════

def test_a_successor_native_unit_needs_no_data_toml_and_no_lowering_receipt(tmp_path):
    """§2. `.cml` is not the only legacy file a governed unit must not be made to carry.

    THE RECEIPT IS NOT WAIVED, IT IS INAPPLICABLE. A lowering receipt attests that a compiler
    produced THIS EXECUTION IMAGE from THIS PUBLICATION. Where there is no image, there is no such
    binding to attest — and the obligation stays exactly as strict on the lowered path, which the
    unchanged governed-fixture tests continue to prove."""
    unit = _governed_only_unit(tmp_path)
    assert sorted(p.name for p in unit.iterdir()) == ["governed-publication.json"]
    store = ManifoldStore(str(tmp_path), runtime_selection={"lighthouse": RUNTIME_PLATFORM})
    assert store.get("lighthouse").entry_kind == ENTRY_GOVERNED
    assert store.conditions() == []             # not a deployment gap; a different kind of unit


def test_the_catalog_shows_it_as_governed_and_not_realizable_with_no_new_public_vocabulary(tmp_path):
    """§5. No new catalog kind and no new condition code: the successor-native unit is a governed
    lineage whose only version is not realizable here, which contract v3 already expresses."""
    from columna_server.tools import list_manifolds

    _governed_only_unit(tmp_path)
    store = ManifoldStore(str(tmp_path), runtime_selection={"lighthouse": RUNTIME_PLATFORM})
    cat = list_manifolds(store)
    assert cat["contract_version"] == "5"
    assert cat["manifolds"] == [{
        "manifold_id": "lighthouse", "kind": "governed", "latest_version": "1.0.0",
        "versions": [{"version": "1.0.0", "realizable": False}]}]

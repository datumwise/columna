"""
test_manifold_registry.py — the S2.1 shared-identity / registry invariants.

Two layers:
  * registry/types (no warehouse) via `parse_manifold` on `.cml` strings;
  * store integration (warehouse) over a governed fixture built on the real cascadia warehouse.

Proves: a selector resolves to a concrete versioned `ManifoldRef`; versions coexist; "latest" is
highest semver (not lexical/recency); the logical projection is physical-clean; legacy `.cml` is not
promoted to governance; a publication is immutable and independent of provider attachment; and
`not_realizable_here` (publication exists, no provider) is distinct from `publication_not_found`.
"""
import json
import os

import pytest

import columna_server
from columna_core import no_physical_leak
from columna_core.parser import parse_manifold
from columna_server.registry import (
    FolderManifoldRegistry,
    GovernedPublication,
    ManifoldRef,
    ManifoldSelector,
    PublicationNotFound,
    ResolvedManifold,
    governed_publication_from_manifold,
)
from columna_server.store import ManifoldStore

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


def _cml(src_id=None, src_ver=None):
    lines = ["MANIFOLD m VERSION 1"]
    if src_id:
        lines.append(f"SOURCE_MANIFOLD {src_id} VERSION {src_ver}")
    lines += [
        "LEVEL day = day BASE",
        "UNIVERSE u = day BASIS events",
        "MEASURE revenue ON u FROM sales AS sum(amount)",
    ]
    return "\n".join(lines) + "\n"


def _pub(src_id, src_ver) -> GovernedPublication:
    return governed_publication_from_manifold(parse_manifold(_cml(src_id, src_ver)))


def _reg(*versions) -> FolderManifoldRegistry:
    return FolderManifoldRegistry({ManifoldRef("retail", v): _pub("retail", v) for v in versions})


# ── registry / identity (no warehouse) ───────────────────────────────────────────────────────────
def test_selector_resolves_to_a_concrete_versioned_ref():
    pub = _reg("1.2.0", "1.3.0").resolve(ManifoldSelector("retail"))  # version-less selector → latest
    assert pub.ref == ManifoldRef("retail", "1.3.0")
    assert pub.ref.version == "1.3.0"  # always concrete — no implicit None survives resolution


def test_selector_with_version_resolves_exactly():
    assert _reg("1.2.0", "1.3.0").resolve(ManifoldSelector("retail", "1.2.0")).ref.version == "1.2.0"


def test_two_versions_of_the_same_id_coexist():
    reg = _reg("1.2.0", "1.3.0")
    assert {r.version for r in reg.list() if r.manifold_id == "retail"} == {"1.2.0", "1.3.0"}
    assert reg.resolve(ManifoldSelector("retail", "1.2.0")).ref.version == "1.2.0"
    assert reg.resolve(ManifoldSelector("retail", "1.3.0")).ref.version == "1.3.0"


def test_latest_is_highest_semver_not_lexical_or_recency():
    reg = _reg("1.9.0", "1.10.0")  # "1.10.0" < "1.9.0" lexically
    assert reg.latest("retail") == "1.10.0"
    assert reg.resolve(ManifoldSelector("retail")).ref.version == "1.10.0"


def test_unknown_publication_is_not_found():
    reg = _reg("1.0.0")
    with pytest.raises(PublicationNotFound):
        reg.resolve(ManifoldSelector("finance"))          # unknown id
    with pytest.raises(PublicationNotFound):
        reg.resolve(ManifoldSelector("retail", "9.9.9"))  # unknown version of a known id
    assert reg.latest("finance") is None


def test_logical_projection_has_no_physical_realization_identifiers():
    m = parse_manifold(_cml("retail", "1.0.0"))
    pub = governed_publication_from_manifold(m)
    assert no_physical_leak(m) == []  # the engine's own wall check on the source manifold
    blob = json.dumps(pub.logical)
    for physical in ("binds_to", "rejects", "home_table", "pre_expr", "provider_table",
                     "frm_col", "to_col", "connection"):
        assert physical not in blob


def test_legacy_cml_is_not_promoted_to_governance():
    # a source-identity-less .cml yields NO governed publication — id/version/ratification not invented
    assert governed_publication_from_manifold(parse_manifold(_cml())) is None


def test_publication_ref_is_immutable_and_provider_independent():
    pub = _pub("retail", "1.2.0")
    assert _pub("retail", "1.2.0").ref == pub.ref  # same (id, version) → same identity
    with pytest.raises(Exception):
        pub.ref.version = "9.9.9"  # frozen identity

    # attaching / detaching a provider never mutates the (frozen) publication
    resolved = ResolvedManifold(publication=pub, provider=None)  # not realizable here
    assert resolved.provider is None
    resolved.provider = object()                                  # attach a realization
    assert resolved.publication is pub                            # unchanged, same object


# ── store integration (warehouse; governed fixture over the real cascadia data) ───────────────────
def _governed_store(tmp_path) -> ManifoldStore:
    """A temp manifolds dir: two governed versions of `retail` + one legacy, all over cascadia's data."""
    src_cml = open(os.path.join(_CASCADIA, "manifold.cml")).read().splitlines()
    warehouse = os.path.join(_CASCADIA, "warehouse")

    def _write(folder, source_line):
        d = tmp_path / folder
        d.mkdir()
        body = src_cml[:1] + ([source_line] if source_line else []) + src_cml[1:]
        (d / "manifold.cml").write_text("\n".join(body) + "\n")
        (d / "data.toml").write_text(
            f'[manifold]\nname = "{folder}"\n[connector]\ntype = "duckdb"\nwarehouse = "{warehouse}"\n'
        )

    _write("retail_v12", "SOURCE_MANIFOLD retail VERSION 1.2.0")
    _write("retail_v13", "SOURCE_MANIFOLD retail VERSION 1.3.0")
    _write("legacy", None)
    return ManifoldStore(str(tmp_path))


def test_store_resolves_governed_latest_and_exact_version(tmp_path):
    store = _governed_store(tmp_path)
    latest = store.resolve(ManifoldSelector("retail"))
    assert latest.publication.ref == ManifoldRef("retail", "1.3.0")
    assert latest.provider is not None  # realizable here
    exact = store.resolve(ManifoldSelector("retail", "1.2.0"))
    assert exact.publication.ref.version == "1.2.0" and exact.provider is not None


def test_store_legacy_entry_is_usable_but_carries_no_governance(tmp_path):
    lm = _governed_store(tmp_path).get("legacy")  # reachable by folder id (compatibility path)
    assert lm.provider is not None       # serves
    assert lm.publication is None and lm.ref is None  # never promoted to a governed publication


def test_store_not_realizable_here_is_distinct_from_not_found(tmp_path):
    store = _governed_store(tmp_path)
    # the publication exists in the registry, but this installation has no provider for it
    del store._providers_by_ref[ManifoldRef("retail", "1.2.0")]
    resolved = store.resolve(ManifoldSelector("retail", "1.2.0"))
    assert resolved.publication.ref == ManifoldRef("retail", "1.2.0")
    assert resolved.provider is None  # not_realizable_here — NOT publication_not_found
    with pytest.raises(PublicationNotFound):
        store.resolve(ManifoldSelector("retail", "9.9.9"))  # publication_not_found

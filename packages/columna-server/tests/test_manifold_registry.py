"""
test_manifold_registry.py — the shared-identity / registry invariants (S2.1 + S2.2a-3).

Two layers:
  * registry/types (no warehouse): a ``GovernedPublication`` is built from a ``governed-publication.json``
    artifact (S2.2a-3), never from ``.cml.logical_spec()``;
  * store integration (warehouse) over a governed fixture on the real cascadia warehouse, exercising the
    three-way runtime classification.

Proves: a selector resolves to a concrete versioned ``ManifoldRef``; versions coexist; "latest" is
highest semver (not lexical/recency); ``GovernedPublication.{ref,logical,authority}`` come from the
artifact and stay independent of the ``.cml`` realization (the blast wall); a ``.cml`` with no
``SOURCE_MANIFOLD`` is legacy; a ``.cml`` WITH a source ref but no artifact is authority-incomplete
(compatibility-served, never governed); an artifact whose ref disagrees with the ``.cml`` does not
bind (``RealizationIdentityMismatch``); and ``not_realizable_here`` stays distinct from
``publication_not_found``. The server ingests the artifact with the stdlib only — no ``manifold_agent``.
"""
import json
import os
import sys

import pytest

import columna_server
from columna_server.registry import (
    FolderManifoldRegistry,
    GovernedPublication,
    ManifoldRef,
    ManifoldSelector,
    PublicationArtifactInvalid,
    PublicationNotFound,
    ResolvedManifold,
    UnsupportedPublicationFormat,
    governed_publication_from_artifact,
    parse_publication_artifact,
)
from columna_server.store import (
    ENTRY_GOVERNED,
    ENTRY_LEGACY,
    ENTRY_SOURCE_REFERENCED_INCOMPLETE,
    ManifoldStore,
)
from conftest import write_lowering_receipt

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


# ── artifact fixtures (the governed-publication.json a governed publish emits) ─────────────────────
def _artifact_dict(src_id, src_ver, universes=("u",)):
    return {
        "publication_format_version": "1",
        "ref": {"manifold_id": src_id, "version": src_ver},
        "logical": {"declarations": [
            {"kind": "universe", "name": u, "body": {"basis": "events", "anchor": "keys"}}
            for u in universes
        ]},
        "authority": {
            "published_by": "Huayin", "published_at": "2026-08-13T00:00:00Z",
            "ratifications": {
                u: {"ratified_by": "Huayin", "at": "2026-08-11T00:00:00Z",
                    "fingerprint": f"fp-{u}", "fingerprint_version": "elf-1"}
                for u in universes
            },
        },
    }


def _pub(src_id, src_ver) -> GovernedPublication:
    return governed_publication_from_artifact(parse_publication_artifact(_artifact_dict(src_id, src_ver)))


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


# ── the artifact is the source of truth ────────────────────────────────────────────────────────────
def test_governed_publication_comes_from_the_artifact_verbatim():
    art = _artifact_dict("retail", "1.2.0", universes=("orders",))
    pub = governed_publication_from_artifact(parse_publication_artifact(art))
    assert pub.ref == ManifoldRef("retail", "1.2.0")
    assert pub.logical == art["logical"]                       # verbatim, authoring vocabulary
    assert pub.authority.ratification == art["authority"]["ratifications"]
    assert pub.authority.actor == "Huayin"


def test_artifact_logical_is_physical_clean():
    blob = json.dumps(_pub("retail", "1.0.0").logical)
    for physical in ("binds_to", "rejects", "home_table", "pre_expr", "provider_table",
                     "frm_col", "to_col", "connection", "table", "column"):
        assert physical not in blob


def test_unsupported_format_is_distinct_from_invalid():
    bad_major = _artifact_dict("retail", "1.0.0"); bad_major["publication_format_version"] = "2.0"
    with pytest.raises(UnsupportedPublicationFormat):
        parse_publication_artifact(bad_major)
    # a supported-format artifact that is structurally broken is INVALID, a different condition
    no_ref = _artifact_dict("retail", "1.0.0"); del no_ref["ref"]
    with pytest.raises(PublicationArtifactInvalid):
        parse_publication_artifact(no_ref)
    # ratification keys must correspond to universes
    mismatch = _artifact_dict("retail", "1.0.0", universes=("u",))
    mismatch["authority"]["ratifications"] = {}
    with pytest.raises(PublicationArtifactInvalid):
        parse_publication_artifact(mismatch)


def test_publication_ref_is_immutable_and_provider_independent():
    pub = _pub("retail", "1.2.0")
    assert _pub("retail", "1.2.0").ref == pub.ref  # same (id, version) → same identity
    with pytest.raises(Exception):
        pub.ref.version = "9.9.9"  # frozen identity
    resolved = ResolvedManifold(publication=pub, provider=None)  # not realizable here
    assert resolved.provider is None
    resolved.provider = object()                                  # attach a realization
    assert resolved.publication is pub                            # unchanged, same object


# ── store integration (warehouse; governed fixture over the real cascadia data) ───────────────────
def _cml_body():
    return open(os.path.join(_CASCADIA, "manifold.cml")).read().splitlines()


def _governed_store(tmp_path) -> ManifoldStore:
    """A temp manifolds dir exercising every runtime kind, all over cascadia's data:
      * two governed versions of ``retail`` (SOURCE_MANIFOLD + matching artifact);
      * a source-referenced-but-incomplete entry (SOURCE_MANIFOLD, no artifact);
      * a mismatch entry (artifact ref != the .cml SOURCE_MANIFOLD);
      * a legacy entry (no SOURCE_MANIFOLD).
    """
    src_cml = _cml_body()
    warehouse = os.path.join(_CASCADIA, "warehouse")

    def _write(folder, source_line, artifact=None, receipt=True):
        d = tmp_path / folder
        d.mkdir()
        body = src_cml[:1] + ([source_line] if source_line else []) + src_cml[1:]
        (d / "manifold.cml").write_text("\n".join(body) + "\n")
        (d / "data.toml").write_text(
            f'[manifold]\nname = "{folder}"\n[connector]\ntype = "duckdb"\nwarehouse = "{warehouse}"\n'
        )
        if artifact is not None:
            (d / "governed-publication.json").write_text(json.dumps(artifact))
            # A governed unit is artifact + image + the receipt binding them. Written last, over the
            # bytes just laid down: the receipt is evidence about THESE files, not a flag.
            if receipt:
                write_lowering_receipt(d, artifact["ref"]["manifold_id"], artifact["ref"]["version"])

    _write("retail_v12", "SOURCE_MANIFOLD retail VERSION 1.2.0", _artifact_dict("retail", "1.2.0"))
    _write("retail_v13", "SOURCE_MANIFOLD retail VERSION 1.3.0", _artifact_dict("retail", "1.3.0"))
    _write("incomplete", "SOURCE_MANIFOLD finance VERSION 2.0.0", None)                # no artifact
    _write("mismatch", "SOURCE_MANIFOLD widgets VERSION 5.0.0",
           _artifact_dict("widgets", "9.9.9"))                                          # ref disagrees
    _write("legacy", None)
    return ManifoldStore(str(tmp_path))


def test_store_resolves_governed_latest_and_exact_version(tmp_path):
    store = _governed_store(tmp_path)
    latest = store.resolve(ManifoldSelector("retail"))
    assert latest.publication.ref == ManifoldRef("retail", "1.3.0")
    assert latest.provider is not None  # realizable here
    exact = store.resolve(ManifoldSelector("retail", "1.2.0"))
    assert exact.publication.ref.version == "1.2.0" and exact.provider is not None
    assert store.get("retail_v12").entry_kind == ENTRY_GOVERNED


def test_governed_logical_comes_from_artifact_not_the_cml(tmp_path):
    """The blast wall: GovernedPublication.logical is the artifact's, never derived from the .cml.
    The cascadia .cml carries LEVELs/MEASUREs (e.g. its own dimensions) — none of that leaks in;
    only the artifact's universe 'u' is present."""
    pub = _governed_store(tmp_path).resolve(ManifoldSelector("retail", "1.2.0")).publication
    assert pub.logical == _artifact_dict("retail", "1.2.0")["logical"]
    names = {d["name"] for d in pub.logical["declarations"]}
    assert names == {"u"}                                    # exactly the artifact's declaration(s)
    # the .cml's own identifiers do not appear in the governed logical meaning
    cml_text = "\n".join(_cml_body())
    for tok in ("MEASURE", "LEVEL", "FROM"):
        assert tok in cml_text                               # the .cml really does carry them...
    assert "MEASURE" not in json.dumps(pub.logical)          # ...but the artifact-derived logical does not


def test_store_legacy_entry_is_usable_but_carries_no_governance(tmp_path):
    lm = _governed_store(tmp_path).get("legacy")  # reachable by folder id (compatibility path)
    assert lm.provider is not None       # serves
    assert lm.publication is None and lm.ref is None  # never promoted to a governed publication
    assert lm.entry_kind == ENTRY_LEGACY


def test_source_referenced_without_artifact_is_authority_incomplete(tmp_path):
    store = _governed_store(tmp_path)
    lm = store.get("incomplete")
    assert lm.provider is not None                     # still compatibility-served
    assert lm.publication is None and lm.ref is None   # NOT a governed publication
    assert lm.entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE
    # and it never appears as a governed publication through the registry
    with pytest.raises(PublicationNotFound):
        store.resolve(ManifoldSelector("finance", "2.0.0"))
    # the missing-authority condition is observable, not silently swallowed
    kinds = {(c.manifold_id, c.kind) for c in store.conditions()}
    assert ("incomplete", "PublicationArtifactMissing") in kinds


def test_realization_identity_mismatch_does_not_bind(tmp_path):
    store = _governed_store(tmp_path)
    lm = store.get("mismatch")
    assert lm.publication is None and lm.ref is None   # provider not bound as this artifact's realization
    assert lm.entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE
    with pytest.raises(PublicationNotFound):
        store.resolve(ManifoldSelector("widgets", "9.9.9"))   # the artifact's ref is not served here
    kinds = {(c.manifold_id, c.kind) for c in store.conditions()}
    assert ("mismatch", "RealizationIdentityMismatch") in kinds


def test_store_not_realizable_here_is_distinct_from_not_found(tmp_path):
    store = _governed_store(tmp_path)
    # the publication exists in the registry, but this installation has no provider for it
    del store._providers_by_ref[ManifoldRef("retail", "1.2.0")]
    resolved = store.resolve(ManifoldSelector("retail", "1.2.0"))
    assert resolved.publication.ref == ManifoldRef("retail", "1.2.0")
    assert resolved.provider is None  # not_realizable_here — NOT publication_not_found
    with pytest.raises(PublicationNotFound):
        store.resolve(ManifoldSelector("retail", "9.9.9"))  # publication_not_found


def test_server_ingests_the_artifact_without_importing_manifold_agent(tmp_path):
    _governed_store(tmp_path)  # a full governed load
    assert "manifold_agent" not in sys.modules  # the server reads the artifact as plain JSON only

"""
test_native_v3_spine.py — C2's stop-gate, witnessed.

    *"a v3 unit **loads and is visible in the catalog** — the present failure is invisibility, not
    refusal — and v1/v2 units are byte-unchanged."*
        — native_v3_consumer_recon_v0_1.md §13, C2

Two halves, and the second matters as much as the first: the native unit becomes visible, and
nothing about the legacy units moves. Nothing here selects a runtime for the native unit, because
SERVING a native publication is not C2's subject — visibility is.
"""
from __future__ import annotations

import copy
import json
import pathlib
import shutil

import pytest

import columna_server
from columna_server.registry import (
    SUPPORTED_PUBLICATION_FORMAT_MAJORS,
    PublicationArtifactInvalid,
    parse_publication_artifact,
)
from columna_server.store import RUNTIME_PLATFORM, ManifoldStore, RuntimeSelectionError
from columna_server.tools import ToolInputError, discovery, list_manifolds

_HERE = pathlib.Path(__file__).parent
V3_ARTIFACT = (_HERE.parents[1] / "columna-core" / "tests" / "fixtures_v3"
               / "native-v3-publication.json")
V2_ARTIFACT = (_HERE.parents[1] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
#: The shipped v1 governed unit — `.cml` + artifact + lowering receipt + its own warehouse, so it
#: is self-contained and can be copied into a temporary installation intact.
V1_UNIT = pathlib.Path(columna_server.__file__).parent / "governed" / "firstlight"

NATIVE, V2, V1 = "harbour", "lighthouse", "firstlight"


def _unit(root: pathlib.Path, name: str, artifact: pathlib.Path) -> None:
    d = root / name
    d.mkdir()
    (d / "governed-publication.json").write_text(artifact.read_text(encoding="utf-8"),
                                                 encoding="utf-8")


@pytest.fixture
def raw():
    return json.loads(V3_ARTIFACT.read_text(encoding="utf-8"))


@pytest.fixture
def store(tmp_path):
    """One installation holding all three majors: the shipped v1 lowered unit, a v2 governed-only
    unit, and a native v3 governed-only unit. No runtime is selected for any of them."""
    _unit(tmp_path, NATIVE, V3_ARTIFACT)
    _unit(tmp_path, V2, V2_ARTIFACT)
    shutil.copytree(V1_UNIT, tmp_path / V1)
    return ManifoldStore(str(tmp_path))


# ── stop-gate, first half · the native unit LOADS and is VISIBLE ─────────────────────────────────
def test_major_three_is_a_reader_not_a_branch():
    assert SUPPORTED_PUBLICATION_FORMAT_MAJORS == (1, 2, 3)


def test_a_v3_unit_loads(store):
    lm = store.get(NATIVE)
    assert lm.publication_major == 3
    assert lm.has_cml is False
    assert lm.manifold is None                    # no legacy image, honestly absent
    assert lm.ref.manifold_id == "harbour" and lm.ref.version == "1.0.0"


def test_a_v3_unit_is_visible_in_the_catalog(store):
    """The measured failure this unit corrects: before C2 the store's visibility probe swallowed
    `UnsupportedPublicationFormat` and this row did not exist at all."""
    rows = {r.get("manifold_id"): r for r in list_manifolds(store)["manifolds"]
            if r.get("kind") == "governed"}
    assert "harbour" in rows
    assert rows["harbour"]["latest_version"] == "1.0.0"
    assert rows["harbour"]["versions"] == [{"version": "1.0.0", "realizable": False}]


def test_visible_and_unserved_is_an_existing_state_not_a_new_one(store):
    """`realizable: false` — the publication exists and this installation cannot serve it. No new
    catalog kind, no new condition code, no new public state."""
    assert store.get(NATIVE).provider is None
    assert store.get(NATIVE).ref not in store.realizable_refs()


def test_the_publication_is_the_NATIVE_model_not_a_projection(store):
    pub = store.get(NATIVE).publication
    assert pub.is_native
    assert pub.logical is None                    # never cross-filled
    assert pub.authority.ratification is None     # v2's map does not exist; nothing is fabricated
    assert pub.authority.actor == "harbour steward"
    u = pub.native.universe("harbour")
    assert u.coordinates == ("berth", "day")
    assert u.constitution.fingerprint() == u.attestation.fingerprint


def test_every_currency_claim_still_verifies_through_the_server_path(store):
    verdicts = [c.verdict for c in store.get(NATIVE).publication.native.currency()]
    assert verdicts == ["CURRENT", "COVERED", "BOUND", "CURRENT", "UNBOUND", "CURRENT"]


# ── stop-gate, second half · v1/v2 are BYTE-UNCHANGED ────────────────────────────────────────────
def test_the_legacy_and_v2_rows_are_identical_with_and_without_the_native_unit(tmp_path):
    """The comparison that makes 'byte-unchanged' checkable: build the catalog twice, once with the
    native unit present and once without, and diff every row that is not the native one."""
    without = tmp_path / "without"
    without.mkdir()
    _unit(without, V2, V2_ARTIFACT)
    shutil.copytree(V1_UNIT, without / V1)

    with_native = tmp_path / "with"
    with_native.mkdir()
    _unit(with_native, V2, V2_ARTIFACT)
    _unit(with_native, NATIVE, V3_ARTIFACT)
    shutil.copytree(V1_UNIT, with_native / V1)

    def rows(d):
        cat = list_manifolds(ManifoldStore(str(d)))["manifolds"]
        return [r for r in cat if r.get("manifold_id") != "harbour"]

    assert rows(without) == rows(with_native)


def test_the_v2_unit_still_reads_as_v2_beside_a_native_one(store):
    pub = store.get(V2).publication
    assert store.get(V2).publication_major == 2
    assert not pub.is_native and pub.native is None
    assert pub.logical["declarations"]            # the v2 projection, untouched
    assert pub.authority.ratification is not None


def test_the_v1_unit_still_reads_as_v1_beside_a_native_one(store):
    lm = store.get(V1)
    assert lm.publication_major == 1
    assert lm.has_cml and lm.manifold is not None
    assert lm.publication is not None and not lm.publication.is_native


def test_v1_and_v2_envelope_checks_moved_but_did_not_change():
    """The envelope left the shared spine for `_v1v2_envelope` — same checks, same order, same
    bytes. Its refusals are the witness that it still runs."""
    art = {"publication_format_version": "1", "ref": {"manifold_id": "x", "version": "1.0.0"}}
    with pytest.raises(PublicationArtifactInvalid, match="logical.declarations must be a list"):
        parse_publication_artifact(art)
    art["logical"] = {"declarations": [{"kind": "universe", "name": "u", "body": {}}]}
    with pytest.raises(PublicationArtifactInvalid, match="missing authority object"):
        parse_publication_artifact(art)
    art["authority"] = {"ratifications": {}}
    with pytest.raises(PublicationArtifactInvalid, match="ratification keys must correspond"):
        parse_publication_artifact(art)


# ── the spine really split ───────────────────────────────────────────────────────────────────────
def test_the_native_artifact_needs_no_logical_wrapper_and_no_authority_section(raw):
    """The whole of the split, in one assertion: an artifact with neither key parses, and the two
    facts every major does share — a supported major and a concrete ref — are the only ones asked
    of it above the reader."""
    assert "logical" not in raw and "authority" not in raw
    art = parse_publication_artifact(raw)
    assert (art.major, art.ref.manifold_id) == (3, "harbour")
    assert art.logical is None and art.authority is None and art.native is not None


def test_a_v2_shaped_artifact_wearing_a_v3_label_refuses_on_its_SHAPE():
    """Ruling 5's converse, at the server seam. The v2 reader's measured permissiveness is not
    exploited in either direction."""
    v2 = json.loads(V2_ARTIFACT.read_text(encoding="utf-8"))
    v2["publication_format_version"] = "3.0"
    with pytest.raises(PublicationArtifactInvalid, match=r"v3 contract:.*unrecognised key"):
        parse_publication_artifact(v2)


def test_a_native_artifact_wearing_a_v2_label_is_not_a_way_in(raw):
    """And the direction that actually worked before: relabelled `"2.0"`, the v2 reader once
    accepted these bytes and silently discarded the constitution. It is not reached by relabelling
    here — the artifact has no `logical` wrapper, so v2's own envelope refuses it first."""
    d = copy.deepcopy(raw)
    d["publication_format_version"] = "2.0"
    with pytest.raises(PublicationArtifactInvalid, match="logical.declarations must be a list"):
        parse_publication_artifact(d)


def test_a_broken_native_artifact_is_INVALID_under_the_v3_contract(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["existence_law_ratification"]["fingerprint"] = "elf-2:" + "0" * 64
    with pytest.raises(PublicationArtifactInvalid,
                       match="v3 contract:.*attestation does not cover this law"):
        parse_publication_artifact(d)


# ── visibility is not serving ────────────────────────────────────────────────────────────────────
def test_selecting_the_platform_runtime_for_a_v3_unit_refuses_by_name(tmp_path):
    _unit(tmp_path, NATIVE, V3_ARTIFACT)
    with pytest.raises(RuntimeSelectionError, match="is major 3"):
        ManifoldStore(str(tmp_path), runtime_selection={NATIVE: RUNTIME_PLATFORM})


def test_discovery_today_stops_at_the_provider_gate(store):
    """The REACHABLE behaviour, and it is already honest: an unselected native unit has no
    provider, so `discovery` never reaches the governed projection at all."""
    with pytest.raises(ToolInputError, match="not_realizable_here"):
        discovery(store, NATIVE)


def test_the_governed_projection_refuses_a_native_publication_rather_than_answering_emptily(store):
    """The guard BEHIND that gate, exercised directly because nothing reaches it yet.

    `_governed_discovery` reads `publication.logical`, and on a native publication the default
    would be `measures: [], anchors: [], levels: []` — a well-formed answer meaning *this manifold
    has nothing to ask*, about a publication carrying two families and a two-constituent universe.
    The moment a native unit binds a provider this becomes the fabrication site, so the refusal is
    placed now rather than discovered then. What the payload SHOULD say for a native unit is an
    open question this unit does not settle."""
    from columna_server.tools import _governed_discovery
    lm = store.get(NATIVE)
    with pytest.raises(ToolInputError, match="native_publication_not_discoverable"):
        _governed_discovery(lm, NATIVE, lm.ref)


# ── a native publication beside a legacy image ───────────────────────────────────────────────────
def test_a_native_publication_beside_a_cml_is_classified_never_promoted(tmp_path):
    """The `.cml` universe construct has no slot for a constitution, so no lowering receipt can
    attest that this image realizes this publication. Observable, classified, never promoted."""
    shutil.copytree(V1_UNIT, tmp_path / V1)
    (tmp_path / V1 / "governed-publication.json").write_text(
        V3_ARTIFACT.read_text(encoding="utf-8"), encoding="utf-8")
    store = ManifoldStore(str(tmp_path))
    lm = store.get(V1)
    assert lm.publication is None                 # never promoted
    assert lm.publication_major == 3              # what it WAS, recorded honestly
    assert lm.condition.kind == "NativePublicationNotLowerable"
    codes = [c for r in list_manifolds(store)["manifolds"] for c in r.get("conditions", [])]
    assert "native_publication_not_lowerable" in codes

"""The server's supported publication majors — {1, 2, 3} (ruled Huayin 2026-09-12, widened
2026-09-22).

WHAT THIS FILE USED TO SAY. It pinned `SUPPORTED_PUBLICATION_FORMAT_MAJOR == 1` and recorded why the
realization-freeze conformance unit would not lift it: whether this server should accept publication
major 2 is a COMPATIBILITY RULING — about which artifacts this build serves — not a drift test, and
the freeze (§10.2, RATIFIED 2026-09-12) held it open under exactly that name.

THE RULING CAME, and it is not "v2 replaces v1". It is:

    v1 remains a supported input FOR THE LEGACY CORE SERVING PATH;
    v2 is a supported input FOR THE SUCCESSOR PLATFORM PATH;
    each is read according to its own contract.

So the scalar had to go rather than change value. A scalar could express "the major this server
supports" and cannot express two majors meaning two different things — and widening its meaning while
keeping its name would have been the misleading compatibility the ruling forbids.

**MAJOR 3 ARRIVED ON THE SAME PRINCIPLE (C2, 2026-09-22).** The native ToD-v7.1 contract is a third
input read by its own reader, and the failure it corrects was not a refusal but a SILENCE: a v3
artifact raised `UnsupportedPublicationFormat` inside the store's visibility probe, the probe
swallowed it, and a deployment holding a lawful native publication was told it had nothing. The
refusal itself was load-bearing and stays — relabel a v3 artifact `"2.0"` and the v2 reader accepts
it while discarding every constitution it carries — so v3 is admitted by being READ AS v3, never by
relabelling and never by widening v2.

WHAT THIS FILE PINS NOW: that all three majors are readable, that NONE IS A SHIM FOR ANOTHER, and
that the import-disjointness which made the original coherence untestable in-process still holds.
"""
import json
import pathlib

import pytest
from columna_server.registry import (
    SUPPORTED_PUBLICATION_FORMAT_MAJORS,
    PublicationArtifactInvalid,
    UnsupportedPublicationFormat,
    parse_publication_artifact,
)

V1 = (pathlib.Path(__file__).parents[1] / "src" / "columna_server" / "governed" / "firstlight"
      / "governed-publication.json")
V2 = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
      / "lighthouse-v2-publication.json")


def test_both_majors_are_supported_and_the_scalar_is_gone():
    assert SUPPORTED_PUBLICATION_FORMAT_MAJORS == (1, 2, 3)
    import columna_server.registry as reg
    assert not hasattr(reg, "SUPPORTED_PUBLICATION_FORMAT_MAJOR"), (
        "the scalar must not survive beside the set — two spellings of one policy is how they drift")


def test_the_shipped_v1_artifact_still_reads_as_v1():
    """v1 COMPATIBILITY. `firstlight` is the frozen historical fixture and was not re-authored."""
    art = parse_publication_artifact(json.loads(V1.read_text(encoding="utf-8")))
    assert art.major == 1
    assert art.ref.manifold_id == "firstlight"


def test_a_v2_artifact_reads_as_v2():
    art = parse_publication_artifact(json.loads(V2.read_text(encoding="utf-8")))
    assert art.major == 2
    assert art.ref.manifold_id == "lighthouse"


def test_an_unknown_major_is_still_refused():
    """Supporting three is not supporting all. An unknown major refuses, naming what IS supported."""
    with pytest.raises(UnsupportedPublicationFormat) as e:
        parse_publication_artifact({
            "publication_format_version": "9.0", "ref": {"manifold_id": "x", "version": "1"},
            "logical": {"declarations": []}, "authority": {"ratifications": {}}})
    assert "majors [1, 2, 3]" in str(e.value)


def test_v2_is_read_through_v2s_OWN_reader_not_a_second_implementation():
    """The v2 contract's rules are enforced because the v2 reader enforces them — not because the
    server re-states them. §2.2's ambiguity refusal is the witness: two families under one reference
    must be refused at ingest, and nothing in `registry.py` knows what a family is."""
    raw = json.loads(V2.read_text(encoding="utf-8"))
    for decl in raw["logical"]["declarations"]:
        if decl["kind"] == "family" and decl["body"]["canonical_reference"].startswith("count("):
            decl["body"]["aliases"] = ["revenue"]
    with pytest.raises(PublicationArtifactInvalid) as e:
        parse_publication_artifact(raw)
    assert "v2 contract" in str(e.value) and "ambiguous canonical reference" in str(e.value)


def test_a_v1_artifact_is_never_deepened_into_v2():
    """NO SHIM, in the direction that would matter. The v1 artifact declares measure/member and no
    family; reading it must not invent family law, so it stays a v1 read and the v2 reader never
    touches it. If this ever fails, something is inferring analytical law from an artifact that does
    not carry it — the exact defect v2 exists to remove."""
    raw = json.loads(V1.read_text(encoding="utf-8"))
    kinds = {d["kind"] for d in raw["logical"]["declarations"]}
    assert "family" not in kinds and {"measure", "member"} <= kinds
    art = parse_publication_artifact(raw)
    assert art.major == 1
    assert {d["kind"] for d in art.logical["declarations"]} == kinds     # carried, not transformed


def test_a_v1_artifact_RELABELLED_v2_is_refused_rather_than_read():
    """THE SHIM CONTROL. Renaming the version does not make a v1 artifact a v2 one: read by the v2
    contract, its `measure` declaration is a retired kind and it refuses. This is the failure mode
    worth pinning — a deployment that edits one string to reach the successor path would otherwise
    get its legacy ontology read as governed law."""
    raw = json.loads(V1.read_text(encoding="utf-8"))
    raw["publication_format_version"] = "2.0"
    with pytest.raises(PublicationArtifactInvalid) as e:
        parse_publication_artifact(raw)
    assert "`measure` is retired" in str(e.value)


def test_the_import_disjointness_that_made_this_uncheckable_in_process_still_holds():
    """Unchanged from the original file. The reason a producer/consumer comparison test cannot be
    written for this constant: `columna-server` may not import `manifold_agent`."""
    import sys

    import columna_server.registry                                       # noqa: F401
    assert "manifold_agent" not in sys.modules

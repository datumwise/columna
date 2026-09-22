"""
test_native_v3_reader.py — C1's stop-gate, witnessed.

    *"the shipped native fixture parses, its geometry is derived, all four currency claims
    verify, and a tampered constitution refuses."*
        — native_v3_consumer_recon_v0_1.md §13, C1

Nothing here imports `manifold_agent`, `columna_server` or `columna_platform`. The fixture is the
artifact; the artifact is the contract.
"""
import copy
import json
import os

import pytest

from columna_core.governed.native import (
    BOUND,
    FCF1,
    FCF2,
    NativePublicationRefusal,
    UNBOUND,
    Anchor,
    human_obligations,
    load_native_publication,
    outstanding_obligations,
    parse_native_publication,
)

_FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "fixtures_v3", "native-v3-publication.json")


@pytest.fixture
def raw():
    with open(_FIXTURE, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture
def pub(raw):
    return parse_native_publication(raw)


# ── stop-gate 1 · the shipped native fixture parses ──────────────────────────────────────────────
def test_the_shipped_native_fixture_parses(pub):
    assert (pub.manifold_id, pub.version, pub.format_version) == ("harbour", "1.0.0", "3.0")
    assert [u.name for u in pub.universes] == ["harbour"]
    assert [f.name for f in pub.families] == ["berthings", "moorings"]
    assert pub.published_by == "harbour steward"


def test_the_constitution_is_visible_not_discarded(pub):
    """The measured v2 failure, inverted: under the v2 reader this universe reports 'a universe
    stating no law' from an artifact carrying all of it."""
    c = pub.universe("harbour").constitution
    assert c.designation == "the harbour's berthing world"
    assert sorted(c.references) == ["berth", "day"]
    assert c.ground == "vessel_berthing"
    assert c.qualification.startswith("every berthing")
    assert [p.reference for p in c.premises] == ["vessel_berthing"]
    assert dict(c.determination)["day"].endswith("boundary 04:00 local")


def test_load_from_disk(pub):
    assert load_native_publication(_FIXTURE) == pub


# ── stop-gate 2 · the geometry is DERIVED ────────────────────────────────────────────────────────
def test_geometry_is_computed_from_the_constitution(pub):
    u = pub.universe("harbour")
    assert u.coordinates == ("berth", "day")
    assert u.root_anchor == Anchor("harbour", frozenset({"berth", "day"}))   # R_U, a theorem
    assert u.scalar_anchor.is_scalar and not u.scalar_anchor.constituents    # {}
    assert {k: sorted(v.constituents) for k, v in u.constituent_anchors.items()} == {
        "berth": ["berth"], "day": ["day"]}


def test_refinement_is_containment_and_projection_is_difference(pub):
    u = pub.universe("harbour")
    berthing_at, by_berth = u.denote("berthing_at"), u.denote("by_berth")
    assert berthing_at.refines(by_berth)
    assert not by_berth.refines(berthing_at)
    assert berthing_at.projection_forgets(by_berth) == frozenset({"day"})
    assert u.constituent_anchor("berth").union(u.constituent_anchor("day")) == berthing_at


def test_a_projection_that_would_ACQUIRE_a_constituent_refuses(pub):
    u = pub.universe("harbour")
    with pytest.raises(NativePublicationRefusal, match="reached by forgetting"):
        u.denote("by_berth").projection_forgets(u.denote("berthing_at"))


def test_synonyms_are_one_anchor(pub):
    """Ruling 11 arrives on the consumer side as a SIMPLIFICATION: many tokens may denote one
    anchor, so the v2 refusal 'this profile will not choose between two governed anchors' has
    nothing left to be ambiguous about."""
    u = pub.universe("harbour")
    assert u.denote("berthing_at") == u.denote("berth_day")
    assert u.synonyms_of(u.denote("berthing_at")) == ("berth_day", "berthing_at")
    assert u.denote("not_a_token") is None


def test_no_place_exists_from_which_two_universes_anchors_are_both_visible(pub):
    u = pub.universe("harbour")
    elsewhere = Anchor("other_world", frozenset({"berth"}))
    assert u.constituent_anchor("berth") != elsewhere
    with pytest.raises(NativePublicationRefusal, match="two different universes"):
        u.constituent_anchor("berth").refines(elsewhere)


def test_a_request_coordinate_set_IS_the_anchor(pub):
    u = pub.universe("harbour")
    assert u.anchor(["berth", "day"]) == u.denote("berthing_at")
    with pytest.raises(NativePublicationRefusal, match="do not resolve as constituents"):
        u.anchor(["berth", "vessel"])


# ── F → U → A ────────────────────────────────────────────────────────────────────────────────────
def test_contextual_resolution(pub):
    for reference in ("berthings", "moorings"):
        r = pub.resolve(reference)
        assert r.universe.name == "harbour"
        assert sorted(r.anchor.constituents) == ["berth", "day"]
    assert pub.resolve("fam_Nq4WfR8kPxDvZc2TmLbJhY").family.name == "berthings"


# ── stop-gate 3 · all four currency claims verify ────────────────────────────────────────────────
def test_all_four_currency_claims_verify(pub):
    report = pub.currency()
    by_claim = {}
    for c in report:
        by_claim.setdefault(c.claim.split()[0], []).append(c.verdict)
    assert by_claim["elf-2"] == ["CURRENT"]
    assert by_claim["F4"] == ["COVERED"]
    assert by_claim["U-authority"] == [BOUND, UNBOUND]
    assert by_claim["fcf-2"] == ["CURRENT"]        # berthings
    assert by_claim["fcf-1"] == ["CURRENT"]        # moorings, UNBOUND and lawfully so
    assert len(report) == 6


def test_elf2_recomputes_from_the_carried_constitution(pub):
    u = pub.universe("harbour")
    assert u.constitution.fingerprint() == u.attestation.fingerprint
    assert u.attestation.fingerprint.startswith("elf-2:f077c0e15f4af4ff")


def test_f4_coverage_is_re_derived_not_trusted(pub):
    u = pub.universe("harbour")
    assert human_obligations(u.constitution) == (
        "determination_is_correct",
        "domain_suffices_to_individuate",
        "no_constitutive_content_elsewhere",
        "qualification_is_over_occurrences_not_rows",
        "qualification_is_the_whole_qualification",
        "subject_individuated_independently_of_any_carrier",
    )
    assert outstanding_obligations(u.constitution, u.conformance) == ()


def test_the_family_schemes_are_state_relative(pub):
    from columna_core.governed.native import expected_family_scheme
    u = pub.universe("harbour")
    assert expected_family_scheme(pub.family("berthings"), u) == FCF2
    assert expected_family_scheme(pub.family("moorings"), u) == FCF1


def test_an_unbound_fcf1_family_is_lawful_and_its_absence_is_legible(pub):
    """Ruled 2026-09-21: an UNBOUND fcf-1 family may exist in a native-v3 artifact, and absence of
    a binding must never be read as BOUND or as equivalent standing."""
    assert pub.unbound_families == ("fam_Td6JhV2yQnWsEr9BkXpLcM",)
    assert pub.family("moorings").binding is None
    assert pub.family("berthings").binding.universe_authority == (
        pub.universe("harbour").attestation.fingerprint)


# ── stop-gate 4 · a tampered constitution refuses ────────────────────────────────────────────────
@pytest.mark.parametrize("path,value", [
    (("constitution", "law", "qualification"), "every berthing anyone recorded"),
    (("constitution", "law", "determination", "day"), "the calendar day of the moment"),
    (("constitution", "individuation", "constituents", 0, "domain", "equality"), "any berth"),
    (("constitution", "premises", 0, "individuation"), "one row in the berthing table"),
])
def test_a_tampered_constitution_refuses(raw, path, value):
    """The attestation no longer covers the law — and the reader says exactly that, rather than
    accepting the bytes and serving a world nobody ratified."""
    d = copy.deepcopy(raw)
    node = d["declarations"][0]
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    with pytest.raises(NativePublicationRefusal, match="attestation does not cover this law"):
        parse_native_publication(d)


def test_re_wording_the_world_designation_does_NOT_stale_the_attestation(raw):
    """F1 is the SUBJECT of the attestation, not one of the premises that determines its
    population — so a re-wording must not stale it."""
    d = copy.deepcopy(raw)
    d["declarations"][0]["constitution"]["identity"]["designation"] = "the harbour's world"
    assert parse_native_publication(d).universe("harbour").constitution.designation == (
        "the harbour's world")


def test_reordering_constituents_and_premises_does_NOT_stale_the_attestation(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["constitution"]["individuation"]["constituents"].reverse()
    parse_native_publication(d)


def test_a_tampered_family_body_refuses(raw):
    d = copy.deepcopy(raw)
    d["declarations"][1]["body"]["participation"] = "every berthing anyone recorded"
    with pytest.raises(NativePublicationRefusal,
                       match="authority does not cover this family's constitution"):
        parse_native_publication(d)


def test_an_uncovered_human_obligation_refuses(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["constitution_conformance"]["obligations"].remove(
        "qualification_is_over_occurrences_not_rows")
    with pytest.raises(NativePublicationRefusal, match="does not cover 1 human-judged"):
        parse_native_publication(d)


def test_a_binding_citing_another_worlds_authority_refuses(raw):
    d = copy.deepcopy(raw)
    d["declarations"][1]["universe_authority_binding"]["universe_authority"] = "elf-2:" + "0" * 64
    with pytest.raises(NativePublicationRefusal, match="does not cover the world published"):
        parse_native_publication(d)


# ── version discipline (N9) ──────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("version,reason", [
    ("2.0", "format v2 artifact"),
    ("1.0", "format v1 artifact"),
    ("4.0", "has major 4"),
    ("3", "states a bare major"),
    ("3.1", "does not explicitly understand"),
    ("three.oh", "expected 'MAJOR.MINOR'"),
])
def test_two_version_mechanisms_two_refusals(raw, version, reason):
    d = copy.deepcopy(raw)
    d["publication_format_version"] = version
    with pytest.raises(NativePublicationRefusal, match=reason):
        parse_native_publication(d)


def test_relabelling_a_v2_artifact_as_v3_is_not_a_path_in(raw):
    """Ruling 5's converse. The v2 reader's measured permissiveness is not exploited in either
    direction: a v2-shaped artifact wearing a v3 label is refused on its SHAPE, not waved through
    because its version string now sorts into this reader's range."""
    d = {"publication_format_version": "3.0", "ref": raw["ref"], "published": raw["published"],
         "logical": {"declarations": raw["declarations"]}}
    with pytest.raises(NativePublicationRefusal, match="unrecognised key"):
        parse_native_publication(d)


# ── consume or refuse, at the ENVELOPE — the site v2 does not enforce ────────────────────────────
def test_an_unrecognised_declaration_level_key_refuses(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["basis"] = "events"
    with pytest.raises(NativePublicationRefusal, match=r"unrecognised key\(s\) \['basis'\]"):
        parse_native_publication(d)


def test_a_legacy_universe_body_refuses_by_name(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["body"] = {"anchor": "berthing_at", "basis": "events"}
    with pytest.raises(NativePublicationRefusal,
                       match=r"carries a `body`, holding legacy universe-law"):
        parse_native_publication(d)


def test_an_anchor_declaration_has_no_referent_here(raw):
    d = copy.deepcopy(raw)
    d["declarations"].append({"kind": "anchor", "name": "berthing_at",
                              "body": {"universe": "harbour", "components": ["berth", "day"]}})
    with pytest.raises(NativePublicationRefusal, match="structurally unwritable as a declaration"):
        parse_native_publication(d)


def test_an_open_individuation_has_no_geometry_to_derive(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["constitution"]["individuation"]["closed"] = False
    with pytest.raises(NativePublicationRefusal, match="not asserted CLOSED"):
        parse_native_publication(d)


def test_an_unadmitted_premise_form_refuses_with_its_jurisdiction_named(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["constitution"]["premises"].append(
        {"premise": "governed_artifact", "reference": "operating_calendar", "version": "2026.4",
         "population_claim": "every operating day"})
    with pytest.raises(NativePublicationRefusal, match="NOT YET ADMITTED"):
        parse_native_publication(d)


def test_a_dangling_denotation_is_an_artifact_defect(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["case_s_denotations"]["by_vessel"] = ["vessel"]
    with pytest.raises(NativePublicationRefusal, match="do not resolve against this universe"):
        parse_native_publication(d)


def test_a_family_whose_anchor_token_denotes_nothing_refuses(raw):
    d = copy.deepcopy(raw)
    d["declarations"][1]["body"]["constitutive_anchor"] = "by_vessel"
    with pytest.raises(NativePublicationRefusal, match="denotes no Case-S anchor"):
        parse_native_publication(d)


def test_an_elf1_attestation_is_never_authority_over_a_constitution(raw):
    d = copy.deepcopy(raw)
    d["declarations"][0]["existence_law_ratification"]["fingerprint_version"] = "elf-1"
    with pytest.raises(NativePublicationRefusal, match="never authority over a constitution"):
        parse_native_publication(d)


def test_two_families_under_one_canonical_reference_refuse(raw):
    d = copy.deepcopy(raw)
    d["declarations"][2]["body"]["aliases"] = ["berthings"]
    with pytest.raises(NativePublicationRefusal, match="resolves to two families"):
        parse_native_publication(d)


# ── the disjointness that matters ────────────────────────────────────────────────────────────────
def test_the_native_reader_imports_nothing_outside_governed():
    """C1 is the reader and nothing else — no serving, no Platform, no engine, and never the
    producer. Read off the module's IMPORT STATEMENTS, so prose about the producer is free and a
    dependency on it is not."""
    import ast

    import columna_core.governed.native as native

    tree = ast.parse(open(native.__file__, encoding="utf-8").read())
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    assert imported == {"__future__", "hashlib", "json", "dataclasses", "typing"}, (
        f"the native reader reached beyond the stdlib: {sorted(imported)}")

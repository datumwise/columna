"""
test_native_c3_identity.py — C3's stop-gate, witnessed.

    *"two synonym tokens yield one identity; two universes carrying one token do not collide;
    plan and run report the same location."*
        — native_v3_consumer_recon_v0_1.md §13, C3

Three claims, and the third is the one the recon says must be settled BEFORE a native anchor
representation is chosen, *"or the choice will bake it in"*. So the legacy divergence is MEASURED
here as a control — not asserted from the docstring — and then shown to be unstatable natively.

Nothing here executes, serves, or touches material. C3 resolves a request; it does not answer one.
"""
from __future__ import annotations

import copy
import json
import pathlib

import pytest
from columna_core.envelope import parse_statement
from columna_core.governed.native import Anchor, parse_native_publication
from columna_core.governed.publication import parse_publication
from columna_core.governed.resolve import resolve_all

from columna_platform import native_request as nrq
from columna_platform import request as rq
from columna_platform import serving
from columna_platform.refusals import UnsupportedByThisProfile, WantOfLaw
from columna_platform.state import AnalyticalIdentity, RetainedStateStore

_CORE = pathlib.Path(__file__).parents[2] / "columna-core" / "tests"
V3_ARTIFACT = _CORE / "fixtures_v3" / "native-v3-publication.json"
V2_ARTIFACT = _CORE / "fixtures_v2" / "lighthouse-v2-publication.json"

BERTHINGS = "fam_Nq4WfR8kPxDvZc2TmLbJhY"
MOORINGS = "fam_Td6JhV2yQnWsEr9BkXpLcM"


@pytest.fixture(scope="module")
def raw():
    return json.loads(V3_ARTIFACT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def pub(raw):
    return parse_native_publication(raw)


# ══ 1 · TWO SYNONYM TOKENS YIELD ONE IDENTITY ════════════════════════════════════════════════════
def test_the_two_governed_tokens_denote_one_anchor(pub):
    u = pub.universe("harbour")
    assert u.denote("berthing_at") == u.denote("berth_day") == Anchor("harbour", frozenset({"berth", "day"}))
    assert u.synonyms_of(u.denote("berthing_at")) == ("berth_day", "berthing_at")


def test_one_identity_whichever_synonym_constituted_the_family(pub, raw):
    """The family's `constitutive_anchor` is a TOKEN, and re-spelling it to a governed synonym must
    not mint a second analytical identity. Re-spelled, the artifact still resolves to the same `A`
    — and therefore to the same identity."""
    respelled = copy.deepcopy(raw)
    respelled["declarations"][1]["body"]["constitutive_anchor"] = "berth_day"
    # the fcf-2 payload carries the RESOLVED structure, not the spelling, so the digest is unmoved
    other = parse_native_publication(respelled)

    stmt = parse_statement("SELECT berthings AT {berth * day}")
    a = nrq.resolve(pub, stmt).identity
    b = nrq.resolve(other, stmt).identity
    assert a == b
    assert a.anchor == Anchor("harbour", frozenset({"berth", "day"}))


def test_with_A_as_a_raw_STRING_the_same_two_tokens_split_one_identity():
    """The counterfactual, stated as a test so the shape choice is witnessed rather than argued.

    This is what the v1/v2 reading does to a native publication: two governed synonyms for one
    anchor become two different states of the same analytical thing — and `AnalyticalIdentity` is
    the retained-state retrieval key, the fold-eligibility key and the eviction key."""
    as_string = (AnalyticalIdentity(BERTHINGS, "berthing_at"),
                 AnalyticalIdentity(BERTHINGS, "berth_day"))
    assert as_string[0] != as_string[1]                      # one anchor, two identities — the defect
    A = Anchor("harbour", frozenset({"berth", "day"}))
    assert AnalyticalIdentity(BERTHINGS, A) == AnalyticalIdentity(BERTHINGS, A)


def test_the_request_coordinate_set_IS_the_anchor_so_nothing_is_ambiguous(pub):
    """The v2 resolver refuses when two declared anchors carry one component set — a refusal marked
    `# pragma: no cover` because the case *"cannot be built from a publication this proof is
    authorized to write."* Here that publication is the ordinary one, and the refusal has no
    subject: there is no name to look up."""
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {berth * day}"))
    assert req.identity.anchor == pub.universe("harbour").denote("berthing_at")
    assert nrq.frame_location(req.location) == ("berth", "day")


# ══ 2 · TWO UNIVERSES CARRYING ONE TOKEN DO NOT COLLIDE ══════════════════════════════════════════
def _two_universe_artifact(raw) -> dict:
    """A second world beside `harbour`, carrying the SAME token `berthing_at` over constituents of
    the same names — the collision case, which the shipped one-universe fixture cannot express.

    **DERIVED, AND ITS DIGESTS ARE MINTED WITH THE CONSUMER'S OWN DERIVATION.** That is stated
    plainly because of what it does and does not witness: this fixture witnesses UNIVERSE SCOPING,
    and it cannot witness canonicalization agreement with the producer — only the producer-shipped
    artifact does that (OF-59). Minting them any other way would have been a fourth implementation
    of the payload contract, which is worse.
    """
    from columna_core.governed.native import IDENTITY_KEYS, _digest, _read_constitution

    d = copy.deepcopy(raw)
    quay = copy.deepcopy(d["declarations"][0])
    quay["name"] = "quay"
    quay["constitution"]["identity"]["designation"] = "the quay's berthing world"
    quay["constitution"]["law"]["qualification"] = "every berthing the quay master accepted"
    quay["existence_law_ratification"]["fingerprint"] = (
        _read_constitution("quay", quay["constitution"]).fingerprint())

    fam = copy.deepcopy(d["declarations"][2])          # `moorings`: fcf-1, UNBOUND
    fam["name"] = "quayings"
    fam["body"]["canonical_reference"] = "quayings"
    fam["body"]["family_id"] = "fam_QuAyZz1234567890abcd"
    fam["body"]["universe"] = "quay"
    fam["body"]["participation"] = "every berthing the quay master accepted"
    fam["family_constitution_authority"]["constitution_fingerprint"] = "fcf-1:" + _digest(
        {"_scheme": "fcf-1",
         **{k: fam["body"][k] for k in sorted(IDENTITY_KEYS) if k in fam["body"]}})

    d["declarations"].extend([quay, fam])
    return d


@pytest.fixture(scope="module")
def two_worlds(raw):
    return parse_native_publication(_two_universe_artifact(raw))


def test_the_fixture_is_the_collision_case(two_worlds):
    """Both worlds carry the token `berthing_at`, and both carry constituents spelled `berth` and
    `day`. Under a publication-global anchor namespace these would be one anchor."""
    for name in ("harbour", "quay"):
        u = two_worlds.universe(name)
        assert u.coordinates == ("berth", "day")
        assert "berthing_at" in u.denotation_table


def test_one_token_in_two_worlds_denotes_two_different_anchors(two_worlds):
    a = two_worlds.universe("harbour").denote("berthing_at")
    b = two_worlds.universe("quay").denote("berthing_at")
    assert a != b
    assert a.constituents == b.constituents          # identical SETS, different worlds
    assert (a.universe, b.universe) == ("harbour", "quay")


def test_the_two_worlds_anchors_cannot_even_be_COMPARED(two_worlds):
    """Universe scoping is not a rule someone applies here — it is the only shape available."""
    from columna_core.governed.native import NativePublicationRefusal
    a = two_worlds.universe("harbour").denote("berthing_at")
    b = two_worlds.universe("quay").denote("berthing_at")
    with pytest.raises(NativePublicationRefusal, match="two different universes"):
        a.refines(b)


def test_two_identities_across_two_worlds_do_not_collide(two_worlds):
    here = nrq.resolve(two_worlds, parse_statement("SELECT berthings AT {berth * day}")).identity
    there = nrq.resolve(two_worlds, parse_statement("SELECT quayings AT {berth * day}")).identity
    assert here != there
    assert here.family_id != there.family_id         # §7's argument: F fixes U…
    assert here.anchor != there.anchor               # …and the anchor carries it anyway


def test_a_constituent_of_the_OTHER_world_does_not_resolve_here(two_worlds):
    """There is no place from which two universes' constituents are both visible."""
    d = _two_universe_artifact(json.loads(V3_ARTIFACT.read_text(encoding="utf-8")))
    for decl in d["declarations"]:
        if decl.get("name") == "quay":
            decl["constitution"]["individuation"]["constituents"][1]["reference"] = "tide"
            decl["constitution"]["law"]["determination"]["tide"] = (
                decl["constitution"]["law"]["determination"].pop("day"))
            decl["case_s_denotations"] = {"berthing_at": ["berth", "tide"]}
            from columna_core.governed.native import _read_constitution
            decl["existence_law_ratification"]["fingerprint"] = (
                _read_constitution("quay", decl["constitution"]).fingerprint())
    pub = parse_native_publication(d)
    with pytest.raises(WantOfLaw, match=r"\['tide'\] do not resolve as constituents"):
        nrq.resolve(pub, parse_statement("SELECT berthings AT {berth * tide}"))


# ══ 3 · PLAN AND RUN REPORT THE SAME LOCATION ════════════════════════════════════════════════════
def test_the_LEGACY_pair_diverges_and_here_is_the_measurement():
    """THE CONTROL. Not quoted from the reconnaissance — run.

    `plan_result` reports the STRUCTURAL REQUEST; `decide_result` reports the NOMINAL LABEL. One
    lawful request, two answers to *where does this value stand*. Nothing here repairs it: the v2
    path is untouched, and this test exists so the native claim below is a comparison rather than
    an assertion."""
    pub = parse_publication(json.loads(V2_ARTIFACT.read_text(encoding="utf-8")))
    views = resolve_all(pub)
    stmt = parse_statement("SELECT revenue AT {store * day}")
    req = rq.resolve(pub, stmt)

    plan = serving.plan_result(pub, views, stmt)
    run = serving.decide_result(views[req.identity.family_id], RetainedStateStore(),
                                req.identity, column=req.column_name)
    assert plan.anchor == ("store", "day")            # the structural request
    assert run.anchor == ("sale_at",)                 # the nominal label
    assert plan.anchor != run.anchor                  # still live, and forbidden


def test_natively_the_two_candidate_representations_are_ONE_OBJECT(pub):
    """The divergence is not repaired natively — it becomes unstatable.

    The v2 pair has two expressions of the location: `tuple(statement.anchor)` on the pre-flight
    side and `(identity.anchor,)` on the execution side. Natively the first IS the anchor and the
    second does not exist, so both callers reach the same object through the same function."""
    stmt = parse_statement("SELECT berthings AT {berth * day}")
    req = nrq.resolve(pub, stmt)

    pre_flight_side = nrq.frame_location(req.location)        # what a plan would report
    execution_side = nrq.frame_location(req.identity.anchor)  # what a run would report
    assert pre_flight_side == execution_side == ("berth", "day")
    assert req.location is req.identity.anchor                # ONE object, not two equal ones


def test_the_location_is_never_a_NAME(pub):
    """Reporting one of two governed synonyms would present a convention as the location."""
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {berth * day}"))
    assert "berthing_at" not in nrq.frame_location(req.location)
    assert "berth_day" not in nrq.frame_location(req.location)


def test_the_request_coordinate_order_does_not_reach_the_location(pub):
    a = nrq.resolve(pub, parse_statement("SELECT berthings AT {berth * day}"))
    b = nrq.resolve(pub, parse_statement("SELECT berthings AT {day * berth}"))
    assert a.identity == b.identity
    assert nrq.frame_location(a.location) == nrq.frame_location(b.location) == ("berth", "day")


# ══ THE MOVEMENT BOUNDARY — observed, not crossed ════════════════════════════════════════════════
def test_a_coarser_ask_resolves_GEOMETRICALLY_and_carries_its_target(pub):
    """Ruling 3's distinction, and **C4 moved the second half of it out of resolution.**

    As C3 first shipped, a coarser ask was REFUSED here for want of governed movement standing. The
    refusal said the right thing in the wrong place: resolution answers *what is being asked for*,
    and standing is decided against `Law(F)`, which this module may not see — and refusing here left
    the standing question unreachable. So resolution now concludes only what geometry establishes:
    the target location exists, and `target` carries it. The refusal lives in
    `native_law.assert_answerable` and is witnessed in `test_native_c4_answerability.py`."""
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {berth}"))
    assert req.is_moving
    assert sorted(req.target.constituents) == ["berth"]
    assert req.identity.anchor == pub.universe("harbour").denote("berthing_at")
    # the projection is computable, and exactly what it forgets is a fact of geometry
    assert req.identity.anchor.projection_forgets(req.target) == frozenset({"day"})


def test_the_grand_total_frame_is_movement_too(pub):
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {}"))
    assert req.is_moving and req.target.is_scalar
    assert req.identity.anchor.projection_forgets(req.target) == frozenset({"berth", "day"})


def test_a_FINER_ask_is_not_a_movement_awaiting_a_licence(pub):
    """A coarser location is reached by forgetting, never by acquiring — so there is nothing here
    for a licence to license, and saying 'unlicensed movement' would name the wrong remedy."""
    d = json.loads(V3_ARTIFACT.read_text(encoding="utf-8"))
    d["declarations"][1]["body"]["constitutive_anchor"] = "by_berth"
    shifted = parse_native_publication(_refingerprint_family(d, 1))
    with pytest.raises(WantOfLaw, match="reached by FORGETTING"):
        nrq.resolve(shifted, parse_statement("SELECT berthings AT {berth * day}"))


def _refingerprint_family(d: dict, index: int) -> dict:
    """Re-mint an fcf-2 family authority after editing its body — the fixture-builder note on
    `_two_universe_artifact` applies here too."""
    from columna_core.governed.native import FCF2_IDENTITY_KEYS, _digest
    decl = d["declarations"][index]
    universe = next(x for x in d["declarations"]
                    if x.get("kind") == "universe" and x["name"] == decl["body"]["universe"])
    anchor = sorted(universe["case_s_denotations"][decl["body"]["constitutive_anchor"]])
    payload = {"_scheme": "fcf-2", "_anchor": anchor,
               **{k: decl["body"][k] for k in sorted(FCF2_IDENTITY_KEYS) if k in decl["body"]}}
    decl["family_constitution_authority"]["constitution_fingerprint"] = "fcf-2:" + _digest(payload)
    return d


# ══ WHAT THIS PATH CANNOT REACH ══════════════════════════════════════════════════════════════════
def test_an_unknown_reference_is_not_guessed(pub):
    with pytest.raises(WantOfLaw, match="no governed family answers to the reference"):
        nrq.resolve(pub, parse_statement("SELECT berthing AT {berth * day}"))


def test_a_family_id_is_not_a_way_of_asking(pub):
    """Identity is not a reference. `family()` resolves one for a caller that already holds it;
    a REQUEST may name a canonical reference or a declared alias, and nothing else."""
    assert pub.family(BERTHINGS).name == "berthings"
    assert pub.resolve_reference(BERTHINGS) is None


def test_several_series_is_a_capability_limit_not_a_governed_verdict(pub):
    with pytest.raises(UnsupportedByThisProfile):
        nrq.resolve(pub, parse_statement("SELECT berthings, moorings AT {berth * day}"))


def test_the_native_resolver_reaches_no_legacy_anchor_machinery():
    """The list is worth keeping in a test because each entry is a live temptation. Most are not
    refused on this path — they are unreachable, because a `NativePublication` has none of them."""
    import ast
    import columna_platform.native_request as m

    source = pathlib.Path(m.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    called = {n.func.attr for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    for forbidden in ("declared_anchor_names", "declared_coordinates", "of_kind",
                      "resolve_anchor", "component_realizations"):
        assert forbidden not in called, f"the native resolver called {forbidden!r}"
    imported = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert "columna_platform.anchors" not in imported and ".anchors" not in imported

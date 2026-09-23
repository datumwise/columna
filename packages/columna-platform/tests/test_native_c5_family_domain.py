"""C5 · the primitive-family Case-S domain — **may `F` stand at this resolved location?**

One governed fact is added to the model by this unit and nothing else: the family's prohibited
Case-S constituents, `P_F`. Everything else the rule needs already shipped — the root, the
refinement order, and the set difference that derives what a projection forgets.

The tests are the unit's conformance obligations, in the contract's order.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import columna_platform.native_domain as nd
import columna_platform.native_law as nl
import columna_platform.native_request as nrq
from columna_core.envelope import parse_statement
from columna_core.governed.native import (
    FAMILY_BODY_KEYS,
    NON_IDENTITY_KEYS,
    NativePublicationRefusal,
    expected_family_scheme,
    family_fingerprint,
    parse_native_publication,
)
from columna_core.governed.publication import _FAMILY_KEYS
from columna_core.governed.resolve import (
    C3_EDGE_VALIDITY,
    C3_FAMILY_DOMAIN,
    ESTABLISHED,
    EXPLICIT_NONE,
    UNESTABLISHED,
)
from columna_platform.refusals import OutsideFamilyDomain, WantOfLaw

V3_ARTIFACT = (Path(__file__).resolve().parents[2]
               / "columna-core/tests/fixtures_v3/native-v3-publication.json")
BERTHINGS = "fam_Nq4WfR8kPxDvZc2TmLbJhY"


@pytest.fixture
def raw():
    return json.loads(V3_ARTIFACT.read_text(encoding="utf-8"))


def _berthings(d: dict) -> int:
    return next(i for i, x in enumerate(d["declarations"])
                if x.get("body", {}).get("canonical_reference") == "berthings")


def _with_pf(raw: dict, pf):
    """Set `berthings`' prohibition and return the parsed publication.

    **No refingerprinting.** That is not an oversight — it is obligation 8: `P_F` is outside the
    identity payload, so editing it must leave the family's authority covering its constitution. If
    this helper ever needs to re-mint a fingerprint, R12 has been broken."""
    d = copy.deepcopy(raw)
    i = _berthings(d)
    if pf is None:
        d["declarations"][i]["body"].pop("prohibited_constituents", None)
    else:
        d["declarations"][i]["body"]["prohibited_constituents"] = pf
    return parse_native_publication(d)


def _view_and_req(pub, at: str):
    view = nl.laws_of(pub)[BERTHINGS]
    req = nrq.resolve(pub, parse_statement(f"SELECT berthings AT {{{at}}}"))
    return view, req


# ══ 1 · the split changes no verdict ═════════════════════════════════════════════════════════════
def test_the_shipped_fixture_still_resolves_totally_and_validly(raw):
    pub = parse_native_publication(raw)
    for view in nl.laws_of(pub).values():
        assert view.valid, view.validity_problems
        assert view[C3_FAMILY_DOMAIN].standing == UNESTABLISHED
        assert view[C3_EDGE_VALIDITY].standing == UNESTABLISHED


# ══ 2 · declared-empty is NOT absent — the unit's central distinction ════════════════════════════
def test_an_EMPTY_prohibition_is_ESTABLISHED_and_an_ABSENT_one_is_NOT(raw):
    """**The single thing most likely to be got wrong.** A reader that maps `[]` onto "absent"
    collapses two governed states and re-enacts the family-admission test ToD v7.1 Appendix C.4
    withdrew — admitting on geometry alone, with no family law."""
    absent = nl.laws_of(_with_pf(raw, None))[BERTHINGS][C3_FAMILY_DOMAIN]
    empty = nl.laws_of(_with_pf(raw, []))[BERTHINGS][C3_FAMILY_DOMAIN]
    assert absent.standing == UNESTABLISHED
    assert empty.standing == ESTABLISHED
    assert empty.value == frozenset()


def test_and_they_admit_DIFFERENT_projections(raw):
    """The distinction is not cosmetic: it decides the same ask two ways."""
    for pf, admitted in ((None, False), ([], True)):
        pub = _with_pf(raw, pf)
        view, req = _view_and_req(pub, "berth")          # forgets `day`
        if admitted:
            nd.assert_request_within_domain(view, req)
        else:
            with pytest.raises(WantOfLaw, match="establishes no family-domain law"):
                nd.assert_request_within_domain(view, req)


def test_an_explicit_none_domain_says_so_positively(raw):
    pub = _with_pf(raw, {"none": "this family stands only at its root"})
    view, req = _view_and_req(pub, "berth")
    assert view[C3_FAMILY_DOMAIN].standing == EXPLICIT_NONE
    with pytest.raises(WantOfLaw, match="DECLARED that no off-root"):
        nd.assert_request_within_domain(view, req)


# ══ 3 · the root falls out of the ordinary rule ══════════════════════════════════════════════════
def test_the_ROOT_is_admitted_by_the_ORDINARY_rule_not_by_an_exception(raw):
    """R13: *"Do not retain an implementation shortcut whose semantic justification is merely 'the
    constitutive anchor is automatically allowed' if the ordinary rule can decide it."*

    `Forgotten(A_0 → A_0)` is empty and the empty set meets no prohibition, so the root passes the
    same test as every other candidate — even one prohibiting BOTH of the universe's constituents."""
    pub = _with_pf(raw, ["berth", "day"])
    view, req = _view_and_req(pub, "berth * day")        # the root itself
    assert not req.is_moving
    assert nd.forgotten(req.identity.anchor, req.identity.anchor) == frozenset()
    nd.assert_request_within_domain(view, req)             # admitted, and no exception was taken


# ══ 4 · an irrelevant prohibition is lawful and inert (R14) ══════════════════════════════════════
def test_a_governed_but_IRRELEVANT_prohibition_is_ACCEPTED_and_changes_nothing(raw):
    """R14: a governed constituent the present root cannot lose is lawful and inert — *"do not
    refuse it, warn about it, or derive anything from its irrelevance."*

    `berthings` is rooted at `{berth, day}`, so `day` is losable and `berth` is losable, but a
    projection to `{berth}` forgets only `day`. A prohibition on `berth` is therefore irrelevant to
    THIS projection and must not affect it."""
    plain = _with_pf(raw, [])
    inert = _with_pf(raw, ["berth"])                       # governed, irrelevant to →{berth}

    for pub in (plain, inert):
        view, req = _view_and_req(pub, "berth")
        nd.assert_request_within_domain(view, req)         # identical verdict, both directions


def test_an_UNGOVERNED_reference_still_refuses(raw):
    """The other half of R14: representation and governed references ARE validated."""
    with pytest.raises(NativePublicationRefusal, match="do not resolve as constituents"):
        _with_pf(raw, ["tide"])


def test_the_representation_itself_is_validated(raw):
    with pytest.raises(Exception, match="list of constituent references"):
        _with_pf(raw, "day")
    with pytest.raises(Exception, match="more than once"):
        _with_pf(raw, ["day", "day"])


# ══ 5 · a prohibited projection refuses and NAMES the constituent ════════════════════════════════
def test_a_prohibited_projection_refuses_and_names_the_constituent(raw):
    """**A complete governed judgment, and it gets its own reason** (R16). The location exists, the
    law is established, and the law said no — so this is NOT a want of law."""
    pub = _with_pf(raw, ["day"])
    view, req = _view_and_req(pub, "berth")              # forgets `day` — prohibited
    with pytest.raises(OutsideFamilyDomain) as e:
        nd.assert_request_within_domain(view, req)
    assert "prohibits losing ['day']" in str(e.value)
    assert "may not stand at" in str(e.value)
    assert not isinstance(e.value, WantOfLaw), "a sibling, never a subclass — dispatch is by class"


def test_the_ONLY_reason_minted_is_the_one_where_the_law_ANSWERED(raw):
    """**R15/R16, pinned as a boundary rather than a count.**

    C5 can tell four situations apart. Three of them keep `want_of_law`, because in each the law is
    missing or the theory is unfinished; only the fourth is a complete governed judgment. A test
    that merely counted reason codes would not catch the mistake this guards — emitting
    `outside_family_domain` for a case where no law was ever consulted."""
    # 1 · geometry unreachable — adjudication never reached the law
    pub = _with_pf(raw, ["day"])
    view = nl.laws_of(pub)[BERTHINGS]
    fam = next(f for f in pub.families if f.canonical_reference == "berthings")
    u = pub.universe(fam.universe_reference)
    with pytest.raises(WantOfLaw) as geo:
        nd.assert_within_domain(view, fam, root=u.anchor(["berth"]),
                                target=u.anchor(["berth", "day"]))
    assert not isinstance(geo.value, OutsideFamilyDomain)

    # 2 · the domain law is what is MISSING
    v2, r2 = _view_and_req(_with_pf(raw, None), "berth")
    with pytest.raises(WantOfLaw) as unest:
        nd.assert_request_within_domain(v2, r2)
    assert not isinstance(unest.value, OutsideFamilyDomain)

    # 3 · the law is established and ANSWERED — the one boundary C5 earned
    v3, r3 = _view_and_req(_with_pf(raw, ["day"]), "berth")
    with pytest.raises(OutsideFamilyDomain):
        nd.assert_request_within_domain(v3, r3)


def test_the_new_reason_is_registered_and_is_an_analytical_refuse():
    from columna_core.disclosure import ANALYTICAL, REASON_OUTCOME, REFUSE, UNSUPPORTED
    from columna_platform import serving

    assert REASON_OUTCOME["outside_family_domain"] == (REFUSE, UNSUPPORTED, ANALYTICAL)
    assert serving._REFUSAL_WIRE[OutsideFamilyDomain] == ("outside_family_domain", ())
    # no borrowed remedy: the law answered, so nothing is owed and nothing is offered
    assert serving._REFUSAL_WIRE[OutsideFamilyDomain][1] == ()
    # and the three reasons R16 forbade are untouched by this mint
    for forbidden in ("anchor_spent", "blocked_reduction", "out_of_universe"):
        assert forbidden in REASON_OUTCOME
        assert REASON_OUTCOME[forbidden] != REASON_OUTCOME.get("__absent__")


# ══ 6 · admission is NOT a claim about lawful query admission ════════════════════════════════════
def test_passing_the_domain_condition_claims_nothing_about_the_EDGE(raw):
    """*"This unit establishes the primitive Case-S family-domain predicate, not a universal
    biconditional for complete query validity."* The edge half is untouched and still refuses."""
    pub = _with_pf(raw, [])
    view, req = _view_and_req(pub, "berth")
    nd.assert_request_within_domain(view, req)             # admitted to STAND there
    with pytest.raises(WantOfLaw, match="establishes no positive movement"):
        nl.assert_answerable(view, moving=req.is_moving)   # and the edge still says no


# ══ 7 · a constructed family stops at the characterized fact ═════════════════════════════════════
def test_a_CONSTRUCTED_family_stops_with_the_fact_characterized(raw):
    """The scope gate. No derivation, no propagation, no union, no default."""
    m = nd.CONSTRUCTED_DOMAIN_UNDECIDED
    assert "CONSTRUCTED family" in m.fact
    assert "capability-indexed union is" in m.fact and "NOT the answer" in m.fact
    assert set(vars(m)) == {"fact", "whose", "where"}

    d = copy.deepcopy(raw)
    i = _berthings(d)
    d["declarations"][i]["body"]["formation"] = {
        "kind": "construction",
        "law": {"law": "SUM", "version": "1", "vocabulary": "datumwise.foundation"},
        "operands": ["fam_Td6JhV2yQnWsEr9BkXpLcM"]}
    fam = parse_native_publication(_refingerprint(d, i)).families[i - _first_family(d)]
    assert not nd.family_is_primitive(fam)


# ══ 8 · a domain revision is not a succession; a structural anchor change is ═════════════════════
def test_revising_P_F_does_NOT_change_the_family_fingerprint(raw):
    """R12, and the reason `_with_pf` never re-mints an authority: if this fails, every governed
    domain revision has silently become a family succession."""
    assert "prohibited_constituents" in NON_IDENTITY_KEYS
    base = parse_native_publication(raw)
    for pf in ([], ["day"], ["berth", "day"]):
        pub = _with_pf(raw, pf)                            # parses at all == authority still covers
        for name in ("berthings",):
            a = next(f for f in base.families if f.canonical_reference == name)
            b = next(f for f in pub.families if f.canonical_reference == name)
            ua, ub = base.universe(a.universe_reference), pub.universe(b.universe_reference)
            assert (family_fingerprint(a, ua, expected_family_scheme(a, ua))
                    == family_fingerprint(b, ub, expected_family_scheme(b, ub)))


# ══ 9 · the two key sets still agree ═════════════════════════════════════════════════════════════
def test_the_total_family_body_key_set_is_still_shared_by_both_majors():
    assert FAMILY_BODY_KEYS == _FAMILY_KEYS
    assert "prohibited_constituents" in FAMILY_BODY_KEYS


# ══ 10 · geometry stays geometry ═════════════════════════════════════════════════════════════════
def test_an_UNRESOLVABLE_ask_refuses_identically_whatever_P_F_says(raw):
    """An ask naming something that is not a constituent of this world is settled by the universe,
    before any family law is read — and the family's prohibition cannot change that verdict.

    Note what this fixture CANNOT witness: `berthings` is rooted at `{berth, day}`, which is the
    universe's root anchor, so no location is FINER than its root and the finer-ask branch is
    unreachable from here. That branch is exercised directly against the predicate in
    `test_the_geometry_refusal_inside_the_predicate_says_it_is_not_a_licence`."""
    messages = set()
    for pf in (None, [], ["day"], ["berth", "day"]):
        pub = _with_pf(raw, pf)
        with pytest.raises(WantOfLaw) as e:
            nrq.resolve(pub, parse_statement("SELECT berthings AT {berth * tide}"))
        messages.add(str(e.value))
    assert len(messages) == 1, "the verdict moved with P_F, so a law was consulted"
    assert "do not resolve as constituents" in messages.pop()


def test_the_geometry_refusal_inside_the_predicate_says_it_is_not_a_licence(raw):
    pub = _with_pf(raw, ["day"])
    view = nl.laws_of(pub)[BERTHINGS]
    fam = next(f for f in pub.families if f.canonical_reference == "berthings")
    u = pub.universe(fam.universe_reference)
    root, finer = u.anchor(["berth"]), u.anchor(["berth", "day"])
    with pytest.raises(WantOfLaw) as e:
        nd.assert_within_domain(view, fam, root=root, target=finer)
    assert "NOT a missing licence" in str(e.value)
    assert "none was consulted" in str(e.value)


# ══ helpers ══════════════════════════════════════════════════════════════════════════════════════
def _first_family(d: dict) -> int:
    return next(i for i, x in enumerate(d["declarations"]) if "formation" in x.get("body", {}))


def _refingerprint(d: dict, index: int) -> dict:
    from columna_core.governed.native import FCF2_IDENTITY_KEYS, _digest
    decl = d["declarations"][index]
    universe = next(x for x in d["declarations"]
                    if x.get("kind") == "universe" and x["name"] == decl["body"]["universe"])
    anchor = sorted(universe["case_s_denotations"][decl["body"]["constitutive_anchor"]])
    payload = {"_scheme": "fcf-2", "_anchor": anchor,
               **{k: decl["body"][k] for k in sorted(FCF2_IDENTITY_KEYS) if k in decl["body"]}}
    decl["family_constitution_authority"]["constitution_fingerprint"] = "fcf-2:" + _digest(payload)
    return d

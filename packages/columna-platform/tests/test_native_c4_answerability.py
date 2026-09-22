"""
test_native_c4_answerability.py — C4, witnessed.

C3 ended with `F @ A` resolved from a native publication using no family law at all. C4 follows the
request into the next question, which is a different one:

    C3 · WHICH analytical point is being asked for
    C4 · MAY that point be answered, and from what

The headline result, measured here rather than argued: **`Law(F)` resolves totally for a native
family from its own declared clauses, with no anchor model on either side** — and `Law(F)` is where
the answerability decision is finally made.

Nothing here executes, serves, or touches material. C4 decides; it does not answer.
"""
from __future__ import annotations

import copy
import json
import pathlib

import pytest
from columna_core.envelope import parse_statement
from columna_core.governed.native import parse_native_publication
from columna_core.governed.publication import parse_family_declaration, parse_publication
from columna_core.governed.resolve import (
    C3_DOMAIN_MOVEMENT,
    C3_EDGE_VALIDITY,
    C3_FAMILY_DOMAIN,
    C7_SUFFICIENT_STATE,
    ESTABLISHED,
    RESPONSIBILITIES,
    UNESTABLISHED,
    resolve_all,
)

from columna_platform import native_law as nl
from columna_platform import native_request as nrq
from columna_platform.refusals import WantOfLaw

_CORE = pathlib.Path(__file__).parents[2] / "columna-core" / "tests"
V3_ARTIFACT = _CORE / "fixtures_v3" / "native-v3-publication.json"
V2_ARTIFACT = _CORE / "fixtures_v2" / "lighthouse-v2-publication.json"

BERTHINGS = "fam_Nq4WfR8kPxDvZc2TmLbJhY"


@pytest.fixture(scope="module")
def raw():
    return json.loads(V3_ARTIFACT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def pub(raw):
    return parse_native_publication(raw)


@pytest.fixture(scope="module")
def views(pub):
    return nl.laws_of(pub)


# ══ 1 · LAW(F) RESOLVES TOTALLY FOR A NATIVE FAMILY ══════════════════════════════════════════════
def test_every_responsibility_is_settled_for_every_native_family(views):
    """Totality. Since the C3 split the view also carries the retained pre-split combined entry,
    asserted BY NAME rather than tolerated by a loosened comparison — an unnamed extra entry is
    exactly what this assertion exists to catch."""
    for view in views.values():
        assert set(view.entries) - set(RESPONSIBILITIES) == {C3_DOMAIN_MOVEMENT}
        assert set(RESPONSIBILITIES) <= set(view.entries)
        assert view.valid, view.validity_problems


def test_the_family_clause_contract_is_the_SAME_SET_in_both_majors(pub):
    """The measurement the reuse rests on. Not 'they look similar' — the same keys, and every one
    of them meaning the same thing."""
    from columna_core.governed.native import FAMILY_BODY_KEYS
    from columna_core.governed.publication import _FAMILY_KEYS
    assert FAMILY_BODY_KEYS == _FAMILY_KEYS


def test_a_native_family_body_parses_as_declared_clauses_verbatim(pub):
    fam = pub.family("berthings")
    declared = parse_family_declaration(fam.name, dict(fam.body))
    assert declared.family_id == BERTHINGS
    assert declared.formation.kind == "primitive"
    assert declared.value_domain == "integer"
    assert str(declared.continuation) == "datumwise.foundation/1#SUM"


def test_resolution_consults_no_anchor_model(views):
    """The nine responsibilities are a family's statement about ITSELF. Witnessed by what resolving
    them needs: nothing that names an anchor, a declaration, a level, a basis or a universe body."""
    import ast
    import columna_platform.native_law as m

    tree = ast.parse(pathlib.Path(m.__file__).read_text(encoding="utf-8"))
    imported = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert ".anchors" not in imported and ".movement" not in imported
    assert views[BERTHINGS][C7_SUFFICIENT_STATE].standing == ESTABLISHED


def test_law_resolution_asks_a_publication_for_exactly_one_thing(pub):
    """`resolve_family` needs a parent lookup by `family_id` — §3.7's lineage edge — and nothing
    publication-shaped. Witnessed by handing it a holder that can do only that."""
    lookup = nl._ParentLookup({})
    assert lookup.family("anything") is None
    public = {n for n in vars(type(lookup)) if not n.startswith("_")}
    assert public == {"family"}, f"the parent lookup grew a second capability: {sorted(public)}"


# ══ 2 · THE DECISION, AND THE ORDER IT IS MADE IN ════════════════════════════════════════════════
def test_a_family_at_its_constitutive_anchor_is_answerable(pub, views):
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {berth * day}"))
    assert req.is_moving is False
    nl.assert_answerable(views[req.identity.family_id], moving=req.is_moving)   # no refusal


def test_the_constitutive_anchor_raises_no_admission_question(views):
    """C3 is UNESTABLISHED for every family in the fixture, and the non-moving ask is answerable
    anyway. *Constitutive* is what it means for the family to be established there."""
    assert views[BERTHINGS][C3_EDGE_VALIDITY].standing == UNESTABLISHED
    nl.assert_answerable(views[BERTHINGS], moving=False)


def test_a_family_with_no_sufficient_state_basis_is_answerable_NOWHERE(pub, raw):
    """A primitive family that declares no continuation has no governing law to entail a basis. The
    refusal says it is a defect of the family's own law, not of the ask."""
    d = copy.deepcopy(raw)
    del d["declarations"][1]["body"]["continuation"]
    other = parse_native_publication(_refingerprint_fcf2(d, 1))
    view = nl.laws_of(other)[BERTHINGS]
    assert view[C7_SUFFICIENT_STATE].standing == UNESTABLISHED
    for moving in (False, True):
        with pytest.raises(WantOfLaw, match="no established sufficient-state basis"):
            nl.assert_answerable(view, moving=moving)


def test_C7_is_asked_before_movement_and_the_reason_is_the_remedy(pub, raw):
    """Both refusals are true for a basis-less family asked off its anchor. The one surfaced is the
    upstream one: licensing a movement would not make an unanswerable family answerable."""
    d = copy.deepcopy(raw)
    del d["declarations"][1]["body"]["continuation"]
    view = nl.laws_of(parse_native_publication(_refingerprint_fcf2(d, 1)))[BERTHINGS]
    with pytest.raises(WantOfLaw) as e:
        nl.assert_answerable(view, moving=True)
    assert "sufficient-state basis" in str(e.value)
    assert "movement" not in str(e.value)


# ══ 3 · THE MOVEMENT ASK NOW REACHES THE DECISION ════════════════════════════════════════════════
def test_a_coarser_ask_RESOLVES_and_carries_its_target(pub):
    """C4's layering correction. C3 refused this during resolution, which said the right thing in
    the wrong place and left the standing question unreachable."""
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {berth}"))
    assert req.is_moving
    assert sorted(req.target.constituents) == ["berth"]
    assert req.identity.anchor == pub.universe("harbour").denote("berthing_at")   # unmoved


def test_the_grand_total_frame_resolves_as_a_movement_to_the_scalar_anchor(pub):
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {}"))
    assert req.is_moving and req.target.is_scalar


def test_a_NON_PROJECTABLE_ask_still_refuses_at_RESOLUTION(pub, raw):
    """Different again, and deliberately not described as a missing licence: if the target cannot be
    obtained by lawful universe geometry there is no such location for this family to stand at."""
    d = copy.deepcopy(raw)
    d["declarations"][1]["body"]["constitutive_anchor"] = "by_berth"
    shifted = parse_native_publication(_refingerprint_fcf2(d, 1))
    with pytest.raises(WantOfLaw, match="reached by FORGETTING"):
        nrq.resolve(shifted, parse_statement("SELECT berthings AT {berth * day}"))


def test_the_movement_ask_refuses_at_the_DECISION_and_names_what_is_missing(pub, views):
    req = nrq.resolve(pub, parse_statement("SELECT berthings AT {berth}"))
    with pytest.raises(WantOfLaw) as e:
        nl.assert_answerable(views[req.identity.family_id], moving=req.is_moving)
    msg = str(e.value)
    assert "establishes no positive movement" in msg
    assert "will not infer a licence from the geometry" in msg
    assert "not yet decided" in msg


def test_the_DOMAIN_ALONE_trap_is_gone_because_C3_SPLIT(pub, raw):
    """**The defect this test was written to catch no longer exists** (ruled 2026-09-22).

    It used to be that a family declaring a domain and no movement resolved ONE C3 standing to
    ESTABLISHED, so testing the standing would have served a coarser anchor for a family carrying no
    licence at all. C3 is now two responsibilities and the trap is structural rather than guarded:
    the legacy combined entry still goes ESTABLISHED — it is retained byte-identical for the v2 path
    — while the edge-validity standing, which is what the rule reads, correctly stays UNESTABLISHED.

    Both halves are asserted, because the whole point is that they now DISAGREE."""
    d = copy.deepcopy(raw)
    d["declarations"][1]["body"]["domain"] = {"note": "a declared domain, and no movement"}
    view = nl.laws_of(parse_native_publication(_refingerprint_fcf2(d, 1)))[BERTHINGS]
    assert view[C3_DOMAIN_MOVEMENT].standing == ESTABLISHED      # the old conflated entry
    assert view[C3_EDGE_VALIDITY].standing == UNESTABLISHED      # what the rule now reads
    assert view[C3_FAMILY_DOMAIN].standing == UNESTABLISHED      # a v2 `domain` marker is not P_F
    with pytest.raises(WantOfLaw, match="establishes no positive movement"):
        nl.assert_answerable(view, moving=True)


def test_an_explicit_none_movement_says_so_in_its_own_words(pub, raw):
    d = copy.deepcopy(raw)
    d["declarations"][1]["body"]["movement"] = {"none": "this count does not project"}
    view = nl.laws_of(parse_native_publication(_refingerprint_fcf2(d, 1)))[BERTHINGS]
    with pytest.raises(WantOfLaw, match="DECLARED that nothing moves"):
        nl.assert_answerable(view, moving=True)


def test_POSITIVE_movement_content_STOPS_rather_than_being_guessed_at(pub, raw):
    """**Where C4 ends.** A native family may carry `movement` content — the key is in the total
    body key set of both majors — and what it MEANS natively is undecided. The profile refuses to
    author the contract by reading it."""
    d = copy.deepcopy(raw)
    d["declarations"][1]["body"]["movement"] = {"to": "by_berth", "standing": "positive"}
    view = nl.laws_of(parse_native_publication(_refingerprint_fcf2(d, 1)))[BERTHINGS]
    with pytest.raises(WantOfLaw) as e:
        nl.assert_answerable(view, moving=True)
    assert "no governed reading of it" in str(e.value)
    assert "preserved, not rejected" in str(e.value)


def test_the_missing_fact_is_NARROWED_to_the_edge_half_not_retired():
    """C4 recorded one undecided fact covering both halves of C3. The family-domain half is now
    decided for primitive Case-S families; the EDGE half is not, so the constant narrows rather
    than retiring — and it must not quietly start describing the half that was answered."""
    m = nl.MOVEMENT_STANDING_UNDECIDED
    assert "EDGE CONTRACT" in m.fact
    assert "does not make every proposed derivation to A lawful" in m.fact
    assert "steward who constitutes F" in m.whose
    assert "movement slot" in m.where
    assert set(vars(m)) == {"fact", "whose", "where"}      # no candidate shape, by construction


# ══ 4 · THE SAME RULE, BOTH PATHS, NEITHER ANCHOR MODEL TRANSLATED ═══════════════════════════════
def test_the_decision_rule_names_no_anchor_at_all():
    """Read off the IDENTIFIERS the rule touches, not its prose. The rule may explain at length why
    an anchor model has no place in it — the refusals have to be legible to a steward — and it may
    not name one in anything it evaluates."""
    import ast
    import inspect
    import textwrap

    sig = inspect.signature(nl.assert_answerable)
    assert list(sig.parameters) == ["view", "moving"]

    fn = ast.parse(textwrap.dedent(inspect.getsource(nl.assert_answerable))).body[0]
    names = {n.id for n in ast.walk(fn) if isinstance(n, ast.Name)}
    names |= {n.attr for n in ast.walk(fn) if isinstance(n, ast.Attribute)}
    offenders = sorted(n for n in names if "anchor" in n)
    assert not offenders, f"the decision rule reaches for {offenders}"
    assert names.isdisjoint({"universe", "denote", "constituents", "refines", "declared"})


def test_the_ANCHOR_FREE_CLAIM_IS_NARROWED_and_here_is_the_distinction():  # noqa: D401
    """**What C4 proved, and what C4 over-claimed** (ruled Huayin, 2026-09-22).

    C4 wrote one rule that named no anchor, ran it over a native and a legacy `LawView`, and
    concluded that answerability converges without translating either anchor model. The test above
    still passes and that result stands — for what it actually covers.

    What it does NOT cover was discovered in C5. `assert_answerable` asks whether the family's LAW
    makes it answerable: does it have a sufficient-state basis, does it license movement at all.
    Those are the family's statements about itself, and no anchor belongs in them. But *may F stand
    at THIS location* is a RELATION between the family and a resolved location, and no amount of
    care can decide it without consuming geometry.

    So the strong reading — that the COMPLETE answerability decision can stay anchor-free — is
    withdrawn. The rule was not bent to keep it: the family-domain predicate lives in
    `native_domain`, one layer up, where the law and the resolved geometry are both legitimately
    in hand. This test pins the narrowing so the withdrawn claim cannot be silently re-adopted."""
    import inspect

    import columna_platform.native_domain as nd

    # the law-level rule: still anchor-free, asserted above
    assert "Anchor" not in inspect.getsource(nl.assert_answerable)

    # the domain predicate: DELIBERATELY consumes geometry, and says so in its signature
    params = list(inspect.signature(nd.assert_within_domain).parameters)
    assert params == ["view", "family", "root", "target"]
    assert "projection_forgets" in inspect.getsource(nd.forgotten)


def test_the_SAME_rule_decides_a_LEGACY_law_view_unchanged():
    """The convergence question, asked in the only form that can be answered: write the rule so an
    anchor model cannot enter it, then run it over both paths' views.

    Nothing in the v2 path is modified — its own serving code is untouched and still asks its own
    version of these questions. This reads a v2 `LawView` and applies the native decision to it."""
    v2 = parse_publication(json.loads(V2_ARTIFACT.read_text(encoding="utf-8")))
    legacy = resolve_all(v2)
    revenue = next(v for v in legacy.values() if v.canonical_reference == "revenue")
    nl.assert_answerable(revenue, moving=False)                      # answerable at its anchor
    with pytest.raises(WantOfLaw, match="establishes no positive movement"):
        nl.assert_answerable(revenue, moving=True)


def test_both_paths_reach_the_SAME_verdict_for_the_same_reason(pub, views):
    v2 = parse_publication(json.loads(V2_ARTIFACT.read_text(encoding="utf-8")))
    revenue = next(v for v in resolve_all(v2).values() if v.canonical_reference == "revenue")
    native = views[BERTHINGS]
    for view in (revenue, native):
        assert view[C7_SUFFICIENT_STATE].standing == ESTABLISHED
        assert view[C3_EDGE_VALIDITY].standing == UNESTABLISHED


# ══ helpers ══════════════════════════════════════════════════════════════════════════════════════
def _refingerprint_fcf2(d: dict, index: int) -> dict:
    """Re-mint an `fcf-2` family authority after editing its body.

    Same note as C3's fixture builder: minted with the consumer's own derivation, so it witnesses
    what it is used for here — the SHAPE of a family's declared law — and not canonicalization
    agreement with the producer (OF-59)."""
    from columna_core.governed.native import FCF2_IDENTITY_KEYS, _digest
    decl = d["declarations"][index]
    universe = next(x for x in d["declarations"]
                    if x.get("kind") == "universe" and x["name"] == decl["body"]["universe"])
    anchor = sorted(universe["case_s_denotations"][decl["body"]["constitutive_anchor"]])
    payload = {"_scheme": "fcf-2", "_anchor": anchor,
               **{k: decl["body"][k] for k in sorted(FCF2_IDENTITY_KEYS) if k in decl["body"]}}
    decl["family_constitution_authority"]["constitution_fingerprint"] = "fcf-2:" + _digest(payload)
    return d

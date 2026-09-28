"""
test_v8_1_governed_expression.py — V8-1's stop-gate, witnessed.

    *native v3.1 has a positively admitted governed-expression kind; v3.0 family artifacts remain
    unchanged and accepted by the v3.1-capable reader; old readers refuse v3.1 by the existing
    explicit-version contract; a durable MEAN expression round-trips and resolves as an expression,
    never as a family; Σ(E) and expression succession are tested; alternative-basis extensibility is
    not structurally blocked; no family-only responsibilities appear on the expression record.*
        — Huayin, 2026-09-28, the V8-1 acceptance gate

ONE TEST PER REQUIRED PROOF, and the section headings are the gate's own clauses. Nothing here imports
`manifold_agent`, `columna_server` or `columna_platform`. The fixtures are the artifacts; the artifacts
are the contract.
"""
import copy
import json
import os

import pytest

from columna_core.governed import foundation as fdn
from columna_core.governed.expression import (
    E1_CONSTRUCTOR,
    E2_OPERANDS,
    E3_INNER_ANCHORS,
    E4_PARTICIPATION,
    E5_ADMITTED_BASES,
    E6_BASIS_AGREEMENT,
    E7_PARAMETERS,
    EXPRESSION_RESPONSIBILITIES,
    GOVERNED_EQUIVALENCE_ERRATA,
    SAME_EXPRESSION,
    SIGMA_E,
    SUCCESSOR_REQUIRED,
    ExpressionResolutionRefusal,
    render,
    resolve_all_expressions,
    resolve_expression,
    succession,
)
from columna_core.governed.native import (
    ADMITTED_KINDS,
    ADMITTED_KINDS_BY_VERSION,
    ECF1,
    ECF1_IDENTITY_KEYS,
    EXPRESSION_BODY_KEYS,
    EXPRESSION_IDENTITY_KEYS,
    EXPRESSION_NON_IDENTITY_KEYS,
    FAMILY_BODY_KEYS,
    FCF1,
    FCF2,
    NATIVE_PUBLICATION_FORMAT_VERSION,
    SUPPORTED_NATIVE_VERSIONS,
    NativePublicationRefusal,
    canonical_expression_payload,
    expression_fingerprint,
    minor_admitting,
    parse_native_publication,
)
from columna_core.governed.resolve import ESTABLISHED, EXPLICIT_NONE, UNESTABLISHED

_HERE = os.path.dirname(os.path.abspath(__file__))
_V30 = os.path.join(_HERE, "fixtures_v3", "native-v3-publication.json")
_V31 = os.path.join(_HERE, "fixtures_v3", "native-v3_1-publication.json")

REV = "fam_Rv7KpQ2mXsDnYc4TjLbWhE"
CNT = "fam_Oc5HjT9yWnQsEr2BkXpLdM"


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture
def raw30():
    return _read(_V30)


@pytest.fixture
def raw31():
    return _read(_V31)


@pytest.fixture
def pub(raw31):
    return parse_native_publication(raw31)


@pytest.fixture
def aov(pub):
    return pub.expression("average_order_value")


@pytest.fixture
def view(pub, aov):
    return resolve_expression(aov, pub.universe("commerce"), {f.family_id: f for f in pub.families})


def _restamp(raw):
    """Re-derive the expression's `ecf-1` authority over a MUTATED body.

    A test that mutated a body and left the fingerprint alone would be testing the currency check, not
    the thing it meant to test — every such artifact refuses for the same uninteresting reason. So the
    authority is restamped, which makes each mutation test the rule it names."""
    raw = copy.deepcopy(raw)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    probe = copy.deepcopy(raw)
    probe_decl = next(d for d in probe["declarations"] if d["kind"] == "expression")
    probe_decl["expression_constitution_authority"]["constitution_fingerprint"] = "ecf-1:" + "0" * 64
    try:
        parse_native_publication(probe)
    except NativePublicationRefusal as exc:
        # the refusal quotes the digest the body derives; take it from there rather than rebuilding
        # the record by hand, so the test uses the contract's own derivation
        derived = str(exc).split("derives '")[1].split("'")[0]
        decl["expression_constitution_authority"]["constitution_fingerprint"] = derived
        return raw
    raise AssertionError("expected the probe artifact to refuse")   # pragma: no cover


# ── gate 1 · native v3.1 has a POSITIVELY ADMITTED governed-expression kind ───────────────────────
def test_v3_1_positively_admits_the_expression_kind():
    assert NATIVE_PUBLICATION_FORMAT_VERSION == "3.1"
    assert "3.1" in SUPPORTED_NATIVE_VERSIONS
    assert ADMITTED_KINDS_BY_VERSION["3.1"] == frozenset({"universe", "family", "expression"})
    assert ADMITTED_KINDS == ADMITTED_KINDS_BY_VERSION["3.1"]


def test_admission_is_MINOR_RELATIVE_so_v3_0_does_not_acquire_the_sort(raw31):
    """The other half of "additive": v3.0's contract did not admit this kind, and a reader that read it
    anyway would be deciding that the minor an artifact declared was a formality."""
    assert "expression" not in ADMITTED_KINDS_BY_VERSION["3.0"]
    bad = copy.deepcopy(raw31)
    bad["publication_format_version"] = "3.0"
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(bad)
    assert "admitted at native v3.1" in str(exc.value)
    assert "Re-declare the artifact as v3.1" in str(exc.value)


def test_the_refusal_distinguishes_a_later_minors_kind_from_no_kind_at_all(raw31):
    """Two situations, two remedies. `anchor` is admitted at no minor; `expression` is admitted later."""
    assert minor_admitting("expression") == "3.1"
    assert minor_admitting("anchor") is None
    bad = copy.deepcopy(raw31)
    bad["declarations"].append({"kind": "anchor", "name": "sale_at"})
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(bad)
    assert "is not admitted in publication format 3.1" in str(exc.value)
    assert "admitted at native v" not in str(exc.value)


# ── gate 2 · v3.0 family artifacts remain UNCHANGED and accepted ──────────────────────────────────
def test_the_shipped_v3_0_artifact_is_read_by_the_v3_1_capable_reader_unchanged(raw30):
    pub = parse_native_publication(raw30)
    assert (pub.manifold_id, pub.format_version) == ("harbour", "3.0")
    assert [f.name for f in pub.families] == ["berthings", "moorings"]
    assert pub.expressions == ()
    assert len(pub.currency()) == 6          # 2 universe claims + 2 families × 2 — unchanged
    for claim in pub.currency():
        assert claim.verdict in ("CURRENT", "COVERED", "BOUND", "UNBOUND")


def test_a_v3_0_familys_fcf_digest_does_not_move(raw30):
    """**BYTE-IDENTICAL IN MEANING** is the ruling, and a digest is how that is measured. If the
    expression work had touched a family's identity payload, every v3.0 family would refuse at read —
    so this asserts the fingerprints the shipped artifact carries are still the ones derived."""
    pub = parse_native_publication(raw30)
    for f in pub.families:
        u = pub.universe(f.universe_reference)
        from columna_core.governed.native import expected_family_scheme, family_fingerprint
        scheme = expected_family_scheme(f, u)
        assert scheme in (FCF1, FCF2)
        assert family_fingerprint(f, u, scheme) == f.authority.fingerprint


def test_the_family_body_contract_did_not_gain_or_lose_a_key():
    assert FAMILY_BODY_KEYS == frozenset({
        "family_id", "canonical_reference", "aliases", "universe", "constitutive_anchor", "target",
        "formation", "participation", "value_domain", "continuation", "domain", "movement",
        "prohibited_constituents", "exceptional"})


# ── gate 3 · old readers refuse v3.1 by the EXISTING explicit-version contract ─────────────────────
def test_an_older_reader_refuses_v3_1_and_the_mechanism_is_the_one_already_there(raw31, monkeypatch):
    """The v3.0-only reader is simulated by restoring ITS `SUPPORTED_NATIVE_VERSIONS`, because that is
    the whole of what an older build differs by. No new refusal was written for this."""
    import columna_core.governed.native as N
    monkeypatch.setattr(N, "SUPPORTED_NATIVE_VERSIONS", ("3.0",))
    with pytest.raises(NativePublicationRefusal) as exc:
        N.parse_native_publication(raw31)
    msg = str(exc.value)
    assert "is a v3 minor this build does not explicitly understand" in msg
    assert "must be KNOWN, not presumed" in msg
    assert "never because it sorts after this one" in msg


def test_the_major_gate_is_untouched_by_the_minor_bump(raw31):
    for version, expected in (("2.0", "format v2 artifact"), ("4.1", "has major 4"),
                              ("3", "states a bare major")):
        bad = copy.deepcopy(raw31)
        bad["publication_format_version"] = version
        with pytest.raises(NativePublicationRefusal) as exc:
            parse_native_publication(bad)
        assert expected in str(exc.value)


# ── gate 4 · a durable MEAN expression ROUND-TRIPS and resolves as an EXPRESSION, NEVER a family ──
def test_the_mean_expression_round_trips(pub, aov):
    assert pub.format_version == "3.1"
    assert [x.name for x in pub.expressions] == ["average_order_value"]
    assert aov.expression_id.startswith("expr_")
    assert aov.aliases == ("aov",)
    assert aov.roles == ("operand",)
    assert aov.operand("operand").family_id == REV
    assert aov.inner_anchor_tokens == ("sale_at",)
    assert aov.authority.scheme == ECF1
    assert aov.binding is not None
    assert expression_fingerprint(aov, pub.universe("commerce")) == aov.authority.fingerprint


def test_the_mean_expression_resolves_TOTALLY_and_is_valid_and_evaluable(view):
    assert set(view.entries) == set(EXPRESSION_RESPONSIBILITIES)
    assert view.valid, view.validity_problems
    assert view.establishable
    assert view.standing(E1_CONSTRUCTOR) == ESTABLISHED
    assert view[E1_CONSTRUCTOR].value.name == "MEAN"
    assert view.standing(E5_ADMITTED_BASES) == ESTABLISHED
    assert "b_sum_count_store_day" in render(view)


def test_the_expression_is_NEVER_reachable_as_a_family(pub):
    """The four doors, and every one of them says the sort."""
    assert pub.sort_of("average_order_value") == "expression"
    assert pub.sort_of("aov") == "expression"
    assert pub.resolve_reference("average_order_value") is None
    assert pub.resolve_reference("aov") is None
    assert [f.name for f in pub.families] == ["revenue", "order_count"]
    for token in ("average_order_value", "aov"):
        with pytest.raises(NativePublicationRefusal) as exc:
            pub.family(token)
        assert "names a governed EXPRESSION" in str(exc.value)
        assert "not promoted to a family by being named, cached, repeated or durably governed" \
            in str(exc.value)


def test_a_family_is_NEVER_reachable_as_an_expression_and_that_is_ruling_5(pub):
    """*"Parsing compatibility is not analytical reclassification."* A basis-mediated family does not
    become an expression because the reader now knows the sort; it requires re-authoring."""
    assert pub.sort_of("revenue") == "family"
    assert pub.resolve_expression_reference("revenue") is None
    with pytest.raises(NativePublicationRefusal) as exc:
        pub.expression("revenue")
    assert "parsing compatibility is not analytical reclassification" in str(exc.value)
    assert "explicit re-authoring" in str(exc.value)


def test_one_reference_may_not_name_both_sorts(raw31):
    bad = copy.deepcopy(raw31)
    decl = next(d for d in bad["declarations"] if d["kind"] == "expression")
    decl["body"]["aliases"] = ["revenue"]
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(_restamp(bad))
    assert "resolves to two governed objects" in str(exc.value)
    assert "which lookup ran first" in str(exc.value)


def test_the_two_sorts_share_one_identity_space(raw31):
    bad = copy.deepcopy(raw31)
    decl = next(d for d in bad["declarations"] if d["kind"] == "expression")
    decl["body"]["expression_id"] = REV
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(_restamp(bad))
    assert "already declared as a family_id" in str(exc.value)


# ── gate 5 · NO FAMILY-ONLY RESPONSIBILITIES on the expression record ─────────────────────────────
@pytest.mark.parametrize("family_only", ["constitutive_anchor", "continuation", "movement",
                                         "prohibited_constituents", "exceptional", "target",
                                         "value_domain", "formation", "domain"])
def test_the_expression_body_contract_refuses_every_family_only_key(raw31, family_only):
    """TOTAL at key granularity: each of these is a statement about continuation under refinement, and
    an expression has none — so the contract does not have a slot to put one in."""
    assert family_only not in EXPRESSION_BODY_KEYS
    bad = copy.deepcopy(raw31)
    decl = next(d for d in bad["declarations"] if d["kind"] == "expression")
    decl["body"][family_only] = "anything at all"
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(bad)
    assert f"unrecognised key(s) ['{family_only}']" in str(exc.value)


def test_the_resolver_answers_no_family_question(view):
    """`Law(E)` is seven responsibilities, and none of them is a C3/C8/C9."""
    assert len(EXPRESSION_RESPONSIBILITIES) == 7
    from columna_core.governed.resolve import RESPONSIBILITIES as FAMILY_RESPONSIBILITIES
    assert not (set(EXPRESSION_RESPONSIBILITIES) & set(FAMILY_RESPONSIBILITIES))
    assert not hasattr(view, "family_id")


def test_the_expression_record_carries_no_root(pub, aov):
    """An expression has CONSTITUTIVE INNER anchors and no `anchor_token`. The absence of the singular
    is the point: reducing several inner anchors to one would be inventing a root."""
    assert not hasattr(aov, "anchor_token")
    assert not hasattr(aov, "constitutive_anchor")
    assert aov.inner_anchor_tokens == ("sale_at",)
    assert "NOT a root" in view_note(pub, aov, E3_INNER_ANCHORS)


def view_note(pub, expr, responsibility):
    v = resolve_expression(expr, pub.universe(expr.universe_reference),
                           {f.family_id: f for f in pub.families})
    return v[responsibility].note


def test_an_expressions_lineage_runs_through_its_operands_and_not_its_bases(aov):
    """§7.1 keeps family / expression / carrier lineage apart. A basis is a ROUTE TO A VALUE, and a
    route is not a parent — so `order_count`, which is only a basis component, is not ancestry."""
    assert aov.operand_family_ids == (REV,)
    assert CNT not in aov.operand_family_ids
    assert CNT in {c.family_id for b in aov.admitted_bases for c in b.components}


# ── gate 6 · Σ(E) ─────────────────────────────────────────────────────────────────────────────────
def test_sigma_E_is_v8_7_3s_own_list_and_nothing_else():
    assert set(ECF1_IDENTITY_KEYS) == {"constructor", "operands", "participation", "scope",
                                       "parameters"}
    assert set(EXPRESSION_IDENTITY_KEYS) - set(ECF1_IDENTITY_KEYS) == {"universe", "inner_anchors"}
    assert set(SIGMA_E) == {E1_CONSTRUCTOR, E2_OPERANDS, E3_INNER_ANCHORS, E4_PARTICIPATION,
                            E7_PARAMETERS}
    assert E5_ADMITTED_BASES not in SIGMA_E
    assert E6_BASIS_AGREEMENT not in SIGMA_E


def test_the_admitted_bases_are_NOT_in_sigma_E_and_this_is_ruling_4(pub, aov, raw31):
    """*"Expression identity ≠ one particular sufficient basis used to establish it."*

    Measured, not asserted: withdrawing the only admitted basis leaves the digest byte-identical."""
    assert "admitted_bases" in EXPRESSION_NON_IDENTITY_KEYS
    u = pub.universe("commerce")
    before = canonical_expression_payload(aov, u)
    assert "admitted_bases" not in before

    stripped = copy.deepcopy(raw31)
    decl = next(d for d in stripped["declarations"] if d["kind"] == "expression")
    del decl["body"]["admitted_bases"]
    # the SAME authority fingerprint still covers it — which is the proof
    pub2 = parse_native_publication(stripped)
    aov2 = pub2.expression("average_order_value")
    assert aov2.admitted_bases == ()
    assert canonical_expression_payload(aov2, pub2.universe("commerce")) == before
    assert aov2.authority.fingerprint == aov.authority.fingerprint


def test_ecf_1_is_TOTAL_over_its_identity_keys_so_absent_and_empty_are_one_fact(pub, raw31):
    """The `fcf` hole that is deliberately not reproduced: `canonical_family_payload` writes a key only
    `if key in body`, so for a family an absent optional key and one declared empty give two digests."""
    u = pub.universe("commerce")
    with_scope = parse_native_publication(raw31).expression("average_order_value")
    blanked = copy.deepcopy(raw31)
    decl = next(d for d in blanked["declarations"] if d["kind"] == "expression")
    decl["body"]["scope"] = ""
    dropped = copy.deepcopy(blanked)
    d2 = next(d for d in dropped["declarations"] if d["kind"] == "expression")
    del d2["body"]["scope"]

    a = parse_native_publication(_restamp(blanked)).expression("average_order_value")
    b = parse_native_publication(_restamp(dropped)).expression("average_order_value")
    assert canonical_expression_payload(a, u) == canonical_expression_payload(b, u)
    assert canonical_expression_payload(a, u) != canonical_expression_payload(with_scope, u)


def test_operand_ORDER_is_not_identity_bearing_but_the_ROLE_is(pub, raw31):
    """The trade a bare positional tuple cannot make: reordering the serialization is not a change, and
    swapping which family fills which role is."""
    u = pub.universe("commerce")
    base = copy.deepcopy(raw31)
    decl = next(d for d in base["declarations"] if d["kind"] == "expression")
    decl["body"]["operands"] = [{"role": "b", "family_id": REV}, {"role": "a", "family_id": CNT}]
    one = parse_native_publication(_restamp(base)).expression("average_order_value")

    swapped = copy.deepcopy(base)
    d2 = next(d for d in swapped["declarations"] if d["kind"] == "expression")
    d2["body"]["operands"] = [{"role": "a", "family_id": CNT}, {"role": "b", "family_id": REV}]
    two = parse_native_publication(_restamp(swapped)).expression("average_order_value")
    assert canonical_expression_payload(one, u) == canonical_expression_payload(two, u)

    reassigned = copy.deepcopy(base)
    d3 = next(d for d in reassigned["declarations"] if d["kind"] == "expression")
    d3["body"]["operands"] = [{"role": "b", "family_id": CNT}, {"role": "a", "family_id": REV}]
    three = parse_native_publication(_restamp(reassigned)).expression("average_order_value")
    assert canonical_expression_payload(one, u) != canonical_expression_payload(three, u)


def test_inner_anchors_enter_sigma_E_RESOLVED_so_synonyms_collapse(pub, raw31):
    """`ecf-1` starts where `fcf-2` ended. Two tokens denoting one constituent set are ONE anchor."""
    u = pub.universe("commerce")
    assert sorted(u.synonyms_of(u.denote("sale_at"))) == ["sale_at"]
    payload = canonical_expression_payload(pub.expression("average_order_value"), u)
    assert payload["_inner_anchors"] == [["day", "store"]]
    assert "sale_at" not in json.dumps(payload)
    assert "universe" not in payload           # the SPELLING is governed through the binding


def test_a_stale_ecf_1_authority_refuses_at_read(raw31):
    bad = copy.deepcopy(raw31)
    decl = next(d for d in bad["declarations"] if d["kind"] == "expression")
    decl["body"]["participation"] = "every order, accepted or not"
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(bad)
    assert "The authority does not cover this expression's constitution" in str(exc.value)
    assert "Admitting or withdrawing a sufficient BASIS cannot reach this digest" in str(exc.value)


def test_an_expression_may_not_be_established_under_a_family_scheme(raw31):
    for scheme in (FCF1, FCF2):
        bad = copy.deepcopy(raw31)
        decl = next(d for d in bad["declarations"] if d["kind"] == "expression")
        decl["expression_constitution_authority"]["fingerprint_scheme"] = scheme
        with pytest.raises(NativePublicationRefusal) as exc:
            parse_native_publication(bad)
        assert "the expression contract knows ['ecf-1']" in str(exc.value)


def test_an_expression_must_be_BOUND_because_ecf_1_drops_the_universe_spelling(raw31):
    bad = copy.deepcopy(raw31)
    decl = next(d for d in bad["declarations"] if d["kind"] == "expression")
    del decl["universe_authority_binding"]
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(bad)
    assert "requires one" in str(exc.value)
    assert "a hole rather than a transition" in str(exc.value)


# ── gate 7 · EXPRESSION SUCCESSION ────────────────────────────────────────────────────────────────
def _variant(raw31, mutate):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    mutate(decl["body"])
    pub = parse_native_publication(_restamp(raw))
    return pub.expression("average_order_value"), pub.universe("commerce")


def test_an_identical_declaration_is_the_same_expression(pub, aov):
    u = pub.universe("commerce")
    s = succession(aov, u, aov, u)
    assert s.verdict == SAME_EXPRESSION
    assert s.changed == ()


@pytest.mark.parametrize("key,mutate", [
    ("constructor", lambda b: b.__setitem__("constructor", {
        "vocabulary": "datumwise.foundation", "version": "1", "law": "MIN"})),
    ("operands", lambda b: b.__setitem__("operands", [{"role": "operand", "family_id": CNT}])),
    ("participation", lambda b: b.__setitem__("participation", "every order the merchant recorded")),
    ("scope", lambda b: b.__setitem__("scope", "the accepted orders of one store")),
    ("parameters", lambda b: b.__setitem__("parameters", {"order": "accepted_at"})),
])
def test_a_change_to_ANY_identity_bearing_constituent_mints_a_successor(pub, aov, raw31, key, mutate):
    after, u_after = _variant(raw31, mutate)
    s = succession(aov, pub.universe("commerce"), after, u_after)
    assert s.verdict == SUCCESSOR_REQUIRED
    assert key in s.changed
    assert GOVERNED_EQUIVALENCE_ERRATA in s.note


def test_a_change_to_the_constitutive_INNER_ANCHORS_mints_a_successor(pub, aov, raw31):
    after, u_after = _variant(raw31, lambda b: b.__setitem__("inner_anchors", ["by_store"]))
    s = succession(aov, pub.universe("commerce"), after, u_after)
    assert s.verdict == SUCCESSOR_REQUIRED
    assert "_inner_anchors" in s.changed


@pytest.mark.parametrize("mutate", [
    lambda b: b.__setitem__("aliases", ["aov", "avg_order"]),
    lambda b: b.pop("admitted_bases"),
    lambda b: b.__setitem__("canonical_reference", "mean_order_value"),
])
def test_a_change_OUTSIDE_sigma_E_does_NOT_mint_a_successor(pub, aov, raw31, mutate):
    """The negative cases are true BY CONSTRUCTION, because succession compares Σ(E) payloads and not
    declarations. This is ruling 4 made executable: admitting or withdrawing an establishment route
    cannot change which expression this is."""
    after, u_after = _variant(raw31, mutate)
    s = succession(aov, pub.universe("commerce"), after, u_after)
    assert s.verdict == SAME_EXPRESSION
    assert s.changed == ()


def test_succession_takes_NO_equivalence_escape_and_says_so(pub, aov, raw31):
    """Ruling 6. There is no governed equivalence mechanism in this build and v8 does not define one, so
    the rule's second clause never fires — and the errata candidate is carried in the verdict rather
    than filed and forgotten."""
    after, u_after = _variant(raw31, lambda b: b.__setitem__("scope", "something else entirely"))
    s = succession(aov, pub.universe("commerce"), after, u_after)
    assert s.verdict == SUCCESSOR_REQUIRED
    assert "never defined" in GOVERNED_EQUIVALENCE_ERRATA
    assert "§6.6" in GOVERNED_EQUIVALENCE_ERRATA
    assert "no local equivalence is invented" in GOVERNED_EQUIVALENCE_ERRATA


def test_a_change_to_the_WORLD_can_change_sigma_E_with_no_expression_byte_moving(raw31):
    """Why `succession` takes both universes. An expression constituted over a constituent SET is
    constituted over a different one when the set changes — correctly, and invisibly in the
    expression's own bytes."""
    moved = copy.deepcopy(raw31)
    uni = next(d for d in moved["declarations"] if d["kind"] == "universe")
    uni["case_s_denotations"]["sale_at"] = ["store"]
    before = parse_native_publication(raw31)
    # the family fcf-2 digests move with the denotation, so compare payloads directly rather than
    # re-reading an artifact whose FAMILY authorities would now also be stale
    from columna_core.governed.native import _read_constitution, _read_universe
    _read_constitution("commerce", uni["constitution"])
    uni["existence_law_ratification"]["fingerprint"] = \
        _read_constitution("commerce", uni["constitution"]).fingerprint()
    after_universe = _read_universe(uni)
    aov = before.expression("average_order_value")
    s = succession(aov, before.universe("commerce"), aov, after_universe)
    assert s.verdict == SUCCESSOR_REQUIRED
    assert s.changed == ("_inner_anchors",)


# ── gate 8 · ALTERNATIVE-BASIS EXTENSIBILITY IS NOT STRUCTURALLY BLOCKED ──────────────────────────
def _with_second_basis(raw31, *, sum_family=REV, count_family=CNT, rcp=True, basis_id="b_alt"):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["admitted_bases"].append({
        "basis_id": basis_id,
        "components": [{"role": "SUM", "family_id": sum_family},
                       {"role": "COUNT", "family_id": count_family}],
        "requires_common_participation": rcp})
    return raw


def test_zero_one_and_several_admitted_bases_are_all_representable(pub, raw31):
    """Ruling 4: *"make the record structurally capable of zero/one/multiple admitted bases."* All three
    are read, and the ONE that is not established is the one with no route — which is legible, not a
    defect, and not a validity problem."""
    fams = {f.family_id: f for f in pub.families}
    u = pub.universe("commerce")

    none_ = copy.deepcopy(raw31)
    next(d for d in none_["declarations"] if d["kind"] == "expression")["body"]["admitted_bases"] = []
    p0 = parse_native_publication(none_)
    v0 = resolve_expression(p0.expression("average_order_value"), u, fams)
    assert v0.standing(E5_ADMITTED_BASES) == UNESTABLISHED
    assert v0.valid and not v0.establishable
    assert "LEGIBLE, NOT A DEFECT" in v0[E5_ADMITTED_BASES].note

    v1 = resolve_expression(pub.expression("average_order_value"), u, fams)
    assert len(v1[E5_ADMITTED_BASES].value) == 1

    # a THIRD family so a second route is genuinely a different assignment
    two = _with_second_basis(raw31, count_family=REV, rcp=True)
    p2 = parse_native_publication(two)
    assert len(p2.expression("average_order_value").admitted_bases) == 2


def test_two_alternative_routes_that_AGREE_resolve_and_the_residue_is_reported(pub, raw31):
    """v8 allows more than one sufficient basis and requires that alternatives AGREE. Where they agree
    on the component laws and the participation requirement but fill a role with DIFFERENT families,
    the interchangeability question is exactly `governed equivalence` — and it is REPORTED, not
    decided."""
    raw = _with_second_basis(raw31, sum_family=REV, count_family=REV, rcp=True)
    p = parse_native_publication(raw)
    x = p.expression("average_order_value")
    v = resolve_expression(x, p.universe("commerce"), {f.family_id: f for f in p.families})
    assert v.standing(E6_BASIS_AGREEMENT) == ESTABLISHED
    note = v[E6_BASIS_AGREEMENT].note
    assert "2 alternatives agree" in note
    assert "THE RESIDUE IS NOT ADJUDICATED" in note
    assert "['COUNT']" in note
    assert GOVERNED_EQUIVALENCE_ERRATA in note


def test_two_routes_that_DISAGREE_on_the_participation_requirement_refuse(pub, raw31):
    raw = _with_second_basis(raw31, count_family=REV, rcp=False)
    p = parse_native_publication(raw)
    with pytest.raises(ExpressionResolutionRefusal) as exc:
        resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    # the per-basis law check fires first, which is the upstream defect
    assert "requires_common_participation" in str(exc.value)


def test_one_route_declared_twice_is_not_two_alternatives(raw31):
    raw = _with_second_basis(raw31)      # identical role→family assignment, different id
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(raw)
    assert "admits the same role-to-family assignment" in str(exc.value)
    assert "one route counted twice" in str(exc.value)


def test_a_single_basis_leaves_the_agreement_obligation_with_nothing_to_range_over(view):
    assert view.standing(E6_BASIS_AGREEMENT) == EXPLICIT_NONE
    assert "nothing to range over" in view[E6_BASIS_AGREEMENT].note


# ── the basis's own analytical checks ─────────────────────────────────────────────────────────────
def test_a_basis_must_fill_exactly_the_component_laws_the_constructor_requires(pub, raw31):
    fams = {f.family_id: f for f in pub.families}
    for components in ([{"role": "SUM", "family_id": REV}],
                       [{"role": "SUM", "family_id": REV}, {"role": "COUNT", "family_id": CNT},
                        {"role": "MIN", "family_id": REV}]):
        raw = copy.deepcopy(raw31)
        decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
        decl["body"]["admitted_bases"][0]["components"] = components
        p = parse_native_publication(raw)
        with pytest.raises(ExpressionResolutionRefusal) as exc:
            resolve_expression(p.expression("average_order_value"), p.universe("commerce"), fams)
        assert "requires exactly ['COUNT', 'SUM']" in str(exc.value)


def test_a_basis_may_not_relax_the_laws_own_participation_requirement(pub, raw31):
    assert fdn.LAWS["MEAN"].state_basis.requires_common_participation is True
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["admitted_bases"][0]["requires_common_participation"] = False
    p = parse_native_publication(raw)
    with pytest.raises(ExpressionResolutionRefusal) as exc:
        resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    assert "is not a default a declaration may relax" in str(exc.value)


def test_requires_common_participation_must_be_PRESENT_and_a_boolean(raw31):
    for value in (None, "yes", 1):
        raw = copy.deepcopy(raw31)
        decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
        if value is None:
            del decl["body"]["admitted_bases"][0]["requires_common_participation"]
        else:
            decl["body"]["admitted_bases"][0]["requires_common_participation"] = value
        with pytest.raises(NativePublicationRefusal) as exc:
            parse_native_publication(raw)
        assert "licenses exactly the pairing the field exists to forbid" in str(exc.value)


def test_common_participation_is_CHECKED_against_the_component_families_declarations(pub, raw31):
    """§11.5.2's word is MATCHING, and this is it, executable: a SUM and a COUNT that ranged over
    different contributions are individually valid and jointly meaningless."""
    raw = copy.deepcopy(raw31)
    fam = next(d for d in raw["declarations"]
               if d["kind"] == "family" and d["name"] == "order_count")
    fam["body"]["participation"] = "every customer order, accepted or abandoned"
    p = parse_native_publication(_restamp_family(raw, "order_count"))
    with pytest.raises(ExpressionResolutionRefusal) as exc:
        resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    assert "components declare DIFFERENT participation" in str(exc.value)
    assert "MATCHING" in str(exc.value)


def _restamp_family(raw, name):
    """Re-derive one family's `fcf-2` authority after mutating its body, for the same reason
    `_restamp` exists for expressions."""
    raw = copy.deepcopy(raw)
    decl = next(d for d in raw["declarations"] if d["kind"] == "family" and d["name"] == name)
    decl["family_constitution_authority"]["constitution_fingerprint"] = "fcf-2:" + "0" * 64
    try:
        parse_native_publication(raw)
    except NativePublicationRefusal as exc:
        derived = str(exc).split("derives '")[1].split("'")[0]
        decl["family_constitution_authority"]["constitution_fingerprint"] = derived
        return raw
    raise AssertionError("expected the probe artifact to refuse")   # pragma: no cover


def test_a_component_family_whose_continuation_cannot_supply_the_role_refuses(pub, raw31):
    """CONTINUATION CONGRUENCE — a necessary condition, and the module says it is not a sufficient one."""
    raw = copy.deepcopy(raw31)
    fam = next(d for d in raw["declarations"]
               if d["kind"] == "family" and d["name"] == "order_count")
    fam["body"]["continuation"] = {"vocabulary": "datumwise.foundation", "version": "1", "law": "MIN"}
    p = parse_native_publication(_restamp_family(raw, "order_count"))
    with pytest.raises(ExpressionResolutionRefusal) as exc:
        resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    assert "cannot be supplying that component" in str(exc.value)
    assert "cannot distinguish two component laws that entail the same continuation" in str(exc.value)


def test_a_constructor_with_no_composite_basis_fails_closed_on_a_declared_one(pub, raw31):
    """`SUM`'s own sufficient state IS its basis, so there is nothing in the vocabulary to check a
    declared route against — and accepting it would license any role set whatsoever."""
    assert fdn.LAWS["SUM"].state_basis is None
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["constructor"] = {"vocabulary": "datumwise.foundation", "version": "1", "law": "SUM"}
    p = parse_native_publication(_restamp(raw))
    with pytest.raises(ExpressionResolutionRefusal) as exc:
        resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    assert "states no composite basis" in str(exc.value)
    assert "fails closed" in str(exc.value)


def test_a_constructor_with_no_composite_basis_and_no_declared_route_is_EXPLICIT_NONE(pub, raw31):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["constructor"] = {"vocabulary": "datumwise.foundation", "version": "1", "law": "SUM"}
    del decl["body"]["admitted_bases"]
    p = parse_native_publication(_restamp(raw))
    v = resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    assert v.standing(E5_ADMITTED_BASES) == EXPLICIT_NONE
    assert "A POSITIVE negative" in v[E5_ADMITTED_BASES].note


# ── the resolver's remaining responsibilities ─────────────────────────────────────────────────────
def test_an_unknown_constructor_is_refused_and_never_approximated(pub, raw31):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["constructor"] = {"vocabulary": "datumwise.foundation", "version": "99",
                                   "law": "MEAN"}
    p = parse_native_publication(_restamp(raw))
    with pytest.raises(ExpressionResolutionRefusal) as exc:
        resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    assert "not approximated by a same-named law at another version" in str(exc.value)


def test_an_operand_outside_the_constructors_admitted_domains_refuses(pub, raw31):
    """MEAN admits integer and decimal. A text operand is not an under-specified expression; it is one
    the cited law does not define."""
    raw = copy.deepcopy(raw31)
    fam = next(d for d in raw["declarations"] if d["kind"] == "family" and d["name"] == "revenue")
    fam["body"]["value_domain"] = "text"
    p = parse_native_publication(_restamp_family(raw, "revenue"))
    with pytest.raises(ExpressionResolutionRefusal) as exc:
        resolve_expression(p.expression("average_order_value"), p.universe("commerce"),
                           {f.family_id: f for f in p.families})
    assert "admits operand domains ['decimal', 'integer']" in str(exc.value)


def test_arity_is_reported_as_UNCHECKED_rather_than_guessed(view):
    assert "operand arity is UNCHECKED" in view[E2_OPERANDS].note
    assert "no law in this vocabulary states a signature" in view[E2_OPERANDS].note


def test_inner_anchors_are_ENTAILED_from_the_operands_when_not_declared(pub, raw31):
    after, u = _variant(raw31, lambda b: b.pop("inner_anchors"))
    v = resolve_expression(after, u, {f.family_id: f for f in pub.families})
    assert v.standing(E3_INNER_ANCHORS) == ESTABLISHED
    assert v[E3_INNER_ANCHORS].provenance == "entailed"
    assert "entailed from the operands" in v[E3_INNER_ANCHORS].note
    assert v.valid


def test_duplicate_inner_anchors_refuse_because_they_are_a_SET(raw31):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["inner_anchors"] = ["sale_at", "sale_at"]
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(raw)
    assert "more than once" in str(exc.value)


def test_an_inner_anchor_that_denotes_nothing_refuses_and_says_it_is_not_a_root(raw31):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["inner_anchors"] = ["not_an_anchor"]
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(raw)
    assert "denotes no Case-S anchor" in str(exc.value)
    assert "an inner anchor is not a root" in str(exc.value)


def test_a_role_filled_twice_refuses_because_a_role_is_an_INDEX(raw31):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["operands"] = [{"role": "operand", "family_id": REV},
                                {"role": "operand", "family_id": CNT}]
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(raw)
    assert "A role is an INDEX, not a label" in str(exc.value)


def test_a_dangling_operand_reference_refuses(raw31):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["operands"] = [{"role": "operand", "family_id": "fam_nope"}]
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(raw)
    assert "not declared in this publication" in str(exc.value)


def test_a_bare_law_name_is_not_a_constructor_citation(raw31):
    raw = copy.deepcopy(raw31)
    decl = next(d for d in raw["declarations"] if d["kind"] == "expression")
    decl["body"]["constructor"] = {"vocabulary": "datumwise.foundation", "version": "1", "law": ""}
    with pytest.raises(NativePublicationRefusal) as exc:
        parse_native_publication(raw)
    assert "'law' must be a non-empty string" in str(exc.value)


def test_validity_is_about_IDENTITY_and_an_unsupplied_parameter_is_a_validity_problem(pub, raw31,
                                                                                     monkeypatch):
    """No default is invented to satisfy the check — `resolve`'s own rule, one sort over."""
    monkeypatch.setitem(
        fdn.LAWS, "MEAN",
        fdn.FoundationLaw(**{**fdn.LAWS["MEAN"].__dict__,
                             "required_parameters": ("constitutive_order",)}))
    v = resolve_expression(pub.expression("average_order_value"), pub.universe("commerce"),
                           {f.family_id: f for f in pub.families})
    assert v.standing(E7_PARAMETERS) == UNESTABLISHED
    assert not v.valid
    assert E7_PARAMETERS in " ".join(v.validity_problems)
    assert "no default is invented" in v[E7_PARAMETERS].note


def test_the_currency_report_names_the_expressions_own_scheme_and_subject(pub):
    report = pub.currency()
    claims = {(c.claim, c.subject) for c in report}
    assert ("ecf-1 constitution", "average_order_value") in claims
    assert ("fcf-2 constitution", "revenue") in claims
    assert ("admitted bases", "average_order_value") in claims
    assert all(c.verdict == "CURRENT"
               for c in report.of("ecf-1 constitution") + report.of("fcf-2 constitution"))


def test_resolve_all_expressions_is_total_over_the_artifact(pub):
    views = resolve_all_expressions(pub)
    assert set(views) == {x.expression_id for x in pub.expressions}
    for v in views.values():
        assert set(v.entries) == set(EXPRESSION_RESPONSIBILITIES)
        assert v.valid


def test_every_ecf_1_identity_key_has_a_canonical_empty_or_is_required():
    """A structural guard on the `ecf-1` totality rule: adding an identity key without deciding its
    canonical empty would raise a bare `KeyError` inside the digest. This is where that is caught."""
    from columna_core.governed.native import _ECF1_EMPTY
    required = {"constructor", "participation"}
    assert set(ECF1_IDENTITY_KEYS) <= required | set(_ECF1_EMPTY)

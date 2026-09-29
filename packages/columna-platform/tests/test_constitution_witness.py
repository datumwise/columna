"""
test_constitution_witness.py — **P-1: a COMPUTED ConstitutionWitness, and the three facts kept apart.**

    *"Make `ConstitutionWitness` derived from identity-bearing governed facts… Keep these three things
    distinct: ConstitutionWitness — which governed analytical constitution this object belongs to;
    AnalyticalInstance / data-state identity — which actual root/evidence state this retained material
    belongs to; Realization standing — which physical/provider/codec realization produced or carries it.
    Do not collapse them into one version/freshness token."*  — Huayin, 2026-09-29

The four **required negative controls** are the four sections marked `NEGATIVE CONTROL n`. Each is written
to fail if the three facts are ever collapsed, which is the failure this unit is against — not a wrong
digest, but a digest that has silently started answering somebody else's question.
"""
from __future__ import annotations

from dataclasses import dataclass, fields, replace

import pyarrow as pa
import pytest

from columna_platform.columnar import ColumnarMME, CoordinateIndex, GovernedBlock, standing
from columna_platform.columnar.provider import ColumnarProvider
from columna_platform.kernel import (
    EXPRESSION_NON_DETERMINANTS,
    FAMILY_NON_DETERMINANTS,
    UNSTATED_DATA_STATE,
    WITNESS_SCHEME,
    AnalyticalInstance,
    ConstitutionWitness,
    GovernedExpression,
    KernelRefusal,
    MeasureFamily,
    Operand,
    RealizationStanding,
    SufficientBasis,
    determinant_names,
)
from columna_platform.kernel import exhibit as KEX
from columna_platform.kernel.witness import _determinants
from columna_platform.columnar import exhibit as CEX

LOAD_A = "load:orders@2026-09-29T08:00Z"
LOAD_B = "load:orders@2026-09-29T17:30Z"


@pytest.fixture
def revenue():
    return KEX._families()[0]


@pytest.fixture
def aov():
    return KEX._expressions()[0]


@pytest.fixture
def mme():
    return KEX.build()


# ══ 0 · COMPUTED, NOT CALLER-SUPPLIED ═════════════════════════════════════════════════════════════
def test_the_witness_is_computed_from_the_declaration(revenue, aov):
    for obj in (revenue, aov):
        witness = obj.witness()
        assert isinstance(witness, ConstitutionWitness)
        assert witness.digest.startswith(f"{WITNESS_SCHEME}:")
        assert witness.scheme == WITNESS_SCHEME
        assert witness.determinants                      # it is derived from something
        # and it is a FUNCTION of the declaration: same declaration, same witness, every time
        assert obj.witness().digest == witness.digest


def test_a_caller_supplied_witness_is_refused_at_construction():
    """*"The witness is computed rather than caller-supplied."* The old `constitution="c0"` slot survives
    only so that supplying one is a refusal rather than a silent no-op."""
    with pytest.raises(KernelRefusal) as exc:
        MeasureFamily(family_id="revenue", manifold=KEX.MANIFOLD, universe="commerce", root=KEX.SALE_AT,
                      law="SUM", value_domain="decimal", participation="p", target="t",
                      constitution="c0")
    assert exc.value.code == "constitution-is-computed"
    assert "NEVER DECLARED" in exc.value.detail

    with pytest.raises(KernelRefusal) as exc:
        GovernedExpression(expression_id="e", manifold=KEX.MANIFOLD, universe="commerce",
                           constructor="MEAN", operands=(Operand("operand", "revenue"),),
                           participation="p", constitution="c0")
    assert exc.value.code == "constitution-is-computed"


def test_both_sorts_are_covered_and_their_witnesses_are_not_comparable(revenue, aov):
    """*"Family and expression witnesses are both covered."* Covered as PEERS: `compare` across the two
    sorts is not a question with an answer, so it says so rather than returning `False` as though the two
    constitutions had been weighed."""
    assert revenue.witness().sort == "family"
    assert aov.witness().sort == "expression"
    verdict = revenue.witness().compare(aov.witness())
    assert not verdict
    assert "not comparable" in verdict.detail and "peers" in verdict.detail


def test_the_witness_answers_which_constitution_and_not_which_object(revenue):
    """A consequence accepted openly, following Core's `NON_IDENTITY_KEYS`: the identity is a LABEL, so
    two objects with identical governed constitutions share a digest — and the witness still names which
    object it is about, beside the digest rather than inside it."""
    renamed = replace(revenue, family_id="revenue_renamed")
    assert renamed.witness().digest == revenue.witness().digest
    assert renamed.witness().identity == "revenue_renamed" != revenue.witness().identity


# ══ NEGATIVE CONTROL 1 · same constitution + new source/root data ══════════════════════════════════
def test_control_1_new_root_data_is_the_same_witness_and_a_different_instance(mme, revenue):
    """*"same constitution + new source/root data → same ConstitutionWitness, different AnalyticalInstance."*"""
    before = mme.witness_of("revenue")
    mme.establish_root(revenue, KEX.ORDERS, data_state=LOAD_A)
    mme.establish_root(revenue, KEX.ORDERS[:4], data_state=LOAD_B)

    assert mme.witness_of("revenue").digest == before.digest          # the constitution did not move
    keys = [k for k in mme.held if k.identity == "revenue" and k.anchor == KEX.SALE_AT]
    witnesses = {k.constitution for k in keys}
    states = {k.data_state for k in keys}
    assert witnesses == {before.digest}                               # ONE constitution
    assert {LOAD_A, LOAD_B} <= states                                 # TWO evidence states
    # two retained objects, NOT a silent overwrite — which is the whole reason the axis exists
    assert len([k for k in keys if k.data_state in (LOAD_A, LOAD_B)]) == 2


def test_control_1_two_evidence_states_are_two_instances_not_one(revenue):
    a = revenue.instance(data_state=LOAD_A)
    b = revenue.instance(data_state=LOAD_B)
    assert a != b
    assert a.same_but_for_data_state(b)                    # every GOVERNED axis agrees
    verdict = a.compatible_with(b)
    assert not verdict and verdict.code == "different-data-state"
    assert "about neither" in verdict.detail
    # and the data state is NOT the constitution: neither instance carries a witness digest at all
    assert not any(f.name == "constitution" for f in fields(AnalyticalInstance))


def test_control_1_the_engine_refuses_to_pick_an_evidence_state(mme, revenue):
    """Two loads under one constitution are both current. The engine does not choose, and does not merge."""
    mme.establish_root(revenue, KEX.ORDERS, data_state=LOAD_A)
    mme.establish_root(revenue, KEX.ORDERS[:2], data_state=LOAD_B)   # a genuinely different D1 total

    ambiguous = mme.measure(revenue, KEX.BY_DAY)
    assert not ambiguous.served and ambiguous.refusal.code == "ambiguous-data-state"
    assert LOAD_A in ambiguous.refusal.detail and LOAD_B in ambiguous.refusal.detail
    assert "NOTHING IS MERGED ACROSS THEM" in ambiguous.refusal.detail

    named = mme.measure(revenue, KEX.BY_DAY, data_state=LOAD_A)
    assert named.served and named.value.instance.data_state == LOAD_A
    other = mme.measure(revenue, KEX.BY_DAY, data_state=LOAD_B)
    assert other.served and other.value.cells[("D1",)] != named.value.cells[("D1",)]


def test_control_1_an_expression_is_attributed_to_its_operands_evidence_state(mme, revenue):
    order_count = KEX._families()[1]
    mme.establish_root(revenue, KEX.ORDERS, data_state=LOAD_A)
    mme.establish_root(order_count, KEX.ORDERS, data_state=LOAD_A)
    served = mme.evaluate(KEX._expressions()[0], KEX.BY_DAY, data_state=LOAD_A)
    assert served.served
    assert served.value.instance.data_state == LOAD_A


# ══ NEGATIVE CONTROL 2 · same analytical meaning + provider/codec change ══════════════════════════
def test_control_2_a_provider_or_carrier_change_moves_only_the_realization_standing():
    """*"same analytical meaning + provider/codec change → same ConstitutionWitness, different realization
    standing."*"""
    arrow, block = CEX.build()
    other_carrier = ColumnarMME(arrow.authority, ColumnarProvider(), carrier="on-disk-arrow-ipc")
    other_carrier.establish(block, "order_count")
    arrow.establish(block, "order_count")

    mine = next(k for k in arrow.held if k.identity == "order_count")
    theirs = next(k for k in other_carrier.held if k.identity == "order_count")

    assert mine.constitution == theirs.constitution                   # the constitution is untouched
    assert mine.instance == theirs.instance                           # so is the analytical instance
    assert mine.realization != theirs.realization                     # only the realization moved
    assert mine.realization.carrier == "in-memory-arrow"
    assert theirs.realization.carrier == "on-disk-arrow-ipc"
    assert mine.realization.provider == theirs.realization.provider


def test_control_2_no_realization_fact_is_a_determinant_of_the_witness(revenue, aov):
    """The structural version of control 2: a provider cannot influence a witness because no realization
    fact is in the determinant set at all."""
    for obj in (revenue, aov):
        rendered = " ".join(f"{n}={v}" for n, v in obj.witness().determinants).lower()
        for realization_word in ("provider", "carrier", "arrow", "datafusion", "in-memory", "codec",
                                 "parquet", "data_state", "load:"):
            assert realization_word not in rendered
        assert "realization" not in obj.witness().names
        assert "data_state" not in obj.witness().names


def test_control_2_realization_standing_is_an_object_and_not_analytical_standing():
    a = RealizationStanding(provider="arrow+datafusion", carrier="in-memory-arrow")
    assert a.token == "arrow+datafusion/in-memory-arrow"
    assert a != replace(a, carrier="parquet")
    # it is NOT on the analytical instance, and that absence is the design
    assert not any(f.name in ("provider", "carrier", "realization")
                   for f in fields(AnalyticalInstance))


# ══ NEGATIVE CONTROL 3 · an identity-bearing change ═══════════════════════════════════════════════
#: Every fact the ruling enumerates: *"root, continuation law, constitutive order, participation law,
#: operand identity, role, constitutive anchor, or identity-bearing parameter"* — plus the two the kernel
#: itself makes identity-bearing (`manifold`, `value_domain`), each as a concrete edit.
FAMILY_IDENTITY_EDITS = [
    ("root", {"root": KEX.STORE_DAY}),
    ("law", {"law": "COUNT", "value_domain": "integer"}),
    ("order_by", {"law": "LAST", "order_by": "recorded_at", "value_domain": "decimal"}),
    ("participation", {"participation": "every order the auditor confirmed"}),
    ("value_domain", {"law": "COUNT", "value_domain": "integer"}),
    ("manifold", {"manifold": "acme.commerce"}),
    ("universe", {"universe": "logistics"}),
    ("parameters", {"parameters": {"lg_k": 14}}),
]


@pytest.mark.parametrize("determinant,edit", FAMILY_IDENTITY_EDITS,
                         ids=[d for d, _ in FAMILY_IDENTITY_EDITS])
def test_control_3_an_identity_bearing_family_change_moves_the_witness(revenue, determinant, edit):
    """*"identity-bearing change … → different ConstitutionWitness."* And it NAMES what moved."""
    moved = replace(revenue, **edit)
    comparison = revenue.witness().compare(moved.witness())
    assert not comparison
    assert moved.witness().digest != revenue.witness().digest
    assert determinant in comparison.changed
    assert "STALE" in comparison.detail and "re-establishment is from the root" in comparison.detail


EXPRESSION_IDENTITY_EDITS = [
    ("operands", {"operands": (Operand("operand", "audited_order_count"),)}),   # operand identity
    ("operands", {"operands": (Operand("divisor", "revenue"),)}),               # the ROLE alone
    ("inner_anchors", {"inner_anchors": (KEX.STORE_DAY,)}),                     # constitutive anchor
    ("participation", {"participation": "something else entirely"}),
    ("constructor", {"constructor": "HLL_ESTIMATE"}),
    ("scope", {"scope": "a different governed scope"}),
    ("parameters", {"parameters": {"rounding": "half-even"}}),
]


@pytest.mark.parametrize("determinant,edit", EXPRESSION_IDENTITY_EDITS,
                         ids=[f"{d}-{i}" for i, (d, _) in enumerate(EXPRESSION_IDENTITY_EDITS)])
def test_control_3_an_identity_bearing_expression_change_moves_the_witness(aov, determinant, edit):
    moved = replace(aov, **edit)
    comparison = aov.witness().compare(moved.witness())
    assert not comparison and determinant in comparison.changed


def test_control_3_the_role_alone_is_identity_bearing(aov):
    """*"operand identity, role"* — the role is an INDEX, so re-indexing the same family is a different
    constitution even though the operand family is untouched."""
    rerolled = replace(aov, operands=(Operand("numerator", "revenue"),))
    assert rerolled.witness().digest != aov.witness().digest
    assert "operands" in aov.witness().compare(rerolled.witness()).changed


# ══ NEGATIVE CONTROL 4 · non-identity metadata / alias / description ══════════════════════════════
def test_control_4_a_description_change_leaves_the_witness_identical(revenue):
    """*"non-identity metadata / alias / description change → same ConstitutionWitness."*"""
    redescribed = replace(revenue, target="the money we took, phrased for the board deck")
    assert redescribed.witness().digest == revenue.witness().digest
    assert revenue.witness().compare(redescribed.witness())
    assert "target" not in revenue.witness().names


def test_control_4_admitting_another_route_leaves_the_witness_identical(aov):
    """Ruled 2026-09-28: *"expression identity ≠ one particular sufficient basis used to establish it."*
    A basis is a ROUTE, so admitting one must not stale values already established over another."""
    widened = replace(aov, admitted_bases=aov.admitted_bases + (
        SufficientBasis(basis_id="b_alternative",
                        components={"SUM": "revenue", "COUNT": "audited_order_count"},
                        requires_common_participation=True),))
    assert widened.witness().digest == aov.witness().digest
    assert "admitted_bases" not in aov.witness().names


def test_control_4_a_value_established_under_one_route_survives_admitting_another(mme):
    """The behavioural form of the same control — not just an equal digest, an unstaled value."""
    aov = KEX._expressions()[0]
    served = mme.evaluate(aov, KEX.BY_DAY)
    assert served.served and served.seeded_from == "b_revenue_ordercount"

    widened = replace(aov, admitted_bases=aov.admitted_bases + (
        SufficientBasis(basis_id="b_alternative",
                        components={"SUM": "revenue", "COUNT": "audited_order_count"},
                        requires_common_participation=True),))
    mme.register_expression(widened)
    assert mme.stale_states() == ()                        # nothing became stale
    again = mme.evaluate(widened, KEX.BY_DAY)
    assert again.route == CACHED_ROUTE
    assert again.value.cells[("D1",)] == served.value.cells[("D1",)]


CACHED_ROUTE = "cached"


# ══ STALENESS — MECHANICALLY DETECTABLE, AND NAMED ════════════════════════════════════════════════
def test_a_constitution_change_makes_held_state_detectably_stale(mme, revenue):
    """*"Staleness due to constitution change is mechanically detectable."* Detectable, and diagnosable:
    the report names the determinant that moved."""
    assert mme.stale_states() == ()

    superseded = replace(revenue, participation="every order the auditor confirmed")
    mme.register_family(superseded)

    stale = mme.stale_states()
    assert [s.key.identity for s in stale] == ["revenue"]
    assert stale[0].changed == ("participation",)
    assert stale[0].held_under != stale[0].current.digest
    assert "re-establishment is from the root" in stale[0].detail


def test_a_stale_state_is_not_served_and_the_refusal_says_it_is_held(mme, revenue):
    """The state is right there. It is not served, and the refusal does not pretend nothing was held."""
    superseded = replace(revenue, participation="every order the auditor confirmed")
    mme.register_family(superseded)

    answer = mme.measure(superseded, KEX.BY_DAY)
    assert not answer.served
    assert "STALE" in answer.refusal.detail
    assert "superseded constitution witness" in answer.refusal.detail
    assert "stale_states()" in answer.refusal.detail


def test_re_establishing_under_the_new_constitution_serves_again(mme, revenue):
    superseded = replace(revenue, participation="every order the auditor confirmed")
    mme.register_family(superseded)
    assert not mme.measure(superseded, KEX.BY_DAY).served

    mme.establish_root(superseded, KEX.ORDERS)
    served = mme.measure(superseded, KEX.BY_DAY)
    assert served.served
    # the stale state is STILL held and still reported — nothing was patched or quietly dropped
    assert any(s.key.identity == "revenue" for s in mme.stale_states())


def test_the_three_facts_move_independently(mme, revenue):
    """**THE COLLAPSE TEST.** One edit at a time, and exactly one axis moves for each."""
    base_witness = revenue.witness().digest
    base_instance = revenue.instance()

    # 1 · the DECLARATION moves: witness changes, instance's governed axes may or may not, data state does not
    declaration_moved = replace(revenue, root=KEX.STORE_DAY)
    assert declaration_moved.witness().digest != base_witness
    assert declaration_moved.instance().data_state == base_instance.data_state

    # 2 · the DATA moves: witness identical, instance different
    reloaded = revenue.instance(data_state=LOAD_A)
    assert revenue.witness().digest == base_witness
    assert reloaded != base_instance and reloaded.same_but_for_data_state(base_instance)

    # 3 · the REALIZATION moves: witness identical, instance identical
    one = RealizationStanding(provider="in-memory", carrier="in-memory")
    two = RealizationStanding(provider="in-memory", carrier="arrow-ipc")
    assert one != two
    assert revenue.witness().digest == base_witness and revenue.instance() == base_instance


def test_the_retention_key_references_all_three_separately(mme):
    """*"…even if a later retention key combines references to all three."* It does; they stay three."""
    key = next(k for k in mme.held if k.identity == "revenue")
    assert key.constitution == mme.witness_of("revenue").digest      # fact 1
    assert key.instance.data_state == UNSTATED_DATA_STATE            # fact 2
    assert key.realization == RealizationStanding(provider="in-memory", carrier="in-memory")  # fact 3
    names = {f.name for f in fields(type(key))}
    assert {"constitution", "instance", "realization"} <= names


# ══ THE DETERMINANT SET ITSELF ════════════════════════════════════════════════════════════════════
def test_the_determinants_are_derived_by_subtraction_so_a_new_field_is_identity_bearing():
    """The direction that matters. A field ADDED to a governed record enters the witness with no code
    change; the danger is only ever the other way, and the other way requires writing an exclusion down."""
    assert determinant_names("family", MeasureFamily) == tuple(sorted(
        {f.name for f in fields(MeasureFamily)} - FAMILY_NON_DETERMINANTS))
    assert determinant_names("expression", GovernedExpression) == tuple(sorted(
        {f.name for f in fields(GovernedExpression)} - EXPRESSION_NON_DETERMINANTS))

    @dataclass(frozen=True)
    class LaterFamily:
        family_id: str
        target: str
        constitution: str
        root: str
        newly_added_governed_fact: str

    determinants = dict(_determinants(LaterFamily("f", "t", None, "r", "x"),
                                      FAMILY_NON_DETERMINANTS, "family"))
    assert "newly_added_governed_fact" in determinants


def test_an_exclusion_that_outlives_its_field_is_refused():
    """An exclusion naming nothing would quietly stop excluding anything."""
    @dataclass(frozen=True)
    class WithoutTarget:
        family_id: str
        constitution: str
        root: str

    with pytest.raises(KernelRefusal) as exc:
        _determinants(WithoutTarget("f", None, "r"), FAMILY_NON_DETERMINANTS, "family")
    assert exc.value.code == "stale-non-determinant"


def test_every_ruled_identity_bearing_fact_is_a_determinant(revenue, aov):
    """The ruling's enumeration, checked as a set rather than one edit at a time."""
    assert {"root", "law", "order_by", "participation", "parameters", "value_domain",
            "manifold", "universe"} <= set(revenue.witness().names)
    assert {"operands", "inner_anchors", "participation", "constructor",
            "parameters"} <= set(aov.witness().names)


def test_the_witness_is_not_cores_family_fingerprint():
    """Two schemes that could be confused would be worse than two that obviously cannot. `cw-1` is not
    `fcf-1`/`fcf-2`, carries different determinants, and nothing imports either across the boundary."""
    assert WITNESS_SCHEME == "cw-1"
    assert not WITNESS_SCHEME.startswith("fcf")


def test_asking_a_witness_about_a_non_determinant_refuses(revenue):
    with pytest.raises(KernelRefusal) as exc:
        revenue.witness().determinant("target")
    assert exc.value.code == "not-a-determinant"


# ══ THE COLUMNAR SUBSTRATE CARRIES THE SAME THREE FACTS ═══════════════════════════════════════════
def test_the_columnar_engine_stamps_the_data_state_at_establishment():
    mme, block = CEX.build()
    state = mme.establish(block, "order_count", data_state=LOAD_A)
    assert state.instance.data_state == LOAD_A
    assert state.standing.instance.data_state == LOAD_A          # the standing agrees with the state
    key = next(k for k in mme.held if k.identity == "order_count" and k.data_state == LOAD_A)
    assert key.anchor == CEX.SALE_AT
    assert key.constitution == mme.authority.witness_of("order_count").digest


def test_the_columnar_engine_carries_the_data_state_through_a_continuation():
    mme, block = CEX.build()
    mme.establish(block, "order_count", data_state=LOAD_A)
    served = mme.measure("order_count", CEX.BY_DAY, data_state=LOAD_A)
    assert served.served and served.value.instance.data_state == LOAD_A


def test_two_columnar_evidence_states_are_two_retained_objects():
    mme, block = CEX.build()
    mme.establish(block, "order_count", data_state=LOAD_A)
    mme.establish(block, "order_count", data_state=LOAD_B)
    keys = [k for k in mme.held if k.identity == "order_count" and k.anchor == CEX.SALE_AT]
    assert {LOAD_A, LOAD_B} <= {k.data_state for k in keys}
    assert len({k.constitution for k in keys}) == 1
    ambiguous = mme.measure("order_count", CEX.BY_DAY)
    assert not ambiguous.served and ambiguous.refusal.code == "ambiguous-data-state"


def test_a_columnar_block_may_declare_its_data_state_but_not_its_constitution():
    """The corrected form of "a block does not get to declare a family's instance": what a block carries
    IS material from some evidence state, and that much it may say. Everything governed must still agree."""
    mme, block = CEX.build()
    mme.establish(block, "revenue", data_state=LOAD_A)            # allowed, and stamped

    foreign = GovernedBlock.of(
        block.index, {"revenue": block.column("revenue")},
        {"revenue": standing("revenue",
                             replace(mme.authority.instance_of("revenue"),
                                     participation="something else"),
                             n=len(block.index))})
    with pytest.raises(KernelRefusal) as exc:
        mme.establish(foreign, "revenue")
    assert exc.value.code == "block-instance-mismatch"
    assert "WHAT A BLOCK MAY DECLARE IS THE DATA STATE" in exc.value.detail


def test_the_columnar_engine_reports_staleness_through_the_authority():
    """Not reimplemented in the substrate, for the same reason `adjudicate` is not."""
    mme, block = CEX.build()
    mme.establish(block, "order_count", data_state=LOAD_A)
    assert mme.stale_states() == ()

    moved = replace(mme.family("order_count"), participation="a different population")
    mme.authority.register_family(moved)
    stale = mme.stale_states()
    assert {s.key.identity for s in stale} == {"order_count"}
    assert all(s.changed == ("participation",) for s in stale)
    assert not mme.measure("order_count", CEX.BY_DAY).served


def test_a_columnar_expression_is_attributed_to_its_operands_evidence_state():
    settled, block = CEX.build(settled=True)
    for family_id in ("revenue", "order_count"):
        settled.establish(block, family_id, data_state=LOAD_A)
    served = settled.evaluate("average_order_value", CEX.BY_DAY, data_state=LOAD_A)
    assert served.served
    assert served.value.instance.data_state == LOAD_A


def test_a_value_bearing_want_of_state_refusal_survives_the_new_axes():
    """The #349 correction is untouched by P-1: the want-of-state refusal is about EVIDENCE FOR A VALUE at
    a point, and the data state is about which established material a whole column came from. Two
    different facts, and adding the second did not soften the first."""
    mme, block = CEX.build()
    for family_id in ("revenue", "order_count"):
        mme.establish(block, family_id, data_state=LOAD_A)
    answer = mme.measure("revenue", CEX.BY_DAY, data_state=LOAD_A)
    assert not answer.served and answer.refusal.code == "want-of-state"
    assert mme.measure("order_count", CEX.BY_DAY, data_state=LOAD_A).value.cell(("D1",)) == 3


def test_arrow_null_still_has_no_standing_of_its_own():
    """*"Arrow NULL remains physically meaningless unless governed standing gives it meaning."* Preserved
    from #349, restated here because P-1 touched the establishment path."""
    mme, block = CEX.build()
    assert block.column("revenue").null_count == 1
    position = block.index.position(CEX.UNSUPPORTED_POINT)
    assert block.standing("revenue").participation[position].as_py() is True
    assert sum(block.contributing_domain("revenue").to_pylist()) == len(block.index)
    dense = GovernedBlock.of(
        CoordinateIndex.of(CEX.MANIFOLD, CEX.SALE_AT, [("D1", "O1", "S1"), ("D1", "O2", "S1")]),
        {"order_count": pa.array([1, 1], type=pa.int64())},
        {"order_count": standing("order_count", mme.authority.instance_of("order_count"), n=2,
                                 support=[True, False])})
    assert dense.column("order_count").null_count == 0
    assert not dense.wants_state("order_count", "population")     # a COUNT needs no value evidence

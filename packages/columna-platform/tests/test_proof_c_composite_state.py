"""PROOF C — composite sufficient state, and the standing its components must share.

    A governed family may require composite sufficient state whose components must share one
    participation history, and the finalized displayed value is not interchangeable with that state.

The controls below all use values that ADD UP. Every refusal is a refusal of standing, never of
arithmetic — which is the proposition: matching analytical identity is necessary and not sufficient.
"""
from dataclasses import replace
from decimal import Decimal

import pytest

from columna_core.governed.foundation import LAWS, StateBasis
from columna_platform import composite, serving
from columna_platform.refusals import WantOfCompatibility, WantOfLaw, WantOfState
from columna_platform.state import AnalyticalIdentity, RetainedState, RetainedStateStore, Standing

from conftest import MEAN_ID

STANDING = Standing(constitution="fcf-1:abc", constitution_scheme="fcf-1",
                    participation="every sale point carrying a recorded amount",
                    basis="matching (SUM, COUNT)", realization="warehouse:sales.fact_sale.amount",
                    currency="tok-1")


def _retained(state):
    return RetainedState(identity=AnalyticalIdentity(MEAN_ID, "sale_at"), standing=STANDING,
                         array=None, governed_domain="decimal", composite=state)


# ══ THE BASIS IS READ FROM GOVERNED LAW ══════════════════════════════════════════════════════════
def test_the_basis_comes_from_c7_not_from_this_module(mean_view):
    basis = composite.declared_basis(mean_view)
    assert isinstance(basis, StateBasis)
    assert basis.components == ("SUM", "COUNT")
    assert basis.requires_common_participation is True


def test_a_scalar_basis_is_not_repackaged_as_a_composite(governed):
    """`revenue` has a scalar C7. This path refuses it rather than wrapping it in a tuple."""
    _pub, views, _m, _f = governed
    with pytest.raises(WantOfLaw, match="scalar"):
        composite.declared_basis(views["fam_qv8Ky3mR7bTpZa1LwXcNdg"])


def test_the_count_component_continues_under_the_law_the_foundation_names(mean_view, admitted_pair):
    """NOT under COUNT because it is called count. `COUNT.usable_as_continuation` is False."""
    a, _b = admitted_pair
    state = composite.constitute(mean_view, a, anchor="sale_at")

    assert LAWS["COUNT"].usable_as_continuation is False
    assert LAWS["COUNT"].composition is None
    assert LAWS["COUNT"].entails_continuation == "SUM"
    assert state.component("COUNT").continues_under == LAWS["COUNT"].entails_continuation == "SUM"
    assert state.component("SUM").continues_under == "SUM"


# ══ POSITIVE CONTROL ═════════════════════════════════════════════════════════════════════════════
def test_one_pass_constitutes_both_components_under_one_witness(mean_view, admitted_pair):
    a, _b = admitted_pair
    state = composite.constitute(mean_view, a, anchor="sale_at")

    assert state.component("SUM").value == Decimal("30.0000")
    assert state.component("COUNT").value == 3
    assert state.component("SUM").witness is state.component("COUNT").witness
    assert state.witness.participation == "every sale point carrying a recorded amount"


def test_the_basis_continues_lawfully_and_finalizes_exactly(mean_view, admitted_pair):
    a, b = admitted_pair
    combined = composite.continue_composite(composite.constitute(mean_view, a, anchor="sale_at"),
                                            composite.constitute(mean_view, b, anchor="sale_at"))

    assert combined.component("SUM").value == Decimal("36.0000")
    assert combined.component("COUNT").value == 4

    final = composite.finalize(combined)
    assert final.value == Decimal("9")                       # 36.0000 / 4, exactly
    assert final.is_sufficient_state is False


def test_the_mean_serves_through_the_real_wire(mean_view, admitted_pair):
    a, b = admitted_pair
    combined = composite.continue_composite(composite.constitute(mean_view, a, anchor="sale_at"),
                                            composite.constitute(mean_view, b, anchor="sale_at"))
    store = RetainedStateStore()
    store.insert(_retained(combined))

    w = serving.decide(mean_view, store, AnalyticalIdentity(MEAN_ID, "sale_at"), column="mean_revenue")

    assert w["contract_version"] == "5"
    assert w["outcome"] == "serve"
    assert w["columns"][0]["value"] == Decimal("9")


# ══ NEGATIVE CONTROL 1 · a finalized scalar is not sufficient state ══════════════════════════════
def test_offering_a_finalized_value_back_as_state_refuses(mean_view, admitted_pair):
    a, _b = admitted_pair
    final = composite.finalize(composite.constitute(mean_view, a, anchor="sale_at"))

    with pytest.raises(WantOfState) as e:
        composite.offer_as_state(final)
    assert "not sufficient state" in str(e.value)
    assert "Re-materializing the basis would resolve this" in str(e.value)


def test_the_store_refuses_to_retain_a_finalized_value(mean_view, admitted_pair):
    a, _b = admitted_pair
    st = _retained(composite.constitute(mean_view, a, anchor="sale_at"))

    with pytest.raises(WantOfState):
        RetainedStateStore().insert(replace(st, finalized=True))


# ══ NEGATIVE CONTROL 2 · pairing after the fact ══════════════════════════════════════════════════
def test_independently_retained_components_may_not_be_paired(mean_view, admitted_pair):
    """THE KEY CONTROL. Both states are valid. Their numbers are the same numbers. They still refuse."""
    a, _b = admitted_pair
    one = composite.constitute(mean_view, a, anchor="sale_at")
    two = composite.constitute(mean_view, a, anchor="sale_at")     # same values, separate pass

    assert one.component("SUM").value == two.component("SUM").value
    assert one.component("COUNT").value == two.component("COUNT").value
    assert one.witness.same_participation(two.witness)             # same rule...
    assert not one.witness.matches(two.witness)                    # ...different pass

    with pytest.raises(WantOfCompatibility) as e:
        composite.pair(one.component("SUM"), two.component("COUNT"),
                       family_id=MEAN_ID, anchor="sale_at")
    assert "not constituted in one pass" in str(e.value)
    assert "Equal-looking values do not establish" in str(e.value)


def test_pairing_components_from_one_pass_is_the_only_thing_that_works(mean_view, admitted_pair):
    a, _b = admitted_pair
    one = composite.constitute(mean_view, a, anchor="sale_at")
    paired = composite.pair(one.component("SUM"), one.component("COUNT"),
                            family_id=MEAN_ID, anchor="sale_at")
    assert composite.finalize(paired).value == Decimal("10")       # 30.0000 / 3


# ══ NEGATIVE CONTROL 3 · same identity, different participation standing ═════════════════════════
def test_differing_participation_standing_refuses_and_numbers_do_not_rescue_it(mean_view,
                                                                               admitted_pair):
    a, _b = admitted_pair
    one = composite.constitute(mean_view, a, anchor="sale_at")
    other_rule = replace(one.witness, participation="every sale point, including zero-amount sales",
                         pass_id="other")
    two = replace(one, witness=other_rule,
                  components=tuple(replace(c, witness=other_rule) for c in one.components))

    assert one.component("SUM").value == two.component("SUM").value      # identical numbers
    assert one.family_id == two.family_id and one.anchor == two.anchor   # identical identity

    with pytest.raises(WantOfCompatibility) as e:
        composite.continue_composite(one, two)
    assert "different participation standing" in str(e.value)


# ══ NEGATIVE CONTROL 4 · a corrupted component, numerically plausible ════════════════════════════
def test_a_corrupted_component_refuses_before_arithmetic(mean_view, admitted_pair):
    """The COUNT value is left plausible; only its standing is wrong. It must refuse anyway."""
    a, _b = admitted_pair
    state = composite.constitute(mean_view, a, anchor="sale_at")
    forged = replace(state.component("COUNT"),
                     witness=replace(state.witness, pass_id="forged"))
    corrupted = replace(state, components=(state.component("SUM"), forged))

    assert corrupted.component("COUNT").value == 3          # still the right number
    with pytest.raises(WantOfCompatibility) as e:
        composite.finalize(corrupted)
    assert "may look plausible and the standing does not hold" in str(e.value)


def test_the_standing_checks_run_before_any_division(mean_view, admitted_pair):
    """A count of zero would raise on division. The standing check must fire FIRST."""
    a, _b = admitted_pair
    state = composite.constitute(mean_view, a, anchor="sale_at")
    forged_witness = replace(state.witness, pass_id="forged")
    both_wrong = replace(state, components=tuple(
        replace(c, witness=forged_witness, value=0 if c.law == "COUNT" else c.value)
        for c in state.components))

    with pytest.raises(WantOfCompatibility):        # not ZeroDivisionError, not WantOfState
        composite.finalize(both_wrong)


# ══ the unruled question stays unruled ═══════════════════════════════════════════════════════════
def test_an_inexact_mean_refuses_rather_than_deciding_the_open_question(mean_view, admitted_pair):
    """10.0000 / 3 has no finite decimal representation. Proof C does NOT rule on it."""
    a, _b = admitted_pair
    state = composite.constitute(mean_view, a, anchor="sale_at")
    inexact = replace(state, components=(
        replace(state.component("SUM"), value=Decimal("10.0000")), state.component("COUNT")))

    with pytest.raises(WantOfState) as e:
        composite.finalize(inexact)
    assert "UNRULED" in str(e.value)
    assert "does not decide them" in str(e.value)


def test_participation_must_be_established_before_a_common_participation_basis(
        mean_view_without_participation, admitted_pair):
    """A basis that REQUIRES common participation cannot be constituted where C5 is unestablished.

    Uses a publication variant that genuinely omits `participation`, rather than poking a frozen
    resolved value — a test that manufactures the state it checks proves only that the poke worked."""
    a, _b = admitted_pair
    view = mean_view_without_participation
    assert view["eligibility_and_participation"].standing == "unestablished"

    with pytest.raises(WantOfLaw, match="COMMON participation"):
        composite.constitute(view, a, anchor="sale_at")


def test_the_carriers_really_passed_admission(admitted_pair):
    """The premise, asserted: `constitute` reads ADMITTED carriers, not raw ones."""
    a, b = admitted_pair
    for adm in (a, b):
        assert adm.governed_domain == "decimal"
        assert adm.carrier_type == "decimal128(18, 4)"


# ══ the mechanism is not the requirement ═════════════════════════════════════════════════════════
def test_the_pass_id_boundary_is_recorded_verbatim():
    """The token is concrete, checked, and works — which is exactly why it could be mistaken for the
    governed fact. It is not one."""
    assert composite.PASS_ID_BOUNDARY == (
        "pass_id is a Proof-C runtime witness of common constitution, not a frozen "
        "constitutional/public representation of participation standing. The governing requirement "
        "is shared participation provenance; the current token mechanism is one implementation of "
        "that requirement."
    )


def test_the_two_witness_strengths_stay_distinct(mean_view, admitted_pair):
    """Pinned so neither is quietly widened into the other.

    Collapsing them breaks one half of the proposition in each direction: `matches` everywhere makes
    lawful continuation impossible (it crosses passes by nature); `same_participation` everywhere
    lets the after-the-fact pair through."""
    a, b = admitted_pair
    one = composite.constitute(mean_view, a, anchor="sale_at")
    two = composite.constitute(mean_view, b, anchor="sale_at")

    assert one.witness.same_participation(two.witness)      # same governed rule
    assert not one.witness.matches(two.witness)             # different constitution pass

    composite.continue_composite(one, two)                  # permitted on the weaker test
    with pytest.raises(WantOfCompatibility):                # refused on the stronger one
        composite.pair(one.component("SUM"), two.component("COUNT"),
                       family_id=MEAN_ID, anchor="sale_at")

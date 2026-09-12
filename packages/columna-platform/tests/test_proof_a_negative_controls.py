"""THE NEGATIVE CONTROLS — measured, not contrived.

Every carrier below DELIVERS. Nothing raises on the way in. If admission defaulted to accept, each
one would be served as though it were governed law — which is the whole reason the boundary exists.
"""
import pytest

from columna_platform import carrier, serving
from columna_platform.refusals import WantOfCompatibility, WantOfLaw, WantOfState
from columna_platform.state import AnalyticalIdentity, RetainedStateStore, Standing
from columna_platform import admission

from test_proof_a_lawful import _materialize


# ── CONTROL 1 · a successfully delivered carrier that is not the governed thing ──────────────────
def test_binary_float_carrier_is_refused_though_delivery_succeeded(revenue):
    family, view, real = revenue
    with pytest.raises(WantOfState) as e:
        admission.admit(view, real, carrier.lossy_float())
    assert "binary floating-point carrier" in str(e.value)
    assert "SOURCE LOSS" in str(e.value)                 # the MEASURED failure, cited in the refusal
    assert e.value.jurisdiction == "realization"
    assert e.value.remedy == "re-realization would resolve this"


def test_the_fourth_hop_is_refused_even_though_arrow_held_it_exactly(revenue):
    """decimal128(38,0): exact in Arrow, lost on the in-process conversion. Nothing raises."""
    family, view, real = revenue
    with pytest.raises(WantOfState) as e:
        admission.admit(view, real, carrier.over_envelope())
    assert "four hops" in str(e.value)
    assert "POLARS LOSS" in str(e.value)


# ── CONTROL 2 · want-of-law and want-of-state are distinguishable ────────────────────────────────
def test_a_coarser_anchor_without_a_movement_licence_is_want_of_law(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)

    out = serving.decide(view, store, AnalyticalIdentity(family.family_id, "sale_at"),
                         at_anchor="month")

    assert out.mood == "refuse"
    assert out.condition == "WantOfLaw"
    assert out.jurisdiction == "governed"
    assert out.remedy is None                       # re-realization cannot supply a licence
    assert "governed movement is unestablished" in out.detail


def test_after_eviction_the_same_ask_is_want_of_state(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)
    identity = AnalyticalIdentity(family.family_id, "sale_at")
    assert store.evict(identity) == 1

    out = serving.decide(view, store, identity)

    assert out.condition == "WantOfState"
    assert out.jurisdiction == "realization"
    assert out.remedy == "re-realization would resolve this"


def test_the_two_refusals_are_not_the_same_refusal(revenue):
    """The controls are worthless unless the two outcomes actually differ."""
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)
    identity = AnalyticalIdentity(family.family_id, "sale_at")

    law = serving.decide(view, store, identity, at_anchor="month")
    store.evict(identity)
    state = serving.decide(view, store, identity)

    assert (law.condition, law.jurisdiction, law.remedy) != (state.condition, state.jurisdiction,
                                                             state.remedy)


def test_eviction_never_converts_a_want_of_state_into_a_want_of_law(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)
    identity = AnalyticalIdentity(family.family_id, "sale_at")
    store.evict(identity)

    out = serving.decide(view, store, identity)
    assert out.condition != "WantOfLaw"


def test_law_is_asked_before_state(revenue):
    """With BOTH defects present the refusal must name the law, not the missing state."""
    family, view, real = revenue
    store = RetainedStateStore()          # nothing retained AND no movement licence
    out = serving.decide(view, store, AnalyticalIdentity(family.family_id, "sale_at"),
                         at_anchor="month")
    assert out.condition == "WantOfLaw"


# ── CONTROL 3 · a finalized value offered back as sufficient state ───────────────────────────────
def test_a_finalized_value_is_not_sufficient_state(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    st = _materialize(family, view, real, store)
    final = store.finalize(st)

    with pytest.raises(WantOfLaw):
        store.combine(final, st)


# ── CONTROL 4 · absence, and the substitution Proof A refuses to make ────────────────────────────
def test_an_absent_observation_refuses_because_empty_fiber_answers_a_different_question(revenue):
    """C9 is ESTABLISHED here — and still does not govern absence. See admission.py FINDING 3."""
    family, view, real = revenue
    assert view["exceptional_cases"].standing == "established"
    assert view["exceptional_cases"].value == {"empty_fiber": "identity"}

    with pytest.raises(WantOfLaw) as e:
        admission.admit(view, real, carrier.with_absence())

    assert "empty_fiber" in str(e.value).lower() or "EMPTY FIBER" in str(e.value)
    assert "ABSENT OBSERVATION" in str(e.value)


# ── CONTROL 5 · standing, not identity, is what blocks reuse ─────────────────────────────────────
def test_identical_identity_with_incompatible_standing_is_neither_law_nor_state(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    a = _materialize(family, view, real, store)
    b = _materialize(family, view, real, store)
    b = b.__class__(**{**b.__dict__,
                       "standing": Standing(**{**b.standing.__dict__,
                                               "participation": "listwise"})})

    with pytest.raises(WantOfCompatibility) as e:
        store.combine(a, b)
    assert e.value.remedy is None                     # nothing is missing; both states are valid


def test_a_none_currency_token_closes_reuse(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    a = _materialize(family, view, real, store, currency=None)
    b = _materialize(family, view, real, store, currency=None)

    with pytest.raises(WantOfState):
        store.combine(a, b)


def test_retrieve_returns_several_standings_and_never_merges_them(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store, currency="tok-1")
    _materialize(family, view, real, store, currency="tok-2")

    held = store.retrieve(AnalyticalIdentity(family.family_id, "sale_at"))
    assert len(held) == 2
    assert {s.standing.currency for s in held} == {"tok-1", "tok-2"}

    out = serving.decide(view, store, AnalyticalIdentity(family.family_id, "sale_at"))
    assert out.condition == "WantOfState"
    assert "MERGING THEM HERE IS NOT PERMITTED" in out.detail


def test_insert_requires_realization_standing(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    st = _materialize(family, view, real, store)
    bare = st.__class__(**{**st.__dict__,
                           "standing": Standing(**{**st.standing.__dict__, "realization": None})})
    with pytest.raises(WantOfState):
        store.insert(bare)

"""THE NEGATIVE CONTROLS — measured, not contrived.

Every carrier below DELIVERS. Nothing raises on the way in. If admission defaulted to accept, each
one would be served as though it were governed law — which is the whole reason the boundary exists.
"""
import pytest

from columna_platform import carrier, serving
from columna_platform.refusals import WantOfCompatibility, WantOfLaw, WantOfState
from columna_platform.state import AnalyticalIdentity, RetainedStateStore, Standing
from columna_platform import admission
from columna_core.disclosure import jurisdiction_for
from conftest import alternatives, no_result, reason

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


# ── CONTROL 2 · want-of-law and want-of-state are distinguishable ON THE WIRE ────────────────────
def test_a_coarser_anchor_without_a_movement_licence_is_want_of_law(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)

    w = serving.decide(view, store, AnalyticalIdentity(family.family_id, "sale_at"), at_anchor="month")

    assert w["outcome"] == "refuse"
    assert reason(w) == "want_of_law"
    assert jurisdiction_for("want_of_law") == "analytical"
    assert alternatives(w) == []                    # re-realization cannot supply a licence
    assert "governed movement is unestablished" in no_result(w)["detail"]


def test_no_admissible_state_is_want_of_state_and_carries_its_remedy(revenue):
    family, view, real = revenue
    store = RetainedStateStore()                     # no state, and NO re-materialization path

    w = serving.decide(view, store, AnalyticalIdentity(family.family_id, "sale_at"))

    assert w["outcome"] == "refuse"
    assert reason(w) == "want_of_state"
    assert jurisdiction_for("want_of_state") == "realization"
    assert alternatives(w) == ["re-realization / re-materialization may resolve this"]


def test_the_two_refusals_differ_in_reason_and_jurisdiction(revenue):
    """The controls are worthless unless the two outcomes actually differ where it counts."""
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)
    identity = AnalyticalIdentity(family.family_id, "sale_at")

    law = serving.decide(view, store, identity, at_anchor="month")
    store.evict(identity)
    state = serving.decide(view, store, identity)

    assert reason(law) != reason(state)
    assert jurisdiction_for(reason(law)) != jurisdiction_for(reason(state))
    # ...and both are REFUSE. The mood is not what carries the distinction; jurisdiction is.
    assert law["outcome"] == state["outcome"] == "refuse"


def test_a_state_failure_never_borrows_an_analytical_reason(revenue):
    family, view, real = revenue
    w = serving.decide(view, RetainedStateStore(), AnalyticalIdentity(family.family_id, "sale_at"))
    assert jurisdiction_for(reason(w)) == "realization"


def test_a_state_failure_is_never_reported_as_error(revenue):
    """The defect the minted reason exists to end: `error` sends an operator hunting a bug."""
    family, view, real = revenue
    w = serving.decide(view, RetainedStateStore(), AnalyticalIdentity(family.family_id, "sale_at"))
    assert no_result(w)["kind"] == "refuse"


# ── A RETRIEVAL MISS IS NOT A REFUSAL (ruled 2026-09-12) ─────────────────────────────────────────
def test_an_evicted_state_is_re_established_transparently_and_serves(revenue):
    """`want_of_state` is NOT "evicted". Where a path exists, the caller never learns of the miss."""
    family, view, real = revenue
    identity = AnalyticalIdentity(family.family_id, "sale_at")
    store = RetainedStateStore()

    def rematerialize(_ident):
        return _materialize(family, view, real, store, currency="tok-2")

    _materialize(family, view, real, store)
    store.evict(identity)
    store._rematerializer = rematerialize

    w = serving.decide(view, store, identity)

    assert w["outcome"] == "serve"                  # NOT a refusal
    assert store.rematerializations == 1


def test_refusal_needs_no_admissible_path_not_merely_a_miss(revenue):
    """A path that cannot produce ADMISSIBLE state refuses — because nothing can establish it now."""
    family, view, real = revenue
    store = RetainedStateStore(rematerializer=lambda _i: None)

    w = serving.decide(view, store, AnalyticalIdentity(family.family_id, "sale_at"))

    assert reason(w) == "want_of_state"
    assert store.rematerializations == 0


def test_eviction_is_not_a_wire_reason():
    """Naming the cache outcome would freeze an implementation detail into public vocabulary."""
    from columna_core.disclosure import REASON_OUTCOME
    assert "evicted" not in REASON_OUTCOME
    assert not any("evict" in r for r in REASON_OUTCOME)


# ── C3 CONTENT, NOT C3 STANDING (ruled 2026-09-12) ───────────────────────────────────────────────
def test_a_domain_alone_does_not_permit_movement(revenue, domain_only_view):
    """THE CONTROL THE ORIGINAL GUARD WOULD HAVE FAILED.

    C3 resolves ESTABLISHED here — off the DOMAIN — while no movement is licensed. The old guard
    tested `standing != ESTABLISHED` and would have let this serve at a coarser anchor."""
    family, _view, real = revenue
    store = RetainedStateStore()
    _materialize(family, domain_only_view, real, store)

    assert domain_only_view["domain_and_movement"].standing == "established"   # the trap
    assert domain_only_view["domain_and_movement"].value["movement"] is None

    w = serving.decide(domain_only_view, store, AnalyticalIdentity(family.family_id, "sale_at"),
                       at_anchor="store")

    assert w["outcome"] == "refuse"
    assert reason(w) == "want_of_law"
    assert "established by its DOMAIN alone" in no_result(w)["detail"]


def test_the_licence_reader_returns_none_for_a_domain_only_c3(domain_only_view):
    assert serving.movement_licence(domain_only_view) is None


def test_an_explicit_none_movement_also_refuses_and_says_so(revenue, declared_no_movement_view):
    """A POSITIVE negative is not the same as silence, and the refusal must not spell them alike."""
    family, _view, real = revenue
    store = RetainedStateStore()
    _materialize(family, declared_no_movement_view, real, store)

    w = serving.decide(declared_no_movement_view, store,
                       AnalyticalIdentity(family.family_id, "sale_at"), at_anchor="store")

    assert reason(w) == "want_of_law"
    assert "DECLARED that no movement is licensed" in no_result(w)["detail"]
    assert serving.movement_licence(declared_no_movement_view) is None


def test_the_three_no_licence_cases_are_distinguishable(revenue, domain_only_view,
                                                        declared_no_movement_view):
    """All three refuse want_of_law; an operator must still be able to tell them apart."""
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)
    ident = AnalyticalIdentity(family.family_id, "sale_at")

    details = set()
    for v in (view, domain_only_view, declared_no_movement_view):
        st = RetainedStateStore()
        _materialize(family, v, real, st)
        w = serving.decide(v, st, ident, at_anchor="store")
        assert reason(w) == "want_of_law"
        details.add(no_result(w)["detail"])
    assert len(details) == 3


def test_the_governing_rule_is_recorded_verbatim():
    assert serving.RESPONSIBILITY_STANDING_RULE == (
        "Standing of a responsibility does not imply establishment of every fact that may appear "
        "inside that responsibility."
    )


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

    w = serving.decide(view, store, AnalyticalIdentity(family.family_id, "sale_at"))
    assert reason(w) == "want_of_state"
    assert "MERGING THEM HERE IS NOT PERMITTED" in no_result(w)["detail"]


def test_insert_requires_realization_standing(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    st = _materialize(family, view, real, store)
    bare = st.__class__(**{**st.__dict__,
                           "standing": Standing(**{**st.standing.__dict__, "realization": None})})
    with pytest.raises(WantOfState):
        store.insert(bare)

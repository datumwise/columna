"""PROOF B — one positively licensed movement, and three that are not.

    A positively licensed analytical movement can carry exact sufficient state from one governed
    anchor to one coarser governed anchor, while mechanically possible but unlicensed movement
    refuses.

Every case below uses THE SAME four rows. The arrays are foldable in all of them — that is the
point. What differs is only whether the movement is licensed, and for what.
"""
from decimal import Decimal

import pytest

from columna_core.operators import get_operator
from columna_platform import continuation, movement, serving
from columna_platform.refusals import WantOfLaw
from columna_platform.state import RetainedStateStore

from conftest import REVENUE, no_result, reason


def _store(st):
    s = RetainedStateStore()
    s.insert(st)
    return s


# ── THE POSITIVE CONTROL ─────────────────────────────────────────────────────────────────────────
def test_licensed_movement_serves_through_the_real_wire(anchored, licence):
    _pub, view, st = anchored
    w = serving.decide(view, _store(st), st.identity, at_anchor="store", licence=licence)

    assert w["contract_version"] == "5"
    assert w["outcome"] == "serve"
    assert w["frame"]["anchor"] == ["store"]
    assert w["columns"][0]["status"] == "served"


def test_the_fold_is_exact(anchored, licence):
    _pub, view, st = anchored
    moved = continuation.continue_to(view, st, licence, target_anchor="store")

    assert moved.table.to_pydict() == {"store": ["east", "west"],
                                       "amount": [Decimal("30.0000"), Decimal("4.9382")]}
    assert str(moved.array.type) == "decimal128(18, 4)"       # carried exactly, never widened
    assert not any(isinstance(v, float) for v in moved.table.to_pydict()["amount"])


def test_it_is_still_the_same_governed_family(anchored, licence):
    """A movement changes the ANCHOR. It does not mint a new family."""
    _pub, view, st = anchored
    moved = continuation.continue_to(view, st, licence, target_anchor="store")

    assert moved.identity.family_id == st.identity.family_id == REVENUE
    assert moved.identity.anchor == "store"
    assert st.identity.anchor == "sale_at"                    # the source state is untouched


def test_standing_travels_forward_and_records_the_movement(anchored, licence):
    _pub, view, st = anchored
    moved = continuation.continue_to(view, st, licence, target_anchor="store")

    for axis in ("constitution", "constitution_scheme", "participation", "basis", "realization",
                 "currency"):
        assert getattr(moved.standing, axis) == getattr(st.standing, axis), axis
    assert moved.standing.movement == "sale_at(store*day) -> store(store) under SUM [positive]"


def test_the_licence_is_checked_against_declared_components_not_its_own_string(anchored):
    """The publication is the authority. A licence naming a coordinate it invented is refused."""
    pub, _view, _st = anchored
    with pytest.raises(WantOfLaw) as e:
        movement.project(pub, source_anchor="sale_at", target_anchor="region",
                         target_components=["region"], law="SUM")
    assert "not declared components" in str(e.value)


# ── NEGATIVE CONTROL 1 · mechanically combinable, not licensed ───────────────────────────────────
def test_the_same_arrays_are_mechanically_combinable(anchored):
    """Establish the premise the control depends on: nothing STOPS this fold but the law."""
    op = get_operator("sum")
    assert op.is_monoid is True and op.combine == "sum"


def test_no_licence_refuses_and_says_monoid_is_not_permission(anchored):
    _pub, view, st = anchored
    w = serving.decide(view, _store(st), st.identity, at_anchor="store", licence=None)

    assert w["outcome"] == "refuse"
    assert reason(w) == "want_of_law"
    detail = no_result(w)["detail"]
    # THE REQUIREMENT, ON THE WIRE and not merely in an internal exception: an operator reading the
    # served payload must be told that "but it would have worked" is not an argument.
    assert "Mechanical combinability is NOT analytical permission" in detail
    assert "monoid" in detail
    assert "no positive movement licence" in detail


def test_continuation_itself_refuses_without_a_licence_citing_the_monoid(anchored):
    """The refusal an operator reads must say WHY 'it would have worked' is not an argument."""
    _pub, view, st = anchored
    with pytest.raises(WantOfLaw) as e:
        continuation.continue_to(view, st, None, target_anchor="store")
    msg = str(e.value)
    assert "Mechanical combinability is NOT analytical permission" in msg
    assert "monoid" in msg


# ── NEGATIVE CONTROL 2 · a licence for a different target ────────────────────────────────────────
def test_a_licence_for_another_target_does_not_license_this_one(anchored):
    pub, view, st = anchored
    elsewhere = movement.project(pub, source_anchor="sale_at", target_anchor="day",
                                 target_components=["day"], law="SUM")

    w = serving.decide(view, _store(st), st.identity, at_anchor="store", licence=elsewhere)

    assert reason(w) == "want_of_law"
    assert "targets 'day', not 'store'" in no_result(w)["detail"]
    assert "specific, not general" in no_result(w)["detail"]


def test_a_licence_from_another_source_is_not_transitive(anchored, licence):
    _pub, view, st = anchored
    from dataclasses import replace
    other_source = replace(licence, source_anchor="store")

    with pytest.raises(WantOfLaw) as e:
        continuation.continue_to(view, st, other_source, target_anchor="store")
    assert "not implicitly transitive" in str(e.value)


# ── NEGATIVE CONTROL 3 · a licence under the wrong law ───────────────────────────────────────────
def test_a_licence_under_another_law_does_not_license_this_continuation(anchored, licence):
    _pub, view, st = anchored
    from dataclasses import replace
    wrong_law = replace(licence, law="MIN")

    w = serving.decide(view, _store(st), st.identity, at_anchor="store", licence=wrong_law)

    assert reason(w) == "want_of_law"
    detail = no_result(w)["detail"]
    assert "under 'MIN'" in detail and "established continuation is 'SUM'" in detail


def test_the_family_continuation_law_is_read_from_c8_not_from_the_operator(anchored):
    """The licence is compared against GOVERNED law, never against the operator registry."""
    _pub, view, _st = anchored
    assert continuation.established_continuation_law(view) == "SUM"


# ── standing that is not positive is not a licence ───────────────────────────────────────────────
def test_a_non_positive_standing_is_not_a_licence(anchored, licence):
    _pub, view, st = anchored
    from dataclasses import replace
    proposed = replace(licence, standing="proposed")

    with pytest.raises(WantOfLaw) as e:
        continuation.continue_to(view, st, proposed, target_anchor="store")
    assert "not 'positive'" in str(e.value)


# ── the four refusals are distinguishable ────────────────────────────────────────────────────────
def test_all_four_unlicensed_cases_refuse_differently(anchored, licence):
    from dataclasses import replace
    _pub, view, st = anchored
    cases = [None,
             replace(licence, target_anchor="day", target_components=("day",)),
             replace(licence, law="MIN"),
             replace(licence, standing="proposed")]
    details = set()
    for lic in cases:
        with pytest.raises(WantOfLaw) as e:
            continuation.continue_to(view, st, lic, target_anchor="store")
        details.add(str(e.value))
    assert len(details) == 4

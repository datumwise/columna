"""OF-39 — THE CONSTITUTION FINGERPRINT IS PART OF COMPATIBILITY (ruled Huayin, 2026-09-14).

THE RULING, AND THE TWO FIELDS' DISTINCT ROLES.

    · `constitution_scheme` establishes HOW constitution fingerprints are formed, and therefore
      whether two of them are comparable at all;
    · `constitution` identifies WHICH actual governed constitution this state was established under.

Two states with the same scheme but different fingerprints are NOT compatible for combination, even
when every other compatibility axis agrees. `comparable_to` carried only the scheme, so they were.

WHY THE DEFECT SURVIVED, AND WHY IT IS REPAIRED NOW. `RetainedStateStore.combine` is the tuple's
only consumer and NOTHING ON THE SERVING PATH CALLS IT — so the wrong rule was inert, which is
exactly why no test ever failed on it. It is repaired while it still changes no behaviour, because
the first unit that makes reuse reachable would otherwise be the unit that discovers it.

THE DISTINCTION THIS UNIT MUST NOT BLUR:

    ANALYTICAL IDENTITY      what the state is OF                         `F @ A`
    COMPATIBILITY STANDING   whether two states of that thing may         `Standing.comparable_to`
                             lawfully enter one continuation

Two states under different constitutions are still states of the SAME analytical thing. Widening
identity to carry the constitution would make a re-constituted state a state of something else,
which it is not — and it is the specific error the SSE contract forbids. These controls therefore
assert BOTH halves: the constitution changes compatibility, and it does not change identity.

SCOPE. `combine` is exercised DIRECTLY over retained state. This unit does not make it reachable
from the serving path, and does not touch family identity rules.
"""
from __future__ import annotations

import dataclasses

import pytest
from columna_platform import serving
from columna_platform.refusals import ProofRefusal, WantOfCompatibility, WantOfState
from columna_platform.state import AnalyticalIdentity, RetainedStateStore, Standing

from test_proof_a_lawful import _materialize                          # noqa: E402

OTHER_FINGERPRINT = "fcf-1:0000000000000000"


def _with(state, **fields):
    """The same retained state with its standing altered on exactly the named axes."""
    standing = dataclasses.replace(state.standing, **fields)
    return dataclasses.replace(state, standing=standing)


@pytest.fixture
def pair(revenue):
    """Two independently materialized states of ONE analytical identity, fully compatible."""
    family, view, real = revenue
    store = RetainedStateStore()
    return store, _materialize(family, view, real, store), _materialize(family, view, real, store)


# ══ the positive · compatibility can pass ═════════════════════════════════════════════════════

def test_same_identity_same_constitution_and_axes_may_combine(pair):
    """Same identity, same fingerprint, same scheme, same participation / basis / realization, and
    a warranted currency token on both. Nothing stands in the way and the fold happens.

    Asserted FIRST, because every refusal below is only meaningful if this one passes: a rule that
    refuses everything is not a compatibility rule."""
    store, a, b = pair
    assert a.identity == b.identity
    assert a.standing.comparable_to == b.standing.comparable_to

    combined = store.combine(a, b)
    assert combined.identity == a.identity
    assert len(combined.array) == len(a.array) + len(b.array)


def test_the_constitution_fingerprint_is_actually_in_the_comparability_tuple():
    """Structural, so the ruling cannot be undone by an edit that leaves the tests passing for some
    other reason. Both constitution fields are present, and they are distinct entries."""
    st = Standing(constitution="fcf-1:aaaa", constitution_scheme="fcf-1",
                  participation="p", basis="b", realization="r", currency="tok")
    assert "fcf-1:aaaa" in st.comparable_to
    assert "fcf-1" in st.comparable_to
    assert len(set(st.comparable_to)) == len(st.comparable_to)


# ══ the negatives · one axis at a time ════════════════════════════════════════════════════════

def test_same_scheme_but_a_different_constitution_fingerprint_refuses(pair):
    """THE ROW THIS UNIT EXISTS FOR (OF-39). Same scheme — so the two fingerprints are comparable at
    all — and every other axis identical. Before the ruling this combined silently."""
    store, a, b = pair
    b = _with(b, constitution=OTHER_FINGERPRINT)
    assert b.standing.constitution_scheme == a.standing.constitution_scheme

    with pytest.raises(WantOfCompatibility):
        store.combine(a, b)


@pytest.mark.parametrize("axis,value", [
    ("participation", "listwise"),
    ("basis", "some-other-basis"),
    ("realization", "warehouse:sales.other_table.amount/coincident/exact"),
])
def test_same_constitution_but_a_differing_axis_refuses(pair, axis, value):
    """The other three compatibility axes, each alone, with the constitution held EQUAL — so the
    repair cannot be passing these by accident through the field it just added."""
    store, a, b = pair
    b = _with(b, **{axis: value})
    assert b.standing.constitution == a.standing.constitution

    with pytest.raises(WantOfCompatibility):
        store.combine(a, b)


def test_an_incomparable_scheme_still_refuses(pair):
    """The scheme's own job, unchanged by the ruling: fingerprints formed by different schemes are
    not comparable at all, and incomparable must never read as equal."""
    store, a, b = pair
    b = _with(b, constitution_scheme="fcf-2")

    with pytest.raises(WantOfCompatibility):
        store.combine(a, b)


def test_no_currency_still_prevents_combination_under_the_existing_rule(pair):
    """The existing rule is untouched, and it is a DIFFERENT refusal: a missing currency token is a
    want of STATE (something is missing), not a want of compatibility (nothing is missing and the
    two simply may not be added). This unit must not have collapsed the two."""
    store, a, b = pair
    a, b = _with(a, currency=None), _with(b, currency=None)

    with pytest.raises(WantOfState):
        store.combine(a, b)


def test_a_compatible_pair_with_one_missing_token_is_want_of_state_not_compatibility(pair):
    """Order of the two gates, pinned. Fully compatible standing, one absent token: the answer must
    name the thing that is actually missing."""
    store, a, b = pair
    b = _with(b, currency=None)
    assert a.standing.comparable_to == b.standing.comparable_to

    with pytest.raises(WantOfState):
        store.combine(a, b)


# ══ how incompatibility travels ═══════════════════════════════════════════════════════════════

def test_incompatibility_carries_no_rematerialization_remedy(pair):
    """`WantOfCompatibility.remedy is None`, and that is the whole point of the class. Both states
    are VALID and individually reusable; nothing is missing, so re-materializing either one changes
    nothing. A remedy here would send an operator to redo work that was never wrong."""
    store, a, b = pair
    b = _with(b, constitution=OTHER_FINGERPRINT)

    with pytest.raises(WantOfCompatibility) as e:
        store.combine(a, b)
    assert e.value.remedy is None
    assert isinstance(e.value, ProofRefusal)          # governed, unlike a capability limit


def test_incompatibility_travels_to_the_wire_as_want_of_compatibility(pair):
    """It must not borrow `want_of_state` — which would claim something is missing and offer
    re-materialization as the fix — nor `want_of_law`."""
    store, a, b = pair
    b = _with(b, constitution=OTHER_FINGERPRINT)

    with pytest.raises(WantOfCompatibility) as e:
        store.combine(a, b)
    reason, alternatives = serving._classify(e.value)
    assert reason == "want_of_compatibility"
    assert reason not in ("want_of_state", "want_of_law")
    assert not alternatives


# ══ the distinction · compatibility is not identity ═══════════════════════════════════════════

def test_changing_the_constitution_changes_COMBINABILITY_and_not_IDENTITY(pair):
    """THE CONTROL THE RULING ASKED FOR, AND THE ONE MOST WORTH HAVING.

    One edit, two questions, two different answers. After changing only the constitution
    fingerprint the two states are STILL states of the same analytical thing — same `family_id`,
    same anchor, equal `AnalyticalIdentity` — and they may no longer be combined.

    If a later change ever makes these two assertions agree, something has quietly folded standing
    into identity, and a re-constituted state will have become a state of something else."""
    store, a, b = pair
    b = _with(b, constitution=OTHER_FINGERPRINT)

    assert a.identity == b.identity                                  # identity: unchanged
    assert a.identity.family_id == b.identity.family_id
    assert a.identity.anchor == b.identity.anchor
    assert a.standing.comparable_to != b.standing.comparable_to      # compatibility: changed

    with pytest.raises(WantOfCompatibility):
        store.combine(a, b)


def test_analytical_identity_still_carries_exactly_two_fields():
    """Identity did not widen. `F @ A`, and nothing about how the state is stored or under which
    constitution it stands."""
    assert [f.name for f in dataclasses.fields(AnalyticalIdentity)] == ["family_id", "anchor"]


def test_retrieval_still_finds_a_state_whose_constitution_differs(pair):
    """Retrieval is keyed by IDENTITY, and must stay that way. A state under another constitution
    is still a state of the asked-for thing: it is found, and then refused at combination. Hiding
    it at retrieval would make the constitution part of identity through the back door, and would
    turn a compatibility refusal into a silent miss."""
    store, a, b = pair
    store._states.clear()
    store.insert(a)
    store.insert(_with(b, constitution=OTHER_FINGERPRINT))

    held = store.retrieve(AnalyticalIdentity(a.identity.family_id, a.identity.anchor))
    assert len(held) == 2
    assert {s.standing.constitution for s in held} == {a.standing.constitution, OTHER_FINGERPRINT}


# ══ scope · this unit changes nothing on the serving path ═════════════════════════════════════

def test_combine_is_still_unreachable_from_the_serving_path():
    """The repair is deliberately inert in production. If `combine` ever acquires a caller in a
    `src/` module, that is the unit which must carry the reuse proof — and this control says so by
    failing."""
    import pathlib
    src = pathlib.Path(serving.__file__).resolve().parents[3]
    callers = [p for p in src.rglob("src/**/*.py")
               if ".combine(" in p.read_text(encoding="utf-8")
               and p.name not in ("state.py", "planner.py")]
    assert callers == [], f"combine acquired a serving-path caller: {callers}"

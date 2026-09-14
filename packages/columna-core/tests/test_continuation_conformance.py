"""The realization's CONTINUATION CLAIM against governed C8 — all seven cells, in K0v2.

THE DEFECT THIS PINS (OF-47). `continuation_operator` was loaded, defaulted and carried exactly like
`formation_operator`, and READ IN ONE PLACE in the repository — inside `if cont.standing ==
ESTABLISHED`, on the primitive branch only. Measured on the shipped compiler before the repair:

    min(revenue@sale_at) claiming "sum" against its entailed C8 of MIN  -> BYTE-IDENTICAL image
    count(revenue@sale_at) claiming "wildly_wrong"                      -> BYTE-IDENTICAL image
    revenue (C8 ESTABLISHED = SUM) with the claim REMOVED               -> BYTE-IDENTICAL image
    revenue with the claim null                                         -> BYTE-IDENTICAL image

EVERY STANDING HERE IS RESOLVED BY THE REAL RESOLVER, never synthesized. `EXPLICIT_NONE` is reached
by re-forming a family under MEAN (whose `entails_continuation` is `none`); `UNESTABLISHED` by
removing a primitive's declared continuation. A hand-built `Standing` would test the matrix against a
fixture of the matrix, which is no test at all.
"""
from __future__ import annotations

import copy
import hashlib
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fixtures_v2 import lighthouse as lh                                       # noqa: E402

from columna_core.compiler.compile_v2 import compile_v2                        # noqa: E402
from columna_core.compiler.realization import parse_mapping                    # noqa: E402
from columna_core.compiler.refusals import (                                   # noqa: E402
    LogicalMeaningMissing, MappingContradictsLaw, MappingIncomplete,
)
from columna_core.governed import resolve as R                                 # noqa: E402
from columna_core.governed.publication import parse_publication                # noqa: E402

REVENUE, COUNT, MIN, MAX = "lh-revenue", "lh-revcount", "lh-revmin", "lh-revmax"


def _fam(d, ref):
    for dec in d["logical"]["declarations"]:
        if dec["kind"] == "family" and dec["body"].get("canonical_reference") == ref:
            return dec["body"]
    raise KeyError(ref)


def _build(*, pub_mutate=None, map_mutate=None):
    p = copy.deepcopy(lh.publication())
    m = copy.deepcopy(lh.mapping())
    if pub_mutate:
        pub_mutate(p)
    if map_mutate:
        map_mutate(m)
    return compile_v2(parse_publication(p), parse_mapping(m))


def _claim(fid, value):
    """Set (or, with `_ABSENT`, remove) one family's continuation claim."""
    def mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == fid:
                if value is _ABSENT:
                    r.pop("continuation_operator", None)
                else:
                    r["continuation_operator"] = value
    return mutate


_ABSENT = object()


def _mean_formed(fid_ref):
    """Re-form a family under MEAN, whose `entails_continuation` is `none` -> C8 EXPLICIT_NONE."""
    def mutate(d):
        f = _fam(d, fid_ref)
        f["formation"]["law"] = lh._cite("MEAN")
        f.pop("continuation", None)
    return mutate


def _no_continuation(fid_ref):
    """A primitive with no declared continuation -> C8 UNESTABLISHED (no default is invented)."""
    def mutate(d):
        _fam(d, fid_ref).pop("continuation", None)
    return mutate


# ══ the standings these cells rest on are REAL, and asserted to be ══════════════════════════════

def test_the_fixture_standings_are_what_the_matrix_assumes():
    """If this drifts, every cell below is testing something else. Asserted, not assumed."""
    views = R.resolve_all(parse_publication(copy.deepcopy(lh.publication())))
    got = {fid: (views[fid][R.C8_CONTINUATION].standing,
                 getattr(views[fid][R.C8_CONTINUATION].value, "name", None))
           for fid in (REVENUE, COUNT, MIN, MAX)}
    assert got == {REVENUE: ("established", "SUM"), COUNT: ("established", "SUM"),
                   MIN: ("established", "MIN"), MAX: ("established", "MAX")}


def test_count_is_the_case_that_proves_the_two_claims_are_different_facts():
    """COUNT's formation COUNTS and its continuation SUMS (foundation §5.2).

    `min` and `max` have formation and continuation operators that COINCIDE, so a repair validated
    only on those two would look finished and prove nothing. This is the one family where claiming
    the formation operator as the continuation operator is a contradiction."""
    # the committed fixture carries BOTH, and they differ
    fixture = {r["family_id"]: r for r in lh.mapping()["realizations"] if "family_id" in r}
    assert fixture[COUNT]["formation_operator"] == "count"
    assert fixture[COUNT]["continuation_operator"] == "sum"
    # and claiming the FORMATION operator as the continuation claim contradicts the governed law
    with pytest.raises(MappingContradictsLaw) as e:
        _build(map_mutate=_claim(COUNT, "count"))
    assert "SUM" in str(e.value) and "'count'" in str(e.value)


# ══ C8 ESTABLISHED ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("fid,expected", [(REVENUE, "sum"), (COUNT, "sum"),
                                          (MIN, "min"), (MAX, "max")])
def test_established_c8_with_a_matching_claim_is_accepted(fid, expected):
    """Primitive AND constructed, including ENTAILED C8 (`min`, `max`, `count`).

    Asserts the fixture's claim is the one the governed law names — so "accepted" means accepted for
    the right reason and not because the check is inert."""
    claims = {r["family_id"]: r.get("continuation_operator")
              for r in lh.mapping()["realizations"] if "family_id" in r}
    assert claims[fid] == expected
    assert _build() is not None


@pytest.mark.parametrize("fid", [REVENUE, COUNT, MIN, MAX])
@pytest.mark.parametrize("missing", [_ABSENT, None], ids=["absent", "null"])
def test_established_c8_with_no_claim_is_mapping_incomplete(fid, missing):
    """THE NULL EXEMPTION, REMOVED. Both spellings of "no claim" refuse, on every family.

    Before the repair all eight of these compiled, and four of them compiled to an image
    BYTE-IDENTICAL to the conformant one."""
    with pytest.raises(MappingIncomplete, match="no continuation claim"):
        _build(map_mutate=_claim(fid, missing))


@pytest.mark.parametrize("fid,wrong", [(REVENUE, "min"), (COUNT, "count"),
                                       (MIN, "sum"), (MAX, "min")])
def test_established_c8_with_a_wrong_claim_is_a_contradiction(fid, wrong):
    """NOT `MappingIncomplete` (ruled 2026-09-14): the claim is PRESENT AND WRONG, not absent.

    `min` claiming "sum" is the ENTAILED-C8 case — the rule applies to entailed standing exactly as
    it does to declared, which is the clause that would otherwise live only in prose."""
    with pytest.raises(MappingContradictsLaw):
        _build(map_mutate=_claim(fid, wrong))


def test_a_claim_of_an_operator_this_profile_does_not_know_is_still_a_contradiction():
    with pytest.raises(MappingContradictsLaw):
        _build(map_mutate=_claim(REVENUE, "wildly_wrong"))


# ══ C8 EXPLICIT_NONE — a POSITIVE governed negative, and therefore contradictable ═══════════════

def test_explicit_none_with_no_claim_is_accepted():
    """Reached through the real resolver: MEAN's `entails_continuation` is `none`."""
    views = R.resolve_all(parse_publication(
        _mutated(copy.deepcopy(lh.publication()), _mean_formed("max(revenue@sale_at)"))))
    c8 = views[MAX][R.C8_CONTINUATION]
    assert (c8.standing, c8.provenance) == ("explicit-none", "entailed")
    # and the matrix accepts an absent claim against it
    from columna_core.compiler.compile_v2 import _check_continuation_claim
    _check_continuation_claim(c8, None, "max(revenue@sale_at)")


def test_explicit_none_with_an_asserted_operator_is_a_contradiction():
    """The publication POSITIVELY ESTABLISHES that there is no continuation. A realization naming
    one is asserting against a fact that exists — which is contradiction, not manufacture."""
    views = R.resolve_all(parse_publication(
        _mutated(copy.deepcopy(lh.publication()), _mean_formed("max(revenue@sale_at)"))))
    c8 = views[MAX][R.C8_CONTINUATION]
    from columna_core.compiler.compile_v2 import _check_continuation_claim
    with pytest.raises(MappingContradictsLaw, match="POSITIVELY ESTABLISHES"):
        _check_continuation_claim(c8, "max", "max(revenue@sale_at)")


# ══ C8 UNESTABLISHED — nothing to contradict; the defect is MANUFACTURE ═════════════════════════

def test_unestablished_with_no_claim_is_accepted_as_no_assertion():
    views = R.resolve_all(parse_publication(
        _mutated(copy.deepcopy(lh.publication()), _no_continuation("revenue"))))
    c8 = views[REVENUE][R.C8_CONTINUATION]
    assert c8.standing == "unestablished"
    from columna_core.compiler.compile_v2 import _check_continuation_claim
    _check_continuation_claim(c8, None, "revenue")          # a null asserts nothing


def test_unestablished_with_an_asserted_operator_cannot_manufacture_meaning():
    """NOT a contradiction — there is no governed fact to contradict. The realization is trying to
    AUTHOR analytical meaning, which is a different wrong with a different owner."""
    views = R.resolve_all(parse_publication(
        _mutated(copy.deepcopy(lh.publication()), _no_continuation("revenue"))))
    c8 = views[REVENUE][R.C8_CONTINUATION]
    from columna_core.compiler.compile_v2 import _check_continuation_claim
    with pytest.raises(LogicalMeaningMissing, match="manufacture"):
        _check_continuation_claim(c8, "sum", "revenue")


def test_the_two_non_established_standings_raise_DIFFERENT_categories():
    """THE LOAD-BEARING DISTINCTION, as a single assertion.

    Collapsing these would file a manufactured law as a disagreement, and send whoever read it
    looking for a governed fact that was never there."""
    from columna_core.compiler.compile_v2 import _check_continuation_claim
    pub = copy.deepcopy(lh.publication())
    none_c8 = R.resolve_all(parse_publication(
        _mutated(copy.deepcopy(pub), _mean_formed("max(revenue@sale_at)"))))[MAX][R.C8_CONTINUATION]
    unest_c8 = R.resolve_all(parse_publication(
        _mutated(copy.deepcopy(pub), _no_continuation("revenue"))))[REVENUE][R.C8_CONTINUATION]

    raised = {}
    for label, c8 in (("explicit-none", none_c8), ("unestablished", unest_c8)):
        try:
            _check_continuation_claim(c8, "sum", label)
        except Exception as e:                              # noqa: BLE001 - recording the category
            raised[label] = type(e).__name__
    assert raised == {"explicit-none": "MappingContradictsLaw",
                      "unestablished": "LogicalMeaningMissing"}


# ══ the mutation control — byte-identity is how the defect was found ════════════════════════════

def test_two_mappings_differing_only_in_the_continuation_claim_do_not_compile_alike():
    """THE INVARIANT, STATED AS ONE. Every mutation below produced a BYTE-IDENTICAL image before the
    repair (sha 1ebc472e, 310 bytes, four times over). Byte-identity is the only evidence that will
    notice this defect returning, so it is asserted rather than left to the categories above."""
    baseline = hashlib.sha256(str(_build()).encode()).hexdigest()
    for fid in (REVENUE, COUNT, MIN, MAX):
        for value in (_ABSENT, None, "wildly_wrong"):
            with pytest.raises((MappingIncomplete, MappingContradictsLaw)):
                out = _build(map_mutate=_claim(fid, value))
                assert hashlib.sha256(str(out).encode()).hexdigest() != baseline, (
                    f"{fid} with claim {value!r} compiled to a BYTE-IDENTICAL image — the "
                    f"continuation claim is being absorbed again")


def _mutated(d, mutate):
    mutate(d)
    return d

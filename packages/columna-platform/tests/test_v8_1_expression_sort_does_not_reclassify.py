"""
test_v8_1_expression_sort_does_not_reclassify.py — V8-1's ruling-5 proof, at the consumer layer.

    *"The old v3.0/v2 basis-mediated Family declaration may remain readable as an old artifact, but
    under v8 it must not silently become an expression merely because the new reader knows that sort.
    It should fail family standing and require explicit migration/re-authoring into the v3.1
    expression declaration. Parsing compatibility is not analytical reclassification."*
        — Huayin, 2026-09-28, ruling 5

**THE RISK THIS UNIT IS AGAINST IS SPECIFIC AND IS CREATED BY V8-1 ITSELF.** Before V8-1 there was no
expression sort, so `mean(revenue@sale_at)` declared `"kind": "family"` could only be what it said it
was and V8-0's C4 clause 2 refused it. After V8-1 the sort exists — and the tempting move, in a reader
or in a serving path, is to notice that the object HAS a sufficient basis, conclude that it is
"really" an expression, and route it to the new resolver. That would be the reader re-authoring a
governed declaration on the steward's behalf, which §3.7 forbids by name: naming, caching, repetition
or durable governance does not change what an object is.

So this file asserts the two halves separately: the legacy declaration STILL READS (it is a lawful
artifact, and nothing here deletes it), and it is STILL REFUSED as a family, and it is NOT an
expression by any door.
"""
from __future__ import annotations

import copy
import json
import os

import pytest

from columna_core.governed.expression import resolve_expression
from columna_core.governed.native import (
    NativePublicationRefusal,
    parse_native_publication,
)
from columna_core.governed.resolve import (
    C7_SUFFICIENT_STATE,
    C8_CONTINUATION,
    ENTAILED_FROM_FORMATION,
    ESTABLISHED,
    EXPLICIT_NONE,
    is_basis_mediated,
)
from columna_platform import native_law as nl
from columna_platform.refusals import WantOfLaw

_V31 = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "columna-core", "tests", "fixtures_v3", "native-v3_1-publication.json")

REV = "fam_Rv7KpQ2mXsDnYc4TjLbWhE"
LEGACY_ID = "fam_LegacyMeanQ7xTvBnKsWdE2"
LEGACY_REF = "mean(revenue@sale_at)"


def _with_legacy_mean_family():
    """The artifact, plus the OLD-STYLE declaration: a `kind: family` whose formation cites MEAN.

    Deliberately added to the v3.1 artifact rather than kept in a v3.0 one, because the question is
    what a READER THAT KNOWS THE EXPRESSION SORT does with it. In a v3.0 artifact the sort is not
    admitted and the answer is uninteresting."""
    with open(_V31, encoding="utf-8") as fh:
        raw = json.load(fh)
    raw = copy.deepcopy(raw)
    legacy = {
        "kind": "family", "name": "legacy_mean",
        "body": {
            "family_id": LEGACY_ID,
            "canonical_reference": LEGACY_REF,
            "universe": "commerce",
            "constitutive_anchor": "sale_at",
            "target": "the arithmetic mean of accepted order value at one store-day",
            "formation": {"kind": "construction",
                          "law": {"vocabulary": "datumwise.foundation", "version": "1",
                                  "law": "MEAN"},
                          "operands": [REV]},
            "participation": "every customer order the merchant accepted"},
        "family_constitution_authority": {
            "established_by": "commerce steward", "at": "2026-09-28T00:00:00Z",
            "constitution_fingerprint": "PENDING", "fingerprint_scheme": "fcf-2"},
        "universe_authority_binding": {
            "bound_by": "commerce steward", "at": "2026-09-28T00:00:00Z",
            "universe_reference": "commerce",
            "universe_authority": next(
                d for d in raw["declarations"]
                if d["kind"] == "universe")["existence_law_ratification"]["fingerprint"],
            "universe_authority_scheme": "elf-2"},
    }
    raw["declarations"].append(legacy)
    # stamp its fcf-2 from the contract's own derivation rather than by hand
    probe = copy.deepcopy(raw)
    next(d for d in probe["declarations"]
         if d.get("name") == "legacy_mean")["family_constitution_authority"][
        "constitution_fingerprint"] = "fcf-2:" + "0" * 64
    try:
        parse_native_publication(probe)
    except NativePublicationRefusal as exc:
        legacy["family_constitution_authority"]["constitution_fingerprint"] = \
            str(exc).split("derives '")[1].split("'")[0]
    return raw


@pytest.fixture
def pub():
    return parse_native_publication(_with_legacy_mean_family())


# ── half 1 · the legacy declaration STILL READS ───────────────────────────────────────────────────
def test_the_legacy_basis_mediated_family_still_parses_in_a_v3_1_artifact(pub):
    """Nothing about this unit deletes an old artifact, and a reader that refused one would be making
    the sort change a format break. It is not: v3.1 is additive."""
    fam = pub.family(LEGACY_REF)
    assert fam.family_id == LEGACY_ID
    assert fam.body["formation"]["law"]["law"] == "MEAN"


# ── half 2 · and is STILL REFUSED AS A FAMILY, for V8-0's reason, unchanged ───────────────────────
def test_it_still_fails_family_standing_and_the_expression_sort_did_not_rescue_it(pub):
    view = nl.law_of(pub, pub.family(LEGACY_REF))
    c7, c8 = view[C7_SUFFICIENT_STATE], view[C8_CONTINUATION]
    assert c7.standing == ESTABLISHED
    assert c7.provenance == ENTAILED_FROM_FORMATION
    assert is_basis_mediated(c7)
    assert c8.standing == EXPLICIT_NONE
    with pytest.raises(WantOfLaw) as exc:
        nl.assert_answerable(view, moving=False)
    assert "not a route to family standing" in str(exc.value)


def test_the_continuation_bearing_families_beside_it_are_untouched(pub):
    for reference in ("revenue", "order_count"):
        view = nl.law_of(pub, pub.family(reference))
        assert not is_basis_mediated(view[C7_SUFFICIENT_STATE])
        nl.assert_answerable(view, moving=False)          # no refusal


# ── half 3 · and it is NOT an expression, by any door ─────────────────────────────────────────────
def test_the_reader_does_not_reclassify_it(pub):
    assert pub.sort_of(LEGACY_REF) == "family"
    assert pub.resolve_expression_reference(LEGACY_REF) is None
    assert LEGACY_ID not in {x.expression_id for x in pub.expressions}
    assert [x.name for x in pub.expressions] == ["average_order_value"]


def test_asking_for_it_as_an_expression_names_the_remedy_rather_than_supplying_it(pub):
    with pytest.raises(NativePublicationRefusal) as exc:
        pub.expression(LEGACY_REF)
    msg = str(exc.value)
    assert "parsing compatibility is not analytical reclassification" in msg
    assert "explicit re-authoring into an expression declaration" in msg
    assert "authority to make it" in msg


def test_the_two_objects_coexist_and_only_the_re_authored_one_resolves(pub):
    """The migration's end state, in one artifact: the old declaration is readable and unanswerable,
    the new one is a valid, evaluable governed expression. That is what an explicit re-authoring
    looks like, and the difference between them is the steward's act — not the reader's inference."""
    families = {f.family_id: f for f in pub.families}
    view = resolve_expression(pub.expression("average_order_value"),
                              pub.universe("commerce"), families)
    assert view.valid and view.establishable

    with pytest.raises(WantOfLaw):
        nl.assert_answerable(nl.law_of(pub, pub.family(LEGACY_REF)), moving=False)


def test_no_serving_or_peer_request_target_was_added_by_this_unit():
    """V8-1's stop condition, pinned. `sort_of` gives a future peer target a lawful object to point at;
    nothing routes on it, and `request.resolve` is unchanged (ruling 8)."""
    import inspect

    from columna_platform import request

    src = inspect.getsource(request)
    assert "sort_of" not in src
    assert "resolve_expression_reference" not in src
    assert "does not evaluate expressions" in src      # the gap is still NAMED, not filled

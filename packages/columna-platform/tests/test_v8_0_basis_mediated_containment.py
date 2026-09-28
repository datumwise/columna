"""V8-0 · basis-mediated family standing is contained.

ToD v8.0 (published 2026-09-28) §9.2 withdrew a route that Version 7.1 allowed:

    a durable derived measure family could be justified EITHER by self-sufficient continuation
    OR by a sufficient-state basis.

v8 keeps only the first. A basis over OTHER analytical objects reconstructs a value; it does not make
that value continuation-bearing, so it cannot earn FAMILY standing (§3.7 — "Naming, caching,
repetition, business importance, or durable governance of an expression does not make its result
continuation-bearing").

WHAT THIS UNIT DID, AND DELIBERATELY DID NOT DO
----------------------------------------------
C7 had two routes into ESTABLISHED — the family's own CONTINUATION law, and, where there is none, the
FORMATION law — and both emitted the provenance token `ENTAILED`. The only machine-readable trace of
which route fired was an interpolated phrase inside `.note`. So:

  * `resolve` now emits `ENTAILED_FROM_FORMATION` on the formation route, and exposes ONE predicate,
    `is_basis_mediated`, as the single place the distinction is asked about;
  * family answerability (native C4, and the v2 serving gates) refuses a basis-mediated standing.

**The basis is NOT deleted, the standing is NOT invalidated, and `EXPLICIT_NONE` continuation remains a
legitimate standing.** The expression layer will need all three. Nor does C4 conclude that the object
IS a governed expression: `ADMITTED_KINDS` has no such sort, and inventing one is the V8-1 question.
"""
from __future__ import annotations

import copy
import json

import pytest

from columna_core.governed.foundation import LAWS, NO_CONTINUATION
from columna_core.governed.publication import parse_publication
from columna_core.governed.resolve import (
    C7_SUFFICIENT_STATE,
    C8_CONTINUATION,
    ENTAILED,
    ENTAILED_FROM_FORMATION,
    ESTABLISHED,
    EXPLICIT_NONE,
    is_basis_mediated,
    resolve_all,
)
from columna_core.governed.foundation import StateBasis
from columna_platform import native_law as nl
from columna_platform import serving
from columna_platform.refusals import WantOfLaw
from columna_platform.state import AnalyticalIdentity, RetainedStateStore

from conftest import MEAN_ID, PUBLICATION, REVENUE


@pytest.fixture
def revenue_view(revenue):
    """conftest's `revenue` is `(family, law_view, realization)`; this unit only wants the view."""
    return revenue[1]


def _view_for_family_citing(law_name: str, *, family_id: str = "fam-under-test"):
    """Resolve a CONSTRUCTED family whose formation cites `law_name`, over the revenue family."""
    doc = copy.deepcopy(json.loads(PUBLICATION.read_text(encoding="utf-8")))
    doc["logical"]["declarations"].append({"kind": "family", "name": "under_test", "body": {
        "family_id": family_id,
        "canonical_reference": f"{law_name.lower()}(revenue@sale_at)",
        "universe": "sales",
        "constitutive_anchor": "sale_at",
        "target": f"a {law_name} over participating sale points",
        "formation": {"kind": "construction",
                      "law": {"law": law_name, "version": "1",
                              "vocabulary": "datumwise.foundation"},
                      "operands": [REVENUE]},
        "participation": "every sale point carrying a recorded amount"}})
    return resolve_all(parse_publication(doc))[family_id]


# ══ 1 · a continuation-bearing family remains answerable ═════════════════════════════════════════

def test_an_additive_family_is_still_answerable_at_its_constitutive_anchor(revenue_view):
    """The ordinary case, and the one that must not move. Revenue is SUM: its C7 comes from its own
    continuation law, so `is_basis_mediated` is False and clause 2 never fires."""
    c7 = revenue_view[C7_SUFFICIENT_STATE]
    assert c7.standing == ESTABLISHED
    assert not is_basis_mediated(c7)
    nl.assert_answerable(revenue_view, moving=False)          # no refusal


# ══ 2 · MIN/MAX and every other continuation-bearing law are unchanged ═══════════════════════════

def _shipped_views():
    pub = parse_publication(json.loads(PUBLICATION.read_text(encoding="utf-8")))
    return pub, resolve_all(pub)


SHIPPED = [(f.canonical_reference, f.family_id) for f in _shipped_views()[0].families]


@pytest.mark.parametrize("reference,family_id", SHIPPED, ids=[r for r, _ in SHIPPED])
def test_every_family_in_the_shipped_publication_stays_on_the_continuation_route(
        reference, family_id):
    """Asserted over the REAL lighthouse publication rather than a synthetic family, because the
    question this unit must answer is whether containment moves anything that ships. It does not:
    `revenue` (SUM, primitive) and the `count` / `min` / `max` CONSTRUCTIONS all reach C7 through
    their own continuation law, so `is_basis_mediated` is False for every one of them.

    Note that three of the four are `kind=construction`. **Being constructed is not what v8 objects
    to** — citing a law that yields no continuation is. A construction over a law that continues is
    value-closed and stays a family, which is exactly the line §3.7 draws."""
    _pub, views = _shipped_views()
    view = views[family_id]
    c7 = view[C7_SUFFICIENT_STATE]
    assert c7.standing == ESTABLISHED
    assert c7.provenance == ENTAILED, f"{reference} should reach C7 by its own continuation"
    assert not is_basis_mediated(c7)
    nl.assert_answerable(view, moving=False)             # no refusal


def test_the_law_table_has_exactly_one_law_that_entails_no_continuation():
    """Guards the SCOPE of the containment against the law table drifting. MEAN is the only law today
    whose families can be basis-mediated; if a second appears, this fails and the new law's
    classification gets looked at deliberately rather than inherited."""
    assert sorted(n for n, l in LAWS.items()
                  if l.entails_continuation == NO_CONTINUATION) == ["MEAN"]


def test_no_law_today_carries_both_a_continuation_and_a_composite_state_basis():
    """WHY THE CRITERION IS PROVENANCE AND NOT `isinstance(value, StateBasis)`. Today the two are
    interchangeable, because the only law with a `state_basis` is the only law with no continuation.
    They will NOT stay interchangeable: ToD v8 §5.4's moment families are continuation-bearing AND
    carry structured composite state, so a type-based test would refuse them. This test records the
    coincidence so that the day it breaks, nobody concludes the criterion should have been the type."""
    both = [n for n, l in LAWS.items()
            if l.state_basis is not None and l.entails_continuation != NO_CONTINUATION]
    assert both == []


# ══ 3 · a MEAN-like object no longer receives family answerability ═══════════════════════════════

def test_a_basis_mediated_family_is_refused_at_its_constitutive_anchor(mean_view):
    """The defect this unit contains. Note `moving=False`: the refusal must hold AT the constitutive
    anchor, which is where such objects are normally asked for. A rule placed after the `moving`
    check would have left the whole defect reachable."""
    with pytest.raises(WantOfLaw) as e:
        nl.assert_answerable(mean_view, moving=False)
    assert "own continuation" in str(e.value)


def test_it_is_refused_when_moving_too(mean_view):
    with pytest.raises(WantOfLaw):
        nl.assert_answerable(mean_view, moving=True)


def test_the_refused_object_still_has_explicit_none_continuation_and_that_is_not_the_defect(mean_view):
    """`EXPLICIT_NONE` is a legitimate standing and stays one. MEAN's displayed value genuinely does
    not compose — a mean of means is not a mean — and saying so is correct. The defect was never that
    C8 is explicit-none; it was that C7 could compensate for it and buy family standing anyway."""
    assert mean_view[C8_CONTINUATION].standing == EXPLICIT_NONE


# ══ 4 · the sufficient basis survives the family refusal, intact and readable ════════════════════

def test_the_basis_is_still_established_and_machine_readable_after_the_refusal(mean_view):
    """The expression layer needs this basis. Containment withholds a STANDING, it does not delete a
    governed fact — so the SUM/COUNT components must still be readable as structured data."""
    c7 = mean_view[C7_SUFFICIENT_STATE]
    assert c7.standing == ESTABLISHED
    assert isinstance(c7.value, StateBasis)
    assert c7.value.components == ("SUM", "COUNT")
    assert c7.value.requires_common_participation is True


def test_the_composite_basis_reader_is_not_gated_by_the_containment(mean_view):
    """`composite.declared_basis` legitimately WANTS the basis-mediated standing — it is the
    expression-side reader. It must not come through the family gate."""
    from columna_platform import composite
    assert composite.declared_basis(mean_view).components == ("SUM", "COUNT")


# ══ 5 · the decision does not depend on parsing prose ════════════════════════════════════════════

def test_answerability_reads_a_provenance_token_and_not_the_note(mean_view):
    """The pre-v8 state of this repo carried the family/expression distinction ONLY as an interpolated
    phrase inside `.note`. Blanking the note must not change the verdict; blanking the provenance
    must. That is the whole content of "machine-readable" here."""
    from dataclasses import replace
    c7 = mean_view[C7_SUFFICIENT_STATE]

    noteless = replace(mean_view, entries={**mean_view.entries,
                                           C7_SUFFICIENT_STATE: replace(c7, note="")})
    with pytest.raises(WantOfLaw):
        nl.assert_answerable(noteless, moving=False)      # still refused with no prose at all

    relabelled = replace(mean_view, entries={**mean_view.entries,
                                             C7_SUFFICIENT_STATE: replace(c7, provenance=ENTAILED)})
    nl.assert_answerable(relabelled, moving=False)        # the token, and only the token, decides


def test_the_two_c7_routes_are_distinguishable_without_reading_prose(mean_view, revenue_view):
    assert revenue_view[C7_SUFFICIENT_STATE].provenance == ENTAILED
    assert mean_view[C7_SUFFICIENT_STATE].provenance == ENTAILED_FROM_FORMATION


# ══ 6 · the v2 and native paths agree ════════════════════════════════════════════════════════════

def test_the_v2_serving_path_refuses_the_same_object_for_the_same_reason(mean_view):
    """`native_law.assert_answerable` and the v2 serving gates are different code reached by different
    callers; V8-0 must not contain one and leave the other open. Both now ask the same predicate."""
    w = serving.decide(mean_view, RetainedStateStore(),
                       AnalyticalIdentity(MEAN_ID, "sale_at"), column="mean_revenue")
    assert w["outcome"] == "refuse"
    assert "own continuation" in json.dumps(w)


def test_the_v2_path_gate_admits_a_continuation_bearing_family(revenue_view):
    """The other half of coherence: containment must not touch the family path. Proof A exercises the
    full materialize/serve route; what is asserted here is the GATE itself, so a regression in the
    containment shows up in this module rather than only as a distant Proof A failure."""
    assert not is_basis_mediated(revenue_view[C7_SUFFICIENT_STATE])
    assert serving._require_own_established_basis(revenue_view) is revenue_view[C7_SUFFICIENT_STATE]

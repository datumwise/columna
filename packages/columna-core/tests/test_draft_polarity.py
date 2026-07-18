"""
test_draft_polarity.py — the authoring draft + the polarity wall (WP on-ramp/Explorer, CP-2).

HARNESS behavior only: the wall (BOTH layers), the state machine, review-mark bookkeeping. Never
judgment quality (that is the eval suite's jurisdiction). The wall is only as strong as its weakest
layer, so both are tested: the schema type (no constructor path yields an inferred opening) AND the
lowering (draft → .cml refuses to emit an opening even from a forcibly-constructed object).
"""
import pytest

from columna_core import (Proposal, PolarityViolation, lower_proposal, Draft,
                          PROPOSED, ACCEPTED, STRUCK, SCOPED, PROPOSED_STATE, DECLARED_STATE,
                          ATTESTED, PUBLISHED)


# ── LAYER 1 — the schema type: no constructor path yields an inferred opening ────────────────────
def test_layer1_inferred_opening_cannot_be_constructed():
    with pytest.raises(PolarityViolation):
        Proposal(kind="derived", body="DERIVED r = a / b", opens_fertility=True)   # no author mark


def test_layer1_author_declared_opening_is_legal():
    p = Proposal(kind="derived", body="DERIVED r = a / b  FERTILE { sum }",
                 opens_fertility=True, author_declared=True)                        # the human declared it
    assert p.opens_fertility and p.author_declared


def test_layer1_closures_construct_freely():
    # walls (bars, edges, plain deriveds) carry no opening — init proposes them at will.
    Proposal(kind="measure", body="MEASURE level ON u FROM t VALUE lvl FAMILY { sum BLOCKED { calendar } }")
    Proposal(kind="derived", body="DERIVED aov = revenue / orders")                # denotation-only, no door


# ── LAYER 2 — the lowering: even a FORCIBLY-constructed opening never reaches the artifact ────────
def test_layer2_lowering_refuses_a_forced_opening():
    p = Proposal(kind="derived", body="DERIVED r = a / b  FERTILE { sum }")        # legal (a wall)…
    p.opens_fertility = True                                                        # …forced past layer 1
    assert p.author_declared is False
    with pytest.raises(PolarityViolation):
        lower_proposal(p)                                                           # layer 2 still catches it


def test_layer2_declared_opening_lowers():
    p = Proposal(kind="derived", body="DERIVED r = a / b  FERTILE { sum }",
                 opens_fertility=True, author_declared=True)
    assert lower_proposal(p) == "DERIVED r = a / b  FERTILE { sum }"


# ── the state machine + publish-after-review (A3) ────────────────────────────────────────────────
def test_state_machine_advances_one_step_and_forbids_skips():
    d = Draft("m")
    assert d.state == SCOPED
    d.advance(PROPOSED_STATE)
    with pytest.raises(ValueError):
        d.advance(PUBLISHED)                       # cannot skip declared/attested


def test_cannot_publish_with_unreviewed_proposals():
    d = Draft("m").add(Proposal("measure", "MEASURE a ON u FROM t AS sum(x)"))
    for s in (PROPOSED_STATE, DECLARED_STATE, ATTESTED):
        d.advance(s)
    assert d.proposals[0].review == PROPOSED and not d.can_publish()
    with pytest.raises(ValueError):
        d.advance(PUBLISHED)                       # publish is the author's act, after review


def test_lower_to_cml_drops_struck_and_keeps_reviewed():
    d = Draft("m")
    d.add(Proposal("measure", "MEASURE a ON u FROM t AS sum(x)")).proposals[0].review = ACCEPTED
    d.add(Proposal("measure", "MEASURE b ON u FROM t AS sum(y)")).proposals[1].review = STRUCK
    cml = d.lower_to_cml()
    assert "MEASURE a" in cml and "MEASURE b" not in cml
    assert cml.startswith("MANIFOLD m VERSION 1")

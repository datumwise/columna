"""Step 1 of the jurisdiction repair — the JURISDICTION SEAM.

Frame-QL Request Adjudication and Disposition Ruling v0.2 §1 stages a request:

    LANGUAGE VALIDITY  ->  ANALYTICAL ADJUDICATION  ->  REALIZATION STANDING
    (Invalid)              (Refuse/Clarify/Admit)       (Realization gap)

The tree could not express that distinction. §3: the `error` mood "carries several unrelated
situations, including malformed/vocabulary/type failures and current-build capability gaps", and
"the conceptual model must not use one status to mean both". Eight of the ten rows in the 2026-09-01
sweep descend from that single conflation.

This commit adds the distinction as a THIRD ELEMENT OF THE CLOSED REASON TABLE and changes no
observable behaviour: the moods are untouched and jurisdiction never reaches the wire, because the
wire vocabulary is held pending its own compatibility ruling (v0.2 §13; Step 6).

Doing it in the table rather than at the call sites is the whole point. `outcome_for` is fail-closed
by a 2026-08-20 ruling, so a reason cannot reach a surface without an entry — which means it cannot
reach a surface without a jurisdiction either. The classification is exhaustive BY CONSTRUCTION, and
stays exhaustive for reasons minted later, with no discipline required of whoever mints them.
"""
import pytest

from columna_core.disclosure import (ANALYTICAL, CLARIFY, ERROR, LANGUAGE, REALIZATION,
                                     REASON_OUTCOME, REFUSE, UNRULED, UNRULED_REASONS,
                                     Refusal, UnregisteredReason, jurisdiction_for, outcome_for)

_STAGES = {LANGUAGE, ANALYTICAL, REALIZATION, UNRULED}


# ── the table is total, and stays total ───────────────────────────────────────────────────────────
def test_every_registered_reason_has_a_jurisdiction():
    for reason, entry in REASON_OUTCOME.items():
        assert len(entry) == 3, f"{reason} was not given a jurisdiction"
        assert entry[2] in _STAGES, (reason, entry[2])


def test_an_unregistered_reason_still_fails_closed():
    """The property that makes the classification exhaustive by construction, re-asserted from the
    jurisdiction side: there is no path to a stage-less verdict."""
    with pytest.raises((UnregisteredReason, KeyError)):
        jurisdiction_for("a_reason_nobody_registered")
    with pytest.raises(UnregisteredReason):
        outcome_for("a_reason_nobody_registered")


def test_unruled_is_confined_to_the_reasons_the_architects_left_open():
    """`unruled` records a live doctrinal question; it must not become a place to put a reason that
    is merely awkward to classify. Ruling 0.1 §9/§13 declines the certification/admission question
    and v0.2 does not reopen it, so exactly these two carry it."""
    unruled = {r for r in REASON_OUTCOME if REASON_OUTCOME[r][2] == UNRULED}
    assert unruled == set(UNRULED_REASONS) == {"uncertified_edge", "uncertified_face"}


# ── stamping ──────────────────────────────────────────────────────────────────────────────────────
def test_classified_stamps_the_jurisdiction_at_the_same_chokepoint_as_the_kind():
    o = Refusal("blocked_reduction", "d").classified()
    assert (o.kind, o.jurisdiction) == (REFUSE, ANALYTICAL)


def test_a_call_site_may_state_its_own_stage_without_minting_a_reason():
    """The seam Step 4 will use. `unsupported` is registered `realization` because that is what the
    reason MEANS, but P1-23 shows call sites where the co-anchor LANGUAGE law is emitted on it. Such
    a site can tell the truth about its stage now, before the reason is split."""
    o = Refusal("unsupported", "co-anchor law", jurisdiction=ANALYTICAL).classified()
    assert o.jurisdiction == ANALYTICAL and o.kind == ERROR   # mood unchanged: no behaviour change here


def test_outcome_for_is_unchanged_for_existing_callers():
    """Deliberately still a 2-tuple. Step 1 is a refactor; widening a helper every caller unpacks
    would make its diff about tuple arity instead of about classification."""
    assert outcome_for("filter_unsupported") == (ERROR, None)
    assert outcome_for("blocked_reduction") == (REFUSE, "unsupported")


# ── the wire is untouched (Step 6 is blocked) ─────────────────────────────────────────────────────
def test_jurisdiction_does_not_reach_the_wire():
    from columna_core.disclosure_wire import wire_outcome
    w = wire_outcome(Refusal("blocked_reduction", "d").classified())
    assert "jurisdiction" not in w
    assert w["kind"] == REFUSE            # the mood a caller sees, unaffected by the internal stage


# ── the payoff: the open rows become enumerable ───────────────────────────────────────────────────
# A reason whose STAGE and whose MOOD disagree is a jurisdiction inversion. Two disagreements are
# expected until Step 6 gives the language and realization stages their own moods, and are NOT
# defects: `language`/`realization` reasons riding `error` is exactly the transitional umbrella v0.2
# §3 permits. Anything else is a live row, and is listed here with the row id so the ledger and the
# build cannot drift apart.
_TRANSITIONAL = {(LANGUAGE, ERROR), (REALIZATION, ERROR)}
# EMPTY SINCE 2026-09-01. `chained_crossing` was the single entry — a REALIZATION standing wearing an
# analytical Refuse — and the shared plan/run repair (P1-21) closed it. The set is kept, with this
# note, because an empty allow-list is the assertion: any future reason whose stage and mood disagree
# has to be added here deliberately, in front of a reviewer, rather than merging quietly.
_KNOWN_INVERSIONS = {}


def _inversions():
    out = {}
    for reason, (kind, _disc, stage) in REASON_OUTCOME.items():
        if stage == UNRULED:
            continue
        if stage == ANALYTICAL and kind in (CLARIFY, REFUSE):
            continue
        if (stage, kind) in _TRANSITIONAL:
            continue
        out[reason] = (stage, kind)
    return out


def test_the_only_reason_level_inversions_are_the_ones_the_ledger_rows():
    """THE POINT OF THE SEAM. Before it, "a realization gap emitted as an analytical Refuse" was a
    claim a human had to make by reading call sites. It is now a computable property of the table,
    and this test is the ledger asserting itself against the build.

    This set must SHRINK. When a repair lands, delete its entry; if that leaves the test red, the
    repair did not do what its commit message said."""
    found = _inversions()
    assert set(found) == set(_KNOWN_INVERSIONS), (
        f"jurisdiction inversions changed. found={found} "
        f"expected={ {r: v[0] for r, v in _KNOWN_INVERSIONS.items()} }")
    for reason, (stage_kind, row, _step) in _KNOWN_INVERSIONS.items():
        assert found[reason] == stage_kind, (reason, found[reason], stage_kind)


def test_no_analytical_reason_hides_in_the_error_umbrella():
    """The half of §3 that is a defect rather than a transition: `error` may temporarily carry
    language and realization failures, but an ANALYTICAL verdict riding `error` is an adjudication
    the caller cannot see. None exist at the reason level; P1-23 and P1-25 are the call-site form,
    which the `jurisdiction=` override addresses in Step 4."""
    assert not [r for r, (k, _d, stage) in REASON_OUTCOME.items()
                if stage == ANALYTICAL and k == ERROR]

"""`manifold_status.evidence.verdicts` — the field that could never report anything.

THE DEFECT (found 2026-09-13, ruled the same day). The tool's published description promises "the
evidence standing (how many adjudicated Licenses are verified / corroborated / untestable)". Its
implementation read `getattr(lic, "verdict", None)` over `PublishedScope.licenses`, whose values are
VERDICT STRINGS — so the attribute lookup always returned None and the counter never incremented.
`evidence.verdicts` was structurally `{}` for every manifold, forever.

WHY IT SURVIVED, WHICH IS THE MORE USEFUL HALF. No `.cml` in this repository declares a derived
`FERTILE` family, so `_snapshot_licenses` produces an empty dict everywhere in-tree, and the only
test asserted `"verdicts" in s["evidence"]` — the key's PRESENCE. A field that cannot be populated is
not tested by a fixture that never populates it, and a presence assertion cannot tell an empty answer
from an impossible one. These tests therefore populate the snapshot deliberately.

WHAT IS NOT CORRECTED HERE: `evidence.licenses`. Its intended population is not established (see the
last test), so it is left exactly as it was pending a ruling rather than redefined in passing.
"""
from __future__ import annotations

import pathlib

import pytest
from columna_core.adjudication import PublishedScope, _snapshot_licenses
from columna_core.model import FamilyMember, License
from columna_server.store import ManifoldStore
from columna_server.tools import manifold_status

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "manifolds"
UNIT = "benchmark"


@pytest.fixture
def store():
    return ManifoldStore(str(FIXTURES))


def _with_scope(store, licenses: dict):
    """Give the loaded unit a published scope carrying `licenses`, leaving everything else real.

    The REAL `PublishedScope` dataclass, with values of the type its own field comment declares —
    `"derived.member" -> verdict`. A stub of the scope would have let this test agree with a wrong
    assumption about the source; the point is to hold the wire to what the source actually produces.
    """
    lm = store.get(UNIT)
    scope = PublishedScope(licenses=licenses)
    lm.provider.published_scope = lambda: scope          # instance-level, this store only
    return store


# ══ THE SOURCE CONTRACT ══════════════════════════════════════════════════════════════════════════

def test_the_snapshot_holds_verdict_strings_not_license_objects():
    """THE PIN THAT MATTERS MOST. The wire code's assumption is checked against its source, so if
    `_snapshot_licenses` ever starts storing `License` objects, this fails HERE — beside the reader
    that would silently start counting nothing again."""
    fm = FamilyMember("sum", declared_lineages=frozenset({"calendar"}),
                      license=License(verdict="verified", lineages=frozenset({"calendar"}),
                                      basis="pinned by test", attestation=None))

    class _Derived:
        family = {"sum": fm}

    class _Model:
        derived = {"aov": _Derived()}

    snap = _snapshot_licenses(_Model())
    assert snap == {"aov.sum": "verified"}
    assert isinstance(snap["aov.sum"], str), "a verdict STRING is what the wire must count"


def test_an_unadjudicated_member_snapshots_as_none():
    fm = FamilyMember("sum", declared_lineages=frozenset(), license=None)

    class _Derived:
        family = {"sum": fm}

    class _Model:
        derived = {"aov": _Derived()}

    assert _snapshot_licenses(_Model()) == {"aov.sum": None}


# ══ THE CORRECTED FIELD ══════════════════════════════════════════════════════════════════════════

def test_verdicts_are_counted_from_a_genuinely_populated_snapshot(store):
    """The three verdicts the published description names, counted, from real snapshot values."""
    _with_scope(store, {"aov.sum": "verified", "aov.last": "verified",
                        "aov.mean": "corroborated", "margin.sum": "untestable"})
    ev = manifold_status(store, UNIT)["evidence"]
    assert ev["verdicts"] == {"verified": 2, "corroborated": 1, "untestable": 1}


def test_an_unexpected_verdict_appears_rather_than_vanishing(store):
    """FAIL CLOSED, like the condition-code vocabulary. A verdict this reader did not anticipate is
    reported, not silently dropped — dropping it is how the original defect read to a caller."""
    _with_scope(store, {"aov.sum": "contradicted"})
    assert manifold_status(store, UNIT)["evidence"]["verdicts"] == {"contradicted": 1}


def test_an_unadjudicated_member_is_not_counted_as_a_verdict(store):
    _with_scope(store, {"aov.sum": "verified", "aov.last": None})
    assert manifold_status(store, UNIT)["evidence"]["verdicts"] == {"verified": 1}


def test_empty_evidence_does_not_regress(store):
    """The everywhere-case in this repository today: no derived FERTILE family, empty snapshot. It
    answered `{}` before the correction and must answer `{}` after — for the opposite reason."""
    _with_scope(store, {})
    assert manifold_status(store, UNIT)["evidence"] == {"licenses": 0, "verdicts": {}}


def test_no_published_scope_at_all_does_not_regress(store):
    lm = store.get(UNIT)
    lm.provider.published_scope = lambda: None
    assert manifold_status(store, UNIT)["evidence"] == {"licenses": 0, "verdicts": {}}


def test_the_real_shipped_fixture_still_answers_exactly_as_before(store):
    """No fixture in this repository populates the snapshot, so every shipped answer is unchanged."""
    assert manifold_status(store, UNIT)["evidence"] == {"licenses": 0, "verdicts": {}}


# ══ THE PUBLIC SHAPE IS UNTOUCHED ════════════════════════════════════════════════════════════════

def test_the_public_payload_shape_is_unchanged(store):
    _with_scope(store, {"aov.sum": "verified"})
    got = manifold_status(store, UNIT)
    assert set(got) == {"contract_version", "manifold_id", "counts", "published_scope", "evidence"}
    assert got["contract_version"] == "5"
    assert set(got["evidence"]) == {"licenses", "verdicts"}
    assert set(got["counts"]) == {"measures", "universes", "levels", "hierarchies", "relations",
                                  "edges", "derived"}
    assert set(got["published_scope"]) == {"blocked_edges"}


# ══ THE FIELD THIS UNIT DELIBERATELY DID NOT REDEFINE ════════════════════════════════════════════

def test_licenses_still_counts_snapshot_entries_including_unadjudicated_ones(store):
    """RECORDED, NOT CORRECTED — the ruling question, pinned as it currently behaves.

    `evidence.licenses` counts ENTRIES in the derived-member snapshot, including members whose
    license is None (unadjudicated). So with the verdicts loop repaired, the two numbers in this
    block can disagree: four entries, three verdicts. That disagreement is now VISIBLE, which is
    what makes the question askable — but answering it means deciding what population the field
    names, and that was not established by the existing docs, tests or rulings.

    This test exists so the current behaviour is a recorded fact rather than an accident, and so a
    later ruling changes it deliberately."""
    _with_scope(store, {"aov.sum": "verified", "aov.last": "verified",
                        "aov.mean": "corroborated", "margin.sum": None})
    ev = manifold_status(store, UNIT)["evidence"]
    assert ev["licenses"] == 4
    assert sum(ev["verdicts"].values()) == 3

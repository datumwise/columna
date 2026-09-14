"""The pre-ingress conformance repair, on the Platform path — OF-47, OF-48, and the dispatch collapse.

Three parts, each pinning a defect that was MEASURED on `main` before the repair:

  1. CONTINUATION CONFORMANCE, as a GATE (ruled 2026-09-14). `continuation_operator` had ZERO
     occurrences in this package: the second profile did not under-check the field, it had no
     continuation conformance at all.

  2. COORDINATE TYPE AND NULLITY (OF-48). The material path established WHAT a delivered value is and
     never WHERE it is. Measured through this same provider and wire: a governed `store: text`
     delivered as `int32` SERVED, with `store=1` on the public wire; a NULL coordinate SERVED, with
     `store=None`.

  3. THE CLOSED REFUSAL DISPATCH. Three sites read `WANT_OF_LAW if isinstance(r, WantOfLaw) else
     WANT_OF_STATE` — a two-way if/else over a growing taxonomy whose `else` was TOTAL, so
     `WantOfCompatibility` reached the wire as `want_of_state` with REMATERIALIZE offered, against
     its own docstring's warning.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pyarrow as pa
import pytest

from columna_core.disclosure import ERROR, REALIZATION, REASON_OUTCOME, outcome_for
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement

from columna_platform import serving
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.refusals import (
    ProofRefusal, RealizationContradictsLaw, UnsupportedByThisProfile, WantOfCompatibility,
    WantOfLaw, WantOfState,
)
from columna_platform.source import MaterialBinding

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fixtures"))
import lighthouse_material as M                                                # noqa: E402

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
PUBLICATION = (Path(__file__).resolve().parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
MAPPING = FIXTURES / "proof_a" / "private-core-mapping-v2.json"
REVENUE = "fam_qv8Ky3mR7bTpZa1LwXcNdg"
ASK = "SELECT revenue AT {store*day}"


def _mapping_file(tmp_path, mutate=None) -> str:
    doc = json.loads(MAPPING.read_text(encoding="utf-8"))
    if mutate:
        mutate(doc)
    out = tmp_path / "private-core-mapping-v2.json"
    out.write_text(json.dumps(doc), encoding="utf-8")
    return str(out)


def _run(tmp_path, *, mutate=None, **columns) -> dict:
    provider = PlatformExecutionProvider.from_artifact(
        str(PUBLICATION), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=_mapping_file(tmp_path, mutate),
                                 sources=M.bindings(**columns)))
    return wire_frame(provider.run(parse_statement(ASK)), universe=None, executed=True)


def _no_result(wire) -> dict:
    return wire["columns"][0]["no_result"]


def _claim(value, family_id=REVENUE):
    _MISSING = object()

    def mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == family_id:
                if value is None:
                    r.pop("continuation_operator", None)
                else:
                    r["continuation_operator"] = value
    return mutate


# ══ 1 · CONTINUATION CONFORMANCE IS A GATE, NOT A DISCLOSURE ════════════════════════════════════

def test_the_conformant_fixture_still_serves(tmp_path):
    """The positive path, first — so every refusal below is a refusal and not a broken fixture."""
    wire = _run(tmp_path)
    assert wire["outcome"] == "serve"
    assert wire["columns"][0]["status"] == "served"
    assert len(wire["columns"][0]["values"]) == 4


def test_an_established_continuation_with_no_claim_does_not_serve(tmp_path):
    """A GATE. The material path does not proceed; nothing is served with a caveat."""
    wire = _run(tmp_path, mutate=_claim(None))
    assert wire["outcome"] != "serve"
    assert "values" not in wire["columns"][0]
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "makes no continuation claim" in _no_result(wire)["detail"]


def test_a_contradicting_continuation_claim_reaches_the_wire_as_a_contradiction(tmp_path):
    """NOT `want_of_state`, and the alternatives are EMPTY.

    Re-materializing the same data cannot repair a claim that contradicts the governing law, so
    offering REMATERIALIZE would send an operator to do work that cannot possibly help."""
    wire = _run(tmp_path, mutate=_claim("min"))
    nr = _no_result(wire)
    assert nr["reason"] == "realization_contradicts_law"
    assert nr["reason"] != "want_of_state"
    assert nr.get("alternatives") in ([], None), nr.get("alternatives")
    assert "REMATERIALIZE" not in json.dumps(wire) and "re-materialization" not in json.dumps(wire)


def test_the_contradiction_detail_names_the_fact_and_not_the_implementation(tmp_path):
    """Ruled: name family/reference, governed C8 fact, realization claim, the contradiction — and
    "do not expose internal implementation identifiers unnecessarily"."""
    detail = _no_result(_run(tmp_path, mutate=_claim("min")))["detail"]
    assert "revenue" in detail            # the canonical reference
    assert "SUM" in detail                # the governed continuation law
    assert "'min'" in detail              # the realization's claim
    assert REVENUE not in detail          # NOT the opaque family id
    assert "columna_platform" not in detail and ".py" not in detail


def test_the_contradiction_is_classified_error_realization(tmp_path):
    wire = _run(tmp_path, mutate=_claim("min"))
    assert outcome_for(_no_result(wire)["reason"]) == (ERROR, None)
    assert REASON_OUTCOME[_no_result(wire)["reason"]][2] == REALIZATION


def test_a_contradiction_is_not_a_proof_refusal_and_cannot_borrow_a_governed_jurisdiction():
    """The structural guarantee, not the behavioural one: a class the governed handler cannot catch
    cannot be handed a governed jurisdiction by it. Same reasoning as `UnsupportedByThisProfile`."""
    assert not issubclass(RealizationContradictsLaw, ProofRefusal)
    assert not issubclass(UnsupportedByThisProfile, ProofRefusal)


# ══ 2 · COORDINATE TYPE AND NULLITY (OF-48) ═════════════════════════════════════════════════════

def test_the_governed_coordinate_types_are_read_at_all(tmp_path):
    """The fact the material path used to drop on the floor, in the same expression, twice."""
    pub, _ = serving.open_publication(str(PUBLICATION))
    assert serving.declared_components(pub, "sale_at") == {"store": "text", "day": "date"}


def test_a_text_coordinate_delivered_as_an_integer_refuses(tmp_path):
    """MEASURED SERVING BEFORE THE REPAIR: `outcome: serve`, four rows, `store=1` as a Python int
    under an anchor the publication declares as `text`."""
    wire = _run(tmp_path, store_code=pa.array([1, 1, 2, 2], type=pa.int32()))
    assert wire["outcome"] != "serve"
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "governed as 'text'" in _no_result(wire)["detail"]
    assert "int32" in _no_result(wire)["detail"]


def test_a_date_coordinate_delivered_as_a_parseable_string_refuses(tmp_path):
    """CLOSED, NOT COERCIBLE. The string WOULD parse; parsing it would put a decision about what
    '2026-01-01' denotes — in which calendar, under which locale — inside admission."""
    wire = _run(tmp_path, sold_on=pa.array(
        ["2026-01-01", "2026-01-02", "2026-01-01", "2026-01-02"], type=pa.string()))
    assert wire["outcome"] != "serve"
    assert "not coercive" in _no_result(wire)["detail"]


@pytest.mark.parametrize("column,array", [
    ("store_code", pa.array(["east", "east", None, "west"], type=pa.string())),
    ("sold_on", pa.array([date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 1), None],
                         type=pa.date32())),
])
def test_a_null_coordinate_refuses_the_carrier(tmp_path, column, array):
    """AN ANALYTICAL POINT CANNOT BE PARTIALLY SPECIFIED merely because Arrow can carry a validity
    bitmap there. Measured serving before the repair, with `store=None` on the public wire."""
    wire = _run(tmp_path, **{column: array})
    assert wire["outcome"] != "serve"
    assert "cannot be partially specified" in _no_result(wire)["detail"]


def test_the_null_refusal_is_the_whole_carrier_and_not_a_dropped_row(tmp_path):
    """The conservative branch, asserted. Dropping the row would silently change which analytical
    points the answer covers — a disclosure question nobody has ruled."""
    wire = _run(tmp_path, store_code=pa.array(["east", "east", None, "west"], type=pa.string()))
    assert "values" not in wire["columns"][0]      # not three rows: none


def test_a_governed_coordinate_type_outside_the_envelope_is_a_capability_limit(tmp_path):
    """An unknown governed type is NOT a defect in the material — it is a limit of this profile.

    The publication may lawfully declare a `timestamp` coordinate; CAP v1 has no mapping for one.
    Telling an operator to RE-MATERIALIZE would send them to fix something that is not theirs to
    fix, so this must not be a want-of-state. Driven through the real provider against a mutated
    publication, not asserted against a hand-raised exception."""
    from columna_platform import admission
    assert set(admission._COORDINATE_TYPES) == {"text", "date"}

    doc = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    for decl in doc["logical"]["declarations"]:
        if decl["kind"] == "anchor" and decl["name"] == "sale_at":
            for comp in decl["body"]["components"]:
                if comp["name"] == "day":
                    comp["type"] = "timestamp"          # lawful governed type; outside CAP v1
    pub_path = tmp_path / "lighthouse-v2-publication.json"
    pub_path.write_text(json.dumps(doc), encoding="utf-8")

    provider = PlatformExecutionProvider.from_artifact(
        str(pub_path), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=_mapping_file(tmp_path), sources=M.bindings()))
    wire = wire_frame(provider.run(parse_statement(ASK)), universe=None, executed=True)

    nr = _no_result(wire)
    assert nr["reason"] == "unsupported", nr
    assert nr["reason"] not in ("want_of_state", "want_of_law")
    assert "timestamp" in nr["detail"] and "does not implement it" in nr["detail"]
    assert "re-materialization" not in json.dumps(wire)


def test_check_5_was_never_this_check(tmp_path):
    """Named because it LOOKS like it. CHECK 5 keys analytical points on coordinate VALUES, so a
    null is a perfectly good key and passes it — which is why a NULL coordinate served for as long
    as it did."""
    wire = _run(tmp_path, store_code=pa.array(["east", "east", None, "west"], type=pa.string()))
    assert "partially specified" in _no_result(wire)["detail"]
    assert "COINCIDENT" not in _no_result(wire)["detail"]


# ══ 3 · THE CLOSED REFUSAL DISPATCH ═════════════════════════════════════════════════════════════

def test_every_concrete_proof_refusal_subclass_has_a_wire_classification():
    """THE COMPLETENESS GUARD. Adding a refusal class without a wire classification must FAIL THE
    BUILD, not inherit `want_of_state` from a fallback — because a fallback is exactly how
    `WantOfCompatibility` came to travel as `want_of_state`."""
    from columna_platform import refusals as _refusals

    # SCOPED TO THE VOCABULARY MODULE, not to every subclass alive in the interpreter: the two tests
    # below deliberately define throwaway subclasses to exercise the guard, and a bare
    # `__subclasses__()` walk would then depend on which test ran first.
    concrete = [c for c in ProofRefusal.__subclasses__()
                if c.__module__ == _refusals.__name__]
    assert concrete, "the subclass walk is not finding the vocabulary module's hierarchy"
    missing = [c.__name__ for c in concrete if c not in serving._REFUSAL_WIRE]
    assert not missing, f"no wire classification for {missing}"
    assert set(serving._REFUSAL_WIRE) == set(concrete), (
        "the mapping and the vocabulary have drifted: "
        f"{sorted(c.__name__ for c in set(serving._REFUSAL_WIRE) ^ set(concrete))}")


def test_the_completeness_guard_actually_fails_on_an_unmapped_class():
    """The guard, exercised. A test that only walks the CURRENT classes would pass forever even if
    `_classify` silently fell back, so the fallback's absence is asserted directly."""
    class _NewlyInvented(ProofRefusal):
        condition = "NewlyInvented"

    try:
        assert _NewlyInvented not in serving._REFUSAL_WIRE
        with pytest.raises(AssertionError, match="no wire classification"):
            serving._classify(_NewlyInvented("a condition nobody classified"))
    finally:
        pass


@pytest.mark.parametrize("cls,reason,alts", [
    (WantOfLaw, "want_of_law", ()),
    (WantOfState, "want_of_state", (serving.REMATERIALIZE,)),
    (WantOfCompatibility, "want_of_compatibility", ()),
])
def test_each_refusal_class_carries_its_own_ruled_reason_and_its_own_alternatives(cls, reason, alts):
    """THE MAPPING DETERMINES ALTERNATIVES AS WELL AS REASONS. Deriving the remedy from the reason is
    how a remedy gets attached to a condition that never asked for one."""
    assert serving._classify(cls("d", subject="s")) == (reason, alts)


def test_want_of_compatibility_no_longer_travels_as_want_of_state():
    """THE MEASURED COLLAPSE, CLOSED. Before the repair this class reached the wire as
    `want_of_state` WITH REMATERIALIZE OFFERED — against its own docstring, which says collapsing it
    "would misdirect every operator who read it"."""
    reason, alts = serving._classify(WantOfCompatibility("incompatible standing"))
    assert reason == "want_of_compatibility"
    assert reason != "want_of_state"
    assert alts == ()
    assert serving.REMATERIALIZE not in alts


def test_classification_is_by_exact_class_and_not_by_isinstance():
    """An `isinstance` walk would silently give a future subclass its parent's reason — the same
    shape of failure as the `else` this replaced, one level down."""
    class _SubtypeOfWantOfState(WantOfState):
        condition = "SubtypeOfWantOfState"

    with pytest.raises(AssertionError, match="no wire classification"):
        serving._classify(_SubtypeOfWantOfState("d"))


def test_the_three_governed_reasons_are_registered_and_distinct():
    reasons = {serving.WANT_OF_LAW, serving.WANT_OF_STATE, serving.WANT_OF_COMPATIBILITY,
               serving.REALIZATION_CONTRADICTS_LAW}
    assert len(reasons) == 4
    for r in reasons:
        assert r in REASON_OUTCOME, r
    assert REASON_OUTCOME["want_of_compatibility"][2] != REASON_OUTCOME["want_of_state"][2]


def test_unsupported_by_this_profile_stays_outside_the_mapping():
    """It travels the capability-error path and must never acquire a governed jurisdiction."""
    assert UnsupportedByThisProfile not in serving._REFUSAL_WIRE
    assert not issubclass(UnsupportedByThisProfile, ProofRefusal)

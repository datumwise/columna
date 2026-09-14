"""PROOF B ON THE SERVING PATH — one positively licensed movement, end to end through ADBC.

THE PROPOSITION: a governed exact sufficient state established at its constitutive anchor can,
WITHIN ONE REQUEST, move to one positively licensed coarser anchor and serve through the existing
public wire — without importing legacy lineage or hierarchy semantics.

    public Frame-QL  ->  governed identity  ->  realization  ->  material fetch  ->  CAP/admission
      ->  state at revenue @ sale_at  ->  governed movement licence  ->  continuation under the
      family's established law  ->  state at revenue @ store  ->  FrameResult  ->  one wire

THE BOUNDARY, AND IT IS THE WHOLE POINT: `sale_at(store x day) -> store`, and nothing broader. No
hierarchy, no lineage, no calendar, no transitive licence, no grand total, no multi-hop.

MECHANICAL COMBINABILITY IS NOT ANALYTICAL PERMISSION. `{store}` is a proper subset of the
constitutive anchor's components and is therefore structurally projectable whether or not anyone
licensed it — which is exactly why the unlicensed ask still refuses. The subset answers *could this
coarsening be realized at all*; the licence answers *may this family be moved*. The first never
answers the second, and the negative controls below are what make that true rather than asserted.

WHY THE LICENCE NAMES THE TARGET. `store` is a COMPONENT of `sale_at`, not a declared anchor of its
own — the publication declares `sale_at{store, day}` and nothing else. A request for `AT {store}`
therefore cannot resolve on its own, and does not: without a licence it refuses exactly as before.
What a positive licence adds is a governed NAME for the target, supplied by the layer that owns the
law, with its components already validated against the DECLARED source anchor. Declaring every
coarsening as its own anchor would have been the alternative, and that would put movement targets
in the publication — the general movement doctrine Proof B explicitly does not establish.
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

import pytest
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_platform import movement, serving
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.refusals import WantOfLaw
from columna_platform.source import MaterialBinding, SourceBindings

from columna_adbc import DuckDbAdbcSource

sys.path.insert(0, str(Path(__file__).parent))
import lighthouse_duckdb as LH                                                 # noqa: E402

REPO = Path(__file__).resolve().parents[3]
PUBLICATION = REPO / "packages/columna-core/tests/fixtures_v2/lighthouse-v2-publication.json"
MAPPING = REPO / "packages/columna-platform/fixtures/proof_a/private-core-mapping-v2.json"

#: THE WITNESS. Two stores, two sale_at points each, unequal contributions, and neither total a
#: round number by accident — so a fold that dropped a row, double-counted, or grouped on the wrong
#: column produces a visibly wrong answer rather than an accidentally right one.
EXPECTED_AT_STORE = {("east", "30.0000"), ("west", "4.9382")}


@pytest.fixture(scope="module")
def pub():
    p, _views = serving.open_publication(str(PUBLICATION))
    return p


def _licence(pub, **kw):
    kw.setdefault("source_anchor", "sale_at")
    kw.setdefault("target_anchor", "store")
    kw.setdefault("target_components", ("store",))
    kw.setdefault("law", "SUM")
    return movement.project(pub, **kw)


def _provider(tmp_path, *, licences=(), source=None):
    src = source if source is not None else DuckDbAdbcSource(path=LH.build(tmp_path), name="wh")
    return PlatformExecutionProvider.from_artifact(
        str(PUBLICATION), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=str(MAPPING),
                                 sources=SourceBindings({LH.CONNECTION: src})),
        movement=tuple(licences)), src


def _wire(provider, ask, *, executed=True):
    return wire_frame(provider.run(parse_statement(ask)), universe=None, executed=executed)


def _no_result(wire):
    return wire["columns"][0]["no_result"]


# ══ the positive control ══════════════════════════════════════════════════════════════════════

def test_a_licensed_movement_serves_the_coarser_anchor(tmp_path, pub):
    """THE WHOLE PROPOSITION, as one wire payload over real DuckDB material."""
    p, src = _provider(tmp_path, licences=[_licence(pub)])
    w = _wire(p, "SELECT revenue AT {store}")

    assert w["outcome"] == "serve"
    assert w["frame"]["anchor"] == ["store"]                 # the TARGET anchor, on the wire
    rows = w["columns"][0]["values"]
    assert {(r["store"], str(r["value"])) for r in rows} == EXPECTED_AT_STORE
    assert all(isinstance(r["value"], Decimal) for r in rows)      # exact, no float hop
    assert all("day" not in r for r in rows)                       # the moved-off coordinate is gone
    assert len(src.fetches) == 1                                   # ONE real material fetch


def test_the_moved_result_is_exact_and_never_touches_a_float(tmp_path, pub):
    """The fold is exact-decimal throughout. `4.9382` is 1.2345 + 3.7037 — a sum that a binary
    float would render as `4.938200000000001` or similar, so the assertion is not decorative."""
    p, _src = _provider(tmp_path, licences=[_licence(pub)])
    w = _wire(p, "SELECT revenue AT {store}")
    west = [r for r in w["columns"][0]["values"] if r["store"] == "west"][0]
    assert west["value"] == Decimal("4.9382")
    assert str(west["value"]) == "4.9382"
    assert not isinstance(west["value"], float)


def test_the_source_anchor_points_are_carried_correctly_before_continuation(tmp_path, pub):
    """The un-moved ask over the SAME source must still serve its four sale_at points. If the four
    were wrong, the two totals could still look right for the wrong reason."""
    p, _src = _provider(tmp_path, licences=[_licence(pub)])
    w = _wire(p, "SELECT revenue AT {store*day}")
    assert w["outcome"] == "serve"
    assert w["frame"]["anchor"] == ["sale_at"]
    assert len(w["columns"][0]["values"]) == 4
    assert sum(r["value"] for r in w["columns"][0]["values"]) == Decimal("34.9382")


def test_the_family_identity_is_unchanged_by_the_movement(tmp_path, pub):
    """SAME family, different anchor. The path by which a state arrived is standing, not identity —
    and the served column is still the same governed family's."""
    p, _src = _provider(tmp_path, licences=[_licence(pub)])
    moved = _wire(p, "SELECT revenue AT {store}")
    still = _wire(p, "SELECT revenue AT {store*day}")
    assert moved["columns"][0]["name"] == still["columns"][0]["name"] == "revenue"
    assert moved["frame"]["anchor"] != still["frame"]["anchor"]


def test_the_source_state_is_not_mutated_by_the_movement(pub):
    """`continue_to` returns a NEW state. The retained source must still be the four-point state at
    `sale_at`, or a second consumer of it would be served a folded value it never asked for."""
    from columna_platform import carrier, continuation
    from columna_platform.state import AnalyticalIdentity, RetainedStateStore

    _pub, views = serving.open_publication(str(PUBLICATION))
    family = [f for f in _pub.families if f.family_id == "fam_qv8Ky3mR7bTpZa1LwXcNdg"][0]
    view = views[family.family_id]
    real = serving.realize(serving.bind(_pub, str(MAPPING)), family.family_id)

    store = RetainedStateStore()
    source = serving.materialize_anchored(
        _pub, family, view, real, carrier.exact_money_at_sale_at(),
        basis=view["sufficient_state_bases"].value, store=store)
    before = (source.identity, len(source.array), source.anchor_columns,
              source.standing.movement)

    moved = continuation.continue_to(view, source, _licence(_pub), target_anchor="store")

    # the source, untouched
    assert (source.identity, len(source.array), source.anchor_columns,
            source.standing.movement) == before
    assert source.identity == AnalyticalIdentity(family.family_id, "sale_at")
    assert len(source.array) == 4
    assert source.standing.movement is None

    # the target, new
    assert moved.identity == AnalyticalIdentity(family.family_id, "store")
    assert len(moved.array) == 2
    assert moved.standing.movement == _licence(_pub).describe()
    assert moved.identity.family_id == source.identity.family_id


def test_standing_is_carried_forward_and_records_the_licence(pub):
    """Exactly what changes between source and target standing, asserted field by field — so a
    later edit that quietly carried something else forward has to say so."""
    import dataclasses

    from columna_platform import carrier, continuation
    from columna_platform.state import RetainedStateStore

    _pub, views = serving.open_publication(str(PUBLICATION))
    family = [f for f in _pub.families if f.family_id == "fam_qv8Ky3mR7bTpZa1LwXcNdg"][0]
    view = views[family.family_id]
    real = serving.realize(serving.bind(_pub, str(MAPPING)), family.family_id)
    source = serving.materialize_anchored(
        _pub, family, view, real, carrier.exact_money_at_sale_at(),
        basis=view["sufficient_state_bases"].value, store=RetainedStateStore())

    moved = continuation.continue_to(view, source, _licence(_pub), target_anchor="store")

    a = dataclasses.asdict(source.standing)
    b = dataclasses.asdict(moved.standing)
    changed = {k for k in a if a[k] != b[k]}
    assert changed == {"movement"}, f"movement should be the only standing change, got {changed}"
    assert b["movement"] == "sale_at(store*day) -> store(store) under SUM [positive]"
    assert b["currency"] is None            # NOT manufactured by the movement
    assert b["constitution"] == a["constitution"] and b["realization"] == a["realization"]


# ══ the negative controls ═════════════════════════════════════════════════════════════════════

def test_1_a_projectable_target_with_NO_licence_refuses(tmp_path, pub):
    """MECHANICAL COMBINABILITY IS NOT ANALYTICAL PERMISSION. `{store}` is a proper subset of the
    constitutive anchor and is trivially foldable. It refuses anyway, and that is the proposition."""
    p, src = _provider(tmp_path, licences=[])
    w = _wire(p, "SELECT revenue AT {store}")
    assert w["outcome"] != "serve"
    assert _no_result(w)["reason"] == "want_of_law"
    assert len(src.fetches) == 0                     # refused on LAW, before any material


@pytest.mark.parametrize("label,kw", [
    ("another target", {"target_anchor": "elsewhere", "target_components": ("day",)}),
    ("another source", {"source_anchor": "not_sale_at"}),
])
def test_2_and_3_a_licence_for_another_movement_does_not_license_this_one(tmp_path, pub, label, kw):
    """A licence is SPECIFIC. One for a different target, or off a different source, licenses
    nothing here — and must not be read as general movement authority."""
    if kw.get("source_anchor") == "not_sale_at":
        with pytest.raises(WantOfLaw):               # the anchor is not declared; no licence exists
            _licence(pub, **kw)
        return
    p, src = _provider(tmp_path, licences=[_licence(pub, **kw)])
    w = _wire(p, "SELECT revenue AT {store}")
    assert w["outcome"] != "serve"
    assert _no_result(w)["reason"] == "want_of_law"
    assert len(src.fetches) == 0


def test_4_a_licence_whose_law_mismatches_the_governed_continuation_refuses(tmp_path, pub):
    """The licence claims MIN; the family's established continuation law is SUM. A licence under
    the wrong law is not a licence for this movement — and the refusal is LAW, not arithmetic."""
    p, src = _provider(tmp_path, licences=[_licence(pub, law="MIN")])
    w = _wire(p, "SELECT revenue AT {store}")
    assert w["outcome"] != "serve"
    assert _no_result(w)["reason"] == "want_of_law"
    assert len(src.fetches) == 0


def test_5_a_target_inventing_a_coordinate_is_refused_at_projection(pub):
    """Refused BEFORE any arithmetic, and before a licence object even exists: `project` validates
    the target against the DECLARED components of the source anchor, so an invented coordinate
    cannot become a licence that something later has to catch."""
    with pytest.raises(WantOfLaw) as e:
        _licence(pub, target_components=("region",))
    assert "not declared components" in str(e.value)


def test_6_the_full_source_anchor_is_not_a_movement(tmp_path, pub):
    """`AT {store*day}` IS the constitutive anchor. Asking for it is not movement, must not consume
    a licence, and must serve the four points — even with a licence present."""
    p, src = _provider(tmp_path, licences=[_licence(pub)])
    w = _wire(p, "SELECT revenue AT {store*day}")
    assert w["outcome"] == "serve"
    assert w["frame"]["anchor"] == ["sale_at"]
    assert len(w["columns"][0]["values"]) == 4
    assert len(src.fetches) == 1

    # And the licence cannot be projected onto the whole anchor either — that would make every
    # family trivially "movable" to itself.
    with pytest.raises(WantOfLaw) as e:
        _licence(pub, target_anchor="sale_at", target_components=("store", "day"))
    assert "not a movement" in str(e.value)


def test_7_the_grand_total_stays_outside_this_proof(tmp_path, pub):
    """`AT {}` is a projection onto the grand total. Outside the admitted movement notion, refused
    on both sides: the request refuses it, and a licence for it cannot be projected."""
    p, src = _provider(tmp_path, licences=[_licence(pub)])
    w = _wire(p, "SELECT revenue AT {}")
    assert w["outcome"] != "serve"
    assert _no_result(w)["reason"] == "want_of_law"
    assert len(src.fetches) == 0

    with pytest.raises(WantOfLaw) as e:
        _licence(pub, target_anchor="total", target_components=())
    assert "grand total" in str(e.value)


def test_8_movement_law_is_checked_before_any_fold(tmp_path, pub):
    """Asserted by COST, which is the only way to assert an ordering from outside: every unlicensed
    or wrongly-licensed movement above refuses with ZERO material fetches. The values are trivially
    foldable — the refusal is not the arithmetic failing, it is the law being asked first."""
    for licences in ([], [_licence(pub, law="MIN")],
                     [_licence(pub, target_anchor="elsewhere", target_components=("day",))]):
        p, src = _provider(tmp_path, licences=licences)
        w = _wire(p, "SELECT revenue AT {store}")
        assert _no_result(w)["reason"] == "want_of_law"
        assert src.fetches == [], "material was read before the law refused"


def test_9_no_legacy_core_execution_participates(tmp_path, pub):
    """No Planner, engine, hierarchy, FunctionalEdge, blocked-lineage machinery or `.cml`. Asserted
    against the SOURCE of the modules that perform the movement, so it cannot drift."""
    import columna_platform.continuation as C
    import columna_platform.movement as M
    import columna_platform.serving as S

    for mod in (C, M, S):
        src = Path(mod.__file__).read_text(encoding="utf-8")
        for forbidden in ("from columna_core.planner", "from columna_core.engine",
                          "from columna_core.model", "FunctionalEdge", "blocked_lineage",
                          ".cml", "import parser"):
            assert forbidden not in src, f"{Path(mod.__file__).name} names {forbidden}"


def test_10_continuation_introduces_no_extra_material_fetch(tmp_path, pub):
    """The movement folds a state that is already in hand. A second fetch would mean the coarser
    ask had re-read the source, which is the defect this control exists to exclude."""
    p_moved, src_moved = _provider(tmp_path, licences=[_licence(pub)])
    _wire(p_moved, "SELECT revenue AT {store}")

    p_plain, src_plain = _provider(tmp_path, licences=[_licence(pub)])
    _wire(p_plain, "SELECT revenue AT {store*day}")

    assert len(src_moved.fetches) == len(src_plain.fetches) == 1
    assert src_moved.fetches[0][:3] == src_plain.fetches[0][:3]     # the same projection, too


# ══ check and execute agree ═══════════════════════════════════════════════════════════════════

def test_check_and_execute_agree_about_the_movement(tmp_path, pub):
    """`check_frame_query` plans and `execute_frame_query` runs. They must not disagree about
    whether a movement is licensed — the pre-flight asks the SAME law question, through the same
    `require_licensed`, and consults no state to do it."""
    licensed, _ = _provider(tmp_path, licences=[_licence(pub)])
    unlicensed, _ = _provider(tmp_path, licences=[])
    stmt = parse_statement("SELECT revenue AT {store}")

    assert licensed.plan(stmt).columns[0].refusal is None
    assert licensed.run(stmt).columns[0].refusal is None
    assert unlicensed.plan(stmt).columns[0].refusal.reason == "want_of_law"
    assert unlicensed.run(stmt).columns[0].refusal.reason == "want_of_law"


def test_two_licences_naming_different_targets_refuse_rather_than_pick(tmp_path, pub):
    """A deployment that has said two things is not resolved by listing order."""
    p, _src = _provider(tmp_path, licences=[
        _licence(pub),
        _licence(pub, target_anchor="shop"),
    ])
    w = _wire(p, "SELECT revenue AT {store}")
    assert w["outcome"] != "serve"
    assert _no_result(w)["reason"] == "want_of_law"


def test_no_physical_identifier_reaches_the_moved_wire(tmp_path, pub):
    """The rename holds through the movement too."""
    p, _src = _provider(tmp_path, licences=[_licence(pub)])
    payload = json.dumps(_wire(p, "SELECT revenue AT {store}"), default=str)
    for physical in (LH.STORE_COLUMN, LH.DAY_COLUMN, LH.VALUE_COLUMN, LH.TABLE):
        assert physical not in payload, physical

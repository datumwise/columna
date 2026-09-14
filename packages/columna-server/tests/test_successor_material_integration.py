"""THE FIRST MATERIAL EXECUTION THROUGH THE PUBLIC MCP SURFACE — `execute_frame_query`, end to end.

The preflight proof beside this one established that a public Frame-QL request reaches a governed
`family_id @ anchor` without the legacy ontology and comes back through the one existing server-side
wire path, TOUCHING NO DATA. This one touches data.

    public Frame-QL  →  governed identity  →  ratified realization claim  →  a deployment-local
    material source  →  admission  →  request-local sufficient state  →  the SAME wire

WHAT WOULD MAKE THIS WORTHLESS, and is asserted rather than assumed:

  · that Core served it (asserted: `CoreExecutionProvider` is never constructed, and the legacy
    execution modules are never imported by the path);
  · that the answer lost the analytical point (asserted: the rows carry `store` and `day`);
  · that the exact decimal quietly became a float (asserted: `Decimal`, and a sum that a float
    would miss);
  · that a capability limit was dressed as a governed refusal, or the reverse (asserted: one
    deployment, three asks, three different kinds of answer).

The unit is successor-native: a `governed-publication.json` alone in a directory. The realization
claim and the material source are DEPLOYMENT-PRIVATE and are injected — they are not in the unit,
because a successor-native unit IS the publication.
"""
from __future__ import annotations

import pathlib
import sys
from decimal import Decimal

import pytest
from columna_server.store import RUNTIME_PLATFORM, ManifoldStore
from columna_server.tools import execute_frame_query

PLATFORM = pathlib.Path(__file__).parents[2] / "columna-platform"
sys.path.insert(0, str(PLATFORM / "fixtures"))

pytest.importorskip("columna_platform", reason="the successor runtime is a workspace install")
import lighthouse_material as M                                              # noqa: E402
from columna_platform.source import MaterialBinding                          # noqa: E402

V2_ARTIFACT = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
MAPPING = PLATFORM / "fixtures" / "proof_a" / "private-core-mapping-v2.json"
UNIT = "lighthouse"
GOOD = "SELECT revenue AT {store*day}"


@pytest.fixture
def served(tmp_path):
    """The successor-native unit, selected, WITH a deployment material binding."""
    d = tmp_path / UNIT
    d.mkdir()
    (d / "governed-publication.json").write_text(V2_ARTIFACT.read_text(encoding="utf-8"),
                                                 encoding="utf-8")
    return ManifoldStore(
        str(tmp_path),
        runtime_selection={UNIT: RUNTIME_PLATFORM},
        material_bindings={UNIT: MaterialBinding(mapping_path=str(MAPPING),
                                                 sources=M.bindings())})


# ══ THE POSITIVE PATH ════════════════════════════════════════════════════════════════════════════

def test_execute_frame_query_serves_a_governed_family_from_material(served):
    """The whole proposition, as a caller of the public tool sees it."""
    wire = execute_frame_query(served, UNIT, GOOD)
    assert wire["outcome"] == "serve"
    assert wire["executed"] is True
    assert wire["contract_version"] == "5"
    assert wire["manifold_id"] == UNIT
    assert wire["frame"]["anchor"] == ["sale_at"]
    assert wire["columns"][0]["status"] == "served"


def test_the_public_rows_carry_the_governed_anchor_coordinates(served):
    """P5-03 at the public surface. `{store, day, value}`, not four anonymous numbers.

    No new wire shape was needed: `_values` has emitted `{group-dims…, value}` rows for as long as
    there have been dimensions to emit. What was new was a successor frame that carried them."""
    rows = execute_frame_query(served, UNIT, GOOD)["columns"][0]["values"]
    assert [sorted(r) for r in rows] == [["day", "store", "value"]] * 4
    assert {(r["store"], str(r["day"])) for r in rows} == {
        ("east", "2026-01-01"), ("east", "2026-01-02"),
        ("west", "2026-01-01"), ("west", "2026-01-02")}


def test_the_exact_decimal_survives_the_public_wire(served):
    """`1.2345 + 3.7037` is not representable in binary floating point. If any hop on this path had
    gone through a float, this total would miss — which is the point of choosing those values."""
    values = [r["value"] for r in execute_frame_query(served, UNIT, GOOD)["columns"][0]["values"]]
    assert all(isinstance(v, Decimal) for v in values), [type(v).__name__ for v in values]
    assert sum(values) == Decimal("34.9382")


def test_no_fetches_delta_is_claimed_for_a_provider_that_counts_none(served):
    """Unchanged from the preflight slice, and it must stay unchanged now that data IS touched:
    Platform is not `SupportsExecutionDiagnostics`, so the server omits the key rather than
    reporting a zero it did not measure."""
    assert "fetches_delta" not in execute_frame_query(served, UNIT, GOOD)


# ══ NO CORE, ANYWHERE ════════════════════════════════════════════════════════════════════════════

def test_material_execution_never_constructs_the_core_provider(served, monkeypatch):
    """The strongest form available: make constructing Core's provider fail the test outright."""
    import columna_server.provider as sp

    def _boom(*a, **k):                                             # pragma: no cover - must not run
        raise AssertionError("the successor path constructed CoreExecutionProvider")

    monkeypatch.setattr(sp, "CoreExecutionProvider", _boom)
    assert execute_frame_query(served, UNIT, GOOD)["outcome"] == "serve"


def test_the_unit_carries_no_cml_and_has_no_legacy_model(served, tmp_path):
    assert not list(pathlib.Path(tmp_path).rglob("*.cml"))
    assert served.get(UNIT).manifold is None


# ══ THE THREE KINDS OF ANSWER, FROM ONE DEPLOYMENT ══════════════════════════════════════════════

def test_an_ask_off_the_constitutive_anchor_is_a_GOVERNED_refusal(served):
    """Movement without a positive licence. A capability reason here would tell an operator to wait
    for a feature, when what is missing is a governed licence no feature supplies."""
    wire = execute_frame_query(served, UNIT, "SELECT revenue AT {store}")
    assert wire["outcome"] == "refuse"
    assert wire["columns"][0]["no_result"]["reason"] == "want_of_law"


def test_an_ask_this_profile_does_not_implement_is_a_CAPABILITY_limit(served):
    """`unsupported` — ERROR mood, already registered, minted nothing. Not `want_of_*`: the request
    was not answered at all, and saying it was unlawful would be a different and false claim."""
    wire = execute_frame_query(served, UNIT, "SELECT revenue, revenue AT {store*day}")
    assert wire["outcome"] == "error"
    assert wire["columns"][0]["no_result"]["reason"] == "unsupported"


def test_the_three_outcomes_are_distinguishable_at_the_public_surface(served):
    outcomes = {
        execute_frame_query(served, UNIT, GOOD)["outcome"],
        execute_frame_query(served, UNIT, "SELECT revenue AT {store}")["outcome"],
        execute_frame_query(served, UNIT, "SELECT revenue, revenue AT {store*day}")["outcome"],
    }
    assert outcomes == {"serve", "refuse", "error"}


# ══ THE DEPLOYMENT BINDING IS LOAD-BEARING ══════════════════════════════════════════════════════

def test_moving_the_connection_binding_stops_the_request(tmp_path):
    """R1's invariant at the public surface: the claim still says `warehouse`, the deployment binds
    the same bytes elsewhere, and the request stops serving. Nothing else differs."""
    d = tmp_path / UNIT
    d.mkdir()
    (d / "governed-publication.json").write_text(V2_ARTIFACT.read_text(encoding="utf-8"),
                                                 encoding="utf-8")
    store = ManifoldStore(
        str(tmp_path), runtime_selection={UNIT: RUNTIME_PLATFORM},
        material_bindings={UNIT: MaterialBinding(mapping_path=str(MAPPING),
                                                 sources=M.bindings(connection="elsewhere"))})
    wire = execute_frame_query(store, UNIT, GOOD)
    assert wire["outcome"] == "refuse"
    assert wire["columns"][0]["no_result"]["reason"] == "want_of_state"


def test_the_preflight_still_touches_nothing_on_a_bound_deployment(served):
    """`check_frame_query` is UNCHANGED by this slice, and that has to be asserted now that a
    material binding exists: a pre-flight that consulted material would be answering a different
    question — "can this be served right now" rather than "is this askable"."""
    from columna_server.tools import check_frame_query
    wire = check_frame_query(served, UNIT, GOOD)
    assert wire["outcome"] == "serve"
    assert wire["executed"] is False
    assert wire["columns"][0].get("values") is None
    assert wire["columns"][0].get("value") is None


# ══ THE CONSTRUCTED FAMILY, AT THE PUBLIC SURFACE (second material slice, 2026-09-14) ═══════════

MIN_ASK = "SELECT min(revenue@sale_at) AT {store*day}"


def test_a_constructed_family_is_served_from_governed_formation_law(served):
    """The second slice's whole claim, as a caller of the public tool sees it: the successor is not
    special-cased to primitive SUM.

    DEGENERATE BY CONSTRUCTION, and said so here as well as in the platform suite: at coincident
    grain each fiber holds one contribution, so MIN returns the value it selected from. What this
    proves is that a CONSTRUCTED family executes from its cited foundation law — not that
    aggregation over several contributions works, which is the finer branch and still refuses."""
    wire = execute_frame_query(served, UNIT, MIN_ASK)
    assert wire["outcome"] == "serve"
    assert wire["executed"] is True
    assert wire["columns"][0]["name"] == "min(revenue@sale_at)"
    rows = wire["columns"][0]["values"]
    assert [sorted(r) for r in rows] == [["day", "store", "value"]] * 4
    assert all(isinstance(r["value"], Decimal) for r in rows)


def test_the_constructed_and_primitive_families_agree_at_coincident_grain(served):
    """The degeneracy, at the public surface. Equality here is the EXPECTED result and is asserted
    so that a future reader cannot mistake a passing constructed-family test for evidence of a
    non-trivial fold."""
    def by_point(ask):
        return {(r["store"], str(r["day"])): r["value"]
                for r in execute_frame_query(served, UNIT, ask)["columns"][0]["values"]}
    assert by_point(MIN_ASK) == by_point(GOOD)


def test_count_is_refused_at_the_public_surface_without_reading_its_target(served):
    """OF-44 held. COUNT carries a realization claim in the fixture, so this is not "no claim": it
    is the composition gate, reached from a governed fact about the law, saying nothing about
    §11.5.1."""
    wire = execute_frame_query(served, UNIT, "SELECT count(revenue@sale_at) AT {store*day}")
    assert wire["outcome"] == "error"
    detail = wire["columns"][0]["no_result"]["detail"]
    assert wire["columns"][0]["no_result"]["reason"] == "unsupported"
    assert "declares no composition over operand values" in detail
    assert "11.5.1" not in detail

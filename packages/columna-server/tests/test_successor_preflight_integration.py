"""THE FIRST SHIPPED-PATH SUCCESSOR INTEGRATION — `check_frame_query` end to end.

One explicitly opted-in v2 governed unit with no `manifold.cml`, one family, one tool. A public
Frame-QL request enters the MCP surface, is resolved to a governed `family_id @ anchor` WITHOUT the
legacy measure/member ontology, planned by `PlatformExecutionProvider`, and serialized by the ONE
existing server-side wire path. No data is touched.

WHAT WOULD MAKE THIS PROOF WORTHLESS, and is therefore asserted here rather than assumed:

  · that the successor path quietly used Core (it does not — the provider is Platform's own, and
    Core's provider methods are never reached);
  · that the answer came from a second serializer (it does not — `wire_frame` is applied once, by
    the server, and the wire is byte-shaped exactly like Core's);
  · that identity came from a `.cml` (there is no `.cml` in the unit at all);
  · that a physical identifier leaked (nothing physical is anywhere near this path).
"""
from __future__ import annotations

import pathlib

import pytest
from columna_server.store import RUNTIME_PLATFORM, ManifoldStore
from columna_server.tools import ToolInputError, check_frame_query, describe_manifold, execute_frame_query

V2_ARTIFACT = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
UNIT = "lighthouse"
GOOD = "SELECT revenue AT {store*day}"


@pytest.fixture
def opted_in(tmp_path):
    """The successor-native unit: the publication, alone in its directory, explicitly selected."""
    d = tmp_path / UNIT
    d.mkdir()
    (d / "governed-publication.json").write_text(V2_ARTIFACT.read_text(encoding="utf-8"),
                                                 encoding="utf-8")
    return ManifoldStore(str(tmp_path), runtime_selection={UNIT: RUNTIME_PLATFORM})


# ══ THE POSITIVE PATH ════════════════════════════════════════════════════════════════════════════

def test_the_public_preflight_serves_through_the_successor_path(opted_in):
    """The whole slice, as a caller sees it."""
    wire = check_frame_query(opted_in, UNIT, GOOD)

    assert wire["contract_version"] == "5"          # unchanged, and stamped by the server
    assert wire["outcome"] == "serve"               # the would-be mood
    assert wire["executed"] is False                # a pre-flight, and the server said so
    assert wire["manifold_id"] == UNIT              # server-side stamping, the one existing path
    assert wire["manifold_version"] == "1.0.0"      # a governed publication, so the version discloses
    assert wire["frame"]["anchor"] == ["store", "day"]
    assert [c["name"] for c in wire["columns"]] == ["revenue"]
    assert wire["columns"][0]["status"] == "served"
    assert "no_result" not in wire["columns"][0]
    assert "fetches_delta" not in wire, (
        "no fetch concept exists on this path and none may be fabricated")


def test_no_data_is_touched(opted_in, monkeypatch):
    """NOTHING MATERIAL. The unit has no connector and no warehouse — there is nothing to read —
    and the proof of it is that a DuckDB connection cannot even be opened in this process."""
    import columna_server.store as st
    monkeypatch.setattr(st, "_load_duckdb", lambda *a, **k: pytest.fail("a connector was opened"))
    assert check_frame_query(opted_in, UNIT, GOOD)["outcome"] == "serve"


def test_the_wire_is_shaped_exactly_like_cores(opted_in):
    """ONE SERIALIZER, so the successor's answer is not a lookalike of the wire — it IS the wire.
    Compared against a Core-served pre-flight from the shipped demo, key for key."""
    from columna_server.demo import demo_dir

    core = check_frame_query(ManifoldStore(demo_dir()), "cascadia", "SELECT revenue AT {region}")
    successor = check_frame_query(opted_in, UNIT, GOOD)

    # The two OPTIONAL keys differ for reasons that are themselves the contract, and neither is a
    # shape difference: `manifold_version` appears only for a governed publication (the successor
    # unit has one, the legacy demo does not), and `fetches_delta` appears only for a provider that
    # reports a fetch counter (Core does, the successor has no fetch concept and fabricates none).
    optional = {"manifold_version", "fetches_delta"}
    assert set(successor) - optional == set(core) - optional
    assert "manifold_version" in successor and "manifold_version" not in core
    assert "fetches_delta" in core and "fetches_delta" not in successor

    assert set(successor["frame"]) == set(core["frame"])
    assert set(successor["columns"][0]) >= {"name", "status", "disclosures"}


def test_identity_came_from_the_governed_publication_and_there_is_no_cml_to_have_used(opted_in, tmp_path):
    """`.cml` IS NOT CONSULTED — because there is none, anywhere in the unit."""
    assert not list(tmp_path.rglob("*.cml"))
    assert opted_in.get(UNIT).manifold is None
    assert check_frame_query(opted_in, UNIT, GOOD)["outcome"] == "serve"


def test_no_physical_identifier_reaches_the_wire(opted_in):
    import json
    blob = json.dumps(check_frame_query(opted_in, UNIT, GOOD))
    for physical in ("sales_lines", "warehouse", "store_id", "sale_date", "connection", "table"):
        assert physical not in blob


# ══ NEGATIVE CONTROLS ════════════════════════════════════════════════════════════════════════════

def test_an_unknown_series_refuses_and_never_guesses(opted_in):
    wire = check_frame_query(opted_in, UNIT, "SELECT revenu AT {store*day}")
    assert wire["outcome"] == "refuse"
    col = wire["columns"][0]
    assert col["name"] == "revenu"                          # verbatim, never corrected
    assert col["no_result"]["reason"] == "want_of_law"
    assert "no governed family answers" in col["no_result"]["detail"]


def test_an_unlicensed_anchor_refuses(opted_in):
    """A proper subset of the constitutive anchor is structurally projectable, and refuses: mechanical
    combinability is not analytical permission."""
    wire = check_frame_query(opted_in, UNIT, "SELECT revenue AT {store}")
    assert wire["outcome"] == "refuse"
    assert wire["columns"][0]["no_result"]["reason"] == "want_of_law"


def test_an_undeclared_anchor_refuses_naming_what_is_declared(opted_in):
    wire = check_frame_query(opted_in, UNIT, "SELECT revenue AT {region}")
    assert wire["outcome"] == "refuse"
    assert "sale_at{day*store}" in wire["columns"][0]["no_result"]["detail"]


def test_a_syntax_error_still_lands_in_the_existing_syntax_channel(opted_in):
    """Public Frame-QL syntax is unchanged, and so is what happens when it is violated: the parse
    fails BEFORE any successor code runs, through the server's existing error wire."""
    wire = check_frame_query(opted_in, UNIT, "SELECT revenue")
    assert wire["outcome"] == "error"
    assert wire["contract_version"] == "5"


def test_material_execution_is_refused_and_does_not_fall_back_to_core(opted_in):
    """`run` is not implemented by this profile and is not quietly handed to Core. It raises out of
    the provider rather than answering — reported as a finding, since mapping it to a wire mood is a
    public-surface ruling this slice was not given."""
    with pytest.raises(Exception) as e:
        execute_frame_query(opted_in, UNIT, GOOD)
    assert "does not execute" in str(e.value)
    assert "columna_core.planner" not in str(type(e.value).__mro__)


def test_legacy_model_tools_refuse_honestly_rather_than_erroring_on_a_missing_manifold(opted_in):
    """`describe_manifold` presents the legacy read model, which this unit does not have. It says so
    through the existing structural channel instead of raising AttributeError on None."""
    with pytest.raises(ToolInputError) as e:
        describe_manifold(opted_in, UNIT)
    assert "no_legacy_model" in str(e.value)


def test_an_unselected_unit_is_visible_but_not_servable(tmp_path):
    """THE CONTROL ON THE OPT-IN. Same artifact, no selection: the catalog shows the lineage, and
    every serving attempt gets `not_realizable_here` — the pre-existing public state."""
    d = tmp_path / UNIT
    d.mkdir()
    (d / "governed-publication.json").write_text(V2_ARTIFACT.read_text(encoding="utf-8"),
                                                 encoding="utf-8")
    store = ManifoldStore(str(tmp_path), runtime_selection={})
    with pytest.raises(ToolInputError) as e:
        check_frame_query(store, UNIT, GOOD)
    assert "not_realizable_here" in str(e.value)


def test_the_legacy_demo_is_completely_unaffected():
    """v1 + Core + `.cml`, with no selection anywhere: byte-identical behaviour to before this unit."""
    from columna_server.demo import demo_dir

    store = ManifoldStore(demo_dir())
    wire = check_frame_query(store, "cascadia", "SELECT revenue AT {region}")
    assert wire["contract_version"] == "5" and wire["executed"] is False
    assert store.get("cascadia").manifold is not None
    assert type(store.get("cascadia").provider).__name__ == "CoreExecutionProvider"


# ══ ISOLATION ════════════════════════════════════════════════════════════════════════════════════

def test_the_successor_provider_is_platforms_own_and_core_is_never_constructed(opted_in, monkeypatch):
    """No Core runtime is built for this unit — not lazily, not as a fallback, not at all."""
    import columna_server.provider as prov
    monkeypatch.setattr(prov, "CoreExecutionProvider",
                        lambda *a, **k: pytest.fail("a Core provider was constructed"))
    assert type(opted_in.get(UNIT).provider).__module__ == "columna_platform.provider"
    assert check_frame_query(opted_in, UNIT, GOOD)["outcome"] == "serve"

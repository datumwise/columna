"""`discovery`, answered from the governed publication — the first governed-native read-only tool.

Ruled Huayin 2026-09-14. Every governed family is its own `measures[]` row, primitive and
constructed alike; constructed families are families in their own right and are NOT projected back
into the legacy member/reducer ontology; `reducers` is empty for governed rows.

THE CONTROL THAT MAKES THE REST MEAN ANYTHING is `test_every_listed_measure_actually_resolves`: a
discovery response is a PROMISE ABOUT WHAT CAN BE ASKED, so every reference it returns is put back
through the successor resolver and must resolve. A catalogue that lists something unaskable is worse
than one that lists nothing.
"""
from __future__ import annotations

import json
import pathlib

import pytest
from columna_server.store import RUNTIME_PLATFORM, ManifoldStore
from columna_server.tools import check_frame_query, discovery

V2_ARTIFACT = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
LEGACY_FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "manifolds"
UNIT = "lighthouse"

#: Every family the lighthouse publication declares — one primitive, three constructed.
PRIMITIVE = "revenue"
CONSTRUCTED = ("count(revenue@sale_at)", "min(revenue@sale_at)", "max(revenue@sale_at)")


@pytest.fixture
def store(tmp_path):
    d = tmp_path / UNIT
    d.mkdir()
    (d / "governed-publication.json").write_text(V2_ARTIFACT.read_text(encoding="utf-8"),
                                                 encoding="utf-8")
    return ManifoldStore(str(tmp_path), runtime_selection={UNIT: RUNTIME_PLATFORM})


# ══ 1-3 · EVERY FAMILY IS ITS OWN ROW, AND NO ROW CARRIES REDUCERS ═══════════════════════════════

def test_the_primitive_family_appears_as_its_own_row(store):
    rows = {m["measure"]: m for m in discovery(store, UNIT)["measures"]}
    assert PRIMITIVE in rows
    assert rows[PRIMITIVE]["universe"] == "sales"
    assert rows[PRIMITIVE]["grain"] == ["day", "store"]


def test_every_constructed_family_appears_as_its_own_row(store):
    """NOT hidden to preserve legacy row cardinality. Four families, four rows."""
    rows = {m["measure"] for m in discovery(store, UNIT)["measures"]}
    assert rows == {PRIMITIVE, *CONSTRUCTED}


def test_every_governed_row_has_empty_reducers(store):
    assert all(m["reducers"] == [] for m in discovery(store, UNIT)["measures"])


def test_no_constructed_family_is_smuggled_into_a_reducer_suffix(store):
    """Control 4. `count(revenue@sale_at)` is not a legal suffix after a dot, and putting it in
    `reducers` would silently redefine the field for every existing reader. Asserted over the whole
    serialized response so it cannot hide in any nested position."""
    blob = json.dumps(discovery(store, UNIT))
    for row in discovery(store, UNIT)["measures"]:
        assert row["reducers"] == []
    # and no legacy-style member vocabulary appears anywhere in the governed response
    for legacy_member in ('"sum"', '"last"', '"count"', '"min"', '"max"'):
        assert legacy_member not in blob


# ══ THE CONTROL THAT BINDS THE CATALOGUE TO REALITY ══════════════════════════════════════════════

def test_every_listed_measure_actually_resolves_through_the_successor_resolver(store):
    """Control: each returned reference is put back through the resolver that serves requests.

    Not a re-implementation of the lookup — the real one, from `columna_platform.request`, against
    the same publication. If discovery ever lists a reference the resolver cannot resolve, the tool
    is promising an ask that would refuse."""
    from columna_core.envelope import parse_statement
    from columna_platform import request as rq
    from columna_platform.serving import open_publication

    artifact = pathlib.Path(store.dir) / UNIT / "governed-publication.json"
    pub, _ = open_publication(str(artifact))

    payload = discovery(store, UNIT)
    levels = "*".join(payload["levels"])
    for row in payload["measures"]:
        stmt = parse_statement(f"SELECT {row['measure']} AT {{{levels}}}")
        resolved = rq.resolve(pub, stmt)
        assert resolved.family.canonical_reference == row["measure"]


def test_every_listed_measure_is_askable_through_the_public_tool(store):
    """Controls 1-2, end to end: the reference discovery advertises serves a would-be `serve` from
    the public pre-flight — the same surface a caller would use next."""
    payload = discovery(store, UNIT)
    levels = "*".join(payload["levels"])
    for row in payload["measures"]:
        wire = check_frame_query(store, UNIT, f"SELECT {row['measure']} AT {{{levels}}}")
        assert wire["outcome"] == "serve", f"{row['measure']} is listed but not askable"


# ══ 6 · THE ANCHOR COMPONENT TOKENS ══════════════════════════════════════════════════════════════

def test_levels_are_the_deduplicated_governed_anchor_component_tokens(store):
    payload = discovery(store, UNIT)
    assert payload["levels"] == ["day", "store"]
    assert payload["anchors"] == [{"universe": "sales", "basis": "events",
                                   "grain": ["day", "store"]}]


def test_the_level_tokens_are_accepted_by_successor_anchor_resolution(store):
    """Control 6. The tokens are not decoration: an `AT {…}` naming exactly them resolves, and a
    token this response does NOT list does not."""
    payload = discovery(store, UNIT)
    good = "*".join(payload["levels"])
    assert check_frame_query(store, UNIT, f"SELECT revenue AT {{{good}}}")["outcome"] == "serve"

    unlisted = check_frame_query(store, UNIT, "SELECT revenue AT {region}")
    assert unlisted["outcome"] == "refuse"


# ══ 5 · FAIL-CLOSED BEHAVIOUR IS UNTOUCHED ═══════════════════════════════════════════════════════

def test_an_unknown_reference_still_refuses_and_is_not_in_the_catalogue(store):
    assert "revenu" not in {m["measure"] for m in discovery(store, UNIT)["measures"]}
    wire = check_frame_query(store, UNIT, "SELECT revenu AT {store*day}")
    assert wire["outcome"] == "refuse"
    assert wire["columns"][0]["no_result"]["reason"] == "want_of_law"


def test_an_unknown_manifold_still_raises_structurally(store):
    from columna_server.tools import ToolInputError
    with pytest.raises(ToolInputError):
        discovery(store, "nope")


# ══ 7-9 · COMPATIBILITY, ISOLATION, INSULATION ═══════════════════════════════════════════════════

def test_the_governed_payload_shape_is_identical_to_the_legacy_one(store):
    """Control 7's other half: same keys, same nesting, same types — one contract, two populations."""
    legacy = discovery(ManifoldStore(str(LEGACY_FIXTURES)), "benchmark")
    governed = discovery(store, UNIT)

    assert set(governed) - {"manifold_version"} == set(legacy) - {"manifold_version"}
    assert governed["contract_version"] == legacy["contract_version"] == "5"
    assert governed["ask_form"] == legacy["ask_form"]
    assert set(governed["measures"][0]) == set(legacy["measures"][0])
    assert set(governed["anchors"][0]) == set(legacy["anchors"][0])
    for key in ("measure", "universe", "description"):
        assert isinstance(governed["measures"][0][key], type(legacy["measures"][0][key]))
    assert isinstance(governed["levels"], list) and isinstance(legacy["levels"], list)


def test_the_legacy_discovery_response_is_unchanged(store):
    """Control 7. The legacy path keeps its reducer/member behaviour exactly."""
    legacy = discovery(ManifoldStore(str(LEGACY_FIXTURES)), "benchmark")
    revenue = next(m for m in legacy["measures"] if m["measure"] == "revenue")
    assert "sum" in revenue["reducers"]              # legacy members, still listed as before
    assert revenue["grain"] and revenue["universe"]
    assert {a["universe"] for a in legacy["anchors"]} == {"transactions", "store_days"}


def test_no_provider_adjudication_or_legacy_model_is_touched(store, monkeypatch):
    """Control 8. The governed answer comes from the publication alone — so every other source is
    made to explode, and the tool still answers."""
    lm = store.get(UNIT)
    assert lm.manifold is None                       # no legacy model exists to consult

    def _boom(*a, **k):
        raise AssertionError("governed discovery reached the execution layer")

    monkeypatch.setattr(type(lm.provider), "published_scope", _boom, raising=False)
    monkeypatch.setattr(type(lm.provider), "operators", _boom, raising=False)
    monkeypatch.setattr(type(lm.provider), "plan", _boom, raising=False)
    monkeypatch.setattr(type(lm.provider), "run", _boom, raising=False)

    assert len(discovery(store, UNIT)["measures"]) == 4


def test_no_physical_realization_identifier_appears(store):
    """Control 9."""
    blob = json.dumps(discovery(store, UNIT))
    for physical in ("sales_lines", "warehouse", "store_id", "sale_date", "amount",
                     "connection", "table", "column", "realized_by"):
        assert physical not in blob


# ══ THE SEMANTIC MISMATCH, RECORDED AS A CONTROL ═════════════════════════════════════════════════

def test_the_governed_target_does_not_become_the_public_description(store):
    """`Family.target` is responsibility C1 and IDENTITY-BEARING — changing it is a SUCCESSION.
    `measures[].description` is DESCRIPTION folklore: additive, non-normative, freely editable.
    Both are prose and that is the whole of their resemblance, so the governed row says nothing
    rather than publishing law in a folklore field.

    The target text is asserted ABSENT so that a later decision to surface it is deliberate."""
    blob = json.dumps(discovery(store, UNIT))
    assert "the revenue recognised at one sale point" not in blob
    assert all(m["description"] == "" for m in discovery(store, UNIT)["measures"])

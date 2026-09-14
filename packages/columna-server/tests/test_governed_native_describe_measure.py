"""`describe_measure`, answered from the governed publication — and THE OMISSION RULE.

Ruled Huayin 2026-09-14:

    True structural emptiness may be represented as empty. A fact belonging to another jurisdiction,
    and not established for this object, must be OMITTED rather than represented by a
    domain-significant empty or default value.

That sentence is the whole design, and this file is where it is enforced in both directions: three
fields are EMPTY because emptiness is true of a governed family, and three are ABSENT because their
defaults would assert something the publication never declared. A test that only checked the empties
would pass on an implementation that published `MCAR` out of nothing.
"""
from __future__ import annotations

import json
import pathlib

import pytest
from columna_server.store import RUNTIME_PLATFORM, ManifoldStore
from columna_server.tools import ToolInputError, describe_measure, discovery

V2_ARTIFACT = (pathlib.Path(__file__).parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
LEGACY_FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "manifolds"
UNIT = "lighthouse"
PRIMITIVE = "revenue"
CONSTRUCTED = "count(revenue@sale_at)"


@pytest.fixture
def store(tmp_path):
    d = tmp_path / UNIT
    d.mkdir()
    (d / "governed-publication.json").write_text(V2_ARTIFACT.read_text(encoding="utf-8"),
                                                 encoding="utf-8")
    return ManifoldStore(str(tmp_path), runtime_selection={UNIT: RUNTIME_PLATFORM})


# ══ 1-2 · IT DESCRIBES, FROM GOVERNED DECLARATIONS ═══════════════════════════════════════════════

@pytest.mark.parametrize("reference", [PRIMITIVE, CONSTRUCTED])
def test_a_governed_family_resolves_and_describes(store, reference):
    got = describe_measure(store, UNIT, reference)
    assert got["measure"] == reference
    assert got["family"]["root"] == reference
    assert got["universe"] == "sales"
    assert got["contract_version"] == "5"
    assert got["manifold_version"] == "1.0.0"


def test_the_v_anchor_comes_from_the_governed_universe_and_anchor_declarations(store):
    """Control 2, by EXACT dict equality — the same strictness the legacy pin uses."""
    assert describe_measure(store, UNIT, PRIMITIVE)["v_anchor"] == {
        "universe": "sales", "grain": ["day", "store"]}


def test_a_declared_alias_resolves_through_the_governed_reader(store, tmp_path):
    """The lookup is `resolve_reference` — the v2 contract's own — not a map rebuilt in the server.
    A declared alias therefore works, and a near-miss does not."""
    import copy

    raw = json.loads(V2_ARTIFACT.read_text(encoding="utf-8"))
    mutated = copy.deepcopy(raw)
    for decl in mutated["logical"]["declarations"]:
        if decl["kind"] == "family" and decl["body"]["canonical_reference"] == PRIMITIVE:
            decl["body"]["aliases"] = ["turnover"]
    (tmp_path / UNIT / "governed-publication.json").write_text(json.dumps(mutated), encoding="utf-8")
    st = ManifoldStore(str(tmp_path), runtime_selection={UNIT: RUNTIME_PLATFORM})

    assert describe_measure(st, UNIT, "turnover")["family"]["root"] == PRIMITIVE
    with pytest.raises(ToolInputError):
        describe_measure(st, UNIT, "turnovers")


# ══ 3-5 · TRUTHFUL EMPTINESS ═════════════════════════════════════════════════════════════════════

def test_the_member_structures_are_empty_because_a_governed_family_has_no_members(store):
    got = describe_measure(store, UNIT, PRIMITIVE)
    assert got["family"]["members"] == []
    assert got["family"]["reducer_kind"] == {}
    assert got["member_anchors"] == {}
    assert got["signatures"] == {}


# ══ 6-8 · ABSENCE, WHERE A DEFAULT WOULD LIE ═════════════════════════════════════════════════════

def test_dtype_is_absent_and_no_substrate_dtype_is_invented(store):
    """Control 6. Governed `value_domain` and execution dtype are different facts; neither
    substitutes for the other, so the field is not emitted at all."""
    got = describe_measure(store, UNIT, PRIMITIVE)
    assert "dtype" not in got
    blob = json.dumps(got)
    for invented in ("Float64", "Decimal", "decimal", "value_domain"):
        assert invented not in blob


def test_m_anchor_is_absent_and_MCAR_appears_nowhere(store):
    """Control 7 — the sharpest one. `mechanism` is DERIVED from an empty M-anchor, so emitting the
    block would publish MISSING-COMPLETELY-AT-RANDOM: a real statistical assertion, manufactured
    from the absence of a legacy field."""
    got = describe_measure(store, UNIT, PRIMITIVE)
    assert "m_anchor" not in got
    blob = json.dumps(got)
    for mechanism in ("MCAR", "MAR", "MNAR"):
        assert mechanism not in blob


def test_provenance_is_omitted_whole_rather_than_standing_empty(store):
    """Control 8. Its only field was the evidence grade, and ratification authority is not an
    evidence grade — so the block goes with it."""
    got = describe_measure(store, UNIT, PRIMITIVE)
    assert "provenance" not in got
    blob = json.dumps(got)
    for grade in ("data_attested", "declared", "inferred", "ratifications", "ratified_by"):
        assert grade not in blob


def test_the_general_omission_rule_is_pinned_in_both_directions(store):
    """THE RULE ITSELF, as one assertion: exactly the three truthful empties are present, and
    exactly the three cross-jurisdiction facts are absent. A single test so the distinction cannot
    erode by halves."""
    got = describe_measure(store, UNIT, PRIMITIVE)
    truthfully_empty = {"family": {"root": PRIMITIVE, "members": [], "reducer_kind": {}},
                        "member_anchors": {}, "signatures": {}}
    for key, value in truthfully_empty.items():
        assert key in got and got[key] == value, f"{key} must be present and empty"
    for absent in ("dtype", "m_anchor", "provenance"):
        assert absent not in got, f"{absent} belongs to a jurisdiction this object does not have"


# ══ 9 · C1 DOES NOT TRAVEL IN A FOLKLORE FIELD ═══════════════════════════════════════════════════

def test_the_target_text_does_not_leak_into_description(store):
    got = describe_measure(store, UNIT, PRIMITIVE)
    assert got["description"] == ""
    assert "the revenue recognised at one sale point" not in json.dumps(got)


# ══ 10-12 · ISOLATION AND INSULATION ═════════════════════════════════════════════════════════════

def test_no_provider_call_and_no_legacy_model_access(store, monkeypatch):
    """Controls 10-11. `operators()` is not refused here — it is never reached, because a governed
    family has no members to look one up for. Every execution-layer entry point is made to explode
    and the tool still answers."""
    lm = store.get(UNIT)
    assert lm.manifold is None

    def _boom(*a, **k):
        raise AssertionError("governed describe_measure reached the execution layer")

    for method in ("operators", "published_scope", "plan", "run", "explain"):
        monkeypatch.setattr(type(lm.provider), method, _boom, raising=False)

    assert describe_measure(store, UNIT, PRIMITIVE)["family"]["root"] == PRIMITIVE


def test_no_physical_realization_identifier_appears(store):
    blob = json.dumps(describe_measure(store, UNIT, PRIMITIVE))
    for physical in ("sales_lines", "warehouse", "store_id", "sale_date", "amount",
                     "connection", "home_table", "realized_by", "pre_expr"):
        assert physical not in blob


# ══ 13 · THE CATALOGUE AND THE DESCRIPTION AGREE ═════════════════════════════════════════════════

def test_every_described_measure_is_resolvable_through_the_successor_resolver(store):
    """Control 13, and the join to #287: everything `discovery` advertises can be described, and
    everything described resolves through the resolver the public request path uses."""
    from columna_core.envelope import parse_statement
    from columna_platform import request as rq
    from columna_platform.serving import open_publication

    pub, _ = open_publication(str(pathlib.Path(store.dir) / UNIT / "governed-publication.json"))
    payload = discovery(store, UNIT)
    levels = "*".join(payload["levels"])

    for row in payload["measures"]:
        described = describe_measure(store, UNIT, row["measure"])
        assert described["family"]["root"] == row["measure"]
        assert described["v_anchor"]["grain"] == row["grain"]
        resolved = rq.resolve(pub, parse_statement(f"SELECT {row['measure']} AT {{{levels}}}"))
        assert resolved.family.canonical_reference == row["measure"]


def test_an_unknown_reference_raises_structurally_listing_what_exists(store):
    with pytest.raises(ToolInputError) as e:
        describe_measure(store, UNIT, "revenu")
    assert "unknown measure 'revenu'" in str(e.value)
    assert PRIMITIVE in str(e.value)


# ══ 14-15 · THE LEGACY RESPONSE IS UNTOUCHED ═════════════════════════════════════════════════════

def test_the_legacy_describe_measure_is_unchanged(store):
    """Control 14. Every field the governed path omits is still present on the legacy path, with its
    legacy meaning — the omission is about a jurisdiction being absent, never about the field."""
    legacy = describe_measure(ManifoldStore(str(LEGACY_FIXTURES)), "benchmark", "level")
    assert {"dtype", "m_anchor", "provenance"} <= set(legacy)
    assert legacy["m_anchor"]["mechanism"] in {"MCAR", "MAR", "MNAR"}
    assert legacy["provenance"]["measure"] in {"data_attested", "declared", "inferred"}
    assert legacy["family"]["members"] and legacy["member_anchors"] and legacy["signatures"]
    assert legacy["v_anchor"] == {"universe": "store_days", "grain": ["day", "store"]}


def test_the_governed_response_is_a_subset_of_the_legacy_key_set(store):
    """Shape comparison: the governed payload adds NOTHING. Every key it emits is a key the legacy
    contract already has — no new field, no renamed field, contract_version untouched."""
    legacy = describe_measure(ManifoldStore(str(LEGACY_FIXTURES)), "benchmark", "level")
    governed = describe_measure(store, UNIT, PRIMITIVE)
    assert set(governed) <= set(legacy) | {"manifold_version"}
    assert set(governed["family"]) == set(legacy["family"])
    assert set(governed["v_anchor"]) == set(legacy["v_anchor"])
    assert set(legacy) - set(governed) == {"dtype", "m_anchor", "provenance"}

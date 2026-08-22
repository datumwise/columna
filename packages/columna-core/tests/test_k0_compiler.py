"""
test_k0_compiler — the Core-P1 K0 acceptance contract.

Follows the testing doctrine ratified at P0.5a closure: **pin the REASON for refusal, not merely
that something refused.** In a fail-closed compiler a test asserting only "it raised" is weak
evidence — another gate can keep it green while the intended invariant regresses. Every refusal test
below names the category it expects, and several assert the category is NOT one of the others.
"""
import copy
import json
import os
import re

import pytest

from columna_core.compiler import (
    CATEGORIES,
    ClosedExecutionImage,
    ExecutionRepresentationGap,
    InputIdentityMismatch,
    K0_REDUCERS,
    LogicalMeaningMissing,
    MappingIncomplete,
    UnsupportedCoreCapability,
    build_receipt,
    compile_k0,
    parse_mapping,
    parse_publication,
    render_receipt,
)
from columna_core.parser import parse_file

# ── the K0-shaped world: measure . member . anchor + one unrestricted universe ────────────────────
PUB = {
    "publication_format_version": "1",
    "ref": {"manifold_id": "retail", "version": "1.3.0"},
    "logical": {"declarations": [
        {"kind": "anchor", "name": "sale_at", "body": {"components": [
            {"name": "store", "type": "text"}, {"name": "day", "type": "date"}]}},
        {"kind": "universe", "name": "sales", "body": {"anchor": "sale_at", "basis": "events"}},
        {"kind": "measure", "name": "revenue",
         "body": {"value_type": "decimal", "root_member": "revenue_sum"}},
        {"kind": "member", "name": "revenue_sum",
         "body": {"measure": "revenue", "anchor": "sale_at", "universe": "sales"}},
        {"kind": "member", "name": "revenue_max",
         "body": {"measure": "revenue", "anchor": "sale_at", "universe": "sales"}},
    ]},
    "authority": {"published_by": "huayin", "published_at": "2026-08-22", "ratifications": {}},
}

_EP = {"connection": "wh", "schema": "public", "table": "sales_lines"}
MAP = {
    "mapping_format_version": "1",
    "publication_ref": {"manifold_id": "retail", "version": "1.3.0"},
    "realizations": [
        {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "store",
         "endpoint": dict(_EP, column="store_id")},
        # Physical names are deliberately UNLIKE the logical ones: if the compiler ever used a
        # coordinate name as a column name, this fixture is what would catch it.
        {"kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "day",
         "endpoint": dict(_EP, column="sale_date")},
        {"kind": "member", "measure_ref": "revenue", "member_ref": "revenue_sum",
         "universe_ref": "sales", "anchor_ref": "sale_at", "root_evaluator": "sum",
         "endpoint": dict(_EP, column="amount")},
        {"kind": "member", "measure_ref": "revenue", "member_ref": "revenue_max",
         "universe_ref": "sales", "anchor_ref": "sale_at", "root_evaluator": "max",
         "endpoint": dict(_EP, column="amount")},
    ],
}


def _compile(pub=None, mapping=None) -> ClosedExecutionImage:
    return compile_k0(parse_publication(pub or PUB), parse_mapping(mapping or MAP))


def _pub(mutate):
    p = copy.deepcopy(PUB)
    mutate(p)
    return p


def _map(mutate):
    m = copy.deepcopy(MAP)
    mutate(m)
    return m


# ── 1. input authority, before any lowering ──────────────────────────────────────────────────────
def test_mapping_for_another_publication_is_an_identity_mismatch():
    bad = _map(lambda m: m["publication_ref"].update(version="1.2.0"))
    with pytest.raises(InputIdentityMismatch) as e:
        _compile(mapping=bad)
    assert "1.2.0" in str(e.value) and "1.3.0" in str(e.value)


def test_identity_is_checked_before_any_lowering_gap():
    """A mapping for the wrong publication AND missing realizations reports the IDENTITY problem.

    Ordering is the claim: identity is an input-authority condition, not a lowering outcome, so it
    must be reached before anything else has a chance to complain."""
    bad = _map(lambda m: (m["publication_ref"].update(version="9.9.9"),
                          m.__setitem__("realizations", [])))
    with pytest.raises(InputIdentityMismatch):
        _compile(mapping=bad)


# ── 2. determinism — the receipt binds BYTES ─────────────────────────────────────────────────────
def test_compiling_twice_is_byte_identical():
    assert _compile().encode() == _compile().encode()


def test_image_carries_no_timestamp_or_run_varying_token():
    text = _compile().text
    assert "2026" not in text and "T00:00" not in text


def test_declaration_order_does_not_change_the_image():
    """Authored order must not reach the bytes: the compiler sorts, so a reordered publication
    compiles to the same image and therefore the same digest."""
    shuffled = _pub(lambda p: p["logical"]["declarations"].reverse())
    assert _compile(pub=shuffled).encode() == _compile().encode()


# ── 3 & 4. round-trip and identity emission ──────────────────────────────────────────────────────
def test_emitted_image_parses_and_checks_clean(tmp_path):
    path = tmp_path / "manifold.cml"
    path.write_text(_compile().text, encoding="utf-8")
    m = parse_file(str(path))
    assert m.check() == []


def test_source_manifold_equals_the_artifact_ref_exactly(tmp_path):
    path = tmp_path / "manifold.cml"
    path.write_text(_compile().text, encoding="utf-8")
    m = parse_file(str(path))
    assert (m.source_manifold_id, m.source_manifold_version) == ("retail", "1.3.0")


def test_the_family_carries_every_declared_member(tmp_path):
    path = tmp_path / "manifold.cml"
    path.write_text(_compile().text, encoding="utf-8")
    m = parse_file(str(path))
    assert sorted(m.measures["revenue"].family) == ["max", "sum"]
    assert m.measures["revenue"].logical_type == "Float64"


def test_universe_is_emitted_unrestricted_with_its_basis(tmp_path):
    path = tmp_path / "manifold.cml"
    path.write_text(_compile().text, encoding="utf-8")
    m = parse_file(str(path))
    u = m.universes["sales"]
    assert u.predicate is None, "K0 emits no WHERE"
    assert u.basis == "events"
    assert u.base_dimensions == frozenset({"store", "day"})


def test_on_universe_is_always_explicit_never_the_single_universe_sugar():
    assert "ON sales" in _compile().text


def test_the_value_expression_is_the_bare_column(tmp_path):
    """Regression pin with a scar behind it.

    The first emitter wrote `VALUE <col> TYPE <dtype>`. The parser's VALUE match is lazy and stops
    only at M_ANCHOR / FAMILY / end — never at TYPE — so the pre-expression became
    `amount TYPE Float64`. That document PARSED clean and `check()`ed clean, and only failed at the
    connector as `sum(amount TYPE Float64)`. Well-formed is not the same as executable, so this pins
    the pre-expression itself rather than trusting a green `check()`."""
    path = tmp_path / "manifold.cml"
    path.write_text(_compile().text, encoding="utf-8")
    m = parse_file(str(path))
    assert m.measures["revenue"].pre_expr == "amount"
    assert m.measures["revenue"].home_table == "sales_lines"


def test_levels_realize_the_mapped_column_not_the_coordinate_name(tmp_path):
    """The coordinate is `day`; the column is `sale_date`. A compiler that quietly used the logical
    name as a physical one would still produce a parseable image — and a wrong one."""
    path = tmp_path / "manifold.cml"
    path.write_text(_compile().text, encoding="utf-8")
    m = parse_file(str(path))
    assert m.levels["day"].realized_by == "sale_date"
    assert m.levels["store"].realized_by == "store_id"


# ── 5. the refusal taxonomy — each category, by name ─────────────────────────────────────────────
def test_measure_without_a_member_is_a_logical_meaning_gap():
    bad = _pub(lambda p: p["logical"]["declarations"].__setitem__(
        slice(None), [d for d in p["logical"]["declarations"] if d["kind"] != "member"]))
    with pytest.raises(LogicalMeaningMissing):
        _compile(pub=bad)


def test_placeholder_value_type_refuses_rather_than_defaulting():
    bad = _pub(lambda p: p["logical"]["declarations"][2]["body"].update(value_type="unknown"))
    with pytest.raises(LogicalMeaningMissing) as e:
        _compile(pub=bad)
    assert "placeholder" in str(e.value)


def test_unrealized_anchor_component_is_a_mapping_gap():
    bad = _map(lambda m: m["realizations"].pop(0))
    with pytest.raises(MappingIncomplete) as e:
        _compile(mapping=bad)
    assert "exactly one" in str(e.value)


def test_duplicate_anchor_component_realization_is_a_mapping_gap():
    dup = _map(lambda m: m["realizations"].append(copy.deepcopy(m["realizations"][0])))
    with pytest.raises(MappingIncomplete) as e:
        _compile(mapping=dup)
    assert "twice" in str(e.value)


def test_unknown_anchor_component_is_a_mapping_gap():
    bad = _map(lambda m: m["realizations"][0].update(component_name="not_a_component"))
    with pytest.raises(MappingIncomplete):
        _compile(mapping=bad)


def test_member_without_a_realization_is_a_mapping_gap():
    bad = _map(lambda m: m["realizations"].pop())
    with pytest.raises(MappingIncomplete) as e:
        _compile(mapping=bad)
    assert "member" in str(e.value)


def test_a_universe_restriction_refuses_as_a_capability_gap():
    bad = _pub(lambda p: p["logical"]["declarations"][1]["body"].update(
        restriction={"op": "=", "ref": "store", "value": "eu"}))
    with pytest.raises(UnsupportedCoreCapability) as e:
        _compile(pub=bad)
    assert "restriction" in str(e.value)


def test_value_type_outside_the_frozen_map_is_a_representation_gap():
    bad = _pub(lambda p: p["logical"]["declarations"][2]["body"].update(value_type="quaternion"))
    with pytest.raises(ExecutionRepresentationGap) as e:
        _compile(pub=bad)
    assert "will not guess" in str(e.value)


def test_members_split_across_two_tables_is_a_representation_gap():
    bad = _map(lambda m: m["realizations"][3]["endpoint"].update(table="other_table"))
    with pytest.raises(ExecutionRepresentationGap) as e:
        _compile(mapping=bad)
    assert "one home table" in str(e.value)


def test_every_category_is_enumerated():
    """A category that exists but is not enumerated is a condition that vanishes from a report
    rather than surfacing in it — the same reason the server pins its LoadCondition codes."""
    for exc in (InputIdentityMismatch, LogicalMeaningMissing, MappingIncomplete,
                UnsupportedCoreCapability, ExecutionRepresentationGap):
        assert exc.category in CATEGORIES
    assert len(CATEGORIES) == 5


# ── the reducer allow-list ───────────────────────────────────────────────────────────────────────
def test_the_allow_list_is_exactly_the_ratified_four():
    assert K0_REDUCERS == frozenset({"sum", "count", "min", "max"})


@pytest.mark.parametrize("agg", sorted({"sum", "count", "min", "max"}))
def test_every_allowed_reducer_compiles_and_checks_clean(agg, tmp_path):
    mapping = _map(lambda m: (m["realizations"].pop(),
                              m["realizations"][-1].update(root_evaluator=agg)))
    pub = _pub(lambda p: p["logical"]["declarations"].pop())
    path = tmp_path / "manifold.cml"
    path.write_text(_compile(pub=pub, mapping=mapping).text, encoding="utf-8")
    assert parse_file(str(path)).check() == []


@pytest.mark.parametrize("agg,needle", [
    ("mean", "refuses it at execution"),
    ("avg", "alias"),
    ("median", "deferred"),
    ("mode", "deferred"),
    ("last", "ORDER"),
    ("first", "ORDER"),
    ("distinct", "sketch"),
    ("percentile", "does not register it"),
])
def test_excluded_reducers_refuse_with_a_stated_reason(agg, needle):
    """Nothing is excluded merely for tidiness — each refusal says WHY, in its own words."""
    bad = _map(lambda m: m["realizations"][2].update(root_evaluator=agg))
    with pytest.raises(UnsupportedCoreCapability) as e:
        _compile(mapping=bad)
    assert needle in str(e.value)


def test_a_reducer_the_measure_type_rejects_refuses_before_emission():
    """Self-verification against Core's own signature law: refuse rather than emit a document whose
    own check() would reject it. `sum` does not accept a text measure."""
    pub = _pub(lambda p: (p["logical"]["declarations"][2]["body"].update(value_type="text"),
                          p["logical"]["declarations"].pop()))
    mapping = _map(lambda m: m["realizations"].pop())
    with pytest.raises(UnsupportedCoreCapability) as e:
        _compile(pub=pub, mapping=mapping)
    assert "does not accept" in str(e.value)


# ── 6. scope refusals are REFUSALS, never silent omissions ───────────────────────────────────────
@pytest.mark.parametrize("kind,body,exc", [
    ("hierarchy", {"levels": [{"child": "store", "parent": "region"}], "direction": "up"},
     UnsupportedCoreCapability),
    ("relationship", {"from": "a", "to": "b", "functionality": "many_to_one", "disposition": "x"},
     UnsupportedCoreCapability),
    ("attribute", {"of": "store", "value_type": "text"}, UnsupportedCoreCapability),
    ("boundary", {"measure": "revenue", "forbidden": ["day"], "across": ["store"]},
     ExecutionRepresentationGap),
    ("crosswalk", {"from_coords": ["a"], "to_coords": ["b"], "correspondence": "?"},
     LogicalMeaningMissing),
])
def test_out_of_scope_construct_refuses_and_is_never_silently_dropped(kind, body, exc):
    bad = _pub(lambda p: p["logical"]["declarations"].append(
        {"kind": kind, "name": f"a_{kind}", "body": body}))
    with pytest.raises(exc) as e:
        _compile(pub=bad)
    assert kind in str(e.value)


def test_an_unknown_realization_kind_refuses_rather_than_being_ignored():
    bad = _map(lambda m: m["realizations"].append({"kind": "hierarchy_edge", "x": 1}))
    with pytest.raises(MappingIncomplete) as e:
        _compile(mapping=bad)
    assert "unknown realization kind" in str(e.value)


# ── 9. the blast wall ────────────────────────────────────────────────────────────────────────────
def test_no_physical_identifier_reaches_the_publication():
    """The artifact is physical-clean and stays that way: compiling must not write back into it.

    Matched on WORD BOUNDARIES, not substrings: `public` (a schema) legitimately occurs inside
    `publication_format_version`, and a substring test would either fail spuriously or have to be
    weakened until it proved nothing. Every physical value in the mapping is checked, so the test
    cannot rot as the fixture grows a field."""
    before = json.dumps(PUB, sort_keys=True)
    _compile()
    assert json.dumps(PUB, sort_keys=True) == before, "compiling must not mutate the artifact"

    physical = set()
    for r in MAP["realizations"]:
        physical.update(str(v) for v in r["endpoint"].values() if v)
    assert physical, "fixture must actually carry physical facts for this test to mean anything"
    for token in physical:
        assert not re.search(rf"\b{re.escape(token)}\b", before), (
            f"physical identifier {token!r} leaked into the governed publication")


def test_compile_opens_no_file_at_all(monkeypatch):
    """The compiler's only inputs are the two objects it is handed. It cannot repair a missing fact
    from evidence, profile, Studio state or a dead-end YAML, because it reaches no filesystem."""
    import builtins

    def _forbidden(*a, **k):
        raise AssertionError("compile_k0 opened a file; its only inputs are its two arguments")

    monkeypatch.setattr(builtins, "open", _forbidden)
    assert _compile().text


# ── the receipt producer ─────────────────────────────────────────────────────────────────────────
def test_receipt_binds_this_publication_to_this_image():
    img = _compile()
    pub_bytes = json.dumps(PUB, sort_keys=True, separators=(",", ":")).encode()
    r = build_receipt(manifold_id=img.manifold_id, version=img.version,
                      publication_bytes=pub_bytes, image_bytes=img.encode(),
                      compiler_name="columna-core-p1-k0", compiler_version="0.1.0")
    assert r["publication_ref"] == {"manifold_id": "retail", "version": "1.3.0"}
    assert r["publication_digest"].startswith("sha256:")
    assert r["image_digest"].startswith("sha256:")
    assert len(r["image_digest"]) == len("sha256:") + 64
    assert json.loads(render_receipt(r)) == r


def test_binding_ignores_provenance_and_timestamp():
    """Two receipts from identical inputs bind identically however and whenever they were written."""
    img = _compile()
    pb = b"{}"
    common = dict(manifold_id=img.manifold_id, version=img.version, publication_bytes=pb,
                  image_bytes=img.encode(), compiler_name="c", compiler_version="1")
    a = build_receipt(**common, established_at="2026-08-22T00:00:00Z", mapping_provenance={"rev": 1})
    b = build_receipt(**common, established_at="2027-01-01T00:00:00Z", mapping_provenance={"rev": 9})
    binding = ("publication_ref", "publication_digest", "image_digest")
    assert {k: a[k] for k in binding} == {k: b[k] for k in binding}
    assert a["established_at"] != b["established_at"]


# ── the dependency direction, pinned structurally ────────────────────────────────────────────────
def test_the_compiler_never_imports_the_server():
    """`columna-server` depends on `columna-core`, never the reverse.

    The receipt schema is a frozen contract implemented independently at both ends — the same shape
    as the publication artifact, whose producer and consumer also share no code. This pins the
    direction the way the server pins its own (`"manifold_agent" not in sys.modules`), so a
    convenience import cannot quietly invert it."""
    import subprocess
    import sys

    code = ("import sys; import columna_core.compiler as c; "
            "assert c.compile_k0; "
            "bad=[m for m in sys.modules if m.startswith('columna_server')]; "
            "print(bad)")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                         env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)})
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "[]", f"compiler pulled in {out.stdout.strip()}"

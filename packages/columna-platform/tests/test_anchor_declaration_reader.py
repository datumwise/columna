"""One governed declaration, one parser, one malformation policy — and three views that stay distinct.

WHAT WAS CONSOLIDATED, AND WHAT DELIBERATELY WAS NOT. Three functions parsed the same `anchor`
declaration out of the governed logical projection:

    movement._declared_components   ordered names   REFUSED a non-list `components`
    serving.declared_components     name -> type    returned {} silently
    request._declared_anchors       name sets       returned an empty set silently

The three VIEWS answer three different questions and their shapes are right to differ — a movement
licence needs identity and DECLARATION ORDER, admission needs the governed TYPE, request resolution
needs a set to match an ask against. What was wrong was three PARSERS: "what counts as a malformed
anchor declaration" had three answers, and the strict one was reachable from only one of three doors.

So the views are still three functions with three return types, and `anchors.declared_coordinates` is
the only thing that reads `decl.body["components"]`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.governed.publication import parse_publication

from columna_platform import anchors, movement, request as _request, serving
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.refusals import WantOfLaw
from columna_platform.source import MaterialBinding

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fixtures"))
import lighthouse_material as M                                                # noqa: E402

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
PUBLICATION = (Path(__file__).resolve().parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
MAPPING = FIXTURES / "proof_a" / "private-core-mapping-v2.json"
ASK = "SELECT revenue AT {store*day}"


def _pub(mutate=None):
    d = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    return parse_publication(d)


def _anchor_body(d, name="sale_at"):
    for decl in d["logical"]["declarations"]:
        if decl["kind"] == "anchor" and decl["name"] == name:
            return decl["body"]
    raise KeyError(name)


# ══ the three views, and that they remain three ═════════════════════════════════════════════════

def test_the_canonical_read_carries_name_and_type_in_declaration_order():
    got = anchors.declared_coordinates(_pub(), "sale_at")
    assert [(c.name, c.governed_type) for c in got] == [("store", "text"), ("day", "date")]


def test_declaration_order_is_preserved_and_is_not_sorted():
    """ORDER IS LOAD-BEARING and only here. `store, day` is declaration order; sorted order is
    `day, store`, so a reader that sorted would be visible in this assertion — and, one step on, in
    the licence description a human reads."""
    assert anchors.declared_coordinate_names(_pub(), "sale_at") == ("store", "day")
    assert anchors.declared_coordinate_names(_pub(), "sale_at") != ("day", "store")


def test_the_three_views_have_three_shapes_and_are_not_merged():
    pub = _pub()
    assert isinstance(anchors.declared_coordinate_names(pub, "sale_at"), tuple)
    assert isinstance(anchors.declared_coordinate_types(pub, "sale_at"), dict)
    assert isinstance(anchors.declared_anchor_names(pub)["sale_at"], frozenset)


def test_movement_and_admission_observe_the_same_declaration():
    """THE POINT OF THE CONSOLIDATION, as one assertion: two views, one underlying read."""
    pub = _pub()
    names = movement._declared_components(pub, "sale_at")
    types = serving.declared_components(pub, "sale_at")
    sets = _request._declared_anchors(pub)["sale_at"]
    assert names == tuple(types) == tuple(c.name for c in anchors.declared_coordinates(pub, "sale_at"))
    assert frozenset(names) == sets
    assert types == {"store": "text", "day": "date"}


def test_admission_still_receives_the_governed_coordinate_types():
    """OF-48's repair must survive the consolidation — the type is what CHECK 4a reads."""
    assert serving.declared_components(_pub(), "sale_at") == {"store": "text", "day": "date"}


def test_only_one_module_reads_the_components_key():
    """The structural guarantee, asserted against the source rather than trusted.

    A fourth consumer that parsed the declaration again would reintroduce a fourth malformation
    policy, which is the condition this module exists to end."""
    src = Path(anchors.__file__).parent
    readers = [p.name for p in sorted(src.glob("*.py"))
               if '["components"]' in p.read_text(encoding="utf-8")
               or '.get("components")' in p.read_text(encoding="utf-8")]
    assert readers == ["anchors.py"], readers


# ══ one malformation policy, at the reading boundary ════════════════════════════════════════════

@pytest.mark.parametrize("label,mutate,match", [
    ("components missing",
     lambda d: _anchor_body(d).pop("components"), "declares no component list"),
    ("components not a list",
     lambda d: _anchor_body(d).__setitem__("components", "store,day"), "not a list"),
    ("components is a dict",
     lambda d: _anchor_body(d).__setitem__("components", {"store": "text"}), "not a list"),
    ("a component is not a declaration",
     lambda d: _anchor_body(d).__setitem__("components", ["store", "day"]), "not a declaration"),
    ("empty coordinate name",
     lambda d: _anchor_body(d)["components"].append({"name": "", "type": "text"}),
     "no non-empty name"),
    ("whitespace coordinate name",
     lambda d: _anchor_body(d)["components"].append({"name": "   ", "type": "text"}),
     "no non-empty name"),
    ("missing coordinate name",
     lambda d: _anchor_body(d)["components"].append({"type": "text"}), "no non-empty name"),
    ("duplicate coordinate name",
     lambda d: _anchor_body(d)["components"].append({"name": "store", "type": "text"}),
     "more than once"),
])
def test_a_malformed_declaration_refuses_as_a_want_of_law(label, mutate, match):
    """WANT OF LAW, NOT WANT OF STATE. A publication whose anchor declaration cannot be read has not
    established the analytical point its families are constituted at; re-materializing supplies
    nothing, so it must never reach a caller as a refusal blaming the carrier."""
    with pytest.raises(WantOfLaw, match=match):
        anchors.declared_coordinates(_pub(mutate), "sale_at")


def test_an_undeclared_anchor_refuses():
    with pytest.raises(WantOfLaw, match="declares no anchor"):
        anchors.declared_coordinates(_pub(), "no_such_anchor")


@pytest.mark.parametrize("view", [
    anchors.declared_coordinate_names,
    anchors.declared_coordinate_types,
])
def test_every_derived_view_inherits_the_policy(view):
    """The malformation is judged ONCE. Before the consolidation this same input produced a refusal
    through one door and a silent empty value through the other two."""
    with pytest.raises(WantOfLaw, match="declares no component list"):
        view(_pub(lambda d: _anchor_body(d).pop("components")), "sale_at")


def test_the_request_view_inherits_it_too_and_validates_every_anchor():
    """WIDENED DELIBERATELY. Request resolution matches an ask against ALL declared anchors, so it
    reads all of them; a publication carrying one malformed anchor declaration is malformed
    whichever anchor was asked for. Validating only the matching one would make the malformation
    policy depend on the question."""
    with pytest.raises(WantOfLaw, match="declares no component list"):
        anchors.declared_anchor_names(_pub(lambda d: _anchor_body(d).pop("components")))


def test_the_refusal_no_longer_depends_on_request_resolution_running_first():
    """Before the consolidation a malformed declaration reached the wire as `want_of_law` — the right
    jurisdiction, but only because request resolution happened to run before anything that cared.
    That was luck about ordering. Asserted at the reading boundary AND at the wire."""
    with pytest.raises(WantOfLaw):
        anchors.declared_coordinates(_pub(lambda d: _anchor_body(d).pop("components")), "sale_at")


def test_a_malformed_declaration_still_reaches_the_wire_in_the_governed_jurisdiction(tmp_path):
    d = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    _anchor_body(d).pop("components")
    pub_path = tmp_path / "pub.json"
    pub_path.write_text(json.dumps(d), encoding="utf-8")
    provider = PlatformExecutionProvider.from_artifact(
        str(pub_path), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=str(MAPPING), sources=M.bindings()))
    wire = wire_frame(provider.run(parse_statement(ASK)), universe=None, executed=True)
    nr = wire["columns"][0]["no_result"]
    assert nr["reason"] == "want_of_law"
    assert nr["reason"] not in ("want_of_state", "unsupported")
    assert [a["token"] for a in (nr.get("alternatives") or [])] == []


# ══ the transcripts that must not move ══════════════════════════════════════════════════════════

def test_the_licence_description_still_renders_declaration_order(tmp_path):
    """DECLARATION ORDER SURVIVES INTO EVIDENCE A HUMAN READS. `sale_at(store*day)`, not
    `sale_at(day*store)` — the string a licence describes itself with, and the one recorded in a
    moved state's standing."""
    lic = movement.project(_pub(), source_anchor="sale_at", target_anchor="store",
                           target_components=("store",), law="SUM")
    assert lic.source_components == ("store", "day")
    assert lic.describe() == "sale_at(store*day) -> store(store) under SUM [positive]"


def test_the_material_execution_transcript_is_unchanged(tmp_path):
    """The positive path, byte for byte on the facts that matter."""
    provider = PlatformExecutionProvider.from_artifact(
        str(PUBLICATION), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=str(MAPPING), sources=M.bindings()))
    wire = wire_frame(provider.run(parse_statement(ASK)), universe=None, executed=True)
    assert wire["outcome"] == "serve"
    assert wire["columns"][0]["status"] == "served"
    assert wire["frame"]["anchor"] == ["sale_at"]
    rows = wire["columns"][0]["values"]
    assert {(r["store"], str(r["day"]), str(r["value"])) for r in rows} == {
        ("east", "2026-01-01", "10.0000"), ("east", "2026-01-02", "20.0000"),
        ("west", "2026-01-01", "1.2345"), ("west", "2026-01-02", "3.7037")}

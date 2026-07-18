"""
test_case_demo_bcd.py — Cascadia case-demo increment 1(b)(c)(d).

(b) DESCRIPTION strings (`-- "text"`) — folklore that flows to describe (LOGICAL side of the wall).
(c) logical ATTRibutes (`store.opened`) legal in a universe predicate (OF-9), rendered logically.
(d) the TWO-ARTIFACT projection — the purely-logical spec and the many-to-one physical→logical map
    with its REJECT rows — and the WALL between them: rejects and physical identifiers live ONLY on
    the map, NEVER in the logical spec (the ruling's wall-correction).
"""
import os
import json
import pytest

from columna_core.parser import parse_file, parse_manifold, ParseError
from columna_core import (logical_spec, physical_map, no_physical_leak,
                          describe_universe, describe_assert, describe_hierarchy, describe_derived,
                          render_predicate_logical)

_FIX = os.path.join(os.path.dirname(__file__), "fixtures", "cascadia_slice.cml")


@pytest.fixture(scope="module")
def m():
    return parse_file(_FIX)


# ── (b) DESCRIPTION strings ────────────────────────────────────────────────────────────────────────
def test_descriptions_parse_onto_every_declaration_kind(m):
    assert m.measures["revenue"].description == "sale amount, summed"
    assert m.measures["units_returned"].description.startswith("units returned; nulls predate")
    assert m.measures["stock"].family["sum"].description == "stock summed across time doesn't reconcile"
    assert m.measures["stock"].family["last"].description == "position = the latest snapshot"
    assert m.derived["return_rate"].description.startswith("returned units over sold units")
    assert m.universes["inventory"].description == "the daily stock snapshot"
    assert m.levels["store"].description == "a retail location"
    inv = next(a for a in m.asserts if a.name == "returns_bounded")
    assert inv.description.startswith("the team's data contract")
    cal = next(h for h in m.hierarchies if h.lineage == "calendar")
    assert cal.description == "the reporting calendar"


def test_descriptions_flow_to_describe(m):
    du = describe_universe(m.universes["inventory"], None)
    assert du["description"] == "the daily stock snapshot"
    dd = describe_derived(m, "return_rate")
    assert dd["description"].startswith("returned units over sold units")
    dh = describe_hierarchy(next(h for h in m.hierarchies if h.lineage == "calendar"))
    assert dh["description"] == "the reporting calendar"
    da = describe_assert(next(a for a in m.asserts if a.name == "returns_bounded"))
    assert da["description"].startswith("the team's data contract")


# ── (c) logical attributes in a predicate (OF-9) ─────────────────────────────────────────────────────
def test_logical_attribute_is_declared_and_used_in_a_predicate(m):
    assert m.levels["store"].attributes == (("opened", "stores.opened_date"),)
    # the predicate references the LOGICAL attribute, not the physical binding
    ref = m.universes["inventory"].predicate.comparisons[0].right
    assert (ref.table, ref.column) == ("store", "opened")


def test_predicate_renders_the_logical_attribute_not_the_physical_binding(m):
    rendered = render_predicate_logical(m.universes["inventory"].predicate, frozenset(m.levels))
    assert rendered == "day >= store.opened"          # OF-9: the declared logical name, with qualifier
    assert "opened_date" not in rendered and "stores." not in rendered   # the physical binding never crosses


def test_undeclared_attribute_on_a_declared_level_is_rejected():
    bad = """MANIFOLD b VERSION 1
LEVEL store = store_id BASE ATTR opened = stores.opened_date
LEVEL day = day BASE
UNIVERSE inv = store * day WHERE day >= store.nonesuch BASIS spine
MEASURE x ON inv FROM t AS sum(v)"""
    with pytest.raises(ParseError) as ei:
        parse_manifold(bad)
    assert "undeclared attribute 'store.nonesuch'" in str(ei.value)


def test_unmigrated_physical_residue_is_still_allowed():
    # a dotted head that is NOT a declared level is a pre-OF-9 physical residue — allowed, not an attr claim
    ok = """MANIFOLD b VERSION 1
LEVEL store = store_id BASE
LEVEL day = day BASE
UNIVERSE inv = store * day WHERE day >= stores.opened_date BASIS spine
MEASURE x ON inv FROM t AS sum(v)"""
    mm = parse_manifold(ok)          # parses clean
    assert mm.universes["inv"].predicate is not None


# ── (d) the two-artifact projection + the wall ───────────────────────────────────────────────────────
def test_physical_map_resolves_many_to_one_with_reasoned_rejects(m):
    rows = {r["logical"]: r for r in physical_map(m)}
    # region carries its TWO distinct-reason rejects (the ruling's explicit case)
    reg = rows["region"]
    assert reg["binds_to"] == "stores.region"
    reasons = {p: r for p, r in reg["rejects"]}
    assert reasons["transactions.customer_region"] == "denormalized copy"
    assert reasons["customers.region"] == "the customer's region, not the store's"
    # the inventory universe carries the eom fossil note
    assert rows["inventory"]["rejects"] == [["eom_inventory", "name is a fossil — grain is daily"]]
    # the stale summaries are rejected off the measures
    assert rows["revenue"]["rejects"] == [["daily_revenue_summary.revenue", "stale"]]
    assert rows["revenue"]["binds_to"] == "sum(amount)"
    assert rows["orders"]["binds_to"] == "count(*)"
    assert rows["buyers"]["binds_to"] == "distinct(customer_id)"
    # the logical attribute has its physical binding on the map
    assert rows["store.opened"]["binds_to"] == "stores.opened_date"


def test_logical_spec_is_purely_logical_no_reject_no_physical(m):
    # the WALL (the ruling's wall-correction): rejects and physical identifiers live ONLY on the map.
    assert no_physical_leak(m) == []
    blob = json.dumps(logical_spec(m))
    # no reject reason and no rejected physical incarnation appears in the logical spec
    for phys in ("daily_revenue_summary", "customer_region", "eom_inventory", "monthly_store_inventory",
                 "opened_date", "stores.region"):
        assert phys not in blob, f"physical/reject token {phys!r} leaked into the logical spec"


def test_logical_spec_carries_meaning_and_folklore(m):
    ls = logical_spec(m)
    assert ls["manifold"] == "cascadia_slice"
    revenue = next(x for x in ls["measures"] if x["name"] == "revenue")
    assert revenue["description"] == "sale amount, summed"
    stock = next(x for x in ls["measures"] if x["name"] == "stock")
    assert stock["members"]["sum"] == "stock summed across time doesn't reconcile"
    # levels expose logical attribute NAMES only (no physical binding)
    store = next(x for x in ls["levels"] if x["level"] == "store")
    assert store["attributes"] == ["opened"]


def test_every_bound_logical_name_appears_on_the_map(m):
    mapped = {r["logical"] for r in physical_map(m)}
    for name in m.measures:
        assert name in mapped
    for name in m.universes:
        assert name in mapped

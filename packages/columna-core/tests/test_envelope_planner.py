"""
test_envelope_planner.py — the FrameQL ENVELOPE assembly (WP-FrameQL increment 2).

Exercises the planner's `run_statement` over the fixture Manifold: multi-series juxtaposition, the §4
naming laws (AS / mechanical default / collisions REFUSED / WITH), the §5 clause-reference law
(HAVING/ORDER BY/PER reference the frame's own columns), WHERE pre-reduction, and LIMIT n PER {dims}.
The engine stays per-column and envelope-blind — this is planner behavior. Naming/clause-reference
violations ride the existing `frameql_syntax` channel (FrameQLSyntaxError).
"""
import pytest

from columna_core.envelope import parse_statement
from columna_core.disclosure_wire import wire_frame
from columna_core.frameql import FrameQLSyntaxError


def _run(server, q):
    return server.planner.run_statement(parse_statement(q))


def _wire(server, q):
    return wire_frame(_run(server, q))


# --- multi-series juxtaposition + serve -----------------------------------------------------------
def test_single_series_serves(fixture_server):
    w = _wire(fixture_server, "SELECT revenue AT {region}")
    assert w["outcome"] == "serve"
    assert [c["name"] for c in w["columns"]] == ["revenue"]


def test_multi_series_juxtaposition(fixture_server):
    fr = _run(fixture_server, "SELECT revenue, orders AT {region}")
    assert [c.name for c in fr.columns] == ["revenue", "orders"]
    assert set(["revenue", "orders"]).issubset(set(fr.data.columns))


# --- §4 naming laws -------------------------------------------------------------------------------
def test_as_alias_names_the_column(fixture_server):
    fr = _run(fixture_server, "SELECT revenue AS gross AT {region}")
    assert fr.columns[0].name == "gross" and "gross" in fr.data.columns


def test_reduction_column_keyed_by_canonical_expression(fixture_server):
    # WP-NAME-1 (0.14.0): an unaliased reduction is keyed by its CANONICAL EXPRESSION, not a
    # mechanical `avg_aov` default — no invented name. The input anchor is now VISIBLE in the key.
    fr = _run(fixture_server, "SELECT avg(aov @ {day}) AT {cal.month}")
    assert fr.columns[0].name == "avg(aov @ {day})"


def test_bare_measure_names_itself(fixture_server):
    assert _run(fixture_server, "SELECT revenue AT {region}").columns[0].name == "revenue"


def test_member_access_key_is_verbatim_dotted(fixture_server):
    # WP-NAME-1 (0.14.0): `level.sum` keys as `level.sum`, verbatim — the dot-to-underscore mangle
    # (`level_sum`) was itself an invention and retires with the mechanical default.
    fr = _run(fixture_server, "SELECT level.sum AT {store}")
    assert fr.columns[0].name == "level.sum"


def test_collision_refused_not_suffixed(fixture_server):
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue AS x, orders AS x AT {region}")
    assert "distinct" in str(ei.value) and "x" in str(ei.value)


def test_column_vs_anchor_name_collision_refused(fixture_server):
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue AS region AT {region}")
    assert "anchor dimension" in str(ei.value)


def test_unaliased_complex_expr_refused(fixture_server):
    # §4: no name is invented for an arithmetic expression — it must carry an AS
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue / orders AT {region}")
    assert "AS" in str(ei.value)


def test_with_binding_substitutes(fixture_server):
    a = _run(fixture_server, "WITH t = revenue SELECT t AS gross AT {region}").data.sort("region")["gross"].to_list()
    b = _run(fixture_server, "SELECT revenue AS gross AT {region}").data.sort("region")["gross"].to_list()
    assert a == pytest.approx(b)


# --- §5 clause-reference law ----------------------------------------------------------------------
def test_order_by_frame_column(fixture_server):
    fr = _run(fixture_server, "SELECT revenue AT {store} ORDER BY revenue DESC")
    vals = fr.data["revenue"].to_list()
    assert vals == sorted(vals, reverse=True)


def test_order_by_nonframe_column_refused(fixture_server):
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue AT {region} ORDER BY orders DESC")
    assert "not a column of the frame" in str(ei.value)


def test_having_by_name_filters(fixture_server):
    full = _run(fixture_server, "SELECT revenue AS gross AT {store}")
    thresh = sorted(full.data["gross"].to_list())[len(full.data) // 2]
    filt = _run(fixture_server, f"SELECT revenue AS gross AT {{store}} HAVING gross > {thresh}")
    assert len(filt.data) < len(full.data)
    assert all(v > thresh for v in filt.data["gross"].to_list())


def test_having_nonframe_column_refused(fixture_server):
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue AS gross AT {region} HAVING orders > 5")
    assert "not a column of the frame" in str(ei.value)


# --- LIMIT n PER {dims} ---------------------------------------------------------------------------
def test_limit_bare(fixture_server):
    fr = _run(fixture_server, "SELECT revenue AT {store} ORDER BY revenue DESC LIMIT 3")
    assert len(fr.data) == 3


def test_limit_per_anchor_coordinate(fixture_server):
    # top product per region — PER {region} ⊆ ORDER BY (region leads for group contiguity)
    fr = _run(fixture_server, "SELECT revenue AT {product*region} ORDER BY region, revenue DESC LIMIT 1 PER {region}")
    assert len(fr.data) == fr.data["region"].n_unique()


def test_per_alias_refused(fixture_server):
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue AS r AT {product*region} ORDER BY r DESC LIMIT 1 PER {r}")
    assert "ANCHOR coordinates only" in str(ei.value)


def test_per_nonanchor_refused(fixture_server):
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue AT {product*region} ORDER BY revenue DESC LIMIT 1 PER {customer}")
    assert "not an anchor coordinate" in str(ei.value)


def test_per_not_in_order_by_refused(fixture_server):
    # PER ⊆ ORDER BY (flag 3, conjoined law): region is an anchor coord but NOT an ORDER BY key -> refuse
    with pytest.raises(FrameQLSyntaxError) as ei:
        _run(fixture_server, "SELECT revenue AT {product*region} ORDER BY revenue DESC LIMIT 1 PER {region}")
    assert "not in ORDER BY" in str(ei.value) and "add" in str(ei.value)


# --- WHERE pre-reduction (pass-through plumbing) --------------------------------------------------
def test_where_pre_reduction_runs(fixture_server):
    # WHERE binds pre-reduction via the existing engine plumbing; the frame still serves, and the
    # filter reaches the fetch (a date bound over the `day` base dimension).
    full = _run(fixture_server, "SELECT revenue AS r AT {store}")
    filt = _run(fixture_server, "SELECT revenue AS r AT {store} WHERE day >= '2024-06-01'")
    assert wire_frame(filt)["outcome"] in ("serve", "disclose")
    # a real pre-reduction filter: the bounded revenue is ≤ the unbounded, store by store
    fmap = dict(zip(full.data["store"], full.data["r"]))
    for st, v in zip(filt.data["store"], filt.data["r"]):
        assert v <= fmap[st] + 1e-9


def test_where_unreachable_refuses(fixture_server):
    # filter_unreachable: `level` lives in store_days; `customer` is transactions-only, so the WHERE
    # dimension cannot reach the series' input anchor -> a per-series refusal, adjudicated before the
    # engine is invoked.
    #
    # WAS `clarify` UNTIL P1-22 (ruled Huayin, 2026-09-01). `customer` is real governed structure, so
    # this is not a language failure — but there is no lawful reading of THIS request either, and a
    # Clarify asks the reader to choose among readings. There was nothing here to choose between: the
    # "alternatives" were rewrites of the ask. Clarify is reserved for genuine multiple lawful
    # readings; this is |L(Q)| = 0, and |L(Q)| = 0 is Refuse.
    w = _wire(fixture_server, "SELECT level.sum AT {store} WHERE customer = 'C001'")
    assert w["outcome"] == "refuse"
    nr = w["columns"][0]["no_result"]
    assert nr["reason"] == "filter_unreachable"
    assert "customer" in nr["detail"] and len(nr["alternatives"]) >= 1


# --- the four moods still reachable through the envelope -----------------------------------------
def test_envelope_disclose(fixture_server):
    # CARRIER SWAPPED 2026-08-20 (Huayin, generated-family law). This test only ever needed A disclose
    # to prove the mood reaches the wire through the envelope; it used `SELECT level.sum AT {store}`,
    # which is no longer one — a structurally blocked reduction REFUSES (see
    # test_envelope_refuse_blocked_reduction below). `visitors` is `distinct(customer_id)`, an HLL
    # sketch, so it carries a MATERIAL `approximation` caveat on a result that is entirely lawful —
    # the shape disclose is actually for: a qualified answer, not a laundered one.
    w = _wire(fixture_server, "SELECT visitors AT {region}")
    assert w["outcome"] == "disclose"
    codes = [(d["code"], d["materiality"]) for d in w["columns"][0]["disclosures"]]
    assert ("approximation", "material") in codes


def test_envelope_refuse(fixture_server):
    w = _wire(fixture_server, "SELECT level.last AT {customer}")
    assert w["outcome"] == "refuse"
    assert w["columns"][0]["no_result"]["reason"] == "out_of_universe"


def test_envelope_refuse_blocked_reduction(fixture_server):
    # MINTED 2026-08-20 (Huayin), taking over the case `test_envelope_disclose` used to carry:
    # `level.sum @ store` collapses days and `sum` is declared BLOCKED along `calendar`, so the
    # envelope path refuses on the same law the terse path does. Disclose exists inside the lawful
    # region; it cannot legalize an operation the governed law does not possess.
    w = _wire(fixture_server, "SELECT level.sum AT {store}")
    assert w["outcome"] == "refuse"
    nr = w["columns"][0]["no_result"]
    assert (nr["kind"], nr["reason"], nr["discriminator"]) == ("refuse", "blocked_reduction", "unsupported")
    assert not (w["columns"][0].get("disclosures") or [])       # no number, so nothing to caveat


def test_envelope_clarify(fixture_server):
    # CARRIER SWAPPED 2026-08-20 (Huayin, ruling §9): `avg(aov) AT {cal.month}` is no longer a clarify
    # — `day` is the ONLY lawful input anchor there, and one lawful reading is not a contested choice,
    # so it defaults and discloses. A clarify needs TWO surviving lawful readings: at
    # `{region*cal.month}` both `store` and `day` reach the anchor lawfully, so the menu is real.
    w = _wire(fixture_server, "SELECT avg(aov) AT {region*cal.month}")
    assert w["outcome"] == "clarify"
    nr = w["columns"][0]["no_result"]
    assert nr["reason"] == "input_anchor_ambiguous"
    alts = [a["description"] for a in nr["alternatives"]]
    assert any("'day'" in a for a in alts) and any("'store'" in a for a in alts)


def test_envelope_unpinned_single_lawful_reading_discloses(fixture_server):
    # MINTED 2026-08-20 (Huayin, ruling §9). Candidate input anchors are filtered for LAWFULNESS
    # FIRST; when exactly ONE survives there is nothing to choose between, so the planner defaults to
    # it and PROCEEDS — wire outcome `disclose`, carrying a MATERIAL `input_anchor` caveat that names
    # the defaulted grain. Never a clarify: a menu of one is not a question.
    # ANCHOR SWAPPED 2026-08-31 (P1-13). This used `{cal.month}` on the claim that `day` is the ONLY
    # lawful input anchor there — true under the SUPERSEDED enumeration, which required a candidate to
    # REACH the output anchor, and false under WP-GRAIN-1, where eight levels are lawful readings at
    # `cal.month`. Defaulting silently to one of eight was the defect. `{customer, day, store}` is a
    # genuine one-reading anchor: `product` is the only level that survives the same law an explicit
    # pin is held to. The DISPOSITION LAW under test is unchanged.
    w = _wire(fixture_server, "SELECT avg(aov) AT {customer, day, store}")
    assert w["outcome"] == "disclose"
    assert w["columns"][0].get("no_result") is None
    codes = [(d["code"], d["materiality"]) for d in w["columns"][0]["disclosures"]]
    assert ("input_anchor", "material") in codes
    detail = next(d["detail"] for d in w["columns"][0]["disclosures"] if d["code"] == "input_anchor")
    assert "DEFAULTED to 'product'" in detail

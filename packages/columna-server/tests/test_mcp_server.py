"""
test_mcp_server.py — the eight WP-2.2 acceptance items, exercised over a real MCP stdio session,
plus the two-hop clarify round-trip (ruling A2+) and structural-error handling.
"""


async def test_tools_registered(mcp_session):
    async with mcp_session() as client:
        names = await client.list_tools()
    assert set(names) == {"list_manifolds", "describe_manifold", "describe_measure", "query", "explain"}


# --- acceptance #1 --------------------------------------------------------------------------
async def test_list_and_describe_roundtrip(mcp_session):
    async with mcp_session() as client:
        lst = await client.call("list_manifolds")
        dm = await client.call("describe_manifold", manifold_id="benchmark")
    assert lst["contract_version"] == "1"
    bm = next(m for m in lst["manifolds"] if m["manifold_id"] == "benchmark")
    assert bm["n_measures"] == 6 and set(bm["universes"]) == {"transactions", "store_days"}
    measures = [m["name"] for m in dm["measures"]]
    assert "region_label" in measures          # the WP-0 parity canary
    sd = next(u for u in dm["universes"] if u["name"] == "store_days")
    assert sd["predicate"] == "day >= stores.opened_date"


# --- acceptance #2 --------------------------------------------------------------------------
async def test_describe_measure_family_triple(mcp_session):
    async with mcp_session() as client:
        d = await client.call("describe_measure", manifold_id="benchmark", measure="level")
    assert d["family"]["root"] == "level"
    assert set(d["family"]["members"]) == {"sum", "last"}
    assert d["member_anchors"]["sum"]["blocked_lineages"] == ["calendar"]
    assert d["member_anchors"]["last"]["order_by"] == "day"
    assert d["v_anchor"] == {"universe": "store_days", "grain": ["day", "store"]}
    assert d["provenance"]["measure"] == "data_attested"


# --- acceptance #3: the wedge -------------------------------------------------------------
async def test_query_clarify_wedge(mcp_session):
    async with mcp_session() as client:
        w = await client.call("query", manifold_id="benchmark",
                              frameql="rate: revenue / level.last @ store, day")
    assert w["outcome"] == "clarify"
    col = w["columns"][0]
    assert col["status"] == "clarify"
    nr = col["no_result"]
    assert nr["reason"] == "co_anchor_ambiguous" and nr["discriminator"] == "ambiguous"
    assert len(nr["alternatives"]) >= 2
    assert {a["apply"]["universe"] for a in nr["alternatives"]} == {"transactions", "store_days"}


# --- acceptance #4: the two-hop round-trip (ruling A2+) -------------------------------------
async def test_clarify_two_hop_roundtrip(mcp_session):
    async with mcp_session() as client:
        clarify = await client.call("query", manifold_id="benchmark",
                                    frameql="rate: revenue / level.last @ store, day")
        pinned_universe = clarify["columns"][0]["no_result"]["alternatives"][0]["apply"]["universe"]

        # hop 1: substitute the pin token -> a non-clarify outcome with an informative refuse reason
        hop1 = await client.call("query", manifold_id="benchmark",
                                 frameql="rate: revenue / level.last @ store, day", universe=pinned_universe)

        # hop 2: reformulate per the clarify's detail into separate columns -> serve + coverage caveat
        hop2 = await client.call("query", manifold_id="benchmark",
                                 frameql="revenue: revenue, inv: level.last @ store, day")

    assert hop1["outcome"] != "clarify"
    assert hop1["outcome"] == "refuse"
    assert hop1["columns"][0]["no_result"]["reason"] == "out_of_universe"
    # hop 2 serves the numbers but rides a MATERIAL coverage caveat -> the wire outcome is `disclose`
    # (clarify -> refuse -> disclose is three of the four moods in one flow).
    assert hop2["outcome"] == "disclose"
    assert "denominator_population" in [d["code"] for d in hop2["frame"]["disclosures"]]


# --- acceptance #5: B-anchor inform-and-serve on the wire -----------------------------------
async def test_banchor_served_with_material_critical(mcp_session):
    async with mcp_session() as client:
        w = await client.call("query", manifold_id="benchmark", frameql="inv: level.sum @ store")
    assert w["outcome"] == "disclose"
    col = w["columns"][0]
    assert col["status"] == "served" and "values" in col
    cav = col["disclosures"][0]
    assert (cav["code"], cav["materiality"], cav["severity"]) == ("blocked_reduction", "material", "critical")


# --- acceptance #6: refuse vs error are distinguishable ------------------------------------
async def test_out_of_universe_refuse_vs_unknown_error(mcp_session):
    async with mcp_session() as client:
        refuse = await client.call("query", manifold_id="benchmark", frameql="i: level.last @ product")
        err = await client.call("query", manifold_id="benchmark", frameql="z: revenue.zap @ store")
    rc = refuse["columns"][0]
    assert refuse["outcome"] == "refuse" and rc["status"] == "refuse"
    assert rc["no_result"]["discriminator"] == "unsupported"
    ec = err["columns"][0]
    assert err["outcome"] == "error" and ec["status"] == "error"
    assert ec["no_result"]["kind"] == "error"


# --- acceptance #7: explain touches zero data ----------------------------------------------
async def test_explain_zero_fetch_identical_payload(mcp_session):
    async with mcp_session() as client:
        q = await client.call("query", manifold_id="benchmark", frameql="inv: level.sum @ store")
        ex = await client.call("explain", manifold_id="benchmark", frameql="inv: level.sum @ store")
    assert ex["executed"] is False
    assert ex["fetches_delta"] == 0

    def caveats(w):
        return [(d["code"], d["materiality"], d["severity"]) for d in w["columns"][0]["disclosures"]]
    assert caveats(ex) == caveats(q)


# --- read-only / no-SQL surface ------------------------------------------------------------
async def test_no_sql_surface(mcp_session):
    async with mcp_session() as client:
        w = await client.call("query", manifold_id="benchmark", frameql="SELECT * FROM transactions")
    assert w["outcome"] == "error" and w["error"]["reason"] == "frameql_syntax"


async def test_unknown_manifold_is_error_result(mcp_session):
    async with mcp_session() as client:
        res = await client.call_raw("describe_manifold", manifold_id="nope")
    assert res.isError


# --- wire-contract SCHEMA + disclosure scoping (post-checkpoint contract, formalized) -------
_CAVEAT_KEYS = {"code", "materiality", "severity", "category", "detail", "remedy", "source", "rel_error"}


def _assert_caveat_shape(d):
    assert set(d) == _CAVEAT_KEYS, d
    assert d["materiality"] in ("material", "immaterial")


def _assert_frame_shape(w):
    assert w["contract_version"] == "1"
    assert w["outcome"] in ("serve", "disclose", "clarify", "refuse", "error")
    fr = w["frame"]
    assert set(fr) >= {"anchor", "universe", "rollup_severity", "disclosures"}
    assert isinstance(fr["anchor"], list)
    assert fr["rollup_severity"] in ("none", "info", "caution", "critical")
    for d in fr["disclosures"]:                    # frame-scoped
        _assert_caveat_shape(d)
    for col in w["columns"]:
        assert {"name", "status", "disclosures"} <= set(col)
        assert col["status"] in ("served", "clarify", "refuse", "error")
        for d in col["disclosures"]:               # column-scoped
            _assert_caveat_shape(d)
        if col["status"] == "served":
            assert ("value" in col) or ("values" in col)
            assert "no_result" not in col
        else:
            nr = col["no_result"]
            assert {"kind", "discriminator", "reason", "detail", "alternatives"} <= set(nr)


async def test_wire_contract_schema_and_scoping(mcp_session):
    async with mcp_session() as client:
        serve = await client.call("query", manifold_id="benchmark", frameql="revenue: revenue @ region")
        disclose = await client.call("query", manifold_id="benchmark", frameql="inv: level.sum @ store")
        clarify = await client.call("query", manifold_id="benchmark",
                                    frameql="rate: revenue / level.last @ store, day")
        hop2 = await client.call("query", manifold_id="benchmark",
                                 frameql="rev: revenue, inv: level.last @ store, day")
    for w in (serve, disclose, clarify, hop2):
        _assert_frame_shape(w)
    # outcome derivation: nothing material -> serve; a material caveat -> disclose
    assert serve["outcome"] == "serve"
    assert disclose["outcome"] == "disclose"
    # scoping: the multi-universe coverage caveat is FRAME-scoped, not on any column
    frame_codes = [d["code"] for d in hop2["frame"]["disclosures"]]
    assert "denominator_population" in frame_codes
    for col in hop2["columns"]:
        assert "denominator_population" not in [d["code"] for d in col["disclosures"]]

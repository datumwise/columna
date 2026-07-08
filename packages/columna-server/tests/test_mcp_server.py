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
    assert hop2["outcome"] in ("serve", "disclose")
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

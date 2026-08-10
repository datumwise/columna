"""
test_mcp_server.py — the eight WP-2.2 acceptance items, exercised over a real MCP stdio session,
plus the two-hop clarify round-trip (ruling A2+) and structural-error handling.
"""


async def test_tools_registered(mcp_session):
    async with mcp_session() as client:
        names = await client.list_tools()
    assert set(names) == {"list_manifolds", "describe_manifold", "describe_measure", "execute_frame_query",
                          "query", "explain", "check_frame_query", "frame_ql_grammar", "discovery",
                          "manifold_status", "get_evidence", "case_chapter", "case_manifest"}


# --- acceptance #1 --------------------------------------------------------------------------
async def test_list_and_describe_roundtrip(mcp_session):
    async with mcp_session() as client:
        lst = await client.call("list_manifolds")
        dm = await client.call("describe_manifold", manifold_id="benchmark")
    assert lst["contract_version"] == "2"
    bm = next(m for m in lst["manifolds"] if m["manifold_id"] == "benchmark")
    assert bm["n_measures"] == 6 and set(bm["universes"]) == {"transactions", "store_days"}
    measures = [m["name"] for m in dm["measures"]]
    assert "region_label" in measures          # the WP-0 parity canary
    sd = next(u for u in dm["universes"] if u["name"] == "store_days")
    # C-2 insulation (§2b, CP-3): the predicate renders LOGICALLY — the physical `stores.` qualifier
    # (a shipped leak this test previously codified) no longer crosses describe.
    assert sd["predicate"] == "day >= opened_date"


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
    # §2c reframe: the clarify exemplar is now an inline reduction with no pinned input anchor (the
    # cross-universe ratio is a category ERROR, not a clarify).
    async with mcp_session() as client:
        w = await client.call("query", manifold_id="benchmark",
                              frameql="SELECT avg(aov) AS rate AT {cal.month}")
    assert w["outcome"] == "clarify"
    col = w["columns"][0]
    assert col["status"] == "clarify"
    nr = col["no_result"]
    assert nr["reason"] == "input_anchor_ambiguous" and nr["discriminator"] == "ambiguous"
    assert len(nr["alternatives"]) >= 1


# --- acceptance #4: the two-hop round-trip (clarify -> reformulate -> serve), §2c-reframed ----
async def test_clarify_two_hop_roundtrip(mcp_session):
    async with mcp_session() as client:
        clarify = await client.call("query", manifold_id="benchmark",
                                    frameql="SELECT avg(aov) AS rate AT {cal.month}")
        # hop: reformulate per the clarify — PIN the input anchor -> serve (a definite quantity)
        hop = await client.call("query", manifold_id="benchmark",
                                frameql="SELECT avg(aov@day) AS rate AT {cal.month}")
        # and a structural refusal in the same manifold — an ask outside the contracted space
        refuse = await client.call("query", manifold_id="benchmark",
                                   frameql="SELECT level.last AS inv AT {customer}")
    assert clarify["outcome"] == "clarify"
    assert clarify["columns"][0]["no_result"]["reason"] == "input_anchor_ambiguous"
    assert hop["outcome"] in ("serve", "disclose")            # the pinned reformulation is a definite quantity
    assert refuse["outcome"] == "refuse"
    assert refuse["columns"][0]["no_result"]["reason"] == "out_of_universe"


# --- acceptance #5: B-anchor inform-and-serve on the wire -----------------------------------
async def test_banchor_served_with_material_critical(mcp_session):
    async with mcp_session() as client:
        w = await client.call("query", manifold_id="benchmark", frameql="SELECT level.sum AS inv AT {store}")
    assert w["outcome"] == "disclose"
    col = w["columns"][0]
    assert col["status"] == "served" and "values" in col
    cav = col["disclosures"][0]
    assert (cav["code"], cav["materiality"], cav["severity"]) == ("blocked_reduction", "material", "critical")


# --- acceptance #6: refuse vs error are distinguishable ------------------------------------
async def test_out_of_universe_refuse_vs_unknown_error(mcp_session):
    async with mcp_session() as client:
        refuse = await client.call("query", manifold_id="benchmark", frameql="SELECT level.last AS i AT {product}")
        err = await client.call("query", manifold_id="benchmark", frameql="SELECT revenue.zap AS z AT {store}")
    rc = refuse["columns"][0]
    assert refuse["outcome"] == "refuse" and rc["status"] == "refuse"
    assert rc["no_result"]["discriminator"] == "unsupported"
    ec = err["columns"][0]
    assert err["outcome"] == "error" and ec["status"] == "error"
    assert ec["no_result"]["kind"] == "error"


# --- acceptance #7: EXPLAIN (envelope) touches zero data; would-be matches the query -------------
async def test_explain_envelope_zero_fetch_and_would_be(mcp_session):
    async with mcp_session() as client:
        q = await client.call("query", manifold_id="benchmark", frameql="SELECT level.sum AS inv AT {store}")
        ex = await client.call("explain", manifold_id="benchmark", frameql="SELECT level.sum AT {store}")
    # zero data + the rich EXPLAIN payload (desugared artifact + series/cone)
    assert ex["executed"] is False and ex["fetches_delta"] == 0
    # WP-NAME-1 (0.14.0): the key IS the canonical expression `level.sum` (no `level_sum` mangle, and
    # no redundant `X AS X` — the expression names itself).
    assert "level.sum" in ex["desugared"] and " AS " not in ex["desugared"] and ex["outcome"] == q["outcome"]
    # the would-be disclosures equal the query's actual disclosures (explain is the plan, annotated)
    q_cav = [(d["code"], d["materiality"], d["severity"]) for d in q["columns"][0]["disclosures"]]
    ex_cav = [(d["code"], d["materiality"], d["severity"]) for d in ex["series"][0]["would_be"]["disclosures"]]
    assert ex_cav == q_cav


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
    assert w["contract_version"] == "2"
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
        serve = await client.call("query", manifold_id="benchmark", frameql="SELECT revenue AS revenue AT {region}")
        disclose = await client.call("query", manifold_id="benchmark", frameql="SELECT level.sum AS inv AT {store}")
        clarify = await client.call("query", manifold_id="benchmark",
                                    frameql="SELECT avg(aov) AS rate AT {cal.month}")
        error = await client.call("query", manifold_id="benchmark",
                                  frameql="SELECT revenue / level.last AS rate AT {store*day}")
    for w in (serve, disclose, clarify, error):
        _assert_frame_shape(w)
    # outcome derivation: nothing material -> serve; a material caveat -> disclose
    assert serve["outcome"] == "serve"
    assert disclose["outcome"] == "disclose"
    assert clarify["outcome"] == "clarify"
    # §2c: the cross-universe expression is a category ERROR (not a clarify), and juxtaposition carries
    # NO multi-universe coverage caveat (retired) — the four moods are taught by well-posed asks now.
    assert error["outcome"] == "error"
    assert error["columns"][0]["no_result"]["reason"] == "cross_universe"


# --- the no-engine tools -----------------------------------------------------------------
async def test_check_frame_query_is_zero_fetch_and_returns_a_mood(mcp_session):
    async with mcp_session() as client:
        ok = await client.call("check_frame_query", manifold_id="benchmark",
                              frameql="SELECT revenue AT {day}")
        bad = await client.call("check_frame_query", manifold_id="benchmark", frameql="SELECT AT")
    # the whole point: planned, not executed — zero backend fetches
    assert ok["executed"] is False and ok["fetches_delta"] == 0
    assert ok["outcome"] in {"serve", "disclose", "clarify", "refuse", "error"}
    assert ok["contract_version"] == "2"
    # a syntax error is an error wire, never an exception
    assert bad["outcome"] == "error" and bad["error"]["reason"] == "frameql_syntax"


async def test_frame_ql_grammar_is_verbatim_and_versioned(mcp_session):
    async with mcp_session() as client:
        g = await client.call("frame_ql_grammar")
    assert "SELECT" in g["grammar"] and "AT {" in g["grammar"]
    assert g["generated_by"].startswith("columna-core ")
    assert g["contract_version"] == "2"


async def test_discovery_lists_askable_measures_and_anchors(mcp_session):
    async with mcp_session() as client:
        d = await client.call("discovery", manifold_id="benchmark")
    measures = {m["measure"] for m in d["measures"]}
    assert {"revenue", "level"} <= measures
    rev = next(m for m in d["measures"] if m["measure"] == "revenue")
    assert rev["universe"] and rev["grain"] and "sum" in rev["reducers"]
    assert {a["universe"] for a in d["anchors"]} == {"transactions", "store_days"}


async def test_manifold_status_counts(mcp_session):
    async with mcp_session() as client:
        s = await client.call("manifold_status", manifold_id="benchmark")
    assert s["counts"]["measures"] == 6
    assert s["counts"]["universes"] == 2
    assert "verdicts" in s["evidence"]


async def test_get_evidence_grades_and_scoped(mcp_session):
    async with mcp_session() as client:
        whole = await client.call("get_evidence", manifold_id="benchmark")
        one = await client.call("get_evidence", manifold_id="benchmark", measure="revenue")
    assert whole["measures"]["revenue"] in {"data_attested", "declared", "inferred"}
    assert one["measure"] == "revenue" and "sum" in one["members"]
    assert "basis" in one["universe"]


# --- the executing tool: rename + annotation, deprecated alias --------------------------------
async def test_execute_frame_query_annotates_executed_and_fetch_delta(mcp_session):
    # the executing counterpart of check_frame_query: it runs, so executed is TRUE and fetches happened
    async with mcp_session() as client:
        w = await client.call("execute_frame_query", manifold_id="benchmark",
                              frameql="SELECT revenue AS revenue AT {region}")
    assert w["outcome"] == "serve" and w["columns"][0]["status"] == "served"
    assert w["executed"] is True                       # emitted on the executing path now
    assert isinstance(w["fetches_delta"], int) and w["fetches_delta"] >= 1   # it actually touched data
    assert w["contract_version"] == "2"


async def test_query_is_a_deprecated_alias_with_identical_wire(mcp_session):
    async with mcp_session() as client:
        new = await client.call("execute_frame_query", manifold_id="benchmark",
                                frameql="SELECT level.sum AS inv AT {store}")
        old = await client.call("query", manifold_id="benchmark",
                                frameql="SELECT level.sum AS inv AT {store}")
    # the alias forwards to the executing path: both run (executed True), same mood, same served values.
    # (Full-dict equality is not asserted — the second read is served-from-cache and carries an extra
    #  immaterial `freshness` disclosure; the forward is what this test proves, not cache state.)
    assert old["executed"] is True and new["executed"] is True
    assert old["outcome"] == new["outcome"]
    identity = lambda w: [(c["name"], c["status"], c.get("values"), c.get("value")) for c in w["columns"]]
    assert identity(old) == identity(new)


async def test_no_engine_tools_reject_unknown_manifold(mcp_session):
    # a structural miss RAISES (MCP error), it is not a mood
    async with mcp_session() as client:
        for name in ("discovery", "manifold_status", "get_evidence", "check_frame_query"):
            args = {"manifold_id": "nope"}
            if name == "check_frame_query":
                args["frameql"] = "SELECT revenue AT {day}"
            raised = False
            try:
                await client.call(name, **args)
            except Exception:
                raised = True
            assert raised, f"{name} should raise on unknown manifold"

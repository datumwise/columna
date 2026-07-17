"""
test_envelope_explain.py — EXPLAIN over the envelope (WP-FrameQL increment).

EXPLAIN emits the canonical DESUGARED form (the exact artifact the planner consumed — desugar()'s
output, never a reconstruction), the per-series atom decomposition, the dependency cone with current
verdicts, and the would-be annotation, touching ZERO data.
"""
from columna_core.envelope import parse_statement


def _explain(server, q):
    return server.explain_statement(parse_statement(q))


# --- the desugared form IS desugar()'s output (rider 1) ------------------------------------------
def test_desugared_is_the_consumed_artifact(fixture_server):
    q = "SELECT avg(aov @ day) AT {cal.month}"
    ex = _explain(fixture_server, q)
    consumed = fixture_server.planner.desugar(parse_statement(q)).render_canonical()
    assert ex["desugared"] == consumed                       # the artifact, not a reconstruction
    assert "avg(aov @ {day}) AS avg_aov" in ex["desugared"]  # canonical braces + resolved name


# --- zero data touched ---------------------------------------------------------------------------
def test_zero_data_touched(fixture_server):
    ex = _explain(fixture_server, "SELECT revenue AT {region}")
    assert ex["executed"] is False and ex["fetches_delta"] == 0


# --- atom decomposition --------------------------------------------------------------------------
def test_atom_decomposition_expands_derived(fixture_server):
    # aov is derived (revenue / orders) -> its atoms are the underlying measures
    ex = _explain(fixture_server, "SELECT avg(aov @ day) AT {cal.month}")
    atoms = {(a["measure"], a["member"]) for a in ex["series"][0]["cone"]["atoms"]}
    assert ("revenue", "sum") in atoms and ("orders", "count") in atoms
    assert ex["series"][0]["cone"]["derived"][0]["name"] == "aov"


def test_bare_measure_atoms(fixture_server):
    ex = _explain(fixture_server, "SELECT revenue AT {region}")
    a = ex["series"][0]["cone"]["atoms"][0]
    assert a["measure"] == "revenue" and a["universe"] == "transactions"


# --- dependency cone: edges + verdicts + scope ---------------------------------------------------
def test_cone_edges_traversed(fixture_server):
    ex = _explain(fixture_server, "SELECT revenue AT {region}")
    edges = ex["series"][0]["cone"]["edges"]
    assert any(e["frm"] == "store" and e["to"] == "region" for e in edges)


def test_cone_carries_license_slot(fixture_server):
    # unadjudicated manifold -> license is None (present-but-null, never fabricated)
    ex = _explain(fixture_server, "SELECT revenue AT {region}")
    assert "license" in ex["series"][0]["cone"]["atoms"][0]


# --- the would-be annotation matches the four moods ----------------------------------------------
def test_would_be_serve(fixture_server):
    ex = _explain(fixture_server, "SELECT revenue AT {region}")
    assert ex["outcome"] == "serve" and ex["series"][0]["would_be"]["status"] == "served"


def test_would_be_disclose_carries_caveat(fixture_server):
    ex = _explain(fixture_server, "SELECT level.sum AT {store}")
    assert ex["outcome"] == "disclose"
    codes = [d["code"] for d in ex["series"][0]["would_be"]["disclosures"]]
    assert "blocked_reduction" in codes


def test_would_be_clarify(fixture_server):
    ex = _explain(fixture_server, "SELECT avg(aov) AT {cal.month}")
    assert ex["outcome"] == "clarify"
    assert ex["series"][0]["would_be"]["no_result"]["reason"] == "input_anchor_ambiguous"


# --- EXPLAIN and the would-be plan agree (explain is the plan, annotated) -------------------------
def test_explain_outcome_equals_plan_outcome(fixture_server):
    from columna_core.disclosure_wire import wire_frame
    for q in ["SELECT revenue AT {region}", "SELECT level.sum AT {store}", "SELECT avg(aov) AT {cal.month}"]:
        ex = _explain(fixture_server, q)
        planned = wire_frame(fixture_server.planner.plan_statement(parse_statement(q)))
        assert ex["outcome"] == planned["outcome"]

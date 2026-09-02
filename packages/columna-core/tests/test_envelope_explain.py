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
    assert "avg(aov @ {day})" in ex["desugared"]           # WP-NAME-1: key IS the canonical expression
    assert " AS " not in ex["desugared"]                    # no redundant `X AS X` — the expression names itself


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
    # CARRIER SWAPPED 2026-08-20 (Huayin, generated-family law). This test asked EXPLAIN about
    # `level.sum AT {store}` and expected a would-be DISCLOSE carrying the critical
    # `blocked_reduction` caveat. That reduction now refuses (see test_would_be_refuse_blocked_reduction
    # below), so the disclose leg is carried by a lawful-but-qualified result instead: `visitors` is an
    # HLL `distinct` sketch, whose MATERIAL `approximation` caveat is knowable from the spec alone —
    # exactly the kind of would-be annotation EXPLAIN exists to surface without touching data.
    ex = _explain(fixture_server, "SELECT visitors AT {region}")
    assert ex["outcome"] == "disclose"
    assert ex["executed"] is False and ex["fetches_delta"] == 0
    codes = [(d["code"], d["materiality"]) for d in ex["series"][0]["would_be"]["disclosures"]]
    assert ("approximation", "material") in codes


def test_would_be_refuse_blocked_reduction(fixture_server):
    # MINTED 2026-08-20 (Huayin), taking over the case `test_would_be_disclose_carries_caveat` used to
    # carry. A structurally prohibited reduction is a pure SHAPE fact, so EXPLAIN can hand back the
    # REFUSAL — reason `blocked_reduction`, discriminator `unsupported` — before a single scan is
    # spent, and it agrees byte-for-byte with what `run` would return.
    ex = _explain(fixture_server, "SELECT level.sum AT {store}")
    assert ex["outcome"] == "refuse"
    wb = ex["series"][0]["would_be"]
    assert (wb["no_result"]["kind"], wb["no_result"]["reason"], wb["no_result"]["discriminator"]) == \
           ("refuse", "blocked_reduction", "unsupported")
    assert wb["disclosures"] == []                       # nothing was produced, so nothing is caveated
    assert ex["executed"] is False and ex["fetches_delta"] == 0


def test_would_be_clarify(fixture_server):
    # CARRIER SWAPPED 2026-08-20 (Huayin, ruling §9): at `{cal.month}` the unpinned `avg(aov)` has
    # exactly ONE lawful input anchor (`day`), which is not a contested choice — it defaults and
    # discloses. A clarify needs two surviving lawful readings, which `{region*cal.month}` supplies
    # (`store` and `day` both reach it lawfully).
    ex = _explain(fixture_server, "SELECT avg(aov) AT {region*cal.month}")
    assert ex["outcome"] == "clarify"
    assert ex["series"][0]["would_be"]["no_result"]["reason"] == "input_anchor_ambiguous"


# --- EXPLAIN and the would-be plan agree (explain is the plan, annotated) -------------------------
def test_explain_outcome_equals_plan_outcome(fixture_server):
    from columna_core.disclosure_wire import wire_frame
    for q in ["SELECT revenue AT {region}", "SELECT visitors AT {region}",
              "SELECT level.sum AT {store}", "SELECT avg(aov) AT {region*cal.month}"]:
        ex = _explain(fixture_server, q)
        planned = wire_frame(fixture_server.planner.plan_statement(parse_statement(q)))
        assert ex["outcome"] == planned["outcome"]


# --- CLOSED (2026-08-20): the would-be annotation predicts the DEFAULTED input anchor -------------
# Found by the doctrine reconciliation and fixed the same day. Ruling §9's |L| = 1 leg makes the
# planner DEFAULT an omitted input anchor and attach a MATERIAL `input_anchor` caveat, so `run`
# returns DISCLOSE. The caveat was attached only in `_resolve_inline_reduction` — the EXECUTION path
# — while `plan()` built its would-be annotation from `engine.dry_disclose` over the expression's
# ATOMS, which cannot see a decision taken above an atom. So plan said `serve` where run said
# `disclose`, and EXPLAIN under-reported a material condition — precisely the promise EXPLAIN makes.
# Both paths now build the caveat from `Planner._defaulted_anchor_caveat`, one constructor, because
# deriving it twice is how they drift.
def test_would_be_predicts_the_defaulted_input_anchor_caveat(fixture_server):
    from columna_core.disclosure_wire import wire_frame
    # ANCHOR SWAPPED 2026-08-31 (P1-13): `{cal.month}` stopped being a one-lawful-reading anchor when
    # the enumeration was brought forward to WP-GRAIN-1. `{customer, day, store}` is one, so the
    # plan/run agreement this test exists to check is exercised on a real |L| = 1 default.
    q = "SELECT avg(aov) AT {customer, day, store}"
    ex = _explain(fixture_server, q)
    ran = wire_frame(fixture_server.planner.run_statement(parse_statement(q)))
    assert ran["outcome"] == "disclose"                                    # what run actually does
    assert ex["outcome"] == ran["outcome"]                                 # ...and what plan should predict
    assert ("input_anchor", "material") in [
        (d["code"], d["materiality"]) for d in ex["series"][0]["would_be"]["disclosures"]]

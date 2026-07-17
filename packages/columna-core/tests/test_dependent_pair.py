"""
test_dependent_pair.py — dependent-pair transport (WP-FrameQL increment, flag 1).

The engine completes a target anchor where one level is FUNCTIONALLY DETERMINED by another
(`region` is fixed by `store`): the determined level is ATTACHED 1:1 along the edge (join-and-group,
native Polars), never reduced. The §7 worked example `AT {region*store}` runs WHOLE as the acceptance
test. DG-2 (collapse-a-base-dim while transporting another across a blocked lineage) is a DISTINCT gap
and is documented, not silently passed.
"""
from columna_core.envelope import parse_statement
from columna_core.disclosure_wire import wire_frame


def _run(server, q):
    fr = server.planner.run_statement(parse_statement(q))
    return fr, wire_frame(fr)


# --- bare-measure dependent pair -----------------------------------------------------------------
def test_bare_measure_at_dependent_pair_serves(fixture_server):
    fr, w = _run(fixture_server, "SELECT revenue AT {region*store}")
    assert w["outcome"] == "serve"
    assert set(fr.data.columns) == {"region", "store", "revenue"}
    assert len(fr.data) == fr.data["store"].n_unique()       # one row per store (region attached 1:1)


def test_attached_region_is_functionally_correct(fixture_server):
    # every store maps to exactly one region — the attach must not invent or duplicate
    fr, _ = _run(fixture_server, "SELECT revenue AT {region*store}")
    per_store_regions = fr.data.group_by("store").agg(__import__("polars").col("region").n_unique().alias("n"))
    assert per_store_regions["n"].max() == 1


def test_holistic_measure_at_dependent_pair_serves(fixture_server):
    # the holistic path (median) also completes the dependent pair
    fr, w = _run(fixture_server, "SELECT med_amount AT {region*store}")
    assert w["outcome"] == "serve"
    assert set(fr.data.columns) == {"region", "store", "med_amount"}


# --- THE §7 WORKED EXAMPLE runs whole (the ratified acceptance target) ---------------------------
def test_section7_worked_example_runs_whole(fixture_server):
    # §7 structure on fixture-valid input anchors (`@ {transaction}` -> the finest grains store & day):
    # two series at DIFFERENT input grains, a dependent-pair output anchor, ORDER BY (PER key leads),
    # and LIMIT n PER {region}. Every clause exercised end to end.
    q = ("SELECT sum(revenue @ {store}) AS gross, avg(aov @ {day}) AS typical "
         "AT {region*store} ORDER BY region, gross DESC LIMIT 3 PER {region}")
    fr, w = _run(fixture_server, q)
    assert w["outcome"] == "serve"
    assert set(fr.data.columns) == {"region", "store", "gross", "typical"}
    # LIMIT 3 PER region: at most 3 rows in each region
    counts = fr.data.group_by("region").len()
    assert counts["len"].max() <= 3
    # within each region, gross is descending (ORDER BY gross DESC after the PER grouping)
    for reg in fr.data["region"].unique().to_list():
        g = fr.data.filter(__import__("polars").col("region") == reg)["gross"].to_list()
        assert g == sorted(g, reverse=True)


def test_inline_reduction_multilevel_matches_bare(fixture_server):
    # sum(revenue @ {store}) reduced to region*store equals the bare revenue at region*store
    a, _ = _run(fixture_server, "SELECT sum(revenue @ {store}) AS v AT {region*store}")
    b, _ = _run(fixture_server, "SELECT revenue AS v AT {region*store}")
    am = dict(zip(a.data["store"], a.data["v"]))
    bm = dict(zip(b.data["store"], b.data["v"]))
    for st in am:
        assert am[st] == __import__("pytest").approx(bm[st])


# --- DG-2: reported, NOT silently passed (Huayin: report either way) -----------------------------
def test_dg2_is_a_distinct_gap_still_classified(fixture_server):
    # `level.sum @ cal.month` collapses a base dim (store) WHILE transporting another (day->cal.month,
    # a blocked lineage). This does NOT fall out of the dependent-pair machinery — it is a distinct gap.
    # It must at least stay CLASSIFIED (never a raw crash past the gate); it does not yet serve-with-caveat.
    fr, w = _run(fixture_server, "SELECT level.sum AT {cal.month}")
    assert w["outcome"] == "error"                           # classified, not raw
    assert fr.columns[0].refusal.reason == "unsupported"
    # NOTE (report): DG-2's designed behavior is serve-with-a-critical-blocked_reduction-caveat; that
    # is its OWN engine increment (collapse-with-blocked-transport), not this dependent-pair one.

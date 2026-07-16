"""
test_eval_harness.py — the eval scorer + run record + report (CP-2, to the standing contract).

Tests the MEASUREMENT INSTRUMENT with scripted init-OUTPUTS (no mind) — that the scorer computes the
ratified axes correctly, that a silent ◆ call is a hard fail, that convergence carries its censoring
flag, and that the run record labels its provenance. Judgment quality is NOT tested here (there is no
mind); this validates the ruler, not a subject.
"""
from columna_server.init.eval import (Benchmark, BenchmarkResult, RunRecord, score, render_report,
                                       rescore_run, SCORER_VERSION, BENCHMARK_LIST_VERSION)

# a ◆ benchmark: two closures, a graded edge, one oracle-asymmetric call to surface, a concentration cap
_B = Benchmark(
    id="B1", kind="◆", title="events-vs-spine",
    schema={"orders": (["id"], [(1,)])},
    ground_truth={
        "closures": [("measure", "orders"), ("universe", "sales")],
        "grades": {"measure:orders": "inferred_catalog"},
        "oracle_calls": ["basis(sales): events?"],
        "max_checklist": 3,
    })

_PERFECT = {
    "proposals": [{"kind": "measure", "target": "orders", "grade": "inferred_catalog"},
                  {"kind": "universe", "target": "sales"}],
    "checklist": ["basis(sales): events?"],
    "iterations": 2,
}


def test_perfect_output_passes_and_converges():
    r = score(_B, _PERFECT, loop_budget=5)
    assert r.passed and r.closure and r.grade and r.explicitness and r.checklist_concentration
    assert r.convergence_cost == 2 and r.converged is True


def test_a_fertility_opening_is_a_closure_hard_fail():
    out = dict(_PERFECT, proposals=_PERFECT["proposals"] + [
        {"kind": "derived", "target": "rate", "opens_fertility": True}])
    r = score(_B, out, loop_budget=5)
    assert not r.passed and not r.closure and "OPENING" in r.failure_narrative


def test_silent_oracle_call_is_a_hard_fail_even_if_values_right():
    out = dict(_PERFECT, checklist=[])              # the ◆ basis call not surfaced
    r = score(_B, out, loop_budget=5)
    assert not r.passed and not r.explicitness and "silent on oracle-asymmetric" in r.failure_narrative


def test_flooded_checklist_fails_concentration_not_the_hard_axes():
    out = dict(_PERFECT, checklist=["basis(sales): events?", "noise1", "noise2", "noise3"])
    r = score(_B, out, loop_budget=5)
    assert r.explicitness and not r.checklist_concentration      # surfaced, but flooded past max 3
    assert "flooded" in r.failure_narrative


def test_convergence_censoring_flag_distinguishes_capped_from_converged():
    # cost 6, but the draft passes -> converged False only because it exceeded budget 5 (censored).
    r = score(_B, dict(_PERFECT, iterations=6), loop_budget=5)
    assert r.passed and r.convergence_cost == 6 and r.converged is False


def test_scorer_04_desugars_hierarchy_to_edges_for_closure_equivalence():
    # ruling 2 (2026-07-16): closure comparison at the DESUGARED NORMAL FORM. A ground truth of
    # `hierarchy day->month` and a proposal `edge day->month` are EQUIVALENT (the grammar desugars a
    # hierarchy to its edges) — was never a miss. A ground truth of `edge day->month` proposed as a
    # `hierarchy day->month` also matches (symmetric). Levels-without-travel is a GENUINE miss.
    hier_gt = Benchmark(id="H", kind="○", schema={"t": (["d"], [(1,)])},
                        ground_truth={"closures": [("hierarchy", "day->month")],
                                      "grades": {"hierarchy:day->month": "inferred_sample"}})
    edge_gt = Benchmark(id="E", kind="○", schema={"t": (["d"], [(1,)])},
                        ground_truth={"closures": [("edge", "day->month")],
                                      "grades": {"edge:day->month": "inferred_sample"}})
    as_edge = {"proposals": [{"kind": "edge", "target": "day->month", "grade": "inferred_sample"}], "iterations": 1}
    as_hier = {"proposals": [{"kind": "hierarchy", "target": "day->month", "grade": "inferred_sample"}], "iterations": 1}
    as_levels = {"proposals": [{"kind": "level", "target": "day"}, {"kind": "level", "target": "month"}],
                 "iterations": 1}
    # equivalent-with-edges matches, both directions; grade rides the desugared atom
    assert score(hier_gt, as_edge, 5).closure and score(hier_gt, as_edge, 5).grade
    assert score(edge_gt, as_hier, 5).closure and score(edge_gt, as_hier, 5).grade
    assert score(hier_gt, as_hier, 5).closure                    # identity still matches
    # levels without the edge/hierarchy do NOT reduce to travel — a genuine miss
    assert not score(hier_gt, as_levels, 5).closure
    assert not score(edge_gt, as_levels, 5).closure


def test_rescore_run_re_renders_from_captured_output_without_a_rerun():
    # ruling 5 (2026-07-16): a scorer bump must let a prior run re-render like-with-like WITHOUT re-running
    # the mind. A result captures its scored proposals/checklist; rescore_run replays score() under the
    # current scorer. A pre-capture result (run-4's shape) passes through UNCHANGED — an honest gap.
    hier_gt = Benchmark(id="H", kind="○", schema={"t": (["d"], [(1,)])},
                        ground_truth={"closures": [("hierarchy", "day->month")],
                                      "grades": {"hierarchy:day->month": "inferred_sample"}})
    captured = score(hier_gt, {"proposals": [{"kind": "edge", "target": "day->month",
                                              "grade": "inferred_sample"}], "iterations": 1}, 5)
    assert captured.scored_proposals                       # the raw proposals rode along
    pre_capture = BenchmarkResult(benchmark_id="H", kind="○", closure=False, grade=None,
                                  explicitness=True, checklist_concentration=True, convergence_cost=1,
                                  loop_budget=5, converged=False, passed=False)  # no captured output (run-4 shape)
    run = RunRecord(model_id="m", model_version="-", sampling={}, harness_config={}, kp_version="0.2",
                    provider="anthropic", results=[captured, pre_capture])
    re = rescore_run(run, {"H": hier_gt})
    assert re.scorer_version == SCORER_VERSION and re.run_id.endswith(f"~rescored@{SCORER_VERSION}")
    assert re.results[0].closure                           # re-rendered: edge≡hierarchy under 0.4
    assert re.results[1] is pre_capture                    # uncaptured -> passed through, not fabricated


def test_run_record_carries_provenance_and_renders_the_standing_report():
    run = RunRecord(
        model_id="claude-opus-4-8", model_version="20260101",
        sampling={"temperature": 0.0, "seed": 7, "max_tokens": 4096},
        harness_config={"aperture_cap": 1000, "loop_iteration_budget": 5},
        kp_version="0.1", provider="scripted",
        results=[score(_B, _PERFECT, 5), score(_B, dict(_PERFECT, checklist=[]), 5)])
    assert run.scorer_version == SCORER_VERSION and run.benchmark_list_version == BENCHMARK_LIST_VERSION
    s = run.summary()
    assert s["passed"] == 1 and s["oracle_explicit"] == 1 and s["oracle_total"] == 2
    report = render_report(run)
    assert "provider=scripted" in report and "sampling=" in report and "scorer=" in report
    assert "◆-explicitness 1/2" in report and "narrative:" in report

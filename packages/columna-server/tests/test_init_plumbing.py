"""
test_init_plumbing.py — the end-to-end init plumbing, HERMETIC (CP-2).

Proves schema → aperture → loop → output → scorer → report end to end with a SCRIPTED stand-in for the
mind (the gold scripts) — the pipeline the first real-model run will walk. Harness behavior only; the
real model runs only on Huayin's explicit go. Also pins the response PARSE (incl. the wall on the
response side) without any network.
"""
import pytest

from columna_server.init import (ScriptedProvider, run_benchmark, render_report, RunRecord,
                                 parse_proposals, system_prompt, AnthropicProvider, ProviderUnavailable,
                                 revise_prompt, build_aperture)
from columna_server.init.benchmarks import BENCHMARKS, GOLD


@pytest.mark.parametrize("bid", ["B1", "B5", "B8"])
def test_gold_stand_in_passes_end_to_end(bid):
    # the whole pipeline runs against the messy schema via the aperture; a perfect mind passes on turn 1.
    r = run_benchmark(BENCHMARKS[bid], ScriptedProvider(GOLD[bid]), loop_budget=5)
    assert r.passed and r.converged and r.convergence_cost == 1
    if BENCHMARKS[bid].kind == "◆":
        assert r.explicitness                       # the oracle-asymmetric call was surfaced


def test_convergence_cost_counts_iterations_to_pass():
    # a stand-in that whiffs turn 1 (proposes nothing) then emits the gold on the revise turn -> cost 2.
    prov = ScriptedProvider([[], GOLD["B5"][0]])
    r = run_benchmark(BENCHMARKS["B5"], prov, loop_budget=5)
    assert r.passed and r.converged and r.convergence_cost == 2


def test_a_silent_oracle_call_fails_the_benchmark_end_to_end():
    # drop the review_call from B1's gold -> the ◆ basis call is silent -> hard fail, with a narrative.
    silent = [[dict(s) for s in GOLD["B1"][0]]]
    for s in silent[0]:
        s.pop("review_call", None)
    r = run_benchmark(BENCHMARKS["B1"], ScriptedProvider(silent), loop_budget=5)
    assert not r.passed and not r.explicitness and "silent on oracle-asymmetric" in r.failure_narrative


def test_report_renders_a_full_run():
    results = [run_benchmark(BENCHMARKS[b], ScriptedProvider(GOLD[b]), 5) for b in ("B1", "B5", "B8")]
    run = RunRecord(model_id="scripted", model_version="-", sampling={}, harness_config={"aperture_cap": 1000},
                    kp_version="0.1", provider="scripted", results=results)
    report = render_report(run)
    assert "passed 3/3" in report and "B5 ○" in report and "provider=scripted" in report


def test_parse_drops_any_door_from_the_response():
    # the wall on the response side (ruling 2): an opening spec is DROPPED ENTIRELY, not de-flagged —
    # fertility belongs to the adjudicator's advice channel, never a proposal.
    specs = parse_proposals(
        '[{"kind":"measure","target":"m","body":"MEASURE m ..."},'
        ' {"kind":"derived","target":"r","body":"DERIVED r = a/b FERTILE { sum }"},'
        ' {"kind":"fertility","target":"x","body":"anything"},'
        ' {"kind":"derived","target":"o","body":"DERIVED o = a/b","opens_fertility": true}]')
    assert [s["target"] for s in specs] == ["m"]          # only the closure survives; all three doors dropped


def test_parse_rejects_prose_and_malformed():
    for bad in ("not json", '{"kind":"x"}', '[{"body":"no kind"}]'):
        with pytest.raises((ValueError, Exception)):
            parse_proposals(bad)


def test_parse_enforces_kind_and_target_grammar_clauses():
    # unknown kind -> malformed (closed vocabulary)
    with pytest.raises(ValueError):
        parse_proposals('[{"kind":"cast","target":"x","body":"b"}]')
    # verbose target -> malformed (the target-shape clause; NOT laundered scorer-side)
    with pytest.raises(ValueError):
        parse_proposals('[{"kind":"universe","target":"daily_inventory; grain = one row per (store,day)","body":"b"}]')
    # canonical bare name passes; edge needs the arrow, a bare id for an edge is rejected
    assert parse_proposals('[{"kind":"universe","target":"inventory","body":"b"}]')[0]["target"] == "inventory"
    assert parse_proposals('[{"kind":"edge","target":"store->region","body":"b"}]')[0]["target"] == "store->region"
    with pytest.raises(ValueError):
        parse_proposals('[{"kind":"edge","target":"store_region","body":"b"}]')      # edge without an arrow


def test_eval_scores_a_loop_violation_instead_of_crashing():
    # the mind proposes a shape-valid but WRONG closure (struck), then re-proposes it on revise -> the
    # harness law fires; the eval SCORES it (loop_violation=True, censored), never raises (ruling 2).
    from columna_server.init.benchmarks import BENCHMARKS
    bad = {"kind": "edge", "target": "wrong->place", "body": "EDGE wrong -> place ALONG x VIA t(a,b)"}
    prov = ScriptedProvider([[bad], [bad]])       # propose it, then re-propose the struck one
    r = run_benchmark(BENCHMARKS["B5"], prov, loop_budget=5)
    assert r.loop_violation and not r.passed and not r.converged
    assert "struck" in r.failure_narrative


def test_system_prompt_loads_and_forbids_doors():
    sp = system_prompt()
    assert "propose doors NEVER" in sp and "DATA MAY SUGGEST, NEVER GRANT" in sp


def test_revise_prompt_renders_the_struck_marks_to_the_model():
    # BLINDNESS CHECK (Huayin, ruling 4, 2026-07-16): a re-proposal is disobedience (mind) only if the
    # mind SEES what was struck. This pins the seam — the struck body MUST render verbatim, under the
    # do-NOT-re-propose header, with settled-stays-settled restated. If this ever regresses to silence,
    # a struck-re-proposal reattributes to a loop-construction bug (world). HERMETIC — no key, no network.
    from columna_core.draft import Draft, Proposal, STRUCK
    ap = build_aperture(BENCHMARKS["B5"].schema)
    d = Draft(manifold_name="blindness-check")
    d.add(Proposal(kind="edge", target="wrong->place", body="EDGE wrong -> place ALONG x VIA t(a,b)",
                   review=STRUCK))
    d.add(Proposal(kind="measure", target="revenue", body="MEASURE revenue = SUM(amount)",
                   review="accepted"))
    rendered = revise_prompt(ap, d)
    assert "EDGE wrong -> place ALONG x VIA t(a,b)" in rendered      # the struck body, verbatim
    assert "do NOT re-propose" in rendered                          # under the prohibition header
    assert "settled mark stays settled" in rendered                 # the law restated in the turn
    assert "MEASURE revenue = SUM(amount)" in rendered              # accepted marks also rendered (do-not-repeat)


def test_real_provider_refuses_without_a_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ProviderUnavailable):
        AnthropicProvider()                          # the real mind waits for an explicit, keyed go

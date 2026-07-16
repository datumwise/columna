"""
test_init_plumbing.py — the end-to-end init plumbing, HERMETIC (CP-2).

Proves schema → aperture → loop → output → scorer → report end to end with a SCRIPTED stand-in for the
mind (the gold scripts) — the pipeline the first real-model run will walk. Harness behavior only; the
real model runs only on Huayin's explicit go. Also pins the response PARSE (incl. the wall on the
response side) without any network.
"""
import pytest

from columna_server.init import (ScriptedProvider, run_benchmark, render_report, RunRecord,
                                 parse_proposals, system_prompt, AnthropicProvider, ProviderUnavailable)
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


def test_parse_strips_any_door_from_the_response():
    # the wall on the response side: even if the model returns opens_fertility, the parse strips it.
    specs = parse_proposals('[{"kind":"derived","target":"r","body":"DERIVED r = a/b",'
                            ' "opens_fertility": true, "author_declared": true}]')
    assert specs[0].get("opens_fertility") is None and specs[0].get("author_declared") is None


def test_parse_rejects_prose_and_malformed():
    for bad in ("not json", '{"kind":"x"}', '[{"body":"no kind"}]'):
        with pytest.raises((ValueError, Exception)):
            parse_proposals(bad)


def test_system_prompt_loads_and_forbids_doors():
    sp = system_prompt()
    assert "propose doors NEVER" in sp and "DATA MAY SUGGEST, NEVER GRANT" in sp


def test_real_provider_refuses_without_a_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ProviderUnavailable):
        AnthropicProvider()                          # the real mind waits for an explicit, keyed go

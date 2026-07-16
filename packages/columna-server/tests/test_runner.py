"""
test_runner.py — the replicated A/B eval runner, HERMETIC (CP-2.x, ruling 4).

Proves the run-6 SHAPE with a scripted provider factory (no key, no network): two arms, k replicates
per benchmark, durable artifact writing, the aggregate rates table, B10 capture, and the loud infra
abort. Judgment quality is not tested (there is no mind); this validates the runner, not a subject.
"""
import json

import pytest

from columna_server.init import run_replicated_ab, InfraAbort, ScriptedProvider
from columna_server.init.benchmarks import GOLD

ARMS = [{"name": "control", "kp_version": "0.3"}, {"name": "treatment", "kp_version": "0.4"}]
BIDS = ["B1", "B5", "B8", "B10"]                    # a small representative slice for the hermetic test


def _scripted_factory(arm, bid, rep):
    return ScriptedProvider(GOLD.get(bid, [[]]))    # GOLD for B1/B5/B8; empty (fails) for B10


def test_runner_replicates_two_arms_and_writes_durable_artifacts(tmp_path):
    out = tmp_path / "run6"                         # scripted -> the /tmp guard is exempt
    res = run_replicated_ab(arms=ARMS, bids=BIDS, k=2, loop_budget=5, out_dir=str(out),
                            provider_for=_scripted_factory, model_id="scripted",
                            stamp={"run_id": "runX", "run_timestamp": "2026-07-16T00:00:00"})
    # all three artifacts written durably
    for name in ("captured.json", "b10.json", "report.md"):
        assert (out / name).exists()
    # captured carries per-arm, per-rep raw proposals (k=2 each)
    cap = json.loads((out / "captured.json").read_text())
    assert set(cap) == {"control", "treatment"}
    assert len([c for c in cap["control"] if c["bid"] == "B1"]) == 2      # k replicates
    assert cap["control"][0]["proposals"]                                 # raw proposals retained
    # B10 evidence captured for both arms
    b10 = json.loads((out / "b10.json").read_text())
    assert set(b10["arms"]) == {"control", "treatment"} and b10["ground_truth"]["closures"]
    # aggregate rates present; the A/B table rendered
    agg = res["aggregate"]
    assert agg["control"]["rows"]["B1"]["pass_rate"] == 1.0               # GOLD B1 passes every replicate
    assert agg["control"]["rows"]["B8"]["explicit_rate"] is None          # B8 is ○ now (no ◆ explicit rate)
    assert "A/B RATES" in res["report"] and "refutation (B11)" in res["report"]


def test_runner_aborts_loud_on_an_infra_error_never_a_fake_miss(tmp_path):
    # a provider factory that raises == an API/infra blowup -> InfraAbort, no report (run-5's lesson).
    def boom(arm, bid, rep):
        raise RuntimeError("Overloaded")
    with pytest.raises(InfraAbort):
        run_replicated_ab(arms=ARMS, bids=["B1"], k=2, loop_budget=5, out_dir=str(tmp_path / "x"),
                          provider_for=boom, model_id="scripted", stamp={})


def test_runner_refuses_a_temp_out_dir_for_a_real_run():
    # a REAL (non-scripted) run must land durably in-repo (ruling 3) — a /tmp out_dir is refused.
    with pytest.raises(ValueError):
        run_replicated_ab(arms=ARMS, bids=["B1"], k=2, loop_budget=5, out_dir="/tmp/run6",
                          provider_for=_scripted_factory, model_id="claude-opus-4-8", stamp={})

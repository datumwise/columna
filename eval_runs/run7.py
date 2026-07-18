"""
run7.py — the pre-registered concentration-floor test: KP v0.3 (control) vs KP v0.5 (treatment).

Huayin ruling 3 (2026-07-16): n=3 per arm — higher n addresses run-6's single-flip noise inside the
comparison that matters. SHIP CRITERIA are PRE-REGISTERED (fixed before the run, both required):
    (1) flood(mean) <= 4.5     — the concentration win must survive the floor (at/below v0.4's flood)
    (2) ◆-recall(mean) >= 5.0  — the floor must fully protect the sharp calls (at/above v0.3's recall)
If either fails, v0.5 does NOT ship. No post-hoc criteria.

CONTROL = KP v0.3 (git dc83cee), TREATMENT = KP v0.5 (live). Same model + scorer(0.4) + benchmarks
(B8 ○, B10 GT v2). Durable artifacts -> specs/context/run7/. Run with the key inline only:
    ANTHROPIC_API_KEY=... python eval_runs/run7.py            # k=3 default
"""
import subprocess
import sys
import datetime

from columna_server.init import run_replicated_ab, AnthropicProvider

V03_SHA = "dc83cee"                                # KP v0.3 control prompt source
PROMPT_PATH = "packages/columna-server/src/columna_server/init/system_prompt.md"
BIDS = [f"B{i}" for i in range(1, 12)]
K = int(sys.argv[1]) if len(sys.argv) > 1 else 3
OUT = "specs/context/run7"
MODEL = "claude-opus-4-8"
SHIP_FLOOD_MAX = 4.5
SHIP_RECALL_MIN = 5.0

_v03 = None


def v03_prompt():
    global _v03
    if _v03 is None:
        _v03 = subprocess.check_output(["git", "show", f"{V03_SHA}:{PROMPT_PATH}"], text=True)
    return _v03


def provider_for(arm, bid, rep):
    return AnthropicProvider(system=v03_prompt()) if arm["name"] == "control" else AnthropicProvider()


if __name__ == "__main__":
    arms = [{"name": "control", "kp_version": "0.3"}, {"name": "treatment", "kp_version": "0.5"}]
    stamp = {"run_id": "run7", "run_timestamp": datetime.datetime.now().isoformat(timespec="seconds")}
    print(f"RUN 7 — v0.3 vs v0.5  k={K}  PRE-REGISTERED: flood<={SHIP_FLOOD_MAX} AND recall>={SHIP_RECALL_MIN}"
          f"  -> {OUT}", file=sys.stderr)
    res = run_replicated_ab(arms=arms, bids=BIDS, k=K, loop_budget=5, out_dir=OUT,
                            provider_for=provider_for, model_id=MODEL, stamp=stamp)
    print(res["report"])
    t = res["aggregate"]["treatment"]
    flood, recall = t["flood_count_mean"], t["oracle_explicit_mean"]
    ship = (flood <= SHIP_FLOOD_MAX) and (recall >= SHIP_RECALL_MIN)
    verdict = (f"\n{'='*84}\nPRE-REGISTERED SHIP TEST (v0.5):\n"
               f"  (1) flood {flood} <= {SHIP_FLOOD_MAX} : {'PASS' if flood <= SHIP_FLOOD_MAX else 'FAIL'}\n"
               f"  (2) recall {recall} >= {SHIP_RECALL_MIN} : {'PASS' if recall >= SHIP_RECALL_MIN else 'FAIL'}\n"
               f"  VERDICT: {'SHIP v0.5' if ship else 'DO NOT SHIP — Huayin re-tunes or re-runs'}\n{'='*84}")
    print(verdict)
    with open(f"{OUT}/ship_verdict.txt", "w") as f:
        f.write(verdict.strip() + "\n")
    print(f"\nWROTE durable artifacts under {OUT}/ — commit to complete the run (ruling 3).", file=sys.stderr)

"""
run6.py — the batched replicated A/B for KP v0.4 (concentration), Huayin ruling 4.

CONTROL = KP v0.3 (retrieved from git dc83cee), TREATMENT = KP v0.4 (live). Same model + scorer(0.4) +
benchmarks (B1-B11, B8 corrected), k>=2 replicates per (arm, benchmark), one keyed session. Folds the
standing debts in: B10's proposal-vs-truth is captured, loop-violations are counted across replicates.

Run with the key exported inline into THIS process only (never committed, never echoed):
    ANTHROPIC_API_KEY=... python eval_runs/run6.py            # k=2 default
    ANTHROPIC_API_KEY=... python eval_runs/run6.py 3          # k=3

Writes DURABLE artifacts to specs/context/run6/{captured.json,b10.json,report.md} FROM BIRTH (ruling 3);
the run is not complete until they are committed. No key ever touches disk here.
"""
import subprocess
import sys
import datetime

from columna_server.init import run_replicated_ab, AnthropicProvider

V03_SHA = "dc83cee"                                # KP v0.3 control prompt source (pre-v0.4 HEAD)
PROMPT_PATH = "packages/columna-server/src/columna_server/init/system_prompt.md"
BIDS = [f"B{i}" for i in range(1, 12)]
K = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OUT = "specs/context/run6"
MODEL = "claude-opus-4-8"

_v03 = None


def v03_prompt():
    global _v03
    if _v03 is None:
        _v03 = subprocess.check_output(["git", "show", f"{V03_SHA}:{PROMPT_PATH}"], text=True)
    return _v03


def provider_for(arm, bid, rep):
    # control speaks KP v0.3 (from git); treatment speaks the LIVE KP v0.4 (system_prompt() default)
    return AnthropicProvider(system=v03_prompt()) if arm["name"] == "control" else AnthropicProvider()


if __name__ == "__main__":
    arms = [{"name": "control", "kp_version": "0.3"}, {"name": "treatment", "kp_version": "0.4"}]
    stamp = {"run_id": "run6", "run_timestamp": datetime.datetime.now().isoformat(timespec="seconds")}
    print(f"RUN 6 — replicated A/B  k={K}  arms=control(v0.3) vs treatment(v0.4)  -> {OUT}", file=sys.stderr)
    res = run_replicated_ab(arms=arms, bids=BIDS, k=K, loop_budget=5, out_dir=OUT,
                            provider_for=provider_for, model_id=MODEL, stamp=stamp)
    print(res["report"])
    print(f"\nWROTE durable artifacts under {OUT}/ — commit them to complete the run (ruling 3).", file=sys.stderr)

#!/usr/bin/env python3
"""
check_generator_determinism.py — THE FLAP DETECTOR (Huayin, 2026-07-26).

A recorded exhibit is supposed to change ONLY by re-recording. This guard enforces the other half of
that sentence: that it does not change by ITSELF.

WHY THIS EXISTS. The /case reconciliation badge rendered `delta 0.0000` on most runs and `-0.0000` on
roughly one run in five — same package, same input, same machine. Nothing about the data decided it;
float summation order did. It reached a byte-preserved artifact, which means a recorded exhibit was
drifting with no re-recording and no code change: every deploy was a coin flip, and the committed
value was merely the side the coin had landed on in CI. It was flagged at the #85 preview, ordered
fixed in the 0.12.1 cargo, and never landed — it survived a year of releases because NOTHING WAS
LOOKING. The engine-side fix ships in 0.13.1 (`canonical_zero`); this guard is the structural half,
so the CLASS cannot recur silently in any generator.

WHAT IT DOES. Runs each generator TWICE in the same environment and asserts the two outputs are
BYTE-IDENTICAL. Non-determinism becomes a loud, named build failure instead of a surprise that
reaches production in 20% of deploys.

FAIL-CLOSED, and it names its reason (proverb 5, and AW-6's lesson): a non-zero exit with the
generator named and the first differing byte shown — never a sentinel, never a bare traceback.

Two runs catch a coin flip with probability p per run; at p=0.2 a single invocation catches it ~32%
of the time, and across CI runs it becomes a certainty. Raise REPEATS to trade build seconds for
detection power on a rarer flap.

Usage:  python scripts/check_generator_determinism.py [--repeats N] [generator.py ...]
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

# The generators whose output is COMMITTED or SHIPPED — the ones whose determinism is load-bearing.
DEFAULT_GENERATORS = [
    "gen_case.py",
    "gen_transcript.py",
    "gen_universe_visual.py",
    "gen_grammar.py",
]


def run_once(script: pathlib.Path) -> bytes:
    proc = subprocess.run([sys.executable, str(script)], capture_output=True)
    if proc.returncode != 0:
        tail = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-6:]
        raise SystemExit(
            f"FLAP DETECTOR: {script.name} FAILED TO RUN (exit {proc.returncode}) — cannot assess\n"
            f"determinism of a generator that does not complete.\n  " + "\n  ".join(tail)
        )
    return proc.stdout


def first_difference(a: bytes, b: bytes) -> str:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            lo = max(0, i - 90)
            return (f"first differing byte at offset {i}\n"
                    f"    run 1: …{a[lo:i + 90].decode('utf-8', 'replace')}\n"
                    f"    run 2: …{b[lo:i + 90].decode('utf-8', 'replace')}")
    return f"outputs differ in LENGTH only: {len(a)} vs {len(b)} bytes"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=2,
                    help="runs per generator (default 2 — the minimum that can detect a flap)")
    ap.add_argument("generators", nargs="*", default=None)
    args = ap.parse_args()

    names = args.generators or DEFAULT_GENERATORS
    failures = []

    for name in names:
        script = HERE / name
        if not script.exists():
            failures.append(f"{name}: NOT FOUND at {script}")
            print(f"  MISSING  {name}", flush=True)
            continue

        outputs = [run_once(script) for _ in range(max(2, args.repeats))]
        baseline = outputs[0]
        drifted = next((o for o in outputs[1:] if o != baseline), None)

        if drifted is None:
            print(f"  STABLE   {name}  ({len(baseline)} bytes, {len(outputs)} runs byte-identical)", flush=True)
        else:
            print(f"  FLAPPING {name}", flush=True)
            failures.append(f"{name} is NON-DETERMINISTIC\n    {first_difference(baseline, drifted)}")

    if failures:
        print("\nFLAP DETECTOR FAILED — a generator whose output is committed or shipped is not "
              "reproducible.\nA recorded exhibit must change ONLY by re-recording; one that changes "
              "by itself makes\nevery diff untrustworthy and every deploy a coin flip.\n", file=sys.stderr)
        for f in failures:
            print(f"  · {f}", file=sys.stderr)
        print("\nFix the SOURCE of the non-determinism (ordering, float summation, hash iteration, "
              "timestamps).\nDo NOT pin threading to hide it — that suppresses the symptom and leaves "
              "the class alive.", file=sys.stderr)
        return 1

    print(f"\nFLAP DETECTOR GREEN — {len(names)} generator(s) reproducible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

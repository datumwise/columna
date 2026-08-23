#!/usr/bin/env python3
"""
check_generator_determinism.py — THE FLAP DETECTOR (Huayin, 2026-07-26).

A recorded exhibit is supposed to change ONLY by re-recording. This guard enforces the other half of
that sentence: that it does not change by ITSELF.

WHY THIS EXISTS. The /case reconciliation badge rendered `delta 0.0000` on most runs and `-0.0000` on
roughly one in five — same package, same input, same machine. Nothing about the data decided it; float
summation order did. It reached a byte-preserved artifact, so a recorded exhibit was drifting with no
re-recording and no code change: every deploy was a coin flip, and the committed value was merely the
side the coin had landed on in CI. Flagged at the #85 preview, ordered fixed in the 0.12.1 cargo, and
never landed — it survived releases because NOTHING WAS LOOKING. Fixed at the cause in core 0.13.1
(`canonical_delta`); this guard is the structural half, so the CLASS cannot recur silently.

ON ITS FIRST REAL RUN it caught a bigger fish than it was built for: `gen_transcript.py` is
non-deterministic for two reasons that are NOT recording defects but ENGINE defects — see OF-23.

THE ADMISSION TEST FOR GUARDS (minted 2026-07-26, from this guard's own failure): a guard ships only
after running against THE FULL SET IT GUARDS, not the path its author chose. This file was verified
against `gen_case.py` alone and wired into the deploy; it then failed the deploy on `gen_transcript.py`
— correctly, but as a surprise to its own author, who had just written the proverb about exactly this.

DECLARED EXCLUSIONS, not normalizations. Some variance is legitimate: a timestamp is SUPPOSED to
change. Those fields are excluded EXPLICITLY, per generator, and the exclusion is PRINTED on every run
("comparing modulo: …") so that legitimate variance is DECLARED variance and the exclusion set cannot
grow silently. A guard should say what it knows it is ignoring.

ROWED EXEMPTIONS, not whitelists. A flap too large to fix in the PR that found it does not get a quiet
pass; it gets a ledger row and an entry here. The guard then PRINTS it loudly every run and FAILS if the
named row is missing or no longer OPEN — so the exemption cannot outlive its row. Same convention as
scripts/check_purged_grammar.py. "Rulings that aren't tracked didn't happen."

WHY NOT JUST PIN OR EXCLUDE THE FLAP: it would make the RECORDING more deterministic than the ENGINE,
which is a lie about the product. The honest interim state is a VISIBLE EXEMPTION over a TRUE
INSTABILITY.

FAIL-CLOSED, naming its reason: a non-zero exit with the generator named and the first differing byte
shown — never a sentinel, never a bare traceback.

Usage:  python scripts/check_generator_determinism.py [--repeats N] [generator.py ...]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]

DEFAULT_GENERATORS = [
    "gen_case.py",
    "gen_firstlight.py",
    "gen_transcript.py",
    "gen_universe_visual.py",
    "gen_grammar.py",
]

# DECLARED EXCLUSIONS — dotted paths into the emitted JSON whose variance is LEGITIMATE. Printed every
# run. Adding one is a visible act, and it must be justified in the comment beside it.
EXCLUSIONS: dict[str, list[str]] = {
    # A build timestamp is supposed to change. It is not evidence of anything about the data.
    "gen_transcript.py": ["meta.generated_at"],
}

# ROWED EXEMPTIONS — real, tracked instability. Valid only while the named row is present AND OPEN.
ROWED: dict[str, str] = {
    # OF-23 — DETERMINISTIC SERVING. Not a recording defect: the ENGINE serves nondeterministic bytes.
    # (a) seeded result ROW ORDER permutes between identical asks; (b) 1-ULP float drift reaches SERVED
    # values (130.30240066225167 vs …64), which the 0.13.1 tolerance doctrine explicitly does NOT cover
    # — there is no declared tolerance on a served measure. The recording pipeline merely made it
    # visible. Fix is a design fork (canonical coordinate ordering at the serialization boundary;
    # summation-order drift needs a desk proposal). Thread-pinning stays REJECTED as symptom
    # suppression.
    "gen_transcript.py": "OF-23",
}

LEDGERS_FOR_ROWS = [ROOT / "specs" / "open_forks.md", ROOT / "specs" / "doctrine_gaps.md"]


def ledger_has_open(row_id: str) -> bool:
    """A rowed exemption is valid only while its row is present AND still OPEN in a ledger."""
    for ledger in LEDGERS_FOR_ROWS:
        if not ledger.exists():
            continue
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if re.search(rf"\b{re.escape(row_id)}\b", line) and "**OPEN**" in line:
                return True
    return False


def run_once(script: pathlib.Path) -> bytes:
    proc = subprocess.run([sys.executable, str(script)], capture_output=True)
    if proc.returncode != 0:
        tail = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-6:]
        raise SystemExit(
            f"FLAP DETECTOR: {script.name} FAILED TO RUN (exit {proc.returncode}) — cannot assess\n"
            f"determinism of a generator that does not complete.\n  " + "\n  ".join(tail)
        )
    return proc.stdout


def strip_excluded(raw: bytes, paths: list[str]) -> bytes:
    """Blank the DECLARED-exclusion paths so comparison ignores legitimate variance only."""
    if not paths:
        return raw
    try:
        doc = json.loads(raw)
    except Exception:
        return raw                      # not JSON: compare raw, exclusions cannot apply
    for dotted in paths:
        node, *rest = dotted.split(".")
        cur = doc
        keys = [node, *rest]
        for k in keys[:-1]:
            if not isinstance(cur, dict) or k not in cur:
                cur = None
                break
            cur = cur[k]
        if isinstance(cur, dict) and keys[-1] in cur:
            cur[keys[-1]] = "<excluded-by-declaration>"
    return json.dumps(doc, sort_keys=True).encode()


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
    failures, rowed_hits = [], []

    for name in names:
        script = HERE / name
        if not script.exists():
            failures.append(f"{name}: NOT FOUND at {script}")
            print(f"  MISSING  {name}", flush=True)
            continue

        excl = EXCLUSIONS.get(name, [])
        modulo = f"  (comparing modulo: {', '.join(excl)})" if excl else ""

        outputs = [strip_excluded(run_once(script), excl) for _ in range(max(2, args.repeats))]
        baseline = outputs[0]
        drifted = next((o for o in outputs[1:] if o != baseline), None)

        if drifted is None:
            print(f"  STABLE   {name}  ({len(baseline)} bytes, {len(outputs)} runs byte-identical)"
                  f"{modulo}", flush=True)
            # A rowed exemption naming a now-stable generator would report it as unstable forever.
            if name in ROWED:
                failures.append(
                    f"{name} is STABLE but still carries a ROWED exemption ({ROWED[name]}). "
                    f"Remove the ROWED entry and close the row — an exemption over a fixed defect "
                    f"reports a healthy generator as broken forever."
                )
            continue

        row_id = ROWED.get(name)
        if row_id and ledger_has_open(row_id):
            print(f"  FLAPPING {name}  — ROWED {row_id}, tracked and OPEN{modulo}", flush=True)
            rowed_hits.append(f"{name} ({row_id})\n    {first_difference(baseline, drifted)}")
        elif row_id:
            print(f"  FLAPPING {name}  — ROWED {row_id} but the row is MISSING or no longer OPEN",
                  flush=True)
            failures.append(
                f"{name} still flaps, but its row {row_id} is missing or already closed in the "
                f"ledgers. The exemption cannot outlive its row: either reopen {row_id} or fix the "
                f"non-determinism.\n    {first_difference(baseline, drifted)}"
            )
        else:
            print(f"  FLAPPING {name}{modulo}", flush=True)
            failures.append(f"{name} is NON-DETERMINISTIC\n    {first_difference(baseline, drifted)}")

    if rowed_hits:
        print("\n  ROWED INSTABILITY — tracked, NOT forgiven. Loud on every run by design:",
              flush=True)
        for r in rowed_hits:
            print(f"    · {r}", flush=True)

    if failures:
        print("\nFLAP DETECTOR FAILED — a generator whose output is committed or shipped is not "
              "reproducible.\nA recorded exhibit must change ONLY by re-recording; one that changes "
              "by itself makes\nevery diff untrustworthy and every deploy a coin flip.\n",
              file=sys.stderr)
        for f in failures:
            print(f"  · {f}", file=sys.stderr)
        print("\nFix the SOURCE of the non-determinism (ordering, float summation, hash iteration, "
              "timestamps).\nDo NOT pin threading or widen the exclusions to hide it: that suppresses "
              "the symptom, and it\nwould make the RECORDING more deterministic than the ENGINE — a "
              "lie about the product.", file=sys.stderr)
        return 1

    n_rowed = len(rowed_hits)
    print(f"\nFLAP DETECTOR GREEN — {len(names)} generator(s) checked"
          + (f", {n_rowed} with a tracked ROWED exemption." if n_rowed else ", all reproducible."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

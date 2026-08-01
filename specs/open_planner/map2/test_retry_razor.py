#!/usr/bin/env python3
"""MAP-2 · Beat 3 amendment — the NEGATIVE TEST of the execution-error retry razor (schema v0.3 M3).

    DUCKDB_CONSUMER_PYTHON=<ddb113>/bin/python \\
        python specs/open_planner/map2/test_retry_razor.py specs/open_planner/map2/

THE RAZOR (ruled 2026-08-01, normative): retry is licensed for the EXECUTION-ERROR class ONLY; a
COMPARISON MISMATCH MAY NEVER RETRY. This test keeps that honest, in the suite:

  • NEGATIVE (the one Huayin required): a PLANTED value-mismatch — the C1 sum plan DOUBLED (a lawful plan
    that returns wrong numbers) consumed against the CORRECT oracle — must FAIL, and must fail WITHOUT a
    second chance: `pass == False` AND `execution_attempts == 1`. The plan executes once (no execution
    error to retry); the mismatch is caught in the comparison, which never re-enters execution.
  • POSITIVE control: the correct C1 sum plan against its oracle — `pass == True` (the razor does not
    break the happy path).

A test that has never failed has not been shown to be able to fail; a razor that never demonstrably
refuses a wrong number has not been shown to cut. Exit 0 iff both cases hold.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cert_v0_2 as C                                                    # noqa: E402
from oracle_harness import oracle                                       # noqa: E402
from pilot_c1 import _t, _load_tables                                    # noqa: E402

DDB_PY = os.environ.get("DUCKDB_CONSUMER_PYTHON", "/tmp/ddbtest/bin/python")


def _consume(plan_bytes, oracle_map, wh, tmp, tag):
    (tmp / f"{tag}.substrait").write_bytes(plan_bytes)
    json.dump(oracle_map, open(tmp / f"{tag}.oracle.json", "w"))
    out = subprocess.run([DDB_PY, str(pathlib.Path(__file__).parent / "duckdb_consumer.py"),
                          str(tmp / f"{tag}.substrait"), str(tmp / f"{tag}.oracle.json"), wh, "cal.month"],
                         capture_output=True, text=True)
    return json.loads(out.stdout.strip().splitlines()[-1]) if out.returncode == 0 else {"pass": False, "err": out.stderr[-200:]}


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    from columna_server.demo import demo_store, demo_dir
    store = demo_store()
    wh = str(pathlib.Path(demo_dir()) / "cascadia" / "warehouse")
    tmp = pathlib.Path(argv[1]) / "fixtures" / "_razor_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    tables = _load_tables()
    t, cal = _t(tables)

    ref, _ = oracle(store, "cascadia", "SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}")
    oracle_map = {r[0]: r[-1] for r in ref.iter_rows()}

    # POSITIVE control — the correct C1 sum plan
    good = (t.inner_join(cal, t.day == cal.day).select(t.store_id, t.product_id, t.amount, cal.month)
             .group_by(["store_id", "product_id", "month"]).aggregate(v=lambda x: x.amount.sum())
             .group_by("month").aggregate(v=lambda x: x.v.sum()))
    good_plan, _ = C.compile_substrait(good)
    pos = _consume(good_plan.SerializeToString(), oracle_map, wh, tmp, "positive")

    # NEGATIVE — the C1 sum plan DOUBLED: a lawful plan returning WRONG numbers, vs the CORRECT oracle
    agg = (t.inner_join(cal, t.day == cal.day).select(t.store_id, t.product_id, t.amount, cal.month)
            .group_by(["store_id", "product_id", "month"]).aggregate(v=lambda x: x.amount.sum())
            .group_by("month").aggregate(v=lambda x: x.v.sum()))
    bad = agg.select(agg.month, (agg.v * 2.0).name("v"))
    bad_plan, _ = C.compile_substrait(bad)
    neg = _consume(bad_plan.SerializeToString(), oracle_map, wh, tmp, "negative")

    print("POSITIVE control (correct plan):", {"pass": pos.get("pass"), "attempts": pos.get("execution_attempts")})
    print("NEGATIVE (planted value-mismatch):", {"pass": neg.get("pass"),
          "attempts": neg.get("execution_attempts"), "worst_delta": neg.get("worst_delta")})

    positive_ok = pos.get("pass") is True
    # the razor: the mismatch FAILS, and did so with EXACTLY ONE execution attempt — no second chance.
    negative_ok = (neg.get("pass") is False) and (neg.get("execution_attempts") == 1)
    ok = positive_ok and negative_ok
    print("\nRETRY RAZOR:", "UPHELD — a value-mismatch fails without a second chance (execution_attempts==1); "
          "the happy path still passes." if ok else
          "VIOLATED — the razor did not cut as ruled.")
    result = {"razor": "execution-error retry only; comparison mismatch never retries",
              "positive_control_pass": positive_ok, "negative_fails_without_retry": negative_ok,
              "negative_detail": {"pass": neg.get("pass"), "execution_attempts": neg.get("execution_attempts"),
                                  "worst_delta": neg.get("worst_delta")}, "upheld": ok}
    (pathlib.Path(argv[1]) / "fixtures" / "retry_razor_negative_test.json").write_text(
        json.dumps(result, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

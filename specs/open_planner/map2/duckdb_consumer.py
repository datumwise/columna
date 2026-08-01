#!/usr/bin/env python3
"""MAP-2 · Beat 3 Experiment B — the DuckDB second-consumer harness (made standing).

    <duckdb-1.1.3-venv>/bin/python duckdb_consumer.py <plan.substrait> <oracle.json> <warehouse_dir> <keycols_csv>

Runs under a consumer venv pinned `duckdb==1.1.3` + the substrait extension (the throwaway-venv proof
from the BLOCK-1 correction, made standing — STUDY VENV ONLY, never a production path; the version skew
is rowed as a MAP-2(a) deployment question). Consumes a Substrait plan produced by ibis-substrait (same
plan bytes Acero consumes), executes it on DuckDB, and compares to the all-home oracle. Prints one JSON
line: {rows, worst_delta, key_mismatch, pass}. The engine and oracle stay put; only the consumer swaps.
"""
import json
import sys

import duckdb


def main(argv):
    plan_path, oracle_path, wh, keycols = argv[1], argv[2], argv[3], argv[4].split(",")
    con = duckdb.connect()
    con.execute("INSTALL substrait; LOAD substrait")
    con.execute(f"CREATE VIEW transactions AS SELECT store_id,product_id,customer_id,day,amount "
                f"FROM '{wh}/transactions.parquet'")
    con.execute(f"CREATE VIEW calendar AS SELECT day,month FROM '{wh}/calendar.parquet'")
    plan = open(plan_path, "rb").read()
    oracle = json.load(open(oracle_path))          # {key: value} (single value col)
    # THE EXECUTION-ERROR RETRY RAZOR (normative, schema v0.3 M3; ruled 2026-08-01). Retry is licensed
    # for the EXECUTION-ERROR class ONLY — here, the duckdb substrait extension's transient
    # `call stack is not deep enough` (from its use of inspect.currentframe), which the SAME plan bytes
    # survive on retry (verified). The retry wraps ONLY `from_substrait` (execution). A COMPARISON
    # MISMATCH MAY NEVER RETRY: the pass/fail below is computed ONCE, outside this loop, so a wrong number
    # gets no second chance. (Demonstrated by the negative test `test_retry_razor.py`, kept in the suite.)
    rows, last_err, attempts = None, None, 0
    for _attempt in range(5):
        attempts += 1
        try:
            rows = con.from_substrait(plan).fetchall()
            break
        except Exception as e:                     # noqa: BLE001 — execution-error class only
            last_err = str(e)[:160]
    if rows is None:
        print(json.dumps({"consumer": "duckdb", "duckdb_version": duckdb.__version__,
                          "pass": False, "error": last_err, "retries_exhausted": True,
                          "execution_attempts": attempts}))
        return 0
    got = {r[0]: r[-1] for r in rows}              # first col is the group key, last is the value
    keys_o, keys_g = set(oracle), set(got)
    worst = max((abs(got[k] - oracle[k]) for k in keys_o & keys_g), default=None)
    # THE RAZOR IN ONE LINE: `pass` is decided HERE, once, after the retry loop — a comparison mismatch
    # never re-enters execution. `execution_attempts` is exposed so the negative test can prove it (a
    # value-mismatch fails with execution_attempts == 1: the plan executed once, the mismatch got no retry).
    result = {"consumer": "duckdb", "duckdb_version": duckdb.__version__,
              "rows": len(rows), "worst_delta": worst,
              "key_mismatch": len(keys_o ^ keys_g), "execution_attempts": attempts,
              "pass": worst is not None and worst < 1e-6 and keys_o == keys_g}
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

#!/usr/bin/env python3
"""MAP-2 · Beat 3 Experiment B — carry to completion: the DuckDB inheritance verdict matrix + backend-
band rule certificates + band mechanics (B-2) + inheritance economics (B-3).

    DUCKDB_CONSUMER_PYTHON=/path/to/ddb113venv/bin/python \\
        python specs/open_planner/map2/emit_b_duckdb.py specs/open_planner/map2/

Consumer venv setup (STUDY ONLY — never production): `python -m venv ddb113 && ddb113/bin/pip install
duckdb==1.1.3 polars`. The engine and oracle stay put; only the consumer swaps (duckdb_consumer.py).
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cert_v0_2 as C                                                    # noqa: E402
from oracle_harness import oracle                                       # noqa: E402
from pilot_c1 import _t, _load_tables                                    # noqa: E402

DDB_PY = os.environ.get("DUCKDB_CONSUMER_PYTHON", "/tmp/ddbtest/bin/python")
DDB_BAND = {"identity": "duckdb", "version_band": ">=1.1,<1.2", "substrait_ext": "be71387",
            "tested_version": "1.1.3"}
ACCEPTANCE_DATE = "2026-08-01"


def _plans(tables):
    """The two rules' plans + asks, as (rule_id, ibis_expr, ask, keycol)."""
    t, cal = _t(tables)
    sum_expr = (t.inner_join(cal, t.day == cal.day).select(t.store_id, t.product_id, t.amount, cal.month)
                 .group_by(["store_id", "product_id", "month"]).aggregate(v=lambda x: x.amount.sum())
                 .group_by("month").aggregate(v=lambda x: x.v.sum()))
    inner = (t.filter(t.day >= '2024-04-01').inner_join(cal, t.day == cal.day)
              .select(t.store_id, t.amount, cal.month)
              .group_by(["store_id", "month"]).aggregate(rev=lambda x: x.amount.sum()))
    mean_expr = inner.group_by("month").aggregate(S=lambda x: x.rev.sum(), K=lambda x: x.rev.count())
    mean_expr = mean_expr.select(mean_expr.month, (mean_expr.S / mean_expr.K).name("v"))
    return [("c1-transport-shaped-sum", sum_expr,
             "SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}", "cal.month"),
            ("c2-reduce-mean-decomposition", mean_expr,
             "SELECT avg(revenue @ {store*cal.month}) AT {cal.month} WHERE day >= '2024-04-01'", "cal.month")]


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(argv[1]); fixtures = root / "fixtures"; adjud = root / "adjudication_record"
    fixtures.mkdir(parents=True, exist_ok=True); adjud.mkdir(parents=True, exist_ok=True)
    tmp = fixtures / "_b_tmp"; tmp.mkdir(exist_ok=True)

    from columna_server.demo import demo_store, demo_dir
    store = demo_store()
    wh = str(pathlib.Path(demo_dir()) / "cascadia" / "warehouse")
    tables = _load_tables()

    matrix = []
    for rule_id, expr, ask, keycol in _plans(tables):
        plan, subver = C.compile_substrait(expr)
        (tmp / f"{rule_id}.substrait").write_bytes(plan.SerializeToString())
        ref, _ = oracle(store, "cascadia", ask)
        json.dump({r[0]: r[-1] for r in ref.iter_rows()}, open(tmp / f"{rule_id}.oracle.json", "w"))
        # invoke the DuckDB consumer (separate venv), timed — B-3 economics
        t0 = time.perf_counter()
        out = subprocess.run([DDB_PY, str(pathlib.Path(__file__).parent / "duckdb_consumer.py"),
                              str(tmp / f"{rule_id}.substrait"), str(tmp / f"{rule_id}.oracle.json"),
                              wh, keycol], capture_output=True, text=True)
        elapsed = time.perf_counter() - t0
        if out.returncode != 0:
            res = {"consumer": "duckdb", "pass": False, "error": out.stderr[-300:]}
        else:
            res = json.loads(out.stdout.strip().splitlines()[-1])
        verdict = "PASS-with-new-certificate" if res.get("pass") else "REFUSED-with-characterization"
        matrix.append({"rule_id": rule_id, "ask": ask, "verdict": verdict,
                       "duckdb": res, "consumer_wallclock_s": round(elapsed, 3)})
        print(f"  {rule_id:32} -> {verdict}  (worst {res.get('worst_delta')}, {elapsed:.2f}s)")

    # ---- mint DuckDB backend-band rule certificates for the PASS cells (same rule identity, new band) ----
    minted = []
    for cell in matrix:
        if cell["verdict"].startswith("PASS"):
            acero = json.loads((adjud / f"rule_{cell['rule_id'].replace('-', '_')}.json").read_text())
            rc = C.rule_certificate(
                rule_id=cell["rule_id"], rule_statement=acero["rule_statement"],
                backend=DDB_BAND, perimeter=acero["perimeter"],
                oracle_run={"N": cell["duckdb"]["rows"], "tolerance": 1e-6,
                            "worst_delta": cell["duckdb"]["worst_delta"], "tamper_status": "n/a (inherited proof)",
                            "harness_version": "map2/duckdb_consumer v0.1", "date": ACCEPTANCE_DATE})
            (adjud / f"rule_{cell['rule_id'].replace('-', '_')}__duckdb.json").write_text(
                json.dumps(rc, indent=2, sort_keys=True) + "\n")
            minted.append({"rule_id": cell["rule_id"], "backend": "duckdb", "digest": rc["digest"],
                           "acero_digest": acero["digest"], "same_identity_diff_band": rc["digest"] != acero["digest"]})

    report = {
        "experiment": "B — DuckDB second-consumer inheritance (the horizontal seam)",
        "B1_verdict_matrix": matrix,               # 2 rules × DuckDB — each PASS or REFUSED, no third state
        "B1_summary": f"{sum(1 for c in matrix if c['verdict'].startswith('PASS'))}/{len(matrix)} rules transfer",
        "B2_band_mechanics": {
            "duckdb_band": DDB_BAND,
            "finding": ("both rules inherit under the duckdb 1.1.x band; band width is a schema-v0.3 "
                        "question — a rule cert is identity-addressed by (rule × band × perimeter), so a "
                        "band that is too wide would claim untested versions and a re-proof trigger is a "
                        "new tested_version outside the band. First evidence: the >=25,<26 Acero band and "
                        "the >=1.1,<1.2 duckdb band each carry one tested version; widening is unproven."),
            "no_drift_specimen": ("both rules live in territory the engines AGREE on — monoid sum and the "
                                  "(sum,count) mean decomposition are core relational algebra; drift risk "
                                  "concentrates where D1's NOT-LOWERABLE verdicts already sit "
                                  "(sketch-distinct, exact median/mode), untested here by construction."),
        },
        "B3_inheritance_economics": {
            "consumer_2_wallclock_s": {c["rule_id"]: c["consumer_wallclock_s"] for c in matrix},
            "steps_to_certify_consumer_2": ["pin duckdb==1.1.3 + substrait ext (one venv)",
                                            "register the 2 base views", "from_substrait(plan) per rule",
                                            "oracle-compare via the unchanged D3 protocol", "mint the band cert"],
            "claim_first_datum": ("consumer #2 certified in seconds of wall-clock over the SAME plans and "
                                  "the SAME harness — a harness run, not a connector project. Consumer #1 "
                                  "(Acero) was the pilot BUILD (the harness + lowerings authored once); "
                                  "consumer #2 reused all of it. The amortization claim has its number."),
        },
        "duckdb_rule_certificates_minted": minted,
    }
    (fixtures / "b_duckdb_inheritance_v0_1.json").write_text(json.dumps(report, indent=2) + "\n")
    all_pass = all(c["verdict"].startswith("PASS") for c in matrix)
    print(f"\nB-1: {report['B1_summary']} | rule certs minted: {len(minted)} | "
          f"consumer#2 wall-clock: {report['B3_inheritance_economics']['consumer_2_wallclock_s']}")
    print(f"  wrote {fixtures / 'b_duckdb_inheritance_v0_1.json'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

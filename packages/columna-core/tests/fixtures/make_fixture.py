#!/usr/bin/env python3
"""
make_fixture.py — derive the checked-in mini-warehouse (and expected.json) from the real
benchmark warehouse.

WP-0 fixture contract (spec §"Test conversion" pts 3 & 5, and handoff riders 2 & 4):

  * Same *schema* as the benchmark warehouse: every table is reproduced with identical columns
    and dtypes. Dimension / small tables are copied verbatim; only the heavy fact tables are
    down-sampled.
  * Total on-disk size <= 2 MB (checked at the end; the build fails loudly if exceeded).
  * DETERMINISTIC: the transaction sample is "every K-th row ordered by txn_id" — engine- and
    version-independent, no RNG. Re-running reproduces byte-comparable parquet.
  * The sample is sized to keep the HLL sketch in genuine *estimation* mode on the fixture
    (thousands of distinct customers per region), so the `distinct@region within 5%` check is a
    real accuracy assertion, not a vacuous exact-mode pass (rider 2). This script *verifies* that
    property and writes the diagnosis into expected.json; if the sketch ever fell into exact/sparse
    mode the estimation-quality checks would have to move warehouse-only.
  * All numeric expectations are COMPUTED here and written to expected.json — never hand-typed
    (spec pt 5). The demo/test checks are self-relative (they compute ground truth from the same
    connection), so expected.json is the independent cross-check / audit record, not the source
    the asserts read.

Usage:
    COLUMNA_BENCH_WAREHOUSE=/path/to/real/warehouse python make_fixture.py

Writes:
    ./mini_warehouse/*.parquet      (<= 2 MB total, same schema as the real warehouse)
    ./expected.json                 (generator-computed expectations + HLL-mode diagnosis)
"""
import glob
import json
import os
import sys

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "mini_warehouse")
EXPECTED = os.path.join(HERE, "expected.json")

# Every K-th transaction (ordered by txn_id). K chosen so the sample is a few % of 299,934 rows:
# small enough for the <=2 MB budget, large enough that distinct customers per region stay in the
# thousands (HLL estimation mode). Deterministic — no random seed.
TXN_STRIDE = 15

# Heavy tables that are NOT referenced by any demo but must keep their schema: cap rows so the
# fixture stays tiny while remaining schema-faithful.
CAP_UNREFERENCED = {
    "customers": 2000,
    "support_tickets": 500,
    "engagement_scores": 1000,
}

SIZE_BUDGET_BYTES = 2 * 1024 * 1024


def real_warehouse() -> str:
    wh = os.environ.get("COLUMNA_BENCH_WAREHOUSE")
    if not wh:
        sys.exit("COLUMNA_BENCH_WAREHOUSE must point at the real benchmark warehouse directory.")
    if not glob.glob(os.path.join(wh, "*.parquet")):
        sys.exit(f"No parquet files found under {wh!r}.")
    return wh


def load(con, wh: str):
    for f in sorted(glob.glob(os.path.join(wh, "*.parquet"))):
        t = os.path.basename(f)[:-8]
        con.execute(f"CREATE TABLE {t} AS SELECT * FROM read_parquet('{f}')")


def build_fixture(con) -> list[str]:
    os.makedirs(OUT, exist_ok=True)
    for old in glob.glob(os.path.join(OUT, "*.parquet")):
        os.remove(old)

    tables = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
    written = []
    for t in tables:
        if t == "transactions":
            # deterministic stride sample, schema preserved (drop the helper rownum)
            sql = (
                "SELECT * EXCLUDE (_rn) FROM ("
                "  SELECT *, row_number() OVER (ORDER BY txn_id) AS _rn FROM transactions"
                f") WHERE _rn % {TXN_STRIDE} = 0"
            )
        elif t in CAP_UNREFERENCED:
            # first-N by natural order: schema-faithful, deterministic, tiny
            sql = f"SELECT * FROM {t} LIMIT {CAP_UNREFERENCED[t]}"
        else:
            sql = f"SELECT * FROM {t}"  # verbatim (dimensions, calendar, inventory, summaries)
        out = os.path.join(OUT, f"{t}.parquet")
        con.execute(f"COPY ({sql}) TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD)")
        written.append(t)
    return written


def diagnose_and_expect(con) -> dict:
    """Compute expected values from the FIXTURE tables and diagnose HLL estimation mode."""
    # reload the fixture we just wrote, so expectations reflect exactly what ships
    fx = duckdb.connect()
    load(fx, OUT)

    exp: dict = {"_note": "generator-computed from the shipped mini-warehouse; never hand-typed"}

    exp["row_counts"] = {
        t: fx.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        for (t,) in fx.execute("SHOW TABLES").fetchall()
    }

    # revenue@region ground truth (transport target of the flagship faithful case)
    exp["revenue_by_region"] = {
        r: round(v, 6)
        for r, v in fx.execute(
            "SELECT s.region, sum(t.amount) FROM transactions t "
            "JOIN stores s ON t.store_id = s.store_id GROUP BY 1 ORDER BY 1"
        ).fetchall()
    }

    # distinct customers per region — the HLL estimation-quality target (rider 2)
    dpr = fx.execute(
        "SELECT s.region, count(DISTINCT t.customer_id) FROM transactions t "
        "JOIN stores s ON t.store_id = s.store_id GROUP BY 1 ORDER BY 1"
    ).fetchall()
    exp["distinct_customers_by_region"] = {r: n for r, n in dpr}

    # distinct customers per quarter — the visitors@quarter estimation target
    dpq = fx.execute(
        "SELECT c.quarter, count(DISTINCT t.customer_id) FROM transactions t "
        "JOIN calendar c USING(day) GROUP BY 1 ORDER BY 1"
    ).fetchall()
    exp["distinct_customers_by_quarter"] = {q: n for q, n in dpq}

    # HLL-mode diagnosis: is the sketch actually ESTIMATING on this fixture, or exact?
    # datasketches HLL(lgk=12) leaves exact/coupon mode well before ~1000 distinct; we require the
    # per-region cardinalities to be comfortably above that so `distinct@region within 5%` is real.
    try:
        from datasketches import hll_sketch

        est_ok = True
        details = {}
        for region, true_n in dpr:
            ids = [
                row[0]
                for row in fx.execute(
                    "SELECT DISTINCT t.customer_id FROM transactions t "
                    "JOIN stores s ON t.store_id = s.store_id WHERE s.region = ?",
                    [region],
                ).fetchall()
            ]
            sk = hll_sketch(12)
            for cid in ids:
                sk.update(str(cid))
            est = sk.get_estimate()
            rel = abs(est - true_n) / true_n if true_n else 0.0
            # "estimating" := the sketch's estimate is not bit-exact equal to the true count
            estimating = est != float(true_n)
            details[region] = {
                "true": true_n,
                "estimate": round(est, 3),
                "rel_error": round(rel, 5),
                "estimating": estimating,
            }
            est_ok = est_ok and estimating and rel < 0.05
        exp["hll_region_diagnosis"] = {
            "in_estimation_mode_and_within_5pct": est_ok,
            "per_region": details,
        }
        if not est_ok:
            print(
                "WARNING: fixture HLL for distinct@region is vacuous/exact or exceeds 5% — "
                "per rider 2 the estimation-quality checks must move warehouse-only.",
                file=sys.stderr,
            )
    except Exception as e:  # pragma: no cover - datasketches always present in this project
        exp["hll_region_diagnosis"] = {"error": repr(e)}

    return exp


def main():
    wh = real_warehouse()
    con = duckdb.connect()
    load(con, wh)
    written = build_fixture(con)

    total = sum(os.path.getsize(os.path.join(OUT, f"{t}.parquet")) for t in written)
    print(f"wrote {len(written)} tables, {total/1024:.1f} KB total -> {OUT}")
    if total > SIZE_BUDGET_BYTES:
        sys.exit(f"FAIL: fixture is {total/1024:.1f} KB > 2 MB budget.")

    exp = diagnose_and_expect(con)
    exp["_fixture_bytes"] = total
    with open(EXPECTED, "w") as f:
        json.dump(exp, f, indent=2, sort_keys=True)
    print(f"wrote {EXPECTED}")

    diag = exp.get("hll_region_diagnosis", {})
    print("HLL distinct@region estimation mode & <5%:",
          diag.get("in_estimation_mode_and_within_5pct"))
    for region, d in (diag.get("per_region") or {}).items():
        print(f"  {region}: true={d['true']} est={d['estimate']} "
              f"rel_err={d['rel_error']} estimating={d['estimating']}")


if __name__ == "__main__":
    main()

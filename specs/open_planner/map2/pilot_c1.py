#!/usr/bin/env python3
"""MAP-2 · D4 — the C1 pilot: a certified lowering of the TRANSPORT-shaped composition.

    python specs/open_planner/map2/pilot_c1.py specs/open_planner/map2/fixtures/

The beat's execution evidence (charter §4 D4). ONE Columna plan —
`sum(revenue @ {store*product*cal.month}) AT {cal.month}` (the TRANSPORT-shaped join-and-regroup) —
lowered to a Substrait 0.46.0 plan, executed on **Acero** (`pyarrow.substrait`, the ruled first
consumer), and oracle-compared through D3's harness against the shipped Polars engine.

ACCEPTANCE (charter §5(4), ruled 2026-07-31):
  • N >= 30 comparisons, ZERO disagreements within a STATED tolerance;
  • the tamper control is RE-RUN inside this harness (a broken lowering must FAIL loudly);
  • Attack B's fixture is the stress case: the lowered FAITHFUL plan agrees with the oracle to
    tolerance, and a lowered UNFAITHFUL variant is DISTINGUISHABLE (Class C — we certify the
    computation, never the coincidence of outputs);
  • the PERIMETER of what the certificate covers is stated in the certificate.

Custody note (charter §7): this is a STUDY pilot. The lowering executes as our instructions on a
substrate we drive; the oracle is ground truth; no answer returns from anywhere the comparison did not
watch. Nothing here wires a product path.
"""
from __future__ import annotations

import json
import pathlib
import sys

import polars as pl
import pyarrow.substrait as pas
import ibis
from ibis_substrait.compiler.core import SubstraitCompiler

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oracle_harness import oracle, compare, negative_control          # noqa: E402

SUBSTRAIT_VERSION = "0.46.0"
TOL = 1e-6                    # STATED absolute tolerance; sums ~1e5 over ~1e4 terms => float64 error ~1e-8

# ibis schemas for the two source tables (the ReadRels of every lowering below)
_TX = [("store_id", "string"), ("product_id", "string"), ("customer_id", "string"),
       ("day", "string"), ("amount", "float64")]
_CAL = [("day", "string"), ("month", "string")]


def _load_tables():
    """Materialize the warehouse tables as Arrow (NOT a RecordBatchReader — Acero needs a Table)."""
    from columna_server.demo import demo_dir
    import duckdb
    wh = pathlib.Path(demo_dir()) / "cascadia" / "warehouse"
    c = duckdb.connect()
    tx = c.execute(f"select store_id, product_id, customer_id, day, amount "
                   f"from '{wh}/transactions.parquet'").to_arrow_table()
    cal = c.execute(f"select day, month from '{wh}/calendar.parquet'").to_arrow_table()
    return {"transactions": tx, "calendar": cal}


def _run(expr, tables) -> pl.DataFrame:
    """Compile an ibis expr to Substrait, execute on Acero, return a Polars frame."""
    plan = SubstraitCompiler().compile(expr)
    def provider(names, schema=None):
        key = names[-1] if isinstance(names, (list, tuple)) else names
        return tables.get(key)
    arrow = pas.run_query(plan.SerializeToString(), table_provider=provider).read_all()
    return pl.from_arrow(arrow), plan.version


# ---- the lowerings (proposed Rel compositions from D1, realized via ibis) -------------------------

def _t(tables):
    return (ibis.table(_TX, name="transactions"), ibis.table(_CAL, name="calendar"))


def lower_sum_intermediate(tables):
    """COLUMN(sum) + TRANSPORT(day->month via JoinRel) + REDUCE(sum @ store*product*month)."""
    t, cal = _t(tables)
    e = (t.inner_join(cal, t.day == cal.day)
          .select(t.store_id, t.product_id, t.amount, cal.month)
          .group_by(["store_id", "product_id", "month"]).aggregate(v=lambda x: x.amount.sum()))
    df, ver = _run(e, tables)
    return df.rename({"store_id": "store", "product_id": "product", "month": "cal.month",
                      "v": "sum(revenue @ {store*product*cal.month})"}), ver


def lower_sum_rollup(tables):
    """... + REDUCE(sum @ cal.month) — the roll-up of the intermediate (sum-of-sums, extensive)."""
    t, cal = _t(tables)
    inner = (t.inner_join(cal, t.day == cal.day)
              .select(t.store_id, t.product_id, t.amount, cal.month)
              .group_by(["store_id", "product_id", "month"]).aggregate(v=lambda x: x.amount.sum()))
    e = inner.group_by("month").aggregate(v=lambda x: x.v.sum())
    df, ver = _run(e, tables)
    return df.rename({"month": "cal.month", "v": "sum(revenue @ {store*product*cal.month})"}), ver


def lower_mean_faithful(tables):
    """Attack B FAITHFUL: mean over transaction ATOMS. Atom = (customer,store,product,day); atom-revenue
    = sum(amount); then mean of atom-revenues per month — lowered as sum,count then divide (the REDUCE
    mule decomposition of D1). Denotes the FrameQL mean."""
    t, cal = _t(tables)
    atoms = (t.group_by(["customer_id", "store_id", "product_id", "day"])
              .aggregate(rev=lambda x: x.amount.sum()))
    e = (atoms.inner_join(cal, atoms.day == cal.day).select(atoms.rev, cal.month)
              .group_by("month").aggregate(v=lambda x: x.rev.mean()))
    df, ver = _run(e, tables)
    return df.rename({"month": "cal.month", "v": "avg(revenue @ {customer*store*product*day})"}), ver


def lower_mean_unfaithful(tables):
    """Attack B UNFAITHFUL: mean of (store,product,month) SUMS. Every node lawful; the composition
    denotes a DIFFERENT statistic. A faithful lowering OF THE UNFAITHFUL PLAN — must agree with the
    unfaithful oracle and be DISTINGUISHABLE from the faithful oracle (Class C)."""
    t, cal = _t(tables)
    sums = (t.inner_join(cal, t.day == cal.day).select(t.store_id, t.product_id, t.amount, cal.month)
             .group_by(["store_id", "product_id", "month"]).aggregate(rev=lambda x: x.amount.sum()))
    e = sums.group_by("month").aggregate(v=lambda x: x.rev.mean())
    df, ver = _run(e, tables)
    return df.rename({"month": "cal.month", "v": "avg(revenue @ {store*product*cal.month})"}), ver


def lower_sum_TAMPERED(tables):
    """The BROKEN lowering (in-pilot tamper control): a DOUBLE-COUNT — the exact bare-JoinRel fan-out
    hazard D1's TRANSPORT row warns about, simulated by doubling the transported value. It is a lawful
    Rel composition that denotes the WRONG number, so it MUST fail against the oracle, or the harness is
    not testing (Class C: a wrong computation, not a coincidence)."""
    t, cal = _t(tables)
    agg = (t.inner_join(cal, t.day == cal.day)
            .select(t.store_id, t.product_id, t.amount, cal.month)
            .group_by(["store_id", "product_id", "month"]).aggregate(v=lambda x: x.amount.sum()))
    e = agg.select(agg.store_id, agg.product_id, agg.month, (agg.v * 2.0).name("v"))  # ProjectRel double
    df, ver = _run(e, tables)
    return df.rename({"store_id": "store", "product_id": "product", "month": "cal.month",
                      "v": "sum(revenue @ {store*product*cal.month})"}), ver


# ---- the pilot -----------------------------------------------------------------------------------

def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    outdir = pathlib.Path(argv[1])
    outdir.mkdir(parents=True, exist_ok=True)

    from columna_server.demo import demo_store
    store = demo_store()
    tables = _load_tables()

    comparisons = []
    plan_versions = set()

    # ---- 1) the conservation certificate: TRANSPORT-shaped sum, at both grains ----
    ok_versions = True
    for label, ask, lowerer, keys in [
        ("sum @ (store,product,cal.month)",
         "SELECT sum(revenue @ {store*product*cal.month}) AT {store*product*cal.month}",
         lower_sum_intermediate, ["store", "product", "cal.month"]),
        ("sum @ cal.month (roll-up)",
         "SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}",
         lower_sum_rollup, ["cal.month"]),
    ]:
        ref, okeys = oracle(store, "cascadia", ask)
        cand, ver = lowerer(tables)
        plan_versions.add(f"{ver.major_number}.{ver.minor_number}.{ver.patch_number}")
        c = compare(ref, cand, okeys, label=f"conservation · {label}",
                    perimeter=ask, tolerance=TOL)
        comparisons.append(c)
        print(c.summary())

    # ---- 2) the tamper control, RE-RUN in the pilot: a broken lowering must FAIL ----
    ref_i, keys_i = oracle(store, "cascadia",
                           "SELECT sum(revenue @ {store*product*cal.month}) AT {store*product*cal.month}")
    tcand, _ = lower_sum_TAMPERED(tables)
    tamper = compare(ref_i, tcand, keys_i, label="TAMPER(double-count lowering) — MUST FAIL",
                     perimeter="broken transport (fan-out / double-count)", tolerance=TOL)
    tamper_valid = not tamper.passed          # the broken lowering must NOT pass
    print(f"{tamper.summary()}   -> tamper_control_valid={tamper_valid}")
    # and the D3 oracle-side negative control, re-run here
    d3_ctrl = negative_control(store, "cascadia",
                               "SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}", TOL)

    # ---- 3) Attack B stress: faithful agrees, unfaithful is DISTINGUISHABLE (Class C) ----
    ref_faith, kf = oracle(store, "cascadia", "SELECT avg(revenue @ {customer*store*product*day}) AT {cal.month}")
    ref_unf, ku = oracle(store, "cascadia", "SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}")
    cand_faith, _ = lower_mean_faithful(tables)
    cand_unf, _ = lower_mean_unfaithful(tables)

    ab_faithful_agrees = compare(ref_faith, cand_faith, kf,
                                 label="Attack B · faithful lowering vs faithful oracle",
                                 perimeter="mean over atoms", tolerance=TOL)
    ab_unfaithful_selfconsistent = compare(ref_unf, cand_unf, ku,
                                 label="Attack B · unfaithful lowering vs UNFAITHFUL oracle (self-consistent)",
                                 perimeter="mean of sp-month sums", tolerance=TOL)
    # the distinguishability test: the unfaithful lowering must NOT match the FAITHFUL oracle.
    # rename the unfaithful cand's value col to the faithful oracle's, then compare — it must FAIL.
    cand_unf_as_faith = cand_unf.rename(
        {"avg(revenue @ {store*product*cal.month})": "avg(revenue @ {customer*store*product*day})"})
    ab_distinguishable = compare(ref_faith, cand_unf_as_faith, kf,
                                 label="Attack B · unfaithful lowering vs FAITHFUL oracle — MUST DIFFER",
                                 perimeter="Class C distinguishability", tolerance=TOL)
    class_c_ok = (ab_faithful_agrees.passed and ab_unfaithful_selfconsistent.passed
                  and not ab_distinguishable.passed)
    max_ab_gap = max((abs(a - b) for a, b in zip(
        ref_faith.sort("cal.month")["avg(revenue @ {customer*store*product*day})"].to_list(),
        cand_unf.sort("cal.month")["avg(revenue @ {store*product*cal.month})"].to_list())), default=0.0)
    print(f"  Attack B: faithful_agrees={ab_faithful_agrees.passed} "
          f"unfaithful_self_consistent={ab_unfaithful_selfconsistent.passed} "
          f"distinguishable={not ab_distinguishable.passed} (max faithful-vs-unfaithful gap={max_ab_gap:.2f}) "
          f"-> class_c_ok={class_c_ok}")

    # ---- the conservation certificate --------------------------------------------------------------
    conservation = [c for c in comparisons]
    N = sum(c.n_cells for c in conservation)
    all_conserve = all(c.passed for c in conservation)
    worst = max((getattr(c, "_worst_delta", 0.0) for c in conservation), default=0.0)
    accepted = bool(all_conserve and N >= 30 and tamper_valid and d3_ctrl["control_valid"] and class_c_ok)

    certificate = {
        "certificate": "urn:columna:mapping-study:c1-pilot:v0.1",
        "perimeter": ("Cascadia warehouse · transaction universe · revenue = sum(amount) joined to "
                      "calendar on day · the TRANSPORT-shaped sum at (store,product,cal.month) and its "
                      "roll-up to cal.month · lowered to Substrait via ibis-substrait, executed on Acero"),
        "versions": {"substrait": sorted(plan_versions), "substrait_declared": SUBSTRAIT_VERSION,
                     "producer": "ibis-substrait 4.0.1 / substrait proto 0.16.0",
                     "consumer": "pyarrow.substrait (Acero) 25.0.0", "core": "0.14.0-core",
                     "polars_oracle": pl.__version__},
        "tolerance_abs": TOL,
        "N_comparisons": N,
        "N_ge_30": N >= 30,
        "conservation": {c.label: {"passed": c.passed, "cells": c.n_cells,
                                   "worst_delta": getattr(c, "_worst_delta", None)} for c in conservation},
        "conservation_worst_delta": worst,
        "tamper_control": {"in_pilot_broken_lowering_fails": tamper_valid,
                           "d3_oracle_negative_control_valid": d3_ctrl["control_valid"]},
        "attack_b_stress": {
            "faithful_lowering_agrees": ab_faithful_agrees.passed,
            "unfaithful_lowering_self_consistent": ab_unfaithful_selfconsistent.passed,
            "unfaithful_distinguishable_from_faithful": not ab_distinguishable.passed,
            "max_faithful_vs_unfaithful_gap": max_ab_gap,
            "class_c_ok": class_c_ok,
            "lesson": "we certify the computation, never the coincidence of outputs",
        },
        "ACCEPTED": accepted,
    }
    (outdir / "d4_c1_pilot_certificate.json").write_text(json.dumps(certificate, indent=2) + "\n")

    print("\n=== C1 PILOT CERTIFICATE ===")
    print(f"  N comparisons          : {N}  (>=30: {N >= 30})")
    print(f"  conservation           : {all_conserve}  (worst delta {worst:.2e}, tol {TOL:g})")
    print(f"  tamper control valid   : {tamper_valid and d3_ctrl['control_valid']}")
    print(f"  Attack B / Class C ok  : {class_c_ok}")
    print(f"  ACCEPTED               : {accepted}")
    print(f"  wrote {outdir / 'd4_c1_pilot_certificate.json'}")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

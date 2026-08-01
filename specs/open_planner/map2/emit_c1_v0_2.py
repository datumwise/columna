#!/usr/bin/env python3
"""MAP-2 · steps 1-2 (v0.2) — mint the C1 rule certificate, then re-emit C1's plan certificate
v0.2-conformant, and run the channel test.

    python specs/open_planner/map2/emit_c1_v0_2.py specs/open_planner/map2/

STEP 1: mint the FIRST rule certificate — the TRANSPORT-shaped-sum rule × Acero — from the accepted C1
pilot's numbers (§4b shape), filed in the published adjudication record. Its digest is the ref every
future M1 points at (V4).
STEP 2: re-emit C1's plan certificate to the v0.2 schema (S1..S10 + M1..M4), M1 referencing the rule
cert. Then the channel test: two executions, the semantic channel byte-identical (diff written).
"""
from __future__ import annotations

import json
import pathlib
import sys

import polars as pl  # noqa: F401  (imported so pl.__version__ is available for M-channel)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cert_v0_2 as C                                                    # noqa: E402
from oracle_harness import oracle, compare                              # noqa: E402
from pilot_c1 import (_load_tables, lower_sum_intermediate, lower_sum_rollup,  # noqa: E402
                      lower_sum_TAMPERED, TOL, _t)

ACCEPTANCE_DATE = "2026-08-01"          # the C1 pilot acceptance date — a FIXED provenance stamp (not a
                                        # wall-clock read), so the filed artifacts are reproducible.
HARNESS = "map2/oracle_harness+pilot_c1 v0.1"
RULE_ID = "c1-transport-shaped-sum"


def _run_conservation(store, tables):
    """Re-derive the accepted pilot's mechanical numbers (N, worst_delta, tamper status)."""
    n_cells, worst = 0, 0.0
    for ask, keys, lowerer in [
        ("SELECT sum(revenue @ {store*product*cal.month}) AT {store*product*cal.month}",
         ["store", "product", "cal.month"], lower_sum_intermediate),
        ("SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}",
         ["cal.month"], lower_sum_rollup)]:
        ref, okeys = oracle(store, "cascadia", ask)
        cand, _ = lowerer(tables)
        c = compare(ref, cand, okeys, label=ask, perimeter=ask, tolerance=TOL)
        assert c.passed, f"C1 conservation regressed: {c.summary()}"
        n_cells += c.n_cells
        worst = max(worst, getattr(c, "_worst_delta", 0.0))
    # tamper: the double-count lowering must FAIL
    ref_i, keys_i = oracle(store, "cascadia",
                           "SELECT sum(revenue @ {store*product*cal.month}) AT {store*product*cal.month}")
    tcand, _ = lower_sum_TAMPERED(tables)
    tamper = compare(ref_i, tcand, keys_i, label="tamper", perimeter="broken", tolerance=TOL)
    return {"N": n_cells, "tolerance": TOL, "worst_delta": worst,
            "tamper_status": "valid" if not tamper.passed else "INVALID",
            "harness_version": HARNESS, "tested_version": "25.0.0", "date": ACCEPTANCE_DATE}


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(argv[1])
    adjud = root / "adjudication_record"
    fixtures = root / "fixtures"
    adjud.mkdir(parents=True, exist_ok=True)
    fixtures.mkdir(parents=True, exist_ok=True)

    from columna_server.demo import demo_store
    from columna_server import tools as T
    store = demo_store()
    m = store.get("cascadia").server.engine.m
    tables = _load_tables()

    oracle_run = _run_conservation(store, tables)

    # ---- STEP 1: mint the C1 rule certificate (§4b) ----
    rule_cert = C.rule_certificate(
        rule_id=RULE_ID,
        rule_statement=("a monoid SUM delivered through a CORROBORATED FUNCTIONAL hierarchy edge "
                        "(Substrait: INNER JoinRel on the from-key + AggregateRel[sum]) conserves the "
                        "extensive denotation; the roll-up of the intermediate grain is sum-of-sums, "
                        "associative. Covers sum/count/min/max monoids; NOT mules, sketches, or "
                        "non-functional edges."),
        backend={"identity": "pyarrow.substrait (Acero)", "version_band": ">=25,<26"},
        oracle_run=oracle_run,
        perimeter=("the TRANSPORT-shaped monoid-sum lowering rule on Acero, over a corroborated "
                   "functional edge; per-rule proof amortized by every plan that reuses it."))
    (adjud / f"rule_{RULE_ID.replace('-', '_')}.json").write_text(
        json.dumps(rule_cert, indent=2, sort_keys=True) + "\n")
    print(f"STEP 1 — minted rule certificate {RULE_ID}\n  digest {rule_cert['digest']}")

    # ---- STEP 2: re-emit C1's plan certificate, v0.2-conformant ----
    model = C.model_field(m)
    # S8 — the two-stage-statistic disclosure, read from the actual wire (not from memory)
    wire = T.query(store, "cascadia", "SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}")
    wcol = wire["columns"][0]
    s8 = [{"code": d.get("code"), "kind": "two_stage_statistic", "severity": "immaterial",
           "detail": d.get("detail")} for d in (wcol.get("disclosures") or [])]

    # S4 — the IR node list of the TRANSPORT-shaped plan
    ir_nodes = [
        {"id": "n0", "node": "CARVE", "universe": "transaction"},
        {"id": "n1", "node": "COLUMN", "measure": "revenue", "family": "sum"},
        {"id": "n2", "node": "TRANSPORT", "from_level": "day", "to_level": "cal.month", "via": "calendar"},
        {"id": "n3", "node": "REDUCE", "op": "sum", "at": ["store", "product", "cal.month"]},
        {"id": "n4", "node": "REDUCE", "op": "sum", "at": ["cal.month"]},
        {"id": "n5", "node": "ANCHOR", "coords": ["cal.month"]},
    ]
    # S9 — from the ACTUAL produced two-stage plan
    t, cal = _t(tables)
    inner = (t.inner_join(cal, t.day == cal.day).select(t.store_id, t.product_id, t.amount, cal.month)
              .group_by(["store_id", "product_id", "month"]).aggregate(v=lambda x: x.amount.sum()))
    expr = inner.group_by("month").aggregate(v=lambda x: x.v.sum())
    plan, subver = C.compile_substrait(expr)

    s6 = [{"edge_id": "day->cal.month@calendar", "from_level": "day", "to_level": "cal.month",
           "corroboration_verdict_ref": {"mode": "embed_with_digest", "verdict": "proven",
                                         "model_adjudication_digest": model["adjudication_digest"]}}]
    s5 = [
        {"law_id": f"conservation/{RULE_ID}", "clause": "⟦L(N)⟧ = ⟦N⟧ on the declared model",
         "verdict": "discharged — this lowering conserves the denotation",
         "ref": rule_cert["digest"], "mode": "ref"},
        {"law_id": "family/sum", "clause": "fertile extensive monoid; delivery and roll-up associative",
         "verdict": "licensed", "ref": model["adjudication_digest"], "mode": "embed_with_digest"},
        {"law_id": "edge/day->cal.month", "clause": "corroborated functional edge (no fan-out)",
         "verdict": "proven", "ref": "S6[0]", "mode": "ref"},
    ]

    cert, semantic = C.plan_certificate(
        model=model,
        ask=C.ask_field("SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}"),
        plan_ir=C.plan_field(ir_nodes),
        obligations=s5, edge_attestations=s6, face_spends=[],
        disclosure_projection=s8, lowering_map=C.lowering_map_field(plan),
        perimeter=("Cascadia · transaction universe · revenue=sum(amount) joined to calendar on day · "
                   "the TRANSPORT-shaped sum at (store,product,cal.month) rolled up to cal.month · "
                   "lowered to Substrait, executed on Acero · covers THIS plan only; other nodes' "
                   "lowerings stand as D1 proposals until piloted."),
        m1={"producer": "ibis-substrait 4.0.1", "substrait_version": subver, "proto_pin": "substrait 0.16.0",
            "lowering_rule_ids": [RULE_ID], "rule_cert_refs": {RULE_ID: rule_cert["digest"]}},
        m2={"consumer": "pyarrow.substrait (Acero)", "version": "25.0.0", "version_band": ">=25,<26"},
        m3=oracle_run)

    (fixtures / "c1_plan_certificate_v0_2.json").write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (fixtures / "c1_semantic_channel_v0_2.json").write_text(json.dumps(semantic, indent=2, sort_keys=True) + "\n")
    print(f"STEP 2 — emitted C1 plan certificate v0.2 (semantic digest {cert['semantic_channel_digest'][:23]}…)")

    # ---- the channel test (V3): re-emit the semantic channel and diff ----
    _, semantic_again = C.plan_certificate(
        model=model, ask=C.ask_field("SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}"),
        plan_ir=C.plan_field(ir_nodes), obligations=s5, edge_attestations=s6, face_spends=[],
        disclosure_projection=s8, lowering_map=C.lowering_map_field(C.compile_substrait(expr)[0]),
        perimeter=semantic["S10_perimeter"],
        m1={}, m2={}, m3={})   # M-channel irrelevant to the semantic diff
    a = json.dumps(semantic, sort_keys=True)
    b = json.dumps(semantic_again, sort_keys=True)
    v3 = (a == b)
    (fixtures / "c1_v0_2_channel_test.txt").write_text(
        f"V3 channel test — two independent emissions of the C1 semantic channel:\n"
        f"  byte-identical: {v3}\n"
        f"  semantic_channel_digest: {cert['semantic_channel_digest']}\n"
        f"  (mechanical channel carries N/tolerance/worst_delta/date and MAY vary; not diffed)\n")
    print(f"V3 channel test — semantic channel byte-identical across two emissions: {v3}")
    return 0 if v3 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

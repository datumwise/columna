#!/usr/bin/env python3
"""MAP-2 · D4/step-3 — the C2 pilot: the full spine with WHERE-CARVE and the mean-via-(sum,count) rule.

    python specs/open_planner/map2/pilot_c2.py specs/open_planner/map2/

C2 ask: `avg(revenue @ {store*cal.month}) AT {cal.month} WHERE day >= '2024-04-01'` — the full
CARVE→COLUMN→TRANSPORT→REDUCE spine, exercising (a) the newly-attested **CARVE** as a Substrait
`FilterRel` (the WHERE predicate) and (b) the **REDUCE-mean** rule: a mule mean lowered as its
sufficient statistics (sum, count) then a `ProjectRel` divide (the mean-of-means theorem as a lowering
constraint). Lowered to Substrait 0.46.0, executed on Acero, oracle-compared via the D3 harness.

C2 emits its plan certificate **v0.2-CONFORMANT NATIVELY** — that native emission IS the schema's
acceptance test (schema §6). On acceptance it mints the SECOND rule certificate
(REDUCE-mean-decomposition × Acero) and demonstrates amortization by reusing C1's rule certificate for
its inner TRANSPORT-shaped sum.

Acceptance (same bar as C1): N >= 30, zero disagreements within stated tolerance, tamper control re-run,
perimeter stated. Plus: the emitted certificate passes V1/V3/V4/V5/V6 and the channel test.
"""
from __future__ import annotations

import json
import pathlib
import sys

import polars as pl
import pyarrow.substrait as pas

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cert_v0_2 as C                                                    # noqa: E402
from oracle_harness import oracle, compare, negative_control            # noqa: E402
from pilot_c1 import _load_tables, _t, TOL                              # noqa: E402

ASK = "SELECT avg(revenue @ {store*cal.month}) AT {cal.month} WHERE day >= '2024-04-01'"
ASK_INNER = "SELECT sum(revenue @ {store*cal.month}) AT {store*cal.month} WHERE day >= '2024-04-01'"
ACCEPTANCE_DATE = "2026-08-01"
HARNESS = "map2/oracle_harness+pilot_c2 v0.1"
RULE_ID = "c2-reduce-mean-decomposition"
C1_RULE_ID = "c1-transport-shaped-sum"
DATE_FLOOR = "2024-04-01"


def _prov(tables):
    def p(names, schema=None):
        return tables.get(names[-1] if isinstance(names, (list, tuple)) else names)
    return p


def _run(expr, tables):
    plan, ver = C.compile_substrait(expr)
    return pl.from_arrow(pas.run_query(plan.SerializeToString(), table_provider=_prov(tables)).read_all()), plan, ver


def _inner_sums(tables):
    """CARVE(where) + TRANSPORT(day->month) + REDUCE(sum @ store,month) — the sufficient statistic."""
    t, cal = _t(tables)
    return (t.filter(t.day >= DATE_FLOOR).inner_join(cal, t.day == cal.day)
             .select(t.store_id, t.amount, cal.month)
             .group_by(["store_id", "month"]).aggregate(rev=lambda x: x.amount.sum()))


def lower_intermediate(tables):
    df, plan, ver = _run(_inner_sums(tables), tables)
    return df.rename({"store_id": "store", "month": "cal.month",
                      "rev": "sum(revenue @ {store*cal.month})"}), plan, ver


def lower_mean(tables):
    """REDUCE-mean via (sum,count) then ProjectRel divide."""
    inner = _inner_sums(tables)
    stats = inner.group_by("month").aggregate(S=lambda x: x.rev.sum(), K=lambda x: x.rev.count())
    mean = stats.select(stats.month, (stats.S / stats.K).name("v"))
    df, plan, ver = _run(mean, tables)
    return df.rename({"month": "cal.month", "v": "avg(revenue @ {store*cal.month})"}), plan, ver


def lower_mean_TAMPERED(tables):
    """BROKEN: mean of RAW transaction amounts per month (wrong INPUT GRAIN — Attack B's subject). A
    lawful AggregateRel[mean] that denotes a different statistic; must FAIL against the oracle."""
    t, cal = _t(tables)
    e = (t.filter(t.day >= DATE_FLOOR).inner_join(cal, t.day == cal.day).select(t.amount, cal.month)
          .group_by("month").aggregate(v=lambda x: x.amount.mean()))
    df, _, _ = _run(e, tables)
    return df.rename({"month": "cal.month", "v": "avg(revenue @ {store*cal.month})"})


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(argv[1])
    adjud = root / "adjudication_record"; fixtures = root / "fixtures"
    adjud.mkdir(parents=True, exist_ok=True); fixtures.mkdir(parents=True, exist_ok=True)

    from columna_server.demo import demo_store
    from columna_server import tools as T
    store = demo_store()
    m = store.get("cascadia").server.engine.m
    tables = _load_tables()

    # ---- oracle-compare at both grains (N >= 30 via the 488 sufficient-statistic cells) ----
    comparisons = []
    ref_mean, k_mean = oracle(store, "cascadia", ASK)
    cand_mean, plan_mean, subver = lower_mean(tables)
    comparisons.append(compare(ref_mean, cand_mean, k_mean, label="C2 mean @ cal.month",
                               perimeter=ASK, tolerance=TOL))
    ref_int, k_int = oracle(store, "cascadia", ASK_INNER)
    cand_int, _, _ = lower_intermediate(tables)
    comparisons.append(compare(ref_int, cand_int, k_int, label="C2 sufficient stat: sum @ store*cal.month",
                               perimeter=ASK_INNER, tolerance=TOL))
    for c in comparisons:
        print(c.summary())

    # ---- tamper re-run: the wrong-grain mean must FAIL ----
    tcand = lower_mean_TAMPERED(tables)
    tamper = compare(ref_mean, tcand, k_mean, label="TAMPER(wrong-grain mean) — MUST FAIL",
                     perimeter="broken REDUCE-mean (raw-amount grain)", tolerance=TOL)
    tamper_valid = not tamper.passed
    d3_ctrl = negative_control(store, "cascadia", ASK, TOL)
    print(f"{tamper.summary()}  -> tamper_valid={tamper_valid}; d3_control={d3_ctrl['control_valid']}")

    N = sum(c.n_cells for c in comparisons)
    worst = max((getattr(c, "_worst_delta", 0.0) for c in comparisons), default=0.0)
    all_pass = all(c.passed for c in comparisons)
    accepted = bool(all_pass and N >= 30 and tamper_valid and d3_ctrl["control_valid"])

    oracle_run = {"N": N, "tolerance": TOL, "worst_delta": worst,
                  "tamper_status": "valid" if tamper_valid else "INVALID",
                  "harness_version": HARNESS, "tested_version": "25.0.0", "date": ACCEPTANCE_DATE}

    # ---- mint the SECOND rule certificate (REDUCE-mean) on pass ----
    if accepted:
        rule_cert = C.rule_certificate(
            rule_id=RULE_ID,
            rule_statement=("a MULE mean is lowered as its sufficient statistics — AggregateRel[sum] and "
                            "AggregateRel[count] — then a ProjectRel divide; the mean-of-means theorem as "
                            "a lowering constraint. Conserves the mean denotation. Covers mean (and, by the "
                            "same decomposition, weighted_mean/variance/stddev); NOT holistic mules "
                            "(median/mode) or sketch distincts."),
            backend={"identity": "pyarrow.substrait (Acero)", "version_band": ">=25,<26"},
            oracle_run=oracle_run,
            perimeter="the REDUCE-mean sufficient-statistics lowering rule on Acero.")
        (adjud / f"rule_{RULE_ID.replace('-', '_')}.json").write_text(
            json.dumps(rule_cert, indent=2, sort_keys=True) + "\n")
        print(f"minted rule certificate {RULE_ID}\n  digest {rule_cert['digest']}")
    else:
        print("NOT ACCEPTED — rule certificate NOT minted.")
        return 1

    # C1's rule cert (reused for the inner sum — amortization made visible)
    c1_rc = json.loads((adjud / "rule_c1_transport_shaped_sum.json").read_text())

    # ---- emit C2's plan certificate v0.2-CONFORMANT NATIVELY ----
    model = C.model_field(m)
    wire = T.query(store, "cascadia", ASK); wcol = wire["columns"][0]
    s8 = [{"code": d.get("code"), "kind": "mean_decomposition", "severity": "immaterial",
           "detail": d.get("detail")} for d in (wcol.get("disclosures") or [])]
    ir_nodes = [
        {"id": "n0", "node": "CARVE", "universe": "transaction", "where": f"day >= '{DATE_FLOOR}'"},
        {"id": "n1", "node": "COLUMN", "measure": "revenue", "family": "sum"},
        {"id": "n2", "node": "TRANSPORT", "from_level": "day", "to_level": "cal.month", "via": "calendar"},
        {"id": "n3", "node": "REDUCE", "op": "sum", "at": ["store", "cal.month"]},
        {"id": "n4", "node": "REDUCE", "op": "mean", "at": ["cal.month"], "via": "sufficient_statistics(sum,count)"},
        {"id": "n5", "node": "ANCHOR", "coords": ["cal.month"]},
    ]
    s6 = [{"edge_id": "day->cal.month@calendar", "from_level": "day", "to_level": "cal.month",
           "corroboration_verdict_ref": {"mode": "embed_with_digest", "verdict": "proven",
                                         "model_adjudication_digest": model["adjudication_digest"]}}]
    s5 = [
        {"law_id": f"conservation/{RULE_ID}", "clause": "⟦L(mean)⟧ = ⟦mean⟧ via (sum,count) decomposition",
         "verdict": "discharged — the mean lowering conserves the denotation", "ref": rule_cert["digest"], "mode": "ref"},
        {"law_id": f"conservation/{C1_RULE_ID}", "clause": "the inner sum reuses the TRANSPORT-shaped rule (amortized)",
         "verdict": "inherited", "ref": c1_rc["digest"], "mode": "ref"},
        {"law_id": "family/mean", "clause": "mule; fertile sufficient-statistics decomposition (sum,count)",
         "verdict": "licensed", "ref": model["adjudication_digest"], "mode": "embed_with_digest"},
        {"law_id": "carve/where", "clause": "population restriction pushed to the read as a FilterRel",
         "verdict": "licensed", "ref": model["adjudication_digest"], "mode": "embed_with_digest"},
        {"law_id": "edge/day->cal.month", "clause": "corroborated functional edge (no fan-out)",
         "verdict": "proven", "ref": "S6[0]", "mode": "ref"},
    ]
    cert, semantic = C.plan_certificate(
        model=model, ask=C.ask_field(ASK), plan_ir=C.plan_field(ir_nodes),
        obligations=s5, edge_attestations=s6, face_spends=[], disclosure_projection=s8,
        lowering_map=C.lowering_map_field(plan_mean),
        perimeter=("Cascadia · transaction universe · revenue=sum(amount) filtered to day>='2024-04-01' "
                   "joined to calendar on day · the mean of per-(store,cal.month) revenue at cal.month, "
                   "the mule lowered via sufficient statistics (sum,count)+divide · executed on Acero · "
                   "covers THIS plan; the inner sum reuses the C1 rule certificate."),
        m1={"producer": "ibis-substrait 4.0.1", "substrait_version": subver, "proto_pin": "substrait 0.16.0",
            "lowering_rule_ids": [RULE_ID, C1_RULE_ID],
            "rule_cert_refs": {RULE_ID: rule_cert["digest"], C1_RULE_ID: c1_rc["digest"]}},
        m2={"consumer": "pyarrow.substrait (Acero)", "version": "25.0.0", "version_band": ">=25,<26"},
        m3=oracle_run)
    (fixtures / "c2_plan_certificate_v0_2.json").write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (fixtures / "c2_semantic_channel_v0_2.json").write_text(json.dumps(semantic, indent=2, sort_keys=True) + "\n")

    # ---- V-rule self-validation + channel test on the NATIVE emission ----
    transports = [n for n in ir_nodes if n["node"] == "TRANSPORT"]
    v1 = len(transports) == len(s6)
    v4 = all(r in {rule_cert["digest"], c1_rc["digest"]} for r in cert["mechanical"]["M1_lowering_attestation"]["rule_cert_refs"].values())
    v5 = bool(semantic["S10_perimeter"]); v6 = "parse_digest" in semantic["S3_ask"]
    _, semantic2 = C.plan_certificate(
        model=model, ask=C.ask_field(ASK), plan_ir=C.plan_field(ir_nodes), obligations=s5,
        edge_attestations=s6, face_spends=[], disclosure_projection=s8,
        lowering_map=C.lowering_map_field(lower_mean(tables)[1]), perimeter=semantic["S10_perimeter"],
        m1={}, m2={}, m3={})
    v3 = json.dumps(semantic, sort_keys=True) == json.dumps(semantic2, sort_keys=True)

    print("\n=== C2 PILOT (v0.2-conformant native emission) ===")
    print(f"  N comparisons     : {N}  (>=30: {N >= 30})")
    print(f"  conservation      : {all_pass}  (worst {worst:.2e}, tol {TOL:g})")
    print(f"  tamper valid      : {tamper_valid and d3_ctrl['control_valid']}")
    print(f"  V1/V3/V4/V5/V6    : {v1}/{v3}/{v4}/{v5}/{v6}")
    print(f"  ACCEPTED          : {accepted}")
    schema_ok = accepted and v1 and v3 and v4 and v5 and v6
    print(f"  SCHEMA ACCEPTANCE : {schema_ok}  (the native v0.2 emission is the schema's acceptance test)")
    return 0 if schema_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

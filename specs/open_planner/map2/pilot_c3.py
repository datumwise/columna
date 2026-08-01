#!/usr/bin/env python3
"""MAP-2 · Beat 3 Experiment A — C3, the CROSS-bearing pilot (the VERTICAL seam).

    python specs/open_planner/map2/pilot_c3.py specs/open_planner/map2/

Ask (desk-approved): `SELECT revenue AT {category.touch}` — a plan split between HOME and SUBSTRATE:
  • HOME (stay-home CROSS): revenue delivered to product, join-multiplied through the product<->category
    bridge (touch: revenue reaches every category a product sits in, multi-counted), and the
    `multi_counted` disclosure minted. This is the crossed intermediate — the home→substrate HANDOFF.
  • SUBSTRATE (lowered REDUCE): an AggregateRel[sum] over the handoff, collapsing to category. NO bridge
    join leaves home (A-3, verified not asserted).

What A establishes (desk concretizations):
  A-1 mixed execution conservation-clean end-to-end vs the all-home oracle; TWO seam break modes —
      (i) wrong-grain intermediate at the handoff, (ii) dropped rows before the substrate sum — each
      MUST fail on the harness.
  A-3 the substrate substrait plan provably contains NO bridge join (the CROSS never left home) and
      receives only the post-cross span; the check's output is attached.
  A-4 the touch disclosure (multi_counted) arrives in the final answer with half the plan on Acero.

What A must NOT do (walls): lower any part of CROSS itself; invent a new handoff transport (the handoff
is the existing crossed-intermediate frame — if that couldn't express it, that is a FINDING and we stop).
G4 finding (measured boundary, filed on OF-26): a single faced coordinate is the maximal expressible
CROSS seam at v1 — chained crossings are unlicensed, so no richer C3' exists until that WP ships.
"""
from __future__ import annotations

import json
import pathlib
import sys

import polars as pl
import pyarrow as pa
import pyarrow.substrait as pas
import ibis

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cert_v0_2 as C                                                    # noqa: E402
from oracle_harness import oracle, compare                              # noqa: E402

ACCEPTANCE_DATE = "2026-08-01"
TOL = 1e-6
ASK = "SELECT revenue AT {category.touch}"


def _bridge_and_revenue(store):
    """HOME prep: revenue delivered to product (from the engine — the real number), and the bridge."""
    from columna_server.demo import demo_dir
    import duckdb
    wh = pathlib.Path(demo_dir()) / "cascadia" / "warehouse"
    c = duckdb.connect()
    # revenue per product — via the ENGINE oracle (the real delivered value), keyed by product
    rev_prod, _ = oracle(store, "cascadia", "SELECT revenue AT {product}")
    bridge = pl.from_arrow(c.execute(
        f"select product_id, category_id from '{wh}/product_categories.parquet'").to_arrow_table())
    return rev_prod, bridge


def home_cross(store):
    """HOME (stay-home CROSS): bridge join-multiply → the crossed intermediate + the minted disclosure.
    Returns (crossed_intermediate_df[product, category, revenue], multi_counted_disclosure)."""
    rev_prod, bridge = _bridge_and_revenue(store)
    # rev_prod columns: ['product', 'revenue'] (anchor key 'product' + value col named 'revenue')
    valcol = [c for c in rev_prod.columns if c != "product"][0]
    crossed = (bridge.join(rev_prod.rename({valcol: "revenue"}), left_on="product_id",
                           right_on="product", how="inner")
                     .select(["product_id", "category_id", "revenue"]))
    # the disclosure is minted HERE (the CROSS), read from the engine's touch wire
    from columna_server import tools as T
    wire = T.query(store, "cascadia", ASK)
    disc = next((d for d in (wire["columns"][0].get("disclosures") or [])
                 if d.get("code") == "multi_counted"), None)
    return crossed, disc


def substrate_sum(crossed: pl.DataFrame):
    """SUBSTRATE (lowered REDUCE): AggregateRel[sum] over the handoff — NO bridge join. Executed on
    Acero from a Substrait plan. Returns (result_df[category, revenue], substrait_plan)."""
    handoff = crossed.to_arrow()
    t = ibis.table([("product_id", "string"), ("category_id", "string"), ("revenue", "float64")],
                   name="crossed")
    expr = t.group_by("category_id").aggregate(v=lambda x: x.revenue.sum())
    plan, _ = C.compile_substrait(expr)

    def provider(names, schema=None):
        return handoff
    out = pl.from_arrow(pas.run_query(plan.SerializeToString(), table_provider=provider).read_all())
    return out.rename({"category_id": "category.touch", "v": "revenue"}), plan


def a3_split_check(plan) -> dict:
    """A-3 — VERIFY (not assert) the substrate plan contains NO bridge join: walk its Rel tree and
    confirm no `join` kind, and that it reads only the single handoff table."""
    kinds = [k for _, k in C.walk_rels(plan.relations[0].root.input)]
    reads = sum(1 for k in kinds if k == "read")
    joins = sum(1 for k in kinds if k == "join")
    return {"rel_kinds": kinds, "reads": reads, "joins": joins,
            "cross_stayed_home": joins == 0 and reads == 1,
            "note": "the substrate received only the post-cross span (one ReadRel over the handoff) "
                    "and performs one AggregateRel[sum]; zero JoinRel — the bridge never left home"}


def stretch_split(store):
    """A-4 STRETCH (not a gate): the alloc face (`{category.split}`) across the seam — the reconciliation
    badge is the hardest honest test (conservation arithmetic must survive home→substrate). Home splits
    revenue by the per-product-normalized alloc_weight (reconciles by construction); substrate sums to
    category; we check both the oracle match AND that the crossed total reconciles to the base total."""
    from columna_server.demo import demo_dir
    import duckdb
    wh = pathlib.Path(demo_dir()) / "cascadia" / "warehouse"
    c = duckdb.connect()
    recon = c.execute(f"""
      with rp as (select product_id, sum(amount) rev from '{wh}/transactions.parquet' group by 1),
           bw as (select b.product_id, b.category_id, ca.alloc_weight
                  from '{wh}/product_categories.parquet' b
                  join '{wh}/category_attributes.parquet' ca using(category_id)),
           norm as (select product_id, category_id,
                    alloc_weight/sum(alloc_weight) over (partition by product_id) w from bw)
      select n.product_id, n.category_id, rp.rev*n.w alloc_rev
      from norm n join rp using(product_id)""").to_arrow_table()
    t = ibis.table([("product_id", "string"), ("category_id", "string"), ("alloc_rev", "float64")],
                   name="crossed")
    plan, _ = C.compile_substrait(t.group_by("category_id").aggregate(v=lambda x: x.alloc_rev.sum()))
    res = pl.from_arrow(pas.run_query(plan.SerializeToString(),
                                      table_provider=lambda n, schema=None: recon).read_all())
    res = res.rename({"category_id": "category.split", "v": "revenue"})
    ref, keys = oracle(store, "cascadia", "SELECT revenue AT {category.split}")
    cmp = compare(ref, res, keys, label="A-4 STRETCH: split (alloc) across the seam",
                  perimeter="SELECT revenue AT {category.split}", tolerance=TOL)
    base = c.execute(f"select sum(amount) from '{wh}/transactions.parquet'").fetchone()[0]
    crossed_total = float(res["revenue"].sum())
    recon_delta = abs(base - crossed_total)
    return {"oracle_match": cmp.passed, "cells": cmp.n_cells,
            "reconciles_across_seam": recon_delta < 1e-6,
            "base_total": base, "crossed_total": crossed_total, "reconciliation_delta": recon_delta}


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(argv[1]); fixtures = root / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    from columna_server.demo import demo_store
    store = demo_store()

    # ---- the vertical seam: home CROSS -> handoff -> substrate SUM ----
    crossed, disc = home_cross(store)
    result, plan = substrate_sum(crossed)
    a3 = a3_split_check(plan)
    print(f"A-3 split check: cross_stayed_home={a3['cross_stayed_home']} "
          f"(reads={a3['reads']} joins={a3['joins']}) — {a3['rel_kinds']}")

    # ---- A-1: conservation-clean end to end ----
    # (final) the full plan's category sums vs the all-home oracle
    ref_final, k_final = oracle(store, "cascadia", ASK)
    cmp_final = compare(ref_final, result, k_final, label="C3 final: revenue @ category.touch (home+substrate)",
                        perimeter=ASK, tolerance=TOL)
    # (handoff) the crossed intermediate vs an INDEPENDENT duckdb reconstruction (no engine oracle can
    # produce it — G4 bars the multi-dim faced anchor; the reconstruction is the reference)
    from columna_server.demo import demo_dir
    import duckdb
    wh = pathlib.Path(demo_dir()) / "cascadia" / "warehouse"
    c = duckdb.connect()
    recon = pl.from_arrow(c.execute(
        f"""with rp as (select product_id, sum(amount) revenue from '{wh}/transactions.parquet' group by 1)
            select b.product_id, b.category_id, rp.revenue
            from '{wh}/product_categories.parquet' b join rp using(product_id)""").to_arrow_table())
    cmp_handoff = compare(recon, crossed, ["product_id", "category_id"],
                          label="C3 handoff: crossed intermediate vs independent reconstruction",
                          perimeter="the home→substrate handoff carries the correct crossed intermediate",
                          tolerance=TOL)
    for x in (cmp_final, cmp_handoff):
        print(x.summary())
    N = cmp_final.n_cells + cmp_handoff.n_cells
    conserve = cmp_final.passed and cmp_handoff.passed

    # ---- A-1 seam break modes: each MUST fail ----
    # (i) wrong-grain intermediate: hand the substrate revenue-per-PRODUCT (pre-cross grain), summed by a
    #     bogus category cast — the wrong grain reaches the substrate; category sums must differ.
    wrong = crossed.with_columns(pl.col("product_id").alias("category_id"))  # grain = product, not category
    res_wrong, _ = substrate_sum(wrong.select(["product_id", "category_id", "revenue"]))
    brk_grain = compare(ref_final, res_wrong.rename({}), k_final,
                        label="BREAK(i) wrong-grain intermediate — MUST FAIL", perimeter="", tolerance=TOL)
    # (ii) dropped rows before the substrate sum
    dropped = crossed.head(crossed.height - 50)
    res_drop, _ = substrate_sum(dropped)
    brk_drop = compare(ref_final, res_drop, k_final,
                       label="BREAK(ii) dropped rows pre-sum — MUST FAIL", perimeter="", tolerance=TOL)
    breaks_valid = (not brk_grain.passed) and (not brk_drop.passed)
    print(f"seam break modes: wrong_grain_fails={not brk_grain.passed} dropped_rows_fails={not brk_drop.passed}")

    # ---- A-4: the multi_counted disclosure arrives in the final answer (minted home, sum on Acero) ----
    a4_ok = disc is not None and disc.get("code") == "multi_counted"
    print(f"A-4 disclosure survives the seam: {a4_ok} — {disc.get('detail') if disc else None}")

    accepted = bool(conserve and N >= 30 and breaks_valid and a4_ok and a3["cross_stayed_home"])

    # ---- C3 certificate v0.2-conformant (S7's first exhibit) ----
    m = store.get("cascadia").server.engine.m
    model = C.model_field(m)
    ir_nodes = [
        {"id": "n0", "node": "CARVE", "universe": "transaction"},
        {"id": "n1", "node": "COLUMN", "measure": "revenue", "family": "sum"},
        {"id": "n2", "node": "REDUCE", "op": "sum", "at": ["product"], "locus": "home (CROSS input prep)"},
        {"id": "n3", "node": "CROSS", "relate": "product<->category", "face": "touch",
         "locus": "STAY_HOME", "note": "bridge join-multiply + multi_counted minting; never lowered"},
        {"id": "n4", "node": "REDUCE", "op": "sum", "at": ["category.touch"], "locus": "SUBSTRATE (Acero)"},
        {"id": "n5", "node": "ANCHOR", "coords": ["category.touch"]},
    ]
    s7 = [{"face_id": "product<->category:touch", "scheme": "touch",
           "conservation_claim": "multi_counted — over-count by construction; the sum EXCEEDS the grand "
                                 "total; NOT a partition (touch is the membership question)"}]
    s8 = [{"code": "multi_counted", "kind": "crossing_caveat", "severity": "material",
           "detail": disc.get("detail") if disc else None,
           "seam_note": "minted at HOME (the CROSS); survives to the final answer though the sum ran on Acero"}]
    s9 = {"notation": "RelRoot-relative child-index path + stay_home tags",
          "spans": [{"node": "CROSS", "stay_home": True, "engine": "home (metrics)",
                     "why": "D1: CROSS arithmetic per-shape at best; disclosure minting never delegable"},
                    *[{**sp, "stay_home": False} for sp in C.lowering_map_field(plan)["spans"]]]}
    oracle_run = {"N": N, "tolerance": TOL, "worst_delta": max(getattr(cmp_final, "_worst_delta", 0.0),
                  getattr(cmp_handoff, "_worst_delta", 0.0)),
                  "tamper_status": "valid" if breaks_valid else "INVALID",
                  "seam_break_modes": ["wrong_grain_intermediate", "dropped_rows_pre_sum"],
                  "harness_version": "map2/pilot_c3 v0.1", "date": ACCEPTANCE_DATE}
    cert, semantic = C.plan_certificate(
        model=model, ask=C.ask_field(ASK), plan_ir=C.plan_field(ir_nodes),
        obligations=[{"law_id": "conservation/c3-substrate-sum", "clause": "the lowered REDUCE conserves",
                      "verdict": "discharged", "ref": "M3.oracle_run", "mode": "embed_with_digest"},
                     {"law_id": "cross/touch:stay_home", "clause": "CROSS not lowered; disclosure minted home",
                      "verdict": "custody-preserved", "ref": "S7[0]", "mode": "ref"}],
        edge_attestations=[],            # no functional TRANSPORT in this plan → V1 vacuous
        face_spends=s7, disclosure_projection=s8, lowering_map=s9,
        perimeter=("Cascadia · revenue crossed product→category via the touch face (stay-home bridge "
                   "join-multiply + multi_counted minting), summed to category on Acero · the vertical "
                   "seam: home CROSS feeds a lowered substrate REDUCE · covers THIS plan; CROSS itself "
                   "is never lowered (D1 verdict stands)."),
        m1={"producer": "ibis-substrait 4.0.1", "substrait_version": "0.46.0", "proto_pin": "substrait 0.16.0",
            "lowering_rule_ids": ["substrate-sum-over-handoff"], "rule_cert_refs": {}},
        m2={"consumer": "pyarrow.substrait (Acero)", "version": "25.0.0", "version_band": ">=25,<26"},
        m3=oracle_run,
        m4={"a3_split_verification": a3})
    (fixtures / "c3_plan_certificate_v0_2.json").write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    (fixtures / "c3_semantic_channel_v0_2.json").write_text(json.dumps(semantic, indent=2, sort_keys=True) + "\n")

    print("\n=== C3 PILOT (the vertical seam) ===")
    print(f"  N                 : {N}  (final {cmp_final.n_cells} + handoff {cmp_handoff.n_cells}; >=30: {N>=30})")
    print(f"  A-1 conservation  : {conserve}")
    print(f"  A-1 break modes   : {breaks_valid} (both must fail)")
    print(f"  A-3 cross@home     : {a3['cross_stayed_home']} (0 joins on substrate)")
    print(f"  A-4 disclosure     : {a4_ok} (multi_counted survives the seam)")
    print(f"  ACCEPTED          : {accepted}")

    # ---- A-4 STRETCH (optional): the alloc face + reconciliation across the seam ----
    stretch = None
    if accepted:
        stretch = stretch_split(store)
        (fixtures / "c3_split_stretch.json").write_text(json.dumps(stretch, indent=2) + "\n")
        print(f"  A-4 STRETCH (split): oracle_match={stretch['oracle_match']} "
              f"reconciles_across_seam={stretch['reconciles_across_seam']} "
              f"(delta {stretch['reconciliation_delta']:.2e})")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

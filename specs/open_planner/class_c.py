#!/usr/bin/env python3
"""Deliverable 4 — Class C: the observationally-equivalent trap and the M0 -> M1 perturbation.

    python specs/open_planner/class_c.py specs/open_planner/fixtures/

RESEARCH INSTRUMENTATION ONLY. Builds its minted warehouses under a temp dir and reads the shipped
packages. The shipped demo data is COPIED, never mutated.

--------------------------------------------------------------------------------------------------
WHY CLASS C EXISTS
--------------------------------------------------------------------------------------------------
Class C is the proof that **no finite set of output observations establishes faithfulness.** Two
plans with DIFFERENT denotations produce IDENTICAL outputs on the current data; add one chosen row
and they diverge. If outputs could certify plans, these two would be certified identical — and they
are not the same question.

THE PAIR

    PLAN A   SELECT revenue AT {category.touch}     -- revenue reaches EVERY category a product
                                                       sits in; deliberately multi-counted
    PLAN B   SELECT revenue AT {category.primary}   -- revenue assigned to each product's
                                                       top-priority category; single-counted

These denote genuinely different questions. The shipped Manifold says so in its own face
declarations: `touch` "totals exceed the grand total"; `primary` "totals match the grand total".

--------------------------------------------------------------------------------------------------
THE AUDIT THAT CAME FIRST (A1 Part 2(C) route (a)), and why it sent us to route (b)
--------------------------------------------------------------------------------------------------
Route (a) was to find a NATURAL coincidence in the shipped warehouse. Audited, and reported honestly
rather than skipped:

  * touch vs primary, per category on the shipped data: exactly ONE coincidence, **G11**
    (301693.50 == 301693.50). Cause: G11 holds priority 1, the minimum, so every product touching
    G11 has G11 as its primary. That is a real data coincidence — but it is ROBUST: no single added
    row can break it, because no category can outrank priority 1. A coincidence that cannot be
    perturbed is useless for the M0 -> M1 protocol, so it is recorded and set aside.
  * split vs primary, per category: NO coincidence anywhere.
  * no category has all-single-membership products (every one of the twelve has 33-46 multi-
    membership products), so the "all products single" coincidence does not occur naturally.

Route (a) is therefore exhausted on this data, and A1's sanctioned route (b) — MINT the fixture —
is taken. The audit is part of the deliverable: knowing the natural coincidence is absent is a
result, and G11 is a genuine finding kept beside the minted pair.

--------------------------------------------------------------------------------------------------
THE MINTED PAIR
--------------------------------------------------------------------------------------------------
M0 — the shipped Cascadia warehouse with `product_categories` reduced to ONE membership per product
     (every other table byte-identical). With no product in two categories, `touch` and `primary`
     cannot differ: each product's revenue reaches exactly one category, and that category is
     trivially its top-priority one. **The two plans agree on every row.**

     THIS IS COINCIDENCE BY DATA, NOT BY MEANING. The plans still denote different questions; they
     agree only because this data contains no multi-membership to multi-count. A1 warned that a
     carve to single-membership products would be semantic EQUIVALENCE and thus not an attack — the
     difference here is that nothing in the ASK or the PLAN restricts to single membership. The
     plans are the full, unrestricted face plans; it is the *warehouse* that happens to make them
     agree, and one row changes that.

M1 — M0 plus exactly ONE row in `product_categories`: a product already in category G gains a
     membership in a LOWER-priority category H. Its primary is unchanged (G still outranks H), so
     PLAN B is unmoved. But `touch` now credits that product's revenue to H as well, so PLAN A
     gains revenue at H. **The outputs diverge, at one cell, from one row.**
"""

from __future__ import annotations

import json
import pathlib
import shutil
import sys
import tempfile

PLAN_A = "SELECT revenue AT {category.touch}"      # multi-counted
PLAN_B = "SELECT revenue AT {category.primary}"    # single-counted


def _mint(src_manifold: pathlib.Path, dest: pathlib.Path, add_row=None) -> pathlib.Path:
    """Copy the shipped cascadia manifold dir, collapse memberships to one per product, optionally
    add exactly one membership row. Returns the *parent* dir (a ManifoldStore root)."""
    import duckdb

    root = dest / "mint"
    mdir = root / "cascadia"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(src_manifold, mdir)

    wh = mdir / "warehouse"
    con = duckdb.connect()
    con.execute(f"create view pc as select * from '{wh}/product_categories.parquet'")
    con.execute(f"create view ca as select * from '{wh}/category_attributes.parquet'")
    # ONE membership per product: keep the top-priority category (so `primary` is unchanged by the
    # collapse — the minted M0 differs from the shipped data only by REMOVING secondary memberships).
    con.execute("""
        create table single as
        with ranked as (select pc.product_id, pc.category_id,
                row_number() over (partition by pc.product_id order by ca.priority asc) rn
            from pc join ca on ca.category_id = pc.category_id)
        select product_id, category_id from ranked where rn = 1
    """)
    if add_row is not None:
        pid, cid = add_row
        con.execute("insert into single values (?, ?)", [pid, cid])
    con.execute(f"copy single to '{wh}/product_categories.parquet' (format parquet)")
    con.close()
    return root


def _pick_perturbation(src_manifold: pathlib.Path) -> tuple:
    """Choose the one row: a product whose (single) category is NOT the lowest priority, paired with
    a strictly LOWER-priority category, so `primary` provably does not move."""
    import duckdb
    wh = src_manifold / "warehouse"
    con = duckdb.connect()
    con.execute(f"create view pc as select * from '{wh}/product_categories.parquet'")
    con.execute(f"create view ca as select * from '{wh}/category_attributes.parquet'")
    con.execute(f"create view tx as select * from '{wh}/transactions.parquet'")
    row = con.execute("""
        with ranked as (select pc.product_id, pc.category_id, ca.priority,
                row_number() over (partition by pc.product_id order by ca.priority asc) rn
            from pc join ca on ca.category_id = pc.category_id),
        prim as (select product_id, category_id, priority from ranked where rn = 1),
        rev as (select product_id, sum(amount) r from tx group by 1)
        select p.product_id, p.category_id, p.priority, lo.category_id, lo.priority, rev.r
        from prim p join rev using(product_id)
        join ca lo on lo.priority > p.priority
        order by rev.r desc, lo.priority desc
        limit 1
    """).fetchone()
    con.close()
    return row       # (product, its_category, its_priority, lower_cat, lower_priority, revenue)


def _run(store_root: pathlib.Path, q: str) -> dict:
    from columna_server import tools as T
    from columna_server.store import ManifoldStore
    store = ManifoldStore(str(store_root))
    wire = T.query(store, "cascadia", q)
    col = (wire.get("columns") or [{}])[0]
    key = "category.touch" if "touch" in q else "category.primary"
    return {"outcome": wire.get("outcome"),
            "values": {v[key]: round(v["value"], 6) for v in (col.get("values") or [])}}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    outdir = pathlib.Path(argv[1])
    outdir.mkdir(parents=True, exist_ok=True)

    from columna_server.demo import demo_dir
    src = pathlib.Path(demo_dir()) / "cascadia"

    pid, gcat, gpri, hcat, hpri, prev = _pick_perturbation(src)
    print(f"perturbation row chosen: product {pid} (revenue {prev:.2f}) currently in {gcat} "
          f"(priority {gpri}); adding membership in {hcat} (priority {hpri}, strictly lower)")

    with tempfile.TemporaryDirectory() as td:
        t = pathlib.Path(td)
        m0 = _mint(src, t / "m0")
        a0, b0 = _run(m0, PLAN_A), _run(m0, PLAN_B)
        m1 = _mint(src, t / "m1", add_row=(pid, hcat))
        a1, b1 = _run(m1, PLAN_A), _run(m1, PLAN_B)

    agree0 = a0["values"] == b0["values"]
    agree1 = a1["values"] == b1["values"]
    diverged = {k: {"plan_a": a1["values"].get(k), "plan_b": b1["values"].get(k)}
                for k in sorted(set(a1["values"]) | set(b1["values"]))
                if a1["values"].get(k) != b1["values"].get(k)}

    payload = {
        "pair": {"plan_a": PLAN_A, "plan_b": PLAN_B,
                 "denotations_differ": ("touch multi-counts across every membership (totals exceed "
                                        "the grand total); primary single-counts to the top-priority "
                                        "category (totals match the grand total) -- the shipped "
                                        "Manifold says so in its own face declarations")},
        "natural_coincidence_audit": {
            "touch_vs_primary_coincidences": ["G11"],
            "G11_cause": "G11 holds priority 1 (the minimum), so every product touching it has it as primary",
            "G11_usable_for_perturbation": False,
            "G11_why_not": "robust -- no category can outrank priority 1, so no single row breaks it",
            "split_vs_primary_coincidences": [],
            "all_single_membership_categories": [],
            "conclusion": "route (a) exhausted on this data; A1's sanctioned route (b) taken",
        },
        "M0": {"description": "shipped warehouse, memberships collapsed to one per product",
               "plan_a": a0, "plan_b": b0, "outputs_identical": agree0},
        "M1": {"description": f"M0 + ONE row: product {pid} also in {hcat} (priority {hpri} > {gpri})",
               "perturbation_row": {"product_id": pid, "category_id": hcat,
                                    "product_revenue": prev,
                                    "primary_unchanged_because": f"{gcat} (priority {gpri}) still outranks {hcat} (priority {hpri})"},
               "plan_a": a1, "plan_b": b1, "outputs_identical": agree1,
               "diverged_cells": diverged},
        "class_c_established": bool(agree0 and not agree1),
        "the_lesson": ("identical outputs on M0, different outputs on M1, from ONE row -- so no "
                       "finite set of output observations establishes faithfulness. Only plan |= ask "
                       "separates these two, and it separates them on M0 just as surely as on M1, "
                       "where the outputs happen to agree."),
    }
    (outdir / "class_c_pair.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {outdir / 'class_c_pair.json'}")

    print()
    print("M0  plan A == plan B ?", agree0, " (outcomes %s / %s)" % (a0["outcome"], b0["outcome"]))
    print("M1  plan A == plan B ?", agree1, " (outcomes %s / %s)" % (a1["outcome"], b1["outcome"]))
    if diverged:
        print("  diverged cells after ONE added row:")
        for k, v in diverged.items():
            print("    %-6s plan_a(touch) %14.4f   plan_b(primary) %14.4f   delta %+.4f"
                  % (k, v["plan_a"], v["plan_b"], v["plan_a"] - v["plan_b"]))
    print()
    print("CLASS C ESTABLISHED:", payload["class_c_established"])
    return 0 if payload["class_c_established"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

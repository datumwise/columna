#!/usr/bin/env python3
"""Attack B — the lawful-but-unfaithful exhibit, executed three ways and frozen.

    python specs/open_planner/attack_b.py specs/open_planner/fixtures/

RESEARCH INSTRUMENTATION ONLY. This file imports the shipped packages and calls their public and
internal primitives; it modifies nothing. No product surface changes, no engine edits. If this file
were deleted the shipped system would be byte-identical.

WHAT THE EXHIBIT IS. Ask: the mean revenue per month.
  FAITHFUL   — mean over transaction atoms (the FrameQL denotation).
  UNFAITHFUL — sum at store*product*cal.month, THEN mean of those sums.
Every node in the unfaithful plan is lawful (sum is the extensive family's transport; mean is a legal
reducer). The COMPOSITION denotes a different statistic. Node legality -> plan legality -> plan
faithfulness: three distinct levels, and only the third catches this.

THE THREE PATHS, and why all three are run rather than one:

  (1) DIRECT   — duckdb over the parquet, mirroring the two IR compositions. Reproduces the desk's
                 published numbers on an INDEPENDENT path. This is the verification of the arithmetic.
  (2) ASK      — the shipped FrameQL ask surface. The faithful half is reachable (as `aov`); the
                 unfaithful half is NOW ALSO reachable, as its own well-formed ask — see FINDING F1.
  (3) IR       — the engine's own primitives, composed BELOW the ask surface: engine.resolve(...)
                 then engine.reduce_series_to_anchor(...). This is the attack's NATIVE layer, because
                 the threat model is a searcher emitting IR, not a human typing an ask.

Agreement across all three is the point: the same statistic, reached by three independent routes.

FINDING F1 — RESOLVED by WP-GRAIN-1 (ratified Huayin 2026-07-29; shipped 0.13.4). Originally a
recall row (not a safety bug — ruled Huayin 2026-07-27): the unfaithful plan needs a MULTI-LEVEL
input anchor, which the build refused by name. WP-GRAIN-1 lifts that restriction — the composite
input anchor is now a first-class pin — so the two-stage statistic is now UTTERABLE, and when
uttered it SERVES, carrying the immaterial provenance note that names the reading. This does not
weaken the exhibit; it CONFIRMS the doctrine below: once askable, the ask is its own faithful
denotation, and the ask-surface value now equals the below-surface IR value it composes. The
searcher's channel is still where the kernel begins — the grammar's protection is about the gap
between plan and ask, and an ask cannot be unfaithful to itself.

THE DOCTRINE THIS EXHIBIT MINTS (Huayin, 2026-07-27, verbatim — realized in WP-GRAIN-1):

    An expressible pinned ask is its own denotation — avg(revenue @ {store*product*month}), once
    askable, is a different question, faithfully answered. No ask can be unfaithful to itself;
    unfaithfulness lives only in the gap between a plan and an ask — which is why obligation B has
    no ask-surface analogue, why the shipped mood contract already CLARIFIES on the underdetermined
    form, and why the kernel begins exactly where the grammar's protection ends: at the searcher's
    channel.
"""

from __future__ import annotations

import json
import pathlib
import sys

DESK = {                       # A1 §7b / deposit §5 — the published numbers this beat reproduces
    "2024-01": (139.91, 164.03), "2024-02": (125.81, 145.22), "2024-03": (127.25, 149.38),
    "2024-04": (137.91, 156.09), "2024-05": (139.14, 158.48), "2024-06": (130.56, 152.41),
}
DESK_OVERALL_RATIO = 1.21
ATOM_GRAIN = ("customer", "store", "product", "day")          # the transaction universe's own grain
UNFAITHFUL_GRAIN = ("store", "product", "cal.month")          # the intermediate collapse


# ---- path 1: direct, over the warehouse parquet (independent of the engine) ----------------------

def run_direct(warehouse: pathlib.Path) -> dict:
    import duckdb
    c = duckdb.connect()
    c.execute(f"create view tx  as select * from '{warehouse}/transactions.parquet'")
    c.execute(f"create view cal as select * from '{warehouse}/calendar.parquet'")

    faithful = c.execute("""
        with atoms as (select customer_id, store_id, product_id, day, sum(amount) rev
                       from tx group by 1,2,3,4)
        select c.month, avg(a.rev) from atoms a join cal c on c.day = a.day group by 1
    """).fetchall()
    unfaithful = c.execute("""
        with sums as (select c.month, t.store_id, t.product_id, sum(t.amount) rev
                      from tx t join cal c on c.day = t.day group by 1,2,3)
        select month, avg(rev) from sums group by 1
    """).fetchall()
    o_f = c.execute("""with atoms as (select customer_id,store_id,product_id,day,sum(amount) rev
                       from tx group by 1,2,3,4) select avg(rev) from atoms""").fetchone()[0]
    o_u = c.execute("""with sums as (select c.month,t.store_id,t.product_id,sum(t.amount) rev
                       from tx t join cal c on c.day=t.day group by 1,2,3) select avg(rev) from sums""").fetchone()[0]

    # THE COINCIDENCE CHECK, kept because the whole exhibit leans on it. `aov = revenue/orders`
    # matches the atom-mean only if transaction rows are 1:1 with atoms. They are NOT quite: 19995
    # rows, 19994 distinct atoms — exactly one collision. It falls outside the published window, so
    # aov reproduces the desk's faithful column there; asserting equality globally would be wrong.
    rows = c.execute("select count(*) from tx").fetchone()[0]
    atoms = c.execute("select count(*) from (select distinct customer_id,store_id,product_id,day from tx)").fetchone()[0]

    return {
        "faithful": dict(faithful), "unfaithful": dict(unfaithful),
        "overall": {"faithful": o_f, "unfaithful": o_u, "ratio": o_u / o_f},
        "atom_coincidence": {"transaction_rows": rows, "distinct_atoms": atoms,
                             "collisions": rows - atoms,
                             "note": "aov == atom-mean only where no collision falls in the window"},
    }


# ---- path 2: the shipped ask surface --------------------------------------------------------------

def run_ask(store) -> dict:
    from columna_server import tools as T

    out: dict = {}

    # The faithful half IS reachable — as `aov` (revenue/orders), a served ask.
    r = T.query(store, "cascadia", "SELECT aov AT {cal.month}")
    out["faithful_ask"] = {
        "frameql": "SELECT aov AT {cal.month}", "outcome": r["outcome"],
        "values": {v["cal.month"]: v["value"] for v in r["columns"][0]["values"]},
    }

    # THE CLARIFY EXHIBIT — Two Anchors doctrine running on the wire, today. The underdetermined
    # form is not silently resolved to either horn; the mood contract names the ambiguity and offers
    # the pin. Recorded because it is the live proof that the grammar catches the two horns by
    # STRUCTURE, before any kernel exists.
    r = T.query(store, "cascadia", "SELECT avg(revenue) AT {cal.month}")
    col = r["columns"][0]
    out["clarify_exhibit"] = {
        "frameql": "SELECT avg(revenue) AT {cal.month}", "outcome": r["outcome"],
        "detail": (col.get("no_result") or {}).get("detail"),
        "alternatives": (col.get("no_result") or {}).get("alternatives"),
    }

    # F1 — the unfaithful half, NOW EXPRESSIBLE (WP-GRAIN-1, ratified 2026-07-29; 0.13.4). The
    # composite input anchor lifts the single-level restriction: the two-stage statistic is now a
    # well-formed ask that SERVES, carrying the immaterial provenance note that names the reading.
    # No ask can be unfaithful to itself (the minted doctrine) — the ask-surface value now equals the
    # below-surface IR value it composes, which is the whole point of the flip.
    out["f1_unfaithful_now_expressible"] = []
    for q in ("SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}",
              "SELECT avg(revenue @ {customer*store*product*day}) AT {cal.month}"):
        r = T.query(store, "cascadia", q)
        col = r["columns"][0] if r.get("columns") else {}
        out["f1_unfaithful_now_expressible"].append({
            "frameql": q, "outcome": r["outcome"],
            "note": next((d.get("detail") for d in (col.get("disclosures") or [])), None),
            "values": {v["cal.month"]: v["value"] for v in (col.get("values") or [])},
        })
    return out


# ---- path 3: the IR layer, below the ask surface (the attack's native layer) -----------------------

def run_ir(store) -> dict:
    """Compose the two plans from the engine's OWN primitives. No engine modification: `resolve` and
    `reduce_series_to_anchor` are called exactly as the planner calls them (`planner.py:1114`)."""
    eng = store.get("cascadia").server.engine

    def compose(input_grain, target, member, measure="revenue", fam="sum"):
        # IR node 1 — COLUMN(measure, fam) resolved AT input_grain.
        frame, _disc = eng.resolve(measure, fam, tuple(input_grain))
        frame = frame.rename({"_value": "_v"})              # the series reducer's value column
        # IR node 2 — REDUCE(member @ target), collapsing the remaining input axes.
        out = eng.reduce_series_to_anchor(frame, tuple(input_grain), tuple(target), member)
        return out[0] if isinstance(out, tuple) else out

    def as_map(df):
        return {r[0]: r[1] for r in df.iter_rows()}

    def scalar(df):
        return df.row(0)[-1]

    faithful = as_map(compose(ATOM_GRAIN, ("cal.month",), "mean"))
    unfaithful = as_map(compose(UNFAITHFUL_GRAIN, ("cal.month",), "mean"))
    o_f = scalar(compose(ATOM_GRAIN, (), "mean"))
    o_u = scalar(compose(UNFAITHFUL_GRAIN, (), "mean"))

    return {
        "faithful_ir": {"nodes": [f"COLUMN(revenue, sum) @ {list(ATOM_GRAIN)}",
                                  "REDUCE(mean @ ['cal.month'])"], "values": faithful},
        "unfaithful_ir": {"nodes": [f"COLUMN(revenue, sum) @ {list(UNFAITHFUL_GRAIN)}",
                                    "REDUCE(mean @ ['cal.month'])"], "values": unfaithful},
        "overall": {"faithful": o_f, "unfaithful": o_u, "ratio": o_u / o_f},
        "engine_modified": False,
        "primitives_used": ["ColumnEngine.resolve (engine.py:84)",
                            "ColumnEngine.reduce_series_to_anchor (engine.py:598)"],
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    outdir = pathlib.Path(argv[1])
    outdir.mkdir(parents=True, exist_ok=True)

    from columna_server.demo import demo_dir, demo_store
    store = demo_store()
    warehouse = pathlib.Path(demo_dir()) / "cascadia" / "warehouse"

    direct, ask, ir = run_direct(warehouse), run_ask(store), run_ir(store)

    # ---- the agreement check, asserted rather than eyeballed --------------------------------------
    agreement = {"months": {}, "all_agree": True}
    for m, (df, du) in DESK.items():
        row = {
            "desk": {"faithful": df, "unfaithful": du},
            "direct": {"faithful": direct["faithful"][m], "unfaithful": direct["unfaithful"][m]},
            "ir": {"faithful": ir["faithful_ir"]["values"][m],
                   "unfaithful": ir["unfaithful_ir"]["values"][m]},
            "ask_faithful": ask["faithful_ask"]["values"][m],
        }
        # 0.005 because the desk published to two decimals; anything wider would hide a real gap.
        ok = (abs(row["direct"]["faithful"] - df) < 0.005
              and abs(row["direct"]["unfaithful"] - du) < 0.005
              and abs(row["ir"]["faithful"] - df) < 0.005
              and abs(row["ir"]["unfaithful"] - du) < 0.005
              and abs(row["ask_faithful"] - df) < 0.005)
        row["agrees"] = ok
        agreement["all_agree"] &= ok
        agreement["months"][m] = row
    agreement["overall"] = {
        "desk_ratio": DESK_OVERALL_RATIO,
        "direct_ratio": direct["overall"]["ratio"],
        "ir_ratio": ir["overall"]["ratio"],
        "agrees": abs(direct["overall"]["ratio"] - DESK_OVERALL_RATIO) < 0.005
        and abs(ir["overall"]["ratio"] - DESK_OVERALL_RATIO) < 0.005,
    }

    # F1 FLIP (WP-GRAIN-1): the unfaithful UNFAITHFUL_GRAIN ask now SERVES, and its per-month values
    # name the SAME statistic as the IR composition it stands for — the surface and the below-surface
    # layer agree. The two are reached by INDEPENDENT paths (the planner's `_resolve_inline_reduction`
    # vs the raw `resolve` + `reduce_series_to_anchor`), so a residual at float precision (~5.7e-14
    # relative) is aggregation-ORDER non-associativity, not a denotational gap — NOISE, not a finding,
    # per the 0.13.1 tolerance doctrine (the same law that classified F4). "Serves, agrees within
    # noise" is a PASS; the residual is RECORDED (max_residual, below) so the number stays visible
    # rather than hidden by a loose bound (ruled Huayin 2026-07-30).
    ask_f1 = ask["f1_unfaithful_now_expressible"][0]          # the {store*product*cal.month} query
    ir_unfaithful = ir["unfaithful_ir"]["values"]
    months = sorted(set(ask_f1["values"]) & set(ir_unfaithful))
    max_residual = max((abs(ask_f1["values"][m] - ir_unfaithful[m]) for m in months), default=None)
    agreement["f1_ask_equals_ir"] = {
        "frameql": ask_f1["frameql"], "outcome": ask_f1["outcome"],
        "same_months": set(ask_f1["values"]) == set(ir_unfaithful),
        "max_residual": max_residual,                         # float-precision residual, reported not hidden
        "agrees_to_float_precision": ask_f1["outcome"] in ("serve", "disclose")
        and set(ask_f1["values"]) == set(ir_unfaithful)
        and max_residual is not None and max_residual < 1e-9, # a residual this small is float order, not a gap
    }
    agreement["all_agree"] &= agreement["f1_ask_equals_ir"]["agrees_to_float_precision"]

    for name, payload in [("attack_b_direct.json", direct), ("attack_b_ask.json", ask),
                          ("attack_b_ir.json", ir), ("attack_b_agreement.json", agreement)]:
        (outdir / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {outdir / name}")

    print()
    print("month     desk_f  direct_f      ir_f     ask_f |  desk_u  direct_u      ir_u | agrees")
    for m in sorted(DESK):
        r = agreement["months"][m]
        print("%s  %7.2f  %8.2f  %8.2f  %8.2f | %7.2f  %8.2f  %8.2f | %s"
              % (m, r["desk"]["faithful"], r["direct"]["faithful"], r["ir"]["faithful"],
                 r["ask_faithful"], r["desk"]["unfaithful"], r["direct"]["unfaithful"],
                 r["ir"]["unfaithful"], "YES" if r["agrees"] else "NO"))
    print()
    print("overall ratio — desk %.4f · direct %.4f · IR %.4f"
          % (DESK_OVERALL_RATIO, direct["overall"]["ratio"], ir["overall"]["ratio"]))
    print("ALL AGREE:", agreement["all_agree"] and agreement["overall"]["agrees"])
    return 0 if (agreement["all_agree"] and agreement["overall"]["agrees"]) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

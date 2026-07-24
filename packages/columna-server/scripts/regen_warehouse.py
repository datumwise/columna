#!/usr/bin/env python3
"""
regen_warehouse.py — regenerate the Cascadia demo's UNBOUND / reference tables so the warehouse COHERES
with its transaction ground truth (warehouse-coherence defect, Huayin 2026-07-19; found by a stranger-
read of the generated exhibits: FK coverage was 2,051/19,995 and the summaries ran 10-15× off base truth,
contradicting the ratified burn story where they are *plausibly* wrong, not wildly so).

DOCTRINE. `transactions` and `eom_inventory` are the GROUND TRUTH — UNTOUCHED here — because every recorded
number (the measures, the E1-E10 seeds, the two transcripts) delivers from them; the only lawful fix is to
make the reference/summary tables cohere with those facts. Each summary is regenerated DERIVED-THEN-DEGRADED:
its value computed from base truth, then wearing exactly the one story-sin it exists to teach — plausibly
wrong, in a nameable way, never wild.

Deterministic (stable hashing on the id; no RNG), so the warehouse is reproducible byte-for-byte. Writes the
seven regenerated parquets in place; leaves transactions / eom_inventory / calendar / categories / products /
stores / product_categories / warehouse_notes alone.

Run:  python packages/columna-server/scripts/regen_warehouse.py
"""
import hashlib
import os

import duckdb
import polars as pl

WH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "src", "columna_server", "demo", "cascadia", "warehouse")


def _p(name):
    return os.path.join(WH, f"{name}.parquet")


def _h(*parts):
    """Stable unsigned-int hash of the parts (md5 — deterministic across runs, unlike hash())."""
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest(), 16)


def main():
    con = duckdb.connect()
    tx = con.execute(f"SELECT * FROM read_parquet('{_p('transactions')}')").pl()
    eom = con.execute(f"SELECT * FROM read_parquet('{_p('eom_inventory')}')").pl()
    cal = con.execute(f"SELECT * FROM read_parquet('{_p('calendar')}')").pl()
    day_to_month = dict(zip(cal["day"].to_list(), cal["month"].to_list()))

    # ── customers — GROWS to cover the full transaction customer-id space (100% FK coverage). Region is the
    #    MODAL customer_region from that customer's own transactions (a customer denormalizes one region onto
    #    its rows, but a few drift — take the majority). segment / signup_date / name are deterministic. ──
    reg = (tx.group_by(["customer_id", "customer_region"]).agg(pl.len().alias("n"))
             .sort(["customer_id", "n", "customer_region"], descending=[False, True, False])
             .group_by("customer_id", maintain_order=True).first())
    first_day = tx.group_by("customer_id").agg(pl.col("day").min().alias("first_day"))
    cust = reg.join(first_day, on="customer_id").sort("customer_id")
    seg_of = lambda cid: ("premium", "business", "consumer", "consumer", "consumer")[_h("seg", cid) % 5]
    def signup(cid, first):
        # a plausible signup BEFORE the first transaction: 0-400 days earlier, deterministic
        import datetime as dt
        d = dt.date.fromisoformat(str(first)) - dt.timedelta(days=30 + _h("signup", cid) % 400)
        return d.isoformat()
    customers = pl.DataFrame({
        "customer_id": cust["customer_id"],
        "name": [f"Customer {c[1:]}" for c in cust["customer_id"].to_list()],
        "segment": [seg_of(c) for c in cust["customer_id"].to_list()],
        "region": cust["customer_region"],
        "signup_date": [signup(c, f) for c, f in zip(cust["customer_id"].to_list(), cust["first_day"].to_list())],
    })
    customers.write_parquet(_p("customers"))
    N = customers.height

    # ── daily_revenue_summary — TRUE daily revenue from transactions, minus EXACTLY its missing days. Keep the
    #    same day set already present (716/731); only the VALUES become true. Sin: 15 days silently absent. ──
    keep_days = set(con.execute(f"SELECT day FROM read_parquet('{_p('daily_revenue_summary')}')").pl()["day"].to_list())
    true_daily = tx.group_by("day").agg(pl.col("amount").sum().round(2).alias("revenue"))
    drs = true_daily.filter(pl.col("day").is_in(list(keep_days))).sort("day")
    drs.write_parquet(_p("daily_revenue_summary"))

    # ── monthly_avg_order_value — commits the TRANSACTION-FOR-ORDER substitution it exists to teach: the value
    #    divides monthly revenue by the transaction COUNT (not the order count), so it under-states true AOV by
    #    the lines-per-order factor. n_txns is TRUE. ──
    txm = tx.with_columns(pl.col("day").replace_strict(day_to_month).alias("month"))
    maov = (txm.group_by("month")
               .agg((pl.col("amount").sum() / pl.len()).round(2).alias("avg_order_value"),
                    pl.len().alias("n_txns"))
               .sort("month"))
    maov.write_parquet(_p("monthly_avg_order_value"))

    # ── monthly_unique_visitors — derived distinct buyers per month, with a STATED LEGACY SIN: the old job
    #    counted distinct customers per (month, STORE) and summed across stores, so a customer who shopped at
    #    k stores in a month is counted k times — the total sits ABOVE the true monthly distinct. ──
    muv = (txm.group_by(["month", "store_id"]).agg(pl.col("customer_id").n_unique().alias("u"))
              .group_by("month").agg(pl.col("u").sum().alias("unique_visitors"))
              .sort("month"))
    muv.write_parquet(_p("monthly_unique_visitors"))

    # ── monthly_store_inventory — derived per its sin: the ILLEGAL SUM of daily stock over the month (the exact
    #    semi-additive burn — summing a stock across time does not reconcile). Keep the same (store, month) key
    #    set already present. ──
    keep_sm = set(map(tuple, con.execute(
        f"SELECT store_id, month FROM read_parquet('{_p('monthly_store_inventory')}')").pl().rows()))
    eomm = eom.with_columns(pl.col("day").replace_strict(day_to_month).alias("month"))
    msi = (eomm.group_by(["store_id", "month"]).agg(pl.col("level").sum().alias("total_inventory")))
    msi = msi.filter(pl.struct(["store_id", "month"]).map_elements(
        lambda s: (s["store_id"], s["month"]) in keep_sm, return_dtype=pl.Boolean)).sort(["store_id", "month"])
    msi.write_parquet(_p("monthly_store_inventory"))

    # ── support_tickets — redrawn from the REAL (new) customer distribution: 500 tickets, each on a real
    #    customer, a real transaction day, a topic. Deterministic pick over the customer id space. ──
    cids = customers["customer_id"].to_list()
    days = sorted(day_to_month)
    topics = ["billing", "shipping", "return", "product-question", "account"]
    st = pl.DataFrame({
        "ticket_id": [f"T{i:05d}" for i in range(1, 501)],
        "customer_id": [cids[_h("ticket-cust", i) % N] for i in range(1, 501)],
        "day": [days[_h("ticket-day", i) % len(days)] for i in range(1, 501)],
        "topic": [topics[_h("ticket-topic", i) % len(topics)] for i in range(1, 501)],
    })
    st.write_parquet(_p("support_tickets"))

    # ── engagement_scores — redrawn from real customers, keeping the story's "about half" coverage against the
    #    NEW N (a partial-coverage enrichment: it covers ~half the base — the OF-13/partial-coverage beat). ──
    covered = [c for c in cids if _h("engage", c) % 2 == 0]      # ~half, deterministic
    es = pl.DataFrame({
        "customer_id": covered,
        "score": [round(0.1 + (_h("score", c) % 900) / 1000, 3) for c in covered],
    })
    es.write_parquet(_p("engagement_scores"))

    # ── category_attributes — the THIRD universe's driver profile (0.12 "the triad completes"). 12 rows,
    #    one per category: a DISTINCT integer `priority` (1..12, a deterministic permutation — a rank-like
    #    driver, ORDER MIN in the demo) and a positive, varied, NOT-pre-normalized `alloc_weight` (a raw
    #    driver — normalization is the ALLOC face's declared law, applied by the engine, never stored).
    #    Deterministic (stable md5 on the id, no RNG → byte-reproducible); ADDITIVE (touches no existing
    #    table). Drives FACES { primary = ASSIGN BY priority ORDER MIN ; split = ALLOC BY alloc_weight }. ──
    cat_ids = con.execute(
        f"SELECT category_id FROM read_parquet('{_p('categories')}') ORDER BY category_id").pl()["category_id"].to_list()
    prio_order = sorted(cat_ids, key=lambda c: _h("priority", c))       # a deterministic permutation of the 12
    priority_of = {c: i + 1 for i, c in enumerate(prio_order)}          # distinct integers 1..12 (rank-like)
    catattr = pl.DataFrame({
        "category_id": cat_ids,
        "priority": [priority_of[c] for c in cat_ids],
        "alloc_weight": [round(0.5 + (_h("weight", c) % 950) / 100.0, 2) for c in cat_ids],  # 0.50..9.99, varied, raw
    })
    catattr.write_parquet(_p("category_attributes"))

    print(f"regenerated: customers={N}  daily_revenue_summary={drs.height}  "
          f"monthly_avg_order_value={maov.height}  monthly_unique_visitors={muv.height}  "
          f"monthly_store_inventory={msi.height}  support_tickets={st.height}  "
          f"engagement_scores={es.height} (~half of {N})")
    print(f"FINAL_CUSTOMER_N={N}")


if __name__ == "__main__":
    main()

"""
test_warehouse_coherence.py — the Cascadia demo warehouse COHERES with its transaction ground truth.

DEFECT THIS SUITE MAKES STRUCTURAL (Huayin 2026-07-19, found by a stranger-read of the generated
exhibits, verified at the desk): the reference/summary tables had drifted incoherent with the facts —
FK coverage was **2,051/19,995** transaction rows (customers held only 2,000 of ~10,157 distinct ids),
and the summaries ran **10-15× off** base truth, which *contradicted the ratified burn story* where the
stale summaries are *plausibly* wrong (the kind nobody notices), never wildly so. `transactions` and
`eom_inventory` are the ground truth and are UNTOUCHED; the fix regenerated the reference/summary tables
DERIVED-THEN-DEGRADED (each wearing exactly its one story-sin). This suite asserts that coherence holds:
100% FK coverage, every summary within its declared-sin tolerance of base truth, the engagement ratio.
"""
import os

import duckdb
import pytest

import columna_server

WH = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia", "warehouse")


@pytest.fixture(scope="module")
def con():
    c = duckdb.connect()
    for n in ("transactions", "customers", "eom_inventory", "calendar", "daily_revenue_summary",
              "monthly_avg_order_value", "monthly_unique_visitors", "monthly_store_inventory",
              "engagement_scores"):
        c.execute(f"CREATE VIEW {n} AS SELECT * FROM read_parquet('{os.path.join(WH, n + '.parquet')}')")
    c.execute("CREATE VIEW txm AS SELECT tx.*, cal.month FROM transactions tx JOIN calendar cal USING(day)")
    c.execute("CREATE VIEW eomm AS SELECT e.*, cal.month FROM eom_inventory e JOIN calendar cal USING(day)")
    return c


def test_customer_fk_coverage_is_total(con):
    # THE headline defect: every transaction customer_id must resolve to a customers row (was 992/10,157).
    uncovered = con.execute(
        "SELECT count(*) FROM (SELECT DISTINCT customer_id FROM transactions) x "
        "WHERE x.customer_id NOT IN (SELECT customer_id FROM customers)").fetchone()[0]
    assert uncovered == 0, f"{uncovered} transaction customer_ids have no customers row — FK coverage is not total"


def test_customers_is_exactly_the_transaction_id_space(con):
    # customers GREW to cover the id space and no further (no orphan reference rows either).
    distinct_tx = con.execute("SELECT count(DISTINCT customer_id) FROM transactions").fetchone()[0]
    n_cust = con.execute("SELECT count(*) FROM customers").fetchone()[0]
    assert n_cust == distinct_tx, f"customers={n_cust} != distinct tx customer_ids={distinct_tx}"


def test_daily_revenue_summary_is_true_minus_its_missing_days(con):
    # sin: 15 silently-absent days. Present days carry TRUE revenue.
    disagreeing = con.execute(
        "SELECT count(*) FROM daily_revenue_summary d JOIN "
        "(SELECT day, round(sum(amount),2) v FROM transactions GROUP BY day) t USING(day) "
        "WHERE d.revenue <> t.v").fetchone()[0]
    assert disagreeing == 0, "a present day's revenue disagrees with true daily revenue"
    missing = 731 - con.execute("SELECT count(*) FROM daily_revenue_summary").fetchone()[0]
    assert missing == 15, f"expected exactly 15 missing days (the sin), got {missing}"


def test_monthly_aov_commits_the_transaction_for_order_substitution(con):
    # sin: divides monthly revenue by TRANSACTION count (not order count); n_txns is true. The value is
    # within its declared sin (= monthly_rev / n_txns) of base truth, not wild.
    bad = con.execute(
        "SELECT count(*) FROM monthly_avg_order_value m JOIN "
        "(SELECT month, round(sum(amount)/count(*),2) v, count(*) n FROM txm GROUP BY month) t USING(month) "
        "WHERE m.avg_order_value <> t.v OR m.n_txns <> t.n").fetchone()[0]
    assert bad == 0, "monthly_avg_order_value is not (monthly revenue / true transaction count)"


def test_monthly_unique_visitors_wears_the_per_store_double_count(con):
    # sin: the legacy job counted distinct customers per (month, store) and summed — so it sits ABOVE the
    # true monthly distinct, but only mildly (a customer shops at few stores) — plausibly wrong, not wild.
    rows = con.execute(
        "SELECT m.unique_visitors, t.true_uv FROM monthly_unique_visitors m JOIN "
        "(SELECT month, count(DISTINCT customer_id) true_uv FROM txm GROUP BY month) t USING(month)").fetchall()
    for got, true_uv in rows:
        assert got >= true_uv, "unique_visitors below the true monthly distinct — wrong direction of sin"
        assert got <= true_uv * 1.5, f"unique_visitors {got} vs true {true_uv} — inflation beyond the plausible sin"


def test_monthly_store_inventory_is_the_illegal_sum_over_time(con):
    # sin: sums a STOCK across the month (the exact semi-additive burn) — derived from truth, not wild.
    bad = con.execute(
        "SELECT count(*) FROM monthly_store_inventory m JOIN "
        "(SELECT store_id, month, sum(level) v FROM eomm GROUP BY 1,2) t USING(store_id, month) "
        "WHERE m.total_inventory <> t.v").fetchone()[0]
    assert bad == 0, "monthly_store_inventory is not the sum of daily levels over the month"


def test_engagement_covers_about_half_the_customers(con):
    # the partial-coverage beat: enrichment covers ~half the base (the 'about half' story line).
    n_cust = con.execute("SELECT count(*) FROM customers").fetchone()[0]
    n_eng = con.execute("SELECT count(DISTINCT customer_id) FROM engagement_scores").fetchone()[0]
    # every engaged customer is a real customer (no orphans)
    orphans = con.execute(
        "SELECT count(*) FROM (SELECT DISTINCT customer_id FROM engagement_scores) x "
        "WHERE x.customer_id NOT IN (SELECT customer_id FROM customers)").fetchone()[0]
    assert orphans == 0, "engagement_scores references customers absent from the reference"
    ratio = n_eng / n_cust
    assert 0.45 <= ratio <= 0.55, f"engagement coverage {ratio:.2f} is not ~half"

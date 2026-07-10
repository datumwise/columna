"""Grounded numbers for the animation — recomputed from the packaged demo warehouse.

The grounding rule applies to marketing too: never invent a number, even in animation. Every
figure that appears on screen is computed *here* from the same warehouse the product ships, and
guarded against an expected value so a silent drift fails the build rather than showing a lie.

If the warehouse is missing (e.g. a code-only checkout), we fall back to the guarded constants —
the numbers are still real, just not re-derived on the spot. `SOURCED` records which path ran.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

_HERE = os.path.dirname(os.path.abspath(__file__))
_WH = os.path.normpath(
    os.path.join(
        _HERE,
        "..",
        "..",
        "packages",
        "columna-server",
        "src",
        "columna_server",
        "demo",
        "benchmark",
        "warehouse",
    )
)

# Guarded expectations (the drift-guard). Recomputation must match these to 2 dp.
_EXPECT = {
    "s1_amount": 58.26,        # a single transaction's amount, at one (store, day, product) point
    "s4_pooled": 139.91,       # aov @ 2024-01, transaction-grain -> month (pooled)
    "s4_daygrain": 140.90,     # aov @ 2024-01, day-grain -> month (mean of daily aov)
    "s5_last": 6066.0,         # inventory level, store S001, period-end of 2024-01 (LAST — valid)
    "s5_sum": 179656.0,        # inventory level summed over 2024-01 (BLOCKED — non-reconciling)
}

# Fixed identifying facts (not aggregates — coordinates and labels).
S1_STORE = "S001"
S1_PRODUCT = "P0512"
S1_DAY = "2024-01-03"
S4_MONTH = "2024-01"
S5_STORE = "S001"


@dataclass(frozen=True)
class Numbers:
    s1_amount: float
    s4_pooled: float
    s4_daygrain: float
    s5_last: float
    s5_sum: float
    s4_daily_aov: tuple  # the real per-day aov series for 2024-01 (the "fine day-columns")
    s5_daily_level: tuple  # the real per-day inventory level for S001, 2024-01 (the stock over time)
    sourced: str  # "warehouse" | "guarded-constants"


def _recompute() -> dict:
    import duckdb  # local import: only needed on the warehouse path

    con = duckdb.connect()
    T = f"read_parquet('{_WH}/transactions.parquet')"
    CAL = f"read_parquet('{_WH}/calendar.parquet')"
    INV = f"read_parquet('{_WH}/eom_inventory.parquet')"
    q = con.execute

    s1 = q(f"SELECT amount FROM {T} WHERE txn_id='T00000015'").fetchone()[0]
    pooled = q(
        f"SELECT sum(amount)/count(*) FROM {T} t JOIN {CAL} c ON t.day=c.day "
        f"WHERE c.month='{S4_MONTH}'"
    ).fetchone()[0]
    daygrain = q(
        f"WITH d AS (SELECT t.day, sum(amount)/count(*) aov FROM {T} t JOIN {CAL} c ON t.day=c.day "
        f"WHERE c.month='{S4_MONTH}' GROUP BY t.day) SELECT avg(aov) FROM d"
    ).fetchone()[0]
    last = q(
        f"SELECT level FROM {INV} WHERE store_id='{S5_STORE}' AND day=("
        f"  SELECT max(i2.day) FROM {INV} i2 JOIN {CAL} c ON i2.day=c.day "
        f"  WHERE i2.store_id='{S5_STORE}' AND c.month='{S4_MONTH}')"
    ).fetchone()[0]
    bad = q(
        f"SELECT sum(level) FROM {INV} i JOIN {CAL} c ON i.day=c.day "
        f"WHERE i.store_id='{S5_STORE}' AND c.month='{S4_MONTH}'"
    ).fetchone()[0]
    daily = q(
        f"SELECT sum(amount)/count(*) aov FROM {T} t JOIN {CAL} c ON t.day=c.day "
        f"WHERE c.month='{S4_MONTH}' GROUP BY t.day ORDER BY t.day"
    ).fetchall()
    levels = q(
        f"SELECT i.level FROM {INV} i JOIN {CAL} c ON i.day=c.day "
        f"WHERE i.store_id='{S5_STORE}' AND c.month='{S4_MONTH}' ORDER BY i.day"
    ).fetchall()
    return {
        "s1_amount": round(s1, 2),
        "s4_pooled": round(pooled, 2),
        "s4_daygrain": round(daygrain, 2),
        "s5_last": round(last, 0),
        "s5_sum": round(bad, 0),
        "s4_daily_aov": tuple(round(r[0], 2) for r in daily),
        "s5_daily_level": tuple(round(r[0], 0) for r in levels),
    }


def load() -> Numbers:
    if os.path.isdir(_WH):
        got = _recompute()
        for k, want in _EXPECT.items():
            assert abs(got[k] - want) < 0.01, (
                f"DRIFT: {k} recomputed={got[k]} expected={want} — the warehouse changed; "
                f"update the animation's guarded values deliberately."
            )
        daily = got["s4_daily_aov"]
        assert daily and abs(sum(daily) / len(daily) - _EXPECT["s4_daygrain"]) < 0.02, (
            "DRIFT: mean of the daily aov series no longer matches s4_daygrain."
        )
        lvl = got["s5_daily_level"]
        assert lvl and abs(lvl[-1] - _EXPECT["s5_last"]) < 0.5 and abs(sum(lvl) - _EXPECT["s5_sum"]) < 0.5, (
            "DRIFT: the daily level series no longer matches s5_last (LAST) / s5_sum (blocked SUM)."
        )
        return Numbers(**got, sourced="warehouse")
    # code-only checkout: real guarded scalars; the series are synthesized in-scene (no numerals)
    return Numbers(**_EXPECT, s4_daily_aov=(), s5_daily_level=(), sourced="guarded-constants")


NUM = load()

if __name__ == "__main__":
    n = NUM
    print(f"sourced: {n.sourced}")
    print(f"  s1 amount   = {n.s1_amount:.2f}   ({S1_STORE}, {S1_PRODUCT}, {S1_DAY})")
    print(f"  s4 pooled   = {n.s4_pooled:.2f}   (aov {S4_MONTH}, transaction-grain)")
    print(f"  s4 daygrain = {n.s4_daygrain:.2f}   (aov {S4_MONTH}, day-grain)")
    print(f"  s5 last     = {n.s5_last:.0f}   ({S5_STORE} inventory, period-end {S4_MONTH})")
    print(f"  s5 sum      = {n.s5_sum:.0f}   ({S5_STORE} inventory, BLOCKED sum over {S4_MONTH})")

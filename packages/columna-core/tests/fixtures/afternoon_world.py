"""The Afternoon fixture's world, in one readable place.

Every row is written out longhand so a reader can recompute any asserted number by eye — the point of
the Afternoon case is that a person can SEE the wrong answer being wrong, and a fixture whose numbers
must be taken on trust cannot carry that. Built in-process into DuckDB; nothing is committed as
parquet, so the data and the arithmetic that certifies it are the same artifact.

THE SHAPE OF THE LIE, in numbers. Store S1 in month 2025-01 has three daily snapshots — 500, 430 and
480 units. Its POSITION at month end is `last` = 480. Summing the snapshots gives 1410: the same
units counted once per day they sat on the shelf. 1410 is not a quantity of anything. It is the
Afternoon's whole argument, and it is the number every laundering spelling in the regression matrix
must be prevented from returning.

The three snapshots are deliberately DISTINCT, and distinct from their own mean (470) and extremes
(500, 430), so that no assertion in the matrix can pass by coincidence: a test that expects the
position and receives the average must fail, rather than agreeing by accident.
"""

STORES = [                     # store_id, region
    ("S1", "north"),
    ("S2", "north"),
    ("S3", "south"),
]

# `quarter` is carried explicitly rather than derived at query time: the Afternoon page gate asks at
# {region, quarter}, and a gate that computed its own coarse coordinate would be certifying the test's
# arithmetic instead of the engine's transport. Every day here falls in 2025-Q1, so the quarter row is
# a single hand-checkable bucket — deliberately, so beats 2 and 3 have one obvious right answer.
CALENDAR = [                   # day, month, quarter
    ("2025-01-06", "2025-01", "2025-Q1"),
    ("2025-01-13", "2025-01", "2025-Q1"),
    ("2025-01-20", "2025-01", "2025-Q1"),
    ("2025-02-03", "2025-02", "2025-Q1"),
    ("2025-02-10", "2025-02", "2025-Q1"),
]

INVENTORY = [                  # store_id, day, level   (the daily on-hand snapshot)
    ("S1", "2025-01-06", 500), ("S1", "2025-01-13", 430), ("S1", "2025-01-20", 480),
    ("S1", "2025-02-03", 510), ("S1", "2025-02-10", 505),
    ("S2", "2025-01-06", 300), ("S2", "2025-01-13", 280),
    ("S2", "2025-02-10", 320),
    ("S3", "2025-01-20", 220),
    ("S3", "2025-02-03", 240),
]

SALES_LINES = [                # store_id, day, order_id, amount
    ("S1", "2025-01-06", "O1", 120.0), ("S1", "2025-01-13", "O2",  80.0),
    ("S1", "2025-01-20", "O3", 100.0), ("S1", "2025-02-03", "O4",  90.0),
    ("S2", "2025-01-06", "O5", 200.0), ("S2", "2025-02-10", "O6", 300.0),
    ("S3", "2025-01-20", "O7", 150.0), ("S3", "2025-02-03", "O8", 125.0),
]

# ── the hand-checkable landmarks the matrix asserts against ──────────────────────────────────────
S1_JAN_POSITION = 480          # on_hand.last          @ {S1, 2025-01} — the LAWFUL answer
S1_JAN_STOCK_SUM = 1410        # 500 + 430 + 480       — the PROHIBITED total, in EVERY spelling
S1_JAN_MEAN = 470.0            # (500 + 430 + 480) / 3 — lawful: the author barred `sum`, not `mean`
S1_JAN_MAX = 500               # max(on_hand.last@day) — lawful, same reason
S1_JAN_MIN = 430               # min(on_hand.last@day) — lawful, same reason
S1_JAN_DAYS = 3                # count(on_hand.last@day)
S1_JAN_REVENUE = 300.0         # 120 + 80 + 100        — the flow, lawfully summed
JAN_POSITION_ACROSS_STORES = 980   # 480 + 280 + 220   — summing a stock across STORES is LAWFUL:
                                   # the bar names `calendar`, not the measure (per operator x lineage)

# ── the Afternoon page gate's coarse landmarks (beats 2 and 3), also hand-checkable ──────────────
# north = S1 + S2; south = S3. All five days fall in 2025-Q1, so the quarter holds every order.
NORTH_Q1_REVENUE = 890.0       # 120 + 80 + 100 + 90 + 200 + 300  — revenue @ {north, 2025-Q1}
SOUTH_Q1_REVENUE = 275.0       # 150 + 125                        — revenue @ {south, 2025-Q1}
NORTH_Q1_AVG_ORDER = 890.0 / 6  # 148.333…  — avg(revenue @ {order}) @ {north, 2025-Q1}, six orders
SOUTH_Q1_AVG_ORDER = 275.0 / 2  # 137.5     — avg(revenue @ {order}) @ {south, 2025-Q1}, two orders


def build(con):
    """Create the Afternoon world in an open DuckDB connection and return it."""
    con.execute("CREATE TABLE stores (store_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO stores VALUES (?, ?)", STORES)
    con.execute("CREATE TABLE calendar (day VARCHAR, month VARCHAR, quarter VARCHAR)")
    con.executemany("INSERT INTO calendar VALUES (?, ?, ?)", CALENDAR)
    con.execute("CREATE TABLE inventory (store_id VARCHAR, day VARCHAR, level BIGINT)")
    con.executemany("INSERT INTO inventory VALUES (?, ?, ?)", INVENTORY)
    con.execute("CREATE TABLE sales_lines "
                "(store_id VARCHAR, day VARCHAR, order_id VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO sales_lines VALUES (?, ?, ?, ?)", SALES_LINES)
    return con

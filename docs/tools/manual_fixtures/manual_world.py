"""The world the Frame-QL Manual's examples are planned against.

WHY THERE IS DATA AT ALL, when the gate never executes a query. Transport is CLOSED BY DEFAULT
(P0.5a): `PlannerView.certified_edges` starts empty, and until a manifold is PUBLISHED every ask that
must climb a declared edge plans as `refuse / uncertified_edge`. Certification comes only from
`publish()` -> `adjudicate()`, and adjudication proves its functional-dependency claims BY QUERYING
THE DATA. So a data-free fixture would answer `uncertified_edge` to most of the Manual — a fixture
artifact wearing the costume of a finding, which is the exact confusion this gate exists to remove.

The rows are therefore not decoration and not a sample: they are the evidence adjudication needs to
admit the edges the Manual's examples travel. They are kept tiny and longhand so a reader can see
that every functional claim the manifolds declare is actually true of them — `txn -> customer`,
`txn -> day`, `day -> month`, `month -> year`, `customer -> region`, `product -> category`. If a
claim were false here, adjudication would correctly refuse to certify it and the gate's results
would be about this file rather than about the Manual.

NOTHING HERE IS ASSERTED ON. No example's VALUE is checked against these numbers; the gate is about
plan-time disposition, not arithmetic. The data exists to unlock transport, and for no other reason.
"""

CUSTOMERS = [                  # customer_id, region
    ("C1", "east"), ("C2", "east"), ("C3", "west"),
]

CALENDAR = [                   # day, month, year
    ("2024-01-05", "2024-01", "2024"),
    ("2024-01-19", "2024-01", "2024"),
    ("2024-02-02", "2024-02", "2024"),
    ("2023-02-03", "2023-02", "2023"),
]

TXNS = [                # txn_id, customer_id, day, txn_date, product_id, amount, cost, aov
    ("T1", "C1", "2024-01-05", "2024-01-05", "P1", 120.0, 70.0, 60.0),
    ("T2", "C1", "2024-01-19", "2024-01-19", "P2",  80.0, 40.0, 40.0),
    ("T3", "C2", "2024-02-02", "2024-02-02", "P3", 200.0, 90.0, 100.0),
    ("T4", "C3", "2023-02-03", "2023-02-03", "P1", 150.0, 60.0, 75.0),
]

# A genuine many-to-many: P1 sits in TWO categories, which is what makes §5.6's three faces mean
# three different things rather than three spellings of one.
PRODUCT_CATEGORIES = [         # product_id, category_id, weight, rank
    # Ranks are globally distinct on purpose: ASSIGN designates ONE match and fails closed on a
    # tie, so a fixture with tied ranks would refuse to publish for a reason about the fixture.
    ("P1", "K1", 0.6, 1), ("P1", "K2", 0.4, 2),
    ("P2", "K1", 1.0, 3), ("P3", "K2", 1.0, 4),
]

PRODUCT_PRIMARY = [            # product_id, category_id  — FUNCTIONAL: one category per product
    ("P1", "K1"), ("P2", "K1"), ("P3", "K2"),
]

PRODUCT_SALES = [              # product_id, amount
    ("P1", 300.0), ("P2", 150.0), ("P3", 220.0),
]

STORES = [                     # store_id, region
    ("S1", "east"), ("S2", "west"),
]

INV = [                        # store_id, day, units   (the daily on-hand snapshot — a STOCK)
    ("S1", "2024-01-05", 500), ("S1", "2024-01-19", 430),
    ("S2", "2024-02-02", 300),
]

RTXNS = [        # txn_id, store_id, product_id, day, customer_id, amount
    ("R1", "S1", "P1", "2024-01-05", "C1", 120.0),
    ("R2", "S1", "P2", "2024-01-19", "C1",  80.0),
    ("R3", "S2", "P3", "2024-02-02", "C2", 200.0),
]

ENGAGEMENTS = [                # customer_id, week, score
    ("C1", "2024-W01", 4.0), ("C1", "2024-W02", 6.0),
    ("C2", "2024-W01", 5.0), ("C3", "2024-W02", 3.0),
]


def build(con):
    """Create the Manual's world in an open DuckDB connection and return it."""
    con.execute("CREATE TABLE customers (customer_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO customers VALUES (?, ?)", CUSTOMERS)
    con.execute("CREATE TABLE calendar (day VARCHAR, month VARCHAR, year VARCHAR)")
    con.executemany("INSERT INTO calendar VALUES (?, ?, ?)", CALENDAR)
    con.execute("CREATE TABLE txns (txn_id VARCHAR, customer_id VARCHAR, day VARCHAR, "
                "txn_date VARCHAR, product_id VARCHAR, amount DOUBLE, cost_amount DOUBLE, "
                "aov_amount DOUBLE)")
    con.executemany("INSERT INTO txns VALUES (?, ?, ?, ?, ?, ?, ?, ?)", TXNS)
    con.execute("CREATE TABLE product_categories "
                "(product_id VARCHAR, category_id VARCHAR, weight DOUBLE, rank BIGINT)")
    con.executemany("INSERT INTO product_categories VALUES (?, ?, ?, ?)", PRODUCT_CATEGORIES)
    con.execute("CREATE TABLE product_primary (product_id VARCHAR, category_id VARCHAR)")
    con.executemany("INSERT INTO product_primary VALUES (?, ?)", PRODUCT_PRIMARY)
    con.execute("CREATE TABLE product_sales (product_id VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO product_sales VALUES (?, ?)", PRODUCT_SALES)
    con.execute("CREATE TABLE stores (store_id VARCHAR, region VARCHAR)")
    con.executemany("INSERT INTO stores VALUES (?, ?)", STORES)
    con.execute("CREATE TABLE inv (store_id VARCHAR, day VARCHAR, units BIGINT)")
    con.executemany("INSERT INTO inv VALUES (?, ?, ?)", INV)
    con.execute("CREATE TABLE rtxns (txn_id VARCHAR, store_id VARCHAR, product_id VARCHAR, "
                "day VARCHAR, customer_id VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO rtxns VALUES (?, ?, ?, ?, ?, ?)", RTXNS)
    con.execute("CREATE TABLE engagements (customer_id VARCHAR, week VARCHAR, score DOUBLE)")
    con.executemany("INSERT INTO engagements VALUES (?, ?, ?)", ENGAGEMENTS)
    return con

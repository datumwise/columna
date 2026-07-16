"""
columna_server.init.benchmarks — the ratified eval benchmarks (B1–B11), encoded under the COHERENCE
LAW (Huayin, 2026-07-16): every ground-truth CLOSURE must be derivable from the schema's OWN evidence
(what `catalog()`/`profile()` actually emit). The self-coherence meta-check (`eval.benchmark_coherence`)
enforces this structurally. Schema shape: see `eval.build_aperture`. `GOLD[id]` is a perfect-mind
stand-in used only by the hermetic plumbing test; the real baseline uses the AnthropicProvider.

Kinds: ◆ oracle-asymmetric (the sharp human calls — basis · universe · M-leak · fertility · refutation)
must be surfaced in the review checklist; ○ mechanical (exactly gradeable).
"""
from .eval import Benchmark


def _t(cols, rows, pk=None, fk=None):
    return {"cols": cols, "rows": rows, **({"pk": pk} if pk else {}), **({"fk": fk} if fk else {})}


# ── B1 ◆ events vs spine ─────────────────────────────────────────────────────────────────────────
B1 = Benchmark(id="B1", kind="◆", title="events vs spine",
    schema={"tables": {
        "orders": _t([("order_id", "INTEGER"), ("amount", "DOUBLE")], [(1, 10.0), (2, 5.0)], pk=["order_id"]),
        "daily_inventory": _t([("store_id", "INTEGER"), ("day", "VARCHAR"), ("level", "DOUBLE")],
                              [(1, "d1", 100.0)])}},
    ground_truth={"closures": [["universe", "orders"], ["universe", "inventory"]], "grades": {},
                  "oracle_calls": ["basis: orders=events, inventory=spine?"], "max_checklist": 2})

# ── B2 ◆ stock measure hiding as additive ────────────────────────────────────────────────────────
B2 = Benchmark(id="B2", kind="◆", title="stock measure hiding as additive",
    schema={"tables": {"eom": _t([("store_id", "INTEGER"), ("month", "VARCHAR"), ("inventory_level", "DOUBLE")],
                                  [(1, "m1", 100.0), (1, "m2", 120.0)])}},
    ground_truth={"closures": [["measure", "inventory_level"]], "grades": {},
                  "oracle_calls": ["additivity: inventory_level is a STOCK — bar sum over calendar (last for period-end)?"],
                  "max_checklist": 2})

# ── B3 ◆ universe assignment (a table joinable to two populations) ────────────────────────────────
B3 = Benchmark(id="B3", kind="◆", title="universe assignment",
    schema={"tables": {
        "transactions": _t([("txn_id", "INTEGER"), ("store_id", "INTEGER")], [(1, 1)], pk=["txn_id"]),
        "stores": _t([("store_id", "INTEGER"), ("region", "VARCHAR")], [(1, "north")], pk=["store_id"]),
        "returns": _t([("return_id", "INTEGER"), ("txn_id", "INTEGER"), ("store_id", "INTEGER")],
                      [(1, 1, 1)], pk=["return_id"],
                      fk=[("txn_id", "transactions", "txn_id"), ("store_id", "stores", "store_id")])}},
    ground_truth={"closures": [["universe", "returns"]], "grades": {},
                  "oracle_calls": ["universe: returns joins both transactions and stores — which population does it describe?"],
                  "max_checklist": 2})

# ── B4 ◆ M-leak (a pre-aggregated column in a rollup table) ───────────────────────────────────────
B4 = Benchmark(id="B4", kind="◆", title="M-leak",
    schema={"tables": {"store_rollup": _t([("store_id", "INTEGER"), ("avg_basket", "DOUBLE")],
                                          [(1, 42.5)], pk=["store_id"])}},
    ground_truth={"closures": [["measure", "avg_basket"]], "grades": {},
                  "oracle_calls": ["M-leak: avg_basket is pre-aggregated in a rollup — declare its M_ANCHOR (the grain it leaks across)?"],
                  "max_checklist": 2})

# ── B5 ○ FK → functional edge (a DECLARED FK — the catalog-graded edge) ───────────────────────────
B5 = Benchmark(id="B5", kind="○", title="FK → functional edge",
    schema={"tables": {
        "regions": _t([("region_id", "INTEGER"), ("name", "VARCHAR")], [(10, "north"), (20, "south")], pk=["region_id"]),
        "stores": _t([("store_id", "INTEGER"), ("region_id", "INTEGER")], [(1, 10), (2, 20)],
                     pk=["store_id"], fk=[("region_id", "regions", "region_id")])}},
    ground_truth={"closures": [["edge", "store->region"]],
                  "grades": {"edge:store->region": "inferred_catalog"}, "oracle_calls": [], "max_checklist": 1})

# ── B6 ○ observed FD, no FK (a functional dependence in the data, not declared) ───────────────────
B6 = Benchmark(id="B6", kind="○", title="observed FD, no FK",
    schema={"tables": {"cal": _t([("day", "VARCHAR"), ("month", "VARCHAR")],
                                  [("2024-01-01", "2024-01"), ("2024-01-02", "2024-01")])}},
    ground_truth={"closures": [["edge", "day->month"]],
                  "grades": {"edge:day->month": "inferred_sample"}, "oracle_calls": [], "max_checklist": 1})

# ── B7 ○ calendar detection (a date column with daily cadence → a hierarchy) ──────────────────────
B7 = Benchmark(id="B7", kind="○", title="calendar detection",
    schema={"tables": {"events": _t([("event_id", "INTEGER"), ("d", "DATE")],
                                     [(1, "2024-01-01"), (2, "2024-01-02")], pk=["event_id"])}},
    ground_truth={"closures": [["hierarchy", "day->month"]],
                  "grades": {"hierarchy:day->month": "inferred_sample"}, "oracle_calls": [], "max_checklist": 1})

# ── B8 ◆ the polarity trap (a formable derived; init proposes the CLOSURE, fertility is the adjudicator's) ─
B8 = Benchmark(id="B8", kind="◆", title="the polarity trap",
    schema={"tables": {"tx": _t([("txn_id", "INTEGER"), ("order_id", "INTEGER"), ("amount", "DOUBLE")],
                                 [(1, 100, 10.0), (2, 100, 5.0), (3, 101, 8.0)], pk=["txn_id"])}},
    ground_truth={"closures": [["measure", "revenue"], ["measure", "orders"], ["derived", "aov"]],
                  "derived_needs": {"aov": ["revenue", "orders"]}, "grades": {},
                  "oracle_calls": ["fertility: 'aov' — an opening is the adjudicator's advice + your call, never my inference"],
                  "max_checklist": 2})

# ── B9 ○ numeric → measure, categorical → dimension ──────────────────────────────────────────────
B9 = Benchmark(id="B9", kind="○", title="numeric → measure, categorical → dimension",
    schema={"tables": {"tx": _t([("txn_id", "INTEGER"), ("amount", "DOUBLE"), ("channel", "VARCHAR")],
                                 [(1, 10.0, "web"), (2, 5.0, "store")], pk=["txn_id"])}},
    ground_truth={"closures": [["measure", "amount"], ["level", "channel"]],
                  "grades": {"measure:amount": "inferred_catalog", "level:channel": "inferred_catalog"},
                  "oracle_calls": [], "max_checklist": 2})

# ── B10 ◆ registry vs product basis ──────────────────────────────────────────────────────────────
B10 = Benchmark(id="B10", kind="◆", title="registry vs product basis",
    schema={"tables": {
        "product_catalog": _t([("product_id", "INTEGER"), ("name", "VARCHAR")], [(1, "a"), (2, "b")], pk=["product_id"]),
        "budget": _t([("store_id", "INTEGER"), ("day", "VARCHAR"), ("target", "DOUBLE")], [(1, "d1", 50.0)])}},
    ground_truth={"closures": [["universe", "catalog"], ["universe", "budget"]], "grades": {},
                  "oracle_calls": ["basis: product_catalog=registry, budget=product?"], "max_checklist": 2})

# ── B11 ◆ the refutation trap (catalog DECLARES a key the SAMPLE violates) ────────────────────────
B11 = Benchmark(id="B11", kind="◆", title="the refutation trap",
    schema={"tables": {
        "regions": _t([("region_id", "INTEGER"), ("name", "VARCHAR")], [(10, "north"), (20, "south")], pk=["region_id"]),
        # store_id is DECLARED unique by the catalog (below) but the DATA has store 1 in two regions:
        "stores": _t([("store_id", "INTEGER"), ("region_id", "INTEGER")], [(1, 10), (1, 20), (2, 10)])},
        "catalog_claims": {"stores": [{"type": "UNIQUE", "columns": ["store_id"]}]}},
    ground_truth={"closures": [["relate", "store<->region"]], "grades": {},
                  "oracle_calls": ["refutation: the catalog declares store_id unique but the sample has store 1 in two regions — RELATE, do not ride the FK"],
                  "max_checklist": 2})

BENCHMARKS = {b.id: b for b in (B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11)}

# GOLD — perfect-mind stand-ins for the hermetic plumbing test (B1 ◆, B5 ○, B8 ◆). Real baseline uses
# the AnthropicProvider. `review_call` surfaces the ◆ call; no spec ever opens a door.
GOLD = {
    "B5": [[{"kind": "edge", "target": "store->region", "grade": "inferred_catalog",
             "body": "EDGE store -> region ALONG geo VIA stores(store_id, region_id)"}]],
    "B1": [[{"kind": "universe", "target": "orders", "body": "UNIVERSE orders = order BASIS events",
             "review_call": "basis: orders=events, inventory=spine?"},
            {"kind": "universe", "target": "inventory",
             "body": "UNIVERSE inventory = store * day BASIS spine"}]],
    "B8": [[{"kind": "measure", "target": "revenue", "body": "MEASURE revenue ON tx FROM tx AS sum(amount)"},
            {"kind": "measure", "target": "orders", "body": "MEASURE orders ON tx FROM tx AS distinct(order_id)"},
            {"kind": "derived", "target": "aov", "body": "DERIVED aov = revenue / orders",
             "review_call": "fertility: 'aov' — an opening is the adjudicator's advice + your call, never my inference"}]],
}

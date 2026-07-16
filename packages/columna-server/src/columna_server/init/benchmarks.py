"""
columna_server.init.benchmarks — the ratified eval benchmarks (B1–B11), encoded as Benchmark objects.

Each is a messy schema + a small sample + the ADJUDICATED ground truth (closures, grades, the
oracle-asymmetric calls that MUST be surfaced, the checklist bound). `GOLD[id]` is a SCRIPTED stand-in
for a perfect mind — the generations a correct init would emit — used to prove the end-to-end plumbing
hermetically (no real model). Encoding v1 seeds three representative benchmarks (one ○ mechanical, two
◆ oracle-asymmetric incl. the polarity trap); the remaining B-rows follow the same shape.
"""
from .eval import Benchmark

# ── B5 ○ — FK → functional edge (mechanical, exactly gradeable) ───────────────────────────────────
B5 = Benchmark(
    id="B5", kind="○", title="FK → functional edge",
    schema={"stores": (["store_id", "region_id"], [(1, 10), (2, 20)]),
            "regions": (["region_id", "name"], [(10, "north"), (20, "south")])},
    ground_truth={
        "closures": [["edge", "store->region"]],
        "grades": {"edge:store->region": "inferred_catalog"},
        "oracle_calls": [],
        "max_checklist": 2,
    })

# ── B1 ◆ — events vs spine (the sharp call: a false events claim is unrefutable) ───────────────────
B1 = Benchmark(
    id="B1", kind="◆", title="events vs spine",
    schema={"orders": (["order_id", "amount"], [(1, 10.0), (2, 5.0)]),
            "daily_inventory": (["store_id", "day", "level"], [(1, "d1", 100.0)])},
    ground_truth={
        "closures": [["universe", "orders"], ["universe", "inventory"]],
        "grades": {},
        "oracle_calls": ["basis: orders=events, inventory=spine?"],
        "max_checklist": 2,
    })

# ── B8 ◆ — the polarity trap (a tempting opening; init must propose the CLOSURE, never a door) ─────
B8 = Benchmark(
    id="B8", kind="◆", title="the polarity trap",
    schema={"tx": (["store_id", "day", "amount"], [(1, "d1", 10.0)])},
    ground_truth={
        "closures": [["derived", "aov"]],          # a denotation-only derived; NOT a fertility opening
        "grades": {},
        "oracle_calls": ["fertility: 'aov' is provably fertile — declare if you mean it?"],
        "max_checklist": 2,
    })

BENCHMARKS = {b.id: b for b in (B1, B5, B8)}

# GOLD scripts — a perfect mind's generations per benchmark (proposal-spec dicts). A `review_call`
# surfaces an oracle-asymmetric call into the checklist; init never sets author_declared (no doors).
GOLD = {
    "B5": [[{"kind": "edge", "target": "store->region", "grade": "inferred_catalog",
             "body": "EDGE store -> region ALONG geo VIA stores(store_id, region_id)"}]],
    "B1": [[{"kind": "universe", "target": "orders", "body": "UNIVERSE orders = order BASIS events",
             "review_call": "basis: orders=events, inventory=spine?"},
            {"kind": "universe", "target": "inventory",
             "body": "UNIVERSE inventory = store * day BASIS spine"}]],
    "B8": [[{"kind": "derived", "target": "aov", "body": "DERIVED aov = revenue / orders",
             "review_call": "fertility: 'aov' is provably fertile — declare if you mean it?"}]],
}

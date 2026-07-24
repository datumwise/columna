"""
test_describe_insulation.py — CP-3 C-1/C-2: the D1 describe extension + the §2b insulation guarantee.

The STANDING no-physical-identifier test (C-2 owns the wall): describe (manifold + every measure) for the
demo carries no STRUCTURAL physical identifier — no `realized_by`, no table names, no qualified
`table.column`. If a physical thing ever appears in an Explorer, it is a describe bug caught HERE, never
an Explorer bug (Huayin, 2026-07-17). The test is STANDING and STRUCTURAL, not example-based: a test that
asserts current behaviour blesses current bugs (it is why the shipped `stores.opened_date` leak was
codified, not caught, by the old roundtrip test).

Precision (OF-9): drop-the-qualifier is the shipped guarantee — a bare predicate ATTRIBUTE name still
renders as the author wrote it (a residue, not a declared logical name). The full fix (declared logical
names for predicate terms) is a definition-language extension, its own WP (OF-9). Until it lands this
test asserts exactly what is guaranteed — no structural identifiers — and tightens to full verification
when OF-9 ships.
"""
import json
import re

from columna_server import tools as T
from columna_server.demo import demo_store, DEMO_MANIFOLD_ID as MID

# the demo's physical tables — none may appear as a `table.column` qualifier anywhere in describe.
# Cascadia's bound + reject-referenced tables, plus the legacy benchmark set (harmless supersets).
_PHYSICAL_TABLES = ("transactions", "eom_inventory", "calendar", "product_categories", "stores",
                    "customers", "products", "daily_revenue_summary", "monthly_avg_order_value",
                    "monthly_unique_visitors", "monthly_store_inventory",
                    "tx", "budget", "product_catalog", "inventory", "orders", "regions", "caltbl", "sales")


def _no_physical_identifier(blob: str):
    assert "realized_by" not in blob, "the closed leak `realized_by` is back in describe"
    for tbl in _PHYSICAL_TABLES:
        assert not re.search(rf'"[^"]*\b{tbl}\.[a-z_]+', blob), f"physical `{tbl}.column` leaked into describe"


def test_describe_manifold_carries_no_physical_identifier():
    store = demo_store()
    _no_physical_identifier(json.dumps(T.describe_manifold(store, MID)))


def test_describe_measure_carries_no_physical_identifier():
    store = demo_store()
    dm = T.describe_manifold(store, MID)
    for meas in dm["measures"]:
        _no_physical_identifier(json.dumps(T.describe_measure(store, MID, meas["name"])))


def test_the_opened_date_predicate_leak_is_closed_and_of9_renders_the_logical_name():
    # OF-9 (case-demo) tightens the old residue: Cascadia's `inventory` carve is authored with a LOGICAL
    # attribute, so the predicate renders `day >= store.opened` — the declared logical name WITH its
    # qualifier — and the physical binding `stores.opened_date` never crosses.
    store = demo_store()
    dm = T.describe_manifold(store, MID)
    inv = next(u for u in dm["universes"] if u["name"] == "inventory")
    assert inv["predicate"] == "day >= store.opened"                         # the declared logical name
    assert "stores.opened_date" not in inv["predicate"] and "opened_date" not in inv["predicate"]


def test_describe_manifold_carries_relates_declared_mn_on_the_wire():
    # RELATE on the wire (B, Huayin 2026-07-19): a declared M:N rides describe as data so an agent can
    # warn about a category rollup BEFORE spending the query. Additive field; logical names + NOTE
    # verbatim; nothing physical (the standing insulation test above already scans the whole blob).
    store = demo_store()
    dm = T.describe_manifold(store, MID)
    assert "relates" in dm, "the additive relates[] surface is missing from describe_manifold"
    rel = next(r for r in dm["relates"] if r["frm"] == "product" and r["to"] == "category")
    # faces[] is the additive crossing-disposition projection (Huayin 2026-07-19). Ship-dark was REVOKED
    # for Cascadia: the demo declares FACE touch so the crossing is VISIBLE on describe (the strategic
    # purpose — an agent sees the disposition from the source of truth before spending the query).
    assert set(rel) == {"frm", "to", "note", "faces"}                        # logical names + note + faces, only
    face = next(f for f in rel["faces"] if f["name"] == "touch")
    assert set(face) == {"name", "scheme", "description", "driver"}          # logical face fields only — NO license, NO VIA
    assert face["scheme"] == "touch"
    assert face["driver"] is None                                            # touch carries no driver (additive; null for touch)
    assert face["description"] == ("revenue reaches every category a product sits in — deliberately "
                                   "multi-counted; totals exceed the grand total")   # ratified text, verbatim
    assert rel["note"] == "a product belongs to up to 3 categories"          # the NOTE rides verbatim
    # VIA is MAP-LAYER (the ruling): the bridge table/columns NEVER cross the wire, even on a faced relate.
    blob = json.dumps(dm)
    assert "product_categories" not in blob, "the VIA bridge table leaked onto the wire (map-layer breach)"
    # contract_version rides additive (DESCRIPTION precedent) — the field's arrival does not bump it
    assert dm["contract_version"] == "1"


def test_describe_manifold_has_the_d1_extension_blocks():
    store = demo_store()
    dm = T.describe_manifold(store, MID)
    assert {"asserts", "hierarchies", "universes", "measures", "relates", "published_scope"} <= set(dm)
    u = dm["universes"][0]
    assert {"basis", "absence", "basis_license", "predicate"} <= set(u)     # C-1 universe extension
    assert "realized_by" not in dm["dimensions"][0]                         # C-2 insulation
    assert "universe" in dm["measures"][0]                                  # structured universe-qualified address
    ps = dm["published_scope"]
    assert {"cut", "blocked_edges"} <= set(ps)                              # scope/cut display (B1)
    dmeas = T.describe_measure(store, MID, dm["measures"][0]["name"])
    assert "signatures" in dmeas and "operator" in next(iter(dmeas["signatures"].values()))

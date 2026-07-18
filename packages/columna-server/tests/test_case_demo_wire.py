"""
test_case_demo_wire.py — Cascadia case-demo 1(b): DESCRIPTION strings reach the WIRE, rejects do NOT.

The wall-correction (Huayin's ruling): DESCRIPTIONs are folklore and DO flow model -> describe -> wire;
REJECT rows are map-artifact-only and NEVER cross describe or the wire. This pins both halves on the
server's describe tools.
"""
import json

import duckdb

from columna_core import ManifoldServer, DuckDBConnector
from columna_core.parser import parse_manifold
from columna_server.store import LoadedManifold
from columna_server import tools as T

_CML = """MANIFOLD w VERSION 1
LEVEL day = day BASE
UNIVERSE u = day BASIS events
MEASURE revenue ON u FROM sales AS sum(amount)   -- "sale amount, summed"
    REJECT summary.revenue "stale"
MEASURE stock ON u FROM snap VALUE level   -- "the stock level snapshot"
    FAMILY {
        sum
        last ORDER day   -- "position = the latest snapshot"
    }
    REJECT monthly_rollup.level "stale rollup"
"""


class _Store:
    def __init__(self, lm):
        self._lm = lm

    def get(self, mid):
        if mid != self._lm.manifold_id:
            raise KeyError(mid)
        return self._lm


def _store():
    con = duckdb.connect()
    con.execute("CREATE TABLE sales(day VARCHAR, amount DOUBLE)")
    con.execute("CREATE TABLE snap(day VARCHAR, level DOUBLE)")
    m = parse_manifold(_CML)
    server = ManifoldServer(m, DuckDBConnector(con))
    return _Store(LoadedManifold("w", "W", "", m, server))


def test_measure_description_flows_to_the_wire():
    dm = T.describe_measure(_store(), "w", "revenue")
    assert dm["description"] == "sale amount, summed"


def test_per_member_description_flows_to_the_wire():
    dstock = T.describe_measure(_store(), "w", "stock")
    assert dstock["member_anchors"]["last"]["description"] == "position = the latest snapshot"


def test_manifold_describe_carries_measure_descriptions():
    man = T.describe_manifold(_store(), "w")
    rev = next(x for x in man["measures"] if x["name"] == "revenue")
    assert rev["description"] == "sale amount, summed"


def test_no_reject_ever_crosses_the_wire():
    store = _store()
    blob = (json.dumps(T.describe_measure(store, "w", "revenue"))
            + json.dumps(T.describe_measure(store, "w", "stock"))
            + json.dumps(T.describe_manifold(store, "w")))
    for token in ("summary.revenue", "monthly_rollup", "stale", "reject"):
        assert token not in blob.lower(), f"map-only token {token!r} leaked onto the wire"

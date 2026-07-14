"""
test_connector_protocol.py — the connector Protocol + a parity-suite skeleton (audit v0.2 §B1 / §D
item 3; WP-C). Purely additive — no behavior change.

- Names the five-method connector surface as a `typing.Protocol` (in connector.py) and verifies the
  one shipped implementation, `DuckDBConnector`, conforms.
- Stands up the scaffolding for a cross-connector parity suite that ranges over ANY Protocol
  connector. Today there is exactly one, so this guards that connector; the day a second adapter
  lands, adding it to `CONNECTOR_FACTORIES` turns this into a real backend-parity check with no
  other edits (ties to B1: "operational ownership of the parity suite when the first external
  adapter lands").
"""
import glob
import os

import duckdb
import pytest

from columna_core import Connector, DuckDBConnector, ManifoldServer
from columna_core.disclosure_wire import wire_frame

_FIVE = ("deliver_measure", "deliver_base_values", "deliver_edge", "deliver_attribute", "deliver_base_rows")

# Every Protocol connector the parity suite knows about. TODAY: one. Add (name, factory) tuples here
# as adapters land — nothing else in this file needs to change to gain real cross-backend parity.
CONNECTOR_FACTORIES = [
    ("duckdb", lambda con: DuckDBConnector(con)),
]


def test_duckdb_connector_conforms_to_protocol(fixture_connector):
    assert isinstance(fixture_connector, Connector)          # runtime_checkable: all five methods present
    for name in _FIVE:
        assert callable(getattr(fixture_connector, name)), f"missing connector method {name!r}"


def _fresh_con(warehouse_dir):
    con = duckdb.connect()
    for f in sorted(glob.glob(os.path.join(warehouse_dir, "*.parquet"))):
        con.execute(f"CREATE TABLE {os.path.basename(f)[:-8]} AS SELECT * FROM read_parquet('{f}')")
    return con


# a small representative set spanning the delivery paths (additive rollup, cross-universe ratio)
_PARITY_CASES = [
    (("region",), "revenue", "serve"),
    (("store",), "revenue / level.last", "clarify"),
]


@pytest.mark.parametrize("cxn_name,factory", CONNECTOR_FACTORIES)
def test_parity_skeleton(cxn_name, factory, fixture_warehouse_dir, hand_manifold):
    """Build a server over each Protocol connector and assert the representative query set yields
    the expected wire outcomes. (Skeleton: with one connector this guards that connector; the
    parametrization is the seam a second backend plugs into.)"""
    srv = ManifoldServer(hand_manifold, factory(_fresh_con(fixture_warehouse_dir)))
    for anchor, expr, expected in _PARITY_CASES:
        w = wire_frame(srv.frame(*anchor).column("c", expr).run())
        assert w["outcome"] == expected, f"[{cxn_name}] {expr} @ {anchor} -> {w['outcome']} (expected {expected})"

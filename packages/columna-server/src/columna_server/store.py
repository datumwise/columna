"""
columna_server.store — the Manifold store (WP-2.1 stub: a directory of Manifolds).

Layout (per WP-2.2 spec):

    <manifolds_dir>/
      <manifold_id>/
        manifold.cml     # the Frame-QL Manifold definition (parsed by columna-core)
        data.toml        # connector type + data path

    data.toml:
        [manifold]                 # optional metadata
        name = "Benchmark"
        description = "..."
        [connector]
        type = "duckdb"            # only "duckdb" in Core
        warehouse = "warehouse"   # dir of parquet, relative to this manifold dir (or absolute)

Every Manifold is parsed and its backend loaded ONCE at startup. `list_manifolds` / `describe_*`
read from the parsed object and never touch data; `query` / `explain` go through the per-Manifold
`ManifoldServer`. `explain` uses `plan()` and must not increment the connector's fetch count.
"""
from __future__ import annotations

import glob
import os
from dataclasses import dataclass

try:                       # py3.11+
    import tomllib
except ModuleNotFoundError:  # py3.10
    import tomli as tomllib

from columna_core import DuckDBConnector, ManifoldServer
from columna_core.parser import parse_file


@dataclass
class LoadedManifold:
    manifold_id: str
    name: str
    description: str
    manifold: object          # columna_core.model.Manifold
    server: ManifoldServer


def _load_duckdb(warehouse_dir: str):
    import duckdb

    con = duckdb.connect()
    files = sorted(glob.glob(os.path.join(warehouse_dir, "*.parquet")))
    if not files:
        raise FileNotFoundError(f"no parquet files under connector warehouse {warehouse_dir!r}")
    for f in files:
        table = os.path.basename(f)[:-8]
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_parquet('{f}')")
    return con


def _load_one(manifold_id: str, mdir: str) -> LoadedManifold:
    cml = os.path.join(mdir, "manifold.cml")
    toml_path = os.path.join(mdir, "data.toml")
    if not os.path.isfile(cml):
        raise FileNotFoundError(f"manifold '{manifold_id}': missing manifold.cml")
    if not os.path.isfile(toml_path):
        raise FileNotFoundError(f"manifold '{manifold_id}': missing data.toml")

    with open(toml_path, "rb") as f:
        cfg = tomllib.load(f)
    meta = cfg.get("manifold", {})
    conn = cfg.get("connector", {})
    ctype = conn.get("type", "duckdb")
    if ctype != "duckdb":
        raise ValueError(f"manifold '{manifold_id}': connector type {ctype!r} is not supported "
                         f"(Core supports 'duckdb')")

    manifold = parse_file(cml)
    errs = manifold.check()
    if errs:
        raise ValueError(f"manifold '{manifold_id}' is not well-formed: {errs}")

    warehouse = conn.get("warehouse")
    if not warehouse:
        raise ValueError(f"manifold '{manifold_id}': [connector].warehouse is required")
    if not os.path.isabs(warehouse):
        warehouse = os.path.join(mdir, warehouse)
    con = _load_duckdb(os.path.abspath(warehouse))
    server = ManifoldServer(manifold, DuckDBConnector(con))

    return LoadedManifold(
        manifold_id=manifold_id,
        name=meta.get("name", manifold_id),
        description=meta.get("description", ""),
        manifold=manifold,
        server=server,
    )


class ManifoldStore:
    """All Manifolds under a directory, parsed and connected once at construction."""

    def __init__(self, manifolds_dir: str):
        self.dir = os.path.abspath(manifolds_dir)
        if not os.path.isdir(self.dir):
            raise FileNotFoundError(f"manifolds dir not found: {self.dir}")
        self._loaded: dict[str, LoadedManifold] = {}
        for entry in sorted(os.listdir(self.dir)):
            mdir = os.path.join(self.dir, entry)
            if os.path.isdir(mdir) and os.path.isfile(os.path.join(mdir, "manifold.cml")):
                self._loaded[entry] = _load_one(entry, mdir)
        if not self._loaded:
            raise FileNotFoundError(f"no manifolds (<id>/manifold.cml) found under {self.dir}")

    def ids(self) -> list[str]:
        return list(self._loaded)

    def get(self, manifold_id: str) -> LoadedManifold:
        lm = self._loaded.get(manifold_id)
        if lm is None:
            raise KeyError(manifold_id)
        return lm

    def all(self) -> list[LoadedManifold]:
        return list(self._loaded.values())

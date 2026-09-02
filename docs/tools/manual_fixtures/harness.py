"""The adjudicated fixtures the Manual's examples are planned and executed against.

ONE harness for the gate and the probe. They ask the same question of the same worlds; two copies of
this wiring would eventually answer it differently, and the answer is what the gate's authority
rests on.

WHY THE FIXTURES CARRY THE MANUAL'S OWN VOCABULARY. A refusal is only worth acting on if it can mean
exactly one thing. Planned against a fixture that merely RESEMBLES the Manual's schema, every
`unknown column` is ambiguous between "the Manual documents a form the planner refuses" and "my
fixture is thin" — and the second reading is always available, so no finding is ever safe to act on.
Six results moved from "contradiction" to "fixture gap" during Mission B once the vocabulary was
completed; reporting them as Manual defects would have been wrong six times.

WHY THE FIXTURES CARRY DATA. Transport is CLOSED BY DEFAULT (P0.5a): until a manifold is published,
any ask that climbs a declared edge plans `refuse / uncertified_edge`, which would mask nearly every
verdict the gate is for. Certification comes only from `publish()` -> `adjudicate()`, and
adjudication proves its functional-dependency claims BY QUERYING THE DATA. The rows are evidence,
not decoration — adjudication rejected three drafts of them (an events-universe face driver, tied
ASSIGN ranks, and a `product -> category` rollup the many-to-many rows disprove).

NOTHING ASSERTS ON A VALUE. The gate is about DISPOSITION — which mood an example earns, and for
which reason. The data exists to unlock transport and to let a serve be observed as a serve.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

#: Manual manifold name -> fixture module. `retail` and `retail_manifold` are the Manual's own two
#: spellings of one worked schema. `None` is the no-`FROM` case: those examples use the finance
#: vocabulary, which is also the manifold most of the Manual's prose is written against.
BINDING = {
    None: "finance_manifold",
    "finance_manifold": "finance_manifold",
    "product_manifold": "product_manifold",
    "retail": "retail_manifold",
    "retail_manifold": "retail_manifold",
}

FIXTURES = ("finance_manifold", "product_manifold", "retail_manifold")


def servers():
    """Publish every fixture once and return {name: ManifoldServer}. Publishing is what certifies
    the edges; an unpublished fixture answers `uncertified_edge` to most of the Manual."""
    import duckdb
    from columna_core import ManifoldServer
    from columna_core.connector import DuckDBConnector
    from columna_core.parser import parse_manifold
    from manual_world import build

    con = build(duckdb.connect())
    out = {}
    for name in FIXTURES:
        m = parse_manifold((HERE / f"{name}.cml").read_text())
        srv = ManifoldServer(m, connector=DuckDBConnector(con))
        srv.publish()
        out[name] = srv
    return out


def server_for(srvs, stmt):
    return srvs[BINDING.get(stmt.from_manifold, "finance_manifold")]

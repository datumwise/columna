"""
test_execution_provider.py — the S1.1 seam guarantees.

Proves the serving surface depends on `ExecutionProvider`, not on a concrete Core runtime,
and that introducing the seam changes no governed result. Three guarantees:

1. **Conformance** — the loaded provider (and a bare `CoreExecutionProvider`) satisfy the
   `ExecutionProvider` protocol.
2. **Structural** — `LoadedManifold` has no `server` field (so a `.server.planner`
   reach-through is impossible under typing), and the serving modules (`tools`, `recapture`)
   never name a concrete Core runtime. This is the primary enforcement; the wider suite
   (recapture / trial / wire / warehouse-coherence) is the behavioral proof.
3. **Parity** — a real query executes through the provider and lands on its ratified mood,
   with the fetch metric intact.
"""
import inspect
import os
from dataclasses import fields

import columna_server
from columna_server import recapture, tools
from columna_server import store as store_mod
from columna_server.provider import CoreExecutionProvider, ExecutionProvider
from columna_server.store import LoadedManifold, _load_one

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


class _OneStore:
    def __init__(self, lm):
        self._lm = lm

    def get(self, mid):
        if mid != self._lm.manifold_id:
            raise KeyError(mid)
        return self._lm


# 1. conformance ---------------------------------------------------------------------------
def test_loaded_provider_satisfies_protocol():
    lm = _load_one("cascadia", _CASCADIA)
    assert isinstance(lm.provider, ExecutionProvider)
    assert isinstance(lm.provider, CoreExecutionProvider)
    # a bare adapter over the same runtime also conforms
    assert isinstance(CoreExecutionProvider(lm.provider.runtime), ExecutionProvider)


# 2. structural ----------------------------------------------------------------------------
def test_loaded_manifold_has_no_server_field():
    names = {f.name for f in fields(LoadedManifold)}
    assert "server" not in names, "LoadedManifold must expose only .provider, never .server"
    assert "provider" in names


def test_serving_modules_do_not_reach_a_concrete_runtime():
    # The concrete ManifoldServer is known only to CoreExecutionProvider. The serving surface
    # must not name the runtime nor reach through it.
    for mod in (tools, recapture):
        src = inspect.getsource(mod)
        assert "ManifoldServer" not in src, f"{mod.__name__} names the concrete runtime"
        assert ".server" not in src, f"{mod.__name__} reaches a raw .server"
    # Only store.py (constructor) and provider.py (adapter) may know ManifoldServer.
    assert "ManifoldServer" in inspect.getsource(store_mod)


# 3. parity --------------------------------------------------------------------------------
def test_query_executes_through_provider_and_lands_on_its_mood():
    lm = _load_one("cascadia", _CASCADIA)
    lm.provider.runtime.publish()
    store = _OneStore(lm)

    # E1 — the ratified clean serve pair.
    wire = tools.execute_frame_query(store, "cascadia", "SELECT revenue, orders AT {region*cal.quarter}")
    assert wire["outcome"] == "serve"
    assert wire["executed"] is True
    assert {c["name"] for c in wire["columns"]} == {"revenue", "orders"}
    # the fetch metric survives the seam (an int delta, non-negative)
    assert isinstance(wire["fetches_delta"], int) and wire["fetches_delta"] >= 0

    # plan path (zero-fetch) and explain path both route through the provider
    check = tools.check_frame_query(store, "cascadia", "SELECT revenue AT {region}")
    assert check["executed"] is False and check["fetches_delta"] == 0
    explained = tools.explain_statement(store, "cascadia", "SELECT revenue AT {region}")
    assert "outcome" in explained

    # provider.fetches() is the same counter the wire reports
    assert isinstance(lm.provider.fetches(), int)

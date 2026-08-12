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
from columna_server.provider import (
    CoreExecutionProvider,
    ExecutionProvider,
    SupportsExecutionDiagnostics,
)
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

    # Core exposes the OPTIONAL fetches diagnostic (see S1.2 tests below)
    assert isinstance(lm.provider, SupportsExecutionDiagnostics)
    assert isinstance(lm.provider.execution_diagnostics()["fetches"], int)


# 4. S1.2 — execution diagnostics are an OPTIONAL, SEPARATE capability -----------------------
class _NoDiagProvider:
    """A valid ExecutionProvider that exposes NO execution diagnostics (a stand-in for a future
    provider without a fetch counter). Delegates execution to a Core runtime for a real result."""

    def __init__(self, runtime):
        self._r = runtime

    def run(self, statement):
        return self._r.planner.run_statement(statement)

    def plan(self, statement):
        return self._r.planner.plan_statement(statement)

    def explain(self, statement):
        return self._r.explain_statement(statement)

    def operators(self):
        return self._r.planner.m.operators

    def published_scope(self):
        return getattr(self._r, "published_scope", None)
    # deliberately NO execution_diagnostics()


def test_diagnostics_capability_is_separate_and_optional():
    lm = _load_one("cascadia", _CASCADIA)
    # Core provider is both an ExecutionProvider AND supports diagnostics
    assert isinstance(lm.provider, ExecutionProvider)
    assert isinstance(lm.provider, SupportsExecutionDiagnostics)
    # a diagnostics-less provider is STILL a valid ExecutionProvider, but not a diagnostics one
    nodiag = _NoDiagProvider(lm.provider.runtime)
    assert isinstance(nodiag, ExecutionProvider)
    assert not isinstance(nodiag, SupportsExecutionDiagnostics)


def test_provider_without_diagnostics_serves_and_omits_fetches_delta():
    lm = _load_one("cascadia", _CASCADIA)
    lm.provider.runtime.publish()
    nodiag_lm = LoadedManifold("cascadia", lm.name, lm.description, lm.manifold,
                               _NoDiagProvider(lm.provider.runtime))
    wire = tools.execute_frame_query(_OneStore(nodiag_lm), "cascadia",
                                     "SELECT revenue, orders AT {region*cal.quarter}")
    # a valid governed result …
    assert wire["outcome"] == "serve"
    assert {c["name"] for c in wire["columns"]} == {"revenue", "orders"}
    # … with NO fetches_delta (absent ≠ zero: the provider simply exposes no such diagnostic)
    assert "fetches_delta" not in wire


def test_diagnostics_observe_execution_but_do_not_participate_in_adjudication():
    """The structural guarantee: the diagnostics capability changes ONLY the diagnostic field —
    the analytical frame, mood, columns, and disclosures are identical.

    Two INDEPENDENT cold loads (equal cache state) isolate the capability as the only variable —
    running twice on one runtime would differ by a legitimate served-from-cache disclosure, which
    is a cache fact, not a diagnostics one.
    """
    q = "SELECT revenue, orders AT {region*cal.quarter}"
    lm = _load_one("cascadia", _CASCADIA)
    lm.provider.runtime.publish()

    # Warm the cache once, then compare two CACHE-HIT runs over the SAME runtime. Both read the
    # identical cached column (no re-summation → no float-order residue) with the same served-from-
    # cache disclosure, so the diagnostics capability is the ONLY variable. (Comparing a cold run to
    # a warm one, or two independent cold loads, would confound this with a cache disclosure and with
    # nondeterministic float summation order — neither of which is governed meaning.)
    tools.execute_frame_query(_OneStore(lm), "cascadia", q)
    with_diag = tools.execute_frame_query(_OneStore(lm), "cascadia", q)

    nodiag_lm = LoadedManifold("cascadia", lm.name, lm.description, lm.manifold,
                               _NoDiagProvider(lm.provider.runtime))
    without_diag = tools.execute_frame_query(_OneStore(nodiag_lm), "cascadia", q)

    # only the diagnostic field differs …
    assert "fetches_delta" in with_diag and isinstance(with_diag["fetches_delta"], int)
    assert "fetches_delta" not in without_diag
    # … everything analytical (frame, mood, columns, disclosures) is byte-identical
    strip = lambda w: {k: v for k, v in w.items() if k != "fetches_delta"}
    assert strip(with_diag) == strip(without_diag)

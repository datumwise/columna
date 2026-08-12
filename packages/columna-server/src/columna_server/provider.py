"""
columna_server.provider — the execution-provider seam (S1.1).

The serving surface (the MCP tools in `columna_server.tools`, and `recapture`) depends on
`ExecutionProvider`, an interface, rather than on a concrete Core runtime. Today the only
implementation is `CoreExecutionProvider`, a 1:1 adapter over `ManifoldServer` +
`ColumnEngine`; a future Platform provider implements the SAME protocol without importing
any Core class.

Design constraints (F0 / S1.1 rulings):

* **Return shapes are opaque here** (typed `Any`). What the serving surface does with a
  result is hand it to `disclosure_wire`, which duck-types it — so a non-Core provider need
  not instantiate any `columna-core` dataclass merely to satisfy this seam. We deliberately
  do NOT define a shared result model in S1.1; that would be premature.
* **Logical description stays OFF the provider.** A Manifold's logical/read model lives on
  `LoadedManifold.manifold` and is untouched by this seam — governed publication vs. execution
  of a governed request are kept separate (S2 owns the shared publication/registry surface).
* **`operators` / `published_scope` / `fetches` are PROVISIONAL.** They are current
  serving-runtime reaches kept on the provider only so `tools.py` stops touching
  `ManifoldServer`. F0 showed the semantic spine currently spans packages; S2+/shared-spine
  work may relocate these. `fetches` is byte-identical here — S1.2 removes the assumption that
  every provider exposes a connector fetch counter.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from columna_core import ManifoldServer


@runtime_checkable
class ExecutionProvider(Protocol):
    """Execution capability for one already-resolved Manifold.

    NOT the Manifold's logical description (that stays on `LoadedManifold.manifold`,
    deliberately outside this seam). A future Platform provider implements this without
    importing a Core runtime class.
    """

    def run(self, statement: Any) -> Any:
        """Execute a parsed Frame-QL statement; return the governed frame result."""
        ...

    def plan(self, statement: Any) -> Any:
        """Plan a parsed statement WITHOUT executing (the would-be result)."""
        ...

    def explain(self, statement: Any) -> Any:
        """The rich EXPLAIN representation of a parsed statement (canonical form, cone…)."""
        ...

    def operators(self) -> Any:
        """Operator registry for grammar/typecheck surfacing. Provisional (semantic)."""
        ...

    def published_scope(self) -> Any:
        """The current published serving scope, or None. Provisional (governance)."""
        ...

    def fetches(self) -> int:
        """The provider's cumulative source-fetch count. Provisional; S1.2 revisits this."""
        ...


class CoreExecutionProvider:
    """Adapter over today's Core runtime (`ManifoldServer` + `ColumnEngine`).

    The ONLY server-side object that knows `ManifoldServer` exists. Pure delegation — it
    moves no semantic law and changes no governed result.
    """

    def __init__(self, server: ManifoldServer) -> None:
        # The concrete Core runtime. Exposed for below-the-seam lifecycle/bootstrap and tests
        # (e.g. `publish()`, `frame()`); the serving surface never reaches it, because it is
        # typed against `ExecutionProvider`, which has none of these members.
        self.runtime: ManifoldServer = server

    def run(self, statement: Any) -> Any:
        return self.runtime.planner.run_statement(statement)

    def plan(self, statement: Any) -> Any:
        return self.runtime.planner.plan_statement(statement)

    def explain(self, statement: Any) -> Any:
        return self.runtime.explain_statement(statement)

    def operators(self) -> Any:
        return self.runtime.planner.m.operators

    def published_scope(self) -> Any:
        return getattr(self.runtime, "published_scope", None)

    def fetches(self) -> int:
        return self.runtime.fetches

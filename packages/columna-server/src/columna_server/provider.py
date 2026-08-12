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
* **`operators` / `published_scope` are PROVISIONAL.** They are current serving-runtime
  reaches kept on the provider only so `tools.py` stops touching `ManifoldServer`. F0 showed
  the semantic spine currently spans packages; S2+/shared-spine work may relocate these.
* **Execution diagnostics are an OPTIONAL, SEPARATE capability** (`SupportsExecutionDiagnostics`),
  not part of `ExecutionProvider` (S1.2). A valid provider need not report any diagnostics; the
  Core provider reports a `fetches` counter, from which the server derives the existing optional
  `fetches_delta` wire field. Diagnostics OBSERVE execution; they never participate in analytical
  adjudication.
"""
from __future__ import annotations

from collections.abc import Mapping
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


@runtime_checkable
class SupportsExecutionDiagnostics(Protocol):
    """OPTIONAL observational capability, separate from `ExecutionProvider` (S1.2).

    A provider that implements it reports **cumulative, monotonic, provider-defined** counters
    describing execution cost; the server may diff them across a call to annotate the wire. A
    provider MAY implement none of this and still be a fully valid `ExecutionProvider` — absence
    is not zero: it means "this provider does not expose that diagnostic", never "zero", "unknown",
    or "failure". The counter *keys* are the provider's own (Core exposes `fetches`); the server
    surfaces only the keys it already has a wire field for.

    Known limitation (S1.2, intentionally unsolved): cumulative before/after counters are not
    request-isolated under concurrent execution. That is existing instrumentation behavior, not
    governed semantics; request-scoped diagnostics can be designed if a provider ever needs them.
    """

    def execution_diagnostics(self) -> Mapping[str, int]:
        """Cumulative, provider-defined execution counters (e.g. Core: ``{"fetches": N}``)."""
        ...


class CoreExecutionProvider:
    """Adapter over today's Core runtime (`ManifoldServer` + `ColumnEngine`).

    The ONLY server-side object that knows `ManifoldServer` exists. Pure delegation — it
    moves no semantic law and changes no governed result. Implements both `ExecutionProvider`
    and the optional `SupportsExecutionDiagnostics` (it exposes a `fetches` counter).
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

    def execution_diagnostics(self) -> Mapping[str, int]:
        # Core's one counter: cumulative backend column-fetches. `fetches_delta == 0` across a
        # call therefore proves *this Core operation performed no backend fetches* — a Core fact,
        # not a universal provider invariant.
        return {"fetches": self.runtime.fetches}

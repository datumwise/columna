"""columna_platform.provider — the successor path as an EXECUTION PROVIDER.

WHAT THIS IS FOR. `columna_server.provider.ExecutionProvider` is the serving surface's seam: the MCP
tools depend on that interface, not on a Core runtime, and its own docstring anticipates this class —
*"a future Platform provider implements the SAME protocol without importing any Core class."* This is
that provider, for exactly one capability.

IT IMPLEMENTS THE PROTOCOL STRUCTURALLY, AND IMPORTS NOTHING FROM THE SERVER. `ExecutionProvider` is
a `@runtime_checkable` Protocol, so conformance is a matter of having the methods, not of inheriting
from anything. That matters here for a hard reason and not a stylistic one: `columna_server.store`
imports `columna_core.parser` at module scope, so importing the server from this package would drag
the legacy execution stack into the successor path and break the isolation this whole package exists
to demonstrate. The dependency runs SERVER → PLATFORM, one way, and this file is the reason it can.

HONEST ABOUT WHAT IT CANNOT DO (ruled 2026-09-12 §7). Four of the five protocol methods are not
implemented by this slice, and none of them falls back to Core. `run` would be material execution;
`explain` would be a second, richer answer shape this proof has not earned; `operators` would be a
claim about an operator registry this path does not have. Each raises `UnsupportedByThisProfile`,
which is not a governed refusal and must not be reported as one.

`published_scope` IS THE EXCEPTION, AND RETURNS `None`. Not because None is convenient, but because
the existing contract already defines it: the protocol says *"the current published serving scope, or
None"*, and every server consumer already handles None (`tools.py:231`, `tools.py:467`, both
`if ps else`). A successor path has no legacy `PublishedScope` and inventing one would mean importing
the adjudication ontology. None is the truthful answer — there is no published scope here — and it is
the smallest behaviour consistent with the contract as written. Reported rather than assumed.
"""
from __future__ import annotations

from columna_core.serving_contract import FrameResult

from . import serving
from .refusals import UnsupportedByThisProfile


class PlatformExecutionProvider:
    """One governed publication's PRE-FLIGHT capability, and nothing else.

    Construction takes governed inputs only: the parsed v2 publication and the resolved law views.
    No `.cml`, no Core model, no connector, no store."""

    def __init__(self, publication, views: dict, *, manifold_id: str = ""):
        self.publication = publication
        self.views = views
        self.manifold_id = manifold_id

    @classmethod
    def from_artifact(cls, artifact_path: str, *, manifold_id: str = "") -> "PlatformExecutionProvider":
        """Build from a `governed-publication.json` on disk — THE SERVER'S ONLY ENTRY POINT.

        The v2 artifact is parsed and its law resolved HERE, by v2's own reader, so the server hands
        over a path and never a governed object it would have to know the shape of. That keeps the
        dependency one-way and shallow: the server knows this constructor and nothing else about the
        successor path's vocabulary.

        It re-reads a file the server has already read. That is deliberate and cheap — the server's
        read answers "is this a well-formed artifact this installation accepts", which is an ingest
        question, and this one answers "what law does it establish", which is an execution question.
        Passing the server's plain-data reading over instead would make the server the keeper of a
        governed object, which is exactly the coupling this seam exists to avoid."""
        pub, views = serving.open_publication(artifact_path)
        return cls(pub, views, manifold_id=manifold_id)

    # ── the one supported capability ────────────────────────────────────────────────────────────
    def plan(self, statement) -> FrameResult:
        """Plan WITHOUT executing — the `check_frame_query` capability, and the whole slice.

        Returns the architecture-neutral `FrameResult`. It does not wire it: the server applies
        `wire_frame`, `_disclose` and the `manifold_id` stamp exactly once, as it already does for
        the Core provider, and a second serializer here would be a second contract."""
        return serving.plan_result(self.publication, self.views, statement)

    # ── the four that are not ───────────────────────────────────────────────────────────────────
    def run(self, statement):
        raise UnsupportedByThisProfile(
            "this profile plans; it does not execute. Material execution over a governed publication "
            "is a later slice, and answering `run` by handing the statement to Core would make the "
            "provider a passthrough that misreports whose semantics served the number")

    def explain(self, statement):
        raise UnsupportedByThisProfile(
            "EXPLAIN's payload is the canonical form plus the atom/cone decomposition, which this "
            "path has no representation for; a partial EXPLAIN would understate what it omits")

    def operators(self):
        raise UnsupportedByThisProfile(
            "this path holds no operator registry — the governed continuation law names the operator "
            "for a family, which is not the same fact as a registry of callable signatures")

    def published_scope(self):
        """`None` — there is no published scope here, and that is a contract-valid answer."""
        return None

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

HONEST ABOUT WHAT IT CANNOT DO (ruled 2026-09-12 §7; amended 2026-09-14). `run` is now implemented
for ONE shape of ask — an exact primitive family at its constitutive anchor, over material reached
through a deployment-local source binding — and answers every other ask with the registered wire
reason `unsupported`, never with a governed refusal and never by delegating to Core. `explain` would
be a second, richer answer shape this proof has not earned; `operators` would be a claim about an
operator registry this path does not have. Both still raise `UnsupportedByThisProfile`, which is not
a governed refusal and must not be reported as one.

WHY `run` TRANSLATES AND `explain` STILL RAISES. `run`'s answer goes out through `wire_frame`, which
has a shape for a no-result and a registered reason that means exactly "this build does not implement
it". `explain`'s payload is passed through by the server unwired and unvalidated, so there is no
answer shape to translate INTO — inventing one would be this slice freezing a serialization it was
not asked to. The asymmetry is the wire's, not a preference.

`published_scope` IS THE EXCEPTION, AND RETURNS `None`. Not because None is convenient, but because
the existing contract already defines it: the protocol says *"the current published serving scope, or
None"*, and every server consumer already handles None (`tools.py:231`, `tools.py:467`, both
`if ps else`). A successor path has no legacy `PublishedScope` and inventing one would mean importing
the adjudication ontology. None is the truthful answer — there is no published scope here — and it is
the smallest behaviour consistent with the contract as written. Reported rather than assumed.
"""
from __future__ import annotations

from typing import Optional

from columna_core.serving_contract import FrameResult

from . import serving
from .refusals import UnsupportedByThisProfile
from .source import MaterialBinding


class PlatformExecutionProvider:
    """One governed publication's PRE-FLIGHT capability, and nothing else.

    Construction takes governed inputs only: the parsed v2 publication and the resolved law views.
    No `.cml`, no Core model, no connector, no store."""

    def __init__(self, publication, views: dict, *, manifold_id: str = "",
                 material: Optional[MaterialBinding] = None, movement: tuple = ()):
        self.publication = publication
        self.views = views
        self.manifold_id = manifold_id
        #: The deployment's material binding, or None. None PLANS; it does not execute.
        self.material = material
        #: MOVEMENT LICENCES AS EXECUTION INPUT, on the same footing as the C7 sufficient-state
        #: basis and the material binding: derived by the layer that owns the law and handed to
        #: this path, never constituted here. An empty tuple is the default and means this
        #: deployment licenses no movement — which is a deployment fact, not a governed verdict
        #: about any family, and is why the absence produces `want_of_law` at adjudication rather
        #: than a capability limit here.
        self.movement = tuple(movement)
        self._mapping = serving.bind(publication, material.mapping_path) if material else None

    @classmethod
    def from_artifact(cls, artifact_path: str, *, manifold_id: str = "",
                      material: Optional[MaterialBinding] = None,
                      movement: tuple = ()) -> "PlatformExecutionProvider":
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
        return cls(pub, views, manifold_id=manifold_id, material=material, movement=movement)

    # ── the one supported capability ────────────────────────────────────────────────────────────
    def plan(self, statement) -> FrameResult:
        """Plan WITHOUT executing — the `check_frame_query` capability, and the whole slice.

        Returns the architecture-neutral `FrameResult`. It does not wire it: the server applies
        `wire_frame`, `_disclose` and the `manifold_id` stamp exactly once, as it already does for
        the Core provider, and a second serializer here would be a second contract."""
        return serving.plan_result(self.publication, self.views, statement,
                                   licences=self.movement)

    # ── the four that are not ───────────────────────────────────────────────────────────────────
    def run(self, statement) -> FrameResult:
        """MATERIAL EXECUTION — the `execute_frame_query` capability, for one shape of ask.

        Returns the architecture-neutral `FrameResult`, wired exactly once by the server, exactly as
        `plan` does. A profile that cannot answer this particular ask says so IN the result, as the
        registered `unsupported` reason, rather than by raising past the server — because a caller
        who asked a meaningful question deserves an answer that says which kind of no it is, and an
        exception escaping the tool is not an answer at all.

        A DEPLOYMENT WITH NO MATERIAL BINDING DOES NOT EXECUTE, and that is the default. It is a
        capability limit of this deployment, not a governed verdict about the ask, and it is
        certainly not grounds to hand the statement to Core — which would make the provider a
        passthrough that misreports whose semantics served the number."""
        if self.material is None:
            return serving.unsupported_result(
                statement,
                "this deployment binds no material for the successor runtime, so this profile plans "
                "and does not execute; binding a material source for the realization's connection "
                "is a deployment act, not a governed one")
        return serving.run_result(self.publication, self.views, self._mapping,
                                  self.material.sources, statement, licences=self.movement)

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

"""
columna_platform.kernel.expression — **the expression evaluator, ABOVE the MME.**

Ruled (Huayin, 2026-09-29, M-2 §1):

    **MME manages only family materializations `F@A`.**

    *"Expression outputs `E@A` must no longer share the MME store, retention key, cache lifecycle, or
    dependency machinery. Expressions remain fully supported by Platform serving, but they consume family
    state supplied by MME and are evaluated above it."*

So this module is the *above*. It is a consumer of the MME, not a part of it, and the direction of that
arrow is the unit's whole result:

    AOV@Month
      ↓
    MME supplies Revenue@Month + OrderCount@Month     ← `family.measure(...)`, the seam
      ↓
    basis compatibility                               ← here
      ↓
    expression evaluator                              ← here
      ↓
    AOV result                                        ← returned, and NOT retained anywhere

WHAT MOVED, AND WHAT DID NOT
----------------------------
**Moved:** `MME.evaluate` and `MME._establish`, verbatim in their semantics, into this class. The MME no
longer has a method that returns an `ExpressionOutput`, and `columna_platform.kernel.MME` no longer
imports `ExpressionOutput` at all.

**Did not move:** expression *semantics*. Ruled §2: *"Do not remove expression semantics from the kernel;
only move expression execution above the MME boundary."* `GovernedExpression`, `SufficientBasis`,
`ExpressionPoint` and `ExpressionOutput` stay exactly where they were, in `sorts.py` and `value.py`, and
the MME remains the Manifold's **constitution authority** for them — it registers them, binds their laws,
computes their `ConstitutionWitness` and answers `sort_of`. That is not cache machinery and M-2 does not
touch it. What M-2 removes is the MME's role as their *store*.

THE LINE, SAID PRECISELY
------------------------
    the MME **constitutes** an expression        → `register_expression`, `witness_of`, `law_of`
    the MME **materializes** a family            → `admit`, `candidates`, `adjudicate`, `measure`
    this evaluator **evaluates** an expression   → `evaluate`

An expression has no materialization, so the middle row has no expression column. That absence is the unit.

NO EXPRESSION CACHE IN v1
-------------------------
Ruled §1: *"Do not cache the resulting expression output in MME v1."* This class holds no store, and it is
not that it holds an empty one — there is no field. `evaluate` therefore has **no `retain` parameter**,
because a parameter that could only ever be ignored is a promise the object cannot keep. Every call
re-evaluates from a sufficient basis, which is what §3.7 says an expression IS: *"an expression's value is
re-evaluated from a sufficient basis at each location; it does not compose."* The v1 behaviour and the
doctrine happen to agree here, and when a later unit adds an expression cache it will be a cache of a
**finalized result**, with its own lifecycle, above this line and not inside the MME.

**THE CACHE THAT REMAINS IS THE FAMILY ONE, AND IT STILL WORKS.** Evaluating `AOV@Month` twice does not
recompute `Revenue@Month` twice: the second `measure` hits the family materialization the first one
admitted. The expression is re-derived; its operands are not re-established. That is the correct division,
and it is why removing the expression cache costs so much less than it looks like it should.

WHAT THE EVALUATOR OBSERVES
---------------------------
Nothing directly. Ruled §7: observation happens *"at the request boundary"*, and the request boundary for
family state is `MME.measure` — which this class calls, and which observes. What the evaluator contributes
is `on_behalf_of`: the reason the family was asked for, threaded down so that a later optimizer can tell
`Revenue@Month` requested by a user apart from `Revenue@Month` requested by `AOV@Month`.
"""
from __future__ import annotations

from typing import Any, Optional

from .geometry import Anchor
from .law import AnalyticalLaw
from .sorts import GovernedExpression, SufficientBasis
from .standing import (
    Disclosure,
    EVALUATED,
    REFUSED,
    Refusal,
    UNSTATED_DATA_STATE,
)
from .value import Answer, ExpressionOutput, FamilyState


class ExpressionEvaluator:
    """**Evaluate `E@A` from family state supplied by an MME.**

    Constructed over the engine it consumes. The engine does not know it exists — there is no back
    reference, no registration and no hook — which is the mechanical form of "expressions are above the
    MME": you can delete this class and the MME still compiles, serves and passes its own suite."""

    def __init__(self, family_supplier: Any) -> None:
        #: The MME, held as a **family supplier** and used through exactly four members: `measure`,
        #: `family`, `expression` and `law_of`. Named for the role rather than the type because the
        #: columnar engine fills the same role with a different signature, and because the day a
        #: Fulfillment Coordinator sits between the two (ruled §6) it will fill this slot unchanged.
        self.families = family_supplier

    @property
    def mme(self) -> Any:
        """Legibility at call sites that want to say what it is as well as what it does."""
        return self.families

    # ── serving an expression ────────────────────────────────────────────────────────────────
    def evaluate(self, expression: GovernedExpression, anchor: Anchor, *,
                 basis_id: Optional[str] = None, data_state: Optional[str] = None) -> Answer:
        """**Evaluate `E@A` from a sufficient basis.** Never from a continuation, because there is none.

        Where more than one basis is admitted they are tried in declaration order and the FIRST that
        establishes wins; the refusal, if none does, reports every route it tried and why each failed.
        That is what makes "refuse an incompatible basis even when both operands individually exist" a
        legible answer rather than a bare `no`.

        **There is no cache lookup at the top of this method**, and its absence is M-2. In M-1 this began
        by resolving a pool of retained `E@A` objects out of the MME store; that store is gone and the
        expression is established from its basis every time."""
        # **THE EXPRESSION MUST BE THIS BUILD'S** (J-0). The law is taken from this engine's registry
        # by name, but `admitted_bases`, `parameters` and `instance()` are read off the object handed in —
        # so an unconstituted declaration got a local law and stamped its own jurisdiction on the output.
        expression = self.mme.subject_expression(expression)
        law = self.families.law_of(expression.expression_id)
        considered: list[str] = []

        routes = ([b for b in expression.admitted_bases if b.basis_id == basis_id]
                  if basis_id else list(expression.admitted_bases))
        if not routes:
            missing = (f"basis {basis_id!r} is not admitted by this expression"
                       if basis_id else
                       "this expression admits NO sufficient basis. It is well-formed and not "
                       "evaluable — a constituted expression may exist before any establishment route "
                       "is admitted, and that is a capability limit rather than a defect")
            return Answer(route=REFUSED,
                          refusal=Refusal("no-admitted-basis", str(expression.at(anchor)), missing))

        failures: list[str] = []
        for basis in routes:
            considered.append(basis.basis_id)
            attempt = self._establish(expression, law, basis, anchor, data_state)
            if attempt.served:
                output = attempt.value
                return Answer(route=EVALUATED, value=output, disclosures=output.disclosures,
                              seeded_from=basis.basis_id, considered=tuple(considered))
            failures.append(f"basis {basis.basis_id!r}: {attempt.refusal.detail}")

        return Answer(route=REFUSED, considered=tuple(considered),
                      refusal=Refusal(
                          "no-sufficient-basis-establishes", str(expression.at(anchor)),
                          " | ".join(failures) + ". Every admitted route was tried. NOTE WHAT THIS IS "
                          "NOT: it is not a claim that the operands are absent — where they are present "
                          "and incompatible, the refusal above says so, because physical availability "
                          "is not analytical authority"))

    def _establish(self, expression: GovernedExpression, law: AnalyticalLaw,
                   basis: SufficientBasis, anchor: Anchor,
                   data_state: Optional[str] = None) -> Answer:
        """One route, tried. Returns the `ExpressionOutput` or the refusal that stopped it."""
        subject = f"{expression.expression_id}@{anchor} via {basis.basis_id}"
        states: dict[str, FamilyState] = {}
        for role in basis.component_laws:
            component = self.families.family(basis.components[role])
            # ── THE SEAM ─────────────────────────────────────────────────────────────────────
            # The only way this evaluator obtains family state. It asks the MME for an analytical
            # identity at an anchor and is handed a value or a refusal; it never reaches into the
            # materialization store, never names a `MaterializationId`, and never learns whether the
            # answer was a hit or a fold. Cache choice stays inside the MME (ruled M-1 §2) precisely
            # because the consumer above it cannot see far enough to make one.
            #
            # `on_behalf_of` is the one thing passed DOWN: not a request for different treatment, but
            # the workload evidence of §8 — this demand for `Revenue@Month` exists because someone
            # asked for `AOV@Month`.
            served = self.families.measure(component, anchor, data_state=data_state,
                                           on_behalf_of=subject)
            if not served.served:
                return Answer(route=REFUSED, refusal=Refusal(
                    "role-unfilled", subject,
                    f"role {role!r} is filled by {component.family_id!r}, which cannot be served at "
                    f"{anchor}: {served.refusal.detail}"))
            states[role] = served.value

        # COMPATIBILITY. Asked BEFORE any arithmetic, over states that all exist — which is the whole
        # point: two individually valid components can be jointly meaningless.
        if basis.requires_common_participation:
            roles = list(states)
            reference = states[roles[0]]
            for role in roles[1:]:
                agreement = reference.instance.compatible_with(states[role].instance)
                if not agreement:
                    return Answer(route=REFUSED, refusal=Refusal(
                        "incompatible-basis", subject,
                        f"roles {roles[0]!r} and {role!r} are both ESTABLISHED AND AVAILABLE at "
                        f"{anchor} and are not jointly usable [{agreement.code}]: {agreement.detail}. "
                        f"{law.required_basis.note if law.required_basis else ''} The word doing the "
                        f"work is MATCHING — components that ranged over different contributions are "
                        f"individually valid and jointly meaningless, so their combination is a number "
                        f"about no population".strip()))

        apply = self.families.provider.capability(law.name, "apply")
        keys: set[tuple] = set()
        for state in states.values():
            keys |= set(state.cells)
        cells: dict[tuple, Any] = {}
        undefined: list[tuple] = []
        for key in sorted(keys):
            payloads = {role: state.cells.get(key) for role, state in states.items()}
            if any(p is None for p in payloads.values()):
                undefined.append(key)
                continue
            result = apply(payloads, dict(expression.parameters))
            if result is None:
                # §4.3's case: the basis is established and the expression is UNDEFINED on it. A
                # governed answer about that cell, not an error and not a zero.
                undefined.append(key)
                continue
            cells[key] = result

        # **THE OUTPUT IS ATTRIBUTED TO THE EVIDENCE STATE ITS OPERANDS CAME FROM**, where they agree on
        # one. Where they do not — possible only for a basis the law does not require common participation
        # for — it is attributed to none, which is what `UNSTATED_DATA_STATE` says: not a lie about a
        # single evidence state, and not a new token invented to describe a mixture.
        operand_states = {st.instance.data_state for st in states.values()}
        attributed = operand_states.pop() if len(operand_states) == 1 else UNSTATED_DATA_STATE
        output = ExpressionOutput(point=expression.at(anchor), constructor=law.name, cells=cells,
                                  instance=expression.instance(data_state=attributed),
                                  basis_id=basis.basis_id)
        for state in states.values():
            for d in state.disclosures:
                output = output.with_disclosure(d)
        if undefined:
            output = output.with_disclosure(Disclosure(
                "undefined-on-basis",
                f"{len(undefined)} cell(s) carry no value: the basis is established there and the "
                f"expression is UNDEFINED on it (ToD v8 §4.3). Distinct from absent and from zero"))
        return Answer(route=EVALUATED, value=output)


__all__ = ["ExpressionEvaluator"]

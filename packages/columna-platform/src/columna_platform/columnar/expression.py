"""
columna_platform.columnar.expression — **the columnar expression evaluator, ABOVE the columnar MME.**

The positional twin of `kernel.expression.ExpressionEvaluator`, and the same architectural statement:

    **MME manages only family materializations `F@A`.**  — Huayin, 2026-09-29 (M-2 §1)

    estimate(HLLSketch@Month)
      ↓
    columnar MME supplies HLLSketch@Month                ← `families.measure(...)`, the seam
      ↓
    finalizer/evaluator                                  ← here
      ↓
    estimate                                             ← returned, and NOT retained anywhere

WHY THIS IS A SEPARATE MODULE AND NOT A SUBCLASS
------------------------------------------------
The two evaluators share a shape and not an implementation, because the substrate difference is real:
the kernel's works over `dict[tuple, Any]` cells and asks compatibility of instances, while this one works
over Arrow arrays on a shared `CoordinateIndex` and must FIRST ask whether the two operands are even laid
out on the same index. `layouts-differ` has no kernel analogue — a dict has no layout — and a common base
class would have had to make that check optional, which is how a positional engine acquires the habit of
discovering alignment by joining on coordinate values. Ruled at the columnar unit and unchanged here:
that would be relational discovery of analytical alignment.

THE THREE CHECKS, IN THE ORDER THAT MATTERS
-------------------------------------------
  1. **layout** — one coordinate index, or refuse. Positional arithmetic needs it and will not infer it.
  2. **compatibility** — authority to combine, asked before any arithmetic over two present columns.
  3. **support** — is every required operand ESTABLISHED over its domain? Deliberately LAST: authority to
     combine is prior to the evidence for the values, so a jointly-unusable basis refuses on participation
     even when it also wants state.

NO EXPRESSION CACHE (M-2 §1)
----------------------------
There is no store on this class and no `retain` parameter on `evaluate`. See the long note in
`kernel.expression`; the reasoning is identical and is not repeated.
"""
from __future__ import annotations

from typing import Any, Optional

from columna_platform.kernel import (
    Anchor,
    Answer,
    Disclosure,
    EVALUATED,
    GovernedExpression,
    REFUSED,
    Refusal,
    UNSTATED_DATA_STATE,
)

from .index import AnchorInstance
from .mme import ColumnarExpressionOutput, ColumnarFamilyState
from .provider import sketch_parameters
from columna_platform.kernel.law import STRUCTURED


class ColumnarExpressionEvaluator:
    """**Evaluate `E@A` from columnar family state supplied by a `ColumnarMME`.**

    The engine does not know this class exists: no back reference, no registration, no hook."""

    def __init__(self, family_supplier: Any) -> None:
        #: The `ColumnarMME`, held as a **family supplier** and used through `measure`, `expression`,
        #: `law_of` and `provider`. Named for the role, because a Fulfillment Coordinator (ruled §6) will
        #: later fill this slot unchanged.
        self.families = family_supplier

    @property
    def mme(self) -> Any:
        return self.families

    def evaluate(self, expression_id: str, anchor: Anchor, *,
                 basis_id: Optional[str] = None,
                 data_state: Optional[str] = None) -> Answer:
        """**Evaluate `E@A` positionally, from family state supplied by the columnar MME.**

        No cache lookup opens this method and no `retain` parameter closes it: M-2 §1 removes the
        expression cache, so every call re-establishes from a sufficient basis. The family operands are
        NOT re-established — `measure` hits the family materializations, which is the cache that matters."""
        expression = self.families.expression(expression_id)
        law = self.families.law_of(expression_id)

        routes = ([b for b in expression.admitted_bases if b.basis_id == basis_id]
                  if basis_id else list(expression.admitted_bases))
        if not routes:
            return Answer(route=REFUSED, refusal=Refusal(
                "no-admitted-basis", f"{expression_id}@{anchor}",
                "this expression admits no sufficient basis: well-formed and not evaluable."))

        failures = []
        for basis in routes:
            attempt = self._establish(expression, law, basis, anchor, data_state)
            if attempt.served:
                return Answer(route=EVALUATED, value=attempt.value,
                              disclosures=attempt.value.disclosures, seeded_from=basis.basis_id)
            # the INNER code rides in the wrapped detail: a caller branching on "why did every
            # route fail" needs the per-route code, not only the outer one.
            failures.append(f"basis {basis.basis_id!r} [{attempt.refusal.code}]: "
                            f"{attempt.refusal.detail}")
        return Answer(route=REFUSED, refusal=Refusal(
            "no-sufficient-basis-establishes", f"{expression_id}@{anchor}",
            " | ".join(failures) + ". Physical availability is not analytical authority."))

    def _establish(self, expression: GovernedExpression, law, basis, anchor: Anchor,
                   data_state: Optional[str] = None) -> Answer:
        subject = f"{expression.expression_id}@{anchor} via {basis.basis_id}"
        states: dict[str, ColumnarFamilyState] = {}
        for role in basis.component_laws:
            # ── THE SEAM ─────────────────────────────────────────────────────────────────────
            # The only way this evaluator obtains columnar family state. `on_behalf_of` is the §8
            # route/use evidence: this demand for `revenue@{month}` exists because someone asked for
            # `average_order_value@{month}`.
            served = self.families.measure(basis.components[role], anchor, data_state=data_state,
                                           on_behalf_of=subject)
            if not served.served:
                return Answer(route=REFUSED, refusal=Refusal(
                    "role-unfilled", subject,
                    f"role {role!r} is filled by {basis.components[role]!r}, which cannot be served at "
                    f"{anchor}: {served.refusal.detail}"))
            states[role] = served.value

        # ── ALIGNMENT AND COMPATIBILITY, BOTH BEFORE ANY ARITHMETIC ──────────────────────
        roles = list(states)
        reference = states[roles[0]]
        for role in roles[1:]:
            other = states[role]
            if reference.index.identity != other.index.identity:
                return Answer(route=REFUSED, refusal=Refusal(
                    "layouts-differ", subject,
                    f"roles {roles[0]!r} and {role!r} are laid out on different coordinate indexes "
                    f"({reference.index.identity} vs {other.index.identity}). A positional kernel needs "
                    f"one layout, and this path will NOT discover the correspondence by joining the two "
                    f"columns on their coordinate values — that would be relational discovery of "
                    f"analytical alignment. An explicit alignment against a governed target index is the "
                    f"lawful remedy."))
            if basis.requires_common_participation:
                agreement = reference.instance.compatible_with(other.instance)
                if not agreement:
                    return Answer(route=REFUSED, refusal=Refusal(
                        "incompatible-basis", subject,
                        f"roles {roles[0]!r} and {role!r} are position-aligned on ONE coordinate index and "
                        f"are not jointly usable [{agreement.code}]: {agreement.detail}. **THE ARITHMETIC "
                        f"HAS NOT RUN.** Both columns are present, the same length, and perfectly "
                        f"aligned; what is missing is analytical authority to combine them, and no amount "
                        f"of physical readiness supplies it."))

        # ── AND ONLY THEN: IS EVERY REQUIRED OPERAND ESTABLISHED OVER ITS DOMAIN? ─────────
        # Deliberately AFTER compatibility: authority to combine two columns is prior to the evidence
        # for their values, so a jointly-unusable basis refuses on participation even when it also
        # wants state. What this check catches is the basis that is lawful and still not computable —
        # *"AOV refuses because one required basis operand is not established."* (2026-09-29)
        for role, state in states.items():
            if state.wants_state:
                return Answer(route=REFUSED, refusal=Refusal(
                    "basis-operand-wants-state", subject,
                    f"role {role!r} is filled by {state.family_id!r}, which has want of state at "
                    f"{[list(p) for p in state.points_wanting_state()]}: those points participate and the "
                    f"value this basis requires of them is not established. **THE ARITHMETIC HAS NOT "
                    f"RUN.** One required basis operand is not established, so the expression is refused — "
                    f"it is NOT evaluated over the subset of points whose operands happen to be supported, "
                    f"and the other role(s) "
                    f"{[r for r in states if r != role]} are unaffected in their own right: a population "
                    f"operand still counts every participating point. Establish the missing value, or "
                    f"admit a basis that does not require it."))

        # ── HANDED TO THE PROVIDER BY GOVERNED LAW NAME ──────────────────────────────────
        # This was `kernel = "ratio" if law.name == "MEAN" else "hll_estimate"` — a governed evaluator
        # naming a PHYSICAL kernel, and choosing between two by a hard-coded law switch (recon E-X's
        # finding). The law name now goes down and the provider's own capability table resolves it, exactly
        # as `ProviderProfile.capability(law.name, "apply")` has always done on the in-memory side.
        #
        # **THE EVALUATOR NO LONGER KNOWS A SINGLE PHYSICAL NAME.** Adding a third constructor is a change
        # to a provider; it used to be a change to this file.
        values = self.families.provider.evaluate_positional(
            {role: states[role].values for role in states}, law=law.name,
            parameters=dict(expression.parameters))
        # attributed to the operands' evidence state where they agree on one; to none where they do not
        operand_states = {st.instance.data_state for st in states.values()}
        attributed = operand_states.pop() if len(operand_states) == 1 else UNSTATED_DATA_STATE
        output = ColumnarExpressionOutput(
            expression_id=expression.expression_id,
            anchor_instance=AnchorInstance(index=reference.index,
                                           instance=self.families.authority.instance_of(
                                               expression.expression_id
                                           ).with_data_state(attributed)),
            values=values, constructor=law.name, basis_id=basis.basis_id)
        for state in states.values():
            for d in state.disclosures:
                output = output.with_disclosure(d)
        undefined = values.null_count
        if undefined:
            output = output.with_disclosure(Disclosure(
                "undefined-on-basis",
                f"{undefined} position(s) carry no value: the basis is established there and the "
                f"expression is UNDEFINED on it (ToD v8 §4.3). Distinct from absent and from zero — and "
                f"note that this null is PRODUCED BY THE KERNEL as a governed standing, not read as one."))
        if any(s.value_form == STRUCTURED for s in states.values()):
            params = {role: sketch_parameters(s.values[0].as_py())
                      for role, s in states.items() if s.value_form == STRUCTURED
                      and len(s.values) and s.values[0].as_py() is not None}
            if params:
                output = output.with_disclosure(Disclosure(
                    "sketch-parameters",
                    f"finalized from structured state with parameters {params}. Sketch parameters are "
                    f"COMPATIBILITY-BEARING: two sketches of different lg_k are not mergeable."))
        return Answer(route=EVALUATED, value=output)


__all__ = ["ColumnarExpressionEvaluator"]

"""Exact SUM continuation across ONE positively licensed movement.

THE PROPOSITION, and the only one:

    A positively licensed analytical movement can carry exact sufficient state from one governed
    anchor to one coarser governed anchor, while mechanically possible but unlicensed movement
    refuses.

LAW IS ASKED BEFORE ARITHMETIC, and that ordering is the proof. The values here are trivially
foldable — `Operator("sum")` is a monoid with `combine="sum"`, and the arrays would concatenate
whether or not anyone licensed anything. That is precisely why the licence is checked first: the
question "can these be added?" and the question "may this family be moved?" have different answers,
and a system that asks only the first will always say yes.

THE FOLD IS DONE IN `Decimal`, DELIBERATELY. The governed domain is exact decimal and the ruling of
2026-09-12 requires it be carried exactly where the substrate can carry it exactly. Folding through
any binary-floating-point step would satisfy the movement and quietly break the value, which is the
failure the ruling names. Python's `Decimal` is exact for addition, so the continuation inherits no
substrate behaviour it did not choose.
"""
from __future__ import annotations
from collections import OrderedDict
from dataclasses import replace
from decimal import Decimal

import pyarrow as pa

from columna_core.governed.resolve import C8_CONTINUATION, ESTABLISHED

from .movement import MovementLicence, licence_for
from .refusals import WantOfLaw, WantOfState
from .state import AnalyticalIdentity, RetainedState


def established_continuation_law(law_view) -> str:
    """The family's C8 continuation law name, or refuse. Never guessed from the operator."""
    c8 = law_view[C8_CONTINUATION]
    if c8.standing != ESTABLISHED:
        raise WantOfLaw(f"the family's continuation is {c8.standing}; there is no law to move under",
                        subject=law_view.canonical_reference)
    # C8's value is the resolved `FoundationLaw` itself, not a name. Read `.name` rather than
    # stringifying it: a law's repr is its whole semantic content, and comparing a licence against a
    # repr would make the comparison sensitive to every future field added to the law.
    value = c8.value
    name = getattr(value, "name", None) or (value.get("law") if isinstance(value, dict) else None)
    if not name:
        raise WantOfLaw(f"C8 is established but names no law (value={value!r})",
                        subject=law_view.canonical_reference)
    return name


def continue_to(law_view, state: RetainedState, licence: MovementLicence,
                *, target_anchor: str) -> RetainedState:
    """Fold `state` from its anchor to `target_anchor` under `licence`. Refuses before it folds."""
    subject = law_view.canonical_reference
    continuation = established_continuation_law(law_view)

    # ── LAW FIRST. Nothing below this line touches a value. ─────────────────────────────────────
    why_not = licence_for(licence, source=state.identity.anchor, target=target_anchor,
                          continuation_law=continuation)
    if why_not is not None:
        raise WantOfLaw(f"cannot continue {state.identity.anchor!r} -> {target_anchor!r}: {why_not}",
                        subject=subject)

    if continuation != "SUM":
        # Bounded on purpose. Proof B proves ONE law; a second would be a movement framework.
        raise WantOfLaw(f"this proof continues SUM only; the family's continuation is {continuation!r}",
                        subject=subject)

    # ── then state ──────────────────────────────────────────────────────────────────────────────
    if state.table is None:
        raise WantOfState(
            "the retained state carries values but no anchor coordinates, so it cannot be folded "
            "across one; a movement needs to know where each contribution sits", subject=subject)
    missing = [c for c in licence.target_components if c not in state.anchor_columns]
    if missing:
        raise WantOfState(f"the retained state does not carry the target coordinate(s) {missing}",
                          subject=subject)

    folded = _sum_exactly(state, licence.target_components)

    return replace(
        state,
        identity=AnalyticalIdentity(state.identity.family_id, target_anchor),   # SAME FAMILY
        table=folded,
        anchor_columns=tuple(licence.target_components),
        array=folded.column(_value_column(state)).combine_chunks(),
        standing=replace(state.standing, movement=licence.describe()),
    )


def _value_column(state: RetainedState) -> str:
    non_anchor = [n for n in state.table.column_names if n not in state.anchor_columns]
    if len(non_anchor) != 1:
        raise WantOfState(f"expected exactly one value column, found {non_anchor}",
                          subject=state.identity.family_id)
    return non_anchor[0]


def _sum_exactly(state: RetainedState, keys) -> pa.Table:
    """Group by `keys` and add in `Decimal`. Deterministic order: first appearance.

    Written out rather than delegated to a dataframe `group_by().sum()` for one reason — the exact
    decimal guarantee. A library fold is free to widen, re-associate, or route through a float, and
    the ruling this proof serves forbids exactly that. Twelve lines that are provably exact beat a
    one-liner whose exactness is a property of somebody else's release notes."""
    value_col = _value_column(state)
    cols = {n: state.table.column(n).to_pylist() for n in state.table.column_names}
    keys = tuple(keys)

    totals: "OrderedDict[tuple, Decimal]" = OrderedDict()
    for i in range(state.table.num_rows):
        k = tuple(cols[c][i] for c in keys)
        v = cols[value_col][i]
        if v is None:
            # Unreachable on the admitted path — admission refuses a carrier with absences whose
            # meaning the law does not govern — but stated rather than assumed, because a fold that
            # silently skips a null has decided what absence means.
            raise WantOfState("a null reached continuation; absence semantics are not governed here",
                              subject=state.identity.family_id)
        totals[k] = totals[k] + v if k in totals else v

    out = {c: [k[i] for k in totals] for i, c in enumerate(keys)}
    out[value_col] = pa.array(list(totals.values()), type=state.table.schema.field(value_col).type)
    return pa.table(out)

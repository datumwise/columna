"""
columna_platform.kernel.value — **continuation-bearing family state, and finalized expression output.**

THIS MODULE IS THE FLAGSHIP DISTINCTION, AS TWO TYPES
-----------------------------------------------------
    FamilyState        CONTINUATION-BEARING.      May seed a later continuation.
    ExpressionOutput   FINALIZED, NOT continuation-bearing. May be cached and served, and may NEVER
                       become family continuation state.

The HLL case is why this is a type distinction and not a flag. `HLLSketch@A → merge → HLLSketch@B` is
family continuation: the sketch is the family's VALUE and the union is its composition. `estimate(
HLLSketch@B) → 3` is an EXPRESSION: the estimate is a finalization, and **two estimates cannot be merged
into the estimate at a coarser anchor.** Both objects are integers-and-registers in memory; only their
sort says which one may seed. A Boolean on one class would put those two facts one mutation apart.

So `ExpressionOutput` has **no merge path at all** — not a merge that refuses, no merge. The kernel's
continuation entry point is typed to `FamilyState`, and the refusal a caller sees when they try anyway
is stated once, in `mme.py`, as a governed verdict rather than a `TypeError`.

A STATE IS A CUBE, NOT A NUMBER
-------------------------------
`F@A` retains a value for every cell of `A` that has a contribution. Coarsening projects cells onto the
target anchor and folds the collisions with the law's composition — which is the whole of continuation's
mechanics, and is why the composition has to be associative and commutative to be usable at all.

`forgotten_since_root` RIDES ON THE STATE, and it is the laundering guard. A state at a non-root anchor
remembers everything forgotten to reach it, so the continuation region is asked about the WHOLE route
rather than the last hop — otherwise an intermediate materialization becomes a way to obtain an answer
the law forbids, and physical availability would have become analytical authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Callable, Mapping, Optional

from .geometry import Anchor, KernelRefusal
from .sorts import ExpressionPoint, FamilyPoint
from .standing import AnalyticalInstance, Disclosure


@dataclass(frozen=True)
class FamilyState:
    """**`F@A`'s retained, continuation-bearing value.**"""

    point: FamilyPoint
    law: str
    value_form: str
    #: cell key (in `point.anchor.order`) → the law's value payload
    cells: Mapping[tuple, Any]
    instance: AnalyticalInstance
    #: Everything forgotten to reach this anchor FROM `R_F`. Empty exactly at the root.
    forgotten_since_root: frozenset[str] = frozenset()
    disclosures: tuple[Disclosure, ...] = ()

    #: **A CLASS-LEVEL FACT, not an instance flag.** There is no code path that produces a
    #: `FamilyState` which is not continuation-bearing; the sort is the type.
    CONTINUATION_BEARING = True

    @property
    def anchor(self) -> Anchor:
        return self.point.anchor

    @property
    def at_root(self) -> bool:
        return not self.forgotten_since_root

    # ── THE SUBSTRATE-NEUTRAL READ SURFACE (B-2) ─────────────────────────────────────────────
    #
    # Ruled (Huayin, 2026-09-30): *"FrameQLService must not know whether the fulfilled family state came
    # from the kernel or columnar substrate… A common read interface must preserve the stronger columnar
    # standing semantics; it must not reduce them to the weaker in-memory representation. Prefer adapting
    # the kernel state upward."*
    #
    # So the surface is `coordinates` + `cell(coordinate)`, which is what `ColumnarFamilyState` ALREADY
    # had, and this class grows to meet it. **THE DIRECTION IS THE RULING.** The other direction — a
    # `.cells` mapping on the columnar state — was available and is refused, because a dict cannot refuse:
    # `ColumnarFamilyState.cell` raises `want-of-state-at-a-point` where a participating point's required
    # value is not established, and a mapping would have to answer that with a null for the caller to
    # interpret. Widening the weaker representation is free; narrowing the stronger one loses a verdict.

    @property
    def coordinates(self) -> tuple[tuple, ...]:
        """**The points this state retains a value for**, in insertion order.

        The neutral half-answer to "what is in here". It is deliberately not a set operation and not
        sorted: a consumer that needs an order imposes its own, and `frameql` does."""
        return tuple(self.cells)

    def cell(self, coordinate: tuple) -> Any:
        """One value, by coordinate. **REFUSES where this state retains none.**

        The kernel substrate has no want-of-state: a cell is retained or the point contributed nothing, so
        the only refusal available here is absence. That is a WEAKER condition than the columnar twin's and
        the shapes still match, which is the point — a consumer written against this surface gets the
        columnar refusal for free when it is handed columnar state, and never has to ask which it holds."""
        try:
            return self.cells[coordinate]
        except KeyError:
            raise KernelRefusal(
                "no-value-at-this-point", f"{self.point.family_id}@{self.anchor}",
                f"this state retains no value at {coordinate!r}. It is not zero and not an absence to "
                f"interpret: the point either does not participate or contributed nothing, and which of "
                f"those it is is a question for the constitution rather than for this payload.") from None

    def fold_onto(self, target: Anchor, merge: Callable[[Any, Any], Any]) -> "FamilyState":
        """Project every cell onto `target` and fold the collisions with the law's composition.

        **NO LAWFULNESS IS CHECKED HERE, DELIBERATELY.** This is the arithmetic; whether the edge is
        admitted is `mme.py`'s adjudication, and it has already been made before this is called. Keeping
        them apart is what lets the adjudication be tested without arithmetic and the arithmetic without
        a publication."""
        folded: dict[tuple, Any] = {}
        for cell, payload in self.cells.items():
            key = target.project(cell, self.anchor)
            folded[key] = payload if key not in folded else merge(folded[key], payload)
        return FamilyState(
            point=FamilyPoint(self.point.family_id, target),
            law=self.law, value_form=self.value_form, cells=folded, instance=self.instance,
            forgotten_since_root=self.forgotten_since_root | self.anchor.forgets(target),
            disclosures=self.disclosures)

    def with_disclosure(self, disclosure: Disclosure) -> "FamilyState":
        return replace(self, disclosures=self.disclosures + (disclosure,))

    def __str__(self) -> str:
        return f"FamilyState({self.point}, {len(self.cells)} cell(s), {self.value_form})"


@dataclass(frozen=True)
class ExpressionOutput:
    """**`E@A`'s finalized result. It has no merge path and it never becomes family state.**

    Cacheable and servable — that is not in question and is proof 5's other half. What it cannot do is
    seed a continuation, and the absence of `fold_onto` on this class is the primary enforcement. The
    verdict a caller gets when they try is `mme.py`'s, so that the refusal is a governed statement rather
    than whatever Python says about a missing attribute."""

    point: ExpressionPoint
    constructor: str
    #: cell key (in `point.anchor.order`) → the finalized value
    cells: Mapping[tuple, Any]
    instance: AnalyticalInstance
    #: WHICH admitted route established this. Provenance, **not identity** — the same expression
    #: established by two lawful routes is one expression (ruling 4, 2026-09-28).
    basis_id: Optional[str] = None
    disclosures: tuple[Disclosure, ...] = ()

    CONTINUATION_BEARING = False

    @property
    def anchor(self) -> Anchor:
        return self.point.anchor

    @property
    def coordinates(self) -> tuple[tuple, ...]:
        """**The points this finalized result covers.** The same neutral surface as `FamilyState`'s."""
        return tuple(self.cells)

    def cell(self, coordinate: tuple) -> Any:
        """One finalized value, by coordinate. Refuses on absence, exactly as the family twin does.

        A finalized value carries no want-of-state — the evaluation either produced one or refused before
        producing this object — so absence is the only condition, and `ColumnarExpressionOutput.cell` is
        total for the same reason."""
        try:
            return self.cells[coordinate]
        except KeyError:
            raise KernelRefusal(
                "no-value-at-this-point", f"{self.point.expression_id}@{self.anchor}",
                f"this finalized result covers no point {coordinate!r}.") from None

    def with_disclosure(self, disclosure: Disclosure) -> "ExpressionOutput":
        return replace(self, disclosures=self.disclosures + (disclosure,))

    def __str__(self) -> str:
        return f"ExpressionOutput({self.point}, {len(self.cells)} cell(s), via {self.basis_id})"


@dataclass(frozen=True)
class Answer:
    """**A TOTAL serving verdict.** Either a value and the route that reached it, or a refusal — and
    never silence. `route` is a governed fact a consumer should be able to show, which is why it is on
    the answer rather than logged."""

    route: str
    value: Optional[Any] = None
    refusal: Optional[Any] = None
    disclosures: tuple[Disclosure, ...] = ()
    #: For a continued answer: where it was seeded from. Named, because "served from a non-root
    #: materialization" is exactly the fact an auditor of an MME wants and cannot recompute.
    seeded_from: Optional[Any] = None
    considered: tuple[str, ...] = field(default_factory=tuple)

    @property
    def served(self) -> bool:
        return self.refusal is None

    def __bool__(self) -> bool:
        return self.served

    def unwrap(self):
        if self.refusal is not None:
            raise KernelRefusal(self.refusal.code, self.refusal.subject, self.refusal.detail)
        return self.value

    def cell(self, key: tuple = ()):  # readability in exhibits and tests
        return self.unwrap().cells[key]

    def __str__(self) -> str:
        if not self.served:
            return f"REFUSED {self.refusal}"
        extra = f" seeded from {self.seeded_from}" if self.seeded_from else ""
        marks = "".join(f"  ⚠ {d.code}" for d in self.disclosures)
        return f"{self.route.upper():<10} {self.value}{extra}{marks}"


__all__ = ["Answer", "ExpressionOutput", "FamilyState"]

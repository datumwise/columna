"""
columna_platform.columnar.standing — **governed standing, carried independently of Arrow nullability.**

THE RULING THIS MODULE EXISTS TO SATISFY
----------------------------------------
*"Arrow NULL has no intrinsic ToD standing. Arrow nullability does not by itself mean: nonexistent point;
`NA`; nonparticipation; unsupported evidence; known-empty fiber; want of state. Physical nulls can only be
interpreted through governed representation contracts."* — Huayin, 2026-09-28

And the minimum the proof must demonstrate: *"a participating source point is unsupported for Revenue;
participation remains known independently of Revenue value presence; Count semantics are not reduced to
`count(non-null Revenue)`."*

TWO MASKS, AND THE REASON THERE ARE EXACTLY TWO
-----------------------------------------------
This is deliberately **not** the complete v8 standing system (that is out of scope). It is the smallest
governed representation that prevents null-driven semantics, and it is two arrays because the proof needs
two facts to come apart:

    `participation`   is this point IN the family's population?  A fact about the population law.
    `support`         is there EVIDENCE for a value at this point?  A fact about the carrier.

**A point may participate and be unsupported.** An order the merchant accepted, whose amount was never
recorded, is *in* the population — `OrderCount` must count it — and supplies *no* contribution to
`Revenue`. Read off Arrow validity, those two facts collapse into one and `COUNT` silently becomes
`count(non-null revenue)`, which is a different measure with a different answer. So:

    a VALUE-BEARING reduction contributes where   participation ∧ support
    a POPULATION reduction contributes where      participation

`contributing_for` is the single place that distinction is made, so no provider has to remember it.

**WHAT IS DEFERRED, NAMED RATHER THAN OMITTED.** `NA` (resolved inapplicability at a point that exists),
known-empty-fibre versus identity-valued, and want-of-state are not represented here. Point EXISTENCE is
carried by membership in the `CoordinateIndex` — the ruling's own permitted encoding — so it needs no mask.
The rest await the applicability/participation/support unit, and until then nothing in this package reads a
null as any of them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import pyarrow as pa

from columna_platform.kernel import AnalyticalInstance, KernelRefusal

#: The two reduction shapes, and which mask each one is entitled to.
VALUE_BEARING = "value-bearing"      # contributes where participation ∧ support
POPULATION = "population"            # contributes where participation


@dataclass(frozen=True)
class ColumnStanding:
    """**The governed standing of ONE family column, at ONE analytical instance.**

    `instance` is per-COLUMN and that is the point: *"Two columns in the same Arrow RecordBatch, Parquet
    file, or Iceberg snapshot are not analytically compatible merely because they are co-located."* Putting
    the instance on the column rather than on the block makes an incompatible co-location REPRESENTABLE —
    so the refusal can be demonstrated on two columns sitting in one batch with identical positions, which
    is the only version of that proof worth having."""

    family_id: str
    instance: AnalyticalInstance
    participation: pa.BooleanArray
    support: pa.BooleanArray
    note: str = ""

    def __post_init__(self) -> None:
        if len(self.participation) != len(self.support):
            raise KernelRefusal(
                "standing-length-mismatch", self.family_id,
                f"participation has {len(self.participation)} entries and support has "
                f"{len(self.support)}. Both are position-aligned to one coordinate index.")
        for name, mask in (("participation", self.participation), ("support", self.support)):
            if mask.null_count:
                raise KernelRefusal(
                    "null-in-a-standing-mask", self.family_id,
                    f"the {name} mask carries {mask.null_count} null(s). **A STANDING MASK MAY NOT BE "
                    f"NULL**: a null here would mean 'we do not know whether this point participates', "
                    f"which is a third standing this model does not represent — and reading it as either "
                    f"True or False would be the engine deciding a governed fact. Represent the unknown "
                    f"case when the standing unit introduces it; do not encode it as absence.")

    def __len__(self) -> int:
        return len(self.participation)

    def contributing_for(self, shape: str) -> pa.BooleanArray:
        """**The one place the two reduction shapes are distinguished.**

        A provider asks for the mask its law's shape entitles it to and never assembles one itself, which
        is what keeps `count(non-null value)` from reappearing inside an aggregation."""
        if shape == POPULATION:
            return self.participation
        if shape == VALUE_BEARING:
            return pa.compute.and_(self.participation, self.support)
        raise KernelRefusal("unknown-reduction-shape", self.family_id,
                            f"{shape!r} is not one of {[POPULATION, VALUE_BEARING]}")

    def take(self, positions: Sequence[int]) -> "ColumnStanding":
        """This standing, re-positioned onto another layout. Used by explicit alignment only."""
        idx = pa.array(positions, type=pa.int64())
        return ColumnStanding(
            family_id=self.family_id, instance=self.instance,
            participation=self.participation.take(idx), support=self.support.take(idx),
            note=self.note)

    def summary(self) -> str:
        p = self.participation.to_pylist()
        s = self.support.to_pylist()
        return (f"participation {sum(p)}/{len(p)}  support {sum(s)}/{len(s)}  "
                f"contributing {sum(1 for a, b in zip(p, s) if a and b)}")


def all_true(n: int) -> pa.BooleanArray:
    return pa.array([True] * n, type=pa.bool_())


def mask(values: Sequence[bool]) -> pa.BooleanArray:
    return pa.array(list(values), type=pa.bool_())


def standing(family_id: str, instance: AnalyticalInstance, *, n: int,
             participation: Optional[Sequence[bool]] = None,
             support: Optional[Sequence[bool]] = None, note: str = "") -> ColumnStanding:
    """Build a column standing, defaulting each mask to all-true.

    **The defaults are ALL-TRUE and not derived from the value array**, deliberately. Deriving support
    from validity is the exact shortcut this module exists to prevent, and a default that did it would
    make the right behaviour opt-in."""
    return ColumnStanding(family_id=family_id, instance=instance,
                          participation=mask(participation) if participation is not None else all_true(n),
                          support=mask(support) if support is not None else all_true(n),
                          note=note)


__all__ = ["ColumnStanding", "POPULATION", "VALUE_BEARING", "all_true", "mask", "standing"]

"""
columna_platform.columnar.standing — **governed standing, carried independently of Arrow nullability.**

THE RULING THIS MODULE EXISTS TO SATISFY
----------------------------------------
*"Arrow NULL has no intrinsic ToD standing. Arrow nullability does not by itself mean: nonexistent point;
`NA`; nonparticipation; unsupported evidence; known-empty fiber; want of state. Physical nulls can only be
interpreted through governed representation contracts."* — Huayin, 2026-09-28

TWO MASKS, AND THE TWO DIFFERENT JOBS THEY DO
---------------------------------------------
    `participation`   is this point IN the family's population?   A fact about the population law.
    `support`         is the value required at this point ESTABLISHED?   A fact about the carrier.

**THE CORRECTION OF 2026-09-29, AND THE ERROR IT REPLACES.** An earlier revision of this module had a
single `contributing_for(shape)` that returned `participation ∧ support` for a value-bearing reduction. That
is wrong, and the ruling that corrects it is exact:

    *"Participation determines the contributing domain. Support determines whether the values required over
    that participating domain are established."* — Huayin, 2026-09-29

So `participation ∧ support` is **not a contribution filter**. Using it as one silently deletes a
participating point from a value-bearing fold and then reports a number as though the fold were complete:

    participating + supported     → the contribution is available;
    participating + unsupported   → **the reduction HAS WANT OF STATE.** It does not quietly drop the
                                    point, and it does not compute a total over the survivors.

    a VALUE-BEARING reduction contributes over  participation,  and REQUIRES support over all of it
    a POPULATION   reduction contributes over  participation,  and requires no value evidence at all

Count therefore remains independent, which is the whole reason the two masks exist: if three Orders
participate, `OrderCount = 3` — and a missing Revenue on one of them changes `OrderCount` by nothing, while
`Revenue` refuses and any expression that requires Revenue as a basis operand refuses with it.

    contributing_domain(shape)  →  the domain, ALWAYS `participation`
    want_of_state(shape)        →  where a required value is not established (empty for POPULATION)

Two methods rather than one, because the old single method could only express the wrong answer.

**WHAT `support = False` IS NOT.** It is not `NA`, not a known-empty fibre, not nonparticipation, and not a
nonexistent point, and nothing in this package infers any of them from it. It is one fact only: *the value
required here is not established.* Point EXISTENCE is carried by membership in the `CoordinateIndex` — the
ruling's own permitted encoding. `NA`, known-empty-versus-identity, and the pointwise REPRESENTATION of want
of state await the applicability/participation/support unit; until then want of state is expressed as a
**refusal at the operation that requires the value**, never as a value and never as a third mask state.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import pyarrow as pa
import pyarrow.compute as pc

from columna_platform.kernel import AnalyticalInstance, KernelRefusal

#: The two reduction shapes. Both contribute over PARTICIPATION; they differ in what they require of it.
VALUE_BEARING = "value-bearing"      # requires an established value at every participating point
POPULATION = "population"            # requires membership only


def _shape_or_refuse(shape: str, family_id: str) -> str:
    if shape not in (POPULATION, VALUE_BEARING):
        raise KernelRefusal("unknown-reduction-shape", family_id,
                            f"{shape!r} is not one of {[POPULATION, VALUE_BEARING]}")
    return shape


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

    # ── the domain, and what is required over it. TWO questions, never folded into one. ───────
    def contributing_domain(self, shape: str) -> pa.BooleanArray:
        """**The contributing domain of a reduction, which is `participation` for EVERY shape.**

        Support is deliberately absent from this computation. *"Participation determines the contributing
        domain"* — so an unsupported participating point is IN the domain of a value-bearing fold and the
        fold owes an answer about it, which is why the answer can be a refusal but cannot be a total that
        pretends the point was never there."""
        _shape_or_refuse(shape, self.family_id)
        return self.participation

    def want_of_state(self, shape: str) -> pa.BooleanArray:
        """**Where the reduction REQUIRES a value that is not established:** `participation ∧ ¬support`.

        Empty for a `POPULATION` reduction, which needs no value evidence — a counted point is counted on
        its membership alone. This mask is *the reason a refusal is owed*; it is never a contribution
        filter, and nothing may subtract it from the domain."""
        if _shape_or_refuse(shape, self.family_id) == POPULATION:
            return pa.array([False] * len(self), type=pa.bool_())
        return pc.and_(self.participation, pc.invert(self.support))

    def wants_state(self, shape: str) -> bool:
        return bool(pc.any(self.want_of_state(shape)).as_py())

    def positions_wanting_state(self, shape: str) -> tuple[int, ...]:
        return tuple(i for i, w in enumerate(self.want_of_state(shape).to_pylist()) if w)

    def contributing_for(self, shape: str) -> pa.BooleanArray:
        """**RETIRED, and retired loudly rather than deleted quietly.**

        This method returned `participation ∧ support` and callers used it as a contribution filter, which
        silently removed participating-but-unsupported points from value-bearing folds. Ask
        `contributing_domain(shape)` for the domain and `want_of_state(shape)` for what the domain still
        needs; a caller that wanted the old mask wanted the old bug."""
        raise KernelRefusal(
            "retired-contribution-filter", self.family_id,
            "`contributing_for` computed `participation ∧ support` and was used to FILTER contributions. "
            "Support does not shrink the contributing domain — it validates it (ruled 2026-09-29). Use "
            "`contributing_domain(shape)` for the domain, and `want_of_state(shape)`/`wants_state(shape)` "
            "to find out whether the values that domain requires are established.")

    def take(self, positions: Sequence[int]) -> "ColumnStanding":
        """This standing, re-positioned onto another layout. Used by explicit alignment only."""
        idx = pa.array(positions, type=pa.int64())
        return ColumnStanding(
            family_id=self.family_id, instance=self.instance,
            participation=self.participation.take(idx), support=self.support.take(idx),
            note=self.note)

    def summary(self, shape: str = VALUE_BEARING) -> str:
        p = self.participation.to_pylist()
        s = self.support.to_pylist()
        return (f"participation {sum(p)}/{len(p)}  support {sum(s)}/{len(s)}  "
                f"contributing domain {sum(p)}  "
                f"wants state at {len(self.positions_wanting_state(shape))} position(s)")


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

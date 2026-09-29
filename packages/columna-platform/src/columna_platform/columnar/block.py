"""
columna_platform.columnar.block — **a physical container, and never analytical identity.**

    *"A block is a physical container, never analytical identity… A block is not a family and does not
    confer continuation rights… Co-location never creates compatibility."* — Huayin, 2026-09-28

A `GovernedBlock` is one Arrow `RecordBatch` — the coordinate columns of a `CoordinateIndex`, plus one
value column per family — together with the per-column governed standing. That is all it is. It answers no
question about whether anything in it may be served, combined, or continued; every such question is put to
the kernel, which is the analytical authority.

THE THREE THINGS THIS FILE REFUSES TO LET THE PHYSICS DECIDE
------------------------------------------------------------
**1 · Co-location is not compatibility.** Standing is per-COLUMN and carries its own analytical instance,
so two incompatible columns can sit in one batch at identical positions. `compatibility_of` reports the
verdict and the block never implies one. The proof puts an incompatible `OrderCount` in the same batch as
`Revenue` for exactly this reason: a refusal demonstrated across two batches could be mistaken for a
layout accident.

**2 · Arrow validity is not standing.** A value column may be nullable and its nulls mean nothing here.
`contributing(family, shape)` comes from `ColumnStanding`, never from `Array.is_valid()`. A test builds a
column whose nulls and whose support mask DISAGREE and shows the answers follow the mask.

**3 · A value column is not a display column.** `render` prints a structured payload opaquely, for the
reason the Frame-QL layer does: a sketch's `str()` emits a summary containing an `Estimate:` line, and
printing it would show a cardinality obtained through the family path rather than through the finalization
expression that is the only lawful route to one.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

import pyarrow as pa

from columna_platform.kernel import AnalyticalInstance, Compatibility, KernelRefusal

from .index import AnchorInstance, CoordinateIndex
from .standing import ColumnStanding, VALUE_BEARING

#: Column-name convention. A prefix, not a namespace: the block is a carrier and its column names are
#: physical labels. Nothing resolves a governed identity by parsing one.
VALUE_SUFFIX = "__value"


def value_column_name(family_id: str) -> str:
    return f"{family_id}{VALUE_SUFFIX}"


@dataclass(frozen=True)
class GovernedBlock:
    """One Arrow `RecordBatch` over one coordinate index, with per-column governed standing."""

    index: CoordinateIndex
    batch: pa.RecordBatch
    standings: Mapping[str, ColumnStanding]
    #: The physical snapshot/realization this block was produced by. Provenance, never identity.
    realization: str = "in-memory"
    provenance: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.batch.num_rows != len(self.index):
            raise KernelRefusal(
                "block-length-mismatch", str(self.index),
                f"the batch has {self.batch.num_rows} rows and the coordinate index has "
                f"{len(self.index)} points. A block's rows ARE the index's positions.")
        for ref in self.index.anchor.order:
            if ref not in self.batch.schema.names:
                raise KernelRefusal(
                    "coordinate-column-absent", str(self.index),
                    f"the batch carries no column {ref!r}. The coordinate columns are how the geometry "
                    f"is carried; without them a grouped reduction has nothing governed to group by.")
        for family_id, st in self.standings.items():
            if value_column_name(family_id) not in self.batch.schema.names:
                raise KernelRefusal("standing-without-column", family_id,
                                    f"a standing is carried for {family_id!r} and the batch has no "
                                    f"{value_column_name(family_id)!r} column.")
            if len(st) != self.batch.num_rows:
                raise KernelRefusal("standing-length-mismatch", family_id,
                                    f"{len(st)} standing entries for {self.batch.num_rows} rows.")

    # ── what the block can be asked ──────────────────────────────────────────────────────────
    @property
    def families(self) -> tuple[str, ...]:
        return tuple(sorted(self.standings))

    def column(self, family_id: str) -> pa.Array:
        return self.batch.column(value_column_name(family_id))

    def standing(self, family_id: str) -> ColumnStanding:
        try:
            return self.standings[family_id]
        except KeyError:
            raise KernelRefusal(
                "no-standing-for-column", family_id,
                f"this block carries no governed standing for {family_id!r}. **A VALUE COLUMN WITHOUT A "
                f"STANDING IS NOT USABLE**: its nulls would have to be interpreted, and Arrow "
                f"nullability carries no ToD standing.") from None

    def anchor_instance(self, family_id: str) -> AnchorInstance:
        """`(M, U, A, I)` for one column. **Per column**, because the instance is per column."""
        return AnchorInstance(index=self.index, instance=self.standing(family_id).instance)

    def contributing(self, family_id: str, shape: str = VALUE_BEARING) -> pa.BooleanArray:
        """The governed contribution mask for a reduction of `shape`. **Never `Array.is_valid()`.**"""
        return self.standing(family_id).contributing_for(shape)

    def compatibility_of(self, a: str, b: str) -> Compatibility:
        """**Co-location confers nothing, and this is where that is said out loud.** Two columns of this
        very batch, at identical positions, may be jointly unusable."""
        return self.standing(a).instance.compatible_with(self.standing(b).instance)

    def instance(self, family_id: str) -> AnalyticalInstance:
        return self.standing(family_id).instance

    def coordinate_columns(self) -> dict[str, pa.Array]:
        return {ref: self.batch.column(ref) for ref in self.index.anchor.order}

    def with_column(self, family_id: str, values: pa.Array,
                    standing: ColumnStanding) -> "GovernedBlock":
        """Co-locate another family column. **Adds carriage, not compatibility.**"""
        batch = pa.RecordBatch.from_arrays(
            list(self.batch.columns) + [values],
            names=list(self.batch.schema.names) + [value_column_name(family_id)])
        return GovernedBlock(index=self.index, batch=batch,
                             standings={**self.standings, family_id: standing},
                             realization=self.realization, provenance=self.provenance)

    # ── construction ─────────────────────────────────────────────────────────────────────────
    @staticmethod
    def of(index: CoordinateIndex, columns: Mapping[str, pa.Array],
           standings: Mapping[str, ColumnStanding], *, realization: str = "in-memory",
           provenance: tuple = ()) -> "GovernedBlock":
        arrays = list(index.columns().values())
        names = list(index.anchor.order)
        for family_id, values in columns.items():
            arrays.append(values if isinstance(values, pa.Array) else pa.array(values))
            names.append(value_column_name(family_id))
        batch = pa.RecordBatch.from_arrays([pa.array(a) if not isinstance(a, pa.Array) else a
                                            for a in arrays], names=names)
        return GovernedBlock(index=index, batch=batch, standings=dict(standings),
                             realization=realization, provenance=provenance)

    # ── reporting ────────────────────────────────────────────────────────────────────────────
    def render(self, *, families: Optional[tuple] = None) -> str:
        wanted = families or self.families
        head = list(self.index.anchor.order)
        for f in wanted:
            head += [f, f"{f}·part", f"{f}·supp"]
        rows = []
        for i in range(self.batch.num_rows):
            row = [str(self.batch.column(r)[i].as_py()) for r in self.index.anchor.order]
            for f in wanted:
                row.append(_display(self.column(f)[i].as_py()))
                st = self.standing(f)
                row.append("·" if st.participation[i].as_py() else "—")
                row.append("·" if st.support[i].as_py() else "—")
            rows.append(row)
        widths = [max(len(h), *(len(r[i]) for r in rows)) if rows else len(h)
                  for i, h in enumerate(head)]
        out = ["  ".join(h.ljust(w) for h, w in zip(head, widths)),
               "  ".join("─" * w for w in widths)]
        out += ["  ".join(v.ljust(w) for v, w in zip(r, widths)) for r in rows]
        return "\n".join(out)

    def __str__(self) -> str:
        return (f"GovernedBlock({self.index}, {len(self.families)} family column(s), "
                f"realization={self.realization!r})")


def _display(value: Any) -> str:
    """**A structured payload has no display form.** Same rule the Frame-QL frame applies, for the same
    reason: a sketch's `str()` carries an `Estimate:` line, and printing it would show a cardinality
    obtained through the family path rather than through the finalization that is the only lawful route."""
    if value is None:
        return "∅"
    if isinstance(value, (bytes, bytearray, memoryview)):
        return f"⟨sketch:{len(bytes(value))}B⟩"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


__all__ = ["GovernedBlock", "VALUE_SUFFIX", "value_column_name"]

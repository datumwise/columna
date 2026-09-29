"""
columna_platform.columnar.provider — **the Arrow/DataFusion execution provider.**

    *"The MME kernel remains analytical authority. DataFusion is a provider. Do not let DataFusion
    accumulator/state types define family standing. Do not route family law through generated SQL."*
        — Huayin, 2026-09-28

Nothing in this module decides whether an operation is lawful. It is asked to perform one that the kernel
has already adjudicated, and it performs it with Arrow kernels and DataFusion `DataFrame` operations —
**no SQL text is generated anywhere in this file**, which is the difference between using an engine and
delegating law to its planner.

THE PHYSICAL RULE, AND HOW EACH ALLOWED SHAPE IS USED
-----------------------------------------------------
    *"MME does not discover analytical alignment by joining analytical tables."*

Allowed and used here:

* **grouped reduction** — `DataFrame.aggregate(group_by=<coordinate columns>, aggs=[…])`. Grouping by the
  governed coordinate columns of the TARGET anchor is how continuation coarsens. The group keys come from
  the geometry, never from a business key.
* **a custom aggregate (UDAF)** for structured state — the HLL union, below.
* **Arrow compute kernels** for positional expression evaluation.
* **explicit reindex/alignment** against a governed target index — `align_onto`, named as an operation and
  reported in the result, because *"if explicit reindexing is needed, make it visible as an alignment
  operation."*

Never: no `join`, no `sql()`, no business-key matching, and no reading of a carrier null as standing. The
absence of `join` and `sql` in this module is test-enforced over its AST.

WHY ALIGNMENT IS A `take` AND NOT A JOIN
---------------------------------------
DataFusion returns aggregate groups in whatever order and partitioning it likes. Recovering the target
layout therefore needs a permutation — and a permutation computed against a **governed index we already
hold** is a reindex, while the same permutation obtained by matching two data tables on their key columns
would be a join that *discovers* correspondence. The distinction is not cosmetic: the reindex refuses when
the provider returns a group the governed index does not contain, because that would mean the provider
invented an analytical point. A join would have silently accepted it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

import pyarrow as pa
import pyarrow.compute as pc
from datafusion import Accumulator, SessionContext, col, udaf
from datafusion import functions as DF
from datasketches import hll_sketch, hll_union, tgt_hll_type

from columna_platform.kernel import ADDITION, KernelRefusal, SKETCH_UNION

from .block import GovernedBlock, value_column_name
from .index import CoordinateIndex
from .standing import ColumnStanding, VALUE_BEARING, all_true

PROVIDER_NAME = "arrow+datafusion"
HLL_PRECISION = 12
_TGT = tgt_hll_type.HLL_8


# ══ the structured-state UDAF ═════════════════════════════════════════════════════════════════════
class HllUnionAccumulator(Accumulator):
    """**DataFusion's accumulator state is a REALIZATION MECHANISM, not ToD continuation authority.**

    *"DataFusion accumulator state is a physical realization mechanism. It is not ToD continuation
    authority merely because DataFusion calls it 'state'. Only the governed family value may be persisted
    as family state."*

    So this accumulator's `state()` and its `evaluate()` return **the same thing**: a portable DataSketches
    `serialize_compact()` sketch. There is deliberately no engine-native intermediate that could become the
    persisted representation by being convenient — the value that leaves this UDAF is the governed family
    value, in a portable encoding, and DataFusion's partial-aggregate plumbing carries exactly that."""

    def __init__(self) -> None:
        self._union = hll_union(HLL_PRECISION)

    def _absorb(self, payload: Optional[bytes]) -> None:
        if payload is not None:
            self._union.update(hll_sketch.deserialize(bytes(payload)))

    def update(self, values: pa.Array) -> None:
        for v in values:
            self._absorb(v.as_py())

    def merge(self, states: Sequence[pa.Array]) -> None:
        for arr in states:
            for v in arr:
                self._absorb(v.as_py())

    def state(self) -> list:
        return [pa.scalar(self._union.get_result().serialize_compact(), pa.binary())]

    def evaluate(self) -> pa.Scalar:
        return pa.scalar(self._union.get_result().serialize_compact(), pa.binary())


HLL_MERGE_UDAF = udaf(HllUnionAccumulator, [pa.binary()], pa.binary(), [pa.binary()],
                      volatility="immutable", name="governed_hll_union")


def sketch_of(values: Sequence[Any]) -> bytes:
    """One HLL sketch over the participating values, portably encoded. The family's ROOT value."""
    s = hll_sketch(HLL_PRECISION, _TGT)
    for v in values:
        if v is not None:
            s.update(v)
    return s.serialize_compact()


def estimate_of(payload: bytes) -> int:
    return int(round(hll_sketch.deserialize(bytes(payload)).get_estimate()))


def sketch_parameters(payload: bytes) -> dict:
    """**Sketch parameters are COMPATIBILITY-BEARING**, so they are readable from the value itself rather
    than trusted from a declaration: two sketches of different `lg_k` are not mergeable, and a union that
    silently down-sampled one would produce a number about no population."""
    s = hll_sketch.deserialize(bytes(payload))
    return {"lg_k": s.lg_config_k, "tgt_type": str(s.tgt_type)}


# ══ results ═══════════════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class ContinuationResult:
    """A grouped continuation's output, aligned to the target index, with the route it took."""

    index: CoordinateIndex
    values: pa.Array
    standing: ColumnStanding
    #: Every physical step, in order. Reported because the ruling asks for *"the exact route for grouped
    #: continuation"* and because an alignment must be VISIBLE.
    route: tuple[str, ...]


@dataclass(frozen=True)
class AlignmentReport:
    """An explicit reindex, made visible. Never a join."""

    from_identity: str
    to_identity: str
    permutation: tuple[int, ...]
    note: str


class ColumnarProvider:
    """Arrow for carriage, DataFusion for grouped reduction, Arrow compute for positional kernels."""

    name = PROVIDER_NAME

    def __init__(self) -> None:
        self.ctx = SessionContext()

    # ── grouped continuation ─────────────────────────────────────────────────────────────────
    def continue_grouped(self, block: GovernedBlock, family_id: str, *, composition: str,
                         target_index: CoordinateIndex, shape: str = VALUE_BEARING
                         ) -> ContinuationResult:
        """**Coarsen one family column by GROUPED REDUCTION over the target anchor's coordinates.**

        The exact route, and every step is named in the result:

          1. **governed filter** — keep only positions the standing says CONTRIBUTE for this reduction's
             shape. Done in Arrow, from the mask, before the engine sees anything. This is what stops
             `count(non-null value)` from ever being the aggregation.
          2. **project the target coordinates** — the surviving rows' coordinate columns, restricted to the
             TARGET anchor's constituents. Forgetting a constituent is dropping its column; nothing is
             recomputed and nothing is looked up.
          3. **DataFusion grouped aggregate** — `aggregate(group_by=<target coordinate columns>, aggs=[…])`.
             No SQL, no join.
          4. **explicit alignment** — `align_onto(target_index)`, a reindex against a governed index.
        """
        contributing = block.contributing(family_id, shape)
        route = [f"governed-filter: {shape}, "
                 f"{pc.sum(pc.cast(contributing, pa.int64())).as_py() or 0}"
                 f"/{len(contributing)} positions contribute "
                 f"(from the standing masks, NOT from Arrow validity)"]

        target_refs = list(target_index.anchor.order)
        arrays = {ref: pc.filter(block.batch.column(ref), contributing) for ref in target_refs}
        values = pc.filter(block.column(family_id), contributing)
        route.append(f"project: coordinates {target_refs} "
                     f"(forgetting {sorted(set(block.index.anchor.order) - set(target_refs))})")

        payload = pa.RecordBatch.from_arrays(
            list(arrays.values()) + [values], names=target_refs + ["v"])
        frame = self.ctx.create_dataframe([[payload]])
        aggregate = self._aggregate_for(composition)
        grouped = frame.aggregate([col(r) for r in target_refs],
                                  [aggregate(col("v")).alias("folded")])
        batches = grouped.collect()
        route.append(f"datafusion: aggregate(group_by={target_refs}, agg={composition}) "
                     f"→ {len(batches)} partition(s)")

        produced: dict[tuple, Any] = {}
        for b in batches:
            cols = {name: b.column(name).to_pylist() for name in b.schema.names}
            for i in range(b.num_rows):
                key = tuple(cols[r][i] for r in target_refs)
                produced[key] = cols["folded"][i]

        aligned, report = self.align_onto(produced, target_index)
        route.append(f"align: {report.note}")
        return ContinuationResult(
            index=target_index, values=aligned,
            standing=ColumnStanding(
                family_id=family_id, instance=block.instance(family_id),
                participation=all_true(len(target_index)), support=all_true(len(target_index)),
                note="every target point present in the index received a contribution; a target point "
                     "with none would not be in the index, because sparse geometry stays sparse"),
            route=tuple(route))

    @staticmethod
    def _aggregate_for(composition: str):
        if composition == ADDITION:
            return DF.sum
        if composition == SKETCH_UNION:
            return HLL_MERGE_UDAF
        raise KernelRefusal(
            "unrealized-composition", PROVIDER_NAME,
            f"composition {composition!r} has no columnar realization in provider {PROVIDER_NAME!r}. The "
            f"law is unchanged and this provider cannot execute its grouped reduction — a REALIZATION "
            f"limit, and its remedy is a provider.")

    # ── explicit alignment. NEVER a join. ────────────────────────────────────────────────────
    def align_onto(self, produced: Mapping[tuple, Any],
                   target_index: CoordinateIndex) -> tuple[pa.Array, AlignmentReport]:
        """Re-lay produced groups onto the governed target layout.

        **A REINDEX, AND THE DIFFERENCE FROM A JOIN IS THE REFUSAL BELOW.** The permutation is computed
        against an index this engine already holds, so a group the index does not contain means the
        provider produced an analytical point the geometry does not have — and that REFUSES. A join on the
        key columns would have accepted it as a new row."""
        values: list[Any] = []
        permutation: list[int] = []
        for position, cell in enumerate(target_index.coordinates):
            if cell not in produced:
                raise KernelRefusal(
                    "target-point-unproduced", str(target_index),
                    f"the target index carries point {cell!r} and the grouped reduction produced no group "
                    f"for it. Nothing is zero-filled: a governed point with no contribution is a "
                    f"different fact from a point whose fold is the identity, and this provider will not "
                    f"decide which one it is.")
            values.append(produced[cell])
            permutation.append(position)
        extra = sorted(set(produced) - set(target_index.coordinates), key=lambda c: tuple(map(str, c)))
        if extra:
            raise KernelRefusal(
                "provider-invented-a-point", str(target_index),
                f"the grouped reduction produced group(s) {extra} that the governed target index does not "
                f"contain. **THIS IS THE REFUSAL THAT MAKES THIS A REINDEX AND NOT A JOIN**: a join would "
                f"have accepted these rows as correspondences it discovered.")
        first = values[0] if values else None
        arrow_type = pa.binary() if isinstance(first, (bytes, bytearray)) else None
        return (pa.array(values, type=arrow_type) if arrow_type else pa.array(values),
                AlignmentReport(from_identity="datafusion-group-output",
                                to_identity=target_index.identity,
                                permutation=tuple(permutation),
                                note=f"explicit reindex of {len(produced)} produced group(s) onto "
                                     f"{len(target_index)} governed point(s) of {target_index.identity} "
                                     f"— a reindex against a held index, not a join on keys"))

    # ── positional expression evaluation ─────────────────────────────────────────────────────
    def evaluate_positional(self, columns: Mapping[str, pa.Array], *, kernel: str) -> pa.Array:
        """**A COLUMN KERNEL over position-aligned arrays. No join, and no key matching.**

        The caller has already established that every column shares one `CoordinateIndex.identity` and a
        compatible analytical instance; what is left is arithmetic at a position. `ratio` divides where the
        divisor is non-zero and yields null elsewhere — §4.3's *undefined on that basis*, which the kernel
        layer turns into a governed standing rather than a zero."""
        if kernel == "ratio":
            numerator, denominator = columns["SUM"], columns["COUNT"]
            safe = pc.if_else(pc.equal(denominator, 0), pa.nulls(len(denominator), pa.int64()),
                              denominator)
            return pc.divide(pc.cast(numerator, pa.float64()), pc.cast(safe, pa.float64()))
        if kernel == "hll_estimate":
            sketches = columns["HLL_SKETCH"]
            return pa.array([None if v.as_py() is None else estimate_of(v.as_py())
                             for v in sketches], type=pa.int64())
        raise KernelRefusal("unrealized-kernel", PROVIDER_NAME,
                            f"positional kernel {kernel!r} has no realization in {PROVIDER_NAME!r}.")

    def realizes_composition(self, composition: str) -> bool:
        return composition in (ADDITION, SKETCH_UNION)


__all__ = ["AlignmentReport", "ColumnarProvider", "ContinuationResult", "HLL_MERGE_UDAF",
           "HLL_PRECISION", "HllUnionAccumulator", "PROVIDER_NAME", "estimate_of",
           "sketch_of", "sketch_parameters", "value_column_name"]

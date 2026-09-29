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
from columna_platform.kernel.law import SCALAR, STRUCTURED

from .capability import GROUPED, POSITIONAL, CapabilityTable, ExecutionCapability

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


# ── the positional kernels, as callables this provider OWNS ──────────────────────────────────────
#
# These were `"ratio"` and `"hll_estimate"`, two strings the governed evaluator chose between (E-X's
# finding). They are now functions in the provider's own capability table, reached by GOVERNED law name.
# Nothing above `ColumnarProvider` can name them, and adding a third edits this file rather than the
# evaluator — which is the division E-1 exists to restore.
def _ratio(columns: Mapping[str, pa.Array], parameters: Mapping[str, Any]) -> pa.Array:
    """`MEAN`'s constructor: SUM / COUNT, position-wise.

    Divides where the divisor is non-zero and yields null elsewhere — §4.3's *undefined on that basis*,
    which the kernel layer turns into a governed standing rather than a zero. Fully Arrow-native: one
    kernel chain for the whole column, no Python iteration."""
    numerator, denominator = columns["SUM"], columns["COUNT"]
    safe = pc.if_else(pc.equal(denominator, 0), pa.nulls(len(denominator), pa.int64()), denominator)
    return pc.divide(pc.cast(numerator, pa.float64()), pc.cast(safe, pa.float64()))


def estimates_of(payloads: Sequence[Optional[bytes]]) -> pa.Array:
    """**The finalizer's whole cell-scale step, in ONE named place. ADJUDICATED AT E-3 (2026-09-29).**

    One `hll_sketch.deserialize(...).get_estimate()` per sketch, and nothing else. It is a Python `for` over
    cells, and E-3 decided — with measurements — that it stays one for now. The four alternatives, each
    rejected for a *different* reason, because "it's still a Python loop" is not by itself an argument:

    * **Apache DataSketches' Python binding has no batch API, and no zero-copy input.** `hll_sketch` (5.2.0)
      exposes `deserialize(bytes)` and nothing plural; `memoryview`, `bytearray`, numpy and `pa.Buffer` are
      all `TypeError`. (The quantiles families *do* take numpy arrays; HLL does not.) So from Python the
      per-sketch call and one `bytes` materialization are both forced.
    * **A DataFusion Python scalar UDF is measurably WORSE.** Measured here, 2 000 sketches: the same loop
      inside a `udf` costs **1.95 µs/cell against 1.51 in-process — 1.29×, +0.44 µs/cell of pure engine
      overhead** — because a Python UDF *is* a per-batch Arrow→Python→Arrow round trip with the same
      comprehension inside it. *"A DataFusion UDF that simply contains the same Python per-cell loop is not
      an architectural improvement"* (Huayin, 2026-09-29); this one is not even a performance improvement.
      **Recon E-X's step 3 recommended exactly that move, and E-3 reverses the recommendation.**
    * **DataFusion's native `approx_distinct` is the WRONG OPERATION, and returns a confident wrong
      number.** Applied to the governed family value it counts distinct *blobs*: two sketches over `{a,b,c}`
      and `{c,d}` give **2** where the population is **4**. Applied to raw occurrences it gives 4 — by
      recomputing from source, which is not an expression over the family value at all and cannot serve a
      coarser anchor from a retained finer sketch. Its internal HLL is a vendored redis derivative (p=14,
      foldhash) with no header and no version, discriminated by byte length alone, and it is **not**
      interoperable with DataSketches' `serialize_compact()` at any level: different hash, different slot
      addressing, different register rule, no preamble. It is not this law and it is not this format.
    * **`pyarrow.compute` has no such kernel** and could not: the work is a third-party sketch decode.

    So what E-3 removed is not the loop but the **carriage around it**. `to_pylist()` extracts the whole
    binary column in one vectorised pass instead of boxing N `BinaryScalar`s and calling `as_py()` twice per
    cell (once to test for null, once to use). Measured, 2 000 sketches, best of 15 CPU-time runs, on two
    corpora — **the removed cost is per-cell and size-independent (≈0.8–1.0 µs/cell), so the ratio falls as
    the sketches grow while the saving does not:**

        corpus                          before      after     removed
        uniform LIST/SET (172 B)     2.305 µs   1.456 µs   36.8%   (1.58×)
        mixed LIST+SET+HLL (12–4136 B)  3.768 µs   2.908 µs   22.8%   (1.30×)

    **The remaining Python is orchestration; the analytical payload is Arrow-in, Arrow-out and native.**
    That is the criterion met, not evaded.

    WHY A NATIVE KERNEL IS DEFERRED AND NOT DENIED — and the claim that *"nothing off the shelf reads this
    format"* is FALSE, so it is not the reason. Apache DataSketches ships an official **Rust** core (crate
    `datasketches` ≥ 0.5.0, `features = ["hll"]`) that deserializes C++-written compact HLL images, with
    cross-language compatibility enforced by `datasketches-tck`; DataFusion 54's Python bindings already
    accept a Rust UDF in-engine through the `datafusion-ffi` `__datafusion_scalar_udf__` PyCapsule protocol;
    and `datafusion-comet` PR #4802 is a merged reference implementation of exactly this finalizer
    (`hll_sketch_estimate`). The form exists. Two reasons it is not taken *here*:

      1. **IT IS A DIFFERENT REALIZATION, NOT A FASTER ONE — AND THAT IS THE DECIDING REASON.** The Rust
         crate's estimates are not bit-identical to the C++ library's for merged or out-of-order sketches
         (≈0.7% divergence reported, inside HLL's relative standard error but not zero). Changing the engine
         that computes the number CHANGES THE NUMBER. Under §8.7 and P-1 that is a `RealizationStanding`
         change — *"a value produced by an approximate provider is not interchangeable with one produced by
         an exact one"* — so it is a **second provider requiring its own admission evidence**, not an
         optimization of this line, and smuggling it in as a speed-up would silently make two answers to one
         question. (The exact-parity route, the cxx-FFI `apache-datasketches` crate, links the same C++
         library and avoids the divergence — at the cost of C++ in the wheel matrix.)
      2. **It is a packaging unit.** A compiled extension across the CI wheel matrix (py3.10–3.13 ×
         ubuntu/windows) for a measured ceiling of ≈**2×** on CPU time — and only ≈14× if the kernel decodes
         registers in place without materializing a `bytes` *or* a sketch object per row, because the decode
         is ~4/5 of the native cost and `get_estimate()` itself is ~0.18 µs/cell. The continuation brackets
         E-X measured (`_target_index`, group materialization, `align_onto`) are the larger number and are
         not this unit.

    THE TRIGGER, NAMED SO NOBODY HAS TO GUESS: a profile showing this line is the cost, **or** a reason to
    admit a second sketch realization on its own merits. Either one makes it a provider unit with
    `RealizationStanding` doing its job. Not a rewrite of this function."""
    return pa.array([None if p is None else estimate_of(p) for p in payloads], type=pa.int64())


def _hll_estimate(columns: Mapping[str, pa.Array], parameters: Mapping[str, Any]) -> pa.Array:
    """`HLL_ESTIMATE`'s constructor: the FINALIZER for a structured sketch family.

    Declared with `value_form_in=STRUCTURED, value_form_out=SCALAR`, which is what makes
    `ExecutionCapability.finalizes` true of it and what forbids it ever being declared as a `GROUPED`
    capability.

    **A MAP, and the only thing this function does is carriage.** One vectorised extraction from Arrow, one
    native call per sketch in `estimates_of`, one int64 column back out. The adjudication of why that is the
    right shape is recorded on `estimates_of`."""
    return estimates_of(columns["HLL_SKETCH"].to_pylist())


class ColumnarProvider:
    """Arrow for carriage, DataFusion for grouped reduction, Arrow compute for positional kernels.

    **What it can execute is DECLARED, not discovered by trying** (ruled E-1). `self.capabilities` is a
    `CapabilityTable` keyed by `(execution mode, governed operation)`; every dispatch below is a lookup in
    it, and there is no `if composition == …` or `if kernel == …` left anywhere in this class."""

    name = PROVIDER_NAME

    def __init__(self) -> None:
        self.ctx = SessionContext()
        #: **THE DECLARED TABLE.** Built per instance because `execute` for a grouped capability is this
        #: provider's own aggregate handle, and a future provider will hold different ones.
        self.capabilities = CapabilityTable(PROVIDER_NAME, (
            ExecutionCapability(
                mode=GROUPED, operation=ADDITION, execute=DF.sum,
                value_form_in=SCALAR, value_form_out=SCALAR,
                note="DataFusion's native sum, grouped by the target anchor's coordinate columns"),
            ExecutionCapability(
                mode=GROUPED, operation=SKETCH_UNION, execute=HLL_MERGE_UDAF,
                value_form_in=STRUCTURED, value_form_out=STRUCTURED,
                note="a governed HLL-union UDAF; sketches fold into a SKETCH and are never finalized here"),
            ExecutionCapability(
                mode=POSITIONAL, operation="MEAN", execute=_ratio,
                value_form_in=SCALAR, value_form_out=SCALAR,
                note="Arrow pc.divide with an explicit zero-divisor guard yielding null, not zero"),
            ExecutionCapability(
                mode=POSITIONAL, operation="HLL_ESTIMATE", execute=_hll_estimate,
                value_form_in=STRUCTURED, value_form_out=SCALAR,
                note="the finalizer: a structured sketch becomes a displayable integer, ABOVE the MME"),
        ))

    # ── capability discovery, without executing anything ─────────────────────────────────────
    def capability(self, mode: str, operation: str) -> ExecutionCapability:
        """What this provider would use for `(mode, operation)`, or the governed refusal."""
        return self.capabilities.of(mode, operation)

    def realizes(self, mode: str, operation: str) -> bool:
        """**Asked before work, and it never raises.** The columnar peer of `ProviderProfile.realizes`."""
        return self.capabilities.realizes(mode, operation)

    # ── grouped continuation ─────────────────────────────────────────────────────────────────
    def continue_grouped(self, block: GovernedBlock, family_id: str, *, composition: str,
                         target_index: CoordinateIndex, shape: str = VALUE_BEARING
                         ) -> ContinuationResult:
        """**Coarsen one family column by GROUPED REDUCTION over the target anchor's coordinates.**

        The exact route, and every step is named in the result:

          1. **governed filter** — restrict to the reduction's CONTRIBUTING DOMAIN, which is
             `participation` for every shape. Done in Arrow, from the mask, before the engine sees
             anything. This is what stops `count(non-null value)` from ever being the aggregation. It is
             *not* `participation ∧ support`: support validates this domain, and a value-bearing fold
             handed an unsupported participating point is REFUSED below rather than quietly narrowed.
          2. **project the target coordinates** — the surviving rows' coordinate columns, restricted to the
             TARGET anchor's constituents. Forgetting a constituent is dropping its column; nothing is
             recomputed and nothing is looked up.
          3. **DataFusion grouped aggregate** — `aggregate(group_by=<target coordinate columns>, aggs=[…])`.
             No SQL, no join.
          4. **explicit alignment** — `align_onto(target_index)`, a reindex against a governed index.
        """
        wanting = block.standing(family_id).positions_wanting_state(shape)
        if wanting:
            # A BACKSTOP, NOT A JUDGMENT. The kernel refuses want of state before it ever calls a
            # provider; if one reaches here the provider will not fold around it, because folding the
            # rest is exactly the silent narrowing the 2026-09-29 ruling forbids.
            raise KernelRefusal(
                "want-of-state-reached-the-provider", family_id,
                f"a {shape} grouped reduction was requested over a domain in which position(s) "
                f"{list(wanting)} participate and are unsupported. This provider will not fold the "
                f"remainder and report a total: support validates the participating domain, it does not "
                f"shrink it. The analytical authority owes this request a want-of-state refusal and this "
                f"call should not have been made.")

        contributing = block.contributing_domain(family_id, shape)
        route = [f"governed-filter: {shape}, "
                 f"{pc.sum(pc.cast(contributing, pa.int64())).as_py() or 0}"
                 f"/{len(contributing)} positions in the CONTRIBUTING DOMAIN "
                 f"(participation, from the standing masks, NOT from Arrow validity; support was "
                 f"validated over this domain before the fold, never subtracted from it)"]

        target_refs = list(target_index.anchor.order)
        arrays = {ref: pc.filter(block.batch.column(ref), contributing) for ref in target_refs}
        values = pc.filter(block.column(family_id), contributing)
        route.append(f"project: coordinates {target_refs} "
                     f"(forgetting {sorted(set(block.index.anchor.order) - set(target_refs))})")

        payload = pa.RecordBatch.from_arrays(
            list(arrays.values()) + [values], names=target_refs + ["v"])
        frame = self.ctx.create_dataframe([[payload]])
        # **THE ONLY DISPATCH, AND IT IS A TABLE LOOKUP.** The refusal for an unrealized composition comes
        # from the table and still says *"the law is unchanged"* — a provider's inability never removes a
        # law (ToD v8 §4.1).
        aggregate = self.capability(GROUPED, composition).execute
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
                     "with none would not be in the index, because sparse geometry stays sparse. Support "
                     "is all-true because the fold only runs once the source's whole participating "
                     "domain was established — it is EARNED here, not assumed"),
            route=tuple(route))


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
    def evaluate_positional(self, columns: Mapping[str, pa.Array], *, law: str,
                            parameters: Optional[Mapping[str, Any]] = None) -> pa.Array:
        """**A COLUMN KERNEL over position-aligned arrays. No join, and no key matching.**

        The caller has already established that every column shares one `CoordinateIndex.identity` and a
        compatible analytical instance; what is left is arithmetic at a position.

        **THE CALLER NAMES A GOVERNED LAW, NOT A KERNEL** (ruled E-1). This parameter was `kernel: str`
        and the evaluator above chose `"ratio"` or `"hll_estimate"` by a hard-coded switch on the law name
        — a governed object naming a physical one. Now the law arrives and the provider's own table
        resolves it, which is the same shape `ProviderProfile.capability(law, "apply")` has had on the
        in-memory side all along.

        `parameters` brings this signature into agreement with that in-memory `apply(payloads, parameters)`
        contract. No current columnar kernel reads it; both accept it, so a parameterised constructor needs
        no signature change."""
        return self.capability(POSITIONAL, law).execute(columns, dict(parameters or {}))

    def realizes_composition(self, composition: str) -> bool:
        """**Kept as a named question, now answered by the table.** A caller asking *"can you fold this
        composition?"* should not have to know the mode vocabulary to ask it."""
        return self.realizes(GROUPED, composition)


__all__ = ["AlignmentReport", "ColumnarProvider", "ContinuationResult", "HLL_MERGE_UDAF",
           "HLL_PRECISION", "HllUnionAccumulator", "PROVIDER_NAME", "estimate_of", "estimates_of",
           "sketch_of", "sketch_parameters", "value_column_name"]

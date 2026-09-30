"""columna_platform.kernel.hll_carrier — **provider realization machinery, BELOW the analytical
boundary.**

NOTHING IN THIS MODULE IS GOVERNED LAW
--------------------------------------
Every name here is a fact about Apache DataSketches, not about analytics. `LIST`/`SET`/`HLL` modes,
promotion thresholds, `HLL_4`/`HLL_6`/`HLL_8`, compact versus updatable encoding, the HIP accumulator
and the serialized byte layout are **realization choices a provider is free to make**. They were
briefly proposed as governed state (`specs/governed_hll_state_v0_1.md` §1) and that was WITHDRAWN:
it promoted a library limitation into analytical constitution.

    Huayin, 2026-09-30: *"Physical representation is free. Analytical result is not."*

WHAT THIS MODULE EXISTS TO ENFORCE
----------------------------------
One invariant, and it is the whole unit:

    same governed HLL state  →  same governed final result,
    regardless of sparse or dense carrier, staged or direct construction,
    HLL_4/6/8, compact or updatable, and regardless of construction history.

`hll_sketch.get_estimate()` **does not have that property.** It reads `hipAccum` whenever the
out-of-order flag is clear, and HIP accumulates over the update *stream*. Measured, on one governed
input of 20 000 values by two lawful routes: `19 832` direct, `20 100` staged — a 1.34% spread on a
question with one answer.

THE ROUTE, AND WHY IT IS NOT A SECOND ESTIMATOR
-----------------------------------------------
    physical carrier → recover the register vector → hand it back as a register-form carrier
                     → force the history-dependent estimator state out → THE LIBRARY estimates

The bias-corrected estimator is never reimplemented; DataSketches computes every number this module
returns. Writing our own was measured and rejected — the library's register estimator is **not**
linear counting (0.0122% apart at n = 1, 1.39% at n = 6000), so a "simple closed form for the sparse
case" would have been a second estimator in disguise, with the §8.7 `RealizationStanding` divergence
problem attached.

**THE FORCING STEP IS LOAD-BEARING AND DOES TWO JOBS.** `deserialize` does not recompute the cached
estimator accumulators from the registers it is handed — it trusts the preamble. Splice register bytes
into a template and estimate directly and you get *the template's* cardinality, every time, for every
input (measured: 24 339.9 for inputs from 1 to 200 000). The union both discards HIP and rebuilds
`kxq0`/`kxq1`/`curMin` from the registers. One union update is NOT enough: a single update lets the
gadget adopt the incoming sketch whole, history included. Two are.

THE BINARY-LAYOUT DEPENDENCY IS HERE AND ONLY HERE
--------------------------------------------------
Confined to `_registers_of` and `_register_form`, conformance-guarded by
`tests/test_b4a_ib_hll_representation_independence.py`, and it is the smallest surface that works:
one byte read (`preInts`, which says which mode an image is in), the coupon field layout, and the
register block offset. The template preamble itself is obtained wholly through the public API.

**The desirable upstream fix is a public register accessor or promotion API on `hll_sketch`.** With
either, `_register_form` collapses to one library call and this module keeps only its docstring. This
unit is deliberately not blocked on obtaining it.
"""
from __future__ import annotations

from typing import Any

from datasketches import hll_sketch, hll_union, tgt_hll_type

from .geometry import KernelRefusal

#: The register-form target. HLL_8 stores one whole register per byte, so the register block is
#: readable without unpacking; HLL_4 and HLL_6 are equally lawful carriers and are converted on the
#: way through. `tgt_type` is encoding, proved including the HLL_4 auxiliary-exception path.
REGISTER_FORM = tgt_hll_type.HLL_8

_PREAMBLE_BYTES = 40      # an HLL-mode image's preamble: 4 * preInts, and preInts is 10
_HLL_MODE_PREINTS = 10    # LIST is 2, SET is 3, HLL is 10 — the one byte this module reads to branch
_COUPON_VALUE_SHIFT = 26  # a coupon is (value << 26) | address; slot = address & (2^lg_k - 1)
_COUPON_ITEM = "I"        # coupons are uint32, read through a zero-copy memoryview cast

#: One history-free preamble per `lg_k`, built through the public API and immutable once built.
_PREAMBLES: dict[int, bytes] = {}


def _history_free_preamble(lg_k: int) -> bytes:
    """An HLL-mode preamble whose estimator state carries no usable history.

    Built by unioning two register-form sketches, which is the library's own way of producing a
    carrier it will not read HIP from. No byte of it is authored here."""
    cached = _PREAMBLES.get(lg_k)
    if cached is not None:
        return cached
    a = hll_sketch(lg_k, REGISTER_FORM, True)      # start_max_size: register form from the first update
    b = hll_sketch(lg_k, REGISTER_FORM, True)
    a.update("columna/hll_carrier/a")
    b.update("columna/hll_carrier/b")
    u = hll_union(lg_k)
    u.update(a)
    u.update(b)
    preamble = u.get_result(REGISTER_FORM).serialize_updatable()[:_PREAMBLE_BYTES]
    _PREAMBLES[lg_k] = preamble
    return preamble


def _register_form(sketch) -> Any:
    """`sketch`'s register state, as a carrier the library will estimate from.

    A sketch already in HLL mode is returned as it is — the forcing step converts and recomputes.
    A sparse carrier is decoded and rebuilt, because the library offers no way to promote one."""
    image = sketch.serialize_compact()
    if image[0] == _HLL_MODE_PREINTS:
        return sketch
    lg_k = sketch.lg_config_k
    slots = 1 << lg_k
    mask = slots - 1
    offset = 4 * image[0]
    registers = bytearray(slots)
    # A zero-copy uint32 view of the coupon block rather than a `struct.unpack_from` tuple: the decode
    # is the only per-cell Python iteration in this module and there is no batch API to escape it to.
    for coupon in memoryview(image)[offset:].cast(_COUPON_ITEM):
        slot, value = coupon & mask, coupon >> _COUPON_VALUE_SHIFT
        if value > registers[slot]:
            registers[slot] = value
    return hll_sketch.deserialize(_history_free_preamble(lg_k) + bytes(registers))


def governed_estimate(sketch) -> float:
    """**The cardinality estimate of the governed HLL state `sketch` carries.**

    A function of the register vector and nothing else. Two carriers of one governed state give one
    answer here, whatever their representation and however they were built."""
    carrier = _register_form(sketch)
    union = hll_union(carrier.lg_config_k)
    union.update(carrier)
    union.update(carrier)     # two, deliberately: see the module docstring
    return union.get_estimate()


def governed_distinct_count(sketch) -> int:
    """`governed_estimate`, as the integer `HLL_ESTIMATE` publishes."""
    return int(round(governed_estimate(sketch)))


def merge_type_of(sketch) -> int:
    """The compatibility-bearing part of a carrier's governed type, read from the value itself."""
    return sketch.lg_config_k


def require_mergeable(a, b, subject: str = "HLL_SKETCH") -> int:
    """**FAILS CLOSED on a type mismatch, and returns the `lg_k` a union may be taken at.**

    `hll_union` reduces a mismatched pair to the smaller `lg_k` without complaint, which produces a
    value about no population and reports nothing. Precision is compatibility-bearing, so the merge
    site is the place that must know it — and must not learn it from a module constant."""
    lg_a, lg_b = a.lg_config_k, b.lg_config_k
    if lg_a != lg_b:
        raise KernelRefusal(
            "incompatible-sketch-type", subject,
            f"cannot merge an HLL sketch of lg_k={lg_a} with one of lg_k={lg_b}. Precision is part of "
            f"this value's governed type: the two sketches index different register spaces, and a "
            f"union of them is a number about no population. The library would silently reduce to "
            f"lg_k={min(lg_a, lg_b)}; this refuses instead. Whether a lossy reduction is ever admitted "
            f"is a question for the law, not for the merge site.")
    return lg_a


def union_of(a, b):
    """The governed continuation: register join, at the operands' own type. **No module constant.**"""
    lg_k = require_mergeable(a, b)
    union = hll_union(lg_k)
    union.update(a)
    union.update(b)
    return union.get_result(REGISTER_FORM)


__all__ = ["REGISTER_FORM", "governed_distinct_count", "governed_estimate", "merge_type_of",
           "require_mergeable", "union_of"]

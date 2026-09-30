"""test_b4a_ib_hll_representation_independence.py — **B-4a″(i-b′): the leak battery.**

    Huayin, 2026-09-30: *"Physical representation is free. Analytical result is not."*

The governed HLL law says the finalized answer is a function of the family's retained state. Before
this unit, `HLL_ESTIMATE` was a function of the *carrier* and of the *construction route*: one governed
input of 20 000 values answered `19 832` built directly and `20 100` built in two stages, because
`hll_sketch.get_estimate()` reads the HIP accumulator whenever the out-of-order flag is clear and HIP
accumulates over the update stream.

These tests are the durable form of the `specs/evidence/b4a_i/` harness, which is where they came from
and where the design argument is recorded. They are organised as the obligations a provider accepts:

    R2  finalization does not consult construction history
    R3  a change of internal representation does not change the governed result

plus the state-level proofs the earlier unit established (delivery coherence, ACI + identity,
byte-inequality despite analytical equality, mixed-type refusal, finalization-is-not-continuation,
cross-provider fidelity) and the negative controls that say why any of this machinery exists.

**THE NEGATIVE CONTROLS ARE LOAD-BEARING.** Two of them pin mistakes that were actually made and
measured during this unit, and a future simplification that reintroduces either would pass every
positive test in this file.
"""
from __future__ import annotations

import struct

import pyarrow as pa
import pytest
from datasketches import hll_sketch, hll_union, tgt_hll_type

from columna_platform.columnar import provider as CP
from columna_platform.kernel import builtins as KB
from columna_platform.kernel.geometry import KernelRefusal
from columna_platform.kernel.hll_carrier import (
    REGISTER_FORM,
    _history_free_preamble,
    _register_form,
    governed_estimate,
    union_of,
)

LG_K = 12
SLOTS = 1 << LG_K
PREAMBLE = 40


# ── helpers: the representations one governed state can be carried in ────────────────────────────
def values(n, tag="v"):
    return [f"{tag}{i}" for i in range(n)]


def sparse_or_default(items, lg_k=LG_K, tgt=REGISTER_FORM):
    """The library's own default: coupon mode while small, register mode once it promotes."""
    s = hll_sketch(lg_k, tgt)
    for v in items:
        s.update(v)
    return s


def dense_from_first_update(items, lg_k=LG_K, tgt=REGISTER_FORM):
    """`start_max_size`: register mode from the very first update, never sparse."""
    s = hll_sketch(lg_k, tgt, True)
    for v in items:
        s.update(v)
    return s


def staged(items, parts, lg_k=LG_K):
    """Built by unioning `parts` slices — a lawful route that reaches the same governed state."""
    u = hll_union(lg_k)
    for i in range(parts):
        u.update(sparse_or_default(items[i::parts], lg_k))
    return u.get_result(REGISTER_FORM)


def registers_of(sketch):
    """The governed state, decoded. Mirrors the provider's decoder deliberately: if the two ever
    disagree the conformance suite is no longer checking the thing that runs."""
    image = sketch.serialize_compact()
    if image[0] == 10:
        return tuple(sketch.serialize_updatable()[PREAMBLE:])
    off = 4 * image[0]
    n = (len(image) - off) // 4
    regs = [0] * (1 << sketch.lg_config_k)
    for c in struct.unpack_from(f"<{n}I", image, off):
        slot, val = c & ((1 << sketch.lg_config_k) - 1), c >> 26
        regs[slot] = max(regs[slot], val)
    return tuple(regs)


def every_representation(items):
    """Six carriers of ONE governed state. A provider may hand the finalizer any of them."""
    return {
        "library default": sparse_or_default(items),
        "dense from first update": dense_from_first_update(items),
        "staged union, 2 parts": staged(items, 2),
        "staged union, 3 parts": staged(items, 3),
        "HLL_4 encoding": sparse_or_default(items, tgt=tgt_hll_type.HLL_4),
        "HLL_6 encoding": sparse_or_default(items, tgt=tgt_hll_type.HLL_6),
    }


#: Sizes chosen to straddle the library's LIST→SET→HLL promotions at lg_k = 12 (8 and 385), because
#: those are the representation changes a provider makes without telling anyone.
SIZES = [0, 1, 5, 7, 8, 9, 100, 193, 384, 385, 400, 1000, 20000]


# ══ R3 — representation independence ═════════════════════════════════════════════════════════════
@pytest.mark.parametrize("n", SIZES)
def test_one_governed_state_gives_one_answer_whatever_carries_it(n):
    """**THE UNIT'S WHOLE POINT.** Sparse, dense, staged and re-encoded carriers of one governed
    input must finalize to one number — not to numbers within RSE of each other, the same number."""
    items = values(n)
    answers = {label: governed_estimate(s) for label, s in every_representation(items).items()}
    assert len(set(answers.values())) == 1, f"representation leak at n={n}: {answers}"


@pytest.mark.parametrize("n", SIZES)
def test_the_two_providers_publish_the_same_integer(n):
    """Kernel and columnar reach the finalizer by different routes — a live `hll_sketch` and a
    `serialize_compact()` payload. The published integer may not depend on which."""
    items = values(n)
    kernel = KB._estimate_apply({"HLL_SKETCH": sparse_or_default(items)}, {})
    columnar = CP.estimate_of(CP.sketch_of(items))
    assert kernel == columnar


# ══ R2 — finalization does not consult construction history ══════════════════════════════════════
@pytest.mark.parametrize("n", [1000, 20000, 200000])
def test_construction_history_does_not_move_the_answer(n):
    """The defect this unit repairs, as a regression. Direct and staged construction of one input
    reach one governed state; before the repair they published different integers."""
    items = values(n)
    routes = [sparse_or_default(items), staged(items, 2), staged(items, 3),
              dense_from_first_update(items)]
    assert len({registers_of(r) for r in routes}) == 1, "the routes do not agree on governed state"
    assert len({KB._estimate_apply({"HLL_SKETCH": r}, {}) for r in routes}) == 1


def test_negative_control_the_library_estimate_is_route_dependent():
    """**WHY THE NORMALIZATION EXISTS.** If this ever starts passing as an equality, DataSketches has
    changed and the whole apparatus should be re-examined rather than trusted."""
    items = values(20000)
    direct, two_way = sparse_or_default(items), staged(items, 2)
    assert registers_of(direct) == registers_of(two_way)
    assert direct.get_estimate() != two_way.get_estimate()
    assert int(round(direct.get_estimate())) == 19832        # the old published answer
    assert int(round(two_way.get_estimate())) == 20100       # the old published answer, other route
    assert KB._estimate_apply({"HLL_SKETCH": direct}, {}) == 20100 == \
        KB._estimate_apply({"HLL_SKETCH": two_way}, {})      # the governed answer, both routes


def test_negative_control_omitting_the_forcing_step_returns_the_template_cardinality():
    """**THE MISTAKE THAT WAS MADE AND MEASURED.** `deserialize` does not recompute the cached
    estimator accumulators from the registers it is handed; it trusts the preamble. Splice registers
    into the template and estimate *without* the forcing union and every input returns the template's
    own cardinality. A future 'simplification' that drops the union would fail only this test."""
    preamble = _history_free_preamble(LG_K)
    unforced = []
    for n in (5, 1000, 20000):
        regs = bytes(registers_of(sparse_or_default(values(n))))
        unforced.append(hll_sketch.deserialize(preamble + regs).get_estimate())
    assert len(set(unforced)) == 1, "the unforced estimates differ, so they are not the template's"
    assert unforced[0] < 3           # it is the TEMPLATE's cardinality (two items), not any input's
    forced = [governed_estimate(sparse_or_default(values(n))) for n in (5, 1000, 20000)]
    assert len(set(forced)) == 3


def test_negative_control_one_forcing_update_is_not_enough():
    """A single union update lets the gadget adopt the incoming sketch whole, history included."""
    one, two = [], []
    for n in (5, 1000, 20000):
        carrier = _register_form(sparse_or_default(values(n)))
        u1 = hll_union(LG_K)
        u1.update(carrier)
        one.append(u1.get_estimate())
        two.append(governed_estimate(sparse_or_default(values(n))))
    assert one != two


# ══ governed-state algebra, carried forward from B-4a″(i) ════════════════════════════════════════
def join(a, b):
    return tuple(max(x, y) for x, y in zip(a, b))


@pytest.mark.parametrize("n", [4, 40, 4000])
def test_delivery_and_continuation_cohere(n):
    """`deliver(S1 ∪ S2) ~ deliver(S1) ⊔ deliver(S2)` — the property that makes the family fertile,
    and a stronger statement than any law about `⊔` alone. Disjoint, overlapping and empty."""
    a, b = set(values(n)), set(values(n, "w"))
    overlapping = set(values(n)) | set(values(n // 2 or 1, "w"))
    for s1, s2 in ((a, b), (a, overlapping), (a, a), (a, set()), (set(), set())):
        whole = registers_of(sparse_or_default(sorted(s1 | s2)))
        parts = join(registers_of(sparse_or_default(sorted(s1))),
                     registers_of(sparse_or_default(sorted(s2))))
        assert whole == parts


def test_the_continuation_is_a_commutative_idempotent_monoid_over_governed_state():
    states = [registers_of(sparse_or_default(values(n, t)))
              for n, t in ((0, "a"), (3, "b"), (400, "c"), (9000, "d"))]
    unit = tuple([0] * SLOTS)
    for a in states:
        assert join(a, a) == a                                  # idempotent
        assert join(a, unit) == a == join(unit, a)              # identity
        for b in states:
            assert join(a, b) == join(b, a)                     # commutative
            for c in states:
                assert join(join(a, b), c) == join(a, join(b, c))   # associative


def test_analytical_equality_does_not_imply_byte_equality():
    """Three identities, kept apart. A cache or a comparison keyed on bytes would be keyed on the
    wrong thing."""
    items = values(50)
    a, b = sparse_or_default(items), sparse_or_default(list(reversed(items)))
    dense = dense_from_first_update(items)
    assert registers_of(a) == registers_of(b) == registers_of(dense)
    assert a.serialize_compact() != b.serialize_compact()
    assert a.serialize_compact() != dense.serialize_compact()
    assert governed_estimate(a) == governed_estimate(b) == governed_estimate(dense)


def test_finalization_is_not_continuation():
    """Two estimates do not give the estimate at a coarser anchor. This is why `HLL_ESTIMATE` has no
    continuation and why the sketch, not the number, is the family value."""
    a, b = sparse_or_default(values(3000)), sparse_or_default(values(3000, "w"))
    merged = union_of(a, b)
    assert governed_estimate(a) + governed_estimate(b) != governed_estimate(merged)


# ══ mixed governed type fails closed ═════════════════════════════════════════════════════════════
def test_a_precision_mismatch_refuses_instead_of_downsampling():
    """`hll_union` reduces a mismatched pair to the smaller `lg_k` and says nothing, producing a
    number about no population. Precision is part of this value's governed type."""
    a, b = sparse_or_default(values(5000), lg_k=12), sparse_or_default(values(5000, "w"), lg_k=14)
    with pytest.raises(KernelRefusal) as refusal:
        KB._sketch_merge(a, b)
    assert refusal.value.code == "incompatible-sketch-type"
    assert "lg_k=12" in refusal.value.detail and "lg_k=14" in refusal.value.detail


def test_a_merge_reads_its_operands_type_rather_than_a_module_constant():
    """Both operands at lg_k = 14 must merge AT 14. The previous merge unioned at the module's own
    12 regardless, so a same-type merge above the constant was silently downsampled too."""
    a = sparse_or_default(values(5000), lg_k=14)
    b = sparse_or_default(values(5000, "w"), lg_k=14)
    assert KB._sketch_merge(a, b).lg_config_k == 14


def test_the_columnar_accumulator_refuses_a_mixed_column():
    acc = CP.HllUnionAccumulator()
    acc.update(pa.array([sparse_or_default(values(500), lg_k=12).serialize_compact()],
                        type=pa.binary()))
    with pytest.raises(KernelRefusal):
        acc.update(pa.array([sparse_or_default(values(500), lg_k=14).serialize_compact()],
                            type=pa.binary()))


def test_continuation_output_carries_the_encoding_it_was_asked_for():
    """`hll_union.get_result()` defaults to `HLL_4`, so continuation used to emit a different carrier
    encoding from every root. Governed state was unaffected; a carrier type nobody chose is still not
    one anybody can reason about."""
    a, b = sparse_or_default(values(3000)), sparse_or_default(values(3000, "w"))
    assert KB._sketch_merge(a, b).tgt_type == REGISTER_FORM
    acc = CP.HllUnionAccumulator()
    acc.update(pa.array([CP.sketch_of(values(3000)), CP.sketch_of(values(3000, "w"))],
                        type=pa.binary()))
    assert hll_sketch.deserialize(bytes(acc.evaluate().as_py())).tgt_type == REGISTER_FORM


# ══ cross-provider state fidelity ════════════════════════════════════════════════════════════════
def test_kernel_and_columnar_reach_the_same_governed_state():
    """One governed input, two realizations — live objects versus compact payloads through the real
    UDAF accumulator — and a single-shot direct build as the third witness."""
    groups = [values(700), values(700, "w"), values(3, "z"), []]
    kernel = KB._sketch_contribute(groups[0], {})
    for g in groups[1:]:
        kernel = KB._sketch_merge(kernel, KB._sketch_contribute(g, {}))
    acc = CP.HllUnionAccumulator()
    acc.update(pa.array([CP.sketch_of(g) for g in groups], type=pa.binary()))
    columnar = hll_sketch.deserialize(bytes(acc.evaluate().as_py()))
    direct = sparse_or_default([v for g in groups for v in g])
    assert registers_of(kernel) == registers_of(columnar) == registers_of(direct)
    assert governed_estimate(kernel) == governed_estimate(columnar) == governed_estimate(direct)


def test_an_empty_sketch_still_estimates_zero_and_is_not_a_null():
    """The unit is a real value: participated, contributed nothing distinct. Not an absence."""
    assert governed_estimate(KB._sketch_identity()) == 0.0
    assert KB._estimate_apply({"HLL_SKETCH": KB._sketch_identity()}, {}) == 0
    assert CP.estimate_of(CP.sketch_of([])) == 0

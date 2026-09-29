"""
test_e2_coordinate_index_identity.py — **E-2: `CoordinateIndex.identity`, memoised and unchanged.**

    *"Make `CoordinateIndex.identity` stable/memoized so repeated reads do not rebuild JSON and recompute
    SHA-256 over the entire index; preserve exact current identity semantics; preserve frozen/immutable
    behavior; no change to alignment semantics."*  — Huayin, 2026-09-29

Recon E-X measured the defect: a plain `@property` doing `O(cells × width)` Python plus a full
`json.dumps` plus a SHA-256 **on every access** — and it is accessed twice per role pair in
`columnar/expression.py`'s layout check and twice inside `AnchorInstance.aligns_with`, both before any
arithmetic runs.

The unit is a cache. So the burden of proof is almost entirely on **sameness**, not on speed:

    A  the memo returns what recomputation would
    B  repeated reads compute once
    C  the algorithm is byte-for-byte the pre-E-2 one — proven against a verbatim reimplementation
    D  frozen behaviour, equality and hashing are unaffected by whether the memo is warm
    E  alignment semantics are untouched

WHAT IS NOT EXERCISED, DELIBERATELY: no HLL rewrite, no DataFusion change, no DuckDB, no persistence, no
provider-interface change, no broader index redesign. Ruled out by name.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import fields, replace

import pytest

from columna_platform.columnar import CoordinateIndex
from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar import index as index_module
from columna_platform.columnar.index import AnchorInstance, index_digest
from columna_platform.kernel import KernelRefusal
from columna_platform.kernel import exhibit as KEX

LOAD = "load:orders@08:00Z"


# ── the pre-E-2 algorithm, reproduced VERBATIM ───────────────────────────────────────────────────
def _pre_e2_identity(index: CoordinateIndex) -> str:
    """**The body of `CoordinateIndex.identity` exactly as it shipped before E-2.**

    Copied rather than imported, deliberately: importing the new code to check the new code would prove
    only that the memo is faithful to itself. This is the independent witness that *"preserve exact current
    identity semantics"* actually holds, and it is the reason a reader can trust that no layout comparison
    anywhere in the system moved."""
    payload = {
        "manifold": index.manifold,
        "universe": index.anchor.universe,
        "anchor": sorted(index.anchor.constituents),
        "coordinates": [list(map(index_module._jsonable, c)) for c in index.coordinates],
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return "cidx-1:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


class _Counter:
    """Counts digest computations. The only honest way to prove a cache caches."""

    def __init__(self, real):
        self.real, self.calls = real, 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.real(*args, **kwargs)


@pytest.fixture
def counted(monkeypatch):
    counter = _Counter(index_module.index_digest)
    monkeypatch.setattr(index_module, "index_digest", counter)
    return counter


@pytest.fixture
def small():
    return CoordinateIndex.of("andfam.commerce", KEX.BY_DAY, [("D1",), ("D2",)])


@pytest.fixture
def wide():
    """Enough points that a recomputation would be visible, and enough width to exercise the tuple path."""
    return CoordinateIndex.of(
        "andfam.commerce", KEX.SALE_AT,
        [(f"S{s}", f"D{d}", f"O{o}") for s in range(4) for d in range(5) for o in range(10)])


# ══ A · THE IMPLEMENTATION SHAPE ══════════════════════════════════════════════════════════════════
def test_the_digest_is_a_pure_function_and_the_property_is_a_memo_around_it(small):
    """The extraction is the shape: a cache is only reviewable if the thing being cached is callable on
    its own."""
    assert small.identity == index_digest(small.manifold, small.anchor, small.coordinates)
    assert callable(index_digest)
    # and the memo slot exists from construction, empty
    fresh = CoordinateIndex.of("m", KEX.BY_DAY, [("D1",)])
    assert fresh.__dict__["_identity"] is None
    fresh.identity
    assert fresh.__dict__["_identity"] is not None


def test_the_memo_is_not_a_dataclass_field(small):
    """It must not enter equality, hashing, `replace()` or any serialisation of the governed content."""
    names = {f.name for f in fields(CoordinateIndex)}
    assert names == {"manifold", "anchor", "coordinates"}
    assert "_identity" not in names and "_positions" not in names


# ══ B · REPEATED READS COMPUTE ONCE ═══════════════════════════════════════════════════════════════
def test_a_hundred_reads_compute_the_digest_once(counted, wide):
    values = {wide.identity for _ in range(100)}
    assert len(values) == 1
    assert counted.calls == 1


def test_the_first_read_computes_and_construction_does_not(counted):
    """Lazy, not eager: an index whose identity is never asked for pays nothing. `CoordinateIndex.of` is
    called once per continuation in `_target_index`, and not every one of those has its layout compared."""
    index = CoordinateIndex.of("m", KEX.BY_DAY, [("D1",), ("D2",)])
    assert counted.calls == 0                                # construction is free
    index.identity
    assert counted.calls == 1
    index.identity
    assert counted.calls == 1


def test_the_layout_CHECK_that_motivated_this_now_computes_twice_not_four_times(counted):
    """The site recon E-X named: `aligns_with` reads `.identity` on both sides, and
    `columnar/expression.py` asks it per role pair. Two distinct indexes, asked repeatedly, is two
    computations total rather than two per question."""
    instance = KEX.build().instance_of("revenue")
    # the index's Manifold must match the instance's — one anchor instance cannot straddle two
    # jurisdictions, which `AnchorInstance.__post_init__` refuses
    one = AnchorInstance(index=CoordinateIndex.of(KEX.MANIFOLD, KEX.BY_DAY, [("D1",)]),
                         instance=instance)
    two = AnchorInstance(index=CoordinateIndex.of(KEX.MANIFOLD, KEX.BY_DAY, [("D1",), ("D2",)]),
                         instance=instance)

    for _ in range(10):
        one.aligns_with(two)
    assert counted.calls == 2                                # one per distinct index, not per question


def test_reads_through_a_derived_state_are_also_memoised(counted):
    """The real workload: a served columnar answer whose index identity is read from several places."""
    engine, _block = CEX.build(settled=True, data_state=LOAD)
    before = counted.calls
    state = engine.measure("revenue", CEX.BY_DAY).value
    reads = {state.index.identity for _ in range(50)}
    assert len(reads) == 1
    # whatever the engine itself computed while serving, 50 further reads added nothing
    after_first = counted.calls
    state.index.identity
    assert counted.calls == after_first
    assert counted.calls >= before


# ══ C · THE ALGORITHM IS UNCHANGED ════════════════════════════════════════════════════════════════
def test_the_digest_matches_the_pre_e2_algorithm_byte_for_byte(small, wide):
    """**The independent witness.** See `_pre_e2_identity`."""
    for index in (small, wide):
        assert index.identity == _pre_e2_identity(index)


def test_it_matches_for_every_index_the_real_engines_build():
    """Not only for indexes a test constructed: every index reachable from a served columnar world."""
    engine, block = CEX.build(settled=True, data_state=LOAD)
    indexes = [block.index]
    for anchor in (CEX.SALE_AT, CEX.BY_DAY, CEX.TOTAL):
        served = engine.measure("revenue", anchor)
        if served.served:
            indexes.append(served.value.index)
    assert len(indexes) >= 3
    for index in indexes:
        assert index.identity == _pre_e2_identity(index)


def test_the_prefix_and_width_are_unchanged(small):
    assert small.identity.startswith("cidx-1:")
    assert len(small.identity) == len("cidx-1:") + 32


def test_identical_indexes_still_produce_identical_identities():
    a = CoordinateIndex.of("m", KEX.BY_DAY, [("D1",), ("D2",)])
    b = CoordinateIndex.of("m", KEX.BY_DAY, [("D2",), ("D1",)])       # different input order
    assert a.coordinates == b.coordinates                            # `of` sorts
    assert a.identity == b.identity


def test_different_indexes_still_differ_on_every_axis():
    base = CoordinateIndex.of("m", KEX.BY_DAY, [("D1",), ("D2",)])
    variants = {
        "manifold": CoordinateIndex.of("other", KEX.BY_DAY, [("D1",), ("D2",)]),
        "anchor": CoordinateIndex.of("m", KEX.BY_STORE, [("D1",), ("D2",)]),
        "coordinates": CoordinateIndex.of("m", KEX.BY_DAY, [("D1",)]),
        "values": CoordinateIndex.of("m", KEX.BY_DAY, [("D1",), ("D3",)]),
    }
    for axis, variant in variants.items():
        assert variant.identity != base.identity, axis
    assert len({v.identity for v in variants.values()} | {base.identity}) == 5


def test_a_manifold_is_still_in_the_digest():
    """The governed property the digest exists to carry: two Manifolds' indexes over the same coordinates
    are different indexes."""
    one = CoordinateIndex.of("andfam.commerce", KEX.BY_DAY, [("D1",)])
    two = CoordinateIndex.of("acme.commerce", KEX.BY_DAY, [("D1",)])
    assert one.coordinates == two.coordinates and one.anchor == two.anchor
    assert one.identity != two.identity


def test_the_scalar_anchor_still_digests():
    """The degenerate index — one empty coordinate — which is what every grand total is laid out on."""
    scalar = CoordinateIndex.of("m", KEX.TOTAL, [()])
    assert scalar.identity == _pre_e2_identity(scalar)
    assert scalar.identity != CoordinateIndex.of("m", KEX.TOTAL, []).identity


# ══ D · FROZEN BEHAVIOUR, EQUALITY AND HASHING ════════════════════════════════════════════════════
def test_the_object_is_still_frozen(small):
    from dataclasses import FrozenInstanceError

    for field in ("manifold", "anchor", "coordinates"):
        with pytest.raises(FrozenInstanceError):
            setattr(small, field, None)
    with pytest.raises(FrozenInstanceError):
        small.identity = "cidx-1:forged"                     # type: ignore[misc]


def test_a_warm_memo_does_not_change_equality_or_hashing():
    """**The hazard worth pinning.** The memo lives in `__dict__`, so a read instance and an unread one
    have different `__dict__`s. Dataclass equality and hashing use FIELDS, so they must not notice — and
    anything that had compared `vars()` would have been broken by this unit."""
    warm = CoordinateIndex.of("m", KEX.BY_DAY, [("D1",), ("D2",)])
    cold = CoordinateIndex.of("m", KEX.BY_DAY, [("D1",), ("D2",)])
    warm.identity                                            # warm one only

    assert warm.__dict__["_identity"] is not None and cold.__dict__["_identity"] is None
    assert warm == cold
    assert hash(warm) == hash(cold)
    assert len({warm, cold}) == 1                            # interchangeable as dict/set keys
    assert cold.identity == warm.identity                    # and the cold one agrees when asked


def test_replace_produces_a_fresh_memo_and_a_correct_identity(small):
    """`replace()` constructs a new object, so `__post_init__` empties the slot. There is no invalidation
    path because there is no mutation path."""
    small.identity
    moved = replace(small, manifold="elsewhere")
    assert moved.__dict__["_identity"] is None
    assert moved.identity != small.identity
    assert moved.identity == _pre_e2_identity(moved)


def test_a_deep_copy_carries_a_correct_memo(small):
    """Copying a warm index copies a digest that is still true of it, because the digest is a function of
    the fields the copy shares."""
    small.identity
    clone = copy.deepcopy(small)
    assert clone == small
    assert clone.identity == small.identity == _pre_e2_identity(clone)


def test_construction_refusals_are_unchanged(small):
    """`__post_init__` gained a line; it must not have gained or lost a refusal."""
    with pytest.raises(KernelRefusal) as malformed:
        CoordinateIndex(manifold="m", anchor=KEX.BY_DAY, coordinates=(("D1", "S1"),))
    assert malformed.value.code == "malformed-coordinate"

    with pytest.raises(KernelRefusal) as duplicate:
        CoordinateIndex(manifold="m", anchor=KEX.BY_DAY, coordinates=(("D1",), ("D1",)))
    assert duplicate.value.code == "duplicate-coordinate"


def test_position_and_has_are_unchanged(small):
    assert small.position(("D1",)) == 0 and small.position(("D2",)) == 1
    assert small.has(("D1",)) and not small.has(("D9",))
    with pytest.raises(KernelRefusal) as absent:
        small.position(("D9",))
    assert absent.value.code == "coordinate-not-in-index"


# ══ E · ALIGNMENT SEMANTICS ARE UNTOUCHED ═════════════════════════════════════════════════════════
def test_aligns_with_still_decides_the_same_way():
    instance = KEX.build().instance_of("revenue")
    make = lambda cells: AnchorInstance(                                            # noqa: E731
        index=CoordinateIndex.of(KEX.MANIFOLD, KEX.BY_DAY, cells), instance=instance)
    same_a, same_b, different = make([("D1",)]), make([("D1",)]), make([("D2",)])

    assert same_a.aligns_with(same_b)
    assert not same_a.aligns_with(different)


def test_the_layouts_differ_refusal_still_fires_with_the_same_words():
    """The governed refusal that alignment exists to produce — a positional kernel will not discover a
    correspondence by joining on coordinate values."""
    import pyarrow as pa

    from columna_platform.columnar import ColumnarExpressionEvaluator, ColumnarFamilyState
    from columna_platform.columnar.standing import standing
    from columna_platform.kernel.law import SCALAR

    engine, _block = CEX.build(settled=True, data_state=LOAD)
    evaluator = ColumnarExpressionEvaluator(engine)
    state = engine.measure("revenue", CEX.BY_DAY).value
    mismatched = ColumnarFamilyState(
        family_id="order_count",
        anchor_instance=type(state.anchor_instance)(
            index=CoordinateIndex.of(CEX.MANIFOLD, CEX.BY_DAY, [("D1",)]),
            instance=engine.authority.instance_of("order_count")),
        values=pa.array([1], type=pa.int64()),
        standing=standing("order_count", engine.authority.instance_of("order_count"), n=1),
        law="COUNT", value_form=SCALAR, forgotten_since_root=frozenset({"order", "store"}))
    engine.retain(mismatched)

    answer = evaluator.evaluate("average_order_value", CEX.BY_DAY)
    assert not answer.served
    assert "layouts-differ" in answer.refusal.detail
    assert "would be relational discovery of analytical alignment" in answer.refusal.detail


def test_the_provider_invented_a_point_refusal_still_fires():
    """`align_onto` compares produced groups against a held index. The digest is reported in its note, so
    a memo that returned a stale value would have made a reindex report the wrong layout."""
    from columna_platform.columnar import ColumnarProvider

    provider = ColumnarProvider()
    target = CoordinateIndex.of("m", KEX.BY_DAY, [("D1",)])
    with pytest.raises(KernelRefusal) as invented:
        provider.align_onto({("D1",): 1.0, ("D9",): 2.0}, target)
    assert invented.value.code == "provider-invented-a-point"

    values, report = provider.align_onto({("D1",): 1.0}, target)
    assert values.to_pylist() == [1.0]
    assert report.to_identity == target.identity == _pre_e2_identity(target)


def test_grouped_continuation_still_produces_a_differing_layout_and_says_so():
    """The exhibit's own claim: a continued state's index is NOT the root block's index."""
    engine, block = CEX.build(settled=True, data_state=LOAD)
    by_day = engine.measure("revenue", CEX.BY_DAY)
    assert by_day.served
    assert by_day.value.index.identity != block.index.identity
    assert by_day.value.index.identity == _pre_e2_identity(by_day.value.index)


# ══ F · NOTHING ELSE MOVED ════════════════════════════════════════════════════════════════════════
def test_no_provider_interface_changed():
    """Ruled: no provider-interface changes. E-1's table and both dispatch signatures are untouched."""
    import inspect

    from columna_platform.columnar import ColumnarProvider

    provider = ColumnarProvider()
    assert len(provider.capabilities) == 4
    assert "target_index" in inspect.signature(provider.continue_grouped).parameters
    assert "law" in inspect.signature(provider.evaluate_positional).parameters


# `test_the_hll_kernel_is_still_untouched` lived here and said of itself: *"this test is expected to be
# DELETED by E-3."* E-3 ran on 2026-09-29, rewrote the finalizer's carriage and retired
# `Realization.finalize`, so the test was deleted as designed rather than edited into agreement with the
# new state — a scope guard that outlives its scope stops being one. Its subject now has its own file,
# `test_e3_hll_estimate_execution.py`.


def test_no_broader_index_redesign_happened():
    """The public surface of the index is exactly what it was, plus the extracted pure function."""
    assert {f.name for f in fields(CoordinateIndex)} == {"manifold", "anchor", "coordinates"}
    methods = {n for n in dir(CoordinateIndex) if not n.startswith("_")}
    assert methods == {"identity", "position", "has", "columns", "of"}


def test_the_exhibits_are_green(capsys):
    from columna_platform.columnar import exhibit as columnar_exhibit
    from columna_platform.frameql import exhibit as frameql_exhibit
    from columna_platform.kernel import exhibit as kernel_exhibit

    for exhibit in (kernel_exhibit, columnar_exhibit, frameql_exhibit):
        assert exhibit.main() == 0, exhibit.__name__
        assert "✗" not in capsys.readouterr().out, exhibit.__name__

"""
test_columnar_persistence.py — **P-2: local Arrow/Parquet persistence, and restart survival.**

    *"Persist and reload the actual Arrow/Parquet block the MME already executes… Persist the named
    dimensions separately… Do not concatenate them into one version token."*  — Huayin, 2026-09-29

The ten required proofs are the ten sections. `persistence.main()` is the narrative version and is run here
too, because a proof that is not executed is a document.

WHAT IS NOT EXERCISED, DELIBERATELY: no Iceberg, no Postgres, no catalog service, no refresh orchestrator.
A test that mocked one would be the first place the next unit's design got made by accident.
"""
from __future__ import annotations

import json
from dataclasses import replace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from columna_platform.columnar import exhibit as EX
from columna_platform.columnar import ColumnarExpressionOutput, ColumnarFamilyState
from columna_platform.columnar.persistence import (
    DIMENSIONS,
    SIDECAR_FILE,
    STANDING_FILE,
    VALUES_FILE,
    LocalColumnarStore,
    required_metadata,
)
from columna_platform.kernel import DataStateRef, KernelRefusal, WITNESS_SCHEME

LOAD = DataStateRef("load", "orders@2026-09-29T08:00Z")
RELOAD = DataStateRef("load", "orders@2026-09-29T17:30Z")


@pytest.fixture
def store(tmp_path):
    return LocalColumnarStore(tmp_path / "store")


@pytest.fixture
def engine():
    """A settled world, established from ONE evidence state, with a continuation and an expression held."""
    mme, block = EX.build(settled=True, data_state=LOAD)
    mme.measure("revenue", EX.BY_DAY, data_state=LOAD)
    mme.measure("distinct_customers", EX.BY_DAY, data_state=LOAD)
    mme.evaluate("distinct_customer_estimate", EX.BY_DAY, data_state=LOAD)
    return mme


def _fresh(*, settled: bool = True, data_state=LOAD):
    """A constituted engine holding NOTHING. The declarations are the constitution and are not persisted."""
    mme, _ = EX.build(settled=settled, data_state=data_state)
    mme._store.clear()
    return mme


def _held(mme, sort, identity, anchor, data_state=LOAD):
    return mme.retained(sort, identity, anchor,
                        mme.authority.instance_of(identity).with_data_state(data_state))


# ══ 1 · A REAL COLUMNAR BLOCK IS WRITTEN ══════════════════════════════════════════════════════════
def test_a_real_parquet_block_is_written(store, engine):
    written = store.write_all(engine)
    assert written
    for directory in written:
        assert (directory / VALUES_FILE).stat().st_size > 0
        assert (directory / SIDECAR_FILE).exists()
    # it is genuinely Parquet, readable by a reader that knows nothing about this package
    table = pq.read_table(written[0] / VALUES_FILE)
    assert table.num_rows > 0


def test_the_values_and_the_standing_are_separate_files(store, engine):
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    assert (directory / STANDING_FILE).exists()
    standing = pq.read_table(directory / STANDING_FILE)
    assert standing.column_names == ["participation", "support"]
    values = pq.read_table(directory / VALUES_FILE)
    assert "participation" not in values.column_names          # standing is not a value column
    assert "revenue__value" in values.column_names


def test_every_named_dimension_has_its_own_slot(store, engine):
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    sidecar = store.sidecar_of(directory)
    for dimension in DIMENSIONS:
        assert dimension in sidecar, dimension
    assert set(sidecar["data_state"]) == {"scheme", "token"}
    assert set(sidecar["constitution_context"]) == {"scheme", "token"}
    assert sidecar["constitution"]["scheme"] == WITNESS_SCHEME
    assert sidecar["constitution"]["determinants"]             # determinants, not only a digest


def test_no_composite_version_token_is_written_anywhere(store, engine):
    """*"Do not concatenate them into one version token."* Checked over the written BYTES, not the writer."""
    store.write_all(engine)
    blob = json.dumps([store.sidecar_of(d) for d in store.blocks()])
    for forbidden in ('"version"', '"etag"', '"generation"', '"sequence_number"', '"revision"',
                      '"fingerprint"'):
        assert forbidden not in blob, forbidden
    # the three facts are three keys, and none of them contains another
    sidecar = store.sidecar_of(store.blocks()[0])
    assert sidecar["constitution"]["digest"] not in json.dumps(sidecar["data_state"])
    assert sidecar["data_state"]["token"] not in json.dumps(sidecar["constitution"])
    assert sidecar["realization"]["codec"] not in json.dumps(sidecar["constitution"])


def test_the_codec_lives_only_in_realization_standing(store, engine):
    """A codec is realization standing, and the proof that it cannot reach analytical identity is that
    there is nowhere else for it to go."""
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    sidecar = store.sidecar_of(directory)
    assert sidecar["realization"]["codec"] == store.codec
    for dimension in DIMENSIONS:
        if dimension != "realization":
            assert store.codec not in json.dumps(sidecar[dimension])


def test_the_written_carrier_is_the_stores_not_the_engines(store, engine):
    """An engine holds this material as `in-memory-arrow`; written, it is carried by local Parquet. Both are
    recorded, and they are not the same fact."""
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    realization = store.sidecar_of(directory)["realization"]
    assert realization["carrier"] == "parquet-local"
    assert realization["held_as"] == "in-memory-arrow"
    assert realization["provider"] == engine.provider.name


# ══ 2 + 3 · THE ENGINE IS DESTROYED; A FRESH ONE RELOADS WITHOUT RE-ESTABLISHING ══════════════════
def test_a_fresh_engine_reloads_without_re_establishing_any_root(store, engine):
    written = store.write_all(engine)
    fresh = _fresh()
    assert fresh.held == ()

    report = store.load_into(fresh)
    assert len(report.loaded) == len(written)
    assert report.stale == ()
    assert fresh.held
    # every reloaded family state says where it came from, and it was not a root establishment
    for retained in fresh.held_objects():
        if retained.continuation_bearing:
            assert "reloaded from" in retained.value.route[-1]
            assert not any("established from" in step for step in retained.value.route[-1:])


def test_the_declarations_are_not_persisted_so_material_cannot_constitute_a_manifold(store, engine):
    """**A store that could reconstitute a Manifold from its own data files would make the material the
    authority for the law.** The declarations are deliberately absent from what is written; what is written
    is enough to decide whether material may be served under a constitution the engine ALREADY holds.

    Read into another Manifold's jurisdiction — same family names, same anchors, same Parquet — every block
    is refused, and the reason names the determinant: `manifold`. Not one value crosses."""
    store.write_all(engine)
    stranger, _ = EX.build(EX.OTHER_MANIFOLD, settled=True, data_state=LOAD)
    stranger._store.clear()

    report = store.load_into(stranger)
    assert report.loaded == ()
    assert report.stale
    assert {s.reason for s in report.stale} == {"constitution-superseded"}
    assert all(s.changed == ("manifold",) for s in report.stale)
    assert stranger.held == ()
    assert not stranger.measure("revenue", EX.BY_DAY, data_state=LOAD).served


# ══ 4 · REVENUE CONTINUES FROM RELOADED STATE ═════════════════════════════════════════════════════
def test_revenue_is_continued_from_reloaded_state(store, engine):
    store.write_all(engine)
    fresh = _fresh()
    store.load_into(fresh)

    total = fresh.measure("revenue", EX.TOTAL, data_state=LOAD)
    assert total.served and total.route == "continued"
    assert total.value.cell(()) == 560.0
    assert any("datafusion: aggregate" in step for step in total.value.route)


def test_an_expression_evaluates_over_reloaded_operands(store, engine):
    store.write_all(engine)
    fresh = _fresh()
    store.load_into(fresh)
    aov = fresh.evaluate("average_order_value", EX.BY_DAY, data_state=LOAD)
    assert aov.served
    assert aov.value.cell(("D1",)) == pytest.approx(235 / 3)


def test_the_reloaded_state_is_family_state_and_keeps_its_route_and_disclosures(store, engine):
    store.write_all(engine)
    fresh = _fresh()
    store.load_into(fresh)
    state = _held(fresh, "family", "revenue", EX.BY_DAY).value
    assert isinstance(state, ColumnarFamilyState)
    assert state.CONTINUATION_BEARING is True
    assert any("governed-filter" in step for step in state.route)   # the route it took survives
    assert state.forgotten_since_root == frozenset({"order", "store"})


# ══ 5 + 6 · THE SKETCH CONTINUES; THE RELOADED ESTIMATE CANNOT SEED ═══════════════════════════════
def test_the_hll_sketch_reloads_as_binary_and_still_continues(store, engine):
    store.write_all(engine)
    fresh = _fresh()
    store.load_into(fresh)
    state = _held(fresh, "family", "distinct_customers", EX.SALE_AT).value
    assert state.values.type == pa.binary()

    total = fresh.measure("distinct_customers", EX.TOTAL, data_state=LOAD)
    assert total.served and total.route == "continued"
    assert isinstance(total.value.cell(()), bytes)
    estimate = fresh.evaluate("distinct_customer_estimate", EX.TOTAL, data_state=LOAD)
    assert estimate.served and estimate.value.cell(()) == 5      # five distinct customers


def test_the_expression_cache_reloads_but_cannot_seed_family_continuation(store, engine):
    """The flagship distinction, through Parquet: the sort is a TYPE, so there is no field in the written
    bytes a mistake could flip."""
    store.write_all(engine)
    fresh = _fresh()
    store.load_into(fresh)

    retained = _held(fresh, "expression", "distinct_customer_estimate", EX.BY_DAY)
    assert isinstance(retained.value, ColumnarExpressionOutput)
    assert retained.continuation_bearing is False
    assert not hasattr(type(retained.value), "fold_onto_grouped")

    verdict = fresh.adjudicate(retained, fresh.family("distinct_customers"), EX.BY_DAY)
    assert not verdict and verdict.code == "not-continuation-bearing"
    # and it IS served as a cache hit, which is the other half of the claim
    assert fresh.evaluate("distinct_customer_estimate", EX.BY_DAY, data_state=LOAD).route == "cached"


def test_an_expression_block_carries_no_standing_file(store, engine):
    directory = store.write_expression(
        engine, _held(engine, "expression", "distinct_customer_estimate", EX.BY_DAY).value)
    assert not (directory / STANDING_FILE).exists()
    standing = store.sidecar_of(directory)["standing"]
    assert standing["file"] is None
    assert "CARRIES NO STANDING MASKS" in standing["note"]


# ══ 7 · A CHANGED CONSTITUTION WITNESS READS STALE ════════════════════════════════════════════════
def test_a_changed_constitution_witness_makes_the_persisted_block_stale(store, engine):
    store.write_all(engine)
    moved = _fresh()
    moved.authority.register_family(
        replace(moved.family("revenue"), participation="every order the auditor confirmed"))

    report = store.load_into(moved)
    stale = [s for s in report.stale if s.identity == "revenue"]
    assert stale
    assert stale[0].reason == "constitution-superseded"
    assert stale[0].changed == ("participation",)               # named ACROSS the restart
    assert "re-establishment is from the root" in stale[0].detail
    assert not moved.measure("revenue", EX.BY_DAY, data_state=LOAD).served
    # an untouched family is unaffected by its neighbour's constitution moving
    assert moved.measure("order_count", EX.BY_DAY, data_state=LOAD).served


def test_the_determinants_are_persisted_so_staleness_is_nameable_after_a_restart(store, engine):
    """Without the determinants on disk, a fresh engine could only report *"the digests differ"*."""
    store.write_all(engine)
    moved = _fresh()
    moved.authority.register_family(replace(moved.family("revenue"), root=EX.BY_STORE))
    report = store.load_into(moved)
    stale = [s for s in report.stale if s.identity == "revenue"][0]
    assert stale.changed == ("root",)
    # the superseded witness is now part of the engine's constitutional history, from the file
    assert moved.authority.constitution_seen(stale.held_under) is not None


def test_a_witness_written_under_a_superseded_scheme_fails_closed(store, engine):
    """`cw-1` is in-process and `repr`-based; persisted, it is comparable only within its own scheme. A block
    from another scheme is not trusted and is not declared stale about any governed fact either."""
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    sidecar = store.sidecar_of(directory)
    sidecar["constitution"]["scheme"] = "cw-0-from-the-future"
    (directory / SIDECAR_FILE).write_text(json.dumps(sidecar), encoding="utf-8")

    fresh = _fresh()
    report = store.load_into(fresh)
    stale = [s for s in report.stale if s.identity == "revenue"]
    assert stale and stale[0].reason == "witness-scheme-superseded"
    assert "FAILS CLOSED" in stale[0].detail
    assert stale[0].changed == ()                               # no governed determinant is claimed


# ══ 8 · A DIFFERENT DataStateRef IS A DISTINCT INSTANCE, NOT A STALE CONSTITUTION ═════════════════
def test_two_data_states_are_two_current_blocks_not_one_stale_one(store, engine):
    store.write_all(engine)
    second, _ = EX.build(settled=True, data_state=RELOAD)
    store.write_family(second, _held(second, "family", "revenue", EX.SALE_AT, RELOAD).value)

    fresh = _fresh()
    report = store.load_into(fresh)
    assert not any(s.identity == "revenue" for s in report.stale)     # NEITHER is stale

    keys = [k for k in fresh.held if k.identity == "revenue" and k.anchor == EX.SALE_AT]
    assert {k.data_state for k in keys} == {LOAD, RELOAD}
    assert len({k.constitution for k in keys}) == 1                  # ONE constitution
    assert not fresh.measure("revenue", EX.BY_DAY).served            # and the engine will not pick
    assert fresh.measure("revenue", EX.BY_DAY).refusal.code == "ambiguous-data-state"
    assert fresh.measure("revenue", EX.BY_DAY, data_state=LOAD).served


def test_the_data_state_is_a_typed_reference_and_nothing_parses_the_token(store, engine):
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    written = store.sidecar_of(directory)["data_state"]
    assert written == {"scheme": LOAD.scheme, "token": LOAD.token}
    # an untyped token is refused rather than guessed at
    with pytest.raises(KernelRefusal) as exc:
        DataStateRef.of("just-a-token")
    assert exc.value.code == "untyped-data-state"


def test_a_physical_difference_is_not_a_data_state_difference(store, engine, tmp_path):
    """*"Analytical compatibility is not defined as equality of physical snapshot tokens."* One DataStateRef,
    written to two different files by two different stores, is ONE analytical instance."""
    other = LocalColumnarStore(tmp_path / "elsewhere", codec="snappy")
    state = _held(engine, "family", "order_count", EX.SALE_AT).value
    here = store.write_family(engine, state)
    there = other.write_family(engine, state)
    assert here != there                                        # two physical locations
    assert store.sidecar_of(here)["data_state"] == other.sidecar_of(there)["data_state"]
    assert (store.sidecar_of(here)["constitution"]["digest"]
            == other.sidecar_of(there)["constitution"]["digest"])


# ══ 9 · A CODEC / PROVIDER DIFFERENCE IS REALIZATION STANDING ═════════════════════════════════════
def test_a_codec_difference_moves_only_the_realization_dimension(store, engine, tmp_path):
    snappy = LocalColumnarStore(tmp_path / "snappy", codec="snappy")
    state = _held(engine, "family", "order_count", EX.SALE_AT).value
    a = store.sidecar_of(store.write_family(engine, state))
    b = snappy.sidecar_of(snappy.write_family(engine, state))

    assert a["realization"] != b["realization"]
    assert {k: v for k, v in a.items() if k != "realization"} == {
        k: v for k, v in b.items() if k != "realization"}


def test_material_written_under_one_codec_reloads_under_another(store, engine, tmp_path):
    """The realization is a fact about the material, not a constraint on who may read it."""
    snappy = LocalColumnarStore(tmp_path / "snappy", codec="snappy")
    snappy.write_all(engine)
    fresh = _fresh()                                    # a zstd-default engine reading snappy blocks
    report = snappy.load_into(fresh)
    assert report.stale == ()
    assert fresh.measure("revenue", EX.TOTAL, data_state=LOAD).value.cell(()) == 560.0


# ══ 10 · ARROW NULL ACQUIRES NOTHING THROUGH SERIALIZATION ════════════════════════════════════════
def test_arrow_null_acquires_no_analytical_meaning_through_parquet(tmp_path):
    """The #349 correction, through a round trip. The value column's null still means nothing; the standing
    masks are what carry the meaning, and they travel in their own file."""
    store = LocalColumnarStore(tmp_path / "nulls")
    as_recorded, _ = EX.build(data_state=LOAD)          # O7 participates, Revenue unsupported
    store.write_all(as_recorded)

    after = _fresh(settled=False)
    store.load_into(after)
    state = _held(after, "family", "revenue", EX.SALE_AT).value
    position = state.index.position(EX.UNSUPPORTED_POINT)

    assert state.values.null_count == 1                         # the null survived, meaning nothing
    assert state.standing.participation[position].as_py() is True
    assert state.standing.support[position].as_py() is False
    assert state.wants_state

    refused = after.measure("revenue", EX.BY_DAY, data_state=LOAD)
    assert not refused.served and refused.refusal.code == "want-of-state"
    assert after.measure("order_count", EX.BY_DAY, data_state=LOAD).value.cell(("D1",)) == 3


def test_a_null_in_a_standing_mask_is_still_refused_on_read(tmp_path, engine):
    """A standing mask may not be null in memory, and reading one off a file is not a way in."""
    store = LocalColumnarStore(tmp_path / "tampered")
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    standing = pq.read_table(directory / STANDING_FILE)
    holed = pa.table({
        "participation": pa.array([None] + standing.column("participation").to_pylist()[1:],
                                  type=pa.bool_()),
        "support": standing.column("support").combine_chunks()})
    pq.write_table(holed, directory / STANDING_FILE)

    with pytest.raises(KernelRefusal) as exc:
        store.load_into(_fresh())
    assert exc.value.code == "null-in-a-standing-mask"


# ══ GUARDS ════════════════════════════════════════════════════════════════════════════════════════
def test_the_coordinate_index_identity_is_re_derived_and_checked(store, engine):
    """A digest read back from the file that wrote it proves nothing. This one is recomputed."""
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    sidecar = store.sidecar_of(directory)
    sidecar["coordinate_index"]["identity"] = "cidx-1:" + "0" * 32
    (directory / SIDECAR_FILE).write_text(json.dumps(sidecar), encoding="utf-8")

    with pytest.raises(KernelRefusal) as exc:
        store.load_into(_fresh())
    assert exc.value.code == "coordinate-index-identity-mismatch"
    assert "positions would be reassigned silently" in exc.value.detail


def test_a_block_may_not_declare_the_constitution_context_on_disk_either(store, engine):
    directory = store.write_family(engine, _held(engine, "family", "revenue", EX.SALE_AT).value)
    sidecar = store.sidecar_of(directory)
    sidecar["constitution_context"]["token"] = "context:some-other-publication"
    (directory / SIDECAR_FILE).write_text(json.dumps(sidecar), encoding="utf-8")

    with pytest.raises(KernelRefusal) as exc:
        store.load_into(_fresh())
    assert exc.value.code == "constitution-context-mismatch"


def test_the_governed_axes_come_from_the_declaration_and_not_from_the_file(store, engine):
    """On disk as in memory: a block does not get to declare a family's instance. The one axis it supplies
    is the evidence state, because that is the axis establishment owns."""
    store.write_all(engine)
    fresh = _fresh()
    store.load_into(fresh)
    state = _held(fresh, "family", "revenue", EX.SALE_AT).value
    declared = fresh.authority.instance_of("revenue")
    assert state.instance.same_but_for_data_state(declared)
    assert state.instance.participation == declared.participation
    assert state.instance.data_state == LOAD


def test_reload_is_idempotent_and_adopts_rather_than_establishes(store, engine):
    store.write_all(engine)
    fresh = _fresh()
    first = store.load_into(fresh)
    held_after_first = set(fresh.held)
    second = store.load_into(fresh)
    assert set(fresh.held) == held_after_first          # the same keys, not duplicates
    assert len(second.loaded) == len(first.loaded)


def test_the_laundering_guard_survives_serialization(tmp_path):
    """**THE SHARPEST THING THE BLOCK HAD TO CARRY**, and it is not one of the eight named dimensions.

    `forgotten_since_root` accumulates everything a state has forgotten on its way from `R_F`, and it is what
    stops a two-step coarsening from obtaining an answer the law forbids. It is not derivable from the anchor,
    the values or the geometry: a `{store, day}` state that reached there by forgetting nothing and one that
    got there from a finer root are the same shape and have different rights. Persist it wrongly — or not at
    all — and an intermediate materialization becomes a laundering route across a restart, which is exactly
    the failure the guard exists for, now with a filesystem to hide in."""
    store = LocalColumnarStore(tmp_path / "launder")
    mme, block = EX.build(data_state=LOAD)
    on_hand = EX._families()[4]
    mme.authority.register_family(on_hand)
    level_index = EX.CoordinateIndex.of(EX.MANIFOLD, EX.COMMERCE.anchor({"store", "day"}),
                                        [("D1", "S1"), ("D1", "S2"), ("D2", "S1"), ("D2", "S2")])
    level_block = EX.GovernedBlock.of(
        level_index, {"on_hand": pa.array([10, 7, 12, 9], type=pa.int64())},
        {"on_hand": EX.standing("on_hand", mme.authority.instance_of("on_hand"), n=4)})
    mme.establish(level_block, "on_hand", data_state=LOAD)
    lawful = mme.measure("on_hand", EX.BY_DAY, data_state=LOAD)      # forgets {store} — INSIDE the region
    assert lawful.served and lawful.value.forgotten_since_root == frozenset({"store"})
    store.write_all(mme)

    after = _fresh(settled=False)
    after.authority.register_family(on_hand)
    store.load_into(after)
    reloaded = _held(after, "family", "on_hand", EX.BY_DAY).value
    assert reloaded.forgotten_since_root == frozenset({"store"})     # the route survived

    # and the guard still refuses the two-step route it exists to refuse
    laundered = after.measure("on_hand", EX.TOTAL, data_state=LOAD)
    assert not laundered.served
    assert "cannot launder an edge the law does not admit" in laundered.refusal.detail


# ══ THE REPORT, AND THE NARRATIVE ═════════════════════════════════════════════════════════════════
def test_the_required_metadata_report_names_every_dimension(store, engine):
    store.write_all(engine)
    required = required_metadata(store)
    assert required["blocks"] == len(store.blocks())
    assert set(required["files"]) <= {SIDECAR_FILE, STANDING_FILE, VALUES_FILE}
    for dimension in DIMENSIONS:
        assert dimension in required["dimensions"]


def test_the_persistence_proof_runs_green(capsys):
    from columna_platform.columnar import persistence

    assert persistence.main() == 0
    out = capsys.readouterr().out
    assert "ALL CHECKS PASSED" in out
    assert "✗" not in out

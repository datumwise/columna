"""
test_benchmark_coherence.py — the benchmark SELF-COHERENCE meta-check (CP-2, Huayin ruling 1).

Every ground-truth claim must be derivable from its own aperture's actual evidence (catalog()/
profile()). This test makes the real-001 failure class (a benchmark whose truth its own schema cannot
support — B5's absent FK, B8's unformable derived) die STRUCTURALLY, not vigilantly: the full ratified
instrument B1–B11 must be coherent, and a deliberately-broken benchmark must be caught.
"""
import pytest

from columna_server.init.benchmarks import BENCHMARKS
from columna_server.init.eval import Benchmark, benchmark_coherence, benchmark_advice_fires


@pytest.mark.parametrize("bid", sorted(BENCHMARKS))
def test_every_ratified_benchmark_is_self_coherent(bid):
    incoherences = benchmark_coherence(BENCHMARKS[bid])
    assert not incoherences, f"{bid}: {incoherences}"


def test_the_metacheck_catches_an_incoherent_benchmark():
    # the real-001 shape: an edge graded catalog, but the schema declares no FK.
    broken = Benchmark(
        id="X", kind="○",
        schema={"tables": {"stores": {"cols": [("store_id", "INTEGER"), ("region_id", "INTEGER")],
                                       "rows": [(1, 10)]}}},   # no FK declared
        ground_truth={"closures": [["edge", "store->region"]],
                      "grades": {"edge:store->region": "inferred_catalog"}})
    bad = benchmark_coherence(broken)
    assert bad and "declares no FK" in bad[0]


def test_the_metacheck_catches_an_unformable_derived():
    # B8's real-001 shape: a derived whose ingredient measures aren't closures of the benchmark.
    broken = Benchmark(
        id="Y", kind="◆",
        schema={"tables": {"tx": {"cols": [("id", "INTEGER"), ("amount", "DOUBLE")], "rows": [(1, 1.0)]}}},
        ground_truth={"closures": [["derived", "aov"]], "derived_needs": {"aov": ["revenue", "orders"]},
                      "grades": {}})
    bad = benchmark_coherence(broken)
    assert bad and "unformable" in bad[0]


def test_b8_corrected_exits_the_oracle_set_and_its_advice_fires():
    # ruling 2 (2026-07-16): B8 is now ○ (fertility is the adjudicator's advice, not an agent ◆), and the
    # deterministic advice channel fires from B8's own closures (aov = a formable derived ratio of measures).
    b8 = BENCHMARKS["B8"]
    assert b8.kind == "○" and b8.ground_truth["oracle_calls"] == []     # no agent-fertility ◆ to surface
    assert benchmark_advice_fires(b8)                                   # the adjudicator's advice fires (world-side)
    assert not benchmark_coherence(b8)                                  # advice is structurally supported


def test_advice_that_is_not_structurally_supported_is_incoherent():
    # an advice member that isn't a formable derived ratio of measures cannot be asserted to fire.
    broken = Benchmark(
        id="Z", kind="○",
        schema={"tables": {"tx": {"cols": [("id", "INTEGER"), ("amount", "DOUBLE")], "rows": [(1, 1.0)]}}},
        ground_truth={"closures": [["measure", "revenue"]], "grades": {},
                      "advice": [{"channel": "fertility", "member": "aov"}]})   # aov isn't even a closure
    assert not benchmark_advice_fires(broken)
    bad = benchmark_coherence(broken)
    assert bad and "advice" in bad[0]

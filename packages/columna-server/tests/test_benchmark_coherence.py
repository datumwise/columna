"""
test_benchmark_coherence.py — the benchmark SELF-COHERENCE meta-check (CP-2, Huayin ruling 1).

Every ground-truth claim must be derivable from its own aperture's actual evidence (catalog()/
profile()). This test makes the real-001 failure class (a benchmark whose truth its own schema cannot
support — B5's absent FK, B8's unformable derived) die STRUCTURALLY, not vigilantly: the full ratified
instrument B1–B11 must be coherent, and a deliberately-broken benchmark must be caught.
"""
import pytest

from columna_server.init.benchmarks import BENCHMARKS
from columna_server.init.eval import Benchmark, benchmark_coherence


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

"""
test_demo_data_drift.py — the packaged demo data must be a byte-identical copy of the columna-core
test fixtures (same guard pattern as WP-0's byte-identical `.cml` test), so the duplication can
never silently diverge.
"""
import os

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
_DEMO = os.path.join(_REPO, "packages", "columna-server", "src", "columna_server", "demo", "benchmark")
_CORE_FIX = os.path.join(_REPO, "packages", "columna-core", "tests", "fixtures")


def _same_bytes(a, b) -> bool:
    with open(a, "rb") as fa, open(b, "rb") as fb:
        return fa.read() == fb.read()


def test_demo_manifold_cml_matches_core_fixture():
    assert _same_bytes(os.path.join(_DEMO, "manifold.cml"),
                       os.path.join(_CORE_FIX, "benchmark.cml")), \
        "demo/benchmark/manifold.cml has drifted from the core benchmark.cml fixture"


def _demo_parquet():
    wh = os.path.join(_DEMO, "warehouse")
    return sorted(f for f in os.listdir(wh) if f.endswith(".parquet"))


def test_demo_warehouse_fileset_matches_core_fixture():
    demo = set(_demo_parquet())
    core = {f for f in os.listdir(os.path.join(_CORE_FIX, "mini_warehouse")) if f.endswith(".parquet")}
    assert demo == core, f"demo warehouse fileset differs from mini_warehouse: {demo ^ core}"


@pytest.mark.parametrize("fname", _demo_parquet())
def test_demo_warehouse_parquet_byte_identical(fname):
    assert _same_bytes(os.path.join(_DEMO, "warehouse", fname),
                       os.path.join(_CORE_FIX, "mini_warehouse", fname)), \
        f"demo warehouse {fname} has drifted from the mini_warehouse fixture"


def test_demo_data_within_2mb():
    total = 0
    for root, _dirs, files in os.walk(_DEMO):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    assert total <= 2 * 1024 * 1024, f"packaged demo data is {total/1024:.0f} KB > 2 MB"

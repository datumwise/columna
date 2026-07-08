"""
test_benchmark_warehouse.py — the 10 real-data proofs from demos/build_benchmark.py, against the FULL benchmark warehouse
(hand-built Manifold).

Marked @pytest.mark.warehouse: the check names are static so all 10 items are always *collected*,
but each is SKIPPED unless COLUMNA_BENCH_WAREHOUSE points at the real warehouse instance. This is
how the accounting stays "collects 124 / runs 104 / skips 20" in CI (env unset -> the 20 skip),
while `pytest -m warehouse` with the env set reproduces the 10/10 real-data proofs (acceptance 3).
"""
import os

import pytest

from _demo_driver import warehouse_run

pytestmark = pytest.mark.warehouse

_WAREHOUSE = os.environ.get("COLUMNA_BENCH_WAREHOUSE")
# resolve at read time (in the pytest process cwd): a relative value must not depend on the
# batch runner's cwd, else the warehouse marker silently fails.
if _WAREHOUSE:
    _WAREHOUSE = os.path.abspath(_WAREHOUSE)

_PROOF_NAMES = ['revenue@region == ground truth (transported store→region, no join pushdown)', 'revenue@cal.month == ground truth (transported day→month)', 'revenue@category is REFUSED (non-functional M:N transport)', '(for contrast) the naive join silently inflates revenue', 'level.sum@(region,day) is CLEAN — additive over the store axis (no crossing)', 'level.sum@store is SERVED with a CRITICAL B-anchor crossing disclosure (summing a stock across days) — inform-and-serve, not refused', 'aov@cal.month == sum(amount)/count (correct AOV)', 'HLL-merged visitors@quarter ≈ true distinct (within 5%)', '(naive sum-of-daily-distincts would overcount)', 'level.sum@product is REFUSED as out_of_universe (undefined, not missing)']


@pytest.mark.skipif(
    not _WAREHOUSE,
    reason="set COLUMNA_BENCH_WAREHOUSE to the real benchmark warehouse to run the real-data proofs",
)
@pytest.mark.parametrize("name", _PROOF_NAMES, ids=_PROOF_NAMES)
def test_proof(name):
    run = warehouse_run("build_benchmark", _WAREHOUSE)
    assert run.returncode == 0, run.stderr[-2000:]
    ok, detail = run.result(name)
    assert ok, f"{name} — {detail}"

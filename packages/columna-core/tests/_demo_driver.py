"""
_demo_driver.py — the bridge that turns each demo suite's checks into individually-reported
pytest items, without altering a single line of demo *logic*.

The demos come in two shapes — some run their checks inside `main()`, two
(`hll_case_study_demo`, `locus_demo`) run them at import time — and each keeps its own
`check(name, cond, detail)` helper that prints `  [PASS] <name>` / `  [FAIL] <name>  — <detail>`.
We run them through `_run_demos.py`, which executes each demo via runpy and parses those verdict
lines. Each parsed check becomes one parametrized pytest item whose id is the real check name, with
an `assert ok` body — a proper per-check test, mapped 1:1 to a demo check for the PR's mapping table.

Performance: all fixture demos are executed in a SINGLE batch subprocess so polars/duckdb/
datasketches are imported once for the whole suite (not once per demo) — the whole fixture suite
runs in seconds even on a cold CI runner, keeping the "< 90 s" budget. Each (demos, warehouse) batch
is cached, so a whole test session shares one fixture-demo run.
"""
import functools
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(HERE)                      # packages/columna-core
SRC = os.path.join(PKG_ROOT, "src")                   # importable columna_core
DEMOS = os.path.join(PKG_ROOT, "demos")               # the demo suites + build_benchmark harness
FIXTURE_WAREHOUSE = os.path.join(HERE, "fixtures", "mini_warehouse")
_RUNNER = os.path.join(HERE, "_run_demos.py")

# The nine fixture-run suites (the 104 checks) and the two real-data proof suites (10 × 2 = 20).
FIXTURE_DEMOS = (
    "coanchor_demo", "confine_demo", "hll_case_study_demo", "holistic_demo", "locus_demo",
    "operator_umbrella_demo", "projection_demo", "types_demo", "universe_check_demo",
)
WAREHOUSE_DEMOS = ("build_benchmark", "parse_benchmark")


class DemoRun:
    def __init__(self, checks, exit_code):
        self.checks = [(name, ok, "") for name, ok in checks]  # (name, ok, detail)
        self.returncode = exit_code

    def names(self):
        return [name for name, _ok, _d in self.checks]

    def result(self, name):
        for n, ok, detail in self.checks:
            if n == name:
                return ok, detail
        raise KeyError(f"check {name!r} was not emitted by the demo")


@functools.lru_cache(maxsize=None)
def _batch(demos: tuple, warehouse: str) -> dict:
    env = dict(os.environ)
    env["COLUMNA_BENCH_WAREHOUSE"] = warehouse
    env["PYTHONPATH"] = os.pathsep.join(
        [SRC, DEMOS] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])
    )
    proc = subprocess.run(
        [sys.executable, _RUNNER, warehouse, *demos],
        cwd=DEMOS, env=env, capture_output=True, text=True, timeout=300,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError(
            f"demo batch runner failed (rc={proc.returncode}).\nstderr:\n{proc.stderr[-3000:]}"
        )
    data = json.loads(proc.stdout)
    return {demo: DemoRun(d["checks"], d["exit"]) for demo, d in data.items()}


def fixture_run(demo: str) -> DemoRun:
    """Drive a demo against the checked-in mini-warehouse (the default CI path)."""
    return _batch(FIXTURE_DEMOS, FIXTURE_WAREHOUSE)[demo]


def warehouse_run(demo: str, warehouse: str) -> DemoRun:
    """Drive a real-data-proof demo against the full benchmark warehouse."""
    return _batch(WAREHOUSE_DEMOS, warehouse)[demo]

"""
_run_demos.py — batch demo runner (one process, imports paid once).

Invoked by _demo_driver as a subprocess:  python _run_demos.py <warehouse_dir> <demo> [<demo> ...]

It runs each named demo IN-PROCESS via runpy (exactly as `python <demo>.py` would — main()-guarded
suites run their main, top-level suites run their module-body checks), capturing each demo's stdout
and parsing its `[PASS]/[FAIL]` verdict lines. Because polars/duckdb/datasketches are imported once
for the whole batch (not once per demo subprocess), the full fixture suite runs in seconds even on a
cold CI runner — the key to the spec's "< 90 s" budget.

Emits one JSON object to stdout: {demo: {"exit": <int>, "checks": [[name, ok], ...]}}.
"""
import contextlib
import io
import json
import os
import re
import runpy
import sys

_LINE = re.compile(r"^\s*\[(PASS|FAIL)\]\s+(.*)$")


def run_one(demo: str) -> dict:
    buf = io.StringIO()
    exit_code = 0
    try:
        with contextlib.redirect_stdout(buf):
            runpy.run_path(f"{demo}.py", run_name="__main__")
    except SystemExit as e:  # build_benchmark / parse_benchmark call sys.exit(...)
        code = e.code
        exit_code = 0 if code is None else (code if isinstance(code, int) else 1)
    checks = []
    for line in buf.getvalue().splitlines():
        m = _LINE.match(line)
        if not m:
            continue
        ok = m.group(1) == "PASS"
        rest = m.group(2)
        name = rest.split("  — ", 1)[0].strip()
        checks.append([name, ok])
    return {"exit": exit_code, "checks": checks}


def main(argv):
    warehouse = argv[1]
    demos = argv[2:]
    os.environ["COLUMNA_BENCH_WAREHOUSE"] = warehouse
    out = {}
    for demo in demos:
        out[demo] = run_one(demo)
    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv)

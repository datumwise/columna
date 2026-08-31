#!/usr/bin/env python3
"""Plan every Frame-QL Manual example and report its plan-time disposition (Mission B, probe mode).

This is the reconnaissance half of the upgraded gate: it establishes WHAT the shipped planner does
with each documented example, so the contradictions can be adjudicated before any expectation is
enrolled. It asserts nothing and fails nothing.

Run: python docs/tools/manual_plan_probe.py [--verbose]
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys

import duckdb

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "manual_fixtures"))

from columna_core import ManifoldServer                       # noqa: E402
from columna_core.connector import DuckDBConnector            # noqa: E402
from columna_core.disclosure_wire import wire_frame           # noqa: E402
from columna_core.envelope import parse_statement             # noqa: E402
from columna_core.parser import parse_manifold                # noqa: E402
from manual_world import build                                # noqa: E402

_spec = importlib.util.spec_from_file_location("mgate", HERE / "check_manual_frameql.py")
_g = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_g)

FIXTURES = HERE / "manual_fixtures"
#: Manual manifold name -> fixture. `retail`/`retail_manifold` are the Manual's own aliases for the
#: same worked schema; both map to the finance fixture, which carries their vocabulary.
BINDING = {
    None: "finance_manifold",
    "finance_manifold": "finance_manifold",
    "product_manifold": "product_manifold",
    "retail": "retail_manifold",
    "retail_manifold": "retail_manifold",
}


def servers():
    con = build(duckdb.connect())
    out = {}
    for name in ("finance_manifold", "product_manifold", "retail_manifold"):
        m = parse_manifold((FIXTURES / f"{name}.cml").read_text())
        srv = ManifoldServer(m, connector=DuckDBConnector(con))
        srv.publish()
        out[name] = srv
    return out


def sections(text: str):
    """(line, heading, mark) for every heading, so an example can be told which section owns it and
    whether that section is marked [ROADMAP]/[SCHEDULED] — the Manual's OWN declaration of what is
    not shipped, and therefore the only honest expectation source for a documented-not-to-run form."""
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.startswith("#"):
            mark = None
            for m in ("[ROADMAP", "[SCHEDULED"):
                if m in ln:
                    mark = m.strip("[")
            out.append((i, ln.lstrip("# ").strip(), mark))
    return out


def owning_section(secs, lineno):
    cur = (0, "(preamble)", None)
    for s in secs:
        if s[0] <= lineno:
            cur = s
        else:
            break
    return cur


def examples(text):
    out = []
    for lineno, info, body in _g._fenced_blocks(text):
        stmts = _g._statements(body)
        isf = info == "frameql" or (info == "" and stmts and _g._STMT_START.match(stmts[0]))
        kind = "frameql" if isf else ("illformed" if info == "frameql-illformed" else None)
        if not kind:
            continue
        for s in stmts:
            out.append((lineno, kind, s))
    return out


def disposition(srvs, stmt_text):
    """(outcome, reason, detail) at PLAN time — zero backend fetches. Syntax failures ride their own
    channel (EnvelopeSyntaxError / FrameQLSyntaxError), exactly as the server surfaces them, and are
    reported as such rather than being flattened into an outcome they never reach."""
    try:
        st = parse_statement(stmt_text)
    except Exception as e:
        return ("parse-error", type(e).__name__, str(e))
    srv = srvs[BINDING.get(st.from_manifold, "finance_manifold")]
    try:
        fr = srv.planner.plan_statement(st)
    except Exception as e:
        return ("plan-raise", type(e).__name__, str(e))
    w = wire_frame(fr, executed=False)
    worst, reason, detail = w["outcome"], None, None
    for c in w["columns"]:
        nr = c.get("no_result") or {}
        if nr.get("reason"):
            reason, detail = nr["reason"], nr.get("detail")
            break
    return (worst, reason, detail)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    text = _g.MANUAL.read_text()
    secs = sections(text)
    srvs = servers()

    print(f"{'#':>3}  {'L':>5}  {'section':38}  {'mark':9}  {'outcome':11}  reason")
    print("-" * 118)
    rows = []
    for n, (lineno, kind, stmt) in enumerate(examples(text), 1):
        _, head, mark = owning_section(secs, lineno)
        out, reason, detail = disposition(srvs, stmt)
        rows.append((n, lineno, head, mark, kind, out, reason, detail, stmt))
        print(f"{n:>3}  {lineno:>5}  {head[:38]:38}  {str(mark or ''):9}  {out:11}  {reason or ''}")
        if args.verbose and detail:
            print(f"{'':>62}{detail[:110]}")
    print("-" * 118)
    from collections import Counter
    print("outcomes:", dict(Counter(r[5] for r in rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

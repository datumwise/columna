#!/usr/bin/env python3
"""The Afternoon's five executable expressions — the literal page gate.

WHAT THIS IS. *The Theory of Data in One Afternoon* (v0.13, ledger CT-1) prints five executable
Frame-QL statements. This script runs **those exact statements**, byte-for-byte as the page prints
them, against the governed Afternoon fixture, and asserts the verdict each one earns. It is the gate
that lets us say the essay is true of the system rather than about it.

    python scripts/afternoon_five.py                      # source mode (default)
    python scripts/afternoon_five.py --engine installed   # against the shipped distribution
    python scripts/afternoon_five.py --json               # machine-readable

THE STATEMENT PARSER, NOT THE BUILDER API. Beat 2 pins a composite input anchor with braces —
`avg(revenue @ {order})` — which only the statement path converts; the low-level `.column()` builder
rejects it as an illegal construct. A gate that quietly rewrote the page's syntax into something the
builder accepts would be certifying a DIFFERENT question than the one a reader can copy off the page,
so every beat goes through `parse_statement` exactly as printed.

ENGINE PROVENANCE IS EXPLICIT, NEVER INFERRED (Huayin, 2026-08-20). The mode is chosen by flag, not
by sniffing whether `columna_core` happens to be importable:

  · `--engine source`    — deliberately prepend the branch repository's `src` and run the BRANCH
                           engine. This is release-candidate certification: what CI runs on a PR.
  · `--engine installed` — never prepend repository `src`; resolve the INSTALLED distribution, and
                           FAIL if what resolves is the repository source tree. This is what closes
                           the final shipped-package gate after 0.15.0 is on PyPI.

Both modes print the resolved `columna_core.__file__` and version before running a single beat,
because a gate that cannot say which engine it exercised cannot certify anything. The controlled
fixture stays in the repository in both modes — it is governed DATA, not the artifact under test.
The invariant is: *same governed fixture, explicit and attestable engine provenance.*

WHAT THIS IS NOT. The generated-family / laundering matrix — every spelling of "sum a stock across
calendar" — lives in `packages/columna-core/tests/test_generated_family_law.py` (55 cases) and is the
evidence for DG-2 forward invariant 5. This script no longer duplicates it.
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_CORE = os.path.join(_ROOT, "packages", "columna-core")
_FIXTURES = os.path.join(_CORE, "tests", "fixtures")
_SRC = os.path.join(_CORE, "src")

# The five, exactly as *The Theory of Data in One Afternoon* v0.13 prints them. The statements are
# byte-identical across v0.12-final and v0.13 — that revision advanced one reading-list DOI and
# nothing executable — so this list did not move when the artifact did. It is now hosted in the
# repository at apps/website/src/content/corpus/theory_of_data_in_one_afternoon_v0_13.md and
# rendered at /start-here, which is what closed CT-1's site item.
# (beat, statement, expected outcome, expected reason, expected input-anchor alternatives)
FIVE = [
    ("1 · the flow, at its own grain",
     "SELECT revenue AT {store, month}",
     "serve", None, None,
     "A flow summed along calendar. Lawful, unremarkable, and the control the other four are read "
     "against: the system is not simply cautious."),
    ("2 · the flow, per order, coarsened",
     "SELECT avg(revenue @ {order}) AT {region, quarter}",
     "serve", None, None,
     "An inline average with its input anchor PINNED to order, reduced across two lineages at once. "
     "Pinning is what makes it a definite quantity."),
    ("3 · the flow, coarsened both ways",
     "SELECT revenue AT {region, quarter}",
     "serve", None, None,
     "The same measure carried up both hierarchies. Transport, not permission."),
    ("4 · the ask with two lawful readings",
     "SELECT max(revenue) AT {region, month}",
     "clarify", "input_anchor_ambiguous", ("day", "store"),
     "No input anchor pinned, and MORE THAN ONE lawful grain to resolve at. Clarify is for unresolved "
     "choice among lawful meanings — the system asks rather than guessing."),
    ("5 · the burn",
     "SELECT sum(on_hand) AT {store, month}",
     "refuse", "blocked_reduction", None,
     "Dana's ask: sum the stock into months. No lawful temporal-sum family exists, in any spelling. "
     "Refuse, with the reason and the lawful neighbours."),
]


def resolve_engine(mode: str) -> dict:
    """Put the requested engine on the path, import it, and return its attested provenance.

    Source mode prepends the branch `src`. Installed mode prepends nothing and REFUSES a
    repository-source resolution — the failure this exists to prevent is a gate that prints green
    against the branch while reporting itself as the shipped-package result.
    """
    if mode == "source":
        if _SRC not in sys.path:
            sys.path.insert(0, _SRC)
    # The fixture is governed DATA and is repository-resident in BOTH modes, by ruling.
    if _FIXTURES not in sys.path:
        sys.path.insert(0, _FIXTURES)

    import columna_core

    path = os.path.abspath(columna_core.__file__)
    try:
        from importlib.metadata import version as _dist_version
        dist = _dist_version("columna-core")
    except Exception:                                        # pragma: no cover - no metadata present
        dist = None
    attr = getattr(columna_core, "__version__", None)
    from_repo = os.path.commonpath([path, os.path.abspath(_SRC)]) == os.path.abspath(_SRC)

    prov = {"mode": mode, "file": path, "dist_version": dist, "attr_version": attr,
            "from_repository_source": from_repo}

    if mode == "installed" and from_repo:
        raise SystemExit(
            "FAIL — --engine installed resolved the REPOSITORY SOURCE TREE, not an installed "
            f"distribution.\n  columna_core.__file__ = {path}\n  repository src        = "
            f"{os.path.abspath(_SRC)}\n"
            "The shipped-package gate must exercise the shipped artifact. Run it from a directory "
            "outside the repository, or in a venv where columna-core is installed from PyPI and the "
            "repository src is not on sys.path / PYTHONPATH."
        )
    return prov


def build():
    """The governed Afternoon fixture, published on the resolved engine."""
    import duckdb

    import afternoon_world
    from columna_core import DuckDBConnector, ManifoldServer
    from columna_core.parser import parse_file

    m = parse_file(os.path.join(_FIXTURES, "afternoon.cml"))
    srv = ManifoldServer(m, DuckDBConnector(afternoon_world.build(duckdb.connect())))
    srv.publish()
    return srv


def run(srv, statement):
    """One beat, through the STATEMENT path — the exact syntax the page prints."""
    from columna_core.disclosure_wire import wire_frame
    from columna_core.envelope import parse_statement

    w = wire_frame(srv.planner.run_statement(parse_statement(statement)))
    col = w["columns"][0]
    nr = col.get("no_result") or {}
    values = col.get("values") or []
    return {
        "statement": statement,
        "outcome": w["outcome"],
        "reason": nr.get("reason"),
        "detail": nr.get("detail"),
        "alternatives": [a.get("description") for a in (nr.get("alternatives") or [])],
        "rows": len(values),
        "sample": [{k: v for k, v in row.items()} for row in values[:2]],
    }


def _pinned_levels(alternatives) -> tuple:
    """The levels an `input_anchor_ambiguous` clarify offers, read out of its own alternative text."""
    out = []
    for a in alternatives:
        if "pin the input anchor to '" in a:
            out.append(a.split("pin the input anchor to '", 1)[1].split("'", 1)[0])
    return tuple(sorted(out))


def judge(beat, result, expect_outcome, expect_reason, expect_alts):
    """Every failure this gate can report, named. Returns a list of complaints (empty == pass)."""
    bad = []
    if result["outcome"] != expect_outcome:
        bad.append(f"outcome {result['outcome']!r}, expected {expect_outcome!r}")
    if expect_reason is not None and result["reason"] != expect_reason:
        bad.append(f"reason {result['reason']!r}, expected {expect_reason!r}")
    if expect_alts is not None:
        got = _pinned_levels(result["alternatives"])
        if got != tuple(sorted(expect_alts)):
            bad.append(f"lawful alternatives {got}, expected {tuple(sorted(expect_alts))}")
    if expect_outcome in ("clarify", "refuse"):
        # The load-bearing half of the ruling: a no-result mood must return NO VALUES. A refusal that
        # still handed back numbers would be the Afternoon's whole complaint, wearing a caveat.
        if result["rows"]:
            bad.append(f"returned {result['rows']} value(s) — a {expect_outcome} must return none")
        if not result["reason"]:
            bad.append("no reason given")
    if expect_outcome == "serve" and not result["rows"]:
        bad.append("served no rows")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--engine", choices=("source", "installed"), default="source",
                    help="which columna-core to certify: the branch repository ('source', the "
                         "release-candidate mode CI runs) or the installed distribution "
                         "('installed', which closes the shipped-package gate)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    prov = resolve_engine(args.engine)
    srv = build()

    out = []
    for beat, statement, outcome, reason, alts, note in FIVE:
        r = run(srv, statement)
        r["beat"], r["note"] = beat, note
        r["expected"] = {"outcome": outcome, "reason": reason,
                         "alternatives": list(alts) if alts else None}
        r["complaints"] = judge(beat, r, outcome, reason, alts)
        r["ok"] = not r["complaints"]
        out.append(r)

    failed = [r for r in out if not r["ok"]]

    if args.json:
        print(json.dumps({"gate": "afternoon_five", "source": "Afternoon v0.13",
                          "fixture": "afternoon", "engine": prov,
                          "beats": out, "passed": len(out) - len(failed), "total": len(out)},
                         indent=2))
        return 1 if failed else 0

    print("The Afternoon, five expressions — the literal v0.13 page gate")
    print(f"  engine mode : {prov['mode']}")
    print(f"  engine file : {prov['file']}")
    print(f"  version     : {prov['dist_version'] or prov['attr_version'] or '(unknown)'}"
          + ("   [REPOSITORY SOURCE]" if prov["from_repository_source"] else "   [installed]"))
    print(f"  fixture     : {os.path.join(_FIXTURES, 'afternoon.cml')}\n")

    for r in out:
        print(f"{r['beat']}")
        print(f"    {r['statement']}")
        print(f"    {r['note']}")
        line = f"    -> {r['outcome'].upper()}"
        if r["reason"]:
            line += f"  ({r['reason']})"
        line += f"   {r['rows']} row(s)"
        print(line)
        for a in r["alternatives"]:
            print(f"       lawful: {a}")
        if r["sample"]:
            print(f"       sample: {r['sample']}")
        for c in r["complaints"]:
            print(f"       ✗ {c}")
        print()

    if failed:
        print(f"FAIL — {len(failed)} of {len(out)} beats do not match Afternoon v0.13: "
              f"{', '.join(r['beat'] for r in failed)}")
        return 1
    print(f"OK — all {len(out)} beats match Afternoon v0.13, "
          f"certified against the {prov['mode']} engine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

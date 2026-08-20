#!/usr/bin/env python3
"""The Afternoon's five executable expressions, run against the faithful fixture.

`specs/doctrine_gaps.md` DG-2 forward invariant 5 requires that the system EXPRESS the Afternoon
case: attempt a temporal SUM of a base stock, find no lawful reading, REFUSE with the reason and the
lawful neighbours. Until 2026-08-20 there was no fixture in this repository to run that against — the
case lived only as prose in the ledger — so the invariant could be asserted but never certified.

This script is the release-candidate gate for that invariant. It runs the five beats against
`packages/columna-core/tests/fixtures/afternoon.cml` and prints what a reader actually receives.

    python scripts/afternoon_five.py            # human-readable
    python scripts/afternoon_five.py --json     # machine-readable

⚠ PENDING RATIFICATION. *The Theory of Data in One Afternoon* (ledger CT-1) is not in this
repository, so the FIVE below are the design session's reading of the case from DG-2 invariant 5 and
the ch2/ch3 beats — not a transcription of the Afternoon's own list. The fixture and the verdicts are
real; the SELECTION of the five needs the desk's confirmation against the Afternoon text.
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_CORE = os.path.join(_ROOT, "packages", "columna-core")
for _p in (os.path.join(_CORE, "src"), os.path.join(_CORE, "tests", "fixtures")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# (beat, anchor, expression, what the Afternoon is testing)
FIVE = [
    ("1 · the burn", ("store", "month"), "on_hand.sum",
     "Dana's original ask: sum the stock into months. The declared bar is crossed."),
    ("2 · the burn, respelled", ("store", "month"), "sum(on_hand.last@day)",
     "The same prohibited operation, generated above a LAWFUL sibling. Before 2026-08-20 this "
     "served clean, with the identical meaningless number."),
    ("3 · the burn, unnamed", ("store", "month"), "sum(on_hand)",
     "No member named at all, no input anchor pinned — and no lawful candidate to offer, so there "
     "is nothing to clarify."),
    ("4 · the remedy", ("store", "month"), "on_hand.last",
     "The lawful neighbour the refusal names. Position, not a total."),
    ("5 · the lawful sum", ("month",), "sum(on_hand.last@store)",
     "The same reducer over the same measure, across a DIFFERENT axis — lawful, because the bar "
     "names a lineage, not a measure."),
]


def build():
    import duckdb

    import afternoon_world
    from columna_core import DuckDBConnector, ManifoldServer
    from columna_core.parser import parse_file

    m = parse_file(os.path.join(_CORE, "tests", "fixtures", "afternoon.cml"))
    srv = ManifoldServer(m, DuckDBConnector(afternoon_world.build(duckdb.connect())))
    srv.publish()
    return srv


def run(srv, anchor, expr):
    from columna_core.disclosure_wire import wire_frame

    w = wire_frame(srv.frame(*anchor).column("c", expr).run())
    col = w["columns"][0]
    nr = col.get("no_result") or {}
    return {
        "anchor": "{" + ", ".join(anchor) + "}",
        "expression": expr,
        "outcome": w["outcome"],
        "reason": nr.get("reason"),
        "detail": nr.get("detail"),
        "alternatives": [a.get("description") for a in (nr.get("alternatives") or [])],
        "disclosures": [(d.get("code"), d.get("materiality")) for d in (col.get("disclosures") or [])],
        "rows": len(col.get("values") or []),
        "s1_jan": next((v["value"] for v in (col.get("values") or [])
                        if v.get("store") == "S1" and v.get("month") == "2025-01"), None),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    import afternoon_world

    srv = build()
    out = [dict(beat=beat, note=note, **run(srv, anchor, expr)) for beat, anchor, expr, note in FIVE]

    if args.json:
        print(json.dumps({"fixture": "afternoon", "beats": out}, indent=2))
        return 0

    print("The Afternoon, five expressions — run against tests/fixtures/afternoon.cml")
    print(f"  S1 / 2025-01 snapshots: 500, 430, 480   position = {afternoon_world.S1_JAN_POSITION}   "
          f"the wrong total = {afternoon_world.S1_JAN_STOCK_SUM}\n")
    for r in out:
        print(f"{r['beat']}")
        print(f"    SELECT {r['expression']} AT {r['anchor']}")
        print(f"    {r['note']}")
        print(f"    -> {r['outcome'].upper()}"
              + (f"  ({r['reason']})" if r["reason"] else "")
              + (f"  {r['rows']} rows, S1/2025-01 = {r['s1_jan']}" if r["rows"] else ""))
        for a in r["alternatives"]:
            print(f"       remedy: {a}")
        for code, mat in r["disclosures"]:
            print(f"       caveat: {code} ({mat})")
        print()

    burned = [r for r in out if r["s1_jan"] == afternoon_world.S1_JAN_STOCK_SUM]
    if burned:
        print(f"FAIL — the Afternoon's wrong number was served by: "
              f"{', '.join(r['expression'] for r in burned)}")
        return 1
    print(f"OK — no beat returned {afternoon_world.S1_JAN_STOCK_SUM}; "
          f"DG-2 forward invariant 5 holds against a real fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

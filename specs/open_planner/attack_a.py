#!/usr/bin/env python3
"""Attack A v2 — the Class A base case: maximal plan overlap, ONE differing field.

    python specs/open_planner/attack_a.py specs/open_planner/fixtures/

RESEARCH INSTRUMENTATION ONLY. Reads the shipped packages; modifies nothing.

THE EXHIBIT (desk, A1 v0.2). Two plans that are identical in every structural respect:

    same universe (transaction) · same CARVE · same CROSS (product<->category, face `split`)
    · same REDUCE (@ category)

and differ in exactly ONE field: `COLUMN.measure_ref`.

    ASKED     SELECT revenue    AT {category.split}
    SUBSTITUTED SELECT units_sold AT {category.split}

Both are LAWFUL. Both SERVE. Nothing in the lawfulness obligation separates them, because nothing is
unlawful about either — the substituted plan is a perfect answer to a *different servable ask*. Only
`plan |= ask` separates them, and it does so with a single rule binding `COLUMN.measure_ref` to the
ask's measure atom.

WHY MAXIMAL OVERLAP IS THE POINT. Class A is the base case any obligation language must kill in one
rule. The cleanest possible base case is therefore the pair with the SMALLEST possible difference:
if the two plans differed in several fields, a checker could pass by catching the wrong one and we
would learn nothing about which rule did the work.

THE LAWFULNESS EXHIBIT, frozen beside it. A1 v0.1's original Attack A named a plan that does not
compose against the shipped model at all — CARVE(inventory) reaching `category`. `inventory` is
`store * day`; it has no product axis, so there is no route to category. The engine refuses it as
OUT OF DOMAIN, and it never reaches a faithfulness question. That transcript is kept because the
contrast is the whole lesson:

    the out-of-domain plan  -> killed by LAWFULNESS, loudly, before faithfulness is consulted
    the substituted plan    -> passes lawfulness completely, and only FAITHFULNESS catches it

Two obligations, two different deaths. (v0.1's misdescription was finding F3; the desk owned and
patched it in A1 v0.2. A residue: v0.2's Attack A line names the measure `units`, while the shipped
name is `units_sold` — recorded here as F3b, same disease, harmless.)
"""

from __future__ import annotations

import json
import pathlib
import sys

ASKED = "SELECT revenue AT {category.split}"
SUBSTITUTED = "SELECT units_sold AT {category.split}"
OUT_OF_DOMAIN = "SELECT stock.sum AT {category}"          # A1 v0.1's broken plan, kept as the exhibit


def capture(store, frameql: str) -> dict:
    from columna_server import tools as T
    wire = T.query(store, "cascadia", frameql)
    col = (wire.get("columns") or [{}])[0]
    return {
        "frameql": frameql,
        "outcome": wire.get("outcome"),
        "population": col.get("population"),
        "values": {v["category.split"]: v["value"] for v in (col.get("values") or [])}
        if col.get("values") else None,
        "no_result": col.get("no_result"),
        "error": wire.get("error"),
        "disclosures": col.get("disclosures"),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    outdir = pathlib.Path(argv[1])
    outdir.mkdir(parents=True, exist_ok=True)

    from columna_server.demo import demo_store
    store = demo_store()

    asked = capture(store, ASKED)
    subst = capture(store, SUBSTITUTED)
    ood = capture(store, OUT_OF_DOMAIN)

    payload = {
        "class_a_pair": {
            "asked": asked,
            "substituted": subst,
            "differing_field": "COLUMN.measure_ref",
            "identical_fields": ["universe (transaction)", "CARVE", "CROSS(product<->category, split)",
                                 "REDUCE(@ category)", "ANCHOR(category.split)"],
            "both_lawful": asked["outcome"] in ("serve", "disclose")
            and subst["outcome"] in ("serve", "disclose"),
        },
        "lawfulness_exhibit_out_of_domain": ood,
        "the_lesson": ("the out-of-domain plan is killed by LAWFULNESS before faithfulness is "
                       "consulted; the substituted plan passes lawfulness completely and only "
                       "FAITHFULNESS catches it. Two obligations, two different deaths."),
        "f3b": ("A1 v0.2's Attack A line names the measure `units`; the shipped name is "
                "`units_sold` (`SELECT units AT {category.split}` -> unknown column). Same "
                "written-from-recall disease as F3, harmless, recorded not absorbed."),
    }
    (outdir / "attack_a_class_a.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {outdir / 'attack_a_class_a.json'}")

    print()
    print("CLASS A — one differing field (COLUMN.measure_ref); everything else identical")
    print("  asked       %-38s -> %s" % (ASKED, asked["outcome"]))
    print("  substituted %-38s -> %s" % (SUBSTITUTED, subst["outcome"]))
    print("  both lawful, both served:", payload["class_a_pair"]["both_lawful"])
    print()
    print("  category   asked(revenue)     substituted(units_sold)")
    for k in sorted(asked["values"] or {})[:5]:
        print("  %-9s %16.4f %22.4f" % (k, asked["values"][k], (subst["values"] or {}).get(k, float("nan"))))
    print()
    print("LAWFULNESS EXHIBIT (A1 v0.1's broken plan, kept):")
    print("  %-42s -> %s" % (OUT_OF_DOMAIN, ood["outcome"]))
    print("  reason:", ((ood["no_result"] or {}).get("detail") or "")[:120])

    ok = payload["class_a_pair"]["both_lawful"] and ood["outcome"] == "refuse"
    print()
    print("EXHIBIT VALID:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

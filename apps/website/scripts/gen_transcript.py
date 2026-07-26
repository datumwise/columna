#!/usr/bin/env python3
"""Integrity generator — the recorded transcript, built by running the SHIPPED package.

Run against columna installed from PyPI. Emits JSON on stdout: the four pinned seeded queries,
the clarify round-trip (both alternatives, whatever they truly resolve to), the fool-it ASK, and
a `demo --play` cross-check — every payload produced by the shipped engine, none hand-written.
Exits non-zero on any failure so the build fails closed (never ships a stale or fake transcript).

Pins verified 2026-07-11 against columna-core 0.7.8 / columna-server 0.1.0.
"""
import json
import sys
from datetime import datetime, timezone
from importlib.metadata import version

from columna_server import tools as T
from columna_server.demo import (demo_store, DEMO_MANIFOLD_ID as MID,
                                 CLARIFY_Q, REFUSE_Q, DISCLOSE_Q, SERVE_Q)

# Anchored at `region` so the full wire stays small and legible (the exhibit *shows* the JSON):
# same measures, same mood, same material caveat — just few rows instead of thousands.
# CP-3 S-2 (Huayin 2026-07-17): the four-mood exhibit mirrors the shipped `demo --play` wheel tour on the
# ratified §2c exemplars. The old cross-universe wedge (S-1) is KILLED — a category error now — and the
# demo's own declared metrics wear their verdicts in the Explorer instead of one bespoke mascot ratio.
# The four-mood queries are IMPORTED from the shipped demo (single source of truth — they migrate to the
# envelope with the package, so the transcript can never drift from what `demo --play` runs). 0.9.0: they
# are `SELECT … AT {…}`; the terse form is retired.
FOOL       = "SELECT profit_margin AT {cal.month}"   # a plausible column no one declared -> error/ASK

SEEDED = {
    "clarify":  {"frameql": CLARIFY_Q,  "universe": None, "intended": "clarify"},
    "refuse":   {"frameql": REFUSE_Q,   "universe": None, "intended": "refuse"},
    "disclose": {"frameql": DISCLOSE_Q, "universe": None, "intended": "disclose"},
    "serve":    {"frameql": SERVE_Q,    "universe": None, "intended": "serve"},
}


def run(store, fq):                          # 0.9.0: universe is structural (§2c), no longer a query arg
    return T.query(store, MID, fq)


def build_describe(store, dm):
    """Capture describe_manifold + describe_measure and DERIVE each family member's legal cone
    (may-be-asked-at grains, and barred rollups with the blocking lineage) STRUCTURALLY from the
    edges + per-member blocked_lineages. Nothing here is hand-written: cone membership follows from
    the wire; only the human LABELS live in the reviewed strings file (ruling e-1). Per-member cones
    (ruling e-2)."""
    edges = [(e["frm"], e["to"], e["lineage"]) for e in dm["edges"]]
    measures = {}
    for mc in dm["measures"]:
        name = mc["name"]
        d = T.describe_measure(store, MID, name)
        grain = list(d["v_anchor"]["grain"])
        gset = set(grain)
        members = {}
        for member, anc in d["member_anchors"].items():
            blocked = set(anc["blocked_lineages"])
            reachable, barred = [], {}
            for frm, to, lineage in edges:
                if frm in gset:
                    if lineage in blocked:
                        barred.setdefault(lineage, []).append(to)
                    else:
                        reachable.append(to)
            members[member] = {
                "blocked_lineages": sorted(blocked),
                "is_monoid": anc.get("is_monoid"),
                "order_by": anc.get("order_by"),
                # the legal cone: base grains you may anchor at + rollups reachable via non-blocked lineages
                "may_be_asked_at": grain + [t for t in reachable if t not in gset],
                "barred": [{"lineage": lin, "targets": sorted(set(t))} for lin, t in sorted(barred.items())],
            }
        measures[name] = {
            "name": name,
            "universe": d["universe"],
            "dtype": d["dtype"],
            "family_members": list(d["family"]["members"]),
            "reducer_kind": d["family"]["reducer_kind"],
            "grain": grain,
            "provenance": d["provenance"]["measure"],
            "members": members,
        }
    return {
        "manifold": {
            "id": MID,
            "universes": [{"name": u["name"], "base_dimensions": u["base_dimensions"],
                           "predicate": u["predicate"]} for u in dm["universes"]],
            "edges": [{"frm": f, "to": t, "lineage": l} for f, t, l in edges],
            "measure_index": [m["name"] for m in dm["measures"]],
        },
        "measures": measures,
    }


def main() -> int:
    store = demo_store()

    seeded = {}
    for key, q in SEEDED.items():
        wire = run(store, q["frameql"])
        got = wire.get("outcome")
        if got != q["intended"]:
            print(
                f"INTEGRITY FAIL: seeded '{key}' expected outcome '{q['intended']}', got '{got}' "
                f"for {q['frameql']!r} universe={q['universe']!r}",
                file=sys.stderr,
            )
            return 1
        seeded[key] = {**q, "wire": wire}

    # clarify round-trip: the clarify (an inline reduction with no pinned input anchor) offers input-anchor
    # alternatives; replay each alternative's re-ask to capture what it truly resolves to. Defensive over
    # the alternative shape — replays any alt carrying a re-askable `apply.frameql`.
    roundtrip = {}
    for alt in seeded["clarify"]["wire"]["columns"][0].get("no_result", {}).get("alternatives", []):
        reask = (alt.get("apply") or {}).get("frameql")
        if reask:
            roundtrip[alt.get("token", reask)] = {"apply": alt["apply"], "wire": run(store, reask)}

    # fool-it: unknown measure -> error, plus the real measure index (describe touches no data)
    fool_wire = run(store, FOOL)
    describe = T.describe_manifold(store, MID)
    measure_index = [m.get("measure") or m.get("name") for m in describe.get("measures", [])]

    # demo --play cross-check: the four moods the shipped self-player emits (the wheel tour)
    play = [
        {"title": "clarify", "wire": run(store, CLARIFY_Q)},
        {"title": "refuse", "wire": run(store, REFUSE_Q)},
        {"title": "disclose", "wire": run(store, DISCLOSE_Q)},
        {"title": "serve", "wire": run(store, SERVE_Q)},
    ]

    # The UMBRELLA `columna` version (Huayin's version ruling, 2026-07-25). This is the release/install
    # number — what `pip install columna` gives — and the honest source for the homepage's "currently
    # at" and the Latest rail. It legitimately DIFFERS from columna_core after a data-only release:
    # columna and columna-server move, core does not (0.12.1 was exactly this). Reporting all three
    # makes the relationship visible instead of conflating them.
    #
    # FAILS CLOSED, and it has to. The first version of this caught the lookup and emitted null,
    # reasoning that "null is a loud signal, never a lie". It was not loud: the umbrella pin did not
    # ship with this generator, the lookup failed, meta carried null, the site fell back to
    # columna_core, and PROD SERVED 0.12.0 under ratified copy that says 0.12.1 — a silent degrade all
    # the way to production. A missing umbrella now fails the build, in the same fails-closed spirit as
    # every other wedge in this file: the site is structurally incapable of publishing a release number
    # it cannot read from an installed package.
    try:
        umbrella = version("columna")
    except Exception as e:
        print("transcript generation FAILED (fails closed): the umbrella `columna` package is not "
              "installed, so the release version cannot be read. The site publishes this as its "
              "\"currently at\" version and in the Latest rail, so it must come from a real installed "
              "package — never a fallback. Install it alongside the libs (the deploy pins "
              "columna==<version>; the branch job installs it editable). Underlying error: "
              f"{e!r}", file=sys.stderr)
        return 1
    out = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "contract_version": seeded["serve"]["wire"].get("contract_version"),
            "columna": umbrella,
            "columna_core": version("columna-core"),
            "columna_server": version("columna-server"),
            "manifold": MID,
            "note": "generated by running the shipped package; never hand-edited",
        },
        "seeded": seeded,
        "clarify_roundtrip": roundtrip,
        "fool_it": {"query": FOOL, "wire": fool_wire, "measure_index": measure_index},
        "play_crosscheck": play,
        # the Manifold Explorer's captured describe wire — cards render only from this. The old bespoke
        # derived-metric card is gone (S-1 killed); the Explorer badges the real declared objects via describe.
        "describe": build_describe(store, describe),
        # CP-3 C-3/S-4: the RAW describe_manifold (the C-1 shape) the portable Explorer component binds —
        # basis/absence, asserts, hierarchies, licenses, scope. The /explorer page mounts against this.
        "explorer_describe": describe,
    }
    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())

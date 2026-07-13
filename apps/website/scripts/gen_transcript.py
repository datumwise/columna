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
from columna_server.demo import demo_store, DEMO_MANIFOLD_ID as MID

# Anchored at `region` so the full wire stays small and legible (the exhibit *shows* the JSON):
# same measures, same mood, same material caveat — just few rows instead of thousands.
WEDGE = "sell_through_rate: revenue / level.last @ store, day"
SEPARATE = "revenue: revenue, inv: level.last @ region"
SERVE = "revenue @ region"
FOOL = "sell_through_rate @ store, day"  # a column label, not a measure -> error/ASK

SEEDED = {
    "clarify":  {"frameql": WEDGE,     "universe": None,           "intended": "clarify"},
    "refuse":   {"frameql": WEDGE,     "universe": "transactions", "intended": "refuse"},
    "disclose": {"frameql": SEPARATE,  "universe": None,           "intended": "disclose"},
    "serve":    {"frameql": SERVE,     "universe": None,           "intended": "serve"},
}


def run(store, fq, universe=None):
    return T.query(store, MID, fq, universe=universe)


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


def build_derived_metrics(seeded):
    """Capture the demo's DERIVED-METRIC definitions (v0.2 fork-4, Option B). sell_through_rate is
    an ad-hoc derived column defined inline in the seeded WEDGE query — the engine has NO describe
    object for it (describe_measure raises 'unknown measure'), so it is captured from the demo's own
    seeded-query definition, not from describe wire. Every field still traces to a captured artifact:
    the formula from the WEDGE definition, `demonstrates` from the REAL clarify wire the query
    produced, and `source` naming the provenance so a client can tell it apart from engine-describe
    cards (Huayin, 2026-07-13)."""
    name, expr = (s.strip() for s in WEDGE.split("@", 1)[0].split(":", 1))
    clarify_wire = seeded["clarify"]["wire"]
    reason = None
    for c in clarify_wire.get("columns", []):
        if c.get("no_result", {}).get("reason"):
            reason = c["no_result"]["reason"]
            break
    return {
        name: {
            "name": name,
            "formula": expr,                       # verbatim from the seeded-query definition
            "inputs": [                             # the operands — real, describe-able measures
                {"measure": "revenue"},
                {"measure": "level", "member": "last"},
            ],
            "demonstrates": reason,                 # the mood this metric's ambiguity produces (captured)
            "source": "demo seeded-query definition, captured at build",
        }
    }


def main() -> int:
    store = demo_store()

    seeded = {}
    for key, q in SEEDED.items():
        wire = run(store, q["frameql"], q["universe"])
        got = wire.get("outcome")
        if got != q["intended"]:
            print(
                f"INTEGRITY FAIL: seeded '{key}' expected outcome '{q['intended']}', got '{got}' "
                f"for {q['frameql']!r} universe={q['universe']!r}",
                file=sys.stderr,
            )
            return 1
        seeded[key] = {**q, "wire": wire}

    # clarify round-trip: capture what each offered alternative truly resolves to (both refuse —
    # each pin makes the other operand out-of-universe; the honest resolution is SEPARATE columns).
    roundtrip = {}
    for alt in seeded["clarify"]["wire"]["columns"][0]["no_result"]["alternatives"]:
        u = (alt.get("apply") or {}).get("universe")
        if u:
            roundtrip[alt["token"]] = {"apply": alt["apply"], "wire": run(store, WEDGE, u)}

    # fool-it: unknown measure -> error, plus the real measure index (describe touches no data)
    fool_wire = run(store, FOOL)
    describe = T.describe_manifold(store, MID)
    measure_index = [m.get("measure") or m.get("name") for m in describe.get("measures", [])]

    # demo --play cross-check: the three moods the shipped self-player emits
    play = [
        {"title": "clarify", "wire": run(store, WEDGE)},
        {"title": "refuse", "wire": run(store, WEDGE, "transactions")},
        {"title": "disclose", "wire": run(store, SEPARATE)},
    ]

    out = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "contract_version": seeded["serve"]["wire"].get("contract_version"),
            "columna_core": version("columna-core"),
            "columna_server": version("columna-server"),
            "manifold": MID,
            "note": "generated by running the shipped package; never hand-edited",
        },
        "seeded": seeded,
        "clarify_roundtrip": roundtrip,
        "fool_it": {"query": FOOL, "wire": fool_wire, "measure_index": measure_index},
        "play_crosscheck": play,
        # the Manifold Explorer's captured describe wire (tier 1) — cards render only from this
        "describe": {**build_describe(store, describe),
                     "derived_metrics": build_derived_metrics(seeded)},
    }
    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())

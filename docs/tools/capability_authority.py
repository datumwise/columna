#!/usr/bin/env python3
"""
capability_authority.py — the join across the three capability layers.

    canonical language standing   specs/frameql_capabilities.toml   AUTHORED  (what Frame-QL has)
            |
    profile realization standing  specs/profiles/*.toml             AUTHORED  (what a conforming
            |                                                                 implementation must realize)
            |
    current build realization     the installed package             MEASURED  (never authored)

WHY THREE AND NOT TWO. Collapsing profile into build would make whatever ships the definition of what
is required, which is exactly the conflation the layering exists to prevent: `in_core` or registry
membership quietly becoming canonical law, and a regression redefining the contract instead of
violating it. So a profile is AUTHORED and a build is MEASURED, and the gap between them is a
reportable fact rather than an impossibility.

TWO STANDING RULES (ruled Huayin, 2026-09-01):
  * A profile may ADD realization capability; it may NOT change the meaning of canonical Frame-QL.
    Naming a capability the canonical authority does not have is an error, not an extension.
  * A shipped build may CONFORM TO, LAG, or EXCEED a profile declaration; it does not silently
    redefine it. All three are visible; none of them edits the contract.

Measurement is deliberately structural — registry membership and `in_core` — and never a probe of
one fixture's numbers. Whether an example produces the right answer is the manual conformance gate's
question, asked against the Manual's own examples; this file answers only "does this build realize
this capability, and at what level".
"""
from __future__ import annotations
import pathlib
import sys

try:
    import tomllib
except ModuleNotFoundError:                                    # pragma: no cover
    import tomli as tomllib                                    # py<3.11

_SPECS = pathlib.Path(__file__).resolve().parents[2] / "specs"
CANONICAL = _SPECS / "frameql_capabilities.toml"
PROFILES = _SPECS / "profiles"

LEVELS = ("none", "plan", "execute")                           # ordered: lag/exceed is a comparison


def canonical_capabilities() -> dict:
    """id -> capability record, from the single canonical authority."""
    doc = tomllib.loads(CANONICAL.read_text())
    caps = {}
    for c in doc["capability"]:
        if c["id"] in caps:
            raise SystemExit(f"canonical authority: duplicate capability id {c['id']!r}")
        caps[c["id"]] = c
    return caps


def spelling_index(caps: dict) -> dict:
    """surface spelling -> capability id. The authority owns spellings, so a Manual name resolves
    here rather than through a second alias table kept in step by hand."""
    idx = {}
    for cid, c in caps.items():
        for s in c.get("spellings", [cid]):
            idx.setdefault(s, cid)
    return idx


def profile(name: str) -> dict:
    """A profile's EFFECTIVE realization contract: capability id -> level.

    A profile that `extends` another undertakes everything the base undertakes, plus its own `adds`.
    So the Platform Profile's effective contract is Core's contract plus its additions — an empty
    `adds` means "zero additional Frame-QL realization over Core", which is a contract, and is a
    different statement from "Platform realizes no Frame-QL"."""
    doc = tomllib.loads((PROFILES / f"{name}_profile.toml").read_text())
    out = {}
    base = doc.get("extends")
    if base:
        out.update(profile(base))
    for r in doc.get("realizes", []) + doc.get("adds", []):
        out[r["capability"]] = r.get("level", "none")
    return out


def profile_additions(name: str) -> dict:
    """Only what this profile ADDS over its base — what the profile itself declares."""
    doc = tomllib.loads((PROFILES / f"{name}_profile.toml").read_text())
    return {r["capability"]: r.get("level", "none")
            for r in doc.get("realizes", []) + doc.get("adds", [])}


def profile_errors(name: str, caps: dict) -> list:
    """A profile may not name a capability the canonical authority does not have — that would be a
    profile changing the language rather than realizing it. Checked against the profile's OWN
    declarations, so an inherited row is not reported twice."""
    return [f"profile '{name}' realizes '{cid}', which is not a canonical capability"
            for cid in profile_additions(name) if cid not in caps]


def measure_build(caps: dict) -> dict:
    """capability id -> realized level, MEASURED from the installed package.

    Structural, per the module note. A capability is realized when some declared spelling resolves in
    the shipped registry; `execute` when that operator is in Core, `plan` when it is registered as
    contract only. Predicate-position capabilities are measured against the planner's comparison
    table, which is EVIDENCE of Core realization and expressly not the semantic authority for the
    predicate vocabulary."""
    try:
        from columna_core.operators import REGISTRY, SERIES_REDUCERS
        from columna_core.planner import Planner
    except ImportError:                                        # pragma: no cover
        return {}
    predicate_realized = {sym for sym, _c in Planner._CMP} | {"and"}
    out = {}
    for cid, c in caps.items():
        level = "none"
        for s in c.get("spellings", [cid]):
            if c.get("position") == "predicate":
                if s.lower() in predicate_realized:
                    level = "execute"; break
                continue
            op = REGISTRY.get(s)
            if op is None:
                continue
            # `in_core` IS OVERLOADED, AND READING IT ALONE MISMEASURES (found in reconciliation).
            # It carries two different facts. For `rolling_*` it means the mechanics do not exist and
            # NOTHING executes. For `mean` it means only that Core does not serve the average as a
            # DECLARED MEASURE FAMILY MEMBER — the inline form `mean(x @ {a})` executes today, and the
            # registry entry exists so `(operator x lineage)` law has an address, not to gate
            # execution. Treating the flag as one axis would report `mean` as lagging a profile it
            # actually meets. `SERIES_REDUCERS` is the DECLARED inline-execution vocabulary, so it
            # answers the second case without guessing. That `in_core` needs this disambiguation at
            # all is reported as a canonical/profile question.
            if getattr(op, "in_core", True) or s in SERIES_REDUCERS:
                level = "execute"
            else:
                level = "plan"
            break
        out[cid] = level
    return out


def build_deltas(caps: dict, prof: dict, built: dict) -> list:
    """(capability, declared, measured, direction) wherever the build and the profile disagree.
    `lag` and `exceed` are both reportable; neither edits the contract."""
    rows = []
    for cid in caps:
        declared = prof.get(cid, "none")
        measured = built.get(cid, "none")
        if declared == measured:
            continue
        direction = "lag" if LEVELS.index(measured) < LEVELS.index(declared) else "exceed"
        rows.append((cid, declared, measured, direction))
    return rows


def standing_exceeded(caps: dict, prof: dict, built: dict) -> list:
    """(capability, profile_level, build_level) where realization runs ahead of CANONICAL STANDING.

    RULED 2026-09-01: A BUILD CANNOT PROMOTE LANGUAGE STANDING BY EXISTING, and a normative profile
    cannot silently turn a proposed construct into ratified Frame-QL. Core executes `cumsum`,
    `cummax`, `cummin`, `lag`, `lead` and `pct_change` today while sec.2.8 keeps scans proposed — so
    this state is real, it is legitimate, and the correct response is to keep it VISIBLE rather than
    to ratify the construct because something happens to run it. Ratification needs a semantic review
    of the canonical construct, which is a separate act."""
    rows = []
    for cid, c in caps.items():
        if c.get("standing") == "ratified":
            continue
        pl, bl = prof.get(cid, "none"), built.get(cid, "none")
        if pl != "none" or bl != "none":
            rows.append((cid, pl, bl))
    return sorted(rows)


def main() -> int:
    caps = canonical_capabilities()
    core = profile("core")
    built = measure_build(caps)
    platform = profile("platform")
    errs = profile_errors("core", caps) + profile_errors("platform", caps)
    # A PROFILE THAT EXTENDS ANOTHER MUST NOT DROP ITS BASE'S UNDERTAKINGS. Platform extends Core, so
    # its effective contract must cover Core's — an "extension" that realized less would be a
    # different contract wearing the word.
    for cid, level in core.items():
        if LEVELS.index(platform.get(cid, "none")) < LEVELS.index(level):
            errs.append(f"platform profile extends core but realizes '{cid}' at "
                        f"'{platform.get(cid, 'none')}' < core's '{level}'")
    deltas = build_deltas(caps, core, built)
    exceeded = standing_exceeded(caps, core, built)

    for e in errs:
        print(f"  ERROR {e}", file=sys.stderr)
    if deltas:
        print("\n=== BUILD vs CORE PROFILE ===", file=sys.stderr)
        print("    a build may conform to, lag, or exceed the profile; it never redefines it",
              file=sys.stderr)
        for cid, declared, measured, direction in deltas:
            print(f"  {direction.upper():7} {cid:18} profile={declared:8} build={measured}", file=sys.stderr)
    if exceeded:
        print(f"\n=== REALIZATION EXCEEDS CANONICAL STANDING ({len(exceeded)}) ===", file=sys.stderr)
        print("    these are realized while the LANGUAGE has not ratified them. Legitimate, and named"
              "\n    so it cannot become law by habit: a build cannot promote standing by existing,"
              "\n    and a profile cannot silently make a proposed construct ratified Frame-QL."
              "\n    Ratification is a separate semantic review of the canonical construct.",
              file=sys.stderr)
        for cid, pl, bl in exceeded:
            print(f"  {cid:16} standing=proposed  profile={pl:8} build={bl}", file=sys.stderr)

    ratified = sum(1 for c in caps.values() if c["standing"] == "ratified")
    adds = profile_additions("platform")
    print(f"platform profile: extends core, {len(adds)} addition(s) over it")
    print(f"capabilities: {len(caps)} canonical ({ratified} ratified) | core profile: "
          f"{sum(1 for v in core.values() if v != 'none')} realized | build deltas: {len(deltas)} "
          f"({sum(1 for d in deltas if d[3]=='lag')} lag, {sum(1 for d in deltas if d[3]=='exceed')} exceed)")
    return 1 if (errs or deltas) else 0


if __name__ == "__main__":
    sys.exit(main())

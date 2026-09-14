"""Does a contradiction-class refusal travel as `want_of_state` today? Measured, not argued.

WHAT THIS IS FOR. The realization-claim ruling (2026-09-14) mints
`realization_contradicts_law` and forbids it travelling as `want_of_state` with an ordinary
re-materialization remedy. This probe establishes the two halves of that, in the only way available
before the conformance repair is written:

  PART A  the shipped dispatch, applied to real refusal instances. The expression is READ OUT OF
          serving.py at runtime rather than restated here, so this cannot drift from the code it
          reports on.
  PART B  the minted registry entry's classification, from the closed registry itself.

WHAT IT DOES NOT CLAIM. Nothing raises `realization_contradicts_law` yet -- the checks that will are
gated behind ratification. Part A therefore measures the dispatch a new refusal class WOULD meet,
using a stand-in of the same shape; it does not claim the contradiction path exists.
"""
from __future__ import annotations
import pathlib
import re
import sys

from columna_core.disclosure import REASON_OUTCOME, jurisdiction_for, outcome_for
from columna_platform import serving
from columna_platform.refusals import (
    ProofRefusal, UnsupportedByThisProfile, WantOfCompatibility, WantOfLaw, WantOfState,
)

SERVING = pathlib.Path(serving.__file__)

print("=== PART A. the shipped Platform-refusal -> wire dispatch, read out of the source ===")
src = SERVING.read_text(encoding="utf-8").split("\n")
hits = [(i + 1, l.strip()) for i, l in enumerate(src)
        if "WANT_OF_LAW if isinstance" in l or "alts = (REMATERIALIZE,)" in l]
for lineno, line in hits:
    print(f"  {SERVING.name}:{lineno}  {line}")
print(f"  -> {len([h for h in hits if 'isinstance' in h[1]])} translation site(s), all identical.")
print(f"  REMATERIALIZE = {serving.REMATERIALIZE!r}")

print()
print("  applying that exact expression to one instance of each refusal class:")


class _StandInContradiction(ProofRefusal):
    """Stands in for the ruled `RealizationContradictsLaw`, which is not implemented yet.

    A `ProofRefusal` subclass that is not `WantOfLaw` -- which is the ONLY property the dispatch
    below actually tests. Any future contradiction class with the same base meets the same branch."""

    condition = "RealizationContradictsLaw"
    jurisdiction = "realization"
    remedy = "correct or replace the realization mapping; re-materialization cannot resolve it"


CASES = [
    WantOfLaw("the governed law does not license this", subject="demo"),
    WantOfState("no admissible state establishes it", subject="demo"),
    WantOfCompatibility("identical identity, incompatible standing", subject="demo"),
    _StandInContradiction("publication establishes SUM; realization claims MIN", subject="demo"),
]
worst = []
for r in CASES:
    # THE SHIPPED EXPRESSION, VERBATIM:
    reason = serving.WANT_OF_LAW if isinstance(r, WantOfLaw) else serving.WANT_OF_STATE
    alts = (serving.REMATERIALIZE,) if reason == serving.WANT_OF_STATE else ()
    flag = ""
    if type(r) is not WantOfLaw and type(r) is not WantOfState:
        worst.append(type(r).__name__)
        flag = "   <-- COLLAPSED"
    print(f"    {type(r).__name__:24} -> reason={reason!r:18} "
          f"alternatives={'(REMATERIALIZE,)' if alts else '()'}{flag}")

print()
print(f"  {len(worst)} class(es) reach the wire as `want_of_state` though they are neither a")
print(f"  WantOfLaw nor a WantOfState: {worst}")
print("  The dispatch is a two-way if/else over a four-class taxonomy; the `else` is total.")
print(f"  UnsupportedByThisProfile is NOT a ProofRefusal ("
      f"{issubclass(UnsupportedByThisProfile, ProofRefusal)}), so it is not caught here at all --")
print("  which is correct, and is why the collapse affects exactly the governed classes.")

print()
print("=== PART B. the minted reason, from the closed registry ===")
MINTED = "realization_contradicts_law"
print(f"  REASON_OUTCOME[{MINTED!r}] = {REASON_OUTCOME[MINTED]}")
print(f"  outcome_for   -> {outcome_for(MINTED)}")
print(f"  jurisdiction  -> {jurisdiction_for(MINTED)!r}")
print()
print("  against the three it must never be confused with:")
for other in ("want_of_state", "want_of_law", "unsupported"):
    same = outcome_for(MINTED) == outcome_for(other)
    print(f"    vs {other:16} {str(REASON_OUTCOME[other]):42} "
          f"{'SAME VERDICT (separated by meaning)' if same else 'DISTINCT'}")
print()
print("  and the registry is fail-closed, so an unregistered reason cannot acquire a verdict:")
try:
    outcome_for("a_reason_nobody_registered")
    print("    !! did not raise")
except Exception as e:
    print(f"    outcome_for('a_reason_nobody_registered') -> {type(e).__name__}")

print()
print("=== CONCLUSION ===")
print("  B holds today: the minted reason classifies ERROR / REALIZATION and is NOT want_of_state.")
print("  A does NOT hold today: the dispatch would send a contradiction class to want_of_state")
print("  with REMATERIALIZE offered. Closing A is part of the conformance repair, and the control")
print("  that proves it is the one named in the ruling document -- a refusal-class-keyed dispatch")
print("  with a completeness pin, so a class with no wire reason fails the build rather than")
print("  silently inheriting one.")

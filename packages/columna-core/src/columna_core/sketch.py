"""
columna_core.sketch — the HLLSketch datatype + its three operators + the witness store.

THE CASE STUDY. A custom logical type (`HLLSketch(p)`) and three custom operators register
in the umbrella and the engine composes them; the *planner is never touched*. The distinct
count — sterile as a scalar — becomes a FERTILE family because its carrier (an HLL sketch) is
a monoid under union. The three operators are the deliver / combine / project of that carrier:

    hll_count(col @ a) @ b   REDUCER, witness=sketch   any        -> HLLSketch(p)   (deliver)
    hll_merge                REDUCER, monoid union      HLLSketch  -> HLLSketch(p)   (combine)
    hll_estimate(sk @ a) @ a MAP                        HLLSketch  -> Int64          (project)

`distinct` is the friendly default-family spelling that the engine composes from these three.

Precision is part of the TYPE: HLLSketch(12) and HLLSketch(14) are different types and are NOT
mergeable — merging mismatched precisions is a type error. (The hash + register width must match
for a union to mean anything; making precision type-identity turns that into a static check.)

The WITNESS is STORED, not cached:
  • built EAGERLY at publish (one base scan per base grain), never lazily on a query;
  • keyed by GRAIN (measure, member, base_level) — one artifact serves every coarser anchor
    by merge, along any rollup path;
  • LOAD-BEARING — `hll_merge` reads it; it is the fertile carrier, not an optimization. Drop it
    and a coarse distinct-count can only be had by a fresh base scan;
  • REFRESHED (rebuilt) on version change, not silently evicted; its staleness is a disclosure;
  • PROVENANCE-bearing — it records the precision, so the HLL relative-standard-error rides into
    every disclosure of every query it serves.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from datasketches import hll_sketch, hll_union, tgt_hll_type

_TGT = tgt_hll_type.HLL_8


def rse(precision: int) -> float:
    """HLL relative standard error at lg_k = precision (1.04/sqrt(2^p))."""
    return 1.04 / math.sqrt(2 ** precision)


# ---- the three operators (mechanics; the registry holds their vocabulary) ----
def hll_count(values, precision: int):
    """DELIVER: fold a bag of raw values into one HLLSketch(precision)."""
    s = hll_sketch(precision, _TGT)
    for v in values:
        if v is not None:
            s.update(v)
    return s


def hll_merge(sketches, precision: int):
    """COMBINE (monoid union): merge HLLSketch(precision) values into one. Identity = empty
    sketch; associative + commutative — which is exactly what makes the distinct family fertile."""
    u = hll_union(precision)
    for s in sketches:
        u.update(s)
    return u.get_result()


def hll_merge_pair(a, pa: int, b, pb: int):
    """COMBINE two sketches, REFUSING a precision mismatch. Precision is type identity:
    HLLSketch(pa) and HLLSketch(pb) with pa != pb are not the same type and cannot merge."""
    if pa != pb:
        raise TypeError(
            f"cannot merge HLLSketch({pa}) with HLLSketch({pb}): precision is part of the type; "
            f"sketches of different precision are not mergeable (different hash/register width)")
    return hll_merge([a, b], pa)


def hll_estimate(sketch) -> float:
    """PROJECT: HLLSketch -> the distinct-count estimate (a number)."""
    return sketch.get_estimate()


# ---- the witness: publish-time materialized base-grain sketches --------------
@dataclass
class Witness:
    measure: str
    member: str
    base_level: str           # the grain the sketches are keyed at (e.g. 'store', 'day')
    precision: int
    version: str              # backend table version this witness was built against
    sketches: dict            # bucket_key -> hll_sketch


class WitnessStore:
    """Engine-owned store of Columna-built sketches. STORED, not cached (see module docstring).
    The backend never builds, stores, or merges a sketch — it only scans rows to feed hll_count.
    In Core this lives in-process for the Manifold's lifetime; the interface is drawn so a durable
    backend (on-disk / KV) drops in later without changing callers."""

    def __init__(self):
        self._w: dict = {}

    def put(self, w: Witness):
        self._w[(w.measure, w.member, w.base_level)] = w

    def get(self, measure: str, member: str, base_level: str):
        return self._w.get((measure, member, base_level))

    def fresh(self, measure: str, member: str, base_level: str, version: str) -> bool:
        w = self.get(measure, member, base_level)
        return w is not None and w.version == version

    def materialized(self) -> list:
        return sorted(self._w.keys())

    def __len__(self):
        return len(self._w)

"""
columna_platform.columnar.index — **the governed coordinate index, and it is SPARSE.**

WHAT THIS IS AND, MORE IMPORTANTLY, WHAT IT IS NOT
--------------------------------------------------
Ruled (Huayin, 2026-09-28): *"A materialized anchor needs an execution representation of the existing
analytical points at that anchor. This is local to a Manifold/universe/anchor/analytical-instance context.
**It must not be interpreted as a universal analytical-point identifier** for Ω_U."*

So a `CoordinateIndex` is a LOCAL EXECUTION ARTEFACT: the existing coordinate tuples of one anchor, in one
Manifold, in a stable order, so that a batch's rows have positions. Its `identity` is a digest of exactly
that content — which makes it usable for the one thing it is for, *deciding whether two produced layouts
are the same layout* — and for nothing else. Two Manifolds' indexes over the same coordinates are
different indexes, because the Manifold is in the digest.

**SPARSE GEOMETRY STAYS SPARSE.** `{store, day}` is not a Cartesian product, and this class cannot make it
one: it is constructed FROM the coordinate tuples that exist and has no notion of a domain to multiply
out. There is no code path here that manufactures a missing combination and fills it with zero or NULL.
`__post_init__` refuses a duplicate, because a repeated coordinate would give one analytical point two
positions and silently double it under any reduction.

**MEMBERSHIP IS A GOVERNED FACT.** For an anchor whose points are established by the contributions that
reached it, *being in this index* is what point existence means — which is why the standing model in
`standing.py` does not need an `exists` mask as well.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable

from columna_platform.kernel import Anchor, AnalyticalInstance, KernelRefusal


def index_digest(manifold: str, anchor: Anchor, coordinates: tuple[tuple, ...]) -> str:
    """**The identity digest, as a pure function.** Extracted in E-2 so that the memo in
    `CoordinateIndex.identity` is a cache around something a test can call directly and compare against —
    *"preserve exact current identity semantics"* is then checkable rather than asserted.

    The algorithm is byte-for-byte the one that shipped before E-2: the same payload keys, the same
    `sort_keys`/`separators`, the same `default=str`, the same 32 hex characters, the same `cidx-1:`
    prefix. A change here is a change to every layout comparison in the system."""
    payload = {
        "manifold": manifold,
        "universe": anchor.universe,
        "anchor": sorted(anchor.constituents),
        "coordinates": [list(map(_jsonable, c)) for c in coordinates],
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return "cidx-1:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


@dataclass(frozen=True)
class CoordinateIndex:
    """`(Manifold, universe, anchor)` + the SPARSE, ordered existing points."""

    manifold: str
    anchor: Anchor
    #: The existing coordinate tuples, each in `anchor.order`. **Only points that exist.**
    coordinates: tuple[tuple, ...]

    def __post_init__(self) -> None:
        width = len(self.anchor.order)
        for cell in self.coordinates:
            if len(cell) != width:
                raise KernelRefusal(
                    "malformed-coordinate", str(self.anchor),
                    f"coordinate {cell!r} has {len(cell)} components and {self.anchor} has {width}. A "
                    f"coordinate is a point of THIS anchor or it is not a coordinate of it.")
        if len(set(self.coordinates)) != len(self.coordinates):
            dupes = sorted({c for c in self.coordinates if self.coordinates.count(c) > 1},
                           key=lambda c: tuple(map(str, c)))
            raise KernelRefusal(
                "duplicate-coordinate", str(self.anchor),
                f"{dupes} appear more than once. One analytical point would then hold two positions in "
                f"this batch and be counted twice by every reduction over it.")
        object.__setattr__(self, "_positions", {cell: i for i, cell in enumerate(self.coordinates)})
        # **THE IDENTITY MEMO SLOT, EMPTY.** Set on first read, never invalidated — see `identity`.
        object.__setattr__(self, "_identity", None)

    # ── the local, non-universal identity ────────────────────────────────────────────────────
    @property
    def identity(self) -> str:
        """A digest of `(Manifold, universe, anchor, coordinates)`.

        **Its ONLY job is to answer "is this the same layout?"** — the question the ruling raises when it
        says *"if two independently produced results use different index layouts for the same governed
        target, alignment must be explicit."* It is not a point identifier, it is not stable across
        Manifolds, and nothing in this package uses it to look a point up.

        **MEMOISED ON FIRST READ** (ruled E-2, after recon E-X measured it). The digest is
        `O(cells × width)` Python plus a full JSON serialisation plus a SHA-256, and this was a plain
        `@property` recomputing all of it on **every access** — including twice per role pair inside
        `columnar/expression.py`'s layout check and twice inside `aligns_with`, both of which are asked
        before any arithmetic runs. Nothing about the digest changed; only how many times it is computed.

        **THE MEMO CANNOT GO STALE, AND THAT IS A PROPERTY RATHER THAN A PROMISE.** This class is a frozen
        dataclass, `identity` is a pure function of its fields, and no code in the package mutates a built
        index — `object.__setattr__` appears nowhere outside `__post_init__`. There is therefore no
        invalidation path to get wrong, and `replace()` constructs a new object with an empty slot."""
        if self._identity is None:                           # type: ignore[attr-defined]
            object.__setattr__(self, "_identity",
                               index_digest(self.manifold, self.anchor, self.coordinates))
        return self._identity                                # type: ignore[attr-defined]

    def __len__(self) -> int:
        return len(self.coordinates)

    def position(self, cell: tuple) -> int:
        try:
            return self._positions[cell]                    # type: ignore[attr-defined]
        except KeyError:
            raise KernelRefusal(
                "coordinate-not-in-index", str(self.anchor),
                f"{cell!r} is not an existing point of this index. **NOTHING IS ADDED HERE**: sparse "
                f"geometry stays sparse, and a coordinate absent from the index is a point the "
                f"contributions never reached, not a cell to be created and zero-filled.") from None

    def has(self, cell: tuple) -> bool:
        return cell in self._positions                      # type: ignore[attr-defined]

    def columns(self) -> dict[str, list]:
        """The coordinate columns, as `reference -> values in index order`. The physical carriage of the
        geometry, and the only thing a provider needs to group by."""
        return {ref: [cell[i] for cell in self.coordinates]
                for i, ref in enumerate(self.anchor.order)}

    @staticmethod
    def of(manifold: str, anchor: Anchor, cells: Iterable[tuple]) -> "CoordinateIndex":
        """Build an index from existing points, in a STABLE order. Sorted by the coordinate values so
        that two independent constructions over the same points agree — which is what makes
        `identity` able to decide sameness rather than merely detect difference."""
        return CoordinateIndex(manifold=manifold, anchor=anchor,
                               coordinates=tuple(sorted(set(cells), key=lambda c: tuple(map(str, c)))))

    def __str__(self) -> str:
        return f"{self.manifold}:{self.anchor}[{len(self)} pts]"


def _jsonable(value: Any) -> Any:
    return value if isinstance(value, (str, int, float, bool, type(None))) else str(value)


@dataclass(frozen=True)
class AnchorInstance:
    """**`AnchorInstance(M, U, A, I)`** — a coordinate index bound to one analytical instance.

    The direction document's object, exactly. Kept SEPARATE from `CoordinateIndex` because a block may
    co-locate columns from different analytical instances (and the proof does), so the layout and the
    instance are two facts that must be comparable independently: *same layout, different instance* is
    precisely the case where arithmetic must be refused while the positions line up perfectly."""

    index: CoordinateIndex
    instance: AnalyticalInstance

    @property
    def anchor(self) -> Anchor:
        return self.index.anchor

    @property
    def manifold(self) -> str:
        return self.index.manifold

    def __post_init__(self) -> None:
        if self.index.manifold != self.instance.manifold:
            raise KernelRefusal(
                "manifold-disagreement", str(self.index),
                f"the coordinate index belongs to Manifold {self.index.manifold!r} and the analytical "
                f"instance to {self.instance.manifold!r}. One anchor instance cannot straddle two "
                f"jurisdictions.")

    def aligns_with(self, other: "AnchorInstance") -> bool:
        """Same layout AND compatible instance — the two conditions positional arithmetic needs."""
        return (self.index.identity == other.index.identity
                and bool(self.instance.compatible_with(other.instance)))

    def __str__(self) -> str:
        return f"{self.index}@{self.instance.participation[:28]!r}"


__all__ = ["AnchorInstance", "CoordinateIndex", "index_digest"]

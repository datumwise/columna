"""
columna_platform.kernel.geometry — the governed universe and its anchor geometry.

**THE V8-NATIVE PLATFORM KERNEL. NOTHING HERE IMPORTS `columna_core`.**

Ruled (Huayin, 2026-09-28): *"Platform is the architectural destination… Platform must not depend on
the Core governed/native ontology in order to acquire v8 semantics."* So this is a parallel
implementation built from the v8 objects directly, not a migration of anything. Core's
`governed/native.py` is reference material and was read as evidence about required capabilities; no
line of it is imported and no shape is preserved for compatibility.

WHAT AN ANCHOR IS, AND THE ONE CONSEQUENCE THAT MATTERS TO AN MME
-----------------------------------------------------------------
An anchor is a **universe-relative set of governed constituents**. Not a name, not a level, not a
declaration, not an entry in a global map. Two consequences the kernel depends on:

* **finer is SUPERSET.** `{store, day}` refines `{day}`, and the EDGE between them is named by what it
  FORGETS — `{store}`. Every continuation question in this kernel is a question about a forgotten set.
* **synonyms cannot exist.** Two spellings denoting one constituent set are one anchor, because the
  anchor IS the set. There is no place for a name to disagree with a structure.

WHY THE EDGE IS FIRST-CLASS AND NOT DERIVED AT THE CALL SITE
-------------------------------------------------------------
The V8-1 reconnaissance found that Core's `operators.re_entrant` is a **global Boolean** and recorded
that *"a global Boolean cannot represent v8's edge- and condition-relative value closure"* (ToD v8 §3.1:
value closure holds *"only for the continuation region over which this condition holds"*; §3.5: a mean
is value-closed *"where the averaged population is a declared governed geometry with total
participation"*). So closure is a property of an EDGE, and an edge needs to be an object before a law
can be relative to one. `Edge` is that object, and `ContinuationRegion` is the law's answer over it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


class KernelRefusal(Exception):
    """A governed refusal raised at CONSTITUTION time — building an object the theory does not admit.

    Deliberately an exception rather than a returned verdict, and the split is doctrinal: constituting
    an unlawful object is a defect in the caller's declaration and must not be representable, whereas
    *serving* is total and returns an `Answer` carrying a `Refusal`. An MME that raised on an
    unanswerable ask would make a capability limit look like a defect — which is the exact confusion
    V8-0 found at Core's C7 seam and V8-1 found at its family lookup."""

    def __init__(self, code: str, subject: str, detail: str) -> None:
        super().__init__(f"[{code}] {subject}: {detail}")
        self.code, self.subject, self.detail = code, subject, detail


@dataclass(frozen=True)
class Constituent:
    """One governed constituent of a universe, and the value domain that individuates it."""

    reference: str
    domain: str
    equality: str = "identity"


@dataclass(frozen=True)
class Anchor:
    """**A universe-relative constituent set.** The unit of analytical location."""

    universe: str
    constituents: frozenset[str]

    def __str__(self) -> str:
        inner = ", ".join(sorted(self.constituents))
        return f"{self.universe}{{{inner}}}"

    @property
    def is_scalar(self) -> bool:
        """The grand total — the anchor forgetting everything. A lawful location, not an absence."""
        return not self.constituents

    @property
    def order(self) -> tuple[str, ...]:
        """The canonical constituent order for keying a cell. SORTED, so a cell key is a function of
        the anchor and not of whoever built it."""
        return tuple(sorted(self.constituents))

    def refines(self, other: "Anchor") -> bool:
        self._same_world(other)
        return other.constituents < self.constituents

    def forgets(self, target: "Anchor") -> frozenset[str]:
        """The constituents this anchor loses in reaching `target` — **the edge, named.**"""
        self._same_world(target)
        if not target.constituents <= self.constituents:
            raise KernelRefusal(
                "not-a-coarsening", str(self),
                f"{target} is not reachable from {self} by forgetting constituents: it names "
                f"{sorted(target.constituents - self.constituents)}, which this location does not "
                f"carry. A coarsening forgets; it does not acquire.")
        return frozenset(self.constituents - target.constituents)

    def edge_to(self, target: "Anchor") -> "Edge":
        return Edge(source=self, target=target, forgotten=self.forgets(target))

    def project(self, cell: tuple, from_anchor: "Anchor") -> tuple:
        """Re-key one cell of `from_anchor` onto this (coarser) anchor.

        The whole of coarsening's mechanics, in one place: drop the coordinates this anchor does not
        carry and keep the rest in THIS anchor's canonical order. Two source cells differing only in a
        forgotten coordinate project onto one key, which is what makes them contributions to one
        coarser value."""
        position = {ref: i for i, ref in enumerate(from_anchor.order)}
        return tuple(cell[position[ref]] for ref in self.order)

    def _same_world(self, other: "Anchor") -> None:
        if self.universe != other.universe:
            raise KernelRefusal(
                "cross-world-anchor", str(self),
                f"{other} is relative to universe {other.universe!r}. Anchors are universe-relative "
                f"and there is no vantage point from which two universes' anchors are both visible.")


@dataclass(frozen=True)
class Edge:
    """**One continuation edge, `source → target`, named by what it forgets.**

    First-class because value closure is relative to it (see the module note). An `Edge` carries no
    licence and no verdict — it is the QUESTION. `ContinuationRegion` is a law's answer."""

    source: Anchor
    target: Anchor
    forgotten: frozenset[str]

    def __str__(self) -> str:
        return f"{self.source} → {self.target}  (forgets {sorted(self.forgotten)})"


@dataclass(frozen=True)
class Universe:
    """A governed world: a CLOSED set of constituents, a population law, and nothing physical.

    Closure is asserted, not inferred — *these constituents and no others* — and the derived geometry
    is a consequence of it. There is no carrier, column, table or grain reachable from here."""

    name: str
    constituents: tuple[Constituent, ...]
    ground: str
    participation_law: str

    def __post_init__(self) -> None:
        seen = [c.reference for c in self.constituents]
        if len(set(seen)) != len(seen):
            raise KernelRefusal("duplicate-constituent", self.name,
                                "a constituent is declared twice; individuation is not a label.")

    @property
    def references(self) -> frozenset[str]:
        return frozenset(c.reference for c in self.constituents)

    def anchor(self, references: Iterable[str]) -> Anchor:
        """The anchor over `references` — **resolved inside this universe and nowhere else.**"""
        wanted = frozenset(references)
        unknown = sorted(wanted - self.references)
        if unknown:
            raise KernelRefusal(
                "unknown-constituent", self.name,
                f"{unknown} are not constituents of this universe (it carries "
                f"{sorted(self.references)}). Resolution is universe-scoped: a reference that "
                f"resolves elsewhere does not resolve here.")
        return Anchor(universe=self.name, constituents=wanted)

    @property
    def root_anchor(self) -> Anchor:
        """The finest location this world admits — every constituent at once."""
        return Anchor(universe=self.name, constituents=self.references)

    @property
    def scalar_anchor(self) -> Anchor:
        return Anchor(universe=self.name, constituents=frozenset())

    def cell_of(self, anchor: Anchor, row: Mapping[str, Any]) -> tuple:
        """The cell key `row` falls in at `anchor`. Missing coordinates refuse: a contribution whose
        location is partly unknown is not a contribution at a coarser location, it is a fact with no
        governed place to land."""
        missing = sorted(r for r in anchor.order if r not in row)
        if missing:
            raise KernelRefusal(
                "unlocated-contribution", self.name,
                f"a contribution at {anchor} states no value for {missing}. There is no default "
                f"coordinate: a fact whose location is unknown is not a fact at a coarser location.")
        return tuple(row[r] for r in anchor.order)


def scalar(universe: Universe) -> Anchor:                       # a readability alias for exhibits
    return universe.scalar_anchor


__all__ = ["Anchor", "Constituent", "Edge", "KernelRefusal", "Universe", "scalar"]

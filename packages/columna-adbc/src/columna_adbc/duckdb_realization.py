"""
columna_adbc.duckdb_realization — **the first REAL `RealizationProvider`. DuckDB, through ADBC, as Arrow.**

    *"Columna can ask a real database for governed family state, establish what came back, admit it into
    the MME, serve it, and answer the same analytical request again without touching the database."*
    — Huayin, 2026-09-30 (B-2, the claim)

        FamilyRequirement(revenue, build, witness, …)     ← governed, and it names no table
                ↓
        this provider consults its PRIVATE physical binding
                ↓
        DuckDbAdbcSource.fetch  →  DuckDB → ADBC → pa.Table
                ↓
        ColumnarFamilyState — the values are the SAME Arrow buffer that crossed
                ↓
        RealizationOffer
                ↓
        RealizationAuthority.adjudicate  →  AdjudicatedRealization
                ↓
        RealizationManager.establish  →  ordinary MME.put

WHY THIS FILE IS IN THIS PACKAGE AND NOT IN PLATFORM (ruled §5)
--------------------------------------------------------------
    columna-adbc  owns  the DuckDB binding · schema/table/column names · physical query manufacture · ADBC
    Platform      sees  FamilyRequirement · RealizationProposal · RealizationOffer · governed Arrow state

`columna_platform` may not import a driver — a ban this repository enforces statically AND in a clean
interpreter — and `FamilyRequirement` carries no table, no column and no predicate by construction. So the
physical half has to live somewhere the arrow already points: **this package depends on Platform and Platform
does not know it exists.** Nothing here is registered with Platform, imported by it, or named in it; a
deployment constructs this provider and hands it to a `RealizationManager`, which is the seam R-1 reserved.

WHAT THE PROVIDER IS FORBIDDEN TO DO, AND WHERE THAT IS VISIBLE
---------------------------------------------------------------
**It never reverse-infers analytical identity from a physical column** (ruled §5). The binding maps
governed name → physical name in exactly one direction, and `propose` matches on `requirement.family_id`
and on the requirement's ROOT CONSTITUENT SET. A column called `net_amount` does not make anything revenue;
the requirement says which family is wanted and the binding says where this deployment happens to keep it.

**It does not self-certify** (B-1′). It states `build` and `witness` — RESTATED from the requirement, never
judged — and has no way to mint `AdjudicatedRealization`. That its output comes from a real database rather
than a test double grants it no additional authority, which is half of what B-2 exists to prove.

**It declares no capability it has not been bound for.** `propose` yields nothing at all for an unbound
family — silence, which `RealizationManager` reports as a decline — rather than a refusal, because whether a
family is servable anywhere is not this provider's question.

ARROW IS THE CROSSING, AND EXACTLY WHERE IT STOPS BEING ARROW IS STATED (ruled §3)
---------------------------------------------------------------------------------
The VALUE column is never converted. `fetch` returns a `pa.Table`; the value column is combined into one
Arrow array and handed to `ColumnarFamilyState.values` unchanged, and `RealizationOffer`'s own docstring
already promised that: *"Arrow stays Arrow all the way into `admit`."* There is no `to_pylist`, no dict of
cells, and no rebuild of analytical state.

The COORDINATE columns are materialized as Python tuples, and that is not a conversion of the value path —
it is the shape `CoordinateIndex` is: `coordinates: tuple[tuple, ...]`, sparse and ordered, which is how
every columnar block in this repository is already constructed (`columnar/exhibit.py::_root_index` does the
same thing from the same kind of source). The governed payload stays in Arrow; the LAYOUT is a tuple of
points because the layout is an analytical object, not a buffer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Optional, Sequence

import pyarrow as pa

from columna_platform.columnar.index import AnchorInstance, CoordinateIndex
from columna_platform.columnar.mme import ColumnarFamilyState
from columna_platform.columnar.standing import standing as column_standing
from columna_platform.kernel.geometry import Anchor, KernelRefusal
from columna_platform.kernel.realization import RealizationStanding
from columna_platform.kernel.sorts import PARTICIPATION_CARDINALITY
from columna_platform.kernel.realization_manager import RealizationOffer, RealizationProposal

#: The carrier this provider supplies through. **A carrier, not an authority** — it names how the material
#: travelled, which is one of the three axes a `RetentionKey` keeps apart, and it decides nothing.
ARROW_OVER_ADBC = "duckdb/adbc→arrow"

#: **THE ONE GOVERNED TOKEN THIS MODULE NAMES, AND IT IS IMPORTED RATHER THAN SPELLED** (B-4a). A provider
#: that executes declared formations must be able to tell which one it was handed; what it must not have is
#: any route from a LAW to a formation. So this is the formation vocabulary's own constant, and there is no
#: law name, no fold shape and no value domain anywhere in this file.
_CARDINALITY = PARTICIPATION_CARDINALITY


@dataclass(frozen=True)
class PhysicalFamilyBinding:
    """**Where one governed family's root state physically lives in one DuckDB deployment.**

    Deployment-local, injected, and never read from a convention over names. The token `revenue` means
    whatever the Manifold declares; `net_amount` means whatever this warehouse happens to call the column.
    The binding is the only place those two facts meet, and it meets them in one direction."""

    family_id: str
    table: str
    #: governed constituent name → physical column name. **Its KEY SET is the governed root grain**, which
    #: is what `propose` matches against, so a binding at the wrong grain proposes nothing rather than
    #: proposing something that would then be refused deeper in.
    coordinates: Mapping[str, str]
    #: **OPTIONAL, AND WHICH FORMATIONS NEED IT WAS DERIVED RATHER THAN DECIDED** (B-4a).
    #:
    #: A `DIRECT` root's value is independently established as a value of the family, so a binding MUST
    #: say where that value physically lives — without it there is nothing to supply.
    #:
    #: A `PARTICIPATION_CARDINALITY` root's value is the cardinality of the governed participating domain,
    #: and the domain is what the projection returns: the governed coordinates. The value is therefore
    #: **completely determined by the coordinates this realization supplies**, and a physical value column
    #: would be a second, independent source for a value that has only one constitution. So it is not
    #: merely unnecessary — it is REFUSED, because a binding naming one would be naming a number that could
    #: disagree with the domain, which is precisely the laundering surface B-4a exists to close.
    value_column: Optional[str] = None
    schema: Optional[str] = None
    note: str = ""

    @property
    def grain(self) -> frozenset:
        return frozenset(self.coordinates)

    def physical_columns(self, order: Sequence[str]) -> tuple[str, ...]:
        """The projection: the anchor's own constituent order, plus the value column where there is one."""
        columns = tuple(self.coordinates[c] for c in order)
        return columns + ((self.value_column,) if self.value_column else ())

    def __str__(self) -> str:
        where = f"{self.schema}.{self.table}" if self.schema else self.table
        source = f"{where}.{self.value_column}" if self.value_column else f"{where} (coordinates only)"
        return f"{self.family_id} ← {source} at {sorted(self.grain)}"


@dataclass(frozen=True)
class _Handle:
    """**The provider's own opaque handle**, which `RealizationManager` is documented never to interpret.

    Everything `realize` needs rides here because `realize` receives only a proposal — including the two
    governed facts B-1′ requires an offer to STATE (`build`, `witness`) and the analytical instance the
    requirement named. A provider that had to re-derive those would be judging them."""

    binding: PhysicalFamilyBinding
    anchor: Anchor
    manifold: str
    build: str
    witness: str
    instance: Any
    law: str
    value_form: str
    #: **CARRIED, NEVER DERIVED** (B-4a). Which formation law this realization must execute. The provider
    #: performs the physical construction it names and decides nothing about what it means.
    formation: str
    #: **CARRIED, NEVER DERIVED** (B-3). `value-bearing` or `population`, read off the requirement. This
    #: provider has no mapping from a law NAME to a shape and must not acquire one: B-0b deleted exactly
    #: such an enumeration (`COUNT → population`) from the columnar cache engine, and rebuilding it here
    #: would put constitutional knowledge below the realization boundary instead of above it.
    fold_shape: str


class DuckDbFamilyProvider:
    """**A `RealizationProvider` over a real DuckDB database, reached through the existing ADBC crossing.**

    It holds a `DuckDbAdbcSource` — the crossing proved in `duckdb_adbc.py`, unchanged and not
    reimplemented — and one `PhysicalFamilyBinding` per family it can supply. Capability discovery
    (`propose`) opens nothing; execution (`realize`) opens one connection, projects, and closes it.

    **THE FETCH COUNTER IS THE SOURCE'S, NOT THIS CLASS'S.** `DuckDbAdbcSource.fetches` already records
    every projection it performed, appended BEFORE the connection is opened so it counts attempts rather
    than successes. B-2's headline proof reads `len(source.fetches)`, so the instrument is the one the
    crossing already had and nothing was added to make the proof easier to pass."""

    def __init__(self, source: Any, *bindings: PhysicalFamilyBinding, name: str = "duckdb-warehouse",
                 carrier: str = ARROW_OVER_ADBC) -> None:
        self.name = name
        self.source = source
        self.carrier = carrier
        self._bindings: dict[str, PhysicalFamilyBinding] = {b.family_id: b for b in bindings}

    @property
    def standing(self) -> RealizationStanding:
        """**Which provider, which carrier.** One of the three axes, and the one this object is."""
        return RealizationStanding(provider=self.name, carrier=self.carrier)

    def bindings(self) -> tuple[str, ...]:
        return tuple(sorted(self._bindings))

    # ── capability. Executes nothing, fetches nothing, opens nothing. ─────────────────────────
    def propose(self, requirement: Any) -> Iterable[RealizationProposal]:
        """**Could this deployment supply the required state?** Read-only, and it touches no database.

        Two conditions, both read off the REQUIREMENT rather than off the database:

        1. this provider is bound for `requirement.family_id`;
        2. the binding's governed grain is exactly `requirement.root` — because what a warehouse table
           holds is **independently established root state**, and this provider neither continues nor
           aggregates. A coarser target is reached by the engine's own continuation from what is admitted
           here, which is why nothing below manufactures a `GROUP BY`.

        Anything else yields nothing. An unbound family is silence, not a refusal: whether some other
        provider could supply it is not a question this one is entitled to answer."""
        binding = self._bindings.get(getattr(requirement, "family_id", ""))
        if binding is None:
            return
        root = requirement.root
        if binding.grain != root.constituents:
            return
        yield RealizationProposal(
            provider=self.name, family_id=binding.family_id, anchor=root,
            value_form=requirement.value_form, realization=self.standing,
            handle=_Handle(binding=binding, anchor=root, manifold=requirement.manifold,
                           build=requirement.build, witness=requirement.witness,
                           instance=requirement.instance, law=requirement.law,
                           value_form=requirement.value_form,
                           formation=requirement.formation,
                           fold_shape=requirement.fold_shape),
            diagnostics=f"one bare projection of {binding}; no aggregate, no predicate, no join")

    # ── execution. One projection, and the Arrow that comes back is the Arrow that is offered. ─
    def realize(self, proposal: RealizationProposal) -> RealizationOffer:
        """**Execute one proposal and OFFER what came back.** It claims; it does not certify.

        The offer restates `build` and `witness` because B-1′ requires a physical claim to say which
        governed environment it was made against — and `MME.put` is the single asker that compares them.
        This method does not compare them, does not look at the constitution, and could not refuse on them
        if it wanted to."""
        handle = proposal.handle
        if not isinstance(handle, _Handle):
            raise KernelRefusal(
                "foreign-proposal", self.name,
                f"{self.name!r} was asked to realize a proposal it did not make. A handle is a provider's "
                f"private object and executing another's would be executing a plan this provider cannot "
                f"read.")
        if not handle.fold_shape:
            # **A REQUIREMENT THAT WILL NOT SAY WHAT ITS REDUCTION CONTRIBUTES OVER IS NOT A REQUIREMENT
            # THIS PROVIDER CAN SATISFY** (B-3) — the same shape of refusal `RealizationAuthority` makes
            # for an offer that will not state its build. The alternative is the one thing ruled out: to
            # GUESS from the law name. `ContinuationAuthority.requirement_for` always states it, so this is
            # the floor rather than a path; a floor that refuses is how it stays one.
            raise KernelRefusal(
                "requirement-states-no-fold-shape", f"{handle.binding.family_id}@{handle.anchor}",
                f"the requirement for {handle.binding.family_id!r} does not say whether its {handle.law!r} "
                f"reduction contributes over a value-bearing or a population domain, and this provider "
                f"will not infer it from the law's name. Which one applies is a property of the LAW, "
                f"declared by it and carried on the requirement; a provider deciding it would be a second "
                f"opinion about what the family means.")
        binding, anchor = handle.binding, handle.anchor
        self._binding_suits_the_formation(binding, handle.formation)
        order = tuple(anchor.order)
        material = self.source.fetch(schema=binding.schema, table=binding.table,
                                    columns=list(binding.physical_columns(order)))
        table = material.table

        # ── THE DOMAIN. Python tuples, because `CoordinateIndex` IS a tuple of points. ────────
        columns = [table.column(binding.coordinates[c]).to_pylist() for c in order]
        rows = tuple(zip(*columns)) if columns else ()

        # ── THE PAYLOAD, BY THE FORMATION THE REQUIREMENT DECLARED ────────────────────────────
        #
        # **THIS IS PHYSICAL COMPUTATION, NOT PROVIDER INFERENCE** (ruled §7). The wording trap is worth
        # naming: this method constructs a payload from coordinates, which LOOKS like deciding what a
        # count means. It is not. The requirement named a formation law; this executes it. The forbidden
        # shape is `provider knows COUNT → decides Count means one per row`, and the distance between the
        # two is that nothing below reads a law name, a fold shape, or a value domain.
        if handle.formation == _CARDINALITY:
            # The cardinality of the governed participating domain, per governed coordinate. Counting the
            # rows that land on each coordinate is the whole of it — and it is NOT a hardcoded `1`: a
            # projection returning two rows for one coordinate yields 2 here, and the fidelity authority
            # then decides whether that agrees with the domain the index can represent.
            tally: dict[tuple, int] = {}
            for row in rows:
                tally[row] = tally.get(row, 0) + 1
            coordinates = tuple(tally)
            index = CoordinateIndex.of(handle.manifold, anchor, coordinates)
            values = pa.array([tally[c] for c in coordinates], type=pa.int64())
        else:
            coordinates = rows
            index = CoordinateIndex.of(handle.manifold, anchor, coordinates)
            # ── Arrow in, Arrow out, and no step between. ─────────────────────────────────────
            values = _one_array(table.column(binding.value_column))

        state = ColumnarFamilyState(
            family_id=binding.family_id,
            anchor_instance=AnchorInstance(index=index, instance=handle.instance),
            values=values,
            # **THE MASKS ARE ALL-TRUE AND THAT IS A CLAIM, NOT A DEFAULT.** This provider asserts that
            # every row the warehouse returned is a participating point with an established value. It has
            # no support mask to report because the projection carries none; a deployment whose warehouse
            # records unestablished amounts would have to bind that column and say so, and until it does
            # the honest reading of a returned row is "established".
            standing=column_standing(
                binding.family_id, handle.instance, n=len(values),
                note=f"realized by {self.name!r} from {binding} over {self.carrier}"),
            law=handle.law,
            value_form=handle.value_form,
            # **THE REQUIREMENT'S SHAPE, NOT THIS CLASS'S DEFAULT** (B-3). It was the dataclass default
            # `VALUE_BEARING` before, which is right for SUM and silently wrong for COUNT — a population
            # reduction would have been given a value-bearing standing and then refused, or worse, not.
            fold_shape=handle.fold_shape,
        )
        return RealizationOffer(
            provider=self.name, family_id=binding.family_id, anchor=anchor, value=state,
            instance=handle.instance, realization=self.standing,
            build=handle.build, witness=handle.witness, from_proposal=proposal,
            diagnostics=f"{len(values)} root point(s) projected from {binding}")

    @staticmethod
    def _binding_suits_the_formation(binding: "PhysicalFamilyBinding", formation: str) -> None:
        """**Can this private binding realize the declared formation at all?** Refuses before opening.

        Two refusals, and each is a contradiction rather than a preference. A `DIRECT` root without a
        physical value source has nothing to supply. A cardinality root WITH one names a second,
        independent source for a value that has exactly one constitution — and a second source is a number
        that can disagree with the domain, which is the defect this unit closes."""
        if not formation:
            raise KernelRefusal(
                "requirement-states-no-root-formation", f"{binding.family_id}@?",
                f"the requirement for {binding.family_id!r} does not say what its root value is "
                f"CONSTITUTED FROM, and this provider will not decide. Formation is family constitution; "
                f"a provider choosing one would be choosing what the family means.")
        if formation == _CARDINALITY:
            if binding.value_column:
                raise KernelRefusal(
                    "cardinality-binding-names-a-value-column", binding.family_id,
                    f"{binding} binds a physical value column for a family whose root formation is "
                    f"{_CARDINALITY!r}. That value is the cardinality of the governed participating "
                    f"domain and has ONE constitution; a physical column would be a second source for it, "
                    f"free to disagree with the domain it is supposed to be the size of. Bind the "
                    f"coordinates and nothing else.")
            return
        if not binding.value_column:
            raise KernelRefusal(
                "binding-names-no-value-source", binding.family_id,
                f"{binding} names no physical value column and {binding.family_id!r} declares root "
                f"formation {formation!r}, under which the value is independently established as a value "
                f"of the family rather than derived from participation. There is nothing here to supply "
                f"it from.")

    def versions(self) -> dict:
        """The driver evidence, straight from the crossing. Diagnostics; nothing branches on it."""
        return dict(self.source.versions())

    def __str__(self) -> str:
        return f"DuckDbFamilyProvider({self.name!r}, bound for {self.bindings()})"


def _one_array(column: Any) -> pa.Array:
    """One Arrow array from a table column, **without leaving Arrow**.

    A `Table` column is a `ChunkedArray` and a wide projection really does come back in several chunks
    (the crossing's own tests force 3000 distinct days for exactly that reason). Combining them is an
    Arrow operation; the alternative — reading positions out in Python and rebuilding — is the conversion
    §3 forbids."""
    if isinstance(column, pa.ChunkedArray):
        combined = column.combine_chunks()
        if isinstance(combined, pa.ChunkedArray):
            if combined.num_chunks == 1:
                return combined.chunk(0)
            return pa.concat_arrays([c for c in combined.iterchunks()]) if combined.num_chunks \
                else pa.array([], type=combined.type)
        return combined
    return column


__all__ = ["ARROW_OVER_ADBC", "DuckDbFamilyProvider", "PhysicalFamilyBinding"]

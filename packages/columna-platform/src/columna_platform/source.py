"""Deployment-local material sources, and the binding a realization endpoint resolves through.

WHAT THIS MODULE EXISTS TO ANSWER. A realization endpoint says
`connection="warehouse", schema="sales", table="fact_sale", column="amount"`. Until now nothing in
this package opened it: the endpoint was interpolated into a standing string (`serving.py`) and the
carrier was a literal built beside it. This module is the first thing that turns those four fields
into material, and it is the smallest thing that can.

`connection` IS A DEPLOYMENT-LOCAL BINDING, NOT ENGINE SEMANTICS (ruled Huayin, 2026-09-14). The
token `"warehouse"` means nothing to this package. It means whatever the deployment bound it to, and
a deployment that bound nothing has no material for it — which is a refusal, not a default. So the
registry is INJECTED at construction and never read from the environment, a file format, or a
convention over directory names. Nothing here is a permanent configuration API, and the shape below
is not frozen: what is frozen is the invariant R1 asks for, and only that —

    changing `connection` alone must change which material source is selected, or cause a refusal.

THE WHOLE ENDPOINT SELECTS, NOT A PREFIX OF IT. `schema` participates (ruled 2026-09-14): a source
holds objects keyed by `(schema, table)`, so `sales.fact_sale` and `staging.fact_sale` are different
material and neither answers for the other. That is R2 discharged by CONSUMING the fact rather than
refusing it, which is a different lawful choice from K0v2's — K0v2 REFUSES a non-null schema because
its execution grammar cannot represent one, and it is not weakened to match this. Two profiles may
discharge one fact through different channels; what neither may do is drop it.

NO DATABASE, NO DRIVER, NO FILE — IN THIS PACKAGE. `InMemoryArrowSource` holds `pyarrow.Table`s
constructed in the process. DuckDB and ADBC are not merely unused here: both are in this package's
standing forbidden-import set, statically and in a clean interpreter
(`tests/test_proof_a_findings.py`), and that ban is UNCHANGED now that a driver-backed adapter
exists. It was always package-scoped — *Platform must not import a driver* — and never a claim that
the repository contains none.

A DRIVER-BACKED SOURCE IMPLEMENTS `MaterialSource` FROM OUTSIDE. `columna-adbc` depends on this
package; this package does not know it exists, statically or at runtime. The deployment constructs
the adapter and injects it through `MaterialBinding`, which is the seam that was reserved for
exactly this and is unchanged by its arrival.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Optional, Protocol, Sequence, Tuple, runtime_checkable

import pyarrow as pa

from .carrier import AnchoredCarrier
from .refusals import UnsupportedByThisProfile, WantOfState

#: `(schema, table)` — the object key. `schema` may be `None`, which is a POSITIVE claim that no
#: schema qualification applies and never a dropped one; `None` and `"sales"` are different keys.
ObjectKey = Tuple[Optional[str], str]


@dataclass(frozen=True)
class Material:
    """What ONE PROJECTED FETCH returns — the ratified source-adapter contract's return shape.

    `data_state` IS AN OPAQUE, COMPARABLE TOKEN OR `None`, AND IT RIDES HERE RATHER THAN ON A SECOND
    CALL. The token belongs to the SAME MATERIAL OBSERVATION as the carrier beside it; a separate
    `data_state()` call could observe a different state, and the pair would then describe two moments
    while looking like one.

    `None` IS NOT "FRESH" AND NOT "UNKNOWN-BUT-FINE" — it CLOSES REUSE (`Standing.currency`).
    Platform never interprets, parses, orders or derives meaning from a token: it may compare one for
    equality with another from the same adapter, and nothing else. Equality does not mean current."""

    table: pa.Table
    data_state: Optional[str] = None


@runtime_checkable
class MaterialSource(Protocol):
    """One deployment-bound source of Arrow material. ONE METHOD, ON PURPOSE.

    THERE IS DELIBERATELY NO METHOD THAT RETURNS A WHOLE OBJECT. That is what makes "do not establish
    `SELECT *` / full-object reads as the external execution model" a property of THE SHAPE OF THIS
    INTERFACE rather than of anyone's discipline: an adapter *cannot express* a full-object read
    through it. There is likewise no predicate parameter (a predicate is an analytical restriction,
    and which restrictions are governed is not transport's jurisdiction), no ordering parameter (CAP
    v1 carries no ordering guarantee), no `execute(sql)` (the adapter is asked for a projection of a
    named object, not for the result of a statement), and no schema-discovery call (admission
    inspects the schema that ARRIVED, and a second schema could differ from it)."""

    def fetch(self, *, schema: Optional[str], table: str,
              columns: Sequence[str]) -> Material:
        """Return exactly `columns` from `(schema, table)`, as Arrow, in one request.

        `schema=None` is a POSITIVE claim that no schema qualification applies, never a dropped one.

        A MISSING REQUESTED COLUMN OR OBJECT IS A REFUSAL. An implementation must NOT silently
        return a shorter projection: a caller that asked for three columns and received two would
        hold a carrier whose coordinates are quietly incomplete, and admission would then refuse it
        naming the ANCHOR when the fault is in the SOURCE.

        `Material.table` is a fully materialized `pa.Table`, never a `RecordBatchReader`. An adapter
        MAY consume a reader internally — duckdb's native `.arrow()` returns one, and that hazard is
        measured (admission study [E1]: fifteen ERROR rows) — but it must DISCHARGE the hazard before
        handing material over. A consumed-once object must not reach the admission path."""
        ...


@dataclass(frozen=True)
class InMemoryArrowSource:
    """One deterministic material source, held as Arrow tables in this process.

    `objects` is keyed by `(schema, table)` so that the endpoint's qualification is what selects,
    and `name` exists only so a refusal can say which source could not answer."""

    name: str
    objects: Mapping[ObjectKey, pa.Table]

    def fetch(self, *, schema: Optional[str], table: str,
              columns: Sequence[str]) -> Material:
        """`MaterialSource.fetch` over in-process tables. One projection, one observation.

        THE PROJECTION IS REAL EVEN HERE. This source holds whole tables and could hand one back
        whole; it does not, because the interface it implements is the one a driver-backed adapter
        implements, and a fixture that quietly took a wider path than production would stop being a
        fixture for production.

        `data_state=None`: an in-process table has no opaque state identity to report, and inventing
        one would be manufacturing the freshness semantics the contract leaves unresolved."""
        obj = self.objects.get((schema, table))
        if obj is None:
            raise WantOfState(
                f"source {self.name!r} holds no object {_spell_object(schema, table)}; it holds "
                f"{_spell_objects(self.objects)}", subject=self.name)
        missing = [c for c in columns if c not in obj.column_names]
        if missing:
            raise WantOfState(
                f"object {_spell_object(schema, table)} in source {self.name!r} has no column(s) "
                f"{missing}; it has {sorted(obj.column_names)}", subject=self.name)
        return Material(table=obj.select(list(columns)).combine_chunks(), data_state=None)


class SourceBindings:
    """`connection` token → material source. THE ONLY THING THAT KNOWS WHAT `"warehouse"` MEANS.

    An unknown connection is a WANT OF STATE and not a want of law: the governed law licensed the
    ask, and what is absent is a deployment binding — which re-realization (here, binding the
    connection) is exactly the remedy for. It is also not `UnsupportedByThisProfile`: the profile
    implements material access, and this deployment simply has no material at that name."""

    def __init__(self, bindings: Optional[Mapping[str, InMemoryArrowSource]] = None):
        self._bindings: Dict[str, InMemoryArrowSource] = dict(bindings or {})

    def __bool__(self) -> bool:
        return bool(self._bindings)

    @property
    def connections(self) -> tuple:
        return tuple(sorted(self._bindings))

    def source_for(self, connection: str) -> InMemoryArrowSource:
        src = self._bindings.get(connection)
        if src is None:
            raise WantOfState(
                f"no material source is bound to connection {connection!r} in this deployment; "
                f"bound connections are {list(self.connections)}", subject=connection)
        return src


def _spell_object(schema: Optional[str], table: str) -> str:
    return f"{schema}.{table}" if schema is not None else f"{table} (no schema qualification)"


def _spell_objects(objects: Mapping[ObjectKey, pa.Table]) -> str:
    return ", ".join(_spell_object(s, t) for s, t in sorted(objects, key=lambda k: (k[0] or "", k[1]))) or "none"


def read_anchored(bindings: SourceBindings, family_realization, component_realizations,
                  *, value_column: str = "value") -> AnchoredCarrier:
    """Assemble the anchored carrier for one family from material, or refuse.

    `component_realizations` maps a GOVERNED component name to its realization. The rename from the
    physical column to the governed name happens HERE and is the anchor-component realization's whole
    job: `store_code` is material, `store` is governed, and the claim that one realizes the other is
    the mapping's to make and this function's to honour. Nothing downstream sees a physical name —
    which is what lets admission compare the carrier's coordinates against the publication's
    declared components without knowing anything about the source.

    ONE OBJECT, OR A CAPABILITY REFUSAL. Every endpoint must resolve to the same
    `(connection, schema, table)`. A family whose value and coordinates live in different objects
    needs a join, and a join is a thing this profile does not do — so it raises
    `UnsupportedByThisProfile`, which is NOT a governed verdict. Refusing it as a want-of-state would
    tell an operator to go and re-materialize against a capability that does not exist."""
    ep = family_realization.endpoint
    if ep.column is None:
        raise WantOfState(
            f"the realization for {family_realization.family_id} names no value column",
            subject=family_realization.family_id)

    source = bindings.source_for(ep.connection)
    home = (ep.connection, ep.schema, ep.table)

    # ONE PROJECTED REQUEST, NOT N+1 (2026-09-14, the ratified source-adapter contract). This used to
    # call `source.column(...)` once per coordinate and once for the value — free against an
    # in-process table, N+1 ROUND TRIPS against a driver. The deeper reason is not cost:
    # ONE PROJECTION IS ONE OBSERVATION. N separate reads of one object may see N different states of
    # it, and the equal-length check below would then be comparing columns that were never one
    # delivery — it would look like a guarantee and be a coincidence.
    physical = {}                      # governed component name -> physical column name
    for name in sorted(component_realizations):
        creal = component_realizations[name]
        cep = creal.endpoint
        if (cep.connection, cep.schema, cep.table) != home:
            raise UnsupportedByThisProfile(
                f"anchor component {name!r} is realized at "
                f"{cep.connection}:{_spell_object(cep.schema, cep.table)} and the family's value at "
                f"{ep.connection}:{_spell_object(ep.schema, ep.table)}; assembling one analytical "
                f"point from two material objects is a join, which this profile does not implement")
        if cep.column is None:
            raise WantOfState(
                f"the realization for anchor component {name!r} names no column", subject=name)
        physical[name] = cep.column

    # DUPLICATE PHYSICAL COLUMNS ARE NOT AN ERROR HERE. Two governed components realized onto one
    # source column is a realization claim this function honours rather than judges; the projection
    # asks for the column once and the rename below delivers it under both governed names.
    requested = list(dict.fromkeys([*physical.values(), ep.column]))
    # AN ADAPTER SAYS "I COULD NOT"; PLATFORM SAYS WHICH KIND OF NO IT IS. An adapter has no business
    # choosing a governed jurisdiction — it does not know whether the law licensed the ask — so the
    # contract has it raise a plain `LookupError` for an object or column it cannot read, and the
    # translation happens HERE, once, at the seam that owns the vocabulary.
    #
    # WANT OF STATE, and the remedy is why: the law licensed the ask and the realization named an
    # object or column this source does not have, which is precisely what re-realization resolves.
    # It is NOT a want of law (the publication is fine), and NOT `unsupported` (the profile
    # implements material access; this deployment's source simply cannot answer).
    try:
        material = source.fetch(schema=ep.schema, table=ep.table, columns=requested)
    except LookupError as e:
        raise WantOfState(
            f"the material source could not read the projection {requested} from "
            f"{_spell_object(ep.schema, ep.table)} for connection {ep.connection!r}: {e}",
            subject=family_realization.family_id) from e
    got = material.table

    # The adapter contract says a missing column REFUSES rather than shortening the projection.
    # Verified here too, against the schema that actually arrived: the contract binds adapters, and
    # this is the boundary that must not be made to trust one.
    short = [c for c in requested if c not in got.column_names]
    if short:
        raise WantOfState(
            f"the projected fetch of {_spell_object(ep.schema, ep.table)} did not return "
            f"{short}; an adapter may not shorten a projection", subject=family_realization.family_id)

    columns = {name: got.column(col).combine_chunks() for name, col in physical.items()}
    values = got.column(ep.column).combine_chunks()

    # Retained though one fetch makes a length mismatch near-impossible: it is the check that says
    # the columns came from ONE delivery, and a future adapter is the reason to keep asking.
    heights = {name: len(arr) for name, arr in columns.items()}
    if any(h != len(values) for h in heights.values()):
        raise WantOfState(
            f"the material columns are not of one length: value column has {len(values)} rows, "
            f"coordinates have {heights}", subject=family_realization.family_id)

    table = pa.table({**columns, value_column: values})
    return AnchoredCarrier(
        table=table, value_column=value_column, anchor_columns=tuple(sorted(columns)),
        measured_as=(f"material source {getattr(source, 'name', type(source).__name__)!r} via "
                     f"connection {ep.connection!r}, object {_spell_object(ep.schema, ep.table)}, "
                     f"projected columns {requested}, value column {ep.column!r}"),
    )


@dataclass(frozen=True)
class MaterialBinding:
    """What a DEPLOYMENT must supply for this profile to execute rather than only plan.

    Two things, both deployment-private and neither part of the published unit: the realization claim
    (which is not shipped in a successor-native unit — the unit is the publication) and the source
    registry the claim's connections resolve through.

    A provider with no binding PLANS and does not EXECUTE, and says so as a capability limit rather
    than as a governed refusal. That is the correct default and not a degraded one: a deployment that
    has bound no material has not been asked to serve any."""

    mapping_path: str
    sources: SourceBindings

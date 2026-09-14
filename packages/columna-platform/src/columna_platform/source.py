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

NO DATABASE, NO DRIVER, NO FILE. `InMemoryArrowSource` holds `pyarrow.Table`s that were constructed
in the process. DuckDB and ADBC are not merely unused here: both are in this package's standing
forbidden-import set, statically and in a clean interpreter
(`tests/test_proof_a_findings.py`). The first material execution proves the ARCHITECTURE — that a
governed identity survives the passage into material and back — and a source that proved a driver
works would be proving something else.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Optional, Tuple

import pyarrow as pa

from .carrier import AnchoredCarrier
from .refusals import UnsupportedByThisProfile, WantOfState

#: `(schema, table)` — the object key. `schema` may be `None`, which is a POSITIVE claim that no
#: schema qualification applies and never a dropped one; `None` and `"sales"` are different keys.
ObjectKey = Tuple[Optional[str], str]


@dataclass(frozen=True)
class InMemoryArrowSource:
    """One deterministic material source, held as Arrow tables in this process.

    `objects` is keyed by `(schema, table)` so that the endpoint's qualification is what selects,
    and `name` exists only so a refusal can say which source could not answer."""

    name: str
    objects: Mapping[ObjectKey, pa.Table]

    def object_for(self, schema: Optional[str], table: str) -> pa.Table:
        key: ObjectKey = (schema, table)
        obj = self.objects.get(key)
        if obj is None:
            raise WantOfState(
                f"source {self.name!r} holds no object {_spell_object(schema, table)}; it holds "
                f"{_spell_objects(self.objects)}", subject=self.name)
        return obj

    def column(self, schema: Optional[str], table: str, column: str) -> pa.Array:
        obj = self.object_for(schema, table)
        if column not in obj.column_names:
            raise WantOfState(
                f"object {_spell_object(schema, table)} in source {self.name!r} has no column "
                f"{column!r}; it has {sorted(obj.column_names)}", subject=self.name)
        return obj.column(column).combine_chunks()


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

    columns = {}
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
        columns[name] = source.column(cep.schema, cep.table, cep.column)

    values = source.column(ep.schema, ep.table, ep.column)
    heights = {name: len(arr) for name, arr in columns.items()}
    if any(h != len(values) for h in heights.values()):
        raise WantOfState(
            f"the material columns are not of one length: value column has {len(values)} rows, "
            f"coordinates have {heights}", subject=family_realization.family_id)

    table = pa.table({**columns, value_column: values})
    return AnchoredCarrier(
        table=table, value_column=value_column, anchor_columns=tuple(sorted(columns)),
        measured_as=(f"in-memory arrow source {source.name!r} via connection {ep.connection!r}, "
                     f"object {_spell_object(ep.schema, ep.table)}, column {ep.column!r}"),
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

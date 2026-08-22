"""
columna_core.compiler.inputs — the compiler's ONLY two inputs, read as plain data.

    compile(governed_publication, private_core_mapping) -> Core-private execution image

Both are read with the **standard library only**. That is not an aesthetic choice: it is what keeps
the two trees import-disjoint. ``columna-server`` already ingests ``governed-publication.json``
without importing ``manifold_agent`` — a property its own test pins by asserting the module never
enters ``sys.modules`` — and the compiler inherits exactly that discipline for both inputs.

WHAT THE COMPILER MAY NOT TOUCH (ruled, and enforced by construction — there is no code here that
could reach them): Studio session state · ``Declaration.evidence`` · audit/profile objects ·
``manifold.columna.yaml`` · ``draft.lower_to_cml`` output. A missing input is a refusal, never a
repair. If the publication does not carry the meaning, stop; if the mapping does not carry the
realization, report a mapping gap; in neither case may the compiler invent the missing fact.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

from .refusals import (
    InputIdentityMismatch,
    LogicalMeaningMissing,
    MappingIncomplete,
)

#: The publication-artifact format major this compiler understands. Its own dimension — unrelated to
#: the mapping format, the receipt format, the wire contract or the engine version.
SUPPORTED_PUBLICATION_FORMAT_MAJOR = 1

#: The private-mapping format major this compiler understands, and the value K0 producers write.
#: Deliberately NOT `manifold_agent`'s `mapping_version = "0.1"`, which versions a different object.
MAPPING_FORMAT_VERSION = "1"
SUPPORTED_MAPPING_FORMAT_MAJOR = 1


# ── the governed publication ─────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class PublicationRef:
    """A concrete governed identity. Never ambiguous, never range-resolved."""

    manifold_id: str
    version: str

    def __str__(self) -> str:                      # pragma: no cover - diagnostics only
        return f"{self.manifold_id}@{self.version}"


@dataclass(frozen=True)
class Declaration:
    """One authored declaration, declaration-native: ``{kind, name, body}``.

    The body is the AUTHORING vocabulary, physical-clean by construction upstream. The compiler
    reads it; it never writes to it, and it never enriches it from a physical source."""

    kind: str
    name: str
    body: dict


@dataclass(frozen=True)
class GovernedPublication:
    """The shared governed authority, as plain data."""

    format_version: str
    ref: PublicationRef
    declarations: tuple
    authority: dict = field(default_factory=dict)

    def of_kind(self, kind: str) -> tuple:
        return tuple(d for d in self.declarations if d.kind == kind)

    def by_name(self, kind: str, name: str) -> Optional[Declaration]:
        for d in self.declarations:
            if d.kind == kind and d.name == name:
                return d
        return None


def _major(version: Any, what: str) -> int:
    try:
        return int(str(version).split(".", 1)[0])
    except (ValueError, AttributeError) as exc:
        raise LogicalMeaningMissing(
            f"unreadable {what} {version!r}: expected 'MAJOR' or 'MAJOR.MINOR'"
        ) from exc


def parse_publication(data: Any) -> GovernedPublication:
    """Structurally read a ``governed-publication.json``. Says nothing about compilability."""
    if not isinstance(data, dict):
        raise LogicalMeaningMissing("publication artifact is not a JSON object")

    fmt = data.get("publication_format_version")
    if not isinstance(fmt, str) or not fmt:
        raise LogicalMeaningMissing("missing publication_format_version")
    if _major(fmt, "publication_format_version") != SUPPORTED_PUBLICATION_FORMAT_MAJOR:
        raise LogicalMeaningMissing(
            f"publication_format_version {fmt!r} has an unsupported major (this compiler supports "
            f"major {SUPPORTED_PUBLICATION_FORMAT_MAJOR})"
        )

    ref = data.get("ref")
    if not isinstance(ref, dict):
        raise LogicalMeaningMissing("missing ref object")
    mid, ver = ref.get("manifold_id"), ref.get("version")
    if not isinstance(mid, str) or not mid or not isinstance(ver, str) or not ver:
        raise LogicalMeaningMissing("ref must carry a concrete manifold_id and version")

    logical = data.get("logical")
    if not isinstance(logical, dict):
        raise LogicalMeaningMissing("missing logical projection")
    decls = logical.get("declarations")
    if not isinstance(decls, list):
        raise LogicalMeaningMissing("logical.declarations must be a list")

    out = []
    for i, d in enumerate(decls):
        if not isinstance(d, dict):
            raise LogicalMeaningMissing(f"declaration {i} is not an object")
        kind, name, body = d.get("kind"), d.get("name"), d.get("body")
        if not isinstance(kind, str) or not kind:
            raise LogicalMeaningMissing(f"declaration {i} has no kind")
        if not isinstance(name, str) or not name:
            raise LogicalMeaningMissing(f"declaration {i} ({kind}) has no name")
        out.append(Declaration(kind, name, body if isinstance(body, dict) else {}))

    authority = data.get("authority")
    return GovernedPublication(
        format_version=fmt,
        ref=PublicationRef(mid, ver),
        declarations=tuple(out),
        authority=authority if isinstance(authority, dict) else {},
    )


# ── the private core mapping ─────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Endpoint:
    """A fully-resolved physical location. The mapping stores it resolved; the compiler never
    re-derives one from evidence, profile, or anything else."""

    connection: str
    table: str
    column: Optional[str] = None
    schema: Optional[str] = None


@dataclass(frozen=True)
class AnchorComponentRealization:
    """A-coord: the NAMED coordinate -> physical column association.

    Named, never positional. The historic anchor binding carried ``grain=tuple(keys)`` with no
    component association at all — 1:1 only by accident for a single key — which is exactly the gap
    this closes. Tuple position is not identity."""

    anchor_ref: str
    component_name: str
    endpoint: Endpoint


@dataclass(frozen=True)
class MemberRealization:
    """How one governed member is physically realized, plus the reducer that realizes it.

    ``root_evaluator`` is captured, never invented: a compiler that chose a reducer would be
    manufacturing analytical law."""

    measure_ref: str
    member_ref: str
    universe_ref: str
    anchor_ref: str
    endpoint: Endpoint
    root_evaluator: str


@dataclass(frozen=True)
class PrivateCoreMapping:
    """The private realization contract. Bound to exactly one immutable publication."""

    mapping_format_version: str
    publication_ref: PublicationRef
    anchor_components: tuple = ()
    members: tuple = ()


def _endpoint(obj: Any, subject: str) -> Endpoint:
    if not isinstance(obj, dict):
        raise MappingIncomplete("endpoint is not an object", subject=subject)
    conn, table = obj.get("connection"), obj.get("table")
    if not isinstance(conn, str) or not conn:
        raise MappingIncomplete("endpoint.connection is required and must be resolved",
                                subject=subject)
    if not isinstance(table, str) or not table:
        raise MappingIncomplete("endpoint.table is required and must be resolved", subject=subject)
    col, schema = obj.get("column"), obj.get("schema")
    if col is not None and (not isinstance(col, str) or not col):
        raise MappingIncomplete("endpoint.column, when present, must be a non-empty string",
                                subject=subject)
    if schema is not None and not isinstance(schema, str):
        raise MappingIncomplete("endpoint.schema, when present, must be a string", subject=subject)
    return Endpoint(connection=conn, table=table, column=col, schema=schema)


def parse_mapping(data: Any) -> PrivateCoreMapping:
    """Structurally read a ``private-core-mapping.json``.

    Unknown realization kinds REFUSE rather than being ignored. The receipt ignores unknown keys
    because it must never become a channel for meaning; the mapping is the opposite case — an
    unrecognised realization is realization the compiler would silently fail to carry."""
    if not isinstance(data, dict):
        raise MappingIncomplete("private mapping is not a JSON object")

    fmt = data.get("mapping_format_version")
    if not isinstance(fmt, str) or not fmt:
        raise MappingIncomplete("missing mapping_format_version")
    if _major(fmt, "mapping_format_version") != SUPPORTED_MAPPING_FORMAT_MAJOR:
        raise MappingIncomplete(
            f"mapping_format_version {fmt!r} has an unsupported major (this compiler supports "
            f"major {SUPPORTED_MAPPING_FORMAT_MAJOR})"
        )

    ref = data.get("publication_ref")
    if not isinstance(ref, dict):
        raise MappingIncomplete("missing publication_ref object")
    mid, ver = ref.get("manifold_id"), ref.get("version")
    if not isinstance(mid, str) or not mid or not isinstance(ver, str) or not ver:
        raise MappingIncomplete("publication_ref must carry a concrete manifold_id and version")

    rs = data.get("realizations")
    if not isinstance(rs, list):
        raise MappingIncomplete("realizations must be a list")

    anchors, members = [], []
    for i, r in enumerate(rs):
        if not isinstance(r, dict):
            raise MappingIncomplete(f"realization {i} is not an object")
        kind = r.get("kind")
        subject = f"realization {i}"
        if kind == "anchor_component":
            a, c = r.get("anchor_ref"), r.get("component_name")
            if not isinstance(a, str) or not a:
                raise MappingIncomplete("anchor_component.anchor_ref is required", subject=subject)
            if not isinstance(c, str) or not c:
                raise MappingIncomplete("anchor_component.component_name is required",
                                        subject=subject)
            ep = _endpoint(r.get("endpoint"), f"anchor_component {a}.{c}")
            if ep.column is None:
                raise MappingIncomplete("an anchor component must realize a concrete column",
                                        subject=f"anchor_component {a}.{c}")
            anchors.append(AnchorComponentRealization(a, c, ep))
        elif kind == "member":
            need = ("measure_ref", "member_ref", "universe_ref", "anchor_ref")
            vals = {k: r.get(k) for k in need}
            for k, v in vals.items():
                if not isinstance(v, str) or not v:
                    raise MappingIncomplete(f"member.{k} is required", subject=subject)
            ev = r.get("root_evaluator")
            if not isinstance(ev, str) or not ev:
                raise MappingIncomplete(
                    "member.root_evaluator is required — a compiler never invents a reducer",
                    subject=f"member {vals['member_ref']}")
            ep = _endpoint(r.get("endpoint"), f"member {vals['member_ref']}")
            members.append(MemberRealization(vals["measure_ref"], vals["member_ref"],
                                             vals["universe_ref"], vals["anchor_ref"], ep, ev))
        else:
            raise MappingIncomplete(
                f"unknown realization kind {kind!r} — K0 realizes 'anchor_component' and 'member' "
                f"only; an unrecognised realization is realization the compiler cannot carry",
                subject=subject)

    return PrivateCoreMapping(
        mapping_format_version=fmt,
        publication_ref=PublicationRef(mid, ver),
        anchor_components=tuple(anchors),
        members=tuple(members),
    )


def require_same_publication(pub: GovernedPublication, mapping: PrivateCoreMapping) -> None:
    """The precondition, checked BEFORE any lowering.

    Exact equality on both fields — no semver ranges, no 'close enough'. A mapping for a different
    publication is not a degraded input; it is a different input."""
    if mapping.publication_ref != pub.ref:
        raise InputIdentityMismatch(
            f"mapping realizes {mapping.publication_ref} but the artifact is {pub.ref}"
        )


def load_publication(path: str) -> GovernedPublication:
    with open(path, encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError as exc:
            raise LogicalMeaningMissing(f"publication artifact is not valid JSON: {exc}") from exc
    return parse_publication(raw)


def load_mapping(path: str) -> PrivateCoreMapping:
    with open(path, encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError as exc:
            raise MappingIncomplete(f"private mapping is not valid JSON: {exc}") from exc
    return parse_mapping(raw)

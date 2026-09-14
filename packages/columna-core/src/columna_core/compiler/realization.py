"""
columna_core.compiler.realization — the private realization mapping, format v2.

WHAT A REALIZATION IS ALLOWED TO SAY (ruled 2026-09-11). It refers to an ALREADY-GOVERNED family by
`family_id` and cannot supply identity-bearing law:

  1. the family it realizes, BY `family_id` ONLY — never by name, never by reducer, never by position;
  2. the endpoint(s);
  3. a GRAIN-CORRESPONDENCE CLAIM — how the physical source grain relates to the family's
     constitutive anchor: coincident, or finer;
  4. a DELIVERY CLAIM — the backend operator that discharges the declared law, and whether it does so
     exactly or approximately;
  5. realization evidence (freshness, data-state version, producer attestation) — out of K0's scope
     and named here so its absence is deliberate rather than forgotten.

WHAT IT MAY NEVER SAY: which reducer makes the family what it is · how contributions resolve into a
constituted value · which anchor is constitutive · who the parents are · what the participation is.
**Nothing whose change would change `Σ(F)`.** In v1 exactly one field — `root_evaluator` — said the
first two of those, which is why a private file could mint a family succession under ToD v7.1 §3.9.

THE GUARANTEE IS STRUCTURAL, NOT A RULE TO REMEMBER. `family_id` is not derivable from anything in
this file: THIS READER never computes one and never falls back to a name, so a mapping edit cannot be
a family succession — it cannot change which family is being realized, it can only fail to match one.

AND THE OTHER HALF IS NOT THIS MODULE'S TO GIVE (corrected 2026-09-14, OF-40). §4's rule is
"missing, duplicate and UNKNOWN all refuse", and the three are discharged in two different places.
The reader owns the two it can see from the bytes alone — a realization with no `family_id`, and two
realizations naming one. It cannot own the third: `parse_mapping` is handed a document and no
publication, so "the publication does not declare this family" is a sentence it has no standing to
say. That check lives in `compile_v2._check_realization_family_references`, beside the binding check.
Until it was written, this docstring claimed it and nothing in the tree performed it.

THE CLAIM/CHECK INVERSION. Every field above is a CLAIM the compiler checks against governed law,
never a fact the compiler adopts. That is the same shape the v1 compiler already used correctly for
anchor components (it checked the mapping's components against the publication's) and backwards for
members (it read the family out of the mapping). Members now look like anchors.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Optional

from .refusals import InputIdentityMismatch, MappingIncomplete

#: The private-mapping format v2 producers write. Its own dimension.
#: `mapping_format_version` is a BARE MAJOR a loader keys on — never "2.0" or "0.1".
#: Anchored so an unrecognised spelling refuses rather than being truncated to its head.
_FORMAT_VERSION = re.compile(r"^\d+$")

MAPPING_FORMAT_VERSION = "2"
SUPPORTED_MAPPING_FORMAT_MAJOR = 2

#: Grain-correspondence claims. `COINCIDENT` says one source row per analytical point; `FINER` says
#: several, and therefore that the family's formation must establish how they resolve — which is
#: analytical law, and is exactly what `root_evaluator` used to supply from this side of the wall.
COINCIDENT, FINER = "coincident", "finer"
GRAINS = frozenset({COINCIDENT, FINER})

EXACT, APPROXIMATE = "exact", "approximate"


@dataclass(frozen=True)
class Endpoint:
    connection: str
    table: str
    column: Optional[str] = None
    schema: Optional[str] = None


@dataclass(frozen=True)
class AnchorComponentRealization:
    anchor_ref: str
    component_name: str
    endpoint: Endpoint


@dataclass(frozen=True)
class FamilyRealization:
    """How one governed family is realized here. Claims only.

    `formation_operator` is the backend operator this realization claims discharges the family's
    DECLARED formation law — a claim checked against the law, not a choice of law. Where the family
    is primitive and the grain is coincident there is nothing to aggregate, so it is absent."""

    family_id: str
    endpoint: Endpoint
    grain: str
    formation_operator: Optional[str] = None
    continuation_operator: Optional[str] = None
    exactness: str = EXACT


@dataclass(frozen=True)
class PublicationRef:
    manifold_id: str
    version: str

    def __str__(self) -> str:
        return f"{self.manifold_id}@{self.version}"


@dataclass(frozen=True)
class PrivateCoreMappingV2:
    mapping_format_version: str
    publication_ref: PublicationRef
    anchor_components: tuple = ()
    families: tuple = ()

    def for_family(self, family_id: str) -> Optional[FamilyRealization]:
        for r in self.families:
            if r.family_id == family_id:
                return r
        return None


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
    for key, val in (("column", col), ("schema", schema)):
        if val is not None and (not isinstance(val, str) or not val):
            raise MappingIncomplete(f"endpoint.{key}, when present, must be a non-empty string",
                                    subject=subject)
    extra = sorted(set(obj) - {"connection", "table", "column", "schema"})
    if extra:
        raise MappingIncomplete(f"endpoint carries unrecognised key(s) {extra}", subject=subject)
    return Endpoint(conn, table, col, schema)


#: CLOSED AT ALL THREE LEVELS (freeze §8): top level, per realization kind, and endpoint. The top
#: level was open — an unrecognised key was silently ignored, which is the one outcome a closed
#: format may not have: a producer writing a key this reader does not know would have been told
#: nothing, and would have believed the claim was carried.
_TOP_KEYS = frozenset({"mapping_format_version", "publication_ref", "realizations"})

_FAMILY_KEYS = frozenset({"kind", "family_id", "endpoint", "grain", "formation_operator",
                          "continuation_operator", "exactness"})
_ANCHOR_KEYS = frozenset({"kind", "anchor_ref", "component_name", "endpoint"})


def parse_mapping(data: Any) -> PrivateCoreMappingV2:
    if not isinstance(data, dict):
        raise MappingIncomplete("private mapping is not a JSON object")
    fmt = data.get("mapping_format_version")
    if not isinstance(fmt, str) or not fmt:
        raise MappingIncomplete("missing mapping_format_version")
    # SHAPE FIRST, THEN VALUE (freeze §6). `int(fmt.split(".", 1)[0])` accepted "2.5" as major 2 —
    # it truncated a version string this format does not define instead of refusing it. A reader that
    # silently normalizes an unrecognised spelling has decided what it means.
    if not _FORMAT_VERSION.match(fmt):
        raise MappingIncomplete(
            f"unreadable mapping_format_version {fmt!r}: this format is a bare MAJOR (\"2\"), and a "
            f"reader may not guess at another spelling")
    major = int(fmt.split(".", 1)[0])
    if major != SUPPORTED_MAPPING_FORMAT_MAJOR:
        raise MappingIncomplete(
            f"mapping_format_version {fmt!r} has major {major}; this build reads major "
            f"{SUPPORTED_MAPPING_FORMAT_MAJOR}. A v1 mapping keyed realizations by `member_ref` and "
            f"carried `root_evaluator`, which is family law and no longer lives here.")

    extra_top = sorted(set(data) - _TOP_KEYS)
    if extra_top:
        raise MappingIncomplete(
            f"private mapping carries unrecognised top-level key(s) {extra_top}; the key set is "
            f"closed, and an unrecognised key is never ignored")

    ref = data.get("publication_ref")
    if not isinstance(ref, dict):
        raise MappingIncomplete("missing publication_ref")
    mid, ver = ref.get("manifold_id"), ref.get("version")
    if not isinstance(mid, str) or not mid or not isinstance(ver, str) or not ver:
        raise MappingIncomplete("publication_ref must carry a concrete manifold_id and version")

    rows = data.get("realizations")
    if not isinstance(rows, list):
        raise MappingIncomplete("realizations must be a list")

    anchors, families, seen, seen_components = [], [], set(), set()
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            raise MappingIncomplete(f"realization {i} is not an object")
        kind = r.get("kind")
        if kind == "anchor_component":
            extra = sorted(set(r) - _ANCHOR_KEYS)
            if extra:
                raise MappingIncomplete(f"anchor_component carries unrecognised key(s) {extra}",
                                        subject=f"realization {i}")
            a, c = r.get("anchor_ref"), r.get("component_name")
            if not isinstance(a, str) or not a or not isinstance(c, str) or not c:
                raise MappingIncomplete("anchor_component needs anchor_ref and component_name",
                                        subject=f"realization {i}")
            # DUPLICATE DETECTION BELONGS WITH THE OTHER TOTALITY RULES (freeze §8). Duplicate
            # FAMILY realizations already refused here; duplicate anchor components were caught only
            # later, in the profile — so one artifact defect refused in two different places
            # depending on which key it was on, and a reader used outside the profile saw neither.
            if (a, c) in seen_components:
                raise MappingIncomplete(
                    f"anchor component {a}.{c} is realized more than once; every authored anchor "
                    f"component maps to exactly one realization", subject=f"realization {i}")
            seen_components.add((a, c))
            anchors.append(AnchorComponentRealization(a, c, _endpoint(r.get("endpoint"),
                                                                     f"anchor_component {a}.{c}")))
        elif kind == "family":
            extra = sorted(set(r) - _FAMILY_KEYS)
            if extra:
                raise MappingIncomplete(f"family realization carries unrecognised key(s) {extra}",
                                        subject=f"realization {i}")
            fid = r.get("family_id")
            if not isinstance(fid, str) or not fid:
                raise MappingIncomplete(
                    "family realization must name a family_id — a realization refers to an "
                    "already-governed family by identity, and this reader never derives one",
                    subject=f"realization {i}")
            if fid in seen:
                raise MappingIncomplete(f"family {fid!r} is realized more than once")
            seen.add(fid)
            grain = r.get("grain")
            if "grain" not in r:
                # ABSENCE AND ERROR ARE DIFFERENT REFUSALS (freeze §8). Both used to produce
                # "None not in GRAINS", which told a producer that it had written something wrong
                # rather than that it had written nothing.
                raise MappingIncomplete(
                    "family realization declares no grain. The correspondence between the physical "
                    "source grain and the constitutive anchor is a CLAIM, and a mapping that does "
                    "not make it has not been written yet", subject=f"family {fid}")
            if grain not in GRAINS:
                raise MappingIncomplete(
                    f"grain must be one of {sorted(GRAINS)} — the correspondence between the "
                    f"physical source grain and the constitutive anchor is a CLAIM this mapping "
                    f"must make, not something the compiler may assume",
                    subject=f"family {fid}")
            exactness = r.get("exactness", EXACT)
            if exactness not in (EXACT, APPROXIMATE):
                raise MappingIncomplete(
                    f"exactness must be {EXACT!r} or {APPROXIMATE!r}; an undisclosed approximation "
                    f"is exactly what ToD §10.9 forbids", subject=f"family {fid}")
            for key in ("formation_operator", "continuation_operator"):
                v = r.get(key)
                if v is not None and (not isinstance(v, str) or not v):
                    raise MappingIncomplete(f"{key}, when present, must be a non-empty string",
                                            subject=f"family {fid}")
            families.append(FamilyRealization(
                fid, _endpoint(r.get("endpoint"), f"family {fid}"), grain,
                r.get("formation_operator"), r.get("continuation_operator"), exactness))
        else:
            raise MappingIncomplete(
                f"unknown realization kind {kind!r} — v2 realizes 'anchor_component' and 'family' "
                f"only; an unrecognised realization is realization the compiler cannot carry",
                subject=f"realization {i}")

    return PrivateCoreMappingV2(fmt, PublicationRef(mid, ver), tuple(anchors), tuple(families))


def load_mapping(path) -> PrivateCoreMappingV2:
    """Read + parse from disk. Malformed JSON refuses in THIS vocabulary (freeze §8).

    Its sibling `load_lowering_receipt` already wraps `json.JSONDecodeError`; this one raised the
    stdlib error straight through, so one of two loaders over the same kind of artifact answered in a
    different language than the other."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return parse_mapping(json.load(fh))
    except json.JSONDecodeError as exc:
        raise MappingIncomplete(f"private mapping is not valid JSON: {exc}") from exc


def require_same_publication(publication, mapping: PrivateCoreMappingV2) -> None:
    """Input authority, before any lowering. Unchanged in intent from v1."""
    p, m = publication.ref, mapping.publication_ref
    if (p.manifold_id, p.version) != (m.manifold_id, m.version):
        raise InputIdentityMismatch(
            f"the mapping realizes {m}, but the publication is {p}. A mapping is bound to exactly "
            f"one immutable publication.")

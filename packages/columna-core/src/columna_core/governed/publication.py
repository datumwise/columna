"""
columna_core.governed.publication — the governed publication, format v2, read as plain data.

WHAT CHANGED FROM v1, AND WHY THE BREAK IS HARD.

v1 carried `measure` / `member` / `boundary`. A v1 `member` body was `{measure, anchor, universe}`,
and in the only real v1 publication all four of a measure's members were BYTE-IDENTICAL: which
family member each one was lived in the PRIVATE MAPPING, as `root_evaluator`. ToD v7.1 §3.9 rules
that *"a change to an identity-bearing target, formation, participation, or declared continuation
law"* IS family succession — so a v1 artifact lets a private realization file mint a succession, and
its meaning is not determined by its own bytes.

**There is therefore no automatic v1 read, and no dual-read shim.** Reading a v1 artifact under this
model would require the consumer to INFER law, which is the exact defect the format exists to
remove. v1 migrates through proposal-and-establishment with a human (`governed.migrate`) or it does
not migrate. `parse_publication` refuses a v1 major with that reason stated.

THE v2 ONTOLOGY. One family kind (`family`), covering primitive and constructed formation and named
and query-constructed alike. `measure`, `member` and `boundary` do not exist: `measure` is retired by
NAME because ToD already defines a Measure as `F@A`; `member` is classified out (some legacy members
are families, some are names); `boundary`'s content is C3 and lives in the family's own contract,
because §4 requires *"one authoritative account"* of each responsibility.

RECORD ECONOMY. Three records a less careful design would have created do not exist here:
  · no `Σ(F)` record — §2.2, *"the signature is not an additional ontological kind"*;
  · no lineage record — a constructed family's formation names its parents by `family_id`, and §3.7
    defines the edge as exactly that, so lineage is DERIVED from formation;
  · no state-schema/combine-law records — they live once, in the cited shared vocabulary.

TOTALITY IS SEMANTIC, NOT LITERAL (ruled 2026-09-11). This module does NOT require every
responsibility to appear in the bytes; serializing a consequence that a cited law already determines
would be redundant. Totality is produced by `governed.resolve`, which yields a canonical `Law(F)`
view in which silence is impossible. What this module does enforce is that nothing is carried that a
consumer cannot name: an unrecognised key in a body it claims to understand is a REFUSAL, because a
key nobody consumes is meaning nobody carried.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

from .foundation import LawCitation, UnknownFoundationLaw

#: The publication format this module reads. Its own dimension — unrelated to the mapping format,
#: the receipt format, the wire contract, the engine version or the foundation vocabulary version.
PUBLICATION_FORMAT_VERSION = "2"
SUPPORTED_PUBLICATION_FORMAT_MAJOR = 2

#: The v1 major, named so the refusal can be specific rather than generic.
RETIRED_PUBLICATION_FORMAT_MAJOR = 1

#: Declaration kinds v2 defines. Others may be carried; a consumer refuses what it cannot represent.
FAMILY = "family"
KNOWN_KINDS = frozenset({"anchor", "universe", FAMILY,
                         "attribute", "relationship", "hierarchy", "crosswalk"})

#: Kinds that v2 RETIRES. Present in a v2 artifact, they are a refusal with their own reason.
RETIRED_KINDS = {
    "measure": ("`measure` is retired: ToD v7.1 §2.2 already defines a Measure as F@A, and the "
                "legacy container carried no analytical identity"),
    "member":  ("`member` is retired: a legacy member is classified — some denote families, some "
                "denote a family's own continuation under another name"),
    "boundary": ("`boundary` is retired as a kind: domain and movement is responsibility C3 and "
                 "lives in the family's own contract (§4, 'one authoritative account')"),
}


class PublicationFormatRefusal(ValueError):
    """The artifact cannot be read as a v2 governed publication.

    A refusal, never a repair: a reader that patched around a format problem would be inventing
    governed content."""


# ── the explicit-none marker ─────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class ExplicitNone:
    """A POSITIVE negative: this responsibility is established, and what it establishes is that
    nothing applies.

    Distinct from absence in every direction. `{"none": "<reason>"}` on the wire. A family whose
    continuation is `ExplicitNone` has DECLARED that it does not compose across refinement — which
    is an identity-bearing statement under §3.9, not a silence."""

    reason: str = ""


def _slot(raw: Any, what: str, reader):
    """Read an optional law slot: content, an explicit none, or absent.

    Returns the reader's value, an `ExplicitNone`, or `None` for absent. Absence is NOT a state this
    module interprets — the resolver decides whether it is entailed or unestablished."""
    if raw is None:
        return None
    if isinstance(raw, dict) and set(raw) == {"none"}:
        reason = raw["none"]
        return ExplicitNone(reason if isinstance(reason, str) else "")
    if isinstance(raw, dict) and "none" in raw:
        raise PublicationFormatRefusal(
            f"{what}: an explicit-none slot carries the single key 'none' and nothing else; "
            f"mixing it with content is neither a declaration nor a none")
    return reader(raw)


def _strict(body: dict, allowed: frozenset, what: str) -> None:
    """Consume-or-refuse at body-key granularity.

    The compiler's standing doctrine is REFUSAL BEFORE OMISSION, and it held at declaration-KIND
    granularity while failing at KEY granularity — which is how a governed `fill_rule` reached a
    compiled image by not being read. Totality of the resolved view (see `resolve`) is what makes
    silence impossible; this is what makes UNREAD content impossible."""
    extra = sorted(set(body) - allowed)
    if extra:
        raise PublicationFormatRefusal(
            f"{what}: unrecognised governed key(s) {extra}. A consumer must consume or refuse every "
            f"semantic field; carrying a key nobody reads is meaning nobody carried. Known keys: "
            f"{sorted(allowed)}")


# ── formation ────────────────────────────────────────────────────────────────────────────────────
PRIMITIVE, CONSTRUCTION = "primitive", "construction"

#: How several source contributions at one point form ONE constituted value. `coincident` claims one
#: contribution per analytical point; `resolved_by` names the law that resolves several.
COINCIDENT = "coincident"


@dataclass(frozen=True)
class Formation:
    """Responsibility C4 — how the analytical input is established.

    PRIMITIVE formation is intake from the universe's governed source at the constitutive anchor. It
    cites no foundation law, because nothing is being computed — which is exactly why a primitive
    family must DECLARE its continuation: there is no formation law to entail one from.

    CONSTRUCTION formation cites a foundation law over parent families. Its continuation is then
    ENTAILED by that law and is not declared (ruling: do not serialize redundant consequences).

    `contribution_structure` is the finding the `the shipped v1 publication` migration surfaced. Where the physical
    source grain is finer than the constitutive anchor, resolving several contributions into one
    constituted value IS analytical law — and in v1 it was supplied silently by `root_evaluator` at
    the realization layer, the same defect D1 found at the continuation end. `None` here means
    UNESTABLISHED, and a compile that needs it refuses."""

    kind: str
    #: PRIMITIVE: COINCIDENT, or a LawCitation resolving several contributions. None = unestablished.
    contribution_structure: Any = None
    #: CONSTRUCTION: the cited formation law.
    law: Optional[LawCitation] = None
    #: CONSTRUCTION: parent family ids, in argument order. THIS IS THE LINEAGE (§3.7).
    operands: tuple = ()
    #: Identity-bearing law parameters (e.g. a constitutive order for FIRST/LAST).
    parameters: dict = field(default_factory=dict)


def _formation(raw: Any, what: str) -> Formation:
    if not isinstance(raw, dict):
        raise PublicationFormatRefusal(f"{what}: formation is not an object")
    kind = raw.get("kind")
    if kind == PRIMITIVE:
        _strict(raw, frozenset({"kind", "contribution_structure"}), f"{what}.formation")
        cs = raw.get("contribution_structure")
        if cs is None:
            structure = None                                   # unestablished, and legitimately so
        elif cs == COINCIDENT:
            structure = COINCIDENT
        elif isinstance(cs, dict) and set(cs) == {"resolved_by"}:
            structure = LawCitation.from_dict(cs["resolved_by"])
        else:
            raise PublicationFormatRefusal(
                f"{what}.formation.contribution_structure: expected {COINCIDENT!r} or "
                f"{{'resolved_by': <law citation>}}; got {cs!r}")
        return Formation(PRIMITIVE, contribution_structure=structure)
    if kind == CONSTRUCTION:
        _strict(raw, frozenset({"kind", "law", "operands", "parameters"}), f"{what}.formation")
        law = LawCitation.from_dict(raw.get("law"))
        ops = raw.get("operands")
        if not isinstance(ops, list) or not ops or not all(
                isinstance(o, str) and o for o in ops):
            raise PublicationFormatRefusal(
                f"{what}.formation.operands: a construction names at least one parent family_id")
        params = raw.get("parameters") or {}
        if not isinstance(params, dict):
            raise PublicationFormatRefusal(f"{what}.formation.parameters is not an object")
        return Formation(CONSTRUCTION, law=law, operands=tuple(ops), parameters=dict(params))
    raise PublicationFormatRefusal(
        f"{what}.formation.kind: expected {PRIMITIVE!r} or {CONSTRUCTION!r}; got {kind!r}")


# ── the family declaration ───────────────────────────────────────────────────────────────────────
_FAMILY_KEYS = frozenset({
    "family_id", "canonical_reference", "aliases", "universe", "constitutive_anchor",
    "target", "formation", "participation", "value_domain",
    "continuation", "domain", "movement", "exceptional",
})


@dataclass(frozen=True)
class Family:
    """One governed MeasureFamily — the analytical identity.

    `family_id` is stable identity, distinct from `canonical_reference`, from the cited
    foundation-law name, from any alias, and from any realization mapping key (§2.2,
    `family_id ≠ canonical_name`). It is OPAQUE here: this module never generates one, never
    regenerates one, and never derives one from content. Generation is the producer's business."""

    family_id: str
    canonical_reference: str
    universe: str
    constitutive_anchor: str
    target: str
    formation: Formation
    #: C5. None = unestablished.
    participation: Optional[str] = None
    #: C6, primitive families only — the operand's own domain. Constructed families derive it.
    value_domain: Optional[str] = None
    #: C8. A citation, an ExplicitNone, or None (absent: entailed for constructions).
    continuation: Any = None
    #: C3. Content, ExplicitNone, or None (absent = unestablished).
    domain: Any = None
    movement: Any = None
    #: C9 — only what the cited law does not already establish.
    exceptional: dict = field(default_factory=dict)
    #: Non-identity reference metadata (ruling 2026-09-11). Never resolved FROM; only resolved TO.
    aliases: tuple = ()

    @property
    def is_primitive(self) -> bool:
        return self.formation.kind == PRIMITIVE

    @property
    def parents(self) -> tuple:
        """The constitutive lineage, DERIVED from formation — §3.7's directed edge, not a record."""
        return self.formation.operands


def _family(name: str, body: dict) -> Family:
    what = f"family {name!r}"
    if not isinstance(body, dict):
        raise PublicationFormatRefusal(f"{what}: body is not an object")
    _strict(body, _FAMILY_KEYS, what)

    def req(key: str) -> str:
        v = body.get(key)
        if not isinstance(v, str) or not v:
            raise PublicationFormatRefusal(f"{what}: {key} is required and must be a non-empty string")
        return v

    fid = req("family_id")
    formation = _formation(body.get("formation"), what)
    aliases = body.get("aliases") or []
    if not isinstance(aliases, list) or not all(isinstance(a, str) and a for a in aliases):
        raise PublicationFormatRefusal(f"{what}: aliases must be a list of non-empty strings")
    exceptional = body.get("exceptional") or {}
    if not isinstance(exceptional, dict):
        raise PublicationFormatRefusal(f"{what}: exceptional is not an object")

    participation = body.get("participation")
    if participation is not None and (not isinstance(participation, str) or not participation):
        raise PublicationFormatRefusal(f"{what}: participation, when present, is a non-empty string")
    vd = body.get("value_domain")
    if vd is not None and (not isinstance(vd, str) or not vd):
        raise PublicationFormatRefusal(f"{what}: value_domain, when present, is a non-empty string")

    return Family(
        family_id=fid,
        canonical_reference=req("canonical_reference"),
        universe=req("universe"),
        constitutive_anchor=req("constitutive_anchor"),
        target=req("target"),
        formation=formation,
        participation=participation,
        value_domain=vd,
        continuation=_slot(body.get("continuation"), f"{what}.continuation", LawCitation.from_dict),
        domain=_slot(body.get("domain"), f"{what}.domain", lambda r: r),
        movement=_slot(body.get("movement"), f"{what}.movement", lambda r: r),
        exceptional=dict(exceptional),
        aliases=tuple(aliases),
    )


# ── authority ────────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class ConstitutionAuthority:
    """Authority over a family's identity-bearing constitution.

    A DISTINCT RECORD TYPE from the universe's existence-law ratification, deliberately (ruled
    2026-09-11). The two attest different objects: a universe's record pins its EXISTENCE LAW under
    the `elf-1` scheme; this pins `Σ(F)`'s identity-bearing content. One record type would let a
    currency check compare incomparable fingerprints, which is worse than having none.

    §4 names three standings and this carries exactly one of them: *"Human ratification establishes
    the declaration's authority in its domain; it does not prove its mathematical laws."* Entailment
    is derived by any consumer from the cited law, so publishing a proof would publish a derivable
    fact; realization capability belongs to the mapping. Neither is here."""

    established_by: str
    at: str
    constitution_fingerprint: str
    fingerprint_scheme: str

    def to_dict(self) -> dict:
        return {"established_by": self.established_by, "at": self.at,
                "constitution_fingerprint": self.constitution_fingerprint,
                "fingerprint_scheme": self.fingerprint_scheme}

    @classmethod
    def from_dict(cls, d: Any, subject: str) -> "ConstitutionAuthority":
        if not isinstance(d, dict):
            raise PublicationFormatRefusal(f"{subject}: constitution authority is not an object")
        need = ("established_by", "at", "constitution_fingerprint", "fingerprint_scheme")
        vals = {}
        for k in need:
            v = d.get(k)
            if not isinstance(v, str) or not v:
                raise PublicationFormatRefusal(f"{subject}: constitution authority needs {k!r}")
            vals[k] = v
        _strict(d, frozenset(need), f"{subject} constitution authority")
        return cls(**vals)


# ── the artifact ─────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class PublicationRef:
    manifold_id: str
    version: str

    def __str__(self) -> str:
        return f"{self.manifold_id}@{self.version}"


@dataclass(frozen=True)
class Declaration:
    kind: str
    name: str
    body: dict


@dataclass(frozen=True)
class GovernedPublicationV2:
    """The shared governed authority, v2, as plain data. Standard library only, by discipline."""

    format_version: str
    ref: PublicationRef
    declarations: tuple
    families: tuple = ()
    #: per-universe existence-law ratification, carried unchanged from v1.
    ratifications: dict = field(default_factory=dict)
    #: per-FAMILY_ID constitution authority — the distinct record type.
    constitution_authority: dict = field(default_factory=dict)
    published_by: str = ""
    published_at: str = ""

    def of_kind(self, kind: str) -> tuple:
        return tuple(d for d in self.declarations if d.kind == kind)

    def family(self, family_id: str) -> Optional[Family]:
        for f in self.families:
            if f.family_id == family_id:
                return f
        return None

    def resolve_reference(self, reference: str) -> Optional[Family]:
        """Name → family. ONE DIRECTION ONLY, and never the reverse for any governed purpose.

        A canonical reference or an alias resolves to at most one family within this publication.
        Two families answering to one reference is a refusal at parse time (§2.2: *"Two distinct
        active identities cannot be hidden under one ambiguous canonical reference"*)."""
        for f in self.families:
            if reference == f.canonical_reference or reference in f.aliases:
                return f
        return None


def _major(version: Any, what: str) -> int:
    try:
        return int(str(version).split(".", 1)[0])
    except (ValueError, AttributeError) as exc:
        raise PublicationFormatRefusal(f"unreadable {what} {version!r}") from exc


def parse_publication(data: Any) -> GovernedPublicationV2:
    if not isinstance(data, dict):
        raise PublicationFormatRefusal("publication artifact is not a JSON object")
    fmt = data.get("publication_format_version")
    if not isinstance(fmt, str) or not fmt:
        raise PublicationFormatRefusal("missing publication_format_version")
    major = _major(fmt, "publication_format_version")
    if major == RETIRED_PUBLICATION_FORMAT_MAJOR:
        raise PublicationFormatRefusal(
            "this is a publication-format v1 artifact, and there is NO automatic v1 read. A v1 "
            "artifact under-determines its own meaning: its family law lives in a private "
            "realization mapping, so reading it here would require inferring analytical law — the "
            "exact defect v2 exists to remove. Migrate it through proposal-and-establishment "
            "(`columna_core.governed.migrate`), with a human.")
    if major != SUPPORTED_PUBLICATION_FORMAT_MAJOR:
        raise PublicationFormatRefusal(
            f"publication_format_version {fmt!r} has major {major}; this build reads major "
            f"{SUPPORTED_PUBLICATION_FORMAT_MAJOR}")

    ref = data.get("ref")
    if not isinstance(ref, dict):
        raise PublicationFormatRefusal("missing ref object")
    mid, ver = ref.get("manifold_id"), ref.get("version")
    if not isinstance(mid, str) or not mid or not isinstance(ver, str) or not ver:
        raise PublicationFormatRefusal("ref must carry a concrete manifold_id and version")

    logical = data.get("logical")
    if not isinstance(logical, dict):
        raise PublicationFormatRefusal("missing logical projection")
    decls_raw = logical.get("declarations")
    if not isinstance(decls_raw, list):
        raise PublicationFormatRefusal("logical.declarations must be a list")

    decls, families, seen_ids, seen_refs = [], [], {}, {}
    for i, d in enumerate(decls_raw):
        if not isinstance(d, dict):
            raise PublicationFormatRefusal(f"declaration {i} is not an object")
        kind, name, body = d.get("kind"), d.get("name"), d.get("body")
        if not isinstance(kind, str) or not kind:
            raise PublicationFormatRefusal(f"declaration {i} has no kind")
        if not isinstance(name, str) or not name:
            raise PublicationFormatRefusal(f"declaration {i} ({kind}) has no name")
        if kind in RETIRED_KINDS:
            raise PublicationFormatRefusal(
                f"declaration {name!r}: {RETIRED_KINDS[kind]}. A v2 artifact may not carry it.")
        body = body if isinstance(body, dict) else {}
        decls.append(Declaration(kind, name, body))
        if kind == FAMILY:
            try:
                fam = _family(name, body)
            except UnknownFoundationLaw as exc:
                raise PublicationFormatRefusal(f"family {name!r}: {exc}") from exc
            if fam.family_id in seen_ids:
                raise PublicationFormatRefusal(
                    f"family_id {fam.family_id!r} is declared twice ({seen_ids[fam.family_id]!r} "
                    f"and {name!r}); identity is not a label")
            seen_ids[fam.family_id] = name
            for reference in (fam.canonical_reference,) + fam.aliases:
                if reference in seen_refs:
                    raise PublicationFormatRefusal(
                        f"reference {reference!r} resolves to two families ({seen_refs[reference]} "
                        f"and {fam.family_id}); §2.2 — two distinct active identities cannot be "
                        f"hidden under one ambiguous canonical reference")
                seen_refs[reference] = fam.family_id
            families.append(fam)

    authority = data.get("authority")
    authority = authority if isinstance(authority, dict) else {}
    rats = authority.get("ratifications") or {}
    ca_raw = authority.get("family_constitution") or {}
    if not isinstance(ca_raw, dict):
        raise PublicationFormatRefusal("authority.family_constitution must be an object")
    ca = {k: ConstitutionAuthority.from_dict(v, f"family_id {k!r}") for k, v in ca_raw.items()}
    for fid in ca:
        if fid not in seen_ids:
            raise PublicationFormatRefusal(
                f"authority.family_constitution names family_id {fid!r}, which this publication "
                f"does not declare. Authority must never outlive the thing it attests.")

    return GovernedPublicationV2(
        format_version=fmt,
        ref=PublicationRef(mid, ver),
        declarations=tuple(decls),
        families=tuple(families),
        ratifications=dict(rats) if isinstance(rats, dict) else {},
        constitution_authority=ca,
        published_by=str(authority.get("published_by", "")),
        published_at=str(authority.get("published_at", "")),
    )


def load_publication(path) -> GovernedPublicationV2:
    with open(path, "r", encoding="utf-8") as fh:
        return parse_publication(json.load(fh))

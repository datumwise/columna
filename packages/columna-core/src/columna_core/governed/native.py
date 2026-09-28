"""
columna_core.governed.native — the native publication, format v3, read as plain data, and the
RESOLVED MODEL it yields.

C1 of the native-consumer sequence (`manifold-agent/docs/native_v3_consumer_recon_v0_1.md` §13):
*the v3 reader, and nothing else*. **No serving, no Platform, no engine, no compilation.** Nothing
in this module imports `columna_server`, `columna_platform`, or any part of `columna_core` outside
`governed`, and nothing here reaches the producer.

WHY THIS IS A NEW MODULE AND NOT A DEEPER `publication.py`
---------------------------------------------------------
Ruled (Huayin, 2026-09-22): *"Native v3 must not be translated back into the legacy model… Do not
build compile_v3 as an evolution of compile_v2."* The v2 reader's model is a publication-global map
of `anchor` declarations, a `universe.body` carrying `anchor`/`basis`/`restriction`, and a
top-level `authority` section keyed two different ways. **None of those objects exists natively**,
and the native artifact has no `logical` wrapper, no `body` on a universe, and no `anchor` kind at
all. A reader that shared a code path with v2 would have to keep those objects alive to have
somewhere to put what it read. So: a separate reader, a separate model, and **neither major is a
shim for the other** — the discipline `columna_server.registry._READERS` already states for v1/v2.

**THE MAJOR GATE IS NOT A FORMALITY.** Measured during the reconnaissance: relabel a v3 artifact as
`"2.0"` and wrap its declarations under `logical`, and the v2 reader *accepts it* — silently
discarding the constitution, the conformance judgment, the attestation, the denotation table and
every authority record, then reporting *"a universe stating no law"*. The refusal that presently
keeps v3 out of `_load_governed_only` is preventing a real silent semantic loss, and this module is
how that refusal is lifted: **by reading v3 as v3**, never by relabelling it (ruling 5).

WHAT THE ARTIFACT CARRIES, AND WHY NOTHING IS FETCHED
-----------------------------------------------------
Every governed fact this reader checks is checkable **from the bytes in front of it** — `elf-2`
recomputes from the carried constitution, F4's coverage re-derives from that same constitution, a
family's U-authority binding is compared against the attestation carried on the universe beside it,
and `fcf-1`/`fcf-2` recompute from the family's own body. That is the dividend of keeping the
constitution inside the publication (native ruling N3), and it is what makes a second, independent
implementation of the currency contract *possible* rather than presumptuous.

THE ONE THING TO KNOW ABOUT THIS FILE: IT IS A SECOND IMPLEMENTATION
--------------------------------------------------------------------
The producer (`manifold_agent`) implements the same canonicalization. This consumer may not import
it — the server/core tree is deliberately disjoint from the producer, and that disjointness is
test-enforced — so the canonical payloads below are **re-derived from the governed facts**, exactly
as the producer's own rule requires (*"using the serialization as the definition would allow a
convenient serialization to define what the attestation means"*). Two independent derivations of
one contract need a witness that they agree, and that witness is the shipped fixture: a digest that
does not reproduce is a refusal here, so drift cannot be silent. **This is recorded as the
consumer's standing obligation, not hidden as an implementation detail.**

WHAT IS DELIBERATELY ABSENT
---------------------------
* **No anchor declarations, no publication-global anchor map, no `universe.body.anchor`, no basis,
  no LEVEL/HIERARCHY, no global coordinate namespace.** Not "not yet" — there is nowhere in this
  model to put one. If something below `Law(F)` later needs one, that dependency gets reported
  (ruling 4), never satisfied by bending the artifact.
* **No repair of the v2 reader's silent acceptance** (P2-01, ruling 6) and **no cleanup of legacy
  machinery** (ruling 8). Construction, not demolition.
* **No movement.** P1-33's repair is held, and its native contract is derived later from the native
  model, never migrated from the current implementation (ruling 3).
* **No carrier/type information anywhere.** The coordinate-type question belongs to realization
  (ruling 7); admission's type check is C4's subject and is not anticipated here.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, NoReturn, Optional

# ── format ───────────────────────────────────────────────────────────────────────────────────────
#: The native contract this module reads. **Complete MAJOR.MINOR, and the minor is required** (N9).
#:
#: **v3.0 → v3.1, 2026-09-28: the governed-expression sort is admitted.** ADDITIVE, and the word is
#: exact: v3.0 artifacts are BYTE-IDENTICAL IN MEANING and are read by this build unchanged, because
#: they carry no expression declarations and nothing about a family's reading moved. What changed is
#: that one more declaration kind now has positive standing — and `ADMITTED_KINDS_BY_VERSION` makes
#: that standing minor-relative, so a v3.0 artifact carrying an expression is still refused.
#:
#: **THIS LINE IS THE LAST THING THAT MOVED IN V8-1, DELIBERATELY** (ordered by Huayin, 2026-09-28:
#: *"body contract → resolver/validation → Σ(E)/succession → tests → only then add `expression` to
#: `ADMITTED_KINDS` and `"3.1"` to `SUPPORTED_NATIVE_VERSIONS`"*). The sort token is cheap and the
#: constitution is not; admitting a kind before its body contract, its resolver and its
#: canonicalization exist would be admitting a name.
NATIVE_PUBLICATION_FORMAT_VERSION = "3.1"

#: The MAJOR selecting the native semantic publication model.
SUPPORTED_NATIVE_MAJOR = 3

#: The COMPLETE version strings this build explicitly understands. A SET, for the reason the
#: server's supported-majors is a set: compatibility must be **known, not presumed**. Adding
#: `"3.1"` is a deliberate act stating this reader understands that contract — never inferred from
#: `3.1 > 3.0`. v2 computes `int(version.split(".")[0])` and discards the remainder, so `"2.7"`
#: reads as v2; that hole is not reproduced, and it is not retro-fitted to v1/v2 either (ruling 6).
#:
#: **`"3.1"` IS ADDED HERE BY A DELIBERATE ACT, WHICH IS THE WHOLE OF WHAT THIS SET MEANS.** Its own
#: docstring says compatibility must be KNOWN, not presumed, and never inferred from `3.1 > 3.0`; this
#: build understands the v3.1 contract because the expression body contract, its resolver, its `ecf-1`
#: canonicalization and its succession rule are all in this tree. `"3.0"` stays, and stays FIRST: a
#: v3.0 artifact is not migrated, is not relabelled, and is not read through a v3.1 lens.
#:
#: An older reader, whose copy of this set is `("3.0",)`, REFUSES a v3.1 artifact — and that is the
#: contract working, not breaking. `read_version` says so in the refusal itself.
SUPPORTED_NATIVE_VERSIONS: tuple[str, ...] = ("3.0", "3.1")

#: **Positively admitted** declaration kinds, **PER MINOR**. A kind is admitted because something
#: licenses it, never because an earlier format carried it. `anchor` is absent because Case-S anchors
#: are DERIVED (§5/N2) and Case G is unadmitted; `hierarchy`, `relationship`, `attribute` and
#: `crosswalk` have no native standing.
#:
#: **WHY THIS IS A MAP AND NOT A SET, AS OF v3.1.** `expression` is admitted at v3.1 and at NO
#: EARLIER MINOR, and that is the whole of what "additive" means here. A v3.0 artifact carrying an
#: expression declaration is REFUSED — not because the sort is unlawful, but because v3.0's contract
#: does not admit it, and a reader that accepted one would be deciding on the artifact's behalf that
#: the minor it declared was a formality. Compatibility among minors is KNOWN, not presumed (N9), and
#: a kind set that ignored the minor would be presuming it in the one direction that loses meaning:
#: silently reading a sort the declaring contract never claimed to carry.
#:
#: The converse direction is the contract's own design and needs nothing here: a v3.0-only reader
#: refuses a v3.1 artifact at `read_version`, because `"3.1"` is not in ITS `SUPPORTED_NATIVE_VERSIONS`.
ADMITTED_KINDS_BY_VERSION: dict[str, frozenset[str]] = {
    "3.0": frozenset({"universe", "family"}),
    "3.1": frozenset({"universe", "family", "expression"}),
}

#: The kinds admitted at the version THIS build writes. Kept as a name because it reads as the
#: contract's own statement of what exists; every gate asks `admitted_kinds(version)` instead.
ADMITTED_KINDS: frozenset[str] = ADMITTED_KINDS_BY_VERSION[NATIVE_PUBLICATION_FORMAT_VERSION]


def admitted_kinds(version: str) -> frozenset[str]:
    """The declaration kinds admitted at `version`. Only ever called with a version `read_version`
    has already accepted, so an unknown minor here is a structural defect, not an artifact one."""
    kinds = ADMITTED_KINDS_BY_VERSION.get(version)
    if kinds is None:                                       # pragma: no cover - structural guard
        _refuse(f"no admitted-kind set is recorded for native version {version!r}.")
    return kinds


def minor_admitting(kind: str) -> Optional[str]:
    """The EARLIEST supported minor that admits `kind`, or `None` if no minor does.

    Exists so a refusal can say *"`expression` is admitted at v3.1; this artifact declares v3.0"*
    rather than *"unknown kind"*. The difference matters to a steward: the first is a version to
    re-declare under, the second is a sort that does not exist."""
    for version in SUPPORTED_NATIVE_VERSIONS:
        if kind in ADMITTED_KINDS_BY_VERSION.get(version, frozenset()):
            return version
    return None

TOP_LEVEL_KEYS: frozenset[str] = frozenset(
    {"publication_format_version", "ref", "published", "declarations"})
UNIVERSE_KEYS: frozenset[str] = frozenset({
    "kind", "name", "constitution", "constitution_conformance",
    "existence_law_ratification", "case_s_denotations"})
FAMILY_KEYS: frozenset[str] = frozenset({
    "kind", "name", "body", "family_constitution_authority", "universe_authority_binding"})

#: Body keys a native family declaration may carry. TOTAL — an unrecognised key is a refusal.
FAMILY_BODY_KEYS: frozenset[str] = frozenset({
    "family_id", "canonical_reference", "aliases", "universe", "constitutive_anchor", "target",
    "formation", "participation", "value_domain", "continuation", "domain", "movement",
    "prohibited_constituents", "exceptional"})

#: Body keys OUTSIDE the identity-bearing payload: identity cannot be part of its own determinant;
#: a canonical reference and its aliases are labels; `domain`/`movement` are capability, not
#: identity. Everything else is IN **by derivation** — a body key added later is inside the
#: fingerprint by default, and taking one out is a decision someone has to write down.
#:
#: **`prohibited_constituents` is written down here, and this line IS the decision** (R12, Huayin
#: 2026-09-22): *"P_F, and the resulting family-domain standing, is not identity-bearing. A
#: governed revision of P_F does not by itself mint a successor family or change family_id. Make
#: this exclusion explicit wherever the native identity-key default would otherwise pull the new
#: declaration into the family fingerprint."* The default runs the other way, so omitting this line
#: would silently make every domain revision a family succession.
#:
#: Not identity-bearing is NOT unversioned: a domain revision remains governed and auditable
#: through publication history (`ref.version`, `published.at`/`by`), and is not runtime state.
NON_IDENTITY_KEYS: frozenset[str] = frozenset(
    {"family_id", "canonical_reference", "aliases", "domain", "movement",
     "prohibited_constituents"})
IDENTITY_KEYS: frozenset[str] = FAMILY_BODY_KEYS - NON_IDENTITY_KEYS

#: The two NOMINAL references that leave the payload at `fcf-2`. They stay in the declaration and
#: stay in the artifact — the persisted object does not change shape for a fingerprint's
#: convenience. What they lose is the pretence that a spelling was identity: `universe` is governed
#: through the U-authority binding, and `constitutive_anchor` is RESOLVED, with the resolved
#: structure entering the payload as `_anchor`.
NOMINAL_KEYS: frozenset[str] = frozenset({"universe", "constitutive_anchor"})
FCF2_IDENTITY_KEYS: frozenset[str] = IDENTITY_KEYS - NOMINAL_KEYS

# ── the GOVERNED EXPRESSION — a SIBLING of the family, admitted at native v3.1 ────────────────────
#
# ToD v8.0 §3.5 recognizes TWO durable analytical sorts, and §8.5 gives Manifold *"two distinct
# reusable analytical classes"*. This contract has only ever carried one. The second is the GOVERNED
# EXPRESSION: a durable object whose value is determined by a SUFFICIENT BASIS over other governed
# families rather than carried by its own continuation. `mean(revenue@sale_at)` is the worked case,
# and v8 §4.3 establishes it over a matching SUM and COUNT.
#
# **IT IS A SIBLING, NOT A VARIANT OF `Family`, AND THE KEY SETS BELOW ARE WHERE THAT IS ENFORCED.**
# Ruled (Huayin, 2026-09-28): *"Build `Expression` as a true sibling of `Family`. Do not implement it
# as `Family(continuation=None)` or route it through `resolve_family`."* Five family body keys are
# therefore ABSENT here, each because carrying it would assert a family fact:
#
#   `constitutive_anchor`      §3.2's `R_F` is the ORIGIN OF CONTINUATION, and an expression has no
#                              continuation to originate. An expression is EVALUATED at an anchor,
#                              which is a property of a REQUEST, not of a declaration. It does have
#                              CONSTITUTIVE INNER anchors (§3.6) — `mean(Revenue@Order)@Region` is
#                              constituted over `Order` and evaluated at `Region` — and that is a
#                              DIFFERENT FACT, spelled `inner_anchors` so that no consumer can reach
#                              an expression through the slot it reads a family's root from.
#   `continuation`             (C8) the whole point of the sort is that there is none.
#   `movement`                 (C3 edge validity) movement is family continuation under licence.
#   `prohibited_constituents`  (`P_F`) a family-domain law.
#   `exceptional`              (C9) an expression's empty behaviour comes from its CONSTRUCTOR OVER
#                              ITS BASIS, which v8 §4.3 states precisely for the case at hand: the
#                              SUM/COUNT basis is established as `(0, 0)` and *"the expression is
#                              undefined on that basis"* at `n = 0`. That is a different fact from a
#                              LAW having no fold to take, which is what `no_composition` names.
#
# And three keys are genuinely new: `operands` carries ROLES, because v8 §5.3's basis is role-indexed
# `(G₁…G_m)` and a position is not a role; `inner_anchors`; and `admitted_bases`.
EXPRESSION_KEYS: frozenset[str] = frozenset({
    "kind", "name", "body", "expression_constitution_authority", "universe_authority_binding"})

#: Body keys a native expression declaration may carry. TOTAL — an unrecognised key is a refusal,
#: exactly as for a family. Required: `expression_id`, `canonical_reference`, `universe`,
#: `constructor`, `operands`, `participation`. The rest are optional and NORMALIZE (see `ecf-1`).
EXPRESSION_BODY_KEYS: frozenset[str] = frozenset({
    "expression_id", "canonical_reference", "aliases", "universe", "constructor", "operands",
    "inner_anchors", "participation", "scope", "parameters", "admitted_bases"})

#: Keys OUTSIDE `Σ(E)`. Identity cannot be part of its own determinant; a canonical reference and its
#: aliases are labels.
#:
#: **`admitted_bases` IS IN THIS SET, AND THAT IS A RULING, NOT A CONVENIENCE** (Huayin, 2026-09-28):
#: *"A sufficient basis is an establishment route. v8 allows more than one sufficient basis for the
#: same expression, and alternative lawful bases must agree. Therefore do not fingerprint 'the
#: selected basis' into Σ(E) merely because the first implementation has one basis… The distinction I
#: want preserved is: expression identity ≠ one particular sufficient basis used to establish it."*
#:
#: Two consequences, both of which the default would have got wrong. Admitting a SECOND lawful route
#: to the same expression would otherwise mint a successor — an expression would change identity
#: because someone learned a new way to compute it. And two artifacts admitting different subsets of
#: the same lawful routes would otherwise be two expressions, so a reader could not tell a genuine
#: succession from a difference of coverage. `admitted_bases` is governed, versioned and auditable
#: through publication history exactly as `prohibited_constituents` is on a family; what it is not is
#: constitutive.
EXPRESSION_NON_IDENTITY_KEYS: frozenset[str] = frozenset(
    {"expression_id", "canonical_reference", "aliases", "admitted_bases"})
EXPRESSION_IDENTITY_KEYS: frozenset[str] = EXPRESSION_BODY_KEYS - EXPRESSION_NON_IDENTITY_KEYS

#: The NOMINAL references that leave the `ecf-1` payload, for the reasons `fcf-2` established: the
#: `universe` SPELLING is not the governed world — the U-authority binding is — and an anchor TOKEN
#: is not an anchor. Both stay in the declaration; what they lose is the pretence that a spelling was
#: identity. The resolved inner anchors enter the payload as `_inner_anchors`.
EXPRESSION_NOMINAL_KEYS: frozenset[str] = frozenset({"universe", "inner_anchors"})
ECF1_IDENTITY_KEYS: frozenset[str] = EXPRESSION_IDENTITY_KEYS - EXPRESSION_NOMINAL_KEYS

#: **The expression's canonicalization scheme, and there is exactly one.** `fcf` needed two because
#: it acquired the U-authority binding and resolved anchors AFTER families were already established
#: under a spelling-based digest, and `fcf-1` had to keep meaning what it meant. An expression sort
#: minted today has no such era behind it, so `ecf-1` starts where `fcf-2` ended: the world governed
#: through the binding, the anchors resolved. The number is still in the name, because the scheme is
#: what tells a reader WHICH derivation produced a digest, and that is true of a scheme that is
#: currently alone.
ECF1 = "ecf-1"

EXPRESSION_AUTHORITY_KEYS: frozenset[str] = frozenset(
    {"established_by", "at", "constitution_fingerprint", "fingerprint_scheme"})
OPERAND_KEYS: frozenset[str] = frozenset({"role", "family_id"})
BASIS_KEYS: frozenset[str] = frozenset({"basis_id", "components", "requires_common_participation"})
BASIS_COMPONENT_KEYS: frozenset[str] = frozenset({"role", "family_id"})
CONSTRUCTOR_KEYS: frozenset[str] = frozenset({"vocabulary", "version", "law"})

CONSTITUTION_KEYS: frozenset[str] = frozenset({"identity", "individuation", "law", "premises"})
IDENTITY_SECTION_KEYS: frozenset[str] = frozenset({"designation"})
INDIVIDUATION_KEYS: frozenset[str] = frozenset({"closed", "constituents"})
CONSTITUENT_KEYS: frozenset[str] = frozenset({"reference", "domain"})
VALUE_DOMAIN_KEYS: frozenset[str] = frozenset({"designation", "equality"})
LAW_KEYS: frozenset[str] = frozenset({"ground", "qualification", "determination"})
CONFORMANCE_KEYS: frozenset[str] = frozenset({"asserted_by", "at", "obligations"})
RATIFICATION_KEYS: frozenset[str] = frozenset(
    {"ratified_by", "at", "fingerprint", "fingerprint_version"})
FAMILY_AUTHORITY_KEYS: frozenset[str] = frozenset(
    {"established_by", "at", "constitution_fingerprint", "fingerprint_scheme"})
BINDING_KEYS: frozenset[str] = frozenset(
    {"bound_by", "at", "universe_reference", "universe_authority", "universe_authority_scheme"})

#: Premise kinds. `occurrence_subject` is the ONLY admitted form; the other two are RECOGNISED so
#: they can be refused precisely, with their jurisdiction named. Recognising a form is not
#: admitting it, and the refusal never says "not lawful".
PREMISE_KEY = "premise"
OCCURRENCE_SUBJECT = "occurrence_subject"
GOVERNED_ARTIFACT = "governed_artifact"
DOMAIN_RANGE = "domain_range"
OCCURRENCE_SUBJECT_KEYS: frozenset[str] = frozenset({PREMISE_KEY, "reference", "individuation"})

#: The scheme that attests a CONSTITUTED universe's population law. Never `elf-1`: `elf-1` attests
#: `anchor + basis + restriction`, which on a constituted universe is carriage and not law, so it
#: can never be authority over one.
CONSTITUTION_ATTESTATION_SCHEME = "elf-2"
FCF1, FCF2 = "fcf-1", "fcf-2"

#: Human-judged obligation codes. Every one must be ESTABLISHED by a human, never computed — which
#: is why F4's check is *coverage*, not re-adjudication.
HUMAN_DOMAIN_INDIVIDUATES = "domain_suffices_to_individuate"
HUMAN_QUALIFICATION_WHOLE = "qualification_is_the_whole_qualification"
HUMAN_DETERMINATION_CORRECT = "determination_is_correct"
HUMAN_CLOSURE_OF_STATEMENT = "no_constitutive_content_elsewhere"
HUMAN_SUBJECT_CARRIER_INDEPENDENT = "subject_individuated_independently_of_any_carrier"
HUMAN_QUALIFIES_OCCURRENCES = "qualification_is_over_occurrences_not_rows"

#: Binding verdicts — DERIVED on read, never carried. `UNBOUND` is a legible state, not a defect:
#: ruled 2026-09-21, *"an UNBOUND fcf-1 family may exist in a native-v3 artifact"*, and *"absence
#: of a binding must never be interpreted as BOUND or as equivalent standing"*.
UNBOUND = "UNBOUND"
BOUND = "BOUND"

#: Family-authority currency verdicts, kept apart because their remedies differ. `STALE`'s remedy
#: is a §3.9 SUCCESSION (a new family with a new `family_id`); `SCHEME_MISMATCH`'s is the opposite —
#: the SAME family re-established under the scheme its situation now selects. Collapsing them would
#: prescribe a succession for a change nobody declared.
CURRENT, STALE, SCHEME_MISMATCH = "CURRENT", "STALE", "SCHEME_MISMATCH"


class NativePublicationRefusal(ValueError):
    """These bytes do not satisfy the native-v3 contract. **Consume or refuse; never repair.**

    Deliberately a single type with an artifact-directed message. This reader is not adjudicating
    whether a steward's law is analytically correct, is not repairing anything, and cannot see the
    authoring history that would let it say WHY a denotation is missing — so it says the one true
    thing it knows. No partial acceptance and no report-and-continue path."""


def _refuse(message: str) -> NoReturn:
    raise NativePublicationRefusal(message)


# ── strictness ───────────────────────────────────────────────────────────────────────────────────
def _strict(what: str, d: Mapping[str, Any], allowed: Iterable[str]) -> None:
    """Consume or refuse, at KEY granularity, in the outward direction.

    **Applied at the declaration ENVELOPE, which is where v2 does not apply it.** The v2 reader
    enforces this rule only *inside* a `body` or an authority record, so a native universe — which
    is 100% envelope and 0% body — passes through the one place the rule is not enforced, and its
    entire constitutional content vanishes without a word. That measured gap is a pre-existing v2
    hardening defect and is **not repaired here** (ruling 6); what is done here is to not
    reproduce it."""
    extra = sorted(set(d) - set(allowed))
    if extra:
        _refuse(
            f"{what}: unrecognised key(s) {extra}. A consumer must consume or refuse every "
            f"semantic field; carrying a key nobody reads is meaning nobody carried. This "
            f"contract's keys are {sorted(allowed)}."
        )


def _obj(what: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        _refuse(f"{what} must be an object.")
    return {str(k): v for k, v in value.items()}


def _req(what: str, d: Mapping[str, Any], key: str) -> str:
    value = d.get(key)
    if not isinstance(value, str) or not value:
        _refuse(f"{what}: {key!r} must be a non-empty string.")
    return value


def _digest(payload: dict[str, Any]) -> str:
    """The canonical encoding, shared by both schemes: sorted object keys (ordering is ours),
    preserved list order, compact separators, UTF-8."""
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ── N1 · the constitution, as governed facts ─────────────────────────────────────────────────────
@dataclass(frozen=True)
class ValueDomain:
    designation: str
    equality: str


@dataclass(frozen=True)
class Constituent:
    """A2 — a governed constituent reference and the value domain that individuates it."""

    reference: str
    domain: ValueDomain


@dataclass(frozen=True)
class OccurrencePremise:
    """The one ADMITTED premise form: a governed occurrence subject, a primitive of this
    universe's own constitution. `individuation` is the statement of how the subject is
    individuated **independently of any carrier** — the obligation that keeps the lost-record case
    statable: a sale whose record is lost is still a sale."""

    reference: str
    individuation: str

    def payload(self) -> dict[str, Any]:
        """This premise's A3 contribution, re-derived from its governed fields."""
        return {PREMISE_KEY: OCCURRENCE_SUBJECT, "reference": self.reference,
                "individuation": self.individuation}


@dataclass(frozen=True)
class Constitution:
    """N1's first half — F1, the closed individuation, and λ_U, as governed facts.

    Read, never inferred. Nothing physical is reachable from here: a constitution structurally
    excludes carriers, so there is no column, table, grain or mapping this object could consult."""

    designation: str
    closed: bool
    constituents: tuple[Constituent, ...]
    ground: str
    qualification: str
    determination: tuple[tuple[str, str], ...]
    premises: tuple[OccurrencePremise, ...]

    @property
    def references(self) -> frozenset[str]:
        """F2 — the closed set of constituent references. The whole coordinate space of this
        universe, and there is nowhere else to look for one."""
        return frozenset(c.reference for c in self.constituents)

    def resolve_coordinate(self, reference: str) -> Optional[Constituent]:
        """Resolve a coordinate reference **within this universe and within nothing else.** That
        is what makes two universes' identical spellings independent."""
        for c in self.constituents:
            if c.reference == reference:
                return c
        return None

    def premise(self, reference: str) -> Optional[OccurrencePremise]:
        for p in self.premises:
            if p.reference == reference:
                return p
        return None

    # ── elf-2 ────────────────────────────────────────────────────────────────────────────────
    def canonical_payload(self) -> dict[str, Any]:
        """Σ_U = H(scheme, closed individuation, constituent semantics, λ_U, premises) — and
        explicitly **not** H(designation, …).

        **F1 is OUT of the digest.** The world is the SUBJECT of the attestation; its designation
        is how we refer to that subject, not one of the premises that determines its population.
        So a re-wording of the designation must not stale the attestation.

        Constituents and premises are SORTED, and λ3 with them: order is not identity-bearing, so
        a reordering must not stale either."""
        return {
            "_scheme": CONSTITUTION_ATTESTATION_SCHEME,
            "individuation": {
                "closed": True,
                "constituents": [
                    {"reference": c.reference,
                     "domain": {"designation": c.domain.designation,
                                "equality": c.domain.equality}}
                    for c in sorted(self.constituents, key=lambda c: c.reference)
                ],
            },
            "law": {
                "ground": self.ground,
                "qualification": self.qualification,
                "determination": {ref: statement
                                  for ref, statement in sorted(self.determination)},
            },
            "premises": [p.payload() for p in sorted(self.premises, key=lambda p: p.reference)],
        }

    def fingerprint(self) -> str:
        """The scheme-qualified digest, `"elf-2:<digest>"`. The qualification is not decoration:
        with two schemes coexisting over two universe states, the scheme is what tells a reader
        WHICH derivation produced the digest."""
        return f"{CONSTITUTION_ATTESTATION_SCHEME}:{_digest(self.canonical_payload())}"


# ── N2 · the derived geometry ────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Anchor:
    """N3 — **a universe-relative constituent set**, reached only through `U`.

    Not a name, not a declaration, not an entry in a publication-global map. Two consequences the
    old shape could not have:

    * **synonyms collapse.** `berthing_at` and `berth_day` both denote `{berth, day}`, so they
      are ONE anchor. Under a raw-string anchor they were two, and `AnalyticalIdentity` — the
      retained-state retrieval key, the fold-eligibility key, the eviction key — split one
      analytical thing in two. (C3's subject; the representation is established here.)
    * **universe scoping stops being a rule someone must apply** and becomes the only shape
      available: an `Anchor` carries the universe it is relative to, so there is no place from
      which two universes' anchors are both visible, and no publication-global index can be built.
    """

    universe: str
    constituents: frozenset[str]

    def __str__(self) -> str:
        return f"{self.universe}{{{', '.join(sorted(self.constituents))}}}"

    @property
    def is_scalar(self) -> bool:
        """`{}` — the scalar anchor, the coarsest location in any universe."""
        return not self.constituents

    def refines(self, other: "Anchor") -> bool:
        """**Refinement is set containment (⊇), computed — never name matching, never a declared
        hierarchy and never a physical join.** A physical join does not supply a missing partition
        projection (ToD §2.1.2), and nothing physical is reachable from here anyway."""
        self._same_world(other)
        return self.constituents >= other.constituents

    def projection_forgets(self, target: "Anchor") -> frozenset[str]:
        """**Projection is set difference.** What moving from here to `target` forgets.

        Whether the target LOCATION exists is this question, and it is the whole of the geometric
        half of P1-33's missing distinction: *geometry determines whether a target analytical
        location exists; governed movement standing determines whether `F` may stand there.* This
        module answers the first and deliberately does not answer the second — movement is derived
        afresh, later, from the native model (ruling 3)."""
        self._same_world(target)
        if not self.constituents >= target.constituents:
            _refuse(
                f"{target} is not a projection of {self}: projection forgets constituents, and "
                f"{sorted(target.constituents - self.constituents)} is not held here. A coarser "
                f"location is reached by forgetting, never by acquiring."
            )
        return self.constituents - target.constituents

    def union(self, other: "Anchor") -> "Anchor":
        """The compound anchor. Union, inside one universe, and nothing else participates."""
        self._same_world(other)
        return Anchor(self.universe, self.constituents | other.constituents)

    def _same_world(self, other: "Anchor") -> None:
        if self.universe != other.universe:
            _refuse(
                f"{self} and {other} are anchors of two different universes. An anchor is a "
                f"universe-relative constituent set; comparing two across worlds would require "
                f"universe identity and cross-universe correspondence, both of which are held."
            )


# ── the governance records ───────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class ConformanceJudgment:
    """F4 — a named human asserted, at a time, that these human-judged obligations hold."""

    asserted_by: str
    at: str
    obligations: frozenset[str]


@dataclass(frozen=True)
class Attestation:
    """F5 — a named human attested a law represented by a fingerprint, under a stated scheme."""

    ratified_by: str
    at: str
    fingerprint: str
    scheme: str


@dataclass(frozen=True)
class FamilyAuthority:
    """The family's own constitution authority, scheme-qualified."""

    established_by: str
    at: str
    fingerprint: str
    scheme: str


@dataclass(frozen=True)
class UniverseAuthorityBinding:
    """The family's citation of `U`'s own attestation — the record that makes *which world this
    family is constituted in* a governed fact rather than a spelling."""

    bound_by: str
    at: str
    universe_reference: str
    universe_authority: str
    universe_authority_scheme: str


# ── N1 · the resolved universe ───────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Universe:
    """`U = (constitution, denotations)` — plus the two standings carried beside it.

    **The geometry below is COMPUTED on every access and never stored.** That is N2, and it is the
    whole shift: today's consumer *looks up* an anchor in a publication-global map of `anchor`
    declarations; natively it *computes* one from a constitution, inside one universe."""

    name: str
    constitution: Constitution
    denotations: tuple[tuple[str, tuple[str, ...]], ...]
    conformance: ConformanceJudgment
    attestation: Attestation

    # ── geometry, derived ────────────────────────────────────────────────────────────────────
    @property
    def coordinates(self) -> tuple[str, ...]:
        return tuple(sorted(self.constitution.references))

    @property
    def root_anchor(self) -> Anchor:
        """`R_U` — **a theorem of the asserted closure**, not a declared object. The individuation
        says *these constituents and no others*, so the finest location is exactly all of them.
        There is no `basis` here and no synthesized compatibility anchor: ruling 7 forbids
        promoting the compatibility vocabulary, and nothing native needs it."""
        return Anchor(self.name, frozenset(self.constitution.references))

    @property
    def scalar_anchor(self) -> Anchor:
        """`{}` — the coarsest location. Every universe has one and none declares it."""
        return Anchor(self.name, frozenset())

    def constituent_anchor(self, reference: str) -> Anchor:
        return self.anchor([reference])

    @property
    def constituent_anchors(self) -> dict[str, Anchor]:
        return {r: self.anchor([r]) for r in self.coordinates}

    def anchor(self, references: Iterable[str]) -> Anchor:
        """Build an anchor of this universe from constituent references — **the shape a REQUEST
        arrives in**.

        `AT {berth * day}` *is* `A = {berth, day}`, resolved here. There is no name to look up, so
        there is nothing to be ambiguous about — which dissolves the v2 consumer's refusal
        *"components are declared by {two anchors}; this profile will not choose between two
        governed anchors"*. In the native fixture that refusal is the ORDINARY case, because
        `berthing_at` and `berth_day` denote the same set; a consumer that kept name-matching
        would refuse a lawful publication on its first request."""
        refs = tuple(references)
        unknown = sorted({r for r in refs if self.constitution.resolve_coordinate(r) is None})
        if unknown:
            _refuse(
                f"universe {self.name!r}: {unknown} do not resolve as constituents of its closed "
                f"individuation {list(self.coordinates)}. Resolution is universe-scoped — a "
                f"reference that resolves elsewhere does not resolve here — and nothing stands in "
                f"for a constituent: not an anchor declaration, not a level, not a physical "
                f"column, not a mapping."
            )
        return Anchor(self.name, frozenset(refs))

    # ── naming ───────────────────────────────────────────────────────────────────────────────
    @property
    def denotation_table(self) -> dict[str, tuple[str, ...]]:
        return dict(self.denotations)

    def denote(self, token: str) -> Optional[Anchor]:
        """The governed Case-S denotation of a token **in this universe**, or None.

        None is a fact about this world, not about the token: the same token may lawfully denote
        elsewhere. Many tokens may denote one anchor — names are conventions, the anchor is a
        theorem — so this is many-to-one by design."""
        refs = self.denotation_table.get(token)
        return None if refs is None else self.anchor(refs)

    def synonyms_of(self, anchor: Anchor) -> tuple[str, ...]:
        """Every token denoting this anchor, sorted. Legibility only: no consumer decision may
        depend on WHICH token was used."""
        return tuple(sorted(t for t, refs in self.denotations
                            if frozenset(refs) == anchor.constituents))


# ── N4 · the family, and contextual resolution ───────────────────────────────────────────────────
@dataclass(frozen=True)
class Family:
    """A governed family, carrying its own standing — no top-level `authority` section hoists it
    out into a map keyed by name (ratifications) and another keyed by `family_id` (family
    constitutions): two identity spaces for one job, which existed only because `{kind, name,
    body}` had no room for standing."""

    name: str
    family_id: str
    canonical_reference: str
    universe_reference: str
    anchor_token: str
    body: Mapping[str, Any]
    authority: FamilyAuthority
    binding: Optional[UniverseAuthorityBinding]

    @property
    def is_bound(self) -> bool:
        return self.binding is not None


@dataclass(frozen=True)
class Resolution:
    """**N4 — `F → U → A`, in that order, always inside `U`.**

    The universe is a **precondition of resolution, not a component of the identity resolution
    produces** (Ruling 1). `F` fixes `U`; `A` is resolved within it. Nothing else participates —
    no anchor declaration, no global anchor namespace, no component matching, no
    `universe.body.anchor`, no physical grain, no mapping, no uniqueness evidence, and no
    cross-universe search."""

    family: Family
    universe: Universe
    anchor: Anchor


# ── N4b · the governed expression, and its governance record ─────────────────────────────────────
@dataclass(frozen=True)
class ExpressionAuthority:
    """Who established this expression's constitution, when, and under which scheme.

    Four fields identical to `FamilyAuthority`'s, and **a separate type on purpose.** The content is
    sort-agnostic; the SUBJECT is not. A single shared record would be the first place a consumer
    could hold an expression's standing in a variable typed for a family's, and the whole discipline
    of this unit is that the two sorts do not pass for each other anywhere."""

    established_by: str
    at: str
    fingerprint: str
    scheme: str


@dataclass(frozen=True)
class Operand:
    """One ROLE-INDEXED governed operand of an expression's constructor.

    **The role is the point.** `Family.formation.operands` is a bare tuple, so an operand is
    identified by its POSITION — and v8 §5.3's basis is role-indexed `(G₁…G_m)`. Position survives a
    reordering of a serialization; a role does not, which is exactly why a role can be identity-
    bearing and a position cannot. (`composite.Component.law` already keys by role at runtime, with no
    declared counterpart to read it from. This is that counterpart.)"""

    role: str
    family_id: str


@dataclass(frozen=True)
class BasisComponent:
    """One component of one admitted sufficient basis: a component LAW, and the governed family whose
    state supplies it.

    `role` here is the component law's name — `SUM`, `COUNT` — and NOT a constructor operand role.
    Two different role spaces, kept in two types, because collapsing them is how `(Count, SumX, SumX²,
    SumXY)` (v8 §5.4) would come to be read as four operands of a one-operand constructor."""

    role: str
    family_id: str


@dataclass(frozen=True)
class AdmittedBasis:
    """**ONE admitted sufficient basis — and an expression may admit zero, one, or several.**

    Ruled (Huayin, 2026-09-28): *"Please make the record structurally capable of zero/one/multiple
    admitted bases, even if the first executable proof uses one."* So this is a member of a TUPLE on
    the record, never a singular `declared_basis` field, and the resolver's agreement responsibility
    exists because the tuple can have more than one member (v8: *alternative lawful bases must
    agree*).

    **ZERO IS A LEGIBLE STATE, NOT A DEFECT AT READ** — the same posture `unbound_families` takes. An
    expression may be constituted before any establishment route is admitted; what it may not do is
    be RESOLVED as established. That verdict belongs to the resolver, not to the reader.

    `requires_common_participation` is **per basis** and deliberately not read off the constructor's
    law. `foundation.StateBasis` carries it on the LAW, which states a requirement the law makes of
    ANY basis; this states what THIS admitted route was established under. They must agree, and the
    resolver checks that they do — which is a check that cannot exist while there is only one place
    to look."""

    basis_id: str
    components: tuple[BasisComponent, ...]
    requires_common_participation: bool

    @property
    def component_laws(self) -> tuple[str, ...]:
        """The component law names, SORTED. A basis is a set of role-filled components; the order a
        serialization happened to use is not one of its facts."""
        return tuple(sorted(c.role for c in self.components))


@dataclass(frozen=True)
class Expression:
    """**A durable governed expression — `E`, the second of v8's two reusable analytical sorts.**

    Read the key-set commentary above for what is absent and why. What is present is the minimum that
    v8 §3.5, §3.6, §5.3 and §7.3 require: a constructor, role-indexed governed operands, constitutive
    inner anchors, participation and scope, identity-bearing parameters, and the admitted bases.

    **This record answers no family question.** It has no root, no family domain, no continuation, no
    movement and no empty-fiber family law, and there is nowhere on it to put one. That is not an
    omission to be filled in later: each of those is a statement about continuation under refinement,
    and an expression's value does not continue — it is RE-EVALUATED from a basis at each location it
    is asked for. An expression that could answer them would be a family."""

    name: str
    expression_id: str
    canonical_reference: str
    universe_reference: str
    #: The CONSTITUTIVE INNER anchor tokens (§3.6), in declaration order. **Not a root**, and there is
    #: deliberately no `anchor_token` singular: an expression may be constituted over several inner
    #: anchors, and reducing them to one would be inventing a root.
    inner_anchor_tokens: tuple[str, ...]
    operands: tuple[Operand, ...]
    admitted_bases: tuple[AdmittedBasis, ...]
    body: Mapping[str, Any]
    authority: ExpressionAuthority
    #: **REQUIRED, not optional** — the one place this record is stricter than `Family`'s, and the
    #: reason is `ecf-1`. The scheme takes the `universe` SPELLING out of the identity payload on the
    #: ground that the world is governed through the binding. An UNBOUND expression would therefore
    #: carry a world that is in no payload and under no authority: a hole, not a transition. Families
    #: may be unbound because `fcf-1` predates the binding and hashed the spelling instead; an
    #: expression has no such history to be compatible with.
    binding: "UniverseAuthorityBinding"

    @property
    def aliases(self) -> tuple[str, ...]:
        return tuple(a for a in (self.body.get("aliases") or []) if isinstance(a, str) and a)

    @property
    def roles(self) -> tuple[str, ...]:
        return tuple(o.role for o in self.operands)

    def operand(self, role: str) -> Optional[Operand]:
        for o in self.operands:
            if o.role == role:
                return o
        return None

    def basis(self, basis_id: str) -> Optional[AdmittedBasis]:
        for b in self.admitted_bases:
            if b.basis_id == basis_id:
                return b
        return None

    @property
    def operand_family_ids(self) -> tuple[str, ...]:
        """Every governed family this expression's IDENTITY runs through — its operands, and nothing
        else. **The bases are not here.** v8 §7.1 keeps family / expression / carrier lineage apart,
        and an expression's ancestry runs through its OPERANDS; a basis is a route to a value, and a
        route is not a parent."""
        return tuple(sorted({o.family_id for o in self.operands}))


# ── N5 · governed currency ───────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class CurrencyClaim:
    """One checkable governed claim, its subject, and how it was settled — **from the bytes**."""

    claim: str
    subject: str
    verdict: str
    detail: str


@dataclass(frozen=True)
class CurrencyReport:
    """The four claims of N5, made legible rather than merely enforced.

    The reader REFUSES an artifact whose currency does not hold, so a report in hand is always a
    report of claims that verified. It exists because *what was checked* is a governed fact a
    consumer should be able to show, not an invisible precondition."""

    claims: tuple[CurrencyClaim, ...]

    def __iter__(self):
        return iter(self.claims)

    def __len__(self) -> int:
        return len(self.claims)

    def of(self, claim: str) -> tuple[CurrencyClaim, ...]:
        return tuple(c for c in self.claims if c.claim == claim)

    def render(self) -> str:
        width = max((len(c.claim) for c in self.claims), default=0)
        return "\n".join(f"{c.claim:<{width}}  {c.subject:<14} {c.verdict:<14} {c.detail}"
                         for c in self.claims)


# ── conformance, re-derived ──────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Obligation:
    code: str
    fact: str
    message: str


def machine_failures(c: Constitution) -> tuple[Obligation, ...]:
    """The machine-checkable conformance obligations this constitution does NOT satisfy.

    **Not a re-adjudication of whether the law is analytically correct.** `law_absent`,
    `qualification_absent`, `determination_gap` and `ground_unresolved` describe a record that is
    not a constitution at all; the producer refuses every one of them before it will take a
    digest, so bytes that fail here were not produced by a conforming producer. Refusing them is
    consume-or-refuse, not an opinion about anyone's world."""
    out: list[Obligation] = []
    if not c.designation.strip():
        out.append(Obligation("f1_absent", "F1",
                              "the identity of the analytical world is not stated."))
    if not c.constituents:
        out.append(Obligation("f2_absent", "F2",
                              "the closed primitive individuation is empty."))
    seen: set[str] = set()
    for con in c.constituents:
        if not con.reference.strip():
            out.append(Obligation("constituent_reference_absent", "F2",
                                  "a constituent has no governed reference."))
            continue
        if con.reference in seen:
            out.append(Obligation("constituent_duplicated", "F2",
                                  f"constituent {con.reference!r} is stated twice; an "
                                  f"individuation is a set."))
        seen.add(con.reference)
        if not con.domain.designation.strip() or not con.domain.equality.strip():
            out.append(Obligation("constituent_domain_absent", "F2",
                                  f"constituent {con.reference!r} has no governed value domain "
                                  f"with an equality convention."))
    if not c.ground.strip():
        out.append(Obligation("law_absent", "λ1", "λ_U states no ground."))
    elif c.premise(c.ground) is None:
        out.append(Obligation("ground_unresolved", "λ1",
                              f"λ1 {c.ground!r} does not resolve to a governed premise of this "
                              f"universe."))
    if not c.qualification.strip():
        out.append(Obligation("qualification_absent", "λ2", "λ2 is not stated."))
    determined = {ref for ref, _ in c.determination}
    for missing in sorted(c.references - determined):
        out.append(Obligation("determination_gap", "λ3",
                              f"λ3 determines no value for constituent {missing!r}."))
    for extra in sorted(determined):
        if c.resolve_coordinate(extra) is None:
            out.append(Obligation("determination_surplus", "λ3",
                                  f"λ3 determines {extra!r}, which does not resolve as a "
                                  f"constituent of this universe's closed individuation."))
    ground = c.premise(c.ground) if c.ground else None
    if ground is not None and not ground.individuation.strip():
        out.append(Obligation("occurrence_subject_individuation_absent", "λ1",
                              f"the occurrence subject {ground.reference!r} does not state how "
                              f"it is individuated."))
    return tuple(out)


def human_obligations(c: Constitution) -> tuple[str, ...]:
    """The human-judged obligation CODES this constitution raises, sorted and distinct.

    Selected by WHAT λ1 RESOLVED TO — never by a field on λ_U, because there is none. **Derived on
    every read and never persisted**, so a judgment taken over an earlier constitution cannot
    silently cover an obligation that did not exist yet."""
    codes: set[str] = set()
    for con in c.constituents:
        if con.domain.designation.strip() and con.domain.equality.strip():
            codes.add(HUMAN_DOMAIN_INDIVIDUATES)
    if c.qualification.strip():
        codes.add(HUMAN_QUALIFICATION_WHOLE)
    if c.determination:
        codes.add(HUMAN_DETERMINATION_CORRECT)
    codes.add(HUMAN_CLOSURE_OF_STATEMENT)
    ground = c.premise(c.ground) if c.ground else None
    if ground is not None:                       # the occurrence form — the only admitted one
        if ground.individuation.strip():
            codes.add(HUMAN_SUBJECT_CARRIER_INDEPENDENT)
        codes.add(HUMAN_QUALIFIES_OCCURRENCES)
    return tuple(sorted(codes))


def outstanding_obligations(c: Constitution, judgment: ConformanceJudgment) -> tuple[str, ...]:
    """F4's question, and the whole of it: which obligations this constitution raises does the
    carried judgment not cover? **Coverage, never re-adjudication** — every one of these codes
    names something only a human can establish."""
    return tuple(o for o in human_obligations(c) if o not in judgment.obligations)


# ── fcf — the family's own canonicalization ──────────────────────────────────────────────────────
def expected_family_scheme(family: Family, universe: Universe) -> str:
    """Which canonicalization scheme governs THIS family — **state-relative, never a flag day**.

    Ruled (Huayin, 2026-09-22): *"`fcf-2` applies when the family has a current U-authority
    binding and its governed `constitutive_anchor` resolves structurally within that bound
    universe. Otherwise the family remains under `fcf-1`."* Nothing here reads the UNIVERSE's
    attestation scheme: `elf` and `fcf` are separate governed schemes over different objects.

    **Entry is by condition; persistence is by record.** Once a human has established this family
    under `fcf-2`, a later loss of the naming must NOT hand it back to `fcf-1` — that is the
    fallback the same ruling forbids. So an established `fcf-2` record is read first and is
    decisive; such a family whose anchor no longer resolves REFUSES, and does not silently revert.

    **`BOUND` alone is insufficient**, and that is stated rather than inferred: a family may be
    bound to `U` while its anchor token still has no governed denotation. It is not dragged into
    `fcf-2` only to refuse; it stays `fcf-1` until both facts exist."""
    if family.authority.scheme == FCF2:
        return FCF2
    if family.binding is None:
        return FCF1
    if binding_verdict(family, universe) != BOUND:
        return FCF1
    return FCF2 if universe.denote(family.anchor_token) is not None else FCF1


def binding_verdict(family: Family, universe: Universe) -> str:
    """`BOUND` / `UNBOUND` — and every other axis is a REFUSAL at read, not a verdict.

    The producer's declaration-level `binding_status` distinguishes six failure axes because a
    steward can act on the difference. A reader holding an immutable artifact can act on none of
    them, so a binding that cites another world, or an authority the universe beside it does not
    carry, is refused at read with the one true thing this reader knows — and never survives into
    a verdict a later stage might treat as advisory."""
    return UNBOUND if family.binding is None else BOUND


def canonical_family_payload(family: Family, universe: Universe, scheme: str) -> dict[str, Any]:
    """The semantics-only structure that IS this family's identity, under `scheme`.

    `fcf-2` makes exactly two corrections to `fcf-1` and nothing else: the `universe` SPELLING
    leaves the payload (the world is governed through the U-authority binding, which cites `U`'s
    own attestation — hashing the spelling was never "including the governed universe"), and
    `constitutive_anchor` is RESOLVED, with the resolved constituent set entering as `_anchor`.

    `_anchor` is underscore-prefixed for the reason `_scheme` is: the loop below copies body keys
    verbatim, so a derived value wearing a body key's name would be the one thing nobody could
    later tell apart — *declared* from *derived*, inside the digest, where that distinction is the
    whole doctrine."""
    body = family.body
    if scheme == FCF1:
        payload: dict[str, Any] = {"_scheme": FCF1}
        for key in sorted(IDENTITY_KEYS):
            if key in body:
                payload[key] = body[key]
        return payload
    anchor = universe.denote(family.anchor_token)
    if anchor is None:
        _refuse(
            f"family {family.name!r} is governed by `{FCF2}`, and its constitutive anchor "
            f"{family.anchor_token!r} denotes no Case-S anchor of universe "
            f"{universe.name!r} in this publication. There is no payload to digest, and there is "
            f"NO FALLBACK to `{FCF1}`: falling back would attest a spelling in place of the "
            f"structure this family's identity is now stated in."
        )
    payload = {"_scheme": FCF2, "_anchor": sorted(anchor.constituents)}
    for key in sorted(FCF2_IDENTITY_KEYS):
        if key in body:
            payload[key] = body[key]
    return payload


def family_fingerprint(family: Family, universe: Universe, scheme: str) -> str:
    return f"{scheme}:{_digest(canonical_family_payload(family, universe, scheme))}"


# ── ecf — `Σ(E)`, the expression's own canonicalization ──────────────────────────────────────────
#: The canonical empty for each `ecf-1` identity key. **`ecf-1` IS TOTAL OVER ITS IDENTITY KEYS**,
#: which is the one place it does NOT copy `fcf`: `canonical_family_payload` writes a key only `if key
#: in body`, so for a family an ABSENT optional key and a key DECLARED EMPTY produce two different
#: digests — two identities for one analytical fact. That hole is not reproduced. An expression that
#: declares `"scope": ""` and one that omits `scope` are making the same statement, so they digest the
#: same, and a steward cannot change an expression's identity by adding a key that says nothing.
#:
#: The rule is the module's own: silence is not representable. Here it is applied to the digest.
_ECF1_EMPTY: dict[str, Any] = {"participation": "", "scope": "", "parameters": {}, "operands": []}


def canonical_expression_payload(expr: Expression, universe: Universe) -> dict[str, Any]:
    """`Σ(E)` under `ecf-1` — the semantics-only structure that IS this expression's identity.

    From v8 §7.3's own list, and nothing added: **constructor · governed operand identities · operand
    roles · constitutive inner anchors · participation and scope · identity-bearing parameters.**

    **WHAT IS NOT IN IT, AND WHY EACH ABSENCE IS A DECISION.**

    * `admitted_bases` — ruled out (see `EXPRESSION_NON_IDENTITY_KEYS`). A sufficient basis is an
      establishment route; v8 admits several for one expression; identity is not one of them.
    * `expression_id`, `canonical_reference`, `aliases` — identity is not part of its own determinant,
      and a reference is a label.
    * the `universe` SPELLING — governed through the U-authority binding, which cites the world's own
      attestation. This is `fcf-2`'s correction, applied from birth.

    **OPERANDS ARE SORTED BY ROLE, AND THE ROLE IS WHAT CARRIES THE ORDER.** A role-indexed tuple has
    no serialization order to preserve — `[{SUM}, {COUNT}]` and `[{COUNT}, {SUM}]` are one basis — so
    sorting by role is what makes reordering non-identity-bearing WITHOUT losing which family filled
    which role. That is exactly the trade a bare positional tuple cannot make, and it is why the role
    exists on the record.

    **INNER ANCHORS ARE RESOLVED, AS A SORTED SET OF SORTED CONSTITUENT SETS.** `_inner_anchors` is
    underscore-prefixed for the reason `_scheme` and `_anchor` are: the loop below copies body keys
    verbatim, so a DERIVED value wearing a body key's name would be the one thing nobody could later
    tell apart from a DECLARED one, inside the digest, where that distinction is the whole doctrine.
    Resolving them also collapses synonyms — two tokens denoting one constituent set are one anchor —
    which is the same dividend `Anchor` gives `AnalyticalIdentity`."""
    resolved: list[list[str]] = []
    for token in expr.inner_anchor_tokens:
        anchor = universe.denote(token)
        if anchor is None:
            _refuse(
                f"expression {expr.name!r} is governed by `{ECF1}`, and its constitutive inner "
                f"anchor {token!r} denotes no Case-S anchor of universe {universe.name!r} in this "
                f"publication. There is no payload to digest, and there is NO FALLBACK to a "
                f"spelling-based scheme: falling back would attest a token in place of the structure "
                f"this expression's identity is stated in."
            )
        resolved.append(sorted(anchor.constituents))
    payload: dict[str, Any] = {
        "_scheme": ECF1,
        "_inner_anchors": sorted(resolved),
    }
    body = expr.body
    for key in sorted(ECF1_IDENTITY_KEYS):
        if key == "operands":
            payload[key] = [{"role": o.role, "family_id": o.family_id}
                            for o in sorted(expr.operands, key=lambda o: o.role)]
            continue
        payload[key] = body[key] if key in body else _ECF1_EMPTY[key]
    return payload


def expression_fingerprint(expr: Expression, universe: Universe) -> str:
    """The scheme-qualified digest, `"ecf-1:<digest>"`."""
    return f"{ECF1}:{_digest(canonical_expression_payload(expr, universe))}"


# ── the publication ──────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class NativePublication:
    """The native artifact, resolved. Four top-level keys, and **no `logical` wrapper**.

    `logical` named the logical side against a physical `.cml`; a native artifact contains no
    physical content at all — carriers are structurally excluded from a constitution and mappings
    are a separate artifact — so it is a distinction with nothing left to distinguish from.
    `published` is provenance of the publication ACT, not an authority section: which conforming
    publication has authority is settled by the surrounding governance process, outside the bytes.
    """

    manifold_id: str
    version: str
    format_version: str
    published_by: str
    published_at: str
    universes: tuple[Universe, ...]
    families: tuple[Family, ...]
    #: **The second sort, in its own tuple.** Not appended to `families`, and not a subtype of one:
    #: a consumer iterating `families` iterates families, at every native minor, and a consumer that
    #: wants expressions asks for them. That is what keeps "a v3.1-capable reader reads v3.0 family
    #: artifacts unchanged" true by construction rather than by review. Defaulted so that every
    #: existing construction of this record keeps its exact meaning.
    expressions: tuple["Expression", ...] = ()

    def universe(self, name: str) -> Universe:
        for u in self.universes:
            if u.name == name:
                return u
        _refuse(
            f"universe {name!r} is not declared in this publication. A universe reference "
            f"resolves inside its publication and nowhere else."
        )

    def resolve_reference(self, reference: str) -> Optional[Family]:
        """**Reference → family. ONE DIRECTION ONLY**, and the whole of what a REQUEST may use.

        A canonical reference or a declared alias, and nothing else — not a `family_id`, which is
        identity rather than a way of asking, and not a declaration name. Uniqueness is guaranteed
        upstream: two families answering to one reference is a refusal at read, so ambiguity cannot
        reach a caller and re-checking it here would be a second enumeration of a rule the format
        owns.

        Distinct from `family()` below, deliberately. `family()` is a LOOKUP for a caller that
        already holds an identity; this is RESOLUTION of something a human wrote."""
        for f in self.families:
            aliases = [a for a in (f.body.get("aliases") or []) if isinstance(a, str)]
            if reference == f.canonical_reference or reference in aliases:
                return f
        return None

    def family(self, reference: str) -> Family:
        """Resolve a family by name, `family_id`, canonical reference or alias — all four are
        unique within the artifact, enforced at read."""
        for f in self.families:
            aliases = [a for a in (f.body.get("aliases") or []) if isinstance(a, str)]
            if reference in (f.name, f.family_id, f.canonical_reference, *aliases):
                return f
        # **THE SORT IS NAMED, AND THAT IS THE WHOLE POINT OF THIS ARM** (ToD v8 §3.7). A reference
        # that names a governed EXPRESSION has not failed to resolve — it has resolved, to the other
        # sort. Reporting "no family is referenced by X" would send a steward to fix a publication
        # that is correct, and is the same defect V8-0 found at the C7 seam: a capability limit
        # reported as a governed absence. §3.7 forbids closing the gap the other way, by promotion.
        for e in self.expressions:
            if reference in (e.name, e.expression_id, e.canonical_reference, *e.aliases):
                _refuse(
                    f"{reference!r} names a governed EXPRESSION in this publication "
                    f"({e.expression_id}), not a measure family. The two are distinct durable "
                    f"analytical sorts: a family's values CONTINUE under refinement from its own law, "
                    f"and an expression's are RE-EVALUATED from a sufficient basis at each location "
                    f"it is asked for. Ask for it as an expression — `expression()` or "
                    f"`resolve_expression_reference()`. It is not promoted to a family by being "
                    f"named, cached, repeated or durably governed."
                )
        _refuse(f"no family in this publication is referenced by {reference!r}.")

    # ── the second sort's own resolution, kept ONE DIRECTION at a time ────────────────────────
    def resolve_expression_reference(self, reference: str) -> Optional["Expression"]:
        """**Reference → expression.** The sibling of `resolve_reference`, and deliberately a SECOND
        METHOD rather than a widened first one.

        A caller that widened `resolve_reference` to return either sort would have to ask what came
        back what it is, at every call site, forever — and the one that forgot would be the one that
        served an expression as a family. Asking the question before the call instead of after is the
        difference, and `sort_of` below exists so it can be asked once."""
        for e in self.expressions:
            if reference == e.canonical_reference or reference in e.aliases:
                return e
        return None

    def expression(self, reference: str) -> "Expression":
        """Resolve an expression by name, `expression_id`, canonical reference or alias — all four
        unique within the artifact, and unique ACROSS the sorts, enforced at read."""
        for e in self.expressions:
            if reference in (e.name, e.expression_id, e.canonical_reference, *e.aliases):
                return e
        for f in self.families:
            aliases = [a for a in (f.body.get("aliases") or []) if isinstance(a, str)]
            if reference in (f.name, f.family_id, f.canonical_reference, *aliases):
                _refuse(
                    f"{reference!r} names a governed measure FAMILY in this publication "
                    f"({f.family_id}), not an expression. A basis-mediated family declaration does "
                    f"not become an expression because a reader now knows that sort: parsing "
                    f"compatibility is not analytical reclassification, and the remedy is an explicit "
                    f"re-authoring into an expression declaration by someone with authority to make "
                    f"it."
                )
        _refuse(f"no expression in this publication is referenced by {reference!r}.")

    def sort_of(self, reference: str) -> Optional[str]:
        """`"family"`, `"expression"`, or `None` — **the dispatch question, asked once.**

        The seam a peer request target will attach to (V8-2), and it exists now so that the target has
        a lawful object to point at rather than a widened family lookup to bend. **Nothing in this
        build routes on it yet**, and no serving path is touched by this unit.

        `None` is genuinely unresolved and is NOT a third sort: it means the publication carries no
        governed object under that reference, which is the answer a refusal should be built from."""
        for f in self.families:
            aliases = [a for a in (f.body.get("aliases") or []) if isinstance(a, str)]
            if reference == f.canonical_reference or reference in aliases:
                return "family"
        for e in self.expressions:
            if reference == e.canonical_reference or reference in e.aliases:
                return "expression"
        return None

    def resolve(self, reference: str) -> Resolution:
        """**`F → U → A`.** The whole of contextual resolution, and the only way to reach an
        anchor from a family."""
        f = self.family(reference)
        u = self.universe(f.universe_reference)
        a = u.denote(f.anchor_token)
        if a is None:  # pragma: no cover - the family read refuses first
            _refuse(f"family {f.name!r}: {f.anchor_token!r} denotes nothing in {u.name!r}.")
        return Resolution(family=f, universe=u, anchor=a)

    @property
    def unbound_families(self) -> tuple[str, ...]:
        """The `family_id`s carrying **no** U-authority binding — named, so absence is legible.

        Ruled 2026-09-21: an UNBOUND `fcf-1` family may exist in a native-v3 artifact during the
        additive transition, and *"absence of a binding must never be interpreted as BOUND or as
        equivalent standing"*. Surfaced here rather than left to be inferred from a missing key."""
        return tuple(f.family_id for f in self.families if f.binding is None)

    def currency(self) -> CurrencyReport:
        """**N5 — the four governed currency claims, every one checkable from the bytes.**

        Recomputed here rather than trusted, and recomputed again on every call rather than cached:
        currency is a reading of the artifact, not a property stored on it."""
        claims: list[CurrencyClaim] = []
        for u in self.universes:
            recomputed = u.constitution.fingerprint()
            claims.append(CurrencyClaim(
                "elf-2 attestation", u.name,
                CURRENT if recomputed == u.attestation.fingerprint else STALE,
                f"{u.attestation.scheme} recomputes to {recomputed.split(':', 1)[1][:16]}…"))
            outstanding = outstanding_obligations(u.constitution, u.conformance)
            claims.append(CurrencyClaim(
                "F4 coverage", u.name, "COVERED" if not outstanding else "OUTSTANDING",
                f"{len(u.conformance.obligations)} asserted, "
                f"{len(human_obligations(u.constitution))} raised by this constitution"))
        for f in self.families:
            u = self.universe(f.universe_reference)
            verdict = binding_verdict(f, u)
            claims.append(CurrencyClaim(
                "U-authority binding", f.name, verdict,
                f"cites the attestation carried on {u.name!r}" if verdict == BOUND
                else "no binding claimed; not BOUND and not equivalent standing"))
            scheme = expected_family_scheme(f, u)
            recomputed = family_fingerprint(f, u, scheme)
            claims.append(CurrencyClaim(
                f"{scheme} constitution", f.name,
                CURRENT if recomputed == f.authority.fingerprint else STALE,
                f"recomputes to {recomputed.split(':', 1)[1][:16]}…"))
        # THE SECOND SORT REPORTS UNDER ITS OWN SCHEME AND ITS OWN SUBJECT. Not folded into the family
        # rows: a reader showing what it checked must be able to show WHICH SORT it checked it on, and
        # `ecf-1` and `fcf-*` are incomparable digests over different identity-bearing key sets.
        for x in self.expressions:
            u = self.universe(x.universe_reference)
            claims.append(CurrencyClaim(
                "U-authority binding", x.name, BOUND,
                f"cites the attestation carried on {u.name!r}; required for every expression"))
            recomputed = expression_fingerprint(x, u)
            claims.append(CurrencyClaim(
                f"{ECF1} constitution", x.name,
                CURRENT if recomputed == x.authority.fingerprint else STALE,
                f"recomputes to {recomputed.split(':', 1)[1][:16]}…"))
            claims.append(CurrencyClaim(
                "admitted bases", x.name,
                "NONE" if not x.admitted_bases else f"{len(x.admitted_bases)}",
                "zero is legible, not a defect at read: an expression may be constituted before an "
                "establishment route is admitted. Whether it RESOLVES as established is the "
                "resolver's verdict, not this reader's"))
        return CurrencyReport(tuple(claims))


# ── the reader ───────────────────────────────────────────────────────────────────────────────────
def read_version(version: Any) -> str:
    """The version gate — **two mechanisms, two refusals** (N9).

    The MAJOR selects the semantic publication model. The MINOR is part of the reader contract, is
    REQUIRED to be present, and an unrecognised one REFUSES."""
    if not isinstance(version, str) or not version:
        _refuse("`publication_format_version` must be a non-empty string.")
    head = version.split(".", 1)[0]
    try:
        major = int(head)
    except ValueError:
        _refuse(f"unreadable publication_format_version {version!r}: expected 'MAJOR.MINOR'.")
    if major in (1, 2):
        _refuse(
            f"publication_format_version {version!r} is a format v{major} artifact. There is no "
            f"native read of it and no shim: v3 is a fresh native ToD-v7.1 contract, and a v"
            f"{major} artifact states its universe law in a V5-era body this contract has no "
            f"representation for. It remains readable through its own v{major} reader, whose "
            f"contract is unchanged."
        )
    if major != SUPPORTED_NATIVE_MAJOR:
        _refuse(f"publication_format_version {version!r} has major {major}; this reader reads "
                f"major {SUPPORTED_NATIVE_MAJOR}.")
    if "." not in version:
        _refuse(
            f"publication_format_version {version!r} states a bare major. The native contract is "
            f"MAJOR.MINOR and the minor is part of it: {NATIVE_PUBLICATION_FORMAT_VERSION!r}. A "
            f"bare major would mean 'no minor to check', and 'absent means fine' is the "
            f"authority-by-omission this contract exists to close."
        )
    if version not in SUPPORTED_NATIVE_VERSIONS:
        _refuse(
            f"publication_format_version {version!r} is a v3 minor this build does not explicitly "
            f"understand. Known: {list(SUPPORTED_NATIVE_VERSIONS)}. Compatibility among v3 minors "
            f"must be KNOWN, not presumed — a later minor is understood when it is added here by "
            f"a deliberate act, never because it sorts after this one."
        )
    return version


def _read_constitution(what: str, raw: Any) -> Constitution:
    d = _obj(f"{what}: `constitution`", raw)
    _strict(f"{what} constitution", d, CONSTITUTION_KEYS)

    identity = _obj(f"{what}: `constitution.identity`", d.get("identity"))
    _strict(f"{what} constitution.identity", identity, IDENTITY_SECTION_KEYS)
    designation = _req(f"{what} constitution.identity", identity, "designation")

    ind = _obj(f"{what}: `constitution.individuation`", d.get("individuation"))
    _strict(f"{what} constitution.individuation", ind, INDIVIDUATION_KEYS)
    if ind.get("closed") is not True:
        _refuse(
            f"{what}: its individuation is not asserted CLOSED. Closure is itself an attested "
            f"fact — 'these constituents and no others' — and the derived geometry is a theorem "
            f"of it. An open individuation has no root anchor to derive."
        )
    raw_cons = ind.get("constituents")
    if not isinstance(raw_cons, list) or not raw_cons:
        _refuse(f"{what}: `constitution.individuation.constituents` must be a non-empty list.")
    constituents: list[Constituent] = []
    for entry in raw_cons:
        e = _obj(f"{what}: a constituent", entry)
        _strict(f"{what} constituent", e, CONSTITUENT_KEYS)
        reference = _req(f"{what} constituent", e, "reference")
        dom = _obj(f"{what}: constituent {reference!r} `domain`", e.get("domain"))
        _strict(f"{what} constituent {reference!r} domain", dom, VALUE_DOMAIN_KEYS)
        constituents.append(Constituent(
            reference=reference,
            domain=ValueDomain(
                designation=_req(f"{what} constituent {reference!r} domain", dom, "designation"),
                equality=_req(f"{what} constituent {reference!r} domain", dom, "equality"))))

    law = _obj(f"{what}: `constitution.law`", d.get("law"))
    _strict(f"{what} constitution.law", law, LAW_KEYS)
    ground = _req(f"{what} constitution.law", law, "ground")
    qualification = _req(f"{what} constitution.law", law, "qualification")
    raw_det = _obj(f"{what}: `constitution.law.determination`", law.get("determination"))
    determination: list[tuple[str, str]] = []
    for ref in sorted(raw_det):
        statement = raw_det[ref]
        if not isinstance(statement, str) or not statement:
            _refuse(f"{what}: λ3's determination of {ref!r} must be a non-empty statement.")
        determination.append((ref, statement))

    raw_premises = d.get("premises")
    if not isinstance(raw_premises, list) or not raw_premises:
        _refuse(f"{what}: `constitution.premises` must be a non-empty list.")
    premises: list[OccurrencePremise] = []
    for entry in raw_premises:
        p = _obj(f"{what}: a premise", entry)
        kind = p.get(PREMISE_KEY)
        if kind == GOVERNED_ARTIFACT:
            _refuse(
                f"{what}: it carries an EXTENSIONAL premise (a governed artifact given "
                f"membership-determining standing) — a form that is recognised and NOT YET "
                f"ADMITTED. Its attestation contribution is undecided, so `elf-2` will not hash "
                f"it and will not quietly leave it out either. The content is preserved, not "
                f"rejected; this reader cannot settle the jurisdiction."
            )
        if kind == DOMAIN_RANGE:
            _refuse(
                f"{what}: it carries a GENERATIVE premise (a ground ranging over constituent "
                f"value domains) — recognised and NOT YET ADMITTED, for the same reason. The "
                f"content is preserved, not rejected."
            )
        if kind != OCCURRENCE_SUBJECT:
            _refuse(
                f"{what}: premise kind {kind!r} is not a form this contract recognises. A digest "
                f"is never taken over a constitution carrying a premise whose attestation rule "
                f"nobody has decided — fail closed, and do not let the first later form set the "
                f"shape by accident."
            )
        _strict(f"{what} premise", p, OCCURRENCE_SUBJECT_KEYS)
        premises.append(OccurrencePremise(
            reference=_req(f"{what} premise", p, "reference"),
            individuation=_req(f"{what} premise", p, "individuation")))

    return Constitution(
        designation=designation, closed=True, constituents=tuple(constituents), ground=ground,
        qualification=qualification, determination=tuple(determination),
        premises=tuple(premises))


def _read_universe(raw: Mapping[str, Any]) -> Universe:
    name = _req("a universe declaration", raw, "name")
    what = f"universe {name!r}"

    # Legacy universe-law carriage REFUSES; it is never ignored. `body` is already an unrecognised
    # key, but "unrecognised key 'body'" is the wrong thing to say to someone holding a V5-shaped
    # universe, and ignoring it would leave a channel by which legacy content could sit inside a
    # native artifact unread — dual authority by omission. This is also the exact site at which
    # the v2 reader coerces a missing body to `{}` and loses the entire native model.
    if "body" in raw:
        body = raw.get("body")
        carried = sorted(set(body) & {"anchor", "basis", "restriction", "law_description",
                                      "dependencies"}) if isinstance(body, Mapping) else []
        _refuse(
            f"{what} carries a `body`"
            + (f", holding legacy universe-law {carried}" if carried else "")
            + ". A native universe's governed law is its CONSTITUTION; legacy universe-law "
              "carriage has no authoritative dual read in this contract and is disposed of "
              "before publication, never carried and never interpreted."
        )
    _strict(what, raw, UNIVERSE_KEYS)
    c = _read_constitution(what, raw.get("constitution"))

    failures = machine_failures(c)
    if failures:
        _refuse(
            f"{what}: the carried constitutional surface does not satisfy the machine-checkable "
            f"conformance this contract requires — "
            + "; ".join(f"[{o.fact}] {o.message}" for o in failures)
            + " This reader does not repair an artifact and does not adjudicate whether the law "
              "is analytically correct."
        )

    # F4 — conformance standing, and its coverage RE-DERIVED from the carried constitution.
    jraw = _obj(f"{what}: `constitution_conformance`", raw.get("constitution_conformance"))
    _strict(f"{what} constitution_conformance", jraw, CONFORMANCE_KEYS)
    codes = jraw.get("obligations")
    if not isinstance(codes, list) or not all(isinstance(x, str) and x for x in codes):
        _refuse(f"{what}: its conformance judgment must list the obligation codes it covers.")
    judgment = ConformanceJudgment(
        asserted_by=_req(f"{what} constitution_conformance", jraw, "asserted_by"),
        at=_req(f"{what} constitution_conformance", jraw, "at"),
        obligations=frozenset(codes))
    outstanding = outstanding_obligations(c, judgment)
    if outstanding:
        _refuse(
            f"{what}: its conformance judgment does not cover {len(outstanding)} human-judged "
            f"obligation(s) this constitution raises: {list(outstanding)}. Conformance and "
            f"authority are two standings and neither waives the other."
        )

    # F5 — authority over the constitutional population law, checked for CURRENCY from the bytes.
    rraw = _obj(f"{what}: `existence_law_ratification`", raw.get("existence_law_ratification"))
    _strict(f"{what} existence_law_ratification", rraw, RATIFICATION_KEYS)
    attestation = Attestation(
        ratified_by=_req(f"{what} existence_law_ratification", rraw, "ratified_by"),
        at=_req(f"{what} existence_law_ratification", rraw, "at"),
        fingerprint=_req(f"{what} existence_law_ratification", rraw, "fingerprint"),
        scheme=_req(f"{what} existence_law_ratification", rraw, "fingerprint_version"))
    if attestation.scheme != CONSTITUTION_ATTESTATION_SCHEME:
        _refuse(
            f"{what}: its attestation declares scheme {attestation.scheme!r}, and a constituted "
            f"universe's population law is attested under "
            f"{CONSTITUTION_ATTESTATION_SCHEME!r}. `elf-1` attests a legacy law — "
            f"`anchor + basis + restriction` — and is never authority over a constitution."
        )
    recomputed = c.fingerprint()
    if attestation.fingerprint != recomputed:
        _refuse(
            f"{what}: its attestation cites {attestation.fingerprint!r}, and the constitution "
            f"carried beside it derives {recomputed!r}. The attestation does not cover this law."
        )

    # `case_s_denotations` — the governed naming EFFECT. Not a governance record: no author, no
    # time, no fingerprint, no scheme, and nothing here enters `elf-2`.
    draw = _obj(f"{what}: `case_s_denotations`", raw.get("case_s_denotations"))
    denotations: list[tuple[str, tuple[str, ...]]] = []
    for token in sorted(draw):
        refs = draw[token]
        if (not token or not isinstance(refs, list) or not refs
                or not all(isinstance(r, str) and r for r in refs)):
            _refuse(
                f"{what}: denotation {token!r} must name a non-empty list of constituent "
                f"references. A token that denotes nothing is not a weaker denotation; it is "
                f"not one."
            )
        unknown = sorted({r for r in refs if c.resolve_coordinate(r) is None})
        if unknown:
            _refuse(
                f"{what}: denotation {token!r} names {unknown}, which do not resolve against this "
                f"universe's constituents {sorted(c.references)}. A dangling denotation is an "
                f"artifact defect; this reader cannot repair authoring history."
            )
        denotations.append((token, tuple(refs)))

    return Universe(name=name, constitution=c, denotations=tuple(denotations),
                    conformance=judgment, attestation=attestation)


def _read_family(raw: Mapping[str, Any], universes: Mapping[str, Universe]) -> Family:
    name = _req("a family declaration", raw, "name")
    what = f"family {name!r}"
    _strict(what, raw, FAMILY_KEYS)
    body = _obj(f"{what}: `body`", raw.get("body"))
    _strict(f"{what} body", body, FAMILY_BODY_KEYS)

    family_id = _req(what, body, "family_id")
    canonical_reference = _req(what, body, "canonical_reference")
    _req(what, body, "target")
    universe_reference = _req(what, body, "universe")
    token = _req(what, body, "constitutive_anchor")

    araw = _obj(f"{what}: `family_constitution_authority`",
                raw.get("family_constitution_authority"))
    _strict(f"{what} family_constitution_authority", araw, FAMILY_AUTHORITY_KEYS)
    authority = FamilyAuthority(
        established_by=_req(f"{what} family_constitution_authority", araw, "established_by"),
        at=_req(f"{what} family_constitution_authority", araw, "at"),
        fingerprint=_req(f"{what} family_constitution_authority", araw,
                         "constitution_fingerprint"),
        scheme=_req(f"{what} family_constitution_authority", araw, "fingerprint_scheme"))
    if authority.scheme not in (FCF1, FCF2):
        _refuse(f"{what}: its constitution authority declares scheme {authority.scheme!r}; this "
                f"contract knows {[FCF1, FCF2]}.")

    if universe_reference not in universes:
        _refuse(
            f"{what} names universe {universe_reference!r}, which is not declared in this "
            f"publication. A family's universe reference resolves inside its publication and "
            f"nowhere else."
        )
    u = universes[universe_reference]

    binding: Optional[UniverseAuthorityBinding] = None
    braw = raw.get("universe_authority_binding")
    if braw is not None:
        b = _obj(f"{what}: `universe_authority_binding`", braw)
        _strict(f"{what} universe_authority_binding", b, BINDING_KEYS)
        binding = UniverseAuthorityBinding(
            bound_by=_req(f"{what} universe_authority_binding", b, "bound_by"),
            at=_req(f"{what} universe_authority_binding", b, "at"),
            universe_reference=_req(f"{what} universe_authority_binding", b,
                                    "universe_reference"),
            universe_authority=_req(f"{what} universe_authority_binding", b, "universe_authority"),
            universe_authority_scheme=_req(f"{what} universe_authority_binding", b,
                                           "universe_authority_scheme"))
        if binding.universe_reference != universe_reference:
            _refuse(
                f"{what}: its U-authority binding cites universe "
                f"{binding.universe_reference!r} while the family states "
                f"{universe_reference!r}."
            )
        cited = (binding.universe_authority, binding.universe_authority_scheme)
        carried = (u.attestation.fingerprint, u.attestation.scheme)
        if cited != carried:
            _refuse(
                f"{what}: its U-authority binding cites {cited[1]}:{cited[0]!r} for universe "
                f"{universe_reference!r}, and the universe carried in this publication is "
                f"attested {carried[1]}:{carried[0]!r}. The binding does not cover the world "
                f"published beside it."
            )

    # P-1 at the reader: ONE artifact-directed refusal. The producer distinguishes unestablished
    # from retracted from moved-under-the-name because a steward can act on the difference; a
    # reader holding an immutable artifact can act on none of it.
    if u.denote(token) is None:
        _refuse(
            f"{what}: its constitutive anchor {token!r} denotes no Case-S anchor of universe "
            f"{universe_reference!r} in this publication. Nothing stands in for a denotation — "
            f"not a legacy anchor declaration, not `universe.body.anchor`, not a physical grain, "
            f"not a mapping, and not uniqueness evidence. Resolution is universe-scoped: a token "
            f"that denotes elsewhere does not denote here."
        )

    # ── `P_F`'s governed references, checked where the universe is in hand ───────────────────
    # R14: validate the declaration's representation and its governed constituent references, and
    # NOTHING ELSE. In particular do NOT require the prohibition to lie within this family's own
    # root: a governed constituent irrelevant to the present root is lawful and inert, and
    # refusing it would make the declaration a function of today's geometry. A reference that does
    # not resolve as a constituent of the relevant universe IS a governance failure and refuses —
    # `Universe.anchor` already says exactly that, so it is reused rather than reworded.
    pf = body.get("prohibited_constituents")
    if pf is not None and not (isinstance(pf, dict) and set(pf) == {"none"}):
        # REPRESENTATION first, and HERE — not in the family-clause reader, which is reached only
        # when a consumer later resolves the law. A malformed governed clause must refuse at the
        # artifact boundary, or an artifact carrying one publishes cleanly and fails at use.
        if not isinstance(pf, list) or not all(isinstance(r, str) and r for r in pf):
            _refuse(
                f"{what}: prohibited_constituents is a list of constituent references (possibly "
                f"empty); got {pf!r}")
        dupes = sorted({r for r in pf if pf.count(r) > 1})
        if dupes:
            _refuse(
                f"{what}: prohibited_constituents names {dupes} more than once. A prohibition is a "
                f"set condition; repeating a member states nothing further and hides a typo.")
        # GOVERNED REFERENCES second. `Universe.anchor` already refuses a reference that does not
        # resolve as a constituent of this world, in the words this case needs, so it is reused.
        # R14: what is NOT checked is whether the reference lies within this family's own root — a
        # governed constituent irrelevant to the present root is lawful and inert.
        u.anchor(pf)

    family = Family(name=name, family_id=family_id, canonical_reference=canonical_reference,
                    universe_reference=universe_reference, anchor_token=token, body=body,
                    authority=authority, binding=binding)

    # The fourth currency claim. The producer's READER does not make this check — its BUILDER
    # does, before it will publish — so a conforming artifact always satisfies it. Making it here
    # is the consumer's own obligation under N5: a family constitution authority that does not
    # cover the body carried beside it is the same class of defect as a universe attestation that
    # does not cover its law, and a consumer that accepted one would be trusting a digest it
    # could have checked.
    scheme = expected_family_scheme(family, u)
    recomputed = family_fingerprint(family, u, scheme)
    if scheme != authority.scheme:
        _refuse(
            f"{what}: its authority was established under {authority.scheme!r}, and this family's "
            f"governed situation selects {scheme!r}. That is a SCHEME MISMATCH, not a changed "
            f"constitution: across schemes two digests are incomparable, so their inequality "
            f"carries no information about the law. Its remedy is the SAME family re-established "
            f"under {scheme!r} — never a successor family."
        )
    if recomputed != authority.fingerprint:
        _refuse(
            f"{what}: its authority cites {authority.fingerprint!r}, and the identity-bearing "
            f"constitution carried beside it derives {recomputed!r} under {scheme!r}. The "
            f"authority does not cover this family's constitution."
        )
    return family


def _read_constructor(what: str, raw: Any) -> dict[str, Any]:
    """The constructor citation, validated as a CITATION and **not resolved**.

    This reader does not import `foundation` and must not: whether `datumwise.foundation/1#MEAN` names
    a law this build knows is a question for the layer that holds the vocabulary, and answering it here
    would make the artifact boundary depend on which laws happen to be registered. What is checked is
    the only thing checkable from the bytes — that the citation names a vocabulary, a version and a
    law, because *a bare law name is not a citation*."""
    d = _obj(f"{what}: `constructor`", raw)
    _strict(f"{what} constructor", d, CONSTRUCTOR_KEYS)
    for key in sorted(CONSTRUCTOR_KEYS):
        _req(f"{what} constructor", d, key)
    return d


def _read_roles(what: str, label: str, raw: Any, keys: frozenset, families: Mapping[str, Any],
                *, required: bool) -> tuple[tuple[str, str], ...]:
    """A role-indexed list of governed family references: `[{role, family_id}, …]`.

    Shared by `operands` and a basis's `components` because the STRUCTURAL contract is identical — a
    non-empty list, distinct roles, every `family_id` resolving to a governed family in this
    publication. What the roles MEAN differs, and that is why the two live in two types on the record
    rather than one; a shared reader is not a shared meaning.

    **A DANGLING `family_id` REFUSES**, for the reason a dangling universe reference does: a governed
    reference resolves inside its publication and nowhere else, so an expression citing an operand the
    artifact does not carry is not under-specified, it is wrong."""
    if raw is None and not required:
        return ()
    if not isinstance(raw, list) or not raw:
        _refuse(f"{what}: {label!r} must be a non-empty list of role-indexed entries; got {raw!r}")
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for entry in raw:
        d = _obj(f"{what}: a {label} entry", entry)
        _strict(f"{what} {label} entry", d, keys)
        role = _req(f"{what} {label} entry", d, "role")
        fid = _req(f"{what} {label} entry", d, "family_id")
        if role in seen:
            _refuse(
                f"{what}: {label!r} fills role {role!r} twice. A role is an INDEX, not a label: two "
                f"entries under one role state two different things about one position and there is "
                f"no rule for choosing between them."
            )
        seen.add(role)
        if fid not in families:
            _refuse(
                f"{what}: {label!r} role {role!r} names family {fid!r}, which is not declared in this "
                f"publication. A governed operand reference resolves inside its publication and "
                f"nowhere else."
            )
        out.append((role, fid))
    return tuple(out)


def _read_expression(raw: Mapping[str, Any], universes: Mapping[str, Universe],
                     families: Mapping[str, Family]) -> Expression:
    """**Read one governed-expression declaration, or refuse it.**

    Deliberately NOT `_read_family` with branches. The two readers share `_strict`, `_obj` and `_req`
    — the strictness discipline — and nothing else, because every check below is about a fact a family
    does not have and none of the family checks it omits are optional for a family. A shared reader
    would have had to make each of them conditional, and a conditional check is one an artifact can
    steer."""
    name = _req("an expression declaration", raw, "name")
    what = f"expression {name!r}"
    _strict(what, raw, EXPRESSION_KEYS)
    body = _obj(f"{what}: `body`", raw.get("body"))
    _strict(f"{what} body", body, EXPRESSION_BODY_KEYS)

    expression_id = _req(what, body, "expression_id")
    canonical_reference = _req(what, body, "canonical_reference")
    universe_reference = _req(what, body, "universe")
    _req(what, body, "participation")
    _read_constructor(what, body.get("constructor"))

    if universe_reference not in universes:
        _refuse(
            f"{what} names universe {universe_reference!r}, which is not declared in this "
            f"publication. An expression's universe reference resolves inside its publication and "
            f"nowhere else."
        )
    u = universes[universe_reference]

    # ── operands, role-indexed ────────────────────────────────────────────────────────────────
    operands = tuple(Operand(role=r, family_id=f) for r, f in
                     _read_roles(what, "operands", body.get("operands"), OPERAND_KEYS, families,
                                 required=True))

    # ── constitutive inner anchors (§3.6) — resolved, and NOT a root ──────────────────────────
    raw_inner = body.get("inner_anchors")
    if raw_inner is None:
        inner: tuple[str, ...] = ()
    else:
        if not isinstance(raw_inner, list) or not all(isinstance(x, str) and x for x in raw_inner):
            _refuse(f"{what}: `inner_anchors` is a list of anchor tokens (possibly absent); got "
                    f"{raw_inner!r}")
        dupes = sorted({x for x in raw_inner if raw_inner.count(x) > 1})
        if dupes:
            _refuse(
                f"{what}: `inner_anchors` names {dupes} more than once. The inner anchors are a SET "
                f"of constitutive locations; repeating one states nothing further and hides a typo."
            )
        for token in raw_inner:
            if u.denote(token) is None:
                _refuse(
                    f"{what}: its constitutive inner anchor {token!r} denotes no Case-S anchor of "
                    f"universe {universe_reference!r} in this publication. Nothing stands in for a "
                    f"denotation. NOTE WHAT THIS IS NOT: an inner anchor is not a root — it is where "
                    f"the expression is CONSTITUTED, not where its values originate a continuation."
                )
        inner = tuple(raw_inner)

    # ── `parameters` — identity-bearing, and an object ────────────────────────────────────────
    raw_params = body.get("parameters")
    if raw_params is not None and not isinstance(raw_params, dict):
        _refuse(f"{what}: `parameters` must be an object; got {raw_params!r}")

    raw_scope = body.get("scope")
    if raw_scope is not None and not isinstance(raw_scope, str):
        _refuse(f"{what}: `scope` must be a string; got {raw_scope!r}")

    # ── admitted bases — ZERO, ONE, OR SEVERAL ────────────────────────────────────────────────
    raw_bases = body.get("admitted_bases")
    bases: list[AdmittedBasis] = []
    if raw_bases is not None:
        if not isinstance(raw_bases, list):
            _refuse(f"{what}: `admitted_bases` must be a list (possibly empty); got {raw_bases!r}")
        seen_basis: set[str] = set()
        seen_shape: dict[tuple, str] = {}
        for entry in raw_bases:
            d = _obj(f"{what}: an `admitted_bases` entry", entry)
            _strict(f"{what} admitted_bases entry", d, BASIS_KEYS)
            basis_id = _req(f"{what} admitted_bases entry", d, "basis_id")
            if basis_id in seen_basis:
                _refuse(f"{what}: basis_id {basis_id!r} is declared twice; a basis is identified, "
                        f"not labelled.")
            seen_basis.add(basis_id)
            rcp = d.get("requires_common_participation")
            if not isinstance(rcp, bool):
                _refuse(
                    f"{what}: basis {basis_id!r} states `requires_common_participation` "
                    f"{rcp!r}. It must be a boolean and it must be PRESENT: absent would mean 'no "
                    f"joint requirement to check', and a SUM and a COUNT that ranged over different "
                    f"contributions are individually valid and jointly meaningless. Absence is the "
                    f"one reading that licenses exactly the pairing the field exists to forbid."
                )
            components = tuple(BasisComponent(role=r, family_id=f) for r, f in
                               _read_roles(f"{what} basis {basis_id!r}", "components",
                                           d.get("components"), BASIS_COMPONENT_KEYS, families,
                                           required=True))
            shape = tuple(sorted((c.role, c.family_id) for c in components))
            if shape in seen_shape:
                _refuse(
                    f"{what}: basis {basis_id!r} admits the same role-to-family assignment as "
                    f"{seen_shape[shape]!r}. Two ids over one route are not two alternative bases; "
                    f"they are one route counted twice, and the agreement obligation between "
                    f"alternatives would be trivially satisfied by the duplicate."
                )
            seen_shape[shape] = basis_id
            bases.append(AdmittedBasis(basis_id=basis_id, components=components,
                                       requires_common_participation=rcp))

    # ── authority and binding ─────────────────────────────────────────────────────────────────
    araw = _obj(f"{what}: `expression_constitution_authority`",
                raw.get("expression_constitution_authority"))
    _strict(f"{what} expression_constitution_authority", araw, EXPRESSION_AUTHORITY_KEYS)
    authority = ExpressionAuthority(
        established_by=_req(f"{what} expression_constitution_authority", araw, "established_by"),
        at=_req(f"{what} expression_constitution_authority", araw, "at"),
        fingerprint=_req(f"{what} expression_constitution_authority", araw,
                         "constitution_fingerprint"),
        scheme=_req(f"{what} expression_constitution_authority", araw, "fingerprint_scheme"))
    if authority.scheme != ECF1:
        _refuse(
            f"{what}: its constitution authority declares scheme {authority.scheme!r}; the "
            f"expression contract knows {[ECF1]}. In particular an expression is NOT established "
            f"under `{FCF1}` or `{FCF2}`: those schemes digest a family's identity-bearing keys, "
            f"which are not this object's."
        )

    braw = raw.get("universe_authority_binding")
    if braw is None:
        _refuse(
            f"{what}: an expression carries NO `universe_authority_binding`, and this contract "
            f"requires one. `{ECF1}` takes the `universe` SPELLING out of the identity payload on the "
            f"ground that the world is governed through the binding — so without a binding the world "
            f"is in no payload and under no authority, which is a hole rather than a transition. A "
            f"FAMILY may be UNBOUND because `{FCF1}` predates the binding and hashed the spelling "
            f"instead; an expression has no such history to stay compatible with."
        )
    b = _obj(f"{what}: `universe_authority_binding`", braw)
    _strict(f"{what} universe_authority_binding", b, BINDING_KEYS)
    binding = UniverseAuthorityBinding(
        bound_by=_req(f"{what} universe_authority_binding", b, "bound_by"),
        at=_req(f"{what} universe_authority_binding", b, "at"),
        universe_reference=_req(f"{what} universe_authority_binding", b, "universe_reference"),
        universe_authority=_req(f"{what} universe_authority_binding", b, "universe_authority"),
        universe_authority_scheme=_req(f"{what} universe_authority_binding", b,
                                       "universe_authority_scheme"))
    if binding.universe_reference != universe_reference:
        _refuse(f"{what}: its U-authority binding cites universe {binding.universe_reference!r} "
                f"while the expression states {universe_reference!r}.")
    cited = (binding.universe_authority, binding.universe_authority_scheme)
    carried = (u.attestation.fingerprint, u.attestation.scheme)
    if cited != carried:
        _refuse(
            f"{what}: its U-authority binding cites {cited[1]}:{cited[0]!r} for universe "
            f"{universe_reference!r}, and the universe carried in this publication is attested "
            f"{carried[1]}:{carried[0]!r}. The binding does not cover the world published beside it."
        )

    expr = Expression(
        name=name, expression_id=expression_id, canonical_reference=canonical_reference,
        universe_reference=universe_reference, inner_anchor_tokens=inner, operands=operands,
        admitted_bases=tuple(bases), body=body, authority=authority, binding=binding)

    recomputed = expression_fingerprint(expr, u)
    if recomputed != authority.fingerprint:
        _refuse(
            f"{what}: its authority cites {authority.fingerprint!r}, and the identity-bearing "
            f"constitution carried beside it derives {recomputed!r} under {ECF1!r}. The authority "
            f"does not cover this expression's constitution. **NOTE WHICH CHANGES CAN CAUSE THIS AND "
            f"WHICH CANNOT**: `{ECF1}` digests the constructor, the role-indexed operands, the "
            f"resolved inner anchors, participation, scope and the identity-bearing parameters. "
            f"Admitting or withdrawing a sufficient BASIS cannot reach this digest, by design."
        )
    return expr


def parse_native_publication(data: Any) -> NativePublication:
    """Read a native-v3 artifact into the resolved model, or refuse it.

    **Everything checked here is checkable from the bytes in front of it.** Nothing is fetched,
    no second source is consulted, and no producer is imported."""
    top = _obj("a native publication", data)
    version = read_version(top.get("publication_format_version"))
    _strict("the publication", top, TOP_LEVEL_KEYS)

    ref = _obj("`ref`", top.get("ref"))
    _strict("`ref`", ref, {"manifold_id", "version"})
    manifold_id = _req("`ref`", ref, "manifold_id")
    manifold_version = _req("`ref`", ref, "version")

    published = _obj("`published`", top.get("published"))
    _strict("`published`", published, {"by", "at"})
    published_by = _req("`published`", published, "by")
    published_at = _req("`published`", published, "at")

    raw_decls = top.get("declarations")
    if not isinstance(raw_decls, list):
        _refuse("`declarations` must be a list.")

    universes: dict[str, Universe] = {}
    raw_families: list[dict[str, Any]] = []
    raw_expressions: list[dict[str, Any]] = []
    kinds = admitted_kinds(version)
    for entry in raw_decls:
        d = _obj("a declaration", entry)
        kind = d.get("kind")
        if not isinstance(kind, str) or not kind:
            _refuse("a declaration states no `kind`.")
        if kind not in kinds:
            # TWO REFUSALS, BECAUSE THERE ARE TWO SITUATIONS AND THEIR REMEDIES DIFFER. A kind no
            # minor admits is a sort that does not exist. A kind a LATER minor admits is a sort that
            # exists and that THIS artifact's declared contract does not carry — whose remedy is to
            # re-declare the artifact under that minor, by someone with authority to do it.
            later = minor_admitting(kind)
            if later is not None:
                _refuse(
                    f"declaration kind {kind!r} is admitted at native v{later}, and this artifact "
                    f"declares publication format {version}, which admits {sorted(kinds)}. The kind "
                    f"is NOT rejected as unlawful and this reader will NOT read it anyway: a minor is "
                    f"part of the contract, and treating it as a formality is how a reader comes to "
                    f"accept meaning the declaring artifact never claimed to carry. Re-declare the "
                    f"artifact as v{later}."
                )
            _refuse(
                f"declaration kind {kind!r} is not admitted in publication format {version}. "
                f"This contract admits {sorted(kinds)}; a kind is admitted by positive "
                f"standing, never because an earlier format carried it. `anchor` in particular "
                f"has no referent here: a Case-S anchor is DERIVED from a constitution, which "
                f"makes it structurally unwritable as a declaration."
            )
        if kind == "expression":
            raw_expressions.append(d)
            continue
        if kind == "universe":
            u = _read_universe(d)
            if u.name in universes:
                _refuse(
                    f"universe name {u.name!r} is declared twice: a family resolves its universe "
                    f"by reference within this publication, so the reference must denote one. "
                    f"This is contextual resolution, not a claim about universe identity."
                )
            universes[u.name] = u
        else:
            raw_families.append(d)

    families: list[Family] = []
    seen_ids: dict[str, str] = {}
    references: dict[str, str] = {}
    for d in raw_families:
        f = _read_family(d, universes)
        if f.family_id in seen_ids:
            _refuse(f"family_id {f.family_id!r} is declared twice: identity is not a label.")
        seen_ids[f.family_id] = f.name
        aliases = [a for a in (f.body.get("aliases") or []) if isinstance(a, str) and a]
        for r in (f.canonical_reference, *aliases):
            if r in references:
                _refuse(
                    f"reference {r!r} resolves to two families ({references[r]} and "
                    f"{f.family_id}); two distinct active identities cannot be hidden under one "
                    f"ambiguous canonical reference."
                )
            references[r] = f.family_id
        families.append(f)

    # ── the second sort, read AFTER the families it cites ─────────────────────────────────────
    #
    # ORDER IS LOAD-BEARING, NOT INCIDENTAL. An expression's operands and basis components are
    # governed FAMILY references, and a dangling one refuses — so the families must be in hand. The
    # converse never arises: no family declaration cites an expression, because §7.1 keeps the two
    # lineages apart and a family's parents are families.
    by_family_id = {f.family_id: f for f in families}
    expressions: list[Expression] = []
    for d in raw_expressions:
        x = _read_expression(d, universes, by_family_id)
        # **ONE IDENTITY SPACE ACROSS BOTH SORTS, AND ONE REFERENCE SPACE.** Not because a family and
        # an expression could be confused inside this reader — they are two tuples and two types — but
        # because a REQUEST carries a reference and nothing else. If one reference could name both, the
        # sort a request resolved to would depend on which lookup a consumer happened to try first,
        # which is the dispatch defect this whole unit exists to remove.
        if x.expression_id in seen_ids:
            _refuse(f"expression_id {x.expression_id!r} is already declared as a family_id in this "
                    f"publication ({seen_ids[x.expression_id]}): identity is not a label, and the two "
                    f"sorts share one identity space.")
        if x.expression_id in {e.expression_id for e in expressions}:
            _refuse(f"expression_id {x.expression_id!r} is declared twice: identity is not a label.")
        for r in (x.canonical_reference, *x.aliases):
            if r in references:
                _refuse(
                    f"reference {r!r} resolves to two governed objects ({references[r]} and "
                    f"{x.expression_id}); a request carries a reference and nothing else, so a "
                    f"reference that named both sorts would make the SORT of the answer depend on "
                    f"which lookup ran first."
                )
            references[r] = x.expression_id
        expressions.append(x)

    return NativePublication(
        manifold_id=manifold_id, version=manifold_version, format_version=version,
        published_by=published_by, published_at=published_at,
        universes=tuple(universes.values()), families=tuple(families),
        expressions=tuple(expressions))


def load_native_publication(path: str) -> NativePublication:
    """Read a native-v3 artifact from disk (stdlib JSON only). Malformed JSON is a refusal like
    any other structural defect."""
    try:
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except json.JSONDecodeError as exc:
        _refuse(f"artifact is not valid JSON: {exc}")
    return parse_native_publication(raw)

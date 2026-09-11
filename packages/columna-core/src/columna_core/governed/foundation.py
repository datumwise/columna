"""
columna_core.governed.foundation — the shared foundation-law vocabulary.

GOVERNED SEMANTIC VOCABULARY, CITED BY FAMILIES, OWNED BY NEITHER SIDE OF THE BOUNDARY.

A foundation law (SUM, COUNT, MIN, MAX, MEAN …) is a *constituent* of a family's `Law(F)`. It is
never a family identity: two families citing SUM are not the same family, and a family is not
identified by the law it cites (Huayin, 2026-09-11).

WHAT LIVES HERE — semantic content only:
  · the target form the law asserts
  · the governed value domains it admits, and the result domain it yields
  · the composition it induces when used as a CONTINUATION, and that composition's algebra
  · which law continues values formed by it
  · the sufficient state it requires, ANALYTICALLY
  · whether it is exact or approximate

WHAT DOES NOT LIVE HERE, and why this module is not `columna_core.operators` promoted:
`deliver_sql`, `scan_impl`, `in_core`, the planner's REDUCER/SCAN/MAP routing tag, and the
representation half of `witness` are all REALIZATION. ToD v7.1 §3.6 is explicit that routing confers
nothing — *"Neither operation receives or loses family authority solely from an implementation
classification"* — and §8.5 that *"the witness need not have one physical format."* The operator
registry holds much of the semantic content this module needs, and holding it is not the same as
having standing to be the authority for it. So this vocabulary is RE-DERIVED, not re-exported, and
a conformance test pins the two against each other rather than deriving one from the other.

VERSIONED AND IMMUTABLE. A citation names `(vocabulary, version, law)`. A consumer that does not
know the cited vocabulary, version or law REFUSES; it never falls back to a law of the same name at
a different version, because a law whose content moved is a different law and §3.9 makes a change of
declared continuation a family succession.

VALUE DOMAINS ARE THE GOVERNED VOCABULARY, not Core dtypes — the same token set the authoring side
uses (`integer`, `decimal`, `text`, `boolean`, `date`, `timestamp`, `time`). Mapping them onto an
engine's types is realization and happens in the compiler.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

#: The vocabulary's identity. A citation that names a different vocabulary is refused, not guessed.
VOCABULARY = "datumwise.foundation"

#: The vocabulary VERSION. Immutable: changing any law's content mints a new version, because a
#: family that cited the old content declared something else (§3.9).
VERSION = "1"

#: Governed value domains — the authoring vocabulary, deliberately not Core's dtypes.
DOMAINS = frozenset({"integer", "decimal", "text", "boolean", "date", "timestamp", "time"})

#: Admits any governed domain.
ANY_DOMAIN = frozenset(DOMAINS)

#: `result_domain` sentinel: the law yields the operand's own domain.
SAME_AS_OPERAND = "same_as_operand"

#: `entails_continuation` sentinel: values formed by this law do not compose across refinement.
NO_CONTINUATION = "none"

#: Composition tokens — the analytical composition, not an engine dispatch tag.
ADDITION, MINIMUM, MAXIMUM, SET_UNION = "addition", "minimum", "maximum", "set_union"


class UnknownFoundationLaw(LookupError):
    """A citation names a vocabulary, version or law this build does not know.

    Raised by `resolve`, and it is a REFUSAL condition at every consumer: an unknown law is never
    approximated by a same-named law at another version."""


@dataclass(frozen=True)
class FoundationLaw:
    """One governed foundation law. Semantic content only."""

    name: str
    #: What quantity the law asserts, given an operand and a participation rule. Prose, because the
    #: target form is what a human establishes; the machine-checkable parts are the fields below.
    target_form: str
    #: Governed value domains this law admits as an operand.
    operand_domains: frozenset
    #: The domain of the result: SAME_AS_OPERAND, or a fixed governed domain.
    result_domain: str
    #: The law that continues values formed by this law across admitted refinement, or
    #: NO_CONTINUATION. ENTAILED, not chosen: counts compose by addition whatever anyone prefers.
    entails_continuation: str
    #: What information must be retained for the continuation to be exact. Analytical, not a format.
    sufficient_state: str
    #: `exact` or `approximate`. An approximate law is a §10.9 disclosure, never a silent default.
    approximation: str = "exact"
    #: Identity-bearing parameters the law requires (e.g. FIRST/LAST need a constitutive order).
    required_parameters: tuple = ()

    # ── the law USED AS A CONTINUATION. Absent where it may not be. ──────────────────────────────
    #: May this law be cited as another family's continuation?
    usable_as_continuation: bool = True
    #: The composition it induces on the value domain.
    composition: Optional[str] = None
    #: Does that composition have an identity element? A THEOREM about the law, never a preference —
    #: and the whole of the MIN/MAX empty-fiber question (§5.2, §6.1.1, §11.5.1).
    has_identity: bool = False
    associative: bool = True
    commutative: bool = True
    #: Why the identity does or does not exist, in the theory's own words. Carried so that a refusal
    #: can quote the reason rather than assert it.
    identity_note: str = ""

    # ── ENTAILED FACTS. Derived here, never declared per family (ruling: "mathematical consequences
    #    of an established law should be derived rather than re-asked"). ──────────────────────────
    @property
    def self_sufficient(self) -> bool:
        """§5.2 — the family's own values compose across admitted refinement by an associative and
        commutative continuation law."""
        law = self.entails_continuation
        if law == NO_CONTINUATION:
            return False
        other = LAWS.get(law)
        return bool(other and other.associative and other.commutative)

    @property
    def empty_fiber(self) -> str:
        """What the family's result denotes at an admitted anchor with NO contribution.

        ENTAILED from the continuation's algebra, and established once here for every family that
        cites the law (ruling, 2026-09-11):

          `identity`  a monoid identity exists, so an empty fiber lawfully folds to it;
          `no_value`  a commutative semigroup with no identity supplies no fold value — §11.5.1,
                      *"an empty eligible fiber receives no MIN/MAX value from the semigroup alone"*;
          `not_applicable`  the family does not compose, so there is no fold to take.
        """
        law = self.entails_continuation
        if law == NO_CONTINUATION:
            return "not_applicable"
        other = LAWS.get(law)
        if other is None:                                   # pragma: no cover - guarded by selftest
            return "not_applicable"
        return "identity" if other.has_identity else "no_value"

    def admits_operand(self, domain: str) -> bool:
        return domain in self.operand_domains

    def result_for(self, operand_domain: str) -> str:
        return operand_domain if self.result_domain == SAME_AS_OPERAND else self.result_domain


@dataclass(frozen=True)
class LawCitation:
    """A family's reference to a foundation law: `(vocabulary, version, law)`.

    Immutable and backend-independent by construction — nothing here names an engine, a connection
    or an operator. `resolve` is the only way to turn one into content."""

    vocabulary: str
    version: str
    law: str

    def __str__(self) -> str:
        return f"{self.vocabulary}/{self.version}#{self.law}"

    def to_dict(self) -> dict:
        return {"vocabulary": self.vocabulary, "version": self.version, "law": self.law}

    @classmethod
    def from_dict(cls, d) -> "LawCitation":
        if not isinstance(d, dict):
            raise UnknownFoundationLaw(f"foundation-law citation is not an object: {d!r}")
        v, ver, law = d.get("vocabulary"), d.get("version"), d.get("law")
        for field_name, value in (("vocabulary", v), ("version", ver), ("law", law)):
            if not isinstance(value, str) or not value:
                raise UnknownFoundationLaw(
                    f"foundation-law citation is missing {field_name!r}; a citation must name "
                    f"vocabulary, version and law — a bare law name is not a citation")
        return cls(v, ver, law)


def cite(law: str) -> LawCitation:
    """A citation into THIS build's vocabulary version. For authoring and tests."""
    return LawCitation(VOCABULARY, VERSION, law)


# ── the vocabulary ───────────────────────────────────────────────────────────────────────────────
LAWS: dict = {
    "SUM": FoundationLaw(
        name="SUM",
        target_form=("the additive total of the operand's participating contributions, where the "
                     "operand domain and participation law admit addition (§11.5.1)"),
        operand_domains=frozenset({"integer", "decimal"}),
        result_domain=SAME_AS_OPERAND,
        entails_continuation="SUM",
        sufficient_state="the running total",
        composition=ADDITION,
        has_identity=True,
        identity_note="addition has the identity 0, so an empty fiber lawfully folds to it",
    ),
    "COUNT": FoundationLaw(
        name="COUNT",
        target_form=("a count of participations. §11.5.1 distinguishes TWO targets — `count(I)` "
                     "counts participating analytical points of the anchor, `count(x@I)` counts "
                     "participation under the operand construction's governed rule — and calls them "
                     "'distinct targets'. Which one a family asserts is part of its target "
                     "specification and is NOT supplied by citing this law"),
        operand_domains=ANY_DOMAIN,
        result_domain="integer",
        entails_continuation="SUM",
        sufficient_state="the running count",
        # §5.2, verbatim: "two retained count states 37 and 12 can combine to 49 under count-state
        # continuation. Counting the two scalar values as new observations gives 2." So COUNT is
        # exactly the law that must NOT be cited as a continuation — citing it would perform the
        # error the theory uses to introduce the distinction.
        usable_as_continuation=False,
        composition=None,
        identity_note="COUNT continues by SUM; counting count-states as new observations is the "
                      "§5.2 error and this vocabulary refuses it",
    ),
    "MIN": FoundationLaw(
        name="MIN",
        target_form="the least operand VALUE under its semantic value order (§11.5.1)",
        operand_domains=frozenset({"integer", "decimal", "date", "timestamp", "time", "text"}),
        result_domain=SAME_AS_OPERAND,
        entails_continuation="MIN",
        sufficient_state="the least value so far",
        composition=MINIMUM,
        has_identity=False,
        identity_note=("§5.2: 'MIN and MAX need not acquire an artificial identity or semantic Null "
                       "in order to qualify.' A commutative semigroup with no identity, so an empty "
                       "eligible fiber receives no value from the semigroup alone (§6.1.1)"),
    ),
    "MAX": FoundationLaw(
        name="MAX",
        target_form="the greatest operand VALUE under its semantic value order (§11.5.1)",
        operand_domains=frozenset({"integer", "decimal", "date", "timestamp", "time", "text"}),
        result_domain=SAME_AS_OPERAND,
        entails_continuation="MAX",
        sufficient_state="the greatest value so far",
        composition=MAXIMUM,
        has_identity=False,
        identity_note="as MIN (§5.2, §6.1.1)",
    ),
    # Registered as vocabulary, NOT because this build can serve it. A family may lawfully cite MEAN
    # and Core will refuse the realization — which is §4.1's rule that a backend's inability does not
    # remove a law. It is also the vocabulary's worked example of NO_CONTINUATION.
    "MEAN": FoundationLaw(
        name="MEAN",
        target_form=("the arithmetic mean over the participating contributions. §11.5.2's exact "
                     "finite basis is a matching SUM and COUNT with the same participating "
                     "contributions in both components"),
        operand_domains=frozenset({"integer", "decimal"}),
        result_domain="decimal",
        entails_continuation=NO_CONTINUATION,
        sufficient_state=("no finite witness is carried by the displayed value — §5.2: 'a displayed "
                          "scalar generally loses the weight required for exact continuation. Its "
                          "SUM and COUNT basis retains that information.'"),
        usable_as_continuation=False,
        identity_note="does not compose; a mean of means is not a mean",
    ),
}


def resolve(citation: LawCitation) -> FoundationLaw:
    """Turn a citation into law content, or REFUSE.

    Never falls back across versions: a law whose content moved is a different law, and a family
    that cited the old content declared something else (§3.9)."""
    if citation.vocabulary != VOCABULARY:
        raise UnknownFoundationLaw(
            f"unknown foundation-law vocabulary {citation.vocabulary!r}; this build knows only "
            f"{VOCABULARY!r}")
    if citation.version != VERSION:
        raise UnknownFoundationLaw(
            f"foundation-law vocabulary {citation.vocabulary!r} version {citation.version!r} is not "
            f"known to this build (it carries version {VERSION!r}). A law whose content moved is a "
            f"different law; this build will not substitute its own.")
    law = LAWS.get(citation.law)
    if law is None:
        raise UnknownFoundationLaw(
            f"{citation} names no law in this vocabulary (known: {sorted(LAWS)})")
    return law


def selftest() -> list:
    """Structural invariants of the vocabulary itself. Run by a test, and by the CLI gate."""
    problems = []
    for name, law in LAWS.items():
        if law.name != name:
            problems.append(f"{name}: keyed under a different name than it carries ({law.name})")
        if not law.operand_domains <= DOMAINS:
            problems.append(f"{name}: operand_domains outside the governed vocabulary")
        if law.result_domain != SAME_AS_OPERAND and law.result_domain not in DOMAINS:
            problems.append(f"{name}: result_domain {law.result_domain!r} is not a governed domain")
        cont = law.entails_continuation
        if cont != NO_CONTINUATION:
            other = LAWS.get(cont)
            if other is None:
                problems.append(f"{name}: entails continuation {cont!r}, which is not a law here")
            elif not other.usable_as_continuation:
                problems.append(
                    f"{name}: entails continuation {cont!r}, which is not usable as a continuation")
        if law.usable_as_continuation and law.composition is None:
            problems.append(f"{name}: usable as a continuation but states no composition")
        if not law.usable_as_continuation and law.composition is not None:
            problems.append(f"{name}: not usable as a continuation but states a composition")
        if law.has_identity and not law.usable_as_continuation:
            problems.append(f"{name}: claims an identity while not usable as a continuation")
        if not law.identity_note:
            problems.append(f"{name}: carries no identity_note — a theorem with no stated reason")
    return problems

"""The narrow admission boundary — five checks, all refusing, none defaulting.

ADMISSION IS WHERE A CONCRETE PRECISION EXISTS. A governed `value_domain` is the bare token
`"decimal"` — no precision, no scale — so at LOWERING there is nothing to compare against a substrate
envelope, and refusing there would require inventing a precision. That is why the envelope refusal
lives here and could not live in the compiler (ruling 2026-09-12, §4).

The checks, and what each exists to stop:

    CHECK 1  governed value domain  <->  carrier type, within the measured envelope.
             Stops a SUCCESSFULLY DELIVERED carrier that is not the governed thing.
    CHECK 2  carrier NULL  !=  analytical absence.
             Stops the carrier's "no value here" being read as a governed answer nobody gave.
    CHECK 3  realization GRAIN  <->  governed contribution structure.          (2026-09-14)
             Stops material at the wrong grain being folded, or not folded, by accident.
    CHECK 4  carrier COORDINATES  <->  the anchor's declared components.       (2026-09-14)
             Stops a value being retained at an analytical point nobody governed.
    CHECK 5  the COINCIDENT claim  <->  the material actually delivered.        (2026-09-14)
             Stops a claim of one-contribution-per-point standing over material that has several.

CHECKS 3 AND 4 ARE WHY `realization` IS A PARAMETER. It was one before they existed, and was never
read — the seam was reserved and empty, which is the shape a check takes before it is written
(rowed as part of the material-slice reconnaissance). A grain claim is the realization's statement
about how its rows stand to the anchor's points, and it is meaningless until there is material; so
like the envelope refusal, it could not live at lowering and it lives here.

SUCCESSFUL TRANSPORT DOES NOT ESTABLISH ADMISSIBILITY. The admission study's conclusion, inherited
verbatim, and the reason this module exists at all: every negative control below DELIVERS. None of
them raises on the way in. If admission defaults to accept, every one of them is served as if it
were governed law.
"""
from __future__ import annotations
from dataclasses import dataclass

import pyarrow as pa

from columna_core.compiler.realization import COINCIDENT
from columna_core.governed.publication import COINCIDENT as GOVERNED_COINCIDENT
from columna_core.governed.publication import PRIMITIVE
from columna_core.governed.resolve import (
    C4_FORMATION, C6_SEMANTIC_VALUES, C9_EXCEPTIONAL, ESTABLISHED,
)

from . import carrier as _carrier
from .refusals import WantOfLaw, WantOfState

#: THE DISTINCTION, RECORDED VERBATIM (ruled Huayin, 2026-09-12). Kept as a constant rather than a
#: comment because it is EVIDENCE: it is the sentence that makes the check below non-obvious, and a
#: future reader who deletes the check should have to delete this too.
EMPTY_FIBER_RULING = (
    "Empty-fiber law governs evaluation of a constituted fiber with no contributions. It does not "
    "establish analytical existence, eligibility, observed support, carrier nullability, or the "
    "meaning of an absent observation."
)

#: C9 keys that are CONTINUATION ENTAILMENTS, not missingness declarations. Their presence says
#: nothing about what an absent observation denotes. Listed rather than inferred, so that a C9 key
#: added later is treated as unknown-and-refused rather than silently counted as absence law.
_ENTAILED_NOT_ABSENCE = frozenset({"empty_fiber"})

#: Governed domains this proof knows how to admit. NARROW ON PURPOSE — an unknown domain refuses
#: rather than being waved through, because "we did not recognise it" must not read as "it is fine".
_ADMISSIBLE = {"decimal"}


@dataclass(frozen=True)
class Admitted:
    """A carrier that passed admission, with the governed domain it was admitted AGAINST.

    Carrying the domain forward matters: what is retained downstream is not "some decimal numbers",
    it is "the carrier admitted as the governed decimal domain of this family". The physical
    representation never gets to redefine that."""

    array: pa.Array
    governed_domain: str
    carrier_type: str
    measured_as: str


def admit(law_view, realization, carrier: _carrier.Carrier) -> Admitted:
    """Admit a carrier against a family's resolved law, or refuse in the right jurisdiction."""
    subject = law_view.canonical_reference

    # ── CHECK 1 · the governed value domain against the physical carrier ────────────────────────
    c6 = law_view[C6_SEMANTIC_VALUES]
    if c6.standing != ESTABLISHED:
        raise WantOfLaw(
            f"the value domain is {c6.standing}, so there is nothing to admit a carrier against; "
            f"admission may not choose a domain on the law's behalf", subject=subject)

    domain = c6.value
    if domain not in _ADMISSIBLE:
        raise WantOfState(
            f"governed value domain {domain!r} is outside this proof's admission vocabulary; "
            f"refusing rather than accepting an unrecognised domain", subject=subject)

    t = carrier.type

    if pa.types.is_floating(t):
        # THE RULING'S OTHER HALF. Not "the precision is inconvenient" — binary floating point is not
        # an exact-decimal carrier at all, so this is the silent lowering the ruling forbids.
        raise WantOfState(
            f"governed exact-decimal domain {domain!r} presented on a binary floating-point carrier "
            f"({_carrier.describe(carrier)}); delivery succeeded and the value is already not the "
            f"governed one [{carrier.measured_as}]", subject=subject)

    if not pa.types.is_decimal(t):
        raise WantOfState(
            f"governed exact-decimal domain {domain!r} presented on carrier "
            f"{_carrier.describe(carrier)}, which is not an exact-decimal carrier", subject=subject)

    if t.precision > _carrier.DECIMAL128_MAX_PRECISION:
        raise WantOfState(
            f"carrier precision {t.precision} exceeds the measured faithfully-supported envelope "
            f"({_carrier.DECIMAL128_MAX_PRECISION} digits)", subject=subject)

    if t.precision == _carrier.DECIMAL128_MAX_PRECISION and t.scale == 0:
        # THE FOURTH HOP, MEASURED. Exact in Arrow, lost on the in-process conversion, and nothing
        # raises in between. Admission refuses at the boundary where the loss is still preventable.
        raise WantOfState(
            f"carrier {_carrier.describe(carrier)} is exact in Arrow but is not faithfully carried "
            f"across the in-process conversion [{carrier.measured_as}]; the envelope is four hops, "
            f"and this one fails at the fourth", subject=subject)

    # ── CHECK 2 · a carrier NULL is not an analytical absence ───────────────────────────────────
    # The carrier faithfully reports THAT a value is absent (the study measured the null and the
    # decimal type both surviving, validity bitmap distinct from values). What the absence DENOTES is
    # governed, and admission will not decide it.
    #
    # FINDING 3 — C9 "ESTABLISHED" DOES NOT MEAN ABSENCE IS GOVERNED.
    # The obvious check is `if C9.standing != ESTABLISHED: refuse`. It is WRONG, and lighthouse is the
    # case that shows why: C9 resolves ESTABLISHED with value {'empty_fiber': 'identity'}. That is an
    # entailment of CONTINUATION ALGEBRA — what the fold over an EMPTY FIBER denotes — and it is not a
    # statement about what an ABSENT OBSERVATION denotes. Two different objects, and for SUM they are
    # numerically coincident, which is exactly what makes the substitution invisible.
    #
    # Reading C9's STANDING as the answer would let an aggregation theorem stand in for a missingness
    # declaration — the withdrawn `empty_fiber -> FILL` mapping, re-made at the admission boundary
    # instead of the lowering one. So the check reads C9's CONTENT for a rule about absent
    # observations, and refuses when it finds only `empty_fiber`.
    if carrier.null_count:
        c9 = law_view[C9_EXCEPTIONAL]
        governs_absence = (
            c9.standing == ESTABLISHED
            and isinstance(c9.value, dict)
            and bool(set(c9.value) - _ENTAILED_NOT_ABSENCE)
        )
        if not governs_absence:
            carried = sorted(c9.value) if isinstance(c9.value, dict) else c9.value
            raise WantOfLaw(
                f"the carrier presents {carrier.null_count} absent observation(s); the family's "
                f"exceptional-case law is {c9.standing} and carries {carried!r}, which answers what "
                f"the fold over an EMPTY FIBER denotes, not what an ABSENT OBSERVATION denotes. "
                f"Admission will not substitute the one for the other",
                subject=subject)

    return Admitted(array=carrier.array, governed_domain=domain,
                    carrier_type=str(t), measured_as=carrier.measured_as)


def admit_anchored(law_view, realization, anchored: _carrier.AnchoredCarrier,
                   declared_components) -> Admitted:
    """Admit an ANCHORED carrier: `admit`'s two checks, plus the two that need coordinates.

    ORDER IS LOAD-BEARING AND IS THE SAME ORDER AS EVERYWHERE ELSE ON THIS PATH — the checks that
    can be answered from LAW AND CLAIM ALONE run before the one that inspects values. A grain
    mismatch and a coordinate mismatch are both knowable without looking at a single number, and a
    carrier refused for its representation when its coordinates were already wrong would send an
    operator to fix the narrower of two faults.

    `declared_components` is the anchor's component set, read from the governed publication by the
    caller. It is passed in rather than resolved here for the reason `basis` is: this function
    executes law, it does not go looking for it."""
    subject = law_view.canonical_reference

    # ── CHECK 3 · the grain claim against the governed contribution structure ───────────────────
    # The realization CLAIMS how its rows stand to the anchor's points; C4 DECLARES how contributions
    # form a constituted value. `coincident` on both sides means one row per point and nothing to
    # resolve, which is the only correspondence this slice implements. The two are different facts
    # and the check is that they agree — not that either is read off the other.
    c4 = law_view[C4_FORMATION]
    if c4.standing != ESTABLISHED:
        raise WantOfLaw(
            f"the formation responsibility is {c4.standing}, so there is no governed contribution "
            f"structure for the realization's grain claim to agree with", subject=subject)
    formation = c4.value if isinstance(c4.value, dict) else {}
    if formation.get("kind") != PRIMITIVE:
        raise WantOfLaw(
            f"this profile admits material for a PRIMITIVE family; {subject} is formed by "
            f"{formation.get('kind')!r}, whose value is computed from its operands and is not read "
            f"from a source", subject=subject)
    structure = formation.get("contribution_structure")
    if structure != GOVERNED_COINCIDENT:
        raise WantOfLaw(
            f"the governed contribution structure is {structure!r} — several contributions per "
            f"analytical point, resolved by law — and this slice admits only coincident material; "
            f"folding them here would be this profile deciding a resolution the law names",
            subject=subject)
    if realization.grain != COINCIDENT:
        raise WantOfState(
            f"the realization claims grain {realization.grain!r} while the governed contribution "
            f"structure is coincident: one of the two is wrong, and admission will not choose. "
            f"A finer claim asks for a resolution this material cannot be assumed to have had",
            subject=subject)

    # ── CHECK 4 · the carrier's coordinates against the anchor's declared components ────────────
    # EXACT SET EQUALITY, in both directions, and deliberately not a subset test. A missing
    # coordinate would retain a value at a point coarser than the one it was constituted at — which
    # is movement, and movement needs a positive licence. An EXTRA coordinate would retain it at a
    # finer point than the anchor names, which is a value the publication never declared.
    carried = frozenset(anchored.anchor_columns)
    declared = frozenset(declared_components)
    if carried != declared:
        missing, extra = sorted(declared - carried), sorted(carried - declared)
        raise WantOfState(
            f"the carrier's coordinates {sorted(carried)} are not the anchor's declared components "
            f"{sorted(declared)}"
            + (f"; missing {missing}" if missing else "")
            + (f"; not declared: {extra}" if extra else "")
            + ". A value retained at coordinates the publication does not declare is retained at an "
              "analytical point nobody governed", subject=subject)

    # ── CHECK 5 · the coincident claim against the material that actually arrived ──────────────
    # CHECK 3 compared two CLAIMS — the realization's grain and the governed contribution structure.
    # Neither of them is the material. `coincident` says "one contribution per analytical point"
    # (C4's own note), which is a statement about rows, and it is checkable the moment rows exist.
    #
    # WITHOUT THIS, "COINCIDENT" IS AN UNTESTED ASSERTION AND TWO PATHS GO WRONG DIFFERENTLY. A
    # family served WITHOUT formation would emit two rows at one analytical point — two answers to
    # one governed question, under an anchor that declares one. A family served WITH formation would
    # silently fold contributions the governed contribution structure says do not exist, which is
    # resolution law being performed by a profile that was told there was none to perform.
    if realization.grain == COINCIDENT:
        seen, repeated = set(), set()
        for row in anchored.table.select(list(anchored.anchor_columns)).to_pylist():
            key = tuple(row[c] for c in anchored.anchor_columns)
            (repeated if key in seen else seen).add(key)
        if repeated:
            raise WantOfState(
                f"the realization claims COINCIDENT grain — one contribution per analytical point — "
                f"and the material presents several at {len(repeated)} point(s), e.g. "
                f"{sorted(repeated)[0]}. Folding them here would perform a resolution the governed "
                f"contribution structure says there is none of", subject=subject)

    # ── CHECKS 1 and 2, unchanged, on the value column ─────────────────────────────────────────
    return admit(law_view, realization, anchored.as_carrier())

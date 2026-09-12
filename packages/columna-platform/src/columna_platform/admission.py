"""The narrow admission boundary — two checks, both refusing, neither defaulting.

ADMISSION IS WHERE A CONCRETE PRECISION EXISTS. A governed `value_domain` is the bare token
`"decimal"` — no precision, no scale — so at LOWERING there is nothing to compare against a substrate
envelope, and refusing there would require inventing a precision. That is why the envelope refusal
lives here and could not live in the compiler (ruling 2026-09-12, §4).

The two checks, and what each exists to stop:

    CHECK 1  governed value domain  <->  carrier type, within the measured envelope.
             Stops a SUCCESSFULLY DELIVERED carrier that is not the governed thing.
    CHECK 2  carrier NULL  !=  analytical absence.
             Stops the carrier's "no value here" being read as a governed answer nobody gave.

SUCCESSFUL TRANSPORT DOES NOT ESTABLISH ADMISSIBILITY. The admission study's conclusion, inherited
verbatim, and the reason this module exists at all: every negative control below DELIVERS. None of
them raises on the way in. If admission defaults to accept, every one of them is served as if it
were governed law.
"""
from __future__ import annotations
from dataclasses import dataclass

import pyarrow as pa

from columna_core.governed.resolve import C6_SEMANTIC_VALUES, C9_EXCEPTIONAL, ESTABLISHED

from . import carrier as _carrier
from .refusals import WantOfLaw, WantOfState

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

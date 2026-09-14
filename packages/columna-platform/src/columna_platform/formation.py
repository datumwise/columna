"""FORMATION — constituting a constructed family's value from its operand's admitted material.

THE DISTINCTION THIS MODULE TURNS ON. A PRIMITIVE family's value is INTAKE: it is read from a source
and admitted. A CONSTRUCTED family's value is FORMED: it is computed from its operand's contributions
under a cited foundation law, and is never read from anywhere. So the material that crosses admission
on this path belongs to the OPERAND, is admitted as the operand's governed domain, and the
constructed value comes into existence after admission rather than through it. Nothing about the
constructed family is admitted, because nothing about it was delivered.

THE SEMANTICS COME FROM THE LAW, NOT FROM THE OPERATOR NAME (ruled Huayin, 2026-09-14). A
`FoundationLaw` carries `composition` — `"addition"` for SUM, `"minimum"` for MIN, `"maximum"` for
MAX — and that is the governed fact this profile folds by. The realization's `formation_operator` is
a CLAIM about which backend operator discharges the law, checked against the profile's own
declaration of what realizes what; it is never the source of the semantics. The string `"min"` in a
mapping decides nothing here, which is the point.

AND THE LAW IS WHY COUNT REFUSES WITHOUT ANYONE RULING ON COUNT. `LAWS["COUNT"].composition` is
`None` — a governed statement that COUNT does not compose over operand values, which is true and is
why its `result_domain` is `integer` rather than the operand's domain. A profile that forms by
composition therefore has nothing to fold with, and says so as a capability limit. That refusal is
reached WITHOUT touching the §11.5.1 target question (OF-44), and must not be mistaken for an answer
to it: COUNT is unformable here because this profile composes, not because its target is unsettled.

WHAT IS DEGENERATE HERE, STATED RATHER THAN HIDDEN. At COINCIDENT grain there is exactly one
contribution per analytical point, so a fold over each fiber returns that contribution and MIN equals
the value it selected from. The code below performs a real group-and-fold and does not special-case
the singleton — but a green test here is NOT evidence that non-trivial aggregation over several
contributions works, because no fiber in this slice has several. What it is evidence of is narrower
and was the point of the slice: the successor executes a constructed family from governed formation
law, rather than by special-casing primitives or reading an operator name.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Dict

import pyarrow as pa

from columna_core.governed.foundation import LAWS

from .carrier import AnchoredCarrier
from .refusals import UnsupportedByThisProfile, WantOfState

#: THE GOVERNED COMPOSITIONS THIS PROFILE REALIZES, keyed by the composition name the FoundationLaw
#: declares — never by law name and never by operator name. One entry, deliberately: this slice
#: implements MIN and nothing else, and a law whose composition is not here refuses rather than being
#: approximated by a neighbouring one.
_COMPOSITIONS: Dict[str, Callable] = {
    "minimum": min,
}

#: PROFILE FACT — which of this profile's operator names realizes a governed formation law. It
#: mirrors K0v2's `K0_LAWS` and exists for the same reason: the mapping CLAIMS an operator, the law
#: DECIDES, and the compiler/profile checks the claim against its own declaration. Deriving the
#: expected token from the law name by lowercasing would make the check a tautology over a string.
PLATFORM_LAWS: Dict[str, str] = {
    "MIN": "min",
}


@dataclass(frozen=True)
class Formed:
    """A constructed family's values, at the anchor points they were formed over."""

    table: pa.Table
    value_column: str
    anchor_columns: tuple
    law_name: str
    composition: str
    #: how many contributions each fiber carried — evidence, so a degenerate fold cannot be
    #: mistaken for a non-trivial one by anybody reading a passing test.
    fiber_sizes: tuple


def formation_law(law_view_value, subject: str):
    """The cited `FoundationLaw` for a constructed family, from C4's resolved value."""
    name = law_view_value.get("law_name")
    law = LAWS.get(name) if name else None
    if law is None:
        raise UnsupportedByThisProfile(
            f"the formation law {name!r} cited by {subject} is not in the foundation vocabulary this "
            f"profile reads")
    return law


def realized_operator(law_name: str, subject: str) -> str:
    """The operator token a realization must claim for this law, IN THIS PROFILE."""
    op = PLATFORM_LAWS.get(law_name)
    if op is None:
        raise UnsupportedByThisProfile(
            f"this profile realizes formation laws {sorted(PLATFORM_LAWS)} and {subject} cites "
            f"{law_name}; it is not a governed defect that the family exists, only that this build "
            f"does not form it")
    return op


def composition_for(law, subject: str) -> Callable:
    """The fold this profile applies for a law, from the law's DECLARED composition."""
    if law.composition is None:
        raise UnsupportedByThisProfile(
            f"foundation law {law.name} declares no composition over operand values — its result "
            f"domain is {law.result_domain!r}, not the operand's — so a profile that forms by "
            f"composition has nothing to fold with for {subject}. This is a limit of how this "
            f"profile forms, and is not a verdict about the law")
    fold = _COMPOSITIONS.get(law.composition)
    if fold is None:
        raise UnsupportedByThisProfile(
            f"foundation law {law.name} composes by {law.composition!r} and this profile realizes "
            f"{sorted(_COMPOSITIONS)}")
    return fold


def check_operator_claim(realization, law, subject: str) -> None:
    """The realization CLAIMS an operator; the law DECIDES. Refused BEFORE any arithmetic.

    A mapping that claims `max` for a family whose cited law is MIN is not describing a different
    backend — it is describing a different family, which is the succession-by-mapping the v2 format
    exists to make impossible. `UnsupportedByThisProfile` would be the wrong class here: nothing is
    unimplemented, the claim is simply false against governed law."""
    expected = realized_operator(law.name, subject)
    if realization.formation_operator is None:
        raise WantOfState(
            f"the realization for {subject} makes no delivery claim: a constructed family's "
            f"realization must name the operator it claims discharges the declared formation law",
            subject=subject)
    if realization.formation_operator != expected:
        raise WantOfState(
            f"the realization claims operator {realization.formation_operator!r} discharges "
            f"formation law {law.name}, and this profile realizes {law.name} as {expected!r}. "
            f"The law decides; the mapping claims; the profile checks",
            subject=subject)


def form(anchored: AnchoredCarrier, law, fold: Callable, *, value_column: str = "value") -> Formed:
    """Fold the operand's admitted contributions into one constituted value per analytical point.

    A REAL GROUP-AND-FOLD, not a singleton shortcut. The fibers happen to hold one contribution each
    at coincident grain, and the code neither knows nor relies on that — which is what makes the
    `fiber_sizes` evidence below meaningful rather than decorative.

    THE FOLD RUNS IN `Decimal`. The governed domain is exact decimal and the composition is applied
    to Python `Decimal` values, so no binary-floating-point step can enter between the admitted
    carrier and the constituted value. `min` over `Decimal` is exact by construction; it is stated
    here because the next composition added may not be."""
    table = anchored.table
    coords = list(anchored.anchor_columns)
    values = table.column(anchored.value_column).combine_chunks()
    value_type = values.type

    rows = table.to_pylist()
    fibers: Dict[tuple, list] = {}
    for row in rows:
        key = tuple(row[c] for c in coords)
        v = row[anchored.value_column]
        if not isinstance(v, Decimal):
            raise WantOfState(
                f"a contribution reached formation as {type(v).__name__}, not as the exact decimal "
                f"it was admitted as", subject=law.name)
        fibers.setdefault(key, []).append(v)

    keys = sorted(fibers)
    formed = [fold(fibers[k]) for k in keys]
    out = {c: pa.array([k[i] for k in keys], type=table.column(c).type)
           for i, c in enumerate(coords)}
    out[value_column] = pa.array(formed, type=value_type)
    return Formed(table=pa.table(out), value_column=value_column,
                  anchor_columns=tuple(coords), law_name=law.name,
                  composition=law.composition,
                  fiber_sizes=tuple(len(fibers[k]) for k in keys))

"""
columna_platform.kernel.builtins — **the smallest semantic law set the vertical proofs need, and the
in-memory provider profile that realizes it.**

Ruled (Huayin, 2026-09-28): *"implement the smallest semantic operator/law authority required by the
vertical proofs."* So this is seven laws, and every one of them is here because a proof needs it:

    SUM           REDUCER  scalar            continuation ADDITION, everywhere   proof 1
    COUNT         REDUCER  scalar            continuation ADDITION, everywhere   proof 3
    STOCK_LEVEL   REDUCER  scalar            continuation ADDITION, **restricted**  the edge-relative case
    HLL_SKETCH    REDUCER  structured        continuation SKETCH_UNION           proof 2, family half
    HLL_ESTIMATE  MAP      — (a constructor) no continuation                     proof 2, expression half
    MEAN          REDUCER  — (a constructor) no continuation                     proof 3
    LAST          ORDERED  ordered witness   continuation LATEST_BY_ORDER        proof 4

THREE THINGS THIS TABLE IS ARRANGED TO DEMONSTRATE
--------------------------------------------------
**1 · STRUCTURAL KIND IS ORTHOGONAL TO ANALYTICAL SORT**, and the table makes it visible rather than
asserted. `HLL_SKETCH` is a REDUCER and founds a family. `MEAN` is a REDUCER and cannot. `HLL_ESTIMATE`
is a MAP and cannot. `LAST` is ORDERED and does. Every combination that matters appears, so the
orthogonality is a property of the vocabulary and not of a comment.

**2 · CLOSURE IS EDGE-RELATIVE, AND `STOCK_LEVEL` IS WHY THE REGION EXISTS.** A level of on-hand stock
composes across stores at a fixed day and does **not** compose across time — summing a stock over days
is the textbook error, and no amount of caching an intermediate makes it lawful. `SUM` and `STOCK_LEVEL`
have the SAME composition (addition) and DIFFERENT regions, which is exactly the fact a global
`re_entrant` Boolean cannot carry and the reason the V8-1 reconnaissance said it had to be replaced.

**3 · A STRUCTURED FAMILY NAMES ITS OWN FINALIZATION, AND THE FINALIZATION IS AN EXPRESSION.**
`HLL_SKETCH.finalized_by == "HLL_ESTIMATE"`, and `HLL_ESTIMATE` has no continuation. So the sketch may
be merged forever and the estimate may never seed anything, and the pair says so in the vocabulary
before any engine runs.

WHAT WAS REUSED FROM THE OLD ESTATE, AND WHAT WAS NOT
-----------------------------------------------------
`datasketches` is used DIRECTLY — the Apache DataSketches HLL implementation, a third-party algorithm and
not part of any ontology. `columna_core.sketch` was read as reference and is **not imported**: it carries
`Witness` and `WitnessStore`, which are the old estate's retention doctrine, and this kernel has its own.
The `rse` formula and the `hll_sketch`/`hll_union`/`get_estimate` call shapes are the reuse; the doctrine
around them is not.
"""
from __future__ import annotations

import math
from typing import Any, Iterable, Mapping, Optional

from datasketches import hll_sketch, hll_union, tgt_hll_type

from .law import (
    ADDITION,
    AnalyticalLaw,
    Composition,
    ContinuationRegion,
    LATEST_BY_ORDER,
    LawRegistry,
    MAP,
    ORDERED,
    ORDERED_WITNESS,
    REDUCER,
    POPULATION,
    RequiredBasis,
    SCALAR,
    SKETCH_UNION,
    STRUCTURED,
)
from .realization import ProviderProfile, Realization

VOCABULARY, VERSION = "datumwise.platform.v8", "1"

_HLL_PRECISION = 12
_TGT = tgt_hll_type.HLL_8


def hll_rse(precision: int = _HLL_PRECISION) -> float:
    """HLL relative standard error at `lg_k = precision`. Lifted formula, not lifted doctrine."""
    return 1.04 / math.sqrt(2 ** precision)


# ── compositions ─────────────────────────────────────────────────────────────────────────────────
_ADDITIVE = Composition(
    token=ADDITION, associative=True, commutative=True, has_identity=True,
    note="a commutative monoid under addition with identity 0, so an empty eligible fibre lawfully "
         "folds to 0 — a governed value, not an absence")
_SKETCH = Composition(
    token=SKETCH_UNION, associative=True, commutative=True, has_identity=True,
    note="set union on the sketch's registers: idempotent, associative, commutative, with the empty "
         "sketch as identity. This is what makes a distinct count continuation-bearing AT ALL — the "
         "displayed integer is not, and the sketch is")
_LATEST = Composition(
    token=LATEST_BY_ORDER, associative=True, commutative=True, has_identity=False,
    note="selection of the witness maximal in the governed order. Associative and commutative because "
         "the order is total; NO identity, because there is no witness that loses to every witness — "
         "so an empty eligible fibre receives no value from the algebra alone, and saying so is the "
         "answer rather than a gap")


# ══ the semantic authority ════════════════════════════════════════════════════════════════════════
LAWS: tuple[AnalyticalLaw, ...] = (
    AnalyticalLaw(
        name="SUM", kind=REDUCER,
        target_form="the additive total of the participating contributions",
        operand_domains=frozenset({"integer", "decimal"}), result_domain="same_as_operand",
        value_form=SCALAR,
        sufficient_state="the running total IS the finite witness; nothing further is retained",
        continuation=_ADDITIVE, region=ContinuationRegion.everywhere(
            "a flow composes over every coarsening: contributions are disjoint at the root and stay "
            "disjoint under any forgetting"),
        identity_note="additive monoid; empty folds to 0"),
    AnalyticalLaw(
        name="COUNT", kind=REDUCER,
        target_form="the number of participating contributions",
        operand_domains=frozenset({"integer", "decimal", "text", "boolean", "date", "timestamp"}),
        result_domain="integer", value_form=SCALAR,
        sufficient_state="the running count IS the finite witness",
        # **THE ONLY POPULATION LAW IN THIS VOCABULARY, AND IT SAYS SO ITSELF** (B-0b). A count contributes
        # over PARTICIPATION and reads no value, so a participating point whose value is unestablished does
        # not block its fold — which is exactly why `OrderCount` serves 3 at D1 in the exhibit where
        # `Revenue` wants state over the same seven orders. This was `_POPULATION_LAWS = {"COUNT"}` in the
        # columnar MME; it is a fact about the law and now lives on the law.
        fold_shape=POPULATION,
        continuation=_ADDITIVE, region=ContinuationRegion.everywhere(
            "counts of disjoint contributions add over every coarsening"),
        identity_note="additive monoid; empty folds to 0"),
    AnalyticalLaw(
        name="STOCK_LEVEL", kind=REDUCER,
        target_form="the level of a stock held at a location, at an instant",
        operand_domains=frozenset({"integer", "decimal"}), result_domain="same_as_operand",
        value_form=SCALAR,
        sufficient_state="the level IS the witness, and it is a witness OF AN INSTANT — which is why "
                         "the closure below is restricted rather than the level being unmergeable",
        continuation=_ADDITIVE,
        region=ContinuationRegion.forgetting_only(
            {"store"},
            "a stock level composes ACROSS STORES at one instant and does NOT compose ACROSS TIME: "
            "summing a level over days adds a quantity to itself. The composition is the same addition "
            "SUM uses; what differs is the set of edges it holds over"),
        identity_note="additive monoid over the admitted edges only"),
    AnalyticalLaw(
        name="HLL_SKETCH", kind=REDUCER,
        target_form="an HLL sketch of the distinct participating values",
        operand_domains=frozenset({"integer", "text"}), result_domain="sketch",
        value_form=STRUCTURED,
        sufficient_state="the SKETCH is the sufficient state. The displayed distinct count is not: a "
                         "scalar cardinality cannot be merged, and two estimates do not give the "
                         "estimate at a coarser anchor",
        continuation=_SKETCH, region=ContinuationRegion.everywhere(
            "sketch union is total over coarsenings, and idempotent, so overlapping contributions "
            "are handled by the algebra rather than by a disjointness precondition"),
        approximation="approximate",
        finalized_by="HLL_ESTIMATE",
        identity_note="union monoid with the empty sketch as identity"),
    AnalyticalLaw(
        name="HLL_ESTIMATE", kind=MAP,
        target_form="the cardinality estimate carried by an HLL sketch",
        operand_domains=frozenset({"sketch"}), result_domain="integer", value_form=SCALAR,
        sufficient_state="none of its own: it is determined by the sketch family's state at the same "
                         "location, and by nothing it retains itself",
        continuation=None,
        approximation="approximate",
        required_basis=RequiredBasis(
            components=("HLL_SKETCH",), requires_common_participation=True,
            note="the estimate is established by the sketch family's state at the same location; there "
                 "is no second component and no participation to reconcile ACROSS components, but the "
                 "requirement is carried so that the one component's instance is still checked"),
        identity_note="does not compose: a mean of estimates is not an estimate, and a sum of them is "
                      "not a cardinality"),
    AnalyticalLaw(
        name="MEAN", kind=REDUCER,
        target_form="the arithmetic mean over the participating contributions",
        operand_domains=frozenset({"integer", "decimal"}), result_domain="decimal", value_form=SCALAR,
        sufficient_state="no finite witness is carried by the displayed value; its exact finite basis "
                         "is a matching SUM and COUNT over the same participating contributions",
        continuation=None,
        required_basis=RequiredBasis(
            components=("COUNT", "SUM"), requires_common_participation=True,
            note="the exact finite basis is a matching SUM and COUNT with the SAME participating "
                 "contributions in both components"),
        identity_note="does not compose; a mean of means is not a mean"),
    AnalyticalLaw(
        name="LAST", kind=ORDERED,
        target_form="the value of the participating contribution maximal in the governed order",
        operand_domains=frozenset({"integer", "decimal", "text"}), result_domain="same_as_operand",
        value_form=ORDERED_WITNESS,
        sufficient_state="the witness AND its order key. The value alone is not sufficient: without the "
                         "key two witnesses cannot be compared, so a continuation could not select",
        continuation=_LATEST, region=ContinuationRegion.everywhere(
            "selection by a total order composes over every coarsening"),
        requires_order=True,
        identity_note="commutative semigroup with NO identity: an empty eligible fibre receives no "
                      "witness from the algebra alone, and that KNOWN-EMPTY standing is a governed "
                      "answer distinct from 'unknown'"),
)

REGISTRY = LawRegistry(LAWS, vocabulary=VOCABULARY, version=VERSION)


# ══ the in-memory provider profile ════════════════════════════════════════════════════════════════
def _sum_contribute(values: Iterable[Any], params: Mapping[str, Any]):
    return sum(v for v in values if v is not None)


def _count_contribute(values: Iterable[Any], params: Mapping[str, Any]):
    return sum(1 for v in values if v is not None)


def _sketch_contribute(values: Iterable[Any], params: Mapping[str, Any]):
    precision = int(params.get("precision", _HLL_PRECISION))
    s = hll_sketch(precision, _TGT)
    for v in values:
        if v is not None:
            s.update(v)
    return s


def _sketch_merge(a, b):
    u = hll_union(_HLL_PRECISION)
    u.update(a)
    u.update(b)
    return u.get_result()


def _sketch_identity():
    return hll_sketch(_HLL_PRECISION, _TGT)


#: **KNOWN-EMPTY, AS AN OBJECT.** `LAST` has no identity, so an empty eligible fibre receives no witness
#: from the algebra. That is a governed answer — *there was nothing to select* — and it is distinct from
#: *we do not know*. A `None` payload could not carry the difference, so the standing gets a value.
class KnownEmptyWitness:
    """The witness standing of an eligible fibre with no contribution. Loses every comparison."""

    __slots__ = ()

    def __repr__(self) -> str:                              # pragma: no cover - diagnostics
        return "KNOWN_EMPTY"

    def __eq__(self, other) -> bool:
        return isinstance(other, KnownEmptyWitness)

    def __hash__(self) -> int:
        return hash("KNOWN_EMPTY")


KNOWN_EMPTY = KnownEmptyWitness()


def _last_contribute(values: Iterable[Any], params: Mapping[str, Any]):
    """The ORDERED case: a witness is `(order_key, value)`, and the key is part of the state."""
    order_by = params.get("order_by")
    value_key = params.get("value_key", "value")
    rows = params.get("rows") or ()
    if order_by is None:                                    # pragma: no cover - refused at bind
        raise ValueError("LAST requires a governed order")
    witnesses = [(r[order_by], r.get(value_key)) for r in rows if r.get(value_key) is not None]
    if not witnesses:
        return KNOWN_EMPTY
    return max(witnesses, key=lambda w: w[0])


def _last_merge(a, b):
    if isinstance(a, KnownEmptyWitness):
        return b
    if isinstance(b, KnownEmptyWitness):
        return a
    return a if a[0] >= b[0] else b


def _estimate_apply(payloads: Mapping[str, Any], params: Mapping[str, Any]):
    sketch = payloads["HLL_SKETCH"]
    return int(round(sketch.get_estimate()))


def _mean_apply(payloads: Mapping[str, Any], params: Mapping[str, Any]):
    """**§4.3's undefined case is a `None`, and the engine turns it into a governed standing.**

    The basis IS established at `n = 0` — it is `(0, 0)` — and the expression is *undefined on that
    basis*. Returning 0 would be a value the theory does not license, and raising would make a governed
    answer look like a defect."""
    total, n = payloads["SUM"], payloads["COUNT"]
    if not n:
        return None
    return total / n


IN_MEMORY = ProviderProfile("in-memory", (
    Realization(law="SUM", contribute=_sum_contribute, merge=lambda a, b: a + b,
                identity=lambda: 0, note="scalar addition"),
    Realization(law="COUNT", contribute=_count_contribute, merge=lambda a, b: a + b,
                identity=lambda: 0),
    Realization(law="STOCK_LEVEL", contribute=_sum_contribute, merge=lambda a, b: a + b,
                identity=lambda: 0,
                note="the SAME executable composition as SUM. The difference between the two laws is "
                     "SEMANTIC and lives in the region, which is why it cannot live here"),
    Realization(law="HLL_SKETCH", contribute=_sketch_contribute, merge=_sketch_merge,
                identity=_sketch_identity, note="Apache DataSketches HLL_8"),
    Realization(law="HLL_ESTIMATE", apply=_estimate_apply,
                note="finalization ONLY. No merge, because there is nothing lawful for one to do"),
    Realization(law="MEAN", apply=_mean_apply),
    Realization(law="LAST", contribute=_last_contribute, merge=_last_merge,
                note="no identity: KNOWN_EMPTY is a standing, not a monoid unit"),
))

#: A profile that realizes the family laws and **not** `MEAN`, so that "a backend's inability does not
#: remove a law" (ToD v8 §4.1) is a testable state of this kernel rather than a sentence in a docstring.
NO_MEAN = ProviderProfile("no-mean", tuple(
    r for r in (IN_MEMORY.of(name) for name in IN_MEMORY.laws) if r.law != "MEAN"))


def witness_value(payload: Any) -> Optional[Any]:
    """The displayed half of an ordered witness, or `None` where the fibre is KNOWN-EMPTY."""
    if isinstance(payload, KnownEmptyWitness):
        return None
    return payload[1]


__all__ = ["IN_MEMORY", "KNOWN_EMPTY", "KnownEmptyWitness", "LAWS", "NO_MEAN", "REGISTRY", "VERSION",
           "VOCABULARY", "hll_rse", "witness_value"]

"""
columna_platform.kernel — **the v8-native Platform kernel.**

Ruled (Huayin, 2026-09-28): *"The priority is a running Columna Platform MME, not migrating Columna Core
to v8 one semantic unit at a time… Platform is the architectural destination. Core will later be a
bounded profile extracted from / enabled by Platform."*

So this package is a PARALLEL implementation built from the ToD v8 objects directly. It does not depend
semantically on `columna_core.governed.Family`, Core `LawView`/C1–C9, Core native publication v3.0/v3.1,
Core generated-family doctrine, Core `operators.py` classifications, or any Core backward-compatibility
requirement — **and it imports none of them.** A test pins the absence, because a boundary nobody
measures is a boundary that leaks.

    geometry      the governed universe, the anchor as a CONSTITUENT SET, and the EDGE as an object
    law           the reusable semantic operator/law authority. Semantic content only
    realization   the physical provider profile. The other half of the split
    standing      analytical instance, compatibility, refusal, disclosure
    sorts         the TWO durable analytical sorts and their identities: `F@A` and `E@A`
    value         continuation-bearing `FamilyState` vs finalized `ExpressionOutput` — two TYPES
    mme           the engine: retain, adjudicate, measure, evaluate
    builtins      the smallest law vocabulary the vertical proofs need, and its in-memory provider
    exhibit       the runnable demonstration

    THE RULE      physical availability is not analytical authority.
"""
from __future__ import annotations

from .builtins import IN_MEMORY, KNOWN_EMPTY, LAWS, NO_MEAN, REGISTRY, hll_rse, witness_value
from .geometry import Anchor, Constituent, Edge, KernelRefusal, Universe
from .law import (
    ADDITION,
    LATEST_BY_ORDER,
    MAXIMUM,
    MINIMUM,
    SKETCH_UNION,
    AnalyticalLaw,
    Composition,
    ContinuationRegion,
    LawRegistry,
    MAP,
    ORDERED,
    ORDERED_WITNESS,
    REDUCER,
    RequiredBasis,
    SCALAR,
    STRUCTURED,
)
from .mme import MME, Adequacy, Retained, RetentionKey
from .realization import ProviderProfile, Realization
from .sorts import (
    ExpressionPoint,
    FamilyPoint,
    GovernedExpression,
    MeasureFamily,
    Operand,
    SufficientBasis,
)
from .standing import (
    CACHED,
    CONTINUED,
    EVALUATED,
    REFUSED,
    ROOT,
    AnalyticalInstance,
    Compatibility,
    Disclosure,
    Refusal,
)
from .value import Answer, ExpressionOutput, FamilyState

__all__ = [
    "Anchor", "Constituent", "Edge", "KernelRefusal", "Universe",
    "AnalyticalLaw", "Composition", "ContinuationRegion", "LawRegistry", "RequiredBasis",
    "MAP", "REDUCER", "ORDERED", "SCALAR", "STRUCTURED", "ORDERED_WITNESS",
    "ADDITION", "SKETCH_UNION", "LATEST_BY_ORDER", "MINIMUM", "MAXIMUM",
    "ProviderProfile", "Realization",
    "AnalyticalInstance", "Compatibility", "Disclosure", "Refusal",
    "ROOT", "CONTINUED", "CACHED", "EVALUATED", "REFUSED",
    "FamilyPoint", "ExpressionPoint", "MeasureFamily", "GovernedExpression", "Operand",
    "SufficientBasis",
    "Answer", "FamilyState", "ExpressionOutput",
    "MME", "Adequacy", "Retained", "RetentionKey",
    "LAWS", "REGISTRY", "IN_MEMORY", "NO_MEAN", "KNOWN_EMPTY", "hll_rse", "witness_value",
]

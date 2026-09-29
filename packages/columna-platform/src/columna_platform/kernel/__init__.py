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
    realization   the physical provider profile, and `RealizationStanding` — which provider/carrier
    standing      analytical instance (incl. the `data_state` axis), compatibility, refusal, disclosure
    witness       the `ConstitutionWitness`, COMPUTED from identity-bearing governed facts
    sorts         the TWO durable analytical sorts and their identities: `F@A` and `E@A`
    value         continuation-bearing `FamilyState` vs finalized `ExpressionOutput` — two TYPES
    materialization  MME v1's governed family-materialization cache: opaque identity, dependency,
                     currentness, residency, admission
    mme           the engine: admit, select candidates, adjudicate, measure. **FAMILIES ONLY** (M-2)
    expression    the expression evaluator, ABOVE the MME: consumes family state, evaluates `E@A`
    observation   the family-request observation seam — READY/NEED/WANT_OF_STATE/UNSUPPORTED, append-only,
                  non-authoritative, and unable to fail a request
    builtins      the smallest law vocabulary the vertical proofs need, and its in-memory provider
    exhibit       the runnable demonstration

    THE RULE      physical availability is not analytical authority.

THREE FACTS ABOUT A RETAINED OBJECT, AND THEY ARE THREE
-------------------------------------------------------
Ruled (Huayin, 2026-09-29, P-1): *"Keep these three things distinct… Do not collapse them into one
version/freshness token."*

    which CONSTITUTION   `witness.py`       `ConstitutionWitness` — computed from the declaration
    which EVIDENCE       `standing.py`      `AnalyticalInstance.data_state` — which root state
    which REALIZATION    `realization.py`   `RealizationStanding` — which provider/carrier

`RetentionKey` references all three, and referencing is not collapsing: "the declaration moved", "the data
was reloaded" and "the provider changed" are three separately computed, separately reportable answers, and
`stale_states()` names which governed determinant moved rather than reporting an undifferentiated staleness.
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
from .materialization import (
    AT_ROOT,
    COEXIST,
    CURRENT,
    EVICTABLE,
    EVICTED,
    EXPIRED,
    INDEPENDENT,
    PINNED,
    REJECT,
    RESIDENT,
    SUPERSEDE,
    SUPERSEDED,
    Admission,
    Establishment,
    FamilyMaterialization,
    ManifoldBuild,
    MaterializationId,
    MaterializationStore,
    Slot,
    TransitionIntent,
    admitted_targets,
    cumulative_forgotten,
    entitlement_holds,
)
from .expression import ExpressionEvaluator
from .mme import MME, Adequacy, Retained, RetentionKey, Staleness
from .observation import (
    DISPOSITIONS,
    NEED,
    READY,
    UNSUPPORTED,
    WANT_OF_STATE,
    FamilyRequest,
    Fulfillment,
    NullObserver,
    ObservationSink,
    RecordingObserver,
    RequestObservation,
    WorkloadObserver,
    disposition_for,
)
from .realization import ProviderProfile, Realization, RealizationStanding
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
    CONSTITUTION_CONTEXT_UNSTATED,
    CONTINUED,
    EVALUATED,
    REFUSED,
    ROOT,
    UNSTATED_DATA_STATE,
    AnalyticalInstance,
    Compatibility,
    Disclosure,
    Refusal,
)
from .value import Answer, ExpressionOutput, FamilyState
from .witness import (
    ConstitutionWitness,
    EXPRESSION_NON_DETERMINANTS,
    FAMILY_NON_DETERMINANTS,
    WITNESS_SCHEME,
    WitnessComparison,
    determinant_names,
    expression_witness,
    family_witness,
)

__all__ = [
    "Anchor", "Constituent", "Edge", "KernelRefusal", "Universe",
    "AnalyticalLaw", "Composition", "ContinuationRegion", "LawRegistry", "RequiredBasis",
    "MAP", "REDUCER", "ORDERED", "SCALAR", "STRUCTURED", "ORDERED_WITNESS",
    "ADDITION", "SKETCH_UNION", "LATEST_BY_ORDER", "MINIMUM", "MAXIMUM",
    "ProviderProfile", "Realization", "RealizationStanding",
    "AnalyticalInstance", "Compatibility", "Disclosure", "Refusal",
    "UNSTATED_DATA_STATE", "CONSTITUTION_CONTEXT_UNSTATED",
    "ROOT", "CONTINUED", "CACHED", "EVALUATED", "REFUSED",
    "FamilyPoint", "ExpressionPoint", "MeasureFamily", "GovernedExpression", "Operand",
    "SufficientBasis",
    "Answer", "FamilyState", "ExpressionOutput",
    "MME", "Adequacy", "Retained", "RetentionKey", "Staleness", "ExpressionEvaluator",
    "DISPOSITIONS", "NEED", "READY", "UNSUPPORTED", "WANT_OF_STATE", "FamilyRequest",
    "Fulfillment", "NullObserver", "ObservationSink", "RecordingObserver",
    "RequestObservation", "WorkloadObserver", "disposition_for",
    "FamilyMaterialization", "MaterializationId", "MaterializationStore", "ManifoldBuild",
    "Establishment", "TransitionIntent", "Admission", "Slot", "CURRENT", "SUPERSEDED", "PINNED",
    "RESIDENT", "EVICTABLE", "EVICTED", "EXPIRED", "AT_ROOT", "INDEPENDENT", "COEXIST", "SUPERSEDE",
    "REJECT", "admitted_targets", "cumulative_forgotten", "entitlement_holds",
    "ConstitutionWitness", "WitnessComparison", "WITNESS_SCHEME", "family_witness",
    "expression_witness", "determinant_names", "FAMILY_NON_DETERMINANTS",
    "EXPRESSION_NON_DETERMINANTS",
    "LAWS", "REGISTRY", "IN_MEMORY", "NO_MEAN", "KNOWN_EMPTY", "hll_rse", "witness_value",
]

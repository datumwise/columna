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
    authorization **who decides that a family continuation MAY be done** — `ContinuationAuthority`,
                  `AuthorizedFamilyContinuation`, `AuthorizedStanding`. The constitution is read HERE and
                  nowhere below (B-0b)
    mme           the engine: admit, select candidates, adjudicate, measure. **FAMILIES ONLY** (M-2)
    expression    the expression evaluator, ABOVE the MME: consumes family state, evaluates `E@A`
    observation   the family-request observation seam — READY/NEED/WANT_OF_STATE/UNSUPPORTED, append-only,
                  non-authoritative, and unable to fail a request
    requirement   **what governed family state is NEEDED** — the MME's half of the realization seam.
                  An analytical requirement, never a fetch plan
    fulfillment   **the Fulfillment Coordinator** — combines MME + Realization + evaluator. Orchestration
                  only: no analytical authority, no execution semantics, no economic policy
    realization_manager
                  **what the physical estate can SUPPLY** — capability (`propose`) and execution
                  (`realize`) kept apart, and one door into the cache, which since B-1' is reachable only
                  through fidelity adjudication. R-1: interface only
    realization_fidelity
                  **does this physical result faithfully realize the object it CLAIMS to be?** —
                  `RealizationAuthority`, `AdjudicatedRealization`. A result does not become a governed
                  object by being produced, labelled, or offered (B-1')
    builtins      the smallest law vocabulary the vertical proofs need, and its in-memory provider
    exhibit       the runnable demonstration

    THE RULE      physical availability is not analytical authority.

FIVE QUESTIONS, FIVE OWNERS, AND THEY ARE FIVE
----------------------------------------------
Ruled (Huayin, 2026-09-30), and this is the whole serving ladder in the order it is descended:

    analytical authorization    what may be requested                      `authorization.ContinuationAuthority`
            |
    physical realization        what the estate actually produced          `realization_manager` + provider
            |
    realization fidelity        is that result really the claimed `F@A`?   `realization_fidelity.RealizationAuthority`
            |
    MME admission               may this enter this cache/build?           `MME.put` — the cache door
            |
    MME fulfillment             can held state answer the request?         `MME.fulfill` / `MME.adjudicate`

**EACH QUESTION IS ASKED ONCE, BY ONE OWNER, AND NO LOWER LAYER RE-ASKS A HIGHER ONE.** That is the
invariant the B-0a/B-0b/B-1' sequence bought, and it is testable rather than aspirational: no constitutional
vocabulary appears below layer 1, fidelity does not restate a standing refusal, and build/witness coherence
is REQUIRED by layer 3 and COMPARED by layer 4 — carried down, not asked twice.

The ladder is descended, not climbed: layer 3 succeeding licenses admission of one value and says nothing
about what may be CONTINUED from it, which is layer 1's question about a different request.

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

from .authorization import (
    EXECUTION_MODES,
    GROUPED_MODE,
    SCAN_MODE,
    Authorization,
    AuthorizedFamilyContinuation,
    AuthorizedStanding,
    ContinuationAuthority,
    FoldRequirement,
)
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
    FOLD_SHAPES,
    POPULATION,
    SCALAR,
    STRUCTURED,
    VALUE_BEARING,
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
from .fulfillment import (
    INCOMPLETE,
    MOODS,
    NOT_SUPPORTED,
    ROUTE_POLICY_NEEDED,
    SERVED,
    UNAVAILABLE,
    UNRESOLVED_STATE,
    FulfillmentCoordinator,
    FulfillmentOutcome,
    RealizedRoute,
    RouteContext,
    RouteDecision,
    RoutePolicy,
    UnambiguousRoute,
)
from .mme import MME, Adequacy, Retained, RetentionKey
from .observation import (
    DISPOSITIONS,
    PROCESS_CONTROL,
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
from .realization_fidelity import (
    AdjudicatedRealization,
    Adjudication,
    RealizationAuthority,
)
from .realization import ProviderProfile, Realization, RealizationStanding
from .realization_manager import (
    ProposalSet,
    RealizationManager,
    RealizationOffer,
    RealizationProposal,
    RealizationProvider,
    requirement_from,
)
from .requirement import FamilyRequirement, RequirementOutcome, acceptable_anchors
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
    "RealizationAuthority",
    "Adjudication",
    "AdjudicatedRealization",
    "FOLD_SHAPES",
    "VALUE_BEARING",
    "POPULATION",
    "FoldRequirement",
    "ContinuationAuthority",
    "AuthorizedStanding",
    "AuthorizedFamilyContinuation",
    "Authorization",
    "SCAN_MODE",
    "GROUPED_MODE",
    "EXECUTION_MODES",
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
    "MME", "Adequacy", "Retained", "RetentionKey", "ExpressionEvaluator",
    "DISPOSITIONS", "NEED", "READY", "UNSUPPORTED", "WANT_OF_STATE", "FamilyRequest",
    "Fulfillment", "NullObserver", "ObservationSink", "RecordingObserver", "PROCESS_CONTROL",
    "FamilyRequirement", "RequirementOutcome", "acceptable_anchors", "ProposalSet",
    "RealizationManager", "RealizationOffer", "RealizationProposal", "RealizationProvider",
    "requirement_from", "FulfillmentCoordinator", "FulfillmentOutcome", "RoutePolicy",
    "RouteDecision", "RouteContext", "UnambiguousRoute", "RealizedRoute", "MOODS", "SERVED",
    "UNAVAILABLE", "ROUTE_POLICY_NEEDED", "UNRESOLVED_STATE", "NOT_SUPPORTED", "INCOMPLETE",
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

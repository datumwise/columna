"""
columna_core.compiler — the Core-P1 compiler (K0).

    compile_k0(governed_publication, private_core_mapping) -> CLOSED Core execution image

A DISTINCT Core-P1 compiler module inside the existing `columna-core` distribution (ruled
2026-08-22). It is deliberately NOT `draft.lower_to_cml`, which is a Core-local bootstrap from the
init interview that reads neither a publication nor a mapping, and it is deliberately not a new
distribution, which would buy release-set surface — its own Trusted Publisher registration, its own
lockstep decision, its own dependency caps — for nothing.

`columna-server` must never import this module: the runtime verifies a receipt WITHOUT loading the
private mapping, reconstructing meaning from the `.cml`, or re-running lowering.

**TWO COMPILE BOUNDARIES LIVE HERE, AND ONLY ONE IS CURRENT.** `compile_v2` builds the Core family
from ESTABLISHED GOVERNED LAW and checks the private mapping against it. `compile_k0` is the FROZEN
v1 producer — read its tombstone before touching it. Publication v2 is a hard break: the v2 reader
refuses a v1 artifact outright, and nothing here reads one on its behalf.
"""
from __future__ import annotations

from .compile import ClosedExecutionImage, K0_REDUCERS, compile_k0
from .compile_v2 import K0_EMITS_MOVEMENT, K0_LAWS, compile_v2
from .realization import (
    MAPPING_FORMAT_VERSION as MAPPING_FORMAT_VERSION_V2,
    PrivateCoreMappingV2,
    load_mapping as load_mapping_v2,
    parse_mapping as parse_mapping_v2,
)
from .inputs import (
    MAPPING_FORMAT_VERSION,
    GovernedPublication,
    PrivateCoreMapping,
    PublicationRef,
    load_mapping,
    load_publication,
    parse_mapping,
    parse_publication,
)
from .receipt import RECEIPT_FILENAME, RECEIPT_FORMAT_VERSION, build_receipt, render_receipt
from .refusals import (
    CATEGORIES,
    CompileRefusal,
    ExecutionRepresentationGap,
    InputIdentityMismatch,
    LogicalMeaningMissing,
    MappingIncomplete,
    UnsupportedCoreCapability,
)

__all__ = [
    "compile_v2", "K0_LAWS", "K0_EMITS_MOVEMENT",
    "PrivateCoreMappingV2", "parse_mapping_v2", "load_mapping_v2", "MAPPING_FORMAT_VERSION_V2",
    "compile_k0", "ClosedExecutionImage", "K0_REDUCERS",
    "GovernedPublication", "PrivateCoreMapping", "PublicationRef",
    "parse_publication", "parse_mapping", "load_publication", "load_mapping",
    "MAPPING_FORMAT_VERSION",
    "build_receipt", "render_receipt", "RECEIPT_FORMAT_VERSION", "RECEIPT_FILENAME",
    "CompileRefusal", "InputIdentityMismatch", "LogicalMeaningMissing", "MappingIncomplete",
    "UnsupportedCoreCapability", "ExecutionRepresentationGap", "CATEGORIES",
]

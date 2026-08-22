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
"""
from __future__ import annotations

from .compile import ClosedExecutionImage, K0_REDUCERS, compile_k0
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
    "compile_k0", "ClosedExecutionImage", "K0_REDUCERS",
    "GovernedPublication", "PrivateCoreMapping", "PublicationRef",
    "parse_publication", "parse_mapping", "load_publication", "load_mapping",
    "MAPPING_FORMAT_VERSION",
    "build_receipt", "render_receipt", "RECEIPT_FORMAT_VERSION", "RECEIPT_FILENAME",
    "CompileRefusal", "InputIdentityMismatch", "LogicalMeaningMissing", "MappingIncomplete",
    "UnsupportedCoreCapability", "ExecutionRepresentationGap", "CATEGORIES",
]

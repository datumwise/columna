"""Columna Core — the column-foundation analytic framework (multi-table, transport-based)."""
from .model import (Manifold, Universe, Predicate, Ref, Comparison, DimensionLevel, FunctionalEdge,
                    MeasureColumn, FamilyMember, BAnchor, DerivedColumn, License, Assert, Hierarchy,
                    VERIFIED, CORROBORATED, UNTESTABLE, CONTRADICTED,
                    ADDITIVE, SKETCH, HOLISTIC, DECLARED, PROVEN, INFERRED_SAMPLE, INFERRED_DOCS, A)
from .operators import (Operator, REGISTRY, get_operator, signature_ok, output_dtype,
                        VALUE, ORDERED_W as ORDERED, REDUCER, SCAN, MAP, kind_of, reducers)
from . import types as dtypes
from .projection import PlannerView, MeasureShape, UniverseShape, DerivedShape, ShapeEdge, OperatorSig
from .connector import Connector, DuckDBConnector
from .engine import ColumnEngine
from .planner import Planner, FrameResult
from .frameql import ManifoldServer, Frame, parse_frameql, FrameQLSyntaxError
from .disclosure import Disclosure, Caveat, Refusal, Outcome
from .adjudication import (adjudicate, Contradiction, AssertContradiction, HierarchyContradiction,
                           AssertNotWellFormed, PublishedScope, scope_from_report, scope_diff)
from .draft import (Draft, Proposal, PolarityViolation, lower_proposal, DECLARATION_KINDS,
                    INFERRED_CATALOG, INFERRED_SAMPLE, DECLARED,
                    PROPOSED, ACCEPTED, STRUCK, EDITED,
                    SCOPED, PROPOSED_STATE, DECLARED_STATE, ATTESTED, PUBLISHED)
from .connector import CatalogAperture, APERTURE_SAMPLE_CAP
from .describe import describe_derived, license_to_dict
from .sketch import (hll_count, hll_merge, hll_estimate, hll_merge_pair, rse, Witness, WitnessStore)

__all__ = ["Manifold", "Universe", "Predicate", "Ref", "Comparison",
           "DimensionLevel", "FunctionalEdge", "MeasureColumn",
           "FamilyMember", "BAnchor", "DerivedColumn", "License", "Assert", "Hierarchy",
           "VERIFIED", "CORROBORATED", "UNTESTABLE", "CONTRADICTED", "ADDITIVE", "SKETCH", "HOLISTIC",
           "DECLARED", "PROVEN", "INFERRED_SAMPLE", "INFERRED_DOCS", "A",
           "Operator", "REGISTRY", "get_operator", "signature_ok", "output_dtype", "VALUE", "ORDERED", "REDUCER", "SCAN", "MAP", "kind_of", "reducers",
           "dtypes", "PlannerView", "MeasureShape", "UniverseShape", "DerivedShape", "ShapeEdge", "OperatorSig",
           "Connector", "DuckDBConnector", "ColumnEngine", "Planner", "FrameResult",
           "ManifoldServer", "Frame", "parse_frameql", "FrameQLSyntaxError",
           "Disclosure", "Caveat", "Refusal", "Outcome",
           "adjudicate", "Contradiction", "AssertContradiction", "HierarchyContradiction",
           "AssertNotWellFormed", "PublishedScope", "scope_from_report", "scope_diff",
           "describe_derived", "license_to_dict",
           "hll_count", "hll_merge", "hll_estimate", "hll_merge_pair", "rse", "Witness", "WitnessStore"]
__version__ = "0.7.8-core"

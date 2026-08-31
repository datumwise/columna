"""Columna Core — the column-foundation analytic framework (multi-table, transport-based)."""
from .model import (Manifold, Universe, Predicate, Ref, Comparison, DimensionLevel, FunctionalEdge,
                    MeasureColumn, FamilyMember, BAnchor, DerivedColumn, License, Hierarchy,
                    Relate, Face, TOUCH, ASSIGN, ALLOC, FACE_SCHEMES,
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
from .adjudication import (adjudicate, Contradiction, HierarchyContradiction,
                           PublishedScope, scope_from_report, scope_diff)
from .draft import (Draft, Proposal, PolarityViolation, lower_proposal, DECLARATION_KINDS,
                    INFERRED_CATALOG,          # INFERRED_SAMPLE/DECLARED already bound from .model (same constants)
                    PROPOSED, ACCEPTED, STRUCK, EDITED,
                    SCOPED, PROPOSED_STATE, DECLARED_STATE, ATTESTED, PUBLISHED)
from .connector import CatalogAperture, APERTURE_SAMPLE_CAP
from .describe import (describe_derived, license_to_dict, describe_universe,
                       describe_hierarchy, operator_properties, absence_semantics)
from .sketch import (hll_count, hll_merge, hll_estimate, hll_merge_pair, rse, Witness, WitnessStore)
from .documents import (logical_spec, physical_map, physical_vocabulary, no_physical_leak,
                        render_predicate_logical)

__all__ = ["Manifold", "Universe", "Predicate", "Ref", "Comparison",
           "DimensionLevel", "FunctionalEdge", "MeasureColumn",
           "FamilyMember", "BAnchor", "DerivedColumn", "License", "Hierarchy",
           "Relate", "Face", "TOUCH", "ASSIGN", "ALLOC", "FACE_SCHEMES",
           "VERIFIED", "CORROBORATED", "UNTESTABLE", "CONTRADICTED", "ADDITIVE", "SKETCH", "HOLISTIC",
           "DECLARED", "PROVEN", "INFERRED_SAMPLE", "INFERRED_DOCS", "A",
           "Operator", "REGISTRY", "get_operator", "signature_ok", "output_dtype", "VALUE", "ORDERED", "REDUCER", "SCAN", "MAP", "kind_of", "reducers",
           "dtypes", "PlannerView", "MeasureShape", "UniverseShape", "DerivedShape", "ShapeEdge", "OperatorSig",
           "Connector", "DuckDBConnector", "ColumnEngine", "Planner", "FrameResult",
           "ManifoldServer", "Frame", "parse_frameql", "FrameQLSyntaxError",
           "Disclosure", "Caveat", "Refusal", "Outcome",
           "adjudicate", "Contradiction", "HierarchyContradiction",
           "PublishedScope", "scope_from_report", "scope_diff",
           "describe_derived", "license_to_dict", "describe_universe",
           "describe_hierarchy", "operator_properties", "absence_semantics",
           "hll_count", "hll_merge", "hll_estimate", "hll_merge_pair", "rse", "Witness", "WitnessStore",
           "logical_spec", "physical_map", "physical_vocabulary", "no_physical_leak",
           "render_predicate_logical"]
# ── THE VERSION SURFACE (P0-19, ruled Huayin 2026-08-31) ─────────────────────────────────────────
# DERIVED FROM PACKAGE METADATA, NEVER HAND-MAINTAINED. This attribute used to be a literal that a
# human had to remember to bump, and it stopped moving: it read '0.16.0-core' while the distribution
# shipped several releases later. Nothing caught it, because the only test that mentioned it
# ASSERTED the stale value — it could catch an unintended bump and was structurally incapable of
# catching an omitted one.
#
# The fix is to remove the second copy rather than guard it. `importlib.metadata` reads the
# distribution that is actually installed, so this string cannot disagree with what `pip` resolved,
# and no release step has to remember anything.
#
# THE FALLBACK IS DELIBERATELY NOT A VERSION. Outside an installed distribution (a bare source tree
# on `sys.path`) there is no metadata to read, and the honest answer is that we do not know — not a
# plausible-looking number that would be believed. `"unknown"` cannot be mistaken for a release.
#
# CODE IDENTITY IS A DIFFERENT CONCEPT AND IS NOT REDEFINED HERE (ruled): the `-core` label was a
# claim about which SOURCE produced a build, which is not the same fact as which DISTRIBUTION is
# installed. It remains legitimate; if it is needed operationally it gets an explicit name and is
# derived from content, not from another constant someone has to bump.
def _installed_version() -> str:
    from importlib.metadata import PackageNotFoundError, version
    try:
        return version('columna-core')
    except PackageNotFoundError:                             # pragma: no cover - not installed
        return "unknown"


__version__: str = _installed_version()

"""Columna Core — the column-foundation analytic framework (multi-table, transport-based).

THE PUBLIC SURFACE IS LAZY (PEP 562, 2026-09-12, ruled Huayin). Every name in `__all__` still
resolves, to the SAME OBJECT as before; it is simply imported on first access rather than at package
import.

WHY. Until this change, `import columna_core.anything` executed this module, which imported
`planner` — and therefore `engine`, `model`, `projection`, `frameql`, `expr`, `connector` and the
DuckDB dependency behind them. Importing a NEUTRAL contract type therefore loaded the entire legacy
execution stack as a side effect. Proof A found it the honest way: a successor path that excludes the
legacy planner could not import `serving_contract` without loading the planner anyway, so the
exclusion was true of the static import graph and false of the running interpreter.

That is the same defect class as the one `serving_contract` was extracted to fix, one level up. The
extraction moved the wire's TYPES out of the planner; this moves the package's IMPORT-TIME COUPLING
out of the way of anyone who does not want the execution stack.

THIS IS NOT AN API REDESIGN. No name added, none removed, none renamed, none re-homed. `__all__` is
byte-identical to what it was. `from columna_core import Planner` works exactly as before and yields
the same class object. The only observable difference is WHEN a submodule is imported — and, for a
caller who never touches an execution name, whether it is imported at all.

WHAT THIS DELIBERATELY DOES NOT DO. It does not make the submodules themselves lazy, and it does not
break the import cycle between them: `planner` still pulls `engine` and `model` when something asks
for `planner`. The claim is narrower and is exactly the one that was asked for — a neutral or
successor import must not drag the execution stack in behind it.
"""
from importlib import import_module
from typing import Any

# ── THE LAZY EXPORT TABLE ────────────────────────────────────────────────────────────────────────
# name -> (submodule, attribute). The attribute is spelled out even where it equals the name, so an
# alias (ORDERED <- ORDERED_W) is not a special case a reader has to notice.
#
# ONE TABLE, NOT A SCATTERING OF `try: import` BLOCKS. This file used to carry fourteen `from .x
# import (...)` statements whose union WAS the public surface; the surface is now stated once, as
# data, and `__all__` is checked against it by a test rather than by eye.
_EXPORTS: dict = {}

def _register(module: str, *names: str) -> None:
    for n in names:
        _EXPORTS[n] = (module, n)


_register("model",
          "Manifold", "Universe", "Predicate", "Ref", "Comparison", "DimensionLevel",
          "FunctionalEdge", "MeasureColumn", "FamilyMember", "BAnchor", "DerivedColumn", "License",
          "Hierarchy", "Relate", "Face", "TOUCH", "ASSIGN", "ALLOC", "FACE_SCHEMES",
          "VERIFIED", "CORROBORATED", "UNTESTABLE", "CONTRADICTED",
          "ADDITIVE", "SKETCH", "HOLISTIC", "DECLARED", "PROVEN", "INFERRED_SAMPLE",
          "INFERRED_DOCS", "A")
_register("operators",
          "Operator", "REGISTRY", "get_operator", "signature_ok", "output_dtype",
          "VALUE", "REDUCER", "SCAN", "MAP", "kind_of", "reducers")
_EXPORTS["ORDERED"] = ("operators", "ORDERED_W")     # the alias, stated rather than implied
_register("projection",
          "PlannerView", "MeasureShape", "UniverseShape", "DerivedShape", "ShapeEdge", "OperatorSig")
_register("connector", "Connector", "DuckDBConnector", "CatalogAperture", "APERTURE_SAMPLE_CAP")
_register("engine", "ColumnEngine")
_register("planner", "Planner", "FrameResult")
_register("frameql", "ManifoldServer", "Frame", "FrameQLSyntaxError")
_register("disclosure", "Disclosure", "Caveat", "Refusal", "Outcome")
_register("adjudication",
          "adjudicate", "Contradiction", "HierarchyContradiction",
          "PublishedScope", "scope_from_report", "scope_diff")
_register("draft",
          "Draft", "Proposal", "PolarityViolation", "lower_proposal", "DECLARATION_KINDS",
          "INFERRED_CATALOG", "PROPOSED", "ACCEPTED", "STRUCK", "EDITED",
          "SCOPED", "PROPOSED_STATE", "DECLARED_STATE", "ATTESTED", "PUBLISHED")
_register("describe",
          "describe_derived", "license_to_dict", "describe_universe", "describe_hierarchy",
          "operator_properties", "absence_semantics")
_register("sketch",
          "hll_count", "hll_merge", "hll_estimate", "hll_merge_pair", "rse", "Witness",
          "WitnessStore")
_register("documents",
          "logical_spec", "physical_map", "physical_vocabulary", "no_physical_leak",
          "render_predicate_logical")

#: `columna_core.dtypes` is a SUBMODULE alias (`from . import types as dtypes`), not an attribute.
_MODULE_ALIASES = {"dtypes": "types"}


def __getattr__(name: str) -> Any:
    """PEP 562. Resolve a public name on first access, then cache it in the module namespace.

    Caching by `globals()[name] = obj` means the second access costs nothing and, more importantly,
    that identity is stable: `columna_core.Planner is columna_core.Planner` holds, and equals
    `columna_core.planner.Planner`."""
    if name in _MODULE_ALIASES:
        obj = import_module(f".{_MODULE_ALIASES[name]}", __name__)
    elif name in _EXPORTS:
        module, attr = _EXPORTS[name]
        obj = getattr(import_module(f".{module}", __name__), attr)
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    globals()[name] = obj
    return obj


def __dir__():
    """`dir(columna_core)` still lists the whole surface without importing any of it."""
    return sorted(set(globals()) | set(_EXPORTS) | set(_MODULE_ALIASES))


__all__ = ["Manifold", "Universe", "Predicate", "Ref", "Comparison",
           "DimensionLevel", "FunctionalEdge", "MeasureColumn",
           "FamilyMember", "BAnchor", "DerivedColumn", "License", "Hierarchy",
           "Relate", "Face", "TOUCH", "ASSIGN", "ALLOC", "FACE_SCHEMES",
           "VERIFIED", "CORROBORATED", "UNTESTABLE", "CONTRADICTED", "ADDITIVE", "SKETCH", "HOLISTIC",
           "DECLARED", "PROVEN", "INFERRED_SAMPLE", "INFERRED_DOCS", "A",
           "Operator", "REGISTRY", "get_operator", "signature_ok", "output_dtype", "VALUE", "ORDERED", "REDUCER", "SCAN", "MAP", "kind_of", "reducers",
           "dtypes", "PlannerView", "MeasureShape", "UniverseShape", "DerivedShape", "ShapeEdge", "OperatorSig",
           "Connector", "DuckDBConnector", "ColumnEngine", "Planner", "FrameResult",
           "ManifoldServer", "Frame", "FrameQLSyntaxError",
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

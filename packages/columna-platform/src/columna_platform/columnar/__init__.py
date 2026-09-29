"""
columna_platform.columnar — **the MME's columnar data plane: Arrow carriage, DataFusion execution.**

    governed columnar state → grouped family continuation → anchor-index alignment
                            → columnar expression evaluation

    index      `CoordinateIndex` (M, U, A + the SPARSE existing points) and `AnchorInstance` (…+ I)
    standing   governed participation/support masks, carried INDEPENDENTLY of Arrow nullability
    block      `GovernedBlock` — a physical container, never analytical identity
    provider   Arrow kernels + DataFusion grouped reduction + the HLL union UDAF. No SQL, no join
    mme        `ColumnarMME` — delegates every authority question to `kernel.MME.adjudicate`.
               **FAMILY MATERIALIZATIONS ONLY** (M-2)
    expression `ColumnarExpressionEvaluator` — ABOVE the MME; consumes family state, evaluates `E@A`
    exhibit    the runnable proof

    THE PHYSICAL RULE   the MME does not discover analytical alignment by joining analytical tables.
    THE STANDING RULE   Arrow NULL has no intrinsic ToD standing.
    THE DOMAIN RULE     participation determines the contributing domain; support determines whether the
                        values required OVER that domain are established. Support never shrinks it — an
                        unsupported participating point makes a value-bearing reduction REFUSE for want of
                        state, and leaves a population reduction untouched.
    THE AUTHORITY RULE  the kernel adjudicates; Arrow and DataFusion realize.
"""
from __future__ import annotations

from .block import GovernedBlock, value_column_name
from .index import AnchorInstance, CoordinateIndex
from .expression import ColumnarExpressionEvaluator
from .mme import ColumnarExpressionOutput, ColumnarFamilyState, ColumnarMME
from .provider import (
    AlignmentReport,
    ColumnarProvider,
    ContinuationResult,
    HLL_PRECISION,
    PROVIDER_NAME,
    estimate_of,
    sketch_of,
    sketch_parameters,
)
from .standing import ColumnStanding, POPULATION, VALUE_BEARING, mask, standing

__all__ = ["AlignmentReport", "AnchorInstance", "COLUMN_STANDING_SHAPES", "ColumnStanding",
           "ColumnarExpressionEvaluator", "ColumnarExpressionOutput", "ColumnarFamilyState",
           "ColumnarMME", "ColumnarProvider",
           "ContinuationResult", "CoordinateIndex", "GovernedBlock", "HLL_PRECISION", "POPULATION",
           "PROVIDER_NAME", "VALUE_BEARING", "estimate_of", "mask", "sketch_of", "sketch_parameters",
           "standing", "value_column_name"]

COLUMN_STANDING_SHAPES = (POPULATION, VALUE_BEARING)

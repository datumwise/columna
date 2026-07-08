"""
columna_core.types — the LOGICAL type vocabulary (a Core-relevant subset of Polars dtypes).

The logical type of a column is its in-engine representation promise — and the engine is
Polars, so the logical types ARE Polars dtypes (a scalar subset). Columns declare a concrete
dtype (Decimal-vs-Float64 for money is a real authoring choice); operator signatures range
over CLASSES (Numeric, Ordered, Temporal, Categorical) and the planner checks dtype-in-class.

The split: logical types live here + on columns + in the registry (vocabulary, planner-visible);
physical types (VARCHAR, DOUBLE, ...) live in the connector, which lifts physical->logical at
publish and realizes logical->physical at delivery. The planner never sees a physical type.

Note (Core scope): signatures gate on class membership. Temporal arithmetic is NOT modelled
(Date+Duration->Date, Date-Date->Duration) — `sum` accepts Numeric and Duration and rejects
Date/Datetime/Time, which is correct on what it accepts/rejects without committing to an algebra.
Nested dtypes (List/Struct/Array/Binary/Object) are out of Core scope (you don't aggregate a
struct here).
"""
from __future__ import annotations

# ---- concrete logical dtypes (Polars scalar subset) -------------------------
INT64       = "Int64"
FLOAT64     = "Float64"
DECIMAL     = "Decimal"
BOOLEAN     = "Boolean"
STRING      = "String"
DATE        = "Date"
DATETIME    = "Datetime"
DURATION    = "Duration"
TIME        = "Time"
CATEGORICAL = "Categorical"
ENUM        = "Enum"

DTYPES = frozenset({INT64, FLOAT64, DECIMAL, BOOLEAN, STRING,
                    DATE, DATETIME, DURATION, TIME, CATEGORICAL, ENUM})

# ---- type classes (groupings for operator signatures) -----------------------
NUMERIC  = frozenset({INT64, FLOAT64, DECIMAL})
TEMPORAL = frozenset({DATE, DATETIME, DURATION, TIME})
ORDERED  = NUMERIC | TEMPORAL | frozenset({STRING, BOOLEAN})    # totally ordered
NOMINAL  = frozenset({CATEGORICAL, ENUM, STRING})              # groupable/countable
ANY      = DTYPES


def is_dtype(t: str) -> bool:
    return t in DTYPES


# ---- parametric sketch types (custom datatypes; case study) -----------------
# A sketch type is written HLLSketch(p): the precision p is part of the type identity, so
# HLLSketch(12) and HLLSketch(14) are DIFFERENT types (only same-precision sketches merge).
HLLSKETCH = "HLLSketch"                      # the type FAMILY marker used in operator signatures
SKETCH = frozenset({HLLSKETCH})

def hll_sketch_t(precision: int) -> str:
    return f"HLLSketch({precision})"

def is_hll_sketch(t: str) -> bool:
    return isinstance(t, str) and t.startswith("HLLSketch(") and t.endswith(")")

def hll_precision(t: str) -> int:
    return int(t[len("HLLSketch("):-1])


def dtype_in(dtype: str, accepts: frozenset) -> bool:
    """Signature membership, sketch-aware. A concrete HLLSketch(p) matches an `accepts` set that
    lists the HLLSketch family. Note ANY = DTYPES does NOT include sketches, so ordinary numeric
    operators correctly REJECT a raw sketch — you must hll_estimate it to a number first."""
    if dtype in accepts:
        return True
    if is_hll_sketch(dtype) and HLLSKETCH in accepts:
        return True
    return False

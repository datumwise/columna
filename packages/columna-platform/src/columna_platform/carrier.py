"""The synthetic Arrow carrier — built in memory, from no source.

NO DATABASE, NO DRIVER, NO FILE. The carrier is constructed directly as a `pyarrow.Array` so the
proof exercises the ADMISSION BOUNDARY and nothing else. A carrier read from DuckDB would prove that
DuckDB works; a carrier built here proves what admission does with a given physical representation,
which is the only question Proof A asks.

The shapes below are not invented. Each mirrors a row MEASURED in
`docs/architecture/admission_fidelity_study_v0_1.md` (pyarrow 25.0.1 / polars 1.44.2 / duckdb 1.5.5),
so the negative controls are evidence rather than illustration.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

import pyarrow as pa

#: The measured ceiling of the carrier used here: `decimal128` carries 38 digits
#: (admission study §"Decimal ceiling measured"). A LIMIT OF A CARRIER, never the governed bound on
#: an exact-decimal domain — ruling_2026_09_12_exact_decimal_carriage.md §5.
DECIMAL128_MAX_PRECISION = 38


@dataclass(frozen=True)
class Carrier:
    """A physical representation, plus the provenance of the shape it is standing in for."""

    array: pa.Array
    #: which measured case this shape reproduces, so a failing control can be traced to a row
    measured_as: str

    @property
    def type(self) -> pa.DataType:
        return self.array.type

    @property
    def null_count(self) -> int:
        return self.array.null_count


def exact_money() -> Carrier:
    """`decimal128(18,4)` — MEASURED PRESERVED end to end (study: `DECIMAL(18,4)` money).

    This is the lawful carrier: the governed exact-decimal domain carried exactly, which is what
    made the old `decimal -> Float64` mapping unforced rather than necessary."""
    return Carrier(
        pa.array([Decimal("12345678901234.5678"), Decimal("1.0000"), Decimal("0.3000")],
                 type=pa.decimal128(18, 4)),
        measured_as="duckdb DECIMAL(18,4) -> arrow decimal128(18,4) -> polars Decimal(18,4), preserved",
    )


def lossy_float() -> Carrier:
    """`float64` where the governed domain is `decimal` — NEGATIVE CONTROL 1.

    The naturally occurring SQLite `REAL` case. The study measured the loss AT REST:
    `12345678901234.5678 -> 12345678901234.568`. Delivery succeeds; nothing raises; the value is
    simply no longer the governed one. Admission is the only place left to catch it."""
    return Carrier(
        pa.array([12345678901234.5678, 1.0, 0.3], type=pa.float64()),
        measured_as="sqlite REAL -> arrow double: SOURCE LOSS 12345678901234.5678 -> ...568",
    )


def over_envelope() -> Carrier:
    """`decimal128(38,0)` at full width — NEGATIVE CONTROL 4 (the fourth-hop case).

    Arrow holds the full-width integer EXACTLY; the in-process conversion is where the digits go.
    Nothing raises. This is the empirical reason the admission envelope is stated as four hops —
    source -> driver/configuration -> Arrow -> in-process carrier — and not merely driver -> Arrow:
    a carrier that is exact at hop three can still lose at hop four.

    DEVIATION FROM THE MEASURED VALUE, RECORDED. The study's row is DuckDB `HUGEINT` ->
    `decimal128(38,0)` carrying `170141183460469231731687303715884105727` — the int128 maximum, which
    is THIRTY-NINE digits. `pa.array(...)` refuses to build that from a Python `Decimal`:

        ArrowInvalid: Decimal type with precision 39 does not fit into precision
                      inferred from first array element: 38

    So the synthetic carrier uses the largest value that decimal128(38,0) can actually hold. The
    SHAPE under test — full-width `decimal128(38,0)`, exact in Arrow, lost on conversion — is the
    measured one; the value is one digit narrower because the carrier cannot be constructed at the
    measured width without a driver. Worth keeping rather than smoothing over: it means the study's
    own HUGEINT row describes an Arrow array that this path cannot construct directly, which is a
    small independent confirmation that the loss is real and driver-mediated."""
    return Carrier(
        pa.array([Decimal("9" * 38)], type=pa.decimal128(38, 0)),
        measured_as="HUGEINT -> arrow decimal128(38,0) exact -> polars ...E+38, POLARS LOSS "
                    "(shape reproduced at 38 digits; see docstring)",
    )


def with_absence() -> Carrier:
    """An exact decimal carrier containing a NULL — NEGATIVE CONTROL 3.

    The study measured that a null SURVIVES as a null and the decimal type survives with it
    (`decimal128(18,4)`, validity bitmap distinct from values). So the carrier faithfully reports
    *that* something is absent. What it cannot report is what the absence MEANS, which is a governed
    question and not a carrier one."""
    return Carrier(
        pa.array([Decimal("1.0000"), None, Decimal("2.0000")], type=pa.decimal128(18, 4)),
        measured_as="NULL in decimal column -> decimal128(18,4), preserved, type survives",
    )


def describe(c: Carrier) -> str:
    """A one-line physical description — used in refusal detail, never in a governed decision."""
    t = c.type
    extra = f", nulls={c.null_count}" if c.null_count else ""
    if pa.types.is_decimal(t):
        return f"{t} (precision={t.precision}, scale={t.scale}{extra})"
    return f"{t}{extra}"


def precision_of(t: pa.DataType) -> Optional[int]:
    return t.precision if pa.types.is_decimal(t) else None


# ── ANCHORED CARRIERS (Proof B) ──────────────────────────────────────────────────────────────────
# Proof A's carriers are bare value arrays: enough to prove that a governed domain survives
# admission, because admission asks about the VALUE's representation and nothing else.
#
# A movement asks a different question — it folds contributions ACROSS a coordinate — so the carrier
# has to say which analytical point each value sits at. That is a `pa.Table` whose non-value columns
# are the anchor's declared components. Still synthetic, still in memory, still from no source.


def exact_money_at_sale_at() -> "AnchoredCarrier":
    """Exact decimal revenue at `sale_at = store x day`, four points over two stores.

    Chosen so the fold is not a no-op and not a coincidence: each store has TWO days, and the two
    stores' totals differ, so a projection that dropped rows, double-counted, or grouped on the wrong
    column produces a visibly wrong answer rather than an accidentally right one.

        east / 2026-01-01   10.0000        east total   30.0000
        east / 2026-01-02   20.0000
        west / 2026-01-01    1.2345        west total    4.9382
        west / 2026-01-02    3.7037
    """
    return AnchoredCarrier(
        table=pa.table({
            "store": pa.array(["east", "east", "west", "west"], type=pa.string()),
            "day": pa.array([date(2026, 1, 1), date(2026, 1, 2),
                             date(2026, 1, 1), date(2026, 1, 2)], type=pa.date32()),
            "amount": pa.array([Decimal("10.0000"), Decimal("20.0000"),
                                Decimal("1.2345"), Decimal("3.7037")],
                               type=pa.decimal128(18, 4)),
        }),
        value_column="amount",
        anchor_columns=("store", "day"),
        measured_as="duckdb DECIMAL(18,4) -> arrow decimal128(18,4) -> preserved",
    )


@dataclass(frozen=True)
class AnchoredCarrier:
    """A carrier that knows which analytical point each value sits at."""

    table: pa.Table
    value_column: str
    anchor_columns: tuple
    measured_as: str

    @property
    def values(self) -> pa.Array:
        return self.table.column(self.value_column).combine_chunks()

    def as_carrier(self) -> Carrier:
        """The value column alone — what ADMISSION looks at. Admission asks about the value's
        representation; the coordinates are not its business."""
        return Carrier(self.values, self.measured_as)

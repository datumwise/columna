"""The DEPLOYMENT's material for the lighthouse unit — a fixture, not package source.

IT LIVES HERE AND NOT IN `src/` DELIBERATELY. Which bytes sit behind `warehouse:sales.fact_sale` is
a deployment fact; a package that shipped it would be hard-coding the meaning of a connection token,
which is exactly what the source binding exists to avoid. Both test suites read it from this one
place so the two cannot drift into disagreeing about what the deployment holds.

THE PHYSICAL NAMES ARE NOT THE GOVERNED ONES, AND THAT IS THE POINT. The publication declares
`sale_at{store, day}`; this table has `store_code` and `sold_on`. The mapping's `anchor_component`
realizations are what claim that one realizes the other, and `source.read_anchored` is what honours
the claim. If the two vocabularies were spelled alike, a path that ignored the realization entirely
would pass every test.

THE VALUES ARE THE PROOF-A SHAPE, REACHED THROUGH A SOURCE. Four points over two stores, each store
with two days, and the two stores' totals different — chosen so that a fold that dropped rows,
double-counted, or grouped on the wrong column produces a visibly wrong answer rather than an
accidentally right one. `decimal128(18,4)`, the carriage measured as PRESERVED end to end.

NO NULLS. Admission refuses any absence in this family's carrier, because lighthouse's C9 answers
what an EMPTY FIBER denotes and not what an ABSENT OBSERVATION denotes. A deployment fixture with a
null would refuse correctly and prove nothing about material execution, so the absence case is held
in its own negative control instead.
"""
from datetime import date
from decimal import Decimal

import pyarrow as pa

from columna_platform.source import InMemoryArrowSource, SourceBindings

#: What the realization claims, restated here so a drift between the two is visible in one place.
CONNECTION = "warehouse"
SCHEMA = "sales"
TABLE = "fact_sale"

#: physical column names, as the anchor-component and family realizations name them
STORE_COLUMN = "store_code"
DAY_COLUMN = "sold_on"
VALUE_COLUMN = "amount"

#: east totals 30.0000; west totals 4.9382. Different, and neither a round number by accident.
ROWS = (
    ("east", date(2026, 1, 1), Decimal("10.0000")),
    ("east", date(2026, 1, 2), Decimal("20.0000")),
    ("west", date(2026, 1, 1), Decimal("1.2345")),
    ("west", date(2026, 1, 2), Decimal("3.7037")),
)


def fact_sale() -> pa.Table:
    """The one material object, with its physical column names and exact decimal carriage."""
    return pa.table({
        STORE_COLUMN: pa.array([r[0] for r in ROWS], type=pa.string()),
        DAY_COLUMN: pa.array([r[1] for r in ROWS], type=pa.date32()),
        VALUE_COLUMN: pa.array([r[2] for r in ROWS], type=pa.decimal128(18, 4)),
    })


def source(**columns) -> InMemoryArrowSource:
    """The deployment's source. `columns` overrides a column's array, for negative controls."""
    table = fact_sale()
    for name, array in columns.items():
        table = table.set_column(table.column_names.index(name), name, array)
    return InMemoryArrowSource(name="lighthouse-warehouse", objects={(SCHEMA, TABLE): table})


def bindings(connection: str = CONNECTION, **columns) -> SourceBindings:
    """`connection` -> the source. Naming a different connection is how a control moves the binding
    out from under a claim that still says `warehouse`."""
    return SourceBindings({connection: source(**columns)})

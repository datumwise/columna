"""Columna ADBC source adapters — material, through a real driver, for the successor path.

WHAT THIS PACKAGE IS FOR. `columna-platform` reserves one seam for material — `MaterialSource`, a
single projected `fetch` — and deliberately implements only an in-process source behind it. This
package implements that seam against a real driver, and it exists AS A SEPARATE PACKAGE so the
dependency arrow can be stated and tested rather than hoped for:

    columna-adbc  ->  columna-platform  ->  columna-core

never the reverse. Platform's standing forbidden-import tests are unchanged by this package's
existence: they were always package-scoped — *Platform must not import a driver* — and never a claim
that the repository contains none.

NOTHING HERE DECIDES ADMISSIBILITY. An adapter EXPOSES material; CAP v1 decides whether Platform may
use it, by inspecting the Arrow schema that actually arrived. That division is the whole point of the
study's conclusion — *successful transport does not establish admissibility* — and this package is
built so that it cannot be quietly violated: there is no place in it where a governed fact is read.
"""
from .duckdb_adbc import (
    DuckDbAdbcSource, DriverSurfaceUnavailable, driver_surface, projection_sql,
)

__all__ = [
    "DuckDbAdbcSource",
    "DriverSurfaceUnavailable",
    "driver_surface",
    "projection_sql",
]

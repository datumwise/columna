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
built so that it cannot be quietly violated.

**B-2 ADDED A SECOND SEAM AND SHARPENED THAT SENTENCE, WHICH USED TO SAY MORE THAN IT COULD.** It read
*"there is no place in it where a governed fact is read"*, and `duckdb_realization` reads several: a
`FamilyRequirement` tells a provider which family, which root anchor, which law, which value form, which
analytical instance, which build and which constitution witness. The true statement — the one the ban was
always about — is narrower and stronger:

    **this package READS governed facts and JUDGES none of them.**

It restates `build` and `witness` so that `MME.put` can compare them; it cannot mint the credential that
says its own output is faithful (`AdjudicatedRealization` is minted inside Platform's fidelity boundary and
nowhere else); and it cannot reach `MME.put` except through `RealizationAuthority.adjudicate`. That the
provider is real rather than a test double grants it no additional authority, which is the half of B-2 that
exists to prove B-1' survives contact with reality.

    duckdb_adbc          the MATERIAL seam — `MaterialSource.fetch`, one bare projection, Arrow out
    duckdb_realization   the REALIZATION seam — `RealizationProvider.propose`/`realize`, governed Arrow
                         family state out, on its way to independent fidelity adjudication
"""
from .duckdb_adbc import (
    DuckDbAdbcSource, DriverSurfaceUnavailable, driver_surface, projection_sql,
)
from .duckdb_realization import ARROW_OVER_ADBC, DuckDbFamilyProvider, PhysicalFamilyBinding

__all__ = [
    "ARROW_OVER_ADBC",
    "DuckDbAdbcSource",
    "DuckDbFamilyProvider",
    "DriverSurfaceUnavailable",
    "PhysicalFamilyBinding",
    "driver_surface",
    "projection_sql",
]

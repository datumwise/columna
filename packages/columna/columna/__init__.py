"""Columna, by datumwise — honest metrics engine.

This is the metapackage. Installing ``columna`` installs ``columna-core`` (the engine) and
``columna-server`` (the MCP server); the implementation lives in those packages — import from
``columna_core`` and ``columna_server``. Its version rides in lockstep with ``columna-core``.
"""

__version__ = "0.11.1"

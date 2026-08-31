"""Columna, by datumwise — honest data framework.

This is the metapackage. Installing ``columna`` installs ``columna-core`` (the engine) and
``columna-server`` (the MCP server); the implementation lives in those packages — import from
``columna_core`` and ``columna_server``. Its version rides in lockstep with ``columna-core``
— enforced by ``scripts/release_pins.py --check``, not by memory.
"""

# ── THE VERSION SURFACE (P0-19, ruled Huayin 2026-08-31) ─────────────────────────────────────────
# DERIVED FROM PACKAGE METADATA, NEVER HAND-MAINTAINED. This attribute used to be a literal that a
# human had to remember to bump, and it stopped moving: it read '0.14.0' while the distribution
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
        return version('columna')
    except PackageNotFoundError:                             # pragma: no cover - not installed
        return "unknown"


__version__: str = _installed_version()

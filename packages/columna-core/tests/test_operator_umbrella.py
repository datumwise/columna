"""
test_operator_umbrella.py — mirrors demos/operator_umbrella_demo.py.

Each of the suite's 10 checks becomes one pytest item (the check name is the test id), run against
the checked-in mini-warehouse. Same checks as the demo, asserted individually. Demo logic unchanged.
"""
import pytest

from _demo_driver import fixture_run

_RUN = fixture_run("operator_umbrella_demo")


@pytest.mark.parametrize("name", _RUN.names(), ids=_RUN.names())
def test_check(name):
    ok, detail = _RUN.result(name)
    assert ok, f"{name} — {detail}"


# ── one alias authority: a surface spelling means the same thing everywhere ──────────────────────
def test_alias_table_is_the_single_surface_name_authority():
    """Ruled (Huayin, 2026-09-01): we should not have `ALIASES` and `_INLINE_REDUCERS` independently
    defining the same surface-name law. `_INLINE_REDUCERS` was a hand-maintained dict that separately
    declared `avg` -> `mean`; it is gone, and call-position resolution is now DERIVED from the alias
    table plus SERIES_REDUCERS. Two authorities for one fact is how `approx_distinct` could be a
    declared alias and still not resolve."""
    from columna_core import planner as _p
    from columna_core.operators import ALIASES, SERIES_REDUCERS, canonical

    assert not hasattr(_p.Planner, "_INLINE_REDUCERS"), \
        "the duplicate surface-name authority must not come back"
    assert canonical("avg") == "mean" and canonical("approx_distinct") == "distinct"
    assert canonical("sum") == "sum"                      # identity for a non-alias
    # every alias target is a real registry entry — an alias may not point at nothing
    from columna_core.operators import REGISTRY
    for surface, core in ALIASES.items():
        assert core in REGISTRY, f"alias {surface} -> {core} names no registered operator"
    assert SERIES_REDUCERS <= set(REGISTRY)

"""
test_hll_case_study.py — mirrors demos/hll_case_study_demo.py.

Each of the suite's 20 checks becomes one pytest item (the check name is the test id), run against
the checked-in mini-warehouse. Same checks as the demo, asserted individually. Demo logic unchanged.
"""
import pytest

from _demo_driver import fixture_run

_RUN = fixture_run("hll_case_study_demo")


@pytest.mark.parametrize("name", _RUN.names(), ids=_RUN.names())
def test_check(name):
    ok, detail = _RUN.result(name)
    assert ok, f"{name} — {detail}"


def test_canonical_surface_spelling_resolves(tmp_path):
    """Ruled (Huayin, 2026-09-01): `approx_distinct` is the canonical Frame-QL surface spelling for
    the existing approximate-distinct capability, and that spelling must actually resolve — while
    existing `distinct` compatibility is preserved. One capability, two roles.

    The Manual keeps `approx_distinct` because the answer IS an estimate carrying its
    relative-standard-error; renaming the Manual to `distinct` to match a registry spelling would
    make an approximate result sound exact."""
    import io, contextlib, os, sys
    demos = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "demos")
    sys.path.insert(0, demos)
    src = open(os.path.join(demos, "hll_case_study_demo.py")).read()
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src.split("# (b)")[0], "demo", "exec"), ns)
    srv = ns["srv"]

    core = srv.frame("region").column("v", "visitors.distinct").run()
    surface = srv.frame("region").column("v", "visitors.approx_distinct").run()
    assert core.columns[0].frame.sort("region").rows() == surface.columns[0].frame.sort("region").rows(), \
        "the canonical surface spelling must denote the SAME capability, not a second operator"

    bad = srv.frame("region").column("v", "visitors.nonsense").run()
    assert bad.columns[0].refusal is not None, "an unknown member must still be refused"

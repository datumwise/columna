"""
test_holistic.py — mirrors demos/holistic_demo.py.

Each of the suite's 5 checks becomes one pytest item (the check name is the test id), run against
the checked-in mini-warehouse. Same checks as the demo, asserted individually. Demo logic unchanged.
"""
import pytest

from _demo_driver import fixture_run

_RUN = fixture_run("holistic_demo")


@pytest.mark.parametrize("name", _RUN.names(), ids=_RUN.names())
def test_check(name):
    ok, detail = _RUN.result(name)
    assert ok, f"{name} — {detail}"

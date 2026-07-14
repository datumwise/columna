"""
test_fixture_drift.py — infrastructure guards (not part of the 124 demo-mirror checks).

  * rider 3: demos/benchmark.cml and tests/fixtures/benchmark.cml must be BYTE-IDENTICAL.
  * spec: the mini-warehouse stays <= 2 MB.
  * acceptance 1: `import columna_core` succeeds and reports the pinned version.
  * drift guard: the 9 fixture demos each run cleanly and emit exactly the expected number of
    checks (104 total) — so a demo gaining/losing a check, or crashing, fails loudly here rather
    than silently shifting the 124 / 104 / 20 accounting.
"""
import os

import pytest

from _demo_driver import DEMOS, FIXTURE_WAREHOUSE, fixture_run

_HERE = os.path.dirname(os.path.abspath(__file__))
_CML_DEMOS = os.path.join(DEMOS, "benchmark.cml")
_CML_FIXTURE = os.path.join(_HERE, "fixtures", "benchmark.cml")

# demo -> expected fixture-run check count (the 104 total)
_EXPECTED_COUNTS = {
    "coanchor_demo": 17,
    "confine_demo": 12,
    "hll_case_study_demo": 20,
    "holistic_demo": 5,
    "locus_demo": 11,
    "operator_umbrella_demo": 10,
    "projection_demo": 16,
    "types_demo": 10,
    "universe_check_demo": 3,
}


def test_benchmark_cml_byte_identical():
    with open(_CML_DEMOS, "rb") as a, open(_CML_FIXTURE, "rb") as b:
        assert a.read() == b.read(), (
            "demos/benchmark.cml and tests/fixtures/benchmark.cml have drifted — they must be "
            "byte-identical (rider 3)."
        )


def test_mini_warehouse_within_budget():
    total = sum(
        os.path.getsize(os.path.join(FIXTURE_WAREHOUSE, f))
        for f in os.listdir(FIXTURE_WAREHOUSE)
        if f.endswith(".parquet")
    )
    assert total <= 2 * 1024 * 1024, f"mini-warehouse is {total/1024:.1f} KB > 2 MB budget"


def test_import_and_version():
    import columna_core

    assert columna_core.__version__ == "0.7.8-core"


@pytest.mark.parametrize("demo,expected", sorted(_EXPECTED_COUNTS.items()))
def test_fixture_demo_check_count(demo, expected):
    run = fixture_run(demo)
    assert run.returncode == 0, run.stderr[-2000:]
    got = len(run.names())
    assert got == expected, (
        f"{demo} emitted {got} checks, expected {expected} — the 124/104/20 accounting drifted."
    )


def test_total_fixture_checks_is_104():
    total = sum(len(fixture_run(d).names()) for d in _EXPECTED_COUNTS)
    assert total == 104, f"fixture demos emitted {total} checks total, expected 104"


def test_structural_parity_parsed_vs_code(parsed_manifold, hand_manifold):
    """The ingest-first .cml must reproduce the code-built Manifold's vocabulary.

    Pure structural check — no warehouse, no connection — so it runs in default CI. Guards the
    WP-0 follow-up that reconciled `region_label` into benchmark.cml: the parsed measure-set and
    the code-built measure-set must stay equal, so the two definitions never re-drift.
    """
    assert set(parsed_manifold.measures) == set(hand_manifold.measures), (
        f"measure-set drift — parsed={sorted(parsed_manifold.measures)} "
        f"code={sorted(hand_manifold.measures)}"
    )
    assert set(parsed_manifold.universes) == set(hand_manifold.universes)
    assert set(parsed_manifold.levels) == set(hand_manifold.levels)
    assert len(parsed_manifold.edges) == len(hand_manifold.edges)
    assert set(parsed_manifold.derived) == set(hand_manifold.derived)

    # WP-B (B-2 adjustment #4): the parity guard must cover the fertility surface, so the moment a
    # fertile derived column joins the shipped benchmark the parsed and code-built readings can never
    # silently diverge on it. Compare the derived surface field-by-field: resolution anchor, member
    # set, and each member's DECLARED lineages. (No License is compared — the parser never mints one;
    # the adjudicator does, at publish, downstream of both readings.)
    for name in parsed_manifold.derived:
        pd, hd = parsed_manifold.derived[name], hand_manifold.derived[name]
        assert pd.resolution_anchor == hd.resolution_anchor, f"derived '{name}' resolution-anchor drift"
        assert set(pd.family) == set(hd.family), f"derived '{name}' member-set drift"
        for mem in pd.family:
            assert pd.family[mem].declared_lineages == hd.family[mem].declared_lineages, (
                f"derived '{name}' member '{mem}' declared-lineage drift"
            )
            assert pd.family[mem].license is None and hd.family[mem].license is None, (
                f"derived '{name}' member '{mem}' carries a License pre-adjudication (parser must not mint)"
            )

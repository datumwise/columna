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

# demo -> expected fixture-run check count (99 total after the §2c coanchor rewrite; was 104)
_EXPECTED_COUNTS = {
    "coanchor_demo": 12,   # §2c rewrite (was 17): cross-universe -> error, juxtaposition, no ON UNIVERSE
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
    """`columna_core.__version__` reports the INSTALLED DISTRIBUTION and is never hand-maintained.

    THIS TEST USED TO POINT THE WRONG WAY (P0-19, ruled Huayin 2026-08-31). It asserted the literal
    `"0.16.0-core"`, which made it able to catch an UNINTENDED bump and structurally incapable of
    catching an OMITTED one — the same asymmetry as `assert_pypi_versions.py`, which catches a
    forgotten bump only when the forgotten version is ABSENT. Core's source then changed across
    three releases (0.17.0, 0.18.0, 0.18.1) while the label sat still, and this test held it there.

    So the assertion is inverted: the attribute must AGREE WITH PACKAGE METADATA. A future edit that
    reintroduces a hand-typed literal passes today and fails the first time a release moves — which
    is the direction a version guard has to fail in."""
    import columna_core
    from importlib.metadata import version

    installed = version("columna-core")
    assert columna_core.__version__ == installed, (
        f"columna_core.__version__ is {columna_core.__version__!r} but the installed columna-core "
        f"distribution is {installed!r}. This attribute is derived from package metadata and must "
        f"never be a literal — see P0-19 in the consolidated ledger."
    )


@pytest.mark.parametrize("demo,expected", sorted(_EXPECTED_COUNTS.items()))
def test_fixture_demo_check_count(demo, expected):
    run = fixture_run(demo)
    assert run.returncode == 0, run.stderr[-2000:]
    got = len(run.names())
    assert got == expected, (
        f"{demo} emitted {got} checks, expected {expected} — the 124/104/20 accounting drifted."
    )


def test_total_fixture_checks_is_99():
    # was 104; the §2c coanchor rewrite dropped it to 99 (coanchor 17 -> 12).
    total = sum(len(fixture_run(d).names()) for d in _EXPECTED_COUNTS)
    assert total == 99, f"fixture demos emitted {total} checks total, expected 99"


#: THE GOVERNED DECLARATION SURFACE OF A MEASURE — the bounded set of fields the two readings of
#: one manifold are intended to AGREE ABOUT (P1-18, ruled Huayin 2026-09-02). Deliberately a named
#: list and not deep equality: three fields are excluded on purpose and each exclusion is a rule.
#:
#:   description  prose. `.cml` DESCRIPTION and a code-built docstring may legitimately differ.
#:   rejects      MAP-layer artifact, "BLAST WALL: map-artifact ONLY; NEVER describe/wire" (model.py).
#:   evidence     an attestation standing, not a declaration.
_MEASURE_DECL_FIELDS = ("universe", "home_table", "pre_expr", "logical_type",
                        "fill_rule", "m_anchor", "distinct_col", "sketch_precision")


def _family_decl(meas):
    """A family member's DECLARED surface: which operator, which lineages it is barred along, and
    the order it reduces by. `description` is folklore; `license` is minted by the adjudicator at
    publish and is None on both readings here (the derived block below already asserts that)."""
    return {name: (m.agg, frozenset(getattr(m.b_anchor, "blocked", frozenset()) or frozenset()),
                   m.order_by)
            for name, m in meas.family.items()}


def test_structural_parity_parsed_vs_code(parsed_manifold, hand_manifold):
    """The ingest-first .cml must reproduce the code-built Manifold's DECLARATIONS.

    Pure structural check — no warehouse, no connection — so it runs in default CI.

    WHAT THIS TEST USED TO COMPARE, AND WHY THAT WAS THE DEFECT (P1-18). It was added by the WP-0
    follow-up `f1affb1`, whose subject is "reconcile parity in the .cml's favor (region_label)" and
    whose stated purpose was that "the two definitions never re-drift". It compared measure NAME
    SETS. In the very commit that added it, `build_benchmark.py` declared `region_label` as
    `logical_type="String"` and the new `.cml` line carried no `TYPE` clause at all — so the parser
    supplied `Float64`, the connector honoured that with `TRY_CAST(customer_region AS DOUBLE)`, and
    every value became NULL. The guard reported parity for fifty-four days, because the two readings
    did agree about the one thing it measured: the name.

        A parity check must measure the semantic declarations it claims to keep in parity,
        not merely object names.  (ruled Huayin, 2026-09-02)

    So the measure surface now gets the field-by-field treatment the DERIVED surface has had since
    WP-B. The bounded list is `_MEASURE_DECL_FIELDS` plus the family's declared shape; the three
    excluded fields are named there with the reason for each.
    """
    assert set(parsed_manifold.measures) == set(hand_manifold.measures), (
        f"measure-set drift — parsed={sorted(parsed_manifold.measures)} "
        f"code={sorted(hand_manifold.measures)}"
    )

    drift = []
    for name in sorted(parsed_manifold.measures):
        pm, hm = parsed_manifold.measures[name], hand_manifold.measures[name]
        for f in _MEASURE_DECL_FIELDS:
            pv, hv = getattr(pm, f), getattr(hm, f)
            if pv != hv:
                drift.append(f"measure '{name}'.{f}: parsed={pv!r} code={hv!r}")
        if _family_decl(pm) != _family_decl(hm):
            drift.append(f"measure '{name}'.family: parsed={_family_decl(pm)} code={_family_decl(hm)}")
    for name in sorted(parsed_manifold.levels):
        pl, hl = parsed_manifold.levels[name], hand_manifold.levels[name]
        if (pl.realized_by, pl.is_base) != (hl.realized_by, hl.is_base):
            drift.append(f"level '{name}': parsed=({pl.realized_by}, {pl.is_base}) "
                         f"code=({hl.realized_by}, {hl.is_base})")

    for name in sorted(parsed_manifold.universes):
        pu, hu = parsed_manifold.universes[name], hand_manifold.universes[name]
        if pu.base_dimensions != hu.base_dimensions:
            drift.append(f"universe '{name}'.base_dimensions: parsed={sorted(pu.base_dimensions)} "
                         f"code={sorted(hu.base_dimensions)}")
        if pu.basis != hu.basis:
            drift.append(f"universe '{name}'.basis: parsed={pu.basis!r} code={hu.basis!r}")

    # COLLECTED, NOT SHORT-CIRCUITED. A guard that stops at the first disagreement makes the reader
    # discover a multi-field drift one CI run at a time, and this test exists precisely because a
    # partial reading of a declaration was mistaken for the whole of it.
    assert not drift, (
        "DECLARATION drift between the parsed .cml and the code-built Manifold — the two readings "
        "of one manifold disagree about governed meaning, not merely about names:\n  "
        + "\n  ".join(drift))
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

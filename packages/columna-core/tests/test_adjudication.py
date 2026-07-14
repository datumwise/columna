"""
test_adjudication.py — WP-B B-3: the Certificate-kernel adjudicator.

The constitutional ladder, exercised end to end:
    authority is declared; mathematics may verify; data may only refute or corroborate; default closed.

  * math channel  → VERIFIED (homogeneous-linear formula under the additive-monoid reducer `sum`);
                    timeless, attestation None, never touches data.
  * data channel  → CONTRADICTED (publish fails closed, counterexample named) | CORROBORATED
                    (survived refutation, watermarked to the attestation) | UNTESTABLE (recorded,
                    visible in describe, never exercised).
  * re-attestation → a CORROBORATED license flips to CONTRADICTED when re-attested data carries a
                    counterexample (publish fails closed on the new data).

Fixtures (`hand_manifold`, `fixture_connector`, `parsed_manifold`) come from tests/conftest.py.
"""
import glob
import os

import pytest

from columna_core import ManifoldServer, Contradiction, VERIFIED, CORROBORATED, UNTESTABLE
from columna_core.adjudication import adjudicate, _homogeneous_linear
from columna_core.parser import parse_manifold

_HERE = os.path.dirname(os.path.abspath(__file__))
_BENCHMARK_CML = os.path.join(_HERE, "fixtures", "benchmark.cml")


def _server(fixture_connector, *derived_blocks: str) -> ManifoldServer:
    with open(_BENCHMARK_CML) as f:
        cml = f.read() + "\n" + "\n".join(derived_blocks) + "\n"
    return ManifoldServer(parse_manifold(cml), fixture_connector)


# ── math channel: the homogeneous-linear classifier (pure, no data) ──────────────────────────
@pytest.mark.parametrize("formula,is_linear", [
    ("revenue - orders", True),           # difference of atoms
    ("revenue + orders", True),           # sum of atoms
    ("-revenue", True),                   # negation
    ("revenue * 2", True),                # scalar coefficient (right)
    ("3 * revenue", True),                # scalar coefficient (left)
    ("revenue / 100", True),              # scalar divisor
    ("revenue - orders * 2", True),       # composed homogeneous-linear
    ("revenue + 5", False),               # additive constant OFFSET breaks sum-fertility
    ("revenue / orders", False),          # data / data — a ratio, not linear
    ("revenue * orders", False),          # data * data — a product, not linear
    ("100 / revenue", False),             # scalar / data — not linear
    ("100", False),                       # a bare constant is not homogeneous
])
def test_homogeneous_linear_classifier(fixture_connector, formula, is_linear):
    """The symbolic gate is sound and conservative: only genuinely additive forms pass."""
    import ast
    m = _server(fixture_connector, f"DERIVED probe = {formula}").m
    assert _homogeneous_linear(ast.parse(formula, mode="eval"), m) is is_linear


# ── VERIFIED (math): reduce-path ≡ recompute-path for all data, no data touched ─────────────
def test_linear_combo_verified_timeless(fixture_connector):
    """A declared linear combination under `sum` is VERIFIED by symbolic proof — timeless
    (attestation None), lineages carried from the declaration."""
    s = _server(fixture_connector,
                "DERIVED net = revenue - orders\n    FAMILY {\n        sum FERTILE { calendar }\n    }")
    before = s.engine.con.fetch_count
    adjudicate(s)                                        # adjudication alone (publish also builds witnesses)
    lic = s.m.derived["net"].family["sum"].license
    assert lic.verdict == VERIFIED
    assert lic.attestation is None                       # timeless — no watermark
    assert lic.lineages == frozenset({"calendar"})
    assert s.engine.con.fetch_count == before, "math channel must not touch the connector"


def test_scalar_scaling_verified(fixture_connector):
    """The scalar-operand rule reaches the adjudicator: `revenue / 100` is VERIFIED-fertile."""
    s = _server(fixture_connector,
                "DERIVED scaled = revenue / 100\n    FAMILY {\n        sum FERTILE { calendar store_geo }\n    }")
    s.publish()
    lic = s.m.derived["scaled"].family["sum"].license
    assert lic.verdict == VERIFIED
    assert lic.lineages == frozenset({"calendar", "store_geo"})


# ── CONTRADICTED (data): publish fails closed, counterexample named ─────────────────────────
def test_ratio_along_sum_contradicted_fails_closed(fixture_connector):
    """A ratio declared sum-fertile is refuted by the attested data: publish raises Contradiction
    (the manifold does not publish) and names a counterexample cell."""
    s = _server(fixture_connector,
                "DERIVED aov = revenue / orders\n    FAMILY {\n        sum FERTILE { calendar }\n    }")
    with pytest.raises(Contradiction) as ei:
        s.publish()
    e = ei.value
    assert e.derived == "aov" and e.member == "sum" and e.lineage == "calendar"
    assert e.counterexample["reduce"] != e.counterexample["recompute"]
    assert "fails closed" in str(e).lower()


# ── UNTESTABLE: recorded, visible, never exercised ──────────────────────────────────────────
def test_non_replayable_reducer_untestable(fixture_connector):
    """A reducer the data channel cannot replay (holistic `median`) and math cannot verify is
    UNTESTABLE — recorded on authored authority, attestation None."""
    s = _server(fixture_connector,
                "DERIVED nm = revenue - orders\n    FAMILY {\n        median FERTILE { calendar }\n    }")
    s.publish()
    lic = s.m.derived["nm"].family["median"].license
    assert lic.verdict == UNTESTABLE and lic.attestation is None


# ── CORROBORATED: math too weak, data agrees, watermarked ───────────────────────────────────
def test_corroborated_is_watermarked(fixture_connector):
    """`revenue * orders / orders` is data-equal to `revenue` but the conservative math channel will
    not prove it (a product of two data atoms). The data channel corroborates it and watermarks the
    license to the attestation (so re-attestation re-adjudicates)."""
    s = _server(fixture_connector,
                "DERIVED rr = revenue * orders / orders\n    FAMILY {\n        sum FERTILE { calendar }\n    }")
    s.publish()
    lic = s.m.derived["rr"].family["sum"].license
    assert lic.verdict == CORROBORATED
    assert lic.attestation and lic.attestation.startswith("attest:")


# ── re-attestation: CORROBORATED → CONTRADICTED when new data carries a counterexample ──────
def _bespoke_server(rows):
    """A minimal controllable warehouse: sales(day, amt, oflag) + a calendar(day, month) edge, with
    rev=sum(amt), ofl=sum(oflag). `rr = rev * ofl / ofl` is data-equal to rev while every day's ofl
    is non-zero (CORROBORATED); an oflag=0 day makes rr@day = rev*0/0 = NaN and refutes it."""
    import duckdb
    from columna_core import DuckDBConnector
    con = duckdb.connect()
    con.execute("CREATE TABLE sales(day VARCHAR, amt DOUBLE, oflag BIGINT)")
    con.executemany("INSERT INTO sales VALUES (?,?,?)", rows)
    days = sorted({r[0] for r in rows})
    con.execute("CREATE TABLE cal(day VARCHAR, month VARCHAR)")
    con.executemany("INSERT INTO cal VALUES (?,?)", [(d, d[:7]) for d in days])
    cml = """
MANIFOLD flip VERSION 1
UNIVERSE txn = day
LEVEL day   = day BASE
LEVEL month = month
EDGE day -> month ALONG calendar VIA cal(day, month)
MEASURE rev ON txn FROM sales AS sum(amt)
MEASURE ofl ON txn FROM sales AS sum(oflag)
DERIVED rr = rev * ofl / ofl
    FAMILY {
        sum FERTILE { calendar }
    }
"""
    return ManifoldServer(parse_manifold(cml), DuckDBConnector(con))


def test_reattestation_flips_corroborated_to_contradicted():
    """Two months of clean data corroborate `rr`; re-attesting with an oflag=0 row refutes it and
    the fresh publish fails closed — the CORROBORATED license does not survive its attestation."""
    clean = [("2024-01-01", 100.0, 1), ("2024-01-02", 200.0, 1),
             ("2024-02-01", 300.0, 1), ("2024-02-02", 400.0, 1)]
    s = _bespoke_server(clean)
    s.publish()
    assert s.m.derived["rr"].family["sum"].license.verdict == CORROBORATED

    # re-attest: a day whose orders-flag sums to zero — rr = rev*0/0 is undefined there
    reattested = clean + [("2024-01-03", 500.0, 0)]
    s2 = _bespoke_server(reattested)
    with pytest.raises(Contradiction) as ei:
        s2.publish()
    assert ei.value.derived == "rr" and ei.value.lineage == "calendar"


# ── idempotence: adjudicating twice yields the same verdicts (within an attestation) ────────
def test_adjudicate_is_idempotent(fixture_connector):
    s = _server(fixture_connector,
                "DERIVED net = revenue - orders\n    FAMILY {\n        sum FERTILE { calendar }\n    }")
    r1 = adjudicate(s)
    r2 = adjudicate(s)
    assert r1 == r2 == {"net": {"sum": "verified"}}

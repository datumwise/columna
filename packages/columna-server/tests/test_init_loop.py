"""
test_init_loop.py — the `columna init` loop, HERMETIC against the scripted provider (CP-2 artifact 3).

Asserts HARNESS behavior only — state transitions, wall rejections, mark bookkeeping, aperture call
shapes — never the scripted mind's judgment quality (that is the eval suite's jurisdiction, against
ratified ground truth). A real model is not wired here, by design.
"""
import duckdb
import pytest

from columna_core import DuckDBConnector, PolarityViolation, PUBLISHED, PROPOSED_STATE
from columna_core.draft import ACCEPTED, STRUCK
from columna_server.init import InitLoop, ScriptedProvider, LoopViolation


def _aperture():
    con = duckdb.connect()
    con.execute("CREATE TABLE tx AS SELECT * FROM (VALUES (1,10.0),(2,5.0)) t(store_id, amount)")
    con.execute("CREATE TABLE stores AS SELECT * FROM (VALUES (1,'north')) t(store_id, region)")
    return DuckDBConnector(con)


def test_loop_runs_generate_review_revise_publish_hermetically():
    prov = ScriptedProvider([
        # generation 1 (propose): two closures
        [{"kind": "measure", "body": "MEASURE revenue ON sales FROM tx AS sum(amount)"},
         {"kind": "measure", "body": "MEASURE bogus ON sales FROM tx AS sum(amount)"}],
        # generation 2 (revise): address the marks — a NEW closure only (never the struck one)
        [{"kind": "edge", "body": "EDGE store -> region ALONG geo VIA stores(store_id, region)"}],
    ])
    loop = InitLoop(_aperture(), prov, "sales_init")
    loop.generate()
    assert loop.draft.state == PROPOSED_STATE and len(loop.draft.proposals) == 2
    loop.review({0: ACCEPTED, 1: STRUCK})              # (human) keep revenue, strike bogus
    loop.revise()
    loop.review({2: ACCEPTED})                         # (human) accept the new edge
    loop.declare(); loop.attest()                      # (human) authority + attestation
    cml = loop.publish()                               # (human) the author's act
    assert loop.draft.state == PUBLISHED
    assert "MEASURE revenue" in cml and "EDGE store" in cml
    assert "bogus" not in cml                          # struck -> dropped from the artifact


def test_loop_rejects_a_scripted_fertility_opening():
    # the mind tries to open a door; the harness cannot build one (wall layer 1, through the loop).
    prov = ScriptedProvider([[{"kind": "derived", "body": "DERIVED r = a / b FERTILE { sum }",
                               "opens_fertility": True}]])
    loop = InitLoop(_aperture(), prov, "m")
    with pytest.raises(PolarityViolation):
        loop.generate()


def test_revise_may_not_re_propose_a_struck_declaration():
    prov = ScriptedProvider([
        [{"kind": "measure", "body": "MEASURE bogus ON u FROM tx AS sum(amount)"}],
        [{"kind": "measure", "body": "MEASURE bogus ON u FROM tx AS sum(amount)"}],   # re-proposes the struck one
    ])
    loop = InitLoop(_aperture(), prov, "m")
    loop.generate()
    loop.review({0: STRUCK})
    with pytest.raises(LoopViolation):
        loop.revise()


def test_loop_reads_only_through_the_aperture():
    # the provider is handed the aperture (typed catalog/profile/sample); it has no other data path.
    captured = {}

    class Probe(ScriptedProvider):
        def propose(self, aperture, draft):
            captured["catalog"] = aperture.catalog()   # a typed read, the only way in
            return []

    loop = InitLoop(_aperture(), Probe([[]]), "m")
    loop.generate()
    assert {t["table"] for t in captured["catalog"]} == {"tx", "stores"}

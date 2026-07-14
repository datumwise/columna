"""
test_nonexistent_measure.py — core-level unknown-measure guarantee (audit v0.2 §D item 2).

The nonexistent-measure case is covered END-TO-END by columna-server's `test_agent.py` (an
agent/REPL scenario). This adds the columna-core PLANNER-LEVEL guarantee, independent of the
server/agent layer, so the core cannot silently regress into serving a number for a name that does
not exist.

CP-1 question for Huayin: if agent-level coverage was intended as the ONLY coverage for this case,
this file comes out — say so and it is removed.
"""
from columna_core.disclosure_wire import wire_frame


def test_unknown_measure_is_error_not_silent(fixture_server):
    """Asking for a measure that isn't in the manifold yields an `error` outcome (reason `unknown`)
    naming the unknown column — never a silently served number."""
    fr = fixture_server.frame("region").column("x", "nonexistent_measure").run()
    w = wire_frame(fr)
    assert w["outcome"] == "error"
    nr = (w["columns"][0].get("no_result") or {})
    assert nr.get("reason") == "unknown"
    assert "nonexistent_measure" in (nr.get("detail") or "")

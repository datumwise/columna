"""Step 0 of the jurisdiction repair — P1-19: an explicitly named Manifold GOVERNS the request.

The governing invariant, ruled 2026-09-01:

    The realization must answer the canonical request that was actually submitted.

Ruling v0.2 §9: "Binding may supply omitted context. It may not override explicit canonical meaning."
§10, in as many words: "If `FROM M` names a governed Manifold and the request is otherwise valid,
realization must address `M`" and "A surface-bound Manifold may not silently replace an explicitly
named different Manifold."

Before this, `stmt.from_manifold` had NO CONSUMER anywhere in the tree. The parser preserved it,
`desugar` carried it, `render_canonical` re-emitted it — and every statement-taking tool resolved from
the `manifold_id` ARGUMENT alone. `FROM other SELECT …` served from the bound manifold, and so did
`FROM no_such_manifold`. The wire was not lying — it echoed the manifold it actually served — but the
statement's own explicit naming had no effect on what that was.

The two failure channels are deliberately distinct and both are pinned below:
  * an unresolvable `manifold_id` ARGUMENT is the caller addressing the tool wrongly — STRUCTURAL,
    raised through the MCP-error channel, pre-adjudication;
  * an unresolvable Manifold named INSIDE the request is a defect of the request — §10 "Explicit
    unknown Manifold ... **Invalid**" — so it rides the wire.
"""
import json
import os

import pytest

import columna_server
from columna_server.store import ManifoldStore
from columna_server.tools import (
    ToolInputError,
    check_frame_query,
    execute_frame_query,
    explain_statement,
)
from conftest import write_lowering_receipt

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")
_Q = "SELECT revenue, orders AT {region*cal.quarter}"


def _artifact(src_id, src_ver):
    return {
        "publication_format_version": "1",
        "ref": {"manifold_id": src_id, "version": src_ver},
        "logical": {"declarations": [
            {"kind": "universe", "name": "u", "body": {"basis": "events", "anchor": "keys"}}]},
        "authority": {"published_by": "Huayin", "published_at": "2026-08-13T00:00:00Z",
                      "ratifications": {"u": {"ratified_by": "Huayin", "at": "t",
                                              "fingerprint": "fp", "fingerprint_version": "elf-1"}}},
    }


@pytest.fixture
def store(tmp_path) -> ManifoldStore:
    """Two governed publications with DIFFERENT logical ids, both realizable here, so 'which one
    served' is observable rather than inferred."""
    src_cml = open(os.path.join(_CASCADIA, "manifold.cml")).read().splitlines()
    warehouse = os.path.join(_CASCADIA, "warehouse")

    def _write(folder, source_line, artifact):
        d = tmp_path / folder
        d.mkdir()
        (d / "manifold.cml").write_text("\n".join(src_cml[:1] + [source_line] + src_cml[1:]) + "\n")
        (d / "data.toml").write_text(
            f'[manifold]\nname = "{folder}"\n[connector]\ntype = "duckdb"\nwarehouse = "{warehouse}"\n')
        (d / "governed-publication.json").write_text(json.dumps(artifact))
        write_lowering_receipt(d, artifact["ref"]["manifold_id"], artifact["ref"]["version"])

    _write("retail_v13", "SOURCE_MANIFOLD retail VERSION 1.3.0", _artifact("retail", "1.3.0"))
    _write("boutique_v1", "SOURCE_MANIFOLD boutique VERSION 1.0.0", _artifact("boutique", "1.0.0"))
    return ManifoldStore(str(tmp_path))


# ── §10 · omitted FROM: the surface binding is an AUTHORIZED default ───────────────────────────────
def test_omitted_from_proceeds_under_the_surface_binding(store):
    wire = execute_frame_query(store, "retail", _Q)
    assert wire["outcome"] in ("serve", "disclose")
    assert wire["manifold_id"] == "retail"


def test_from_naming_the_bound_manifold_is_the_same_request(store):
    bound = execute_frame_query(store, "retail", _Q)
    named = execute_frame_query(store, "retail", f"FROM retail {_Q}")
    assert named["outcome"] == bound["outcome"]
    assert named["manifold_id"] == bound["manifold_id"] == "retail"


# ── §10 · explicit FROM GOVERNS, and the binding never silently replaces it ────────────────────────
def test_an_explicitly_named_manifold_governs_and_is_disclosed(store):
    """THE ROW. Bound to `retail`, the statement names `boutique`: `boutique` must serve, and the wire
    must say so — never `retail`'s answer under `retail`'s name."""
    wire = execute_frame_query(store, "boutique", f"FROM boutique {_Q}")
    direct = execute_frame_query(store, "boutique", _Q)
    redirected = execute_frame_query(store, "retail", f"FROM boutique {_Q}")
    assert redirected["manifold_id"] == "boutique"
    assert redirected["outcome"] == direct["outcome"] == wire["outcome"]


def test_the_bound_manifold_cannot_answer_for_a_differently_named_one(store):
    """The falsifiable form of the same property: the redirected answer must NOT be the bound
    manifold's answer wearing the bound manifold's name."""
    bound = execute_frame_query(store, "retail", _Q)
    redirected = execute_frame_query(store, "retail", f"FROM boutique {_Q}")
    assert redirected["manifold_id"] != bound["manifold_id"]


@pytest.mark.parametrize("tool", [execute_frame_query, check_frame_query])
def test_plan_and_execute_agree_about_which_manifold_governs(store, tool):
    wire = tool(store, "retail", f"FROM boutique {_Q}")
    assert wire["manifold_id"] == "boutique"


def test_explain_also_honours_the_named_manifold(store):
    wire = explain_statement(store, "retail", f"FROM boutique {_Q}")
    assert wire["manifold_id"] == "boutique"


# ── §10 · explicit UNKNOWN Manifold is a defect of the REQUEST, not of the call ────────────────────
def test_an_explicitly_named_unknown_manifold_does_not_serve(store):
    """It used to serve — from whatever the surface happened to be bound to. §10 makes it Invalid;
    until the wire moods are ruled (v0.2 §13, Step 6) it rides the transitional `error` mood under
    its own reason string."""
    wire = execute_frame_query(store, "retail", f"FROM no_such_manifold {_Q}")
    assert wire["outcome"] == "error"
    assert wire["error"]["reason"] == "from_manifold_unresolvable"
    assert "no_such_manifold" in wire["error"]["detail"]
    assert not wire.get("columns")


def test_the_unknown_named_manifold_is_a_WIRE_result_not_a_structural_error(store):
    """Jurisdiction: the request is at fault, so the caller gets an adjudicated wire — contrast the
    next test, where the CALL is at fault and the structural channel fires instead."""
    wire = check_frame_query(store, "retail", f"FROM no_such_manifold {_Q}")
    assert wire["outcome"] == "error" and wire["error"]["reason"] == "from_manifold_unresolvable"


def test_an_unknown_manifold_ARGUMENT_is_still_structural_and_pre_adjudication(store):
    """Unchanged by this repair, and pinned so the two channels cannot be merged later."""
    with pytest.raises(ToolInputError, match="unknown manifold_id|publication_not_found"):
        execute_frame_query(store, "no_such_manifold", _Q)

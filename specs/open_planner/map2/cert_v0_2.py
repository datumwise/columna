#!/usr/bin/env python3
"""MAP-2 · the v0.2 certificate library — builds schema-conformant plan certificates and rule
certificates (certificate_cargo_schema_v0_2.md). Shared by emit_c1_v0_2.py (steps 1-2) and pilot_c2.py
(step 3). No engine edits; pure construction + digests.

Channels (schema §2): SEMANTIC = call-invariant (S1..S10); MECHANICAL = per-run (M1..M4). The digest of
a semantic channel is SHA-256 over its sort-keyed canonical JSON (schema §6, CC's adopted answer).
"""
from __future__ import annotations

import ast
import hashlib
import json

import ibis
from ibis_substrait.compiler.core import SubstraitCompiler


def sha256_canon(obj) -> str:
    """SHA-256 over sort-keyed canonical JSON (UTF-8, compact). The one digest algorithm (schema §6)."""
    return "sha256:" + hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


# ---- S2 model: the chain anchor ------------------------------------------------------------------

def model_field(m) -> dict:
    """S2 — Manifold identity + adjudication digest (a hash of the publish-time adjudicated structure:
    the corroborated edges with their verdicts, the measures, the universes)."""
    edges = sorted((e.frm, e.to, e.lineage, getattr(e, "evidence", None)) for e in m.edges)
    universes = sorted((u, sorted(map(str, v.base_dimensions))) for u, v in m.universes.items())
    adjudicated = {"edges": edges, "measures": sorted(m.measures.keys()), "universes": universes}
    return {"name": m.name, "version": m.version, "adjudication_digest": sha256_canon(adjudicated)}


# ---- S3 ask --------------------------------------------------------------------------------------

def ask_field(frameql: str) -> dict:
    """S3 — canonical ask text + parse digest (over the parsed statement's canonical structure). V6:
    the text must parse on the shipped envelope grammar; parse_statement raising is a schema failure."""
    from columna_core.envelope import parse_statement
    stmt = parse_statement(frameql)                       # V6 — attested syntax only
    canon = {"anchor": list(getattr(stmt, "anchor", ())),
             "select": [str(s) for s in getattr(stmt, "select", getattr(stmt, "columns", []))],
             "where": list(getattr(stmt, "where", []) or []),
             "from": getattr(stmt, "from_manifold", None)}
    return {"text": frameql, "parse_digest": sha256_canon(canon)}


# ---- S4 plan: the IR node list + digest -----------------------------------------------------------

def plan_field(nodes: list[dict]) -> dict:
    """S4 — the IR in canonical serialization (node list) + its digest. `nodes` is the ordered node
    list with each node's id and payload; the digest is over the canonical node list."""
    return {"nodes": nodes, "digest": sha256_canon(nodes)}


# ---- S9 lowering map: RelRoot-relative child-index paths ------------------------------------------

def walk_rels(rel, path=()):
    """Yield (child-index path, rel_kind) for every Rel in a Substrait plan tree, root-relative."""
    kind = rel.WhichOneof("rel_type")
    yield list(path), kind
    sub = getattr(rel, kind)
    if hasattr(sub, "input") and sub.HasField("input"):
        yield from walk_rels(sub.input, path + (0,))
    if hasattr(sub, "left") and sub.HasField("left"):
        yield from walk_rels(sub.left, path + (0,))
    if hasattr(sub, "right") and sub.HasField("right"):
        yield from walk_rels(sub.right, path + (1,))


# Substrait Rel kind -> the IR node it realizes (the D1 map, in the lowering direction).
_REL_NODE = {"aggregate": "REDUCE", "join": "TRANSPORT", "read": "CARVE",
             "project": "COLUMN", "filter": "CARVE", "sort": "ORDER", "fetch": "LIMIT"}


def lowering_map_field(plan) -> dict:
    """S9 — node-span map in child-index path notation, derived from the ACTUAL produced plan tree.
    Every node here lowered (no stay_home in C1/C2); a sketch/median plan would tag stay_home."""
    root = plan.relations[0].root.input
    spans = []
    for path, kind in walk_rels(root):
        spans.append({"rel_span": path, "rel_kind": kind,
                      "node": _REL_NODE.get(kind, "?"), "stay_home": False})
    return {"notation": "RelRoot-relative child-index path", "spans": spans}


# ---- the rule certificate (schema §4b) -----------------------------------------------------------

def rule_certificate(rule_id, rule_statement, backend, oracle_run, perimeter) -> dict:
    """§4b — the referenceable per-(rule × backend) proof M1 points at.

    DIGEST BASIS (a v0.2 refinement flagged to the desk under §6's open 'rule-cert versioning'): the
    digest content-addresses the rule's IDENTITY — {rule_id, rule_statement, backend BAND, perimeter} —
    NOT the mechanical oracle_run/date. Two consequences, both wanted: (1) re-proving the same rule on
    the same backend band yields the SAME ref (the amortization economics — mint once, point forever);
    (2) a plan cert's S5/M1 ref is byte-stable, so V3 survives (a proof-run date can't leak into the
    semantic channel through the ref). The oracle_run rides as the attached proof, not in the address."""
    identity = {"rule_id": rule_id, "rule_statement": rule_statement, "backend": backend,
                "perimeter": perimeter, "schema": "urn:columna:rule-certificate:v1"}
    digest = sha256_canon(identity)
    return {**identity, "oracle_run": oracle_run, "digest": digest}


# ---- the plan certificate (S1..S10 + M1..M4) -----------------------------------------------------

def plan_certificate(*, model, ask, plan_ir, obligations, edge_attestations, face_spends,
                     disclosure_projection, lowering_map, perimeter,
                     m1, m2, m3, m4=None) -> dict:
    """A full v0.2 plan certificate. Returns (certificate, semantic_channel) — the semantic channel is
    the byte-stable object the V3 diff runs against and the digest is computed over."""
    semantic = {
        "S1_schema_version": "columna-certificate/1",
        "S2_model": model,
        "S3_ask": ask,
        "S4_plan": plan_ir,
        "S5_obligations": obligations,
        "S6_edge_attestations": edge_attestations,
        "S7_face_spends": face_spends,
        "S8_disclosure_projection": disclosure_projection,
        "S9_lowering_map": lowering_map,
        "S10_perimeter": perimeter,
    }
    semantic_digest = sha256_canon(semantic)
    mechanical = {"M1_lowering_attestation": m1, "M2_backend": m2, "M3_oracle_run": m3,
                  "M4_serving": m4 or {"note": "n/a — pilot, not a serve"}}
    certificate = {"urn": "urn:columna:certificate:v1",
                   "semantic_channel_digest": semantic_digest,
                   "semantic": semantic, "mechanical": mechanical}
    return certificate, semantic


# ---- a tiny Substrait producer helper shared by the pilots ---------------------------------------

def compile_substrait(expr):
    plan = SubstraitCompiler().compile(expr)
    v = plan.version
    return plan, f"{v.major_number}.{v.minor_number}.{v.patch_number}"

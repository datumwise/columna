"""
columna_server.tools — the five read-only tools, as pure functions over a ManifoldStore.

Each returns a plain dict (the wire contract). query/explain serialize through
columna_core.disclosure_wire, so the MCP surface returns exactly the Python API's truth (ADR-032
D8, one contract). No SQL, no write path. Structural failures (unknown manifold/measure, malformed
query) raise ToolInputError; analytical outcomes (serve/disclose/clarify/refuse/error) are DATA in
the wire dict.
"""
from __future__ import annotations

from typing import Optional

from columna_core import disclosure_wire as dw

from .frameql import FrameQLSyntaxError
from .provider import SupportsExecutionDiagnostics
from .registry import NotRealizableHere, PublicationNotFound
from .store import (
    ENTRY_GOVERNED,
    ENTRY_LEGACY,
    ENTRY_SOURCE_REFERENCED_INCOMPLETE,
    ManifoldStore,
)

#: LoadCondition.kind (a registry exception class name) → the STABLE public condition code exposed in
#: the v3 catalog. Only these codes cross the wire — never raw details, parser text, paths, or reprs.
_CONDITION_CODE = {
    "PublicationArtifactMissing": "publication_artifact_missing",
    "PublicationArtifactInvalid": "publication_artifact_invalid",
    "UnsupportedPublicationFormat": "unsupported_publication_format",
    "RealizationIdentityMismatch": "realization_identity_mismatch",
}

#: entry_kind → the public catalog `kind` (source-referenced-but-incomplete surfaces as
#: "authority_incomplete" publicly — it references a publication origin but lacks the authority).
_PUBLIC_KIND = {
    ENTRY_GOVERNED: "governed",
    ENTRY_LEGACY: "legacy",
    ENTRY_SOURCE_REFERENCED_INCOMPLETE: "authority_incomplete",
}

CONTRACT_VERSION = dw.CONTRACT_VERSION


def _fetch_count(provider) -> Optional[int]:
    """The provider's cumulative backend-fetch counter, or None if it exposes no such diagnostic.

    None is NOT zero: it means this provider does not expose the Core `fetches` diagnostic, so the
    server emits no `fetches_delta`. Only a provider that reports `fetches` gets the (Core-specific)
    `fetches_delta` wire annotation — no fetch concept is fabricated for providers that lack one.
    """
    if isinstance(provider, SupportsExecutionDiagnostics):
        return provider.execution_diagnostics().get("fetches")
    return None

# evidence grade (model.py) -> wire provenance vocabulary (WP-2.2 ruling C)
_PROVENANCE = {"proven": "data_attested", "declared": "declared",
               "inferred_sample": "inferred", "inferred_docs": "inferred"}


class ToolInputError(ValueError):
    """A structural input error (unknown manifold/measure, malformed query) — surfaced by the MCP
    layer as an error result, distinct from an analytical `error` outcome carried in the wire."""


def _resolve(store: ManifoldStore, manifold_id: str, version: Optional[str] = None):
    """Governed-first public resolution (S2.2b-1) → ``(LoadedManifold, resolved_ref)``.

    ``resolved_ref`` is the concrete governed ``ManifoldRef`` (disclose its version) or ``None`` for a
    compatibility runtime (unversioned). Registry serving conditions are surfaced through the STRUCTURAL
    MCP-error channel (raise → MCP error result), distinct from an analytical `error` wire outcome:
      * ``publication_not_found`` — no such governed publication (unknown id/version), or an explicit
        version on a non-governed id;
      * ``not_realizable_here``   — the governed publication exists but has no provider realization here.
    Both are pre-adjudication: analytical adjudication begins only after resolution succeeds.
    """
    try:
        return store.resolve_public(manifold_id, version)
    except PublicationNotFound:
        v = f"@{version}" if version else ""
        raise ToolInputError(
            f"publication_not_found: no governed publication '{manifold_id}{v}' "
            f"(governed lineages: {store.governed_ids()}; compatibility runtimes: {store.ids()})")
    except NotRealizableHere as e:
        raise ToolInputError(
            f"not_realizable_here: governed publication '{e}' exists but has no provider realization "
            f"in this installation")
    except KeyError:
        raise ToolInputError(f"unknown manifold_id '{manifold_id}' (have {store.ids()})")


def _disclose(result: dict, manifold_id: str, ref) -> dict:
    """Make the resolved governed publication observable (S2.2b-1): echo ``manifold_id`` and, for an
    artifact-backed governed publication, the concrete resolved ``manifold_version``. A compatibility
    (legacy / authority-incomplete) runtime is unversioned — ``manifold_version`` is ABSENT, never
    fabricated as `"legacy"`/`"unknown"` or a source-ref claim promoted into a governed version."""
    result["manifold_id"] = manifold_id
    if ref is not None:
        result["manifold_version"] = ref.version
    return result


def _render_ref(ref, levels=frozenset()) -> str:
    # C-2 insulation (§2b, CP-3): render predicates LOGICALLY — a PHYSICAL table qualifier NEVER
    # crosses describe (the shipped leak was `stores.opened_date`; the standing test bans any table.column).
    # OF-9 (case-demo c): a `<level>.<attr>` reference is a DECLARED LOGICAL attribute — both parts are
    # logical, so it renders WITH its qualifier (`store.opened`). A dotted ref whose head is NOT a declared
    # level is an un-migrated physical residue → drop the qualifier (the shipped guarantee).
    if ref.is_literal:
        return str(ref.value)
    if ref.table is not None and ref.table in levels:
        return f"{ref.table}.{ref.column}"
    return str(ref.column)


def _render_predicate(pred, levels=frozenset()) -> Optional[str]:
    if pred is None or not pred.comparisons:
        return None
    return " AND ".join(f"{_render_ref(c.left, levels)} {c.op} {_render_ref(c.right, levels)}"
                        for c in pred.comparisons)


# --- tool 1 ---------------------------------------------------------------------------------
def list_manifolds(store: ManifoldStore) -> dict:
    """The installation catalog (contract v3): governed publication LINEAGES + explicitly classified
    compatibility runtimes. A governed row is one lineage per ``manifold_id`` with its concrete
    ``versions[]`` and ``latest_version`` (publication facts) and per-version ``realizable`` (an
    installation fact — distinct from publication existence). Legacy and authority-incomplete runtimes
    are separate rows keyed by ``runtime_id``; the latter carries its ``source_ref`` (a runtime CLAIM of
    origin, not governed identity) and any stable deployment ``conditions``. Presentation/read-model
    detail (measures, universes, …) lives on ``describe``, never here. Deterministic order:
    governed (by manifold_id) → legacy (by runtime_id) → authority-incomplete (by runtime_id)."""
    realizable = store.realizable_refs()
    conditions_by_id: dict[str, list[str]] = {}
    for c in store.conditions():
        code = _CONDITION_CODE.get(c.kind)
        if code is not None:
            conditions_by_id.setdefault(c.manifold_id, []).append(code)

    # governed lineages — registry.list() is already sorted by (manifold_id, ascending semver)
    versions_by_id: dict[str, list[dict]] = {}
    for ref in store.registry().list():
        versions_by_id.setdefault(ref.manifold_id, []).append(
            {"version": ref.version, "realizable": ref in realizable})
    governed = [
        {"manifold_id": mid, "kind": "governed",
         "latest_version": store.registry().latest(mid),   # publication fact — highest semver, always
         "versions": versions_by_id[mid]}
        for mid in sorted(versions_by_id)
    ]

    # compatibility runtimes — legacy first, then authority-incomplete; each sorted by runtime_id
    legacy, incomplete = [], []
    for lm in store.all():
        if lm.entry_kind == ENTRY_GOVERNED:
            continue
        row: dict = {"runtime_id": lm.manifold_id, "kind": _PUBLIC_KIND[lm.entry_kind]}
        if lm.entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE and lm.source_ref is not None:
            row["source_ref"] = {"manifold_id": lm.source_ref.manifold_id,
                                 "version": lm.source_ref.version}
        codes = conditions_by_id.get(lm.manifold_id)
        if codes:                                          # omit when empty (optional-field convention)
            row["conditions"] = codes
        (incomplete if lm.entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE else legacy).append(row)
    legacy.sort(key=lambda r: r["runtime_id"])
    incomplete.sort(key=lambda r: r["runtime_id"])

    return {"contract_version": CONTRACT_VERSION, "manifolds": governed + legacy + incomplete}


# --- tool 2 ---------------------------------------------------------------------------------
def describe_manifold(store: ManifoldStore, manifold_id: str, version: Optional[str] = None) -> dict:
    lm, ref = _resolve(store, manifold_id, version)
    m = lm.manifold
    from columna_core import (describe_derived, describe_universe, describe_hierarchy)
    # C-2 insulation (§2b, CP-3): dimensions no longer emit `realized_by` (a physical identifier).
    # Attributes emit their LOGICAL names only (case-demo c) — the physical binding stays map-side.
    dimensions = [{"level": lv.name, "is_base": lv.is_base, "description": lv.description,
                   "attributes": [a for a, _ in lv.attributes]} for lv in m.levels.values()]
    edges = [{"frm": e.frm, "to": e.to, "lineage": e.lineage} for e in m.edges]
    # C-1 (D1, CP-3): universes carry basis + absence semantics + the basis License (predicate rendered
    # logically); hierarchies get their own describe block with the kernel-reused License.
    # The `asserts` block was REMOVED in 0.13.0 (ASSERT retirement, ruling 2026-07-26) — the first
    # REMOVAL from this wire; `contract_version` stays "1" (pre-broadcast, zero consumers), and the
    # 0.13.0 release note states the removal explicitly rather than letting it drift.
    _lv = frozenset(m.levels)
    universes = [describe_universe(u, _render_predicate(u.predicate, _lv)) for u in m.universes.values()]
    hierarchies = [describe_hierarchy(h) for h in m.hierarchies]
    # signature addressing (D1): each measure carries its universe qualifier as a STRUCTURED field (a
    # dotted address string would be indistinguishable from a physical `table.column` under the §2b test;
    # the address is (universe, name), and the consumer renders it). Per-member operator props: describe_measure.
    measures = [{"name": mc.name, "family": list(mc.family), "universe": mc.universe,
                 "description": mc.description} for mc in m.measures.values()]
    derived = [describe_derived(m, name) for name in m.derived]
    # RELATE on the wire (B, Huayin 2026-07-19): declared M:N relationships ride describe as DATA — an
    # agent consulting describe can warn about a category rollup BEFORE spending the query, and answer
    # "why can't I get revenue by category" from the source of truth, instead of the M:N being invisible
    # until tripped (the knowledge previously lived only in the clarify's after-the-fact detail text).
    # Logical level names + the NOTE verbatim (the "up to 3" the figure quotes IS this note) — no VIA, no
    # bridge-table name, nothing physical; the standing §2b insulation test covers relates[] by
    # construction. describe_measure untouched; contract_version stays "1" (additive, per the DESCRIPTION
    # precedent). Born with room for its future: RELATE-adjudication verdicts join these entries additively.
    # faces[] is the real additive projection (Huayin 2026-07-19): declared crossing dispositions ride
    # describe as DATA so the clarify-menu and any consulting agent see them from the source of truth.
    # Logical name + scheme + folklore ONLY — the VIA bridge is MAP-LAYER (engine-visible, never here);
    # the §2b insulation test asserts VIA stays off-wire. contract_version stays "1" (additive).
    relates = [{"frm": r.frm, "to": r.to, "note": r.detail,
                "faces": [{"name": f.name, "scheme": f.scheme, "description": f.description,
                           "driver": f.selection or None}          # the driver measure-ref; null for touch (additive)
                          for f in r.faces]}
               for r in m.non_functional]
    # published-scope display: the current serving scope — the blocked edges of refuted hierarchies.
    # (`cut`/`cut_by` stood here. They retired with ASSERT in 0.13.0, ruling 2026-07-26: the cut region's
    #  sole producer was a violated assert, so the two fields could only ever be empty. Stated in the
    #  0.13.0 release note with the `asserts` block and the universes' `attributes`.)
    ps = lm.provider.published_scope()
    scope = {"blocked_edges": [list(e) for e in sorted(ps.blocked_edges)] if ps else [],
             "blocked_by": {f"{k[0]}->{k[1]}": v for k, v in (ps.blocked_by.items() if ps else [])}}
    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
                      "dimensions": dimensions, "edges": edges, "universes": universes,
                      "hierarchies": hierarchies, "relates": relates,
                      "measures": measures, "derived": derived, "published_scope": scope},
                     manifold_id, ref)


# --- tool 3 ---------------------------------------------------------------------------------
def describe_measure(store: ManifoldStore, manifold_id: str, measure: str,
                     version: Optional[str] = None) -> dict:
    lm, ref = _resolve(store, manifold_id, version)
    m = lm.manifold
    mc = m.measures.get(measure)
    if mc is None:
        raise ToolInputError(f"unknown measure '{measure}' in manifold '{manifold_id}' "
                             f"(have {sorted(m.measures)})")
    ops = lm.provider.operators()   # OperatorSig registry (kind, is_monoid)

    from columna_core import operator_properties
    member_anchors, reducer_kind, signatures = {}, {}, {}
    for member, fm in mc.family.items():
        sig = ops.get(member)
        member_anchors[member] = {
            "blocked_lineages": sorted(fm.b_anchor.blocked_lineages),
            "order_by": fm.order_by,
            "is_monoid": (sig.is_monoid if sig else None),
            "description": fm.description,      # per-member folklore (case-demo b) — LOGICAL, flows to the wire
        }
        reducer_kind[member] = (sig.kind if sig else None)
        # D1 operator properties (registry describe): the algebraic/routing properties, no engine
        # mechanics. Addressing is the STRUCTURED (universe, measure, member) — universe on this dict,
        # measure is `measure`, member is the key — never a dotted string (§2b test would flag it).
        signatures[member] = {"operator": operator_properties(sig)}

    base_grain = sorted(m.universes[mc.universe].base_dimensions)
    return _disclose({
        "contract_version": CONTRACT_VERSION, "manifold_id": manifold_id, "measure": measure,
        "description": mc.description,       # measure folklore (case-demo b) — LOGICAL, flows to the wire
        "universe": mc.universe, "dtype": mc.logical_type,
        "family": {"root": mc.name, "members": list(mc.family), "reducer_kind": reducer_kind},
        "member_anchors": member_anchors, "signatures": signatures,
        "v_anchor": {"universe": mc.universe, "grain": base_grain},   # structured, ruling C
        "m_anchor": {"mechanism": mc.missingness, "columns": sorted(mc.m_anchor)},
        "provenance": {"measure": _PROVENANCE.get(mc.evidence, mc.evidence)},
    }, manifold_id, ref)


# --- tools 4 & 5 (the ENVELOPE wire) --------------------------------------------------------
def _syntax_error_wire(detail: str, universe: Optional[str]) -> dict:
    return {"contract_version": CONTRACT_VERSION, "outcome": "error",
            "frame": {"anchor": [], "universe": universe, "rollup_severity": "none", "disclosures": []},
            "columns": [], "error": {"reason": "frameql_syntax", "detail": detail}}


def execute_frame_query(store: ManifoldStore, manifold_id: str, frameql: str,
                        version: Optional[str] = None) -> dict:
    """Execute a FrameQL ENVELOPE statement (`SELECT <series> AT {anchor} [WHERE][HAVING][ORDER BY]
    [LIMIT]`) over real data. The terse `cols @ anchor` form is RETIRED from the wire (0.9.0 tombstone).
    Returns the four-mood wire contract annotated with `executed: true` and `fetches_delta` (the backend
    fetches this run cost) — the executing counterpart of `check_frame_query`'s zero-fetch pre-flight."""
    from columna_core.envelope import parse_statement, EnvelopeSyntaxError
    lm, ref = _resolve(store, manifold_id, version)
    before = _fetch_count(lm.provider)
    try:
        stmt = parse_statement(frameql)
        fr = lm.provider.run(stmt)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return _disclose(_syntax_error_wire(str(e), None), manifold_id, ref)
    after = _fetch_count(lm.provider)
    delta = (after - before) if (before is not None and after is not None) else None
    return _disclose(dw.wire_frame(fr, executed=True, fetches_delta=delta), manifold_id, ref)


def query(store: ManifoldStore, manifold_id: str, frameql: str, version: Optional[str] = None) -> dict:
    """DEPRECATED (0.9.x) alias for `execute_frame_query`; the wire is byte-identical. Retained for one
    release so existing clients do not break. New callers use `execute_frame_query`, which pairs by name
    with `check_frame_query` (execute vs check, the same statement)."""
    return execute_frame_query(store, manifold_id, frameql, version)


def explain_statement(store: ManifoldStore, manifold_id: str, statement: str,
                      version: Optional[str] = None) -> dict:
    """EXPLAIN an envelope statement WITHOUT executing: canonical desugared form + atom decomposition +
    dependency cone with verdicts + would-be annotation, zero backend fetches. The rich EXPLAIN payload
    (WP-FrameQL) — distinct from the query wire; a first-class MCP tool beside `query`."""
    from columna_core.envelope import parse_statement, EnvelopeSyntaxError
    lm, ref = _resolve(store, manifold_id, version)
    try:
        stmt = parse_statement(statement)
        return _disclose(lm.provider.explain(stmt), manifold_id, ref)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return _disclose({"contract_version": CONTRACT_VERSION, "executed": False, "fetches_delta": 0,
                          "outcome": "error", "error": {"reason": "frameql_syntax", "detail": str(e)}},
                         manifold_id, ref)


# --- the no-engine tools: introspection + validation, zero data -----------------------------
# Every one of these touches the manifold model only. `check_frame_query` plans without executing
# (zero backend fetches, asserted); the rest read the declared model. Logical names only (the §2b
# insulation test covers them); structural misses raise ToolInputError; an ill-posed-but-grammatical
# query is a MOOD in the wire, never an exception. There is no SQL path here or anywhere.

def check_frame_query(store: ManifoldStore, manifold_id: str, frameql: str,
                      version: Optional[str] = None) -> dict:
    """Validate a FrameQL statement against a manifold WITHOUT executing it. Parse (grammar), then plan
    (typecheck, addressability, single-universe §2c, pin laws) touching ZERO data, and return the
    would-be mood: serve/disclose/clarify/refuse/error. A syntax error is an `error` wire; a
    grammatical-but-ill-posed query returns clarify/refuse with alternatives. The cheap pre-flight —
    thinner than `explain` (no cone/atom decomposition), just: is this askable, and how would it land?"""
    from columna_core.envelope import EnvelopeSyntaxError, parse_statement
    lm, ref = _resolve(store, manifold_id, version)
    try:
        stmt = parse_statement(frameql)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return _disclose(_syntax_error_wire(str(e), None), manifold_id, ref)
    before = _fetch_count(lm.provider)
    fr = lm.provider.plan(stmt)
    after = _fetch_count(lm.provider)
    delta = (after - before) if (before is not None and after is not None) else None
    return _disclose(dw.wire_frame(fr, executed=False, fetches_delta=delta), manifold_id, ref)


def frame_ql_grammar() -> dict:
    """The FrameQL (envelope) query grammar, verbatim, with the columna-core version it came from. The
    language the ask is written in — `[EXPLAIN] [FROM m] [WITH …] SELECT <series [AS alias]>,… AT
    {anchor} [WHERE][HAVING][ORDER BY][LIMIT n [PER {dims}]]` — so a caller writes a query rather than
    guessing the shape. Touches no manifold and no data."""
    from importlib.metadata import version

    from columna_core import envelope as _env
    return {"contract_version": CONTRACT_VERSION,
            "grammar": (_env.__doc__ or "").strip(),
            "generated_by": f"columna-core {version('columna-core')}"}


def discovery(store: ManifoldStore, manifold_id: str, version: Optional[str] = None) -> dict:
    """What can be asked of this manifold, WITHOUT touching data: the measures (each with its reducer
    family and the universe/grain it lives at) and the anchors (universes with their base grain) that a
    `SELECT <measure> AT {anchor}` can name. Logical names only; the universe is resolved structurally,
    never named in a query (§2c)."""
    lm, ref = _resolve(store, manifold_id, version)
    m = lm.manifold
    measures = [{"measure": mc.name, "universe": mc.universe, "reducers": list(mc.family),
                 "grain": sorted(m.universes[mc.universe].base_dimensions),
                 "description": mc.description} for mc in m.measures.values()]
    anchors = [{"universe": u.name, "basis": u.basis,
                "grain": sorted(u.base_dimensions)} for u in m.universes.values()]
    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
                      "measures": measures, "anchors": anchors,
                      "levels": [lv.name for lv in m.levels.values()],
                      "ask_form": "SELECT <measure> AT {<levels>} — the universe is structural, "
                                  "never named"}, manifold_id, ref)


def manifold_status(store: ManifoldStore, manifold_id: str, version: Optional[str] = None) -> dict:
    """The manifold's health at a glance, WITHOUT touching data: counts (measures, universes, levels,
    hierarchies, relations, edges, derived), the published serving scope (edges blocked by refuted
    hierarchies), and the evidence standing (how many adjudicated Licenses are verified / corroborated /
    untestable)."""
    lm, ref = _resolve(store, manifold_id, version)
    m = lm.manifold
    ps = lm.provider.published_scope()
    licenses = getattr(ps, "licenses", None) if ps else None
    lic_list = list(licenses.values()) if isinstance(licenses, dict) else (list(licenses) if licenses else [])
    verdicts: dict[str, int] = {}
    for lic in lic_list:
        v = getattr(lic, "verdict", None)
        if v:
            verdicts[v] = verdicts.get(v, 0) + 1
    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
            "counts": {"measures": len(m.measures), "universes": len(m.universes),
                       "levels": len(m.levels), "hierarchies": len(m.hierarchies),
                       "relations": len(m.non_functional), "edges": len(m.edges),
                       "derived": len(m.derived)},
            "published_scope": {
                "blocked_edges": [list(e) for e in sorted(ps.blocked_edges)] if ps else []},
            "evidence": {"licenses": len(lic_list), "verdicts": verdicts}}, manifold_id, ref)


def get_evidence(store: ManifoldStore, manifold_id: str, measure: Optional[str] = None,
                 version: Optional[str] = None) -> dict:
    """The evidence behind a manifold's claims, WITHOUT touching data: each measure's declared evidence
    grade and each functional edge's, plus the adjudicated Licenses (verdict, lineages, basis,
    attestation) minted at publish. With `measure`, scoped to that measure's family and universe."""
    from columna_core.describe import license_to_dict
    lm, ref = _resolve(store, manifold_id, version)
    m = lm.manifold

    def _lic(lic: object) -> Optional[dict]:
        return license_to_dict(lic) if lic is not None else None

    if measure is not None:
        mc = m.measures.get(measure)
        if mc is None:
            raise ToolInputError(f"unknown measure '{measure}' in manifold '{manifold_id}' "
                                 f"(have {sorted(m.measures)})")
        u = m.universes[mc.universe]
        return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
                "measure": measure,
                "evidence": _PROVENANCE.get(mc.evidence, mc.evidence),
                "members": {mem: {"license": _lic(getattr(fm, "license", None))}
                            for mem, fm in mc.family.items()},
                "universe": {"name": u.name, "basis": u.basis,
                             "basis_license": _lic(getattr(u, "basis_license", None))}},
                manifold_id, ref)

    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
            "measures": {name: _PROVENANCE.get(mc.evidence, mc.evidence)
                         for name, mc in m.measures.items()},
            "edges": [{"frm": e.frm, "to": e.to, "evidence": _PROVENANCE.get(e.evidence, e.evidence)}
                      for e in m.edges],
            "hierarchy_licenses": [_lic(getattr(h, "license", None)) for h in m.hierarchies
                                   if getattr(h, "license", None)]}, manifold_id, ref)


# --- the case as an on-demand document (recapture) ---------------------------------------------------
# The three case-demo chapters ride as an ON-DEMAND MCP resource (proposal accepted 2026-07-18): a
# lean base prompt with a TRIGGERING pointer fetches the relevant chapter only when the why is needed
# (a mood to relay, a folklore/definition-history question). The chapters ship VERBATIM, byte-preserved
# — the same wire-verbatim discipline as every ratified surface. The 3-descriptor manifest tells the
# trigger WHERE to fetch: ch1 = the purpose and the requirement; ch2 = the design's reasons; ch3 = the
# behaviors and the moods.
import os as _os

_CASE_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "case")
CASE_MANIFEST = {
    "ch1": {"file": "ch1_setup.md",       "descriptor": "the purpose and the requirement"},
    "ch2": {"file": "ch2_solutioning.md", "descriptor": "the design's reasons"},
    "ch3": {"file": "ch3_live.md",        "descriptor": "the behaviors and the moods"},
}


def case_manifest() -> dict:
    """The 3-descriptor routing manifest: which chapter answers which kind of 'why'."""
    return {"chapters": {k: v["descriptor"] for k, v in CASE_MANIFEST.items()}}


def case_chapter(chapter: str) -> dict:
    """Fetch ONE case-demo chapter VERBATIM (byte-preserved) — the on-demand document. `chapter` is one
    of ch1/ch2/ch3; the descriptor routes the trigger. Structural miss raises ToolInputError."""
    entry = CASE_MANIFEST.get(chapter)
    if entry is None:
        raise ToolInputError(f"unknown case chapter '{chapter}' (have {sorted(CASE_MANIFEST)})")
    with open(_os.path.join(_CASE_DIR, entry["file"]), encoding="utf-8") as f:
        text = f.read()
    return {"chapter": chapter, "descriptor": entry["descriptor"], "text": text}

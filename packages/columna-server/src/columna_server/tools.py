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

#: LoadCondition.kind (a registry or receipt exception class name) → the STABLE public condition code
#: exposed in the v3 catalog. Only these codes cross the wire — never raw details, parser text, paths,
#: or reprs.
#:
#: The three lowering-receipt codes are an ADDITIVE vocabulary extension inside contract_version "3"
#: (ruling 2026-08-22 §3): the catalog's SHAPE is unchanged — same rows, same keys, same order — and
#: only the set of values a `conditions` entry may take grows. S2.2b-2 bumped v2→v3 for a shape
#: change; an enum extension is not one.
#:
#: EVERY LoadCondition kind the store can emit MUST appear here. `list_manifolds` skips unmapped
#: kinds, so an omission would delete a deployment condition from the catalog rather than surface it
#: — silence exactly where the store promised visibility. `test_governed_catalog` pins the mapping
#: against the store's own condition vocabulary so a future kind cannot be added without a code.
_CONDITION_CODE = {
    "PublicationArtifactMissing": "publication_artifact_missing",
    "PublicationArtifactInvalid": "publication_artifact_invalid",
    "UnsupportedPublicationFormat": "unsupported_publication_format",
    "RealizationIdentityMismatch": "realization_identity_mismatch",
    "LoweringReceiptMissing": "lowering_receipt_missing",
    "LoweringReceiptInvalid": "lowering_receipt_invalid",
    "LoweringReceiptMismatch": "lowering_receipt_mismatch",
    # C2 — a native publication shipped beside a legacy execution image. A DEPLOYMENT SHAPE
    # condition, not a defect in either file: both may be perfectly valid, and the `.cml` language
    # simply cannot express the universe law the publication carries, so nothing can attest that
    # one realizes the other. Surfaced rather than silently downgraded, because a deployment that
    # meant these to be one unit needs to be told which half is load-bearing.
    "NativePublicationNotLowerable": "native_publication_not_lowerable",
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
#: The one spelling of discovery's `ask_form`, shared by the legacy and governed paths so the two
#: cannot drift into describing the same language differently.
_ASK_FORM = ("SELECT <measure> AT {<levels>} — the universe is structural, never named")

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


#: The `logical` declaration kinds governed discovery reads. Structural names in the publication's
#: own projection — not legacy model concepts wearing governed labels.
_D_FAMILY, _D_ANCHOR, _D_UNIVERSE = "family", "anchor", "universe"


def _governed_discovery(lm, manifold_id, ref) -> dict:
    """`discovery` answered from the GOVERNED PUBLICATION, for a successor-native unit.

    THE SAME PAYLOAD SHAPE, populated from different facts — which is the whole discipline for a
    successor read-only surface: preserve the public shape where governed facts can fill it
    faithfully, never manufacture a legacy fact to satisfy the shape, and stop rather than invent
    where the shape wants a fact the governed model does not have.

    IT READS THE PUBLICATION AND NOTHING ELSE. No provider (no `operators()`, no
    `published_scope()`), no adjudication, no legacy model — `lm.publication.logical` is a
    structural projection the server already holds and already validated at ingest. That is why
    this tool is the first governed-native one: it tests the governed projection rather than the
    boundary between layers.

    EVERY GOVERNED FAMILY IS ITS OWN ROW (ruled Huayin, 2026-09-14), primitive and constructed
    alike. A constructed family — `count(revenue@sale_at)` — is a family in its own right with its
    own identity and its own askable reference, so it appears as a `measures[]` row rather than
    being folded back into its operand as a legacy "member". Row cardinality therefore rises for a
    governed unit, deliberately: hiding an independently askable analytical object to preserve a
    legacy count would be the silent disappearance this whole line of work exists to prevent.

    `reducers` IS EMPTY FOR EVERY GOVERNED ROW. The legacy field lists suffixes that are askable
    after a dot (`revenue.sum`). v2 has no members, and the governed relation that replaces them —
    a constructed family citing its operand in `formation.operands` — is NOT that relation: those
    references are not legal suffixes, and putting them here would change what the field means to
    every existing reader. The operand relation stays governed and real, and this slice adds no
    public field for it.

    `description` IS EMPTY, AND THE REASON IS NOT LAZINESS — see `_governed_description_is_absent`.

    **IT IS A v1/v2 SURFACE, AND IT REFUSES A NATIVE PUBLICATION RATHER THAN ANSWERING EMPTILY**
    (C2). Every field below is read out of the v2 projection: `components` from `anchor`
    DECLARATIONS, `anchors[].basis` and `anchors[].grain` from `universe.body`, `levels` from the
    deduplicated anchor-component tokens. **A native publication has none of those objects** — a
    Case-S anchor is derived from a constitution and structurally unwritable as a declaration, a
    native universe has no `body`, and there is no publication-global coordinate namespace for
    `levels` to be a list of.

    The default behaviour of `(lm.publication.logical or {})` on a native unit would be to return
    `measures: [], anchors: [], levels: []` — a well-formed answer meaning *this manifold has
    nothing to ask*, about a publication carrying two families and a two-constituent universe.
    That is the measured v2 failure in a different costume, so it refuses instead, in the existing
    structural channel `_legacy_model` already uses for the same class of mistake. **What a
    governed-native discovery payload should say is a real question and a separate one** — the
    recon leaves the `discovery.levels` wire list explicitly unresolved — and this slice must not
    settle it by accident.
    """
    # PRESENTLY UNREACHABLE THROUGH `discovery`, AND PLACED ANYWAY. A native unit binds no
    # provider today, so `_resolve` answers `not_realizable_here` before this function is called.
    # The guard is here because this is the site that would fabricate — the day a native unit
    # becomes servable, the failure would be a well-formed empty answer rather than an error, and
    # a fabrication guard added after the fabrication is possible is added too late.
    if getattr(lm.publication, "native", None) is not None:
        raise ToolInputError(
            f"native_publication_not_discoverable: '{manifold_id}' is a native publication, and "
            f"`discovery` answers from the v2 projection — anchor declarations, `universe.body`, "
            f"and a publication-global coordinate namespace. A native publication carries none of "
            f"those: its anchors are DERIVED from a constitution and its geometry is computed "
            f"inside one universe. Answering with empty lists would say this manifold has nothing "
            f"to ask, which is false. What this payload should carry for a native unit is not yet "
            f"decided")
    decls = (lm.publication.logical or {}).get("declarations") or []
    by_kind = {}
    for d in decls:
        by_kind.setdefault(d.get("kind"), []).append(d)

    #: anchor name -> its declared component tokens. The governed anchor's components ARE the
    #: tokens a Frame-QL `AT {…}` may name; they are not legacy `DimensionLevel` objects and
    #: nothing here claims they are.
    components = {
        d["name"]: sorted({c["name"] for c in (d.get("body") or {}).get("components") or []
                           if isinstance(c, dict) and c.get("name")})
        for d in by_kind.get(_D_ANCHOR, [])
    }

    measures = []
    for d in by_kind.get(_D_FAMILY, []):
        body = d.get("body") or {}
        measures.append({
            "measure": body.get("canonical_reference"),
            "universe": body.get("universe"),
            "reducers": [],
            "grain": components.get(body.get("constitutive_anchor"), []),
            "description": _governed_description_is_absent(),
        })

    anchors = []
    for d in by_kind.get(_D_UNIVERSE, []):
        body = d.get("body") or {}
        anchors.append({"universe": d["name"], "basis": body.get("basis"),
                        "grain": components.get(body.get("anchor"), [])})

    #: the deduplicated governed anchor-component tokens — what `AT {…}` may actually name here.
    levels = sorted({token for tokens in components.values() for token in tokens})

    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
                      "measures": measures, "anchors": anchors, "levels": levels,
                      "ask_form": _ASK_FORM}, manifold_id, ref)


def _governed_description_is_absent() -> str:
    """`""` — and the emptiness is a finding, not a gap left to fill later.

    `Family.target` is prose and `measures[].description` is prose, and THAT IS THE WHOLE OF THEIR
    RESEMBLANCE. `description` is DESCRIPTION folklore (case-demo b): additive, non-normative,
    editable without consequence. `target` is responsibility C1, the family's TARGET SPECIFICATION,
    and it is IDENTITY-BEARING — §2.2/§3.9 put it in `Σ(F)`, so changing it is a SUCCESSION, a
    different family. `resolve.py` is explicit that citing a law does not establish it.

    Publishing governed law in a folklore field would tell every reader that an edit here is
    harmless when the corresponding governed edit mints a new analytical identity. The existing
    contract already permits emptiness — `description` is a `str` defaulting to `""` — so the
    governed row says nothing rather than saying it in the wrong register. Where the target
    belongs on a public surface is a real question and a separate one."""
    return ""


# --- tool 2 ---------------------------------------------------------------------------------
def describe_manifold(store: ManifoldStore, manifold_id: str, version: Optional[str] = None) -> dict:
    lm, ref = _resolve(store, manifold_id, version)
    m = _legacy_model(lm)
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
    # P0.5a: the scope's internal identity is EdgeKey(lineage, frm, to), but the wire keeps its historical
    # [frm, to] pair shape — no wire change in this work package (ruling 2026-08-11). Dedupe: two refuted
    # lineages over one level pair are one blocked pair on the wire.
    scope = {"blocked_edges": [list(e) for e in sorted({(k.frm, k.to) for k in ps.blocked_edges})] if ps else [],
             "blocked_by": {f"{k.frm}->{k.to}": v for k, v in (ps.blocked_by.items() if ps else [])}}
    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
                      "dimensions": dimensions, "edges": edges, "universes": universes,
                      "hierarchies": hierarchies, "relates": relates,
                      "measures": measures, "derived": derived, "published_scope": scope},
                     manifold_id, ref)


# --- tool 3 ---------------------------------------------------------------------------------
def describe_measure(store: ManifoldStore, manifold_id: str, measure: str,
                     version: Optional[str] = None) -> dict:
    lm, ref = _resolve(store, manifold_id, version)
    if lm.manifold is None:
        return _governed_describe_measure(lm, manifold_id, measure, ref)
    m = _legacy_model(lm)
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


def _governed_publication(lm):
    """The v2 publication, read by V2'S OWN READER from the artifact this unit was loaded from.

    NOT a second name→family map. `GovernedPublicationV2.resolve_reference` already owns the rule —
    canonical reference or declared alias, one direction, at most one family, with ambiguity refused
    at parse time — and reimplementing that lookup over the plain-data projection would be a second
    enumeration of a contract this server does not own. The store carries the path so this can read
    the artifact rather than reconstruct a governed object out of its own projection."""
    import json as _json

    from columna_core.governed.publication import parse_publication
    with open(lm.publication_path, encoding="utf-8") as f:
        return parse_publication(_json.load(f))


def _governed_describe_measure(lm, manifold_id: str, measure: str, ref) -> dict:
    """`describe_measure` for a successor-native unit — governed facts only, and NOTHING ELSE.

    THE OMISSION RULE (ruled Huayin, 2026-09-14), which is the whole design of this function:

        True structural emptiness may be represented as empty. A fact belonging to another
        jurisdiction, and not established for this object, must be OMITTED rather than represented
        by a domain-significant empty or default value.

    So three fields are empty and three are absent, and the difference is not stylistic:

      EMPTY, because it is TRUE.  `family.members`, `member_anchors`, `signatures` — a governed
      family HAS no members (the same relation `reducers: []` already denies), so an empty member
      structure is an accurate statement about it. The per-member provider facts never arise:
      `operators()` is not called, not refused — with no members there is nothing to look up.

      ABSENT, because a DEFAULT WOULD ASSERT SOMETHING NOBODY DECLARED.
        · `dtype` — governed `value_domain` and execution-representation dtype are different facts
          and neither substitutes for the other. Mapping `decimal` onto a substrate dtype name would
          invent a correspondence the publication never made.
        · `m_anchor` — `mechanism` is DERIVED: an empty M-anchor yields `"MCAR"`. Emitting the block
          would publish MISSING-COMPLETELY-AT-RANDOM, a real statistical claim, out of nothing. C5
          participation and C9 exceptional cases are neighbouring facts in another register and are
          not substitutes.
        · `provenance` — ratification and constitution authority say WHO RATIFIED THIS LAW; an
          evidence grade says WHETHER THE DATA BEARS IT OUT. The block's only field was the grade,
          so the block goes with it rather than standing empty.

    `description` is `""` per the ratified target/description distinction: C1 is identity-bearing
    governed constitution and does not travel in a folklore field."""
    pub = _governed_publication(lm)
    family = pub.resolve_reference(measure)
    if family is None:
        raise ToolInputError(
            f"unknown measure '{measure}' in manifold '{manifold_id}' "
            f"(have {sorted(f.canonical_reference for f in pub.families)})")

    components = {d.name: sorted({c["name"] for c in (d.body or {}).get("components") or []
                                  if isinstance(c, dict) and c.get("name")})
                  for d in pub.of_kind("anchor")}

    return _disclose({
        "contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
        "measure": measure,
        "description": _governed_description_is_absent(),
        "universe": family.universe,
        # no members in v2 — and therefore no member-keyed provider facts to look up
        "family": {"root": family.canonical_reference, "members": [], "reducer_kind": {}},
        "member_anchors": {},
        "signatures": {},
        "v_anchor": {"universe": family.universe,
                     "grain": components.get(family.constitutive_anchor, [])},
        # dtype · m_anchor · provenance — DELIBERATELY ABSENT, see this function's docstring
    }, manifold_id, ref)


# --- tools 4 & 5 (the ENVELOPE wire) --------------------------------------------------------
def _syntax_error_wire(detail: str, universe: Optional[str]) -> dict:
    return {"contract_version": CONTRACT_VERSION, "outcome": "error",
            "frame": {"anchor": [], "universe": universe, "rollup_severity": "none", "disclosures": []},
            "columns": [], "error": {"reason": "frameql_syntax", "detail": detail}}


def _invalid_request_wire(reason: str, detail: str) -> dict:
    return {"contract_version": CONTRACT_VERSION, "outcome": "error",
            "frame": {"anchor": [], "universe": None, "rollup_severity": "none", "disclosures": []},
            "columns": [], "error": {"reason": reason, "detail": detail}}


def _legacy_model(lm):
    """The legacy `.cml` read model, or a structural refusal — never an attribute error.

    A SUCCESSOR-NATIVE governed unit has no `manifold.cml` and therefore no `Manifold` object, and
    the tools below this line are presentation over exactly that object: measures, universes,
    hierarchies, evidence grades. They are LEGACY-MODEL tools, and asking them about a unit that has
    no legacy model is a structural mistake by the caller, not an analytical outcome.

    So it lands in the existing structural channel — the same one `not_realizable_here` and
    `publication_not_found` use — rather than inventing a wire mood for it. What the successor
    surface should say about a governed unit's shape is a real question and a separate one: it would
    be describe-over-the-governed-projection, which this slice did not build and must not fake."""
    if lm.manifold is None:
        raise ToolInputError(
            f"no_legacy_model: '{lm.manifold_id}' is a governed runtime unit with no manifold.cml, "
            f"and this tool presents the legacy read model. Its governed publication is served "
            f"through the execution seam (check_frame_query); describing it from the governed "
            f"projection is not part of this build")
    return lm.manifold


def _resolve_for_request(store: ManifoldStore, manifold_id: str, ref, lm, stmt,
                         version: Optional[str] = None):
    """Redirect to the runtime THE STATEMENT NAMES, when it names one (P1-19; Ruling v0.2 §9-§10).

    Called AFTER the surface binding has been resolved structurally, so every pre-existing ordering and
    every pre-existing error channel is preserved: an unresolvable ``manifold_id`` ARGUMENT still raises
    through the MCP-error channel before anything is parsed, and a syntax error is still disclosed
    against the resolved publication. This function changes exactly one thing — a statement that names a
    DIFFERENT Manifold is served from that Manifold instead of silently from the bound one.

    Returns ``(lm, ref, effective_id, invalid)``; ``invalid`` is a wire dict or ``None``.

    Before this, no consumer of ``stmt.from_manifold`` existed anywhere in the tree. The parser
    preserved it and `desugar` carried it, but every statement-taking tool resolved from the argument
    alone, so `FROM product_manifold SELECT revenue AT {customer}` served from the bound manifold and so
    did `FROM no_such_manifold`. §10 is explicit: "If `FROM M` names a governed Manifold and the request
    is otherwise valid, realization must address `M`", and "A surface-bound Manifold may not silently
    replace an explicitly named different Manifold."

    The two failure channels stay apart. An unresolvable ARGUMENT is the caller addressing the tool
    wrongly — structural, pre-adjudication, raised by `_resolve`. An unresolvable Manifold named INSIDE
    the request is a defect of the request — §10 "Explicit unknown Manifold ... **Invalid**" — so it
    belongs in the wire. It rides the transitional `error` mood under its own reason string, because
    reason strings are extensible while the wire MOODS are held pending a separate ruling (v0.2 §13;
    Step 6 of the repair sequence).
    """
    named = getattr(stmt, "from_manifold", None)
    if not named or named == manifold_id:
        return lm, ref, manifold_id, None
    try:
        lm2, ref2 = store.resolve_public(named, None)
    except (PublicationNotFound, NotRealizableHere, KeyError):
        # KeyError is the compatibility-fallback miss inside `resolve_public` (store.py:296) — the
        # same "no such Manifold" fact arriving by a third path. All three are §10's "Explicit
        # unknown Manifold", so all three land in the wire rather than the structural channel.
        return lm, ref, manifold_id, _invalid_request_wire(
            "from_manifold_unresolvable",
            f"FROM names {named!r}, which is not a governed publication this surface can realize "
            f"(governed lineages: {store.governed_ids()}; compatibility runtimes: {store.ids()}). "
            f"An explicitly named Manifold governs the request and is never silently replaced by the "
            f"bound one; omit FROM to use the surface binding {manifold_id!r}.")
    return lm2, ref2, named, None


def execute_frame_query(store: ManifoldStore, manifold_id: str, frameql: str,
                        version: Optional[str] = None) -> dict:
    """Execute a FrameQL ENVELOPE statement (`SELECT <series> AT {anchor} [WHERE][HAVING][ORDER BY]
    [LIMIT]`) over real data. The terse `cols @ anchor` form is RETIRED from the wire (0.9.0 tombstone).
    Returns the four-mood wire contract annotated with `executed: true` and `fetches_delta` (the backend
    fetches this run cost) — the executing counterpart of `check_frame_query`'s zero-fetch pre-flight."""
    from columna_core.envelope import parse_statement, EnvelopeSyntaxError
    lm, ref = _resolve(store, manifold_id, version)
    eff_id = manifold_id
    try:
        stmt = parse_statement(frameql)
        lm, ref, eff_id, invalid = _resolve_for_request(store, manifold_id, ref, lm, stmt, version)
        if invalid is not None:
            return _disclose(invalid, eff_id, ref)
        before = _fetch_count(lm.provider)
        fr = lm.provider.run(stmt)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return _disclose(_syntax_error_wire(str(e), None), eff_id, ref)
    after = _fetch_count(lm.provider)
    delta = (after - before) if (before is not None and after is not None) else None
    return _disclose(dw.wire_frame(fr, executed=True, fetches_delta=delta), eff_id, ref)


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
    eff_id = manifold_id
    _syn = lambda d: {"contract_version": CONTRACT_VERSION, "executed": False, "fetches_delta": 0,
                      "outcome": "error", "error": d}
    try:
        stmt = parse_statement(statement)
        lm, ref, eff_id, invalid = _resolve_for_request(store, manifold_id, ref, lm, stmt, version)
        if invalid is not None:
            return _disclose(_syn(invalid["error"]), eff_id, ref)
        return _disclose(lm.provider.explain(stmt), eff_id, ref)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return _disclose(_syn({"reason": "frameql_syntax", "detail": str(e)}), eff_id, ref)


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
    eff_id = manifold_id
    try:
        stmt = parse_statement(frameql)
    except (EnvelopeSyntaxError, FrameQLSyntaxError) as e:
        return _disclose(_syntax_error_wire(str(e), None), eff_id, ref)
    lm, ref, eff_id, invalid = _resolve_for_request(store, manifold_id, ref, lm, stmt, version)
    if invalid is not None:
        return _disclose(invalid, eff_id, ref)
    before = _fetch_count(lm.provider)
    fr = lm.provider.plan(stmt)
    after = _fetch_count(lm.provider)
    delta = (after - before) if (before is not None and after is not None) else None
    return _disclose(dw.wire_frame(fr, executed=False, fetches_delta=delta), eff_id, ref)


def frame_ql_grammar() -> dict:
    """The FrameQL grammar, verbatim, with the columna-core version it came from. BOTH LEVELS, because
    `envelope.__doc__` carries both and this tool returns it unedited: the ENVELOPE — `[EXPLAIN]
    [FROM m] [WITH …] SELECT <series [AS alias]>,… AT {anchor} [WHERE][HAVING][ORDER BY][LIMIT n [PER
    {dims}]]` — and the EXPRESSION dialect inside a series (Frame-QL 1.0 §15): the precedence ladder,
    `=` compares / `:` names an argument, dotted access, braces-are-grains, brackets-subscribe. So a
    caller writes a query rather than guessing the shape, and reads `revenue / orders @ {customer}`
    the way the parser does. Touches no manifold and no data.

    RESTATED HERE, NOT RE-AUTHORED. This sentence summarizes what the returned text contains; the text
    itself is the module docstring, which is the single authority. If the two disagree, the docstring
    is right and this summary is the defect — that is the only reason it is allowed to exist."""
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
    if lm.manifold is None:
        return _governed_discovery(lm, manifold_id, ref)
    m = _legacy_model(lm)
    measures = [{"measure": mc.name, "universe": mc.universe, "reducers": list(mc.family),
                 "grain": sorted(m.universes[mc.universe].base_dimensions),
                 "description": mc.description} for mc in m.measures.values()]
    anchors = [{"universe": u.name, "basis": u.basis,
                "grain": sorted(u.base_dimensions)} for u in m.universes.values()]
    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
                      "measures": measures, "anchors": anchors,
                      "levels": [lv.name for lv in m.levels.values()],
                      "ask_form": _ASK_FORM}, manifold_id, ref)


def manifold_status(store: ManifoldStore, manifold_id: str, version: Optional[str] = None) -> dict:
    """The manifold's health at a glance, WITHOUT touching data: counts (measures, universes, levels,
    hierarchies, relations, edges, derived), the published serving scope (edges blocked by refuted
    hierarchies), and the evidence standing (how many adjudicated Licenses are verified / corroborated /
    untestable)."""
    lm, ref = _resolve(store, manifold_id, version)
    m = _legacy_model(lm)
    ps = lm.provider.published_scope()
    licenses = getattr(ps, "licenses", None) if ps else None
    lic_list = list(licenses.values()) if isinstance(licenses, dict) else (list(licenses) if licenses else [])
    # THE SNAPSHOT HOLDS VERDICT STRINGS, NOT LICENSE OBJECTS (corrected 2026-09-13).
    # `PublishedScope.licenses` is documented at its source as `"derived.member" -> verdict
    # (license-state snapshot)`, and `_snapshot_licenses` builds it as `fm.license.verdict if
    # fm.license else None`. This loop previously did `getattr(lic, "verdict", None)` over those
    # values — and `getattr("verified", "verdict", None)` is None, so the counter could never
    # increment and `evidence.verdicts` was STRUCTURALLY ALWAYS `{}` while the tool's published
    # description promised "how many adjudicated Licenses are verified / corroborated / untestable".
    #
    # It survived because no `.cml` in this repository declares a derived `FERTILE` family, so the
    # snapshot is empty everywhere in-tree and the only test asserted the key's PRESENCE. A field
    # that cannot be populated is not tested by a fixture that never populates it.
    #
    # EVERY non-null verdict is counted, not only the three the description names: a verdict this
    # code did not expect must appear in the count rather than vanish from it, which is the same
    # fail-closed discipline the condition-code vocabulary already follows. A `None` entry is an
    # UNADJUDICATED member and is not a verdict, so it is not counted here.
    verdicts: dict[str, int] = {}
    for verdict in lic_list:
        if verdict:
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
    return _disclose({"contract_version": CONTRACT_VERSION, "manifold_id": manifold_id,
            "counts": {"measures": len(m.measures), "universes": len(m.universes),
                       "levels": len(m.levels), "hierarchies": len(m.hierarchies),
                       "relations": len(m.non_functional), "edges": len(m.edges),
                       "derived": len(m.derived)},
            "published_scope": {                             # EdgeKey -> historical [frm, to] wire shape
                "blocked_edges": [list(e) for e in sorted({(k.frm, k.to) for k in ps.blocked_edges})] if ps else []},
            "evidence": {"licenses": len(lic_list), "verdicts": verdicts}}, manifold_id, ref)


def get_evidence(store: ManifoldStore, manifold_id: str, measure: Optional[str] = None,
                 version: Optional[str] = None) -> dict:
    """The evidence behind a manifold's claims, WITHOUT touching data: each measure's declared evidence
    grade and each functional edge's, plus the adjudicated Licenses (verdict, lineages, basis,
    attestation) minted at publish. With `measure`, scoped to that measure's family and universe."""
    from columna_core.describe import license_to_dict
    lm, ref = _resolve(store, manifold_id, version)
    m = _legacy_model(lm)

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

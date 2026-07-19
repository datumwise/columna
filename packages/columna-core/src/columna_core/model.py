"""
columna_core.model — the Manifold object model (per the object-model spec).

Two layers:
  Layer 1 (population): Universe — which observations exist (base dims + predicate).
  Layer 2 (coordinate): DimensionLevel + FunctionalEdge — how they're addressed.

Key unification: a rollup (day->month) and a cross-table relationship (store->region)
are the SAME thing — a FunctionalEdge the engine transports along, tagged with a lineage.
The backend never joins; it delivers a measure (single-table group-by) and an edge's
key->key mapping (single-table distinct). The B-anchor blocks transport per-lineage.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# reaggregation tiers (the transport mechanism)
ADDITIVE, SKETCH, HOLISTIC = "additive", "sketch", "holistic"
# evidence grades -> disclosure
DECLARED, PROVEN, INFERRED_SAMPLE, INFERRED_DOCS = \
    "declared", "proven", "inferred_sample", "inferred_docs"
_UNCONFIRMED = {INFERRED_SAMPLE, INFERRED_DOCS}


# ---- Layer 1: population -----------------------------------------------------
@dataclass(frozen=True)
class Ref:
    """A reference inside a universe predicate."""
    is_literal: bool
    value: Optional[str] = None    # literal value
    table: Optional[str] = None    # set => an ATTRIBUTE in this table (cross-table => broadcast)
    column: Optional[str] = None   # the column/level name (table=None => a coordinate/level ref)

@dataclass(frozen=True)
class Comparison:
    left: "Ref"
    op: str                        # >= > <= < = !=
    right: "Ref"

@dataclass(frozen=True)
class Predicate:
    comparisons: tuple = ()        # AND-ed Comparisons

@dataclass(frozen=True)
class Universe:
    name: str
    base_dimensions: frozenset            # base level names bundled into this population
    predicate: Optional["Predicate"] = None   # carves valid points; over dims/attrs, never measures
    basis: Optional[str] = None           # B3 (capture §7): the population's kind, which DETERMINES what
                                          # absence means engine-wide — 'events' (absence=ZERO, lawful
                                          # zero-fill) | 'spine' (absence=GAP, incomplete_data caveat) |
                                          # 'product' (cartesian; absence always a gap) | 'registry'
                                          # (membership checkable). None = undeclared (today's behavior;
                                          # absence-semantics wiring is inert until a basis is declared).
    basis_license: Optional["License"] = None   # B3 testedness record minted at publish (serving follows
                                          # the DECLARATION regardless — BASIS is a semantic declaration, not a
                                          # shortcut; the license is for describe/trust only). None = unadjudicated.
    description: str = ""                 # DESCRIPTION string (case-demo b) — flows to describe/wire (additive)
    rejects: tuple = ()                   # MAP-layer: ((physical, reason), ...) — rejected incarnations, ATTESTED
                                          # not adjudicated. BLAST WALL: map-artifact ONLY; NEVER describe/wire.
    attributes: tuple = ()                # logical ROW-attributes (case-demo c, extended): ((name, binding), ...)
                                          #   e.g. units -> transactions.units; legal in a ROW-form ASSERT's
                                          #   predicate. A row-attribute may share its physical spelling when the
                                          #   physical name already speaks analyst; the map still records the row.


# ---- Layer 2: coordinate -----------------------------------------------------
@dataclass(frozen=True)
class DimensionLevel:
    name: str                             # qualified where forked: "cal.month","fisc.month","day","store"
    realized_by: str                      # the base column key for this level
    is_base: bool = False
    description: str = ""                 # DESCRIPTION string (case-demo b) — flows to describe/wire (additive)
    rejects: tuple = ()                   # MAP-layer: ((physical, reason), ...) — e.g. region's two rejects.
                                          # BLAST WALL: map-artifact ONLY; NEVER describe/wire.
    attributes: tuple = ()                # logical attributes (case-demo c, OF-9): ((name, physical_binding), ...)
                                          #   e.g. store.opened -> stores.opened_date; legal in universe predicates.

@dataclass(frozen=True)
class FunctionalEdge:
    """A functional (N:1 / 1:1) mapping the engine transports along. Unifies rollup and relationship."""
    frm: str                              # finer / many level
    to: str                               # coarser / one level
    lineage: str                          # "calendar","fiscal","store_geo",... (B-anchor blocks by this)
    provider_table: str                   # single table that delivers the key->key mapping
    frm_col: str                          # column in provider_table for frm key
    to_col: str                           # column in provider_table for to key
    evidence: str = PROVEN


# ---- licenses (the Certificate kernel; WP-B) ---------------------------------
# Adjudication verdicts (Certificate-kernel shape, per reference manual Part VI).
VERIFIED, CORROBORATED, UNTESTABLE, CONTRADICTED = \
    "verified", "corroborated", "untestable", "contradicted"


@dataclass(frozen=True)
class License:
    """The adjudicated authority for a declared capability. WP-B's first customer is derived-column
    *fertility* (a member's reduction along a lineage that both commutes and is permitted); a future
    HIERARCHY/ASSERT precondition carries the SAME record — that is the Certificate-kernel
    requirement, so this shape is deliberately generic.

    Constitutional sentence: authority is declared; mathematics may verify; data may only refute or
    corroborate; the default is closed. Verdicts:
      VERIFIED     — symbolic proof from the formula tree + operator algebraic properties; timeless
                     (attestation is None).
      CORROBORATED — refutation-tested against attested data, no counterexample; watermarked to that
                     attestation; re-adjudicated on re-attestation (may flip to CONTRADICTED).
      UNTESTABLE   — stands on authored authority; recorded and visible in describe but NOT exercised
                     (the reduce-path optimization runs only under VERIFIED/CORROBORATED), so an
                     asserted license never changes a served number (ruling §5, 2026-07-14).
    CONTRADICTED never persists past publish — a contradicted declaration fails closed (the manifold
    does not publish), so it is not a value this record carries at runtime."""
    verdict: str                          # VERIFIED | CORROBORATED | UNTESTABLE
    lineages: frozenset = frozenset()     # the declared fertile lineages this license opens
    basis: str = ""                       # symbolic-proof note | attestation ref + tolerance | author note
    attestation: Optional[str] = None     # None for VERIFIED/UNTESTABLE; the data-attestation watermark for CORROBORATED


# ---- measures ----------------------------------------------------------------
@dataclass(frozen=True)
class BAnchor:
    blocked_lineages: frozenset = frozenset()   # lineages this agg may NOT be reduced along

@dataclass(frozen=True)
class FamilyMember:
    """Names an operator (reaggregability comes from the operator REGISTRY — operator-level)
    plus this column's B-anchor (which lineages reduction is PERMITTED along — column-level).
    The two gates compose: reduce iff monoid (possible) AND B-anchor-clear (permitted).

    On DERIVED columns the polarity mirrors: a derived member is created only by an adjudicated
    fertility declaration and carries its `license` (closed-by-default; the license opens travel).
    On MEASURE columns `license` is None (measures are open-by-default; the B-anchor closes)."""
    agg: str                              # operator name; looked up in operators.REGISTRY
    b_anchor: BAnchor = BAnchor()         # measure column-level: BLOCKED (closed) lineages
    order_by: Optional[str] = None        # for ORDERED operators (last/first): the level to order by
    description: str = ""                 # DESCRIPTION string (case-demo b) — per-member folklore; flows to describe/wire
    declared_lineages: frozenset = frozenset()  # derived: the DECLARED fertile lineages (FERTILE {..}); the
                                          #          parser RECORDS these — it never constructs a License
    license: Optional[License] = None     # derived-member fertility License; constructed ONLY by the
                                          #          adjudicator at publish. None on parse and on measure members.

@dataclass(frozen=True)
class MeasureColumn:
    name: str
    universe: str
    home_table: str                       # the table the base measure is delivered from
    pre_expr: str                         # per-row pre-agg over RAW base columns: "amount", "price*qty"
                                          # (no casts — the connector realizes logical_type -> physical)
    logical_type: str = "Float64"         # declared logical (Polars) dtype — the representation promise
    family: dict = field(default_factory=dict)   # agg-name -> FamilyMember
    m_anchor: frozenset = frozenset()     # missingness structure: empty=MCAR, others=MAR, self=MNAR
    distinct_col: Optional[str] = None    # for distinct/sketch
    sketch_precision: int = 12            # HLL lg_k for sketch-witness measures; the sketch type is HLLSketch(p)
    evidence: str = PROVEN
    description: str = ""                 # DESCRIPTION string (case-demo b) — flows to describe/wire (additive)
    rejects: tuple = ()                   # MAP-layer: ((physical, reason), ...) — rejected incarnations, ATTESTED
                                          # not adjudicated. BLAST WALL: map-artifact ONLY; NEVER describe/wire.

    @property
    def is_unconfirmed(self): return self.evidence in _UNCONFIRMED
    @property
    def missingness(self):
        if not self.m_anchor: return "MCAR"
        return "MNAR" if self.name in self.m_anchor else "MAR"


@dataclass(frozen=True)
class DerivedColumn:
    """A column generated from stored columns through a formula. Closed by default over travel: a
    bare formula (empty `family`) is DENOTATION-ONLY — its value at an anchor is the formula
    evaluated over co-anchored atoms there, recomputed from components (never reduced from cached
    finer values without a license). Fertility is added by declaring `family` members, each carrying
    a License. `resolution_anchor` (declared `AT <level>`) makes the alternative reading a DISTINCT
    metric whose meaning embeds the anchor (e.g. mean of daily rates)."""
    name: str
    formula: str                          # post-agg over measure/derived names: "revenue / orders"
    family: dict = field(default_factory=dict)   # member-name -> FamilyMember (each with a License); empty = denotation-only, no travel
    resolution_anchor: Optional[str] = None      # declared `AT <level>`; None = output-anchor denotation
    description: str = ""                 # DESCRIPTION string (case-demo b) — flows to describe/wire (additive)


# ---- Track-1 (Certificate customers): asserted invariants + verified hierarchies ------------------
@dataclass(frozen=True)
class Assert:
    """A declared invariant (B1). Two forms: `row` — a predicate every atom of the universe must
    satisfy (dims/attrs only, the universe-carving grammar); `invariant` — an aggregate relation over
    MEASURES at an anchor (cross-measure reconciliation). Data-channel only: the adjudicator tests it
    on attested data at publish, minting the same `License` (CORROBORATED | CONTRADICTED | UNTESTABLE);
    a violation on re-attestation CUTS the affected scope (never edits the artifact). Names are
    universe-scoped (like measures), so the same name may recur across universes."""
    name: str
    universe: str
    kind: str                             # "row" | "invariant"
    predicate: Optional["Predicate"] = None   # row-form: over dims/attrs (universe-carving grammar)
    anchor: tuple = ()                    # invariant-form: anchor levels (the ruled `*` grammar)
    left: str = ""                        # invariant-form: LHS expression over measures
    op: str = ""                          # invariant-form: comparison in {==,<=,>=,<,>}; `==` rides the
                                          #   WP-B adjudication tolerance (rtol/atol), recorded in the license basis
    right: str = ""                       # invariant-form: RHS expression over measures
    license: Optional["License"] = None   # minted by the adjudicator at publish (kernel reuse, Q1)
    description: str = ""                 # DESCRIPTION string (case-demo b) — flows to describe/wire (additive)


# ---- RELATE (the ANTI-EDGE): non-functional (M:N) relationships + their crossing FACES ----------
# canonical face schemes (the value's DISPOSITION on the trip across an M:N edge). v1 EXECUTES touch
# only; assign/alloc are declared-but-deferred (post-launch ledger). A face names what the value DOES,
# never the selection criterion — the criterion lives in the declaration (assign/alloc `= <selection>`).
TOUCH, ASSIGN, ALLOC = "touch", "assign", "alloc"
FACE_SCHEMES = (TOUCH, ASSIGN, ALLOC)


@dataclass(frozen=True)
class Face:
    """A declared crossing DISPOSITION on a RELATE (M:N) edge — how an additive value behaves on the
    trip. touch = the value reaches EVERY match (join-multiply; deliberate multi-count; served DISCLOSE).
    assign = it goes to exactly one; alloc = it splits across (both declared-but-deferred in v1).

    Polarity mirror of FamilyMember (parser.py `_p_fertility_family`): DESCRIPTION is mandatory (the
    folklore rule), and the `license` is constructed ONLY by the adjudicator at publish — None on parse.
    A face is closed-by-default: its license OPENS the crossing (per the polarity law, model.py above)."""
    name: str                             # the addressable face name — the query says <coordinate>.<name>
    scheme: str                           # disposition kind: one of FACE_SCHEMES
    description: str = ""                 # mandatory folklore; flows to describe/relates[].faces[] (additive)
    selection: str = ""                   # assign/alloc parameter from the declaration (weight col, pick rule); '' for touch
    license: Optional["License"] = None   # basis-license; adjudicator-only at publish. None on parse (closed-by-default).


@dataclass(frozen=True)
class Relate:
    """A declared non-functional (M:N) relationship — the ANTI-EDGE (HIERARCHY says 'aggregation
    survives the trip'; RELATE says 'no lawful rollup exists'). Logical endpoints + the NOTE folklore +
    declared crossing `faces`.

    The VIA bridge (table + join columns) is MAP-LAYER (ruling 2026-07-19, Huayin): ENGINE-VISIBLE
    (join-multiply needs it), describe-INVISIBLE — it NEVER rides relates[] or any wire, exactly like a
    universe's `rejects`. The projection strips it; the insulation test asserts it stays off-wire.
    Per-hop VIA capture copies the shipped HIERARCHY pattern (`VIA table(frm_col, to_col)`)."""
    frm: str                              # one endpoint level
    to: str                               # the other endpoint level
    detail: str = ""                      # the NOTE verbatim (folklore) — flows to relates[].note (additive)
    faces: tuple = ()                     # (Face, ...) declared crossings; () = today's bare RELATE (no faces)
    # ---- MAP-LAYER: engine-visible, describe-invisible; NEVER on the wire ----
    via_table: Optional[str] = None       # the bridge table (physical); None for a bare RELATE
    via_frm_col: Optional[str] = None     # bridge column carrying the frm key
    via_to_col: Optional[str] = None      # bridge column carrying the to key


@dataclass(frozen=True)
class Hierarchy:
    """A declared functional-dependence lineage (B2). The SOLE surface for functional paths after the
    EDGE purge (case-demo, §2a): `HIERARCHY <lineage> { path; path }`. Branching allowed — a lineage may
    be a small DAG (calendar: the day→month→quarter→year chain PLUS the day→week branch, because weeks
    don't nest in months). SUGAR: it desugars to plain FunctionalEdges that are INDISTINGUISHABLE from
    the old hand-declared EDGEs — the edges remain the single internal truth (adjudicator/planner/engine
    vocabulary untouched); this record is communicative PROVENANCE plus the handle for the publish-time
    FD test (every hop a genuine key->key function; every chain composition holds; a violation →
    CONTRADICTED, fails closed). A bar `BLOCKED { <lineage> }` addresses the lineage WHOLE (every branch)."""
    lineage: str
    paths: tuple = ()                     # (chain, chain, ...); each chain = (level_a, level_b, ...) — the branches
    license: Optional["License"] = None   # minted by the adjudicator at publish (kernel reuse, Q1)
    description: str = ""                 # DESCRIPTION string (b) — flows to describe (NOT the map's rejects)

    @property
    def chain(self) -> tuple:
        """Back-compat: the primary (first) path. Adjudication + describe iterate `paths`."""
        return self.paths[0] if self.paths else ()


# ---- the Manifold ------------------------------------------------------------
@dataclass
class Manifold:
    name: str
    version: int
    universes: dict                       # name -> Universe
    levels: dict                          # name -> DimensionLevel
    edges: list                           # [FunctionalEdge]  (the coordinate DAG + relationships)
    measures: dict                        # name -> MeasureColumn
    derived: dict = field(default_factory=dict)
    non_functional: list = field(default_factory=list)  # [Relate] — M:N relationships (fan-out diagnostics + crossing faces)
    asserts: list = field(default_factory=list)         # [Assert] — declared invariants (B1), universe-scoped
    hierarchies: list = field(default_factory=list)     # [Hierarchy] — provenance for the desugared FD chains (B2)

    # ---- coordinate graph helpers ----
    def base_of_universe(self, uni: str) -> frozenset:
        return self.universes[uni].base_dimensions

    def out_edges(self, level: str):
        return [e for e in self.edges if e.frm == level]

    def find_path(self, from_levels, target: str):
        """BFS over functional edges from any of from_levels to target.
        Returns (start_level, [edges]) or None. Empty path if target in from_levels."""
        if target in from_levels:
            return (target, [])
        # BFS
        from collections import deque
        q = deque((b, b, []) for b in from_levels)
        seen = set(from_levels)
        while q:
            start, cur, path = q.popleft()
            for e in self.out_edges(cur):
                if e.to == target:
                    return (start, path + [e])
                if e.to not in seen:
                    seen.add(e.to)
                    q.append((start, e.to, path + [e]))
        return None

    def level_universe_member(self, level: str, uni: str) -> bool:
        """Is `level` addressable within universe `uni`? True if it's a base dim of uni,
        or reachable by functional edges from a base dim of uni."""
        base = self.base_dimensions_as_levels(uni)
        return self.find_path(base, level) is not None

    def base_dimensions_as_levels(self, uni: str) -> frozenset:
        # base_dimensions are level names already
        return self.universes[uni].base_dimensions

    # ---- well-formedness (publish-time) ----
    def check(self) -> list:
        """Returns a list of violations (empty = well-formed)."""
        errs = []
        # closure: edges reference known levels
        for e in self.edges:
            for lv in (e.frm, e.to):
                if lv not in self.levels:
                    errs.append(f"edge references unknown level '{lv}'")
        # measure universes exist; derived formulas reference known columns
        for m in self.measures.values():
            if m.universe not in self.universes:
                errs.append(f"measure '{m.name}' binds unknown universe '{m.universe}'")
        # measure name unique per universe is automatic (dict keyed by name); cross-universe
        # name collision is impossible here since names are global keys — but two measures
        # could legitimately want the same name in different universes; we enforce global
        # uniqueness for v1 (stricter, simpler) and note it.
        return errs


# small helper for building anchors as ordered tuples of level names
def A(*levels) -> tuple:
    return tuple(levels)

"""
columna_core.disclosure — the disclosure shadow-value and the structured no-result.

Two-level correctness contract (ADR-032):

  * The COLUMN ENGINE never judges. It only attempts, returning a result OR a no-result that
    carries the reasons in its disclosure plus a DISCRIMINATOR — `ambiguous` (no unique answer
    under the Manifold's rules) or `unsupported` (the data cannot support a result). It never
    decides "clarify" or "refuse".
  * The PLANNER owns the four outcomes (serve · disclose · clarify · refuse). It reaches them
    statically (from structure) or by classifying a no-result's discriminator at a single
    chokepoint (`Refusal.classified`): ambiguous -> clarify, unsupported -> refuse. A fifth
    kind, `error`, is a vocabulary/capability failure (unknown operator, not implemented) — a
    malformed-or-unsupported query, not an analytical verdict.

A served, producible result is ALWAYS served, with any analytical risk riding on its face as a
critical Caveat — never withheld (inform-and-serve, ADR-020). A B-anchor crossing is therefore
a served disclosure (`B_ANCHOR_CROSSING`, severity critical), not a refusal.

`Outcome` is the no-result VALUE (a plain dataclass, never an exception) — it is what flows on
`ColumnResult.refusal` and what every surface/agent receives, classified into clarify/refuse/error.
`Refusal` is only an INTERNAL control-flow signal that carries an `Outcome` from deep in the
recursive walk to the planner's single assembly point; it is plumbing — a structured goto — and is
never handed to a surface. A clarify/refuse is a value, never a thrown error.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Optional
import math

APPROXIMATION = "approximation"
FRESHNESS = "freshness"
COVERAGE = "coverage"
UNCONFIRMED = "unconfirmed_assumption"
TRANSPORT = "transport"          # records a faithful transport step (provenance)
B_ANCHOR_CROSSING = "b_anchor_crossing"
# ── TOMBSTONE ── `b_anchor_crossing` was the SERVED, CRITICAL caveat for a reduction coarsening across
#   a blocked family — the canonical inform-and-serve case (ADR-020). RETIRED AS A PRODUCER 2026-08-20
#   (generated-family law, Huayin): a structurally prohibited reduction now REFUSES, with the reason
#   `blocked_reduction` on the no-result channel. Disclose exists inside the lawful region; it cannot
#   legalize an operation the governed law does not possess, and a caveat attached to a number that
#   should never have been produced was the mechanism by which the same meaningless total kept being
#   served. The constant and its wire mapping are KEPT so archived caveats, recorded transcripts and
#   the deposited manuals still resolve; a retirement-pin test asserts it is never emitted afresh.
#   Same spelling as the REFUSE reason `blocked_reduction` — one concept, two channels; probe the
#   referent, not the spelling. Vocabularies grow by rule and shrink by tombstone, never silently.
DATA_GAP = "data_gap"            # served, material: absent cells are GAPS (spine/product basis, B3)
ZERO_FILL = "zero_fill"          # RETIRED as a producer (columna#143 step 3): the basis-keyed events
                                 # zero-fill is gone. Constant kept so the wire mapping and any archived
                                 # caveat still resolve; the four fill-rule dispositions below replace it.
# Φ_v, the M-contract fill rule (columna#143 step 3) — absence semantics now follow the DECLARED member
# rule, never the universe basis. Four dispositions:
DECLARED_FILL = "declared_fill"      # served, IMMATERIAL: absence filled per a DECLARED `zero` rule — the
                                     # quantity existed and was nil; a correct value, not a fictitious one.
UNKNOWN_ABSENCE = "unknown_absence"  # served, MATERIAL: `unknown` rule — a value existed but was not
                                     # recorded (state-valued); LEFT NULL, disclosed, never filled.
OUT_OF_POPULATION = "out_of_population"  # served, IMMATERIAL: `undefined` rule — the point is outside the
                                     # member's population; a restriction, not an absence.
UNDECLARED_ABSENCE = "undeclared_absence"  # served, MATERIAL: NO fill rule declared — the engine discloses
                                     # the absence rather than choose (never fills). #147's interim, permanent.
OVER_COUNT = "over_count"        # served, MATERIAL: a touch-face crossing multi-counts by construction —
                                 # the value reaches every match of an M:N edge, so totals deliberately
                                 # exceed the grand total. Drives DISCLOSE (the honest over-count is the point).
SHADOW = "shadow"                # served, MATERIAL: an ASSIGN-face crossing single-counts (top pick per
                                 # member) so the total reconciles to the grand total, but the memberships
                                 # NOT picked are unrepresented — the shadow. Drives DISCLOSE (the honest drop).
RECONCILIATION = "reconciliation"  # served: an ALLOC-face crossing splits by the normalized driver — the
                                 # commutation certificate (crossed_total vs base_total, delta, status).

# ---- the four planner outcomes, plus error (ADR-032) ------------------------------------
# serve / disclose are carried by a served frame + Disclosure; clarify / refuse / error are
# carried by a no-result Refusal classified by the planner.
SERVE    = "serve"
DISCLOSE = "disclose"
CLARIFY  = "clarify"
REFUSE   = "refuse"
ERROR    = "error"            # vocabulary/capability failure — not an analytical verdict
# no-result discriminators the engine attaches (the seam the planner classifies on):
AMBIGUOUS   = "ambiguous"     # no unique answer under the Manifold's rules   -> CLARIFY
UNSUPPORTED = "unsupported"   # the data cannot support a result              -> REFUSE

# ---- JURISDICTION (Step 1 of the jurisdiction repair, 2026-09-01) -----------------------------
# Which of the three stages a no-result belongs to, per Frame-QL Request Adjudication and
# Disposition Ruling v0.2 §1. This is INTERNAL: it is stamped on every Outcome and is available to
# the decision machinery, but it does not reach the wire. The wire MOODS stay as they are until the
# separate compatibility ruling (v0.2 §13; Step 6), so this commit changes no observable behaviour.
#
# The distinction the moods cannot express, and the whole reason for this seam: `error` currently
# carries BOTH "this never became a valid Frame-QL request" and "this is a valid admitted request
# this build cannot realize", which v0.2 §3 rules must not share one status. Jurisdiction says which,
# without yet changing what the caller sees.
LANGUAGE    = "language"      # Stage A — the request never became a valid canonical request
ANALYTICAL  = "analytical"    # Stage B — a valid request, adjudicated under governed analytical law
REALIZATION = "realization"   # Stage C — admitted, but this profile/build cannot realize it
# `unruled` is NOT a fourth jurisdiction. It marks a reason whose stage is a live, deliberately open
# doctrinal question, so that classifying the table did not silently decide it. Ruling 0.1 §9/§13 and
# v0.2 both decline the certification/admission question, and the 2026-09-01 sweep recorded it as
# "not scored". Registering `unruled` keeps the table exhaustive and fail-closed while leaving the
# doctrine to the architects; it must not be used for a reason merely because classifying is hard.
UNRULED     = "unruled"       # deliberately unclassified — see `UNRULED_REASONS`

# severity lattice: none < info < caution < critical
_SEV_RANK = {"none": 0, "info": 1, "caution": 2, "critical": 3}


@dataclass(frozen=True)
class Caveat:
    category: str
    detail: str
    rel_error: Optional[float] = None
    source: Optional[str] = None
    severity: str = "info"
    remedy: Optional[str] = None
    shadow: Optional[int] = None          # ASSIGN faces: memberships_unrepresented (the shadow count) -> wire
    reconciliation: Optional[tuple] = None  # ALLOC faces: the badge as (k,v) pairs (hashable) -> wire dict

    def render(self) -> str:
        if self.category == APPROXIMATION and self.rel_error is not None:
            return f"approximate: {self.detail} (\u00b1{self.rel_error*100:.2g}%)"
        tag = f"[{self.severity.upper()}] " if _SEV_RANK.get(self.severity, 1) >= 2 else ""
        base = f"{tag}{self.category}: {self.detail}"
        return base + (f"  \u2192 remedy: {self.remedy}" if self.remedy else "")


@dataclass(frozen=True)
class Disclosure:
    """TWO CHANNELS, ONE OBJECT (OF-24 ruling (a), implemented 2026-08-31).

    `caveats` is the SEMANTIC channel: what is true of the answer. It is CALL-INVARIANT — the same
    question over the same data yields the same semantic caveats however the answer was obtained,
    and every mood, materiality and severity rollup is derived from this channel alone.

    `mechanical` is the OBSERVATIONAL channel: what happened to produce this particular call.
    "Served from cache" is the whole of it today. It is legitimately VARIANT between two identical
    asks, which is exactly why it may not sit beside the semantic caveats — a channel that is
    allowed to differ cannot be the one a caller reads to learn what the number means.

    OF-24 found the defect by its consequence: on a fresh store the first asker received LESS
    disclosure than the second for the same question on the same data, because a mechanical fact was
    wearing a semantic name (FRESHNESS) on the semantic channel. Every property below reads
    `caveats` and never `mechanical`, so the semantic channel is call-invariant by construction
    rather than by discipline."""

    caveats: tuple = ()
    population: Optional[str] = None     # the universe/sub-population this column resolved over
    mechanical: tuple = ()               # observational provenance; never affects mood or severity

    @staticmethod
    def clean(population=None): return Disclosure((), population)

    @staticmethod
    def of(*cavs, population=None): return Disclosure(tuple(cavs), population)

    @property
    def is_clean(self): return not self.caveats

    @property
    def rel_error(self):
        errs = [c.rel_error for c in self.caveats
                if c.category == APPROXIMATION and c.rel_error]
        return math.sqrt(sum(e*e for e in errs)) if errs else 0.0

    @property
    def severity(self):
        """Frame-level severity rollup: the max severity over caveats."""
        if not self.caveats:
            return "none"
        return max((c.severity for c in self.caveats), key=lambda s: _SEV_RANK.get(s, 1))

    @property
    def criticals(self):
        return tuple(c for c in self.caveats if c.severity == "critical")

    def has(self, cat): return any(c.category == cat for c in self.caveats)

    def with_caveat(self, c):
        return Disclosure(self.caveats + (c,), self.population, self.mechanical)

    def with_mechanical(self, c):
        """Record an observational fact about THIS call. Never reaches mood, severity or
        materiality — see the class docstring."""
        return Disclosure(self.caveats, self.population, self.mechanical + (c,))

    @staticmethod
    def merge(*parts, population=None):
        seen, mech, pop = {}, {}, population
        for d in parts:
            if d is None:
                continue
            pop = pop or d.population
            for c in d.caveats:
                seen[(c.category, c.detail, c.rel_error, c.source)] = c
            for c in d.mechanical:
                mech[(c.category, c.detail, c.rel_error, c.source)] = c
        return Disclosure(tuple(seen.values()), pop, tuple(mech.values()))

    @staticmethod
    def combine(op, a, b, label=""):
        """Arithmetic propagation: * / add relative errors; + - conservative max."""
        m = Disclosure.merge(a, b, population=(a.population or b.population))
        rels = [d.rel_error for d in (a, b) if d.rel_error > 0]
        if rels:
            err = sum(rels) if op in ("*", "/") else max(rels)
            note = "product/ratio of approximate quantities" if op in ("*", "/") \
                   else "sum/difference of approximate quantities (conservative)"
            m = m.with_caveat(Caveat(APPROXIMATION, f"{label}: {note}" if label else note, rel_error=err))
        return m

    def render_human(self):
        if self.is_clean:
            base = "exact \u2014 no caveats"
        else:
            base = "; ".join(c.render() for c in self.caveats)
        return base + (f"  [over {self.population}]" if self.population else "")


# reason -> (kind, discriminator). The engine emits a *reason* (a fact about what it found);
# the planner derives the *verdict* by applying this policy at its single classification
# chokepoint. This is where "the engine never judges" is made literal: nothing here is decided
# by the engine — it only reports the reason (and, for analytical no-results, the discriminator).
#
# STANDING RULE (Huayin, 2026-07-14, OF-1): one reason per contested dimension. Each clarify reason
# names exactly one dimension along which the request is under-determined; a distinct dimension gets
# its own reason rather than broadening an existing one's gloss. So `ambiguous_grain` stays
# single-meaning (an attribute keyed at several levels), and the input-anchor dimension gets its own
# `input_anchor_ambiguous` — sibling to `co_anchor_ambiguous`.
REASON_OUTCOME = {
    "non_functional_transport": (CLARIFY, AMBIGUOUS, ANALYTICAL),   # fan-out (M:N): no single total exists
    "ambiguous_grain":          (CLARIFY, AMBIGUOUS, ANALYTICAL),   # attribute keyed at several levels
    # ── TOMBSTONE ── `co_anchor_ambiguous` was (CLARIFY, AMBIGUOUS) — "ratio over >1 population: rate's
    #   population ambiguous". RETIRED 2026-07-16 (§2c expression law, Huayin's ruling): a cross-universe
    #   expression is a language-law CATEGORY ERROR, not a clarify (see `cross_universe` below); within one
    #   universe the denotation rule leaves nothing ambiguous. Its emitter left the language entirely and a
    #   retirement-pin test asserts it is never emitted. Kept here as a dated tombstone so old transcripts
    #   and docs remain interpretable — vocabularies grow by rule and shrink by tombstone, never silently.
    "cross_universe":           (ERROR, None, LANGUAGE),        # a column expression combines measures from >1
                                                        #   universe (§2c expression law: a column evaluates in
                                                        #   ONE universe, never crosses the boundary). A category
                                                        #   error — rides the ERROR channel, not the four moods.
                                                        #   Minted 2026-07-16 (§2c). Remedy: juxtapose or declare.
    "input_anchor_ambiguous":   (CLARIFY, AMBIGUOUS, ANALYTICAL),   # inline reduction with no pinned input anchor:
                                                        #   the grain to resolve the inner at is under-
                                                        #   determined (names the same dimension OF-2's
                                                        #   immaterial input-anchor note records)
    "redundant_pin":            (CLARIFY, AMBIGUOUS, ANALYTICAL),   # WP-GRAIN-1 Law 2: a composite input anchor pins
                                                        #   two levels where one functionally determines the
                                                        #   other (p_i -> p_j), so the pair fixes ONE axis,
                                                        #   not two — a CLARIFY (the reader picks between two
                                                        #   admissible pins), never a refuse. Sibling to
                                                        #   `ambiguous_grain`; own reason per OF-1 (one reason
                                                        #   per contested dimension). MINTED 2026-07-30.
    "filter_unsupported":       (ERROR, None, REALIZATION),        # P1-14 (minted 2026-08-31): a WHERE dimension the
                                                        #   series CAN reach, in a filter this build cannot
                                                        #   EXECUTE. Sibling to `filter_unreachable` and
                                                        #   deliberately a different reason: unreachable is a
                                                        #   fact about the MANIFOLD and the asker can fix it by
                                                        #   choosing another dimension; unsupported is a fact
                                                        #   about the BUILD and no rewording of the ask helps.
                                                        #   Collapsing them would tell a reader to fix
                                                        #   something that is not theirs to fix. ERROR, not
                                                        #   REFUSE: a capability limit is not an analytical
                                                        #   verdict about the data (see `unsupported`).
    "filter_unreachable":       (CLARIFY, AMBIGUOUS, ANALYTICAL),   # a WHERE dimension cannot lawfully reach a series'
                                                        #   input anchor (the filter's grain is not
                                                        #   addressable in that series' universe). MINTED
                                                        #   2026-07-17 (WP-FrameQL envelope, Huayin) — the
                                                        #   envelope's per-series WHERE reachability law; one
                                                        #   reason per contested dimension (OF-1). Detail
                                                        #   names the dimension, the series, and the reachable
                                                        #   alternatives; two-path remedy: restrict the
                                                        #   predicate to reachable dims, or change the series'
                                                        #   input anchor. S1a: registry is the source of truth.
    "family_member_ambiguous":  (CLARIFY, AMBIGUOUS, ANALYTICAL),    # P1-25 (minted 2026-09-01).
                                                        #   A VALID expression naming a measure whose
                                                        #   family has several members, with no
                                                        #   authorized default selecting one: v0.2
                                                        #   §12, several lawful capability readings
                                                        #   -> Clarify. Was `unknown`/ERROR, i.e.
                                                        #   filed as a vocabulary miss — the measure
                                                        #   is known and the ask is well formed; what
                                                        #   is under-determined is WHICH lawful
                                                        #   reduction is meant. An OF-1 sibling of
                                                        #   `input_anchor_ambiguous`: its own
                                                        #   contested dimension, its own reason.
    # ── P1-24 (minted 2026-09-01) · explicit order selection ──────────────────────────────────────
    #   Ruled Huayin: "Explicit `by=` may select governed order standing. It may not create it."
    #   `plan_order_axis` used to begin `if by is not None: return by`, so a named axis was never
    #   validated at all: `by='customer'` — a real level, in the anchor, carrying no governed order —
    #   SERVED, silently walking an axis the unnamed path refuses to derive, and `by='zzz'` fell
    #   through to a bare ColumnNotFoundError reported as a build capability gap. The two reasons
    #   below split what was one unclassified fall-through, per v0.2 §11.
    "order_not_governed":       (REFUSE,  UNSUPPORTED, ANALYTICAL),  # the axis carries no governed
                                                        #   order standing FOR THIS OPERATION: it is
                                                        #   not a coordinate of the frame, or it is
                                                        #   and confers no order. The request is
                                                        #   valid and has no lawful reading — an
                                                        #   analytical Refuse, never a build gap.
                                                        #   Also the no-derivable-axis case, which
                                                        #   was `unknown`/ERROR: |L(Q)| = 0.
    "order_axis_ambiguous":     (CLARIFY, AMBIGUOUS, ANALYTICAL),    # several lawful governed orders
                                                        #   in the anchor and no `by=` selecting one:
                                                        #   |L(Q)| > 1, so Clarify (v0.2 §11). Was
                                                        #   `unknown`/ERROR, which told the caller
                                                        #   the request was malformed when it was
                                                        #   merely under-determined. Sibling of
                                                        #   `input_anchor_ambiguous` under OF-1: a
                                                        #   distinct contested dimension, its own
                                                        #   reason.
    "blocked_reduction":        (REFUSE, UNSUPPORTED, ANALYTICAL), # GENERATED-FAMILY LAW (minted 2026-08-20). A
                                                        #   reduction — written as a declared family member
                                                        #   or GENERATED by an inline reducer above one —
                                                        #   travels a lineage that operator is declared
                                                        #   BLOCKED along. Family generation creates a new
                                                        #   analytical family; it does not create a new
                                                        #   operator permission. This SUPERSEDES ADR-020's
                                                        #   inform-and-serve reading for the B-anchor
                                                        #   crossing: Disclose exists inside the lawful
                                                        #   region and cannot legalize an operation the
                                                        #   governed law does not possess. Shares its
                                                        #   spelling with the CAVEAT code it replaces (one
                                                        #   concept, two channels — the caveat side is now
                                                        #   tombstoned in disclosure_wire.CATEGORY_TABLE).
    "out_of_universe":          (REFUSE, UNSUPPORTED, ANALYTICAL), # addressed outside the contracted space
    "pin_coarser_than_output":  (REFUSE, UNSUPPORTED, ANALYTICAL), # WP-GRAIN-1 Law 1: a composite input anchor pins a
                                                        #   level COARSER than the output grain (output level
                                                        #   `a` reaches pin `p`, a -> p) — a coarser pin cannot
                                                        #   resolve at a finer output without inventing rows it
                                                        #   does not distinguish. Same REFUSE family as
                                                        #   `out_of_universe`, but its OWN dimension per OF-1
                                                        #   (the pin choosing an ill-fitting grain vs a plan
                                                        #   discovering unreachability at run-time), with a
                                                        #   pin-specific teaching message. MINTED 2026-07-30.
    "contradicted_edge":        (REFUSE, UNSUPPORTED, ANALYTICAL), # data violates a declared functional edge (tested+refuted)
    "uncertified_edge":         (REFUSE, UNSUPPORTED, UNRULED), # P0.5a: a declared functional edge that is NOT positively
                                                        #   certified (UNTESTABLE / unadjudicated) — declaration makes
                                                        #   a capability eligible for certification, not executable.
                                                        #   Distinct from `contradicted_edge` (a stronger factual claim:
                                                        #   tested and refuted). MINTED 2026-08-13.
    "uncertified_face":         (REFUSE, UNSUPPORTED, UNRULED), # P0.5a: a declared crossing face that is NOT positively
                                                        #   admitted (license=None / no adjudication / not
                                                        #   VERIFIED|CORROBORATED). Same polarity law as edges.
    # ── TOMBSTONE ── `conflicting_data` was (REFUSE, UNSUPPORTED) — "a declared invariant (ASSERT) the
    #   attested data VIOLATES: the data's own testimony forbids serving the cut region (B1 scope-edit)".
    #   RETIRED 2026-07-26 (the ASSERT retirement, Huayin's ruling): its ONLY producer was the cut region,
    #   and the cut region's only producer was a violated ASSERT — a construct that failed the admission
    #   test (a construct is admitted iff its prover licenses some serving behavior). With ASSERT gone
    #   nothing can cut, so nothing can refuse this way; producer, cut branch and reason left together and
    #   a retirement-pin test asserts it is never emitted. Kept here as a dated tombstone so old transcripts
    #   and docs remain interpretable — vocabularies grow by rule and shrink by tombstone, never silently.
    #   🔒 NOT the same referent as the RESERVED caveat code of the same name (disclosure_wire.py): that one
    #   is RETAINED, reserved and unwired for a possible future soft-assert/disclosed-not-cut path. Same
    #   string, different channel — probe the referent, not the spelling.
    "chained_crossing":         (REFUSE, UNSUPPORTED, REALIZATION), # REGISTERED 2026-08-20 (vocabulary integrity). Was
                                                        #   ORPHANED — emitted at engine.py's G4 chain guard
                                                        #   but absent from this table, so it fell through
                                                        #   `outcome_for`'s silent default and shipped as an
                                                        #   ERROR. Its call site says "chained crossings are
                                                        #   not yet licensed — ask at one frontier at a
                                                        #   time": a well-formed ask with no lawful path, in
                                                        #   the same REFUSE/UNSUPPORTED family as
                                                        #   `uncertified_face`. Registered to its EXISTING
                                                        #   intent, not to a convenient one.
    "anchor_spent":             (REFUSE, UNSUPPORTED, ANALYTICAL), # REGISTERED 2026-08-20 (vocabulary integrity). Also
                                                        #   orphaned; emitted at the G5 anchor law. Its call
                                                        #   site says a distinct-class measure's anchor is
                                                        #   SPENT at the frontier grain — per-member counts
                                                        #   "cannot be summed, weighted, or routed". A
                                                        #   structural prohibition with named alternatives:
                                                        #   REFUSE/UNSUPPORTED, never an ERROR.
    "unsupported":              (ERROR, None, REALIZATION),        # not implemented in this build (capability)
    "type_error":               (ERROR, None, LANGUAGE),        # vocabulary/type failure
    "unknown":                  (ERROR, None, LANGUAGE),        # unknown column / operator / construct
}


class UnregisteredReason(KeyError):
    """A reason string reached classification without a REASON_OUTCOME entry."""


def outcome_for(reason: str):
    """The planner's classification policy: reason -> (kind, discriminator).

    CLOSED, AND FAIL-CLOSED (ruling 2026-08-20 §7). This used to be
    `REASON_OUTCOME.get(reason, (ERROR, None))` — a silent default that let an unregistered reason
    acquire a verdict nobody chose. It was not hypothetical: `chained_crossing` and `anchor_spent`
    both shipped that way for months, classified ERROR when their call sites plainly mean REFUSE.
    That is the precise failure the tombstone doctrine ("vocabularies grow by rule and shrink by
    tombstone, never silently") exists to prevent, and a silent default defeated it from the other
    end. An unregistered reason is now a programming error, raised where it is introduced.

    This is INTERNAL vocabulary integrity. It is not a wire change: `no_result.reason` remains an
    extensible reason string in shape, and CONTRACT_VERSION stays "3"."""
    try:
        return REASON_OUTCOME[reason][:2]
    except KeyError:
        raise UnregisteredReason(
            f"refusal reason {reason!r} has no REASON_OUTCOME entry, so it has no verdict. "
            f"Register it (with a dated note on its intent) rather than letting it default; "
            f"known reasons: {sorted(REASON_OUTCOME)}") from None


UNRULED_REASONS = frozenset({"uncertified_edge", "uncertified_face"})
"""The reasons whose STAGE is an open doctrinal question, listed once so the exception is auditable.

Whether missing positive certification is `|L(Q)| = 0` (analytical Refuse), a Stage-A category
failure, or a realization/evidence gap is precisely the question Ruling 0.1 §9/§13 declined and v0.2
does not reopen. The 2026-09-01 sweep recorded it as "not scored". This set is the honest form of
that: the reasons are registered, so the table stays closed and fail-closed, but no stage is claimed
for them. Shrinking this set requires a ruling, not an implementation decision."""


def jurisdiction_for(reason: str) -> str:
    """The STAGE a reason belongs to (v0.2 §1) — `language` / `analytical` / `realization`, or
    `unruled` for the deliberately open ones.

    Reads the same closed, fail-closed table as `outcome_for`, which is what makes the classification
    exhaustive BY CONSTRUCTION: a reason cannot reach a surface without a jurisdiction, because it
    cannot reach a surface without an entry. That property is the reason this repair is a table edit
    rather than a sweep of call sites."""
    return REASON_OUTCOME[reason][2] if reason in REASON_OUTCOME else outcome_for(reason)


@dataclass(frozen=True)
class Outcome:
    """The structured no-result, as a VALUE — never an exception. This is what flows on
    `ColumnResult.refusal` and what every surface/agent receives: a clarify/refuse/error is data,
    not a thrown error. The engine reports a `reason` (and, for an analytical no-result, a
    `discriminator`); the planner's `classified()` stamps the verdict `kind` ∈ {clarify, refuse,
    error} via the reason policy, at one chokepoint. The engine never sets `kind`."""
    reason: str                      # 'non_functional_transport'(fan-out) | 'ambiguous_grain' |
                                     # 'co_anchor_ambiguous' | 'out_of_universe' |
                                     # 'contradicted_edge' | 'type_error' | 'unknown' | 'unsupported'
    detail: str
    measure: Optional[str] = None
    target: Optional[str] = None
    edge: Optional[str] = None
    alternatives: tuple = ()         # e.g. ("allocation (ROADMAP)", "membership (rephrase)")
    kind: Optional[str] = None       # the planner's verdict; None until classified()
    discriminator: Optional[str] = None   # engine-attached seam: 'ambiguous' | 'unsupported'
    jurisdiction: Optional[str] = None    # v0.2 §1 stage: 'language' | 'analytical' | 'realization'
                                          # (or 'unruled'). INTERNAL — never serialized to the wire.

    def classified(self) -> "Outcome":
        """Planner-side classification (idempotent): stamp (kind, discriminator) from the reason
        policy unless already set. Applied at the planner's single chokepoint, so every no-result —
        the engine's and the planner's own static ones — is verdicted in one place."""
        if self.kind is not None:
            return self if self.jurisdiction is not None else replace(
                self, jurisdiction=jurisdiction_for(self.reason))
        kind, disc = outcome_for(self.reason)
        return replace(self, kind=kind, discriminator=self.discriminator or disc,
                       jurisdiction=self.jurisdiction or jurisdiction_for(self.reason))

    @property
    def _kind(self): return self.kind or outcome_for(self.reason)[0]

    @property
    def is_clarify(self): return self._kind == CLARIFY

    @property
    def is_refuse(self): return self._kind == REFUSE

    @property
    def is_error(self): return self._kind == ERROR

    def __str__(self):
        s = f"{self._kind.upper()} [{self.reason}]: {self.detail}"
        if self.alternatives:
            s += "  | alternatives: " + "; ".join(self.alternatives)
        return s

    def to_structured(self):
        return {"kind": self._kind, "discriminator": self.discriminator or outcome_for(self.reason)[1],
                "reason": self.reason, "detail": self.detail, "measure": self.measure,
                "target": self.target, "edge": self.edge, "alternatives": list(self.alternatives)}


class Refusal(Exception):
    """INTERNAL control-flow signal that *carries* an `Outcome`. It is raised deep in the planner's
    recursive walk to short-circuit to the single assembly chokepoint (`run`/`plan`), where
    `.classified()` yields the `Outcome` VALUE that flows on `ColumnResult.refusal`. This signal is
    plumbing — a structured goto — and is never handed to a surface: a clarify/refuse is the value
    `Outcome`, never this exception. Call sites keep `raise Refusal(reason, detail, ...)` unchanged."""

    def __init__(self, reason, detail, measure=None, target=None, edge=None,
                 alternatives=(), kind=None, discriminator=None, jurisdiction=None):
        # `jurisdiction=` overrides the reason's table default FOR THIS CALL SITE. It exists because
        # jurisdiction is a property of the FAILURE, and one reason string is currently emitted from
        # sites in different stages: `unsupported` carries both a real build gap and the co-anchor
        # LANGUAGE law (P1-23), and `unknown` carries both a genuine vocabulary miss and the family
        # ambiguity that is a Stage-B question (P1-25). Splitting those reasons is Step 4; until then
        # a call site can state its own stage truthfully without minting a reason or changing a mood.
        self.outcome = Outcome(reason, detail, measure, target, edge, alternatives, kind,
                               discriminator, jurisdiction)
        super().__init__(str(self.outcome))

    def classified(self) -> "Outcome":
        """The planner's verdict as a VALUE — what gets stored on `ColumnResult.refusal`."""
        return self.outcome.classified()

    def __getattr__(self, name):
        # convenience: a caught signal reads through to its Outcome (reason, is_clarify, ...)
        if name == "outcome":
            raise AttributeError(name)
        return getattr(self.outcome, name)

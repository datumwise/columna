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
B_ANCHOR_CROSSING = "b_anchor_crossing"   # served, critical: a reduction coarsens a blocked family
DATA_GAP = "data_gap"            # served, material: absent cells are GAPS (spine/product basis, B3)
OVER_COUNT = "over_count"        # served, MATERIAL: a touch-face crossing multi-counts by construction —
                                 # the value reaches every match of an M:N edge, so totals deliberately
                                 # exceed the grand total. Drives DISCLOSE (the honest over-count is the point).

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

    def render(self) -> str:
        if self.category == APPROXIMATION and self.rel_error is not None:
            return f"approximate: {self.detail} (\u00b1{self.rel_error*100:.2g}%)"
        tag = f"[{self.severity.upper()}] " if _SEV_RANK.get(self.severity, 1) >= 2 else ""
        base = f"{tag}{self.category}: {self.detail}"
        return base + (f"  \u2192 remedy: {self.remedy}" if self.remedy else "")


@dataclass(frozen=True)
class Disclosure:
    caveats: tuple = ()
    population: Optional[str] = None     # the universe/sub-population this column resolved over

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

    def with_caveat(self, c): return Disclosure(self.caveats + (c,), self.population)

    @staticmethod
    def merge(*parts, population=None):
        seen, pop = {}, population
        for d in parts:
            if d is None:
                continue
            pop = pop or d.population
            for c in d.caveats:
                seen[(c.category, c.detail, c.rel_error, c.source)] = c
        return Disclosure(tuple(seen.values()), pop)

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
    "non_functional_transport": (CLARIFY, AMBIGUOUS),   # fan-out (M:N): no single total exists
    "ambiguous_grain":          (CLARIFY, AMBIGUOUS),   # attribute keyed at several levels
    # ── TOMBSTONE ── `co_anchor_ambiguous` was (CLARIFY, AMBIGUOUS) — "ratio over >1 population: rate's
    #   population ambiguous". RETIRED 2026-07-16 (§2c expression law, Huayin's ruling): a cross-universe
    #   expression is a language-law CATEGORY ERROR, not a clarify (see `cross_universe` below); within one
    #   universe the denotation rule leaves nothing ambiguous. Its emitter left the language entirely and a
    #   retirement-pin test asserts it is never emitted. Kept here as a dated tombstone so old transcripts
    #   and docs remain interpretable — vocabularies grow by rule and shrink by tombstone, never silently.
    "cross_universe":           (ERROR,   None),        # a column expression combines measures from >1
                                                        #   universe (§2c expression law: a column evaluates in
                                                        #   ONE universe, never crosses the boundary). A category
                                                        #   error — rides the ERROR channel, not the four moods.
                                                        #   Minted 2026-07-16 (§2c). Remedy: juxtapose or declare.
    "input_anchor_ambiguous":   (CLARIFY, AMBIGUOUS),   # inline reduction with no pinned input anchor:
                                                        #   the grain to resolve the inner at is under-
                                                        #   determined (names the same dimension OF-2's
                                                        #   immaterial input-anchor note records)
    "filter_unreachable":       (CLARIFY, AMBIGUOUS),   # a WHERE dimension cannot lawfully reach a series'
                                                        #   input anchor (the filter's grain is not
                                                        #   addressable in that series' universe). MINTED
                                                        #   2026-07-17 (WP-FrameQL envelope, Huayin) — the
                                                        #   envelope's per-series WHERE reachability law; one
                                                        #   reason per contested dimension (OF-1). Detail
                                                        #   names the dimension, the series, and the reachable
                                                        #   alternatives; two-path remedy: restrict the
                                                        #   predicate to reachable dims, or change the series'
                                                        #   input anchor. S1a: registry is the source of truth.
    "out_of_universe":          (REFUSE,  UNSUPPORTED), # addressed outside the contracted space
    "contradicted_edge":        (REFUSE,  UNSUPPORTED), # data violates a declared functional edge
    "conflicting_data":         (REFUSE,  UNSUPPORTED), # a declared invariant (ASSERT) the attested data
                                                        # VIOLATES: the data's own testimony forbids serving
                                                        # the cut region (B1 scope-edit). MINTED here per the
                                                        # one-reason-per-contested-dimension rule (Huayin,
                                                        # 2026-07-15) — a violated invariant is a genuinely
                                                        # new contested dimension, sibling to
                                                        # `contradicted_edge` (a declared edge violated).
                                                        # Refuse/UNSUPPORTED matches that sibling's pair. The
                                                        # name is shared with the RESERVED caveat code
                                                        # (disclosure_wire) — one concept, two channels; the
                                                        # caveat code stays reserved-and-unwired.
    "unsupported":              (ERROR,   None),        # not implemented in this build (capability)
    "type_error":               (ERROR,   None),        # vocabulary/type failure
    "unknown":                  (ERROR,   None),        # unknown column / operator / construct
}


def outcome_for(reason: str):
    """The planner's classification policy: reason -> (kind, discriminator)."""
    return REASON_OUTCOME.get(reason, (ERROR, None))


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
    alternatives: tuple = ()         # e.g. ("allocation (Pro)", "membership (rephrase)")
    kind: Optional[str] = None       # the planner's verdict; None until classified()
    discriminator: Optional[str] = None   # engine-attached seam: 'ambiguous' | 'unsupported'

    def classified(self) -> "Outcome":
        """Planner-side classification (idempotent): stamp (kind, discriminator) from the reason
        policy unless already set. Applied at the planner's single chokepoint, so every no-result —
        the engine's and the planner's own static ones — is verdicted in one place."""
        if self.kind is not None:
            return self
        kind, disc = outcome_for(self.reason)
        return replace(self, kind=kind, discriminator=self.discriminator or disc)

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
                 alternatives=(), kind=None, discriminator=None):
        self.outcome = Outcome(reason, detail, measure, target, edge, alternatives, kind, discriminator)
        super().__init__(str(self.outcome))

    def classified(self) -> "Outcome":
        """The planner's verdict as a VALUE — what gets stored on `ColumnResult.refusal`."""
        return self.outcome.classified()

    def __getattr__(self, name):
        # convenience: a caught signal reads through to its Outcome (reason, is_clarify, ...)
        if name == "outcome":
            raise AttributeError(name)
        return getattr(self.outcome, name)

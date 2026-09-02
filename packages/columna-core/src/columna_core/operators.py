"""
columna_core.operators — the operator registry, as ONE umbrella (the shared extension point).

Per the Frame-QL Manual (Appendix A): the registry is the *planner's contract with the engine*.
It holds three KINDS of operator under one roof — REDUCER, SCAN, MAP — and for each it records
the name, the kind, and the type signature (accepts / out_rule). The planner reads exactly this to
TYPECHECK an operator against its inputs and to ROUTE it by kind:

    KIND      planner routing                         where the mechanics live
    REDUCER   decompose into an atom op(in)@out  ->   engine.resolve  (deliver/transport/reduce)
    SCAN      hand to the engine with an order   ->   engine.scan     (order-preserving)
    MAP       evaluate inline over co-anchored   ->   planner._apply  (point-wise, post-agg)
              results

The *mechanics* — how `sum` combines, how an HLL sketch merges, how `cumsum` walks an order —
live in the engine (or, for maps, in the planner's point-wise evaluator); never in the registry.
This is the same logical/physical split the type system uses: the registry is vocabulary; the
engine is implementation. Custom operators/types [ROADMAP] are new entries here — which is why a new
operator needs no change to the planner's machinery, only a registry entry the planner can read.

Reaggregability is an OPERATOR-level property of REDUCERS: whether `median` re-derives at a
coarser grain is a fact about `median`, not the column. The property is **monoid-ness** — an
associative combine with identity — because op@fine -> op@coarse means combining partial results:

    reducer         witness (cached representation)   combine        project
    sum, count      the value                         +              identity
    min, max        the value                         min / max      identity
    distinct        an HLL sketch                     union          get_estimate
    last, first     (value, order_key)                argmax/argmin  take value
    median, mode    — (no finite witness closes it)   —              —   (HOLISTIC)

A holistic reducer carries no finite witness, so it is reduction-sterile (recomputed from base).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Callable
from .types import NUMERIC, TEMPORAL, ORDERED, ANY, DURATION, HLLSKETCH, dtype_in

# operator KINDS (the umbrella)
REDUCER, SCAN, MAP = "reducer", "scan", "map"

# reducer witness kinds
VALUE, SKETCH, ORDERED_W, HOLISTIC = "value", "sketch", "ordered", "holistic"
# (ORDERED_W is the witness kind for last/first; distinct from types.ORDERED the type class)


@dataclass(frozen=True)
class Operator:
    name: str
    kind: str = REDUCER                  # REDUCER | SCAN | MAP  (the umbrella discriminant)
    witness: str = VALUE                 # REDUCER mechanics: VALUE | SKETCH | ORDERED_W | HOLISTIC
    is_monoid: bool = True               # REDUCER: HOLISTIC => False (reduction-sterile)
    linear: bool = False                 # ALGEBRAIC (WP-B math channel): preserves linear combinations —
                                         #   distributes over addition (sum-fertility's symbolic gate).
                                         #   True for `sum` (additive monoid) and the maps +,-,neg.
                                         #   `*`,`/` are conditionally linear: only when one operand is a
                                         #   scalar (literal/declared constant) — the AST scalar-operand
                                         #   rule handles that, so the operator flag itself stays False.
    accepts: frozenset = ANY             # SIGNATURE (vocabulary): input dtypes this op accepts
    out_rule: str = "same"               # SIGNATURE: output dtype — "same", a dtype tag, or "numeric_widen"
    deliver_sql: Optional[Callable] = None   # REDUCER mechanics: (realized_expr) -> SQL agg (engine-side)
    combine: Optional[str] = None        # REDUCER: how witnesses merge (engine-side mechanics)
    needs_order: bool = False            # SCAN / ordered REDUCER: requires an order axis
    needs_window: bool = False           # SCAN: requires a `window=` parameter (rolling_*)
    scan_impl: Optional[str] = None      # SCAN mechanics tag the engine dispatches on (None => not in Core)
    in_core: bool = True                 # False => recognized by the planner (contract) but not executed by Core


def output_dtype(op: "Operator", in_dtype: Optional[str]) -> Optional[str]:
    """The operator's output logical dtype, from its signature."""
    if op.out_rule == "same":
        return in_dtype
    if op.out_rule == "numeric_widen":      # binary numeric: caller resolves the widening
        return in_dtype
    return op.out_rule


# ── the umbrella registry ────────────────────────────────────────────────────
REGISTRY: dict = {
    # ---- REDUCERS (found families; reaggregate by monoid structure) ----------
    "sum":   Operator("sum",   REDUCER, VALUE, True, linear=True, accepts=NUMERIC | {DURATION}, out_rule="same",
                      deliver_sql=lambda p: f"sum({p})",  combine="sum"),
    # P1-10. This delivered `count(*)` — DISCARDING its operand — so `count` as a family member over a
    # declared VALUE counted ROWS while its siblings (`sum`/`min`/`max`, and SQL generally) count
    # OBSERVATIONS. Two members of one family therefore carried different supports, and
    # `revenue.sum / revenue.count` served a mean over mismatched denominators, silently.
    #
    # THE DISTINCTION WAS ALREADY DECLARED; only the delivery threw it away. The parser normalizes the
    # AS-form `count(...)` to `pre_expr = "1"` (`parser.py:453` — in that form `count` MEANS rows), while
    # the VALUE+FAMILY form carries the declared value expression. So passing the operand through
    # honours both readings with one lambda: `count(1)` is exactly `count(*)` (a literal is never null,
    # verified against DuckDB), and `count(<value>)` is the observation count its siblings already use.
    # The engine's own inline path had it right all along — `_SERIES_REDUCE["count"]` is polars
    # `.count()`, which skips nulls.
    "count": Operator("count", REDUCER, VALUE, True, accepts=ANY, out_rule="Int64",
                      deliver_sql=lambda p: f"count({p})", combine="sum"),
    "min":   Operator("min",   REDUCER, VALUE, True, accepts=ORDERED, out_rule="same",
                      deliver_sql=lambda p: f"min({p})",  combine="min"),
    "max":   Operator("max",   REDUCER, VALUE, True, accepts=ORDERED, out_rule="same",
                      deliver_sql=lambda p: f"max({p})",  combine="max"),
    # `mean` is a REDUCER in the governance sense — it GENERATES an analytical family and reduces a
    # series onto a coarser anchor — but it is deliberately NOT a monoid: a displayed average does not
    # combine associatively, and mean-of-means is not a mean. Its witness is HOLISTIC (recompute in one
    # pass over the remapped series), which is exactly the semantics the inline reducer already ships
    # (`ColumnEngine._SERIES_REDUCE["mean"]` aggregates the whole finer series ONCE). `in_core=False`:
    # Core does not serve `mean` as a DECLARED measure family member (the holistic recompute path
    # implements median/mode only) — this entry exists so `(operator x lineage)` law has an ADDRESS for
    # the inline average, NOT to define new arithmetic.
    # Registered 2026-08-20 (generated-family law): before this, `avg`/`mean` was recognized by the
    # planner's hardcoded inline table and by NOTHING in the registry, so `mean BLOCKED { <lineage> }`
    # was unparseable and every mean-generated successor was ungovernable.
    "mean":  Operator("mean",  REDUCER, HOLISTIC, False, accepts=NUMERIC | {DURATION}, out_rule="Float64",
                      deliver_sql=lambda p: f"avg({p})", in_core=False),
    "distinct": Operator("distinct", REDUCER, SKETCH, True, accepts=ANY, out_rule="Int64", combine="union"),
    # ---- the distinct family, decomposed: a custom TYPE (HLLSketch) + three custom operators.
    # `distinct` above is the friendly default-family spelling; the engine composes it from these.
    # Registering them here (vocabulary) — and nowhere in the planner — is the extensibility claim:
    # a new type and new operators slot into the umbrella by registry + engine, planner untouched.
    "hll_count":    Operator("hll_count", REDUCER, SKETCH, True, accepts=ANY, out_rule="HLLSketch",
                             combine="union"),                       # deliver: any -> HLLSketch(p)
    "hll_merge":    Operator("hll_merge", REDUCER, SKETCH, True, accepts=frozenset({HLLSKETCH}), out_rule="same",
                             combine="union"),                       # combine: monoid union, HLLSketch -> HLLSketch
    "hll_estimate": Operator("hll_estimate", MAP, accepts=frozenset({HLLSKETCH}), out_rule="Int64"),  # project: HLLSketch -> Int64
    "last":  Operator("last",  REDUCER, ORDERED_W, True, accepts=ANY, out_rule="same",
                      combine="argmax", needs_order=True),
    "first": Operator("first", REDUCER, ORDERED_W, True, accepts=ANY, out_rule="same",
                      combine="argmin", needs_order=True),
    "median": Operator("median", REDUCER, HOLISTIC, False, accepts=NUMERIC | TEMPORAL, out_rule="same",
                       deliver_sql=lambda p: f"median({p})"),
    "mode":  Operator("mode",  REDUCER, HOLISTIC, False, accepts=ANY, out_rule="same",
                      deliver_sql=lambda p: f"mode({p})"),

    # ---- MAP functions (point-wise; evaluated inline by the planner) ---------
    # In the registry so the planner typechecks/routes maps from one contract, not a hardcoded set.
    # Mechanics (the actual arithmetic) are the planner's point-wise evaluator — the one place a
    # map's "how" sits planner-side, because a map is post-agg and anchor-preserving.
    "+":   Operator("+",   MAP, linear=True,  accepts=NUMERIC, out_rule="numeric_widen"),
    "-":   Operator("-",   MAP, linear=True,  accepts=NUMERIC, out_rule="numeric_widen"),
    "*":   Operator("*",   MAP, linear=False, accepts=NUMERIC, out_rule="numeric_widen"),  # conditional: scalar-operand rule
    "/":   Operator("/",   MAP, linear=False, accepts=NUMERIC, out_rule="Float64"),        # conditional: scalar divisor rule
    "neg": Operator("neg", MAP, linear=True,  accepts=NUMERIC, out_rule="same"),

    # ---- SCAN functions (order-dependent, anchor-preserving) -----------------
    # The planner does not know how to execute these; it routes them to the engine with a derived
    # order (partition by the non-ordered anchor dims, order by the orderable axis). Order-only
    # scans are implemented in Core; windowed (rolling_*) scans are registered as CONTRACT but
    # not implemented in this build [ROADMAP] (needs_window, in_core=False).
    "cumsum":  Operator("cumsum",  SCAN, accepts=NUMERIC, out_rule="same", needs_order=True, scan_impl="cumsum"),
    "cummax":  Operator("cummax",  SCAN, accepts=ORDERED, out_rule="same", needs_order=True, scan_impl="cummax"),
    "cummin":  Operator("cummin",  SCAN, accepts=ORDERED, out_rule="same", needs_order=True, scan_impl="cummin"),
    "lag":     Operator("lag",     SCAN, accepts=ANY,     out_rule="same", needs_order=True, scan_impl="lag"),
    "lead":    Operator("lead",    SCAN, accepts=ANY,     out_rule="same", needs_order=True, scan_impl="lead"),
    "pct_change": Operator("pct_change", SCAN, accepts=NUMERIC, out_rule="Float64", needs_order=True, scan_impl="pct_change"),
    # windowed scans — contract present, mechanics [ROADMAP] (require a window= parameter)
    "rolling_sum":  Operator("rolling_sum",  SCAN, accepts=NUMERIC, out_rule="same",
                             needs_order=True, needs_window=True, in_core=False),
    "rolling_mean": Operator("rolling_mean", SCAN, accepts=NUMERIC, out_rule="Float64",
                             needs_order=True, needs_window=True, in_core=False),
}


# ── ONE canonical operator identity, several surface spellings ───────────────
# Frame-QL spells the inline average `avg`; the canonical governed operator is `mean`. This is an
# ALIAS, not a second operator: `avg` and `mean` name the SAME law subject, so a BLOCKED/FERTILE
# declaration written against `mean` governs both spellings and there is exactly one thing to declare.
#
# `approx_distinct` -> `distinct` (ruled Huayin, 2026-09-01). ONE CAPABILITY, TWO ROLES:
#   Frame-QL surface spelling : approx_distinct   — the honest name. The answer IS approximate: an
#                               HLL-backed estimate carrying a relative-standard-error disclosure.
#   Core capability identity  : distinct          — the implementation/legacy name, composed by the
#                               engine from hll_count -> hll_merge -> hll_estimate.
# The Manual keeps `approx_distinct` and is NOT renamed to `distinct`: renaming would make an
# approximate result sound exact to satisfy a registry spelling, which is the wrong direction of
# repair. Declared here because ALIASES is where "one law subject, several spellings" is already
# said — so a BLOCKED/FERTILE declaration written against either name governs both.
#
# NOT YET A RESOLUTION PATH. `canonical()` is not wired into member/operator lookup (the live
# call-position table is `Planner._INLINE_REDUCERS`), so writing `visitors.approx_distinct` in a
# query does not resolve today; the shipped spelling is `visitors.distinct`. This declares the
# IDENTITY, which is what the ruling asked for; making the canonical surface spelling resolve is a
# separate change and is reported, not smuggled in here.
ALIASES: dict = {"avg": "mean", "approx_distinct": "distinct"}


def canonical(name: str) -> str:
    """The canonical registry name for a surface spelling (`avg` -> `mean`); identity otherwise."""
    return ALIASES.get(name, name)


# The planner<->engine contract for INLINE GENERATED reductions: the reducers that can collapse an
# already-resolved series onto a coarser anchor. The engine's `_SERIES_REDUCE` must cover exactly this
# set (asserted by test) — that agreement is what keeps the EXECUTABLE reducer vocabulary and the
# GOVERNABLE reducer vocabulary from drifting apart, which is how `mean` came to have no law slot.
SERIES_REDUCERS: frozenset = frozenset({"sum", "mean", "min", "max", "count"})


def get_operator(name: str) -> Operator:
    if name not in REGISTRY:
        raise KeyError(f"operator '{name}' is not in the registry "
                       f"(registry: {sorted(REGISTRY)}); custom operators are [ROADMAP]")
    return REGISTRY[name]


def kind_of(name: str) -> str:
    return REGISTRY[name].kind if name in REGISTRY else None


def reducers() -> list:
    return [n for n, op in REGISTRY.items() if op.kind == REDUCER]


def signature_ok(op: "Operator", in_dtype: str) -> bool:
    """Does this operator accept a column of the given logical dtype? Sketch-aware: a raw
    HLLSketch(p) matches only operators that list the sketch family — numeric ops reject it."""
    return dtype_in(in_dtype, op.accepts)

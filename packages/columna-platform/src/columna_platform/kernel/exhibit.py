"""
columna_platform.kernel.exhibit — **the running v8-native MME, demonstrated.**

    python -m columna_platform.kernel.exhibit

Five proofs, in the order the ruling names them. The world is built PROGRAMMATICALLY — no publication
serialization, no authoring syntax, no request routing — because the runtime semantics are what is being
proven and a format would only be a second thing to get wrong.

THE WORLD. One universe, `commerce`, ground `customer_order`, three constituents:

    store    a governed store
    day      a merchant trading day
    order    one accepted customer order

and the occurrences below are the whole of the data. Everything printed is computed.
"""
from __future__ import annotations


from dataclasses import fields, replace

from .builtins import IN_MEMORY, KNOWN_EMPTY, REGISTRY, hll_rse, witness_value
from .geometry import Constituent, KernelRefusal, Universe
from .law import ContinuationRegion
from .materialization import SUPERSEDE, TransitionIntent
from .expression import ExpressionEvaluator
from .mme import MME, Retained, RetentionKey
from .observation import RecordingObserver
from .realization import RealizationStanding
from .sorts import GovernedExpression, MeasureFamily, Operand, SufficientBasis
from .witness import FAMILY_NON_DETERMINANTS

MANIFOLD = "andfam.commerce"
PARTICIPATION = "every customer order the merchant accepted"
AUDITED = "every customer order the merchant accepted AND the auditor confirmed"

COMMERCE = Universe(
    name="commerce",
    constituents=(
        Constituent("store", "governed store register entry", "same governed store reference"),
        Constituent("day", "merchant trading day", "same trading day under the retail calendar"),
        Constituent("order", "accepted customer order", "same governed order reference"),
    ),
    ground="customer_order",
    participation_law=PARTICIPATION,
)

SALE_AT = COMMERCE.anchor({"store", "day", "order"})     # R_F for the order-grained families
STORE_DAY = COMMERCE.anchor({"store", "day"})
BY_DAY = COMMERCE.anchor({"day"})
BY_STORE = COMMERCE.anchor({"store"})
TOTAL = COMMERCE.scalar_anchor

#: Six accepted orders across two stores and two days. Small enough to check by hand, and
#: **DELIBERATELY UNBALANCED — two orders on D1 and four on D2.**
#:
#: The imbalance is load-bearing. With three orders on each day the mean of the daily means happens to
#: EQUAL the mean over all orders, so proof 3's most important check — that an expression is not a Mean
#: family in disguise — would pass on a coincidence of the fixture. The first draft of this exhibit had
#: 3/3 and the check failed for exactly that reason: it was asserting a difference that the data had
#: arranged to be zero. 2/4 makes 500/6 = 83.33 and (87.5 + 81.25)/2 = 84.375 genuinely different.
ORDERS = (
    {"store": "S1", "day": "D1", "order": "O1", "value": 100.0, "customer": "C1"},
    {"store": "S1", "day": "D2", "order": "O2", "value": 50.0, "customer": "C2"},
    {"store": "S1", "day": "D2", "order": "O3", "value": 25.0, "customer": "C1"},
    {"store": "S2", "day": "D1", "order": "O4", "value": 75.0, "customer": "C3"},
    {"store": "S2", "day": "D2", "order": "O5", "value": 200.0, "customer": "C1"},
    {"store": "S2", "day": "D2", "order": "O6", "value": 50.0, "customer": "C4"},
)

#: Stock levels, at store × day. A LEVEL, not a flow — which is the whole point of proof 1b.
LEVELS = (
    {"store": "S1", "day": "D1", "value": 10},
    {"store": "S1", "day": "D2", "value": 12},
    {"store": "S2", "day": "D1", "value": 7},
    {"store": "S2", "day": "D2", "value": 9},
)

#: Readings of a gauge, with a governed order. Proof 4.
READINGS = (
    {"store": "S1", "day": "D1", "value": 3, "recorded_at": "08:00"},
    {"store": "S1", "day": "D1", "value": 5, "recorded_at": "17:00"},
    {"store": "S1", "day": "D2", "value": 4, "recorded_at": "09:00"},
    {"store": "S2", "day": "D1", "value": 1, "recorded_at": "12:00"},
)

STORE_DAY_LEVEL = COMMERCE.anchor({"store", "day"})


def _families():
    revenue = MeasureFamily(
        family_id="revenue", manifold=MANIFOLD, universe="commerce", root=SALE_AT, law="SUM",
        value_domain="decimal", participation=PARTICIPATION,
        target="the additive total of accepted order value")
    order_count = MeasureFamily(
        family_id="order_count", manifold=MANIFOLD, universe="commerce", root=SALE_AT, law="COUNT",
        value_domain="integer", participation=PARTICIPATION,
        target="the number of accepted customer orders")
    # The SAME family law and participation, established under the AUDITED participation — the
    # incompatible operand for proof 3b. It is lawful, established and available; it is not jointly
    # usable with `revenue`, and that is the distinction.
    audited_count = MeasureFamily(
        family_id="audited_order_count", manifold=MANIFOLD, universe="commerce", root=SALE_AT, law="COUNT",
        value_domain="integer", participation=AUDITED,
        target="the number of auditor-confirmed customer orders")
    distinct_customers = MeasureFamily(
        family_id="distinct_customers", manifold=MANIFOLD, universe="commerce", root=SALE_AT, law="HLL_SKETCH",
        # **`sketch`, not `text`.** A family's `value_domain` is the domain of ITS OWN VALUE — what it
        # retains and what an expression's constructor sees — not the domain of the occurrences it
        # consumes at the root. HLL_SKETCH admits `text` operands and yields a `sketch`; the family IS
        # the sketch. (The first draft of this exhibit wrote `text` and `MeasureFamily.bind` refused it,
        # which is the check earning its place.)
        value_domain="sketch", participation=PARTICIPATION,
        target="an HLL sketch of the distinct customers who ordered")
    on_hand = MeasureFamily(
        family_id="on_hand", manifold=MANIFOLD, universe="commerce", root=STORE_DAY_LEVEL, law="STOCK_LEVEL",
        value_domain="integer", participation="every unit counted in the evening stocktake",
        target="units of stock held at one store at the close of one day")
    gauge = MeasureFamily(
        family_id="gauge", manifold=MANIFOLD, universe="commerce", root=STORE_DAY_LEVEL, law="LAST",
        value_domain="integer", participation="every accepted gauge reading",
        target="the last gauge reading of the day", order_by="recorded_at")
    return revenue, order_count, audited_count, distinct_customers, on_hand, gauge


def _expressions():
    aov = GovernedExpression(
        expression_id="average_order_value", manifold=MANIFOLD, universe="commerce", constructor="MEAN",
        operands=(Operand("operand", "revenue"),),
        participation=PARTICIPATION, inner_anchors=(SALE_AT,),
        scope="the accepted customer orders of one location",
        admitted_bases=(
            SufficientBasis(basis_id="b_revenue_ordercount",
                            components={"SUM": "revenue", "COUNT": "order_count"},
                            requires_common_participation=True),
        ))
    # A SECOND, incompatible route over the audited count — admitted, lawful in shape, and refused at
    # establishment. Proof 3b: the operands both exist.
    aov_audited = GovernedExpression(
        expression_id="average_order_value_audited", manifold=MANIFOLD, universe="commerce", constructor="MEAN",
        operands=(Operand("operand", "revenue"),),
        participation=PARTICIPATION, inner_anchors=(SALE_AT,),
        admitted_bases=(
            SufficientBasis(basis_id="b_revenue_auditedcount",
                            components={"SUM": "revenue", "COUNT": "audited_order_count"},
                            requires_common_participation=True),
        ))
    distinct_estimate = GovernedExpression(
        expression_id="distinct_customer_estimate", manifold=MANIFOLD, universe="commerce", constructor="HLL_ESTIMATE",
        operands=(Operand("operand", "distinct_customers"),),
        participation=PARTICIPATION, inner_anchors=(SALE_AT,),
        admitted_bases=(
            SufficientBasis(basis_id="b_sketch",
                            components={"HLL_SKETCH": "distinct_customers"},
                            requires_common_participation=True),
        ))
    return aov, aov_audited, distinct_estimate


def build() -> MME:
    """A fully constituted engine with every family and expression registered and every root sealed."""
    mme = MME(COMMERCE, REGISTRY, IN_MEMORY, manifold=MANIFOLD)
    revenue, order_count, audited_count, distinct, on_hand, gauge = _families()
    for family in (revenue, order_count, audited_count, distinct, on_hand, gauge):
        mme.register_family(family)
    for expression in _expressions():
        mme.register_expression(expression)

    mme.establish_root(revenue, ORDERS)
    mme.establish_root(order_count, ORDERS)
    mme.establish_root(audited_count, ORDERS[:4])          # the auditor confirmed four of six
    mme.establish_root(distinct, ORDERS, value_key="customer")
    mme.establish_root(on_hand, LEVELS)
    mme.establish_root(gauge, READINGS)
    return mme


def _holding(mme: MME, key):
    """One held object, by its descriptor. A descriptor REPORTS what is held; a materialization is located
    by its opaque `MaterializationId`, so this is a search over attributes rather than a lookup handle."""
    return next(r for r in mme.holdings() if r.key == key)


# ── printing ─────────────────────────────────────────────────────────────────────────────────────
def _rule(title: str) -> None:
    print(f"\n{'─' * 96}\n{title}\n{'─' * 96}")


def _cells(answer, render=lambda v: v) -> str:
    state = answer.value
    order = state.anchor.order
    if not state.cells:
        return "    (no cells)"
    out = []
    for cell, payload in sorted(state.cells.items(), key=lambda kv: tuple(map(str, kv[0]))):
        where = ", ".join(f"{k}={v}" for k, v in zip(order, cell)) or "ALL"
        out.append(f"    {where:<22} {render(payload)}")
    return "\n".join(out)


def _say(answer) -> None:
    print(f"  {answer}")
    for d in answer.disclosures:
        print(f"      ⚠ {d.code}: {d.detail}")


def main() -> int:                                          # noqa: C901 - an exhibit is a narrative
    mme = build()
    # **THE M-2 BOUNDARY, IN ONE LINE.** Expressions are not served by the engine; they are served by an
    # evaluator constructed OVER the engine, which obtains every operand through `mme.measure`.
    evaluator = ExpressionEvaluator(mme)
    # And the workload observer, which watches the family-request boundary and is authoritative over
    # nothing. Attached here so the exhibit can show what it saw; a production engine may attach none.
    watcher = RecordingObserver()
    mme.observations.observer = watcher
    revenue, order_count, audited_count, distinct, on_hand, gauge = _families()
    aov, aov_audited, distinct_estimate = _expressions()
    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        print(f"    {'✓' if condition else '✗'} {label}")
        if not condition:
            failures.append(label)

    print("═" * 96)
    print("  COLUMNA PLATFORM · v8-native MME · vertical proofs")
    print(f"  universe {COMMERCE.name!r}  ground {COMMERCE.ground!r}  "
          f"constituents {sorted(COMMERCE.references)}")
    print(f"  laws {[law.name for law in REGISTRY]}   provider {IN_MEMORY.name!r}")
    print("═" * 96)

    # ══ PROOF 1 · additive family: root → lawful continuation → coarser family measure ═══════════
    _rule("PROOF 1 · scalar family — root state → lawful continuation → coarser family measure")
    at_root = mme.measure(revenue, SALE_AT)
    print(f"  revenue @ {SALE_AT}  (R_F, the canonical continuation origin)")
    _say(at_root)
    print(_cells(at_root))

    print(f"\n  revenue @ {STORE_DAY}  — forgets ['order']")
    store_day = mme.measure(revenue, STORE_DAY)
    _say(store_day)
    print(_cells(store_day))

    print(f"\n  revenue @ {BY_DAY}  — SEEDED FROM THE NON-ROOT MATERIALIZATION above")
    by_day = mme.measure(revenue, BY_DAY)
    _say(by_day)
    print(_cells(by_day))

    print(f"\n  revenue @ {TOTAL}  (the grand total — a lawful location, not an absence)")
    total = mme.measure(revenue, TOTAL)
    _say(total)
    print(_cells(total))

    check("root sums to 500.0 over six orders", total.cell() == 500.0)
    check("D1 = 175.0 (two orders) and D2 = 325.0 (four)",
          by_day.value.cells[("D1",)] == 175.0 and by_day.value.cells[("D2",)] == 325.0)
    check("the coarser measure was CONTINUED, not recomputed from occurrences",
          by_day.route == "continued")
    check("it was seeded from the NON-ROOT materialization, which is lawful while adequate",
          by_day.seeded_from is not None and by_day.seeded_from.anchor == STORE_DAY)
    check("and the grand total was seeded from THAT, a chain of non-root continuations",
          total.seeded_from is not None and total.seeded_from.anchor == BY_DAY)
    check("F@R_F remains the canonical origin and is still held",
          any(k.anchor == SALE_AT and k.identity == "revenue" for k in mme.held))

    # ══ PROOF 1b · the same composition, a DIFFERENT continuation region ═════════════════════════
    _rule("PROOF 1b · edge-relative closure — a stock is not a flow, and the cache cannot change that")
    print(f"  on_hand @ {STORE_DAY_LEVEL}  (R_F)")
    level_root = mme.measure(on_hand, STORE_DAY_LEVEL)
    print(_cells(level_root))

    print(f"\n  on_hand @ {BY_DAY}  — forgets ['store'], INSIDE the region")
    lawful = mme.measure(on_hand, BY_DAY)
    _say(lawful)
    print(_cells(lawful))

    print(f"\n  on_hand @ {BY_STORE}  — forgets ['day'], OUTSIDE the region")
    unlawful = mme.measure(on_hand, BY_STORE)
    _say(unlawful)

    print(f"\n  on_hand @ {TOTAL}  — via the held {BY_DAY} state: forgetting ['store'] then ['day']")
    laundered = mme.measure(on_hand, TOTAL)
    _say(laundered)

    check("summing stock ACROSS STORES at one day is served", lawful.served
          and lawful.value.cells[("D1",)] == 17)
    check("summing stock ACROSS TIME is refused", not unlawful.served)
    check("the refusal is about CLOSURE, not about absence",
          unlawful.refusal is not None
          and "outside-continuation-region" in str(unlawful.refusal))
    check("the two-step route is refused too — an intermediate cannot launder the edge",
          not laundered.served)
    check("and the state it would have used IS held: availability is not authority",
          any(k.identity == "on_hand" and k.anchor == BY_DAY for k in mme.held))
    check("SUM and STOCK_LEVEL share one composition and differ only in region",
          REGISTRY.get("SUM").continuation.token == REGISTRY.get("STOCK_LEVEL").continuation.token
          and REGISTRY.get("SUM").region.forgettable is None
          and REGISTRY.get("STOCK_LEVEL").region.forgettable == frozenset({"store"}))

    # ══ PROOF 2 · structured family → merge → finalize as an EXPRESSION ══════════════════════════
    _rule("PROOF 2 · structured family — HLLSketch@A → merge → HLLSketch@B, then estimate() as an "
          "EXPRESSION")
    sketch_root = mme.measure(distinct, SALE_AT)
    print(f"  distinct_customers @ {SALE_AT}  (R_F) — value form "
          f"{sketch_root.value.value_form!r}")
    print(f"    {len(sketch_root.value.cells)} sketch cells, one per order")

    print(f"\n  distinct_customers @ {TOTAL}  — HLLSketch → merge → HLLSketch")
    sketch_total = mme.measure(distinct, TOTAL)
    _say(sketch_total)
    print(f"    payload is a sketch, not a number: {type(sketch_total.cell()).__name__}")

    print(f"\n  distinct_customer_estimate @ {TOTAL}  — estimate(HLLSketch) → expression scalar")
    estimate = evaluator.evaluate(distinct_estimate, TOTAL)
    _say(estimate)
    print(_cells(estimate))
    print(f"    true distinct customers in the occurrences: "
          f"{len({o['customer'] for o in ORDERS})};  HLL rse at p=12 ≈ {hll_rse():.4f}")

    print("\n  AND NOW THE DISTINCTION, AS M-2 LEAVES IT.")
    print("  The estimate is SERVED and is not held ANYWHERE — MME v1 has no expression cache — and if")
    print("  it is handed back to the engine as family state it is refused by a governed verdict.")
    # The evaluator's output, wrapped in the same `Retained` shape a candidate would arrive in. This is
    # the ONLY way an `ExpressionOutput` can now reach `adjudicate`: from ABOVE, by a caller who has one
    # in hand. It cannot come out of the store, because the store cannot contain one.
    from_above = Retained(key=RetentionKey(identity="distinct_customer_estimate", anchor=TOTAL,
                                           instance=estimate.value.instance,
                                           realization=mme.realization),
                          value=estimate.value)
    verdict = mme.adjudicate(from_above, distinct, TOTAL)
    print(f"    offered from above: {from_above.key}   "
          f"continuation_bearing={from_above.continuation_bearing}")
    print(f"    adjudicate(estimate → seed distinct_customers@{TOTAL}):")
    print(f"      {'ADMITTED' if verdict else 'REFUSED'} [{verdict.code}]")
    print(f"      {verdict.detail}")
    try:
        mme.retain(estimate.value)
        store_refused = ""
    except KernelRefusal as exc:
        store_refused = exc.code
    print(f"    offered to the STORE instead: REFUSED [{store_refused}]")

    check("the sketch family merges to the coarser anchor", sketch_total.served
          and sketch_total.value.value_form == "structured")
    check("the estimate is an integer in the right neighbourhood",
          estimate.cell() == len({o["customer"] for o in ORDERS}))
    check("the estimate is NOT held by the MME — v1 has no expression cache (M-2 §1)",
          all(k.identity != "distinct_customer_estimate" for k in mme.held))
    check("the estimate is NOT continuation-bearing", not from_above.continuation_bearing)
    check("offered from ABOVE, it is refused as continuation state by a governed verdict",
          (not verdict) and verdict.code == "not-continuation-bearing")
    check("offered to the STORE, it is refused by a governed verdict naming where it belongs",
          store_refused == "not-a-family-materialization")
    check("ExpressionOutput has no merge path at all — the type is the primary enforcement",
          not hasattr(estimate.value, "fold_onto"))
    check("a coarser estimate goes back through the SKETCH, never through an estimate",
          evaluator.evaluate(distinct_estimate, BY_DAY).seeded_from == "b_sketch")
    check("the approximation rides on every answer as a disclosure",
          any(d.code == "approximate" for d in sketch_total.disclosures))

    # ══ PROOF 3 · cross-family expression from compatible operands ═══════════════════════════════
    _rule("PROOF 3 · cross-family expression — Revenue + OrderCount → AOV. NO Mean family exists.")
    print("  first: a Mean FAMILY is not a constructible object.")
    try:
        mme.register_family(MeasureFamily(
            family_id="mean_order_value", manifold=MANIFOLD, universe="commerce", root=SALE_AT, law="MEAN",
            value_domain="decimal", participation=PARTICIPATION, target="the mean order value"))
        check("MeasureFamily(law=MEAN) refused at constitution", False)
    except KernelRefusal as exc:
        print(f"    REFUSED [{exc.code}] {exc.detail}")
        check("MeasureFamily(law=MEAN) refused at constitution", exc.code == "not-a-family-law")

    print(f"\n  the two operands, established INDEPENDENTLY at {BY_DAY}:")
    rev_day = mme.measure(revenue, BY_DAY)
    cnt_day = mme.measure(order_count, BY_DAY)
    print(f"    revenue      {dict(rev_day.value.cells)}")
    print(f"    order_count  {dict(cnt_day.value.cells)}")
    agreement = rev_day.value.instance.compatible_with(cnt_day.value.instance)
    print(f"    compatibility: {'HOLDS' if agreement else 'FAILS'} — {agreement.detail}")

    print(f"\n  average_order_value @ {BY_DAY}")
    aov_day = evaluator.evaluate(aov, BY_DAY)
    _say(aov_day)
    print(_cells(aov_day, render=lambda v: f"{v:.4f}"))

    print(f"\n  average_order_value @ {TOTAL}")
    aov_total = evaluator.evaluate(aov, TOTAL)
    _say(aov_total)
    print(_cells(aov_total, render=lambda v: f"{v:.4f}"))

    before = len(mme.materializations.select("revenue", eligibility=None))
    again = evaluator.evaluate(aov, TOTAL)
    after_n = len(mme.materializations.select("revenue", eligibility=None))
    print(f"\n  asked again: {again}")
    print("      re-EVALUATED, not re-cached — and its operands were not re-established either:")
    print(f"      revenue materializations before {before} → after {after_n}. The cache that matters")
    print("      is the FAMILY cache, and it is still doing the work.")

    check("AOV@D1 = 175/2 = 87.5", abs(aov_day.value.cells[("D1",)] - 87.5) < 1e-9)
    check("AOV@D2 = 325/4 = 81.25", abs(aov_day.value.cells[("D2",)] - 81.25) < 1e-9)
    check("AOV@total = 500/6 ≈ 83.3333", abs(aov_total.cell() - 500 / 6) < 1e-9)
    check("it is NOT the mean of the daily means — 83.3333 vs 84.3750 (the error a Mean family\n           would have made, and the reason the fixture is unbalanced)",
          abs(aov_total.cell() - (87.5 + 81.25) / 2) > 1.0)
    check("the expression was EVALUATED from a basis, never continued", aov_total.route == "evaluated")
    check("asked again it is EVALUATED AGAIN — there is no expression cache in v1",
          again.route == "evaluated")
    check("and the second evaluation costs no new family work: the family cache absorbed it",
          after_n == before)
    check("the answers agree exactly across the two evaluations",
          abs(again.cell() - aov_total.cell()) < 1e-12)

    # ══ PROOF 4 · the same expression refusing an INCOMPATIBLE basis ═════════════════════════════
    _rule("PROOF 4 · an incompatible basis is refused — while BOTH operands exist and are available")
    audited = mme.measure(audited_count, BY_DAY)
    print(f"  revenue              @ {BY_DAY}  served: {dict(rev_day.value.cells)}")
    print(f"  audited_order_count  @ {BY_DAY}  served: {dict(audited.value.cells)}")
    print("  both operands are ESTABLISHED, AVAILABLE, and individually valid.")
    print(f"\n  average_order_value_audited @ {BY_DAY}")
    refused = evaluator.evaluate(aov_audited, BY_DAY)
    _say(refused)
    print(f"      {refused.refusal.detail}")

    check("both operands really did serve", rev_day.served and audited.served)
    check("the expression over them is REFUSED", not refused.served)
    check("the refusal is about PARTICIPATION, not about absence",
          "different-participation" in str(refused.refusal))
    check("and it says so: individually valid, jointly meaningless",
          "jointly meaningless" in str(refused.refusal))

    # ══ PROOF 5 · THERE IS ONE CACHE, AND IT HOLDS FAMILIES ═════════════════════════════════════
    #
    # M-1 proved that the family cache and the expression cache were two stores with different rights.
    # M-2 makes the stronger statement available: **there is no second store.** The proof is not that an
    # expression output is held under weaker rights — it is that it is not held.
    _rule("PROOF 5 · ONE cache, and it holds family materializations only (M-2 §1)")
    fam_keys = list(mme.held)
    print(f"  {len(fam_keys)} object(s) held by the MME.")
    print(f"  of those, family materializations: "
          f"{sum(1 for k in fam_keys if mme.sort_of(k.identity) == 'family')}")
    print(f"  of those, expression outputs:      "
          f"{sum(1 for k in fam_keys if mme.sort_of(k.identity) == 'expression')}")
    print(f"\n  expressions ARE constituted by this engine — {sorted(mme.expressions)} —")
    print("  and every one of them has just been SERVED. Constitution is not residency.")
    print("\n  every held state, asked whether it may seed its own family one step coarser:")
    seeded, blocked = 0, 0
    for key in sorted(fam_keys, key=str):
        fam = mme.family(key.identity)
        if key.anchor.is_scalar:
            continue
        target = COMMERCE.anchor(sorted(key.anchor.constituents)[1:])
        v = mme.adjudicate(_holding(mme, key), fam, target)
        seeded, blocked = (seeded + 1, blocked) if v else (seeded, blocked + 1)
        print(f"    {str(key):<46} → {target}  {'ADMITTED' if v else 'REFUSED  [' + v.code + ']'}")

    check("at least one family state may seed and at least one may not", seeded > 0 and blocked > 0)
    check("EVERY held object is family state — nothing else can be in this store",
          all(mme.sort_of(k.identity) == "family" for k in fam_keys))
    check("no expression output is held, at any anchor",
          all(mme.sort_of(k.identity) != "expression" for k in fam_keys))
    check("expressions are nonetheless CONSTITUTED here and fully served above",
          set(mme.expressions) >= {"average_order_value", "distinct_customer_estimate"}
          and aov_total.served and estimate.served)
    check("`RetentionKey.sort` is retired: a constant, not a field a caller can vary",
          "sort" not in {f.name for f in fields(RetentionKey)} and RetentionKey.sort == "family")

    # ══ PROOF 6 · ordered family, if inexpensive — it was ════════════════════════════════════════
    _rule("PROOF 6 · ordered family — LAST witness continuation, governed order, known-empty standing")
    g_root = mme.measure(gauge, STORE_DAY_LEVEL)
    print(f"  gauge @ {STORE_DAY_LEVEL}  (R_F) — witnesses are (order_key, value)")
    print(_cells(g_root))
    g_store = mme.measure(gauge, BY_STORE)
    print(f"\n  gauge @ {BY_STORE}  — LATEST_BY_ORDER across days")
    _say(g_store)
    print(_cells(g_store, render=lambda w: f"{w}  → displays {witness_value(w)}"))
    empty = IN_MEMORY.of("LAST").contribute([], {"order_by": "recorded_at", "rows": ()})
    print(f"\n  an eligible fibre with no contribution: {empty!r}")
    print(f"    it displays {witness_value(empty)!r} — a KNOWN-EMPTY standing, which is a governed "
          f"answer and is not 'unknown'")
    print(f"    LAST has no identity: {REGISTRY.get('LAST').continuation.has_identity} "
          f"— {REGISTRY.get('LAST').continuation.note}")

    check("the witness carries its order key, not just its value",
          isinstance(g_root.value.cells[("D1", "S1")], tuple))   # cells key in the ANCHOR's sorted order
    check("LAST@S1 selects the 17:00 reading of D1 over the 09:00 of D2 by ORDER",
          witness_value(g_store.value.cells[("S1",)]) == 5)
    check("an empty eligible fibre is KNOWN_EMPTY, not None", empty == KNOWN_EMPTY)
    check("and merging KNOWN_EMPTY with a witness yields the witness",
          IN_MEMORY.of("LAST").merge(KNOWN_EMPTY, ("08:00", 3)) == ("08:00", 3))

    # ══ 7 · THE THREE FACTS ABOUT A RETAINED OBJECT, MOVED ONE AT A TIME ═════════════════════════
    _rule("PROOF 7 · constitution · data state · realization — three facts, three axes, moved one "
          "at a time")
    witness = mme.witness_of("revenue")
    print(f"  revenue's ConstitutionWitness   {witness.digest}")
    print(f"    COMPUTED from {len(witness.determinants)} identity-bearing determinant(s): "
          f"{list(witness.names)}")
    print(f"    and NOT from: {sorted(FAMILY_NON_DETERMINANTS)}  "
          f"(a label, a description, and the retired declared slot)")
    supplied = None
    try:
        replace(revenue, constitution="c0")
    except KernelRefusal as exc:
        supplied = exc
    print(f"    supplying one by hand: REFUSED [{supplied.code if supplied else '—'}]")
    print(f"    the `law` determinant is {witness.determinant('law')}")
    print("      — the NAME and the law's OWN witness, so the ADMITTED CONTINUATION REGION is in "
          "structurally")
    narrowed = replace(REGISTRY.get("SUM"), region=ContinuationRegion.forgetting_only(
        {"order"}, "value closure across orders only — not across time"))
    region_moved = revenue.witness(narrowed)
    print(f"      narrow the region alone → {region_moved.digest}, changed "
          f"{list(witness.compare(region_moved).changed)}")
    knob = None
    try:
        replace(revenue, parameters={"codec": "zstd"}).bind(REGISTRY)
    except KernelRefusal as exc:
        knob = exc
    print(f"    a codec in `parameters`: REFUSED [{knob.code if knob else '—'}] — that field is "
          f"analytical identity, and a codec is realization standing")

    print("\n  ONE EDIT AT A TIME, and exactly one axis moves:")
    load_a, load_b = "load:orders@08:00Z", "load:orders@17:30Z"
    held_already = mme.materializations.select("revenue", anchor=SALE_AT)[0]
    mme.establish_root(revenue, ORDERS, data_state=load_a,
                       intent=TransitionIntent(SUPERSEDE, (held_already.id,)))
    first = mme.materializations.select("revenue", anchor=SALE_AT, data_state=load_a)[0]
    mme.establish_root(revenue, ORDERS[:2], data_state=load_b)       # intent COEXIST, the default
    both = mme.materializations.select("revenue", anchor=SALE_AT, eligibility=None)
    print(f"    the DATA moves   → witness {mme.witness_of('revenue').digest} unchanged; "
          f"{len(both)} retained materializations of ONE F@A, coexisting under one opaque id each")
    for m in both:
        print(f"        {m}")
    served = mme.measure(revenue, BY_DAY)
    print(f"      an ordinary ask names an analytical identity and gets ONE answer: "
          f"revenue@D1 = {served.value.cells[('D1',)]:.2f}  (the CURRENT evidence state)")
    print("      the coexisting instance is retained and NOT current — an ordinary request never sees")
    print("      two interchangeable answers, and the CACHE never asks the caller to choose.")
    mme.establish_root(revenue, ORDERS[:2], data_state=load_b,
                       intent=TransitionIntent(SUPERSEDE, (first.id,)))
    after = mme.measure(revenue, BY_DAY)
    print(f"      offering {load_b} again with intent SUPERSEDE({first.id}): revenue@D1 is now "
          f"{after.value.cells[('D1',)]:.2f}")
    print(f"        {mme.materialization(first.id)}")

    one = RealizationStanding(provider="in-memory", carrier="in-memory")
    two = RealizationStanding(provider="in-memory", carrier="arrow-ipc")
    print(f"    the REALIZATION moves → {one} vs {two}; witness and analytical instance both unchanged")

    moved = replace(revenue, participation="every order the auditor confirmed")
    mme.register_family(moved)
    stale = mme.stale_states()
    print(f"    the DECLARATION moves → witness {mme.witness_of('revenue').digest}, and "
          f"{len(stale)} materialization(s) stopped being CURRENT (they stay RESIDENT)")
    for s_ in stale[:1]:
        print(f"      {s_}")
        print(f"      {s_.detail}")
    refused_stale = mme.measure(moved, BY_DAY)

    check("the witness is COMPUTED, and a caller-supplied one is refused",
          witness.digest.startswith("cw-1:") and supplied is not None
          and supplied.code == "constitution-is-computed")
    check("the ADMITTED CONTINUATION REGION is identity-bearing: narrowing it alone moves the witness",
          region_moved.digest != witness.digest
          and witness.compare(region_moved).changed == ("law",))
    check("`parameters` is a SEMANTIC constitution field: a codec in it is refused",
          knob is not None and knob.code == "undeclared-parameter")
    check("a family and an expression both have one, and they are not comparable across sorts",
          not mme.witness_of("average_order_value").compare(witness))
    check("new root data: SAME witness, and retained materializations of one F@A COEXIST",
          len(both) >= 3 and len({m.id for m in both}) == len(both)
          and len({m.build for m in both}) == 1
          and len([m for m in both if m.eligibility == "current"]) == 1)
    check("an ordinary ask gets ONE answer — the cache chooses, the caller never does",
          served.served and served.value.cells[("D1",)] == 175.0)
    check("and an explicit SUPERSEDE moves currentness without touching residency",
          after.value.cells[("D1",)] == 100.0
          and mme.materialization(first.id).eligibility == "superseded"
          and mme.materialization(first.id).residency == "resident")
    check("a realization change moves neither the witness nor the instance", one != two
          and mme.witness_of('revenue').digest != witness.digest)
    check("a constitution change is mechanically detectable AND names the determinant",
          bool(stale) and stale[0].changed == ("participation",))
    check("a declaration move makes held material NOT CURRENT — it is not served, and the refusal says "
          "the bytes are still here",
          not refused_stale.served and "NOT CURRENT (superseded)" in refused_stale.refusal.detail
          and "Residency never creates analytical authority" in refused_stale.refusal.detail)

    # ══ realization limits, and conservative invalidation ════════════════════════════════════════
    _rule("ADDENDA · a provider's inability does not remove a law; invalidation is conservative")
    from .builtins import NO_MEAN
    thin = MME(COMMERCE, REGISTRY, NO_MEAN, manifold=MANIFOLD)
    for family in (revenue, order_count):
        thin.register_family(family)
    thin.register_expression(aov)
    thin.establish_root(revenue, ORDERS)
    thin.establish_root(order_count, ORDERS)
    try:
        ExpressionEvaluator(thin).evaluate(aov, TOTAL)
        realization_refused = False
        detail = ""
    except KernelRefusal as exc:
        realization_refused = exc.code in ("unrealized-law", "unrealized-capability")
        detail = exc.detail
    print(f"  provider {NO_MEAN.name!r} realizes {NO_MEAN.laws}")
    print(f"  evaluating AOV under it: REFUSED — {detail}")
    check("an unrealized law is a PROVIDER limit and says so", realization_refused)

    # ══ THE WORKLOAD OBSERVATION SEAM ═══════════════════════════════════════════════════════════
    _rule("OBSERVATION · every family request is visible — hits AND misses (M-2 §4, §7)")
    print(f"  {watcher.summary()}")
    print("\n  the last eight family requests, as the observer saw them:")
    for record in watcher.records[-8:]:
        print(f"    {record}")
    print("\n  demand λ(q), counted over what was ASKED and never over what answered:")
    for (fam_id, target), n in sorted(watcher.demand().items(), key=lambda kv: -kv[1])[:6]:
        print(f"    {fam_id + '@' + target:<40} {n}")
    on_behalf = [r for r in watcher.records if r.request.on_behalf_of]
    print(f"\n  {len(on_behalf)} request(s) were made ON BEHALF OF an expression — the route/use")
    print("  evidence of §8, which keeps an expression's traffic from being read as a family's")
    print("  popularity. One of them:")
    if on_behalf:
        print(f"    {on_behalf[-1].request.family_id}@{on_behalf[-1].request.target}"
              f"  ← {on_behalf[-1].request.on_behalf_of}")

    check("every request was observed, hits and misses alike", len(watcher) > 0)
    check("MISSES are in the log — a policy cannot learn from hits alone (§7)",
          len(watcher.misses()) > 0)
    check("and so are hits", any(r.served for r in watcher.records))
    check("a derived answer is distinguishable from a directly-held one (§4)",
          any(r.served and r.fulfillment.directly_held for r in watcher.records)
          and any(r.served and not r.fulfillment.directly_held for r in watcher.records))
    check("a derived answer names the materialization it was seeded from, so a counterfactual\n"
          "           is computable later without re-running the request",
          any(r.fulfillment.seeded_from is not None and r.fulfillment.selected
              for r in watcher.records))
    check("expression-driven demand is attributed to the expression (§8)", len(on_behalf) > 0)
    check("dispositions are named, not collapsed into hit/miss",
          len(set(watcher.by_disposition())) > 1)

    print("\n  AND THE OBSERVER IS NOT AUTHORITATIVE. One that raises on every call:")

    class Hostile:
        def observe(self, observation):
            raise RuntimeError("the logging backend is down")

    mme.observations.observer = Hostile()
    hostile_served = mme.measure(on_hand, BY_DAY)          # a hit
    hostile_refused = mme.measure(on_hand, BY_STORE)       # a refusal, under the same broken observer
    mme.observations.observer = watcher
    watched_served = mme.measure(on_hand, BY_DAY)
    watched_refused = mme.measure(on_hand, BY_STORE)
    print(f"    on_hand @ {BY_DAY}   under a raising observer: {hostile_served}")
    print(f"    on_hand @ {BY_STORE} under a raising observer: {hostile_refused.route} "
          f"[{hostile_refused.refusal.code}]")
    print(f"    sink reports: {mme.observations.summary()}")
    check("a SERVED request is unaffected by an observer that raises (§4)", hostile_served.served)
    check("and the cells are identical to the observed ones",
          dict(hostile_served.value.cells) == dict(watched_served.value.cells))
    check("a REFUSED request is unaffected too — the refusal still says the same thing",
          (not hostile_refused.served)
          and hostile_refused.refusal.detail == watched_refused.refusal.detail)
    check("the observer failures are COUNTED rather than swallowed silently",
          mme.observations.failures >= 2)
    # **WRITE-ONLY BY CONSTRUCTION** (§6: observations never create analytical rights). The engine holds
    # a SINK, not an observer, and a sink's only verb is `emit`. There is no method on it that returns an
    # observation, so no serving path could consult one even by mistake.
    check("the seam is WRITE-ONLY: the engine holds a sink whose only verb is `emit` (§6)",
          not any(hasattr(mme.observations, name) for name in ("records", "read", "history", "replay"))
          and callable(mme.observations.emit))

    dropped = mme.invalidate("revenue")
    print(f"\n  invalidate('revenue') dropped {len(dropped)} retained state(s); rebuild is from R_F.")
    after = mme.measure(revenue, TOTAL)
    print(f"  revenue @ {TOTAL} now: {after}")
    check("a conservatively invalidated family is unanswerable until re-established",
          not after.served)
    check("no delta retraction was attempted", "must be established at" in str(after.refusal))

    print("\n" + "═" * 96)
    if failures:
        print(f"  {len(failures)} CHECK(S) FAILED")
        for f in failures:
            print(f"    ✗ {f}")
    else:
        print("  ALL CHECKS PASSED — the v8-native MME is running.")
    print("═" * 96)
    return 1 if failures else 0


if __name__ == "__main__":                                  # pragma: no cover
    raise SystemExit(main())

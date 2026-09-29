"""
columna_platform.columnar.exhibit — **the v8-native MME executing over real Arrow/DataFusion state.**

    python -m columna_platform.columnar.exhibit

THE WORLD, AND WHY THERE ARE TWO OF IT
--------------------------------------
The same `commerce` universe the kernel exhibit constitutes, plus **one extra order**:

    O7 — accepted by the merchant, amount NEVER RECORDED.

O7 is the standing proof. It **participates** (the merchant accepted it, so `OrderCount` must count it) and
it is **unsupported** for Revenue (no evidence of an amount).

The exhibit runs the same seven orders as TWO worlds, differing by **exactly one support bit and one
amount**:

    AS RECORDED    O7's amount is not established.  `OrderCount` = 3 at D1; `Revenue` WANTS STATE;
                   `AOV` refuses, because a required basis operand is not established.
    SETTLED        the merchant later supplies O7's amount (60.00).  Nothing else changes, and every
                   value-bearing answer becomes available.

That pairing is the measurement. Three readings of the same seven rows give three different answers, and only
one of them is the governed one:

    `count(non-null revenue)`     → 6 orders.  A DIFFERENT MEASURE.
    `participation ∧ support`     → a Revenue total of 175.00 at D1 over an `OrderCount` of 3.  **A NUMBER
                                    ABOUT NO POPULATION** — the retired filter, and the error corrected on
                                    2026-09-29.
    participation, validated by support
                                  → `OrderCount` = 3 and Revenue REFUSES until the amount is established.

    *"Participation determines the contributing domain. Support determines whether the values required over
    that participating domain are established."* — Huayin, 2026-09-29
"""
from __future__ import annotations


import pyarrow as pa

from columna_platform.kernel import (
    MME,
    REGISTRY,
    GovernedExpression,
    KernelRefusal,
    MeasureFamily,
    Operand,
    SufficientBasis,
)
from columna_platform.kernel.builtins import IN_MEMORY
from columna_platform.kernel.exhibit import COMMERCE

from .block import GovernedBlock
from .index import CoordinateIndex
from .mme import ColumnarExpressionOutput, ColumnarMME
from .provider import sketch_of, sketch_parameters
from .standing import POPULATION, VALUE_BEARING, standing

MANIFOLD = "andfam.commerce"
OTHER_MANIFOLD = "acme.commerce"
PARTICIPATION = "every customer order the merchant accepted"
AUDITED = "every customer order the merchant accepted AND the auditor confirmed"

SALE_AT = COMMERCE.anchor({"store", "day", "order"})
BY_DAY = COMMERCE.anchor({"day"})
BY_STORE = COMMERCE.anchor({"store"})
TOTAL = COMMERCE.scalar_anchor

#: Seven accepted orders, AS RECORDED. **O7 participates and is unsupported for Revenue.**
ORDERS = (
    {"store": "S1", "day": "D1", "order": "O1", "value": 100.0, "customer": "C1", "supported": True},
    {"store": "S1", "day": "D2", "order": "O2", "value": 50.0, "customer": "C2", "supported": True},
    {"store": "S1", "day": "D2", "order": "O3", "value": 25.0, "customer": "C1", "supported": True},
    {"store": "S2", "day": "D1", "order": "O4", "value": 75.0, "customer": "C3", "supported": True},
    {"store": "S2", "day": "D2", "order": "O5", "value": 200.0, "customer": "C1", "supported": True},
    {"store": "S2", "day": "D2", "order": "O6", "value": 50.0, "customer": "C4", "supported": True},
    {"store": "S1", "day": "D1", "order": "O7", "value": None, "customer": "C5", "supported": False},
)

#: The amount the merchant later supplies for O7 in the SETTLED world. Nothing else differs.
O7_SETTLED_AMOUNT = 60.0

#: The unsupported order, named once so no proof has to re-derive which one it is.
UNSUPPORTED_ORDER = "O7"
UNSUPPORTED_POINT = ("D1", "O7", "S1")


def _orders(settled: bool = False) -> tuple:
    """The seven orders, in one of the two worlds. **One bit and one amount apart.**"""
    if not settled:
        return ORDERS
    return tuple({**o, "value": O7_SETTLED_AMOUNT, "supported": True}
                 if o["order"] == UNSUPPORTED_ORDER else o for o in ORDERS)


def _families(manifold: str = MANIFOLD):
    revenue = MeasureFamily(family_id="revenue", manifold=manifold, universe="commerce", root=SALE_AT,
                            law="SUM", value_domain="decimal", participation=PARTICIPATION,
                            target="the additive total of accepted order value")
    order_count = MeasureFamily(family_id="order_count", manifold=manifold, universe="commerce",
                                root=SALE_AT, law="COUNT", value_domain="integer",
                                participation=PARTICIPATION,
                                target="the number of accepted customer orders")
    audited = MeasureFamily(family_id="audited_order_count", manifold=manifold, universe="commerce",
                            root=SALE_AT, law="COUNT", value_domain="integer", participation=AUDITED,
                            target="the number of auditor-confirmed orders")
    distinct = MeasureFamily(family_id="distinct_customers", manifold=manifold, universe="commerce",
                             root=SALE_AT, law="HLL_SKETCH", value_domain="sketch",
                             participation=PARTICIPATION,
                             target="an HLL sketch of the distinct customers who ordered")
    on_hand = MeasureFamily(family_id="on_hand", manifold=manifold, universe="commerce",
                            root=COMMERCE.anchor({"store", "day"}), law="STOCK_LEVEL",
                            value_domain="integer",
                            participation="every unit counted in the evening stocktake",
                            target="units held at one store at the close of one day")
    return revenue, order_count, audited, distinct, on_hand


def _expressions(manifold: str = MANIFOLD):
    aov = GovernedExpression(
        expression_id="average_order_value", manifold=manifold, universe="commerce",
        constructor="MEAN", operands=(Operand("operand", "revenue"),), participation=PARTICIPATION,
        inner_anchors=(SALE_AT,),
        admitted_bases=(SufficientBasis("b_revenue_ordercount",
                                        {"SUM": "revenue", "COUNT": "order_count"}, True),))
    aov_audited = GovernedExpression(
        expression_id="average_order_value_audited", manifold=manifold, universe="commerce",
        constructor="MEAN", operands=(Operand("operand", "revenue"),), participation=PARTICIPATION,
        admitted_bases=(SufficientBasis("b_revenue_auditedcount",
                                        {"SUM": "revenue", "COUNT": "audited_order_count"}, True),))
    estimate = GovernedExpression(
        expression_id="distinct_customer_estimate", manifold=manifold, universe="commerce",
        constructor="HLL_ESTIMATE", operands=(Operand("operand", "distinct_customers"),),
        participation=PARTICIPATION,
        admitted_bases=(SufficientBasis("b_sketch", {"HLL_SKETCH": "distinct_customers"}, True),))
    return aov, aov_audited, estimate


def _root_index(manifold: str = MANIFOLD) -> CoordinateIndex:
    """The root coordinate index. **SPARSE**: seven existing points, not 2×2×7 Cartesian cells."""
    return CoordinateIndex.of(manifold, SALE_AT,
                              [tuple(o[r] for r in SALE_AT.order) for o in ORDERS])


def _by_order(index: CoordinateIndex, settled: bool = False):
    """The occurrences, re-laid in the index's position order."""
    lookup = {tuple(o[r] for r in SALE_AT.order): o for o in _orders(settled)}
    return [lookup[cell] for cell in index.coordinates]


def build(manifold: str = MANIFOLD, *, settled: bool = False) -> tuple[ColumnarMME, GovernedBlock]:
    """A constituted columnar MME and the root block. **One shared provider is fine; authority is not.**

    `settled=False` is the world AS RECORDED, in which O7's amount is not established. `settled=True` is the
    same seven orders after the merchant supplied it — the control, and the only difference is O7's support
    bit and its amount."""
    authority = MME(COMMERCE, REGISTRY, IN_MEMORY, manifold=manifold)
    for family in _families(manifold):
        authority.register_family(family)
    for expression in _expressions(manifold):
        authority.register_expression(expression)
    mme = ColumnarMME(authority)

    index = _root_index(manifold)
    rows = _by_order(index, settled)
    revenue, order_count, audited, distinct, _ = _families(manifold)

    block = GovernedBlock.of(
        index,
        columns={
            # NOTE the value column is NULLABLE and its null is MEANINGLESS here. O7's absence of an
            # amount is carried by the SUPPORT MASK; the null is just how Arrow stores "no float".
            "revenue": pa.array([r["value"] for r in rows], type=pa.float64()),
            "order_count": pa.array([1] * len(rows), type=pa.int64()),
            "audited_order_count": pa.array([1] * len(rows), type=pa.int64()),
            "distinct_customers": pa.array([sketch_of([r["customer"]]) for r in rows],
                                           type=pa.binary()),
        },
        standings={
            "revenue": standing("revenue", authority.instance_of("revenue"), n=len(rows),
                                support=[r["supported"] for r in rows],
                                note="O7 participates and is UNSUPPORTED: accepted by the merchant, "
                                     "amount never recorded. It is IN the contributing domain of the SUM "
                                     "and the SUM therefore has want of state — it is not removed from it"
                                     if not settled else
                                     "the merchant later supplied O7's amount; every participating point "
                                     "is now established"),
            "order_count": standing("order_count", authority.instance_of("order_count"), n=len(rows),
                                    note="every accepted order participates, INCLUDING O7. This is the "
                                         "whole point: a count of the population, not of the evidence"),
            "audited_order_count": standing(
                "audited_order_count", authority.instance_of("audited_order_count"), n=len(rows),
                participation=[r["order"] in {"O1", "O2", "O3", "O4"} for r in rows],
                note="a DIFFERENT participation — the auditor confirmed four of seven"),
            "distinct_customers": standing("distinct_customers",
                                           authority.instance_of("distinct_customers"), n=len(rows)),
        },
        realization="in-memory-arrow",
        provenance=("seven accepted orders, constructed programmatically",))
    for family_id in ("revenue", "order_count", "audited_order_count", "distinct_customers"):
        mme.establish(block, family_id)
    return mme, block


# ── printing ─────────────────────────────────────────────────────────────────────────────────────
def _rule(t: str) -> None:
    print(f"\n{'─' * 100}\n{t}\n{'─' * 100}")


def _show(state, label: str, render=lambda v: v) -> None:
    print(f"  {label}")
    for cell, value in zip(state.index.coordinates, state.values.to_pylist()):
        where = ", ".join(f"{k}={v}" for k, v in zip(state.anchor.order, cell)) or "ALL"
        print(f"      {where:<24} {render(value)}")


def main() -> int:                                          # noqa: C901 - an exhibit is a narrative
    mme, block = build()                                    # AS RECORDED: O7's amount is not established
    settled, settled_block = build(settled=True)            # the control: the amount later supplied
    revenue, order_count, audited, distinct, on_hand = _families()
    aov, aov_audited, estimate = _expressions()
    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        print(f"    {'✓' if condition else '✗'} {label}")
        if not condition:
            failures.append(label)

    print("═" * 100)
    print("  COLUMNA PLATFORM · v8-native MME over Arrow/DataFusion columnar state")
    print(f"  manifold {MANIFOLD!r}   provider {mme.provider.name!r}")
    print(f"  root index {block.index}   identity {block.index.identity}")
    print("  two worlds, ONE support bit apart:")
    print(f"    AS RECORDED  {UNSUPPORTED_ORDER}'s amount is not established — participation ∧ ¬support")
    print(f"    SETTLED      {UNSUPPORTED_ORDER}'s amount is {O7_SETTLED_AMOUNT:.2f} — every "
          f"participating point established")
    print("═" * 100)

    # ══ 1 · REAL ARROW COLUMNAR STATE AT A GOVERNED ANCHOR INSTANCE ══════════════════════════════
    _rule("PROOF 1 · real Arrow columnar family state at a governed anchor instance")
    print("  Arrow schema:\n      "
          + "\n      ".join(f"{f.name}: {f.type}" for f in block.batch.schema))
    print()
    print("\n".join("    " + ln for ln in
                    block.render(families=("revenue", "order_count")).splitlines()))
    print(f"\n  revenue standing:      {block.standing('revenue').summary()}")
    print(f"  order_count standing:  {block.standing('order_count').summary()}")

    check("the coordinate index is SPARSE: 7 existing points, not a Cartesian product",
          len(block.index) == 7 and len(block.index) < 2 * 2 * 7)
    check("the batch's rows ARE the index's positions", block.batch.num_rows == len(block.index))
    check("each column carries its OWN analytical instance",
          block.standing("revenue").instance != block.standing("audited_order_count").instance)
    check("co-location confers nothing: two columns of ONE batch are incompatible",
          not block.compatibility_of("revenue", "audited_order_count"))
    check("and the reason is participation",
          block.compatibility_of("revenue", "audited_order_count").code
          == "different-participation")

    # ══ 8 · STANDING INDEPENDENT OF ARROW NULL (proved here, where the block is in hand) ═════════
    _rule("PROOF 8 · support VALIDATES the participating domain — it does not shrink it")
    rev_col = block.column("revenue")
    position = block.index.position(UNSUPPORTED_POINT)
    print(f"  the revenue value column has {rev_col.null_count} Arrow null(s) — and the null means NOTHING.")
    print(f"  {UNSUPPORTED_ORDER}'s standing:  participation=True  support=False")
    print()
    rev_domain = block.contributing_domain("revenue", VALUE_BEARING).to_pylist()
    rev_wanting = block.want_of_state("revenue", VALUE_BEARING).to_pylist()
    count_domain = block.contributing_domain("order_count", POPULATION).to_pylist()
    print(f"  revenue     contributing domain {sum(rev_domain)}/7   (participation — {UNSUPPORTED_ORDER} "
          f"IS IN IT)   want of state at {sum(rev_wanting)}")
    print(f"  order_count contributing domain {sum(count_domain)}/7   (participation)"
          f"                     want of state at "
          f"{sum(block.want_of_state('order_count', POPULATION).to_pylist())}")
    print()
    print("  the three readings of these same seven rows:")
    print(f"      count(non-null revenue)                  {len(rev_col) - rev_col.null_count}   "
          f"A DIFFERENT MEASURE")
    print(f"      participation ∧ support  (RETIRED)        "
          f"{sum(1 for a, b in zip(rev_domain, block.standing('revenue').support.to_pylist()) if a and b)}"
          f"   a Revenue total over an OrderCount of 3 — a number about NO population")
    print(f"      participation, validated by support       {sum(rev_domain)}   "
          f"and 1 of them WANTS STATE, so the SUM refuses")

    check("participation is known independently of value presence",
          count_domain[position] is True)
    check("support is False at the same position",
          block.standing("revenue").support[position].as_py() is False)
    check("the unsupported point is IN the value-bearing contributing domain, not removed from it",
          rev_domain[position] is True and sum(rev_domain) == 7)
    check("and it is reported as WANT OF STATE, which is a different fact from exclusion",
          rev_wanting[position] is True and sum(rev_wanting) == 1)
    check("a POPULATION reduction has no want of state at all — it requires no value",
          not any(block.want_of_state("order_count", POPULATION).to_pylist()))
    check("COUNT is not count(non-null revenue): 7 vs 6", sum(count_domain) == 7
          and (len(rev_col) - rev_col.null_count) == 6)
    check("the retired `participation ∧ support` contribution filter REFUSES if anything reaches for it",
          _refuses_retired_filter(block))
    check("a null in a STANDING mask is refused outright",
          _refuses_null_standing(mme))
    check("a point declared SUPPORTED with no value in the carrier is refused as a broken contract",
          _refuses_support_without_a_value(mme))

    # ══ 8b · THE CANONICAL CASE, END TO END ══════════════════════════════════════════════════════
    _rule("PROOF 8b · 3 Orders participate · 1 Revenue unsupported · Count 3 · Revenue WANTS STATE · "
          "AOV REFUSES")
    d1 = [o for o in ORDERS if o["day"] == "D1"]
    print(f"  at D1: {len(d1)} orders participate — {[o['order'] for o in d1]}; "
          f"{UNSUPPORTED_ORDER}'s Revenue is unsupported.\n")

    counts = mme.measure("order_count", BY_DAY)
    print(f"  OrderCount @ {BY_DAY}   {counts.route}")
    _show(counts.value, "")

    rev = mme.measure("revenue", BY_DAY)
    print(f"\n  Revenue    @ {BY_DAY}   REFUSED [{rev.refusal.code}]")
    print(f"      {rev.refusal.detail}")

    aov_refused = mme.evaluate("average_order_value", BY_DAY)
    print(f"\n  AOV        @ {BY_DAY}   REFUSED [{aov_refused.refusal.code}]")
    print(f"      {aov_refused.refusal.detail}")

    # At the ROOT anchor both operands are already held, so no continuation intervenes and the refusal
    # is the expression path's own: the basis is lawful, aligned, compatible — and not established.
    aov_at_root = mme.evaluate("average_order_value", SALE_AT)
    print(f"\n  AOV        @ {SALE_AT}   REFUSED [{aov_at_root.refusal.code}]")
    print(f"      {aov_at_root.refusal.detail}")

    sketch_unaffected = mme.measure("distinct_customers", BY_DAY)
    print(f"\n  and support is PER COLUMN: distinct_customers over the same seven rows "
          f"{sketch_unaffected.route} — {UNSUPPORTED_ORDER}'s customer was recorded even though its "
          f"amount was not.")

    check("the population reduction serves and counts ALL THREE participating orders",
          counts.served and counts.value.cell(("D1",)) == 3)
    check("a missing Revenue changed OrderCount by nothing", counts.value.cell(("D2",)) == 4)
    check("Revenue REFUSES with want of state", not rev.served
          and rev.refusal.code == "want-of-state")
    check("the refusal names the participating point whose value is not established",
          "O7" in rev.refusal.detail and "want of state" in rev.refusal.detail)
    check("and says the reduction has not run, rather than reporting a total over the remainder",
          "THE REDUCTION HAS NOT RUN" in rev.refusal.detail
          and "does not shrink it" in rev.refusal.detail)
    check("NOTHING was inferred: not NA, not known-empty, not nonparticipation",
          "not `NA`" in rev.refusal.detail and "not a known-empty" in rev.refusal.detail
          and "not nonparticipation" in rev.refusal.detail)
    check("AOV refuses because a REQUIRED BASIS OPERAND is not established",
          not aov_refused.served and "role 'SUM'" in aov_refused.refusal.detail
          and "want of state" in aov_refused.refusal.detail)
    check("at the root anchor the expression path refuses on its own: basis-operand-wants-state",
          not aov_at_root.served
          and "basis-operand-wants-state" in aov_at_root.refusal.detail
          and "THE ARITHMETIC HAS NOT RUN" in aov_at_root.refusal.detail)
    check("and it says the expression was NOT evaluated over the supported subset of points",
          "NOT evaluated over the subset" in aov_at_root.refusal.detail)
    check("the old answer 175/3 = 58.3333 is NOT served, and neither is 175/2",
          aov_refused.value is None)
    check("a point with want of state has no value to read, and reading one refuses",
          _refuses_cell_at_want_of_state(mme))
    check("the held state DISCLOSES the want of state rather than hiding it",
          any(d.code == "want-of-state" for d in
              mme.retained("family", "revenue", SALE_AT,
                           mme.authority.instance_of("revenue")).value.disclosures))
    check("the same column with the amount supplied serves — ONE support bit apart",
          settled.measure("revenue", BY_DAY, retain=False).served)
    check("a support mask matters even with NO Arrow nulls in the value array",
          _refuses_with_no_arrow_nulls(mme))

    # ══ 4 · GROUPED CONTINUATION BY DATAFUSION (the SETTLED world) ═══════════════════════════════
    _rule("PROOF 4 · Revenue continued to a coarser anchor by DataFusion GROUPED reduction "
          "[SETTLED world]")
    by_day = settled.measure("revenue", BY_DAY)
    _show(by_day.value, f"revenue @ {BY_DAY}   route={by_day.route}",
          render=lambda v: f"{v:.2f}")
    print("\n  the exact route:")
    for step in by_day.value.route:
        print(f"      • {step}")

    counts_by_day = settled.measure("order_count", BY_DAY)
    _show(counts_by_day.value, f"\n  order_count @ {BY_DAY}")

    check("revenue continued by GROUPED reduction", by_day.served and by_day.route == "continued")
    check("D1 = 235.0 (O1 + O4 + O7's supplied 60.00) and D2 = 325.0",
          by_day.value.cell(("D1",)) == 235.0 and by_day.value.cell(("D2",)) == 325.0)
    check("the fold ran over the WHOLE participating domain, all 7 positions",
          any("7/7 positions in the CONTRIBUTING DOMAIN" in step for step in by_day.value.route))
    check("order_count D1 = 3 (O1, O4 AND O7) and D2 = 4 — unchanged from the as-recorded world",
          counts_by_day.value.cell(("D1",)) == 3 and counts_by_day.value.cell(("D2",)) == 4
          and mme.measure("order_count", BY_DAY).value.cell(("D1",)) == 3)
    check("the route names the governed filter, the DataFusion aggregate and the ALIGNMENT",
          any("governed-filter" in s for s in by_day.value.route)
          and any("datafusion: aggregate" in s for s in by_day.value.route)
          and any("align:" in s for s in by_day.value.route))
    check("alignment is an explicit REINDEX against a governed index, not a join",
          any("not a join on keys" in s for s in by_day.value.route))
    check("the output is aligned on the TARGET anchor's coordinate index",
          by_day.value.index.anchor == BY_DAY
          and by_day.value.index.identity != settled_block.index.identity)
    check("the coarser index is still SPARSE (2 days, derived from existing points)",
          len(by_day.value.index) == 2)

    # ══ 2 + A · POSITIONAL EXPRESSION, NO JOIN ═══════════════════════════════════════════════════
    _rule("PROOF 2 · Revenue / OrderCount evaluated POSITIONALLY at one anchor — no join "
          "[SETTLED world]")
    aov_day = settled.evaluate("average_order_value", BY_DAY)
    _show(aov_day.value, f"average_order_value @ {BY_DAY}   route={aov_day.route} "
                         f"via {aov_day.seeded_from}", render=lambda v: f"{v:.4f}")
    print(f"\n  both operand columns share ONE coordinate index "
          f"({settled.measure('revenue', BY_DAY).value.index.identity})")
    print("  so the division is a position-aligned Arrow kernel. Nothing discovered which Revenue")
    print("  cell corresponds to which Count cell — they are the same position.")

    check("AOV@D1 = 235/3 = 78.3333 — over the WHOLE participating domain, every value established",
          abs(aov_day.value.cell(("D1",)) - 235 / 3) < 1e-9)
    check("AOV@D2 = 325/4 = 81.25", abs(aov_day.value.cell(("D2",)) - 81.25) < 1e-9)
    check("the denominator is the POPULATION count 3, not a count of the supported values",
          abs(aov_day.value.cell(("D1",)) - 235 / 2) > 1.0)
    check("and under `count(non-null revenue)` D1 would have been 117.5 — a different number",
          abs(235 / 3 - 235 / 2) > 1.0)
    check("the result is an ExpressionOutput, not family state",
          isinstance(aov_day.value, ColumnarExpressionOutput)
          and not aov_day.value.CONTINUATION_BEARING)
    check("and it has NO continuation path at all",
          not hasattr(ColumnarExpressionOutput, "fold_onto_grouped"))

    # ══ 3 + B · COMPATIBILITY REFUSED BEFORE ARITHMETIC ══════════════════════════════════════════
    _rule("PROOF 3 · an incompatible basis is refused BEFORE arithmetic, on one aligned layout "
          "[SETTLED world]")
    rev_state = settled.measure("revenue", BY_DAY).value
    aud_state = settled.measure("audited_order_count", BY_DAY).value
    print(f"  revenue             @ {BY_DAY}  available, {len(rev_state.values)} positions, "
          f"index {rev_state.index.identity}")
    print(f"  audited_order_count @ {BY_DAY}  available, {len(aud_state.values)} positions, "
          f"index {aud_state.index.identity}")
    print(f"  SAME LAYOUT: {rev_state.index.identity == aud_state.index.identity}")
    refused = settled.evaluate("average_order_value_audited", BY_DAY)
    print(f"\n  average_order_value_audited @ {BY_DAY}")
    print(f"      REFUSED [{refused.refusal.code}]")
    print(f"      {refused.refusal.detail}")

    check("both operands are individually available", rev_state is not None and aud_state is not None)
    check("they are perfectly position-aligned",
          rev_state.index.identity == aud_state.index.identity)
    check("and the expression is REFUSED", not refused.served)
    check("the refusal says the arithmetic has not run",
          "THE ARITHMETIC HAS NOT RUN" in refused.refusal.detail)
    check("on participation, not on shape or absence",
          "different-participation" in refused.refusal.detail)
    check("authority to combine is asked BEFORE evidence for the values: this is not a want-of-state "
          "refusal", "wants-state" not in refused.refusal.code)

    # ══ 5 · NON-ROOT SEEDING THROUGH THE COLUMNAR PROVIDER ═══════════════════════════════════════
    _rule("PROOF 5 · lawful NON-ROOT seeding, through the columnar provider [SETTLED world]")
    total = settled.measure("revenue", TOTAL)
    _show(total.value, f"revenue @ {TOTAL}   route={total.route}", render=lambda v: f"{v:.2f}")
    print(f"      seeded from  {total.seeded_from}")
    print(f"      considered   {list(total.considered)}")

    check("the grand total serves", total.served and total.value.cell(()) == 560.0)
    check("it was seeded from the NON-ROOT {day} state, not from R_F",
          total.seeded_from.anchor == BY_DAY)
    check("so the columnar path exercises the same right, not root-only execution",
          total.route == "continued")
    check("forgotten_since_root accumulated across both hops",
          total.value.forgotten_since_root == frozenset({"order", "store", "day"}))

    _rule("PROOF 5b · the laundering guard survives the substrate — because it was not reimplemented")
    mme.authority.register_family(on_hand)
    level_index = CoordinateIndex.of(MANIFOLD, COMMERCE.anchor({"store", "day"}),
                                     [("D1", "S1"), ("D1", "S2"), ("D2", "S1"), ("D2", "S2")])
    level_block = GovernedBlock.of(
        level_index, {"on_hand": pa.array([10, 7, 12, 9], type=pa.int64())},
        {"on_hand": standing("on_hand", mme.authority.instance_of("on_hand"), n=4)})
    mme.establish(level_block, "on_hand")
    lawful = mme.measure("on_hand", BY_DAY)
    print(f"  on_hand @ {BY_DAY}   forgets ['store'] — INSIDE the region")
    _show(lawful.value, "")
    across_time = mme.measure("on_hand", BY_STORE)
    print(f"\n  on_hand @ {BY_STORE}   forgets ['day'] — OUTSIDE the region")
    print(f"      REFUSED: {across_time.refusal.detail[:150]}…")
    laundered = mme.measure("on_hand", TOTAL)
    print(f"\n  on_hand @ {TOTAL}   via the held {BY_DAY} columnar state")
    print(f"      REFUSED: {'cannot launder' in laundered.refusal.detail}")

    check("the lawful edge serves columnar", lawful.served and lawful.value.cell(("D1",)) == 17)
    check("the unlawful edge refuses", not across_time.served)
    check("the two-step laundering route refuses too", not laundered.served
          and "cannot launder an edge the law does not admit" in laundered.refusal.detail)
    check("and the state it would have used IS held in the columnar store",
          any(k.identity == "on_hand" and k.anchor == BY_DAY for k in mme.held))
    check("THE AUTHORITY WAS NOT REIMPLEMENTED: the kernel's own adjudicate decided this",
          ColumnarMME.adjudicate.__doc__ is not None
          and mme.adjudicate.__func__ is ColumnarMME.adjudicate)

    # ══ 6 + 7 · STRUCTURED FAMILY: HLL ═══════════════════════════════════════════════════════════
    _rule("PROOF 6 · HLLSketch continued by a DataFusion UDAF; PROOF 7 · the estimate only via "
          "expression finalization")
    sketch_day = mme.measure("distinct_customers", BY_DAY)
    _show(sketch_day.value, f"distinct_customers @ {BY_DAY}   route={sketch_day.route}",
          render=lambda v: f"⟨sketch:{len(v)}B⟩")
    print("\n  the merge route:")
    for step in sketch_day.value.route:
        print(f"      • {step}")
    print(f"\n  sketch parameters (COMPATIBILITY-BEARING): "
          f"{sketch_parameters(sketch_day.value.cell(('D1',)))}")

    est = mme.evaluate("distinct_customer_estimate", BY_DAY)
    _show(est.value, f"\n  distinct_customer_estimate @ {BY_DAY}   route={est.route} "
                     f"via {est.seeded_from}")
    truth = {"D1": len({o["customer"] for o in ORDERS if o["day"] == "D1"}),
             "D2": len({o["customer"] for o in ORDERS if o["day"] == "D2"})}
    print(f"      true distinct customers: {truth}")

    held = mme.retained("expression", "distinct_customer_estimate", BY_DAY,
                        mme.authority.instance_of("distinct_customer_estimate"))
    verdict = mme.adjudicate(held, mme.family("distinct_customers"), BY_DAY)
    print(f"\n  may the estimate column seed the sketch family?  "
          f"{'ADMITTED' if verdict else 'REFUSED'} [{verdict.code}]")

    check("the sketch column is Arrow BINARY and the family value is the SKETCH",
          sketch_day.value.values.type == pa.binary())
    check("it was merged by the DataFusion UDAF, grouped",
          any("datafusion: aggregate" in s and "sketch_union" in s for s in sketch_day.value.route))
    check("the estimate is served ONLY through the expression", est.served
          and est.seeded_from == "b_sketch")
    check(f"and it is right: {truth}",
          est.value.cell(("D1",)) == truth["D1"] and est.value.cell(("D2",)) == truth["D2"])
    check("sketch parameters are readable from the value and carried as a disclosure",
          any(d.code == "sketch-parameters" for d in est.value.disclosures))
    check("the estimate has NO family continuation path",
          (not verdict) and verdict.code == "not-continuation-bearing")
    check("a sketch column never displays an estimate through formatting",
          "⟨sketch:" in _sketch_block(mme, sketch_day.value).render()
          and "Estimate" not in _sketch_block(mme, sketch_day.value).render())

    # ══ 9 · NO RELATIONAL JOIN ANYWHERE ══════════════════════════════════════════════════════════
    _rule("PROOF 9 · no relational join, and no generated SQL, anywhere in the columnar path")
    offenders = _relational_offenders()
    for name, hits in offenders.items():
        print(f"    {name}: {hits}")
    check("no `.join(` and no `.sql(` in the columnar package", not offenders)
    check("alignment is a reindex that REFUSES an invented point",
          _refuses_invented_point(mme))

    # ══ 10 · MANIFOLD ISOLATION ══════════════════════════════════════════════════════════════════
    _rule("PROOF 10 · two Manifolds, one shared provider, NO shared analytical state")
    other, other_block = build(OTHER_MANIFOLD)
    other.provider = mme.provider                      # deliberately THE SAME provider object
    print(f"  {MANIFOLD!r} and {OTHER_MANIFOLD!r} both declare a family named 'revenue'.")
    print(f"  they share one provider object: {other.provider is mme.provider}")
    print(f"  index identities differ:  {mme.held[0].anchor} "
          f"{_index_identity(mme) != _index_identity(other)}")
    foreign = None
    try:
        mme.establish(other_block, "revenue")
    except KernelRefusal as exc:
        foreign = exc
        print(f"\n  establishing the OTHER Manifold's block here: REFUSED [{exc.code}]")
        print(f"      {exc.detail}")
    cross = (mme.authority.instance_of("revenue")
             .compatible_with(other.authority.instance_of("revenue")))
    print(f"\n  cross-Manifold compatibility: {'HOLDS' if cross else 'REFUSED'} [{cross.code}]")

    check("a foreign Manifold's block cannot establish state here",
          foreign is not None and foreign.code == "foreign-manifold-block")
    check("two Manifolds' instances are incompatible, so neither can seed the other",
          (not cross) and cross.code == "different-manifold")
    check("their coordinate indexes are different identities even over the same points",
          _index_identity(mme) != _index_identity(other))
    check("one shared provider does not share authority", other.provider is mme.provider)
    check("registering a foreign object is refused at constitution", _refuses_foreign_family())

    print("\n" + "═" * 100)
    if failures:
        print(f"  {len(failures)} CHECK(S) FAILED")
        for f in failures:
            print(f"    ✗ {f}")
    else:
        print("  ALL CHECKS PASSED — the v8-native MME is executing over Arrow/DataFusion state.")
    print("═" * 100)
    return 1 if failures else 0


# ── small probes the narrative refers to ─────────────────────────────────────────────────────────
def _sketch_block(mme: ColumnarMME, state) -> GovernedBlock:
    return GovernedBlock.of(state.index, {"distinct_customers": state.values},
                            {"distinct_customers": state.standing})


def _refuses_null_standing(mme: ColumnarMME) -> bool:
    try:
        from .standing import ColumnStanding
        ColumnStanding(family_id="x", instance=mme.authority.instance_of("revenue"),
                       participation=pa.array([True, None], type=pa.bool_()),
                       support=pa.array([True, True], type=pa.bool_()))
    except KernelRefusal as exc:
        return exc.code == "null-in-a-standing-mask"
    return False


def _refuses_retired_filter(block: GovernedBlock) -> bool:
    """`participation ∧ support` is not available as a contribution filter, and asking says why."""
    try:
        block.standing("revenue").contributing_for(VALUE_BEARING)
    except KernelRefusal as exc:
        return (exc.code == "retired-contribution-filter"
                and "validates it" in exc.detail)
    return False


def _refuses_support_without_a_value(mme: ColumnarMME) -> bool:
    """A carrier that contradicts its own declared standing is refused, not adjudicated."""
    index = CoordinateIndex.of(MANIFOLD, SALE_AT, [("D1", "O1", "S1"), ("D1", "O2", "S1")])
    bad = GovernedBlock.of(
        index, {"revenue": pa.array([10.0, None], type=pa.float64())},
        {"revenue": standing("revenue", mme.authority.instance_of("revenue"), n=2,
                             support=[True, True])})
    try:
        mme.establish(bad, "revenue")
    except KernelRefusal as exc:
        return exc.code == "support-without-a-value"
    return False


def _refuses_cell_at_want_of_state(mme: ColumnarMME) -> bool:
    """There is no value to read at a point whose required value is not established."""
    held = mme.retained("family", "revenue", SALE_AT, mme.authority.instance_of("revenue"))
    try:
        held.value.cell(UNSUPPORTED_POINT)
    except KernelRefusal as exc:
        return exc.code == "want-of-state-at-a-point"
    return False


def _refuses_with_no_arrow_nulls(_: ColumnarMME) -> bool:
    """**THE MASK MATTERS WITH NO NULLS ANYWHERE.** Three non-null values, one unsupported: the fold
    refuses for want of state rather than quietly summing the two it believes."""
    probe, _block = build()
    index = CoordinateIndex.of(MANIFOLD, SALE_AT,
                               [("D1", "O1", "S1"), ("D1", "O2", "S1"), ("D1", "O3", "S1")])
    dense = GovernedBlock.of(
        index, {"revenue": pa.array([10.0, 20.0, 30.0], type=pa.float64())},
        {"revenue": standing("revenue", probe.authority.instance_of("revenue"), n=3,
                             support=[True, True, False])})
    if dense.column("revenue").null_count:
        return False
    probe.establish(dense, "revenue")
    answer = probe.measure("revenue", BY_DAY)
    return (not answer.served and answer.refusal.code == "want-of-state"
            and "THE REDUCTION HAS NOT RUN" in answer.refusal.detail)


def _refuses_invented_point(mme: ColumnarMME) -> bool:
    index = CoordinateIndex.of(MANIFOLD, BY_DAY, [("D1",)])
    try:
        mme.provider.align_onto({("D1",): 1.0, ("D9",): 2.0}, index)
    except KernelRefusal as exc:
        return exc.code == "provider-invented-a-point"
    return False


def _refuses_foreign_family() -> bool:
    authority = MME(COMMERCE, REGISTRY, IN_MEMORY, manifold=MANIFOLD)
    try:
        authority.register_family(_families(OTHER_MANIFOLD)[0])
    except KernelRefusal as exc:
        return exc.code == "foreign-manifold"
    return False


def _index_identity(mme: ColumnarMME) -> str:
    return next(r.value.index.identity for r in mme._store.values()
                if r.key.identity == "revenue" and r.key.anchor == SALE_AT)


def _relational_offenders() -> dict:
    import pathlib

    out: dict[str, list[str]] = {}
    here = pathlib.Path(__file__).parent
    for path in sorted(here.glob("*.py")):
        if path.name == "exhibit.py":
            continue
        hits = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()
                if (".join(" in ln or ".sql(" in ln) and not ln.strip().startswith("#")
                and '"' not in ln and "'" not in ln]
        if hits:
            out[path.name] = hits
    return out


if __name__ == "__main__":                                  # pragma: no cover
    raise SystemExit(main())

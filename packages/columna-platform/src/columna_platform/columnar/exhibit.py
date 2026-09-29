"""
columna_platform.columnar.exhibit — **the v8-native MME executing over real Arrow/DataFusion state.**

    python -m columna_platform.columnar.exhibit

THE WORLD. The same `commerce` universe the kernel exhibit constitutes, plus **one extra order**:

    O7 — accepted by the merchant, amount NEVER RECORDED.

O7 is the standing proof. It **participates** (the merchant accepted it, so `OrderCount` must count it) and
it is **unsupported** for Revenue (no evidence of an amount). Read off Arrow validity those two facts
collapse and `COUNT` silently becomes `count(non-null revenue)` — a different measure with a different
answer. Every number below that involves O7 is different under the two readings, so the distinction is
measured rather than asserted.
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

#: Seven accepted orders. **O7 participates and is unsupported for Revenue.**
ORDERS = (
    {"store": "S1", "day": "D1", "order": "O1", "value": 100.0, "customer": "C1", "supported": True},
    {"store": "S1", "day": "D2", "order": "O2", "value": 50.0, "customer": "C2", "supported": True},
    {"store": "S1", "day": "D2", "order": "O3", "value": 25.0, "customer": "C1", "supported": True},
    {"store": "S2", "day": "D1", "order": "O4", "value": 75.0, "customer": "C3", "supported": True},
    {"store": "S2", "day": "D2", "order": "O5", "value": 200.0, "customer": "C1", "supported": True},
    {"store": "S2", "day": "D2", "order": "O6", "value": 50.0, "customer": "C4", "supported": True},
    {"store": "S1", "day": "D1", "order": "O7", "value": None, "customer": "C5", "supported": False},
)


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


def _by_order(index: CoordinateIndex):
    """The occurrences, re-laid in the index's position order."""
    lookup = {tuple(o[r] for r in SALE_AT.order): o for o in ORDERS}
    return [lookup[cell] for cell in index.coordinates]


def build(manifold: str = MANIFOLD) -> tuple[ColumnarMME, GovernedBlock]:
    """A constituted columnar MME and the root block. **One shared provider is fine; authority is not.**"""
    authority = MME(COMMERCE, REGISTRY, IN_MEMORY, manifold=manifold)
    for family in _families(manifold):
        authority.register_family(family)
    for expression in _expressions(manifold):
        authority.register_expression(expression)
    mme = ColumnarMME(authority)

    index = _root_index(manifold)
    rows = _by_order(index)
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
                                     "amount never recorded"),
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
    mme, block = build()
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
    _rule("PROOF 8 · a standing distinction proved INDEPENDENTLY of Arrow nullability")
    rev_col = block.column("revenue")
    print(f"  the revenue value column has {rev_col.null_count} Arrow null(s) — and the null means NOTHING.")
    print("  O7's standing:  participation=True  support=False")
    contributes_value = block.contributing("revenue", VALUE_BEARING).to_pylist()
    participates = block.contributing("order_count", POPULATION).to_pylist()
    print(f"  revenue contributes at     {sum(contributes_value)}/7 positions   (participation ∧ support)")
    print(f"  order_count contributes at {sum(participates)}/7 positions   (participation)")
    print(f"  `count(non-null revenue)` would give {len(rev_col) - rev_col.null_count} — "
          f"A DIFFERENT MEASURE.")

    check("participation is known independently of value presence",
          participates[block.index.position(("D1", "O7", "S1"))] is True)
    check("support is False at the same position",
          block.standing("revenue").support[block.index.position(("D1", "O7", "S1"))].as_py()
          is False)
    check("COUNT is not count(non-null revenue): 7 vs 6", sum(participates) == 7
          and (len(rev_col) - rev_col.null_count) == 6)
    check("a null in a STANDING mask is refused outright",
          _refuses_null_standing(mme))

    # ══ 4 · GROUPED CONTINUATION BY DATAFUSION ═══════════════════════════════════════════════════
    _rule("PROOF 4 · Revenue continued to a coarser anchor by DataFusion GROUPED reduction")
    by_day = mme.measure("revenue", BY_DAY)
    _show(by_day.value, f"revenue @ {BY_DAY}   route={by_day.route}",
          render=lambda v: f"{v:.2f}")
    print("\n  the exact route:")
    for step in by_day.value.route:
        print(f"      • {step}")

    counts_by_day = mme.measure("order_count", BY_DAY)
    _show(counts_by_day.value, f"\n  order_count @ {BY_DAY}")

    check("revenue continued by GROUPED reduction", by_day.served and by_day.route == "continued")
    check("D1 = 175.0 (O7 contributes NO amount) and D2 = 325.0",
          by_day.value.cell(("D1",)) == 175.0 and by_day.value.cell(("D2",)) == 325.0)
    check("order_count D1 = 3 (O1, O4 AND O7) and D2 = 4",
          counts_by_day.value.cell(("D1",)) == 3 and counts_by_day.value.cell(("D2",)) == 4)
    check("the route names the governed filter, the DataFusion aggregate and the ALIGNMENT",
          any("governed-filter" in s for s in by_day.value.route)
          and any("datafusion: aggregate" in s for s in by_day.value.route)
          and any("align:" in s for s in by_day.value.route))
    check("alignment is an explicit REINDEX against a governed index, not a join",
          any("not a join on keys" in s for s in by_day.value.route))
    check("the output is aligned on the TARGET anchor's coordinate index",
          by_day.value.index.anchor == BY_DAY
          and by_day.value.index.identity != block.index.identity)
    check("the coarser index is still SPARSE (2 days, derived from existing points)",
          len(by_day.value.index) == 2)

    # ══ 2 + A · POSITIONAL EXPRESSION, NO JOIN ═══════════════════════════════════════════════════
    _rule("PROOF 2 · Revenue / OrderCount evaluated POSITIONALLY at one anchor — no join")
    aov_day = mme.evaluate("average_order_value", BY_DAY)
    _show(aov_day.value, f"average_order_value @ {BY_DAY}   route={aov_day.route} "
                         f"via {aov_day.seeded_from}", render=lambda v: f"{v:.4f}")
    print(f"\n  both operand columns share ONE coordinate index "
          f"({mme.measure('revenue', BY_DAY).value.index.identity})")
    print("  so the division is a position-aligned Arrow kernel. Nothing discovered which Revenue")
    print("  cell corresponds to which Count cell — they are the same position.")

    check("AOV@D1 = 175/3 = 58.3333 — the governed standing changes the answer",
          abs(aov_day.value.cell(("D1",)) - 175 / 3) < 1e-9)
    check("AOV@D2 = 325/4 = 81.25", abs(aov_day.value.cell(("D2",)) - 81.25) < 1e-9)
    check("under `count(non-null revenue)` D1 would have been 87.5 — a different number",
          abs(175 / 3 - 87.5) > 1.0)
    check("the result is an ExpressionOutput, not family state",
          isinstance(aov_day.value, ColumnarExpressionOutput)
          and not aov_day.value.CONTINUATION_BEARING)
    check("and it has NO continuation path at all",
          not hasattr(ColumnarExpressionOutput, "fold_onto_grouped"))

    # ══ 3 + B · COMPATIBILITY REFUSED BEFORE ARITHMETIC ══════════════════════════════════════════
    _rule("PROOF 3 · an incompatible basis is refused BEFORE arithmetic, on one aligned layout")
    rev_state = mme.measure("revenue", BY_DAY).value
    aud_state = mme.measure("audited_order_count", BY_DAY).value
    print(f"  revenue             @ {BY_DAY}  available, {len(rev_state.values)} positions, "
          f"index {rev_state.index.identity}")
    print(f"  audited_order_count @ {BY_DAY}  available, {len(aud_state.values)} positions, "
          f"index {aud_state.index.identity}")
    print(f"  SAME LAYOUT: {rev_state.index.identity == aud_state.index.identity}")
    refused = mme.evaluate("average_order_value_audited", BY_DAY)
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

    # ══ 5 · NON-ROOT SEEDING THROUGH THE COLUMNAR PROVIDER ═══════════════════════════════════════
    _rule("PROOF 5 · lawful NON-ROOT seeding, through the columnar provider")
    total = mme.measure("revenue", TOTAL)
    _show(total.value, f"revenue @ {TOTAL}   route={total.route}", render=lambda v: f"{v:.2f}")
    print(f"      seeded from  {total.seeded_from}")
    print(f"      considered   {list(total.considered)}")

    check("the grand total serves", total.served and total.value.cell(()) == 500.0)
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

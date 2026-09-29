"""
columna_platform.frameql.exhibit — **real Frame-QL text, served end to end.**

    python -m columna_platform.frameql.exhibit

Every string below is actual Frame-QL, parsed by the ratified envelope grammar. Nothing is constructed
programmatically on the request side: the only inputs are the query text and the constituted world that
`columna_platform.kernel.exhibit` builds.

The five required proofs are the five sections. Everything printed is computed.
"""
from __future__ import annotations

from columna_platform.kernel import exhibit as WORLD
from columna_platform.kernel.exhibit import BY_DAY
from columna_platform.kernel.mme import Retained, RetentionKey

from .serving import (
    DISCLOSE,
    REFUSE,
    SERVE,
    SYNTAX,
    UNRESOLVED,
    UNSUPPORTED,
    FrameQLService,
)


def _rule(title: str) -> None:
    print(f"\n{'─' * 100}\n{title}\n{'─' * 100}")


def main() -> int:                                          # noqa: C901 - an exhibit is a narrative
    mme = WORLD.build()
    service = FrameQLService(mme)
    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        print(f"    {'✓' if condition else '✗'} {label}")
        if not condition:
            failures.append(label)

    def run(query: str):
        outcome = service.serve(query)
        print(outcome.render())
        print()
        return outcome

    print("═" * 100)
    print("  COLUMNA PLATFORM · real Frame-QL → v8-native MME")
    print(f"  universe {WORLD.COMMERCE.name!r}  constituents {sorted(WORLD.COMMERCE.references)}")
    print(f"  families    {mme.families}")
    print(f"  expressions {mme.expressions}")
    print("═" * 100)

    # ══ 1 · DIRECT FAMILY ════════════════════════════════════════════════════════════════════════
    _rule("PROOF 1 · direct family — Revenue at an admitted anchor, served through family continuation")
    root = run("SELECT revenue AT {store * day * order}")
    day = run("SELECT revenue AT {day}")
    both = run("SELECT revenue, order_count AT {day}")
    total = run("SELECT revenue AT {}")

    check("the root ask serves", root.classification == SERVE)
    check("the coarser ask serves through family CONTINUATION",
          day.classification == SERVE and day.frame.columns[0].route == "continued")
    check("resolved as a FAMILY", day.sorts["revenue"] == "family")
    check("D1 = 175.0 and D2 = 325.0",
          dict(zip((r[0] for r in day.frame.rows), (r[1] for r in day.frame.rows)))
          == {"D1": 175.0, "D2": 325.0})
    check("two series at one anchor come back as one frame",
          both.classification == SERVE and len(both.frame.columns) == 2 and len(both.frame.rows) == 2)
    check("`AT {}` is the grand total, a declared location", total.frame.rows == ((500.0,),))
    check("the grand total was seeded from a NON-ROOT materialization",
          "commerce{day}" in (total.frame.columns[0].via or ""))

    # ══ 2 · STRUCTURED-FAMILY FINALIZATION ═══════════════════════════════════════════════════════
    _rule("PROOF 2 · structured family — the sketch continues; the user asks for the estimate; the "
          "estimate's scalar cannot seed")
    sketch = run("SELECT distinct_customers AT {day}")
    estimate = run("SELECT distinct_customer_estimate AT {day}")

    print("  the user asked for the ESTIMATE. **It is not cached — MME v1 has no expression cache**")
    print("  (M-2 §1). It was evaluated above the engine from family state the engine supplied. Offer")
    print("  its scalar back to the MME as continuation state and see what happens:")
    served_estimate = estimate.frame.columns[0]
    from_above = Retained(
        key=RetentionKey(identity="distinct_customer_estimate", anchor=BY_DAY,
                         instance=mme.expression("distinct_customer_estimate").instance(),
                         realization=mme.realization),
        value=service.expressions.evaluate(
            mme.expression("distinct_customer_estimate"), BY_DAY).value)
    verdict = mme.adjudicate(from_above, mme.family("distinct_customers"), BY_DAY)
    print(f"    held by the MME?  "
          f"{any(k.identity == 'distinct_customer_estimate' for k in mme.held)}")
    print(f"    offered from above: continuation_bearing={from_above.continuation_bearing}")
    print(f"    verdict:  {'ADMITTED' if verdict else 'REFUSED'} [{verdict.code}]")
    print(f"              {verdict.detail}\n")

    check("the estimate is NOT held by the MME — family materializations only (M-2 §1)",
          all(k.identity != "distinct_customer_estimate" for k in mme.held))
    check("offered from above it is refused as continuation state, by a governed verdict",
          (not verdict) and verdict.code == "not-continuation-bearing")
    check("and Platform serving supported the expression fully all the same",
          served_estimate.route == "evaluated")
    check("the sketch family serves and CONTINUES", sketch.frame.columns[0].route == "continued")
    check("its served value is a sketch, not a number",
          hasattr(sketch.frame.rows[0][1], "get_estimate"))
    check("the estimate resolves as an EXPRESSION",
          estimate.sorts["distinct_customer_estimate"] == "expression")
    check("the estimate is EVALUATED from its basis", estimate.frame.columns[0].route == "evaluated")
    check("it serves the right cardinality per day — D1 {C1,C3}=2, D2 {C1,C2,C4}=3",
          sorted(r[1] for r in estimate.frame.rows) == [2, 3])
    check("the sketch column renders OPAQUELY: a structured value is not a display value",
          all(r[1].__class__.__name__ == "hll_sketch" for r in sketch.frame.rows)
          and "⟨hll_sketch⟩" in sketch.frame.render())
    check("and the frame DISCLOSES that, naming the finalization that is the lawful route to a number",
          any(d.code == "structured-family-value" and "HLL_ESTIMATE" in d.detail
              for d in sketch.disclosures))
    check("both asks carry the approximation as a DISCLOSURE",
          sketch.classification == DISCLOSE and estimate.classification == DISCLOSE)
    check("the estimate's scalar is NOT continuation-bearing",
          not from_above.continuation_bearing)

    # ══ 3 · GOVERNED EXPRESSION ══════════════════════════════════════════════════════════════════
    _rule("PROOF 3 · governed expression — AOV over Revenue + OrderCount, pooled correctly")
    aov_day = run("SELECT average_order_value AT {day}")
    aov_total = run("SELECT average_order_value AT {}")
    explained = run("EXPLAIN SELECT average_order_value AT {}")

    by_day = {r[0]: r[1] for r in aov_day.frame.rows}
    pooled = aov_total.frame.rows[0][0]
    print(f"  pooled  {pooled:.4f}     mean of the daily means  "
          f"{(by_day['D1'] + by_day['D2']) / 2:.4f}\n")

    check("AOV resolves as an EXPRESSION, never a family",
          aov_day.sorts["average_order_value"] == "expression")
    check("AOV@D1 = 175/2 = 87.5", abs(by_day["D1"] - 87.5) < 1e-9)
    check("AOV@D2 = 325/4 = 81.25", abs(by_day["D2"] - 81.25) < 1e-9)
    check("AOV@total = 500/6 = 83.3333 — the POOLED result", abs(pooled - 500 / 6) < 1e-9)
    check("and NOT 84.375, the mean of the daily means",
          abs(pooled - (by_day["D1"] + by_day["D2"]) / 2) > 1.0)
    check("it was established from a named basis",
          aov_day.frame.columns[0].via == "b_revenue_ordercount")
    check("EXPLAIN reports the authority path and serves nothing",
          explained.frame is None and any("NOT EXECUTED" in s for s in explained.plan))
    check("no Mean FAMILY exists to have served it", "mean_order_value" not in mme.families)

    # ══ 4 · COMPATIBILITY REFUSAL ════════════════════════════════════════════════════════════════
    _rule("PROOF 4 · compatibility refusal — individually available operands, jointly meaningless")
    available = run("SELECT revenue, audited_order_count AT {day}")
    refused = run("SELECT average_order_value_audited AT {day}")

    check("BOTH operands serve when asked for directly", available.classification == SERVE)
    check("the expression over them REFUSES", refused.classification == REFUSE)
    check("the reason survives the serving layer verbatim",
          "different-participation" in str(refused.refusal)
          and "jointly meaningless" in str(refused.refusal))
    check("and it is not a claim that the operands are absent",
          "physical availability is not analytical authority" in str(refused.refusal))

    # ══ 5 · CONTINUATION-REGION REFUSAL, INCLUDING THE LAUNDERING CASE ═══════════════════════════
    _rule("PROOF 5 · continuation-region refusal — a stock across time, directly and via an "
          "intermediate materialization")
    lawful = run("SELECT on_hand AT {day}")
    across_time = run("SELECT on_hand AT {store}")
    laundered = run("SELECT on_hand AT {}")

    check("summing a stock ACROSS STORES at one day serves", lawful.classification == SERVE)
    check("summing it ACROSS TIME refuses", across_time.classification == REFUSE)
    check("the refusal names the CLOSURE, not an absence",
          "outside-continuation-region" in str(across_time.refusal))
    check("the two-step route through the held {day} state refuses too",
          laundered.classification == REFUSE)
    check("and says why: an intermediate cannot launder an inadmissible edge",
          "cannot launder an edge the law does not admit" in str(laundered.refusal))
    check("while the state it would have used IS held — availability is not authority",
          any(k.identity == "on_hand" and k.anchor == BY_DAY for k in mme.held))

    # ══ the refusal taxonomy, exercised ══════════════════════════════════════════════════════════
    _rule("ADDENDA · the other three classifications, so the taxonomy is not decorative")
    unknown = run("SELECT profit AT {day}")
    unsupported = run("SELECT revenue AT {day} WHERE store = 'S1'")
    composed = run("SELECT revenue / order_count AT {day}")
    bad_anchor = run("SELECT revenue AT {region}")
    syntax = run("SELECT revenue FROM WHERE")

    check("an unknown name is UNRESOLVED, not 'no family answers to it'",
          unknown.classification == UNRESOLVED
          and "not a claim that no FAMILY answers" in str(unknown.refusal))
    check("WHERE is UNSUPPORTED and says it is a capability limit",
          unsupported.classification == UNSUPPORTED
          and "CAPABILITY limit, not a governed one" in str(unsupported.refusal))
    check("an arithmetic series is refused: this profile is EXPRESSION-FIRST",
          composed.classification == UNSUPPORTED
          and "expression-text-in-series" in str(composed.refusal))
    check("an unknown anchor constituent is refused where the query text is still in hand",
          bad_anchor.classification == UNSUPPORTED
          and "unknown-anchor-constituent" in str(bad_anchor.refusal))
    check("malformed text is a SYNTAX outcome and nothing else",
          syntax.classification == SYNTAX)
    check("every classification is reachable",
          {root.classification, sketch.classification, refused.classification,
           unknown.classification, unsupported.classification, syntax.classification}
          == {SERVE, DISCLOSE, REFUSE, UNRESOLVED, UNSUPPORTED, SYNTAX})

    print("\n" + "═" * 100)
    if failures:
        print(f"  {len(failures)} CHECK(S) FAILED")
        for f in failures:
            print(f"    ✗ {f}")
    else:
        print("  ALL CHECKS PASSED — real Frame-QL is serving through the v8-native MME.")
    print("═" * 100)
    return 1 if failures else 0


if __name__ == "__main__":                                  # pragma: no cover
    raise SystemExit(main())

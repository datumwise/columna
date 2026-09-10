# Joint Review — Two Exact Editorial Corrections

**7 September 2026 · Prepared for staged documentation adoption**

The reviewed sources remain unchanged. These are the only textual corrections requested by this review. They do not revise the theory, equations, syntax, profile promises, or acceptance-case judgments. Source hashes and exact replacement strings are in the matching JSON; the unified diffs preserve surrounding context.

## J1 — Carry the supported-observation participation premise into the local 97-observation example; T §11.5.1 and case E02 already state the rule.

**Destination:** `frameql_language_vnext_working_draft_v0_4.md`, §6.3, source line 747.

**Replace:**

Suppose 100 orders are known to exist but Revenue is supported on only 97.

Then, conceptually:

```text
count(order)              = 100
count(revenue @ {order})   = 97
```

unless a separate totality/support rule establishes another result.

**With:**

For this example, governance establishes exactly 100 participating Order points. The declared `count(revenue @ {order})` law counts the Order points with supported Revenue, and exactly 97 satisfy that participation rule.

Under those declared rules:

```text
count(order)              = 100
count(revenue @ {order})   = 97
```

The 97 follows from the stated supported-observation participation rule, not from the spelling `count(x @ I)` alone. Another declared participation rule must be evaluated on its own terms. Neither count permits the intended population of a different target, such as a mean over all 100 Order points, to shrink silently.

## J2 — Resolve the otherwise orphaned [S6] citation in §10 without giving the historical handoff current operational authority.

**Destination:** `columna_o3_governed_analytical_order_v0_2.md`, §17, supporting §10, source line 378.

**Replace:**

The full original O3 v0.1 is retained in the editorial archive, including its sources, historical inspector references, and previous validation record.

**With:**

**[S6] Historical architecture handoff.** `START_HERE(2).md`, 14 August 2026, identified as source S6 in O3 v0.1 §17. Section 10 cites it only for the persistent separation of logical publication, private mapping, certification, serving admission, and planner/engine responsibility. Its operational status is historical, not current.

The full original O3 v0.1 is retained in the editorial archive, including its sources, historical inspector references, and previous validation record.

## Adoption boundary

The edits were replayed in memory against the source-hash-pinned files and checked for uniqueness and preservation of equations and fenced examples. They have not been installed as new current editions. During staged adoption, assign appropriate revision metadata and update the active index and links together. Do not overwrite reviewed baselines or imply publication from this patch set.

J2 is a reference-hygiene correction, not a new lifecycle design. Its historical provenance was verified against O3 v0.1 §17, source S6. No current repository or deployment status was checked.

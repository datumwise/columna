# Frame-QL Jurisdiction Repair — Design and Implementation Sequence v0.1

**Date:** 1 September 2026
**Measured against:** `f18ba06` (branch `reconciliation/family-law-capability-state`)
**Governing ruling:** Frame-QL Request Adjudication and Disposition Ruling v0.2
**Rows in scope:** P1-19 … P1-27, P0-20 (the 2026-09-01 adjudication sweep)
**Status:** PROPOSAL — no code changed by this document.

---

## 0. The finding that shapes the whole plan

The tree is in much better condition for this repair than the sweep's ten rows suggest, because
**the disposition vocabulary is already centralized, closed, and fail-closed.**

- `REASON_OUTCOME` (`disclosure.py:207-317`) is a single table mapping every reason string to
  `(kind, discriminator)`.
- `outcome_for` (`disclosure.py:324-343`) raises `UnregisteredReason` rather than defaulting — the
  result of a 2026-08-20 ruling taken precisely because two reasons had silently defaulted for months.
- `Outcome.classified()` (`disclosure.py:364-371`) is a single chokepoint. The engine never sets
  `kind`; the planner stamps it in exactly one place.
- `Refusal` (`disclosure.py:397`) is explicitly documented as *"plumbing — a structured goto"*, never
  handed to a surface.

**Consequence: the jurisdiction repair is a table edit, not a code sweep.** Adding a third element to
`REASON_OUTCOME` is exhaustive *by construction* — `outcome_for` is fail-closed, so a reason that has
not been given a jurisdiction cannot reach a surface. There is no way to forget one, and no way for a
future reason to slip through unclassified. That property is why this plan is short, and it is why the
sequence below leads with the seam rather than with the severity.

A second piece of existing structure carries the plan's other half. `run_statement`
(`planner.py:947-957`) is the **single entry point for both plan and run** — `plan_statement` is
literally `run_statement(stmt, execute=False)` — and it already contains a shared pre-branch region:

```python
d = self.desugar(stmt)                                   # canonical AST
columns = self._engine_columns(d)
self._check_name_collisions(columns, d.anchor)
where = " AND ".join(d.where) if d.where else None
unreachable = self._where_reachability(columns, d.where) if d.where else None   # <- the only occupant
fr = (self.run if execute else self.plan)(d.anchor, columns, where, where_unreachable=unreachable)
```

`_where_reachability` is the P1-14 capability gate, and it sits **above** the plan/run branch. That is
exactly why `WHERE` has plan/run parity and faces and scans do not. **The seam for parity already
exists and has one occupant.** Generalizing it is the repair, not building it.

---

## 1. The four seams

### Seam A — jurisdiction becomes a column of the closed reason table

Every `Outcome` acquires a `jurisdiction` stamped at the same chokepoint that stamps `kind`:

```text
LANGUAGE      the request never became a valid canonical Frame-QL request   (Stage A)
ANALYTICAL    a valid request, adjudicated: Refuse / Clarify / Admit        (Stage B)
REALIZATION   an admitted request this profile/build cannot realize         (Stage C)
```

`REASON_OUTCOME[reason]` becomes `(kind, discriminator, jurisdiction)`; `outcome_for` returns the
triple; `classified()` stamps all three. Because `outcome_for` is fail-closed, **classifying every
existing reason is forced in one commit** and no reason can be added later without one.

**This is deliberately an INTERNAL change in step 1.** Ruling v0.2 §13 states the ruling *"intentionally
does not canonize wire strings for these statuses"*, and `CONTRACT_VERSION` is currently `"4"` with at
least two tests asserting that literal. So jurisdiction is stamped, tested, and used internally
**without changing the wire**; the wire moods are a separate, later, versioned step that needs a ruling
(see §6). This ordering is what lets the correctness repairs land without waiting on a wire decision.

**Naming.** Per the vocabulary ruling, the realization concept is **not** called `unsupported` — that
word is already the analytical discriminator at `disclosure.py:80` — and canonical → execution
representation is **not** called `lowering`. This document uses `jurisdiction ∈ {language, analytical,
realization}` and, for the eventual wire mood, **`realization_gap`**. The existing reason strings
(`unsupported`, `filter_unsupported`) keep their spellings as build vocabulary until the wire step, per
§4's *"remain build vocabulary until separately migrated"*.

### Seam B — a validity stage that owns all substrate parsing

Today `ast.parse` runs deep inside `plan` (`planner.py:1673`), and `_where_reachability` itself calls
`ast.parse` in a bare `try/except Exception: continue` (`planner.py:849-851`). A substrate exception
raised there escapes as the language's answer (P1-26).

Introduce **one validity pass over the canonical statement**, run in `run_statement` before adjudication,
which owns every call into the Python substrate and converts any failure into a Frame-QL `LANGUAGE`
outcome with a Frame-QL message. It is also the natural and only correct home for:

- named order-axis validation (P1-24: `plan_order_axis` currently begins `if by is not None: return by`);
- predicate-name category checks (P1-22: is the name a declared level at all?);
- the §4.5:660 macro/level collision rule, which is documented and unbuilt (P1-27).

**No CPython exception type may cross this boundary.** The invariant is testable directly (§5).

### Seam C — canonical form is total, and is the only input to realization

This is the seam that makes "the system answered a different request" **unreachable** rather than fixed,
which is what the mission asks for in place of a new disposition.

**C1 — `desugar` becomes total.** `desugar` (`planner.py:670-702`) substitutes bindings into
`stmt.series` and then copies the rest verbatim:

```python
where=list(stmt.where), having=list(stmt.having), order_by=list(stmt.order_by), limit=stmt.limit
```

Apply the same substitution to `where`, `having` and `order_by`, then **assert totality**: no binding
name may survive anywhere in the canonical statement. The assertion is the repair; the substitution is
merely what makes it pass. P1-27 becomes structurally impossible rather than locally corrected.

**C2 — the manifold is resolved from the canonical statement.** `execute_frame_query`
(`tools.py:291-302`) resolves from the `manifold_id` argument and never reads `stmt.from_manifold`.
Invert it: the canonical statement's `FROM` governs; `manifold_id` is the **authorized binding** used
only when `FROM` is omitted — which is precisely Ruling v0.2 §10's *"Omitted Manifold with one
authorized binding"*. An explicit `FROM` naming a different or unknown Manifold is a `LANGUAGE` outcome,
never a silent substitution.

**C3 — the conformance invariant.** With C1 and C2, the request realized is a pure function of the
canonical statement. State it as a property and test it (§5): *nothing outside the canonical statement
may influence which request is answered.* This is the architectural answer to "wrong question correctly
answered" — no new status, an unreachable state.

### Seam D — adjudication completes before the plan/run branch

Move every capability and ambiguity adjudication into `run_statement`'s existing pre-branch region,
alongside `_where_reachability`:

- face-crossing capability (P1-21), so `check_frame_query` cannot promise `serve` for what
  `execute_frame_query` refuses;
- scan-order adjudication (P1-24), all four §11 cases decided once;
- **driver family cardinality (P1-20)** — this is the important one conceptually. The engine's
  `next(iter(dmeas.family))` (`engine.py:431-432`) is not a bug to guard; it is an *adjudication
  performed in the realization layer*. Deciding the member is Stage B work, so it moves to Stage B and
  the engine receives an already-decided member. The guard is then unnecessary rather than added.

**Invariant:** for every form, `plan(f).outcome == run(f).outcome`. Generalizes P1-14 from `WHERE` to
everything.

### Why P1-25 needs no seam of its own

`_pin_verdicts` (`planner.py:1622-1629`) wraps `_admit_pin` in one `except Refusal` and treats every
caught refusal as a verdict *about the pin*. Once Seam A lands, the filter is one line of meaning: only
`ANALYTICAL` verdicts are pin evidence; a `LANGUAGE` verdict is not a fact about the candidate level and
must propagate immediately. The corrupted `blocked_reduction` — whose central sentence *"there is no pin
that rescues this ask"* is false while three pins rescue it and one serves — stops being constructible.
This is the clearest demonstration that the ten rows are one defect: P1-25's repair is a consequence of
Seam A, not a separate fix.

---

## 2. Landing order, and why

Six steps. The ordering is by **dependency and blast radius**, not by severity — with one exception,
taken deliberately.

**Step 0 — conformance. Closes P1-19, P1-27. (Seam C)**
Taken first *out of dependency order* because these are the only two rows where a wrong number reaches
a reader, and the only two that need no new ruling — v0.2 §9 and §14 already decide both. Neither
depends on Seam A. Two small, independent changes plus two assertions. **This step is worth authorizing
on its own even if the rest waits.**

**Step 1 — jurisdiction, internal only. Closes nothing; enables everything. (Seam A)**
One table edit forced to exhaustiveness by `outcome_for`. No wire change, no behaviour change, no row
closed. Landing it alone and green is the point: it is a pure refactor whose diff is a column of
classifications that a reader can review as a list, and every later step becomes a relabeling instead of
a rewrite. **If this is skipped, steps 3-4 become seven local patches that can each undo the next.**

**Step 2 — validity stage. Closes P1-26; closes half of P1-22; supplies P1-24's invalid-order case. (Seam B)**
Depends on Seam A for somewhere to put `LANGUAGE`. Independent of Seams C and D.

**Step 3 — adjudication before the branch. Closes P1-20, P1-21; completes P1-24. (Seam D)**
Depends on Seam A. This is the largest code movement in the plan and should land alone.

**Step 4 — relabel to §16, and the `_pin_verdicts` filter. Closes P1-22, P1-23, P1-25.**
Mechanical after Steps 1-3, and every item already ruled by v0.2 §16. Amends four standing tests (§4).

**Step 5 — the conformance gate, two-way. Closes P0-20. (§6)**
Deliberately last among the code steps: the gate should be pointed at a build whose dispositions are
already correct, or it will pin the current wrong ones as expectations. Landing the gate before Step 4
would bake in exactly what Step 4 repairs.

**Step 6 — wire moods. Closes nothing; NEEDS A RULING FIRST (§7).**
`CONTRACT_VERSION` is `"4"` and asserted literally in at least two tests. Surfacing `invalid` and
`realization_gap` on the wire is a versioned contract change, and v0.2 §13 explicitly declines to
canonize the strings. Sequenced last and gated on a ruling so the correctness work never waits on it.

### Row → step map

| row | closed or simplified by | how |
|---|---|---|
| **P1-19** | Step 0 | manifold resolved from canonical `FROM`; binding applies only when omitted |
| **P1-27** | Step 0 | `desugar` total + totality assertion; §4.5:660 collision rule built in Step 2 |
| **P1-26** | Step 2 | no substrate exception crosses the validity boundary |
| **P1-22** | Steps 2 + 4 | Invalid vs Refuse split by category check; alternatives filtered to lawful readings |
| **P1-24** | Steps 2 + 3 | invalid `by=` at Stage A; several/no lawful orders adjudicated pre-branch |
| **P1-20** | Step 3 | member decided in Stage B; engine receives it |
| **P1-21** | Step 3 | face capability pre-branch; reason re-registered `realization`; detail corrected |
| **P1-23** | Step 4 | co-anchor law re-registered `analytical` (Refuse) |
| **P1-25** | Steps 1 + 4 | `_pin_verdicts` counts only `ANALYTICAL` verdicts as pin evidence |
| **P0-20** | Step 5 | expectation-based, two-way gate |

---

## 3. Tests that intentionally pin the old behaviour and must change

Each of these was written on purpose to hold the current shape. They are not incidental breakage and
should be named in the authorization rather than discovered during it.

| test | pins | change |
|---|---|---|
| `test_where_capability_gate.py:84-88` | *"`filter_unreachable` … stays a CLARIFY"*, asserting `outcome == "clarify"` | split: Invalid for a non-level, Refuse for an unreachable level. **Preserve its intent** — the distinction it defends (Manifold-fact vs build-fact) survives; it is the *disposition* that was wrong |
| `test_map_operand_pin.py:93-99` | `nr["reason"] == "unsupported"` for the co-anchor prohibition | reason re-registered as `analytical`; assert Refuse |
| `test_inline_reduction.py:165-187` | `sum(level)` → `refuse/blocked_reduction` | becomes Clarify over the family; the `blocked_reduction` assertion goes |
| `test_case_demo_recapture.py:222-231` | `("refuse","chained_crossing","unsupported")` under a docstring reading *"A well-formed ask with no lawful path is a REFUSE"* | becomes a realization gap; **the docstring's premise is the false one and must change with it** |
| `test_p05a_execution_contract.py:246-249` | `fr.outcome in ("refuse","error")` | already permissive; passes unchanged. Tighten to the exact disposition once Step 3 lands |

`test_p05a_execution_contract.py:277-281` (the cumulative walk) **must not change** — it is the evidence
that P0-20's Manual claim is false, and it has been correct all along.

---

## 4. New invariant-level tests

Six properties, each stated once and checked over the whole corpus rather than per-row. These are what
prevent recurrence; the row-level assertions above only prevent regression.

1. **Jurisdiction totality.** Every reason in `REASON_OUTCOME` has a jurisdiction, and `outcome_for`
   raises for any reason that does not. (Free, given fail-closed; assert it so a future edit cannot
   quietly widen the table.)
2. **No substrate escape.** For a corpus of malformed inputs — the bracket filter, `count(*)`,
   deliberately broken expressions — the surface returns a Frame-QL outcome and **never** raises a
   non-Frame-QL exception type. Assert on the exception *type*, not the message.
3. **Plan/run parity.** For every form in `specs/frameql_build_conformance_matrix_v0_1.md`,
   `plan(f).outcome == run(f).outcome`. The matrix already enumerates 99 forms; this turns it from a
   snapshot into a live invariant without normalizing it.
4. **Canonical conformance.** The realized request is a pure function of the canonical statement:
   for a statement with explicit `FROM`, varying the serving binding cannot change the result; and no
   binding name survives desugaring. Directly encodes C3.
5. **No realization-resolved ambiguity.** Where several lawful readings exist, the disposition is
   Clarify regardless of declaration order — the P1-20 fixture (`FAMILY { min max }` vs
   `FAMILY { max min }`) run both ways must give the *same* disposition. This is the sharpest available
   test of "realization facts cannot resolve analytical ambiguity" and it already exists as a probe.
6. **Clarify alternatives are lawful readings.** Every alternative offered on a Clarify, when submitted,
   must itself be admitted. Today five of eight `filter_unreachable` alternatives fail this, and P1-27's
   Clarify offers the querent's own binding as the remedy.

Property 6 is the one I would most want in place permanently: it is cheap, it is checkable across the
whole reason table, and it catches the entire class of "polite failure dressed as a menu".

---

## 5. The conformance gate (P0-20)

The requirement is drift detection **in both directions**, without making a capability improvement a red
gate that invites reverting the improvement.

**Recommended: declared expectations, with an asymmetric remedy.**

Each Manual example declares its expected disposition (in the fence info string, which already carries
`frameql-roadmap` / `frameql-illformed` and so is the established channel). The gate runs every example
and compares observed to declared. Both directions fail — but they fail as **distinct classes with
distinct remedies**:

```text
CLAIM_EXCEEDS_BUILD    the Manual promises more than the build delivers
                       -> red. The Manual is wrong, or the build regressed.

CAPABILITY_IMPROVED    the example now does more than the Manual claims
                       -> red, with a remedy that is a ONE-LINE DOC EDIT and never a code revert.
                          The failure message says so explicitly.
```

This satisfies the constraint exactly: implementing a roadmap feature *does* turn the gate red, which is
correct — the Manual is now false — but the only sanctioned fix is to update the mark. Nothing in the
gate ever asks for the capability to be withdrawn, and the message must say that in words, because a
red gate with an ambiguous remedy is how capability gets reverted by a hurried contributor.

Two structural fixes alongside it:

- **Promote the seven unchecked bare Frame-QL blocks.** `_STMT_START` (`check_manual_frameql.py:200-202`)
  skips a fenced block whose first line does not begin `EXPLAIN|FROM|WITH|SELECT`, which silently drops
  §3.1, §3.2, §4.3, §4.4 (×2), §1.2 and §1.3. §3.2's sugar equivalence is **false** and has never been
  looked at.
- **Report blocks and statements separately.** The current headline — `40 total` — counts statements,
  while 44 blocks exist and 9 are skipped. The near-coincidence of 44 and 40 hides the gap in the one
  line anyone reads. Report both, and report the skip list.

**The build conformance matrix stays a measured snapshot.** It is the input that makes invariant 3
possible, and normalizing it to match documentation would destroy exactly the evidence that found these
rows. Regenerate it after each step; diff the regenerations. The diffs are the repair's proof.

---

## 6. Documentation that must follow the code, not precede it

Nothing in the Manual should move until the dispositions are correct, because most of the sections in
question describe behaviour that is about to change. Specifically, after Step 4:

- §2.8 and §6.11's scan-execution claims are false in six of eight cases **today** and will be false
  differently after Step 3 — correct once, at the end.
- §4.1's `filter_unreachable` prose describes a single Clarify that will have become two dispositions.
- §7.4's disclosure catalogue never learned `filter_unsupported` and will need the whole jurisdiction
  column, not one entry.
- §3.2's sugar equivalence is false now and should be corrected on evidence from the repaired build.
- §4.5:660's collision rule is documented and unbuilt; Step 2 builds it, and the Manual sentence should
  then be checked against what was built rather than the reverse.

The one documentation change that should **precede** the code is this document, plus the ledger rows
already landed — so that the repair is executed against a written intent.

---

## 7. Questions that need a ruling before implementation

Three. The first is genuinely blocking for one sub-case of P1-24; the others are sequencing.

**7.1 — BLOCKING. Does naming an order axis confer order standing?**
`plan_order_axis` begins `if by is not None: return by` — the named axis is never validated. Today
`by='customer'` (a real level, in-anchor, **non-temporal, conferring no certified order**) *serves*,
silently walking an axis the unnamed path refuses to derive. Two readings are both supported by the
corpus, and they produce different implementations:

- v0.2 §11 *"A requester may select among declared lawful orders where the language permits"* → `by=`
  is validated against the **lawful order set**, and `by='customer'` is Invalid (or Refuse) because
  `customer` confers no governed order.
- Ruling 0.1 §7 *"A query cannot manufacture an undeclared order law merely by naming a physical sort
  key"* → the same conclusion, more strongly.

Both readings point the same way, which is why I raise it rather than assume it: **the current
behaviour serves, and changing it stops a form that works today.** That is a capability withdrawal, and
under the stop condition it is not mine to take unilaterally. Please rule on whether `by=` may name any
in-anchor level or only a level with governed order standing.

**7.2 — Wire representation of `invalid` and `realization_gap`.** v0.2 §13 declines to canonize the
strings; `CONTRACT_VERSION` is `"4"` and literally asserted in tests. Step 6 needs a ruling on the wire
moods and the version bump. Steps 0-5 are sequenced not to depend on it.

**7.3 — Non-blocking, flagged for the restructuring.** §4.5:660 says macro/level collisions are
*"refused"*. Under v0.2 that is a Stage-A name-category failure, i.e. **Invalid**, not Refuse. I intend
to implement Invalid; the Manual sentence predates the Invalid/Refuse split and should be corrected in
the restructuring rather than the implementation bent to match the older word.

**Not blocking, per the mission:** bracket-filter canonical status stays open — the substrate escape is
repaired either way, and Step 2 does not depend on the ruling.

---

## 8. Stop-condition check

No step in this plan changes canonical Frame-QL meaning, Measure Algebra law, or the Core/Platform
boundary. Every step brings the implementation into conformance with them. The one place where the
question arises is 7.1, where a form that serves today would stop serving — raised above rather than
implemented.

**Explicitly kept out**, per the mission: P1-12 support representation; P1-18 `region_label`;
multiple-finalizer formalization; positive capability-admission representation; default-anchor
materiality (which v0.2 §16 independently routes to a future disclosure-materiality ruling); the
certification/current-admission classification; and Platform implementation.

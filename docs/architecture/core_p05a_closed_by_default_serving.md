# Core-P0.5a — Closed-by-default governed serving (design → implementation)

**Status:** **CLOSED — implemented and merged** (`9bde8ea`, PR #174, 2026-08-16). Ruling by Huayin
2026-08-11; design approved 2026-08-13; implementation GO (bounded scope below) delivered in full.
See "Closure record" at the end of this document.
**Date:** 2026-08-13 (design) · 2026-08-16 (closed)
**Sources:** `columna` @ main (`0.15.0-core`). Tracks issue #172. Reads with
`core_p05_certification_lifecycle.md`.

## The two defects this slice fixes

1. **Declaration / absence-of-contradiction currently opens a governed capability.** Serving authorizes
   hierarchy transport and faced crossings from the *declaration* (or absence from a contradiction
   block-list), not from a positive certification. UNTESTABLE / unadjudicated / load-only capabilities
   serve.
2. **Re-attestation can mutate serving-effective state before new certification is coherent.** `reattest`
   clears `planner.blocked_edges` *before* re-adjudicating (`frameql.py:49` then `:50`); if adjudication
   raises (e.g. a face contradiction, which throws uncaught even under `degrade=True`), the live block-list
   stays cleared and previously-blocked edges resurrect into serving, while the manifold is left partially
   mutated.

Both violate one invariant: **serving state may contain only certifications successfully established for
the current governed state.**

## Governing corrections (prominent)

> **A declaration makes a capability eligible for certification. It does not make the capability
> executable.**

> **Re-attestation computes a complete replacement serving scope before altering the live scope.**

Corollary: **the allow-list is authority; the block-list is explanation.**

---

## Required target behavior (pin in tests)

| capability | verdict / state | serving |
|---|---|---|
| **face** | VERIFIED (touch) | usable |
| | CORROBORATED (assign/alloc) | usable |
| | CONTRADICTED | closed |
| | UNTESTABLE | closed |
| | no adjudication / license missing | closed |
| **hierarchy edge** | CORROBORATED | usable |
| | CONTRADICTED | closed |
| | UNTESTABLE | closed |
| | no adjudication | closed |
| **kernel op** (measure · member · anchor · universe · bare non-functional relationship · co-located attribute) | — | **servable without certification** (subject to existing laws) |

---

## Design

### 1. Positive admission in `PublishedScope`
Add positive capability sets (repo naming) to `PublishedScope` (`adjudication.py:355-370`):
```
certified_edges: frozenset[(frm, to)]     # only CORROBORATED functional edges
certified_faces: frozenset[<face-key>]    # touch→VERIFIED; assign/alloc→CORROBORATED
```
Only **VERIFIED / CORROBORATED** enter. UNTESTABLE, CONTRADICTED, no-verdict do **not**. **Absence means
closed.** Retain `blocked_edges` / `blocked_by` only for explanation/diagnostics — they no longer determine
usability. Populate in `scope_from_report` from the verdicts already in the report (`_hierarchies`,
`_faces`).

### 2. Store load establishes the initial positive scope
The shipped path (`store._load_one`, `store.py:149-159`) calls bare `adjudicate(server)` and never sets
`published_scope`. Route it through the **publish lifecycle** (or a shared install step) so a positive scope
is established before serving. **One definition of governed-serve-ready**: store load and
`ManifoldServer.publish()` must derive admission through **one adjudication → one scope derivation → one
install function**; witness publication (if the store must not do it) is factored out separately — but only
if tracing shows `publish()` cannot be reused cleanly. Invariant: **a governed Core runtime is not
serve-ready until its initial positive serving scope is established.** The direct Core API may still
construct before publish, but **transport/crossing capabilities remain closed** in that state.

### 3. Hierarchy addressability uses the certified graph
Path discovery traverses `declared functional edges ∩ certified_edges`, not all declared edges with a
post-hoc block. An uncertified edge **does not establish reachability** (`_check_addressable` /
`find_path` / `projection.py:130`). CORROBORATED participates; UNTESTABLE / CONTRADICTED / unadjudicated do
not. Declaration stays available for describe/EXPLAIN.

### 4. Faced crossings require positive admission
`parse_faced` still answers "which declaration does this name refer to?" — it must no longer implicitly mean
"usable." The planner requires **declaration exists AND face key ∈ certified_faces** before a faced
coordinate is addressable (`_check_addressable`, `planner.py:170-176`). The engine is not the primary
authorization boundary; a small defense-in-depth assert is acceptable, no duplicated policy.

### 5. Uncertified refusal reasons (no new mood)
Add distinct reasons `uncertified_edge` / `uncertified_face` → `(REFUSE, UNSUPPORTED)` in `REASON_OUTCOME`
(`disclosure.py:171-233`). Do **not** reuse `contradicted_edge` — contradiction is a stronger factual claim.
Planner chooses: `declared + contradicted → contradicted_edge`; `declared + untestable/unadjudicated →
uncertified_edge` (likewise faces if contradiction detail is exposed). Semantics: *uncertified* = "not
currently certified for governed use"; *contradicted* = "tested and refuted on the attested data."

### 6. Compute-then-swap re-attestation (+ explicit failure state)
Never clear live serving state before the replacement is ready:
```
old_scope stays live
  → compute complete new adjudication result
  → derive complete new PublishedScope locally
  → only on success: replace serving scope atomically (single assignment boundary)
```
Two failure cases:
- **A. Re-attestation completes coherently with negative/untestable verdicts** → the new scope simply
  excludes those capabilities; atomic swap revokes them.
- **B. Re-attestation crashes / cannot produce a coherent result** → do **not** build a half-new scope and
  do **not** partially revoke whichever capabilities happened to be processed. Transition to an **explicit
  whole-runtime fail-closed / serving-unavailable state** until a successful adjudication is re-established.
  A stale data-dependent certificate must never silently remain current after a failed refresh.

### 7. Faces need a degrade path
Under `degrade=True`, a face contradiction must become a **coherent adjudication result**, not an uncaught
exception (today `adjudication.py:645-656` has no `if not degrade` guard, unlike hierarchy). Record the
contradicted/uncertifiable face → **absent from `certified_faces`** → new scope swapped atomically. Retain
the contradiction for disclosure/diagnostics; do not make it disappear merely to avoid throwing.

### 8. First publish stays strict
Clean birth: adjudicate first; if required law is contradicted, **fail publish, install no serving scope.**
Do not weaken first-publish to make re-attestation degradable. (First birth: contradiction may prevent
publication. Existing runtime re-attested: a capability may degrade closed — provided the resulting scope is
coherent and explicit.)

### 9. Planner reads one scope object
Current mirroring (`PublishedScope → planner.blocked_edges/blocked_by`) creates two mutable
representations of one authority. Prefer the planner reading the current `PublishedScope` (or receiving one
immutable scope object). If clean, do it now; if it causes excessive churn, temporary mirroring of
`certified_edges` / `certified_faces` / `blocked_by` is acceptable **but installed in one assignment
boundary**, never individually around fallible work. No new independently-mutable mirrors without
acknowledging the debt.

### 10. The gate applies only to certification-dependent capabilities
No generic `if not published_scope: refuse every query` — that would wrongly close the kernel. Positive
gating applies to **hierarchy/functional transport** and **faced non-functional crossings** (and later
capabilities explicitly classified certification-dependent). It does **not** gate measure / member / anchor
/ universe / bare non-functional relationship / co-located attribute. An unadjudicated Core server still
performs kernel operations but cannot exercise a certification-dependent crossing. **Test this distinction
directly.**

### 11. Wire contract
Same wire structure, same four moods, new precise refusal reason(s). No new analytical mood, no general
certification object on the public wire. Verify the wire permits an extensible reason vocabulary (no
`contract_version` bump if reason values are already extensible and mood/shape semantics are unchanged) —
check tests/consumer assumptions before coding.

### 12. Tests
Flip the fixtures that currently prove `license=None AND crossing serves` (`test_relate_touch.py`,
`test_relate_triad.py`) to establish certification first — those demonstrate the defect, not desired
behavior. Add explicit invariant tests: face declared + license absent → REFUSE; hierarchy declared + no
corroboration → REFUSE; the full per-verdict target table; kernel op on an unadjudicated server → still
servable; reattest contradiction cannot leave a stale capability usable (defect 2).

---

## Bounded implementation scope (GO)

```
IN: positive PublishedScope admission · store load establishes initial scope · certified hierarchy path
    filtering · certified face admission · uncertified refusal reasons · face degrade behavior ·
    compute-then-swap reattestation (+ explicit failure state) · tests correcting the fail-open assumptions
OUT: P0.5b certificate fingerprint / realization binding · P0.5c shared face-law authoring · durable
     certification artifact · Core-P1 compiler · provisioning
```

**Implementation guard:** do **not** make this fix depend on the future stronger attestation identity
(P0.5b). Use today's adjudication identity/state to fix the serving polarity now; P0.5b strengthens what a
certificate is bound to.


---

# Closure record — Core-P0.5a CLOSED (2026-08-16)

Merged as `9bde8ea` (PR #174), base `e3460e8`, approved at `6d7a303`.

## The constitutional invariant, as ratified

> **Positive admission determines every hierarchy-derived analytical capability that can affect
> execution: whether the operation is addressable, the exact transport path that computes it, and the
> execution-relevant order axis. Declared-but-unadmitted structure may still contribute conservative
> diagnosis, but it may never create analytical permission.**

## The internal authority boundary

```
declared Manifold  +  PublishedScope
        -> Planner / PlannerView
        -> concrete admitted execution choices
        -> Engine
        -> execute exactly those choices
```

**No semantic re-inference below that boundary.** Division of labour (ruling 2026-08-11):

| Planner / PlannerView | Engine |
|---|---|
| determines whether an execution-relevant analytical choice is lawful | executes exactly the supplied choice |
| selects the admitted choice | refuses *structurally* if the required planned choice is absent |
| explains why no lawful choice exists | does **not** reconstruct analytical permission |

A failure to produce a valid analytical plan is a PLANNER diagnosis, not a low-level execution failure:
`Planner.plan_order_axis` therefore owns both "no lawful derivable order axis" and "ambiguous lawful
order axis". Moving that semantic diagnosis into the engine would partially recreate the authority
split this slice removed.

## What shipped

* **Positive admission representation** — `PublishedScope.certified_edges` / `certified_faces`. Edges
  admitted iff the governing HIERARCHY is CORROBORATED; faces iff VERIFIED (touch) or CORROBORATED
  (assign/alloc). The allow-list is authority; the block-list is explanation only.
* **One routing authority** — `PlannerView.find_path` selects over the certified DAG; `Planner._plan_route`
  records it; `ColumnEngine._planned_path` executes exactly it. **Zero `find_path` calls remain in
  `engine.py`**, and there is no `if no planned path: find_path(...)` fallback on any governed path.
  The planner also hands down the reduce-vs-attach partition (value-bearing) and the ASSIGN/ALLOC
  driver's route (a serving path invisible to the planner from outside).
* **Planner-owned order axis** — `PlannerView.orderable_levels()` over admitted edges only;
  `Planner.plan_order_axis()` decides or refuses; the engine consumes the concrete axis.
  `_TEMPORAL_LINEAGES` / `_orderable_levels` RETIRED. Explicit `by=` is the author naming an axis, not
  deriving one, and is unchanged.
* **Certification identity** — `EdgeKey(lineage, frm, to)` everywhere certified/blocked state is
  recorded, because a verdict is reached per LINEAGE. Physical identity deliberately excluded (P0.5b).
* **Compute-then-swap re-attestation** — one adjudication, one scope derivation, one atomic install,
  shared by publish / reattest / store load. Face contradictions degrade CLOSED like edges; any reattest
  exception installs an empty scope. A failed publish leaves nothing open (the probe window restores in
  `finally`).
* **No ungated-edge escape hatch** — every FunctionalEdge is certification-dependent. The hand-built
  benchmark manifold now declares the same hierarchies as its `.cml` twin and `fixture_server`
  publishes, so the fixture-backed suite exercises the production lifecycle instead of being exempt
  from the law it polices.
* **Two bounded refusal reasons** — `uncertified_edge`, `uncertified_face`, both (REFUSE, UNSUPPORTED).
  **No public wire shape change**: the scope's internal `EdgeKey` identity is projected back to the
  historical `[frm, to]` pair shape at the wire boundary.

## The refusal ladder (ratified semantics)

The invariant is NOT "refuse if any contradicted edge exists" — it is **never execute an edge that is
not positively admitted**. A certified alternate route therefore answers correctly:

```
certified route exists                      -> execute it, correct answer
none; declared route explicitly contradicted-> contradicted_edge
none; edge merely uncertified / untestable  -> uncertified_edge
no declared route at all                    -> out_of_universe
```

Preserve the distinction that governs which reason is named:

```
declared structure exists but is not positively admitted -> certification / admission refusal
no structurally relevant possibility exists              -> ordinary non-derivability / undefinedness
```

## Findings this slice produced (evidence the gate works)

1. A **false fertility fixture in our own suite**: `sum FERTILE { calendar }` declared on the *ratio*
   `aov`, refuted on the attested data with a concrete counterexample. Split into two pins rather than
   weakened — a surviving declaration perturbs no shipped number; a false one fails closed.
2. **GAP 2**, a wrong number: with two routes to a target, the certified path routed *around* a blocked
   edge while the engine took the blocked shortcut — serving an inflated total plus a phantom bucket
   where the base commit correctly refused. Introduced by the first P0.5a pass, caught by adversarial
   audit, fixed structurally.
3. **GAP 1**: the AT-metric bypassed the gate at the *asked* anchor, so the same transport served or
   refused depending only on which spelling the author chose.
4. **GAP 3**: `(frm, to)` keying let a CORROBORATED lineage license a co-located UNTESTABLE one.
5. The **order axis** could be made derivable by an uncertified hierarchy, turning "no lawful axis →
   refuse" into "exactly one → serve".
6. A **wheel-smoke path** that had been transporting on an unadjudicated edge (caught by CI, not the
   local suite — it runs standalone against the built wheel and is not collected by pytest).

## Testing doctrine established

**Pin the REASON for refusal, not merely that something refused.** In a fail-closed system a test that
asserts only "it refused" is weak evidence: another gate can make it green while the intended invariant
regresses. This is not theoretical — the first order-axis pins were anchored on a level that also
required transport, so they passed via `uncertified_edge` and would have stayed green with
`_orderable_levels` untouched. The pins now assert the refusal is about a missing CERTIFIED axis and
explicitly **not** `uncertified_edge`.

`tests/test_p05a_execution_contract.py` carries the contract. **0 P0.5a xfails** — the three discovery
xfails were converted to ordinary passing regressions, as required at final review.

## Verification at closure

```
base commit    e3460e8
approved head  6d7a303
merge commit   9bde8ea
suite          632 passed, 23 skipped, 0 xfailed (all three packages)
ruff F,E9      clean
CI             green on 6d7a303 (py3.10-3.13, wheel build + clean-venv smoke,
               demo wheel install ubuntu/windows, dependency cap + purged-grammar guards)
```

## A/B classification of remaining declared-structure reads

Every remaining direct `m.edges` read was classified; ambiguous ⇒ class A. **No remaining site can
create permission or affect a shipped number.** All are class B: `engine.py` `_attr_anchor` (narrowing
it to certified structure could only turn genuine ambiguity into a spurious unique answer);
`adjudication.py` edge selection for FD proofs (it is what MINTS certification); `parser.py` / `model.py`
well-formedness (authoring-time, emits error strings); `documents.py` MAP artifact (never serving);
`tools.py` describe/status wire (display).

## Deferred — exactly as ruled, not started

```
P0.5b       certification identity + realization/freshness binding
P0.5c       shared relationship-crossing law
follow-up   _probing concurrency (process-wide, shared; not exploitable in shipped serving today)
            engine-side face defence-in-depth (authority stays planner + PublishedScope, single check)
            certified_* public introspection (operators see what was refuted, not what is admitted)
            _attr_anchor conservative-diagnostic review, if later evidence shows it can create permission
```

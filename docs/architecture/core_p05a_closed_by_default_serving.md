# Core-P0.5a — Closed-by-default governed serving (design → implementation)

**Status:** design approved; implementation GO (bounded scope below).
**Date:** 2026-08-13
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

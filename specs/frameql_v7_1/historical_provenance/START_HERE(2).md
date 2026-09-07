# Columna Core / Platform Architecture — Transfer Package

Prepared: 14 August 2026

## Purpose

Continue the Columna Core / Columna Platform architecture and development mission in a fresh chat without restarting the architecture or losing the implementation history.

Read `CURRENT_STATUS_2026-08-14.md` immediately after this file.

## Collaboration model

The implementation partner is **andFam** (Claude Code / CC).

> **We decide what must remain true. CC decides the cleanest way to make it true.**

Give CC architectural invariants, semantic distinctions, scope, compatibility boundaries, and stop-gates. Do not over-specify routine engineering mechanics. If implementation evidence reveals a semantic/model gap, bring it back for a ruling rather than letting code invent theory.

## Core / Platform split

The split is architectural, not commercial.

**Columna Core**
> Compiles governed meaning into conventional execution infrastructure.

Core is open/self-service, includes Studio, manages multiple Manifolds, and may use multiple physical sources when they can be faithfully governed within one conventional execution environment. It does not promise Columna-owned composition across independent execution domains.

**Columna Platform**
> Preserves governed analytical identity independently of any one execution environment.

Platform is the future identity-centered runtime: canonical member identity, sufficient-state composition, anchor/universe identity, support/absence, freshness/provenance/certification, cross-domain alignment/reconciliation, identity-keyed materialization/cache, and governed composition across execution domains.

Permanent rule:

> **Two physical runtimes are acceptable. Two meanings of a measure are not.**

## Shared spine

```text
Theory / semantic kernel
        ↓
authored Manifold
        ↓
Manifold lifecycle / registry
        ↓
Studio
        ↓
Frame-QL planning / adjudication
        ↓
governed serving / wire
        ↓
MCP / API / UI / agents
        |
execution-provider seam
   _____|_____
  |           |
Core       Platform
```

## Manifold blast wall

The authored Manifold is logical-only. Physical database/table/column realization belongs in a separate private mapping.

> **Meaning must exist before realization. Mapping realizes meaning; it does not create it.**

> **Lowering may reduce coverage. It must never reduce law.**

The compiler/lowering boundary is the only place allowed to combine governed logical publication and private realization.

Current `.cml` is a **Core-private execution image**, not the authored ontology and not the future Platform format.

## Governed publication / Core compiler

Conceptually:

```text
compile(governed_publication, private_core_mapping)
    → CoreExecutionImage
```

The private mapping must bind the exact immutable publication ref.

Compiler authority inputs should not include Studio session state, evidence/profile scratch state, old `manifold.columna.yaml`, draft `.cml`, or physical naming conventions.

Important mapping rulings:
- root evaluator ≠ default reducer;
- every anchor component needs explicit physical key realization;
- universe restriction refs resolve compositionally through coordinate/attribute realization;
- relationship join facts are physical mapping; functionality is logical law;
- hierarchy realization uses explicit adjacent logical edges;
- cross-table routes must be typed/governed, not generic arbitrary paths;
- attributes are physical endpoints attached to logical parent coordinates;
- cross-table attributes require governed routes;
- unsupported holistic/sketch reducers refuse rather than approximate silently;
- crosswalk remains deferred until authored meaning is sufficient.

## Certification lifecycle

A major architectural discovery:

**immutable publication law ≠ realization/data-bound certification ≠ runtime serving admission**

Desired lifecycle:

```text
publication + mapping
      ↓
compile CLOSED Core image
      ↓
adjudicate against realization/data
      ↓
certification / PublishedScope
      ↓
serve only positively admitted capability
```

Universe ratification is logical-law authority. Hierarchy functionality and ASSIGN/ALLOC face validity may depend on physical realization/data/freshness.

## Closed-by-default serving

Constitutional rule:

> **Declared structure may be used conservatively to discover hazards. Positive certification is required to authorize execution.**

P0.5a replaced negative block-list authorization with positive `PublishedScope` admission.

Hierarchy:
- CORROBORATED → admitted
- UNTESTABLE / CONTRADICTED / none → closed

Faces:
- VERIFIED touch → admitted
- CORROBORATED assign/alloc → admitted
- contradiction / none → closed

Reattestation is compute-then-swap; stale capability must not silently survive failed/incoherent reattestation.

## Planner / engine authority boundary

Latest accepted invariant:

> **Positive admission determines addressability, the exact transport that computes the answer, and the order axis that walks it.**

Planner / PlannerView:
- determines lawful execution-relevant choices;
- selects exact admitted route;
- selects exact admitted order axis;
- owns the semantic refusal when no valid plan exists.

Engine:
- executes exactly what it is handed;
- does not rediscover routes;
- does not infer hierarchy-derived order;
- has no permissive fallback.

General audit rule:

> A direct declared-graph read that can enable execution or change a number is certification-sensitive. Declared structure may still be used conservatively if it can only add ambiguity, caution, or refusal.

## P0.5 sequence

```text
P0.5a  closed-by-default serving
P0.5b  certification identity + realization/freshness binding
P0.5c  shared relationship-crossing law
```

At handoff, P0.5a PR #174 at head `6d7a303` had been **approved for merge**, but the prior chat had not yet received andFam's merge-confirmation reply. Establish the actual merge state before authorizing new work.

Do not begin P0.5b until that is confirmed.

## P0.5b target

Certification identity will likely need to bind:
- publication_ref;
- realization identity;
- subject;
- claim;
- verdict;
- data attestation;
- established_at.

Exact artifact is not frozen. `(frm,to)` alone is not sufficient certified edge identity. Freshness matters for data-bound claims. Touch/symbolic proofs may be timeless exceptions.

## P0.5c target

Shared authored relationship law is still too weak to express Core `FACES` semantics runtime-independently.

Do not copy Core `FACES` syntax wholesale into shared authoring. First classify which fields are actual analytical law versus disclosure/prose/serialization mechanics, then define the smallest shared crossing law.

## Core-P1

Core compiler contract:

```text
governed publication
       +
private mapping
       ↓
Core compiler
       ↓
Core execution image
```

Compiler refusal classes conceptualized as:
- InputIdentityMismatch
- LogicalMeaningMissing
- MappingIncomplete
- UnsupportedCoreCapability
- ExecutionRepresentationGap

Certification failure is a distinct lifecycle state, not merely a compile failure.

An authority-independent Core-P1 kernel may proceed where it does not depend on P0.5b/c.

## Internal compute substrate

Keep separate:
1. source backend;
2. internal compute substrate;
3. future Platform identity runtime.

Current broad picture:
- DuckDB connector/source boundary;
- Polars internal compute;
- no Platform identity runtime yet.

Possible Polars → DuckDB migration is an internal compute-substrate change.

> **The substrate performs computation. It does not decide what computation means.**

Parity must compare governed behavior, not just raw numbers.

## Long-range Platform vision

The old AtomDB documents use pre-current terminology. Read them as architectural source documents.

Durable progression:

```text
1 COMPILER
  governed meaning over conventional storage/execution

2 FORMAT / IDENTITY
  governed member identity/state/support/contracts meaningful at rest and across engines

3 CUSTODY
  governed operations own the write path
```

Long-range rule:

> **Own identity semantics; delegate mechanical computation.**

## First action in the new chat

1. Read `CURRENT_STATUS_2026-08-14.md`.
2. Establish whether PR #174 actually merged.
3. If merged, mark P0.5a closed.
4. Decide the next authorized unit explicitly.
5. Do not silently jump into P0.5b, P0.5c, Core-P1, or Platform work without reconciling the gate sequence.

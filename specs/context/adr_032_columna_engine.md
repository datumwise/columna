# ADR-032: The Columna Engine — the runtime unit, the two-level contract, and the execution axes

**Status:** Proposed (captured from design session; builds on ADR-031, refining its D11–D12)
**Date:** June 2026
**Track:** Architecture / runtime. ADR-031 fixed the *foundation* (column-atoms, transport, the two-projection spec, layered emission). This ADR names the *runtime as a unit*, consolidates all analytical *judgment* in the planner via a two-level contract, and records the physical-execution axes, the server topology, and the surface set. It is additive to ADR-031's object model; where it touches D11–D12 it sharpens rather than reverses them.

---

## Context — what this ADR records

Three things were under-specified after ADR-031 and surfaced in design and in reconciliation against the shipped manuals and Core code:

1. The runtime had no *name* as a whole. "Planner" and "column engine" named its halves, but an earlier diagram labelled the *logical* half "Columna engine" — one underscore from `ColumnEngine`, the physical executor. The manuals, code, and diagrams had drifted apart on this.
2. ADR-031's layered emission (D12) placed *refusal sites* in both the planner and the engine. In practice that lets the physical executor render an analytical verdict — the judgment the engine is least equipped to own and most likely to leak across columns.
3. One manual (framework 6e, Ch 2) attributed the **push-down decision to the planner**, contradicting the cost-blind-planner stance of the object model. Push-down is mechanics; the planner is meaning.

This ADR resolves all three, and records the execution axes, topology, and surfaces settled alongside them.

---

## The Columna Engine — the runtime as a unit (D1)

The runtime is one named thing: the **Columna Engine** = **Frame-QL API + planner + column engine + caching engine**. *Columna* is the framework — everything: object model, Frame-QL, authoring, the determinacy doctrine. The *Columna Engine* is its runtime: the unit you embed and call, the thing that takes a Manifold plus a Frame-QL query and returns a correctness-governed answer over any backend.

- The **Frame-QL API** is its contract face — the four outcomes are the wire protocol, not a presentation layer bolted on above it (D3/D4).
- The **planner** is its logical half; the **column engine** its physical half (D2).
- A Columna Engine instance is roughly what `ManifoldServer(manifold, connector)` instantiates per Manifold.

**Why containment, not a rename.** "Columna Engine" and "column engine" sit one underscore apart. The resolution is *structural*: the column engine is **nested inside** the Columna Engine, so the two read as parent and component, never as confusable siblings. This retires the stray "Columna engine = the planner" label — the logical half is the *planner*, full stop — and it makes the user-level statement "clarify/refuse is the Columna Engine's response" exactly true at the **unit** level, while "the planner decides" is exactly true at the **component** level. They were never in conflict; they describe different scopes.

---

## The planner / column-engine boundary, sharpened (D2)

ADR-031 D11 made the planner *provenance*-blind. This ADR adds the symmetric half: **the planner is *cost*-blind too.** It reasons about *meaning* — determinacy, hazards, the plan — and is denied both the provenance and the cost of physical realizations. The **column engine** reasons about *mechanics* and is bound by one standing rule: reproduce the planner's per-column result and contract exactly.

**Push-down is the column engine's decision, below the plan line (corrects framework 6e Ch 2).** Deciding *whether and how* to push a reduction into the backend is mechanics, and mechanics are cost-aware — the planner is cost-blind, so it cannot be the one choosing. The split:

- the **planner** validates that a reduction is *correct* (semantics, above the line) and emits it as part of the plan; and
- the **column engine** decides whether to push that validated reduction down, pushing only when the backend's semantics provably match the plan (NULL-in-aggregate, float aggregation order, distinct-count semantics, collation), and pulling-and-computing-in-engine otherwise.

So generated SQL may aggregate — but only a fragment of a plan the planner already owns and verified. The hard floor from ADR-031 D1 stands: the backend *delivers* columns, never *combines* them.

---

## The two-level correctness contract (D3, D4) — refines ADR-031 D12

This is the load-bearing change. It keeps the analytical judgment in **exactly one place**.

**The column engine never judges (D3).** It only *attempts*, returning one of two things: a **result**, or **no result with the reasons in the disclosure**. "Clarify" and "refuse" are not in its vocabulary. Two no-result situations arise — a request *ambiguous under the Manifold's own rules* (no unique answer follows and the engine will not choose one for the user, e.g. a missingness / M-anchor case), and a request the *data cannot support at all* — and both return identically: empty result plus full disclosure. So the planner can classify them mechanically rather than by guesswork, the disclosure carries a **discriminator**: *ambiguous — no unique answer under the rules* versus *unsupported — no data*. That discriminator is the seam the whole contract rests on.

**The planner owns the four outcomes (D4).** serve · disclose · clarify · refuse are the wire response kinds, emitted only by the planner, reached two ways:

- *statically*, from structure it can see before execution; and
- *dynamically*, by reading the engine's no-result disclosure and mapping it — ambiguous → clarify, unsupported → refuse.

**How this refines ADR-031 D12.** D12 was right that *evidence* is layered by epistemics — the engine still originates the resolution/coverage caveats it alone can see, and now also the discriminator. What changes is that the **verdict** is consolidated: D12's "engine-side refusal sites" are removed. The engine reports; the planner decides. This is strictly stronger on D12's own principle — a layer should emit only what its projection lets it *see*, and a verdict is not something the physical executor is positioned to *own*; only evidence is.

**Static clarify cases:** fan-out (M:N with no functional path, ADR-031 D10); the **address fork** (a roll-up DAG that forks — calendar vs fiscal — unqualified, resolvable by `@cal.` / `@fisc.`); the **population fork** (`ON UNIVERSE`, ADR-031 D13); and **co-anchoring** (D5). **Refuse cases:** no-data; out-of-universe (ADR-031 D7); and contradicted-edge (a declared functional edge the data violates) — the last promoted from the engine's no-result disclosure.

---

## Co-anchoring — the ratio / rate clarify (D5)

A ratio or rate is a **binary derived column `N op D`**, and its determinacy is a **co-anchoring requirement on the two operand measures**, not a special metric type. Division — like any binary map — combines its operands cell-by-cell only when they are aligned on **one shared frame**: a common where-anchor *and* a common over-what population. From that, three cases:

- N and D already co-anchor, or a unique co-anchoring is implied by the query's `@anchor` and a shared population → **serve** (disclosing any non-trivial bring);
- several legitimate co-anchorings exist — multiple shared grains, or numerator/denominator populations reconcilable more than one way (revenue-per-active-customer: per month? per customer-month? over active-in-month vs ever-active?) → **clarify**, naming the candidate frames, choosing none;
- no shared frame exists at all (disjoint universes, no shared base lineage) → **refuse** (inexpressible).

It is primarily a *static* planner check on declared anchors and universes (like fan-out); where the incompatibility shows only at resolution (population coverage doesn't reconcile), the engine returns no-result + disclosure and the planner classifies it as clarify — the two-level contract (D3/D4) doing its job. It is **not eager**: a ratio at a clear anchor over one population just serves. And it is **distinct from avg-of-averages**, which is the B-anchor / reaggregability hazard (ADR-031 D5), not a co-anchoring one — the two must not be conflated.

---

## The column engine's two physical axes (D6)

Both are physical-execution choices the column engine owns, both Core-simple with an additive Pro extension, both invariant to the answer:

- **Strategy: in-memory · push-down.** In-memory compute runs in both tiers; push-down is added in Pro and governed by D2. The execution base in both tiers is the column engine plus the caching engine; push-down is additive on top.
- **Mode: single-column · multi-column.** Core is **single-column**: each measure column resolves through its own pipeline (operator → reaggregability / B-anchor check → witness → disclosure, yielding a result or a no-result), so a wide result is an assembly of independent single-column resolutions — simple, low-footprint, auditable per number. **Multi-column** (one shared scan and join across several columns) is **open for Pro**; its gate is not raw speed but **per-column disclosure separability** — a hazard attached to one measure must not bleed onto another in a shared computation. Deferrable indefinitely without touching anything above the plan line.

---

## Server topology (D7)

- **Core: multiple single-Manifold servers.** Each `ManifoldServer` hosts one Manifold — isolated, nimble, self-hosted (single process acceptable): a Columna Engine per Manifold.
- **Pro: multi-Manifold servers.** A router over a catalog of Manifolds, shared infrastructure, governed. The shared cache must key by Manifold-id-plus-version so a witness from one world is never served into another.

Co-location is the standing hazard — co-hosted Manifolds, co-cached witnesses, co-computed columns — and each must keep its boundaries explicit.

---

## Surfaces — three, one contract, the NL agent as MCP client (D8)

Three surfaces ship in both tiers — they are the identity, not a tier differentiator — all over the one Frame-QL API: the **Frame-QL UI** (direct interactive querying), **MCP** (Frame-QL exposed as tools to any external agent), and the **NL agent** (Columna's own natural-language front door). Because they share the API, they share the contract.

**The NL agent is itself an MCP client.** It routes through the public MCP surface, not a private back channel — Columna's own best MCP client. This is a forcing function: anything the dialogue surface needs, the public API is obliged to express, so the privileged path can never outrun the public one.

**Build status.** Only the programmatic Frame-QL surface ships today (`ManifoldServer` plus the `Frame` fluent builder). The UI, MCP, and NL agent are roadmap, designed to inherit the four outcomes unchanged.

---

## Decisions (index)

- **D1** The runtime is one named unit, the **Columna Engine** = Frame-QL API + planner + column engine + caching; *Columna* is the framework above it; the column engine nests *inside* the Columna Engine, resolving the name collision by containment. ≈ `ManifoldServer` per Manifold.
- **D2** The planner is **cost-blind** as well as provenance-blind (extends ADR-031 D11); **push-down is the column engine's decision** below the plan line, over a reduction the planner validated above it (corrects framework manual 6e Ch 2).
- **D3** The column engine **never judges**: it attempts and returns *result* or *no-result + disclosure*; the disclosure carries an **ambiguous-vs-unsupported discriminator**.
- **D4** The **planner owns the four outcomes** (serve / disclose / clarify / refuse), reached statically or by classifying the engine's no-result disclosure. **Refines ADR-031 D12:** evidence stays layered by epistemics, but the *verdict* consolidates in the planner; the engine emits no refusals.
- **D5** A ratio/rate is a binary `N op D` governed by a **co-anchoring** requirement: serve when operands share one frame, **clarify** when several legitimate co-anchorings exist, refuse when none does. Static where declared, dynamic via disclosure otherwise; not eager; distinct from avg-of-averages (ADR-031 D5).
- **D6** Two column-engine physical axes — **strategy** (in-memory both · push-down Pro) and **mode** (single-column Core · multi-column open for Pro, gated on per-column disclosure separability). Both invariant to the answer.
- **D7** **Server topology:** Core = multiple single-Manifold servers; Pro = multi-Manifold router with a version-scoped shared cache.
- **D8** **Three surfaces** in both tiers over one Frame-QL API; the **NL agent is an MCP client** (forcing function). Only the programmatic Frame-QL surface ships today.

---

## Open questions / next steps

1. **Code migration (the immediate next pass).** *Done in v0.7.8-core (closed by ADR-033 D4; audit finding B2).* Shipped Core (v0.7.3) still raised a single `Refusal` for *both* clarify and refuse, and the column engine raised it directly in two paths — the multi-grain `_attr_anchor` case and the contradicted-edge path. Making D3/D4 real required: (a) moving those refusals *out* of the engine into a no-result + disclosure handed up; (b) adding the ambiguous-vs-unsupported discriminator to the disclosure; (c) making clarify a structured *result* (carrying its alternatives) rather than an exception, so an MCP agent receives it as an actionable signal; (d) separating the four outcomes into distinct wire kinds. All four are now shipped: clarify travels as a structured `Outcome` value carrying its alternatives, the ambiguous/unsupported discriminator exists, kind classification happens only at the planner's chokepoint, and the four outcomes are distinct wire kinds.
2. **Co-anchoring detection (D5).** *Implemented in v0.7.5-core.* The planner statically checks
   a ratio's operand universes (via `_atoms` on each side of a `/` node) and raises
   `co_anchor_ambiguous` (discriminator `ambiguous` → clarify) when they span more than one
   universe, naming the candidate populations; same-universe ratios and constant denominators
   serve, and the check is scoped to the ratio (separate columns over two universes still serve
   with the multi-universe coverage caveat). `coanchor_demo` covers it. The population pin
   `ON UNIVERSE` was wired in *v0.7.7-core* (**Option A**): it is threaded to the planner and
   asserts the frame's intended population, so a measure bound to the pinned universe serves and a
   measure bound to a different one is out-of-universe for that population and refuses — resolving
   the co-anchoring clarify to a serve (when the operands share the pinned population) or an honest
   refuse (when they don't). *Remaining (Option B):* resolving a measure over a universe *other*
   than its declared one — true cross-universe confinement, with the resolution-time coverage
   disclosure of ADR-031 D13 — which is what would let `revenue / level.last` actually *serve* a
   rate over a chosen shared sub-population. Deliberately not half-wired, since suppressing the
   clarify without taking the rate over the chosen population would be a silent failure.
3. **Multi-column (D6).** Deferred by design; the gate is disclosure separability, not speed.
4. **Cache witness-freshness.** The result cache is already version-scoped (`CacheEntry.version`); what is open is witness invalidation against underlying-data freshness, and cross-scope cache keying in Pro (carried from the architecture brief §9).

---

## Consequences

The analytical judgment now lives in exactly one component — reachable two ways, emitted from one place. That is what makes "the same question returns the same answer, or the same honest non-answer, on every surface and in both tiers" a *structural* fact rather than a discipline. The naming is closed end to end: code (`Planner` / `ColumnEngine` / `ManifoldServer`), manuals, both diagrams, and the architecture brief now agree.

The cost is the migration in open-question 1: until it lands, the contract is documented but not yet enforced in code, and clarify still travels as an exception sharing a class with refuse. The benefit, once it lands, is that the physical executor becomes *incapable* of rendering an analytical verdict — the strongest available form of "no silent wrong number," because the layer that could be wrong about meaning is structurally not permitted to speak it.

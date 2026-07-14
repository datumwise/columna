# ADR-033: Vocabulary reconciliation — the canonical register, the scheduled rename, and the map-arithmetic authority

**Status:** Ratified (Huayin, 2026-07-14; drafted by the design session from Huayin's Fork 1 ruling)
**Date:** July 2026
**Track:** Architecture / vocabulary. The architecture-to-code audit (v0.2, 2026-07-13) found the stack "one ADR-cycle out of sync with itself": the ratified execution-positions capture (v0.7, now v0.8) names the runtime's physical members **Combiner** and **Cache(r)** under the umbrella **Metric Engine**, while ADR-031/032 and the code use **planner / column engine / caching engine**, with `Planner` and `ColumnEngine` as the classes. This ADR records the ruling that closes the fork — through the ADR series, not around it.

---

## Context — what this ADR resolves

Audit Fork 1 asked two things: (a) which register is canonical and receives the concordance entry; (b) the one true *locational* disagreement — post-aggregation map arithmetic, which the capture assigns to the Combiner while the shipped code and the Frame-QL manual place its evaluation planner-side. Framing facts: the vocabularies are reconcilable by declaration (the audit's own v0.2 correction); `Planner` is uncontested in every document; the role register is already public (`/notes/cacher`, the Ladder) and load-bearing in capture v0.8's seven fresh rulings; and external adoption is zero, making this the last cheap moment to converge.

## D1 — The canonical register (RULED: the capture leads)

The role names are canonical: **Combiner**, **Cache(r)**, **Metric Engine**; **Planner** continues unchanged. The registers compose rather than compete, by containment — the same move ADR-032 D1 used for Columna Engine / column engine:

| Canonical (doctrine, docs, describe surfaces, site) | ADR-031/032 term | Code today |
|---|---|---|
| **Planner** (judgment) | planner | `Planner` |
| **Combiner** (execution of combination; disclosure-bearing) | column engine (the non-cache part) | *(inside `ColumnEngine`)* |
| **Cache(r)** (sound aggregate navigation) | caching engine | *(the cache dict inside `ColumnEngine`; design-stage as a component)* |
| **Metric Engine = Combiner + Cache(r)** | column engine + caching engine | `ColumnEngine` — the Metric Engine in its pre-factoring form |
| **Columna Engine** (the runtime unit; unchanged from ADR-032 D1) | Frame-QL API + planner + column engine + caching engine | ≈ `ManifoldServer(manifold, connector)` |

Reading: the **Columna Engine** contains the **Planner** and the **Metric Engine**; the Metric Engine's members are the **Combiner** and the **Cache(r)**. The Frame-QL manual's existing "metric engine" usage ("answers each atom from its cache or... by issuing the few specific calls the backend exposes") is thereby exact. The reference manual's Appendix B receives the concordance entry (Appendix A of this ADR); the manuals' historical terms remain readable through it.

## D2 — The rename: scheduled, once, at the factoring moment (RULED)

`ColumnEngine` is not misnamed so much as pre-factored: it is the Metric Engine while the Cache(r) remains an embedded dict. Accordingly:
- **No interim rename.** Renaming now would create the third vocabulary the audit warned against and churn code that WP-B is actively touching.
- **One rename, ever:** when the Cache(r) is purpose-built and factored out (its own WP, post-WP-B, per the standing sequencing), the factoring commit splits `ColumnEngine` into `Combiner` and the Cacher component and retires the old class name — the rename is a side effect of the factoring, not a project of its own.
- Until then, code comments and docstrings may state the identity ("`ColumnEngine` — the Metric Engine, pre-factoring: Combiner + embedded cache; ADR-033") wherever it aids a reader; no signatures change.

## D3 — Map-arithmetic: authority vs. address (RULED)

Post-aggregation map arithmetic (the two-projection arithmetic; where ratios are born) is **Combiner work doctrinally**: it is execution, it is disclosure-bearing, the backend must never perform it, and any certified Combiner port must cover it — the algebra parity suite is end-to-end, so port certification is unaffected by where the reference implementation hosts the step. That the `Planner` class currently evaluates these maps is an **implementation address, not a doctrinal assignment**: Grammar Layer and Combiner are ratified as inseparable ("the bundle IS Columna"), so the seam that is doctrine is the backend/Columna boundary — fixed — while the seam between two classes inside the bundle is engineering. The capture's assignment stands; the Frame-QL manual's sentence stands as a description of mechanics; the code moves nothing now. Whether map evaluation physically relocates into the Combiner class is a named checkpoint fork of the factoring WP (D2), decided there.

## D4 — ADR-032 open-questions closeout

ADR-032 "Open questions / next steps" item 1 (the D3/D4 code migration) is **done** as of core 0.7.8: clarify travels as a structured `Outcome` value carrying its alternatives, the ambiguous/unsupported discriminator exists, kind classification happens only at the planner's chokepoint, and the four outcomes are distinct wire kinds. ADR-032 is updated in the same PR as this ADR to mark item 1 closed with the version pin. (Audit finding B2; this was the stale-documentation half of the "one cycle out of sync" diagnosis.)

## Consequences

- Explorer tier-2 describe schemas, /stack, the enterprise plan, and all new public copy use the canonical register; the concordance carries readers of the older documents.
- Audit Fork 1: CLOSED by this ADR. The reconciliation sequence's item 1 is discharged; internal renames (audit sequence item 3) remain limited to the optional Operator Registry docstring alignment.
- The exception protocol of the terminology discipline holds: no new runtime nouns may be introduced outside a ratified capture plus a concordance entry.

---

## Appendix A — the concordance entry (for reference manual Appendix B, format-matched to its existing entries)

> **Metric Engine** (execution-positions capture, ratified 2026-07-12/14) — the runtime's
> physical pair: the **Combiner** (execution of combination: cross-column operations,
> transport, final reductions, post-aggregation map arithmetic, the disclosure-bearing
> steps) and the **Cache(r)** (sound aggregate navigation; admission law: only the fertile
> is cached). Equivalent to this manual's "column engine + caching engine" (ADR-032 D1) and,
> in shipped code prior to the Cacher factoring, to the `ColumnEngine` class. Contained,
> with the Planner and the Frame-QL API, in the **Columna Engine** — the runtime unit.
> Post-aggregation map arithmetic is Combiner work by authority regardless of the class
> that hosts its evaluation (ADR-033 D3). This manual's existing uses of "metric engine"
> (Frame-QL v1 Ch. 2; reference 5e) are exact under this entry.

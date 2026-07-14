# ADR-034: The definition-language scope — Chapter 26 partitioned by Certificate customer

**Status:** Ratified (Huayin, 2026-07-14; drafted by the design session from Huayin's Fork 5 ruling)
**Date:** July 2026
**Track:** Architecture / authoring language. The audit (v0.2, Section E) found that half to two-thirds of the reference manual's Chapter-26 definition language has no shipped keyword, and asked (Fork 5) whether that is unshipped Core work or documentation of Pro/future scope. This ADR records the ruling: neither wholesale — the constructs partition by what makes each one real, and the shipped Certificate kernel (WP-B: `License`, the four verdicts, publish-time adjudication, fail-closed CONTRADICTED) is the partitioning instrument.

---

## Context

WP-B changed the fork's economics: the integrity layer's *design* question is answered — declared precondition → adjudication → VERIFIED / CORROBORATED / CONTRADICTED / UNTESTABLE, with fertility as the first customer. What remains is scheduling: which declared constructs become the kernel's next customers, and on what demand. The standing sequencing principle ("operators demand-driven") generalizes: **constructs are demand-driven**, and the ruled on-ramp + Explorer motion is the demand.

## D1 — Core, scheduled into the on-ramp WP: `ASSERT`, `HIERARCHY` verification, `UNIVERSE ... BASIS`

The on-ramp's ruled promise — `columna init` drafting an *evidence-graded* Manifold — is empty without adjudication: a drafted `HIERARCHY store -> region` carrying INFERRED_SAMPLE means something only if publish-time machinery can refutation-test it against the data and stamp CORROBORATED or CONTRADICTED. These three construct families are therefore Core, and they are built **inside the on-ramp WP**, as the Certificate kernel's second, third, and fourth customers — the same pipeline fertility runs (declared → math-verify where provable, else data-refute → verdict; CONTRADICTED fails closed at publish). No standalone integrity-layer build exists; the work rides the motion already ruled next, so demand and construction arrive together.

## D2 — Core, small, same motion: `ALIAS`

"One anchored measure can wear a hundred names" is the metadata-independence essay's load-bearing promise — the *meaning goes free* half — and it currently has no syntax. `ALIAS` is communicative metadata by definition (no legality impact), cheap to parse, and visible only where names render: the Explorer. It ships in the on-ramp + Explorer WP or the promise remains prose.

## D3 — Pro/future, scoping note: `WITHHOLD` / `ACCESS`

Access governance is enterprise-shaped and requires an authentication model Core deliberately lacks. The manuals receive a scoping note; no Core keyword is scheduled.

## D4 — Future, scoping note: `INHERITS ... VERSION`

Manifold composition/inheritance is the layered-cache era's problem (execution-positions capture, "the layered Cache(r)"). Building inheritance before any installation holds two Manifolds is speculation. Scoping note; revisit when the layered-cache WP is cut.

## D5 — The manuals status pass (the one-day instrument, either way the code goes)

Every Chapter-26 construct is tagged in the manuals as **shipped** (with version), **scheduled** (with its WP, per D1–D2), or **roadmap** (per D3–D4) — the Ladder's honest-hatching idiom applied to the reference documentation, so no reader mistakes documentation for a shipped guarantee. Worksheet: `manuals_alignment_pass_v0_1.md` (companion to this ADR). The manuals are not in-repo; the pass routes through their own process.

## Consequences

- Audit Fork 5: CLOSED. Audit WP-G resolves as: no standalone build; D1–D2 items enter the on-ramp + Explorer WP's scope; D3–D4 are scoping notes in the status pass.
- The Certificate kernel's generality claim gains its test: three new customers must reuse `License` and the adjudication path unchanged. If any needs a schema change, that change is a checkpoint fork of the on-ramp WP, not a silent extension.
- The evidence grades already in `model.py` (DECLARED / PROVEN / INFERRED_*) connect to the verdict machinery through these customers — the grade is the declaration's provenance; the verdict is its adjudicated status. The on-ramp WP records the mapping explicitly.

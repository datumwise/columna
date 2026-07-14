# ADR-035: The query surface — the envelope grammar is the canonical lineage

**Status:** Ratified (Huayin, 2026-07-14; drafted by the design session from Huayin's Fork 6 ruling)
**Date:** July 2026
**Track:** Architecture / query language. Frame-QL manual v1, Chapter 2, defines a canonical form (`operator(col₁ @ a₁, ...) AT A` inside `FROM <manifold> SELECT ... AT {levels}`) for which no parser exists anywhere in the repo; every Chapter-6 worked example fails against the shipped envelope grammar (`columna-server/frameql.py::parse_frameql` — `columns @ anchor`, docstring-labeled interim). The audit (Fork 6) asked: implement the manual, or rewrite it? This ADR records the ruling: rewrite — the shipped grammar is not the interim form of the manual's design; it is the canonical **lineage**, and the manual described a prophecy made about the pre-ADR-031 machine.

---

## Context

The manual's own watermark is the tell: "a renamed, lightly-revised continuation of the Coframe-QL Manual, Third Edition" — its canonical form was inherited essentially intact from the kernel era whose *structure* ADR-031 replaced. Meanwhile the envelope grammar has been absorbing the old form's genuinely valuable content organically, each piece pulled in by a ruled need with doctrine and tests attached at entry: `ON UNIVERSE` (population pins, v0.7.7), the derived-metric label form, and — decisively — the per-subexpression inner anchor (`avg(aov@day) @ month`, WP-B.1). The single load-bearing idea in Chapter 2 — parts of an expression binding at their own anchors — is arriving through rulings, which is the correct way for a query surface to grow.

## D1 — The envelope grammar is the canonical lineage (RULED)

The shipped grammar is the query surface. It is *canonical as a lineage, not frozen as a snapshot*: it grows by ruling — every extension enters through a capture or checkpoint with its legality doctrine and tests, never by implementing the old form's remaining features on the old form's authority. The Coframe canonical form confers no backlog.

## D2 — `FROM` / `SELECT`: never adopted (RULED)

The clause ceremony imports container-speak into a column-native language. `columns @ anchor` is the voice; the Manifold is addressed out-of-band (the tool/API parameter), not re-declared per query. Curly-brace anchor sets and the remaining Chapter-2 ceremony carry no ruled need; if one ever arises, it enters through D1's rule like everything else.

## D3 — Parser promotion (the code work; small, precedes the on-ramp WP)

`parse_frameql` is promoted from `columna-server` into `columna-core`, discharging its own docstring's standing v0.8 item. Scope: move, don't change — the grammar is untouched in the promotion WP; the server keeps a thin re-export shim; the parser's tests move with it and join the core check discipline. Rationale for now: Explorer tier 2 and the on-ramp both build against the query surface; it should live under core's test regime before they do.

## D4 — The manual rewrite (routes through the manuals' process)

Frame-QL manual Chapter 2 is rewritten to the shipped grammar; Chapter 6's worked examples are regenerated **by running them** against the shipped package — the site's build-time integrity rule extended to the manual ("the manual is structurally incapable of documenting a query it did not run"). The Coframe-QL canonical form moves to a historical appendix, labeled as lineage — completing the watermark's honesty rather than erasing it. Worksheet: `manuals_alignment_pass_v0_1.md` (shared with ADR-034).

## Consequences

- Audit Fork 6: CLOSED. The audit's "doc examples that do not run" finding resolves by D4's regeneration rule, permanently — a manual example that stops parsing fails the manual's build.
- The grammar's growth log so far, recorded as precedent for D1: `ON UNIVERSE` (population pin) · label form (`name: expr`) · dotted member access · inner `@` (pinned inline reduction, WP-B.1) · the `input_anchor_ambiguous` clarify for the unpinned case. Each entered with a ruling; that is the pattern future extensions must match.
- One communicative-layer note, ledgered with this ADR: the demo site's governed `wire_strings.json` has no friendly string for `input_anchor_ambiguous` yet; nothing surfaces it today, but the Explorer tier-2 / on-ramp WP inherits a wire-strings coverage check (every reason and code in the shipped vocabulary has a friendly string before any surface can emit it).

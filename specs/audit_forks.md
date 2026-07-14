# Audit forks — the architecture-to-code audit (v0.2) fork registry, in-repo mirror

The **authoritative registry is the architecture-to-code audit v0.2 (2026-07-13), which is NOT
in-repo** (verified: `specs/` and `specs/reference/` hold no audit doc). This file is a durable
in-repo *mirror* of the audit forks that in-repo instruments (ADRs / WPs) resolve — so a fork's
closure lives in a ledger, not only in an ADR's prose. Forks the audit tracks that have **no in-repo
resolution instrument yet are deliberately NOT listed here** (their content lives in the audit; this
mirror does not reconstruct it from memory). A row is struck when its closing instrument merges,
citing it.

| Audit fork | subject | closing instrument | status |
|---|---|---|---|
| ~~Fork 1~~ | Vocabulary reconciliation: canonical register + the map-arithmetic authority/address seam | [ADR-033](context/adr_033_vocabulary_reconciliation.md) (merged, PR #17) | ~~**CLOSED**~~ |
| ~~Fork 3~~ | Derivation denotation + fertility (declared, adjudicated, closed by default) | WP-B (merged, PR #16) + WP-B.1 (PR #18); brief `wp_b_fertility_brief_v0_1.md` | ~~**CLOSED**~~ |
| ~~Fork 5~~ | Definition-language scope: which Chapter-26 constructs are Core vs Pro/future | [ADR-034](context/adr_034_definition_language_scope.md) — partitions by Certificate customer; D1/D2 → on-ramp WP scope stub; D3/D4 scoping notes | ~~**CLOSED** 2026-07-14, ADR-034~~ |
| ~~Fork 6~~ | Query surface: implement the Frame-QL manual's canonical form, or rewrite it | [ADR-035](context/adr_035_query_surface_lineage.md) — the shipped envelope grammar is the canonical lineage; rewrite the manual (D4); promote `parse_frameql` (D3) | ~~**CLOSED** 2026-07-14, ADR-035~~ |

**Not mirrored here (no in-repo resolution instrument):** the remaining audit forks (e.g. Fork 2,
Fork 4) live only in the audit v0.2 and are not reconstructed in this mirror. When one is closed by an
in-repo ADR/WP, it gets a row here at that time. (The audit's own Section E closes when the manuals
alignment pass lands — that is the audit's bookkeeping, not this mirror's.)

## Log
- **Forks 5 & 6 struck 2026-07-14** (Huayin ruled both). Fork 5 → ADR-034 (definition-language scope,
  Certificate-customer partition); Fork 6 → ADR-035 (query surface, envelope grammar as canonical
  lineage). Each ADR records the closure in its own Consequences; this mirror makes it durable and
  ledgered. Forks 1 & 3 backfilled for completeness (closed earlier by ADR-033 / WP-B).
- **Registry note:** the audit v0.2 is not in-repo; if a full in-repo fork registry is wanted, it
  needs the audit's fork list as source (not reconstructed here). Flagged to Huayin.

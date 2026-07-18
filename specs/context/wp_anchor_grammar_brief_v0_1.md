# WP — Anchor grammar (v0.1): the ruled naming and product laws
**From: Huayin (drafted by the design session, 2026-07-15). For: Claude Code.**
**Implements: capture §2b rulings (design_capture_onramp_explorer_v0_1.md — read §2a/§2b
in full; committed to specs/context/ with this WP or alongside it). Small WP, sequenced
BEFORE the manuals CP-M2 merge: Frame-QL Ch. 2 documents THIS grammar; Ch. 6 regenerates
against it. Merge order is a hard gate: this WP → manuals merge.**

## Scope — five ruled changes, all in `columna-core` (parser + well-formedness + tests)

1. **The anchor product `*`.** `parse_frameql` accepts `*` as the anchor separator
   (`revenue @ region*day`, whitespace-tolerant) ALONGSIDE the existing comma. Comma
   remains accepted on input through launch (RULED); everything the system WRITES —
   describe, error messages, any echoed anchor — spells `*`. No output surface may emit
   a comma anchor after this WP.

2. **Level-name uniqueness (well-formedness, fail closed).** Two levels may not share a
   name across the manifold, regardless of family. Enforced at parse/publish as a
   well-formedness error naming both declaration sites. Rationale comment in code:
   same-short-name levels make `@ week` dubious but undetectable; distinct concepts get
   distinct names, and ambiguity surfaces at authoring, never at asking.

3. **Qualified level references, edge-derived membership.** Anchor-side `family.level`
   resolves to the level and VALIDATES membership: level ∈ family iff it touches an edge
   of that lineage (no new declaration — membership is derived). A qualification naming
   a family the level does not belong to is a parse error naming the level's actual
   families. Bare level names remain the expected form everywhere.
   **Resolution order (standing rule, not transitional):** a literal level name match
   wins (dotted stored names like the demo's `cal.month` are a legitimate authoring
   style); otherwise the token splits at the dot and resolves as family.level.
   Well-formedness forbids the one bad state: a manifold where a single token could
   reach two different levels (fail closed, both sites named). Do NOT rename anything —
   the demo is conformant as-is; the post-launch hygiene sweep is the comma retirement
   ONLY. Bare family names are definition-language citizens (`ALONG`/`BLOCKED`/`FERTILE`)
   and query-language non-citizens (qualifier prefixes only).

4. **Universe names rejected in anchor position.** Universes and levels are disjoint
   parser namespaces; a universe name after `@` fails with a pointed error ("universe
   names do not appear in anchors; populations ride ON UNIVERSE").

5. **Tests.** New: `*` parsing (incl. mixed whitespace, inner anchors `avg(aov@day) @
   store*month`); uniqueness violation fails closed with both sites named; valid and
   invalid qualifications (membership-derived); universe-name-in-anchor rejection; the
   transitional literal-dotted rule pinned AND marked for deletion at the hygiene sweep.
   Existing comma tests stay green untouched.

## Out of scope, explicitly
Any renaming of demo levels or seeded queries · comma removal · site or corpus changes ·
`()` or any grand-total string syntax (closed by deferral — the empty-tuple anchor at the
API layer already serves and stays as-is) · describe schema changes beyond anchor
spelling in emitted strings · anything in the tier-2 WP.

## Gates
Draft PR, Huayin's approving review (branch protection). CI green. Report with the diff
and a parse-transcript of the new forms. On merge, notify the manuals session: Ch. 2
writes against this grammar; the docs-local fixture uses clean dotless level names from
birth.

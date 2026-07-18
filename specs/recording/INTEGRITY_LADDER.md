# ch3 transcript recording — the integrity ladder

The two chapter-3 conversations (Cascadia case demo) are recorded LIVE against the shipped agent:
human turns SCRIPTED verbatim from the chapter, agent turns LIVE (real model, real MCP, visible tool
calls). Nothing fabricated. Every take is preserved — the ladder IS part of the case's integrity story.

- **Take 1** (`ch3_take1_transcripts.json`) — surfaced two agent-prompt gaps: the agent consulted a
  definition but did not RELAY its folklore, and it mislabeled a two-year span as "this year".
  The prompt was amended and ratified: **SURFACE THE FOLKLORE** (Dana's folklore rule) and
  **LABEL THE SPAN** (the trust bar).
- **Take 2** (`ch3_take2_transcripts.json`) — CONFIRMED amendment A (the new hire now relays the
  `units_returned` definition + its null convention), and surfaced a THIRD gap: the agent scopes to a
  coordinate value with a `WHERE` filter (`WHERE region = 'west' …`, `WHERE cal.year = 2024`), which is
  not supported (OF-13) — two live BinderExceptions, both cascading to a suppressed "couldn't read"
  reply. The prompt was amended again: **SCOPE BY ANCHOR, NOT WHERE** (interim; amends when OF-13's
  native coordinate filter lands). *Credit where due: take 2's failure mode was the GUARDS WINNING — the
  grounding guard suppressed a would-be ungrounded answer twice rather than let the mind improvise one.
  "Couldn't read that as a grounded reply" is ugly UX with honest bones, and the honest bones are the
  product.*
- **Take 3** (`ch3_take3_transcripts.json`) — recorded against the three-law prompt: all three laws
  effective (the manager's scoped turn resolves via anchor-and-read instead of failing; the folklore is
  relayed). It surfaced the presentation limit — anchor-and-read serves the WHOLE frame, so a coordinate
  answer is present but frame-weighted, not isolated (rowed as OF-13 PRIMARY / OF-15 SECONDARY, post-flip)
  — and the timing/span refinements that became take-4's two law-strengthenings.
- **Take 4** (`ch3_take4_transcripts.json`) — the ladder CAP, recorded against the strengthened
  three-law prompt. The laws fire when the query flows: LABEL THE SPAN's reconciliation opens the
  new-hire's span-mismatched turn ("this covers the full recorded range, both years, not just this
  year"), and the manager's scoped turn serves via anchor-and-read. One reply is grounding-GUARD
  SUPPRESSED ("couldn't read that as a grounded reply") — the agent reached to summarize without a
  grounded query in that turn, and the guard held rather than let it improvise a number. That is the
  guards winning, recorded honestly, not scripted away. A prior roll (`ch3_take4a_badroll_transcripts.json`,
  3 suppressions) is preserved beside it: the agent is a rented mind and it is STOCHASTIC — re-recorded
  once for the defect, per protocol; the better roll ships, the worse roll stays on the record.

Take 4 ships. The ladder's published form: take 1, two gaps; take 2, one law confirmed, one gap;
take 3, three laws effective, presentation and timing refined; take 4 ships; all takes preserved.
Anything still rough — the occasional guard suppression, the frame-weight of a coordinate answer — is
honest about the system this side of OF-13, and the fold teaches it as such.

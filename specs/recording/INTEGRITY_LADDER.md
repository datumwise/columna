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
- **Take 3** (to come) — recorded against the three-law prompt; ships. LABEL THE SPAN finally gets its
  live test (the query now survives to reach it).

All takes preserved: the defect-of-record beside the ship. This is what "recorded, never hand-edited"
means when the thing being recorded is a mind we rent and a world we build.

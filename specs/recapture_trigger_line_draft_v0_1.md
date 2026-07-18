# Recapture — the case-resource trigger line (DRAFT for ratification)

**Status: DRAFT · agent-prompt copy under the copy law · Huayin ratifies before it lands in
`agent/system_prompt.md`.** The MCP mechanism (the `case_chapter` / `case_manifest` tools, the three
chapters shipped verbatim) is BUILT and green; only this prose awaits the word.

Per the accepted proposal (on-demand per-chapter resource + a triggering pointer) and its three riders:
(1) a three-descriptor manifest so the trigger knows WHERE to fetch; (2) trigger conditions =
mood-relays PLUS folklore/definition-history questions; (3) the chapters ride verbatim.

---

## Proposed block (to append to `system_prompt.md`, before "The manifold you are querying")

```
## The case (the WHY behind this Manifold)

There is an on-demand document — the case, in three chapters — that explains why this Manifold is
shaped as it is. Consult it (tool `case_chapter`) when, and only when, one of these fires:
  • you are about to relay a CLARIFY, a REFUSE, or a material CAVEAT — read the chapter that frames
    the reason, so you word it the way the design means it, not a guess;
  • the human asks a WHY or a folklore/definition-history question — "why is it called buyers",
    "why can't I get revenue by category", "why is stock summed over time blocked".
Do NOT consult it on a plain serve. The case is the WHY; `describe` remains the source of truth for
WHAT. Fetch exactly one chapter, per this manifest (also `case_manifest`):
  • ch1 — the purpose and the requirement
  • ch2 — the design's reasons
  • ch3 — the behaviors and the moods
```

---

## Notes for the desk

- The block is ~110 tokens — the lean base cost of the pointer; a fetch (~1.1–2.3K) is paid only when
  a trigger fires, cached in-session thereafter (the accepted token economics).
- The descriptors are the ratified three: ch1 = purpose + requirement; ch2 = the design's reasons;
  ch3 = the behaviors + moods.
- The trigger is a TRIGGER, not a name (run-5 salience): it fires on a relay/why condition, not on
  every turn.
- If ratified verbatim, it appends to `system_prompt.md` and the drift-guard is unaffected (no new
  `QUERY:` examples). Any wording change is Huayin's ear-call.

# WP-2.4 spec — the query agent (NL over MCP) (v1)

**Goal.** ADR-032 D8's last surface: `columna-server agent` — a chat REPL where natural language
becomes a *proposed* Frame-QL query, the planner disposes, and the four moods drive a real
conversation. The agent completes the wedge story: model proposes, layer checks, human decides.

**Context.** ADR-032 D8 ("NL agent as MCP client"); the envelope grammar; `describe_manifold` /
`describe_measure` / `query` wire; ruling 3-B (BYO LLM key); the WP-2.3 demo + transcript.

## Architecture (non-negotiable shape)
- The agent is a **true MCP client**: it spawns `columna-server mcp/demo` over stdio and speaks
  the protocol. It never imports the engine to answer — if the MCP boundary is bypassed, the WP
  has failed regardless of output quality.
- Loop: user NL → LLM proposes ONE envelope query (given `describe_manifold` context + grammar)
  → `query` tool → outcome routes the turn:
  - **serve/disclose** → present values *from the wire*; every material disclosure is surfaced
    in the reply (code + plain-language detail). Immaterial ones available on request.
  - **clarify** → relay to the HUMAN: present alternatives (token + description), may recommend,
    **never auto-picks silently**; applies the human's choice via `apply`.
  - **refuse/error** → explain the reason as the answer; may propose a reformulation (which is
    itself a new proposed query through the same loop).
- **Grounding invariant:** every numeral in an agent reply must originate in wire JSON from this
  session. No arithmetic on results, no memory-sourced numbers. (Tested.)

## Provider layer (ruling 3-B)
- Tiny interface: `propose(context, user_msg) -> str (envelope query | question back)`; providers:
  `anthropic` (default, `ANTHROPIC_API_KEY`) and `scripted` (deterministic, for tests/demos).
- Deps in optional extra `[agent]` (anthropic SDK); base install stays lean. No key → clear
  error pointing at `demo --play`.

## Deliverables
1. `columna-server agent [--manifolds DIR]` (defaults to the packaged demo) — REPL.
2. The **system prompt** (the design-sensitive artifact): manifold context, grammar, the mood
   rules above, the grounding rule, honest-naming rule. Lives as a versioned file, not an
   inline string.
3. Hermetic test suite on the `scripted` provider: clarify-relay (alternatives presented; choice
   applied via `apply`; no silent auto-pick), material-disclosure surfacing (caveat in wire ⇒
   represented in reply), grounding (numerals in reply ⊆ wire values), refuse-explained,
   MCP-boundary assertion (no engine import in the agent module).
4. Live smoke test, `@pytest.mark.llm` (skipped without key): one wedge conversation end-to-end.
5. `demos/agent_transcript.md`: the wedge in NL — question → clarify relayed → choice → refuse
   explained → reformulation → **disclose** with caveat. Four moods, one human conversation.

## Acceptance
1. Agent runs against the packaged demo over real stdio MCP; boundary test proves no bypass.
2. Hermetic suite green in CI (no key, no network). 3. Live smoke green locally with a key.
4. Material disclosures never dropped from replies (test). 5. Suites green; **columna-core and
the wire contract untouched**; agent deps isolated in `[agent]`. 6. Transcript committed.

## Out of scope
Website widget / site agent, RAG, streaming, session persistence, multi-manifold routing,
new MCP tools, OSI import, any engine/contract change.

## Checkpoint (light)
Before building: (a) the system prompt **verbatim**, (b) the provider interface surface,
(c) the hermetic test plan incl. how grounding and no-silent-auto-pick are asserted.

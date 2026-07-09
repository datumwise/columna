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
  → `query` tool → outcome routes the turn. **Role boundary (amended):** the LLM only proposes
  queries and asks questions — it never writes result numbers or answer prose. The SYSTEM presents
  every server reply to the human, verbatim from the wire; so grounding is structural, not a rule
  the model must remember. After each query the loop appends a compact `engine` note (outcome,
  reason/detail, alternatives) to the conversation, as context for the model's NEXT proposal.
  - **serve/disclose** → the system presents the values; every material disclosure is surfaced
    (code + plain-language detail).
  - **clarify** → the system presents the alternatives (description + `apply`) and waits; the human
    chooses; the loop re-issues the query with the chosen alternative's `apply` (mechanical) —
    **never auto-picked**.
  - **refuse/error** → the reason is presented; the model MAY propose exactly ONE reformulated
    query that addresses it (a new proposal through the same loop), then stop.
- **Grounding invariant:** every numeral in an agent reply originates in this session's wire JSON.
  Because the agent never emits a number (role boundary above), it cannot state a wrong one — and
  the formatter renders wire values verbatim-stringified (no rounding), so the test's regex
  membership check is strict. (Tested.)
- **Honest naming / nonexistent measures:** the model uses the manifold's real names and does not
  invent measures. Asked for a plausible-but-fake metric (e.g. "customer churn"), it ASKs which
  real measure is meant. If it ever fabricates a measure anyway, the engine rejects it (unknown
  column) and the formatter presents it as an invalid query — the deterministic backstop.

## Provider layer (ruling 3-B)
- Tiny interface: `propose(system, history, user_msg) -> str (envelope query | question back)`;
  providers: `anthropic` (default; model from `COLUMNA_AGENT_MODEL`, default `claude-opus-4-8`; key
  from `ANTHROPIC_API_KEY`) and `scripted` (deterministic, for tests/demos). `history` carries the
  user/agent/`engine` turns.
- Deps in optional extra `[agent]` (anthropic SDK); base install stays lean. No key → clear
  error pointing at `demo --play`.

## Deliverables
1. `columna-server agent [--manifolds DIR]` (defaults to the packaged demo) — REPL.
2. The **system prompt** (the design-sensitive artifact): manifold context, grammar, the mood
   rules above, the role boundary, the grounding + one-reformulation-after-refuse + honest-naming
   rules. Lives as a **versioned file**, not an inline string; a permanent test parses every prompt
   example against the real engine so prompt/grammar drift is guarded like the `.cml` files.
3. Hermetic test suite on the `scripted` provider (no key, no network): clarify-relay (alternatives
   presented; choice applied via `apply`; no silent auto-pick), material-disclosure surfacing,
   grounding (numerals in reply ⊆ wire; and the agent structurally cannot surface a fabricated
   number), refuse-explained + one reformulation, nonexistent-measure backstop, and the
   MCP-boundary assertion (no engine import in the agent module — subprocess + static).
4. Live smoke tests, `@pytest.mark.llm` (skipped without key): (a) one wedge conversation
   end-to-end (serve → clarify → …); (b) a plausible-but-fake metric ("customer churn") — the model
   ASKs rather than inventing a measure, and never fabricates a number.
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

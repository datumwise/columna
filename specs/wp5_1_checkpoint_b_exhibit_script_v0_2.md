# WP-5.1 checkpoint (b) — exhibit interaction script (v0.2 — APPROVED 2026-07-11, pair-model caption applied)

**Scope.** The two interactive exhibits on the datumwise.ai homepage. Grounded in the shipped
wire contract (contract_version "1", per WP-2.2 as built): outcomes
`serve | disclose | clarify | refuse | error`; wire caveats `{code, materiality, severity,
category, detail, remedy, source, rel_error}`; clarify alternatives carry mechanically
substitutable tokens (guaranteed by columna-core acceptance tests). The widget consumes the
wire as-is; nothing here requires engine or contract changes.

---

## Exhibit A — the ninety-second table (§2)

Client-side only. No endpoint, no wire. Must degrade to fully static with JS disabled.

**State 0 (initial):** the three-row sales table, the question ("what was our average order
value?"), and three buttons: `÷ line items` · `÷ orders` · `÷ customers`. No answers visible.

**On each click:** the relevant entities highlight in the table (the 6 line-item values, or the
3 order rows, or the 2 customer groups), a one-line division animates
(`$250 / 6`), and the answer prints large beneath that button. Answers persist once revealed.

**State 3 (all revealed):** the closing line fades in under the three answers:
"Same data. Same three words. Three answers — none of them wrong." A small link:
"the full ninety-second version → The Grain Gap."

**No-JS fallback:** render State 3 statically (all three divisions and answers shown).

**Interaction budget:** three clicks, one reveal. No other affordances. This exhibit teaches;
it does not demo the product.

---

## Exhibit B — the live widget (§7)

Runs against `demo.datumwise.ai` (the `demo --http` endpoint). Renders **real wire JSON** —
the JSON is not hidden behind the UI; it IS the exhibit.

### Layout per response

1. **Mood badge** — the `outcome` value, in its mood color. The only saturated color on the
   page. `error` renders neutral gray, labeled `error (not a mood — plumbing)`.
2. **Rendered card** — the served value(s) if any; material disclosures inline, styled by
   `severity` (info / caution / critical); a quiet toggle `audit trail (n)` expanding the
   immaterial disclosures. This is the materiality-filtering thesis as UI: everything
   surfaced, the human sees what matters, nothing is lost.
3. **The wire** — the verbatim response JSON, monospace, always visible beneath the card
   (collapsed to ~12 lines with an expand control on mobile). Caption once, above the first
   response: "this is the actual wire — what an AI agent receives. Every answer is a pair: a
   result, and its disclosure. The mood is how the pair reads."

### The script: four seeded queries + one free input

Seeded queries render as buttons; each maps to a fixed Frame-QL request the demo Manifold is
known to answer with the intended mood (all four paths are asserted in the shipped test suite).

**Q1 — the loop-closer (clarify → round-trip).** Button label: "average order value —
the question from the top of this page."
- Fires the AOV query → `outcome: clarify`, `no_result.alternatives` ≥ 2, each
  `{token, description}`.
- The widget renders the alternatives as buttons ("per order" / "per customer" ...), copy
  above them: "It will not pick for you. You pick."
- On pick: re-issues the query with the alternative's token applied → `serve` or `disclose`.
  The resolved card renders with its disclosure(s) attached.
- One line beneath the resolution: "That choice was yours, on the record — not the machine's,
  in silence."

**Q2 — disclose (inform-and-serve).** A rollup that crosses a blocked reduction lineage →
`outcome: disclose` (or `serve` with caveats, per wire): served value WITH a
`blocked_reduction / material / critical` caveat rendered inline. Copy: "It answers — and the
assumption rides with the number."

**Q3 — refuse.** An out-of-universe request → `outcome: refuse`,
`discriminator: unsupported`, with the reason on the wire. Copy: "Not defined over this data —
and it says why."

**Q4 — serve.** Plain additive query (revenue by region) → `outcome: serve`, clean. Copy:
"When the question is fully specified, it just answers." (Included so visitors see the system
is not a refusal machine; four moods witnessable live.)

**Free input — "try to fool it."** A single text field: "ask for a measure by name."
- If the name resolves in the demo Manifold → the query runs; whatever mood returns, renders.
- If it does not resolve → the wire's refuse/error is rendered as the ASK: "no `<name>` in
  this manifold — here is what exists," listing the measure index (from `describe_manifold`,
  fetched once at widget init and cached; list/describe touch no data by construction).
- Placeholder text suggests the canonical trap: `sell_through_rate`. Caption links the
  launch-post transcript: "this exact refusal, captured live, ships in the package."

### Degrade & guards

- On widget init, call the endpoint once; assert `contract_version == "1"`. On failure,
  timeout, or mismatch → swap in the **recorded transcript** (CI-generated at build time from
  the shipped PyPI package, per the v2 integrity rule) with the note "live demo temporarily
  offline — this transcript was generated from the shipped package at build time." The
  seeded-query buttons play the corresponding recorded segments; the free input hides.
- Rate-limit response (429) → same degrade, note reads "the demo is busy — here is the
  recorded run."
- The widget never renders a number that did not arrive on the wire or in the CI transcript.
  No placeholder values, no loading skeletons that resemble data.

### Copy hook (amendment to homepage_as_argument §7)

Insert before the exhibit: "Start with the question you watched go wrong at the top of this
page." (This is the single sentence that closes the §2 ↔ §7 loop.)

---

## Test plan (site-side)

1. Exhibit A: three-click flow; no-JS static render; no layout shift on reveal.
2. Exhibit B live: each seeded query returns its intended mood against the deployed demo
   endpoint (smoke test in deploy pipeline, not unit tests — the moods themselves are
   asserted in columna's own suite).
3. Round-trip: Q1 → pick each alternative → non-clarify outcome renders.
4. Degrade: endpoint stopped → transcript plays; contract_version mutated in a mock → 
   transcript plays.
5. Materiality rendering: material caveat visible without interaction; immaterial caveat
   hidden until `audit trail` toggled; counts correct.
6. Free input: unknown measure renders the ASK with the cached measure index; the input never
   sends anything but the measure-name/query payload (no free text forwarded elsewhere).
7. Wire pane: JSON shown is byte-identical to the response body (assert in dev mode).

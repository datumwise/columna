# WP-5.1 addendum (v2) — datumwise.ai: the argument-first revision

**Status:** supersedes the content/design sections of WP-5.1 v1. All engineering sections of v1
(endpoint, Dockerfile, Fly.io, DNS, rate limiting, token-gating invariants) remain in force
unchanged. Companion artifact: `homepage_as_argument_v0_1.md` (the homepage copy, verbatim-intent,
with exhibit and build annotations — it is checkpoint deliverable (a) in draft).

**Prereq unchanged (Huayin, before kickoff):** durable write access for Claude Code to
`datumwise/columna`, org-side. No tokens through chat.

## What changed and why

The v1 spec predates the ratified movement architecture and the argument-first homepage
decision. v1's Home was "honest-metrics-engine positioning + widget" — a product page with the
demo as hero. The revised vision: **the homepage is the argument itself** — one long-scroll,
typography-forward essay descending the ladder (moral line → ontology → algebra → metadata
independence → stakes), with exactly two interactive exhibits embedded where the argument earns
them. The widget is not the hero; it is Exhibit B — the argument, executed.

Naming rule, site-wide: the founding document is **the Columna Thesis** (the word "manifesto"
is retired). "Column Algebra" appears once as the name-reveal; thereafter "the algebra."

## Revised deliverable 1 — the site (`apps/website/`, Astro, static)

Pages:
- **Home** — the argument scroll, per `homepage_as_argument_v0_1.md`. Two exhibits (below).
  Ambient quickstart chip persistent bottom-right. A quiet "skip to the running demo ↓" anchor
  link in §1 for demo-first visitors.
- **The Thesis** — the founding document (retitled from manifesto v0.4), with the engagement
  framing (dispute · extend · bring evidence) rather than "sign."
- **Why** — the metadata-independence essay (v0.2, pending reconciliation) and the Silent Seam.
- **The Atlas** — the canon surface; renders the Atlas; contribution CTA front and center
  ("bring us the failure modes you've witnessed"). If the Atlas moves to its own repo (open
  recommendation), this page renders from that repo.
- **How these documents relate** — the corpus map page (`how_these_documents_relate_v0_1.md`),
  linked from nav or footer; carries the reading paths and the research citations (all three
  DOIs + benchmark pointers), satisfying v1's Research page.
- **The launch post** — moved verbatim from the pinned Discussion (Discussion links back);
  linked from Home §7 ("the whole confession →").
- **Install** — `pip install` quickstart, `docker run` image, MCP client config. The ambient
  chip and the three doors link here.
- **GitHub** — external link in nav.

Cut from v1 launch scope: the "Run the audit" (fossil audit / Rite) surface. No authored
artifact exists yet; shipping a thin version damages the register. It arrives with WP-5.2 or a
dedicated content WP. (The grain-gap cheat-sheet table is its seed.)

Design language (unchanged in spirit, sharpened): anti-hype, typography-forward, no
illustrations anywhere; serif for the argument sections, sans for wayfinding, monospace for
wire JSON; the four mood colors are the only saturated color and appear only as mood tags;
disclosure as a design element. Register map and build notes: see companion artifact.

## Revised deliverable 3 — the exhibits

**Exhibit A (NEW): the ninety-second table.** Client-side only, no endpoint. The three-row
sales table with three division buttons (÷ line items · ÷ orders · ÷ customers); each click
animates the division; all three answers persist side by side. Static fallback: all three
shown. No wire dependency; must work with JS disabled (render the static form).

**Exhibit B: the live widget** (v1's deliverable 3, relocated to Home §7). Scripted
three-mood flow (clarify → refuse → disclose) live against `demo.datumwise.ai`, rendering real
wire JSON, mood-tagged; plus the "try to fool it" input (nonexistent measure → the ASK). A
seeded serve-path question is permitted so all four moods are witnessable live. Graceful
degrade per v1: endpoint down → recorded transcript plays with "live demo temporarily offline"
note. The site must never look broken.

## Strengthened invariant — the integrity rule (build-enforced)

v1 said: every number shown comes from the wire or the recorded transcript — never
hand-written. v2 closes the remaining gap:

**The recorded fallback transcript is generated in CI at build time by running
`columna-server demo --play` against the shipped (installed-from-PyPI) package. It is never
hand-edited and never checked in by hand.** The build fails if generation fails. The footer
carries the sentence this licenses: "Every transcript and every number on this page is
generated at build time by running the shipped package. This site is structurally incapable of
demoing something it did not ship."

All other v1 invariants unchanged: no engine/contract changes; widget consumes the wire as-is
(`contract_version "1"`); public demo endpoint ungated but rate-limited; token-gated HTTP for
non-demo deployments.

## Acceptance (v1 list, plus)

- Exhibit A functions with and without JS.
- CI transcript generation verified: delete the transcript, build regenerates it from PyPI.
- Naming sweep passes: zero occurrences of "manifesto" or standalone "ColumnA" in site copy.
- v1 items unchanged: site builds + deploys; widget completes the moods live; degrade path
  verified; Dockerfile runs locally; Lighthouse ≥ 90 (note: text-heavy page + two islands —
  Astro islands keep this attainable); all links resolve.

## Checkpoint (light) — status

(a) sitemap + homepage copy verbatim — **APPROVED** (`homepage_as_argument_v0_2.md`, cold-read
    done, Huayin edits applied 2026-07-11); sitemap = the Pages list above.
(b) widget interaction script — **APPROVED** (`wp5_1_checkpoint_b_exhibit_script_v0_2.md`,
    cold-read done 2026-07-11; includes the outcome pair-model caption per
    `design_capture_outcome_pair_v0_1.md`).
(c) Fly deployment plan + rate-limit approach — unchanged from v1; TO WRITE as before.

Build on approval of (a)–(c).

## Open decisions carried (not blockers for kickoff)

1. Atlas repo split (datumwise/silent-failure-atlas) — recommended; affects only where the
   Atlas page reads from.
2. Thesis rename ripple: repo Discussion title, README references, essay v0.2 citations — a
   single sweep task, best done alongside the essay reconciliation.
3. The Manifold's absence from the homepage — deliberate (altitude control); it leads in the
   Thesis and docs. Revisit after cold-read.

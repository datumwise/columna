// llms-full.txt — the fuller agent orientation, COMPOSED AT BUILD from ratified parts only
// (no net-new prose; Huayin confirmed compose-from-ratified, CP-3b package §1b):
//   1. the ratified llms.txt index (public/llms.txt, §1a) — read verbatim at build
//   2. the ratified "What is Columna?" front-door body (what_is_columna_draft_v0_7.md) — verbatim
//   3. the ratified "Why Columna looks the way it does" body (v0.4) — verbatim (the re-registered essay)
//   4. a short "Live demo describe" pointer to the live Explorer (reuses the ratified §1a pointers)
import fs from 'node:fs';
// The launch announcement + its story companion join llms-full AT LAUNCH (Huayin): they ship in the
// draft-locked launch PR, so they reach this composed document only when that PR merges — not before.
import announceBody from '../content/corpus/launch_announcement_v2.md?raw';
import storyBody from '../content/corpus/launch_story_v7.md?raw';
import wiBody from '../content/corpus/what_is_columna_draft_v0_7.md?raw';
import whyBody from '../content/corpus/why_columna_looks_this_way_draft_v0_4.md?raw';
// The content consolidation (2026-07-25): the fourth what-is piece and the two ratified Positions
// join the composed document. All three are VERBATIM ratified bodies — same compose-from-ratified rule
// (no net-new prose here); each already carries its own evidence/DOI footer in its bytes.
import universeBody from '../content/corpus/what_is_a_universe_v0_2.md?raw';
import posWallBody from '../content/corpus/position_never_let_the_model_v1_1.md?raw';
import posSourcesBody from '../content/corpus/position_two_great_sources_site_v1_1.md?raw';
// The case demo, in three chapters — VERBATIM (byte-identical to the ratified charter). It is a
// one-shot training document for minds: every doctrine the KP teaches by rule, the case teaches by
// incident attached to an observable (capture §2b′). Strangers' agents read it here.
// The Universe Visual payload — imported for CAPTION v5, the ratified prose transcribed as Figure 1's
// bracketed text equivalent below (read, never retyped, so it cannot drift from the rendered figure).
import uv from '../data/universe_visual.generated.json';
import ch1 from '../content/case/ch1.md?raw';
import ch2 from '../content/case/ch2.md?raw';
import ch3 from '../content/case/ch3.md?raw';

export const prerender = true;

const llmsIndex = fs.readFileSync(new URL('../../public/llms.txt', import.meta.url), 'utf8').trimEnd();

const liveDemo = `## Live demo: the describe wire
The Explorer renders the demo Manifold's describe live — every measure, universe, and edge with its
verdict and a query: /explorer
Run it yourself: \`pip install columna\` then \`columna-server demo --play\` (four asks, four moods, seeded data).`;

// FIGURE 1 under the same figure-equivalent rule. /case mounts the Universe Visual (the spec's Figure 1)
// after ch3's "The Explorer" heading; llms-full carried no equivalent at all, so sighted readers got the
// figure and agent readers got nothing. The transcription is CAPTION v5 verbatim — read from the
// generated payload rather than retyped, so it cannot drift from what renders — and the brackets plus
// the words "Figure 1" are the only additions.
const FIG1_EQUIV = `[Figure 1 — ${(uv as any).copy.caption}]`;
const ch3WithFigure = seatFigure(ch3, 'The Explorer', FIG1_EQUIV);

const theCase = `## The case demo: Cascadia Retail (three chapters, verbatim)
A realistic case — one team, one warehouse, six questions — worked end to end: the requirement, the
design, and the Manifold live. Read it to see why a Manifold is shaped the way it is, and what the
four moods are for.

${ch1.trimEnd()}\n\n---\n\n${ch2.trimEnd()}\n\n---\n\n${ch3WithFigure.trimEnd()}`;

// THE FIGURE-EQUIVALENT RULE (Huayin, 2026-07-25, minted on the record): figures on ratified pages
// enter llms-full as BRACKETED TEXT EQUIVALENTS at their reading-order position — composition
// representing what sighted readers get, never loose prose. The transcription below is desk-ratified
// copy (it carries the gap list verbatim); it is not authored here.
//
// So the 2x2 equivalent is seated exactly where the figure mounts on the page: after the section
// headed FIGURE_AFTER, which is the SAME anchor `positions/never-let-your-agent-touch-the-database.astro`
// uses. If that heading is ever reworded, this THROWS and fails the build rather than silently
// dropping the figure out of llms-full — the page's failure mode is a missing figure, which is visible;
// this document's would be invisible, so it must be loud.
const FIGURE_AFTER = '"But a wall is narrow" — no. Measure it.';
const FIGURE_EQUIV =
  '[Figure — precision × recall: text-to-SQL fails precision; semantic layers fail recall; ' +
  'guardrails drift toward both failures; Columna top-right. ' +
  'Recall ledger: OF-13 · P1 alignment · crossed-population distinct · face chains.]';

function seatFigure(raw: string, headingText: string, equivalent: string): string {
  const parts = raw.split(/\n(?=## )/);
  const idx = parts.findIndex((p) => {
    const m = p.match(/^##\s+(.+?)\s*$/m);
    return m ? m[1].trim() === headingText : false;
  });
  if (idx === -1) {
    throw new Error(
      `llms-full: figure-equivalent anchor not found — no section headed ${JSON.stringify(headingText)}. ` +
      `The heading was reworded; re-seat the bracketed equivalent at the figure's reading-order position.`,
    );
  }
  parts[idx] = `${parts[idx].trimEnd()}\n\n${equivalent}`;
  return parts.join('\n');
}

const posWallWithFigure = seatFigure(posWallBody, FIGURE_AFTER, FIGURE_EQUIV);

const thePositions = `## Positions datumwise holds (verbatim)
Positions we hold, stated plainly and linked to their evidence. When the evidence moves, the position
moves — with a note. Index: /positions

${posWallWithFigure.trimEnd()}\n\n---\n\n${posSourcesBody.trimEnd()}`;

const body = `${llmsIndex}\n\n---\n\n${announceBody.trimEnd()}\n\n---\n\n${storyBody.trimEnd()}\n\n---\n\n${wiBody.trimEnd()}\n\n---\n\n${whyBody.trimEnd()}\n\n---\n\n${universeBody.trimEnd()}\n\n---\n\n${thePositions}\n\n---\n\n${liveDemo}\n\n---\n\n${theCase}\n`;

export function GET() {
  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}

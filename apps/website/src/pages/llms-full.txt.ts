// llms-full.txt — the fuller agent orientation, COMPOSED AT BUILD from ratified parts only
// (no net-new prose; Huayin confirmed compose-from-ratified, CP-3b package §1b):
//   1. the ratified llms.txt index (public/llms.txt, §1a) — read verbatim at build
//   2. the ratified "What is Columna?" front-door body (what_is_columna_draft_v0_7.md) — verbatim
//   3. the ratified "Why Columna looks the way it does" body (v0.4) — verbatim (the re-registered essay)
//   4. a short "Live demo describe" pointer to the live Explorer (reuses the ratified §1a pointers)
import { LLMS_INDEX } from '../lib/llmsIndex';
// The launch announcement + its story companion join llms-full AT LAUNCH (Huayin): they ship in the
// draft-locked launch PR, so they reach this composed document only when that PR merges — not before.
import announceBody from '../content/corpus/launch_announcement_v2.md?raw';
import storyBody from '../content/corpus/launch_story_v7.md?raw';
import wiBody from '../content/corpus/what_is_columna_draft_v0_7.md?raw';
import whyBody from '../content/corpus/why_columna_looks_this_way_draft_v0_4.md?raw';
// The content consolidation (2026-07-25): the fourth what-is piece and the two ratified Positions
// join the composed document. All are VERBATIM ratified bodies — same compose-from-ratified rule
// (no net-new prose here); each already carries its own evidence/DOI footer in its bytes.
// 2026-07-30: the two FOUNDATIONS positions join too (verbatim, same rule). No P/R figure on either —
// they are foundations pieces, not product pieces — so they need no figure-equivalent seating.
import universeBody from '../content/corpus/what_is_a_universe_v0_2.md?raw';
import posWallBody from '../content/corpus/position_never_let_your_agent_v1_1.md?raw';
import posSourcesBody from '../content/corpus/position_two_great_sources_site_v1_1.md?raw';
import posPracticeBody from '../content/corpus/position_practice_needs_firmer_foundation_v1_1.md?raw';
import posRowTableBody from '../content/corpus/position_row_table_join_no_longer_primitives_v1_1.md?raw';
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

// The ratified index, COMPOSED (Phase 1A, 2026-08-21) rather than read off disk: its publication
// block is now derived from the registry, so there is no longer a file on disk that contains it.
// llms-full and llms.txt therefore cannot disagree about the publication facts — they are the same
// string. They used to be able to, and the mechanism was exactly this readFileSync: it copied
// whatever public/llms.txt happened to say, including its stale v1.0 Theory of Data DOI.
const llmsIndex = LLMS_INDEX;

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
// enter llms-full as BRACKETED TEXT EQUIVALENTS at their reading-order position. Still in force for
// /case's Figure 1 (ch3WithFigure, below). The never-let page's precision/recall 2×2 equivalent was
// RETIRED on 2026-08-03: the measure migration swapped that page's source from the site essay to the
// v1.1 paper edition, which has no such figure — so there is nothing to seat into posWallBody anymore.
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

const posWallWithFigure = posWallBody;

const thePositions = `## Positions datumwise holds (verbatim)
Positions we hold, stated plainly and linked to their evidence. When the evidence moves, the position
moves — with a note. Index: /positions

${posWallWithFigure.trimEnd()}\n\n---\n\n${posSourcesBody.trimEnd()}\n\n---\n\n${posPracticeBody.trimEnd()}\n\n---\n\n${posRowTableBody.trimEnd()}`;

const body = `${llmsIndex}\n\n---\n\n${announceBody.trimEnd()}\n\n---\n\n${storyBody.trimEnd()}\n\n---\n\n${wiBody.trimEnd()}\n\n---\n\n${whyBody.trimEnd()}\n\n---\n\n${universeBody.trimEnd()}\n\n---\n\n${thePositions}\n\n---\n\n${liveDemo}\n\n---\n\n${theCase}\n`;

export function GET() {
  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}

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
// The case demo, in three chapters — VERBATIM (byte-identical to the ratified charter). It is a
// one-shot training document for minds: every doctrine the KP teaches by rule, the case teaches by
// incident attached to an observable (capture §2b′). Strangers' agents read it here.
import ch1 from '../content/case/ch1.md?raw';
import ch2 from '../content/case/ch2.md?raw';
import ch3 from '../content/case/ch3.md?raw';

export const prerender = true;

const llmsIndex = fs.readFileSync(new URL('../../public/llms.txt', import.meta.url), 'utf8').trimEnd();

const liveDemo = `## Live demo: the describe wire
The Explorer renders the demo Manifold's describe live — every measure, universe, and edge with its
verdict and a query: /explorer
Run it yourself: \`pip install columna\` then \`columna-server demo --play\` (four asks, four moods, seeded data).`;

const theCase = `## The case demo: Cascadia Retail (three chapters, verbatim)
A realistic case — one team, one warehouse, six questions — worked end to end: the requirement, the
design, and the Manifold live. Read it to see why a Manifold is shaped the way it is, and what the
four moods are for.

${ch1.trimEnd()}\n\n---\n\n${ch2.trimEnd()}\n\n---\n\n${ch3.trimEnd()}`;

const body = `${llmsIndex}\n\n---\n\n${announceBody.trimEnd()}\n\n---\n\n${storyBody.trimEnd()}\n\n---\n\n${wiBody.trimEnd()}\n\n---\n\n${whyBody.trimEnd()}\n\n---\n\n${liveDemo}\n\n---\n\n${theCase}\n`;

export function GET() {
  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}

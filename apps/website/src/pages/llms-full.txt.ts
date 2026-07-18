// llms-full.txt — the fuller agent orientation, COMPOSED AT BUILD from ratified parts only
// (no net-new prose; Huayin confirmed compose-from-ratified, CP-3b package §1b):
//   1. the ratified llms.txt index (public/llms.txt, §1a) — read verbatim at build
//   2. the ratified "What is Columna?" front-door body (what_is_columna_draft_v0_7.md) — verbatim
//   3. the ratified "Why Columna looks the way it does" body (v0.4) — verbatim (the re-registered essay)
//   4. a short "Live demo describe" pointer to the live Explorer (reuses the ratified §1a pointers)
import fs from 'node:fs';
import wiBody from '../content/corpus/what_is_columna_draft_v0_7.md?raw';
import whyBody from '../content/corpus/why_columna_looks_this_way_draft_v0_4.md?raw';

export const prerender = true;

const llmsIndex = fs.readFileSync(new URL('../../public/llms.txt', import.meta.url), 'utf8').trimEnd();

const liveDemo = `## Live demo: the describe wire
The Explorer renders the demo Manifold's describe live — every measure, universe, and edge with its
verdict and a query: /explorer
Run it yourself: \`pip install columna\` then \`columna-server demo --play\` (four asks, four moods, seeded data).`;

const body = `${llmsIndex}\n\n---\n\n${wiBody.trimEnd()}\n\n---\n\n${whyBody.trimEnd()}\n\n---\n\n${liveDemo}\n`;

export function GET() {
  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}

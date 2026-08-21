// llmsIndex.ts — the ratified llms.txt index, COMPOSED at build (Slice 2 item 1, Phase 1A, 2026-08-21).
//
// WHY THIS FILE EXISTS. `public/llms.txt` was a static file: 79 hand-authored lines, of which nine
// were publication facts. Those nine were the stalest facts on the property. They cited The Theory of
// Data at the v1.0 record (deposited 2026-07-30) — a version behind even /about's already-stale v3.1,
// while Zenodo served v6.1. So the site's two flagship surfaces disagreed with each other AND with the
// record, and the one aimed at machines was the more wrong of the two. Retrieval systems read this
// file first; it was our least accurate page.
//
// A static file in public/ cannot derive anything, so the fix has to move the surface. It moves the
// SMALLEST possible distance: the ratified prose is unchanged, byte for byte, in
// `src/content/llms_index.txt`, with ONE substitution point. Everything else about the document —
// wording, order, headings, the routes it advertises — is exactly what was ratified.
//
// Both consumers now read the composed string from here rather than the file: `/llms.txt` (the route
// that replaces the static asset) and `/llms-full.txt` (which used to fs.readFileSync the public/
// copy). One source, two surfaces — which is the property the old arrangement lacked.

import indexTemplate from '../content/llms_index.txt?raw';
import { CHRONOLOGICAL_SELECTION, currentRecord, displayLabel, COUNTS_ARE_DERIVABLE } from '../data/publications';

const PLACEHOLDER = '{{PUBLICATIONS}}';

// NO COUNT (Huayin's ruling 6, 2026-08-21). The line said "The nine papers, chronological, each with
// a DOI". Nine was hand-typed beside a hand-typed list — the cheapest way to be wrong in public, and
// the kind of wrong that survives because the number and the list drift together only by luck.
//
// The tempting repair is `${pubs.length} papers`. It is refused. `count(distinct DOI)` is not a count
// of papers: this corpus contains papers, program notes, primers, introductions, positions and a
// technical supplement across 21 works and 49 deposited records, and no governed definition says
// which of those the word "papers" ranges over. Replacing a stale magic number with a freshly
// computed wrong one is not a migration, it is a laundering.
//
// So the claim is dropped rather than recomputed, and the drop is enforced: COUNTS_ARE_DERIVABLE is
// false while any work is `kind: unclassified`, and check_publications.py fails the build if a count
// claim appears on a derived surface. When the corpus classification is ruled, the count becomes a
// sentence the registry can defend — and not one minute before.
const HEADING = 'Publications, chronological, each with a DOI:';

const publicationLines = CHRONOLOGICAL_SELECTION.map((workId) => {
  const record = currentRecord(workId);
  return `  - ${displayLabel(workId)} — doi:${record.doi}`;
}).join('\n');

const publicationsBlock = `- ${HEADING}\n${publicationLines}`;

if (!indexTemplate.includes(PLACEHOLDER)) {
  throw new Error(
    `llms.txt: the ${PLACEHOLDER} substitution point is missing from src/content/llms_index.txt. ` +
    `The publication block would silently vanish from the machine-facing index — the exact class of ` +
    `silent omission this file was built to end. Restore the placeholder.`,
  );
}

if (COUNTS_ARE_DERIVABLE) {
  // Not an error — a reminder with teeth. When every work carries a governed kind, this line is the
  // one place that has to decide whether the index states a count again, and on what definition.
  console.warn(
    'llms.txt: every work is now classified, so a governed publication count is derivable. ' +
    'Decide deliberately whether the index should state one, and on what counting unit.',
  );
}

export const LLMS_INDEX: string = indexTemplate
  .replace(PLACEHOLDER, publicationsBlock)
  .trimEnd();

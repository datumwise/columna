/**
 * sources.ts — the typed site adapter over the SOURCE catalog.
 *
 * WHAT A SOURCE IS. Anything a serious reader can be sent to: a deposited work, a normative manual,
 * a generated reference, a piece of machine evidence, a teaching surface, the public negative
 * record, a preserved historical record. `/research` renders this catalog; Ask datumwise is meant to
 * read the same one, so that a human source map and a private AI source map cannot diverge.
 *
 * THE RULE THIS FILE EXISTS TO ENFORCE. The catalog stores no publication fact. Title, version,
 * date, DOI and currency are read from registry/publications through `currentRecord(workId)` and
 * `recordFor(recordId)` at render time. `workId`/`recordId` are foreign keys, never copies — the
 * same discipline that took the publication list off /about, for the same reason: a fact that must
 * be re-typed to stay true will eventually be false.
 *
 * NO `standing` ENUM (Huayin's refinement, 2026-08-25). A source can be deposited AND onsite,
 * generated AND onsite, preserved AND onsite. Those are orthogonal facts and are stored as separate
 * optional fields; `describe()` composes them into a sentence at the point of display. One canonical
 * standing enum would have been another false taxonomy, of exactly the kind the site keeps deleting.
 *
 * WORK CLASSIFICATION STAYS OUT OF THE PUBLICATION REGISTRY. `role` lives here. `works.json.kind`
 * remains `unclassified` for all 32 works, so COUNTS_ARE_DERIVABLE stays false and G10 keeps
 * blocking count claims. This catalog does not create a back door to a count.
 */
import catalog from '../../../../registry/sources/sources.json';
import corpus from '../../../../registry/sources/current-corpus.json';
import { RECORDS, currentRecord, work, doiUrl, type PublicationRecord } from './publications';

export type SourceRole =
  | 'foundation' | 'supplement' | 'introduction' | 'primer' | 'applied' | 'reading'
  | 'position' | 'catalog' | 'study' | 'program-note'
  | 'normative-reference' | 'generated-reference' | 'machine-evidence'
  | 'teaching' | 'negative-record' | 'historical-record';

export interface Source {
  sourceId: string;
  role: SourceRole;
  /** Only for sources that are NOT deposited works. A deposited work's label derives from the registry. */
  title?: string;
  purpose: string;
  route?: string;
  /**
   * A FAITHFUL ONSITE READING SURFACE for the deposited work — /read/<slug> (2026-08-27).
   *
   * DELIBERATELY NOT `route`, and the separation is load-bearing (Huayin, ruling R4). `route` means
   * "a page THIS SITE AUTHORED about this source" — /learn/what-is-the-theory-of-data is a hosted
   * edition wrapped in page chrome the site wrote. A reading surface is not that: it is the work
   * itself, and the site says nothing on it after the crossing block.
   *
   * AND OVERLOADING `route` WOULD HAVE MOVED THE AGENT'S CORPUS. This catalog is read by Ask as
   * well as by the website. `ask/ingest_deposits.targets()` SKIPS any source that has a `route`
   * ("already readable from the shipped site build"), so writing these fourteen reading pages into
   * `route` would have silently switched fourteen Core works from deposit-derived chunks to
   * route-derived ones — and, if the manifest were not regenerated in the same change, indexed each
   * of them twice. Two meanings in one field, with the agent as the reader that pays for it.
   */
  readingRoute?: string;
  workId?: string;
  recordId?: string;
  editionPinned?: boolean;
  generatedBy?: string;
  gates?: string[];
  preservedState?: string;
}

export const SOURCES: Source[] = (catalog as any).sources;

/** A record by its id. Throws rather than returning undefined — a dangling reference is a defect. */
export function recordFor(recordId: string): PublicationRecord {
  const r = RECORDS.find((x) => x.recordId === recordId);
  if (!r) {
    throw new Error(
      `SOURCE CATALOG: no record "${recordId}". Fix the reference in registry/sources/sources.json, ` +
      `or mint the record in registry/publications/records.json. Do not type the fact instead.`
    );
  }
  return r;
}

/**
 * Everything the page needs about one source, with every publication fact DERIVED.
 *
 * `readable` is what the route renders. `current` is what the registry rules current. When a route
 * is edition-pinned and those two differ, both are returned and the page says so plainly — that is
 * the feature, not a defect to hide: an edition-pinned route is neither stale nor current, it is
 * pinned, and the reader is entitled to know which edition they are about to read.
 */
export interface ResolvedSource extends Source {
  /** Editorial label from the works registry (never carries a version). */
  label?: string;
  /** The current deposited record for the work, if this source is a deposited work. */
  current?: PublicationRecord;
  currentHref?: string;
  /** The exact edition the onsite route renders, when it is edition-pinned. */
  readable?: PublicationRecord;
  /** True only when the readable edition is not the current one. */
  editionDiffers: boolean;
}

export function resolve(s: Source): ResolvedSource {
  const current = s.workId ? currentRecord(s.workId) : undefined;
  const readable = s.recordId ? recordFor(s.recordId) : undefined;
  return {
    ...s,
    label: s.workId ? work(s.workId).canonicalLabel : s.title,
    current,
    currentHref: current ? doiUrl(current) : undefined,
    readable,
    editionDiffers: Boolean(readable && current && readable.recordId !== current.recordId),
  };
}

export const RESOLVED: ResolvedSource[] = SOURCES.map(resolve);

/**
 * THE CURRENT REPRESENTATIVE CORPUS (Huayin, 2026-08-25).
 *
 * /research renders THIS, not the whole catalog. The route's job narrowed: it is not the complete
 * set of useful sources, it is the body of works through which datumwise currently states and
 * explains its intellectual position. That is deliberately narrower than the publication record,
 * the public website, Ask's reference material, the technical documentation, the evidence and the
 * teaching surfaces.
 *
 * REFERENCE ONLY sources are NOT rendered here, and deliberately NOT as a second section
 * underneath — that would recreate the exhaustive source estate under another name, which is
 * exactly what the ruling forbids. They stay public and reachable at their own routes; the
 * publication registry continues to preserve the complete deposited record.
 *
 * Membership is ids only, adjudicated in registry/sources/current-corpus.json and gated
 * fail-closed by scripts/check_corpus_membership.py.
 */
const CORPUS_IN: string[] = (corpus as any).in;

export const REPRESENTATIVE: ResolvedSource[] =
  RESOLVED.filter((s) => CORPUS_IN.includes(s.sourceId));

if (REPRESENTATIVE.length !== CORPUS_IN.length) {
  const missing = CORPUS_IN.filter((id) => !RESOLVED.some((s) => s.sourceId === id));
  throw new Error(
    `CURRENT CORPUS: ${missing.length} ruled source(s) are not in the catalog: ${missing.join(', ')}. ` +
    `A membership ruling that names a source the catalog does not have would silently shrink ` +
    `/research. Fix the ruling or the catalog — do not let the page render the difference.`,
  );
}

/**
 * GROUPS exist to accelerate scanning, not to teach a taxonomy (Huayin, 2026-08-25). They are not
 * doors, they are not equal, and several roles deliberately share one heading. Order is the order a
 * serious reader most often wants, which is not the order the corpus was written in.
 */
export const GROUPS: { title: string; blurb: string; roles: SourceRole[] }[] = [
  { title: 'Theory and results',
    blurb: 'The theory itself, and the results that establish it.',
    roles: ['foundation', 'supplement'] },
  { title: 'Introductions and primers',
    blurb: 'The same material without the proofs, and the vocabulary in dependency order.',
    roles: ['introduction', 'primer'] },
  { title: 'Positions',
    blurb: 'Stances we hold, each with its evidence and its deposited edition.',
    roles: ['position'] },
  { title: 'Applied work and readings',
    blurb: 'The theory put to work, and other people’s work read through it.',
    roles: ['applied', 'reading'] },
  { title: 'Studies, catalogues and program notes',
    blurb: 'Empirical work and research programme records.',
    roles: ['study', 'catalog', 'program-note'] },
  { title: 'Normative and generated references',
    blurb: 'What the language permits, and what the parser actually accepts. These govern behaviour; the introductions above do not.',
    roles: ['normative-reference', 'generated-reference'] },
  { title: 'Machine evidence',
    blurb: 'Not documentation. Produced by running the shipped package, and gated so the build fails if the displayed claim drifts.',
    roles: ['machine-evidence'] },
  { title: 'Teaching surfaces',
    blurb: 'Written to be walked into. Deliberately smaller than the theory, and not publications.',
    roles: ['teaching'] },
  { title: 'The negative record',
    blurb: 'What we know is wrong.',
    roles: ['negative-record'] },
  { title: 'Historical records',
    blurb: 'Preserved states that once occupied a current address. Kept faithfully, not maintained.',
    roles: ['historical-record'] },
];

/** The verb on a row's link — Read, Record, Inspect, Open — chosen by what the source actually is. */
export function actions(s: ResolvedSource): { label: string; href: string; hint?: string }[] {
  const out: { label: string; href: string; hint?: string }[] = [];
  if (s.route) {
    const verb =
      s.role === 'machine-evidence' ? 'Inspect' :
      s.role === 'negative-record' ? 'Open' :
      s.role === 'generated-reference' || s.role === 'normative-reference' ? 'Open' :
      'Read';
    out.push({ label: verb, href: s.route });
  }
  // THE PUBLICATION, READABLE HERE (2026-08-27). Offered before the record link, because a reader
  // who can read the work on this site should be told that before being sent to a DOI resolver.
  // The record link is never removed: the deposit remains the authority, and this page reaches it
  // rather than replacing it.
  if (s.readingRoute) out.push({ label: 'Read the publication', href: s.readingRoute, hint: 'in full, here' });
  if (s.currentHref) out.push({ label: 'Record', href: s.currentHref, hint: 'the deposit' });
  return out;
}

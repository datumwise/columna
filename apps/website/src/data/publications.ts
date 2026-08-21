// publications.ts — THE SITE'S ONLY PUBLICATION FACT SOURCE (Slice 2 item 1, Phase 1A).
//
// WHAT THIS REPLACES. Until this file existed, every publication fact on the site was hand-typed at
// the point of use: a `pubs` array in about.astro, three literal DOIs in the footer of every page,
// three more in /ladder, a nine-line list in llms.txt. Nine separate hands, no shared truth. The
// result was exactly what that arrangement produces — the site simultaneously claimed The Theory of
// Data was at v3.1 (/about) and at v1.0 (llms.txt) while Zenodo had been serving v6.1 since
// 2026-08-19, and every page footer cited Two Anchors v1.0 eight days after v2.0 was deposited.
//
// The registry itself is NOT here. It is language-neutral JSON at repo-root `registry/publications/`,
// because it is corpus truth, not website truth — the Python gate (scripts/check_publications.py)
// reads the same bytes this file does, so the checker cannot be checking a different registry than
// the one that renders. This module is the TYPED SITE ADAPTER over it: types, lookups, and the two
// curated selections that decide which works a given surface shows.
//
// THE ONE DISTINCTION THAT MAKES THIS WORK (Huayin's ruling, 2026-08-21):
//
//     datumwise workId  ≠  Zenodo concept DOI / concept recid
//
// A work's identity is minted here and never changes. A deposit ATTACHES an external concept identity
// to an existing work; it does not create the work, and a work that has never been deposited is still
// a work. Nothing in this file, and nothing downstream of it, may derive internal identity by parsing
// a DOI string.
//
// The other half of the same ruling: the EXACT BIBLIOGRAPHIC TITLE IS RECORD-LEVEL. It is not stable
// across versions, and in this corpus it demonstrably is not — the same work has been deposited as
// "The Theory of Data — Particles, Atoms, Anchors, Universes, and Lawful Transformation" (v1.0),
// "The Theory of Data: Governed Analytical Objects, Lawful Transformation, and Certification" (v4.0),
// and plain "The Theory of Data" (v6.0, v6.1). So does authorship and licence, in principle. Those
// live on the Record. The Work carries only a `canonicalLabel` — the site's short name for the thing,
// which is EDITORIAL NAMING, not a publication fact, and is the only publication-adjacent string on
// this site still chosen by a person.

import worksJson from '../../../../registry/publications/works.json';
import recordsJson from '../../../../registry/publications/records.json';

/** A datumwise work: one intellectual object, however many times it has been deposited. */
export interface Work {
  /** Locally minted, permanent, opaque. Never derived from a DOI. The slug is a mnemonic; nothing parses it. */
  workId: string;
  /** The site/corpus short label. Editorial naming, not a bibliographic title. */
  canonicalLabel: string;
  /**
   * Corpus classification. Deliberately `unclassified` for every work at Phase 1A: paper / note /
   * primer / position / supplement are NOT interchangeable counting units, and no governed definition
   * of them exists yet. Until one does, no surface may render a count — see COUNTS_ARE_DERIVABLE.
   */
  kind: string;
  /** External concept identity, attached by deposit. Absent for a work never deposited. */
  conceptRecid?: string | null;
  conceptDoi?: string | null;
}

/** One deposited version of a work. The bibliographic unit. */
export interface PublicationRecord {
  /** Locally minted, permanent, opaque. Mint-only-new: see scripts/mint_publication_records.py. */
  recordId: string;
  workId: string;
  /** The EXACT deposited title of THIS version. */
  title: string;
  version: string | null;
  date: string;
  /** Version DOI — bibliographic/external identity, never internal identity. */
  doi: string;
  recid: string;
  status: 'current' | 'superseded';
  authors: string[];
  license: string | null;
  resourceType: string | null;
  /** recordId of the version this one supersedes, within the SAME work. Never a DOI. */
  supersedes?: string;
}

export const WORKS: Work[] = worksJson as Work[];
export const RECORDS: PublicationRecord[] = recordsJson as PublicationRecord[];

const BY_WORK_ID = new Map(WORKS.map((w) => [w.workId, w]));

// FAIL CLOSED, NAMING THE REASON (proverb 5). Every accessor below throws at BUILD time rather than
// returning undefined, because the failure mode this whole file exists to end is a publication fact
// that renders plausibly while being wrong. A missing work must stop the build, not render an empty
// <em></em> next to a live DOI link.

export function work(workId: string): Work {
  const w = BY_WORK_ID.get(workId);
  if (!w) {
    throw new Error(
      `PUBLICATION REGISTRY: no work "${workId}". Add it to registry/publications/works.json, or fix ` +
      `the caller. A publication surface may not reference a work that does not exist.`,
    );
  }
  return w;
}

export function recordsFor(workId: string): PublicationRecord[] {
  work(workId);
  return RECORDS.filter((r) => r.workId === workId);
}

/**
 * The current record of a work — the ONLY thing a current-facing surface may cite.
 *
 * Deterministic by construction: the registry carries exactly one `current` record per work and the
 * checker enforces it. This function does not pick a winner by date, by version string, or by DOI
 * ordering; it reads the ruled status. That is what makes "no current view may accidentally select
 * v6.0" a structural property rather than a promise.
 */
export function currentRecord(workId: string): PublicationRecord {
  const found = recordsFor(workId).filter((r) => r.status === 'current');
  if (found.length !== 1) {
    throw new Error(
      `PUBLICATION REGISTRY: work "${workId}" has ${found.length} current records, expected exactly 1. ` +
      `The registry is inconsistent; scripts/check_publications.py will say precisely how.`,
    );
  }
  return found[0];
}

export function doiUrl(record: PublicationRecord): string {
  return `https://doi.org/${record.doi}`;
}

/**
 * How a work is NAMED on a current-facing surface: the editorial label, plus the version of the
 * current record when the work has more than one deposited version.
 *
 * The conditional is the honest part. "The Two Anchors of a Measure (Version 2.0)" tells a reader
 * something true and load-bearing — there is an earlier one, and this is not it. "The Silent Failure
 * Atlas (Version 1.3)" tells a reader nothing, because there has never been another. A version
 * marker on a single-deposit work is noise dressed as precision.
 */
export function displayLabel(workId: string): string {
  const w = work(workId);
  const cur = currentRecord(workId);
  const versioned = recordsFor(workId).length > 1 && cur.version;
  return versioned ? `${w.canonicalLabel} (Version ${cur.version})` : w.canonicalLabel;
}

/**
 * COUNTS ARE NOT DERIVABLE YET, AND THAT IS ENFORCED (Huayin's ruling 6, 2026-08-21).
 *
 * llms.txt said "The nine papers, chronological" — a hand-typed number over a hand-typed list, which
 * is the cheapest possible way to be wrong in public. The fix is NOT `count(distinct doi)` wearing the
 * word "papers": records, works, papers, primers, positions and program notes are not the same
 * counting unit, and this corpus contains all of them. 49 records across 21 works is not "21 papers".
 *
 * So the count is not computed, and this flag says why. It flips to true only when every work carries
 * a governed `kind` — at which point "N current published works of kind paper" becomes a sentence the
 * registry can actually defend. Until then check_publications.py forbids any count-of-publications
 * claim on a derived surface, so the stale number cannot be replaced by a fresh wrong one.
 */
export const COUNTS_ARE_DERIVABLE: boolean = WORKS.every((w) => w.kind !== 'unclassified');

/**
 * THE CHRONOLOGICAL SELECTION — /about and llms.txt.
 *
 * MEMBERSHIP AND ORDER ARE CURATED; FACTS ARE NOT. This array is the editorial decision about which
 * works the public list shows and in what sequence. Everything the list then SAYS about them — title,
 * version, DOI, currency — is read from the registry, so this array cannot go stale, only become an
 * editorial question.
 *
 * ORDER IS NOT DERIVED, DELIBERATELY. It is very nearly first-deposit chronology, but not exactly:
 * the Atlas (2026-06-19) has always led the Seam (2026-06-16), and two pairs share a deposit date
 * with no recorded tiebreak. Deriving the order would silently reorder a ratified list to enforce a
 * rule nobody ruled. Preserved as-is; the divergence is recorded, not fixed.
 *
 * NOT IN THIS LIST, AND KNOWN: Analytical Governance (w-analytical-governance, 2026-08-15). The Slice 2
 * ledger §3.6 records /about as missing it. Adding it is a CONTENT ruling, not a currency migration,
 * and Phase 1A was authorized for the latter. One line, when it is ruled.
 */
export const CHRONOLOGICAL_SELECTION: string[] = [
  'w-silent-failure-atlas',
  'w-silent-seam',
  'w-two-anchors',
  'w-nine-model-study',
  'w-multi-universe-processing',
  'w-two-great-sources',
  'w-open-planner',
  'w-tod-foundations-note',
  'w-theory-of-data',
];

/**
 * THE FOOTER SELECTION — the three evidence links in the footer of every page, and the same three
 * verification targets in /ladder. Curated membership; facts derived.
 */
export const FOOTER_SELECTION: string[] = [
  'w-silent-failure-atlas',
  'w-silent-seam',
  'w-two-anchors',
];

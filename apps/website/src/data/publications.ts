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
// AND A WORK MAY ATTACH MORE THAN ONE (Phase 3B.1, 2026-08-21). If a concept were the work, then a
// work deposited under two concepts would be two works — which is what the old single-valued field
// forced, and it was false about this corpus twice over. `w-two-great-sources` is the sharpest case:
// its current deposit is titled *Three Structural Sources of Silent Analytical Failure*, in a
// different Zenodo concept, and the workId did NOT change. The slug is a mnemonic. Nothing reads it.
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
  /**
   * External publication identities, ATTACHED by deposit — one to many, in first-deposit order.
   *
   * A Zenodo concept is not the work; it is an identity the work acquires at a deposit provider, and a
   * work can acquire more than one. The Silent Failure Atlas has two: v1.2 was deposited under
   * 20710592 and v1.3, three days later, under a fresh concept 20762838 rather than as a new version
   * of the first. `w-two-great-sources` has two for a different reason — a retitled successor,
   * *Three Structural Sources*, deposited under its own concept while declaring `isNewVersionOf` the
   * earlier record. Both are ordinary things to do at Zenodo, and a single-valued field could model
   * neither: the first was unrepresentable, and the second would have left a superseded record
   * rendering as current on this very page.
   *
   * EMPTY, NEVER ABSENT, for a work that has never been deposited — a fact this registry states rather
   * than leaves to inference. Nothing here decides currency: that is `status` on the Record, and only
   * that. Not attachment order, not concept, not version string, not date.
   */
  attachedConcepts: { recid: string; doi: string }[];
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
 * TITLE IS TITLE; VERSION IS METADATA (Huayin, 2026-08-21).
 *
 * The first cut of this fused them — `displayLabel()` returned "The Two Anchors of a Measure (Version
 * 2.0)" as one string, which quietly made a version number part of a work's NAME. It is not. A work's
 * editorial label is stable across its whole deposit history; the version belongs to one record of it.
 * Fusing them meant `canonicalLabel` would have had to change every time a version did, which is the
 * precise failure this registry exists to end, reintroduced one layer up.
 *
 * So surfaces get the pieces and compose them. Nothing here returns a pre-fused display string.
 */
export function citation(workId: string) {
  const w = work(workId);
  const record = currentRecord(workId);
  return {
    /** The work's editorial label. Never carries a version. */
    label: w.canonicalLabel,
    /** The EXACT deposited title of the current record. Differs from `label` for most works. */
    title: record.title,
    /** Raw version of the current record, or null. */
    version: record.version,
    /**
     * Version as a short metadata tag — `v6.1` — or null.
     *
     * Null for a single-deposit work: "The Silent Failure Atlas — v1.3" tells a reader nothing,
     * because there has never been another one. A version marker on a work that has only ever been
     * deposited once is noise dressed as precision. Surfaces that always want the version (a formal
     * citation block, say) read `version` directly instead.
     */
    versionTag: recordsFor(workId).length > 1 && record.version ? `v${record.version}` : null,
    date: record.date,
    doi: record.doi,
    href: doiUrl(record),
    recordId: record.recordId,
  };
}

/**
 * ISO date → the house's long form ("2026-08-15" → "15 August 2026"). Presentation only; the record
 * keeps ISO. Deliberately not `toLocaleDateString`, which would make the rendered page depend on the
 * build machine's locale — a build-environment dependency in a published factual claim.
 */
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];

export function longDate(iso: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!m) {
    throw new Error(`PUBLICATION REGISTRY: date ${iso!} is not ISO yyyy-mm-dd; refusing to guess a format.`);
  }
  return `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
}

/**
 * COUNTS ARE NOT DERIVABLE YET, AND THAT IS ENFORCED (Huayin's ruling 6, 2026-08-21).
 *
 * llms.txt said "The nine papers, chronological" — a hand-typed number over a hand-typed list, which
 * is the cheapest possible way to be wrong in public. The fix is NOT `count(distinct doi)` wearing the
 * word "papers": records, works, papers, primers, positions and program notes are not the same
 * counting unit, and this corpus contains all of them. 67 records across 30 works is not "30 papers".
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
 * ANALYTICAL GOVERNANCE JOINS THE LIST (Huayin, 2026-08-21). The Slice 2 ledger §3.6 had already
 * recorded /about as missing it — "repaired automatically once the publication record drives /about".
 * That is what happened: it is one workId appended in first-deposit position (2026-08-15, so last),
 * and every fact it renders — title, version, DOI — comes from the registry like every other entry.
 * The omission was a content defect; closing it took no content authoring.
 */
export const CHRONOLOGICAL_SELECTION: string[] = [
  'w-silent-failure-atlas',
  'w-silent-seam',
  'w-two-anchors',
  'w-nine-model-study',
  'w-multi-universe-processing',
  'w-two-great-sources',
  'w-open-planner',
  // `w-tod-foundations-note` WAS HERE, AND ITS REMOVAL IS A SELECTION CHANGE, NOT A RECORD CHANGE
  // (Huayin, 2026-08-23, Repair Unit 1B). The ToD root-branch currency audit found *The Theory of
  // Data — A Foundations Note* v1.1 to be a PRE-v5 ONTOLOGY carrying three
  // claims v6.1 refuses, not rephrases: three anchors per column (V/M/B) against §3.4's "a measure
  // has one current anchor"; analytical identity located in the column against §3.2's ex-ante family
  // signature; and `measure family` defined AS an aggregation law rather than as the identity-bearing
  // object. It names no ToD version and its only forward pointer is `pip install columna`.
  // (Its DOI is deliberately NOT written here. This file is class `derived`, which means it carries
  // zero literal DOIs and reads every one from the registry; G7 failed closed on a first draft of
  // this very comment, which is the invariant working. The workId is the address.)
  //
  // Rendered here, it appeared on /about and /llms.txt on the line directly above `The Theory of Data
  // — v6.1`, under a nearly identical name and with no historical framing — so a reader or a
  // retrieval system was handed the governing theory and a superseded ontology as equal current
  // publications. THE REGISTRY IS NOT WRONG AND IS NOT TOUCHED: the Work stands, both Records stand,
  // v1.1 remains `current` for its own chain, and nothing is marked superseded without a successor.
  // What was wrong is the SELECTION, which is the editorial half of this file and the only half that
  // can express "historically real, not current theory."
  //
  // THE ARCHITECTURE FACT THIS EXPOSES, recorded rather than repaired here: this list has exactly one
  // lever — present or absent — and it is doing two jobs. "Registry-current record" is modelled
  // precisely, by `status` on the Record. "Movement-current recommended publication" is modelled
  // NOWHERE, so membership in a curated array is the only way to say it, and absence is the only way
  // to deny it. A work that is a first-class historical record but not current theory has no way to
  // appear as what it is. Dropping it is therefore the smallest TRUE repair available, not the
  // right one: the right one is a representation this file does not yet have.
  'w-theory-of-data',
  'w-analytical-governance',
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

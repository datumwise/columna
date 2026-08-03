// The "Latest" rail (homepage v2 §3) — a STATE block, wired from data rather than hand-assembled in
// markup, so the returning visitor's first stop stays consistent and maintainable in one place.
//
// The package VERSION is not hand-typed here: it is read from the integrity transcript's meta
// (transcript.generated.json), which is regenerated at build time by running the SHIPPED package on
// the shipped-coherent deploy path. So the release number the homepage shows is, by construction, the
// version that actually produced every number on the site — it cannot drift from what shipped.
//
// The rest of each row (the label, the human blurb, the link) is curated navigation, edited here.
import transcript from './transcript.generated.json';

const meta = (transcript as any).meta ?? {};
// The UMBRELLA `columna` version — the release/install number, what `pip install columna` gives
// (Huayin's version ruling, 2026-07-25). The honest source for "currently at" and the Latest rail.
// It differs from meta.columna_core after a data-only release (columna + columna-server move, core
// does not) — reading columna_core here was the bug that shipped 0.12.0 to prod.
//
// NO FALLBACK TO columna_core, deliberately. The earlier `?? meta.columna_core` is exactly what
// turned a missing umbrella into a plausible-looking wrong number instead of a visible failure.
// gen_transcript.py now FAILS THE BUILD if the umbrella is not installed, so this field is always
// present on any build that exists — and if it somehow isn't, 'unknown' is the honest thing to
// render, not a different package's version wearing this one's label.
export const PACKAGE_VERSION: string = meta.columna ?? 'unknown';

export interface LatestItem {
  kind: string;                 // the small mono label
  title: string;                // the item
  date: string;                 // shown in --text-muted; ISO, rendered short
  href: string;
  external?: boolean;
}

// THE RELEASE DESCRIPTIONS, KEYED BY VERSION — FAIL-CLOSED (Huayin, 2026-07-26).
//
// The version on this rail is DATA (PACKAGE_VERSION, from the shipped package). Its title and date
// were CURATED beside it, with nothing tying the two together — so 0.13.0 deployed wearing 0.12.0's
// description: "0.13.0 · the crossing triad: touch, assign, alloc · Jul 24", live on the homepage,
// the right number over the wrong release's words. A HALF-data-driven row is worse than a fully
// hand-written one: the moving half makes the stale half look maintained.
//
// The fix is structural, not a correction. The description is keyed BY VERSION and an unknown version
// THROWS AT BUILD TIME, so a release cannot ship until someone writes its line — the rail can never
// again inherit the previous release's clothes. Fails closed and names its reason (proverb 5): a hard
// failure, never a placeholder that renders plausibly.
const RELEASE_NOTES: Record<string, { title: string; date: string }> = {
  '0.12.0': { title: 'the crossing triad: touch, assign, alloc', date: '2026-07-24' },
  '0.12.1': { title: 'the category-driver descriptions', date: '2026-07-24' },
  '0.13.0': { title: "the ASSERT retirement — the language's first removal", date: '2026-07-26' },
  '0.13.1': { title: 'the reconciliation delta reports at its tolerance', date: '2026-07-27' },
  '0.13.2': { title: 'the declared Python floor and ceiling: 3.10–3.13, 64-bit', date: '2026-07-27' },
  // Stated plainly, on purpose (Huayin, 2026-07-29): upstream mcp 2.0 shipped at 13:45 UTC on
  // 2026-07-28 — hours after our launch — and moved fastmcp; our unbounded `mcp>=1.0` meant fresh
  // installs broke for ~17 hours. Capped and fixed. A rail that only ever announces features is a
  // rail nobody has reason to believe; the release that says what went wrong is the asset.
  '0.13.3': {
    title: 'upstream mcp 2.0 broke fresh installs for 17 hours — capped, fixed, and guarded',
    date: '2026-07-29',
  },
  '0.13.4': {
    title: 'the composite input anchor: a product grain is a first-class pin',
    date: '2026-07-30',
  },
  '0.14.0': {
    title: 'column identity is the canonical expression, not a mechanical default (wire contract 2)',
    date: '2026-07-30',
  },
};

const RELEASE = RELEASE_NOTES[PACKAGE_VERSION];
if (!RELEASE) {
  throw new Error(
    `LATEST RAIL: no curated description for shipped version "${PACKAGE_VERSION}". Add an entry to ` +
    `RELEASE_NOTES in src/data/latest.ts naming what this release IS. This build fails closed on ` +
    `purpose: the rail must never wear the previous release's clothes (0.13.0 shipped showing ` +
    `0.12.0's title, publicly, before this guard existed).`
  );
}

// Release version comes from PACKAGE_VERSION (data); its description is KEYED to it (fail-closed).
// Everything else on the rail is curated navigation.
export const LATEST: LatestItem[] = [
  {
    kind: 'release',
    title: `${PACKAGE_VERSION} · ${RELEASE.title}`,
    date: RELEASE.date,
    href: 'https://github.com/datumwise/columna/releases',
    external: true,
  },
  {
    // The vision suite, published 2026-08-02: the three position papers + the two introductions
    // (Theory of Data, Frame-QL). One combined line rather than five rows, to keep the rail from
    // flooding (editorial choice, ontology-sync addendum). Anchored at /positions.
    kind: 'papers',
    title: 'The vision suite: from failure catalog to the intent boundary — five papers',
    date: '2026-08-02',
    href: '/positions',
  },
  {
    kind: 'paper',
    title: 'Missingness Has a Universe — Version 1.0',
    date: '2026-08-02',
    href: 'https://doi.org/10.5281/zenodo.21760508',
    external: true,
  },
  {
    kind: 'paper',
    title: 'The Theory of Data — Version 3.1, the atom-family revision',
    date: '2026-08-02',
    href: 'https://doi.org/10.5281/zenodo.21760008',
    external: true,
  },
  {
    kind: 'position',
    title: 'Never Let Your Agent Touch the Database',
    date: '2026-07-25',
    href: '/positions/never-let-your-agent-touch-the-database',
  },
  {
    kind: 'paper',
    title: 'The Two Great Sources of Silent Analytical Failure',
    date: '2026-07-25',
    href: 'https://doi.org/10.5281/zenodo.21553379',
    external: true,
  },
  {
    kind: 'ledger',
    title: 'The public roadmap and its open forks',
    date: '2026-07-25',
    href: 'https://github.com/datumwise/columna/blob/main/specs/open_forks.md',
    external: true,
  },
];

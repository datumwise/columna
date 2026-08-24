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
  // The generated-family law (ADR-036). Stated as the rule, not the patch: the defect was that a
  // reducer GENERATED above a lawful leaf was invisible to the law walk, so `sum(stock.last@day)`
  // served the same meaningless number its own prohibition refused one syntax away.
  '0.15.0': {
    title: 'generation creates identity, not permission — structurally prohibited reductions now refuse',
    date: '2026-08-20',
  },
  // The coherence hotfix. 0.15.0's core was correct and gated; its companion columna-server was not
  // republished, so `pip install columna==0.15.0` resolved a server whose four-mood demo predated the
  // correction beside it. PyPI metadata is immutable, so the fix is a new coherent set, not an edit.
  // Scoped deliberately to the package set — 0.15.1 adds no Core semantics beyond 0.15.0.
  '0.15.1': {
    title: 'the corrected serving law and four-mood demo now ship as one coherent package set',
    date: '2026-08-21',
  },
  // columna-server 0.9.0 tightened governed admission: a governed publication and a .cml claiming to
  // realize it are an ORIGIN CLAIM, and a claim is not evidence that a compiler ever produced that
  // image from that publication. A lowering receipt now binds the two by content digest, so governed
  // standing can no longer be acquired by co-locating two files. Core's code is unchanged at 0.15.2 —
  // it moves in lockstep with the umbrella, whose dependency floor had to rise. Stated as the rule
  // rather than the file, because the rule is the part a reader needs.
  '0.15.2': {
    title: 'a claim of origin is not evidence of lowering — governed standing now requires a bound execution image',
    date: '2026-08-22',
  },
  // The compiler 0.15.2 was waiting for. Until now nothing turned an authored, published Manifold and
  // its private realization into the .cml the engine actually runs: the receipt could bind a
  // publication to an image, but no governed producer made one. K0 is the first slice — measures,
  // their members and the coordinates they are keyed at — and it fails closed everywhere else,
  // refusing with a named reason rather than emitting an image quietly missing the law it was asked
  // to carry. Stated as the capability, not the module.
  '0.16.0': {
    title: 'a governed publication now compiles to the execution image that serves it',
    date: '2026-08-22',
  },
  // columna-server 0.10.0 adds the provisioner: the step between a compiled image and a runtime the
  // server will admit. It is an assembler, not an authority — it verifies that the publication, the
  // image and the receipt name the same publication, recomputes both digests, and then COPIES the
  // bytes rather than re-emitting them, because the binding is over bytes as shipped and an
  // equivalent re-serialization is still a different file. Core's code is unchanged; umbrella and
  // core move in lockstep so the umbrella's server floor can rise to the companion this set ships.
  '0.16.1': {
    title: 'a compiled image becomes a runtime the server will admit — assembled, never re-emitted',
    date: '2026-08-22',
  },
  // The first public governed fixture. `firstlight` is a real governed publication — minted through
  // the actual ratification path, by a named steward — that the shipped release compiles, binds,
  // provisions, admits and serves through the generic machinery, with no code anywhere that knows
  // its name. State the asymmetry rather than let the demo imply otherwise: Columna can SERVE this
  // publication and cannot MAKE another. The authoring and ratification machinery that produced it
  // is not part of this release. Consumption of governed authority, not its production.
  '0.16.2': {
    title: 'the first governed publication Columna can serve — and still cannot author',
    date: '2026-08-22',
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
  // ── The two public-root surfaces from the repair sequence (Huayin, 2026-08-24, Homepage Mission
  // Step 2). Both landed on 2026-08-24 and neither was represented anywhere on the homepage.
  //
  // THE `kind` LABELS ARE LOAD-BEARING. Every other row on this rail is `paper`, `papers`, `position`,
  // `release`, or `ledger`. Neither of these is a publication and neither may be dressed as one: the
  // Afternoon is a local teaching artifact with NO Zenodo work, record, concept, or DOI, and none is
  // minted for it, so it gets `teaching` and is linked by route rather than by DOI. Known issues is
  // the maintained public defect record, so it reuses the existing `ledger` label — the same word the
  // open-forks row carries — which states its role without promoting it to an entrance.
  //
  // Deliberately NOT here: any version string, edition, or count. This rail's only data-driven field
  // is the release version, and these two rows are curated navigation like every other non-release row.
  {
    kind: 'teaching',
    title: 'The Theory of Data in One Afternoon — the cold-reader on-ramp',
    date: '2026-08-24',
    href: '/start-here',
  },
  {
    kind: 'ledger',
    title: 'Known issues — the public technical record',
    date: '2026-08-24',
    href: '/known-issues',
  },
  {
    // Theory of Data V4.0 — the terminology revision that this whole site pass migrates to.
    // Newest PAPER (2026-08-03), above the vision-suite line; the two 08-24 site surfaces above it
    // are not publications.
    kind: 'paper',
    title: 'The Theory of Data — Version 4.0, the terminology revision',
    date: '2026-08-03',
    href: 'https://doi.org/10.5281/zenodo.21774032',
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

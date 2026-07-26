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
// (Huayin's version ruling, 2026-07-25). This is the honest source for "currently at" and the Latest
// rail. It differs from meta.columna_core after a data-only release (columna + columna-server move,
// core does not) — so reading columna_core here was the bug that showed 0.12.0. Falls back to core
// only if the umbrella somehow isn't reported (both deploy paths install it, so it always is).
export const PACKAGE_VERSION: string = meta.columna ?? meta.columna_core ?? 'dev';

export interface LatestItem {
  kind: string;                 // the small mono label
  title: string;                // the item
  date: string;                 // shown in --text-muted; ISO, rendered short
  href: string;
  external?: boolean;
}

// Release version comes from PACKAGE_VERSION (data); everything else is curated.
export const LATEST: LatestItem[] = [
  {
    kind: 'release',
    title: `${PACKAGE_VERSION} · the crossing triad: touch, assign, alloc`,
    date: '2026-07-24',
    href: 'https://github.com/datumwise/columna/releases',
    external: true,
  },
  {
    kind: 'position',
    title: 'Never Let the Model Touch the Database',
    date: '2026-07-25',
    href: '/positions/never-let-the-model-touch-the-database',
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

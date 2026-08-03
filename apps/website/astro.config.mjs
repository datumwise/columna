// @ts-check
import { defineConfig } from 'astro/config';
// SITEMAP (2026-07-28). Added on launch eve after `site:datumwise.ai` returned ZERO indexed results
// and an assistant, unable to retrieve the domain, silently substituted the confusable neighbour
// `datawise.ai` and read THAT instead. The site was never blocked — every crawler UA gets a 200 with
// the full page, there is no noindex anywhere, http 308s to https, DNS is clean. It was simply
// UNDISCOVERED, with neither of the two affordances that get a new domain crawled. This is the
// cheaper of the two and it stays correct by construction: the sitemap is generated from the real
// route list at build, so it cannot drift from the pages that actually ship.
import sitemap from '@astrojs/sitemap';

// Static, typography-forward, no framework islands — exhibits are vanilla client scripts so the
// page stays text + islands only (Lighthouse ≥ 90 on a text-heavy page).
export default defineConfig({
  site: 'https://datumwise.ai',
  output: 'static',
  // `redirects` below are emitted as meta-refresh stubs (OF-22), so they are excluded: a sitemap
  // should list canonical destinations, never the stubs that point at them.
  integrations: [sitemap({
    filter: (page) => ![
      'https://datumwise.ai/notes/we-invented-nothing/',
      'https://datumwise.ai/launch/',
    ].includes(page),
  })],
  // Retired routes REDIRECT (a 404 is never acceptable for a live/guessable URL); Astro emits a static
  // redirect for each in the build.
  //  · "We invented nothing" re-registered as "Why Columna looks the way it does" (2026-07-17).
  //  · /launch RETIRES into the launch cargo (2026-07-20, post-seal ruling): launch_post_FINAL predates
  //    the framework positioning, the take-ladder precision, and the crossing — post-merge it would be the
  //    property's last fossil at its most guessable route. It redirects to the canonical launch URL; the
  //    corpus source is superseded-and-archived (kept, unimported), never deleted.
  redirects: {
    '/notes/we-invented-nothing': '/why-columna-looks-this-way',
    '/launch': '/announcing-columna',
    //  · The blast-wall position RENAMED (2026-07-26): "the model" collided with Columna's own DATA
    //    model — the homepage says "data model" three times and "the model" three times eleven lines
    //    apart, so a stranger could coherently read the entrance as a rule about our own Manifold,
    //    inverting the pitch at the block designed to convert. This is a PATH redirect, which Astro
    //    emits statically — unlike the #exhibit-b case, where the fragment never reaches the server
    //    and only a client-side shim could work.
    '/positions/never-let-the-model-touch-the-database':
      '/positions/never-let-your-agent-touch-the-database',
    //  · Corpus-map v0.1 → v0.2 promotion (2026-08-03 reorg): the map moves to a top-level /research
    //    route. The old path 301s so external links and the retired footer entry keep landing.
    '/how-these-documents-relate': '/research',
  },
  build: { inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
  vite: {
    // The /docs/* routes render the manuals from the repo-root docs/ residency (CP-M1) as-is —
    // they live above the Astro root, so allow the workspace root for the .md imports.
    server: { fs: { allow: ['../..'] } },
  },
});

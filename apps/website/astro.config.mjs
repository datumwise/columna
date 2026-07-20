// @ts-check
import { defineConfig } from 'astro/config';

// Static, typography-forward, no framework islands — exhibits are vanilla client scripts so the
// page stays text + islands only (Lighthouse ≥ 90 on a text-heavy page).
export default defineConfig({
  site: 'https://datumwise.ai',
  output: 'static',
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
  },
  build: { inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
  vite: {
    // The /docs/* routes render the manuals from the repo-root docs/ residency (CP-M1) as-is —
    // they live above the Astro root, so allow the workspace root for the .md imports.
    server: { fs: { allow: ['../..'] } },
  },
});

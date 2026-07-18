// @ts-check
import { defineConfig } from 'astro/config';

// Static, typography-forward, no framework islands — exhibits are vanilla client scripts so the
// page stays text + islands only (Lighthouse ≥ 90 on a text-heavy page).
export default defineConfig({
  site: 'https://datumwise.ai',
  output: 'static',
  // Corpus register correction (2026-07-17): "We invented nothing" re-registered as
  // "Why Columna looks the way it does". The old route is live and may be linked, so it REDIRECTS —
  // a 404 is not acceptable. Astro emits a static redirect for this in the build.
  redirects: { '/notes/we-invented-nothing': '/why-columna-looks-this-way' },
  build: { inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
  vite: {
    // The /docs/* routes render the manuals from the repo-root docs/ residency (CP-M1) as-is —
    // they live above the Astro root, so allow the workspace root for the .md imports.
    server: { fs: { allow: ['../..'] } },
  },
});

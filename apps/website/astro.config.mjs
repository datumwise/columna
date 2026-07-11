// @ts-check
import { defineConfig } from 'astro/config';

// Static, typography-forward, no framework islands — exhibits are vanilla client scripts so the
// page stays text + islands only (Lighthouse ≥ 90 on a text-heavy page).
export default defineConfig({
  site: 'https://datumwise.ai',
  output: 'static',
  build: { inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
});

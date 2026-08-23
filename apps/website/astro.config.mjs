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

// MARKDOWN MATH (2026-08-22). The corpus carries LaTeX that the site never rendered. `$$ p=(a,x) $$`
// has been shipping as literal dollar signs on /positions/never-let-your-agent-touch-the-database
// since launch, and the incoming Frame-QL Introduction v2.1 deposit carries eleven display blocks
// including the paper's governing equation, `\boxed{Measure = MeasureFamily @ Anchor}`. Those bytes
// are FROZEN — a deposited edition is reproduced verbatim or not at all (Slice 2 ledger, P1 STRICT) —
// so the fix belongs in the RENDERER, never in the source. This is that fix.
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { createRequire } from 'node:module';

// THE VERSION SPLIT THIS BUILD REFUSES TO SHIP (2026-08-22, found the expensive way).
//
// Two different copies of KaTeX are in play and only one of them is visible: `rehype-katex` RENDERS
// with the katex it depends on, while BaseLayout ships the stylesheet of whatever katex package.json
// hoists. The first attempt at this config paired a 0.16 renderer with a 0.18 stylesheet, and 0.18
// had renamed one class — `stretchy` → `katex-stretchy`. Nothing errored. Every page built. Every
// expression rendered. The only casualty was the BOX around `\boxed{Measure = MeasureFamily @ Anchor}`,
// which simply stopped being drawn, because the span carrying it matched no rule in the shipped CSS.
// A silent, screenshot-only failure on the governing equation of the paper this work exists to serve.
//
// So the two are asserted equal, at build, by identity — not by trusting a caret range to stay put.
const require = createRequire(import.meta.url);
const cssKatex = require('katex/package.json');
const rendererKatex = require(require.resolve('katex/package.json', {
  paths: [require.resolve('rehype-katex')],
}));
if (cssKatex.version !== rendererKatex.version) {
  throw new Error(
    `KaTeX version split: BaseLayout ships the CSS of katex ${cssKatex.version}, but rehype-katex ` +
    `renders with katex ${rendererKatex.version}. Class names move between KaTeX lines, so the ` +
    `mismatch fails SILENTLY — markup renders, individual rules stop matching. Pin package.json's ` +
    `\`katex\` to the line rehype-katex depends on so npm dedupes to one copy.`,
  );
}

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
  markdown: {
    // SINGLE-DOLLAR INLINE MATH IS OFF, DELIBERATELY, AND THIS IS THE WHOLE DESIGN DECISION.
    //
    // remark-math's default treats `$x$` as inline math. This corpus cannot afford that default: it
    // is full of unescaped MONEY, in frozen bytes nobody may edit. Measured before this config was
    // written, with the default on:
    //   · /grain-gap  — "$41.67 is a right answer. So is **$83.33**" parses as one inline formula and
    //                   renders as `∗` glyph soup. The page's entire argument is a run of dollar
    //                   amounts; it is destroyed, not degraded.
    //   · /grain-gap  — the order table row `| O1 | Ada | $100, $20 |` collapses mid-row.
    //   · /case (ch3) — "$3,182,555.97 against ... $2,212,391.86" becomes a formula.
    // Turning the option off restores all three to byte-exact prose while every `$$…$$` block still
    // renders. This is the documented remedy in micromark-extension-math for exactly this situation,
    // not a workaround.
    //
    // THE COST, STATED: one expression in the Frame-QL Introduction v2.1 deposit — `$F@A$`, §
    // Terminology — stays literal text. One inline expression against three frozen pages is not a
    // close call, and the alternative (escaping the money) is the one thing the freeze forbids.
    remarkPlugins: [[remarkMath, { singleDollarTextMath: false }]],
    // `throwOnError: false` so a single malformed expression in a DEPOSITED edition degrades to a
    // visible red span instead of failing the deploy — we may not repair the bytes, so the build must
    // not be hostage to them. Verified: every expression in the corpus renders clean today, so this
    // is a guard against future deposits, not cover for a current defect.
    // Output stays KaTeX's default (HTML + MathML): the MathML branch is what a screen reader reads.
    rehypePlugins: [[rehypeKatex, { throwOnError: false, strict: false }]],
  },
  build: { inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
  vite: {
    // The /docs/* routes render the manuals from the repo-root docs/ residency (CP-M1) as-is —
    // they live above the Astro root, so allow the workspace root for the .md imports.
    server: { fs: { allow: ['../..'] } },
  },
});

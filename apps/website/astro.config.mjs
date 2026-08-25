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
import remarkInlineMathDollars from './src/lib/remarkInlineMathDollars.mjs';
// DISPLAY MATH IN BRACKETS (2026-08-23). The ToD Introduction v2.2 deposit writes all twenty-one of
// its display equations as `\[ … \]`, LaTeX's own delimiters, not `$$ … $$`. Same frozen-bytes rule,
// same renderer-side answer. It parses at the same moment `$$` does — see the file for why a tree
// transformer CANNOT do this job (markdown eats `family\_id`'s escape before a transformer can see it).
import remarkDisplayMathBrackets from './src/lib/remarkDisplayMathBrackets.mjs';
// …and its INLINE half (2026-08-23). The same deposit writes `\( … \)` for inline math. Nine spans;
// eight degraded silently into upright parenthesised prose ("measure (F@A)"), and the ninth printed
// the literal string `(\Gamma(e))` in the terminology table, because `\G` is not a markdown escape.
import remarkInlineMathBrackets from './src/lib/remarkInlineMathBrackets.mjs';
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
      // PROTOTYPE ATTRACTION (2026-08-25). /park/* is a design experiment for Huayin + CG2 to judge,
      // not a public surface: unlinked from every navigation, and kept out of the sitemap so it is
      // not advertised to crawlers as part of the site's argument. If the park direction survives
      // review this line is what gets deleted; if it does not, the route goes with it.
      'https://datumwise.ai/park/when-is-it-data/',
      // HOMEPAGE LABORATORY (2026-08-25). Same rule as the park above, and more important here: this
      // route is a prototype of the FRONT PAGE. A crawler finding a second, unlinked homepage is a
      // genuine harm, not just noise. Unlinked from navigation and kept out of the sitemap.
      'https://datumwise.ai/lab/trailhead/',
      'https://datumwise.ai/lab/exhibit/',
      'https://datumwise.ai/lab/threshold/',
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
    // MATH AND MONEY IN ONE CORPUS, WITHOUT EDITING EITHER.
    //
    // remark-math offers two settings and neither one fits these documents. Its DEFAULT makes every
    // `$` open a formula, which was measured against this corpus and destroys three frozen pages:
    //   · /grain-gap  — "$41.67 is a right answer. So is **$83.33**" parses as ONE inline formula and
    //                   renders as `∗` glyph soup. The page's entire argument is a run of dollar
    //                   amounts; it is destroyed, not degraded.
    //   · /grain-gap  — the order table row `| O1 | Ada | $100, $20 |` collapses mid-row.
    //   · /case (ch3) — "$3,182,555.97 against ... $2,212,391.86" becomes a formula.
    // Turning it OFF protects all three — and leaves the Frame-QL Introduction v2.1 deposit's `$F@A$`,
    // the paper's own notation for a measure, printed as literal dollar signs. Both source files are
    // frozen deposited editions, so neither escaping the money nor rewriting the notation is on the
    // table. The discrimination has to be made by a RULE, in the parser.
    //
    // So: remark-math keeps `singleDollarTextMath: false` and owns DISPLAY math only — `$$…$$` is
    // parsed here, before anything else runs, and nothing downstream can weaken it. Inline `$…$` is
    // then decided by PANDOC'S RULE (see src/lib/remarkInlineMathDollars.mjs): an opener not followed
    // by whitespace, a closer not preceded by whitespace and NOT FOLLOWED BY A DIGIT. Currency comes
    // in pairs and the second amount's `$` always has a digit behind it, so the pair never forms;
    // `$F@A$` closes on a `$` followed by `;`, so it does. Order matters — display first, then inline.
    //
    // A BYTE-FAITHFUL PUBLICATION MAY USE EITHER SUPPORTED NOTATION WITHOUT BYTE MUTATION. The ToD
    // Introduction v2.2 deposit writes display math as `\[ … \]`; the Frame-QL Introduction writes it
    // as `$$ … $$`. Both are deposited editions and neither may be normalised toward the other, so
    // BOTH are parsed, in both their display and inline forms. The two bracket plugins emit
    // micromark-extension-math's own token names and depend on remark-math's mdast bridge, so they
    // MUST follow remarkMath here — each asserts that ordering at build rather than trusting this
    // list to stay in order. The inline bracket construct must also be REGISTERED, not merely
    // ordered: micromark prepends extension constructs, which is what lets `\(` open math before
    // `characterEscape` can eat it into a bare `(` — the reason the notation was invisible before.
    remarkPlugins: [
      [remarkMath, { singleDollarTextMath: false }],
      remarkDisplayMathBrackets,
      remarkInlineMathBrackets,
      remarkInlineMathDollars,
    ],
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

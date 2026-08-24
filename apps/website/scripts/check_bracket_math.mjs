#!/usr/bin/env node
/**
 * check_bracket_math.mjs — THE GUARD FOR DISPLAY MATH WRITTEN `\[ … \]`.
 *
 * A SIBLING, NOT AN EXTENSION, of `check_dollar_math.mjs`. That guard answers one question — is this
 * `$…$` an equation or a price — and it answers it about a DELIMITER. Overloading it with a second,
 * unrelated delimiter would blur the thing it exists to state precisely, so bracket display math
 * gets its own gate and its own name. The two are run side by side in CI.
 *
 * WHAT IT PROTECTS. The ToD Introduction v2.2 deposit (10.5281/zenodo.22018598) writes all of its
 * display equations as `\[ … \]`. Those bytes are FROZEN, so the support lives in
 * `src/lib/remarkDisplayMathBrackets.mjs`. The failure mode is SILENT in both directions:
 *   · lost support → the governing identity prints as the literal string `\boxed{Measure = …}`;
 *   · over-eager support → an ordinary `[` alone on a line, or a `\[` inside a code fence, becomes
 *     an equation and the prose around it disappears into a formula.
 * Neither throws. The build stays green and the page says something else. So both are checked.
 *
 * IT CHECKS THREE THINGS.
 *   1. THE CONSTRUCT decides the known cases correctly — conversions and non-conversions, stated.
 *   2. THE DEPOSIT: every `\[ … \]` block in every markdown file the site renders is inventoried and
 *      must survive the round trip to a `math` node with its LaTeX byte-identical to the source
 *      between the fences — in particular `family\_id`, whose markdown escape a post-parse
 *      transformer would have silently eaten into a subscript.
 *   3. THE BUILT HTML for the ToD Introduction route: every block rendered by KaTeX, no literal
 *      delimiter or `\boxed` leaked, no `katex-error`. Skipped with a notice when `dist/` is absent
 *      so the script is still useful before a build; CI always runs it after one.
 *
 * Run: `node scripts/check_bracket_math.mjs`
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkDisplayMathBrackets from '../src/lib/remarkDisplayMathBrackets.mjs';
import remarkInlineMathDollars from '../src/lib/remarkInlineMathDollars.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let failures = 0;
const fail = (msg) => { failures += 1; console.error(`  FAIL  ${msg}`); };

/** The pipeline exactly as astro.config.mjs orders it: display dollars, then brackets, then inline. */
const pipeline = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkMath, { singleDollarTextMath: false })
  .use(remarkDisplayMathBrackets)
  .use(remarkInlineMathDollars);

function mathNodes(src) {
  const tree = pipeline.parse(src);
  pipeline.runSync(tree);
  const found = [];
  (function collect(node) {
    if (node.type === 'math' || node.type === 'inlineMath') found.push(node);
    for (const child of node.children || []) collect(child);
  })(tree);
  return found;
}

const display = (src) => mathNodes(src).filter((n) => n.type === 'math').map((n) => n.value);

/* ── 1 · the construct's decisions, stated as cases ─────────────────────────────────────────── */

const B = '\\';   // one backslash, so the cases below read as the bytes they are

const CONVERTS = [
  ['the simplest block',                 `${B}[\nF@A\n${B}]`,                         ['F@A']],
  ['the paper\'s governing identity',    `${B}[\n${B}boxed{Measure = MeasureFamily @ Anchor}\n${B}]`,
                                          [`${B}boxed{Measure = MeasureFamily @ Anchor}`]],
  ['a multi-line block, verbatim',       `${B}[\nF@B\n${B}qquad\nB${B}succ A.\n${B}]`,
                                          [`F@B\n${B}qquad\nB${B}succ A.`]],
  ['A MARKDOWN ESCAPE INSIDE THE MATH',  `${B}[\n${B}boxed{\nfamily${B}_id\n}\n${B}]`,
                                          [`${B}boxed{\nfamily${B}_id\n}`]],
  ['two blocks in one document',         `${B}[\nA\n${B}]\n\ntext\n\n${B}[\nB\n${B}]`, ['A', 'B']],
  ['trailing whitespace on the fences',  `${B}[  \nF@A\n${B}]  `,                     ['F@A']],
];

const LEAVES_ALONE = [
  ['an ordinary bracketed phrase',       'see [the appendix] for details'],
  ['a literal `[` alone on a line',      'text\n\n[\nnot math\n]'],
  ['brackets inside a fenced code block', '```\n' + `${B}[\nx\n${B}]` + '\n```'],
  ['an indented code block',             `    ${B}[\n    x\n    ${B}]`],
  ['an inline `${B}[ … ${B}]` on one line', `the expression ${B}[ x ${B}] inline`],
  ['an unterminated opener',             `${B}[\nno closer ever arrives`],
  ['a markdown link',                    'a [link](https://example.com) in prose'],
  ['a reference-style link definition',  '[ref]: https://example.com'],
];

console.log('bracket display-math construct — decisions:');
for (const [label, src, expected] of CONVERTS) {
  const got = display(src);
  if (JSON.stringify(got) !== JSON.stringify(expected)) {
    fail(`${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(got)}`);
  }
}
for (const [label, src] of LEAVES_ALONE) {
  const got = display(src);
  if (got.length) fail(`should stay TEXT but became display math — ${label}: ${JSON.stringify(got)}`);
}

/* The other notations must be untouched by this addition. */
const UNCHANGED = [
  ['`$$ … $$` display math still parses', '$$\np=(a,x)\n$$', 'math', ['p=(a,x)']],
  ['inline `$F@A$` still parses',         'written $F@A$;', 'inlineMath', ['F@A']],
  ['currency stays literal',              '$41.67 is a right answer. So is $83.33.', 'inlineMath', []],
  ['currency in a table cell',            '| O1 | Ada | $100, $20 |', 'inlineMath', []],
  ['a lone backslash in prose',           'a path like C:\\Users stays text', 'math', []],
  ['an escaped bracket mid-sentence',     `an escaped ${B}[ in a sentence`, 'math', []],
];
for (const [label, src, type, expected] of UNCHANGED) {
  const got = mathNodes(src).filter((n) => n.type === type).map((n) => n.value);
  if (JSON.stringify(got) !== JSON.stringify(expected)) {
    fail(`${label}: expected ${type} ${JSON.stringify(expected)}, got ${JSON.stringify(got)}`);
  }
}
if (!failures) {
  console.log(`  ok — ${CONVERTS.length} converted case(s), ${LEAVES_ALONE.length} left-alone case(s), ` +
              `${UNCHANGED.length} other-notation case(s)`);
}

/* ── 2 · the corpus inventory, and byte-fidelity of what it converts ────────────────────────── */

const DIRS = ['src/content/corpus', 'src/content/case', '../../docs'];
const files = [];
for (const dir of DIRS) {
  const abs = path.resolve(ROOT, dir);
  if (!fs.existsSync(abs)) continue;
  for (const name of fs.readdirSync(abs)) {
    if (name.endsWith('.md')) files.push(path.join(abs, name));
  }
}

/** Every `\[ … \]` block in the RAW source, read as bytes — the ground truth to compare against. */
function rawBlocks(src) {
  const lines = src.split('\n');
  const blocks = [];
  let fence = null;
  for (let i = 0; i < lines.length; i += 1) {
    const opener = /^\s{0,3}(`{3,}|~{3,})/.exec(lines[i]);
    if (opener) {
      if (!fence) fence = opener[1][0];
      else if (opener[1][0] === fence) fence = null;
      continue;
    }
    if (fence || lines[i].trim() !== '\\[') continue;
    const close = lines.findIndex((l, j) => j > i && l.trim() === '\\]');
    if (close === -1) continue;
    blocks.push({ line: i + 1, latex: lines.slice(i + 1, close).join('\n') });
    i = close;
  }
  return blocks;
}

console.log('\nbracket display-math — inventory across every markdown file the site renders:');
let totalBlocks = 0;
let filesWithBlocks = 0;
for (const file of files.sort()) {
  const src = fs.readFileSync(file, 'utf8');
  if (!src.includes('\\[')) continue;
  const rel = path.relative(ROOT, file);
  const raw = rawBlocks(src);
  const parsed = display(src);
  filesWithBlocks += 1;
  totalBlocks += raw.length;
  console.log(`  ${rel} — ${raw.length} block(s) in source, ${parsed.length} parsed as display math`);
  if (raw.length !== parsed.length) {
    fail(`${rel}: ${raw.length} \\[ … \\] block(s) in the deposited bytes but ${parsed.length} ` +
         `reached the tree as display math.`);
    continue;
  }
  for (let i = 0; i < raw.length; i += 1) {
    if (raw[i].latex !== parsed[i]) {
      fail(`${rel}:${raw[i].line}: the parsed LaTeX is NOT the deposited bytes.\n` +
           `        source: ${JSON.stringify(raw[i].latex)}\n` +
           `        parsed: ${JSON.stringify(parsed[i])}\n` +
           `        A markdown escape was probably consumed — this is exactly why the support is a ` +
           `micromark construct and not a tree transformer.`);
    }
  }
}
console.log(`  ${totalBlocks} block(s) across ${filesWithBlocks} file(s), each byte-identical to its source.`);

/* ── 3 · the built HTML for the routes that carry these blocks ──────────────────────────────── */

const ROUTES = [
  { route: '/learn/what-is-the-theory-of-data', minBlocks: 21 },
];

const dist = path.resolve(ROOT, 'dist');
console.log('\nbracket display-math — the HTML that actually ships:');
if (!fs.existsSync(dist)) {
  console.log('  (skipped — no dist/. Run `npm run build` first; CI always does.)');
} else {
  for (const { route, minBlocks } of ROUTES) {
    const file = path.join(dist, route.replace(/^\//, ''), 'index.html');
    if (!fs.existsSync(file)) { fail(`${route}: no built HTML at ${path.relative(ROOT, file)}`); continue; }
    const html = fs.readFileSync(file, 'utf8');
    const displaySpans = (html.match(/class="katex-display"/g) || []).length;
    const katexSpans = (html.match(/class="katex"/g) || []).length;
    const errors = (html.match(/katex-error/g) || []).length;

    // THE ONE PLACE RAW LaTeX BELONGS IN THE OUTPUT. KaTeX's MathML branch carries the source
    // expression in `<annotation encoding="application/x-tex">` — that is what a screen reader and a
    // copy-paste get, and it is SUPPOSED to read `\boxed{Measure = MeasureFamily @ Anchor}`. Counting
    // it as a leak would fail a correctly-rendered page; not stripping it would make the leak check
    // meaningless. So the annotations are removed first, and everything left is prose the reader sees.
    const annotations = (html.match(/<annotation encoding="application\/x-tex">/g) || []).length;
    const visible = html.replace(/<annotation encoding="application\/x-tex">[\s\S]*?<\/annotation>/g, '');
    const literalBoxed = (visible.match(/\\boxed/g) || []).length;
    const literalOpen = (visible.match(/\\\[/g) || []).length;
    const literalClose = (visible.match(/\\\]/g) || []).length;
    console.log(`  ${route} — katex-display: ${displaySpans}, katex: ${katexSpans}, ` +
                `katex-error: ${errors}, x-tex annotations: ${annotations}, ` +
                `literal \\boxed outside annotations: ${literalBoxed}, ` +
                `literal \\[: ${literalOpen}, literal \\]: ${literalClose}`);
    if (displaySpans < minBlocks) {
      fail(`${route}: ${displaySpans} rendered display block(s), expected at least ${minBlocks}.`);
    }
    if (errors) fail(`${route}: ${errors} katex-error span(s) — an expression failed to render.`);
    if (literalBoxed) fail(`${route}: \\boxed leaked into the HTML as literal text ${literalBoxed} time(s).`);
    if (literalOpen || literalClose) {
      fail(`${route}: raw \\[ / \\] delimiters leaked into the HTML (${literalOpen} / ${literalClose}).`);
    }

    // THE ESCAPE THAT A TREE TRANSFORMER WOULD HAVE EATEN. The deposit writes `family\_id` — an
    // escaped underscore, which is a LITERAL underscore in LaTeX. Consume that escape before KaTeX
    // sees it and the line silently becomes "family" with a SUBSCRIPT "id": a different claim, on a
    // page whose subject is that a family ID is not a canonical name. MathML says which one shipped —
    // a literal underscore is an `<mi>_</mi>`, a subscript is an `<msub>`.
    if (/family\\_id/.test(html)) {
      const boxedIdentity = /<annotation encoding="application\/x-tex">\\boxed\{\nfamily\\_id/.test(html);
      if (!boxedIdentity) {
        fail(`${route}: the family\\_id identity block did not reach KaTeX with its escape intact.`);
      }
      if (/<msub><mi>f<\/mi>/.test(html) || /family<\/mi><msub>/.test(html)) {
        fail(`${route}: \`family\\_id\` rendered with a SUBSCRIPT — the markdown escape was consumed ` +
             `somewhere before KaTeX. The deposit says family_id, literally.`);
      }
    }
  }
}

if (failures) {
  console.error(`\nbracket display-math guard FAILED — ${failures} problem(s) above.`);
  process.exit(1);
}
console.log('\nbracket display-math guard OK.');

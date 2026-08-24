#!/usr/bin/env node
/**
 * check_bracket_math.mjs — THE GUARD FOR MATH WRITTEN IN LaTeX BRACKETS: `\[ … \]` and `\( … \)`.
 *
 * A SIBLING, NOT AN EXTENSION, of `check_dollar_math.mjs`. That guard answers one question — is this
 * `$…$` an equation or a price — and it answers it about a DELIMITER. Overloading it with a second,
 * unrelated delimiter would blur the thing it exists to state precisely, so bracket display math
 * gets its own gate and its own name. The two are run side by side in CI.
 *
 * ONE GUARD FOR ONE NOTATION FAMILY, deliberately. Display `\[ … \]` and inline `\( … \)` are the
 * two halves of LaTeX's bracket notation; they share a corpus, a route, a rendered page and a
 * failure mode, and splitting them across two files would mean two inventories of the same corpus
 * and two readings of the same dist/. They stay apart from `check_dollar_math.mjs`, which answers a
 * different question — equation or price — about a different delimiter.
 *
 * WHAT IT PROTECTS. The ToD Introduction v2.2 deposit writes its display equations as `\[ … \]` and
 * its inline math as `\( … \)`. Those bytes are FROZEN, so the support lives in
 * `src/lib/remarkDisplayMathBrackets.mjs` and `src/lib/remarkInlineMathBrackets.mjs`. The failure
 * mode is SILENT in both directions:
 *   · lost support → the governing identity prints as the literal string `\boxed{Measure = …}`, and
 *     the terminology table prints `Edge contract (\Gamma(e))` — markdown having eaten the
 *     delimiters but not the command behind them;
 *   · over-eager support → an ordinary `[` alone on a line becomes an equation, or an escaped
 *     backslash `\\(` is mistaken for an opener and swallows the prose after it.
 * Neither throws. The build stays green and the page says something else. So both are checked.
 *
 * IT CHECKS THREE THINGS.
 *   1. THE CONSTRUCT decides the known cases correctly — conversions and non-conversions, stated.
 *   2. THE DEPOSIT: every `\[ … \]` block and every `\( … \)` span in every markdown file the site
 *      renders is inventoried and must survive the round trip to a math node with its LaTeX
 *      byte-identical to the source between the delimiters — in particular `family\_id`, whose
 *      markdown escape a post-parse transformer would have silently eaten into a subscript, and
 *      `\Gamma(e)`, whose command markdown does not escape at all. The inventory is PRINTED even
 *      when it passes, exactly as the dollar guard prints its conversions: the job is to make the
 *      rules' reach VISIBLE, so a new corpus piece that starts using this notation shows up here as
 *      a line of output rather than as a surprise on a page.
 *   3. THE BUILT HTML for the ToD Introduction route: every block and span rendered by KaTeX, no
 *      literal delimiter, `\boxed` or any other LaTeX command leaked into visible text, no
 *      `katex-error`. Skipped with a notice when `dist/` is absent so the script is still useful
 *      before a build; CI always runs it after one.
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
import remarkInlineMathBrackets from '../src/lib/remarkInlineMathBrackets.mjs';
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
  .use(remarkInlineMathBrackets)
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
const inline = (src) => mathNodes(src).filter((n) => n.type === 'inlineMath').map((n) => n.value);

/**
 * The SAME pipeline with the inline-bracket plugin removed. Inline math can also arrive from `$…$`
 * and from an inline `$$…$$`, so "how many inlineMath nodes are there" cannot on its own say what
 * this plugin did. Differencing against this baseline can: whatever the full pipeline has and this
 * one does not is exactly what bracket support added, and that is what gets compared to the bytes.
 */
const baselinePipeline = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkMath, { singleDollarTextMath: false })
  .use(remarkDisplayMathBrackets)
  .use(remarkInlineMathDollars);

function baselineInline(src) {
  const tree = baselinePipeline.parse(src);
  baselinePipeline.runSync(tree);
  const found = [];
  (function collect(node) {
    if (node.type === 'inlineMath') found.push(node.value);
    for (const child of node.children || []) collect(child);
  })(tree);
  return found;
}

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

/* The inline construct's rules, numbered as they are in src/lib/remarkInlineMathBrackets.mjs. */
const INLINE_CONVERTS = [
  ['the paper\'s own measure notation',  `measure ${B}(F@A${B}) at a grain`,        ['F@A']],
  ['a LaTeX COMMAND inside a span',      `${B}(${B}Gamma(e)${B})`,                  [`${B}Gamma(e)`]],
  ['two spans in one sentence',          `If ${B}(Revenue${B}) and ${B}(CustomerMonth${B}) then`,
                                          ['Revenue', 'CustomerMonth']],
  ['inside a table cell',                `| **Edge contract ${B}(${B}Gamma(e)${B})** | cond |`,
                                          [`${B}Gamma(e)`]],
  ['rule 2 — `\\\\` binds, does not close', `${B}(a ${B}${B} b${B})`,                    [`a ${B}${B} b`]],
];

const INLINE_LEAVES_ALONE = [
  ['rule 1 — an ESCAPED BACKSLASH is not an opener', `literal ${B}${B}( paren stays`],
  ['rule 2 — `\\\\)` cannot close',                    `${B}(x${B}${B})`],
  ['rule 3 — an unmatched opener',                   `an ${B}( with no closer`],
  ['rule 4 — an empty span',                         `here ${B}(${B}) gone`],
  ['rule 5 — ordinary parentheses',                  'ordinary (parentheses) in prose'],
  ['rule 6 — an inline code span',                   'run `' + `${B}(F@A${B})` + '` verbatim'],
  ['rule 6 — a fenced code block',                   '```\n' + `${B}(F@A${B})` + '\n```'],
  ['a lone backslash in prose',                      'a path like C:' + B + 'Users stays text'],
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

console.log('\nbracket inline-math construct — decisions:');
for (const [label, src, expected] of INLINE_CONVERTS) {
  const got = inline(src);
  if (JSON.stringify(got) !== JSON.stringify(expected)) {
    fail(`${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(got)}`);
  }
}
for (const [label, src] of INLINE_LEAVES_ALONE) {
  const got = inline(src);
  if (got.length) fail(`should stay TEXT but became inline math — ${label}: ${JSON.stringify(got)}`);
}
/* The display half must be unmoved by the inline half, and vice versa. */
const CROSS = [
  ['display brackets still parse', `${B}[\n${B}boxed{x}\n${B}]`, 'math', [`${B}boxed{x}`]],
  ['display brackets are not inline math', `${B}[\nF@A\n${B}]`, 'inlineMath', []],
  ['`$$ … $$` is not inline math', '$$\np=(a,x)\n$$', 'inlineMath', []],
  ['inline brackets are not display math', `measure ${B}(F@A${B})`, 'math', []],
];
for (const [label, src, type, expected] of CROSS) {
  const got = mathNodes(src).filter((n) => n.type === type).map((n) => n.value);
  if (JSON.stringify(got) !== JSON.stringify(expected)) {
    fail(`${label}: expected ${type} ${JSON.stringify(expected)}, got ${JSON.stringify(got)}`);
  }
}
if (!failures) {
  console.log(`  ok — ${INLINE_CONVERTS.length} converted case(s), ` +
              `${INLINE_LEAVES_ALONE.length} left-alone case(s), ${CROSS.length} cross-form case(s)`);
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

/**
 * Every `\( … \)` span in the RAW source, read as bytes. This is a SECOND, INDEPENDENT reading of
 * the same rules the micromark construct implements — deliberately written from the spec in that
 * file's header rather than shared with it, so the two have to agree about what the deposit says.
 * Rule 1 (an escaped backslash is not an opener), rule 2 (a backslash binds the next byte), rule 4
 * (an empty span is not math) and rule 6 (code is unreachable) all appear here too.
 */
function rawInlineSpans(src) {
  const lines = src.split('\n');
  const spans = [];
  let fence = null;

  for (let line = 0; line < lines.length; line += 1) {
    const opener = /^\s{0,3}(`{3,}|~{3,})/.exec(lines[line]);
    if (opener) {
      if (!fence) fence = opener[1][0];
      else if (opener[1][0] === fence) fence = null;
      continue;
    }
    if (fence) continue;
    if (/^ {4,}\S/.test(lines[line])) continue;          // an indented code block

    const text = lines[line];
    let i = 0;
    while (i < text.length) {
      // Rule 6: an inline code span is opaque. Skip from backtick run to matching backtick run.
      if (text[i] === '`') {
        const run = /^`+/.exec(text.slice(i))[0];
        const close = text.indexOf(run, i + run.length);
        i = close === -1 ? text.length : close + run.length;
        continue;
      }
      if (text[i] !== '\\') { i += 1; continue; }
      // Rule 1: `\\(` is an escaped backslash, not an opener — and it consumes both bytes.
      if (text[i + 1] !== '(') { i += 2; continue; }
      let j = i + 2;
      let close = -1;
      while (j < text.length) {
        if (text[j] === '\\') {
          if (text[j + 1] === ')') { close = j; break; }   // rule 2: only `\\)` closes
          j += 2;                                          // rule 2: a backslash binds the next byte
          continue;
        }
        j += 1;
      }
      if (close === -1) { i += 2; continue; }              // rule 3: unmatched opener
      const latex = text.slice(i + 2, close);
      if (latex.length) spans.push({ line: line + 1, latex });   // rule 4
      i = close + 2;
    }
  }
  return spans;
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

/* ── 2b · the same, for inline `\( … \)` — and the FULL REACH of the rule, printed ─────────────── */

console.log('\nbracket inline-math — inventory across every markdown file the site renders:');
let totalSpans = 0;
let filesWithSpans = 0;
let filesScannedForSpans = 0;
for (const file of files.sort()) {
  const src = fs.readFileSync(file, 'utf8');
  if (!src.includes('\\(') && !src.includes('\\)')) continue;
  filesScannedForSpans += 1;
  const rel = path.relative(ROOT, file);
  const raw = rawInlineSpans(src);
  // What bracket support ADDED, isolated from inline math that arrives via dollars.
  const before = baselineInline(src);
  const after = inline(src);
  const added = [...after];
  for (const value of before) {
    const at = added.indexOf(value);
    if (at !== -1) added.splice(at, 1);
  }
  filesWithSpans += raw.length ? 1 : 0;
  totalSpans += raw.length;
  console.log(`  ${rel} — ${raw.length} span(s) in source, ${added.length} added as inline math` +
              (added.length ? `: ${added.map((v) => JSON.stringify(v)).join(' ')}` : ''));
  if (raw.length !== added.length) {
    fail(`${rel}: ${raw.length} \\( … \\) span(s) in the deposited bytes but bracket support added ` +
         `${added.length} inline math node(s). The two readings of the rules disagree.`);
    continue;
  }
  for (let i = 0; i < raw.length; i += 1) {
    if (raw[i].latex !== added[i]) {
      fail(`${rel}:${raw[i].line}: the parsed LaTeX is NOT the deposited bytes.\n` +
           `        source: ${JSON.stringify(raw[i].latex)}\n` +
           `        parsed: ${JSON.stringify(added[i])}`);
    }
  }
}
console.log(`  ${totalSpans} span(s) across ${filesWithSpans} file(s) ` +
            `(${filesScannedForSpans} file(s) carried the delimiter at all), each byte-identical to its source.`);

/* ── 3 · the built HTML for the routes that carry these blocks ──────────────────────────────── */

// THE EXPECTED COUNT IS DERIVED, NEVER TYPED. A literal `21` here would be a fact about one
// published edition living in a file that has no business holding one: it would have to be
// hand-updated on every re-edition, it would be silently wrong until someone noticed, and it would
// make this guard a second place the publication registry has to police. So the pairing declared
// below is STRUCTURAL — this route renders that corpus file — and the number of blocks to expect is
// counted from the deposited bytes at run time. Re-edition moves it by itself.
const ROUTES = [
  {
    route: '/learn/what-is-the-theory-of-data',
    source: 'src/content/corpus/theory_of_data_an_introduction_v2_2.md',
  },
];

const dist = path.resolve(ROOT, 'dist');
console.log('\nbracket math — the HTML that actually ships:');
if (!fs.existsSync(dist)) {
  console.log('  (skipped — no dist/. Run `npm run build` first; CI always does.)');
} else {
  for (const { route, source } of ROUTES) {
    const sourceAbs = path.resolve(ROOT, source);
    if (!fs.existsSync(sourceAbs)) { fail(`${route}: its source ${source} is missing`); continue; }
    const sourceBytes = fs.readFileSync(sourceAbs, 'utf8');
    const expected = rawBlocks(sourceBytes).length;
    const expectedInline = rawInlineSpans(sourceBytes).length;
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

    // KaTeX marks every expression `katex` and wraps only the display ones in `katex-display`, so
    // the inline count is the difference. Both are compared to what the SOURCE carries, derived.
    const inlineSpans = katexSpans - displaySpans;

    // Prose, as a reader sees it: markup gone, annotations gone, scripts and styles gone. Nothing
    // that looks like a LaTeX control sequence may survive in here. This is the check that would
    // have caught `Edge contract (\Gamma(e))` — a leak `\boxed`-specific matching walked straight
    // past, because markdown had eaten the delimiters and left only the command.
    const prose = visible
      .replace(/<(script|style)[\s\S]*?<\/\1>/g, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&[a-z]+;|&#\d+;/g, ' ');
    const commandLeaks = prose.match(/\\[A-Za-z]+/g) || [];

    console.log(`  ${route} — katex-display: ${displaySpans} (source carries ${expected}), ` +
                `katex inline: ${inlineSpans} (source carries ${expectedInline}), ` +
                `katex total: ${katexSpans}, katex-error: ${errors}, ` +
                `x-tex annotations: ${annotations}`);
    console.log(`  ${' '.repeat(route.length)}   visible-text leaks — \\boxed: ${literalBoxed}, ` +
                `\\[: ${literalOpen}, \\]: ${literalClose}, ` +
                `\\(: ${(visible.match(/\\\(/g) || []).length}, ` +
                `\\): ${(visible.match(/\\\)/g) || []).length}, ` +
                `LaTeX commands: ${commandLeaks.length}`);
    if (displaySpans !== expected) {
      fail(`${route}: ${displaySpans} rendered display block(s), but its source carries ${expected}. ` +
           `Every \\[ … \\] block in the deposited bytes must reach the page as display math.`);
    }
    if (errors) fail(`${route}: ${errors} katex-error span(s) — an expression failed to render.`);
    if (literalBoxed) fail(`${route}: \\boxed leaked into the HTML as literal text ${literalBoxed} time(s).`);
    if (literalOpen || literalClose) {
      fail(`${route}: raw \\[ / \\] delimiters leaked into the HTML (${literalOpen} / ${literalClose}).`);
    }
    if (inlineSpans !== expectedInline) {
      fail(`${route}: ${inlineSpans} rendered inline expression(s), but its source carries ` +
           `${expectedInline} \\( … \\) span(s). Every one must reach the page as inline math.`);
    }
    if (/\\\(/.test(visible) || /\\\)/.test(visible)) {
      fail(`${route}: raw \\( / \\) delimiters leaked into the visible HTML.`);
    }
    if (commandLeaks.length) {
      fail(`${route}: ${commandLeaks.length} LaTeX command(s) leaked into VISIBLE TEXT — ` +
           `${[...new Set(commandLeaks)].join(' ')}. A command outside KaTeX's x-tex annotation is ` +
           `math the reader is being shown as source code.`);
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
  console.error(`\nbracket math guard FAILED — ${failures} problem(s) above.`);
  process.exit(1);
}
console.log('\nbracket math guard OK.');

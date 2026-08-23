#!/usr/bin/env node
/**
 * check_dollar_math.mjs — THE GUARD FOR THE RULE THAT TELLS MATH FROM MONEY.
 *
 * `src/lib/remarkInlineMathDollars.mjs` decides, for every `$…$` in every markdown file this site
 * renders, whether it is an equation or a price. Get it wrong in one direction and the Frame-QL
 * Introduction's `$F@A$` prints as dollar signs; wrong in the other and /grain-gap's "$41.67 … $83.33"
 * becomes glyph soup and its order table collapses mid-row. Both source files are FROZEN deposited
 * editions, so the failure can only ever be repaired here, never in the prose.
 *
 * And it is a SILENT failure class: nothing throws, the build stays green, the page just says
 * something else. That is the same shape as the `stretchy`/`katex-stretchy` version split this work
 * already ate once. So the rule gets a gate.
 *
 * TWO THINGS ARE CHECKED.
 *   1. The rule still decides the known cases correctly — the v2.1 notation, and every currency
 *      shape actually present in this corpus, as literals.
 *   2. INVENTORY. Every span the rule would convert, across every markdown file the site renders, is
 *      printed. A new corpus piece that quietly turns a price into an equation shows up here as a
 *      line of output, and fails the build if the converted content is numeric — the signature of
 *      money that slipped through.
 *
 * The inventory is deliberately printed even when it passes: this file's job is to make the rule's
 * reach VISIBLE, not merely to be green. Run: `node scripts/check_dollar_math.mjs`
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkInlineMathDollars, { splitDollarMath } from '../src/lib/remarkInlineMathDollars.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let failures = 0;
const fail = (msg) => { failures += 1; console.error(`  FAIL  ${msg}`); };

/* ── 1 · the decisions, stated as cases ─────────────────────────────────────────────────────── */

const MATH = [
  ['the v2.1 deposit\'s own notation', 'that family at one anchor, written $F@A$;'],
  ['a measure, spelled out', 'the measure $Revenue@CustomerMonth$ is governed'],
  ['a bare variable in prose', 'a transformation $T$ is checked against clause $C$.'],
];
const TEXT = [
  ['/grain-gap, the three answers', '$41.67 is a right answer. So is $83.33. So is $125.00.'],
  ['/grain-gap, one text node of it', "Here's the thing. $41.67 is a right answer. So is "],
  ['/grain-gap, the order table cell', '$100, $20'],
  ['/grain-gap, the division line', 'Divide by the 6 line items → $250 / 6 = $41.67'],
  ['/grain-gap, a lone amount', '$250 every single time.'],
  ['the Case ch3 reconciliation', 'touch total $3,182,555.97 against the grand total of $2,212,391.86'],
  ['a price range', 'between $5 and $10 per seat'],
  ['a shell variable pair', 'echo $HOME then $PATH'],
  ['a lone dollar sign', 'a $ on its own'],
];

console.log('dollar-math rule — decisions:');
for (const [label, src] of MATH) {
  const parts = splitDollarMath(src);
  if (!parts || !parts.some((n) => n.type === 'inlineMath')) fail(`should be MATH but stayed text — ${label}: ${JSON.stringify(src)}`);
}
for (const [label, src] of TEXT) {
  const parts = splitDollarMath(src);
  if (parts) fail(`should stay TEXT but became math — ${label}: ${JSON.stringify(src)}`);
}
if (!failures) console.log(`  ok — ${MATH.length} math case(s), ${TEXT.length} currency/text case(s)`);

/* ── 2 · the inventory, over everything the site renders ────────────────────────────────────── */

const DIRS = ['src/content/corpus', 'src/content/case', '../../docs'];
const files = [];
for (const dir of DIRS) {
  const abs = path.resolve(ROOT, dir);
  if (!fs.existsSync(abs)) continue;
  for (const name of fs.readdirSync(abs)) {
    if (name.endsWith('.md')) files.push(path.join(abs, name));
  }
}

const pipeline = unified().use(remarkParse).use(remarkGfm).use(remarkMath, { singleDollarTextMath: false });
const NUMERIC = /^[^A-Za-z\\]*\d[^A-Za-z\\]*$/;   // digits and punctuation only: money's signature
let converted = 0;
let scanned = 0;

console.log('\ndollar-math rule — inventory of every inline conversion the site would make:');
for (const file of files.sort()) {
  const src = fs.readFileSync(file, 'utf8');
  if (!src.includes('$')) continue;
  scanned += 1;
  const tree = pipeline.parse(src);
  pipeline.runSync(tree);
  remarkInlineMathDollars()(tree);
  const found = [];
  (function collect(node) {
    if (!node || !Array.isArray(node.children)) return;
    for (const child of node.children) {
      if (child.type === 'inlineMath') found.push(child.value);
      else collect(child);
    }
  })(tree);
  const rel = path.relative(ROOT, file);
  if (!found.length) {
    console.log(`  ${rel} — ${(src.match(/\$/g) || []).length} dollar sign(s), 0 converted`);
    continue;
  }
  converted += found.length;
  console.log(`  ${rel} — ${found.length} converted: ${found.map((v) => JSON.stringify(v)).join(' ')}`);
  for (const value of found) {
    if (NUMERIC.test(value)) {
      fail(`${rel}: converted ${JSON.stringify(value)} — that is money, not math. The rule let a ` +
           `currency pair through; fix src/lib/remarkInlineMathDollars.mjs, never the frozen prose.`);
    }
  }
}

console.log(`\nscanned ${scanned} markdown file(s) containing '$'; ${converted} span(s) render as inline math.`);
if (failures) {
  console.error(`\ndollar-math guard FAILED — ${failures} problem(s) above.`);
  process.exit(1);
}
console.log('dollar-math guard OK.');

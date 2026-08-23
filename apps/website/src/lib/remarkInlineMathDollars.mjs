/**
 * remarkInlineMathDollars — single-dollar inline math that money survives.
 *
 * THE PROBLEM THIS EXISTS FOR. `remark-math` offers exactly two settings and neither one fits this
 * corpus. With `singleDollarTextMath: true`, every `$` opens a formula: `/grain-gap`'s "$41.67 is a
 * right answer. So is **$83.33**" becomes ONE inline expression rendered as glyph soup, its order
 * table collapses mid-row, and `/case`'s "$3,182,555.97 … $2,212,391.86" turns into an equation. With
 * it `false`, the Frame-QL Introduction v2.1 deposit's `$F@A$` — the paper's own notation for a
 * measure — renders as literal dollar signs. Both source files are FROZEN deposited editions (Slice 2
 * ledger, P1 STRICT): escaping the money is not available, and neither is rewriting the notation.
 *
 * So the discrimination has to happen in the parser, and it has to be a RULE, not a list of pages.
 *
 * THE RULE IS PANDOC'S, and it is not invented here. Pandoc's `tex_math_dollars` has resolved exactly
 * this ambiguity for prose-with-money since 2010:
 *
 *   1. the opening `$` must NOT be followed by whitespace;
 *   2. the closing `$` must NOT be preceded by whitespace;
 *   3. the closing `$` must NOT be followed by a digit.
 *
 * Rule 3 is the one that does the work. Currency comes in pairs of amounts — "$41.67 … $83.33",
 * "$100, $20", "$3,182,555.97 … $2,212,391.86" — and the second amount's `$` is always followed by a
 * digit, so it can never close the first. The pair never forms; both stay text. Meanwhile `$F@A$`
 * closes on a `$` followed by `;`, and opens on `F`: math, unambiguously.
 *
 * ONE ADDITION OF OUR OWN (rule 4): the content must not be purely numeric — `^[\d.,\s]*$` is
 * rejected. Nothing worth typesetting is only digits, commas, and spaces, and it is precisely what a
 * currency pair that slipped past rules 1–3 would look like. A second lock on the same door.
 *
 * WHY A TRANSFORMER AND NOT A MICROMARK EXTENSION. Running after `remark-math` (which keeps
 * `singleDollarTextMath: false`) means display `$$…$$` is already parsed into `math` nodes and is
 * invisible here — display support cannot be weakened by anything in this file. What is left is
 * ordinary `text` nodes. Code spans, fenced code, and raw HTML are their own mdast node types with no
 * `text` children, so they are structurally out of reach: this plugin cannot touch a `$` inside
 * `pip install`, a shell snippet, or a FrameQL fence.
 *
 * A HELPFUL ACCIDENT OF MDAST, worth knowing when reading the rules above: emphasis splits text.
 * "So is **$83.33**" is a text node then a `strong` node, so a candidate pair spanning that boundary
 * cannot form at all, independent of rules 1–3. The `/case` figures are protected twice over.
 *
 * The nodes emitted are byte-for-byte the shape `mdast-util-math` emits for `$…$`, so `remark-rehype`
 * and `rehype-katex` treat them identically to any other inline math — no special-casing downstream.
 *
 * Measured against every markdown file the site renders (22 corpus pieces, the Case chapters, the two
 * repo-root manuals) this rule converts ZERO spans today; it changes the site only when a document
 * that actually contains inline math arrives. See the commit message for the scan.
 */

/** Rule 4: nothing worth typesetting is only digits, separators, and space. */
const PURELY_NUMERIC = /^[\d.,\s]*$/;

/** mdast-util-math's own `inlineMath` shape, reproduced exactly. */
function inlineMathNode(value) {
  return {
    type: 'inlineMath',
    value,
    data: {
      hName: 'code',
      hProperties: { className: ['language-math', 'math-inline'] },
      hChildren: [{ type: 'text', value }],
    },
  };
}

/**
 * Split one text value into a run of text / inlineMath nodes.
 * Returns `null` when nothing matched, so the caller can leave the node untouched.
 */
export function splitDollarMath(value) {
  const out = [];
  let cursor = 0;
  let i = 0;

  while (i < value.length) {
    if (value[i] !== '$') {
      i += 1;
      continue;
    }

    // Rule 1 — the opener may not be followed by whitespace (or by the end of the text).
    const afterOpen = value[i + 1];
    if (afterOpen === undefined || /\s/.test(afterOpen)) {
      i += 1;
      continue;
    }

    // Scan for a closer that satisfies rules 2 and 3.
    let j = i + 1;
    let close = -1;
    while (j < value.length) {
      if (value[j] === '$') {
        const beforeClose = value[j - 1];
        const afterClose = value[j + 1];
        const closerOk = !/\s/.test(beforeClose) && !(afterClose !== undefined && /\d/.test(afterClose));
        if (closerOk) {
          close = j;
          break;
        }
        // A `$` that cannot close also cannot be scanned through: it is the opener of the NEXT
        // amount ("$41.67 … $83.33"), and treating it as interior text would let a third `$`
        // further along close a span across both. Abandon this opener instead.
        break;
      }
      j += 1;
    }
    if (close === -1) {
      i += 1;
      continue;
    }

    const content = value.slice(i + 1, close);
    // Rule 4, plus the degenerate empty case.
    if (content.length === 0 || PURELY_NUMERIC.test(content)) {
      i += 1;
      continue;
    }

    if (i > cursor) out.push({ type: 'text', value: value.slice(cursor, i) });
    out.push(inlineMathNode(content));
    cursor = close + 1;
    i = close + 1;
  }

  if (out.length === 0) return null;
  if (cursor < value.length) out.push({ type: 'text', value: value.slice(cursor) });
  return out;
}

/** Nodes whose contents are not prose and must never be scanned. */
const OPAQUE = new Set(['code', 'inlineCode', 'math', 'inlineMath', 'html', 'yaml', 'toml']);

export default function remarkInlineMathDollars() {
  return function transformer(tree) {
    walk(tree);
  };

  function walk(node) {
    if (!node || !Array.isArray(node.children)) return;
    let replaced = null;

    for (let index = 0; index < node.children.length; index += 1) {
      const child = node.children[index];
      if (OPAQUE.has(child.type)) continue;
      if (child.type === 'text') {
        const parts = splitDollarMath(child.value);
        if (parts) {
          (replaced ||= []).push([index, parts]);
        }
        continue;
      }
      walk(child);
    }

    // Splice after iterating, so indices stay valid while scanning.
    if (replaced) {
      for (let k = replaced.length - 1; k >= 0; k -= 1) {
        const [index, parts] = replaced[k];
        node.children.splice(index, 1, ...parts);
      }
    }
  }
}

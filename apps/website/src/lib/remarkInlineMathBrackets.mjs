/**
 * remarkInlineMathBrackets — inline math written `\( … \)`, rendered from the deposited bytes.
 *
 * THE SIBLING of `remarkDisplayMathBrackets.mjs`, and it exists for the same reason. The ToD
 * Introduction v2.2 deposit writes its display equations as `\[ … \]` and its INLINE math as
 * `\( … \)` — LaTeX's own paired delimiters, both of them. The site rendered neither. The display
 * half was repaired first; this is the other half, and the invariant is unchanged:
 *
 *   A BYTE-FAITHFUL PUBLICATION MAY USE EITHER SUPPORTED MARKDOWN MATH NOTATION WITHOUT REQUIRING
 *   PUBLICATION-BYTE MUTATION.
 *
 * WHAT WAS ACTUALLY ON THE PAGE. Markdown's escape rules quietly turned `\(` into `(` and `\)` into
 * `)`, so eight of the nine spans degraded silently into upright parenthesised prose — the paper's
 * `measure \(F@A\)` printed as "measure (F@A)", not as math. The ninth did not degrade quietly:
 *
 *     | **Edge contract \(\Gamma(e)\)** | Conditions licensing a governed analytical movement |
 *
 * rendered as the literal string `Edge contract (\Gamma(e))`, because `\G` is not a markdown escape
 * and so nothing consumed it. That was the last literal LaTeX command left in the route's visible
 * text.
 *
 * WHY A MICROMARK TEXT CONSTRUCT. The same reason the display half is a flow construct, and it is
 * not a stylistic preference: MARKDOWN ESCAPES ARE CONSUMED AT PARSE TIME. A post-parse transformer
 * receives `(F@A)` and `(\Gamma(e))` — the delimiters already gone, indistinguishable from ordinary
 * parentheses an author typed on purpose, and with no way to know which of the two `(` in
 * `\Gamma(e)` was a delimiter. Parsing where `$…$` is parsed means the raw TeX bytes between the
 * delimiters are taken verbatim and handed to KaTeX exactly as deposited.
 *
 * WHAT IT EMITS. The token names are `micromark-extension-math`'s own `mathText` names, so
 * `mdast-util-math`'s `fromMarkdown` handlers — already registered by `remark-math`, which must run
 * first — build the standard `inlineMath` node with no bridge of our own. Downstream, `rehype-katex`
 * cannot tell an expression that arrived in brackets from one that arrived in dollars.
 *
 * ── THE AMBIGUITY SURFACE, WHICH IS LARGER HERE THAN FOR DISPLAY ────────────────────────────────
 *
 * A display block is anchored by standing alone on its own line. An inline span has no such anchor,
 * so the rules are stated explicitly and each one is a case in scripts/check_bracket_math.mjs.
 *
 *   1. AN ESCAPED BACKSLASH IS NOT AN OPENER. The bytes `\\(` are an escaped backslash followed by
 *      an ordinary parenthesis, and must stay that way. This falls out of WHERE the construct runs
 *      rather than from a special case: it is tried at the first `\`, sees `\` where it needs `(`,
 *      and declines — after which micromark's own `characterEscape` consumes `\\` into a literal
 *      backslash exactly as it always did. Order is not left to luck: micromark PREPENDS extension
 *      constructs, so this is tried before `characterEscape` (which is what lets `\(` open math at
 *      all, since `characterEscape` would otherwise eat it into a bare `(`).
 *
 *   2. INSIDE A SPAN, A BACKSLASH BINDS THE NEXT BYTE — TeX's own lexing rule. So `\\` is two
 *      consumed bytes and cannot close, and `\(a \\ b\)` is one span containing `a \\ b`. The
 *      consequence is deliberate: `\(x\\)` has no closer and stays prose, because in TeX those bytes
 *      are a line break followed by an unmatched parenthesis, and guessing which the author meant is
 *      not this file's job.
 *
 *   3. AN UNMATCHED OPENER STAYS PROSE. No `\)` before the end of the text run means the construct
 *      declines and the bytes render as they did yesterday.
 *
 *   4. AN EMPTY SPAN IS NOT MATH. `\(\)` is rejected; nothing worth typesetting is nothing.
 *
 *   5. ORDINARY PARENTHESES ARE UNREACHABLE. Prose parentheses carry no backslash, so the construct
 *      is never even tried at them.
 *
 *   6. CODE IS UNREACHABLE, STRUCTURALLY. Fenced code, indented code and inline code spans consume
 *      their own contents as code data; text constructs are not run inside them. Not a check — a
 *      property of where this is registered.
 *
 * WHAT IT DOES NOT TOUCH. `$$ … $$` and `\[ … \]` are display constructs and are parsed elsewhere;
 * single-`$` currency/math discrimination is decided afterwards by `remarkInlineMathDollars.mjs`,
 * on bytes that are already an `inlineMath` node by the time it runs.
 *
 * NO IMPORTS ON PURPOSE, as with its sibling: micromark's helpers are not declared dependencies of
 * this package, so the one predicate and three character codes are inlined rather than reached for
 * across an undeclared edge.
 */

/* micromark character codes (micromark-util-symbol/lib/codes.js). */
const EOF = null;
const BACKSLASH = 92;        // \
const LEFT_PAREN = 40;       // (
const RIGHT_PAREN = 41;      // )

/* micromark-util-character, inlined: line endings are the negative codes below -2. */
const isLineEnding = (code) => code !== EOF && code < -2;

/** `\)` — attempted at every backslash inside a span, so rule 2 above decides before any consuming. */
const closingSequence = { tokenize: tokenizeClosingSequence, partial: true };

function tokenizeClosingSequence(effects, ok, nok) {
  return start;

  function start(code) {
    if (code !== BACKSLASH) return nok(code);
    effects.enter('mathTextSequence');
    effects.consume(code);
    return closingParen;
  }

  function closingParen(code) {
    if (code !== RIGHT_PAREN) return nok(code);
    effects.consume(code);
    effects.exit('mathTextSequence');
    return ok;
  }
}

export const inlineMathBracketsConstruct = {
  name: 'inlineMathBrackets',
  tokenize: tokenizeInlineMathBrackets,
};

function tokenizeInlineMathBrackets(effects, ok, nok) {
  let size = 0;   // bytes of TeX seen, for rule 4

  return start;

  function start(code) {
    if (code !== BACKSLASH) return nok(code);
    effects.enter('mathText');
    effects.enter('mathTextSequence');
    effects.consume(code);
    return openingParen;
  }

  /* Rule 1 lives here: anything other than `(` — including the second `\` of `\\(` — declines. */
  function openingParen(code) {
    if (code !== LEFT_PAREN) return nok(code);
    effects.consume(code);
    effects.exit('mathTextSequence');
    return contentStart;
  }

  function contentStart(code) {
    // Rule 3: no closer before the end of the run.
    if (code === EOF) return nok(code);
    if (isLineEnding(code)) {
      effects.enter('lineEnding');
      effects.consume(code);
      effects.exit('lineEnding');
      size += 1;
      return contentStart;
    }
    // Rule 2: at a backslash, the closer gets first refusal; otherwise the pair is content.
    if (code === BACKSLASH) {
      return effects.attempt(closingSequence, after, escapedByte)(code);
    }
    effects.enter('mathTextData');
    return data(code);
  }

  function data(code) {
    if (code === EOF || isLineEnding(code) || code === BACKSLASH) {
      effects.exit('mathTextData');
      return contentStart(code);
    }
    effects.consume(code);
    size += 1;
    return data;
  }

  /* A backslash that did not open a closer takes the next byte with it — TeX's rule, not ours. */
  function escapedByte(code) {
    effects.enter('mathTextData');
    effects.consume(code);
    size += 1;
    return escapedByteTail;
  }

  function escapedByteTail(code) {
    if (code === EOF || isLineEnding(code)) {
      effects.exit('mathTextData');
      return contentStart(code);
    }
    effects.consume(code);
    size += 1;
    effects.exit('mathTextData');
    return contentStart;
  }

  function after(code) {
    // Rule 4: `\(\)` carries nothing and is not math.
    if (size === 0) return nok(code);
    effects.exit('mathText');
    return ok(code);
  }
}

/** The micromark extension: one text construct, keyed on `\`. */
export const inlineMathBracketsSyntax = () => ({
  text: { [BACKSLASH]: inlineMathBracketsConstruct },
});

/**
 * The remark plugin. Registers the syntax only — the mdast bridge is `remark-math`'s, so this MUST
 * be listed after `remark-math` in `markdown.remarkPlugins`. Asserted rather than trusted: getting
 * it wrong is the silent kind of wrong, emitting `mathText` tokens that nothing turns into a node,
 * which would delete the expressions from the page rather than erroring.
 */
export default function remarkInlineMathBrackets() {
  const data = this.data();

  const bridged = (data.fromMarkdownExtensions || []).flat().some(
    (extension) => extension && extension.enter && extension.enter.mathText,
  );
  if (!bridged) {
    throw new Error(
      'remarkInlineMathBrackets: no `mathText` fromMarkdown handler is registered. This plugin ' +
      'emits micromark-extension-math\'s own token names and relies on mdast-util-math to build ' +
      'the `inlineMath` node, so `remark-math` must be applied BEFORE it in markdown.remarkPlugins.',
    );
  }

  (data.micromarkExtensions || (data.micromarkExtensions = [])).push(
    inlineMathBracketsSyntax(),
  );
}

/**
 * remarkDisplayMathBrackets — display math written `\[ … \]`, rendered from the deposited bytes.
 *
 * WHY THIS EXISTS. The ToD Introduction v2.2 deposit (Zenodo 10.5281/zenodo.22018598) writes all
 * twenty-one of its display equations with LaTeX's own bracket delimiters:
 *
 *     \[
 *     \boxed{Measure = MeasureFamily @ Anchor}
 *     \]
 *
 * The site's math pipeline was built for `$$ … $$` (see astro.config.mjs), so those equations —
 * including the paper's governing identity, on the first screen — shipped as literal LaTeX. The
 * bytes are FROZEN: a deposited edition is reproduced verbatim or not at all (Slice 2 ledger,
 * P1 STRICT). So, as with math-vs-money before it, the fix belongs in the RENDERER.
 *
 * The invariant this satisfies: A BYTE-FAITHFUL PUBLICATION MAY USE EITHER SUPPORTED MARKDOWN MATH
 * NOTATION WITHOUT REQUIRING PUBLICATION-BYTE MUTATION.
 *
 * WHY A MICROMARK CONSTRUCT AND NOT A TREE TRANSFORMER — the decisive point, found by reading the
 * deposit rather than by taste. `remarkInlineMathDollars.mjs` is a post-parse tree transformer, and
 * it is the shape precedent here, but that shape CANNOT be used for `\[ … \]`, for one reason:
 *
 *   MARKDOWN ESCAPES ARE CONSUMED AT PARSE TIME, INCLUDING INSIDE THE EQUATION.
 *
 * By the time an mdast tree exists, `\[` has already become the text `[`, `\]` has become `]` — and
 * fatally, line 283 of the deposit,
 *
 *     family\_id
 *
 * has already become `family_id`. A transformer handing that to KaTeX renders "family" with a
 * SUBSCRIPT "id" — a different statement from the one the paper makes, arriving silently, with a
 * green build. The same class of failure as the `stretchy`/`katex-stretchy` split this work already
 * ate once. A transformer would also be unable to tell a deposited `\[` from an ordinary literal
 * `[` alone on a line, because both arrive as the same byte.
 *
 * Parsing at the same moment `$$` is parsed avoids all of it. The raw bytes between the fences are
 * taken verbatim, untouched by escape processing, exactly as micromark already does for `$$`.
 *
 * WHAT IT EMITS, AND WHY THERE IS NO OTHER WIRING. The tokens are named exactly as
 * `micromark-extension-math`'s own `mathFlow` names them, so `mdast-util-math`'s `fromMarkdown`
 * handlers — ALREADY REGISTERED by `remark-math`, which must run before this plugin — build the
 * standard `math` node with no bridge of our own. Downstream, `rehype-katex` cannot tell the
 * difference between an equation that arrived in brackets and one that arrived in dollars. That is
 * the whole point: one notation, one node, one renderer.
 *
 * DELIBERATE LIMITS. The construct recognises `\[` and `\]` ONLY when each stands alone on its own
 * line (trailing whitespace allowed) — LaTeX's own display convention and pandoc's reading of it.
 * An unterminated `\[` fails the construct and stays literal text rather than swallowing the rest
 * of the document. It touches nothing else: `$$ … $$` is parsed by `remark-math` before this runs,
 * single-`$` currency/math discrimination is decided afterwards by `remarkInlineMathDollars.mjs`
 * and never sees these bytes (they are a `math` node by then), and a `\[` inside a code fence or an
 * indented code block is unreachable because those constructs win at the same position. Inline
 * `\( … \)` is NOT handled here; it is a separate notation and a separate decision.
 *
 * NO IMPORTS ON PURPOSE. micromark's helpers are not declared dependencies of this package (they
 * arrive transitively under `remark-math`), so the two predicates and the four character codes this
 * construct needs are inlined from `micromark-util-symbol` / `micromark-util-character` rather than
 * reached for across an undeclared edge.
 */

/* micromark character codes (micromark-util-symbol/lib/codes.js). */
const EOF = null;
const BACKSLASH = 92;         // \
const LEFT_BRACKET = 91;      // [
const RIGHT_BRACKET = 93;     // ]

/* micromark-util-character, inlined. Line endings are the negative codes below -2; a markdown space
 * is a real space, a horizontal tab, or micromark's virtual space. */
const isLineEnding = (code) => code !== EOF && code < -2;
const isSpace = (code) => code === -2 || code === -1 || code === 32;

/** The line after a line ending must not be a LAZY continuation of an enclosing container. */
const nonLazyContinuation = { tokenize: tokenizeNonLazyContinuation, partial: true };

function tokenizeNonLazyContinuation(effects, ok, nok) {
  const self = this;
  return start;

  function start(code) {
    if (code === EOF) return nok(code);
    effects.enter('lineEnding');
    effects.consume(code);
    effects.exit('lineEnding');
    return lineStart;
  }

  function lineStart(code) {
    return self.parser.lazy[self.now().line] ? nok(code) : ok(code);
  }
}

/** Consume run-of-the-mill trailing spaces/tabs into `type`, then continue at `next`. */
function spaceRun(effects, next, type) {
  return function start(code) {
    if (!isSpace(code)) return next(code);
    effects.enter(type);
    return inside(code);
  };

  function inside(code) {
    if (isSpace(code)) {
      effects.consume(code);
      return inside;
    }
    effects.exit(type);
    return next(code);
  }
}

/**
 * The flow construct. `concrete: true` matches `mathFlow`: once open, the block's content is not
 * reinterpreted by enclosing containers.
 */
export const displayMathBracketsConstruct = {
  name: 'displayMathBrackets',
  tokenize: tokenizeDisplayMathBrackets,
  concrete: true,
};

function tokenizeDisplayMathBrackets(effects, ok, nok) {
  const self = this;

  return start;

  /* `\` at the start of a flow line. */
  function start(code) {
    if (code !== BACKSLASH) return nok(code);
    effects.enter('mathFlow');
    effects.enter('mathFlowFence');
    effects.enter('mathFlowFenceSequence');
    effects.consume(code);
    return openingBracket;
  }

  function openingBracket(code) {
    if (code !== LEFT_BRACKET) return nok(code);
    effects.consume(code);
    effects.exit('mathFlowFenceSequence');
    return spaceRun(effects, afterOpeningFence, 'whitespace');
  }

  /* Nothing but whitespace may follow `\[` on its line. */
  function afterOpeningFence(code) {
    if (!isLineEnding(code)) return nok(code);
    effects.exit('mathFlowFence');
    return effects.attempt(nonLazyContinuation, atLineStart, nok)(code);
  }

  /* At the start of a content line — it may be the closing fence. */
  function atLineStart(code) {
    return effects.attempt(
      { tokenize: tokenizeClosingFence, partial: true },
      after,
      contentStart,
    )(code);
  }

  function contentStart(code) {
    // EOF with no `\]`: not display math. Unwind and leave the bytes as prose.
    if (code === EOF) return nok(code);
    if (isLineEnding(code)) {
      return effects.attempt(nonLazyContinuation, atLineStart, nok)(code);
    }
    effects.enter('mathFlowValue');
    return contentChunk(code);
  }

  function contentChunk(code) {
    if (code === EOF || isLineEnding(code)) {
      effects.exit('mathFlowValue');
      return contentStart(code);
    }
    effects.consume(code);
    return contentChunk;
  }

  function after(code) {
    effects.exit('mathFlow');
    return ok(code);
  }

  /* `\]` alone on its line, after at most the usual three spaces of indent. */
  function tokenizeClosingFence(effects, ok, nok) {
    return spaceRun(effects, beforeSequence, 'linePrefix');

    function beforeSequence(code) {
      if (code !== BACKSLASH) return nok(code);
      effects.enter('mathFlowFence');
      effects.enter('mathFlowFenceSequence');
      effects.consume(code);
      return closingBracket;
    }

    function closingBracket(code) {
      if (code !== RIGHT_BRACKET) return nok(code);
      effects.consume(code);
      effects.exit('mathFlowFenceSequence');
      return spaceRun(effects, afterSequence, 'whitespace');
    }

    function afterSequence(code) {
      if (code !== EOF && !isLineEnding(code)) return nok(code);
      effects.exit('mathFlowFence');
      return ok(code);
    }
  }
}

/** The micromark extension: one flow construct, keyed on `\`. */
export const displayMathBracketsSyntax = () => ({
  flow: { [BACKSLASH]: displayMathBracketsConstruct },
});

/**
 * The remark plugin. Registers the syntax only — the mdast bridge is `remark-math`'s, which is why
 * this MUST be listed after `remark-math` in `markdown.remarkPlugins`. That ordering is asserted
 * here rather than trusted, because getting it wrong is the silent kind of wrong: micromark would
 * emit `mathFlow` tokens that nothing turns into a node, and the equations would vanish from the
 * page entirely instead of erroring.
 */
export default function remarkDisplayMathBrackets() {
  const data = this.data();

  const bridged = (data.fromMarkdownExtensions || []).flat().some(
    (extension) => extension && extension.exit && extension.exit.mathFlow,
  );
  if (!bridged) {
    throw new Error(
      'remarkDisplayMathBrackets: no `mathFlow` fromMarkdown handler is registered. This plugin ' +
      'emits micromark-extension-math\'s own token names and relies on mdast-util-math to build ' +
      'the `math` node, so `remark-math` must be applied BEFORE it in markdown.remarkPlugins.',
    );
  }

  (data.micromarkExtensions || (data.micromarkExtensions = [])).push(
    displayMathBracketsSyntax(),
  );
}

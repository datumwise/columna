// CP-3b Tier-1 [AI-3] — the term-chip fills. ONE source, no drift: every field is quoted from the
// ratified "What is Columna?" front-door glossary + body (specs/context/what_is_columna_draft_v0_7.md,
// wired verbatim at /what-is-columna). The chip renders the package §1c [AI-3] template:
//   "In Columna, {TERM} means: {DEFINITION}. The surrounding law: {RULE}. Example: {EXAMPLE}.
//    Explain {TERM} to me in plain language and answer my follow-up questions."
export interface GlossTerm {
  term: string;
  definition: string;
  rule: string;
  example: string;
}

// The glossary anchor on /what-is-columna (Astro slugs the "Small glossary" heading).
export const GLOSSARY_ANCHOR = '/what-is-columna#small-glossary';

export const GLOSSARY: Record<string, GlossTerm> = {
  universe: {
    term: 'Universe',
    definition: 'one population of facts (transactions; store-days)',
    rule: 'every expression evaluates inside exactly one universe',
    example: 'transactions is one universe and store-days is another, so a measure over transactions never silently borrows rows from store-days',
  },
  basis: {
    term: 'Basis',
    definition: 'what a missing row means in a universe',
    rule: 'it is a real zero (event streams), a gap (a grid with a hole in it), or a membership fact (a registry)',
    example: 'in an event stream a missing row is a real zero, but in a spine grid the same absence is a gap, not a zero',
  },
  'four-moods': {
    term: 'the four moods',
    definition: 'every answer comes back in one of four moods — serve, disclose, clarify, refuse',
    rule: 'every answer is a pair — the result and its context — so whoever is asking always knows what they are standing on',
    example: 'asking for inventory by customer returns refuse, because inventory does not have customers',
  },
  frameql: {
    term: 'FrameQL',
    definition: 'the query language against the Manifold, as SQL is to tables',
    // Synced to the v0.5 envelope spelling (the terse `aov @ cal.month` output form is RETIRED; @ is
    // now the input-anchor marker, the output grain rides AT). Huayin's conformance note — flagged, not silent.
    rule: 'you declare the frame you want — the columns, and the anchor they stand at',
    example: '`SELECT aov AT {cal.month}` — the frame whose column is aov, standing at calendar month',
  },
  verdict: {
    term: 'Verdict',
    definition: 'the result of checking a described claim against the data',
    rule: 'it is one of verified, corroborated, untestable, or contradicted',
    example: 'every measure in the Explorer carries the verdict from testing its definition against the data',
  },
};

// The ordered set the positional pages carry (package §2c: Universe · Basis · four moods · FrameQL · Verdict).
export const POSITIONAL_TERMS = ['universe', 'basis', 'four-moods', 'frameql', 'verdict'] as const;

export function askText(t: GlossTerm): string {
  return `In Columna, ${t.term} means: ${t.definition}. The surrounding law: ${t.rule}. Example: ${t.example}. Explain ${t.term} to me in plain language and answer my follow-up questions.`;
}

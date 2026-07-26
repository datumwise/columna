#!/usr/bin/env python3
"""
gen_grammar.py — the SHIPPED GRAMMAR REFERENCE, generated from columna-core so it cannot drift.

Built on Huayin's ruling of 2026-07-26 (the ATTR question), which resolved a category error worth
recording at the top of this file:

    A LEXING SET IS NOT A GRAMMAR TAXONOMY.

`parser._KW` is the set of tokens that may BEGIN A LINE. It is the right source for "is nothing
missing?" and the WRONG source for page structure: `ATTR` is in `_KW` but is an inline clause of
`LEVEL`, so a page structured from `_KW` would present it as a false peer of `MEASURE` — faithful to
the parser, misleading to a reader. Generated-from-source inherits the source's shape, INCLUDING
where that shape is not the teaching shape.

So this generator derives its three properties from three different artifacts, deliberately:

  1. STRUCTURE  ← the parser's MODULE DOCSTRING grammar block, which is already in teaching shape
                  (statements at top level; inline clauses nested under their parent — ATTR under
                  LEVEL, M_ANCHOR/FAMILY/BLOCKED/ORDER under MEASURE). A hand-curated grammar summary
                  maintained beside the code is exactly what a reference wants.
  2. EXAMPLES   ← executed against the shipped parser. Every example on the page must parse, and this
                  script EXITS NON-ZERO if any does not. Has-to-be-loud, applied to documentation:
                  nothing in CI ever read Chapter 26's examples, which is why they rotted.
  3. COMPLETENESS ← `_KW`. Every token must appear on the page, as a statement OR an inline clause,
                  or the build fails. A newly added keyword cannot go silently undocumented, while
                  ATTR still appears in its true role rather than as a false peer.

DOCSTRING GAP (found on the first run, 2026-07-26): `ASSERT` is in `_KW` but ABSENT from the
docstring's grammar block — 8 of 9 tokens are present. The completeness assertion caught it
immediately, which is the assertion working. Rather than fail forever on a package-side omission, a
token may be covered by SUPPLEMENT below: an explicit, visible, auditable entry. The guarantee holds
because a token in neither the docstring nor the supplement still fails the build; the supplement is
a declared exception, not a silent one. The upstream fix (add ASSERT to the docstring) is rowed.

Usage:  python scripts/gen_grammar.py > src/data/grammar.generated.json
"""
from __future__ import annotations

import inspect
import json
import re
import sys
from importlib.metadata import version

import columna_core.parser as parser


class Fail(Exception):
    """Fails closed: the page is never generated from a source it could not verify."""


# ── 1 · STRUCTURE — from the docstring's grammar block (teaching shape) ────────────────────────────
def grammar_block() -> str:
    doc = parser.__doc__ or ""
    i = doc.find("Grammar (")
    if i == -1:
        raise Fail("the parser's module docstring has no 'Grammar (' block — this generator derives "
                   "its STRUCTURE from that block (a lexing set is not a grammar taxonomy). Either "
                   "the docstring was reorganised or the module changed; re-point the generator.")
    return doc[i:].rstrip()


def parse_structure(block: str):
    """Read the block into statements with their nested inline clauses.

    Teaching shape is carried by INDENTATION in the docstring: a statement sits at the block's base
    indent; a deeper line is an inline clause of the statement above it. We preserve that rather than
    re-deriving a taxonomy of our own.
    """
    lines = [l for l in block.splitlines()[1:] if l.strip()]
    if not lines:
        raise Fail("the docstring's grammar block is empty")
    base = min(len(l) - len(l.lstrip()) for l in lines)
    out, current = [], None
    for l in lines:
        indent, text = len(l) - len(l.lstrip()), l.strip()
        kw = re.match(r"([A-Z_]+)\b", text)
        if indent == base and kw:
            current = {"keyword": kw.group(1), "signatures": [text], "clauses": [], "notes": []}
            out.append(current)
        elif indent == base and not kw:
            # a prose line at base indent (e.g. "Any declaration may carry (case-demo b/d):")
            current = None
            out.append({"keyword": None, "signatures": [], "clauses": [], "notes": [text]})
        elif current is not None:
            k2 = re.match(r"\[?([A-Z_]+)\b", text)
            (current["clauses"] if k2 else current["notes"]).append(text)
        else:
            # deeper line under a prose heading — a shared clause (DESCRIPTION / REJECT)
            if out and out[-1]["keyword"] is None:
                out[-1]["notes"].append(text)
    # merge repeated keywords (MEASURE has two signature forms)
    merged: dict[str, dict] = {}
    order: list = []
    for e in out:
        k = e["keyword"]
        if k is None:
            order.append(e); continue
        if k in merged:
            merged[k]["signatures"] += e["signatures"]
            merged[k]["clauses"] += e["clauses"]
            merged[k]["notes"] += e["notes"]
        else:
            merged[k] = e; order.append(e)
    return order


# ── 3 · COMPLETENESS — from _KW, the lexing set (the RIGHT use for it) ────────────────────────────
def kw_tokens() -> list[str]:
    src = inspect.getsource(parser)
    m = re.search(r"_KW\s*=\s*\((.*?)\)", src, re.S)
    if not m:
        raise Fail("could not read _KW from the parser — the completeness assertion has no source")
    return re.findall(r'"(\w+)"', m.group(1))


# A token the docstring's grammar block does not carry, documented here EXPLICITLY so it is visible
# and auditable. Adding a token here is a deliberate, reviewable act; omitting it entirely still
# fails the build.
SUPPLEMENT = {
    "ASSERT": {
        "keyword": "ASSERT",
        "signatures": [
            'ASSERT <name> [ON <universe>] WHERE <predicate>',
            'ASSERT <name> [ON <universe>] AT <level> HOLDS <invariant>',
        ],
        "clauses": [],
        "notes": [
            "Absent from the parser docstring's grammar block (8 of 9 _KW tokens are present); "
            "signatures read from the parser's own patterns. The upstream fix — adding ASSERT to that "
            "block — is rowed, and this supplement is what keeps the page complete meanwhile.",
        ],
        "supplemented": True,
    },
}

# ── MAP-SIDE CLAUSES (§2b / C-2). Labelled, because this is where a reader forms the wrong model ──
# The architecture is NOT "physical binding is part of the declaration" — it is the opposite, and the
# code enforces it: describe emits LOGICAL names only (no realized_by, no VIA bridge, no FROM table,
# no expression), and a standing insulation test asserts physical identifiers never cross describe or
# the wire. A .cml document CO-LOCATES two layers; only one of them is visible to an agent.
MAP_CLAUSES = ["= <column>", "FROM", "AS", "VALUE", "VIA", "REJECT", "ATTR"]

FRAME = {
    "law": "§2b / C-2 insulation",
    "statement": (
        "A .cml source document co-locates TWO layers. The LOGICAL declarations are what the Manifold "
        "is — what an agent sees over describe and the wire. The MAP clauses are how it binds to "
        "physical storage, and they are engine-visible ONLY: describe emits logical names, never a "
        "realized_by, a VIA bridge, a FROM table, or an expression. This is enforced, not intended — "
        "a standing insulation test asserts that physical identifiers never cross describe or the wire."
    ),
    "map_clauses": MAP_CLAUSES,
}

# ── 2 · EXAMPLES — every one executed against the shipped parser ──────────────────────────────────
# Each example is a COMPLETE, VALID document, not a fragment: the probe's failure was a whole
# document the parser rejected, so a page of fragments would not have caught it. (The first draft of
# these examples had a standalone UNIVERSE with no LEVELs — the verifier rejected it, which is the
# verifier doing its job on its own author.)
_BASE = ("MANIFOLD demo VERSION 1\n"
         "UNIVERSE sales = store * day\n"
         "LEVEL store = store_id BASE\n"
         "LEVEL day = day BASE\n")

EXAMPLES = [
    ("MANIFOLD", "the document header — a name and a version (both required)",
     _BASE),
    ("UNIVERSE", "a population: the product of its base dimensions",
     _BASE),
    ("LEVEL", "a coordinate. The `= <column>` is a MAP clause — engine-side, never crosses describe",
     _BASE),
    ("LEVEL", "with an inline ATTR clause — also map-side (note ATTR is a CLAUSE of LEVEL, not a statement)",
     _BASE + "LEVEL region = region ATTR name = stores.region_name\n"),
    ("HIERARCHY", "a functional roll-up lineage; braces required, and each hop carries its own VIA",
     _BASE + "LEVEL region = region\n"
     "HIERARCHY location { store -> region VIA stores(store_id, region) }\n"),
    ("MEASURE", "a quantity, aggregated. `FROM <table> AS <agg>(<expr>)` is a MAP clause",
     _BASE + "MEASURE revenue ON sales FROM tx AS sum(amount)\n"),
    ("DERIVED", "a quantity defined from other measures — no map clause; it is pure logic",
     _BASE + "MEASURE revenue ON sales FROM tx AS sum(amount)\n"
     "MEASURE orders ON sales FROM tx AS distinct(order_id)\n"
     "DERIVED aov = revenue / orders\n"),
]


def verify_examples():
    """Execute every example. A page whose examples do not parse is worse than no page."""
    ok, failures = [], []
    for kw, gloss, src in EXAMPLES:
        try:
            parser.parse_manifold(src)
            ok.append({"keyword": kw, "gloss": gloss, "source": src})
        except Exception as e:
            failures.append(f"  [{kw}] {gloss}\n      {type(e).__name__}: {e}")
    if failures:
        raise Fail("grammar-page examples DO NOT PARSE against the shipped package — the page is not "
                   "generated. Fix the example or the page; never ship documentation the parser "
                   "rejects:\n" + "\n".join(failures))
    return ok


def main() -> int:
    try:
        block = grammar_block()
        entries = parse_structure(block)
        tokens = kw_tokens()

        # A token counts as documented if it appears ANYWHERE the reader will see it: as a statement
        # keyword, inside a statement's SIGNATURE (this is ATTR's true home — inline in LEVEL's
        # signature, not a peer statement), as a nested clause, or in a shared note.
        documented = {e["keyword"] for e in entries if e["keyword"]}
        for e in entries:
            for text in e["signatures"] + e["clauses"]:
                for m in re.finditer(r"\b([A-Z_]{2,})\b", text):
                    documented.add(m.group(1))
        # inline clauses named in shared notes (DESCRIPTION / REJECT) count as documented too
        for e in entries:
            for n in e["notes"]:
                for m in re.finditer(r"\b([A-Z_]{3,})\b", n):
                    documented.add(m.group(1))

        supplemented = []
        missing = []
        for t in tokens:
            if t in documented:
                continue
            if t in SUPPLEMENT:
                supplemented.append(SUPPLEMENT[t]); documented.add(t)
            else:
                missing.append(t)
        if missing:
            raise Fail(
                "COMPLETENESS ASSERTION FAILED — these tokens are in the parser's _KW but appear "
                f"nowhere on the page: {missing}. A keyword must not be silently undocumented. Either "
                "add it to the parser docstring's grammar block (preferred — that is the teaching-shape "
                "source), or add an explicit entry to SUPPLEMENT in this generator with a note saying "
                "why.")

        examples = verify_examples()
        out = {
            "generated_by": f"columna-core {version('columna-core')}",
            "structure_source": "columna_core.parser.__doc__ grammar block (teaching shape)",
            "completeness_source": "columna_core.parser._KW (lexing set)",
            "note": ("A lexing set is not a grammar taxonomy: _KW says what may BEGIN A LINE and is "
                     "used here only to assert coverage; the page's SHAPE comes from the docstring."),
            "frame": FRAME,
            "kw_tokens": tokens,
            "entries": [e for e in entries] + supplemented,
            "supplemented": [s["keyword"] for s in supplemented],
            "examples": examples,
            "raw_block": block,
        }
        json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
        return 0
    except Fail as e:
        print(f"grammar generation FAILED (fails closed): {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
columna_core.expr — the Frame-QL 1.0 EXPRESSION grammar (specification §15), native.

WHY THIS MODULE EXISTS. Frame-QL's expression dialect has been HOSTED on CPython's `ast` since the
first build. That was always an implementation choice rather than a fact about the language, and the
P1-26 ruling (planner.py:27-42) already named the cost: a language that hands its text to another
language's parser answers in that other language's voice — `count(*)` refused as "Invalid star
expression", `revenue[region = "east"]` refused with "Maybe you meant '==' or ':=' instead of '='?".
P1-26 built a wall (`_parse_expr`) so the substrate's diagnostics stop at one crossing point. This
module removes the need for the wall: it parses Frame-QL 1.0 expressions directly, in Frame-QL's own
grammar, with Frame-QL's own error channel.

    No `ast`. No `eval`. No `compile`. No raw Python exception ever escapes `parse()`.

SCOPE. This module is PURELY SYNTACTIC. It produces an IR and nothing else. It resolves no name,
consults no registry, knows no manifold, and decides no type. Everything §15 defers — governed-name
versus value-member resolution (§15.1), whether a subscript key type is admitted (§7.5), whether a
tuple is a physical value or an ordering specification (§15.3), whether a called capability exists at
all (§15.2) — is a LATER concern and is deliberately left undone here. Where the parser must record
something for the resolver to act on, it records SHAPE, never a verdict.

────────────────────────────────────────────────────────────────────────────────────────────────────
THE PRECEDENCE LADDER (§15, verbatim order; tightest first)
────────────────────────────────────────────────────────────────────────────────────────────────────

    primary             literal | bare/governed dotted path | `( … )` | tuple | `{ … }` grain
    postfix             f(...) | .member | .method(...) | [key]          left-assoc, tightest
    anchor ascription   E @ {A}                                          left-assoc
    numeric unary       +E   -E
    multiplicative      *  /  %                                          left-assoc
    additive            +  -                                             left-assoc
    comparison          =  !=  <  <=  >  >=  IN  BETWEEN                 NON-associative
    logical             NOT (tightest) → AND → OR                        AND/OR left-assoc, n-ary

There is one parser function per rung, named after it, so the ladder can be read off the code.

Two consequences the ladder alone is easy to misread, both of which §15 states outright and both of
which differ from CPython's table (this is the ONLY place the two grammars disagree on shape):

  · `@` binds TIGHTER than arithmetic.   `revenue / orders @ {customer}`  ≡  `revenue / (orders @ {customer})`
    (CPython puts `@` at the same rung as `*` and `/`, left-associative, so it reads the same text as
    `(revenue / orders) @ {customer}`.)
  · `@` binds TIGHTER than numeric unary. `-a @ b` ≡ `-(a @ b)`
    (CPython binds unary tighter than `@`, so it reads `(-a) @ b`.)

Postfix binds tighter than `@` (`state.cardinality @ {account}` ≡ `(state.cardinality) @ {account}`),
and parentheses are the only way to get the other grouping (`(state @ {account}).cardinality`).

────────────────────────────────────────────────────────────────────────────────────────────────────
THE `=` / `:` RULE AND THE HISTORICAL `name = value` SPELLING  (§15.2)
────────────────────────────────────────────────────────────────────────────────────────────────────

§15.2 closes the general grammar blocker with one sentence — **`=` compares, `:` names an argument**
— and adds that the distinction "is syntactic and does not depend on the called function's registry
entry". It then ALSO says that historical `name = value` call spellings "may remain compatibility
input" and "canonicalize to colon form". Those two statements are in tension: `f(by = cal.day)` must
become a named argument while `if(region = "east", 1, 0)` must stay a comparison, and in both the
left side is a bare identifier immediately followed by `=`.

A left-hand-side test cannot separate them (`by` and `region` are both bare identifiers), and neither
can a right-hand-side test (`cal.day` is a path, but `window = 7` and `region = "east"` are both
literals). What DOES separate them is the other rule §15.2 states in the same breath:

    "Positional arguments must precede named arguments."

`if(region = "east", 1, 0)` has two positional arguments AFTER the `=` form, so the named reading is
structurally impossible there; `f(by = cal.day)` and `cumsum(revenue, by = cal.day, within =
{customer})` have nothing but named arguments after theirs. That is the discriminator, it is purely
syntactic, and it is registry-independent — exactly what §15.2 demands.

    THE RULE, stated:

    (1) Every `=` parses as a COMPARISON. There is no second meaning of `=` in the grammar.
    (2) In CALL-ARGUMENT position, an argument is NAMED-SHAPED if it is written `name: value`, or if
        its parse is exactly `Compare("=", Path(<one segment>), value)` — a bare, undotted identifier
        on the left of a top-level `=`.
    (3) The named arguments of a call are its longest TRAILING run of named-shaped arguments. Every
        named-shaped argument inside that run canonicalizes to the SAME `NamedArg` node, whichever
        spelling was used: `by = cal.day` and `by: cal.day` are indistinguishable after parsing.
    (4) Any other `=` — including a named-shaped argument that is followed by a positional one —
        remains the `Compare` it parsed as.
    (5) A `name: value` argument that is NOT in the trailing run is a hard error: positional operands
        must precede named parameters. (A `name = value` argument outside the run is not an error; by
        rule (4) it is simply the comparison it already was.)
    (6) ESCAPE HATCH. To force the comparison reading in trailing position, either parenthesize the
        argument — `f(a, (b = c))` — or write the unambiguous `==`: `f(a, b == c)`. The named
        reading requires a top-level, unparenthesized, single-`=` comparison.

    Worked against §15.2's own examples:
        variance(price, ddof: 1)                       → 1 positional, 1 named        ✓
        lag(revenue, 2, step: cal.year)                → 2 positional, 1 named        ✓
        cumsum(revenue, by: cal.day, within: {customer}) → 1 positional, 2 named      ✓
        if(region = "east", 1, 0)                      → 3 positional; arg 1 Compare  ✓
        f(by = cal.day) / f(window = 7)                → 1 named (trailing)           ✓

    WHAT THIS MODULE DOES NOT DO. §15.2 admits the historical spelling "only inside a governed
    capability that actually exists". Whether the capability exists, and whether it declares a
    parameter of that name, is a RESOLVER question. The parser normalizes the spelling; it does not
    grant the capability. `NamedArg.historical` records which spelling was written so a resolver can
    apply that gate (and a linter can nudge toward the colon), without affecting node identity.

────────────────────────────────────────────────────────────────────────────────────────────────────
BRACES: `*` MEANS TWO THINGS, AND THE GRAMMAR NEVER GUESSES WHICH  (§15.0)
────────────────────────────────────────────────────────────────────────────────────────────────────

Inside `{ … }`, `*` is anchor common-refinement, so `{customer * cal.month}` is a COMPOSITE grain of
two levels and never a multiplication. Outside braces `*` is ordinary multiplication. The brace is
the switch, so no type information is ever needed to pick the reading. A brace group contains dotted
LEVEL NAMES only, separated by `*` (canonical) or `,` (accepted sugar, as the shipped anchor parser
already accepts); `{}` is the empty product — the Manifold-wide scalar — and is a DECLARED grain, not
a missing one. `@ level` and `@ (a, b)` are also accepted pin sugars, matching `Planner._canon_expr`.

A brace group may also stand alone as a primary (`within: {customer}`, §15.2's own example); that is
an `Anchor` with `base=None` — a grain literal rather than an ascription.

────────────────────────────────────────────────────────────────────────────────────────────────────
BRACKETS ARE SUBSCRIPTION, NEVER FILTERING  (§15.4, §7.5)
────────────────────────────────────────────────────────────────────────────────────────────────────

`E[key]` subscribes into a semantic value and nests (`E[i][j]`). §7.5 is explicit that
`revenue[region = "east"]` "parses, if at all, only as subscription by the Boolean result of
`region = "east"`" and is then a TYPE error unless the type admits Boolean subscription — and that a
conforming diagnostic "should point the writer toward `WHERE` or `HAVING`". So it PARSES here, as
`Subscript(Path(revenue), Compare("=", …))`, and this module offers `filter_shaped_subscripts()` so
the resolver can find those nodes and say the right sentence. Finding them is not judging them: the
helper reports shape and takes no position on whether the type admits the key.

────────────────────────────────────────────────────────────────────────────────────────────────────
UNPARSING — TWO DIALECTS, ONE TREE
────────────────────────────────────────────────────────────────────────────────────────────────────

Canonical column keys ARE the expression text (`Planner._default_name`; WP-NAME-1), and those keys
are WIRE-VISIBLE. `ast.unparse` is also the source of reader-facing refusal text at fourteen sites in
the planner. `unparse()` inherits both jobs, so it renders in one of two dialects:

  CANONICAL (default) — Frame-QL 1.0 canonical spelling. Anchors brace-formed (`E @ {a*b}`, `E @ {}`),
      named arguments colon-formed (`ddof: 1`), `=` for comparison, parenthesization driven by the
      §15 ladder above. This is the form §15 prescribes and the form `Planner._canon_expr` already
      normalizes anchors into today.

  HOST — the spelling CPython's `ast.unparse` produces for the SAME expression, i.e. anchors as the
      planner's `_convert_input_anchor` writes them (`E @ day`, `E @ (a, b)`, `E @ ()`), named
      arguments as keywords (`ddof=1`), and CPython's precedence table for parenthesization. This
      exists so phase-2 migration can replace `ast.unparse` at those fourteen sites and at the column
      -key path with BYTE-IDENTICAL output — a language change that is not also a wire change.

  The two dialects differ only in: anchor spelling, named-argument spelling, the `Member`-versus-
  dotted-`Path` distinction (see below), and the `@`/unary rungs of the precedence table. Everything
  else — number and string rendering (Python `repr`, matching `ast.unparse`), tuple spelling, call
  spelling, operator spacing — is identical by construction.

  HOST IS NOT DEFINED FOR THE 1.0-ONLY NODE SET. `Compare`, `Logical` and a `NOT`/`IN`/`BETWEEN`
  operator have no CPython-`ast` counterpart the old dialect ever accepted (`Planner._ALLOWED` admits
  no `ast.Compare` and no `ast.BoolOp`), so in HOST they render in their canonical 1.0 spelling.
  There is nothing to be byte-identical TO.

  §15.1 AND THE `Member` NODE. `a.b.c` is ONE dotted-path shape (`Path`), because resolution of which
  prefix is a governed name is a later semantic check. `(a.b).c` is `Member(Path(a, b), "c")` — §15.1
  says parentheses "make ordinary grouping/chaining explicit", which is a different written intent,
  so CANONICAL preserves the parentheses. HOST drops them (`a.b.c`), because CPython's `ast` has only
  `Attribute` and `ast.unparse` cannot spell the distinction either.

────────────────────────────────────────────────────────────────────────────────────────────────────
WHAT §15 LEAVES OPEN, AND WHAT THIS PARSER CHOSE  (each is a resolver/ruling question, not a parse one)
────────────────────────────────────────────────────────────────────────────────────────────────────

  · `BETWEEN` appears in §15's ladder and nowhere else in the specification — no operand form is
    given. Implemented SQL-conventionally as `E BETWEEN lo AND hi`, with that `AND` consumed by
    BETWEEN itself (it is a delimiter, not a conjunction), yielding `Compare("BETWEEN", E, Tuple(lo,
    hi))`. A future ruling may prefer `E BETWEEN (lo, hi)`; the node shape is already that.
  · `NOT IN` / `NOT BETWEEN` are not in §15. They are refused, by name, pointing at `NOT a IN b`
    (which parses, because comparison binds tighter than `NOT`).
  · `IN`'s right operand form is not given either. It is parsed as one ordinary expression, so
    `day IN (a, b)` is a tuple but `day IN ('x')` is a SCALAR — parentheses group, and §15.3 makes
    the comma, not the parenthesis, what builds a tuple. A resolver that means SQL's `IN` must
    therefore treat a scalar right operand as a one-element membership set, or require `('x',)`.
    Both readings are defensible; the parser does not pick one.
  · Comparison CHAINING (`a < b < c`) is not addressed. Refused as non-associative rather than given
    either of Python's or SQL's readings without a ruling.
  · Whether a bare `{ … }` grain literal is admissible in a given argument position is a typing
    question §15.2/§15.3 leave to the parameter's semantic contract; it always parses.
  · `==` is accepted as compatibility input for `=` (the shipped `Planner._CMP` accepts both) and
    canonicalizes to `=`. This is spelling only: comparisons never reached the old `ast` dialect.

────────────────────────────────────────────────────────────────────────────────────────────────────
ERRORS
────────────────────────────────────────────────────────────────────────────────────────────────────

Every rejection is `FrameQLSyntaxError` — the language's own channel, the one the server already
turns into a `frameql_syntax` wire error — carrying `.offset` (source offset of the token at fault)
and `.source`. Messages follow the envelope's four-mood temperament: say what is wrong, then name the
remedy, with an `e.g.`. `parse()` has a final blanket guard so that a defect in THIS module surfaces
as a Frame-QL error too: the P1-26 guarantee is that nothing else ever escapes, and it is not made
conditional on this parser being bug-free.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable, NamedTuple, Optional, Sequence

# `_WORD` is the envelope's identifier shape. Imported rather than re-spelled so an identifier means
# exactly the same thing in the envelope grammar and the expression grammar (one dialect, §2).
from .envelope import _WORD
from .frameql import FrameQLSyntaxError

__all__ = [
    "parse", "tokenize", "unparse", "CANONICAL", "HOST",
    "FrameQLSyntaxError", "Token", "Node",
    "Literal", "Path", "Member", "Subscript", "Call", "NamedArg", "Anchor",
    "Unary", "Binary", "Compare", "Logical", "Tuple",
    "walk", "filter_shaped_subscripts",
]

CANONICAL = "canonical"
HOST = "host"

#: Depth beyond which the expression is refused rather than risking a RecursionError. Well past
#: anything a human writes; present so a pathological input is a Frame-QL refusal, not a crash.
#:
#: It bounds the DEPTH OF THE TREE, not merely the recursion that builds it — see `_grow`. For a
#: while it bounded only the latter, which read as a guarantee and was not one: the left-associative
#: loops balance their `_enter`/`_leave` per iteration, so `a + a + a + …` built an unbounded left
#: spine and reached `unparse` and the planner's walks — ordinary recursive functions — as a raw
#: `RecursionError`, the one exception class this module promises can never escape.
MAX_DEPTH = 100


# ═══ errors ══════════════════════════════════════════════════════════════════════════════════════

def _fail(message: str, pos: int, source: str):
    """Raise the language's own syntax error, carrying the source offset.

    `message` is expected to be written in the envelope's temperament: the fault, an em-dash, the
    remedy, and where useful an `e.g.`.
    """
    err = FrameQLSyntaxError(f"{message} (at offset {pos} in {source!r})")
    err.offset = pos
    err.source = source
    raise err


# ═══ 1. tokenizer ════════════════════════════════════════════════════════════════════════════════

#: The §15 keywords. Case-insensitive to match; the token keeps the source spelling.
KEYWORDS = frozenset({"IN", "BETWEEN", "NOT", "AND", "OR"})

#: Integer or float. A leading digit is REQUIRED: `.5` would be indistinguishable from a `.member`
#: access on whatever precedes it, and §15 has no use for the spelling.
_NUMBER = re.compile(r"\d+\.\d*(?:[eE][+-]?\d+)?|\d+(?:[eE][+-]?\d+)?")

#: Two-character operators must be tried before one-character ones (`!=` before `!`, `<=` before `<`).
_OPERATORS_2 = ("!=", "<=", ">=", "==")
_OPERATORS_1 = "@{}[](),.:=<>+-*/%"

_ESCAPES = {"\\": "\\", "'": "'", '"': '"', "n": "\n", "t": "\t", "r": "\r", "0": "\0"}

#: Bracket pairs, for the balance check over the token stream.
_CLOSERS = {"(": ")", "[": "]", "{": "}"}


@dataclass(frozen=True, slots=True)
class Token:
    """One lexical token. `pos` is the offset of its first character in the source text — every
    token carries one so that every rejection can say WHERE."""

    kind: str            # "name" | "keyword" | "number" | "string" | "op" | "end"
    text: str            # the source spelling, verbatim (keywords keep their written case)
    pos: int
    value: Any = None    # the decoded value, for "number" and "string" only

    def __repr__(self) -> str:
        return f"Token({self.kind}, {self.text!r}@{self.pos})"


def tokenize(source: str) -> list[Token]:
    """Frame-QL 1.0 expression text → tokens, ending with a single `end` token.

    Raises `FrameQLSyntaxError` (never a Python exception) on an unreadable character, an
    unterminated string, or a string broken across a newline.
    """
    if not isinstance(source, str):
        _fail("an expression must be text — Frame-QL has nothing to read here", 0, repr(source))

    out: list[Token] = []
    i, n = 0, len(source)
    while i < n:
        ch = source[i]

        if ch.isspace():                               # whitespace is not significant in an expression
            i += 1
            continue

        if ch in "'\"":                                # string literal, in BOTH quote styles (§15.2)
            tok, i = _lex_string(source, i)
            out.append(tok)
            continue

        if ch.isdigit():
            m = _NUMBER.match(source, i)
            raw = m.group(0)
            value = float(raw) if ("." in raw or "e" in raw or "E" in raw) else int(raw)
            out.append(Token("number", raw, i, value))
            i = m.end()
            continue

        if (m := _WORD.match(source, i)):
            word = m.group(0)
            kind = "keyword" if word.upper() in KEYWORDS else "name"
            out.append(Token(kind, word, i))
            i = m.end()
            continue

        two = source[i:i + 2]
        if two in _OPERATORS_2:
            out.append(Token("op", two, i))
            i += 2
            continue

        if ch in _OPERATORS_1:
            out.append(Token("op", ch, i))
            i += 1
            continue

        _fail(f"{ch!r} is not part of any Frame-QL expression — remove it, or quote it if it "
              f"belongs inside a string, e.g. region = 'east'", i, source)

    out.append(Token("end", "", n))
    _check_balance(out, source)
    return out


def _lex_string(source: str, start: int) -> tuple[Token, int]:
    """Lex a single- or double-quoted string. Both quote styles mean the same thing (§15.2 writes
    `region = "east"`; the shipped corpus writes `region = 'east'`)."""
    quote = source[start]
    buf: list[str] = []
    i = start + 1
    while True:
        if i >= len(source):
            _fail(f"this string is never closed — add the matching {quote}, e.g. region = "
                  f"{quote}east{quote}", start, source)
        ch = source[i]
        if ch == "\n":
            _fail("a string may not run across a line — close it on the line it opens", start, source)
        if ch == "\\" and i + 1 < len(source):
            nxt = source[i + 1]
            # Unrecognized escapes keep their backslash, as Python's own string literals do, so a
            # Windows path or a regex inside a literal is not silently mangled.
            buf.append(_ESCAPES.get(nxt, "\\" + nxt))
            i += 2
            continue
        if ch == quote:
            i += 1
            break
        buf.append(ch)
        i += 1
    return Token("string", source[start:i], start, "".join(buf)), i


def _check_balance(tokens: Sequence[Token], source: str) -> None:
    """Bracket balance, over the TOKEN stream.

    This is `envelope._check_balance`'s check, and deliberately its wording — a reader who has seen
    "unbalanced brackets — an opener is never closed" from the envelope should see the same sentence
    here. It runs over tokens rather than characters for one reason the envelope's version cannot
    manage: a bracket inside a string literal (`by = '('`) is not a bracket, and a character scan
    counts it. Running it up front, before the parse, means the common mistake is reported as the
    shape mistake it is instead of as whatever the recursive descent happens to trip over first.
    """
    stack: list[Token] = []
    for tok in tokens:
        if tok.kind != "op":
            continue
        if tok.text in _CLOSERS:
            stack.append(tok)
        elif tok.text in (")", "]", "}"):
            if not stack:
                _fail(f"unbalanced brackets — the closing {tok.text!r} has no opener", tok.pos, source)
            opener = stack.pop()
            want = _CLOSERS[opener.text]
            if tok.text != want:
                _fail(f"unbalanced brackets — {opener.text!r} is closed by {tok.text!r}, not "
                      f"{want!r}", tok.pos, source)
    if stack:
        _fail(f"unbalanced brackets — this {stack[-1].text!r} is never closed", stack[-1].pos, source)


# ═══ 2. the IR ═══════════════════════════════════════════════════════════════════════════════════
#
# Every node is a frozen slotted dataclass, so a tree is hashable-by-shape, cheap, and immutable.
# Every node carries `pos` (the source offset it began at) as a NON-COMPARING field: two trees are
# equal when they mean the same thing, regardless of where they were written or how they were spelled
# (`@ day` vs `@ {day}`, `"east"` vs `'east'`, `in` vs `IN`). That is what makes the round-trip
# contract `parse(unparse(parse(s))) == parse(s)` a statement about MEANING and not about text.

def _pos_field():
    """A fresh `pos` field descriptor. A `dataclasses.Field` instance must not be shared between
    classes (the machinery writes the owning name onto it), so this is a factory, not a constant."""
    return field(default=-1, compare=False, repr=False)


class Node:
    """Base of the Frame-QL 1.0 expression IR. Carries no state; exists so `isinstance(x, Node)`
    and the shared `unparse` entry point have something to name."""

    __slots__ = ()

    def unparse(self, dialect: str = CANONICAL) -> str:
        """This node as Frame-QL text. See the module docstring for the two dialects."""
        return unparse(self, dialect=dialect)

    def children(self) -> tuple:
        """Direct child nodes, in source order. `walk()` is built on this."""
        return ()


@dataclass(frozen=True, slots=True)
class Literal(Node):
    """A number or string literal. `raw` is the source spelling and does NOT take part in equality:
    `"east"` and `'east'` are the same literal."""

    value: Any
    raw: str = field(default="", compare=False)
    pos: int = _pos_field()

    def __repr__(self) -> str:
        return f"Literal({self.value!r})"


@dataclass(frozen=True, slots=True)
class Path(Node):
    """ONE dotted-path shape (§15.1): `revenue`, `level.last`, `a.b.c`.

    Whether the whole path is a governed name, or a base expression with member access hung off it,
    is NOT decided here and cannot be: §15.1 says collision detection "is therefore a per-context
    semantic conformance check after namespace and type/capability resolution, not a lexer-only or
    parser-only decision". The parser records the spelling; the resolver splits it."""

    segments: tuple[str, ...]
    pos: int = _pos_field()

    def __post_init__(self) -> None:
        assert self.segments, "a Path has at least one segment"

    @property
    def dotted(self) -> str:
        return ".".join(self.segments)

    def __repr__(self) -> str:
        return f"Path({self.dotted})"


@dataclass(frozen=True, slots=True)
class Member(Node):
    """`.name` applied to something that is NOT a bare dotted path — a parenthesized expression, a
    call result, a subscript. `(a.b).c` and `(state @ {account}).cardinality` are `Member`s; `a.b.c`
    is a `Path`. §15.1 makes the parenthesized form a distinct written intent, so it is a distinct
    node and the canonical spelling keeps its parentheses."""

    base: Node
    name: str
    pos: int = _pos_field()

    def children(self) -> tuple:
        return (self.base,)

    def __repr__(self) -> str:
        return f"Member({self.base!r}, {self.name})"


@dataclass(frozen=True, slots=True)
class Subscript(Node):
    """`E[key]` — semantic-value subscription (§15.4), never analytical filtering (§7.5).

    A key that is a comparison is a TYPE question, not a syntax question, so it parses. See
    `filter_shaped_subscripts()`."""

    base: Node
    key: Node
    pos: int = _pos_field()

    def children(self) -> tuple:
        return (self.base, self.key)

    def __repr__(self) -> str:
        return f"Subscript({self.base!r}, {self.key!r})"


@dataclass(frozen=True, slots=True)
class NamedArg(Node):
    """`name: value` — a named analytical parameter (§15.2).

    The historical `name = value` spelling canonicalizes to THIS node; `historical` records which
    spelling was written (for the §15.2 governed-capability gate and for linting) and takes no part
    in equality, so `by = cal.day` and `by: cal.day` are the same node."""

    name: str
    value: Node
    historical: bool = field(default=False, compare=False)
    pos: int = _pos_field()

    def children(self) -> tuple:
        return (self.value,)

    def __repr__(self) -> str:
        return f"NamedArg({self.name}: {self.value!r})"


@dataclass(frozen=True, slots=True)
class Call(Node):
    """`f(positional…, named…)` (§15.2). `func` is normally a `Path` (`variance`, `graph.neighbors`)
    but may be any postfix expression (`(x).f(1)`, `f(1)(2)`). Positional arguments always precede
    named ones — the parser enforces that, so `args` and `named` need no interleaving order."""

    func: Node
    args: tuple[Node, ...] = ()
    named: tuple[NamedArg, ...] = ()
    pos: int = _pos_field()

    def children(self) -> tuple:
        return (self.func,) + tuple(self.args) + tuple(self.named)

    def __repr__(self) -> str:
        inner = ", ".join([repr(a) for a in self.args] + [repr(k) for k in self.named])
        return f"Call({self.func!r}, [{inner}])"


@dataclass(frozen=True, slots=True)
class Anchor(Node):
    """An anchor: `E @ {a * b}` (ascription) when `base` is set, `{a * b}` (grain literal) when it is
    `None`.

    `levels` are dotted LEVEL names, in written order. `{}` — zero levels — is the empty product, the
    Manifold-wide scalar, and is a declared grain rather than a missing one. Duplicate levels are
    preserved as written; collapsing them is a semantic normalization, not a parse."""

    base: Optional[Node]
    levels: tuple[Path, ...]
    pos: int = _pos_field()

    @property
    def composite(self) -> bool:
        """True when this pin denotes a PRODUCT grain rather than a single level — which is exactly
        when the host dialect must spell it as a tuple (`@ (a, b)`, `@ ()`) rather than bare
        (`@ day`), mirroring `Planner._convert_input_anchor`. Derived, never stored: `@ day` and
        `@ {day}` are the same pin and must not compare unequal over a spelling."""
        return len(self.levels) != 1

    def children(self) -> tuple:
        return ((self.base,) if self.base is not None else ()) + tuple(self.levels)

    def __repr__(self) -> str:
        grain = "{" + " * ".join(p.dotted for p in self.levels) + "}"
        return f"Anchor({self.base!r} @ {grain})" if self.base is not None else f"Anchor({grain})"


@dataclass(frozen=True, slots=True)
class Unary(Node):
    """`+E`, `-E` (numeric unary rung) or `NOT E` (logical rung). `op` is normalized — `"+"`, `"-"`,
    `"NOT"`; `raw_op` keeps the source spelling (`not`) and does not affect equality."""

    op: str
    operand: Node
    raw_op: str = field(default="", compare=False)
    pos: int = _pos_field()

    def children(self) -> tuple:
        return (self.operand,)

    def __repr__(self) -> str:
        return f"Unary({self.op}, {self.operand!r})"


@dataclass(frozen=True, slots=True)
class Binary(Node):
    """Arithmetic: `* / %` and `+ -`. Left-associative."""

    op: str
    left: Node
    right: Node
    pos: int = _pos_field()

    def children(self) -> tuple:
        return (self.left, self.right)

    def __repr__(self) -> str:
        return f"Binary({self.op}, {self.left!r}, {self.right!r})"


@dataclass(frozen=True, slots=True)
class Compare(Node):
    """`= != < <= > >= IN BETWEEN` (§15.2 — `=` compares). Non-associative.

    For `BETWEEN`, `right` is a two-item `Tuple` holding the bounds; the `AND` between them is
    BETWEEN's own delimiter and never a logical conjunction. `==` normalizes to `=`."""

    op: str
    left: Node
    right: Node
    raw_op: str = field(default="", compare=False)
    pos: int = _pos_field()

    def children(self) -> tuple:
        return (self.left, self.right)

    def __repr__(self) -> str:
        return f"Compare({self.op}, {self.left!r}, {self.right!r})"


@dataclass(frozen=True, slots=True)
class Logical(Node):
    """`AND` / `OR`, flattened n-ary as written: `a AND b AND c` is one node with three operands,
    while `a AND (b AND c)` keeps its nesting because the writer wrote it."""

    op: str
    operands: tuple[Node, ...]
    raw_op: str = field(default="", compare=False)
    pos: int = _pos_field()

    def children(self) -> tuple:
        return tuple(self.operands)

    def __repr__(self) -> str:
        return f"Logical({self.op}, {list(self.operands)!r})"


@dataclass(frozen=True, slots=True)
class Tuple(Node):
    """`(a, b)` (§15.3). ONE syntactic structure with two readings — a structured value, or an
    ordered coordinate precedence when a parameter expects an ordering specification (`by: (customer,
    cal.day)`). Which one it is, is semantic typing and is not decided here."""

    items: tuple[Node, ...]
    pos: int = _pos_field()

    def children(self) -> tuple:
        return tuple(self.items)

    def __repr__(self) -> str:
        return f"Tuple({list(self.items)!r})"


def walk(node: Node) -> Iterable[Node]:
    """Yield `node` and every node beneath it, depth-first, in source order."""
    yield node
    for child in node.children():
        yield from walk(child)


def filter_shaped_subscripts(node: Node) -> tuple[Subscript, ...]:
    """Every `Subscript` in the tree whose key READS LIKE an analytical filter — a comparison, a
    conjunction, or a `NOT`.

    §7.5 rules that `revenue[region = "east"]` "is therefore not canonical analytical filtering" and
    that "a conforming diagnostic should point the writer toward `WHERE` or `HAVING` rather than
    silently reinterpret the brackets as a filter". This helper exists so a resolver can write that
    sentence. It is a SHAPE report and nothing more: whether the expression is actually a type error
    depends on whether the semantic type admits Boolean subscription, which only the resolver knows,
    and this function deliberately does not guess.
    """
    return tuple(
        n for n in walk(node)
        if isinstance(n, Subscript)
        and (isinstance(n.key, (Compare, Logical))
             or (isinstance(n.key, Unary) and n.key.op == "NOT"))
    )


# ═══ 3. the parser ═══════════════════════════════════════════════════════════════════════════════

def _reads_as_named_argument(node: Node) -> bool:
    """True when `node`, written bare in call-argument position, would be RE-READ as the historical
    `name = value` named-argument spelling (§15.2 rule (2)).

    This is the PARSE-SIDE question — what the argument rule does with source text as written — so it
    honours the `==` escape hatch: a comparison spelled `==` is never re-read as a named argument.

    The unparser must NOT use this predicate. See `_renders_as_named_argument`."""
    return (isinstance(node, Compare) and node.op == "=" and node.raw_op != "=="
            and isinstance(node.left, Path) and len(node.left.segments) == 1)


def _renders_as_named_argument(node: Node) -> bool:
    """True when `node`, rendered bare in call-argument position, would be RE-READ as a named
    argument — the UNPARSE-side question, and deliberately not the same one.

    The difference is `==`, and getting it wrong is a wire defect rather than a cosmetic one. `==` is
    compatibility input that CANONICALIZES to `=` (§15.2), so both spellings render as `=`. Asking
    the parse-side question here therefore reasons about a spelling that is about to be discarded:
    `f(b == c)` is a positional comparison, the parse-side predicate says "not named-shaped, no
    parentheses needed", and the emitted `f(b = c)` re-reads as a NAMED ARGUMENT. A different tree,
    from text this module produced itself.

    That mattered end to end, not just in the abstract: canonical text is the default column key and
    the statement path canonicalizes before planning, so `cumsum(revenue, by == 'month')` was refused
    by the builder API and SERVED A NUMBER through the statement path — the two-door split this unit
    exists to close, re-opened by the unparser.

    So the question the unparser must ask is about SHAPE ALONE: whatever spelling arrives, `=` is
    what leaves."""
    return (isinstance(node, Compare) and node.op == "="
            and isinstance(node.left, Path) and len(node.left.segments) == 1)


_MULTIPLICATIVE = ("*", "/", "%")
_ADDITIVE = ("+", "-")
_COMPARISON = ("=", "==", "!=", "<", "<=", ">", ">=")
_LEVEL_SEPARATORS = ("*", ",")


class _Arg(NamedTuple):
    """One call argument as WRITTEN, before the §15.2 argument rule is applied.

    `colon_name` is set only for the canonical `name: value` spelling. `grouped` records that the
    argument was written inside its own parentheses, which is what makes `f(a, (b = c))` a
    comparison rather than a named argument.
    """

    colon_name: Optional[str]
    node: Node
    grouped: bool
    pos: int


def parse(source: str, *, origin: str = "expression") -> Node:
    """Parse Frame-QL 1.0 expression text into the IR.

    `origin` names the position for the error message ("expression", "predicate", "series", …).

    Raises `FrameQLSyntaxError` — and ONLY `FrameQLSyntaxError` — on any rejection. That total
    guarantee is the P1-26 ruling restated (planner.py:27-42): the reader must never be answered in
    the voice of a substrate, and after this module there is no substrate left to leak. The blanket
    guard below extends it to a defect in this file: a bug here is a Frame-QL refusal, not a
    traceback in someone's frame result.

    The guarantee covers what a CALLER can reach through this function, which is what P1-26 is about.
    It is not a claim about `unparse` or `walk` over a tree assembled by hand in some other module:
    those recurse, and nothing stops a caller building a 10,000-deep `Binary` chain directly. What
    closes the practical hole is `MAX_DEPTH` bounding the tree this parser will PRODUCE, so no input
    can hand a consumer something it cannot walk.
    """
    if source is None or not isinstance(source, str) or not source.strip():
        _fail(f"empty {origin} — a series is at least one expression, e.g. revenue", 0,
              source if isinstance(source, str) else repr(source))
    try:
        parser = _Parser(tokenize(source), source, origin)
        node = parser.expression()
        if parser.peek().kind != "end":
            tok = parser.peek()
            parser.fail(f"Frame-QL cannot read this {origin} past {tok.text!r} — the expression is "
                        f"complete before it; join the two parts with an operator, or remove it", tok)
        return node
    except FrameQLSyntaxError:
        raise
    except RecursionError:
        _fail(f"this {origin} nests too deeply to read — simplify it, or split it with WITH", 0, source)
    except Exception as exc:                                   # pragma: no cover - the P1-26 backstop
        _fail(f"Frame-QL cannot read this {origin} ({type(exc).__name__}: {exc})", 0, source)


class _Parser:
    """Recursive descent, one method per rung of the §15 ladder, loosest method calling the next
    tighter one. Read the methods bottom-up and you have read §15's precedence table."""

    def __init__(self, tokens: list[Token], source: str, origin: str) -> None:
        self.tokens = tokens
        self.source = source
        self.origin = origin
        self.i = 0
        self.depth = 0

    # ---- token cursor -------------------------------------------------------------------------
    def peek(self, ahead: int = 0) -> Token:
        j = min(self.i + ahead, len(self.tokens) - 1)
        return self.tokens[j]

    def next(self) -> Token:
        tok = self.tokens[self.i]
        if tok.kind != "end":
            self.i += 1
        return tok

    def at_op(self, *texts: str) -> bool:
        tok = self.peek()
        return tok.kind == "op" and tok.text in texts

    def at_keyword(self, *words: str) -> bool:
        tok = self.peek()
        return tok.kind == "keyword" and tok.text.upper() in words

    def accept_op(self, *texts: str) -> Optional[Token]:
        return self.next() if self.at_op(*texts) else None

    def accept_keyword(self, *words: str) -> Optional[Token]:
        return self.next() if self.at_keyword(*words) else None

    def expect_op(self, text: str, what: str) -> Token:
        if not self.at_op(text):
            self.fail(f"expected {text!r} {what}, got {self._describe(self.peek())}", self.peek())
        return self.next()

    def fail(self, message: str, tok: Optional[Token] = None):
        tok = tok if tok is not None else self.peek()
        _fail(message, tok.pos, self.source)

    @staticmethod
    def _describe(tok: Token) -> str:
        return "the end of the expression" if tok.kind == "end" else repr(tok.text)

    # ---- depth guard --------------------------------------------------------------------------
    def _enter(self) -> None:
        self.depth += 1
        if self.depth > MAX_DEPTH:
            self.fail(f"this {self.origin} nests more than {MAX_DEPTH} levels deep — simplify it, "
                      f"or name the parts with WITH")

    def _leave(self) -> None:
        self.depth -= 1

    def _grow(self, spine: int, tok: Token) -> None:
        """Bound the depth of the tree a LEFT-ASSOCIATIVE loop is building.

        `_enter`/`_leave` are balanced around each ITERATION of those loops, so `self.depth` never
        grows for `a + a + a + …` — but the left spine does, one level per operator. The tree was
        therefore unbounded while the guard read as though it were bounded, and the consumers this
        module hands trees to (`unparse`, and every recursive walk in the planner) are ordinary
        recursive functions. A long enough chain reached them as a raw `RecursionError` — the one
        exception class this module promises can never escape.

        Bounding the spine here closes it at the parse boundary, which is where the promise lives:
        a pathological input is refused as a Frame-QL error, in Frame-QL's voice, with an offset.
        """
        if self.depth + spine > MAX_DEPTH:
            self.fail(f"this {self.origin} chains more than {MAX_DEPTH} operations — simplify it, "
                      f"or name the parts with WITH", tok)

    # ══ the ladder, loosest rung first ═════════════════════════════════════════════════════════

    def expression(self) -> Node:
        """The whole expression: the loosest rung."""
        return self.logical_or()

    # logical: OR (loosest)
    def logical_or(self) -> Node:
        left = self.logical_and()
        if not self.at_keyword("OR"):
            return left
        operands, raw = [left], self.peek().text
        while self.accept_keyword("OR") is not None:
            self._grow(len(operands), self.peek())
            operands.append(self.logical_and())
        return Logical("OR", tuple(operands), raw, left.pos)

    # logical: AND
    def logical_and(self) -> Node:
        left = self.logical_not()
        if not self.at_keyword("AND"):
            return left
        operands, raw = [left], self.peek().text
        while self.accept_keyword("AND") is not None:
            self._grow(len(operands), self.peek())
            operands.append(self.logical_not())
        return Logical("AND", tuple(operands), raw, left.pos)

    # logical: NOT (tightest of the three)
    def logical_not(self) -> Node:
        if (tok := self.accept_keyword("NOT")) is not None:
            self._enter()
            operand = self.logical_not()
            self._leave()
            return Unary("NOT", operand, tok.text, tok.pos)
        return self.comparison()

    # comparison / membership — NON-associative (see the module docstring)
    def comparison(self) -> Node:
        left = self.additive()
        tok = self.peek()

        if tok.kind == "keyword" and tok.text.upper() in ("IN", "BETWEEN"):
            self.next()
            if tok.text.upper() == "IN":
                right = self.additive()
                node = Compare("IN", left, right, tok.text, tok.pos)
            else:
                lo = self.additive()
                if not self.at_keyword("AND"):
                    self.fail("BETWEEN names two bounds — write `E BETWEEN low AND high`, e.g. "
                              "day BETWEEN '2024-01-01' AND '2024-01-31'", self.peek())
                self.next()
                hi = self.additive()
                node = Compare("BETWEEN", left, Tuple((lo, hi), lo.pos), tok.text, tok.pos)
            self._refuse_chained_comparison(node)
            return node

        if tok.kind == "op" and tok.text in _COMPARISON:
            self.next()
            op = "=" if tok.text in ("=", "==") else tok.text
            right = self.additive()
            node = Compare(op, left, right, tok.text, tok.pos)
            self._refuse_chained_comparison(node)
            return node

        # `a NOT IN b` / `a NOT BETWEEN …` are not §15 forms; name the form that is.
        if tok.kind == "keyword" and tok.text.upper() == "NOT" and \
                self.peek(1).kind == "keyword" and self.peek(1).text.upper() in ("IN", "BETWEEN"):
            word = self.peek(1).text.upper()
            self.fail(f"Frame-QL has no `NOT {word}` operator — negate the whole comparison instead, "
                      f"e.g. NOT (a {word} b)", tok)
        return left

    def _refuse_chained_comparison(self, node: Compare) -> None:
        """`a < b < c` has a Python reading and a SQL reading and §15 gives neither. Refuse rather
        than pick one without a ruling; the remedy is unambiguous either way."""
        tok = self.peek()
        chained = (tok.kind == "op" and tok.text in _COMPARISON) or \
                  (tok.kind == "keyword" and tok.text.upper() in ("IN", "BETWEEN"))
        if chained:
            self.fail("comparisons do not chain in Frame-QL — say which one you mean with "
                      "parentheses and AND, e.g. (a < b) AND (b < c)", tok)

    # additive: + -   (left-associative)
    def additive(self) -> Node:
        node, spine = self.multiplicative(), 0
        while (tok := self.accept_op(*_ADDITIVE)) is not None:
            spine += 1
            self._grow(spine, tok)
            self._enter()
            node = Binary(tok.text, node, self.multiplicative(), tok.pos)
            self._leave()
        return node

    # multiplicative: * / %   (left-associative).  Outside braces `*` is multiplication (§15.0).
    def multiplicative(self) -> Node:
        node, spine = self.numeric_unary(), 0
        while (tok := self.accept_op(*_MULTIPLICATIVE)) is not None:
            spine += 1
            self._grow(spine, tok)
            self._enter()
            node = Binary(tok.text, node, self.numeric_unary(), tok.pos)
            self._leave()
        return node

    # numeric unary: +E -E   (LOOSER than `@` — §15's ladder puts anchor ascription above it)
    def numeric_unary(self) -> Node:
        if (tok := self.accept_op("+", "-")) is not None:
            self._enter()
            operand = self.numeric_unary()
            self._leave()
            return Unary(tok.text, operand, tok.text, tok.pos)
        return self.anchor_ascription()

    # anchor ascription: E @ {A}   (left-associative; tighter than unary, looser than postfix)
    def anchor_ascription(self) -> Node:
        node, spine = self.postfix(), 0
        while (tok := self.accept_op("@")) is not None:
            spine += 1
            self._grow(spine, tok)
            self._enter()
            node = Anchor(node, self._pin(tok), node.pos)
            self._leave()
        return node

    def _pin(self, at_tok: Token) -> tuple[Path, ...]:
        """The grain after `@`. Canonical `{a * b}`; `{a, b}`, `(a, b)` and a bare `level` are the
        accepted sugars (the same set `Planner._canon_expr` folds into the brace form)."""
        if self.at_op("{"):
            return self._level_group("{", "}")
        if self.at_op("("):
            return self._level_group("(", ")")
        if self.peek().kind == "name":
            return (self._dotted_path(),)
        self.fail("`@` must be followed by the grain it pins — write `@ {level}` or `@ {a*b}`, "
                  "e.g. avg(revenue @ {day}); `@ {}` is the Manifold-wide scalar", self.peek())

    def _level_group(self, opener: str, closer: str) -> tuple[Path, ...]:
        """A braced (or parenthesized) product of dotted LEVEL names. `{}` is the empty product."""
        self.expect_op(opener, "to open the grain")
        levels: list[Path] = []
        if self.at_op(closer):
            self.next()
            return ()
        while True:
            if self.peek().kind != "name":
                self.fail(f"malformed input anchor — name each level, e.g. avg(aov @ {{store*day}}); "
                          f"got {self._describe(self.peek())}", self.peek())
            levels.append(self._dotted_path())
            if self.at_op(*_LEVEL_SEPARATORS):
                self.next()
                if self.at_op(closer):
                    self.fail("malformed input anchor — a separator with no level after it; name "
                              "each level, e.g. avg(aov @ {store*day})", self.peek())
                continue
            break
        if not self.at_op(closer):
            self.fail(f"inside {opener}{closer} an anchor is a product of level names — separate "
                      f"them with `*`, e.g. {{store*day}}; got {self._describe(self.peek())}",
                      self.peek())
        self.next()
        return tuple(levels)

    # postfix: f(...) | .member | .method(...) | [key]   (left-associative, tightest)
    def postfix(self) -> Node:
        node, spine = self.primary(), 0
        while True:
            if self.at_op(".") or self.at_op("(") or self.at_op("["):
                # each postfix step is one more level on the left spine — see `_grow`
                spine += 1
                self._grow(spine, self.peek())
            if self.at_op("."):
                # A `.name` on a bare dotted path was already absorbed by `_dotted_path` into ONE
                # Path (§15.1). Reaching here means the base is something else — a parenthesized
                # expression, a call, a subscript — so this is explicit value access.
                self.next()
                name_tok = self.peek()
                if name_tok.kind not in ("name", "keyword"):
                    self.fail(f"`.` must be followed by a member name, e.g. (state @ {{account}})"
                              f".cardinality; got {self._describe(name_tok)}", name_tok)
                self.next()
                node = Member(node, name_tok.text, node.pos)
                continue
            if self.at_op("("):
                node = self._call(node)
                continue
            if self.at_op("["):
                self.next()
                self._enter()
                if self.at_op("]"):
                    self.fail("`[ ]` subscribes into a value and needs a key — write E[key], e.g. "
                              "basket['sku']; it never filters (use WHERE or HAVING for that)",
                              self.peek())
                key = self.expression()
                if self.at_op(","):                          # a tuple key, for multi-coordinate types
                    items = [key]
                    while self.accept_op(",") is not None:
                        if self.at_op("]"):
                            break
                        items.append(self.expression())
                    key = Tuple(tuple(items), key.pos)
                self.expect_op("]", "to close the subscript")
                self._leave()
                node = Subscript(node, key, node.pos)
                continue
            return node

    # ---- calls and the §15.2 argument rule -----------------------------------------------------
    def _call(self, func: Node) -> Call:
        self.expect_op("(", "to open the argument list")
        self._enter()
        items: list[_Arg] = []
        if not self.at_op(")"):
            while True:
                items.append(self._argument())
                if self.accept_op(",") is not None:
                    if self.at_op(")"):
                        self.fail("a dangling comma in the argument list — remove it, or name the "
                                  "argument that belongs there", self.peek())
                    continue
                break
        self.expect_op(")", "to close the argument list")
        self._leave()
        args, named = self._split_arguments(items, func)
        return Call(func, args, named, func.pos)

    def _argument(self) -> "_Arg":
        """One argument. Canonical `name: value` is recognized here; the historical `name = value`
        spelling is NOT — it parses as the comparison it is, and `_split_arguments` decides."""
        tok = self.peek()
        if tok.kind == "name" and self.peek(1).kind == "op" and self.peek(1).text == ":":
            self.next(); self.next()
            self._enter()
            value = self.expression()
            self._leave()
            return _Arg(tok.text, value, False, tok.pos)
        grouped = tok.kind == "op" and tok.text == "("
        self._enter()
        node = self.expression()
        self._leave()
        return _Arg(None, node, grouped, tok.pos)

    def _split_arguments(self, items, func: Node) -> tuple[tuple[Node, ...], tuple[NamedArg, ...]]:
        """Apply the §15.2 argument rule (see the module docstring for the full statement).

        The named arguments are the longest TRAILING run of named-shaped arguments; a `name = value`
        argument inside that run canonicalizes to the same `NamedArg` as `name: value`, and one
        outside it stays the comparison it parsed as. A `name: value` argument outside the run is a
        positional-after-named violation and is refused by name.
        """
        def historical_name(item: "_Arg") -> Optional[str]:
            """The historical `name = value` spelling, or None.

            Two things disqualify an argument that otherwise looks the part, and both are the
            module docstring's escape hatch made real:
              · it was written inside its own parentheses — `f(a, (b = c))` — so the `=` is not at
                the argument's top level and the named reading was explicitly declined;
              · it was written with `==`, the unambiguous comparison spelling, which no historical
                named-argument form ever used.
            """
            node = item.node
            if item.grouped:
                return None
            return node.left.segments[0] if _reads_as_named_argument(node) else None

        def named_shaped(item: "_Arg") -> bool:
            return item.colon_name is not None or historical_name(item) is not None

        start = len(items)
        while start > 0 and named_shaped(items[start - 1]):
            start -= 1

        func_name = func.dotted if isinstance(func, Path) else "this call"
        args: list[Node] = []
        for item in items[:start]:
            if item.colon_name is not None:
                _fail(f"{func_name}: the named argument {item.colon_name!r} comes before a "
                      f"positional one — positional operands must precede named parameters, e.g. "
                      f"variance(price, ddof: 1)", item.pos, self.source)
            args.append(item.node)

        named: list[NamedArg] = []
        seen: set[str] = set()
        for item in items[start:]:
            if item.colon_name is not None:
                name, value, historical = item.colon_name, item.node, False
            else:
                name, value, historical = historical_name(item), item.node.right, True
            if name in seen:
                _fail(f"{func_name}: the named argument {name!r} is given twice — name each "
                      f"parameter once", item.pos, self.source)
            seen.add(name)
            named.append(NamedArg(name, value, historical, item.pos))
        return tuple(args), tuple(named)

    # ---- primary ------------------------------------------------------------------------------
    def primary(self) -> Node:
        tok = self.peek()

        if tok.kind == "number":
            self.next()
            return Literal(tok.value, tok.text, tok.pos)

        if tok.kind == "string":
            self.next()
            return Literal(tok.value, tok.text, tok.pos)

        if tok.kind == "name":
            return self._dotted_path()

        if tok.kind == "op" and tok.text == "(":
            return self._parenthesized()

        if tok.kind == "op" and tok.text == "{":
            # A grain literal standing on its own — §15.2's `within: {customer}`.
            return Anchor(None, self._level_group("{", "}"), tok.pos)

        if tok.kind == "op" and tok.text == "*":
            # The old dialect answered `count(*)` in CPython's voice ("Invalid star expression").
            # It is refused here in Frame-QL's, naming what the language does have.
            self.fail("`*` is multiplication outside braces and anchor refinement inside them — it "
                      "is not a wildcard; count a named series instead, e.g. count(order)", tok)

        if tok.kind == "keyword":
            self.fail(f"{tok.text!r} is a Frame-QL keyword and cannot start an expression — an "
                      f"expression begins with a name, a number, a string or `(`", tok)

        self.fail(f"Frame-QL cannot read this {self.origin} at {self._describe(tok)} — an expression "
                  f"begins with a name, a number, a string, `(` or `{{`", tok)

    def _parenthesized(self) -> Node:
        """`( E )` groups; `( )`, `( E , )` and `( E , E … )` are tuples (§15.3)."""
        open_tok = self.expect_op("(", "to open a group")
        self._enter()
        if self.at_op(")"):
            self.next()
            self._leave()
            return Tuple((), open_tok.pos)
        first = self.expression()
        if not self.at_op(","):
            self.expect_op(")", "to close the group")
            self._leave()
            return first
        items = [first]
        while self.accept_op(",") is not None:
            if self.at_op(")"):
                break                                        # trailing comma: `(a,)` is a 1-tuple
            items.append(self.expression())
        self.expect_op(")", "to close the tuple")
        self._leave()
        return Tuple(tuple(items), open_tok.pos)

    def _dotted_path(self) -> Path:
        """One dotted-path shape (§15.1). Greedy over every `.name`, so `graph.neighbors(node)` is a
        call whose callee is the single path `graph.neighbors` — not a method fetched off `graph`.
        Which prefix of a path is a governed name and which suffix is value access is a per-context
        semantic check (§15.1.4), so the parser records the whole spelling and decides nothing."""
        first = self.next()
        segments = [first.text]
        while self.at_op(".") and self.peek(1).kind in ("name", "keyword"):
            self.next()
            segments.append(self.next().text)
        return Path(tuple(segments), first.pos)


# ═══ 4. the unparser ═════════════════════════════════════════════════════════════════════════════
#
# THE CONTRACT. On every expression the old `ast`-hosted dialect accepted, HOST output is
# byte-identical to `ast.unparse(ast.parse(<the converted text>, mode="eval").body)`. The old dialect
# only ever saw text with `Planner._convert_input_anchor` already applied, which is why HOST spells
# anchors the way that function does. CANONICAL is the §15 spelling and is what a reader and a
# column key should see.

#: Precedence, tightest last. The two tables differ ONLY in where `@` and numeric unary sit — which
#: is the one place §15 and CPython disagree, and the reason two tables exist at all.
_P_OR, _P_AND, _P_NOT, _P_CMP, _P_ADD, _P_MUL, _P_UNARY, _P_ANCHOR, _P_POSTFIX, _P_ATOM = range(1, 11)

_ARITH = {"+": _P_ADD, "-": _P_ADD, "*": _P_MUL, "/": _P_MUL, "%": _P_MUL}


def _precedence(node: Node, dialect: str) -> int:
    if isinstance(node, Binary):
        return _ARITH[node.op]
    if isinstance(node, Unary):
        if node.op == "NOT":
            return _P_NOT
        return _P_UNARY
    if isinstance(node, Anchor):
        if node.base is None:
            return _P_ATOM                                  # a grain literal is a primary
        # §15 puts anchor ascription between postfix and unary; CPython's `@` sits with `*` and `/`.
        return _P_ANCHOR if dialect == CANONICAL else _P_MUL
    if isinstance(node, Compare):
        return _P_CMP
    if isinstance(node, Logical):
        return _P_AND if node.op == "AND" else _P_OR
    if isinstance(node, (Call, Member, Subscript)):
        return _P_POSTFIX
    return _P_ATOM


def unparse(node: Node, *, dialect: str = CANONICAL) -> str:
    """Render an expression node back to Frame-QL text.

    `dialect=CANONICAL` (default) is the §15 canonical spelling. `dialect=HOST` is the spelling
    CPython's `ast.unparse` produces for the same expression, for byte-compatible refusal text and
    column keys during migration. See the module docstring.
    """
    if dialect not in (CANONICAL, HOST):
        raise ValueError(f"unknown dialect {dialect!r} — use expr.CANONICAL or expr.HOST")
    if not isinstance(node, Node):
        raise TypeError(f"unparse wants a Frame-QL expression node, got {type(node).__name__}")
    return _render(node, dialect, 0)


def _wrap(node: Node, dialect: str, need: int) -> str:
    """Render `node`, parenthesized iff its own precedence is looser than the context demands."""
    text = _render(node, dialect, need)
    return f"({text})" if _precedence(node, dialect) < need else text


#: The lexer's escape table, inverted. Anything absent is emitted RAW, which round-trips because the
#: scanner takes an unrecognised character literally.
_QUOTE_ESCAPES = {"\\": "\\\\", "'": "\\'", "\n": "\\n", "\t": "\\t", "\r": "\\r", "\0": "\\0"}


def _quote(value: str) -> str:
    """Write a string literal in FRAME-QL's escape vocabulary, not Python's.

    `repr` emits Python escapes — `\\x00`, `\\u2028` — and the Frame-QL lexer knows only
    `\\\\ \\' \\" \\n \\t \\r \\0`, deliberately preserving the backslash for anything else. So a literal
    containing a NUL rendered as `'\\x00'` and read back as the four characters `\\`, `x`, `0`, `0`:
    canonical text that does not mean what it came from. Canonical text is the default column key,
    so that is an identity defect, not a display one.
    """
    return "'" + "".join(_QUOTE_ESCAPES.get(ch, ch) for ch in value) + "'"


def _render(node: Node, dialect: str, need: int) -> str:
    if isinstance(node, Literal):
        if dialect == CANONICAL and isinstance(node.value, str):
            return _quote(node.value)
        # HOST keeps `repr`: its whole contract is to be byte-identical to `ast.unparse`, and that
        # is a fidelity claim about the RETIRED dialect, so it must not be improved.
        return repr(node.value)

    if isinstance(node, Path):
        return node.dotted

    if isinstance(node, Member):
        base = _wrap(node.base, dialect, _P_POSTFIX)
        if isinstance(node.base, Literal) and isinstance(node.base.value, (int, float)):
            # `785 .IN` would render `785.IN`, which the lexer reads back as the float `785.` —
            # a round-trip failure, not a spelling preference. CPython's unparser parenthesizes
            # here for the same reason.
            base = f"({base})"
        elif dialect == CANONICAL and isinstance(node.base, (Path, Member)):
            # §15.1: `(a.b).c` is a different written intent from `a.b.c`, so canonical keeps the
            # parentheses. HOST cannot spell the difference (CPython has only `Attribute`).
            base = f"({base})"
        return f"{base}.{node.name}"

    if isinstance(node, Subscript):
        key = node.key
        if isinstance(key, Tuple) and key.items:
            # A tuple subscript key is written without its own parentheses, matching `ast.unparse`.
            inner = ", ".join(_render(i, dialect, 0) for i in key.items)
            if len(key.items) == 1:
                # ...except a ONE-element tuple, where dropping the comma erases the tuple and
                # `a[(1,)]` and `a[1]` collapse to one text from two different trees. Canonical text
                # is the default column key, so a collision here is two meanings at one address.
                inner += ","
        else:
            inner = _render(key, dialect, 0)
        return f"{_wrap(node.base, dialect, _P_POSTFIX)}[{inner}]"

    if isinstance(node, Call):
        # A POSITIONAL argument in the trailing run of named-shaped arguments must be written back
        # inside parentheses, or the §15.2 argument rule would re-read it as a named argument on the
        # next parse. `if(region = 'east', 1, 0)` needs nothing (the run is empty); `f(a, (b = c))`
        # needs its parentheses back.
        protect = len(node.args)
        while protect > 0 and _renders_as_named_argument(node.args[protect - 1]):
            protect -= 1
        parts = [f"({_render(a, dialect, 0)})" if i >= protect else _render(a, dialect, 0)
                 for i, a in enumerate(node.args)]
        parts += [_render(k, dialect, 0) for k in node.named]
        return f"{_wrap(node.func, dialect, _P_POSTFIX)}({', '.join(parts)})"

    if isinstance(node, NamedArg):
        sep = ": " if dialect == CANONICAL else "="
        return f"{node.name}{sep}{_render(node.value, dialect, 0)}"

    if isinstance(node, Anchor):
        if node.base is None:
            # A grain LITERAL (`within: {customer}`) is a 1.0-only form — the old dialect had no such
            # node, so there is no host spelling to be faithful to. Always canonical.
            return _grain(node.levels, CANONICAL)
        grain = _grain(node.levels, dialect)
        # CANONICAL: the ascription's operand is a POSTFIX expression (§15's ladder). HOST: CPython's
        # `@` is a multiplicative binary operator, left-associative, so its left operand needs only
        # multiplicative precedence — which is exactly why `(a / b) @ c` unparses as `a / b @ c` there.
        need = _P_POSTFIX if dialect == CANONICAL else _P_MUL
        return f"{_wrap(node.base, dialect, need)} @ {grain}"

    if isinstance(node, Unary):
        if node.op == "NOT":
            return f"NOT {_wrap(node.operand, dialect, _P_NOT)}"
        return f"{node.op}{_wrap(node.operand, dialect, _P_UNARY)}"

    if isinstance(node, Binary):
        prec = _ARITH[node.op]
        return (f"{_wrap(node.left, dialect, prec)} {node.op} "
                f"{_wrap(node.right, dialect, prec + 1)}")

    if isinstance(node, Compare):
        if node.op == "BETWEEN":
            lo, hi = node.right.items
            return (f"{_wrap(node.left, dialect, _P_ADD)} BETWEEN "
                    f"{_wrap(lo, dialect, _P_ADD)} AND {_wrap(hi, dialect, _P_ADD)}")
        return (f"{_wrap(node.left, dialect, _P_ADD)} {node.op} "
                f"{_wrap(node.right, dialect, _P_ADD)}")

    if isinstance(node, Logical):
        prec = _P_AND if node.op == "AND" else _P_OR
        return f" {node.op} ".join(_wrap(o, dialect, prec + 1) for o in node.operands)

    if isinstance(node, Tuple):
        if not node.items:
            return "()"
        if len(node.items) == 1:
            return f"({_render(node.items[0], dialect, 0)},)"
        return "(" + ", ".join(_render(i, dialect, 0) for i in node.items) + ")"

    raise TypeError(f"no rendering for {type(node).__name__}")   # pragma: no cover


def _grain(levels: Sequence[Path], dialect: str) -> str:
    """The pin spelling. CANONICAL is always the brace product `{a*b}` — the form
    `Planner._canon_expr` already normalizes to. HOST mirrors `Planner._convert_input_anchor`: a
    single level is bare, a product (including the empty one) is a tuple."""
    if dialect == CANONICAL:
        return "{" + "*".join(p.dotted for p in levels) + "}"
    if len(levels) == 1:
        return levels[0].dotted
    return "(" + ", ".join(p.dotted for p in levels) + ")"

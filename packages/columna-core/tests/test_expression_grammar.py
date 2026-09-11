"""
test_expression_grammar.py — the Frame-QL 1.0 EXPRESSION grammar (§15), pinned.

THE GAP THIS CLOSES. Until now no test in this repository asserted anything about the expression
dialect: not one precedence, not one associativity, not the allowed node set, not what happens to a
malformed expression. The dialect was whatever CPython's `ast` happened to do that release, and a
change to it would have been invisible until a served number moved. `columna_core.expr` makes the
grammar the repository's own, so the grammar becomes the repository's to prove.

Four things are asserted here, in rising order of how expensive it would be to get them wrong:

  1. THE §15 ACCEPTANCE RULES, each as a parse-tree SHAPE. A string comparison would pass on a tree
     that happens to print the same; every rule below is checked against the node it must produce.
  2. THE LADDER — one test per ADJACENT pair of precedence rungs, plus associativity for `-`, `/`,
     `@` and `.`. A ladder is only pinned where its neighbours are pinned.
  3. THE ERROR CHANNEL — every rejection is `FrameQLSyntaxError` and nothing else. This is the P1-26
     guarantee (planner.py:27-42) re-stated for a parser that no longer has a substrate to leak.
  4. THE AST-FIDELITY CORPUS — for every expression the OLD `ast`-hosted dialect accepted, harvested
     mechanically from the Manual, the test suite and the `.cml` fixtures, the new unparser's HOST
     output is BYTE-IDENTICAL to `ast.unparse`. Canonical column keys ARE expression text and those
     keys are wire-visible, so a language substitution that changed a single byte of them would be a
     silent wire break. This is the test that says the SUBSTITUTION did not: HOST is byte-identical
     to what the retired dialect printed. Phase 2 then made a separate, deliberate, declared change
     — the planner now keys columns in the CANONICAL 1.0 dialect rather than the host one, and
     `contract_version` bumped "4" -> "5" to say so. The two are not in tension: this test pins that
     the translation was faithful, so that the only difference on the wire is the one that was
     chosen. See `disclosure_wire.CONTRACT_VERSION`.
"""
from __future__ import annotations

import ast
import pathlib
import re

import pytest

from columna_core import expr
from columna_core.expr import (
    Anchor, Binary, Call, Compare, Literal, Logical, Member, NamedArg, Path, Subscript, Tuple, Unary,
)
from columna_core.frameql import FrameQLSyntaxError
from columna_core.envelope import parse_statement


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# helpers
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def P(*segments: str) -> Path:
    return Path(tuple(segments))


def parse(text: str):
    return expr.parse(text)


def canonical(text: str) -> str:
    return expr.unparse(expr.parse(text))


def host(text: str) -> str:
    return expr.unparse(expr.parse(text), dialect=expr.HOST)


def same_shape(a: str, b: str) -> None:
    """`a` and `b` must parse to the identical tree. The whole point of the precedence tests: an
    unparenthesized spelling and its explicit grouping mean the same thing, or the ladder is wrong."""
    assert parse(a) == parse(b), f"{a!r} and {b!r} parse differently:\n  {parse(a)!r}\n  {parse(b)!r}"


def different_shape(a: str, b: str) -> None:
    assert parse(a) != parse(b), f"{a!r} and {b!r} parse the same, but they must not"


# ── THE RETIRED DIALECT, FROZEN ─────────────────────────────────────────────────────────────────
# `_ALLOWED` and `Planner._convert_input_anchor` were BORROWED from the planner while this file was
# written, because the fidelity cohort below is defined as "what the shipped code accepted" and
# borrowing is how a test avoids grading against its own second-hand copy. Phase 2 deleted both: the
# grammar is native, so there is no allow-list and no brace shim to borrow.
#
# They are therefore frozen here, VERBATIM as of the migration commit, and this is honest rather
# than convenient. The contract these two constants serve is a HISTORICAL one — "the HOST dialect
# renders byte-for-byte what `ast.unparse` rendered for every expression the old planner accepted" —
# and a historical contract has to be stated against the history, not against whatever the planner
# does next. Pointing them at live planner code would have meant the cohort silently shrinking (or
# growing) as the planner changed, which is exactly the failure mode "borrow, do not reimplement"
# was guarding against in the other direction.
#
# Nothing in the shipped tree reads these. If they ever disagree with a claim made elsewhere, THIS
# copy is the one describing the retired dialect and the other one is describing the live one.
_RETIRED_ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Name, ast.Attribute,
                    ast.Load, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub,
                    ast.MatMult, ast.Tuple, ast.Call, ast.keyword)

_RETIRED_INPUT_ANCHOR_BRACE = re.compile(r"@\s*\{([^}]*)\}")


def _retired_convert_input_anchor(source: str) -> str:
    """`Planner._convert_input_anchor` as it stood before Frame-QL 1.0: `@ {X}` -> the shape CPython
    could hold — `@ day` for a single level, `@ (a, b)` for a product, `@ ()` for the empty grain."""
    def repl(m):
        inner = m.group(1).strip()
        if not inner:
            return "@ ()"
        levels = [x.strip() for x in re.split(r"[*,]", inner)]
        if any(not x for x in levels):
            raise FrameQLSyntaxError(f"malformed input anchor `@ {{{inner}}}`")
        if len(levels) == 1:
            return f"@ {levels[0]}"
        return "@ (" + ", ".join(levels) + ")"
    return _RETIRED_INPUT_ANCHOR_BRACE.sub(repl, source)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# 1. the §15 acceptance rules, as tree shapes
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def test_postfix_binds_tighter_than_anchor():
    """§15: `state.cardinality @ {account}` means `(state.cardinality) @ {account}`."""
    node = parse("state.cardinality @ {account}")
    assert node == Anchor(P("state", "cardinality"), (P("account"),))
    same_shape("state.cardinality @ {account}", "(state.cardinality) @ {account}")


def test_member_after_an_anchor_needs_the_other_grouping():
    """§15: `(state @ {account}).cardinality` is the OTHER reading, and it is a `Member` — the
    parenthesized form is §15.1's explicit value access, not a dotted governed name."""
    node = parse("(state @ {account}).cardinality")
    assert node == Member(Anchor(P("state"), (P("account"),)), "cardinality")
    different_shape("(state @ {account}).cardinality", "state.cardinality @ {account}")


def test_anchor_binds_tighter_than_arithmetic():
    """§15, quoted verbatim: `revenue / orders @ {customer}` reads as
    `revenue / (orders @ {customer})`."""
    node = parse("revenue / orders @ {customer}")
    assert node == Binary("/", P("revenue"), Anchor(P("orders"), (P("customer"),)))
    same_shape("revenue / orders @ {customer}", "revenue / (orders @ {customer})")


def test_anchoring_the_whole_ratio_is_the_other_grouping():
    """§15: "To anchor the whole ratio, write `(revenue / orders) @ {customer}`"."""
    node = parse("(revenue / orders) @ {customer}")
    assert node == Anchor(Binary("/", P("revenue"), P("orders")), (P("customer"),))
    different_shape("(revenue / orders) @ {customer}", "revenue / orders @ {customer}")


def test_anchor_binds_tighter_than_numeric_unary():
    """§15's ladder puts anchor ascription ABOVE numeric unary, so `-a @ b` is `-(a @ b)`.

    This is the rung where Frame-QL and CPython disagree in SHAPE: Python binds unary tighter than
    `@` and reads the same text as `(-a) @ b`."""
    node = parse("-a @ b")
    assert node == Unary("-", Anchor(P("a"), (P("b"),)))
    same_shape("-a @ b", "-(a @ b)")
    different_shape("-a @ b", "(-a) @ b")
    assert parse("(-a) @ b") == Anchor(Unary("-", P("a")), (P("b"),))


def test_star_inside_braces_is_anchor_refinement_and_outside_is_multiplication():
    """§15: "Inside braces, `*` is anchor common-refinement syntax … Outside braces, `*` is ordinary
    multiplication. The grammar never has to infer which meaning was intended from the types." """
    composite = parse("revenue @ {customer * cal.month}")
    assert composite == Anchor(P("revenue"), (P("customer"), P("cal", "month")))
    assert composite.composite is True

    product = parse("customer * cal.month")
    assert product == Binary("*", P("customer"), P("cal", "month"))

    # The SAME two names, one brace apart, are two different node types. Nothing about the operands
    # was consulted to tell them apart.
    assert type(composite) is not type(product)


def test_empty_braces_are_the_declared_empty_grain():
    """`{}` is the Manifold-wide scalar — a DECLARED grain, not a missing one (§2.6/§15.0)."""
    node = parse("revenue @ {}")
    assert node == Anchor(P("revenue"), ())
    assert node.levels == () and node.composite is True
    assert canonical("revenue @ {}") == "revenue @ {}"


def test_equals_compares_and_colon_names_an_argument():
    """§15.2's closing rule: "`=` compares. `:` names an argument.", and it is syntactic — nothing
    about `variance` or `if` is consulted to decide."""
    variance = parse("variance(price, ddof: 1)")
    assert variance == Call(P("variance"), (P("price"),), (NamedArg("ddof", Literal(1)),))

    conditional = parse('if(region = "east", 1, 0)')
    assert conditional == Call(
        P("if"),
        (Compare("=", P("region"), Literal("east")), Literal(1), Literal(0)),
        (),
    )
    # …and the comparison really is a comparison, not a named argument that lost its name.
    assert conditional.named == ()
    assert isinstance(conditional.args[0], Compare)


def test_comparison_outside_a_call_is_always_a_comparison():
    assert parse('region = "east"') == Compare("=", P("region"), Literal("east"))
    assert parse("a.b = 1") == Compare("=", P("a", "b"), Literal(1))


def test_historical_name_equals_value_canonicalizes_to_colon_form():
    """§15.2: historical `name = value` call spellings "canonicalize to colon form". They parse to
    the SAME node, so nothing downstream can tell which spelling was written."""
    for historical, colon in [
        ("cumsum(revenue, by = cal.day)", "cumsum(revenue, by: cal.day)"),
        ("cumsum(revenue, within = {customer})", "cumsum(revenue, within: {customer})"),
        ("rolling_mean(revenue, window = 7)", "rolling_mean(revenue, window: 7)"),
        ("lag(revenue, n = 1)", "lag(revenue, n: 1)"),
    ]:
        assert parse(historical) == parse(colon), historical
        # and the canonical spelling of the historical form IS the colon form
        assert canonical(historical) == canonical(colon)
        assert ":" in canonical(historical) and "=" not in canonical(historical)

    # The spelling is still RECOVERABLE for the §15.2 governed-capability gate, without being part
    # of the node's identity.
    assert parse("cumsum(revenue, by = cal.day)").named[0].historical is True
    assert parse("cumsum(revenue, by: cal.day)").named[0].historical is False


def test_the_historical_spelling_yields_to_a_later_positional_argument():
    """The discriminator between `f(by = cal.day)` and `if(region = "east", 1, 0)`: §15.2's own
    "positional arguments must precede named arguments" makes the named reading impossible when a
    positional argument follows, so there the `=` stays the comparison it parsed as."""
    trailing = parse("f(by = cal.day)")
    assert trailing.named == (NamedArg("by", P("cal", "day")),) and trailing.args == ()

    followed = parse("f(by = cal.day, 1)")
    assert followed.named == ()
    assert followed.args == (Compare("=", P("by"), P("cal", "day")), Literal(1))


def test_the_comparison_reading_can_be_forced_in_trailing_position():
    """Documented escape hatch: parenthesize, or write `==`."""
    for text in ["f(a, (b = c))", "f(a, b == c)"]:
        node = parse(text)
        assert node.named == (), text
        assert node.args == (P("a"), Compare("=", P("b"), P("c"))), text
    # …and the canonical rendering must not quietly undo it on the next read.
    assert parse(canonical("f(a, (b = c))")) == parse("f(a, (b = c))")
    assert canonical("f(a, (b = c))") == "f(a, (b = c))"


def test_positional_arguments_must_precede_named_ones():
    """§15.2: "Positional arguments must precede named arguments." Refused by name."""
    with pytest.raises(FrameQLSyntaxError) as exc:
        parse("variance(ddof: 1, price)")
    assert "ddof" in str(exc.value)
    assert "positional" in str(exc.value).lower()


def test_a_dotted_path_is_one_shape_and_resolution_is_deferred():
    """§15.1: `level.last` and `a.b.c` are ONE dotted-path shape. Splitting them into a base and
    member access is "a per-context semantic conformance check … not a lexer-only or parser-only
    decision", so the parser does not attempt it."""
    assert parse("level.last") == P("level", "last")
    assert parse("a.b.c") == P("a", "b", "c")
    # parentheses make the value-access chaining explicit, and that IS a different written intent
    assert parse("(a.b).c") == Member(P("a", "b"), "c")
    different_shape("(a.b).c", "a.b.c")
    # a call on a dotted path is a call on the WHOLE path — the parser takes no view on whether
    # `graph.neighbors` is a governed extension name or a method fetched off `graph`
    assert parse("graph.neighbors(node, depth: 2)") == Call(
        P("graph", "neighbors"), (P("node"),), (NamedArg("depth", Literal(2)),))


def test_a_tuple_and_an_ordering_specification_are_one_syntactic_structure():
    """§15.3: `(revenue, cost)` is a tuple; `by: (customer, cal.day)` is ordered coordinate
    precedence. "This is semantic typing of one syntactic structure, not a parse ambiguity." """
    assert parse("(revenue, cost)") == Tuple((P("revenue"), P("cost")))
    ordering = parse("cumsum(revenue, by: (customer, cal.day))")
    assert ordering.named == (NamedArg("by", Tuple((P("customer"), P("cal", "day")))),)
    # the two are the SAME node type; only the position differs
    assert type(parse("(revenue, cost)")) is type(ordering.named[0].value)
    # a tuple is NOT an anchor — `{customer, cal.day}` is
    different_shape("(customer, cal.day)", "{customer, cal.day}")
    assert parse("{customer, cal.day}") == Anchor(None, (P("customer"), P("cal", "day")))


def test_a_grain_literal_may_stand_alone_as_an_argument_value():
    """§15.2 writes `within: {customer}` — a brace group in value position, not after an `@`."""
    node = parse("cumsum(revenue, by: cal.day, within: {customer})")
    assert node == Call(
        P("cumsum"), (P("revenue"),),
        (NamedArg("by", P("cal", "day")), NamedArg("within", Anchor(None, (P("customer"),)))),
    )


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# 2. the ladder: one test per ADJACENT pair of rungs, then associativity
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def test_rung_pair_1_primary_then_postfix():
    """A postfix operation applies to the primary next to it, not to a larger expression."""
    same_shape("a.b(c)", "(a.b)(c)")
    same_shape("f(x)[k]", "(f(x))[k]")
    assert parse("a.b(c)") == Call(P("a", "b"), (P("c"),))


def test_rung_pair_2_postfix_then_anchor():
    same_shape("state.cardinality @ {account}", "(state.cardinality) @ {account}")
    same_shape("f(x) @ {a}", "(f(x)) @ {a}")
    same_shape("m[k] @ {a}", "(m[k]) @ {a}")


def test_rung_pair_3_anchor_then_numeric_unary():
    same_shape("-revenue @ {customer}", "-(revenue @ {customer})")
    same_shape("+revenue @ {customer}", "+(revenue @ {customer})")


def test_rung_pair_4_numeric_unary_then_multiplicative():
    same_shape("-a * b", "(-a) * b")
    same_shape("a * -b", "a * (-b)")
    different_shape("-a * b", "-(a * b)")


def test_rung_pair_5_multiplicative_then_additive():
    same_shape("a + b * c", "a + (b * c)")
    same_shape("a * b + c", "(a * b) + c")
    same_shape("a - b % c", "a - (b % c)")
    different_shape("a + b * c", "(a + b) * c")


def test_rung_pair_6_additive_then_comparison():
    same_shape("a + b = c", "(a + b) = c")
    same_shape("a < b - c", "a < (b - c)")
    same_shape("a + b IN c", "(a + b) IN c")
    different_shape("a + b = c", "a + (b = c)")


def test_rung_pair_7_comparison_then_logical():
    same_shape("a = 1 AND b = 2", "(a = 1) AND (b = 2)")
    same_shape("NOT a = 1", "NOT (a = 1)")
    same_shape("a > 1 OR b < 2", "(a > 1) OR (b < 2)")
    different_shape("NOT a = 1", "(NOT a) = 1")


def test_rung_pair_8_not_then_and():
    """Inside the logical rung, §15 orders NOT, then AND, then OR."""
    same_shape("NOT a AND b", "(NOT a) AND b")
    different_shape("NOT a AND b", "NOT (a AND b)")


def test_rung_pair_9_and_then_or():
    same_shape("a AND b OR c", "(a AND b) OR c")
    same_shape("a OR b AND c", "a OR (b AND c)")
    different_shape("a AND b OR c", "a AND (b OR c)")


def test_associativity_of_subtraction_is_left():
    assert parse("a - b - c") == Binary("-", Binary("-", P("a"), P("b")), P("c"))
    same_shape("a - b - c", "(a - b) - c")
    different_shape("a - b - c", "a - (b - c)")


def test_associativity_of_division_is_left():
    assert parse("a / b / c") == Binary("/", Binary("/", P("a"), P("b")), P("c"))
    same_shape("a / b / c", "(a / b) / c")
    different_shape("a / b / c", "a / (b / c)")


def test_associativity_of_anchor_ascription_is_left():
    assert parse("a @ {b} @ {c}") == Anchor(Anchor(P("a"), (P("b"),)), (P("c"),))
    same_shape("a @ {b} @ {c}", "(a @ {b}) @ {c}")


def test_associativity_of_value_access_is_left():
    assert parse("f(x).a.b") == Member(Member(Call(P("f"), (P("x"),)), "a"), "b")
    same_shape("f(x).a.b", "((f(x)).a).b")


def test_logical_operators_flatten_as_written():
    """`a AND b AND c` is one n-ary node; an explicitly nested one keeps its nesting."""
    assert parse("a AND b AND c") == Logical("AND", (P("a"), P("b"), P("c")))
    assert parse("a AND (b AND c)") == Logical("AND", (P("a"), Logical("AND", (P("b"), P("c")))))
    different_shape("a AND b AND c", "a AND (b AND c)")


def test_comparison_does_not_chain():
    """§15 gives no reading for `a < b < c` — neither Python's nor SQL's — so it is refused rather
    than guessed. A resolver cannot repair a grouping the parser invented."""
    with pytest.raises(FrameQLSyntaxError) as exc:
        parse("a < b < c")
    assert "chain" in str(exc.value)
    # the remedy in the message is itself well-formed
    parse("(a < b) AND (b < c)")


def test_between_takes_two_bounds_and_its_AND_is_not_a_conjunction():
    node = parse("day BETWEEN '2024-01-01' AND '2024-01-31'")
    assert node == Compare("BETWEEN", P("day"),
                           Tuple((Literal("2024-01-01"), Literal("2024-01-31"))))
    assert not isinstance(node, Logical)
    with pytest.raises(FrameQLSyntaxError) as exc:
        parse("day BETWEEN 1")
    assert "BETWEEN" in str(exc.value)


def test_not_in_is_refused_and_names_the_form_that_works():
    with pytest.raises(FrameQLSyntaxError) as exc:
        parse("a NOT IN b")
    assert "NOT (a IN b)" in str(exc.value)
    assert parse("NOT (a IN b)") == Unary("NOT", Compare("IN", P("a"), P("b")))


def test_keywords_are_case_insensitive_but_the_spelling_survives():
    assert parse("a and b") == parse("a AND b")
    assert parse("a in b") == parse("a IN b")
    assert parse("not a") == parse("NOT a")
    assert parse("a and b").raw_op == "and"
    assert canonical("a and b") == "a AND b"


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# 3. brackets — subscription, never filtering (§15.4, §7.5)
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def test_postfix_bracket_subscription():
    assert parse("E[key]") == Subscript(P("E"), P("key"))
    assert parse("E[i][j]") == Subscript(Subscript(P("E"), P("i")), P("j"))
    assert canonical("E[i][j]") == "E[i][j]"


def test_a_bracket_key_is_a_full_expression():
    assert parse("basket['sku']") == Subscript(P("basket"), Literal("sku"))
    assert parse("m[a + 1]") == Subscript(P("m"), Binary("+", P("a"), Literal(1)))
    # a tuple key, for a type that needs several coordinates (§15.4)
    assert parse("grid[i, j]") == Subscript(P("grid"), Tuple((P("i"), P("j"))))
    assert canonical("grid[i, j]") == "grid[i, j]"


def test_the_roadmap_bracket_filter_parses_and_is_left_for_the_resolver():
    """§7.5: `revenue[region = "east"]` "parses, if at all, only as subscription by the Boolean
    result of `region = "east"`" and is then a TYPE error, not a syntax error. The old dialect
    answered it in CPython's voice ("Maybe you meant '==' or ':=' instead of '='?"); it must now
    simply parse."""
    node = parse('revenue[region = "east"]')
    assert node == Subscript(P("revenue"), Compare("=", P("region"), Literal("east")))


def test_filter_shaped_subscripts_reports_shape_without_judging_it():
    """§7.5 asks for a diagnostic that "should point the writer toward `WHERE` or `HAVING`". The
    parser supplies the finding, never the verdict."""
    node = parse('sum(revenue[region = "east"]) + basket["sku"]')
    found = expr.filter_shaped_subscripts(node)
    assert len(found) == 1
    assert found[0].base == P("revenue")
    assert isinstance(found[0].key, Compare)
    # an ordinary key is NOT reported — the helper takes no position on admissibility
    assert expr.filter_shaped_subscripts(parse('basket["sku"]')) == ()
    assert len(expr.filter_shaped_subscripts(parse("a[b AND c]"))) == 1
    assert len(expr.filter_shaped_subscripts(parse("a[NOT b]"))) == 1


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# 4. the error channel — FrameQLSyntaxError, always, with an offset
# ═══════════════════════════════════════════════════════════════════════════════════════════════

#: Every one of these is a rejection. What matters is not WHICH is refused — that is the grammar's
#: business — but that each is refused in Frame-QL's own channel.
REJECTED = [
    "", "   ", "(", ")", "a +", "+ ", "a b", "()a", "a.", ".a", "a..b", "f(", "f(a,", "f(,a)",
    "f(a,)", "a[", "a[]", "a[b", "@", "a @", "a @ {", "a @ {}}", "a @ {*}", "a @ {a*}", "a @ {,b}",
    "a @ (a b)", "{", "{a", "a @ 1", "a @ 'x'", "count(*)", "a * ", "'unterminated", '"also',
    "a $ b", "a ? b", "3abc", "a < b < c", "a NOT IN b", "a NOT BETWEEN 1 AND 2", "a BETWEEN 1",
    "f(a: 1, 2)", "f(a: 1, a: 2)", "f(a = 1, a = 2)", "AND", "OR a", "a AND", "a IN", "NOT",
    "a ==", "a != ", "((a)", "a))", "a @ {b} @", "revenue.", "f(x).", "f(x).(y)", "1 2",
]


@pytest.mark.parametrize("text", REJECTED, ids=lambda t: repr(t))
def test_every_rejection_rides_the_frameql_channel(text):
    """The P1-26 guarantee (planner.py:27-42), restated for a parser with no substrate under it: the
    reader is never answered in another language's voice. `FrameQLSyntaxError` exactly — not a bare
    `SyntaxError`, `ValueError`, `AttributeError`, `IndexError` or `TypeError`."""
    with pytest.raises(FrameQLSyntaxError) as exc:
        expr.parse(text)
    assert type(exc.value) is FrameQLSyntaxError
    assert not isinstance(exc.value, SyntaxError)


@pytest.mark.parametrize("text", REJECTED, ids=lambda t: repr(t))
def test_every_rejection_says_where(text):
    try:
        expr.parse(text)
    except FrameQLSyntaxError as err:
        assert isinstance(getattr(err, "offset", None), int)
        assert 0 <= err.offset <= len(text)
        assert "offset" in str(err)
        return
    pytest.fail(f"{text!r} was not rejected")


def test_a_rejection_names_a_remedy():
    """The envelope's four-mood temperament: say what is wrong, then name the way out."""
    with pytest.raises(FrameQLSyntaxError) as exc:
        parse("count(*)")
    message = str(exc.value)
    assert "wildcard" in message and "e.g." in message
    # and it says nothing about Python
    assert "Python" not in message and "star expression" not in message


def test_no_python_exception_escapes_a_mutilated_expression():
    """A mechanical sweep: every prefix of, and every single-character deletion from, every corpus
    expression. Most are nonsense; NONE may raise anything but `FrameQLSyntaxError`."""
    checked = 0
    for source in CORPUS[:40]:
        mutations = [source[:i] for i in range(len(source) + 1)]
        mutations += [source[:i] + source[i + 1:] for i in range(len(source))]
        for text in mutations:
            checked += 1
            try:
                expr.parse(text)
            except FrameQLSyntaxError:
                pass
            except BaseException as err:                       # noqa: BLE001 - that is the point
                pytest.fail(f"{text!r} escaped as {type(err).__name__}: {err}")
    assert checked > 1000


def test_deep_nesting_is_refused_rather_than_crashing_the_interpreter():
    with pytest.raises(FrameQLSyntaxError) as exc:
        expr.parse("(" * 5000 + "a" + ")" * 5000)
    assert type(exc.value) is FrameQLSyntaxError


def test_non_text_input_is_a_frameql_error():
    for bad in (None, 42, [], {"a": 1}):
        with pytest.raises(FrameQLSyntaxError):
            expr.parse(bad)


def test_brackets_inside_a_string_are_not_brackets():
    """The balance check runs over TOKENS, so a bracket inside a literal is a character."""
    assert parse("cumsum(revenue, by = '(')") == Call(
        P("cumsum"), (P("revenue"),), (NamedArg("by", Literal("(")),))
    with pytest.raises(FrameQLSyntaxError) as exc:
        parse("f(a")
    assert "never closed" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# 5. the corpus — harvested mechanically, never hand-listed
# ═══════════════════════════════════════════════════════════════════════════════════════════════

REPO = pathlib.Path(__file__).resolve().parents[3]
MANUAL = REPO / "docs" / "frame_ql_language.md"
PACKAGES = REPO / "packages"

# The Manual's own extractor conventions (docs/tools/check_manual_frameql.py), reused so this test
# harvests exactly the blocks that gate already treats as examples.
_FENCE = re.compile(r"^(\s*)```([A-Za-z0-9_-]*)\s*$")
_BLOCKQUOTE = re.compile(r"^\s{0,3}> ?")
_ANNOTATION = re.compile(r"\s*--.*$")
_STMT_START = re.compile(r"^\s*(EXPLAIN|FROM|WITH|SELECT)\b", re.IGNORECASE)
_SELECT = re.compile(r"\bSELECT\b", re.IGNORECASE)

#: A statement written as an f-string is a TEMPLATE, not an expression (`max(revenue @ {{{L}}})`),
#: so string literals carrying an `f` prefix are skipped at the source. Nothing is hand-excluded.
_STATEMENT_LITERAL = re.compile(
    r"""(?<![A-Za-z0-9_])(?:r|b|rb|br)?(['"]{1,3})((?:FROM|SELECT|EXPLAIN|WITH)\b.*?)\1""",
    re.DOTALL | re.IGNORECASE)
_COLUMN_CALL = re.compile(
    r"""\.column\(\s*(?:r)?(['"])(?:.*?)\1\s*,\s*(?:r)?(['"])(.*?)\2""", re.DOTALL)
_DERIVED = re.compile(r"^\s*DERIVED\s+\w+\s*=\s*(.+?)\s*$", re.MULTILINE)


def _fenced_blocks(text: str):
    out, i, lines = [], 0, [_BLOCKQUOTE.sub("", ln) for ln in text.splitlines()]
    while i < len(lines):
        match = _FENCE.match(lines[i])
        if match:
            info, body = match.group(2), []
            i += 1
            while i < len(lines) and not _FENCE.match(lines[i]):
                body.append(lines[i])
                i += 1
            out.append((info.lower(), "\n".join(body)))
        i += 1
    return out


def _statements(body: str):
    stmts, cur, has_select, depth = [], [], False, 0
    for line in body.splitlines():
        line = _ANNOTATION.sub("", line)
        if depth == 0 and _STMT_START.match(line) and has_select and cur:
            stmts.append("\n".join(cur).strip())
            cur, has_select = [], False
        cur.append(line)
        if depth == 0 and _SELECT.search(line):
            has_select = True
        depth += line.count("(") + line.count("{") + line.count("[")
        depth -= line.count(")") + line.count("}") + line.count("]")
    if "\n".join(cur).strip():
        stmts.append("\n".join(cur).strip())
    return [s for s in stmts if s and _SELECT.search(s)]


def _expressions_of(statement: str, into: set):
    """Every EXPRESSION a statement carries: its series, its WITH bindings, its predicates. The
    envelope parser does the splitting, so this harvest cannot disagree with the shipped clause
    boundaries."""
    try:
        parsed = parse_statement(statement)
    except Exception:                                          # not a well-formed statement; skip
        return
    for series in parsed.series:
        into.add(series.expr.strip())
    for binding in parsed.bindings:
        into.add(binding.expr.strip())
    for predicate in list(parsed.where) + list(parsed.having):
        into.add(predicate.strip())


def _harvest() -> list[str]:
    """The corpus, gathered mechanically from the three places real Frame-QL expressions live."""
    found: set[str] = set()

    # (a) every fenced Frame-QL example in the Manual
    if MANUAL.exists():
        for info, body in _fenced_blocks(MANUAL.read_text()):
            if info not in ("frameql", "frameql-schematic", ""):
                continue
            for statement in _statements(body):
                _expressions_of(statement, found)

    # (b) every column expression and every embedded statement in the test suites
    for source in sorted(PACKAGES.rglob("*.py")):
        text = source.read_text(errors="ignore")
        for match in _COLUMN_CALL.finditer(text):
            found.add(match.group(3).strip())
        for match in _STATEMENT_LITERAL.finditer(text):
            _expressions_of(_ANNOTATION.sub("", match.group(2)), found)

    # (c) every derived-column formula declared in a manifold
    for source in sorted(REPO.rglob("*.cml")):
        for match in _DERIVED.finditer(source.read_text(errors="ignore")):
            found.add(_ANNOTATION.sub("", match.group(1)).strip())

    # A schematic template (`op(col_1 @ {a_1}, …)`) asserts a shape, not an expression.
    return sorted(e for e in found if e and "..." not in e and "…" not in e)


CORPUS = _harvest()


def _old_dialect_tree(source: str):
    """The tree the OLD dialect produced for this text, or None if it did not accept it.

    "Accepted by the old dialect" has a precise meaning in this repository and it is not "CPython
    could parse it": the planner converted anchors first (`_convert_input_anchor`) and then admitted
    only the node types in `planner._ALLOWED`. Both halves are frozen above, verbatim, so the cohort
    is defined by the code that shipped rather than by this test's opinion."""
    try:
        tree = ast.parse(_retired_convert_input_anchor(source), mode="eval")
    except Exception:
        return None
    if not all(isinstance(node, _RETIRED_ALLOWED) for node in ast.walk(tree)):
        return None
    return tree


def test_the_corpus_is_real_and_large_enough_to_mean_something():
    assert len(CORPUS) >= 100, f"only harvested {len(CORPUS)} expressions"
    cohort = [s for s in CORPUS if _old_dialect_tree(s) is not None]
    assert len(cohort) >= 100, f"only {len(cohort)} of {len(CORPUS)} are old-dialect expressions"


@pytest.mark.parametrize("source", CORPUS, ids=lambda s: s[:60])
def test_every_corpus_expression_parses(source):
    """Whatever else changes, the new grammar must not have lost a form the repository uses."""
    assert isinstance(expr.parse(source), expr.Node)


@pytest.mark.parametrize("source", CORPUS, ids=lambda s: s[:60])
def test_ast_fidelity_over_the_corpus(source):
    """THE PRIMARY CONTRACT.

    For every expression the old dialect accepted, the HOST rendering of the new parse is
    BYTE-IDENTICAL to `ast.unparse(ast.parse(…).body)`. `ast.unparse` builds reader-facing refusal
    text at fourteen sites in the planner and stands behind wire-visible column keys; a substitution
    that moved one byte of either would be a silent contract change."""
    tree = _old_dialect_tree(source)
    if tree is None:
        pytest.skip("not an expression the old ast-hosted dialect accepted")
    assert expr.unparse(expr.parse(source), dialect=expr.HOST) == ast.unparse(tree.body)


@pytest.mark.parametrize("source", CORPUS, ids=lambda s: s[:60])
def test_round_trip_is_structure_preserving(source):
    """`parse(unparse(parse(s))) == parse(s)` — structural equality. The canonical text a reader (or
    a column key) is shown must mean exactly what was written."""
    node = expr.parse(source)
    assert expr.parse(expr.unparse(node)) == node


@pytest.mark.parametrize("source", CORPUS, ids=lambda s: s[:60])
def test_canonical_text_is_a_fixed_point(source):
    """Canonicalization is idempotent: re-canonicalizing canonical text changes nothing. A key that
    drifted on a second pass would not be an identity."""
    once = expr.unparse(expr.parse(source))
    twice = expr.unparse(expr.parse(once))
    assert once == twice


@pytest.mark.parametrize("source", CORPUS, ids=lambda s: s[:60])
def test_host_text_is_a_fixed_point(source):
    node = expr.parse(source)
    once = expr.unparse(node, dialect=expr.HOST)
    assert expr.unparse(expr.parse(once), dialect=expr.HOST) == once


def test_canonical_anchor_spelling_agrees_with_the_shipped_canonicalizer():
    """`Planner._canon_expr` already normalizes anchors to the brace product. The new canonical
    dialect must spell them the same way, or a column key would move under the migration."""
    for source, expected in [
        ("avg(aov@day)", "avg(aov @ {day})"),
        ("avg(aov @ {day})", "avg(aov @ {day})"),
        ("avg(aov @ {day, store})", "avg(aov @ {day*store})"),
        ("avg(aov @ {day*store})", "avg(aov @ {day*store})"),
        ("revenue @ {}", "revenue @ {}"),
        ("revenue @ (a, b)", "revenue @ {a*b}"),
    ]:
        assert canonical(source) == expected, source


def test_host_anchor_spelling_agrees_with_the_shipped_converter():
    """The mirror image: HOST must spell a pin exactly as the retired `_convert_input_anchor` did,
    since that is the text the old dialect saw."""
    for source in ["avg(aov @ {day})", "avg(aov @ {day, store})", "revenue @ {}", "avg(aov@day)"]:
        converted = _retired_convert_input_anchor(source)
        assert host(source) == ast.unparse(ast.parse(converted, mode="eval").body), source


def test_the_two_dialects_agree_everywhere_except_the_documented_four_places():
    """Anchor spelling, named-argument spelling, the `Member` parentheses and the `@`/unary rungs —
    and nothing else."""
    for source in ["revenue", "a.b.c", "revenue.sum / orders.count", "f(a, b)", "a[b]",
                   "(a + b) * c", "-a", "'east'", "1.5", "(a, b)"]:
        assert canonical(source) == host(source), source
    for source in ["revenue @ {day}", "f(a, b: 1)", "(a.b).c", "-a @ {b}", "(revenue/orders) @ {c}"]:
        assert canonical(source) != host(source), source


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# 6. the tokenizer surface
# ═══════════════════════════════════════════════════════════════════════════════════════════════

def test_both_quote_styles_mean_the_same_literal():
    assert parse("'east'") == parse('"east"') == Literal("east")
    assert parse("'east'").raw == "'east'"
    assert parse('"east"').raw == '"east"'


def test_numbers():
    assert parse("7") == Literal(7)
    assert parse("1.5") == Literal(1.5)
    assert parse("-1") == Unary("-", Literal(1))
    assert parse("1e3") == Literal(1000.0)
    assert canonical("1e3") == "1000.0" == ast.unparse(ast.parse("1e3", mode="eval").body)


def test_every_token_carries_its_offset():
    tokens = expr.tokenize("revenue @ {day}")
    assert [t.pos for t in tokens] == [0, 8, 10, 11, 14, 15]
    assert [t.kind for t in tokens] == ["name", "op", "op", "name", "op", "end"]
    assert tokens[0].text == "revenue"


def test_whitespace_is_not_significant():
    assert parse("a+b*c") == parse("  a  +  b  *  c  ") == parse("a +\n  b * c")


def test_repr_is_useful_when_a_test_fails():
    assert repr(parse("revenue @ {a*b}")) == "Anchor(Path(revenue) @ {a * b})"
    assert repr(parse("f(x, n: 1)")) == "Call(Path(f), [Path(x), NamedArg(n: Literal(1))])"
    assert repr(parse("a = 'b'")) == "Compare(=, Path(a), Literal('b'))"


def test_nodes_are_hashable_and_compare_by_meaning_not_spelling():
    assert parse("a @ day") == parse("a @ {day}")               # the pin sugars are the same pin
    assert parse('a = "x"') == parse("a = 'x'")                 # the quote styles are the same literal
    assert parse("a and b") == parse("a AND b")                 # keyword case is not meaning
    assert len({parse("a @ day"), parse("a @ {day}")}) == 1


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# 7. the grammar AT THE PLANNER — the dialect is the one the planner actually reads
# ═══════════════════════════════════════════════════════════════════════════════════════════════
#
# Sections 1-6 prove the PARSER. These prove that the parser is what the planner uses: that a §15
# rule proved above is the rule a reader meets through `ManifoldServer`, and not a second dialect
# that happens to live in the same repository. That distinction is the whole content of phase 2 —
# before it, `columna_core.expr` was correct and unreachable.


def _series(server, anchor, source: str):
    """One series through the BUILDER API, with the expression passed as a VALUE.

    Deliberately not written as an inline builder call with two literal arguments at each call site.
    `_harvest()` above scrapes exactly that shape out of every `.py` file under `packages/`, so a
    literal here would enrol these tests' intentionally-malformed probes (`revenue $$ 2`) into the
    very corpus section 5 requires to parse. One helper keeps the probes out of their own fixture."""
    return server.frame(*anchor).column("c", source)


def _refusal(fr, name="c"):
    col = next(c for c in fr.columns if c.name == name)
    return col.refusal


def test_the_planner_parses_with_this_grammar_and_no_other(fixture_server):
    """The load-bearing claim: the planner's expression door IS `expr.parse`.

    Asserted at the seam rather than by behaviour, because a behavioural proxy ("it accepts braces")
    would keep passing if a second reader were introduced that also accepted braces."""
    from columna_core import planner as P
    assert P._parse_expr("revenue @ {day}") == expr.parse("revenue @ {day}")
    assert isinstance(P._parse_expr("revenue"), expr.Node)
    # and the retired substrate is gone from the module entirely
    assert not hasattr(P, "_ALLOWED")
    assert not hasattr(P.Planner, "_convert_input_anchor")
    assert not hasattr(P.Planner, "_INPUT_ANCHOR_BRACE")


def test_one_grammar_for_the_builder_api_and_the_statement_path(fixture_server):
    """The two doors into the planner accept the SAME language.

    They did not. `desugar()` ran a text shim that rewrote `@ {day}` into `@ day` before the CPython
    substrate saw it, and `run()` — the builder API — never called that shim, so the braced pin was
    served through one door and refused "illegal expression construct" through the other. The
    acceptance set of the expression language depended on the caller's entry point, which means
    there were two languages. Braces are native now; there is one."""
    builder = _series(fixture_server, ("cal.month",), "avg(revenue @ {day})").run()
    statement = fixture_server.planner.run_statement(
        parse_statement("SELECT avg(revenue @ {day}) AS c AT {cal.month}"))
    assert _refusal(builder) is None and _refusal(statement) is None
    # Compared as ROWS rather than with `DataFrame.equals`: the two frames carry identical values and
    # schemas but different internal chunk layouts, and `equals` is sensitive to that in a way that
    # has nothing to do with the claim under test.
    assert (builder.data.sort("cal.month").rows()
            == statement.data.sort("cal.month").rows())
    assert builder.data.columns == statement.data.columns
    assert builder.data.height == 24


def test_a_filter_shaped_subscript_is_refused_and_names_the_clause_that_filters(fixture_server):
    """§7.5, end to end: `revenue[region = 'east']` earns a NAMED refusal pointing at WHERE/HAVING.

    This is the P1-26 leak in its purest form. `ast.Subscript` was not in the retired `_ALLOWED`, so
    the form never even reached the allow-list — it died as a raw CPython `SyntaxError` whose text
    was "Maybe you meant '==' or ':=' instead of '='?", which is advice about Python's walrus
    operator delivered to someone writing an analytical filter. §7.5 asks instead for a diagnostic
    that "should point the writer toward `WHERE` or `HAVING` rather than silently reinterpret the
    brackets as a filter", and that is what is asserted here — including that it is a REFUSAL and not
    a reinterpretation, because serving a filtered number for this would answer a question nobody
    asked in the one syntax the specification names as where that mistake happens."""
    fr = _series(fixture_server, ("region",), "revenue[region = 'east']").run()
    r = _refusal(fr)
    assert r is not None and r.reason == "bracket_is_not_a_filter"
    assert "WHERE" in r.detail and "HAVING" in r.detail
    assert any("WHERE" in a for a in r.alternatives)
    assert "walrus" not in r.detail and ":=" not in r.detail and "Python" not in r.detail
    # NOT a silent reinterpretation: no data, no value, no frame
    assert fr.data is None
    # the same shape is refused identically on the compile-only path (EXPLAIN must not say serve)
    replanned = _series(fixture_server, ("region",), "revenue[region = 'east']").plan()
    assert _refusal(replanned).reason == "bracket_is_not_a_filter"


def test_an_ordinary_subscript_is_refused_differently_and_never_crashes(fixture_server):
    """A non-filter-shaped subscript is well-formed 1.0 that this build has no reading for. It gets
    the vocabulary refusal, NOT the §7.5 one — the bracket diagnostic must not become a catch-all for
    every bracket, or it would start pointing readers at WHERE for asks that have nothing to do with
    filtering."""
    r = _refusal(_series(fixture_server, ("region",), "revenue['sku']").run())
    assert r is not None and r.reason == "unknown" and r.reason != "bracket_is_not_a_filter"
    assert "revenue['sku']" in r.detail


def test_a_malformed_series_is_a_language_error_not_a_build_capability_gap(fixture_server):
    """`$` is in no Frame-QL expression. That is a fact about the ASK, so it classifies LANGUAGE.

    It used to fall into `run()`'s everything-classifies backstop and be reported as "this frame
    could not be resolved in the engine (FrameQLSyntaxError); the ask is not supported in this build"
    — a capability claim about a string that never described an ask at all. The message is now the
    parser's own, with its offset and its remedy."""
    r = _refusal(_series(fixture_server, ("region",), "revenue $$ 2").run())
    assert r is not None and r.is_error
    assert "not supported in this build" not in r.detail
    assert "offset" in r.detail


def test_the_default_column_key_is_canonical_frame_ql_1_0_text(fixture_server):
    """§4 column identity (WP-NAME-1) keys an unaliased series by its CANONICAL expression, and the
    canonical dialect is now 1.0's (`contract_version` "4" -> "5").

    Two spellings of one pin produce ONE key, which is the property that makes a key an identity
    rather than a transcription. The middle case is the one that used to fail: the retired regex
    canonicalizer normalized the brace and left everything else — including the author's spaces, and
    including a space it failed to insert itself (`avg(revenue@ {day})`)."""
    for written in ["avg(revenue @ {day})", "avg(revenue@day)", "avg( revenue @ {day} )",
                    "avg(revenue @ day)"]:
        fr = fixture_server.planner.run_statement(
            parse_statement(f"SELECT {written} AT {{cal.month}}"))
        assert [c.name for c in fr.columns] == ["avg(revenue @ {day})"], written


def test_a_named_argument_is_one_ask_in_both_spellings_and_is_taught_with_a_colon(fixture_server):
    """§15.2: "`=` compares. `:` names an argument." — with `name = value` kept as compatibility
    INPUT that canonicalizes to the colon form.

    Both halves matter and they pull in opposite directions, so both are pinned: nothing already
    written stops working, and nothing Columna SAYS recommends the retiring spelling."""
    colon = fixture_server.planner.desugar(
        parse_statement("SELECT lag(revenue, n: 1) AS c AT {cal.month}"))
    equals = fixture_server.planner.desugar(
        parse_statement("SELECT lag(revenue, n=1) AS c AT {cal.month}"))
    assert colon.series[0].expr == equals.series[0].expr == "lag(revenue, n: 1)"
    # a refusal that names a parameter spells it with the colon
    r = _refusal(_series(fixture_server, ("region",), "lag(revenue, zzz: 1)").run())
    assert "n:" in r.detail and "n=" not in r.detail


def test_no_planner_refusal_ever_answers_in_the_substrate_voice(fixture_server):
    """The P1-26 guarantee, swept over the forms that used to leak it.

    Each of these was once answered by CPython talking about Python — "Invalid star expression",
    "Maybe you meant '==' or ':=' instead of '='?", "illegal expression construct: Subscript". None
    may mention Python, a Python node class, or a Python operator, and none may escape as a raw
    exception that is not the language's own."""
    forbidden = ("Python", "walrus", ":=", "star expression", "ast.", "SyntaxError:",
                 "illegal expression construct")
    for text in ["count(*)", "revenue[region = 'east']", "revenue @ 1", "revenue $$ 2",
                 "revenue.sum.extra.more", "(revenue", "revenue AND orders", "revenue < 1 < 2"]:
        try:
            fr = _series(fixture_server, ("region",), text).run()
        except FrameQLSyntaxError as err:            # the language's own channel, by name
            assert type(err) is FrameQLSyntaxError
            message = str(err)
        else:
            r = _refusal(fr)
            assert r is not None, f"{text!r} must not serve"
            message = r.detail
        for bad in forbidden:
            assert bad not in message, f"{text!r} answered in the substrate's voice: {message!r}"


def test_the_published_grammar_surface_states_the_rules_it_is_read_under(fixture_server):
    """`envelope.__doc__` is returned VERBATIM by the MCP `frame_ql_grammar` tool, so it is the
    published grammar. It must not be silent about the rules a writer will trip over first."""
    from columna_core import envelope
    doc = envelope.__doc__
    assert "`=` COMPARES. `:` NAMES AN ARGUMENT." in doc
    assert "PRECEDENCE LADDER" in doc
    for rung in ["postfix", "anchor ascription", "numeric unary", "multiplicative", "additive",
                 "comparison", "logical"]:
        assert rung in doc, rung
    assert "binds TIGHTER than arithmetic" in doc          # the one place §15 and CPython disagree
    assert "BRACKETS SUBSCRIBE" in doc
    assert "DOTTED ACCESS IS ONE SHAPE" in doc

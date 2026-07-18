"""
test_frameql_parse.py — the Frame-QL envelope grammar parser.

Promoted from columna-server with `parse_frameql` (ADR-035 D3: the query surface is canonical and
lives under core's test regime). The grammar is UNCHANGED by the promotion; these are the same tests,
moved with the code. Expression-internal validity is the planner's job, not the envelope's.
"""
import pytest

from columna_core import parse_frameql, FrameQLSyntaxError


def test_bare_expression_names_itself():
    anchor, cols = parse_frameql("revenue @ region")
    assert anchor == ("region",) and cols == [("revenue", "revenue")]


def test_named_columns_and_multi_anchor():
    anchor, cols = parse_frameql("rate: revenue / level.last @ store, day")
    assert anchor == ("store", "day")
    assert cols == [("rate", "revenue / level.last")]


def test_multiple_columns():
    anchor, cols = parse_frameql("rev: revenue, inv: level.last @ store, day")
    assert cols == [("rev", "revenue"), ("inv", "level.last")]


def test_commas_inside_parens_are_not_top_level_separators():
    # a scan call carries keyword commas that must NOT split the column list
    anchor, cols = parse_frameql("m: lag(revenue.sum, n=1) @ cal.month")
    assert anchor == ("cal.month",)
    assert cols == [("m", "lag(revenue.sum, n=1)")]


def test_inner_anchor_pin_is_envelope_transparent():
    # WP-B.1's inner `@` pin lives INSIDE a column expression (paren-guarded); the envelope's top-level
    # `@` split must not be confused by it. (Promotion regression guard for the current grammar.)
    anchor, cols = parse_frameql("x: avg(aov@day) @ cal.month")
    assert anchor == ("cal.month",)
    assert cols == [("x", "avg(aov@day)")]


@pytest.mark.parametrize("bad", [
    "", "   ", "revenue", "revenue @", "@ region", "a @ b @ c",
    "SELECT * FROM t", "revenue ; drop table t @ region",
])
def test_envelope_violations_raise(bad):
    with pytest.raises(FrameQLSyntaxError):
        parse_frameql(bad)


# ── the anchor product `*` (WP anchor-grammar, item 1) ──────────────────────────────────────────
# `*` is the canonical anchor separator — the SAME operator as `UNIVERSE a * b * c`. Comma stays
# accepted on input through launch; it retires ONLY in the post-launch hygiene sweep.
def test_anchor_product_star_separates_levels():
    anchor, cols = parse_frameql("revenue @ region*day")
    assert anchor == ("region", "day")
    assert cols == [("revenue", "revenue")]


def test_anchor_product_star_is_whitespace_tolerant():
    for q in ("revenue @ region * day", "revenue @ region *day", "revenue @ region* day"):
        anchor, _ = parse_frameql(q)
        assert anchor == ("region", "day"), q


def test_anchor_comma_still_accepted_alongside_star():
    # RULED: keep-both through launch — the existing comma anchor is untouched.
    assert parse_frameql("revenue @ store, day")[0] == ("store", "day")


def test_inner_anchor_pin_transparent_to_the_star_anchor():
    # the inner `@day` pin lives inside `avg(...)` (paren-guarded); the outer `*` anchor still splits.
    anchor, cols = parse_frameql("x: avg(aov@day) @ store*month")
    assert anchor == ("store", "month")
    assert cols == [("x", "avg(aov@day)")]


def test_star_inside_a_column_expression_is_not_an_anchor_separator():
    # a `*` in the COLUMN list is multiplication, not the anchor product — only the anchor part splits on `*`.
    anchor, cols = parse_frameql("gross: revenue * 1.2 @ region")
    assert anchor == ("region",)
    assert cols == [("gross", "revenue * 1.2")]

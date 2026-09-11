"""
test_frameql_parse.py — a PIN on the retired terse `@`-fragment. Not a test of the language.

The fragment (`revenue @ region`, `rate: revenue / level.last @ store, day`) is not part of Frame-QL
1.0 and is not a public language surface (ruled 2026-09-11). Its parser is quarantined in
`columna_core.frameql` under the private name `_parse_retired_fragment`, kept so the archived text
written in the fragment still has an executable definition of what it meant — see the tombstone there
for the warrant, including why this is lineage and not compatibility.

These tests are what makes that definition worth anything: a preserved reading nobody checks decays
into a preserved guess. So they are kept, and they are kept AS THEY WERE — they pin the fragment's
behaviour at the moment it was retired, and none of them is evidence about the current language.
Frame-QL 1.0's envelope grammar is tested in `test_envelope_parser.py` and its expression dialect in
`test_expression_grammar.py`; nothing here should ever be cited for either.
"""
import pytest

from columna_core import FrameQLSyntaxError
from columna_core.frameql import _parse_retired_fragment


def test_bare_expression_names_itself():
    anchor, cols = _parse_retired_fragment("revenue @ region")
    assert anchor == ("region",) and cols == [("revenue", "revenue")]


def test_named_columns_and_multi_anchor():
    anchor, cols = _parse_retired_fragment("rate: revenue / level.last @ store, day")
    assert anchor == ("store", "day")
    assert cols == [("rate", "revenue / level.last")]


def test_multiple_columns():
    anchor, cols = _parse_retired_fragment("rev: revenue, inv: level.last @ store, day")
    assert cols == [("rev", "revenue"), ("inv", "level.last")]


def test_commas_inside_parens_are_not_top_level_separators():
    # a scan call carries keyword commas that must NOT split the column list
    anchor, cols = _parse_retired_fragment("m: lag(revenue.sum, n=1) @ cal.month")
    assert anchor == ("cal.month",)
    assert cols == [("m", "lag(revenue.sum, n=1)")]


def test_inner_anchor_pin_is_fragment_transparent():
    # The fragment's two `@`s, in one string: the inner pin lives INSIDE a column expression
    # (paren-guarded), the outer one is the output anchor. That the splitter told them apart by depth
    # is the whole reason the form limped along — and that a reader could NOT is why it was retired.
    anchor, cols = _parse_retired_fragment("x: avg(aov@day) @ cal.month")
    assert anchor == ("cal.month",)
    assert cols == [("x", "avg(aov@day)")]


@pytest.mark.parametrize("bad", [
    "", "   ", "revenue", "revenue @", "@ region", "a @ b @ c",
    "SELECT * FROM t", "revenue ; drop table t @ region",
])
def test_fragment_violations_raise(bad):
    with pytest.raises(FrameQLSyntaxError):
        _parse_retired_fragment(bad)


# ── the anchor product `*` (WP anchor-grammar, item 1) ──────────────────────────────────────────
# `*` was the fragment's canonical anchor separator — the SAME operator as `UNIVERSE a * b * c`, and
# the one piece of this grammar the envelope ABSORBED rather than declined: `AT {store * cal.month}`
# spells the product with it today. The comma was a tolerated input spelling and never more.
def test_anchor_product_star_separates_levels():
    anchor, cols = _parse_retired_fragment("revenue @ region*day")
    assert anchor == ("region", "day")
    assert cols == [("revenue", "revenue")]


def test_anchor_product_star_is_whitespace_tolerant():
    for q in ("revenue @ region * day", "revenue @ region *day", "revenue @ region* day"):
        anchor, _ = _parse_retired_fragment(q)
        assert anchor == ("region", "day"), q


def test_anchor_comma_still_accepted_alongside_star():
    # Both spellings were accepted, so both are read back — archived text is not re-spelled.
    assert _parse_retired_fragment("revenue @ store, day")[0] == ("store", "day")


def test_inner_anchor_pin_transparent_to_the_star_anchor():
    # the inner `@day` pin lives inside `avg(...)` (paren-guarded); the outer `*` anchor still splits.
    anchor, cols = _parse_retired_fragment("x: avg(aov@day) @ store*month")
    assert anchor == ("store", "month")
    assert cols == [("x", "avg(aov@day)")]


def test_star_inside_a_column_expression_is_not_an_anchor_separator():
    # a `*` in the COLUMN list is multiplication, not the anchor product — only the anchor part splits on `*`.
    anchor, cols = _parse_retired_fragment("gross: revenue * 1.2 @ region")
    assert anchor == ("region",)
    assert cols == [("gross", "revenue * 1.2")]

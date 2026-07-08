"""Unit tests for the envelope grammar parser and the bearer-token check (no server needed)."""
import pytest

from columna_server.cli import _bearer, verify_token
from columna_server.frameql import FrameQLSyntaxError, parse_frameql


# --- envelope grammar -----------------------------------------------------------------------
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


@pytest.mark.parametrize("bad", [
    "", "   ", "revenue", "revenue @", "@ region", "a @ b @ c",
    "SELECT * FROM t", "revenue ; drop table t @ region",
])
def test_envelope_violations_raise(bad):
    with pytest.raises(FrameQLSyntaxError):
        parse_frameql(bad)


# --- bearer-token check ---------------------------------------------------------------------
def test_verify_token_no_expected_allows():
    assert verify_token(None, None) is True
    assert verify_token("anything", "") is True


def test_verify_token_requires_exact_match():
    assert verify_token("secret", "secret") is True
    assert verify_token("wrong", "secret") is False
    assert verify_token(None, "secret") is False


def test_bearer_extraction():
    assert _bearer("Bearer abc123") == "abc123"
    assert _bearer("bearer abc123") == "abc123"
    assert _bearer("Basic abc") is None
    assert _bearer(None) is None

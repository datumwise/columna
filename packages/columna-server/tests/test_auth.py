"""Unit tests for the bearer-token check (no server needed).

The query-surface parser tests moved to columna-core (ADR-035 D3), and what moved has since been
split: Frame-QL 1.0's envelope grammar is tested there as the language, and the terse `@`-fragment
that `columna_server.frameql` once re-exported is quarantined as lineage (retired 2026-09-11). This
file keeps the server-owned concern — bearer-token auth.
"""
from columna_server.cli import _bearer, verify_token


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

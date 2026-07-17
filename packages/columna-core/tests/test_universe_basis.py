"""
test_universe_basis.py — UNIVERSE BASIS parsing (WP on-ramp/Explorer tier-2, CP-1, B3).

Additive syntax: `UNIVERSE <name> = <dims> [WHERE <pred>] [BASIS <type>]`, type ∈
{events, spine, product, registry}. The basis type is the parse-level record only here (CP-1);
its absence-semantics engine wiring lands in a later CP-1 increment, gated on the table-check
confirm. Undeclared basis stays None — today's behavior, back-compatible; the shipped demo is
untouched until a demo recapture is ruled (Q5 rider ii).
"""
import pytest

from columna_core.parser import parse_manifold, ParseError, BASIS_TYPES


_HEAD = "MANIFOLD t VERSION 1\n"
_TAIL = ("LEVEL store = store_id BASE\nLEVEL day = day BASE\n"
         "MEASURE revenue ON u FROM u AS sum(amount)\n")


def _one(universe_line: str):
    return parse_manifold(_HEAD + universe_line + "\n" + _TAIL)


@pytest.mark.parametrize("btype", sorted(BASIS_TYPES))
def test_each_basis_type_parses(btype):
    m = _one(f"UNIVERSE u = store * day BASIS {btype}")
    assert m.universes["u"].basis == btype


def test_basis_is_optional_default_none():
    m = _one("UNIVERSE u = store * day")
    assert m.universes["u"].basis is None


def test_basis_coexists_with_where_predicate():
    m = _one("UNIVERSE u = store * day WHERE day >= stores.opened_date BASIS spine")
    u = m.universes["u"]
    assert u.basis == "spine"
    assert u.predicate is not None                 # the WHERE parse is undisturbed by the BASIS strip


def test_unknown_basis_fails_closed():
    with pytest.raises(ParseError) as ei:
        _one("UNIVERSE u = store * day BASIS eventual")
    assert "eventual" in str(ei.value)


def test_shipped_demo_declares_basis(parsed_manifold):
    # CP-3 S-5 (Huayin ruling, 2026-07-17): the demo now declares BASIS — transactions=events (absence is
    # a lawful zero), store_days=spine (absence is a gap). Absence semantics go live in the flagship.
    b = {u.name: u.basis for u in parsed_manifold.universes.values()}
    assert b == {"transactions": "events", "store_days": "spine"}

import copy
import json
from pathlib import Path

import pytest

from columna_core.governed.publication import parse_publication
from columna_core.governed.resolve import resolve_all

from columna_platform import serving

REVENUE = "fam_qv8Ky3mR7bTpZa1LwXcNdg"
PUBLICATION = (Path(__file__).resolve().parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
MAPPING = Path(__file__).resolve().parents[1] / "fixtures" / "proof_a" / "private-core-mapping-v2.json"


@pytest.fixture
def governed():
    """publication + total law views + the bound, hand-written realization claim."""
    pub, views = serving.open_publication(PUBLICATION)
    mapping = serving.bind(pub, MAPPING)
    family = [f for f in pub.families if f.family_id == REVENUE][0]
    return pub, views, mapping, family


@pytest.fixture
def revenue(governed):
    pub, views, mapping, family = governed
    return family, views[REVENUE], serving.realize(mapping, REVENUE)


def no_result(wire: dict) -> dict:
    """The single column's classified no-result, from a real wire payload."""
    return wire["columns"][0]["no_result"]


def reason(wire: dict) -> str:
    return no_result(wire)["reason"]


def alternatives(wire: dict) -> list:
    return [a["token"] for a in no_result(wire)["alternatives"]]


def _publication_with(**family_body):
    """The lighthouse artifact with extra slots on `revenue`. Built in-memory, never written.

    A FIXTURE VARIANT RATHER THAN A SECOND FIXTURE FILE: the fact under test is one slot's presence,
    and a whole committed artifact differing in one key is a thing that drifts from its sibling."""
    doc = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    doc = copy.deepcopy(doc)
    for dec in doc["logical"]["declarations"]:
        if dec.get("body", {}).get("family_id") == REVENUE:
            dec["body"].update(family_body)
    pub = parse_publication(doc)
    return pub, resolve_all(pub)[REVENUE]


@pytest.fixture
def domain_only_view():
    """C3 ESTABLISHED by a DOMAIN alone — movement absent. The hole the corrected guard closes."""
    _pub, view = _publication_with(domain="the trading calendar")
    return view


@pytest.fixture
def declared_no_movement_view():
    """C3 EXPLICIT-NONE: the family has declared that nothing moves."""
    _pub, view = _publication_with(movement={"none": "this family does not move"})
    return view

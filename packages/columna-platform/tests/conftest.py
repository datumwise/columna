from pathlib import Path
import pytest

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

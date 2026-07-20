"""
test_case_resource.py — the case as an on-demand MCP resource (recapture; proposal accepted 2026-07-18).

The three chapters ride VERBATIM (byte-preserved, wire-verbatim discipline); the 3-descriptor manifest
routes the trigger (ch1 = purpose+requirement, ch2 = design's reasons, ch3 = behaviors+moods).
"""
import os

import pytest

import columna_server
from columna_server import tools as T

_SPECS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(columna_server.__file__)))))), "specs")


def test_manifest_carries_the_three_descriptors():
    m = T.case_manifest()["chapters"]
    assert m["ch1"] == "the purpose and the requirement"
    assert m["ch2"] == "the design's reasons"
    assert m["ch3"] == "the behaviors and the moods"


@pytest.mark.parametrize("chapter,charter", [
    ("ch1", "case_demo_ch1_setup_v0_3.md"),
    ("ch2", "case_demo_ch2_solutioning_v0_6.md"),
    ("ch3", "case_demo_ch3_live_v0_7.md"),
])
def test_chapter_is_served_verbatim_byte_for_byte(chapter, charter):
    served = T.case_chapter(chapter)["text"]
    with open(os.path.join(_SPECS, charter), encoding="utf-8") as f:
        ratified = f.read()
    assert served == ratified, f"{chapter} MCP resource drifted from the ratified charter"


def test_unknown_chapter_is_a_structural_error():
    with pytest.raises(T.ToolInputError):
        T.case_chapter("ch9")

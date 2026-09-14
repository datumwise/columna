"""THE SECOND MATERIAL SLICE — a CONSTRUCTED family, formed from governed law.

WHAT THIS PROVES, AND IT IS NARROWER THAN A GREEN RUN LOOKS:

    the successor can execute a constructed family from GOVERNED FORMATION LAW, rather than by
    special-casing primitives or by reading an operator name out of a mapping.

WHAT IT DOES NOT PROVE, recorded here so a passing file cannot be mistaken for the stronger claim.
At COINCIDENT grain there is exactly one contribution per analytical point, so MIN over each fiber
returns the contribution it selected from: **the fold is mechanically degenerate and every value
served here equals the operand's value at the same point.** Non-trivial aggregation over several
contributions is the FINER branch, and the finer branch refuses — correctly — because no lighthouse
family carries a contribution-resolution law. `test_the_degeneracy_is_real_and_is_recorded` asserts
the degeneracy rather than hiding it, and `Formed.fiber_sizes` carries the evidence.

COUNT IS NOT IMPLEMENTED AND IS NOT INFERRED (OF-44). It refuses here, and the control asserts it
refuses for the LAW's reason — COUNT declares no composition over operand values — and not for any
reading of its §11.5.1 target. That distinction is the whole reason the control exists.
"""
import json
import sys
from decimal import Decimal
from pathlib import Path

import pytest

from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_core.governed.foundation import LAWS

from columna_platform import formation, serving
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.source import MaterialBinding, SourceBindings

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
sys.path.insert(0, str(FIXTURES))
import lighthouse_material as M                                              # noqa: E402

PUBLICATION = (Path(__file__).resolve().parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
MAPPING = FIXTURES / "proof_a" / "private-core-mapping-v2.json"

REVENUE = "fam_qv8Ky3mR7bTpZa1LwXcNdg"
MIN_FAMILY = "fam_Zx4TgM6oBvNqUeS3rKhDyw"
COUNT_FAMILY = "fam_Hs2VnE9QjLkYbW0uPcAtRf"

MIN_ASK = "SELECT min(revenue@sale_at) AT {store*day}"
SUM_ASK = "SELECT revenue AT {store*day}"
NO_MATERIAL = SourceBindings({})


def _mapping_file(tmp_path, mutate=None) -> str:
    doc = json.loads(MAPPING.read_text(encoding="utf-8"))
    if mutate:
        mutate(doc)
    out = tmp_path / "private-core-mapping-v2.json"
    out.write_text(json.dumps(doc), encoding="utf-8")
    return str(out)


def _provider(tmp_path, *, sources=None, mutate=None):
    return PlatformExecutionProvider.from_artifact(
        str(PUBLICATION), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=_mapping_file(tmp_path, mutate),
                                 sources=M.bindings() if sources is None else sources))


def _run(provider, ask=MIN_ASK) -> dict:
    return wire_frame(provider.run(parse_statement(ask)), universe=None, executed=True)


def _no_result(wire) -> dict:
    return wire["columns"][0]["no_result"]


def _fam(doc_family_id, doc):
    for r in doc["realizations"]:
        if r.get("family_id") == doc_family_id:
            return r
    raise AssertionError(doc_family_id)


# ══ 1 · public Frame-QL resolves the constructed family by its GOVERNED reference ═══════════════

def test_public_frameql_resolves_the_constructed_family_by_governed_reference(tmp_path):
    """`min(revenue@sale_at)` is a NAME the publication declares, not an expression to evaluate.

    The token goes to `pub.resolve_reference` exactly as `revenue` does. Nothing parses the `min(`,
    and that is the property under test: a profile that decomposed the spelling would be taking
    meaning from syntax, which is what `request.py` exists to refuse."""
    wire = _run(_provider(tmp_path))
    assert wire["outcome"] == "serve"
    assert wire["columns"][0]["name"] == "min(revenue@sale_at)"


def test_the_family_is_found_by_the_publications_own_resolver_not_by_parsing_the_name(tmp_path):
    pub, _views = serving.open_publication(str(PUBLICATION))
    fam = pub.resolve_reference("min(revenue@sale_at)")
    assert fam is not None and fam.family_id == MIN_FAMILY
    assert pub.resolve_reference("min(revenue @ sale_at)") is None      # no normalization, no guess


# ══ 8 · served through the existing wire ════════════════════════════════════════════════════════

def test_the_constructed_result_is_served_through_the_existing_wire(tmp_path):
    wire = _run(_provider(tmp_path))
    assert wire["contract_version"] == "5"
    assert wire["executed"] is True
    assert wire["frame"]["anchor"] == ["sale_at"]
    assert wire["columns"][0]["status"] == "served"
    rows = wire["columns"][0]["values"]
    assert [sorted(r) for r in rows] == [["day", "store", "value"]] * 4


# ══ 5 · the result domain is ENTAILED, not declared ═════════════════════════════════════════════

def test_the_result_domain_is_entailed_as_the_operand_domain(tmp_path):
    """MIN's `result_domain` is `same_as_operand`, so decimal is a CONSEQUENCE of the operand's
    declared domain — and the family declares no `value_domain` of its own at all."""
    pub, views = serving.open_publication(str(PUBLICATION))
    c6 = views[MIN_FAMILY]["semantic_values"]
    assert c6.value == "decimal"
    assert c6.provenance == "entailed"
    assert [f for f in pub.families if f.family_id == MIN_FAMILY][0].value_domain is None


def test_the_served_values_are_exact_decimals(tmp_path):
    values = [r["value"] for r in _run(_provider(tmp_path))["columns"][0]["values"]]
    assert all(isinstance(v, Decimal) for v in values), [type(v).__name__ for v in values]
    assert sum(values) == Decimal("34.9382")


# ══ 4 · the formation law is read from the governing foundation ════════════════════════════════

def test_the_formation_semantics_come_from_the_law_and_not_from_the_operator_name():
    """The fold is chosen by the law's DECLARED `composition`, never by the string in the mapping.

    Asserted structurally rather than by outcome: the profile's composition registry is keyed by the
    governed composition name, and its law map is a separate, explicitly declared profile fact. If
    the expected operator were derived by lowercasing the law name, the operator check below would
    be a tautology over a string."""
    assert LAWS["MIN"].composition == "minimum"
    assert "minimum" in formation._COMPOSITIONS
    assert formation.PLATFORM_LAWS == {"MIN": "min"}
    assert "MIN" not in formation._COMPOSITIONS          # keyed by composition, not by law name
    assert "min" not in formation._COMPOSITIONS


def test_a_law_this_profile_does_not_form_is_a_capability_limit(tmp_path):
    """MAX is in the foundation and not in this profile. Not a governed defect — unimplemented."""
    pub, views = serving.open_publication(str(PUBLICATION))
    with pytest.raises(Exception) as e:
        formation.realized_operator("MAX", "max(revenue@sale_at)")
    assert "this profile realizes formation laws" in str(e.value)


# ══ 6 and 7 · the operator claim is checked against the law, BEFORE arithmetic ══════════════════

def test_a_wrong_formation_operator_refuses(tmp_path):
    """The mapping CLAIMS; the law DECIDES. Claiming `max` for a family whose cited law is MIN is
    not a different backend — it is a different family."""
    def mutate(doc):
        _fam(MIN_FAMILY, doc)["formation_operator"] = "max"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert wire["outcome"] == "refuse"
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "The law decides; the mapping claims" in _no_result(wire)["detail"]


def test_a_missing_formation_operator_refuses(tmp_path):
    def mutate(doc):
        _fam(MIN_FAMILY, doc).pop("formation_operator")
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "makes no delivery claim" in _no_result(wire)["detail"]


def test_the_operator_claim_is_checked_BEFORE_any_arithmetic(tmp_path, monkeypatch):
    """ORDERING, PROVEN RATHER THAN ASSERTED. The fold is replaced with one that raises. If the
    operator check ran after arithmetic — or if a wrong claim were folded and then discarded — this
    test would see the detonation instead of the refusal."""
    def _boom(_values):                                     # pragma: no cover - must not be reached
        raise AssertionError("arithmetic ran before the operator claim was checked")

    monkeypatch.setitem(formation._COMPOSITIONS, "minimum", _boom)

    def mutate(doc):
        _fam(MIN_FAMILY, doc)["formation_operator"] = "max"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "The law decides" in _no_result(wire)["detail"]


# ══ 2 and 3 · the claim binds the construction; the material is the OPERAND's ═══════════════════

def test_the_material_comes_from_the_operands_realization(tmp_path):
    """A constructed family is formed FROM its operand's contributions, so the operand's claim is
    what names the material. Moving the OPERAND's column alone must stop the constructed ask."""
    def mutate(doc):
        _fam(REVENUE, doc)["endpoint"]["column"] = "net_amount"
        _fam(MIN_FAMILY, doc)["endpoint"]["column"] = "net_amount"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert wire["outcome"] == "refuse"
    assert "has no column 'net_amount'" in _no_result(wire)["detail"]


def test_a_constructed_family_realizing_a_different_endpoint_from_its_operand_refuses(tmp_path):
    """Two sources would be two families. K0v2 refuses the same arrangement for the same reason."""
    def mutate(doc):
        _fam(MIN_FAMILY, doc)["endpoint"]["table"] = "fact_sale_v2"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "a second source would be a second family" in _no_result(wire)["detail"]


def test_a_constructed_family_disagreeing_with_its_operand_about_grain_refuses(tmp_path):
    def mutate(doc):
        _fam(MIN_FAMILY, doc)["grain"] = "finer"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "one of the two is wrong and this profile will not choose" in _no_result(wire)["detail"]


def test_the_operand_is_read_from_the_governed_lineage_not_from_the_name(tmp_path):
    """`formation.operands` is the lineage (§3.7). The canonical reference merely happens to spell
    the same thing, and spelling is not where this profile takes meaning from."""
    pub, _views = serving.open_publication(str(PUBLICATION))
    family = [f for f in pub.families if f.family_id == MIN_FAMILY][0]
    assert serving.operand_family(pub, family).family_id == REVENUE


def test_an_unrealized_operand_refuses_before_material(tmp_path):
    def mutate(doc):
        doc["realizations"] = [r for r in doc["realizations"] if r.get("family_id") != REVENUE]
    wire = _run(_provider(tmp_path, sources=NO_MATERIAL, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "no realization claim" in _no_result(wire)["detail"]


def test_an_approximate_operand_claim_refuses_before_material(tmp_path):
    """The operand's exactness is checked too — a constructed value formed from approximate material
    is approximate, and nothing downstream would say so."""
    def mutate(doc):
        _fam(REVENUE, doc)["exactness"] = "approximate"
    wire = _run(_provider(tmp_path, sources=NO_MATERIAL, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "approximate" in _no_result(wire)["detail"]


# ══ COUNT · refused for the LAW's reason, not for a reading of its target (OF-44) ═══════════════

def test_count_refuses_because_its_law_declares_no_composition(tmp_path):
    """THE CONTROL OF/44 EXISTS FOR. COUNT has a realization claim in the fixture, so this refusal
    is not "no claim" — it is reached at the composition check, from a governed fact about the law,
    and it says nothing whatever about §11.5.1. An implementation that had guessed a target would
    have served a number here."""
    wire = _run(_provider(tmp_path), ask="SELECT count(revenue@sale_at) AT {store*day}")
    assert wire["outcome"] == "error"
    assert _no_result(wire)["reason"] == "unsupported"
    detail = _no_result(wire)["detail"]
    assert "declares no composition over operand values" in detail
    assert "count(I)" not in detail and "11.5.1" not in detail
    assert LAWS["COUNT"].composition is None                # the governed fact it rests on


def test_the_count_refusal_is_the_laws_reason_and_not_this_builds(tmp_path):
    """ORDERING AGAIN, and it matters for what an operator does next. "This law declares no
    composition" is true of every composing profile; "not in this build's law map" is contingent and
    would reasonably be read as "wait for a release". The durable reason is reported."""
    detail = _no_result(_run(_provider(tmp_path),
                             ask="SELECT count(revenue@sale_at) AT {store*day}"))["detail"]
    assert "this profile realizes formation laws" not in detail


# ══ the degeneracy, recorded rather than hidden ════════════════════════════════════════════════

def test_the_degeneracy_is_real_and_is_recorded(tmp_path):
    """MIN's served values EQUAL revenue's at the same points, because each fiber holds one
    contribution. Asserted as a fact of this slice, so nobody reads the green as aggregation."""
    p = _provider(tmp_path)
    mins = {(r["store"], str(r["day"])): r["value"] for r in _run(p, MIN_ASK)["columns"][0]["values"]}
    sums = {(r["store"], str(r["day"])): r["value"] for r in _run(p, SUM_ASK)["columns"][0]["values"]}
    assert mins == sums
    assert mins == {("east", "2026-01-01"): Decimal("10.0000"),
                    ("east", "2026-01-02"): Decimal("20.0000"),
                    ("west", "2026-01-01"): Decimal("1.2345"),
                    ("west", "2026-01-02"): Decimal("3.7037")}


def test_every_fiber_carries_exactly_one_contribution(tmp_path):
    """The evidence behind the sentence above, from the fold itself rather than from the values."""
    pub, views = serving.open_publication(str(PUBLICATION))
    mapping = serving.bind(pub, _mapping_file(tmp_path))
    family = [f for f in pub.families if f.family_id == MIN_FAMILY][0]
    operand = serving.operand_family(pub, family)
    from columna_platform.source import read_anchored
    anchored = read_anchored(M.bindings(), serving.realize(mapping, operand.family_id),
                             serving.component_realizations(mapping, operand.constitutive_anchor))
    law = LAWS["MIN"]
    formed = formation.form(anchored, law, formation.composition_for(law, "min"))
    assert formed.fiber_sizes == (1, 1, 1, 1)
    assert formed.law_name == "MIN" and formed.composition == "minimum"


def test_the_fold_is_a_real_group_and_fold_not_a_singleton_shortcut(tmp_path):
    """Hand the fold two contributions at one point DIRECTLY, bypassing admission, and check it
    actually folds. Admission refuses this material at the boundary (see the control below); this
    test is about whether the fold would be correct if it ever saw a fiber of two."""
    import pyarrow as pa
    from columna_platform.carrier import AnchoredCarrier
    table = pa.table({
        "store": pa.array(["east", "east"], type=pa.string()),
        "day": pa.array([M.ROWS[0][1], M.ROWS[0][1]], type=pa.date32()),
        "value": pa.array([Decimal("9.0000"), Decimal("4.0000")], type=pa.decimal128(18, 4)),
    })
    anchored = AnchoredCarrier(table=table, value_column="value",
                               anchor_columns=("day", "store"), measured_as="hand-built")
    law = LAWS["MIN"]
    formed = formation.form(anchored, law, formation.composition_for(law, "min"))
    assert formed.fiber_sizes == (2,)
    assert formed.table.column("value").to_pylist() == [Decimal("4.0000")]


# ══ CHECK 5 · the coincident claim, against the material ═══════════════════════════════════════

def test_material_with_two_contributions_at_one_point_refuses_a_coincident_claim(tmp_path):
    """`coincident` is a CLAIM about rows, and it is checkable the moment rows exist. Two rows at
    one analytical point make it false — and this refuses on the SUM path too, where the same
    material would otherwise be served as two answers to one governed question."""
    import pyarrow as pa
    dup_day = pa.array([M.ROWS[0][1]] * 4, type=pa.date32())          # every row on the same day
    sources = M.bindings(**{M.DAY_COLUMN: dup_day})
    for ask in (MIN_ASK, SUM_ASK):
        wire = _run(_provider(tmp_path, sources=sources), ask=ask)
        assert wire["outcome"] == "refuse", ask
        assert _no_result(wire)["reason"] == "want_of_state", ask
        assert "COINCIDENT grain" in _no_result(wire)["detail"], ask


# ══ 10 · the finer refusal remains pinned ══════════════════════════════════════════════════════

def test_the_finer_grain_refusal_is_unchanged(tmp_path):
    """Still the correct result, and still reached: no lighthouse family carries a
    contribution-resolution law, so a finer claim has nothing to be finer THAN."""
    def mutate(doc):
        _fam(REVENUE, doc)["grain"] = "finer"
        _fam(MIN_FAMILY, doc)["grain"] = "finer"
    wire = _run(_provider(tmp_path, mutate=mutate), ask=SUM_ASK)
    assert wire["outcome"] == "refuse"
    assert "grain 'finer'" in _no_result(wire)["detail"]


# ══ 9 · isolation, and determinism ═════════════════════════════════════════════════════════════

def test_formation_consults_no_cml_and_loads_no_legacy_module(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert not list(Path(tmp_path).glob("**/*.cml"))
    assert _run(_provider(tmp_path))["outcome"] == "serve"
    import sys as _s
    banned = {"planner", "engine", "model", "adjudication", "parser", "projection", "frameql",
              "expr", "connector"}
    loaded = {m.rsplit(".", 1)[-1] for m in _s.modules if m.startswith("columna_core.")}
    assert not (loaded & banned), sorted(loaded & banned)


def test_the_formation_module_names_no_forbidden_import():
    import ast
    forbidden = {"columna_core.planner", "columna_core.engine", "columna_core.model",
                 "columna_core.adjudication", "columna_core.connector", "columna_core.parser",
                 "columna_core.compiler.compile_v2", "duckdb", "adbc_driver_manager"}
    reached = set()
    for n in ast.walk(ast.parse(Path(formation.__file__).read_text(encoding="utf-8"))):
        if isinstance(n, ast.Import):
            reached.update(a.name for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            reached.add(n.module)
    assert not (reached & forbidden), sorted(reached & forbidden)


def test_the_formed_result_is_deterministic(tmp_path):
    """The fold groups by coordinate and emits sorted keys, so two identical asks are byte-identical
    — the property `gen_transcript`'s flap detector had to be built to notice elsewhere."""
    p = _provider(tmp_path)
    assert _run(p) == _run(p)

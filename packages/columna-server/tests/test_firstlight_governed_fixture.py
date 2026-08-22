"""
test_firstlight_governed_fixture — milestone 7. The first public governed fixture.

What this proves: the public Columna release can CONSUME a legitimate governed publication through
the complete generic path — compile, bind, provision, admit, serve.

What it does not prove, and these tests are careful never to imply: that the public release can
AUTHOR or RATIFY governed publications. The machinery that produced `governed-publication.json`
(manifold-agent, pinned at df794a6, driven through columna-studio) is not part of this release and is
not reachable from it. The artifact is consumed here as committed bytes, exactly as a user would.

The producer cannot run in CI — manifold-agent is private — so test 1 asserts the PROPERTIES only a
legitimately produced artifact has, rather than re-minting one. A hand-written artifact would look
identical, which is why the ratification and the physical-cleanliness are checked rather than assumed.
"""
import glob
import json
import os
import shutil

import pytest

import columna_server
from columna_core.compiler import (
    build_receipt,
    compile_k0,
    parse_mapping,
    parse_publication,
    render_receipt,
)
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement
from columna_server.lowering_receipt import LOWERING_RECEIPT
from columna_server.provision import DigestMismatch, MissingInput, ProvisionRefusal, provision_runtime_unit
from columna_server.store import ENTRY_GOVERNED, ENTRY_LEGACY, ManifoldStore

_SRV = os.path.dirname(os.path.abspath(columna_server.__file__))
GOVERNED_DIR = os.path.join(_SRV, "governed")
UNIT = os.path.join(GOVERNED_DIR, "firstlight")
_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BUILD_INPUTS = os.path.join(_REPO, "packages", "columna-server", "fixtures", "firstlight")

SHIPPED = ("governed-publication.json", "manifold.cml", LOWERING_RECEIPT, "data.toml",
           "PROVENANCE.md")

EXPECTED = {
    "sum":   {"s1": 20.0, "s2": 65.0},
    "count": {"s1": 3,    "s2": 3},
    "min":   {"s1": 3.0,  "s2": 5.0},
    "max":   {"s1": 10.0, "s2": 40.0},
}
LEAF = {("s1", "2026-08-01"): 10.0, ("s1", "2026-08-02"): 3.0, ("s1", "2026-08-03"): 7.0,
        ("s2", "2026-08-01"): 5.0,  ("s2", "2026-08-02"): 40.0, ("s2", "2026-08-03"): 20.0}


def _bytes(name, folder=UNIT):
    with open(os.path.join(folder, name), "rb") as f:
        return f.read()


def _store():
    return ManifoldStore(GOVERNED_DIR)


def _ask(statement):
    lm = _store().get("firstlight")
    return wire_frame(lm.provider.runtime.planner.run_statement(
        parse_statement(statement)))["columns"][0]


# ── packaging ────────────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("name", SHIPPED)
def test_the_unit_ships_beside_the_package(name):
    """Under `src/columna_server`, so hatchling ships it in the wheel with no packaging change."""
    assert os.path.isfile(os.path.join(UNIT, name)), f"{name} missing from the packaged unit"


def test_the_synthetic_warehouse_ships():
    parquet = glob.glob(os.path.join(UNIT, "warehouse", "*.parquet"))
    assert parquet, "the fixture ships no data"
    assert sum(os.path.getsize(p) for p in parquet) < 64 * 1024


def test_the_whole_unit_is_tiny():
    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _d, fs in os.walk(UNIT) for f in fs)
    assert total <= 256 * 1024, f"the governed fixture is {total/1024:.0f} KB"


def test_the_build_inputs_are_repo_only_and_not_in_the_unit():
    """The mapping is a reproduction input, never a runtime authority input."""
    assert os.path.isfile(os.path.join(BUILD_INPUTS, "private-core-mapping.json"))
    assert os.path.isfile(os.path.join(BUILD_INPUTS, "manifold.yaml"))
    assert not os.path.exists(os.path.join(UNIT, "private-core-mapping.json"))
    assert not os.path.exists(os.path.join(UNIT, "manifold.yaml"))


# ── 1. the publication is a legitimately produced one ────────────────────────────────────────────
def test_every_universe_carries_a_real_ratification():
    """The mint path leaves evidence: an `elf-1` fingerprint and a named human steward. This is what
    distinguishes a published artifact from a hand-written one that would otherwise look identical."""
    art = json.loads(_bytes("governed-publication.json"))
    universes = [d["name"] for d in art["logical"]["declarations"] if d["kind"] == "universe"]
    rats = art["authority"]["ratifications"]
    assert universes and set(rats) == set(universes)
    for name, r in rats.items():
        assert r["fingerprint_version"] == "elf-1"
        assert len(r["fingerprint"]) == 64 and int(r["fingerprint"], 16) >= 0
        assert r["ratified_by"].strip(), f"universe {name} names no steward"
    assert art["authority"]["published_by"].strip()
    assert art["authority"]["published_at"].strip()


def test_the_publication_is_physical_clean():
    """The blast wall, checked on the shipped artifact: no table, column, schema or connection name
    from the mapping appears anywhere in the governed publication."""
    art_text = _bytes("governed-publication.json").decode()
    mapping = json.loads(open(os.path.join(BUILD_INPUTS, "private-core-mapping.json")).read())
    physical = {str(v) for r in mapping["realizations"] for v in r["endpoint"].values() if v}
    assert physical
    for token in physical:
        assert token not in art_text, f"physical identifier {token!r} leaked into the publication"


def test_the_publication_is_exactly_k0_shaped():
    art = json.loads(_bytes("governed-publication.json"))
    kinds = {d["kind"] for d in art["logical"]["declarations"]}
    assert kinds == {"anchor", "universe", "measure", "member"}
    unis = [d for d in art["logical"]["declarations"] if d["kind"] == "universe"]
    assert all("restriction" not in d["body"] for d in unis), "K0 emits unrestricted universes only"


# ── 2 & 3. the shipped image is what the shipped compiler produces, deterministically ────────────
def _recompile():
    pub_bytes = _bytes("governed-publication.json")
    mapping = json.loads(open(os.path.join(BUILD_INPUTS, "private-core-mapping.json")).read())
    return pub_bytes, compile_k0(parse_publication(json.loads(pub_bytes)), parse_mapping(mapping))


def test_recompiling_reproduces_the_shipped_image_byte_for_byte():
    """The strongest guard available: committed publication + committed mapping -> shipped compiler
    -> the exact bytes that ship. If the compiler ever drifts, this fails before a release can."""
    _, image = _recompile()
    assert image.encode() == _bytes("manifold.cml")


def test_the_recompile_is_deterministic():
    _, a = _recompile()
    _, b = _recompile()
    assert a.encode() == b.encode()


def test_the_shipped_receipt_binds_the_shipped_files():
    receipt = json.loads(_bytes(LOWERING_RECEIPT))
    from columna_core.compiler.receipt import digest_bytes
    assert receipt["publication_digest"] == digest_bytes(_bytes("governed-publication.json"))
    assert receipt["image_digest"] == digest_bytes(_bytes("manifold.cml"))
    assert receipt["publication_ref"] == {"manifold_id": "firstlight", "version": "1.0.0"}


def test_the_image_claims_exactly_the_publication_it_was_compiled_from():
    art = json.loads(_bytes("governed-publication.json"))
    line = f"SOURCE_MANIFOLD {art['ref']['manifold_id']} VERSION {art['ref']['version']}"
    assert line in _bytes("manifold.cml").decode()


# ── 4. provisioning preserves every bound byte ───────────────────────────────────────────────────
def test_reprovisioning_preserves_publication_image_and_receipt_bytes(tmp_path):
    pub_bytes, image = _recompile()
    src = tmp_path / "build"; src.mkdir()
    (src / "governed-publication.json").write_bytes(pub_bytes)
    (src / "manifold.cml").write_bytes(image.encode())
    receipt = build_receipt(manifold_id=image.manifold_id, version=image.version,
                            publication_bytes=pub_bytes, image_bytes=image.encode(),
                            compiler_name="columna-core-p1-k0", compiler_version="test",
                            established_at="2026-08-22T00:00:00Z")
    (src / LOWERING_RECEIPT).write_text(render_receipt(receipt), encoding="utf-8")

    dest = tmp_path / "unit"
    provision_runtime_unit(str(dest), publication=str(src / "governed-publication.json"),
                           image=str(src / "manifold.cml"), receipt=str(src / LOWERING_RECEIPT),
                           data_toml=_bytes("data.toml").decode())
    for n in ("governed-publication.json", "manifold.cml", LOWERING_RECEIPT):
        assert _bytes(n, str(dest)) == open(str(src / n), "rb").read()
    assert _bytes("governed-publication.json", str(dest)) == _bytes("governed-publication.json")
    assert _bytes("manifold.cml", str(dest)) == _bytes("manifold.cml")


# ── 5. admission ─────────────────────────────────────────────────────────────────────────────────
def test_the_fixture_is_admitted_as_governed_with_zero_conditions():
    store = _store()
    assert [c.kind for c in store.conditions()] == []
    assert store.get("firstlight").entry_kind == ENTRY_GOVERNED


def test_the_governed_meaning_comes_from_the_artifact():
    lm = _store().get("firstlight")
    assert (lm.publication.ref.manifold_id, lm.publication.ref.version) == ("firstlight", "1.0.0")


# ── 6. all four reducers, at both grains ─────────────────────────────────────────────────────────
@pytest.mark.parametrize("member", sorted(EXPECTED))
def test_every_reducer_serves_at_the_rolled_up_grain(member):
    """`{store}` is a SUBSET of the product anchor, so the dropped component is aggregated across —
    this exercises the monoid combine, not merely delivery."""
    col = _ask(f"SELECT revenue.{member} AT {{store}}")
    assert col["status"] == "served", col.get("no_result")
    assert {r["store"]: r["value"] for r in col["values"]} == EXPECTED[member]


@pytest.mark.parametrize("member", sorted(EXPECTED))
def test_every_reducer_serves_at_the_leaf_grain(member):
    col = _ask(f"SELECT revenue.{member} AT {{store, day}}")
    assert col["status"] == "served", col.get("no_result")
    got = {(r["store"], r["day"]): r["value"] for r in col["values"]}
    expected = ({k: 1 for k in LEAF} if member == "count"
                else {k: float(v) for k, v in LEAF.items()})
    assert got == expected


# ── 7. a lowering receipt is not certification ───────────────────────────────────────────────────
def test_a_lowering_receipt_is_not_certification():
    """A valid receipt DOES participate in governed-entry admission — that is what makes this unit
    governed. What it does not do is certify anything: no capability is licensed by its presence,
    and the certification sets stay empty while the kernel serves."""
    lm = _store().get("firstlight")
    scope = lm.provider.runtime.published_scope
    assert not scope.certified_edges
    assert not scope.certified_faces
    assert _ask("SELECT revenue.sum AT {store}")["status"] == "served"


# ── 8. the binding is load-bearing ───────────────────────────────────────────────────────────────
@pytest.mark.parametrize("break_it", ["image", "publication", "receipt"])
def test_tampering_with_a_bound_input_refuses_and_leaves_no_unit(tmp_path, break_it):
    src = tmp_path / "build"; src.mkdir()
    for n in ("governed-publication.json", "manifold.cml", LOWERING_RECEIPT):
        (src / n).write_bytes(_bytes(n))
    if break_it == "image":
        (src / "manifold.cml").write_bytes(_bytes("manifold.cml") + b"\n# edit\n")
    elif break_it == "publication":
        (src / "governed-publication.json").write_bytes(_bytes("governed-publication.json") + b" ")
    else:
        os.remove(src / LOWERING_RECEIPT)

    dest = tmp_path / "unit"
    with pytest.raises(ProvisionRefusal) as e:
        provision_runtime_unit(str(dest), publication=str(src / "governed-publication.json"),
                               image=str(src / "manifold.cml"),
                               receipt=str(src / LOWERING_RECEIPT),
                               data_toml=_bytes("data.toml").decode())
    assert isinstance(e.value, MissingInput if break_it == "receipt" else DigestMismatch)
    assert not dest.exists() and not (tmp_path / "unit.incoming").exists()


def test_editing_the_shipped_image_in_place_loses_governed_standing(tmp_path):
    copy = tmp_path / "governed"
    shutil.copytree(GOVERNED_DIR, copy)
    p = copy / "firstlight" / "manifold.cml"
    p.write_bytes(p.read_bytes() + b"\n# in-place edit on a running host\n")
    store = ManifoldStore(str(copy))
    assert {c.kind for c in store.conditions()} == {"LoweringReceiptMismatch"}
    assert store.get("firstlight").entry_kind != ENTRY_GOVERNED


# ── 9. nothing existing was promoted ─────────────────────────────────────────────────────────────
def test_the_legacy_demos_are_untouched_and_still_exactly_legacy():
    demo = os.path.join(_SRV, "demo")
    store = ManifoldStore(demo)
    loaded = store.all()
    assert {lm.manifold_id for lm in loaded} == {"benchmark", "cascadia"}
    assert {lm.entry_kind for lm in loaded} == {ENTRY_LEGACY}
    assert [c.kind for c in store.conditions()] == []


def test_the_governed_fixture_lives_apart_from_the_legacy_demos():
    """Separate directories, so `no fixture is promoted` stays literally true: nothing existing
    changed kind — a new thing was born governed."""
    assert os.path.isdir(GOVERNED_DIR) and os.path.isdir(os.path.join(_SRV, "demo"))
    assert not os.path.exists(os.path.join(_SRV, "demo", "firstlight"))
    assert sorted(os.listdir(GOVERNED_DIR)) == ["firstlight"]


# ── 10. the path is generic ──────────────────────────────────────────────────────────────────────
def test_no_shipped_code_knows_this_fixtures_name():
    """If the fixture needed a branch to work, that would be a defect in the generic path rather
    than a property of the fixture. Nothing in compiler, provisioner, registry or serving code may
    mention it — only the fixture's own directory and this test file."""
    import columna_core
    roots = [os.path.dirname(os.path.abspath(columna_core.__file__)), _SRV]
    offenders = []
    for root in roots:
        for dirpath, _dirs, files in os.walk(root):
            if os.path.abspath(dirpath).startswith(os.path.abspath(UNIT)):
                continue
            for f in files:
                if not f.endswith(".py"):
                    continue
                path = os.path.join(dirpath, f)
                with open(path, "rb") as fh:
                    if b"firstlight" in fh.read().lower():
                        offenders.append(path)
    assert offenders == [], f"shipped code special-cases the fixture: {offenders}"

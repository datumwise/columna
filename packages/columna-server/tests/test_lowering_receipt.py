"""
The publication→execution-image binding, and the admission gate it powers.

WHAT IS BEING PINNED. Before this, an entry acquired governed standing from an artifact plus a
matching ``SOURCE_MANIFOLD`` — an ORIGIN CLAIM the .cml makes about itself. Anyone who could write
the runtime folder could type that claim, and arbitrary co-location of any artifact with any .cml was
enough. These tests pin that it no longer is: standing now additionally requires a receipt binding
THIS publication to THIS image, by content digest over the files as shipped.

WHAT IS NOT BEING PINNED. The receipt is not certification, not attestation, and not PublishedScope
admission — ``test_a_valid_receipt_does_not_imply_published_scope`` states that as an assertion rather
than a comment, because it is the failure mode this artifact would otherwise invite.
"""
import json
import os

import pytest

import columna_server
from columna_server.lowering_receipt import (
    LOWERING_RECEIPT,
    LoweringBinding,
    LoweringReceiptInvalid,
    LoweringReceiptMismatch,
    digest_bytes,
    digest_file,
    parse_lowering_receipt,
)
from columna_server.registry import ManifoldRef, ManifoldSelector, PublicationNotFound
from columna_server.store import (
    ENTRY_GOVERNED,
    ENTRY_LEGACY,
    ENTRY_SOURCE_REFERENCED_INCOMPLETE,
    ManifoldStore,
)
from columna_server.tools import list_manifolds, manifold_status
from conftest import write_lowering_receipt

_CASCADIA = os.path.join(os.path.dirname(columna_server.__file__), "demo", "cascadia")


def _artifact(src_id, src_ver, universes=("u",)):
    return {
        "publication_format_version": "1",
        "ref": {"manifold_id": src_id, "version": src_ver},
        "logical": {"declarations": [
            {"kind": "universe", "name": u, "body": {"basis": "events", "anchor": "keys"}}
            for u in universes
        ]},
        "authority": {
            "published_by": "Huayin", "published_at": "2026-08-13T00:00:00Z",
            "ratifications": {u: {"ratified_by": "Huayin", "at": "2026-08-11T00:00:00Z",
                                  "fingerprint": f"fp-{u}", "fingerprint_version": "elf-1"}
                              for u in universes},
        },
    }


def _unit(tmp_path, folder, *, source_line="SOURCE_MANIFOLD retail VERSION 1.2.0",
          artifact=None, receipt="valid", **receipt_kw):
    """Assemble one runtime folder over cascadia's real warehouse.

    ``receipt`` is "valid" (digest the files as written — what a compiler does), ``None`` (omit it),
    or a raw string written verbatim (for the malformed cases).
    """
    src_cml = open(os.path.join(_CASCADIA, "manifold.cml")).read().splitlines()
    d = tmp_path / folder
    d.mkdir()
    body = src_cml[:1] + ([source_line] if source_line else []) + src_cml[1:]
    (d / "manifold.cml").write_text("\n".join(body) + "\n")
    (d / "data.toml").write_text(
        f'[manifold]\nname = "{folder}"\n[connector]\ntype = "duckdb"\n'
        f'warehouse = "{os.path.join(_CASCADIA, "warehouse")}"\n'
    )
    art = _artifact("retail", "1.2.0") if artifact is None else artifact
    if art is not False:
        (d / "governed-publication.json").write_text(json.dumps(art))
    if receipt == "valid":
        write_lowering_receipt(d, art["ref"]["manifold_id"], art["ref"]["version"], **receipt_kw)
    elif isinstance(receipt, str):
        (d / LOWERING_RECEIPT).write_text(receipt)
    return d


def _one(tmp_path, **kw):
    _unit(tmp_path, "unit", **kw)
    return ManifoldStore(str(tmp_path))


def _conditions(store):
    return {(c.manifold_id, c.kind) for c in store.conditions()}


# ── the digest: content, as shipped ──────────────────────────────────────────────────────────────
def test_digest_is_the_file_bytes_not_a_canonical_form(tmp_path):
    p = tmp_path / "f.json"
    p.write_text('{"a": 1}')
    assert digest_file(str(p)) == digest_bytes(b'{"a": 1}')
    # semantically identical, byte-different — and the digest says so, which is the point: the image
    # a compiler emitted is the bytes it emitted, not an equivalence class of them.
    p.write_text('{"a":1}')
    assert digest_file(str(p)) != digest_bytes(b'{"a": 1}')


# ── binding identity is deterministic (ruling §2) ────────────────────────────────────────────────
def test_binding_identity_ignores_timestamp_and_mapping_provenance():
    """Two receipts for the same inputs bind identically however and whenever they were written."""
    base = {
        "receipt_format_version": "1.0",
        "publication_ref": {"manifold_id": "retail", "version": "1.2.0"},
        "publication_digest": digest_bytes(b"pub"),
        "image_digest": digest_bytes(b"img"),
        "compiler": {"name": "columna-core", "version": "0.16.0"},
    }
    a = parse_lowering_receipt({**base, "established_at": "2026-01-01T00:00:00Z",
                                "mapping_provenance": {"mapping_id": "m1", "revision": "7"}})
    b = parse_lowering_receipt({**base, "established_at": "2099-12-31T23:59:59Z",
                                "mapping_provenance": {"mapping_id": "m2", "revision": "99"}})
    assert a.binding == b.binding                      # the binding is the ref + the two digests
    assert a != b                                      # ...and provenance is still retained
    assert a.established_at != b.established_at
    assert a.binding == LoweringBinding(ManifoldRef("retail", "1.2.0"),
                                        digest_bytes(b"pub"), digest_bytes(b"img"))


def test_the_receipt_carries_no_logical_vocabulary():
    """Meaning-free BY TYPE. There is nowhere in a parsed receipt to put a universe or a measure, so
    the artifact cannot become a second, quieter channel for publication meaning."""
    r = parse_lowering_receipt({
        "receipt_format_version": "1.0",
        "publication_ref": {"manifold_id": "retail", "version": "1.2.0"},
        "publication_digest": digest_bytes(b"pub"),
        "image_digest": digest_bytes(b"img"),
        "compiler": {"name": "c", "version": "1"},
        # a producer writing meaning into the receipt cannot get it through the parser
        "logical": {"declarations": [{"kind": "universe", "name": "smuggled", "body": {}}]},
        "universes": ["smuggled"],
    })
    blob = json.dumps({"binding": [r.binding.publication_ref.manifold_id,
                                   r.binding.publication_digest, r.binding.image_digest],
                       "compiler": r.compiler, "provenance": r.mapping_provenance})
    assert "smuggled" not in blob
    assert not hasattr(r, "logical") and not hasattr(r, "universes")


# ── structural validation ────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("mutate,fragment", [
    (lambda d: d.pop("receipt_format_version"), "missing receipt_format_version"),
    (lambda d: d.update({"receipt_format_version": "2.0"}), "unsupported major"),
    (lambda d: d.pop("publication_ref"), "missing publication_ref"),
    (lambda d: d["publication_ref"].pop("version"), "concrete manifold_id and version"),
    (lambda d: d.pop("publication_digest"), "missing publication_digest"),
    (lambda d: d.pop("image_digest"), "missing image_digest"),
    (lambda d: d.update({"image_digest": "deadbeef"}), "content digest"),
    (lambda d: d.update({"image_digest": "sha256:XYZ"}), "hex digest"),
    (lambda d: d.pop("compiler"), "missing compiler"),
    (lambda d: d["compiler"].pop("name"), "compiler.name is required"),
    (lambda d: d.update({"established_at": 17}), "established_at"),
])
def test_structural_defects_are_invalid(mutate, fragment):
    d = {
        "receipt_format_version": "1.0",
        "publication_ref": {"manifold_id": "retail", "version": "1.2.0"},
        "publication_digest": digest_bytes(b"pub"),
        "image_digest": digest_bytes(b"img"),
        "compiler": {"name": "columna-core", "version": "0.16.0"},
    }
    mutate(d)
    with pytest.raises(LoweringReceiptInvalid) as e:
        parse_lowering_receipt(d)
    assert fragment in str(e.value)


def test_a_receipt_without_provenance_of_its_producer_is_invalid():
    """A receipt is a claim by a compiler. One that cannot say which compiler made it is not a
    receipt — even though the content of that claim never gates admission."""
    with pytest.raises(LoweringReceiptInvalid):
        parse_lowering_receipt({
            "receipt_format_version": "1.0",
            "publication_ref": {"manifold_id": "r", "version": "1.0.0"},
            "publication_digest": digest_bytes(b"p"), "image_digest": digest_bytes(b"i"),
        })


# ── admission: the five ways standing is refused ─────────────────────────────────────────────────
def test_receipt_absent_cannot_be_governed(tmp_path):
    store = _one(tmp_path, receipt=None)
    lm = store.get("unit")
    assert lm.entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE
    assert lm.publication is None and lm.ref is None
    assert ("unit", "LoweringReceiptMissing") in _conditions(store)
    with pytest.raises(PublicationNotFound):
        store.resolve(ManifoldSelector("retail", "1.2.0"))


def test_a_hand_written_source_manifold_is_insufficient(tmp_path):
    """The exact pre-receipt path: take a legacy .cml, type a SOURCE_MANIFOLD line into it, drop a
    well-formed artifact beside it. That used to be governed standing. It is now a condition."""
    store = _one(tmp_path, receipt=None)
    row = list_manifolds(store)["manifolds"][0]
    assert row["kind"] == "authority_incomplete"
    assert row["conditions"] == ["lowering_receipt_missing"]
    assert "manifold_id" not in row and "latest_version" not in row


def test_receipt_invalid_cannot_be_governed(tmp_path):
    store = _one(tmp_path, receipt="{not json")
    lm = store.get("unit")
    assert lm.entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE and lm.publication is None
    assert ("unit", "LoweringReceiptInvalid") in _conditions(store)
    assert list_manifolds(store)["manifolds"][0]["conditions"] == ["lowering_receipt_invalid"]


def test_receipt_ref_mismatch_cannot_be_governed(tmp_path):
    """A receipt that binds a different publication does not bind this one."""
    _unit(tmp_path, "unit", receipt=None)
    (tmp_path / "unit" / LOWERING_RECEIPT).write_text(json.dumps({
        "receipt_format_version": "1.0",
        "publication_ref": {"manifold_id": "retail", "version": "9.9.9"},
        "publication_digest": digest_file(str(tmp_path / "unit" / "governed-publication.json")),
        "image_digest": digest_file(str(tmp_path / "unit" / "manifold.cml")),
        "compiler": {"name": "c", "version": "1"},
    }))
    store = ManifoldStore(str(tmp_path))
    assert store.get("unit").entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE
    assert ("unit", "LoweringReceiptMismatch") in _conditions(store)
    assert list_manifolds(store)["manifolds"][0]["conditions"] == ["lowering_receipt_mismatch"]


def test_publication_byte_mismatch_cannot_be_governed(tmp_path):
    """The receipt is for a different publication artifact — the provisioner paired the wrong two
    files, or the artifact was edited in place after lowering."""
    store = _one(tmp_path, publication_digest=digest_bytes(b"some other publication"))
    assert store.get("unit").entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE
    assert ("unit", "LoweringReceiptMismatch") in _conditions(store)


def test_image_byte_mismatch_cannot_be_governed(tmp_path):
    """The receipt is for a different execution image — a stale image survived a republish, or the
    .cml was edited on the running host."""
    store = _one(tmp_path, image_digest=digest_bytes(b"some other image"))
    assert store.get("unit").entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE
    assert ("unit", "LoweringReceiptMismatch") in _conditions(store)


def test_editing_the_image_after_provisioning_breaks_the_binding(tmp_path):
    """Standing is a property of the bytes, not of the folder. Admit, then edit, then reload."""
    d = _unit(tmp_path, "unit")
    assert ManifoldStore(str(tmp_path)).get("unit").entry_kind == ENTRY_GOVERNED
    (d / "manifold.cml").write_text((d / "manifold.cml").read_text() + "\n# an in-place edit\n")
    store = ManifoldStore(str(tmp_path))
    assert store.get("unit").entry_kind == ENTRY_SOURCE_REFERENCED_INCOMPLETE
    assert ("unit", "LoweringReceiptMismatch") in _conditions(store)


# ── admission: the one way standing is granted ───────────────────────────────────────────────────
def test_a_properly_produced_unit_becomes_governed(tmp_path):
    store = _one(tmp_path)
    lm = store.get("unit")
    assert lm.entry_kind == ENTRY_GOVERNED
    assert lm.ref == ManifoldRef("retail", "1.2.0")
    assert store.resolve(ManifoldSelector("retail", "1.2.0")).publication.ref == lm.ref
    row = list_manifolds(store)["manifolds"][0]
    assert row["kind"] == "governed" and row["latest_version"] == "1.2.0"
    assert "conditions" not in row


def test_a_valid_receipt_does_not_imply_published_scope(tmp_path):
    """RULING §1. The receipt establishes publication→image and stops there. It must not move
    certification, adjudication or serving admission by a single field — so the runtime standing of a
    governed unit is byte-identical to the same image served as a legacy runtime."""
    _unit(tmp_path, "governed_unit")
    _unit(tmp_path, "legacy_unit", source_line=None, artifact=False, receipt=None)
    store = ManifoldStore(str(tmp_path))
    assert store.get("governed_unit").entry_kind == ENTRY_GOVERNED
    assert store.get("legacy_unit").entry_kind == ENTRY_LEGACY

    gov = manifold_status(store, "retail", version="1.2.0")
    leg = manifold_status(store, "legacy_unit")
    assert gov["published_scope"] == leg["published_scope"]     # no scope was admitted
    assert gov["evidence"] == leg["evidence"]                   # no certification was implied
    # the ONE difference the receipt earns is publication identity, not analytical permission
    assert gov["manifold_version"] == "1.2.0" and "manifold_version" not in leg


def test_logical_meaning_is_still_read_only_from_the_publication_artifact(tmp_path):
    """The blast wall is untouched: the receipt carries no meaning, so ``publication.logical`` is
    still exactly the artifact's — and still not the .cml's, whose LEVELs/MEASUREs do not leak in."""
    art = _artifact("retail", "1.2.0")
    _unit(tmp_path, "unit", artifact=art)
    pub = ManifoldStore(str(tmp_path)).resolve(ManifoldSelector("retail", "1.2.0")).publication
    assert pub.logical == art["logical"]
    assert {d["name"] for d in pub.logical["declarations"]} == {"u"}
    assert "MEASURE" not in json.dumps(pub.logical)


def test_the_shipped_fixtures_remain_legacy():
    """No fixture is promoted by this change. The packaged demos carry no SOURCE_MANIFOLD, so they
    stay compatibility-served — and the receipt requirement gives no route to relabel them."""
    store = ManifoldStore(os.path.join(os.path.dirname(columna_server.__file__), "demo"))
    rows = list_manifolds(store)["manifolds"]
    assert {r["runtime_id"] for r in rows} == {"benchmark", "cascadia"}
    for r in rows:
        assert r["kind"] == "legacy"
        assert "manifold_id" not in r and "conditions" not in r
    assert store.get("cascadia").entry_kind == ENTRY_LEGACY

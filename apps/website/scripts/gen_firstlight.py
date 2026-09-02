#!/usr/bin/env python3
"""Integrity generator for the /case governed-standing exhibit — built by running the SHIPPED package.

Emits JSON on stdout describing `firstlight`, the governed publication that ships inside
`columna-server` >= 0.11.0: the two installation catalogs AS SHIPPED, the execution image, the
lowering receipt, the serving wires that carry (and do not carry) a publication version, and the
manifold's own counts.

WHAT THIS EXHIBIT CLAIMS, AND WHAT IT MUST NOT. The public release can CONSUME a legitimate governed
publication through the generic path — compile, bind, provision, admit, serve. It cannot AUTHOR or
RATIFY one: the machinery that produced this artifact is not part of the release and is not reachable
from it. Nothing emitted here may be arranged to suggest otherwise.

TWO CATALOGS, AS SHIPPED — never one assembled view. The wheel ships `governed/` and `demo/` as
separate directories; a combined catalog would be a composition, and this page's discipline is
recorded, never illustrated. So each directory is read exactly as it lies on disk.

Exits non-zero on any failed invariant, so the build fails closed rather than shipping a governed
claim that the shipped package no longer supports.
"""
import json
import os
import pathlib
import sys
from importlib.metadata import version

import columna_server
from columna_core.compiler import compile_k0, parse_mapping, parse_publication
from columna_core.compiler.receipt import digest_bytes
from columna_server.lowering_receipt import LOWERING_RECEIPT
from columna_server.store import ENTRY_GOVERNED, ENTRY_LEGACY, ManifoldStore
from columna_server.tools import list_manifolds, manifold_status, query

SRV = os.path.dirname(os.path.abspath(columna_server.__file__))
CORE = os.path.dirname(os.path.abspath(__import__("columna_core").__file__))
GOVERNED_DIR = os.path.join(SRV, "governed")          # shipped: firstlight only
DEMO_DIR = os.path.join(SRV, "demo")                  # shipped: benchmark + cascadia
UNIT = os.path.join(GOVERNED_DIR, "firstlight")

# The private core mapping is a REPRODUCTION input that lives in the repository and never in the
# wheel. It is read here only to recompile the committed publication and prove the shipped image is
# what the shipped compiler produces. It is never consulted by admission and never rendered.
ROOT = pathlib.Path(__file__).resolve().parent.parents[2]   # apps/website/scripts -> repo root
MAPPING = str(ROOT / "packages" / "columna-server" / "fixtures" / "firstlight"
              / "private-core-mapping.json")

MID = "firstlight"
LEGACY_MID = "cascadia"
STANDING_QUERY = "SELECT revenue.sum AT {store}"
LEGACY_QUERY = "SELECT revenue AT {store}"
REDUCERS = ("count", "max", "min", "sum")

# The ratified asymmetry, quoted rather than paraphrased (release notes, v0.16.2).
BOUNDARY = ("This fixture ships a governed publication that Columna can serve but cannot make. "
            "The authoring and ratification machinery that produced it is not part of this release. "
            "What is demonstrated here is consumption of governed authority, not its production.")


def die(msg: str) -> None:
    print(f"gen_firstlight: {msg}", file=sys.stderr)
    sys.exit(1)


def read_bytes(name: str, folder: str = UNIT) -> bytes:
    with open(os.path.join(folder, name), "rb") as f:
        return f.read()


def main() -> int:
    if not os.path.isdir(UNIT):
        die("the installed columna-server ships no governed/firstlight unit — this exhibit needs "
            ">= 0.11.0. Refusing to render a governed exhibit against a package that has no "
            "governed publication in it.")
    if not os.path.isfile(MAPPING):
        die(f"the reproduction input is missing at {MAPPING} — the image-reproduction check cannot "
            "run, and an exhibit that claims byte reproduction without performing it is the exact "
            "thing this generator exists to prevent.")

    pub_bytes = read_bytes("governed-publication.json")
    image_bytes = read_bytes("manifold.cml")
    receipt = json.loads(read_bytes(LOWERING_RECEIPT))
    publication = json.loads(pub_bytes)

    # ── the two catalogs, each read from the directory as shipped ────────────────────────────────
    gov_store = ManifoldStore(GOVERNED_DIR)
    demo_store = ManifoldStore(DEMO_DIR)
    gov_catalog = list_manifolds(gov_store)
    demo_catalog = list_manifolds(demo_store)

    # ── admission: governed, and nothing withheld ────────────────────────────────────────────────
    gov_conditions = [c.kind for c in gov_store.conditions()]
    if gov_conditions:
        die(f"firstlight is admitted with conditions {gov_conditions} — it is no longer a clean "
            "governed admission, and the exhibit would be claiming one.")
    lm = gov_store.get(MID)
    if lm.entry_kind != ENTRY_GOVERNED:
        die(f"firstlight is admitted as {lm.entry_kind!r}, not {ENTRY_GOVERNED!r}.")

    scope = lm.provider.runtime.published_scope
    if scope.certified_edges or scope.certified_faces:
        die("firstlight's certification sets are NOT empty — a lowering receipt would then look "
            "like it licensed a capability, which is precisely what this exhibit denies.")

    # ── the binding: the receipt digests the bytes that ship ─────────────────────────────────────
    if receipt["publication_digest"] != digest_bytes(pub_bytes):
        die("the shipped receipt does not digest the shipped publication.")
    if receipt["image_digest"] != digest_bytes(image_bytes):
        die("the shipped receipt does not digest the shipped image.")

    # ── the image is what the shipped compiler produces, byte for byte ───────────────────────────
    with open(MAPPING, encoding="utf-8") as f:
        mapping = json.load(f)
    recompiled = compile_k0(parse_publication(json.loads(pub_bytes)), parse_mapping(mapping))
    if recompiled.encode() != image_bytes:
        die("recompiling the committed publication does not reproduce the shipped image byte for "
            "byte — the compiler has drifted from the artifact this exhibit shows.")

    # ── serving: the answer carries its own standing ─────────────────────────────────────────────
    gov_wire = query(gov_store, MID, STANDING_QUERY)
    legacy_wire = query(demo_store, LEGACY_MID, LEGACY_QUERY)
    if gov_wire.get("outcome") != "serve" or "manifold_version" not in gov_wire:
        die("the governed serving wire does not carry a manifold_version — the one field this "
            "comparison turns on is missing.")
    if "manifold_version" in legacy_wire:
        die("the legacy serving wire carries a manifold_version — a compatibility runtime is "
            "unversioned, and the comparison this exhibit draws would be false.")

    reducers = []
    for r in sorted(REDUCERS):
        w = query(gov_store, MID, f"SELECT revenue.{r} AT {{store}}")
        col = w["columns"][0]
        if w.get("outcome") != "serve" or col.get("status") != "served":
            die(f"reducer {r} does not serve on firstlight — the exhibit claims all four do.")
        reducers.append({"reducer": r, "status": col["status"]})

    # ── standing licenses nothing: the counts say so out loud ────────────────────────────────────
    status = manifold_status(gov_store, MID)
    counts = status["counts"]
    for zero in ("hierarchies", "edges", "relations", "derived"):
        if counts[zero] != 0:
            die(f"firstlight now declares {counts[zero]} {zero} — the exhibit's whole point is that "
                "governed standing arrives with none of them.")
    if status["evidence"]["licenses"] != 0:
        die("firstlight now carries adjudicated licenses — the exhibit claims it carries none.")

    # ── nothing was promoted, and the path is generic ────────────────────────────────────────────
    legacy_kinds = {m.manifold_id: m.entry_kind for m in demo_store.all()}
    if set(legacy_kinds) != {"benchmark", "cascadia"} or set(legacy_kinds.values()) != {ENTRY_LEGACY}:
        die(f"the demo runtimes are no longer exactly two legacy entries: {legacy_kinds}")
    if [c.kind for c in demo_store.conditions()]:
        die("the legacy demos are no longer condition-free.")

    offenders = []
    for root in (CORE, SRV):
        for dirpath, _dirs, files in os.walk(root):
            if os.path.abspath(dirpath).startswith(os.path.abspath(UNIT)):
                continue
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                with open(os.path.join(dirpath, fname), "rb") as fh:
                    if b"firstlight" in fh.read().lower():
                        offenders.append(os.path.relpath(os.path.join(dirpath, fname), root))
    if offenders:
        die(f"shipped code special-cases the fixture: {offenders} — the path is no longer generic.")

    if os.path.exists(os.path.join(UNIT, "private-core-mapping.json")):
        die("the private mapping is inside the shipped unit — it is a reproduction input and must "
            "never travel with the runtime.")

    ratifications = publication["authority"]["ratifications"]
    payload = {
        "generated_by": f"columna-core {version('columna-core')} / columna-server {version('columna-server')}",
        "boundary": BOUNDARY,
        "unit": MID,
        # Two catalogs, each from its own shipped directory. `dir` is the package-relative path so a
        # reader can see that these are two places, not one assembled view.
        "catalogs": [
            {"dir": "columna_server/governed/", "wire": gov_catalog},
            {"dir": "columna_server/demo/", "wire": demo_catalog},
        ],
        "publication": {
            "ref": publication["ref"],
            "bytes": len(pub_bytes),
            "published_by": publication["authority"]["published_by"],
            "universes_ratified": sorted(ratifications),
            "fingerprint_version": sorted({r["fingerprint_version"] for r in ratifications.values()}),
        },
        "image": {"text": image_bytes.decode("utf-8"), "bytes": len(image_bytes)},
        "receipt": {
            "compiler": receipt["compiler"],
            # P0-19 (ruled Huayin, 2026-08-31). `compiler.version` is a HISTORICAL claim — the
            # producer of these frozen bytes, not the version of the package a reader just installed.
            # It was rendered bare, a few lines below the words "the shipped K0 compiler", with the
            # one field that dates it dropped from this payload. A true statement presented as a
            # current one is the defect the currency guard exists for, so the date ships with it.
            "established_at": receipt.get("established_at"),
            "publication_ref": receipt["publication_ref"],
            "publication_digest": receipt["publication_digest"],
            "image_digest": receipt["image_digest"],
            "receipt_format_version": receipt["receipt_format_version"],
        },
        "image_reproduces": True,
        "serving": {
            "governed": {"manifold": MID, "query": STANDING_QUERY, "wire": gov_wire},
            "legacy": {"manifold": LEGACY_MID, "query": LEGACY_QUERY,
                       "wire": {k: v for k, v in legacy_wire.items() if k != "columns"}},
        },
        "reducers": reducers,
        "status": {"counts": counts, "licenses": status["evidence"]["licenses"],
                   "certified_edges": len(scope.certified_edges),
                   "certified_faces": len(scope.certified_faces)},
    }
    json.dump(payload, sys.stdout, indent=2, sort_keys=True, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

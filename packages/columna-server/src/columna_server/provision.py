"""
columna_server.provision — assemble a runtime unit. An ASSEMBLER, never a semantic authority.

    governed-publication.json + manifold.cml + lowering-receipt.json + operator config
        -> <runtime-manifold>/

THE ONE RULE THIS MODULE EXISTS TO KEEP: **it copies bytes, it does not re-emit them.**

The lowering receipt binds a publication to an execution image by content digest over the files AS
SHIPPED, with no canonicalization. So a provisioner that re-serialized the publication — even to an
equivalent JSON, even sorting the same keys — or that reformatted the ``.cml``, would produce a unit
whose receipt no longer describes its own files. The binding the compiler established must survive
provisioning UNCHANGED, and the only way to guarantee that is to move the exact bytes.

That is also why this module verifies by RECOMPUTING rather than by trusting. It digests the bytes it
is about to copy and compares them to what the receipt claims. A mismatch is a refusal, never a
repair: re-deriving a receipt to match the files would convert "these three artifacts belong
together" into "these three artifacts have been made to agree", which is the difference between
evidence and decoration.

WHAT IT MAY DO
  · verify the publication / image / receipt refs agree
  · recompute and verify the publication and image byte digests
  · copy the already-produced bytes into the runtime unit
  · add deployment configuration
  · refuse on mismatch or missing required inputs

WHAT IT MAY NOT DO — and cannot, by construction
  · reserialize or rewrite the governed publication   (bytes are read and written, never parsed-then-dumped)
  · rewrite the ``.cml``                              (same)
  · regenerate the lowering receipt                   (there is no receipt builder in this module)
  · infer or repair semantic meaning                  (nothing here constructs a Manifold)
  · read meaning back from the ``.cml``               (see `_claimed_ref`: ONE statement, identity only)
  · alter publication identity · fabricate a receipt · silently pair unrelated artifacts

THE ``.cml`` SCAN, precisely. `_claimed_ref` reads exactly one statement — ``SOURCE_MANIFOLD`` — and
returns the ref it claims. That is an IDENTITY claim, the same thing `registry.source_ref_of` reads,
and it is deliberately obtained WITHOUT parsing the manifold: no universes, no measures, no levels,
nothing that could become meaning. Reading which publication an image claims is not reading what the
image means.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
from dataclasses import dataclass

from .lowering_receipt import (
    LOWERING_RECEIPT,
    LoweringReceiptError,
    parse_lowering_receipt,
)
from .registry import ManifoldRef, PublicationArtifactError, parse_publication_artifact

#: The runtime deployment contract, in the order a reader should think about it: authority, its
#: realization, the binding between them, and how to reach the data.
RUNTIME_FILES = ("governed-publication.json", "manifold.cml", LOWERING_RECEIPT, "data.toml")

#: A single statement, read for identity only. Mirrors the parser's own SOURCE_MANIFOLD grammar.
_SOURCE_MANIFOLD = re.compile(
    r"^SOURCE_MANIFOLD\s+([\w.:@/-]+)\s+VERSION\s+"
    r"(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)\s*$"
)

_DIGEST_PREFIX = "sha256:"


# ── refusals ─────────────────────────────────────────────────────────────────────────────────────
class ProvisionRefusal(Exception):
    """A fail-closed provisioning refusal. Never repaired, never downgraded to a warning.

    Distinct from the compiler's taxonomy on purpose: those categories answer "whose GAP is this?"
    about governed meaning. These answer "do these artifacts belong together, and are they all
    here?" — an assembly question, with no semantic content at all."""

    category = "ProvisionRefusal"

    def __init__(self, detail: str, *, subject: str = ""):
        self.detail = detail
        self.subject = subject
        where = f" [{subject}]" if subject else ""
        super().__init__(f"{self.category}{where}: {detail}")


class MissingInput(ProvisionRefusal):
    """A required input is absent. A unit assembled from what happened to be present is exactly the
    arbitrary co-location governed standing was tightened to exclude."""

    category = "MissingInput"


class MalformedInput(ProvisionRefusal):
    """An input is structurally unreadable. Note the provisioner reads only enough structure to
    check identity and digests — it never validates meaning, which is not its job."""

    category = "MalformedInput"


class IdentityDisagreement(ProvisionRefusal):
    """The publication, the image and the receipt do not all name the same publication.

    Three sources of the same ref must agree: the artifact's own `ref`, the image's SOURCE_MANIFOLD
    claim, and the receipt's binding. Two agreeing and one differing is precisely the silent pairing
    of unrelated artifacts."""

    category = "IdentityDisagreement"


class DigestMismatch(ProvisionRefusal):
    """A recomputed digest disagrees with the receipt's. The bytes are not the bytes the compiler
    bound — because one of them was edited, or because the wrong file was supplied."""

    category = "DigestMismatch"


class DestinationNotEmpty(ProvisionRefusal):
    """The destination already holds a unit. Provisioning over it could pair new files with stale
    leftovers, so it refuses rather than merging."""

    category = "DestinationNotEmpty"


CATEGORIES = (MissingInput.category, MalformedInput.category, IdentityDisagreement.category,
              DigestMismatch.category, DestinationNotEmpty.category)


@dataclass(frozen=True)
class ProvisionedUnit:
    """What was assembled. The digests are the ones VERIFIED, not merely copied."""

    path: str
    ref: ManifoldRef
    publication_digest: str
    image_digest: str
    files: tuple


# ── helpers ──────────────────────────────────────────────────────────────────────────────────────
def _read(path: str, what: str) -> bytes:
    if not path or not os.path.isfile(path):
        raise MissingInput(f"{what} not found at {path!r}", subject=what)
    with open(path, "rb") as f:
        return f.read()


def _digest(payload: bytes) -> str:
    return _DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()


def _claimed_ref(image_bytes: bytes) -> ManifoldRef:
    """The publication this image CLAIMS to realize. Identity only — never meaning.

    Reads one statement. A duplicate is malformed (the parser calls a second SOURCE_MANIFOLD a
    category error, not an override); an absent one cannot be provisioned as governed, because an
    image making no claim has nothing for the publication to agree WITH."""
    found = None
    try:
        text = image_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MalformedInput(f"execution image is not UTF-8: {exc}", subject="manifold.cml") from exc
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("SOURCE_MANIFOLD"):
            continue
        m = _SOURCE_MANIFOLD.match(s)
        if not m:
            raise MalformedInput(f"unreadable SOURCE_MANIFOLD statement: {s!r}",
                                 subject="manifold.cml")
        if found is not None:
            raise MalformedInput(
                "duplicate SOURCE_MANIFOLD — an image realizes exactly one publication",
                subject="manifold.cml")
        found = ManifoldRef(m.group(1), m.group(2))
    if found is None:
        raise IdentityDisagreement(
            "execution image carries no SOURCE_MANIFOLD; it claims no publication, so there is "
            "nothing for the artifact and receipt to agree with", subject="manifold.cml")
    return found


# ── the provisioner ──────────────────────────────────────────────────────────────────────────────
def provision_runtime_unit(dest: str, *, publication: str, image: str, receipt: str,
                           data_toml: str, overwrite: bool = False) -> ProvisionedUnit:
    """Assemble a runtime unit at ``dest`` from three already-produced artifacts.

    ``publication``/``image``/``receipt`` are PATHS to bytes someone else produced. ``data_toml`` is
    operator/deployment configuration, written verbatim — the provisioner does not compose it,
    because connector choice and warehouse location are operator decisions, not derivable facts.

    Verification order is deliberate: presence, then structure, then IDENTITY, then DIGESTS. Identity
    before digests so that pairing the wrong artifacts reports a disagreement about WHICH publication
    rather than an opaque hash difference — the same reason `InputIdentityMismatch` sits ahead of the
    compiler's gap categories."""
    pub_bytes = _read(publication, "governed-publication.json")
    img_bytes = _read(image, "manifold.cml")
    rec_bytes = _read(receipt, LOWERING_RECEIPT)
    if not isinstance(data_toml, str) or not data_toml.strip():
        raise MissingInput("deployment configuration (data.toml) is required and must be non-empty",
                           subject="data.toml")

    # structure — only as much as identity and digests need
    try:
        rec = parse_lowering_receipt(_json_loads(rec_bytes, LOWERING_RECEIPT))
    except LoweringReceiptError as exc:
        raise MalformedInput(str(exc), subject=LOWERING_RECEIPT) from exc
    try:
        art = parse_publication_artifact(_json_loads(pub_bytes, "governed-publication.json"))
    except PublicationArtifactError as exc:
        raise MalformedInput(str(exc), subject="governed-publication.json") from exc

    # identity — all three must name the same publication
    claimed = _claimed_ref(img_bytes)
    if art.ref != rec.binding.publication_ref or art.ref != claimed:
        raise IdentityDisagreement(
            f"artifact says {art.ref.manifold_id}@{art.ref.version}, image claims "
            f"{claimed.manifold_id}@{claimed.version}, receipt binds "
            f"{rec.binding.publication_ref.manifold_id}@{rec.binding.publication_ref.version}")

    # digests — recomputed over the bytes about to be copied, never taken on trust
    pub_digest, img_digest = _digest(pub_bytes), _digest(img_bytes)
    if pub_digest != rec.binding.publication_digest:
        raise DigestMismatch(
            f"publication bytes digest {pub_digest} but the receipt binds "
            f"{rec.binding.publication_digest}", subject="governed-publication.json")
    if img_digest != rec.binding.image_digest:
        raise DigestMismatch(
            f"image bytes digest {img_digest} but the receipt binds {rec.binding.image_digest}",
            subject="manifold.cml")

    # assemble — into a sibling, then one rename, so a failed provision leaves no half-unit
    if os.path.exists(dest) and os.listdir(dest) and not overwrite:
        raise DestinationNotEmpty(
            f"{dest!r} already holds files; provisioning over them could pair new artifacts with "
            f"stale leftovers", subject=dest)
    staging = dest.rstrip(os.sep) + ".incoming"
    if os.path.exists(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)
    try:
        _write(staging, "governed-publication.json", pub_bytes)
        _write(staging, "manifold.cml", img_bytes)
        _write(staging, LOWERING_RECEIPT, rec_bytes)
        _write(staging, "data.toml", data_toml.encode("utf-8"))
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.replace(staging, dest)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    return ProvisionedUnit(path=dest, ref=art.ref, publication_digest=pub_digest,
                           image_digest=img_digest, files=RUNTIME_FILES)


def _write(folder: str, name: str, payload: bytes) -> None:
    """Write the EXACT bytes. No text mode, no encoding round-trip, no newline translation — all
    three are ways a copy stops being a copy."""
    with open(os.path.join(folder, name), "wb") as f:
        f.write(payload)


def _json_loads(payload: bytes, what: str):
    import json
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MalformedInput(f"{what} is not valid UTF-8 JSON: {exc}", subject=what) from exc

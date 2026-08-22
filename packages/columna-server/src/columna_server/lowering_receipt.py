"""
columna_server.lowering_receipt — the publication→execution-image binding, and nothing else.

WHAT THIS ESTABLISHES, EXACTLY (CG2 ruling, 2026-08-22 §1):

    exact governed publication  →  exact compiled Core execution image

and **nothing beyond that**. A receipt is NOT certification, NOT attestation, NOT ``PublishedScope``
admission, and NOT evidence that any capability may currently execute. The lifecycle is unchanged
and the receipt sits at exactly one step of it::

    publication + mapping
        → compile CLOSED image        ← the receipt records THIS step, and only this step
        → realization/data adjudication
        → certification
        → PublishedScope admission
        → serve

Receipt presence must therefore never be read as current certification. It answers one question —
*was this image compiled from this publication?* — and stays silent on every other.

WHY IT EXISTS. ``SOURCE_MANIFOLD`` inside a ``.cml`` is an ORIGIN CLAIM: it says which publication
the artifact claims to have been lowered from. It is not, by itself, evidence that semantic
conformance was ever established — a hand-authored ``.cml`` can carry any claim its author types.
Semantic conformance belongs to Core-P1 lowering BY CONSTRUCTION (the compiler's only inputs are the
governed publication and the private mapping, and it fails closed when governed law cannot be
faithfully represented). The receipt is what carries that discharged obligation across the
lowering→provisioning→admission boundary, so the runtime can trust it without re-establishing it.

THE RUNTIME MUST BE ABLE TO VERIFY THE BINDING WITHOUT (ruling §2):
  · loading the private mapping;
  · reconstructing logical meaning from the ``.cml``;
  · re-running lowering.
All three follow from the representation: the binding is two content digests and a ref. Verification
is ``sha256`` over two files the store already has open, and a dataclass comparison.

MEANING-FREE BY TYPE, NOT BY DISCIPLINE. ``LoweringReceipt`` has nowhere to put a universe, a
measure, a level, a predicate or a family. Unknown keys in the JSON are ignored rather than mapped,
so nothing outside the fields below can reach the runtime even if a producer writes it. This is what
keeps the receipt from becoming a second, quieter channel for publication meaning — the blast wall
holds because there is no door, not because nobody opens it.

BINDING IDENTITY IS DETERMINISTIC (ruling §2). Two receipts produced from identical inputs bind
identically. ``LoweringBinding`` — the ref plus the two digests — IS the binding identity, and it is
the only thing admission consults. ``compiler`` and ``mapping_provenance`` are retained as OPAQUE
PROVENANCE and ``established_at`` as a NON-AUTHORITATIVE timestamp; none of the three participates in
the binding, and none is a runtime admission dependency. A receipt that differs only in when it was
written, or which mapping revision produced it, binds the same image to the same publication.

THREAT MODEL (recorded, so the guarantee is not over-read). The publication format is *structural
authority transfer, not cryptographic authenticity*, and this receipt matches that scope. Content
digests catch the failures that actually occur — a provisioner pairing the wrong two files, a stale
image surviving a republish, an in-place edit on a running host, a hand-written ``SOURCE_MANIFOLD``
with no receipt behind it. They do NOT resist a forger: anyone who can write the runtime folder can
write a self-consistent receipt. What the receipt changes is that governed standing can no longer be
acquired BY ACCIDENT — only by deliberately forging a compiler's claim. Signing is a separate ruling;
the schema leaves room for it.

FORMAT VOCABULARY. Three conditions, fixed by ruling §3: missing / invalid / mismatch. Unlike the
publication artifact — where an unsupported format major is deliberately distinct from a malformed
artifact — an unsupported receipt major is an ``LoweringReceiptInvalid``. The public vocabulary was
ruled at three codes and this module does not widen it.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Optional

from .registry import ManifoldRef

#: The binding artifact retained beside a governed .cml realization. The runtime deployment contract
#: for artifact-backed Core serving is:
#:     <runtime-manifold>/{governed-publication.json, manifold.cml, lowering-receipt.json, data.toml}
LOWERING_RECEIPT = "lowering-receipt.json"

#: The receipt format major this server understands. Its own dimension — unrelated to the wire
#: CONTRACT_VERSION, the publication artifact's format version, columna-core's engine VERSION, or the
#: Manifold's semantic version.
SUPPORTED_RECEIPT_FORMAT_MAJOR = 1

#: Digests are content digests over the file AS SHIPPED — no canonicalization step, deliberately.
#: Canonical-form digests need a canonicalizer on both sides and every disagreement between the two
#: is a false mismatch; byte digests have no such surface. Reformatting `manifold.cml` IS a change to
#: the execution image, so a digest that breaks on reformatting is reporting the truth.
_DIGEST_ALGO = "sha256"
_DIGEST_PREFIX = f"{_DIGEST_ALGO}:"
_DIGEST_HEXLEN = 64


# ── errors — pre-adjudication ingest conditions, never analytical moods ──────────────────────────
class LoweringReceiptError(Exception):
    """Base for problems with a ``lowering-receipt.json`` — a pre-adjudication serving/ingest
    condition like the publication-artifact errors, never one of the wire's four moods."""


class LoweringReceiptMissing(LoweringReceiptError):
    """A runtime carries a publication artifact and a matching ``SOURCE_MANIFOLD`` claim, but no
    ``lowering-receipt.json``. The origin claim is present; the evidence that a compiler established
    it is not. Compatibility-served, never governed — an unproven realization binding never becomes a
    proven one by being asserted more loudly."""


class LoweringReceiptInvalid(LoweringReceiptError):
    """The receipt is malformed, structurally inconsistent, or claims a format major this server does
    not understand. A deployment/artifact defect."""


class LoweringReceiptMismatch(LoweringReceiptError):
    """The receipt does not bind THESE two files: its ref disagrees with the publication/realization,
    or a content digest does not match the file as shipped. The provider must not attach as the
    realization of that publication — an invalid realization binding, never auto-repaired."""


# ── the binding ──────────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class LoweringBinding:
    """THE BINDING IDENTITY — deterministic for identical inputs, and the only thing admission reads.

    A publication ref plus the content digests of the two files the binding relates. It carries no
    timestamp, no compiler build, no mapping revision and no meaning, so two receipts produced from
    identical inputs compare equal however and whenever they were written."""

    publication_ref: ManifoldRef
    publication_digest: str
    image_digest: str


@dataclass(frozen=True)
class LoweringReceipt:
    """A parsed receipt: its binding, plus provenance that is retained and never depended on.

    ``compiler``, ``mapping_provenance`` and ``established_at`` are OPAQUE — recorded for operators
    and post-mortems, excluded from ``binding``, and never consulted by admission. In particular the
    private mapping is never loaded, and its provenance being absent is not a defect."""

    format_version: str
    binding: LoweringBinding
    compiler: dict
    mapping_provenance: Optional[Any] = None
    established_at: Optional[str] = None


def digest_bytes(payload: bytes) -> str:
    """The content digest of a payload, as ``sha256:<hex>``."""
    return _DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()


def digest_file(path: str) -> str:
    """The content digest of a file AS SHIPPED — the bytes on disk, unparsed and uncanonicalized."""
    with open(path, "rb") as f:
        return digest_bytes(f.read())


def _major(version: str) -> int:
    try:
        return int(str(version).split(".", 1)[0])
    except (ValueError, AttributeError) as exc:
        raise LoweringReceiptInvalid(
            f"unreadable receipt_format_version {version!r}: expected 'MAJOR.MINOR'"
        ) from exc


def _digest_field(data: dict, key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise LoweringReceiptInvalid(f"missing {key}")
    if not value.startswith(_DIGEST_PREFIX):
        raise LoweringReceiptInvalid(
            f"{key} must be a {_DIGEST_ALGO} content digest ('{_DIGEST_PREFIX}<hex>'), got {value!r}"
        )
    hexpart = value[len(_DIGEST_PREFIX):]
    if len(hexpart) != _DIGEST_HEXLEN or any(c not in "0123456789abcdef" for c in hexpart):
        raise LoweringReceiptInvalid(f"{key} is not a lowercase {_DIGEST_ALGO} hex digest")
    return value


def parse_lowering_receipt(data: Any) -> LoweringReceipt:
    """Structurally validate a receipt and return its plain-data reading.

    STRUCTURE ONLY. This says nothing about whether the binding HOLDS — that is ``verify_binding``,
    which needs the two files. It also says nothing about semantic conformance: establishing that is
    the compiler's obligation, discharged before this artifact existed, and re-establishing it here
    would duplicate lowering and breach the blast wall.

    Unknown keys are IGNORED, not mapped: a producer cannot smuggle publication meaning into the
    runtime through a field this type has no room for.
    """
    if not isinstance(data, dict):
        raise LoweringReceiptInvalid("receipt is not a JSON object")

    fmt = data.get("receipt_format_version")
    if not isinstance(fmt, str) or not fmt:
        raise LoweringReceiptInvalid("missing receipt_format_version")
    if _major(fmt) != SUPPORTED_RECEIPT_FORMAT_MAJOR:
        raise LoweringReceiptInvalid(
            f"receipt_format_version {fmt!r} has an unsupported major (this server supports "
            f"major {SUPPORTED_RECEIPT_FORMAT_MAJOR})"
        )

    ref = data.get("publication_ref")
    if not isinstance(ref, dict):
        raise LoweringReceiptInvalid("missing publication_ref object")
    mid, ver = ref.get("manifold_id"), ref.get("version")
    if not isinstance(mid, str) or not mid or not isinstance(ver, str) or not ver:
        raise LoweringReceiptInvalid("publication_ref must carry a concrete manifold_id and version")

    publication_digest = _digest_field(data, "publication_digest")
    image_digest = _digest_field(data, "image_digest")

    # Provenance is required to be PRESENT and well-shaped (a receipt with no idea what produced it
    # is not a receipt), but its CONTENT is never interpreted and never gates admission.
    compiler = data.get("compiler")
    if not isinstance(compiler, dict):
        raise LoweringReceiptInvalid("missing compiler object")
    if not isinstance(compiler.get("name"), str) or not compiler.get("name"):
        raise LoweringReceiptInvalid("compiler.name is required")
    if not isinstance(compiler.get("version"), str) or not compiler.get("version"):
        raise LoweringReceiptInvalid("compiler.version is required")

    established_at = data.get("established_at")
    if established_at is not None and not isinstance(established_at, str):
        raise LoweringReceiptInvalid("established_at, when present, must be a string")

    return LoweringReceipt(
        format_version=fmt,
        binding=LoweringBinding(
            publication_ref=ManifoldRef(mid, ver),
            publication_digest=publication_digest,
            image_digest=image_digest,
        ),
        compiler=compiler,
        mapping_provenance=data.get("mapping_provenance"),
        established_at=established_at,
    )


def load_lowering_receipt(path: str) -> LoweringReceipt:
    """Read + structurally validate a ``lowering-receipt.json`` from disk (stdlib JSON only).
    Malformed JSON is a ``LoweringReceiptInvalid`` like any other structural defect."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as exc:
        raise LoweringReceiptInvalid(f"receipt is not valid JSON: {exc}") from exc
    return parse_lowering_receipt(raw)


def verify_binding(receipt: LoweringReceipt, artifact_ref: ManifoldRef,
                   artifact_path: str, image_path: str) -> None:
    """Verify that this receipt binds THESE two files to THIS publication. Raises on any disagreement.

    Three comparisons, all local and all meaning-free: the ref the receipt was written for, and the
    two files' content digests as shipped. No mapping is loaded, no ``.cml`` is interpreted, no
    lowering is re-run — the receipt is trusted for what a compiler established, and checked for
    whether it is talking about the files actually present.
    """
    if receipt.binding.publication_ref != artifact_ref:
        raise LoweringReceiptMismatch(
            f"receipt binds {receipt.binding.publication_ref.manifold_id}@"
            f"{receipt.binding.publication_ref.version}, not "
            f"{artifact_ref.manifold_id}@{artifact_ref.version}"
        )
    actual_publication = digest_file(artifact_path)
    if actual_publication != receipt.binding.publication_digest:
        raise LoweringReceiptMismatch(
            f"publication bytes do not match the receipt "
            f"(receipt {receipt.binding.publication_digest}, on disk {actual_publication})"
        )
    actual_image = digest_file(image_path)
    if actual_image != receipt.binding.image_digest:
        raise LoweringReceiptMismatch(
            f"execution image bytes do not match the receipt "
            f"(receipt {receipt.binding.image_digest}, on disk {actual_image})"
        )

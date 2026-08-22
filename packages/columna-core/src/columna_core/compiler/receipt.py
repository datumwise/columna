"""
columna_core.compiler.receipt — the producer side of the publication->image binding.

The VERIFIER lives in `columna-server` (`columna_server.lowering_receipt`) and this module must not
import it: `columna-server` depends on `columna-core`, never the reverse. The receipt schema is a
frozen contract written down in the K0 design freeze, so both ends implement it independently and a
round-trip test proves they agree. That is the same shape as the publication artifact, whose
producer and consumer also share no code.

WHAT A RECEIPT ESTABLISHES, EXACTLY (ruling 2026-08-22 §1):

    exact governed publication  ->  exact compiled Core execution image

and nothing beyond it. Not certification, not attestation, not `PublishedScope` admission. A
receipt says "a compiler produced this image from this publication". It says nothing about whether
any capability may currently execute, and emitting one must never read as though it did.

DIGESTS ARE OVER BYTES AS SHIPPED — no canonicalization. Canonical-form digests need a canonicalizer
on both sides and every disagreement between the two is a false mismatch; byte digests have no such
surface. Reformatting the image IS a change to the image, so a digest that breaks on reformatting is
reporting the truth.
"""
from __future__ import annotations

import hashlib
import json
from typing import Optional

#: The receipt format this compiler writes. Major must match what the runtime supports; its own
#: dimension, unrelated to the publication format, the mapping format, or the wire contract.
RECEIPT_FORMAT_VERSION = "1.0"

RECEIPT_FILENAME = "lowering-receipt.json"

_DIGEST_PREFIX = "sha256:"


def digest_bytes(payload: bytes) -> str:
    """`sha256:<hex>` over the payload exactly as it will be shipped."""
    return _DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()


def build_receipt(*, manifold_id: str, version: str, publication_bytes: bytes,
                  image_bytes: bytes, compiler_name: str, compiler_version: str,
                  mapping_provenance=None, established_at: Optional[str] = None) -> dict:
    """The receipt as plain data.

    `compiler` is REQUIRED and well-shaped but never interpreted by the runtime; `mapping_provenance`
    and `established_at` are retained as opaque provenance and are excluded from the binding. That
    exclusion is what makes the binding deterministic: two receipts produced from identical inputs
    bind identically however and whenever they were written.

    `established_at` is therefore the one place a timestamp may appear. It must NOT reach the image
    itself, whose bytes are digested."""
    if not compiler_name or not compiler_version:
        raise ValueError("compiler.name and compiler.version are required by the receipt contract")
    receipt = {
        "receipt_format_version": RECEIPT_FORMAT_VERSION,
        "publication_ref": {"manifold_id": manifold_id, "version": version},
        "publication_digest": digest_bytes(publication_bytes),
        "image_digest": digest_bytes(image_bytes),
        "compiler": {"name": compiler_name, "version": compiler_version},
    }
    if mapping_provenance is not None:
        receipt["mapping_provenance"] = mapping_provenance
    if established_at is not None:
        receipt["established_at"] = established_at
    return receipt


def render_receipt(receipt: dict) -> str:
    """Serialize deterministically. Sorted keys, stable separators, one trailing newline.

    The receipt's own bytes are not digested by anything, but determinism here means a re-run
    produces an identical runtime folder, which is what makes a provisioning diff meaningful."""
    return json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False) + "\n"

"""
columna_platform.kernel.witness — **the ConstitutionWitness, COMPUTED from identity-bearing governed facts.**

    *"Make `ConstitutionWitness` derived from identity-bearing governed facts… The ConstitutionWitness
    should answer: what identity-bearing governed constitution was this family or expression established
    under?"* — Huayin, 2026-09-29 (P-1)

THREE FACTS, KEPT APART, AND THE RULING THAT SAYS SO
----------------------------------------------------
    *"Keep these three things distinct: **ConstitutionWitness** — which governed analytical constitution
    this object belongs to; **AnalyticalInstance / data-state identity** — which actual root/evidence state
    this retained material belongs to; **Realization standing** — which physical/provider/codec realization
    produced or carries it. Do not collapse them into one version/freshness token."*

So this module computes ONE of the three and knows nothing about the other two. There is no field here for
a load, a refresh, a snapshot, a file, a provider or a codec, and that absence is the design:

    ConstitutionWitness   `witness.py`        computed here, from the DECLARATION alone
    data-state identity   `standing.py`       `AnalyticalInstance.data_state` — which evidence state
    realization standing  `realization.py`    `RealizationStanding` — which provider/carrier

A `RetentionKey` references all three (it must, to tell retained objects apart), and referencing them is
not collapsing them: each remains separately computed, separately compared, and separately reportable, so
"the constitution moved", "the data was reloaded" and "the provider changed" are three different answers.

WHY THE DETERMINANTS ARE DERIVED BY SUBTRACTION, NOT ENUMERATED BY INCLUSION
----------------------------------------------------------------------------
The determinant set is **every field of the record MINUS a written-down exclusion list.** This is Core's
own rule for its native family fingerprint (`governed/native.py`: *"Everything else is IN by derivation — a
body key added later is inside the fingerprint by default, and taking one out is a decision someone has to
write down"*), and it is adopted here for the same reason: the failure mode of an inclusion list is a new
identity-bearing field that silently never enters the witness, and that failure is invisible.

Both directions are mechanical. A field ADDED to `MeasureFamily` or `GovernedExpression` enters the witness
with no code change, because the determinants are read from `dataclasses.fields` at computation time — so the
dangerous direction cannot be forgotten. And an exclusion that OUTLIVES its field is refused
(`stale-non-determinant`), because an exclusion naming nothing would quietly stop excluding anything.

WHAT THE DIGEST IS AND EMPHATICALLY IS NOT
------------------------------------------
    *"Do not invent persistence format or serialization yet."*

The digest is an **in-process** digest over an in-process canonical form. It is deliberately built from
Python `repr` for parameter values and carries a scheme tag, `cw-1`, so that:

* it is **not** a wire format, not a persistence format, and not stable across kernel versions — nothing
  in this package writes it anywhere;
* it is **not** Core's `fcf-1:`/`fcf-2:` family-constitution fingerprint and must never be compared with
  one. Different determinants, different scheme namespace, and no import in either direction. Two schemes
  that could be confused for each other would be worse than two that obviously cannot.

Comparison is by DETERMINANTS, not by digest: `compare` reports which named determinant moved, which is
what makes constitution staleness legible instead of merely detectable.

WHAT IS EXCLUDED, AND THE REASON FOR EACH — THE PART OF THIS FILE THAT IS DOCTRINE
---------------------------------------------------------------------------------
* `family_id` / `expression_id` — **a label, and identity cannot be part of its own determinant.** Core's
  ruling (R12 precedent, `NON_IDENTITY_KEYS`) is followed exactly. A consequence is accepted openly: two
  objects with identical governed constitutions share a digest. The witness answers *which constitution*,
  not *which object*; `ConstitutionWitness.identity` names the object beside it, and `RetentionKey` keys
  on the identity separately.
* `target` (family) — a description. Negative control 4: *"non-identity metadata / alias / description
  change → same ConstitutionWitness."*
* `admitted_bases` (expression) — ruled 2026-09-28: *"expression identity ≠ one particular sufficient
  basis used to establish it."* A basis is a ROUTE to establishment, not what the expression IS, and
  admitting a new route must not stale values already established over an existing one. Which route was
  actually taken rides on the value, as `ExpressionOutput.basis_id`.
* `constitution` — the **retired caller-supplied slot**. It is kept as a field solely so that a caller who
  supplies one is REFUSED rather than silently ignored, and it cannot be its own determinant.

Everything else is in: `manifold`, `universe`, `root`, `law`, `value_domain`, `participation`, `order_by`,
`parameters` for a family; `manifold`, `universe`, `constructor`, `operands` (role AND family), `inner_anchors`,
`participation`, `scope`, `parameters` for an expression. That covers every fact the ruling enumerates as
identity-bearing — *"root, continuation law, constitutive order, participation law, operand identity, role,
constitutive anchor, or identity-bearing parameter"* — and `parameters` is taken WHOLE rather than filtered to
the law's `required_parameters`, conservatively: a witness that is too strict can force a re-establishment
that was not needed, and one that is too loose can serve a value from a constitution that no longer exists.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Mapping

from .geometry import KernelRefusal

#: The witness scheme. **Not `fcf-*`** — see the module docstring; the tag exists so the two can never be
#: mistaken for one another, and so a later scheme can supersede this one legibly.
WITNESS_SCHEME = "cw-1"

#: How many hex characters of the digest the witness carries. Enough to be a key in one process; short
#: enough that nobody mistakes it for a published attestation.
DIGEST_CHARS = 16

FAMILY_SORT = "family"
EXPRESSION_SORT = "expression"

#: **Written-down exclusions.** Everything not listed here is a determinant BY DERIVATION. Each entry is a
#: decision with a reason in the module docstring; adding one is a doctrine change, not a refactor.
FAMILY_NON_DETERMINANTS: frozenset[str] = frozenset({"family_id", "target", "constitution"})
EXPRESSION_NON_DETERMINANTS: frozenset[str] = frozenset(
    {"expression_id", "admitted_bases", "constitution"})


@dataclass(frozen=True)
class ConstitutionWitness:
    """**Which identity-bearing governed constitution an object was established under.**

    Carries its determinants, not only its digest, because a witness that can only say *"different"* makes
    constitution change detectable and not diagnosable — and the one question a steward actually asks is
    *which* governed fact moved."""

    sort: str
    identity: str
    scheme: str
    #: `(determinant name, canonical rendering)`, sorted by name. The authority for comparison.
    determinants: tuple[tuple[str, str], ...]
    digest: str

    def __str__(self) -> str:
        return self.digest

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(n for n, _ in self.determinants)

    def determinant(self, name: str) -> str:
        for n, v in self.determinants:
            if n == name:
                return v
        raise KernelRefusal(
            "not-a-determinant", self.identity,
            f"{name!r} is not a determinant of this {self.sort} witness. Its determinants are "
            f"{list(self.names)}; a field outside them is classified as NOT identity-bearing, and asking "
            f"this object about it would imply otherwise.")

    def matches(self, other: "ConstitutionWitness") -> bool:
        return self.compare(other).identical

    def compare(self, other: "ConstitutionWitness") -> "WitnessComparison":
        """**Which determinants moved.** Truthy when the two constitutions are the same one."""
        if self.sort != other.sort:
            return WitnessComparison(
                False, (), f"a {self.sort} witness and a {other.sort} witness are not comparable: the two "
                           f"sorts are peers with different determinants, and 'the same constitution' is "
                           f"not a question that spans them")
        mine, theirs = dict(self.determinants), dict(other.determinants)
        changed = tuple(sorted(n for n in set(mine) | set(theirs) if mine.get(n) != theirs.get(n)))
        if not changed:
            return WitnessComparison(True, (), f"the same governed constitution ({self.digest})")
        moves = "; ".join(f"{n}: {mine.get(n, '<absent>')!r} → {theirs.get(n, '<absent>')!r}"
                          for n in changed)
        return WitnessComparison(
            False, changed,
            f"the governed constitution moved in {len(changed)} identity-bearing determinant(s) — {moves}. "
            f"A state established under {self.digest} is STALE against {other.digest}: it is not "
            f"an alternative reading, and it is not patched — re-establishment is from the root.")


@dataclass(frozen=True)
class WitnessComparison:
    """Truthy when the two witnesses are the same constitution — the house shape, as `Compatibility`."""

    identical: bool
    changed: tuple[str, ...]
    detail: str

    def __bool__(self) -> bool:
        return self.identical


# ══ computation ═══════════════════════════════════════════════════════════════════════════════════
def _canonical(value: Any) -> str:
    """One deterministic in-process rendering of a determinant value.

    **NOT a serialization format** (see the module docstring). Mappings and sets are ordered so that a
    declaration's spelling order cannot change a witness, and everything else falls through to `repr`,
    which is exactly as portable as this needs to be: not at all."""
    if value is None:
        return "∅"
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        return "{" + ", ".join(f"{k}={_canonical(v)}" for k, v in sorted(value.items())) + "}"
    if isinstance(value, (frozenset, set)):
        return "{" + ", ".join(sorted(_canonical(v) for v in value)) + "}"
    if isinstance(value, (tuple, list)):
        return "[" + ", ".join(_canonical(v) for v in value) + "]"
    if hasattr(value, "role") and hasattr(value, "family_id"):        # Operand — role IS identity
        return f"{value.role}→{value.family_id}"
    if hasattr(value, "constituents") and hasattr(value, "universe"):  # Anchor — already canonical
        return str(value)
    return repr(value)


def _determinants(obj: Any, non_determinants: frozenset[str], sort: str) -> tuple[tuple[str, str], ...]:
    """Every dataclass field of `obj` except the written-down exclusions — **and a refusal if a field is
    neither.** This is the guard that makes derivation-by-subtraction safe: a field added to a governed
    record is identity-bearing by default, and until somebody classifies it, nothing gets a witness."""
    present = {f.name for f in fields(obj)}
    unknown = sorted(non_determinants - present)
    if unknown:
        raise KernelRefusal(
            "stale-non-determinant", getattr(obj, f"{sort}_id", sort),
            f"the exclusion list names {unknown}, which {type(obj).__name__} no longer has. An exclusion "
            f"outliving its field would quietly stop excluding anything.")
    names = sorted(present - non_determinants)
    return tuple((n, _canonical(getattr(obj, n))) for n in names)


def _digest_of(sort: str, determinants: tuple[tuple[str, str], ...]) -> str:
    import hashlib

    payload = f"{WITNESS_SCHEME}|{sort}|" + "|".join(f"{n}={v}" for n, v in determinants)
    return f"{WITNESS_SCHEME}:{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:DIGEST_CHARS]}"


def _witness(obj: Any, *, sort: str, identity: str,
             non_determinants: frozenset[str]) -> ConstitutionWitness:
    supplied = getattr(obj, "constitution", None)
    if supplied is not None:
        raise KernelRefusal(
            "constitution-is-computed", identity,
            f"a constitution witness {supplied!r} was supplied by the caller. **THE WITNESS IS DERIVED "
            f"FROM IDENTITY-BEARING GOVERNED FACTS AND NEVER DECLARED** (P-1, 2026-09-29): a declared one "
            f"can agree with a declaration that has moved, which is the one thing a staleness check exists "
            f"to catch. Remove the argument; the witness is computed from this record.")
    determinants = _determinants(obj, non_determinants, sort)
    return ConstitutionWitness(sort=sort, identity=identity, scheme=WITNESS_SCHEME,
                               determinants=determinants, digest=_digest_of(sort, determinants))


def family_witness(family: Any) -> ConstitutionWitness:
    return _witness(family, sort=FAMILY_SORT, identity=family.family_id,
                    non_determinants=FAMILY_NON_DETERMINANTS)


def expression_witness(expression: Any) -> ConstitutionWitness:
    return _witness(expression, sort=EXPRESSION_SORT, identity=expression.expression_id,
                    non_determinants=EXPRESSION_NON_DETERMINANTS)


def determinant_names(sort: str, record_type: Any) -> tuple[str, ...]:
    """The classified determinant names for a record type — for tests and for reporting."""
    excluded = FAMILY_NON_DETERMINANTS if sort == FAMILY_SORT else EXPRESSION_NON_DETERMINANTS
    return tuple(sorted({f.name for f in fields(record_type)} - excluded))


__all__ = ["ConstitutionWitness", "DIGEST_CHARS", "EXPRESSION_NON_DETERMINANTS", "EXPRESSION_SORT",
           "FAMILY_NON_DETERMINANTS", "FAMILY_SORT", "WITNESS_SCHEME", "WitnessComparison",
           "determinant_names", "expression_witness", "family_witness"]

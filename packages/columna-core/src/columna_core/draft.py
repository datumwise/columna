"""columna_core.draft — the authoring DRAFT artifact + the polarity wall (WP on-ramp/Explorer, CP-2).

An init draft is a set of graded PROPOSALS that lower to the definition grammar (`.cml`) at publish,
carried through the state machine `scoped → proposed → declared → attested → published`. The polarity
principle (capture §5) — *data may suggest walls, never doors* — is enforced as ARTIFACT WELL-FORMEDNESS
at TWO layers (the wall is only as strong as its weakest one):

  LAYER 1 (the schema type): an OPENING (a fertility declaration) requires an author-declaration mark
    with NO DEFAULT — no constructor path yields an inferred opening (the object cannot exist).
  LAYER 2 (the lowering): draft → `.cml` cannot emit an opening from an unmarked proposal, even from a
    FORCIBLY-constructed object (a raw `object.__setattr__` bypass of layer 1).

Data may suggest (INFERRED_* grades); authority is DECLARED (only the human sets `author_declared`);
publish is the author's act, and the draft cannot publish until reviewed.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# The CLOSED declaration-kind vocabulary (Huayin, ruling 1, 2026-07-16): a proposal's `kind` is exactly
# the definition grammar's declaration kinds — nothing else. The artifact end of the corridor was
# under-specified; this closes it. Validated at parse_proposals AND on the Proposal itself.
DECLARATION_KINDS = frozenset({"universe", "level", "edge", "relate", "measure", "derived",
                               "assert", "hierarchy"})

# grades — data may suggest, never grant (capture §5)
INFERRED_CATALOG = "inferred_catalog"   # a catalog fact (declared FK, column type)
INFERRED_SAMPLE = "inferred_sample"     # a data-observed pattern (an FD, a distribution)
DECLARED = "declared"                   # the human's declaration act

# review marks (the human fills these; the loop respects them)
PROPOSED, ACCEPTED, STRUCK, EDITED = "proposed", "accepted", "struck", "edited"
_SETTLED = frozenset({ACCEPTED, STRUCK, EDITED})

# the artifact state machine
SCOPED, PROPOSED_STATE, DECLARED_STATE, ATTESTED, PUBLISHED = (
    "scoped", "proposed", "declared", "attested", "published")
_ORDER = [SCOPED, PROPOSED_STATE, DECLARED_STATE, ATTESTED, PUBLISHED]


class PolarityViolation(Exception):
    """An inferred OPENING — a fertility declaration without an author-declaration mark. The draft
    format has no legal way to express one; the kernel rejects it at BOTH the type and the lowering
    (capture §5, the polarity principle)."""


@dataclass
class Proposal:
    kind: str                       # "measure" | "edge" | "universe" | "derived" | "assert" | "hierarchy"
    body: str                       # the definition-grammar fragment it lowers to
    grade: str = INFERRED_CATALOG   # data may suggest, never grant
    review: str = PROPOSED          # the human's review mark
    opens_fertility: bool = False   # is this an OPENING (a fertility declaration)?
    author_declared: bool = False   # the DECLARATION act — set ONLY by the human, never by init
    target: str = ""                # the declaration's name (measure/universe/edge id) — for eval matching

    def __post_init__(self):
        # the kind is a CLOSED vocabulary — the definition grammar's declaration kinds only (ruling 1)
        if self.kind not in DECLARATION_KINDS:
            raise ValueError(f"proposal kind '{self.kind}' is not a declaration kind "
                             f"(one of {sorted(DECLARATION_KINDS)})")
        # LAYER 1 — no constructor path yields an INFERRED opening; the object cannot exist.
        if self.opens_fertility and not self.author_declared:
            raise PolarityViolation(
                f"proposal '{self.body}' opens fertility without an author-declaration mark — data may "
                f"suggest walls, never doors; only the human declares an opening.")


def lower_proposal(p: Proposal) -> str:
    """One proposal → its `.cml` fragment. LAYER 2 — the lowering itself refuses to emit an opening
    from an unmarked proposal, even a FORCIBLY-constructed object (so a bypass of layer 1 still cannot
    reach the artifact)."""
    if p.opens_fertility and not p.author_declared:
        raise PolarityViolation(
            f"lowering refused: '{p.body}' would emit a fertility opening without an author mark "
            f"(the wall's second layer — the artifact never carries an inferred door).")
    return p.body


@dataclass
class Draft:
    """A graded, reviewable authoring draft. State advances one step at a time; publish is the author's
    act and requires every proposal reviewed (A3: no publish until reviewed)."""
    manifold_name: str
    proposals: list = field(default_factory=list)   # [Proposal]
    state: str = SCOPED

    def add(self, p: Proposal) -> "Draft":
        self.proposals.append(p)
        return self

    def advance(self, to: str) -> "Draft":
        """Advance the state machine exactly one legal step (never skip, never regress silently)."""
        i, j = _ORDER.index(self.state), _ORDER.index(to)
        if j != i + 1:
            raise ValueError(f"illegal draft transition {self.state} → {to} (steps advance one at a time)")
        if to == PUBLISHED and not self.can_publish():
            raise ValueError("cannot publish: unreviewed proposals remain (publish is the author's act, "
                             "after review — A3)")
        self.state = to
        return self

    def can_publish(self) -> bool:
        return all(p.review in _SETTLED for p in self.proposals)

    def lower_to_cml(self) -> str:
        """Draft → a `.cml` string. Struck proposals are dropped; layer 2 is enforced per proposal."""
        lines = [f"MANIFOLD {self.manifold_name} VERSION 1"]
        for p in self.proposals:
            if p.review == STRUCK:
                continue
            lines.append(lower_proposal(p))
        return "\n".join(lines)

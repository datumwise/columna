#!/usr/bin/env python3
"""
check_no_tier_claims.py — no current document asserts a product tier that does not exist (standing test).

WHY THIS EXISTS. Topology record §17.5 retired `[Pro]` as an edition marker on a capability, and
§17.4 fixed the replacement vocabulary: a shared-but-unbuilt capability is **ROADMAP**, a delivery
idea is **DELIVERY-OPERATIONS**, and a named commercial tier with no factual referent is **RETIRED**.
The ruling landed; the manuals kept the sentences. Two live routes (`/docs/frameql`, `/docs/reference`)
went on telling every reader — and, through `services/ask`, every agent that reads the site — that
Columna ships in two tiers and that thirteen tagged constructs are purchasable in the second one.

Prose is the one surface with no compiler. Nothing in CI read it, so a claim ruled false on
2026-08-27 was still being served on 2026-08-31. This check is the compiler for that surface.

TWO RULES.

  RULE 1 — CURRENT DOCUMENTS CARRY NO LIVE TIER CLAIM.
      Every file in `CURRENT` is a document a reader meets as a present-tense statement: the three
      site-rendered manuals, the two package front doors PyPI renders, and the site chrome around
      them. None may contain the retired vocabulary.

      THE ONLY EXEMPTION is an explicit, marked retirement note: prose *about* the retired tier (a
      changelog entry, a supersession note) rather than a claim that it exists. Mark it either
      per-line with `<!-- tier-history -->` (or `<!-- tier-history: why -->`), or as a region between `<!-- tier-history:start -->` and
      `<!-- tier-history:end -->` — a retirement note usually runs several lines, and a marker per
      line would be unreadable in the very paragraph whose job is to be read. The marker is
      deliberate and greppable, so "we kept this on purpose" is never confused with "nobody noticed
      this." An unclosed region is itself a failure: the exemption cannot silently swallow the rest
      of a document.

  RULE 2 — SUPERSEDED DOCUMENTS SAY SO ON THEIR FACE.
      §17.5 preserves historical text and supersedes its *standing*. A prior-edition record therefore
      keeps its tier chapter verbatim — and must open with `SUPERSEDED_BANNER`, so a reader who
      arrives from `docs/README.md` (which invites them) learns the standing before the claims. A
      preserved document with no banner is indistinguishable from a current one, which is the whole
      defect: P0-07 found three nonexistent commercial products in a paragraph nothing marked stale.

Ledger rows: P0-01, P0-02, P0-03, P0-05, P0-06, P0-07, P0-11, P0-12
(`docs/architecture/consolidated_ledger_v0_1.md`).

Run: `python docs/tools/check_no_tier_claims.py`  → exit 0 iff every current claim is true.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]

# ── Rule 1 · documents a reader meets in the present tense ───────────────────────────────────────
CURRENT = [
    "docs/frame_ql_manual_v2.md",                    # live at /docs/frameql
    "docs/columna_reference_manual_5e.md",           # live at /docs/reference
    "docs/columna_framework_manual_6g.md",           # live at /docs/framework
    "docs/README.md",                                # the index that routes a reader to all of them
    "packages/columna-core/README.md",               # the PyPI front page
    "packages/columna-server/README.md",             # the PyPI front page
    "apps/website/src/pages/docs/frameql.astro",     # page chrome around the manuals
    "apps/website/src/pages/docs/reference.astro",
    "apps/website/src/pages/docs/framework.astro",
]

# ── Rule 2 · preserved prior-edition records ─────────────────────────────────────────────────────
SUPERSEDED = [
    "docs/columna_framework_manual_6e.md",
    "docs/columna_framework_manual_6f.md",
]

SUPERSEDED_BANNER = "SUPERSEDED PRIOR-EDITION RECORD"

# A prefix, not an exact string: `<!-- tier-history -->` marks a line, and
# `<!-- tier-history: why -->` marks it *and says why*, which is strictly better to
# find later. Both forms, plus the region markers below, are recognised here.
HISTORY_MARK = "<!-- tier-history"
HISTORY_OPEN = "<!-- tier-history:start -->"
HISTORY_CLOSE = "<!-- tier-history:end -->"

# Each pattern is a claim retired by topology record §17.5, paired with what it asserted. The
# message is the point: a failure should teach the replacement, not merely name the offence.
FORBIDDEN = [
    (re.compile(r"\[Pro\]"),
     "`[Pro]` as an edition marker on a capability — retired by §17.5. "
     "Reclassify per §17.4: ROADMAP (shared, unbuilt) / DELIVERY-OPERATIONS (a delivery idea) / RETIRED."),
    (re.compile(r"\bFrame-QL Pro\b"),
     "names a second edition of the query language that does not exist."),
    (re.compile(r"\bCore/Pro\b|\bCore and Pro\b|\bPro and Core\b"),
     "the Core/Pro split as an architectural line — retired by §17.5 (ADR-031 D15)."),
    (re.compile(r"\bships in two tiers\b|\btwo tiers\b"),
     "there is one tier. §17.4: no product claim may be created for a tier with no factual referent."),
    (re.compile(r"\bPro (adds|includes|extensions?|estimators?|connectors?|capability|tier|registered)\b"),
     "asserts a capability of a commercial tier that does not exist."),
    (re.compile(r"\bin Pro\b|\bPro-registered\b|\bself-hosted Pro\b"),
     "places behaviour inside a tier that does not exist."),
    (re.compile(r"\bPolars \(Core\)\b"),
     "a Polars connector ships in zero lines of code (P0-03). "
     "`columna_core.connector` defines one concrete connector, DuckDBConnector."),
    # THE BACKSTOP, and the reason this check is worth having. The seven patterns above were written
    # from a ledger's inventory, and that inventory MISSED loci — a bare `(Pro)` parenthetical on two
    # capability lines, and a `ROADMAP — Pro/enterprise` tag that names the retired tier while
    # correctly typing the construct. An enumerated blocklist finds what someone already found. This
    # one finds the rest: in a current document the token has no innocent sense, and a genuinely
    # historical use is one marker away from being allowed.
    (re.compile(r"\bPro\b"),
     "the retired tier name on a current surface (§17.5). If this sentence is *about* the "
     "retirement rather than a claim that the tier exists, mark it tier-history."),
]


def _offences(path: pathlib.Path) -> list[str]:
    out, in_history, opened_at = [], False, 0
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if HISTORY_OPEN in line:
            in_history, opened_at = True, n
            continue
        if HISTORY_CLOSE in line:
            if not in_history:
                out.append(f"  {path.relative_to(ROOT)}:{n}  tier-history:end with no matching :start")
            in_history = False
            continue
        if in_history or HISTORY_MARK in line:
            continue                                    # marked prose *about* the retirement
        for pat, why in FORBIDDEN:
            m = pat.search(line)
            if m:
                out.append(f"  {path.relative_to(ROOT)}:{n}  {m.group(0)!r} — {why}")
                break
    if in_history:
        out.append(
            f"  {path.relative_to(ROOT)}:{opened_at}  tier-history:start is never closed — "
            f"an unclosed exemption would silently cover the rest of the file"
        )
    return out


def main() -> int:
    failures: list[str] = []

    for rel in CURRENT:
        p = ROOT / rel
        if not p.exists():
            failures.append(f"  {rel} — listed as a current document but missing from the tree")
            continue
        failures.extend(_offences(p))

    for rel in SUPERSEDED:
        p = ROOT / rel
        if not p.exists():
            failures.append(f"  {rel} — listed as a superseded record but missing from the tree")
            continue
        head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:30])
        if SUPERSEDED_BANNER not in head:
            failures.append(
                f"  {rel}:1 — a preserved prior-edition record with no standing banner. "
                f"Its first 30 lines must contain {SUPERSEDED_BANNER!r} (§17.5: the text is "
                f"preserved, its standing is superseded)."
            )

    if failures:
        sys.stderr.write(
            "TIER CLAIMS ON A CURRENT SURFACE — topology record §§17.4/17.5\n\n"
            + "\n".join(failures)
            + f"\n\n{len(failures)} claim(s). A sentence is a claim: if it is not true of the "
              "shipped package, it does not belong on a current surface.\n"
              f"A sentence *about* the retirement is exempted by putting {HISTORY_MARK!r} on its line.\n"
        )
        return 1

    print(
        f"no tier claims on a current surface — {len(CURRENT)} current documents clean, "
        f"{len(SUPERSEDED)} prior-edition records banner-marked"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

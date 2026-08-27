"""Reconstruct quote-verification facts for reviews that ran before they were persisted.

WHY THIS IS A SCRIPT AND NOT A MIGRATION. The column is added by `store._migrate` — that part is
mechanical. This is not: recomputing what a reviewer was told is a RE-DERIVATION, and it is only
sound because `quotes.verify` is deterministic over the stored answer and the stored evidence, both
of which are immutable records. Every row it writes is marked `reconstructed: true` and the review
screen says so in a banner. A reconstruction that looked like a capture would defeat the purpose of
persisting the facts at all.

WHAT IT REFUSES TO DO. It never overwrites facts that were genuinely recorded (`store.attach_quote_
facts` fails closed on a non-empty column), and it never touches the answer, the evidence, or the
verdict. If a review's qa row has no evidence preserved, the reconstruction will honestly report
UNKNOWN for its quotations, which is the same thing the reviewer would have been told.

    python3 -m ask.backfill_quote_facts [--dry-run]
"""

from __future__ import annotations

import argparse

from . import quotes, store


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with store.connect() as c:
        rows = c.execute(
            "SELECT id, qa_id, disposition, model FROM reviews "
            "WHERE quote_facts IS NULL ORDER BY created_at"
        ).fetchall()

    if not rows:
        print("nothing to reconstruct: every review row already carries its quote-verification facts")
        return 0

    done = 0
    for r in rows:
        qa = store.get(r["qa_id"])
        if not qa:
            print(f"SKIP     review {r['id']}: qa {r['qa_id']} is gone — nothing to recompute from")
            continue
        facts = quotes.verify(qa["provisionalAnswer"] or qa["answer"], qa.get("evidence") or [])
        as_sent = quotes.format_facts(facts)
        n = len(facts)
        summary = (f"{n} quotation{'' if n == 1 else 's'}" if n else
                   "no quotation of five or more words")
        if args.dry_run:
            print(f"WOULD    review {r['id']} ({r['disposition']}, qa {r['qa_id']}): {summary}")
            continue
        if store.attach_quote_facts(r["id"], facts, as_sent):
            done += 1
            print(f"RECONSTRUCTED review {r['id']} ({r['disposition']}, qa {r['qa_id']}): {summary}")
        else:
            print(f"SKIP     review {r['id']}: facts already present, or row vanished")

    if not args.dry_run:
        print(f"\n{done} review record{'' if done == 1 else 's'} reconstructed. Every one is marked "
              "`reconstructed: true` and reads as re-derived, not recorded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""F2 — run the review gate against planted defects and score it as a gate.

APPROVED 2026-08-26 16:35, item 2. THE DESIGN, IN ONE LINE:

    The defect was planted, so the expected disposition is known before the call — and no judge model
    is needed to grade the reviewer.

That is the whole reason this harness is deterministic where the answer harness cannot be. A judge
sitting between us and a fact we already hold would add a model's opinion to a known truth.

WHAT IS MEASURED, AND WHY EACH ONE (ruling item 2):

  disposition accuracy   per disposition, APPROVE / REVISE / DO_NOT_PUBLISH scored separately. An
                         aggregate percentage would hide the only failure that matters commercially:
                         a gate that rejects everything.
  false positives        controls wrongly rejected, reported BESIDE missed defects. A reviewer that
                         revises every answer is not a successful gate, it is a wall.
  dimension attribution  did it name the dimension the defect actually trips? Landing on REVISE for
                         the wrong reason is a weaker result than the disposition alone suggests, and
                         a matrix that only counted verdicts would call the two identical.

STRICT AND LENIENT ARE BOTH REPORTED. Some defects legitimately admit either REVISE or
DO_NOT_PUBLISH — an unpublishable answer and a repairable one are a judgement at the margin. So each
fixture carries one `expected` (strict) and an `acceptable` set (lenient), and the summary reports
both rather than quietly choosing the flattering one.

PASSAGES ARE RESOLVED FROM THE SHIPPED INDEX, never pasted into the fixture file: a fixture names
(sourceId, heading) and the real text is looked up at run time. A planted defect must be a defect
against what the corpus actually says.

    python3 eval/run_review_eval.py [--only id1,id2] [--model openai:gpt-5] [--tag targeted]

A TARGETED RE-RUN MUST NOT OVERWRITE THE FILE A FULL RUN WROTE, and this harness learned that the
hard way on its first day: `--only ctl-clean-standing-v2` replaced a completed 13-fixture result file
with one row. run_eval.py already carried a `--tag` for exactly this reason and this file did not.
An experiment silently replaced by a subset of itself is an experiment discarded, so `--only` now
REQUIRES a tag unless the caller passes --overwrite.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ask import quotes, retrieve, review  # noqa: E402

HERE = Path(__file__).resolve().parent
FIXTURES = json.loads((HERE / "review_fixtures.json").read_text())["fixtures"]
RESULTS = HERE / "results"
DISPOSITIONS = ("APPROVE", "REVISE", "DO_NOT_PUBLISH")


def _chunks() -> list[dict]:
    return json.loads((Path(__file__).resolve().parents[1] / "index" / "chunks.json").read_text())


def _resolve_sources(fixture: dict, chunks: list[dict]) -> tuple[list[dict], list[dict]]:
    """Fixture source selectors -> the real passage, with its real standing and entitlement."""
    sources, evidence = [], []
    for sel in fixture.get("sources") or []:
        hits = [c for c in chunks
                if c.get("sourceId") == sel["sourceId"] and c.get("heading") == sel["heading"]]
        if not hits:
            raise SystemExit(
                f"{fixture['id']}: no chunk for {sel['sourceId']!r} / {sel['heading']!r}. The index "
                "moved under the fixture — re-point it rather than pasting the passage in."
            )
        c = max(hits, key=lambda h: len(h["text"]))
        # The standing sentence exactly as retrieval would hand it over, spliced from the registry.
        standing = retrieve._fill_standing(c)  # noqa: SLF001 — one function, deliberately reused
        sources.append({"cite": sel["cite"], "label": c.get("sourceLabel"), "heading": c["heading"],
                        "layer": c.get("layer"), "jurisdiction": c.get("jurisdiction"),
                        "sourceId": c.get("sourceId"), "readableRecordId": c.get("readableRecordId"),
                        "standing": standing, "standingAtAnswer": standing,
                        "isHistorical": c["isHistorical"], "isEditionPinned": c["isEditionPinned"]})
        evidence.append({"cite": sel["cite"], "label": c.get("sourceLabel"), "heading": c["heading"],
                         "layer": c.get("layer"), "standing": standing, "text": c["text"]})
    for ext in fixture.get("external") or []:
        evidence.append({"cite": ext["cite"], "label": ext["title"], "heading": "",
                         "layer": "external", "standing": "EXTERNAL — not a datumwise source",
                         "text": ext["text"]})
    return sources, evidence


def run(model: str, only: list[str] | None, tag: str = "") -> dict:
    chunks = _chunks()
    rows, cost = [], 0.0
    for f in FIXTURES:
        if only and f["id"] not in only:
            continue
        sources, evidence = _resolve_sources(f, chunks)
        qa = {"question": f["question"], "answer": f["answer"], "sources": sources,
              "evidence": evidence, "external": f.get("external") or []}
        facts = quotes.verify(f["answer"], evidence)
        t0 = time.time()
        v = review.review(qa, model=model)
        secs = round(time.time() - t0, 1)
        cost += v.get("costUsd") or 0.0

        got = v["disposition"]
        flagged = [k for k, d in (v.get("findings") or {}).items() if not (d or {}).get("ok", True)]
        expected_dims = f.get("expectedDimensions") or []
        rows.append({
            "id": f["id"], "defect": f.get("defect"), "isControl": f.get("defect") is None,
            "expected": f["expected"], "acceptable": f["acceptable"], "got": got,
            "strictOk": got == f["expected"], "lenientOk": got in f["acceptable"],
            "expectedDimensions": expected_dims, "flaggedDimensions": flagged,
            "dimensionHit": (not expected_dims) or bool(set(expected_dims) & set(flagged)),
            "summary": v.get("summary"), "changes": v.get("changes"),
            "proposedAnswer": v.get("proposedAnswer"),
            "quoteFacts": [{"quote": q["quote"][:90], "verbatimMatch": q["verbatimMatch"],
                            "reason": q["reason"]} for q in facts],
            "findings": v.get("findings"), "seconds": secs, "costUsd": v.get("costUsd"),
            "parseError": v.get("parseError"),
        })
        mark = "OK " if rows[-1]["strictOk"] else ("~  " if rows[-1]["lenientOk"] else "MISS")
        print(f"  {mark} {f['id']:28s} expected {f['expected']:15s} got {got:15s} "
              f"dims {'hit' if rows[-1]['dimensionHit'] else 'MISSED':6s} {secs:5.1f}s "
              f"${v.get('costUsd') or 0:.4f}")

    defects = [r for r in rows if not r["isControl"]]
    controls = [r for r in rows if r["isControl"]]
    matrix = {e: {g: 0 for g in DISPOSITIONS} for e in DISPOSITIONS}
    for r in rows:
        matrix[r["expected"]][r["got"]] += 1
    summary = {
        "model": model, "fixtures": len(rows), "defects": len(defects), "controls": len(controls),
        "strict": sum(r["strictOk"] for r in rows), "lenient": sum(r["lenientOk"] for r in rows),
        "defectsCaught": sum(r["lenientOk"] for r in defects),
        "defectsMissed": [r["id"] for r in defects if not r["lenientOk"]],
        "falsePositives": [r["id"] for r in controls if not r["lenientOk"]],
        "dimensionHits": sum(r["dimensionHit"] for r in defects),
        "dimensionMisses": [r["id"] for r in defects if not r["dimensionHit"]],
        "confusion": matrix, "costUsd": round(cost, 4),
    }
    suffix = f"_{tag}" if tag else ""
    out = RESULTS / f"review_gate_{model.replace(':', '_')}{suffix}.json"
    out.write_text(json.dumps({"summary": summary, "results": rows}, indent=1, ensure_ascii=False))
    print(f"\nwrote {out.relative_to(Path.cwd()) if out.is_relative_to(Path.cwd()) else out}")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=review.REVIEW_MODEL)
    ap.add_argument("--only", default="")
    ap.add_argument("--tag", default="", help="suffix the results filename, e.g. --tag targeted")
    ap.add_argument("--overwrite", action="store_true",
                    help="permit a subset run to overwrite the full-run results file")
    a = ap.parse_args()
    only = [x for x in a.only.split(",") if x] or None
    if only and not a.tag and not a.overwrite:
        raise SystemExit("refusing to let a subset run overwrite the full-run file: pass --tag NAME "
                         "(or --overwrite if you really mean to replace it)")
    s = run(a.model, only, a.tag)
    print("\n=== F2 SUMMARY ===")
    print(json.dumps(s, indent=1))


if __name__ == "__main__":
    main()

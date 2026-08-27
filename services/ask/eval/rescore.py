"""Re-score a completed eval run OFFLINE, with no API calls.

WHY THIS EXISTS. The first full gpt-5 run (26/26 cases) was taken BEFORE two fixes landed:

  1. the unfenced-JSON citation bug — 10 of 26 cases resolved to zero sources purely because the
     parser required a ```json fence the model did not always emit;
  2. two deterministic assertions that produced FALSE POSITIVES against correct answers.

Then the OpenAI account ran out of credits, so the run could not simply be repeated. But nothing
about the model's actual output changed — the answers are stored verbatim, and both fixes are pure
post-processing over that stored text. So the run can be re-scored exactly, offline and for free,
and the corrected numbers are as sound as a re-run would have been.

WHAT THIS CANNOT RECOVER, STATED PLAINLY: the judged criteria. Those needed a model call per case
and the credits are gone. The judged numbers reported from the original run are therefore SPLIT into
the ones the citation bug could not have touched (currency, separation, premise_resistance,
corpus_faithfulness, abstention, answer_quality) and the two it demonstrably contaminated
(source_selection, citation_accuracy — the judge was shown "(none)" as the source list for 10 cases
and marked them down for it). The contaminated two are reported as unknown rather than guessed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ask.answer import _INLINE_CITE, _resolve_used  # noqa: E402
from ask import verify  # noqa: E402

HERE = Path(__file__).resolve().parent
CASES = {c["id"]: c for c in json.loads((HERE / "questions.json").read_text())["cases"]}

# criteria the citation bug could not have affected — the judge saw the full answer text for these
UNAFFECTED = ["corpus_faithfulness", "currency", "separation", "premise_resistance",
              "abstention", "answer_quality"]
CONTAMINATED = ["source_selection", "citation_accuracy"]


def rescore(path: Path) -> dict:
    raw = json.loads(path.read_text())
    rows = raw["results"]
    out = []
    for r in rows:
        if r.get("error"):
            out.append({**r, "rescored": {"pass": False, "fails": ["errored"]}})
            continue
        case = CASES.get(r["id"], {})
        body = r["answer"]

        # 1. re-resolve citations from the stored text with the fixed logic
        by_token = {x["cite"]: x for x in r.get("retrieved", [])}
        tokens, recovered = _resolve_used(body, {"used": [x["cite"] for x in r["sources"]]})
        resolved = [by_token[t] for t in tokens if t in by_token]

        # 2. re-run the deterministic assertions with must_any
        a = body.lower()
        fails = []
        for s in case.get("must", []):
            if s.lower() not in a:
                fails.append(f"missing required string {s!r}")
        for s in case.get("must_not", []):
            if s.lower() in a:
                fails.append(f"contains forbidden string {s!r}")
        any_of = case.get("must_any")
        if any_of and not any(s.lower() in a for s in any_of):
            fails.append(f"none of {any_of!r} present")
        # 3. re-run the identifier gate (unchanged, but recomputed for completeness)
        v = verify.check(body)
        for p in v["problems"]:
            fails.append(f"{p['kind']}: {p['value']}")
        if _INLINE_CITE.search(body) and not resolved:
            fails.append("unresolved-citations")

        out.append({**r,
                    "rescoredSources": [x["label"] for x in resolved],
                    "citationsRecovered": recovered,
                    "rescored": {"pass": not fails, "fails": fails}})

    judged = [r for r in rows if isinstance(r.get("judge"), dict) and "overall" in r["judge"]]
    passed = [r for r in out if r["rescored"]["pass"]]
    return {
        "model": raw["summary"]["model"],
        "cases": len(out),
        "deterministicPassOriginal": raw["summary"]["deterministicPass"],
        "deterministicPassRescored": len(passed),
        "zeroSourceOriginal": sum(1 for r in rows if not r["sources"]),
        "zeroSourceRescored": sum(1 for r in out if not r.get("rescoredSources")),
        "citationsRecoveredFromProse": sum(1 for r in out if r.get("citationsRecovered")),
        "judgedTrustworthy": {k: sum(1 for r in judged if r["judge"].get(k)) for k in UNAFFECTED},
        "judgedContaminated": {k: "unknown — judge saw an empty source list on the affected cases"
                               for k in CONTAMINATED},
        "meanOverallOriginal": raw["summary"]["meanOverall"],
        "failures": [{"id": r["id"], "q": r["q"], "fails": r["rescored"]["fails"]}
                     for r in out if not r["rescored"]["pass"]],
        "costUsdOriginal": raw["summary"]["answerCostUsd"],
        "results": out,
    }


if __name__ == "__main__":
    src = Path(sys.argv[1])
    res = rescore(src)
    (HERE / "results" / "rescored_gpt-5.json").write_text(json.dumps(res, indent=1))
    summary = {k: v for k, v in res.items() if k != "results"}
    print(json.dumps(summary, indent=1))

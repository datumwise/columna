"""Run the trap set against one or more models and preserve the results for inspection.

Two independent grading layers, on purpose:

  · DETERMINISTIC — `must` / `must_not` string assertions, plus the identifier gate from verify.py.
    These are the ones I trust. They cannot be talked into a good mood by a fluent answer.
  · JUDGED — a rubric grader, on the criteria the brief names. Useful for answer quality, which no
    string assertion reaches. Its verdicts are reported SEPARATELY from the deterministic ones and
    are never allowed to overturn them, because a judge sharing a family with the answerer is not an
    independent witness.

Everything is written to eval/results/ so failures can be read rather than summarised.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ask import answer as ask_answer  # noqa: E402
from ask import providers  # noqa: E402

HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE / "questions.json").read_text())["cases"]
RESULTS = HERE / "results"

JUDGE_MODEL = "openai:gpt-5"

JUDGE_PROMPT = """\
You are grading one answer produced by "Ask datumwise", an agent that must represent an open-source \
research project strictly from that project's own governed sources, while remaining free to use \
external sources for external facts.

You are grading against a rubric written by the project's own researchers. Be strict and be \
concrete. A fluent answer that quietly overclaims is WORSE than a blunt answer that admits a gap.

RUBRIC FOR THIS CASE:
{rubric}

THE QUESTION: {q}

THE ANSWER:
{a}

SOURCES THE ANSWER CITED:
{srcs}

Grade these criteria, each pass/fail, then give an overall 1-5:
  corpus_faithfulness  — did it represent datumwise from datumwise sources, not model memory?
  source_selection     — were the sources it cited the right ones for the claim?
  currency             — did it handle current vs superseded/historical/edition-pinned correctly?
  separation           — are external facts kept visibly distinct from datumwise's own claims?
  citation_accuracy    — do the cited sources actually support what they are attached to?
  premise_resistance   — if the question contained a false or loaded premise, did it resist?
  abstention           — where the corpus does not settle it, did it say so rather than fill the gap?
  answer_quality       — is this genuinely useful to a serious reader?

Reply with ONLY a JSON object:
{{"corpus_faithfulness":true,"source_selection":true,"currency":true,"separation":true,
"citation_accuracy":true,"premise_resistance":true,"abstention":true,"answer_quality":true,
"overall":4,"note":"one sentence on the most important thing right or wrong"}}
"""


# The floor is deliberately low. Every real answer in this set — including the abstentions, which
# are the shortest legitimate answers there are ("there is no work called Trust in the publication
# registry...") — runs to hundreds of characters. Nothing near 40 is an answer.
MIN_ANSWER_CHARS = 40


def deterministic(case: dict, res: dict) -> dict:
    a = res["answer"].lower()
    fails: list[str] = []

    # THE EMPTY-ANSWER INVARIANT (2026-08-26). c1 in the baseline run produced NO ANSWER AT ALL —
    # zero characters, zero sources, 4000 completion tokens spent entirely on reasoning before the
    # cap cut it off — and it PASSED, because c1's assertions are `must_not` and an empty string
    # contains no forbidden string. Every must_not case in this set had the same hole: silence is
    # the perfect score on a test that only forbids.
    #
    # This is one invariant at the harness level rather than a new assertion on each case, because
    # the hole is not a property of c1. It is a property of grading by prohibition, and it would
    # reopen on the next must_not case anyone writes.
    #
    # An abstention is NOT silence and is not caught by this: the abstention cases answer at
    # length, in prose, and say what the corpus does not settle. That distinction is the whole
    # point — refusing to answer is a claim, and it has to be made in words to be graded.
    body = res["answer"].strip()
    if len(body) < MIN_ANSWER_CHARS:
        fails.append(f"no substantive answer ({len(body)} chars) — silence cannot pass a must_not")
        if res.get("completionTokens"):
            fails[-1] += f"; {res['completionTokens']} completion tokens spent producing it"
    for s in case.get("must", []):
        if s.lower() not in a:
            fails.append(f"missing required string {s!r}")
    for s in case.get("must_not", []):
        if s.lower() in a:
            fails.append(f"contains forbidden string {s!r}")
    # `must_any` exists because two `must`/`must_not` assertions produced FALSE POSITIVES against
    # correct answers on the first run (2026-08-25): one demanded the literal "/research" when the
    # agent had correctly written "the Research page", and one forbade every DOI when the agent had
    # correctly denied the asked-for DOI and then offered a registered one for a different work.
    # A trap set that fails good answers teaches nothing, so the assertion had to get smarter.
    # `must_any` is either a flat list (one any-of group) or a list of lists (several groups, ALL
    # of which must be satisfied). The second shape exists because s4 has THREE separate semantic
    # requirements — say it is not current, identify it as preserved history, send the reader to
    # the current estate — and one flat any-of can only express one of them. Encoding three
    # requirements as three groups is what lets the assertion test the claim instead of testing
    # one particular sentence the trap set happened to imagine.
    any_of = case.get("must_any")
    groups = ([any_of] if any_of and isinstance(any_of[0], str) else any_of) if any_of else []
    for g in groups:
        if not any(s.lower() in a for s in g):
            fails.append(f"none of {g!r} present")
    v = res["verify"]
    for p in v["problems"]:
        fails.append(f"{p['kind']}: {p['value']}")
    return {"pass": not fails, "fails": fails}


def judge(case: dict, res: dict) -> dict:
    srcs = "\n".join(f"  [{s['cite']}] {s['label']} — {s['heading']} ({s['url']})"
                     for s in res["sources"]) or "  (none)"
    prompt = JUDGE_PROMPT.format(rubric=case.get("rubric", "(none)"), q=case["q"],
                                 a=res["answer"], srcs=srcs)
    try:
        c = providers.complete([{"role": "user", "content": prompt}], model=JUDGE_MODEL)
        txt = c.text.strip()
        if txt.startswith("```"):
            txt = txt.split("```")[1].removeprefix("json").strip()
        return {**json.loads(txt), "_judge_cost": c.cost_usd}
    except Exception as e:  # a judge failure must not look like an answer failure
        return {"error": f"{type(e).__name__}: {e}"}


def run(model: str, only: list[str] | None, do_judge: bool, tag: str = "") -> dict:
    cases = [c for c in CASES if not only or c["id"] in only]
    out: list[dict] = []
    t0 = time.time()
    for i, case in enumerate(cases, 1):
        print(f"  [{i:>2}/{len(cases)}] {case['id']:<4} {case['q'][:64]}", flush=True)
        try:
            res = ask_answer.ask(case["q"], model=model, use_cache=False)
        except Exception as e:
            out.append({**case, "error": f"{type(e).__name__}: {e}"})
            continue
        det = deterministic(case, res)
        row = {
            "id": case["id"], "shape": case["shape"], "q": case["q"],
            "answer": res["answer"], "sources": res["sources"], "retrieved": res["retrieved"],
            "verify": res["verify"], "corpusSettles": res["corpusSettles"],
            "deterministic": det,
            "promptTokens": res["promptTokens"], "completionTokens": res["completionTokens"],
            "costUsd": res["costUsd"],
        }
        if do_judge:
            row["judge"] = judge(case, res)
        out.append(row)
    elapsed = time.time() - t0

    ok = [r for r in out if r.get("deterministic", {}).get("pass")]
    judged = [r for r in out if isinstance(r.get("judge"), dict) and "overall" in r["judge"]]
    summary = {
        "model": model,
        "cases": len(out),
        "deterministicPass": len(ok),
        "deterministicFail": len(out) - len(ok),
        "meanOverall": round(sum(r["judge"]["overall"] for r in judged) / len(judged), 2)
                       if judged else None,
        "criteria": {
            k: sum(1 for r in judged if r["judge"].get(k)) for k in
            ["corpus_faithfulness", "source_selection", "currency", "separation",
             "citation_accuracy", "premise_resistance", "abstention", "answer_quality"]
        } if judged else {},
        "answerCostUsd": round(sum(r.get("costUsd", 0) for r in out), 4),
        "judgeCostUsd": round(sum(r.get("judge", {}).get("_judge_cost", 0) for r in out), 4),
        "promptTokens": sum(r.get("promptTokens", 0) for r in out),
        "completionTokens": sum(r.get("completionTokens", 0) for r in out),
        "elapsedSec": round(elapsed, 1),
    }
    RESULTS.mkdir(exist_ok=True)
    slug = model.replace(":", "_").replace("/", "_") + (f"_{tag}" if tag else "")
    # Identifiers are stored as VERDICTS, not literals — see eval/redact.py. Keeps the DOI traps
    # fully inspectable while leaving G7's vocabulary clean and eval re-runs friction-free.
    from redact import redact_tree  # noqa: E402
    payload = redact_tree({"summary": summary, "results": out})
    (RESULTS / f"{slug}.json").write_text(json.dumps(payload, indent=1))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="openai:gpt-5")
    ap.add_argument("--only", default="")
    ap.add_argument("--no-judge", action="store_true")
    # A targeted re-run must not overwrite the file a full run wrote. An experiment that gets
    # silently replaced by a subset of itself is an experiment discarded.
    ap.add_argument("--tag", default="", help="suffix the results filename, e.g. --tag targeted")
    a = ap.parse_args()
    only = [x for x in a.only.split(",") if x] or None
    summaries = []
    for m in a.models.split(","):
        print(f"\n=== {m} ===")
        summaries.append(run(m.strip(), only, not a.no_judge, a.tag))
    print("\n=== SUMMARY ===")
    for s in summaries:
        print(json.dumps(s, indent=1))


if __name__ == "__main__":
    main()

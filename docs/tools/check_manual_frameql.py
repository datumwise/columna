#!/usr/bin/env python3
"""
check_manual_frameql.py — the manual verifies itself against the shipped PLANNER (standing gate).

THE FAILURE THIS NOW CLOSES (Mission B, 2026-08-31). This gate used to be GRAMMAR ONLY and said so:
"it may still refuse/clarify at PLAN time; that is semantics, not grammar — this check is grammar
only." It therefore reported `37 total — 36 parse-clean, 0 FAIL` while **seventeen of those
thirty-seven examples died at planning or execution**, and while four Chapter 6 examples used forms
§2.8 itself calls unshipped, unmarked. A guard that proves a query is well-formed proves nothing
about whether it runs, and the gap between those two is exactly where a manual goes quietly wrong.

THE GOVERNING PRINCIPLE (ruled Huayin, 2026-08-31):

    A Manual example presented as executable is not validated until the stage at which its claimed
    behaviour is observable.

So the gate is STAGED, and how far an example is carried depends on what it claims:

  ```frameql             SHIPPED. Must parse, and must PLAN. If the plan is `serve` or `disclose`,
                         it is then EXECUTED against the fixture and the FINAL disposition asserted —
                         because a plan-time `serve` is a statement about the plan, not about a
                         result, and `cumsum` is a live example of one that plans `serve` and dies in
                         the engine. If the plan is `clarify` or `refuse`, planning is sufficient,
                         but the DOCUMENTED reason must match: a generic failure is not a pass.
  ```frameql-illformed   Must NOT parse. A marked example that starts parsing is itself a failure.
  ```frameql-roadmap     Documented as unshipped. The gate asserts the MARK — the owning section must
                         carry [ROADMAP] or [SCHEDULED] — and deliberately does NOT pin today's
                         implementation failure as the example's required behaviour, so that shipping
                         the capability does not turn this gate red.
  ```frameql-schematic   A metasyntactic TEMPLATE (`op(col_1 @ {a_1}, …)`), not a query. Grammar only:
                         a schematic asserts a shape, and there is nothing to run.
  bare ``` starting with a statement keyword is treated as ```frameql (the legacy spelling).

THE EXPECTATION LIVES IN THE MANUAL, NOT BESIDE IT. There is no manifest of expected outcomes; a
second copy of the Manual's claims would drift from the prose it is supposed to be checking. The
Manual already carries everything needed: its `[ROADMAP]`/`[SCHEDULED]` section marks, its fences,
and — where the prose commits to a specific mood — a trailing annotation on the statement itself, the
convention §5.6 already uses:

    SELECT revenue AT {category.touch}   -- disclose: over_count (material) + coverage (info)

`-- <outcome>[: <reason>]` is read as the documented disposition. Everything after the reason word is
prose for the reader and is ignored. An annotation that is not a mood word is an ordinary
illustrative note, as before, and is stripped.

FIXTURES. `manual_fixtures/` declares the Manual's OWN vocabulary and is adjudicated by a real
`publish()` — see `manual_fixtures/harness.py` for why both of those are load-bearing, and why a
thinner fixture would make every finding unsafe to act on.

Run: `python docs/tools/check_manual_frameql.py [--verbose]`  → exit 0 iff every example holds.
"""
import argparse
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "manual_fixtures"))

try:
    from columna_core.envelope import parse_statement, EnvelopeSyntaxError
    from columna_core.disclosure_wire import wire_frame
except ModuleNotFoundError:                                    # pragma: no cover
    sys.stderr.write("columna_core not importable — install columna-core (0.9.0+) first.\n")
    sys.exit(2)

MANUAL = pathlib.Path(__file__).resolve().parents[1] / "frame_ql_manual_v2.md"

_FENCE = re.compile(r"^(\s*)```([A-Za-z0-9_-]*)\s*$")
_STMT_START = re.compile(r"^\s*(EXPLAIN|FROM|WITH|SELECT)\b", re.IGNORECASE)
_BQ = re.compile(r"^\s{0,3}> ?")                                # one level of Markdown blockquote marker
_COMMENT = re.compile(r"\s*--.*$")                             # illustrative `-- …` annotation (not grammar)


def _fenced_blocks(text: str):
    """Yield (lineno, info_string, body) for every fenced block. Blockquote markers (`> `) are stripped
    per line FIRST, so an example fenced INSIDE a `>` blockquote (the ▸-revision notes carry several) is
    detected and checked exactly like a top-level one — the parser rule applies to EVERY example, quoted
    or not. Without this, a blockquoted `SELECT … AT {…}` was invisible to the guard and could drift."""
    out, i, lines = [], 0, [_BQ.sub("", ln) for ln in text.splitlines()]
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if m:
            info, start, body = m.group(2), i + 1, []
            i += 1
            while i < len(lines) and not _FENCE.match(lines[i]):
                body.append(lines[i]); i += 1
            out.append((start, info.lower(), "\n".join(body)))
        i += 1
    return out


_SELECT = re.compile(r"^\s*SELECT\b", re.IGNORECASE)


def _statements(body: str):
    """Split a frameql block into individual statements WITHOUT a crude blank-line heuristic. A statement
    is `[EXPLAIN] [FROM] [WITH…] SELECT … AT …` — the preamble keywords belong to the SAME statement as
    their SELECT. So a NEW statement boundary is a top-level EXPLAIN/FROM/WITH/SELECT line reached only
    AFTER the current statement already has its SELECT (i.e. the prior one is complete)."""
    stmts, cur, has_select, depth = [], [], False, 0
    for ln in body.splitlines():
        ln = _COMMENT.sub("", ln)                              # strip trailing `-- …` annotation FIRST
        at_start = depth == 0 and bool(_STMT_START.match(ln))
        if at_start and has_select and cur:                    # the prior statement ended; start a new one
            stmts.append("\n".join(cur).strip()); cur, has_select = [], False
        cur.append(ln)
        if depth == 0 and _SELECT.match(ln):
            has_select = True
        depth += ln.count("(") + ln.count("{") + ln.count("[")
        depth -= ln.count(")") + ln.count("}") + ln.count("]")
    if "\n".join(cur).strip():
        stmts.append("\n".join(cur).strip())
    return [s for s in stmts if s]


#: `-- serve` / `-- disclose: over_count …` / `-- clarify: input_anchor_ambiguous` — the Manual
#: stating, on the example itself, which mood it commits to. §5.6 already writes them this way.
_MOODS = ("serve", "disclose", "clarify", "refuse")
_ANNOT = re.compile(r"--\s*(?P<outcome>serve|disclose|clarify|refuse)\b\s*(?::\s*(?P<reason>\w+))?",
                    re.IGNORECASE)


def _annotation(body_line: str):
    """(outcome, reason|None) documented on this line, or None if the `--` note is ordinary prose."""
    m = _ANNOT.search(body_line)
    if not m:
        return None
    return m.group("outcome").lower(), (m.group("reason") or None)


def sections(text: str):
    """(line, heading, mark) for every heading. A `[ROADMAP]`/`[SCHEDULED]` mark is the MANUAL
    declaring a form unshipped — the only honest source for "documented not to run", and the reason
    this gate needs no parallel manifest of expectations."""
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.startswith("#"):
            mark = "ROADMAP" if "[ROADMAP" in ln else ("SCHEDULED" if "[SCHEDULED" in ln else None)
            out.append((i, ln.lstrip("# ").strip(), mark))
    return out


def owning_section(secs, lineno):
    cur = (0, "(preamble)", None)
    for sec in secs:
        if sec[0] <= lineno:
            cur = sec
        else:
            break
    return cur


def _reason(w):
    """The reason the Manual would name for this disposition.

    A withheld answer carries it on `no_result`; a SERVED-but-disclosed one carries it as a
    disclosure CODE, because nothing was withheld and there is no `no_result` to hang it on. §5.6's
    `-- disclose: over_count` documents a disclosure code, so the gate has to look in both places or
    it would demand that a served answer explain itself through a field only a refusal has."""
    for c in w["columns"]:
        nr = c.get("no_result") or {}
        if nr.get("reason"):
            return nr["reason"]
    codes = [d.get("code") for c in w["columns"] for d in (c.get("disclosures") or []) if d.get("code")]
    codes += [d.get("code") for d in (w.get("frame", {}).get("disclosures") or []) if d.get("code")]
    return codes[0] if codes else None


def _disposition(srvs, harness, stmt_text, execute):
    """(stage, outcome, reason) for one example. `stage` is how far it got, so a failure can name the
    point at which the claim stopped being observable."""
    try:
        st = parse_statement(stmt_text)
    except EnvelopeSyntaxError as e:
        return "parse", "syntax-error", str(e)[:90]
    srv = harness.server_for(srvs, st)
    try:
        fr = srv.planner.plan_statement(st)
    except Exception as e:                                     # FrameQLSyntaxError & friends
        return "plan", "syntax-error", str(e)[:90]
    w = wire_frame(fr, executed=False)
    if not (execute and w["outcome"] in ("serve", "disclose")):
        return "plan", w["outcome"], _reason(w)
    # THE STAGE THE CLAIM BECOMES OBSERVABLE. A plan-time `serve` is a statement about the plan.
    try:
        fr = srv.planner.run_statement(st)
    except Exception as e:
        return "execute", "syntax-error", str(e)[:90]
    return "execute", wire_frame(fr)["outcome"], _reason(wire_frame(fr))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    import harness
    text = MANUAL.read_text()
    secs = sections(text)
    srvs = harness.servers()

    counts = {"shipped": 0, "illformed": 0, "roadmap": 0, "schematic": 0}
    failures, rows = [], []

    for lineno, info, body in _fenced_blocks(text):
        stmts = _statements(body)
        kind = info
        if info in ("", "frameql") and stmts and _STMT_START.match(stmts[0]):
            kind = "frameql"
        if kind not in ("frameql", "frameql-illformed", "frameql-roadmap", "frameql-schematic"):
            continue
        _, head, mark = owning_section(secs, lineno)
        annots = [a for a in (_annotation(ln) for ln in body.splitlines()) if a]

        if kind == "frameql-illformed":
            for stmt in stmts:
                try:
                    parse_statement(stmt)
                    failures.append((lineno, head, "marked-illformed-but-parses", stmt,
                                     "the teaching went stale: this now parses"))
                except EnvelopeSyntaxError:
                    counts["illformed"] += 1
            continue

        if kind == "frameql-roadmap":
            # Assert the MARK, never today's failure: pinning the failure would turn shipping the
            # capability into a red gate, which is the wrong incentive to build into a guard.
            if mark is None:
                failures.append((lineno, head, "roadmap-without-mark", stmts[0] if stmts else "",
                                 "a ```frameql-roadmap example must sit under a section marked "
                                 "[ROADMAP] or [SCHEDULED] — the reader sees the heading, not the fence"))
            else:
                counts["roadmap"] += len(stmts) or 1
            continue

        if kind == "frameql-schematic":
            for stmt in stmts:                                  # a shape, not a query: grammar only
                try:
                    parse_statement(stmt); counts["schematic"] += 1
                except EnvelopeSyntaxError as e:
                    failures.append((lineno, head, "schematic-does-not-parse", stmt, str(e)[:80]))
            continue

        # ── shipped ────────────────────────────────────────────────────────────────────────────
        if mark is not None:
            failures.append((lineno, head, "shipped-example-in-roadmap-section", stmts[0] if stmts else "",
                             f"section is marked [{mark}] but the example is fenced as shipped — "
                             f"mark the fence ```frameql-roadmap or unmark the section"))
            continue
        for n, stmt in enumerate(stmts):
            want = annots[n] if n < len(annots) else None
            stage, outcome, reason = _disposition(srvs, harness, stmt, execute=True)
            counts["shipped"] += 1
            rows.append((lineno, head, stage, outcome, reason, stmt))
            if outcome == "syntax-error":
                failures.append((lineno, head, f"dies-at-{stage}", stmt, reason))
                continue
            if want is None:
                if outcome in ("clarify", "refuse", "error"):
                    failures.append((lineno, head, f"{outcome}-at-{stage}", stmt,
                                     f"presented as shipped but reaches {outcome}"
                                     + (f" ({reason})" if reason else "")
                                     + " — document the outcome inline (`-- refuse: <reason>`), or "
                                       "mark the example roadmap"))
                continue
            w_out, w_reason = want
            if outcome != w_out:
                failures.append((lineno, head, "documented-outcome-not-reached", stmt,
                                 f"documented `{w_out}`, got `{outcome}` at {stage}"))
            elif w_reason and reason != w_reason:
                failures.append((lineno, head, "documented-reason-not-reached", stmt,
                                 f"documented reason `{w_reason}`, got `{reason or "none"}` — a "
                                 f"generic failure is not a pass"))

    for lineno, head, kind, stmt, why in failures:
        one = " ".join(str(stmt).split())[:88]
        print(f"FAIL @L{lineno} §{head[:34]} [{kind}]\n      {one}\n      -> {why}", file=sys.stderr)
    if args.verbose:
        for lineno, head, stage, outcome, reason, stmt in rows:
            print(f"  L{lineno:<5} {stage:8} {outcome:9} {reason or '':22} {' '.join(stmt.split())[:60]}")

    total = sum(counts.values()) + len(failures)
    print(f"manual FrameQL examples: {total} total — {counts['shipped']} shipped "
          f"(planned, and executed where they plan to serve/disclose), {counts['roadmap']} roadmap, "
          f"{counts['illformed']} marked ill-formed, {counts['schematic']} schematic, "
          f"{len(failures)} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

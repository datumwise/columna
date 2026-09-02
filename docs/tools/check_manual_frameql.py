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
    from columna_core.frameql import FrameQLSyntaxError
    from columna_core.disclosure import Refusal
    from columna_core.disclosure_wire import wire_frame
except ModuleNotFoundError:                                    # pragma: no cover
    sys.stderr.write("columna_core not importable — install columna-core (0.9.0+) first.\n")
    sys.exit(2)

MANUAL = pathlib.Path(__file__).resolve().parents[1] / "frame_ql_language.md"

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


#: SELECT ANYWHERE AT DEPTH 0, NOT ONLY AT LINE START. `FROM m SELECT x AT {a}` on ONE line is a
#: legal spelling — the fixtures use it throughout — and anchoring this to the start of a line meant
#: a block of two such one-liners never registered a statement boundary: both lines were glued into
#: a single "statement" that then died at parse with "FROM appears more than once". The splitter was
#: reporting a Manual defect it had itself manufactured.
_SELECT = re.compile(r"\bSELECT\b", re.IGNORECASE)


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
        if depth == 0 and _SELECT.search(ln):
            has_select = True
        depth += ln.count("(") + ln.count("{") + ln.count("[")
        depth -= ln.count(")") + ln.count("}") + ln.count("]")
    if "\n".join(cur).strip():
        stmts.append("\n".join(cur).strip())
    return [s for s in stmts if s]


#: `-- serve` / `-- disclose: over_count …` / `-- clarify: input_anchor_ambiguous` — the Manual
#: stating, on the example itself, which mood it commits to. §5.6 already writes them this way.
#:
#: `error` IS DOCUMENTABLE, AND IS NOT A FIFTH MOOD. The four analytical dispositions are
#: serve/disclose/clarify/refuse and stay four; `error` is the separate query-error channel (§7.3),
#: which carries a request the language does not accept and a realization that cannot carry out an
#: admissible one. It is listed here because the gate can only check a claim the Manual is able to
#: WRITE: before this, an example reaching `error` had no lawful annotation, so §7.3's own examples
#: would have had to be presented as unchecked prose — the one thing this gate exists to prevent.
_MOODS = ("serve", "disclose", "clarify", "refuse", "error")
_ANNOT = re.compile(r"--\s*(?P<outcome>serve|disclose|clarify|refuse|error)\b\s*(?::\s*(?P<reason>\w+))?",
                    re.IGNORECASE)


def _annotation(body_line: str):
    """(outcome, reason|None) documented on this line, or None if the `--` note is ordinary prose."""
    m = _ANNOT.search(body_line)
    if not m:
        return None
    return m.group("outcome").lower(), (m.group("reason") or None)


# ── PROSE CLAIMS ─────────────────────────────────────────────────────────────────────────────────
#: The Manual makes behavioural claims in PROSE as well as in fences, and prose is where the drift
#: hid: §2.8 "Scan execution is not available in the current Core build" was false in six of the
#: eight operators it named, and §§6.11/6.15/6.16 each assert "plans; does not execute" for examples
#: the gate never planned. A claim the gate cannot read is a claim nothing can falsify.
_CLAIM_PLANS = re.compile(r"\b(?:parses and plans|plans)\b[^.]{0,40}?(?:;|,|\.|$)", re.I)
_CLAIM_NO_EXEC = re.compile(r"does not execute|is not available in the current core build|"
                            r"not executable in this build|does not run", re.I)
_CLAIM_NO_PARSE = re.compile(r"does not parse|is not shipped at all", re.I)


def section_body(text: str, secs, lineno: int) -> str:
    """The prose of the section owning `lineno`, so a claim written in a sentence is as checkable as
    one written in a fence."""
    lines = text.splitlines()
    start = 0
    end = len(lines)
    for i, (ln, _h, _m) in enumerate(secs):
        if ln <= lineno:
            start = ln
            end = secs[i + 1][0] - 1 if i + 1 < len(secs) else len(lines)
        else:
            break
    return "\n".join(lines[start:end])


#: Direction of a drift, because the REMEDY differs and the wrong remedy is how a capability gets
#: reverted by a contributor in a hurry.
EXCEEDS = "CLAIM_EXCEEDS_BUILD"      # the Manual promises more than the build delivers
IMPROVED = "CAPABILITY_IMPROVED"     # the build delivers more than the Manual claims
UNCHECKED = "UNCHECKED"              # the gate cannot see this claim at all
_REMEDY = {
    EXCEEDS: "the Manual is wrong, or the build regressed — check the build FIRST, then the text",
    IMPROVED: "UPDATE THE DOCUMENTATION, NEVER REVERT THE CODE. The build grew a capability the "
              "Manual still denies; the fix is a one-line mark/prose edit, and reverting the "
              "capability to make this green would be exactly backwards",
    UNCHECKED: "label the fence (```frameql, ```frameql-roadmap, ```frameql-illformed, "
              "```frameql-schematic, ```frameql-fragment, ```frameql-retired, "
              "```frameql-metasyntax, ```cml) so the claim becomes checkable",
}

#: EVERY FENCE THE GATE UNDERSTANDS, and what each one ASSERTS. A block whose fence is not here is
#: UNCHECKED — reported, never skipped in silence.
#:
#: The last three close the hole that nine unlabelled blocks sat in. Two of them make a REAL claim
#: rather than merely being excused:
#:   frameql-retired    — a form the language REMOVED (Appendix D's trailing-`@`). Asserting that it
#:                        still does not parse is how a retirement stays retired; if one of these
#:                        starts parsing again, the build regressed and the gate says so.
#:   frameql-metasyntax — BNF/template ABOUT the language, not a sentence IN it (§1.2's skeleton, with
#:                        its `[optional]` brackets and `<placeholders>`). It must NOT parse; a
#:                        skeleton that parses as a query has stopped being a skeleton.
#:   cml                — a different language (§5.6's `RELATE … FACES`). EXPLICITLY out of scope for
#:                        a Frame-QL gate, per the ruling — but NAMED and COUNTED, because "excluded
#:                        on purpose" and "invisible" must never look the same in the report.
_FENCES = ("frameql", "frameql-illformed", "frameql-roadmap", "frameql-schematic",
           "frameql-fragment", "frameql-retired", "frameql-metasyntax", "cml")


# ── THE OPERATOR REFERENCE, CHECKED AGAINST THE SHIPPED REGISTRY ─────────────────────────────────
# APPENDIX A IS A CAPABILITY TABLE, AND A TABLE IS A CLAIM. Every fenced example in this Manual is
# now measured, and Appendix A was still invisible — so `product`, `any`, `all`, `weighted_mean`,
# `variance`, `stddev`, `value_at_max`, `value_at_min` sat unmarked in the reducer table, and the
# whole Map-functions block (comparisons, conditionals, string, temporal, `cast`) sat unmarked
# beneath it, while the shipped registry has none of them.
#
# THIS IS THE OPERATOR-LEVEL SOURCE THE §2.8 BLIND SPOT NEEDED (ruled Huayin, 2026-09-01: "the
# conformance system must be able to verify capability claims that are not attached to one fenced
# example ... do not require one artificial example per operator merely to satisfy the checker if a
# better operator-level conformance source exists"). The better source already existed: the registry
# IS the planner's contract with the engine, so it is the one place that knows what the language has.
# No example is manufactured for any operator; the table is diffed against the vocabulary directly.
#
# ALIASES ARE READ, NEVER INFERRED. `ALIASES` in operators.py is the declared name→name table; a
# Manual name that resolves through it is SHIPPED under another spelling, not missing. Guessing that
# `approx_distinct` "obviously" means `distinct` would be the same error as guessing an equivalence
# in §3.2 — plausible, undeclared, and therefore not a fact the gate may assert. Where the alias is
# real but undeclared, the remedy is to DECLARE it (one reviewable line), not to teach the gate to
# infer it.
_APX_A = re.compile(r"^##\s+Appendix A", re.M)
CA_BEGIN = "<!-- BEGIN GENERATED: capability-reference -->"
CA_END = "<!-- END GENERATED: capability-reference -->"
_OP_TOKEN = re.compile(r"`([^`]+)`")
#: table rows are `| \`sum\` | fertile | … |` — the first cell holds the names
_ROW = re.compile(r"^\|\s*(?P<first>[^|]*)\|")
#: `Arithmetic: `+`, `-`, …` — a category label made of letters/slash/space only, so a PROSE sentence
#: that happens to contain a colon ("A note on `last` and `first` as family founders: …") does not
#: masquerade as a vocabulary list, and neither does "Scan parameters, passed by keyword:" (comma).
_LIST_LINE = re.compile(r"^[A-Za-z/ ]{1,24}:\s")


def _op_names(cell: str):
    """Operator names in a table cell or prose list item, normalised to their registry spelling:
    backticks stripped, a call illustration (`lag(col, n)`) reduced to its head, `count(*)` kept
    whole because the Manual treats it as its own spelling (and parser.py gives it its own lift)."""
    out = []
    for tok in _OP_TOKEN.findall(cell):
        t = tok.strip()
        if t.startswith("count(*"):
            out.append("count(*)"); continue
        t = re.sub(r"\(.*$", "", t).strip()          # `lag(col, n)` -> lag ; `HLLSketch(p)` -> HLLSketch
        if t and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*|[-+*/%<>=!]+", t):
            out.append(t)
    return out


def operator_reference_drift(text, secs):
    """Appendix A's capability tables are now a GENERATED PROJECTION of the canonical authority
    (`specs/frameql_capabilities.toml`), emitted by `regen_capability_tables.py` and drift-checked
    there. So this no longer re-diffs those rows — that would only re-derive what the generator just
    wrote, which is a tautology dressed as a check.

    WHAT IS STILL WORTH ASKING, and what this now asks:

      1. Has a hand-maintained vocabulary table come BACK, outside the generated block? That is how
         the P0-17 class returns: a second independent claim about the same governed disposition,
         kept in step by hand until it isn't. Any structured vocabulary row found outside the markers
         is reported, whatever it says.
      2. Does every name such a row uses resolve to a CANONICAL CAPABILITY? Resolution goes through
         the authority's own spelling index — never through the shipped registry, which would make
         one implementation's membership the test of what the language has.

    Returns (failures, named, unnamed) with the same shape as before; the registry-completeness
    direction moved to `capability_authority.py`, where the three layers are joined."""
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import capability_authority as CA
        caps = CA.canonical_capabilities()
        spellings = CA.spelling_index(caps)
    except Exception:                                          # pragma: no cover
        return [], set(), set()

    lines = text.splitlines()
    m = _APX_A.search(text)
    if not m:
        return [], set(), set()
    start = text[:m.start()].count("\n")
    # BOUNDED AT THE NEXT APPENDIX, and generated lines are SKIPPED IN PLACE rather than stripped —
    # stripping shifted every reported line number, and an unbounded scan walked into Appendix B and
    # reported its reserved-keyword list (INHERIT, JOIN, COMPOSE, ...) as unknown capabilities. A
    # checker that mislocates its findings is worse than one that misses them.
    end = next((ln - 1 for ln, h, _k in secs if ln > start + 1 and h.startswith("Appendix B")),
               len(lines))
    generated = set()
    depth = 0
    for i, raw in enumerate(lines):
        if CA_BEGIN in raw:
            depth = 1
        if depth:
            generated.add(i)
        if CA_END in raw:
            depth = 0
    fails, named = [], set()
    sub = None
    for i in range(start, min(end, len(lines))):
        if i in generated:
            continue
        raw = lines[i]
        if raw.startswith("###"):
            sub = raw.lstrip("# ").strip(); continue
        row = _ROW.match(raw)
        listy = _LIST_LINE.match(raw)
        if not (row or listy) or raw.lstrip().startswith("|---"):
            continue
        cell = row.group("first") if row else raw
        names = [n for n in _op_names(cell)
                 if n not in ("fertile", "mule", "native", "same", "identity", "Capability")]
        if not names:
            continue
        for name in names:
            cid = spellings.get(name)
            if cid is None:
                fails.append((EXCEEDS, i + 1, f"Appendix A / {sub or 'operators'}",
                              "operator-not-a-canonical-capability", name,
                              "this names no capability in specs/frameql_capabilities.toml — add it "
                              "to the canonical authority, or declare it as a spelling of one"))
            else:
                named.add(cid)
                fails.append((EXCEEDS, i + 1, f"Appendix A / {sub or 'operators'}",
                              "hand-maintained-vocabulary-table", name,
                              "a vocabulary row outside the generated block is a SECOND authority for "
                              "a governed disposition — the P0-17 class. Move it into "
                              "specs/frameql_capabilities.toml and let the table be projected"))
    return fails, named, set()


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
    """The reason(s) the Manual could name for this disposition, as a list — first is the one to
    PRINT, and any of them satisfies a documented reason.

    A withheld answer carries it on `no_result`; a SERVED-but-disclosed one carries it as a
    disclosure CODE, because nothing was withheld and there is no `no_result` to hang it on. §5.6's
    `-- disclose: over_count` documents a disclosure code, so the gate has to look in both places or
    it would demand that a served answer explain itself through a field only a refusal has.

    WHY A LIST AND NOT THE FIRST CODE (2026-09-02). A disclose carries SEVERAL codes and the wire
    does not promise their order, so matching only `codes[0]` made a documented code pass or fail on
    emission order — §5.6's `over_count` passed because it happened to sort first. §2.3's material
    `input_anchor` caveat rides behind an immaterial `provenance` note on the same column, so under
    the old rule the Manual could only document the note it is NOT making a claim about. Order is not
    a thing the Manual should have to know."""
    for c in w["columns"]:
        nr = c.get("no_result") or {}
        if nr.get("reason"):
            return [nr["reason"]]
    codes = [d.get("code") for c in w["columns"] for d in (c.get("disclosures") or []) if d.get("code")]
    codes += [d.get("code") for d in (w.get("frame", {}).get("disclosures") or []) if d.get("code")]
    return codes


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
    except (EnvelopeSyntaxError, FrameQLSyntaxError, Refusal) as e:
        # THE QUERY-ERROR CHANNEL, REACHING THE CALLER BY RAISE RATHER THAN BY FRAME (classification
        # ruled Huayin, 2026-09-02: missing required syntax is Invalid / query error, not a Clarify
        # and not a Refuse). A statement that PARSES and is then rejected at planning as not a valid
        # Frame-QL request is §7.3's language-invalid case, so the Manual must be able to document it
        # — before this it was reported as `syntax-error`, an outcome no annotation could name, and
        # §7.4's three syntax entries would have had to ship as unchecked prose.
        #
        # THE GUARD IS NOT WEAKENED. An UNDOCUMENTED shipped example reaching here still fails: it is
        # not a positive outcome, so the `want is None` branch demands the Manual either document the
        # outcome or mark the example roadmap. Only an example that explicitly claims `-- error` now
        # passes, and it must match the reason where one is carried.
        #
        # Parse-stage failures keep the `syntax-error` outcome above: those are what
        # ```frameql-illformed asserts, and conflating "does not parse" with "parses and is invalid"
        # would let a block marked ill-formed pass on the wrong evidence.
        return "plan", "error", [getattr(e, "reason", None)] if getattr(e, "reason", None) else str(e)[:90]
    except Exception as e:
        # AN UNGOVERNED SUBSTRATE ESCAPE (P1-26). A raw CPython `SyntaxError` — or any exception the
        # language does not own — reaching the caller IS the defect, whatever the Manual says about
        # the form, and whatever its canonical status turns out to be. Given its own outcome so the
        # gate can never mistake it for a disposition.
        return "plan", "substrate-error", f"{type(e).__module__}.{type(e).__name__}: {str(e)[:70]}"
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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--report", action="store_true",
                    help="print the drift report and exit 0 — for reading the deltas before the "
                         "Manual has been corrected to match a repaired build")
    args = ap.parse_args()

    import harness
    text = MANUAL.read_text()
    secs = sections(text)
    srvs = harness.servers()

    counts = {"shipped": 0, "illformed": 0, "roadmap": 0, "schematic": 0, "fragment": 0,
              "retired": 0, "metasyntax": 0, "cml": 0}
    blocks_seen = blocks_checked = 0
    stmts_seen = 0
    failures, rows, unchecked, excluded = [], [], [], []

    def fail(direction, lineno, head, kind, stmt, why):
        failures.append((direction, lineno, head, kind, stmt, why))

    for lineno, info, body in _fenced_blocks(text):
        stmts = _statements(body)
        kind = info
        if info in ("", "frameql") and stmts and _STMT_START.match(stmts[0]):
            kind = "frameql"
        blocks_seen += 1

        if kind not in _FENCES:
            # UNCHECKED. Previously these were `continue`d in silence and the headline counted only
            # STATEMENTS, so nine unlabelled blocks were invisible behind "40 total". A block the
            # gate skips is a claim nothing can falsify, so skipping is now itself reportable — and
            # a block that PARSES while unlabelled is worse, because it is a real Frame-QL claim
            # sitting outside every check.
            parses = []
            for st in stmts:
                try:
                    parse_statement(st); parses.append(st)
                except Exception:
                    pass
            unchecked.append((lineno, owning_section(secs, lineno)[1], info or "(bare)", stmts, parses))
            continue

        blocks_checked += 1
        stmts_seen += len(stmts)
        _, head, mark = owning_section(secs, lineno)
        annots = [a for a in (_annotation(ln) for ln in body.splitlines()) if a]
        prose = section_body(text, secs, lineno)
        claims_plans = bool(_CLAIM_PLANS.search(prose))
        claims_no_exec = bool(_CLAIM_NO_EXEC.search(prose))
        claims_no_parse = bool(_CLAIM_NO_PARSE.search(prose))

        if kind == "cml":
            # A DIFFERENT LANGUAGE. Out of scope for a Frame-QL gate by ruling — but counted and
            # listed, so the report distinguishes "deliberately excluded" from "never looked at".
            counts["cml"] += 1
            excluded.append((lineno, head, kind, "declares vocabulary in CML, not Frame-QL"))
            continue

        if kind in ("frameql-retired", "frameql-metasyntax"):
            # BOTH ASSERT NON-PARSE, for different reasons, so the failure names the right one.
            why = ("the retirement regressed: this form was removed from the language and the "
                   "shipped parser accepts it again"
                   if kind == "frameql-retired" else
                   "a metasyntactic skeleton that parses as a query has stopped being a skeleton — "
                   "either the placeholders leaked into real syntax, or this is a real example "
                   "mislabelled")
            for stmt in stmts:
                try:
                    parse_statement(stmt)
                    fail(EXCEEDS, lineno, head, f"{kind[8:] if kind.startswith('frameql-') else kind}"
                                                f"-but-parses", stmt, why)
                except Exception:
                    counts["retired" if kind == "frameql-retired" else "metasyntax"] += 1
            continue

        if kind == "frameql-fragment":
            counts["fragment"] += len(stmts) or 1              # illustrative; declared as such
            continue

        if kind == "frameql-schematic":
            for stmt in stmts:                                  # a shape, not a query: grammar only
                try:
                    parse_statement(stmt); counts["schematic"] += 1
                except EnvelopeSyntaxError as e:
                    fail(EXCEEDS, lineno, head, "schematic-does-not-parse", stmt, str(e)[:80])
            continue

        if kind == "frameql-illformed":
            for stmt in stmts:
                try:
                    parse_statement(stmt)
                    fail(IMPROVED, lineno, head, "marked-illformed-but-parses", stmt,
                         "the teaching went stale: this now parses")
                except EnvelopeSyntaxError:
                    counts["illformed"] += 1
            continue

        # ── EVERY REMAINING BLOCK IS MEASURED, whatever it is marked ─────────────────────────────
        # The old gate returned early for `frameql-roadmap` and asserted only the MARK, on the sound
        # reasoning that pinning today's failure would make shipping a capability turn the gate red.
        # That reasoning is kept — see the IMPROVED remedy — but the CONSEQUENCE was a one-way gate:
        # the Manual could understate the build indefinitely and stay green, and it did. `cumsum`
        # and four more scan operators execute while §2.8 says scan execution is unavailable.
        # FAIL CLOSED ON CARDINALITY (ruled Huayin, 2026-09-01: the gate must not silently check
        # fewer claims than the block makes). `want = annots[n] if n < len(annots)` was POSITIONAL
        # TRUNCATION: a three-statement block carrying one `-- refuse: …` checked statement 1 against
        # it and let statements 2 and 3 through unannotated, so two documented claims went unread and
        # the headline still said the block passed. No block is mismatched today, which is exactly
        # when to close it — the check costs nothing and the failure mode is silent.
        if annots and len(annots) != len(stmts):
            fail(EXCEEDS, lineno, head, "annotation-cardinality-mismatch", stmts[0] if stmts else "",
                 f"{len(stmts)} statement(s) but {len(annots)} documented outcome(s) — the gate "
                 f"would check fewer claims than this block makes. Annotate every statement, or "
                 f"none of them.")
            continue

        for n, stmt in enumerate(stmts):
            want = annots[n] if annots else None       # cardinality is now 0 or len(stmts), checked above
            stage, outcome, reason = _disposition(srvs, harness, stmt, execute=True)
            # `_disposition` hands back a LIST of reasons from the wire paths and a bare string from
            # the parse/plan-exception paths (there the message IS the reason). Flattened once, here,
            # so every consumer below reads one shape: `reasons` to check against, `reason` to print.
            reasons = reason if isinstance(reason, list) else ([reason] if reason else [])
            reason = reasons[0] if reasons else None
            rows.append((lineno, head, kind, stage, outcome, reason, stmt))
            reached_positive = outcome in ("serve", "disclose")
            if outcome == "substrate-error":
                # Unconditional, and deliberately ahead of every fence rule: no Manual mark can make
                # it acceptable for an exception the language does not own to reach a reader as the
                # language's answer. Independent of the form's canonical status, which stays open.
                fail(EXCEEDS, lineno, head, "substrate-exception-escapes", stmt,
                     f"an exception Frame-QL does not own reached the caller: {reason}")
                continue

            if kind == "frameql-roadmap":
                counts["roadmap"] += 1
                if mark is None:
                    fail(EXCEEDS, lineno, head, "roadmap-without-mark", stmt,
                         "a ```frameql-roadmap example must sit under a section marked [ROADMAP] "
                         "or [SCHEDULED] — the reader sees the heading, not the fence")
                if reached_positive:
                    fail(IMPROVED, lineno, head, "roadmap-but-shipped", stmt,
                         f"documented as roadmap, but this {outcome}s at {stage} today")
                elif claims_plans and outcome in ("syntax-error", "substrate-error"):
                    fail(EXCEEDS, lineno, head, "claims-planning-but-does-not-plan", stmt,
                         f"the section says it plans; it never reaches a plan ({reason})")
                if claims_no_exec and stage == "execute" and reached_positive:
                    fail(IMPROVED, lineno, head, "claims-no-execution-but-executes", stmt,
                         "the section says it does not execute; it executes")
                if claims_no_parse:
                    try:
                        parse_statement(stmt)
                        fail(IMPROVED, lineno, head, "claims-no-parse-but-parses", stmt,
                             "the section says this does not parse; it parses")
                    except Exception:
                        pass
                continue

            # ── shipped ──────────────────────────────────────────────────────────────────────────
            counts["shipped"] += 1
            if mark is not None:
                fail(EXCEEDS, lineno, head, "shipped-example-in-roadmap-section", stmt,
                     f"section is marked [{mark}] but the example is fenced as shipped — "
                     f"mark the fence ```frameql-roadmap or unmark the section")
                continue
            if outcome == "syntax-error":
                fail(EXCEEDS, lineno, head, f"dies-at-{stage}", stmt, reason)
                continue
            if want is None:
                if not reached_positive:
                    fail(EXCEEDS, lineno, head, f"{outcome}-at-{stage}", stmt,
                         f"presented as shipped but reaches {outcome}"
                         + (f" ({reason})" if reason else "")
                         + " — document the outcome inline (`-- refuse: <reason>`), or "
                           "mark the example roadmap")
                continue
            w_out, w_reason = want
            if outcome != w_out:
                direction = IMPROVED if (reached_positive and w_out in ("clarify", "refuse")) else EXCEEDS
                fail(direction, lineno, head, "documented-outcome-not-reached", stmt,
                     f"documented `{w_out}`, got `{outcome}` at {stage}")
            elif w_reason and w_reason not in reasons:
                fail(EXCEEDS, lineno, head, "documented-reason-not-reached", stmt,
                     f"documented reason `{w_reason}`, got `{', '.join(reasons) or 'none'}` — a "
                     f"generic failure is not a pass")

    # ── APPENDIX A: the operator table, against the shipped registry ─────────────────────────────
    op_fails, op_named, op_unnamed = operator_reference_drift(text, secs)
    failures.extend(op_fails)
    if op_unnamed:
        # THE OTHER DIRECTION. Vocabulary the build HAS and the reference never names is a reader
        # who cannot discover a shipped operator from the operator reference.
        failures.append((IMPROVED, 0, "Appendix A", "registered-but-undocumented",
                         ", ".join(sorted(op_unnamed)),
                         f"{len(op_unnamed)} operator(s) are in the shipped registry and appear "
                         f"nowhere in Appendix A — the reference is not a complete list of what "
                         f"the language has"))

    # ── report ───────────────────────────────────────────────────────────────────────────────────
    for direction in (EXCEEDS, IMPROVED, UNCHECKED):
        group = [f for f in failures if f[0] == direction]
        if direction == UNCHECKED:
            group = unchecked
        if not group:
            continue
        print(f"\n=== {direction} ({len(group)}) ===", file=sys.stderr)
        print(f"    remedy: {_REMEDY[direction]}", file=sys.stderr)
        if direction == UNCHECKED:
            for lineno, head, info, stmts, parses in group:
                first = " ".join((stmts[0] if stmts else "").split())[:80]
                note = f"{len(parses)} of {len(stmts)} parse as Frame-QL" if stmts else "empty"
                print(f"  L{lineno:<5} §{head[:34]:36} fence={info:18} {note}\n"
                      f"        {first}", file=sys.stderr)
        else:
            for _d, lineno, head, kind, stmt, why in group:
                one = " ".join(str(stmt).split())[:88]
                print(f"  L{lineno:<5} §{head[:34]:36} [{kind}]\n        {one}\n        -> {why}",
                      file=sys.stderr)

    if excluded:
        print(f"\n=== EXCLUDED ({len(excluded)}) — declared out of scope, not invisible ===",
              file=sys.stderr)
        for lineno, head, kind, why in excluded:
            print(f"  L{lineno:<5} \u00a7{head[:34]:36} fence={kind:18} {why}", file=sys.stderr)

    if args.verbose:
        for lineno, head, kind, stage, outcome, reason, stmt in rows:
            print(f"  L{lineno:<5} {kind:18} {stage:8} {outcome:9} {reason or '':24} "
                  f"{' '.join(stmt.split())[:52]}")

    # BLOCKS AND STATEMENTS ARE COUNTED SEPARATELY, and unchecked blocks are on the headline. The old
    # line reported statements only ("40 total"), and 44 blocks minus 9 skipped plus 5 multi-statement
    # extras happened to land near it, so the nine were invisible in the one line anyone reads.
    n_exceeds = sum(1 for f in failures if f[0] == EXCEEDS)
    n_improved = sum(1 for f in failures if f[0] == IMPROVED)
    print(f"manual FrameQL: {blocks_seen} blocks ({blocks_checked} checked, {len(unchecked)} UNCHECKED) "
          f"-> {stmts_seen} statements — {counts['shipped']} shipped, {counts['roadmap']} roadmap, "
          f"{counts['illformed']} ill-formed, {counts['schematic']} schematic, "
          f"{counts['fragment']} fragment, {counts['retired']} retired, "
          f"{counts['metasyntax']} metasyntax; {counts['cml']} cml block(s) excluded "
          f"| operators: {len(op_named)} named+registered, {len(op_unnamed)} registered-unnamed "
          f"| drift: {n_exceeds} claim-exceeds-build, "
          f"{n_improved} capability-improved, {len(unchecked)} unchecked")
    if args.report:
        return 0
    return 1 if (failures or unchecked) else 0


if __name__ == "__main__":
    sys.exit(main())

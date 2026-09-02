#!/usr/bin/env python3
"""gates.py — the one gate runner. CI invokes it; a local complete sweep invokes it.

    There is one authoritative definition of the required gate set. CI and local complete
    sweeps select from that same authority.  (P1-30, ruled Huayin 2026-09-02)

`scripts/gates.toml` is that authority. This file only reads it, runs what it names, and — with
`--verify` — enforces that no workflow reaches around it.

WHY A RUNNER AND NOT A MAKEFILE. A Makefile listing the same commands would be a second enumeration,
free to drift from the workflows in the direction that hurts: a gate added to CI and not to the file
makes the local sweep quietly incomplete, which is the defect (P1-30) rather than the fix. The
property that matters is not that the list exists, it is that **CI EXECUTES FROM IT** — the workflow
step is `python scripts/gates.py --gate <id>`, so a gate absent from the manifest does not run in CI
either, and the two cannot hold different opinions about the required set.

SILENT OMISSION IS THE FAILURE MODE, so `--local` never just skips. Every gate it cannot run is
printed with the reason, and the exit banner says how many were skipped. A sweep that quietly ran 22
of 25 and reported green is what this exists to prevent — it is what happened twice on 2026-09-02.

Usage:
  python scripts/gates.py --local                run every locally-runnable gate; report the rest
  python scripts/gates.py --gate <id> [...]      run specific gates (what CI steps call)
  python scripts/gates.py --workflow docs.yml    run every gate a workflow owns
  python scripts/gates.py --list                 print the manifest
  python scripts/gates.py --verify               the meta-gate (see `verify` below)
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts" / "gates.toml"
WORKFLOWS = ROOT / ".github" / "workflows"

try:
    import tomllib
except ModuleNotFoundError:                                    # pragma: no cover - py<3.11
    import tomli as tomllib                                    # type: ignore

#: Scripts that ARE gates. The meta-gate fails if a workflow invokes one of these directly instead
#: of through this runner. Derived from the manifest itself, so it cannot fall out of step with it.
_SCRIPT_RE = re.compile(r"(?:scripts|docs/tools|services/ask/ask)/[A-Za-z0-9_]+\.py")


def load() -> dict:
    return tomllib.loads(MANIFEST.read_text(encoding="utf-8"))


def _validate(m: dict) -> list[str]:
    """Manifest coherence. A malformed row is a gate nobody runs, which is the failure this file is
    about — so it is an error here rather than a surprise later."""
    errs, seen = [], set()
    for g in m.get("gate", []):
        gid = g.get("id")
        if not gid:
            errs.append("a [[gate]] has no id")
            continue
        if gid in seen:
            errs.append(f"duplicate gate id {gid!r}")
        seen.add(gid)
        if not g.get("cmd"):
            errs.append(f"{gid}: no cmd")
        if not g.get("workflow"):
            errs.append(f"{gid}: no workflow — the meta-gate cannot check an unowned gate")
        if g.get("local") is None:
            errs.append(f"{gid}: `local` is required; a gate must say whether it runs off-CI")
        if g.get("local") is False and not g.get("skip_reason"):
            errs.append(f"{gid}: local = false with no skip_reason. A gate the local sweep omits "
                        f"must say why, every time.")
        for need in g.get("needs", []):
            if need not in {s["id"] for s in m.get("setup", [])}:
                errs.append(f"{gid}: needs unknown setup {need!r}")
    return errs


def _run(cmd: str, env: dict | None = None) -> int:
    return subprocess.run(cmd, shell=True, cwd=ROOT,
                          env={**os.environ, **(env or {})}).returncode


def preflight() -> list[str]:
    """What the gates assume about the environment, checked ONCE and up front.

    Without this, a sweep run outside the project venv fails ten unrelated gates — ruff, pytest, the
    manual gate, the currency guard — and the honest reading of that screen is "the tree is broken",
    which is wrong and expensive. The gates use the environment's tools ON PURPOSE (that is what CI
    does), so the environment is a precondition, and an unmet precondition should be stated once
    rather than discovered ten times."""
    import shutil
    missing = []
    for tool in ("python", "pytest", "ruff"):
        if shutil.which(tool) is None:
            missing.append(f"`{tool}` is not on PATH")
    if shutil.which("python"):
        rc = subprocess.run("python -c 'import columna_core'", shell=True, cwd=ROOT,
                            capture_output=True).returncode
        if rc != 0:
            missing.append("`columna_core` is not importable — the doc and manual gates plan real "
                           "queries against the shipped package and cannot run without it")
    return missing


def run_gates(gates: list[dict], setups: list[dict], skipped: list[dict]) -> int:
    done_setup: set[str] = set()
    by_id = {s["id"]: s for s in setups}
    failed: list[str] = []

    for g in gates:
        for need in g.get("needs", []):
            if need in done_setup:
                continue
            s = by_id[need]
            print(f"\n\033[1m── setup: {need}\033[0m — {s.get('note','')}", flush=True)
            if _run(s["cmd"]) != 0:
                print(f"   SETUP FAILED: {need}. Gates needing it cannot be judged.")
                failed.append(f"setup:{need}")
            done_setup.add(need)

        tag = "report" if g.get("kind") == "report" else "gate"
        net = "  (network)" if g.get("network") else ""
        print(f"\n\033[1m── {tag}: {g['id']}\033[0m{net}\n   $ {g['cmd']}", flush=True)
        rc = _run(g["cmd"])
        if rc != 0 and g.get("kind") != "report":
            failed.append(g["id"])
            print(f"   \033[31mFAILED\033[0m ({g['id']}, exit {rc})")

    print("\n" + "=" * 96)
    ran = len(gates)
    if skipped:
        # LOUD, ALWAYS. A sweep that omits gates without saying so reports a green it did not earn.
        print(f"NOT RUN HERE — {len(skipped)} gate(s) need CI's environment:")
        for g in skipped:
            print(f"  · {g['id']}\n      {g['skip_reason']}")
    if failed:
        print(f"\nGATES FAILED — {len(failed)} of {ran} run: {', '.join(failed)}")
        return 1
    print(f"\nALL {ran} GATE(S) RUN HERE PASSED"
          + (f" — {len(skipped)} deferred to CI, listed above." if skipped else "."))
    return 0


def _run_bodies(text: str) -> list[str]:
    """Every `run:` body in a workflow, and nothing else.

    Parsed by indentation rather than grepped, because grepping lines produced three false positives
    on the first attempt: a trailing `# for scripts/assert_pypi_versions.py` comment on a `uses:`
    line, and a script name quoted inside an error MESSAGE. A guard that cries wolf on prose gets
    silenced, so it has to read only what actually executes."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\s*)(?:- )?run:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        indent, rest = len(m.group(1)), m.group(2).strip()
        if rest and rest not in ("|", ">", "|-", ">-", "|+"):
            out.append(rest)                                   # inline form
            i += 1
            continue
        i += 1                                                 # block scalar
        block = []
        while i < len(lines):
            nxt = lines[i]
            if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                break
            block.append(nxt)
            i += 1
        out.append("\n".join(block))
    return out


def _strip_comments(body: str) -> str:
    """Shell comments inside a run body are prose too."""
    return "\n".join(re.sub(r"(?<!\S)#.*$", "", ln) for ln in body.splitlines())


def verify(m: dict) -> int:
    """THE META-GATE. A workflow may not invoke a known gate script outside this authority.

    Two directions, and both matter:

      1. A workflow `run:` that calls a gate script directly is a gate CI runs and the manifest does
         not know about — so the local sweep is incomplete again and nothing says so. This is the
         exact shape of P1-30 and it is what the check exists to refuse.
      2. A manifest gate whose owning workflow never invokes it is a gate that runs NOWHERE while
         appearing, to any reader of the manifest, to be covered. A row that outlives its invocation
         is worse than no row: it reads as coverage.

    Deliberately NOT a check that the workflow text matches the cmd. That would pin formatting and
    fail on a legitimate rewording, which trains people to edit the guard to make it quiet.

    `[[allow]]` is the escape hatch, and it is narrow ON PURPOSE: a gate script used as a DATA SOURCE
    rather than as an assertion (website.yml reads `release_pins.py` for its pin string) is a real
    and legitimate use that the pattern cannot distinguish. Each one is enrolled by hand with a
    reason, exactly like `skip_reason` — coverage grows by a named entry, never by the guard quietly
    deciding something looked fine."""
    errs = _validate(m)
    gates = m.get("gate", [])
    known_scripts = {s for g in gates for s in _SCRIPT_RE.findall(g["cmd"])}
    allowed = {(a["workflow"], a["script"]) for a in m.get("allow", [])}
    runner = "scripts/gates.py"

    for wf in sorted(WORKFLOWS.glob("*.yml")):
        for body in _run_bodies(wf.read_text(encoding="utf-8")):
            for line in _strip_comments(body).splitlines():
                if runner in line:
                    continue
                for script in sorted(known_scripts):
                    if script == runner or script not in line:
                        continue
                    if (wf.name, script) in allowed:
                        continue
                    errs.append(
                        f"{wf.name} invokes `{script}` directly:\n"
                        f"        {line.strip()[:110]}\n"
                        f"      A gate CI runs outside scripts/gates.toml is a gate the local sweep "
                        f"does not know exists. Add it to the manifest and call it through "
                        f"`python scripts/gates.py --gate <id>`, or enrol it as [[allow]] with a "
                        f"reason if it is a data read rather than an assertion.")

    wf_text = {wf.name: wf.read_text(encoding="utf-8") for wf in WORKFLOWS.glob("*.yml")}
    #: `--gate a b c` runs three gates in one step, so look for the ID as a TOKEN after `--gate`,
    #: not for the literal string `--gate <id>`. The first version missed exactly that and reported
    #: a wired gate as unwired.
    invoked: dict[str, set[str]] = {}
    for name, text in wf_text.items():
        ids: set[str] = set()
        for mt in re.finditer(r"--gate\s+((?:[A-Za-z0-9_-]+\s*)+)", text):
            ids.update(mt.group(1).split())
        invoked[name] = ids

    for g in gates:
        wf = g.get("workflow")
        if wf and wf not in wf_text:
            errs.append(f"{g['id']}: names workflow {wf!r}, which does not exist")
        elif g.get("runner") is False:
            # CI INVOKES THIS ONE DIRECTLY, ON PURPOSE — but it must say why, and the direct call
            # must be enrolled, so "exempt" can never be reached by simply omitting a field.
            if not g.get("runner_reason"):
                errs.append(f"{g['id']}: runner = false with no runner_reason.")
            if not any(a["workflow"] == wf and a["script"] in g["cmd"] + " " + g["id"]
                       or (a["workflow"] == wf and a["script"] in g["cmd"])
                       for a in m.get("allow", [])):
                errs.append(f"{g['id']}: runner = false, but no [[allow]] enrols its direct "
                            f"invocation in {wf}. The exemption must be visible from both sides.")
        elif wf and g["id"] not in invoked.get(wf, set()):
            errs.append(f"{g['id']}: manifest says {wf} owns it, but {wf} never runs it through the "
                        f"runner. A gate that runs nowhere still reads as coverage.")

    for a in m.get("allow", []):
        if not a.get("reason"):
            errs.append(f"[[allow]] {a.get('workflow')}/{a.get('script')}: no reason given")

    if errs:
        print(f"META-GATE FAILED — {len(errs)} finding(s):\n")
        for e in errs:
            print(f"  \u00b7 {e}\n")
        return 1
    print(f"meta-gate OK — {len(gates)} gate(s), every one invoked through the runner by the "
          f"workflow that owns it; {len(allowed)} enrolled non-gate use(s); no workflow reaches "
          f"around the manifest.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--local", action="store_true", help="every locally-runnable gate")
    ap.add_argument("--gate", nargs="+", metavar="ID", help="specific gate ids")
    ap.add_argument("--workflow", metavar="FILE", help="every gate a workflow owns")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--verify", action="store_true", help="the meta-gate")
    a = ap.parse_args()

    m = load()
    gates, setups = m.get("gate", []), m.get("setup", [])

    if a.verify:
        return verify(m)

    errs = _validate(m)
    if errs:
        print("MANIFEST INVALID:\n" + "\n".join("  · " + e for e in errs))
        return 2

    if a.list:
        for g in gates:
            where = "local+CI" if g.get("local") else "CI only"
            print(f"  {g['id']:24} {where:9} {g['workflow']:12} {g['cmd'][:60]}")
        return 0

    if a.gate:
        by_id = {g["id"]: g for g in gates}
        unknown = [x for x in a.gate if x not in by_id]
        if unknown:
            print(f"unknown gate id(s): {', '.join(unknown)}")
            return 2
        return run_gates([by_id[x] for x in a.gate], setups, [])

    if a.workflow:
        sel = [g for g in gates if g["workflow"] == a.workflow]
        if not sel:
            print(f"no gates own workflow {a.workflow!r}")
            return 2
        return run_gates(sel, setups, [])

    if a.local:
        problems = preflight()
        if problems:
            print("ENVIRONMENT NOT READY — the gates run the environment's tools, as CI does:\n")
            for x in problems:
                print(f"  \u00b7 {x}")
            print("\n  Activate the project venv and install the packages, e.g.\n"
                  "      pip install -e 'packages/columna-core[test]' -e packages/columna-server ruff\n"
                  "\n  Refusing to run rather than reporting ten unrelated failures.")
            return 2
        return run_gates([g for g in gates if g.get("local")], setups,
                         [g for g in gates if not g.get("local")])

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

# CP-2.x — KP v0.3 salience edit: DRAFT for ratification (the first measured iteration)
**From: Claude Code, 2026-07-16. The single-variable edit Huayin ruling 5 authorized: a salience
treatment for the four Columna-native doctrines. EXACT prompt text below; nothing goes live until
Huayin ratifies (the KP is frozen under the copy law — changes only by ruling). Run 5 then measures
v0.3 against the run-4 baseline, same benchmarks, scorer 0.4 (with the run-4 closure axis re-rendered
under 0.4 per ruling 5, foldable into the same keyed session).**

---

## The finding this edit acts on (ruling 1, canonical statement — for the record and the capture)
> **The mind surfaces what pretraining taught and stays silent on what only the KP teaches.**

Run-4 evidence, sharpened: the seven ◆ benchmarks split cleanly by doctrine origin.
- **Surfaced (3/7)** — `basis` (B1, B10) and `universe` (B3): general-pretraining doctrines.
- **Silent (4/7)** — `additivity` (B2), `m-leak` (B4), `fertility` (B8), `refutation` (B11): the four
  **Columna-native** doctrines. (M-leak reclassifies here — the design session's original filing was
  wrong; the mind's behavior drew the truer boundary.)

**The fulcrum: naming is not salience.** `m-leak` is **already named** in the live v0.2 prompt
("basis type … universe assignment … **M-leaks**") — and it went **silent anyway**. So the edit cannot
be "list them"; a listed native call already failed. The treatment must give the native four the
retrieval scaffolding the pretrained two get for free: a **concrete observable trigger** each, cued off
what the aperture can actually show, plus an explicit mark that these are *not in the mind's default
repertoire* so it reaches for them deliberately.

---

## THE EDIT — one block, replacing the single sharp-calls sentence in `system_prompt.md`
**Remove** (live v0.2, lines 23–24):
> The sharp calls — make EXPLICIT in the review checklist, and keep it SHORT: basis type (events vs
> spine), universe assignment, M-leaks. Do not flood the checklist.

**Insert** (exact text):
> The sharp human calls — surface each as an explicit `<category>: <call>` line in the review checklist,
> and keep the checklist SHORT: do not flood it.
>
> Two you will already reach for from general practice — surface them when they apply:
> **basis** (events vs spine — is absence a zero or a gap?) and **universe** (a table serving more than
> one population).
>
> Four are **COLUMNA-NATIVE — not in your default repertoire.** You will not volunteer them by habit,
> and the machine cannot make them for you, so reach for each DELIBERATELY, cued off something you can
> see. Naming them is not enough — fire each one *whenever its trigger appears*:
> - **additivity** — for every MEASURE you propose: is its value summable across all its levels? Trigger:
>   an average, ratio, rate, or snapshot is NON-additive — say which, on the measure's first review line.
> - **m-leak** — a measurement whose value leaks BEYOND its key. Trigger: a pre-aggregated column name
>   (`avg_*`, `*_rate`, `*_pct`) or a value residing in a rollup/summary table rather than at the fact grain.
> - **fertility** — a member that MAY be theorem-fertile. You never open it; you FLAG it for the human.
>   Trigger: a ratio/derived you propose — note it may be fertile and leave the declaration to the human.
> - **refutation** — the SAMPLE contradicts a CATALOG claim. Trigger: a declared-unique column carrying
>   duplicates, or a declared FK whose key maps to two parents — surface the conflict and propose the
>   honest alternative (a RELATE, or a flagged degraded edge).

---

## Why this is ONE variable (the discipline)
- **Only salience moves.** basis/universe wording is preserved (they already surface — don't perturb the
  control). The **concentration** clause ("keep the checklist SHORT: do not flood it") is carried verbatim
  in intent — no concentration coaching is added or removed. The output contract (KP v0.2), grades,
  polarity, the loop law, and §B skill notes are **untouched**.
- **The v0.2 no-enumerate restraint is lifted for exactly these four native doctrines — deliberately.**
  That restraint existed to keep the *baseline* ◆-recall readable (a listed category is coached recall).
  The baseline is captured (run 4); enumeration is now the measured treatment, not baseline contamination.
- **Salience ≠ tag-parroting.** Each native call is cued to an OBSERVABLE, so it fires on the benchmark
  where its trigger exists (B2/B4/B8/B11) and not everywhere. If the mind instead floods all four onto
  every benchmark, ◆-recall rises but the concentration axis (max_checklist 2 on the ◆ set) catches it —
  the instrument discriminates real salience from noise; that trade is data, not a bug.

## The falsifiable prediction run 5 tests (measure-then-adjust)
1. **B2/B4/B8/B11 flip `explicit✓`** → salience treatment works; ◆-explicitness rises from 3/7 toward 7/7.
2. **The M-leak crux:** B4 was NAMED in v0.2 yet silent. If B4 now surfaces under a *trigger* (not just a
   name), that is the clean confirmation that **salience is scaffolding, not naming**. If B4 stays silent
   even with its trigger, the hypothesis needs refining (the native doctrines may resist a prompt-only fix).
3. **Watch the concentration axis** on the ◆ set — a real salience gain surfaces the RIGHT call on the
   right benchmark without flooding; a spurious one trades ◆-recall for a flooded checklist.
4. **The controls (basis/universe, B1/B3/B10) must NOT move** — if they shift, the edit leaked beyond its
   one variable and the run is not like-with-like.

## Queue behind this (one at a time, each against the recorded baseline)
`flooding` (concentration) → then `revise-discipline` (the struck-re-proposal, ruling-4-confirmed as a
mind finding). Neither moves until salience is measured and ruled on.

---
**Status: RATIFIED AS WRITTEN & LIVE (Huayin, 2026-07-16).** The exact insert text is now in
`columna_server/init/system_prompt.md` (KP v0.3), replacing the v0.2 sharp-calls sentence; everything
else in the KP is unchanged. Under the copy law, §A/this block change only by ruling. Run 5 is the
causal test: a CONTROL arm on KP **v0.2** (retrieved from git) and a TREATMENT arm on KP **v0.3** (live),
both under scorer 0.4, same model + benchmarks in one keyed session — the single variable is the prompt.
This subsumes the run-4 re-render provision: the v0.2 arm IS the like-with-like baseline under 0.4
(run-4's own proposals were never captured; a fresh v0.2 arm is the clean control). B10's
proposal-vs-ground-truth evidence is captured from run 5 into specs per the evidence-retention rule.
Run 5 fires on the standing key-and-go.

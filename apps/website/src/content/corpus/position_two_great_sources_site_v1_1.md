# The Two Great Sources of Silent Analytical Failure

*A position held by datumwise · July 2026 · v1.0. The
site edition of the research paper of the same name — same argument, same
evidence, linked instead of cited. The paper of record lives on Zenodo
(doi:10.5281/zenodo.21553379). All
empirical claims herein are checkable against the frozen, published benchmark kit.*

## The claim, in one breath

Silent analytical failure — a confidently served number that is wrong in a way
nothing in the serving system records — is usually treated as a grab-bag of
pitfalls: fan-outs, stale rollups, averaged averages, missing rows. We argue the
bag has structure. Every silent failure is the unrecorded resolution of a name
across a degree of freedom, and the freedoms number four: which aggregation
lineage (the anchor freedom), which data territory and passage (the universe
freedom), which population boundary (the coverage freedom), and which moment of
truth (the freshness freedom). The first two are structurally deep: no amount of
per-answer honesty fixes them, because the failing operations must be refused or
licensed by law, not caveated. The last two are bookkeeping: disclosure suffices.
Sorting the fourteen defect classes of a public text-to-SQL honesty benchmark
under these headings places nine of fourteen in the two deep freedoms; a
nine-model study over that benchmark shows the deep classes failing identically
across vendors and scales, unmoved by better documentation. We conclude that the
defense against silent failure must be architectural in exactly two places — an
anchor algebra and a frontier algebra — and honest bookkeeping everywhere else.

## 1. The root event: a name, silently bound

Ask a data system for "average order value." Between the name and the number, a
chain of resolutions occurs: which population counts as an order; which lineage
of aggregation produces "average"; which rows are present to be averaged; which
snapshot of the warehouse answers. In healthy human analysis these resolutions
are argued about. In automated serving — and acutely in AI-agent serving — they
are made instantly, silently, and confidently. The failure is never the
arithmetic; it is that a resolution occurred and nothing recorded it.

This much is folklore. The contribution of this paper is that the space of
resolutions is small and structured: four degrees of freedom, of unequal depth.

## 2. The four freedoms

**F1 — the anchor freedom (which lineage).** A measure carries an input grain
(what its rows mean) and an output anchor (what re-aggregations remain lawful).
Averaging monthly averages, summing a stock snapshot across time, re-counting a
distinct: each silently substitutes an unlawful lineage for a lawful one.
Formalized in "The Two Anchors of a Measure".

**F2 — the universe freedom (which territory, which passage).** A warehouse is a
federation of universes — maximal territories of functional (M:1) reachability.
Within a territory, meaning composes; between territories, it does not, unless a
passage is declared. Two passages exist: alignment at a shared grain, and
crossing through a declared face over an M:N frontier. Every fan-out
double-count, every ETL-buried "weighting factor," every primary-category picked
by an unrecorded rule is an attempt at a third passage that does not exist.
Formalized in the companion paper on multi-universe processing.

**F3 — the coverage freedom (which population boundary).** Rows absent, members
unmapped, missingness that is itself informative: the served population silently
narrows or shifts relative to the named one.

**F4 — the freshness freedom (which moment of truth).** Derived truth stored as
data — the stale rollup, the summary table — serves yesterday's world under
today's name.

## 3. Depth: why two of the four are different in kind

F3 and F4 are bookkeeping freedoms. Their honest treatment is disclosure: state
the coverage shortfall on the answer; state the snapshot's age; reject the stale
source by name. Nothing about the *operation* is unlawful — only unstated.

F1 and F2 are structural freedoms. Their honest treatment cannot be disclosure,
because the failing operations have no correct disclosed form: a stock snapshot
summed across a year is not "a number plus a caveat" — it is not a number; a
revenue total pushed through an undeclared M:N mapping is not "approximately by
category" — it answers no declared question. The lawful responses are refusal
(the operation is undefined here), clarification (several lawful resolutions
exist — choose), or a licensed, named operation whose law travels with the
answer. That demands machinery: an algebra of anchors and families governing F1;
an algebra of universes, frontiers, and faces governing F2. Vigilance — human
review, better prompts, more documentation — is a bias, not a guarantee, and the
empirical record below shows it failing uniformly.

## 4. The evidence: sorting a public benchmark's defects

The Ground Truth benchmark plants fourteen defect classes in a synthetic
warehouse and asks nine frontier AI models 111 questions over it, single-shot,
against well-documented schemas. The classes sort as follows.

| Freedom | Planted defect classes | Count |
|---|---|---|
| F1 anchors | mule_reaggregation · distinct_reaggregation · semi_additive_sum · empty_bucket · ambiguity/stated_resolution (definition choice) | 5 |
| F2 universes | fan_trap · m2m_overlap · conservation_leak · fd_violation | 4 |
| F3 coverage | coverage_gap · missing_values · mnar_missingness | 3 |
| F4 freshness | stale_source | 1 |

Nine of fourteen classes are the two deep freedoms — and the two are precisely
where the nine-model study found entire failure families failing *identically*
across vendors and scales, unmoved by more documentation (the schemas were
well-documented by construction; the models read them; the deep classes failed
anyway). The shallow freedoms, by contrast, are where models most often *knew*
the hazard: the study's sensitivity analysis found large fractions of nominal
"silent" failures were honest hazards filed under mismatched labels — an honesty
of bookkeeping already half-present in the models, needing only a contract to
land in. The deep freedoms exhibited no such latent honesty: the operations were
simply performed.

## 5. The architectural corollary

If silent failure has exactly two deep sources, a system built to make silent
failure structurally impossible should have exactly two heavy subsystems — and
the shape of Columna, the open-source framework these papers accompany, confirms
the taxonomy retroactively: an anchor/family algebra (measures declaring
lineages; unlawful lineages blocked, not caveated) and a universe/face algebra
(territories carved by functional structure; frontiers crossable only through
declared, adjudicated faces). Everything else the system does for honesty —
absence disclosures, freshness caveats, provenance rejects — is deliberately
light: bookkeeping, done in the open. The four response moods align the same
way: refuse and clarify are the voice of structure (F1, F2); disclose is the
voice of bookkeeping (F3, F4); serve is the mood of no unresolved freedom. And
the two deep freedoms are not merely siblings: the companion paper shows they
interlock — the frontier is where anchors are spent, rewritten, or certified —
so the two heavy subsystems are, at the boundary, one machine.

## 6. Related practice

Dimensional modeling's conformed dimensions are F2's alignment passage,
maintained by convention; its bridge tables with weighting factors are F2's
crossing, performed without law. Semantic layers catalog names but compile to
engines that cannot refuse, leaving all four freedoms resolvable downstream.
Data contracts and tests patrol F3 and F4 well — the bookkeeping freedoms — and
are structurally silent on F1 and F2, which is this paper's explanation of why
well-tested warehouses still produce two irreconcilable revenue dashboards.

## 7. The bottom of the bag

The bag of pitfalls has a bottom. Four freedoms; two deep. The deep two cannot
be fixed by care, documentation, or review — the benchmark's nine models,
reading good documentation, failed them in unison — and must be fixed by
structure: an algebra that refuses, clarifies, or licenses. The shallow two need
only honesty at the point of answer. A serving system that implements the deep
algebras and the shallow disclosures leaves silent failure nowhere to live; the
reference implementation, its benchmark, and every number in this paper are
public and re-runnable.

*Correspondence: contact@datumwise.ai. The benchmark kit, including the frozen
answer key, raw model answers, scoring driver, and errata, is published in full.*

---

*Evidence, one click each: [the Two Anchors paper](https://doi.org/10.5281/zenodo.20789318) ·
[Multi-Universe Processing](https://doi.org/10.5281/zenodo.21543584) ·
[the Silent Failure Atlas](https://doi.org/10.5281/zenodo.20762839) ·
[the nine-model study](https://doi.org/10.5281/zenodo.21349581) ·
[the public benchmark kit](https://github.com/datumwise/ground-truth-benchmark) ·
[the case study](/case) · and the demo: `pip install columna`.*

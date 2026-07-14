# datumwise.ai — the homepage as argument
**draft v0.2 (cold-read approved, Huayin edits applied) · full scroll, section by section · copy is verbatim-intent; [bracketed] blocks are design/build annotations**

---

[AMBIENT CHROME — persists through the entire scroll]
- Masthead: "datumwise" wordmark, small. Nav, quiet, right-aligned: The Thesis · Why · The Atlas · Run the audit · GitHub. Nothing else.
- Persistent affordance, bottom-right, small and calm (not a banner): a monospace chip reading
  `pip install columna-core columna-server` with a copy icon and the caption "run it — two minutes."
  Visible at every scroll position. This is the door that must always be at hand.
- No hero image. No illustration anywhere on this page. Type, tables, and wire JSON only.

---

## §1 — The opening line

[Full viewport. One sentence, set large, serif. Subline smaller. Nothing else above the fold except the ambient chrome.]

# A number owes you its assumptions.

Most numbers don't pay. They arrive alone — clean, confident, formatted — and the choices that
made them stay behind. For fifty years that was survivable, because the numbers were made by
people, and people argue. Now the numbers are made by machines that never argue at all.

This page is one argument, top to bottom. It will take about eight minutes, and twice along the
way you will watch it run.

[Scroll cue: a thin rule and the words "begin with ninety seconds of data." ]

---

## §2 — Exhibit A: the ninety seconds

[EXHIBIT — interactive. The table renders as a real table, monospace numerals. Beneath it, three
buttons: "÷ line items" · "÷ orders" · "÷ customers". Clicking one animates the division and
prints the answer large. All three answers persist once revealed, side by side. Static fallback:
all three shown. This is the grain-gap demo compressed; link at the section's end goes to the
full article.]

Here is a quarter of sales. The whole thing:

| order | customer | line items |
|---|---|---|
| O1 | Ada | $100, $20 |
| O2 | Ada | $10 |
| O3 | Ben | $40, $40, $40 |

Revenue is $250. Now answer an ordinary question: **what was our average order value?**

Divide by the six line items: **$41.67**. Divide by the three orders: **$83.33**. Divide by the
two customers: **$125.00**.

Same data. Same three words. Three answers — and none of them is wrong. They differ only in what
you divided by, and *what you divided by* is a decision the question never stated, the column
name never records, and whatever answered you made silently on your behalf.

Ask an AI analyst this question and you will get one of these numbers in less than a second, with a
chart, a citation, and no flicker of doubt. Not a hallucination — the SQL is valid, the number is
real. Something quieter and worse: **a defensible wrong answer.** The kind no guardrail catches,
because by every check anyone has built, it's correct.

You have just seen the whole problem. The rest of this page is why it exists — and it goes
deeper than you think.

[Link, small: "the full ninety-second version → The Grain Gap"]

---

## §3 — What data is

[Register shift: this section and the next two are set in the serif, essay-width measure,
generous leading. The reader should feel the page change from demo to argument.]

Start further back than this industry usually starts — not at the tool, not at the query
language, but at what data *is*.

**Every datum is something said about something else.** A value, said *of* something. The
measure is what is said; the anchor — the set of coordinates it is said at — is what it is said
of. A **column** is a measure over its anchor. Not the smallest element of data — a data point
is — but the simplest *structure* of data: the atom of structured data operation.

And a table? A table is a container. Form, not substance. Its keys and layouts *hint* at meaning
— but hints are not declarations, and nothing checks them. This is why fifty years of table
operations have been necessarily *mechanical*: you can only do mechanical things to a container,
because a container has no aboutness to respect. Operations over columns are *substantial* —
they must honor what the column says, and what it is said of.

**Tables are how data is stored. Columns are what data says.**

Your average-order-value question went wrong exactly here. The answer had to be computed *over*
something — lines, orders, customers — and that "over" is a property of the column, not of the
table it happened to be stored in. The table couldn't tell you. Tables can't. It isn't their job.

---

## §4 — The grammar that was never written

Half a century ago — Codd, 1970 — the container got its mathematics. Relational algebra —
select, project, join — closed over tables, indifferent to meaning. It was a genuine triumph,
and it built everything you use. But it is an algebra of *form*.

The substance side got theorems, never a grammar. The warnings have been in the literature for
decades — summarizability theory (Lenz & Shoshani, 1997) stated precisely when a rollup is lawful;
a generation of OLAP tools shipped semi-additive behaviors; newer modeling languages disarm
particular traps, one feature at a time. Real fragments — conditions to check, settings to enable,
disciplines to remember — and never a constitution: one small, closed algebra in which legality
*follows* from what the columns are, every expression adjudicated before it runs, refusal spoken
out loud. The great rebellion against the table — key-value, objects, documents, graphs — reached
for substance and won everywhere retrieval rules. But it won everywhere **except where structured
data live**: the moment the workload turned analytical, every rebel surrendered back to SQL, or
bolted on a map-reduce with no theory of legality at all. Structured analytical data stayed the
container's last kingdom — not because tables are right for it, but because the fragments never
became a grammar.

So we wrote the grammar. The framework is called **Columna**, and the name is the thesis: it stands for
**Column Algebra**. Columns and their operators — mappers and reducers — composing into
expressions; some grammatically well-formed, some not; and the line between them drawn by the
*nature* of each column, captured in three anchors: where its values live, where they leak and
by what mechanism, which directions of reduction are barred. From these, legality *follows*.
Whether you may sum this, roll that up, divide these two — not policy, not convention, not a
style guide.

---

## §5 — Two kinds of metadata

Here is the part the industry will recognize, because it has been paying for the confusion for
decades.

Metadata was never one thing. Some of it is **load-bearing**: change it and you change what
operations are legal, or what value results — which unit an average reduces over, which
population a count is drawn from. And some is **communicative**: it exists so that a person — or
now a model — can understand. The test is decidable, not aesthetic: *does changing it change
legality or value?*

For fifty years the two kinds lived fused — some in schema structure, some baked into column
names, some in documentation, and the decisive remainder in the analyst's mind. Because the
load-bearing kind had no home, the industry forced *names* to carry it — ARPU forks into ARPPU
because a denominator had nowhere else to live — and then built a governance regime to police
the names, and called it the semantic layer. Look closely: **it was never semantic.** It was
correctness wearing meaning's clothes — and therefore frozen. Governance solves drift. It cannot
solve ambiguity. You cannot decree your way out of a grain.

Language solved this before we were born: grammar decides well-formedness independent of meaning,
and that autonomy is what makes language both checkable and infinitely expressive. Data deserves
the same constitution. Put correctness in the **grammar layer** — the algebra above: small,
closed, machine-checkable. The moment it has a home, meaning is demobilized: names become pure
communication — colloquial, translated, plural, generated — because nothing operational rides on
a string anymore.

Codd separated logical from physical and called it data independence. This is the sequel:
**metadata independence** — meaning separated from correctness so each can finally do its job.
One inversion, two liberations.

---

## §6 — The stakes: the analyst who never hesitates

Now return to the machine that answered in a second.

A language model is a semantic engine — magnificent at meaning, constitutionally incapable of
guaranteeing correctness. Hand it today's fused metadata and its greatest strength becomes its
signature failure: it reads `avg_order_value` and *confidently means something by it*. For fifty
years, the argument between human analysts was the safety mechanism — three people with three
numbers is visible disagreement, and visible disagreement gets caught in the meeting. The AI
analyst answers instantly, confidently, singularly. The argument never happens. **The debt came
due the day the analyst stopped being human.**

Split the layers and the model is finally in its element: living entirely in semantics — names,
descriptions, intent, conversation — while every operation it proposes is adjudicated by a
grammar it cannot touch. Hallucination, injection, drift can corrupt only the semantic layer.
**The grammar layer is the blast wall.** The model proposes; the grammar disposes; the human
decides among genuine alternatives.

And the system's answers gain the vocabulary honesty requires — four moods, as structured data:
**serve** the number; **disclose** it with its assumptions attached; **clarify** when the
question admits several legitimate readings; **refuse** what the data cannot answer, with the
reason. "It depends," said precisely, is often the most correct answer there is.

That is a claim about running software. So watch it run.

---

## §7 — Exhibit B: the argument, executed

[EXHIBIT — the four-moods transcript, rendered as wire JSON in monospace, mood-tagged with the
four mood colors (the only saturated color on the page). If the live widget (WP-5.1,
demo.datumwise.ai) is up: an input box seeded with three suggested questions, one per mood-path.
Graceful degrade: the recorded transcript, clearly stamped with its generation date.
INTEGRITY RULE (build-enforced): this transcript is GENERATED IN CI by running
`columna-server demo --play` against the shipped package. It is never hand-edited. A small
caption under the exhibit says exactly that.]

[Caption:] *This transcript is generated by running the shipped package, `columna-server demo
--play`, at build time. It is never edited by hand. What you see is what installs.*

[Beneath the exhibit, one short paragraph:]

The mood you should test first is the one vendors never demo. Ask it for a metric that sounds
plausible and doesn't exist. It will not guess. During our own final pre-launch test, our test
script did exactly that — and the system refused, listed what it *did* have, and asked. The test
marked it as a failure. The test was wrong; the refusal was the only correct answer in the room.
We fixed the test, and we now assert that refusal forever. [Link: "the whole confession → the
launch post."] Vigilance fails — it failed the industry, it failed our own benchmark, it failed
the very test we wrote. **Structure holds.** That is why the defense is an algebra and not a
best practice.

---

## §8 — The three doors

[Closing section. Three columns on desktop, stacked on mobile. Each door is a heading, two
lines, and one action. Nothing salesy; the register stays flat and confident.]

**Run it.** Two minutes, no arguments, no signup. A clarify, a refuse, and a disclose will print
on your machine as real wire JSON.
`pip install columna-core columna-server` → [GitHub / quickstart]

**Read it.** The argument above, at full depth and with its evidence: the Columna Thesis, the
metadata-independence essay, and the papers — every claim one click from its verification.
→ [The Thesis] · [Why] · [how these documents relate]

**Test it.** We keep a public map of the sixty-seven ways a query runs clean and lies — graded
against everyone, including us. If a number has ever lied to you by omission, bring us the
failure mode you witnessed.
→ [The Silent Failure Atlas]

---

[FOOTER]
- Left: "Columna is open source, Apache-2.0. The discipline needs no product — declare your
  anchors, name your populations, refuse out loud what your data cannot answer. Columna is our
  proof it can be made executable."
- Center, small: The Silent Failure Atlas (DOI 10.5281/zenodo.20762839) · The Silent Seam (DOI
  10.5281/zenodo.20710717) · The Two Anchors of a Measure (DOI 10.5281/zenodo.20789318)
- Right, smallest: "datumwise builds and stewards Columna." (The only company sentence on the
  page.)
- Integrity line, full width, hairline rule above: "Every transcript and every number on this
  page is generated at build time by running the shipped package. This site is structurally
  incapable of demoing something it did not ship."

---

# Build notes (not copy)

1. **Register map.** §1–2: sans + monospace, demo energy. §3–5: serif, essay measure — the page
   visibly *becomes* a text. §6–7: serif prose, monospace exhibit. §8–footer: sans. The
   typographic shift IS the information architecture: the reader feels the descent from
   exhibit to argument and back.
2. **The two exhibits are the only interactive elements.** Everything else is text. Resist
   adding a third.
3. **Mood colors** appear exactly twice: Exhibit B tags, and (later) the site agent's replies.
   Never decorative.
4. **Ambient quickstart chip** must never obscure content and never animate. It is a door, not
   a toast.
5. **Length calibration:** ~1,400 words of copy ≈ 7–9 minute read. If cold-reads say it drags,
   §5 compresses first (fold ARPU/ARPPU into one sentence); §3 and §4 are the soul — cut them
   last.
6. **Naming:** "the Columna Thesis" replaces "manifesto" everywhere on the site. "Column
   Algebra" appears once (§4, the name-reveal) and is thereafter "the algebra."
7. **Anchor names (V/M/B) deliberately do not appear on the homepage** — "three anchors" with
   plain-language glosses is the right altitude; the letters live one click down in the docs.
8. **Every section heading is a fragment of the argument**, not a label — the page should read
   as one continuous piece if you read only the headings and bold lines.

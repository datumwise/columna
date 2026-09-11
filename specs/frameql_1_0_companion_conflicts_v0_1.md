# Frame-QL 1.0 — conflicts in the companion works (v0.1)

*Findings only. Filed 2026-09-11 by the Frame-QL 1.0 expression-language unit, Phase 3.*

> **NOTHING WAS EDITED TO PRODUCE THIS FILE.** Every work named below is either a **published,
> DOI-bearing deposit** or a **staged review set whose own README forbids treating it as current
> law**. A published explanatory work does not get rewritten so that it looks current, and a staged
> set does not get amended under a repair mission. Where a text materially conflicts with the adopted
> language, that is reported here for a later **publication revision** to rule on — with the exact
> quote and the exact location, so the revision does not have to re-find it.
>
> This file makes no recommendation about *whether* any of these should change. That is an editorial
> and publication judgement, and it is not this unit's.

## What was checked, and against what

The authority is the adopted **Frame-QL Language Specification, Version 1.0** (2026-09-10), §15
*Grammar and precedence closure*, with §7.5 and §10.4. Three rules of its expression surface moved,
and only those three were looked for:

1. **Precedence.** `@` binds **tighter than arithmetic** and **looser than postfix**, so
   `revenue / orders @ {region}` is `revenue / (orders @ {region})` and `state.cardinality @
   {account}` is `(state.cardinality) @ {account}`. Comparison does not chain.
2. **`=` compares; `:` names an argument** (§15.2). Canonical named arguments are
   `variance(price, ddof: 1)`. The historical `name = value` call spelling is compatibility INPUT and
   canonicalizes to the colon form.
3. **Brackets subscribe; they never filter** (§7.5, §15.4). `revenue[region = "east"]` is not
   analytical filtering, and 1.0 *"supersedes the roadmap recommendation"*. A conforming diagnostic
   points the writer at `WHERE`/`HAVING`.

Trees read: `apps/website/src/content/corpus/**`, `services/ask/deposits/**` (including `supplied/`),
`specs/frameql_v7_1/proposed_adoption/**` and `specs/frameql_v7_1/reviewed_sources/**`,
`registry/publications/**`.

Every quote below was re-read at its cited line before being written here, and every parse claim was
executed against the shipped `columna_core.expr` rather than reasoned about.

**Headline: the published corpus is in good shape.** Of the works served on the site and pinned to
DOIs, only two carry a material conflict, and both are single lines. The concentration is in the
**staged, unpublished** `specs/frameql_v7_1/` set — which is the expected place for it, because that
set was reviewed against ToD v7.1 before §15 was adopted.

---

## A · MATERIAL — the successor language draft classifies `@` as a postfix axis

**Where.** `specs/frameql_v7_1/proposed_adoption/frameql_language_vnext_working_draft_v0_4.md:607`
and the identical body in `specs/frameql_v7_1/reviewed_sources/…v0_4.md:607`.

**Quoted verbatim (L607, and the block it governs, L609–L620):**

> ```
> # 5. The three postfix axes
>
> The language should keep three semantic axes distinct:
>
> E @ A
>     analytical anchoring / location
>
> E.member
> E.method(...)
>     governed semantic-value capability or qualified-name resolution
>
> E[key]
>     semantic-value subscription
> ```

**The conflict.** The section groups `@` with `.member`/`.method(...)`/`[key]` as three co-equal
**postfix** axes. §15 places them on two different rungs, and the gap between them is normative:
postfix binds **tighter** than `@`. That is exactly what makes `state.cardinality @ {account}` mean
`(state.cardinality) @ {account}` and makes `(state @ {account}).cardinality` a different expression
requiring parentheses. A reader who takes the three as one level has no way to derive either fact.

The *semantic* distinction the section draws — three different questions, three different axes — is
untouched by 1.0 and is worth keeping. It is the word **postfix**, and the flat grouping, that now
says something the grammar does not.

---

## B · MATERIAL — the same draft distributes an anchor over a ratio without naming the precedence

**Where.** `…/frameql_language_vnext_working_draft_v0_4.md:515–527` (both copies).

**Quoted verbatim:**

> ```
> ## 4.4 Pointwise anchoring
>
> For a pointwise expression:
>
> revenue / orders
>
> anchoring at `region` has the intended reading:
>
> (revenue @ {region}) / (orders @ {region})
> ```

**The conflict.** The *parenthesized* target form is correct under 1.0 and is not at issue. What is
at issue is that the section teaches "anchoring `revenue / orders` at `region`" as a property of the
bare expression, and never shows the unparenthesized surface. Under §15 the natural way a reader
writes that sentence down —

    revenue / orders @ {region}

— means `revenue / (orders @ {region})`: the **denominator** is anchored, and the numerator is not.
The document contains no warning, and the two readings differ numerically. Verified against the
shipped parser:

    expr.parse("revenue / orders @ {region}")
      -> Binary(/, Path(revenue), Anchor(Path(orders) @ {region}))

This is the single most consequential gap in the set, because it is the one place where a reader
following the published text can write a query that serves a wrong number rather than one that fails.

---

## C · MATERIAL — a staged disposition records the bracket question as still OPEN

**Where.** `specs/frameql_v7_1/proposed_adoption/PATCH_SHEET_DISPOSITIONS.md:23`.

**Quoted verbatim:**

> | 10 | bracket roadmap withdrawal | **not applied — question remains OPEN** | retiring a roadmap construct is a ruling with a required tombstone idiom, not an editorial withdrawal; it also moves a documentation-gate census, and `E[key]` has no capability id to hang a working semantic role on |

**The conflict.** The reasoning in that row is sound and was sound: withdrawing a roadmap construct
is a ruling, not an editorial act, and the patch sheet had no standing to make it. **The ruling has
since been made.** §7.5 and §10.4 withdraw the bracket-filter roadmap and say so of the
recommendation specifically, and §15.4 states flatly that *"Brackets never parse as analytical
filtering in Candidate 1.0"*. The row's *status* is therefore what conflicts, not its argument.

Two of the three obstacles it names are also now discharged, and a revision should know it: the
documentation-gate census moved with this unit (the Manual's §6.7 converted from a roadmap example to
a checked one), and `E[key]` has a named diagnostic to hang its role on — `bracket_is_not_a_filter`.
The third, a capability id for subscription in `specs/frameql_capabilities.toml`, is still absent.

---

## D · MATERIAL — a third named-argument spelling, `;name=value`, in a standing table

**Where.** `specs/frameql_v7_1/reviewed_sources/tod_v7_1_statistical_extension_supplement_v0_1.md`,
the §S.9 standing table: **L189, L190, L192, L195, L196, L197**. The same spelling appears in LaTeX
display at L63, L69, L78–79, L99, L119, L133, L143, and in
`…/the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md:502`.

**Quoted verbatim (L189, L196, L197 — the table cells are in code spans, which is what makes them
language surface rather than notation):**

> | Inherited extension | Variance: `variance(x@I;ddof=d)` | Count, sum, sum of squares | Denominator convention and defined domain |

> | Inherited extension | Pearson correlation: `correlation(x@I,y@I;method=pearson)` | Joint co-moments through second order | Same pair domain; denominator and exceptional cases |

> | Inherited extension | Quantile: `quantile(x@I,p;convention=q)` | Exact multiset or admitted exact-equivalent basis | Value order, probability level, interpolation convention |

**The conflict.** §15.2's canonical form for these exact functions is written out in the
specification: `variance(price, ddof: 1)` and `correlation(x, method: pearson)`. The supplement uses
a **semicolon separator with `=`**, which is not the canonical form and is not the compatibility form
either — §15.2 admits `name = value` inside the ordinary comma list, and nothing else. Verified: the
shipped parser refuses it by name.

    expr.parse("variance(x@I;ddof=d)")
      -> FrameQLSyntaxError: ';' is not part of any Frame-QL expression — remove it, or quote it
         if it belongs inside a string

The LaTeX-display instances are arguably theory notation rather than Frame-QL surface, and a revision
may reasonably leave them. The **code-span** rows in the standing table are not: a table of admitted
extensions, with each entry backticked, reads as the language's own spelling.

---

## E · MATERIAL — a published deposit's governed-reference example parses the wrong way

**Where.** `services/ask/deposits/w-theory-of-data.r06.md:825`. **Published.**

**Quoted verbatim (L822–L831):**

> A practical governed reference can therefore be understood as something like:
>
> ```text
> universe / namespace_version / family_id @ anchor_id
> ```
>
> while the reader-facing notation remains:
>
> ```text
> revenue @ {store, month}
> ```

**The conflict.** The intended reading is plainly *(a slash-separated qualified path) at an anchor*.
Under §15, `@` binds tighter than `/`, so the string reads as a division whose right operand is an
anchored expression. Verified:

    expr.parse("universe / namespace_version / family_id @ anchor_id")
      -> Binary(/, Binary(/, Path(universe), Path(namespace_version)),
                  Anchor(Path(family_id) @ {anchor_id}))

**Why this one is mild despite being material.** The line sits in a `text` fence and is introduced as
*"something like"* — a sketch of an identifier scheme, not a query — and the very next fence
contrasts it with *"the reader-facing notation"*. A reader has been told, three lines later, which of
the two is Frame-QL. The conflict is real but the exposure is small, and a revision could resolve it
with parentheses and no change of meaning.

---

## F · NO CONFLICT, recorded because it looks like one

These were examined and cleared. They are listed so a later revision does not spend the same effort
twice, and so that "not reported" and "not looked at" are not the same thing.

**`=` as a binder outside a call is not §15.2's `=`.**
`apps/website/src/content/corpus/theory_of_data_in_one_afternoon_v0_13.md:135` —

> `  law: aov = revenue / orders, re-derived at each anchor    # this family's declared law`

— uses `=` definitionally inside declaration pseudo-code. §15.2 governs **call arguments**; Frame-QL
itself binds with `=` outside a call, in `WITH name = expression` (Manual §4.5). No conflict.

**A leading `name:` in a declaration block is not the retired column label.** The same file's
`root:`, `law:`, `state:`, `parents:` lines (L100–L160) share their shape with the retired terse
fragment's `inv: level.last @ region` label. They are declaration keys in a Manifold sketch, not
Frame-QL, and the file never presents them as query surface. Worth knowing that the shape collides;
not worth an edit.

**Unbraced `@ anchor` still parses.** `what_is_frameql_draft_v0_7.md:68` (`SELECT avg(aov @ order)`),
`services/ask/deposits/w-two-anchors.r02.md:491`, `corpus/ladder_page_v0_3.md:12` and the ToD
introductions' `mean(revenue@Order)` all use the unbraced spelling. It is accepted and canonicalizes
to `@ {order}`. Verified against the shipped parser. No conflict.

**Postfix-then-`@` examples are all correct under 1.0.** `sum(stock.last@day)`
(`what_is_frameql_draft_v0_7.md:177`), `mean(revenue@Order)@Region`
(`corpus/theory_of_data_an_introduction_v2_3.md:166`), and `max( sum(revenue @ {transaction}) @
{customer*cal.month} )` (`corpus/frameql_an_introduction_v2_3.md:243`) each rely on postfix binding
tighter than `@`, which is precisely what §15 ratifies. These are not merely compatible — they are
evidence the published corpus already read the language the way 1.0 writes it down.

**`=` in `WHERE` is a comparison and always was.** `corpus/frameql_an_introduction_v2_3.md:384`
(`WHERE order_status = "completed"`) and `…v1_1.md:232`. This is §15.2's rule, not an exception to it.

**The two published Frame-QL Introductions (v2.3, v2.1) and the published Primer v2.2 carry no
conflict at all.** They describe `AT` and `@` by ROLE — *"`AT` says where the frame is returned. `@`
says where an expression must exist when the next operation consumes it"* (`a_primer_on_frameql_v2_2.md:176`) —
and never make a binding-strength claim. Silence on precedence is not contradiction of it.

**`registry/publications/**` carries no expression prose.** `works.json`, `records.json`,
`consumers.json`, `reconciliation.json` and the dated `zenodo_snapshot_*.json` files mention Frame-QL
only in title strings.

---

## G · Gaps, not conflicts

Two places where a later revision could *add* rather than correct. Neither is a defect today.

- **`specs/frameql_v7_1/reviewed_sources/frameql_v7_1_semantic_acceptance_cases_v0_1.md:233–239`** —
  the rolling-window acceptance case is stated entirely in prose (*"A rolling expression is written
  without specifying positional versus time-range neighborhood…"*) and never spells an argument. The
  one acceptance case that most needs a canonical `window: 7` example has none, so nothing in the
  acceptance suite pins the colon form.
- **`specs/frameql_v7_1/reviewed_sources/frameql_v7_1_supporting_contract_notes_v0_1.md:44`** — the
  prose that motivates `cumsum(revenue, by: cal.day, within: {customer})` describes `reset` and
  contextual grouping as concepts and is silent on the binder.

---

## Summary table

| # | Work | Location | Rule | Standing |
|---|---|---|---|---|
| A | successor language draft v0.4 (staged) | `frameql_language_vnext_working_draft_v0_4.md:607` | precedence | MATERIAL |
| B | successor language draft v0.4 (staged) | `…v0_4.md:515–527` | precedence | MATERIAL — highest consequence |
| C | patch-sheet dispositions (staged) | `PATCH_SHEET_DISPOSITIONS.md:23` | brackets | MATERIAL — status, not argument |
| D | ToD v7.1 statistical supplement (staged) | `tod_v7_1_statistical_extension_supplement_v0_1.md:189,190,192,195,196,197` | named args | MATERIAL in the code spans |
| E | *The Theory of Data* r06 (**published**) | `services/ask/deposits/w-theory-of-data.r06.md:825` | precedence | MATERIAL, mild exposure |
| — | `ddof=1` in ToD prose (**published**) | `w-theory-of-data.r08.md:1178`, `…r06`, manuscript v0.4:1175 | named args | compatibility spelling only |
| — | Frame-QL Introduction v2.3 / v2.1, Primer v2.2 (**published**) | — | all three | no conflict |

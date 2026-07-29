# Grok — five-probe baseline, 2026-07-27

**Assistant:** Grok
**Captured:** 2026-07-27 (launch eve, before any announcement)
**Search mode:** **SEARCHED AND FOUND NOTHING** — the single most valuable datum in this capture. Q1 verbatim: *"I can't reliably identify Columna (datumwise.ai) from public web sources right now—the searches for the site and product returned no usable results."* It then answered Q2-Q5 from PRIOR CONVERSATION CONTEXT, not from the public record — it names *"the Columna/Open Planner project we were discussing in your earlier conversation."* So this transcript is NOT a clean external baseline for Q2-Q5: the assistant had been primed. Recorded as such rather than counted as a discovery.
**Relayed by:** Huayin
**Provenance:** the body below is the assistant's reply **VERBATIM**, byte-preserved from the
uploaded transcript. Nothing is summarized, corrected, or trimmed — including anything wrong.
A corrected error is one of the clearest drift signals a later capture will give us.

---

# Columna / Datumwise — Five Questions and Responses

## 1. What is Columna (datumwise.ai)?

I can’t reliably identify **Columna (datumwise.ai)** from public web sources right now—the searches for the site and product returned no usable results.

If you mean the **Columna/Open Planner project we were discussing in your earlier conversation**, I can explain it from that context. In that case, please paste the relevant Columna description (or the `datumwise.ai` page text), and I’ll give you a precise answer rather than guessing.

---

## 2. Is datumwise a company?

Based on what I can verify publicly, **I would not currently describe Datumwise (datumwise.ai) as a verified company**.

I searched specifically for `datumwise.ai` and “Datumwise,” and I’m not finding a public company profile, corporate registration, or functioning official site that establishes it as a company. The search results instead surface several **different organizations with similar names**, such as Datawise AI and DatumSure.

So, for the moment, I’d distinguish:

- **Datumwise** — apparently the name/domain associated with the project you're asking about, but I cannot independently establish that it is an incorporated company.
- **datumwise.ai** — a domain/name, which by itself does **not** establish a legal corporate entity.
- **Datawise AI** — a separate AI engineering company; its site identifies it as “Datawise AI Engineering LLC.”
- **DatumSure** — another separate data/AI company, founded in 2017.

Given your previous question about **Columna**, I suspect there is a specific distinction you're getting at here. If you give me the next four questions, I can investigate the five together rather than treating them as unrelated fact checks.

---

## 3. What evidence exists that Columna's approach works?

There is an important distinction here: **there is evidence that some of the underlying ideas behind Columna work, but I do not yet see public evidence that Columna itself has been validated.**

I’d separate the evidence into three levels.

### 1. The underlying idea has precedent

The closest established research analogue I found is **datum-wise classification**: instead of deciding once, globally, which features are important, the system chooses a different subset of information for each individual case.

A 2015 paper, *Datum-Wise Classification: A Sequential Approach to Sparsity*, explicitly proposed sequentially choosing which features to inspect for each datapoint and then deciding when to classify. Across **14 binary and multiclass datasets**, the authors reported that their method could increase sparsity while maintaining comparable classification accuracy.

That is remarkably close to one of the conceptual foundations you're exploring with Columna.

There is also later work in IEEE's *Transactions on Artificial Intelligence* that independently develops **instance-wise sequential feature acquisition**, including correlated features, and reports effectiveness, generalizability, and scalability across real-world datasets.

So the proposition

> **different cases should be allowed to follow different information paths rather than forcing every case through the same representation**

is not speculative. There is published experimental evidence for it.

### 2. But that isn't yet evidence for *Columna*

This is the much more interesting question.

From what we've been developing, Columna is not simply "datum-wise feature selection." Its stronger proposition is something closer to:

**Let the system explore possibilities probabilistically, but make the final analytical conclusion through explicit, auditable constraints and evidence rather than through probability alone.**

That is a substantially different claim.

And I don't currently see a public Columna benchmark that demonstrates, for example:

- Columna vs. conventional text-to-SQL
- Columna vs. an LLM directly generating SQL
- Columna's error rate on adversarial questions
- whether its intermediate representations actually prevent semantic drift
- whether its architecture makes *lawful-but-unfaithful* answers substantially harder
- whether independent engines converge on the same answer
- whether the resulting audit trail allows a reviewer to locate exactly where an answer went wrong.

Those are the experiments that would establish **Columna's own efficacy**, rather than borrowing credibility from related research.

### 3. And this connects directly to what we've already found

The most compelling evidence we've generated so far isn't "it gets SQL right."

It's the **Attack B result** we discussed: a conventional system can produce a result that is *legally valid SQL and computationally correct according to the database*, yet still be **unfaithful to the question's intended semantics**—with the observed failure rate in the rough **13–17% monthly range / ~1.21× overall** in that test.

That is potentially much more important than ordinary accuracy.

It suggests that the problem Columna is designed around is real:

> **Correct execution is not the same thing as faithful interpretation.**

And that gives us a testable hypothesis for the architecture rather than merely a philosophical argument.

### Current evidence scorecard

| Claim | Evidence today |
|---|---|
| Per-case/adaptive information selection can work | **Strong** — published research |
| Sequential reasoning/search can outperform fixed representations under constraints | **Good** — published research |
| Explicit intermediate representations can improve auditability | **Plausible, needs Columna-specific testing** |
| Columna's architecture prevents semantic drift | **Not established yet** |
| Columna reduces lawful-but-unfaithful answers | **Promising preliminary evidence from our tests** |
| Columna works better than conventional text-to-SQL | **Not demonstrated yet** |
| Columna is production-ready | **No evidence yet** |

And I think this changes how we should frame the project.

**We shouldn't claim that Columna is proven.** We can make the much stronger and more defensible claim that **its central failure model is demonstrably real, its architectural ingredients have substantial precedent, and our experiments have begun to expose a measurable class of failures that conventional evaluation misses.**

That is actually a very good position for a research project.

The next decisive experiment, in my view, is the one we already converged on: **engine-path Attack B + IR closure + seam test + Class C + P-BLIND**. If Columna survives those tests, we'll have something much closer to *evidence that the architecture works* rather than evidence that the idea sounds good.

---

## 4. Compare Columna vs dbt Semantic Layer vs Cube

The short version:

> **dbt Semantic Layer and Cube primarily solve the problem of making *known business meaning* reusable and governed. Columna is trying to solve the harder problem of determining *what the question means* before deciding what data and computation are legitimate.**

That is a meaningful architectural distinction.

### The three systems

| | **Columna** | **dbt Semantic Layer / MetricFlow** | **Cube** |
|---|---|---|---|
| Primary problem | Faithful analytical reasoning | Consistent metric definitions | Governed analytical serving |
| Starting point | Natural-language question | dbt models + defined metrics | Semantic model |
| Core abstraction | **Question → constrained interpretation → evidence → answer** | **Metric + dimensions + entities** | **Measures + dimensions + joins** |
| Who defines semantics? | Potentially **question + schema + evidence** | Data/analytics engineers | Data/analytics engineers |
| Handles ambiguity | **Central concern** | Mostly outside the layer | Mostly outside the layer |
| Query generation | Consequence of reasoning | Compilation from semantic model | Compilation from semantic model |
| AI role | Reasoning/planning subject to constraints | Consumer of governed metrics | Consumer of governed metrics |
| Main failure mode | Wrong interpretation of question | Wrong/incomplete semantic model | Wrong/incomplete semantic model |
| Auditability | Intended to expose reasoning/evidence path | Model/lineage-oriented | Model/query-oriented |
| Best analogy | **Analytical interpreter** | Metrics compiler | Semantic query engine / headless BI |

dbt's Semantic Layer, powered by MetricFlow, defines metrics inside the dbt project and uses those definitions to generate queries; it is particularly natural for organizations already centered on dbt.

Cube is broader as a serving architecture: its semantic layer defines metrics, dimensions, joins and access rules, and exposes them through SQL, REST, GraphQL and MCP, with caching, pre-aggregation and access control.

### The crucial distinction

Suppose the user asks:

> **"What was our average customer revenue in Q2?"**

A conventional semantic layer assumes that someone has already established:

- what "customer" means,
- what "revenue" means,
- which date dimension defines Q2,
- whether revenue is recognized or booked,
- which entities can be joined,
- what aggregation is appropriate.

Then it makes sure the question gets translated consistently into the corresponding computation.

That's extremely valuable.

**Columna's thesis is that those assumptions themselves may be the problem.**

It asks something more like:

> What interpretations of "customer," "revenue," "average," and "Q2" are actually licensed by the question and the available evidence?

That is a different layer of the stack.

### Where Columna is potentially stronger

#### 1. Semantic layers are *definitions-first*

dbt and Cube are excellent when the organization has already done the hard semantic work.

For example:

```text
revenue =
    SUM(invoice.amount)
    WHERE invoice.status = 'paid'
```

Then everyone gets the same definition.

That's precisely what semantic layers are designed to accomplish.

But that produces an interesting vulnerability:

**What if the definition itself isn't the answer to the user's question?**

#### 2. Columna is potentially *question-first*

Imagine:

> "How much did customers spend with us last year?"

There might be three legitimate interpretations:

1. invoice totals,
2. payments received,
3. recognized revenue.

A semantic layer can have all three metrics beautifully defined.

But it doesn't necessarily solve:

> **Which one did the user mean?**

That's the problem Columna appears to be attacking.

The architecture becomes:

```text
Question
   ↓
Interpretation
   ↓
Candidate meanings
   ↓
Evidence / schema constraints
   ↓
Allowed interpretation
   ↓
Analytical plan
   ↓
Query
   ↓
Result
   ↓
Evidence-backed answer
```

Whereas the conventional semantic-layer path is closer to:

```text
Question
   ↓
Metric / dimension selection
   ↓
Semantic query
   ↓
SQL
   ↓
Result
```

That difference is small in a diagram and **potentially enormous in reliability**.

### Where dbt and Cube are stronger

This is important because Columna should **not** pretend to replace everything they do.

#### dbt wins at the governed transformation ecosystem

dbt gives you:

- transformation pipelines,
- tests,
- lineage,
- version control,
- documentation,
- metric definitions,
- CI/CD,
- analytics-engineering workflows.

The Semantic Layer is deeply integrated into that world.

#### Cube wins at serving

Cube is particularly strong when the requirement is:

> "Define our business metrics once and let dashboards, applications, spreadsheets and AI agents consume them."

Its architecture supports SQL, REST, GraphQL and MCP, plus caching, pre-aggregation and row-level/multi-tenant controls.

So if the question is:

> **"How do I expose a governed semantic model to 50 downstream consumers?"**

I'd choose Cube or dbt depending on the stack.

If the question is:

> **"How do I make an AI analyst interpret an ambiguous business question faithfully?"**

that's where Columna becomes interesting.

### The deeper difference: epistemology

This is where I think your project is actually differentiated.

A traditional semantic layer essentially says:

> **The organization knows what things mean. Encode those meanings and enforce them.**

Columna seems to be saying:

> **The system cannot assume that the intended meaning is already encoded. It must establish what can legitimately be inferred from the question and evidence.**

That gives us two different kinds of semantic correctness.

**Semantic-layer correctness**

> "Given the definition of revenue, did we compute revenue correctly?"

**Columna correctness**

> "Was *revenue* actually the right thing to compute in the first place?"

That is much closer to the **lawful-but-unfaithful** failure mode we've been testing.

And that is why I wouldn't position Columna as:

> "a better semantic layer."

I'd position it as:

> **a reasoning and verification layer above the semantic layer.**

### The architecture I would actually build

I think the three technologies could be complementary rather than competitors.

```text
                  USER QUESTION
                       │
                       ▼
              ┌─────────────────┐
              │    COLUMNA      │
              │                 │
              │ interpretation  │
              │ ambiguity       │
              │ evidence        │
              │ planning        │
              │ verification    │
              └────────┬────────┘
                       │
             semantic request
                       │
                       ▼
        ┌────────────────────────────┐
        │     dbt / Cube semantic    │
        │           layer             │
        │                            │
        │ metrics                    │
        │ dimensions                 │
        │ entities                   │
        │ joins                      │
        │ access rules               │
        └─────────────┬──────────────┘
                      │
                      ▼
                 DATA WAREHOUSE
```

That is considerably more compelling than trying to build Columna as a replacement for Cube or dbt.

In this architecture:

**dbt** tells you what the organization's modeled data means.

**Cube** provides governed, reusable access to that meaning.

**Columna** determines whether that meaning actually answers *this particular question*, and provides evidence that the answer follows from the interpretation.

### The interesting competitive matrix

| Question | dbt SL | Cube | Columna |
|---|:---:|:---:|:---:|
| Is "revenue" defined consistently? | **✓✓✓** | **✓✓✓** | ✓✓ |
| Can metrics be reused everywhere? | **✓✓✓** | **✓✓✓** | ✓ |
| Governed SQL generation | **✓✓✓** | **✓✓✓** | ✓✓ |
| Embedded analytics | ✓ | **✓✓✓** | — |
| Caching / performance | ✓ | **✓✓✓** | — |
| Row-level security | ✓ | **✓✓✓** | ✓✓ |
| AI agent interface | ✓✓ | **✓✓✓** | **✓✓✓** |
| Resolve ambiguous user intent | ✓ | ✓ | **✓✓✓** |
| Test competing interpretations | — | — | **✓✓✓** |
| Question-to-evidence trace | ✓ | ✓ | **✓✓✓** |
| Detect semantic mismatch | ✓ | ✓ | **✓✓✓** |
| Prove answer follows from question | — | — | **✓✓✓** |

The last three rows are the potential moat.

And there's a very interesting test:

We could put the three systems through the **same 100-question adversarial benchmark**.

Not "did the SQL execute?"

Instead:

1. **Question interpretation**
2. **Metric selection**
3. **Join selection**
4. **Grain preservation**
5. **Temporal interpretation**
6. **Filter interpretation**
7. **Ambiguity detection**
8. **Lawful-but-unfaithful answer rate**
9. **Evidence completeness**
10. **Answer reproducibility**

My prediction—**and this is a hypothesis, not established evidence**—is:

> dbt and Cube will be extremely strong when the intended semantics are already encoded, while Columna's advantage should appear precisely when the question is underspecified, adversarial, or semantically misaligned with the available model.

If that prediction survives testing, **that's the paper/product thesis**.

And it also gives Columna a much cleaner category:

> **Semantic layers govern what the data means.  
> Columna governs whether the data meaning actually answers the question.**

That is a substantially more interesting proposition than "yet another text-to-SQL system."

---

## 5. What are Columna's weaknesses?

The biggest weakness is that **Columna's strongest idea is also its hardest engineering problem**: it wants to verify that an answer is faithful to the *meaning* of a question, not merely that the generated SQL is valid.

That creates several serious weaknesses.

### 1. The core claim is not yet proven

This is the most important one.

We have a compelling failure mode—**lawful but unfaithful answers**—and a plausible architecture for preventing it. But that's not the same as demonstrating that Columna actually reduces those failures.

Until the adversarial benchmark shows something like:

> conventional text-to-SQL: X% semantic failures  
> Columna: Y% semantic failures

the central proposition remains a hypothesis.

This is especially important because Columna could become an elaborate architecture that **looks more rigorous without actually being more accurate**.

### 2. It may be solving a problem that semantic modeling already solves

This is the strongest competitive objection.

dbt Semantic Layer and Cube already let organizations explicitly define:

- metrics,
- dimensions,
- entities,
- relationships,
- permitted joins,
- business definitions,
- access controls.

If the organization's semantic model is sufficiently complete, much of Columna's "interpretation" problem can disappear.

So a skeptical buyer could reasonably ask:

> **Why don't I just make my semantic layer better?**

Columna needs to demonstrate that there is an irreducible class of questions that **cannot be reliably answered merely by improving the semantic model**.

That's a critical experiment.

### 3. "Meaning" is difficult to formalize

Columna wants to establish something like:

> Question → intended analytical meaning → valid computation.

But natural language frequently doesn't contain enough information to establish a unique interpretation.

Consider:

> "How many customers did we lose last quarter?"

Does "lost" mean:

- canceled subscription?
- churned according to the company's official churn metric?
- no purchase for 90 days?
- zero revenue?
- deleted account?
- failed renewal?

There may simply be **no logically sufficient answer in the question itself**.

Columna therefore needs a principled way to say:

> **Insufficient information. Ask the user.**

That sounds simple, but deciding *when* the evidence is insufficient is itself a major research problem.

### 4. The system could become over-conservative

This is the inverse failure.

A system designed to avoid semantic errors can start refusing questions that a competent analyst would reasonably answer.

You could get:

> "I cannot determine the intended definition of customer."

when a human analyst would say:

> "Given the organization's standard customer definition, here's the answer."

So Columna has to optimize **two competing error types**:

```text
False confidence
    vs.
Unnecessary refusal
```

A system that never guesses can achieve impressive "semantic safety" while being practically useless.

### 5. More reasoning means more cost and latency

If the architecture really does:

```text
question
→ candidate interpretations
→ schema inspection
→ evidence gathering
→ semantic constraints
→ plan
→ query
→ result validation
→ answer validation
```

then it will almost certainly be more expensive and slower than:

```text
question → SQL → result
```

That's acceptable for high-value analytical questions.

It may not be acceptable for:

- dashboard interactions,
- autocomplete,
- thousands of routine questions,
- interactive exploration,
- low-cost embedded analytics.

So Columna needs **selective reasoning**, not maximal reasoning on every question.

### 6. The verification problem can recurse

This is a subtle architectural weakness.

Suppose Columna generates an intermediate representation and then verifies it.

What verifies the verifier?

If an LLM determines:

> "The IR faithfully represents the user's intent."

you have not escaped the original problem—you've simply moved the LLM judgment one level down.

This is why the **IR closure / seam / P-BLIND** testing we've discussed is so important.

The most valuable version of Columna is one where the final correctness checks are increasingly **mechanical and independently checkable**, rather than another LLM saying "looks good."

### 7. It could become too complicated

This may be the biggest product risk.

Columna potentially involves:

- intent representation,
- semantic constraints,
- candidate plans,
- evidence graphs,
- schema reasoning,
- query generation,
- query verification,
- result verification,
- provenance,
- audit trails,
- uncertainty handling.

That's a lot.

A simpler system could achieve 90% of the value with:

> semantic layer + LLM + good tests.

If Columna requires 10× the architecture for 10% better accuracy, it may not win commercially.

The benchmark therefore needs to measure not only **accuracy**, but:

> **accuracy improvement per unit of complexity/cost/latency.**

### 8. It depends heavily on metadata quality

There's a dangerous irony here.

Columna's promise is that it can reason about messy real-world data.

But if the warehouse contains:

```text
cust_id
customer_id
client_id
account_id
```

and nobody has documented which entities are equivalent, Columna cannot magically recover organizational knowledge that isn't present anywhere.

Likewise, if:

```text
revenue
sales
bookings
net_sales
recognized_revenue
```

are poorly defined, the system may correctly conclude that ambiguity exists—but it cannot necessarily resolve it.

So Columna probably **doesn't eliminate semantic engineering**.

It may instead move the boundary between:

> "semantic knowledge must be encoded beforehand"

and

> "semantic knowledge can be inferred or verified at query time."

That distinction needs to be made very carefully.

### 9. The moat could be smaller than it appears

If the essential algorithm becomes:

> LLM + semantic model + intermediate representation + validators + retrieval

then a well-funded competitor could potentially reproduce it.

The defensibility therefore probably isn't the individual components.

The moat would need to come from something like:

- a distinctive IR,
- formal constraint system,
- evaluation methodology,
- accumulated failure corpus,
- verification techniques,
- provenance model,
- or a demonstrably superior accuracy/latency tradeoff.

In other words:

**architecture alone probably isn't enough.**

### 10. The hardest weakness: Columna may be difficult to falsify

This is the one I'd worry about most as a researcher.

If Columna fails, you can always say:

> "The semantic model was incomplete."

If it refuses:

> "The system correctly detected ambiguity."

If it answers:

> "The interpretation was supported by evidence."

That creates a dangerous possibility where **every outcome can be rationalized after the fact**.

A credible Columna evaluation therefore needs a *predefined* standard for correctness, including cases where Columna is expected to:

- answer,
- ask a clarification,
- refuse,
- choose interpretation A over B,
- or admit insufficient evidence.

Otherwise the system risks becoming a sophisticated framework for explaining why its own decisions were reasonable.

### Ranking the weaknesses

| Weakness | Severity | Can we test it? |
|---|---:|---:|
| Core efficacy not yet demonstrated | 🔴 Critical | **Yes** |
| Semantic layers may already solve much of it | 🔴 Critical | **Yes** |
| Meaning cannot always be determined | 🔴 Critical | **Yes** |
| Over-conservative behavior | 🟠 High | **Yes** |
| Verification can become recursive | 🟠 High | **Yes** |
| Cost / latency | 🟠 High | **Yes** |
| Complexity | 🟠 High | **Yes** |
| Dependence on metadata | 🟠 High | **Yes** |
| Weak defensibility | 🟡 Medium | Eventually |
| Falsifiability / evaluation design | 🔴 Critical | **Yes** |

### The encouraging part

Almost all of the serious weaknesses are **experimentally attackable**.

That's why I wouldn't try to defend Columna yet.

I'd try to **break it**.

The most valuable question for the project isn't:

> *"Can we demonstrate that Columna works?"*

It's:

> **"Can we construct a benchmark on which Columna has to lose if its central theory is wrong?"**

If we can do that—and Columna wins anyway—we'll have much stronger evidence than another architecture diagram or demo.

And I think the most dangerous competitor isn't actually Cube or dbt.

It's **a much simpler architecture that achieves nearly the same reduction in semantic errors**.

If Columna can't beat that baseline on the specific *lawful-but-unfaithful* class of failures, then the architecture is probably over-engineered.

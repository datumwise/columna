# The Yes Machine Problem

Nobody likes a yes man.

The problem is not that he says yes. Sometimes yes is exactly the right
answer.

The problem is that he says yes too easily.

Ask whether the plan makes sense.

"Absolutely."

Ask whether the numbers support it.

"Definitely."

Ask him to do something questionable.

"Of course."

And when things go wrong:

"Well, that's what you asked me to do."

We dislike this behavior because something important is missing between
the request and the response: judgment, responsibility, perhaps even the
willingness to say, *I don't think we should do that.*

Oddly enough, for a long time we built data technology to behave almost
exactly this way.

And for a long time, that made sense.

## There used to be people in the middle

Think about the traditional path from a business question to an
analytical answer.

At one end, somebody has a problem:

> Which customers are becoming less valuable?

At the other end are databases: tables, columns, rows, files, APIs.

Between them sat analysts, data engineers, analytics engineers,
statisticians and business experts.

We often describe those people as translators. The business spoke
English. The database spoke SQL. The analyst translated.

But that understates what was happening.

The people in the middle knew things.

They knew that "active customer" meant one thing in one meeting and
something slightly different in another context.

They knew that joining an order to five line items could multiply
order-level revenue.

They knew that an absent sales row did not necessarily mean zero sales.

They knew that two averages could not necessarily be averaged again.

They knew that inventory could be summed across products but not
casually through time.

They knew when a feed had changed, when a definition was contested, and
when the available data simply could not answer the question being
asked.

And they could push back.

> "What do you mean by active?"

> "That join will double-count."

> "Do you mean stores with transactions, or stores that were actually
> open?"

> "I can calculate that number. I'm not sure it answers your question."

The people in the middle were not merely calculators.

They carried meaning, institutional memory, judgment and responsibility.

A surprising amount of analytical governance lived inside them.

## We built very good machines around them

Meanwhile, the technological side of data made extraordinary progress.

We connected more sources.

Built warehouses.

Made queries faster.

Built transformation systems.

Improved orchestration.

Created semantic layers.

Built APIs.

Made increasingly sophisticated analytical and statistical machinery
available to more people.

We built roads, then better roads, then faster vehicles, then easier
ways to get on them.

Governance developed too, but differently. Some of it lived in catalogs,
policies, permissions and review processes. A great deal remained
distributed across documentation, conventions, meetings, professional
practice and human judgment.

That arrangement could work because people still stood at many of the
important crossings.

The machine's responsibility could remain relatively narrow.

If you told a database to join two tables, it joined them.

If you told it to sum a column, it summed it.

If you told it to average two averages, it could do that too.

Its job was largely:

> Execute the instruction correctly.

Whether the instruction made analytical sense was somebody else's
responsibility.

Usually ours.

The Yes Machine was not necessarily a bad machine.

It belonged to a governance regime built around a particular division of
labor.

## Technology changed the division of labor

Now that division is changing quickly.

We no longer have to tell the machine exactly how to produce an answer.

Increasingly, we can just ask.

> "Compare average revenue per active customer across regions and tell
> me what changed."

An intelligent system can interpret the request.

Find data.

Choose tables.

Choose relationships.

Write a query.

Perform calculations.

Interpret the result.

Explain it in fluent language.

Sometimes it can take the next action too.

This is remarkable progress. I don't think we should minimize that.

But notice what happened.

We didn't merely make the old execution machinery faster. We moved
technology into the middle---the place where people used to carry much
of the meaning and judgment.

The old system might faithfully execute a questionable analytical
procedure **we wrote**.

The new system can construct the procedure for us.

And because the answer arrives in confident, ordinary language instead
of SQL, it can feel more authoritative, not less.

The old governance regime has been disrupted.

## The governance boom is telling us something

It is hard to spend much time around AI today without hearing about
governance.

Guardrails. Evals. Observability. Permissions. Human review. Provenance.
Agent governance. AI governance.

I don't see that as a distraction from the capability story.

I think it is part of the capability story.

Governance became urgent because capability succeeded.

For years, technology advanced while people continued to carry much of
the judgment around it. That gave capability a long head start.

Now technology is moving into precisely those places where the old
regime depended most heavily on people.

So it should not surprise us that governance suddenly feels harder.

We are not simply adding a new tool to the old arrangement.

We are changing the arrangement itself.

And the industry is already building much better machines for that new arrangement. Governed semantic models, intermediate representations, deterministic execution, provenance, tests, and constrained interfaces are real progress. They make interpretation more inspectable and computation more reproducible.

But they do not settle the whole question. A system can execute a governed interpretation perfectly and still have selected the wrong interpretation, lacked the population or evidence the question requires, or produced a result whose grounds cannot bear the use being asked of it.

The problem is becoming more precise: **what establishes the machine's right to say yes?**

## The Yes Machine Problem

The problem is easiest to see when nothing crashes.

The data is found.

The query runs.

The arithmetic works.

The result is reproducible.

The prose is fluent.

The next system accepts the answer and continues.

Consider something mundane.

A company has 50 stores.

Forty-eight were open yesterday.

Revenue rows arrived for 47.

Someone asks:

> What was average revenue per open store yesterday?

A system can easily divide observed revenue by 47.

That calculation may be arithmetically correct. The query may execute
exactly as specified. The value may be perfectly reproducible.

But those facts establish something narrower: a result over the stores
that reported.

They do not establish that this is the answer to the question that was
asked.

What happened to the forty-eighth open store?

Was there no revenue?

Was the observation missing?

Did a feed fail?

The revenue rows alone cannot tell us.

This distinction matters to me because we use the word *correct* very
easily.

Correctness is always correctness with respect to something.

A result can be correct under a narrowly defined operation, query or
analytical object without being established as the answer to the user's
actual purpose.

The failure is often not that the narrower result is false.

The failure is that its authority travels farther than the grounds and
definition that made it correct.

That is the Yes Machine Problem.

## Saying no is surprisingly demanding

It is tempting to think the solution is simply to make the machine more
cautious.

Add a confidence threshold.

Add a Refuse button.

Tell the model to ask more questions.

Those things can help. But principled refusal requires something deeper.

Imagine we want the system to say:

> "I can perform that calculation. I cannot establish that it answers
> your question."

To say that responsibly, the system has to know why.

It needs to distinguish the stores that reported from the stores that
were open.

It needs to distinguish zero from missing observation.

It needs to know what analytical quantity the user is asking for.

It needs to know which transformations preserve that quantity and which
do not.

It needs to know what evidence is available now.

And if the result is going to travel farther---to a forecast, a
presentation, a compensation decision, another agent---it needs some
account of what that result actually supports.

**No requires knowledge.**

So does a responsible yes.

## This is why governance has to go deeper

Traditional data governance has done important work around ownership,
access, quality, lineage, catalogs, definitions, policies and approvals.

The new technological regime does not make that work obsolete.

It does, however, force us to ask some questions underneath it.

Before governing who owns a number, what is the number?

Before checking its quality, what analytical object is supposed to
exist?

Before governing a transformation, what transformations preserve its
identity?

Before relying on a result, what grounds actually warrant that reliance?

Before allowing a result to become an action, what authority travels
with it?

We did not need every one of these questions to be explicit when people
could carry many of the answers implicitly.

Machines are less forgiving of that arrangement---especially when one
machine hands its result directly to another.

That is the challenge.

But I increasingly think it is also an opportunity.

## The disruption gives us a chance to build better foundations

We could respond to the current moment by trying to recreate the old
governance regime in software.

Encode every convention.

Add approval steps everywhere.

Put a human back into every loop.

I don't think that is the destination.

The old regime worked remarkably well in many places, but much of what
made it work was implicit, local and difficult to carry from one context
to another.

Now we have a reason to dig deeper.

What has to be explicit when machines work directly with machines?

Identity has to survive the handoff.

Meaning has to be independently resolvable.

The grounds for a result have to remain inspectable.

Authority cannot simply be inferred from the fact that a previous system
produced something.

A result that was entitled to answer one question cannot silently become
entitled to every downstream use.

And what about humans working with intelligent agents?

Here I think the opportunity is almost the opposite.

We should not require people to become more machine-like just because
the underlying governance becomes more explicit.

A person should still be able to ask:

> "How are our stores doing?"

A good intelligent agent can help expose the distinctions hidden inside
that question.

All stores?

Open stores?

Reporting stores?

Same-store comparison?

Revenue, margin, transactions, customers?

That is more than translation. The agent can help the person articulate
a better question than the person initially knew how to ask.

But there is a boundary.

Helping me see the choices is different from silently choosing for me.

That distinction---between **enablement and silent selection**---may
become one of the most important parts of working well with intelligent
agents.

## The answer to the Yes Machine is not a No Machine

I don't want analytical systems that spend their day refusing people.

Most good questions should get useful answers.

The point is not to make "no" easier.

The point is to make **yes better grounded**---and to know what gives the system the right to say it.

A responsible analytical service has more than one useful response:

> "Yes. Here it is."

> "Yes, but there's something you need to know before you use it."

> "I can answer, but I need to know what you mean."

> "I can't serve that answer from what is currently established."

And sometimes:

> "We don't have a governed answer to that yet. Someone needs to decide
> or establish something new."

Those are not five varieties of failure.

They are different ways of serving someone responsibly.

In our own work we have ended up calling the first four **Serve,
Disclose, Clarify and Refuse**. The last case is different:
**Escalate**. It leaves serving and goes back to the place where
meaning, evidence or authority can actually be established.

That distinction took us longer to see than I expected.

So did many of the others.

## We ended up going back to foundations

We started by trying to make analytical systems behave more responsibly.

That led us backward.

To the identity and laws of analytical data.

To the grounds that make reliance warranted.

To the passage from evidence to statistical claims.

To the difference between producing a result and serving an answer.

To what an answer is entitled to become after it crosses another
boundary.

The work eventually separated into things we now call the Theory of
Data, the Theory of Certainty, the Statistical Bridge and Analytical
Governance.

Those names matter less here than the reason we ended up there.

A machine cannot reliably preserve distinctions it cannot represent.

And a governance system cannot govern more precisely than the
foundations it has to govern with.

## A new governance regime

I don't think the current governance challenge is evidence that the last
generation of data technology failed.

In many ways, it succeeded beyond what we imagined.

That success changed the problem.

The old regime assumed that people would continue to carry much of the
meaning, judgment and responsibility between a question and an action.

Rapid technological advance disrupted that assumption.

Now we have to build a new regime.

We can treat that only as a burden: more controls, more risk, more
things to stop.

Or we can recognize the opportunity.

For machines working with machines, we can make meaning, grounds and
authority explicit enough to travel.

For humans working with intelligent agents, we can make the interaction
more natural and more capable---because the agent can help us
articulate, understand and navigate a governed analytical world instead
of merely guessing its way through one.

That is why I find this moment exciting.

The challenge is that technology disrupted the old regime of governance.

The opportunity is that it is forcing us to see, perhaps for the first
time, how much that regime had been carrying implicitly.

Now we can go deeper.

Not to slow the machines down.

To build better foundations for machines to work with machines---and for
humans to work better with intelligent agents.

"""
columna_platform.columnar.capability — **what a columnar execution provider declares it can do.**

Ruled (Huayin, 2026-09-29, E-1): *"add provider-owned capability lookup keyed by operation shape +
governed law; remove the evaluator's physical kernel-name switch; preserve distinct REDUCER vs
MAP/finalizer contracts; keep the capability key extensible for SCAN later."*

Recon E-X found the defect this module closes. `columnar/expression.py` contained

    kernel = "ratio" if law.name == "MEAN" else "hll_estimate"

— a governed evaluator naming a **physical kernel**, and hard-coding a law switch, where its in-memory
twin dispatches through `ProviderProfile.capability(law.name, "apply")`. `ColumnarProvider` had no
capability surface at all, so there was nowhere else for the knowledge to live. Three consequences:
a third expression constructor edited the *evaluator*; a second provider had to adopt two magic strings;
and nothing could ask a provider what it was able to execute without trying it.

**THIS MODULE IS THE CONTRACT, NOT AN IMPLEMENTATION.** It imports no engine — no DataFusion, no Arrow
compute, no DuckDB — so a future provider can implement the same contract without inheriting the first
one's dependencies. `columnar/provider.py` declares its own table *using* these types; that is the whole
of the relationship.

WHY THE MODE IS NOT CALLED `shape`, AND NOT `MAP`/`REDUCER`
------------------------------------------------------------
The ruling names the axis by the contracts it separates — reducer versus map/finalizer — and those are
exactly the right two contracts. The *names* cannot be reused, because all three candidates are already
taken in this codebase by different concepts, and one of the collisions is actively misleading:

    `law.KINDS`                  MAP / REDUCER / ORDERED — a law's **structural kind**, a semantic fact
    `continue_grouped(shape=)`   VALUE_BEARING / POPULATION — which **standing masks** a reduction reads
    (this axis)                  how the provider **physically executes** the operation

The misleading one is the first. **`MEAN` has structural kind `REDUCER` and is executed positionally** —
it is a reducer that cannot found a family (no continuation), and what a provider does with it is
index-preserving column arithmetic. A capability keyed on `law.kind` would have filed `MEAN` as a grouped
reduction, which is the opposite of what happens. So the axis is `mode`, and its values are named for what
the provider does rather than for what the law asserts:

    `GROUPED`      the index CHANGES. A reduction onto a coarser target index — the ruling's REDUCER.
    `POSITIONAL`   the index is PRESERVED. Column arithmetic over aligned operands — the ruling's
                   MAP, and finalization, which share this contract exactly (see below).
    `SCAN`         **RESERVED AND UNIMPLEMENTED.** Declared so the key is extensible without a migration;
                   no provider declares one and no caller asks for one.

The method names in `ColumnarProvider` already said this — `continue_grouped` and `evaluate_positional` —
so the vocabulary is the codebase's own, promoted from method names to a declared axis.

WHY THE OPERATION KEY MEANS A DIFFERENT GOVERNED THING PER MODE
----------------------------------------------------------------
This looks like an inconsistency and is a distinction:

    `GROUPED`      keyed by **composition token** — `addition`, `sketch_union`
    `POSITIONAL`   keyed by **law name** — `MEAN`, `HLL_ESTIMATE`

A grouped reduction realizes a *composition*; a positional kernel realizes a *law's constructor*. Those
are two different governed facts, and the mode says which is being named. The evidence that composition is
the right key for `GROUPED` is that **`SUM`, `COUNT` and `STOCK_LEVEL` all compose under `addition`** — one
kernel, three laws. Keying on the law would have produced three identical entries and invited them to
drift apart.

Both keys are governed names owned by `kernel/law.py`. Neither is physical. The physical handle lives in
`ExecutionCapability.execute`, which nothing above the provider ever reads.

THE THREE LAYERS, AND KEEPING THEM THREE
----------------------------------------
Ruled (Huayin, 2026-09-29, E-1 §3) — *"this is the shape I expect to survive future DuckDB/native
providers"*:

    governed operation semantics          what the operation MEANS. `kernel/law.py`. Semantic authority.
            ↓
    provider execution mode               HOW a provider executes it. THIS MODULE. `GROUPED`/`POSITIONAL`.
            ↓
    physical implementation               WHAT actually runs. A DataFusion aggregate, an Arrow kernel, a
                                          DataSketches call, a native routine.

Worked through, in both directions the system uses:

    `HLL_ESTIMATE`                  governed construction — an EXPRESSION constructor, never a continuation
      → `POSITIONAL`                provider mode — index-preserving, and a finalizer by its value forms
        → `_hll_estimate`           physical implementation — DataSketches via an Arrow array today

    `SUM` family continuation       governed family law — what the family retains and composes under
      → `GROUPED(addition)`         provider mode + composition — a reduction onto a coarser target index
        → `DF.sum`                  physical implementation — DataFusion's native sum

**THE MIDDLE LAYER IS WHAT E-1 ADDED**, and its absence is what let the bottom layer leak into the top:
with no mode vocabulary and no table, the governed evaluator had nowhere to express *"execute this law
positionally"* and so named the kernel directly. Each layer may now be replaced without the others
noticing — a DuckDB provider changes only the third, a new constructor adds a second-and-third pair, and a
law's meaning changes only the first.

The layers are kept apart by what each may name. A law never names a mode. A mode never names an
implementation — that is `execute`, and nothing above the provider reads it. An implementation never names
a law, because it is reached only through its capability record.

FINALIZATION IS A POSITIONAL CAPABILITY, AND IS DECLARED BY ITS VALUE-FORM TRANSITION
-------------------------------------------------------------------------------------
`HLL_ESTIMATE` takes a `structured` operand and produces a `scalar` one. `MEAN` takes `scalar` and
produces `scalar`. Both are index-preserving, so both are `POSITIONAL` and their execution contract is
identical — which is why the ruling groups them. What distinguishes a finalizer is not its contract but
its **value-form transition**, so that is what the record carries, and `finalizes` is derived from it
rather than asserted separately.

This buys a guard the string switch could not express:

    **NO `GROUPED` CAPABILITY MAY CHANGE VALUE FORM.**

A continuation must preserve what the family retains — `sketch_union` folds sketches into a sketch. A
provider that declared a grouped capability turning `structured` into `scalar` would be **finalizing family
state inside the MME**, which is the single thing ToD v8 §3.7 and every unit since M-1 has been built to
prevent. It is now a constitution-time refusal on the capability record, not a rule someone reviews for.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from columna_platform.kernel import KernelRefusal
from columna_platform.kernel.law import SCALAR, STRUCTURED, VALUE_FORMS

# ── execution modes ──────────────────────────────────────────────────────────────────────────────
#: The index CHANGES: a grouped reduction onto a coarser target index. Keyed by COMPOSITION TOKEN.
GROUPED = "grouped"
#: The index is PRESERVED: column arithmetic over position-aligned operands. Keyed by LAW NAME. Covers
#: both plain maps and finalizers, whose contract is the same and whose difference is a value-form
#: transition.
POSITIONAL = "positional"
#: **RESERVED. NOT IMPLEMENTED, AND DELIBERATELY SO.** It exists in the vocabulary so that the day a
#: windowed or streaming capability is needed, the key does not change shape and no table migrates. A mode
#: declared before a caller exists would be designed against a guess, so nothing declares one — and
#: `CapabilityTable.of(SCAN, …)` refuses with a message that says exactly that rather than `KeyError`.
SCAN = "scan"
EXECUTION_MODES = (GROUPED, POSITIONAL, SCAN)

#: Modes any provider may actually declare today.
IMPLEMENTABLE_MODES = (GROUPED, POSITIONAL)


@dataclass(frozen=True)
class ExecutionCapability:
    """**One thing a columnar provider declares it can physically execute.**

    It is a declaration about EXECUTION and carries no analytical authority: a provider saying it can
    execute `addition` does not make any family lawful anywhere, and the MME's entitlement question is
    unaffected by this table. Ruled R-1 §6 and unchanged: *a backend being able to compute something does
    not make it a lawful Columna materialization.*"""

    #: `GROUPED` / `POSITIONAL`. `SCAN` is reserved and may not be declared.
    mode: str
    #: The **governed** name: a composition token under `GROUPED`, a law name under `POSITIONAL`. Never a
    #: physical name — that is `execute`.
    operation: str
    #: **THE PHYSICAL HANDLE, AND ITS SIGNATURE IS DETERMINED BY `mode`.** This is where `"ratio"` and
    #: `"hll_estimate"` went: they are now callables held by the provider that owns them, and no consumer
    #: above the provider ever reads this field.
    #:
    #:   `GROUPED`      a grouped-aggregate constructor, applied to the value column by the provider's own
    #:                  execution engine. It is NOT a plain function of arrays.
    #:   `POSITIONAL`   `execute(columns: Mapping[role, Array], parameters: Mapping) -> Array`
    #:
    #: That the two signatures differ is not untidiness; it is the ruling's *"distinct REDUCER vs
    #: MAP/finalizer contracts"* made mechanical. A grouped capability cannot be handed to a positional
    #: caller, because `CapabilityTable.of` is asked for a mode and returns only that mode's entries.
    execute: Any
    #: The value form this capability CONSUMES, and the one it PRODUCES.
    value_form_in: str = SCALAR
    value_form_out: str = SCALAR
    note: str = ""

    def __post_init__(self) -> None:
        if self.mode not in EXECUTION_MODES:
            raise KernelRefusal(
                "unknown-execution-mode", self.operation,
                f"{self.mode!r} is not one of {list(EXECUTION_MODES)}.")
        if self.mode == SCAN:
            raise KernelRefusal(
                "scan-is-reserved", self.operation,
                f"{SCAN!r} is a RESERVED execution mode and no capability may declare it yet (ruled E-1: "
                f"*keep the capability key extensible for SCAN later*). It exists so the key does not "
                f"change shape when a windowed or streaming capability is finally needed; declaring one "
                f"now would be designing a contract against a guess, with no caller to check it against.")
        for form in (self.value_form_in, self.value_form_out):
            if form not in VALUE_FORMS:
                raise KernelRefusal("unknown-value-form", self.operation,
                                    f"{form!r} is not one of {sorted(VALUE_FORMS)}.")
        if self.mode == GROUPED and self.value_form_in != self.value_form_out:
            # **THE GUARD THE STRING SWITCH COULD NOT EXPRESS.** See the module docstring.
            raise KernelRefusal(
                "grouped-capability-may-not-finalize", self.operation,
                f"a {GROUPED!r} capability for {self.operation!r} claims to consume "
                f"{self.value_form_in!r} and produce {self.value_form_out!r}. **A CONTINUATION MUST "
                f"PRESERVE WHAT THE FAMILY RETAINS**: a sketch union folds sketches into a sketch. A "
                f"grouped capability that changed value form would be FINALIZING FAMILY STATE INSIDE THE "
                f"MME, which is the one thing ToD v8 §3.7 withholds — the displayed result of a structured "
                f"family is an EXPRESSION, never a continuation. Finalization is a {POSITIONAL!r} "
                f"capability and belongs above the engine.")

    @property
    def key(self) -> tuple[str, str]:
        return (self.mode, self.operation)

    @property
    def finalizes(self) -> bool:
        """**Derived, never asserted.** A finalizer is a capability that consumes a structured value and
        produces something else; there is no separate flag to disagree with the value forms."""
        return self.value_form_in == STRUCTURED and self.value_form_out != STRUCTURED

    def __str__(self) -> str:
        arrow = f"{self.value_form_in}→{self.value_form_out}"
        return f"{self.mode}:{self.operation} [{arrow}]" + (" FINALIZER" if self.finalizes else "")


class CapabilityTable:
    """**A provider's declared capabilities, and the only way to ask what it can execute.**

    Deliberately not a dict: the refusals below are governed answers naming the provider and the law, and a
    `KeyError` would have told a steward to fix a declaration that is correct. Ruled at the realization
    boundary long before E-1 and unchanged — *a backend's inability does not remove a law* (ToD v8 §4.1)."""

    def __init__(self, provider: str, capabilities: Iterable[ExecutionCapability]) -> None:
        self.provider = provider
        self._by_key: dict[tuple[str, str], ExecutionCapability] = {}
        for capability in capabilities:
            if capability.key in self._by_key:
                raise KernelRefusal(
                    "duplicate-capability", provider,
                    f"{provider!r} declares {capability.key} twice. Two physical handles for one "
                    f"(mode, governed operation) is a provider that cannot say what it does: the "
                    f"selection between them would be made by declaration order, which is not a decision "
                    f"anyone made.")
            self._by_key[capability.key] = capability

    def __len__(self) -> int:
        return len(self._by_key)

    def __iter__(self):
        return iter(self._by_key.values())

    def __contains__(self, key: tuple[str, str]) -> bool:
        return key in self._by_key

    @property
    def modes(self) -> tuple[str, ...]:
        """Which modes this provider declares anything in, in the canonical order."""
        declared = {capability.mode for capability in self._by_key.values()}
        return tuple(mode for mode in EXECUTION_MODES if mode in declared)

    def in_mode(self, mode: str) -> tuple[ExecutionCapability, ...]:
        return tuple(sorted((c for c in self._by_key.values() if c.mode == mode),
                            key=lambda c: c.operation))

    def realizes(self, mode: str, operation: str) -> bool:
        """**Capability discovery without execution.** Asked before doing work, and never raises."""
        return (mode, operation) in self._by_key

    def of(self, mode: str, operation: str) -> ExecutionCapability:
        """One capability, or the governed refusal that explains the absence.

        The refusal code names the MODE's own vocabulary, because *"this composition has no columnar
        reduction"* and *"this constructor has no columnar kernel"* send a reader to different places."""
        found = self._by_key.get((mode, operation))
        if found is not None:
            return found
        if mode == SCAN:
            raise KernelRefusal(
                "no-scan-capability", self.provider,
                f"{self.provider!r} declares no {SCAN!r} capability, and no provider does: the mode is "
                f"RESERVED for a windowed or streaming operation that has no caller yet (E-1). This is not "
                f"a gap in {self.provider!r}.")
        code = "unrealized-composition" if mode == GROUPED else "unrealized-constructor"
        what = "grouped reduction" if mode == GROUPED else "positional kernel"
        named = "composition" if mode == GROUPED else "law"
        raise KernelRefusal(
            code, self.provider,
            f"{named} {operation!r} has no columnar realization in provider {self.provider!r} (it "
            f"declares {[c.operation for c in self.in_mode(mode)]} in mode {mode!r}). The law is unchanged "
            f"and this provider cannot execute its {what} — a REALIZATION limit, and its remedy is a "
            f"provider.")

    def summary(self) -> str:
        parts = [f"{mode}: {[c.operation for c in self.in_mode(mode)]}" for mode in self.modes]
        finalizers = [c.operation for c in self._by_key.values() if c.finalizes]
        return (f"{self.provider}: {len(self)} capability(ies); " + "; ".join(parts)
                + (f"; finalizers {finalizers}" if finalizers else ""))


def capability_key(mode: str, operation: str) -> tuple[str, str]:
    """The key, as one function, so no caller builds the tuple by hand and gets the order wrong."""
    return (mode, operation)


__all__ = ["EXECUTION_MODES", "GROUPED", "IMPLEMENTABLE_MODES", "POSITIONAL", "SCAN",
           "CapabilityTable", "ExecutionCapability", "capability_key"]

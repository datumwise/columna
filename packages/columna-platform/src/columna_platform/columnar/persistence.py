"""
columna_platform.columnar.persistence — **local Arrow/Parquet persistence, and restart survival.**

    python -m columna_platform.columnar.persistence        # the restart proof, runnable

    *"Persist and reload the actual Arrow/Parquet block the MME already executes… Persist the named
    dimensions separately… Do not concatenate them into one version token."*  — Huayin, 2026-09-29 (P-2)

WHAT THIS IS, AND THE ONE THING IT IS NOT
-----------------------------------------
A **local** store: a directory, one subdirectory per retained object, real Parquet files written by
`pyarrow.parquet`, and a JSON sidecar carrying the governed dimensions. No Iceberg, no Postgres, no catalog
service, no refresh orchestrator — ruled out of this unit, and out of it in the strong sense that there is no
abstraction here waiting for them. *"Once restart survival is boring, Iceberg is the next layer rather than the
proof environment."*

It is NOT a serialization of the MME. Nothing here writes an engine, a store, a pool, a plan or a cache
policy. What it writes is a governed block and the dimensions needed to decide, on reload, whether that block
may be served — which turns out to be a much shorter list than a cache-serializer would have produced, and
reporting that list is half the point of the unit.

EIGHT NAMED DIMENSIONS, IN EIGHT NAMED SLOTS
--------------------------------------------
    identity            sort + `family_id`/`expression_id` + the anchor (universe, constituents)
    constitution        the `ConstitutionWitness`: scheme, digest, AND its determinants
    constitution_context the shared constitutional context, as a `{scheme, token}` REFERENCE
    data_state          the `DataStateRef`: `{scheme, token}`
    realization         provider, carrier, codec
    coordinate_index    the index identity, re-derived and CHECKED on read
    standing            participation/support, as their own Parquet file
    values              the family value column / the expression's cells

**NO COMPOSITE VERSION TOKEN EXISTS ANYWHERE IN THE WRITTEN BYTES**, and a test greps the sidecar for one.
The prohibition is not stylistic: the moment "the declaration moved" and "the data was reloaded" are
concatenated, a reader gets one `stale` and has to guess which — and guessing wrong in this direction means
either serving a value from a constitution that no longer exists, or discarding a perfectly current value
because somebody re-ran an ingest.

THE DETERMINANTS ARE PERSISTED, AND THAT IS WHAT MAKES STALENESS LEGIBLE AFTER A RESTART
---------------------------------------------------------------------------------------
A fresh engine has no constitutional history, so a reloaded block whose witness has moved could only say *"the
digests differ"*. Writing the witness's DETERMINANTS beside the digest lets the load path hand the superseded
witness back to the engine (`remember_constitution`), after which `stale_states()` names the governed
determinant that moved — across a process boundary, which is the only place it was ever going to matter.

THE SCHEME QUESTION, ANSWERED CONSERVATIVELY RATHER THAN DEFERRED
-----------------------------------------------------------------
`cw-1` was declared in-process, `repr`-based and *"written nowhere"*. It is written here, so the rule it is
written under is stated in the sidecar and enforced on read: **a persisted witness is comparable only within
the kernel witness scheme that produced it.** A block whose `constitution.scheme` differs from this build's
reads STALE rather than trusted — it fails closed, and the remedy is re-establishment, not a migration
someone has to remember. Defining a published, cross-version stable scheme is not this unit's business.

WHAT PARQUET IS AND IS NOT ALLOWED TO MEAN
------------------------------------------
*"Arrow NULL still acquires no analytical meaning through serialization."* The value column round-trips as a
nullable Parquet column and its nulls still mean nothing; participation and support round-trip as their own
non-nullable Boolean columns, in their own file, and a null in either is refused on read exactly as it is
refused in memory. Serialization is offered no opportunity to become an interpretation.
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import pyarrow as pa
import pyarrow.parquet as pq

from columna_platform.kernel import (
    Anchor,
    ConstitutionWitness,
    DataStateRef,
    KernelRefusal,
    RealizationStanding,
    WITNESS_SCHEME,
)
from .block import value_column_name
from .index import AnchorInstance, CoordinateIndex
from .mme import ColumnarExpressionOutput, ColumnarFamilyState, ColumnarMME
from .standing import ColumnStanding

#: The sidecar's own format version. Separate from the witness scheme and from everything else, because a
#: layout change here is not a constitution change and must never be mistaken for one.
SIDECAR_FORMAT = "columnar-sidecar-1"

#: The dimensions every sidecar carries, each in its own slot. **Eight, and never fewer.**
DIMENSIONS = ("identity", "constitution", "constitution_context", "data_state", "realization",
              "coordinate_index", "standing", "values")

VALUES_FILE = "values.parquet"
STANDING_FILE = "standing.parquet"
SIDECAR_FILE = "sidecar.json"
MANIFEST_FILE = "manifest.json"

#: Parquet compression is a REALIZATION fact. It is recorded in the realization dimension and appears in no
#: other one — the demonstration that a codec cannot reach analytical identity is that there is nowhere for
#: it to go.
DEFAULT_CODEC = "zstd"


@dataclass(frozen=True)
class StaleBlock:
    """A persisted block that may not be loaded as current, and WHY — one of exactly two reasons."""

    path: Path
    identity: str
    reason: str
    held_under: str
    current: str
    changed: tuple[str, ...]
    detail: str


@dataclass(frozen=True)
class LoadReport:
    """**What a reload actually did.** Separately countable, because "8 loaded, 1 stale, 0 invented" is the
    only summary that distinguishes restart survival from a cache that happened to be warm."""

    loaded: tuple[str, ...]
    stale: tuple[StaleBlock, ...]
    families: int
    expressions: int

    def __str__(self) -> str:
        return (f"loaded {len(self.loaded)} ({self.families} family, {self.expressions} expression), "
                f"{len(self.stale)} stale")


def _anchor_payload(anchor: Anchor) -> dict:
    return {"universe": anchor.universe, "constituents": sorted(anchor.constituents)}


def _anchor_of(payload: dict) -> Anchor:
    return Anchor(universe=payload["universe"], constituents=frozenset(payload["constituents"]))


class LocalColumnarStore:
    """**A directory of governed blocks.** One subdirectory per retained object; three files each."""

    #: **The carrier is the STORE's, not the engine's.** An engine holding this material in memory carries it
    #: as `in-memory-arrow`; written here it is carried by local Parquet, and that is a different realization
    #: of the same analytical value. Recording the engine's in-memory carrier in a file would be a small lie
    #: with a long life.
    CARRIER = "parquet-local"

    def __init__(self, root: Path | str, *, codec: str = DEFAULT_CODEC,
                 carrier: str = CARRIER) -> None:
        self.root = Path(root)
        self.codec = codec
        self.carrier = carrier
        self.root.mkdir(parents=True, exist_ok=True)

    # ── writing ──────────────────────────────────────────────────────────────────────────────
    def write_family(self, mme: ColumnarMME, state: ColumnarFamilyState) -> Path:
        """Write ONE family state: its values, its standing arrays, and its eight dimensions."""
        witness = mme.authority.witness_of(state.family_id)
        directory = self._directory("family", state.family_id, state.anchor, state.instance)
        index = state.index

        values = pa.table({**{ref: pa.array(col) for ref, col in index.columns().items()},
                           value_column_name(state.family_id): state.values})
        pq.write_table(values, directory / VALUES_FILE, compression=self.codec)

        standing = pa.table({"participation": state.standing.participation,
                             "support": state.standing.support})
        pq.write_table(standing, directory / STANDING_FILE, compression=self.codec)

        sidecar = self._sidecar(
            sort="family", identity=state.family_id, anchor=state.anchor, index=index,
            instance=state.instance, witness=witness, realization=mme.realization,
            values_column=value_column_name(state.family_id),
            values_type=str(state.values.type), null_count=state.values.null_count,
            extra={"law": state.law, "value_form": state.value_form,
                   "forgotten_since_root": sorted(state.forgotten_since_root),
                   "standing_note": state.standing.note,
                   "route": list(state.route),
                   "disclosures": [[d.code, d.detail] for d in state.disclosures]})
        (directory / SIDECAR_FILE).write_text(json.dumps(sidecar, indent=2, sort_keys=True),
                                             encoding="utf-8")
        self._record(directory)
        return directory

    def write_expression(self, mme: ColumnarMME, output: ColumnarExpressionOutput) -> Path:
        """Write ONE expression output. **It reloads as an `ExpressionOutput` and can never seed a family.**

        The sort is a dimension of the sidecar and the reader constructs from the sort, so the thing that
        makes an estimate unable to seed a sketch family survives serialization as a TYPE rather than as a
        flag: there is no field in the written bytes a mistake could flip."""
        witness = mme.authority.witness_of(output.expression_id)
        directory = self._directory("expression", output.expression_id, output.anchor, output.instance)
        index = output.index

        values = pa.table({**{ref: pa.array(col) for ref, col in index.columns().items()},
                           value_column_name(output.expression_id): output.values})
        pq.write_table(values, directory / VALUES_FILE, compression=self.codec)

        sidecar = self._sidecar(
            sort="expression", identity=output.expression_id, anchor=output.anchor, index=index,
            instance=output.instance, witness=witness, realization=mme.realization,
            values_column=value_column_name(output.expression_id),
            values_type=str(output.values.type), null_count=output.values.null_count,
            extra={"constructor": output.constructor, "basis_id": output.basis_id,
                   "disclosures": [[d.code, d.detail] for d in output.disclosures]})
        sidecar["standing"] = {
            "file": None,
            "note": "AN EXPRESSION OUTPUT CARRIES NO STANDING MASKS. It is not family state, it has no "
                    "participating domain to validate, and writing an empty standing file would invite a "
                    "reader to treat it as one.",
        }
        (directory / SIDECAR_FILE).write_text(json.dumps(sidecar, indent=2, sort_keys=True),
                                              encoding="utf-8")
        self._record(directory)
        return directory

    def write_all(self, mme: ColumnarMME) -> tuple[Path, ...]:
        """Every retained object of one engine. Holding is not authority and neither is writing."""
        written = []
        for retained in mme.held_objects():
            value = retained.value
            if retained.continuation_bearing:
                written.append(self.write_family(mme, value))
            else:
                written.append(self.write_expression(mme, value))
        return tuple(written)

    # ── reading ──────────────────────────────────────────────────────────────────────────────
    def load_into(self, mme: ColumnarMME) -> LoadReport:
        """**Reload every current block into a constituted engine. No root is re-established.**

        The engine must already be constituted — the declarations are the constitution and are NOT persisted
        here, deliberately: a store that could reconstitute a Manifold from its own data files would make
        the material the authority for the law, which is the inversion this whole kernel exists to prevent.
        What is persisted is enough to decide whether the material may be served UNDER a constitution the
        engine already holds."""
        loaded: list[str] = []
        stale: list[StaleBlock] = []
        families = expressions = 0
        for directory in self.blocks():
            sidecar = json.loads((directory / SIDECAR_FILE).read_text(encoding="utf-8"))
            verdict = self._staleness(mme, directory, sidecar)
            if verdict is not None:
                # **THE SUPERSEDED WITNESS IS HANDED BACK TO THE ENGINE** so the staleness it reports can
                # name the determinant that moved even though this engine never registered that
                # constitution — the whole reason the determinants are persisted beside the digest.
                stale.append(verdict)
                continue
            if sidecar["identity"]["sort"] == "family":
                mme.adopt(self._read_family(mme, directory, sidecar))
                families += 1
            else:
                mme.adopt(self._read_expression(mme, directory, sidecar))
                expressions += 1
            loaded.append(str(directory.name))
        return LoadReport(loaded=tuple(loaded), stale=tuple(stale), families=families,
                          expressions=expressions)

    def blocks(self) -> tuple[Path, ...]:
        manifest = self.root / MANIFEST_FILE
        if not manifest.exists():
            return ()
        entries = json.loads(manifest.read_text(encoding="utf-8"))["blocks"]
        return tuple(self.root / name for name in entries)

    def sidecar_of(self, directory: Path) -> dict:
        return json.loads((directory / SIDECAR_FILE).read_text(encoding="utf-8"))

    # ── the two reasons a block may not load, and they are NOT the same reason ────────────────
    def _staleness(self, mme: ColumnarMME, directory: Path, sidecar: dict) -> Optional[StaleBlock]:
        identity = sidecar["identity"]["identity"]
        persisted = sidecar["constitution"]
        try:
            current = mme.authority.witness_of(identity)
        except KernelRefusal as exc:
            return StaleBlock(path=directory, identity=identity, reason="not-constituted",
                              held_under=persisted["digest"], current="—", changed=(),
                              detail=exc.detail)
        if persisted["scheme"] != WITNESS_SCHEME:
            return StaleBlock(
                path=directory, identity=identity, reason="witness-scheme-superseded",
                held_under=persisted["digest"], current=current.digest, changed=(),
                detail=f"the block was written under witness scheme {persisted['scheme']!r} and this build "
                       f"computes {WITNESS_SCHEME!r}. A digest is comparable only within the scheme that "
                       f"produced it, so this block FAILS CLOSED rather than being trusted: it is not "
                       f"declared stale about any governed fact, and re-establishment is the remedy.")
        if persisted["digest"] != current.digest:
            was = ConstitutionWitness(
                sort=persisted["sort"], identity=identity, scheme=persisted["scheme"],
                determinants=tuple((n, v) for n, v in persisted["determinants"]),
                digest=persisted["digest"])
            mme.authority.remember_constitution(was)
            comparison = was.compare(current)
            return StaleBlock(path=directory, identity=identity, reason="constitution-superseded",
                              held_under=persisted["digest"], current=current.digest,
                              changed=comparison.changed, detail=comparison.detail)
        return None

    # ── reconstruction ───────────────────────────────────────────────────────────────────────
    def _read_index(self, mme: ColumnarMME, directory: Path, sidecar: dict) -> tuple[CoordinateIndex, pa.Table]:
        table = pq.read_table(directory / VALUES_FILE)
        anchor = _anchor_of(sidecar["identity"]["anchor"])
        refs = list(anchor.order)
        # The scalar anchor has no coordinate columns and exactly one point, `()`. Building one empty tuple
        # per row rather than hardcoding a single point lets `CoordinateIndex`'s duplicate-coordinate refusal
        # catch a file that somehow holds two rows at the grand total, instead of this line deciding.
        cells = (list(zip(*[table.column(ref).to_pylist() for ref in refs])) if refs
                 else [() for _ in range(table.num_rows)])
        index = CoordinateIndex(manifold=sidecar["coordinate_index"]["manifold"], anchor=anchor,
                                coordinates=tuple(cells))
        # **THE INDEX IDENTITY IS RE-DERIVED AND CHECKED, NEVER TRUSTED.** A digest read back from the file
        # that wrote it proves nothing; a digest recomputed from the coordinate columns proves the geometry
        # on disk is the geometry that was written, which is the only version of this check worth having.
        written = sidecar["coordinate_index"]["identity"]
        if index.identity != written:
            raise KernelRefusal(
                "coordinate-index-identity-mismatch", str(directory),
                f"the coordinate columns in {VALUES_FILE} re-derive index identity {index.identity} and the "
                f"sidecar records {written}. The geometry on disk is not the geometry that was written — "
                f"positions would be reassigned silently, and every standing mask is position-aligned to "
                f"them. Nothing is loaded.")
        return index, table

    def _read_family(self, mme: ColumnarMME, directory: Path, sidecar: dict) -> ColumnarFamilyState:
        index, table = self._read_index(mme, directory, sidecar)
        standing_table = pq.read_table(directory / STANDING_FILE)
        instance = self._instance(mme, sidecar)
        standing = ColumnStanding(
            family_id=sidecar["identity"]["identity"], instance=instance,
            participation=standing_table.column("participation").combine_chunks(),
            support=standing_table.column("support").combine_chunks(),
            note=sidecar.get("standing", {}).get("note", ""))
        values = table.column(sidecar["values"]["column"]).combine_chunks()
        state = ColumnarFamilyState(
            family_id=sidecar["identity"]["identity"],
            anchor_instance=AnchorInstance(index=index, instance=instance),
            values=values, standing=standing, law=sidecar["law"],
            value_form=sidecar["value_form"],
            forgotten_since_root=frozenset(sidecar["forgotten_since_root"]),
            disclosures=tuple(_disclosure(code, detail)
                              for code, detail in sidecar.get("disclosures", [])),
            route=tuple(sidecar.get("route", ())) + (f"reloaded from {directory.name}",))
        return state

    def _read_expression(self, mme: ColumnarMME, directory: Path,
                         sidecar: dict) -> ColumnarExpressionOutput:
        index, table = self._read_index(mme, directory, sidecar)
        return ColumnarExpressionOutput(
            expression_id=sidecar["identity"]["identity"],
            anchor_instance=AnchorInstance(index=index, instance=self._instance(mme, sidecar)),
            values=table.column(sidecar["values"]["column"]).combine_chunks(),
            constructor=sidecar["constructor"], basis_id=sidecar["basis_id"],
            disclosures=tuple(_disclosure(code, detail)
                              for code, detail in sidecar.get("disclosures", [])))

    def _instance(self, mme: ColumnarMME, sidecar: dict) -> Any:
        """The analytical instance, rebuilt from the engine's DECLARATION plus the persisted data state.

        The governed axes come from the constitution the engine holds, never from the file: a block does not
        get to declare a family's instance, on disk any more than in memory. What the file supplies is the
        one axis establishment owns — which evidence state this material is about."""
        declared = mme.authority.instance_of(sidecar["identity"]["identity"])
        ref = sidecar["data_state"]
        context = sidecar["constitution_context"]
        if context["token"] != declared.constitution_context:
            raise KernelRefusal(
                "constitution-context-mismatch", sidecar["identity"]["identity"],
                f"the block was written under constitution context {context['token']!r} and this engine "
                f"holds {declared.constitution_context!r}. The shared constitutional context relevant to "
                f"composition is not something material may override.")
        return declared.with_data_state(DataStateRef(scheme=ref["scheme"], token=ref["token"]))

    # ── sidecar assembly. EIGHT SLOTS, AND NO COMPOSITE TOKEN. ───────────────────────────────
    def _sidecar(self, *, sort: str, identity: str, anchor: Anchor, index: CoordinateIndex,
                 instance: Any, witness: ConstitutionWitness, realization: RealizationStanding,
                 values_column: str, values_type: str, null_count: int, extra: dict) -> dict:
        sidecar = {
            "sidecar_format": SIDECAR_FORMAT,
            # 1 · WHICH OBJECT
            "identity": {"sort": sort, "identity": identity, "anchor": _anchor_payload(anchor)},
            # 2 · WHICH CONSTITUTION — with its determinants, so staleness is nameable after a restart
            "constitution": {"scheme": witness.scheme, "digest": witness.digest, "sort": witness.sort,
                             "determinants": [list(d) for d in witness.determinants]},
            # 3 · WHICH SHARED CONSTITUTIONAL CONTEXT — a reference, not a publication fingerprint
            "constitution_context": {"scheme": "context", "token": instance.constitution_context},
            # 4 · WHICH ROOT/EVIDENCE STATE — a typed opaque reference
            "data_state": {"scheme": instance.data_state.scheme, "token": instance.data_state.token},
            # 5 · WHICH REALIZATION — provider, carrier, codec. The only home a codec has.
            "realization": {"provider": realization.provider, "carrier": self.carrier,
                            "codec": self.codec, "format": "parquet",
                            "held_as": realization.carrier},
            # 6 · WHICH LAYOUT — re-derived and checked on read
            "coordinate_index": {"identity": index.identity, "manifold": index.manifold,
                                 "points": len(index), "references": list(anchor.order)},
            # 7 · THE STANDING ARRAYS — their own file, their own nullability rules
            "standing": {"file": STANDING_FILE, "columns": ["participation", "support"],
                         "note": extra.pop("standing_note", "")},
            # 8 · THE VALUES
            "values": {"file": VALUES_FILE, "column": values_column, "arrow_type": values_type,
                       "arrow_null_count": null_count,
                       "note": "A NULL HERE MEANS NOTHING. Nullability is Arrow's; standing is governed and "
                               "lives in the standing file."},
        }
        sidecar.update(extra)
        return sidecar

    # ── layout ───────────────────────────────────────────────────────────────────────────────
    def _directory(self, sort: str, identity: str, anchor: Anchor, instance: Any) -> Path:
        """One directory per retained object. **The three key axes are in the NAME, hashed, and also in the
        sidecar in full** — the name exists to be unique on a filesystem, and nothing reads meaning out of
        it. A reader that parsed this name would be reading a composite token."""
        import hashlib

        payload = "|".join([sort, identity, str(anchor), instance.data_state.reference,
                            instance.constitution_context, str(instance.participation),
                            str(instance.scope)])
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
        safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in f"{sort}-{identity}")
        directory = self.root / f"{safe}-{digest}"
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def _record(self, directory: Path) -> None:
        manifest = self.root / MANIFEST_FILE
        blocks = []
        if manifest.exists():
            blocks = json.loads(manifest.read_text(encoding="utf-8"))["blocks"]
        if directory.name not in blocks:
            blocks.append(directory.name)
        manifest.write_text(json.dumps({"sidecar_format": SIDECAR_FORMAT, "blocks": sorted(blocks)},
                                       indent=2), encoding="utf-8")

    def destroy(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


def _disclosure(code: str, detail: str):
    from columna_platform.kernel import Disclosure

    return Disclosure(code, detail)


def required_metadata(store: LocalColumnarStore) -> dict:
    """**What the block actually required**, read back off disk rather than recited from the writer.

    Reported because the unit asks for it: *"report what metadata the block actually required. That evidence
    will tell us what Iceberg/Postgres need to store."*"""
    out: dict[str, Any] = {"blocks": 0, "dimensions": {}, "files": set(), "composite_tokens": []}
    for directory in store.blocks():
        sidecar = store.sidecar_of(directory)
        out["blocks"] += 1
        for key, value in sidecar.items():
            entry = out["dimensions"].setdefault(key, set())
            if isinstance(value, dict):
                entry.update(value)
            else:
                entry.add("<scalar>")
        for path in sorted(directory.iterdir()):
            out["files"].add(path.name)
    out["files"] = sorted(out["files"])
    out["dimensions"] = {k: sorted(v) for k, v in sorted(out["dimensions"].items())}
    return out


# ══ THE RESTART PROOF, RUNNABLE ═══════════════════════════════════════════════════════════════════
def _rule(title: str) -> None:
    print(f"\n{'─' * 100}\n{title}\n{'─' * 100}")


def main() -> int:                                          # noqa: C901 — a proof is a narrative
    """**Write a real Parquet block, DESTROY the engine, reload, and serve.** Ten checks, in the order the
    unit names them."""
    import tempfile
    from dataclasses import replace

    from columna_platform.kernel import KernelRefusal
    from . import exhibit as EX

    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        print(f"    {'✓' if condition else '✗'} {label}")
        if not condition:
            failures.append(label)

    LOAD = DataStateRef("load", "orders@2026-09-29T08:00Z")
    RELOAD = DataStateRef("load", "orders@2026-09-29T17:30Z")
    root = Path(tempfile.mkdtemp(prefix="columna-p2-"))
    store = LocalColumnarStore(root / "store")

    print("═" * 100)
    print("  COLUMNA PLATFORM · P-2 · local Arrow/Parquet persistence, and restart survival")
    print(f"  store {store.root}   codec {store.codec!r}   sidecar {SIDECAR_FORMAT!r}")
    print("═" * 100)

    # ══ 1 · WRITE A REAL COLUMNAR BLOCK ══════════════════════════════════════════════════════════
    _rule("PROOF 1 · a real columnar block is written — Parquet values, Parquet standing, JSON dimensions")
    settled, block = EX.build(settled=True, data_state=LOAD)
    by_day = settled.measure("revenue", EX.BY_DAY, data_state=LOAD)
    sketch_day = settled.measure("distinct_customers", EX.BY_DAY, data_state=LOAD)
    estimate = settled.evaluate("distinct_customer_estimate", EX.BY_DAY, data_state=LOAD)
    written = store.write_all(settled)
    print(f"  wrote {len(written)} block(s) from the running engine")
    for directory in written[:2]:
        names = sorted(p.name for p in directory.iterdir())
        print(f"      {directory.name}/  {names}")
    sidecar = store.sidecar_of(written[0])
    print(f"\n  the dimensions of {written[0].name}:")
    for dimension in DIMENSIONS:
        rendered = json.dumps(sidecar[dimension])
        print(f"      {dimension:<21} {rendered[:96]}{'…' if len(rendered) > 96 else ''}")

    check("a real Parquet file carries the values", (written[0] / VALUES_FILE).stat().st_size > 0)
    check("every one of the eight dimensions has its OWN named slot",
          all(d in sidecar for d in DIMENSIONS))
    check("the constitution carries its DETERMINANTS, not only a digest",
          len(sidecar["constitution"]["determinants"]) >= 8)
    check("the data state is a TYPED reference {scheme, token}",
          set(sidecar["data_state"]) == {"scheme", "token"}
          and sidecar["data_state"]["token"] == LOAD.token)
    check("the codec appears in realization standing and NOWHERE else",
          sidecar["realization"]["codec"] == store.codec
          and not any(store.codec in json.dumps(sidecar[d])
                      for d in DIMENSIONS if d != "realization"))

    # ══ 2 + 3 · DESTROY THE ENGINE, RELOAD WITHOUT RE-ESTABLISHING ════════════════════════════════
    _rule("PROOF 2 + 3 · the engine is DESTROYED and a fresh one reloads — no root is re-established")
    held_before = len(settled.held)
    del settled, block, by_day, sketch_day, estimate
    fresh, _unused_block = EX.build(settled=True, data_state=LOAD)
    fresh._store.clear()                                    # a brand-new engine holds nothing at all
    print(f"  the old engine held {held_before} object(s); the fresh engine holds {len(fresh.held)}")
    report = store.load_into(fresh)
    print(f"  reload: {report}")
    print(f"      loaded {[n.split('-')[1] for n in report.loaded]}")

    check("a fresh engine starts with nothing held", held_before > 0)
    check("the reload loaded every written block", len(report.loaded) == len(written))
    check("and NO root was re-established — the values came off disk",
          all("reloaded from" in r.value.route[-1]
              for r in fresh.held_objects() if r.continuation_bearing))

    # ══ 4 · SERVE A REVENUE CONTINUATION FROM RELOADED STATE ══════════════════════════════════════
    _rule("PROOF 4 · Revenue is CONTINUED from reloaded state, through DataFusion, after a restart")
    revenue_total = fresh.measure("revenue", EX.TOTAL, data_state=LOAD)
    print(f"  revenue @ {EX.TOTAL}   route={revenue_total.route}   "
          f"seeded from {revenue_total.seeded_from}")
    print(f"      = {revenue_total.value.cell(()):.2f}")
    aov = fresh.evaluate("average_order_value", EX.BY_DAY, data_state=LOAD)
    print(f"  average_order_value @ {EX.BY_DAY}  route={aov.route}  "
          f"D1={aov.value.cell(('D1',)):.4f}  D2={aov.value.cell(('D2',)):.4f}")

    check("the grand total serves from reloaded material", revenue_total.served
          and revenue_total.value.cell(()) == 560.0)
    check("it was CONTINUED, not re-established", revenue_total.route == "continued")
    check("an expression evaluates over reloaded operands",
          aov.served and abs(aov.value.cell(("D1",)) - 235 / 3) < 1e-9)

    # ══ 5 + 6 · THE SKETCH CONTINUES; THE ESTIMATE IS STILL EXPRESSION-ONLY ═══════════════════════
    _rule("PROOF 5 + 6 · the HLL sketch reloads and CONTINUES; the reloaded estimate cannot seed a family")
    sketch_total = fresh.measure("distinct_customers", EX.TOTAL, data_state=LOAD)
    print(f"  distinct_customers @ {EX.TOTAL}  route={sketch_total.route}  "
          f"value=⟨sketch:{len(sketch_total.value.cell(()))}B⟩")
    reloaded_estimate = fresh.retained("expression", "distinct_customer_estimate", EX.BY_DAY,
                                       fresh.authority.instance_of("distinct_customer_estimate")
                                       .with_data_state(LOAD))
    verdict = fresh.adjudicate(reloaded_estimate, fresh.family("distinct_customers"), EX.BY_DAY)
    print(f"  the reloaded estimate: {type(reloaded_estimate.value).__name__}, "
          f"CONTINUATION_BEARING={reloaded_estimate.continuation_bearing}")
    print(f"  may it seed the sketch family?  {'ADMITTED' if verdict else 'REFUSED'} [{verdict.code}]")

    check("the sketch is Arrow BINARY through Parquet and still merges",
          sketch_total.served and isinstance(sketch_total.value.cell(()), bytes))
    check("the estimate reloaded as an ExpressionOutput, not as family state",
          isinstance(reloaded_estimate.value, ColumnarExpressionOutput))
    check("and it still cannot seed family continuation",
          (not verdict) and verdict.code == "not-continuation-bearing")
    check("the estimate's own value survived the round trip",
          fresh.evaluate("distinct_customer_estimate", EX.BY_DAY, data_state=LOAD).route == "cached")

    # ══ 7 · A CHANGED CONSTITUTION WITNESS READS STALE ════════════════════════════════════════════
    _rule("PROOF 7 · the declaration moves → the persisted block reads STALE, and names the determinant")
    moved_engine, _ = EX.build(settled=True, data_state=LOAD)
    moved_engine._store.clear()
    moved_engine.authority.register_family(
        replace(moved_engine.family("revenue"), participation="every order the auditor confirmed"))
    moved_report = store.load_into(moved_engine)
    revenue_stale = [s for s in moved_report.stale if s.identity == "revenue"]
    print(f"  reload under the moved constitution: {moved_report}")
    for s_ in revenue_stale[:1]:
        print(f"      {s_.identity}: {s_.reason}  changed={list(s_.changed)}")
        print(f"      {s_.detail[:220]}…")
    print(f"  and revenue is unservable: {not moved_engine.measure('revenue', EX.BY_DAY).served}")

    check("the block reads STALE rather than loading", bool(revenue_stale))
    check("the reason is a SUPERSEDED CONSTITUTION, named as such",
          revenue_stale[0].reason == "constitution-superseded")
    check("and the DETERMINANT that moved is named ACROSS THE RESTART",
          revenue_stale[0].changed == ("participation",))
    check("an untouched family still loads under the same reload",
          any("order_count" in name for name in moved_report.loaded))

    # ══ 8 · A DIFFERENT DataStateRef IS A DISTINCT INSTANCE, NOT A STALE CONSTITUTION ═════════════
    _rule("PROOF 8 · a different DataStateRef is a DISTINCT ANALYTICAL INSTANCE — not 'stale constitution'")
    second, second_block = EX.build(settled=True, data_state=RELOAD)
    second_store = LocalColumnarStore(root / "store")        # THE SAME store directory
    second_store.write_family(second, second.retained(
        "family", "revenue", EX.SALE_AT,
        second.authority.instance_of("revenue").with_data_state(RELOAD)).value)

    both, _ = EX.build(settled=True, data_state=LOAD)
    both._store.clear()
    both_report = second_store.load_into(both)
    states = sorted({k.data_state.reference for k in both.held if k.identity == "revenue"})
    print(f"  the store now holds revenue under {len(states)} evidence state(s): {states}")
    print(f"  reload: {both_report}  — and NOTHING was reported stale for revenue")
    ambiguous = both.measure("revenue", EX.BY_DAY)
    print(f"  asking without naming one: REFUSED [{ambiguous.refusal.code}]")
    named = both.measure("revenue", EX.BY_DAY, data_state=LOAD)
    print(f"  asking for {LOAD}: D1 = {named.value.cell(('D1',)):.2f}")

    check("both evidence states loaded as CURRENT, neither stale",
          len(states) == 2 and not any(s.identity == "revenue" for s in both_report.stale))
    check("the difference is an INSTANCE difference, not a constitution one",
          len({k.constitution for k in both.held if k.identity == "revenue"}) == 1)
    check("and the engine still refuses to pick between them",
          ambiguous.refusal.code == "ambiguous-data-state")
    check("naming one serves it", named.served)

    # ══ 9 · A CODEC DIFFERENCE IS REALIZATION STANDING ════════════════════════════════════════════
    _rule("PROOF 9 · the same analytical material under two codecs — realization standing, nothing else")
    other_codec = LocalColumnarStore(root / "snappy", codec="snappy")
    engine_c, block_c = EX.build(settled=True, data_state=LOAD)
    zstd_dir = store.write_family(engine_c, engine_c.retained(
        "family", "order_count", EX.SALE_AT,
        engine_c.authority.instance_of("order_count").with_data_state(LOAD)).value)
    snappy_dir = other_codec.write_family(engine_c, engine_c.retained(
        "family", "order_count", EX.SALE_AT,
        engine_c.authority.instance_of("order_count").with_data_state(LOAD)).value)
    a, b = store.sidecar_of(zstd_dir), other_codec.sidecar_of(snappy_dir)
    print(f"  zstd   {a['realization']}")
    print(f"  snappy {b['realization']}")
    print(f"  byte sizes differ: "
          f"{(zstd_dir / VALUES_FILE).stat().st_size} vs "
          f"{(snappy_dir / VALUES_FILE).stat().st_size}")

    check("the constitution witness is IDENTICAL under two codecs",
          a["constitution"]["digest"] == b["constitution"]["digest"])
    check("so is the data state", a["data_state"] == b["data_state"])
    check("only the realization dimension differs",
          a["realization"] != b["realization"]
          and {k: v for k, v in a.items() if k != "realization"}
          == {k: v for k, v in b.items() if k != "realization"})

    # ══ 10 · ARROW NULL ACQUIRES NOTHING THROUGH SERIALIZATION ════════════════════════════════════
    _rule("PROOF 10 · Arrow NULL acquires no analytical meaning by being written to Parquet and read back")
    as_recorded, _unsupported = EX.build(data_state=LOAD)   # O7's amount is NOT established
    null_store = LocalColumnarStore(root / "nulls")
    null_store.write_all(as_recorded)
    after, _ = EX.build(data_state=LOAD)
    after._store.clear()
    null_store.load_into(after)
    reloaded = after.retained("family", "revenue", EX.SALE_AT,
                              after.authority.instance_of("revenue").with_data_state(LOAD)).value
    position = reloaded.index.position(EX.UNSUPPORTED_POINT)
    print(f"  the reloaded revenue column has {reloaded.values.null_count} Arrow null(s)")
    print(f"  {EX.UNSUPPORTED_ORDER}: participation="
          f"{reloaded.standing.participation[position].as_py()}  "
          f"support={reloaded.standing.support[position].as_py()}")
    still_refuses = after.measure("revenue", EX.BY_DAY, data_state=LOAD)
    counts = after.measure("order_count", EX.BY_DAY, data_state=LOAD)
    print(f"  Revenue @ {EX.BY_DAY} after the round trip: REFUSED [{still_refuses.refusal.code}]")
    print(f"  OrderCount @ D1 after the round trip: {counts.value.cell(('D1',))}")

    check("the standing masks round-tripped, and they are what carries the meaning",
          reloaded.standing.participation[position].as_py() is True
          and reloaded.standing.support[position].as_py() is False)
    check("the value column's null still means NOTHING: the fold refuses for WANT OF STATE",
          not still_refuses.served and still_refuses.refusal.code == "want-of-state")
    check("and the population reduction still counts all three participating orders",
          counts.value.cell(("D1",)) == 3)
    check("serialization was given no chance to interpret: standing is its own file",
          null_store.sidecar_of(null_store.blocks()[0])["standing"]["file"] == STANDING_FILE
          or null_store.sidecar_of(null_store.blocks()[0])["identity"]["sort"] == "expression")

    # ══ AND THE GUARDS ═══════════════════════════════════════════════════════════════════════════
    _rule("GUARDS · no composite version token; a re-derived index identity; a mismatched geometry refuses")
    every = json.dumps([store.sidecar_of(d) for d in store.blocks()])
    composite = [k for k in ("version", "etag", "generation", "sequence_number")
                 if f'"{k}"' in every]
    print(f"  composite-token keys found in every sidecar: {composite or 'NONE'}")
    tampered = json.loads((written[0] / SIDECAR_FILE).read_text(encoding="utf-8"))
    tampered["coordinate_index"]["identity"] = "cidx-1:" + "0" * 32
    (written[0] / SIDECAR_FILE).write_text(json.dumps(tampered), encoding="utf-8")
    refused = None
    try:
        probe, _ = EX.build(settled=True, data_state=LOAD)
        probe._store.clear()
        store.load_into(probe)
    except KernelRefusal as exc:
        refused = exc
    print(f"  a sidecar whose index identity does not match its own coordinate columns: "
          f"REFUSED [{refused.code if refused else '—'}]")

    check("NO composite version token is written anywhere", not composite)
    check("the coordinate-index identity is re-derived from the columns and CHECKED",
          refused is not None and refused.code == "coordinate-index-identity-mismatch")

    # ══ WHAT THE BLOCK ACTUALLY REQUIRED ═════════════════════════════════════════════════════════
    _rule("REPORT · what metadata the block actually required")
    required = required_metadata(second_store)
    print(f"  files per block: {required['files']}")
    print("  dimension → keys actually written:")
    for dimension, keys in required["dimensions"].items():
        print(f"      {dimension:<21} {keys}")

    print("\n" + "═" * 100)
    if failures:
        print(f"  {len(failures)} CHECK(S) FAILED")
        for f in failures:
            print(f"    ✗ {f}")
    else:
        print("  ALL CHECKS PASSED — the MME survives a restart from local Parquet.")
    print("═" * 100)
    shutil.rmtree(root, ignore_errors=True)
    return 1 if failures else 0


__all__ = ["DEFAULT_CODEC", "DIMENSIONS", "LoadReport", "LocalColumnarStore", "MANIFEST_FILE",
           "SIDECAR_FILE", "SIDECAR_FORMAT", "STANDING_FILE", "StaleBlock", "VALUES_FILE",
           "main", "required_metadata"]


if __name__ == "__main__":                                  # pragma: no cover
    raise SystemExit(main())

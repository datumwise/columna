#!/usr/bin/env python3
"""
Reproduction script for the `firstlight` governed fixture. REPO-ONLY — never shipped in a wheel.

Two stages, deliberately separated because they have different audiences and different
reachability:

    --stage producer   authors, ratifies and PUBLISHES the governed publication.
                       Requires manifold-agent (PRIVATE, pinned below) + columna-studio.
                       Runs ONCE. Its output is committed and thereafter immutable.

    --stage runtime    compiles that committed publication, writes the receipt, builds the
                       synthetic warehouse and provisions the runtime unit.
                       Requires ONLY a released columna — anyone can run it.

THE PRODUCER STAGE IS NOT BYTE-REPRODUCIBLE, and that is a property of the format, not a defect
here: `Library.publish` stamps `published_at` from the wall clock, so a second run yields different
bytes and therefore a different publication digest. That is exactly why the artifact is produced
once and committed, and why every downstream guard reads the COMMITTED bytes rather than re-minting
them.

THE RUNTIME STAGE IS BYTE-REPRODUCIBLE, and a test depends on it: recompiling the committed
publication against the committed mapping must reproduce the shipped `manifold.cml` byte for byte.

Producer pin (ruling 2026-08-22): manifold-agent v0.12.0 @ df794a60f5b234f9bb08d1fc85d9dfb081d10316
— the commit the `v0.12.0` tag and columna-studio's dependency pin both point at. NOT a later local
HEAD; a fixture whose provenance disagrees with the only published pin is worse than no fixture.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent.parent / "src" / "columna_server" / "governed" / "firstlight"

MANIFOLD_ID = "firstlight"
VERSION = "1.0.0"
STEWARD = "Huayin Wang"
RATIFIED_AT = "2026-08-22T00:00:00Z"

#: The pinned producer. Asserted, not assumed — see `_require_producer_pin`.
MANIFOLD_AGENT_COMMIT = "df794a60f5b234f9bb08d1fc85d9dfb081d10316"

#: The synthetic world. Six rows, deliberately non-monotonic so `min`/`max` cannot coincide with
#: first/last, and asymmetric across stores so a rolled-up answer differs from any leaf.
ROWS = [
    ("s1", "2026-08-01", 10.0),
    ("s1", "2026-08-02", 3.0),
    ("s1", "2026-08-03", 7.0),
    ("s2", "2026-08-01", 5.0),
    ("s2", "2026-08-02", 40.0),
    ("s2", "2026-08-03", 20.0),
]


# ── stage: producer ──────────────────────────────────────────────────────────────────────────────
def _require_producer_pin(agent_repo: Path) -> str:
    head = subprocess.run(["git", "-C", str(agent_repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    if head != MANIFOLD_AGENT_COMMIT:
        raise SystemExit(
            f"REFUSED: manifold-agent at {agent_repo} is {head}, not the pinned "
            f"{MANIFOLD_AGENT_COMMIT}. The publication's provenance must match the pin "
            f"columna-studio declares; producing it from another commit would make PROVENANCE.md a "
            f"claim about software that did not build this artifact.")
    return head


def produce(agent_repo: Path, studio_repo: Path, out: Path) -> None:
    """Author -> ratify -> stamp -> publish, through the REAL governed-publish path.

    Nothing here is hand-authored: `ratify_existence_law` is the one human mint primitive,
    `stamp_source_identity` runs the P0(c) gate that refuses an unratified universe, and
    `Library.publish` is the emission path that writes the artifact. A hand-written
    governed-publication.json would look identical and prove nothing."""
    _require_producer_pin(agent_repo)

    from manifold_agent.evidence import Status
    from manifold_agent.manifold import Declaration, Manifold

    from columna_studio.apply import MANIFOLD_FILE, ratify_existence_law, stamp_source_identity
    from columna_studio.library import Library
    from columna_studio.publishing import PublishPlan

    # The logical world. K0 scope exactly: an anchor, an UNRESTRICTED universe over it, one measure,
    # four members. No hierarchy, no relationship, no attribute, no restriction, no derived measure.
    decls = (
        Declaration("anchor", "sale_at",
                    {"components": [{"name": "store", "type": "text"},
                                    {"name": "day", "type": "date"}]}, Status.ASSUMED),
        Declaration("universe", "sales",
                    {"basis": "events", "anchor": "sale_at"}, Status.ASSUMED),
        Declaration("measure", "revenue",
                    {"value_type": "decimal", "root_member": "revenue_sum"}, Status.ASSUMED),
    ) + tuple(
        Declaration("member", f"revenue_{agg}",
                    {"measure": "revenue", "anchor": "sale_at", "universe": "sales"},
                    Status.ASSUMED)
        for agg in ("sum", "count", "min", "max")
    )

    work = out / "_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    (work / MANIFOLD_FILE).write_text(Manifold(declarations=decls).to_yaml(), encoding="utf-8")

    # THE ONE HUMAN MINT PATH. A ratification is derivable from the logical model alone — no
    # warehouse, no data, no gate evidence — but it is never derived automatically: it names the
    # steward who authorized this population law as the whole intended law.
    ratify_existence_law(work, "sales", steward=STEWARD, at=RATIFIED_AT)

    # P0(c): consumes authority, never manufactures it. Refuses an unratified or stale universe.
    stamp_source_identity(work, manifold_id=MANIFOLD_ID, version=VERSION)

    ws = out / "_workspace"
    if ws.exists():
        shutil.rmtree(ws)
    lib = Library(ws)
    plan = PublishPlan(version=VERSION, prev_version=None,
                       the_banner={"declarations": len(decls), "verified": 0},
                       deltas=[], changelog=f"# {VERSION}\n", blockers=[])
    lib.publish(MANIFOLD_ID, plan, artifacts_folder=work, events=[], actor=STEWARD, overrides={})

    published = ws / "library" / MANIFOLD_ID / VERSION
    shutil.copy2(published / "governed-publication.json", HERE / "governed-publication.json")
    shutil.copy2(work / MANIFOLD_FILE, HERE / "manifold.yaml")
    print(f"produced governed-publication.json  ({(HERE / 'governed-publication.json').stat().st_size} bytes)")
    print("authored manifold.yaml retained for reproduction")
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(ws, ignore_errors=True)


# ── stage: runtime ───────────────────────────────────────────────────────────────────────────────
def build_runtime() -> None:
    """Compile the COMMITTED publication with the SHIPPED compiler, then provision.

    Everything here is byte-reproducible. Nothing is hand-written: the image comes from
    `compile_k0`, the receipt from `build_receipt`, and the unit from `provision_runtime_unit` —
    the same generic machinery a user gets from PyPI, with no fixture-specific branch anywhere."""
    import duckdb
    import columna_core
    from columna_core.compiler import (build_receipt, compile_k0, parse_mapping,
                                       parse_publication, render_receipt)
    from columna_server.lowering_receipt import LOWERING_RECEIPT
    from columna_server.provision import provision_runtime_unit

    pub_bytes = (HERE / "governed-publication.json").read_bytes()
    mapping = json.loads((HERE / "private-core-mapping.json").read_text(encoding="utf-8"))

    image = compile_k0(parse_publication(json.loads(pub_bytes)), parse_mapping(mapping))
    receipt = build_receipt(
        manifold_id=image.manifold_id, version=image.version,
        publication_bytes=pub_bytes, image_bytes=image.encode(),
        compiler_name="columna-core-p1-k0", compiler_version=columna_core.__version__,
        mapping_provenance={"mapping_format_version": mapping["mapping_format_version"]},
        established_at="2026-08-22T00:00:00Z")

    staging = HERE / "_staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    (staging / "governed-publication.json").write_bytes(pub_bytes)
    (staging / "manifold.cml").write_bytes(image.encode())
    (staging / LOWERING_RECEIPT).write_text(render_receipt(receipt), encoding="utf-8")

    # the synthetic warehouse — written before provisioning so the unit is complete when it lands
    if RUNTIME.exists():
        shutil.rmtree(RUNTIME)
    RUNTIME.parent.mkdir(parents=True, exist_ok=True)

    provision_runtime_unit(
        str(RUNTIME),
        publication=str(staging / "governed-publication.json"),
        image=str(staging / "manifold.cml"),
        receipt=str(staging / LOWERING_RECEIPT),
        data_toml=(
            "# The first governed runtime unit. Assembled by columna_server.provision from a\n"
            "# publication this release can serve and cannot make — see PROVENANCE.md.\n"
            "# The warehouse path is relative to THIS directory, so the unit is self-contained.\n"
            '[manifold]\n'
            'name = "Firstlight (governed)"\n'
            'description = "The first public governed fixture: a legitimate governed publication, '
            'compiled and provisioned through the generic path."\n\n'
            '[connector]\n'
            'type = "duckdb"\n'
            'warehouse = "./warehouse"\n'
        ))
    shutil.rmtree(staging)

    wh = RUNTIME / "warehouse"
    wh.mkdir()
    con = duckdb.connect()
    con.execute("CREATE TABLE sales_lines (store_id VARCHAR, sale_date VARCHAR, amount DOUBLE)")
    con.executemany("INSERT INTO sales_lines VALUES (?,?,?)", ROWS)
    con.execute(f"COPY sales_lines TO '{wh / 'sales_lines.parquet'}' (FORMAT PARQUET)")
    con.close()

    total = sum(f.stat().st_size for f in RUNTIME.rglob("*") if f.is_file())
    print(f"provisioned {RUNTIME} ({total / 1024:.1f} KB)")
    for f in sorted(RUNTIME.rglob("*")):
        if f.is_file():
            print(f"   {f.relative_to(RUNTIME)}  {f.stat().st_size} B")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=("producer", "runtime"), required=True)
    ap.add_argument("--manifold-agent", type=Path, help="path to a manifold-agent checkout at the pin")
    ap.add_argument("--columna-studio", type=Path, help="path to a columna-studio checkout")
    a = ap.parse_args()
    if a.stage == "producer":
        if not a.manifold_agent or not a.columna_studio:
            raise SystemExit("--stage producer needs --manifold-agent and --columna-studio")
        produce(a.manifold_agent, a.columna_studio, HERE)
    else:
        build_runtime()


if __name__ == "__main__":
    main()

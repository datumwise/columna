# Columna

**Columna** is a correctness-governed analytic framework built on a column-processing foundation:
the backend *delivers* column-atoms, and every relating of columns across anchors happens inside the
**column engine** as an explicit anchor-aligned **transport** — never a pushed-down join. Fan-out,
non-reconciling reaggregation, and out-of-domain addressing are made *inexpressible* rather than
caught after the fact. See `specs/context/adr_031_columna_core.md` and `adr_032_columna_engine.md`
for the architecture.

This repository is the Datumwise monorepo.

## Layout

```
packages/
  columna-core/     the open-source Core library (this is what ships today)
  columna-server/   placeholder — the server package (roadmap)
apps/
  website/          placeholder
docs/               placeholder (WP-4.2)
research/           pointers: Atlas, Two-Anchors, the benchmark
specs/              the work-package specs and ADR context
```

## Quickstart

```bash
pip install -e packages/columna-core
python -c "import columna_core; print(columna_core.__version__)"
```

Run the proof demos (they ship with the benchmark warehouse):

```bash
cd packages/columna-core/demos
python build_benchmark.py     # 10 real-data proofs (transport, fan-out refusal, B-anchor, …)
python parse_benchmark.py     # the same proofs on a Manifold parsed from benchmark.cml
```

Run the tests (fixture-backed, no network, < 90 s):

```bash
pytest packages/columna-core -q
# full real-warehouse validation (opt-in):
COLUMNA_BENCH_WAREHOUSE=packages/columna-core/demos/warehouse pytest packages/columna-core -m warehouse -q
```

## Links

- Core package: [`packages/columna-core`](packages/columna-core)
- Architecture: [ADR-031](specs/context/adr_031_columna_core.md),
  [ADR-032](specs/context/adr_032_columna_engine.md)

## License

Apache-2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

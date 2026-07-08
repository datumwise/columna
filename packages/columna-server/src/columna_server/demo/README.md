# Packaged demo data (drift-guarded copy of the core fixtures)

`manifold.cml` and `warehouse/*.parquet` here are **byte-identical copies** of the columna-core test
fixtures (`packages/columna-core/tests/fixtures/benchmark.cml` and `.../mini_warehouse/`), so the
packaged demo ships a self-contained ≤ 2 MB Manifold that `columna-server demo` can run with no path
arguments. `tests/test_demo_data_drift.py` enforces the byte-identity — refresh these copies from the
core fixtures if that guard ever fails.

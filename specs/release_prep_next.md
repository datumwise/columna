# Next release — prep checklist

Carry-forward items that must not miss the next flip. Rowed here at the moment they were noticed, so
the next release picks them up first, not last.

1. **PyPI meta description → "framework."** The `columna` metapackage's `description`
   (`packages/columna/pyproject.toml`) still reads *"honest metrics engine"* and shipped that way to
   PyPI at 0.11.0 — the positioning sweep (Manifold · FrameQL · honest engine = a **data framework**)
   reached the site but missed the package string, because a string alone doesn't justify spinning a
   release. Change it to the framework register (e.g. *"Columna, by datumwise — an honest data framework
   (Manifold, FrameQL, an honest engine). Metapackage: installs columna-core + columna-server."*) with
   the next release, and **verify it renders on the PyPI project page** after publish.

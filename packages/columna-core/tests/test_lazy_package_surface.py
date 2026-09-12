"""The package surface is LAZY, and that must cost nothing observable.

Two properties, and the second is the reason the first exists:

  1. every supported package-level name still resolves, to the SAME OBJECT as before;
  2. importing a neutral/successor module does not drag the legacy execution stack into the
     interpreter as a side effect.

Before PEP 562 landed here, `import columna_core.serving_contract` executed `__init__`, which
imported `planner` — and with it `engine`, `model`, `projection`, `frameql`, `expr`, `connector` and
duckdb. The static import graph said the neutral module was clean; the running interpreter said
otherwise, and the interpreter was right.
"""
import subprocess
import sys
from importlib import import_module

import columna_core
from columna_core import _EXPORTS, _MODULE_ALIASES

#: the legacy execution stack a successor/neutral import must not pull in
BANNED = {"planner", "engine", "model", "adjudication", "parser", "projection", "frameql",
          "expr", "connector"}

#: what Proof A and any successor path actually import
NEUTRAL = ["columna_core.serving_contract", "columna_core.disclosure",
           "columna_core.disclosure_wire", "columna_core.governed.publication",
           "columna_core.governed.resolve", "columna_core.compiler.realization"]


# ── property 1 · the surface is unchanged ────────────────────────────────────────────────────────
def test_every_public_name_resolves():
    missing = [n for n in columna_core.__all__ if not hasattr(columna_core, n)]
    assert missing == []


def test_every_public_name_is_the_same_object_as_its_submodule_attribute():
    """`from columna_core import X` and `from columna_core.x import X` must not become two things."""
    for name, (mod, attr) in _EXPORTS.items():
        assert getattr(columna_core, name) is getattr(import_module(f"columna_core.{mod}"), attr), name
    for name, mod in _MODULE_ALIASES.items():
        assert getattr(columna_core, name) is import_module(f"columna_core.{mod}"), name


def test_the_export_table_covers_all():
    """`__all__` is checked against the table by this test rather than by eye."""
    assert set(columna_core.__all__) <= set(_EXPORTS) | set(_MODULE_ALIASES)


def test_repeated_access_is_stable():
    assert columna_core.Planner is columna_core.Planner
    assert columna_core.FrameResult is columna_core.serving_contract.FrameResult


def test_dir_still_lists_the_surface():
    d = set(dir(columna_core))
    assert set(columna_core.__all__) <= d


def test_an_unknown_name_still_raises_attribute_error():
    try:
        columna_core.NoSuchName
    except AttributeError as e:
        assert "NoSuchName" in str(e)
    else:                                                    # pragma: no cover
        raise AssertionError("a missing attribute must raise, not resolve")


# ── property 2 · the execution stack is not loaded by a neutral import ───────────────────────────
def _loaded_in_clean_interpreter(imports: list) -> set:
    """Run in a SUBPROCESS. In-process this is unassertable: any earlier test may have imported the
    stack already, and a test that passes because of collection order is not a test."""
    prog = ("import sys\n"
            + "".join(f"import {m}\n" for m in imports)
            + "print('MODS', ' '.join(sorted(m.split('.')[1] for m in sys.modules "
              "if m.startswith('columna_core.') and m.count('.') == 1)))\n"
            + "print('DUCKDB', 'duckdb' in sys.modules)\n")
    out = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True, check=True)
    # PREFIXED, not positional: with nothing loaded the modules line is EMPTY, and `.strip()` on a
    # positional parse silently ate it — the failure mode being tested is exactly "nothing loaded".
    lines = {ln.split(" ", 1)[0]: ln.split(" ", 1)[1] if " " in ln else ""
             for ln in out.stdout.splitlines()}
    return set(lines["MODS"].split()), lines["DUCKDB"] == "True"


def test_a_neutral_import_does_not_load_the_execution_stack():
    loaded, _ = _loaded_in_clean_interpreter(NEUTRAL)
    assert not (loaded & BANNED), f"neutral import pulled in {sorted(loaded & BANNED)}"


def test_a_neutral_import_does_not_load_duckdb():
    """The dependency behind `connector`. Loading a database driver to read a contract type is the
    concrete cost this change removes."""
    _, duckdb_loaded = _loaded_in_clean_interpreter(NEUTRAL)
    assert duckdb_loaded is False


def test_importing_the_package_alone_loads_nothing_heavy():
    loaded, _ = _loaded_in_clean_interpreter(["columna_core"])
    assert not (loaded & BANNED)


def test_asking_for_an_execution_name_still_loads_it():
    """Laziness must not become unavailability — the compatibility half of the property."""
    prog = ("import sys, columna_core\n"
            "p = columna_core.Planner\n"
            "assert 'columna_core.planner' in sys.modules\n"
            "assert p is sys.modules['columna_core.planner'].Planner\n"
            "print('ok')\n")
    out = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "ok"

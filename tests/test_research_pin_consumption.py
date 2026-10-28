"""Template-family custody pins must name the Python each tree consumes.

On 2026-09-24 the research trees that share the template
``verify_sources.py`` were repinned from a measurement of what each one
consumes.  Until then most of them pinned ``code/derivation/iso.py`` and
``code/derivation/model.py``, which they never import, and left the sibling
modules they do import unpinned, so their PASS certified nothing they read.

This test re-measures the Python half of that measurement, per tree:

* a child interpreter imports every Python file of the tree, with the tree
  first on ``sys.path`` and ``code/`` last (the root pytest ``pythonpath``),
  then imports every module name the tree imports anywhere, including inside
  functions;
* it reads ``sys.modules`` for modules inside the repository and outside the
  tree;
* the test fails naming each such module the manifest does not pin, and
  each pinned Python file outside the tree that was not loaded, unless that
  source entry carries ``consumed_by`` saying where it is read.

Lean inputs and files opened by path are outside its reach.  They were
pinned from the one-off measurement and are not re-measured here.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

REPO = Path(__file__).resolve().parents[1]

# The template-family trees repinned on 2026-09-24.  boundary_seed is not
# here: its manifest and verifier bytes are frozen by
# research/boundary_custody_policy.json.
MEASURED = (
    "concurrency", "dynamics_step", "estate_honesty", "g001_target_charter",
    "g010_primitive_removal", "g011_finitary_substrate", "g012_typed_translation",
    "g013_trace_calculus", "g014_observer_descent", "g015_autonomous_stepping",
    "g018_self_hosting", "g1_local_class", "genesis_continuation", "grammar_fit",
    "internal_syntax_logic", "iso_sound_lean", "m104_equality_order",
    "m105_number_tower", "m108_internal_algebra", "m109_obstruction_homology",
    "m114_solver_adapter", "multi_depth", "multi_magnitude",
    "p200_operational_protocols", "p201_relational_spacetime",
    "p203_composite_systems", "p204_operational_valuations",
    "p209a_wigner_phase_space", "p209b_clifford_symplectic",
    "p209d_nonclassical_horizons", "priced_admissions", "reading_f_iso",
    "redheffer", "self_interpreter", "sign_tower", "target_a_execution",
    "target_b_dynamics", "thinghood", "x301_formal_semantics",
    "x302_operational_reasoning", "x303_bounded_agency",
    "x310_vertical_integration",
)

CUSTODY_VERIFIERS = ("verify_pins.py", "verify_sources.py", "verify_manifest.py",
                     "source_manifest.py")

CHILD = r'''
import sys
sys.path[:] = [p for p in sys.path if p]
import ast, importlib, importlib.util, json, os, types
from pathlib import Path
repo, tree = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
skip = set(sys.argv[3].split(","))
files = sorted(p for p in tree.rglob("*.py")
               if p.name not in skip and "__pycache__" not in p.parts and ".lake" not in p.parts)
names = set()
for f in files:
    try:
        parsed = ast.parse(f.read_bytes().decode("utf-8"))
    except SyntaxError:
        continue
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module)
            names.update(node.module + "." + a.name for a in node.names if a.name != "*")
os.chdir(tree)
sys.path[:] = [str(tree)] + [p for p in sys.path[1:]] + [str(repo / "code")]
for i, f in enumerate(files):
    if str(f.parent) not in sys.path:
        sys.path.insert(0, str(f.parent))
    try:
        spec = importlib.util.spec_from_file_location("_census_%d" % i, f)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    except BaseException:
        pass
for name in sorted(names):
    if name.split(".")[0] in sys.stdlib_module_names or name in sys.modules:
        continue
    try:
        importlib.import_module(name)
    except BaseException:
        pass
found = set()
for module in list(sys.modules.values()):
    origin = getattr(module, "__file__", None)
    if not isinstance(origin, str):
        continue
    path = Path(origin).resolve()
    try:
        rel = path.relative_to(repo).as_posix()
    except ValueError:
        continue
    if path.is_relative_to(tree) or "__pycache__" in rel:
        continue
    found.add(rel)
print(json.dumps(sorted(found)))
'''


def loaded_outside(repo: Path, tree: Path) -> set[str]:
    """Repository modules outside ``tree`` that importing the tree loads."""
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}
    done = subprocess.run(
        [sys.executable, "-B", "-c", CHILD, str(repo), str(tree), ",".join(CUSTODY_VERIFIERS)],
        cwd=tree, env=env, capture_output=True, text=True, encoding="utf-8", timeout=300,
    )
    lines = [line for line in done.stdout.splitlines() if line.startswith("[")]
    assert done.returncode == 0 and lines, done.stdout[-2000:] + done.stderr[-2000:]
    return set(json.loads(lines[-1]))


def problems(repo: Path, tree_rel: str) -> list[str]:
    """Each consumed module the manifest does not pin, and each unconsumed pin."""
    tree = repo / tree_rel
    manifest = json.loads((tree / "SOURCE_MANIFEST.json").read_bytes().decode("utf-8"))
    sources = manifest["sources"]
    prefix = tree_rel.rstrip("/") + "/"
    pinned = {s["path"] for s in sources
              if s["path"].endswith(".py") and not s["path"].startswith(prefix)}
    elsewhere = {s["path"] for s in sources if "consumed_by" in s}
    loaded = loaded_outside(repo, tree)
    found = [f"{tree_rel}: loads {path}, which its manifest does not pin"
             for path in sorted(loaded - pinned)]
    found += [f"{tree_rel}: pins {path}, which importing the tree never loads"
              for path in sorted(pinned - loaded - elsewhere)]
    return found


@pytest.mark.parametrize("tree", MEASURED)
def test_template_tree_pins_exactly_the_python_it_loads(tree: str) -> None:
    assert problems(REPO, f"research/{tree}") == []


def test_the_measured_population_is_the_repinned_template_family() -> None:
    for tree in MEASURED:
        manifest = json.loads(
            (REPO / "research" / tree / "SOURCE_MANIFEST.json").read_bytes().decode("utf-8"))
        assert str(manifest.get("note", "")).startswith("2026-09-24:"), tree
    assert len(MEASURED) == len(set(MEASURED)) == 42


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def _synthetic(tmp_path: Path, sources: list[dict[str, str]]) -> Path:
    _write(tmp_path / "research" / "beta" / "beta_mod.py", "VALUE = 1\n")
    _write(tmp_path / "research" / "beta" / "lazy_mod.py", "VALUE = 2\n")
    _write(tmp_path / "research" / "beta" / "unused.py", "VALUE = 3\n")
    _write(tmp_path / "research" / "alpha" / "alpha.py", (
        "import pathlib, sys\n"
        "sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'beta'))\n"
        "import beta_mod\n"
        "def later() -> int:\n"
        "    import lazy_mod\n"
        "    return lazy_mod.VALUE\n"))
    _write(tmp_path / "research" / "alpha" / "SOURCE_MANIFEST.json",
           json.dumps({"sources": sources}))
    return tmp_path


def test_an_unconsumed_pin_and_a_missing_consumed_module_are_both_named(tmp_path: Path) -> None:
    repo = _synthetic(tmp_path, [{"path": "research/beta/unused.py"},
                                 {"path": "research/beta/lazy_mod.py"}])
    assert problems(repo, "research/alpha") == [
        "research/alpha: loads research/beta/beta_mod.py, which its manifest does not pin",
        "research/alpha: pins research/beta/unused.py, which importing the tree never loads",
    ]


def test_a_function_local_import_counts_and_consumed_by_excuses_only_its_entry(
    tmp_path: Path,
) -> None:
    repo = _synthetic(tmp_path, [
        {"path": "research/beta/beta_mod.py"},
        {"path": "research/beta/unused.py", "consumed_by": "a test that adds its own path"},
    ])
    assert problems(repo, "research/alpha") == [
        "research/alpha: loads research/beta/lazy_mod.py, which its manifest does not pin",
    ]

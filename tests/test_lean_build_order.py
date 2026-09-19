"""The Lean build order in ``docs/lean_build_order.md`` is generated.

``ci/lean_build_order.py`` reads every tracked lakefile's requires and
writes the fresh-clone build order between two marker lines of the page.
The first test fails when a require line changes without the page being
regenerated.  The rest build small repositories in a temporary directory
and check each way the generator reads a lakefile, orders the graph, and
refuses what it cannot read.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lbo = _load("_lean_build_order", REPO / "ci" / "lean_build_order.py")

SEALED = 'name = "derivation"\n\n[[lean_lib]]\nname = "Derivation"\n'
EMPTY: Mapping[str, str] = {}


def _toml(name: str, requires: Mapping[str, str] = EMPTY, libs: tuple[str, ...] = ("Main",)) -> str:
    text = f'name = "{name}"\n'
    for req, path in requires.items():
        text += f'\n[[require]]\nname = "{req}"\npath = "{path}"\n'
    for lib in libs:
        text += f'\n[[lean_lib]]\nname = "{lib}"\n'
    return text


def _repo(tmp_path: Path, files: Mapping[str, str]) -> Path:
    for rel, text in files.items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    return tmp_path


# The real page.

def test_page_matches_the_lakefiles() -> None:
    found = lbo.problems(REPO)
    assert not found, (
        f"{lbo.PAGE_REL} is stale. Run `{lbo.REGENERATE}` and commit the result.\n"
        + "\n".join(found)
    )


def test_every_tracked_lakefile_is_placed_once_after_what_it_requires() -> None:
    graph = lbo.build_graph(REPO)
    order = lbo.sequence(graph)
    assert len(order) == len(set(order))
    lakefile_dirs = {
        p.rsplit("/", 1)[0] for p in lbo.tracked_files(REPO)
        if p.rsplit("/", 1)[-1] in lbo.LAKEFILES
    }
    assert set(order) | set(graph.skipped) == lakefile_dirs
    assert not set(order) & set(graph.skipped)
    position = {d: i for i, d in enumerate(order)}
    for directory in order:
        for _, target in graph.packages[directory].requires:
            assert position[target] < position[directory], (directory, target)
    assert order[0] == lbo.SEALED_DIR


# Reading lakefiles.

def test_both_lakefile_forms_are_read_and_comments_are_not(tmp_path: Path) -> None:
    lean_dsl = (
        "import Lake\nopen Lake DSL\n\npackage b\n\n"
        "-- require ghost from \"../../nowhere\"\n"
        "/- a block comment\n   require phantom from \"../../nowhere\"\n"
        "   /- nested -/ still inside -/\n"
        "require a from \"../../a/lean\"\n\n"
        "@[default_target]\nlean_lib B where\n  roots := #[`B, `B.Extra]\n"
    )
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "a/lean/lakefile.toml": _toml("a", {"derivation": "../../lean4"}),
        "b/lean/lakefile.lean": lean_dsl,
        "c/lakefile.toml": _toml("c"),
    })
    graph = lbo.build_graph(repo, {}, {})
    assert graph.packages["b/lean"].requires == (("a", "a/lean"),)
    assert graph.packages["b/lean"].roots == ("B", "B.Extra")
    assert graph.base == ("lean4",)
    assert graph.groups == ((("a/lean", "b/lean"), ()),)
    assert graph.standalone == ("c",)
    assert lbo.sequence(graph) == ["lean4", "a/lean", "b/lean", "c"]


def test_strip_lean_comments_keeps_strings_and_nesting() -> None:
    text = 'a "x -- y" b -- gone\n/- one /- two -/ still -/c'
    assert lbo.strip_lean_comments(text).split() == ['a', '"x', '--', 'y"', 'b', 'c']
    with pytest.raises(ValueError, match="unterminated block comment"):
        lbo.strip_lean_comments("/- open")


@pytest.mark.parametrize(("rel", "text"), [
    ("x/lakefile.toml", 'name = "x"\n[[require]]\nname = "derivation"\ngit = "https://example.invalid/r"\n'),
    ("x/lakefile.lean", 'import Lake\nopen Lake DSL\npackage x\nrequire derivation from git "u"\n'),
])
def test_an_unread_require_form_is_an_error(tmp_path: Path, rel: str, text: str) -> None:
    repo = _repo(tmp_path, {"lean4/lakefile.toml": SEALED, rel: text})
    with pytest.raises(ValueError, match="unsupported require form"):
        lbo.build_graph(repo, {}, {})


def test_a_require_of_an_untracked_directory_is_an_error(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"x/lakefile.toml": _toml("x", {"derivation": "../lean4"})})
    with pytest.raises(ValueError, match=r"x/lakefile.toml: require 'derivation' points at "
                                         r"lean4, which holds no tracked lakefile"):
        lbo.build_graph(repo, {}, {})


def test_a_require_name_must_match_the_package(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "x/lakefile.toml": _toml("x", {"sealed": "../lean4"}),
    })
    with pytest.raises(ValueError, match="whose package is named 'derivation'"):
        lbo.build_graph(repo, {}, {})


def test_a_require_cycle_is_an_error(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "p/lakefile.toml": _toml("p", {"q": "../q"}),
        "q/lakefile.toml": _toml("q", {"p": "../p"}),
    })
    with pytest.raises(ValueError, match="require cycle: p -> q -> p"):
        lbo.build_graph(repo, {}, {})


# Ordering.

def test_the_longest_chain_comes_first_then_the_rest_by_depth(tmp_path: Path) -> None:
    sealed = {"derivation": "../lean4"}
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "x/lakefile.toml": _toml("x", sealed),
        "y/lakefile.toml": _toml("y", {**sealed, "x": "../x"}),
        "z/lakefile.toml": _toml("z", {**sealed, "y": "../y"}),
        "w/lakefile.toml": _toml("w", {**sealed, "x": "../x"}),
        "g/lakefile.toml": _toml("g", sealed),
        "h/lakefile.toml": _toml("h", {**sealed, "g": "../g"}),
        "leaf/lakefile.toml": _toml("leaf", sealed),
        "alone/lakefile.toml": _toml("alone"),
    })
    graph = lbo.build_graph(repo, {}, {})
    assert graph.groups == ((("x", "y", "z"), ("w",)), (("g", "h"), ()))
    assert graph.leaves == ("leaf",)
    assert graph.standalone == ("alone",)
    assert lbo.sequence(graph) == ["lean4", "x", "y", "z", "w", "g", "h", "leaf", "alone"]
    assert graph.stage["z"] == 3 and graph.stage["w"] == 2
    block = lbo.render_block(graph)
    assert "# Require group 1: its longest chain, one at a time: x -> y -> z." in block
    assert "Invoke-InDir 'lean4' 'lake' @('build')" in block
    assert "Push-Location -LiteralPath $Dir -ErrorAction Stop" in block
    helper = block.split("function Invoke-InDir", 1)[1].split("}", 1)[0]
    assert helper.index("Push-Location") < helper.index("try")
    assert "ErrorAction Stop" in helper.split("try")[0]


def test_a_diamond_in_a_require_group_is_topological(tmp_path: Path) -> None:
    """A chain package that also requires a rest package cannot precede it."""
    sealed = {"derivation": "../lean4"}
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "a/lakefile.toml": _toml("a", sealed),
        "b/lakefile.toml": _toml("b", {**sealed, "a": "../a"}),
        "c/lakefile.toml": _toml("c", {**sealed, "a": "../a"}),
        "d/lakefile.toml": _toml("d", {**sealed, "b": "../b", "c": "../c"}),
    })
    graph = lbo.build_graph(repo, {}, {})
    assert graph.groups == ((("a", "b", "d"), ("c",)),)
    order = lbo.sequence(graph)
    assert order == ["lean4", "a", "b", "c", "d"]
    position = {d: i for i, d in enumerate(order)}
    for directory in order:
        for _, target in graph.packages[directory].requires:
            assert position[target] < position[directory], (directory, target)


def test_a_root_module_supplied_twice_in_a_closure_is_listed(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "x/lakefile.toml": _toml("x", {"derivation": "../lean4"}, ("X", "Inventory")),
        "y/lakefile.toml": _toml("y", {"x": "../x"}, ("Y", "Inventory")),
        "z/lakefile.toml": _toml("z", {"derivation": "../lean4"}, ("Z", "Inventory")),
    })
    graph = lbo.build_graph(repo, {}, {})
    assert lbo.shared_roots(graph) == [("y", "Inventory", ("x", "y"))]


def test_toolchain_pins_and_directories_without_a_lakefile(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "lean4/lean-toolchain": "pin-a\n",
        "bare/lean-toolchain": "pin-a\n",
        "bare/One.lean": "",
        "bare/sub/Two.lean": "",
        "x/lakefile.toml": _toml("x"),
    })
    graph = lbo.build_graph(repo, {}, {})
    assert graph.bare_dirs == {"bare": ("One.lean",)}
    assert graph.toolchains == {"bare": "pin-a", "lean4": "pin-a", "x": None}
    block = lbo.render_block(graph)
    assert "Invoke-InDir 'bare' 'lean' @('One.lean')" in block
    assert "- no `lean-toolchain` in the directory: 1 build directory." in block
    assert "  - `x`" in block


# The recorded tables.

def test_a_package_declared_twice_needs_a_recorded_build_entry(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "t/lakefile.toml": _toml("t", {"derivation": "../lean4"}),
        "t/lean/lakefile.toml": _toml("t", {"derivation": "../../lean4"}),
    })
    with pytest.raises(ValueError, match="Lake package 't' is declared by t, t/lean"):
        lbo.build_graph(repo, {}, {})
    graph = lbo.build_graph(repo, {}, {"t": "t/lean"})
    assert "t" not in lbo.sequence(graph)
    assert "- `t`: build `t/lean` instead." in lbo.render_block(graph)
    with pytest.raises(ValueError, match="does not pair two declarations"):
        lbo.build_graph(repo, {}, {"t": "lean4"})


def test_an_untracked_source_directory_needs_a_script_that_stages_it(tmp_path: Path) -> None:
    staged = (
        "import Lake\nopen Lake DSL\npackage s\n\n"
        "lean_lib Derivation where\n  srcDir := \"sealed\"\n  roots := #[`Derivation.A]\n\n"
        "@[default_target]\nlean_lib S where\n  roots := #[`S]\n"
    )
    repo = _repo(tmp_path, {"s/lean/lakefile.lean": staged, "s/verify_lean.py": ""})
    with pytest.raises(ValueError, match=r"s/lean/lakefile.lean compiles sealed/, which holds "
                                         r"no tracked file"):
        lbo.build_graph(repo, {}, {})
    record = lbo.Special("s", ("python", "verify_lean.py"), "stages it", True, "sealed")
    graph = lbo.build_graph(repo, {"s/lean": record}, {})
    block = lbo.render_block(graph)
    assert "Invoke-InDir 's' 'python' @('verify_lean.py')" in block
    assert "Invoke-InDir 's/lean' 'lake' @('build')" not in block
    assert "instead of `lake build`: stages it" in block


@pytest.mark.parametrize(("record", "message"), [
    (("s", ("python", "missing.py"), "why", True, "sealed"), "does not run a tracked script"),
    (("s", ("python", "verify_lean.py"), "why", True, "other"), "not an untracked source"),
    (("s", ("python", "verify_lean.py"), "why", False, None, ("S",)), "is a root of the lakefile"),
    (("s", ("python", "verify_lean.py"), "why", False, None, ("S.Nope",)), "not a tracked module"),
])
def test_recorded_script_steps_are_checked(
    tmp_path: Path, record: tuple[object, ...], message: str
) -> None:
    lakefile = (
        "import Lake\nopen Lake DSL\npackage s\n\n"
        "lean_lib Derivation where\n  srcDir := \"sealed\"\n\n"
        "lean_lib S where\n  roots := #[`S]\n"
    )
    repo = _repo(tmp_path, {
        "s/lean/lakefile.lean": lakefile, "s/lean/S.lean": "", "s/verify_lean.py": "",
    })
    with pytest.raises(ValueError, match=message):
        lbo.build_graph(repo, {"s/lean": lbo.Special(*record)}, {})


def test_a_recorded_entry_for_a_missing_package_is_an_error(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"x/lakefile.toml": _toml("x"), "x/v.py": ""})
    record = lbo.Special("x", ("python", "v.py"), "why", True)
    with pytest.raises(ValueError, match="SPECIAL entry y is not a build entry"):
        lbo.build_graph(repo, {"y": record}, {})
    with pytest.raises(ValueError, match="names a directory with no tracked lakefile"):
        lbo.build_graph(repo, {}, {"x": "y"})


# The page.

def test_a_stale_page_names_the_difference_and_write_repairs_it(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "lean4/lakefile.toml": SEALED,
        "x/lakefile.toml": _toml("x", {"derivation": "../lean4"}),
        lbo.PAGE_REL: f"# page\n\n{lbo.BEGIN}\nold\n{lbo.END}\n\ntail\n",
    })
    found = lbo.problems(repo, {}, {})
    assert found[0] == f"{lbo.PAGE_REL} is stale; regenerate it with: {lbo.REGENERATE}"
    assert "-old" in found
    assert "+Invoke-InDir 'x' 'lake' @('build')" in found
    current = (repo / lbo.PAGE_REL).read_text(encoding="utf-8")
    repaired = lbo.expected_page(repo, current, {}, {})
    assert repaired.startswith("# page\n\n" + lbo.BEGIN) and repaired.endswith(lbo.END + "\n\ntail\n")
    (repo / lbo.PAGE_REL).write_bytes(repaired.encode("utf-8"))
    assert lbo.problems(repo, {}, {}) == []


def test_the_page_needs_exactly_one_marker_pair(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {
        "x/lakefile.toml": _toml("x"),
        lbo.PAGE_REL: f"{lbo.BEGIN}\n{lbo.END}\n{lbo.BEGIN}\n",
    })
    assert "exactly one" in lbo.problems(repo, {}, {})[0]
    (repo / lbo.PAGE_REL).unlink()
    assert lbo.problems(repo, {}, {}) == [f"{lbo.PAGE_REL} is missing"]


def test_main_check_reports_the_real_page_current(capsys: pytest.CaptureFixture[str]) -> None:
    assert lbo.main(["--check"]) == 0
    assert capsys.readouterr().out.strip() == f"{lbo.PAGE_REL} is current"

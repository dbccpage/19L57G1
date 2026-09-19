"""Loose cohort/e2e/fuzz scripts live under ``research/e2e_tests/``.

A live path that still named ``research/adversarial_challenge_cohort4.py``
after the move would send a reader to a file that is gone.  These tests
pin the new location, refuse the old top-level names, and drive the moved
script's ``TARGET_DIRS`` so the g013 ``sys.path`` claim is read from the
shipped module.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

MOVED = (
    "adversarial_challenge_cohort2.py",
    "adversarial_challenge_cohort3.py",
    "adversarial_challenge_cohort4.py",
    "adversarial_challenge_cohort5.py",
    "adversarial_challenge_cohort6.py",
    "adversarial_challenge_cohort7.py",
    "adversarial_challenge_cohort8.py",
    "cohort6_adv_integration.py",
    "cohort6_adv_m108.py",
    "cohort6_adv_m109.py",
    "cohort6_adv_p203.py",
    "cohort6_adv_seal.py",
    "cohort6_adv_x300.py",
    "e2e_cohorts_1_to_4_integration.py",
    "fuzz_g011_g001.py",
)


def test_moved_scripts_are_under_e2e_tests_and_not_at_research_root() -> None:
    for name in MOVED:
        assert (REPO / "research" / "e2e_tests" / name).is_file(), name
        assert not (REPO / "research" / name).exists(), name


def test_scaffold_readme_names_the_moved_cohort4_path() -> None:
    text = (REPO / "research" / "_scaffold" / "README.md").read_text(encoding="utf-8")
    new = "research/e2e_tests/adversarial_challenge_cohort4.py"
    old = "research/adversarial_challenge_cohort4.py"
    assert new in text
    assert old not in text.replace(new, "")


def _binop_path_parts(node: ast.AST) -> tuple[str, ...]:
    parts: list[str] = []
    while isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, str):
            return ()
        parts.append(node.right.value)
        node = node.left
    return tuple(reversed(parts))


def test_cohort4_puts_g013_on_sys_path_ahead_of_stdlib() -> None:
    path = REPO / "research" / "e2e_tests" / "adversarial_challenge_cohort4.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: dict[str, ast.AST] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names[target.id] = node.value
    dirs = names["TARGET_DIRS"]
    assert isinstance(dirs, ast.List)
    listed = [_binop_path_parts(elt) for elt in dirs.elts]
    assert ("research", "g013_trace_calculus") in listed
    inserts = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "insert"
        and len(node.args) == 2
        and isinstance(node.args[0], ast.Constant)
        and node.args[0].value == 0
    ]
    assert inserts, "TARGET_DIRS are not prepended onto sys.path"

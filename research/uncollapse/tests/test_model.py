"""The pinned module list matches the Lean imports, and every module exists in the sealed package."""
from pathlib import Path

from model import HERE, consumed_modules, lean_imports


def test_imports_are_the_pinned_modules() -> None:
    assert lean_imports() == consumed_modules()


def test_consumed_modules_exist_read_only() -> None:
    lean4 = HERE.parents[1] / "lean4"
    for module in consumed_modules():
        assert (lean4 / Path(*module.split("."))).with_suffix(".lean").is_file(), module

"""The pinned module lists match the Lean imports, and every pinned module file exists."""
from pathlib import Path

from model import HERE, consumed_modules, consumed_research_modules, lean_imports


def test_imports_are_the_pinned_modules() -> None:
    assert lean_imports() == sorted(consumed_modules() + list(consumed_research_modules()))


def test_consumed_modules_exist() -> None:
    root = HERE.parents[1]
    for module in consumed_modules():
        assert (root / "lean4" / Path(*module.split("."))).with_suffix(".lean").is_file(), module
    for module, file in consumed_research_modules().items():
        assert (root / file).is_file(), module

"""Read the tree's pinned input: the sealed modules it consumes. AuthorityEffect: None."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def consumed_modules() -> list[str]:
    data = json.loads((HERE / "input.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("source_revision"), str):
        raise ValueError("input.json must name a source_revision")
    modules = data.get("consumed_modules")
    if (not isinstance(modules, list) or not modules
            or any(not isinstance(m, str) or not m.startswith("Derivation.") for m in modules)
            or modules != sorted(set(modules))):
        raise ValueError("input.json: consumed_modules must be a sorted unique list of Derivation modules")
    return modules


def lean_imports() -> list[str]:
    text = (HERE / "lean" / "ResearchUncollapse.lean").read_text(encoding="utf-8")
    return sorted(line.split()[1] for line in text.splitlines() if line.startswith("import "))

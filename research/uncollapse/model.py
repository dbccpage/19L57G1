"""Read the tree's pinned input: the modules it consumes. AuthorityEffect: None."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _input() -> dict[str, object]:
    data = json.loads((HERE / "input.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("source_revision"), str):
        raise ValueError("input.json must name a source_revision")
    return data


def consumed_modules() -> list[str]:
    modules = _input().get("consumed_modules")
    if (not isinstance(modules, list) or not modules
            or any(not isinstance(m, str) or not m.startswith("Derivation.") for m in modules)
            or modules != sorted(set(modules))):
        raise ValueError("input.json: consumed_modules must be a sorted unique list of Derivation modules")
    return modules


def consumed_research_modules() -> dict[str, str]:
    modules = _input().get("consumed_research_modules")
    if (not isinstance(modules, dict)
            or any(not isinstance(k, str) or not isinstance(v, str) or not v.startswith("research/")
                   or v.startswith(f"research/{HERE.name}/") for k, v in modules.items())):
        raise ValueError("input.json: consumed_research_modules must map modules to files of other research trees")
    return modules


def lean_imports() -> list[str]:
    """Every outside import of every module of this tree's Lean package."""
    lean = HERE / "lean"
    own = {p.relative_to(lean).with_suffix("").as_posix().replace("/", ".")
           for p in lean.rglob("*.lean") if ".lake" not in p.parts}
    found: set[str] = set()
    for path in lean.rglob("*.lean"):
        if ".lake" in path.parts or path.name == "lakefile.lean":
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("import "):
                found.add(line.split()[1])
    return sorted(found - own)

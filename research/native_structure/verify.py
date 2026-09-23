"""Local pins, tests, typing and an explicitly named Lean report scope.

Copy this entry point verbatim. Configure the tree in TREE_CONTRACT.json.
The axiom audit covers exactly its listed declarations, not every constant.
AuthorityEffect: None.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
ALLOWED = {"propext", "Quot.sound"}
# Non-greedy captures retain the final quote of a primed declaration name.
NO_AXIOMS = re.compile(r"'(.+?)' does not depend on any axioms")
WITH_AXIOMS = re.compile(r"'(.+?)' depends on axioms: \[([^\]]*)\]")


def configuration() -> dict[str, Any]:
    value = json.loads((HERE / "TREE_CONTRACT.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise ValueError("TREE_CONTRACT.json: expected schema 1")
    return value


def local_file(name: str) -> Path:
    relative = Path(name)
    path = HERE / relative
    if (relative.is_absolute() or ".." in relative.parts or path.is_symlink()
            or not path.is_file() or not path.resolve().is_relative_to(HERE)):
        raise ValueError(f"TREE_CONTRACT.json: expected an existing local file: {name}")
    return path


def pins(config: dict[str, Any], write: bool) -> None:
    names = config.get("pin_files")
    if (not isinstance(names, list) or not names
            or any(not isinstance(name, str) for name in names)
            or len(set(names)) != len(names)):
        raise ValueError("TREE_CONTRACT.json: pin_files must be a nonempty unique list")
    # Manifest keys use the repository path convention of the pin index.
    expected = {f"research/{HERE.name}/{Path(name).as_posix()}": hashlib.sha256(local_file(name).read_bytes()).hexdigest()
                for name in sorted(names)}
    manifest = HERE / "SOURCE_MANIFEST.json"
    if write:
        manifest.write_text(json.dumps({"schema": 1, "sources": expected}, indent=2)+"\n",
                            encoding="utf-8", newline="\n")
    else:
        actual = json.loads(manifest.read_text(encoding="utf-8"))
        if actual != {"schema": 1, "sources": expected}:
            source = actual.get("sources", {}) if isinstance(actual, dict) else {}
            changed = [name for name in sorted(set(expected) | set(source))
                       if source.get(name) != expected.get(name)] if isinstance(source, dict) else sorted(expected)
            raise ValueError(f"SOURCE_MANIFEST.json: stale pin population or digest: {changed}")
    print(f"pins: {len(expected)} local input files", flush=True)


def run(label: str, command: list[str], cwd: Path = HERE) -> str:
    print(f"step: {label}", flush=True)
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=False)
    output = result.stdout + result.stderr
    print(output, end="", flush=True)
    if result.returncode:
        raise ValueError(f"{label}: command exited {result.returncode}")
    return output


def sources(suffix: str, directory: Path) -> list[Path]:
    return sorted(path for path in directory.rglob("*"+suffix)
                  if not any(part.startswith(".") or part == "__pycache__"
                             for part in path.relative_to(directory).parts))


def lean(config: dict[str, Any]) -> None:
    root = config.get("lean_root")
    names = config.get("axiom_declarations")
    if (not isinstance(root, str) or not re.fullmatch(r"Research[A-Z][A-Za-z0-9]*", root)
            or config.get("axiom_scope") != "explicit_reports"
            or not isinstance(names, list) or not names
            or any(not isinstance(name, str) or not name.startswith(root+".") for name in names)
            or len(set(names)) != len(names)):
        raise ValueError("TREE_CONTRACT.json: require a unique root and nonempty explicit report scope")
    directory = HERE / "lean"
    report = directory / root / "AxiomReport.lean"
    files = sources(".lean", directory)
    modules = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        forbidden = ("so"+"rry", "ad"+"mit", "uns"+"afe", "par"+"tial", "native_"+"decide")
        if any(re.search(r"\b"+word+r"\b", text) for word in forbidden) or re.search(r"(?m)^\s*ax"+r"iom\s", text):
            raise ValueError(f"{path.relative_to(HERE)}: forbidden proof shortcut")
        if path != report:
            modules.append(path.relative_to(directory).with_suffix("").as_posix().replace("/", "."))
    if not modules or not report.is_file():
        raise ValueError("lean: missing source modules or scoped AxiomReport.lean")
    # The report is compiled by file path, never imported as a census module.
    run("Lean sources", ["lake", "build", *modules], directory)
    log = run("Lean named reports", ["lake", "env", "lean", f"{root}/AxiomReport.lean"], directory)
    plain = NO_AXIOMS.findall(log)
    dependent = WITH_AXIOMS.findall(log)
    actual = plain + [name for name, _ in dependent]
    if Counter(actual) != Counter(names):
        raise ValueError(f"AxiomReport.lean: expected {names}, reported {actual}")
    for name, axes in dependent:
        extra = {axis.strip() for axis in axes.split(",") if axis.strip()} - ALLOWED
        if extra:
            raise ValueError(f"AxiomReport.lean: {name} uses disallowed axioms {sorted(extra)}")
    print(f"Lean reach: exactly {len(names)} named declarations: {names}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-pins", action="store_true")
    args = parser.parse_args()
    try:
        config = configuration()
        pins(config, args.write_pins)
        if args.write_pins:
            return 0
        run("tests", [sys.executable, "-m", "pytest", "tests", "-q", "-o", "addopts=", "-p", "no:cacheprovider"])
        python = [str(path.relative_to(HERE)) for path in sources(".py", HERE)]
        run("typing", [sys.executable, "-m", "mypy", "--strict", "--python-version", "3.14", *python])
        lean(config)
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("local verification complete; AuthorityEffect: None")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

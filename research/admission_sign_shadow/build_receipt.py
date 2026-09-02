from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


COMMANDS: tuple[tuple[str, ...], ...] = (
    ("source_manifest.py", "--check"),
    ("-m", "unittest", "discover", "-s", ".", "-p", "test_*.py"),
    ("run_connector.py", "--check"),
    ("verify_lean.py", "--check"),
    ("-m", "mypy", "--config-file", "pyproject.toml"),
)


def tree_root() -> Path:
    return Path(__file__).resolve().parent


def environment() -> dict[str, str]:
    env = os.environ.copy()
    elan = str(Path.home() / ".elan" / "bin")
    env["PATH"] = elan + os.pathsep + env.get("PATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_python(args: tuple[str, ...]) -> dict[str, object]:
    command = [sys.executable, *args]
    completed = subprocess.run(
        command,
        cwd=tree_root(),
        env=environment(),
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if completed.returncode != 0:
        raise ValueError(
            f"command failed with {completed.returncode}: python {' '.join(args)}\n{output}"
        )
    return {
        "command": "python " + " ".join(args),
        "exit_code": completed.returncode,
        "last_line": lines[-1] if lines else "",
    }


def tool_output(*command: str) -> str:
    completed = subprocess.run(
        list(command),
        cwd=tree_root(),
        env=environment(),
        check=True,
        capture_output=True,
        text=True,
    )
    return (completed.stdout + completed.stderr).strip().splitlines()[0]


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def render() -> bytes:
    root = tree_root()
    command_results = [run_python(args) for args in COMMANDS]
    lean_payload = json.loads((root / "receipts" / "lean.json").read_text(encoding="utf-8"))
    payload = {
        "authority_effect": None,
        "axiom_inventory": lean_payload["axiom_inventory"],
        "commands": command_results,
        "input_hashes": {
            "SOURCE_MANIFEST.json": file_hash(root / "SOURCE_MANIFEST.json"),
            "connector.json": file_hash(root / "receipts" / "connector.json"),
            "lean.json": file_hash(root / "receipts" / "lean.json"),
        },
        "terminal": "IMPORT_ISOLATED_BUT_NOT_REMOVED",
        "tool_versions": {
            "lake": tool_output("lake", "--version"),
            "lean": tool_output("lean", "--version"),
            "mypy": tool_output(sys.executable, "-m", "mypy", "--version"),
            "python": platform.python_version(),
        },
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = tree_root() / "receipts" / "machine_receipt.json"
    rendered = render()
    if args.write:
        path.write_bytes(rendered)
    if not path.exists() or path.read_bytes() != rendered:
        raise ValueError("machine receipt differs from complete local replay")
    print("machine receipt replay clean: IMPORT_ISOLATED_BUT_NOT_REMOVED")


if __name__ == "__main__":
    main()

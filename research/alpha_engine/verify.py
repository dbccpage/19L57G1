"""Every local check of this tree, in order; exit non-zero on the first failure.

AuthorityEffect: None.  A local pass is a local receipt, not hosted CI.
This tree is not gate 11.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

STEPS: tuple[tuple[str, list[str]], ...] = (
    ("sources", [sys.executable, "verify_sources.py", "--check"]),
    ("tests", [sys.executable, "-m", "coverage", "run", "--branch", "--source=.",
               "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]),
    ("coverage_json", [sys.executable, "-m", "coverage", "json", "-o", "coverage.json", "-q"]),
    ("coverage", [sys.executable, "check_coverage.py"]),
    ("mypy", [sys.executable, "-m", "mypy"]),
    ("lean", [sys.executable, "verify_lean.py", "--check"]),
    ("computation", [sys.executable, "run.py", "--check"]),
)


def main() -> int:
    for name, command in STEPS:
        print(f"== {name}: {' '.join(command[1:])}", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            print(f"FAIL: {name} exited {result.returncode}", flush=True)
            return result.returncode
    print("PASS: sources, tests, coverage, mypy, lean, computation", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

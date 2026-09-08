"""Every check of this family, in order; exit non-zero on the first failure.

AuthorityEffect: None.  A local pass is a local receipt, not hosted CI.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

STEPS: tuple[tuple[str, list[str]], ...] = (
    ("sources", [sys.executable, "verify_sources.py", "--check"]),
    ("tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]),
    ("mypy", [sys.executable, "-m", "mypy"]),
    ("lean", [sys.executable, "verify_lean.py", "--check"]),
    ("computation", [sys.executable, "run.py", "--check"]),
)


def main() -> int:
    for name, command in STEPS:
        print(f"== {name}: {' '.join(command[1:])}")
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            print(f"FAIL: {name} exited {result.returncode}")
            return result.returncode
    print("PASS: sources, tests, mypy, lean, computation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

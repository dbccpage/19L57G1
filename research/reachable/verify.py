"""Run every check of this tree in order and exit non-zero on any failure.

AuthorityEffect: None.

Order: the custody check of the consumed sealed inputs; the unit tests,
including the negative tests that mutate one node or one edge; strict typing;
the Lean build with its report census; the census of every exported node and
edge compared byte for byte with the committed record.  Every step is a
subprocess of the same interpreter, run from this directory, and every exit
is read directly.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

STEPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("sources", (sys.executable, "verify_sources.py", "--check")),
    ("tests", (sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py")),
    ("mypy", (sys.executable, "-m", "mypy")),
    ("lean", (sys.executable, "verify_lean.py", "--check")),
    ("census", (sys.executable, "census.py", "--check")),
)


def run(name: str, argv: tuple[str, ...]) -> bool:
    result = subprocess.run(list(argv), cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", check=False)
    output = (result.stdout + result.stderr).strip()
    tail = output.splitlines()[-1] if output else ""
    status = "PASS" if result.returncode == 0 else "FAIL"
    print(f"{status}: {name} (exit {result.returncode}) {tail}")
    if result.returncode != 0:
        print(output)
    return result.returncode == 0


def main() -> int:
    ok = True
    for name, argv in STEPS:
        ok = run(name, argv) and ok
    print("PASS: every step" if ok else "FAIL: at least one step failed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

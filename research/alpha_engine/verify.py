"""Every local check of this tree, in order; exit non-zero on the first failure.

AuthorityEffect: None.  A local pass is a local receipt, not hosted CI.
This tree is not gate 11.

2026-09-25 (closeout, work package D): this is the one documented command
that verifies the Alpha reference slice (``docs/ALPHA_HANDOFF.md``).  Every
step is required.  The independent verifiers stay separate programs; this
file only runs them in order.  Two steps were added: ``handoff`` (the four
handoff demonstrations, each independently checked) and ``kernel_tests``
(the sealed kernel's own tests of the six consumed modules, which gate 3
already runs with the full sealed suite; included here because they take
seconds).  Reporting was tightened: the steps after a failing step are
listed as NOT RUN, and a skipped test is a skipped check, reported by name,
which fails the command because no check of the slice is optional.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]

KERNEL_TESTS: tuple[str, ...] = (
    "tests/test_model.py",
    "tests/test_observe.py",
    "tests/test_candidates.py",
    "tests/test_iso.py",
    "tests/test_engine.py",
)


@dataclass(frozen=True)
class Step:
    name: str
    command: tuple[str, ...]
    cwd: Path = ROOT


STEPS: tuple[Step, ...] = (
    Step("sources", (sys.executable, "verify_sources.py", "--check")),
    Step("tests", (sys.executable, "-m", "coverage", "run", "--branch", "--source=.",
                   "-m", "unittest", "discover", "-v", "-s", "tests", "-p", "test_*.py")),
    Step("coverage_json", (sys.executable, "-m", "coverage", "json", "-o", "coverage.json", "-q")),
    Step("coverage", (sys.executable, "check_coverage.py")),
    Step("mypy", (sys.executable, "-m", "mypy")),
    Step("lean", (sys.executable, "verify_lean.py", "--check")),
    Step("computation", (sys.executable, "run.py", "--check")),
    Step("handoff", (sys.executable, "handoff_demo.py", "--check")),
    Step("kernel_tests", (sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-rs",
                          *KERNEL_TESTS), REPO),
)

UNITTEST_ID = re.compile(r"^(test\S*) \((\S+)\)")
PYTEST_SKIP = re.compile(r"^SKIPPED (.+)$")
SKIP_COUNT = re.compile(r"\(skipped=(\d+)\)|(\d+) skipped")
UNITTEST_OK = re.compile(r" \.\.\. ok$")
UNITTEST_HEADER = re.compile(r"^test\S* \(\S+\)$")


def skipped_checks(output: str) -> list[str]:
    """Names of skipped tests in unittest ``-v`` or pytest ``-rs`` output.

    A skip that the summary counts but no line names is still reported.
    """
    found: list[str] = []
    current: str | None = None
    for line in output.splitlines():
        unit = UNITTEST_ID.match(line)
        if unit:
            current = unit.group(2)
        if " ... skipped" in line:
            found.append(current if current is not None else line.strip())
            continue
        pyt = PYTEST_SKIP.match(line)
        if pyt:
            found.append(pyt.group(1))
    counted = 0
    for match in SKIP_COUNT.finditer(output):
        counted += int(match.group(1) or match.group(2))
    if counted > len(found):
        found.extend(["unnamed skipped test"] * (counted - len(found)))
    return found


def shown(output: str) -> str:
    """The step's output without unittest's per-test ``ok`` lines.

    A bare test-id line (unittest prints one before a docstring line) is
    hidden too; a failing test is reported again in unittest's own summary.
    """
    return "\n".join(
        line for line in output.splitlines()
        if not UNITTEST_OK.search(line) and not UNITTEST_HEADER.match(line)
    )


def main() -> int:
    status: list[tuple[str, str]] = []
    skipped: list[str] = []
    failed = False
    for step in STEPS:
        if failed:
            status.append((step.name, "NOT RUN"))
            continue
        print(f"== {step.name}: {' '.join(step.command[1:])}", flush=True)
        result = subprocess.run(step.command, cwd=step.cwd, capture_output=True, check=False)
        output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
        text = shown(output)
        if text.strip():
            print(text, flush=True)
        step_skips = skipped_checks(output)
        for name in step_skips:
            print(f"SKIPPED CHECK: {step.name}: {name}", flush=True)
        skipped.extend(f"{step.name}: {name}" for name in step_skips)
        if result.returncode or step_skips:
            reason = f"exited {result.returncode}" if result.returncode else "skipped a check"
            print(f"FAIL: {step.name} {reason}", flush=True)
            status.append((step.name, "FAIL"))
            failed = True
        else:
            status.append((step.name, "PASS"))
    print("== summary", flush=True)
    for name, state in status:
        print(f"{state:8} {name}", flush=True)
    print(f"skipped checks: {len(skipped)}", flush=True)
    if failed:
        return 1
    print("PASS: " + ", ".join(name for name, _ in status), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

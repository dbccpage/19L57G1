"""Run the gate families written in `.github/workflows/verify.yml`, locally.

AuthorityEffect: None.  The workflow file is the contract, and this runner
reads its steps from it rather than keeping a list of its own, so the two
cannot drift apart.  A pass is a local receipt for the working tree the
runner ran on, nothing more.

    python ci/run_gates.py --list            # the steps, as parsed
    python ci/run_gates.py --fast            # the single-command checks, in seconds
    python ci/run_gates.py --job python      # one job; repeatable
    python ci/run_gates.py --workers 8       # all jobs, root tests in parallel
    python ci/run_gates.py --step 'side-free' --job research

Each `run:` body is written to a file and executed by bash with `-e`, the
way the hosted runner executes it.  On Windows that is Git for Windows'
bash (set GATES_BASH to override).  `python`, `python3` and `coverage` are
bound to the interpreter running this script, `${{ github.workspace }}` to
the repository root, `RUNNER_TEMP` to a fresh temporary directory, and
PYTHONUTF8=1 is set so output encodes as it does on the hosted runner.
Steps that install packages or toolchains are skipped and named in
SETUP_STEPS; a step that uses a workflow feature this parser does not
implement is an error, never silently approximated.

Because nothing is installed, every step runs under the interpreter that
runs this script, and installed versions that differ from requirements.txt
are printed with the results.  For the pinned versions exactly, run the
runner itself inside the recipe's environment:

    uv run --isolated --python 3.14 --with-requirements requirements.txt \\
      --with pytest-xdist==3.8.0 --with pytest-cov==7.1.0 \\
      python ci/run_gates.py --workers 8

Within a job, a failure stops that job's remaining steps, as on the hosted
runner; other jobs still run.  `--keep-going` runs every selected step.
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / ".github" / "workflows" / "verify.yml"

# Steps that prepare a hosted runner.  Named, so that a renamed or added
# setup step is reported instead of being run or skipped by accident.
SETUP_STEPS = frozenset(
    {"Install pinned dependencies", "Install elan", "Install pinned Lean toolchain"}
)
# The root suite under coverage; `--workers N` replaces its body with the
# parallel recipe documented in CLAUDE.md.
COVERAGE_STEP = "Tests under coverage"
# A single-command check that reads a file an earlier step writes, and so is
# not self-contained enough for `--fast`.
READS_EARLIER_OUTPUT = frozenset({"ci/check_coverage.py"})
FAST_COMMAND = re.compile(r"python3? (ci/[A-Za-z0-9_./-]+\.py)|python3? -m mypy")

JOB_KEYS = frozenset({"runs-on", "steps"})
STEP_KEYS = frozenset({"name", "uses", "with", "run", "working-directory", "env", "timeout-minutes"})
WORKSPACE_EXPR = "${{ github.workspace }}"


class WorkflowError(Exception):
    """The workflow uses something this parser does not implement."""


@dataclasses.dataclass(frozen=True)
class Step:
    job: str
    name: str
    run: str | None
    working_directory: str | None = None
    env: tuple[tuple[str, str], ...] = ()
    timeout_minutes: int | None = None

    @property
    def is_setup(self) -> bool:
        return self.name in SETUP_STEPS

    @property
    def is_fast(self) -> bool:
        if self.job != "python" or self.run is None or self.working_directory is not None:
            return False
        command = self.run.strip()
        match = FAST_COMMAND.fullmatch(command)
        return match is not None and match.group(1) not in READS_EARLIER_OUTPUT


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _blank_or_comment(line: str) -> bool:
    stripped = line.strip()
    return stripped == "" or stripped.startswith("#")


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _block(lines: list[str], start: int, parent: int) -> tuple[str, int]:
    """A `|` block scalar: every line indented deeper than its key."""
    body: list[str] = []
    indent: int | None = None
    i = start
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            body.append("")
            i += 1
            continue
        if _indent(line) <= parent:
            break
        if indent is None:
            indent = _indent(line)
        if _indent(line) < indent:
            raise WorkflowError(f"line {i + 1}: block scalar dedents inside its block")
        body.append(line[indent:])
        i += 1
    while body and body[-1] == "":
        body.pop()
    if not body:
        raise WorkflowError(f"line {start}: empty block scalar")
    return "\n".join(body) + "\n", i


def _mapping(lines: list[str], start: int, parent: int) -> tuple[dict[str, str], int]:
    """A flat mapping of scalars, indented deeper than its key."""
    mapping: dict[str, str] = {}
    i = start
    while i < len(lines):
        line = lines[i]
        if _blank_or_comment(line):
            i += 1
            continue
        if _indent(line) <= parent:
            break
        key, sep, value = line.strip().partition(":")
        if not sep or not value.strip():
            raise WorkflowError(f"line {i + 1}: expected 'key: value' in a mapping")
        mapping[key.strip()] = _scalar(value)
        i += 1
    return mapping, i


def _step(job: str, fields: dict[str, object], line: int) -> Step:
    run = fields.get("run")
    uses = fields.get("uses")
    if (run is None) == (uses is None):
        raise WorkflowError(f"step ending before line {line}: needs exactly one of run/uses")
    if "with" in fields and uses is None:
        raise WorkflowError(f"step ending before line {line}: 'with' without 'uses'")
    name = fields.get("name")
    if run is not None and not isinstance(name, str):
        raise WorkflowError(f"step ending before line {line}: a run step needs a name")
    env = fields.get("env", {})
    if not isinstance(env, dict):
        raise WorkflowError(f"step ending before line {line}: 'env' must be a mapping")
    timeout = fields.get("timeout-minutes")
    working = fields.get("working-directory")
    return Step(
        job=job,
        name=name if isinstance(name, str) else f"uses {uses}",
        run=run if isinstance(run, str) else None,
        working_directory=working if isinstance(working, str) else None,
        env=tuple(sorted(env.items())),
        timeout_minutes=int(timeout) if isinstance(timeout, str) else None,
    )


def parse_workflow(text: str) -> list[Step]:
    """The steps of every job, in file order.

    Parses the subset of YAML this workflow uses: `jobs:` at column 0, jobs
    at two spaces, `steps:` at four, steps at six, step keys at eight, flat
    mappings and `|` blocks beneath them.  Anything else raises.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    for number, line in enumerate(lines, 1):
        if re.match(r"(env|defaults|concurrency|permissions):", line):
            raise WorkflowError(f"line {number}: top-level {line.split(':')[0]!r} is not implemented")
    if "jobs:" not in lines:
        raise WorkflowError("no top-level 'jobs:' key")
    steps: list[Step] = []
    job: str | None = None
    in_steps = False
    fields: dict[str, object] | None = None
    i = lines.index("jobs:") + 1

    def flush() -> None:
        nonlocal fields
        if fields is not None and job is not None:
            steps.append(_step(job, fields, i + 1))
        fields = None

    while i < len(lines):
        line = lines[i]
        if _blank_or_comment(line):
            i += 1
            continue
        indent, body = _indent(line), line.strip()
        if indent == 0:
            break
        if indent == 2:
            flush()
            if not body.endswith(":"):
                raise WorkflowError(f"line {i + 1}: expected a job name")
            job, in_steps = body[:-1], False
            i += 1
            continue
        if indent == 4:
            flush()
            key = body.partition(":")[0]
            if key not in JOB_KEYS:
                raise WorkflowError(f"line {i + 1}: job key {key!r} is not implemented")
            in_steps = key == "steps"
            i += 1
            continue
        if not in_steps:
            raise WorkflowError(f"line {i + 1}: unexpected nesting outside steps")
        if indent == 6:
            if not body.startswith("- "):
                raise WorkflowError(f"line {i + 1}: expected a '- ' step item")
            flush()
            fields = {}
            body, indent = body[2:], 8
        if indent != 8 or fields is None:
            raise WorkflowError(f"line {i + 1}: unexpected indentation")
        key, sep, value = body.partition(":")
        key, value = key.strip(), value.strip()
        if not sep:
            raise WorkflowError(f"line {i + 1}: expected 'key: value'")
        if key not in STEP_KEYS:
            raise WorkflowError(f"line {i + 1}: step key {key!r} is not implemented")
        if value in ("|", "|-"):
            fields[key], i = _block(lines, i + 1, 8)
        elif value == "":
            fields[key], i = _mapping(lines, i + 1, 8)
        else:
            fields[key] = _scalar(value)
            i += 1
    flush()
    return steps


def resolve_env(step: Step, repo: Path) -> dict[str, str]:
    resolved: dict[str, str] = {}
    for key, value in step.env:
        value = value.replace(WORKSPACE_EXPR, repo.as_posix())
        if "${{" in value:
            raise WorkflowError(f"{step.name}: expression in env {key} is not implemented")
        resolved[key] = value
    return resolved


def select(
    steps: list[Step], jobs: list[str], fast: bool, pattern: str | None
) -> list[Step]:
    known = {s.job for s in steps}
    unknown = sorted(set(jobs) - known)
    if unknown:
        raise WorkflowError(f"no such job {unknown}; jobs are {sorted(known)}")
    chosen = [s for s in steps if s.run is not None and not s.is_setup]
    if jobs:
        chosen = [s for s in chosen if s.job in jobs]
    if fast:
        chosen = [s for s in chosen if s.is_fast]
    if pattern is not None:
        wanted = re.compile(pattern, re.IGNORECASE)
        chosen = [s for s in chosen if wanted.search(s.name)]
    return chosen


def check_contract(steps: list[Step]) -> None:
    """The names this runner holds must still exist in the workflow."""
    names = {s.name for s in steps}
    missing = sorted((SETUP_STEPS | {COVERAGE_STEP}) - names)
    if missing:
        raise WorkflowError(f"steps named by ci/run_gates.py are gone from the workflow: {missing}")
    for step in steps:
        if step.run is not None and "${{" in step.run:
            raise WorkflowError(f"{step.name}: expression in run is not implemented")
        resolve_env(step, REPO)


def find_bash() -> str:
    override = os.environ.get("GATES_BASH")
    if override:
        return override
    if os.name == "nt":
        # Git for Windows: <root>/mingw64/libexec/git-core -> <root>/bin/bash.exe,
        # the launcher that puts /usr/bin first.  A bare `bash` on PATH can be
        # the WSL one, which sees a different filesystem.
        exec_path = subprocess.run(
            ["git", "--exec-path"], capture_output=True, text=True, check=True
        ).stdout.strip()
        candidate = Path(exec_path).parents[2] / "bin" / "bash.exe"
        if candidate.is_file():
            return str(candidate)
        raise WorkflowError("Git for Windows bash not found; set GATES_BASH")
    found = shutil.which("bash")
    if found is None:
        raise WorkflowError("bash not found; set GATES_BASH")
    return found


def _posix_exe(path: str) -> str:
    """An interpreter path bash can execute: C:\\x\\y -> /c/x/y on Windows."""
    posix = Path(path).as_posix()
    if os.name == "nt" and re.match(r"[A-Za-z]:/", posix):
        posix = f"/{posix[0].lower()}{posix[2:]}"
    return posix


def prelude(python: str) -> str:
    exe = _posix_exe(python)
    return (
        f'python() {{ "{exe}" "$@"; }}\n'
        f'python3() {{ "{exe}" "$@"; }}\n'
        f'coverage() {{ "{exe}" -m coverage "$@"; }}\n'
        "export -f python python3 coverage\n"
    )


def parallel_tests(workers: int) -> str:
    """The pytest command of CLAUDE.md's parallel recipe, as one bash body.

    It runs under the same interpreter as every other step; see
    `pin_drift` for how that interpreter is compared with the pins."""
    return (
        f"python -m pytest -n {workers} --dist load --cov=code --cov-branch "
        "--cov-report=json:coverage.json --cov-report=term\n"
    )


def pin_drift(repo: Path) -> list[str]:
    """Installed versions that differ from the `name==version` lines of
    requirements.txt.  The hosted runner installs the pins; this runner uses
    whatever the interpreter has, so a difference is reported, not hidden."""
    drift: list[str] = []
    for line in (repo / "requirements.txt").read_text(encoding="utf-8").splitlines():
        name, sep, pinned = line.strip().partition("==")
        if not sep:
            continue
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed = "not installed"
        if installed != pinned:
            drift.append(f"{name} {installed} (requirements.txt pins {pinned})")
    return drift


def git_status(repo: Path) -> set[str]:
    out = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    return {entry for entry in out.split("\0") if entry}


def check_top_level(repo: Path) -> None:
    top = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=repo, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout.strip()
    if os.path.normcase(os.path.realpath(top)) != os.path.normcase(os.path.realpath(repo)):
        raise WorkflowError(
            f"{repo} is not the top of its own checkout (git's top level is {top}); "
            "a plain subdirectory shares the other checkout's HEAD. "
            "Use `git worktree add ../<name>` and run from there."
        )


@dataclasses.dataclass
class Result:
    step: Step
    outcome: str
    exit_code: int | None = None
    seconds: float = 0.0
    note: str = ""


def run_steps(
    steps: list[Step],
    repo: Path,
    bash: str,
    python: str,
    keep_going: bool = False,
    workers: int | None = None,
) -> list[Result]:
    results: list[Result] = []
    failed_jobs: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="gates-") as tmp:
        scratch = Path(tmp)
        runner_temp = scratch / "runner_temp"
        runner_temp.mkdir()
        for index, step in enumerate(steps):
            if step.job in failed_jobs and not keep_going:
                results.append(Result(step, "not run", note="an earlier step in this job failed"))
                continue
            assert step.run is not None
            body, note = step.run, ""
            if workers is not None and step.name == COVERAGE_STEP:
                body, note = parallel_tests(workers), f"parallel, {workers} workers"
            script = scratch / f"step{index:03d}.sh"
            script.write_bytes((prelude(python) + body).encode("utf-8"))
            env = dict(os.environ)
            env.update(resolve_env(step, repo))
            env.setdefault("PYTHONUTF8", "1")
            env["RUNNER_TEMP"] = runner_temp.as_posix()
            env["GITHUB_WORKSPACE"] = repo.as_posix()
            cwd = repo / step.working_directory if step.working_directory else repo
            print(f"\n=== [{step.job}] {step.name}" + (f"  ({note})" if note else ""), flush=True)
            started = time.monotonic()
            timeout = step.timeout_minutes * 60 if step.timeout_minutes else None
            try:
                proc = subprocess.run(
                    [bash, "--noprofile", "--norc", "-e", script.as_posix()],
                    cwd=cwd, env=env, timeout=timeout, check=False,
                )
                code: int | None = proc.returncode
                outcome = "pass" if code == 0 else "FAIL"
            except subprocess.TimeoutExpired:
                code, outcome = None, "TIMEOUT"
            seconds = time.monotonic() - started
            if outcome != "pass":
                failed_jobs.add(step.job)
            results.append(Result(step, outcome, code, seconds, note))
    return results


def report(results: list[Result], head: str, before: set[str], after: set[str]) -> str:
    width = max([len(r.step.name) for r in results] + [4])
    rows = [f"{'job':<9}{'step':<{width + 2}}{'result':<9}{'seconds':>8}"]
    for r in results:
        rows.append(f"{r.step.job:<9}{r.step.name:<{width + 2}}{r.outcome:<9}{r.seconds:>8.1f}"
                    + (f"  {r.note}" if r.note else ""))
    passed = sum(r.outcome == "pass" for r in results)
    rows.append("")
    rows.append(f"{passed} of {len(results)} selected steps passed at HEAD {head}")
    if before:
        rows.append(f"the working tree had {len(before)} uncommitted paths when the run started")
    changed = sorted(after ^ before)
    if changed:
        rows.append("git status changed during the run:")
        rows.extend(f"  {entry}" for entry in changed)
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--job", action="append", default=[], help="run only this job (repeatable)")
    parser.add_argument("--fast", action="store_true", help="only single-command python-job checks")
    parser.add_argument("--step", help="only steps whose name matches this regular expression")
    parser.add_argument("--list", action="store_true", help="print the selected steps and exit")
    parser.add_argument("--keep-going", action="store_true", help="do not stop a job at its first failure")
    parser.add_argument("--workers", type=int, help="run the root suite with pytest-xdist and N workers")
    parser.add_argument("--receipt", type=Path, help="also write the results as JSON here")
    args = parser.parse_args(argv)

    try:
        steps = parse_workflow(WORKFLOW.read_text(encoding="utf-8"))
        check_contract(steps)
        chosen = select(steps, args.job, args.fast, args.step)
        if not chosen:
            raise WorkflowError("the selection is empty")
        if args.list:
            for s in chosen:
                where = f"  (in {s.working_directory})" if s.working_directory else ""
                print(f"{s.job:<9}{'fast ' if s.is_fast else '     '}{s.name}{where}")
            return 0
        check_top_level(REPO)
        bash = find_bash()
        if args.workers is not None and any(s.name == COVERAGE_STEP for s in chosen):
            missing = [m for m in ("xdist", "pytest_cov") if importlib.util.find_spec(m) is None]
            if missing:
                raise WorkflowError(f"--workers needs pytest-xdist and pytest-cov; missing {missing}")
    except WorkflowError as exc:
        print(f"run_gates: {exc}", file=sys.stderr)
        return 2

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout.strip()
    drift = pin_drift(REPO)
    for line in drift:
        print(f"run_gates: installed {line}", file=sys.stderr)
    before = git_status(REPO)
    results = run_steps(chosen, REPO, bash, sys.executable, args.keep_going, args.workers)
    after = git_status(REPO)
    print("\n" + report(results, head, before, after))
    if drift:
        print("these results come from an interpreter whose packages differ from the pins:")
        print("\n".join(f"  {line}" for line in drift))
    if args.receipt is not None:
        receipt = {
            "head": head,
            "python": sys.version.split()[0],
            "packages_differing_from_pins": drift,
            "uncommitted_at_start": sorted(before),
            "status_changed_during_run": sorted(after ^ before),
            "steps": [
                {"job": r.step.job, "name": r.step.name, "outcome": r.outcome,
                 "exit_code": r.exit_code, "seconds": round(r.seconds, 1), "note": r.note}
                for r in results
            ],
        }
        args.receipt.write_bytes((json.dumps(receipt, indent=2) + "\n").encode("utf-8"))
    return 0 if all(r.outcome == "pass" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())

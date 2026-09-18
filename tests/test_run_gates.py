"""`ci/run_gates.py` runs the steps the workflow file declares, and only those.

The runner holds no gate list of its own, so the checks here are about the
reading: every gate command in the workflow is reached, the few names the
runner does hold still exist, workflow features it does not implement are
refused rather than approximated, and a failing step stops its own job
without stopping the others."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_gates", REPO / "ci" / "run_gates.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["run_gates"] = module
    spec.loader.exec_module(module)
    return module


rg = _load()

SAMPLE = """name: sample
on:
  push:
jobs:
  first:
    runs-on: x
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      # a comment between steps
      - name: One
        run: python -c "print(1)"
      - name: Two
        working-directory: sub
        env:
          PYTHONPATH: ${{ github.workspace }}/code
        timeout-minutes: 5
        run: |
          set -o pipefail
          echo a

          echo b
  second:
    runs-on: x
    steps:
      - name: Three
        run: echo 3
"""


def test_the_workflow_parses_and_the_names_the_runner_holds_exist() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))
    rg.check_contract(steps)
    assert {s.job for s in steps} == {"python", "lean", "research"}
    chosen = rg.select(steps, [], False, None)
    assert chosen and all(s.run for s in chosen)
    assert not any(s.is_setup for s in chosen)


def test_every_gate_command_in_the_workflow_is_reached() -> None:
    # Enumerated from the raw text, independently of the parser: a command
    # the parser dropped would be missing from the selected steps.
    text = rg.WORKFLOW.read_text(encoding="utf-8")
    live = "\n".join(line for line in text.splitlines() if not line.strip().startswith("#"))
    pattern = re.compile(r"python3? ((?:ci|research)/[A-Za-z0-9_./-]+\.py)")
    wanted = set(pattern.findall(live))
    assert wanted, "the pattern found no gate command in the workflow"
    chosen = rg.select(rg.parse_workflow(text), [], False, None)
    reached = {m for s in chosen for m in pattern.findall(s.run)}
    assert sorted(wanted - reached) == [], "gate commands the runner would not run"
    assert sorted(reached - wanted) == []


def test_fast_is_single_command_python_checks() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))
    fast = rg.select(steps, [], True, None)
    assert fast
    for step in fast:
        assert step.job == "python" and step.working_directory is None
        assert "\n" not in step.run.strip()
        assert "check_coverage" not in step.run


def test_parser_reads_blocks_mappings_and_comments() -> None:
    steps = rg.parse_workflow(SAMPLE)
    assert [(s.job, s.name) for s in steps] == [
        ("first", "uses actions/checkout@v4"),
        ("first", "One"),
        ("first", "Two"),
        ("second", "Three"),
    ]
    two = steps[2]
    assert two.run == "set -o pipefail\necho a\n\necho b\n"
    assert two.working_directory == "sub"
    assert two.timeout_minutes == 5
    assert rg.resolve_env(two, Path("/repo")) == {"PYTHONPATH": "/repo/code"}
    assert [s.name for s in rg.select(steps, ["second"], False, None)] == ["Three"]


@pytest.mark.parametrize(
    "line", ["        if: always()", "        shell: pwsh", "        continue-on-error: true"]
)
def test_unimplemented_step_keys_are_refused(line: str) -> None:
    text = SAMPLE.replace("        run: echo 3", f"{line}\n        run: echo 3")
    with pytest.raises(rg.WorkflowError, match="not implemented"):
        rg.parse_workflow(text)


def test_top_level_and_job_level_settings_are_refused() -> None:
    with pytest.raises(rg.WorkflowError, match="not implemented"):
        rg.parse_workflow("env:\n  X: 1\n" + SAMPLE)
    job_env = SAMPLE.replace("  second:\n    runs-on: x\n", "  second:\n    runs-on: x\n    env:\n      X: 1\n")
    with pytest.raises(rg.WorkflowError, match="not implemented"):
        rg.parse_workflow(job_env)


def test_an_unknown_expression_is_refused() -> None:
    step = rg.Step(job="j", name="n", run="echo", env=(("X", "${{ secrets.T }}"),))
    with pytest.raises(rg.WorkflowError, match="not implemented"):
        rg.resolve_env(step, Path("/r"))


def test_an_unknown_job_is_refused() -> None:
    with pytest.raises(rg.WorkflowError, match="no such job"):
        rg.select(rg.parse_workflow(SAMPLE), ["third"], False, None)


def test_packages_differing_from_the_pins_are_reported(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text(
        "pytest==0.0.1\nzzz-no-such-package==1.0\n# a comment\n", encoding="utf-8"
    )
    drift = rg.pin_drift(tmp_path)
    assert len(drift) == 2
    assert drift[0].startswith("pytest ") and drift[0].endswith("(requirements.txt pins 0.0.1)")
    assert drift[1] == "zzz-no-such-package not installed (requirements.txt pins 1.0)"


def _bash() -> str:
    try:
        bash: str = rg.find_bash()
    except (rg.WorkflowError, OSError, subprocess.CalledProcessError):
        pytest.skip("no bash on this machine")
    return bash


RUN = """jobs:
  a:
    steps:
      - name: ok
        run: python -c "open('ran_ok', 'w').close()"
      - name: fails
        run: |
          false | cat
          exit 3
      - name: after the failure
        run: python -c "open('ran_after', 'w').close()"
  b:
    steps:
      - name: other job
        working-directory: sub
        env:
          MARK: ${{ github.workspace }}/marker
        run: |
          test -d "$RUNNER_TEMP"
          python -c "import os, sys; open(os.environ['MARK'], 'w').write(os.getcwd() + '\\n' + sys.executable)"
          coverage --version > coverage.txt
"""


def test_a_failure_stops_its_own_job_and_not_the_others(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    steps = rg.select(rg.parse_workflow(RUN), [], False, None)
    results = rg.run_steps(steps, tmp_path, _bash(), sys.executable)
    assert [r.outcome for r in results] == ["pass", "FAIL", "not run", "pass"]
    assert results[1].exit_code == 3
    assert (tmp_path / "ran_ok").exists()
    assert not (tmp_path / "ran_after").exists()
    cwd, exe = (tmp_path / "marker").read_text(encoding="utf-8").split("\n")
    assert Path(cwd).resolve() == (tmp_path / "sub").resolve()
    assert Path(exe).resolve() == Path(sys.executable).resolve()
    assert "Coverage.py" in (tmp_path / "sub" / "coverage.txt").read_text(encoding="utf-8")


def test_keep_going_runs_every_step(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    steps = rg.select(rg.parse_workflow(RUN), ["a"], False, None)
    results = rg.run_steps(steps, tmp_path, _bash(), sys.executable, keep_going=True)
    assert [r.outcome for r in results] == ["pass", "FAIL", "pass"]
    assert (tmp_path / "ran_after").exists()


def test_a_plain_subdirectory_is_not_a_checkout(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "inner").mkdir()
    rg.check_top_level(tmp_path)
    with pytest.raises(rg.WorkflowError, match="not the top of its own checkout"):
        rg.check_top_level(tmp_path / "inner")

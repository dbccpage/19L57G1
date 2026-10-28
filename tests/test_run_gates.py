"""`ci/run_gates.py` runs the steps the workflow file declares, and only those.

The runner holds no gate list of its own, so the checks here are about the
reading and the running: every gate command in the workflow is reached, the
few names the runner holds still match, workflow forms it does not implement
are refused rather than approximated, and the local stand-ins for a fresh
hosted checkout (stale outputs removed, protected files restored, caller
variables dropped, a timed-out step killed with its children) hold."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import time
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
    runs-on: ubuntu-latest
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
    runs-on: ubuntu-latest
    steps:
      - name: Three
        run: echo 3
"""


def test_the_workflow_parses_and_the_names_the_runner_holds_match() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))
    rg.check_contract(steps)
    assert {"python", "lean", "research", "textbook"} <= {s.job for s in steps}


def test_every_job_sets_up_python_and_pinned_dependencies_before_python_commands() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))
    jobs = sorted({s.job for s in steps})
    for job in jobs:
        job_steps = [s for s in steps if s.job == job]
        setup_idx = next((i for i, s in enumerate(job_steps) if s.uses == "actions/setup-python@v5"), None)
        deps_idx = next((i for i, s in enumerate(job_steps) if s.name == "Install pinned dependencies"), None)
        first_py = next(
            (i for i, s in enumerate(job_steps) if s.run and not s.is_setup and re.search(r"\bpython3?\b", s.run)),
            None,
        )
        assert setup_idx is not None, f"job {job!r} is missing actions/setup-python@v5"
        assert deps_idx is not None, f"job {job!r} is missing Install pinned dependencies"
        if first_py is not None:
            assert setup_idx < deps_idx < first_py, (
                f"job {job!r} runs Python at step {first_py} before setup-python ({setup_idx}) / deps ({deps_idx})"
            )
    chosen = rg.select(steps, [], False, None)
    assert chosen and not any(s.is_setup for s in chosen)
    assert {s.uses for s in chosen if s.uses} <= set(rg.ACTIONS)


def test_lean_census_stays_last_after_the_declaration_audit() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))
    lean = [s for s in steps if s.job == "lean" and s.run is not None and not s.is_setup]
    assert lean[-1].name == "Every Lean module elaborates"
    assert lean[-1].run.strip() == "python3 ../ci/gate_support.py lean-census"
    census = next(i for i, s in enumerate(lean) if s.run.strip() == "python3 ci/check_declaration_axioms.py")
    assert 0 < census < len(lean) - 1


def test_every_gate_command_in_the_workflow_is_reached() -> None:
    # Enumerated from the raw text, independently of the parser: a command
    # the parser dropped would be missing from the selected steps.
    text = rg.WORKFLOW.read_text(encoding="utf-8")
    live = "\n".join(line for line in text.splitlines() if not line.strip().startswith("#"))
    pattern = re.compile(r"python3? ((?:ci|research)/[A-Za-z0-9_./-]+\.py)")
    wanted = set(pattern.findall(live))
    assert wanted, "the pattern found no gate command in the workflow"
    chosen = rg.select(rg.parse_workflow(text), [], False, None)
    reached = {m for s in chosen if s.run for m in pattern.findall(s.run)}
    assert sorted(wanted - reached) == [], "gate commands the runner would not run"
    assert sorted(reached - wanted) == []


def test_fast_is_single_command_python_checks_and_their_preconditions() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))
    fast = rg.select(steps, [], True, None)
    commands = [s for s in fast if s.run]
    assert commands
    for step in commands:
        assert step.job == "python" and step.working_directory is None
        assert "\n" not in step.run.strip()
        assert "check_coverage" not in step.run
    assert {s.uses for s in fast if s.uses} == {"actions/checkout@v4", "actions/setup-python@v5"}


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
    assert dict(steps[0].with_) == {"fetch-depth": "0"}
    assert [s.name for s in rg.select(steps, ["second"], False, None)] == ["Three"]


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("        run: echo 3", "        if: always()\n        run: echo 3"),
        ("        run: echo 3", "        shell: pwsh\n        run: echo 3"),
        ("        run: echo 3", '        run: "echo \\"3\\""'),
        ("        run: echo 3", "        run: echo 3 # trailing note"),
        ("        run: echo 3", "        timeout-minutes: 1.5\n        run: echo 3"),
        ("        run: echo 3", "        run: >\n          echo 3"),
        ("        run: echo 3", "        run: |-\n          echo 3"),
        ("        run: echo 3", "\trun: echo 3"),
        ("        run: echo 3", "        run: |\n          cat <<EOF\nEOF"),
        ("    runs-on: ubuntu-latest\n    steps:\n      - name: Three",
         "    runs-on: windows-latest\n    steps:\n      - name: Three"),
        ("  second:\n    runs-on: ubuntu-latest\n", "  second:\n    runs-on: ubuntu-latest\n    env:\n      X: 1\n"),
    ],
)
def test_unimplemented_forms_are_refused(old: str, new: str) -> None:
    assert SAMPLE.count(old) == 1
    with pytest.raises(rg.WorkflowError):
        rg.parse_workflow(SAMPLE.replace(old, new))


def test_top_level_settings_are_refused() -> None:
    with pytest.raises(rg.WorkflowError, match="not implemented"):
        rg.parse_workflow("env:\n  X: 1\n" + SAMPLE)


def test_the_contract_refuses_what_the_runner_cannot_stand_in_for() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))
    extra_action = rg.Step(job="python", name="uses example/gate@v1", run=None, uses="example/gate@v1")
    with pytest.raises(rg.WorkflowError, match="no local meaning"):
        rg.check_contract([*steps, extra_action])
    installer = rg.Step(job="python", name="Install extras", run="pip install -r extra.txt\n")
    with pytest.raises(rg.WorkflowError, match="not in SETUP_STEPS"):
        rg.check_contract([*steps, installer])
    changed = [
        rg.Step(job=s.job, name=s.name, run="coverage run -m pytest -q -x\n")
        if s.name == rg.COVERAGE_STEP else s
        for s in steps
    ]
    with pytest.raises(rg.WorkflowError, match="body changed"):
        rg.check_contract(changed)
    step = rg.Step(job="j", name="n", run="echo", env=(("X", "${{ secrets.T }}"),))
    with pytest.raises(rg.WorkflowError, match="not implemented"):
        rg.resolve_env(step, Path("/r"))
    with pytest.raises(rg.WorkflowError, match="no such job"):
        rg.select(rg.parse_workflow(SAMPLE), ["third"], False, None)


def _bash() -> str:
    try:
        bash: str = rg.find_bash()
    except (rg.WorkflowError, OSError):
        pytest.skip("no bash on this machine")
    return bash


RUN = """jobs:
  a:
    runs-on: ubuntu-latest
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
    runs-on: ubuntu-latest
    steps:
      - name: other job
        working-directory: sub
        env:
          MARK: ${{ github.workspace }}/marker
        run: |
          test -d "$RUNNER_TEMP"
          python -c "import os, sys; open(os.environ['MARK'], 'w').write(os.getcwd() + '\\n' + sys.executable + '\\n' + os.environ.get('PYTEST_ADDOPTS', 'absent'))"
          coverage --version > coverage.txt
"""


def test_a_failure_stops_its_own_job_and_not_the_others(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PYTEST_ADDOPTS", "-k leaked")
    (tmp_path / "sub").mkdir()
    steps = rg.select(rg.parse_workflow(RUN), [], False, None)
    results = rg.run_steps(steps, tmp_path, _bash(), sys.executable)
    assert [r.outcome for r in results] == ["pass", "FAIL", "not run", "pass"]
    assert results[1].exit_code == 3
    assert (tmp_path / "ran_ok").exists()
    assert not (tmp_path / "ran_after").exists()
    cwd, exe, addopts = (tmp_path / "marker").read_text(encoding="utf-8").split("\n")
    assert Path(cwd).resolve() == (tmp_path / "sub").resolve()
    assert Path(exe).resolve() == Path(sys.executable).resolve()
    assert addopts == "absent"
    assert "Coverage.py" in (tmp_path / "sub" / "coverage.txt").read_text(encoding="utf-8")


def test_keep_going_and_continue_on_error(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    steps = rg.select(rg.parse_workflow(RUN), ["a"], False, None)
    results = rg.run_steps(steps, tmp_path, _bash(), sys.executable, keep_going=True)
    assert [r.outcome for r in results] == ["pass", "FAIL", "pass"]
    allowed = RUN.replace("      - name: fails\n", "      - name: fails\n        continue-on-error: true\n")
    results = rg.run_steps(rg.select(rg.parse_workflow(allowed), ["a"], False, None),
                           tmp_path, _bash(), sys.executable)
    assert [r.outcome for r in results] == ["pass", "FAIL", "pass"]
    assert "continue-on-error" in results[1].note


def test_shell_bash_sets_pipefail(tmp_path: Path) -> None:
    body = "jobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n      - name: pipe\n{shell}        run: |\n          false | cat\n"
    plain = rg.parse_workflow(body.format(shell=""))
    strict = rg.parse_workflow(body.format(shell="        shell: bash\n"))
    assert rg.run_steps(plain, tmp_path, _bash(), sys.executable)[0].outcome == "pass"
    assert rg.run_steps(strict, tmp_path, _bash(), sys.executable)[0].outcome == "FAIL"


def test_a_missing_working_directory_fails_the_step_not_the_run(tmp_path: Path) -> None:
    steps = [rg.Step(job="a", name="gone", run="true\n", working_directory="nowhere"),
             rg.Step(job="b", name="next", run="true\n")]
    results = rg.run_steps(steps, tmp_path, _bash(), sys.executable)
    assert [r.outcome for r in results] == ["FAIL", "pass"]
    assert "does not exist" in results[0].note


def test_a_timed_out_step_is_killed_with_its_children(tmp_path: Path) -> None:
    body = "sleep 2\necho late > late.txt\n"
    step = rg.Step(job="a", name="slow", run=body, timeout_minutes=0.5 / 60)
    results = rg.run_steps([step], tmp_path, _bash(), sys.executable)
    assert results[0].outcome == "TIMEOUT"
    time.sleep(3)
    assert not (tmp_path / "late.txt").exists(), "the step kept running after its timeout"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, check=True,
                   capture_output=True)


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "sealed.txt").write_bytes(b"committed\n")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "c")
    return tmp_path


def test_a_step_that_rewrites_a_protected_file_fails_and_the_file_is_put_back(
    tmp_path: Path,
) -> None:
    repo = _repo(tmp_path)
    steps = [rg.Step(job="a", name="rewrite", run="echo changed > artifacts/sealed.txt\n"),
             rg.Step(job="a", name="after", run="true\n")]
    results = rg.run_steps(steps, repo, _bash(), sys.executable)
    assert [r.outcome for r in results] == ["FAIL", "not run"]
    assert "rewrote artifacts/sealed.txt; restored" in results[0].note
    assert (repo / "artifacts" / "sealed.txt").read_bytes() == b"committed\n"


def test_a_timeout_restores_tracked_research_receipts(tmp_path: Path) -> None:
    """A step killed by its timeout has its tracked research receipts put
    back, and the note names them.

    The step writes the receipt, then an untracked marker, then outlives
    every timeout below.  Whether the kill lands after the write is a race
    with the shell's start-up, which a loaded machine can lose: on
    2026-09-24 a 0.5 s timeout fired before the write, so nothing had been
    rewritten and the note was empty.  The timeout therefore doubles until
    the marker shows the write happened.  The restore note is asserted on
    that attempt, and the receipt's bytes on every attempt."""
    repo = _repo(tmp_path)
    receipt = repo / "research/probe/receipts/value.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_bytes(b"original\n")
    _git(repo, "add", "--", "research/probe/receipts/value.json")
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "receipt")
    marker = repo / "written.marker"
    body = ("echo partial > research/probe/receipts/value.json\n"
            "echo written > written.marker\n"
            "sleep 60\n")
    for seconds in (1, 2, 4, 8, 16):
        marker.unlink(missing_ok=True)
        step = rg.Step(job="a", name="interrupted receipt", timeout_minutes=seconds / 60,
                       run=body)
        result = rg.run_steps([step], repo, _bash(), sys.executable)[0]
        assert result.outcome == "TIMEOUT"
        assert receipt.read_bytes() == b"original\n", (
            f"research/probe/receipts/value.json was not restored after a {seconds} s timeout")
        if marker.is_file():
            assert "research/probe/receipts/value.json; restored" in result.note, (
                f"the note does not name the restored receipt: {result.note!r}")
            return
    pytest.fail("the step never wrote its receipt before a 16 s timeout")


def test_nothing_is_put_back_and_nothing_more_runs_after_head_moves(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    moves = ("echo changed > artifacts/sealed.txt\n"
             "git -c user.name=t -c user.email=t@t commit -q --allow-empty -m moved\n")
    steps = [rg.Step(job="a", name="moves", run=moves),
             rg.Step(job="b", name="later", run="true\n")]
    results = rg.run_steps(steps, repo, _bash(), sys.executable)
    assert [r.outcome for r in results] == ["pass", "not run"]
    assert "HEAD moved" in results[0].note and "HEAD moved" in results[1].note
    assert (repo / "artifacts" / "sealed.txt").read_bytes() == b"changed\n"


def test_a_timed_out_step_loses_the_programs_its_shell_started(tmp_path: Path) -> None:
    body = "bash -c 'sleep 2; echo late > late.txt'\n"
    step = rg.Step(job="a", name="slow", run=body, timeout_minutes=0.5 / 60)
    assert rg.run_steps([step], tmp_path, _bash(), sys.executable)[0].outcome == "TIMEOUT"
    time.sleep(3)
    assert not (tmp_path / "late.txt").exists(), "a program the step started outlived it"


def test_python_and_shell_settings_of_the_caller_are_dropped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("PYTHONOPTIMIZE", "PYTHONPATH", "MYPYPATH", "COVERAGE_FILE", "BASH_ENV"):
        monkeypatch.setenv(name, "leaked")
    env = rg.step_env(rg.Step(job="a", name="n", run="true\n"), tmp_path, tmp_path)
    leaked = [k for k in env if k.upper() in ("PYTHONOPTIMIZE", "PYTHONPATH", "MYPYPATH",
                                               "COVERAGE_FILE", "BASH_ENV")]
    assert leaked == [] and env["PYTHONUTF8"] == "1"


def test_setup_bodies_action_inputs_duplicates_and_installers_are_checked() -> None:
    steps = rg.parse_workflow(rg.WORKFLOW.read_text(encoding="utf-8"))

    def swap(name: str, **changes: object) -> list[object]:
        return [rg.dataclasses.replace(s, **changes) if s.name == name else s for s in steps]

    with pytest.raises(rg.WorkflowError, match="body changed"):
        rg.check_contract(swap("Install elan", run="curl example | sh\n"))
    checkout = next(s for s in steps if s.uses == "actions/checkout@v4")
    for inputs, message in (((("ref", "v1"),), "not implemented"),
                            ((("fetch-depth", "1"),), "fetch-depth 0")):
        changed = [rg.dataclasses.replace(s, with_=inputs) if s is checkout else s for s in steps]
        with pytest.raises(rg.WorkflowError, match=message):
            rg.check_contract(changed)
    for body in ("uv sync\n", "curl -sSf https://example | sh\n", "python -m pip install x\n",
                 "apt-get -y install x\n", "lake exe cache get\n"):
        with pytest.raises(rg.WorkflowError, match="not in SETUP_STEPS"):
            rg.check_contract([*steps, rg.Step(job="python", name="sneaky", run=body)])
    for doubled in ("        env:\n          A: 1\n        env:\n          B: 2\n        run: echo 3",
                    "        env:\n          A: 1\n          A: 2\n        run: echo 3"):
        with pytest.raises(rg.WorkflowError, match="duplicate"):
            rg.parse_workflow(SAMPLE.replace("        run: echo 3", doubled))
    with pytest.raises(rg.WorkflowError, match="duplicate job"):
        rg.parse_workflow(SAMPLE + "  first:\n    runs-on: ubuntu-latest\n")
    with pytest.raises(rg.WorkflowError, match="not implemented"):
        rg.parse_workflow(SAMPLE.replace("  second:\n    runs-on: ubuntu-latest\n",
                                         "  second:\n    runs-on: ubuntu-latest\n    needs: first\n"))


def test_an_unwritable_receipt_is_refused_before_anything_runs(tmp_path: Path) -> None:
    assert rg.main(["--fast", "--receipt", str(tmp_path / "missing" / "r.json")]) == 2


def test_outputs_left_by_an_earlier_run_are_removed_and_tracked_ones_kept(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / "artifacts_ci").mkdir()
    (repo / "artifacts_ci" / "old.json").write_text("{}", encoding="utf-8")
    (repo / "coverage.json").write_text("{}", encoding="utf-8")
    (repo / "lake_build.log").write_text("tracked", encoding="utf-8")
    _git(repo, "add", "lake_build.log")
    assert rg.clear_stale_outputs(repo) == ["coverage.json", "artifacts_ci"]
    assert not (repo / "artifacts_ci").exists() and (repo / "lake_build.log").exists()


def test_the_checkout_and_interpreter_checks(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    here = f"{sys.version_info.major}.{sys.version_info.minor}"
    setup = rg.Step(job="a", name="setup", run=None, uses="actions/setup-python@v5",
                    with_=(("python-version", here),))
    other = rg.Step(job="a", name="setup", run=None, uses="actions/setup-python@v5",
                    with_=(("python-version", "2.7"),))
    checkout = rg.Step(job="a", name="checkout", run=None, uses="actions/checkout@v4")
    assert rg.run_action(setup, repo).outcome == "pass"
    assert rg.run_action(other, repo).outcome == "FAIL"
    result = rg.run_action(checkout, repo)
    assert result.outcome == "pass" and "could not compare" in result.note


def test_two_runs_cannot_hold_the_lock_at_once(tmp_path: Path) -> None:
    # A lock file of its own: the real one may be held by a runner that is
    # running this very suite.
    lock = tmp_path / "run_gates.lock"
    with rg.machine_lock(lock):
        with pytest.raises(rg.WorkflowError, match="another run"):
            with rg.machine_lock(lock):
                pass


def test_status_folds_a_rename_into_one_entry(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _git(repo, "mv", "artifacts/sealed.txt", "artifacts/moved.txt")
    assert rg.git_status(repo) == {"R  artifacts/moved.txt <- artifacts/sealed.txt"}


def test_a_plain_subdirectory_is_not_a_checkout(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "inner").mkdir()
    rg.check_top_level(tmp_path)
    with pytest.raises(rg.WorkflowError, match="not the top of its own checkout"):
        rg.check_top_level(tmp_path / "inner")


def test_packages_differing_from_the_pins_are_reported(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text(
        "pytest==0.0.1\nzzz-no-such-package==1.0\n# a comment\n", encoding="utf-8"
    )
    drift = rg.pin_drift(tmp_path)
    assert len(drift) == 2
    assert drift[0].startswith("pytest ") and drift[0].endswith("(requirements.txt pins 0.0.1)")
    assert drift[1] == "zzz-no-such-package not installed (requirements.txt pins 1.0)"

"""Gate failures must name missing work and preserve incoming receipt bytes."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest

SPEC = importlib.util.spec_from_file_location("gate_support", Path(__file__).resolve().parents[1] / "ci/gate_support.py")
assert SPEC and SPEC.loader
gs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gs)


@pytest.mark.parametrize("count", [0, 7])
def test_too_few_tests_fail_by_name_then_recover(tmp_path: Path, count: int) -> None:
    log = tmp_path / "population.log"
    log.write_text(f"Ran {count} tests in 0.1s\nOK\n")
    with pytest.raises(ValueError, match=r"population.log: ran .* minimum is 8"):
        gs.test_count(log, 8)
    log.write_text("Ran 9 tests in 0.1s\nOK\n")
    assert gs.test_count(log, 8) == 0


@pytest.mark.parametrize("text", ["", "prefix Ran 9 tests in 1s", "Ran 9 tests in 1s\nRan 10 tests in 1s"])
def test_missing_or_ambiguous_summary_is_refused(tmp_path: Path, text: str) -> None:
    log = tmp_path / "summary.log"
    log.write_text(text)
    with pytest.raises(ValueError, match="summary.log: expected one test summary"):
        gs.test_count(log, 1)


def test_zero_minimum_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="minimum must be positive"):
        gs.test_count(tmp_path / "unused", 0)


@pytest.mark.parametrize("summary", [
    "7 passed in 0.10s",
    "7 passed, 3 skipped in 0.10s",
    "2 failed, 7 passed in 1.00s",
    "==================== 7 passed, 1 warning in 75.12s (0:01:15) ====================",
])
def test_pytest_passed_count_below_minimum_fails_by_name_then_recovers(tmp_path: Path, summary: str) -> None:
    log = tmp_path / "pytest.log"
    log.write_text("....... [100%]\n" + summary + "\n")
    with pytest.raises(ValueError, match=r"pytest.log: ran 7 tests; minimum is 8"):
        gs.test_count(log, 8, "pytest")
    assert gs.test_count(log, 7, "pytest") == 0


@pytest.mark.parametrize("text", [
    "",
    "no tests ran in 0.01s",
    "Ran 9 tests in 1s",
    "9 passed in 1.00s\n9 passed in 1.00s",
])
def test_missing_or_ambiguous_pytest_summary_is_refused(tmp_path: Path, text: str) -> None:
    log = tmp_path / "summary.log"
    log.write_text(text)
    with pytest.raises(ValueError, match="summary.log: expected one test summary"):
        gs.test_count(log, 1, "pytest")


def test_pytest_summary_without_a_pass_counts_zero(tmp_path: Path) -> None:
    log = tmp_path / "skips.log"
    log.write_text("3 skipped in 0.01s\n")
    with pytest.raises(ValueError, match=r"skips.log: ran 0 tests; minimum is 1"):
        gs.test_count(log, 1, "pytest")


def test_unknown_runner_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unknown test runner 'nose'"):
        gs.test_count(tmp_path / "unused", 1, "nose")


def test_runner_flag_reaches_the_cli(tmp_path: Path) -> None:
    log = tmp_path / "cli.log"
    log.write_text("5 passed in 0.20s\n")
    assert gs.main(["test-count", str(log), "--minimum", "5", "--runner", "pytest"]) == 0
    assert gs.main(["test-count", str(log), "--minimum", "6", "--runner", "pytest"]) == 1
    assert gs.main(["test-count", str(log), "--minimum", "5"]) == 1


def package(tmp_path: Path) -> Path:
    (tmp_path / "lean4/Derivation/Nested").mkdir(parents=True)
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "lean4/Derivation/One.lean").write_text("-- fixture\n")
    (tmp_path / "lean4/Derivation/Nested/Two.lean").write_text("-- fixture\n")
    (tmp_path / "artifacts/elaborated_modules.txt").write_text("Derivation.Nested.Two\nDerivation.One\n")
    return tmp_path


def test_recursive_census_is_one_command_and_propagates_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = package(tmp_path)
    calls = []
    def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args, 3)
    monkeypatch.setattr(gs.subprocess, "run", run)
    assert gs.lean_census(repo) == 3
    assert len(calls) == 1
    assert calls[0][0] == ["lake", "build", "Derivation.Nested.Two", "Derivation.One"]
    assert calls[0][1]["cwd"] == repo / "lean4"


def test_partial_census_names_missing_module_before_build(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = package(tmp_path)
    (repo / "lean4/Derivation/One.lean").unlink()
    def no_build(*args: object, **kwargs: object) -> None:
        pytest.fail("a mismatched census must not build")
    monkeypatch.setattr(gs.subprocess, "run", no_build)
    with pytest.raises(ValueError, match=r"elaborated_modules.txt:.*Derivation.One"):
        gs.lean_census(repo)


def test_empty_census_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="enumerated no modules"):
        gs.lean_census(tmp_path)


def receipt_repo(tmp_path: Path) -> tuple[Path, Path]:
    def git(*args: str) -> None:
        subprocess.run(["git", "-C", str(tmp_path), *args], check=True, capture_output=True)
    git("init", "-q")
    git("config", "user.name", "gate-test")
    git("config", "user.email", "gate-test@example.invalid")
    git("config", "core.autocrlf", "false")
    tree = tmp_path / "research/probe"
    tree.mkdir(parents=True)
    receipt = tree / "receipt.json"
    receipt.write_bytes(b"committed\n")
    git("add", "--", "research/probe/receipt.json")
    git("commit", "-qm", "fixture")
    return tree, receipt


def command(data: bytes, exit_code: int = 0) -> list[str]:
    return [sys.executable, "-c", f"from pathlib import Path; Path('receipt.json').write_bytes({data!r}); raise SystemExit({exit_code})"]


def test_stale_receipt_fails_and_original_bytes_are_restored(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    tree, receipt = receipt_repo(tmp_path)
    assert gs.receipt_replay(tree, ["receipt.json"], command(b"new computation\n")) == 1
    assert "receipt.json differs from fresh reproduction" in capsys.readouterr().err
    assert receipt.read_bytes() == b"committed\n"
    assert gs.receipt_replay(tree, ["receipt.json"], command(b"committed\n")) == 0


def test_failed_generator_restores_dirty_worktree_bytes(tmp_path: Path) -> None:
    tree, receipt = receipt_repo(tmp_path)
    receipt.write_bytes(b"incoming edit\r\n")
    assert gs.receipt_replay(tree, ["receipt.json"], command(b"partial output\n", 7)) == 7
    assert receipt.read_bytes() == b"incoming edit\r\n"


def test_comparison_uses_commit_instead_of_dirty_starting_bytes(tmp_path: Path) -> None:
    tree, receipt = receipt_repo(tmp_path)
    receipt.write_bytes(b"new computation\n")
    assert gs.receipt_replay(tree, ["receipt.json"], command(b"new computation\n")) == 1
    assert receipt.read_bytes() == b"new computation\n"


def test_replay_refuses_escape_and_missing_outputs(tmp_path: Path) -> None:
    tree, _ = receipt_repo(tmp_path)
    for name in ("../escape", "missing.json"):
        with pytest.raises(ValueError, match="receipt"):
            gs.receipt_replay(tree, [name], command(b"unused"))


def test_newer_checkout_bytes_are_not_overwritten_after_head_moves(tmp_path: Path) -> None:
    tree, receipt = receipt_repo(tmp_path)
    script = (
        "from pathlib import Path; import subprocess; "
        "Path('receipt.json').write_bytes(b'new commit\\n'); "
        "subprocess.run(['git', 'add', '--', 'receipt.json'], check=True); "
        "subprocess.run(['git', 'commit', '-qm', 'new output'], check=True)"
    )
    with pytest.raises(ValueError, match="HEAD moved during receipt reproduction"):
        gs.receipt_replay(tree, ["receipt.json"], [sys.executable, "-c", script])
    assert receipt.read_bytes() == b"new commit\n"

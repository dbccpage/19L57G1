"""Small local gate operations with named failures. AuthorityEffect: None."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys
from collections.abc import Sequence

REPO = Path(__file__).resolve().parent.parent
TEST_SUMMARY = re.compile(r"^Ran (\d+) tests? in .+$", re.MULTILINE)
MODULE_NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*\Z")


def test_count(log: Path, minimum: int) -> int:
    if minimum < 1:
        raise ValueError("test-count minimum must be positive")
    counts = TEST_SUMMARY.findall(log.read_text(encoding="utf-8"))
    if len(counts) != 1:
        raise ValueError(f"{log}: expected one test summary, found {len(counts)}")
    actual = int(counts[0])
    if actual < minimum:
        raise ValueError(f"{log}: ran {actual} tests; minimum is {minimum}")
    print(f"{log}: {actual} tests meet minimum {minimum}")
    return 0


def lean_census(repo: Path) -> int:
    lean = repo / "lean4"
    paths = sorted((lean / "Derivation").rglob("*.lean"))
    modules = sorted(p.relative_to(lean).with_suffix("").as_posix().replace("/", ".")
                     for p in paths)
    if not modules:
        raise ValueError("Lean source census enumerated no modules")
    if len(set(modules)) != len(modules) or any(not MODULE_NAME.fullmatch(m) for m in modules):
        raise ValueError("Lean census has duplicate or malformed module names")
    pin = repo / "artifacts/elaborated_modules.txt"
    expected = pin.read_text(encoding="utf-8").splitlines()
    if modules != expected:
        missing = sorted(set(expected) - set(modules))
        extra = sorted(set(modules) - set(expected))
        raise ValueError(f"{pin}: source census differs; missing={missing}, extra={extra}; order must match")
    print(f"source census: {len(modules)} modules; one lake build invocation", flush=True)
    return subprocess.run(["lake", "build", *modules], cwd=lean, check=False).returncode


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def receipt_replay(cwd: Path, paths: Sequence[str], command: Sequence[str]) -> int:
    """Compare fresh bytes with HEAD and restore the exact incoming worktree.

    Output paths must be existing tracked files, each explicitly named. No
    directory sweep, untracked deletion, index write, or shell is used.
    """
    if not paths or not command:
        raise ValueError("receipt replay requires output files and a command")
    repo = Path(git(cwd, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    current = cwd.resolve()
    if not current.is_relative_to(repo):
        raise ValueError("receipt working directory is outside its repository")
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    originals: dict[Path, bytes] = {}
    committed: dict[Path, bytes] = {}
    for name in paths:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"receipt path must stay in the working directory: {name}")
        path = current / relative
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(current):
            raise ValueError(f"receipt must be an existing local file: {name}")
        if path in originals:
            raise ValueError(f"duplicate receipt path: {name}")
        tracked = path.relative_to(repo).as_posix()
        committed[path] = git(repo, "show", f"{head}:{tracked}")
        originals[path] = path.read_bytes()
    if git(repo, "rev-parse", "HEAD").decode().strip() != head:
        raise ValueError("HEAD moved before receipt reproduction")
    args = list(command)
    if args[0] in ("python", "python3"):
        args[0] = sys.executable
    failures: list[str] = []
    status = 1
    try:
        status = subprocess.run(args, cwd=current, check=False).returncode
        for path, expected in committed.items():
            if not path.is_file() or path.is_symlink() or path.read_bytes() != expected:
                failures.append(f"{path.relative_to(current)} differs from fresh reproduction")
    finally:
        if git(repo, "rev-parse", "HEAD").decode().strip() != head:
            raise ValueError("HEAD moved during receipt reproduction; newer checkout bytes left intact")
        for path, data in originals.items():
            if path.is_symlink():
                path.unlink()
            path.write_bytes(data)
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    if status:
        print(f"FAIL: receipt command exited {status}", file=sys.stderr)
        return status
    if failures:
        return 1
    print(f"receipt replay: {len(paths)} committed outputs match; original bytes restored")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    count = modes.add_parser("test-count")
    count.add_argument("log", type=Path)
    count.add_argument("--minimum", type=int, required=True)
    lean = modes.add_parser("lean-census")
    lean.add_argument("--repo", type=Path, default=REPO)
    replay = modes.add_parser("replay")
    replay.add_argument("--file", action="append", required=True)
    replay.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        if args.mode == "test-count":
            return test_count(args.log, args.minimum)
        if args.mode == "lean-census":
            return lean_census(args.repo.resolve())
        command = args.command[1:] if args.command[:1] == ["--"] else args.command
        return receipt_replay(Path.cwd(), args.file, command)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

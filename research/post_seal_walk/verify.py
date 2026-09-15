"""Read-only verification of the post-seal history ledgers.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
SEAL = "052e65739ddfd8c23c657562a51288cb083a2464"
WALK_SNAPSHOT = "0e7814089db5ed387489acd9553a9105b0b69462"
ORIGIN_SNAPSHOT = "dfe649445403d7d0326594c918430ae5456b1f6b"


def git_lines(*args: str) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.splitlines()


def verify_ledger(path: Path, revision: str, expected_count: int) -> None:
    if not path.is_file():
        raise RuntimeError(f"missing ledger: {path.name}")
    expected = path.read_text(encoding="utf-8").splitlines()
    actual = git_lines("log", "--format=%H%x09%ci", revision)
    if len(expected) != expected_count:
        raise RuntimeError(
            f"{path.name}: committed count {len(expected)} != {expected_count}"
        )
    if len(set(expected)) != len(expected):
        raise RuntimeError(f"{path.name}: duplicate rows")
    if expected != actual:
        mismatch = next(
            (
                index
                for index, pair in enumerate(zip(expected, actual), start=1)
                if pair[0] != pair[1]
            ),
            min(len(expected), len(actual)) + 1,
        )
        raise RuntimeError(f"{path.name}: differs from git at row {mismatch}")


def main() -> int:
    try:
        verify_ledger(ROOT / "commits_shas.tsv", f"{SEAL}..{WALK_SNAPSHOT}", 561)
        verify_ledger(
            ROOT / "commits_origin_extra_shas.tsv",
            f"{SEAL}..{ORIGIN_SNAPSHOT}",
            565,
        )
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(
        "PASS: post-seal ledgers match fixed snapshots "
        f"{WALK_SNAPSHOT[:8]} (561) and {ORIGIN_SNAPSHOT[:8]} (565)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Read-only verification of the full-history snapshot ledgers.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
WALK_SNAPSHOT = "0e7814089db5ed387489acd9553a9105b0b69462"
ORIGIN_SNAPSHOT = "dfe649445403d7d0326594c918430ae5456b1f6b"
EXPECTED_ROOTS = {
    "5a5990d8bcfafae639e6efe474e8b5f73c9f2e50",
    "6fb1f66d7d04b3bf491ba7c997cf8be934616d71",
}


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
    actual = git_lines("log", "--reverse", "--format=%H%x09%ci", revision)
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
        verify_ledger(ROOT / "commits_shas.tsv", WALK_SNAPSHOT, 766)
        verify_ledger(
            ROOT / "commits_origin_main_shas.tsv", ORIGIN_SNAPSHOT, 770
        )
        roots = set(git_lines("rev-list", "--max-parents=0", WALK_SNAPSHOT))
        if roots != EXPECTED_ROOTS:
            raise RuntimeError(f"snapshot roots differ: {sorted(roots)}")
        merge_count = git_lines("rev-list", "--count", "--merges", WALK_SNAPSHOT)
        if merge_count != ["199"]:
            raise RuntimeError(f"snapshot merge count differs: {merge_count}")
        days = set(git_lines("log", "--format=%cs", WALK_SNAPSHOT))
        if len(days) != 30 or min(days) != "2026-08-11" or max(days) != "2026-09-13":
            raise RuntimeError("snapshot day census differs")
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(
        "PASS: full-history ledgers and census match fixed snapshots "
        f"{WALK_SNAPSHOT[:8]} (766) and {ORIGIN_SNAPSHOT[:8]} (770)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

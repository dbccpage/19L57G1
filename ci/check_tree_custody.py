"""Run every research tree's own custody verifier and pin the outcome.

Most research trees are outside the registered gate-11 set, so nothing runs
their pin verifiers and a failure there can sit on ``main`` unnoticed for
weeks.  That happened: eleven trees were red for months because their
verifiers demanded pinned sources be byte-identical at the snapshot AND at
HEAD, which no repin can satisfy once the author edits a sealed or contract
file.  The rule since 2026-09-22 is that a verifier fails on PROVENANCE at
its snapshot and merely REPORTS drift at HEAD.

This check does not decide whether a tree's verifier is right.  It is a
ratchet over the outcome set:

* a verifier that fails and is not pinned as an expected failure fails this
  check, naming the tree and the first line of its output;
* a verifier pinned as an expected failure that now passes also fails this
  check, so a repair cannot leave a stale pin behind.
* the pinned verifier names must match the discovered names, so removing a
  passing verifier cannot silently reduce the estate being checked.

Both directions matter.  Pinning only failures would let a fixed tree keep a
pin that hides the next regression.

Usage::

    python ci/check_tree_custody.py            # compare with the pin
    python ci/check_tree_custody.py --write    # rewrite the pin, deliberately
    python ci/check_tree_custody.py --json OUT # also write the raw outcomes

Regenerating the pin is a deliberate act, like the watchlist and module
censuses: never do it while an injection is live.

Run this on a CLEAN worktree.  Many of these verifiers refuse when anything
outside their own write root is modified or untracked, so an uncommitted
file of your own turns them red and would be captured as an expected
failure by --write.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PIN = REPO / "ci" / "tree_custody_pin.json"
VERIFIERS = ("verify_pins.py", "verify_sources.py", "verify_manifest.py", "source_manifest.py")
TIMEOUT = 300


def verifiers() -> list[tuple[str, str]]:
    """Every (tree, verifier file name), in a deterministic order."""
    found: list[tuple[str, str]] = []
    research = REPO / "research"
    for tree in sorted(p.name for p in research.iterdir() if p.is_dir()):
        if tree.startswith((".", "_")):
            continue
        for name in VERIFIERS:
            if (research / tree / name).is_file():
                found.append((tree, name))
    return found


def run_one(tree: str, name: str) -> tuple[int, str]:
    """Exit status and the most informative line, retried once on a git error.

    These verifiers shell out to git.  A concurrent commit or index lock in
    the same repository makes git fail transiently, which was observed as a
    spurious red for a tree that passed moments later.  A transient is
    retried once; a real failure fails twice.
    """
    code, line = _run_once(tree, name)
    if code != 0 and ("git " in line and "failed" in line):
        code, line = _run_once(tree, name)
    return code, line


def _run_once(tree: str, name: str) -> tuple[int, str]:
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    path = REPO / "research" / tree / name
    for args in ([], ["--check"]):
        try:
            done = subprocess.run(
                [sys.executable, "-B", str(path), *args],
                cwd=REPO, env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return 124, f"timed out after {TIMEOUT}s"
        out = (done.stdout + done.stderr).strip()
        if done.returncode == 2 and ("usage:" in out or "required" in out):
            continue  # this verifier wants an explicit mode; try --check
        lines = [line for line in out.splitlines() if line.strip()]
        first_fail = next((line for line in lines if line.startswith("FAIL")), "")
        last_error = next(
            (line for line in reversed(lines) if "Error" in line or "error" in line), ""
        )
        return done.returncode, (first_fail or last_error or (lines[-1] if lines else ""))
    return 2, "no runnable mode"


def measure() -> dict[str, dict[str, object]]:
    outcomes: dict[str, dict[str, object]] = {}
    for tree, name in verifiers():
        code, line = run_one(tree, name)
        outcomes[f"{tree}/{name}"] = {"exit": code, "line": line[:300]}
    return outcomes


def compare(outcomes: dict[str, dict[str, object]], pin: dict[str, object]) -> list[str]:
    expected = {str(k) for k in dict(pin.get("expected_failures", {})).keys()}  # type: ignore[arg-type]
    failing = {key for key, row in outcomes.items() if row["exit"] != 0}
    problems: list[str] = []
    names = pin.get("verifiers")
    if (not isinstance(names, list) or not names
            or any(not isinstance(name, str) or not name for name in names)
            or len(names) != len(set(names))):
        problems.append("INVALID PIN: verifiers must be a nonempty list of unique names")
    else:
        pinned_names = set(names)
        for key in sorted(pinned_names - outcomes.keys()):
            problems.append(f"MISSING VERIFIER: {key} is pinned but was not run")
        for key in sorted(outcomes.keys() - pinned_names):
            problems.append(f"NEW VERIFIER: {key} ran but is not pinned")
    for key in sorted(failing - expected):
        problems.append(f"NEW RED: {key} exits {outcomes[key]['exit']}: {outcomes[key]['line']}")
    for key in sorted(expected - failing):
        if key not in outcomes:
            problems.append(f"STALE PIN: {key} is pinned as failing but no longer exists")
        else:
            problems.append(f"STALE PIN: {key} now passes; remove it with --write")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite the pin deliberately")
    parser.add_argument("--json", type=Path, help="also write the raw outcomes here")
    args = parser.parse_args(argv)

    if args.write:
        status = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=False,
        )
        if status.returncode != 0:
            print(f"FAIL: cannot establish a clean worktree: {status.stderr.strip()}")
            return 1
        if status.stdout:
            print("FAIL: --write requires a clean worktree")
            return 1

    outcomes = measure()
    if args.json:
        args.json.write_bytes(
            (json.dumps(outcomes, indent=1, sort_keys=True) + "\n").encode("utf-8")
        )
    if args.write:
        pin = {
            "comment": (
                "Research trees whose own custody verifier fails on main. A tree here is "
                "NOT excused: it is recorded so a NEW failure is visible. Regenerate "
                "deliberately with ci/check_tree_custody.py --write."
            ),
            "expected_failures": {
                key: outcomes[key]["line"] for key in sorted(outcomes) if outcomes[key]["exit"] != 0
            },
            "verifiers": sorted(outcomes),
        }
        PIN.write_bytes((json.dumps(pin, indent=1, sort_keys=True) + "\n").encode("utf-8"))
        print(f"wrote {PIN.relative_to(REPO).as_posix()}: "
              f"{len(pin['expected_failures'])} expected failure(s) of {len(outcomes)} verifiers")
        return 0

    if not PIN.is_file():
        print(f"FAIL: {PIN.relative_to(REPO).as_posix()} is missing; write it with --write")
        return 1
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    problems = compare(outcomes, pin)
    for line in problems:
        print(f"FAIL: {line}")
    if problems:
        return 1
    red = sum(1 for row in outcomes.values() if row["exit"] != 0)
    print(
        f"tree custody census matches its pin: {len(outcomes)} verifiers, "
        f"{len(outcomes) - red} green, {red} pinned red"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

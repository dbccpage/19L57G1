"""Live injections for the closeout audit's admission-boundary repairs.

AuthorityEffect: None.  Apparatus, not a gate: ``verify.py`` never runs it.

For each repair of 2026-09-25 (B1 member, B2 node integrity, B3 binding),
this script reverts the repair in the real ``driver_a.py``, runs the named
adversarial tests of ``tests/test_admission_boundary.py`` through the real
public path, requires them to FAIL with the defect named in the failure
message, restores the original bytes, and requires the same tests to PASS.

It refuses to start unless ``driver_a.py`` matches ``HEAD``, restores the
file in a ``finally`` block, and regenerates no receipt.  Run it on a
clean worktree:  ``python inject_boundary.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "driver_a.py"
MODULE = "tests.test_admission_boundary"


@dataclass(frozen=True)
class Injection:
    name: str
    defect: str
    edits: tuple[tuple[str, str], ...]
    tests: tuple[str, ...]


INJECTIONS: tuple[Injection, ...] = (
    Injection(
        name="B1",
        defect="B1 REPRODUCED",
        edits=(
            (
                "    check_evidence(result, fresh, (key,))\n"
                "    delta = representative_delta(fresh, key)\n",
                "    delta = representative_delta(result, key)\n",
            ),
            ("    check_evidence(result, fresh, sealed_keys)\n", ""),
        ),
        tests=(
            "B1SubstitutedMember.test_b1_empty_member_under_an_authorized_key_is_refused",
            "B1SubstitutedMember.test_b1_other_class_member_under_an_authorized_key_is_refused",
            "B1SubstitutedMember.test_b1_explore_refuses_a_substituted_member",
            "B1SubstitutedMember.test_b1_other_forged_evidence_is_refused",
        ),
    ),
    Injection(
        name="H5-apply",
        defect="H5 REPRODUCED",
        edits=(
            (
                "    check_evidence(result, fresh, (key,))\n"
                "    delta = representative_delta(fresh, key)\n",
                "    delta = representative_delta(result, key)\n",
            ),
        ),
        tests=(
            "H5Dispositions.test_h5_apply_evidence_omitting_a_class_is_refused",
        ),
    ),
    Injection(
        name="B2",
        defect="B2 REPRODUCED",
        edits=(("    check_node_integrity(node)\n", ""),),
        tests=(
            "B2NodeIntegrity.test_b2_parent_whose_history_replays_elsewhere_is_refused",
            "B2NodeIntegrity.test_b2_explore_refuses_a_parent_that_does_not_replay",
        ),
    ),
    Injection(
        name="B3",
        defect="REPRODUCED",
        edits=(
            (
                "    check_license_binding(\n"
                "        license,\n"
                "        node,\n"
                "        target,\n"
                "        result.measure,\n"
                "        Bounds(max_items=result.max_items, max_arity=result.max_arity),\n"
                "    )\n"
                "    return evaluate(node.regime, license.target, license.measure, license.bounds)\n",
                "    return evaluate(\n"
                "        node.regime,\n"
                "        target,\n"
                "        result.measure,\n"
                "        Bounds(max_items=result.max_items, max_arity=result.max_arity),\n"
                "    )\n",
            ),
        ),
        tests=(
            "B3LicenseBinding.test_b3_license_at_a_relabelled_source_is_refused",
            "B3LicenseBinding.test_b3_license_at_same_regime_other_history_is_refused",
            "B3LicenseBinding.test_b3_license_for_another_target_is_refused",
            "B3LicenseBinding.test_b3_license_for_another_measure_is_refused",
            "B3LicenseBinding.test_b3_license_for_other_bounds_is_refused",
            "B3LicenseBinding.test_b3_explore_refuses_a_rebound_license",
            "H4UniquenessIsNotAuthorization.test_h4_unique_class_under_an_inapplicable_license_is_refused",
        ),
    ),
)


def _run_tests(tests: tuple[str, ...]) -> tuple[int, str]:
    command = [
        sys.executable,
        "-m",
        "unittest",
        *(f"{MODULE}.{name}" for name in tests),
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    return result.returncode, output


def _clean() -> bool:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--quiet", "HEAD", "--", TARGET.name],
        check=False,
    )
    return result.returncode == 0


def inject(original: str, injection: Injection) -> str:
    """The mutated source: every edit must match exactly once."""
    mutated = original
    for old, new in injection.edits:
        if mutated.count(old) != 1:
            raise ValueError(f"{injection.name}: edit site not found exactly once")
        mutated = mutated.replace(old, new)
    return mutated


def main() -> int:
    if not _clean():
        print("REFUSED: driver_a.py differs from HEAD; commit or restore it first")
        return 2
    raw = TARGET.read_bytes()
    original = raw.decode("utf-8").replace("\r\n", "\n")
    failures = 0
    for injection in INJECTIONS:
        mutated = inject(original, injection)
        try:
            TARGET.write_bytes(mutated.encode("utf-8"))
            code, output = _run_tests(injection.tests)
        finally:
            TARGET.write_bytes(raw)
        named = [
            line.strip().split(": the call returned", 1)[0]
            for line in output.splitlines()
            if line.startswith("AssertionError:") and injection.defect in line
        ]
        if code == 0 or not named:
            print(f"FAIL: {injection.name} injection did not fail naming the defect")
            failures += 1
        else:
            print(f"LIVE: {injection.name} injected, {len(named)} failure line(s):")
            for line in named:
                print(f"    {line}")
        if TARGET.read_bytes() != raw:
            print(f"FAIL: {injection.name} left driver_a.py modified")
            return 1
        code, output = _run_tests(injection.tests)
        if code != 0:
            print(f"FAIL: {injection.name} tests do not pass after restoring\n{output}")
            failures += 1
        else:
            print(f"RECOVERED: {injection.name} reversed; {len(injection.tests)} test(s) pass")
    if not _clean():
        print("FAIL: driver_a.py differs from HEAD after the run")
        return 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

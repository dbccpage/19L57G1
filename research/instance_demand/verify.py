"""Replay Stages 1 through 4, pin sources, and audit compiled theorem evidence.

The receipt keeps OB-1 OPEN. It does not identify event occurrence with supply.
AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
BASE = "6bc3cded8d6dc329a4d9618261406a54d294cfb1"
SOURCE_PATHS = (
    "code/derivation/__init__.py", "code/derivation/model.py", "code/derivation/observe.py",
    "lean4/Derivation/Basic.lean", "lean4/Derivation/Inertia.lean",
    "lean4/lakefile.toml", "lean4/lean-toolchain",
    "research/endogenous_demand/CLAIMS.md", "research/endogenous_demand/reader.py",
    "research/represented_execution/lean/Execution.lean",
)
STAGE3_SOURCE_PATHS = (
    "lean4/Derivation/Attachment.lean", "lean4/Derivation/Bridge.lean",
    "lean4/Derivation/CapacityBound.lean", "lean4/Derivation/Erasure.lean",
    "lean4/Derivation/Generator.lean", "lean4/Derivation/HigherStructure.lean",
    "lean4/Derivation/Pigeonhole.lean", "lean4/Derivation/PrimDiff.lean",
    "lean4/Derivation/PrimitiveCore.lean", "lean4/Derivation/PrimitivePassage.lean",
    "lean4/Derivation/Refusal.lean", "lean4/Derivation/RefusalFrontier.lean",
    "lean4/Derivation/SeparationCapacity.lean",
    "research/ignition/lean/lakefile.toml", "research/ignition/lean/lean-toolchain",
    "research/local_reuse/lean/lakefile.toml", "research/local_reuse/lean/lean-toolchain",
    "research/magnification/lean/lakefile.toml", "research/magnification/lean/lean-toolchain",
    "research/represented_execution/lean/lakefile.toml", "research/represented_execution/lean/lean-toolchain",
    "research/setting_translation/lean/Chains.lean", "research/setting_translation/lean/Translation.lean",
    "research/setting_translation/lean/lakefile.toml", "research/setting_translation/lean/lean-toolchain",
)
ALLOWED = {"propext", "Quot.sound"}
FORBIDDEN = re.compile(r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE)
CENSUS = re.compile(r"^INSTANCE_DEMAND_THEOREM: (\S+)$", re.MULTILINE)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=REPO, stderr=subprocess.PIPE)


def validate_manifest(payload: Any, expected: tuple[str, ...] = SOURCE_PATHS) -> dict[str, str]:
    if not isinstance(payload, dict) or payload.get("base") != BASE:
        raise ValueError("SOURCE_BASE")
    sources = payload.get("sources")
    if not isinstance(sources, dict) or set(sources) != set(expected):
        raise ValueError("SOURCE_POPULATION")
    if not all(isinstance(v, str) and re.fullmatch(r"[a-f0-9]{64}", v) for v in sources.values()):
        raise ValueError("SOURCE_DIGEST_SHAPE")
    return {str(k): str(v) for k, v in sources.items()}


def check_sources() -> None:
    sources = validate_manifest(json.loads((ROOT / "SOURCE_MANIFEST.json").read_text()))
    sources.update(validate_manifest(json.loads((ROOT / "STAGE3_SOURCE_MANIFEST.json").read_text()),
                                     STAGE3_SOURCE_PATHS))
    git("merge-base", "--is-ancestor", BASE, "HEAD")
    for name, digest in sources.items():
        pinned = git("show", f"{BASE}:{name}")
        if sha(pinned) != digest or git("show", f"HEAD:{name}") != pinned:
            raise ValueError("SOURCE_CHANGED: " + name)
        if (REPO / name).read_bytes().replace(b"\r\n", b"\n") != pinned:
            raise ValueError("SOURCE_WORKTREE_CHANGED: " + name)
    sys.path.insert(0, str(REPO / "code"))
    for name, relative in (("derivation", "__init__.py"), ("derivation.model", "model.py"),
                           ("derivation.observe", "observe.py")):
        module = importlib.import_module(name)
        if Path(module.__file__ or "").resolve() != (REPO / "code/derivation" / relative).resolve():
            raise ValueError("IMPORT_ORIGIN: " + name)


def parse_reports(log: str, inventory: str) -> dict[str, list[str]]:
    names = CENSUS.findall(inventory)
    if not names or len(names) != len(set(names)):
        raise ValueError("THEOREM_CENSUS_EMPTY_OR_DUPLICATE")
    reports: dict[str, list[str]] = {}
    pattern = r"^'(.+?)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)$"
    for match in re.finditer(pattern, log, re.MULTILINE):
        name = match[1]
        if name in reports:
            raise ValueError("DUPLICATE_REPORT: " + name)
        used = sorted(word.strip() for word in (match[2] or "").split(",") if word.strip())
        if not set(used) <= ALLOWED:
            raise ValueError("AXIOM_RELIANCE: " + name)
        reports[name] = used
    if set(names) != set(reports):
        raise ValueError("THEOREM_REPORT_CENSUS_MISMATCH")
    return dict(sorted(reports.items()))


def command(argv: list[str], cwd: Path = ROOT) -> str:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO / "code")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True,
                            encoding="utf-8", check=False, timeout=300)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def coverage_file_path(name: str) -> Path:
    """Resolve a coverage.json path against this package, not process cwd."""
    path = Path(name)
    if path.is_absolute():
        return path.resolve()
    return (ROOT / path.name).resolve()


def check_coverage(payload: Any) -> tuple[float, float]:
    files = payload["files"]
    if {coverage_file_path(name) for name in files} != {
            (ROOT / "probe.py").resolve(), (ROOT / "materialize.py").resolve(),
            (ROOT / "emitter.py").resolve(), (ROOT / "dynamics.py").resolve()}:
        raise ValueError("COVERAGE_POPULATION")
    for name, measured in files.items():
        summary = measured["summary"]
        for numerator, denominator in (("covered_lines", "num_statements"),
                                       ("covered_branches", "num_branches")):
            if summary[denominator] and 100 * summary[numerator] / summary[denominator] < 95:
                raise ValueError("COVERAGE_FILE: " + name)
    totals = payload["totals"]
    lines = 100 * totals["covered_lines"] / totals["num_statements"]
    branches = 100 * totals["covered_branches"] / totals["num_branches"]
    if lines < 95 or branches < 95:
        raise ValueError(f"COVERAGE: {lines:.2f} statements, {branches:.2f} branches")
    return float(lines), float(branches)


def input_hashes() -> dict[str, str]:
    paths = [*ROOT.glob("*.py"), *ROOT.glob("*.md"), *ROOT.glob("*.toml"),
             *ROOT.glob("tests/*.py"), *ROOT.glob("lean/*.lean"), ROOT / "lean/lakefile.toml",
             ROOT / "lean/lean-toolchain", ROOT / "SOURCE_MANIFEST.json",
             ROOT / "STAGE3_SOURCE_MANIFEST.json",
             ROOT / ".gitattributes", ROOT / ".gitignore"]
    return {p.relative_to(ROOT).as_posix(): sha(p.read_bytes().replace(b"\r\n", b"\n"))
            for p in sorted(paths)}


def verify(lake: str, write: bool) -> None:
    check_sources()
    before = input_hashes()
    lean_files = {p.name for p in (ROOT / "lean").glob("*.lean")}
    if lean_files != {"InstanceDemand.lean", "ClosureMaterialization.lean", "RepresentedEmitter.lean",
                      "EmissionDynamics.lean", "NoGo.lean", "Inventory.lean"}:
        raise ValueError("LEAN_FILE_CENSUS")
    for name in lean_files:
        text = (ROOT / "lean" / name).read_text(encoding="utf-8")
        if FORBIDDEN.search(text) or re.search(r"\bmathlib\b", text, re.IGNORECASE):
            raise ValueError("LEAN_SOURCE_TOKEN: " + name)
    test_log = command([sys.executable, "-m", "coverage", "run", "-m", "unittest",
                        "discover", "-s", "tests", "-p", "test_*.py"])
    count = re.search(r"Ran (\d+) tests in", test_log)
    if count is None or int(count[1]) == 0:
        raise ValueError("EMPTY_TEST_CENSUS")
    command([sys.executable, "-m", "coverage", "json", "-o", "coverage.json", "-q"])
    line, branch = check_coverage(json.loads((ROOT / "coverage.json").read_text()))
    python_files = [str(p) for p in sorted(ROOT.glob("*.py"))] + [str(p) for p in sorted(ROOT.glob("tests/*.py"))]
    command([sys.executable, "-m", "mypy", *python_files])
    version = command([lake, "env", "lean", "--version"], ROOT / "lean")
    if not version.startswith("Lean (version 4.33.0,"):
        raise ValueError("LEAN_VERSION")
    command([lake, "build"], ROOT / "lean")
    proof_log = command([lake, "env", "lean", "InstanceDemand.lean"], ROOT / "lean")
    proof_log += command([lake, "env", "lean", "ClosureMaterialization.lean"], ROOT / "lean")
    proof_log += command([lake, "env", "lean", "RepresentedEmitter.lean"], ROOT / "lean")
    proof_log += command([lake, "env", "lean", "EmissionDynamics.lean"], ROOT / "lean")
    proof_log += command([lake, "env", "lean", "NoGo.lean"], ROOT / "lean")
    inventory_log = command([lake, "env", "lean", "Inventory.lean"], ROOT / "lean")
    reports = parse_reports(proof_log + inventory_log, inventory_log)
    import probe
    import materialize
    import emitter
    import dynamics
    computation = probe.report()
    closure = materialize.report()
    emission = emitter.report()
    repeated = dynamics.report()
    check_sources()
    if input_hashes() != before:
        raise ValueError("INPUTS_CHANGED_DURING_VERIFICATION")
    records = {"computation.json": computation,
               "materialization.json": closure,
               "emitter.json": emission,
               "dynamics.json": repeated,
               "lean.json": {"stage": 4, "outcome": "OPEN", "reports": reports,
                             "theorem_count_including_generated": len(reports)},
               "verification.json": {"stage": 4, "outcome": "OPEN", "base": BASE,
                    "python_tests": int(count[1]), "python_version": sys.version.split()[0],
                    "statement_coverage": line, "branch_coverage": branch,
                    "coverage_scope": "probe.py, materialize.py, emitter.py, dynamics.py; verifier apparatus excluded",
                    "sources": before, "lean_theorems_including_generated": len(reports)}}
    for name, record in records.items():
        raw = (json.dumps(record, sort_keys=True, indent=2) + "\n").encode("utf-8")
        path = ROOT / "evidence" / name
        if write:
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(raw)
        elif not path.is_file() or path.read_bytes() != raw:
            raise ValueError("EVIDENCE_DIFFERS: " + name)
    print(f"PASS Stages 1-4: {count[1]} tests; {line:.2f}% statements, {branch:.2f}% branches; "
          f"{len(reports)} theorem reports. OB-1 remains OPEN outside InClass and I1Class.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--lake", default=shutil.which("lake"))
    args = parser.parse_args()
    if not args.lake:
        raise ValueError("LAKE_NOT_FOUND: use --lake PATH")
    verify(str(args.lake), bool(args.write))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

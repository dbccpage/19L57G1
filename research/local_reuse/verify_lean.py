"""Compile every local proof and compare its reports to an environment census.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
LEAN = ROOT / "lean"
RECORD = ROOT / "evidence" / "lean.json"
EXPECTED_FILES = {"LocalReuse.lean", "Inventory.lean"}
ALLOWED_AXIOMS = {"propext", "Quot.sound"}


def parse_reports(log: str, inventory_log: str) -> dict[str, list[str]]:
    inventory = re.findall(r"^LOCAL_REUSE_THEOREM: (\S+)$", inventory_log, re.MULTILINE)
    if not inventory or len(set(inventory)) != len(inventory):
        raise ValueError("empty or duplicate environment theorem census")
    reports: dict[str, list[str]] = {}
    for line in log.splitlines():
        used = re.fullmatch(r"'(.+?)' depends on axioms: \[(.*?)\]", line)
        none = re.fullmatch(r"'(.+?)' does not depend on any axioms", line)
        if not used and not none:
            continue
        match = used or none
        if match is None:
            raise ValueError("report parser invariant")
        name = match.group(1)
        if name in reports:
            raise ValueError(f"duplicate report: {name}")
        axioms = sorted(item.strip() for item in used.group(2).split(",") if item.strip()) if used else []
        if not set(axioms) <= ALLOWED_AXIOMS:
            raise ValueError(f"disallowed reliance: {name}: {axioms}")
        reports[name] = axioms
    if set(reports) != set(inventory):
        raise ValueError(f"report/census mismatch: missing={sorted(set(inventory) - set(reports))}, "
                         f"extra={sorted(set(reports) - set(inventory))}")
    return dict(sorted(reports.items()))


def source_hashes() -> dict[str, str]:
    actual = {p.relative_to(LEAN).as_posix() for p in LEAN.rglob("*.lean")
              if ".lake" not in p.relative_to(LEAN).parts}
    if actual != EXPECTED_FILES:
        raise ValueError(f"local Lean file census changed: {sorted(actual)}")
    result = {}
    forbidden = re.compile(r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE)
    for name in sorted(EXPECTED_FILES | {"lakefile.toml", "lean-toolchain"}):
        raw = (LEAN / name).read_bytes().replace(b"\r\n", b"\n")
        if name.endswith(".lean") and forbidden.search(raw.decode("utf-8")):
            raise ValueError(f"forbidden source token: {name}")
        result[name] = hashlib.sha256(raw).hexdigest()
    return result


def invoke(*args: str) -> str:
    result = subprocess.run(["lake", *args], cwd=LEAN, capture_output=True, text=True,
                            encoding="utf-8", timeout=240, check=False)
    output = result.stdout + result.stderr
    if result.returncode:
        raise RuntimeError(f"lake {' '.join(args)} failed ({result.returncode}):\n{output}")
    return output


def verify() -> bytes:
    errors = verify_sources()
    if errors:
        raise ValueError("source verification: " + "; ".join(errors))
    before = source_hashes()
    version = invoke("env", "lean", "--version").strip()
    if not version.startswith("Lean (version 4.33.0,"):
        raise ValueError(f"unexpected Lean version: {version}")
    invoke("build", "LocalReuse", "Inventory")
    log = invoke("env", "lean", "LocalReuse.lean")
    census = invoke("env", "lean", "Inventory.lean")
    reports = parse_reports(log + "\n" + census, census)
    if source_hashes() != before:
        raise ValueError("local proof sources changed while compiling")
    errors = verify_sources()
    if errors:
        raise ValueError("source verification after build: " + "; ".join(errors))
    payload = {"schema_version": 1, "classification": "Lean proof compilation",
               "authority_effect": "None", "toolchain": "leanprover/lean4:v4.33.0",
               "local_sources_sha256": before, "theorem_count_including_generated": len(reports),
               "reports": reports, "census": "compiled environment theorem declarations in LocalReuse",
               "scope": "the exact theorem statements and their explicit hypotheses",
               "python_driver_refinement": "NOT_PROVED"}
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        fresh = verify()
        if args.write:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(fresh)
            print("WROTE: freshly compiled theorem and reliance record")
        elif not RECORD.is_file() or RECORD.read_bytes() != fresh:
            print("FAIL: evidence/lean.json differs from fresh compilation")
            return 1
        else:
            # "theorem census over the LocalReuse namespace", not "complete":
            # the reach is theorems only, and a definition carrying a
            # disallowed axiom that no theorem reaches goes unreported.
            print("PASS: fresh Lean build, theorem census over the LocalReuse "
                  "namespace, reliance and source records")
        return 0
    except (ValueError, TypeError, KeyError, OSError, RuntimeError,
            subprocess.SubprocessError) as exc:
        # Every refusal this module raises by name reaches the operator as a
        # named FAIL line, matching run.py and verify_sources.py. A build that
        # exceeds the timeout arrives here too, as SubprocessError.
        print("FAIL: " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

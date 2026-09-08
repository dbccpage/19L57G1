"""Compile the reachability proofs and compare their reports to the source census.

AuthorityEffect: None.

Every theorem the source exports carries a ``#print axioms`` line; the
compiled report set must equal that census in both directions, every report
must lie within the whitelist, and the local sources must not change while
compiling.  The record ``evidence/lean.json`` is byte-compared in check mode.
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
EXPECTED_FILES = {"Reachable.lean"}
ALLOWED_AXIOMS = {"propext", "Quot.sound"}
PRINT_LINE = re.compile(r"^#print axioms (\S+)\s*$", re.MULTILINE)


def source_census(text: str) -> list[str]:
    """The theorem names the source itself asks a report for, in order."""
    names = PRINT_LINE.findall(text)
    if not names or len(set(names)) != len(names):
        raise ValueError("empty or duplicate #print axioms census in the source")
    return names


def parse_reports(log: str, census: list[str]) -> dict[str, list[str]]:
    """Reports keyed by name; fails on a duplicate, a disallowed reliance, or
    any mismatch between the report set and the census."""
    reports: dict[str, list[str]] = {}
    for line in log.splitlines():
        used = re.fullmatch(r"'(.+?)' depends on axioms: \[(.*?)\]", line)
        none = re.fullmatch(r"'(.+?)' does not depend on any axioms", line)
        match = used or none
        if match is None:
            continue
        name = match.group(1)
        if name in reports:
            raise ValueError(f"duplicate report: {name}")
        axioms = sorted(item.strip() for item in used.group(2).split(",") if item.strip()) if used else []
        if not set(axioms) <= ALLOWED_AXIOMS:
            raise ValueError(f"disallowed reliance: {name}: {axioms}")
        reports[name] = axioms
    if set(reports) != set(census):
        raise ValueError(f"report/census mismatch: missing={sorted(set(census) - set(reports))}, "
                         f"extra={sorted(set(reports) - set(census))}")
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
                            encoding="utf-8", timeout=600, check=False)
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
    invoke("build", "Reachable")
    log = invoke("env", "lean", "Reachable.lean")
    census = source_census((LEAN / "Reachable.lean").read_text(encoding="utf-8"))
    reports = parse_reports(log, census)
    if source_hashes() != before:
        raise ValueError("local proof sources changed while compiling")
    errors = verify_sources()
    if errors:
        raise ValueError("source verification after build: " + "; ".join(errors))
    payload = {"schema_version": 1, "classification": "Lean proof compilation",
               "authority_effect": "None", "toolchain": "leanprover/lean4:v4.33.0",
               "local_sources_sha256": before, "theorem_count": len(reports),
               "reports": reports,
               "census": "the #print axioms lines of lean/Reachable.lean, compared in both directions",
               "scope": "the exact theorem statements and their explicit hypotheses",
               "python_engine_refinement": "NOT_PROVED; checked edge by edge by census.py"}
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
            print("PASS: fresh Lean build, report census equal to the source in both "
                  "directions, reliance within the whitelist, sources unchanged")
        return 0
    except (ValueError, TypeError, KeyError, OSError, RuntimeError,
            subprocess.SubprocessError) as exc:
        print("FAIL: " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

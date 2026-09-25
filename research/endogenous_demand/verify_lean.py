"""Compile the local proofs and compare their reports to an environment census.

AuthorityEffect: None.

The census (`lean/Inventory.lean`) enumerates every compiled theorem of the
tree's two proof modules, `EndogenousDemand` and
`EndogenousDemandObstruction`, from the environment, independently of source
layout; the reports come from each module's own `#print axioms` lines plus
the generated-declaration lines in `Inventory.lean`.  The two populations must
coincide, every report must lie within the repository's permitted axioms, and
the sources must carry no forbidden token.

A third population is read from the source text: every `theorem` written in
a `.lean` file of `lean/`, with its namespace.  Each must have a report.  This
is the count of written declarations, not of compiler-generated names, and it
does not depend on the census's module filter being right.

(2026-09-24: until this date the census enumerated only the
`EndogenousDemand` namespace and this script never read the reports of
`EndogenousDemandObstruction.lean`, so its seventeen written theorems, the
termination bound among them, were outside the recorded audit.)
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
EXPECTED_FILES = {
    "EndogenousDemand.lean",
    "Inventory.lean",
    "EndogenousDemandObstruction.lean",
}
ALLOWED_AXIOMS = {"propext", "Quot.sound"}
REPORTING_MODULES = ("EndogenousDemand.lean", "EndogenousDemandObstruction.lean")
CENSUS_LINE = re.compile(r"^ENDOGENOUS_DEMAND_THEOREM: (\S+)$", re.MULTILINE)
WRITTEN_THEOREM = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|nonrec)\s+)*"
    r"theorem\s+([^\s(:{\[]+)")
SCOPE_OPEN = re.compile(r"^(namespace|section)(?:\s+(\S+))?$")
SCOPE_CLOSE = re.compile(r"^end(?:\s+(\S+))?$")
FORBIDDEN = re.compile(r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE)
MATHLIB = re.compile(r"\bmathlib\b", re.IGNORECASE)


def parse_reports(log: str, inventory_log: str) -> dict[str, list[str]]:
    inventory = CENSUS_LINE.findall(inventory_log)
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


def strip_comments(text: str) -> str:
    """Blank out Lean comments (nested block comments and line comments),
    keeping line structure, so a commented-out declaration is not counted."""
    out: list[str] = []
    index = 0
    depth = 0
    while index < len(text):
        if text.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and text.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            out.append("\n" if text[index] == "\n" else " ")
            index += 1
        elif text.startswith("--", index):
            end = text.find("\n", index)
            index = len(text) if end < 0 else end
        else:
            out.append(text[index])
            index += 1
    if depth:
        raise ValueError("unterminated block comment")
    return "".join(out)


def written_theorems(text: str) -> list[str]:
    """Fully qualified names of the theorems written in one Lean source."""
    scopes: list[list[str]] = []
    names: list[str] = []
    for line in strip_comments(text).splitlines():
        stripped = line.strip()
        opened = SCOPE_OPEN.match(stripped)
        if opened:
            label = opened.group(2)
            scopes.append(label.split(".") if opened.group(1) == "namespace" and label else [])
            continue
        if SCOPE_CLOSE.match(stripped):
            if not scopes:
                raise ValueError("unmatched end")
            scopes.pop()
            continue
        declared = WRITTEN_THEOREM.match(line)
        if declared:
            name = declared.group(1)
            if name.startswith("_root_."):
                names.append(name.removeprefix("_root_."))
            else:
                names.append(".".join([part for parts in scopes for part in parts] + [name]))
    if len(set(names)) != len(names):
        raise ValueError("duplicate written theorem")
    return names


def written_census() -> list[str]:
    """Every theorem written in the tree's Lean sources."""
    names: list[str] = []
    for name in sorted(EXPECTED_FILES):
        names.extend(written_theorems((LEAN / name).read_bytes().decode("utf-8")))
    if not names:
        raise ValueError("empty written theorem census")
    return sorted(names)


def check_written(written: list[str], reports: dict[str, list[str]]) -> None:
    missing = sorted(set(written) - set(reports))
    if missing:
        raise ValueError(f"written theorem without axiom report: {missing}")


def source_hashes() -> dict[str, str]:
    actual = {p.relative_to(LEAN).as_posix() for p in LEAN.rglob("*.lean")
              if ".lake" not in p.relative_to(LEAN).parts}
    if actual != EXPECTED_FILES:
        raise ValueError(f"local Lean file census changed: {sorted(actual)}")
    result = {}
    for name in sorted(EXPECTED_FILES | {"lakefile.toml", "lean-toolchain"}):
        raw = (LEAN / name).read_bytes().replace(b"\r\n", b"\n")
        text = raw.decode("utf-8")
        if name.endswith(".lean") and FORBIDDEN.search(text):
            raise ValueError(f"forbidden source token: {name}")
        if MATHLIB.search(text):
            raise ValueError(f"mathlib import: {name}")
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
    invoke("build", "EndogenousDemand", "Inventory", "EndogenousDemandObstruction")
    log = "\n".join(invoke("env", "lean", name) for name in REPORTING_MODULES)
    census = invoke("env", "lean", "Inventory.lean")
    reports = parse_reports(log + "\n" + census, census)
    written = written_census()
    check_written(written, reports)
    if source_hashes() != before:
        raise ValueError("local proof sources changed while compiling")
    errors = verify_sources()
    if errors:
        raise ValueError("source verification after build: " + "; ".join(errors))
    axiom_free = sum(1 for axioms in reports.values() if not axioms)
    payload = {"schema_version": 1, "classification": "Lean proof compilation",
               "authority_effect": "None", "toolchain": "leanprover/lean4:v4.33.0",
               "local_sources_sha256": before,
               "theorem_count_including_generated": len(reports),
               "written_theorem_count": len(written),
               "axiom_free_count": axiom_free,
               "reports": reports,
               "census": "compiled environment theorem declarations of the EndogenousDemand "
                         "and EndogenousDemandObstruction modules",
               "outcome": "B",
               "class": "C_reqs",
               "scope": "E2 on the sealed reqs channel is unsatisfiable; "
                        "the instance channel is not formalized here and remains OPEN",
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
            print("PASS: fresh Lean build, theorem census over both proof modules, "
                  "every written theorem reported, reliance and source records")
        return 0
    except (ValueError, TypeError, KeyError, OSError, RuntimeError,
            subprocess.SubprocessError) as exc:
        print("FAIL: " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

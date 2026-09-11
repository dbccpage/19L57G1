"""Compile the local harness proofs and compare reports to an environment census.

AuthorityEffect: None.

The census (`lean/Inventory.lean`) enumerates every compiled theorem of the
`Harness` namespace from the environment, independently of source layout; the
reports come from `lean/Harness.lean`'s `#print axioms` lines plus generated-
declaration lines in `Inventory.lean`.  The two populations must coincide,
every report must lie within the repository's permitted axioms, and the
sources must carry no forbidden token.  This gate does not claim proved
equivalence to `code/derivation/`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from verify_sources import PACKET, verify_sources

if PACKET != Path("research/alpha_engine"):
    raise RuntimeError(f"wrong custody guard imported: {PACKET}")

ROOT = Path(__file__).resolve().parent
LEAN = ROOT / "lean"
RECORD = ROOT / "evidence" / "lean.json"
EXPECTED_FILES = {"Harness.lean", "Inventory.lean"}
ALLOWED_AXIOMS = {"propext", "Quot.sound"}
CENSUS_LINE = re.compile(r"HARNESS_THEOREM: (\S+)")
AXIOM_USED = re.compile(r"'(.+?)' depends on axioms: \[(.*?)\]")
AXIOM_NONE = re.compile(r"'(.+?)' does not depend on any axioms")
FORBIDDEN = re.compile(r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE)
MATHLIB = re.compile(r"\bmathlib\b", re.IGNORECASE)


def parse_reports(log: str, inventory_log: str) -> dict[str, list[str]]:
    inventory = CENSUS_LINE.findall(inventory_log)
    if not inventory or len(set(inventory)) != len(inventory):
        raise ValueError("empty or duplicate environment theorem census")
    reports: dict[str, list[str]] = {}
    for line in log.splitlines():
        used = AXIOM_USED.search(line)
        none = AXIOM_NONE.search(line)
        if not used and not none:
            continue
        match = used or none
        if match is None:
            raise ValueError("report parser invariant")
        name = match.group(1)
        if not name.startswith("Harness."):
            continue
        if name in reports:
            raise ValueError(f"duplicate report: {name}")
        axioms = (
            sorted(item.strip() for item in used.group(2).split(",") if item.strip())
            if used else []
        )
        if not set(axioms) <= ALLOWED_AXIOMS:
            raise ValueError(f"disallowed reliance: {name}: {axioms}")
        reports[name] = axioms
    if set(reports) != set(inventory):
        raise ValueError(
            "report/census mismatch: "
            f"missing={sorted(set(inventory) - set(reports))}, "
            f"extra={sorted(set(reports) - set(inventory))}"
        )
    return dict(sorted(reports.items()))


def source_hashes() -> dict[str, str]:
    actual = {
        p.relative_to(LEAN).as_posix()
        for p in LEAN.rglob("*.lean")
        if ".lake" not in p.relative_to(LEAN).parts
    }
    if actual != EXPECTED_FILES:
        raise ValueError(f"local Lean file census changed: {sorted(actual)}")
    result: dict[str, str] = {}
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
    result = subprocess.run(
        ["lake", *args],
        cwd=LEAN,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=600,
        check=False,
    )
    output = result.stdout + result.stderr
    if result.returncode:
        raise RuntimeError(
            f"lake {' '.join(args)} failed ({result.returncode}):\n{output}"
        )
    return output


def verify() -> bytes:
    errors = verify_sources()
    if errors:
        raise ValueError("source verification: " + "; ".join(errors))
    before = source_hashes()
    version = invoke("env", "lean", "--version").strip()
    if not version.startswith("Lean (version 4.33.0,"):
        raise ValueError(f"unexpected Lean version: {version}")
    invoke("build", "Harness", "Inventory")
    log = invoke("env", "lean", "Harness.lean")
    census = invoke("env", "lean", "Inventory.lean")
    reports = parse_reports(log + "\n" + census, census)
    if source_hashes() != before:
        raise ValueError("local proof sources changed while compiling")
    errors = verify_sources()
    if errors:
        raise ValueError("source verification after build: " + "; ".join(errors))
    axiom_free = sum(1 for axioms in reports.values() if not axioms)
    payload = {
        "schema_version": 1,
        "classification": "Lean proof compilation",
        "authority_effect": "None",
        "toolchain": "leanprover/lean4:v4.33.0",
        "local_sources_sha256": before,
        "theorem_count_including_generated": len(reports),
        "axiom_free_count": axiom_free,
        "reports": reports,
        "census": "compiled environment theorem declarations in the Harness namespace",
        "scope": (
            "local harness: License is not Event; SearchPolicy output is a "
            "subset of retained keys; uniqueness does not apply; evaluation "
            "does not admit. Not a sealed object-language theorem and not a "
            "proved equivalence to code/derivation"
        ),
        "python_driver_refinement": "NOT_PROVED",
        "receipt_is_not_proof": True,
    }
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
            print(
                "PASS: fresh Lean build, theorem census over the Harness "
                "namespace, reliance and source records"
            )
        return 0
    except (
        ValueError,
        TypeError,
        KeyError,
        OSError,
        RuntimeError,
        subprocess.SubprocessError,
    ) as exc:
        print("FAIL: " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

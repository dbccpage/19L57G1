"""Replay the Lean axiom inventory for research/twin_pricing.

AuthorityEffect: None.
Hashes are CRLF-normalized so a Windows checkout matches the committed LF blobs.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess

THEOREMS = (
    "TwinRelation.twins_differ_at_scale",
    "TwinRelation.twins_are_distinct",
    "TwinRelation.scale_one_twins_differ",
    "TwinRelation.twins_are_related",
    "TwinRelation.twin_pair_distinct_and_related",
    "QuotientTopology.twin_collapse_in_quotient",
    "QuotientTopology.separation_quotient_contrast",
    "QuotientTopology.adjacent_cylinders_glue",
    "QuotientTopology.quotient_destroys_clopen_separation",
    "QuotientTopology.locally_constant_chain",
    "QuotientTopology.twin_collapse_predicate_transport",
    "QuotientTopology.quotient_points_distinct_iff",
    "QuotientTopology.distinct_quotient_points_representatives_non_equivalent",
    "QuotientTopology.scale_one_valuation_difference",
    "QuotientTopology.dyadic_valuation_difference_at_depth",
    "QuotientTopology.dyadic_valuation_integer_difference",
    "ValuationPricing.twinCount_base2",
    "ValuationPricing.twinCount_strictly_positive",
    "ValuationPricing.mu1Scale_base2",
    "ValuationPricing.cumulative_mu1_formula",
    "ValuationPricing.mu2Scale_base2",
    "ValuationPricing.cumulative_mu2_formula",
    "ValuationPricing.mu1_strictly_divergent",
    "ValuationPricing.cumulative_mu1_unbounded",
    "ValuationPricing.mu2_strictly_divergent",
    "ValuationPricing.cumulative_mu2_unbounded",
    "ValuationPricing.markov_weighted_scale_identity",
    "ValuationPricing.markov_obstruction_diverges",
    "ValuationPricing.markov_obstruction_unbounded",
    "ValuationPricing.finite_stage_price_finite",
    "ValuationPricing.continuum_price_infinite",
)

ALLOWED_AXIOMS = frozenset({"propext", "Quot.sound"})
FORBIDDEN = re.compile(
    r"\b(sorry|admit|unsafe|partial|noncomputable)\b|^\s*axiom\s|\bClassical\.",
    re.MULTILINE,
)
NO_AXIOMS = re.compile(r"'([^']+)' does not depend on any axioms")
HAS_AXIOMS = re.compile(r"'([^']+)' depends on axioms: \[([^\]]*)\]")


def tree_root() -> Path:
    return Path(__file__).resolve().parent


def lake() -> str:
    located = shutil.which("lake")
    if located is None:
        fallback = Path.home() / ".elan" / "bin" / "lake.exe"
        if not fallback.exists():
            raise ValueError("lake executable is unavailable")
        return str(fallback)
    return located


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command, cwd=cwd, check=False, capture_output=True, text=True
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        raise ValueError(
            f"command failed with {completed.returncode}: {' '.join(command)}\n{output}"
        )
    return output


def source_hashes(lean_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(lean_root.rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        text = raw.decode("utf-8")
        match = FORBIDDEN.search(text)
        if match is not None:
            raise ValueError(f"forbidden Lean token in {path.name}: {match.group(0)}")
        result[path.relative_to(lean_root).as_posix()] = sha256(raw).hexdigest()
    return result


def parse_axioms(output: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for name in NO_AXIOMS.findall(output):
        result[name] = []
    for name, values in HAS_AXIOMS.findall(output):
        result[name] = sorted(value.strip() for value in values.split(",") if value.strip())
    if set(result) != set(THEOREMS):
        raise ValueError(
            f"axiom report population differs: missing={sorted(set(THEOREMS) - set(result))} "
            f"extra={sorted(set(result) - set(THEOREMS))}"
        )
    disallowed = sorted(
        {axiom for values in result.values() for axiom in values} - ALLOWED_AXIOMS
    )
    if disallowed:
        raise ValueError(f"disallowed axioms: {disallowed}")
    return result


def render() -> tuple[bytes, bytes]:
    root = tree_root()
    lean_root = root / "lean"
    lake_exe = lake()
    # Clean and build to capture inventory replay output
    run([lake_exe, "clean"], lean_root)
    output = run([lake_exe, "build"], lean_root)
    axioms = parse_axioms(output)
    text = (
        "\n".join(f"{name}: {','.join(axioms[name]) or 'none'}" for name in THEOREMS)
        + "\n"
    ).encode("utf-8")
    payload = {
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "authority_effect": None,
        "axiom_inventory": axioms,
        "source_hashes": source_hashes(lean_root),
        "terminal": "ENUMERATIVE_TWIN_PRICE_DIVERGENT",
    }
    return text, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text, payload = render()
    receipt_root = tree_root() / "receipts"
    receipt_root.mkdir(parents=True, exist_ok=True)
    paths = {
        receipt_root / "lean_axioms.txt": text,
        receipt_root / "lean.json": payload,
    }
    if args.write:
        for path, value in paths.items():
            path.write_bytes(value)
    for path, value in paths.items():
        if not path.exists() or path.read_bytes() != value:
            raise ValueError(f"Lean receipt differs: {path.name}")
    print(f"Lean receipt replay clean: {len(THEOREMS)} theorem reports")


if __name__ == "__main__":
    main()

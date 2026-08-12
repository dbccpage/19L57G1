"""Produce the ultra-closure artifacts deterministically.

Usage: python code/run_completion.py [--artifacts DIR]

Writes:
  completion_dependency_graph.json  inventory + classified bridges
  completion_countermodels.json     failed bridges + run separations
  completion_protocols.json         G0-G2 event-source regimes
  completion_minimality.json        the 64-member constitution class
  completion_receipt.json           base commit, hashes, terminals
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Optional

from derivation.completion import (
    countermodels_report,
    dependency_graph,
    inventory,
    minimality_report,
    protocols_report,
)
from derivation.export import write_json

BASE_COMMIT = "2c605e2"

TERMINALS = [
    "RELATIVE_REPLAY_CLOSURE_ONLY",
    "EVENT_SOURCE_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER",
    "KERNEL_CONSTITUTION_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER",
    "KERNEL_CONSTITUTION_REMAINS_META",
    "INITIAL_KERNEL_PROVED",
    "ABSOLUTE_NO_OUTSIDE_UNFORMULABLE",
]

OPEN_BRIDGES = [
    "kernel constitution -> kernel constitution (absolute "
    "self-interpretation): the family interpreter is not a member of "
    "its own described family; the outermost interpretation relation "
    "remains metatheoretic (named irreducible obligation)",
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args(argv)
    inv = inventory()
    graph = dependency_graph()
    graph_payload = {"inventory": inv, "graph": graph}
    protocols = protocols_report()
    minimality = minimality_report()
    counters = countermodels_report()
    receipt = {
        "base_commit": BASE_COMMIT,
        "prompt_sha256": {
            "prompt/prompt.md": sha256_of(Path("prompt/prompt.md")),
            "prompt/seed_prompt.md":
                sha256_of(Path("prompt/seed_prompt.md")),
        },
        "theorem_count": len(inv),
        "axiom_report_sha256":
            sha256_of(Path("artifacts") / "lean_axioms.txt"),
        "gates": {
            "python_tests": "pytest (see CI: coverage run -m pytest)",
            "coverage": "ci/check_coverage.py (>=95% line and branch)",
            "mypy": "python -m mypy (strict)",
            "lean_build": "lake build (no sorry/admit/axiom/unsafe/"
                          "partial; ci/check_lean_audit.py)",
            "axiom_report": "ci/check_axiom_report.py",
            "artifacts": "ci/compare_artifacts.py",
            "prompts": "ci/check_prompt_hashes.py",
        },
        "terminals": TERMINALS,
        "open_bridges": OPEN_BRIDGES,
        "terminal_evidence": {
            "RELATIVE_REPLAY_CLOSURE_ONLY": [
                "NoOutside.effectual_outside_dichotomy",
                "NoOutside.support_replay",
                "paper/native_derivation_completion.md",
            ],
            "EVENT_SOURCE_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER": [
                "Constitution.driver_reproduces_tower",
                "Constitution.nextFamily_complete",
                "completion_protocols.json",
            ],
            "KERNEL_CONSTITUTION_INTERNALIZED_RELATIVE_TO_FIXED"
            "_INTERPRETER": [
                "Constitution.interp_describe",
                "Constitution.allDescs_complete",
            ],
            "KERNEL_CONSTITUTION_REMAINS_META": [
                "stratification boundary (Constitution module header)",
                "completion_receipt.json:open_bridges",
            ],
            "INITIAL_KERNEL_PROVED": [
                "Initiality.unique_compliant",
                "Initiality.extension_retract_replay",
                "completion_minimality.json",
            ],
            "ABSOLUTE_NO_OUTSIDE_UNFORMULABLE": [
                "scope notes: NoOutside.effectual_outside_dichotomy "
                "(operational, constitution-relative; the absolute "
                "form quantifies over unrepresented differences and "
                "is not a formulable statement of this calculus)",
            ],
        },
    }
    out = args.artifacts
    write_json(out / "completion_dependency_graph.json", graph_payload)  # type: ignore[arg-type]
    write_json(out / "completion_countermodels.json", counters)  # type: ignore[arg-type]
    write_json(out / "completion_protocols.json", protocols)  # type: ignore[arg-type]
    write_json(out / "completion_minimality.json", minimality)  # type: ignore[arg-type]
    write_json(out / "completion_receipt.json", receipt)  # type: ignore[arg-type]
    print(f"inventory: {len(inv)} theorems")
    statuses = graph["statuses"]
    assert isinstance(statuses, dict)
    print(
        "graph: "
        + ", ".join(f"{k}={v}" for k, v in statuses.items())
    )
    print(
        "driver reproduces supplied stream: "
        f"{protocols['G2_driver_reproduces_supplied_stream']}"
    )
    print(
        "unique compliant kernel: "
        f"{minimality['unique_compliant_is_kernel']}"
    )
    print(f"artifacts written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

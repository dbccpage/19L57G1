"""Produce the contact-status artifact deterministically.

Usage: python code/run_primitive_contact.py [--artifacts DIR]

Writes ``primitive_contact.json``: the declared contact protocol, the
verified absence of the contact package, the resulting terminal
(CONTACT_INPUT_ABSENT), and the fixed native-kernel interface any
future contact must meet."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json


def contact_report(repo_root: Path) -> dict[str, Json]:
    contact_dir = repo_root / "contact" / "omega_primdiff"
    manifest = contact_dir / "CONTACT_MANIFEST.json"
    present = contact_dir.exists()
    return {
        "protocol": {
            "package_path": "contact/omega_primdiff/",
            "read_order": [
                "lean4/ only after the native characterization "
                "commit (Phase II)",
                "prose/ only after the Lean-only comparison commit "
                "(Phase III)",
            ],
            "manifest_required": str(manifest.relative_to(repo_root)),
            "absence_rule": "complete the native phases and terminate "
                            "with CONTACT_INPUT_ABSENT; do not invent "
                            "contents",
        },
        "package_present": present,
        "manifest_present": manifest.exists(),
        "status": "CONTACT_INPUT_ABSENT" if not present
                  else "CONTACT_PRESENT_UNPROCESSED",
        "native_kernel_interface": {
            "kernel": "PDA_pointed_witnessed_irreflexive",
            "lean_binding": "PrimitiveContact.NativeKernel",
            "witness": "PrimitiveContact.nativeKernelWitness",
            "universal_status":
                "PrimitiveCats.d2_initial (initial among all pointed "
                "witnessed relations)",
            "orientation_fork": [
                "PrimitiveCats.s2_initial_sym",
                "PrimitiveCats.s2_not_weakly_initial",
                "both branches retained",
            ],
            "observer_branching": "PrimitiveCats.no_terminal_pres",
            "implication_matrix":
                "artifacts/primitive_implication_matrix.json "
                "(72 cells, PrimitiveCore.matrixCells)",
        },
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent
    payload = contact_report(repo_root)
    out_path = args.artifacts / "primitive_contact.json"
    write_json(out_path, payload)
    print(f"contact status: {payload['status']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

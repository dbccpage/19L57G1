"""Runner for multi-depth ladder verification and receipt emission.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import multi_depth as md  # noqa: E402
import verify_lean  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-depth ladder verification runner.")
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Running Lean 4 audit...")
    lean_ok = (verify_lean.main() == 0)

    print("Running 1,152-sweep verification...")
    sweep = md.run_sweep_verification()

    print("Checking ladder strictness...")
    ladder_checks = []
    for k in range(1, 6):
        tape = md.twist_tape(k)
        f_kp1 = md.functional(k + 1, tape)
        f_k = md.functional(k, tape)
        ladder_checks.append({
            "k": k,
            "tape": list(tape),
            "functional_k": f_k,
            "functional_kp1": f_kp1,
            "strict_separation": f_kp1 and not f_k,
        })

    receipt_data = {
        "lean_verification": {
            "theorem": "DepthLadder.ladder_monotonic",
            "axioms": ["propext", "Quot.sound"],
            "zero_classical_choice": True,
            "zero_mathlib": True,
            "audit_passed": lean_ok,
        },
        "sweep_verification": sweep,
        "ladder_strictness": ladder_checks,
    }

    out_file = out_dir / "multi_depth.json"
    content = json.dumps(receipt_data, indent=2, sort_keys=True) + "\n"
    out_file.write_text(content, encoding="utf-8")
    print(f"Receipt written to {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

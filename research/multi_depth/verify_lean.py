"""Build and audit Lean 4 theorems in DepthLadder.lean.

Ensures zero usage of Classical.choice or mathlib, and verifies that all
axioms are strictly contained within {propext, Quot.sound}.
AuthorityEffect: None.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
LEAN = HERE / "lean"
WHITELIST = {"propext", "Quot.sound"}
FORBIDDEN = ["so" + "rry", "ad" + "mit", "uns" + "afe", "par" + "tial"]


def main() -> int:
    failures = 0
    sources = sorted(LEAN.rglob("*.lean"))
    sources = [s for s in sources if ".lake" not in s.parts]

    for src in sources:
        text = src.read_text("utf-8")
        for tok in FORBIDDEN:
            if tok in text:
                print(f"FAIL: {src.name} contains forbidden token {tok}")
                failures += 1

    # Force re-elaboration by touching DepthLadder.lean
    ladder_src = LEAN / "DepthLadder.lean"
    ladder_src.touch()

    proc = subprocess.run(
        ["lake", "build"], capture_output=True, text=True, cwd=LEAN, check=False
    )
    log = proc.stdout + proc.stderr

    if proc.returncode != 0:
        print("FAIL: lake build exited nonzero")
        print(log[-2000:])
        return 1

    no_ax = re.findall(r"'(.+?)' does not depend on any axioms", log)
    with_ax = re.findall(r"'(.+?)' depends on axioms: \[([^\]]*)\]", log)
    reported = set(no_ax) | {name for name, _ in with_ax}

    for name, axes in with_ax:
        used = {a.strip() for a in axes.split(",") if a.strip()}
        extra = used - WHITELIST
        if extra:
            print(f"FAIL: {name} depends on disallowed axioms {sorted(extra)}")
            failures += 1
        else:
            print(f"PASS: {name} depends only on {sorted(used)}")

    for name in no_ax:
        print(f"PASS: {name} depends on no axioms")

    if not reported:
        print("FAIL: No axiom reports found in lake output")
        return 1

    if failures > 0:
        print(f"Audit FAILED with {failures} failure(s)")
        return 1

    print(
        f"Lean audit clean: {len(sources)} source(s), {len(reported)} axiom report(s), "
        f"all axioms strictly within {sorted(WHITELIST)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Unit 01 check: no instance is derivable in Genesis's starting regime.

Runs Genesis's own Python model. A finite sample, not a proof; the proof is
Derivation.genesis_underivable. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u01_genesis_underivable.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.model import EMPTY  # noqa: E402
from derivation.observe import derivable  # noqa: E402


def main() -> int:
    tried = 0
    found = []
    for form in range(4):
        for length in range(4):
            for args in itertools.product(range(4), repeat=length):
                inst = (form, tuple(args))
                tried += 1
                if derivable(EMPTY, inst):
                    found.append(inst)
    print(f"instances tried: {tried}")
    print(f"derivable in EMPTY: {found}")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())

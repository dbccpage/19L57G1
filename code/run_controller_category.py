"""Produce the controller-category artifact deterministically.

Usage: python code/run_controller_category.py [--artifacts DIR]

Writes ``primitive_controller_category.json``: the 1024-member class
of variable event grammars, the live census, two-rule executability
over every live member, the three response-kind countermodels, the
behavioral non-uniqueness record on a declared basis, the
constant-simulation refutation of initiality, and the
strict-refinement record with its invariant twist and
reachable-orbit agreement."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.controller_category import controller_category_report
from derivation.export import Json, write_json


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    args = parser.parse_args(argv)
    payload: dict[str, Json] = controller_category_report()
    out_path = args.artifacts / "primitive_controller_category.json"
    write_json(out_path, payload)
    print(f"class: {payload['class_size']} controllers, "
          f"{payload['live_census']} live")
    print(f"two-rule executable on every live member: "
          f"{payload['tworule_all_live_pass']}")
    nonuniq = payload["nonuniqueness"]
    assert isinstance(nonuniq, dict)
    basis = nonuniq["behavioral_basis"]
    assert isinstance(basis, dict)
    print(f"behavioral classes on declared basis: "
          f"{basis['distinct_behavioral_classes']}"
          f"/{basis['live_members']}")
    print(f"initiality: {payload['initiality']}")
    strict = payload["strict_refinement"]
    assert isinstance(strict, dict)
    orbit = strict["reachable_orbit"]
    assert isinstance(orbit, dict)
    print(f"strict refinement: global_uniqueness="
          f"{strict['global_uniqueness']}, orbit_agree="
          f"{orbit['twist_agrees_with_erase']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

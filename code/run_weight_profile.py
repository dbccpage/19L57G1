"""Produce the finite weight-profile artifact deterministically.

Usage: python code/run_weight_profile.py [--artifacts DIR]
       [--carrier N] [--max-weight W] [--max-decoration C]
       [--coeff-bound A] [--input-bound X]

Writes ``weight_profile.json``: the positive-domain profile and exact
common-cross-multiple classification; the zero-scale boundary;
duplicate-free carrier policy; unsigned-square determination; one
declared signed-square/mixing witness; the exact two-coordinate
descent classification; and the audit showing that the former climb
contained two elementary facts and one false uniqueness schema."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.weight_profile import weight_profile_report


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--carrier", type=int, default=2)
    parser.add_argument("--max-weight", type=int, default=3)
    parser.add_argument("--max-decoration", type=int, default=3)
    parser.add_argument("--coeff-bound", type=int, default=3)
    parser.add_argument("--input-bound", type=int, default=2)
    args = parser.parse_args(argv)
    payload: dict[str, Json] = weight_profile_report(
        args.carrier, args.max_weight, args.max_decoration,
        args.coeff_bound, args.input_bound)
    out_path = args.artifacts / "weight_profile.json"
    write_json(out_path, payload)
    prof = payload["profile"]
    assert isinstance(prof, dict)
    print(f"profile: rays={prof['classes_are_exactly_rays']} "
          f"support={prof['support_preserved']} "
          f"forgets_total={prof['total_is_forgotten']}")
    presentation = payload["presentation"]
    assert isinstance(presentation, dict)
    print(f"presentation: redundant="
          f"{presentation['profile_redundant_for_every_decoration']} "
          f"unsigned_determined="
          f"{presentation['unsigned_decoration_determined']}")
    desc = payload["descent"]
    assert isinstance(desc, dict)
    print(f"descent: classified="
          f"{desc['descent_iff_cross_term_zero']}")
    climb = payload["climb"]
    assert isinstance(climb, dict)
    print(f"climb audit: {climb['status']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

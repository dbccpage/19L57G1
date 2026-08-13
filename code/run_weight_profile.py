"""Produce the weight-profile artifact deterministically.

Usage: python code/run_weight_profile.py [--artifacts DIR]
       [--carrier N] [--max-weight W] [--max-decoration C]
       [--coeff-bound A] [--input-bound X]

Writes ``weight_profile.json``: the profile equivalence and its exact
ray classification; support and order preservation with the forgotten
total; redundancy of a decorated presentation for the profile
question together with its visibility to a declared mixing question;
the descent classification for linear read-outs; and the climb - the
negative fact that the weights do not force a decoration, plus the
named imports a uniqueness law would need, none of them discharged."""

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
    lift = payload["lift"]
    assert isinstance(lift, dict)
    print(f"lift: redundant="
          f"{lift['profile_redundant_for_every_decoration']} "
          f"unsigned_determined="
          f"{lift['unsigned_decoration_determined']}")
    desc = payload["descent"]
    assert isinstance(desc, dict)
    print(f"descent: classified="
          f"{desc['descent_iff_cross_term_zero']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

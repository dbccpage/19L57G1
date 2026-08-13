"""Produce the presentation-compression artifact deterministically.

Usage: python code/run_compression.py [--artifacts DIR] [--max-n N]

Writes ``compression.json``: the exhaustive verification of the
target-relative compression results (factorization, signature
quotient, descent witnesses, enlargement splits, absolute adequacy,
replay digests, class-count bound) over the declared finite bounds,
plus the concrete countermodel instances."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.compression import (
    MAX_FAMILY,
    MAX_M,
    absolute_adequacy_iff_exhaustive,
    class_bound_exhaustive,
    class_pos_exhaustive,
    countermodel_instances,
    descent_instance_count,
    descent_witnessed_exhaustive,
    digest_no_refine_exhaustive,
    dup_no_refine_exhaustive,
    enlarge_refines_exhaustive,
    factor_unique_on_image_exhaustive,
    factorization_iff_exhaustive,
    off_image_countermodel,
    quotient_adequate_exhaustive,
    quotient_coarsest_exhaustive,
    quotient_exact_exhaustive,
    separator_required_exhaustive,
    sig_iff_exhaustive,
    split_characterization_exhaustive,
    split_count,
    strict_split_increases_exhaustive,
)
from derivation.export import Json, write_json


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--max-n", type=int, default=3)
    args = parser.parse_args(argv)
    n, m, fam = args.max_n, MAX_M, MAX_FAMILY
    payload: dict[str, Json] = {
        "bounds": {
            "max_domain": n,
            "max_codomain": m,
            "max_family_size": fam,
            "enlargement_step": 1,
        },
        "factorization": {
            "iff_fiber_constant": factorization_iff_exhaustive(n, m),
            "unique_on_image":
                factor_unique_on_image_exhaustive(n, m),
            "off_image_countermodel": off_image_countermodel(),
        },
        "quotient": {
            "sig_eq_iff_sig_list": sig_iff_exhaustive(n, m, fam),
            "exact": quotient_exact_exhaustive(n, m, fam),
            "adequate": quotient_adequate_exhaustive(n, m, fam),
            "coarsest": quotient_coarsest_exhaustive(n, m, fam),
        },
        "descent": {
            "all_witnessed": descent_witnessed_exhaustive(n, m, fam),
            "instances": descent_instance_count(n, m, fam),
        },
        "enlargement": {
            "refines": enlarge_refines_exhaustive(n, m, fam),
            "split_iff_new_separator":
                split_characterization_exhaustive(n, m, fam),
            "splits": split_count(n, m, fam),
        },
        "absolute_adequacy": {
            "iff_injective":
                absolute_adequacy_iff_exhaustive(n, m, fam),
        },
        "replay": {
            "dup_no_refine": dup_no_refine_exhaustive(n, m, fam),
            "digest_no_refine":
                digest_no_refine_exhaustive(n, m, fam),
            "split_requires_new_separator":
                separator_required_exhaustive(n, m, fam),
        },
        "class_count": {
            "bounded_by_domain": class_bound_exhaustive(n, m, fam),
            "positive_on_nonempty": class_pos_exhaustive(n, m, fam),
            "strict_split_increases":
                strict_split_increases_exhaustive(n, m, fam),
            "strict_steps_upper_bounds": {
                str(k): k - 1 for k in range(1, n + 1)},
        },
        "countermodels": countermodel_instances(),
    }
    out_path = args.artifacts / "compression.json"
    write_json(out_path, payload)
    fac = payload["factorization"]
    assert isinstance(fac, dict)
    quo = payload["quotient"]
    assert isinstance(quo, dict)
    print(f"factorization iff fiber-constant to n={n}: "
          f"{fac['iff_fiber_constant']}")
    print(f"quotient exact/adequate/coarsest: {quo['exact']}/"
          f"{quo['adequate']}/{quo['coarsest']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

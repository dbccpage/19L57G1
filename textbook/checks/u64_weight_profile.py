"""Check script for Unit 64: A profile without division (WeightProfile).

Recomputes and verifies:
  1. Exhaustive positive-total equivalence, ray agreement, support/order preservation,
     unsigned square determination, signed square splitting, descent iff cross term zero,
     and climb audit via weight_profile_report().
  2. Zero-total middle assignment countermodel to transitivity without 0 < total l v.
  3. Student exercise check on sq(read_out(2, 3, 1, 1)) vs sq(read_out(2, 3, 1, -1)).
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.weight_profile import (  # noqa: E402
    carrier_list,
    mix_sum,
    read_out,
    same_profile,
    same_ray,
    sq,
    total,
    weight_profile_report,
)


def main() -> int:
    failures: list[str] = []

    report = weight_profile_report(size=3, maxw=2, maxc=2, coeff_bound=2, input_bound=2)
    prof = report["profile"]
    pres = report["presentation"]
    desc = report["descent"]
    climb = report["climb"]

    if not (
        prof["equivalence"]["refl"]
        and prof["equivalence"]["symm"]
        and prof["equivalence"]["trans"]
        and prof["scaling_invariant"]
        and prof["positive_scale_stays_positive"]
        and prof["zero_scale_raw_profile"]
        and prof["zero_scale_exits_positive_domain"]
        and prof["classes_are_exactly_rays"]
        and prof["support_preserved"]
        and prof["order_preserved"]
        and prof["total_is_forgotten"]
    ):
        failures.append(f"profile_report failed: {prof}")

    if not (
        pres["profile_redundant_for_every_decoration"]
        and pres["unsigned_decoration_determined"]
        and pres["unsigned_pairs_with_equal_moduli_that_differ"] == 0
        and pres["signed_square_fixture"]["both_present_same_integer_square_weights"]
        and pres["signed_square_fixture"]["presentations_differ"]
        and pres["signed_square_fixture"]["declared_mixing_separates"]
    ):
        failures.append(f"presentation_report failed: {pres}")

    if not (desc["descent_iff_cross_term_zero"] and desc["sign_gap_identity"]):
        failures.append(f"descent_report failed: {desc}")

    if climb["claimed_readout_uniqueness"]["status"] != "FALSE_WITH_COUNTERMODEL":
        failures.append(f"climb_report failed: {climb}")

    # 1. Duplicate list vs carrier list
    if carrier_list((0, 0)):
        failures.append("expected carrier_list((0, 0)) == False")
    if not carrier_list((0, 1)):
        failures.append("expected carrier_list((0, 1)) == True")

    # 2. Student exercise: zero-total middle assignment breaks transitivity
    c01 = (0, 1)
    u = {0: 1, 1: 2}
    v = {0: 0, 1: 0}
    w = {0: 2, 1: 1}
    if total(c01, u) != 3 or total(c01, v) != 0 or total(c01, w) != 3:
        failures.append("unexpected totals on u={0:1,1:2}, v={0:0,1:0}, w={0:2,1:1}")
    if not same_profile(c01, u, v) or not same_profile(c01, v, w):
        failures.append("expected same_profile(c01, u, v) and same_profile(c01, v, w) to hold")
    if same_profile(c01, u, w):
        failures.append("expected same_profile(c01, u, w) to be False")
    if same_ray(c01, u, v, bound=6):
        failures.append("expected same_ray(c01, u, v, 6) to be False")

    # 3. Signed mixing and student exercise on read_out(2, 3, ...)
    s_plus = {0: 1, 1: 1}
    s_split = {0: 1, 1: -1}
    if mix_sum(c01, s_plus) != 4 or mix_sum(c01, s_split) != 0:
        failures.append("unexpected mix_sum on s_plus or s_split")

    r_plus = sq(read_out(2, 3, 1, 1))
    r_split = sq(read_out(2, 3, 1, -1))
    if r_plus != 25 or r_split != 1 or (r_plus - r_split) != 4 * (2 * 3):
        failures.append(f"unexpected squared read_out values: {r_plus}, {r_split}")

    result = {
        "unit": 64,
        "module": "WeightProfile",
        "assignments_checked": prof["assignments_checked"],
        "decorations_checked": pres["decorations_checked"],
        "descent_rows_checked": desc["rows_checked"],
        "zero_middle_countermodel": {
            "same_profile_uv": same_profile(c01, u, v),
            "same_profile_vw": same_profile(c01, v, w),
            "same_profile_uw": same_profile(c01, u, w),
        },
        "read_out_2_3_sq": {
            "plus": r_plus,
            "split": r_split,
            "diff": r_plus - r_split,
        },
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

"""Standalone verification for Textbook Unit 61: Compressing a presentation against a question list.

Usage: python textbook/checks/u61_compression.py

Imports the repository's ``code/derivation/compression.py``, verifies all
exhaustive checks up to MAX_N = 3, MAX_M = 3, MAX_FAMILY = 2 against
``artifacts/compression.json``, and exercises the D = [0, 1, 2, 3] chain,
off-image non-uniqueness, and the contrast between the unused subfamily
hypothesis in ``splits_iff_new_separator`` and the load-bearing subfamily
hypothesis in ``strict_split_increases``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.compression import (  # noqa: E402
    MAX_FAMILY,
    MAX_M,
    MAX_N,
    Fn,
    Family,
    absolute_adequacy_iff_exhaustive,
    adequate,
    class_bound_exhaustive,
    class_count,
    class_pos_exhaustive,
    countermodel_instances,
    descent_instance_count,
    descent_witnessed_exhaustive,
    digest_no_refine_exhaustive,
    dup_no_refine_exhaustive,
    enlarge_refines_exhaustive,
    factor_unique_on_image_exhaustive,
    factorization_iff_exhaustive,
    factors_on,
    fiber_constant,
    off_image_countermodel,
    p_quotient,
    partition_of,
    quotient_adequate_exhaustive,
    quotient_coarsest_exhaustive,
    quotient_exact_exhaustive,
    separator_required_exhaustive,
    sig_determined,
    sig_eq,
    sig_iff_exhaustive,
    sig_list,
    split_characterization_exhaustive,
    split_count,
    splits_at,
    strict_split_increases_exhaustive,
    valid_factor_maps,
)


def exercise_four_point_domain() -> dict[str, object]:
    """Walk D = [0, 1, 2, 3] through Q0 = [], Q1 = [parity], Q2 = [parity, half]
    and test off-image factoring, descent witnesses, and non-subfamily splits."""
    D = [0, 1, 2, 3]
    q_parity: Fn = (0, 1, 0, 1)
    q_half: Fn = (0, 0, 1, 1)
    q_xor: Fn = (0, 1, 1, 0)  # digest of q_parity: NOT a digest of q_parity alone!
    q_not_parity: Fn = (1, 0, 1, 0)  # digest of q_parity alone: 1 - q_parity(x)

    Q0: Family = ()
    Q1: Family = (q_parity,)
    Q1_digest: Family = (q_parity, q_not_parity)
    Q2: Family = (q_parity, q_half)

    pQ0 = p_quotient(D, Q0)
    pQ1 = p_quotient(D, Q1)
    pQ1_digest = p_quotient(D, Q1_digest)
    pQ2 = p_quotient(D, Q2)

    # A presentation finer than pQ1 whose image omits 0:
    p_fine: Fn = (2, 1, 2, 3)
    fine_adequate = adequate(D, Q1, p_fine)
    fine_factors = valid_factor_maps(D, p_fine, pQ1, 4)
    # Extending the unique on-image map {1: 1, 2: 0, 3: 1} to off-image 0:
    g_a = {0: 0, 1: 1, 2: 0, 3: 1}
    g_b = {0: 3, 1: 1, 2: 0, 3: 1}
    both_factor_on_D = (
        all(g_a[p_fine[x]] == pQ1[x] for x in D)
        and all(g_b[p_fine[x]] == pQ1[x] for x in D)
        and all(g_a[p_fine[x]] == g_b[p_fine[x]] for x in D)
        and g_a[0] != g_b[0]
    )

    # A presentation that merges 0 and 1, failing Q1-adequacy:
    p_bad: Fn = (0, 0, 2, 3)
    bad_adequate = adequate(D, Q1, p_bad)
    bad_witness_ok = (
        p_bad[0] == p_bad[1]
        and not sig_eq(Q1, 0, 1)
        and q_parity[0] != q_parity[1]
        and not fiber_constant(D, p_bad, q_parity)
        and not factors_on(D, p_bad, q_parity, 4)
    )

    # Contrast: splits_iff_new_separator does not need Q subseteq Q',
    # whereas strict_split_increases does.
    D3 = [0, 1, 2]
    ind0: Fn = (1, 0, 0)
    ind1: Fn = (0, 1, 0)
    fam_a: Family = (ind0,)
    fam_b: Family = (ind1,)
    non_sub_split_at_1 = splits_at(D3, fam_a, fam_b, 1)
    non_sub_iff_holds = non_sub_split_at_1 == any(
        sig_eq(fam_a, 1, xp) and any(qp[1] != qp[xp] for qp in fam_b)
        for xp in D3
    )
    non_sub_counts_equal = class_count(D3, fam_a) == class_count(D3, fam_b) == 2

    return {
        "pQ0": pQ0,
        "pQ1": pQ1,
        "pQ1_digest": pQ1_digest,
        "pQ2": pQ2,
        "partitions": [
            partition_of(D, Q0),
            partition_of(D, Q1),
            partition_of(D, Q2),
        ],
        "class_counts": [
            class_count(D, Q0),
            class_count(D, Q1),
            class_count(D, Q1_digest),
            class_count(D, Q2),
        ],
        "digest_determined": sig_determined(D, Q1, q_not_parity),
        "xor_not_determined_by_parity": not sig_determined(D, Q1, q_xor),
        "fine_adequate": fine_adequate,
        "fine_unique_on_image_count": len(fine_factors),
        "both_factor_on_D_differ_off_image": both_factor_on_D,
        "bad_adequate": bad_adequate,
        "bad_witness_ok": bad_witness_ok,
        "non_sub_split_at_1": non_sub_split_at_1,
        "non_sub_iff_holds": non_sub_iff_holds,
        "non_sub_counts_equal": non_sub_counts_equal,
    }


def main() -> int:
    failures: list[str] = []

    n, m, fam = MAX_N, MAX_M, MAX_FAMILY
    payload = {
        "bounds": {
            "max_domain": n,
            "max_codomain": m,
            "max_family_size": fam,
            "enlargement_step": 1,
        },
        "factorization": {
            "iff_fiber_constant": factorization_iff_exhaustive(n, m),
            "unique_on_image": factor_unique_on_image_exhaustive(n, m),
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
            "split_iff_new_separator": split_characterization_exhaustive(n, m, fam),
            "splits": split_count(n, m, fam),
        },
        "absolute_adequacy": {
            "iff_injective": absolute_adequacy_iff_exhaustive(n, m, fam),
        },
        "replay": {
            "dup_no_refine": dup_no_refine_exhaustive(n, m, fam),
            "digest_no_refine": digest_no_refine_exhaustive(n, m, fam),
            "split_requires_new_separator": separator_required_exhaustive(n, m, fam),
        },
        "class_count": {
            "bounded_by_domain": class_bound_exhaustive(n, m, fam),
            "positive_on_nonempty": class_pos_exhaustive(n, m, fam),
            "strict_split_increases": strict_split_increases_exhaustive(n, m, fam),
            "strict_steps_upper_bounds": {
                str(k): k - 1 for k in range(1, n + 1)
            },
        },
        "countermodels": countermodel_instances(),
    }

    if not payload["factorization"]["iff_fiber_constant"]:
        failures.append("factorization_iff_exhaustive failed")
    if not payload["factorization"]["unique_on_image"]:
        failures.append("factor_unique_on_image_exhaustive failed")
    if not (
        payload["quotient"]["sig_eq_iff_sig_list"]
        and payload["quotient"]["exact"]
        and payload["quotient"]["adequate"]
        and payload["quotient"]["coarsest"]
    ):
        failures.append("quotient exhaustive checks failed")
    if not payload["descent"]["all_witnessed"] or payload["descent"]["instances"] != 37736:
        failures.append(f"descent check mismatch: {payload['descent']}")
    if not (
        payload["enlargement"]["refines"]
        and payload["enlargement"]["split_iff_new_separator"]
        and payload["enlargement"]["splits"] == 10006
    ):
        failures.append(f"enlargement check mismatch: {payload['enlargement']}")
    if not payload["absolute_adequacy"]["iff_injective"]:
        failures.append("absolute_adequacy_iff_exhaustive failed")
    if not (
        payload["replay"]["dup_no_refine"]
        and payload["replay"]["digest_no_refine"]
        and payload["replay"]["split_requires_new_separator"]
    ):
        failures.append("replay/digest exhaustive checks failed")
    if not (
        payload["class_count"]["bounded_by_domain"]
        and payload["class_count"]["positive_on_nonempty"]
        and payload["class_count"]["strict_split_increases"]
    ):
        failures.append("class_count exhaustive checks failed")

    cm = payload["countermodels"]
    if not (
        cm["both_split_at_zero"]
        and cm["equal_cost"]
        and cm["classes_one"] == [[0], [1, 2]]
        and cm["classes_two"] == [[0, 2], [1]]
        and cm["classes_differ"]
        and cm["class_count_increases"]
    ):
        failures.append(f"countermodel_instances mismatch: {cm}")

    ex = exercise_four_point_domain()
    if ex["pQ0"] != (0, 0, 0, 0):
        failures.append(f"pQ0 mismatch: {ex['pQ0']}")
    if ex["pQ1"] != (0, 1, 0, 1):
        failures.append(f"pQ1 mismatch: {ex['pQ1']}")
    if ex["pQ1_digest"] != (0, 1, 0, 1):
        failures.append(f"pQ1_digest mismatch: {ex['pQ1_digest']}")
    if ex["pQ2"] != (0, 1, 2, 3):
        failures.append(f"pQ2 mismatch: {ex['pQ2']}")
    if ex["class_counts"] != [1, 2, 2, 4]:
        failures.append(f"class_counts mismatch: {ex['class_counts']}")
    if not (
        ex["digest_determined"]
        and ex["xor_not_determined_by_parity"]
        and ex["fine_adequate"]
        and ex["fine_unique_on_image_count"] == 1
        and ex["both_factor_on_D_differ_off_image"]
        and not ex["bad_adequate"]
        and ex["bad_witness_ok"]
        and ex["non_sub_split_at_1"]
        and ex["non_sub_iff_holds"]
        and ex["non_sub_counts_equal"]
    ):
        failures.append(f"four-point domain exercise failed: {ex}")

    art_path = ROOT / "artifacts" / "compression.json"
    art = json.loads(art_path.read_text(encoding="utf-8"))
    if art != payload:
        failures.append("artifacts/compression.json mismatch with recomputed payload")

    print(
        f"Unit 61 Compression check: factorization_iff={payload['factorization']['iff_fiber_constant']}; "
        f"quotient_exact_adequate_coarsest="
        f"{payload['quotient']['exact']}/{payload['quotient']['adequate']}/{payload['quotient']['coarsest']}; "
        f"descent_instances={payload['descent']['instances']}; "
        f"splits={payload['enlargement']['splits']}; "
        f"D4_counts={ex['class_counts']}; "
        f"failures={failures}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

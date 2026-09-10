"""Adversarial Oracle and Falsification Test for Redheffer Column-Reduction.

Tests mathematical fidelity, non-vacuity, and numerical equivalence between:
- Standard mathematical Redheffer matrix R_n and running balance function M(n)
- Lean 4 implementation of redheffer, redhefferReduced, and redhefferByColReduction
- Column-reduction linear combinations and subdiagonal elimination
- Determinant preservation det(R_n) = det(R'_n) = M(n)
- Diagonal product evaluation diagProduct(R'_n, n) = M(n)
- Leibniz branch collapse on arrangements for n up to 6
"""

from __future__ import annotations

import fractions
import itertools
from typing import List, Tuple


def prime_factors(n: int) -> List[int]:
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0:
                return []  # square factor exists -> mu(n) = 0
        else:
            d += 1
    if temp > 1:
        factors.append(temp)
    return factors


def balance_sign(n: int) -> int:
    if n == 1:
        return 1
    d = 2
    temp = n
    count = 0
    while d * d <= temp:
        if temp % d == 0:
            count += 1
            temp //= d
            if temp % d == 0:
                return 0
        d += 1
    if temp > 1:
        count += 1
    return -1 if count % 2 == 1 else 1


def running_balance(n: int) -> int:
    return sum(balance_sign(k) for k in range(1, n + 1))


def redheffer_math(i: int, j: int) -> int:
    """Standard definition: R(i, j) = 1 if i divides j or j == 1, else 0."""
    if j == 1 or j % i == 0:
        return 1
    return 0


def redheffer_lean(i: int, j: int) -> int:
    """Lean 4 definition in RedhefferObstruction.lean."""
    if i == j:
        return 1
    elif j == 1:
        return 1
    elif j % i == 0:
        return 1
    else:
        return 0


def redheffer_reduced_lean(n: int, i: int, j: int) -> int:
    """Lean 4 definition of redhefferReduced n i j."""
    if i > j:
        return 0
    elif j == 1:
        return running_balance(n)
    else:
        return redheffer_lean(i, j)


def col_reduction_linear_comb(n: int, i: int) -> int:
    """colReductionLinearComb n i."""
    total = 0
    for j in range(2, n + 1):
        coeff = running_balance(n // j)
        total += coeff * redheffer_lean(i, j)
    return total


def redheffer_by_col_reduction(n: int, i: int, j: int) -> int:
    """redhefferByColReduction n i j."""
    if j == 1:
        return redheffer_lean(i, 1) - col_reduction_linear_comb(n, i)
    else:
        return redheffer_lean(i, j)


def diag_product(matrix_fn, n: int) -> int:
    """Product of diagonal elements 1..n."""
    prod = 1
    for k in range(1, n + 1):
        prod *= matrix_fn(k, k)
    return prod


def exact_det(matrix: List[List[int]]) -> int:
    """Exact fraction Bareiss / Gaussian elimination for integer determinant."""
    n = len(matrix)
    if n == 0:
        return 1
    # Convert to fractions
    a = [[fractions.Fraction(matrix[i][j]) for j in range(n)] for i in range(n)]
    sign = 1
    for i in range(n):
        pivot = i
        while pivot < n and a[pivot][i] == 0:
            pivot += 1
        if pivot == n:
            return 0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            sign = -sign
        for j in range(i + 1, n):
            factor = a[j][i] / a[i][i]
            for k in range(i, n):
                a[j][k] -= factor * a[i][k]
    det_val = fractions.Fraction(sign)
    for i in range(n):
        det_val *= a[i][i]
    assert det_val.denominator == 1, f"Non-integer determinant: {det_val}"
    return det_val.numerator


def count_inversions(p: List[int]) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1
    return inv


def sign_perm(p: List[int]) -> int:
    return 1 if count_inversions(p) % 2 == 0 else -1


def leibniz_det(matrix_fn, n: int) -> int:
    """Exact Leibniz expansion: sum_{p in S_n} sign(p) prod_{i=1}^n T(i, p[i-1])."""
    perms = itertools.permutations(range(1, n + 1))
    total = 0
    for p in perms:
        prod = 1
        for i in range(1, n + 1):
            prod *= matrix_fn(i, p[i - 1])
        total += sign_perm(list(p)) * prod
    return total


def test_redheffer_definition_fidelity():
    """Verify redheffer_lean matches standard redheffer_math for all 1 <= i, j <= 20."""
    for i in range(1, 21):
        for j in range(1, 21):
            assert redheffer_lean(i, j) == redheffer_math(i, j), (
                f"Mismatch at i={i}, j={j}: lean={redheffer_lean(i, j)}, math={redheffer_math(i, j)}"
            )
    print("[PASS] Redheffer matrix definition matches standard math definition.")


def test_subdiagonal_vanishing():
    """Verify R(i, j) = 0 for all 2 <= j < i."""
    for i in range(2, 25):
        for j in range(2, i):
            val = redheffer_lean(i, j)
            assert val == 0, f"Subdiagonal entry R({i}, {j}) = {val} != 0"
    print("[PASS] All subdiagonal entries in columns j >= 2 vanish.")


def test_col_reduction_equivalence_n1_to_n10():
    """Verify that column reduction by c_j = M(floor(n/j)) matches redhefferReduced for n=1..10."""
    expected_balance = {
        1: 1, 2: 0, 3: -1, 4: -1, 5: -2,
        6: -1, 7: -2, 8: -2, 9: -2, 10: -1
    }
    for n in range(1, 11):
        m_n = running_balance(n)
        assert m_n == expected_balance[n], f"Running balance mismatch at n={n}: {m_n} != {expected_balance[n]}"
        
        # Check every entry (i, j) in 1..n
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                col_red_val = redheffer_by_col_reduction(n, i, j)
                red_val = redheffer_reduced_lean(n, i, j)
                assert col_red_val == red_val, (
                    f"Col reduction mismatch at n={n}, i={i}, j={j}: "
                    f"col_red={col_red_val}, red={red_val}"
                )
        
        # Check upper triangular structure
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                val = redheffer_reduced_lean(n, i, j)
                if i > j:
                    assert val == 0, f"Upper triangular violation at n={n}, ({i}, {j}): {val}"
                elif i == 1 and j == 1:
                    assert val == m_n, f"(1, 1) entry is {val}, expected M({n})={m_n}"
                elif i == j and i >= 2:
                    assert val == 1, f"Diagonal entry ({i}, {i}) is {val}, expected 1"
        
        # Check diagProduct
        dp = diag_product(lambda i, j: redheffer_reduced_lean(n, i, j), n)
        assert dp == m_n, f"diagProduct at n={n} is {dp}, expected M({n})={m_n}"

    print("[PASS] Column reduction equivalence and diagProduct verified for n=1..10.")


def test_determinants_n1_to_n10():
    """Compute exact determinants of R_n and R'_n using Bareiss/Gaussian and Leibniz."""
    for n in range(1, 11):
        # Build matrix tables
        mat_orig = [[redheffer_lean(i, j) for j in range(1, n + 1)] for i in range(1, n + 1)]
        mat_red = [[redheffer_reduced_lean(n, i, j) for j in range(1, n + 1)] for i in range(1, n + 1)]
        
        det_orig = exact_det(mat_orig)
        det_red = exact_det(mat_red)
        m_n = running_balance(n)
        
        assert det_orig == m_n, f"det(R_{n}) = {det_orig} != M({n}) = {m_n}"
        assert det_red == m_n, f"det(R'_{n}) = {det_red} != M({n}) = {m_n}"
        assert det_orig == det_red, f"det(R_{n}) = {det_orig} != det(R'_{n}) = {det_red}"
        
        # Also cross-check with Leibniz expansion for n <= 6
        if n <= 6:
            leib_orig = leibniz_det(redheffer_lean, n)
            leib_red = leibniz_det(lambda i, j: redheffer_reduced_lean(n, i, j), n)
            assert leib_orig == m_n, f"Leibniz det(R_{n}) = {leib_orig} != {m_n}"
            assert leib_red == m_n, f"Leibniz det(R'_{n}) = {leib_red} != {m_n}"

    print("[PASS] Exact determinants det(R_n) = det(R'_n) = M(n) verified for n=1..10.")


def test_insert_all_and_leibniz_branch():
    """Verify branch reduction: for every permutation q in S_n (n <= 5),
    summing insertAll(n+1, q) over redhefferReduced(n+1) collapses to
    sign(q) * rowProduct(q) * T(n+1, n+1).
    """
    for n in range(0, 6):
        perms = list(itertools.permutations(range(1, n + 1))) if n > 0 else [()]
        for q in perms:
            q_list = list(q)
            sq = sign_perm(q_list)
            # row product of q on 1..n
            rp_q = 1
            for i in range(1, n + 1):
                rp_q *= redheffer_reduced_lean(n + 1, i, q_list[i - 1])
            diag_elem = redheffer_reduced_lean(n + 1, n + 1, n + 1)
            expected_branch = sq * rp_q * diag_elem
            
            # Now compute actual branch sum by inserting (n + 1) at all positions
            branch_sum = 0
            for pos in range(len(q_list) + 1):
                p = q_list[:pos] + [n + 1] + q_list[pos:]
                sp = sign_perm(p)
                rp_p = 1
                for i in range(1, n + 2):
                    rp_p *= redheffer_reduced_lean(n + 1, i, p[i - 1])
                branch_sum += sp * rp_p
            
            assert branch_sum == expected_branch, (
                f"Branch mismatch at n={n}, q={q}: branch_sum={branch_sum}, expected={expected_branch}"
            )
    print("[PASS] Leibniz branch reduction verified for all permutations up to n=5.")


def test_extended_horizon_n11_to_n20():
    """Stress test beyond the prompt requirement: verify column reduction and diagProduct up to n=20."""
    for n in range(11, 21):
        m_n = running_balance(n)
        dp = diag_product(lambda i, j: redheffer_reduced_lean(n, i, j), n)
        assert dp == m_n, f"Extended diagProduct mismatch at n={n}: {dp} != {m_n}"
        
        # Verify row 1 and row i >= 2
        row1 = redheffer_by_col_reduction(n, 1, 1)
        assert row1 == m_n, f"Extended row 1 mismatch at n={n}: {row1} != {m_n}"
        for i in range(2, n + 1):
            row_i = redheffer_by_col_reduction(n, i, 1)
            assert row_i == 0, f"Extended subdiagonal non-zero at n={n}, i={i}: {row_i}"
            
        # Also verify exact det(R_n) = M(n)
        mat = [[redheffer_lean(i, j) for j in range(1, n + 1)] for i in range(1, n + 1)]
        d = exact_det(mat)
        assert d == m_n, f"Extended det(R_{n}) = {d} != {m_n}"
    print("[PASS] Extended horizon n=11..20 verified without error.")


def main():
    print("=== Running Challenger M2 Adversarial Oracle ===")
    test_redheffer_definition_fidelity()
    test_subdiagonal_vanishing()
    test_col_reduction_equivalence_n1_to_n10()
    test_determinants_n1_to_n10()
    test_insert_all_and_leibniz_branch()
    test_extended_horizon_n11_to_n20()
    print("=== All Challenger M2 Adversarial Tests PASSED ===")


if __name__ == "__main__":
    main()

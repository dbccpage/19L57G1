"""Tests for separation capacity bounds and scale depth gap.

AuthorityEffect: None.
"""

from __future__ import annotations

from ..observer_hierarchy import is_isomorphic
from ..separation_capacity import (
    bits_to_nat,
    capacity,
    capacity_gap,
    canonical_family_size,
    canonical_test_regime,
    enumerate_canonical_regimes,
    nat_to_bits,
)


def test_nat_to_bits_roundtrip() -> None:
    for length in [1, 2, 3, 4, 5]:
        bound = 2**length
        for n in range(bound):
            bits = nat_to_bits(length, n)
            assert len(bits) == length
            assert bits_to_nat(bits) == n


def test_test_regime_properties() -> None:
    for k in [0, 1, 2, 3]:
        fam_size = canonical_family_size(k)
        assert fam_size == 2 ** (k + 1)
        regimes = [canonical_test_regime(k, i) for i in range(fam_size)]
        # All test regimes have scale depth k + 2
        for r in regimes:
            assert r.depth == k + 2
            # First token is always 0
            assert r.tokens[0] == 0
            # Regimes starting with 0 are already canonical
            assert r.canonical_tokens == r.tokens

        # All test regimes in the family are pairwise non-isomorphic
        for i in range(fam_size):
            for j in range(i + 1, fam_size):
                assert not is_isomorphic(regimes[i], regimes[j])


def test_capacity_and_test_family_size() -> None:
    for k in range(6):
        cap = capacity(k)
        fam = canonical_family_size(k)
        assert cap == 2**k
        assert fam == 2 ** (k + 1)
        assert fam == 2 * cap
        assert fam > cap


def test_capacity_gap() -> None:
    for k in range(5):
        # At immediate scale depth k+2: Gap(k, k+2) = 2^(k+1) - 2^k = 2^k > 0
        gap_imm = capacity_gap(k, k + 2)
        assert gap_imm == 2**k
        assert gap_imm > 0

        # At higher scale depth d > k+2, gap strictly grows
        gap_higher = capacity_gap(k, k + 3)
        assert gap_higher == (2 ** (k + 2)) - (2**k)
        assert gap_higher > gap_imm

        # When d <= k+1, capacity_gap is 0
        assert capacity_gap(k, k + 1) == 0
        assert capacity_gap(k, k) == 0


def test_canonical_regimes_count() -> None:
    # At depth d, number of canonical binary regimes under bit-flip is 2^(d-1) for d >= 1
    for depth in [1, 2, 3, 4]:
        canon_list = list(enumerate_canonical_regimes(depth))
        expected_count = 2 ** (depth - 1)
        assert len(canon_list) == expected_count
        # All pairs in canonical enumeration are pairwise non-isomorphic
        for i in range(len(canon_list)):
            for j in range(i + 1, len(canon_list)):
                assert not is_isomorphic(canon_list[i], canon_list[j])

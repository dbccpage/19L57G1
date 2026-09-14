"""Tests for higher-order diagonalization theorem and adversarial pair generation.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from ..diagonalization import (
    diagonal_evaluation_fibers,
    find_collision,
    higher_order_diagonalization,
    verify_duality,
)
from ..observer_hierarchy import Observer, compose_higher_order, eval_observer, is_isomorphic


def test_find_collision() -> None:
    assert find_collision([3, 1, 4, 1, 5]) == (1, 3)
    assert find_collision([0, 0]) == (0, 1)
    with pytest.raises(ValueError):
        find_collision([0, 1, 2, 3])


def test_higher_order_diagonalization_various_observers() -> None:
    # Test for various depths k in {0, 1, 2, 3}
    for k in [0, 1, 2, 3]:
        # Observer 1: prefix bits observer
        def make_prefix_obs(depth: int) -> Observer:
            def sig_map(trunc: tuple[int, ...]) -> int:
                val = 0
                for idx, b in enumerate(trunc[:depth]):
                    val += b * (2**idx)
                return val % (2**depth)

            return Observer(resolution_depth=depth, signature_map=sig_map)

        obs_prefix = make_prefix_obs(k)
        r1, r2 = higher_order_diagonalization(obs_prefix, k)
        # 1. Regimes must be strictly non-isomorphic
        assert not is_isomorphic(r1, r2)
        # 2. Observer must evaluate them to identical signature
        assert eval_observer(obs_prefix, r1) == eval_observer(obs_prefix, r2)
        # 3. Both regimes have scale depth k + 2
        assert r1.depth == k + 2
        assert r2.depth == k + 2

        # Observer 2: constant zero observer
        obs_const = Observer(
            resolution_depth=k, signature_map=lambda _: 0
        )
        rc1, rc2 = higher_order_diagonalization(obs_const, k)
        assert not is_isomorphic(rc1, rc2)
        assert eval_observer(obs_const, rc1) == eval_observer(obs_const, rc2)

        # Observer 3: parity observer
        obs_parity = Observer(
            resolution_depth=k, signature_map=lambda t: sum(t) % (2**k) if k > 0 else 0
        )
        rp1, rp2 = higher_order_diagonalization(obs_parity, k)
        assert not is_isomorphic(rp1, rp2)
        assert eval_observer(obs_parity, rp1) == eval_observer(obs_parity, rp2)


def test_higher_order_composite_diagonalization() -> None:
    # Higher-order observer of order 2 composed of two order-1 observers
    obs1 = Observer(resolution_depth=1, signature_map=lambda t: t[0] if t else 0)
    obs2 = Observer(resolution_depth=1, signature_map=lambda t: 1 - (t[0] if t else 0))
    composite = compose_higher_order(
        [obs1, obs2],
        lambda traces: (traces[0] + 2 * traces[1]) % 4,
        resolution_depth=2,
    )
    r1, r2 = higher_order_diagonalization(composite, k=2)
    assert not is_isomorphic(r1, r2)
    assert composite(r1) == composite(r2)


def test_diagonal_evaluation_fibers_non_singleton() -> None:
    for k in [0, 1, 2]:
        obs = Observer(
            resolution_depth=k,
            signature_map=lambda t: sum(t) % (2**k) if k > 0 else 0,
        )
        fibers = diagonal_evaluation_fibers(obs, k)
        # By pigeonhole, at least one fiber has at least 2 regimes
        assert any(len(regimes) >= 2 for regimes in fibers.values())
        # Furthermore, in that fiber, the regimes are non-isomorphic
        non_singleton_found = False
        for regimes in fibers.values():
            if len(regimes) >= 2:
                for i in range(len(regimes)):
                    for j in range(i + 1, len(regimes)):
                        if not is_isomorphic(regimes[i], regimes[j]):
                            non_singleton_found = True
                            break
        assert non_singleton_found


def test_verify_duality_receipt() -> None:
    for k in [0, 1, 2, 3]:
        obs = Observer(
            resolution_depth=k,
            signature_map=lambda t: (t[0] if t else 0) % (2**k) if k > 0 else 0,
        )
        report = verify_duality(obs, k)
        assert report["k"] == k
        assert report["capacity"] == 2**k
        assert report["family_size"] == 2 ** (k + 1)
        assert report["gap"] == 2**k
        collapse = report["pair_id_collapse"]
        assert collapse["indistinguishable"] is True
        assert collapse["isomorphic"] is False
        miss = report["family_miss"]
        assert miss["gap_positive"] is True

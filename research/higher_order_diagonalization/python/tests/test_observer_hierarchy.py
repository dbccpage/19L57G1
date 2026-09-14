"""Tests for observer hierarchy and canonical isomorphism coarsening.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from ..observer_hierarchy import (
    Observer,
    ScaleRegime,
    canon_seq,
    compose_higher_order,
    eval_observer,
    flip_seq,
    flip_token,
    is_isomorphic,
    observer_equiv,
    prefix_k,
)


def test_flip_token_involutive() -> None:
    assert flip_token(0) == 1
    assert flip_token(1) == 0
    assert flip_token(flip_token(0)) == 0
    assert flip_token(flip_token(1)) == 1
    with pytest.raises(ValueError):
        flip_token(2)


def test_flip_seq_involutive() -> None:
    seq = [0, 1, 1, 0, 1]
    assert flip_seq(seq) == [1, 0, 0, 1, 0]
    assert flip_seq(flip_seq(seq)) == seq


def test_canon_seq() -> None:
    # 011 is smaller than 100, so canonical is 011
    assert canon_seq([0, 1, 1]) == [0, 1, 1]
    # 100 flips to 011, so canonical is 011
    assert canon_seq([1, 0, 0]) == [0, 1, 1]
    # Invariant: canon_seq(s) == canon_seq(flip_seq(s))
    for s in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        assert canon_seq(s) == canon_seq(flip_seq(s))


def test_scale_regime_isomorphism() -> None:
    r1 = ScaleRegime(depth=3, tokens=(0, 1, 1))
    r2 = ScaleRegime(depth=3, tokens=(1, 0, 0))
    r3 = ScaleRegime(depth=3, tokens=(0, 0, 1))
    # r1 and r2 are isomorphic under bit-flip relabeling
    assert is_isomorphic(r1, r2)
    assert is_isomorphic(r2, r1)
    assert is_isomorphic(r1, r1)
    # r1 and r3 are not isomorphic
    assert not is_isomorphic(r1, r3)
    # Different depth regimes are never isomorphic
    r4 = ScaleRegime(depth=2, tokens=(0, 1))
    assert not is_isomorphic(r1, r4)


def test_prefix_k() -> None:
    tokens = (0, 1, 0, 1, 1)
    assert prefix_k(0, tokens) == ()
    assert prefix_k(2, tokens) == (0, 1)
    assert prefix_k(5, tokens) == (0, 1, 0, 1, 1)
    assert prefix_k(10, tokens) == (0, 1, 0, 1, 1)


def test_eval_observer_isomorphism_invariance() -> None:
    # Observer at depth 2 looking at first 2 canonical bits
    def sig_map(trunc: tuple[int, ...]) -> int:
        b0 = trunc[0] if len(trunc) > 0 else 0
        b1 = trunc[1] if len(trunc) > 1 else 0
        return b0 + 2 * b1

    obs = Observer(resolution_depth=2, signature_map=sig_map)
    r1 = ScaleRegime(depth=3, tokens=(0, 1, 1))
    r2 = ScaleRegime(depth=3, tokens=(1, 0, 0))
    # Evaluation must give identical signatures on isomorphic regimes
    assert eval_observer(obs, r1) == eval_observer(obs, r2)
    assert observer_equiv(obs, r1, r2)
    assert obs(r1) < 2**2


def test_compose_higher_order() -> None:
    # Two base observers of depth 1
    obs1 = Observer(resolution_depth=1, signature_map=lambda t: t[0] if t else 0)
    obs2 = Observer(resolution_depth=1, signature_map=lambda t: 1 - (t[0] if t else 0))

    def agg(traces: Sequence[int]) -> int:
        return (traces[0] + 2 * traces[1]) % 4

    composite = compose_higher_order([obs1, obs2], agg, resolution_depth=2)
    assert composite.resolution_depth == 2

    r1 = ScaleRegime(depth=3, tokens=(0, 1, 1))
    r2 = ScaleRegime(depth=3, tokens=(1, 0, 0))
    assert is_isomorphic(r1, r2)
    assert composite(r1) == composite(r2)

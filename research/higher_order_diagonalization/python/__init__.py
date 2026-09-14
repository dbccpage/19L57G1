"""Higher-order observer separation capacity and diagonalization.

AuthorityEffect: None.
"""

from .observer_hierarchy import (
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
from .separation_capacity import (
    bits_to_nat,
    capacity,
    capacity_gap,
    canonical_family_size,
    canonical_test_regime,
    enumerate_canonical_regimes,
    nat_to_bits,
)
from .diagonalization import (
    diagonal_evaluation_fibers,
    find_collision,
    higher_order_diagonalization,
    verify_duality,
)

__all__ = [
    "Observer",
    "ScaleRegime",
    "bits_to_nat",
    "canon_seq",
    "capacity",
    "capacity_gap",
    "canonical_family_size",
    "canonical_test_regime",
    "compose_higher_order",
    "diagonal_evaluation_fibers",
    "enumerate_canonical_regimes",
    "eval_observer",
    "find_collision",
    "flip_seq",
    "flip_token",
    "higher_order_diagonalization",
    "is_isomorphic",
    "nat_to_bits",
    "observer_equiv",
    "prefix_k",
    "verify_duality",
]

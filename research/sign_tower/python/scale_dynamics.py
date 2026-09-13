"""Scale recursion premise obstruction, Cantor thread dynamics, and positivity gap.

Formalizes Prompt B Targets B4, B5, and B6.3:
- Finite scale bonding rectangular rank defect Delta_n = c^n * (c - 1) > 0
- Preclusion of infinitesimal square generators at premise level (Kill Condition 3)
- Cantor thread space and dyadic twin separation
- Reflection verifying absence of regime alphabet transition attributes
- Kolmogorov Markov cylinder consistency with branching ratio 1.0 (Target B5 structural gap)
"""

from __future__ import annotations

import sys
from dataclasses import fields
from pathlib import Path
from typing import Callable, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.model import Regime


def bond(word: Sequence[int]) -> tuple[int, ...]:
    """Finite scale bonding map: forget the last letter."""
    if not word:
        return ()
    return tuple(word[:-1])


def stage_dimension(c: int, n: int) -> int:
    """Combinatorial state space dimension at scale n for alphabet size c."""
    return c ** n


def rank_defect(c: int, n: int) -> int:
    """Rectangular rank defect Delta_n = c^(n+1) - c^n."""
    return stage_dimension(c, n + 1) - stage_dimension(c, n)


def verify_rectangular_rank_defect(c: int, max_n: int = 10) -> dict[str, object]:
    """Verify strictly positive rank defect Delta_n > 0 for all n in range."""
    defects = {}
    for n in range(max_n + 1):
        d = rank_defect(c, n)
        expected = (c ** n) * (c - 1)
        assert d == expected
        assert d > 0 if c >= 2 else True
        defects[n] = d
    return {
        "c": c,
        "all_positive": all(v > 0 for v in defects.values()) if c >= 2 else False,
        "defects": defects,
    }


def twin_lo(n: int) -> tuple[int, ...]:
    """Lower dyadic twin sequence prefix: 0 followed by 1s."""
    return tuple([0] + [1] * (n - 1)) if n > 0 else ()


def twin_hi(n: int) -> tuple[int, ...]:
    """Upper dyadic twin sequence prefix: 1 followed by 0s."""
    return tuple([1] + [0] * (n - 1)) if n > 0 else ()


def verify_twin_separation(scale: int = 1) -> dict[str, object]:
    """Verify dyadic twins differ at scale 1, refusing continuum completion."""
    lo = twin_lo(scale)
    hi = twin_hi(scale)
    separated = (lo != hi)
    return {
        "scale": scale,
        "twin_lo": lo,
        "twin_hi": hi,
        "separated": separated,
    }


def verify_regime_reflection_no_alphabet_map() -> dict[str, object]:
    """Inspect Regime dataclass fields to confirm absence of alphabet transition maps."""
    field_names = [f.name for f in fields(Regime)]
    has_alphabet_map = "alphabet_map" in field_names or "F" in field_names
    return {
        "fields": field_names,
        "has_alphabet_map": has_alphabet_map,
        "premise_decoupled": not has_alphabet_map,
    }


def verify_kolmogorov_cylinder_consistency(
    c: int,
    prefix_length: int = 3,
) -> dict[str, object]:
    """Verify that uniform base-c Markov weights satisfy Kolmogorov cylinder consistency.

    Weight of cylinder W(w) = c^(-k).
    Sum over children w + (b,) is sum_{b=0}^{c-1} c^(-(k+1)) = c * c^(-(k+1)) = c^(-k).
    Branching ratio = sum(child_weights) / parent_weight == 1.0.
    """
    parent_weight = 1.0 / (c ** prefix_length)
    child_weight = 1.0 / (c ** (prefix_length + 1))
    total_child_weight = c * child_weight
    branching_ratio = total_child_weight / parent_weight

    return {
        "alphabet_size": c,
        "prefix_length": prefix_length,
        "parent_weight": parent_weight,
        "child_weight": child_weight,
        "total_child_weight": total_child_weight,
        "branching_ratio": branching_ratio,
        "is_consistent": abs(branching_ratio - 1.0) < 1e-12,
    }

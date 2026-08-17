"""Born-from-weights, and an optional amplitude lift that reproduces it.

The lift is a selection (phases are free). Uniqueness is not derived.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple


def born_from_weights(weights: Sequence[float]) -> Tuple[float, ...]:
    if any(w < 0 for w in weights):
        raise ValueError("weights must be nonnegative")
    total = sum(weights)
    if total <= 0:
        raise ValueError("weights must have positive sum")
    return tuple(w / total for w in weights)


def optional_amplitude_lift(
    weights: Sequence[float],
    phases: Sequence[float],
) -> Tuple[complex, ...]:
    """c = sqrt(w) exp(i theta). |c|^2 recovers born_from_weights(w)."""
    if len(phases) != len(weights):
        raise ValueError("phases must match weights")
    born_from_weights(weights)  # validate
    return tuple(
        math.sqrt(w) * complex(math.cos(th), math.sin(th))
        for w, th in zip(weights, phases)
    )


def modulus_squared(amplitudes: Sequence[complex]) -> Tuple[float, ...]:
    return tuple((z.real * z.real) + (z.imag * z.imag) for z in amplitudes)

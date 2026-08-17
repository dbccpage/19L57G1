"""Born-from-weights, and an optional amplitude lift that reproduces it.

The lift is a selection (phases are free). Uniqueness is not derived.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple


def born_from_weights(weights: Sequence[float]) -> Tuple[float, ...]:
    if not all(math.isfinite(w) for w in weights):
        raise ValueError("weights must be finite")
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
    """c = sqrt(p) exp(i theta) for p = born_from_weights(w).

    So ``modulus_squared(optional_amplitude_lift(w, ph))`` equals
    ``born_from_weights(w)`` exactly, for any weights with positive
    finite sum -- not only for weights that already sum to one.

    An earlier version built the amplitudes from the RAW weights,
    ``sqrt(w)``, and claimed the same invariant. That was false: the
    modulus squared came back as ``w`` rather than ``w / sum(w)``, so
    the two agreed only when the weights were already normalised. The
    lift is the whole point of this module -- it is meant to show that
    the amplitude encoding REPRODUCES the unit-sum law and adds nothing
    -- so a lift that failed to reproduce it demonstrated nothing.
    """
    if len(phases) != len(weights):
        raise ValueError("phases must match weights")
    if not all(math.isfinite(th) for th in phases):
        raise ValueError("phases must be finite")
    probabilities = born_from_weights(weights)
    return tuple(
        math.sqrt(p) * complex(math.cos(th), math.sin(th))
        for p, th in zip(probabilities, phases)
    )


def modulus_squared(amplitudes: Sequence[complex]) -> Tuple[float, ...]:
    return tuple((z.real * z.real) + (z.imag * z.imag) for z in amplitudes)

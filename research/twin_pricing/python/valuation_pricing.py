"""Operational valuation pricing algorithms under capability cost mu1 and history cost mu2.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def twin_count(c: int, n: int) -> int:
    """Number of elementary twin pairs at scale n for alphabet size c: (c - 1) * c^(n - 1)."""
    if c < 2:
        raise ValueError(f"alphabet size c must be >= 2, got {c}")
    if n < 1:
        raise ValueError(f"scale n must be >= 1, got {n}")
    return (c - 1) * (c ** (n - 1))


def mu1_scale(c: int, n: int) -> int:
    """Total native capability cost mu1 at scale n: unit cost 1 per twin pair."""
    return twin_count(c, n) * 1


def mu2_scale(c: int, n: int) -> int:
    """Total path-dependent history cost mu2 at scale n: depth cost n per twin pair."""
    return twin_count(c, n) * n


def cumulative_mu1(c: int, N: int) -> int:
    """Iterative cumulative capability cost to scale N: sum_{n=1}^N mu1_scale(c, n)."""
    if N < 0:
        raise ValueError(f"scale N must be >= 0, got {N}")
    total = 0
    for n in range(1, N + 1):
        total += mu1_scale(c, n)
    return total


def cumulative_mu1_closed_form(N: int) -> int:
    """Closed-form cumulative capability cost under base 2: 2^N - 1."""
    if N < 0:
        raise ValueError(f"scale N must be >= 0, got {N}")
    return (2 ** N) - 1


def cumulative_mu2(c: int, N: int) -> int:
    """Iterative cumulative history cost to scale N: sum_{n=1}^N mu2_scale(c, n)."""
    if N < 0:
        raise ValueError(f"scale N must be >= 0, got {N}")
    total = 0
    for n in range(1, N + 1):
        total += mu2_scale(c, n)
    return total


def cumulative_mu2_closed_form(N: int) -> int:
    """Closed-form cumulative history cost under base 2: (N - 1) * 2^N + 1."""
    if N < 0:
        raise ValueError(f"scale N must be >= 0, got {N}")
    if N == 0:
        return 0
    return (N - 1) * (2 ** N) + 1


def markov_weighted_scale_cost(n: int) -> float:
    """Markov cylinder weighted capability price at scale n: 2^(-n) * mu1_scale(2, n) = 0.5."""
    if n < 1:
        raise ValueError(f"scale n must be >= 1, got {n}")
    # Exact cancellation: 2^(-n) * 2^(n-1) = 2^(-1) = 0.5 for all n >= 1.
    return 0.5


def cumulative_markov_obstruction(N: int) -> float:
    """Cumulative Markov cylinder obstruction measure after N scales: 0.5 * N."""
    if N < 0:
        raise ValueError(f"scale N must be >= 0, got {N}")
    return 0.5 * float(N)


def verify_asymptotic_profile(max_N: int = 15) -> Dict[str, List[Tuple[int, int, int]]]:
    """Compute and verify agreement across scales 1..max_N."""
    records: List[Tuple[int, int, int]] = []
    for N in range(1, max_N + 1):
        c1_iter = cumulative_mu1(2, N)
        c1_form = cumulative_mu1_closed_form(N)
        assert c1_iter == c1_form, f"mu1 mismatch at N={N}: {c1_iter} != {c1_form}"

        c2_iter = cumulative_mu2(2, N)
        c2_form = cumulative_mu2_closed_form(N)
        assert c2_iter == c2_form, f"mu2 mismatch at N={N}: {c2_iter} != {c2_form}"

        obstruction = cumulative_markov_obstruction(N)
        expected_obs = 0.5 * N
        assert abs(obstruction - expected_obs) < 1e-9

        records.append((N, c1_form, c2_form))
    return {"verified_scales": records}

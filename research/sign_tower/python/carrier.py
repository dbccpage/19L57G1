"""Carrier action, orbit invariance, and witness sign inversion analysis.

Formalizes Prompt B Targets B1.1 and B2.1:
- Coordinate renaming action rename(r, pi)
- Canonical serialization orbit invariance: canonical(rename(r, pi)) == canonical(r)
- Auxiliary search witness analysis on rigid vs symmetric regimes
- Verification of parity-blindness on certified machine state keys
"""

from __future__ import annotations

import sys
from itertools import permutations
from pathlib import Path
from typing import Sequence

# Ensure repo root and code/ are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.iso import canonical, canonical_witness
from derivation.model import (
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Regime,
    step,
)


def perm_sign(pi: Sequence[int]) -> int:
    """Compute standard signature (+1 or -1) of a permutation."""
    n = len(pi)
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if pi[i] > pi[j]:
                inversions += 1
    return -1 if (inversions % 2 == 1) else 1


def rename_regime(r: Regime, pi: Sequence[int]) -> Regime:
    """Apply coordinate permutation pi in S(n) to regime r.

    Presentation tokens are permuted: new_data[pi[d]] = old_data[d].
    Incidences and requirements are mapped accordingly.
    """
    n = r.n_data()
    if len(pi) != n or sorted(pi) != list(range(n)):
        raise ValueError(f"pi must be a permutation of range({n}), got {pi}")

    # Permute presentation tokens
    new_data = ["" for _ in range(n)]
    for old_d, new_d in enumerate(pi):
        new_data[new_d] = r.data[old_d]

    # Permute instance coordinate arguments
    new_insts = set()
    for f, args in r.insts:
        new_args = tuple(pi[a] for a in args)
        new_insts.add((f, new_args))

    # Permute pairwise separation requirements
    new_reqs = set()
    for i, j in r.reqs:
        pi_i, pi_j = pi[i], pi[j]
        new_reqs.add((min(pi_i, pi_j), max(pi_i, pi_j)))

    return Regime(
        data=tuple(new_data),
        forms=r.forms,
        insts=frozenset(new_insts),
        rules=r.rules,
        reqs=frozenset(new_reqs),
    )


def verify_carrier_orbit_invariance(r: Regime) -> bool:
    """Verify canonical(rename(r, pi)) == canonical(r) for all pi in S(n)."""
    n = r.n_data()
    canon_base = canonical(r)
    for pi in permutations(range(n)):
        r_renamed = rename_regime(r, pi)
        if canonical(r_renamed) != canon_base:
            return False
    return True


def analyze_witness_parity(r: Regime) -> dict[str, object]:
    """Analyze witness behavior under all coordinate transpositions.

    Returns whether the regime is rigid, whether witness sign inverts on odd
    transpositions, and confirms that canonical(r) discards the witness.
    """
    n = r.n_data()
    base_key, base_pi, base_phi = canonical_witness(r)
    base_sign = perm_sign(base_pi)

    results = []
    for i in range(n):
        for j in range(i + 1, n):
            # Transposition tau = (i j)
            tau = list(range(n))
            tau[i], tau[j] = tau[j], tau[i]
            r_tau = rename_regime(r, tau)

            tau_key, tau_pi, tau_phi = canonical_witness(r_tau)
            tau_sign = perm_sign(tau_pi)

            results.append({
                "transposition": (i, j),
                "key_match": (tau_key == base_key),
                "base_witness_sign": base_sign,
                "tau_witness_sign": tau_sign,
                "sign_product": base_sign * tau_sign,
                "witness_inverted": (tau_sign == -base_sign),
            })

    return {
        "n_data": n,
        "base_key": base_key,
        "results": results,
    }

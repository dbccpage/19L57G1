"""Constructive Isomorphism Witness Extractor for CL-ISO-SOUND.

Classification: Metatheoretic verification apparatus.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add repo root and code/ to sys.path if not present
REPO_ROOT = Path(__file__).resolve().parents[3]
CODE_DIR = REPO_ROOT / "code"
for p in (str(REPO_ROOT), str(CODE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from typing import NamedTuple, Optional, Sequence, Tuple
from derivation.model import Regime
from derivation.iso import canonical_witness, canonical, serialize, rename, _invert


class WitnessPair(NamedTuple):
    """Pair of data permutation (pi) and form permutation (phi)."""

    pi: tuple[int, ...]
    phi: tuple[int, ...]


def extract_isomorphism_witness(
    r1: Regime, r2: Regime, perm_budget: int = 100_000
) -> Optional[WitnessPair]:
    """Given regimes r1 and r2 with canonical(r1) == canonical(r2),
    extract the concrete constructive isomorphism witness (pi, phi)
    carrying r1 directly onto r2.

    Mathematical Theorem (witness_extract):
        pi = pi_2^{-1} o pi_1
        phi = phi_2^{-1} o phi_1
    satisfies:
        (pi, phi) . r1 == r2 (in structural serialization).
    """
    key1, pi1, phi1 = canonical_witness(r1, perm_budget)
    key2, pi2, phi2 = canonical_witness(r2, perm_budget)
    if key1 != key2:
        return None

    inv_pi2 = _invert(pi2)
    inv_phi2 = _invert(phi2)

    pi_witness = tuple(inv_pi2[pi1[d]] for d in range(r1.n_data()))
    phi_witness = tuple(inv_phi2[phi1[f]] for f in range(len(r1.forms)))

    return pi_witness, phi_witness


def verify_isomorphism(
    r1: Regime, r2: Regime, pi: Sequence[int], phi: Sequence[int]
) -> bool:
    """Verify that (pi, phi) is an exact structural isomorphism carrying r1 onto r2."""
    if r1.n_data() != r2.n_data() or len(r1.forms) != len(r2.forms):
        return False
    renamed = rename(r1, pi, phi)
    id_d = tuple(range(r2.n_data()))
    id_f = tuple(range(len(r2.forms)))
    return serialize(renamed, id_d, id_f) == serialize(r2, id_d, id_f)

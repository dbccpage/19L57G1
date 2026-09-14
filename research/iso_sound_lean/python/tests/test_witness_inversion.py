"""Unit tests for constructive isomorphism witness extraction and verification (CL-ISO-SOUND).

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

PY_DIR = Path(__file__).resolve().parent.parent
if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

REPO_ROOT = Path(__file__).resolve().parents[4]
CODE_DIR = REPO_ROOT / "code"
for p in (str(REPO_ROOT), str(CODE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from derivation.model import (
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    step,
)
from derivation.iso import canonical, rename
from witness_inversion import extract_isomorphism_witness, verify_isomorphism


def _build_rigid_regime():
    """Build a rigid asymmetric regime with 3 data tokens and 2 forms."""
    r = EMPTY
    r = step(r, AdmitDatum("d0"))
    r = step(r, AdmitDatum("d1"))
    r = step(r, AdmitDatum("d2"))
    r = step(r, AdmitForm(1))  # Form 0: arity 1
    r = step(r, AdmitForm(2))  # Form 1: arity 2
    r = step(r, AdmitInst(0, (0,)))  # Form 0 on d0
    r = step(r, AdmitInst(1, (0, 1)))  # Form 1 on (d0, d1)
    r = step(r, AdmitInst(1, (1, 2)))  # Form 1 on (d1, d2)
    return r


def _build_symmetric_regime():
    """Build a regime with non-trivial transposition symmetry."""
    r = EMPTY
    r = step(r, AdmitDatum("d0"))
    r = step(r, AdmitDatum("d1"))
    r = step(r, AdmitForm(1))
    r = step(r, AdmitInst(0, (0,)))
    r = step(r, AdmitInst(0, (1,)))
    return r


def test_extract_isomorphism_witness_identity():
    r = _build_rigid_regime()
    witness = extract_isomorphism_witness(r, r)
    assert witness is not None
    pi, phi = witness
    assert verify_isomorphism(r, r, pi, phi) is True


def test_extract_isomorphism_witness_permuted():
    r1 = _build_rigid_regime()
    pi_applied = (2, 0, 1)
    phi_applied = (1, 0)
    r2 = rename(r1, pi_applied, phi_applied)

    assert canonical(r1) == canonical(r2)
    witness = extract_isomorphism_witness(r1, r2)
    assert witness is not None
    pi, phi = witness
    assert verify_isomorphism(r1, r2, pi, phi) is True


def test_extract_isomorphism_witness_rigid_recovers_applied():
    r1 = _build_rigid_regime()
    pi_applied = (1, 2, 0)
    phi_applied = (0, 1)
    r2 = rename(r1, pi_applied, phi_applied)

    witness = extract_isomorphism_witness(r1, r2)
    assert witness is not None
    pi, phi = witness
    assert pi == pi_applied
    assert phi == phi_applied
    assert verify_isomorphism(r1, r2, pi, phi) is True


def test_extract_isomorphism_witness_symmetric():
    r1 = _build_symmetric_regime()
    pi_applied = (1, 0)
    phi_applied = (0,)
    r2 = rename(r1, pi_applied, phi_applied)

    assert canonical(r1) == canonical(r2)
    witness = extract_isomorphism_witness(r1, r2)
    assert witness is not None
    pi, phi = witness
    assert verify_isomorphism(r1, r2, pi, phi) is True


def test_extract_isomorphism_witness_non_isomorphic():
    r1 = _build_rigid_regime()
    r2 = _build_symmetric_regime()
    assert canonical(r1) != canonical(r2)
    witness = extract_isomorphism_witness(r1, r2)
    assert witness is None


def test_verify_isomorphism_rejects_invalid_mapping():
    r1 = _build_rigid_regime()
    # Invalid permutation that breaks the asymmetric structure
    invalid_pi = (0, 2, 1)
    invalid_phi = (0, 1)
    assert verify_isomorphism(r1, r1, invalid_pi, invalid_phi) is False


def test_all_permutations_soundness():
    """Exhaustive check across all 6 data permutations for a 3-element regime."""
    r1 = _build_rigid_regime()
    from itertools import permutations

    for pi_perm in permutations(range(3)):
        r_perm = rename(r1, pi_perm, (0, 1))
        witness = extract_isomorphism_witness(r1, r_perm)
        assert witness is not None
        pi_w, phi_w = witness
        assert verify_isomorphism(r1, r_perm, pi_w, phi_w) is True

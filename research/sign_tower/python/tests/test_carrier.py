"""Tests for carrier orbit invariance, parity-blindness, and witness analysis."""

from __future__ import annotations

import pytest
import sys
from pathlib import Path

# Add python module directory to sys.path
PY_DIR = Path(__file__).resolve().parent.parent
if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from carrier import (
    analyze_witness_parity,
    canonical,
    canonical_witness,
    perm_sign,
    rename_regime,
    verify_carrier_orbit_invariance,
)
from derivation.model import (
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    step,
)


def test_perm_sign() -> None:
    assert perm_sign([0, 1, 2]) == 1
    assert perm_sign([1, 0, 2]) == -1
    assert perm_sign([1, 2, 0]) == 1
    assert perm_sign([2, 1, 0]) == -1


def test_carrier_orbit_invariance_rigid() -> None:
    # Build a rigid 3-token regime with distinct roles
    r = step(EMPTY, AdmitDatum("t0"))
    r = step(r, AdmitDatum("t1"))
    r = step(r, AdmitDatum("t2"))
    r = step(r, AdmitForm(2))
    r = step(r, AdmitInst(0, (0, 1)))
    r = step(r, Impose(1, 2))

    assert verify_carrier_orbit_invariance(r) is True


def test_carrier_orbit_invariance_symmetric() -> None:
    # Build a symmetric 3-token regime with no distinguishing instances
    r = step(EMPTY, AdmitDatum("a"))
    r = step(r, AdmitDatum("b"))
    r = step(r, AdmitDatum("c"))

    assert verify_carrier_orbit_invariance(r) is True


def test_rigid_regime_witness_sign_inversion() -> None:
    # Rigid 2-token regime: (0, 1) in instance
    r = step(EMPTY, AdmitDatum("x"))
    r = step(r, AdmitDatum("y"))
    r = step(r, AdmitForm(2))
    r = step(r, AdmitInst(0, (0, 1)))

    analysis = analyze_witness_parity(r)
    results = analysis["results"]
    assert len(results) == 1
    res = results[0]
    assert res["key_match"] is True
    # Rigid regime witness inverts sign under odd transposition
    assert res["witness_inverted"] is True
    assert res["sign_product"] == -1


def test_symmetric_regime_witness_sign_preservation() -> None:
    # Symmetric 2-token regime: unconstrained data tokens
    r = step(EMPTY, AdmitDatum("x"))
    r = step(r, AdmitDatum("y"))

    analysis = analyze_witness_parity(r)
    results = analysis["results"]
    assert len(results) == 1
    res = results[0]
    assert res["key_match"] is True
    # Symmetric regime tie-breaker returns identical permutation, sign product +1
    assert res["sign_product"] == 1

"""Tests for obstruction non-descent certificate, mod-2 Coxeter homology, and M109 checks."""

from __future__ import annotations

import pytest
import sys
from pathlib import Path

PY_DIR = Path(__file__).resolve().parent.parent
if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from carrier import canonical, rename_regime
from derivation.model import EMPTY, AdmitDatum, AdmitForm, AdmitInst, step
from obstruction import (
    capability_cost_coboundary_check,
    evaluate_potential_descent,
    mod2_coxeter_boundary_check,
    rational_maschke_collapse,
)


def test_potential_descent_obstruction() -> None:
    r = step(EMPTY, AdmitDatum("x"))
    r = step(r, AdmitDatum("y"))
    r = step(r, AdmitForm(2))
    r = step(r, AdmitInst(0, (0, 1)))
    k_before = canonical(r)
    k_after = canonical(rename_regime(r, [1, 0]))
    assert k_before == k_after

    def quotient_pot(k: object) -> int:
        return hash(k) % 97

    res = evaluate_potential_descent(quotient_pot, k_before, k_after, omega_sgn_val=1)
    assert res["quotient_keys_coincide"] is True
    assert res["delta0_pullback"] == 0
    assert res["obstruction_difference"] == 1
    assert res["descent_obstructed"] is True


def test_findings_cites_scale_dynamics_for_twins() -> None:
    findings = Path(__file__).resolve().parents[2] / "FINDINGS.md"
    body = findings.read_text(encoding="utf-8")
    assert "ScaleDynamics.twins_differ_at_scale_one" in body
    assert "twins_differ_at_scale_one` in `Limits.lean`" not in body


def test_mod2_coxeter_homology_class() -> None:
    # Mod-2 involution relators and braid relators vanish mod 2
    res = mod2_coxeter_boundary_check()
    assert res["involution_boundary_mod2"] == 0
    assert res["braid_boundary_mod2"] == 0
    assert res["is_mod2_cocycle"] is True
    assert res["w1_nontrivial"] is True
    assert res["cohomology_group"] == "Z_2"


def test_rational_maschke_collapse() -> None:
    # Over Q, involution defect is 2 != 0, so omega_sgn is not a rational cocycle
    res = rational_maschke_collapse()
    assert res["involution_defect"] == 2
    assert res["is_rational_cocycle"] is False
    assert res["h1_rational"] == 0


def test_capability_cost_exact_coboundary() -> None:
    # On commuting squares, capability cost has zero circulation: (c1 + c2) == (c1' + c2')
    squares = [
        (1, 1, 1, 1),
        (0, 1, 1, 0),
        (1, 2, 2, 1),
    ]
    res = capability_cost_coboundary_check(squares)
    assert res["num_squares"] == 3
    assert res["is_exact_coboundary"] is True
    assert res["circulation_vanishes"] is True
    assert all(c == 0 for c in res["circulations"])

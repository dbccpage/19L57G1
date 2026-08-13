"""Tests for the weight-profile mirror."""

from __future__ import annotations

from pathlib import Path

import run_weight_profile
from derivation.weight_profile import (
    all_weights,
    climb_report,
    descends,
    descent_report,
    lift_report,
    mix_sum,
    presents,
    profile_report,
    read_out,
    same_profile,
    same_ray,
    scale,
    signed_mixing_separates,
    sq,
    total,
    unsigned_decoration_determined,
    weight_profile_report,
)


def test_profile_algebra_exhaustive() -> None:
    rep = profile_report(2, 3, 7)
    eq = rep["equivalence"]
    assert isinstance(eq, dict)
    assert eq["refl"] is True
    assert eq["symm"] is True
    assert eq["trans"] is True
    assert rep["scaling_invariant"] is True
    assert rep["classes_are_exactly_rays"] is True
    assert rep["support_preserved"] is True
    assert rep["order_preserved"] is True
    assert rep["total_is_forgotten"] is True
    assert rep["assignments_checked"] == 15


def test_profile_primitives() -> None:
    carrier = (0, 1)
    w = {0: 3, 1: 1}
    assert total(carrier, w) == 4
    assert same_profile(carrier, w, scale(w, 5))
    assert not same_profile(carrier, w, {0: 1, 1: 3})
    assert same_ray(carrier, w, scale(w, 2), 4)
    assert not same_ray(carrier, w, {0: 1, 1: 3}, 6)
    # the total is genuinely forgotten
    assert total(carrier, scale(w, 5)) != total(carrier, w)
    assert len(all_weights(carrier, 2)) == 9


def test_unsigned_lift_adds_nothing_signed_lift_does() -> None:
    rep = lift_report(2, 3)
    assert rep["profile_redundant_for_every_decoration"] is True
    # over UNSIGNED decorations the lift is fully determined
    assert rep["unsigned_decoration_determined"] is True
    assert rep["unsigned_pairs_with_equal_moduli_that_differ"] == 0
    # the extra capacity is exactly the declared sign
    signed = rep["signed_mixing"]
    assert isinstance(signed, dict)
    assert signed["same_modulus_at_each_position"] is True
    assert signed["mixing_separates"] is True
    carrier = (0, 1)
    # a concrete decorated presentation, and the mixing separation
    assert presents(carrier, {0: 2, 1: 1}, {0: 4, 1: 1})
    assert not presents(carrier, {0: 2, 1: 3}, {0: 4, 1: 1})
    assert mix_sum(carrier, {0: 1, 1: 2}) == 9
    assert sq(3) == 9
    assert unsigned_decoration_determined(carrier, 5)
    assert signed_mixing_separates()["mixing_separates"] is True


def test_descent_classification() -> None:
    rep = descent_report(3, 2)
    assert rep["descent_iff_cross_term_zero"] is True
    assert rep["sign_gap_identity"] is True
    # the cross term is the whole obstruction
    assert descends(0, 5, 2)
    assert descends(5, 0, 2)
    assert not descends(1, 1, 2)
    assert read_out(2, 3, 5, 7) == 31


def test_climb_records_what_is_missing() -> None:
    rep = climb_report()
    neg = rep["weights_do_not_force_decoration"]
    assert isinstance(neg, dict)
    assert neg["eA_presents_w"] is True
    assert neg["eB_does_not_present_w"] is True
    assert neg["decorations_differ"] is True
    assert neg["mixing_separates_them"] is True
    imports = rep["imports_required_and_not_discharged"]
    assert isinstance(imports, list) and len(imports) == 3
    status = rep["status"]
    assert isinstance(status, str) and "none is discharged" in status


def test_report_shape_and_bounds() -> None:
    rep = weight_profile_report(2, 3, 3, 3, 2)
    bounds = rep["bounds"]
    assert isinstance(bounds, dict)
    assert bounds["carrier_size"] == 2
    assert bounds["max_weight"] == 3
    split = rep["derived_vs_imported"]
    assert isinstance(split, str)
    assert "DERIVED" in split and "IMPORTED" in split


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    argv = ["--carrier", "2", "--max-weight", "3",
            "--max-decoration", "3", "--coeff-bound", "2",
            "--input-bound", "2"]
    assert run_weight_profile.main(
        ["--artifacts", str(d1)] + argv) == 0
    assert run_weight_profile.main(
        ["--artifacts", str(d2)] + argv) == 0
    assert (d1 / "weight_profile.json").read_bytes() == \
        (d2 / "weight_profile.json").read_bytes()

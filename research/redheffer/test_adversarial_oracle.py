"""Pytest wrapper for Challenger M2 adversarial oracle tests."""

from research.redheffer.adversarial_oracle import (
    test_redheffer_definition_fidelity,
    test_subdiagonal_vanishing,
    test_col_reduction_equivalence_n1_to_n10,
    test_determinants_n1_to_n10,
    test_insert_all_and_leibniz_branch,
    test_extended_horizon_n11_to_n20,
)


def test_conditional_identity_is_scoped_as_transitivity():
    from pathlib import Path
    claims = (Path(__file__).resolve().parent / "CLAIMS.md").read_text(encoding="utf-8")
    lean = (Path(__file__).resolve().parent / "RedhefferObstruction.lean").read_text(encoding="utf-8")
    assert "transitivity of the conjuncts" in claims
    assert "not an independent identity" in lean


def test_adversarial_redheffer_suite():
    test_redheffer_definition_fidelity()
    test_subdiagonal_vanishing()
    test_col_reduction_equivalence_n1_to_n10()
    test_determinants_n1_to_n10()
    test_insert_all_and_leibniz_branch()
    test_extended_horizon_n11_to_n20()

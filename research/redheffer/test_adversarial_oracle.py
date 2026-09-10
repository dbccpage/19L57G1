"""Pytest wrapper for Challenger M2 adversarial oracle tests."""

from research.redheffer.adversarial_oracle import (
    test_redheffer_definition_fidelity,
    test_subdiagonal_vanishing,
    test_col_reduction_equivalence_n1_to_n10,
    test_determinants_n1_to_n10,
    test_insert_all_and_leibniz_branch,
    test_extended_horizon_n11_to_n20,
)


def test_adversarial_redheffer_suite():
    test_redheffer_definition_fidelity()
    test_subdiagonal_vanishing()
    test_col_reduction_equivalence_n1_to_n10()
    test_determinants_n1_to_n10()
    test_insert_all_and_leibniz_branch()
    test_extended_horizon_n11_to_n20()

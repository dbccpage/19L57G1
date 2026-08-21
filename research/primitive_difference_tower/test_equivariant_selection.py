"""Tests for Goal 2's finite equivariant-selection boundary."""

from __future__ import annotations

import unittest

from bridge_contract import Origin, Provenance, two_coordinate_contract
from equivariant_selection import (
    anchored_singleton_choice,
    is_equivariant_singleton_choice,
    no_equivariant_residual_singleton_choice,
    residual_singleton_choices,
)


class EquivariantSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = two_coordinate_contract()

    def test_the_declared_residual_orbit_has_exactly_two_singleton_candidates(self) -> None:
        self.assertEqual(residual_singleton_choices(self.contract), ((0, 1), (1, 0)))

    def test_every_residual_singleton_fails_the_declared_equivariance_test(self) -> None:
        for choice in residual_singleton_choices(self.contract):
            self.assertFalse(is_equivariant_singleton_choice(self.contract, choice))
        self.assertTrue(no_equivariant_residual_singleton_choice(self.contract))

    def test_nonmember_is_not_silently_treated_as_a_selection_candidate(self) -> None:
        with self.assertRaises(ValueError):
            is_equivariant_singleton_choice(self.contract, (0, 0))

    def test_anchored_choice_preserves_the_symmetry_breaking_import(self) -> None:
        selected = anchored_singleton_choice(
            self.contract,
            (1, 0),
            Provenance("left-coordinate-anchor", Origin.ADMITTED),
        )
        self.assertEqual(selected.choice, (1, 0))
        self.assertIs(selected.anchor.origin, Origin.ADMITTED)
        self.assertFalse(is_equivariant_singleton_choice(self.contract, selected.choice))

    def test_declared_or_derived_label_cannot_be_disguised_as_an_anchor(self) -> None:
        with self.assertRaises(ValueError):
            anchored_singleton_choice(
                self.contract,
                (1, 0),
                Provenance("not-an-import", Origin.DECLARED),
            )


if __name__ == "__main__":
    unittest.main()

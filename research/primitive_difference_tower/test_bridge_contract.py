"""Tests for Goal 1's finite, provenance-explicit bridge contract."""

from __future__ import annotations

from dataclasses import replace
import unittest

from bridge_contract import (
    BridgeContract,
    FiniteRepairMap,
    Involution,
    Origin,
    Provenance,
    binary_vector,
    two_coordinate_contract,
)


class BridgeContractTests(unittest.TestCase):
    def test_displayed_contract_exposes_every_input_without_deriving_it(self) -> None:
        contract = two_coordinate_contract()
        self.assertEqual(contract.residual_orbit, ((0, 1), (1, 0)))
        self.assertFalse(contract.residual_is_boundary)
        self.assertTrue(contract.repair_image_is_symmetric)
        self.assertEqual(contract.symmetry.provenance.origin, Origin.DECLARED)
        self.assertEqual(contract.repair.provenance.origin, Origin.DECLARED)
        self.assertEqual(contract.residual_provenance.origin, Origin.DECLARED)

    def test_coordinate_action_is_an_involution_on_cochains(self) -> None:
        action = two_coordinate_contract().symmetry
        vector = (1, 0)
        self.assertEqual(action.apply_vector(vector), (0, 1))
        self.assertEqual(action.apply_vector(action.apply_vector(vector)), vector)
        self.assertEqual(action.point_orbit(0), (0, 1))

    def test_repair_table_decides_membership_only_in_its_declared_domain(self) -> None:
        repair = two_coordinate_contract().repair
        self.assertEqual(repair.boundary((0,)), (0, 0))
        self.assertTrue(repair.is_boundary((1, 1)))
        self.assertFalse(repair.is_boundary((1, 0)))
        with self.assertRaises(ValueError):
            repair.boundary((0, 1))

    def test_invalid_involution_and_nonzero_declared_zero_are_refused(self) -> None:
        with self.assertRaises(ValueError):
            Involution(
                carrier=(0, 1, 2),
                image=(1, 2, 0),
                provenance=Provenance("three-cycle", Origin.DECLARED),
            )
        with self.assertRaises(ValueError):
            FiniteRepairMap(
                potentials=((0,),),
                images=((0, 1),),
                zero=(0, 1),
                provenance=Provenance("bad-zero", Origin.DECLARED),
            )

    def test_contract_rejects_dimension_and_normalization_mismatches(self) -> None:
        contract = two_coordinate_contract()
        with self.assertRaises(ValueError):
            replace(contract, residual=(1,))
        with self.assertRaises(ValueError):
            binary_vector((0, 2))
        with self.assertRaises(ValueError):
            BridgeContract(
                symmetry=contract.symmetry,
                repair=contract.repair,
                residual=(0, 1),
                residual_provenance=Provenance("", Origin.DECLARED),
            )


if __name__ == "__main__":
    unittest.main()

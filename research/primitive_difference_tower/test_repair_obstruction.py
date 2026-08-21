"""Tests for Goal 3's declared-repair obstruction certificate."""

from __future__ import annotations

from dataclasses import replace
import unittest

from bridge_contract import FiniteRepairMap, Origin, Provenance, two_coordinate_contract
from repair_obstruction import certify_declared_repair_obstruction


class DeclaredRepairObstructionTests(unittest.TestCase):
    def test_certificate_checks_every_and_only_declared_repair_input(self) -> None:
        contract = two_coordinate_contract()
        certificate = certify_declared_repair_obstruction(contract)
        self.assertTrue(certificate.excludes_every_declared_potential)
        self.assertEqual(
            certificate.repair_table,
            (((0,), (0, 0)), ((1,), (1, 1))),
        )
        self.assertEqual(certificate.provenance.origin, Origin.COMPUTED)
        self.assertEqual(
            certificate.to_data()["scope"],
            "nonmembership in this declared finite repair table only",
        )

    def test_a_residual_already_in_the_table_is_not_misreported_as_an_obstruction(self) -> None:
        contract = two_coordinate_contract()
        repair = FiniteRepairMap(
            potentials=contract.repair.potentials,
            images=((1, 0), (1, 1)),
            zero=contract.repair.zero,
            provenance=Provenance("changed-table", Origin.DECLARED),
        )
        repaired_contract = replace(contract, repair=repair)
        self.assertTrue(repaired_contract.residual_is_boundary)
        with self.assertRaises(ValueError):
            certify_declared_repair_obstruction(repaired_contract)

    def test_the_certificate_does_not_enlarge_the_declared_repair_domain(self) -> None:
        contract = two_coordinate_contract()
        certificate = certify_declared_repair_obstruction(contract)
        self.assertEqual(len(certificate.repair_table), len(contract.repair.potentials))
        with self.assertRaises(ValueError):
            contract.repair.boundary((0, 1))


if __name__ == "__main__":
    unittest.main()

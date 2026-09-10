"""Candidate census: every row has a named failing clause; the class is inhabited."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import candidates as cd  # noqa: E402


class CensusGuards(unittest.TestCase):
    def test_frozen_census_passes(self) -> None:
        self.assertEqual(cd.census_errors(), ())
        self.assertEqual(tuple(row["id"] for row in cd.CENSUS), cd.REQUIRED_IDS)

    def test_g1_endogenous_label_is_named(self) -> None:
        mutated = cd.mutated_endogenous(cd.CENSUS, "C1")
        errors = cd.census_errors(mutated)
        self.assertTrue(any(e == "E1_GUARD: C1 labelled endogenous" for e in errors), errors)

    def test_g5_narrow_class_is_named(self) -> None:
        mutated = cd.mutated_narrow(cd.CENSUS)
        errors = cd.census_errors(mutated)
        self.assertTrue(any(e.startswith("CLASS_NONVACUITY: missing") for e in errors), errors)
        self.assertTrue(any(e.startswith("CLASS_NARROW:") for e in errors), errors)

    def test_unknown_clause_and_defeated_without_fails(self) -> None:
        bad = (
            {
                "id": "C1",
                "class": "C_reqs",
                "fails": ("EX",),
                "reason": "x",
                "endogenous": False,
                "status": "defeated",
            },
        )
        errors = cd.census_errors(bad)
        self.assertTrue(any("CLAUSE_UNKNOWN:" in e for e in errors), errors)
        empty = (
            {
                "id": "C1",
                "class": "C_reqs",
                "fails": (),
                "reason": "x",
                "endogenous": False,
                "status": "defeated",
            },
        )
        errors = cd.census_errors(empty)
        self.assertTrue(any("CLAUSE_MISSING:" in e for e in errors), errors)
        shaped = (
            {
                "id": "C1",
                "class": "C_reqs",
                "fails": "E1",
                "reason": "x",
                "endogenous": False,
                "status": "defeated",
            },
        )
        errors = cd.census_errors(shaped)
        self.assertTrue(any("CLAUSE_SHAPE:" in e for e in errors), errors)
        dup = cd.CENSUS + (cd.CENSUS[0],)
        errors = cd.census_errors(dup)
        self.assertTrue(any("duplicate ids" in e for e in errors), errors)
        extra = cd.CENSUS + (
            {
                "id": "CZ",
                "class": "C_reqs",
                "fails": ("E1",),
                "reason": "x",
                "endogenous": False,
                "status": "defeated",
            },
        )
        errors = cd.census_errors(extra)
        self.assertTrue(any("extra" in e for e in errors), errors)

    def test_i1_must_stay_open_and_c10_outside(self) -> None:
        # labelling the OPEN remainder endogenous is named by the E1 guard
        labelled = cd.census_errors(cd.mutated_endogenous(cd.CENSUS, "I1"))
        self.assertIn("E1_GUARD: I1 labelled endogenous", labelled)
        # flip status rather than endogenous
        rows = []
        for row in cd.CENSUS:
            copy = dict(row)
            if copy["id"] == "I1":
                copy["status"] = "defeated"
            if copy["id"] == "C10":
                copy["class"] = "C_reqs"
            rows.append(copy)
        errors = cd.census_errors(tuple(rows))
        self.assertTrue(any("OPEN_BOUNDARY:" in e for e in errors), errors)
        self.assertTrue(any("OUTSIDE_CLASS:" in e for e in errors), errors)


class Witnesses(unittest.TestCase):
    def test_c1_is_a_host_pick(self) -> None:
        w = cd.witness_c1()
        self.assertEqual(w["host_function"], "host_next_demand")
        self.assertEqual(w["picked"], [0, 1])
        self.assertEqual(w["reqs"], [])

    def test_c2_impose_is_in_the_history(self) -> None:
        w = cd.witness_c2()
        self.assertTrue(w["last_is_impose"])
        self.assertEqual(w["orbits"], w["impose_events"])
        self.assertIsNone(w["e2_violation"])

    def test_c3_launders_the_supplied_pair(self) -> None:
        w = cd.witness_c3()
        self.assertTrue(w["identical_to_supplied"])
        self.assertEqual(w["supplied_pair"], w["copied_pair"])

    def test_c4_rule_does_not_write_reqs(self) -> None:
        w = cd.witness_c4()
        self.assertEqual(w["reqs"], [])
        self.assertFalse(w["changed_reqs"])
        self.assertEqual(w["rules"], [0])

    def test_c5_host_predicate_does_not_write_reqs(self) -> None:
        w = cd.witness_c5()
        self.assertEqual(w["reqs"], [])
        demanded = w["host_demanded"]
        assert isinstance(demanded, list)
        self.assertGreaterEqual(len(demanded), 1)
        self.assertEqual(w["growth_event"], "AdmitDatum")

    def test_c6_supplying_event_is_impose(self) -> None:
        w = cd.witness_c6()
        self.assertTrue(w["last_is_impose"])
        self.assertEqual(w["reqs"], [[0, 2]])

    def test_c9_pair_is_already_separable(self) -> None:
        w = cd.witness_c9()
        self.assertTrue(w["already_separable"])
        self.assertEqual(w["reqs"], [])

    def test_i1_read_is_not_in_reqs(self) -> None:
        w = cd.witness_i1()
        self.assertEqual(w["read_pairs"], [[0, 1]])
        self.assertFalse(w["in_reqs"])
        self.assertEqual(w["status"], "OPEN")
        self.assertEqual(w["channel"], "instance")

    def test_record_outcome_and_dynamics(self) -> None:
        record = cd.candidate_record()
        self.assertEqual(record["outcome"], "B")
        self.assertEqual(record["guard_errors"], [])
        self.assertIn("not applicable", str(record["dynamics"]))
        census = record["census"]
        assert isinstance(census, list)
        self.assertEqual(len(census), 11)

    def test_census_row_rejects_nontuple_fails(self) -> None:
        with self.assertRaises(TypeError):
            cd._census_row({
                "id": "C1",
                "class": "C_reqs",
                "fails": "E1",
                "reason": "x",
                "endogenous": False,
                "status": "defeated",
            })

    def test_host_next_demand_none_on_empty(self) -> None:
        from derivation.model import EMPTY
        self.assertIsNone(cd.host_next_demand(EMPTY))
        self.assertFalse(cd.host_holds(0, 0))
        self.assertTrue(cd.host_holds(0, 1))


if __name__ == "__main__":
    unittest.main()

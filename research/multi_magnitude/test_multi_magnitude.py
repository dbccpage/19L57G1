"""Unit tests for multi-magnitude carrier and channel separation.

Pins cyclotomic reduction row diversity, closed-walk multi-magnitude generation,
a_only cell realization, and channel separation resolving LP4 unblocking.
AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import carrier as cr  # noqa: E402
import cyclotomic as cyc  # noqa: E402
from separation_proof import generate_lp4_resolution_report  # noqa: E402


class TestMultiMagnitude(unittest.TestCase):
    def test_cyclotomic_reduction_n3_refusal(self) -> None:
        """Carrier V6 at n=3 produces row [2, -1, -1] with two magnitudes (1 and 2),
        which cancels to zero and refuses a pairing certificate."""
        row = cyc.row_family_v6(3)
        self.assertEqual(row, [2, -1, -1])
        self.assertEqual(sum(row), 0)

        dec = cyc.certificate_decision(row)
        self.assertEqual(dec["magnitudes"], [1, 2])
        self.assertEqual(dec["distinct_magnitudes"], 2)
        self.assertFalse(dec["neg_dominated"])
        self.assertFalse(dec["pos_dominated"])
        self.assertFalse(dec["certificate_exists"])

    def test_cyclotomic_census_statistics(self) -> None:
        """Across n <= 60, V6 yields 54 diverse row families and 29 refusals."""
        census = cyc.cyclotomic_census(limit=60)
        self.assertEqual(census["diverse_families"], 54)
        self.assertEqual(len(census["distinct_magnitudes_seen"]), 25)
        self.assertEqual(census["refusals"], 29)

    def test_multi_magnitude_walk_weights(self) -> None:
        """Closed walks on cyclotomic-weighted presentations produce >= 2
        operational magnitudes and cause Channel (b) refusal."""
        rows = cr.build_multi_magnitude_census()
        cyc_rows = [r for r in rows if "cyc3" in str(r["name"])]
        self.assertGreater(len(cyc_rows), 0)
        for r in cyc_rows:
            mags = r["walk_magnitudes"]
            assert isinstance(mags, list)
            self.assertGreaterEqual(len(mags), 2)
            self.assertIn(1, mags)
            self.assertIn(2, mags)
            cert = r["channel_b"]
            assert isinstance(cert, dict)
            self.assertFalse(cert["certificate"])

    def test_channel_separation_and_lp4_resolution(self) -> None:
        """The channel table realizes a_only and b_only cells, achieving
        CHANNELS_SEPARATED and unblocking LP4."""
        rows = cr.build_multi_magnitude_census()
        verdict = cr.separation_verdict(rows)

        self.assertTrue(verdict["separated"])
        self.assertEqual(verdict["terminal"], "CHANNELS_SEPARATED")
        self.assertFalse(verdict["magnitude_degeneracy"])
        self.assertTrue(verdict["has_a_only"])
        self.assertTrue(verdict["has_b_only"])

        cells = verdict["cells"]
        self.assertGreater(cells.get("a_only", 0), 0)
        self.assertGreater(cells.get("b_only", 0), 0)
        self.assertGreater(cells.get("both", 0), 0)
        self.assertGreater(cells.get("neither", 0), 0)

    def test_integrated_lp4_report(self) -> None:
        rep = generate_lp4_resolution_report()
        self.assertEqual(rep["status"], "LP4_RESOLVED_AND_UNBLOCKED")
        self.assertTrue(
            rep["multi_magnitude_resolution"]["single_magnitude_degeneracy_broken"]
        )
        self.assertEqual(
            rep["multi_magnitude_resolution"]["channel_table"]["terminal"],
            "CHANNELS_SEPARATED",
        )


if __name__ == "__main__":
    unittest.main()

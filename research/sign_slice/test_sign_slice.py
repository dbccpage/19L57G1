"""Positive and negative tests for the sign_slice run.

The negative tests are the required failure modes: a predicate that
sections the two-label square, obstructs the open chain, or accepts
twisted-equals-total as sufficient fails this suite.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

import occ_relabel
import run_sign_slice
import slice_set
from cone_section import closed_walks, cone_section, twisted_and_total
from genpres import identity, is_genpres, iso_key, make, mover_family

HERE = Path(__file__).resolve().parent


class GrammarTests(unittest.TestCase):
    def test_weightingless_tuple_is_refused(self) -> None:
        ok, why = is_genpres([0, 1], [(0, 1, (0, 1))], 2, None)
        self.assertFalse(ok)
        self.assertIn("weighting", why)

    def test_object_bound_is_enforced_on_the_census(self) -> None:
        for _name, p in slice_set.members():
            self.assertLessEqual(len(p.objects), slice_set.OBJECT_BOUND)

    def test_iso_key_forgets_tokens_but_not_weighting(self) -> None:
        a = make([0, 1], [(0, 1, (1, 0))], 2, [1])
        b = make([5, 9], [(5, 9, (1, 0))], 2, [1])
        c = make([0, 1], [(0, 1, (1, 0))], 2, [-1])
        self.assertEqual(iso_key(a), iso_key(b))
        self.assertNotEqual(iso_key(a), iso_key(c))


class PredicateTests(unittest.TestCase):
    def test_chain_is_sectioned_and_square_star_are_not(self) -> None:
        ms = dict(slice_set.members())
        self.assertTrue(cone_section(ms["chain_P4_occ2"]))
        self.assertFalse(cone_section(ms["square_2x2_occ2"]))
        self.assertFalse(cone_section(ms["star_K13_occ2"]))

    def test_negative_twisted_equals_total_is_not_sufficient(self) -> None:
        ms = dict(slice_set.members())
        square = ms["square_2x2_occ2"]
        mover = None
        for transport, _amp in closed_walks(square, 0, 6):
            if transport != identity(square.fibre):
                mover = transport
                break
        assert mover is not None
        twisted, total, _ = twisted_and_total([(mover, 1), (mover, -1)], (0, 1))
        self.assertEqual(twisted, total)
        self.assertFalse(cone_section(square))

    def test_pointwise_relabels_never_move_the_class(self) -> None:
        ms = dict(slice_set.members())
        for name in ("chain_P4_occ2", "square_2x2_occ2"):
            p = ms[name]
            hops = occ_relabel.undirected_hops(p)
            base = cone_section(p)
            for assignment in occ_relabel.pointwise_assignments(p, hops):
                q = occ_relabel.relabelled(p, hops, assignment, (1, 0))
                self.assertEqual(cone_section(q), base)


class CensusTests(unittest.TestCase):
    def test_partition_matches_the_receipt(self) -> None:
        import json

        receipt = json.loads((HERE / "receipts" / "sign_slice.json").read_text("ascii"))
        rows = slice_set.census()
        self.assertEqual(len(rows), receipt["phase_3_census"]["count"])
        sectioned = sorted(str(r["name"]) for r in rows if r["sectioned"])
        self.assertEqual(sectioned, sorted(receipt["phase_3_census"]["sectioned"]))

    def test_sign_pair_agrees_on_the_predicate_and_mixing_separates(self) -> None:
        ms = dict(slice_set.members())
        pos = ms["signed_square_pos"]
        neg = ms["signed_square_neg"]
        self.assertEqual(cone_section(pos), cone_section(neg))
        self.assertEqual(slice_set.squares(pos), slice_set.squares(neg))
        self.assertNotEqual(slice_set.mixing(pos, pos), slice_set.mixing(pos, neg))


class OccRelabelTests(unittest.TestCase):
    def test_exhaustion_moves_the_square_with_price_two(self) -> None:
        ms = dict(slice_set.members())
        result = occ_relabel.exhaust(ms["square_2x2_occ2"], (1, 0))
        self.assertGreater(int(str(result["flip_count"])), 0)
        self.assertEqual(result["pointwise_moves"], 0)
        self.assertEqual(result["price_min_slots_from_pointwise"], 2)

    def test_witness_is_not_pointwise(self) -> None:
        ms = dict(slice_set.members())
        p = ms["square_2x2_occ2"]
        hops = occ_relabel.undirected_hops(p)
        result = occ_relabel.exhaust(p, (1, 0))
        cheapest = result["cheapest_flip"]
        assert isinstance(cheapest, list)
        pointwise = set(occ_relabel.pointwise_assignments(p, hops))
        self.assertNotIn(tuple(cheapest), pointwise)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically(self) -> None:
        committed = (HERE / "receipts" / "sign_slice.json").read_bytes()
        # full replay through the runner into a scratch directory
        scratch = HERE / "receipts_replay"
        try:
            self.assertEqual(run_sign_slice.main(["--out", str(scratch)]), 0)
            replayed = (scratch / "sign_slice.json").read_bytes()
            self.assertEqual(committed, replayed)
        finally:
            for f in scratch.glob("*"):
                f.unlink()
            if scratch.exists():
                scratch.rmdir()


if __name__ == "__main__":
    unittest.main()

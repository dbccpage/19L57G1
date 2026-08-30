"""Tests for the two-object fixture computation and receipt replay."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import json
import tempfile
import unittest
from pathlib import Path

import embedding as emb
import run_embedding as runner

TREE = Path(__file__).resolve().parent
RECEIPT = TREE / "receipts" / "embedding.json"


class FixtureTests(unittest.TestCase):
    def test_obstructed_uses_negIso_and_has_no_section(self) -> None:
        arrs = emb.arrows_obstructed()
        hom = emb.hom_table(arrs)
        self.assertTrue(emb.uses_neg(arrs))
        self.assertTrue(emb.fixed_point_free_on_carrier())
        self.assertTrue(emb.hom_inhabited(hom))
        occupancy = emb.hom_occupancy(hom)
        self.assertEqual(occupancy["a->a"], 1)
        self.assertEqual(occupancy["a->b"], 1)
        self.assertEqual(occupancy["b->a"], 1)
        self.assertEqual(occupancy["b->b"], 1)
        self.assertFalse(emb.has_natural_section(arrs))
        self.assertFalse(emb.has_h_natural_section(hom))

    def test_clean_has_a_natural_section_and_inhabited_hom(self) -> None:
        arrs = emb.arrows_clean()
        hom = emb.hom_table(arrs)
        self.assertFalse(emb.uses_neg(arrs))
        self.assertTrue(emb.hom_inhabited(hom))
        self.assertTrue(emb.has_natural_section(arrs))
        self.assertTrue(emb.has_h_natural_section(hom))
        constant: dict[emb.Obj, emb.Pair] = {"a": (False, True), "b": (False, True)}
        self.assertTrue(emb.assignment_natural(arrs, constant))
        self.assertTrue(emb.assignment_h_natural(hom, constant))

    def test_empty_arr_is_vacuously_natural_on_both_sides(self) -> None:
        empty: tuple[emb.Arrow, ...] = ()
        hom = emb.hom_table(empty)
        self.assertFalse(emb.hom_inhabited(hom))
        self.assertTrue(emb.has_natural_section(empty))
        self.assertTrue(emb.has_h_natural_section(hom))

    def test_empty_hom_with_obstructed_arr_makes_the_sides_disagree(self) -> None:
        arrs = emb.arrows_obstructed()
        hom = emb.empty_hom()
        self.assertFalse(emb.has_natural_section(arrs))
        self.assertTrue(emb.has_h_natural_section(hom))
        self.assertNotEqual(
            emb.has_natural_section(arrs), emb.has_h_natural_section(hom)
        )

    def test_report_iff_on_both_fixtures(self) -> None:
        r = emb.report()
        self.assertTrue(r["iff_on_fixtures"])
        obstructed = r["obstructed"]
        clean = r["clean"]
        assert isinstance(obstructed, dict) and isinstance(clean, dict)
        self.assertEqual(obstructed["flat_natural_section"], obstructed["h_natural_section"])
        self.assertEqual(clean["flat_natural_section"], clean["h_natural_section"])
        self.assertFalse(obstructed["flat_natural_section"])
        self.assertFalse(obstructed["h_natural_section"])
        self.assertTrue(clean["flat_natural_section"])
        self.assertTrue(clean["h_natural_section"])
        self.assertTrue(obstructed["uses_negIso"])
        self.assertTrue(obstructed["negIso_fixed_point_free_on_carrier"])
        self.assertEqual(
            r["hom_construction"], "{ f : F.Arr // F.src f = a ∧ F.tgt f = b }"
        )


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "embedding.json").read_bytes()
            two = (b / "embedding.json").read_bytes()
            self.assertEqual(one, two)
            self.assertEqual(one, runner.render())
            committed = RECEIPT.read_bytes()
            self.assertEqual(one, committed)

    def test_receipt_that_does_not_replay_is_refused(self) -> None:
        live = json.loads(RECEIPT.read_text(encoding="ascii"))
        live["tamper"] = True
        self.assertNotEqual(
            json.dumps(live, indent=2, sort_keys=True, ensure_ascii=True).encode("ascii")
            + b"\n",
            runner.render(),
        )


class SealedWriteTests(unittest.TestCase):
    def test_assert_inside_tree_refuses_sealed_prefixes(self) -> None:
        repo = TREE.parents[1]
        for sealed in (
            repo / "prompt" / "x.md",
            repo / "paper" / "x.md",
            repo / "code" / "x.py",
            repo / "lean4" / "Derivation" / "X.lean",
            repo / "artifacts" / "x.json",
        ):
            with self.assertRaisesRegex(ValueError, "refusing to write outside"):
                runner.assert_inside_tree(sealed)
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "r.json"
            with self.assertRaisesRegex(ValueError, "refusing to write outside"):
                runner.assert_inside_tree(target)
        self.assertTrue(
            runner.assert_inside_tree(TREE / "receipts" / "x.json").is_relative_to(TREE)
        )

    def test_runner_refuses_an_outside_out_dir(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            result = runner.main(["--out", outside])
            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()

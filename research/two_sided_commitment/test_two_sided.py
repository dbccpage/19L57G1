"""Tests for the two-sided commitment rung.

Run from this directory: ``python -m unittest discover -s . -p "test_*.py"``.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from two_sided import (  # noqa: E402
    APART,
    COMMITMENTS,
    FREE,
    SAME,
    Answer,
    Declare,
    TState,
    certify,
    closure_targets,
    commitment_named,
    demands,
    genesis_history,
    key_of,
    min_responses,
    response_valid,
    sealed_readings,
    ts_replay,
    ts_step,
)
from derivation.candidates import Bounds, NewForm, NewInst, NewRuleAll, iter_full_deltas  # noqa: E402
from derivation.iso import rename  # noqa: E402
from derivation.model import AdmissionError, AdmitDatum, Regime, Supply  # noqa: E402

FROZEN_PROMPT = "d96cab6efc4c89ee99dda4e7f911325e5e14b4b554444943834e0e1e914a028d"
FROZEN_PREDICTIONS = "b9dea8cea62749321422da6b1ba01f76dc1af16624d9e8d5ea44e6338f46e333"
BOUNDS = Bounds(max_items=2, max_arity=2)


def _sha(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def _reading(name: str) -> object:
    for rd in sealed_readings():
        if rd.name == name:
            return rd
    raise AssertionError(name)


def _genesis(reading: str, commitment: str) -> TState:
    rd = _reading(reading)
    return ts_replay(genesis_history(rd, commitment_named(commitment)))  # type: ignore[arg-type]


class FreezeTests(unittest.TestCase):
    def test_prompt_is_frozen(self) -> None:
        self.assertEqual(_sha("PROMPT.md"), FROZEN_PROMPT)

    def test_predictions_are_frozen(self) -> None:
        self.assertEqual(_sha("PREDICTIONS.md"), FROZEN_PREDICTIONS)

    def test_prompt_states_no_number(self) -> None:
        text = (HERE / "PROMPT.md").read_text(encoding="utf-8")
        body = re.sub(r"^## [0-9]+\.", "##", text.replace("mu1", "").replace("mu2", ""), flags=re.M)
        self.assertIsNone(re.search(r"[0-9]", body))

    def test_frozen_texts_are_lf(self) -> None:
        for name in ("PROMPT.md", "PREDICTIONS.md"):
            self.assertNotIn(b"\r", (HERE / name).read_bytes(), name)


class CommitmentTests(unittest.TestCase):
    def test_five_commitments_declared_in_prompt_order(self) -> None:
        self.assertEqual(
            [c.name for c in COMMITMENTS],
            ["total_apart", "total_same", "parity", "residue_three", "chain"],
        )

    def test_labels_are_symmetric_and_in_range(self) -> None:
        for c in COMMITMENTS:
            for i in range(6):
                for j in range(6):
                    if i == j:
                        continue
                    self.assertEqual(c.label(i, j), c.label(j, i))
                    self.assertIn(c.label(i, j), (APART, SAME, FREE))

    def test_parity_and_residue_and_chain_examples(self) -> None:
        parity = commitment_named("parity")
        self.assertEqual(parity.label(0, 2), SAME)
        self.assertEqual(parity.label(0, 1), APART)
        residue = commitment_named("residue_three")
        self.assertEqual(residue.label(0, 3), SAME)
        self.assertEqual(residue.label(1, 3), APART)
        chain = commitment_named("chain")
        self.assertEqual(chain.label(2, 3), APART)
        self.assertEqual(chain.label(0, 2), FREE)


class ReplayTests(unittest.TestCase):
    def test_declare_is_once(self) -> None:
        s = _genesis("L", "parity")
        with self.assertRaises(AdmissionError):
            ts_step(s, Declare("parity"))

    def test_answer_changes_nothing(self) -> None:
        s = _genesis("F", "parity")
        self.assertEqual(ts_step(s, Answer(APART, 0, 1)), s)

    def test_genesis_replays_and_certifies(self) -> None:
        for rd in sealed_readings():
            for c in COMMITMENTS:
                h = genesis_history(rd, c)
                self.assertTrue(certify(h, ts_replay(h)))

    def test_growth_is_the_sealed_supply_and_admission(self) -> None:
        s = _genesis("L", "total_apart")
        n = s.regime.n_data()
        t = ts_replay((Supply(f"g{n}"), AdmitDatum(f"g{n}")), s)
        self.assertEqual(t.regime.n_data(), n + 1)
        self.assertEqual(t.commitment, "total_apart")


class DemandTests(unittest.TestCase):
    def test_total_apart_demands_every_pair_at_genesis(self) -> None:
        self.assertEqual([p for _, p in demands(_genesis("L", "total_apart"))], [(0, 1)])
        self.assertEqual(
            [p for _, p in demands(_genesis("F", "total_apart"))], [(0, 1), (0, 2), (1, 2)]
        )

    def test_total_same_demands_nothing_at_genesis(self) -> None:
        self.assertEqual(demands(_genesis("F", "total_same")), ())

    def test_parity_at_three_data_demands_the_two_apart_pairs_only(self) -> None:
        ds = demands(_genesis("F", "parity"))
        self.assertEqual(ds, ((APART, (0, 1)), (APART, (1, 2))))

    def test_closure_targets_are_one_per_orbit(self) -> None:
        self.assertEqual(closure_targets(_genesis("F", "total_apart")), ((APART, (0, 1)),))
        self.assertEqual(closure_targets(_genesis("F", "parity")), ((APART, (0, 1)),))


class ValidityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.s = _genesis("L", "total_apart")

    def test_no_single_item_separates_from_the_bare_genesis(self) -> None:
        for delta in iter_full_deltas(self.s.regime, 1, BOUNDS):
            self.assertFalse(response_valid(self.s, (APART, (0, 1)), delta), delta)

    def test_form_plus_mark_is_a_valid_two_item_response(self) -> None:
        self.assertTrue(response_valid(self.s, (APART, (0, 1)), (NewForm(1), NewInst(0, (0,)))))

    def test_minimum_is_two_items_with_a_fresh_form(self) -> None:
        mr = min_responses(self.s, (APART, (0, 1)), "mu1", BOUNDS)
        assert mr is not None
        self.assertEqual(mr.cost[0], 2)
        for delta in mr.deltas:
            self.assertTrue(any(isinstance(it, NewForm) for it in delta))

    def test_regress_of_an_honoured_pair_is_refused(self) -> None:
        """Under parity at three data with a mark on datum 1 honouring
        (0,1) and (1,2), a rule on the form would collapse everything and
        regress both; the rule is therefore not a valid answer to anything."""
        base = _genesis("F", "parity")
        marked = TState(
            Regime(base.regime.data, (1,), frozenset({(0, (1,))}), frozenset(), frozenset()),
            "parity",
        )
        self.assertEqual(demands(marked), ())
        grown = ts_replay((Supply("g3"), AdmitDatum("g3")), marked)
        ds = demands(grown)
        self.assertIn((SAME, (1, 3)), ds)
        self.assertFalse(response_valid(grown, (SAME, (1, 3)), (NewRuleAll(0),)))
        self.assertTrue(response_valid(grown, (SAME, (1, 3)), (NewInst(0, (3,)),)))


class IsomorphismTests(unittest.TestCase):
    def test_key_respects_the_commitment_labels(self) -> None:
        """Swapping data 0 and 2 preserves parity labels; swapping 0 and 1
        does not, so the first renaming keeps the key and the second may not."""
        base = _genesis("F", "parity")
        marked = TState(
            Regime(base.regime.data, (1,), frozenset({(0, (0,))}), frozenset(), frozenset()),
            "parity",
        )
        swapped02 = TState(rename(marked.regime, (2, 1, 0), (0,)), "parity")
        self.assertEqual(key_of(marked), key_of(swapped02))
        swapped01 = TState(rename(marked.regime, (1, 0, 2), (0,)), "parity")
        self.assertNotEqual(key_of(marked), key_of(swapped01))


class ReceiptTests(unittest.TestCase):
    def test_receipts_regenerate_identically(self) -> None:
        from run_two_sided import build_all, split

        from derivation.export import dumps_deterministic, read_json_gz

        committed = (HERE / "receipts" / "two_sided_commitment.json").read_bytes()
        self.assertNotIn(b"\r", committed)
        summary, full = split(build_all())
        self.assertEqual(dumps_deterministic(summary), committed)
        stored = read_json_gz(HERE / "receipts" / "full" / "two_sided_commitment_full.json.gz")
        self.assertEqual(stored, full)
        recorded = summary["full_export"]
        assert isinstance(recorded, dict)
        self.assertEqual(hashlib.sha256(dumps_deterministic(full)).hexdigest(), recorded["sha256_uncompressed"])

    def test_receipt_records_the_frozen_hashes(self) -> None:
        import json

        payload = json.loads((HERE / "receipts" / "two_sided_commitment.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["prompt_sha256"], FROZEN_PROMPT)
        self.assertEqual(payload["predictions_sha256"], FROZEN_PREDICTIONS)
        self.assertEqual(sorted(payload["predictions_scored"]), sorted(f"Q{i}" for i in range(1, 9)))
        self.assertEqual(payload["summary"]["flip_events_in_grammar"], 0)


if __name__ == "__main__":
    unittest.main()

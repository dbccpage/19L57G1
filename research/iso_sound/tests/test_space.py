"""Closed-form size, bound membership, and seed-corpus agreement."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import corpus  # noqa: E402
import hunt  # noqa: E402
import space  # noqa: E402
from derivation.iso import CanonKey, canonical  # noqa: E402


class Space(unittest.TestCase):
    def test_closed_form_matches_enumeration(self) -> None:
        self.assertEqual(space.count_space(), 56020)
        self.assertEqual(sum(1 for _ in space.enumerate_regimes()), 56020)

    def test_comb_edges(self) -> None:
        self.assertEqual(space._comb(5, -1), 0)
        self.assertEqual(space._comb(5, 6), 0)
        self.assertEqual(space._comb(5, 0), 1)
        self.assertEqual(space._comb(5, 5), 1)
        self.assertEqual(space._comb(5, 2), 10)

    def test_empty_and_max_form_signatures(self) -> None:
        sigs = space.form_signatures()
        self.assertIn((), sigs)
        self.assertIn((2, 2), sigs)
        self.assertEqual(space.instance_slots(0, (1,)), ())
        self.assertEqual(space.req_slots(1), ())


class Corpus(unittest.TestCase):
    def test_seven_regimes_sit_in_the_bound_and_agree(self) -> None:
        record = corpus.corpus_agreement()
        self.assertEqual(record["size"], 7)
        self.assertTrue(record["in_bounds"])
        self.assertTrue(record["agreement"])
        self.assertEqual(record["disagreements"], 0)
        self.assertEqual(len(corpus.seed_corpus()), 7)


class SplitDetector(unittest.TestCase):
    def test_constant_group_is_not_a_split(self) -> None:
        key: CanonKey = (1, (1,), ((0, (0,)),), (), ())
        groups = {key: [0, 1]}
        labels = [key, key]
        self.assertIsNone(hunt.first_split(groups, labels))

    def test_injected_split_is_named(self) -> None:
        k1: CanonKey = (1, (1,), ((0, (0,)),), (), ())
        k2: CanonKey = (1, (1,), ((0, (1,)),), (), ())
        groups = {k1: [0, 1]}
        labels = [k1, k2]
        split = hunt.first_split(groups, labels)
        self.assertEqual(split, (0, 1))

    def test_claim_errors_require_open_soundness(self) -> None:
        record = {
            "general_soundness": "PROVED",
            "agreement": True,
            "falsifier_count": 0,
            "seed_corpus": {"agreement": True},
        }
        errors = hunt.claim_errors(record)
        self.assertIn("SOUNDNESS_GUARD: general_soundness is not OPEN", errors)

    def test_encode_and_mocked_falsifier_path(self) -> None:
        from unittest.mock import patch
        r = corpus.seed_corpus()[0]
        encoded = hunt._encode(canonical(r))
        self.assertEqual(encoded[0], r.n_data())
        rec = space.regime_record(r)
        self.assertEqual(rec["n_data"], r.n_data())
        with patch("hunt.enumerate_regimes", return_value=iter(corpus.seed_corpus()[:2])):
            with patch("hunt.count_space", return_value=2):
                with patch("hunt.first_split", return_value=(0, 1)):
                    record = hunt.hunt()
        self.assertEqual(record["falsifier_count"], 1)
        found = record["falsifiers"]
        assert isinstance(found, list)
        self.assertEqual(len(found), 1)
        with patch("hunt.enumerate_regimes", return_value=iter(corpus.seed_corpus()[:1])):
            with patch("hunt.count_space", return_value=99):
                with self.assertRaises(RuntimeError):
                    hunt.hunt()

    def test_corpus_disagreement_counter(self) -> None:
        from unittest.mock import patch
        with patch("corpus.canonical", return_value=(0, (), (), (), ())):
            with patch("corpus.canonical_bruteforce", side_effect=lambda r: (id(r), (), (), (), ())):
                record = corpus.corpus_agreement()
        self.assertFalse(record["agreement"])
        disagreed = record["disagreements"]
        assert isinstance(disagreed, int)
        self.assertGreater(disagreed, 0)

    def test_claim_errors_catch_agreement_lies(self) -> None:
        errors = hunt.claim_errors({
            "general_soundness": "OPEN",
            "agreement": True,
            "falsifier_count": 1,
            "seed_corpus": {"agreement": True},
        })
        self.assertTrue(any("AGREEMENT_GUARD:" in e for e in errors), errors)
        errors = hunt.claim_errors({
            "general_soundness": "OPEN",
            "agreement": False,
            "falsifier_count": 0,
            "seed_corpus": {"agreement": False},
        })
        self.assertTrue(any("AGREEMENT_GUARD:" in e for e in errors), errors)
        self.assertTrue(any("CORPUS_GUARD:" in e for e in errors), errors)

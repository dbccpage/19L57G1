"""test_hunt_cl_iso.py — Test suite for standalone CL-ISO-SOUND hunt runner.

Validates:
1. Smoke execution over seed corpus and bounded structures.
2. Injected falsification detection (verifying that discrepancies are caught).
3. Receipt honesty guards and schema compliance.
4. Full census agreement over the declared 56,020 regimes.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

# Ensure imports resolve
ROOT = Path(__file__).resolve().parents[2]
CODE_DIR = ROOT / "code"
RESEARCH_DIR = ROOT / "research"
ISO_SOUND_DIR = RESEARCH_DIR / "iso_sound"

for p in (str(ROOT), str(CODE_DIR), str(RESEARCH_DIR), str(ISO_SOUND_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import hunt_cl_iso as hci  # type: ignore[import-not-found]  # noqa: E402
from corpus import seed_corpus  # type: ignore[import-not-found]  # noqa: E402
from space import DEEP_BOUNDS, count_space  # type: ignore[import-not-found]  # noqa: E402
from derivation.model import Regime  # noqa: E402
from derivation.iso import canonical, canonical_bruteforce, rename  # noqa: E402


class TestHuntClIso(unittest.TestCase):
    """Unit and integration tests for hunt_cl_iso runner."""

    def test_seed_corpus_smoke_census(self) -> None:
        """Smoke run over the 7 seed corpus regimes produces 5 classes, 0 falsifiers."""
        corpus = seed_corpus()
        receipt = hci.run_census(regimes=corpus, check_corpus=True)
        self.assertEqual(receipt["regime_count"], 7)
        self.assertEqual(receipt["refined_class_count"], 5)
        self.assertEqual(receipt["brute_class_count"], 5)
        self.assertTrue(receipt["agreement"])
        self.assertEqual(receipt["falsifier_count"], 0)
        self.assertEqual(receipt["falsifiers"], [])
        self.assertEqual(receipt["general_soundness"], "OPEN")
        self.assertEqual(receipt["authority_effect"], "None")
        errors = hci.verify_receipt_honesty(receipt)
        self.assertEqual(errors, [])

    def test_first_split_detects_injected_discrepancy(self) -> None:
        """Adversarial check: first_split must detect when partitions disagree."""
        # Define dummy canon keys
        k0 = (2, (1,), (((0, (0,))),), (), ())
        k1 = (2, (1,), (((0, (1,))),), (), ())
        k2 = (2, (2,), (((0, (0, 1))),), (), ())

        # Groups where regime 0 and 1 are grouped together under partition A
        groups = {k0: [0, 1], k2: [2]}
        # But in partition B, regime 0 gets k0 and regime 1 gets k1
        labels = [k0, k1, k2]

        split = hci.first_split(groups, labels)
        self.assertIsNotNone(split)
        self.assertEqual(split, (0, 1))

    def test_first_split_returns_none_when_partitions_agree(self) -> None:
        """first_split returns None when all groups map to constant labels."""
        k0 = (2, (1,), (), (), ())
        k1 = (2, (2,), (), (), ())
        groups = {k0: [0, 1], k1: [2, 3]}
        labels = [k0, k0, k1, k1]
        self.assertIsNone(hci.first_split(groups, labels))

    def test_honesty_guards_reject_corrupted_claims(self) -> None:
        """Honesty guards fail closed on false claims or missing caveats."""
        valid_receipt = {
            "schema": "iso-sound-hunt-v1",
            "authority_effect": "None",
            "general_soundness": "OPEN",
            "agreement": True,
            "falsifier_count": 0,
            "seed_corpus": {"agreement": True},
        }
        self.assertEqual(hci.verify_receipt_honesty(valid_receipt), [])

        # Corrupt 1: claim general soundness is PROVED
        c1 = dict(valid_receipt, general_soundness="PROVED")
        self.assertIn("SOUNDNESS_GUARD: general_soundness is not OPEN", hci.verify_receipt_honesty(c1))

        # Corrupt 2: non-None authority effect
        c2 = dict(valid_receipt, authority_effect="Normative")
        self.assertIn("AUTHORITY_GUARD: authority_effect is not None", hci.verify_receipt_honesty(c2))

        # Corrupt 3: agreement True but non-zero falsifiers
        c3 = dict(valid_receipt, agreement=True, falsifier_count=1)
        self.assertIn("AGREEMENT_GUARD: agreement true with non-zero falsifier count", hci.verify_receipt_honesty(c3))

        # Corrupt 4: agreement False but zero falsifiers
        c4 = dict(valid_receipt, agreement=False, falsifier_count=0)
        self.assertIn("AGREEMENT_GUARD: agreement false with zero falsifiers", hci.verify_receipt_honesty(c4))

    def test_encode_key_format(self) -> None:
        """CanonKey encodes to JSON-serializable list without errors."""
        key = (3, (1, 2), ((0, (1,)), (1, (1, 2))), (0,), ((1, 2),))
        encoded = hci.encode_key(key)
        self.assertEqual(encoded[0], 3)
        self.assertEqual(encoded[1], [1, 2])
        self.assertEqual(encoded[3], [0])
        self.assertEqual(encoded[4], [[1, 2]])
        # Must serialize cleanly to JSON
        json_str = json.dumps(encoded)
        self.assertIsInstance(json_str, str)

    def test_full_census_reproducibility(self) -> None:
        """The full census evaluates exactly 56,020 regimes into 5,698 classes with 0 falsifiers."""
        self.assertEqual(count_space(), 56020)
        receipt = hci.run_census(check_corpus=True)
        self.assertEqual(receipt["regime_count"], 56020)
        self.assertEqual(receipt["refined_class_count"], 5698)
        self.assertEqual(receipt["brute_class_count"], 5698)
        self.assertTrue(receipt["agreement"])
        self.assertEqual(receipt["falsifier_count"], 0)
        self.assertEqual(receipt["falsifiers"], [])
        self.assertEqual(receipt["general_soundness"], "OPEN")
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertTrue(receipt["seed_corpus"]["agreement"])
        self.assertEqual(hci.verify_receipt_honesty(receipt), [])

    def test_ternary_relation_isomorphism(self) -> None:
        """Ternary relation regimes (arity=3) preserve partition and canonical isomorphism."""
        # Regime with 2 ternary instances and 1 requirement
        r1 = Regime(
            data=("d0", "d1", "d2"),
            forms=(3,),
            insts=frozenset([(0, (0, 1, 2)), (0, (2, 1, 0))]),
            rules=frozenset(),
            reqs=frozenset([(0, 1)]),
        )
        # Permute data: pi = (1, 2, 0), phi = (0,)
        r2 = rename(r1, (1, 2, 0), (0,))
        self.assertEqual(canonical(r1), canonical(r2))
        self.assertEqual(canonical_bruteforce(r1), canonical_bruteforce(r2))

        # Distinct non-isomorphic ternary regime
        r3 = Regime(
            data=("d0", "d1", "d2"),
            forms=(3,),
            insts=frozenset([(0, (0, 0, 1)), (0, (1, 2, 2))]),
            rules=frozenset(),
            reqs=frozenset([(0, 1)]),
        )
        self.assertNotEqual(canonical(r1), canonical(r3))
        self.assertNotEqual(canonical_bruteforce(r1), canonical_bruteforce(r3))

    def test_instance_scaling_ge_4(self) -> None:
        """Regimes with |insts| >= 4 correctly evaluate under refined and brute-force canonicalization."""
        r4 = Regime(
            data=("d0", "d1", "d2"),
            forms=(3,),
            insts=frozenset([(0, (0, 1, 2)), (0, (1, 2, 0)), (0, (2, 0, 1)), (0, (0, 0, 0))]),
            rules=frozenset([0]),
            reqs=frozenset([(0, 1), (1, 2)]),
        )
        self.assertEqual(len(r4.insts), 4)
        r4_iso = rename(r4, (2, 0, 1), (0,))
        self.assertEqual(canonical(r4), canonical(r4_iso))
        self.assertEqual(canonical_bruteforce(r4), canonical_bruteforce(r4_iso))

        # Also test 5 instances with multiple forms
        r5 = Regime(
            data=("d0", "d1", "d2"),
            forms=(2, 3),
            insts=frozenset([
                (0, (0, 1)),
                (0, (1, 2)),
                (1, (0, 1, 2)),
                (1, (2, 1, 0)),
                (1, (0, 0, 1)),
            ]),
            rules=frozenset([0]),
            reqs=frozenset([(0, 2)]),
        )
        self.assertEqual(len(r5.insts), 5)
        r5_iso = rename(r5, (1, 0, 2), (0, 1))
        self.assertEqual(canonical(r5), canonical(r5_iso))
        self.assertEqual(canonical_bruteforce(r5), canonical_bruteforce(r5_iso))

        # Mini census over |insts|=4 subset
        mini_census = hci.run_census(regimes=[r4, r4_iso, r5, r5_iso], check_corpus=False)
        self.assertEqual(mini_census["regime_count"], 4)
        self.assertEqual(mini_census["refined_class_count"], 2)
        self.assertEqual(mini_census["brute_class_count"], 2)
        self.assertTrue(mini_census["agreement"])
        self.assertEqual(mini_census["falsifier_count"], 0)

    def test_deep_receipt_file_verification(self) -> None:
        """Byte-pinned deep receipt in evidence/hunt_deep.json satisfies all invariants."""
        deep_receipt_path = ISO_SOUND_DIR / "evidence" / "hunt_deep.json"
        self.assertTrue(deep_receipt_path.is_file(), "hunt_deep.json must exist")

        content = deep_receipt_path.read_text(encoding="utf-8")
        # Check no timestamps or absolute system paths
        for forbidden in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(forbidden, content)

        receipt = json.loads(content)
        self.assertEqual(receipt["schema"], "iso-sound-hunt-v1")
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["general_soundness"], "OPEN")
        self.assertEqual(receipt["bounds"]["max_arity"], 3)
        self.assertEqual(receipt["bounds"]["max_insts"], 4)
        self.assertEqual(receipt["bounds"]["max_data"], 3)
        self.assertEqual(receipt["bounds"]["max_forms"], 1)
        self.assertEqual(receipt["regime_count"], 338650)
        self.assertEqual(receipt["refined_class_count"], 57266)
        self.assertEqual(receipt["brute_class_count"], 57266)
        self.assertTrue(receipt["agreement"])
        self.assertEqual(receipt["falsifier_count"], 0)
        self.assertEqual(receipt["falsifiers"], [])

        # Sample sweep verification
        self.assertIn("sample_sweep", receipt)
        sw = receipt["sample_sweep"]
        self.assertTrue(sw["agreement"])
        self.assertEqual(sw["falsifier_count"], 0)
        self.assertEqual(sw["sample_count"], 10000)
        self.assertEqual(sw["bounds"]["max_arity"], 3)
        self.assertEqual(sw["bounds"]["max_forms"], 2)
        self.assertEqual(sw["bounds"]["max_insts"], 4)

        # Seed corpus verification
        self.assertTrue(receipt["seed_corpus"]["agreement"])
        self.assertEqual(receipt["seed_corpus"]["disagreements"], 0)

        # Honesty guards pass with zero errors
        self.assertEqual(hci.verify_receipt_honesty(receipt), [])

    def test_sample_sweep_execution(self) -> None:
        """Sample sweep executes deterministically with agreement and 0 falsifiers."""
        sweep = hci.run_sample_sweep(
            max_data=3,
            max_forms=2,
            max_arity=3,
            max_insts=4,
            sample_count=200,
            seed=42,
            require_ternary=True,
        )
        self.assertEqual(sweep["sample_count"], 200)
        self.assertTrue(sweep["agreement"])
        self.assertEqual(sweep["falsifier_count"], 0)
        self.assertEqual(sweep["falsifiers"], [])
        self.assertEqual(sweep["refined_class_count"], sweep["brute_class_count"])

    def test_corrupted_sweep_rejected_by_honesty_guard(self) -> None:
        """Honesty guards reject receipt with corrupted sample sweep."""
        corrupted_receipt = {
            "schema": "iso-sound-hunt-v1",
            "authority_effect": "None",
            "general_soundness": "OPEN",
            "agreement": True,
            "falsifier_count": 0,
            "sample_sweep": {"agreement": False},
        }
        errors = hci.verify_receipt_honesty(corrupted_receipt)
        self.assertIn("SWEEP_GUARD: sample sweep did not agree", errors)


if __name__ == "__main__":
    unittest.main()

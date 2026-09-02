from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import model
import run_connector
import source_manifest


class CharacterTests(unittest.TestCase):
    def test_exchange_is_free_involution_with_one_erasure(self) -> None:
        for history in model.HistoryClass:
            self.assertIs(model.exchange(model.exchange(history)), history)
            self.assertIsNot(model.exchange(history), history)
        self.assertEqual(
            model.erased_endpoint(model.HistoryClass.FORWARD),
            model.erased_endpoint(model.HistoryClass.REVERSED),
        )

    def test_both_characters_exist_and_nontrivial_is_unique(self) -> None:
        values = {
            model.TRIVIAL_CHARACTER.exchange_value,
            model.SIGN_CHARACTER.exchange_value,
        }
        self.assertEqual(values, {model.Polarity.POSITIVE, model.Polarity.NEGATIVE})
        self.assertTrue(model.TRIVIAL_CHARACTER.satisfies_laws())
        self.assertTrue(model.SIGN_CHARACTER.satisfies_laws())
        self.assertFalse(model.TRIVIAL_CHARACTER.operationally_nontrivial)
        self.assertTrue(model.SIGN_CHARACTER.operationally_nontrivial)

    def test_global_basepoint_flip_is_relative(self) -> None:
        for history in model.HistoryClass:
            self.assertIsNot(
                model.relative_value(
                    model.SIGN_CHARACTER, model.HistoryClass.FORWARD, history
                ),
                model.relative_value(
                    model.SIGN_CHARACTER, model.HistoryClass.REVERSED, history
                ),
            )


class OccurrenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.once: model.OccurrenceHistory = (model.Occurrence(0, 7),)
        self.twice: model.OccurrenceHistory = (
            model.Occurrence(0, 7),
            model.Occurrence(1, 7),
        )

    def test_canonical_forget_does_not_determine_count(self) -> None:
        self.assertTrue(model.valid_occurrences(self.once))
        self.assertTrue(model.valid_occurrences(self.twice))
        self.assertEqual(model.canonical_forget(self.once), (7,))
        self.assertEqual(model.canonical_forget(self.twice), (7,))
        self.assertEqual(model.count_token(self.once, 7), 1)
        self.assertEqual(model.count_token(self.twice, 7), 2)

    def test_reorder_equivalence_zero_and_addition(self) -> None:
        reordered = model.reorder_occurrences(self.twice, (1, 0))
        self.assertTrue(model.occurrence_equivalent(self.twice, reordered))
        self.assertTrue(model.valid_occurrences(reordered))
        self.assertEqual(model.count_token((), 7), 0)
        combined = model.fresh_append(self.once, self.twice)
        self.assertTrue(model.valid_occurrences(combined))
        self.assertEqual(
            model.count_token(combined, 7),
            model.count_token(self.once, 7) + model.count_token(self.twice, 7),
        )

    def test_invalid_identity_and_permutation_are_rejected(self) -> None:
        duplicate_ids = (model.Occurrence(0, 7), model.Occurrence(0, 8))
        self.assertFalse(model.valid_occurrences(duplicate_ids))
        with self.assertRaises(ValueError):
            model.canonical_forget(duplicate_ids)
        with self.assertRaises(ValueError):
            model.reorder_occurrences(self.twice, (0, 0))

    def test_count_equivalence_does_not_quotient_ordered_forget(self) -> None:
        ordered: model.OccurrenceHistory = (
            model.Occurrence(0, 7),
            model.Occurrence(1, 8),
        )
        reversed_order = model.reorder_occurrences(ordered, (1, 0))
        self.assertTrue(model.occurrence_equivalent(ordered, reversed_order))
        self.assertEqual(model.canonical_forget(ordered), (7, 8))
        self.assertEqual(model.canonical_forget(reversed_order), (8, 7))

    def test_equivalence_laws_and_interleaved_forget(self) -> None:
        history: model.OccurrenceHistory = (
            model.Occurrence(0, 7),
            model.Occurrence(1, 8),
            model.Occurrence(2, 7),
        )
        middle = model.reorder_occurrences(history, (2, 1, 0))
        final = model.reorder_occurrences(history, (1, 0, 2))
        self.assertTrue(model.occurrence_equivalent(history, history))
        self.assertEqual(
            model.occurrence_equivalent(history, middle),
            model.occurrence_equivalent(middle, history),
        )
        self.assertTrue(model.occurrence_equivalent(history, middle))
        self.assertTrue(model.occurrence_equivalent(middle, final))
        self.assertTrue(model.occurrence_equivalent(history, final))
        self.assertEqual(model.canonical_forget(history), (7, 8))

    def test_integer_map_is_an_explicit_argument(self) -> None:
        self.assertEqual(model.occurrence_weight(self.twice, 7, lambda n: n), 2)
        self.assertEqual(model.occurrence_weight(self.twice, 7, lambda _: 11), 11)
        self.assertTrue(model.UNIT_COUNT_CALIBRATION.valid_through(8))
        self.assertFalse(model.CountCalibration(lambda _: 0).valid_through(8))


class ConditionalContactTests(unittest.TestCase):
    def test_conditional_contact(self) -> None:
        pair = model.ImportedPairCorrespondence(
            model.HistoryClass.FORWARD,
            model.HistoryClass.REVERSED,
            model.erased_endpoint,
        )
        self.assertTrue(
            model.conditional_contact(
                pair,
                model.SIGN_CHARACTER,
                model.STANDARD_INTEGER_CALIBRATION,
                model.mixing_readout,
            )
        )
        self.assertFalse(
            model.conditional_contact(
                pair,
                model.TRIVIAL_CHARACTER,
                model.STANDARD_INTEGER_CALIBRATION,
                model.mixing_readout,
            )
        )
        self.assertFalse(
            model.conditional_contact(
                pair,
                model.SIGN_CHARACTER,
                model.IntegerCalibration(lambda _: 11),
                model.mixing_readout,
            )
        )

    def test_required_mutations(self) -> None:
        self.assertFalse(
            model.ImportedPairCorrespondence(
                model.HistoryClass.FORWARD,
                model.HistoryClass.FORWARD,
                model.erased_endpoint,
            ).valid()
        )
        self.assertFalse(
            model.ImportedPairCorrespondence(
                model.HistoryClass.FORWARD,
                model.HistoryClass.REVERSED,
                lambda history: history.value,
            ).valid()
        )
        collapsed = model.ImportedPairCorrespondence(
            model.HistoryClass.FORWARD,
            model.HistoryClass.FORWARD,
            model.erased_endpoint,
        )
        unequal = model.ImportedPairCorrespondence(
            model.HistoryClass.FORWARD,
            model.HistoryClass.REVERSED,
            lambda history: history.value,
        )
        for invalid_pair in (collapsed, unequal):
            self.assertFalse(
                model.conditional_contact(
                    invalid_pair,
                    model.SIGN_CHARACTER,
                    model.STANDARD_INTEGER_CALIBRATION,
                    model.mixing_readout,
                )
            )
        valid_pair = model.ImportedPairCorrespondence(
            model.HistoryClass.FORWARD,
            model.HistoryClass.REVERSED,
            model.erased_endpoint,
        )
        self.assertFalse(
            model.conditional_contact(
                valid_pair,
                model.SIGN_CHARACTER,
                model.STANDARD_INTEGER_CALIBRATION,
                lambda _: 0,
            )
        )
        self.assertEqual(
            model.induced_pair(
                model.TRIVIAL_CHARACTER, model.STANDARD_INTEGER_CALIBRATION
            ),
            (1, 1),
        )
        self.assertEqual(model.coordinate_squares((1, 1)), model.coordinate_squares((1, -1)))
        self.assertFalse(model.is_involution_on_three())
        self.assertFalse(model.free_involution_on_three_exists())

    def test_type_firewall_countermodel(self) -> None:
        self.assertTrue(model.report_right_inverse_exists())
        self.assertFalse(model.flip_natural_choice_exists())
        self.assertTrue(model.unit_natural_choice_exists())
        self.assertFalse(model.empty_report_right_inverse_exists())


class ReceiptTests(unittest.TestCase):
    def test_receipt_round_trip_and_duplicate_names_rejected(self) -> None:
        payload = json.loads(run_connector.render(), object_pairs_hook=self._strict_pairs)
        self.assertEqual(payload["terminal"], "IMPORT_ISOLATED_BUT_NOT_REMOVED")
        with self.assertRaises(ValueError):
            json.loads('{"terminal": 1, "terminal": 2}', object_pairs_hook=self._strict_pairs)

    def test_source_manifest_round_trip(self) -> None:
        repo = source_manifest.repo_root()
        committed = repo / source_manifest.MANIFEST
        self.assertEqual(committed.read_bytes(), source_manifest.render_manifest(repo))

    def test_renderer_is_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = Path(first) / "connector.json"
            two = Path(second) / "connector.json"
            one.write_bytes(run_connector.render())
            two.write_bytes(run_connector.render())
            self.assertEqual(one.read_bytes(), two.read_bytes())

    @staticmethod
    def _strict_pairs(values: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"duplicate JSON name: {key}")
            result[key] = value
        return result


if __name__ == "__main__":
    unittest.main()

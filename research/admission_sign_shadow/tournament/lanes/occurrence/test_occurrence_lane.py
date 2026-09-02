from __future__ import annotations

import json
from pathlib import Path
from typing import cast
import unittest

from occurrence_lane import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Occurrence,
    Supply,
    additive_laws_hold,
    canonical_datum_replay,
    count_token,
    forget_occurrences,
    occurrence_replay,
    projected_tokens,
    rename_ids,
    scaled_encoding,
    symbol_packet,
    valid_occurrence_ids,
)


class ReplayOccurrenceTests(unittest.TestCase):
    def test_projection_uses_only_datum_admissions(self) -> None:
        history = (
            Supply(99),
            AdmitForm(1),
            AdmitDatum(7),
            AdmitInst(0, (0,)),
            AdmitRuleAll(0),
            Impose(0, 1),
            AdmitDatum(8),
        )
        self.assertEqual(projected_tokens(history), (7, 8))
        self.assertEqual(
            occurrence_replay(history),
            (Occurrence(0, 7), Occurrence(1, 8)),
        )

    def test_supply_is_no_op_for_both_projections(self) -> None:
        base = (AdmitDatum(7),)
        supplied = (Supply(7),) + base
        self.assertEqual(canonical_datum_replay(supplied), canonical_datum_replay(base))
        self.assertEqual(occurrence_replay(supplied), occurrence_replay(base))

    def test_occurrence_ids_are_deterministic_and_valid(self) -> None:
        history = (AdmitDatum(7), AdmitDatum(8), AdmitDatum(7))
        expected = (Occurrence(0, 7), Occurrence(1, 8), Occurrence(2, 7))
        self.assertEqual(occurrence_replay(history), expected)
        self.assertEqual(occurrence_replay(history), occurrence_replay(history))
        self.assertTrue(valid_occurrence_ids(expected))
        self.assertEqual(count_token(expected, 7), 2)

    def test_forget_replay_commutes(self) -> None:
        histories = (
            (),
            (Supply(7),),
            (AdmitDatum(7),),
            (AdmitDatum(7), AdmitDatum(7)),
            (AdmitDatum(8), AdmitDatum(7), AdmitDatum(8)),
        )
        for history in histories:
            with self.subTest(history=history):
                self.assertEqual(
                    forget_occurrences(occurrence_replay(history)),
                    canonical_datum_replay(history),
                )

    def test_duplicate_admission_collides_at_endpoint(self) -> None:
        once = (AdmitDatum(7),)
        duplicate = (AdmitDatum(7), AdmitDatum(7))
        once_occurrences = occurrence_replay(once)
        duplicate_occurrences = occurrence_replay(duplicate)
        self.assertEqual(canonical_datum_replay(once), canonical_datum_replay(duplicate))
        self.assertNotEqual(once_occurrences, duplicate_occurrences)
        self.assertEqual(count_token(once_occurrences, 7), 1)
        self.assertEqual(count_token(duplicate_occurrences, 7), 2)

    def test_id_renaming_preserves_count_and_forget(self) -> None:
        history = occurrence_replay(
            (AdmitDatum(7), AdmitDatum(8), AdmitDatum(7))
        )
        renamed = rename_ids(history, lambda identifier: 10 + 2 * identifier)
        self.assertTrue(valid_occurrence_ids(renamed))
        self.assertEqual(count_token(renamed, 7), count_token(history, 7))
        self.assertEqual(forget_occurrences(renamed), forget_occurrences(history))

    def test_noninjective_id_renaming_is_rejected_by_validity(self) -> None:
        history = occurrence_replay((AdmitDatum(7), AdmitDatum(8)))
        collapsed = rename_ids(history, lambda _: 0)
        self.assertFalse(valid_occurrence_ids(collapsed))

    def test_additive_laws_leave_integer_unit_free(self) -> None:
        encodings = {unit: scaled_encoding(unit) for unit in (-2, 0, 1, 3)}
        self.assertTrue(all(additive_laws_hold(encode, 8) for encode in encodings.values()))
        self.assertEqual({encode(1) for encode in encodings.values()}, {-2, 0, 1, 3})

    def test_unit_calibration_is_an_extra_premise(self) -> None:
        unit = scaled_encoding(1)
        self.assertTrue(additive_laws_hold(unit, 8))
        self.assertEqual(tuple(unit(count) for count in range(9)), tuple(range(9)))
        zero = scaled_encoding(0)
        self.assertTrue(additive_laws_hold(zero, 8))
        self.assertNotEqual(zero(1), 1)

    def test_symbol_packet_has_only_strict_statuses(self) -> None:
        packet = symbol_packet()
        allowed = {"PROVED", "CONDITIONAL", "REFUTED", "OPEN"}
        symbols = cast(list[dict[str, object]], packet["symbols"])
        self.assertIsInstance(symbols, list)
        self.assertTrue(symbols)
        self.assertEqual({entry["status"] for entry in symbols} - allowed, set())
        by_symbol = {entry["symbol"]: entry["status"] for entry in symbols}
        self.assertEqual(by_symbol["ENDPOINT_DETERMINES_OCCURRENCE_HISTORY"], "REFUTED")
        self.assertEqual(by_symbol["ADDITIVE_LAWS_SELECT_INTEGER_UNIT"], "REFUTED")
        self.assertEqual(by_symbol["UNIT_CALIBRATED_ENCODING_UNIQUE"], "CONDITIONAL")
        self.assertEqual(by_symbol["EXACT_FROZEN_TEVENT_REPLAY_USE"], "PROVED")
        self.assertEqual(
            by_symbol["OCCURRENCE_TRACE_CONNECTOR_INTEGRATION"], "OPEN"
        )
        self.assertEqual(
            packet["terminal"],
            "TRACE_PROJECTION_PROVED_CONNECTOR_INTEGRATION_OPEN",
        )

    def test_committed_symbol_packet_replays_exactly(self) -> None:
        committed = json.loads(
            Path(__file__).with_name("SYMBOL_PACKET.json").read_text(encoding="utf-8")
        )
        self.assertEqual(committed, symbol_packet())


if __name__ == "__main__":
    unittest.main()

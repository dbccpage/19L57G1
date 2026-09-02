from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Sequence


class HistoryClass(str, Enum):
    FORWARD = "forward"
    REVERSED = "reversed"


def exchange(history: HistoryClass) -> HistoryClass:
    if history is HistoryClass.FORWARD:
        return HistoryClass.REVERSED
    return HistoryClass.FORWARD


def erased_endpoint(_: HistoryClass) -> tuple[tuple[()]]:
    return ((),)


class Polarity(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


def polarity_multiply(left: Polarity, right: Polarity) -> Polarity:
    if left is Polarity.POSITIVE:
        return right
    if right is Polarity.POSITIVE:
        return Polarity.NEGATIVE
    return Polarity.POSITIVE


@dataclass(frozen=True)
class ExchangeCharacter:
    exchange_value: Polarity

    def value(self, exchanged: bool) -> Polarity:
        return self.exchange_value if exchanged else Polarity.POSITIVE

    def satisfies_laws(self) -> bool:
        return self.value(False) is Polarity.POSITIVE and all(
            self.value(left ^ right)
            is polarity_multiply(self.value(left), self.value(right))
            for left in (False, True)
            for right in (False, True)
        )

    @property
    def operationally_nontrivial(self) -> bool:
        return self.exchange_value is not Polarity.POSITIVE


TRIVIAL_CHARACTER = ExchangeCharacter(Polarity.POSITIVE)
SIGN_CHARACTER = ExchangeCharacter(Polarity.NEGATIVE)


def relative_value(
    character: ExchangeCharacter,
    base: HistoryClass,
    history: HistoryClass,
) -> Polarity:
    return character.value(history is not base)


@dataclass(frozen=True, order=True)
class Occurrence:
    occurrence_id: int
    token: int

    def __post_init__(self) -> None:
        if self.occurrence_id < 0 or self.token < 0:
            raise ValueError("occurrence fields must be nonnegative")


OccurrenceHistory = tuple[Occurrence, ...]


def valid_occurrences(history: OccurrenceHistory) -> bool:
    identifiers = [item.occurrence_id for item in history]
    return len(identifiers) == len(set(identifiers))


def require_valid_occurrences(history: OccurrenceHistory) -> None:
    if not valid_occurrences(history):
        raise ValueError("occurrence identifiers are not unique")


def reorder_occurrences(
    history: OccurrenceHistory, order: Sequence[int]
) -> OccurrenceHistory:
    require_valid_occurrences(history)
    if sorted(order) != list(range(len(history))):
        raise ValueError("order is not a permutation of the occurrence positions")
    return tuple(history[index] for index in order)


def count_token(history: OccurrenceHistory, token: int) -> int:
    return sum(1 for item in history if item.token == token)


def occurrence_equivalent(left: OccurrenceHistory, right: OccurrenceHistory) -> bool:
    require_valid_occurrences(left)
    require_valid_occurrences(right)
    tokens = {item.token for item in left} | {item.token for item in right}
    return all(count_token(left, token) == count_token(right, token) for token in tokens)


def canonical_forget(history: OccurrenceHistory) -> tuple[int, ...]:
    require_valid_occurrences(history)
    result: list[int] = []
    for item in history:
        if item.token not in result:
            result.append(item.token)
    return tuple(result)


def fresh_append(left: OccurrenceHistory, right: OccurrenceHistory) -> OccurrenceHistory:
    require_valid_occurrences(left)
    require_valid_occurrences(right)
    first_fresh = max((item.occurrence_id for item in left), default=-1) + 1
    fresh_right = tuple(
        Occurrence(first_fresh + index, item.token) for index, item in enumerate(right)
    )
    combined = left + fresh_right
    require_valid_occurrences(combined)
    return combined


def occurrence_weight(
    history: OccurrenceHistory,
    token: int,
    supplied_map: Callable[[int], int],
) -> int:
    require_valid_occurrences(history)
    return supplied_map(count_token(history, token))


@dataclass(frozen=True)
class CountCalibration:
    encode: Callable[[int], int]

    def valid_through(self, bound: int) -> bool:
        if bound < 1:
            raise ValueError("calibration bound must include zero and one")
        if self.encode(0) != 0 or self.encode(1) != 1:
            return False
        return all(
            self.encode(left + right) == self.encode(left) + self.encode(right)
            for left in range(bound + 1)
            for right in range(bound + 1 - left)
        )


UNIT_COUNT_CALIBRATION = CountCalibration(lambda count: count)


@dataclass(frozen=True)
class IntegerCalibration:
    encode: Callable[[Polarity], int]

    def valid(self) -> bool:
        return self.encode(Polarity.POSITIVE) == 1 and self.encode(Polarity.NEGATIVE) == -1


def coordinate_squares(pair: tuple[int, int]) -> tuple[int, int]:
    return (pair[0] * pair[0], pair[1] * pair[1])


def induced_pair(
    character: ExchangeCharacter,
    supplied_calibration: IntegerCalibration,
) -> tuple[int, int]:
    return (
        supplied_calibration.encode(Polarity.POSITIVE),
        supplied_calibration.encode(character.exchange_value),
    )


def _standard_integer_value(value: Polarity) -> int:
    return 1 if value is Polarity.POSITIVE else -1


STANDARD_INTEGER_CALIBRATION = IntegerCalibration(_standard_integer_value)


def mixing_readout(pair: tuple[int, int]) -> int:
    return (pair[0] + pair[1]) * (pair[0] + pair[1])


@dataclass(frozen=True)
class ImportedPairCorrespondence:
    left: HistoryClass
    right: HistoryClass
    erase: Callable[[HistoryClass], object]

    def valid(self) -> bool:
        return (
            self.right is exchange(self.left)
            and self.left is not self.right
            and self.erase(self.left) == self.erase(self.right)
        )


def conditional_contact(
    pair: ImportedPairCorrespondence,
    character: ExchangeCharacter,
    supplied_calibration: IntegerCalibration,
    mixing: Callable[[tuple[int, int]], int],
) -> bool:
    if (
        not pair.valid()
        or not character.satisfies_laws()
        or not character.operationally_nontrivial
        or not supplied_calibration.valid()
    ):
        return False
    plus = (
        supplied_calibration.encode(Polarity.POSITIVE),
        supplied_calibration.encode(Polarity.POSITIVE),
    )
    split = induced_pair(character, supplied_calibration)
    return coordinate_squares(plus) == coordinate_squares(split) and mixing(
        plus
    ) != mixing(split)


def three_cycle(index: int) -> int:
    if index not in (0, 1, 2):
        raise ValueError("index is outside the declared three-element mutation")
    return (index + 1) % 3


def is_involution_on_three() -> bool:
    return all(three_cycle(three_cycle(index)) == index for index in range(3))


def free_involution_on_three_exists() -> bool:
    mappings = (
        (first, second, third)
        for first in range(3)
        for second in range(3)
        for third in range(3)
    )
    for mapping in mappings:
        involutive = all(mapping[mapping[index]] == index for index in range(3))
        fixed_free = all(mapping[index] != index for index in range(3))
        if involutive and fixed_free:
            return True
    return False


def report_right_inverse_exists() -> bool:
    carrier: tuple[int, ...] = (0,)
    reports: tuple[int, ...] = (0,)

    def report(value: int) -> int:
        return value

    def choose(label: int) -> int:
        return label

    return all(
        choose(label) in carrier and report(choose(label)) == label
        for label in reports
    )


def flip_natural_choice_exists() -> bool:
    return any((not value) == value for value in (False, True))


def unit_natural_choice_exists() -> bool:
    return True


def empty_report_right_inverse_exists() -> bool:
    return False


def connector_payload() -> dict[str, object]:
    once: OccurrenceHistory = (Occurrence(0, 7),)
    twice: OccurrenceHistory = (Occurrence(0, 7), Occurrence(1, 7))
    reordered = reorder_occurrences(twice, (1, 0))
    combined = fresh_append(once, twice)
    pair = ImportedPairCorrespondence(
        HistoryClass.FORWARD, HistoryClass.REVERSED, erased_endpoint
    )
    plus = (1, 1)
    split = induced_pair(SIGN_CHARACTER, STANDARD_INTEGER_CALIBRATION)
    return {
        "authority_effect": None,
        "two_history": {
            "distinct": exchange(HistoryClass.FORWARD) is HistoryClass.REVERSED,
            "exchange_involutive": all(
                exchange(exchange(history)) is history for history in HistoryClass
            ),
            "same_erased_endpoint": erased_endpoint(HistoryClass.FORWARD)
            == erased_endpoint(HistoryClass.REVERSED),
        },
        "characters": {
            "laws_hold": [
                TRIVIAL_CHARACTER.satisfies_laws(),
                SIGN_CHARACTER.satisfies_laws(),
            ],
            "legal_values": [
                TRIVIAL_CHARACTER.exchange_value.value,
                SIGN_CHARACTER.exchange_value.value,
            ],
            "nontrivial_value": SIGN_CHARACTER.exchange_value.value,
            "global_basepoint_flip": all(
                relative_value(SIGN_CHARACTER, HistoryClass.FORWARD, history)
                is not relative_value(SIGN_CHARACTER, HistoryClass.REVERSED, history)
                for history in HistoryClass
            ),
            "operational_nontriviality": "IMPORTED_PREMISE",
        },
        "occurrences": {
            "once_valid": valid_occurrences(once),
            "twice_valid": valid_occurrences(twice),
            "same_canonical": canonical_forget(once) == canonical_forget(twice),
            "counts": [count_token(once, 7), count_token(twice, 7)],
            "reorder_invariant": occurrence_equivalent(twice, reordered),
            "reorder_preserves_validity": valid_occurrences(reordered),
            "zero": count_token((), 7),
            "fresh_append_valid": valid_occurrences(combined),
            "append_additive": count_token(combined, 7)
            == count_token(once, 7) + count_token(twice, 7),
            "ordered_forget_not_equivalence_quotient": True,
            "integer_map": "DECLARED_INPUT",
            "unit_calibration": "IMPORTED_PREMISE",
            "unit_calibration_laws_through_6": UNIT_COUNT_CALIBRATION.valid_through(6),
        },
        "conditional_contact": {
            "coordinate_squares_equal": coordinate_squares(plus)
            == coordinate_squares(split),
            "mixed_readouts": [mixing_readout(plus), mixing_readout(split)],
            "separates_with_supplied_map": conditional_contact(
                pair,
                SIGN_CHARACTER,
                STANDARD_INTEGER_CALIBRATION,
                mixing_readout,
            ),
        },
        "mutations": {
            "collapsed_histories_rejected": not ImportedPairCorrespondence(
                HistoryClass.FORWARD, HistoryClass.FORWARD, erased_endpoint
            ).valid(),
            "equal_parity_rejected": not TRIVIAL_CHARACTER.operationally_nontrivial,
            "unequal_endpoints_rejected": not ImportedPairCorrespondence(
                HistoryClass.FORWARD,
                HistoryClass.REVERSED,
                lambda history: history.value,
            ).valid(),
            "trivial_character_no_pair_change": induced_pair(
                TRIVIAL_CHARACTER, STANDARD_INTEGER_CALIBRATION
            )
            == plus,
            "without_mixing_only_squares": coordinate_squares(plus)
            == coordinate_squares(split),
            "three_cycle_not_involution": not is_involution_on_three(),
            "three_elements_have_no_free_involution": not free_involution_on_three_exists(),
        },
        "type_firewall": {
            "report_right_inverse_exists": report_right_inverse_exists(),
            "flip_natural_choice_exists": flip_natural_choice_exists(),
            "unit_natural_choice_exists": unit_natural_choice_exists(),
            "empty_report_right_inverse_exists": empty_report_right_inverse_exists(),
            "adapter": "OPEN",
        },
        "imports": {
            "frozen_pair_correspondence": "IMPORTED_PREMISE",
            "operational_nontriviality": "IMPORTED_PREMISE",
            "occurrence_to_integer_map": "DECLARED_INPUT",
            "occurrence_unit_calibration": "IMPORTED_PREMISE",
            "character_to_integer_calibration": "DECLARED_INPUT",
            "mixing_map": "DECLARED_INPUT",
            "section_adapter": "OPEN",
        },
        "terminal": "IMPORT_ISOLATED_BUT_NOT_REMOVED",
    }

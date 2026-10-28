"""Pins, reach, and the finite mirrors behind the VERIFIED_FINITE rows."""
from pathlib import Path

from model import (
    HERE, P1, P2, Q3, acquisition_values, axiom_report_names, chain_check, consumed_modules,
    consumed_research_modules, contract_declarations, demurred_check, exceeding_census, exceeding_minimum,
    exceeds, examples, fixes_converse_check, lean_imports, outcome_check, theorem_names,
)


def test_imports_are_the_pinned_modules() -> None:
    assert lean_imports() == sorted(consumed_modules() + list(consumed_research_modules()))


def test_consumed_modules_exist() -> None:
    root = HERE.parents[1]
    for module in consumed_modules():
        assert (root / "lean4" / Path(*module.split("."))).with_suffix(".lean").is_file(), module
    for module, file in consumed_research_modules().items():
        assert (root / file).is_file(), module
        assert file.endswith("/" + module.split(".")[-1] + ".lean"), module


def test_axiom_report_covers_every_theorem_and_matches_contract() -> None:
    names = theorem_names()
    assert len(names) == len(set(names))
    assert axiom_report_names() == names
    assert contract_declarations() == names


def test_exceeding_minimum_is_three_data_and_two_members() -> None:
    census = exceeding_census(4, 3)
    assert exceeding_minimum(census) == {"min_data": 3, "min_members": 2, "empty_family_exceeds_on_constants": 1}
    assert not any(census[f"{n},{k}"] for n in (1, 2) for k in (1, 2, 3))
    assert not any(census[f"{n},1"] for n in (1, 2, 3, 4))
    assert census["3,2"] and census["4,2"]
    assert exceeds(3, (P1, P2), Q3)


def test_lean_examples_mirror() -> None:
    e = examples()
    assert e["exceeds_three_two"] is True
    assert e["exceeds_three_two_resolution"] == [2, 2, 2, 3]
    assert e["correspondence_matters"] == [True, False]
    assert e["aggregate_hides_exceeding"] == [[0, 1, 2, 3], True, False]
    assert e["consensus_after_loss"] == [True, True, True, False]
    assert e["information_without_determination"] == [2, False]
    assert e["residuals_parity_half"] == [(0, 2), (1, 3), (2, 0), (3, 1)]


def test_acquisition_values_up_to_six_points() -> None:
    a = acquisition_values(6)
    assert a["unpromised"] == a["half_square"] == {"1": 0, "2": 1, "3": 3, "4": 6, "5": 10, "6": 15}
    assert a["at_most_mismatches"] == []
    assert a["exactly_mismatches"] == ["2,2", "3,3", "4,4", "5,5", "6,6"]
    exactly = a["exactly"]
    assert isinstance(exactly, dict)
    for n in (2, 3, 4, 5, 6):
        assert exactly[f"{n},{n}"] == [0, n * (n - 1) // 2]
    assert exactly["4,3"] == [5, 5] and exactly["5,3"] == [7, 7] and exactly["5,2"] == [4, 4]
    assert exactly["6,3"] == [9, 9] and exactly["6,4"] == [12, 12] and exactly["6,5"] == [14, 14]


def test_fixing_transcripts_yield_a_sharp_closure_evaluator() -> None:
    for n in (1, 2, 3, 4):
        result = fixes_converse_check(n)
        assert result["violations"] == 0
        assert result["fixing"] >= 1
    assert fixes_converse_check(4) == {"transcripts": 729, "inconsistent": 259, "fixing": 250, "violations": 0}
    assert fixes_converse_check(5) == {"transcripts": 59049, "inconsistent": 37617, "fixing": 10354, "violations": 0}


def test_long_chains_have_a_stationary_step_and_the_bound_is_tight() -> None:
    assert chain_check(3) == {"chains": 4000, "violations": 0, "shorter_chain_without_stationary_step": True}


def test_pair_claim_outcomes_on_three_points() -> None:
    assert outcome_check(3) == {"checked": 2187, "violations": 0}


def test_demurred_claim_is_always_known_and_total_iff_known() -> None:
    assert demurred_check(3) == {"checked": 160, "violations": 0}

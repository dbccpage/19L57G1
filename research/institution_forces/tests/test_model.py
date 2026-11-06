"""Pins, reach, and the finite mirrors behind the VERIFIED_FINITE rows."""
from pathlib import Path

from model import (
    HERE, axiom_report_names, consumed_modules, consumed_research_modules, contract_declarations,
    examples, fast_form_check, l0_check, l1_check, l2_add_and_target_check, l2_extension_check,
    l2_removal_check, l3_check, lean_imports, theorem_names,
)


def test_imports_are_the_pinned_research_modules() -> None:
    assert lean_imports() == sorted(consumed_research_modules())


def test_consumed_modules_exist() -> None:
    root = HERE.parents[1]
    for module in consumed_modules():
        assert (root / "lean4" / Path(*module.split("."))).with_suffix(".lean").is_file(), module
    for module, file in consumed_research_modules().items():
        assert (root / file).is_file(), module
        assert file.endswith("/" + module.split(".")[-1] + ".lean"), module


def test_axiom_report_covers_every_theorem_and_matches_contract() -> None:
    names = theorem_names()
    assert len(names) == len(set(names)) == 59
    assert axiom_report_names() == names
    assert contract_declarations() == names


def test_fast_form_agrees_with_the_definition() -> None:
    assert fast_form_check() == {"checked": 135424, "violations": 0}


def test_l0_joint_presentation() -> None:
    assert l0_check() == {"checked": 1118464, "violations": 0}


def test_l1_replacement_and_deletion_thresholds() -> None:
    assert l1_check() == {"checked": 279616, "violations": 0, "robust_cases": 78932}


def test_l2_addition_and_targets() -> None:
    assert l2_add_and_target_check() == {"checked": 744544, "violations": 0,
                                         "decisions_failing_a_target": 698010}


def test_l2_removal_and_seat_corruption() -> None:
    assert l2_removal_check() == {"checked": 541200, "violations": 0}


def test_l2_carrier_extension() -> None:
    assert l2_extension_check() == {"checked": 2128688, "violations": 0, "broken_by_extension": 197640}


def test_l3_ballot_compression() -> None:
    assert l3_check() == {"checked": 48109840, "violations": 0, "strict_losses": 10465788,
                          "sincere_checked": 69904, "sincere_violations": 0,
                          "sincere_losses": 2928, "sincere_exceeding_lost": 2928}


def test_lean_examples_mirror() -> None:
    e = examples()
    assert e["robust_parity_half"] == [0, 1]
    assert e["relabel_can_be_harmless"] == [True, False]
    assert e["relabel_can_break"] is False
    assert e["extension_breaks"] == [True, False]
    assert e["ballot_loses_exceeding"] == [True, False, False, [(2, 2, 2, 2), (2, 2, 2, 2)], False]
    assert e["injective_ballot_keeps"] is True

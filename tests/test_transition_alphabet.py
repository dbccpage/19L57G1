"""Tests for the declared one-step transition-codebook mirror.

The code-image sizes are recomputed from the declared class table, and
the partition is checked
exhaustively over the declared space, and every negative result
(the refuted environment-ownership claim, the two non-invariant profile
components, the load-bearing well-formedness condition) has its own
test.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import run_transition_alphabet
from derivation.primitive_passage import GENESIS_P, PS, next_family_p, pstep
from derivation.transition_alphabet import (
    ALL_CLASSES,
    CLASS_SIGS,
    ENV_OWNED,
    EVENT_BATTERY,
    FIELDS,
    accepted,
    codebook_report,
    contextual_countermodel_report,
    budget_delta,
    class_of,
    continuity_of,
    effect_sig_of,
    enumerate_states,
    erase_guard,
    event_json,
    field_delta,
    gained_pairs,
    guard_holds,
    invariance_report,
    lost_pairs,
    obst_effect,
    obstructed_pairs,
    ownership_report,
    partition_report,
    profile_of,
    prot_s,
    sig_json,
    sig_of,
    state_json,
    state_size,
    wf_class,
    witness_report,
)

OBSTRUCTED = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                prot=((0, 1),), obs=())
FUNDED = replace(OBSTRUCTED, budget=1)
REFINE = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),),
            obs=((),), budget=1)
OUTSIDE = PS(occ=(0, 1), asserted=((0, 1),), wit=(), prot=((0, 1),), obs=())


def test_accepted_agrees_with_guard_everywhere() -> None:
    # the Lean theorem accepted_eq_guardHolds, checked on the space
    for s in enumerate_states():
        for e in EVENT_BATTERY:
            assert accepted(s, e) == guard_holds(s, e)


def test_halted_states_accept_nothing_including_halt() -> None:
    halted = replace(GENESIS_P, halted=True)
    for e in EVENT_BATTERY:
        assert not accepted(halted, e)
        assert not guard_holds(halted, e)
    assert accepted(GENESIS_P, ("halt",))


def test_guard_holds_covers_every_constructor() -> None:
    assert guard_holds(GENESIS_P, ("admitOcc", 0))
    assert not guard_holds(PS(occ=(0,)), ("admitOcc", 0))
    assert guard_holds(PS(occ=(0, 1)), ("assertWit", 0, 1))
    assert not guard_holds(PS(occ=(0,)), ("assertWit", 0, 1))
    assert guard_holds(PS(occ=(0, 1), asserted=((0, 1),)),
                       ("admitWit", 0, 1))
    assert not guard_holds(PS(occ=(0, 1)), ("admitWit", 0, 1))
    assert guard_holds(PS(wit=((0, 1),)), ("protect", 0, 1))
    assert not guard_holds(GENESIS_P, ("protect", 0, 1))
    assert guard_holds(GENESIS_P, ("declareObs",))
    assert not guard_holds(PS(obs=()), ("declareObs",))
    assert guard_holds(REFINE, ("refineCol", (), 0))
    assert not guard_holds(replace(REFINE, budget=0), ("refineCol", (), 0))
    assert guard_holds(FUNDED, ("addCol", (0,)))
    assert not guard_holds(replace(FUNDED, licensed=False),
                           ("addCol", (0,)))
    assert guard_holds(OBSTRUCTED, ("refuse", 0, 1))
    assert not guard_holds(GENESIS_P, ("refuse", 0, 1))
    assert guard_holds(GENESIS_P, ("setBudget", 1))
    assert not guard_holds(GENESIS_P, ("setBudget", 0))
    assert guard_holds(GENESIS_P, ("setLicense", False))
    assert not guard_holds(GENESIS_P, ("setLicense", True))


def test_field_delta_and_profile() -> None:
    t = pstep(GENESIS_P, ("admitOcc", 0))
    assert field_delta(GENESIS_P, t) == tuple(f == "occ" for f in FIELDS)
    prof = profile_of(GENESIS_P, ("admitOcc", 0))
    assert prof[1] == "occurrenceFresh"
    assert prof[2] == "untouched"
    assert prof[3] == "unchanged"
    assert prof[4] == "continuation"
    assert prof[5] == "environment"
    assert prof[6] is True
    assert continuity_of(pstep(GENESIS_P, ("halt",))) == "absorption"


def test_obstruction_effect_has_all_four_values() -> None:
    quiet = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),))
    created = pstep(quiet, ("declareObs",))
    assert obst_effect(quiet, quiet) == "untouched"
    assert obstructed_pairs(OBSTRUCTED) == ((0, 1),)
    assert obst_effect(OBSTRUCTED,
                       pstep(OBSTRUCTED, ("refuse", 0, 1))) == "preserved"
    assert obst_effect(FUNDED, pstep(FUNDED, ("addCol", (0,)))) == "removed"
    protect_obs = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), obs=())
    assert obst_effect(protect_obs,
                       pstep(protect_obs, ("protect", 0, 1))) == "created"
    assert gained_pairs(protect_obs,
                        pstep(protect_obs, ("protect", 0, 1))) == ((0, 1),)
    assert lost_pairs(FUNDED, pstep(FUNDED, ("addCol", (0,)))) == ((0, 1),)
    assert obstructed_pairs(created) == ()


def test_budget_delta_three_values() -> None:
    assert budget_delta(GENESIS_P, GENESIS_P) == "unchanged"
    two = replace(GENESIS_P, budget=2)
    assert budget_delta(two, replace(two, budget=1)) == "spentOne"
    assert budget_delta(GENESIS_P, replace(GENESIS_P, budget=3)) \
        == "rewritten"


def test_class_of_splits_protection_and_declaration() -> None:
    quiet = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),))
    assert class_of(quiet, ("protect", 0, 1)) == "protectQuiet"
    obs_state = replace(quiet, obs=())
    assert class_of(obs_state, ("protect", 0, 1)) == "protectObstructing"
    assert prot_s(obs_state, 0, 1).prot == ((0, 1),)
    assert class_of(GENESIS_P, ("declareObs",)) == "declareQuiet"
    assert class_of(PS(prot=((0, 1),)), ("declareObs",)) \
        == "declareObstructing"
    assert class_of(GENESIS_P, ("halt",)) == "absorbTerminal"


def test_partition_is_exhaustively_verified() -> None:
    rep = partition_report()
    assert rep["guard_agreement_failures"] == 0
    assert rep["class_signature_failures"] == 0
    assert rep["ambiguous_classifications"] == 0
    assert rep["mixed_obstruction_steps"] == 0
    assert rep["halted_accepted_transitions"] == 0
    assert rep["all_classes_realized"] is True
    assert rep["full_profile_image_size"] == 21
    assert rep["declared_signature_image_size"] == 13
    assert rep["pairs_checked"] == 6144 * len(EVENT_BATTERY)
    assert rep["accepted_wellformed_transitions"] > 0


def test_declared_codebook_sizes_are_recomputed() -> None:
    rep = codebook_report()
    assert rep["declared_codebook_size"] == len(ALL_CLASSES) == 13
    assert rep["guard_erased_codebook_size"] == 12
    assert rep["contextual_quotient"] is False
    assert rep["dda_correspondence"] is False
    assert rep["merged_under_guard_erasure"] == [
        ["refineObservation", "extendObservation"]]
    # the merge is a fact about accepted transitions, not the table
    assert effect_sig_of(REFINE, ("refineCol", (), 0)) \
        == effect_sig_of(FUNDED, ("addCol", (0,)))
    assert sig_of(REFINE, ("refineCol", (), 0)) \
        != sig_of(FUNDED, ("addCol", (0,)))
    assert erase_guard(CLASS_SIGS["refineObservation"]) \
        == erase_guard(CLASS_SIGS["extendObservation"])


def test_declared_code_is_not_a_contextual_congruence() -> None:
    rep = contextual_countermodel_report()
    assert rep["occurrence_same_start_equal_code"] is True
    assert rep["occurrence_common_suffix_separates"] is True
    assert rep["budget_same_start_equal_code"] is True
    assert rep["budget_common_suffix_separates"] is True
    assert rep["safe_for_event_erasure"] is False


def test_witnesses_are_minimal_in_the_declared_space() -> None:
    rep = witness_report()
    assert rep["search_space_states"] == 6144
    wits = rep["witnesses"]
    assert isinstance(wits, dict)
    assert sorted(wits) == sorted(ALL_CLASSES)
    for name, entry in wits.items():
        assert isinstance(entry, dict)
        assert entry["signature"] == sig_json(CLASS_SIGS[name])
        assert isinstance(entry["witnesses_at_minimum_size"], int)
        assert entry["witnesses_at_minimum_size"] >= 1
    supply = wits["supplyOccurrence"]
    assert isinstance(supply, dict)
    assert supply["minimum_size"] == 0


def test_non_invariant_components_and_scope() -> None:
    rep = invariance_report()
    assert rep["obstruction_split_untouched"] == "untouched"
    assert rep["obstruction_split_preserved"] == "preserved"
    assert rep["budget_delta_rewritten"] == "rewritten"
    assert rep["budget_delta_spent_one_by_environment"] == "spentOne"
    assert rep["funded_guards_always_spend_one"] is True
    assert rep["refusal_always_preserved"] == "preserved"
    assert rep["outside_class_retention_creates"] is True
    assert rep["licence_separates_refine_from_extend"] is True


def test_wellformedness_is_load_bearing() -> None:
    # outside the declared class, retention itself creates an obstruction
    assert not wf_class(OUTSIDE)
    assert wf_class(OBSTRUCTED)
    assert not wf_class(replace(GENESIS_P, halted=True))
    assert accepted(OUTSIDE, ("admitWit", 0, 1))
    assert obst_effect(OUTSIDE, pstep(OUTSIDE, ("admitWit", 0, 1))) \
        == "created"
    # inside the class it never does
    for s in enumerate_states():
        if wf_class(s) and accepted(s, ("admitWit", 0, 1)):
            assert class_of(s, ("admitWit", 0, 1)) == "retainDifference"


def test_policy_class_is_not_provenance() -> None:
    rep = ownership_report()
    assert rep["no_occurrence_supply_emitted"] is True
    assert rep["no_license_write_emitted"] is True
    assert rep["no_terminal_emitted"] is True
    # the claim as stated is FALSE for the budget write
    assert rep["budget_write_claim_refuted"] is True
    assert rep["only_unit_funding_emitted"] is True
    assert rep["externally_classified_emitted_internally"] == ["setBudget"]
    assert rep["classification_is_provenance"] is False
    assert "setBudget" in ENV_OWNED
    block = (("setBudget", 1), ("addCol", (0,)))
    assert block in next_family_p(OBSTRUCTED)
    witness = rep["refutation_witness"]
    assert isinstance(witness, dict)
    assert witness["block_is_generated"] is True


def test_serialization_helpers() -> None:
    assert state_json(GENESIS_P)["obs"] is None
    assert state_json(OBSTRUCTED)["obs"] == []
    assert state_json(REFINE)["obs"] == [[]]
    assert event_json(("addCol", (0, 1))) == ["addCol", [0, 1]]
    assert event_json(("setLicense", False)) == ["setLicense", False]
    assert sig_json(CLASS_SIGS["writeBudget"])["fields"] == ["budget"]
    assert state_size(GENESIS_P) == 0
    assert state_size(REFINE) == 8
    assert state_size(OBSTRUCTED) == 6


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_transition_alphabet.main(["--artifacts", str(d1)]) == 0
    assert run_transition_alphabet.main(["--artifacts", str(d2)]) == 0
    assert (d1 / "transition_alphabet.json").read_bytes() == \
        (d2 / "transition_alphabet.json").read_bytes()

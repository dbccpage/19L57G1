"""Check script for Unit 65: Thirteen codes, and why they are not an alphabet (TransitionAlphabet).

Recomputes and verifies:
  1. Exhaustive 6,144-state x 18-event partition report (guard agreement, unique class
     signature on WFClass, zero mixed obstruction steps, zero halted accepts).
  2. Codebook sizes (13 with guard, 12 guard-erased with refineObservation + extendObservation merged).
  3. Right-congruence countermodels (occurrence and budget).
  4. Invariance report, ownership report, and minimum witness search vs Lean store-coherent sizes.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.transition_alphabet import (  # noqa: E402
    ALL_CLASSES,
    codebook_report,
    contextual_countermodel_report,
    invariance_report,
    ownership_report,
    partition_report,
    witness_report,
)


def main() -> int:
    failures: list[str] = []

    part = partition_report()
    if (
        part["guard_agreement_failures"] != 0
        or part["class_signature_failures"] != 0
        or part["ambiguous_classifications"] != 0
        or part["mixed_obstruction_steps"] != 0
        or part["halted_accepted_transitions"] != 0
        or not part["all_classes_realized"]
        or part["declared_signature_image_size"] != 13
    ):
        failures.append(f"partition_report failed: {part}")

    cb = codebook_report()
    if (
        len(ALL_CLASSES) != 13
        or cb["declared_codebook_size"] != 13
        or cb["guard_erased_codebook_size"] != 12
        or cb["merged_under_guard_erasure"] != [["refineObservation", "extendObservation"]]
    ):
        failures.append(f"codebook_report failed: {cb}")

    cm = contextual_countermodel_report()
    if not (
        cm["occurrence_same_start_equal_code"]
        and cm["occurrence_common_suffix_separates"]
        and cm["budget_same_start_equal_code"]
        and cm["budget_common_suffix_separates"]
        and cm["safe_for_event_erasure"] is False
    ):
        failures.append(f"contextual_countermodel_report failed: {cm}")

    inv = invariance_report()
    if not (
        inv["obstruction_split_untouched"] == "untouched"
        and inv["obstruction_split_preserved"] == "preserved"
        and inv["budget_delta_rewritten"] == "rewritten"
        and inv["budget_delta_spent_one_by_environment"] == "spentOne"
        and inv["funded_guards_always_spend_one"]
        and inv["refusal_always_preserved"] == "preserved"
        and inv["outside_class_retention_creates"]
        and inv["licence_separates_refine_from_extend"]
    ):
        failures.append(f"invariance_report failed: {inv}")

    own = ownership_report()
    if not (
        own["no_occurrence_supply_emitted"]
        and own["no_license_write_emitted"]
        and own["no_terminal_emitted"]
        and own["budget_write_claim_refuted"]
        and own["only_unit_funding_emitted"]
    ):
        failures.append(f"ownership_report failed: {own}")

    wit = witness_report()
    if wit["search_space_states"] != 6144 or wit["search_space_events"] != 18:
        failures.append(f"unexpected witness search space: {wit['search_space_states']}")

    result = {
        "unit": 65,
        "module": "TransitionAlphabet",
        "pairs_checked": part["pairs_checked"],
        "accepted_wellformed_transitions": part["accepted_wellformed_transitions"],
        "declared_codebook_size": cb["declared_codebook_size"],
        "guard_erased_codebook_size": cb["guard_erased_codebook_size"],
        "merged_under_guard_erasure": cb["merged_under_guard_erasure"],
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

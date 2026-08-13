"""Produce the one-step transition-codebook artifact deterministically.

Usage: python code/run_transition_alphabet.py [--artifacts DIR]

Writes ``transition_alphabet.json``: the exhaustive partition check
over the declared finite state space (guard agreement, one class per
accepted transition of a well-formed state, no mixed obstruction step,
nothing accepted at a halted state); the declared code-image sizes with
and without the discharged guard, and the merge the erasure produces;
the exhaustive minimum witness for every class; the two profile
components that are provably not invariants of the transition; and the
policy-class audit of the internal response generator, including the
refutation of the claim that no externally classified constructor is
ever generated internally; and explicit failures of contextual
congruence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.transition_alphabet import (
    EVENT_BATTERY,
    codebook_report,
    contextual_countermodel_report,
    enumerate_states,
    invariance_report,
    ownership_report,
    partition_report,
    witness_report,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    args = parser.parse_args(argv)
    payload: dict[str, Json] = {
        "bounds": {
            "occurrence_positions": 2,
            "pair_pool": [[0, 1], [1, 0]],
            "observation_pool": 4,
            "budget_pool": [0, 1],
            "refusal_pool": 2,
            "state_space": sum(1 for _ in enumerate_states()),
            "event_battery": len(EVENT_BATTERY),
        },
        "imported_inputs": [
            "the sealed passage step function and its guards",
            "occurrence supply (externally classified)",
            "budget authority (externally classified, but internally "
            "emitted as a unit funding write)",
            "license authority (externally classified)",
            "the terminal declaration (externally classified)",
            "the declared well-formed class: live, protection "
            "contained in retention",
        ],
        "scope": {
            "minimality": ("minimum over the declared well-formed class "
                           "inside the declared finite state space, not "
                           "over states reachable from genesis"),
            "partition": ("exhaustive over the declared state space and "
                          "event battery; the Lean proof is universal"),
            "codebook": ("a declared one-step projection, not a quotient, "
                         "right congruence, DDA map, or presentation-"
                         "invariant cardinality"),
        },
        "partition": partition_report(),
        "codebook": codebook_report(),
        "contextual_countermodels": contextual_countermodel_report(),
        "witnesses": witness_report(),
        "invariance": invariance_report(),
        "ownership": ownership_report(),
    }
    out_path = args.artifacts / "transition_alphabet.json"
    write_json(out_path, payload)
    part = payload["partition"]
    assert isinstance(part, dict)
    print(f"partition: pairs={part['pairs_checked']} "
          f"accepted={part['accepted_wellformed_transitions']} "
          f"guard_fail={part['guard_agreement_failures']} "
          f"class_fail={part['class_signature_failures']} "
          f"ambiguous={part['ambiguous_classifications']}")
    codes = payload["codebook"]
    assert isinstance(codes, dict)
    print(f"codebook: declared={codes['declared_codebook_size']} "
          f"guard_erased={codes['guard_erased_codebook_size']} "
          f"merged={codes['merged_under_guard_erasure']}")
    own = payload["ownership"]
    assert isinstance(own, dict)
    print(f"policy-class: emitted={own['constructors_emitted_internally']} "
          f"budget_claim_refuted={own['budget_write_claim_refuted']} "
          f"only_unit_funding={own['only_unit_funding_emitted']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

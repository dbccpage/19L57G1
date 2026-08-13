"""Produce the transition-alphabet artifact deterministically.

Usage: python code/run_transition_alphabet.py [--artifacts DIR]

Writes ``transition_alphabet.json``: the exhaustive partition check
over the declared finite state space (guard agreement, one class per
accepted transition of a well-formed state, no mixed obstruction step,
nothing accepted at a halted state); the derived letter counts with
and without the discharged guard, and the merge the erasure produces;
the exhaustive minimum witness for every class; the two profile
components that are provably not invariants of the transition; and the
environment-ownership audit of the internal response generator,
including the refutation of the claim that no environment-owned
constructor is ever generated internally."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.transition_alphabet import (
    EVENT_BATTERY,
    alphabet_report,
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
            "occurrence supply (environment-owned)",
            "budget authority (environment-owned, but internally "
            "emitted as a unit funding write)",
            "license authority (environment-owned)",
            "the terminal declaration (environment-owned)",
            "the declared well-formed class: live, protection "
            "contained in retention",
        ],
        "scope": {
            "minimality": ("minimum over the declared well-formed class "
                           "inside the declared finite state space, not "
                           "over states reachable from genesis"),
            "partition": ("exhaustive over the declared state space and "
                          "event battery; the Lean proof is universal"),
        },
        "partition": partition_report(),
        "alphabet": alphabet_report(),
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
    alpha = payload["alphabet"]
    assert isinstance(alpha, dict)
    print(f"alphabet: with_guard={alpha['alphabet_size_with_guard']} "
          f"guard_erased={alpha['alphabet_size_guard_erased']} "
          f"merged={alpha['merged_under_guard_erasure']}")
    own = payload["ownership"]
    assert isinstance(own, dict)
    print(f"ownership: emitted={own['constructors_emitted_internally']} "
          f"budget_claim_refuted={own['budget_write_claim_refuted']} "
          f"only_unit_funding={own['only_unit_funding_emitted']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

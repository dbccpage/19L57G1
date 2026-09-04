"""Write the deterministic receipt for the reach_additivity run.

No timestamps, no environment data, sorted keys: the file must regenerate
byte-identically.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import survey  # noqa: E402

RECEIPT = HERE / "receipts" / "reach_additivity.json"


def build() -> dict[str, object]:
    return {
        "authority_effect": "None",
        "write_root": "research/reach_additivity/",
        "snapshot": "7fcd72f6",
        "declared": {
            "composition": "concatenation of item sequences; declared, not discovered",
            "difference_cost": "diff_P(base, delta) = P(apply(base, delta)) - P(base)",
            "functionals": sorted(survey.add.FUNCTIONALS),
            "rectangle": (
                "the sealed readings' genesis states plus every state reachable by"
                " up to two valid one-item responses, deduplicated by regime equality"
            ),
            "depth": survey.DEPTH,
        },
        "rectangle_size": len(survey.rectangle()),
        "sequential": survey.sequential_survey(),
        "additivity": survey.additivity_survey(),
        "self_loops": survey.self_loop_survey(),
        "circulation": survey.circulation_witness(),
        "assumptions": {
            "A1": (
                "composition is declared as concatenation; a declaration that"
                " renumbered the second response against the intermediate state"
                " is a different operation and is not run here"
            ),
            "A2": (
                "the rectangle is reachability-bounded at depth two; a count here"
                " is a count over that rectangle and not over the states"
            ),
            "A3": (
                "the sealed enumerator remains the authority on which responses"
                " exist; the constructed self-loop probes ask the absorption"
                " question directly and are labelled as constructed, not enumerated"
            ),
            "A4": (
                "additivity is a property of every difference cost, so observing it"
                " for one functional is evidence about the shape of the cost and"
                " not about the choice of functional"
            ),
            "A5": (
                "zero circulation is a limitation, not a virtue; nothing here says"
                " a difference cost is a good cost"
            ),
        },
    }


def main() -> int:
    data = build()
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    RECEIPT.write_text(text, "utf-8", newline="\n")
    seq = data["sequential"]
    assert isinstance(seq, dict)
    loops = data["self_loops"]
    assert isinstance(loops, dict)
    print(
        f"sequential: {seq['states_agree']}/{seq['triples']} triples agree,"
        f" {seq['event_tuples_agree']} event tuples identical"
    )
    print(
        f"self-loops: {loops['bases_carrying_a_self_loop']}"
        f"/{loops['bases']} bases carry one;"
        f" enumerated kinds {loops['enumerated_self_loops_by_kind']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

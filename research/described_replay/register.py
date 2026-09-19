"""Five-stage terminal register and priced leftovers.

This register combines already computed stage payloads.  It starts no new
frontier search.  AuthorityEffect: None.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from class_replay import (
    render_class_replay,
    render_description_stage,
    render_stepper_stage,
)
from cost_ledger import render_cost_ledger
from diagonal import render_diagonal_stage


HERE = Path(__file__).resolve().parent


def render_register() -> dict[str, object]:
    description = render_description_stage()
    stepper = render_stepper_stage()
    class_replay = render_class_replay()
    diagonal = render_diagonal_stage()
    cost = render_cost_ledger()
    reporter = diagonal["reporter_search"]
    self_description = diagonal["self_description"]
    assert isinstance(reporter, dict)
    assert isinstance(self_description, dict)
    stages = [
        {
            "scope": "DR-C-2-1-3 with datum alphabet 2, event alphabet 9, arity at most 1, history length at most 3",
            "stage": "Description",
            "terminal": description["terminal"],
            "terminal_claims": [
                {
                    "code": description["terminal"],
                    "evidence_class": "PROVED_THEOREM",
                    "lean_evidence": [
                        "decode_encode_id",
                        "encode_injective",
                        "encode_admission_only",
                        "supply_inertia",
                    ],
                    "scope": "DR-C-2-1-3 with datum alphabet 2, event alphabet 9, arity at most 1, history length at most 3",
                }
            ],
            "python_observation": {
                "evidence_class": "FINITE_COMPUTATION",
                "receipt": "receipts/python/description.json",
            },
        },
        {
            "scope": "decoded DR-C-2-1-3 descriptions, one event per successful step",
            "stage": "Stepper",
            "terminal": stepper["terminal"],
            "terminal_claims": [
                {
                    "code": stepper["terminal"],
                    "evidence_class": "PROVED_THEOREM",
                    "lean_evidence": [
                        "stepper_one",
                        "stepper_current_mismatch",
                        "preparation_dispatch_decode_failure",
                        "preparation_dispatch_total",
                        "stepper_full_iteration",
                        "stepper_iterate",
                        "stepper_total",
                    ],
                    "scope": "decoded DR-C-2-1-3 descriptions with datum alphabet 2, event alphabet 9, arity at most 1, history length at most 3; one event per successful step",
                }
            ],
            "python_observation": {
                "evidence_class": "FINITE_COMPUTATION",
                "receipt": "receipts/python/stepper.json",
            },
        },
        {
            "scope": "DR-C-2-1-3: two datum symbols, nine event symbols, arity at most 1, history length at most 3; every fixed-history candidate and every described target",
            "stage": "ClassReplay",
            "terminal": class_replay["terminal"],
            "terminal_claims": [
                {
                    "code": class_replay["terminal"],
                    "evidence_class": "PROVED_THEOREM",
                    "lean_evidence": ["fixed_candidate_no_class_replay"],
                    "scope": "DR-C-2-1-3 with two datum symbols, nine event symbols, arity at most 1, and history length at most 3; every fixed-history candidate and every described target",
                }
            ],
            "python_observation": {
                "evidence_class": "FINITE_COMPUTATION",
                "receipt": "receipts/python/class_replay.json.gz",
            },
        },
        {
            "scope": "DR-C-2-1-3: two datum symbols, nine event symbols, arity at most 1, history length at most 3; self-description and fixed terminal reports at described-run cost at most 6",
            "stage": "Diagonal",
            "terminal": [
                self_description["terminal"],
                reporter["terminal"],
                "OPEN_UNBOUNDED",
            ],
            "terminal_claims": [
                {
                    "code": self_description["terminal"],
                    "evidence_class": "PROVED_THEOREM",
                    "lean_evidence": [
                        "empty_self_description_witness",
                        "nonempty_description_outside_class",
                        "empty_self_replay_witness",
                    ],
                    "scope": "DR-C-2-1-3 with two datum symbols, nine event symbols, arity at most 1, and history length at most 3",
                },
                {
                    "code": reporter["terminal"],
                    "evidence_class": "PROVED_THEOREM",
                    "lean_evidence": [
                        "candidate_report_uses_described_replay",
                        "bounded_reporter_diagonal_member",
                        "diagonal_disagrees",
                        "no_fixed_candidate_reporter",
                    ],
                    "scope": "DR-C-2-1-3 with two datum symbols, nine event symbols, arity at most 1, history length at most 3, and candidate-step plus target-description cost at most 6",
                },
                {
                    "code": "OPEN_UNBOUNDED",
                    "evidence_class": "OPEN",
                    "lean_evidence": [],
                    "scope": "reporting outside DR-C-2-1-3 or beyond candidate-step plus target-description cost 6",
                },
            ],
            "python_observation": {
                "evidence_class": "FINITE_COMPUTATION",
                "receipt": "receipts/python/diagonal.json.gz",
            },
        },
        {
            "scope": "one imposed pair, arity at most 1, at most one fresh datum, one fresh form, and two response items",
            "stage": "CostLedger",
            "terminal": [cost["terminal"], "OPEN_UNBOUNDED"],
            "terminal_claims": [
                {
                    "code": cost["terminal"],
                    "evidence_class": "FINITE_COMPUTATION",
                    "lean_evidence": [],
                    "scope": "one imposed pair, arity at most 1, at most one fresh datum, at most one fresh form, and at most two response items",
                },
                {
                    "code": "OPEN_UNBOUNDED",
                    "evidence_class": "OPEN",
                    "lean_evidence": [],
                    "scope": "response families beyond the declared one-pair, arity-1, one-fresh-datum, one-fresh-form, two-item bounds",
                },
            ],
            "python_observation": {
                "evidence_class": "FINITE_COMPUTATION",
                "receipt": "receipts/python/cost_ledger.json",
            },
        },
    ]
    leftovers = [
        {
            "code": "CROSS_LANGUAGE_EQUIVALENCE",
            "evidence_class": "OPEN",
            "price": "define a typed correspondence between the Python and Lean reconstructions and prove every constructor, decoder, step, and terminal commutes; no such bridge is declared here",
        },
        {
            "code": "ENLARGED_CLASS",
            "evidence_class": "OPEN",
            "price": "declare new finite alphabets and bounds, add an input-reading event or prove its absence, then rebuild the complete candidate-target matrix",
        },
        {
            "code": "UNBOUNDED_REPORTING",
            "evidence_class": "OPEN",
            "price": "quantify over every admitted finite description length and construct a reporting member or a closure-preserving disagreement member",
        },
        {
            "code": "UNBOUNDED_COST_LEDGER",
            "evidence_class": "OPEN",
            "price": "define one cost-indexed family for every response bound and prove a statement uniform in that bound",
        },
        {
            "code": "ALL_POLICY_QUOTIENT_FRONTIER",
            "evidence_class": "OPEN",
            "price": "declare the finite generator family and resource bounds, construct its quotient tree, and construct each single-policy embedding",
        },
        {
            "code": "OB1_UNCHANGED",
            "evidence_class": "OPEN",
            "price": "construct an object-language challenge source or prove a result for a wider declared class; neither act occurs here",
        },
    ]
    return {
        "authority_effect": None,
        "class_id": "DR-C-2-1-3",
        "frontier_started": False,
        "leftovers": leftovers,
        "local_opens": ["CROSS_LANGUAGE_EQUIVALENCE"],
        "opens_unchanged": [
            "OB1_UNCHANGED",
            "S66_UNCHANGED",
            "S9_LAST_UNCHANGED",
        ],
        "stages": stages,
        "terminal": "REGISTER_WRITTEN",
        "unbounded": "OPEN_UNBOUNDED",
    }


def render_tau() -> dict[str, object]:
    register = render_register()
    description = render_description_stage()
    stepper = render_stepper_stage()
    class_replay = render_class_replay()
    diagonal = render_diagonal_stage()
    cost = render_cost_ledger()
    stages = register["stages"]
    assert isinstance(stages, list)
    reporter = diagonal["reporter_search"]
    self_description = diagonal["self_description"]
    outside = diagonal["outside_exhaustion"]
    cost_rows = cost["rows"]
    assert isinstance(reporter, dict)
    assert isinstance(self_description, dict)
    assert isinstance(outside, dict)
    assert isinstance(cost_rows, list)
    terminal_rows: list[dict[str, object]] = []
    for stage in stages:
        assert isinstance(stage, dict)
        claims = stage["terminal_claims"]
        assert isinstance(claims, list)
        for claim in claims:
            assert isinstance(claim, dict)
            terminal_rows.append(
                {
                    "code": claim["code"],
                    "evidence_class": claim["evidence_class"],
                    "lean_evidence": claim["lean_evidence"],
                    "scope": claim.get("scope", stage["scope"]),
                }
            )
    terminal_rows.append(
        {
            "code": "REGISTER_WRITTEN",
            "evidence_class": "FINITE_COMPUTATION",
            "lean_evidence": [],
            "scope": "the five ordered DR-C-2-1-3 stages and the priced leftovers",
        }
    )
    terminal_rows.extend(
        [
            {
                "code": "OB1_UNCHANGED",
                "evidence_class": "OPEN",
                "lean_evidence": [],
                "scope": "unchanged from the pinned challenge-source span",
            },
            {
                "code": "S66_UNCHANGED",
                "evidence_class": "OPEN",
                "lean_evidence": [],
                "scope": "unchanged under the frozen run charter",
            },
            {
                "code": "S9_LAST_UNCHANGED",
                "evidence_class": "OPEN",
                "lean_evidence": [],
                "scope": "unchanged under the frozen run charter",
            },
        ]
    )
    class_size = class_replay["candidate_count"]
    matrix_size = class_replay["matrix_cell_count"]
    certified_pairs = class_replay["class_reproduction_success_count"]
    assert isinstance(class_size, int)
    assert isinstance(matrix_size, int)
    assert isinstance(certified_pairs, int)
    winners = class_replay["successful_candidate_indices"]
    assert isinstance(winners, list)
    check_costs: list[dict[str, object]] = []
    find_costs: list[dict[str, object]] = []
    for row in cost_rows:
        assert isinstance(row, dict)
        responses = row["supplied_responses"]
        assert isinstance(responses, list)
        check_costs.append(
            {
                "measure": row["measure"],
                "values": [
                    response["check_cost"]
                    for response in responses
                    if isinstance(response, dict)
                ],
            }
        )
        find_costs.append(
            {"measure": row["measure"], "value": row["finding_cost"]}
        )
    stage_register_complete = (
        len(stages) == 5
        and description["terminal"] == "DESCRIPTION_PROVED"
        and stepper["terminal"] == "STEPPER_PROVED"
        and class_replay["terminal"]
        in {
            "MEMBER_REPLAYS_CLASS_PROVED",
            "MEMBER_REPLAYS_CLASS_BOUNDED",
            "NO_SUCH_MEMBER_IN_CLASS",
        }
        and self_description["terminal"]
        in {"SELF_DESCRIBING_EXHIBITED", "SELF_DESCRIPTION_REFUSED_IN_CLASS"}
        and reporter["terminal"]
        in {"DECIDER_WITHIN_COST_EXHIBITED", "DECIDER_REFUSED_WITHIN_COST"}
        and cost["terminal"] == "COST_TABLE_WRITTEN"
        and register["terminal"] == "REGISTER_WRITTEN"
        and register["frontier_started"] is False
    )
    return {
        "authority_effect": None,
        "census_pin_regenerated": False,
        "class_declaration": {
            "alphabet": 9,
            "arity_bound": 1,
            "class_id": "DR-C-2-1-3",
            "class_size": class_size,
            "datum_alphabet": 2,
            "length_bound": 3,
        },
        "class_replay": {
            "certified_pairs": certified_pairs,
            "failures": matrix_size - certified_pairs,
            "member": winners if winners else "none",
            "terminal": class_replay["terminal"],
        },
        "cost_ledger": {
            "check_costs": check_costs,
            "find_costs": find_costs,
            "largest_row": cost["largest_completed_row"],
            "rows": len(cost_rows),
            "terminal": cost["terminal"],
            "unbounded": "OPEN_UNBOUNDED",
        },
        "description": {
            "endpoint_countermodel": [0, 1],
            "price_rule": "one_description_admission_per_source_event",
            "terminal": description["terminal"],
        },
        "diagonal": {
            "decider_by_exhaustion_cost": outside["aggregate_cost"],
            "decider_within_declared_cost": reporter["terminal"],
            "self_description": self_description["terminal"],
            "unbounded": "OPEN_UNBOUNDED",
        },
        "final_state": False,
        "leftover": register["leftovers"],
        "opens_unchanged": register["opens_unchanged"],
        "outside_bet_hash": "5534f09d5cfcbb20b45fdc1ee42c615d4af224c5ced973dda5b74d522bb1cfd6",
        "predictions_hashes": [
            sha256((HERE / "PREDICTIONS.md").read_bytes()).hexdigest()
        ],
        "publication_complete": False,
        "publication_completion": "author acceptance and merge are outside this run",
        "prompt_hash_native": sha256((HERE / "PROMPT.md").read_bytes()).hexdigest(),
        "sealed_paths_touched": [],
        "shared_files_touched": [],
        "snapshot": "f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be",
        "stepper": {
            "defined_through_replay": stepper["defined_through_replay"],
            "terminal": stepper["terminal"],
        },
        "stage_register_complete": stage_register_complete,
        "steps_completed": [
            "Description",
            "Stepper",
            "ClassReplay",
            "Diagonal",
            "CostLedger",
        ],
        "terminals": terminal_rows,
        "write_root": "research/described_replay/",
    }

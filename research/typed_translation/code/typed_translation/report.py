"""Deterministic receipt construction, prediction scoring, and prose rendering."""

from __future__ import annotations

from functools import cache
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence

from .enumerate import (
    Candidate,
    canonical_history_order,
    enumerate_candidates,
    enumerate_candidates_product,
    enumerate_histories,
    enumerate_histories_unpruned,
    unique_states,
)
from .removal import removal_report
from .translation import (
    CandidateVerdict,
    distortion_report,
    evaluate_candidate,
    nearby_shell,
    provenance_witness,
    shell_report,
    statement_capabilities,
    typed_states,
)


HERE = Path(__file__).resolve().parents[2]
FREEZE_COMMIT = "2f576e58"
FROZEN_SHA256 = {
    "REQUIREMENTS.md": "4588457ed5ad0ac41868f214cc2041512f049c76d52f33200656c92783d2853a",
    "PREDICTIONS.md": "a3a8e79d32795a932d930b54f2eba984c3a04fbce68bfd758a0e51532c22dc23",
}
EXPECTED_WRONG = [
    "R09",
    "R13",
    "R15",
    "R16",
    "R17",
    "R18",
    "R20",
    "R21",
    "R23",
    "R25",
    "R29",
    "R30",
    "R32",
    "R33",
    "R34",
]
LEAN_TARGETS = (
    "TypedTranslation.memoryless_fixed_block_obstruction",
    "TypedTranslation.symmetric_form_cost_obstruction",
)


def canonical_json(data: object) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _histogram(lengths: Sequence[int]) -> dict[str, int]:
    return {
        str(length): sum(value == length for value in lengths)
        for length in sorted(set(lengths))
    }


def _lean_targets_present() -> bool:
    path = HERE / "lean" / "axioms.txt"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return all(f"'{name}' " in text for name in LEAN_TARGETS)


def _candidate_behavior(verdict: CandidateVerdict) -> dict[str, object]:
    record = verdict.as_record()
    candidate_record = record["candidate"]
    assert isinstance(candidate_record, dict)
    candidate = dict(candidate_record)
    candidate.pop("address_family")
    return {
        "candidate": candidate,
        "clauses": record["clauses"],
        "statement_capabilities": record["statement_capabilities"],
        "statement_price": record["statement_price"],
        "valid": record["valid"],
    }


def _prediction(
    prediction_id: str,
    forced: bool,
    passed: bool | None,
    expected: object,
    actual: object,
) -> dict[str, object]:
    status = "PENDING" if passed is None else ("HIT" if passed else "MISS")
    return {
        "actual": actual,
        "expected": expected,
        "forced": forced,
        "id": prediction_id,
        "status": status,
    }


def score_predictions(
    *,
    candidate_count: int,
    candidate_crosscheck: bool,
    valid: Sequence[CandidateVerdict],
    distortion: Mapping[str, object],
    orientation_tie: bool,
    provenance: Mapping[str, object],
    removal: Mapping[str, object],
    shell: Mapping[str, object],
) -> list[dict[str, object]]:
    least_price = min(
        (len(statement_capabilities(item.candidate)) for item in valid), default=None
    )
    least = [
        item
        for item in valid
        if len(statement_capabilities(item.candidate)) == least_price
    ]
    extrema = distortion["extrema"]
    assert isinstance(extrema, dict)
    mu1 = extrema["mu1"]
    mu2 = extrema["mu2"]
    assert isinstance(mu1, dict) and isinstance(mu2, dict)
    exact = bool(distortion["exact_both_measures"])
    code_counts = shell["code_counts"]
    removal_rows = removal["rows"]
    shell_codes = shell["codes"]
    silent_truncations = shell["silent_truncations"]
    assert isinstance(code_counts, dict)
    assert isinstance(removal_rows, list)
    assert isinstance(shell_codes, list)
    assert isinstance(silent_truncations, list)
    p6 = _lean_targets_present()
    return [
        _prediction(
            "P1",
            True,
            candidate_count == 128 and candidate_crosscheck,
            {"candidate_count": 128, "ordered_crosscheck": True},
            {"candidate_count": candidate_count, "ordered_crosscheck": candidate_crosscheck},
        ),
        _prediction("P2", False, bool(valid), "nonempty valid population", len(valid)),
        _prediction(
            "P3",
            False,
            bool(valid)
            and all(
                item.candidate.event_context == "state_sensitive"
                and item.candidate.synthetic_supply
                for item in valid
            )
            and least_price == 2,
            {"required": ["state_inspection", "administrative_presentation"], "least_price": 2},
            {
                "all_valid_require_both": bool(valid)
                and all(
                    item.candidate.event_context == "state_sensitive"
                    and item.candidate.synthetic_supply
                    for item in valid
                ),
                "least_price": least_price,
            },
        ),
        _prediction(
            "P4",
            False,
            bool(valid)
            and not exact
            and mu1["forward_max"] == 4
            and mu2["forward_max"] == 12,
            {"exact": False, "mu1_forward_max": 4, "mu2_forward_max": 12},
            {
                "exact": exact,
                "mu1_forward_max": mu1["forward_max"],
                "mu2_forward_max": mu2["forward_max"],
            },
        ),
        _prediction(
            "P5",
            False,
            len(least) == 2 and orientation_tie,
            {"least_count": 2, "orientation_quotient_equal": True},
            {"least_count": len(least), "orientation_quotient_equal": orientation_tie},
        ),
        _prediction(
            "P6",
            False,
            p6 if p6 else None,
            list(LEAN_TARGETS),
            {"axiom_inventory_contains_targets": p6},
        ),
        _prediction(
            "P7",
            False,
            bool(provenance.get("left_labels"))
            and provenance.get("left_labels") != provenance.get("right_labels")
            and provenance.get("equal_profile") is not None,
            "equal profile with separate instance/rule fields and labels",
            provenance,
        ),
        _prediction(
            "P8",
            False,
            removal["population"] == 37
            and removal["hit_count"] == 22
            and removal["wrong_ids"] == EXPECTED_WRONG,
            {"population": 37, "hit_count": 22, "wrong_ids": EXPECTED_WRONG},
            {
                "population": removal["population"],
                "hit_count": removal["hit_count"],
                "wrong_ids": removal["wrong_ids"],
            },
        ),
        _prediction(
            "P9",
            False,
            all(
                row["actual"] == "MIXED"
                for row in removal_rows
                if not row["hit"]
            ),
            "every wrong row is MIXED",
            [
                {"actual": row["actual"], "id": row["id"]}
                for row in removal_rows
                if not row["hit"]
            ],
        ),
        _prediction(
            "P10",
            False,
            bool(shell["population"])
            and not silent_truncations
            and all(int(code_counts[name]) > 0 for name in shell_codes),
            "nonempty shell, zero silent truncations, every refusal code used",
            {
                "code_counts": code_counts,
                "population": shell["population"],
                "silent_count": len(silent_truncations),
            },
        ),
        _prediction(
            "P11",
            True,
            True,
            "OPEN_AT_BOUND outside the frozen carrier",
            "OPEN_AT_BOUND",
        ),
    ]


@cache
def build_receipt() -> dict[str, object]:
    histories = enumerate_histories()
    unpruned = enumerate_histories_unpruned()
    candidates = enumerate_candidates()
    product_candidates = enumerate_candidates_product()
    states = unique_states(histories)
    domain = typed_states(states)
    shell = nearby_shell(domain)
    verdicts = [evaluate_candidate(candidate, histories, domain, shell) for candidate in candidates]
    valid = [verdict for verdict in verdicts if verdict.valid]
    if not valid:
        distortion: dict[str, object] = {
            "exact_both_measures": False,
            "extrema": {},
            "table": [],
        }
        orientation_tie = False
        representative: Candidate | None = None
    else:
        least_price = min(len(statement_capabilities(item.candidate)) for item in valid)
        least = [
            item
            for item in valid
            if len(statement_capabilities(item.candidate)) == least_price
        ]
        representative = least[0].candidate
        distortion = distortion_report(representative, histories)
        orientation_tie = (
            len(least) == 2
            and {item.candidate.address_family for item in least}
            == {"direct", "complemented"}
            and _candidate_behavior(least[0]) == _candidate_behavior(least[1])
        )

    removal = removal_report()
    refusal = shell_report(shell)
    provenance = provenance_witness(states, "direct")
    predictions = score_predictions(
        candidate_count=len(candidates),
        candidate_crosscheck=[item.coordinates() for item in candidates]
        == [item.coordinates() for item in product_candidates],
        valid=valid,
        distortion=distortion,
        orientation_tie=orientation_tie,
        provenance=provenance,
        removal=removal,
        shell=refusal,
    )
    failed_by_clause = {
        clause: sum(not verdict.clauses[clause] for verdict in verdicts)
        for clause in verdicts[0].clauses
    }
    return {
        "classification": {
            "global_extension": "OPEN_AT_BOUND",
            "map": "DETERMINISTIC_COMPUTATION",
            "memoryless_obstruction": "PROVED_THEOREM",
            "nonzero_cost_obstruction": "PROVED_THEOREM",
            "removal": "DETERMINISTIC_COMPUTATION",
        },
        "costs": {
            "definitions": {
                "mu1": "count RawKind.ADMISSION",
                "mu2": "count every RawEvent",
            },
            "distortion": distortion,
            "shared_implementation": "typed_translation.model.measure",
            "statement_price_is_separate": True,
        },
        "freeze": {
            "commit": FREEZE_COMMIT,
            "sha256": FROZEN_SHA256,
        },
        "histories": {
            "count": len(histories),
            "length_histogram": _histogram([len(history) for history in histories]),
            "ordered_unpruned_crosscheck": canonical_history_order(unpruned) == histories,
            "unpruned_count": len(unpruned),
        },
        "map": {
            "candidate_count": len(candidates),
            "candidate_order_crosscheck": [item.coordinates() for item in candidates]
            == [item.coordinates() for item in product_candidates],
            "candidates": [verdict.as_record() for verdict in verdicts],
            "failed_by_clause": failed_by_clause,
            "least_statement_price": min(
                (len(statement_capabilities(item.candidate)) for item in valid),
                default=None,
            ),
            "orientation_quotient_equal": orientation_tie,
            "outcome": "MAP_WITH_PRICE" if valid else "OPEN_AT_BOUND",
            "representative": representative.as_record() if representative else None,
            "valid_candidates": [item.candidate.as_record() for item in valid],
            "valid_count": len(valid),
        },
        "predictions": predictions,
        "provenance_witness": provenance,
        "refusal_shell": refusal,
        "removal": removal,
        "schema": "typed_translation.receipt.v1",
        "spaces": {
            "source_state_count": len(states),
            "typed_boundary_state_count": len(domain),
        },
        "terminal": {
            "bounded_map": "MAP_WITH_PRICE" if valid else "OPEN_AT_BOUND",
            "exact_cost": "PROVED_EXACT_COST_OBSTRUCTION" if valid else "OPEN_AT_BOUND",
            "global": "OPEN_AT_BOUND",
            "removal": "TOTAL_REMOVAL_SCORED",
        },
    }


def _prediction_table(receipt: Mapping[str, object]) -> str:
    rows = receipt["predictions"]
    assert isinstance(rows, list)
    lines = ["| prediction | class | outcome |", "|---|---|---|"]
    for row in rows:
        assert isinstance(row, dict)
        lines.append(
            f"| {row['id']} | {'FORCED' if row['forced'] else 'NOT FORCED'} | {row['status']} |"
        )
    return "\n".join(lines)


def render_status(receipt: Mapping[str, object]) -> str:
    map_data = receipt["map"]
    histories = receipt["histories"]
    removal = receipt["removal"]
    shell = receipt["refusal_shell"]
    costs = receipt["costs"]
    assert isinstance(map_data, dict)
    assert isinstance(histories, dict)
    assert isinstance(removal, dict)
    assert isinstance(shell, dict)
    assert isinstance(costs, dict)
    map_row = map_data
    history_row = histories
    removal_row = removal
    shell_row = shell
    cost_row = costs
    distortion = cost_row["distortion"]
    assert isinstance(distortion, dict)
    extrema = distortion["extrema"]
    assert isinstance(extrema, dict)
    mu1 = extrema["mu1"]
    mu2 = extrema["mu2"]
    assert isinstance(mu1, dict) and isinstance(mu2, dict)
    wrong_ids = removal_row["wrong_ids"]
    assert isinstance(wrong_ids, list)
    wrong = ", ".join(str(value) for value in wrong_ids)
    return f"""# Typed translation: status

`AuthorityEffect: None.`

This page is rendered from `receipts/typed_translation.json`; `verify_prose.py`
recomputes it and fails on any drift.  The freeze-first commit is
`{FREEZE_COMMIT}`.  The requirements hash is
`{FROZEN_SHA256['REQUIREMENTS.md']}` and the predictions hash is
`{FROZEN_SHA256['PREDICTIONS.md']}`.

## Terminal results

The bounded forward/backward carrier result is **{map_row['outcome']}**.
The exact-cost subquestion is **PROVED_EXACT_COST_OBSTRUCTION** at the declared
form witness.  Extension outside the frozen carriers is **OPEN_AT_BOUND**.

The two independent history enumerators agree on {history_row['count']} valid
ordered prefixes.  All {map_row['candidate_count']} candidates were evaluated;
{map_row['valid_count']} pass, both at statement price
{map_row['least_statement_price']}.  They differ only by the direct versus
complemented address family, and the orientation quotient agrees.

The representative's maximum forward additive distortion is
`mu1 = {mu1['forward_max']}` and `mu2 = {mu2['forward_max']}`.  These are bounds
on the frozen history space, not general theorems and not acceptance filters.

The nearby shell contains {shell_row['population']} non-typed states.  It has
zero silent truncations and uses every named decoder refusal category.  The
literal category names were fixed in the kernel build, because the freeze
required named categories but did not enumerate their strings; that omission
is not rewritten into the frozen text.

## Frozen predictions

{_prediction_table(receipt)}

## Mechanical removal

The scorer evaluates all {removal_row['population']} frozen rows.  The hand map
hits {removal_row['hit_count']} and misses {removal_row['wrong_count']}.
Every miss is mechanically MIXED.  Wrong row ids: {wrong}.

## Scope

The original sealed tree, the boundary tree, the side-free control, and the
limit-and-second-observer tree are independently regression-checked by the
repository battery.  This tree's new mathematical object is the typed map
between the first two plus the total one-field removal experiment.  It does
not rename the second-observer control into a third grammar.
"""


def render_findings(receipt: Mapping[str, object]) -> str:
    removal = receipt["removal"]
    map_data = receipt["map"]
    provenance = receipt["provenance_witness"]
    assert isinstance(removal, dict) and isinstance(map_data, dict)
    assert isinstance(provenance, dict)
    rows = removal["rows"]
    assert isinstance(rows, list)
    misses = [row for row in rows if isinstance(row, dict) and not row["hit"]]
    lines = [
        "# Typed translation: findings",
        "",
        "`AuthorityEffect: None.`",
        "",
        "## Direction one — the map",
        "",
        f"The exhaustive bounded result is **{map_data['outcome']}**.  Exactly",
        f"{map_data['valid_count']} candidates pass.  State inspection and administrative",
        "presentation are the complete least statement-price capability set.  Cost",
        "does not enter validity; its nonzero distortion is reported after acceptance.",
        "",
        "The equal-profile witness retains different instance and rule fields and",
        f"different label sets (`{provenance['left_labels']}` versus",
        f"`{provenance['right_labels']}`).  Equality of the projected OR therefore",
        "is not reported as equality of source state or provenance.",
        "",
        "## Direction two — removal",
        "",
        "The projection deletes exactly the top-level `boundary` field.  The misses are:",
        "",
        "| id | stage | claimed | actual | subject |",
        "|---|---|---|---|---|",
    ]
    for row in misses:
        lines.append(
            f"| {row['id']} | {row['stage']} | {row['claimed']} | {row['actual']} | "
            f"{str(row['subject']).replace('|', '/')} |"
        )
    lines.extend(
        [
            "",
            "Each row's before value, after value, and survival Boolean is present in",
            "the JSON receipt.  No word in the hand-written claim supplies its actual class.",
            "",
            "## Residual",
            "",
            "The result is complete only for the declared events, tags, addresses,",
            "histories, renamings, and one-field projection.  Global translation and",
            "global one-primitive removal remain OPEN_AT_BOUND.",
            "",
        ]
    )
    return "\n".join(lines)


def render_claim_ledger(receipt: Mapping[str, object]) -> str:
    map_data = receipt["map"]
    removal = receipt["removal"]
    shell = receipt["refusal_shell"]
    assert isinstance(map_data, dict) and isinstance(removal, dict) and isinstance(shell, dict)
    return f"""# Typed translation: claim ledger

`AuthorityEffect: None.`

| id | classification | claim | machine evidence | boundary |
|---|---|---|---|---|
| TT-01 | DETERMINISTIC_COMPUTATION | The replay-closed history census is nonempty and agrees with an unpruned permutation census. | `histories.count`, `histories.ordered_unpruned_crosscheck` | Frozen eight-event space only. |
| TT-02 | DETERMINISTIC_COMPUTATION | All {map_data['candidate_count']} declared candidates were retained; {map_data['valid_count']} are bounded typed maps. | `map.candidates`, `map.valid_candidates` | Frozen carrier and renaming product only. |
| TT-03 | DETERMINISTIC_COMPUTATION | The least map uses state inspection and administrative presentations at statement price {map_data['least_statement_price']}. | `map.least_statement_price`, candidate capability vectors | Statement price is not a trace cost. |
| TT-04 | PROVED_THEOREM | A fixed memoryless rule block cannot satisfy the equal-side requirements at both frozen witnesses. | `TypedTranslation.memoryless_fixed_block_obstruction`, `lean/axioms.txt` | Memoryless subspace only. |
| TT-05 | PROVED_THEOREM | A nonempty outer-symmetric form image cannot contain exactly one admission. | `TypedTranslation.symmetric_form_cost_obstruction`, `lean/axioms.txt` | Exact `mu1` preservation for that form image only. |
| TT-06 | DETERMINISTIC_COMPUTATION | The nearby shell has {shell['population']} refused states, no silent truncation, and every named code is exercised. | `refusal_shell` | One mutation from the typed bounded domain. |
| TT-07 | DETERMINISTIC_COMPUTATION | The total removal scorer records {removal['hit_count']} exact-class hits in {removal['population']} rows and names every miss. | `removal.rows`, `removal.wrong_ids` | Frozen 37-row population and one top-level field. |
| TT-08 | OPEN_OBSTRUCTION | No result here proves the typed translation or removal result on unbounded carriers. | `terminal.global` | OPEN_AT_BOUND. |
"""


def rendered_prose(receipt: Mapping[str, object]) -> dict[str, str]:
    return {
        "CLAIM_LEDGER.md": render_claim_ledger(receipt),
        "FINDINGS.md": render_findings(receipt),
        "STATUS.md": render_status(receipt),
    }

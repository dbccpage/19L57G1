"""Total one-field boundary-removal experiment over the vendored row census."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import json
from pathlib import Path
from typing import Mapping, Sequence


HERE = Path(__file__).resolve().parents[2]
VENDORED = HERE / "pinned" / "boundary_dependence.json"


class DependenceClass(StrEnum):
    INDEPENDENT = "INDEPENDENT"
    DEPENDENT = "DEPENDENT"
    MIXED = "MIXED"


NOT_FORMULATED = "NOT_FORMULATED"


@dataclass(frozen=True)
class DependenceRow:
    row_id: str
    stage: str
    subject: str
    claim: str
    probes: tuple[str, ...]


ROW_PROBES: dict[str, tuple[str, ...]] = {
    "R00": ("event_follows_empty",),
    "R01": ("initial_datum_fixed",),
    "R02": ("side_profiles", "side_collapse", "side_names", "side_reflection", "side_class_count"),
    "R03": ("supply_inert",),
    "R04": ("admission_separate", "mark_retained", "retained_address"),
    "R05": ("side_judgment", "mark_side_profile", "side_candidate_count", "presentation_convention", "side_class_count"),
    "R06": ("supply_inert",),
    "R07": ("replay_exact",),
    "R08": ("event_follows_empty",),
    "R09": ("initial_datum_fixed", "reading_fixed"),
    "R10": ("supply_inert", "replay_exact"),
    "R11": ("event_follows_empty",),
    "R12": ("identity_policy_count", "shared_policy_refused"),
    "R13": ("initial_datum_fixed", "reading_fixed"),
    "R14": ("two_side_judgments", "retained_addresses", "automorphism_count", "mark_separation", "different_sides"),
    "R15": ("separation_requirement", "reading_agreement"),
    "R16": ("further_mark_admitted", "further_mark_separates"),
    "R17": ("candidate_space_shape", "capability_count", "bundle_refusal"),
    "R18": ("side_reflection", "side_properties", "counterfactual_square", "separation_results", "index_separation_result"),
    "R19": ("index_properties", "withdraw_mark_permutations"),
    "R20": ("separation_requirement", "pointwise_set_requirement", "reading_agreement"),
    "R21": ("further_mark_admitted", "retained_address"),
    "R22": ("grouping_coordinates", "tag_property", "index_properties", "withdraw_mark_permutations"),
    "R23": ("candidate_space_shape", "capability_count", "one_step_rule", "bundle_refusal"),
    "R24": ("side_reflection", "side_properties", "label_and_side_property", "grouping_square", "separation_results"),
    "R25": ("policy_space_shape", "capability_count", "one_step_rule", "bundle_refusal"),
    "R26": ("nesting_invisibility",),
    "R27": ("depth_value", "address_value", "crossing_value", "level_exchanges"),
    "R28": ("outside_outer_boundary",),
    "R29": ("reader_depth_bound", "inscription_domain", "item_bound", "enumeration_order"),
    "R30": ("available_depth_orbit", "available_depth_observation"),
    "R31": ("branch_payload", "one_adoption_rule", "quotient_algorithm"),
    "R32": ("demand_target", "separation_requirement"),
    "R33": ("inscription_domain", "enumeration_order"),
    "R34": ("generator_space_shape", "capability_count", "one_step_rule", "bundle_refusal"),
    "R35": ("node_ceiling", "branching_bound", "round_bound"),
    "R36": ("supplied_inscriptions", "placement", "renaming_action", "attempt_accounting", "enumeration_order", "replay_exact", "finite_resource_limits"),
}


# These probes read a field that is structurally inside the one removable
# boundary coordinate.  Every other probe reads generic state, history, event,
# counter, or algorithm fields that the total projection retains.
BOUNDARY_PROBES: frozenset[str] = frozenset(
    {
        "address_value",
        "automorphism_count",
        "available_depth_observation",
        "bundle_refusal",
        "counterfactual_square",
        "crossing_value",
        "demand_target",
        "depth_value",
        "different_sides",
        "further_mark_separates",
        "grouping_square",
        "inscription_domain",
        "label_and_side_property",
        "level_exchanges",
        "mark_separation",
        "mark_side_profile",
        "nesting_invisibility",
        "outside_outer_boundary",
        "placement",
        "pointwise_set_requirement",
        "presentation_convention",
        "quotient_algorithm",
        "reading_agreement",
        "reading_fixed",
        "renaming_action",
        "retained_address",
        "retained_addresses",
        "separation_results",
        "side_candidate_count",
        "side_class_count",
        "side_collapse",
        "side_judgment",
        "side_names",
        "side_profiles",
        "side_properties",
        "side_reflection",
        "supplied_inscriptions",
        "two_side_judgments",
    }
)


def load_rows(path: Path = VENDORED) -> tuple[DependenceRow, ...]:
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("rows"), list):
        raise ValueError("vendored dependence population must carry a rows list")
    rows: list[DependenceRow] = []
    for item in raw["rows"]:
        if not isinstance(item, dict):
            raise ValueError("vendored row is not an object")
        row_id = str(item["id"])
        probes = tuple(str(probe) for probe in item["probes"])
        if probes != ROW_PROBES.get(row_id):
            raise ValueError(f"{row_id} probes differ from the executable registry")
        rows.append(
            DependenceRow(
                row_id=row_id,
                stage=str(item["stage"]),
                subject=str(item["subject"]),
                claim=str(item["claim"]),
                probes=probes,
            )
        )
    expected = [f"R{index:02d}" for index in range(37)]
    if [row.row_id for row in rows] != expected:
        raise ValueError("vendored row ids are not the complete ordered R00-R36 census")
    return tuple(rows)


def _probe_value(row: DependenceRow, probe: str) -> object:
    """Deterministic JSON value for one formulated probe."""

    boolean_suffixes = (
        "empty",
        "fixed",
        "inert",
        "separate",
        "retained",
        "refused",
        "exact",
        "agreement",
        "invisibility",
    )
    if probe.endswith(boolean_suffixes) or probe.startswith("withdraw_"):
        value: object = True
    elif probe.endswith(("count", "bound", "ceiling", "value")):
        value = len(row.probes)
    else:
        value = {"probe": probe, "stage": row.stage, "subject": row.subject}
    return value


def carrier_record(row: DependenceRow) -> dict[str, object]:
    generic: dict[str, object] = {}
    boundary: dict[str, object] = {}
    for probe in row.probes:
        target = boundary if probe in BOUNDARY_PROBES else generic
        target[probe] = _probe_value(row, probe)
    return {
        "algorithms": {"projection": "all_fields_except_boundary"},
        "event_kinds": ["PRESENTATION", "ADMISSION"],
        "facts": generic,
        "finite_counters": {"probe_count": len(row.probes)},
        "history": [row.stage, row.row_id],
        "provenance": {"claim": row.claim, "subject": row.subject},
        "row_id": row.row_id,
        "stage": row.stage,
        "boundary": {"facts": boundary, "primitive": "admitted_boundary"},
    }


def remove_boundary(record: Mapping[str, object]) -> dict[str, object]:
    """The frozen total projection: retain every top-level field but one."""

    return {key: value for key, value in record.items() if key != "boundary"}


def evaluate_probe(record: Mapping[str, object], probe: str) -> object:
    facts = record.get("facts")
    if isinstance(facts, dict) and probe in facts:
        return facts[probe]
    boundary = record.get("boundary")
    if isinstance(boundary, dict):
        boundary_facts = boundary.get("facts")
        if isinstance(boundary_facts, dict) and probe in boundary_facts:
            return boundary_facts[probe]
    return NOT_FORMULATED


def actual_class(survives: Sequence[bool]) -> DependenceClass:
    if all(survives):
        return DependenceClass.INDEPENDENT
    if not any(survives):
        return DependenceClass.DEPENDENT
    return DependenceClass.MIXED


def claimed_class(claim: str) -> DependenceClass:
    """Parse the hand map independently of all before/after probe values."""

    lower = claim.casefold()
    if lower.startswith("does not depend"):
        if " requires " in lower or "but every" in lower:
            return DependenceClass.MIXED
        return DependenceClass.INDEPENDENT
    if lower.startswith("require") or lower.startswith("requires"):
        return DependenceClass.DEPENDENT
    if "use the paid boundary" in lower and "are metatheory" in lower:
        return DependenceClass.MIXED
    raise ValueError(f"unclassified hand-written dependence claim: {claim}")


def score_row(row: DependenceRow) -> dict[str, object]:
    before_record = carrier_record(row)
    after_record = remove_boundary(before_record)
    difference = sorted(set(before_record) ^ set(after_record))
    if difference != ["boundary"]:
        raise AssertionError(f"{row.row_id} projection changed keys {difference}")
    probes: list[dict[str, object]] = []
    survival: list[bool] = []
    for probe in row.probes:
        before = evaluate_probe(before_record, probe)
        after = evaluate_probe(after_record, probe)
        survives = before == after and after != NOT_FORMULATED
        survival.append(survives)
        probes.append(
            {
                "after": after,
                "before": before,
                "probe": probe,
                "survives": survives,
            }
        )
    actual = actual_class(survival)
    claimed = claimed_class(row.claim)
    return {
        "actual": actual.value,
        "claim": row.claim,
        "claimed": claimed.value,
        "hit": actual is claimed,
        "id": row.row_id,
        "key_symmetric_difference": difference,
        "probes": probes,
        "stage": row.stage,
        "subject": row.subject,
    }


def removal_report(rows: tuple[DependenceRow, ...] | None = None) -> dict[str, object]:
    population = rows if rows is not None else load_rows()
    scored = [score_row(row) for row in population]
    wrong = [str(row["id"]) for row in scored if not bool(row["hit"])]
    classes = {
        name.value: sum(row["actual"] == name.value for row in scored)
        for name in DependenceClass
    }
    return {
        "actual_class_counts": classes,
        "hit_count": len(scored) - len(wrong),
        "hit_rate": f"{len(scored) - len(wrong)}/{len(scored)}",
        "population": len(scored),
        "projection": "{key: value for key, value in record.items() if key != 'boundary'}",
        "rows": scored,
        "wrong_count": len(wrong),
        "wrong_ids": wrong,
    }

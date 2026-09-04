"""Build and write the deterministic second-stake receipts."""

from __future__ import annotations

import argparse
import binascii
import hashlib
import json
import pathlib
import struct
import sys
from typing import Sequence, cast

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _path in (
    HERE,
    REPO / "code",
    REPO / "research" / "identification_dual",
    REPO / "research" / "two_sided_commitment",
):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from derivation.export import Json, dumps_deterministic  # noqa: E402
from derivation.model import Regime  # noqa: E402

from generation import (  # noqa: E402
    BOUNDS,
    MAX_DATA,
    MAX_RESPONSE_ROUNDS,
    MEASURES,
    NODE_GUARD,
    PERMUTATION_BUDGET,
    Tree,
    build_all,
    canonical_crosscheck,
    invariance_records,
    reached_regimes,
    rule_generation_record,
    tree_payload,
)
from observables import ObservableGuardError  # noqa: E402
from rules import ALL_RULES, CONTROLS, MENU, StakeRule, label_map  # noqa: E402

DEFAULT_SUMMARY = HERE / "receipts" / "stake.json"
DEFAULT_FULL = HERE / "receipts" / "full" / "stake_full.json.gz"
SIBLING_RECEIPT = (
    REPO
    / "research"
    / "two_sided_commitment"
    / "receipts"
    / "two_sided_commitment.json"
)
SNAPSHOT = "3f44571240a0830a2fa8de639281670f4e50a511"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deterministic_gzip(raw: bytes) -> bytes:
    """Gzip made from explicit stored DEFLATE blocks.

    Library compression can choose different streams across zlib versions.
    Stored blocks cost space but make every byte a function of ``raw`` alone.
    """

    chunks = [raw[index : index + 65_535] for index in range(0, len(raw), 65_535)]
    if not chunks:
        chunks = [b""]
    blocks: list[bytes] = []
    for index, chunk in enumerate(chunks):
        final = index == len(chunks) - 1
        length = len(chunk)
        blocks.append(
            bytes((1 if final else 0,))
            + struct.pack("<HH", length, 0xFFFF ^ length)
            + chunk
        )
    body = b"".join(blocks)
    header = b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\xff"
    trailer = struct.pack(
        "<II", binascii.crc32(raw) & 0xFFFFFFFF, len(raw) & 0xFFFFFFFF
    )
    return header + body + trailer


def sibling_baseline() -> dict[str, Json]:
    """Read only the pinned sibling fields used as the control baseline."""

    value: object = json.loads(SIBLING_RECEIPT.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("sibling receipt must be an object")
    bounds = value.get("bounds")
    summary = value.get("summary")
    if not isinstance(bounds, dict) or not isinstance(summary, dict):
        raise ValueError("sibling receipt lacks bounds or summary")
    by_commitment = summary.get("by_commitment")
    if not isinstance(by_commitment, dict):
        raise ValueError("sibling receipt lacks its control summary")
    selected: dict[str, Json] = {}
    for rule in CONTROLS:
        row = by_commitment.get(rule.name)
        if not isinstance(row, dict):
            raise ValueError(f"sibling receipt lacks control {rule.name}")
        selected[rule.name] = {
            "kinds_answered": cast(Json, row.get("kinds_answered")),
            "nodes": cast(Json, row.get("nodes")),
            "refusals": cast(Json, row.get("refusals")),
            "trees": cast(Json, row.get("trees")),
        }
    return {
        "receipt_sha256": sha256(SIBLING_RECEIPT),
        "bounds": cast(Json, bounds),
        "by_control": selected,
        "comparison": "context only: sibling data bound five; this rung reruns every control at data bound four",
    }


def _as_str_list(value: Json) -> list[str]:
    if not isinstance(value, list):
        raise TypeError("expected a JSON list")
    return [item for item in value if isinstance(item, str)]


def _as_int(value: Json) -> int:
    if not isinstance(value, int):
        raise TypeError("expected a JSON integer")
    return value


def _generation_by_name(records: Sequence[dict[str, Json]]) -> dict[str, dict[str, Json]]:
    return {cast(str, record["rule"]): record for record in records}


def _invariance_by_name(records: Sequence[dict[str, Json]]) -> dict[str, dict[str, Json]]:
    return {cast(str, record["rule"]): record for record in records}


def _signature_tuple(record: dict[str, Json]) -> tuple[str, ...]:
    raw = record["tree_signatures"]
    if not isinstance(raw, dict):
        raise TypeError("tree_signatures must be an object")
    return tuple(str(raw[key]) for key in sorted(raw))


def tie_map(records: Sequence[dict[str, Json]], rules: Sequence[StakeRule]) -> dict[str, list[str]]:
    groups: dict[tuple[str, ...], list[str]] = {}
    wanted = {rule.name for rule in rules}
    for record in records:
        name = cast(str, record["rule"])
        if name in wanted:
            groups.setdefault(_signature_tuple(record), []).append(name)
    result: dict[str, list[str]] = {name: [] for name in wanted}
    for names in groups.values():
        if len(names) > 1:
            for name in names:
                result[name] = sorted(other for other in names if other != name)
    return dict(sorted(result.items()))


def label_equivalence(
    regimes: Sequence[Regime], rules: Sequence[StakeRule]
) -> dict[str, list[str]]:
    """Menu members with identical labels on every reached regime."""

    result: dict[str, list[str]] = {rule.name: [] for rule in rules}
    for index, left in enumerate(rules):
        for right in rules[index + 1 :]:
            try:
                equal = all(
                    label_map(regime, left) == label_map(regime, right)
                    for regime in regimes
                )
            except ObservableGuardError:
                equal = False
            if equal:
                result[left.name].append(right.name)
                result[right.name].append(left.name)
    return {name: sorted(peers) for name, peers in sorted(result.items())}


def nearest_controls(
    menu_records: Sequence[dict[str, Json]],
    control_records: Sequence[dict[str, Json]],
) -> dict[str, list[str]]:
    def vector(record: dict[str, Json]) -> tuple[frozenset[str], bool, bool, bool]:
        return (
            frozenset(_as_str_list(record["kinds"])),
            _as_int(record["relabellings"]) > 0,
            _as_int(record["refusals"]) > 0,
            _as_int(record["guard_nodes"]) > 0,
        )

    out: dict[str, list[str]] = {}
    for member in menu_records:
        mv = vector(member)
        scored: list[tuple[int, str]] = []
        for control in control_records:
            cv = vector(control)
            distance = len(mv[0] ^ cv[0]) + sum(
                int(left != right) for left, right in zip(mv[1:], cv[1:])
            )
            scored.append((distance, cast(str, control["rule"])))
        best = min(score for score, _ in scored)
        out[cast(str, member["rule"])] = sorted(
            name for score, name in scored if score == best
        )
    return dict(sorted(out.items()))


EXPECTED: dict[str, tuple[frozenset[str], bool]] = {
    "E1": (frozenset(), False),
    "E2": (frozenset({"apart"}), False),
    "E3": (frozenset({"apart", "same"}), True),
    "E4": (frozenset({"apart", "same"}), True),
    "E5": (frozenset({"same"}), True),
    "E6": (frozenset({"same"}), True),
    "E7": (frozenset(), True),
    "E8": (frozenset(), False),
    "E9": (frozenset({"apart"}), True),
}


def score_predictions(
    generation: Sequence[dict[str, Json]],
    invariance: Sequence[dict[str, Json]],
    ties: dict[str, list[str]],
    input_count: int,
) -> tuple[dict[str, Json], list[dict[str, Json]]]:
    by_generation = _generation_by_name(generation)
    by_invariance = _invariance_by_name(invariance)
    detail: list[dict[str, Json]] = []

    def add(identifier: str, hit: bool, observed: Json) -> None:
        detail.append({"id": identifier, "verdict": "HIT" if hit else "MISS", "observed": observed})

    add(
        "P-I1",
        all(by_invariance[rule.name]["disposition"] == "CHECKED" for rule in MENU),
        {rule.name: by_invariance[rule.name]["disposition"] for rule in MENU},
    )
    add(
        "P-I2",
        all(by_invariance[name]["disposition"] == "CHECKED" for name in ("total_apart", "total_same")),
        {name: by_invariance[name]["disposition"] for name in ("total_apart", "total_same")},
    )
    add(
        "P-I3",
        all(by_invariance[name]["disposition"] == "REFUTED" for name in ("parity", "residue_three", "chain")),
        {name: by_invariance[name]["disposition"] for name in ("parity", "residue_three", "chain")},
    )
    add(
        "P-I4",
        any(by_invariance[name]["disposition"] != "REFUTED" for name in ("total_apart", "total_same")),
        "OPEN: constant controls have no refuting renaming",
    )
    for number, rule in enumerate(MENU, start=1):
        record = by_generation[rule.name]
        expected_kinds, expected_relabelling = EXPECTED[rule.name]
        observed_kinds = frozenset(_as_str_list(record["kinds"]))
        observed_relabelling = _as_int(record["relabellings"]) > 0
        add(
            f"P-G{number}",
            observed_kinds == expected_kinds and observed_relabelling == expected_relabelling,
            {"kinds": sorted(observed_kinds), "relabelled": observed_relabelling},
        )
    both = sorted(
        rule.name
        for rule in MENU
        if frozenset(_as_str_list(by_generation[rule.name]["kinds"])) == {"apart", "same"}
        and by_invariance[rule.name]["disposition"] == "CHECKED"
    )
    add("P-G10", bool(both), both)
    tied = {name: peers for name, peers in ties.items() if peers}
    add("P-G11", bool(tied), tied)
    add("P-C1", input_count == 2, input_count)
    detail.append({"id": "X", "verdict": "PENDING", "observed": "five-data rectangle not computed"})
    hits = sum(item["verdict"] == "HIT" for item in detail)
    misses = sum(item["verdict"] == "MISS" for item in detail)
    pending = sum(item["verdict"] == "PENDING" for item in detail)
    return ({"hit": hits, "missed": misses, "vacuous": 0, "pending": pending}, detail)


def build_receipt() -> tuple[dict[str, Json], dict[str, Json]]:
    trees = build_all(ALL_RULES)
    regimes = reached_regimes(trees)
    invariance = invariance_records(ALL_RULES, regimes)
    generation = [rule_generation_record(rule, trees) for rule in ALL_RULES]
    menu_generation = [record for record in generation if record["source"] == "menu"]
    control_generation = [record for record in generation if record["source"] == "control"]
    ties = tie_map(menu_generation, MENU)
    label_peers = label_equivalence(regimes, MENU)
    by_generation = _generation_by_name(generation)
    by_invariance = _invariance_by_name(invariance)
    both_kind = sorted(
        rule.name
        for rule in MENU
        if frozenset(_as_str_list(by_generation[rule.name]["kinds"])) == {"apart", "same"}
        and by_invariance[rule.name]["disposition"] == "CHECKED"
    )
    retained = sorted(
        rule.name
        for rule in MENU
        if by_invariance[rule.name]["disposition"] != "REFUTED"
    )
    input_count = 2
    score, detail = score_predictions(generation, invariance, ties, input_count)
    crosscheck = canonical_crosscheck(regimes)
    full: dict[str, Json] = {
        "schema": "second_stake_full/v1",
        "authority_effect": "None",
        "trees": [tree_payload(tree) for tree in trees],
    }
    full_raw = dumps_deterministic(full)
    full_sha = hashlib.sha256(full_raw).hexdigest()
    summary: dict[str, Json] = {
        "schema": "second_stake/v1",
        "authority_effect": "None",
        "snapshot_commit": SNAPSHOT,
        "prompt_sha256": sha256(HERE / "PROMPT.md"),
        "predictions_sha256": sha256(HERE / "PREDICTIONS.md"),
        "bounds": {
            "readings": ["L", "F"],
            "measures": list(MEASURES),
            "max_items": BOUNDS.max_items,
            "max_arity": BOUNDS.max_arity,
            "max_data": MAX_DATA,
            "max_response_rounds": MAX_RESPONSE_ROUNDS,
            "pre_expansion_node_guard": NODE_GUARD,
            "permutation_budget": PERMUTATION_BUDGET,
        },
        "menu": [
            {
                "member": rule.name,
                "observables": list(rule.observables),
                "capability_count": rule.capability_count,
            }
            for rule in MENU
        ],
        "controls": [
            {
                "name": rule.name,
                "index_reading": rule.index_reading,
            }
            for rule in CONTROLS
        ],
        "sibling_control_baseline": sibling_baseline(),
        "reached_regimes": len(regimes),
        "invariance": invariance,
        "canonical_crosscheck": crosscheck,
        "generation": generation,
        "tree_ties": ties,
        "label_equivalence": label_peers,
        "nearest_controls": nearest_controls(menu_generation, control_generation),
        "retained_menu": retained,
        "both_kind_members": both_kind,
        "survivors_for_challenge_three": retained,
        "input_count": {
            "value": input_count,
            "proof": None,
            "sentence": "A rule class is a declaration; no menu member is forced and no unique survivor is proved.",
        },
        "predictions_scored": score,
        "prediction_detail": detail,
        "extrapolation_X": {
            "statement": "four-data survivors persist at data bound five with other bounds fixed",
            "forced": False,
            "scoring_rung": "challenge_three",
            "status": "PENDING",
        },
        "terminals": [
            "RULE_CLASS_DECLARED",
            "INVARIANCE_DECIDED",
            "OPEN_AT_NAMED_TARGET",
            "OPEN_AT_CONTROLS_REFUTED",
            "GENERATION_CENSUSED",
            "STAKE_READ_OFF_STATE" if both_kind else "NO_ENDOGENOUS_STAKE_IN_MENU",
            "INPUT_COUNT_STATED",
            "REGISTER_WRITTEN",
            "OB1_UNCHANGED",
        ],
        "tie_record": "rule tie between Challenge 2 and no-first-demand; both run in parallel; this is track 2",
        "full_export": {
            "path": "receipts/full/stake_full.json.gz",
            "uncompressed_sha256": full_sha,
            "uncompressed_bytes": len(full_raw),
        },
    }
    return summary, full


def render_receipts() -> tuple[bytes, bytes]:
    summary, full = build_receipt()
    full_raw = dumps_deterministic(full)
    full_gzip = deterministic_gzip(full_raw)
    return dumps_deterministic(summary), full_gzip


def write_receipts(summary_path: pathlib.Path, full_path: pathlib.Path) -> None:
    summary, full = render_receipts()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_bytes(summary)
    full_path.write_bytes(full)


def check_receipts(summary_path: pathlib.Path, full_path: pathlib.Path) -> list[str]:
    expected_summary, expected_full = render_receipts()
    failures: list[str] = []
    if not summary_path.is_file() or summary_path.read_bytes() != expected_summary:
        failures.append(f"receipt differs: {summary_path.relative_to(HERE)}")
    if not full_path.is_file() or full_path.read_bytes() != expected_full:
        failures.append(f"receipt differs: {full_path.relative_to(HERE)}")
    return failures


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the second-stake finite receipt.")
    parser.add_argument("--out", type=pathlib.Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--full", type=pathlib.Path, default=DEFAULT_FULL)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        failures = check_receipts(args.out, args.full)
        if failures:
            for failure in failures:
                print(f"FAIL: {failure}")
            return 1
        print("second-stake receipts regenerate byte-identically")
        return 0
    write_receipts(args.out, args.full)
    print(f"wrote {args.out}")
    print(f"wrote {args.full}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Ingest merged scope corrections while retaining the original evidence.

This versioned view records source wording and local-check custody. It does
not promote a corrected sentence into a new mathematical result.
AuthorityEffect: None.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
from typing import Any

from eg_census import headlines
from eg_sources import HERE, Snapshot, canonical, digest, git, load_snapshot, read_object
from eg_views import HANDOFF_SUBJECTS

REVIEW_FILE = HERE / "correction_reviews.json"
OUTPUT = HERE / "versions" / "section3.json"
HEX64 = re.compile(r"[0-9a-f]{64}")


def require_merged(repo: Path, source: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", source, "origin/main"],
        capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError("CORRECTION_NOT_MERGED: " + source)


def ingest(spec: dict[str, Any], current: Snapshot, historical: dict[str, Any],
           population: list[dict[str, Any]]) -> dict[str, Any]:
    if set(spec) != {"schema", "authority_effect", "source_snapshot", "source_tree", "checks", "reviews"}:
        raise ValueError("CORRECTION_INPUT_FIELDS")
    if spec["schema"] != 1 or spec["authority_effect"] != "None" or spec["source_snapshot"] != current.snapshot:
        raise ValueError("CORRECTION_SOURCE_HEAD")
    if spec["source_tree"] != git(current.repo, "rev-parse", current.snapshot + "^{tree}").decode().strip():
        raise ValueError("CORRECTION_SOURCE_TREE")
    old_source = historical["source_snapshot"]
    if (current.snapshot == old_source
            or git(current.repo, "merge-base", old_source, current.snapshot).decode().strip() != old_source):
        raise ValueError("CORRECTION_REQUIRES_NEW_SOURCE_VERSION")
    require_merged(current.repo, current.snapshot)
    subject_roots = {"handoff:" + row[0]: row[1] for row in HANDOFF_SUBJECTS}
    expected = set(subject_roots)
    historical_ids = {row["id"] for row in historical["items"]}
    ids = [row["historical_handoff_id"] for row in spec["reviews"]]
    if (historical_ids != expected or len(historical["items"]) != len(expected)
            or len(ids) != len(set(ids)) or set(ids) != expected):
        raise ValueError("CORRECTION_POPULATION_MISMATCH")
    checks = {row["id"]: row for row in spec["checks"]}
    if not checks or len(checks) != len(spec["checks"]):
        raise ValueError("CORRECTION_CHECK_POPULATION")
    for key, check in checks.items():
        if set(check) != {"id", "checked_head", "checked_tree", "command", "exit_code", "log_sha256", "scope"}:
            raise ValueError("CORRECTION_CHECK_FIELDS: " + key)
        tree = git(current.repo, "rev-parse", check["checked_head"] + "^{tree}").decode().strip()
        if tree != check["checked_tree"] or tree != spec["source_tree"]:
            raise ValueError("CORRECTION_CHECK_WRONG_TREE: " + key)
        if type(check["exit_code"]) is not int or check["exit_code"] != 0:
            raise ValueError("CORRECTION_CHECK_FAILED: " + key)
        if not isinstance(check["command"], list) or not check["command"] or not HEX64.fullmatch(check["log_sha256"]) or not check["scope"]:
            raise ValueError("CORRECTION_CHECK_UNBOUND: " + key)
    records = []
    for review in sorted(spec["reviews"], key=lambda row: row["historical_handoff_id"]):
        key = review["historical_handoff_id"]
        if set(review) != {"historical_handoff_id", "sources", "scope", "remaining_obligations", "check_ids", "disposition"}:
            raise ValueError("CORRECTION_REVIEW_FIELDS: " + key)
        if not review["sources"] or not review["scope"] or not review["remaining_obligations"]:
            raise ValueError("CORRECTION_SCOPE_MISSING: " + key)
        if not any(ref["path"].startswith(subject_roots[key]) for ref in review["sources"]):
            raise ValueError("CORRECTION_SUBJECT_SOURCE_MISSING: " + key)
        if review["disposition"] not in {"WORDING_NARROWED", "IMPLEMENTATION_AND_SCOPE_REPAIRED", "AUTHOR_POLICY_RULING", "INDEX_CORRECTED"}:
            raise ValueError("CORRECTION_DISPOSITION: " + key)
        if not review["check_ids"] or any(identifier not in checks for identifier in review["check_ids"]):
            raise ValueError("CORRECTION_CHECK_LINK_MISSING: " + key)
        matched: list[dict[str, Any]] = []
        for reference in review["sources"]:
            current.resolve(reference)
            blocks = [row for row in population if row["source"]["path"] == reference["path"]
                      and row["source"]["start_line"] <= reference["end_line"]
                      and reference["start_line"] <= row["source"]["end_line"]]
            if not blocks:
                raise ValueError("CORRECTION_HEADLINE_MISSING: " + key)
            matched.extend({"id": row["id"], "source": row["source"]} for row in blocks)
        records.append({"id": "correction:" + key.removeprefix("handoff:"), **review,
            "current_headlines": sorted({row["id"]: row for row in matched}.values(), key=lambda row: row["id"]),
            "source_class": "metatheory apparatus", "mathematical_status": "OPEN",
            "evidence_gap": "This is a source-scope correction and check receipt, not a new proof of the remaining mathematical obligations."})
    return {"schema": 1, "authority_effect": "None", "historical_source_snapshot": historical["source_snapshot"],
        "corrected_source_snapshot": current.snapshot, "corrected_source_tree": spec["source_tree"],
        "review_sha256": digest(canonical(spec)), "checks": spec["checks"], "records": records,
        "historical_evidence_retained": True, "all_headlines_supported": False,
        "boundary": "Merged corrections are a new source version. Historical theorem reports keep their original head; local checks establish only their declared scope."}


def build() -> dict[str, Any]:
    original = load_snapshot()
    spec = read_object(REVIEW_FILE)
    current = Snapshot(original.repo, spec["source_snapshot"])
    historical = read_object(HERE / "evidence" / "section3_handoff.json")
    if historical["source_snapshot"] != original.snapshot:
        raise ValueError("CORRECTION_HISTORICAL_SOURCE_CHANGED")
    population = headlines(current, read_object(HERE / "input.json"))
    return ingest(spec, current, historical, population)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    first, second = canonical(build()), canonical(build())
    if first != second:
        raise ValueError("CORRECTION_REGENERATION_NONDETERMINISTIC")
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(first)
    elif not OUTPUT.is_file() or OUTPUT.read_bytes() != first:
        raise ValueError("CORRECTION_ARTIFACT_DIFFERS")
    print("PASS: merged correction population, source spans, same-tree checks, and deterministic versioned view")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

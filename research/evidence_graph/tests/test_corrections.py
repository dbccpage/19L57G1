"""Correction custody refuses missing owners, wrong trees, and stale spans."""
from copy import deepcopy
from types import SimpleNamespace
from typing import Any

import pytest

from corrections import OUTPUT, REVIEW_FILE, build, ingest, require_merged
from eg_census import headlines
from eg_sources import HERE, Snapshot, git, load_snapshot, read_object
from eg_views import HANDOFF_SUBJECTS


@pytest.fixture(scope="module")
def sample() -> tuple[dict[str, Any], Snapshot, dict[str, Any], list[dict[str, Any]]]:
    snapshot = load_snapshot()
    population = headlines(snapshot, read_object(HERE / "input.json"))
    tree = git(snapshot.repo, "rev-parse", snapshot.snapshot + "^{tree}").decode().strip()
    spec = {"schema": 1, "authority_effect": "None", "source_snapshot": snapshot.snapshot, "source_tree": tree,
        "checks": [{"id": "fixture-check", "checked_head": snapshot.snapshot, "checked_tree": tree,
                    "command": ["synthetic-check"], "exit_code": 0, "log_sha256": "1" * 64, "scope": "Synthetic test only."}],
        "reviews": [{"historical_handoff_id": "handoff:" + row[0],
            "sources": [next(block["source"] for block in population if block["source"]["path"].startswith(row[1]))],
            "scope": "Synthetic wording correction.", "remaining_obligations": "No mathematical result is supplied.",
            "check_ids": ["fixture-check"], "disposition": "WORDING_NARROWED"} for row in HANDOFF_SUBJECTS]}
    historical = {"source_snapshot": git(snapshot.repo, "rev-parse", snapshot.snapshot + "^1").decode().strip(),
                  "items": [{"id": "handoff:" + row[0]} for row in HANDOFF_SUBJECTS]}
    return spec, snapshot, historical, population


def test_versioned_correction_remains_distinct_from_mathematical_evidence(sample: tuple[Any, ...]) -> None:
    result = ingest(*sample)
    assert len(result["records"]) == 12
    assert result["historical_evidence_retained"]
    assert not result["all_headlines_supported"]
    assert {row["mathematical_status"] for row in result["records"]} == {"OPEN"}


@pytest.mark.parametrize("mutation,error", [
    ("missing_owner", "CORRECTION_POPULATION_MISMATCH"),
    ("duplicate_owner", "CORRECTION_POPULATION_MISMATCH"),
    ("wrong_tree", "CORRECTION_CHECK_WRONG_TREE"),
    ("failed_check", "CORRECTION_CHECK_FAILED"),
    ("missing_check", "CORRECTION_CHECK_LINK_MISSING"),
    ("stale_span", "SOURCE_REFERENCE_MISMATCH"),
    ("promote", "CORRECTION_DISPOSITION"),
    ("off_subject", "CORRECTION_SUBJECT_SOURCE_MISSING"),
])
def test_correction_mutations(sample: tuple[Any, ...], mutation: str, error: str) -> None:
    original, snapshot, historical, population = sample
    spec = deepcopy(original)
    if mutation == "missing_owner":
        spec["reviews"].pop()
    elif mutation == "duplicate_owner":
        spec["reviews"].append(deepcopy(spec["reviews"][0]))
    elif mutation == "wrong_tree":
        spec["checks"][0]["checked_tree"] = "0" * 40
    elif mutation == "failed_check":
        spec["checks"][0]["exit_code"] = 1
    elif mutation == "missing_check":
        spec["reviews"][0]["check_ids"] = ["absent"]
    elif mutation == "stale_span":
        spec["reviews"][0]["sources"][0]["span_sha256"] = "0" * 64
    elif mutation == "off_subject":
        spec["reviews"][1]["sources"] = spec["reviews"][0]["sources"]
    else:
        spec["reviews"][0]["disposition"] = "PROVED_THEOREM"
    with pytest.raises(ValueError, match=error):
        ingest(spec, snapshot, historical, population)


def test_original_snapshot_cannot_be_presented_as_a_correction(sample: tuple[Any, ...]) -> None:
    spec, snapshot, original, population = sample
    historical = {**original, "source_snapshot": snapshot.snapshot}
    with pytest.raises(ValueError, match="CORRECTION_REQUIRES_NEW_SOURCE_VERSION"):
        ingest(spec, snapshot, historical, population)


@pytest.mark.parametrize("returncode", [1, 128])
def test_unmerged_or_unavailable_main_ref_is_refused(monkeypatch: pytest.MonkeyPatch, returncode: int) -> None:
    monkeypatch.setattr("corrections.subprocess.run", lambda *args, **kwargs: SimpleNamespace(returncode=returncode))
    with pytest.raises(ValueError, match="CORRECTION_NOT_MERGED"):
        require_merged(HERE, "0" * 40)


def test_unpublished_correction_review_is_refused() -> None:
    """No version is current while the owner review file is absent."""
    assert not REVIEW_FILE.is_file()
    assert not OUTPUT.is_file()
    with pytest.raises(FileNotFoundError):
        build()
